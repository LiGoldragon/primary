# 7 — Synthesis: lojix triad M1 adversarial audit (the orchestrator's fix-list)

cloud-designer lane, 2026-06-05. This is the session synthesis over finders
1-5 and the adversarial verification (6). It carries ONLY flaws the verifier
CONFIRMED against the actual pushed `triad-port` bytes; refuted and
downgraded claims are noted where they were dropped so they are not
re-litigated. I spot-re-read the five load-bearing citations
(`activate_system:1280`, `fail_pipeline:714-715`, `read_body:110`,
`MaximumFrameLength::maximum_for_u32_prefix:36`, `run:1292-1308` no-`.env`)
and they all check out exactly as the verifier reported.

## Verdict — is the M1 work sound?

Partly. The **state-machine scaffolding M1 added is sound**: the
`DeployAction` enum and its `produces_closure()`/`activates()`/
`target_attribute()` mapping are faithful to the legacy deployer with no
mis-mapped variant; the `Eval`/`Build` early-termination is correctly placed;
the finish-path state clearing is symmetric. The re-entrancy and
budget-exhaustion attack vectors the brief weighted hardest both come back
**NEGATIVE** — the single-thread run-to-completion invariant makes the
single-slot `active_deploy`/`active_operation` fields safe TODAY (finder 1's
F4 "active cross-deploy corruption" was REFUTED by the verifier against
finder 3's P3; carry only the defensive-guard half).

But the M1 work is **NOT correct end-to-end** and **NOT safe to expose on a
socket**, for two independent reasons:

1. **The activate path is actively broken, not merely deferred.** `--set
   "$CLOSURE"` is shipped with `$CLOSURE` never defined and
   `switch-to-configuration` dropped (F6/5.1, confirmed at
   `schema_runtime.rs:1280` + no `.env` at `run:1292-1308`). Worse, the
   durable live-set is written with the REAL closure path while the remote
   activation sets nothing (verifier's newly-found issue #1) — the database
   lies about what is deployed. This is in M1 scope because M1 routes the
   activating actions through this body; it is not the deferred A3 addressing
   gap.

2. **The wire layer is trivially weaponizable.** A 4-byte `FF FF FF FF`
   length prefix triggers a 4 GiB pre-zeroed allocation (W1, confirmed at
   `frame.rs:110` + default cap `u32::MAX` at `frame.rs:36`); a
   connect-and-never-send wedges the entire serial daemon forever (W2, no
   `set_read_timeout` anywhere). The owner/ordinary authority boundary rests
   entirely on one chmod taken verbatim from unvalidated config (W3).

The build/eval happy path also silently drops substituters and overrides
(F1/F2) and diverges from the legacy deployer's `<flake>#<attr>` build. So
even the green-passing M1 smokes prove **reachability, not correctness** —
they assert only `meta::Output::Deployed` and the reply carries no store
path (F7), so a silently-empty eval or a no-op activate still passes green.

Recommendation: **do not build M2/M3 on this until the blocks-correctness and
the three top robustness items are fixed.** None is large; the activate fix
and the build-the-attribute fix are the two that change deploy behavior.

## Confirmed flaws, prioritized

### Blocks correctness — the deploy does the wrong thing or nothing

**C1. Activate is a no-op AND the database lies** (F6 / 5.1 + verifier #1).
`schema_runtime.rs:1280` ships `nix-env -p /nix/var/nix/profiles/system --set
"$CLOSURE"`; `$CLOSURE` is never defined (`run:1292-1308` sets no `.env`,
`ActivateGenerationCommand` at `nexus.rs:108-113` carries no closure path,
`activate_generation_command:274-281` drops the stored `closure_path`), and
the legacy `switch-to-configuration <action>` step (`lojix-cli/activate.rs:
59-63`) is omitted. The system profile is set to empty and never switched.
Compounding: `activation_commit:289` records the REAL `/nix/store/...` path
into `live_set`+`gc_roots` (`record_generation_activated:826,833`) — so the
durable state claims a generation is live at a path that was never switched
to on the target. Worse than a clean failure.
*Fix:* thread `closure_path` into `ActivateGenerationCommand` and set it via
`Command::env("CLOSURE", path)` (keeps the remote string argument-free,
dodges the injection seam 5.1 names — NEVER `format!("--set {closure_path}")`,
which legacy guards with `ShellArgument`), AND emit `switch-to-configuration
<action>`. The live-set write should not commit until the remote activation
genuinely succeeds with that path.
*Test:* YES — a smoke that asserts the activate command both interpolates a
real `/nix/store/...` and runs `switch-to-configuration`, and that no
live-set commit lands on activate failure.

**C2. Build drops substituters + overrides and diverges from legacy** (F1 /
F2). `run_nix_eval:1113-1117` captures the eval'd `.drvPath` as `closure_path`
and `run_nix_build:1235-1245` runs `nix build <drv>`; legacy
`build.rs:300-302` builds the attribute `<flake>#<attr>` directly with
`--refresh --print-out-paths` so substituters (`build.rs:333`) and
`--override-input` ride along. `NixBuildCommand.substituters` (`nexus.rs:94`)
is never read in `run_nix_build:1122-1140`. Net: a build that can't pull from
the configured cache and silently ignores the override the schema carries.
*Fix:* build `<flake>#<attr>` directly for legacy parity; wire
`NixBuildCommand.substituters` into `--option extra-substituters` /
`--option extra-trusted-public-keys` mirroring `build.rs:330-339`.
*Test:* YES — assert the build invocation contains the attribute reference
and the substituter options. (Note the verifier could NOT statically confirm
`nix build <bare-.drv>` is version-robust; the legacy-parity fix sidesteps
the question.)

**C3. Boot/Test/BootOnce record slot `Current` in the durable live-set**
(P1b). `activation_commit:288` hardcodes `GenerationSlot::Current`; the
correct slot IS computed (`activation_slot:1168-1175`, used only in the
transient effect result) but never threaded into the commit. A Boot deploy is
durably indistinguishable from a Switch.
*Fix:* thread the computed `GenerationSlot` into `ActivationCommit` (widen the
record), drop the hardcoded `Current`. Pairs with P6b (widen the commit so
`record_generation_activated` stops back-channeling `active_deploy` for
`deployment_kind`/`activation_kind`).
*Test:* YES — assert a Boot deploy records the Boot slot, not `Current`.

**C4. Three wrong rejection reasons** (P6). `deploy_reason:608`
`_ => DeploymentInFlight` swallows the poisoned-lock `PlanNotApproved`
(emitted at 775) — a lock error is reported to the owner as "already
deploying". `pin_reason:577` `_ => PinSlotExhausted` (a reason no sema path
produces); `retire_reason:597` `_ => GenerationUnknown` even for existing
generations.
*Fix:* honest internal-error fallthroughs in all three; the deploy one is the
worst and the only owner-facing one.
*Test:* optional — a unit assertion that the poisoned-lock path maps to an
internal-error reason, not `DeploymentInFlight`.

### Robustness / hardening — correct on the happy path, unsafe under load or attack

**R1. 4 GiB OOM/DoS per frame** (W1) — highest-value wire fix, trivially
weaponizable. The daemon constructs `LengthPrefixedCodec::default()`
(`lojix daemon.rs:94`), whose cap is `maximum_for_u32_prefix() = u32::MAX`
(`frame.rs:36-37`); `read_body:110` does `vec![0_u8; length]` from the
untrusted prefix before `read_exact:111`.
*Fix:* construct the codec with `MaximumFrameLength::new(...)` at KiB-MiB
scale and stop pre-zeroing the declared length — read in bounded chunks.
*Test:* YES — a malformed-frame test sending an oversized length prefix and
asserting a clean bounded rejection, not an allocation.

**R2. Connect-and-never-send wedges the whole daemon** (W2). No
`set_read_timeout` on any accepted stream (grep-confirmed); the accept loop is
serial + synchronous (`triad-runtime daemon.rs:368-380`), so `read_exact`
(`frame.rs:107`) blocks forever and one unauthenticated ordinary client
permanently denies the owner deploy surface.
*Fix:* `set_read_timeout` on every accepted stream; drop on timeout.
*Test:* YES — a connect-and-hang test asserting the daemon stays responsive
on the other socket.

**R3. Owner authority is unvalidated socket-mode only** (W3). No `SO_PEERCRED`
/ token anywhere (grep); `owner_socket_mode: u32` (`lib.rs:96`) flows verbatim
to `from_mode(...)` (`triad-runtime daemon.rs:580`) with no floor — a config
of 0o666/0o777 silently makes the owner socket world-writable.
*Fix:* validate `owner_socket_mode` on decode (fail closed on any `o+w`/`o+r`);
add `SO_PEERCRED` peer-uid authorization on the owner socket as defense in
depth.
*Test:* YES — an authority-boundary test: a non-owner uid is rejected on the
owner socket; a permissive mode in config is rejected at decode.

**R4. Owner deploy dropped with EOF, no typed reply** (W6). `execute:122-143`
`_` arm hardcodes `OrdinaryOutput(QueryRejected)`; on the owner path
`meta_reply:154-161` returns `Err(UnexpectedFrame)` and the connection is
dropped before any `write_body` — the client gets EOF mid-exchange, not a
typed rejection. The comment at `daemon.rs:128-129` asserts the invariant but
nothing enforces it.
*Fix:* make the `_` arm tier-aware (meta `DeployRejected` on the owner path)
and always write a typed rejection frame before dropping on ANY handler `Err`.
*Test:* YES — assert an owner-socket frame that hits the fallback gets a typed
meta `DeployRejected`, not EOF.

**R5. `fail_pipeline` leaks `active_operation`** (P5) — one line. `fail_pipeline:
715` clears `active_deploy` only; `finish_deploy_pipeline:530` clears both. A
mid-pipeline effect failure leaks `Some(Deploy)`. Masked today by every meta
op re-setting on entry, but a real asymmetry.
*Fix:* add `self.active_operation = None;` at `fail_pipeline:715`. Pair with
P4: treat the `reject_active_or_meta:549` `None` case as an internal-invariant
violation, not a defaulted `Deploy`.
*Test:* optional — a unit test that a failed pipeline leaves both in-flight
slots `None`.

**R6. Socket-mode TOCTOU + fully-serial blocking daemon** (W4 / W5 / P3).
`bind_listener:551-556` binds at umask default then chmods on the next
statement; the parent `/run/lojix` is created at umask default. Separately,
the accept loop is serial and the `nix` effect blocks on `Command::output()`
(`schema_runtime.rs:1293-1296`) on the accept thread, so the ordinary socket
is unpolled for the minutes a deploy runs.
*Fix:* W4 — bind-temp-then-chmod-then-rename or a 0700 parent dir. W5/P3 — see
the open design question; minimally, document the single-writer
run-to-completion invariant on `SchemaRuntime` + `handle_stream` NOW (cheap;
prevents the F4/P4/P5 latent bugs going live the day someone adds a thread).
*Test:* the documented-invariant part needs no test; the worker model is
design-gated.

**R7. No structural contract discriminator** (W7 / 5.5) — latent. meta
`INPUT_DEPLOY = 0x0` == ordinary `INPUT_QUERY = 0x0` and all four ordinals
collide exactly (`meta lib.rs:633-636` vs `signal lib.rs:930-933`); a replayed
cross-contract frame is rejected ONLY if rkyv layout happens to diverge —
incidental, not structural. The client's `decode_signal_file:79-90` carries
the same false "headers are distinct" comment.
*Fix:* encode an ordinary-vs-meta tier bit in the short header so routing
rejects the wrong contract independent of rkyv layout; delete the false
client comment. (The verifier could NOT enumerate every payload pair to prove
a same-ordinal collision exists today — the finding is the absence of a
structural discriminator, not a demonstrated exploit.)
*Test:* YES — a cross-contract replay test: a meta frame on the ordinary
socket is structurally rejected.

### Cleanup — legibility / typed-domain / dead code; no behavior change

- **CL1. `first_line` of `nix flake metadata --json` grabs `{` as revision**
  (F8) — inert (the `revision` field is never consumed). Parse `.revision`
  from the JSON or drop the field. `resolve_flake_auth:1102-1106` +
  `first_line:1310-1312`.
- **CL2. Flake attribute is `String` end-to-end** (5.2/5.3). `FlakeAttribute =
  String` alias (`meta lib.rs:69`); both `target_attribute()` (`:134-143`,
  `:241-251`) return bare `String`. Promote `FlakeAttribute` to a real newtype
  with the `#`-join / `.drvPath` logic as methods (currently 3 hand-`format!`
  sites: 140, 1112, 1230).
- **CL3. `DeployStage` name-vs-action mismatch** (P1) — legibility only, NOT a
  correctness break (verifier traced every transition; no wrong effect fires).
  Rename variants to the NEXT action and/or lift the ordered pipeline into one
  driver to kill the dual-driver split (`advance_after_phase` vs
  `decide_effect_completion`).
- **CL4. `MetaOperation` hand-mirrors the meta `Input` discriminant** (5.4).
  Add an exhaustiveness guard so a fifth meta verb breaks the build instead of
  silently desyncing the `*_reason` maps (572-610).
- **CL5. `Error` channel misuse** (5.6a/b). `client.rs:73-74` returns
  `Error::FlagArgument(...)` for a missing-feature message — add
  `Error::InlineNotaUnsupported`. `Error::EffectFailed{stage:String}` is dead
  (zero construction sites; the live `EffectFailed` is the DIFFERENT
  `nexus::EffectResult` type) and re-stringifies typed `EffectStage` — delete
  it or carry `EffectStage` typed.
- **CL6. `bin/lojix-daemon.rs:16 fn run()`** is a module-scope free function
  (5.7) — make it an associated function. Trivial; out of strict scope.
- **CL7. Unbounded `eprintln!` error logging** (W8) at `triad-runtime
  daemon.rs:151-160` — bounded/structured logging. Safe (no panic), pure
  observability.
- **CL8. The `unwrap_or(...)`-papers-over-`None` pattern** (verifier #2/#3 +
  P4 + P6b). Five sites collapse an unexpected absence to a plausible default
  where an internal-invariant assertion belongs:
  `reject_active_or_meta:549`, `activation_commit:289`
  (`closure_path.unwrap_or_default()` — would silently record an EMPTY path),
  `record_generation_activated:809/813/817`, `record_phase:703`
  (`position.unwrap_or(0)` on a poisoned lock). Treat as a pattern to sweep,
  not five isolated fixes.

## Engine-port decision

**HOLD the bump (schema-rust-next / triad-runtime) now.** Confirmed by the
verifier with a stated read-only limit. Rationale:

- **No forcing function.** The generated `NexusEngine`/`SemaEngine` trait
  method set is signature-identical between the pinned engine and latest
  (`tokenize engine trait emission` rewrote the EMITTER, not the trait
  surface; the runtime mail-token types already exist at the pin). The hand
  impl (`schema_runtime.rs:1328-1400`) satisfies exactly the six unchanged
  required methods — nothing in the hand code needs editing to bump.
- **The only new capability (streaming) is unreachable without separate
  feature work.** lojix's generated code has ZERO `StreamingFrame`/
  `Subscription` surface (it declares no `Schema::streams()`), and
  signal-lojix authored Watch/Unwatch as a deliberate token-handshake
  (`schema/lib.schema:11-19`). The triad-runtime `SubscriptionRegistry`
  additions are a precondition for push, not the feature — real push also
  needs the daemon's `handle_stream` to retain the client stream past the
  reply (a contract gap upstream of lojix at `daemon.rs:98-120`).
- **The other additions fix no current defect:** `should_continue()` is
  defaulted; socket-cleanup-on-drop is moot (the pinned runtime already
  unlinks stale sockets at bind, and the daemon test SIGKILLs so Drop never
  runs).

**Plan — bump only when the streaming/Watch* milestone is scheduled:**
1. `cargo update` the two deps.
2. Regen + recommit `src/schema/{nexus,sema}.rs` — the emitter's rustfmt
   reflow makes the checked-in copies stale vs `build.rs:36`'s `write_or_check`
   freshness gate. (This is the ONE real bump cost; cosmetic.)
3. Declare `Schema::streams()` in the lojix schema.
4. Wire the `SubscriptionRegistry`/`SubscriptionEventPublisher` AND solve the
   retain-stream `handle_stream` gap.
5. Replace the Watch* token-handshake stub with event-frame emission.

**Residual risk (the orchestrator's verify loop owns it):** read-only forbade
running the regen, so post-bump byte-cleanliness and transitive-dep compile
are not certified here.

## Test-extension plan (the orchestrator writes these)

The M1 smokes are `#[ignore]` and assert only `Deployed`/reachability. Add:

1. **Activate correctness** (C1) — assert the activate command interpolates a
   real `/nix/store/...` and runs `switch-to-configuration`; assert NO
   live-set commit on activate failure.
2. **Build parity** (C2) — assert the build invocation references the
   attribute `<flake>#<attr>` and carries the substituter options.
3. **Boot-slot durability** (C3) — a Boot deploy records the Boot slot, not
   `Current`, in the live-set.
4. **Malformed-frame / oversized-length** (R1) — an oversized length prefix is
   bounded-rejected, no large allocation.
5. **Connect-and-never-send re-entrancy** (R2) — a hung client does not wedge
   the other socket; read timeout fires.
6. **Authority boundary** (R3) — a non-owner uid is rejected on the owner
   socket; a permissive `owner_socket_mode` is rejected at config decode.
7. **Fallback-arm typed reply** (R4) — an owner frame hitting the `_` arm gets
   a typed meta `DeployRejected`, not EOF.
8. **Cross-contract replay** (R7) — a meta frame on the ordinary socket is
   structurally rejected.
9. **In-flight slot symmetry** (R5) — a failed pipeline leaves BOTH
   `active_deploy` and `active_operation` `None`.
10. **Home-deploy** — the brief named it; no finder surfaced a Home-specific
    flaw, but there is no Home smoke. Add one round-trip so the Home path is
    exercised, not just reasoned about.
11. **Reject-guard** (the F3/F5/F9 deferred residue) — a production `System`
    deploy (`build_attribute: None`) or an activating action is REJECTED at
    submit, not accepted and falsely reported `Deployed`, until M3/A3 land.
    One guard spans all three; assert it fires.
12. **Store-path-carrying reply** (F7) — once `AcceptedDeploy` is extended with
    the realised path (a contract change, M-scope), the smokes should assert
    `/nix/store/...` shape, not just `Deployed`.

## What is genuinely fine — don't touch

- **`DeployAction` enum + `produces_closure()`/`activates()`/
  `target_attribute()` mapping** (schema_runtime.rs:105-143) — faithful to
  legacy, no mis-mapped variant; `Test` correctly classifies as
  activates+produces_closure. The danger was only that it lands in the broken
  activate body (C1), not the mapping.
- **`Eval`/`Build` early-termination placement** — correct.
- **`finish_deploy_pipeline:529-542` finish-path state clearing** — symmetric
  and correct; the in-flight leak is on the FAILURE path (R5), not finish.
- **Re-entrancy / concurrent-deploy safety TODAY** — the single-thread
  run-to-completion invariant makes the single-slot fields safe; finder 1's F4
  "active cross-deploy corruption" was REFUTED. Do NOT add a keyed in-flight
  map as a bug-fix; it is gated on the concurrency design decision below. Just
  document the invariant and add the defensive guard (R5).
- **Continuation budget** — P7's budget-exhausted wrong-reply is UNREACHABLE
  (no path emits `Continue`); not a fix target until concurrency lands.
- **Method-placement discipline** — the four in-scope files have NO
  module-scope free functions (except the trivial CL6 in `bin/`), NO ZST
  namespace holders, a typed `thiserror` `Error` enum with no `anyhow`, full
  English naming, and proper sum types (no bool flag-soup).
- **Malformed/truncated/partial frames** — fail cleanly (no panic); the only
  frame-decode issue is the oversized-length pre-allocation (R1) and the
  never-send hang (R2), both listed.
- **The known-deferred surface** (production `--override-input`; copy/activate
  bare-node addressing; no projection/materialization) — verified genuinely
  deferred (M2/M3/A3), NOT re-reported as flaws. The one net-new ask across
  them is the single reject-guard (test 11) so a deferred-incomplete deploy
  can't falsely report `Deployed`.

## Open design question for the psyche

The blocking-build-stalls-all-requests behavior (R6 / W5 / P3) is the largest
single design gap and is architectural, not a bug-fix. **Is single-request-at-
a-time acceptable for the production deployer** — a deploy is rare, owner-only,
and arguably SHOULD serialize, with the only required fix being that the
*ordinary* read/watch socket stays responsive during a deploy? **Or does
M2/M3 need a worker model / async effect plane?** The answer determines
whether the single-slot `active_deploy`/`active_operation` fields can stay
(with the documented invariant + the R5/P4 guards) or must become a keyed
in-flight map. The wire fixes R1/R2/R3/R4 are unconditionally needed
regardless of that answer.
