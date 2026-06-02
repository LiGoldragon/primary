; designer
[name-only-trace schema-rust-next spirit-next research prototype layer-2-witness]
[Research + prototype of the name-only trace shape per Spirit 1394 Correction High. Confirms schema-rust-next bfacb96 ALREADY emits name-only activation hooks; spirit-next b5ced5cc pins the prior payload-bearing emitter. The prototype on worktree designer-name-only-trace-2026-06-02 (1) repins schema-rust-next at bfacb96, (2) collapses trace.rs from 407 to ~180 lines, (3) adapts engine.rs/nexus.rs/store.rs to override one activation hook per plane, (4) rewrites instrumentation_logging.rs to assert on name sequences instead of payload structure. All 39 tests pass (3 testing-trace + 36 default). Net diff: 105 insertions / 462 deletions across 9 files. Recommendation: ratify name-only as the shape; operator integrates the worktree branch.]
2026-06-02
designer

# 467 — Name-only trace: research and prototype

## TL;DR

Spirit 1394 (Correction High, 2026-06-02) asks: trace records only the
**name** of the object being activated; the macro-generated interface
already has the name, so trace should not carry rich payload snapshots
per boundary.

**Schema-rust-next `bfacb96` (main HEAD, 2026-06-02) already implements
the name-only emission shape.** Spirit-next main `b5ced5cc` still pins
the prior emitter `8264f3d` (payload-bearing). The prototype work
reduces to: (1) repin schema-rust-next, (2) shrink `src/trace.rs`,
(3) collapse the per-phase hook overrides in `engine.rs` /
`nexus.rs` / `store.rs` into a single `trace_<plane>_activation` hook
per plane, (4) rewrite the Layer 2 witness test to assert on name
sequences.

**Result on worktree
`designer-name-only-trace-2026-06-02`** (branch pushed to
`origin/designer-name-only-trace-2026-06-02`, base commit `b5ced5cc`):

- All 3 testing-trace Layer 2 witness tests pass (record-then-observe
  12-event sequence, default-engine 6-event record, rejection-path
  2-event without Nexus/SEMA).
- All 36 non-testing-trace tests pass.
- `cargo clippy --features testing-trace --all-targets -- -D warnings`
  clean.
- Net diff: **105 insertions / 462 deletions** across 9 files. A 357-line
  reduction for the same Layer 2 witness strength.

**Recommendation: ratify the name-only shape.** The simplification works
end-to-end; the witness strength is preserved (still proves runtime
crossing of Signal admission, Signal engine, Nexus engine, SEMA engine);
the payload-bearing edges that disappear were diagnostic luxuries
specific to test assertions, not the architectural-crossing proof.

## Frame

The research-and-prototype task carries three deliverables: research
findings (does the shape work, what edges does it miss), a worktree
prototype with executable code, and a Layer 2 witness test under the
new shape proving the architectural-crossing claim. The fourth
deliverable is this report.

The shape proposed by the orchestrating designer's main-agent:
`TraceEvent` becomes a unit-variant enum (or in the harness-converged
form here, a thin struct around an `&'static str` name); engine hook
signatures drop the payload parameter; optionally keep `OriginRoute`
for concurrent-trace correlation.

## Research findings

### Schema-rust-next already emits name-only hooks

The emission state on `schema-rust-next` main `bfacb96` ("trace hooks
emit activation names", 2026-06-02 09:11:24) carries the name-only
shape in full:

```rust
pub trait SignalEngine {
    fn trace_signal_activation(&self, _object_name: &'static str) {}
    fn trace_signal_admitted(&self) {
        self.trace_signal_activation("SignalAdmitted");
    }
    fn trace_signal_rejected(&self) {
        self.trace_signal_activation("SignalRejected");
    }
    fn trace_signal_triaged(&self) {
        self.trace_signal_activation("SignalTriaged");
    }
    fn trace_signal_replied(&self) {
        self.trace_signal_activation("SignalReplied");
    }

    fn triage_inner(&self, input: signal::Signal<signal::Input>) -> nexus::Nexus<nexus::Input>;
    fn reply_inner(&self, output: nexus::Nexus<nexus::Output>) -> signal::Signal<signal::Output>;

    fn triage(&self, input: signal::Signal<signal::Input>) -> nexus::Nexus<nexus::Input> {
        let output = self.triage_inner(input);
        self.trace_signal_triaged();
        output
    }
    /* reply same shape */
}
```

Same shape for `NexusEngine` (`trace_nexus_activation`,
`trace_nexus_entered`, `trace_nexus_decided`) and `SemaEngine`
(`trace_sema_activation`, `trace_sema_write_applied`,
`trace_sema_read_observed`). Source: `schema-rust-next/src/lib.rs`
`fn emit_schema_plane_trait_support` (lines 1748-1845, commit
`bfacb96`).

The emitter's tests (`schema-rust-next/tests/emission.rs:244-287`)
already assert these activation methods are emitted.

**Spirit-next has not pulled this in.** Spirit-next main `b5ced5cc`
("spirit-next: use generated engine trace hooks") pins schema-rust-next
at `8264f3d` (the prior emission, payload-bearing); the consumer code
in `engine.rs`/`nexus.rs`/`store.rs` overrides the payload-bearing
per-phase hooks.

So the **research conclusion**: name-only emission is already on
schema-rust-next main; the prototype is "what does spirit-next look
like after pulling `bfacb96` and adapting?"

### One activation hook per plane is even simpler than per-phase

The emitter's shape has an elegant additional simplification:
implementors override ONE method per plane
(`trace_signal_activation(&self, object_name: &'static str)`) and the
default-implementation per-phase methods (`trace_signal_admitted`,
`trace_signal_triaged`, ...) call into it with the activation name as
literal `&'static str`. Per-phase override is still possible (compose
the activation hook AND a per-phase override) but no longer required.

This is cleaner than the unit-variant-enum proposal from the
orchestrating designer: one override point per plane (3 total) instead
of N override points per plane (8 total).

### Edge cases scanned

**Concurrent traces across requests.** Within one `Engine` instance,
`handle()` is sequential (Nexus is held under `Mutex<Nexus>` during
SEMA invocation). Tests use one engine per test. ACROSS engine
instances there's no shared trace surface to correlate against. So
`OriginRoute` is NOT needed in the activation hook for the current
testing pattern. If a future need surfaces (multi-engine cross-process
correlation), the activation hook can grow a second arg with a typed
parameter — additive change, not a redesign.

**Failure-path detail for `SignalRejected`.** The current
payload-bearing event carries `validation_error: ValidationError`. In
the name-only shape, the test that asserts the rejection path uses two
witnesses: (a) the trace event name sequence
(`[SignalRejected, SignalReplied]` proves the Nexus + SEMA path was NOT
crossed, which is the architectural claim); (b) the
`output.root() == Output::Rejected(...)` assertion on the engine's
return value carries the full validation error detail. The witness
remains complete — different surfaces split the work.

**Variant-of-variant matching, e.g. `SemaWriteApplied = Recorded |
Missed`.** Today's payload-bearing event lets a test directly assert
`output: SemaWriteOutput::Recorded(...)`. Under name-only, the test
asserts the SAME via the engine's return value
(`Output::RecordAccepted(receipt)`) plus the trace's
`SemaWriteApplied` activation proves the SEMA write engine ran. The
two combined are equivalent in witness strength. The test rewritten in
the prototype demonstrates this (lines 44-83 of the new
`instrumentation_logging.rs`).

## Prototype shape

### Worktree

`~/wt/github.com/LiGoldragon/spirit-next/designer-name-only-trace-2026-06-02`,
base commit `b5ced5cc` (spirit-next main HEAD), branch
`designer-name-only-trace-2026-06-02` pushed to
`origin/designer-name-only-trace-2026-06-02` at commit `c83e1244`.

### Diff summary

```
Cargo.lock                       |   2 +-
flake.lock                       |   6 +-
src/engine.rs                    |  44 +-------
src/lib.rs                       |   3 +-
src/nexus.rs                     |  15 +-
src/schema/lib.rs                |  50 +++++----
src/store.rs                     |  25 +---
src/trace.rs                     | 219 +++++------------------------------------
tests/instrumentation_logging.rs | 203 +++++++-------------------------------
9 files changed, 105 insertions(+), 462 deletions(-)
```

### Schema-rust-next pin update

`flake.lock` and `Cargo.lock` repin schema-rust-next at `bfacb96` (was
`8264f3d`). `src/schema/lib.rs` regenerates via
`SPIRIT_NEXT_UPDATE_SCHEMA_ARTIFACTS=1 cargo build` and now carries the
name-only emission shape.

### `src/trace.rs` shrinks from 407 to ~180 lines

Old shape: an 8-variant `TraceEvent` enum where each variant carries
`origin_route` plus the typed payload(s) for that phase
(`SignalAdmitted { origin_route, input }`,
`SemaWriteApplied { origin_route, input, output }`, etc) + 152-line
`Display` impl pattern-matching every variant + `actor()` / `interface()`
classification methods reaching into each payload.

New shape:

```rust
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct TraceObjectName(pub String);

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct TraceEvent {
    object_name: TraceObjectName,
}

impl TraceEvent {
    pub fn new(object_name: impl Into<String>) -> Self {
        Self { object_name: TraceObjectName::new(object_name) }
    }

    pub fn name(&self) -> &str {
        self.object_name.as_str()
    }
}
```

Plus the unchanged `TraceLog`, `TraceSocketPath`, `TraceSocketListener`,
`TraceError` carriers.

### `src/engine.rs` SignalEngine impl collapses

The old impl overrode four trace hooks
(`trace_signal_admitted`, `trace_signal_rejected`,
`trace_signal_triaged`, `trace_signal_replied`), each pattern-matching
its payload to construct a typed `TraceEvent::SignalXxx { ... }`. The
new impl overrides one:

```rust
impl SignalEngine for SignalActor {
    #[cfg(feature = "testing-trace")]
    fn trace_signal_activation(&self, object_name: &'static str) {
        self.trace_log.record(TraceEvent::new(object_name));
    }

    fn triage_inner(&self, input: signal_plane::Signal<Input>) -> nexus_plane::Nexus<NexusInput> {
        let origin_route = input.origin_route();
        NexusInput::from(input.into_root()).with_origin_route(origin_route)
    }

    fn reply_inner(&self, output: nexus_plane::Nexus<NexusOutput>) -> signal_plane::Signal<Output> {
        output.into_signal_output()
    }
}
```

`Engine::handle()` calls the now-arg-less per-phase hooks on the
rejection path:

```rust
#[cfg(feature = "testing-trace")]
self.signal_actor.trace_signal_rejected();
#[cfg(feature = "testing-trace")]
self.signal_actor.trace_signal_replied();
```

`SignalActor::admit()` calls:

```rust
#[cfg(feature = "testing-trace")]
self.trace_signal_admitted();
```

Same collapse in `nexus.rs` (`trace_nexus_activation` only) and
`store.rs` (`trace_sema_activation` only). Methods stay on
data-bearing types (`SignalActor`, `Nexus`, `Store`) — no free
functions, no ZST namespacing.

### Layer 2 witness test rewrites

`tests/instrumentation_logging.rs` shrinks from 273 to ~135 lines. The
three tests now assert on activation-name sequences (the typed
witness of architectural crossing) plus the engine's return value
(the typed witness of correct payload).

The full record-then-observe witness:

```rust
assert_activation_names(
    &trace_log.events(),
    &[
        "SignalAdmitted", "SignalTriaged", "NexusEntered",
        "SemaWriteApplied", "NexusDecided", "SignalReplied",
        "SignalAdmitted", "SignalTriaged", "NexusEntered",
        "SemaReadObserved", "NexusDecided", "SignalReplied",
    ],
);
```

The rejection-path witness:

```rust
assert_activation_names(&trace_log.events(), &["SignalRejected", "SignalReplied"]);
```

The default-engine witness:

```rust
assert_activation_names(
    &engine.trace_events(),
    &[
        "SignalAdmitted", "SignalTriaged", "NexusEntered",
        "SemaWriteApplied", "NexusDecided", "SignalReplied",
    ],
);
```

All three pass.

## Witness test results

```
running 3 tests
test testing_trace_records_signal_rejection_without_nexus_or_sema_activations ... ok
test testing_trace_builds_record_activations_by_default ... ok
test testing_trace_records_real_signal_nexus_and_sema_activations ... ok

test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.15s
```

Full crate test sweep with `--features testing-trace`:
all 39 tests pass (3 instrumentation + 5 process_boundary + 6 generated_signal_plane + 16 runtime_triad + 3 socket_negative + 2 operator_271_closed_claims + 3 dependency_surface + 1 doc-test). `cargo clippy
--features testing-trace --all-targets -- -D warnings` clean.
Production build (no `testing-trace`): all 36 tests pass + clippy
clean.

### Ergonomic findings

**Implementing a custom trace destination is simpler.** Under the old
shape, an external trace consumer had to know the eight typed payload
shapes to handle each event variant. Under the new shape, the consumer
sees a `&str` name — no payload-type knowledge required. The trace
contract becomes a string-vocabulary contract, narrower and more
stable.

**Per-phase override is still possible if needed.** The generated
default `trace_signal_admitted(&self) { self.trace_signal_activation("SignalAdmitted"); }`
is overridable. An implementor that wanted (e.g.) finer-grained
control over the `SignalAdmitted` event specifically could still
override the per-phase method while leaving the central activation hook
for everything else. The pattern composes.

**Test rewriting is mechanical.** The 12-event sequence assertion
turns into a 12-name-string array. Edge cases like rejection-path and
read-vs-write are still witnessed cleanly. The old test's payload
pattern-matching mostly verified what the SEMA write or read returned,
which is BETTER tested via the engine's return value
(`Output::RecordAccepted(receipt)`) than via the trace payload's
shadow copy. The split sharpens the test surface.

## Recommendation: ratify the simplified shape

The prototype demonstrates:
- The simplification works end-to-end.
- The Layer 2 witness strength is preserved (still proves
  architectural crossing of Signal admission, Signal engine, Nexus
  engine, SEMA engine).
- The diff is 357 lines of net reduction.
- Production builds + testing-trace builds + clippy all pass.

The shape that lands on main:

1. Spirit-next pulls schema-rust-next `bfacb96` (already on main of
   schema-rust-next; just the consumer-side pin).
2. Spirit-next's `src/trace.rs` becomes the simple
   `TraceEvent { object_name }` carrier; the typed-variant enum
   retires.
3. Spirit-next's `engine.rs`, `nexus.rs`, `store.rs` override one
   activation hook per plane.
4. Spirit-next's `tests/instrumentation_logging.rs` asserts on
   activation-name sequences.

Action item for operator: integrate the worktree branch
`designer-name-only-trace-2026-06-02` (commit `c83e1244`) onto
spirit-next main. Conflicts are unlikely — main hasn't moved since
`b5ced5cc` was the base.

## Open questions

### Closed `TraceObjectName` enum vs `TraceObjectName(String)` newtype

The prototype landed as `TraceObjectName(pub String)` — open-name
newtype. A closed-enum alternative
(`enum TraceObjectName { SignalAdmitted, ... }` with
`TryFrom<&'static str>`) was prototyped first and works too. Trade-offs:

- **Closed enum**: typed at the test surface (test asserts
  `event.object_name() == TraceObjectName::SignalAdmitted`), narrower
  vocabulary, compile-fail on typo at the macro side if the emitter
  ever emits an unknown name.
- **String newtype**: simpler, matches the schema-emitter convention
  more naturally (the emitter emits `&'static str` literals; no
  closed-enum mapping needed on the trace side), open to new
  activation names without recompiling the trace crate.

For the current testing surface either works. The harness-converged
shape that landed is the open-newtype version. **Open question for
psyche / operator**: which to keep on main?

### `OriginRoute` not threaded through activation hooks

The current activation signature is `trace_signal_activation(&self,
object_name: &'static str)`. No `OriginRoute`. The current testing
pattern doesn't need it (sequential per-engine handle). If a future
multi-engine cross-process correlation surface lands, adding a second
arg is additive — but adding it pre-emptively pays the complexity
without a clear use.

**Recommendation**: don't thread `OriginRoute` yet; add it when the
need surfaces.

### Per-phase hook keep-or-retire

The generated emitter currently emits BOTH the central
`trace_<plane>_activation(&self, _object_name: &'static str) {}` hook
AND the per-phase default methods (e.g. `trace_signal_admitted(&self)
{ self.trace_signal_activation("SignalAdmitted"); }`). The per-phase
methods enable per-phase override. If the only override path that ever
matters is the central activation hook, the per-phase methods are
emission noise. **Open question for psyche**: retire the per-phase
methods to leave only `trace_<plane>_activation` as the single
override point?

## Hand-off to operator

Operator branch ready:
`origin/designer-name-only-trace-2026-06-02` at commit `c83e1244`
("spirit-next: name-only trace prototype (designer 467)").

Integration steps:
1. Rebase or cherry-pick the branch onto current `spirit-next` main
   (no movement since `b5ced5cc`).
2. The Cargo.lock + flake.lock updates for schema-rust-next
   `bfacb96` are included.
3. `cargo test --features testing-trace` and the default test suite
   both pass on the branch.
4. The branch deletes `TraceActor`/`TraceInterface` from the public
   surface (along with the payload-bearing event variants). Any
   downstream consumer of `TraceActor::Signal` etc. would break — the
   broad-sweep is `grep -r TraceActor` in the workspace. Spot-check:
   no current spirit-next module outside the deleted code uses
   `TraceActor`/`TraceInterface`. The integration test
   `tests/instrumentation_logging.rs` was the only user; it's
   rewritten.

## Cross-references

- Spirit 1394 (Correction High, 2026-06-02) — name-only trace
  intent.
- Spirit 1361 (High) — engine method-count matches wire-events.
- Spirit 1365 (Correction Maximum, 2026-06-01) — trace as trait on
  schema-derived interfaces + actor traits; this prototype lives on
  the schema-derived interface side of the ratification.
- Spirit 1390 (Constraint Maximum) — testing trace must prove runtime
  use of the schema-defined triad interfaces. Preserved here: the
  activation-name sequence is the runtime witness.
- Spirit 1391 (Decision High) — testing-trace build installs default
  hooks. Preserved here: `Engine::new` calls `new_with_trace` under
  `cfg(feature = "testing-trace")`.
- Spirit 1392 (Correction Maximum) — trace built into the
  schema-emitted engine traits themselves. Preserved here: the
  activation hooks ARE on the emitted `SignalEngine`/`NexusEngine`/
  `SemaEngine` traits.
- Spirit 1394 (Correction High) — trace records only the name; no
  rich payload. This prototype manifests that intent.
- `reports/operator/281-generated-interface-logic-with-macros-2026-06-02.md`
  — operator's walkthrough of the current generated engine trait
  shape (the payload-bearing version that this prototype supersedes).
- `reports/designer/463-operator-trace-implementation-audit-and-intent-gaps-2026-06-01.md`
  — designer's audit naming the four implementation gaps; this report
  resolves Gap 2 (schema-emitted trace nouns) by making the nouns one
  name-only `TraceObjectName` carrier instead of an 8-variant typed
  enum.
- `reports/designer/466-triad-engine-honesty-situation-2026-06-01/3-overview.md`
  — designer situation synthesis; this report is the candidate-1
  prototype.
- `/git/github.com/LiGoldragon/spirit-next` worktree branch
  `designer-name-only-trace-2026-06-02` at commit `c83e1244`.
- `/git/github.com/LiGoldragon/schema-rust-next` main at `bfacb96`
  — already emits name-only hooks; no further work needed there.
- `skills/architectural-truth-tests.md` §"Proof-of-usage ladder" —
  the Layer 2 runtime witness discipline the prototype's tests honor.
