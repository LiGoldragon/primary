# Subagent 2 — Code Shape Audit

Scope: read-only inspection of:

- `/home/li/wt/github.com/LiGoldragon/schema/operator-schema-driven-nota-parser-prototype-2026-05-26`
- `/home/li/wt/github.com/LiGoldragon/schema/designer-schema-derived-nota-2026-05-26`

Frame: operator report `195` and meta-report `198/0-frame-and-method.md`.

## Current Branch Shapes

The operator branch has the most directly useful landing base. `src/object_block.rs` introduces `SchemaBlockPass`, `SchemaBlockObject`, `SchemaBlock`, and `SchemaAtom`. It parses delimiter-balanced source into positioned blocks, keeps `[|...|]` block strings opaque, exposes delimiter predicates, object counts, child accessors, and `qualifies_as_symbol`. Its tests in `tests/object_block_pass.rs` already pin the right direction for source spans, recursive predicates, block-string opacity, and delimiter-balance errors.

The operator branch also has the strongest end-to-end proof in `src/nota_reader.rs` and `tests/schema_driven_nota_reader.rs`: authored namespace text lowers to ordered `AssembledNotaSchema`, emits Rust reader code, string-compares the emitted module against a compiled fixture, and proves decoding of positional structs plus unit/data-carrying enum variants. This is the best path for implementation momentum.

The designer branch has the cleaner conceptual vocabulary for the new NOTA layer. `prototype/src/kernel.rs` names the bootstrap boundary explicitly: kernel builds a delimiter tree, schema interpretation happens above it. `prototype/src/blocks.rs` gives first-class `Block` values with spans, root objects, re-emission, and recursive predicates. `prototype/src/macros.rs` sketches a `MacroEngine` that classifies shapes into `SingleIdentifierMap`, `KeyValueMap`, `NamedRecord`, and `Vector`. Its tests in `prototype/tests/block_parser_constraints.rs` are especially useful because their names pin intent records and make the behavior auditable.

## Main Gaps

The operator branch has two parallel structural layers. `SchemaBlockPass` parses the text into blocks, but `AssembledNotaSchema::from_namespace_text` still lowers through `SchemaObjectPass` and `nota_codec::NotaValue`. Today the block pass mostly acts as a delimiter-balance guard before the older `NotaValue` path does the real schema interpretation. The next implementation should make blocks/atoms the consumed substrate, not just a validation sidecar.

The structural layer does not yet distinguish symbol classes. `SchemaAtom::qualifies_as_symbol` is a single boolean over ASCII identifier-like text. Latest intent wants “qualifies as” to be explicit and stronger than final semantic typing: PascalCase, camelCase, kebab-case, and possible future method symbols are structural candidates, while the schema/macro context decides whether the candidate becomes a type, variant, method name, key, or string. That calls for a `QualifiedSymbol` plus `SymbolClass`, not just `Option<&str>`.

The designer macro matcher is not yet connected to schema lowering and is still a classifier over raw `Node`. It can classify `{ universalUnknown }` or `{ host localhost port 8080 }`, but it does not take a macro-position value, a declared macro input type, or a schema context. That is the exact place old ambiguity can return: delimiters would again seem globally meaningful unless the matcher is only invoked from a known macro position.

The designer prototype keeps a five-block schema layout, while latest intent has moved toward the `.schema` file as an implied root `Schema` struct with positional fields, imports/exports first as the pending default, then input/output struct shape. That root-shape drift is outside this subreport's code-edit scope, but any production implementation should avoid baking the five-block prototype layout into the structural library.

Old Feature drift is still live in both main crate surfaces. The operator branch is worse because `EffectTable`, `FanOutTargets`, `StorageDescriptor`, `FeatureInput`, `FeatureMacroRecognizer`, six-position `features`, and tests/fixtures remain executable. The designer branch removed the three retracted effect-side variants from the prototype, but still has a `Feature` surface in the main crate. The new structural library must not route through any of that; it should produce final assembled data definitions only.

## Implementation Recommendations

1. Promote the block/atom model into the actual NOTA structural API. Use the operator branch as the integration base, but pull the designer branch's clearer `Block` vocabulary into a real library surface: `Document`, `Block`, `Atom`, `DelimiterKind`, `SourceSpan`, `SourcePosition`, `QualifiedSymbol`, and `SymbolClass`. The API should answer structural questions: delimiter, object count, child by index, recursive predicates, raw span slice, and qualified-symbol class.

2. Make atom methods say “qualifies as,” never “is.” `Atom::qualified_symbol()` should return `Option<QualifiedSymbol>`, and `QualifiedSymbol` should expose methods such as `is_pascal_case_candidate`, `is_camel_case_candidate`, and `is_kebab_case_candidate`. The raw NOTA layer must not reject PascalCase at string-looking positions; schema context can demote a qualified symbol to string later.

3. Implement a data-bearing `MacroMatcher` over blocks, not a global delimiter interpreter. The matcher should take a `MacroInput` or `MacroPosition` plus a `&Block`, then compose reusable predicates: delimiter kind, arity, nth-child shape, key-value pairing, all-keys-qualified, first-child-qualified, and block-string opacity. This keeps `(…)`, `[…]`, and `{…}` structural until a known macro lowerer consumes them.

4. Move `nota_reader.rs` lowering from `NotaValue` to the structural matcher pipeline. The target path should be source text -> `Document`/blocks -> macro-position matchers -> `Asschema` / `AssembledSchema` -> Rust emitter. `SchemaObjectPass` can remain temporarily as a compatibility witness, but the new tests should prove the reader can lower from blocks without `nota_codec::NotaValue` shape shortcuts.

5. Fence old Feature drift at the boundary. Add tests in the new path that reject authored `EffectTable`, `FanOutTargets`, `StorageDescriptor`, and any six-position `features` root. Keep the existing reader proof's `!emitted.contains("Feature")` check, but add structural tests that the matcher and assembled output have no `FeatureInput`, no `FeatureMacroRecognizer`, and no route through `signal_channel!` or `legacy_signal_channel!`.

## Code-Shape Notes

The operator branch currently uses several zero-sized method-holder structs: `NotaReaderRustEmitter`, `NamespaceTypeLowerer`, `TypeExpressionLowerer`, and `TypeRenderer`. They are acceptable as prototype scaffolding, but they should not become the permanent shape under the current Rust discipline. The durable form should move verbs onto data-bearing nouns: `AssembledSchema::emit_reader_module`, `NamespaceObject::lower_with(&MacroMatcher)`, `TypeExpression::rust_type`, or stateful emitter/lowerer structs carrying configuration and diagnostics.

The designer branch's `Kernel::lex_bracket` contains a heuristic that decides whether plain `[...]` is an inline string or vector by scanning for “string-only” bytes. That is the ugliest part of the prototype relative to the newest intent. The structural library should avoid semantic classification at this layer where possible: preserve the bracket block and its span, keep `[|...|]` opaque as the unambiguous block-string form, and let schema context decide when a bracket block is string content versus a vector-like object.

The designer branch's constraint-test style is worth copying. Test names like `constraint_774_blocks_carry_source_spans` and `constraint_776_reassembly_is_concatenation` make intent breakage searchable. The operator branch should add equivalent focused tests for records `783`, `784`, `786`, `799`, `800`, and `801`: NOTA as thin structure library, macros as custom parsers, no raw PascalCase final legality, “qualifies as” naming, and qualified-symbol demotion.

## Recommended Integration Base

Use the operator branch as the base because it already compiles the reader proof inside the real schema crate and tests generated Rust against a compiled fixture. Import the designer prototype's naming and constraint-test discipline, not its five-block schema layout or standalone `MacroEngine` shape.

The next slice should be small and mechanical: add `SymbolClass`/`QualifiedSymbol`, add `MacroMatcher`, refactor one namespace-value lowerer to consume block predicates instead of direct `NotaValue` matching, and add tests that the old Feature surface is invisible from the new path.
