# Dimension 4 — Engine-Port Assessment (the refresh)

Adversarial read of whether the new-stack lojix triad should bump its engine
crates now. Posture: assume the bump breaks the hand impl until the generated
surface proves otherwise. It does not break it — the recommendation is a
qualified HOLD, with the streaming follow-on as the only bump-worthy lever and
it is not yet wired into the lojix schemas.

## Verified pins (the actual lock, not the Cargo.toml branch spec)

`Cargo.toml` pins every engine crate to `branch = "main"`
(`/git/github.com/LiGoldragon/lojix/triad-port/Cargo.toml:33-39`), so the
*real* pin is the lock, and a `cargo update` would silently move it. The lock
confirms the brief:

- schema-rust-next 0.1.13 `c0a331a`
  (`/git/github.com/LiGoldragon/lojix/triad-port/Cargo.lock`, `schema-rust-next` entry).
- triad-runtime 0.2.1 `28d03c3` (same lock, `triad-runtime` entry).
- schema-next 0.1.4 `5311f9a` (same lock, `schema-next` entry).
- signal-frame `d61ebf25` is ALREADY transitively present in the lojix lock
  (the lock has 8 `signal-frame` references), pulled via the pinned
  triad-runtime/schema-next — so signal-frame is not a net-new crate on a bump.

Upstream HEADs (confirmed by `git log`/`git rev-parse` in each checkout):
schema-rust-next `7f59b39` (0.1.14), triad-runtime `973e1d3`, schema-next
`30a88be`.

## (a) Does bumping schema-rust-next change the generated engine-trait surface?

NO — not for lojix's schemas. `tokenize engine trait emission` (`e332b5e`)
rewrites the *emitter* (`src/lib.rs`, 638 lines churned) but the *generated
output* is signature-identical. Evidence:

- The generated `NexusEngine` trait method set is byte-identical between pinned
  `c0a331a` and latest `7f59b39` (compared via the checked-in fixture
  `tests/fixtures/runner_generated.rs` in schema-rust-next). Both versions emit
  exactly: defaulted `on_start`/`on_stop`/`trace_nexus_activation`/
  `trace_nexus_entered`/`trace_nexus_decided`/`continuation_limit`, plus
  required `apply_sema_write`, `observe_sema_read`, `run_effect`,
  `budget_exhausted_reply`, `decide`, and the defaulted `execute`. The diff on
  those lines is pure rustfmt reflow (`fn apply_sema_write(` wrapped onto
  multiple lines), not a signature change.
- The `-w` (whitespace-ignoring) diff of the generated fixture across the full
  `c0a331a..7f59b39` span is ~entirely derive-list wrapping
  (`#[derive(rkyv::Archive, ...)]` → multi-line) and `match` brace reflow. No
  added/removed/renamed method, no changed parameter or return type on any
  engine trait.
- `MessageProcessed` / `MessageProcessedHook` / `MessageIdentifier` (the
  "runtime mail tokens" of the `7783ae6` 0.1.14 bump) ALREADY exist at the
  pinned `c0a331a` (present in `c0a331a:tests/fixtures/runner_generated.rs` at
  lines 743/866/878). The 0.1.14 "mail tokens" work is an emitter tokenization
  of pre-existing surface, not a new required engine method.

The hand impl in `schema_runtime.rs` implements exactly the six required
methods plus overrides `decide` (`/git/github.com/LiGoldragon/lojix/triad-port/src/schema_runtime.rs:1328-1380`
for `NexusEngine`, `:1382-1400` for `SemaEngine`). Every method it satisfies
is unchanged in the latest emitter, so the hand impl would still compile
against regenerated `nexus.rs`/`sema.rs`. The generated trait defs lojix ships
today (`src/schema/nexus.rs:1233-1274`, `src/schema/sema.rs:1428-1445`) match
the latest fixture.

Adversarial caveat I could NOT fully close: the engine crates also moved their
own `Cargo.lock` (rkyv, prettyplease, etc.), and `cargo update` on lojix would
bump transitive deps beyond just the four engine crates. I read source, not a
build (read-only constraint), so I cannot certify the regen byte-for-byte —
`build.rs` runs `write_or_check` against the checked-in artifacts under
`LOJIX_UPDATE_SCHEMA_ARTIFACTS` (`build.rs:36`), so a bump that reflows the
generated code (the rustfmt-style changes above ARE in the emitter output)
would make the checked-in `src/schema/{nexus,sema}.rs` STALE and fail the
freshness check until regenerated. That is the one concrete bump cost: it is a
regen-and-recommit, not a code-change.

## (b) What do the triad-runtime streaming additions enable for Watch*?

The streaming runtime (`de33226` + `9708fc3`) adds, in
`/git/github.com/LiGoldragon/triad-runtime/src/streaming.rs`, exactly the
machinery lojix's stub handshake needs to become real push streaming:

- `SubscriptionRegistry<Token, Filter>` with `register`/`register_token`
  (pre-minted token, the `9708fc3` addition, `streaming.rs:122-125`)/
  `unregister`/`publish_matching` (`streaming.rs:142-153`).
- `SubscriptionTokenIssuer` (`streaming.rs:67-86`) — monotonic token minting.
- `SubscriptionEventPublisher::publish` (`streaming.rs:232-248`) producing a
  `signal_frame::StreamingFrame` carrying `StreamingFrameBody::SubscriptionEvent`.

These are newly re-exported from triad-runtime's `lib.rs` only at latest
(`pub mod streaming; pub use streaming::{...}` is added in the
`28d03c3..973e1d3` diff; absent at the pin). So lojix CANNOT use them without a
bump.

But the bump alone does NOT light up streaming for lojix, because of TWO
independent gates:

1. The schema-rust-next streaming EMITTER is gated on the schema declaring
   `Schema::streams()` AND the stream event type matching `Output.Event`
   (schema-rust-next `4ee2c89` INTENT addition: "A bare `Output.Event` name
   without a stream declaration is not enough"). lojix's generated
   `nexus.rs`/`sema.rs` reference only the non-streaming
   `encode_signal_frame`/`decode_signal_frame` request/reply surface
   (`src/schema/nexus.rs:929,938,976,985`; `src/schema/sema.rs:1056,1065,1106,1115`);
   grep finds ZERO `StreamingFrame`/`Subscription`/stream surface in lojix's
   generated code. The streaming emission shows up only in schema-rust-next's
   big-schema fixture (`triad-reactive-large.generated.rs`), never in the
   `runner_generated.rs` fixture that mirrors lojix's shape.

2. The signal-lojix contract DELIBERATELY does not declare a stream. Its schema
   header documents the day-one decision
   (`/git/github.com/LiGoldragon/signal-lojix/triad-port/schema/lib.schema:11-19`):
   schema-next/schema-rust-next at pin time "cannot yet emit a daemon-pushed
   event frame," so the Watch/Unwatch handshake is authored as an ordinary
   request → `SubscriptionToken` reply, with the two event payloads
   (`DeploymentPhaseEvent`, `CacheRetentionTransitionEvent`) kept as namespace
   records, and the event-frame-emission enhancement named as the follow-on.

So lojix's `open_subscription`
(`/git/github.com/LiGoldragon/lojix/triad-port/src/schema_runtime.rs:362-377`)
is correctly a token-handshake stub TODAY; the upstream streaming work is the
landing of the named follow-on, but consuming it requires (i) bump, (ii)
declare `streams()` in the two signal contracts so the emitter generates the
stream frame surface, (iii) hand-wire a `SubscriptionRegistry` into the daemon
loop and a publish path on phase-record. That is M-level feature work
(roughly the M4/streaming milestone), not a mechanical refresh. The bump is a
*precondition*, not the feature.

Adversarial note: `SubscriptionRegistry`/publisher live in triad-runtime, but
the daemon-side wiring (where the registry lives across requests, how a
phase-record write fans out to subscribers over the ordinary socket, how the
push frame is written back on a connection the runner doesn't own) is NOT
provided — `LojixRuntime` is request/reply per stream
(`/git/github.com/LiGoldragon/lojix/triad-port/src/daemon.rs:98-120`,
`handle_*` reads one body, writes one reply, returns). Real push needs the
daemon to retain the client `UnixStream` past the reply, which the current
`handle_stream` contract does not express. That gap is upstream-of-lojix and
is the real reason to HOLD on streaming, independent of the bump.

## (c) Multi-listener stop-cleanly + socket-path cleanup — do they fix a wire-audit issue?

Partial. Two changes, assessed against lojix's actual daemon:

- `should_continue()` (`ceb7794`) adds a DEFAULTED `MultiListenerRuntime`
  method returning `true`
  (`/git/github.com/LiGoldragon/triad-runtime/src/daemon.rs`, `should_continue`
  default + `serve_streams`/`serve_next_stream` now loop `while
  self.runtime.should_continue()`). Backward-compatible: lojix's
  `impl MultiListenerRuntime for LojixRuntime`
  (`/git/github.com/LiGoldragon/lojix/triad-port/src/daemon.rs:164-188`) does
  NOT define it, so it keeps serve-forever. This fixes nothing in lojix's
  current wire behavior; it only ENABLES a future supervised-stop. No wire-audit
  bug here.

- Socket-file cleanup on drop (`973e1d3`) adds `BoundSocketFile` with an
  `impl Drop { fs::remove_file }` so a dropped bound daemon unlinks its socket
  paths. This is a real hygiene improvement, but it is NOT a fix for any lojix
  bug TODAY, for two reasons:
  - The PINNED triad-runtime ALREADY removes the stale socket on BIND
    (`28d03c3:src/daemon.rs` `bind_listener` → `prepare` → `remove_stale_socket`
    at lines ~521-541). So a daemon RESTART already rebinds fine; the new code
    only closes the leftover-socket-after-clean-shutdown window.
  - lojix's own daemon round-trip test SIGKILLs the daemon
    (`tests/build_smoke.rs:146` `daemon.kill()`), so `Drop` never runs there
    anyway; the test relies on `tempdir` teardown + bind-time stale removal.
    The new drop cleanup does not touch this test's correctness.

Conclusion: neither commit fixes a CURRENT lojix wire-audit defect. They are
forward-looking enablers (clean supervised stop; tidy socket teardown). If a
sibling dimension's wire audit flagged "stale socket left after shutdown," this
commit addresses it — but for a SIGKILLed or bind-time-restarted daemon it is
moot.

## (d) Recommendation: HOLD now; bump only when streaming work is scheduled

HOLD. Rationale, concrete:

1. Zero forcing function. The generated engine-trait surface is signature-
   identical (a). The runner/`RunnerEngines` public surface is UNCHANGED across
   `28d03c3..973e1d3` (the `src/runner.rs`+`src/lib.rs` signature diff is
   empty). `ContinuationExhausted`/`ContinuationLimit` are unchanged and still
   exported at latest. So the hand impl does not need to change to keep
   compiling. Nothing is broken-at-pin that the bump fixes.

2. The only NEW capability (streaming runtime, b) is unreachable without
   separate feature work: declaring `streams()` in the signal contracts +
   wiring a `SubscriptionRegistry` + solving the retain-the-client-stream
   daemon gap. Bumping now imports `streaming.rs` as dead surface and pays the
   regen-and-recommit cost (the emitter's rustfmt-style reflow makes the
   checked-in `src/schema/{nexus,sema}.rs` stale vs `write_or_check`) for no
   functional gain.

3. The bump carries non-zero risk I could not certify read-only: `cargo update`
   moves transitive deps across all four engine crates' own lockfiles, and the
   regenerated artifacts must pass `build.rs` freshness. That is a build-and-
   verify loop the orchestrator owns; spending it now buys nothing.

Bump WHEN the streaming/Watch* milestone is scheduled (the named follow-on in
signal-lojix's schema header). At that point the step plan is:

1. `cargo update -p schema-rust-next -p triad-runtime -p schema-next` (and let
   signal-frame follow); expect transitive bumps in the lojix lock.
2. Regenerate the checked-in schema artifacts:
   `LOJIX_UPDATE_SCHEMA_ARTIFACTS=1 cargo build` (per `build.rs:36`), then
   recommit `src/schema/{nexus,sema}.rs` — expect rustfmt-style reflow churn,
   verify NO method-signature change (cross-check the regen against
   `runner_generated.rs` at the new rev).
3. Declare `Schema::streams()` + matching `Output.Event` in `signal-lojix`
   (and meta if it grows events) so the emitter generates the `Frame`/
   `RequestBuilder`/`into_subscription_frame` streaming surface.
4. Wire a `SubscriptionRegistry` into `LojixRuntime`, decide its lifetime
   across requests, and solve the daemon's retain-client-stream-past-reply
   gap (the `handle_stream` contract change). This is the real cost center.
5. Replace the `open_subscription` token-handshake stub
   (`schema_runtime.rs:362-377`) with a real `register`/publish path on
   `record_phase`.

Expected breakage on the bump itself (steps 1-2): only the artifact-freshness
check, resolved by regen-and-recommit. The hand impl does not need editing for
the bump to compile. The streaming surface (steps 3-5) is additive feature
work, not bump fallout.

## Confidence and limits

- HIGH on (a): the trait method-set comparison is from the checked-in generated
  fixtures, directly diffed pinned vs latest.
- HIGH on (b): the gate is documented in both the schema-rust-next INTENT
  (`4ee2c89`) and the signal-lojix schema header, and lojix's generated code
  has zero streaming surface.
- HIGH on (c): bind-time stale removal exists at the pin; the test SIGKILLs.
- I did NOT run a build (read-only). I therefore cannot certify the post-bump
  regen is byte-clean or that transitive-dep bumps compile — that is the
  orchestrator's verify loop, and is the one residual risk in the HOLD/bump
  decision. Stated plainly rather than assumed away.
