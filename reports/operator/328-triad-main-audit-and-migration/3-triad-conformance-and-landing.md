# 328/3 — triad_main: triad/engine conformance, streaming soundness, landing risk

Read-only audit of the emitted daemon module (`triad_main!`, design 542 /
handoff 543) on branch `origin/designer-daemon-emit-2026-06-06` across
schema-rust-next (the emitter), triad-runtime (the engine primitives), and
spirit (the pilot). Dimension: triad/engine conformance + Option-B streaming +
cross-repo landing.

## Verdict in one paragraph

The emitted daemon is **triad-conformant and streaming-sound**. The spine
routes Signal-decode -> component engine -> Signal-encode without any plane
bleed in the generated code; the SEMA log-write path is never re-entered by the
meta tier; the wire is rkyv signal-frame only and the single-NOTA-argument rule
holds at argv. The Option-B streaming plumbing (registry + publisher + the
MutexGuard borrow-split + the emitted rkyv `StreamEvent` bound) is correct and
non-blocking, proven end-to-end by spirit's `process_boundary` subscription
test. **The landing is mechanically clean and GREEN** — I performed a real test
merge of the branch onto current (post-Gap-1) schema-rust-next main: it
auto-merges with no conflict markers, `cargo check` passes after `cargo update
-p triad-runtime`, and the daemon-emission tests pass. The single material flaw
is the one 543 already names: `daemon_emit.rs` is fully string-based and
violates standard **4np2** (token-based emission). That is a real but
non-blocking debt — it does not block landing, but it must be migrated to the
`RustModuleRenderer`/`ToTokens` approach Gap-1 established. Everything else is
nits.

## What I checked (falsifiable)

- Emitter source: `schema-rust-next-daemon-emit/src/daemon_emit.rs` (807 lines),
  `src/build.rs`, `tests/daemon_emission.rs`.
- Emitted output: `spirit:src/schema/daemon.rs` (the generated file).
- Engine primitives: `triad-runtime:src/streaming.rs`, `src/process.rs`.
- Pilot impl + tests: `spirit:src/daemon.rs`, `src/engine.rs`,
  `src/meta_transport.rs`, `src/bin/spirit-daemon.rs`, `tests/public_surface.rs`,
  `tests/daemon_command.rs`, `tests/process_boundary.rs`.
- Landing: real `git merge` of the branch onto `origin/main` in a throwaway
  worktree, plus `cargo check`/`cargo test daemon` on the merged tree.

## 1. 3d5z triad separation — CLEAN

The generated spine does NOT do decision-making or state mutation itself; it
decodes, delegates to the component engine, and encodes. From the emitted
`GeneratedDaemonRuntime::handle_working_stream`
(`spirit:src/schema/daemon.rs`):

```rust
let frame = transport.read_frame()?;
let (_route, input) = Input::decode_signal_frame(&frame)?;          // Signal: decode
let output = Daemon::handle_working_input(&self.engine, input)?;    // delegate to engine
transport.write_frame(output.encode_signal_frame()?)?;             // Signal: encode
```

`Daemon::handle_working_input` is the only seam, and spirit implements it as
`engine.handle(input).root().clone()` (`spirit:src/daemon.rs`). The
Signal -> Nexus -> SEMA routing lives entirely inside `Engine`
(`spirit:src/engine.rs`) — the emitter has zero knowledge of Nexus or SEMA. No
plane is named in the emitted runtime except Signal (`Input`/`Output` decode +
encode). This is correct: the emitter owns only the **communication edge**
(Signal-plane wire + socket), and the component owns decision/state behind one
trait method.

Meta tier separation is also clean. `handle_meta_stream` is a full component
escape hatch; spirit's `engine.configure` (`src/engine.rs:183`) is explicitly a
**config effect, not a SEMA log write** — it records the archive target on
Nexus state under the same single-flight Nexus mutex the working path uses, and
the doc-comment correctly states it "never re-enters the Signal -> Nexus -> SEMA
working pipeline." No SEMA-owns-durable-state violation: durable intent records
still flow only through the working pipeline.

**No plane bleed found in the generated daemon.** (Conformant.)

## 2. Single-argument rule + no-NOTA-on-the-wire — CLEAN

- **argv is the only NOTA edge.** The emitted `DaemonCommand::configuration`
  calls `self.command.signal_file_argument()` and accepts ONLY
  `ComponentArgument::SignalFile`, returning `ArgumentError::ExpectedSignalFile`
  for `InlineNota`/`NotaFile`. So the daemon binary takes exactly one argument —
  a signal-encoded (rkyv) configuration file — and explicitly rejects inline or
  file NOTA. The bin is a true one-liner
  (`spirit:src/bin/spirit-daemon.rs`): `SpiritDaemon::run_to_exit_code()`. No
  flags anywhere. Config is the typed `Configuration` rkyv struct loaded via
  `Daemon::load_configuration`. **Conformant.**
- **The socket wire is rkyv signal-frame only.** `WorkingTransport` reads/writes
  a `LengthPrefixedCodec` envelope around `Input::decode_signal_frame` /
  `Output::encode_signal_frame` — binary signal frames, no NOTA. The meta tier
  (`MetaSignalTransport`, `spirit:src/meta_transport.rs`) likewise reuses the
  schema-emitted `encode_signal_frame`/`decode_signal_frame` codec over the same
  length-prefix framing. The subscription-event path (`deliver`) encodes a
  `signal_frame::StreamingFrame` to bytes over the same length-prefix codec — no
  NOTA. **Conformant.**

## 3. Option-B streaming emission — SOUND + NON-BLOCKING

The emitted `EmittedSubscriptions` (registry + publisher + register/publish/
deliver) reuses `triad-runtime`'s `SubscriptionRegistry` +
`SubscriptionEventPublisher` (`triad-runtime:src/streaming.rs`). Two specific
543 claims verified, both genuinely fixed (not papered over):

**(a) The MutexGuard borrow-split in `publish` is real and correct.** In
`EmittedSubscriptions::publish` (`spirit:src/schema/daemon.rs`):

```rust
let mut guard = self.state.lock().expect("subscription state lock");
let state = &mut *guard;                     // reborrow once into owned &mut
let publisher = &mut state.publisher;        // exclusive borrow of one field
let registry = &state.registry;              // shared borrow of a sibling field
```

This is the standard Rust disjoint-field-borrow idiom. Going through
`MutexGuard`'s `Deref`/`DerefMut` directly would borrow the whole `Deref::Target`
and the `&mut publisher` + `&registry` split would conflict; `let state = &mut
*guard` reborrows the guard into a plain `&mut SubscriptionState`, after which
the borrow checker sees two disjoint fields. This compiles, is sound, and the
inline comment explains exactly why. **Not papered over.**

**(b) The emitted `StreamEvent` rkyv bound is correct and necessary.** The
emitted `ComponentDaemon::StreamEvent` associated type carries:

```rust
type StreamEvent: Clone + rkyv::Archive
    + for<'archive> rkyv::Serialize<
        rkyv::api::high::HighSerializer<
            rkyv::util::AlignedVec,
            rkyv::ser::allocator::ArenaHandle<'archive>,
            rkyv::rancor::Error>>;
```

This mirrors exactly what `signal_frame::StreamingFrame::encode` requires of the
event payload (the publisher constructs a `StreamingFrame<Input, Output,
StreamEvent>` and calls `.encode()` in `deliver`). Without the bound the emitted
`deliver` would not compile; with it, the event rides the wire. The bound is
spelled out as a full English path (no abbreviation). **Correct.**

**Non-blocking confirmed end-to-end.** The delivery model in the emitted
`publish` collects matching frames, then writes each to its subscriber's stored
`UnixStream` writer, dropping stale writers on IO error (`Err(_) =>
stale.push(token)` then `unregister`). The working request is replied BEFORE
any publish — `write_frame(output...)` happens in `handle_working_stream`
before `self.subscriptions.publish(event)`. spirit's
`cli_subscription_receives_matching_intent_events_without_blocking_daemon`
(`tests/process_boundary.rs:298`) proves it against the *emitted* daemon binary
over a real socket: an ordinary `Record` completes while a subscription is open
(`assert_no_output` for the non-matching one, then the matching record pushes an
`IntentRecorded` event to the subscriber). **Sound + non-blocking.**

One soundness caveat worth flagging (minor, below): publish delivery is
synchronous within the working request's handler thread. A slow/blocked
subscriber writer could stall the publishing request thread (not the whole
daemon — the listener is per-stream), but a wedged subscriber socket holds the
publishing request open until its `write_body` returns or errors. This matches
the hand-written hub it replaced (no regression), but see Flaw MINOR-1.

## 4. spirit pilot integration — NOTHING LOST

The branch deletes the hand-written `DaemonCommand`/`Daemon`/
`SpiritDaemonRuntime` + the entire `SubscriptionHub` and replaces them with
`impl ComponentDaemon for SpiritDaemon` + the emitted `daemon.rs`. Checked:

- **Behavior preserved.** Every working operation still routes through
  `engine.handle`; the meta `Configure` path is preserved verbatim in
  `handle_meta_stream`; the streaming filter/token/event policy moved into the
  five `ComponentDaemon` hooks (`subscription_filter`, `subscription_token`,
  `published_event`, `event_matches_filter`, `subscription_event_short_header`)
  with the same semantics. A thin `Daemon::new(cfg).run()` wrapper is retained
  for in-process test launchers — a reasonable convenience, not dead weight.
- **Tests preserved + still green per 543** (`process_boundary` 8/8 including
  the streaming + trace tests, `daemon_command` argv tests). `process_boundary`
  covers the same ground: rkyv exchange, subscription non-blocking, state
  classification, certainty change, alias rendering, SEMA persistence across
  restart, candidate-handover database isolation, and trace events.
- **`public_surface.rs` guard change is sound.** The guard still forbids
  flattening the four generated *plane* modules
  (`signal`/`nexus`/`sema`/`meta_signal`) into `spirit::*` via
  `pub use schema::<plane>::`, and exempts `schema::daemon` because the daemon
  entry surface (`DaemonCommand`/`DaemonEntry`/`DaemonError`/`ComponentDaemon`)
  IS the daemon's public API and is re-exported deliberately so the bin can
  `use spirit::{DaemonEntry, SpiritDaemon}`. The guard's stated intent (keep
  wire/runtime nouns reached through `spirit::schema::`) is preserved; the daemon
  module is an entry-point, not a plane. **Sound.**

## 5. Cross-repo landing risk — LOW; merge is clean and GREEN

This was the headline concern in the task (the daemon-emit branch was built off
PRE-Gap-1 main; current main has the token rewrite that deleted `RustWriter` →
`RustModuleRenderer`). I tested it for real rather than reasoning about it:

- The branch's `lib.rs` change is genuinely additive at the merge base
  (`+pub mod daemon_emit;` + 4 reexport lines), but the **two-dot** divergence
  from current main is large (Gap-1 rewrote ~1340 lines of `lib.rs`). The risk
  was that git would either reintroduce the deleted string `RustWriter` or drop
  the daemon additions.
- **Real test merge result (authoritative):** `git merge --no-commit
  origin/designer-daemon-emit-2026-06-06` onto `origin/main` auto-merges with
  **zero conflict files**. The merged `lib.rs` has `RustModuleRenderer` (Gap-1's
  token renderer) and **zero** `struct RustWriter` (Gap-1's deletion wins), AND
  keeps `pub mod daemon_emit` + the reexports; merged `build.rs` keeps the
  daemon dispatch (`match emission.daemon_shape()` → `DaemonModule::new(..)`).
  git correctly composed Gap-1's deletion with the branch's additive module.
- **The merged tree compiles**: `cargo check` passes after `cargo update -p
  triad-runtime` (the lockfile regen 543 calls for). The daemon-emission tests
  pass on the merged tree (`daemon_module_emits_*`,
  `multi_listener_daemon_emits_the_listener_tier_routing`,
  `daemon_runtime_driver_emits_nexus_and_sema_files_with_plane_targets`).
- **`daemon_emit.rs` is self-contained** — it uses its own
  `DaemonModuleWriter`, never the deleted `RustWriter` (only a stale doc-comment
  mentions the old name, see NIT-1). So Gap-1's removal of `RustWriter` does not
  break the daemon emitter.

**Ordering (543's plan holds):** triad-runtime → schema-rust-next → spirit, each
with a lockfile regen against the freshly-landed upstream. The one ordering
caveat I'd add: schema-rust-next must be landed/merged THROUGH the auto-merge
above (not cherry-picked or rebased blindly), because the value is in git
composing Gap-1 + daemon additions; and the operator MUST `cargo update -p
triad-runtime` before verifying, because the branch's pushed lockfile is stale
from the dev `[patch]` (the merged tree's `cargo check` only went green after
that update). No reconciliation of `daemon_emit.rs` against the token direction
is needed for landing — that is the separate 4np2 debt (BLOCKER-as-debt below),
not a landing blocker.

## Flaws

### MAJOR-1 (4np2) — daemon_emit.rs is fully string-based; violates token-emission standard

`schema-rust-next-daemon-emit/src/daemon_emit.rs` emits the entire daemon module
through `DaemonModuleWriter` (a `String` + `self.line(...)` / `format!` writer) —
zero `quote!`, ~400 string-emission constructs across 807 lines. Standard 4np2
(VeryHigh, 2026-06-06) requires schema-to-Rust lowering to use real Rust macro
infra (`quote!`/proc-macro2 `TokenStream`/`ToTokens`), and Gap-1 already
eliminated string emission everywhere else in this crate (RustWriter →
`RustModuleRenderer` + `ToTokens` wrappers). The daemon emitter is the last
string-based holdout.

This is correctly NOT a landing blocker (the emitted output is correct and the
merge is green), but it is a real standard violation and must be migrated. It is
tagged MAJOR rather than BLOCKER only because it is known, isolated, and the
generated output is verified-correct; leaving it string-based indefinitely would
make it a BLOCKER against 4np2.

**Fix:** rewrite `DaemonModule::render` to build a `proc_macro2::TokenStream` via
`quote!`, mirroring Gap-1's `RustModuleRenderer`/`ToTokens` approach. The
`NexusDaemonShape`/`WorkingListenerTier`/`MetaListenerTier`/`DaemonStreamShape`
model types should grow `ToTokens` impls (or feed a `quote!` template) so the
shape *is* the noun and the tokens come from it (de8i). The goldens in
`tests/daemon_emission.rs` pin the output, so the rewrite is a
behavior-preserving refactor checkable against them.

### MINOR-1 — synchronous publish can stall the publishing request thread on a wedged subscriber

In the emitted `EmittedSubscriptions::publish`, `deliver` does a blocking
`write_body` + `flush` to each matching subscriber's `UnixStream` inline, inside
the working request's handler. A subscriber whose socket buffer is full (slow or
hung reader) blocks the *publishing* request until the write returns or errors.
The listener is per-stream so the whole daemon does not freeze, but the request
that triggered the event is held open. 543 frames the test as proving
"without blocking the daemon," which is true at the daemon level; it does not
prove the publishing request is insulated from a slow subscriber.

This matches the hand-written `SubscriptionHub` it replaced (no regression), so
it is MINOR, not a blocker. **Fix (future):** give `EmittedSubscriptions` a
non-blocking write path (set subscriber writers non-blocking and drop on
`WouldBlock`, or move delivery to a dedicated publisher thread/actor per
`skills/actor-systems.md`). Worth a follow-up bead; not required to land.

### MINOR-2 — `Daemon::ConfigurationError: std::fmt::Display` only; no `std::error::Error`

The emitted `ComponentDaemon::ConfigurationError` is bounded only by
`std::fmt::Display`, and `DaemonError::Configuration(Daemon::ConfigurationError)`
uses `#[error("daemon configuration error: {0}")]`. This works, but a typed
crate error should be `std::error::Error` (source chaining) per
`skills/rust/errors.md`. spirit's `ConfigurationError` does implement `Error`,
so this is latent — but the trait bound permits a non-`Error` configuration
error that would silently lose `source()`. **Fix:** tighten the bound to
`std::fmt::Display + std::error::Error` (or `Into<Box<dyn Error>>`) so the
emitted error enum chains sources properly. Low effort, do it during the 4np2
rewrite.

### NIT-1 — stale doc-comment references the deleted `RustWriter`

`daemon_emit.rs:194` doc-comment: "Line-oriented writer for the daemon module,
mirroring the `RustWriter` line/blank style…". Gap-1 renamed `RustWriter` →
`RustModuleRenderer`, so this is now a dangling reference (also a `[RustWriter]`
intradoc link that would warn under `-D rustdoc::broken_intra_doc_links` if it
were a real link path). The whole comment is moot once MAJOR-1 lands (the writer
disappears). **Fix:** delete or update when migrating to tokens.

### NIT-2 — `DaemonModuleWriter` is a transient string-builder noun that vanishes under 4np2

`DaemonModuleWriter` (`output: String`, `self.line`/`self.blank`) is a
data-bearing type so it passes the no-ZST methods rule today, but it exists only
to accumulate emitted text — exactly the construct 4np2 retires. Not a separate
flaw from MAJOR-1; noted so the reviewer doesn't "fix" it into a cleaner string
writer instead of deleting it for tokens.

## Bottom line

Triad separation: conformant (no plane bleed in generated code). Streaming:
sound and non-blocking (borrow-split + rkyv bound genuinely fixed, proven
end-to-end). Single-argument + rkyv-only wire: conformant. spirit integration:
nothing lost, guard change sound. **Landing: low risk — the merge onto post-Gap-1
main is clean, compiles, and tests green (verified by real test merge); land in
order triad-runtime → schema-rust-next → spirit with `cargo update -p
triad-runtime` before verifying each downstream.** The one real debt is the 4np2
string-emission violation in `daemon_emit.rs` (MAJOR-1) — migrate it to the
`quote!`/`ToTokens` approach, but it does NOT block landing.
