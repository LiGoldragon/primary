# 6 — Adversarial verification of finders 1-5 (lojix triad M1 audit)

cloud-designer verifier sub-agent, 2026-06-05. READ-ONLY. I re-read every
cited `file:line` in the pushed `triad-port` copies for each claimed flaw and
either CONFIRMED it (with the bytes I saw) or REFUTED it. Default verdict was
REFUTED until the file proved the claim. Where two finders made the SAME
claim from different angles I note the convergence; where two finders
CONTRADICT each other (F4 vs P3) I adjudicate against the source. The
orchestrator should fix only the CONFIRMED rows.

## Method note

Files re-read in full or in the cited regions:
`lojix/triad-port/src/schema_runtime.rs` (the M1 effect bodies, the
`DeployStage`/`DeployAction` machine, the sema writes, the reason maps,
`NixCommand`), `lib.rs` (`StoreState` counters, `Error`, `DaemonConfiguration`),
`daemon.rs` (the two-socket runtime + `execute` fallback), `client.rs`,
`schema/nexus.rs` (the generated command/result structs),
`triad-runtime/src/{frame.rs,daemon.rs,runner.rs}`,
both contracts' `schema/lib.rs` short-header modules, the meta `schema/lib.schema`,
`tests/build_smoke.rs`, and the legacy `lojix-cli/src/{build.rs,activate.rs}`
for parity. Two `grep` sweeps confirmed the ABSENCE claims (no
`set_read_timeout`/`SO_PEERCRED`/`thread::spawn`/`Error::EffectFailed`
construction).

## Verdict table — every claimed flaw

| Claim | Finder(s) | Verdict | Evidence (file:line) |
|---|---|---|---|
| **F1** build feeds eval'd `.drv`, not `<flake>#<attr>`; diverges from legacy | 1 | **CONFIRMED** | `run_nix_eval:1113-1117` captures `eval_drv_path` (the `.drvPath`) as `closure_path`; `nix_build_command` feeds it to `build_closure:1235-1245` = `nix build <drv>`. Legacy `build.rs:300-302` builds `target_attr` (the attribute) directly with `--refresh --print-out-paths`. Substituters/overrides ride the legacy build, not the new one. |
| **F2** `NixBuildCommand.substituters` never read | 1 | **CONFIRMED** | Field exists `nexus.rs:94` (`substituters: Vec<ExtraSubstituter>`); `run_nix_build:1122-1140` reads only `target`/`closure_path`/`generation_identifier`. Legacy emits `extra-substituters` (`build.rs:333`). |
| **F3** production eval has no `--override-input` | 1 | **CONFIRMED (known-deferred M3)** | `nix_eval_command:231-239` carries no override data; `run_nix_eval:1111-1119` emits `nix eval <flake>#<attr>.drvPath` with no `--override-input`. Schema comment `meta lib.schema:84` HONESTLY documents "no override-inputs". The actionable part is the **missing reject-guard**, not the absence itself. |
| **F4** no in-flight guard → second Deploy clobbers a live pipeline cursor (cross-deploy leak) | 1 | **REFUTED as stated; downgraded to latent (= P3)** | `record_deploy_submitted:764` does set `active_deploy` unconditionally — but the premise "socket loop interleaves deploy-2 between decide calls" is FALSE. `Runner::drive` (runner.rs:156-185) loops to `NextStep::Reply` on `&mut self`; `try_serve_next_stream` (triad-runtime daemon.rs:368-380) calls `handle_stream` synchronously and accepts no next stream until it returns; no `thread::spawn`/async in lojix src (grep). A deploy runs to completion inside ONE `execute`; `active_deploy` is always `None` between requests. The clobber cannot occur today. Valid only as the defensive-guard half of P3. |
| **F5** copy/activate ssh the bare node, not the criome domain | 1, 5 | **CONFIRMED, but KNOWN-DEFERRED (A3)** — not a re-reportable flaw | `copy_closure:1261-1271`/`activate_system:1273-1283` address bare `node_name`. Brief lists A2/A3 addressing as deferred. The actionable residue is the reject-guard ask (overlaps F3). |
| **F6 / 5.1** `activate_system` ships literal `$CLOSURE`, never exported; drops `switch-to-configuration` → activate is a no-op | 1, 5 | **CONFIRMED (actively broken, not merely deferred)** | `activate_system:1280` = `nix-env ... --set "$CLOSURE"`; `run:1292-1308` sets no `.env`; `ActivateGenerationCommand` (nexus.rs:108-113) carries no closure path; `activate_generation_command:274-281` drops the stored `closure_path`. Legacy Switch (`activate.rs:59-63`) interpolates the real `{store}` AND runs `switch-to-configuration {action}`. The legacy `$CLOSURE` form (activate.rs:111-116) DEFINES `CLOSURE='{store}'` first; the port copied the var, dropped the definition. |
| **F7** smokes assert only `Deployed`; reply carries no store path | 1 | **CONFIRMED** | `build_smoke.rs:57,71,150` match only `meta::Output::Deployed`; `AcceptedDeploy` (meta lib.schema:114 / lib.rs:132) = `{DeploymentIdentifier, DatabaseMarker}`, no path field. All three tests `#[ignore]`. |
| **F8** `first_line` of `nix flake metadata --json` grabs `{` as revision | 1 | **CONFIRMED but INERT** | `resolve_flake_auth:1102-1106` stores `first_line(output)` as `revision`; `first_line:1310-1312` takes line 0 of multi-line JSON. The `revision` field is never consumed downstream (silent-wrong-but-harmless today). Cleanup, not correctness. |
| **F9** `source`/`deployment_kind` inert on the override path | 1 | **CONFIRMED but LOW** | `nix_eval_command:235` passes `deployment_kind` to `NixEvalCommand`; `run_nix_eval:1111-1119` never reads it. Honest-schema; the ask is a reject-guard on contradictory input. |
| **W1** codec pre-allocates attacker length: 4 GiB OOM/DoS | 2 | **CONFIRMED** | `Default for LengthPrefixedCodec` (frame.rs:73-77) = `maximum_for_u32_prefix()` = `u32::MAX` (frame.rs:36-37). `read_body:110` `vec![0_u8; length]` BEFORE `read_exact:111`. Daemon uses `default()` (lojix daemon.rs:94). |
| **W2** connect-and-never-send wedges the serial daemon (no read timeout) | 2 | **CONFIRMED** | Listener non-blocking (triad-runtime daemon.rs:308); accepted `UnixStream` (daemon.rs:449-450) inherits nothing — no `set_read_timeout` anywhere (grep). Accept loop serial + synchronous `handle_stream` (daemon.rs:368-380). `read_exact` (frame.rs:107) blocks forever. |
| **W3** authority = socket-mode-only, mode is unvalidated config | 2, 5.5(adj) | **CONFIRMED** | No `SO_PEERCRED`/`peer_cred` anywhere (grep). `owner_socket_mode: u32` (lib.rs:96) → `from_mode(socket_mode.bits())` verbatim (triad-runtime daemon.rs:580), no floor. A config of 0o666/0o777 silently world-writable. |
| **W4** socket-mode TOCTOU (bind then chmod) | 2 | **CONFIRMED** | `bind_listener:551-556`: `prepare()` → `UnixListener::bind` → `apply_socket_mode()`. Socket exists at umask-default between bind and the next statement; parent dir `create_dir_all:565` at umask default. |
| **W5** one slow `nix build` blocks every socket (fully serial) | 2, 3(P3) | **CONFIRMED** | Serial accept (daemon.rs:368-380) + synchronous `handle_stream` + blocking `Command::output()` (schema_runtime.rs:1293-1296); no threading (grep). Ordinary socket unpolled for the build's duration. |
| **W6** `execute()` fallback drops owner deploys silently (EOF, no reply) | 2 | **CONFIRMED** | `execute:122-143` `_` arm hardcodes `OrdinaryOutput(QueryRejected)`; on owner path `meta_reply:154-161` returns `Err(UnexpectedFrame)` → `handle_owner` returns `Err` BEFORE `write_body` → `try_serve_next_stream` only logs (daemon.rs:372-375), connection dropped, client gets EOF. The comment at daemon.rs:128-129 asserts the invariant but nothing enforces it. |
| **W7 / 5.5** cross-contract replay rejected only incidentally; short header is not a contract discriminator | 2, 5 | **CONFIRMED (latent)** | meta `INPUT_DEPLOY=0x0`==ordinary `INPUT_QUERY=0x0`; all four ordinals collide exactly (`meta lib.rs:633-636` vs `signal lib.rs:930-933`). `handle_ordinary`/`handle_owner` bind contract by socket (daemon.rs:98-120), so a replayed meta frame is decoded as ordinary and rejected ONLY if rkyv layout diverges — incidental, not structural. The header has no tier bit. Same incidental disambiguation in `client.rs:79-90` ("headers are distinct" — false). |
| **W8** unbounded `eprintln!` error logging | 2 | **CONFIRMED but LOW** | `report_for_listener:151-160` (triad-runtime daemon.rs) is unrate-limited `eprintln!`. Malformed frames fail cleanly (no panic) — safe; only observability. |
| **P1** DeployStage name-vs-action mismatch (report-26 carryover) | 3 | **CONFIRMED as legibility, REFUTED as correctness** | `advance_after_phase:507-512` (`BuildingRecorded` fires `ActivateGeneration`), `:513-518` (`CopyingRecorded` fires the activation-record WRITE). Traced full Switch chain: no wrong effect fires on the happy path. Dual-driver (stage-keyed `advance_after_phase` + result-keyed `decide_effect_completion`) is a maintainability defect, not a break. |
| **P1b** Boot/Test/BootOnce record slot `Current` in the durable live-set | 3 | **CONFIRMED** | `activation_commit:288` hardcodes `GenerationSlot::Current`; `record_generation_activated:825,832` writes `commit.generation_slot` into live_set + gc_roots. The correct slot IS computed (`activation_slot:1168-1175`, used in the transient `ActivatedGeneration:1162`) but never threaded into the commit. A Boot is indistinguishable from a Switch durably. (Report-3's "dropped at 1161" phrasing is imprecise — the slot is used in the effect result, just not the commit — but the bug is real and correctly located at `activation_commit:288`.) |
| **P2 / P2b** `event_log_position` double-locked, non-atomic, `Vec::len()`-derived, no reservation | 3 | **CONFIRMED (latent: HIGH only if concurrent / on log compaction)** | `next_event_log_position:149-151` = `event_log.0.len() as u64`, `&self`, no increment — the lone non-counter among five `next_*` (commit/deployment/generation/subscription all `+= 1`, lib.rs:134-156). Read under two separate locks: `record_phase:702` then `record_phase_transition:786`. Same value today (single-thread, append-only); collides on concurrency or any log truncation. |
| **P3** single-slot fields safe only by undocumented single-thread run-to-completion; blocking build stalls all requests | 3 | **CONFIRMED** | `Runner::drive:156-185` runs to `Reply` on `&mut self`; daemon serial + no threading (grep). The invariant holds but is undocumented; the blocking `nix` effect (schema_runtime.rs:1293) means no request (not even a Query) is serviced during a build. This is the correct framing of what F4 mis-stated. |
| **P4** `reject_active_or_meta` `.unwrap_or(Deploy)` mis-types a `None` write-rejection | 3 | **CONFIRMED but LATENT** | `reject_active_or_meta:549` `.take().unwrap_or(MetaOperation::Deploy)`. On the meta path `active_operation` is always re-set on entry (388/402/406/410), so the default is unreachable today; it becomes reachable only paired with P5's leak + a stray completion (which P3 prevents). Real defensive gap, low urgency. |
| **P5** `fail_pipeline` clears `active_deploy` but NOT `active_operation` | 1 (note), 3 | **CONFIRMED** | `fail_pipeline:714-727` sets `active_deploy = None` (715) only; `finish_deploy_pipeline:530` clears both. Leak is masked by every meta op re-setting on entry, but it is the cleanest 1-line correctness fix. |
| **P6** three rejection-reason fallthroughs map to wrong/phantom reasons | 3 | **CONFIRMED** | `deploy_reason:608` `_ => DeploymentInFlight` swallows `PlanNotApproved` (the poisoned-lock reason, emitted at 775) → a lock error reported as "already deploying". `pin_reason:577` `_ => PinSlotExhausted` (a reason no sema path produces). `retire_reason:597` `_ => GenerationUnknown` even for existing generations. All three are wrong-diagnosis, not crashes. |
| **P6b** `record_generation_activated` back-channels `active_deploy` for fields the commit should carry | 3 | **CONFIRMED but LOW** | `record_generation_activated:807-817` reads `self.active_deploy` for `deployment_kind`/`activation_kind` with `.unwrap_or` defaults; `ActivationCommit` (activation_commit:283-291) doesn't carry them. Safe today (`Some` on happy path); same widen-the-record fix family as P1b. |
| **P7** `budget_exhausted_reply` always replies a META `DeployRejected` | 3 | **CONFIRMED but UNREACHABLE today** | `budget_exhausted_reply:1358-1365` hardcodes `MetaOutput(DeployRejected(...DeploymentInFlight))`; an ordinary caller would hit `ordinary_reply:150` `UnexpectedFrame`. But the happy Switch spends ~10/32 and no path emits `Continue` (grep) — not reachable. Latent wrong-reply + wrong reason. |
| **5.2 / 5.3** flake attribute is `String` end-to-end; `target_attribute()×2` return bare `String`; `FlakeAttribute` identity discarded | 5 | **CONFIRMED** | `FlakeAttribute = String` alias (meta lib.rs:69); `NixEvalCommand.attribute: String` (nexus.rs:85); `DeployAction::target_attribute:134-143` and `DeployPipeline::target_attribute:241-251` return `String`; override collapses `Option<FlakeAttribute>` → `String` (248). Three hand-`format!` sites (140, 1112, 1230). Typed-domain-value smell, real but cleanup-tier. |
| **5.4** `MetaOperation` is a hand-kept mirror of the meta `Input` discriminant | 5 | **CONFIRMED but LOW (defensible)** | `MetaOperation:35-41` + four `*_reason` maps with `_`-arms (572-610). A fifth meta verb would silently desync. Not a hard violation; sync-risk flag. |
| **5.6a** `Error::FlagArgument(String)` reused as a missing-feature message | 5 | **CONFIRMED** | `client.rs:73-74` returns `Error::FlagArgument("inline NOTA ... requires the nota-text feature")`; the variant's `#[error]` text (lib.rs:54-55) is about flag tokens. Wrong channel. |
| **5.6b** `Error::EffectFailed{stage:String}` re-stringifies typed `EffectStage` AND is never constructed | 5 | **CONFIRMED** | `Error::EffectFailed{stage:String,detail:String}` (lib.rs:69-70). grep: the only `EffectFailed` construction sites (635/685/1189) are the DIFFERENT `nexus::EffectResult::EffectFailed` type — the crate `Error::EffectFailed` has zero construction sites. Dead + typed-wrong variant. |
| **5.7** `bin/lojix-daemon.rs:16 fn run()` is a module-scope free function | 5 | **CONFIRMED (out of strict scope, LOW)** | `bin/lojix-daemon.rs` defines `fn run()` beside `fn main()`. Only `main`/`#[cfg(test)]` are exempt per intent 882. Trivial. |
| **(port)** HOLD the engine bump; trait surface signature-identical; streaming unreachable without feature work | 4 | **CONFIRMED (decision-level, with stated read-only limit)** | I did not re-run the fixture diff (read-only, same constraint), but the structural claims check out: lojix's generated code has zero `StreamingFrame`/`Subscription` surface (consistent with no `streams()` declaration), `open_subscription` is a token-handshake stub, and the `handle_stream` retain-stream gap is real (daemon.rs:98-120 reads one body / writes one reply). The HOLD rests on "no forcing function + streaming needs separate feature work", which the daemon shape supports. Residual risk (post-bump regen byte-cleanliness) is correctly flagged as the orchestrator's verify loop. |

## Adjudicated cross-report conflict: F4 (report 1) vs P3 (report 3)

These two findings are in direct tension and the synthesizer must NOT carry
both as written. Report 1's F4 claims a *genuine, active* cross-deploy state
leak ("the first deploy's chain is silently abandoned and the second hijacks
it"). Report 3's P3 proves — and I independently confirmed — that this is
**impossible under the current code**: `Runner::drive` (runner.rs:156-185)
runs the entire pipeline to a terminal `Reply` on `&mut self` inside ONE
`execute`/`handle_stream` call, the accept loop is strictly serial
(triad-runtime daemon.rs:368-380), and there is no threading anywhere (grep).
A second Deploy frame is not `accept()`ed until the first deploy fully
finishes. `active_deploy` is therefore always `None` between requests and
`record_deploy_submitted:764` never overwrites a live cursor.

**Adjudication: P3 is correct; F4 is REFUTED as a live bug and survives only
as the "add a defensive guard + document the invariant" recommendation that
P3 already makes.** The orchestrator should implement the guard/doc once
(under P3), not treat F4 as a separate active-corruption fix.

## Surviving CONFIRMED flaws, ranked for the orchestrator

### Blocks correctness (the deploy does the wrong thing or nothing)

1. **F6 / 5.1 — activate is a no-op.** `activate_system:1280` ships
   `--set "$CLOSURE"` with `$CLOSURE` undefined (no `.env`, closure_path
   dropped from `ActivateGenerationCommand`), and omits
   `switch-to-configuration`. Even with correct addressing the system profile
   is set to empty and never switched. Fix: thread `closure_path` into
   `ActivateGenerationCommand`; set via `Command::env("CLOSURE", path)` (keeps
   the remote string argument-free, dodges injection) AND emit
   `switch-to-configuration <action>`. NEVER a bare
   `format!("--set {closure_path}")` — that is the injection seam 5.1 names
   (legacy guards it with `ShellArgument`).
2. **F1 / F2 — build drops substituters + overrides and diverges from legacy.**
   Build the attribute `<flake>#<attr>` directly (legacy `build.rs:300-302`
   parity) so substituters (`build.rs:333`) and `--override-input` ride along,
   rather than `nix build <eval'd-drv>`. Wire `NixBuildCommand.substituters`
   (nexus.rs:94, currently ignored) into the invocation.
3. **P1b — Boot/Test/BootOnce record slot `Current`.** Thread the computed
   `GenerationSlot` (`activation_slot:1168-1175`) into `ActivationCommit`
   (drop the hardcoded `Current` at `activation_commit:288`) so the durable
   live-set distinguishes Boot from Switch. Pairs with widening the commit
   record (P6b) so `record_generation_activated` stops back-channeling
   `active_deploy`.
4. **P6 — three wrong rejection reasons.** Give `deploy_reason:608`,
   `pin_reason:577`, `retire_reason:597` honest internal-error fallthroughs
   instead of `DeploymentInFlight` / `PinSlotExhausted` / `GenerationUnknown`.
   The deploy one is the worst (a lock error reported as "already deploying").

### Blocks robustness / safety (correct on the happy path, unsafe under load or attack)

5. **W1 — 4 GiB OOM per frame.** Construct the daemon codec with a real bound
   (`LengthPrefixedCodec::new(MaximumFrameLength::new(...))`, KiB-MiB scale)
   and stop pre-zeroing the declared length (`read_body:110`) — read in
   bounded chunks. Single highest-value wire fix; trivially weaponizable.
6. **W2 — connect-and-never-send wedges the whole daemon.** `set_read_timeout`
   on every accepted stream; drop on timeout. Independent of, and additive to,
   the serial-loop issue.
7. **W3 — owner authority is unvalidated socket mode only.** Validate
   `owner_socket_mode` on decode (fail closed on any `o+w`/`o+r`); add
   `SO_PEERCRED` peer-uid authorization on the owner socket as defense in
   depth so the boundary doesn't rest on one chmod taken from config.
8. **W6 — owner deploy dropped with EOF, no typed reply, on the fallback
   arm.** Make `execute`'s `_` arm tier-aware (meta `DeployRejected` on the
   owner path) and write a typed rejection frame before dropping on ANY
   handler `Err`.
9. **P5 — `fail_pipeline` leaks `active_operation`.** One line:
   `self.active_operation = None;` at `fail_pipeline:715`. Pair with P4
   (treat the `reject_active_or_meta:549` `None` case as an internal-invariant
   violation, not a defaulted `Deploy`).
10. **W4 / W5 / P3 — TOCTOU socket window; fully-serial blocking daemon.**
    W4: bind-temp-then-chmod-then-rename or a 0700 parent dir. W5/P3: the
    blocking build stalls every socket — needs a worker model / off-thread
    effect plane AND a keyed in-flight map to replace the single-slot fields
    before any concurrency. Carry as the open design question below. Document
    the single-writer run-to-completion invariant on `SchemaRuntime` +
    `handle_stream` now (cheap; prevents the F4/P5 latent bugs from going
    live the day someone adds a thread).
11. **W7 / 5.5 — no structural contract discriminator.** Encode an
    ordinary-vs-meta tier bit in the short header so `route_from_short_header`
    rejects the wrong contract independent of rkyv layout; fix the false
    "headers are distinct" comment in `client.rs:82`.

### Cleanup (legibility / typed-domain / dead code; no behavior change)

12. **F8** revision = `first_line` of JSON (inert; parse `.revision` or drop).
13. **5.2 / 5.3** return `meta::FlakeAttribute` (promote to a real newtype with
    `#`-join/`.drvPath` methods) instead of bare `String`.
14. **P1** rename `DeployStage` variants to the NEXT action and/or lift the
    ordered pipeline into one driver (report-26's recommendation) to kill the
    dual-driver split.
15. **5.4** add an exhaustiveness guard so a fifth meta verb breaks the build
    instead of silently desyncing the `*_reason` maps.
16. **5.6a/b** add `Error::InlineNotaUnsupported`; carry `EffectStage` typed
    (or delete the dead `Error::EffectFailed`).
17. **5.7** make `bin/lojix-daemon.rs` `run()` an associated function.
18. **W8** bounded/structured error logging.

### Known-deferred — verified deferred, NOT to be re-fixed as flaws

- **F3 / F5 / F9** (production override-inputs absent; copy/activate bare-node
  addressing; `source`/`deployment_kind` inert on the override path) are the
  M2/M3/A3 surface the brief named. Confirmed present; the only actionable
  residue is a **reject-guard** so a production `System` deploy
  (`build_attribute: None`) or an activating action cannot be SUBMITTED and
  then falsely report `Deployed` until M3/A3 land. That guard is the one
  net-new ask spanning F3/F5/F9 — treat it as a single small fix, not three.
- **F7** (reply carries no store path) is the schema limit (`AcceptedDeploy`
  has no path field, meta lib.schema:114). Threading the realised path into
  the reply is genuinely useful — it would let the smokes assert correctness,
  not just reachability — but it is a contract extension, M-scope, not an M1
  regression.
- The **engine bump** (report 4) — HOLD confirmed; no forcing function.

## Newly-found issues from cross-reading (finders missed or under-stated)

1. **The activate path writes a REAL closure_path to the durable live-set
   while the actual remote activation sets NOTHING** — a durability/reality
   divergence neither F6 nor 5.1 stated crisply. `set_closure_path:689-693`
   populates `pipeline.closure_path` after build, so `activation_commit:289`
   (`self.closure_path.clone().unwrap_or_default()`) records the real
   `/nix/store/...` path into `live_set` + `gc_roots` (record_generation_-
   activated:826,833). But `activate_system` ships literal `$CLOSURE` and sets
   nothing on the node. Net: the daemon's durable state will claim a
   generation is live-and-activated at a path that was never actually
   switched to on the target. That is worse than a clean failure — the
   database lies. Strengthens the F6/5.1 fix priority: the activate effect and
   the live-set write must agree, and the live-set write should not commit
   until the remote activation genuinely succeeded with that path.

2. **`unwrap_or_default()` on `closure_path` at `activation_commit:289` will
   silently record an EMPTY closure_path if the activate path is ever reached
   without a prior build** — e.g. a future early-termination edit, or any
   ordering regression. The `Option<ClosurePath>` is collapsed with a
   default-empty instead of being treated as an invariant violation. Same
   defensive-typing gap as P4/P6b. Low today (build always precedes activate),
   but it is a third instance of the "collapse an unexpected `None`/absence to
   a plausible-looking default" anti-pattern that P4 and P6b also flag — worth
   calling out as a *pattern* for the orchestrator: the engine repeatedly
   papers over `None` with `unwrap_or(...)` where an internal-invariant
   assertion belongs (reject_active_or_meta:549, record_generation_activated:
   809/813/817, activation_commit:289, record_phase:703's
   `position.unwrap_or(0)`).

3. **`record_phase:703` stamps the wire event's `event_log_position` from
   `position.unwrap_or(0)` on a poisoned lock** — a fourth instance of the
   same pattern, and one P2 did not connect: if the store lock is poisoned at
   `record_phase:702`, the outgoing `DeploymentPhaseEvent` gets position `0`
   (colliding with the genuine first event) AND then the subsequent
   `record_phase_transition` write will itself reject on the poisoned lock —
   so the wire event and the (rejected) durable write disagree. Minor (lock
   poison is already a degraded path) but it compounds P2's non-atomic
   double-read: the two positions can diverge not just under concurrency but
   under lock poison on the happy single-thread path too.

## What I could NOT confirm (stated, not assumed away)

- Whether `nix build <bare-.drv>` is robust across Nix versions (F1's
  sub-claim) — same limit report 1 stated; not statically decidable from the
  files, and read-only forbids a `nix` run. The legacy-parity argument (build
  the attribute, not the drv) sidesteps it regardless.
- Whether any specific meta-contract payload's rkyv bytes validate as a
  same-ordinal ordinary variant (W7) — I confirmed the headers collide and
  that only rkyv layout divergence rejects the replay; I did not enumerate
  every payload pair. The design has no structural discriminator, so the
  property is incidental, which is the finding.
- The post-bump regen byte-cleanliness (report 4) — read-only; the
  orchestrator's verify loop owns it.

## Open design question for the synthesizer / psyche

The blocking-build-stalls-all-requests behavior (W5 / P3) is the largest
single design gap and is partly architectural, not a bug-fix: is
single-request-at-a-time acceptable for the production deployer (a deploy is
rare, owner-only, and arguably SHOULD serialize), with the only required fix
being that the *ordinary* read/watch socket stays responsive during a deploy?
Or does M2/M3 need a worker model / async effect plane? The answer determines
whether the single-slot `active_deploy`/`active_operation` fields can stay
(with a documented invariant + the P5/P4/F4 guards) or must become a keyed
in-flight map. The wire fixes W1/W2/W3/W6 are unconditionally needed
regardless of that answer.
