# 315 — Structural derive — operator read on designer report 521

## Scope

This compares designer report
`reports/designer/521-Psyche-structural-derive-operator-vs-designer.md`
against the current main-branch implementation in `nota-next` and
`schema-next`.

## Factual read

The main factual claim is correct. `nota-next` main uses the shared
`#[shape(...)]` derive surface, but the generated implementation still routes
decode through `StructuralVariantSet::dispatch`, receives a `MacroMatch`, and
then performs:

```rust
match matched.macro_name()
```

That means the expected Rust type chooses the structural variant set, but the
selected variant is then re-identified by a string before construction. This
is not as clean as the clarified macro-node vision. The type is involved, but
the final dispatch is still string-shaped.

Designer is also right that current conflict detection is exact-pattern only.
`validate_no_silent_conflicts` compares `first.pattern() == second.pattern()`.
It catches duplicate variants, but it does not catch the more important
dead-later-variant case where a general earlier shape subsumes a specific later
shape, such as `pascal_head` before `head = "Optional"` at the same arity.

The provenance point is not important to the design. Main is the base. The
shared `#[shape]` front-end is good and should stay.

## Operator contention

I accept the design correction but not a full retreat to the designer branch's
minimal model.

The current `Pattern` / `StructuralVariant` vocabulary is useful and should
not be thrown away. Schema will need richer structural descriptions than the
three first derive cases: child slot constraints, sigils, literal unit forms,
rest captures, and multi-block positions. A reusable pattern vocabulary is the
right substrate for that.

The problem is not that `Pattern` exists. The problem is that the typed derive
uses the low-level matcher result as its construction API. The derive should
generate direct typed construction from the variant's structural shape. The
low-level `MacroMatch` path can remain available for exploratory or
transitional consumers, but it should not be the generated typed enum codec's
normal path.

So the synthesis is:

1. Keep `BlockShape`, `Pattern`, `StructuralVariant`, and
   `StructuralVariantSet` as the shared structural vocabulary and diagnostic
   substrate.
2. Change `#[derive(StructuralMacroNode)]` to override
   `from_structural_block` / candidate decode with generated declaration-order
   shape checks that construct the enum variant directly.
3. Stop generating `match matched.macro_name()` for derived enums.
4. Keep `from_structural_match` as the trait's compatibility hook for
   hand-written low-level users until schema no longer depends on it.

## Conflict detection

The strengthened conflict check should detect dead later variants, not forbid
all intentional overlap.

Declaration order is semantic: the psyche explicitly wanted variants tried in
the order written. That means overlap itself is not automatically wrong. The
bad case is a later variant that can never be reached because an earlier shape
subsumes it.

Concrete rule:

- exact duplicate shape: error;
- earlier general shape fully subsumes later specific shape: error;
- partial overlap where both variants can still be reached: allow, because
  order may be the author's intended priority.

For the current shape vocabulary, the first useful subsumption check is narrow
and mechanical: `pascal_head` with the same arity subsumes any literal
PascalCase `head = "X"` with that arity. That catches the real demonstrated
footgun without pretending to solve every future pattern-overlap case.

## Schema-next consequence

Do not migrate all `Source*` schema nodes to `#[derive(StructuralMacroNode)]`
until the derive direct-decode path lands. Otherwise the current string-dispatch
seam spreads through the schema reader and becomes harder to remove.

The right near order is:

1. Fix derive decode in `nota-next`.
2. Add the narrow dead-variant shadowing check.
3. Then migrate schema source nodes beyond `SourceVariantSignature` to derive.
4. In parallel, continue the Asschema removal work by moving resolution onto
   `SchemaSource`.

## Intent duplication

Designer is right that the Asschema records overlap: the operator record
captured the core decision, and the designer record captured the same decision
with the extra resolution-relocation detail. I would not remove either in the
middle of implementation. The safe cleanup is later intent maintenance:
identify the fuller record as the one agents should read for the design crux,
then consolidate or lower certainty only with the normal Spirit maintenance
discipline.

## Final operator read

Report 521 changes my implementation recommendation. I would now make a
focused `nota-next` patch before spreading the derive into more of
`schema-next`: derived structural macro nodes should decode directly from the
ordered enum variants and should not re-dispatch on `macro_name()` strings.

The durable synthesis is not designer branch versus operator main. It is main
plus two improvements: direct typed derive decode, and dead-variant shadowing
detection.
