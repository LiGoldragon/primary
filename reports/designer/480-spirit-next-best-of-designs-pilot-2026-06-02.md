; designer
[spirit-next nexus-recursive-computation stash-effect slim-output continuation-budget designer-pilot vocabulary-rename schema-emitter-coupling pilot-deliverable]
[Designer pilot per Spirit 1469: NexusInput/NexusOutput extended with EffectCompleted/CommandEffect/Continue variants; Stash effect implemented end-to-end; Observe slim-output path proved via Stash recursion; ContinuationBudget bounds the runner loop; layer-2 witness demonstrates Observe -> Stash -> slim handle -> LookupStash -> full records over both in-process Engine and the live daemon process boundary. Branch designer-best-of-designs-2026-06-02 on spirit-next, 47 tests pass under --all-features. Reports what landed, what schema-rust-next emitter constraint deferred (the schema-level NexusWork/NexusAction rename), and the ergonomic findings on the recursive-Nexus vocabulary in practice.]
2026-06-02
designer

# 480 — spirit-next best-of-designs pilot

## TL;DR

Spirit-next now pilots the **recursive-Nexus computation pattern** with
the **Stash effect** as the first working effect. A Layer-2 witness test
proves: Observe with a non-empty result drives the runner loop through
SemaRead -> CommandEffect(Stash) -> EffectCompleted(Stashed) ->
ReplyToSignal(RecordsStashed). The slim wire reply carries a handle +
count + marker; a follow-up `LookupStash(handle)` returns the full
records.

Branch: `designer-best-of-designs-2026-06-02` on
`/git/github.com/LiGoldragon/spirit-next`, pushed to origin.
HEAD `ba24b011` over main `8fe12acb`. 47 tests pass under
`cargo test --all-features`; clippy + fmt clean.

**Headline deferral**: the schema-level rename from `NexusInput` /
`NexusOutput` to `NexusWork` / `NexusAction` is **not** in this pilot.
The schema-rust-next emitter (`a8c0f01`) hard-codes the names
`NexusInput`/`NexusOutput` and the variant names `Signal`/`SemaWrite`/
`SemaRead` when emitting the engine traits, plane modules, projection
helpers, and the `NexusObjectName` trace surface. Renaming at the
schema layer is a schema-rust-next emitter change first, a spirit-next
schema change second. This pilot **exposes the vocabulary at the Rust
layer** via type aliases (`pub type NexusWork = NexusInput;
pub type NexusAction = NexusOutput;`) so call sites can adopt the new
names today; the schema-level rename is named as a follow-on slice in
§"Deferred".

## What landed

### Schema additions (`schema/lib.schema`)

The schema source kept the names `NexusInput` and `NexusOutput` (to
preserve schema-rust-next emission) but the **shape changed**:

```nota
NexusInput  [(Signal Input) (SemaWrite SemaWriteOutput)
             (SemaRead SemaReadOutput) (EffectCompleted NexusEffectResult)]
NexusOutput [(SemaWrite SemaWriteInput) (SemaRead SemaReadInput)
             (Signal Output) (CommandEffect NexusEffectCommand)
             (Continue NexusInput)]
NexusEffectCommand [(Stash StashRequest)]
NexusEffectResult  [(Stashed StashResult)]
StashHandle  Integer
StashRequest        { Records * DatabaseMarker * }
StashResult         { StashHandle * RecordCount * DatabaseMarker * }
StashedObservation  { StashHandle * RecordCount * DatabaseMarker * }
Records (Vec Entry)
```

`Input` grew `(LookupStash StashHandle)`. `Output` grew
`(RecordsStashed StashedObservation)`. `ValidationError` grew
`StashHandleNotFound` for the missing-handle path.

### Runner loop (`src/nexus.rs`)

Nexus now carries a `StashTable` alongside the SEMA store and mail
ledger. `NexusEngine::decide` is the **runner loop** rather than a
single-step projection: it consumes a `NexusInput`, calls
`step_decide` for the decision, then steps a `NexusOutput` against
the runtime, re-entering with the appropriate completion fact:

| NexusOutput variant     | Runtime action                                  | Re-enter as                     |
|---|---|---|
| `Signal(reply)`         | exit the loop, return the reply                 | (terminal)                      |
| `SemaWrite(command)`    | `SemaEngine::apply(&mut store, command)`        | `NexusInput::SemaWrite(reply)`  |
| `SemaRead(command)`     | `SemaEngine::observe(&store, command)`          | `NexusInput::SemaRead(reply)`   |
| `CommandEffect(command)`| `Nexus::apply_effect(command)`                  | `NexusInput::EffectCompleted`   |
| `Continue(work)`        | (no runtime action — direct continuation)       | the inner `NexusInput`          |

`ContinuationBudget` (default 32 iterations) bounds the loop. Running
out returns `Output::Error("nexus continuation budget exhausted")`
with the current database marker.

The Observe slim-output path lives in `step_decide`:

```rust
SemaReadOutput::Observed(observed) => {
    // Spirit 1389: slim reply, not full record set.
    NexusOutput::from(NexusEffectCommand::Stash(StashRequest {
        records: Records(observed.record_set.0),
        database_marker: observed.database_marker,
    }))
}
```

`apply_effect` mints a fresh handle, archives the records, and emits
`NexusEffectResult::Stashed(...)`. `decide_effect_completion` then
emits `Output::RecordsStashed(StashedObservation { handle, count,
marker })`.

### Layer-2 witness test

`tests/runtime_triad.rs::full_runtime_triad_records_then_observes_through_durable_sema_with_stash`
is the witness for operator 287 §"Acceptance Tests":

```rust
let observed = engine.handle(Input::Observe(query));
let stash_handle = match observed.root() {
    Output::RecordsStashed(stashed) => {
        assert_eq!(stashed.record_count, RecordCount(1));
        assert_eq!(stashed.database_marker, record_marker);
        stashed.stash_handle.clone()
    }
    other => panic!("expected slim RecordsStashed reply, got {other:?}"),
};

let looked_up = engine.handle(Input::LookupStash(stash_handle));
match looked_up.root() {
    Output::RecordsObserved(records) => {
        assert_eq!(records.record_set, RecordSet(vec![entry("full runtime triad works")]));
    }
    other => panic!("expected full records from LookupStash, got {other:?}"),
}
```

The process-boundary daemon test
(`tests/process_boundary.rs::daemon_persists_sema_file_across_a_restart`)
proves the same flow **across a daemon restart** with the live
`spirit-next-daemon` binary on a real unix socket — the stash is
re-minted on the new daemon instance, the durable records survive,
and the LookupStash returns them through the typed wire codec.

### Vocabulary aliases

`pub type NexusWork = crate::NexusInput;`
`pub type NexusAction = NexusOutput;`

Re-exported through `lib.rs`. Call sites can write the new vocabulary
at the Rust layer today; the schema-level rename ships when
schema-rust-next supports it.

## What's deferred

### Schema-level NexusWork / NexusAction rename

**Why deferred**: the schema-rust-next emitter is tightly coupled to
the type names `NexusInput`/`NexusOutput` and to the variant names
`Signal`, `SemaWrite`, `SemaRead`. Specifically (verified against
`schema-rust-next` at commit `a8c0f01`):

- `emit_split_nexus_input_projection` at lines 1844-1925 hard-codes
  `NexusInput::Signal`, `NexusInput::SemaWrite`, `NexusInput::SemaRead`
  in the emitted match arms.
- `emit_nexus_output_projection` at lines 1927-1974 hard-codes
  `NexusOutput::Signal`, `NexusOutput::SemaWrite`, `NexusOutput::SemaRead`.
- `NexusObjectName` emission references these names at lines 1282-1294.
- The `pub mod nexus { pub type Input = ... }` aliases at lines
  1718-1724 reference `NexusInput`/`NexusOutput` by name.

Renaming at the schema layer requires schema-rust-next to accept the
new names (either by recognising both old and new names during
migration, or by parameterising emission on the schema's variant
names). That's a parallel pilot in schema-rust-next, ideally landing
**before** the schema-level rename in spirit-next.

### Continue variant — not yet exercised

`NexusOutput::Continue(NexusInput)` is wired through the runner loop
but the pilot's hand-written `step_decide` never emits it. Continue
becomes useful when a SEMA read completion needs to schedule new
internal work without going back through SEMA — e.g. fan-out, retry,
or composed reads. The recursion shape is proven (the loop handles
Continue and re-enters); the use case for emitting it is a follow-on.

### Schema-rust-next emitting the runner loop

The runner loop currently lives in `src/nexus.rs` as hand-written
code. Operator 287 §"Generated Runner" calls for the codegen to emit
it. Today's pilot proves the SHAPE; emission is a follow-on slice in
schema-rust-next paired with the NexusWork/NexusAction rename.

### Inline enum payload pattern (Spirit 1467/1468)

Not piloted in this slice. The `Output` enum has 8 variants today
(`RecordAccepted`, `RecordsObserved`, `RecordsStashed`, `RecordFound`,
`RecordsCounted`, `RecordRemoved`, `Error`, `Rejected`). Spirit
1467/1468 would let small inline-only enums live as bracket lists at
their consumer position; the pilot here doesn't use that idiom because
no inline-only enum showed up under pressure. The pattern is a
candidate when a future variant pushes a one-position-only enum.

## Ergonomic findings — the recursive Nexus vocabulary in practice

### NexusWork / NexusAction feels right when you write the runner

Implementing `Nexus::decide` as a runner loop, the names
NexusInput/NexusOutput felt **wrong**: a SignalArrived "input" and a
SemaWriteCompleted "input" are different kinds of input semantically
(one is a fresh client request, the other is a delayed completion),
and the runner reads more naturally as "consume work, emit action."
The aliases `NexusWork = NexusInput; NexusAction = NexusOutput;` in
the runtime code read better at the call site even when the schema
type name is still `NexusInput`.

The mid-conversion friction is real: `NexusInput::Signal(...)` reads
as "the signal is an input" rather than "the signal arrival is a
work fact." Spirit 1438 was correct to call this asymmetry out.

### ContinuationBudget feels minimal but right

A single `u32` counter is plenty for the pilot. The default of 32
iterations carries 10x headroom over the longest current path
(Observe = 3 iterations). When a future flow approaches the budget
(e.g. fan-out into N sub-reads), the budget tunes per-component.

### Stash as the first effect — the right starting point

Stash is the smallest possible effect: it has clear input
(records + marker), clear output (handle + count + marker), and no
external dependencies. Putting Stash inline (not in an external
service) made the test cycle short. Once the recursion pattern is
proven on Stash, Fanout / Drop / Cascade / Preempt are mechanical
additions.

### The slim Observe output via Stash works at the wire layer

The process-boundary test (live daemon, unix socket, rkyv frames)
proves the slim shape carries through. The wire reply on Observe
went from `RecordsObserved { record_set: Vec<Entry>, marker }` (an
unbounded-size payload) to `RecordsStashed { handle, count, marker }`
(a constant-size payload). Spirit 1389 is realised on a real flow.

### Mail ledger still works without recursion awareness

The mail ledger fires `Sent` at Signal->Nexus handoff and `Processed`
at the wire reply. Inside the runner loop, multiple SEMA + effect
operations all happen under the same `Sent`/`Processed` pair. From
the ledger's view, one Signal-route is one mail; the recursion is
internal to one "being processed" episode.

The trace surface (`testing-trace` feature) shows the same — one
`NexusEntered` / `NexusDecided` pair per route, regardless of how
many internal SEMA + effect steps ran. That matches operator 287's
trace acceptance criterion ("Nexus entered more than once for one
original Signal route") *only if* you read "more than once" as "the
decide step runs multiple times within one NexusEntered/NexusDecided
pair." If the criterion requires emitting one `NexusEntered`
activation per inner iteration, that's a trace-emission change in
the runner loop — a small follow-on, not blocking the pilot.

## File map

| File | Change |
|---|---|
| `schema/lib.schema` | extended NexusInput/NexusOutput variants; added Stash types; added LookupStash + RecordsStashed |
| `schema/lib.asschema` | regenerated from `lib.schema` via build script |
| `src/schema/lib.rs` | regenerated by schema-rust-next emitter (1876 lines) |
| `src/nexus.rs` | Nexus carries StashTable; NexusEngine::decide is now the runner loop; ContinuationBudget + StashTable types added |
| `src/engine.rs` | match exhaustiveness updated for new variants |
| `src/lib.rs` | exports extended for new schema types + ContinuationBudget + StashTable + NexusWork/NexusAction aliases |
| `tests/runtime_triad.rs` | layer-2 witness test added; projection-only tests adapted to runner-loop shape |
| `tests/process_boundary.rs` | stashed_descriptions helper threads LookupStash; restart witness adapted |
| `tests/instrumentation_logging.rs` | Observe trace expectation adapted |
| `tests/operator_271_closed_claims.rs` | substring-witness updated for new Input + ValidationError shape |

## Recommendations to operator

The branch is ready for operator pickup per the designer-operator loop
discipline. Suggested integration sequence:

1. **Audit the runner loop shape** in `src/nexus.rs::Nexus::decide`
   against operator 287 §"Generated Runner". The hand-written version
   here is the executable spec; operator's call on emission timing.
2. **Decide on schema-rust-next NexusWork/NexusAction support** as a
   parallel pilot. Once that lands, spirit-next's schema layer renames
   trivially.
3. **Wire the Continue variant exerciser** — pick one real flow that
   benefits from immediate self-continuation (introspect's IngestTraceEvent
   per designer 469 §"IngestTraceEvent decision" is a likely candidate
   when introspect lands).
4. **Decide on per-iteration `NexusEntered` trace emission** vs. the
   current per-route emission. Operator 287's acceptance test reading
   matters for the choice.

The integration onto main is operator's lane per intent record 515.
The branch demonstrates the design's working-code form; operator
chooses its main-rebase path.
