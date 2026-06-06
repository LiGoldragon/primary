# schema-rust-next refresh for lojix — the Rust emission layer

Crate: `schema-rust-next` (the build-dependency that emits lojix's checked-in
`triad-port/src/schema/*.rs`).
Path: `/git/github.com/LiGoldragon/schema-rust-next`
HEAD at survey: `6685e7b` (v0.1.13/0.1.14 era).
lojix pins (build-dependency): `c0a331a` (v0.1.13) — BEHIND every focus commit.

## Headline

schema-rust-next now EMITS A WHOLE DAEMON MODULE (`daemon_emit::DaemonModule`,
the `triad_main!` emitter, commit `33337d7`). This is the single most important
development for lojix: the crate now generates `src/schema/daemon.rs` carrying
the `ComponentDaemon` hook trait, `DaemonCommand` argv parsing, the
`GeneratedDaemonRuntime` decode→execute→encode spine, single/multi listener
selection, `DaemonError`, and `DaemonEntry::run_to_exit_code` — exactly the
surface lojix HAND-WROTE in `daemon.rs`. BUT the emitted daemon's shape does NOT
match lojix's two-contract / single-Nexus / worker-pool design, so it is a
PARTIAL replacement at best, with a real architectural mismatch and a concurrency
regression if adopted naively. The rest of the arc (frame-codec gating fix,
GAP-1 tokenization, Plane namespace family) is non-breaking for lojix but means
re-emission churns lojix's checked-in generated files and forces a coordinated
triad-runtime bump.

## What a component now gets generated (the daemon emitter)

Source: `src/daemon_emit.rs` (986 lines), entry `DaemonModule::new(shape,
schema, generator_name).to_generated_file()` → `src/schema/daemon.rs`. OFF by
default; turns ON when a component constructs a `NexusDaemonShape`
(`daemon_emit.rs:43`) carrying the OS process name + a `WorkingListenerTier`
(the working signal contract module name) + an optional `MetaListenerTier`
(owner socket mode bits). Streaming wiring is derived from the schema's declared
streams, not from the shape.

The emitted module (`DaemonModuleBody`, `daemon_emit.rs:208`) is composed of
per-section `ToTokens` nouns:

- `ComponentDaemon` hook trait (`daemon_emit.rs:317`) — the ONLY daemon code the
  component hand-writes. Associated types `Configuration: DaemonConfiguration`,
  `ConfigurationError`, `Engine`, `Error`; `const PROCESS_NAME`; required
  `load_configuration`, `build_runtime`, `handle_working_input`; default no-op
  `start`/`stop`; conditional `handle_meta_stream` (meta tier) and streaming
  hooks (declared stream).
- `DaemonCommand<Daemon>` (`daemon_emit.rs:424`) — argv → rkyv `Configuration`
  file → `Daemon::bind(...).run()`. Enforces the single-argument rule
  (`signal_file_argument()`); rejects inline-NOTA / NOTA-file as
  `ExpectedSignalFile`.
- `DaemonBinder` (`daemon_emit.rs:479`) — emitted default-method trait; builds
  the engine via `build_runtime`, constructs `GeneratedDaemonRuntime`, and
  selects `SingleListenerDaemon` vs `MultiListenerDaemon` from the shape (multi
  pushes a second `ListenerSocket::new(ListenerTier::Meta, ...)` with the owner
  socket mode).
- `WorkingTransport` (`daemon_emit.rs:558`) — length-prefixed envelope around the
  schema-emitted signal-frame codec; `read_frame`/`write_frame`/`try_clone_stream`.
- `EmittedSubscriptions` (`daemon_emit.rs:601`) — option-B streaming registry +
  publish wiring over `triad_runtime`'s `SubscriptionRegistry` +
  `SubscriptionEventPublisher` (only when a stream is declared).
- `GeneratedDaemonRuntime<Daemon>` (`daemon_emit.rs:727`) — owns the engine (and
  subscription registry); its `handle_working_stream` (`daemon_emit.rs:842`) IS
  the spine: `ConnectionContext::from_stream` → read frame →
  `Input::decode_signal_frame` → `Daemon::handle_working_input(engine, input,
  &connection)` → `output.encode_signal_frame()` → write frame → (option-B
  publish). Implements `MultiListenerRuntime` (multi) or `DaemonRuntime`
  (single).
- `ListenerTier` enum (`daemon_emit.rs:865`), `DaemonError<Daemon>`
  (`daemon_emit.rs:893`), `DaemonEntry::run_to_exit_code` (`daemon_emit.rs:968`).

What the consumer STILL hand-supplies: the whole `impl ComponentDaemon` — the
`Configuration`/`Engine`/`Error` types, `PROCESS_NAME`, `load_configuration`,
`build_runtime` (open the Store + construct the Engine — the emitter can't know
this), `handle_working_input` (the actual per-request execute), and (if present)
`handle_meta_stream` + the streaming policy hooks. Plus `fn main` calling
`<Daemon as DaemonEntry>::run_to_exit_code()`.

### `handle_working_input` — the hook signature (question b)

```
fn handle_working_input(
    engine: &Self::Engine,
    input: Input,                              // crate::schema::<working>::Input
    connection: &triad_runtime::ConnectionContext,
) -> Result<Output, Self::Error>;              // crate::schema::<working>::Output
```

It takes `&Self::Engine` (shared, NOT `&mut`), the decoded working-contract
`Input` root, and a `ConnectionContext` carrying kernel-vouched `SO_PEERCRED`
peer credentials (uid/gid/pid) so the component mints an origin from the OS
trust boundary instead of trusting a payload claim (added in `6685e7b`, psyche
`g3ax`). It returns the working-contract `Output` root. The spine captures
`ConnectionContext::from_stream(&stream)` BEFORE decode and threads it in
(`daemon_emit.rs:843,849`).

## How this bears on lojix's hand-written daemon.rs

lojix's `daemon.rs` (275 lines) and the emitted daemon overlap heavily in
INTENT but DIVERGE in three load-bearing ways. The emitted daemon is NOT a
drop-in replacement for lojix today.

### Overlap (the emitter would replace this hand-written code)

- `ListenerRole {Ordinary, Owner}` + `Display` ≈ emitted `ListenerTier
  {Working, Meta}` + `Display`. Identical pattern.
- `Daemon::run` socket binding (two `ListenerSocket`s on one
  `MultiListenerDaemon` with socket modes) ≈ emitted `DaemonBinder::bind` multi
  path.
- `map_daemon_error` ≈ emitted `DaemonError` `From<MultiListenerDaemonError>`.
- The argv→config→bind→run flow lojix puts in its `lojix-daemon` bin ≈
  `DaemonCommand` + `DaemonEntry::run_to_exit_code`.
- The `serve_*` decode→execute→encode body ≈ the emitted
  `handle_working_stream` spine.

### Mismatch 1 — single-Nexus two-contract routing vs working+meta-escape-hatch

This is the decisive architectural divergence. lojix routes BOTH tiers into ONE
Nexus plane: the ordinary frame decodes to `signal_lojix::...::Input` and the
owner frame to `meta_signal_lojix::...::Input`, each WRAPPED into one
`nexus::SignalInput::{OrdinaryInput, MetaInput}` enum, then driven through a
SINGLE `SchemaRuntime::execute` runner (`daemon.rs:189-231`). The owner tier
gets the full typed decode→execute→encode through the same engine and the same
runner continuation loop (the deploy pipeline).

The emitted daemon's model is asymmetric: the WORKING tier drives one contract's
`Input`/`Output` through the spine + `handle_working_input`; the META tier is a
fully component-owned `handle_meta_stream(engine, stream)` ESCAPE HATCH handed a
raw `UnixStream` — no emitted frame spine, no decode, no typed input. lojix's
owner tier is a first-class typed path, NOT an escape hatch. If lojix adopted the
emitter as-is, lojix would have to either (a) demote its owner tier to a
hand-written `handle_meta_stream` (losing the uniform engine routing it
deliberately built), or (b) keep its richer single-Nexus daemon. The emitter's
working-tier `Input` is also a SINGLE contract's `Input` (`use
crate::schema::<working>::{Input, Output}`, `daemon_emit.rs:293`) — it has no
notion of a daemon whose two tiers carry two different external wire contracts
funnelled into a runtime Nexus root. lojix's `nexus::SignalInput` is a runtime
Nexus root that wraps both, which is a shape the emitter does not model.

### Mismatch 2 — serial spine vs lojix's BoundedWorkers concurrency (REGRESSION)

triad-runtime's `MultiListenerDaemon::serve_streams` calls `handle_stream`
SERIALLY inline in the accept loop (triad-runtime `daemon.rs:371-372`); there is
no offload in the runtime. The emitted `GeneratedDaemonRuntime::handle_working_stream`
runs decode→execute→encode SYNCHRONOUSLY. So the emitted daemon is SERIAL: a
multi-minute `nix` build blocks the accept loop and every other connection.

lojix's `LojixRuntime::handle_stream` (`daemon.rs:151-165`) deliberately offloads
each request onto a shared `BoundedWorkers` pool (cap 64) and returns
immediately, so the accept loop stays responsive on BOTH sockets while a deploy
runs — this is lojix's M1 concurrency win ("a query answered in ~4ms while a
deploy ran", intent 2alg / k6w1). The emitted daemon does NOT carry worker
offload. Adopting the emitted spine as-is would REGRESS lojix's headline
concurrency property. The emitter would need a "concurrent spine" option (offload
`handle_working_input` onto `BoundedWorkers`, build a fresh per-request engine
over a shared `Arc<Store>`) before it can host lojix's daemon.

### Mismatch 3 — per-request fresh engine over Arc<Store> vs single engine

The emitted `GeneratedDaemonRuntime` owns ONE `engine: Daemon::Engine` and calls
`handle_working_input(&self.engine, ...)` with a shared `&engine`
(`daemon_emit.rs:830,849`). lojix builds a FRESH per-request `SchemaRuntime` over
a clone of a shared `Arc<Store>` per connection (`daemon.rs:220`,
`RequestWorker::execute`) so each request's in-flight deploy cursor is local and
concurrent requests never corrupt each other's state. The emitted `&Self::Engine`
single-engine model + serial spine is coherent with each other but incompatible
with lojix's "shared durable Store, per-request engine" split. This is the same
root mismatch as #2: the emitter assumes a serial single-engine daemon.

### Bottom line on daemon.rs

The emitter REPLACES lojix's boilerplate (socket binding, error mapping, argv
parsing, exit body, the listener-tier enum) but does NOT yet host lojix's three
load-bearing choices (two-contract single-Nexus routing, BoundedWorkers
concurrency, per-request engine over Arc<Store>). Porting lojix onto the emitted
daemon today would be a DOWNGRADE. The right move is to feed these three shapes
back into the emitter as designer requirements (the emitter explicitly invites
this — its doc calls the hook trait "the 1488 escape hatches"), then adopt. This
is a designer-to-designer conversation, not a small port.

## Frame-codec emission (799f678) — question c

Sequence to understand:
1. The Plane family commit `7f59b39` over-stripped the frame codec
   (`InputRoute`, `encode_signal_frame`, `decode_signal_frame`,
   `SignalFrameError`) from `WireContract` targets — the "gb95 over-reach"
   (visible as the test flipping `contains`→`!contains` in `7f59b39`'s
   `tests/emission.rs` diff).
2. `799f678` RE-ADDED the basic frame codec to all wire-facing targets via a new
   `RustEmissionTarget::emits_wire_frame()` (`WireContract | SignalRuntime |
   ComponentRuntime` → true; `NexusRuntime | SemaRuntime` → false). Only the
   streaming/observable surface stays gated by `emits_signal()` + a declared
   stream.

Does re-emitting lojix's schema change its checked-in `src/schema/*.rs`?

- lojix's CONTRACT crates (`signal-lojix`, `meta-signal-lojix`) use
  `GenerationPlan::wire_contract` (`WireContract` target) and ALREADY carry the
  frame codec (`signal-lojix/triad-port/src/schema/lib.rs:945,1025,1034`;
  meta at `:655,728,737`). lojix is NOT missing a hand-rolled codec — it never
  hand-rolled one; the codec was always emitted. So `799f678` does not ADD
  anything lojix lacks.
- The DANGER is the intermediate window: lojix pins `c0a331a`, which is BEFORE
  the over-reach. If lojix bumps to a revision in the `7f59b39..799f678` window,
  re-emission would STRIP the codec from both contract crates and break the
  daemon (which calls `Input::decode_signal_frame` / `encode_signal_frame`,
  lojix `daemon.rs:192,197,204,208`). Bumping all the way to HEAD (`6685e7b`,
  past the fix) is SAFE. Net: re-emission at HEAD leaves lojix's contract codecs
  materially unchanged; the only risk is stopping at a bad intermediate pin.
- lojix's DAEMON-side generated planes (`nexus.rs`, `sema.rs`, `NexusRuntime` /
  `SemaRuntime` targets) never carried the wire frame codec and still don't —
  unaffected by `799f678`.

## Plane namespace family (7f59b39 / 3ebeeda / 9ca8754) — question d

These carry a `Plane` token-namespace noun through the engine traits and trace
object names. Per INTENT/ARCHITECTURE, `Plane` owns ONLY plane-intrinsic names
(module, wrapper, export aliases, engine trait, trace enum names); the GENERATED
PUBLIC SURFACE is unchanged — `nexus::NexusEngine`, `nexus::NexusObjectName`,
`sema::SemaEngine`, `sema::WriteInput`, etc. lojix's generated code ALREADY uses
the Plane-namespaced engine trait form (`fn decide(&mut self, input:
nexus::Nexus<nexus::Work>)`, `apply_inner(input: sema::Sema<sema::WriteInput>)`,
lojix `nexus.rs:1258`, `sema.rs:1444`), so lojix is already aligned with the
Plane direction — its pin `c0a331a` is after the plane-namespace-module work.

Does it RENAME/RELOCATE anything lojix depends on? No renames of the
lojix-consumed surface: `NexusEngine`, `SemaEngine`, `NexusObjectName`,
`SemaObjectName`, `ObjectName`, the `*Route` enums, `NexusRunnerNextStep`,
`into_next_step`, and the `impl triad_runtime::NexusAction for NexusAction` role
impls all keep their names (verified in lojix `nexus.rs:1233,1215,1222,1047,1082`
and `sema.rs:1428`). The Plane commits are an emitter-internal refactor (the
emitter builds these names through a `Plane` noun instead of ad-hoc strings).

The CATCH: the Plane commits plus the tokenization commits (`e332b5e`,
`fa0d4fa`, `fd84aae`, `7783ae6`) and GAP-1 (`4ac90de`) changed the golden
fixtures by ~109 lines each — but these are PURELY prettyplease canonicalization
(blank-line removal, multi-line match-arm wrapping; verified by reading the
`e332b5e` runner-fixture diff: `write!(...)` single-line → braced multi-line,
stray blank lines dropped). NO type/item/logic/ordering change. So re-emitting
lojix's `nexus.rs`/`sema.rs` at HEAD produces a FORMATTING-CHURNED but
SEMANTICALLY IDENTICAL file. lojix's `build.rs` freshness check
(`write_or_check("LOJIX_UPDATE_SCHEMA_ARTIFACTS")`) would FAIL on a bump until
the artifacts are regenerated and re-checked-in.

## GAP-1 string→token migration (4ac90de)

The `RustWriter` string god-struct was eliminated (renamed `RustModuleRenderer`,
builds zero Rust strings); all emission is token-based (145 `quote!`, 42
`ToTokens`); `migration.rs` fully tokenized. This is internal emitter hygiene —
it does not change the generated SEMANTICS, only the canonical formatting (the
same prettyplease churn noted above). Bears on lojix only as: the emitter is now
fully aligned with the workspace's token-first / no-string-emission discipline,
and the daemon emitter (`33337d7`) was built token-first from the start. No
action for lojix beyond the re-emission churn.

## triad-runtime coupling (prerequisite for the daemon emitter)

The emitted daemon imports `triad_runtime::ConnectionContext` (added
triad-runtime `33b9531a`), `DaemonConfiguration` + `ExitReport` (added
`1bd383bf`), plus `SubscriptionRegistry`/`SubscriptionEventPublisher` (streaming)
and the `Single/MultiListenerDaemon` set. lojix pins triad-runtime `fdfd1831`
(the BoundedWorkers commit), which is BEHIND `ConnectionContext` and the
daemon-emit support. So ANY adoption of the emitted daemon REQUIRES a coordinated
triad-runtime bump to >= `33b9531a`. lojix's CURRENT hand-written daemon does NOT
need `ConnectionContext` and works on `fdfd1831`; lojix is not blocked unless it
adopts the emitter. See the sibling triad-runtime report for the runtime-side
detail.

## Recommendations for lojix

### Must do (correctness / drift hygiene)

1. **Pin-bump policy: never stop in the `7f59b39..799f678` window.** When lojix
   bumps schema-rust-next, bump straight to HEAD (`6685e7b`), which has the
   frame-codec fix. A pin inside that window would re-emit contract crates
   WITHOUT the frame codec and break the daemon's `*_signal_frame` calls. Effort:
   small. Risk: low if HEAD; HIGH if an intermediate pin is chosen by accident.

2. **Re-emit and re-check-in generated files on any bump, expecting formatting
   churn.** Bumping past the tokenization/GAP-1/Plane commits changes the
   prettyplease canonicalization of `nexus.rs`/`sema.rs` (and the contract
   crates' `lib.rs`) by ~100+ lines each, semantically identical. Run with
   `LOJIX_UPDATE_SCHEMA_ARTIFACTS` set, re-check-in, and eyeball the diff to
   confirm it is formatting-only (no type/route/logic change). Effort: small.
   Risk: low (formatting only) — but the build freshness check FAILS until done,
   so it is a hard prerequisite for the bump.

### Should consider (the daemon emitter — a designer conversation, not a port)

3. **Do NOT adopt the emitted daemon as-is — feed lojix's three shapes back to
   the emitter first.** The emitted daemon would replace lojix's boilerplate but
   regress its (a) two-contract single-Nexus routing, (b) BoundedWorkers
   concurrency, and (c) per-request engine over Arc<Store>. The emitter's working
   tier assumes ONE contract `Input`/`Output` + a meta escape hatch, a SERIAL
   spine, and a SINGLE shared engine. Treat these as designer requirements for
   the emitter: a "two-wire-contract Nexus root" working tier, a concurrent-spine
   option (offload onto `BoundedWorkers`, fresh per-request engine), and an
   Arc<Store>-shared engine model. Effort: large (cross-repo emitter design +
   triad-runtime bump). Risk: high if rushed — adopting the current emitted
   daemon would be a downgrade.

4. **Adopt the cheap, shape-compatible pieces opportunistically even before #3.**
   Independently of the full daemon, lojix could align its hand-written daemon to
   the emitted vocabulary where the shapes already match: `ConnectionContext` for
   peer-credential origin minting (lojix's audit R3 noted it has NO peer-cred
   check yet on the owner socket — `daemon.rs:96-104`; the emitter's
   `ConnectionContext` is exactly the primitive to close that gap), and the
   `DaemonError`/`DaemonEntry`/`DaemonCommand` shapes. This is a partial,
   low-risk alignment that does not require the full emitted spine. Effort:
   medium. Risk: low. NOTE this still needs the triad-runtime bump to >=
   `33b9531a` for `ConnectionContext`.

### Nice to have

5. **Track the emitter's streaming (option B) for lojix's subscription work.**
   lojix's `Store` already carries a `subscription_sequence` counter
   (`lib.rs:116,156`) and the sema schema has subscription nouns, suggesting a
   streaming surface is planned. The emitter's `EmittedSubscriptions` +
   `ComponentDaemon` streaming hooks (`daemon_emit.rs:601,346`) are the
   schema-derived path for that — when lojix declares a stream and adopts the
   emitter, the subscription hub is emitted rather than hand-written. Not
   actionable until #3. Effort: n/a (downstream of #3). Risk: n/a.

## Adversarial notes — what does NOT apply to lojix

- **The frame-codec fix `799f678` does not "give lojix a codec it hand-rolled."**
  lojix never hand-rolled a frame codec; its contracts always emitted one. The
  fix only matters as a pin-window hazard (recommendation 1), not as a missing
  feature.
- **The Plane family does NOT rename anything lojix consumes.** Despite touching
  ~340 lines of `lib.rs` and the engine/trace emission, the lojix-facing
  generated names (`NexusEngine`, `SemaEngine`, `*ObjectName`, `*Route`,
  `into_next_step`, role impls) are name-stable. The only lojix impact is
  formatting churn, already covered by recommendation 2.
- **GAP-1 tokenization has zero semantic effect on lojix.** It is emitter-internal
  hygiene; the only downstream artifact is prettyplease formatting.
- **The emitted daemon is not "free concurrency" for lojix.** It is SERIAL; it
  would remove, not add, lojix's concurrency. This is the most important
  adversarial correction in this report.
