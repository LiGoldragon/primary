# 10 — verdict: is the new lojix logic stack ready for production?

cloud-designer, 2026-06-10. Synthesis of eight adversarially-verified dimensions
(workflow `lojix-production-readiness`, 18 agents) plus the completeness critique
(file 9). The highest-numbered file IS the synthesis.

## Verdict: NOT READY — and the gap is foundational, not cosmetic

The new lojix stack is **not** a production replacement for `lojix-cli` today.
The code that exists is genuinely high-grade — actor-native, non-blocking by
construction, clean wire contracts, typed errors, green build — but a deploy
tool is judged by whether it can *deploy*, and this one cannot yet activate a
single real node, breaks the build for secret-bearing nodes, and has no migrated
consumer. The engineering substrate is production-shaped; the deploy capability
is not.

The honest framing the critique forced: there are **three different bars**, and
lojix sits at a different place against each.

| Bar | What it means | lojix status |
|---|---|---|
| **Minimal `lojix-cli` parity** | build + activate one node on demand | **Blocked** — cannot activate; secrets break eval for WPA3/LLM nodes; OsOnly builds a *different* closure |
| **The daemon's fuller charter** | durably own the cluster-wide live set, GC-roots retention, event log | **Blocked + partly unbuilt** — all state in-memory; `Retire` reclaims nothing; GC is dead code |
| **Cutover precondition** | a consumer actually consumes the daemon | **Unstarted** — both CriomOS and CriomOS-home still pin legacy `lojix-cli` |

## Ranked gates

### Strict-parity blockers (these alone settle "not ready")

1. **The daemon cannot activate any real node deploy.** The single guard on the
   only Deploy entry point (`unsupported_deploy_reason`,
   `schema_runtime.rs:525-541`, called once at `:486`) admits **only** System
   `Eval`/`Build` and Home `Build`; every activating action — System
   Boot/Switch/Test/BootOnce, Home Profile/Activate — is rejected up front with
   `UnsupportedDeployAction` (test `activating_deploy_is_rejected_until_activate_lands`,
   `engine_routing.rs:163`). And the effect bodies *behind* the guard are broken:
   `activate_system` (`:1819-1829`) ssh-runs `nix-env -p … --set "$CLOSURE"` with
   `$CLOSURE` an **unset shell variable**, never assigns the real closure path,
   and never calls `switch-to-configuration` despite its comment; `copy_closure`
   (`:1807-1817`) targets the bare horizon `node_name` over `ssh-ng://` with no
   `criome_domain_name` resolution. `lojix-cli/src/activate.rs` implements the
   full set (switch-to-configuration, real-path `nix-env --set`,
   bootctl set-default/set-oneshot, `systemd-run --wait --collect`, EFI
   reconcile). *Remedy:* implement target-safe copy/activate (domain-resolved SSH
   host, interpolated closure path, switch-to-configuration, BootOnce transient
   unit + bootctl oneshot + EFI reconcile, Home profile/activate as the requested
   user), then lift the guard — with end-to-end tests against a real
   `nixosSystem`, not the echo-ok fixture.

2. **The production `secrets` override is never materialized — this breaks BUILD,
   not just activate.** lojix-cli injects four overrides
   (horizon/system/deployment/**secrets**); the new daemon's
   `MaterializedInputSet::write` (`schema_runtime.rs:1506-1532`) emits only three,
   and `MaterializationShape` (`nexus.schema:59`) has no `Secrets` variant.
   `CriomOS/modules/nixos/router/default.nix:36` **throws at eval time** when
   `inputs.secrets.sopsFiles.<wifi-password>` is absent. So for a router node
   with `wpa3SaePassword` set (and LLM-enabled nodes, `llm.nix:163`), the new
   daemon's build fails to *evaluate* — defeating the one capability it claims.
   *Scope:* those node kinds, not all nodes. *Remedy:* add a `Secrets`
   materialization shape mirroring `lojix-cli` `artifact.rs` and inject
   `--override-input secrets`.

3. **OsOnly deploys build a different closure than lojix-cli (firmware policy).**
   (Critique B.) New daemon emits `includeAllFirmware` in the deployment input
   (`schema_runtime.rs:1612-1638`) where lojix-cli emits only `includeHome`
   (`lojix-cli/src/build.rs:85-91`). For an OsOnly deploy this flips
   `enableAllFirmware` false→true (`metal/default.nix:36`,
   `checks/metal-firmware-policy/`). A real build-correctness divergence in the
   one working capability. *Remedy:* reconcile the deployment-input field set
   against lojix-cli and pin it with the firmware-policy check.

### Fuller-charter blocker (conditional on the psyche's cutover-scope decision)

4. **All daemon state is in-memory and lost on every restart; GC-retention is
   unbuilt and latently unsafe.** `StoreState` is four `Vec` tables behind one
   `Mutex` with counters minting from 0 (`lib.rs:121-198`); the actor `start()`
   hook is a no-op (`daemon.rs:153-155`); there is **no redb/sema-engine dep in
   the tree at all** — ARCHITECTURE.md:50-51's "BTreeMap persisted via
   sema-engine" overstates reality. So a restarted daemon cannot self-resume,
   violating its own invariant. And (critique A) `Retire` only pops an in-memory
   `Vec` — it deletes no gcroot symlink and frees no store path; the
   `nix-store --gc` effect is dead code, and would be **rootless-unsafe** if wired
   (no on-disk gcroots to protect the running closure). **But** `lojix-cli` is
   itself stateless — so this blocks the daemon's *expanded charter*, not minimal
   parity. Whether durable state must land *before* the first cutover or can be
   sequenced after (against a small node set) is **the psyche's open question 2**,
   not a settled blocker. *Remedy:* land the redb/sema-engine backing + startup
   self-resume, write real gcroot symlinks, gate `nix-store --gc` with keep-roots,
   make `Retire` actually reclaim — OR decide the first cutover runs in-memory.

### Cutover precondition (largest body of remaining work; independent of code)

5. **Zero consumers migrated.** CriomOS (HEAD `b63d922`) and CriomOS-home (HEAD
   `353b9a8`) flake.locks both pin legacy `lojix-cli` (rev `fc2ff02`) with **no**
   reference to the new repo/daemon/socket/signal-lojix anywhere. The new stack's
   invocation model (long-lived daemon + two sockets + thin client speaking
   signal-lojix frames) is fundamentally different from lojix-cli's flake-app CLI;
   migrating requires moving override-writing + substituter resolution into the
   daemon/request-builder, adding the flake input, repointing locks, and running
   both in parallel switching one consumer at a time. Per cutover discipline the
   old cannot retire until this completes — and it is unstarted.

### Discipline / hygiene gaps (land before the privileged surface carries authority)

6. **Daemon parses NOTA at startup — hard-override violation.** `lojix-daemon.rs:17`
   → `nota_config::…from_argv().decode()`; pinned nota-config `bd9173a`
   NOTA-decodes `InlineNota` text and `.nota` files un-gated. Daemons must accept
   only pre-generated rkyv. *Remedy:* accept only the `RkyvFile` variant.
7. **Floating `branch=main` engine deps with a 404'd repo and a rename time-bomb.**
   `nota-codec.git` now 404s on the remote (the offline build survives only on a
   warm cargo cache; a cold clone or `cargo update` red-builds); and triad-runtime
   behind-window commit `0e1badc` renames the exact four symbols `daemon.rs` is
   built on (`ActorMultiListenerDaemon` etc → `Async*`), so a bump breaks the
   compile, while schema-rust-next (19 behind) would red the artifact-freshness
   check. *Remedy:* pin engine deps to explicit revs (or add a flake-level pin),
   resolve the nota-codec 404, coordinate the rename sweep + artifact regen.
8. **Push-not-pull subscription bridge is documented but unbuilt** (no registry /
   event push; client is one-shot — `schema_runtime.rs:460-475`, `client.rs:91-115`);
   **no subprocess timeout/kill** on nix/ssh (`:1838`); **owner authority rests on
   socket file-mode alone**, no SO_PEERCRED despite triad-runtime exposing the
   primitive ("audit R3"). All mitigated today (activate rejected, no consumer
   connects); land before real authority flows.

## What is genuinely production-grade already (credit where due)

- **Actor-native — the exact corrected shape report 35/36 demanded of `cloud`.**
  Consumes triad-runtime's kameo `RequestGate`-actor multi-listener; the
  `actor_native_runtime` test forbids the old sync markers and passes.
- **Non-blocking listener, compiler-enforced.** The `std::sync::Mutex` guard is
  `!Send` and cannot cross the generated `execute` future's `+Send` bound
  (`schema/nexus.rs:1476`) — a forced recompile proved no guard crosses an
  `.await`. The two authority sockets have independent concurrency gates (separate
  Semaphores, cap 64). This is the **inverse** of cloud's report-36 whole-daemon
  stall.
- **Wire contracts are clean, wire-only, fresh, and a strict superset** of
  lojix-cli's vocabulary (which has only 4 request variants and no
  pin/unpin/retire). `build.rs` freshness round-trips byte-clean offline.
- **Typed-error / panic discipline is clean** — one thiserror per-crate `Error`
  with `#[from]`, `unsafe_code=forbid`, zero unwrap/expect/panic/todo in
  hand-written src; lock poison maps to a typed error.
- **Build is green offline; the test suite is honest about its gaps** (it asserts
  the rejection and the handshake-stub rather than hiding them). The report-29
  adversarial-audit hardening genuinely landed in HEAD (`f84a8cf`).

## The decision is the psyche's — two questions gate everything

The audit grounds intent in INTENT.md + report-cited records, **not** a live
Spirit dump (the deployed spirit-daemon's schema was reported out of sync, so a
live Observe couldn't be made). Before any go decision:

1. **What is the exact parity bar for the first cutover?** Recorded intent is
   "reach parity, then switch one consumer at a time" (charter `tvbn`/`fe2j`) but
   the precise capability set was never enumerated (report 26 open Q1). Must the
   `secrets` override and horizon-resolved substituters be in parity-1, or can the
   first target only nodes that need neither?
2. **Is the first cutover allowed to run on in-memory state** (small node set)
   while durable redb/sema-engine backing lands next, or must persistence land
   **before** any consumer migrates? (report 26 open Q2 / record `v5d4` —
   explicitly undecided.) This decides whether gate 4 is a hard precondition or a
   sequenced follow-on.

Plus two engineering decisions surfaced: **where substituter node-name→cache-URL
resolution should live** now the daemon split removed lojix-cli's horizon-side
resolution (the wire currently carries pre-resolved url+key — operator
hand-resolves, or it moves into the daemon); and a **fresh live Spirit Observe**
to confirm no newer record green-lights cutover or redefines the bar.

## My read, held as a recommendation not a decision

**Not ready, and correctly so** — the activation gate alone is decisive, and the
secrets-eval break + firmware divergence mean even the "it can build" claim is
qualified. But the stack is **closer than the headline suggests**: the hard part
(a correct, actor-native, non-blocking, typed daemon spine with clean contracts)
is *done and verified*, which is exactly what cloud still lacks. The remaining
work is well-scoped deploy plumbing (copy/activate, secrets, durable state) plus
the consumer migration — not a redesign. The fastest honest path to a *first*
production cutover is: implement+test target-safe activate, add the secrets
override, reconcile the firmware field, then — per the psyche's answer to Q2 —
either land durable state or pick a first-cutover node set that tolerates
in-memory, and migrate one consumer in parallel with lojix-cli still live.
