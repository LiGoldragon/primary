# 1 — Intent and design synthesis

Subagent 1 report for operator meta-report `198-nota-structural-library-prototype-2026-05-26`.

## Sources Read

Spirit intent:

- `schema` / `nota` / `schema nota` records in the `730-807` range, with emphasis on `746`, `753-756`, `758-764`, `770-776`, `783-793`, and `799-807`.
- `component-shape` records `764-780` for the root-variant pressure, Spirit/core naming, and new-repo direction.

Reports:

- `reports/operator/193-schema-object-pass-and-spirit-v0-3-skill-correction-2026-05-26.md`
- `reports/operator/194-nota-schema-restack-operator-reading-2026-05-26.md`
- `reports/operator/195-schema-driven-nota-reader-prototype-2026-05-26.md`
- `reports/operator/196-schema-object-block-pass-prototype-2026-05-26.md`
- `reports/operator/197-nota-core-design-refresh-and-gap-audit-2026-05-26.md`
- `reports/designer/353-schema-derived-nota-design-2026-05-26.md`
- `reports/designer/355-critique-of-operator-195-schema-driven-nota-reader-2026-05-26.md`
- `reports/designer-assistant/354-schema-derived-nota-prototype-2026-05-26.md`

`reports/designer/354-*` does not exist in the current tree; designer report numbering jumps from `353` to `355`.

## Current Design Reading

The newest turn clarifies the layer boundary more sharply than the earlier schema-derived NOTA reports. NOTA is not the semantic language that decides final type meaning. NOTA is the thin structural library that reads text into blocks and atoms, then exposes methods over that structure.

The raw layer should answer questions such as:

- what delimiter bounds this block;
- where the block begins and ends in source;
- how many root objects the block contains;
- whether a child object has some recursive shape;
- whether an atom qualifies as a symbol candidate;
- which symbol class the atom qualifies for.

Those methods are macro primitives. Schema macros consume them to build custom positional data languages. The macro layer is where a square-bracket block becomes an ordered struct field vector, a parenthesis block becomes an enum declaration, or a curly block becomes a namespace map. The same raw shape can mean something else in another macro position.

That makes record `758` the correction that keeps the design honest: delimiter shape does not globally mean struct, enum, map, or newtype. Meaning appears only when the block is in a macro position whose lowerer gives it that interpretation.

## Symbol Qualification

Records `786-789` and `799-803` move casing and PascalCase legality out of raw NOTA. The raw layer should not reject a PascalCase atom merely because the eventual schema position may be a string position. At the raw layer, the right verb is `qualifies_as`, not `is`.

A token can qualify as a symbol because its text is symbol-safe and matches a structural class such as PascalCase, camelCase, or kebab-case. That does not mean it is already a type name, method name, enum variant, or string. The schema or macro context decides the final type.

The direction of information should be strongest-first: if a token can qualify as a symbol, carry it as a qualified-symbol candidate. Later, the typed schema layer can demote that candidate to string content when the final schema says the position is a string. The reverse direction is weaker: once an atom is treated as arbitrary string too early, reliably promoting it back into a symbol is harder and risks inventing semantic certainty that the raw layer did not have.

This is the cleanest answer to the bracket-string/vector tension too. The raw layer should preserve block/atom structure and symbol qualifications; the schema position interprets whether a bracketed body is string content, a struct vector, an input/output section, or a macro body. `[|...|]` remains the explicit opaque block-string escape for content containing bracket forms.

## Schema Root Shape

The `.schema` file extension supplies the root type context. A schema file is read as the known `Schema` struct, so the authored file should not wrap itself in `(Schema ...)` or any equivalent explicit root record. This continues the older rule from records `433`, `471`, `785`, and `790`: file context supplies the root struct.

The newest records then recast the root shape as ordinary positional structs:

- an imports/exports structure describes what names the schema consumes and what names it makes available to assembly;
- an input/output structure describes the channel surface: what comes in and what goes out;
- namespace/type definitions supply the reusable type vocabulary that input and output refer to.

Record `791` is the strongest phrasing: imports/exports and input/output should be represented faithfully as positional structs, using square brackets because structs are ordered field vectors. Record `805` adds a concrete draft: the root schema struct is implied by `.schema`; the first field is the imports/exports namespace; subsequent positional fields are input/output structs. Record `806` leaves one detail explicitly open: whether imports/exports come first, like a let statement, or input/output comes first, like a function signature. The current implementation should carry that uncertainty and use imports/exports-first only as the pending convention, not as settled metaphysics.

This also corrects the five-block prototype reading from designer-assistant report `354`. That prototype is valuable evidence, but its mandatory five physical blocks are not yet the canonical root representation. The newer intent points toward a smaller faithful root struct whose fields are known by file context and schema-schema, with optionality represented inside the struct shape rather than by a permanently fixed five-block file layout.

## Macro And Asschema Pipeline

The pipeline now reads as:

```text
source text
  -> NOTA structural blocks and atoms
  -> schema macro actors consuming structural methods
  -> macro re-emission / resolved intermediate objects
  -> Asschema / AssembledSchema
  -> Rust composer and runtime readers
```

`Asschema` is the resolved endpoint: pure NOTA-representable assembled schema data, order-preserving, fully typed, and macro-free. It should contain enums, structs, newtypes, and typed endings in their resolved form. It is not authored sugar and not a macro body. Macros may conceptually re-emit NOTA, though an implementation may keep the intermediate in memory as typed Rust values or binary data.

Operator report `195` proved a useful narrow slice: namespace text can lower into ordered assembled declarations, emit Rust readers, compile a fixture, and decode real NOTA. Report `196` then added the missing source-block pass with spans and recursive shape predicates. The remaining design gap is to make those predicates the actual public NOTA structural library surface, then make schema macro matching consume that surface rather than hard-coded namespace-value lowering.

Designer-assistant report `354` proves the broader vision is plausible: a `nota.schema`, bootstrap kernel, three-part schema reader, macro classifier, in-process library with core fallthrough, and tests. But the prototype still has teaching-shape compromises that latest intent tightens: comment-heavy schema files, a five-block physical layout, and heuristic bracket disambiguation that should be pulled toward schema-context interpretation.

## Implementation Consequences For The Main Agent

The main implementation slice should not start by generating more typed readers. It should first make the raw NOTA structural library precise enough that schema macros can stand on it. The natural Rust surface is an object model with methods on block and atom types, not free helper functions:

- `Block` owns delimiter, source span, object count, child access, and recursive shape predicates.
- `Atom` owns text span, literal classification, and `qualifies_as_*` predicates.
- `QualifiedSymbol` owns symbol text plus symbol class.
- `MacroPattern` or equivalent owns reusable matcher composition over blocks and atoms.

The critical naming point is that methods should say `qualifies_as_*` where the raw layer has only a candidate. `is_*` belongs to delimiter facts and source facts, not final schema semantics.

The implementation should also keep two trees from drifting apart. Report `196` currently runs a block pass and then a value pass. That is acceptable for a prototype, but the next reusable component should tie together source span, delimiter shape, recursive predicates, atom classifications, and typed value access for the same object. Future macro lowerers should not need to align two independent trees by position.

Finally, the new design should not be blocked on repository renaming. Record `781` says `nota-next` on the existing `nota` repository is the chosen direction for Nota logic. Record `782` keeps the `schema` repository name. Records `780` and `792` authorize clean new Spirit-facing repos and make new clean repositories acceptable to consider, but the structural-library slice can faithfully prototype on the existing operator schema branch and existing `nota`/`schema` repos.

## Biggest Gaps

1. The canonical raw object type is still not named and stabilized. `SchemaBlockPass` is close, but the reusable NOTA structural library API should be a first-class `nota` surface, not only a schema prototype module.

2. Symbol classification needs tests that prove the new rule: PascalCase, camelCase, and kebab-case atoms qualify as symbols without becoming final semantic types; schema context can demote qualified symbols to strings.

3. The schema root shape is clarified but not fully settled. `.schema` implies the root `Schema` struct, and imports/exports plus input/output are positional structs, but record `806` leaves root field ordering open.

4. `Asschema` is still intent and prototype vocabulary, not a canonical order-preserving Rust type plus NOTA serialization. This is the center that should replace both old six-position schema and the prototype-only `AssembledNotaSchema`.

5. Existing prototypes prove different halves of the design but have not converged: operator has production-adjacent compiled reader and source spans; designer-assistant has broader `nota.schema` and library proof. The next slice should integrate the structural library API first, then let both proof lines collapse into one macro-to-Asschema path.
