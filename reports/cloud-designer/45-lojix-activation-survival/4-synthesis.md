# 45/4 — lojix S4 synthesis: activation + disconnect-survival implementation plan

cloud-designer synthesis over the three S4 recon files (1 pipeline/activation
stub, 2 lojix-cli BootOnce, 3 disconnect-survival job model) plus a direct
source re-verification on `lojix` `main`, `meta-signal-lojix`, and
`signal-lojix`. Every line/shape claim below was re-confirmed against the
checkouts under `/git/github.com/LiGoldragon`. Read-only; nothing mutated; no
live deploy (that is S5). Spirit gate: task-only synthesis order → no capture.

## What S4 delivers

1. **Closure-threading** — carry the real built `/nix/store/...` path through
   `CopyClosure` and `ActivateGeneration` so both are target-safe, fixing the
   unset-`$CLOSURE` activation bug.
2. **Reject-guard opening** — flip `unsupported_deploy_reason` so the now-safe
   activating actions enter the pipeline instead of being rejected.
3. **BootOnce parity** — port `lojix-cli`'s `systemd-run --collect`
   PID-1 transient-unit activation so a daemon->target SSH drop leaves the
   activation running to completion on the node.
4. **Disconnect-survival job model (up9q)** — a daemon-owned deploy job actor
   that owns the pipeline + external process and persists job state, so a
   client->daemon socket drop does not abort the deploy.

Ordering rationale: items 1+2 are pure schema/runtime changes provable by the
existing unit/contract tests and must land first (they unblock everything and
carry the lowest risk). Item 3 is a command-shape port, unit-testable at the
`NixCommand` construction level. Item 4 is the architectural change with the
broadest blast radius (`serve_owner`, a new sema family, a new actor) and lands
last, built on the durable phase substrate the earlier items exercise.

## Decisive findings from re-verification (shape the plan)

- **The built closure path is already on the cursor.** The `ClosureBuilt` arm
  (`schema_runtime.rs:845-846`) calls `set_closure_path(built.closure_path)`,
  and `activation_commit` (`:366`) already reads `self.closure_path`. So the
  closure is captured and stored; the *only* gap is that
  `activate_generation_command` (`:357`) does not put it on the command and
  the schema record has no field for it. The fix is a field add + one threading
  line, mirroring `copy_closure_command` (`:345`) which already takes it.

- **The wire reply contract is already up9q-shaped.** The meta success reply is
  `Deployed AcceptedDeploy { DeploymentIdentifier * DatabaseMarker * }`
  (`meta-signal-lojix/schema/lib.schema:65,114`) — an *accepted-handle* shape
  with a deployment identifier, NOT a terminal "fully applied" payload. The
  client is already meant to receive a handle and observe progress separately.
  This means surface (a) of up9q needs no wire-contract change: reply with the
  accepted handle immediately, then run the pipeline detached.

- **The observe surface already exists.** `WatchDeployments DeploymentWatch {
  deployment (Optional DeploymentIdentifier) ... }` ->
  `Watching SubscriptionOpened` (`signal-lojix/schema/lib.schema:27,77`), and
  `DeploymentPhaseEvent` carries `DeploymentIdentifier * ... DeploymentPhase *
  EventLogPosition *` (`:90-100`) with phases
  `[Submitted Building Built Copying Activating Activated Failed]`. Phase
  transitions already land durably in the event-log table
  (`sema.rs:104,309,513,573`). So a reconnecting client re-observes by
  `DeploymentIdentifier`. CAVEAT: live event *push* is only half-wired —
  `open_subscription` (`schema_runtime.rs:489-499`) returns the token handshake
  but the daemon does not yet stream `DeploymentPhaseEvent`s to a watcher
  (the schema comment at `signal-lojix/schema/lib.schema:14` flags the handshake
  as the implemented part). Reconnect-by-Query against the durable event-log is
  available now; live push is a separable follow-on, not an S4 blocker.

## Step 1 — Closure-threading (unit-testable, lands first)

The seam is `ActivateGenerationCommand`, which today is
`{ GenerationIdentifier * ClusterName * NodeName * ActivationKind * }`
(`schema/nexus.schema:67`) — no closure. `CopyClosureCommand` already has the
`ClosurePath` (`:66`) and `run_copy_closure` copies the real path, so copy is
already correct; only activate is broken.

Steps:

1. **Schema** — add `ClosurePath *` to `ActivateGenerationCommand` in
   `lojix/schema/nexus.schema:67`:
   `{ GenerationIdentifier * ClusterName * NodeName * ClosurePath * ActivationKind * }`.
   Regenerate `src/schema/nexus.rs` via the build. No back-compat concern
   (pre-production, hard override).
2. **Command builder** — `activate_generation_command` (`schema_runtime.rs:357`)
   takes a `closure_path: ordinary::ClosurePath` argument and sets the new
   field, exactly mirroring `copy_closure_command` (`:345`). Thread the value
   the same way the `ClosureBuilt` arm threads it into copy: from
   `pipeline.closure_path` (already set), or carry `built.closure_path` forward
   through the `Copying` -> `advance_after_phase` hop that fires
   `ActivateGeneration` (`:669`). Since the cursor field is already populated by
   `set_closure_path`, reading `self.closure_path` at the activate-command
   construction site is the minimal, correct source.
3. **Command shape** — replace `NixCommand::activate_system(node_name)`
   (`schema_runtime.rs:1898-1908`) with
   `activate_system(node_name, closure_path, activation_kind)` that substitutes
   the real store path inline (no `$CLOSURE`) and runs the kind-appropriate
   `switch-to-configuration`. The `activation_slot` mapping (`:1418`,
   `ActivationKind -> GenerationSlot`) is mirrored into the switch sub-command
   (`switch`/`boot`/`test`). This is also where the per-action BootOnce/EFI
   machinery from Step 3 plugs in.
4. **Call site** — `run_activate_generation` (`:1400-1416`) passes
   `command.closure_path.payload()` and `&command.activation_kind` into the new
   constructor.

Testable now (no live target): the `ClosureBuilt` arm already fires
`CopyClosure(closure_path)` and the engine-routing tests drive the full cursor.
Add a unit/contract test asserting that an activating deploy, once past the
guard, fires an `ActivateGeneration` effect whose command carries the same
non-empty `ClosurePath` that `ClosureBuilt` produced — i.e. the path is no
longer dropped between build and activate. Assert the `NixCommand` argv built by
`activate_system` contains the literal store path and the correct
`switch-to-configuration <kind>` and contains NO `$CLOSURE` token. None of this
needs a node — it is pure command construction + cursor threading.

## Step 2 — Open the reject-guard for now-safe actions (unit-testable, lands with Step 1)

`unsupported_deploy_reason` (`schema_runtime.rs:559-575`) today accepts only
System `Eval | Build` and Home `Build`; the `activates()` set is rejected
`UnsupportedDeployAction`. Once Step 1 makes activate target-safe, flip the
guard so System `Boot | Switch | Test | BootOnce` and Home `Profile | Activate`
are supported. The pipeline machinery (stages, phase records, the `activates()`
branch firing `CopyClosure` -> `ActivateGeneration`) is already wired and
waiting; only the guard and the activate command shape block it.

What opens vs what stays rejected:

| Request | Action / mode | Before S4 | After S4 |
|---|---|---|---|
| System | `Eval` | accepted (drv only) | accepted (unchanged) |
| System | `Build` | accepted (closure, stops) | accepted (unchanged) |
| System | `Switch` | rejected | **opens -> pipeline** |
| System | `Boot` | rejected | **opens -> pipeline** |
| System | `Test` | rejected | **opens -> pipeline** |
| System | `BootOnce` | rejected | **opens -> pipeline** |
| Home | `Build` | accepted (closure, stops) | accepted (unchanged) |
| Home | `Profile` | rejected | **opens -> pipeline** |
| Home | `Activate` | rejected | **opens -> pipeline** |

`UnsupportedDeployAction` does not disappear from the enum — it remains the
honest reply for any future not-yet-implemented shape (the audit-29 honesty
rule, `meta-signal-lojix/schema/lib.schema:122-126`). `InternalError`,
`DeploymentInFlight`, and the unreachable/malformed reasons are unaffected.

Lock-test update: `tests/engine_routing.rs:167-180`
`activating_deploy_is_rejected_until_activate_lands` currently asserts a System
`Switch` replies `UnsupportedDeployAction`. Rewrite it (rename to
`activating_deploy_enters_effect_pipeline`) to assert the System `Switch` now
passes the guard and reaches the pipeline, failing only at the bogus-fixture IO
stage with `ProposalSourceUnreachable` — exactly matching the sibling tests
`production_deploy_without_build_attribute_enters_effect_pipeline` (`:182`) and
`home_build_enters_effect_pipeline` (`:194`). Add a Home `Activate` twin.

Testable now: entirely unit/contract — the guard is a pure function over
`DeployRequest`, and the routing tests drive the cursor with bogus sources, so
no node is required to prove the guard opens and the pipeline is entered.

## Step 3 — Port lojix-cli BootOnce + the rest of the activation matrix (mostly unit-testable)

This is the `daemon->target` survival surface and the per-action activation
parity bar. All of it is `NixCommand` (argv) construction plus the activation
script string; the construction is unit-testable, the *behavior* needs S5.

Port targets (source of truth `lojix-cli/src/activate.rs`, `copy.rs`,
`host.rs`):

1. **SSH addressing** — port `SshTarget` (`host.rs:20-21,49-55`): activate/copy
   address `root@<criome_domain_name>`, never the bare `NodeName`. Recon 1
   (`:234-240`) and recon 2 (`:175`) both flag the bare-`node_name` target as a
   second target-safety gap beyond `$CLOSURE`. The daemon must resolve the
   node's Criome domain (or ygg address per `lojix/INTENT.md:94-97`) before
   building the ssh/copy argv. NOTE: the address source (projected horizon's
   `criome_domain_name`) must be available on the cursor; if it is not yet
   carried, that is an additional field to thread (verify against the horizon
   projection — flagged as an open question below).

2. **Copy** — port `ClosureCopy` (`copy.rs:35-67`): always pass
   `--substitute-on-destination` (target pulls signed paths from the cluster
   cache; raw daemon-to-daemon transfer is unsigned and rejected under
   `require-sigs`); three cases — dispatcher source -> `--to` only; builder ==
   target -> skip (already present); builder != target ->
   `--from ssh-ng://<builder> --to ssh-ng://<target>`. Replace the bare
   `copy_closure` stub (`schema_runtime.rs:1886-1896`). Copy is idempotent and
   re-runnable, so it does NOT need a transient unit (recon 3 `:161`).

3. **Per-action System activation** (`activate.rs`):
   - **Test** (`:58-65`) — ssh runs only
     `<store>/bin/switch-to-configuration test`; no profile set, no bootloader.
   - **Boot / Switch** (`:58-69`) — one ssh:
     `nix-env -p /nix/var/nix/profiles/system --set <store> &&
     <store>/bin/switch-to-configuration <boot|switch>`, THEN the EFI reconcile
     (`:177-230`): ssh `readlink /nix/var/nix/profiles/system` -> parse
     `system-N-link` -> derive `nixos-generation-N.conf` ->
     `bootctl set-default <entry>` + `bootctl set-oneshot ''`. Reason: s-t-c
     writes `loader.conf` default but not the EFI `LoaderEntryDefault`, so a
     stale one-shot from a prior BootOnce could hijack the next boot.
   - **BootOnce** (`:128-147`, `run_boot_once` `:232-255`) — the
     disconnect-survival mechanism (Step 3 below).

4. **BootOnce transient unit** — port `activate.rs:135-147`:
   `ssh -o BatchMode=yes root@<node>.<cluster>.criome
   'systemd-run --unit=<unit> --collect --wait --service-type=oneshot
   /bin/sh -c <script>'`. `--unit` = `lojix-boot-once-<secs:x>-<pid:x>`
   (`unit_name()` `:75-82`) so concurrent deploys do not collide and the
   operator can grep the journal unit after a drop. PID 1 owns the unit, so an
   ssh blip leaves it running to completion; ssh holds open only as a live
   stdout/stderr channel and `--wait` returns the unit's exit code. `--collect`
   reaps the finished transient unit. No `--pipe`/`--pty` (stdio inherits the
   ssh channel). On ssh error, surface the re-attach affordance
   `ssh <target> journalctl -u <unit>.service`.

5. **BootOnce entry-staging script** — port `boot_once_script()`
   (`activate.rs:92-126`): seed `PATH`
   (`/run/current-system/sw/bin:/run/wrappers/bin:$PATH` — transient units get a
   minimal PATH); `CLOSURE='<store>'`;
   `OLD=$(bootctl status | awk '/Current Entry:/...')` (the RUNNING generation's
   EFI Current Entry, not `loader.conf` default);
   `nix-env --set "$CLOSURE"`; `"$CLOSURE/bin/switch-to-configuration" boot`;
   derive `NEW="nixos-generation-$GENERATION.conf"` from the
   `readlink /nix/var/nix/profiles/system` target (canonical latest, not
   `bootctl` Default which can be stale); assert
   `[ -f /boot/loader/entries/$NEW ]` and `[ "$NEW" != "$OLD" ]`;
   `bootctl set-default "$OLD"` + `bootctl set-oneshot "$NEW"`. Net: reboot 1
   lands NEW, reboot 2+ auto-returns to OLD — headless-safe rollback. (Recon 2
   `:97-100` flags drift from report 39: trust the source — NEW from `readlink`,
   OLD from Current Entry.)

6. **Home Profile/Activate** (`activate.rs:266-353`) — port
   `nix-env -p $HOME/.local/state/nix/profiles/home-manager --set <store>` as
   the target user, then for `Activate` run `<store>/activate`; include the
   local fast-path (skip ssh entirely when the dispatcher already is the
   requested user on the target node, `:331-352`).

Testable now (no node): every command above is a `NixCommand` argv plus a
script string. Add construction-level unit tests asserting the exact argv per
action — that BootOnce builds `systemd-run --unit=lojix-boot-once-... --collect
--wait --service-type=oneshot`, that Boot/Switch emit the s-t-c plus the EFI
reconcile commands, that copy always carries `--substitute-on-destination` and
the right `--from`/`--to`/skip case, and that the address is
`root@<domain>` never bare node. The BootOnce script can be snapshot-tested as a
string. What needs S5: that the unit actually survives the drop, that EFI
set-default/set-oneshot land correctly, and that the node boots NEW then rolls
back to OLD.

## Step 4 — Disconnect-survival job model (up9q) — lands last

This is the `client->daemon` survival surface. Today the entire pipeline runs
synchronously inside the owner-connection future: `serve_owner`
(`daemon.rs:275-290`) reads one request, awaits the full `execute_with_store`
continuation loop (`:321-338`) eval->build->copy->activate->record, then writes
the single reply. The deploy lives entirely inside the `tokio::spawn`ed
connection task (`handle_connection` `:223-235`); a client drop drops that task
and the in-flight deploy dies with its child processes. There is no persisted
in-flight job and no resume-mid-pipeline (only committed phase rows survive).

Design (up9q-compliant, both surfaces):

1. **Daemon-owned deploy job actor.** Use the in-house kameo actor framework
   (`triad-runtime` re-exports `pub use kameo`, `lib.rs:22`; the only current
   `impl Actor` is `RequestGate` for admission permits). On `Deploy`,
   `LojixRuntime` spawns a long-lived deploy job actor whose `ActorRef` is held
   on the *runtime*, not the connection worker. The actor owns the
   `execute_with_store` continuation loop and the external `tokio::process`
   children. A dropped client kills only the short request task; the job actor
   runs to completion. Kill-on-drop is explicitly OFF for the job — that is the
   point.

2. **Reply immediately with the accepted handle.** `serve_owner` no longer
   awaits the pipeline. It records the submission, spawns the job actor, and
   replies `Deployed(AcceptedDeploy { DeploymentIdentifier, DatabaseMarker })`
   at once — which the wire contract already is (no schema change for the happy
   path). The `DeploymentIdentifier` is the job's durable handle.

3. **Persist job state.** Add a `DeployJob` sema family alongside the four in
   `lib.rs:44-61` (live-set, gc-roots, event-log, container-lifecycle): job id =
   `DeploymentIdentifier`, phase cursor mirroring `DeployStage`
   (`schema_runtime.rs:131-142`), closure path, resolved target address, and
   (Step 3) the BootOnce unit name. On daemon restart the persisted job row
   makes the in-flight deploy resumable (same self-resume discipline as the
   committed-state resume in `durable_resume.rs`). A resumed job whose recorded
   phase is `Activating` polls the BootOnce transient unit via
   `journalctl -u <unit>` rather than blindly re-running activation; copy, being
   idempotent, is safe to re-run.

4. **Client re-observes by identifier.** A reconnecting (or any) client uses the
   existing `WatchDeployments { deployment: Some(<id>) }` /
   `Query` surface against the durable event-log to learn outcome and progress.
   The phase records already land in the event-log table on every transition.
   Live event *push* to the watcher stream is the half-wired part
   (`open_subscription` returns only the token handshake today) and is a
   separable follow-on; reconnect-by-Query is sufficient for the up9q
   survival guarantee.

5. **Admission.** The 64-permit cap (`MAXIMUM_CONCURRENT_REQUESTS`,
   `daemon.rs:101,133`) currently gates connection tasks and a long deploy holds
   its permit for the whole run. With the job decoupled, the permit covers only
   the short submit-and-reply request; the job actor's concurrency is governed
   separately (a deploy-job cap on the runtime), and `DeploymentInFlight`
   (already in the rejection enum) becomes the honest reply when a node already
   has an in-flight job.

The two surfaces compose: the job actor + persisted job state make the deploy
outlive the client connection and the daemon process; the Step-3 BootOnce
transient unit makes the remote activation outlive the daemon->target ssh. Both
are required; neither alone satisfies up9q.

Testable now (no node): the actor lifecycle and decoupling are unit-testable —
that `serve_owner` returns the accepted handle before the pipeline completes
(inject a slow/blocked effect and assert the reply arrives first); that
dropping the request task does not cancel the job actor; that the `DeployJob`
row is written on submit and updated per phase; that a constructed job actor
resumes from a persisted `Activating` row by polling rather than re-activating.
What needs S5: that a real client SSH drop mid-deploy leaves the node correctly
deployed, and that daemon restart mid-`Activating` resumes against a live
transient unit.

## Risk table

| # | Risk | Surface | Mitigation | Proven by |
|---|---|---|---|---|
| R1 | Schema regen breaks downstream rkyv/wire consumers | Step 1 schema | Pre-production, no back-compat owed; regenerate all consumers in one change; full build + routing tests | Unit |
| R2 | Closure path threaded as empty string (the `unwrap_or_else("")` in `activation_commit` `:366` masks a missing path) | Step 1 | Make the activate command require a non-empty `ClosurePath` and assert it in the routing test; remove the empty-string fallback once the field is mandatory on the command | Unit |
| R3 | Opening the guard lets a genuinely-unsafe action through if Step 1 is incomplete | Step 2 | Land Step 1 + Step 2 in the same change; keep `UnsupportedDeployAction` for future shapes; the rewritten lock test fails loudly if activate is not wired | Unit |
| R4 | Bare `NodeName` target instead of `root@<criome_domain>` mis-addresses or fails to reach the node | Step 3 | Port `SshTarget` addressing; assert `root@<domain>` in argv tests; confirm the domain is carried on the cursor (open question Q1) | Unit (argv) + S5 (reach) |
| R5 | BootOnce EFI reconcile leaves a stale one-shot or wrong default, bricking headless boot | Step 3 | Faithful port of the Current-Entry(OLD)/readlink(NEW) script incl. the `[ -f ]` and `[ NEW != OLD ]` asserts; snapshot-test the script | S5 only |
| R6 | `--substitute-on-destination` omitted -> unsigned path rejected under `require-sigs` | Step 3 | Always pass it (faithful `copy.rs` port); argv test asserts presence | Unit (argv) + S5 |
| R7 | Job actor leak / unbounded concurrent deploys after decoupling from the connection permit | Step 4 | Runtime-level deploy-job cap; `DeploymentInFlight` reply when a node has an in-flight job; supervised kameo spawn | Unit |
| R8 | Resumed job re-runs activation and double-switches instead of polling the unit | Step 4 | Persist the BootOnce unit name; resumed `Activating` job polls `journalctl -u <unit>`; copy is idempotent so re-run is safe | Unit (resume logic) + S5 (real unit) |
| R9 | Client cannot learn outcome because live event push is unwired | Step 4 | Rely on reconnect-by-Query against the durable event-log (already written per phase); treat live push as a separable follow-on, not an S4 blocker | Unit |
| R10 | Spirit daemon down blocks reconfirming up9q/1lex/xv9v/kx32 against the record store | Cross-cutting | Design is grounded in code + `lojix/INTENT.md:82-86` which paraphrases up9q verbatim; flag the Spirit daemon `start-limit-hit` to operator/system-maintainer | n/a |

## Open questions for the psyche

1. Is the node's `criome_domain_name` (or ygg address) already carried on the
   deploy cursor / horizon projection, or is it a new field to thread for
   Step 3 addressing? Recon did not confirm the address source on the lojix
   side (lojix-cli reads it from the projected horizon).
2. For Step 4, is reconnect-by-Query an acceptable S4 endpoint, deferring live
   `DeploymentPhaseEvent` push to a follow-on — or must live push land in S4?
3. Should `DeploymentInFlight` be enforced per-node (one active deploy per node)
   or per-cluster in the new job-admission path?
4. The Spirit daemon is down (`spirit-daemon.service` `start-limit-hit`,
   `ExecStartPre` `spirit-upgrade-store` exits 1) — out of cloud-designer
   scope; who picks up the store-upgrade fix?
