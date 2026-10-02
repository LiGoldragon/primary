
Presentation.{ «Ethos as two skills, the case study» }

Your word: "Let's focus on the stuff about ethos ... let's start moving all of the skills and vision skills ... into the proper prefix skill." (typed, 2026-10-02). This book is the ethos move, whole: what goes where, the exact text of each new skill, and what stays open. The two before it («Where the edit goes, and vision as skills», uncommented) asked for the prefix set; this one assumes `vision-` and `knowledge-` and shows them on ethos so you can rule on the thing itself.

**1. What moves where.**

Today ethos lives in three places: the `ethos` skill (37 lines of your wishes, 27 lines of how the generator behaves), the `Vision/ethos` file (24 approved statements, several now stale by your own word: "we need to change the vision"), and fourteen sayings of yours since 2026-09-30 that are in no skill at all. After the move there are two homes: `vision-ethos`, every line of which is your wish; `knowledge-ethos`, every line of which is what ethos-zero does today, witnessed. The `ethos` skill and `Vision/ethos` are deleted; nothing is kept beside. **Ruling 1:** this move.

**2. `vision-ethos`, the text.**

> "Let's make things clear here also in the knowledge skill." — psyche, typed, 2026-10-02.

```
description: An ethos file is written, or a type, kind or layout is judged against what the living wants ethos to be.
```

Ethos is the schema language: it writes the mental model and the code in one swoop. Ethos specifies the types; datom fills them with data. Any repetition in ethos syntax is an implementation failure.

Four roots: Library, Signal, Operation, Memory. Signal declares what a Nexus says; Operation what it does, one operation type for every effect; Memory what it remembers; Library what they share. A memory kind carries a standard successful-or-unsuccessful change and, for each version, the upgrade from the previous format; that upgrade is the very edit the type needs.

Everything is a type; there is no key-value. A type used once is declared inline where it is used; a type used in more than one place is declared once and named. A variant's payload is written in the variant and bears the variant's name; no second type is invented to hold it. Inline nesting goes about three deep; past that, the type comes from a Library.

Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line. Nothing that has a next layer sits on one line.

A kind is the bearer of capabilities and is qualifier-named: Launchable, Streamable. A capability speaks in Self, the kind's own parameters and other kinds; a concrete type in an input is a kind not yet named. In ethos there are no generics, only kinds; a constraint is a kind, never a type.

The Flow Nexus in the four roots, written this way:

```
Library
[]
[ FlowId.Integer
  Voice.[ Psyche.Rank
          Mind.Rank
          Field.Rank ]
  Rank.[ Primary Secondary Tertiary ]
  Event.[ Started
          ToolUsed.String
          Stopped ] ]
[]
[]

Signal
[ flow:[ FlowId Voice Event ] ]
[ Launch.{ Voice
           Brief.String }
  Report.{ FlowId Event } ]
[ Launched.FlowId
  Refused.[ NoCapsule
            VoiceBusy.Voice ]
  Reported ]
[]

Operation
[ flow:[ FlowId Voice Event ] ]
[ Start.{ Voice Capsule }
  Record.{ FlowId Event } ]
[ Started.FlowId
  Recorded
  Failed.String ]
[ Capsule.{ Home.String
            Login.Vector<String> } ]

Memory
[ flow:[ FlowId Voice Event ] ]
[ Flow.{ FlowId
         Voice
         State.[ Running Ended ]
         Vector<Event> } ]
```

`FlowId`, `Voice` and `Event` are used by three roots, so they live in the Library; `Capsule` is used once, so it sits in the Operation file; `Brief` and `State` are used once and sit inline. **Ruling 2:** this text.

**3. `knowledge-ethos`, the text.**

```
description: Rust is generated from an ethos file with ethos-zero as it runs today, or what the generator accepts is read.
```

ethos-zero reads three roots: Library, Signal, Sema. The sweet form, root head then sections as siblings, is converted to the canonical braced form before reading. Section order: Library imports, types, kinds, associations; Signal imports, queries, responses, types; Sema imports, record types; associations of query, response and record types are implied.

`Name.Type` is an alias, `Name.{ }` a struct, `Name.[ }` an enum. A field is named after its type in snake case, `string_vector`, `lock_option`, `first_lock` and `second_lock` when repeated. An inline payload generates a Rust type named `<Variant>_Data`. Imports are `protos:String` or `protos:[ String Integer ]`; intrinsics need none: String, Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self.

A simple kind is `Name.[ capabilities ]`; receivers `.` self, `!` mutable self, `:` none; a capability with inputs is `push!{ [ inputs ] [ yield ] }`; a complex kind is `Name.{ [ superkinds ] [ associated types ] [ CONSTANTS ] [ capabilities ] }`. The generator accepts a concrete type as a capability input and refuses a kind there.

Every generated struct and enum derives Datomizable and Composing; an alias carries no derive; a Signal's datom derives sit behind a `datom` feature that the CLI enables and the Nexus does not. A generated file opens with `#![allow(dead_code, non_camel_case_types, non_snake_case)]`, every item carries `#[rustfmt::skip]`, names are fully qualified with no `use`. Generated Rust is committed and held fresh by a test. An association generates a compile-time assertion; the interaction body is hand-written. The print is one line, a space inside every non-empty bracket and brace.

```
ethos-zero 'Generate.{ /abs/flow.ethos /abs/out }'
Generated.[ /abs/out/flow.rs ]
```

Three of these lines contradict `vision-ethos` on purpose: three roots, `_Data`, the one-line print. They say what runs; they fall when ethos-zero changes. Before this lands, a flow witnesses each line against ethos-zero itself, since today's lines come from the old skill's text. **Ruling 3:** this text, landed after that witness.

**4. What stays open, and what is dropped.**

Open, your word needed:
- **4a.** `Brief.String` inside `Launch`: a type used once but whose name carries meaning. Inline alias in place, as written above, or in the types section?
- **4b.** The Operation root's sections above are imports, operations, outcomes, types. Is that its anatomy?
- **4c.** Where a version lives. You said "each version is possibly going to have an implementation of an upgrade from"; the old skill says a file carries no version, a manifest does. Manifest, or the Memory file itself?
- **4d.** One line of `Vision/ethos` reads larger than vision: "Ethos will eventually replace everything, Rustlang becoming its assembly layer." Should this be Intent?

Dropped, not moved: the history of the name Ethos Zero; "Why Ethos" (the noise of legacy languages), which explains rather than directs; the `Vision/ethos` lines the above replaces.

