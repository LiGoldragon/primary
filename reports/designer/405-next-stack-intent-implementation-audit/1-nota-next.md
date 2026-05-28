# 405/1 — nota-next intent↔implementation audit (Layer 0, raw text)

*Kind: Audit · Topics: nota, schema, audit, intent · 2026-05-28 · pinned `main` `fa14c7fb027c6c552a4ba29c3eddc61b2b5b6cfb`, confirmed HEAD, no drift.*

## Verdict

nota-next is the cleanest layer in the stack relative to intent: the scope boundary holds (no schema-type knowledge leaks in), the method-only Rust discipline is satisfied with zero free functions and zero ZST namespace holders, and the bracket-string discipline is honored structurally — quotation marks are NOT special to the parser, so it cannot emit them and does not privilege them. All 8 tests pass. The real gaps are at the layer's frontier, not its core: (1) the `StructureHeader` "structure header boundary" — the load-bearing artifact the pinned commit documents — has a packing bug that silently corrupts wide structures and an undocumented lossy truncation policy, and it is AHEAD of psyche intent (no Spirit record names a packed 64-bit triage word — only the repo's own `INTENT.md` does, which is agent-synthesised and itself auditable); (2) the brace `{}` is parsed as a positional list identical to parens, NOT modeled as a key/value map, which is a latent DIVERGENCE from the workspace-wide "brace is ALWAYS key/value" rule even though the boundary-correct reading is defensible; (3) the bracket-as-vector intent (`[a b c]`) is structurally present but the candidate-classification surface only covers atoms, leaving pipe-text and bracket-content unclassified by design — fine, but worth naming. Nothing here is broken-as-shipped for the current consumer; the header bug is the one item that will bite when schema-next leans on `packed_word`.

## Intent item 1 — Scope boundary (schema semantics must not leak in): MET

The boundary is held both in the API surface and in the type vocabulary. The crate's own doc comment states the discipline (`src/lib.rs:1-7`: "deliberately does not interpret those structures as schema types, fields, imports, or macros"), and the code backs it.

- No type named after a schema concept. The enums are `Block` (`src/parser.rs:57`), `Delimiter` (`:207`), `StructureShape` (`:317`), `AtomClassification` (`:453`) — all structural. There is no `Enum`, `Struct`, `Namespace`, `Import`, `Macro`, `Field`, or `Type` anywhere.
- Classification stops at structural candidates. `AtomClassification` has exactly four arms — `SymbolCandidate`, `IntegerCandidate`, `DecimalCandidate`, `TextCandidate` (`src/parser.rs:453-458`) — and `classify` (`:461-478`) decides them from raw character shape only (digit-parse, decimal-point, symbol-character set). It never asks "is this a type name" or "is PascalCase legal here".
- The case predicates are named `qualifies_as_*`, not `is_*`. `qualifies_as_pascal_case_symbol` / `_camel_case_` / `_kebab_case_` (`src/parser.rs:427-449`) report a candidate, deferring legality to the schema layer. The separation test `design_example_reader_exposes_candidates_not_schema_semantics` (`tests/design_examples.rs:71-92`) asserts this boundary directly, and `ARCHITECTURE.md:11-12` codifies the `is_*` (fact) vs `qualifies_as_*` (candidate) split.
- The header records *shape and child-count only*, never meaning (`src/parser.rs:317-351`: `StructureShape` is `Document`/`Atom`/`Parenthesis`/`SquareBracket`/`Brace`/`PipeText`/`Unknown`).

This matches the active-repositories charter ("`qualifies_as_*` methods only; schema semantics live in schema-next") and §1.6's NOTA discipline. No leak found.

## Intent item 2 — NOTA strings come EXCLUSIVELY from bracket forms; never emit quotes: MET (structurally)

The parser treats brackets as the only string-forming syntax and gives `"` no special meaning, which is exactly the bracket-only discipline.

- `[|...|]` is the bracket-safe / multi-line string form, parsed by `parse_pipe_text` (`src/parser.rs:597-616`), recognized via `Some('[') if self.peek_next() == Some('|')` (`:558`). Its body is captured verbatim and NOT recursively parsed — proven by `pipe_text_is_square_bracket_safe_and_not_recursively_parsed` (`tests/block_queries.rs:54-66`), whose fixture deliberately contains a `"` inside the pipe text and round-trips it untouched.
- Quotation marks are inert. In `parse_atom` (`src/parser.rs:618-638`) the stop set is whitespace, `;`, and opening/closing delimiters (`:621-625`); `"` is none of these, so `"foo"` is swallowed into an atom's text as ordinary characters and classified `TextCandidate` (`:461-478`). The parser thus neither rejects nor privileges legacy quoted strings — it has no quote concept at all, which is the strongest possible form of "brackets ARE the string form."
- The crate emits no NOTA. The only `write!` calls are in `NotaError`'s `Display` (`src/parser.rs:499-518`), which emit diagnostic prose with backtick-delimited characters (e.g. `` `{found}` ``), never a NOTA value and never a `"`-wrapped string. `reemit` (`:76-79`) returns a borrowed `&str` slice of the original source by byte offset — it re-presents the author's bytes, it does not serialize.

Caveat (not a violation): the "exclusively from bracket forms" rule has a second leg — bare camelCase/kebab-case atoms at String schema positions. nota-next classifies those as `SymbolCandidate` (`:423-425`, `:447-449`) and leaves the "this is a string here" decision to schema-next. Correct for Layer 0.

## Intent item 3 — Brace `{}` is ALWAYS key/value; records are positional: PARTIAL / latent DIVERGENT

Two halves; the parser gets the positional-record half right and the brace half structurally-present-but-semantically-flat.

Positional records — MET at this layer. There is no `(key value)` pair handling anywhere; `parse_delimited` (`src/parser.rs:566-595`) reads a flat ordered `Vec<Block>` regardless of delimiter, and `root_object_at(index)` (`:134-139`) is purely positional. nota-next correctly does NOT impose the Lisp `(key value)` shape. (Whether records are positional is ultimately a schema-next concern; Layer 0 just preserves order, which it does.)

Brace as key/value — latent DIVERGENT. Workspace `INTENT.md:286` and §1.6 of the frame state the hard rule: "A brace `{ ... }` in NOTA is ALWAYS a key/value map." But in nota-next a `Brace` block is structurally identical to a `Parenthesis` block — both are `Block::Delimited` with a flat `root_objects: Vec<Block>` (`src/parser.rs:58-62`), and `is_brace` / `is_parenthesis` differ only by the `Delimiter` tag (`:81-109`). The structure header records a brace's `child_count` as a raw count (`:201-203`), and the test fixture `{ Entry [Text] }` yields `(StructureShape::Brace, 2)` (`tests/design_examples.rs:103`, `:123`) — a count of 2 flat children, NOT one key/value pair. So at the raw layer a brace is a flat even-length list, and the "these are k/v pairs" reading is entirely deferred to schema-next.

This is defensible under the strict scope boundary (pairing IS a semantic, arguably schema-next's job), so I classify it PARTIAL rather than outright DIVERGENT. But it is a real latent divergence to flag for the synthesis: if "brace is ALWAYS k/v" is meant to be a *structural* invariant (e.g. nota-next should reject an odd-length brace body, or expose `key_value_pairs()` on a brace block), then nota-next does not enforce or even represent it. Nothing in the code or tests asserts a brace body is even-length. Open question for psyche: does the k/v-ness of braces belong at Layer 0 (structural rejection of odd bodies) or Layer 1 (schema-next pairs them)? The repo has silently chosen Layer 1.

Bracket-as-vector (`[a b c]`) — MET structurally. A non-pipe `[` is `Delimiter::SquareBracket` (`src/parser.rs:559`) parsed into ordered children, so `[a b c]` is a 3-child square-bracket block. The vector reading is available; the string-vs-vector disambiguation of `[...]` is left to schema-next (correct).

## Intent item 4 — Method-only Rust discipline, no free functions, no ZST namespace holders: MET

I enumerated every `fn` in `src/parser.rs` and `src/lib.rs`. `lib.rs` contains zero functions (only `mod` + `pub use`, `:9-14`). Every one of the ~60 functions in `parser.rs` sits inside an `impl` block of a data-bearing type or a trait impl. No free functions outside `#[cfg(test)]`/`fn main` (there is no `fn main` and the in-crate has no test module — tests live in `tests/`).

- `impl` blocks and their owning nouns, each NON-zero-sized: `Document` (holds `source: String`, `root_objects: Vec<Block>` — `:17-20`, methods `:22-54`); `Block` (enum with data in every arm — `:67-204`); `Delimiter` (3-variant enum, methods `:213-247`); `StructureHeader` (holds `slots: Vec<StructureSlot>` — `:250-280`); `StructureSlot` (holds `shape` + `child_count` — `:283-314`); `StructureShape` (7-variant enum, `:327-351`); `StructureHeaderBuilder` (holds `slots: Vec<...>` — `:354-395`); `Atom` (holds `text`/`classification`/`span` — `:410-450`); `AtomClassification` (4-variant enum, `:460-479`); `Parser` (holds `source` + `cursor` — `:530-680`); `Cursor` (holds 3 `usize` fields — `:699-707`); `AtomCharacter` (holds `character: char` — `:714-722`).
- Trait impls: `impl fmt::Display for NotaError` (`:496-521`), `impl std::error::Error for NotaError` (`:523`), `impl Default for Cursor` (`:689-697`). All legitimate.
- No ZST namespace holder. The closest candidate is `AtomCharacter` (`:709-722`), a one-field newtype over `char` whose `is_symbol` (`:719-721`) could have been a free function `fn is_symbol(c: char)`. It is NOT a ZST — it carries a `char` field, so erasing its name from the type system loses the wrapped value. It passes the §"No ZST method holders" test (the job does not vanish when you erase the name). It is a real, if thin, data-bearing noun. Acceptable.

No violations. This is full compliance with the method-only hard override and `skills/rust/methods.md`.

## Intent item 5 — The "structure header boundary": AHEAD of psyche intent, with two implementation gaps

The pinned commit `fa14c7f` adds exactly the paragraph in `INTENT.md:14-17` describing "a compact first-two-level structure header … structural only: it records delimiter/atom shape and child counts so higher layers can triage before semantic lowering." The code that backs it is `StructureHeader` / `StructureSlot` / `StructureShape` / `StructureHeaderBuilder` (`src/parser.rs:250-395`) plus `Document::structure_header` (`:49-53`), proven by `design_example_structure_header_captures_first_two_levels` (`tests/design_examples.rs:99-131`).

Classification: AHEAD. The audit yardstick is PSYCHE intent (frame §0: the repos' own `INTENT.md` are "agent-synthesised claims — themselves auditable for drift"). I find NO Spirit record in the frame's amalgamation (§1, records 700-1008) that calls for a packed 64-bit structural triage word, a "first-two-level" header, or a `packed_word`/`from_packed_word` round-trip. The only source for this artifact is the repo's own `INTENT.md`, which the commit message frames as documenting a decision the code already made. So the structure header is an implementation that has run AHEAD of named psyche intent. That is not inherently wrong (Layer 0 may legitimately invent the triage substrate the upper layers will need), but the synthesis should surface it for explicit psyche ratification, because it carries design commitments (a fixed byte layout, a fixed depth, lossy truncation) that upper layers will couple to.

Two concrete implementation gaps within the header:

### 5a. `packed_word` silently corrupts when any slot has more than 15 children (bug)

`StructureSlot` packs `shape.code()` into the high nibble and `child_count` into the low nibble of one byte (`src/parser.rs:304-306`: `(self.shape.code() << 4) | self.child_count`). `child_count` is clamped to 15 at construction (`:292`: `child_count.min(15) as u8`), so a parens with 20 children records `child_count = 15`. That clamp is silent and lossy: `from_packed_byte` reads back `byte & 0x0f` (`:311`) = 15, so a 20-child and a 15-child structure are indistinguishable after a round-trip. Worse, the clamp is only enforced in `StructureSlot::new` (`:289-294`); `child_count()` (`:300-302`) returns the stored value, so the in-memory header from `structure_header()` already carries the clamped 15 even before packing. A "structural triage word" that cannot represent ">15 children" is a real limitation that nothing documents — `INTENT.md:14-17` does not mention the 15-child ceiling or the 8-slot ceiling. The round-trip test (`tests/design_examples.rs:126-130`) only exercises a fixture whose every node has ≤3 children, so the clamp is untested and the corruption is invisible in CI.

### 5b. The header is lossy-by-truncation with no marker, and the depth/breadth policy is silent

`StructureHeaderBuilder` caps at `MAXIMUM_SLOTS = 8` (`src/parser.rs:255`) and depth 2 (`:374` `depth > 2`, `:378` `if depth == 2 return`). A document with more than 8 first-two-level blocks is truncated at slot 8 with NO sentinel indicating truncation occurred — `from_packed_word` (`:269-279`) stops at the first zero byte after index 0, so a naturally-8-slot structure and a truncated-from-50 structure pack identically. The `StructureShape::Unknown` arm (code 15, `:324`/`:336`/`:348`) exists and could have served as a "truncated/overflow" marker but is never emitted by the builder — it is only reachable via `from_code` on an out-of-range nibble. So `Unknown` is dead on the emit path (the crate's `dead_code = "warn"` lint at `Cargo.toml:20` does not catch it because the variant is constructed in `from_code`). Net: the header silently conflates "small structure" with "big structure, first 8 slots." For a triage word this may be acceptable by design, but it is undocumented and the consumer (schema-next) has no way to know whether it is seeing the whole shape or a prefix.

### 5c. Header packing order vs `MAXIMUM_SLOTS` is internally consistent (not a bug)

For completeness: `packed_word` (`:261-267`), `from_packed_word` (`:269-279`), and the builder's two independent `MAXIMUM_SLOTS` guards (`:374`, `:387`) all agree on 8, and slot 0 is always `Document` so the "zero byte after index 0 ends the header" decode (`:273`) is sound (a `Document` slot packs to a non-zero byte because its shape code 0 in the high nibble plus a child count can still be zero only if the document is empty — an empty document packs slot 0 to `0x00`, and `from_packed_word`'s `index > 0` guard at `:273` correctly keeps slot 0). This corner (empty document → single zero slot 0) is handled but untested.

## Test status

`cargo test` at the pinned commit: PASS. 8 tests, 0 failures (5 in `tests/block_queries.rs`, 3 in `tests/design_examples.rs`, 0 unit, 0 doc). Build clean, no warnings. (Did not fix anything; report-only.) The tests prove the boundary discipline well but leave the header's lossy edges (>15 children, >8 slots, empty document) entirely unexercised.

## Top gaps (most severe first)

1. **Header `packed_word` corrupts >15-child structures silently (5a)** — `src/parser.rs:292`,`:305`,`:311`. A child count above 15 is clamped to 15 with no marker; round-trip is lossy and untested. This is the one item that will actually mislead schema-next when it triages a wide structure off `packed_word`. Severity: highest because it is a correctness bug in the load-bearing artifact the pinned commit ships.

2. **Structure header is AHEAD of psyche intent (5)** — no Spirit record in §1 (700-1008) names the packed triage word; only the repo's own `INTENT.md:14-17` does. The byte layout, the depth-2 / 8-slot ceilings, and the truncation policy are unratified design commitments upper layers will couple to. Needs explicit psyche ratification (intent-clarification), or downgrade to a documented-internal-detail.

3. **Header truncation is unmarked (5b)** — `src/parser.rs:255`,`:374`,`:378`,`:269-279`. ">8 first-two-level blocks" and "exactly 8" pack identically; the `Unknown` shape that could mark overflow is never emitted. Consumers cannot distinguish a complete header from a prefix.

4. **Brace `{}` not modeled as key/value (3)** — `src/parser.rs:58-62`,`:101-109`,`:201-203`. Workspace `INTENT.md:286` says brace is ALWAYS k/v; nota-next parses it as a flat even-length list identical to parens, deferring all pairing to schema-next, and never asserts even-length. Latent divergence; needs a psyche call on whether k/v-ness is a Layer-0 structural invariant or a Layer-1 concern.

5. **Header lossy edges are untested (test gap)** — `tests/design_examples.rs:99-131` only covers ≤3-child, ≤8-slot fixtures. The >15-child clamp, the >8-slot truncation, and the empty-document slot-0 decode have zero coverage, which is why gaps 1 and 3 are invisible in CI.
