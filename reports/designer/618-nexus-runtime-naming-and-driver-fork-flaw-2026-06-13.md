# Nexus runtime: the `Nexus*` naming flaw and the spirit driver fork

Investigation of the flaw seeded in chat — `NexusWork` / `NexusAction` /
`NexusEffectCommand` / `NexusEffectResult` carry a module-name prefix — and
the broader "same-style" question: is the workspace-canonical reducer shell
hand-written per component? Method: a six-finder + adversarial-verify
workflow across the 14 nexus.schema components, then **direct source
re-verification of every load-bearing claim** because two verifier agents
were unreliable (one lost the workspace; one waved off the naming flaw with
"it's emitted, so naming rules don't apply" — wrong, the prefix is in the
*authored* schema source). Everything below is confirmed from the code, not
from the workflow's say-so.

## The two real flaws

### 1. `Nexus*` namespace prefix in 12 components' authored schema (systemic)

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

### 2. The spirit driver fork (single component, transitional)

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
| A component owning its own `nexus.schema` | Intended | The three-plane split: every daemon authors signal/nexus/sema schemas. Not duplication. |
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

One-shot (schema-source edit + regenerate; no emitter change):

1. Drop the `Nexus*` prefix in every component's `nexus.schema`
   (`Work`/`Action`/`EffectCommand`/`EffectResult`/`ObjectName`); regenerate
   `src/schema/nexus.rs`; delete the `Sema*` re-aliasing imports in
   `spirit/src/nexus.rs` so the daemon uses `sema::ReadInput` directly.
   Mechanical, breaks all consumers at once (allowed). This is the psyche's
   "rename-`Nexus*`-prefix" item.

Runner/emitter change (heavier, sequence after the rename):

2. Teach `triad-runtime::runner::drive` (or schema-rust-next's runner
   adapter) the no-alias schema shape, then delete spirit's hand-written
   `execute_to_reply` and route spirit through the shared driver. This is the
   psyche's "lift-the-shared-shell" item — but narrowed: the shell is already
   lifted for everyone except spirit; this re-absorbs the one fork.

Bead routing: **neither item belongs to bead `primary-tqe3` (the guardian
retrieval fix)** — the guardian work does not intersect the naming or driver
roots (the `guardian_journal` "violations" were verified false). Item 1 is a
new bead; item 2 is a separate, dependent bead.

## Open questions for the psyche

1. **Capture the prefix-drop as intent?** No Spirit record governs the
   `Nexus*` / `Sema*` runtime-type prefix. Record a Clarification that the
   no-ancestry-prefix guideline binds schema-source runtime type names (not
   just hand-written Rust)?
2. **Driver re-absorption now or later?** Item 2 depends on the shared runner
   learning the no-alias shape. Land the rename now and leave the spirit
   driver fork until the runner work is scheduled, or do both together?
3. **Trace types** — leave `TraceEvent` / `TraceAction` as-is, or fold into
   the engine-trait hook shape in the same pass? (I'd want to read
   `trace_event.rs` first before recommending.)
