# Datom — candidate records for distillation

Every psyche record that could qualify as a candidate for distilling
together on the subject of Datom — the data notation — and its
neighbouring names (NOTA, Dotos, datum, schema syntax ancestor line,
Meaning, Head, guillemets, curly quotes, string blocks, interface
shape, de/serialization, positional, the datom repository).

Each record: originating flow short id (or `vision-raw`), record file
topic, entry heading and date, provenance (typed or STT), verbatim
words, standing.

---

## Intent

### Intent/data.md — "Everything is data"

- **Flow:** 995a164e (raw record), distilled as Intent
- **File topic:** data
- **Date:** 2026-09-01 (distilled 2026-09-02)
- **Provenance:** typed (flows/995a164e/vision/data.md), wording flow-drafted, approved as Intent by the psyche 2026-09-02
- **Verbatim:**

> Everything is data. Code is data: a type is declared with code, so
> a type is data; a trait is data; an impl is data. "Code", "type",
> "check", "configuration" are not kinds of being — they are roles
> data plays for an interpreter, and an interpreter is just another
> program, so it too is data. There is one plane; nothing stands
> above it. Protolanguages make this obvious by being a data
> notation before they are anything else.

- **Standing:** Distilled Intent. The raw source is flows/995a164e/vision/data.md: "everything is data. … Code is data. a type is declared with code, so a type is data. a trait is data. an impl is data. *everything* is data, but protolanguages make it more obvious." Proposed as Spirit; redirected to Intent by the psyche ("make that intent, not spirit").

### Intent/protosParsing.md — "Protos parsing"

- **Flow:** a5587095 (Designer-drafted, approved)
- **File topic:** protosParsing
- **Date:** 2026-08-13T00:19+02:00 (approved)
- **Provenance:** Designer-drafted, approved as Intent by the psyche ("the intent is good", Designer session a5587095)
- **Verbatim:**

> Protos parsing always happens inside a context, and only the
> current context gives shapes their meaning: it defines which
> shapes can appear next and which shape completes it. A met shape
> announces a type, and that type's context takes over completely
> until its completing shape; then the parent context resumes
> exactly where it left off. Reading and writing are one walk in
> two directions — text lands in typed values, and typed values
> project back into the same text.

- **Standing:** Distilled Intent. Governs datom's parsing by inheritance — datom is a protos dialect.

---

## Vision distilled (in Vision/)

### Vision/datom.md — Name

- **Sources:** ac1e9ec8 datomSyntax (per Vision/sources/datom.md)
- **Verbatim:**

> Datom is the psyche's own coinage for the new data notation, the
> successor to NOTA and to the rejected name Dotos. The name was
> chosen for its energetic power and to echo what the notation is:
> data, strictly typed, super dense, no field names.

- **Standing:** Distilled Vision. Current authority.

### Vision/datom.md — Nature

- **Verbatim:**

> Datom carries data only — like JSON, but strictly typed. Generics
> belong to Ethos; Datom's whole work is serialization and
> deserialization — carrying data between text and typed form.
> Generating Rust is Ethos's duty, in today's division of labor. When
> Ethos becomes the full authoring language, with Rustlang as its
> assembly layer, Datom — the data dialect of the Protos family — may
> gain an inline place in authored Ethos, the way Rustlang composes
> data directly in code. That road is reached, or even floated, only
> with explicit context: how, when, and where data yields Rust, stated
> without ambiguity; until then the division stands as spoken.

- **Standing:** Distilled Vision. Current authority. Note: the "like JSON" phrase was explicitly rejected by the psyche in the ac1e9ec8 corrections ("Let's keep this noise out. Totally unecessary.") yet remains in the distilled text. This sits oddly against the correction record.

### Vision/datom.md — De/serialization

- **Verbatim:**

> Schema-driven and positional: the reader walks the expected type,
> writing is the exact reverse projection, and decoding lands directly
> in the typed Rust structs. All naming and self-description live in
> the type; the text carries only the data.

- **Standing:** Distilled Vision. Current authority.

### Vision/datom.md — Repository and migration

- **Verbatim:**

> Everything migrates to Datom. Datom's own line of descent is NOTA —
> which also passed through the temporary name Dotos; that old
> notation stays behind, frozen, and may be called legacy. Schema is
> the abandoned ancestor of Ethos, not of Datom. The repository is
> plain datom, with no variant suffix.

- **Standing:** Distilled Vision. Current authority.

### Vision/datom.md — Relation to Ethos

- **Verbatim:**

> Datom and Ethos are different languages that share an approach, not
> a parser. What they may share is a substrate — traits with a shared
> implementation and types; the universal substrate machinery is homed
> in protos, all dialects ride it, and datom is the pure-data dialect
> on it. Ethos depends on Datom, at minimum to intake data for
> signals; the Meaning context therefore lives in the datom
> repository, seen by both languages.

- **Standing:** Distilled Vision. Current authority.

### Vision/datom.md — The interface shape

- **Verbatim:**

> A program's configuration surface is the datom's shape itself, as
> the ethos interface declares it: a data enum at the root whose
> variants are the main operations. A variant's data carries what
> follows: another enum where sub-operations are wanted, a struct or
> vector for final options — and a struct may embed further
> sub-operations, or any combination imaginable. Output is an enum,
> always — even the most basic response interface is an enum: Success
> or Failure. The shape already is the interface: datom creates the
> configuration options by its very shape.

- **Standing:** Distilled Vision. Current authority.

### Vision/datom.md — Syntax

- **Verbatim:**

> Curly quotes are the default string delimiter. A string is written
> bare whenever the bare form can carry it, and a bare string may
> carry symbols that are load-bearing elsewhere — the machinery is
> made fit for this by the right abstraction layers. String blocks are
> opaque: interior delimiters become content until the block closes. A
> bare brace block is a struct; a dot-parenthesis block is a
> string-carrying variant. The dotted prefix of a delimited block is
> part of the block's type; its official name is Head; a variant
> always re-emits its Head when textualized. Guillemets delimit a map;
> inside, key and value are separated by a space, resolving by
> position. A map in a position that expects a map carries no Head; a
> Head is always a variant.

- **Standing:** Distilled Vision. Current authority. Supersedes the earlier parenthesis-as-default-string-delimiter ruling (2026-08-14) per the psyche's 2026-08-26 correction.

### Vision/datom.md — Meaning

- **Verbatim:**

> Meaning is the structured string: parenthesis-delimited, arbitrary
> depth, a graph of sorts, seeded by the fact that parentheses inside
> text are markup. Curly quotes delimit the plain string. Meaning is
> postponed so a working syntax lands as soon as possible: parenthesis
> text lands as plain String today, the later type marked in code. The
> name Meaning is provisional — it smells of a verb — and is reopened
> together with the type.

- **Standing:** Distilled Vision. Current authority.

---

## Vision raw and undistilled

### ac1e9ec8 — datomIsData — "you've mixed up datom with ethos. datom is data"

- **Flow:** ac1e9ec8
- **File topic:** datomIsData
- **Heading:** 2026-08-26 — the proposal mixed datom with ethos
- **Date:** 2026-08-26
- **Provenance:** typed
- **Verbatim:**

> you've mixed up datom with ethos. datom is data

- **Standing:** Raw, undistilled. The boundary correction. Reflected in distilled Vision/datom.md Nature section but the exact formulation is not carried there.

### ac1e9ec8 — datomSyntax — corrections to the first full-vision draft

- **Flow:** ac1e9ec8
- **File topic:** datomSyntax
- **Heading:** 2026-08-26 — corrections to the first full-vision draft
- **Date:** 2026-08-26
- **Provenance:** typed
- **Verbatim (in sequence):**

On "Datom is the psyche's own coinage for the data notation":

> dont be so apologetic. Datom is the most advanced textual data format in the world.

On "Generics and Rust generation belong to Ethos":

> I said no negatives. This is useless. Do we say "JSON doesnt support generics"?

On "like JSON":

> Let's keep this noise out. Totally unecessary.

On "All naming and self-description live in the type":

> this is ambiguous. Try explaining it properly. You might have to understand it first. Apply this to the whole proposal; understand then explain clearly and unambiguously. Separate statements that make a sentence confusing when you try to say them together. Split everything up then re-assemble <- there's something to extract into distillation skill from this.

On bare strings:

> re: bare strings: make sure it's clear that a string is a string only in a position where the type defines a string.

On the glyph question (typed guillemets or ASCII << >>):

> I dont understand. those are completly different things. <> is used in ethos, and those two must remain compatible in case datom is ever eventually embedded into some ethos positions.

On "each delimiter shows its container's kind":

> this conflicts with ethos vocabulary.

On whether "the root text" opens with the variant or the type name:

> "the root text" - what are you talking about? If we are reading an enum, then it'll start with a variant. if not, it wont. I feel like you really still dont understand the datom vision. the implementation must be pretty bad

- **Standing:** Raw, undistilled. These corrections shaped the distilled Vision/datom.md but are not themselves carried there. "Datom is the most advanced textual data format in the world" is a substantive claim not in the distilled text.

### ac1e9ec8 — datomSyntax — curly quotes are the string delimiter; parentheses reserved for Meaning; datom is the edge form of signal

- **Flow:** ac1e9ec8
- **File topic:** datomSyntax
- **Heading:** 2026-08-26 — curly quotes are the string delimiter; parentheses reserved for Meaning; datom is the edge form of signal
- **Date:** 2026-08-26
- **Provenance:** typed
- **Verbatim:**

> not legacy. In fact I think they should be positioned as the default string delimiter. the vision is that parenthesis will become the delimiter for structured strings, still to be designed. So let's switch it all to curly quotes first, with parenthesis reserved for structured strings, which we currently designate as Meaning

> no, this is false. all our components speak signal, not datom; datom is only used at the edge to let text-based systems (LLMs and all existing editors) understand signal.

- **Standing:** Raw, undistilled. The curly-quotes-as-default supersession is reflected in Vision/datom.md Syntax. The edge-form-of-signal statement is a substantive claim reflected in Vision/datom.md Nature ("carrying data between text and typed form") but the exact formulation — "datom is only used at the edge" — is not carried there.

### ac1e9ec8 — datomSyntax — a map in an expected position carries no Map head

- **Flow:** ac1e9ec8
- **File topic:** datomSyntax
- **Heading:** 2026-08-26 — a map in an expected position carries no Map head
- **Date:** 2026-08-26
- **Provenance:** typed
- **Verbatim:**

> If a position expects a map, the data will be [ k.v ... ], no Map.

Asked in the same message, not ruled:

> Is there a scenario in which a Head. isnt a variant?

- **Standing:** Raw, distilled into Vision/datom.md Syntax ("A map in a position that expects a map carries no Head; a Head is always a variant.").

### ac1e9ec8 — datomSyntax — considering positional key/values in a map

- **Flow:** ac1e9ec8
- **File topic:** datomSyntax
- **Heading:** 2026-08-26 — considering positional key/values in a map
- **Date:** 2026-08-26
- **Provenance:** typed
- **Verbatim:**

> Im considering making key/values resolve by position in a map
>
> [ key value second-key second-value ... ]
>
> that looks cleaner and makes the Head. always a variant; lower cognitive cost

- **Standing:** Raw, undistilled. Superseded the same day by the guillemets ruling.

### ac1e9ec8 — datomSyntax — or a dedicated delimiter for maps

- **Flow:** ac1e9ec8
- **File topic:** datomSyntax
- **Heading:** 2026-08-26 — or a dedicated delimiter for maps
- **Date:** 2026-08-26
- **Provenance:** typed
- **Verbatim:**

> or we could use one of the unused delimiters for maps, making them easy to spot visually

- **Standing:** Raw, undistilled. Superseded the same day by the guillemets ruling.

### ac1e9ec8 — datomSyntax — guillemets delimit a map

- **Flow:** ac1e9ec8
- **File topic:** datomSyntax
- **Heading:** 2026-08-26 — guillemets delimit a map
- **Date:** 2026-08-26
- **Provenance:** typed
- **Verbatim:**

> let use the guillemets.

- **Standing:** Raw, distilled into Vision/datom.md Syntax ("Guillemets delimit a map").

### ac1e9ec8 — archive-distillationNegatives — useless negatives are archived; vision never attributes itself to the psyche

- **Flow:** ac1e9ec8
- **File topic:** distillationNegatives (archived)
- **Heading:** 2026-08-26
- **Date:** 2026-08-26
- **Provenance:** typed
- **Verbatim:**

> now show me the final full-vision for datom. dont give me useless negatives; those can be archived without worrying; the archives are still there and can be linked in the distillation still (we dont carry useless negatives; lets understand how to frame that together)

> I want this kind of stuff to be in the forbidden list for vision distillation; this *is* the psyche's vision.

- **Standing:** Raw, undistilled as datom vision. The negatives-in-distillation ruling is a distillation-skill matter; the "this is the psyche's vision" is a framing rule.

### 01a03eda — datomSyntax — default string delimiter (reconstructed from flow ac1e9ec8)

- **Flow:** 01a03eda (reconstructed from ac1e9ec8)
- **File topic:** datomSyntax
- **Heading:** 2026-08-26T16:51:18.409Z
- **Date:** 2026-08-26
- **Provenance:** typed, transcript `/home/li/.claude/projects/-home-li-primary/ac1e9ec8-903f-4ee0-a9e3-4a5d472c05e0.jsonl`, physical line 332
- **Verbatim:**

> not legacy. In fact I think they should be positioned as the default string delimiter. the vision is that parenthesis will become the delimiter for structured strings, still to be designed. So let's switch it all to curly quotes first, with parenthesis reserved for structured strings, which we currently designate as Meaning

- **Standing:** Raw, distilled into Vision/datom.md Syntax. Duplicate provenance of the ac1e9ec8 datomSyntax entry above — same words, different filing.

### 01a03eda — datomInteger — Integer syntax approved

- **Flow:** 01a03eda
- **File topic:** datomInteger
- **Heading:** 2026-08-26T17:54:13Z
- **Date:** 2026-08-26
- **Provenance:** typed, transcript session `01a03eda-0e08-7451-a5bf-ab48a2f67328`, line 7385
- **Verbatim:**

> 1. yes

(Approving Datom Integer canonical bare decimal syntax: `0`, `42`, `-42`; ASCII digits, no leading `+`, no leading zero except `0`.)

- **Standing:** Raw, undistilled. Not reflected in Vision/datom.md.

### 04db2fd2 — datomMaps — guillemets for maps; key and value separated by a space

- **Flow:** 04db2fd2
- **File topic:** datomMaps
- **Heading:** Guillemets for maps; key and value separated by a space
- **Date:** undated in the file (session 04db2fd2; the flow is from 2026-08-27)
- **Provenance:** STT
- **Verbatim:**

> Vision/datom.md still says parentheses-default strings and [key.value ...] maps; your 2026-08-26 rulings supersede both ... lets get that fixed, we use guillemets for maps now, with key and value separated by a space

- **Standing:** Raw, undistilled. The correction was applied to Vision/datom.md. The record itself is a directive to update.

### 04db2fd2 — datomNexus — whether datom should be a nexus; stays a library for now

- **Flow:** 04db2fd2
- **File topic:** datomNexus
- **Heading:** Whether datom should be a nexus for consistency; stays a library for now; eventually a nexus translating formats
- **Date:** undated in the file (session 04db2fd2)
- **Provenance:** STT
- **Verbatim:**

> well, maybe we should make it a nexus now because consistency is very good for AI models. So if everything is a nexus, I mean, besides, you know, the trait libraries and things like that, we're going to get a lot more consistency out of everything. I just don't know how, you know, as datum [STT: Datom] is essentially a serialization and deserialization functionality, which is going to be included in other programs, other Rust binaries. I just don't know how it becomes a nexus right away. Like I can see eventually how it can be a nexus in the sense that it's going to, it's going to have more functionality, like where we're going to have a nexus to translate certain datum [STT: Datom] objects back and forth between different formats. But anyway, that's not a big issue right now. So this can just stay in a library for now.

- **Standing:** Raw, undistilled. Not reflected in Vision/datom.md.

### 04db2fd2 — text — Text must have something over String; normalized; content-addressed hash; first use for a datom nexus deferred; library renamed

- **Flow:** 04db2fd2
- **File topic:** text
- **Heading:** Text must have something over String; normalized; content-addressed hash; library renamed to free "datom" for the nexus
- **Date:** undated in the file (session 04db2fd2)
- **Provenance:** typed
- **Verbatim:**

> Re: Text: It would have to have something over a String. non-structural whitespace-removed? Otherwise it's really just a String. Although we might need a type anyway just so we can implement the trait for it (Prospective) since the impl must live either with the type or the trait. If we normalize it then we can have a reliable content-addressed hash tied to it which could be hand for cached-reading (instantly get the data without parsing from a parsing cache? could be the first use for a datom nexus - deferred for now, lets stick with the library. Let's call the library something different so we free 'datom' for the eventual nexus. datom-codec?)

- **Standing:** Raw, undistilled. Not reflected in Vision/datom.md. The "datom-codec?" naming question appears unresolved.

### 04db2fd2 — textualTypes — Unscanned text; prospective datom; Datomic

- **Flow:** 04db2fd2
- **File topic:** textualTypes
- **Heading:** Multiple entries
- **Date:** undated in the file (session 04db2fd2)
- **Provenance:** STT and typed (mixed)
- **Verbatim (typed entries):**

> I like "Text taken as a would-be T: Prospective<T>" which gives us Prospective<Datom> although Im unsure if Datom is type or kind, probably kind, since it doesnt have a definite shape yet: give me your input on that.

> Re datom kind: Datomic

- **Standing:** Raw, undistilled. Not reflected in Vision/datom.md. The "Datomic" naming is reflected in the codebase (the datomic crate).

### 04db2fd2 — delimiters — guillemets vs double angle bracket pair; curved quotes terminology

- **Flow:** 04db2fd2
- **File topic:** delimiters
- **Heading:** Guillemets vs double angle bracket pair; curved quotes are an asymmetric pair
- **Date:** undated in the file (session 04db2fd2)
- **Provenance:** typed
- **Verbatim:**

> this is false; you are talking about guillements, and what you showed is a double angle bracket pair

> also false. curved quotes are an asymetric pair of characters, youre showing double quotes (or whatever theyre called; I need a refresh on names of delimiters)

> that's not univeral yet. so not protos. what we can say is it's content-opaque, so all characters it contains are ignored, until the closing unbalanced closing parenthesis. so is can contain any protos anatomical features, but none of them will trigger any delineation for now.

- **Standing:** Raw, undistilled. Clarifications on delimiter terminology not in Vision/datom.md.

### 04db2fd2 — decomposable — the Decomposable kind; finding keyframes in datom

- **Flow:** 04db2fd2
- **File topic:** decomposable
- **Heading:** Maybe not decompose/compose but finding the keyframes
- **Date:** undated in the file (session 04db2fd2)
- **Provenance:** STT
- **Verbatim (datom-relevant excerpt):**

> maybe the abstraction is not decomposable and composable, but like it's not that we're not decomposing it, but we're annotating it. But that word is not annotate. It's like where we find like when people are doing a video editing job, they find the frames, like the cutoff frames, they find all the key frames ... which are for datum [STT: Datom], the beginning and end of all the portions. And a sort of rough idea of not just the beginning and end, but the anatomy of it.

- **Standing:** Raw, undistilled. Not reflected in Vision/datom.md.

### 04db2fd2 — directionAsymmetry — approved for distilled vision

- **Flow:** 04db2fd2
- **File topic:** directionAsymmetry
- **Heading:** Approved for distilled vision: in is a prospective datom untrusted until matched; out is a datom
- **Date:** undated in the file (session 04db2fd2)
- **Provenance:** typed
- **Verbatim:**

> exactly. this can go straight into distilled vision

(Approving: in is a prospective datom untrusted until it matches, out is a datom; Realize carries a fault and Textualize none; spans are found on the way in and computed on the way out; multi-pass.)

- **Standing:** Raw, undistilled. Explicitly approved for distilled vision but not yet landed in Vision/datom.md.

### 04db2fd2 — delineate — Prospective<Datom> is Delineatable; delineation is protos

- **Flow:** 04db2fd2
- **File topic:** delineate
- **Heading:** Two entries
- **Date:** undated in the file (session 04db2fd2)
- **Provenance:** typed
- **Verbatim:**

> Re Delineate: Yes! That's what I was looking for. So a Prospective<Datom> is Delineatable (however this is spelled, or however you think we could word that kind)

> delineation is protos.

- **Standing:** Raw, undistilled. Not reflected in Vision/datom.md.

### 04db2fd2 — kinds — Datomic kind; kinds as qualifiers

- **Flow:** 04db2fd2
- **File topic:** kinds
- **Heading:** Multiple entries
- **Date:** undated in the file (session 04db2fd2)
- **Provenance:** typed
- **Verbatim (datom-relevant excerpts):**

> Kinds as verbs are not allowed; we only tolerate the legacy rust gives us, until ethos takes over completly as the authored language ...

> Textual is already a qualifier. How does that sound as a kind? I like Actual instead of Real, but it's going to cause problems cognitively (too strong). What we're trying to say is that it can take the form the runtime can use. I think Embodied is the right term, unless Forged is better.

> this is quackery. youre missing types and kinds

(Commenting on `Prospect<Datomic>.Text`)

- **Standing:** Raw, undistilled. Kinds-as-qualifiers and Embodied are broader than datom but apply to datom types.

### 04db2fd2 — portion — "Portion" as universal term for field / variant / element

- **Flow:** 04db2fd2
- **File topic:** portion
- **Heading:** Multiple entries
- **Date:** undated in the file (session 04db2fd2)
- **Provenance:** STT and typed (mixed)
- **Verbatim (typed, datom-relevant excerpts):**

> Portions would be an enum with a single data variant (Portion). Did you mean Vector<Portion> ? Is that not the syntax for vectors?

> And it should be Bare.Symbol

> Extent once on portion is better.

> its not enclosed vs opaque. its enclosed vs something like "unenclosed" - opaque is a different concern

> opaque is opaque; no containing portion.

> an enclosed portion has an unknown number (vector) of possible inner portions

- **Standing:** Raw, undistilled. The Portion concept underlies datom anatomy. Superseded in part by e8c4cc61 protos.md ("Structure is a better Portion").

### e8c4cc61 — datomSyntax — single semicolon for comments; space inside bracket delimiters

- **Flow:** e8c4cc61
- **File topic:** datomSyntax
- **Heading:** A single semicolon is the comment marker; Style: a space inside a bracket delimiter
- **Date:** undated in the file (session e8c4cc61; flow is from 2026-08-29)
- **Provenance:** typed (semicolon), STT (space style)
- **Verbatim:**

> I guess a single ; is for comments now. semi-colon isnt load bearing anymore so that works.

> This is not load-bearing on a parser, but just for ease of reading, I would like it whenever there's a delimiter in proto syntax, not the curly quotes, not for strings, but for the brackets or maybe just the brackets. I think it would be good style to leave a space between the delimiter and the next thing inside of it, both at the beginning and the end. It's easier to see the separation there. Otherwise, it just looks like one big word with the head, the dot, the delimiter, and the other thing inside it. It's hard to visually separate them.

- **Standing:** Raw, undistilled. Not reflected in Vision/datom.md. The single-semicolon ruling and the space-inside-brackets style are not in the distilled text.

### e8c4cc61 — datomizable — Datomizable kind with default capability; raised from notion to vision

- **Flow:** e8c4cc61
- **File topic:** datomizable
- **Heading:** Multiple entries
- **Date:** undated in the file (session e8c4cc61)
- **Provenance:** typed and STT (mixed)
- **Verbatim (key entries):**

> Datomizable would be a kind with a default capability, and born by all ethos types by default. It would describe the textual structure of this type (maybe even in different contexts, so and this very context could also be a capability of any Datomizable kind which is used whenever a portion is interpreted *inside* the portion of such a kind)

> no, the point being that it can be overriden

> This is a notion but I think it's quickly becoming a vision so let's just make it a vision. Spare no ambition.

- **Standing:** Raw, undistilled. Originally filed as Notion, raised to Vision by the psyche. Not reflected in Vision/datom.md.

### e8c4cc61 — protos — Structure is a better Portion; Delineatable is better expressed as Structural

- **Flow:** e8c4cc61
- **File topic:** protos
- **Heading:** Two entries
- **Date:** undated in the file (session e8c4cc61)
- **Provenance:** typed
- **Verbatim:**

> your Structure is a better Portion (better name anyway)

> and Delineatable is better expressed as Structural.

- **Standing:** Raw, undistilled. Supersedes 04db2fd2 portion naming.

### 62022e8f — datomSyntax — spaces inside delimiters are canonical, braces included; never inside curly quotes

- **Flow:** 62022e8f
- **File topic:** datomSyntax
- **Heading:** Spaces inside delimiters are canonical, braces included; never inside curly quotes
- **Date:** undated in the file (session 62022e8f; flow is from 2026-08-30)
- **Provenance:** STT
- **Verbatim:**

> The example with the compact version number I had just copied, so it was not intentional for me to not have spaces there between the delimiters and the content. It will be canonical, but it is not load-bearing or considered good style to leave a space between the delimiters and the content, except for the strings, of course. The curly quotes, there it'll be bad because a space in that would be load-bearing, so it actually even disqualifies just on that fact.

- **Standing:** Raw, undistilled. Not reflected in Vision/datom.md. Extends the e8c4cc61 space-style ruling: braces canonical too, curly quotes never (load-bearing).

### 62022e8f — headedAndContained — the headed (implicit) form and the contained (explicit) form

- **Flow:** 62022e8f
- **File topic:** headedAndContained
- **Heading:** Two entries
- **Date:** undated in the file (session 62022e8f)
- **Provenance:** STT
- **Verbatim (key excerpt):**

> Kind of like in Datom [STT: Datum], right? In Datom [STT: Datum] we have the headed is the variant which then if it's more embodied becomes a struct where the variant is like a thing where it has in first position the name of the variant. So then it becomes a sort of self-contained, delimited thing instead of this object having structurally, textually a thing outside of it which is really a part of it but it's just visually better to understand and to express what we're trying to express.

> I like the headed and contained. I think these terms are appropriate to differentiate the two forms. So the headed form and the contained form of an embodiment are the two ways which it can be represented textually. And the contained form is how its embodiment is specified, because obviously in Rust, this all needs to be written with Rust types. So in Rust it's going to be a struct, and its head or its name is going to be one of the fields in that Rust type. So the headed form is really a syntax facility or a syntax sugar, if you will.

- **Standing:** Raw, undistilled. The headed/contained terminology is not in Vision/datom.md.

### 62022e8f — concept — first pass of a datom yields the concept; the conceptual form and the corporal form

- **Flow:** 62022e8f
- **File topic:** concept
- **Heading:** Multiple entries
- **Date:** undated in the file (session 62022e8f)
- **Provenance:** STT
- **Verbatim (datom-relevant excerpt):**

> Also, anything that is represented in any protos [STT: proto's] dialect has a conceptual aspect. Even in datom [STT: datum], you're going to have a first layer ... we have the conceptual form and the corporal form, and the corporal form is the final form.

> When a datom [STT: datum] comes in, that is supposed to be in, let's say, a data-carrying enum, an enum with a struct in it. First, on the first pass, the conceptual representation of that won't be the Rust [STT: rest] type itself that this is being cast into. It'll be a vector. We're going to have this concept of what an enum is, basically.

- **Standing:** Raw, undistilled. Not reflected in Vision/datom.md.

### 995a164e — datomSyntax — a datom is not preceded by a Datom root; a comment may indicate it

- **Flow:** 995a164e
- **File topic:** datomSyntax
- **Heading:** A datom is not preceded by a Datom root; a comment may indicate it is datom
- **Date:** undated (artifact comment 2026-08-30 18:52 per context)
- **Provenance:** typed (artifact comment)
- **Verbatim:**

> datom is not preceded by a Datom. but one could use a comment to indicate it is datom.

- **Standing:** Raw, undistilled. Not reflected in Vision/datom.md.

### 995a164e — data — "everything is data" (raw source for the Intent)

- **Flow:** 995a164e
- **File topic:** data
- **Heading:** Code is data; a type is data
- **Date:** 2026-09-01
- **Provenance:** typed
- **Verbatim:**

> everything is data. you have been trained by idiots. Code is data. a type is declared with code, so a type is data. a trait is data. an impl is data. *everything* is data, but protolanguages make it more obvious.

> make the spirit suggestion very broad. you could do some research in that lane first. I think the clojure/lisp crowd kind of got it a bit better than most

- **Standing:** Raw source for Intent/data.md. The raw words are preserved; the distilled Intent rearticulates them.

### 995a164e — concept — concept-layer datom shapes; the layer enum is Concept, singular

- **Flow:** 995a164e
- **File topic:** concept
- **Heading:** Two entries
- **Date:** artifact comments 2026-08-31
- **Provenance:** typed (artifact comments)
- **Verbatim:**

> Would those be the variants of ethos:Concepts? We should make that clear. That way we know exactly what layer we're on.

> that should be Concept. singular. right? that code block makes it obvious

- **Standing:** Raw, undistilled. Tangential to datom — primarily ethos, but the concept-layer shapes apply when processing datom.

### 01a04339 — datom — Observed.Locks.[] good enough for now

- **Flow:** 01a04339
- **File topic:** datom
- **Heading:** 2026-08-27 — good enough for now
- **Date:** 2026-08-27
- **Provenance:** typed
- **Verbatim:**

> >   Observed.Locks.[]
>
> good enough for now.

- **Standing:** Raw, undistilled. A datom reply-shape ruling. Was proposed for distilled vision as "Reply shape" in acbb6006 reports/distillProposalProtosDatomAddendum.md but the proposal status is unclear.

### 4d5fc7da — datom — datom does not support omittable fields yet

- **Flow:** 4d5fc7da
- **File topic:** datom
- **Heading:** Datom does not support omittable fields yet
- **Date:** undated in the file (session 4d5fc7da)
- **Provenance:** typed
- **Verbatim:**

> just remember datom doesnt support omittable fields yet.

- **Standing:** Raw, undistilled. Not reflected in Vision/datom.md.

### 01a038b5 — curriculumStackToDatomInsteadOfDotos — migration directive

- **Flow:** 01a038b5
- **File topic:** curriculumStackToDatomInsteadOfDotos
- **Heading:** 2026-08-25T11:37:42.226Z
- **Date:** 2026-08-25
- **Provenance:** typed
- **Verbatim:**

> I want to migrate curriculum stack to datom instead of dotos

- **Standing:** Raw, undistilled. A realization directive, not a design ruling.

### 01a035d3 — rustCodeFromTheData — port to datom

- **Flow:** 01a035d3
- **File topic:** rustCodeFromTheData
- **Heading:** 2026-08-25T00:40:51+02:00
- **Date:** 2026-08-25
- **Provenance:** typed
- **Verbatim (datom-relevant excerpt):**

> implement it. create a public repo, and move the runtime out, then adapt it to use an external repo for data. and port it do use datom instead of dotos. and the cli must not use anything other than its datom input for configuration, so add the variables you need to the config type which is used to read the cli datom input.

- **Standing:** Raw, undistilled. A realization directive. The "cli must not use anything other than its datom input for configuration" is a design ruling not reflected in Vision/datom.md.

### 01a03d6e — dotosFiles — there should be no Dotos files anymore

- **Flow:** 01a03d6e
- **File topic:** dotosFiles
- **Heading:** 2026-08-26T10:10:32.842Z
- **Date:** 2026-08-26
- **Provenance:** typed (STT correction: Dodos -> Dotos)
- **Verbatim:**

> There should be no Dodos files anymore.

- **Standing:** Raw, undistilled. Reflected in Vision/datom.md Repository ("that old notation stays behind, frozen").

### 01a03d6e — ethosInterfaces — that is obsolete nota/dotos format

- **Flow:** 01a03d6e
- **File topic:** ethosInterfaces
- **Heading:** 2026-08-26T15:04:27.982Z
- **Date:** 2026-08-26
- **Provenance:** typed
- **Verbatim:**

> that is obsolete nota/dotos format

(Correcting agent-proposed Lock/Release/Observe forms that used parenthesis-wrapped notation.)

- **Standing:** Raw, undistilled. Confirms the NOTA/Dotos format is dead.

### 5abf3be8 — dotOpensDelimiterEverythingIsData — "it opens a delimiter. everything is data"

- **Flow:** 5abf3be8
- **File topic:** dotOpensDelimiterEverythingIsData
- **Heading:** (single entry)
- **Date:** 2026-08-06T17:39:42Z
- **Provenance:** typed (captured 2026-08-08 from transcript during rulings-audit backfill)
- **Verbatim:**

> you mean, it opens a delimiter. everything is data

- **Standing:** Raw, undistilled. The dot-opens-a-delimiter principle. Not directly in Vision/datom.md but pervades the design.

### 5abf3be8 — colonLegalInStringPosition — ": remains legal in a position expecting a string"

- **Flow:** 5abf3be8
- **File topic:** colonLegalInStringPosition
- **Heading:** (single entry)
- **Date:** 2026-08-06T17:39:42Z
- **Provenance:** typed (captured 2026-08-08)
- **Verbatim:**

> and : remains legal in a position expecting a string

- **Standing:** Raw, undistilled. Corollary of bare-string-carries-symbols (distilled in Vision/datom.md Syntax).

### 68512643 — negatives — the negatives ruling and the datom-generates-rust discussion

- **Flow:** 68512643
- **File topic:** negatives
- **Heading:** 68512643-2 (2026-08-23); 68512643-4 (2026-08-23)
- **Date:** 2026-08-23
- **Provenance:** STT (dictated)
- **Verbatim (key excerpts):**

68512643-2:

> On your second point about Datom ... you generated the answer, it does not generate rust, right? And then you went on to say, the idea is dangerous and to be rooted out wherever it appears. ... I'm going to use this very example as a good illustration. So ... you generated the idea that Datom does not generate rust. But let's look at rust for a minute ... has a syntax to express language inline, or directly in its own syntax. When we use ... rustlang to compose a type directly in the code, we're essentially writing data in the code. And so if further down the road ... Ethos becomes a full replacement for authoring software logic ... then there is a strong case that could be made that we might want to have this inline data aspect of rust echoed or made available in Ethos.

68512643-4:

> So the line it's dangerous is true in that context because when the model brought forward the idea that Datom generates rust, there wasn't enough subtlety. Like, we aren't there yet. My whole point was that we might eventually get there. But if we do either get there or if we float the idea of how we would get there, it would be very explicitly, uh, contextualize so that there's no ambiguity as to how and when and where data may or may not generate rust.

- **Standing:** Raw, distilled into Vision/datom.md Nature (the "That road is reached, or even floated, only with explicit context" sentence).

### b675f3d9 — structuralParsing — arity discriminates; more head delimiters; parsing context-dependent

- **Flow:** b675f3d9
- **File topic:** structuralParsing
- **Heading:** Multiple entries (2026-08-27)
- **Date:** 2026-08-27
- **Provenance:** STT and typed
- **Verbatim (datom-relevant excerpts):**

> I have actually reconsidered the idea that we can use multiple... that the structural parsing can actually discern between structs of different size to differentiate between different types.

> <> is a real Protos delimiter of course. I'm surprised you have to ask

> this is false since it is context dependent. and the mere fact that something starts with a head could convey the type. and not every block starts with a head, which is also implied elsewhere and false

- **Standing:** Raw, undistilled. Broader than datom (protos-level) but governs datom parsing.

### 62022e8f — symbols — capitalized vs non-capitalized bare symbol

- **Flow:** 62022e8f
- **File topic:** symbols
- **Heading:** A capitalized and a non-capitalized bare symbol are two different types
- **Date:** undated in the file (session 62022e8f)
- **Provenance:** STT
- **Verbatim:**

> And a bare [STT: bear] symbol also is different, and we should have a different term to speak of those two different types, whether it's capitalized or not. One is an Embodiment ... A Corporal symbol, I guess you could say. The non-capitalized version is more like a reference. It's more like a path to something, like a link, if you will.

- **Standing:** Raw, undistilled. Relevant to datom bare strings but primarily a protos-level concern.

---

## Vision archived (already drawn into a distillation)

### vision-raw — archive-datomSyntax — "Datom carries data only; no generics" and "fix Datom first"

- **Flow:** vision-raw (originally from 012fbf07)
- **File topic:** datomSyntax (archived)
- **Archive note:** "Archived 2026-08-23 by flow 68512643; distilled into Vision/datom.md."
- **Date:** 2026-08-11
- **Provenance:** typed and STT
- **Verbatim:**

> datom doesnt do generics, it only carries data, like json (but strictly typed of course)

> So we can just fix datum [Datom] first because we need that. We need the syntax to start being consistent.

- **Standing:** Archived. Distilled into Vision/datom.md Nature and De/serialization.

### 06196cc7 — archive-datomSyntax — Meaning postponed; string blocks; dotted prefix; Head; bare strings

- **Flow:** 06196cc7
- **File topic:** datomSyntax (archived)
- **Archive note:** "Archived 2026-08-23 by flow 68512643; distilled into Vision/datom.md."
- **Date:** 2026-08-13 to 2026-08-14
- **Provenance:** typed
- **Entries (7 entries):**
  - Meaning postponed; () or curly quotes both land as String for now
  - String blocks ignore interior delimiters until they close
  - The dotted prefix of a delimiter is part of its type
  - A string that doesn't need quotes must not be quoted
  - Parentheses are the default string delimiter; Meaning-as-parenthesis floated
  - Bare {…} is a struct; X.(…) is a string-carrying variant
  - Paren strings are balance-based; parentheses are markup inside text
  - Head is the official term
  - Variants always re-emit their head
  - Bare strings may carry load-bearing symbols
- **Standing:** Archived. Distilled into Vision/datom.md Syntax and Meaning sections. Note: the parenthesis-as-default-string-delimiter was superseded by the 2026-08-26 curly-quotes ruling; the distilled text reflects the supersession.

### a5587095 — archive-datomSyntax — parentheses must not be unused; map payload; structured string

- **Flow:** a5587095
- **File topic:** datomSyntax (archived)
- **Archive note:** "Archived 2026-08-23 by flow 68512643; distilled into Vision/datom.md."
- **Date:** 2026-08-11
- **Provenance:** typed
- **Entries (3 entries):**
  - Parentheses must not be unused in Datom ("They are a major symbol of cognition")
  - Parentheses delimit the structured string; one string type, two variants
  - Map payload is a vector: `Map.[key.val …]` (superseded by guillemets)
- **Standing:** Archived. Distilled into Vision/datom.md.

### 01a02a34 — archive-datum — "Dotos is being replaced by datum"; "use datom instead of dotos"

- **Flow:** 01a02a34
- **File topic:** datum (archived)
- **Archive note:** "Archived 2026-08-23 by flow 68512643; distilled into Vision/datom.md."
- **Date:** 2026-08-22
- **Provenance:** typed
- **Verbatim:**

> And you're saying dotos, but like that's the old syntax, which is being replaced by datum, which is, you know, has the same concept.

> And use datom instead of dotos.

- **Standing:** Archived. Distilled into Vision/datom.md Repository.

### 01a02a34 — archive-schemaSyntax — "we need a schema syntax"

- **Flow:** 01a02a34
- **File topic:** schemaSyntax (archived)
- **Archive note:** "Archived 2026-08-23 by flow 68512643; distilled into Vision/ethos.md."
- **Date:** 2026-08-22
- **Provenance:** typed
- **Verbatim:**

> So this is what I mean. We need a schema syntax to show, to train agents to be able to properly use things and to also show us where our design is lacking.

- **Standing:** Archived. Distilled into Vision/ethos.md Self-description ("The schema syntax serves two audiences").

### c6b71b4c — archive-threeStacks — names confirmed; what the name must echo; "what about datom"

- **Flow:** c6b71b4c (in vision-raw archive as well)
- **File topic:** threeStacks (archived)
- **Archive note:** "Archived 2026-08-23 by flow 68512643; distilled into Vision/datom.md."
- **Date:** 2026-08-10
- **Provenance:** typed
- **Verbatim:**

> obviously protos

> obviously NOTA

> people wont remember dotos, eidos or rhetos. it just wont stick at all

> its data, strictly typed, super dense (no field names). something that echoes this

> what about datom

> ok we'll use datom, and we'll get you started with a fresh session to look at how we spilt those 3 stacks so make yourself a restart prompt

- **Standing:** Archived. Distilled into Vision/datom.md Name.

### vision-raw — archive-threeStacks — the shortcut; everything migrates to datom

- **Flow:** vision-raw (originally from c6b71b4c / 012fbf07)
- **File topic:** threeStacks (archived)
- **Archive note:** "Archived 2026-08-23 by flow 68512643; distilled into Vision/datom.md and Vision/ethosMonolith.md."
- **Date:** 2026-08-10, 2026-08-11
- **Provenance:** STT (dictated)
- **Verbatim (datom-relevant excerpts):**

> So, yeah, I still really much want the new ethos and datum [Datom] languages ... And datum [Datom] is basically just like a different syntax than nota ... it's just a serialization and deserialization logic.

> we don't need to worry about the old repo. We're just going to move forward and migrate everything to datum [Datom].

- **Standing:** Archived. Distilled into Vision/datom.md Repository and Nature.

### vision-raw — archive-ethosDotosDivisionAndHelp — "the two main syntaxes"

- **Flow:** vision-raw (origin unknown, pre-flow)
- **File topic:** ethosDotosDivisionAndHelp (archived)
- **Archive note:** "Archived 2026-08-23 by flow 68512643; distilled into Vision/ethos.md."
- **Date:** 2026-08-02
- **Provenance:** "psyche-verbatim, condensed" (source labels it thus)
- **Verbatim:**

> the two main syntaxes most agents will face; one specifies the types, the other fills them with data — hence why the basic 'cli help' for their dotos objects is meant to emit the ethos syntax that describes their anatomy.

- **Standing:** Archived. Distilled into Vision/ethos.md ("Of the two main syntaxes most agents will face, Ethos specifies the types and Datom fills them with data.").

### bc05da32 — archive-interfaceRootEnumerators — datom creates configuration options by its very shape

- **Flow:** bc05da32
- **File topic:** interfaceRootEnumerators (archived)
- **Archive note:** "Archived 2026-08-23 by flow 68512643; distilled into Vision/datom.md."
- **Date:** 2026-08-22
- **Provenance:** typed
- **Verbatim:**

> and I dont think we need a derive on a datom type for what we want. its simpler than that; datom creates configuration options by its very shape, as the ethos interface shows; a data enum at the root (main operation) with options in its data

- **Standing:** Archived. Distilled into Vision/datom.md "The interface shape".

### d63804f2 — archive-interfaceRootEnumerators — "That's what enumerators are"

- **Flow:** d63804f2
- **File topic:** interfaceRootEnumerators (archived)
- **Archive note:** "Archived 2026-08-23 by flow 68512643; distilled into Vision/datom.md."
- **Date:** 2026-08-07T18:47:12.105Z
- **Provenance:** STT (dictated)
- **Verbatim:**

> The main objects that I've been emphasizing, because we're talking about creating an interface, is the root input objects and perhaps even a lot of the root output objects should be enumerators because if you're trying to create a language, an input and output language, you want to create like branches. That's what enumerators are.

- **Standing:** Archived. Distilled into Vision/datom.md "The interface shape".

### a5587095 — structuredStringType — the Meaning type history

- **Flow:** a5587095
- **File topic:** structuredStringType
- **Date:** 2026-08-11 to 2026-08-12
- **Provenance:** typed
- **Entries (7 entries):**
  - The idea: "a revolutionary type; a structured string type"
  - One type, two variants; parentheses; research directed
  - The Meaning delimiter; context-switching parse
  - The ambition: "the most advanced structured meaning system ever made"
  - Annotations as enums through the tree
  - Meaning lives in datom; seen by both languages
  - A string expects a string; MeaningOrString
- **Standing:** The cross-reference annotation (2026-08-14) notes downstream rulings in datomSyntax.md govern it. Partially archived and distilled into Vision/datom.md Meaning. The detailed anatomy (enums through the tree, MeaningOrString, arbitrary depth graph) remains undistilled.

---

## Notion

### 62022e8f — layerMatching — matching structure to concept; the data lives in the capabilities

- **Flow:** 62022e8f
- **File topic:** layerMatching (notion)
- **Heading:** Multiple entries
- **Date:** undated in the file (session 62022e8f)
- **Provenance:** STT
- **Verbatim (datom-relevant excerpt):**

> This is where we are, I mean, a kind. So this is why we need such a specific dialect, which is why I'm kind of saying embodiments instead of types. ... this is the conceptual layer is where most of our thinking sort of happens conceptually, right? Because this is where we think in terms of datom [STT: datum] and ethos. ... a datom [STT: datum] struct or an ethos kind declaration would be a concept

- **Standing:** Notion. Not for building upon. The psyche explicitly marked it: "this is sort of a notion that we need to crystallize before it really becomes a vision."

---

## Typed transcript words found in no log

The ac1e9ec8 flow (reports/datomSyntaxTranscripts.md) conducted a comprehensive transcript audit covering all 99 Claude Code transcripts and 1530 Codex transcripts. The following are the UNRECORDED items that audit identified, which carry substantive datom-related content. Each is quoted from that report with its transcript reference.

### 236af273:101 [2026-08-03T13:44:31.366Z]

> the *text* is the payload. structural parsing means we can represent a payload any way we want.
>
> You mean for *potential* uses of this?
>
> ```dotos
> ExpectedObject.{ Stream ;; name
>                  SingleDottedPrefix.TypeName ;; Variant and its payload
>                  PossiblyOtherMetadata
>                }
> ```

- **Transcript:** `/home/li/.claude/projects/-home-li-primary/236af273-a771-43bc-bfa5-aa252d20fb3b.jsonl`, line 101
- **Date:** 2026-08-03

### 6b31eff3:80 [2026-08-04T08:47:11.293Z]

> so its the same as {| |} ?
>
> Then it's Name.{ which is much better visually

- **Transcript:** `/home/li/.claude/projects/-home-li-primary/6b31eff3-6477-4ee4-baed-cb491ebadd48.jsonl`, line 80
- **Date:** 2026-08-04

### 6b31eff3:158 [2026-08-04T09:42:51.469Z]

> and I want the Result<Vector<Sortable> Error> syntax for generics, since its more token efficient than using a dot, and recycles rust cognition

- **Transcript:** same file, line 158
- **Date:** 2026-08-04

### 6b31eff3:419-423 [2026-08-04T12:41-44Z]

> ```ethos
> Sorted.{Vector<Ordered>}              ;; struct Sorted<Ordered: Ord>(Vec<Ordered>)
> ```
>
> I want to create a translation table in logos' rust textualform emission for correctNaming <-> incorrectNaming, like Ordered and Ord, so we can have legible ethos/nomos/logos

- **Transcript:** same file, lines 419-423
- **Date:** 2026-08-04

### 6b31eff3:264 [2026-08-04T10:40:06.467Z]

> obviously. youre demonstrating that LLMs arent really intelligent yet by asking. One syntax necessarily replaces another

(On whether `|` retires from the grammar.)

- **Transcript:** same file, line 264
- **Date:** 2026-08-04

### 6b31eff3:677 [2026-08-04T19:52:28.102Z]

> yes, cut it. and you can keep the co-reference syntax.
>
> << >> should be kept for the next special syntax need we might encounter. it is the only good delimiter pair left for extending the language

- **Transcript:** same file, line 677
- **Date:** 2026-08-04

### 6b31eff3:725 [2026-08-04T19:55:08.151Z]

> I never said we need to call strings text

- **Transcript:** same file, line 725
- **Date:** 2026-08-04

### 6b31eff3:741 [2026-08-04T20:00:33.168Z]

> String is correct; remove the table entry

- **Transcript:** same file, line 741
- **Date:** 2026-08-04

### d63804f2:129 [2026-08-07T18:33:22.940Z]

> I also dont like the version number. which makes me wonder; how do we represent floating integer, represent in decimal (0.1)? Technically, if the expected position is a float, then it should be aple to read Interface.0.1.0 right?

- **Transcript:** `/home/li/.claude/projects/-home-li-primary/d63804f2-5a05-4e60-9448-94c95c3803d6.jsonl`, line 129
- **Date:** 2026-08-07

### 236af273:140 [2026-08-03T17:39:34.663Z]

> thanks for reminding me why agents are not going to design my syntax.
>
> The prefix should universally be the name. then something differentiates what comes after [...]
>
> ```ethos
> ;; Regular struct
> X.{ ... }
> ;; Regular enum
> Y.[ ... ]
> ```

- **Transcript:** `/home/li/.claude/projects/-home-li-primary/236af273-a771-43bc-bfa5-aa252d20fb3b.jsonl`, line 140
- **Date:** 2026-08-03

### 012fbf07:218 [2026-08-11T11:23:59.524Z]

> so you created a new repo for datom. were you planning to reuse the dotos code? do you know how I want the datom de/serializer to work?

- **Transcript:** `/home/li/.claude/projects/-home-li-primary/012fbf07-6c4a-4f7a-9474-137aa967e582.jsonl`, line 218
- **Date:** 2026-08-11

### 06196cc7:672 [2026-08-13T12:03:44.075Z]

> no, I said data, not functions

- **Transcript:** `/home/li/.claude/projects/-home-li-primary/06196cc7-0e13-4c16-9beb-509da55a2bb3.jsonl`, line 672
- **Date:** 2026-08-13

### 06196cc7:361 [2026-08-13T23:04:42.944Z]

> I dont understand. where does Group.Group.{ come from?
> There should be a string with inner balanced parentheses

- **Transcript:** same file, line 361
- **Date:** 2026-08-13

---

## Oddities and tensions

1. **"like JSON" in the distilled text.** Vision/datom.md Nature says "like JSON, but strictly typed." The psyche explicitly rejected this in ac1e9ec8 corrections: "Let's keep this noise out. Totally unecessary." The phrase remains in the distilled text. This is a same-flow conflict: the correction was given on the same proposal that produced the distilled wording.

2. **Direction-asymmetry approved for distilled vision but not landed.** The psyche in 04db2fd2 said "exactly. this can go straight into distilled vision" about the in/out asymmetry (Prospective vs Datom; Realize faults, Textualize does not; spans found inbound, computed outbound). This has not landed in Vision/datom.md.

3. **Datom Integer syntax undistilled.** The 01a03eda approval of canonical bare decimal (`0`, `42`, `-42`) is not in Vision/datom.md.

4. **Comment marker undistilled.** The e8c4cc61 ruling (single semicolon for comments) is not in Vision/datom.md.

5. **Space-inside-delimiter style undistilled.** Both e8c4cc61 (bracket space style) and 62022e8f (braces canonical too; never inside curly quotes) are not in Vision/datom.md.

6. **Datomizable not in Vision/datom.md.** The kind was raised from Notion to Vision by the psyche ("let's just make it a vision. Spare no ambition.") but has not been distilled.

7. **Datom-nexus future undistilled.** The 04db2fd2 musing about datom eventually becoming a nexus for format translation is not in Vision/datom.md.

8. **"datom is not preceded by a Datom root" undistilled.** The 995a164e ruling is not in Vision/datom.md.

---

## Sources

### What was read

1. Vision/datom.md — distilled vision (current authority)
2. Vision/sources/datom.md — sources file for datom distillation
3. Intent/data.md — distilled intent on data
4. Intent/protosParsing.md — distilled intent on protos parsing
5. Vision/ethos.md — distilled vision on ethos (for relation-to-datom sections)
6. vision-raw/archive-datomSyntax.md — archived datom syntax (from 012fbf07)
7. vision-raw/archive-threeStacks.md — archived three stacks (from c6b71b4c, 012fbf07)
8. vision-raw/archive-ethosDotosDivisionAndHelp.md — archived ethos/dotos division
9. vision-raw/structuredStringType.md — structured string type annotation
10. flows/01a02a34/vision/archive-datum.md — archived datum (from 01a02a34)
11. flows/01a02a34/vision/archive-schemaSyntax.md — archived schema syntax
12. flows/01a03d6e/vision/dotosFiles.md — dotos files ruling
13. flows/01a03d6e/vision/ethosInterfaces.md — ethos interfaces (nota/dotos correction)
14. flows/01a03eda/vision/datomSyntax.md — default string delimiter
15. flows/01a03eda/vision/datomInteger.md — integer syntax approval
16. flows/01a035d3/vision/rustCodeFromTheData.md — port to datom directive
17. flows/01a038b5/vision/curriculumStackToDatomInsteadOfDotos.md — migration directive
18. flows/01a04339/vision/datom.md — Observed.Locks.[] reply shape
19. flows/04db2fd2/vision/datomMaps.md — guillemets for maps
20. flows/04db2fd2/vision/datomNexus.md — datom as nexus
21. flows/04db2fd2/vision/delimiters.md — delimiter terminology
22. flows/04db2fd2/vision/text.md — Text type
23. flows/04db2fd2/vision/textualTypes.md — Prospective<Datom>, Datomic
24. flows/04db2fd2/vision/decomposable.md — decomposable kind
25. flows/04db2fd2/vision/directionAsymmetry.md — direction asymmetry
26. flows/04db2fd2/vision/delineate.md — Prospective<Datom> is Delineatable
27. flows/04db2fd2/vision/kinds.md — kinds as qualifiers
28. flows/04db2fd2/vision/portion.md — portion as universal term
29. flows/06196cc7/vision/archive-datomSyntax.md — archived datom syntax (from 06196cc7)
30. flows/4d5fc7da/vision/datom.md — omittable fields
31. flows/5abf3be8/vision/dotOpensDelimiterEverythingIsData.md — dot opens delimiter
32. flows/5abf3be8/vision/colonLegalInStringPosition.md — colon legal in string
33. flows/62022e8f/vision/datomSyntax.md — spaces inside delimiters
34. flows/62022e8f/vision/headedAndContained.md — headed and contained forms
35. flows/62022e8f/vision/concept.md — concept layer and datom
36. flows/62022e8f/vision/symbols.md — capitalized vs non-capitalized symbols
37. flows/62022e8f/notion/layerMatching.md — notion on matching structure to concept
38. flows/68512643/vision/negatives.md — negatives ruling
39. flows/68512643/witnesses/datomVisionGround.md — vision ground witness
40. flows/995a164e/vision/datomSyntax.md — datom not preceded by root
41. flows/995a164e/vision/data.md — everything is data
42. flows/995a164e/vision/concept.md — concept-layer shapes
43. flows/a5587095/vision/archive-datomSyntax.md — archived datom syntax
44. flows/a5587095/vision/structuredStringType.md — Meaning type history
45. flows/a5587095/vision/protosIsTheSharedStyle.md — protos shared style
46. flows/ac1e9ec8/vision/datomIsData.md — datom is data
47. flows/ac1e9ec8/vision/datomSkill.md — datom skill (title-only)
48. flows/ac1e9ec8/vision/datomSyntax.md — syntax corrections and rulings
49. flows/ac1e9ec8/vision/archive-distillationNegatives.md — archived negatives
50. flows/ac1e9ec8/reports/datomSyntaxTranscripts.md — transcript audit
51. flows/ac1e9ec8/reports/datomSyntaxWrittenPsyche.md — written psyche acquisition
52. flows/b675f3d9/vision/structuralParsing.md — structural parsing
53. flows/b675f3d9/reports/distillCandidatesProtosDatom.md — distill candidates
54. flows/b675f3d9/reports/distillProposalProtosDatom.md — distill proposal
55. flows/acbb6006/reports/distillProposalProtosDatomAddendum.md — addendum proposal
56. flows/bc05da32/vision/archive-interfaceRootEnumerators.md — archived interface enumerators
57. flows/bc05da32/vision/mainFunction.md — main function (datom input)
58. flows/d63804f2/vision/archive-interfaceRootEnumerators.md — archived interface enumerators
59. flows/e8c4cc61/vision/datomSyntax.md — semicolon and space style
60. flows/e8c4cc61/vision/datomizable.md — Datomizable kind
61. flows/e8c4cc61/vision/protos.md — Structure replaces Portion
62. flows/e8c4cc61/vision/designExamples.md — design examples
63. flows/e8c4cc61/vision/psycheLayers.md — notion layer established
64. flows/04db2fd2/reports/protosDatomPsyche.md — prior psyche catalogue
65. flows/68512643/reports/datomEthosMonolithDistillation.md — prior distillation proposal
66. flows/ac1e9ec8/reports/datomVisionProposal.md — prior vision proposal
67. flows/db97561c/reports/mapSyntaxCorrection.md — map syntax correction (datomVisionFix)
68. flows/01a02fd5/vision/interfaces.md — interfaces in ethos
69. vision-raw/mainFunction.md — main function (datom input at boundary)
70. flows/62022e8f/vision/ethosTypes.md — map type declared with guillemets
71. flows/995a164e/vision/ethosTypes.md — contained kind declaration is ethos not datom
72. flows/e8c4cc61/vision/ethosFileAnatomy.md — ethos file anatomy
73. flows/995a164e/vision/explodedForm.md — exploded form naming

### What was written

1. /home/li/primary/flows/4decf7/reports/datom.md — this report
