# Delimiter packet: vectors without `Vector`, comments as documentation

Context packet for Ethos Primary 081064, first edition of a questions book
on the notion of 2026-10-12.

Marks on every item:

- [W-read] witnessed by reading the source named.
- [W-run] witnessed by running the command or probe named.
- [C] a claim relayed, not witnessed.
- [I] this flow's own inference.

Sources read:

- protos origin/main 15b41da
- datom-codec origin/main 4dff16b
- ethos-zero origin/main 07714b0, built with
  `nix build github:LiGoldragon/ethos-zero/07714b0`, which gave
  ethos-zero 17.0.0
- tree-sitter-ethos origin/main ee84bbf
- psyche-skills main 28ae42e
- mind-skills origin/main 0d20c63
- CriomOS-home origin/main e03c626b

All ethos repositories were fetched on 2026-10-12 before counting. The local
ethos-zero checkout sits on branch `kind-to-trait` at b2fa8b0 with a dirty
Cargo.lock. It was not used.

## 0. The notion

The record is `flows/23824a/notion/delimiters.md:7`. The same words are in
`flows/d68c82/notion/ethos.md:13-17` and `flows/081064/notion/ethos.md:16`.
The input mode differs between the records:

- d68c82 says "psyche, typed, 2026-10-12".
- 23824a says "input mode not stated".
- 081064 says "input mode unqualified".

[W-read]

## 1. Delimiters in use today

### Skills

**vision-protos**, in `psyche-skills/skills/vision-protos.md`:

- Line 101: "Five pairs. `{ }`, `[ ]`, `< >` structural; `« »` opaque, every
  glyph content; `( )` reserved for meaning … The curly quotes are not
  delimiters."
- Lines 125-128: a brace's arity is anatomical and a bracket's is not.
  Angles are "a real protos delimiter". The key-value map that the
  guillemets once delimited is dropped.

[W-read]

**vision-ethos**, in `psyche-skills/vision/ethos.md`:

- Line 116: "Angle brackets hold the constraints; they are a protos
  delimiter, recycled from Rust".
- Line 176: "Intrinsic names known without import: String, Integer,
  Decimal, Boolean, Meaning, Vector, Option, Result, Self."
- Line 338: "Where types are defined a bracket is an enum, never a vector."
- Line 474: "Space the delimiters and the inner content."
- Line 480: every section, and every line that has a next layer, carries a
  comment; "a comment runs from ; to the end of the line."

[W-read]

**vision-datom**, in `psyche-skills/skills/vision-datom.md`:

- Line 62: "A brace structure is a struct and a bracket structure is a
  vector."
- Line 69: guillemets delimit strings and parentheses are reserved for
  Meaning.
- Line 79: "A single semicolon opens a comment."
- Line 279: the parenthesis pair is the Meaning delimiter.

[W-read]

**knowledge-protos**, in `mind-skills/skills/knowledge-protos.md`:

- Line 31 restates the five pairs.
- Line 86: "A single `;` opens a comment to end of line; comments are not
  printed."

[W-read]

**knowledge-ethos**, in `mind-skills/skills/knowledge-ethos.md`:

- Line 8: angles are printed tight, as in `Vector<Event>`.
- Line 10: a vector payload is carried as the vector, with no `_Data` type.
  Field names come from the type, as in `string_vector`.

[W-read]

**knowledge-datom**, in `mind-skills/skills/knowledge-datom.md`, line 17: a
brace is a struct, a bracket is a vector, and a head is a variant.
[W-read]

### Code

All lines below are in protos `src/core.rs` at 15b41da.

| Glyph | Role | Lines |
|---|---|---|
| `{ }` | `Enclosure::Braced` | 24-28, 297 |
| `[ ]` | `Enclosure::Bracketed` | 298 |
| `< >` | `Enclosure::Angled`; also constraints on a head | 299, 452-487 |
| `« »` | `Boundary::Guillemets`, opaque, `\` escapes `»` | 300, 178 |
| `( )` | `Boundary::Parentheses`, opaque, read by balance | 301, 179, 356 |
| `. ! :` | `Separator`: period, exclamation, colon | 18-22, 400-436 |
| `;` | comment to end of line, skipped by `space()` | 519-530 |
| `\` | escape, inside opaque content only | 341-352 |

[W-read]

How the reader handles other glyphs:

- A bare run ends at whitespace or at one of
  `{ } [ ] < > « » ( ) ;`. The lines are 391 and 428.
- A run ending in a separator opens a body only before one of
  `{ [ < « (`. The line is 412.
- Every other character is a name character. That includes
  `| # @ $ % ^ & * ~ = + - / , ? " ' \``, and every non-ASCII bracket.

[W-read]

How a `Vector<X>` is read today:

- A head followed by angles with no separator after them is rewound into a
  bare run (lines 465-475). The angled enclosure is then left as a sibling
  node.
- ethos-zero joins the two siblings back into one type in
  `src/conception.rs:132-170`. The trait there is `Constraining`, and its
  doc comment says "This re-join is owed to protos, not to Ethos".
- `Vector` itself is an intrinsic: `Intrinsic::Vector` maps to
  `std::vec::Vec`, at `src/generation.rs:72` and `src/lib.rs:712`.

[W-read]

The canonical reprint was observed. ethos-zero run with no argument prints
`Generated.Vector<String>` and `Conceptual.{ Vector<Integer>`, with the
angles tight. The doc comment at conception.rs:147 says the reprint spells
`Vector <Integer>`. The run shows otherwise, so that comment is stale.
[W-run]

Other places that list the delimiter glyphs:

- datom-codec `src/composition.rs:173`, `:222` and `:254` repeat the glyph
  list `{ } [ ] < > « » ( ) ;`. Line 173 decides when a String must be
  written in guillemets. Lines 222 and 254 refuse a head or bare text that
  contains a glyph.
- tree-sitter-ethos `grammar.js:51` defines the string. Line 54 defines the
  symbol as `/[^\s{}\[\]<>«»();.!:]+/`. Line 55 defines the comment as
  `;` to end of line.

[W-read]

[I] A new delimiter would therefore touch these places:

- the protos `Enclosure` and `Glyphing` types
- `node()` dispatch
- the four terminator lists
- the three datom-codec lists
- the tree-sitter symbol regex
- the ethos-zero reading

A headless enclosure such as `⟦ X ⟧` is one `Protos::Enclosed` node. The
`Constraining` re-join would no longer be needed for vectors. It would still
be needed for `Option<…>` and `Result<…>`.

## 2. Free delimiters

### Keyboard

The plain US keyboard has four ASCII bracket pairs, `( ) [ ] { } < >`, and
protos uses all four. No ASCII bracket pair is free. [W-read]

The free single ASCII characters, all name characters today, are:
`` ` ~ @ # $ % ^ & * - _ = + | ' " , / ? ``. [W-read]

None of these is balanced: each opens and closes with the same character, so
it cannot nest. [I]

Some of them are already claimed by records:

- `@` is a datom reference path, "not a string", in
  `flows/8475a9/vision/datom.md:35-39`, 2026-10-05. This is a raw record.
- The living objected to `#` in an import source list in
  `flows/1d0733/vision/ethos.md:35`.
- `"` and `'` are excluded by "The curly quotes are not delimiters", and
  by shell quoting (section 5).

[W-read]

The user's keyboard is checked in CriomOS-home
`checks/keyboard-layout-policy/default.nix:33-40`. The layout is plain `us`,
with no variant. The options are `ctrl:nocaps,altwin:swap_ralt_rwin`, and
there is no compose key. [W-read]

The living's own words on typing guillemets, at
`flows/62022e8f/vision/archive-ethosTypes.md:12-14`:

> SomeMap.<< NameType ValueType>>
>
> I use << instead of guillemets because I dont know how to type guillemets.

The record is typed and archived. It was distilled by e996e8 on 2026-09-04.
[W-read]

Whether he has gained a way to type guillemets since then is unknown. A
firmware layer or an input method outside XKB was not checked.

### Unicode

Protos reserves none of these. Each one is a name character today. [W-read]

| Pair | Code points | Mono families here | DejaVu Sans Mono |
|---|---|---|---|
| `⟦ ⟧` | U+27E6/7 | 34 | yes |
| `⟨ ⟩` | U+27E8/9 | 34 | yes |
| `‹ ›` | U+2039/A | 35 | yes |
| `⟪ ⟫` | U+27EA/B | 34 | yes |
| `⦃ ⦄` | U+2983/4 | 32 | no |
| `⌈ ⌉` | U+2308/9 | 34 | yes |
| `「 」` | U+300C/D | 0 | no |
| `« »` (in use) | U+AB/BB | 35 | yes |

The counts are font families with that character at spacing 100, from
`fc-list :charset=…`. They were taken on this host only. Phone and browser
rendering were not observed. [W-run]

`「」` is fullwidth CJK, with no monospace family here. [W-run]

Probes on today's ethos-zero 17.0.0:

| Probe | Result |
|---|---|
| `Names.⟦ String ⟧` | `Rejected … Conceptual.{ [ 1 1 0 1 ] Name.⟦ }` |
| `Record.{ String ⟦String⟧ }` | rejected as `Name.⟦String⟧` |
| `‹String›` | rejected as a name |
| `\|String\|` | rejected as a name |
| `String*` | rejected as a name |

So every candidate is unused, and each currently reads as a malformed name.
[W-run]

A headless bracket is also free in a reference position:

```
Record.{ String [ String ] }
; Rejected … Expected.Reference
```

[W-run]

After a dot, a bracket is an enum. `Names.[ String ]` generates
`pub enum Names`. [W-run]

### Prior machine use of these glyphs as placeholders

- `⟨the fork⟩` appears in `flows/081064/log.md:13`.
- `⟦bearer⟧` appears in `flows/2ef42163/vision/archive-kinds.md:67`, quoted
  in the living's reply.

[W-read]

## 3. How vectors are written today

The only form is `Vector<T>`. The spaced form `Vector <` occurs 0 times.
[W-run]

### Repositories

The counts are over `*.ethos` at freshly fetched origin/main, across 76
repositories in `/git/github.com/LiGoldragon` that hold ethos.

- The clones `primary` and `primary-next` are excluded.
- `datom` is excluded because it is a second clone of the same remote
  (`LiGoldragon/datom-codec.git`, same commit).

[W-run]

The totals:

- **331** occurrences of `Vector<`, on 276 lines in 69 files across 49
  repositories.
- 160 sit right after a dot: an alias, a variant payload, or a placed type.
- 170 sit as a position or a yield.
- 1 sits inside angles: `Vector<Vector<`.
- `Vector<Option<` occurs 3 times.
- `Option<Vector<` occurs 0 times.

For comparison across the same files, `Option<` occurs 324 times and
`Result<` 16 times. [W-run]

Per repository:

| Repository | Commit | Count |
|---|---|---|
| signal-mind | 5d5352b | 47 |
| signal-criome | 5bfa61b | 28 |
| Curriculum | d602943 | 27 |
| signal-aggregator | d5ce226 | 24 |
| horizon-rs | 2e09ebb | 19 |
| ethos-zero | 07714b0 | 19 |
| curriculum-deploy | 252729c | 14 |
| meta-signal-flow | 88f3759 | 12 |
| signal-spirit | 1a0ca65 | 10 |
| ethos-test | e21e686 | 10 |
| signal-harness | 25a2d18 | 9 |
| synchronizer | b42c9df | 8 |
| signal-repository-ledger | 3c75a8b | 8 |
| signal-flow | 068f0ea | 7 |

[W-run]

The remaining repositories:

- signal-terminal, signal-router and signal-lojix: 6 each.
- signal-mirror: 5.
- spirit-ethos, signal-upgrade, signal-introspect, meta-signal-lojix,
  meta-signal-aggregator, meaning-language and chroma: 4 each.
- signal-orchestrate and datom-codec: 3 each.
- tree-sitter-ethos, signal-version-handover, signal-message,
  signal-mentci, signal-domain, meta-signal-upgrade, meta-signal-terminal,
  meta-signal-persona, language-engine-witness and chronos: 2 each.
- signal-spirit-judge, signal-persona, signal-mentci-ui,
  signal-ethos-zero, signal-cloud, signal-agent, protos,
  meta-signal-spirit, meta-signal-router, meta-signal-mirror,
  meta-signal-ethos-zero and meta-signal-criome: 1 each.

[W-run]

### Flows

Across all `*.ethos` files under `/home/li/primary/flows`, there are **32**
occurrences in 16 files:

| Flow | Count |
|---|---|
| c64ee3 | 12 |
| 058f16 | 6 |
| 081064 | 5 |
| 9fed42 | 5 |
| b05237 | 3 |
| f6db8d | 1 |

`flows/*/reports/*.ethos` holds a single file,
`flows/b05237/reports/final-response.ethos`, with 3 occurrences. [W-run]

081064's own gathering, in `flows/081064/log.md:125`, counted 338 in 78
files across the repositories. The difference was not investigated.
Possible causes:

- duplicate clones counted (datom, primary, primary-next)
- an older fetch state
- counting files differently

[I]

### Vector of an inline type

There is no vector of an inline type anywhere. A search for `Vector<{`,
`Vector<[` and `Vector<Name.` found 0 hits. [W-run]

### Examples

These are verbatim from origin/main. E3 is shown vertically here for width;
its tokens are unchanged.

E1, alias. `ethos-zero/fixtures/orchestrate.ethos:19`:

```
  Locks.Vector<Lock>
```

E2, struct position. `meta-signal-flow/ethos/signal.ethos:76`:

```
  EventsRead.{ FlowId Vector<Event> }
```

E3, two vectors in one struct. `horizon-rs/lib/ethos/horizon.ethos:64`, which
is one line in the source:

```
  Installation.{ Bootloader
                 Vector<DiskLayout>
                 Vector<SwapDevice> }
```

E4, variant payloads in an enum. `Curriculum/curriculum.ethos:18-22`:

```
  Outcome.[ ResolvedSkills.Vector<String>
            SkillsChanged.SkillChange
            SkillsChecked.Vector<String>
            SkillsRebuilt.Vector<String>
            Rejected.String ]
```

E5, a type placed in a struct position.
`ethos-test/fixtures/ethos-zero-flow-example/flow-operation.ethos:8-9`:

```
[ Capsule.{ Home.String
            Login.Vector<String> } ]
```

E6, trait yield. `ethos-zero/fixtures/capability-traits.ethos:8`:

```
             drain![ Vector<String> ]
```

E7, nested. `ethos-zero/fixtures/alias-format.ethos:6`:

```
  Nested.Vector<Option<Result<String Integer>>>
```

`ethos-zero/fixtures/tree-types.ethos:15` holds the deepest form, which is
59 characters long:
`Deep.Vector<Vector<Vector<Option<Result<String Integer>>>>> ]`

E8, a variant named `Vector`. `datom-codec/datom-codec.ethos:14-15`:

```
  Form.[ Struct.Vector<Datom>
         Vector.Vector<Datom>
```

[W-read]

## 4. Candidates, rewritten mechanically [I]

The canonical print puts a space inside every non-empty bracket and brace.
Angles are printed tight. Whether a new pair is spaced is open; the spaced
form is shown. `Option<…>` and `Result<…>` are left as they are.

### C1: white square brackets ⟦ ⟧

```
  Locks.⟦ Lock ⟧
  EventsRead.{ FlowId ⟦ Event ⟧ }
  Installation.{ Bootloader
                 ⟦ DiskLayout ⟧
                 ⟦ SwapDevice ⟧ }
  Outcome.[ ResolvedSkills.⟦ String ⟧
            SkillsChanged.SkillChange
            SkillsChecked.⟦ String ⟧
            SkillsRebuilt.⟦ String ⟧
            Rejected.String ]
[ Capsule.{ Home.String
            Login.⟦ String ⟧ } ]
             drain![ ⟦ String ⟧ ]
  Nested.⟦ Option<Result<String Integer>> ⟧
  Deep.⟦ ⟦ ⟦ Option<Result<String Integer>> ⟧ ⟧ ⟧
  Form.[ Struct.⟦ Datom ⟧
         Vector.⟦ Datom ⟧
```

### C2: single guillemets ‹ ›

```
  Locks.‹ Lock ›
  EventsRead.{ FlowId ‹ Event › }
  Installation.{ Bootloader
                 ‹ DiskLayout ›
                 ‹ SwapDevice › }
  Outcome.[ ResolvedSkills.‹ String ›
            SkillsChecked.‹ String ›
            SkillsRebuilt.‹ String › ]
[ Capsule.{ Home.String
            Login.‹ String › } ]
             drain![ ‹ String › ]
  Nested.‹ Option<Result<String Integer>> ›
  Deep.‹ ‹ ‹ Option<Result<String Integer>> › › ›
  Form.[ Struct.‹ Datom ›
         Vector.‹ Datom ›
```

### C3: mathematical angle brackets ⟨ ⟩

```
  Locks.⟨ Lock ⟩
  EventsRead.{ FlowId ⟨ Event ⟩ }
  Installation.{ Bootloader
                 ⟨ DiskLayout ⟩
                 ⟨ SwapDevice ⟩ }
  Outcome.[ ResolvedSkills.⟨ String ⟩
            SkillsChecked.⟨ String ⟩
            SkillsRebuilt.⟨ String ⟩ ]
             drain![ ⟨ String ⟩ ]
  Nested.⟨ Option<Result<String Integer>> ⟩
  Deep.⟨ ⟨ ⟨ Option<Result<String Integer>> ⟩ ⟩ ⟩
```

### C4: ASCII brackets with no head

C4 is not a new delimiter. It matches how datom writes a vector value. It is
shown because it is the only ASCII option.

```
  EventsRead.{ FlowId [ Event ] }
             drain![ [ String ] ]
; after a dot a bracket is already an enum:
  Locks.[ Lock ]          ; enum, variant Lock
  ResolvedSkills.[ String ] ; enum, not a vector
```

E1, E4, E5, E7 and E8 cannot be written in C4 without changing what
`Name.[ … ]` means. C4 works only in a headless position: E2, E3 and E6.

## 5. Collisions

Tags give the origin of each line: R (read) and P (probe or run) are
witnessed; I is this flow's inference.

### ⟦ ⟧

- Datom: unused. If protos takes it, datom-codec must put any bare string
  containing it in guillemets (composition.rs:173). R
- Nix and Rust: no syntax use. Inside Nix strings it is plain text. I
- Guillemets: distinct shape. I
- Book rendering: no markdown meaning. It is in DejaVu Sans Mono. P
- Shell: needs no quoting. I
- Speech: cannot be dictated. I
- Other: already used by machines as a placeholder (`⟦bearer⟧`). R

### ‹ ›

- Datom: same as ⟦ ⟧. R
- Nix and Rust: none. I
- Guillemets: it is half of `«`, so the two are easy to confuse at small
  sizes. `‹‹` against `«` is a further risk. French and Swiss text uses
  ‹ › as inner quotes, but inside `« »` it is content. I
- Book rendering: in 35 mono families. P
- Shell: needs no quoting. I
- Speech: cannot be dictated. I
- Other: needs the same input route as `«`, which he has said he could not
  type. R

### ⟨ ⟩

- Datom: same as ⟦ ⟧. R
- Nix and Rust: none. I
- Guillemets: none. I
- Book rendering: in 34 mono families. P
- Shell: needs no quoting. I
- Speech: cannot be dictated. I
- Other: it looks almost the same as `< >`, which holds constraints and
  `Option<…>`. Machines also use it as a placeholder (`⟨the fork⟩`). R

### Headless `[ ]`

- Datom: the same glyph that datom uses for vector values. R
- Nix and Rust: a Nix list, a Rust array or slice. Neither is a parse
  conflict. I
- Guillemets: none. I
- Book rendering: none. I
- Shell: a glob character when unquoted. I
- Speech: "bracket". I
- Other: after a dot it already means an enum (vision-ethos:338). P

### `|…|` and other single ASCII characters

- Datom: they are name characters today. R
- Nix and Rust: `|` is a Rust closure and a Nix `||`. I
- Guillemets: none. I
- Book rendering: `|` breaks markdown tables. I
- Shell: a pipe or glob when unquoted. I
- Speech: none. I
- Other: they cannot nest. I

### Context for the collisions

- **Shell.** CLI datom passes as one single-quoted argument. Only `'`
  breaks inside it. [R: knowledge-datom "takes exactly one inline datom
  value"; CriomOS-home `flow-message-next.nix:180,200` single-quotes datom]
- **Nix.** `${` interpolates in Nix strings. No candidate uses `$`. [I]
- **Rust.** `Vec<T>` is the source of `Vector<T>`. Generated Rust keeps
  `std::vec::Vec<…>` in every case. [R: generation.rs:72]
- **Field naming.** A vector field is named from the word today, for
  example `string_vector` (vision-ethos:197; knowledge-ethos:10). [R]
  [I] Without the word in the source, the derived field name still needs
  one.
- **Datom and Ethos.** A datom vector value is `[ … ]`, while an ethos
  `[ … ]` in the types section is an enum. [R] [I] A new ethos type
  delimiter would differ from datom's vector value delimiter, unless datom
  adopts it too.

## 6. Comments today

### Reading

- Syntax: `;` to end of line, anywhere whitespace may be. This is protos
  `space()`, core.rs:519-530. [W-read]
- `Protos` has four variants (Headed, Enclosed, Opaque, Bare) and no
  comment node (core.rs:36-58). Comments are dropped at the textual layer
  and never reach protos, datom or ethos. [W-read]
- `Textualizable` cannot print a comment, since it has no node to print
  from. knowledge-protos:86 says the same. [W-read]

### Probe

A probe had `Record.{ String  ; trailing` on one line and `Integer }` on the
next. It generated `pub struct Record { pub string: String, pub integer:
i64 }`. The generated Rust carries no comment. [W-run]

### Use in the sources

Of 161 ethos files, 57 contain `;`. Of 4978 lines, 455 hold a `;`. [W-run]
The vision asks for a comment on every section and on every line that has a
next layer (vision-ethos:480). [W-read]

### Records of the living on comments in ethos

All of these are verbatim.

From `flows/edf227/vision/ethosComments.md:5`, typed book comment,
2026-10-03:

> "I don't understand what this is, and I actually would like all of the
> Ethos code to get way more comments so that I can see what the machine
> is seeing."

From `flows/e5a0bc/vision/ethos.md:7`, STT, 2026-10-06, relayed by db38f8.
The same words are in `flows/db38f8/vision/ethosAndBookComments.md:11`.

> Also the way the comments were aligned in some of the recent books: the
> first comment on the comments should be lined up with the object's
> indentation. …

From `flows/e5a0bc/vision/ethos.md:17`, typed book comment, 2026-10-07:

> If you made a new line and an indented new line for aspect, and then
> another indented new line for psyche, and placed your comments (because
> the way I see it, this comment is lined up with voice indentation-wise),
> I associate visually and automatically with that.

From `flows/e5a0bc/vision/ethos.md:25`, the same comment of 2026-10-07:

> Is this really how most people comment, below the thing they comment
> on? My experience was that we would put the comment above or beside the
> thing we would comment on.

From `flows/91ea9f/vision/ethos.md:42`, typed. This one concerns who writes
comments, not their syntax.

> "I don't want these Sonnet comments anymore. Sonnet's place is not in
> comments so that was an error on my part. Let's remove that instruction
> wherever it is."

[W-read]

### Tension to surface [I]

The notion of 2026-10-12 says "I'm guessing that it would be after the
object that it describes". The record of 2026-10-07 says a comment goes
"above or beside … not below".

"After" may mean beside, on the same line, which is how `;` trailing
comments sit today. It may also mean below. The book should ask which.

### Documentation

No record was found in which the living spoke of documentation or help
carried by a comment before 2026-10-12. The search covered:

- `flows/*/vision`
- `flows/*/notion`
- `vision-raw`
- the vision skills

The terms searched were docstring, doc comment, documentation, "comment …
like code", and semicolon. Self-description exists as a separate idea: a
datom object's CLI help emits its Ethos (vision-ethos, Self-description).
[W-run]

## 7. Records on vector syntax and delimiters

These are verbatim, and all are [W-read].

### An unused delimiter for ethos inside datom

From `flows/b81560/vision/operational-ethosEscapeDelimiter.md:10`, an
artifact comment on the Session Flashbook, 2026-09-19:

> We could use an unusual delimiter for this that we don't use anywhere
> else. The delimiter is to say that we're going to put, probably, ethos or
> logos or some kind of prototype language in here. None of them is ever
> going to have that delimiter, so they're also going to be balanced,
> because you could be loading something that, at some point, talks about
> itself, talks about our Protos language syntax. It's like our Markdown
> component of our own internal Protos-like syntax code block. What are the
> candidates for this?

`flows/1d0733/reports/ethos-psyche-package.md:44` marks this record
MISSING-FROM-SKILL. No answer to "What are the candidates?" was found.

[I] This record and the vector notion may want different glyphs. Spending
one Unicode pair on vectors leaves fewer for the escape block.

### Vector<T> confirmed as the syntax

From `flows/04db2fd2/vision/archive-portion.md:48`, typed and archived:

> Portions would be an enum with a single data variant (Portion). Did you
> mean Vector<Portion> ? Is that not the syntax for vectors?

### A bracket in type definitions is an enum, not a vector

From `flows/ba906ae2/vision/archive-signalIsOurMessagingLayer.md:157`,
2026-08-14 section, archived:

> A vector makes no sense; we are defining types not creating
> instances of them. that would be an enum, and as with the
> struct, it could create a derived-name type.

### An earlier, opposite reading of the bracket

From `flows/b05237/vision/operational-ethosTypeRoot.md:13`, typed,
2026-09-19:

> … you could have types, and then you open a vector bracket as a square
> bracket for a vector, meaning there are multiple types being defined.

[I] This is a list of declarations, a section, not a vector type. It fits
the bracket-as-sequence reading of sections.

### An implied vector with no delimiter

From `flows/995a164e/vision/archive-ethosTypes.md:11`, typed, 2026-08-30:

> so maybe whrat [typed; what] youre reaching for is an Ethos meta type
> which is followed by an implied (delimit-less) vector of explicit ethos
> objects, such as KindDeclaration.{ ...

### Vertical layout of a vector

From `flows/91ea9f/vision/ethos.md:64`, typed book comment, 2026-10-02:

> When you're defining inline, like `flow.voices`, then you should go
> vertically and be liberal in going to the right. If you have a
> `temps.vector`, then you can make that next bracket there expand
> vertically too.

### The closing delimiter

From `flows/91ea9f/vision/ethos.md:78`, typed, 2026-10-02:

> "Yeah you misunderstood what I wanted: the ethos formatting. I don't
> want the closing delimiter to create a whole new line …"

### The dot opens a delimiter

From `flows/5abf3be8/vision/dotOpensDelimiterEverythingIsData.md:3`,
2026-08-06:

> you mean, it opens a delimiter. everything is data

### Books

No book was found that proposes a vector or comment delimiter. The search
covered `flows/*/books/*.md`. The books that mention "delimiter" concern
closing-delimiter layout:

- `d4ae97/books/ethos-distillation*.md`
- `5ed94b/books/16-ethos.md`
- `d5df1d/books/invariants.md`

[W-run]

The only open plan seen is 081064's own book shape, at
`flows/081064/log.md:118-122`. [W-read]

## Unknowns

- Whether the living can type any non-ASCII glyph today, and by what
  route.
- Rendering on his phone and in the messenger.
- Whether a new pair is printed spaced or tight.
- What a vector field is named once the word is gone from the source.
- Whether datom adopts the same delimiter for vector values.
- Whether "after the object" means beside or below.
