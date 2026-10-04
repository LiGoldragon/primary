# Distillation candidates: Ethos and datom; the nexus

Source: `flows/28d847/reports/fable-package-vision.md`, subjects 3 (section 3.1, quotes E1 to E36) and 4 (section 4.1, quotes N1 to N25). `E7` means quote 7 of section 3.1 and `N7` means quote 7 of section 4.1, numbered as in the package. Dates and source paths are the package's own. Tension tags `T13` to `T16` are the package's.

These are candidates gathered for the main flow. The psyche-distillation skill says a distillation is composed only in the main flow, and that each statement lands only when the living approves it. Nothing here has landed, and no raw record has moved to an archive.

Word counts cover only the living's quoted text: words on `>` lines, counted with whitespace splitting. Where a statement carries only some paragraphs of a quote, only those paragraphs are counted, and the rest is listed under "left out". Each quote is counted in one cluster only. Quotes that support another cluster are named there but not counted again.

Subjects 3 and 4 hold 5,952 quoted words: 3,260 in subject 3 and 2,692 in subject 4. Thirteen clusters replace 4,528 of them. The statements total 1,833 words; the exact count is at the end. 1,424 words stay verbatim and are listed at the end.

Where a statement contradicts a distilled Vision file, the conflict is flagged. These are not tensions in the package, and the living has not decided them.

---

## 1. A Nexus has three parts: signal, operation, memory

- Lands in: `Vision/nexus.md`
- Replaces 596 words: N3 paragraphs 1 to 4 (159), N4 (85), N5 (101), N6 (54), N11 (122), N17 (49), N18 (26)
- Supported by N1 and N13 (counted in cluster 5)

**Statement**

A Nexus has three parts, and each is its own ethos specification:

- Signal is how the Nexus talks.
- Operation is how it treats incoming signals and what memory returns.
- Memory is the kinds of things it keeps, as a database keeps them.

Every effect has a matching operation type. A signal reaches memory only through operation. The answer comes back through operation and leaves as a signal. A memory change returns as an operation that either succeeded or failed. A successful change ends with a signal reporting that the effect happened.

A Nexus's core types are exposed in its ethos. Its processes are typed objects too: starting a flow, locking a pane, sending a message, pasting the message into the pane. Reading the ethos alone shows which objects and processes are involved. This is the direction even where the code is not there yet.

Signal gives the main types, the requests and the replies. The central part is not called "nexus", because that word already means the daemon. The development of the anatomy across signal and operation gets a document of its own.

**Sources**
```
91ea9f ethos
26c50c ethos
fe34eb nexus
```

**Left out or in conflict**

- T15, what the parts are called:
  - 2026-09-10 (`flows/fe34eb/vision/nexus.md`): signal gives the main types and sema the database types.
  - 2026-10-02 (`flows/91ea9f/vision/ethos.md`): first signal, process and storage ("not a big fan of storage", and he asks for a better vocabulary for what is memorized). Later the same day: signal, operation and memory ("the memory is good").
  - 2026-10-04 (`flows/5ed94b/vision/nexusEntryPoint.md`): signal, the operation actor or system, and the memory actor or system.
  - The statement uses the 2026-10-04 words. The sema side remains.
- Conflicts with distilled state: `Vision/ethos.md` (Roots) names the roots Library, Signal and Sema, and `Vision/sema.md` names sema the database. Memory is not yet reconciled with sema.
- Discarded as impurity: N5 "let's distill the vision ... start putting out example syntaxes" and N6 "make a book with Astra" are instructions for that day. The rule they imply, that ethos is shown with every new object, is in cluster 9.
- Not carried as written: N11 says "maybe this is too advanced". The statement keeps it only as "the direction even where the code is not there yet".

---

## 2. A Nexus never handles text

- Lands in: `Vision/nexus.md` (it also confirms `Vision/signal.md` "Text and signal" and `Vision/ethos.md` "The datom kinds are compiled in only where text is spoken")
- Replaces 492 words: N8 paragraph 1 (73), N9 (57), N12 paragraph 2 (116), N15 (59), E31 (29), E24 (158)

**Statement**

A Nexus receives only signal and contains no datom logic. It decodes the known types it was compiled with, using rkyv and the protocol built on top of rkyv. Datom is the edge where text-based systems, meaning language models and every existing editor, read and write signal. The CLI translates datom into signal and back.

A type converts between datom text and a Rust value only where that conversion is compiled in. It is a compile-time option: the CLI has it, later the user interface will have it, and the Nexus never does. The reason is size. Nexuses keep running and there may be several, so each runtime stays as small as it can be.

A CLI's help is the type's own ethos, produced end to end. The object comes out of the Nexus's memory, is deserialized at the CLI and is written out in ethos syntax. The help is never a copy of the source string.

```rust
// the conversion compiled in only where text is spoken (form as in Vision/ethos.md)
#[cfg_attr(feature = "datom", derive(Datomizable, Compositional))]
pub enum Query { Lock(LockRequest), Release(LockId) }
```

**Sources**
```
8904b1 skills
26c50c ethos
05c604 nexus
ac1e9ec8 datomSyntax
752e0f helpMenu
```

**Left out or in conflict**

- Open question, not counted (N2, a notion, 2026-10-03): how does a Nexus send datom on to other places without knowing how to serialize and deserialize datom itself?
- Left out because it is undefined: E24 names "the body layer, the incorporated layer, and the rest value layer". These terms are defined nowhere, so the statement does not use them.
- Left out, stays verbatim: N8 paragraph 2 (71 words). The CLI's calling process tells the Nexus which flow sent the message, perhaps through Flow, "not by trusting that the flow put its ID in the message". This is a separate ruling with only one quote.
- T13: E31 (2026-08-26) is the "datom only at the edge" side of T13. See cluster 11.

---

## 3. A machine call is programmed with an ethos spec and corrected against it

- Lands in: `Vision/messaging.md`
- Replaces 446 words: E30 (197), N13 paragraphs 2 and 3 (249)

**Statement**

Datom is programmed into the system prompt of our machine calls, and everything the call says is specified.

A call receives four things:

- the ethos spec of what it is expected to say
- a few examples
- a prose explanation in Markdown
- the word that it now speaks this spec

From then on it answers in datom of the response types the spec gives. When it breaks protocol, it is told which part of the spec it broke.

Error messages are generated from the structure. Decoding the structure first gives "wrong structure" errors. The way protos are parsed and generated gives more specific ones.

Datom is what gets generated and decoded. Ethos is the spec. Ethos explains messages in errors and in training, and it is how new kinds of objects are discussed. Ethos therefore also travels as a payload inside datom. That needs its own specification, and how it is escaped is still open.

Comments are typed as well:

- each comment states what kind of comment it is
- patterns that recur become enums, which saves context
- a description has a limited size, and a longer one is truncated and marked oversized

Identifiers get their own type, a Pascal camel case string identifier.

A Nexus process can be such a call: a subflow given the spec.

**Sources**
```
b81560 operational-datomEverythingSystemPrompt
b81560 operational-nexusProcessObjectsAndEthosInDatom
```

**Left out or in conflict**

- T13, datom everywhere or only where needed:
  - 2026-09-19 (E30): "everything is going to be Datom", in "the system prompt of all our machine calls".
  - 2026-09-27 (`flows/8904b1/vision/datom.md`): "we don't need Datom syntax where the program doesn't need it".
  - The statement drops "all" from the first sentence and keeps "everything ... is specified". The two sides are stated, not resolved. See cluster 11.
- No example code: no ethos form for a spec-programmed call, an oversized description or the identifier type has been ruled. Before it lands, the statement needs an example the living accepts.

---

## 4. Ethos repeats nothing

- Lands in: `Vision/ethos.md` ("Non-repetition", "Inline types", "A variant named as a defined type carries that type", "A variant may declare its payload inline")
- Replaces 394 words: E36 (24), E13 paragraphs 2 and 3 plus the opening of paragraph 5 (165), E29 (84), E21 paragraph 2 (121)

**Statement**

Ethos repeats nothing. Any repetition in its syntax is an implementation failure, and ethos aims to be the tersest, least repetitive syntax ever made. Its compactness comes from low noise, never from short words. Nothing is repeated, nothing is out of place, and the text is pure description of a program.

There is no indirection:

- A variant whose name is an already defined type carries that type, and the type's name is written once. A variant is never written as its name followed by a type.
- A variant whose data is a simple struct has the struct written right after it, and ethos derives the struct's name deterministically. A variant and a struct may share a name.

A type is specified in full, inline, where it first appears. Every later appearance uses only its name. Sugar is used wherever it can be.

```
Library
[]                                         ; imports
[ FilePath.String                          ; types
  SyntaxError.Vector<FilePath>
  GenerationFailure.[ SyntaxError          ;   names a defined type: carries it, written once
                      Unwritable.{ FilePath String } ] ]   ; the struct follows the variant
[]                                         ; kinds
[]                                         ; associations
```

**Sources**
```
vision-raw ethosNonRepetitionLaw
7328f4 ethos
b80e55 ethosInlineTypeDeclaration
e51411 ethos
```

**Left out or in conflict**

- Conflicts with distilled state: `Vision/ethos.md` gives an inline payload a derived name with an underscore (`Unwritable_Data`) so that it never collides. E13 (2026-09-30) says a variant and its struct can share a name, "so I don't even think that's a problem". Both are stated. The living has not ruled on the derived name.
- Left out, stays verbatim: E13 paragraph 1 (52 words, frustration at the syntax). E13 paragraph 4 (49 words), where he is unsure whether "skill name" should be just "name". The rest of E13 paragraph 5 (about 103 words) is the process for that day: Fable and Astra design, then Mind implements.

---

## 5. One standard entry point enforces the Nexus's path

- Lands in: `Vision/nexus.md`
- Replaces 382 words: N1 (205), N13 paragraph 1 (117), N16 first two sentences (35), N23 (25)

**Statement**

Every Nexus enters through one standard entry point, a standard main written like a Rust macro, for its executable or its library. The Nexus is the only main call, and it then loads its signal. Through this entry point the machinery enforces its own invariants, so the rest of the code cannot bypass them. Above all, a signal reaches memory only through operation, then returns through operation and leaves as signal.

The Nexus's process objects process everything. A signal calls a Nexus object, the call goes through a process, and that process is the implementation, written by hand.

The project must use the ethos specs. The ethos defines the types in this path, so reading the ethos shows the main objects and processes. When Rust is written so that the structure is enforced and only the implementation is left to the hand, the code complies with ethos.

At its simplest, the macro takes a datom-derived type and generates all the input selection and conversion boilerplate.

**Sources**
```
5ed94b nexusEntryPoint
b81560 operational-nexusProcessObjectsAndEthosInDatom
6cc91b nexus
bc05da32 mainFunction
```

**Left out or in conflict**

- T16, a standard main was asked for, abandoned and asked for again:
  - Asked for: 2026-08-22 (a simple macro), 2026-09-14 (the Nexus as the only main call), 2026-09-19 (the main function is standard).
  - Abandoned: 2026-09-10 (`flows/fe34eb/vision/nexus.md`), "I think I was overthinking the whole nexus-core runtime concept."
  - Asked for again: 2026-10-04, "an idea of mine that I've been trying to put into practice".
  - Both sides stay.
- Possible conflict with cluster 2: N23 (2026-08-22) has the macro generate "conversion boilerplate". Clusters 2 and 3 (2026-09-15, 2026-09-24, 2026-09-28) keep text conversion out of the Nexus. The records do not say whether the macro's conversion is the CLI's or the Nexus's.
- Left out, stays verbatim: the rest of N16 (about 72 words), on Forge doing everything cargo did, with source caching. That belongs to another subject.
- T15 on the part names: see cluster 1.
- No example code: no form of the macro has been ruled.

---

## 6. Why Ethos: the mental model and the code in one language

- Lands in: `Vision/ethos.md` ("Why Ethos", "Horizon")
- Replaces 378 words: E32 (121), E35 (89), E33 (23), E20 (64), E21 paragraph 1 (49), E22 (32)

**Statement**

Ethos is the language that writes down the mental model of the machine and the code in one swoop, so that the code and the ideas behind it do not drift apart. Rust, JavaScript and similar languages are more than half noise.

Rust is the new assembly language. No serious engineer reads all of it, so our systems are understood through their kinds and main types, and every method call in our Rust belongs to one.

Ethos and Datom are our central language: the specification of data, and data itself. Together they are dense and cognitively concentrated enough to write code with AI agents.

Ethos will eventually replace everything. What that enables, generator emission among it, comes in its own time. Within a few months a whole program is to be written directly in Ethos. That needs:

- a function syntax
- implementations, which are what ethos lacks beyond types and which live on kinds
- a manifest built out for compiling and finding dependencies

**Sources**
```
aa4c7747 ethos
a5587095 rustComponentArchitecture
bc05da32 mainFunction
e51411 ethos
e51411 systemPrompt
```

**Left out or in conflict**

- T13: E22 (2026-09-25, Ethos and Datom are the central language) is on the "everywhere" side of T13. See cluster 11.
- The two timings on the same day differ. E20 (2026-09-25): "within a few months ... the whole program directly in Ethos". E21 (2026-09-25): "we want to eventually do that but for now ...", which asks whether functions are worth designing now. Both stand.
- E35 says "trait". The statement says kind because of his rule in cluster 13 that by trait he means kind. The trait rule itself is already in `Intent/mandatoryTraits.md`.

---

## 7. Every runtime component is a Nexus

- Lands in: `Vision/nexus.md` (it confirms "A kind of thing", "Library and daemon" and "Why everything is a Nexus")
- Replaces 354 words: N19 (50), N20 (19), N21 (21), N22 (105), N24 (40), N25 (26), N10 (93)

**Statement**

Every runtime component built from now on is a Nexus. What used to be called "the rest components" or "daemon CLI signal components" is just another Nexus. Nexus is our word for the style of component that speaks signal and uses a similar database. A Nexus is a daemon among other things, or it would simply be called a daemon. Those other things are still to be specified.

The nexus repository is the library that defines the core of a Nexus component. Libraries are still needed, datom and kind libraries among them.

Design goes straight to a Nexus:

- break down what it deals with
- isolate the kinds through which those things interact
- give the kinds their proper names

The tools we need are nexuses. Psyche Nexus replaces how Psyche is logged. Mind Nexus replaces how Mind and Field are logged, and more than logging: how Mind, Field and Psyche interact with the system. Both are developed realistically.

**Sources**
```
fe34eb nexus
aa4c7747 ethosMonolith
cff271af skillDesigning
e06e4c07 rustComponentArchitecture
e51411 nexus
```

**Left out or in conflict**

- Left out as an impurity of its time: N24 (2026-08-22), "nexus becomes software-design", a skill rename. The skill set has changed since then.
- N10 carries the recorder's own unconfirmed note that "log Psyche and Mind" may be a slip. The statement follows the words as received.
- Left out: N22 names what the ethos Nexus specifically deals with (ethos files, their locations, an index, the regenerated Rust). That detail is specific to one Nexus.

---

## 8. Ethos is laid out so its structure shows

- Lands in: `Vision/ethos.md` ("Spacing")
- Replaces 328 words: E3 (258), E7 (39), E1 (31)

**Statement**

Ethos is laid out so that its structure is obvious. It reads like a data structure that grows downward at each new layer, perfectly aligned, as in Nix or Python.

- Nothing deep is written on one line, because one line hides the structure and a wrapped line falls back under its own start.
- An inline definition goes vertical and moves freely to the right.
- A nested bracket also expands vertically.
- A closing delimiter never takes a line of its own.

A depth of about three was proposed as a soft limit. Past that depth, a part is referenced from another library, where three more levels open.

Ethos code carries many more comments, so that the living sees what the machine sees.

```
; one line hides the structure
Lock.{ LockId LockName Vector<String> Option<Lock> }

; each layer opens downward; the closing delimiter ends the last line
Lock.{ LockId
       LockName
       Vector<String>
       Option<Lock> }
```

The example is an illustration in the syntax of `Vision/ethos.md`. It is not a form he gave, and it needs his approval.

**Sources**
```
91ea9f ethos
edf227 ethosComments
```

**Left out or in conflict**

- T14, comments:
  - 2026-10-03 (`flows/edf227/vision/ethosComments.md`): "all of the Ethos code to get way more comments".
  - State, the 28d847 handover: the ethos-zero departure "comments dropped" is waiting on his Ethos ruling.
  - Both stand.
- Ambiguous, so not carried as a ruling: E3 says the depth limit "would mean it's more like a user interface approach to programming languages rather than accelerating the cognitive transmission of ideas". The record does not say whether that is a merit or a cost.
- Unclear, left out: E7, "I don't think you really understood what I meant about the traits and the parameters for it". What was misunderstood is not recorded.
- Discarded as an impurity of its time: E3's "let's redo all of the book".

---

## 9. Every new object is shown first as its ethos spec

- Lands in: `Vision/ethos.md`
- Replaces 325 words: E8 (57), E9 (28), E10 (16), E11 (14), E12 (60), E14 (61), E28 paragraph 1 (89)

**Statement**

All machine-to-machine language invented along the way is ethos. Whenever a new object is presented, whether a kind, a message or a datom, its ethos spec comes first. Example datom follows, showing the object in use: how it is used and the queries and responses it produces.

Ethos that is shown is always correct ethos. A block that lacks its type is not ethos, because without the type nobody knows what it is.

Three skills teach this:

- protos, kept very general
- datom, which shows the Rust structured type that decodes a datom
- ethos, which shows the Rust generated from ethos, and also the Rust generated by default with nothing in ethos to represent it, such as the compile-time checks of kind implementations

The ethos skill is loaded whenever a messaging system is created or changed. It teaches how to write an ethos spec.

**Sources**
```
91ea9f flowNexus
41fa34 ethos-and-example-datom
e8c4cc61 designPractice
c64ee3 ethos
b81560 operational-ethosSpecSkillAndTriadBranches
```

**Left out or in conflict**

- E9 repeats words from E8. Both are counted because both stand in the package as separate quotes.
- Left out because it belongs to another subject (subject 2, Flow): E28 paragraphs 2 to 4 (348 words) stay verbatim. They cover message specs proposed by agents, reviewed by Mind and approved by Psyche; Field patching; and branches and worktrees per aspect.
- Discarded as an instruction for that day: E8, "design the 'What are your most important questions?' proposition".

---

## 10. An ethos edit is the data migration

- Lands in: `Vision/ethos.md`
- Replaces 234 words: E15 (110), N3 paragraph 5 (124)

**Statement**

Ethos is specified in its own ethos language. It has its own structure for how it is stored in the nexus, and those stored forms are ethos versions.

A change to ethos is operational. The edit to the source is itself the operation that migrates the data, the exact update a data type needs to reach its new memory format.

The memory kind implements a standard successful or unsuccessful change on its data types. Each version may implement an upgrade from its predecessor, or to its successor. Upgrade-from fits better, because it upgrades the past, but the operation may be symmetrical.

The same principle holds for every proto family, datom included. Eventually ethos compiles to a full Rust program.

**Sources**
```
c64ee3 ethos
91ea9f ethos
```

**Left out or in conflict**

- Possible conflict with distilled state: `Vision/ethos.md` says an ethos file carries no version and versioning lives in a manifest. E15's "ethos versions" are versions of how ethos is stored in the nexus, not versions inside a file. The record does not settle whether these conflict.
- He left upgrade-from against upgrade-to open ("I'm not sure"). The statement keeps it open.
- No example code: no form has been ruled for a memory kind or an upgrade operation.

---

## 11. Datom only where a program needs it

- Lands in: `Vision/datom.md`
- Replaces 230 words: E16 (27), E17 (24), E25 (99), E26 (80)

**Statement**

Datom syntax is not forced where a program does not need it. A messenger that needs none gets none, and a tool that requires datom syntax says so in its own skill.

Messages carry no wrapper such as a pasted-content tag. The messenger software stays neutral and datom is enough. Agents are not made to put unneeded information into messages.

A response given as datom is a datom as a whole, with its prose as a Markdown string inside it, which renders. It is never a datom placed inside a fenced code block.

**Sources**
```
8904b1 datom
752e0f messaging
836818 finalResponse
```

**Left out or in conflict**

- T13. Sides in date order:
  - 2026-08-26 (`flows/ac1e9ec8/vision/archive-datomSyntax.md`): components speak signal, and datom is only the edge for text systems.
  - 2026-09-19 (`flows/b81560/vision/operational-datomEverythingSystemPrompt.md`): "everything is going to be Datom".
  - 2026-09-23 (E26): "Your whole response is Datom. That's what we're going to do."
  - 2026-09-24 (E25): datom is enough, and nothing unneeded is forced in.
  - 2026-09-25 (`flows/e51411/vision/systemPrompt.md`): Ethos and Datom are the central language.
  - 2026-09-27 (`flows/8904b1/vision/datom.md`): no datom syntax where the program does not need it.
  - The package marks the 2026-09-27 words as later. This statement follows them for messengers and tools, and is not a ruling on T13.
  - E26 says every response is datom. The statement narrows it to "a response given as datom", which reads E26 in the light of 2026-09-27. Whether E26 still stands as "every response" is for the living. The narrowing is flagged, not settled.

---

## 12. Everything is a type

- Lands in: `Vision/ethos.md` (the datom side confirms `Vision/datom.md` "Name": no field names)
- Replaces 187 words: E5 (11), E19 (105), E27 (56), E18 (15)

**Statement**

Everything is a type, because everything is a variant of a set. Even an instance is one member of a population, and from the right angle it is a type of its own. For engineering reasons not everything becomes an enum, and the open-ended variants are called names.

Ethos has no key-value map, because a map is only a poorly specified struct. Datom has no named fields: the spec is known and the object is just the payload. Datom has variants, not tags.

```
Lock.{ LockId LockName }                                  ; ethos: a struct of types, no keys
GenerationFailure.SyntaxError.[ /abs/orchestrate.ethos ]  ; datom: a variant, no field names
```

**Sources**
```
91ea9f ethos
93ba9f ethosNames
0625c3 datom
93ba9f datomVocabulary
```

**Left out or in conflict**

- E19 says "There are no names really but you specify something while everything is a type". This sits awkwardly next to its own sentence that the open-ended variants are called names. The statement keeps both, with names as the engineering concession.

---

## 13. Kind, not trait; a kind takes kinds

- Lands in: `Vision/ethos.md` ("Kind", "Naming", "Identity" already carry it; landing this statement archives the raw records)
- Replaces 182 words: E6 (34), E4 (118), N12 paragraph 1 (30)

**Statement**

We say kind, not trait. They are nearly the same, but kind is more accurate, and when trait is said, kind is meant. A kind is named by its qualifier, as in Launchable, so that it reads as a kind. Launching, hearing and resolving are not kind names. What a kind takes is another kind, never a specific type, which is too specific. A launchable voice uses self.

```
Processable<[Clonable Sendable] Serializable>   ; constraints are kinds, never types (form as in Vision/ethos.md)
```

**Sources**
```
91ea9f ethos
26c50c ethos
```

**Left out or in conflict**

- Discarded as an instruction for that day: E4, "Do some actual real-world Rust checks ... make things clear here also in the knowledge skill".

---

## Verbatim: quotes that condense poorly or stand alone

Not counted as replaced. They stay in their raw records as they are.

| Quote | Date, source | Words | Why it stays |
|---|---|---|---|
| E2 | 2026-10-03, `flows/dea0ba/vision/contextModules.md` | 86 | The only record of a simple form and an extended form of the same data, defined in signal. It has no cluster partner. |
| E23 | 2026-09-24, `flows/752e0f/vision/ethosNextGeneration.md` | 103 | Nomos and logos. Three layers are named but only two are listed, so it cannot be completed without inventing the third. |
| N7 [NOTION] | 2026-10-01 (file date), `flows/efa157/notion/nexusScaffolding.md` | 399 | A notion, not a ruling: a Nexus that creates Nexuses, Forge subscriptions, private test repositories. |
| N2 [NOTION] | 2026-10-03, `flows/5578cc/notion/nexus.md` | 27 | An open question, named in cluster 2. |
| N8 paragraph 2 | 2026-09-28, `flows/8904b1/vision/skills.md` | 71 | Flow identity taken from the calling process. One quote only. |
| N14 | 2026-09-17 (file date), `flows/b49251/vision/nexusAnatomy.md` | 83 | Functionality may move between nexuses as the anatomy is found. One quote only. |
| E28 paragraphs 2 to 4 | 2026-09-20 (file date), `flows/b81560/vision/operational-ethosSpecSkillAndTriadBranches.md` | 348 | Subject 2, Flow: aspects, branches, worktrees. |
| E13 paragraphs 1 and 4, rest of 5 | 2026-09-30, `flows/7328f4/vision/ethos.md` | about 204 | Frustration, a tentative naming question, and the process for that day. |
| N16 rest | 2026-09-14, `flows/6cc91b/vision/nexus.md` | about 72 | Forge replacing cargo. Another subject. |

## Counts

| Rank | Cluster | Words replaced | Statement words |
|---|---|---|---|
| 1 | Three parts: signal, operation, memory | 596 | 186 |
| 2 | A Nexus never handles text | 492 | 157 |
| 3 | Machine calls programmed with an ethos spec | 446 | 222 |
| 4 | Ethos repeats nothing | 394 | 144 |
| 5 | One standard entry point | 382 | 165 |
| 6 | Why Ethos | 378 | 165 |
| 7 | Every runtime component is a Nexus | 354 | 160 |
| 8 | Layout shows the structure | 328 | 125 |
| 9 | Ethos spec shown first | 325 | 146 |
| 10 | An ethos edit is the migration | 234 | 119 |
| 11 | Datom only where needed | 230 | 93 |
| 12 | Everything is a type | 187 | 83 |
| 13 | Kind, not trait | 182 | 68 |
| | Total | 4,528 | 1,833 |

Statement words count only the statement prose, not the code blocks, measured with whitespace splitting.
