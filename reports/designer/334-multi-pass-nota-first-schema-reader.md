*Kind: Design + Concept · Topic: multi-pass NOTA-first schema reader · Date: 2026-05-25 · Lane: designer*

# 334 · Multi-pass NOTA-first schema reader — every schema is NOTA + context-sensitive macros

## §1 Frame

Per psyche directive 2026-05-25: *"How you're saying we're not using NOTA to read schema because it has its own parser, and I would like to actually remedy that. So it can't use straight-up NOTA because it has these macros — macros that are in effect at certain places, which is what the schema defines. So it's a sort of we have to define the macro in the schema and then read the schema to populate the macro and then reread the schema with the macros. We should do multiple pass."*

This report presents the concept in detail. It pairs with a parallel subagent that test-implements the multi-pass reader to surface design flaws + implementation flaws together.

## §2 The deviation today (one-paragraph recap)

Per `reports/nota-designer/8-nota-schema-lowering-deviation-audit.md`: `signal-frame/macros/src/schema_reader.rs` carries a PRIVATE schema reader with its own grammar — a parallel parser distinct from the canonical NOTA parser. That private grammar accepts shapes the workspace has retired (`(Path ...)`, `[Option T]`, scalar `(Root Payload)`) and rejects shapes the v13 schema requires (multi-endpoint header roots like `Watch [State Records]`). Two parsers, two truths. Schema authority lives where the parser is most lenient — which today is the wrong parser.

The remedy is structural: **NOTA is the only syntax; the schema is NOTA + macro-application passes**. A schema file is read by the universal NOTA parser, then transformed by passes that interpret position-specific macros. No parallel grammar. No private parser. One syntax, one truth.

## §3 The multi-pass conceptual model

Six numbered passes from text to canonical assembled form. Each pass has ONE responsibility; nothing crosses pass boundaries except the typed artifact each pass produces.

### §3.1 Pass 0 — Lexical (text → tokens)

The universal NOTA lexer. Input: the raw bytes of `<component>.schema`. Output: a token stream — open/close paren/bracket/brace, identifier (bare PascalCase, kebab-case, snake_case), integer literal, string literal (`[...]` bracket strings per `primary-36iq`).

No schema-specific behavior. Lives in `nota-codec`.

### §3.2 Pass 1 — Syntactic (tokens → `NotaValue` tree)

The universal NOTA parser. Output: a generic `NotaValue` tree. Variants:

```
NotaValue =
  | NotaRecord    (parenthesised positional list)
  | NotaList      (square-bracketed positional list)
  | NotaMap       (curly-braced name-value map)
  | NotaIdentifier (bare PascalCase / kebab-case)
  | NotaString    (bracket-string)
  | NotaInteger   (decimal)
```

No semantic interpretation. Records are not yet typed. Lives in `nota-codec`. This is the parser EVERY NOTA consumer uses — schema, sema, signal frames, intent records, lock files, all of it.

### §3.3 Pass 2 — Structural (NotaValue → `SchemaDocument` positions)

The first schema-specific pass. Asserts the six-position shape: a `.schema` file's root `NotaValue` is a tuple of six positions matching the canonical layout from `/326-v13`:

```
position 0:  NotaMap     → imports
position 1:  NotaList    → ordinary header
position 2:  NotaList    → owner header
position 3:  NotaList    → sema header
position 4:  NotaMap     → namespace
position 5:  NotaList    → features
```

This pass is itself a structural macro — "the .schema file shape macro." If position 0 isn't a map or position 1 isn't a list, the pass errors. Output: `SchemaDocument` with each position's `NotaValue` stored under its semantic name. No further interpretation yet.

### §3.4 Pass 3 — Macro identification (walk positions, identify `NodeDefinitionPoint` + `BuiltinMacroVariant`)

Per operator/175.4 + `/329`. Each position has a set of valid macros that can appear inside it. The position is the `NodeDefinitionPoint`:

| Position | NodeDefinitionPoint | Valid macro variants |
|---|---|---|
| 0 (imports map values) | `ImportMapValue` | `ImportAll(ImportAllInput)`, `Import(ImportInput)` |
| 1/2/3 (header list items) | `HeaderRoot` | `HeaderRoot(HeaderRootInput)` |
| 4 (namespace map values) | `NamespaceValue` | `EnumDefinition(EnumDefinitionInput)`, `StructDefinition(StructDefinitionInput)`, `NewtypeDefinition(NewtypeDefinitionInput)`, `ImportReference(ImportReferenceInput)`, `Alias(AliasInput)` |
| 5 (features list items) | `FeatureItem` | `Reply(ReplyInput)`, `Event(EventInput)`, `Observable(ObservableInput)`, `Storage(StorageInput)`, `Upgrade(UpgradeInput)` |

(Inside any nested context — e.g., inside a record field type — there's a sub-`NodeDefinitionPoint` called `FieldType` for primitive/container/reference expressions.)

For each `NotaValue` at each position, the pass disambiguates by SYNTACTIC SHAPE:

- A `NotaList` at namespace position → `EnumDefinition` (variants are list items)
- A `NotaRecord` at namespace position → either `StructDefinition` or `NewtypeDefinition` (multi-field vs single-field) or `ImportReference` (if head is a known import binding) or `Alias` (if single bare identifier)
- A `NotaIdentifier` at namespace position → bare reference (alias or import-bound name)

The output is each position annotated with its variant + the typed input struct decoded from the `NotaValue`. Per `/329`'s InputStruct-per-variant pattern: each variant has its own typed input shape.

### §3.5 Pass 4 — Macro application (run each variant's lowerer)

Each `BuiltinMacroVariant` is a `SchemaMacro` implementation (per `/329` trait). The lowerer takes the typed input + a `LoweringContext` and emits `AssembledFragment` entries into a builder.

**Order matters.** Imports run first because subsequent variants may reference imported names. After imports:

1. **Import macros**: load sibling schemas via `schema::LoadedSchema::read_path` (recursive); populate the import-binding map; expose imported types into the local namespace.
2. **Type macros** (enums, structs, newtypes): emit `AssembledType` entries with their layout (computed by the layout subpass after imports are resolved).
3. **Header macros**: emit `Route` entries — `(leg, root_slot, root_name, endpoint_slot, endpoint_name, body_type_reference)`.
4. **Feature macros**: emit `AssembledFeature` entries — reply variants, event streams, storage tables, upgrade rules.

Each macro is PURE over its typed input + the lowering context. The only effectful macro is import (it loads files). Per nota-designer/8 §"Reusable Lowering Shape" — this is the constraint.

### §3.6 Pass 5 — Assembly (AssembledFragments → AssembledSchema)

Pure builder. Inserts each fragment into a typed canonical container. Validates cross-references: every type referenced by a route must exist in the namespace (local or imported). Mints component-scoped UIDs (per nota-designer/8 §"AssembledSchema Lacks Component Identity") — `spirit::Topic`, `orchestrate::RoleIdentifier`, etc. Computes layout metadata on the assembled form (per nota-designer/8 §"Layout Uses Pre-Assembled Document" — the fix is to layout AFTER assembly so imported fixed-width types are known).

Output: `AssembledSchema`. Pure data. Diffable. Cacheable. The canonical machine object for storage descriptors, code emission, and version-diff projection.

### §3.7 Pass 6 — Code emission (downstream consumer)

NOT part of the schema engine — a separate consumer. The proc_macro library (`signal-frame-macros`) calls `schema::LoadedSchema::read_path(...).assembled()` to get an `AssembledSchema`, then emits Rust code from it.

The proc_macro is one of MANY possible consumers. Others (per nota-designer/8 §"Adapters"):
- `version-projection` derives projection impls from previous/next `AssembledSchema` pair
- `sema-engine` emits storage descriptors from assembled storage nodes
- Future schema-daemon stores + queries `AssembledSchema` values
- Future version-diff projection-macro generator

All consume the SAME `AssembledSchema`. None re-parse the schema.

## §4 Macros as context-sensitive transforms

Two NOTA subtrees with identical syntactic shape mean different things at different positions. Examples:

| NOTA shape | Position | Macro | Meaning |
|---|---|---|---|
| `[A B C]` | header list | (the list IS the header) | "the ordinary header contains A, B, C as root verbs" |
| `[A B C]` | namespace value | `EnumDefinition` | "this is an enum with variants A, B, C" |
| `[A B C]` | inside a record field-type | `FieldType` (container shape) | error — `Vec` / `Option` are explicit |
| `(Foo Bar Baz)` | namespace value | `StructDefinition` if Foo is the type name, else `NewtypeDefinition` or alias |
| `(Foo Bar Baz)` | inside header sub-variant | `HeaderEndpoint` | "endpoint Foo with body type Bar Baz" |

The `NodeDefinitionPoint` cursor is what disambiguates. It's the "context" the user named: *"there's places where something has to be run to modify the schema, essentially, and then it can be read as NOTA in a certain context."*

This is exactly how Lisp macros work: read → macroexpand → eval. NOTA reads everything as generic values; the schema's macro pass interprets each value contextually.

## §5 The self-hosting bootstrap

Today the set of valid `BuiltinMacroVariant`s + `NodeDefinitionPoint`s is hard-coded in Rust (`schema/src/engine.rs`). Ideal end-state: the schema language describes itself via a `schema.schema` file — a "meta-schema" — and the engine loads it the same way it loads any other schema.

Bootstrap sequence:

1. **Today**: `schema/src/engine.rs` carries the meta-knowledge in Rust. The 4 builtin variants (Import / Header / Type / Feature) + the 4 position points (ImportMapValue / HeaderRoot / NamespaceValue / FeatureItem) are Rust enum definitions.
2. **Next**: extend to 7 builtins + 7 position points per `/329` + operator/175.4 (add `NewtypeDefinition`, `FieldType`, `UpgradeRule`).
3. **Then**: write `schema/schema.schema` (a meta-schema) declaring those builtins as named macro variants at named position points. The Rust engine LOADS the meta-schema at startup and validates that authored schemas conform to it.
4. **Self-hosting moment**: the meta-schema itself is loaded with the same multi-pass reader; the engine cross-verifies its own bootstrap.
5. **Third-party extensions**: future custom macro variants register the same way as builtins — declare in a sub-schema file; the engine picks them up via the meta-schema registry.

This is the long-term path. The multi-pass reader is the foundation; self-hosting is the eventual fruit.

## §6 Implementation deltas — what changes to land this

**In `nota-codec`**: nothing new. Pass 0 + Pass 1 already work. The lexer + parser are universal and already correct.

**In `schema` (the typed substrate)**:
- Promote the existing `parser.rs` from "schema-flavored NOTA reader" to "Pass 2 structural pass that consumes generic `NotaValue` from `nota-codec`". Likely just re-route the input — currently `schema/src/parser.rs:1-50` does its own NOTA-ish tokenization; replace with `nota_codec::parse(text) -> NotaValue` then convert.
- Add `NodeDefinitionPoint` enum extensions (the 3 missing per `/175.4`): `FieldType`, `HeaderEndpoint`, `UpgradeRule`. Bead `primary-cklr` covers UpgradeRule.
- Add `BuiltinMacroVariant` enum extensions for the missing variants.
- Per nota-designer/8 §"Schema Erases Macro Input Object Roles": add named input structs for each variant (e.g., `HeaderRootInput { root: Name, endpoints: Vec<EndpointInput> }`). Field names live in the Rust input model, not in NOTA value syntax (NOTA stays positional).
- Per nota-designer/8 §"Engine Annotations Do Not Reach AssembledSchema": carry engine annotations on `Route`.
- Per nota-designer/8 §"Layout Uses Pre-Assembled Document": move layout planning to AssembledSchema phase.
- Per nota-designer/8 §"AssembledSchema Lacks Component Identity": add UID minting.

**In `signal-frame/macros/src/schema_reader.rs`**: the big remedy. **Replace the entire file** with a thin adapter:

```rust
// signal-frame/macros/src/schema_reader.rs (the new shape)
use schema::LoadedSchema;

pub(crate) fn channel_spec_from_path(path: &Path) -> Result<ChannelSpec, ...> {
    let loaded = LoadedSchema::read_path(path)?;
    let assembled = loaded.assembled()?;
    ChannelSpec::try_from(&assembled)
}
```

That's it. No private parser. No private grammar. The macro library is JUST an adapter from `AssembledSchema` to `ChannelSpec` (which feeds the existing emit pipeline at `emit.rs`).

The current `schema_reader.rs` is ~1700 LoC of parallel parser. After this remedy: ~50 LoC adapter + `TryFrom<&AssembledSchema> for ChannelSpec` impl elsewhere.

**Compat-breaking tests** (per nota-designer/8): the new adapter must REJECT what's now retired — `(Path ...)`, `[Option T]`, scalar `(Root Payload)`. Add tests asserting these forms produce typed errors. This is the place the deviation gets locked out for good.

## §7 Test implementation plan (the parallel subagent's mission)

Run a subagent in background that builds a proof-of-concept multi-pass reader, runs it against existing `.schema` files, and reports where the model deviates from reality.

**Scope (designer-high-level, per record 509)**:

1. New worktree on the `schema` repo: `~/wt/github.com/LiGoldragon/schema/multi-pass-nota-reader`.
2. Add a `multi_pass` module to the `schema` crate with the six-pass pipeline implemented end-to-end against current 4 builtin variants. Use `nota-codec` for Pass 0 + 1.
3. Run it against the three known live schemas:
   - `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema`
   - `~/wt/github.com/LiGoldragon/signal-version-handover/schema-derived-pilot/version-handover.schema` (from subagent C's earlier work)
   - The orchestrate schema from second-designer/173 (`feature/orchestrate-schema-example` branch in `schema` repo)
4. Compare output `AssembledSchema` against what the current `schema::LoadedSchema::read_path` produces. They should be byte-equivalent (modulo intentional differences).
5. Surface every place the multi-pass model breaks: malformed NOTA we can't classify, missing input-struct fields, layout-after-assemble assumption violations, etc.
6. Per record 547 (in-test unblock-the-blocker): if a test needs a missing piece (e.g., the `(Storage ...)` feature isn't fully typed in the current Rust enums), STUB it in the subagent's fixture, don't refuse.

**Report-back format**: branch + commit + pass-by-pass per-schema status table + concrete flaw list + recommendation on whether the multi-pass shape should ship as the canonical path.

## §8 Open questions + flaws to look for

The subagent should look at these specifically:

1. **Import macro side-effects vs purity boundary.** Imports load sibling schemas (side-effectful). Other macros are pure. Does the lowering context need a typed `Effects` capability so import is the only thing with file-system access, and other macros are statically guaranteed pure? Lean: yes — adds compile-time safety against future contamination.

2. **Macro discovery vs hard-coded registry.** Today the 4 builtins are hard-coded enum variants. The registry-based approach (per nota-designer/8 §"Builtin Macro Variants") would have variants register by `(NodeDefinitionPoint, variant_name)` keys at engine startup. Tradeoff: hard-coded is simpler now; registry is needed for self-hosting + third-party extensions. When does registry pay off?

3. **What does Pass 3 do when the syntactic shape is ambiguous?** Example: a namespace value `(Foo Bar)` could be a struct, a newtype, a reference, or an alias. Currently disambiguation depends on whether `Foo` is a known type name vs a constructor token. Does Pass 3 need a pre-pass that collects all type names before dispatching variants? Lean: yes — two-sub-pass within Pass 3 (collect names, then dispatch variants with name-table context).

4. **Diagnostics span tracking.** Each NotaValue should carry its source position (line/column) so Pass 2-5 errors point back at the authored schema text. Does `nota-codec`'s parser thread span metadata? If not, what's the cost of adding it?

5. **Performance: re-parsing schemas on every consumer call.** Currently `schema::LoadedSchema::read_path` is called fresh from each proc_macro invocation per consuming crate. Should there be a caching layer keyed by file path + content hash? Lean: defer until measurement shows it matters; compile-time is amortized across crate-compile time.

6. **The bootstrap chicken-and-egg.** If the schema language IS described by `schema.schema`, what describes `schema.schema`? Lean: the Rust enums in `schema/src/engine.rs` describe `schema.schema`, and the bootstrap sequence loads them in that order. Validate by self-test: the engine should be able to parse its own meta-schema using its own multi-pass reader.

7. **Compat-break risk on existing consumers.** The current `signal-frame/macros/src/schema_reader.rs` accepts retired forms. If the multi-pass adapter rejects them, do any in-flight branches break? Check second-designer's `feature/orchestrate-schema-example` + second-operator/185 + my own subagent C's `schema-derived-pilot` — do they use any retired forms?

## §9 References

- `reports/nota-designer/8-nota-schema-lowering-deviation-audit.md` — the original deviation audit; this report is the design that implements its §"What Should Change First" plan
- `reports/designer/329-schema-macro-component-extensibility.md` — the InputStruct-per-variant + SchemaMacro trait shape
- `reports/operator/174-v5-schema-import-header-design-critique-2026-05-24.md` — header / body / feature separation
- `reports/operator/175-schema-engine-prep/4-reusable-assembled-schema-lowering.md` — operator's NodeDefinitionPoint + BuiltinSchemaMacro design (which this multi-pass formalizes)
- `reports/designer/326-v13-spirit-complete-schema-vision.md` — canonical six-position .schema shape
- `reports/designer/332-schema-macro-coverage-audit.md` — implementation-vs-vision audit (Q: signal-frame-macros has a parallel parser; this report's §6 is the remedy)
- `reports/designer/333-upgrade-mechanism-full-design-explained.md` §4 — where this multi-pass model fits in the bigger pipeline
- `/git/github.com/LiGoldragon/schema/src/` — current schema crate (parser.rs, document.rs, engine.rs, reader.rs, assembled.rs)
- `/git/github.com/LiGoldragon/signal-frame/macros/src/schema_reader.rs` — the 1700-LoC parallel parser to retire
- `/git/github.com/LiGoldragon/nota-codec/src/` — universal NOTA lexer + parser (Pass 0 + Pass 1 already exist)
- Spirit records: 547 (in-test unblock-the-blocker), 535 (real-world testing), 539 (always-background subagent)
