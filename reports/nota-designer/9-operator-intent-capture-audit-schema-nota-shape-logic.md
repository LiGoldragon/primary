# 9 - Operator intent capture audit: schema NOTA shape logic

*Kind: Audit + implementation alignment note. Topic: schema macro NOTA
shape logic. Date: 2026-05-25. Lane: nota-designer.*

## Frame

The psyche forwarded an operator prompt for a narrow purpose: audit the
operator's intent capture, do not take over the implementation. I recorded
that boundary as Spirit record `592` (forwarded operator prompt is audit
context only).

This report therefore answers three questions:

1. Did the operator capture the durable intent in the forwarded prompt?
2. Was anything missing or overextended?
3. Does the in-flight implementation appear to line up with the captured
   intent, without editing operator-owned files?

## Verdict

The capture is mostly correct.

Records `588` and `589` capture the two central durable statements:

- Spirit record `588` (reusable NOTA shape logic): schema macro dispatch
  should use a reusable NOTA object layer instead of ad hoc strings and
  vectors.
- Spirit record `589` (generic subobject pass-through): schema macro passes
  may parse text into generic NOTA values, then pass subobjects through later
  macro passes instead of forcing every object into the final schema type on
  the first pass.

Records `590` and `591` correctly fill two details that would otherwise be
easy to lose:

- Spirit record `590` (delimiter and arity predicates): macro dispatch needs
  concrete predicates for PascalCase atoms, square-bracket objects,
  bracket-pipe block objects, curly maps, and parenthesized objects by arity.
- Spirit record `591` (real vs design reporting): schema reports must
  distinguish implemented behavior, tested behavior, design intent, and
  uncertain design.

I do not see a dangerous false-intent capture in those records. They stay
close to what the psyche actually said.

## One capture edge

The first line of the forwarded prompt also said:

> And how the macro to derive the schema change upgrade is either in design or in practice or both.

I read that as a request to report current implementation reality, not as a
new schema-design decision. Spirit record `591` covers the durable part:
reports must separate real implementation from design-only behavior. Related
upgrade-macro intent was already present before this prompt: record `587`
(macro can decide projection module placement) and the schema-upgrade cluster
around records `551`, `552`, `561`, and `562`.

So I would not add another intent record unless the psyche wants a sharper
rule specifically about upgrade-macro reporting.

## Correct non-captures

The forwarded prompt ended with "implement that and test it and create a
report." That is a work instruction, not durable intent. It belongs in
operator work, tests, and a report, not in Spirit as psyche intent.

The prompt also contained exploratory uncertainty such as "I am not sure
exactly how that looks in practice." That should not become settled intent.
The capture did not overstate that uncertainty into a decision, which is
correct.

## In-flight implementation alignment

The second-operator lane currently claims:

- `/git/github.com/LiGoldragon/schema`
- `/git/github.com/LiGoldragon/nota-codec`

I did not edit either repo.

The dirty `nota-codec` work appears aligned with records `588` through `590`:

- `/git/github.com/LiGoldragon/nota-codec/src/value.rs` adds a generic
  `NotaDocument` and `NotaValue` tree.
- `NotaValue` has structural variants for `Record`, `Sequence`, `Map`, and
  `Atom`.
- The shape API includes `is_record`, `is_sequence`, `is_map`,
  `is_block_string`, `is_pascal_identifier`, `record_head`,
  `record_item_count`, `data_field_count`, and `has_data_shape`.
- `/git/github.com/LiGoldragon/nota-codec/tests/value_shape.rs` tests
  multiple top-level values, macro candidate classification, record head and
  field count, sequence versus bracket-pipe block string, and PascalCase
  identifier detection.

That is the right reusable component shape for the NOTA side: parse once
into a generic value tree, let macro layers ask structural questions, then
hand selected subobjects to later typed lowerers.

## Implementation risks to watch

First, the generic value layer should not be treated as the schema macro
engine. It is the shape-inspection substrate. The schema crate still needs
the macro-pass orchestration: builtin macro registry, node-definition-point
dispatch, fixed-point macro application, and lowering into `AssembledSchema`.

Second, the generic parser currently classifies plain `[` as a `Sequence`
unless it is the bracket-pipe block string form. That is coherent for a
shape layer, but reports should avoid implying the generic pass has solved
every inline bracket-string semantic question. It has detected delimiter
shape. Typed macro positions still decide what that shape means.

Third, the implementation should keep the "real vs design" split explicit.
The schema crate already has real `BuiltinMacroVariant`,
`NodeDefinitionPoint`, `LoweringContext`, route lowering, engine propagation,
and upgrade planning. The still-not-real part is macro code generation from
schema diffs into `VersionProjection` and storage descriptors. That is the
line future reports must not blur.

## Audit conclusion

The operator capture did not waste the prompt. It caught the two main
intent-bearing design statements, and the subsequent records filled the
predicate vocabulary and reporting constraint.

The only thing I would ask the operator to keep sharp is the boundary:
`nota-codec::NotaValue` is the reusable NOTA shape logic layer. The schema
macro engine is the next layer that consumes those shape predicates and
lowers typed macro variants into `AssembledSchema`.
