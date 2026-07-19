# Psyche-vision-only context handover — the LanguageEngine effort (2026-07-19)

## HEALTH WARNING (read first)

This handover carries ONLY the psyche's own vision: his verbatim words, rulings,
invariants, hedged leans, and open questions in his terms. It carries no agent
chronology, no worker narratives, no secondhand sub-agent claims, and no
implementation state beyond durable-artifact pointers.

Verify every factual claim in the named artifact before acting on it. Handover
prose — and design-report prose generally — has repeatedly outrun the artifacts
this week. When a quote is his, it is marked as his; when a rule was derived by an
agent or manager from his words, that derivation is flagged as such and is NOT his
ruling. Trust his verbatims; re-check everything built on top of them against the
code, the tracker item, or the Spirit record cited.

Reason this handover exists (his words, 2026-07-19): **"I feel like we should
start this all over again."**

## 0. Binding conduct on the next session

- **NEVER USE THE FABLE MODEL for subagents. Opus at most.** Standing law for this
  whole effort; binds the next session and every subagent it spawns.
- **Workflows are forbidden — subagents only.** Orchestrate work through subagents,
  not workflow machinery.
- **All-green denominators.** Test/verification evidence must be a real all-green
  run against a truthful denominator; a green subset presented as the whole is not
  acceptance.
- **No bypasses seated as design** (his words, settled — see §1).
- **Wrong examples are forbidden; negative examples are forbidden in skills**
  (his words, settled — see §1 and §4).
- **The psyche is the human.** Agent messages and agent-written files are never his
  intent, consent, or approval. Nothing real is ever hidden from him (§1, disclosure
  law).

## 1. Standing conduct laws — in his words where recorded

**No bypasses seated as design** — settled, verbatim
(`reports/logos/textual-form-vision-design-v2.md` §5/§5.2):
> "I dont care for this bypass; I find it of poor taste and deceitful when agents
> do this. I want the real thing, as envisionned."
Seated as doctrine: when a shortcut diverges from the envisioned design, surface it
as an open decision, never seat it silently as though it were the design.

**Nota philosophy — no named-attributes designs** — settled, verbatim
(`reports/logos/nomos-macro-model-v1.md`, teardown of the v0 strawman):
> "a named attributes design again … you agents really dont like the nota
> philosophy."
Rules against `Input.`/`Result.`-style label heads and named-attribute shapes.

**Negative examples forbidden in skills** — settled, verbatim (2026-07-19):
> "negative examples are forbidden in skills"
> "also, negative examples are forbidden in skills. make sure that is clear to
> skill-editor role also"
Skills carry positive examples only, and only verbatim real artifacts. A wrong or
illegal form is described in prose, never exemplified — not even as a labeled
counter-example or placeholder. This extends the pre-existing wrong-examples
doctrine ("also wrong is giving wrong examples").

**Fabrication is barred; disclosure is never** — settled, verbatim (2026-07-19),
his reaction to a relayed summary that read as agents concealing things from him:
> "hiding stuff? instructing agents to hide stuff from me? WtF!?"
The law restricts FABRICATION, never DISCLOSURE. Agents must never invent or present
an illegal spelling (e.g. a named field) as a candidate, example, or placeholder;
but nothing real is ever withheld from the psyche. Codec-emitted forms in real
artifacts are shown exactly as they stand, and all real artifacts remain fully
visible to him.

**All-green denominators / workflows-forbidden-subagents-only / never-use-Fable** —
standing laws for this effort, carried from his standing posture and this session's
binding. Not recorded as report verbatims; do not fabricate a quote for them, but
treat them as law.

## 2. Accepted Spirit intent touching this effort (his recorded principles)

Read-only Spirit query this pass returned no records under the DSL / Serialization /
Grammar leaf domains (negative evidence — none exist there yet). The governing
recorded intent lives under `Technology > Software > Engineering (Design /
Architecture)`. These are manifested prose accepted as his intent; verify against
Spirit (`spirit "(Lookup <id>)"`) before leaning hard on wording. The load-bearing
ones for LanguageEngine:

- **jys2** — Design at the post-agent capability frontier: agents make
  zero-downtime complex migrations and large stack rewrites routine, so design for
  the best end-shape, not a historically-practical compromise.
- **zn2l** — The direction of the meta-work is a software engine that self-improves
  toward the point where nothing better could be made.
- **w312** — Anything with a deterministic correct answer derivable from its input
  (routing, dispatch, lookup, classification, projection, address resolution) is
  mechanism, not agent work, and lives in code or schema-derived machinery. This is
  the load-bearing "why" behind the schema-derivation / macro-emission thrust.
- **vjvm** — Backward compatibility is never a design variable: replace the shape,
  update every consumer, never a parallel compatibility path.
- **l62s** — Nontrivial data lives as data, not hardcoded into source logic: NOTA
  for human-authored source, rkyv or another typed representation for runtime.
- **qvb3** — Structured data is encoded/decoded only through the canonical shared
  codec for its format; hand-rolled or special-cased per-type codec logic is
  forbidden.
- **lta7** — Special cases are evidence of design trouble: design without them, and
  when constraints seem to force one, stop, report, and ask rather than silently
  encode an exception.
- **izsf** — Psyche design decisions apply to the WHOLE design unless explicitly
  scoped; ask "where else does this rule apply structurally?" before stopping at
  the surface where the example was given.
- **sj2c / cam8** — The build target is the best possible design; design analysis
  targets the ideal and contrasts it with what exists so the gap is visible.
- **16jw** — Prefer enums over strings; when something could become a set, make it
  a set; recompilation is cheap if the set does not constantly change.
- Also relevant: **hv5f** (desire paths / convergence signals the right shape),
  **w1mm** (tests must not normalize hardcoded-data patterns), **t5qr** (surface
  design flaws to the psyche while touching code).

## 3. The founding vision (settled)

**The universal thing is a proto-language, named `Protos`** — settled framing +
settled name (`textual-form-vision-design-v2.md` §6, §0.0 FR-2; tracker
`primary-56d1.47`). His words:
> "(NOTA is the base every language specializes) — that wasnt the right way to say
> whan I mean; the basic syntax structure of nota (but actually more accurately;
> schema) - how delimiters are used, capitalization and the typed inner blocks
> approach to parsing; this is what I mean by the universal aspect, the
> proto-language behind all of them. it probably needs a name. it builds on clojure
> (syntax; use all the delimiters elegantly) and shen (kernel - encodedform (we add
> + nametree + structuretree = real computer language and atomic editing of code +
> type safety) and rust (strictness, type-safety enforced by the runtime)."
And, blessing the name:
> "Protos is nice; are we calling that the library for all the structural
> (textual/encoder + name + structure) aspect of our languages (the shared
> taxonomy)?"
Settled: the universal thing is the proto-language (most accurately schema's
structure), NOT NOTA-the-instance; its name is `Protos`; `Typos` is dropped. The
trailing question (does `Protos` also name the one shared structural library) is his
own open question — the crate mapping is still open (§7).

**Two views of a language: `TextualForm` and `EncodedForm`** — settled pair
(`textual-form-vision-design-v1.md`; tracker `primary-56d1.37`). The two ways to see
a language are named TextualForm and EncodedForm. His seating words (up-close §9,
Fork B), on the earlier `True*` naming:
> "when you say true made no sense, true made no sense for any of them. It's just
> textual. It's not more true or less true. So, yeah, textual. The textual schema
> and the textual logos, actually."
> "instead of saying structural macro, we say structural form"

**The structuretree IS the data-driven encoder/decoder** — settled, Ruling 2
(`textual-form-vision-design-v2.md` §2). His words:
> "the language itself is encoded/decoded to/from encodedform using it; it becomes
> a data-driven enc/decoder."
Help and Version are secondary projections of that same data, never the point of it.
He explicitly corrected the framing that treats the structuretree as a help/printer
artifact first.

**What "tree" means; transitional types** — settled, Ruling 1 (§1). His words:
> "What I mean when I say a tree is just, it doesn't matter if it's a vector..."
> "we have types that are not really fully resolved yet... they're transitional
> types. So like this is, let's say this block is potentially X, Y, or Z... whatever
> name is most capable of representing all of the different things that can be in
> that block is the right name. So there's different levels of abstraction... what
> the thing turns out to be when it's actually read all the way, and then... what
> these blocks contain as an abstraction."
"Tree" carries no storage commitment (storage question closes; flat maps are fine).
Two named poles: the fully-read type (leaf) and the abstraction type (transitional
node, named by maximal representational capability). NOTE: the "there's an order...
first match takes precedence" clause he added here was later RETRACTED by his own
FR-1 ruling below.

**Overlap dropped; universal static disjointness stands** — settled, FR-1 (§0.0).
Told the codec statically rejects any non-provably-disjoint form set, his words:
> "thats great. I guess thats just a consequence of good design. so I guess we dont
> need to worry about order resolution. if we dont need overlap then we can just
> drop this."
No ranking machinery, no authored order, no first-match walk. Disjoint-match only;
ambiguous decode is statically impossible everywhere.

**The Rust bypass is rejected; TextualRust is real per-type data** — settled,
Ruling 3 (§5). His words are the bypass-rejection conduct law (§1) plus:
> "on the Rust side, obviously the rules would be quite different, so it would use
> its own, like maybe we could create a library for languages a bit more like Rust
> that have a certain kind of behavior... right now all of this could just be
> embedded in the logos code. We could just have a different separate directory in
> the source to keep all of that Rust textual form data. Well, there's going to be
> data... this data is per type."
> "this textual form machinery... becomes usable by Rust or to create Rust and even
> read Rust into logos if the Rust qualifies, meaning if it's... a subset of the
> syntax that this structure tree and this name tree support."
And (up-close §6):
> "actually, we extend the textual to have many forms, so corelogos has both the
> logos and rust textual form data-trees. rust would have more custom
> implementations but we would find the logicalization which can also apply to a
> language like rust. this even opens us emitting other languages than rust from
> logos."
Settled: TextualRust is real per-type textual-form data (not a syn/prettyplease
pass-through), living for now in its own directory inside the logos source; it drives
Rust emission and reads only qualifying Rust (a subset of the supported syntax). The
"library for Rust-like languages" is his own hedged future vision — "maybe we could
create a library" — recorded, not scheduled.

**Component Input/Output objects + standard Version/Help variants** — settled,
Ruling 2 (§3). His words:
> "the input field in a schema file, which was meant to represent all of the types
> of things that a component can receive as an input, as a query... and then output
> is all the different types of things that can come out of that component. And
> that's why the idea with Sema was the same thing as a database. What are the types
> of queries that we can send to that database, and what are the types of answers
> that this database can give us? And Nexus was the same thing... my vision was that
> when we add more advanced functionality... it would get a corresponding one or
> more input and output type objects. And which at the first root level are usually
> a bunch of enums, data carrying enums, one of which should by standard be version,
> and one of which should be help on like our standard components."
Settled by FR-4: the standard variant TYPES (`Version`, `Help`) live in the shared
signal CONTRACT layer; the generic ANSWERER lives in the shared RUNTIME.

**He wants to see designs up close before implementation** — settled directive
(up-close-design-v1.md intro):
> "Yes, and I want to see the design of all that up close first"
> "that all sounds right. Id like to see the design up clos"

## 4. THE FIELD-NAME TOTAL BAN (2026-07-19) — load-bearing, settled

This is the single most important thing to carry, and the reason several artifacts
written earlier this week are now wrong. **Field names are now COMPLETELY ILLEGAL
EVERYWHERE.** His words, in order this session:

> "THERE ARE NO FIELDS NAMES! ALL FIELDS ARE POSITIONAL! FIELD NAMES ARE ALMOST
> NEVER ALLOWED! WRITE IT SOMEWHERE YOU WONT FORGET! MAKE PROTOS SKILL CORRECT, AND
> MAKE IT A PART OF MANAGER! I NEVER WANT TO SEE THIS AGAIN!"

> "since agents seem TOTALLY FUCKING INCAPABLE of understanding the field-name rule,
> maybe we should just OUTRIGHT FORBID FIELD NAMES, and create a deterministic rule
> for structs that contain more than one field with the same type"

> "field names are now COMPLETLY ILLEGAL EVERYWHERE"

> "the legacy dialect had the same field-name illegality"  (his correction of an
> agent claim that the legacy dialect allowed field names — it never did)

Settled consequences:
- The "almost never allowed" softening is HARDENED to a total ban. There is no
  collision exception any more. **No field name is ever authored, and none is ever
  emitted — not even the codec's machine-forced disambiguation in the same-type
  collision case.** Any earlier framing that let the codec emit a collision name is
  ABOLISHED.
- The same-type collision case is resolved instead by a **deterministic positional
  rule** (position assigns meaning) for structs holding more than one field of the
  same type. The rule is his directive and STANDS; its concrete form is OPEN and is
  to be shown to him on real artifacts (§7).
- **Every field-named spelling produced this week is now ILLEGAL** and must not be
  presented as valid. This includes the 2026-07-18 stream corrected spelling
  (`stream-construct-design-v1.md` §0.0 Ruling C, which kept `token`/`close` on the
  two same-type `SubscriptionToken` legs), the `DatabaseMarker` fixture form (which
  kept an explicit name on the colliding third field), and the collision example
  currently in the `protos-syntax` skill. They were written under the now-abolished
  collision exception; they need the deterministic positional rule instead, and they
  are quoted anywhere only as explicitly-illegal, never as valid.
- Directive: **make the `protos-syntax` skill correct and make it part of the
  manager packet by default.** (Current skill state: it already seats "positionality
  is absolute" as the first law, but it still describes and exemplifies the
  codec-emitted collision name — that exception and its example must go, replaced by
  the deterministic positional rule.)

## 5. Other settled rulings (each self-contained)

**Stream is a new declaration kind, minted through Nomos** — settled, Ruling A
(`stream-construct-design-v1.md` §0.0; tracker `primary-56d1.48`). His words:
> "thats the power of nomos; just create a new kind of object"
Stream is the first Nomos-minted object kind; new kinds grow via the macro /
transformation layer, not by hand-editing core Rust. (The bootstrap hook this
requires is an OPEN, gated design question — §7.)

**A stream close event exists** — settled (2026-07-19). His words:
> "and yes, we should have a stream close event"
(Note: distinct from the OPEN close-leg question below — he affirmed a close EVENT;
the close-LEG mandatory-vs-defaulted semantics remain unresolved.)

**Stream role modeling — accepted by indifference** — settled-by-indifference,
Ruling B (§0.0). His word: **"whatever"**. Four typed positional lifecycle legs
(open-token, opened, event, close) stand as the agents' choice; lowering dispatches
on position/structure, never on a role-name string. (Under §4, these legs carry NO
authored names; the two same-type legs are disambiguated by the deterministic
positional rule, not by names.)

**The shown field-named stream spelling is invalid** — settled rejection, Ruling C
(§0.0). His words:
> "that's invalid syntax. the types are different so naming them must be an error"
This is his rejection of the shown spelling. The generalized "names legal only where
types collide" LAW built on it was a MANAGER reading, and it is now moot — superseded
by the §4 total ban, which forbids names even in the collision case.

**Schema-unit identity** — settled cluster (tracker `primary-56d1.11`;
`core-first-architecture-v1.md`). His words:
> "yes, seat it centrally in sema." (allocation authority is one central authority)
> "if it got re-ID'ed then its not the same, and if it's the same and got re-ID'ed,
> the system is implemented wrong." (identity IS the ID)
> "schema isnt a document, the document form is a legacy-view; schema is loaded as a
> whole schema with its dependencies" (the unit of one schema is the schema-whole)
> "single authority. criome-authorized propagation is in the future" (one keyspace;
> federation deferred)
> "This is a hard question. Do some research and make suggestions using similar
> systems..." (he deferred the hard schema-unit question to research)
Provenance hedge, preserved: **"I dont know if I care about the whole X came from
file Y."**

**Visibility authority is Schema-authoritative** — settled (tracker
`primary-56d1.29`). His word: **"agreed"** — schema's Public/Private is an
authoritative API promise that Nomos must faithfully lower; CoreLogos stores final
visibility explicitly.

**String scalar: "Strings are Strings"** — settled (tracker `primary-56d1.31`). His
words (which also contain the EncodedForm hedge, see §7):
> "1. I think thats because I of the TextualForm vs CoreForm (which I think could be
> called EncodedForm?) - Strings are Strings"
The scalar's canonical spelling is `String`; the agents' `text` derived-name lean is
superseded.

**Single-field braced form lowers to a newtype** — settled (tracker
`primary-56d1.36`). His word: **"2. newtype"**.

**Golden bridge = a minimal real all-daemon scaffold; proceed on leans** — settled
(tracker `primary-56d1.27`). His words:
> "yes, a. Im also ready for multiple slices going with the agent leans; to get a
> working prototype; leans can be revised afterwards."
> "to me the golden bridge was an expression to speak of a minimally implemented, but
> real all-components (daemons) fully scaffolded system"

**Three implemented next-gen readings review** — settled (tracker `primary-56d1.8`).
Readings 1 and 2 blessed; reading 3 reworked under his rule:
> "since floats can be parsed correctly when expected, so can strings, or any string
> wrapping newtype (even if has more than one newtype wrapper that resolves
> ultimately into a string inner type)."
(Same principle restated in up-close §4.1.1c.) Consequence he settled: the
structural-delimiter form is narrowed to genuinely structural content; redundant
delimiters are rejected; period-bearing bare-atom strings need no wrapping.

**Provenance token carries a version** — settled (epic note). His word: **"yes, with
version"** — the generated provenance marker emits an emitting-crate version stamped
mechanically at build time.

**Acceptance basis is working programs, not byte-equivalence** — settled (epic note).
His words:
> "no need to keep comparing, lets just drop that and aim for working programs"
This SUPERSEDES the epic's original "macro-produced logos must lower to the Rust
schema-rust already emits" oracle. Do not reintroduce a reference-generation or
byte-comparison stage.

**Copy the production database live** — settled (2026-07-19, also FR-3 authorization
2026-07-17). His words:
> "You can copy the database without stopping the service"
The live daemon and production state stay untouched; only a copy is used. A copy
exists at `~/.local/state/spirit-db-test-copy.sema` (verified present this pass).
Bears on the Spirit port (`primary-56d1.39`).

**Vocabulary correction: not "text"** — settled (2026-07-19). His words:
> "text? daemons use rkyv, which is binary"
Say "authored schema surface" or "TextualForm view", never bare "text", for the
human-authored surface; the daemons' runtime representation is binary (rkyv). He
also parked a follow-up on this (§7 / §6).

**Nomos macro-surface fragments** — settled fragments (tracker `primary-56d1.2`;
`nomos-macro-model-v1.md`). His words:
> "why lowercase? isnt WireNewtype a thing?" (macro identifiers are Capitalized
> objects)
> "so if WireNewType only takes a name and inner type, then the input field would be
> `{ Name Type }`. Name and Type could be pretty standard things, perhaps nomos
> builtins, even a concept shared with schema somehow (it is a schema concept after
> all)."
The last clause is a HEDGE (§6), not a ruling.

## 6. Hedged leans (verbatim hedge preserved — NOT settled)

**Item-envelope for the logos-item** — HEDGED (2026-07-19; tracker
`primary-56d1.43`). His words, hedge preserved:
> "I think I prefer CommitSequence.Newtype.{ … } with a field in the struct for
> visibility (Public Private variant?)"
This is a lean (note "I think I prefer" and the trailing "?"), NOT a ruling. It
selects a name-led framing (`CommitSequence.Newtype.{ … }`) over the kind-keyword-led
codec form. It MUST now be read under the §4 total ban: any "field in the struct for
visibility" is a POSITIONAL Visibility-typed slot, never a named field. Honest
tension he has not resolved: the real CommitSequence item carries TWO visibilities
(outer at item level, inner on the wrapped field) plus a three-attribute preamble, so
"a field for visibility" must say WHICH visibility and where the inner Private and the
attribute preamble sit.

**`EncodedForm` naming** — HEDGED (tracker `primary-56d1.37`, `.31`). His words,
hedge preserved:
> "TextualForm vs CoreForm (which I think could be called EncodedForm?)"
"which I think could be called" is the lean. Its scope (trait-only vs concrete-type
rename) is a live open question — §7.

**Nomos meta-types = schema's seed vocabulary?** — HEDGED (`nomos-macro-model-v1.md`
§2d). His words, hedge preserved:
> "perhaps nomos builtins, even a concept shared with schema somehow (it is a schema
> concept after all)."

**A library for Rust-like languages** — HEDGED future vision (§3, Ruling 3):
> "maybe we could create a library for languages a bit more like Rust"
Recorded, not scheduled.

**Kernel-hardening / trusted-evaluator acceptances** — HEDGED trust (up-close §4.6):
> "1. trusting the recommendation without a clear view, but the surface sounds
> correct."
> "2. yes, that is great design, and a reason I was going this way."

## 7. Open questions to carry (each self-contained, in his terms)

**The rename fork — is `EncodedForm` the trait only, or do the concrete types rename
too?** OPEN and internally contradictory across artifacts (tracker `primary-56d1.25`,
`.37`). His words on the two halves:
> "a - sema will be more complete and correct than core; we are laying the foundation
> for it." (2026-07-16: Core stays the canonical stringless data-layer name; sema
> names the durable storage/runtime component)
> "Core becomes EncodedForm (rename; also it is at least a trait in a library which
> creates the re-usable pieces) EncodedForm<T> -> EncodedForm<X> or similar."
> (2026-07-18: appears to reverse the "Core* prefixes stay" half)
The unresolved question, in agent terms awaiting his word: does "Core becomes
EncodedForm" mean the TRAIT / view-name only (concrete `Core*` type names stay,
per the `.25` preservation), or do the concrete `Core*` types ALSO rename (a separate
multi-repo rename train, downstream waits)? This is HIS to settle; the two framings
cannot both hold. (An agent note also records a subsequent trait rename to `Textual`
with `EncodedForm`/`EncodedConversion` as the truth side — verify against the crates
before trusting; do not treat it as his ruling.)

**The item-envelope lean under the total ban** — OPEN (tracker `primary-56d1.43`).
His hedged lean (§6) must be rendered over the REAL CommitSequence item with
visibility as a positional slot and the attribute preamble placed; shown to him to
rule. Do not present any field-named rendering. The kind-keyword-led candidate that
IS codec-verified real output (no field names — all dotted forms are applications):
`Newtype.{Public [ToolPath.rustfmt.skip Configuration.{Feature.nota-text
Derive.[nota.NotaDecode nota.NotaDecodeTraced nota.NotaEncode]} Derive.[rkyv.Archive
rkyv.Serialize rkyv.Deserialize Clone Debug PartialEq Eq]] CommitSequence Private
Integer}` (source: core-logos round-trip, legal positional form). His lean prefers a
name-led framing instead; the reconciliation is his to rule.

**The Stream kind representation decision** — OPEN, gated on his design acceptance
(tracker `primary-56d1.48`; `stream-construct-design-v1.md` §0.0). Two joints remain:
(1) the close-leg semantics — his words **"I dont follow all that."** is a
lost-understanding signal, NOT a ruling; the close-leg (mandatory vs defaulted) is
re-grounded to him and stays open (he separately affirmed a close EVENT exists, §5);
(2) the Nomos-minted-kind bootstrap: the kind vocabulary today is closed,
exhaustively-matched Rust enums, so "just create a new kind of object via Nomos"
cannot be honored without a minimal hook into core-schema/core-nomos — a
kind-system-topology change gated on his explicit design acceptance before any
implementation.

**Escape sigil and piped forms** — OPEN (tracker `primary-56d1.9`, `.42`;
`nomos-macro-model-v1.md` §4/§6). He ruled the escape must be structural and
nomos-owned; the choice between the `$` sigil and the `<< >>` bracket is unsettled,
and neither binds as an escape today (both raw-parse as bare atoms until the nomos
grammar owns them). A possible fourth escape (name synthesis) is agent-surfaced,
awaiting his word.

**Protos crate mapping** — OPEN (his own trailing question in §3;
`textual-form-vision-design-v2.md` [DECISION 2′]). The NAME `Protos` and its SCOPE
(the one shared structural library) are accepted; only the crate topology is open:
fold the delivered structural-codec + name-table into one `protos` crate, an umbrella
re-exporting them, or a rename-only `protos-*` family. His to settle; no rename done.

**Public-repo verbatims** — OPEN. Whether any of his vision here should land as public
Spirit intent / public repo guidance is unsettled; nothing public was recorded this
effort. Keep private/personal substance out of any public surface.

**NameTable question** — OPEN, status of the question itself pending his word. It was
proposed to be DROPPED as a handover error; his confirmation to drop-or-keep is
pending. (Related live proposal: NameTables as first-class co-versioned siblings of
Core in each daemon store, tracker `primary-56d1.10`, non-rejected but not accepted.)

**Review-pile remnants** — OPEN review commitment (2026-07-19). His words: **"lets
review those too."** The remnants to review: the `.9` syntax slate (macro dotting,
escapes, sigil, meta-types, visibility, delimiters, rustfmt.skip), the `.10` storage
pair (format-upgrade mechanism, co-versioned NameTables), `.12` (the lost/unrecoverable
next-gen bootstrap question 2, which only HE can restate from memory), `.14`
(reports/logos hygiene — his originating directive: **"We should make sure we dont
grow a pile of stale design there"**), and `.38` (short-header byte layout: keep
legacy-derived wire values or revise — he has not reviewed the wire/frame design).

**Clarification-skill shape** — OPEN (2026-07-19). His words:
> "I want to discuss a skill that I can refer for this; where I have a hard time or
> no idea what the agent is talking about, and I feel like I and/or the agent have
> lost the real vision and am probably going to see slop unless I actually understand
> and guide the vision properly. call it clarification"
The skill is under discussion, not designed. He also parked a related note:
> "so we need more skill reinforcement in terms of the language we use to discuss
> those things. dont panic-send an agent, just make a note of it for later"
Parked deliberately; do not dispatch on it — it is a note for later.

**The deterministic positional collision rule's concrete form** — OPEN (§4). The
directive to create a deterministic rule for structs holding more than one field of
the same type STANDS; its concrete form (how position assigns meaning when types
collide) is to be worked out and shown to him on REAL artifacts, never with invented
or field-named syntax.

## 8. Durable-artifact pointers (verify here, not in prose)

- Design authorities with the later-authority ruling-capture sections:
  `reports/logos/textual-form-vision-design-v2.md` (§0.0 FR-1..FR-5 is the later
  authority for the TextualForm/EncodedForm vision, Protos name, four v2 rulings) and
  `reports/logos/stream-construct-design-v1.md` (§0.0 is the later authority for the
  Stream kind rulings; NOTE its Ruling C spelling and the `DatabaseMarker` fixture it
  cites are now illegal under §4). Supporting: `core-first-architecture-v1.md`
  (schema-unit thesis — contains NO fresh psyche verbatims, all restatement),
  `nomos-macro-model-v1.md` (Nomos macro surface, escapes), `up-close-design-v1.md`
  (four-crate family, the True*→Textual* rename, structural-form).
- Tracker epic `primary-56d1` (its DESCRIPTION oracle line is SUPERSEDED — see §5
  working-programs ruling) and its items; the psyche-review/decision cluster carries
  the verbatims: `.8 .11 .25 .27 .29 .31 .36 .37 .43 .47 .48` (settled/hedged) and
  `.9 .10 .12 .14 .26 .38` (open/blocked-on-psyche). Epic NOTES carry the
  DECISION-SLATE and PROTOS-POSITIONAL-LAW capture records (2026-07-19).
- Live production-db copy for the Spirit port: `~/.local/state/spirit-db-test-copy.sema`
  (present, ~987 KB). Port constraint on `.39`: upgrade Spirit only with a
  vestige-aware sema-engine (>= 0.11.1), or it wedges on legacy outbox rows.
- Spirit accepted-intent records (§2): jys2, zn2l, w312, vjvm, l62s, qvb3, lta7,
  izsf, sj2c, cam8, 16jw, hv5f, w1mm, t5qr — query read-only with
  `spirit "(Lookup <id>)"`.
- `protos-syntax` skill (`.claude/skills/protos-syntax/SKILL.md`): seats
  positionality-absolute but still carries the codec-emitted collision exception and
  its example — needs correction to the §4 total ban and the deterministic positional
  rule, and adoption into the manager packet by default (his directive).

## 9. Every 2026-07-19 verbatim, exactly as given (index)

Load-bearing quotes from today, each already placed in its section above; listed here
together so none is lost:

1. "field names are now COMPLETLY ILLEGAL EVERYWHERE" — §4, settled (total ban).
2. "and yes, we should have a stream close event" — §5, settled.
3. "the legacy dialect had the same field-name illegality" — §4, correction of an
   agent error.
4. "THERE ARE NO FIELDS NAMES! ALL FIELDS ARE POSITIONAL! FIELD NAMES ARE ALMOST
   NEVER ALLOWED! WRITE IT SOMEWHERE YOU WONT FORGET! MAKE PROTOS SKILL CORRECT, AND
   MAKE IT A PART OF MANAGER! I NEVER WANT TO SEE THIS AGAIN!" — §4 ("almost never"
   subsequently hardened to the total ban).
5. "negative examples are forbidden in skills" / "also, negative examples are
   forbidden in skills. make sure that is clear to skill-editor role also" — §1,
   settled.
6. "since agents seem TOTALLY FUCKING INCAPABLE of understanding the field-name rule,
   maybe we should just OUTRIGHT FORBID FIELD NAMES, and create a deterministic rule
   for structs that contain more than one field with the same type" — §4 (the
   "maybe" resolved by the total ban; the deterministic-rule directive stands).
7. "I think I prefer CommitSequence.Newtype.{ … } with a field in the struct for
   visibility (Public Private variant?)" — §6, hedged (read under the total ban: any
   visibility field is a positional slot, never named).
8. "text? daemons use rkyv, which is binary" — §5, vocabulary correction.
9. "so we need more skill reinforcement in terms of the language we use to discuss
   those things. dont panic-send an agent, just make a note of it for later" — §7,
   open/parked.
10. "I want to discuss a skill that I can refer for this; where I have a hard time or
    no idea what the agent is talking about, and I feel like I and/or the agent have
    lost the real vision and am probably going to see slop unless I actually
    understand and guide the vision properly. call it clarification" — §7, open.
11. "lets review those too" — §7, open review commitment (.9 .10 .12 .14 .38).
12. "You can copy the database without stopping the service" — §5, settled (db copy
    at ~/.local/state/spirit-db-test-copy.sema).
13. "hiding stuff? instructing agents to hide stuff from me? WtF!?" — §1, disclosure
    law (fabrication barred, never disclosure; nothing real withheld from him).
14. "I feel like we should start this all over again" — the reason this handover
    exists (top).
