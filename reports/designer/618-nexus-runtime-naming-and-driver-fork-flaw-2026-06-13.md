# Nexus runtime: the re-authored universal frame (plus naming and the spirit driver fork)

Investigation of the flaw seeded in chat — `NexusWork` / `NexusAction` /
`NexusEffectCommand` / `NexusEffectResult` are "very generic and, if rewritten
for every component, something has been badly designed." Method: a six-finder
+ adversarial-verify workflow across the 14 nexus.schema components, then
**direct source re-verification of every load-bearing claim** because two
verifier agents were unreliable (one lost the workspace; one waved off the
naming flaw with "it's emitted, so naming rules don't apply" — wrong, the
prefix is in the *authored* schema source). Everything below is confirmed from
the code, not from the workflow's say-so.

The central finding is the one the psyche named first and the workflow buried:
the universal Nexus **reaction frame** is hand-re-authored in every component's
schema. The naming prefix and the spirit driver fork are real but secondary.

## The three real flaws

### 1. The universal reaction frame is hand-re-authored in all 14 schemas (the central flaw)

`spirit/schema/nexus.schema:46-67` declares, by hand, the workspace-canonical
Nexus reaction frame:

```
NexusWork   [(SignalArrived) (SemaWriteCompleted) (SemaReadCompleted) (EffectCompleted)]
NexusAction [(CommandSemaWrite) (CommandSemaRead) (ReplyToSignal) (CommandEffect) (Continue)]

  SignalArrived      SignalInput          ;; wraps THIS component's signal Input
  SemaWriteCompleted SemaWriteOutput
  SemaReadCompleted  SemaReadOutput
  EffectCompleted    NexusEffectResult
  CommandSemaRead    SemaReadInput
  ReplyToSignal      SignalOutput
  CommandEffect      NexusEffectCommand   ;; wraps THIS component's effect vocabulary
  Continue           NexusWork            ;; recurses into Work
```

`component-triad.md` is explicit that "the `NexusWork`/`NexusAction`
asymmetric pair plus a five-variant action set is the **workspace-canonical**
engine mechanism." It is canonical — yet all 14 nexus-plane daemons re-declare
the whole thing: the variant set, the wrapping relationships, and the
recursion (`Continue` → `Work`). Confirmed identical (modulo subset selection)
across spirit, mirror, router, agent, mind, and the other nine.

This is a **generic frame written out longhand 14 times.** The frame is
`Work<Input, WriteOutput, ReadOutput, EffectResult>` and
`Action<SemaWriteCommand, ReadInput, Output, EffectCommand, Work>`; the only
genuinely per-component content is the *payloads bound into it* — this
component's `Input`/`Output`, its `NexusEffectCommand`/`EffectResult`
vocabulary, and its sema-write ops (`Record`/`Remove`/… at line 54). Each
schema **already imports its concrete types** at the top (`SignalInput
spirit:signal:Input`, lines 2-44) — the frame should be imported the same way
(a shared `triad:nexus` schema defining `Work`/`Action` once, the component
binding its payload types), not re-typed. Add a sixth action variant and all
14 schemas need a hand-edit, by definition out of sync until each is touched.

Recorded intent already condemns this. Per the intent census: [the three
planes are one primitive projected three ways (Signal / Nexus / SEMA),
differing only by ownership and runtime semantics, **never by authored
shape**]. Re-authoring the frame per component *is* differing by authored
shape. And the runtime layer already proves the frame is genericizable —
the asymmetry between the runtime and the schema is the whole tell.

#### Rust evidence — the generic already exists; the schema can't reach it

`triad-runtime/src/runner.rs:26` defines the canonical action frame **once,
fully generic**:

```rust
pub enum NextStep<Reply, SemaWrite, SemaRead, Effect, Work> {
    Reply(Reply), SemaWrite(SemaWrite), SemaRead(SemaRead), RunEffect(Effect), Continue(Work),
}
pub trait RunnerEngines {
    type Reply; type SemaWrite: SemaWriteInput; type SemaRead: SemaReadInput;
    type Effect: NexusEffectCommand; type Work: NexusWork;
    fn decide_next_step(&mut self, work: Self::Work) -> RunnerNextStep<Self>;
}
```

That `NextStep<…>` IS the `Action<…>` frame — five type parameters, one
declaration. Rust expresses it trivially. But the schema cannot reference it,
so `schema-rust-next` emits, per component, a **concrete twin**: `pub enum
NexusAction { CommandSemaWrite(..) CommandSemaRead(..) ReplyToSignal(..)
CommandEffect(..) Continue(..) }` — byte-identical between
`spirit/src/schema/nexus.rs:198` and `router/src/schema/nexus.rs:95`. Then,
because the twin and the real `NextStep` are different Rust types, the emitter
also writes a **bridge** (`schema-rust-next/src/lib.rs:2055-2074`):

```rust
pub type NexusRunnerNextStep =
    triad_runtime::NextStep<Output, CommandSemaWrite, CommandSemaRead, CommandEffect, NexusWork>;
fn into_next_step(self) -> NexusRunnerNextStep {
    match self {
        Self::CommandSemaWrite(input) => triad_runtime::NextStep::SemaWrite(input),
        Self::CommandEffect(effect)   => triad_runtime::NextStep::RunEffect(effect),
        Self::ReplyToSignal(output)   => triad_runtime::NextStep::Reply(output),
        Self::Continue(work)          => triad_runtime::NextStep::Continue(work),
        // ...
    }
}
```

The emitter **writes down the correct answer** — the `type NexusRunnerNextStep
= NextStep<Output, …>` alias, the generic instantiated with this component's
types — *and then also* emits the redundant standalone `NexusAction` enum
*and* a variant-by-variant shim to translate between them. The same five-way
choice now exists three times: the generic `NextStep` (once, shared), the
concrete `NexusAction` (14×, emitted), and spirit's hand-written
`execute_to_reply` match (a third re-statement). The variant names even drift
across the boundary (`CommandEffect`↔`RunEffect`, `ReplyToSignal`↔`Reply`),
which is the only reason a translation is needed.

The fix, in Rust terms, is one line the emitter *already knows how to write*:
emit `pub type Action = triad_runtime::NextStep<Output, SemaWriteCommand,
ReadInput, EffectCommand, Work>;` and delete the standalone enum and the
`into_next_step` shim. The single thing stopping that is the schema source's
inability to say "instantiate this parameterized type with my bound types" —
so the emitter manufactures a concrete enum plus glue instead of an alias.

**This is a schema-stack capability gap, not per-component cleanup.** For the
frame to live once and be imported-and-bound, schema must express a
parameterized/generic type (a frame over type parameters), then bind it per
component. If `schema-next` cannot express that yet, that missing capability
is the design fault the psyche named — the schema language forces the
hand-copy. The fix is: define the canonical `Work`/`Action` frame once in a
shared nexus schema, give schema-next the means to import-and-bind it, and
delete the 14 hand-authored copies.

### 2. `Nexus*` namespace prefix in 12 components' authored schema (systemic)

`NexusWork`, `NexusAction`, `NexusEffectCommand`, `NexusEffectResult`,
`NexusObjectName` are declared **in the hand-authored `schema/nexus.schema`
source** of all 12 nexus-plane daemons (cloud, terminal, system, agent,
spirit, router, orchestrate, mirror, mind, message, lojix, harness).
Confirmed at `spirit/schema/nexus.schema:66-67`:

```
NexusWork   [(SignalArrived) (SemaWriteCompleted) (SemaReadCompleted) (EffectCompleted)]
NexusAction [(CommandSemaWrite) (CommandSemaRead) (ReplyToSignal) (CommandEffect) (Continue)]
```

These types are reached as `nexus::Work` / `nexus::Action` — the `Nexus`
prefix names a namespace already visible at the use site, which is exactly
the C-CRATE-PREFIX violation (`skills/naming.md`, `skills/rust-discipline.md`
§"No crate-name prefix"). Correct shape: `Work`, `Action`, `EffectCommand`,
`EffectResult`, `ObjectName`. This is a schema-source edit + regenerate, not
an emitter change — and breaking all consumers at once is fine pre-production.

**The sema plane already did this right, and proves the point.** Sema schema
types are named *unprefixed* at source (`ReadInput`, `WriteInput`,
`ReadOutput`, `WriteOutput`) — and then `spirit/src/nexus.rs:15-17`
*re-adds* the prefix by hand on import:

```rust
sema::{ ReadInput as SemaReadInput, WriteInput as SemaWriteInput, ... }
```

So the natural name is the unprefixed one (the sema author chose it; the
daemon re-breaks it on import). The flaw is asymmetric: **nexus got the
prefix wrong at source; sema got it right and the daemon re-aliases it
back.** Fix is two-sided — drop the prefix in `nexus.schema`, and delete the
`Sema*` re-aliasing imports so the daemon uses `sema::ReadInput` directly.

### 3. The spirit driver fork (single component, transitional)

The original worry — "if the reducer shell is rewritten for every component,
something is badly designed" — does **not** hold for the driver. The
canonical driver loop is *shared*: `triad-runtime/src/runner.rs:157`
defines a generic `drive<Engines>` whose body is `match
engines.decide_next_step(work)`, and both the emitted daemon path
(`schema-rust-next/src/lib.rs:2500`, `runner.drive(...)`) and
`repository-ledger/src/lib.rs:878` call it. The shell is shared, as designed.

**Spirit is the one component that forked it.** `spirit/src/nexus.rs:974`
hand-writes its own `execute_to_reply` — the recursive loop that dispatches
the fixed five-variant `NexusAction` set, spends the continuation budget, and
feeds each result back as the next `Work`. The code comment at line 1041-1043
states the reason plainly:

> *"Spirit drives the recursive runner loop in `Nexus::execute_to_reply`
> because the no-alias schema shape no longer emits the old multi-hook runner
> trait."*

So the canonical loop *used to be emitted*, spirit adopted a newer "no-alias
schema shape" ahead of the shared runner supporting it, and the loop is now
hand-maintained in spirit until the runner/emitter catches up. Genuinely a
flaw (the canonical driver should not live by hand in a daemon), but scoped to
one component and already understood as transitional — **not** systemic
duplication. The only legitimately per-component piece is `step_decide`
(Work→Action); the loop around it is generic boilerplate that belongs in
`triad-runtime::runner::drive` once it speaks the no-alias shape.

## What looked like a flaw but is not (do not "fix")

| Suspected | Verdict | Why |
|---|---|---|
| A component owning its own `nexus.schema` | Intended | The three-plane split: every daemon authors signal/nexus/sema schemas. The file stays per-component — flaw 1 is only that it should *import* the frame and declare *payloads*, not re-author the frame. |
| `GuardianOperation` / `GuardianDecision` not in schema (`spirit/src/guardian_journal.rs`) | **Not a flaw** — my seed example was wrong | A `pub(crate)` audit-journal record format, documented as "hand-written audit state, not a schema-declared wire family." The engine ops it records (Record/Propose/Clarify/Supersede/Retire) *are* declared in `NexusEffectCommand`. The journal records decisions; it defines no engine verbs. |
| Daemon `src/schema/signal.rs` "re-emits" wire types (tb9h) | Not a flaw | Each daemon's `signal.rs` is generated from its *own* `schema/signal.schema` (its Input/Output contract), a different vocabulary from `signal-<component>` (e.g. spirit's `RecordIdentifier(String)` vs signal-spirit's `[u8;12]`). No fork. |
| `Command*` prefix on the five `NexusAction` variants | Not a flaw | The fixed canonical action set; `Command-` distinguishes the command variants from the structural ones (`ReplyToSignal`, `Continue`). |

## Lower-confidence, worth a look (not verified to flaw)

Hand-written trace types — `spirit/src/trace_event.rs:30` `TraceEvent(ObjectName)`
and `mind/src/actors/trace.rs:68` `TraceAction`. `skills/component-triad.md`
§"Instrumentation belongs to the engine-trait contract" wants trace as
default-no-op hooks on the engine traits, not a side type. But `TraceEvent`
here wraps the schema-emitted `ObjectName`, so it may already be closer to
the typed-`TraceObject` shape the skill endorses than to the forbidden
hand-rolled string enum. I did not read `trace_event.rs` end-to-end; flagging,
not asserting.

## Governing intent

Settled and already remediated (intent census, verified to exist):

- Per Spirit `4np2` (Principle): [schema-to-Rust lowering uses quote! /
  proc-macro2 / ToTokens, not a hand-rolled string code generator] — fixed
  2026-06-06 (schema-rust-next commit `33337d74`, the token-emission rewrite).
- Per Spirit `de8i` (Principle): [lowering verbs belong to the schema-model
  nouns themselves, not an external emitter god-struct] — fixed by the same
  refactor (11 `*Tokens` data-bearing nouns with `ToTokens`).

Unsettled (needs a psyche decision):

- **No Spirit record bans the `Nexus*` / `Sema*` runtime-type prefix.**
  `skills/naming.md` governs it in general, but whether the *canonical schema
  source* names must drop the prefix is unrecorded. The psyche floated the
  rename; it is not yet captured as intent. (Open question 1.)
- The hand-authored-vs-emitted **boundary for the driver loop** is not
  formalized — specifically that `execute_to_reply` belongs in
  `triad-runtime`, not in a daemon.

## Fix shape and sequencing

Schema-stack capability (the central fix, heaviest):

1. Define the canonical `Work` / `Action` reaction frame **once** in a shared
   nexus schema; give `schema-next` the means to import-and-bind it (a
   parameterized/generic frame over the component's `Input` / `Output` /
   `EffectCommand` / `EffectResult` / sema-write ops); delete the 14
   hand-authored frame copies, leaving each `nexus.schema` declaring only its
   per-component payloads. This closes flaw 1 and is the real answer to "if
   they're rewritten for every component, something is badly designed."
   Prerequisite check: confirm schema-next can express a parameterized type;
   if not, that capability is the first deliverable.

One-shot (schema-source edit + regenerate; no emitter change):

2. Drop the `Nexus*` prefix in every component's `nexus.schema`
   (`Work`/`Action`/`EffectCommand`/`EffectResult`/`ObjectName`); regenerate
   `src/schema/nexus.rs`; delete the `Sema*` re-aliasing imports in
   `spirit/src/nexus.rs` so the daemon uses `sema::ReadInput` directly.
   Mechanical, breaks all consumers at once (allowed). If item 1 lands first,
   the unprefixed names get authored once in the shared frame and this folds
   into it; if the rename ships first, it is a standalone slice.

Runner change (re-absorb the one fork):

3. Teach `triad-runtime::runner::drive` (or schema-rust-next's runner adapter)
   the no-alias schema shape, then delete spirit's hand-written
   `execute_to_reply` and route spirit through the shared driver. The shell is
   already shared for every component except spirit; this re-absorbs the fork.

Bead routing: **none of these belong to bead `primary-tqe3` (the guardian
retrieval fix)** — the guardian work does not intersect the frame, naming, or
driver roots (the `guardian_journal` "violations" were verified false). Item 1
is a schema-stack bead (schema-next + a shared nexus frame schema); item 2 is
a rename slice that may fold into item 1; item 3 is a separate runner bead.

## Open questions for the psyche

1. **The frame fix needs a schema-next capability — confirm the approach?**
   Lifting the universal `Work`/`Action` frame to one shared schema requires
   schema-next to express a parameterized type the component binds. Is that
   capability already present, planned, or net-new? The answer sets whether
   this is a near-term slice or a schema-stack arc.
2. **Capture the no-re-authored-frame and prefix-drop as intent?** The
   "differ never by authored shape" principle exists, but no record names the
   Nexus frame as the thing being wrongly re-authored, and none binds the
   no-ancestry-prefix rule to schema-source type names. Record these?
3. **Sequencing:** frame-lift first (and fold the rename into it), or ship the
   mechanical rename now and lift the frame later? The driver re-absorption
   (item 3) is independent of both.
4. **Trace types** — leave `TraceEvent` / `TraceAction` as-is, or fold into
   the engine-trait hook shape? (I'd read `trace_event.rs` first.)
