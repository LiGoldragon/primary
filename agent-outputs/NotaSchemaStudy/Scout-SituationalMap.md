# NOTA Schema Study Situational Map

## Task And Scope

Read-only study for a future reusable agent skill about NOTA and schema. Scope was `/home/li/primary`, generated local skills, and relevant LiGoldragon repositories under `/git/github.com/LiGoldragon` surfaced by local guidance and search. No implementation changes were made. The only written artifact is this report.

The study focused on existing NOTA/schema doctrine and the current work around schema help outputs that print type names positionally for a schema, value instance, or schema node.

## Commands And Sources Consulted

Commands used included:

- `sed -n` on `/home/li/primary/AGENTS.md`, the generated skills, and relevant docs/source files.
- `spirit "(PublicTextSearch ...)"` and `spirit "(Lookup w312)"` for public read-only intent grounding.
- `rg --files` and `find /git/github.com/LiGoldragon -maxdepth 3 ...` to locate schema/NOTA surfaces.
- `rg -n "InstanceSchemaText|HelpRequest|HelpModel|TypeReference|OptionalVariantPayload|..."` across `schema-next`, `nota-next`, and `signal-spirit`.
- `test -e /git/github.com/LiGoldragon/schema-next/src/help.rs` to confirm the planned `schema-next` help module is absent on the inspected checkout.

Primary files inspected:

- Local startup/guidance:
  - `/home/li/primary/AGENTS.md`
  - `/home/li/primary/.agents/skills/nota-design/SKILL.md`
  - `/home/li/primary/.agents/skills/nota-schema-docs/SKILL.md`
  - `/home/li/primary/.agents/skills/spirit-query/SKILL.md`
- Skills repo source:
  - `/git/github.com/LiGoldragon/skills/modules/nota-design/full.md`
  - `/git/github.com/LiGoldragon/skills/modules/nota-schema-docs/full.md`
  - `/git/github.com/LiGoldragon/skills/modules/spirit-cli/full.md` surfaced by search, not deeply studied beyond the NOTA rule match.
- Core NOTA/schema repos:
  - `/git/github.com/LiGoldragon/nota-next/ARCHITECTURE.md`
  - `/git/github.com/LiGoldragon/nota-next/src/instance_schema.rs`
  - `/git/github.com/LiGoldragon/schema-next/ARCHITECTURE.md`
  - `/git/github.com/LiGoldragon/schema-next/README.md`
  - `/git/github.com/LiGoldragon/schema-next/src/instance.rs`
  - `/git/github.com/LiGoldragon/schema-next/src/schema.rs`
  - `/git/github.com/LiGoldragon/schema-next/src/source.rs`
  - `/git/github.com/LiGoldragon/schema-next/src/engine.rs`
  - `/git/github.com/LiGoldragon/schema-next/tests/instance_schema_render.rs`
  - `/git/github.com/LiGoldragon/schema-next/tests/specified_schema.rs`
  - `/git/github.com/LiGoldragon/schema-next/tests/raw_core_schema.rs`
  - `/git/github.com/LiGoldragon/schema-next/schemas/core.schema`
  - `/git/github.com/LiGoldragon/schema-next/schemas/reference-grammar.nota`
- Help implementation and tests:
  - `/git/github.com/LiGoldragon/signal-spirit/src/help.rs`
  - `/git/github.com/LiGoldragon/signal-spirit/src/lib.rs`
  - `/git/github.com/LiGoldragon/signal-spirit/tests/generated_contract.rs`
  - `/git/github.com/LiGoldragon/signal-spirit/tests/help_instance_schema_convergence.rs`
  - `/git/github.com/LiGoldragon/signal-spirit/tests/instance_schema.rs`
  - `/git/github.com/LiGoldragon/signal-spirit/schema/signal.schema`
  - `/git/github.com/LiGoldragon/signal-spirit/schema/domain.schema`
- Editor grammar:
  - `/git/github.com/LiGoldragon/tree-sitter-schema/README.md`
  - `/git/github.com/LiGoldragon/tree-sitter-schema/grammar.js`
- Prior local reports, used as non-authoritative background and checked against code:
  - `/home/li/primary/reports/schema-designer/25-schema-self-describing-design.md`
  - `/home/li/primary/agent-outputs/NotaStrictPositional/SchemaSyntax.md`
  - `/home/li/primary/reports/legacy-disposition/SITUATION-2026-06-30-parked-spirit-tracks.md`

Not checked:

- No `/nix/store` search.
- No private repos.
- No branch checkout or raw git history inspection. A prior report mentions a held `schema-help` branch, but this study did not inspect branch commits.
- No tests were run; the task was source study.

## Spirit Grounding

Public Spirit query found `w312`, a Technology/Software/Engineering Architecture principle: deterministic routing, dispatch, lookup, classification, projection, address resolution, and schema-derived mechanics should live in code or schema-derived machinery rather than agent judgment. This supports the future skill’s emphasis: agents should learn to read schema and help outputs, but mechanical schema interpretation should be delegated to schema/code when available.

Searches for `[schema help type names positional]` also returned `qvb3`, a codec constraint: structured data must use the canonical shared codec, not hand-rolled per-type encoding/decoding. That matches the code comments in `schema-next/src/instance.rs` and `signal-spirit/src/help.rs`.

## Observed Facts

### Raw NOTA Layer

`nota-next/ARCHITECTURE.md` says NOTA is the raw structural floor. It parses delimiter-balanced objects and exposes structural predicates, root-object queries, spans, and structural candidate classification; it does not decide schema semantics. Schema assigns meaning above raw NOTA.

The raw grammar includes atoms, parenthesized records, square vectors, brace maps, pipe text, pipe parenthesis, pipe brace, and `;;` comments. `nota-design` repeats this compactly and adds the discipline: records are positional, field order is part of the interface, stable identifiers and canonical names should be bare atoms, and machine data belongs in records rather than comments.

`nota-next/ARCHITECTURE.md` also states that bare atoms are the default string form, and bracket/pipe text forms are for whitespace, delimiters, prose, comments, close markers, or newlines. This matters for LLM prompts: models should not invent JSON quoting, markdown fences, or double-quoted strings when a bare atom is valid.

### Authored `.schema` Layer

`schema-next/README.md` and `schema-next/ARCHITECTURE.md` agree on the split: a `.schema` file must parse as legal NOTA first, then schema-specific reading lowers it to typed schema source data and then semantic `Schema`.

The active schema examples use these root objects:

- optional imports brace map;
- input root enum vector;
- output root enum vector;
- namespace brace map;
- optional relations vector in some files.

Examples:

- `signal-spirit/schema/signal.schema` starts with an imports map, then input and output vectors, then a namespace map.
- `signal-spirit/schema/domain.schema` uses empty imports and root vectors, then a namespace map, then a relations vector.
- `schema-next/schemas/core.schema` is a raw-core single-map schema fixture and is intentionally a different bootstrap shape; `schema-next/tests/raw_core_schema.rs` proves the root name comes from the filename and the root object must be an even-entry map.

Current source evidence in `schema-next/src/source.rs` and `schema-next/src/engine.rs` says struct bodies are positional field-type lists. Legal field forms include:

- `TypeName` when the field role derives from the type name;
- `fieldName.TypeName` when the field role differs from the type;
- `fieldName.(Optional TypeName)` or another `fieldName.(Composite ...)` form when the type reference is parenthesized.

The error text in `schema-next/src/engine.rs` says retired struct field syntax should use `TypeName` or `field_name.TypeName`. `schema-next/src/source.rs` raises `RetiredStructFieldSyntax` for older pair-like forms and `RedundantExplicitFieldRole` when the explicit role only repeats the type-derived name.

There is a documentation/version skew to handle carefully:

- `schema-next/README.md` still describes an older strict key/value body surface with examples such as `Topic String` and `Topics *`.
- `tree-sitter-schema/README.md` and `grammar.js` accept older aliases and forms for editor tolerance: `Vec`, `Option`, `Scope`, `KeyValue`, explicit `field value`, and `*`.
- The lowering source and live schemas inspected use the stricter positional/dot syntax. The future skill should teach the enforced source/lowering rule, and mention editor grammar as tolerant rather than authoritative.

### Type Reference Vocabulary

`schema-next/src/schema.rs` defines semantic `TypeReference` with:

- scalar leaves: `String`, `Integer`, `Boolean`, `Path`, `Bytes`;
- fixed byte source form as `(Bytes N)`, semantic codec variant as `FixedBytes(N)`;
- declared-name leaf: `Plain(Name)`;
- composites: `Vector`, `Map`, `Optional`, `ScopeOf`;
- generic `Application { head, arguments }`.

`schema-next/schemas/reference-grammar.nota` gives the parenthesis-reference dispatch precedence as data: built-in heads `Vector`, `Optional`, `ScopeOf`, `Map`, `Bytes`, then declared macro, then generic application. It explicitly says to edit the grammar and regenerate, not hand-edit the generated resolver.

`nota-next/src/instance_schema.rs` has a different, instance-local `TypeReference`: `Named(&'static str)`, `Vector`, `Optional`, `Map`, `FixedBytes(usize)`. Its traced scalar impls emit `Named("String")`, `Named("Integer")`, `Named("SignedInteger")`, `Named("Float")`, and `Named("Boolean")`; byte sequence emits `Named("Bytes")`. This is one of the known vocabulary mismatches called out in the self-describing-schema report.

### Optional Rule

Settled doctrine and code agree:

- `nota-design` says never place `(Optional T)` in a positional or variant-payload slot; every positional component and every variant payload always appears in text.
- `(Optional T)` is legal as a named brace-record field when absence means something distinct from empty.
- `schema-next/src/schema.rs` rejects enum variant payloads matching `TypeReference::Optional(_)` with `SchemaError::OptionalVariantPayload`.
- `schema-next/src/engine.rs` error text says a variant payload must always appear in the text form and recommends modeling the optional case as an explicit member carrying a required payload.

Live legal examples:

- `signal-spirit/schema/signal.schema`: `VerbatimQuote { QuoteText OptionalAntecedent.(Optional Antecedent) }`
- `signal-spirit/schema/signal.schema`: several configuration fields use `Name.(Optional Type)` inside struct bodies.

### Pseudo-NOTA Documentation

`nota-schema-docs` is intentionally a documentation convention, not the authoritative wire shape. It teaches angle-bracket placeholders, `?` suffixes for optional fields in docs, `|` for closed enum alternatives, square brackets for lists, and `;;` comment lines for field types or constraints.

This should stay separate in the future skill: pseudo-NOTA is useful when a reader needs named fields in markdown, but the schema source and round-trip examples own truth.

## What Schema Help Output Currently Does

There are two implemented help-like surfaces and one planned but absent generic surface.

### `schema-next::InstanceSchemaText`

Implemented in `/git/github.com/LiGoldragon/schema-next/src/instance.rs`, re-exported from `schema-next/src/lib.rs`.

Purpose: render the per-instance schema trace captured by `nota-next::NotaDecodeTraced`. It is value-instance based, not pure type-level schema help. It records the type the decoder expected at each position while decoding a real value. It then projects the trace through `schema-next::SourceReference::from_instance_reference(...).rendered_schema_text()`, so reference tokens use the schema encoder rather than a hand-written schema printer.

Two projections:

- `aligned()`: one reference token per value position. Structs render as brace groups of field type names. Enums render as the enum name plus the realized payload reference one level in. Transparent variant payload wrappers are collapsed.
- `expanded()`: recursively expands the realized value’s schema all the way down, still only for the realized instance path.

Examples asserted in `schema-next/tests/instance_schema_render.rs`:

- `Kind::Decision` renders `Kind` in both aligned and expanded forms.
- An `Entry` value renders aligned as `{ Domains Kind Description Certainty Importance Privacy Referents }`.
- `DomainMatch::Partial(...)` renders aligned as `(DomainMatch DomainScopes)`.
- Empty `Domains` renders aligned as `Domains` and expanded as `(Domains (Vector Domain))`.
- Root `Input::Record(...)` renders aligned as `(Input ({ Domains Kind Description Certainty Importance Privacy Referents } { Testimony Reasoning }))`.
- `Certainty(High)` renders aligned as `Certainty` and expanded as `(Certainty Magnitude)`.

Important limitation: this is not type-level fan-out. For an enum it can show only the variant realized by the decoded value, because `InstanceSchemaBody::EnumPayload` contains only the chosen payload. It cannot show all variants of a type without a schema declaration graph.

### `signal-spirit::HelpModel`

Implemented in `/git/github.com/LiGoldragon/signal-spirit/src/help.rs`, re-exported from `signal-spirit/src/lib.rs`.

Purpose: help as a thin view over `schema`'s fully specified schema IR for signal-spirit’s own deployed schema sources. It stores `SpecifiedSchema` values. It renders help by projecting schema declarations through schema's declaration codec. The comments explicitly say there is no separate help language, no hand `format!` printer, and no parallel decoder.

Request parsing:

- `HelpRequest::from_text("(Help)")` recognizes top-level help.
- `HelpRequest::from_text("(Help Entry)")` recognizes named help.
- Non-help input such as `Version` returns `None`, leaving it for generated input parsing.

Render behavior:

- Top-level help returns root entries.
- Named help searches roots and nodes and returns one `HelpEntry`.
- Help output is canonical schema text. `HelpResponse::to_schema_text()` and `HelpResponse::from_schema_text()` round-trip through `SourceDeclarations`, not a help-specific codec.

Examples asserted in `signal-spirit/tests/generated_contract.rs`:

- `(Help Record)` renders `(Record { Entry Justification })`.
- `(Help Entry)` renders `(Entry { Domains Kind Description Certainty Importance Privacy Referents })`.
- `(Help Domains)` renders `(Domains (Vector Domain))`.
- `(Help Description)` renders `(Description String)`.
- `(Help DomainMatch)` renders `(DomainMatch [Any (Partial) (Full)])`.
- `(Help IntentEventStream)` renders `(IntentEventStream (Stream { token.SubscriptionToken opened.SubscriptionStarted event.IntentEvent close.SubscriptionToken }))`.

`signal-spirit/tests/help_instance_schema_convergence.rs` proves one convergence point: `HelpModel` for `Domains` renders `(Domains (Vector Domain))`, and the per-instance schema expansion for an empty `Domains` value renders the same string.

Important limitation: this is signal-spirit-local, not a generic `schema-next::SchemaHelp` API. A prior local report notes deployed `spirit "(Help)"` rejected help at that time; this study did not re-run that CLI probe because allowed Spirit operations for this worker were read-only query operations. Treat CLI availability as unverified/currently risky.

### Planned `schema-next::SchemaHelp`

`/home/li/primary/reports/schema-designer/25-schema-self-describing-design.md` lays out a planned generic type-level help renderer: `schema-next/src/help.rs`, `SchemaHelp`, `HelpDepth`, `TypeHelpNode`, and `HelpVariant`.

That report says the help renderer should:

- live on the schema/type-definition side, not with instance data;
- render schema's own self-descriptive notation from structure, not authored prose;
- use position name plus type name plus recursion into referenced type;
- use a structured tree (`TypeHelpNode`) with a text projection;
- fan out all enum variants at type level;
- guard recursive expansion with depth or a visited-type set.

Current checkout evidence:

- `schema-next/src/help.rs` does not exist (`test -e` returned nonzero).
- `rg` finds no `SchemaHelp`, `HelpDepth`, `TypeHelpNode`, or `HelpVariant` in `schema-next/src`.

So the planned generic surface is design guidance, not implemented on the inspected main checkout.

## Settled Doctrine Versus Implementation Detail Versus Open Items

Settled doctrine:

- NOTA is structural data; schema/codec layers assign meaning.
- Records and struct/value components are positional; field order is part of the interface.
- Bare atoms are preferred for stable identifiers, enum-like values, and canonical names.
- Comments are not machine data.
- Encode/decode through canonical shared codec paths; avoid hand-rolled per-type parsing/rendering.
- `(Optional T)` is forbidden as enum payload and should not be used in positional slots; use explicit variants or named fields.
- Pseudo-NOTA docs are only documentation; schema and round-trip examples own truth.

Implemented details that a skill should describe as current behavior:

- `InstanceSchemaText` is per-instance and has `aligned()` and `expanded()` projections.
- `signal-spirit::HelpModel` renders one-level declaration help for its schema sources and round-trips through the schema declaration codec.
- Current source lowering uses positional struct fields with dot-bound explicit roles; older pair forms are retired.
- `schema-next` semantic `TypeReference` and `nota-next` instance-local `TypeReference` are still separate vocabularies.

Open or ambiguous:

- The generic `schema-next::SchemaHelp` design is not implemented on the inspected checkout.
- The self-describing-schema report calls for Decision A: store canonical schema-form field names such as `createdAt` and derive snake_case at Rust emit time. Current `schema-next/src/source.rs` still lowers field names with `self.name.field_name()`, so the migration is not landed here.
- `SourceReference::derived_field_name()` still synthesizes snake_case names such as `optional_x`, `x_by_y`, and `work_vector`; the report flags this as an open policy question for help rendering and identity.
- The instance/schema type-reference mismatch remains: instance tracing can name `SignedInteger` and `Float`; semantic schema has `Path` and dedicated `Bytes`/`FixedBytes`, but no dedicated `SignedInteger`/`Float` variants.
- `tree-sitter-schema` accepts aliases and older forms for editor compatibility; source lowering is stricter. The future skill must not treat editor grammar tolerance as canonical schema doctrine.
- Help CLI availability in deployed `spirit` should be rechecked before telling agents to invoke `(Help)` against a live component.

## Future Skill Content Recommendation

Create one reusable skill that augments or replaces the current small `nota-design` plus `nota-schema-docs` pair. Suggested name: `nota-schema-reading`.

Recommended sections:

1. Layer Model
   - Teach raw NOTA, authored `.schema`, semantic schema IR, generated codec, per-instance schema trace, and help projection as separate layers.
   - State that the same NOTA text can mean different things under different schemas.

2. Raw NOTA Syntax
   - Atoms; parenthesized records; square vectors; brace maps; bracket strings; pipe text; pipe parenthesis/brace; `;;` comments.
   - Bare atoms for canonical strings and enum-like values.
   - No markdown fences, JSON quoting, or prose outside the requested NOTA expression.

3. Positionality
   - Records are positional.
   - Every positional component appears.
   - Field order is compatibility-significant.
   - Schema names positions; values do not carry field names.

4. Authored `.schema` Reading
   - Module root shape: imports, input enum, output enum, namespace, optional relations.
   - Struct field forms: `TypeName`, `fieldName.TypeName`, `fieldName.(Optional TypeName)`, `fieldName.(Vector TypeName)`.
   - Explicit dot role should appear only when the role differs from the type-derived role.
   - Enum forms: `Unit`, `(Variant Payload)`, `(Variant)`, and advanced stream relation variants.
   - Type-reference forms: `Vector`, `Optional`, `ScopeOf`, `Map`, `(Bytes N)`, generic application.
   - Mention that `FixedBytes` is the semantic codec name while `(Bytes N)` is the source syntax.

5. Optionality
   - Legal: named struct field `role.(Optional Type)`.
   - Forbidden: enum payload `(Variant (Optional T))` and positional slots that can collapse or disappear.
   - Model absence as explicit variants or named fields.

6. Help Output Reading
   - Explain `InstanceSchemaText::aligned` and `expanded`, with examples from tests.
   - Explain `signal-spirit` Help as one-level declaration projection, with examples.
   - Warn that generic `schema-next::SchemaHelp` is planned but absent on inspected main.
   - Teach agents to prefer schema/help output over inference when available.

7. Pseudo-NOTA Documentation
   - Keep the existing `nota-schema-docs` convention, but label it as markdown explanation only.
   - Include one concise example with placeholders and a field type list.

8. Source References For Fresh Agents
   - Cite:
     - `nota-next/ARCHITECTURE.md`
     - `schema-next/ARCHITECTURE.md`
     - `schema-next/src/source.rs`
     - `schema-next/src/schema.rs`
     - `schema-next/src/engine.rs`
     - `schema-next/src/instance.rs`
     - `nota-next/src/instance_schema.rs`
     - `signal-spirit/src/help.rs`
     - `signal-spirit/tests/generated_contract.rs`
     - `signal-spirit/tests/help_instance_schema_convergence.rs`
     - `schema-next/schemas/reference-grammar.nota`

Recommended examples to embed:

```nota
(Entry { Domains Kind Description Certainty Importance Privacy Referents })
(Domains (Vector Domain))
(DomainMatch [Any (Partial) (Full)])
(Input ({ Domains Kind Description Certainty Importance Privacy Referents } { Testimony Reasoning }))
```

```schema
VerbatimQuote { QuoteText OptionalAntecedent.(Optional Antecedent) }
Entry { Domains Kind Description Certainty Importance Privacy Referents }
DomainMatch [Any (Partial) (Full)]
IntentEventStream (Stream { token.SubscriptionToken opened.SubscriptionStarted event.IntentEvent close.SubscriptionToken })
```

Anti-patterns the skill should forbid:

- Inferring schema meaning from raw NOTA delimiters without the expected schema/type.
- Omitting positional fields because a value is optional.
- Using `(Optional T)` as an enum payload.
- Writing retired struct field pairs such as `(field Type)` or `field Type` where current lowering expects `field.Type` or a bare derived `Type`.
- Treating `Vec`, `Option`, `Scope`, or `KeyValue` aliases as canonical just because editor grammar accepts them.
- Using maps to dodge a named record shape.
- Putting machine-readable values in `;;` comments.
- Hand-rendering or hand-parsing schema/help text instead of using `SourceReference`, `SourceDeclarations`, or canonical codec surfaces.
- Treating pseudo-NOTA docs as wire truth.
- Assuming `(Help)` is wired into every deployed CLI.
- Treating `InstanceSchemaText` as full type-level help; it only knows the realized value path.

## Follow-Up Requirements Before Writing The Skill

- Decide whether to merge this into `nota-design`, replace `nota-schema-docs`, or create a new skill that both existing skills point to.
- Recheck the current target branch for `schema-next/src/help.rs` or a landed `SchemaHelp` before writing "planned" language.
- Recheck deployed component CLI support for `(Help)` if the skill will instruct agents to invoke help on live CLIs.
- Resolve how strongly to mention Decision A field-name migration. The design report treats it as locked direction, but the inspected source has not landed it.
- If the skill is edited in `LiGoldragon/skills`, follow skill-edit/generated-output workflow rather than editing generated `.agents` copies directly.
