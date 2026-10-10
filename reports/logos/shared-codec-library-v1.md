# Shared codec / stringless-Core library — v1

A grounded design answering the psyche's two verbatim statements this session:

1. On Core types — "all Core* have no strings, they use the corresponding
   NameTable" … "In fact i now seeing a pattern; this could go in a library".
2. "what if we agglomerate all the `split_at_first_dot` types of abstraction into
   a shared library/design surface for all the encoding/decoding that all the
   machinery does?"

The coordinator widened statement 2 this session: the agglomeration target is not
only the `split_at_first_dot` helper family but every parsing aspect of the
language family (delimiters included), unified as a **table-driven
structural-expectation mechanism** — the same mechanism by which schema's
semantically-generative delimiters, Nomos's structural macros, and logos's
reader-serving delimiters are all queries against one expected-shape table. Two
further psyche refinements (verbatim, from his exchange with Codex) sharpen that
table and are folded into §2.5 and decisions 7–9: (1) the table is **associated
with the Core types** — each complex Core* type carries its entry for how to expand
the next block, so the boundary's expected Core type IS the key; and (2) the table
is **bidirectional** — one entry per Core-type shape drives both encode and decode,
so round-trip coherence holds by construction instead of by two hand-kept codecs.

Written 2026-07-14 (session `nextgen-recrystallization`, lane
`shared-codec-library`, generalist, Opus 4.8, 1M). Read-only on all code
repositories; the one artifact this lane writes is this file. Sibling reports
this recrystallization builds on: `core-first-architecture-v1.md` (the Core-first
audit and phased bootstrap) and `syntax-recrystallization-audit-v1.md` (the
landed reshuffle, the derived-name rule, the dotted disambiguation).

Provenance discipline: **[observed — cite]** is a scout-verified file:line fact
from this session; **[interpretation]** is my reading; **[AGENT PROPOSAL]** needs
a psyche ruling and is collected in §5.

## 0. The one-paragraph thesis

Every layer of the machinery re-implements the same four families of
encode/decode abstraction — the dotted-text/delimiter discovery family, the
capitalization/derived-name family, the portable-rkyv + blake3-content-identity
family, and the expected-type decode-dispatch family — and each layer reinvents
them independently, so the copies have already drifted. The rkyv portable-feature
line alone is hand-restated in **33 separate Cargo.toml files** with no central
declaration; the signal frame codec is duplicated across **17 generated files**
that ignore the one shared codec they could call; there are **five structurally
identical `[u8;32]` digest newtypes** in sema-engine and a **sixth, incompatible**
blake3 domain-separation convention in schema; and the PascalCase-boundary
name-derivation loop is hand-written **twice** (schema and schema-rust) with a
third derivation implicit in Nomos accessors. The psyche saw a pattern; the
pattern is real and measurable. The design is a **small family of four layered
crates** with a strict one-directional dependency graph (stringless-Core never
depends on text), into which each of these repetitions collapses to a single
owning noun, plus the redirection of the existing `signal-frame` codec so the 17
copies call it instead of re-emitting it.

## 1. The repetition survey

Deliverable 1. Every recurring encode/decode abstraction found across the
machinery, grouped by shape, with paths, reinvention count, and observed drift.
Observations are cited to this session's scouts; interpretations are marked.

### 1.1 Dotted-text splitting / joining — the `split_at_first_dot` family

**[observed — nota `origin/next-gen` `08ce05c`]** The splitting primitive is
`Atom::split_text_at_first_dot(&str) -> Option<(&str, Option<&str>)>`
(`src/parser.rs:572-581`), with exactly **one** call site,
`DottedExpectation::read_string_entry` (`src/expectation.rs:97`). Its own doc
comment at `src/parser.rs:566` refers to a name `split_at_first_dot` that **does
not exist** — the psyche's remembered name is a stale doc link; the real method is
`split_text_at_first_dot`. The join/reconstruction side is
`Block::dotted_text(&self) -> Option<String>` (`src/parser.rs:248-257`), which
walks `Application{head,payload}` and rejoins with `.` (`format!("{head}.{payload}")`).

**[observed]** The join side is reused for two distinct purposes: numeric-literal
reconstruction — `NotaBlock::parse_numeric_text` (`src/codec.rs:454-460`) feeds
`dotted_text()` into `parse_integer` (`codec.rs:399`) and `parse_float`
(`codec.rs:437-444`), which is how `-122.3 = App(-122, 3)` is rejoined by the
Float codec — and a map-decode error path (`codec.rs:592`).

**[observed]** Period-bearing strings `(| |)`: encode is `NotaString::format`
(`src/codec.rs:492-509`), decode is `NotaBlock::parse_string`
(`src/codec.rs:376-393`), escape is `NotaString::escape_pipe_text`
(`codec.rs:517`), and the canonical-form guard is
`NotaString::reject_redundant_delimiter` (`codec.rs:513-520`), invoked from both
`parse_string` branches (`codec.rs:378,388`).

**[observed]** The `.`→`::` projection the reports describe **does not exist in
nota** (no such translation in `src/` or `derive/src/`). The nearest real code is
schema-rust's `import.source().module().replace('-',"_").replace(':',"::")`
(`schema-rust/src/lib.rs:996-999`) — which translates `:`→`::`, not `.`→`::`.
**[interpretation]** The `.`→`::` path-projection is designed but unimplemented;
it is a future logos-projection concern and belongs in the structural-codec
library (§2.3), not in any component today.

**Reinvention/drift:** one split primitive, one join primitive, both in nota; the
schema and schema-rust layers do path work by `:`-splitting on `Name`
(`schema.rs:27`) and string `replace` (`schema-rust/src/lib.rs:996-999`) rather
than reusing nota's dotted primitives — **[interpretation]** three different
notions of "split a qualified name" across three crates, none shared.

### 1.2 Delimiter / dotted-application raw discovery

**[observed — nota]** The raw structural model is `Block` with variants
`Delimited{delimiter,root_objects}` / `Application{head,payload}` /
`PipeText` / `Atom` (`src/parser.rs:57-80`). Right-associative dot binding is
`Parser::parse_object` (`src/parser.rs:716-746`): parse a primary, and on `.`
recurse into `parse_object` for the payload so `A.B.C = App(A, App(B,C))`.
`parse_primary` (`748-770`) rejects a leading dot; `at_primary_start`
(`772-783`) is the stop-gate; `parse_atom` (`848-863`) is the bare-atom scanner
that breaks on whitespace, `.`, any delimiter char, `;;`, or `|)`.

**[interpretation]** This is the "raw layer discovers structure only; the parser
never classifies" invariant (ruling 5) made concrete and tested. It is entirely
language-agnostic — it knows delimiters and dots, not schema/nomos/logos meaning —
and is the single richest asset to lift into a shared crate. It lives only in
nota today; schema re-parses `.schema` text through this same nota parser
(`schema/src/source.rs:31-33` → nota `Document::parse`), so schema already reuses
nota's raw layer rather than duplicating it — the one place reuse already works.

### 1.3 Capitalization classification

**[observed — nota]** `DottedExpectation::{Capitalized,Uncapitalized}`
(`src/expectation.rs:18-25`) with `accepts_head` checking
`is_ascii_uppercase`/`is_ascii_lowercase` (`expectation.rs:37-45`);
`Atom::qualifies_as_pascal_case_symbol` / `qualifies_as_camel_case_symbol`
(`src/parser.rs:592-609`) with thin `Block` delegations (`parser.rs:218-225`);
a case-kind enum consulted in `src/macros.rs:714-715`; and
`StructuralVariantShape::PascalHead*` recognition in nota-derive
(`derive/src/lib.rs:1177-1192`).

**[observed]** Drift: `derive/src/lib.rs:912` uses a **raw** `.is_ascii_uppercase()`
inline rather than routing through the shared `Atom`/`Block` predicates — a second
capitalization test not going through the canonical classifier
(scout flagged it unconfirmed whether it is a genuinely different concern).

**[observed — schema]** schema **delegates** capitalization to
`nota::AtomClassification::classify` (`schema/src/schema.rs:68`) plus
`Name::qualifies_as_pascal_case` (`schema.rs:75-82`) — partial reuse, one local
predicate.

**Reinvention/drift:** the classifier exists once canonically in nota and is
reused by schema, but has at least one raw-inline bypass inside nota-derive.

### 1.4 Derived-name rule (snake_case / PascalCase / SCREAMING_SNAKE)

**[observed — schema]** `Name::field_name(&self) -> String`
(`schema/src/schema.rs:50-65`) is an inline char-by-char PascalCase→snake_case
converter (no crate, no shared helper). It has **16 call sites** across three
files — `declarative.rs` (7: lines 1854,1878,1886,1902,1909,1976,1994),
`schema.rs` (2: 2750,2766), `source.rs` (9: 2371,2500,2524,2555,2571,2580,2597,
3395,3413) — and the pattern is not just "derive a name" but "derive then compare"
(`name.field_name() == derived.as_str()`), reimplemented independently per file.

**[observed — schema-rust]** `ScreamingName::screaming(&self) -> String`
(`schema-rust/src/lib.rs:2178-2204`) is a **second, independently written**
PascalCase-boundary walker — structurally the same loop shape as
`Name::field_name` but emitting SCREAMING_SNAKE instead of snake_case.

**[observed — nota-derive]** No case conversion at all: field decode is strictly
positional by numeric index (`derive/src/lib.rs:338-350`); an explicit
`#[nota(name = "...")]` uses the literal attribute string, never a derived form.

**[observed — syntax audit D11, `syntax-recrystallization-audit-v1.md:196-206`]**
The **same** derived-name rule recurs a third time for Nomos macro accessors: an
input shape `{ Name Type }` yields lowercase accessors `name`, `type` by the same
snake_case derivation.

**Reinvention/drift:** the boundary-walking case converter is hand-written **twice**
(schema `field_name`, schema-rust `screaming`) with a **third** derivation implicit
in Nomos accessors — three sites, two concrete copies, one loop shape.
**[interpretation]** This is the sharpest single instance of the psyche's "pattern":
one rule, three homes, zero sharing.

### 1.5 Bare-vs-delimited string decisions

**[observed — nota]** `NotaString::qualifies_as_bare_string_atom`
(`src/codec.rs:505-513`) is the needs-quoting predicate; the char-level base rule
is `AtomCharacter::is_bare_string` (`src/parser.rs:958-967`), and
`AtomCharacter::is_symbol` (`parser.rs:954-956`) is **literally the same predicate
under a second name** (`self.is_bare_string()`). `NotaString::format`
(`codec.rs:492-509`) is the encode decision tree (bare atom / `(word)` /
`(|escaped|)`); `reject_redundant_delimiter` (`codec.rs:513-520`) enforces
canonical form at decode.

**Reinvention/drift:** one canonicalization rule, but **two names for the identical
char predicate** (`is_symbol` == `is_bare_string`) — the mildest drift, a naming
duplication rather than a logic fork.

### 1.6 Expected-type-driven decode dispatch

**[observed — nota]** `NotaDecode::from_nota_block(&Block) -> Result<Self, _>`
(`src/codec.rs:119-121`) dispatches per expected type. Collection codecs live on
`NotaCollection`: `parse_vector` (`codec.rs:558`), `parse_map` (`codec.rs:576`,
requiring `Map.( … )` application with `DottedExpectation::Uncapitalized` entries),
`parse_option` (`codec.rs:616`, `None`/`Some.payload`). Primitive impls delegate
to `NotaBlock` helpers (`parse_string` 376, `parse_boolean` 465). nota-derive
generates one `from_nota_block` per type — positional-by-index
(`derive/src/lib.rs:338-350`) — and `StructuralVariantShape`
(`derive/src/lib.rs:1178-1186`) is the variant-shape vocabulary
(`PascalAtom`/`Keyword`/`Headed`/`PascalHead`/…).

**[interpretation]** This is the mechanism the coordinator's widened statement 2
points at. Each derive-generated `from_nota_block` is a **hard-coded
structural-expectation entry** for one type; the `StructuralMacroNode` "particular
default" that fires on an unknown `Head.{ … }` in a types section is a per-section
**default** entry. Generalized, these are rows in one table keyed by
`(language, context, expected-type/head) → structural shape (delimiter, arity,
pair-shape, codec)`. Today the table is frozen into generated derives, so a
dialect cannot add a row without regenerating code — the exact opposite of the
"infinitely programmable" property the syntax audit §4.2 claims for the stack.

**[observed — the encode/decode PAIR drift]** decode and encode are **two
independent bodies** per type: `NotaDecode::from_nota_block` (`codec.rs:119-121`)
and `NotaEncode::to_nota` (`codec.rs:123-125`) are separate traits, `to_nota` is
hand-written for the primitives across roughly twelve impls
(`codec.rs:655,667,679,691,703,715,727,739,751,827,903`), and **nota-derive
generates the two as separate impls** (`NotaDecode` at `derive/src/lib.rs:12`,
`NotaEncode` at `:18`, plus `NotaDecodeTraced` at `:30`). **[interpretation]** Two
hand-kept directions per type is exactly the round-trip drift the psyche's
bidirectional-table refinement (§2.5) removes: one entry per Core-type shape, both
directions derived from it, so decode and encode cannot disagree by construction.

**[observed — PrettyLayout is an additive projection, not a codec]** `PrettyLayout`
(nota `src/pretty.rs:72-75`) carries only `line_width` and `indent_unit`; it is a
**pure whitespace reflow over already-encoded canonical text** — it re-parses the
canonical line, adds line-breaks/indentation by delimiter depth, and re-parses to
the identical block tree, "never touch[ing] atom content, string escaping, or
delimiter shape" (`pretty.rs:8-14`). `NotaOutputForm{Canonical,Pretty}`
(`pretty.rs:36-39`) is the single print-shape decision. Critically, its own doc
comment (`pretty.rs:16-21`) names the end state: it is "a structural interim of
the macro-derived formatter the schema stack envisions (Spirit `5p9s`): a formatter
that reads line-break and indentation intent from **each macro's own pattern**."
**[interpretation]** the code already points layout intent into the per-pattern
entry — which is exactly where the bidirectional table puts it (§2.5).

### 1.7 Portable rkyv feature discipline

**[observed]** The exact feature line
`rkyv = { version = "0.8", default-features = false, features = ["std",
"bytecheck", "little_endian", "pointer_width_32", "unaligned"] }` appears
**verbatim** in nota (`Cargo.toml:17`), schema (`Cargo.toml:23`), sema-engine
(`Cargo.toml:17`), signal-frame (`Cargo.toml:26`), and — per the signal scout —
**33 separate `signal-*/Cargo.toml` files**, with **zero** central declaration
(these are separate git repos, not one Cargo workspace, so there is no
`[workspace.dependencies]` to share). signal-standard even pins a **different**
schema-rust generator rev than signal-schema (`rev` vs `branch = "trueschema"`) —
a second drift axis.

**[observed — sema-engine]** The one clean single-sourced artifact is the
`EngineStoredValue` / `EngineStoredRecord` trait bound
(`src/record.rs:153-198`) — the full portable archive+deserialize+bytecheck bound,
blanket-impl'd so callers never restate it, with **no engine-specific type in the
bound itself**. **[interpretation]** directly liftable; the single best seed for a
shared foundation crate.

**[observed — nota]** rkyv is derived on 14 types in `src/macros.rs` but has
**zero** `to_bytes`/`from_bytes`/`access`/`deserialize` call sites — the binary
path is derived and never exercised (corroborates
`core-first-architecture-v1.md:59-68`).

**Reinvention/drift:** one feature-discipline concept, **34+ independent
declarations**, one clean centralizable bound used by exactly one crate.

### 1.8 blake3 content-hash derivation

**[observed — schema]** `ContentHash::derive(HashDomain, bytes)` using
`blake3::Hasher::new_derive_key(domain.context())` (`src/identity.rs:69-73`);
`HashDomain` is a typed enum `{TrueSchema, FamilyClosure}` with `.context()`
returning versioned domain strings (`identity.rs:35-47`);
`TrueSchema::content_hash` folds `to_binary_bytes()` rkyv bytes
(`identity.rs:158-162`), explicitly not source text.

**[observed — sema-engine]** **No** `ContentHash::derive` and **no** `HashDomain`
enum. Instead: `EntryDigest::update_bytes(hasher, bytes)` length-prefixes then
hashes (`src/versioning.rs:299-302`) — the one genuinely reusable primitive — and
domain separation is done by **freeform `&'static [u8]` string literals with a
manual version suffix** baked at each of 5 call sites
(`"sema-engine-versioned-commit-log-entry-v2"`, `"…-checkpoint-segment-v1"`,
`"…-view-digest-v1"`, `"…-store-schema-hash-v1"`, `"…-checkpoint-v1"`). There are
**five structurally identical `[u8;32]` newtypes** — `EntryDigest`,
`SegmentDigest`, `CheckpointDigest`, `SchemaHash`, `StoreSchemaHash`
(`versioning.rs:64-138,245-303`; `checkpoint.rs:100-170`) — each with
`new`/`bytes`/hex-`Display`. And `SchemaHash::for_label` uses `blake3::hash`
directly with **no** domain-separation prefix (`versioning.rs:85-87`) — a third
in-crate convention.

**[interpretation]** Two incompatible blake3 domain conventions across the stack
(schema's typed-enum + `new_derive_key`; sema-engine's freeform-prefix +
`update_bytes` length-prefix), plus a bare-`blake3::hash` third form, plus five
duplicate digest newtypes. Ruling 3 (blake3 over stringless Core rkyv,
NameTable excluded, layout-version-tagged) has no single home to land in — it must
be **built** by unifying these, not lifted from any one of them.

**[observed]** nota has no hashing code at all (confirmed absent).

### 1.9 Name interning (would-be NameTable)

**[observed]** `NameTable` and `CoreSchema` **do not exist** anywhere
(zero hits in schema and schema-rust `src/`; one aspirational prose mention,
`schema-rust/ARCHITECTURE.md:524-525`, "a `Rename` edit touches only the
`NameTable`"). schema stores identifiers as `Name(String)`
(`schema/src/schema.rs:15`) embedded verbatim in every declaration — **123**
`: Name` field/parameter sites across nine source files. There is **no**
interning or index indirection.

**Reinvention/drift:** greenfield — the pattern the psyche named directly
("all Core* have no strings, they use the corresponding NameTable") is
un-built everywhere; the drift is that identifiers-as-owned-strings are scattered
across 123 sites with no owning abstraction.

### 1.10 Frame / wire codec

**[observed — signal-frame]** `ExchangeFrame`/`StreamingFrame` with
`encode`/`decode`/`encode_length_prefixed`/`decode_length_prefixed`
(`src/frame.rs:225-303`), `ShortHeader(u64)` 8-byte little-endian
(`frame.rs:10-42`), and a `ClientFrame` trait that **reuses** the frame codec
(`src/command_line.rs:456-479`). This is the intended single shared frame codec.

**[observed — the doubling]** schema-rust's codegen template
(`schema-rust/src/lib.rs:2042-2062`) emits `encode_signal_frame`/`decode_signal_frame`
plus a **local** `SIGNAL_SHORT_HEADER_BYTE_COUNT = 8` (`lib.rs:5440`) into every
consumer, and that output is checked into **17** separate `src/schema/lib.rs`
files (signal-introspect, -lojix, -domain-criome, -cloud, -listener, -agent,
-mentci-client, -upgrade, -persona, -criome, -schema, -router, -mirror, -terminal,
-orchestrate, -mentci, -message). **None** call `signal_frame::ExchangeFrame::encode`
despite several declaring `Frame = signal_frame::ExchangeFrame<Input,Output>`
aliases that go unused (`signal-schema/src/schema/lib.rs:718`); each hand-rolls
`rkyv::to_bytes`/`from_bytes` + the 8-byte header with its own `SignalFrameError`
distinct from `signal_frame::FrameError`. The runtime path actually exercised is
the generated copy (`schema-rust/src/daemon_emit.rs:1559`), not `signal-frame`.

**Reinvention/drift:** one shared codec exists and is bypassed by 17 generated
copies of an equivalent-but-separate codec with its own header constant and error
type.

### 1.11 Survey summary table

Positional NOTA-style ledger `(shape sites concrete-copies drift)`:

```
[ (DottedSplitJoin        nota          1-split-1-join  stale-doc-name-and-3-notions-of-name-split)
  (RawDiscovery           nota          1               language-agnostic-reused-by-schema)
  (CapitalizationClassify nota+schema   1-canonical     1-raw-inline-bypass-in-derive)
  (DerivedNameRule        schema+schema-rust+nomos  2   3-homes-1-loop-shape)
  (BareVsDelimited        nota          1               2-names-for-1-predicate)
  (ExpectedTypeDispatch   nota          per-type-derive frozen-table-not-extensible)
  (EncodeDecodePair       nota          2-traits-2-derives  round-trip-drift-per-type)
  (RkyvFeatureDiscipline  everywhere    34+             zero-central-1-clean-bound)
  (Blake3ContentHash      schema+sema-engine  2-conventions  5-duplicate-digests-3-conventions)
  (NameInterning          nowhere       0               greenfield-123-string-sites)
  (FrameCodec             signal-frame  1-plus-17-copies bypassed-shared-codec) ]
```

## 2. The library design

Deliverable 2. His phrasing allows one library or a small family; I decide a
**small family of four layered crates** plus redirection of the existing
`signal-frame`, and justify the count in §5 decision 1. The forcing reason is the
ruling itself: **stringless-Core must never depend on the text codec**, and a
single crate cannot honor that — so the boundary is a dependency-direction fact,
not a preference. The four crates are stacked so each arrow points down and no
arrow ever points from Core up into text.

### 2.1 The dependency graph

```
                  structural-codec   (text bridge: raw + expectation table)
                    |            |
        raw-discovery            name-table   (stringless-Core: Identifier + NameTable)
              |                        |
              +----------> content-identity  (portable rkyv bound + ContentHash<Domain>)
                                       ^
                                       |
   sema-engine, signal-frame, CoreSchema/CoreNomos/CoreLogos all depend UP into this
```

- `content-identity` depends only on `rkyv` + `blake3`. **No strings, no text.**
- `name-table` depends on `content-identity`. Holds names as data; **no text codec.**
- `raw-discovery` depends only on `rkyv` (its `Block` is archivable). **No Core dep.**
- `structural-codec` depends on `raw-discovery` + `name-table`. **Text depends on
  Core; the reverse never occurs.**
- `signal-frame` (existing) depends on `content-identity` for the shared bound.

The Core language types (CoreSchema, CoreNomos, CoreLogos, in their own repos)
depend on `content-identity` + `name-table` and **never** on `raw-discovery` or
`structural-codec`. That is the whole ruling, enforced at crate-dependency level.

### 2.2 Crate 1 — `content-identity` (the portable-archive + content-hash foundation)

Contains, each collapsing a repetition from §1:

- **The one portable rkyv bound.** Lift `EngineStoredValue`/`EngineStoredRecord`
  (`sema-engine/src/record.rs:153-198`) verbatim as the canonical archive
  discipline. The feature-set string still appears per-Cargo.toml (Cargo cannot
  inherit features across separate git repos), but the **bound** — the thing that
  actually constrains a type to be portably archived and validated-on-read — lives
  **once** here and every consumer imports it. Closes §1.7 (34+ restatements).
- **`ContentHash<Domain>`** — one generic `[u8;32]` newtype with `new`/`bytes`/
  hex-`Display`/`derive`, collapsing sema-engine's five duplicate digest newtypes
  (§1.8) and schema's `ContentHash` into one type parameterized by domain.
- **`HashDomain`** — the typed, closed, layout-version-tagged domain enum
  realizing ruling 3. Adopts schema's typed-enum + `new_derive_key` shape
  (`schema/src/identity.rs:35-73`) and lifts sema-engine's `update_bytes`
  length-prefix primitive (`versioning.rs:299-302`) as the internal folding
  primitive. Unifies the two-plus incompatible blake3 conventions (§1.8) behind
  one type. The layout-version tag is a field of the domain, not a manual string
  suffix.
- **`ContentHash::of_core(value, domain)`** — the ruling-3 derivation: blake3 over
  the stringless Core's canonical rkyv bytes, **NameTable excluded** (it is not in
  the Core value), domain-separated and layout-tagged. Rename-stability falls out
  because names are not in the pre-image.

Dependency direction: leaf. No strings. Candidate names — **`content-identity`**,
`archive-identity`, `portable-digest`.

### 2.3 Crate 2 — `name-table` (the stringless-Core Identifier + NameTable pattern)

The library the psyche named directly in statement 1. Contains:

- **`Identifier(u32)`** — the index every Core type uses in place of a string.
  Owns nothing but its representation; the noun that carries meaning is the table.
- **`NameTable`** — `Identifier -> Name`, interned, append-only, with methods
  (verb-belongs-to-noun, §3): `intern(name) -> Identifier`, `resolve(id) -> &Name`,
  `extend_from(&NameTable) -> NameTable` for the **continuous identifier space**
  (the logos table is a higher-index append-extension of the schema table, so a
  carried-over schema identifier keeps its exact index — ruling 2 and
  `core-first-architecture-v1.md:213-218`).
- **`Name`** and the **derived-name methods on it** — `field_name()` (snake_case),
  `screaming()` (SCREAMING_SNAKE), `pascal_case()` — the **one** home for the rule
  that is hand-written twice today (§1.4). schema's `Name::field_name` migrates in;
  schema-rust's `ScreamingName::screaming` is **deleted** and becomes a sibling
  method; Nomos accessors call the same methods.
- **The True-projection trait** — `Named<Core>`: `project(core, name_table) ->
  TrueX`. The named view is **derived on demand, never stored** (inverts today's
  stored-`TrueSchema`). This is the trait CoreSchema/CoreNomos/CoreLogos implement.

Note: `name-table` holds strings (the `Name` values are data), but depends on **no
text codec** — names are substance, parsing is not. This is the precise boundary
the ruling draws. Candidate names — **`name-table`**, `identifier-space`,
`stringless-core`.

### 2.4 Crate 3 — `raw-discovery` (the language-agnostic structure layer)

Lift from nota's parser (§1.2). Contains the `Block` model
(`Delimited`/`Application`/`PipeText`/`Atom`), balanced-delimiter scanning,
right-associative dotted-application binding (`parse_object` /
`at_primary_start` / `parse_atom`), the `split_text_at_first_dot` +
`dotted_text` dotted-pair primitives (§1.1), and the capitalization classifier
(§1.3, with the raw-inline bypass at `derive/src/lib.rs:912` routed through it).
This layer **discovers structure and never classifies meaning** (ruling 5) — it
has **no dependency on Core**, so a consumer wanting only structure (a linter, a
formatter, a tree-sitter bridge) uses it alone. nota keeps its parser by importing
it from here; schema keeps reusing it transitively. Candidate names —
**`raw-discovery`**, `positional-structure`, `delimiter-discovery`.

### 2.5 Crate 4 — `structural-codec` (the bidirectional structural-expectation table, associated with the Core types)

The agglomeration target of statement 2, refined this session by the psyche's two
verbatim points: the table is (1) **associated with the Core types** — "the complex
Core types are associated with their respective structural-parsing table for how to
deal with the next block to be expanded" — and (2) **bidirectional** — "this table
is used both for encoding and decoding to-from true/core to text form." Both are
folded in below; the framing that follows is my design (AGENT PROPOSAL, §5 decisions
7–8), the two invariants in quotes are his words.

**The table is keyed by the Core type, and the entry travels with it.** The
expected-type-at-every-boundary invariant (ruling 5) becomes **literal data**: at
any boundary the expected Core type IS the key into the table, and the entry says
how to deal with the next block to expand at that position. So the structural
expectation is not a free-standing registry the codec consults by string; it is a
property of the Core-type shape — the noun that owns "how I am structured" is the
Core type itself (verb-belongs-to-noun, §3). Concretely:

- **`StructuralExpectation`** — the entry: delimiter kind, arity, pair-shape
  (positional / `key.Value` / `Vis.name.Type`), capitalization expectation, the
  leaf codec, and (see below) the layout intent. It is **associated with a
  Core-type shape**, reached as `core_type.structural_expectation()` rather than a
  free `lookup(table, key)`.
- **`ExpectationTable`** — the association from Core-type shape → entry, the thing a
  language/dialect/section **populates**: schema's declarations generate entries
  (its "semantically generative delimiters"), Nomos's structural macros **are**
  entries/defaults (a dialect adds an entry without regenerating a derive), logos's
  reader-serving delimiters are entries. One mechanism; three populators;
  per-language/section variation (delimiters included) is just which entries exist.
  This is the beauty claim: schema-generative-delimiter, nomos-structural-macro, and
  logos-delimiter dissolve into **one** noun — a Core-type's structural expectation.

**One entry drives both directions.** Decode (`text → Core`) and encode
(`Core → text`) are derived from the **same** `StructuralExpectation`, so
`decode(&Block, &mut NameTable) -> CoreValue` and `encode(&CoreValue, &NameTable)
-> Block` cannot disagree — round-trip coherence by construction, not by two
hand-kept codecs. This directly retires the pair drift observed in §1.6: today
`NotaDecode`/`NotaEncode` are two independent bodies per type and nota-derive
emits them **separately**; here there is one entry and two derived directions.

**nota-derive becomes a generator of ENTRIES, not of codec code.**
**[AGENT PROPOSAL]** Today nota-derive generates four codec impls per type
(`derive/src/lib.rs:12,18,24,30`); under this design it generates one
`StructuralExpectation` entry per Core-type shape, and the single shared text
bridge in this crate reads that entry in both directions. This is the beautiful
resolution of the §1.6 and encode/decode-pair findings: the derive stops emitting
two divergeable codec bodies and emits one data entry; the codec logic lives once,
in the library, not regenerated per type. It also restores the "infinitely
programmable" property (syntax audit §4.2): a dialect adds an entry, never a
regenerated derive.

**Layout composes with the table, and migrates into it.** The canonical encode
direction produces the byte-stable single-line form every golden depends on;
`PrettyLayout` (§1.6, `nota/src/pretty.rs`) is today an **additive** pure-whitespace
reflow **over** that canonical text — it composes on top and is not part of the
table. But the code's own cited direction (Spirit `5p9s`, `pretty.rs:16-21`) is a
"macro-derived formatter that reads line-break and indentation intent from each
macro's own pattern" — i.e. layout intent as **per-entry data**. So the honest
reading: **layout composes today** (canonical encode from the table, plus an
additive `PrettyLayout` pass), and **layout intent migrates into the entry** at the
envisioned end state (the entry gains a break/indent-policy field, and `PrettyLayout`
becomes the shared engine that renders that per-entry intent rather than a fixed
width rule). Both live in this crate; the entry is the single home for both
structure and, eventually, layout.

**Also owned here:** the canonical text decisions — bare-vs-delimited (`NotaString`
logic, §1.5, `is_symbol`/`is_bare_string` collapsed to one), the `(| |)`
period-string rule, the derived-name **elision** at projection (D2:
core carries every field name; text elides it when it equals `snakeCase(Type)` —
`syntax-recrystallization-audit-v1.md:70-92`), and the `.`→`::` path projection
(§1.1) when logos lowering is built — projection is this crate's job.

Depends on `raw-discovery` + `name-table`. Candidate names — **`structural-codec`**,
`expected-shape`, `text-bridge`.

**Genuine tension to flag, not force.** The entry is "associated with the Core
type," yet `structural-codec` (text) may not be depended on by the Core types (the
ruling: Core never depends on text). These reconcile only if the **entry type
itself is stringless-Core-shaped** — the association lives on the Core side (an
`Identifier`/index the Core type carries, or an entry stored in `name-table`-level
data), while the **codec that reads the entry in both directions** lives in
`structural-codec`. So the entry is Core-resident data; the bidirectional
interpretation of it is text-side behavior. If instead the entry must carry
text-codec closures, the dependency would invert and the split (decision 2) would
need revisiting. This is the one place the two refinements press on the dependency
graph, and it is a real design fork, resolved below as decision 8.

### 2.6 `signal-frame` — reused, not rebuilt

Not a new crate. `signal-frame` already **is** the shared frame codec (§1.10);
the library work is **redirection**: schema-rust's codegen template
(`schema-rust/src/lib.rs:2042-2062`) stops emitting a private
`encode_signal_frame`/`SIGNAL_SHORT_HEADER_BYTE_COUNT` and instead emits a call to
`signal_frame::ExchangeFrame::encode`; the 17 checked-in copies regenerate to
call-sites; `SignalFrameError` collapses into `signal_frame::FrameError`.
`signal-frame` depends on `content-identity` for the shared bound. No language
migration is involved — this is pure duplication removal at the codegen layer.

### 2.7 Consumer map

Positional NOTA-style `(consumer what-it-gets what-it-deletes)`:

```
[ (nota           [raw-discovery structural-codec content-identity-bound]
                  [local-parser-as-sole-owner dead-unexercised-rkyv-path])
  (schema         [name-table content-identity structural-codec]
                  [Name-String-at-123-sites field_name-copy local-ContentHash])
  (schema-rust    [name-table.screaming structural-codec signal-frame-call]
                  [ScreamingName-walker frame-codegen-template])
  (nomos-new      [name-table content-identity structural-codec-entries] [nothing-built-yet])
  (logos-new      [name-table content-identity structural-codec-projection] [nothing-built-yet])
  (sema-engine    [content-identity-bound ContentHash<Domain>]
                  [EngineStoredValue-lifted 5-duplicate-digest-newtypes])
  (signal-*x33    [content-identity-bound signal-frame-call]
                  [rkyv-bound-restatement generated-frame-codec-copy]) ]
```

## 3. Design-surface coherence — verb belongs to noun, drift cannot recur

Deliverable 3. The family is beautiful only if every reusable verb attaches to the
one noun that owns it, so there is nowhere for a second copy to grow.

- **Interning belongs to `NameTable`**: `name_table.intern(name)`,
  `.resolve(id)`, `.extend_from(other)` — never a free `intern(table, name)`. The
  continuous-space extension is a method on the table that owns the allocation.
- **The derived-name rule belongs to `Name`**: `name.field_name()`,
  `name.screaming()`, `name.pascal_case()` — the affordance advertises what a name
  can spell itself as. The two hand-written walkers (§1.4) become sibling methods
  on one noun; a future SCREAMING or kebab form is a method, not a fourth loop.
- **Content-hashing belongs to the value via its domain**:
  `core_value.content_hash(domain)` delegating to `ContentHash::of_core`; the
  layout-version tag is a field of `HashDomain`, so "which layout" is impossible to
  forget — it is in the type, not a `&'static [u8]` suffix a writer must remember
  to bump (the sema-engine failure mode, §1.8).
- **The expected/raw contact point is named `ExpectedShape`**, not scattered
  through the codec as match arms and capitalization `if`s. Decode is
  `expected_shape.decode(block)`; the enum-vs-enum cross-product lives in one place
  (per `enum-contact-points`), so a new construct is a new row, not a new branch
  threaded through every codec.
- **Structure-discovery belongs to `Block`/`Parser`**: `block.dotted_text()`,
  `block.as_application()` — the raw layer's verbs are methods on the raw nouns,
  and it is a separate crate so a consumer physically cannot reach a Core type from
  inside it.

How drift is prevented: each of the ten repetitions in §1 has exactly **one**
owning noun after the migration, and the dependency graph makes the wrong home
un-typable — schema-rust cannot re-grow `ScreamingName` because `Name::screaming`
is the only `screaming` in scope; a signal-* crate cannot re-grow a frame codec
because the codegen emits a `signal-frame` call; a new digest cannot become a
sixth `[u8;32]` newtype because `ContentHash<Domain>` is generic. The single
source is enforced by ownership and dependency direction, not by discipline alone.

## 4. Bootstrap impact

Deliverable 4. Library-first inserts a **Phase L** beneath the phased bootstrap of
`core-first-architecture-v1.md` (A Core-ify NOTA → B Core-ify schema → C Nomos +
Logos → D self-hosting), and de-risks every later phase by making the foundation
proven before any language is rewritten.

- **Phase L1 — extract `content-identity` first, from sema-engine.** sema-engine is
  the one already-Core-first component (`core-first-architecture-v1.md:160-187`),
  so lift its clean `EngineStoredValue` bound and collapse its five digest newtypes
  into `ContentHash<Domain>` **against working code and its own locked-byte tests**
  (`sema-engine/src/record.rs:200-263` pins exact digest bytes). sema-engine
  becomes the **first consumer** — the library is validated before it is trusted.
  This is the keystone: decisions 2/3/6 of `core-first-architecture-v1.md` all lean
  on the content hash, and here it gets a real, tested home.
- **Phase L2 — build `name-table`** (greenfield; small). Unblocks Phase B, since
  CoreSchema needs `Identifier` + `NameTable`. Migrate schema's `Name::field_name`
  in; delete schema-rust's `ScreamingName`.
- **Phase L3 — extract `raw-discovery` from nota's parser.** This **is** Phase A's
  substance (re-seat text as projection): nota keeps its parser by importing it;
  the shared crate now exercises the rkyv round-trip nota never did (§1.7).
- **Phase L4 — build `structural-codec`**, seeded by nota's `NotaDecode` collection
  codecs and the derived-name/capitalization/bare-vs-delimited rules. Consumed by
  schema at Phase B and by Nomos/Logos at Phase C, so the expectation-table
  mechanism exists before the languages that populate it.

Then Phases A–D proceed as in the sibling report, but each becomes "component X
**consumes** the library and **deletes** its local copy," with the schema-rust
byte-exact golden fixtures (`schema-rust/tests/emission.rs:20-27`, 9 fixtures) as
the unchanged oracle throughout — the Rust output must not move while the
substance migrates into shared crates.

**Migrates into the library:** nota parser → `raw-discovery`; nota `NotaDecode`
collection codecs → `structural-codec`; schema `Name::field_name` → `name-table`;
schema `identity.rs` `ContentHash`/`HashDomain` → `content-identity`; sema-engine
`EngineStoredValue` + five digest newtypes → `content-identity`.

**Gets deleted as duplicates:** schema-rust `ScreamingName` (§1.4); the 17
generated `encode_signal_frame` copies (§1.10); the 34+ rkyv-bound restatements
collapse to the shared bound (§1.7); sema-engine's five digest newtypes → one
generic (§1.8); nota-derive's raw-inline capitalization check
(`derive/src/lib.rs:912`) and the `is_symbol`/`is_bare_string` double name (§1.5).

**Built new:** the four crates; the continuous NameTable extension mechanism; the
`ExpectationTable` that lets a dialect add a row without regenerating a derive.

## 5. Decision points requiring psyche ruling

Deliverable 5. Each carries an [AGENT PROPOSAL] with a one-paragraph rationale.

**Decision 1 — one library vs a family.**
**[AGENT PROPOSAL]** A **family of four layered crates** (`content-identity`,
`name-table`, `raw-discovery`, `structural-codec`) plus reuse of `signal-frame`,
not a single library. Rationale: the settled ruling that stringless-Core must
never depend on the text codec is a **dependency-direction** constraint, and one
crate cannot express it — the whole point would be lost. The boundaries are not
arbitrary: they fall exactly where the dependency needs differ —
`content-identity` has no strings at all, `name-table` has names but no codec,
`raw-discovery` has structure but no Core, `structural-codec` sits on top of both.
That difference is the micro-component split test (distinct nouns, distinct
bounded vocabularies, independently testable). A monolith would also force every
consumer of just the hash discipline (sema-engine, signal-*) to pull the text
parser, which is precisely the coupling the design removes.

**Decision 2 — the raw / expectation split (crates 3 and 4 separate, or one
two-module crate).**
**[AGENT PROPOSAL]** **Separate crates.** Rationale: `raw-discovery` has zero
dependency on Core (it is pure text structure), while `structural-codec` depends
on `name-table`; that dependency difference is the boundary signal. Keeping raw
discovery its own crate honors the "parser never classifies" invariant at the
crate level — a structure-only consumer (formatter, tree-sitter bridge, linter)
links raw discovery without dragging in Core or the expectation machinery. If the
psyche prefers fewer moving repos, the fallback is one crate with a hard internal
module boundary, but the clean answer is two.

**Decision 3 — crate names.**
**[AGENT PROPOSAL]** Two-to-three candidates each, lead choice first, full English
words per the naming rule: Crate 1 **`content-identity`** / `archive-identity` /
`portable-digest`; Crate 2 **`name-table`** / `identifier-space` /
`stringless-core`; Crate 3 **`raw-discovery`** / `positional-structure` /
`delimiter-discovery`; Crate 4 **`structural-codec`** / `expected-shape` /
`text-bridge`. Rationale: each lead name states the crate's single capability as
the noun it owns; `name-table` is the psyche's own word from statement 1, and
`structural-codec` names the mechanism (structural expectation) rather than a glyph
(`split_at_first_dot`) so it does not date.

**Decision 4 — where the library repos live.**
**[AGENT PROPOSAL]** **New standalone repositories** under `repos/`, each
independently buildable and published like the `signal-*` contracts, consumed
across repos by **named portable identity** (published version or tag), never a
sibling `path = "../.."` dependency. Rationale: micro-components' dependency
discipline forbids path deps across separate repos (they break in clones and
sandboxes), and these crates are consumed by nota, schema, schema-rust, nomos,
logos, sema-engine, and 33 signal-* crates — the widest fan-in in the stack, so
portability is mandatory. New repos are justified per repository-management
(distinct nouns, distinct bounded vocabularies, independent test surfaces). No
repo is created under this read-only lane; this is the proposal for the psyche's
authorization.

**Decision 5 — lift `content-identity` from sema-engine as consumer-zero.**
**[AGENT PROPOSAL]** **Yes** — extract the foundation crate from sema-engine's
`EngineStoredValue` bound and its digest newtypes, and make sema-engine the first
consumer. Rationale: it is the cleanest single-sourced artifact in the whole survey
(§1.7), it comes with locked-byte regression tests
(`sema-engine/src/record.rs:200-263`) that prove the lift is behavior-preserving,
and validating the library against the one already-Core-first component before any
language rewrite is the highest-leverage de-risking move available. It also forces
the two-plus blake3 conventions (§1.8) to reconcile at the start rather than after
three languages have each picked one.

**Decision 6 — how to reconcile the two blake3 domain conventions without breaking
sema-engine's storage.**
**[AGENT PROPOSAL]** Adopt schema's **typed `HashDomain` enum + layout-version
tag** as the shared shape and lift sema-engine's **`update_bytes` length-prefix**
as the internal primitive; but preserve sema-engine's **existing domain strings as
specific `HashDomain` variants** so its on-disk digests do not move. Rationale:
changing sema-engine's freeform domain literals (e.g.
`"sema-engine-versioned-commit-log-entry-v2"`) would change every stored content
hash — a storage-format break (`rust-storage-and-wire`). Making those exact strings
into named enum variants gives the shared type without changing the bytes, so the
special case dissolves (one `HashDomain` type) while byte-compatibility holds. New
Core hashes (ruling 3) get fresh layout-tagged variants. Any digest change beyond
this is a versioned storage change and must be flagged as such, not slipped in.

**Decision 7 — the table is associated with the Core types and is bidirectional
(fold the psyche's two refinements).**
**[AGENT PROPOSAL]** Adopt both as the design center: each complex Core* type is
associated with one `StructuralExpectation` entry (the expected Core type at a
boundary IS the table key), and the **same** entry drives decode and encode — one
entry per Core-type shape, both directions derived. Consequence: **nota-derive
becomes a generator of entries, not of codec bodies** — it emits one
`StructuralExpectation` per type instead of separate `NotaDecode`/`NotaEncode`
impls (`derive/src/lib.rs:12,18`), and the single shared bridge in `structural-codec`
reads it both ways. Rationale: this is the psyche's own words made structural, it
removes the round-trip pair-drift observed in §1.6 by construction, and it restores
the dialect-extensibility the syntax audit §4.2 claims. This is the strongest single
simplification the refinements unlock; recommended for adoption now.

**Decision 8 — where the entry lives, given Core-must-not-depend-on-text.**
**[AGENT PROPOSAL]** The **entry is stringless-Core-shaped data** (carried on the
Core side, e.g. an index the Core type holds or entry data at `name-table` level),
and the **bidirectional codec that interprets the entry** lives in `structural-codec`
(text side). Rationale: "associated with the Core type" (his refinement 1) and "Core
never depends on the text codec" (the settled ruling) both hold only if the
association is Core-resident data while the reading-of-it is text-side behavior; the
Core type points at its expectation, the text bridge reads that expectation in both
directions, and no arrow runs from Core up into text. The tension is real (§2.5): if
the entry must instead carry text-codec closures, the dependency inverts and the
raw/expectation split (decision 2) must be reopened. Flagged, not forced — this fork
turns on whether the entry is data or behavior, and I propose **data**.

**Decision 9 — layout: compose now, migrate into the entry later.**
**[AGENT PROPOSAL]** Keep `PrettyLayout` as an additive whitespace pass over the
canonical encode output for now (it composes, it does not join the table), and plan
to move layout **intent** into the `StructuralExpectation` entry at the end state the
code already names (Spirit `5p9s`, `pretty.rs:16-21`), with `PrettyLayout` becoming
the shared engine that renders per-entry break/indent intent rather than a fixed
80-column rule. Rationale: the canonical single-line form is the byte-stable golden
oracle and must not move; layout is legitimately additive today; but the code's own
stated direction puts break/indent intent per-pattern, which is exactly a field of
the bidirectional entry. Compose today, absorb at the end state — no premature move.

## 6. Observations vs interpretations — separation ledger

Per the return discipline, the load-bearing split:

- **Observed (cited, this session's scouts):** every path:line in §1; the counts
  (34+ rkyv restatements, 17 frame copies, 5 digest newtypes, 16 `field_name`
  sites, 123 `: Name` sites, 2 case-walkers, ~12 hand-written `to_nota` bodies);
  the absence facts (no `NameTable`, no `CoreSchema`, no `ContentHash::derive` in
  sema-engine, no `.`→`::` in nota, zero rkyv call sites in nota); the one clean
  bound (`EngineStoredValue`); the encode/decode PAIR being two separate traits and
  two separately-generated derives; `PrettyLayout` being a pure additive whitespace
  projection whose own doc comment (`pretty.rs:16-21`) names the per-pattern
  macro-derived formatter as the end state.
- **The psyche's words (his, verbatim, this session):** Core types are associated
  with their structural-parsing table for how to deal with the next block to expand;
  the same table is used for both encoding and decoding to-from true/core to text.
- **Interpretation (mine):** that these constitute one four-family pattern; that
  the per-type `from_nota_block` derives are a frozen expectation table; that the
  crate split falls on dependency-direction differences; that
  schema-generative-delimiter / nomos-structural-macro / logos-delimiter are one
  noun; that nota-derive should generate entries not codec bodies; that the entry is
  Core-resident data while the bidirectional codec is text-side behavior; that
  layout composes now and migrates into the entry later; the whole of §2–§5 as a
  proposed design.
- **Needs psyche ruling:** decisions 1–9 in §5, all marked [AGENT PROPOSAL].

## 7. Sources

Design corpus (this workspace): `reports/logos/core-first-architecture-v1.md`,
`reports/logos/syntax-recrystallization-audit-v1.md`,
`reports/logos/nomos-macro-model-v1.md`, `design-v0.md`.

Code ground truth (read-only this session, cited inline in §1): nota
`origin/next-gen` `08ce05c`; schema detached `36a79b7`; schema-rust `main`
`87de872`; sema-engine `main` `fa3a822`; signal-frame / signal-schema /
signal-standard / signal-derive at their checked-out `main`. Repositories under
`repos/` are untracked; no code was edited and no branches were switched.
