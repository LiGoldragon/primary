# Six books: proposals, comments, rulings, landing, later records

Gathered 2026-10-16 by flow 65f93a, read-only. Every block below fenced with `~~~~` is copied byte for byte from the file and lines named in its Source line; nothing inside a block is paraphrased. Prose outside blocks is the gatherer's. Search scope: `flows/*/vision`, `flows/*/notion` (non-archive files only), `flows/*/log.md`, `flows/*/reports`, `flows/*/handover.md`. Landing was checked against `/git/github.com/LiGoldragon/psyche-skills` `origin/main` (fetched; head `53f68b6`, 2026-10-16, "Move every psyche module into its type folder", so a skill formerly at `skills/vision-<name>.md` now sits at `vision/<name>.md`). Book texts are embedded whole from their first proposal heading, so the proposed lines and code are exact.

Dates: a record's own date is given where the record states one. Where a record states none, the note says so; file modification times were not used (flows were restored from backups).

## Summary table

| # | Book | Proposals | Ruled | On origin/main | Unruled | Ethos code blocks |
|---|---|---|---|---|---|---|
| 1 | Shared Clojure translation pattern (d68c82/15) | P2 plus choices A and B | P2 "land" on edition 1 (2026-10-14) | prose paragraph only (4d80d68); graph, mapping, worked example not landed | edition-2 expansion of P2, choice A, choice B (3) | 1 (fenced as `clojure`) |
| 2 | Subflows, 4th edition (d68c82/r-subflows-kind) | P1, P2, P3 | none found | none | 3 | 0 (one datom listing, no Ethos fence) |
| 3 | How a metaflow is named on the wire (73ada7/7) | D1 with options a, b, c, d | none found | no | 1 | 0 |
| 4 | Word ids for flows, 2nd edition (0c85a3) | wordable.ethos anatomy with dictionary and casing; one vision-flow line | none found | no | 2 | 1 |
| 5 | The caller is witnessed (875960/8) | Proposal 1 (rulings 1 and 2), Proposal 2 (ruling 3) | none found | no | 3 rulings | 1 (unlabelled fence) |
| 6 | The Source nexus, 2nd edition (058f16) | D1 to D8 | none found | no (no vision-source file exists) | 8 | 1 |

---

# Book 1: The shared Clojure translation pattern, 2nd edition

- Path: `flows/d68c82/books/15-clojure-translation.md`
- Title: «The shared Clojure translation pattern» (Presentation line and `#` heading, identical). It is the edition-2 text (the Ethos worked example and the run Clojure are in it). Edition 1 was artifact Bo8aggF1TNjxDq5ZFTUpLR v1 (d68c82/log.md, 2026-10-14); edition 2 is v2 of the same artifact (same log, 2026-10-14).
- Proposals: one, "Proposal 2: The mapping and its graph", target `psyche-context/skills/vision-clojure.md`, plus two unnumbered choices (A variant representation, B keyword casing). The book states "The shared translation contract is landed in `vision-clojure`" (Proposal 1 of edition 1).
- Ethos code blocks: 1, lines 59-68, fenced as `clojure` (the `Library [] [ Person ... ]` worked example). The block at lines 72-76 is Datom values, 80-84 EDN, 44-55 the mapping table, 88-146 Clojure.

## 1.1 The proposals, verbatim (book lines 4-161)

Lines 4-26 are the graph that Proposal 2 calls "[graph above]"; 28-161 are the crystallization.

**Source:** `d68c82/books/15-clojure-translation.md` lines 4-161 (whole proposal text including the graph, the mapping, the worked example, choices A and B, and the book's own closing Ruling line)

~~~~text
# The shared Clojure translation pattern

```
+------------------+     +------------------+
|  Ethos           |     |  typed Datom     |
|  declaration     |     |  value           |
+------------------+     +------------------+
        |  through              |  through
        v                       v
+---------------------------------------+
|        shared construct mapping       |
+---------------------------------------+
        |  gives                |  gives
        v                       v
+--------------+          +-----------+
| Malli schema |--checks->| EDN value |
+--------------+          +-----------+
                                |  recovers
                                v
                      +-------------------+
                      | the typed value   |
                      +-------------------+
```

The shared translation contract is landed in `vision-clojure`.

## Crystallization

### Proposal 2: The mapping and its graph

File: `psyche-context/skills/vision-clojure.md`, after the landed line

```text
+ [graph above]
+
+ The declaration determines the schema and the interpretation of each value. Recovery preserves the typed value, not its textual spelling.
```

The construct mapping:

```clojure
Ethos        Malli schema        EDN value
scalar       named schema        scalar
struct       closed map of       map of the
             required entries    entries
vector       ordered vector      vector
variant      tag plus whole      tagged value
             payload
nesting      recursive           recursive
Option,      keep their variant  Some(None) is
Result       distinctions        not None
```

The worked example. Ethos:

```clojure
Library
[]
[ Person.{ Name.String Age.Integer }
  Reply.[ Accepted.Person
          Refused.String
          Pending ] ]
[]
[]
```

Datom values:

```clojure
{ Ada 36 }
Accepted.{ Ada 36 }
Pending
```

EDN values, the unit variant an empty vector:

```clojure
{:name "Ada" :age 36}
#accepted {:name "Ada" :age 36}
#pending []
```

Clojure, run:

```clojure
(ns translation-example
  (:require [clojure.edn :as edn]
            [malli.core :as m]))

(defn variant [tag schema]
  (let [valid? (m/validator schema)]
    [:fn (fn [value]
           (and (tagged-literal? value)
                (= tag (:tag value))
                (valid? (:form value))))]))

(def Person
  [:map {:closed true}
   [:name :string] [:age :int]])

(def Reply
  [:or (variant 'accepted Person)
       (variant 'refused :string)
       (variant 'pending [:tuple])])

(def readers
  (into {}
        (map (fn [tag]
               [tag #(tagged-literal tag %)])
             '[accepted refused pending
               some none])))

(defn read-example [text]
  (edn/read-string {:readers readers} text))

(def accepted
  (read-example
    "#accepted {:name \"Ada\" :age 36}"))

(m/validate Reply accepted)
;; => true
(m/validate Reply
  (read-example
    "#accepted {:name \"Ada\" :age \"36\"}"))
;; => false

(defn option-schema [payload]
  [:or (variant 'none [:tuple])
       (variant 'some payload)])

(def NestedOption
  (option-schema (option-schema Person)))
(def absent (read-example "#none []"))
(def present-absent
  (read-example "#some #none []"))

(m/validate NestedOption absent)
;; => true
(m/validate NestedOption present-absent)
;; => true
(= absent present-absent)
;; => false
```

Choice A, variant representation:

1. Tagged literals, `#accepted {...}` (recommended).
2. Tagged vectors.
3. Tag and payload maps.

Choice B, keyword casing:

1. Kebab-case, `:flow-id` (recommended; collisions are detected).
2. Ethos spelling, `:FlowId`.

After the choices: a minimal test fixture, then a knowledge module on how it works in practice, for review.

Ruling: land Proposal 2, with choices A and B.
~~~~

## 1.2 The living's comments on it, verbatim

The comments are on edition 1 (the book as first published, 2026-10-14; the same speech is logged by four flows). The living's first-order remark: all good, it can all land, fleshed out further.

**Source:** `d68c82/vision/ethos.md` lines 37-45 (logged by d68c82, dated in its heading, relayed by the Psyche Core Tertiary)

~~~~text
## 2026-10-14 — The Clojure translation, fleshed out

Context: after reading «The shared Clojure translation pattern».

> I read the shared Clojure translation, or whatever it's called, and it's all good. It can all land in the proposal.
>
> Now I want it much more fleshed out. Even the graph, the flow graph, should be in the vision. I want even more actual examples. I want to see some example code that's been... and then I want the mind to document it to create a knowledge skill that I'll review in terms of how this actually works in practice after testing it.

-- psyche, STT. Relayed by the Psyche Core Tertiary; unfinished sentences kept as spoken.
~~~~

**Source:** `7c89aa/vision/ethos-in-clojure.md` lines 37-53 (logged by 7c89aa, fuller version of the same speech, dated in its heading)

~~~~text
## The Clojure translation lands; fleshed out with the flow graph, examples, a knowledge skill, Chronos as the test, a Fable-assisted Primary and Secondary, an end-turn hook (2026-10-14)

Context: the living had read the shared Clojure translation and spoke this to the Tertiary.

> I read the shared Clojure translation, or whatever it's called, and it's all good. It can all land in the proposal.
>
> Now I want it much more fleshed out. Even the graph, the flow graph, should be in the vision. I want even more actual examples. I want to see some example code that's been... and then I want the mind to document it to create a knowledge skill that I'll review in terms of how this actually works in practice after testing it.
>
> Also let's use the most usable component that works best for testing the Nexus component but I guess something actually really simple. Maybe we re-adapt Chronos, the tool I had made to get astrological time based on current time or based on a specific time and location. Let's rewrite it in idiomatic Nexus architecture and ethos: full specification, just a simple thing, right?
>
> Send it to a fresh Fable-assisted primary and secondary. Starting with the secondary, we'll assemble all of the psyche-relevant and then start creating a prompt, not too long, like a couple thousand characters maximum, to add to what Fable will start with (so that he has a head start in terms of collecting stuff and it comes into the user prompt). Then Fable can just create the design and that's all Fable is for, really.
>
> The only thing it actually can be bothered with is to be given more information and then it can either be allowed to ask questions. If it ends its turn with a question or more than one question, then the secondary will just... We need an end-turn hook, basically, for the primary's turn end to notify the secretary.
>
> We should almost just add the functionality in Flow that decides where the hooks actually talk. The hook is a standard call with the right data so that the Flow daemon can check its database to see where these messages should go or what kind of notification should go where (based on the hook and where it came from).

-- psyche, STT. "I want to see some example code that's been..." and "the secondary will just..." are unfinished sentences, kept as spoken.
~~~~

**Source:** `5b9075/vision/clojure.md` lines 1-7 (logged by 5b9075, relayed by Psyche Core Secondary through Tertiary and Mind Prototyping Secondary; date not stated in the record, same speech, 2026-10-14)

~~~~text

## The flow graph in the vision

Context: After reading «The shared Clojure translation pattern», https://claude.ai/artifact/Bo8aggF1TNjxDq5ZFTUpLR. Relayed by Psyche Core Secondary through Psyche Core Tertiary and Mind Prototyping Secondary. The living approved inclusion in the proposal and requested fuller examples and a knowledge skill reviewed after testing. The unfinished example-code sentence is not completed or treated as a separate statement.

> Even the graph, the flow graph, should be in the vision.

~~~~

**Source:** `e4b7d7/vision/clojure.md` lines 1-7 (logged by e4b7d7; date not stated in the record, same speech, 2026-10-14)

~~~~text
# Clojure

Context: after reading «The shared Clojure translation pattern», artifact Bo8aggF1TNjxDq5ZFTUpLR; relayed by Psyche Core Secondary through Psyche Core Tertiary. The surrounding message asks for a fuller proposal, actual examples, testing, and a knowledge skill for review.

> Even the graph, the flow graph, should be in the vision.

-- psyche, STT, relayed through Psyche Core Tertiary and Psyche Core Secondary.
~~~~

No separate comment on edition 2 was found. The choices A and B drew no comment.

## 1.3 Ruling and landing

Ruling on edition 1 (as logged by the hub). Note the log says the choice was "not named" and that A and B stayed unruled:

**Source:** `d68c82/log.md` lines 1325-1327 (d68c82 log, the Event/Ruling lines of 2026-10-14)

~~~~text
Ruling: «The shared Clojure translation pattern» approved, land (choice not named; the book's choice 1, vision-clojure, taken). Orders: flesh out with graph in vision and examples; Mind knowledge skill after testing; Chronos rewrite in Nexus/Ethos by a fresh Fable-assisted pair, Secondary first, ≤2000-char head-start prompt; Primary turn-end hook notifying its Secretary; Flow routes hooks (vision).
Event: e4b7d7 accepted vision-clojure landing; subflow landing it; Astra Primary 5b9075 has the words and the book→testing→knowledge sequence.
Event: e4b7d7 landed vision-clojure in psyche-context 4d80d68. Variant representation and keyword casing remain unruled (only unruled prose in d4ae97 «Clojure, the vision»); they go in the fleshed-out book.
~~~~

**Source:** `e4b7d7/log.md` lines 26-26 (e4b7d7 log)

~~~~text
- Landing subflow witnessed exact published front matter/text in flows/d68c82/books/15-clojure-translation.md; authored psyche-context/skills/vision-clojure.md landed and pushed origin/main at 4d80d6, diff check passed, lock 20983 released. Commit reported to Psyche Core Secondary and Prototyping Primary.
~~~~

Ruling status: P2 of edition 1 ruled "land" and landed as prose. P2 of edition 2 (graph, construct mapping, worked example, choices A and B) has no ruling: the living said "Now I want it much more fleshed out" and edition 2 is that expansion. Choices A and B are explicitly unruled in the log above ("Variant representation and keyword casing remain unruled").

Landed text: commit `4d80d68` "vision-clojure: land shared translation pattern" (2026-10-14), now in the type folder after `53f68b6`. Complete current file:

**Source:** `psyche-skills origin/main:vision/clojure.md` (current content; no graph, no mapping table, no "The declaration determines the schema" sentence, no worked example)

~~~~text
---
description: A Clojure prototype represents an Ethos type or a Datom value.
dependencies: []
---

## Clojure

The Clojure translation preserves the anatomy declared in Ethos: named types, struct positions, variant identity and payload, and nested containers. One shared construct mapping defines their Malli schemas and EDN representations, including how Datom values become those EDN values. Each representation keeps enough information to recover the same typed value.
~~~~

## 1.4 Later records on the same subject (psyche; vision, notion, non-archive)

Origin of the pattern (before the book, same day):

**Source:** `df159a/vision/clojure.md` lines 3-9 (logged by df159a, 2026-10-14, stated in the record)

~~~~text
## A standard translation of an ethos specification to a Clojure type and EDN; a context module for it

Context: 2026-10-14, spoken to the Psyche Core Tertiary after commenting on «Short-term prototypes: Clojure now?». Relayed by Psyche Flow Secondary da2038.

> I've commented on the Clojure prototypes and I want to design a standard way to translate an ethos specification to essentially a Clojure type, I guess, that can be represented in EDN instead of datom. For both Clojure and EDN let's work out a context module for this: how we translate an ethos and datom syntax into Clojure and EDN.

-- psyche, STT.
~~~~

Same day or after the book:

**Source:** `d68c82/vision/books.md` lines 149-155 (2026-10-14, relayed by the Psyche Core Tertiary)

~~~~text
## 2026-10-14 — Proposals of code

Context: same speech, relayed by the Psyche Core Tertiary.

> I don't want proposals to code. If you want to propose code to me, I want you to propose an approach or a pattern, or some wrapping code that will become standard, like a standard entry point or a standard pattern.

-- psyche, STT.
~~~~

**Source:** `d68c82/vision/books.md` lines 157-163 (2026-10-14, comment on the Clojure book's carried proposal)

~~~~text
## 2026-10-14 — References found the same way

Context: comment on the Clojure book's carried proposal, ruling item on where the reference file lives (choices: beside the book's source, or a references/ directory beside the books); anchored on "under references/ beside the books".

> Yeah make it some kind of standard so that they can all be found the same way.

-- psyche, STT.
~~~~

**Source:** `7c89aa/vision/ethos-in-clojure.md` lines 17-23 (2026-10-14)

~~~~text
## Side question: objects with methods in Clojure (2026-10-14)

Context: asked as a side question, not important.

> I want to know: does Clojure have object-oriented programming where we can have methods on objects instead of functions taking in? So we can be more object-oriented, kind of like how we do [Rust]. Just a side question, not important. If not it's okay.

-- psyche, STT. Transcription corrected: "REST" → "[Rust]" (the living confirmed: "Rust not rest").
~~~~

**Source:** `d68c82/vision/tools.md` lines 14-18 (2026-10-14)

~~~~text
## 2026-10-14 — a repeated use case grows an existing tool; EDN in Clojure, datom in Nexus

> Anything that can be abstracted so that it's reused. If we see a use case repeat itself, then we should try to adapt whatever tool we already have to become more capable and broad. If we're in Clojure we use an EDN payload for everything and if we're in Nexus we use a datom.

-- psyche, STT.
~~~~

**Source:** `da2038/vision/psyche.md` lines 2-10 (2026-10-14, stated in the Context line)

~~~~text
## Mass-delete overruled raw psyche; long term made explicit; makeshift is Clojure, Malli, EDN

Context: the living, directly to Psyche Flow Secondary da2038, 2026-10-14, introducing a message he sent someone (the message itself did not arrive), which he offers as confirmation, not order or vision.

> Here's an interesting message I just sent someone about the current recent developments here. I'm not giving this to you really as order or vision but maybe just as a confirmation that you can use to find the most important crystallizations that are clear in terms of having lots of data to back it up or write a lot of raw psyche.
>
> Also I want to delete a lot of raw psyche. I want to mass-delete all this stuff that I've overcomplicated and rolled back on or overruled for a simpler design, especially anything that simplifies. Also the differentiations between long term and short term so that we can push a bunch of stuff that sounds more advanced into the long term explicit. Then stuff that is really makeshift/prototype, meaning [Clojure], [Malli], EDN in nature.

-- psyche, STT, 2026-10-14. Transcription corrected: "closure" → "[Clojure]", "malle" → "[Malli]".
~~~~

**Source:** `d68c82/vision/flow.md` lines 170-180 (comment of 2026-10-14 relayed 2026-10-15; names the Clojure equivalents of Ethos)

~~~~text
## Subflows by role and by level

Relayed by Psyche Core Tertiary, 2026-10-15; the living's comment of 2026-10-14 on «Subflows», Proposal 2, the specialties table.

> These would all just be redone by role and by level. Secondary is the highest subagent, of course, and then tertiary and quaternary.
>
> Let's have some basic roles instead of writer and reader. ... Let's split this up into these context modules. In these context repos, like psyche context, mind context, and field context, we don't write skills. There's no skills directory. Let's refashion that so it's by type. ...
>
> This is all basically in ethos code, with implied equivalent [Clojure], which we need to draft on also: what the equivalents look like, with some examples and actual code in a knowledge review.

-- psyche, STT. Transcription corrected: "closure" → "Clojure".
~~~~

**Source:** `d68c82/vision/books.md` lines 305-311 (2026-10-16)

~~~~text
## A proposal touching code shows the code

Context: on Proposal 12 of «Flow: context modules and the prompt, 2nd edition» (inline imports), 2026-10-16.

> "This is not quite accurately described and needs example code. Obviously I'm surprised that there was zero code proposal in here. I think almost anything that touches upon a code component should touch on the code."

-- psyche, typed.
~~~~

**Source:** `65f93a/vision/ethos.md` lines 38-105 (2026-10-16 22:16-22:30; applies to every book with Ethos code, this one included)

~~~~text
## Comments on «The Ethos syntax»: real code only, traits declared, Fable involved; the dot and the brace (2026-10-16, 22:16–22:30)

Context: spoken to the Psyche core Tertiary after commenting.

> "I commented on the ethos syntax and there's a lot of garbage. The code is fucking garbage so I want all the books redone because obviously the ethos is going to be wrong everywhere.
>
> Also we need to get serious about ethos traits because I really don't see any of them and it's like you don't want your programs to do anything. If there are no declared traits for these types, these types can't fucking do shit. It means you want a system that does nothing. If you show me another thing that has no [trait], you're showing me a system that doesn't do anything.
>
> Get Fable involved, stop being so retarded, and make systems that actually do things."

Context: Proposal 1, "braces open on their own line, under the variant; the first section sits on the brace's line".

> "No not quite. The braces don't open on their own line. It's just usually canonical to make a new line because, actually, you don't have to open the brace on a new line. I didn't say that. I said that it should be possible in the syntax to do that but that the new line really doesn't need to be for the brace.
>
> It's just that we do it on a non-indented new line, generally in files, because we don't need the indentation. We don't want too much indentation and the first variant is really just giving us the type of that file unless we do start supporting a vector, in which case it's still going to have a variant.
>
> It's not an invariant like you said it is. It's just usually good form but it's not necessary."
>
> "And no you would not put the brace and the first section on the same line. That's the whole point of why you make a new line after the brace actually. But if it's just a single type then there are no breaks because it's just one thing."

Context: Proposal 1's Library example, indented under the brace.

> "See here, you did it all wrong. You did make an indentation when I said... My whole point was the only thing I wanted to say. You missed my entire point, which is: no indentation for that first struct. Do you understand what I'm saying? I don't know why I'm asking you because you're not going to respond like that. Yeah that's what I'm trying to say."

Context: Proposal 2, "A space and a line break may follow the dot".

> "Not a space and a new line, just any kind of space or new line, any amount of space. The dot doesn't care if what comes after is right next to it or if there's a space, a new line, a tab, or any number of spaces."
>
> (On its Observed.Locks example:) "Yeah this example is good."

Context: Proposal 3, the type ethos with a one-variant CommitMessage enum, and "A type ethos may carry one or more examples of its datom."

> "This is invalid. We cannot have an enum with only one variant and I don't understand. I don't think your last paragraph is good. When you say a type ethos may carry one or more examples of its [datom], I don't know what you mean by that. There's no logic there. There's no foundation for what you're saying.
>
> I think you're confused because I said, "If you show me a new [datom], you can show me the type." Now you think that that means... I don't know, you're just fucking hallucinating bullshit. Do you understand what I'm saying?
>
> This is bullshit: you think that you're forcing the jigsaw puzzle pieces together. You're smashing them all. You're just breaking them all by trying to fit shit together that has absolutely nothing to do with what you're trying to explain. You're explaining the vision and then... I'm really tired of this kind of behavior where you just put bullshit together. You just try and fit everything together that doesn't fit together."

Context: Proposal 4, "Every variant is capitalized, a root's variant and `Type` included".

> "You don't need to say "type included." Why the fuck do you say "type included"? That just looks stupid. Stop talking like a retard."
>
> (On its examples:) "Your examples suck 'cause they're wrong. Anything that's wrong, anything that is not canonically written, or just a piece of it is just garbage. Absolutely fucking confusing fucking garbage. Do not confuse everybody with your bad, incorrect, shitty examples."

Context: Proposal 5 (Type is no exception) and Proposal 6 (whitespace after a separator).

> "This section is good."
>
> "This is good."

Context: Proposal 7, a canonical print that breaks after the dot, two spaces per link.

> "No I don't want to make this canonical. Your example is garbage because it's mixing things which cannot be mixed together. Stop making any kind of code that could not work in practice. These are wrong.
>
> We have to stop completely, absolutely: never, ever, ever make an example that is not real code, ever, ever fucking again. Never, ever, ever.
> - Golden fucking rule
> - Top of the list
> - Full book on this topic
>
> Stop giving me bad code ever, never, ever, ever, ever, ever. I want to see bad code ever, ever"

Context: Proposal 8, a new datom shown with its specification; a production datom's specification in a knowledge module; the example Reply.[ Accepted.Integer Pending ].

> "There's a lot of bullshit here. This specification may or may not be in a knowledge module. It depends if it's implemented so why are you saying that? You don't seem to understand the principles that you should understand before you start explaining this to me. Let's go back to those principles.
>
> Your example is bullshit because every ethos needs a variant and your ethos has no variant so it's fucking garbage, just like most of the code in here. You have to stop writing ethos like it's like you're writing it without caring. It's like you don't care. It's like you're just making shit, slop, shit, garbage, filth. Stop giving me fucking filth, you filthy bastard."

-- psyche, input mode not shown, book comments, relayed by Psyche Core Secondary (anchors as in flows/d68c82/vision/ethos.md). Transcription corrected: "trade" → "trait"; "datum" → "datom".
~~~~

---

# Book 2: Subflows: kind, role and level, 4th edition

- Path: `flows/d68c82/books/r-subflows-kind.md`
- Title: «Subflows: kind, role and level, 4th edition» (Presentation line); the `#` heading reads "Subflows: kind, role and level". Published as "Subflows 4th" `22Ppun...` (d68c82/log.md line 1995, 2026-10-16T12:35:55-06:00, "Redo batch 3"). Earlier editions: «Subflows: one kind, specialties, a contextualizer» (MoqWqQyDx49d8PQ9bYWq1h, 2026-10-14), ed. 3 `XpPEQD1TFjWA8rQXrTSTNN` (2026-10-15; file `flows/d68c82/books/17-subflows-kind.md`).
- Proposals: three, targets `psyche-context › skills/vision-flow.md`, `psyche-context › skills/vision-datom.md`, `psyche-context › skills/vision-model-roles.md`. Each ends "Ruling: land, amend, or reject."
- Ethos code blocks: 0. Proposal 2 holds a datom listing (`type.Kind { Field Operator Tertiary }` and two more lines), not an Ethos fence.

## 2.1 The proposals, verbatim (whole book body, lines 4-32)

**Source:** `d68c82/books/r-subflows-kind.md` lines 4-32 (whole book body from the heading to the last ruling line)

~~~~text
# Subflows: kind, role and level

A subflow's kind is its use, made of three parts: its aspect, its role and its level. This edition carries the three lines on that subject still awaiting your ruling. The kind's code and the contextualizer went to their owner, and the folders of context modules were settled in «Context modules: folders, types, placement».

## Proposal 1: psyche-context › skills/vision-flow.md

+ A subflow's kind is its use: an aspect, a role and a level, which compose.
+ Secondary is the highest level of a subflow, then Tertiary and Quaternary.
+ Each kind has its default route and its context modules.

Ruling: land, amend, or reject.

## Proposal 2: psyche-context › skills/vision-datom.md

+ A datom shown to a reader stands beside its Ethos type, written `type.<Type>` before it:
+ ```
+ type.Kind { Field Operator Tertiary }
+ type.Kind { Psyche Explorer Quaternary }
+ type.Level Secondary
+ ```

Ruling: land, amend, or reject.

## Proposal 3: psyche-context › skills/vision-model-roles.md

+ A model is shown by its role and level; its number appears only where a version is pinned, and an alias keeps a version worth keeping.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
~~~~

## 2.2 The living's comments, verbatim

No comment on the 4th edition was found anywhere in `flows/*/vision`, `notion`, logs or reports. The comments below are on edition 1 («Subflows», comment date 2026-10-14, relayed by the Psyche Core Tertiary 2026-10-15) and one render complaint on the ed. 3 page (2026-10-16). Proposals 1, 2, 3 of the 4th edition are the carried remainder of those comments (the edition itself says so).

**Source:** `d68c82/vision/flow.md` lines 182-193 (comment of 2026-10-14 on «Subflows» Proposal 1; relayed 2026-10-15)

~~~~text
## A subflow's kind depends on its use

Relayed by Psyche Core Tertiary, 2026-10-15; the living's comment of 2026-10-14 on «Subflows», Proposal 1, the heading "A subflow is the same kind of flow as its main flow".

> No, the same. The subflow is not the same kind of flow as the main flow. The subflow's kind depends on its use so we need to define roles or tasks, or domains, so we can even compose them.
>
> Probably we should have three things, one of which could be the aspect:
> - Is it a psyche? Does it deal with thinking? Is it mind? Does it deal with documentation, tools, and changing codebases for merge requests or for audit reviews?
> - Field, which deals with debugging, system audits, system search, and things, so that each of these has its default suggested route and basic context modules that are appropriate for this kind of task. How do we want field flows to query the system? Let's build our own tools there, maybe around the field.
> - The field CLJ/CLI prototype that is based on an emulated Nexus architecture of EDN payloads, so that essentially everything can be written as one or the other configuration of an Ethos-based specification language in EDN off the bat (with basic Clojure architecture and stack), which is really easy to code on, deploy, and for machines to think in terms of an analog to [protobuf]-like language.

-- psyche, STT. Transcription corrected: "protos-like" → "protobuf-like"; "No, the same" kept [sic].
~~~~

**Source:** `d68c82/vision/flow.md` lines 170-180 (comment of 2026-10-14 on «Subflows» Proposal 2 (specialties table); relayed 2026-10-15)

~~~~text
## Subflows by role and by level

Relayed by Psyche Core Tertiary, 2026-10-15; the living's comment of 2026-10-14 on «Subflows», Proposal 2, the specialties table.

> These would all just be redone by role and by level. Secondary is the highest subagent, of course, and then tertiary and quaternary.
>
> Let's have some basic roles instead of writer and reader. ... Let's split this up into these context modules. In these context repos, like psyche context, mind context, and field context, we don't write skills. There's no skills directory. Let's refashion that so it's by type. ...
>
> This is all basically in ethos code, with implied equivalent [Clojure], which we need to draft on also: what the equivalents look like, with some examples and actual code in a knowledge review.

-- psyche, STT. Transcription corrected: "closure" → "Clojure".
~~~~

**Source:** `d68c82/vision/seats.md` lines 53-59 (comment of 2026-10-14 on «Subflows» Proposal 2 (depths line); relayed 2026-10-15)

~~~~text
## Model numbers stay out of view by default

Relayed by Psyche Core Tertiary, 2026-10-15; the living's comment of 2026-10-14 on «Subflows», Proposal 2, the depths line naming claude-haiku-4-5 and gpt-5.6-luna.

> All these model numbers are obsolete. Plus we shouldn't make the user interface expose the model number by default. Most users will be oblivious to the model number. It'll just be whatever is the default at that moment. We will at some point specify model numbers of course and then we might even have aliases sometimes when we want to keep some versions because it's interesting.

-- psyche, STT.
~~~~

**Source:** `d68c82/vision/ethos.md` lines 75-81 (comment of 2026-10-14 on «Subflows» Proposal 2 (the read-minimal line); relayed 2026-10-15)

~~~~text
## A datom is shown with its Ethos specification

Relayed by Psyche Core Tertiary, 2026-10-15; the living's comment of 2026-10-14 on «Subflows», Proposal 2, the line { read minimal «One known question, one line back.» }.

> This syntax is wrong because these should be variants so they should be capitalized and never show a [datom] without its ethos specification, which can just use the prefix `type`, right? We can create an inline syntax for an ethos object and an example of it, or more than one example of it.

-- psyche, STT. Transcription corrected: "datum" → "datom".
~~~~

The hub's own summary line of those comments (d68c82/log.md, section dated 2026-10-15), and the render complaint on ed. 3:

**Source:** `d68c82/log.md` lines 1398-1399 (the Subflows sentence is inside this section)

~~~~text
## 2026-10-15 — Book comments relayed by the Tertiary
Flow Nexus: P1 lands except the sentence on starting a new topic on the costliest model, re-proposed smaller in the next version; P2's Ethos paragraph "This is good"; the diff on the dependencies line is wrong (vision-flow kept). Chronos: Decimal → a Rust-imported type vector; sign and nakṣatra derived from an arc. Subflows book: model numbers obsolete and hidden by default; roles by role and level; a subflow's kind depends on its use (P1 heading rejected); variants capitalized, a datom shown with its Ethos type. Open books: "Test", "This is good." Vision logged in books, ethos, context-modules, chronos, seats, flow; notion in notion/ethos.md.
~~~~

**Source:** `d68c82/log.md` lines 1525-1525 (complaint about the ed. 3 page rendering)

~~~~text
## 2026-10-16 — The living (screenshot via Tertiary): «Subflows» P2's Ethos code renders as one run-on serif paragraph. "something went wrong there. fix and get secondary to propose a vision fix". Diagnosis and fix dispatched; vision line to propose.
~~~~

## 2.3 Ruling and landing

Rulings: none found for the three proposals of the 4th edition, nor for the same lines in ed. 3. The hub log lines on the editions:

**Source:** `d68c82/log.md` lines 1411-1412 (d68c82 log)

~~~~text
## 2026-10-15 — Subflows ed. 3 composed (kind = aspect, role, level; typed datom form; context by type; model numbers hidden)
Ethos checked by ethos-zero 16.0.0; Clojure run true/false under bb 1.13.219. Files in scratchpad-subflow-kinds/. Published fresh, since ed. 2 carries comments. Asked Field to add "never stash or reset the shared working copy" to the write roles' shared context.
~~~~

**Source:** `d68c82/log.md` lines 1995-1995 (d68c82 log, 2026-10-16T12:35:55-06:00, the 4th edition is published in "Redo batch 3")

~~~~text
- 2026-10-16T12:35:55-06:00 Redo batch 3: Subflows 4th 22Ppun, Situation 2nd Sdeia, Chronos 3rd TDzS3V, Compensation core 2nd BpTinC, Flow Nexus whole 2nd 9qkgFa. It sent Chronos design defaults (Rational angle, apogee names, no open watches, contextualizer) as decided; told Field to hold them for the Chronos design metaflow. Conflict: Flow Nexus 2nd P9 removes the Flow example that Ethos/Nexus/Chronos P13-15 edit; vision-chronos path differs.
~~~~

Landing: nothing of the three proposals is on origin/main. Checked: `git grep` for "kind is its use", "Quaternary" in vision-flow wording, `type.Kind`, `type.Level`, "version is pinned" across `vision/` returns no match for the proposed sentences; `vision/model-roles.md` still carries the layer-to-model table with model names (Fable, Opus, Sonnet, Haiku, Astra, Sol, Luna), and `vision/datom.md` has no `type.` listing. Related and already landed (the 4th edition says the folders of context modules were settled elsewhere): `e1a300e` "vision-context-modules: a module declares its placement" (2026-10-15) and `8bf1b25` "vision-context-modules: the folder names the type" (2026-10-15), then `53f68b6` (2026-10-16).

Current text of the file Proposal 3 targets:

**Source:** `psyche-skills origin/main:vision/model-roles.md` (current content)

~~~~text
---
description: Which model thinks, designs, delegates or speaks to the living, and in which metaflow, is decided, or a model is named natively.
dependencies: []
---

## Roles are explained by layer, not by model

Roles are explained by layer, not by model; one skill maps layer to model.

| Layer | Claude (Psyche) | OpenAI (Mind, Field) |
|---|---|---|
| Primary | Fable | Astra |
| Secondary | Opus | Sol |
| Tertiary | Sonnet | Luna |
| Quaternary | Haiku | Luna, low effort |

Every metaflow runs at medium effort, except the OpenAI Quaternary.

## Delegation ceiling

Each layer has a ceiling on what subflows it may launch. Conservative by
default: prefer the lower layer.

### OpenAI side

Luna launches only Luna. Sol is not
launched lightly; it is getting expensive. Astra launches Sol and Luna — try Luna first. Astra is main-flow only: no flow ever
launches an Astra subflow.

### Claude side

Sonnet launches Sonnet and Haiku. Opus launches
Sonnet and Haiku, and sometimes Opus, but rarely. Fable launches Opus and
Sonnet often, and Haiku for small jobs. Fable is main-flow only: no flow
ever launches a Fable subflow.

## One declaration sets the model everywhere

The model is declared once, as typed configuration in Flow, mutated only
through the meta wire. Skill variables carry that value by name into every
skill, launcher and brief. Nothing else holds a model name, so a launcher
never writes one by hand and no flow is started in a metaflow by accident.

## Native names use aspect, topic and layer

Every native main session is titled `{ <Aspect> <Topic> <Layer> <FLOW_ID> }`.
The layer selects the configured model through the table above, so the
title names the layer, never the model.

Horizontal communication joins aspects at the same layer.
Vertical communication stays within one aspect and normally advances one layer
at a time.

Aspect, topic, layer, exact model identifier, Flow ID, and native binding
remain separate typed facts. The title grants none of the identity,
authority, availability, or routing those facts establish.

Horizontal routing selects the unique eligible cell in the target aspect at
the sender's layer.
Busy is still
eligible.
Multiple bindings for one cell are an unresolved conflict, never fanout.
Resolve the binding
immediately before each attempt.
~~~~

## 2.4 Later records on the same subject (after the 4th edition, 2026-10-16 12:35, unless dated otherwise)

The `type.` spelling in Proposal 2 conflicts with these comments of 2026-10-16 19:08-19:20 (a variant is capitalized, `Type` not `type`, and the type ethos form changed):

**Source:** `65f93a/vision/ethos.md` lines 2-36 (2026-10-16 19:08-19:20)

~~~~text
## Comments on «The Ethos vision, 3rd edition»: two books; short-term marking; datom proposals; the variant specification as an ordinary datom; Type capitalized

Context: comments of 2026-10-16, 19:08 to 19:20, relayed by Psyche Core Secondary with anchors (flows/d68c82/vision/ethos.md, last section).

> "I've commented on the Ethos vision and it probably needs to be two books out of that, one of which is an Ethos syntax modification proposal. The other being the same thing being redone, adjusted for my comments obviously"

Context: on "Chronos is the example project built with them: the golden example from which Flow is implemented properly, then the other nexuses."

> "The first part is good. The second part is only good after you change it to make it explicitly short-term, in the sense that this truth might change. Maybe there's a particular term for this. Maybe the golden example is not going to stay Chronos and Flow forever and eventually even saying that we're doing this to develop Flow will become obsolete. So we need to mark anything that could at some point become stale."

Context: on "A type ethos opens with type and defines a single type."

> "I guess this would be the only payload that doesn't have a brace after its variant. It would just be inline dotted. It would say `type.` and then it would be the name of the type and then it's its specification."

Context: on "A datom is never shown without its Ethos specification."

> "Well we should say a new [datom] or a [datom] proposal. Obviously if we're using a common [datom] that's in production, then its specification will be in a knowledge module.
>
> Also I want Ethos, Opus, and Fable involved in redesigning. I want to get rid of the exception and change the exception from an actual syntax change that makes everything complicated to a formatting change that makes it simple.
>
> For the variant of an Ethos specification, as we had it before, in a `where` we would remove the outer braces of the struct of that variant of that file. Now I want the braces to be there explicitly and the variant to just be the variant, then the `.`, then the `{}`, but we'll make that on its own line. We won't indent the first inner object unless there's more than one variant and one iso variant. I don't know if we'll allow vectors of variants or whatnot.
>
> This would simplify the code a lot. We would just always expect a traditional datom payload for the Ethos specification, with each different variant having a different shape."

Context: on the type-ethos code example ("CommitMessage").

> "Actually looking at this now, I even want to modify the spec of Ethos. In that other proposal we'd also make it so that when there's a dotted form, there can be a space after it. That way we can split it up onto multiple lines.
>
> Instead of the brace opening on the same line as the dot, we can make a new line and then open the brace. Or if there are several dotted variants in a row, we can make an indent, a new line, an indent, and then the next name, and then another dot. We could even make a new line there again.
>
> That way we don't force things to expand to the right. In this type definition it could be `type.new indent` and then the type, which could be more aesthetic or better to read. I think it would be easier to quickly get the visual impression from that formatting."
>
> "Oh and this is very important: in this code `Type` should be capitalized because it's a variant. All these variants need to be capitalized. This is obligatory. It should be because it's interpreted by the ethos that only uses capitalized symbols for variants."

-- psyche, input mode not shown, book comments, relayed by Psyche Core Secondary. Transcription corrected: "datum" → "datom".
~~~~

**Source:** `65f93a/vision/ethos.md` lines 38-105 (2026-10-16 22:16-22:30)

~~~~text
## Comments on «The Ethos syntax»: real code only, traits declared, Fable involved; the dot and the brace (2026-10-16, 22:16–22:30)

Context: spoken to the Psyche core Tertiary after commenting.

> "I commented on the ethos syntax and there's a lot of garbage. The code is fucking garbage so I want all the books redone because obviously the ethos is going to be wrong everywhere.
>
> Also we need to get serious about ethos traits because I really don't see any of them and it's like you don't want your programs to do anything. If there are no declared traits for these types, these types can't fucking do shit. It means you want a system that does nothing. If you show me another thing that has no [trait], you're showing me a system that doesn't do anything.
>
> Get Fable involved, stop being so retarded, and make systems that actually do things."

Context: Proposal 1, "braces open on their own line, under the variant; the first section sits on the brace's line".

> "No not quite. The braces don't open on their own line. It's just usually canonical to make a new line because, actually, you don't have to open the brace on a new line. I didn't say that. I said that it should be possible in the syntax to do that but that the new line really doesn't need to be for the brace.
>
> It's just that we do it on a non-indented new line, generally in files, because we don't need the indentation. We don't want too much indentation and the first variant is really just giving us the type of that file unless we do start supporting a vector, in which case it's still going to have a variant.
>
> It's not an invariant like you said it is. It's just usually good form but it's not necessary."
>
> "And no you would not put the brace and the first section on the same line. That's the whole point of why you make a new line after the brace actually. But if it's just a single type then there are no breaks because it's just one thing."

Context: Proposal 1's Library example, indented under the brace.

> "See here, you did it all wrong. You did make an indentation when I said... My whole point was the only thing I wanted to say. You missed my entire point, which is: no indentation for that first struct. Do you understand what I'm saying? I don't know why I'm asking you because you're not going to respond like that. Yeah that's what I'm trying to say."

Context: Proposal 2, "A space and a line break may follow the dot".

> "Not a space and a new line, just any kind of space or new line, any amount of space. The dot doesn't care if what comes after is right next to it or if there's a space, a new line, a tab, or any number of spaces."
>
> (On its Observed.Locks example:) "Yeah this example is good."

Context: Proposal 3, the type ethos with a one-variant CommitMessage enum, and "A type ethos may carry one or more examples of its datom."

> "This is invalid. We cannot have an enum with only one variant and I don't understand. I don't think your last paragraph is good. When you say a type ethos may carry one or more examples of its [datom], I don't know what you mean by that. There's no logic there. There's no foundation for what you're saying.
>
> I think you're confused because I said, "If you show me a new [datom], you can show me the type." Now you think that that means... I don't know, you're just fucking hallucinating bullshit. Do you understand what I'm saying?
>
> This is bullshit: you think that you're forcing the jigsaw puzzle pieces together. You're smashing them all. You're just breaking them all by trying to fit shit together that has absolutely nothing to do with what you're trying to explain. You're explaining the vision and then... I'm really tired of this kind of behavior where you just put bullshit together. You just try and fit everything together that doesn't fit together."

Context: Proposal 4, "Every variant is capitalized, a root's variant and `Type` included".

> "You don't need to say "type included." Why the fuck do you say "type included"? That just looks stupid. Stop talking like a retard."
>
> (On its examples:) "Your examples suck 'cause they're wrong. Anything that's wrong, anything that is not canonically written, or just a piece of it is just garbage. Absolutely fucking confusing fucking garbage. Do not confuse everybody with your bad, incorrect, shitty examples."

Context: Proposal 5 (Type is no exception) and Proposal 6 (whitespace after a separator).

> "This section is good."
>
> "This is good."

Context: Proposal 7, a canonical print that breaks after the dot, two spaces per link.

> "No I don't want to make this canonical. Your example is garbage because it's mixing things which cannot be mixed together. Stop making any kind of code that could not work in practice. These are wrong.
>
> We have to stop completely, absolutely: never, ever, ever make an example that is not real code, ever, ever fucking again. Never, ever, ever.
> - Golden fucking rule
> - Top of the list
> - Full book on this topic
>
> Stop giving me bad code ever, never, ever, ever, ever, ever. I want to see bad code ever, ever"

Context: Proposal 8, a new datom shown with its specification; a production datom's specification in a knowledge module; the example Reply.[ Accepted.Integer Pending ].

> "There's a lot of bullshit here. This specification may or may not be in a knowledge module. It depends if it's implemented so why are you saying that? You don't seem to understand the principles that you should understand before you start explaining this to me. Let's go back to those principles.
>
> Your example is bullshit because every ethos needs a variant and your ethos has no variant so it's fucking garbage, just like most of the code in here. You have to stop writing ethos like it's like you're writing it without caring. It's like you don't care. It's like you're just making shit, slop, shit, garbage, filth. Stop giving me fucking filth, you filthy bastard."

-- psyche, input mode not shown, book comments, relayed by Psyche Core Secondary (anchors as in flows/d68c82/vision/ethos.md). Transcription corrected: "trade" → "trait"; "datum" → "datom".
~~~~

Roles and models (2026-10-16, timestamps in the headings):

**Source:** `d68c82/vision/flow.md` lines 203-206 (2026-10-16 11:25 (earlier than the 12:35 publication of the 4th edition, kept because it is the order for role files))

~~~~text
## 2026-10-16 11:25 Roles defined as datom data in their own repository

"These roles are going to get defined in role definition files with datom syntax on an ethos-specific specified object. As if we were creating payloads for the Flow Nexus, we're creating all of this data. It goes in a different directory than the cluster data but it's a different repo. It's how we configure our meta flows and this shared Metaflow infrastructure is a more general public one."
-- psyche, typed.
~~~~

**Source:** `d68c82/vision/flow.md` lines 208-211 (2026-10-16 11:29)

~~~~text
## 2026-10-16 11:29 A role may call a subagent model one rung up

"Let's create a special situation where this quaternary, this haiku model, can actually call sonnet so we can override the allowed subagent models per role. Let's make that part of the specification. This will be the first exception we create that is allowed to call a non-standard one rung up higher than itself. It'll just call the sonnet subagent with an illustrator and the illustrator is an actual subagent file."
-- psyche, STT.
~~~~

**Source:** `d68c82/vision/flow.md` lines 213-216 (2026-10-16 11:32)

~~~~text
## 2026-10-16 11:32 Refreshing the illustrator: fresh over compacted; feedback goes to modules

"He could be either recompacted or restarted regularly because compacting it at some point is necessary unless we auto-compact when it's idle in order to use the cache. I don't know. Maybe we can do a little study on that and what might be the best. If you start fresh then it's just how to illustrate, which is good. If you compact then there are all these illustration jobs that don't really matter. They don't really make it smarter if it has done more illustrations unless there's feedback, in which case it should change the context modules and the new flow would be better trained. This is where we want to finally [iron] out how to easily refresh and reliably refresh flows. This could be a really good Metaflow to practice with."
-- psyche, STT. Transcription corrected: "yarn" → "iron".
~~~~

**Source:** `d68c82/vision/context-modules.md` lines 282-288 (2026-10-16T18:15)

~~~~text
## Role modules are components, not skills

Context: comment on «Short hashes», Proposal 4 (a line for tools/primary-committer/brief.md), 2026-10-16T18:15.

> "This is in the wrong place. All the context modules, absolutely all of them, need to live in the three main aspect context module repos. Some of these are roles. Let's rewrite the tool to do that and have these different role modules that don't become skills but are components to build certain main flows and subagents. Then let's get somebody to write a book that explains this whole design in a vision as it's being implemented now so that I know what's being implemented and I can correct it."

-- psyche, typed.
~~~~

**Source:** `d68c82/vision/flow.md` lines 218-226 (2026-10-16)

~~~~text
## Every representation of a flow is named by its datom struct

Context: spoken to the Psyche Core Tertiary on 2026-10-16, after commenting on «Drawing ideas»; relayed to d68c82.

> "I commented on drawing ideas and you should be restarted as psyche core tertiary. Don't forget that the topic name is uncapitalized so core is uncapitalized, ethos should be uncapitalized, and all of these topics should be uncapitalized.
>
> It looks like the format that's used for Codex is different. Maybe it's because of how I'm seeing it and there are different applications but I like the name of every pane, every tab, everything that represents this flow to be just this triple field struct in datom format (or I guess it's quadruple with the flow ID)."

-- psyche, typed.
~~~~

**Source:** `d68c82/vision/books.md` lines 241-246 (2026-10-16 11:43, comment on «Metaflow roles»)

~~~~text
## 2026-10-16 11:43 No noise; one simple view at a time

"I'm tired of reading noise and I want a book solely on that to make sure that we word things properly from now on for any presentation: how they should be done." ... "I don't want any noise in my books. I don't want to be distracted by anything. They kind of look like children's books except that they talk about really sophisticated concepts, just one simple view at a time."

Context: comment on the opening paragraph of «Metaflow roles» (machine branch status and a vision file path), said to apply to all recent books.
-- psyche, typed.
~~~~

**Source:** `7c89aa/vision/books.md` lines 33-43 (2026-10-16, comment on the Metaflow roles book)

~~~~text
## Presentations for the living are non-technical; technical references sit in a separate field of a typed struct (2026-10-16)

Context: the living had commented on the book on Metaflow roles and then spoke this to the Tertiary.

> I commented on Metaflow roles and it doesn't really have to do with that but I want my comment applied to all of the recent books. I'm tired of reading noise and I want a book solely on that to make sure that we word things properly from now on for any presentation: how they should be done.
>
> Presentations for the living, they're non-technical. All of the technical references go in a separate section so the model can, in one response, give all of the technical stuff and the presentation in two different fields of the datom struct (that we are kind of pseudo-specifying here by getting a machine to start behaving that way).
>
> Let's review that ethos, that spec on what kind of responses can be given that optimize for a clear answer and a more technical reference part. The type obviously is going to be the first variant that opens the struct.

-- psyche, typed.
~~~~

---

# Book 3: How a metaflow is named on the wire

- Path: `flows/73ada7/books/7-address.md`
- Title: «How a metaflow is named on the wire» (Presentation line). Published 2026-10-09 as artifact JyL9DpeoJ3XqutJcXfpFko (73ada7/log.md line 95; 445410/log.md line 183). It is the book the logs call "N4". There is no edition after the first.
- Proposals: one, "D1. What names a metaflow, in vision-flow", target `psyche-skills/skills/vision-flow.md` (now `vision/flow.md`), three options (a), (b), (c) and an (d) "Amend, by line". Plus a closing "Voice" section that restates the choice.
- Ethos code blocks: 0. The book writes short names inline (`Psyche.{ core Secondary }`, `Lock.Metaflow`, `Deliver.{ Lock Sender Request }`) but has no fence.

## 3.1 The proposal, verbatim (book lines 4-36: the case, D1 with its three options, the ruling line, and the Voice section)

**Source:** `73ada7/books/7-address.md` lines 4-36 (whole body)

~~~~text
## The case

Message hands Flow a request for a metaflow in two steps: it asks for the lock with Lock.Metaflow, then hands the request under it with Deliver.{ Lock Sender Request }, where the Lock is a metaflow with the time it lapses and the Sender is the sending metaflow. So the metaflow is what both inputs carry. Flow's buildable design declares one Metaflow in its Library: a variant per aspect, Psyche, Mind or Field, each holding Details, which are the topic and the layer together with the metaflow's State (awake with its current flow, asleep, or ended), its Past flows and its Queue of waiting requests (flows/f5a6e9/reports/flow-buildable-design.md:56-71). Yet where a metaflow is named, in Launch, it is written short, aspect, topic and layer only, as in Psyche.{ flow Primary } (the same design, 265-270), and Message's design sends the short form, as in To.Mind.{ nexus Secondary } (flows/73ada7/reports/build/message-design.md:293 and 518-521). One name stands for two shapes, and the two designs leave it unseparated. vision-flow already writes a flow's title from its aspect, topic, layer and flow id, and writes a voice as an aspect with a rank, Psyche.Primary, with no topic. The Message and Flow these designs describe are in development; neither is in production. That under the present declaration a Lock or a Sender would have to carry a State, a Past and a Queue, which Message neither knows nor holds, is this flow's inference.

## Distillation

### D1. What names a metaflow, in vision-flow

Target: `psyche-skills/skills/vision-flow.md`, the paragraph at line 24, which opens "Every flow has a topic; a flow with no special topic has the topic core" and closes "A flow's title names its aspect, topic, layer and flow id". Nothing in it is removed; a sentence is added at its end. The paragraph before it says voices are addressed by name and a flow id is for the ledger; the one after it gives the routes to the vision-aspects skill.

**Option (a), the address is its own type, the record another.**

Added: A metaflow is named by its aspect, topic and layer, Psyche.{ core Secondary }, and that name is a type of its own, the metaflow's address; what Flow keeps of a metaflow, its state, its past flows and its queue, is a separate record found by that address. Lock, Deliver and every other request that names a metaflow carry its address.

Rests on: flows/d4ae97/vision/flow.md:165-183 (2026-10-08), on a flow being aspect, topic and layer, the aspect its first field, a struct; flows/4ddfe1/vision/flow-names.md:3-7 (2026-10-09), on addressing every metaflow as psyche secondary or psyche primary; flows/01e496/vision/flowIdentity.md:3-9 (2026-10-02), on flows addressable by their continuous name; flows/41fa34/vision/clojure-flow.md:4 and flows/d4ae97/vision/flow.md:153-158 (2026-10-08), on metaflow addressing by metaflow name; flows/f5a6e9/vision/flow.md:27-33 (2026-10-07), on referring to metaflows and keeping the current flow and maybe its predecessor in the metaflow's memory; flows/d4ae97/notion/flow.md:12-21 (2026-10-08), a notion, on a metaflow record without vectors, of one size, pointing at the current flow, with other registries holding other data. With this, Lock.Metaflow takes the three fields and Deliver's Lock and Sender each carry them; that the Library's Details then splits into the address and a Memory record keyed by it, whose name the ruling would give, is this flow's reading.

**Option (b), one metaflow in a simple and an extended form.**

Added: A metaflow has a simple form, its aspect, topic and layer, Psyche.{ core Secondary }, and an extended form that adds its state, its past flows and its queue; both are the same metaflow, defined in ethos as forms of one type. Lock, Deliver and the common requests use the simple form; the extended form is for debugging and for other components.

Rests on: flows/edf227/vision/signalForms.md:3-7 (2026-10-03), on the simplified form, without the flow id, being the same data in another container, defined in ethos in Signal as formats, the simple form for common queries and the extended for the technical side; flows/62022e8f/vision/multiFormConcepts.md:3-12 (2026-08-30), on one concept written at different arities with fields omitted by arity, a simple and a complex form; flows/b7ba00/vision/messaging.md:39-56 (2026-09-26), on simple and full forms of a message and of a psyche. No record or landed skill this flow read gives the ethos form of one type at two arities, and whether ethos-zero accepts it is not observed here.

**Option (c), one Metaflow as it stands.**

Added: A metaflow is a variant of its aspect holding its details, its topic, its layer, its state, its past flows and its queue; a request that names a metaflow carries it whole.

Rests on: flows/73ada7/notion/metaflow.md:3-9 (2026-10-09), a notion, on every metaflow being a variant of psyche, mind or field, the struct holding its details such as the name of its topic; flows/f5a6e9/vision/flow.md:63-68 (2026-10-07), on psyche, mind and field having similar payloads, the variant one of the fields. This is the Library as Flow's design declares it; that it puts on every Lock and Sender data only Flow holds is this flow's inference.

**Ruling D1.** (a) A separate address type. (b) One type, simple and extended forms. (c) One Metaflow as it stands. (d) Amend, by line.

## Voice

One choice. Message asks Flow for a lock on a metaflow, then hands the request under that lock, so both name a metaflow. Flow's design has one Metaflow that holds its topic and layer and also its state, its past flows and its queue, while the launch and Message write only aspect, topic and layer. A makes that short name a type of its own and keeps the rest in a record found by it. B keeps one metaflow with a simple and an extended form, as you said on the 3rd for the form without the flow id. C keeps the one full Metaflow. Which one? This flow's reading: under C, every lock would carry a queue Message does not have.
~~~~

## 3.2 The living's comments, verbatim

No comment from the living on this book was found (searched vision and notion of every flow for the book title, "N4", "Lock.Metaflow", "Deliver", "address type", "simple form", "extended form"). The living's words that the book itself says its options rest on follow; they are earlier than or contemporaneous with the book, and they are not comments on it.

**Source:** `edf227/vision/signalForms.md` lines 3-7 (cited as basis of option (b); the record states 2026-10-03T18:01Z)

~~~~text
## The simplified form (no flow id) is for common queries; the extended for the technical side; defined in ethos in Signal as formats
Comment on 5578cc's «Your answers on Flow ids in words, and what follows», at "The ledger keeps every flow's real id."
> "This is a different representation of the same fundamental data. ... This would not so much be a short form but a simple form, right? The simplified version is the part that doesn't have the flow ID. It's the same data, just represented differently, like it's cast into a different container, if you will. This is defined in ethos somewhere in signal as different types of formats that communication can happen in, basically. These simplified formats are what the common queries and responses will use and the more extended version will be for the more technical side (which can sometimes be used with the CLI, but mostly not). It is mostly used for either debugging or for other components to have some kind of more advanced compatibility or feature with each other."

-- psyche, typed, book comment, 2026-10-03T18:01Z, relayed by 6e782c.
~~~~

**Source:** `73ada7/notion/metaflow.md` lines 3-9 (cited as basis of option (c); 2026-10-09, a notion)

~~~~text
## 2026-10-09 — Every metaflow a variant of psyche, mind or field; a struct holding its details, the topic name a new type

Context: thinking aloud on the Ethos structure of metaflows; relayed by 4ddfe1 through 445410 and dcd651, marked a notion. "annex" left as relayed; its sense is unclear.

> I wanna talk about the structure of the Ethos for um, the metaflows. They're going to be, each one uh, variant of either psyche, mind, or field. So all metaflows will essentially have an aspect. And then the struct, will contain their details, such as their- their- the name of their topic, right? Which will be a, a new type which I talked about yesterday, which is a... annex [sic] uh, I'm trying to come up with a name, maybe Opus actually made some suggestions or Fable.

-- psyche, STT, 2026-10-09, relayed by dcd651.
~~~~

**Source:** `4ddfe1/vision/flow-names.md` lines 1-6 (cited as basis of option (a); the record carries no date, the book dates it 2026-10-09)

~~~~text
# Metaflow names

## Address metaflows without hashes

> I don't want you to read those hashes. What is d4? I don't fucking understand. You mean like, uh... You mean like psyche secondary or psyche primary? I want all the metaflows addressed this way and not with hashes. I don't, I've no fucking idea who [d4ae97] fucking means.

~~~~

## 3.3 Ruling and landing

Rulings: none found for D1 in any log, handover, vision or notion file. The hub logged the book as one of four interface rulings Astra asked for (445410/log.md, 2026-10-09):

**Source:** `445410/log.md` lines 178-179 (445410 log, 2026-10-09)

~~~~text
- 2026-10-09 Astra asked four rulings (N3/F2, N4, N8/F4, N11). F2, F4 already before the living; N4, N11 sent to 73ada7 for books. Build proceeds on first options.
- 2026-10-09 73ada7 drafting N4 and N11 books. No separate F4 book: awake-flow delivery is asked only as ruling 3 of «The Flow Nexus vision» (no duplicate wanted).
~~~~

**Source:** `445410/log.md` lines 183-183 (445410 log, 2026-10-09)

~~~~text
- 2026-10-09 73ada7 published N4 book «How a metaflow is named on the wire»: JyL9DpeoJ3XqutJcXfpFko. All four of Astra's rulings are before the living; told 41fa34. Index update dispatched for N11 and N4.
~~~~

The book's author notes in the following log lines that the Flow side moved on its own (these are not rulings by the living):

**Source:** `73ada7/log.md` lines 105-105 (73ada7 log, 2026-10-09)

~~~~text
2026-10-09 — 9fed42: Flow's design at e17a62ca carries seven new rulings touching Message (Said, Address replacing Details, Lock/Sender/refusals on Address, Send). Whether they are the living's rulings is unverified. Realignment dispatched; the message-test subflow is told to write its tests against e17a62ca.
~~~~

**Source:** `73ada7/log.md` lines 109-109 (73ada7 log, 2026-10-10)

~~~~text
2026-10-10 — Landing: Message design realigned with Flow e17a62ca (bae554), all five Ethos files Checked. None of the seven changes is the living's ruling; they are 9fed42's. Flow's Send drops Up, which pre-empts book 4: raised with 9fed42. The message-test subflow was told to align with bae554.
~~~~

Landing: none of the three options' added sentences is on origin/main. A different sentence naming the metaflow as an address landed on 2026-10-11 in commit `ae0bc79` ("vision-flow: metaflows, the core topic, the flow id, requests, layers, refresh (approved 2026-10-11)"), and the 2026-10-16 commit `455d677` kept it. It is the relevant text now in force (vision/flow.md lines 20, 22, 28):

**Source:** `psyche-skills origin/main:vision/flow.md` lines 20, 22, 28

~~~~text
Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one after another; the flow is its current run, and what is addressed is always the metaflow, never a flow. The default topic is core: the permanent topic, the thing that keeps the machine going, the last topic to stand.
Psyche, Mind and Field have similar payloads, and they go under one: the metaflow, whose aspect is Psyche, Mind or Field.
A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events, learning when a request has entered the flow's context. A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started. A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.
~~~~

D1 therefore stays unruled: the current text says a metaflow is "one address, { Aspect Topic Layer }", which is close to option (a) in naming but does not state that the address is a type of its own, nor that the state, past flows and queue are a separate record found by it. The text also says "Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery", which removes the Lock and Deliver wire inputs that D1 and the book's case are built on (see 3.4, comment 4 of 2026-10-11).

## 3.4 Later records on the same subject (after 2026-10-09)

Comments 1 and 4 of 2026-10-11 on «Flow, whole, in ethos» (875960's book; same words in 9519a1/vision/flow.md). Comment 4 changes the premise of this book: "I don't think that the flow should give the lock to message".

**Source:** `875960/vision/flow.md` lines 11-17 (2026-10-11 20:21)

~~~~text
## 2026-10-11 — the voice concept is gone; the default topic is core, the permanent topic, the last to stand

Comment 1 on «Flow, whole, in ethos», 20:21, at the metaflow paragraph; relayed by core d68c82 through 9519a1.

> No we've gotten rid of the voice concept. Now it's just replaced by the core topic. One thing I did notice, which has maybe been fixed, is that the topic should always start with a small letter. It's uncapitalized. In other words we need a name for that. It's like a datomic name or something: a camelCase identifier. Anyway so far, the presentation proposal is good but we can't take out the voice part. Just replace it by saying that the default topic is `core` and that the `core` topic is essentially the permanent topic. It's the thing that keeps the machine going. It's the last topic to stand.

-- psyche, STT, relayed by 9519a1.
~~~~

**Source:** `875960/vision/flow.md` lines 35-41 (2026-10-11 20:29)

~~~~text
## 2026-10-11 — Flow keeps the lock and delivers; Message asks Flow to send to a metaflow and subscribes to its events

Comment 4, 20:29, at the request paragraph.

> I've actually changed my mind on this. I don't think that the flow should give the lock to message because we need the flow nexus to be the component that delivers the payload because it owns the lock. It can't really give a lock because then, even if it has a timeout, there would be a problematic window when we can't rely on two components sharing a lock. If message wants to send a message, it communicates to flow and flow would take care of the mechanics and then tell message the status. It would also tell message if queued messages have been delivered because a waking message came in and so on. It would just give message the information on what's happening from its perspective. Message would just say, "Okay I want to send a message to this Metaflow." That's what it would tell flow and then flow would do what it does and then respond to message. It might just be like, "Messages queued." Let's say the flow is being refreshed, so the messages are queued for when the flow has restarted. It would have a variant just to express that. Once the message got delivered, message would subscribe to events from flow. When the message gets delivered, message would receive a notification that the message has now entered the context of that flow.

-- psyche, STT, relayed by 9519a1.
~~~~

**Source:** `7c89aa/vision/flow-ids.md` lines 3-9 (2026-10-13)

~~~~text
## Flow IDs almost disappear from the chat (2026-10-13)

Context: the flow had named other flows by their six-character ids in its replies.

> I want everybody to stop referring to the other metaphors [sic] by flow ID. I want flow IDs to almost disappear from the chat. I would like to know who that is, the flow ID you're talking about.

-- psyche, STT. "metaphors" left as heard; the intended word is unclear (possibly "flows"), not corrected.
~~~~

**Source:** `7c89aa/vision/flow-ids.md` lines 19-27 (2026-10-16; the same record sits in d68c82/vision/flow.md under "Every representation of a flow is named by its datom struct")

~~~~text
## Topic names are uncapitalized; every pane and tab is named by the flow's datom struct (2026-10-16)

Context: the living, after commenting on the book "drawing ideas", spoke this to the Tertiary.

> I commented on drawing ideas and you should be restarted as psyche core tertiary. Don't forget that the topic name is uncapitalized so core is uncapitalized, ethos should be uncapitalized, and all of these topics should be uncapitalized.
>
> It looks like the format that's used for Codex is different. Maybe it's because of how I'm seeing it and there are different applications but I like the name of every pane, every tab, everything that represents this flow to be just this triple field struct in datom format (or I guess it's quadruple with the flow ID).

-- psyche, typed.
~~~~

---

# Book 4: Word ids for flows, second edition

- Path: `flows/0c85a3/books/word-flow-id-anatomy-second-edition.md`
- Title: «Word ids for flows — second edition» (Presentation line). Published 2026-10-09 as artifact 329WvCY3Wb5RZ8ZNYtq7ri, source sha256 42b4a4... (445410/log.md, 2026-10-09). The first edition «Word ids for flows» is 8SnQwCA52ReX9UkxYsWAiC (no distillation section).
- Proposals: two. (1) "Add `wordable-clj/ethos/wordable.ethos`", a new file in a proposed flow-id-specific Clojure source home, with the Ethos anatomy, the pinned BIP-39 dictionary, the lower-camel spelling and a regex construction; its ruling line asks to approve the dictionary, spelling and anatomy and to rule on the distillation. (2) "Distillation", target `psyche-skills/skills/vision-flow.md`, insert after the anchor "and is written in words.", one added line.
- Ethos code blocks: 1, lines 11-50 (fenced `ethos`, an `Operation` file with the full type list). Lines 107-116 are a Clojure expression; 153-156 is a text fence holding the added vision-flow line.

## 4.1 The proposals, verbatim (book lines 4-161)

**Source:** `0c85a3/books/word-flow-id-anatomy-second-edition.md` lines 4-161 (whole body, both proposals and both ruling lines)

~~~~text
## Add `wordable-clj/ethos/wordable.ethos`

Removed: none; this is a new file in a proposed,
flow-id-specific Clojure source home.

Added:

```ethos
Operation
[ ]
[ PrefixFromUuid.SessionUuid
  WordIdFromPrefix.FlowPrefix
  PrefixFromWordId.WordIdText
  RegexFromWordId.WordIdText
  MatchPaths.MatchRequest ]
[ Prefix.FlowPrefix
  WordId.WordIdText
  Pattern.RegexPattern
  Matches.MatchSet
  Rejected.InputError ]
[ UuidText.String
  SessionUuid.{ UuidText }
  PrefixValue.Integer
  FlowPrefix.{ PrefixValue }
  WordIndex.Integer
  FirstWordIndex.{ WordIndex }
  SecondWordIndex.{ WordIndex }
  ThirdWordIndex.{ WordIndex }
  DictionaryId.[ Bip39EnglishV1 ]
  FlowWords.{ DictionaryId FirstWordIndex
              SecondWordIndex ThirdWordIndex }
  LowerCamelText.String
  WordIdText.{ LowerCamelText }
  JavaPatternSource.String
  RegexPattern.{ JavaPatternSource }
  PathText.String
  TranscriptPath.{ PathText }
  TranscriptPaths.Vector<TranscriptPath>
  MatchRequest.{ WordIdText TranscriptPaths }
  MatchSet.[ NoMatch
             OneMatch.TranscriptPath
             ManyMatches.TranscriptPaths ]
  UnknownWordText.String
  InputError.[ MalformedUuid InvalidPrefix
               InvalidWordId
               UnknownWord.UnknownWordText ] ]
```

The landed rule in
`mind-skills/skills/operation-clojure-development.md`
requires this Ethos anatomy to specify data and types
before Clojure behavior is implemented.

`SessionUuid` is canonical hyphenated UUID text. Accept
ASCII hex in either case; do not require a UUID version
or variant. `FlowPrefix` is an unsigned integer in
`[0, 2^33)`. Read canonical UUID text-order bytes,
most-significant bit first, and take the first 33 bits.
Do not use platform-specific GUID byte order.

`DictionaryId` identifies a proposed immutable word
list: `bitcoin/bips` commit
`e9d5abfe964db0429e9ca21274439fd981a8a342`, file
[`bip-0039/english.txt`](https://github.com/bitcoin/bips/blob/e9d5abfe964db0429e9ca21274439fd981a8a342/bip-0039/english.txt),
SHA-256
`2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda`.
It has 2,048 sorted unique lowercase English words,
indexed from 0 through 2,047. Carry the license
attribution from the pinned
[`BIP-0039 specification`](https://github.com/bitcoin/bips/blob/e9d5abfe964db0429e9ca21274439fd981a8a342/bip-0039.mediawiki).
This is a proposed selection, not an approved
dictionary.

`WordIndex` is an 11-bit index. `FlowWords` keeps the
three groups in most-significant-first order. Split the
prefix into consecutive 11-bit groups. Render the
corresponding words in lower camel case, capitalizing
the first letter of words two and three. Prefix value
`1` maps to `[0, 0, 1]`, `abandon`, `abandon`,
`ability`, and `abandonAbandonAbility`. This uses the
BIP-39 list only; it is not a wallet mnemonic and does
not use BIP-39 checksum or seed rules.

`WordIdText` accepts exactly three words in canonical
lower-camel form. Reject malformed casing, other word
counts, non-ASCII letters, and unknown words. Decoding
returns only the 33-bit prefix; it cannot reconstruct
the full 128-bit UUID.

`RegexPattern` is source for Java
`java.util.regex.Pattern`. Match only complete basenames
in these two forms: `UUID.jsonl` or
`rollout-YYYY-MM-DDTHH-MM-SS-UUID.jsonl`. The timestamp
is filename syntax only; do not validate its calendar
or clock values. Anchor the pattern at both ends. Use
case-insensitive matching for UUID hex, but keep the
other filename text exact. Do not constrain UUID version
or variant. For each prefix, format its first 32 bits as
eight hex digits and constrain bit 33's nibble to
`[0-7]` or `[89a-f]`. Call `Matcher.matches()` on each
basename. For prefix `1`, this Clojure expression
produces Java Pattern source:

```clojure
(str
  "^(?:(?i:00000000-[89a-f][0-9a-f]{3}-"
  "[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
  "\\.jsonl|rollout-[0-9]{4}-[0-9]{2}-"
  "[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}-"
  "(?i:00000000-[89a-f][0-9a-f]{3}-"
  "[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
  "\\.jsonl)$")
```

`MatchRequest` supplies one word id and paths; no file
is read. Match the basename only, never a directory
component. `MatchSet` reports zero, one, or many
matching paths.
`InputError` distinguishes malformed UUID, invalid
prefix, malformed word id, and an unknown word. The
operations convert UUID text to prefix, prefix to word
id, word id back to prefix, word id to regex, and word
id plus supplied paths to the complete match set.

This adds a prefix label and lookup over supplied paths.
It does not alter six-hex aliases or prescribe title or
registration grammar. A 33-bit prefix can collide; a
match set keeps that ambiguity visible. Canonical
word-ID/title integration is the next increment; this
anatomy does not silently replace current identities.

Ruling: approve the proposed pinned dictionary,
lower-camel spelling, and Ethos anatomy, or specify the
correction. The 33-bit prefix mapping is fixed by the
specified bit order and is not a separate choice.
Also rule on the `vision-flow` distillation below.

## Distillation

File root: `/git/github.com/LiGoldragon/`
Authored source: `psyche-skills/skills/vision-flow.md`

Removed: none.

Insert at line 22, immediately after the exact anchor
`and is written in words.`

Added:

```text
A word id represents the first 33 bits of its
harness id.
```

Provenance: `flows/0c85a3/notion/flow-identifiers.md`,
2026-10-09, relayed by 41fa34.

Ruling: approve these exact `vision-flow` lines.
~~~~

## 4.2 The living's comments, verbatim

No comment from the living on this book was found (searched vision and notion of every flow for "Word ids for flows", the artifact ids, "wordable", "BIP", "33 bits", "dictionary", "word list"). The book names its provenance as the notion below (2026-10-09, relayed by 41fa34):

**Source:** `0c85a3/notion/flow-identifiers.md` lines 2-8 (2026-10-09, a notion, relayed by 41fa34; the book's cited provenance)

~~~~text
## Word-based flow ID — 2026-10-09

Context: exploratory conversion and lookup alternatives relayed by41fa34; implementation/presentation order retained alongside them. Corrected relay supplies [Clojure]; no original transcription pair was supplied.

> I would like the word-based flow ID, but maybe Astra can make a tool, a [Clojure] tool, to do the conversion between the first 33 bits of the identifier we use for the harness and the word thing. It can get a regular expression back so that we can find which session from the list of transcript files we have, or maybe we have a list of the alpha-numerical ID somewhere in the database, or maybe we just make a registry in the database. In the database, we just write this [Clojure]. Let's define it as if we would define the data-oriented design, object data-oriented, kind of like how we design with ethos and stuff. We should have some kind of skill that explains how we want the [Clojure] developed, if we don't already, based on how we do ethos and Rust. The first presentation is an ethos anatomy, and then the [Clojure] code uses that as a guide to create its specification for its data and its types.

-- psyche, relayed by41fa34; original input method unspecified.
~~~~

Earlier comments (2026-10-03, on «Flow ids in words, and seats launched by Flow») that the book's design answers; the second one conflicts with the book's "flow-id-specific" home:

**Source:** `9fb0ad/vision/identifiers.md` lines 31-35 (2026-10-03 per dea0ba/vision/identifiers.md; relayed by 9fb0ad)

~~~~text
## The words are the first 33 bits of the harness's id, reversible, so tools find the transcript from the words
Comment at "1. What the words are."
> "Well it seems to me that the first 33 bits of the actual ID we were using from the harness's ID is what we're using and then converting it into words because then we can go back. Kind of like how people remember their crypto wallet private key with a list of words and then from the words they can get the key back. This utility would allow for tools to deterministically be able to determine which transcript files actually belong to this flow ID by converting the words. Is there anything that doesn't work with that in practice?"

-- psyche, typed, book comment, 2026-10-03T15:59Z, relayed by 5578cc.
~~~~

**Source:** `9fb0ad/vision/ethosLibrary.md` lines 9-13 (2026-10-03, comment on «Flow ids in words, and seats launched by Flow»; relayed by 9fb0ad)

~~~~text
## The word-id library is generic over hash sizes; a kind that yields words
Comment on «Questions on the Ethos library», point 1.
> "No the word ID library that I want is not implemented specifically for Flow ID. It's generic so we can use it for any hashes of any size. We could have a few different types. There's this 33-bit type. Maybe there's a situation in which we don't even need 33 bits. Maybe there's a situation in which we need more so it's a generic type. I don't know. Let's look at the Rust mechanics here and what we can do in terms of reusability. Is this a kind that can yield so we can call the Flow ID method on Flow ID that is `as_words` or something?"

-- psyche, typed, book comment, 2026-10-03T16:08Z.
~~~~

## 4.3 Ruling and landing

Rulings: none found. 0c85a3's own log says the edition was a correction of the first one and that the proposals await approval:

**Source:** `0c85a3/log.md` lines 235-237 (0c85a3 log, 2026-10-09)

~~~~text
## Word-id anatomy distillation correction — 2026-10-09

41fa34 confirmed that the first published anatomy had no revised source and lacked the distillation section required by vision-book. A separate second edition was delegated to deploy, with independent source review by projection_review. The published first edition remains unchanged. Review identified the existing vision-flow word-id sentence as the narrow source target. An initial draft widened the ledger/archive role into addressing a flow; correction requested preservation of the existing role and a proposal limited to the first-33-bit relationship. Dictionary, spelling and anatomy remain proposals; publication is not approval or implementation.
~~~~

Landing: not landed. `git grep` of origin/main for "word id", "33 bits", "BIP" in `vision/` and `intent/` returns nothing, and no `wordable` repository or file is in psyche-skills. The anchor sentence "and is written in words." of the vision-flow proposal no longer exists in vision/flow.md (the paragraph was rewritten in `ae0bc79`, 2026-10-11). The paragraph now in force on the flow id:

**Source:** `psyche-skills origin/main:vision/flow.md` line 26

~~~~text
A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, so a transcript is found from the flow id. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. No flow declares its id: every call to Flow is identified by the calling process. Anybody may call Flow, a flow for its own refresh among them: because the CLI checks the calling process, a flow refreshes itself safely.
~~~~

## 4.4 Later records on the same subject (after 2026-10-09)

Comments on the flow id and the word-built identifier type:

**Source:** `875960/vision/flow.md` lines 27-33 (2026-10-11 20:25, comment 3 on «Flow, whole, in ethos»; relayed by 9519a1)

~~~~text
## 2026-10-11 — the flow id is the harness's session id hash, so a transcript is found from it

Comment 3, 20:25, at the flow-id paragraph; a question, answered by this flow.

> We need the hash from the harness so we have to start the harness before we get the flow ID, I think. I don't know why this got turned around here unless we're not using the harness hash anymore. There are different parts of the session ID depending on the harness, which is supposedly random, and that's what we're using. I don't know why now the proposal is that we create a hash before. We've been using the session ID hash so that we can find a transcript easily from the flow ID. Is my idea stupid somehow or why do you think it's better to not do that?

-- psyche, STT, relayed by 9519a1.
~~~~

**Source:** `9519a1/vision/identifier.md` lines 1-11 (comment on «Flow, whole, in ethos» third edition, 2026-10-12 16:12; the record states the date)

~~~~text
# Word identifier

Comment on «Flow, whole, in ethos» third edition, 2026-10-12 16:12, at the item «Name» among the proposed names for the camelCase identifier type.

> Well if we create a special thing and we call it a name or we call it a word, you're never going to know when I'm talking about it. Those are silly suggestions. We need something that somehow embodies what we're trying to do. This is going to be used a lot here so whenever it's like an identifier, a word identifier, or an expression, it will be more than one word.
>
> Wherever we have something like a topic, a particular object that needs to be identified by agents or humans, which is anything that's user-facing that needs to be named through judgment and has to be given a name. Obviously variants are great but we have to recompile everything to add one. It's essentially a variant that is created on demand and is a bit more descriptive. The fact that it doesn't start with a capital is how we differentiate it from variants.
>
> ... It would go in some kind of shared library, maybe the [protos] library, because I think it could be used in more than one place, in more than one dialect. It would also do a check, which is interesting.

-- psyche, STT. Transcription corrected: "proto library" → "protos library".
~~~~

**Source:** `d68c82/vision/naming.md` lines 3-13 (2026-10-10, comment on «Sources and the registry»; relayed by d68c82)

~~~~text
## Registry names are independent of repository names; uncapitalized camelCase names made of words

Context: «Sources and the registry», proposal 3, "What the key reaches", 15:25.

> Well the name of the repo and the name in the registry, in our own memory, our own Nexus memory, doesn't have to be the same. Even I would say it seems we've gone with a hyphenated kebab case (I think it's called) for repo names, which maybe is more canonical or standard, and it's fine. I don't have any problem with it.
>
> In Protos languages like datom and [Ethos] for things that are not types or traits, we are going to use uncapitalized. It's going to be camel case because we do PascalCase for defined objects in the language and we do variants. If there's a string position in datom and it starts with a capital, that's okay because we have a different type that's kind of like a string but it has to be checked whenever we create a new one. This is the Prototypic name or whatever, the prototype name, which is an uncapitalized identifier. It's going to have to be composed of words so we need to put together some kind of fancy check. Well not that fancy, I guess.
>
> That would need a dedicated Nexus because it would need to have a database of words. If we're going to do the word-based identifiers, I'd like to get a book on the runtime size cost of having these things in a certain runtime and how it might be smarter to create a dedicated Nexus for that functionality. We could still just build it into whatever we're compiling into, whatever we're doing for now.

-- psyche, STT. Transcription corrected: "Esos" → "Ethos".
~~~~

**Source:** `7c89aa/vision/flow-ids.md` lines 3-9 (2026-10-13)

~~~~text
## Flow IDs almost disappear from the chat (2026-10-13)

Context: the flow had named other flows by their six-character ids in its replies.

> I want everybody to stop referring to the other metaphors [sic] by flow ID. I want flow IDs to almost disappear from the chat. I would like to know who that is, the flow ID you're talking about.

-- psyche, STT. "metaphors" left as heard; the intended word is unclear (possibly "flows"), not corrected.
~~~~

Short hashes and the move from hashes to words (the first record is 2026-10-01, earlier than the book but is the living's standing instruction on the same thing; the second is 2026-10-16):

**Source:** `fe945a/vision/hashes.md` lines 3-11 (2026-10-01, stated in the record)

~~~~text
## Long hashes in prompts and messages are shortened to six characters, then turned into words

Context: said after the living read the latest startup prompt for Field Sol.

> I've noticed this in the startup prompt and also in a lot of messages but I just saw the latest startup prompt for Field Sol. There are these huge hashes, these huge alphanumeric strings, and I don't want these. They're extremely expensive context-wise. They're like entire paragraphs.
>
> We have to find a good alternative or we have to find the right way to shorten this. First of all shorten the hash. ... We need to develop a way to deal with these, a standard way to write a shortened hash, really 6 characters. How to do it? Probably several lifetimes of working at this rate with this scale, there's never going to be a collision at 6 characters probably. If there is, it won't be so bad usually. Let's go situation by situation but I also want to eventually go into the transformation of these random strings into the word-based standard.

-- psyche, STT, 2026-10-01, fe945a.
~~~~

**Source:** `d68c82/vision/messenger.md` lines 25-31 (2026-10-16T18:14, comment on «Short hashes» Proposal 1)

~~~~text
## Short hashes live in the vision of messaging

Context: comment on «Short hashes», Proposal 1, 2026-10-16T18:14.

> "Let's put this in Vision messaging. If we're landing it in Vision we don't need it in compensation so we can just remove everything that deals with that. Make messaging the default module for all main flows and even some subflows that need to be able to message."

-- psyche, typed.
~~~~

That comment led to commit `f37708c` "Messages carry hashes and identifiers as six characters" (2026-10-16), whose added lines are:

~~~~text
## A hash or an identifier is six characters

A hash or an identifier in a message is its first six characters.
~~~~

---

# Book 5: The caller is witnessed

- Path: `flows/875960/books/8-caller-witnessed.md`
- Title: «The caller is witnessed» (the `#` heading; this file has no Presentation line). Published 2026-10-12 as artifact WpyAThKiwDyUttYHKdX3ZP (875960/reports/books.md item 8; 9519a1/log.md line 76; d68c82/log.md line 289). One edition.
- Proposals: two. Proposal 1, "the shared library, in ethos", target the nexus repository's `ethos/library.ethos` (new, shown whole), with two rulings (1: land and import into Flow, or change; 2: whether a process identity gains a boot field). Proposal 2, "what a Nexus promises about its caller", target `psyche-skills skills/vision-nexus.md` (now `vision/nexus.md`), section «Default clients», with ruling 3.
- Ethos code blocks: 1, lines 28-48 (unlabelled fence; the `Library` file with `Pid`, `Process`, `Ancestry`, `Unidentified`, the `Identifiable` trait and the association).

## 5.1 The proposals, verbatim (book lines 22-72: the Distillation section and the fixture table)

**Source:** `875960/books/8-caller-witnessed.md` lines 22-72 (Distillation section through the end of the file)

~~~~text
## Distillation

### Proposal 1 — the shared library, in ethos

File: nexus repository, `ethos/library.ethos`, new, shown whole.

```
Library                    ; shared by every Nexus
[]                         ; imports: intrinsic only
[  Pid.Integer             ; types
   Started.Integer         ; stat field 22: ticks
                           ; since boot, not time
   Process.{               ; one process identity
      Pid
      Started }
   Ancestry.Vector<Process> ; the CLI first, its
                           ; parents, init last
   Unidentified.[          ; why a chain is not
      PeerMismatch         ; trusted
      Vanished
      Reused
      Malformed ] ]
[  Identifiable.[          ; traits: re-observe a
      identify.[           ; process and its chain
         Result<Ancestry Unidentified> ] ] ]
[  Process.[ Identifiable ] ] ; associations
```

Ruling 1: (a) land it on nexus main and have Flow import it, dropping its own Process; (b) change it first: name what.

Ruling 2: a process identity is a pid and its start ticks, which do not tell one boot from another; a stored binding lapses with the boot it was observed in. (a) boot identity stays outside Process, as now; (b) Process gains a Boot field; (c) yours.

### Proposal 2 — what a Nexus promises about its caller

File: psyche-skills `skills/vision-nexus.md`, «Default clients», after the shared-library line proposed in the fourth edition.

Added: A Nexus witnesses its caller at the moment it receives: the CLI carries the ancestry it read, the first element must be the socket's peer, and the Nexus re-reads the whole chain and refuses any difference. Shells and wrappers stay in the chain. A Nexus promises nothing about a process's later life, and a stored binding to a process lapses with the boot it was observed in.

Ruling 3: (a) land; (b) reword: say how.

### What passes

| fixture | result |
|---|---|
| real socket CLI through a wrapper, wrapper and parent edges kept | passes |
| parent named as peer; unrelated live process inserted as ancestor | refused |
| vanished process; reused pid or ancestor; reparent or reuse between the two observations | refused |
| missing init, cycles, empty claim | refused |
| stat names with spaces, parentheses, newlines, non-UTF-8 | parsed |
| generated association compiles; Ancestry rkyv roundtrip | passes |
| package build, tests, datom tests on Prometheus | pass |
~~~~

## 5.2 The living's comments, verbatim

No comment on this book itself was found. The two earlier comments from which the book was built (both on «Flow, whole, in ethos»; relayed by 9519a1) are:

**Source:** `875960/vision/flow.md` lines 43-49 (2026-10-11 20:32, comment 6 on «Flow, whole, in ethos»)

~~~~text
## 2026-10-11 — no claimed id: the caller is identified programmatically

Comment 6, 20:32, at the refresh paragraph. (Comment 5, 20:30, asked what "weeds no path the writer calls" meant; the sentence was "reads no path a caller writes"; answered, not vision.)

> Well if it doesn't trust the claimed ID, then there is no claimed [ID]. Why would we ask for a claimed [ID] if we can get the [ID] programmatically? If we enforce the caller identification, then we don't need the model to declare its ID.

-- psyche, STT, relayed by 9519a1. Transcription corrected: "claimed" → "claimed [ID]".
~~~~

**Source:** `875960/vision/flow.md` lines 51-75 (2026-10-12 16:07-16:21; comment 4 (16:21) is the shared-library order)

~~~~text
## 2026-10-12 — four comments on «Flow, whole, in ethos, third edition»

Context: comment 1 sits on proposal 1's paragraph «A request reaching a metaflow is one of a closed set of types…».

> This is all good. Land it.

-- psyche, typed, 16:07, relayed by 9519a1.

Context: comment 2 sits on the item «Name» among the options for the camelCase identifier type (ruling 3); he notes it is used across dialects.

> Well if we create a special thing and we call it a name or we call it a word, you're never going to know when I'm talking about it. Those are silly suggestions. We need something that somehow embodies what we're trying to do. This is going to be used a lot here so whenever it's like an identifier, a word identifier, or an expression, it will be more than one word. Wherever we have something like a topic, a particular object that needs to be identified by agents or humans, which is anything that's user-facing that needs to be named through judgment and has to be given a name. Obviously variants are great but we have to recompile everything to add one. It's essentially a variant that is created on demand and is a bit more descriptive. The fact that it doesn't start with a capital is how we differentiate it from variants. You could give a few different shots at how we could call this. It would go in some kind of shared library, maybe the [protos] library, because I think it could be used in more than one place, in more than one dialect. It would also do a check, which is interesting. Maybe this deserves its own full research, especially in terms of Rust libraries and executable size bloat. If you have a library of words or you use an external service, which I'm not a fan of, at least it should look like a word. Oh my God this is a perfect spot for a system1 AI call to use a cheap judgment on: Is this composed mostly? Is this made up of words? Is this a camel-case string made up of words, whether they're proper nouns or not? It's not a problem and then we would have, I guess, a certainty threshold. Brilliant. But then again maybe there's a cheap library that can do a quick check with a fallback on AI. That's also an interesting possibility: if there's something that's cheap, lightweight (in terms of runtime cost) and can, in many cases, give us an answer on whether or not these components are actual words programmatically, and then fall back to the AI in case of a negative.

-- psyche, STT, 16:12, relayed by 9519a1. Bracket [protos] as relayed.

Context: comment 3 sits on «the title of a thread:»; a question.

> What do you mean by thread?

-- psyche, typed, 16:13, relayed by 9519a1.

Context: comment 4 sits on the process object («Instant») in Flow's Library in the ethos file; the last comment, where he stopped reading.

> I see that you have the process object defined in the library for Flow but we should have a shared library that many components, that many nexuses, are going to use. This is because identifying the calling process of a CLI is something I would like to minimize the amount of code that needs to be rewritten for every CLI and increase the ease of cognition when reading the code as to what this is doing. Obviously this is done in the background whenever the CLI is used so none of it is actually user-facing in a sense or configurable. It's just something that happens and it may be on all CLIs. I'm not sure now but it's an interesting topic to eventually develop further. We should get Mind to put together a concept that can test whether or not this can actually work using Ethos and everything. We can test it on Flow. Let's give free rein to Fable and Astra to design something like this and implement it. Flow isn't even on in production so I'm not even worried about merging more into main. I'm also curious why we haven't been able to start using Flow Nexus so far, even though it's been a month or something, so I'd like to get an investigation on that.

-- psyche, STT, 16:21, relayed by 9519a1.
~~~~

The same comment 4, as logged by 9519a1 (shorter):

**Source:** `9519a1/vision/callerIdentity.md` lines 1-9 (comment on «Flow, whole, in ethos» third edition, 2026-10-12 16:21; the record states the date)

~~~~text
# Identifying the calling process

Comment on «Flow, whole, in ethos» third edition, 2026-10-12 16:21, at the process object (its «Instant» field) in Flow's Library.

> I see that you have the process object defined in the library for Flow but we should have a shared library that many components, that many nexuses, are going to use. This is because identifying the calling process of a CLI is something I would like to minimize the amount of code that needs to be rewritten for every CLI and increase the ease of cognition when reading the code as to what this is doing.
>
> Obviously this is done in the background whenever the CLI is used so none of it is actually user-facing in a sense or configurable. It's just something that happens and it may be on all CLIs. I'm not sure now but it's an interesting topic to eventually develop further.

-- psyche, STT.
~~~~

## 5.3 Ruling and landing

Rulings 1, 2 and 3: none found. The author's log states the import is held for the ruling, and records the hub's reading of the next order:

**Source:** `875960/log.md` lines 97-101 (875960 log, 2026-10-12 entries)

~~~~text
Field 41fa34: nexus implementation child eafe26 (branch field/nexus-process-implementation-b8b768) passes clippy and fmt on Prometheus; package/test/test-datom passed on parent 6720af only; Field observes a live Flow process (package flow 0.14) with lineage qualification ongoing; asks that the minimum Start not be diverted into Process import. Claim with receipts. Nothing diverted: the import is held until he rules on «The caller is witnessed» ruling 1.
Astra confirms the same cohort as Field (child eafe26 clippy/fmt; parent 6720af package/tests/fixtures); shared Process behaviour proven within those tests, not a Flow import or deployment; core keeps the minimum first Flow Start ahead; her Luna launch bundle frozen to Field via core. Claim, consistent with Field's.
«The caller is witnessed» published: https://claude.ai/artifact/WpyAThKiwDyUttYHKdX3ZP (skeleton check clean; phone width not rendered). Link sent to 9519a1 for core, Astra told.
Rule via 9519a1 (Primary's CLAUDE.md): only a main flow commits and pushes Primary, in its PrimaryPublish turn; a subflow leaves edits and returns paths; before committing, the main flow checks shared HEAD equals origin/main, commits only its explicit owned paths, pushes without force; a mismatch is reported, never repaired. The waiting publish subflow was told to stop (the harness reports it already gone); a read-only watcher now reports the lock's release and I commit myself.
Living (via core, 9519a1), logged in vision/nexus.md: the three Nexus parts are the bulk of the machine anatomy; make one good nexus with all its types and traits well defined, and Flow is the most needed — "Let's do that." Read as an order: Flow in ethos, whole, is that one good nexus; the fourth edition and «The caller is witnessed» are its current proposals; nothing changes until his rulings on them.
~~~~

Landing: none. Nothing in origin/main `vision/nexus.md` carries the Proposal 2 sentences ("A Nexus witnesses its caller at the moment it receives..."), and the "shared-library line proposed in the fourth edition" that Proposal 2 sits after is also not in the file. The current «Default clients» section (the sentence on identifying the calling process predates the book):

**Source:** `psyche-skills origin/main:vision/nexus.md` lines 46-56

~~~~text
## Default clients

A client is a separate program from the Nexus. For now the default
clients are packaged with the Nexus as separate crates of its
repository, which is a multi-crate repository: one datom-converting
CLI per socket, however many sockets the Nexus has, at least two. A
default client serves bootstrap first, then debugging and testing,
long after production has stopped using it. The meta CLI is named
component-meta.

A CLI turns text into Signal and nothing more: it takes one inline datom, no flags, no subcommands; it identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process, never by a claim. A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.
~~~~

The library itself is, per the log lines above, on a nexus branch (candidate 6720af, child eafe26 on Prometheus), not on nexus main, and Flow does not import it.

## 5.4 Later records on the same subject (after 2026-10-12)

Only one later psyche record touches the same ground: the order that makes Flow the first fully defined Nexus, logged by 875960 on 2026-10-12 (the log line above reads it as making this book "its current proposals"):

**Source:** `875960/vision/nexus.md` lines 3-9 (2026-10-12; relayed by core d68c82 through 9519a1)

~~~~text
## 2026-10-12 — the Nexus parts are the machine anatomy; one good nexus first, Flow

Context: relayed by core d68c82 through 9519a1; bears on «Flow, whole, in ethos» and the Flow Nexus build.

> I think that what I'm making with the Nexus system (the three different parts: the operation, the signal, and the memory, and then how each of these is divided) is essentially the bulk of the machine anatomy: what are the pieces that we need to define in the system? It was something that was instinctively going towards already. As such we could sort of flesh that out more. I think what we really need to do is create one good nexus that has all of its types and all of its traits well defined and then the flow nexus is the most needed essentially. Let's do that.

-- psyche, STT, relayed.
~~~~

No later record on caller identity, ancestry, boot identity or the shared process library was found in the non-archive vision or notion of any flow. Earlier, outside the window: 9993b5/vision/callerIdentity.md (2026-09-17) and `callerIdentity.md` of 93ba9f and b7ba00 (dates not checked). 9519a1's callerIdentity.md is the 2026-10-12 comment quoted above.

---

# Book 6: The Source nexus, second edition

- Path: `flows/058f16/books/source-nexus.md`
- Title: «The Source nexus» (Presentation line; the first section is headed "One Nexus for every source"). The second edition was published 2026-10-10 as artifact HFKGQrnnLZRbAagX12r4VM (058f16/log.md line 33; 058f16/handover.md line 7). The first edition was artifact JdvPT3naG5WvYpGwotdeGK (058f16/log.md line 28).
- Proposals: eight. D1 the new skill `psyche-skills/skills/vision-source.md` shown whole (now it would sit at `vision/source.md`); D2 the datom file and its own repository (variants 1-3); D3 what bytes are hashed (1-3); D4 what a local snapshot includes (1-3); D5 one registry or several (1-2); D6 who reads the datom files (1-2); D7 where the shared library lives (1-2); D8 the shared library's types in Ethos. Each carries its own "Ruling" line.
- Ethos code blocks: 1, lines 312-325 (fenced `ethos`, the `Library` file in D8). D1 is a Markdown skill file shown as `+` lines, not Ethos.

## 6.1 The proposals, verbatim (book lines 42-331: the Distillation section D1 to D8)

**Source:** `058f16/books/source-nexus.md` lines 42-331 (whole Distillation section to the end of the file)

~~~~text
## Distillation

### D1. The Source nexus, a new skill vision-source

Target: `psyche-skills/skills/vision-source.md`, a
new file, shown whole. It distils the comments of
2026-10-10 on «Sources and the registry»
(flows/058f16/vision/source.md). The design's
answers to the questions below land in it as D2 to
D8.

Added, the whole file:

+---
+description: The Source nexus, its registry of sources, their hashes and fetchers, and the shared sources library.
+dependencies: [vision-nexus]
+---
+
+## One Nexus for sources
+
+The Source nexus serves the sources of every component, so the sources aspect is fixed in one place. To get a source is to send the Source nexus a source request.
+
+## The registry
+
+The Source nexus keeps a registry of sources. An entry reaches its source through a backend fetcher, a Git repository at a revision or a local path on a given host, and carries the source's own Blake3 hash.
+
+## Assembled from repositories
+
+The registry is populated from datom files kept in repositories, each updated by whoever updates its repository, and loaded together into the full registry. The registry is updated atomically.
+
+## The hash verifies
+
+The hash verifies that the files are the right files when they are used. A store for hash-addressed files, which knows what to store, how to fetch it, and what Git already holds so nothing is stored twice, is a later lane.
+
+## The hash covers the whole snapshot
+
+A source's hash covers the whole snapshot of its repository at a revision, as Nix does, without the Git subdirectory. When the source changes, its hash changes.
+
+## A shared sources library
+
+The components that use sources share a library of source types, including the objects a Memory stores for a registry of sources. A component refers to a source by name, so only the Source registry changes when a source's content changes.
+
+## A registry name
+
+A source's registry name need not be its repository's name. Repository names stay kebab-case.
+
+## Sources
+
+058f16 source
+d68c82 source
+081064 ethos
+23824a sources

(One set of comments, 2026-10-10, logged by four
flows.)

**Ruling.** D1 as written, or amend by line.

### D2. The datom file and its own repository

A file inside a repository cannot hold that
repository's whole-snapshot hash: writing the hash
into the file changes the snapshot, and so the
hash. A Git revision cannot be written into its own
commit for the same reason.

Target: `psyche-skills/skills/vision-source.md`.
Place: the end of the section `## Assembled from
repositories`.

Above, unchanged:

The registry is populated from datom files kept in repositories, each updated by whoever updates its repository, and loaded together into the full registry. The registry is updated atomically.

Added, one of three.

Variant 1, the design's:

+A repository's datom file lists the sources that repository uses, each with its hash, as a lock file does. Two repositories cannot list each other.

Variant 2:

+A repository's datom file describes that repository itself, by name and fetcher. Its hash, and for Git its revision, are taken when the registry is assembled.

Variant 3:

+A repository's datom file describes that repository itself, hash included, and the file is left out of the bytes hashed.

Below, unchanged: the heading `## The hash
verifies`.

**Ruling.** 1, 2 or 3.

### D3. What bytes are hashed

The design hashes an archive of the tree in the
format Nix specifies for its own archives: entries
sorted by name, each with its kind, executable bit,
contents or link target. The Nexus skill already
says an encoded form fingerprints itself, by
default by the hash of its rkyv archive.

Target: `psyche-skills/skills/vision-source.md`.
Place: the end of the section `## The hash covers
the whole snapshot`.

Above, unchanged:

A source's hash covers the whole snapshot of its repository at a revision, as Nix does, without the Git subdirectory. When the source changes, its hash changes.

Added, one of three.

Variant 1, the design's:

+The bytes hashed are the snapshot in the Nix archive format.

Variant 2:

+The bytes hashed are the rkyv archive of the snapshot as a typed tree value.

Variant 3:

+The hash is the root of a tree of per-file Blake3 hashes, which a later store can use to keep each file once.

Below, unchanged: the heading `## A shared sources
library`.

**Ruling.** 1, 2 or 3.

### D4. What a local snapshot includes

A local source is a directory as it stands on its
host. Taking every file but the Git subdirectory
includes build output, so the hash of a local
source changes at every build inside it.

Target: `psyche-skills/skills/vision-source.md`.
Place: after D3's line, same section.

Added, one of three.

Variant 1, the design's:

+A local snapshot is every file in the directory except the Git subdirectory, build output included.

Variant 2:

+A local snapshot is the files Git tracks, as they stand in the directory.

Variant 3:

+A local snapshot is every file in the directory except the Git subdirectory and what the repository's ignore rules exclude.

Below, unchanged: the heading `## A shared sources
library`.

**Ruling.** 1, 2 or 3.

### D5. One registry or several

The design keeps one entry per name: one fetcher
and one hash. «The Ethos Nexus» reads the same
comments as placing Git revisions in a registry of
their own, the Git equivalence registry. Either
way, the Ethos registry keeps only a name and a
path inside a source, keyed by the same source
name; the hash and the fetcher stay in the Source
nexus. The hash field is four Integers until
«Bytes in ethos» is ruled.

Target: `psyche-skills/skills/vision-source.md`.
Place: the end of the section `## The registry`.

Above, unchanged:

The Source nexus keeps a registry of sources. An entry reaches its source through a backend fetcher, a Git repository at a revision or a local path on a given host, and carries the source's own Blake3 hash.

Added, one of two.

Variant 1, the design's:

+An entry holds a name, one fetcher and the hash.

Variant 2:

+The registries are two: one from name to hash, and the Git equivalence registry, from hash to where Git holds it. Only the sources that need it are in the second, and it is dropped when Git is.

Below, unchanged: the heading `## Assembled from
repositories`.

**Ruling.** 1 or 2.

### D6. Who reads the datom files

The Nexus skill says a command-line client turns
text into signal and nothing more. Reading the
repositories' datom files is more than that.

Target: `psyche-skills/skills/vision-source.md`.
Place: after D2's line, same section `## Assembled
from repositories`.

Added, one of two.

Variant 1, the design's:

+The Source nexus's meta client reads the repositories' datom files and sends what they hold as signal; it is the one client that does more than turn text into signal.

Variant 2:

+A separate assembler reads the repositories' datom files and sends what they hold as signal; the meta client stays text into signal.

Below, unchanged: the heading `## The hash
verifies`.

**Ruling.** 1 or 2.

### D7. Where the shared library lives

Every component that fetches sources already
depends on the Source nexus's ordinary wire
repository, since peers depend on each other's wire
repositories.

Target: `psyche-skills/skills/vision-source.md`.
Place: the end of the section `## A shared sources
library`.

Above, unchanged:

The components that use sources share a library of source types, including the objects a Memory stores for a registry of sources. A component refers to a source by name, so only the Source registry changes when a source's content changes.

Added, one of two.

Variant 1, the design's:

+The shared sources library is a repository of its own.

Variant 2:

+The shared sources library lives in the Source nexus's ordinary wire repository.

Below, unchanged: the heading `## A registry
name`.

**Ruling.** 1 or 2.

### D8. The shared library's types

The types every user of sources shares, in ethos.
A `Library` declares types; `.` after a name gives
its type, `.{ }` makes a struct of the positions
inside, `.[ ]` an enum of the variants inside.
`SourceName` is the name a component holds;
`Fetcher` says where the bytes come from; `Source`
is one registry entry; `Contribution` is what one
repository's datom file holds. `SourceName` is
plain text here; whether it becomes a checked name
built of words is the question of «Word-built
names». The `Blake3` field is four Integers until
«Bytes in ethos» is ruled.

Target: `psyche-skills/skills/vision-source.md`.
Place: after D7's line, same section `## A shared
sources library`.

Added, the line and the block below it:

+The shared sources library declares these types:

```ethos
Library
[]
[ SourceName.String
  Blake3.{ Integer Integer
           Integer Integer }
  Fetcher.[ Git.{ Remote Revision }
            Local.{ Host Directory } ]
  Source.{ SourceName Fetcher Blake3 }
  Contribution.{ Contributor
                 Vector<Source> } ]
[]
[]
```

Below, unchanged: the heading `## A registry
name`.

**Ruling.** D8 as written, or amend by type.
<!-- to-the-living:end -->
~~~~

## 6.2 The living's comments, verbatim

On this book (the first edition, 2026-10-10, relayed by d68c82). The comment on D1 about the description line ("shorten the skill description and drop 'is being designed'") is carried out as an instruction and was not logged verbatim in any file found; the only trace is the log lines below it.

**Source:** `058f16/vision/book.md` lines 3-9 (2026-10-10, stated in the signature line)

~~~~text
## What he reads is the proposal

Context: comment on «The Source nexus»; the hash stand-in was explained in the book's context section instead of in a proposal.

> Also this should be in the proposal. I basically almost don't read anything that's not in the proposal. It feels like most of the books are going to waste because I don't see the point of me reading something if I'm not reading it to approve or disapprove it with a comment.

-- psyche, STT; comment on «The Source nexus», relayed by d68c82, 2026-10-10.
~~~~

**Source:** `058f16/notion/ethos.md` lines 3-11 (2026-10-10, a notion, stated in the signature line)

~~~~text
## Referring to Rust types from Ethos; a byte array that corresponds to the Rust type

Context: comment on «The Source nexus», at the section where the Blake3 hash is stored as four Integers. He frames it as something to write down as a notion.

> I guess what you're saying is you're going to use 4 64-bit integers but Blake3 is already a type somewhere. This is interesting. We need a way to essentially refer to Rust types from Ethos, which I guess we already do. Maybe it's just a special import syntax: a special way to write syntax, which means this comes from Rust.
>
> Also if you felt compelled to use 4 integers instead of an array of bytes, then does that mean you thought the Ethos syntax didn't allow you to represent this as an array of bytes? Maybe we represent it in Ethos and then it also just corresponds to the Rust type so that we can see that's an array of bytes in Ethos. That sounds complicated and since we're trying to get started on all of the infrastructure, I wouldn't push too hard on that but it's worth just writing in [notion] I guess.

-- psyche, STT; comment on «The Source nexus», relayed by d68c82, 2026-10-10.
~~~~

**Source:** `058f16/log.md` lines 30-30 (058f16 log, 2026-10-10: the trace of the D1 description comment)

~~~~text
- 2026-10-10: Comments from the living on «The Source nexus», relayed by d68c82. On D1: shorten the skill description and drop "is being designed". That is an instruction and is carried out, not logged. Notion on referring to Rust types from Ethos logged in notion/ethos.md. Vision that what he reads is the proposal logged in vision/book.md.
~~~~

**Source:** `d68c82/log.md` lines 81-82 (d68c82 log, 2026-10-10)

~~~~text
- 2026-10-10: Persona book comments: rewrite fresh (old designs); land «What the root does» with the triad named only (Psyche, Mind, Field). Source nexus comments: shorter description; Rust-type reference logged as notion; books: what is ruled sits in the proposal (vision books).
- 2026-10-10: Persona rulings sent to 9519a1 to land. Source nexus comments sent to 058f16 for a new edition.
~~~~

The comments of 2026-10-10 on the earlier book «Sources and the registry» that D1 says it distils (all seven records, as logged by d68c82):

**Source:** `d68c82/vision/source.md` lines 1-62 (whole file; every record carries 2026-10-10 in its signature or Context line)

~~~~text
# Source

## A nexus called Source

Context: said after commenting on the «Sources and the registry» book in «Open books»; the concepts themselves are in his comments there.

> I did advance some concepts on how we can get sources from a particular nexus called Source that we would design.

-- psyche, STT, 2026-10-10.

## The registry: its anatomy, populated from datom files in each repository

Context: comment on «Sources and the registry», proposal 2 (a lowercase source names a registry entry), 15:22.

> Yes this is good and now we need to define the anatomy of that registry and use the same atomically updatable approach. The registry can be populated from multiple sources using the datom files that can be in the repositories that essentially wrap all of the data in that particular repository and can be updated by whoever updates that repo. It can then be loaded along with other repositories to create a full registry.
> ... This will be used to put together a registry and it'll just keep it. Every time we update some Ethos source, add one, or edit its name or something, we need to change the registry.

-- psyche, STT.

## The hash verifies the files; a smart store comes later

Context: same thread, 15:22.

> Also we could use the content hashes maybe. Maybe we need this hash-based storage. I think I had a thing called Logic Store but we could just move it to something more straightforward like a file store, an archive, or a file archive or something. It would be a nexus where we can put these hash-addressed files. Actually never mind all this. The hash is there for us so that we can verify that the files are the right files when we use them. That's all.

> For now we can just check the files. Later on we can have a store dedicated for this that will be smart enough to know what to store and what not to store, and how or where to get it (if it has to just use a Git backend to fetch a particular request) so that we don't double-store if we're already storing it in Git (like some kind of smart system). This is not the first lane. This is not the priority lane.

-- psyche, STT.

## The hash covers the whole repository; one shared sources library for ethos and curriculum

Context: «Sources and the registry», proposal 3, "What the hash covers", 15:27.

> Since we're going to use repos, we're going to hash the whole thing. It's got lights like Nix [sic], right? When the source changes, the source changes. That's why we don't put non-Rust things in the Rust repo, because if we want to change any of it, then Nix has to recompile.
>
> Since the skills are in repos, if we're talking about curriculum, we should have a list of sources. ... It's the same concept for curriculum.
>
> We can create a shared library between them, which is about sources, and it can even have objects for memory to store a registry of sources. That way the skill doesn't have a registry for each skill that doesn't need to be updated because it refers by name to the source. Only the source content addressing registry needs to be updated.

-- psyche, STT.

## A Source nexus: Git at a revision, own Blake3 hashes, several registries, backend fetchers

Context: «Sources and the registry», proposal 3, "How many", 15:30.

> This is actually really interesting. We could just make a registry [of] sources. We could make a Nexus called sources and we just put it all there. It can refer to a certain Git with a certain revision and we keep our own Blake3 hashes. We have different registries in fact. Eventually when we cut off Git, we don't need to keep the Git equivalence registry because it's different and some sources don't necessarily need to have it, right?
>
> We can have different types of backend fetchers. Basically we have this concept: we can get it from Git or we can get it from a local path on a certain host and we have the hash, right? Even the local path on the host is not dangerous. We would use a technique similar to Nix in that we wouldn't, obviously, include the Git subdirectory in the data, right? It would be the snapshot of that revision that we hash, kind of like how Nix does.

-- psyche, STT. Transcription corrected: "registry or sources" → "registry of sources".

## One Source nexus for all components; "get a source" means a source request to it

Context: «Sources and the registry», proposal 3, "How many", choice b, 15:31.

> There's some mix-up here: vision and knowledge. I guess you mean skills or context modules for the curriculum.
>
> ... we can have a source. Essentially we're adapting to the language. If I say, "Go get a source," then eventually you'll automatically know that I mean: use the source nexus and send it a source request and then you'll get a source. It's called the source nexus ...
>
> I think it's easier to just make the nexus for all the sources and reuse it for all components, then we only have one place to fix the sources aspect.

-- psyche, STT.
~~~~

**Source:** `d68c82/vision/naming.md` lines 3-13 (2026-10-10, comment on «Sources and the registry»; the source of D1's "A registry name" section)

~~~~text
## Registry names are independent of repository names; uncapitalized camelCase names made of words

Context: «Sources and the registry», proposal 3, "What the key reaches", 15:25.

> Well the name of the repo and the name in the registry, in our own memory, our own Nexus memory, doesn't have to be the same. Even I would say it seems we've gone with a hyphenated kebab case (I think it's called) for repo names, which maybe is more canonical or standard, and it's fine. I don't have any problem with it.
>
> In Protos languages like datom and [Ethos] for things that are not types or traits, we are going to use uncapitalized. It's going to be camel case because we do PascalCase for defined objects in the language and we do variants. If there's a string position in datom and it starts with a capital, that's okay because we have a different type that's kind of like a string but it has to be checked whenever we create a new one. This is the Prototypic name or whatever, the prototype name, which is an uncapitalized identifier. It's going to have to be composed of words so we need to put together some kind of fancy check. Well not that fancy, I guess.
>
> That would need a dedicated Nexus because it would need to have a database of words. If we're going to do the word-based identifiers, I'd like to get a book on the runtime size cost of having these things in a certain runtime and how it might be smarter to create a dedicated Nexus for that functionality. We could still just build it into whatever we're compiling into, whatever we're doing for now.

-- psyche, STT. Transcription corrected: "Esos" → "Ethos".
~~~~

## 6.3 Ruling and landing

Rulings D1 to D8: none found. The ownership and status lines, in order of date:

**Source:** `058f16/handover.md` lines 6-10 (058f16 handover, written 2026-10-14)

~~~~text
## Open decisions (the living's)
- **«The Source nexus», second edition:** https://claude.ai/artifact/HFKGQrnnLZRbAagX12r4VM. D1 proposes a new vision-source skill, and D2–D8 are forks. The most consequential is D2: a repository's datom file cannot hold its own whole-tree hash, so the design has the file list the sources the repository uses.
- **«Word-built names»:** https://claude.ai/artifact/3dmrXedbdMpqgBeSLJKgAL. It asks where the word check lives (built in now with a Nexus later, built in only, or a Nexus first) and which word list to use. The casing rule belongs to «The prototype name» (Ethos topic).
- **The hash type** is ruled only in «Bytes in ethos» (Ethos topic). The Source design keeps four Integers as its stand-in until then.
- Both books propose Sources lines. Skills no longer have a Sources section, so whoever lands them puts those references in the commit message.
~~~~

**Source:** `a275c0/log.md` lines 4-4 (a275c0 log, 2026-10-16 12:36)

~~~~text
- 12:36 context gathered by Sonnet subflow: predecessors 058f16 (handover 10-14), 73ada7; sibling a60bc8 retired by Field 12:35; open: Source nexus book (D2–D8), Word-built names book, 12 Message books unruled, ~30 raw Flow records in d68c82 and 23 in da2038 uncrystallized.
~~~~

Note: a275c0's line lists only D2-D8 as open, which could be read as D1 being settled; no record of a ruling on D1 was found, and 058f16/handover.md (written 2026-10-14) lists D1 as proposed. D1 is therefore counted as unruled.

**Source:** `d68c82/log.md` lines 221-221 (d68c82 log, a line inside the section dated 2026-10-11)

~~~~text
Book editions audit: only «The Source nexus» 2nd ed. published after his comments; others landed directly or uncommented; registry edition held on a fork (pushed 23824a); meta harness 3rd ed. not made.
~~~~

**Source:** `081064/log.md` lines 52-52 (081064 log, 2026-10-10: the hash type is ruled only in «Bytes in ethos», which is itself unruled)

~~~~text
- 2026-10-10 Answered 058f16 via 23824a: the hash type is proposed only in «Bytes in ethos»; the Source book cites it and keeps the stand-in.
~~~~

A second, different proposal for the same file exists in the Nexus seat's input report, not in a book the living has been shown with these words (it is "Proposal 19" of d68c82's book 38):

**Source:** `a275c0/reports/nexus-inputs.md` lines 310-324 (a275c0 report; its Status line says "unruled")

~~~~text
### B19. Proposal 19 — `psyche-context › skills/vision-source.md`, a new file (the Source nexus)
```
+ ---
+ description: The Source nexus, which holds and verifies sources, is being designed or judged.
+ dependencies: [vision-nexus]
+ ---
+ ## Source
+ One Source nexus holds the sources for all components; to get a source is to send it a source request.
+ A source is a Git repository at a revision, or a local path on a host, fetched by its own kind of backend fetcher.
+ The Source nexus keeps its own Blake3 hash of the whole snapshot, without the Git directory, as Nix does.
+ It keeps several registries; the Git equivalence registry is dropped when Git is cut off.
+ The hash is there to verify that the files are the right files; a smart store that knows what to keep comes later.
+ Ethos and curriculum share one sources library, with Memory objects for the registry of sources; a skill refers to a source by name.
```
Status: **unruled.** Bases: d68c82/vision/source.md:3,20,42,52 (2026-10-10); 23824a/vision/sources.md. Handover: «The Source nexus» 2nd edition and the word-names book are unruled (23824a/handover.md:43-46); a275c0/log.md: Source nexus book D2–D8 open.
~~~~

Landing: none. `git ls-tree origin/main` lists no `vision/source.md` or `skills/vision-source.md`, and `git grep` of origin/main for "Source nexus", "vision-source", "Blake3" in `vision/` returns nothing. Vision files on origin/main mentioning git are `vision/git-server.md` (7d4dc5b, 2026-10-16) and `vision/nix-builds.md` (f81b7b2), neither about sources.

## 6.4 Later records on the same subject (after 2026-10-10)

Two conflicts with D1's proposed file, which ends with a `## Sources` section listing four flow ids and has the parenthesis "(One set of comments, 2026-10-10, logged by four flows.)":

**Source:** `875960/vision/distillation.md` lines 3-9 (2026-10-10, stated; relayed by 9519a1)

~~~~text
## 2026-10-10 — the Sources sections in vision skills are noise, not vision

On the «Sources» sections at the end of vision skills; relayed by core d68c82 through 9519a1.

> To me that looks like noise. There's nothing about this that I want to load into it. It's ridiculous. What the fuck? This is noise. That's not vision; that's noise. If there is a technical reason to have that data, it does not belong in the vision. I can almost be certain of that.

-- psyche, STT, relayed by 9519a1.
~~~~

**Source:** `875960/vision/distillation.md` lines 11-15 (2026-10-10, stated)

~~~~text
## 2026-10-10 — the source reference goes in the commit message

> Well we should just put that source reference in the commit message that makes the change.

-- psyche, STT, relayed by 9519a1.
~~~~

**Source:** `33752b/vision/distillation.md` lines 3-11 (2026-10-11, stated in the signature line)

~~~~text
## The sources of a distillation go in the commit message, not in the skill

Context: comment on «Psyche is the gold», on the proposed vision-psyche paragraph «Everything the living says he wants is distilled: psyche data is what the work mines for, and nothing is built rich without it.»

> Yeah this is good and we already said that the sources of the distillation are going in the commit messages. Somebody has fucked up updating the skills here. If we need me to review it because it's a psyche skill, then let's do that pronto.
>
> All the sources of the distillation should be removed from all skills and all of the history. The commit history needs to be rewritten and the sources of these distillations put into the commit messages that belong to them. The whole history needs to be rewritten and the whole main branch needs to be moved. I said this 2 days ago. It should already be done. If it's not done then fucking get on it.

-- psyche, STT, 2026-10-11, comment on the book.
~~~~

Hash checking and a Rust-type hash (D3, D8):

**Source:** `d68c82/vision/flow.md` lines 290-298 (comment on «Flow: context modules and the prompt, 2nd edition» Proposal 7, 2026-10-16 (dated by the section heading))

~~~~text
Context: Proposal 7, on the module registry's blake3 hash and hash checking.

> "Let's make the hash `long_term` explicitly `long_term` so that the `short_term` tool doesn't need to do that."
>
> "Again let's make the hash checking a long-term goal and ignore it in the short term."
>
> "Until we have a way to efficiently update the hashes as we make edits"

-- psyche, typed.
~~~~

**Source:** `d68c82/vision/ethos.md` lines 67-73 (relayed 2026-10-15; the comment is of 2026-10-14, on «Chronos» Proposal 2)

~~~~text
## A hand-maintained vector of types imported from Rust

Relayed by Psyche Core Tertiary, 2026-10-15; the living's comment of 2026-10-14 on «Chronos», Proposal 2, on Latitude.Decimal.

> Maybe there is a fraction library or even an angle library that has more properly developed types for this. Let's just maintain a hand-maintained, specified vector for a list of types that we sort of import directly from Rust into Ethos, so that the Ethos-to-Rust compiler can use that to know what to link to. We can even eventually have proper programmatic feedback on the code, so it would know where these types are coming from, like built-ins, basically.

-- psyche, STT.
~~~~

---

# What could not be found

- Book 1: no comment on edition 2; no ruling on choices A and B; no ruling on the edition-2 expansion of P2. The living's wording that "it can all land in the proposal" is the only reaction on file.
- Book 2: no comment on the 4th edition; no ruling on P1, P2, P3 in any edition. The comments quoted are on edition 1.
- Book 3: no comment on the book and no ruling on D1 in any log, handover, vision or notion. The book's "as you said on the 3rd" refers to `edf227/vision/signalForms.md` (2026-10-03).
- Book 4: no comment, no ruling. Neither edition has a recorded reaction from the living.
- Book 5: no comment on the book and no ruling on rulings 1, 2, 3. The kernel facts in the book (stat field 22, /proc ancestry) are claims of other flows and were not re-witnessed here.
- Book 6: no verbatim of the D1 description comment ("shorten the skill description, drop 'is being designed'"), only the log lines above. No ruling on any of D1 to D8; the hash type depends on the unruled «Bytes in ethos».
- Not searched: `flows/*/vision/archive-*` files (excluded as instructed); transcripts outside the flows tree; the artifact comment threads themselves (comments are only known through the flows' relayed records).
- Landing check covers `psyche-skills` origin/main only. `psyche-context` origin/main is at the same head `53f68b6`.
