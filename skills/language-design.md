# Skill — language-design instincts

*The load-bearing commitments when designing a text notation, a
request language, a schema notation, or a query surface.*

---

## What this skill is for

Whenever a notation is being designed — Nota records, the Nexus
request language, a future query DSL, a config syntax for a
new tool — apply this skill before writing the parser. The
instincts below are what the workspace's working surfaces
(Nota, Nexus, signal IR) have converged on after the
language-design exploration in `aski` (retired but
inspirational; `aski/spec/design.md` has the original
articulations).

If you're not designing a notation — just *using* one already
defined — this skill isn't for you. Read `nota`'s `README.md`
or the relevant grammar spec instead.

The principles below are upstream of every existing notation
in the workspace. New notations either follow them or have a
named, defended reason not to.

---

## The instincts

### 1. Delimiter-first

Every construct has explicit opening and closing delimiters.
**The parser knows what it is reading from the first token.**
No fallback rules; no multi-token lookahead; no scanning the
interior to decide what kind of thing this is.

Concrete: `(Foo …)` is a record. `[…]` is a sequence. The
opening token determines the construct. If a notation needs
multi-token lookahead to decide what construct a fragment is,
the grammar has a missing surface — extract it as a separate
DSL with its own outer delimiter.

### 2. No keywords beyond truth values

Closed sigil and delimiter budgets. The parser dispatches on
position and head identifier — never on a reserved word. The
only literals that have meaning to the parser are `true`,
`false`, and `None` (the absent-value sentinel for `Option`).

New features land as new delimiter-matrix slots or new
PascalCase records. **Never as new keywords or new sigils.**
If a feature seems to demand a keyword, it's asking for a
typed record instead.

### 3. Position defines meaning

The same delimiter means different things in different
positions. The parse position is the sole authority. `()` at
record-head means "this is a record"; `()` inside a record
body might mean "a typed field"; `()` inside a body block
might mean "call arguments." Readers learn the position
rules once.

This is what removes the need for keywords. *Position* is
what carries meaning; *content* is what's positional.

### 4. PascalCase = type, camelCase = instance

The parser dispatches on first-character case. `Foo` is a
type, variant, or structural name. `foo` is a field name or
local instance. The case rule is **enforced at parse time** in
record-head position, not as a downstream convention. A bare
lowercase identifier in head position is a parse error, not a
schema mismatch.

This has cascading benefits: identifiers carry their kind
visibly; the lexer can dispatch without consulting the
schema; the reader knows what they're looking at without
context.

### 5. Names are meaningful

No pointer names — no `T`, `X`, `A`, `B` for type parameters;
no `x`, `n`, `tmp`, `buf` for locals. **Every name describes
what the thing IS.**

Type parameters use semantic role names: `$Value`, `$Output`,
`$Failure`, `$Left`, `$Right`. Two different parameters always
have different names — `$LeftValue` and `$RightValue` are
different even when they share qualities. Name IS identity.

The cost is a few extra characters at the declaration site.
The gain is that every use site reads unambiguously without
the reader reconstructing context.

### 6. Every value is structured — no opaque strings

If a name or type is stored as a flat string, the ontology is
incomplete. Names are typed domain variants; types are
structured node trees. As the schema grows, strings collapse
into typed records.

Opaque-string smells: `kind: String` where `kind` should be a
closed enum; `name: String` where `name` should be a typed
identifier newtype; `metadata: HashMap<String, String>` where
metadata is hidden control flow.

**Strings are transitional.** Each one in a schema is a
placeholder for a typed record not yet specified. The schema's
job is to grow them into types.

### 7. Newlines are not significant

Whitespace (including newlines) is only a token separator.
Parsing is purely token-based. `(Foo a b c)` and the
multi-line indented form parse identically. The structure of
the program lives in the delimiters, not in the whitespace.

Indentation-sensitive grammars (Python, YAML) get this wrong.
A parser that depends on whitespace can't recover from
formatting; a delimiter-driven parser can. Prefer delimiters.

### 8. Text is flat; trees come from the compiler

Text is a left-to-right, top-to-bottom medium. Every
text-based language is written as a flat sequence of tokens.
Trees are what the compiler constructs from the flat input.
**Grammar rules stay flat; structure lives in the compiler's
data tree.**

Don't try to make grammars hierarchical. The flat-input shape
is the nature of text; let the compiler do the structural work.

### 9. Content-addressing by canonical encoding

When a notation needs identity beyond the moment of writing,
identity is the hash of the canonical encoding. The canonical
form is itself defined: field order, whitespace, optional
emission, string quoting — all specified, all stable.

Mutable handles (slot-refs, named bindings) sit on top of the
content-addressed identity. The hash is the immutable
identity; the slot is the mutable handle.

### 10. No shortcuts in compiler work

No raw-text passthrough. No "skip for now" stubs. No partial
grammars. **When hitting a language limitation, extend the
language properly; don't work around it.**

Self-hosting requires the full grammar — the same grammar
that parses also reconstructs (bidirectional). Shortcuts
break round-tripping.

When the grammar feels like it can't express what's needed,
stop and design the language extension. The cost of a clean
extension is paid once; the cost of a passthrough is paid
every time the gap is encountered.

### 11. The parser stays small

Adding new typed kinds is the central activity of evolving
the schema. Adding new parser rules is the rare activity. New
syntactic territory becomes a new DSL surface — its own outer
delimiter, its own per-position semantics — not new
parser logic in the existing surface.

This is the antidote to grammar bloat. Each surface stays
locally decidable. The number of grammars grows; the
complexity of each one doesn't.

### 12. Mutable is marked

Immutability is the default. Mutation is always visible at
the declaration site. A mutability sigil (`~` in aski; `mut`
in Rust) attached to a name says "this can change"; absence
says "this is fixed." Readers don't need to scan ahead to
discover whether a value is mutable.

Mutation marks compose: `~&self` is "mutable borrow of self,"
combining the mutation marker with the borrow sigil. Each
piece is a separate decision; their combination is the
expressed shape.

### 13. No multi-field unnamed structs

Unnamed positional grouping (Rust's `(A, B, C)` tuple) loses
the name of each field. **If two values travel together,
they have roles, and those roles deserve names.** Use a
named-field struct.

Single-field newtypes (`struct Md5([u8; 16])`) are allowed —
they wrap one thing with a type marker, and the type marker
IS the name. Multi-field tuple structs are forbidden.

The cost is a few extra characters at the declaration site.
The gain: every use site reads unambiguously
(`result.quotient + result.remainder` vs `result.0 + result.1`).

### 14. Records are positional; field names live in the schema

Records on the wire are positional — no field names appear in
the text. The schema (in code) names the positions. This
keeps the wire form short and stable; renaming a field is a
schema change, not a wire-format change.

Tail-omitted optionals are a compatibility read-shape: a
decoder may accept a record missing trailing optional fields.
Canonical encoders emit explicit `None` for absent optionals.
Reordering fields IS a wire-format change (because positions
shift); plan accordingly.

### 15. Domains come from data — never hand-maintained

Every list of names, enum variants, or dispatch table in
source code is a bug. **Types are derived from declarative
data, never hand-written.** When a domain changes, the change
lands in one place — the data — and propagates.

Hand-maintained dispatch tables drift silently. A new variant
gets added to one table and missed in another; a renaming
breaks something three call-sites away. The fix is
generation, not vigilance.

### 16. Pure binary means pure binary

When a notation says "binary," it means actual byte values.
Not hex strings. Not JSON arrays of integers. Not
text-representations of any kind. **The bytes ARE the
protocol.** Hex, JSON, base64 are distinct projections of
binary, useful at boundaries; they are never the canonical
form.

### 17. Defined inputs and outputs

Every pipeline component has explicit, declared inputs and
outputs. A component can take multiple inputs of different
kinds and produce multiple outputs. **What matters is that
every input and output is named and typed.**

No "passthrough metadata," no "context object," no "carry
this along for the next step." If a step needs information,
it's an input. If a step produces information, it's an
output. The plumbing is part of the schema.

### 18. Delimiters earn their place

A delimiter pair belongs in the grammar only when records
and sequences (the universal structural primitives) **cannot
express the structural shape it would denote.** The test:

> *Can the wire form be made shorter or clearer for an
> expressive case that records + sequences + primitives
> can't handle?*

If no, the delimiter stays out.

Two failure modes a free delimiter pair tempts:

**Cosmetic distinctions.** Set vs. ordered list, map vs.
sequence-of-pairs — these differ semantically at the
receiving type's level, not at the wire's level. Adding a
delimiter for a cosmetic distinction grows the parser
without expressive gain. The schema-typed receiver already
encodes the distinction.

**Verb-shaped uses.** "Schema declaration" vs. "data";
"governance record" vs. "domain record"; "with-context"
wrapper. These encode operations into the delimiter — the
opposite of *position defines meaning*. Verbs go on record
head identifiers, never in delimiter pairs.

The structural minimum is records (`( )`) and sequences
(`[ ]`). A third delimiter pair (e.g., curly braces) earns
its place only when the language has a structural shape
genuinely outside this minimum that becomes load-bearing.

The trap: agents looking at a free delimiter reach for ways
to *use* it. The right discipline is to ask whether the
delimiter would express something records and sequences
can't. When the answer is no, the delimiter stays free —
the grammar earns simplicity through subtraction.

Cosmetic and verb-shaped temptations together cover most
proposals for "what a free delimiter could mean." Reject
both classes; keep the grammar small.

---

## Where these instincts live in working code

| Surface | Apply most directly to |
|---|---|
| nota | 1, 2, 3, 4, 6, 7, 8, 14, 16 |
| nexus | 1, 2, 3, 11 (extension surface), 14 |
| signal | 6, 9, 14, 15, 16 |
| persona-message records | 4, 5, 6, 14 |
| ESSENCE.md §"Language-design instincts" | distilled subset (older bullets — this file is the full 18) |

---

## When the rules feel restrictive

The friction usually means the schema is incomplete. The
right response is "find the typed shape that makes this
flow," not "add a string field" or "bend the rule once."
Fixed restrictions push design pressure into structure;
that pressure is the point. The notations work because the
authors held the line.

If a real exception is needed, it gets a name and lives in
the relevant grammar spec — the way nota's "bare-identifier
strings" carve-out is documented. Carve-outs are explicit and
narrow; absence of a documented carve-out means there isn't
one.

---

## See also

- nota's `README.md` — grammar spec for the canonical
  positional text format.
- this workspace's `ESSENCE.md` §"Language-design instincts"
  — distilled summary that this skill expands.
- this workspace's `skills/abstractions.md` — verb belongs to
  noun; same discipline at the Rust-type level.
- this workspace's `skills/naming.md` — full English words;
  applies inside notations as well as code.
- `aski/spec/design.md` — historical record of the
  exploration these instincts emerged from. Retired as an
  authoritative input to current work; preserved for context.
- this workspace's `skills/skill-editor.md` — how skills are
  written and cross-referenced.
