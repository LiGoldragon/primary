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

Generic-alias is **not** a more elegant end-state — that framing was wrong (psyche
challenge). Its *only* real advantage is that a component root which **is** the generic type
plugs straight into generic runtime code (`triad-runtime`'s generic runner over `Action<…>`)
without a per-component bridge. Everything else attributed to it is illusory here: it is
**wire/runtime-identical** (Rust monomorphizes `Work<…>` into the same layout as the expanded
enum — same bytes, same rkyv/NOTA), it satisfies `zjmc`'s declare-once **no better** (the
frame is declared once in *schema* either way; the alias only changes the build-time-only,
machine-managed generated output, where line count is not a virtue per `9rjq`), and it
**costs** the generic-impl-header emission that does not exist. Expansion gives each component
a clean *owned concrete* interface with normal constructors/`From`, for zero new machinery.

So **expansion is the real end-state, not a compromise**: the genericity is a *schema-authoring*
convenience (don't re-author the shape per component), it does not need to persist as a
generic type in every component's output. Generic-alias is deferred unless the
generic-runtime plug-in ever justifies building generic-impl emission — and even then the
bridge it saves is a single leg-for-leg `From<Output> for Action<…>`, small and itself
generatable, so probably not.

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

## Result — implemented and verified green

**The prototype works end-to-end.** Built on designer worktrees (not pushed; shared `/git`
checkouts confirmed clean): schema-next `reaction-expand` (change `rtxlqtkptunw`) and
schema-rust-next `reaction-expand` (change `ulnvylmyypuw`), cross-patched.

What was implemented (matching the plan):
- schema-next `src/schema.rs` (+146) — `RootApplication::expand_with(...)` (the promoted
  `FrameExpansion`, now a method on the data-bearing noun), `Schema::declared_frame_body`,
  `Schema::expand_application_root` (+ `reaim_sibling_application` re-aiming the nested
  Continuation at the sibling root by name).
- schema-next `src/resolution.rs` (+49) — `ResolvedImport` carries `parameters` + `variants`,
  populated from the already-loaded module schema.
- schema-rust-next `src/lib.rs` (+20) — the applied-roots branch calls
  `expand_application_root`: `Some` → a concrete `RustEnum` into `root_enums` (existing
  emission); `None` → legacy alias fallback (kept for rollback). Suppression guards unmodified
  and confirmed not to fire on the empty-param expanded enums.

Verification (re-run independently, not just trusted from the agent):
- **Emitted Rust** (regenerated `tests/fixtures/spirit_nexus_generated.rs:556-571`):
  `pub enum Input { SignalArrived(SignalInput), … }`, `pub enum Output { …, Continue(Input) }`
  — leg-for-leg per spec, with auto-emitted constructors + `From` (incl. `From<Input> for
  Output`), the newtype wrapper flattened as intended.
- **`cargo test --test spirit_frame_application` → 5 passed, 0 failed**: structural expansion
  assertion, rkyv round-trip via the emitted constructor, the recursive `Continue(Input)`
  rkyv round-trip, NOTA round-trip, fixture write.
- Full suites green (agent-run): schema-next 18 binaries 0 failures; schema-rust-next 88
  passed. No regression.

Two caveats for whoever lands it:
1. **rkyv layout / content-hash shift (load-bearing):** adding `Vec<EnumVariant>` to
   `ResolvedImport` introduced an Archive type-cycle requiring `#[rkyv(omit_bounds)]` + the
   bound attributes (the same treatment `TypeReference`/`ApplicationHead` already carry), and
   shifted every schema content hash that includes enum variants (visible as the two
   regenerated `families_generated.rs` blake3 digests). Expected under the no-byte-stability
   override, but the import-resolution wire/storage shape changed.
2. The legacy `RustAppliedRoot` alias path is retained as a `None`-fallback; delete it once
   expansion is accepted as the only route.

**This closes the psyche's loop on the use case:** ideal output (expanded concrete
`Input`/`Output`) → codegen target (expansion at applied-root lowering) → simplest schema
(universal frame once + bind) → syntax (`(| |)` decl head, optional for the prototype) →
implementation → tested green. Operator owns landing it on code-repo main (the worktrees are
the merge-ready material, minus the prototype `[patch]`). Out of this slice and still open:
the `(| |)` parser arm to honor `hh3z` at the surface; the declare-once consolidation of the
triplicated `OriginRoute`/`Engine*Failure` that deletes the `plane.rs` bridges; and the
broader generics/traits emission (`654`).
