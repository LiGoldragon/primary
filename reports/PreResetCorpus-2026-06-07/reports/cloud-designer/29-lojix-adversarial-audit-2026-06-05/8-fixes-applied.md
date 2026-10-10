# 8 — Fixes applied (orchestrator follow-through on the audit)

cloud-designer lane, 2026-06-05. Acting on the confirmed-flaw list in `7`.
Built + tested green in the canonical `/git` layout; pushed to `main`.

## Confirmed flaws fixed

### Blocks-correctness
- **C1 (activate no-op + DB lies) → M1 reject-guard.** Rather than half-build
  the activate path (M2/M3 work), the daemon now REJECTS at submit any deploy
  shape it does not actually implement: production System deploys (no
  `build_attribute` — need horizon materialization), activating actions
  (Boot/Switch/Test/BootOnce — need real copy/activate), and all Home deploys.
  New meta reason `UnsupportedDeployAction`; the guard
  (`unsupported_deploy_reason`) replies `DeployRejected` before any sema write
  or effect, so the live-set can never record a generation that was not
  deployed. The supported M1 shape (System + `build_attribute` + Eval/Build)
  is unaffected — the smokes still reach `Deployed`. Tests:
  `engine_routing.rs` `activating_deploy_is_rejected…`,
  `production_deploy_without_build_attribute_is_rejected`,
  `home_deploy_is_rejected…` (all non-ignored, no nix).
- **C2 (build dropped substituters) → wired.** `run_nix_build` now threads
  `NixBuildCommand.substituters` into `--option extra-substituters /
  extra-trusted-public-keys` (new `NixCommand::substituter_options`). The
  attr-vs-drv parity nuance is left as-is (building the eval'd drv is valid
  nix); the silent substituter drop — the real correctness gap — is closed.
- **C4 (wrong rejection reasons) → honest fallthroughs.** Added meta
  `InternalError`; `deploy_reason`/`pin_reason`/`retire_reason` `_` arms now map
  an unmapped sema reason (e.g. a poisoned lock) to `InternalError`, not a
  misleading domain reason like `DeploymentInFlight`/`PinSlotExhausted`.

### Robustness / hardening
- **R1 (4 GiB OOM) → bounded frame cap.** The daemon + codec now use
  `LengthPrefixedCodec::new(MaximumFrameLength::new(8 MiB))`; `read_body`
  validates length before allocating, so a hostile `0xFFFFFFFF` prefix is
  rejected with no allocation. Test `oversized_frame_is_bounded_and_daemon_survives`
  (sends the hostile frame, asserts a subsequent valid request still
  succeeds).
- **R2 (connect-and-never-send wedge) → read timeout.** Every accepted stream
  gets a 10 s `set_read_timeout` before the request read, bounding the serial
  daemon's wedge from forever to ≤ 10 s.
- **R3 (owner authority = chmod only) → mode floor.** `validate_owner_socket_mode`
  refuses any owner mode granting "other" access (`mode & 0o007`), failing
  closed at startup. New `Error::InsecureOwnerSocketMode`. Test
  `permissive_owner_socket_mode_is_refused`. (Full `SO_PEERCRED` peer-uid auth
  is a triad-runtime follow-up — defense in depth, not done here.)
- **R4 (owner deploy dropped as EOF) → tier-correct reply.** `execute` is now
  tier-aware; the should-never-happen non-reply action returns a meta
  `DeployRejected(InternalError)` on the owner path (and an ordinary
  `QueryRejected` on the ordinary path), so the client always decodes a typed
  reply rather than an EOF.
- **R5 (`fail_pipeline` leaks `active_operation`) → one line.** Now clears both
  in-flight slots, symmetric with the finish path.
- **R6 (serial blocking daemon) → invariant documented.** The single-writer
  run-to-completion invariant is now a doc comment on `LojixRuntime` (the cheap
  half). The worker-model decision is the open question below.

### Cleanup
- **CL5** — added `Error::InlineNotaUnsupported` (client.rs no longer misuses
  `FlagArgument`); deleted the dead `Error::EffectFailed` (zero construction
  sites, confirmed by the build).
- **R7 comment** — the false "short headers are distinct" comment in
  `client.rs` now states the truth (the contract ordinals collide; a structural
  tier discriminator is the proper upstream fix).

## Not fixed — deferred with reason
- **C3 (Boot records `Current` slot)** — moot under the reject-guard (activating
  deploys are now rejected, so `activation_commit` is unreachable in M1); pairs
  with the M2 activate work.
- **R7 structural discriminator** — the fix is a tier bit in the generated
  short header (signal-frame / schema-rust-next), upstream of lojix. Flagged;
  comment corrected. No test added (asserting the current incidental rkyv-layout
  rejection would test unfixed behavior).
- **CL1/CL2/CL3/CL4/CL6/CL7/CL8** — legibility/typed-domain cleanups, no
  behavior change. Notably CL2 (promote `FlakeAttribute` to a newtype) is a
  schema change deferred; CL6 (`bin/lojix-daemon.rs` `run()` free fn) is
  pre-existing bin boilerplate the audit marked out-of-strict-scope.

## Engine-port decision — HELD
Per `7`: no forcing function (trait surface signature-identical; streaming
needs separate feature work). Did NOT bump schema-rust-next / triad-runtime.

## Test status
Regular suite 8 passed (5 routing + 3 reject-guard, all no-nix). Ignored:
3 real-nix smokes + R3 mode-reject + R1 oversized-frame — all green run
explicitly.

## Open design question for the psyche (carried from `7`)
**Is single-request-at-a-time acceptable for the production deployer?** A deploy
is rare and owner-only and arguably should serialize; the only hard requirement
is that the ordinary read/watch socket stay responsive during a long build. If
yes, the single-slot in-flight fields stay (with the now-documented invariant +
the R5 guard). If M2/M3 need concurrent deploys / an async effect plane, those
fields must become a keyed in-flight map and the accept loop needs a worker
model. The wire fixes (R1–R4) are in regardless.
