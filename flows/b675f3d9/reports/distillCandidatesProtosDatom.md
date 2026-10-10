# Distillation Candidates: PROTOS and DATOM

Candidate records for distilling together, grouped by sub-topic.
Each record: id, date, kind, verbatim psyche words (or excerpt), source, status against Vision/datom.md and Vision/ethos.md.

Session-count note: where a session has a dedicated vision file per record, the count follows file order within that session. Where multiple records share one file, they are numbered in chronological order. Counts from the datomSyntaxTranscripts.md audit (ac1e9ec8) use transcript line as tiebreaker.

---

## Sub-topic: PROTOS — what it is

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 1 | a5587095/5 | 2026-08-11 | typed | "protos is the name we give to the style which all our dialects share; hence why the final fully-decomposed engine with 3 daemons is the protos engine, with datom sort of sitting besides it, as it is only for pure, typed data" | flows/a5587095/vision/protosIsTheSharedStyle.md §1 | REFLECTED — Vision/datom.md §Relation to Ethos ("Datom and Ethos are different languages that share an approach") carries part; the protos-engine and protos-as-shared-style are NOT in Vision/datom.md or Vision/ethos.md |
| 2 | ba906ae2/1 | 2026-08-14 | typed | "it *is* a protos dialect, but not part of the future ethos/nomos/logos rust-generation engine" | flows/ba906ae2/vision/protosIsTheSharedStyle.md | REFLECTED — Vision/datom.md §Nature ("Datom — the data dialect of the Protos family") |
| 3 | 6863ef19/2 | 2026-08-13 | typed | "Any type will only have one protos representation. so the datom:: version isnt necessary. look for flaws in my logic. It could even have a constant variant to give the protos dialect it is transcodable into" | flows/6863ef19/vision/traitsAsCapabilities.md §2 | NEW — one-representation-per-type principle not in any Vision/ file. (SUPERSEDED-BY 6863ef19/3 on "transcodable" vocabulary, but the one-representation principle stands) |
| 4 | 6863ef19/1 | 2026-08-13 | typed | "all traits will be qualifiers. I disagree with rust's convention (Write Read should be Writable and Readable). [...] reconsider traits as 'capabilities'" | flows/6863ef19/vision/traitsAsCapabilities.md §1 | NEW — not in Vision/datom.md or Vision/ethos.md (SUPERSEDED-BY 06196cc7/4 which accepts verbs, and b675f3d9-kinds/1 which settles qualifier + kind) |

## Sub-topic: PROTOS — context-dependent parsing

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 5 | a5587095/6 | 2026-08-11 | typed | "there is always a parsing context. it doesnt suspend, it *changes*, but the underlying mechanism is always the same; Now, we are parsing in context X and can therefore expect A, B or C shapes of things, and Z would end that context, but meeting A would switch to the context which A entails. That has been the ruling principle of NOTA (datoms's ancestor) from day one." | flows/a5587095/vision/protosIsTheSharedStyle.md §2 | REFLECTED — Intent/protosParsing.md carries the distilled Intent. Not in Vision/datom.md explicitly |
| 6 | b675f3d9/2 | 2026-08-27 | dictated | "ethos parsing is always dependent on the current context in which the parsing is taking place. So in the import block, colon are treated in a certain way [...] And then the same colon used in another block could be used to, obviously, to mean something else since another block would not involve imports." | flows/b675f3d9/vision/structuralParsing.md §2 | NEW — context-dependent character meaning not in Vision/datom.md (extends the Intent with a concrete example of delimiter reuse across blocks) |

## Sub-topic: PROTOS — structural discrimination by delimiter and arity

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 7 | b675f3d9/1 | 2026-08-27 | dictated + handwritten | (excerpt) "the structural parsing can actually discern between structs of different size to differentiate between different types [...] using different delimiters between the head and the delimiter to add even more type differentiation using very minimal character slash token cost" | flows/b675f3d9/vision/structuralParsing.md §1 | NEW |
| 8 | b675f3d9/1h | 2026-08-27 | handwritten | (excerpt) "Capability.[ SingleYield.{Name Concept} ;; Represented as 'Head.Concept' ;; A Concept being a type or a Kind" | flows/b675f3d9/vision/structuralParsing.md §1 handwritten page | NEW — "Concept = a type or a Kind" |
| 9 | b675f3d9/3 | 2026-08-27 | dictated | "It's perfectly acceptable to have different structures [...] We use the same mechanism in the [...] ethos signal interfaces and others to differentiate between things like an enum and a struck [struct] by [...] checking the delimiter after the head." | flows/b675f3d9/vision/kinds.md §"Different structures may be different types" | REFLECTED partially — Vision/datom.md §Syntax mentions Head; the general discrimination mechanism is NOT in Vision/ |
| 10 | b675f3d9/4 | 2026-08-27 | typed | "yes variable length is [] and all components must share a type or kind" | flows/b675f3d9/vision/kinds.md §"Variable length is []" | NEW — vector semantics not stated in Vision/datom.md |
| 11 | b675f3d9/5 | 2026-08-27 | typed | "a struct {} always has the same fields, in the same order. the struct definition declares the field types, so they can be anything; there are no restriction in which type a field can hold!" | flows/b675f3d9/vision/kinds.md §"A struct always has the same fields" | NEW — struct semantics not stated this explicitly in Vision/datom.md |
| 12 | b675f3d9/1b | 2026-08-27 | dictated | "<> is a real Protos delimiter of course. I'm surprised you have to ask" | flows/b675f3d9/vision/structuralParsing.md §1 | NEW — angle brackets as a Protos delimiter |
| 13 | a5587095/8 | 2026-08-12 | typed | "the more complex trait will be a vector of ProtosShape's (welcome to propose other names), when the structure dictates the outer type, for example in ethos when X.{ means a struct, and Y.[ means an enum, and Z:Transform.[/{ means different kinds of transformers" | flows/a5587095/vision/protosIsTheSharedStyle.md §4 | NEW — ProtosShape vector concept not in Vision/ |

## Sub-topic: <> syntax — generics/kinds, "recycles Rust cognition"

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 14 | 6b31eff3/2 | 2026-08-04 | typed | "and I want the Result<Vector<Sortable> Error> syntax for generics, since its more token efficient than using a dot, and recycles rust cognition" | ac1e9ec8 reports/datomSyntaxTranscripts.md 6b31eff3:158, transcript | NEW — UNRECORDED in any vision file |
| 15 | 6b31eff3/3 | 2026-08-04 | typed | (excerpt) "Sorted.{Vector<Ordered>} ;; struct Sorted<Ordered: Ord>(Vec<Ordered>) [...] I want to create a translation table in logos' rust textualform emission for correctNaming <-> incorrectNaming, like Ordered and Ord, so we can have legible ethos/nomos/logos" | ac1e9ec8 reports/datomSyntaxTranscripts.md 6b31eff3:419-423, transcript | NEW — UNRECORDED |
| 16 | no-id | 2026-08-01 | typed | "the answer is the mandatory trait! so T would be a trait! and multiple trait in the declaration would just adjust the emitted rust - remember for us rust is assembly" | psyche-raw/Vision/genericParametersAreTraits.md | REFLECTED — Vision/ethos.md does not carry this explicitly; ethosAnatomyVision.md §1 lists it. The <> connection is not in Vision/ |
| 17 | b675f3d9/6 | 2026-08-26 | typed | "in Ethos there are no generics, only kinds" | flows/b675f3d9/vision/kinds.md §1 | NEW |
| 18 | b675f3d9/7 | 2026-08-26 | typed | (excerpt) "Processable<[Clonable Sendable] Serializable>" (preferred identity head syntax) | flows/b675f3d9/vision/kinds.md §"Identity head preferred" | NEW |

## Sub-topic: DATOM — nature and name

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 19 | 012fbf07/1 | 2026-08-11 | typed | "datom doesnt do generics, it only carries data, like json (but strictly typed of course)" | psyche-raw/Vision/archive-datomSyntax.md §1 | REFLECTED — Vision/datom.md §Nature |
| 20 | ac1e9ec8/1 | 2026-08-26 | typed | "you've mixed up datom with ethos. datom is data" | flows/ac1e9ec8/vision/datomIsData.md | REFLECTED — Vision/datom.md §Nature |
| 21 | ac1e9ec8/6 | 2026-08-26 | typed | "Datom is the most advanced textual data format in the world." | flows/ac1e9ec8/vision/datomSyntax.md §corrections | NEW — not in Vision/datom.md |
| 22 | ac1e9ec8/9 | 2026-08-26 | typed | "all our components speak signal, not datom; datom is only used at the edge to let text-based systems (LLMs and all existing editors) understand signal." | flows/ac1e9ec8/vision/datomSyntax.md §"curly quotes are the string delimiter" | NEW — SUPERSEDES Vision/datom.md if it implies datom is the wire format |
| 23 | 68512643/2 | 2026-08-24 | typed | "chosen for it's energetic power [...] schema is the abandoned ancestor of ethos, not datom" | ac1e9ec8 reports/datomSyntaxTranscripts.md 68512643:660 | REFLECTED — Vision/datom.md §Name, §Repository |
| 24 | 01a02a34/1 | 2026-08-22 | dictated | "you're saying dotos, but like that's the old syntax, which is being replaced by datum, which is, you know, has the same concept." | flows/01a02a34/vision/archive-datum.md | REFLECTED — Vision/datom.md §Repository |

## Sub-topic: DATOM — de/serialization, positional

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 25 | 012fbf07/2 | 2026-08-11 | typed | "yes, direct to typed structs. [...] no self-describing tags" | ac1e9ec8 reports/datomSyntaxTranscripts.md 012fbf07:240 | REFLECTED — Vision/datom.md §De/serialization |
| 26 | ac1e9ec8/7 | 2026-08-26 | typed | "a string is a string only in a position where the type defines a string." | flows/ac1e9ec8/vision/datomSyntax.md §corrections (on bare strings) | NEW — positional string typing not explicitly stated in Vision/datom.md |

## Sub-topic: DATOM syntax — Head, `.` delimiter

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 27 | 06196cc7/2 | 2026-08-14 | typed | "the dotted prefix of a delimiter must be part of its type. it could be a universal type, and unprefixed blocks simply have no prefix." | flows/06196cc7/vision/archive-datomSyntax.md §"dotted prefix" | REFLECTED — Vision/datom.md §Syntax ("The dotted prefix of a delimited block is part of the block's type; its official name is Head") |
| 28 | 06196cc7/3 | 2026-08-14 | typed | "I like the Head terminology actually. lets make it official" | flows/06196cc7/vision/archive-datomSyntax.md §"Head is the official term" | REFLECTED — Vision/datom.md §Syntax |
| 29 | 06196cc7/4b | 2026-08-14 | typed | "Like in ethos, when we are defining types, X.{} is a struct called X, and textualizing that type back will re-emit X.{} which must be understood in the right context if printed alone, or inserted in the right position, if the whole source is textualized" | flows/06196cc7/vision/archive-datomSyntax.md §"variants always re-emit" | REFLECTED — Vision/datom.md §Syntax ("a variant always re-emits its Head when textualized") |
| 30 | 5abf3be8/1 | 2026-08-06 | typed/dictated | "it opens a delimiter. everything is data" | flows/5abf3be8/vision/dotOpensDelimiterEverythingIsData.md | NEW — "everything is data" not in Vision/datom.md |

## Sub-topic: DATOM syntax — struct `{}`, enum `[]`, vector `[]`

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 31 | 236af273/1 | 2026-08-03 | typed | (excerpt) "The prefix should universally be the name. then something differentiates what comes after [...] X.{ ... } ;; Regular struct / Y.[ ... ] ;; Regular enum" | ac1e9ec8 reports/datomSyntaxTranscripts.md 236af273:140 | REFLECTED — Vision/datom.md §Syntax (implied), but the original explanation is not in Vision/ |
| 32 | 06196cc7/5 | 2026-08-14 | typed | "we have clearly enunciated what those are. the first is a struct, the second is (now) a string-carrying variant." (on {…} and X.(…)) | flows/06196cc7/vision/archive-datomSyntax.md §"bare {…} is a struct" | REFLECTED — Vision/datom.md §Syntax |

## Sub-topic: DATOM syntax — parentheses, strings, Meaning

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 33 | a5587095/3 | 2026-08-11 | typed | "It would be strange for parenthesis to be unused in datom. They are a major symbol of cognition." | flows/a5587095/vision/archive-datomSyntax.md §1 | REFLECTED — Vision/datom.md §Syntax ("Parentheses carry a duty — they are a major symbol of cognition") |
| 34 | 06196cc7/6 | 2026-08-14 | typed | "Ok now Im full backpedaling on the () for simple strings [...] parentheses are already used in text as a way to *markup* the text [...] go for balance-based, where an unbalanced parenthesis needs to be escaped." | flows/06196cc7/vision/archive-datomSyntax.md §"paren strings are balance-based" | REFLECTED — Vision/datom.md §Syntax |
| 35 | ac1e9ec8/8 | 2026-08-26 | typed | "not legacy. In fact I think they should be positioned as the default string delimiter. the vision is that parenthesis will become the delimiter for structured strings, still to be designed. So let's switch it all to curly quotes first, with parenthesis reserved for structured strings, which we currently designate as Meaning" | flows/ac1e9ec8/vision/datomSyntax.md §"curly quotes are the string delimiter" | SUPERSEDES Vision/datom.md §Syntax which says parentheses are the default string delimiter. Curly quotes are now default; parentheses reserved for Meaning. |
| 36 | 06196cc7/7 | 2026-08-14 | typed | "A string that doesnt need quotes *must not* be quoted" | flows/06196cc7/vision/archive-datomSyntax.md §"a string that doesn't need quotes" | REFLECTED — Vision/datom.md §Syntax ("A string is written bare whenever the bare form can carry it") |
| 37 | 06196cc7/8 | 2026-08-14 | typed | "If its a string, then it can use symbols which would be load bearing in other situations [...] lets make the machinery fit for this, bullet proof not by lots of complex code, but by the right abstraction layers." | flows/06196cc7/vision/archive-datomSyntax.md §"bare strings may carry load-bearing symbols" | REFLECTED — Vision/datom.md §Syntax |
| 38 | ac1e9ec8/10 | 2026-08-26 | typed | "<> is used in ethos, and those two must remain compatible in case datom is ever eventually embedded into some ethos positions." | flows/ac1e9ec8/vision/datomSyntax.md §corrections (on glyph question) | NEW — datom-ethos embedding compatibility not in Vision/ |

## Sub-topic: DATOM syntax — map

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 39 | a5587095/4 | 2026-08-11 | typed | "Yes, map would use .[ since a map is conceptually a list of key/values" | flows/a5587095/vision/archive-datomSyntax.md §"map payload" | REFLECTED — Vision/datom.md §Syntax |
| 40 | ac1e9ec8/2 | 2026-08-26 | typed | "If a position expects a map, the data will be [ k.v ... ], no Map." | flows/ac1e9ec8/vision/datomSyntax.md §1 | NEW — headless map in expected position not in Vision/ |
| 41 | ac1e9ec8/3 | 2026-08-26 | typed | "Im considering making key/values resolve by position in a map [...] that looks cleaner and makes the Head. always a variant; lower cognitive cost" | flows/ac1e9ec8/vision/datomSyntax.md §2 | NEW — under consideration, not ruled |
| 42 | ac1e9ec8/4 | 2026-08-26 | typed | "let use the guillemets." | flows/ac1e9ec8/vision/datomSyntax.md §"guillemets delimit a map" | NEW — SUPERSEDES Vision/datom.md §Syntax map-as-square-bracket ruling |
| 43 | ac1e9ec8/5 | 2026-08-26 | typed | "Is there a scenario in which a Head. isnt a variant?" | flows/ac1e9ec8/vision/datomSyntax.md §1 (question, not ruling) | NEW |

## Sub-topic: DATOM syntax — colon, imports, transformers (superseded `.()`)

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 44 | 5abf3be8/2 | 2026-08-06 | typed | "I think Name:TransformerName.( ... ) is the better syntax for named transformers." | psyche-raw/Vision/colonFormTransformerSyntax.md | REFLECTED — Vision/datom.md §Syntax mentions "dot-parenthesis block is a string-carrying variant." The colon-form origin is not in Vision/ |
| 45 | 5abf3be8/3 | 2026-08-06 | typed | "and : remains legal in a position expecting a string" | flows/5abf3be8/vision/colonLegalInStringPosition.md | NEW |
| 46 | d63804f2/1 | 2026-08-07 | typed | "the fixture is blessed, and / for imports" (supersedes colon-in-import; colon keeps exactly one meaning) | psyche-raw/Vision/colonConfusion.md | NEW — `/` as import separator not in Vision/datom.md |
| 47 | a5587095/2 | 2026-08-11 | typed | "I think we are wrongly using parenthesis in ethos now, since we introduced X:Transformer syntax [...] .[ is better [...] .{ is the right delimiter" | flows/a5587095/vision/colonFormTransformerSyntax.md | NEW — transformer payloads to .[ and .{ not in Vision/datom.md |

## Sub-topic: DATOM syntax — sections confer traits

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 48 | 5abf3be8/4 | 2026-08-06 | typed | "What other point is there to have different sections?" | flows/5abf3be8/vision/sectionsExistToConferTraits.md | NEW — sections conferring traits not in Vision/datom.md |

## Sub-topic: Working form / signal form; Realize / Textualize

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 49 | 5abf3be8/5 | 2026-08-06 | dictated | "The encoded form is the code. So the encoded form of ethos is ethos. The textual form is there so that our editors [...] can actually make sense of it." | psyche-raw/Vision/encodedFormIsTheCode.md §1 | SUPERSEDED-BY 06196cc7/1 |
| 50 | 06196cc7/1 | 2026-08-13 | typed | "ok, working form and signal form, drop code/encoded entirely" | psyche-raw/Vision/encodedFormIsTheCode.md §2 | REFLECTED — Vision/datom.md §De/serialization carries part. SUPERSEDED-BY 06196cc7/1b on "working" |
| 51 | 06196cc7/1b | 2026-08-13 | typed | "I dont like working, it smells like a verb. Same with meaning" | flows/06196cc7/vision/encodedFormIsTheCode.md §1 | NEW — form name rejection not in Vision/ |
| 52 | 06196cc7/1c | 2026-08-14 | typed | "Ok with the real/Realize" | flows/06196cc7/vision/encodedFormIsTheCode.md §2 | NEW — "real form" and protos::Realize not in Vision/datom.md |
| 53 | 6863ef19/4 | 2026-08-13 | dictated | "the textual form of a thing is data. So, it's a type." | flows/6863ef19/vision/encodedFormIsTheCode.md | NEW |
| 54 | 06196cc7/4c | 2026-08-14 | typed | "Textualize is good [...] ShapeDefined is good" | flows/06196cc7/vision/traitsAsCapabilities.md §"Textualize confirmed" | NEW — protos::Textualize and ShapeDefined not in Vision/datom.md |

## Sub-topic: DATOM — the interface shape

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 55 | 68512643/3 | 2026-08-24 | typed | "output *is* an enum. always. even the most basic response interface must be an enum; Success/Failure." | ac1e9ec8 reports/datomSyntaxTranscripts.md 68512643:917 | REFLECTED — Vision/datom.md §The interface shape |

## Sub-topic: Self-description / help emits ethos

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 56 | no-id | 2026-08-02 | typed | "the basic 'cli help' for their dotos objects is meant to emit the ethos syntax that describes their anatomy." | psyche-raw/Vision/archive-ethosDotosDivisionAndHelp.md | REFLECTED — Vision/ethos.md §Self-description |

## Sub-topic: Non-repetition

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 57 | no-id | 2026-08-01 | typed | "any such repition in ethos syntax is an implementation failure. ethos will be the most terse non-repetitive syntax ever made" | psyche-raw/Vision/archive-ethosNonRepetitionLaw.md | REFLECTED — Vision/ethos.md §Non-repetition |

## Sub-topic: Protos parsing — the walk, ProtosShape, ShapeDefined

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 58 | a5587095/7 | 2026-08-11 | typed | (excerpt) "Intent would be quite general, about the way the parsing is approached. Lets flesh it out in detail with examples [...] the parse is two-way [...] that must become our design pattern." | flows/a5587095/vision/protosIsTheSharedStyle.md §3 | REFLECTED — Intent/protosParsing.md |
| 59 | a5587095/9 | 2026-08-12 | typed | (excerpt) "To me ProtosShape was a trait [...] implementing ProtosShape means creating a match on standard ProtosShape [...] each of which has its own parsing context implementation" | flows/a5587095/vision/protosIsTheSharedStyle.md §5 | NEW — ProtosShape trait design not in Vision/ |
| 60 | a5587095/10 | 2026-08-12 | typed | "because of recursion, the position of the parent context still needs to be kept [...] Big implementations are a sign of a missing logic plane. Everything should be simple individually. The complexity is in the totality, not the individual parts." | flows/a5587095/vision/protosIsTheSharedStyle.md §6 | NEW — logic-plane principle not in Vision/ |
| 61 | a5587095/11 | 2026-08-13 | typed | "the intent is good" (approving the Protos parsing Intent) | flows/a5587095/vision/protosIsTheSharedStyle.md §7 | REFLECTED — Intent/protosParsing.md |

## Sub-topic: DATOM — Integer syntax

| # | ID | Date | Kind | Psyche verbatim | Source | Status |
|---|-----|------|------|-----------------|--------|--------|
| 62 | 01a03eda/1 | 2026-08-26 | typed | "yes" (approving canonical bare decimal integer syntax: 0, 42, -42) | flows/01a03eda/vision/datomInteger.md | NEW — integer syntax not in Vision/datom.md |

---

## UNRECORDED transcript turns (no vision file at all)

From ac1e9ec8/reports/datomSyntaxTranscripts.md, the following 6b31eff3 (2026-08-04) turns have no vision record anywhere:

| ID | Line | First sentence |
|----|------|----------------|
| 6b31eff3:80 | 80 | "so its the same as {| |}?" (on bare <> as data delimiters) |
| 6b31eff3:158 | 158 | "and I want the Result<Vector<Sortable> Error> syntax for generics, since its more token efficient" |
| 6b31eff3:264 | 264 | "obviously. youre demonstrating that LLMs arent really intelligent yet by asking. One syntax necessarily replaces another" (pipe retirement) |
| 6b31eff3:419-423 | 419 | "Sorted.{Vector<Ordered>} [...] I want to create a translation table in logos' rust textualform emission" |
| 6b31eff3:666 | 666 | "why am I still seeing this?" (on superseded Observer.() form) |
| 6b31eff3:677 | 677 | "<< >> should be kept for the next special syntax need" |
| 6b31eff3:725 | 725 | "I never said we need to call strings text" |
| 6b31eff3:741 | 741 | "String is correct; remove the table entry" |

Other unrecorded transcript turns:

| ID | Line | First sentence |
|----|------|----------------|
| 236af273:101 | 101 | "the *text* is the payload. structural parsing means we can represent a payload any way we want." (with full ethos code example) |
| 236af273:140 | 140 | "thanks for reminding me why agents are not going to design my syntax." (origin of Name.{} / Name.[] convention) |
| 236af273:176 | 176 | "I also think we should use {\|\|} for non-trivial structs" (SUPERSEDED by pipe retirement) |
| 236af273:282-284 | 282 | "Bridge.{| {Left Sortable} {Right Sortable} |}" (SUPERSEDED by pipe retirement) |
| 06196cc7:361 | 361 | "where does Group.Group.{ come from? There should be a string with inner balanced parentheses" |
| 06196cc7:672 | 672 | "no, I said data, not functions" |
| a5587095:337 | 337 | "the more complex trait will be a vector of ProtosShape's" (partially recorded in protosIsTheSharedStyle.md §4) |
| a5587095:398 | 398 | "You mean BareSymbol?" / "What do we call X.[/{/(?" (partially recorded) |
| d63804f2:129 | 129 | "how do we represent floating integer, represent in decimal (0.1)?" |

---

## KEY SUPERSESSION CHAINS for distillation

1. **String delimiter**: parentheses default (06196cc7 2026-08-14) -> SUPERSEDED by curly quotes default (ac1e9ec8 2026-08-26, record 35). Vision/datom.md §Syntax still carries the superseded parentheses-default ruling.

2. **Map delimiter**: .[ square bracket (a5587095 2026-08-11) -> SUPERSEDED by guillemets (ac1e9ec8 2026-08-26, record 42). Vision/datom.md §Syntax still carries "A map's payload is a square-bracket vector."

3. **Datom scope**: Vision/datom.md implies datom is the universal data format. SUPERSEDED by "datom is only used at the edge" (ac1e9ec8 2026-08-26, record 22).

4. **Encoded/code vocabulary** -> "working form and signal form" -> "real form". Vision/datom.md carries "serialization and deserialization" but not the real/signal/textual vocabulary.

5. **Transcodable** -> dropped with code/encoded -> protos::Realize / protos::Textualize (06196cc7 2026-08-14).
