# Skill — NOTA design

*How to design NOTA records well: positional, typed, terse, grep-able. Every meaningful distinction lives in the data; no token is spent on what the context already gives.*

Read this before designing a new NOTA file or schema. Designed badly, NOTA becomes JSON with extra steps — verbose, with data hiding in comments or restated as identical wrappers around every record. Designed well, the same data takes a third of the tokens and the structure itself carries category information that would otherwise be a side channel.

## Rule 1 — If there's no variant, it's a struct (no tag)

A PascalCase tag at the start of `(…)` is an enum variant. If every record in the file would carry the same tag, there is no enum — it's a struct, and structs have **no tag** in the wire form. Drop it.

`skills.nota` has actual variants — `Role`, `Architecture`, `Craft`, `Programming`, `Workflow`, `Meta` — so each record IS an enum variant and the tag tells the reader which kind of skill this is. A deployment plan with one kind of step drops the tag: `(zeus apply 2026-05-19)`. If steps vary (`Build`, `Verify`, `Deploy`), the variant tags appear.

The test: *can the same position carry more than one shape?* If yes, you have an enum and the variant tag names which shape this record is. If no, you have a struct and write the fields directly with no tag.

## Rule 2 — Data lives in records, not in comments

NOTA comments explain the schema — what fields mean, what variants exist, the structural contract. They do NOT organize data into categories or sections. A `;; Roles` header introducing three role records is a category surfaced as a comment: NOTA can't see it and nobody can grep it. The category IS data — make it the type.

Bad:

```nota
;; Roles
(Skill operator skills/operator.md role 1 [...])
(Skill designer skills/designer.md role 1 [...])

;; Architecture
(Skill component-triad skills/component-triad.md architecture 1 [...])
```

Two faults: every record wears a redundant `Skill` wrapper, and the categories are duplicated as both comment and field. Fix both — the type IS the category:

```nota
(Role operator skills/operator.md Apex [...])
(Role designer skills/designer.md Apex [...])

(Architecture component-triad skills/component-triad.md Apex [...])
```

Same data, fewer tokens, grep-able category. Instance names (`operator`, `component-triad`) are lowercase/kebab-case because they're runtime instances; the tier value (`Apex`) is PascalCase because it's a compile-time enum variant.

## Rule 3 — Enums get PascalCase names, not numbers

Integer codes for enum variants are a smell. `tier 1` / `tier 2` means nothing without a key; `tier Apex` / `tier Keystroke` / `tier Topic` is self-documenting and grep-able from a cold read.

Bad: `(Skill component-triad ... 1 ...)`. Good: `(Architecture component-triad ... Apex ...)`.

Variants are **PascalCase** because they're compile-time structural (PascalCase = compile-time structural; camelCase = instance). The parser dispatches on first-character case — a lowercase `apex` parses as an instance identifier, not a variant. Numbers are fine for actual numbers (counts, identifiers, slots, ordinals where ordering matters); not as stand-ins for named categorical distinctions. Grep for `Apex` finds every apex-tier record across every NOTA file that shares the vocabulary.

## Rule 4 — Enum payloads are choices; structs are products

When an enum variant carries data, the payload's shape follows what the data IS:

- **One axis of choice** → direct enum payload. `(Busy BusyReason)` where `BusyReason [DatabaseOverloaded ResourceDisconnected OtherBusyReason]`. Not `(Busy BusyReport)` wrapping the choice in a struct that adds nothing.
- **Product of independent facts** → struct payload. `(RecordAccepted SemaReceipt)` where `SemaReceipt { RecordIdentifier * DatabaseMarker * }` — multiple facts the reply carries together.
- **Only some choices need extra data** → nested data-carrying enum. `BusyReason [(DatabaseOverloaded RetryGuidance) ResourceDisconnected OtherBusyReason]` — guidance attaches to the variant that needs it.

Wrong shape: inventing a `<Variant>Report` struct wrapper around a single enum. The semantic root is the variant; the choice axis is the payload enum; no wrapper. The notation must truthfully represent the data shape — empty wrappers are a smell.

### Header-declared inline enum sugar

The payload enum can be declared at the header position:

```schema
Output [
  RecordAccepted
  RecordsObserved
  (Busy [DatabaseOverloaded ResourceDisconnected OtherBusyReason])
  Rejected
]
```

The header stays a homogeneous vector of variant-signature objects: `RecordAccepted` and `(Busy [...])` and `Rejected` are each signatures. The inline bracket body declares the payload enum locally instead of forcing a separate namespace declaration. The lowered form is equivalent to:

```schema
Output [RecordAccepted RecordsObserved (Busy BusyReason) Rejected]
BusyReason [DatabaseOverloaded ResourceDisconnected OtherBusyReason]
```

### Type-table variant resolution

The header can list variant names without spelling whether each is unit or data-carrying; the schema reader resolves against the local type table:

```schema
Output [RecordAccepted RecordsObserved Busy Rejected]
```

If `RecordAccepted` is a declared type, the variant carries it; if the name is not a declared type, it is a unit variant. The explicit `(Variant PayloadType)` form remains available when the variant name differs from the payload type name (e.g. `(Rejected SignalRejection)`). Same-name resolution defaults to data-carrying when a type exists.

## The canonical example

`skills.nota` is the workspace's canonical example of NOTA designed well. Open it before designing a new file. Notice: no `(Skill ...)` wrapper (implied by the file); the type IS the category (`(Role ...)`, `(Architecture ...)`, etc.); tier values are PascalCase variants (`Apex`, `Keystroke`, `Topic`, `Mechanism`); comments only explain the schema.

## Grammar facts that catch the recurring mistakes

These are the language's actual grammar, not design rules. The source of truth is `nota/README.md`; restated here so the discipline skill carries the load.

### The mental model — three cases for PascalCase, one for the rest

Every PascalCase token falls into one of three cases:

1. `(VariantName fields…)` — **data-carrying enum variant**. An opening `(` immediately followed by a PascalCase token means you're at an enum variant carrying data; everything after the name is its positional fields.
2. `(fields…)` without a leading PascalCase token — **struct**. No tag; the schema position says what struct this is.
3. Bare `VariantName` with no preceding `(` — **unit variant** (no payload). Like `None`, `Maximum`, `Apex`.

Everything else is a primitive (strings, numbers, bools, bytes), a sequence `[…]` which is `Vec<T>` (every element the same schema type), or a map `{…}` which is a flat key/value stream.

The corollary: when you write a record, ask *can this position hold more than one shape?* If yes, it's an enum — tag the variant (case 1) or write a unit (case 3). If no, it's a struct — write fields directly with no tag (case 2). Structs are untagged, enum variants own PascalCase tags, map keys are key text by delimiter position.

### Strings come EXCLUSIVELY from bracket forms

Brackets ARE the string form in NOTA. Quotation marks do NOT form string types — they're ordinary content inside a bracket string, and authored NOTA avoids them entirely. Two canonical forms plus a bare shorthand:

- `[content]` — **inline bracket string**: single-line content. Cannot contain literal `[` or `]` (would ambiguate with sequence syntax).
- `[|content|]` — **block string**: multi-line content AND safe for bare `[` / `]`. The `[|` / `|]` delimiter pair lets content include `[`, `]`, or newlines without escaping.
- **Bare camelCase or kebab-case token** at a `String` schema position equals `[token]` — `nota-codec` is the same value as `[nota-codec]`. A single lowercase letter `a` parses as the bare form; write `[a]` to make the string shape explicit. A bare PascalCase token at an ordinary `String` position is rejected as enum-looking; delimit it as `[User]` when the capitalized text is string content.

The parser distinguishes inline-bracket-string from sequence via the `[|` pair-delimiter, so shape-dispatching macros see `is_block_string` as a predicate distinct from `is_sequence` even though both involve `[`.

The encoder structurally cannot emit a quotation mark: `write_string` has three branches (bare identifier, `[|...|]` block, `[...]` inline) and no quote branch. Legacy `"..."` quoted strings are accepted as **migration input only** (a `read_legacy_quote_string` path); a legacy → canonical round-trip sheds the quotation marks. Legacy acceptance is removed once all emitter sites migrate.

### Embedding-safety is the load-bearing consequence

Because NOTA never contains a `"`, a complete NOTA expression embeds escape-free inside any host whose string syntax uses double quotes — JSON, Rust string literals (including raw `r"..."`), Nix attribute values, YAML scalars, TOML strings, shell double-quote arguments, HTTP bodies, database string columns, env-var values, XML attributes. JSON-in-JSON requires escape cascades; NOTA-in-anything-with-double-quote-strings is escape-free. Design new emitters and storage paths to take advantage of this.

### Shell invocation uses outer double quotes

When NOTA is passed as an inline CLI argument, wrap the whole object in shell double quotes:

```sh
spirit "(Record (nota Correction [description text] Maximum))"
```

This is why authored strings use `[text]` and `[|text|]`, not `"` delimiters: the shell keeps `"` as the outer argument boundary. Single quotes are not the normal inline form — they make natural apostrophes painful and undercut the bracket-string design.

### Inline NOTA — no `\n` escape sequences

Inline NOTA in any single-line string literal context (Rust string, shell argument, markdown inline example, test fixture, doc example) MUST NOT contain `\n` escape sequences. NOTA is whitespace-insensitive — the parser treats any run of whitespace (space, tab, newline) identically between tokens. A `\n` inside a single-line literal adds nothing semantically and produces a hybrid that pretends to be multi-line while being one source line: ugly to read, ugly to grep.

```rust
// Wrong:
let source = "(State [Statement])\n{ Topic [Text] }\n";
// Right (single-line, spaces between tokens):
let source = "(State [Statement]) { Topic [Text] }";
```

For genuinely multi-line NOTA — long fixtures, multi-record sources, schemas with many declarations — use actual newlines in authored `.nota` / `.schema` files loaded via `include_str!`, or a multi-line raw string literal:

```rust
let source = r#"{}
(Input ((Record Entry)))
(Output ())
{
  Topic [Text]
}"#;
```

Single-line for one or two records; file or multi-line raw string when the structure benefits from layout.

### Map keys

Maps use their own delimiter:

```nota
{host localhost port 8080 User 100}
```

Inside `{ }`, odd positions are key text and even positions are values. The schema chooses the scalar key type (`String`, `Path`, or a string-like newtype such as `NodeName`). A bare PascalCase key is allowed because the map delimiter already says this token is key text, not a value. Keys with whitespace are invalid, even when bracket-delimited.

### Schema namespaces use the brace-map rule

In a `.schema` namespace, write `Name body` pairs directly inside `{ }`:

```nota
{
  Entry [Topics Kind Description Magnitude]
  Kind (Decision Principle Correction Clarification Constraint)
}
```

Do not wrap namespace entries as `(Entry [...])` or `(Kind (...))` — the brace already supplies the key/value structure. Conceptually the namespace is a DYNAMIC ENUM where each key is a variant tag and each value is the variant payload, stored as a key/value map for composition and APPEND-ONLY so existing positions stay stable.

### Bare `Path`

Where the schema expects `Path` (not `String`), the bare alphabet widens to include `/` and `.` for filesystem-shaped values. A bare `skills/operator.md` at a `Path` position parses; the same token at a `String` position is a typed error.

### No tuples

NOTA has vectors, structs, enums, and key/value maps. Tuples are poorly specified structs — they carry position but not field names, and field names are information. Use a named-field struct so the schema states what each position means.

### Optional values

`Option<T>` is a normal data-carrying enum. Absence writes bare `None` (case 3); presence writes `(Some inner)` (case 1). Tail omission is **not** a compatibility shape: every position in the text carries every position in the schema, always. `#[nota(default = …)]` is **forbidden**. A record short on tokens is a typed error, not a silent zero-fill.

### Multi-field unnamed structs are forbidden

`struct Pair(i32, i32)` has no field-name mapping; NOTA rejects it at serialize time. Single-field unnamed structs are transparent newtypes only — the inner value emits at the schema position. For heterogeneous positional data, use a named-field struct, which emits as an untagged struct record.

### Sigils

Two are reserved at the syntax layer: `;;` for line comments, `#` for byte literals. Other sigils (`~ @ ! ? *`) are nexus extensions and reserved (syntax error in pure NOTA). `=` is reserved.

## Before you sketch any NOTA record

Before producing any new NOTA shape — in a report, chat, or proposal — do four things:

1. **Open `skills.nota` and read three records.** That's your template. Re-read `nota/README.md` if you haven't recently — these grammar facts are easy to misremember.
2. **Name the wrapping type that carries the most useful distinction** (Rule 1). Never a generic `Item`, `Entry`, or `Record` when the file already says so. The variant test: if you can't name another type that could go in this position, the wrapper is superfluous — drop it.
3. **Heterogeneous positional structure is a record (struct), not a sequence.** Lists are homogeneous; mixed-type positional structure is a struct with positional fields, and the struct's type name is not written as a tag. A PascalCase token immediately after `(` is an enum variant tag; otherwise fields come directly.
4. **Sketch fields positionally — no `(key value)` pairs, no nested wrappers when every record has the same inner shape.** Positional means `(Decision [description] Maximum)`, not `(Decision (description [...]) (magnitude Maximum))` and not `(Decision (Description [description]) Maximum)` when `Description` is the only thing ever in that slot. Variants are PascalCase (`Maximum`, not `maximum`); date and time are two bare positional fields (`2026-05-19 01:23`), not one bracket string.

Most agent NOTA mistakes are the same mistake — labeled fields. The fix is the same: read the canonical example, and let the wrapping type carry the schema.

## When you fight the rules

You'll want to wrap every record in `(Item ...)` "for safety" — don't, the file is the safety. You'll want to group records under section comments — don't, surface the category as the type. You'll want integer codes "because they're shorter" — they're not, once you count the lookup table that decodes them; names win.

If the same structural decision recurs across many NOTA files (a shared enum vocabulary, a shared identity newtype, a shared date-shape), that's a real workspace primitive. Document it once in the relevant repo's `skills.md` or `ARCHITECTURE.md` and reference by name; don't restate it in every preamble.

## When to hand-write the codec instead of deriving

`#[derive(NotaDecode, NotaEncode)]` is the right default for record types. But the derive treats every `String` field as a bracket string — the conservative "any string" choice — which produces noisy NOTA for tokens that qualify as bare symbols.

The canonical case: a newtype around `String` whose content is always a NOTA-identifier-shaped name (no spaces, no special chars). The derive emits `(Public [Entry] (Struct ([Entry] ...)))`; the cleaner canonical NOTA is `(Public Entry (Struct (Entry ...)))`. Bracket strings should be reserved for content that needs them.

The fix: hand-write `NotaDecode` + `NotaEncode` on the newtype to inspect content and choose the emission form, using `nota_next::AtomClassification`:

```rust
impl NotaEncode for Name {
    fn to_nota(&self) -> String {
        if self.qualifies_as_symbol_name() {
            self.as_str().to_owned()
        } else {
            NotaString::new(self.as_str()).format()
        }
    }
}

impl NotaDecode for Name {
    fn from_nota_block(block: &Block) -> Result<Self, NotaDecodeError> {
        NotaBlock::new(block).parse_string().map(Self::new)
    }

    fn qualifies_as_symbol_name(&self) -> bool {
        AtomClassification::classify(self.as_str()) == AtomClassification::SymbolCandidate
    }
}
```

The decode side accepts both forms (bare symbol + bracket string) — the parser doesn't care; the encode side chooses. This keeps emitted NOTA round-trippable and human-readable. Anywhere the derive would emit a less-readable form than the canonical shape (per `AtomClassification`, per the bracket-string-only-when-needed rule), the hand-written impl is the right move — on schema-in-Rust source nouns and on emission-target newtypes alike.

## See also

- `skills/nota-schema-docs.md` — pseudo-NOTA convention for documenting record schemas in markdown (angle-bracket placeholders, optional `?`, enum `|`).
- `skills/skills.nota` — the canonical workspace example.
- `nota/README.md` — the language grammar source of truth.
