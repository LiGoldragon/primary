# 354 — Schema-derived NOTA prototype

*Designer-assistant implementation of the prototype defined by `/353` and intent records 746-753 (Maximum). Empirical proof that NOTA itself can be schema-derived, that schema is the interpretation engine for the delimiter language, and that the three-part schema structure works in practice.*

## Summary

| Repo | Branch | HEAD | Tests | Nix check |
|---|---|---|---|---|
| `schema` | `designer-schema-derived-nota-2026-05-26` | `5d9b0ff` | 29/29 pass (15 kernel + 14 schema) | green |
| `nota` | `designer-schema-derived-nota-2026-05-26` | `abdd9db` | spec repo (0 Rust tests) | green |
| `nota-codec` | `designer-schema-derived-nota-2026-05-26` | `4f04b0e` | docs-only | green |
| `signal-frame` | `designer-schema-derived-nota-2026-05-26` | `07651ad` | docs-only | green |

Branches pushed to origin. Worktrees under `/home/li/wt/github.com/LiGoldragon/<repo>/designer-schema-derived-nota-2026-05-26/`.

## What landed per repo

### `nota` — the foundational schema

- **`schema/nota.schema`** — NOTA's own grammar described in NOTA. Five-block canonical layout:
  1. `{}` — Specifying (no imports at the foundation)
  2. `[]` — Input header (NOTA is a grammar, not an op surface)
  3. `[]` — Input extras
  4. `{...}` — Namespace: TokenKind, Delimiter, IdentifierClass, Sigil, StringForm, Literal, Node, Token, MapEntry, IdentifierToken, LiteralValue, StringValue, ParseError, ParseResult, etc. (23 user-defined types)
  5. `[]` — Output
- **Removed** `schema/nota.concept.schema` (placeholder) in favour of the populated `schema/nota.schema`.
- **`ARCHITECTURE.md` + `INTENT.md`** — document the schema-derived direction without reverting the existing PascalCase / closed-sum / no-defaults discipline (those properties survive as grammar properties OF nota.schema's namespace).

### `schema` — the prototype crate

The schema repo became a workspace (`["., "prototype"]`) with the production `schema` crate untouched. The new `prototype/` crate is self-contained:

- **`prototype/Cargo.toml`** — separate crate, depends on nothing in the workspace (proves the bootstrap circularity has a clean cut).
- **`prototype/src/kernel.rs`** (~380 LOC) — bootstrap kernel: lexer + delimiter-tree parser for NOTA. Handles three delimiter pairs, two bracket-string forms, identifiers (3 classes), integers / floats / bytes, line comments. The bracket-string vs vector disambiguation is the only meaningful boundary the kernel makes; schema-position-driven re-interpretation defers to the layer above.
- **`prototype/src/schema.rs`** (~240 LOC) — three-part schema reader. Parses the five-block layout, builds `AssembledSchema` with `NamespaceEntry`, `EnumVariant`, `OperationEntry`, and a `TypeBody` enum (Enum / Struct / Map / Macro / Alias) classifying each namespace value by its delimiter shape.
- **`prototype/src/emit.rs`** (~120 LOC) — the proof: given an `AssembledSchema` (specifically the assembled `nota.schema`), emit codec predicates — `is_bare_eligible`, `needs_block_form`, `is_known_variant`, `declares` — driven entirely by the schema's namespace, not by hand-authored rules per type.
- **`prototype/src/macros.rs`** (~80 LOC) — macro shape-interpretation engine. Classifies a node into `SingleIdentifierMap`, `KeyValueMap`, `NamedRecord`, `Vector`, or `Unknown`. The two key shapes from record 753 (`{ identifier }` and `{ k1 v1 k2 v2 ... }`) both classify correctly.
- **`prototype/src/library.rs`** (~110 LOC) — precompiled-schema library. Core (`nota.schema`) always implicitly loaded; per-component schemas load on demand; namespace resolution falls through from per-component to core.
- **`prototype/src/bin/demo.rs`** — runs the full chain end-to-end and prints results. Exit 0 confirms feasibility.
- **`prototype/schemas/nota.schema`** — copy of the foundational schema (the prototype is self-contained for the cargo dependency-free demonstration).
- **`prototype/schemas/coordinate.schema`** — three-part demo schema with non-empty Input (Move / Rotate / Read) and Output (Replied) sections.
- **`prototype/tests/kernel.rs`** — 15 tests covering lex + parse for every kernel feature.
- **`prototype/tests/schema.rs`** — 14 tests covering three-part reading, namespace assembly, codec emission, macro classification, and library resolution.
- **`flake.nix`** updated to include `prototype/schemas/` in the crane source filter so `nix flake check` sees the included schema files.

### `nota-codec` — direction note

- **`ARCHITECTURE.md`** — documents the long-term shape (bootstrap kernel + schema-emitted codec surface). No code changes; the production `nota-codec` stays in service while the prototype matures.

### `signal-frame` — direction note + flagged retraction

- **`ARCHITECTURE.md`** — documents the three-part shape direction for `schema-rust`'s composer. Flags the existing crystallization slice (EffectTable / FanOutTargets / StorageDescriptor) for operator review per the audit-policy discipline (record 736); designer does not delete unilaterally.

## `nota.schema` — NOTA described in NOTA

Excerpt of the namespace block (block 4 of the canonical five-block layout):

```nota
{
  Delimiter (RecordOpen RecordClose VectorOpen VectorClose MapOpen MapClose)
  IdentifierClass (PascalCase CamelCase KebabCase)
  PascalCaseRole (DataCarryingVariantTag UnitVariant StructTag)
  Sigil (LineComment ByteLiteralPrefix)
  StringForm (Inline MultilineBlock)

  Literal
    ( Integer Float BareIdentifierString BracketString BlockString
      Bytes Hash True False None SomeWrapped )

  Text [String]
  Position [u32]
  ByteRange [Position Position]

  TokenKind
    ( RecordOpen RecordClose VectorOpen VectorClose MapOpen MapClose
      Identifier Integer Float InlineString BlockString Bytes LineComment )

  Token [TokenKind ByteRange]

  Node
    ( (Record (Vec Node))
      (Vector (Vec Node))
      (Map (Vec MapEntry))
      (Identifier IdentifierToken)
      (Literal LiteralValue)
      (String StringValue) )

  ;; ... etc
}
```

Note the variant-payload convention: `(Tag Payload)` records inside the enum's parenthesised body, matching the existing canonical shape in `spirit.schema` (e.g. `Observation (State (Records RecordQuery) Topics Questions)`).

## Bootstrap kernel boundary

**Hand-authored Rust (kernel):**
- `Kernel<'src>` struct with `lex` + `parse_sequence` + `parse_single` methods
- `KernelToken` / `KernelTokenKind` (13 token kinds)
- `Node` / `NodeKind` (9 node kinds — the delimiter-tree representation)
- `NodeWalker` (private; builds `Node` from tokens)
- ~380 LOC total

**Schema-emitted (or schema-driven at runtime):**
- The `EmittedCodec` rule set (bare-eligibility, block-form detection, variant-tag validation) — emits from the assembled `nota.schema`.
- The `MacroEngine` shape classifier — interprets `Node` shapes the schema declares as macro-shaped.
- All namespace-resolution behaviour in `Library` — driven by the namespace tables the schema reader builds.

The cut is clean: the kernel knows three delimiters, two bracket-string forms, integer / float / bytes / identifiers, line comments. Everything that talks about TYPES (variant tags, struct fields, string eligibility) is downstream of `nota.schema`'s namespace.

## Three-part schema demo

**`prototype/schemas/coordinate.schema`** demonstrates a non-grammar schema with non-empty Input + Output:

```nota
{}                                ;; Specifying (no imports here)

[                                 ;; Input header — operations in variant order
  (Move (MoveRequest))
  (Rotate (RotateRequest))
  (Read (ReadRequest))
]

[]                                ;; Input extras (empty)

{                                 ;; Namespace
  Coordinate [Position Position]
  Position [f64]
  Angle [f64]
  MoveRequest [Coordinate]
  RotateRequest [Angle]
  ReadRequest [unit]
  unit (Unit)
  PositionReply [Coordinate]
  BoundsError ((MinX f64) (MinY f64) (MaxX f64) (MaxY f64))
  Reply ((Position PositionReply) (Bounds BoundsError))
}

[                                 ;; Output — replies / events
  (Replied (Reply))
]
```

After `AssembledSchema::read(...)`, this produces:
- `input_operations = [Move, Rotate, Read]` (3 entries, payload types attached)
- `output_operations = [Replied]` (1 entry)
- `namespace = [Coordinate, Position, Angle, MoveRequest, RotateRequest, ReadRequest, unit, PositionReply, BoundsError, Reply]` (10 user-defined types)

The demo binary prints this end-to-end. Tests `coordinate_schema_has_three_input_operations` and `coordinate_schema_has_one_output_operation` lock the assembled shape.

## Macro shape-interpretation demo

The engine classifies by structural shape per record 753:

```rust
// { universalUnknown } -> SingleIdentifierMap { name: "universalUnknown" }
// { host localhost port 8080 } -> KeyValueMap with entries [("host", ...), ("port", ...)]
// (Some 42) -> NamedRecord { name: "Some", fields: [42] }
```

Tests `macro_classify_single_identifier_map`, `macro_classify_key_value_map`, `macro_classify_named_record` lock these. Adding a new shape lands as a new `MacroShape` variant + a classify-branch — no kernel or schema-reader edits required.

## Precompiled-schema library

`Library::with_core(nota_schema_source)` loads `nota.schema` as the always-implicit core. `library.load("coordinate", coord_source)` loads a per-component schema. `library.resolve("coordinate", "TokenKind")` finds `TokenKind` via core fallthrough (the coordinate schema doesn't declare it; core does). Tests `library_loads_core_implicitly_then_per_component`, `library_resolve_falls_through_to_core`, `library_rejects_double_load` lock the contract.

The library is in-process; the schema daemon (record 750) would be the runtime arm sharing this cache across consumers. The prototype keeps it in-process per the deferred-scope budget below.

## Schema daemon

**Deferred.** The library's `Library` struct exposes the surface a daemon would offer (load / get / resolve / loaded_names). Promoting to a separate process is mechanical work — Unix socket + NOTA RPC + the existing `signal-frame` shape — and lands as a follow-up commit once the prototype's library API stabilises. Per record 750.

## Verification

| Check | Schema | Nota | Nota-codec | Signal-frame |
|---|---|---|---|---|
| `cargo build` | green | spec-only | green | green |
| `cargo test` (prototype) | 29/29 pass | n/a | n/a | n/a |
| `nix flake check` | green | green | green | green |

Detailed test breakdown (29 prototype tests):

**kernel.rs (15 tests):**
- `lex_empty_input_yields_no_tokens`
- `lex_whitespace_only_yields_no_tokens`
- `lex_three_delimiter_pairs`
- `lex_inline_bracket_string_with_apostrophe`
- `lex_token_shaped_brackets_resolve_to_vector`
- `lex_block_string`
- `lex_identifier_classes`
- `lex_integers_floats_bytes`
- `lex_line_comment`
- `lex_unclosed_string_errors`
- `parse_nested_record`
- `parse_map`
- `parse_vector`
- `parse_empty_collections`
- `parse_nota_schema_top_level_layout` — the canonical 5-block sequence

**schema.rs (14 tests):**
- `nota_schema_reads_into_three_part_view`
- `nota_schema_namespace_declares_expected_types`
- `nota_schema_delimiter_is_an_enum_with_six_variants`
- `coordinate_schema_has_three_input_operations`
- `coordinate_schema_has_one_output_operation`
- `emit_codec_from_nota_schema_classifies_kinds`
- `emit_codec_bare_eligibility_matches_nota_rules`
- `emit_codec_block_form_detection`
- `macro_classify_single_identifier_map`
- `macro_classify_key_value_map`
- `macro_classify_named_record`
- `library_loads_core_implicitly_then_per_component`
- `library_resolve_falls_through_to_core`
- `library_rejects_double_load`

The demo binary `cargo run -p schema-derived-nota-prototype --bin schema-derived-nota-demo` exits 0 and prints the full chain (lex → parse → three-part view → assembled namespace → emitted codec → library load → macro classification → core fallthrough).

## What's deferred

- **Schema daemon (record 750).** The `Library` struct exposes the daemon's API shape but stays in-process. Promoting to an out-of-process daemon with a signal-frame socket is the obvious next step.
- **Full nota-codec replacement.** The prototype demonstrates the bootstrap kernel + emitted codec separation; production `nota-codec` stays in service. Migration is operator's call once the prototype shape stabilises.
- **Cross-crate schema imports.** The prototype embeds `nota.schema` as `include_str!(...)` for self-containment. Cross-repo imports via the schema daemon are the natural next layer.
- **EffectTable / FanOutTargets / StorageDescriptor removal from production `schema` crate.** Flagged in signal-frame's ARCHITECTURE for operator review per record 736 audit-policy (designer does not delete unilaterally).
- **Performance optimization of the precompiled library.** The prototype uses `BTreeMap` + linear-scan namespace lookups; production wants a perfect-hash table or similar.
- **schema-rust composer integration.** The prototype's `emit.rs` is a runtime emitter showing the rule set; the composer integration (proc-macro that bakes the rules at compile time) is the next step.
- **The kernel's bracket-disambiguation rule.** Kernel currently defaults `[token token]` to Vector and lets schema position re-interpret; a fully-clean kernel boundary may eventually emit only `BracketOpen` and let ALL string-vs-vector decisions land at the schema layer. The current rule resolves the textbook cases (apostrophes / colons / etc. → InlineString; nested delimiters → Vector) and is enough for the prototype.

## Worktrees + branches pushed

| Worktree | Branch | Remote |
|---|---|---|
| `/home/li/wt/github.com/LiGoldragon/schema/designer-schema-derived-nota-2026-05-26/` | `designer-schema-derived-nota-2026-05-26` | `origin/designer-schema-derived-nota-2026-05-26` |
| `/home/li/wt/github.com/LiGoldragon/nota/designer-schema-derived-nota-2026-05-26/` | `designer-schema-derived-nota-2026-05-26` | `origin/designer-schema-derived-nota-2026-05-26` |
| `/home/li/wt/github.com/LiGoldragon/nota-codec/designer-schema-derived-nota-2026-05-26/` | `designer-schema-derived-nota-2026-05-26` | `origin/designer-schema-derived-nota-2026-05-26` |
| `/home/li/wt/github.com/LiGoldragon/signal-frame/designer-schema-derived-nota-2026-05-26/` | `designer-schema-derived-nota-2026-05-26` | `origin/designer-schema-derived-nota-2026-05-26` |

All four worktrees branched fresh from each repo's `main`. None of them build on the prior `designer-schema-poc-*` branches (which carry the retracted drift per records 730-732).

## Coordination concerns

- **Production `schema` crate stays untouched.** The workspace conversion in `schema/Cargo.toml` adds a `[workspace] members = [".", "prototype"]` header above the existing `[package]` block; production `schema` continues to build standalone (`cargo build -p schema` green). The prototype lives entirely in its own crate.
- **Production `nota-codec` stays untouched.** Only `ARCHITECTURE.md` adds a direction note.
- **Production `signal-frame` stays untouched.** Only `ARCHITECTURE.md` adds a direction note AND flags the existing crystallization slice for operator review. No code edits to the retracted `feature.rs` / `EffectTable` / `FanOutTargets` / `StorageDescriptor` surface — that retraction is operator's authority per record 736.
- **Migration path is intentionally open.** Operator integrates these branches per `skills/feature-development.md` if-and-when the psyche approves; no force-push, no main-touch from designer-assistant.

## What this prototype proves

1. **NOTA's grammar can be expressed as a schema in NOTA.** `nota.schema` reads correctly via the kernel and assembles into a namespace describing every token kind, identifier class, literal form, and node kind the codec needs to know about.
2. **A small bootstrap kernel can read the foundational schema.** ~380 LOC suffices; everything else can emit FROM the schema rather than being hand-maintained.
3. **The three-part schema structure works in practice.** `coordinate.schema` demonstrates non-empty Input + Output sections; `nota.schema` demonstrates the namespace-only case.
4. **Macros bring their own shape interpretation.** `{ identifier }` and `{ k v k v }` shapes classify correctly without the kernel knowing about either.
5. **Precompiled-schema library with core fallthrough is feasible.** Resolution against the implicit core works; per-component schemas load on demand.
6. **The discipline holds.** No `EffectTable` / `FanOutTargets` / `StorageDescriptor` surface. NOTA strings only via bracket forms in the authored schemas. Every Rust function lives on an impl block. No `/nix/store` scans.

## Open questions for the psyche

These are gaps in the design where the prototype made the smallest reasonable interpretation, but the psyche may want a different shape:

1. **Variant-payload representation in nota.schema.** I authored enum variants as `(Tag Payload)` records inside the enum body (matching `spirit.schema`'s `Observation (State (Records RecordQuery) Topics Questions)` pattern). Is that the preferred shape, or should the variant body use a different convention (e.g. `Tag(Payload)` macro syntax)?

2. **Kernel's bracket-disambiguation boundary.** The kernel currently resolves `[token token]` to Vector and lets the schema layer re-interpret as String when the position demands it. An alternative is to emit only a `BracketOpen` token and push ALL string-vs-vector decisions to the schema layer. Which is the canonical cut?

3. **The empty-section convention.** I read `[]` for empty Input and `[]` for empty Output. The /353 design says blocks 2 and 3 (or block 5) may be omitted entirely. Should the five-block-mandatory shape stand (current prototype) or should optional blocks be allowed via shorter top-level sequences (e.g. just `{ ... }` for a namespace-only schema)?

4. **Schema daemon scope.** The prototype's `Library` is in-process. Should the daemon ship side-by-side per the deployment discipline (record 672), and what's its CLI shape — does `persona-schema` follow the spirit triad of `persona-schema` (daemon) / `signal-persona-schema` (working signal) / `owner-signal-persona-schema` (policy signal)?

5. **Bare-identifier eligibility — schema-driven vs universal rule.** My `EmittedCodec::is_bare_eligible` currently mixes a universal rule (`None` is reserved; PascalCase first char excluded; identifier-class bytes only) with the schema's name set. Should the schema declare the universal eligibility rule too (e.g. as a `BareEligible` macro?), or is the universal rule properly a kernel-level invariant?

None of these are blockers for the prototype's purpose (empirical feasibility); they're shape questions for the next iteration. Per `skills/intent-clarification.md`: noting the gaps in this report rather than inferring fills.

## References

- Spirit records **746-753** (Maximum) — the new design intent
- Spirit records **730-732** (Maximum) — EffectTable / FanOutTargets / StorageDescriptor retraction
- Spirit record **698** — NOTA bracket-only string discipline
- Spirit record **729** — methods-only Rust discipline
- Spirit record **736** — audit-policy: agents flag, psyche supersedes
- `/353` — design synthesis (the spec for this prototype)
- `/350` — retraction report (the cleanup that preceded the design)
- `/192` — operator's prior implementation (cross-reference, not foundation)
- Canonical schema example: `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema`
- NOTA grammar spec: `/git/github.com/LiGoldragon/nota/README.md`
