# Context handover — 2026-07-27

This file supersedes the Codex-authored 2026-07-27 handover. A fresh Codex
session boots from this one.

Sources, in authority order. Later psyche statements govern earlier ones.

1. `/git/github.com/LiGoldragon/protos-engine/design/ProtosEngine/SliceOneRulings-2026-07-27.md`
   — firsthand session log, 2026-07-27, entries 1 through 9. Controls the exact
   wording of everything ruled today.
2. `/git/github.com/LiGoldragon/protos-engine/design/ProtosEngine/ShapeAndSliceRulings-2026-07-26.md`
   — firsthand session log, 2026-07-26 plus its entry 8, which belongs to the
   2026-07-27 session and precedes entry 1 of the file above. Controls the exact
   wording of every overlapping 07-26 entry.
3. `/git/github.com/LiGoldragon/protos-engine/design/ProtosEngine/ProtosEngineDesign-2026-07-26.md`
   — the compiled log. Source for the older quotes. Secondhand for R1 through R5;
   the Shape and Slice log is firsthand for those.
4. `/home/li/primary/reports/CodexCorrection-2026-07-26-second.md` — block-model
   rulings A through D, the blocking problems, the slice state.
5. `/home/li/primary/reports/ShortIdentifierRuling-2026-07-26.md`
6. `/home/li/primary/reports/CodexShapeRemediation-2026-07-26.md`

Provenance marks used throughout, on every claim:

- **[ruled]** — verbatim psyche words, copied character-exact from a source file.
- **[confirmed]** — a restatement the psyche confirmed as his; the substance
  carries his authority, the wording may be an agent's or a partial rendering.
- **[derived]** — agent-formalized standing doctrine, consistent with rulings but
  not his words. A derived line is never cited back to him as a ruling.

## Psyche vision

The aim is to rebuild the engine's invariants with correct provenance under them.
Everything below is either his word or marked as not his word.

### 1. The two organs, and text as an interim interface

The engine has two organs and one shared mechanism over them.

**[ruled]** on the vision's shape, from
`reports/logos/textual-form-vision-design-v1.md`, recorded there as psyche
verbatim:

> "I had a great vision for a shared abstraction around textualform and
> encodedform (use to be called true/core)"

> "The vision had associated data-tree (which we thought belongs in the
> textualform) to drive most of the structural encoding/decoding of the text."

> "a nametree and a structuretree"

> "textualform trait writes and reads the name and structure trees"

> "this drives all textual en/decoding, including rust"

> "actually, the vision even allowed multiple textualforms per encodedform;
> logos -> logos or logos -> rust"

> "even nota can take this architecture; it would be the basic/most-universal
> example."

**[confirmed]**, entry 9 of `SliceOneRulings-2026-07-27.md`. A full provenance
sweep (design logs, the reports tree, every repo under the ghq root) found no
file containing the sentence that heads every summary of this system. Asked
whether the sentence is his words, the psyche confirmed verbatim: "yes. those
are my words". The sentence stands as psyche-confirmed by that 2026-07-27
confirmation, not as a located firsthand transcript:

> "nametree and structural tree from the protos library drive all the decoding
> and encoding to/from text with DATA - strict invariant. nothing else will
> do."

The verified words above corroborate the substance — the nametree and the
structuretree drive all textual en/decoding, including Rust.

**[ruled] 07-23**, the shared mechanism, from the compiled log:

> "I want a shared mechanism (either a trait, type, whatever) for all of this
> structure-based decoding which is re-used by all the different parts of the
> machinery that do parsing (and deparsing would use a parallel shared
> machinery)"

**[ruled] 07-23**, what the traits must force:

> "the textualform traits should force the use of structural data"

**[ruled] 07-23**, on the term itself, when an agent called textual-rust "the
bypass":

> "I dont agree with that choice of words. we call it textualform, so you're
> disagreeing with the terms USED IN THE CODE.
>
> You're VERY confusing and windy right now. I dont like it. I think I gave you
> too much context and its confusing you"

**[ruled] 07-23**, that the hand-written Rust reader/printer is being *replaced*,
never *rejected*:

> "Reject in my words? Wtf are you talking about? NO!"

> "right, so how is that rejecting it? That's DEMANDING it, you moron
>
> WTF are you saying I rejected. I dont fucking trust you fucking monkeys"

**[confirmed]**, entry 8 of the 07-26 firsthand log, confirmed by him on
2026-07-27 with "yes, those are my words": TextualForm and EncodedForm — "one is
a view on the other".

**[ruled] 07-21**, text is the interim interface, not the program:

> "I dont like this analogy. text is the current standard programming interface;
> it is what we *must* work with in order to get to the future interface"

**[confirmed]**, same entry 8: "Exactness is structural. Values that matter
semantically must have exact representations… Errors are also structural
values." The log flags this as a partial rendering of a longer turn whose full
text is not recoverable; his 2026-07-27 confirmation establishes it as a ruling,
not as a firsthand transcript.

### 2. The two-pass block model

**[ruled] 07-26**, dictated by him after being shown that the shipped
textual-decode replacement was refused. Verbatim in full:

> "Okay, so let's go over this together. In all languages there's blocks. And
> these blocks can be represented by typed data, which is what we have, the
> encoded form. Plus their names, right? The capsule. So in a protose language,
> the delimiters are very straightforward. And all one has to do is balance them
> out to find the beginning and the end of blocks, along with, I would say, the
> prefix to the opening delimiter, right? Which we have the dotted prefix. So the
> first pass, and I actually wanted to do this, and I've talked about this
> before, and I thought, well, I don't assume that my designs are being
> implemented anymore. But in my mind, because agents have proven that they can't
> follow my instructions yet, I think because my system isn't complete enough
> yet, not because the models are not capable, but because the ontology isn't
> there yet, and the structure, and the memory system, and everything isn't
> properly set up. So we're doing a lot of this by hand. I'm repeating myself
> now, but I'm going to go deeper. So there's a logic to finding the beginning
> and the end of each blocks. And so we could say that we have different variants
> of block delimiters, of finding the beginning and the end of a block. And I
> know that Rust is more particular because there's a lot more rules that are
> involved in balancing out, so to speak, the delimiters. They don't really have
> delimiters, but there's inclusive and exclusive delimiters, I would say. So
> when we look at a Rust block, let's say it starts with struct. Struct is the
> beginning cue, right? It's the cue that there's a struct block that begins
> here. And to find the end, we have to follow all of the parsing rules that
> apply inside of a struct, that could possibly apply inside of a struct, to find
> the final semicolon. Meaning if we come across certain things, then there's a
> certain number of semicolons that have to be skipped, right? So we could say
> this is an inclusive, meaning the struct keyword is part of the block. It's an
> inclusive complex block. And then we have exclusive. On the other side of the
> spectrum, we have exclusive simple blocks, in which the delimiter is not really
> part of the block in the sense that when we want to parse the inside of it, we
> don't need to look at the delimiters, which are parentheses and braces and
> square brackets. But we do have the prefix, which is a bit of a trick, because
> actually we could say that there's no such thing as an exclusive block because
> of the dotted prefix. The dotted prefix, the word, the prefix word is part of
> the data of the block. So we should just look at it as a whole, including the
> parentheses and the square brackets and so on. It's just the logic for finding
> the end of the block is different. And that inside logic, which can also, by
> the way, find the inner blocks. Because as it looks for clues to tell it that
> it needs to skip some more closing delimiters, it also finds other blocks. So
> we could have sort of this recursive block beginning and ending pass, which has
> different logic for different languages, which is really simple for the Protus
> family of languages. And then with that pass done, then we can do the typed
> parsing, because we've found the blocks. It's a lot easier to just pass these
> strings now, which are limited to only their content, and parse them through
> the structural typed parsing step."

**[ruled] 07-26**, ruling B — the block tree is a trait. Agent: "The block tree
itself can be one universal shape — bounds, cue/prefix, children — because it
carries no typing at all". Psyche:

> "so it should be a trait. we love traits; they make agents smarter by giving
> them an ontology (that could go in standards, in a better presented form)"

**[ruled] 07-26**, ruling C — pass-1 opacity. Agent: "In pass 1 for Rust, the
scan must still treat strings and comments as opaque (a ';' inside a string
literal terminates nothing)?" Psyche:

> "yes"

**[ruled] 07-26**, ruling D — source bounds. Agent: "The block tree keeps source
bounds so every later error can point at bytes?" Psyche:

> "yes"

**[derived]** — the architecture these four rulings fix, as formalized in the
second correction report:

- Pass 1 is recursive **block discovery**, driven by per-language block-boundary
  rule *data*, never by full grammar.
  - Protos family: balance delimiters; the dotted prefix word is part of the
    block's data. There is no truly exclusive block — prefix plus delimiters plus
    content is one whole; only the end-finding logic is simple.
  - Rust-like: cue-opened, rule-terminated, **inclusive** — the cue (`struct`,
    `enum`, `fn`, …) is inside the block; the end is found by following only the
    termination rules, i.e. what changes how many semicolons or closers to skip.
    While scanning for its own end, this logic also discovers inner blocks. That
    is the recursion.
  - Carriers (strings) and comments are opaque to pass 1 (ruling C).
  - Every discovered block carries source bounds (ruling D).
  - The block tree is one universal shape expressed as a **protos trait**
    (ruling B): bounds, cue/prefix, children, content — no typing. Per-language
    discovery logic yields per-language implementors.
- Pass 2 is the existing expectation-driven **typed structural parsing**, run per
  block over content-bounded text, producing EncodedForm plus NameTree — the
  capsule.

The block-model ruling B parenthetical names traits as a *standards candidate
only*. It authorizes no standards change.

### 3. Structural parsing laws

**[ruled] 07-24**, boundary-first:

> "structural parsing doesnt reacting blindly on characters; it has a
> state-machine to de/parse the type by finding the outside boundaries first, and
> passing through the inside of that block again and again, recursively and
> structurally."

**[ruled] 07-22**, expected-type payload delegation. Agent: "the expected type at
each position picks the parsing." Psyche:

> "so that expected type needs a payload attached with it when it has a custom
> structure-based logic, and the method for parsing will pick it up when
> non-empty"

**Two corrections against the Codex handover this file supersedes.**

- **Do not carry "explicitly denies horizontal parsing" as a psyche quote.** No
  source file contains it. The boundary-first quote above is the psyche text on
  that subject; use it and nothing else.
- **Do not state a longest-match law, and do not state a longest-match ban.** The
  compiled log records the global longest-match law under "Derived rulings — not
  psyche words", with this note: no explicit reply to that exact question was
  found in the read source; a later same-session message treats the law as
  already driving implementation, so his assent is implicit in what follows, not
  a captured verbatim yes. It is listed under open questions below. Neither
  assert it nor forbid it — ask.

**[derived]** — conservative refusal, in the ratified-requirement phrasing from
`reports/CodexResumePrompt-TypedRules-2026-07-26.md`: disjointness is proven over
typed positions; two rules are disjoint at the first position where their types
cannot accept the same text. What cannot be proven disjoint is rejected. "You
gain proof power through types, never by weakening the check." Stop-the-line
holds: an undecidable case is surfaced, never order-resolved and never
special-cased.

### 4. Typed data laws

**[ruled] 07-26**, shown Codex's rendering of the newtype grammar as
`Product["struct", name, (...), ";"]`:

> "wtf is this garbage? Thats a vector of strings, not typed data! it should be
> fully typed struct."

**[ruled] 07-26**, offered the fork — (1) fully typed rule records, rust-logos
defining a typed vocabulary with typed positions and disjointness proven over
them, versus (2) keep the generic protos vocabulary and teach the prover
positional comparison:

> "1"

**[ruled] 07-26**, R3, kernel reach. Note the delegated form of the assent — he
handed the judgment back rather than exercising it, so do not cite this as an
independent psyche conviction. Agent: does the typed-record ruling reach the
protos kernel itself, accepting the content-hash/layout bump now while the
digests have zero consumers; recommended yes. Psyche:

> "if you think it's a good idea, then yes."

Ruled yes: one deliberate layout bump, now, before slice 1 gives the hashes
consumers.

**[ruled] 07-26**, R4 scope. Agent presented three families with
recommendations — type-ids yes, wire contract IDs no, short codes yes. Psyche:

> "ok"

Ruled: `ScopedEncodedTypeId` and `EncodedConstructorId` become
language-variant-wrapped u16 with private fields; signal-frame `ContractId` does
not change; short codes gain the kind dimension. Clause 3's stored-value
elaboration is superseded by the short-identifier rulings (section 10).

**[derived, ratified-adjacent]** — the R2 requirement set, from the typed-rules
resume prompt, which he has not contradicted:

- rust-logos defines a typed rule vocabulary. Each grammar rule is a typed record
  whose positions are typed — for the newtype item: Attributes, Visibility,
  ItemKeyword, TypeName, Parenthesized(TypeReference), Terminator. No homogeneous
  `Vec<StructuralForm>`, no literals-at-indexes, no position counting.
- The shared evaluator runs this vocabulary alongside the protos primitives. Same
  evaluator, second driven vocabulary — not a parallel engine, not hand-written
  match arms.
- Item grouping is a typed boundary rule of the Rust structuretree: an item's
  extent is found structurally — attributes, then head, then the matching
  terminator (semicolon or balanced brace) — boundary-first, preserving nested
  `#[...]`, parens, and braces.
- The typed-position disjointness proof replaces the product-blind comparison for
  this vocabulary only. The protos-primitive prover's behavior for existing
  tables is not modified.
- Spellings live as data **on** typed positions (ItemKeyword carries "struct"),
  never as bare strings in a sequence.

**[derived standing law]** — no `syn`, `quote`, or `prettyplease` anywhere on the
pipeline. This is grounded in "the textualform traits should force the use of
structural data" plus his demand that the hand-written reader/printer be
*replaced* ("That's DEMANDING it"), not in a verbatim ban. He never said the
crate names. Treat the law as standing; do not attribute the sentence to him.

**[ruled] 07-24**, one permitted concession. Agent: may rust-logos contain one
hand-written, Rust-specific evaluator object — parsing and emission as methods on
that real object — while every individual TextualForm remains sealed structural
data? Psyche:

> "sure, if you think that's a good first MVP"

### 5. Names and identity

**[ruled] 07-19**, on `<visibility-field>.Public`:

> "THERE ARE NO FIELDS NAMES!
>
> ALL FIELDS ARE POSITIONAL!
>
> FIELD NAMES ARE ALMOST NEVER ALLOWED!
>
> WRITE IT SOMEWHERE YOU WONT FORGET!
>
> MAKE PROTOS SKILL CORRECT, AND MAKE IT A PART OF MANAGER!
>
> I NEVER WANT TO SEE THIS AGAIN!"

**[ruled] 07-19**, when an agent excused a named-leg example as legacy dialect:

> "the legacy dialect had the same field-name illegality. so you double fucked up
>
> ok im certain now; field names are now COMPLETLY ILLEGAL EVERYWHERE"

**[ruled] 07-22**, quoting back the agent's own named-field struct example before
rejecting it:

> "No, we won't give the fields names. They are deterministically named in the
> conversion to textualform of rust.
>
> besides you said each field has much more things than just name and visibility,
> and yet you have to slot for this data. you demonstrate stupidity"

**[ruled] 07-26**, name projections are not a new ruling but a confirmation of
his standing design. Agent proposed: derived text becomes a typed algebra over
identifiers, evaluated only at textualform time — NameProjection with Exact,
Cased, Composed, Disambiguated; segments are identifiers; evaluation by
per-language textualform data; nomos constructs projections as pure typed data.
Psyche:

> "I thought that's what I had designed"

**[derived]** — this is a confirmation of the original design, outside the
numbered ruling series. The implementation had inverted it by evaluating
derivations early in nomos and storing the text. No derived spelling is evaluated
before TextualForm. Disambiguation is keyed on **type identity, never on derived
spelling** — that is the fix for the `Vector<Topic>` / `Optional<Topic>` /
`Topic` grouping bug. Sketch, with the concrete variant set as matter:

```
NameProjection.[ Exact.Identifier
                 Cased.{ CaseForm Identifier }
                 Composed.Vector.Segment
                 Disambiguated.{ NameProjection Ordinal } ]
Segment.[ Name.Identifier Projected.NameProjection ]
CaseForm.[ Snake Screaming Pascal ]
```

Composition prefixes are Identifiers in the logos standard nametree slice — no
string anywhere in the algebra. The evaluator lives on name-table's dormant
TextualProjection surface; per-language spelling data (English ordinal words,
case rules) is textualform data owned by rust-logos, never nomos. Logos
Expression gains `NameText(NameProjection)`; `StringLiteral(String)` remains legal
only for genuinely opaque text — current production uses: zero.

**[ruled] 07-17**, identity is the number and is never guessed:

> "if it got re-ID'ed then its not the same, and if it's the same and got
> re-ID'ed, the system is implemented wrong"

**[ruled] 07-19 16:34**, the identifier shape:

> "1. actually, I was complicating things; the ID is the variant with its inner
> u16 (16 bits should be lots for a language)
>
> Schema.Id16 Logos.Id16 etc"

**[ruled] 07-22**, durability:

> "yes — encoded identity is the only durable one; the skeleton hash moves freely
> when the spelling's structure changes."

**[ruled] 07-21**, EncodedForm has no file concept. His hedge is part of the
quote and is kept:

> "to be clear; encodedform has no concept of files; decoding to "filename" must
> be a "beautification" algorithm, maximizing low-repetition and
> small-but-not-too-small filesizes. so not guaranteed to output the same
> separation or even filename. we don't need filename concepts in encodedform,
> its purely a file-management and cognition isolation interface. if im not
> mistaken"

**[ruled] 07-20**, no aliases:

> "no aliases"

Recency makes this the standing law; transparent Protos type aliases do not
exist. Referent aliases — the unrelated Spirit-domain concept of alternate names
for real-world subjects — are not addressed by this ruling either way.

### 6. NEW — the unified namespace

Entries 4 and 5 of the 2026-07-27 firsthand log.

**[ruled] 2026-07-27**, presented with Codex's slice-1 decision 3, adding
SchemaStandard as a new namespace variant holding the seven builtins as typed
prior members:

> "I dont see any problem with all components sharing a unified namespace; it's
> just an integer to string correspondance, including the "standard" or "builtin"
> terms. am I wrong?"

He is not wrong. Consequences:

- All components share **one** integer-to-string correspondence, including the
  "standard" and "builtin" terms. This **supersedes** the 07-19 ruling "yea, one
  nametable for each component. nomos uses the schema nametable to populate the
  logos nametable (and uses its own to read/write from/to its own encodedform)".
  The per-component variant survives as *slice structure of one global
  namespace*, not as separate tables.
- SchemaStandard as a namespace variant is **not needed**. Builtins are ordinary
  prior entries in the one table.
- **[ruled] 07-22**, redefinition remains an error:

  > "it should be an error, whenever anything tries to define something already
  > defined, like builtins. does that solve the problem?"

  The error lands at universe seal.

**[ruled] 2026-07-27**, from the dictation in entry 5 — the space is never flat:

> "But obviously 16-bit integer is not going to fit all of language, all of the
> words and all the languages, all of the spoken human or all of human languages.
> So it has to be broken up. It can't be one flat table for all languages. That
> would be absurd. But anyway, this is all stuff that we can change later. I would
> start with an enum at the root, which we always prefer or almost enforce
> actually in daemon interfaces so that we can split the domain."

An enum at the root splits the domain. The root variant set is matter and is
undesigned — see the consequences section.

### 7. NEW — daemon architecture

Entries 2, 3, and 5 of the 2026-07-27 firsthand log.

**[ruled] 2026-07-27**, after being shown the implementation as it stands — one
central sema-storage daemon as sole durable write authority, with the
schema/nomos/logos engines as stateless socket clients, citing its
ARCHITECTURE.md claim of the settled 2026-07-17 ruling "seat it centrally in
sema":

> "sema is the database of each daemon. either you are mistaken, or the
> implementation is. each daemon is stateful"

**[ruled] 2026-07-27**, of the 2026-07-17 central-in-sema ruling:

> "which was later overruled"

**[ruled] 2026-07-27**:

> "We could have a shared component just for the nametable, while the rest of the
> data lives in each daemon"

**[ruled] 2026-07-27**, asked whether the shared nametable component is (a) its
own small daemon the three daemons consult for name-to-ID binding, or (b) a
shared library over one shared durable store:

> "sema is the storage engine for all our daemons, so this repo will confuse
> everyone with its misleading name. which means that  'seat it centrally in
> sema' means a separate daemon, and wasnt correctly voiced. I shouldnt have said
> "in sema", since all daemon state lives in *its* sema db. There can be no
> sema-storage daemon, as it would overload the term sema."

> "a,  its own small daemon"

Consequences:

- **[ruled]** Each daemon is stateful. Sema is the storage engine of each
  daemon — its embedded db. There can be no sema-storage daemon; the term would
  be overloaded.
- **[ruled]** The 2026-07-17 "seat it centrally in sema" was overruled, and was
  mis-voiced when he said it: it meant *a separate daemon*.
- **[ruled]** The nametable authority is its own small daemon.
- **[derived]** Working name: **sema-translator**. This is a leaning of his, not
  a fixed name, and it is matter — see entry 5's "Maybe SEMA translator to use
  the noun approach that I've been trying to migrate towards."
- **[derived]** The durable identity-authority laws — never re-mint a key, never
  rebind an identity to a structurally different shape — move into this daemon.
  That implementation already exists and is tested; what is new is its reseating.
- **[derived]** sema-storage's stateless-client architecture is dead law, and its
  ARCHITECTURE.md "settled" claim is dead law. The repo cannot keep its name.

### 8. NEW — the sema vision

Entry 5 of the 2026-07-27 firsthand log. **[ruled]**, psyche-initiated, no agent
turn preceded it. Verbatim in full:

> "There's an interesting twist here, ironically, with the agent having decided
> on its own to call the current name component SEMA or SEMA storage. It might
> actually be more appropriate than I first thought, since the idea of SEMA
> originally was for this perfectly typed, perfectly specified schema-based
> language. And by schema here, I'm not talking about our language, which might
> need a different name just because it's confusing. Maybe something that goes
> along with Nomos and Logos. But it could become a universal name storage
> component that would allow all demons to store anything that, not all strings,
> obviously, because some of the fields are actually long blocks of strings for
> holding long strings like records that agents need to write and read as
> strings, obviously. And obviously, I also intend to change that eventually, but
> that's a very, very long-term thing. But at least all of the other, or maybe
> anything that is a single word, maybe we have a type for that, which allows us
> to have a kind of dynamically assigned enum of sorts with variant names that
> are not strictly enums and variants in the runtime as Rust sees them, but that
> have limits on how they can be spelled and are stored as integers using this
> SEMA naming component, which would allow us to start specifying SEMA as I see
> it, which is bigger than just, it's not that it's bigger than a database, but
> it means more than just a database. It's a new way of thinking about data,
> which doesn't contain strings eventually. So this could be the first step. We
> would need a component that can translate these identifiers, which would be
> integers, and this name table concept that we've fleshed out in this engine.
> That component could then extend to do more. And so I'm leaning on a side of
> maybe not SEMA storage is not the right name. Maybe SEMA translator to use the
> noun approach that I've been trying to migrate towards. And we could put that
> also, some of this in standards, also how we name components by nouns as an
> aside. But obviously 16-bit integer is not going to fit all of language, all of
> the words and all the languages, all of the spoken human or all of human
> languages. So it has to be broken up. It can't be one flat table for all
> languages. That would be absurd. But anyway, this is all stuff that we can
> change later. I would start with an enum at the root, which we always prefer or
> almost enforce actually in daemon interfaces so that we can split the domain.
> So maybe we should be using already done, already specified schemas. I think
> schema.org or something like that has an ontology already pretty specified. And
> maybe they have something on language. It's not a big deal, but let's just talk
> about this. See if you can explain it back to me quickly or on the face of it
> anyway."

The agent restated it; he confirmed with three refinements.

**[ruled] 2026-07-27**, on dynamic enums:

> "which could later be re-compiled into proper enums, while keeping their place
> in the translator table"

**[ruled] 2026-07-27**, on the no-strings end-state as intent:

> "almost, if it is extracted into a universal. the ultimate computer language
> cannot use strings, since they are an extremely inefficient way of representing
> a set (which language is)"

**[ruled] 2026-07-27**, on the names, the root variant set, and the ontology
borrowing being matter:

> "something to distill into standards; which I want to lean on more, and use
> more now"

Reading of the vision, in short: sema means more than a database — a way of
thinking about data with no strings eventually. Single-word values become
dynamically assigned enums, constrained in how they may be spelled, stored as
integers via the translator, and later re-compilable into proper Rust enums while
keeping their places in the translator table. Long prose blocks stay strings for
now; changing that is very long-term. The universal — the ultimate computer
language cannot use strings — is **intent**, in his own words.

### 9. NEW — identity representation

Entry 8 of the 2026-07-27 firsthand log.

**[ruled] 2026-07-27**, presented with Codex's slice-1 decision 5 (a distinct
content-hash domain for whole-logos EncodedLogos), and the current scheme's kind
tag inside the hash computation:

> "I think it's better if it's Variant.ContentAddressedHash"

**[ruled] 2026-07-27**, asked whether the variant is the sole carrier of kind
(inner hash over pure content bytes) or the kind also remains in the hashed
bytes:

> "Variant-only"

Consequences:

- The kind lives **solely** in the outer variant, protos-style, like `Schema.Id16`.
- The hash pre-image is **pure content**.
- content-identity's domain-tag-in-preimage scheme is superseded. **Existing
  digests move.** This joins the **one bump train** with the R3 and R4 kernel work
  and lands with fresh locks.
- Short displays remain kind-distinct; the kind is now carried by the variant
  rather than by a separate stored dimension.
- Whole-logos becomes its own variant kind. Decision 5's "preserving existing
  individual-item identities" holds at the identity level, while their digest
  bytes move with the scheme change.

### 10. Capsule

**[ruled] 07-26**, the composed-nametree pin, entry 1 of the 07-26 firsthand log.
The agent's exact question is load-bearing, because that entry exists to replace
a fabrication: "The addendum from my previous session says you ruled on 07-26
that a capsule pins the complete composition of its nametree. The committed
design log says the opposite: that "Yes." was composed by an agent from your
silence after you were asked twice and moved past it, and it lists the question
as still open. The published capsule contract requires the complete composed pin
today. Did you actually rule "the complete composition"?" Psyche:

> "yes"

**[ruled] 2026-07-27**, entry 1 of today's log — the container. Presented with
Codex's slice-1 decision 1 against his earlier "im not actually sure": an enum
with a variant per kind versus a generic struct with kind as a type parameter,
kind-distinct types by construction. Psyche:

> "Generic struct"

**[ruled] 07-22**, the name:

> "Capsule"

**[ruled] 07-23**, the full vision, dictated in one breath, no agent turn before
it:

> "So if we have a capsule for every namespace, which essentially mirrors the
> concept of a file in a regular programming paradigm, then because the potential
> name conflicts are dealt with at each layer, and because local objects are
> non-conflicting outside that capsule, we get no naming conflicts. So what
> happens when the code actually gets emitted into a compilable form like Rust is
> that all of the object names are fully qualified. Like, they get their full name
> all the time, so you never ever ever get a naming problem in the compiler,
> because everything is fully named with its namespace. Because we treat Rust like
> an assembly language, we can use it like one. So we can create capsules
> everywhere. We can create a top-level capsule, which is essentially your... You
> could have even different kinds of capsules. We should. I mean, each... Yeah.
> You can have a top-level capsule that's basically your manifest. Yeah, like the
> equivalent in file of your manifest. And then this resolves all of the top-level
> namespaces, basically. And if we want different kinds of sub-objects, we can
> write it at that level. Maybe there are different types of programs. I don't
> know. But I don't think so. I think every capsule after that is either another
> namespace capsule, basically, which we're basically creating abstraction.
> Basically, it's a way of classifying, I guess, your program, and it could also
> mirror how things are compiled. So maybe the concept of the file can somewhat
> live on in creating domain classification, basically. It's also actionable data,
> in a sense. But no, actually, every one of those capsules can be homogenous
> because they can all have sub-namespaces. So your top-level capsule might be
> where you find the... It might be the only one that's different because it's
> where you find the... If this is an executable or a library, I guess. Actually,
> every one of them can decide to be an executable or a library, which is
> interesting. Or a module, which then just gets used. I don't know. I would need
> to know, or someone would have to match that against the compilation model of
> Rust and how it treats objects and sub-objects, like how fine-grained does it
> get. We could sort of mirror that in how we organize the capsules and then
> create fields to declare, is this an executable or a library? And then declare
> sub-namespaces. Are they public or private? Which would just limit access, I
> guess. But this is all more Rust mechanic-related. Logos doesn't have to follow
> Rust exactly. It's a more correct way of seeing programming, but it does need to
> kind of accommodate Rust so that we get the most out of it. So we have to
> balance those two variables."

**[derived]** — capsule kinds Schema, Logos, Nomos. The enumeration is an agent
formalization; he named no closed set.

**[ruled] 07-25**, rust gets no capsule — his own correction:

> "re: rust capsule; youre right, my bad; rust-logos doesnt get a capsule. which
> means we need an object that deals exclusively with the textualform
> transformation, but is associated with a capsule, like rust"

Asked whether the association is fixed or open:

> "fixed of course.
>
> it would allow for multiple syntaxes to be supported (like the older schema
> syntax which could be made to work, as well as the new one, but both would only
> support schema capsule)
>
> OR, rust has also a capsule, which uses the same logos encodedform, so the rust
> is a different syntax for logos?"

He closed his own turn by reopening the opposite question. That reopening has
never been answered — see open questions.

**[ruled] 07-25**, capsule and short-identifier are protos concepts, not repos:

> "no, those are protos concepts, so they become protos traits, with
> implementations in each schema, logos, nomos, and rust-logos"

**[ruled] 07-23**, the capsule-to-crate correspondence is optional:

> "I didnt say capsules become crates. I said we can have a useful correspondance,
> which we can sometimes use. The impl could simply be always emmited with the
> type in the rust generation. It should be quite easy, since we can lookup all
> impls with a certain encodedID very easily. And we don't need to make the rust
> generation match the capsule separation in all cases; we can have other
> algorithms driven by the size of the generated code (it would be good to keep
> the generated artifacts as accessible as possible; very big code files are not
> easy to deal with)"

**[ruled] 07-23**, on cycles and full qualification:

> "but if we specify the compilation target (which capsule we want to emit as a
> compiled artifact), then would that problem be avoided?"

> "we still dont get name-conflicts, since a method call is on a FQO
> (full-qualified-object)"

**[ruled] 07-26**, short identifiers are display projections, entry 6 of the
firsthand log. Agent: "every capsule carries a short identifier — the little
base36 code ("0000" … "zzzzzzz")." Psyche:

> "no, it's a full content-addressed hash. the short identifiers is for common
> display operations, which will use a method on the hash which solves for the 4
> or more chars shortened version that doesnt conflict in the db"

**[ruled] 07-26**, kind safety, entry 7. Agent: "A schema capsule's short code and
a nomos capsule's short code were the same Rust type." Psyche:

> "they should be a different type for sure"

**[derived]** — the model, from `reports/ShortIdentifierRuling-2026-07-26.md`:
capsule identity is the full content-addressed hash plus the ruled composed
nametree pin, and nothing else. The short identifier is a **display operation,
never state**: a method on the content hash taking a resolver or view of known
hashes and solving for the shortest non-conflicting rendering, minimum 4
characters, growing as needed. The caller's resolver defines the conflict scope.
Git short hashes are the model. The stored ShortCode value model dies entirely —
the numeric type, the mint, the rkyv archive adapters, the archive compatibility
locks, and the kind-typed stored variants. Protos' `ShortIdentifier` supertrait
on Capsule dies with it: a conflict-free short form cannot be derived from the
capsule alone. Retire; do not adapt; zero consumers exist.

**[ruled] 07-25**, the home of the common library:

> "yes, content-identity is that library — add ShortCode to it"

Note the compiled log's own fidelity warning: a later agent-composed topology
document widened this into "ShortCode, ShortIdentifierMint,
CapsuleNameTreeDomain" — two names his sentence never mentioned.

**[derived — no verbatim source located]** Cargo and compilation metadata are
carried separately from capsule identity. A sweep found no psyche words on this;
if it becomes load-bearing, ask.

### 11. NEW — Ethos

Entry 7 of the 2026-07-27 firsthand log. Rename candidates were offered over
several rounds after his own request, "any idea for a schema rename?".

**[ruled] 2026-07-27**, rejecting rounds:

> "nothing pull me. nota is fine. we arent tied to greek. eidos isnt very
> evocative for english speakers"

> "no, not english"

> "no, nothing pulls me"

**[ruled] 2026-07-27**, on Ethos:

> "yes, ethos"

**[ruled] 2026-07-27**, on the repo:

> "can we rename the repo and point the old repo name to the new one? If so I
> want that done"

**[ruled] 2026-07-27**, on the living family (schema-engine, core-schema,
signal-schema, tree-sitter-schema):

> "yes, we'll have all those renamed as well."

**Executed 2026-07-27, verified on disk:** core-schema → core-ethos,
schema-engine → ethos-engine, signal-schema → signal-ethos, tree-sitter-schema →
tree-sitter-ethos. GitHub redirects are live; local ghq mirrors moved; the old
directory names are gone from `/git/github.com/LiGoldragon/`.

Legacy `schema`, `schema-language`, and `schema-rust` die under their old names.
Crate names, type names (the CoreSchema-family identifiers), and pins ride the
correction train. **[ruled]** NOTA keeps its name — "nota is fine".

### 12. Pipeline

**[ruled] 07-22 20:10**, schema's surface:

> "no, not at all; schema is the sugar, sweet syntax. creating a field for complex
> objects is *not* sweet"

Recorded contradiction, unreconciled in the sources: earlier the same day, 12:31,
he ruled "to me, this screams of "make them the same thing" - exceptions are
symptoms of bad design". Recency gives 20:10 the floor — schema keeps a dedicated
declaration surface distinct from the general item envelope — but neither side
has been walked back. Do not resolve this by inference.

**[ruled] 07-19**, the no-strings nomos invariant, as recorded in
`reports/logos/protos-engine-psyche-handover-2026-07-20.md`:

> "basically, in the nomos transformation (schema to logos), there shall be *no
> string manipulation/introduction/reading of any kind*"

with walkers at the boundary — "that is necessary." — and "make the invariant for
nomos transformation in its architecture documents."

**[confirmed]**, entry 8 of the 07-26 firsthand log: "transformers are data".

**[ruled] 07-23**, the manifest:

> "It's a config that associates files to top-level namespaces, and rules for
> rust-like directory-structure subnamespace-to-file resolution. does that make
> sense?
>
> Obviously nota format, with the type ideally defined in schema (we can generate
> rust with modern syntax schema? <- big question actually)"

**[ruled] 07-20**, the generation context:

> "it would involve all 3 engines, since some logos will be "standard logos"
> (ostensibly the only pre-written logos) which can change the output, and nomos
> can obviously change the output as well"

**[derived]** There is no logos source. Logos is produced by nomos from schema;
it is not authored as text. No psyche sentence states this as a prohibition;
it follows from the pipeline he described.

### 13. The ratified item schema

**[ruled] 07-22**, the full block as ratified. Reproduced exactly:

```
Items.Vector.Item

Item.[ Newtype.NewtypePayload Struct.StructPayload Enumeration.EnumerationPayload
       Alias.AliasPayload Const.ConstPayload Function.FunctionPayload
       Module.ModulePayload Impl.ImplPayload Use.UsePayload ]

NewtypePayload.{ ItemName Visibility Attributes WrappedField }
StructPayload.{ ItemName Visibility Attributes Generics Fields }
EnumerationPayload.{ ItemName Visibility Attributes Generics Variants }
AliasPayload.{ ItemName Visibility Attributes Generics TypeReference }
ConstPayload.{ ItemName Visibility Attributes TypeReference Expression }
FunctionPayload.{ ItemName Attributes Visibility Generics Receiver Parameters ReturnType Block }
ModulePayload.{ ItemName Visibility Attributes Items }
ImplPayload.{ SelfType Attributes Generics ImplementedTrait ImplItems }
UsePayload.{ UseBase Visibility Attributes UseGroup }

ItemName.{ String }                       ;; a bare name atom
SelfType.{ TypeReference }                ;; the full range — this is the "complex" slot
UseBase.{ PathNode }

WrappedField.{ Visibility TypeReference }
Fields.Vector.Field
Field.{ Visibility Attributes TypeReference }          ;; no name — derived at emission
Variants.Vector.Variant
Variant.{ VariantName Attributes VariantPayload }
Generics.Vector.GenericParameter
Attributes.Vector.Attribute

TypeReference.[ Path.PathNode Application.TypeApplication Reference.ReferenceType
                Slice.SliceType Tuple.TupleType Lifetime.LifetimeName ]
Visibility.[ Public Crate Restricted.PathNode Private ]
ImplementedTrait.Optional.PathNode
```

The agent's framing that he answered: "So "the identifier object is a variant,
symbol to complex types" is realized *positionally*: every kind's first field is
its identifying subject, and how complex that subject may be is exactly what the
field's type declares."

**[ruled] 07-22**, his ratification, in full:

> "otherwise I like the syntax."

**What "otherwise" excepted was never recovered.** That clause is an open
question. Do not treat the block as unconditionally ratified without flagging it.

Supporting rulings on this shape:

**[ruled] 07-22**, every item kind takes the brace:

> "youre confusing two things here; logos has a few types defined, and they will
> all need multiple typed structs to express everything that rust expresses. So
> there will be an
>
> Struct.X.{} just like there will be an Enum.X.{} (think of all the
> config/options/derives/whatever-theyre-called-features-in-rust that need to be
> specified!)"

**[ruled] 07-22 18:15**, the envelope, superseding the 09:43 dotted form:

> "no, that looks really messy to deal with.
>
> I say we abandon dotted names, and instead make the first field the object
> identifier object, which could be a variant (symbol to complex types - make a
> list of all those different types of objects based on the rust syntax support)
>
> and this applies to all objects. so we end up with a vector of variants [
> Newtype.{} Struct.{} ... ]"

The 09:43 form, which the 18:15 turn abandoned as an envelope but which still
carries his own visibility example, is:

> "Newtype.CommitSequence.{ Public [<attrs>] { Private Integer } }"

Note `Impl` is identified **positionally by SelfType**, not by a name field, and
`Field` carries no name — the `;; no name — derived at emission` comment is his
ratified text.

**[ruled] 07-20**, the escape set, closed at two primitives. Presented with `$x`
realizes and `$@xs` splices, splice defined as typed vector-segment concatenation
legal only at vector element positions:

> "agreed"

### 14. Topology

**[ruled] 07-24**:

> "we dont use the monorepo style; destroy the duplication by keeping the
> micro-repo approach"

**[ruled] 07-24**, asked whether the micro-repo ruling is confirmed knowing it
reverses the July-19 consolidation:

> "Yes, the consolidation was never approved"

**[ruled] 07-25**:

> "I want to remove the monorepo approach, to ensure the micro-repo approach is
> the only one, since it is what I want, and the monorepo was an agent
> hallucination/bad-decision."

The consolidation began with his own 07-19 line "consolidate into protos." — the
reversal is his own correction of his own direction, not an agent's misreading
being corrected.

**[ruled] 07-24**, on protos.git as the home of the common daemon traits:

> "yes"

**[ruled] 07-25**, on protos-engine:

> "ahh, you mean a repo that assembles it all together?
>
> could be a protos-engine repo; mostly just nix code with launch scripts"

> "yes, protos-engine also contains tests"

> "protos-engine.git is a new ASSEMBLY repo, not an engine source repo"

**[derived]** — the dependency-sink law: protos-engine pins the micro-repos,
publishes no library crate, and nothing links against it; a grep of every
Cargo.toml in the family for protos-engine as a dependency must always return
zero; its deps on the micro-repos are published git revs, never path deps. The
compiled log flags this formalization as agent-composed, built from the
repository-topology quotes above.

**[derived]** content-identity is the common library. Repositories live at the
ghq root `/git/<host>/<owner>/<repo>`; a missing repository is cloned with `ghq
get <url>` and never cloned elsewhere.

### 15. Acceptance

**[ruled] 07-19**:

> "I dont care about byte-exactness. get rid of that. working programs is what we
> want."

**[ruled] 07-20**:

> "near roadmap is getting everything running on the new protos engine and
> testing the hell ouf of it"

**[confirmed]**, entry 8 of the 07-26 firsthand log — the spirit-port test, as it
circulated and as he confirmed on 2026-07-27 with "yes, those are my words":
"porting spirit to the new engine, and having a working system with a copy of
production database", with normal operations responding normally against an
isolated migrated copy of production data, zero build or runtime dependency on
schema-rust, and no compatibility adapters. The log's own provenance note applies:
the original turn is unlocated, the fragment is quoted as it circulated, and it
stands as a psyche-confirmed ruling rather than a firsthand transcript.

**[derived]** — vertical slices, each traversing the whole pipeline and
compiling and running the generated Rust. The witness oracle pattern is correct
and is kept: scratch crate, real cargo compile, behavior round-trips, no
byte-golden.

## The five decisions — answered 2026-07-27

1. **Capsule container: generic struct.** **[ruled]** "Generic struct". Kind is a
   type parameter; kind-distinct types by construction. This closes his 07-23
   "I think capsule should be a trait, and it could be contained by an enum or a
   struct - im not actually sure."

2. **Durable declaration IDs: yes.** Decode consults the durable authority, never
   parse order. **The authority's seat is the new small nametable daemon, not
   sema-storage** — entry 3 forecloses a sema-storage daemon entirely. The
   existing tested identity-authority implementation is the substance; its
   reseating into the new daemon is new work and needs a design proposal before
   code.

3. **SchemaStandard namespace variant: no as posed.** Superseded by the unified
   namespace **[ruled]**: "I dont see any problem with all components sharing a
   unified namespace; it's just an integer to string correspondance, including
   the "standard" or "builtin" terms. am I wrong?" Builtins are prior entries in
   the one table. The redefinition error lands at universe seal.

4. **Wrapped-field visibility: yes, Private** for slice 1. **[ruled]** "yes,
   Private", against his own 07-22 example
   `Newtype.CommitSequence.{ Public [<attrs>] { Private Integer } }`.

5. **Whole-logos identity: yes in substance** — whole-logos is its own identity
   kind — but **reshaped**: **[ruled]** "I think it's better if it's
   Variant.ContentAddressedHash" and **[ruled]** "Variant-only". Digests move.
   Fold into the one bump train.

## Consequences requiring design proposals before code — do not infer

None of the following is designed. Each needs a proposal put to the psyche before
any code lands.

- **The nametable daemon.** Its name (sema-translator is a leaning of his, not a
  fixed name), its wire contract, its minting flow, and how the three engines
  consult it. Propose before implementing.
- **sema-storage dissolution.** The repo rename, the migration of document storage
  into per-daemon sema dbs, and the correction of its ARCHITECTURE.md dead law.
  Propose a plan.
- **The unified table's root enum variant set.** Possibly informed by an existing
  ontology — his own suggestion was "I think schema.org or something like that
  has an ontology already pretty specified." Propose.

**How to bring a question.** Every question put to the psyche must be explained in
practice: where a thing is stored, how it is shared, and what happens on the
failure paths. A yes/no question wrapped around an undesigned mechanism gets sent
back.

## Producer work after the rulings

Codex's producer list, carried with corrected names and the reseated authority.

- **raw-discovery** — data-driven cue-to-terminator item discovery: inclusive cue
  bounds, semicolon and balanced-brace termination, recursive inner blocks,
  opaque strings and comments, source bounds on every block. Seed the rebuild
  from the existing balanced scanner (`discover_delimited`, currently dead code
  called only from its own tests) rather than rewriting it — it is nearly the
  protos-family pass-1 variant already, minus dotted-prefix attachment.
- **structural-codec** — typed Rust item-boundary descriptor plus typed-position
  disjointness, through the same shared evaluator. Not a parallel engine.
- **rust-logos** — an in-place rename of textual-rust, with the fully typed
  newtype vocabulary and no legacy emitter anywhere on the slice path.
- **core-ethos** — builtin priors in the unified table; durable-authority input;
  universe seal; production Schema capsule.
- **core-logos** — EncodedLogos with its own identity variant; production Logos
  capsule; public Textual inspection.
- **core-nomos** — a separate, direct, string-free one-newtype converter. It must
  never be routed through the string-bearing NameTableBoundary, macro evaluator,
  prelude, renderer, projection, or ordinal code.
- **protos-engine** — the acceptance gate executing the full chain and compiling
  and running a scratch Rust crate.
- **The bump train** — variant-only identity retype in content-identity plus the
  R3 and R4 relock, as **one landing** with one set of fresh absolute-digest
  locks.

Blocking problems still standing from the second correction, unless resolved
since:

1. **Published state is broken.** content-identity main deleted ShortCode
   (correct), but protos main still imports and re-exports it and its Capsule
   supertrait still returns it — the two published repos cannot compile together.
   Retire protos' ShortIdentifier supertrait, re-exports, and the Capsule getter,
   and land that with the structural-codec push.
2. **Split the unpushed commit.** The 29-file commit mixes R3, R4, identity fixes,
   pins, re-locks, a subsystem replacement, and a 54% test deletion. Kernel
   retype, type-id retype, identity fixes, pins, and re-locks each stand alone.
3. **The textual decode replacement is refused as shipped** and must be rebuilt as
   the block-discovery pass. Its recognizer finds a closing boundary by parsing
   every interior object with full grammar rather than by termination rules; it
   fixes one document-wide trigger set at construction; boundaries are hardcoded
   to `(`, `[`, `{` so angle brackets are unrepresentable, which alone
   disqualifies it for rust-logos; and blocks carry no source bounds, directly
   contrary to ruling D. Conformance laws 1 through 4 and the boundary-first
   suite must be re-established against the two-pass arrangement before it lands.

## Carried mapped facts — verify before relying

These come from Codex's map. They are reported, not re-established here.

- **Re-check:** the claim that "the current concrete Capsule contract needs no
  generic API change" must be re-checked against the generic-struct ruling and
  the variant-only identity ruling. Both move the contract's shape.
- `EncodedReference::Integer` needs a typed identifier drawn from the builtin
  priors — never manufactured from the text "Integer".
- The one-newtype conversion transfers the declaration identifier, maps item
  visibility, and emits empty attributes.
- Generated Rust may be attribute-free: `pub struct CommitSequence(Integer);`.
- The behavior crate may define `type Integer = u64` and round-trip through `.0`
  without touching any un-ruled naming question.
- The intended production schema source is the six-slot document decoding one
  newtype wrapping builtin Integer.

## Completed work — Codex-reported, spot-verify on resume

Carried as reported, not re-asserted by this file.

- Typed-record kernel published.
- Recursive source-bounded block discovery published.
- Two-pass textual decoding through one shared bounded evaluator.
- Encoding descriptor-driven.
- Schema textual tables on the two-pass API.
- Reflection unified to one lookup-only path.
- core-logos fixture migrated.
- core-nomos repinned and namespace-tagged.
- protos repinned.

**Conformance Law 5 remains homeless and open.** Its downstream test lost its home
when the derive repo died, and its only discharge sat inside the unpushed commit.
Do not claim it restored. Carry it as an open item in every slice report until it
is rehomed or retired by ruling.

**Deliberately deferred, not forgotten:** textual-rust runtime, golden, and Nix
tests (syn/quote/prettyplease); core-nomos runtime and Nix tests (string-bearing
legacy); spirit, meta, judge, and signal-frame; slice 2 and beyond.

## Foundation pins

Repository names below are the current ones; the hashes are unchanged by the
renames. All ten were verified to resolve to real commits in the local ghq
mirrors on 2026-07-27.

- content-identity — `24b43bae5d9748b0e7f679c6ec9f85a643c4d36a`
- name-table — `196610e2907687dcb8dbd0d2dfaafe4aefd9fa27`
- raw-discovery — `2ac78f621980fa02daa3b31e90cc5c73570eed6e`
- structural-codec — `23497c43f81b619158e5cfbd83a012eb63c4186f`
- protos — `a18810c819a4e7c09ea70ea1eef83d6a18a732d9`
- core-ethos (was core-schema) — `6067b526ab0e9c0e90389543de03d2cd7bd6202a`
- core-logos — `5b66127de26b265e17a8060d5e06b9d7d31ce93e`
- core-nomos — `e0a375a8a699b938033349f1c40f6e80f6e688e6`
- textual-rust — `1bd10fcb47bfa510d7911a748a08715fc372a109`
- protos-engine (design head) — `27c72fcd0f045d6ddca8f75652b0ddb7d6092cd3`

Cleanup still owed, verified present on 2026-07-27: three stale worktrees under
`~/wt/github.com/LiGoldragon/` under the old names (core-schema, schema-engine,
signal-schema), and 16 old-name entries in `/home/li/primary/orchestrate/worktrees.nota`.
Old repository names keep working through the GitHub redirects, so nothing is
broken while the cleanup waits.

## Open questions — do not infer

**Closed today:** capsule container; SchemaStandard; wrapped-field visibility;
whole-logos identity kind; the identity authority's seat.

**Open:**

1. **Function-parameter and let-binding names.** The field-name ban is settled for
   struct fields and declaration bodies. The nearest psyche word is now
   **[confirmed]** via entry 8: let statements are "semi-anonymous (very private)
   types". That is still not a ruling on function parameters.
2. **Micro-capsule: full pin or light pair.** From his 07-23 remark that "each
   complex object might need a field for its own private micro-capsule" — note
   "might need". Whether it carries the full Capsule pin machinery or a lighter
   pairing is unaddressed.
3. **Manifest self-generation.** "we can generate rust with modern syntax schema?
   <- big question actually" — his own words, his own flag that it is a big
   question. Unanswered.
4. **reify/reflect: eventually derived?** No psyche words on this exist in any
   read source.
5. **StringLiteral remedy** (register Q3): `NameLiteral(Identifier)` versus
   accepting rename-instability.
6. **Plane vocabulary survival** (register Q4), deliberately deferred until the
   slices reach daemon emission.
7. **His own reopened question:** "OR, rust has also a capsule, which uses the
   same logos encodedform, so the rust is a different syntax for logos?" It is
   foreclosed today only by agent-composed amendment text that the compiled log
   itself disowns. It is open.
8. **The global longest-match lexical law.** His assent was never captured. Do not
   assert the law and do not assert a ban on it.
9. **What "otherwise" excepted** in "otherwise I like the syntax." — the excepted
   clause is unrecovered. The item schema's ratification is conditional on
   something we cannot name.
10. **ID retirement policy.** Stale entries are inert under the never-re-mint law,
    but retirement itself is unruled.
11. **The translator daemon's final name.** sema-translator is a leaning.
12. **The root enum's variant set,** and whether to borrow from schema.org or a
    similar existing ontology.

**Slice 2 still opens by presenting the deterministic field-naming rule for
ratification.** The projection algebra is that slice's vocabulary, not its answer.

## Conduct and authority

- Psyche words are design and are never edited. The log is append-only; supersede
  by appending. Later statements govern earlier ones.
- Open questions are answered by the psyche, never by code.
- Never write a comment or a test name claiming a ruling is satisfied. Describe
  the mechanics.
- Every behavior change is named in its own commit body. Plumbing commits carry
  zero behavior. Commit messages have bodies when they touch more than pins.
- Mechanically-checked repository laws are widened only in their own commit,
  citing the authorizing reason — never in the same breath as the violation they
  legalize.
- Stop-the-line on undecidable disjointness: surface it. Never order-resolve,
  never special-case.
- Deleted coverage is named, never silent. Coverage is the proof the new engine
  behaves.
- The log must never state law ahead of the code. Where it does — for instance
  the "first production Capsule implementors" line — treat it as an obligation to
  discharge, not as a status assertion.

Codex-specific:

- The root session coordinates only. All repository work goes through subagents.
- Long interruptible waits, never repeated short waits.
- AGENTS.md discipline: `jj` only, always with inline messages and never an
  editor; exact Orchestrate claims before editing shared files; worktrees through
  the documented `RequestWorktree` / `ConcludeWorktree` flow; repositories at the
  ghq root.

## Preserved external work — do not touch

- The frozen Meta and Judge candidate worktrees.
- The Spirit worktree and the published feature branches.
- structural-codec-derive.
- signal-frame wire primitives.

**Spirit's new-schema-port was never actually pushed**, despite earlier reporting
to the contrary. Its corrected acceptance-harness commit is dangling and
unbookmarked. Preserve it before any cleanup touches that repository.

## Required references

Firsthand design logs, in authority order:

- `/git/github.com/LiGoldragon/protos-engine/design/ProtosEngine/SliceOneRulings-2026-07-27.md`
  — controls today's wording.
- `/git/github.com/LiGoldragon/protos-engine/design/ProtosEngine/ShapeAndSliceRulings-2026-07-26.md`
  — controls yesterday's wording, and carries entry 8's confirmations.

Compiled log:

- `/git/github.com/LiGoldragon/protos-engine/design/ProtosEngine/ProtosEngineDesign-2026-07-26.md`

Reports:

- `/home/li/primary/reports/CodexCorrection-2026-07-26-second.md`
- `/home/li/primary/reports/CodexCourseCorrection-2026-07-26.md`
- `/home/li/primary/reports/ShortIdentifierRuling-2026-07-26.md`
- `/home/li/primary/reports/BadDataShapesRegister-2026-07-26.md`
- `/home/li/primary/reports/CodexShapeRemediation-2026-07-26.md`
- `/home/li/primary/reports/CodexResumePrompt-TypedRules-2026-07-26.md`
