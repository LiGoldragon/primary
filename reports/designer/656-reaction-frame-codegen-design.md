# 656 — Reaction-frame code generation: ideal output → approach → schema → plan

The psyche's loop on the concrete use case (report `655` addendum / `zjmc`): *derive the ideal
generated code, then the codegen to target, then the simplest schema to express it, then a
syntax + a codegen implementation, then test it.* This is the design pass (Ground + Design
workflow); the implement-and-test phase is dispatched separately. Use case: generate spirit's
`NexusWork`/`NexusAction` from binding the universal `Work`/`Action` frame, instead of
re-authoring them per component (`zjmc`: "re-authoring universal types per component is a
design failure").

## Ideal generated code (what we want emitted)

The frame's generic `Work`/`Action` stay declared **once** in `triad-runtime/src/reaction.rs`
(hand-written, already proven to compile + round-trip rkyv and NOTA over multi-parameter
generics — task #408). Each component's root **expands** to a concrete enum:

```rust
// spirit/src/schema/nexus.rs — expanded from  Input (Work SignalInput SemaWriteOutput SemaReadOutput EffectOutcome)
#[cfg_attr(feature = "nota-text", derive(nota_next::NotaDecode, nota_next::NotaEncode))]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub enum Input {
    SignalArrived(SignalInput),
    SemaWriteCompleted(SemaWriteOutput),
    SemaReadCompleted(SemaReadOutput),
    EffectCompleted(EffectOutcome),
}
pub enum Output {                 // from Action ...
    ReplyToSignal(SignalOutput),
    CommandSemaWrite(SemaWriteSet),
    CommandSemaRead(SemaReadInput),
    CommandEffect(EffectCommand),
    Continue(Input),              // the (Work ...) Continuation arg → the sibling expanded root
}
```

The existing concrete-enum emitter then **automatically** supplies the constructors
(`Input::signal_arrived(...)`) and `From` impls — because the expanded enum has *empty*
parameters, the suppression guards don't fire.

**One honest delta (flagged):** today's `NexusWork` wraps each payload in a redundant
single-field newtype (`SignalArrived(SignalArrived)` over `SignalInput`); the frame
**flattens** it to `SignalArrived(SignalInput)` directly. Leg-for-leg identical by
(variant-name, real-payload-type) and constructor set, but it drops the incidental wrapper
layer (constructors get *simpler* — no `::new` wrap). Correct under no-backcompat + `zjmc`;
the wrapper was not load-bearing. This changes spirit's wire enum shape — surfaced here so it
can be vetoed.

## Approach: EXPANSION, not generic-alias (decisive)

| | Generic-alias (`type Input = Work<…>`) | **Expansion (chosen)** |
|---|---|---|
| Emitter machinery | needs generic impl-header rendering, generic `From`/constructor bodies — **none exists** | concrete enum, empty params → **existing** emitters, zero new machinery |
| Suppression guards (`lib.rs:5104/5154`) | fire (skip constructors/`From`) — spirit couldn't use it | don't fire — full constructor/`From` set |
| Substitution | n/a | `FrameExpansion` already written + proven leg-for-leg (`tests/reaction.rs:118-145, 355-510`) |
| `Never`/fewer-leg risk | bites the generic edges | spirit is full-frame (all 4+5 legs) → no absent legs, no stand-in needed |

Generic-alias is the elegant end-state but is blocked on the generic-impl emission `654`
flagged as real new codegen. Expansion is strictly less code, reuses proven substitution, and
reproduces spirit's surface. Generic-alias is deferred until a genuinely-generic / fewer-leg
consumer needs it *and* someone builds generic impl-header emission.

## Simplest schema representation

**Universal frame, declared once** (`reaction` namespace), in the `hh3z` `(| |)` form:

```
Work (| [Event WriteDone ReadDone EffectDone]
  [(SignalArrived Event) (SemaWriteCompleted WriteDone) (SemaReadCompleted ReadDone) (EffectCompleted EffectDone)] |)

Action (| [Reply Write Read Effect Continuation]
  [(ReplyToSignal Reply) (CommandSemaWrite Write) (CommandSemaRead Read) (CommandEffect Effect) (Continue Continuation)] |)
```

**A component binds it** (spirit) — a two-line import + two application lines:

```
{ Work reaction:reaction:Work
  Action reaction:reaction:Action }
(Work SignalInput SemaWriteOutput SemaReadOutput EffectOutcome)
(Action SignalOutput SemaWriteSet SemaReadInput EffectCommand (Work SignalInput SemaWriteOutput SemaReadOutput EffectOutcome))
```

That entire schema surface replaces ~2578 lines of hand-spelled `nexus.rs` + ~1577 of
`sema.rs` + 61 of `plane.rs`. The `(| |)` declaration head is the one new parser affordance
(extend `DeclarationHead::from_block`, `schema.rs:1381`, with a `PipeParenthesis` arm reading
`child[0]` = params, `child[1]` = body → the same lowered `Declaration`). It is **optional for
making expansion work** — the bare-paren `(Work Event …)` fixture already exercises the whole
pipeline — so we land `(| |)` to honor `hh3z`, but the prototype's correctness doesn't depend
on it.

## Codegen plan (minimal slice)

1. **Promote `FrameExpansion`** from `schema-next/tests/reaction.rs:86-145` into library code as
   a method `impl RootApplication { fn expand_with(&self, params: &[Name], variants: &[EnumVariant]) -> Vec<EnumVariant> }` (verbatim positional substitution; method per the no-free-function rule).
2. **Carry the frame across the import boundary** (the one data-flow blocker): add
   `parameters: Vec<Name>` + `variants: Vec<EnumVariant>` to `ResolvedImport`
   (`resolution.rs:102`), populated in `ImportResolver::resolve` from the **already-loaded**
   `module_schema` (`resolution.rs:216` holds the full body; `:233` currently keeps only the
   count and discards the rest).
3. **Expand at applied-root lowering**: re-route applied roots in `Schema::lower_to_rust`
   (`schema-rust-next/lib.rs:375-386`) so a frame application produces a **concrete `RustEnum`**
   (name = root, params = empty, variants = the expansion) pushed into `root_enums` → flows
   through existing constructor/`From`/accessor/nota/wire emission. Nested `(Work …)`
   Continuation → reference the sibling expanded root `Input` by name.
4. Suppression guards (`lib.rs:5104/5154`) need **no change** — empty params pass.
5. Delete the dead alias path (`RustAppliedRoot`, `AppliedRootTokens`, `emit_applied_root`)
   **after** tests are green.

Files: `schema-next/src/{resolution.rs, schema.rs}`, `schema-rust-next/src/lib.rs`.

## Test plan (proves it works)

1. **Emitted == concrete baseline, leg-for-leg** — assert the emitted `Input`/`Output` enums
   have exactly the 4 + 5 expected `(variant, payload)` legs; promote the proven
   `FrameExpansion` equivalence (`tests/reaction.rs:355-510`, asserted against
   `spirit-nexus-concrete.schema`) to assert on **emitted tokens**.
2. **Golden flip** — replace `schema-rust-next/tests/fixtures/spirit_nexus_generated.rs:554-557`
   (currently the `type Input = Work<…>` aliases, no impls) with the expanded concrete enums +
   their constructor/`From` blocks; assert regenerated == golden. The golden **is** the ideal.
3. **Compiles + round-trips both wire formats** — construct via the *emitted* constructor,
   rkyv `to_bytes`/`from_bytes` round-trip, NOTA `to_nota()`/parse round-trip; including the
   recursive `Continue(Input)` leg.
4. **Call-site parity** — point spirit's ~14 constructor call-sites at the emitted
   `Input`/`Output` and `cargo build` spirit; if it compiles, the constructor set matches.

## Build readiness

**Ready** — the substitution is written + proven, the suppression guards verified to pass on
empty-param enums, the cross-import data is already loaded (just discarded), the routing is a
single `filter_map` pair, and spirit is full-frame (no `Never`/stand-in needed this slice).
Two unknowns the implementer resolves in-flight: (1) **nested Continuation** lowers to a
`Plain` reference to the sibling root `Input` (recursion terminates — `Input` has no `Action`
leg); (2) the **newtype-flattening delta** at call sites (most unaffected; pre-wrapped sites
get simpler). Out of this slice: the `OriginRoute`-triplicate / `Engine*Failure` /
`plane.rs`-bridges consolidation (a later declare-once-universal-types slice).

**Next:** implement-and-test dispatched against this plan, in `schema-next` + `schema-rust-next`
worktrees, reporting the four-layer verdict.
