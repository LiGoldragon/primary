*Kind: Design Reversal + Migration Analysis · Topic: bracket semantics swap — () for enum, [] for struct · Date: 2026-05-25 · Lane: second-designer*

# 194 — Bracket semantics swap: `()` for enum, `[]` for struct

## §1 Frame

Per psyche directive 2026-05-25 (to designer responding to `/338`): "() is better for enum/variants and [] better for struct/fields — since a struct is a vector of fields, and an enum is one-of, structurally."

Captured as intent 631 (Decision Maximum). This REVERSES `/326-v13`'s convention (where `[...]` was sequence/enum-variants and `(...)` was record/struct). Touches every existing `.schema` file + the schema-engine substrate operator landed in `/181 + /182 + /190` + my prior `/193` field-naming proposal + intent 614+615+616 (everything-reduces-to-structs, field-naming, divergent-via-newtype).

This is the LARGEST reversal yet seen this session — at the syntactic-bracket level. The substrate compiles + tests pass under the old convention; this rule rewrites the bracket meaning. Counter-ego task: think through the implications cleanly + surface what genuinely needs psyche call.

## §2 The structural justification

The psyche's reasoning: brackets should match the STRUCTURAL CHARACTER of what they enclose.

- **Struct** = vector of fields, all present positionally → `[...]` (vector bracket)
- **Enum** = one-of from alternatives, tagged-variant grouping → `(...)` (variant bracket)

Under this reading, brackets become structurally self-documenting:
- See `[`, expect a vector-shaped content (struct fields, list of items, indexed positional access)
- See `(`, expect a variant-shaped content (tag + payload, alternative grouping, head-and-rest)

This is more principled than `/326-v13`'s convention, which used `[...]` for both sequences (enum variants) AND structural lists (header sub-variants) — overloading the bracket for two semantically-different concepts. The new rule makes the bracket distinction LOAD-BEARING.

## §3 Concrete schema under the new rule

### §3.1 Spirit's namespace declarations

Current (/326-v13 + intent 614 field-naming):
```nota
{
  Kind [Decision Principle Correction Clarification Constraint]
  Magnitude (ImportAll ../sema)
  Topic (String)
  Statement (StatementText)
  Entry (Topic Kind Summary Context Certainty Quote)
  RecordQuery ((Option Topic) (Option Kind) Mode)
}
```

Under intent 631 bracket-swap:
```nota
{
  Kind (Decision Principle Correction Clarification Constraint)       ; ENUM = ()
  Magnitude (ImportAll ../sema)                                       ; (ImportAll ...) is enum-variant → ()
  Topic (String)                                                       ; newtype: also a single-tagged-variant → ()
  Statement (StatementText)                                            ; newtype → ()
  Entry [Topic Kind Summary Context Certainty Quote]                  ; STRUCT = []
  RecordQuery [(Option Topic) (Option Kind) Mode]                     ; STRUCT with container fields
}
```

Reading:
- `(Decision Principle ...)` enumerates one-of alternatives → `()`
- `(ImportAll path)` is a tagged variant of the ImportDirective enum → `()`
- `(String)` and `(StatementText)` are newtype variants — single-tagged-with-payload → `()`
- `[Topic Kind ...]` is a struct's positional field list → `[]`
- `[(Option Topic) (Option Kind) Mode]` is a struct's positional fields where some field types are container expressions → `[]` outer, `()` inner because containers are enum-variant-shaped

### §3.2 Spirit's header section

Current (/326-v13):
```nota
[
  (State [Statement])
  (Record [Entry])
  (Observe [Observation])
]
```

Under intent 631:
```nota
(
  (State [Statement])
  (Record [Entry])
  (Observe [Observation])
)
```

Wait — this is awkward. The HEADER position is a sequence of header-root declarations. Under the new rule:
- Each header-root `(State [Statement])` is an enum-variant: outer `()` for variant, inner `[Statement]` for... struct of sub-variants? Or `[]` for sequence?
- The OUTER bracket containing the list of header-roots: is it a struct (positional ordering matters; all present) or an enum (one-of)?

**Reading A** — outer is struct (positional, all present): `[(State ...) (Record ...) ...]`. The header position is a STRUCT whose fields are header-root variants. Each variant is an enum-variant. This nests cleanly.

**Reading B** — outer is enum (one-of): `((State ...) (Record ...) ...)`. The header position is an ENUM whose variants are header-roots. This is closer to /326-v13's interpretation.

**Lean: Reading A** — header position is structurally a vector of declared header-roots (all must be declared positionally; not one-of). Outer is `[]`. Each header-root is itself an enum-variant declaration → `(State ...)`. Inner sub-variants list — what shape is that?

Sub-variants like `[Statement]`: this is a list of variant names within the State enum. Under the new rule:
- It's a LIST (positional ordering matters; all declared) → `[Statement]` ✓
- OR it's enum-variant declarations (each Statement is a variant of State's sub-enum) → `(Statement)` since the OUTER form of the enum-VARIANT-LIST is the struct of variants

I think Reading A interpretation holds: a list of variant DECLARATIONS is positionally ordered (struct-like), so `[Statement Other...]`. Each variant DECLARATION inside that list is either a unit (bare identifier) or a tagged-variant `(VariantName Payload)`. So sub-variants stay `[]` as a list.

Under this reading:
```nota
[
  (State [Statement])
  (Record [Entry])
  (Observe [Observation])
]
```

Becomes (no change from current /326-v13 form!) because the outer `[...]` was already a sequence (which matches struct semantics) and each header-root variant was `(...)` which matches enum-variant semantics. The /326-v13 convention HAPPENED to align with the new rule at THIS position.

**The header form is mostly unchanged**. The change is in the NAMESPACE section.

### §3.3 The 6-position file shape

Current:
```nota
{Imports}              ; position 0 — map
[Ordinary header]      ; position 1 — sequence of header-roots
[Owner header]         ; position 2
[Sema header]          ; position 3
{Namespace}            ; position 4 — map
[Features]             ; position 5 — sequence
```

Under intent 631:
- Maps `{...}` unchanged (still key-value)
- Sequences `[...]` unchanged AT POSITION LEVEL (header positions are vectors of declared roots — struct-like; features position is vector of declared feature-blocks — struct-like)
- The NAMESPACE map's values change shape per §3.1: enums become `()`, structs become `[]`, newtypes stay `()` (single-tagged-variant)

So the 6-position file shape is unchanged at the top level; only the NAMESPACE VALUES and SOME header sub-variant interiors change.

## §4 Interaction with intent 614+615+616

### §4.1 Field-naming rule (intent 614)

Under intent 614: field names derive from PascalCase type names by lowercasing. Form: `Entry (Topic Kind Summary Context Certainty Quote)` (under old convention) where each PascalCase type name → lowercase field name.

Under intent 631: the form becomes `Entry [Topic Kind Summary Context Certainty Quote]`. Bracket changes; rule unchanged. Field names still derive from type names by lowercasing.

**The two rules COMPOSE cleanly**: intent 614 (field naming) operates on the CONTENT inside the struct bracket; intent 631 (bracket shape) just says which bracket is "struct". Together: `[Type1 Type2 Type3]` is a struct with 3 fields, each named by lowercasing its type name.

### §4.2 Divergent field names via newtype (intent 615)

Under intent 615: divergent field names require newtype declarations. Form: `Certainty (Magnitude)` declares newtype Certainty wrapping Magnitude; then `Entry (... Certainty ...)` uses Certainty in field position.

Under intent 631:
- The struct USING Certainty: `Entry [Topic Kind Summary Context Certainty Quote]` (struct → `[]`)
- The NEWTYPE DECLARATION `Certainty (Magnitude)` — newtype is a single-tagged-variant → `()` ✓

So newtypes use `()`. Newtype declarations look exactly like enum-variants because they ARE single-tagged-variant forms.

```nota
Topic (String)                ; newtype Topic wrapping String
Certainty (Magnitude)         ; newtype Certainty wrapping Magnitude
RecordIdentifier (u64)        ; newtype RecordIdentifier wrapping u64
```

This matches intent 616 (everything-reduces-to-structs): a newtype IS a struct with one field. But the bracket-swap reading: a newtype is also structurally a single-tagged variant (tag = newtype name; payload = inner type). The `()` bracket captures the tagged-variant character.

**Reconciling 616 vs 631 on newtypes**: a newtype is BOTH a struct-with-one-field AND a tagged-variant-with-one-payload. The bracket `()` per intent 631 captures the tagged-variant view. The struct-with-one-field reading (intent 616) is true at the Rust emission level — emitted Rust is `pub struct Topic(pub String)` (a one-tuple-field struct). Both views are valid; the bracket honors the tagged-variant view because it disambiguates from multi-field structs.

### §4.3 Enum data-carrying variants (intent 616)

Per intent 616: data-carrying enum variants are STRUCTS — the data-carrying portion IS the struct shape.

Under intent 631: a data-carrying enum variant `(Foo Type1 Type2)` is the enum-variant tag `Foo` with payload `(Type1 Type2)`. But the PAYLOAD itself, structurally, is a struct of two fields. So:

```nota
RecordQuery (Foo [Type1 Type2])     ; enum-variant Foo carries a struct of 2 fields
```

vs

```nota
RecordQuery (Foo Type1 Type2)       ; same? or different?
```

**Genuine ambiguity**: when a tagged-variant carries multiple values, are they SEPARATE positional arguments (Foo + arg1 + arg2 as flat tuple) OR a single struct payload `[Type1 Type2]`?

I think the cleaner reading is: a tagged-variant always has a SINGLE PAYLOAD which is a struct. If the payload is a single primitive, you can elide the wrapper. So:

```nota
(Foo Type1 Type2)               ; same as (Foo [Type1 Type2]) — implicit struct wrapper
(Foo [Type1 Type2])             ; explicit struct wrapper
```

Per intent 616 (everything-reduces-to-structs), the IMPLICIT struct wrapper is fine — `(Tag value1 value2)` is short-syntax for `(Tag [value1 value2])`. The structure-match recognizer dispatches based on whether the payload position is itself a single struct or a flat-list-of-values.

## §5 Container expressions — the genuine open question

Under /326-v13:
```nota
(Option Topic)     ; container expression with paren
(Vec RecordSummary)
(Map Identifier Path)
```

These use `()` per intent 485 (container types use parens, not brackets).

Under intent 631:
- `(Option Topic)` — Option is a tagged variant (Some+None form); the SHAPE is enum-variant-like → `()` ✓
- `(Vec T)` — Vec is a single-tagged form (the tag is "Vec"; payload is T) — enum-variant-like? OR is Vec STRUCTURALLY a struct-with-one-Vec-field? Per intent 616, Vec is a struct with single field.
- `(Map K V)` — Map is a tagged form with two payload positions — enum-variant-like with multi-arg payload (like (Foo Type1 Type2))

The question: does `(Vec T)` stay `()` (current) under intent 631, or become `[Vec T]` (since Vec is structurally a struct-with-one-field per intent 616)?

**Reading A — `(Vec T)` stays `()`**: container expressions are TAGGED-VARIANT shapes (tag + payload). Vec is a tagged variant of the TypeExpression enum (alongside Named, Option, Map, Primitive). Under intent 631, enum-variants use `()`. So `(Vec T)` stays unchanged.

**Reading B — `(Vec T)` becomes `[Vec T]`**: at the structural level, Vec IS a struct with one field. Per intent 616 (everything-reduces-to-structs), all container expressions are structs. Under intent 631, structs use `[]`. So container expressions become `[Vec T]`, `[Option Topic]`, `[Map K V]`.

But Reading B reverses /326-v10 + intent 485 ("container types use parens, not brackets"). That intent explicitly chose `()` for containers. Reading B would re-reverse it.

**Lean: Reading A — `()` for container expressions stays.** Containers ARE structurally tagged variants of TypeExpression (Named/Option/Vec/Map/Primitive); intent 485 said `()` for containers; intent 631's enum-variant `()` rule confirms it. Intent 616's "everything-reduces-to-structs" is true at the RUST EMISSION level (the emitted Rust is a struct), but at the SCHEMA SYNTAX level the container is a TypeExpression variant — enum-variant-shaped — so `()` per intent 631 + 485.

**Open psyche question**: confirm Reading A (containers stay `()`) or Reading B (containers become `[]`).

## §6 Implications for operator's landings

### §6.1 `nota-codec` (operator/187 + /181 + /190)

The `NotaValue` enum + `NotaValueKind { Record, Sequence, Map, Identifier, ... }` doesn't change — these are STRUCTURAL categories (record = parens; sequence = brackets; map = curly). Intent 631 doesn't change the parser; it changes the SEMANTIC INTERPRETATION at higher layers.

Shape predicates (`is_record`, `is_sequence`, `is_map`, `record_arity`, etc.) stay valid; they ask structural questions. The DISPATCH layer (which higher-layer concept each NotaValue maps to) changes: under /326-v13, `is_sequence` → enum variants list (often); under intent 631, `is_sequence` → struct fields list.

**No code changes to nota-codec.** Only the dispatcher's interpretation rules change.

### §6.2 `schema` crate (operator/180 + /181 + /190 + /182)

- `NodeDefinitionShape` enum (per operator/182): unchanged at the type level
- `NamespaceValueShape::{Enum, Record, Newtype, Alias}`: unchanged at the type level
- But the RECOGNIZER changes: the structure-match macro now classifies `[...]` as `Record` (struct) and `(...)` with multi-element as `Enum`. The OLD recognizer did the opposite. The single-element disambiguator stays: `(SingleType)` is `Newtype`; `[(field-or-element)]` arity check determines struct-vs-enum-variant-list.

**Code change scope**: recognizer arms in `node_shape.rs` / `multi_pass.rs` / `shape_parser.rs` need flipping. Tests need updating. The PUBLIC TYPES stay the same; the IMPLEMENTATION of recognition flips.

### §6.3 Schema fixtures

Every `.schema` file in the workspace (~75 concept schemas per operator/175) needs migration. Mechanical but extensive:
- `[VariantA VariantB VariantC]` → `(VariantA VariantB VariantC)` for enums
- `(field-type1 field-type2 ...)` → `[field-type1 field-type2 ...]` for structs (under intent 614 the field types are positional type-names; field names lowercase-derive)
- Header positions stay `[(Root [Sub]) ...]` — both reads work

Test fixtures + production `.schema` files all migrate. Per /193 §13: dual-witness ensures no semantic drift during migration; the engine produces same AssembledSchema both before + after.

### §6.4 The `Schema::parse_str` flip (per operator/181)

Operator/181 flipped the canonical parser to the NotaValue path. Under intent 631, both paths need updating to honor the new bracket interpretation. Dual-witness still catches divergence.

## §7 Why intent 631 is the right move

Three reasons it's worth the substantial migration:

1. **Structural self-documentation**: brackets carry semantic weight — see `[`, expect struct; see `(`, expect enum-variant. Reading a schema becomes faster + less ambiguous.

2. **Aligns with computer-first interface (per intent 533+ patterns)**: structural correspondence between syntax and semantics is the workspace's aesthetic. `[]` = vector-shape = struct-shape; `()` = grouping = variant-shape. The bracket choice IS the type information at the syntax level.

3. **Resolves the enum-vs-struct ambiguity from /189 §8**: under /326-v13, `Watch [State Records Questions]` and `Watch ((state StateSubscription) ...)` both started with brackets-then-records, requiring inner-element inspection to disambiguate enum-vs-struct. Under intent 631, `Watch (State Records Questions)` is unambiguously an enum (parens); `Watch [Type1 Type2 Type3]` is unambiguously a struct (brackets). Disambiguation moves to the bracket level; structure-match becomes simpler.

The trade-off: migration cost. ~75 concept schemas + production fixtures + recognizer code + tests. Per intent 503 (mockups beat reports for integration) + the dual-witness pattern, migration is mechanical + verifiable.

## §8 Concrete Spirit migration under combined intent 614+615+616+631

Putting all four intents together — Spirit's namespace section becomes:

```nota
{
  Magnitude (ImportAll ../signal-sema/magnitude.schema)            ; ImportDirective enum-variant — ()
  SemaSet (Import ../signal-sema/sema.schema (SemaOperation SemaOutcome))   ; Import variant; names list per intent 631 enum-of-names — ()
}

(                                                                  ; ordinary header position (struct of header-roots — but psyche reading is sequence — discuss)
  (State (Statement))                                              ; header-root State, sub-variants list (Statement) — enum
  (Record (Entry))
  (Observe (Observation))
  (Watch (Subscription))
  (Unwatch (SubscriptionToken))
)

()                                                                 ; owner header — empty
()                                                                 ; sema header — empty

{                                                                  ; namespace map
  Kind (Decision Principle Correction Clarification Constraint)    ; ENUM — ()
  ObservationMode (SummaryOnly WithProvenance)                     ; ENUM — ()
  Presence (Active Absent)                                         ; ENUM
  UnimplementedReason (NotBuiltYet IntegrationNotLanded)           ; ENUM

  Topic (String)                                                   ; newtype — single-tagged → ()
  Summary (String)
  Context (String)
  Quote (String)
  StatementText (String)
  FocusArea (String)
  RecordIdentifier (u64)
  QuestionIdentifier (String)
  QuestionText (String)
  StateSubscriptionToken (u64)
  RecordSubscriptionToken (u64)
  Certainty (Magnitude)                                            ; newtype per intent 615
  Identifier (RecordIdentifier)
  Mode (ObservationMode)
  Text (StatementText)

  Entry [Topic Kind Summary Context Certainty Quote]               ; STRUCT — [] per intent 631
  Statement [Text]                                                 ; STRUCT with one field; per intent 616 also a struct
  RecordQuery [(Option Topic) (Option Kind) Mode]                  ; STRUCT with container-typed fields; containers stay () per §5 Reading A
  RecordSummary [Identifier Topic Kind Summary Certainty]
  ...
}

(                                                                  ; features position — outer container
  (Reply [RecordAccepted StateObserved ...])                       ; Reply feature-variant carries struct of reply types
  (Event [StateChanged RecordCaptured])
  (Observable Default OperationReceived EffectEmitted)
)
```

Big shape changes vs current:
- Enums flip from `[]` to `()` — every enum declaration
- Structs flip from `((field Type) ...)` to `[Type1 Type2 ...]` — every record declaration
- Newtypes stay `()` — symmetric with enum-variant character
- Container expressions stay `()` per §5 lean — TypeExpression variants
- Header sub-variants flip from `[Sub]` to `(Sub)` — sub-variants are enum-of-roots
- Headers position outer might flip from `[(Root ...)]` to `((Root ...))` OR stay `[(Root ...)]` depending on whether header-position is structurally struct (all roots positional) or enum (one-of) — **genuine open question**
- Features position similarly — likely struct (all features declared) → stays `[]`; or enum (one-of feature) → `()`. Lean: STRUCT — all features declared positionally. **Open**.

## §9 Open psyche questions

After applying intent 631 + 614 + 615 + 616 with leans, these genuine uncertainties remain:

1. **Header-position outer bracket** — struct of header-root declarations (`[]`) or enum-of-root-variants (`()`)? Lean: struct since all roots are positionally declared. Per §3.2 Reading A.

2. **Features-position outer bracket** — same question. Lean: struct (`[]`) since all features positionally declared.

3. **Container expressions** — stay `()` per intent 485 (lean A in §5) or flip to `[]` per intent 616 struct-reduction (Reading B)? Lean: stay `()` — containers are TypeExpression enum-variants at the schema layer.

4. **Implicit-struct-wrap for tagged-variant payloads** — `(Tag value1 value2)` short-syntax for `(Tag [value1 value2])`? Or always explicit `(Tag [value1 value2])`? Lean: implicit wrap allowed; explicit also valid (long form). Recognizer accepts both.

5. **Sub-variant lists in headers** — `(State (Statement Reflection Declaration))` (enum of sub-variants) or `(State [Statement Reflection Declaration])` (struct of sub-variants)? Lean: enum (`()`) — sub-variants ARE enum variants of the root's sub-enum.

## §10 Migration impact summary

| Concern | Migration shape |
|---|---|
| `nota-codec` types + predicates | NONE — structural categories unchanged |
| `schema` recognizer arms | FLIP (`is_sequence` now means struct; `is_record` with multi-args now means enum) |
| `NodeDefinitionShape` + `NamespaceValueShape` types | UNCHANGED — only the recognition rule flips |
| `MacroIndex` + `MacroPipeline` structure | UNCHANGED |
| Spirit fixture | RE-AUTHOR per §8 — significant shape change in namespace + minor in headers |
| Orchestrate + signal-version-handover fixtures | RE-AUTHOR per same pattern |
| ~75 concept schemas across workspace | RE-AUTHOR — mechanical |
| Dual-witness tests (per operator/181 §"Test View") | UPDATE both paths together; assertion catches drift |
| AssembledSchema output | UNCHANGED — semantic content is the same; only syntax differs |
| Brilliant macro library emission | UNCHANGED — emits from AssembledSchema |
| /193 field-naming rule | COMPOSES cleanly with intent 631 — field names still type-name-derived, just in `[]` bracket |
| Operator/180 `SchemaField { name, schema_type }` | STAYS REVERSED (per intent 614 — no explicit field names) |

The migration is INVASIVE at the schema-syntax level + recognizer-implementation level; OPAQUE at the AssembledSchema + emission levels (AssembledSchema doesn't see syntax — it holds the semantic content).

## §11 Recommended sequencing

1. **Settle the 5 open questions from §9** (psyche call): header outer bracket, features outer bracket, container expressions, implicit-struct-wrap, sub-variant lists. Each unblocks the migration design.
2. **Update `node_shape.rs` recognizer arms** in `schema` crate — flip the recognition rules per intent 631. Tests will fail initially against existing fixtures.
3. **Migrate Spirit's `spirit.schema`** to new bracket convention. Dual-witness asserts shape parser + streaming parser BOTH produce same AssembledSchema as before — semantic invariant under syntactic change.
4. **Migrate orchestrate + version-handover schemas** similarly.
5. **Migrate the 75 concept schemas** across the workspace — mechanical sed-like pass + per-file verification.
6. **Update `ARCHITECTURE.md` + `skills/nota-design.md`** to document the bracket convention.
7. **Adopt as standard going forward** — every new `.schema` file uses intent 631 brackets from day one.

Estimated effort: ~1 operator session for code changes (recognizer flip + tests); ~1-2 sessions for fixture migration; ~1 session for the 75 concept schemas + docs.

## §12 What this audit does NOT do

- Does NOT block the current substrate from running — production still works on /326-v13 convention; migration is a separate slice
- Does NOT propose new design beyond the bracket-swap; field-naming + newtype-for-divergence + everything-reduces-to-structs stay valid (just inside the new bracket convention)
- Does NOT block designer/338's vision — /338's content still holds; only the bracket-level syntax revises

## §13 References

- `reports/designer/338-schema-engine-refreshed-vision-2026-05-25.md` — the vision report this reverses bracket-syntax in
- `reports/second-designer/193-field-naming-and-module-output-2026-05-25.md` — field-naming rule (composes with intent 631)
- `reports/second-designer/189-macro-system-broader-understanding-2026-05-25.md` §8 — enum-vs-struct ambiguity case (resolved at bracket level by intent 631)
- `reports/second-designer/192-audit-operator-182-second-operator-schema-node-shape-2026-05-25.md` — NodeDefinitionShape boundary (recognizer arms need flipping but type stays)
- `reports/second-designer/191-audit-second-operator-190-schema-mainline-macro-index-port-2026-05-25.md` — MacroIndex + TypeMicroMacro (substrate unchanged; recognition rule flips)
- `reports/second-designer/188-schema-engine-running-walkthrough-2026-05-25.md` — engine walkthrough (rerun under intent 631 brackets)
- `reports/operator/181-fully-schema-and-nota-mvp-2026-05-25/` — Schema::parse_str flip (still works; rule-flip in same place)
- `reports/operator/182-second-operator-schema-node-shape-audit-2026-05-25.md` — NodeDefinitionShape correction (types unchanged; recognizer arms flip)
- `reports/designer/326-v13-spirit-complete-schema-vision.md` — the bracket convention being reversed
- `/git/github.com/LiGoldragon/schema/` main — implementation that needs recognizer-flip
- `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema` — fixture needing migration per §8
- Intent records 485 (container types use parens — stays per §5 lean), 494 (uniform header form), 506 (data-carrying macro variants), 569 (iterative-to-fixed-point), 614 (field-names-derived-from-type-names), 615 (divergent-field-names-via-newtype), 616 (everything-reduces-to-structs), 620 (module-per-schema), 621 (fully-qualified-names), 631 (bracket-swap THIS report)
