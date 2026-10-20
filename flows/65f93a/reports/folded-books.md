# Folded books: proposals, rulings, landing

Gathered 2026-10-16 for the Ethos vision 5th / syntax 2nd / sealed 2nd fold. Read-only gathering; nothing landed or changed.

Method and marks. Proposal blocks are extracted byte-exact by line range from the book sources (5-backtick fences; the books' own headings and fences sit inside). Landing was checked against psyche-context origin/main 53f68b6 (the local clone /git/github.com/LiGoldragon/psyche-skills has that remote): vision/ethos.md, vision/datom.md, vision/protos.md. That tree has no skills/ folder; the files the books call skills/vision-datom.md and skills/vision-protos.md are now vision/datom.md and vision/protos.md. Marks: LANDED, RULED-REJECTED, RULED-AMEND, UNRULED (no ruling by the living found). A comment on a different book that bears on a proposal is quoted as "Bearing" and does not change the mark. Rulings are searched in flows/*/log.md, flows/*/reports/*comment*, flows/*/vision, flows/*/notion; the main source of the living's book comments is flows/d68c82/reports/comments-2026-10-10.md and flows/d68c82/reports/comments-books-evening.md (five of the 081064 books carry an explicit "No comments." there).

Mark totals (36 line proposals; forks and rulings-asked counted inside their proposals): LANDED 2, RULED-REJECTED 1, RULED-AMEND 0, UNRULED 33.

## A. The living's comments on «The Ethos vision» editions and «The Ethos syntax»

Sources: flows/d68c82/vision/ethos.md (lines 103-216), flows/65f93a/vision/ethos.md, flows/65f93a/vision/goldenExample.md, flows/d68c82/log.md, flows/65f93a/log.md. Book sources: flows/65f93a/books/01..05.

### A.1 1st edition (artifact Ms23Gjyg2pQyPzLAfi66JR, flows/65f93a/books/01-ethos-vision.md, 19 proposals)

No comment by the living on it found (flows/65f93a/log.md lines 7-11 show d68c82 itself corrected its markers to a 2nd edition within about 5 minutes). No ruling.

### A.2 2nd edition (artifact BTKBnDFt5CYJYMM4t9UmcR, flows/65f93a/books/02-ethos-vision-2.md)

Two comments, relayed by Psyche Core Secondary 2026-10-16 19:03-19:04 (flows/d68c82/vision/ethos.md lines 103-113):

`````text
## Ethos and Nexus are infrastructure; Chronos is the example

Context: comments on «The Ethos vision, 2nd edition», 2026-10-16T19:03–19:04.

> "Yeah let's use this flowchart in the short-term section in Nexus."

-- psyche, typed. (On the opening figure: Ethos specifies Nexus; Chronos is built as a Nexus; Nexus guides Flow; Flow then guides other nexuses.)

> "I can see already that the machine [who] made this totally misunderstood what I meant. Ethos and Nexus are not golden examples. They're basic infrastructure. They're not examples. They're like the kind of wood we use to build our houses. There's a deep misunderstanding here and this whole book has to be redone."

-- psyche, typed. Transcription corrected: "hood" → "who".
`````

Proposal each sits on. Comment 1 sits on the opening figure (Ethos specifies Nexus; Chronos is built as a Nexus; Nexus guides Flow). Comment 2 sits on Proposal 1 ("Ethos, the Nexus and the Chronos example project together are the golden example", per flows/65f93a/vision/goldenExample.md):

`````text
# golden example

## Ethos and Nexus are basic infrastructure, not golden examples

Context: comment on «The Ethos vision, 2nd edition», Proposal 1, which read "Ethos, the Nexus and the Chronos example project together are the golden example". Relayed by Psyche Core Secondary, 2026-10-16T19:04.

> I can see already that the machine [who] made this totally misunderstood what I meant. Ethos and Nexus are not golden examples. They're basic infrastructure. They're not examples. They're like the kind of wood we use to build our houses. There's a deep misunderstanding here and this whole book has to be redone.

-- psyche, STT, book comment, relayed by Psyche Core Secondary.
`````

Rulings relayed. Comment 1: land the figure in the short-term section of Nexus (flows/65f93a/log.md line 12: "drop opening figure (goes to Nexus short-term section)"). Comment 2: RULED-REJECT of P1 as written; d68c82 order to redo the whole book (flows/65f93a/log.md line 12): "redo whole book; Ethos and Nexus are infrastructure, Chronos alone the example". The 3rd edition followed.

### A.3 3rd edition (artifact 27kia7ou5ik78iTWkvBgUi, flows/65f93a/books/03-ethos-vision-3.md)

Five comments (one with two parts) 2026-10-16 19:08-19:20, relayed by Psyche Core Secondary (flows/d68c82/vision/ethos.md lines 115-147; same text at flows/65f93a/vision/ethos.md lines 2-37):

`````text
## Comments on «The Ethos vision, 3rd edition», 2026-10-16

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

-- psyche, typed (input mode not shown). Transcription corrected: "datum" → "datom".
`````

Proposals they sit on (3rd edition text, flows/65f93a/books/03-ethos-vision-3.md lines 1-45):

`````text

### Proposal 1: Infrastructure and the golden example, a new section after Flow, a current best example · psyche-context › vision/ethos.md

+ Ethos and the Nexus are the basic infrastructure everything is built from.
+ Chronos is the example project built with them: the golden example from which Flow is implemented properly, then the other nexuses.

Ruling: land, amend, or reject.

### Proposal 2: How Ethos is shown, added to What Ethos is · psyche-context › vision/ethos.md

+ Where types are shown, the Ethos is shown, never the Rust it generates, unless the work is on how Ethos generates Rust.
+ Ethos is never shown out of context: each declaration names the kind of object it is and says what its types are for.
+ A datom is never shown without its Ethos specification.

Ruling: land, amend, or reject.

### Proposal 3: The type ethos, a new section after Declaration: File · psyche-context › vision/ethos.md

+ A type ethos opens with `type` and defines a single type.
+ Every type it needs is declared inline, where it is used; a type from a source comes in by the inline import.
+ A type ethos may carry one or more examples of its datom.

```ethos
+ type
+ CommitMessage.[              ; one variant
+    VisionDistillation.Vector< ;  per kind
+       Reference.{            ; a topic and
+          Topic.String        ;   a flow id
+          FlowId.String } > ]
```

```ethos
+ ; datom, expecting CommitMessage
+ VisionDistillation.[ { ethos 000000 } ]
```

Ruling: land, amend, or reject.
`````

Mapping, comment by comment:

- Whole book ("two books ..."): sits on the whole edition. Relayed as: "Comments on Ethos 3rd: two books (Ethos syntax change; Ethos vision 4th with comments)" (flows/d68c82/log.md line 2028); order: 4th edition with comments applied plus a separate Ethos syntax book (flows/65f93a/log.md line 15). Ruling: amend (split).
- "Chronos is the example project built with them ..." = 3rd P1, second sentence. Ruling: first part good (LAND), second part AMEND to explicitly short-term and mark anything that could go stale. 4th edition P1 applied it: "Short term: Chronos is the example project built with them ...".
- "A type ethos opens with `type` and defines a single type." = 3rd P3, first line. Ruling: AMEND to inline dotted `type.` then the type name and its specification; later (A.5) the head is capitalized, `Type.`.
- "A datom is never shown without its Ethos specification." = 3rd P2, third line. Ruling: AMEND to "a new datom or a datom proposal"; a production datom's specification is in a knowledge module (later contradicted in part by the syntax comment on P8, A.5); the exception becomes a formatting change, not a syntax change; braces explicit, `Variant.` then `{}` on its own line, first inner object not indented.
- The CommitMessage code example = 3rd P3 code block. Ruling: AMEND to allow whitespace/new line after the dot, indent chains of dotted variants, and capitalize `Type` ("This is obligatory").
- 3rd P4-P19 (whole programs, cost of datom payload, memory, Ethos Nexus, lowercase sources, Rust types, special representation, new types, flow id, inline mandatory, seniority, names of words, trait naming, every trait in Ethos, vertical layout, white square brackets): no comment found. UNRULED.

### A.4 4th edition (artifact 7m6YaqgLVKE36PpfrdZtD9, flows/65f93a/books/04-ethos-vision-4.md, 18 proposals)

No comment by the living on it found (flows/d68c82/log.md line 2030 publishes it; the next log entries concern the syntax book and the 22:16 syntax comments). No ruling on any of its 18 proposals. The 4th edition P1 is the amended form of 3rd P1.

### A.5 «The Ethos syntax» (artifact 9eqzRNbGq5kRZW5EHz2SfE, flows/65f93a/books/05-ethos-syntax.md, 9 proposals; P1-4 by 65f93a, P5-9 by Fable 39bd0c)

Comments 2026-10-16 22:16-22:30 (flows/d68c82/vision/ethos.md lines 149-216; same at flows/65f93a/vision/ethos.md lines 38-end):

`````text
## Comments on «The Ethos syntax», 2026-10-16, 22:16–22:30

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

-- psyche, typed (input mode not shown). Transcription corrected: "trade" → "trait"; "datum" → "datom".
`````

Rulings relayed (flows/d68c82/log.md line 2040, 2026-10-16T16:33:24-06:00): "Rulings: P2 example good, P5 good, P6 good; P1, P2 text, P3, P4, P7, P8 rejected or amended." Relayed to 65f93a (flows/65f93a/log.md line 23, "Rulings relayed on syntax P1-P8"). Per proposal (the comment sits on the proposal named in its "Context" line):

- P1 (braced file root, "braces open on their own line, under the variant; the first section sits on the brace's line"): rejected or amended. Comment: the new line is canonical in files but not required, not an invariant; first section does not sit on the brace line; no indentation of the first struct. Its Library example (indented) rejected.
- P2 (a space and a line break may follow the dot): text rejected or amended ("Not a space and a new line, just any kind of space or new line, any amount of space"); the Observed.Locks example is good ("Yeah this example is good.").
- P3 (the type ethos, one-variant CommitMessage enum; "may carry one or more examples of its datom"): rejected ("This is invalid. We cannot have an enum with only one variant"; the examples paragraph has "no logic").
- P4 (every variant capitalized, "`Type` included"): wording rejected ("You don't need to say \"type included.\""), examples called wrong.
- P5 (Type is no exception): "This section is good." Ruled good (land).
- P6 (whitespace after a separator): "This is good." Ruled good (land).
- P7 (canonical print breaks after the dot, two spaces per link): rejected ("No I don't want to make this canonical").
- P8 (new datom shown with its specification; production datom in a knowledge module; `Reply.[ Accepted.Integer Pending ]`): rejected or amended (specification "may or may not be in a knowledge module. It depends if it's implemented"; example has no variant).
- P9 (what can go stale is marked short-term): no comment, no ruling found. UNRULED.
- General: all Ethos-code books redone; real parsed code only; traits declared on every type; Fable involved. Landing check: none of P1-P9 is in psyche-context origin/main (no "Type." section, no whitespace-after-separator line in vision/protos.md, no braced-root text in vision/ethos.md). P5 and P6 are approved and not landed.

## B. The books

Repeated rulings that bear on several d5df1d books (quoted once here).

Bearing 1, the living on «The golden ethos» (first edition, artifact F5ymU4N6ma6Rwt8RmNw7Lm), 2026-10-09T18:28 and 18:30, anchored on `FlowId.{ String }` (flows/d68c82/reports/comments-2026-10-10.md; same in flows/ebbe30/vision/ethos.md):

> Well, this is already wrong. Ethos should be in the distill vision, but single-field structs are forbidden. If it was a string, it would be just a new type, and I want the new types not to be type aliases. That was never brought back to me. Also, type, new type, and type aliases: the difference, why we want new types, or why we might not. I need a book on that, but when I don't address a book, it has to be re-edited whenever the books are redone, and then we have an index book.
>
> First of all, it would not be a struct, and second of all, it should not be a string. I don't think we need it. Let's just leave it as a string for now, but let's put a comment there that says the string is very unideal, and we need a real ID based on the real hash bit that we're going to use to identify the flows.

Bearing 2, same book, 2026-10-09T18:23 (mutex): "This is good, and it reminds me: can we support mutex? I've seen mutex in Rust code once that was presented to me, and I was wondering if it was presented to me that way because we can't represent that abstraction in Ethos, or maybe we could. Maybe it's not hard. For any kind of exception or need or anything, we need to train any implementer to tell us if there is something that seems to be difficult to express in Ethos."

Bearing 3, the living on «The golden ethos», third edition (UG93sbmAyxoyS7wRF4gP1Q), 2026-10-09T19:44-20:07 (flows/d68c82/reports/comments-2026-10-10.md): "That graph is good. Let's include it in the vision." / "good" (on "Flow, a current best example") / "rename" (on "Rename every place.") / "should be psyche-skills/vision/ethos.md ..." (on the path). Landed: the graph section, the Flow pointer and the trait rename (flows/d5df1d/log.md line 32, psyche-skills 5c1922; in origin/main vision/ethos.md "## Flow, a current best example", "## Where the golden ethos lives"). The "ruled path" is psyche-skills/vision/ethos.md (now psyche-context vision/ethos.md); books that target psyche-skills/skills/vision-ethos.md carry a stale target.

Bearing 4, provenance. The living on trailing Sources sections of vision skills, 2026-10-10 (flows/081064/vision/ethos.md): "To me that looks like noise. There's nothing about this that I want to load into it. It's ridiculous. What the fuck? This is noise. That's not vision; that's noise. If there is a technical reason to have that data, it does not belong in the vision. I can almost be certain of that." And on «The inline import, second edition», 2026-10-09T22:03: "What is this source edition with a #? I don't like this. I don't like what I'm seeing here. I don't know what this is for." Consequence (flows/081064/log.md lines 43-45, flows/d68c82/log.md): references live in landing commit messages; every "Sources" line proposed in these books is void (RULED-REJECTED).

All "Sources" additions below are marked RULED-REJECTED on that basis.

### B.1 flows/d5df1d/books/golden-ethos-4.md  «The golden ethos, fourth edition»

Proposal (one): "The ethos of ethos, in vision-ethos", a new section in vision-ethos with the Library block of the language's own anatomy; four numbered choices inside (Value; comment in the anatomy; receiver names; Name as `Name.String` or `core:Name`). Target in the book: psyche-skills/skills/vision-ethos.md (stale path).

`````text
## Distillation

### 3. The ethos of ethos, in vision-ethos

Target: `psyche-skills/skills/vision-ethos.md`, a new
section after "## What Ethos is", before "## Why Ethos".

Removed: none.

Above, unchanged:

```text
## What Ethos is

Ethos is the schema language. Of the two main
syntaxes most agents will face, Ethos specifies the
types and Datom fills them with data.

Ethos is central. The anatomy of the system, every
type and every trait it uses, is read in its ethos;
an implementation is mostly the hand-written bodies.
```

Added, prose:

```text
## The ethos of ethos

The anatomy of an ethos file, written in ethos.
The first golden ethos; a draft.
```

Added, the block that follows that prose:

```
Library
[]                             ; imports: none
[  Name.String                 ; types
   ; 4b: core:Name, waiting on
   ;     the inline-import book
   Comment.String
   Names.[
      One.Name
      Several.Vector<Name> ]
   Import.{
      Name
      Names }
   Reference.{
      Name
      Vector<Reference> }
   Head.{
      Name
      Vector<Names> }
   Shape.[                     ; value, struct, enum
      Value.Reference
      Struct.Vector<Position>
      Enum.Vector<Variant> ]
   Position.[
      Reference
      Type ]
   Variant.{
      Name
      Option<Shape> }
   Type.{
      Option<Comment>
      Name
      Shape }
   Receiver.[
      Shared
      Mutable
      Absent ]
   Capability.{                ; inputs and yield
      Name
      Receiver
      Vector<Reference>
      Reference }
   Constant.{
      Name
      Reference }
   Complex.{
      Supertraits.Vector<Head>
      Associated.Vector<Head>
      Constants.Vector<Constant>
      Vector<Capability> }
   Body.[
      Simple.Vector<Capability>
      Complex ]
   Trait.{
      Option<Comment>
      Head
      Body }
   Association.{
      Name
      Vector<Head> }
   Imports.{
      Comment
      Vector<Import> }
   Types.{
      Comment
      Vector<Type> }
   Traits.{
      Comment
      Vector<Trait> }
   Associations.{
      Comment
      Vector<Association> }
   Library.{
      Imports
      Types
      Traits
      Associations } ]
[]                             ; traits: none yet
[]                             ; associations: none
```

Below, unchanged:

```text
## Why Ethos
```

What the types are. A Name is a word, a Comment its plain
text. Names is one name or a bracket of names, as an
import brings `protos:String` or `protos:[ String Integer ]`.
A Reference is a name with its angle arguments, as
`Vector<Name>`; a Head is a name with its constraints, as
a trait's identity. A Type is a name and a Shape: a value,
a struct of positions, or an enum of variants. A Trait is
a head and a body, simple (capabilities only) or complex
(supertraits, associated types, constants, capabilities).
A Library is its four sections, each a comment and its
declarations.

Every rule the block follows is already ruled: trait as
the word (flows/ebbe30/vision/ethos.md, 2026-10-09); a
type of one value written `Name.Type` is a new type, and
no struct holds one position (flows/ebbe30/vision/ethos.md,
2026-10-09; flows/d4ae97/vision/ethos.md, 2026-10-06);
three spaces of indentation (flows/f5a6e9/vision/ethos.md,
2026-10-07); each element on its own indented line, a
comment above or beside what it comments on
(flows/e5a0bc/vision/ethos.md, 2026-10-06 and 2026-10-07).

Four choices inside the block are open:

1. `Value.Reference`: the shape of a type written
   `Name.Type`, a new type over one reference, is named
   Value.
2. A comment is part of the anatomy: a Type and a Trait
   may carry one, and each of the four sections carries
   one.
3. The receiver of a capability is named Shared for `.`,
   Mutable for `!`, Absent for `:`.
4. Name, the type every name in the block uses:
   (4a) `Name.String`, as the block has it; (4b) Name as
   the core built-in reached by the inline import you
   opened, `core:Name`, a camelCaseExpression type checked
   when one is made (flows/d5df1d/vision/ethos.md,
   flows/445410/vision/flow.md, 2026-10-09). The block
   shows 4b on the comment line beneath `Name.String`;
   it waits on the inline-import book.

**Ruling 3.** Land the section as shown, or amend it by
the number of the choice.
<!-- to-the-living:end -->
`````

Ruling: none found on this edition (flows/d5df1d/handover.md lists it open, link 9y9ZqnNDbM6HSRXp1MNydH; flows/d68c82/reports/comments-books-evening.md has none). The living's comments on the 3rd edition (Bearing 3) ruled the graph and the Flow pointer, which are the opening lines of this book (it quotes them as "as it stands"). Landing: opening lines LANDED (origin/main vision/ethos.md "Flow, a current best example", "Where the golden ethos lives"). The proposal itself, a section "The ethos of ethos": not in origin/main (grep: the phrase occurs only inside the graph's box).
Mark: UNRULED.

### B.2 flows/d5df1d/books/invariants.md  «Ethos invariants»

Comments: "No comment threads" (flows/d5df1d/reports/comments-2026-10-09.md). Bearing: 1, 2 above, and e5a0bc 2026-10-06 (flows/e5a0bc/vision/ethos.md) on P4: "the first comment on the comments should be lined up with the object's indentation. I didn't see any use of the new line indentation style, which should be favored over starting indentation on the same line where the containing type is declared."

Proposal 1, a struct of one position is refused. Not in origin/main. Mark: UNRULED (Bearing 1: "single-field structs are forbidden").

`````text
## Proposal 1: a struct of one position is refused

For your ruling now. The proposals after it await their turn.

Target: psyche-skills/skills/vision-ethos.md. A new section lands between «Shapes and placement» and «Kinds are explicit; bodies are hand-written». The file as it stands around the landing:

Above — «Shapes and placement» ends with its Signal example, then its Rust; below — the heading «Kinds are explicit; bodies are hand-written» and its first paragraph: "A kind is declared, never inferred; an association asserts the type bears it."

Lines removed: none.

Lines added, a section heading and its text:

**## What ethos refuses**

The generator refuses a file that breaks one of these rules, and the refusal names the place.

A struct holds two or more positions; a struct of one is refused. A type that holds one other type is written as its name, a dot and that type.

In the example, Library is the root that holds shared types; its four brackets are imports, types, kinds and associations. `Age.{ Integer }` is a struct, Age, of one position, an Integer; `Age.Integer` is Age written as the Integer it holds.

```
; refused: a struct of one position
Library
[]                      ; imports
[ Age.{ Integer } ]     ; types
[]                      ; kinds
[]                      ; associations

; accepted: the type it holds, after a dot
Library
[]                      ; imports
[ Age.Integer ]         ; types
[]                      ; kinds
[]                      ; associations
```

Ruling: land, amend, or refuse.

`````

Proposal 2, no double wrapping. Not in origin/main. UNRULED.

`````text
## Proposal 2: no double wrapping (awaiting its turn)

Target: psyche-skills/skills/vision-ethos.md, in the section «What ethos refuses» that Proposal 1 makes, after its single-field rule.

Lines removed: none.

Lines added:

A type written as a name, a dot and one type never names another such type; it names what it holds. `FlowId.String` is a flow's id; a `Job.FlowId` beside it wraps a wrap, and is refused: where a job is a flow id, it is written FlowId.

```
; refused: Job wraps FlowId, which wraps String
Library
[]                    ; imports
[                     ; types
  FlowId.String       ; a flow's id
  Job.FlowId ]        ; a wrap of a wrap
[]                    ; kinds
[]                    ; associations

; accepted: a flow id is named a flow id
Library
[]                    ; imports
[ FlowId.String ]     ; types: a flow's id
[]                    ; kinds
[]                    ; associations
```

Ruling: land, amend, or refuse.

`````

Proposal 3, the print keeps every comment. Not in origin/main. UNRULED.

`````text
## Proposal 3: the print keeps every comment (awaiting its turn)

Target: psyche-skills/skills/vision-ethos.md, section «Spacing», which stands whole as:

Space the delimiters and the inner content. Ethos follows the canonical protos print: a space inside every bracket and brace at both ends when non-empty.

Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line. Nothing that has a next layer sits on one line.

Ethos carries a comment on every section and on every line that has a next layer, saying in plain words what the machine reads there; a comment runs from ; to the end of the line.

Lines removed: none.

Line added, after the comment paragraph:

The canonical print keeps every comment, at the element it was written on.

Ruling: land, amend, or refuse.

`````

Proposal 4, each element on a new indented line. origin/main Spacing still reads "its elements hang beneath the first, aligned". UNRULED (Bearing: e5a0bc comment above).

`````text
## Proposal 4: each element on a new indented line (awaiting its turn)

Target: psyche-skills/skills/vision-ethos.md, section «Spacing», shown whole under Proposal 3.

Line removed:

Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line. Nothing that has a next layer sits on one line.

Lines added:

Ethos expands vertically: a structure with more than one element opens its delimiter, and each element starts on a new line, indented one level beneath the line that opened it; the closing delimiter ends the last element's line. Nothing that has a next layer sits on one line. A vector of short items may hold several on a line up to a width, each wrapped line aligned with the first item.

A comment sits beside the element it is on, or on the line above it, lined up with that element.

In the example, Voice is a struct of two positions: Aspect, an enum declared in place, and Topic, a String.

```
Library
[]                      ; imports
[                       ; types
  Voice.{               ; where a flow speaks from
    Aspect.[            ; its aspect
      Psyche
      Mind
      Field ]
    Topic.String } ]    ; what it works on
[]                      ; kinds
[]                      ; associations
```

Ruling: land, amend, or refuse.

`````

Proposal 5, implementers report what ethos cannot express (target field-skills/skills/compensation-behavior.md, lines added: none). The rule is in field-skills origin/main compensation/behavior.md line 26 ("An implementer who meets something hard to express in ethos ... reports it to the living as its own finding rather than working around it."), landed from Bearing 2 (flows/ebbe30/log.md line 74, field-skills 9d0028). Not in the three psyche-context files. Mark: LANDED (in field-skills).

`````text
## Proposal 5: implementers report what ethos cannot express (awaiting its turn)

Target: field-skills/skills/compensation-behavior.md. The rule already stands there, a paragraph of its own after the rule that a design or report carries the thing as it now is:

An implementer who meets something hard to express in ethos — a mutex, an exception, any need the language seems not to carry — reports it to the living as its own finding rather than working around it.

Lines removed: none. Lines added: none.

Ruling: keep as it stands, or amend.

`````

Proposal 6, the derive's real name (Composing for Compositional). origin/main vision/ethos.md and vision/datom.md still say Compositional. UNRULED.

`````text
## Proposal 6: the derive's real name (awaiting its turn)

Target: psyche-skills/skills/vision-ethos.md. The generator derives `Composing`, the datom trait that reads a datom; `Compositional` is the trait beneath it, which that derive supplies. The skill names `Compositional` in its derives and in two sentences.

This lands after the trait rename of «The golden ethos», third edition, Ruling 2, since both touch the derive lines.

Each of the eleven derive lines, in «What a declaration turns into», «Inline types», «A variant named as a defined type carries that type», «A variant may declare its payload inline», «Kinds are explicit; bodies are hand-written» and «Kind syntax»:

```diff
-#[derive(Datomizable, Compositional)]
+#[derive(Datomizable, Composing)]
```

In «Every declared type bears both kinds», its first sentence. Removed: "Ethos Zero emits `Datomizable` and `Compositional` on every struct and enum it generates". Added: "Ethos Zero emits `Datomizable` and `Composing` on every struct and enum it generates".

In the same section's example, the line under the two alias lines. Removed: `#[derive(Datomizable, Compositional)]        // a type: always derived`. Added:

```rust
// a type: always derived
#[derive(Datomizable, Composing)]
```

In «The datom kinds are compiled in only where text is spoken», its first sentence. Removed: "A generated signal library bears `Datomizable` and `Compositional` conditionally". Added: "A generated signal library bears `Datomizable` and `Composing` conditionally".

In the same section's example, under the comment "emitted by Ethos Zero into the signal crate". Removed: `#[cfg_attr(feature = "datom", derive(Datomizable, Compositional))]`. Added:

```rust
#[cfg_attr(feature = "datom",
    derive(Datomizable, Composing))]
```

Ruling: land, amend, or refuse.

`````

Forks 1-3 (inline depth; who holds layout and comments; a Mutex field). No ruling. Bearing 2 is the mutex origin. UNRULED.

`````text
## Forks for your ruling

### Fork 1: how deep a type is declared inline

The skill says inline nesting goes about three deep. The record of 2026-10-06 (flows/d4ae97/vision/ethos.md) makes inline mandatory unless a type is too deep, with an algorithm to decide. The generator checks neither: six levels pass. Example, a lock rejection whose payload nests four deep:

```
Library
[]                        ; imports
[                         ; types
  Rejection.[             ; why a lock is refused
    Overlap.{             ; a held lock and a claim
      Lock.{              ; the lock held
        Owner.{           ; who holds it
          FlowId.String
          Since.Integer }
        Path.String }
      Claim.String } ] ]  ; the path claimed
[]                        ; kinds
[]                        ; associations
```

Options: (a) a fixed depth, three, past which the type is named apart and the generator refuses it inline; (b) a width: a type is named apart when inline it would run past the line width; (c) a fixed depth as the rule and a width as the reason, both stated; (d) another rule.

### Fork 2: who holds layout and comments

The print can rewrite any layout into the canonical one and could keep comments; the reader could also refuse a file. Example: a file with `[ Lock.{ LockId LockName } ]` on one line and no comment on it.

Options: (a) the reader refuses it: the layout is wrong and the comment is missing; (b) the reader refuses the missing comment, and the print fixes the layout; (c) the reader accepts both, and the print fixes the layout and keeps what comments there are; (d) another split.

### Fork 3: a Mutex field in ethos

Example: a Nexus holding its live flows behind a lock, a struct with a field of `Mutex<Vector<Flow>>`. Measured on the generator (flows/1d0733/reports/mutex-probe.md, 2026-10-09): an import names one segment as its source, so no accepted form reaches the standard library's Mutex; the path it emits does not compile; with the path fixed by hand, every derive ethos attaches but Debug fails on a Mutex field, the datom traits among them; ethos has no way to give a declaration fewer derives.

Options: (a) ethos expresses a Mutex field: imports of more than one segment, and a declaration that carries fewer derives; (b) shared mutable state stays outside ethos, in hand-written Rust, and implementers report each case under Proposal 5; (c) another form.
<!-- to-the-living:end -->
`````

### B.3 flows/d5df1d/books/types.md  «Type, new type, alias»

Comments: "No comment threads" (flows/d5df1d/reports/comments-2026-10-09.md); none later (flows/d68c82/reports/comments-books-evening.md). The rule it serves is stated in Bearing 1. origin/main vision/ethos.md still calls `FilePath.String` an alias and shows `pub type LockId = Integer;` (contradicted by the records, not changed). Fork 3 (bare or braced datom form) gates the held patches (flows/d5df1d/handover.md). Every proposal: UNRULED. The "Sources, appended" lines inside P1 and P2 are RULED-REJECTED (Bearing 4).

Proposal 1, the new type replacing the alias:

`````text
### Proposal 1. The new type, replacing the alias

A new section after "Imports" (which ends at line
157), before "What a declaration turns into"
(line 159), and the comment on line 225.

The file as it stands around the new section:

> The generated code carries no `use` statements;
> each imported name is written fully qualified:
> `protos:String` appears as `protos::String`,
> `datom:Datom` as `datom::Datom`.
>
> ## What a declaration turns into
>
> A declaration turns into the Rust type with
> named fields, ...

Added, as prose:

> **## New types**
>
> A type written as its name, a period and one
> contained type, `FlowId.String` or
> `Age.Integer`, is a new type: a type of its own
> holding one value of the contained type. It is
> never an alias; Rust receives a distinct type,
> not a second name for the contained one.

Added, the section's example:

```diff
+ Library
+ []                ; imports
+ [ FlowId.String   ; types: a new type over String
+   Age.Integer ]   ;   a new type over Integer
+ []                ; kinds
+ []                ; associations
```

Line 225, in "A variant named as a defined type
carries that type":

```diff
- [ FilePath.String                          ; types: FilePath is an alias of String
+ [ FilePath.String ; types: a new type over
+                   ;   String
```

The block as it stands around line 225:

```
Library
[]                        ; imports
[ FilePath.String         ; (line 225)
  SyntaxError.Vector<FilePath>
  GenerationFailure.[ SyntaxError
                      Unwritable ] ]
[]                        ; kinds
[]                        ; associations
```

Sources, appended at the end of the file's
Sources list:

> ebbe30 ethos
>
> 8e9e77 single-field-structs

Distils flows/d4ae97/vision/ethos.md, 2026-10-06;
flows/ebbe30/vision/ethos.md, 2026-10-09;
flows/8e9e77/vision/single-field-structs.md,
2026-09-08.

**Ruling 1.** (a) Land as shown. (b) Amend, by
line.

`````

Proposal 2, what is refused:

`````text
### Proposal 2. What is refused (awaiting its turn)

Added at the end of the "New types" section of
Proposal 1, as prose:

> A struct of one position is refused: what holds
> one value is a new type, `FlowId.String`, never
> `FlowId.{ String }`; in Rust too, one value is
> held by a new type, never a one-field struct.
>
> A new type never wraps a new type: where `Job`
> would hold a `FlowId`, the position is a
> `FlowId`.
>
> A new type holds a plain value, a String, an
> Integer, a Decimal, a Boolean; a new type over
> a struct or an enum is refused.

Sources, appended:

> e4a40e archive-newtypeWrappingAndSingleFieldStructs

Distils flows/ebbe30/vision/ethos.md, 2026-10-09;
flows/d4ae97/vision/ethos.md, 2026-10-06;
flows/8e9e77/vision/single-field-structs.md,
2026-09-08; flows/e4a40e/vision/
archive-newtypeWrappingAndSingleFieldStructs.md,
2026-09-03.

`````

Proposal 3, what Ethos Zero generates for a new type (also edits the tuple rule line):

`````text
### Proposal 3. What Ethos Zero generates for a new type (awaiting its turn)

Added at the end of the "New types" section, as
prose:

> Ethos Zero emits a new type as a Rust struct of
> one unnamed position, bearing the same derive as
> every struct and enum it emits.

Added, the Rust under the section's example:

```diff
+ #[derive(Datomizable, Compositional)]
+ pub struct FlowId(String);
+ #[derive(Datomizable, Compositional)]
+ pub struct Age(Integer);
```

In full, as the generator writes every struct
today, with the datom kinds behind the datom
feature:

```rust
#[derive(rkyv::Archive, rkyv::Serialize,
  rkyv::Deserialize, Clone, Debug,
  PartialEq, Eq, Hash)]
#[cfg_attr(feature = "datom",
  derive(datom_codec::Datomizable,
         datom_codec::Composing))]
pub struct FlowId(String);
```

Lines 435 and 436, the tuple rule, which a Rust
new type touches since Rust writes it as a
one-position tuple struct:

Removed:

> No tuple in the code we design; if some parts
> require it (standard traits, dependencies), then
> it is allowed at that contact point only.

Added:

> No tuple in the code we design, save the new
> type, which Rust writes as a one-position tuple
> struct; if other parts require a tuple (standard
> traits, dependencies), it is allowed at that
> contact point only.

When Ethos Zero emits this, the knowledge-ethos
skill (mind-skills/skills/knowledge-ethos.md,
which today says `Name.Type` is an alias and an
alias carries no derive) is brought in line with
it; knowledge lands without review.

`````

Proposal 4, the other alias sites:

`````text
### Proposal 4. The other alias sites (awaiting its turn)

Every example in vision-ethos that shows a
`Name.String` or `Name.Integer` as a Rust alias
changes to the new type of Proposal 3. Lines 226,
234, 269 to 271 and 275 are aliases of a vector;
they wait on fork 1 and are not touched here.

Lines 178 and 179, "What a declaration turns
into":

```diff
- pub type LockId = Integer;
- pub type LockName = String;
+ #[derive(Datomizable, Compositional)]
+ pub struct LockId(Integer);
+ #[derive(Datomizable, Compositional)]
+ pub struct LockName(String);
```

Lines 233 and 258:

```diff
- pub type FilePath = String;
+ #[derive(Datomizable, Compositional)]
+ pub struct FilePath(String);
```

Line 274, "Every declared type bears both kinds":

```diff
- pub type FilePath = String;                  // an alias: String already bears both
+ // a new type: derived like every type
+ #[derive(Datomizable, Compositional)]
+ pub struct FilePath(String);
```

Line 303, "Shapes and placement":

Removed:

> Signal's first two sections, an alias in the types section. Where

Added:

> Signal's first two sections, a new type in the types section. Where

Lines 322 to 324:

```diff
- pub type LockId = Integer;
- pub type LockName = String;
- pub type FlowId = String;
+ #[derive(Datomizable, Compositional)]
+ pub struct LockId(Integer);
+ #[derive(Datomizable, Compositional)]
+ pub struct LockName(String);
+ #[derive(Datomizable, Compositional)]
+ pub struct FlowId(String);
```

`````

Proposal 5, the flow id stays a string, marked (Bearing 1 asks the comment; not in origin/main):

`````text
### Proposal 5. The flow id stays a string, marked (awaiting its turn)

Line 315, in the Signal example of "Shapes and
placement":

```diff
-   FlowId.String
+   FlowId.String   ; a string for now, unideal:
+                   ;   the flow id is to be a hash
```

The block as it stands:

```
Signal
[]                        ; imports
[ Lock.LockRequest
  Release.LockId ]        ; queries
[ Locked.Lock
  Released.Lock ]         ; responses
[ LockId.Integer          ; types
  LockName.String
  FlowId.String           ; (line 315)
  LockRequest.{ LockName FlowId }
  Lock.{ LockId LockName } ]
```

The same comment goes on the flow id in «The
golden ethos», which today writes it
`FlowId.{ String }`.

Distils flows/ebbe30/vision/ethos.md, 2026-10-09;
flows/edf227/vision/identifiers.md, 2026-10-03.

`````

Open forks 1-5 (no ruling):

`````text
## Open forks

Each is answered by its number and letter.

**Fork 1. A name over a container.**
`SyntaxError.Vector<FilePath>`,
`LockPaths.Vector<LockPath>`.
(a) a new type over the vector,
`struct SyntaxError(Vec<FilePath>)`.
(b) it stays an alias.
(c) refused; the vector is written inline where
it is used.
The same answer covers `Name.Option<T>`.

**Fork 2. A name over a declared type.**
`DuplicateName.Lock` in a types section, which
Ethos Zero emits today as
`type DuplicateName = Lock`.
(a) Ethos Zero refuses it as an error.
(b) it stays an alias for this case only.

**Fork 3. How a new type reads in datom.**

```
12232711     ; (a) as its value
{ 12232711 } ; (b) as a one-position struct
```

(a) is what the alias writes and what ebbe30's
audit assumed; today's derive writes (b). (a)
needs the derive or the generator to give a new
type its value's form.

**Fork 4. How the value inside is reached.**
`FlowId(String)`, with the string private.
(a) Ethos Zero emits `AsRef<str>` and `From`
both ways, as in "Access boilerplate" above.
(b) the way in is a hand-written `TryFrom` check,
as Ethos Zero's own `Name` has.
(c) the value is public, `FlowId(pub String)`,
as datom-codec's `Meaning(pub Opaque)` is.

**Fork 5. Every semantic string a new type.**
ebbe30's audit proposes, for the Curriculum book,
"Every semantic string has a new type":
`Text.String`, not `Text.{ String }` and not a
bare String position.
(a) vision-ethos carries this line too.
(b) it stays in the Curriculum book alone.
<!-- to-the-living:end -->
`````

### B.4 flows/d5df1d/books/two-heads.md  «Two heads, one name»

Comments: none. Proposal D1, two readings of the Identity section. origin/main vision/ethos.md Identity still reads "Two heads that differ in a constraint are two traits." (reading 1's base, unchanged). Mark: UNRULED.

`````text
## Distillation

### D1. Two heads of one name, in vision-ethos

Target: `psyche-skills/vision/ethos.md`, the
vision-ethos skill. Place: the Identity section,
lines 104–118. Choose one reading.

The section as it stands:

```text
## Identity

A trait is identified as a Rust trait is, by its name and its
constraints, written as one head: Processable<[Clonable Sendable]
Serializable>. A constraint is a trait, or a bracket of traits: what
Rust writes as a generic parameter with its bounds, ethos writes as
the bounds alone, since in ethos there are no generics, only traits; a
constraint in a trait declaration is a trait, never a type. Two heads
that differ in a constraint are two traits. Which constraints belong
to the identity is not a decision to make: the ethos compiles to
Rust, and what identifies the trait identifies the trait. What else a
trait declares, its supertraits, its associated types and constants,
its capabilities, is its definition. Angle brackets hold the
constraints; they are a protos delimiter, recycled from Rust as
Result and Self are.
```

#### Reading (1): two heads are two traits

Lines 111–112 stand. The Rust-identity sentence at
line 114 gains that the generated name carries the
constraint.

Removed, line 114:

```text
Rust, and what identifies the trait identifies the trait. What else a
```

Added:

```text
Rust, and what identifies the trait identifies the trait. The Rust
name generated for a trait carries its constraints, so two heads of
one name become two distinct Rust traits. What else a
```

#### Reading (2): one name is one trait

Lines 111–112 are amended: a second head of the
same name is refused as a duplicate.

Removed, lines 111–112:

```text
constraint in a trait declaration is a trait, never a type. Two heads
that differ in a constraint are two traits. Which constraints belong
```

Added:

```text
constraint in a trait declaration is a trait, never a type. One name
is one trait: a second head of the same name is refused as a
duplicate. Which constraints belong
```

**Ruling D1.** (1) Two traits, two generated names.
(2) One name, one trait. Or amend, by line.
<!-- to-the-living:end -->
`````

### B.5 flows/d5df1d/books/no-tuple.md  «No tuple, and FlowId»

Comments: none. Proposal D1, two readings. origin/main vision/ethos.md still ends Associations with "No tuple in the code we design; if some parts require it (standard traits, dependencies), then it is allowed at that contact point only." Mark: UNRULED.

`````text
## Distillation

### D1. No tuple, and the new type

Target: `psyche-skills/vision/ethos.md`, the
vision-ethos skill, lines 467–468, after the
Interactions paragraph and before "## Spacing".

Above, unchanged:

```text
Interactions — the term for trait implementations — use the type
itself in all cases.
```

**Reading (1).** A new type over a plain value is
the one tuple the rule allows; the lines gain that
sentence. Fork 4 of «Types» stays open.

Removed:

```text
No tuple in the code we design; if some parts require it (standard
traits, dependencies), then it is allowed at that contact point only.
```

Added, prose:

```text
No tuple in the code we design, save the new type: a new type over a
plain value, `FlowId.String`, is the one-position tuple struct
`FlowId(String)`. Where other parts require a tuple (standard traits,
dependencies), it is allowed at that contact point only.
```

**Reading (2).** A new type is emitted with a
named field, and the rule stands as it is. The set
changes its emission from the tuple to:

```rust
pub struct FlowId { pub string: String }
```

The lines stay, unchanged:

```text
No tuple in the code we design; if some parts require it (standard
traits, dependencies), then it is allowed at that contact point only.
```

Reading (2) also answers Fork 4 of «Types»: the
inner value is a named public field, so one ruling
settles both.

Below, unchanged:

```text
## Spacing
```

Distils flows/d4ae97/vision/ethos.md, 2026-10-06
(the new type of «Types» Proposal 1),
and the tension found in
flows/d5df1d/reports/ethos-test-judgement.md.

**Ruling D1.** (1) The new type is the allowed
tuple. (2) The new type takes a named field.
Or amend, by line.
<!-- to-the-living:end -->
`````

### B.6 flows/d5df1d/books/stale-examples.md  «Two stale examples»

Comments: none. Proposal D1, two line pairs (Fillable `push!` input Self; `protos:Textualizable` as the qualified example). origin/main still has `[ Fillable.[ push!{ [ String ] [ Result<Integer SinkError> ] }` and "`protos:String` appears as `protos::String`". Mark: UNRULED (single proposal, two pairs, neither landed).

`````text
## Distillation

### D1. Two examples, in vision-ethos

Target: `psyche-skills/vision/ethos.md`, the
vision-ethos skill. Two line pairs, one in Trait
syntax and one in Imports.

#### 1. Trait syntax, the Fillable example

Above, unchanged:

~~~text
```
Library
[]                                                            ; imports
[ SinkError.[ Closed Full ] ]                                 ; types
~~~

Removed:

```text
[ Fillable.[ push!{ [ String ] [ Result<Integer SinkError> ] } ; traits
```

Added:

```text
[ Fillable.[ push!{ [ Self ] [ Result<Integer SinkError> ] } ; traits
```

Below, unchanged:

~~~text
             drain![ Vector<String> ]
             create:[ Self ] ] ]
[]                                                            ; associations
```
~~~

#### 2. Imports, the full-qualification example

Above, unchanged:

~~~text
[]                                                 ; associations
```

The generated code carries no `use` statements; each imported name is
~~~

Removed:

```text
written fully qualified: `protos:String` appears as `protos::String`,
```

Added:

```text
written fully qualified: `protos:Textualizable` appears as `protos::Textualizable`,
```

Below, unchanged:

```text
`datom:Datom` as `datom::Datom`.

## What a declaration turns into
```

Rests on flows/d5df1d/reports/ethos-test-judgement.md.

**Ruling D1.** (a) Land both. (b) Land one, by
number. (c) Amend, by line.
<!-- to-the-living:end -->
`````

### B.7 flows/d5df1d/books/alias-examples.md  «The alias examples»

Comments: none. Proposal D1, eleven lines, companion of types P1 ("landing that proposal lands these eleven lines with it"). origin/main still shows `pub type LockId = Integer;` etc. Mark: UNRULED.

`````text
## Distillation

### D1. The eleven alias lines follow the ruling

Target: `psyche-skills/vision/ethos.md`, the
vision-ethos skill.

This is the companion of «Type, new type, alias»,
Proposal 1: landing that proposal lands these
eleven lines with it, so one ruling covers both.
The added lines are the forms that book already
shows for the same sites: the Rust new type of its
Proposal 4, and its wording for lines 257 and 335.
The three `FilePath` lines (265, 290, 306) take the
same Rust new type.

#### Line 210, "What a declaration turns into"

Above, unchanged:

```text
[ LockId.Integer                              ; types
  LockName.String
  Lock.{ LockId LockName Vector<String> Option<Lock> }
  Generation.{ String String } ]
[]                                            ; traits
[]                                            ; associations
```

Removed and added:

```diff
- pub type LockId = Integer;
+ #[derive(Datomizable, Compositional)]
+ pub struct LockId(Integer);
```

Below, unchanged:

```text
pub type LockName = String;
#[derive(Datomizable, Compositional)]
pub struct Lock { pub lock_id: LockId, pub lock_name: LockName, pub string_vector: Vec<String>, pub lock_option: Option<Lock> }
```

#### Line 237, "Inline types"

Above, unchanged:

```text
[ LockId.Integer                                         ; types
  LockName.String
  Lock.{ LockId LockName }
```

Removed and added:

```diff
- pub type LockId = Integer;
+ #[derive(Datomizable, Compositional)]
+ pub struct LockId(Integer);
```

Below, unchanged:

```text
pub type LockName = String;
#[derive(Datomizable, Compositional)]
pub struct Lock { pub lock_id: LockId, pub lock_name: LockName }
```

#### Line 257, "A variant named as a defined type carries that type"

Above, unchanged:

```
Library
[]                                         ; imports
```

Removed:

```text
[ FilePath.String                          ; types: FilePath is an alias of String
```

Added:

```diff
+ [ FilePath.String ; types: a new type over
+                   ;   String
```

Below, unchanged:

```text
  SyntaxError.Vector<FilePath>             ;        SyntaxError is a vector of FilePath
  GenerationFailure.[ SyntaxError          ;        an enum: the variant SyntaxError is bare here,
                      Unwritable ] ]       ;        but SyntaxError is a defined type, so it carries one
```

#### Line 265, "A variant named as a defined type carries that type"

Above, unchanged:

````text
[]                                         ; associations
```
```rust
````

Removed and added:

```diff
- pub type FilePath = String;
+ #[derive(Datomizable, Compositional)]
+ pub struct FilePath(String);
```

Below, unchanged:

```text
pub type SyntaxError = Vec<FilePath>;
#[derive(Datomizable, Compositional)]
pub enum GenerationFailure { SyntaxError(SyntaxError), Unwritable }
```

#### Line 290, "A variant named as a defined type carries that type"

Above, unchanged:

````text
[]                                                        ; associations
```
```rust
````

Removed and added:

```diff
- pub type FilePath = String;
+ #[derive(Datomizable, Compositional)]
+ pub struct FilePath(String);
```

Below, unchanged:

```text
#[derive(Datomizable, Compositional)]
pub struct Unwritable_Data { pub file_path: FilePath, pub string: String }
#[derive(Datomizable, Compositional)]
```

#### Lines 301 to 303, "Every declared type bears both traits"

Above, unchanged:

```text
Ethos Zero emits `Datomizable` and `Compositional` on every struct and
enum it generates, so every ethos-declared type always bears both
```

Removed, prose:

```text
traits and no declared type can exist without them. An alias bears them
through the type it names: an alias is not a new type and cannot carry
a derive.
```

Added, prose:

```text
traits and no declared type can exist without them. A new type, such
as `FilePath.String`, is a type of its own and bears them through its
own derive.
```

Below, unchanged:

````text

```rust
````

#### Line 306, "Every declared type bears both traits"

Above, unchanged:

````text

```rust
````

Removed:

```text
pub type FilePath = String;                  // an alias: String already bears both
```

Added:

```diff
+ #[derive(Datomizable, Compositional)]
+ pub struct FilePath(String);
```

Below, unchanged:

```text
pub type SyntaxError = Vec<FilePath>;        // an alias: Vec<T> bears both for any T that does
#[derive(Datomizable, Compositional)]        // a type: always derived
pub enum GenerationFailure { SyntaxError(SyntaxError), Unwritable }
```

#### Line 335, "Shapes and placement"

Above, unchanged:

```text
Each section has its own parsing context; placement carries the
meaning. Head then symbol is a variant of `Query` or `Response` in a
```

Removed, prose:

```text
Signal's first two sections, an alias in the types section. Where
```

Added, prose:

```text
Signal's first two sections, a new type in the types section. Where
```

Below, unchanged:

```text
types are defined a bracket is an enum, never a vector. Ethos may
generate default implementations for Query and Response, which is why
```

#### Line 354, "Shapes and placement"

Above, unchanged:

```text
[ LockId.Integer                                       ; types
  LockName.String
  FlowId.String
```
```text
pub enum Query    { Lock(LockRequest), Release(LockId) }
pub enum Response { Locked(Lock), Released(Lock) }
```

Removed and added:

```diff
- pub type LockId = Integer;
+ #[derive(Datomizable, Compositional)]
+ pub struct LockId(Integer);
```

Below, unchanged:

```text
pub type LockName = String;
pub type FlowId = String;
```

Distils flows/d4ae97/vision/ethos.md, 2026-10-06.

**Ruling D1.** (a) These eleven lines land with
«Type, new type, alias», Proposal 1. (b) Amend, by
line.
<!-- to-the-living:end -->
`````

### B.8 flows/d5df1d/books/inline-import-3.md  «The inline import, third edition»

Proposal D1. Ruling, from the artifact 488DdxYfWUghW6EcBeXg6y comment of 2026-10-10T15:17 (flows/d68c82/reports/comments-2026-10-10.md, anchored on "A type may be declared over a type from a source in place ..."):

> Yes this is good.

Also, spoken 2026-10-10 (flows/081064/vision/ethos.md): "The inline import, we don't have to worry too much about it for now. It's just a nice thing that I thought about and let's not block on it right now."

Landed: psyche-skills 9fb0433, rewritten to 97874fb (flows/081064/log.md lines 15, 109). Present in origin/main vision/ethos.md Imports: "A type may be declared over a type from a source in place, with no entry in the imports section: `Topic.custom:Name` declares `Topic` over the type `Name` from the source `custom`. The source is known twice: its first letter is lowercase, and a colon follows it." Mark: LANDED.

`````text
## Distillation

### D1. The inline import, in vision-ethos

Target: `psyche-skills/vision/ethos.md`, the
vision-ethos skill. Place: the Imports section,
after its closing paragraph and before "## What a
declaration turns into".

Removed: none.

Above, unchanged:

```text
The generated code carries no `use` statements; each imported name is
written fully qualified: `protos:String` appears as `protos::String`,
`datom:Datom` as `datom::Datom`.
```

Added, prose:

```text
A type may be declared over a type from a source in place, with no
entry in the imports section: `Topic.custom:Name` declares `Topic`
over the type `Name` from the source `custom`. The source is known
twice: its first letter is lowercase, and a colon follows it.
```

Below, unchanged:

```text
A declaration turns into the Rust type with named fields, bearing the
datom traits through the derive, which Ethos Zero emits with the type.
```

Distils flows/d5df1d/vision/ethos.md, 2026-10-09.

**Ruling D1.** (a) Land as written. (b) Amend, by
line.
<!-- to-the-living:end -->
`````

### B.9 flows/ebbe30/books/2-distilled-lines-gone-stale.md  «Distilled lines gone stale»

Comments: none ("Books with no comments", flows/d68c82/reports/comments-spirit-books.md; flows/445410/log.md lines 34-36 queue). Eight line proposals (1-8) and five forks (9-13). Marks below are against origin/main (psyche-context 53f68b6). Items 1, 2, 3, 6 and 7 target vision-flow, vision-messaging, vision-nexus, vision-model-roles, which are outside the three files you named; checked by grep only.

`````text
<!-- to-the-living:start -->
Presentation.{ «Distilled lines gone stale» }

Ten lines in the vision skills now contradict a
later record of yours. Each is shown as removed and
added, with the record it follows. Then four
rulings, and one on the books.

`````

Item 1, vision-flow four layers. origin/main vision/flow.md line 41 now says "A layer is Primary, Secondary, Tertiary or Quaternary"; neither the old nor the proposed sentence is present (rewritten). UNRULED, superseded in substance by a later rewrite.

`````text
## 1. vision-flow, line 22 — four layers
Record: 5578cc/vision/layers.md, 2026-10-03.
```
- A voice is an aspect carrying a rank,
- `Psyche.Primary`: Psyche, Mind, Field by
- Primary, Secondary, Tertiary, nine voices.
+ A voice is an aspect carrying a layer,
+ `Psyche.Primary`: Psyche, Mind, Field by
+ Primary, Secondary, Tertiary, Quaternary,
+ twelve voices.
```
Ruling 1: (a) land (b) amend.

`````

Item 2, reach. The old and the new sentence are both absent from origin/main vision/flow.md. UNRULED.

`````text
## 2. vision-flow, line 24 — reach
Record: d4ae97/vision/flow.md, 2026-10-07.
```
- vertically within an aspect one rung at a time
+ vertically within an aspect one layer up, or
+ any layer down
```
Ruling 2: (a) land (b) amend.

`````

Item 3, datom bodies. origin/main vision/messaging.md lines 8-9 still read "The message body is a datom that lands in the recipient's prompt as a datom-formatted object." Not landed. UNRULED.

`````text
## 3. vision-messaging, lines 8–9 — datom bodies
Record: 8904b1/vision/datom.md, 2026-09-27.
```
- The message body is a datom that lands in the
- recipient's prompt as a datom-formatted object.
+ A message body is a datom where the receiving
+ program reads datom; a messenger that needs
+ none is given none.
```
Ruling 3: (a) land (b) amend.

`````

Item 4, new types in vision-ethos. Not landed (alias wording still present). UNRULED. (Same subject as types.md P1/P4 and alias-examples.md.)

`````text
## 4. vision-ethos, lines 206–234, 323–325 — new types
Record: d4ae97/vision/ethos.md, 2026-10-06.
```
- FilePath.String ; types: FilePath is an alias
- of String
- pub type FilePath = String;
+ FilePath.String ; types: FilePath is a new type
+ holding String
+ pub struct FilePath(String);
```
Every other one-position alias in the file
changes the same way.
Ruling 4: (a) land (b) amend.

`````

Item 5, the four roots. Not landed: origin/main vision/ethos.md still has "Signal's sections are queries and responses, since there is communication; Sema's are record types, the rest to be decided. Signal gives a Nexus its main types and Sema its database types."; vision/sema.md still says "its root, Sema, declares record types". UNRULED.

`````text
## 5. vision-ethos, lines 25–28 — the four roots
Record: 91ea9f/vision/ethos.md, 2026-10-02.
```
- since there is communication; Sema's are
- record types, the rest to be decided. Signal
- gives a Nexus its main types and Sema its
- database types.
+ Library, Signal, Operation, Memory. No version
+ in a file. Signal's sections are queries and
+ responses, since there is communication.
```
vision-sema, line 9, the same record:
```
- its root, Sema, declares record types.
+ its root, Memory, declares record types.
```
Ruling 5: (a) land both (b) amend.

`````

Item 6, queries and responses in vision-nexus. origin/main vision/nexus.md line 116 still reads "a closed enum of operations with their paired replies ... Operations are verbs, `Submit`; replies the past tense, `Submitted`; rejections name themselves." Not landed. UNRULED.

`````text
## 6. vision-nexus, line 116 — queries and responses
Record: 564f55/vision/archive-ethos.md, 2026-09-09.
```
- a closed enum of operations with their paired
- replies ... Operations are verbs, `Submit`;
- replies the past tense, `Submitted`;
- rejections name themselves.
+ a closed enum of queries with their paired
+ responses ... Queries are verbs, `Submit`;
+ responses the past tense, `Submitted`;
+ refusals name themselves.
```
Ruling 6: (a) land (b) amend.

`````

Item 7, the title. origin/main vision/model-roles.md line 46 now reads "Every native main session is titled `{ <Aspect> <Topic> <Layer> <FLOW_ID> }`" and "title names the layer, never the model": the old `<Aspect> <Model> <FLOW_ID>` is gone but the proposed wording is not verbatim. UNRULED (no ruling found; changed by another route).

`````text
## 7. vision-model-roles, lines 76–81 — the title
Record: d4ae97/vision/flow.md, 2026-10-07.
```
- Every native main session is titled
- `<Aspect> <Model> <FLOW_ID>`.
+ Every native main session is titled by its
+ aspect and its flow id in words; the title
+ names no model.
```
Lines 77–81 are removed with it.
Ruling 7: (a) land (b) amend.

`````

Item 8, layout in vision-ethos. Not landed (origin/main Spacing still has "its elements hang beneath the first, aligned"). UNRULED. Bearing: e5a0bc 2026-10-06 quoted under B.2.

`````text
## 8. vision-ethos, line 445 — layout
Record: e5a0bc/vision/ethos.md, 2026-10-06.
```
- a structure with more than one element opens
- on its line and its elements hang beneath the
- first, aligned
+ a structure with more than one element opens
+ on its line, and its elements begin on the
+ next line, indented
```
Ruling 8: (a) land (b) amend.

`````

Forks 9-13 (voice; FlowId; inline payload; committing; the books). Rulings asked, none given. Bearing for 10 (FlowId): Bearing 1 ("Let's just leave it as a string for now"). UNRULED.

`````text
## 9. Voice
f5a6e9/vision/flow.md:11 and d4ae97/vision/flow.md:86,
both 2026-10-07, point opposite ways.
Ruling 9: (a) a voice is a permanent metaflow
(b) there is no voice; the metaflow carries the
aspect directly (c) something else.

## 10. FlowId
vision-nexus line 153 holds `FlowId.Integer`;
vision-ethos lines 316 and 325 hold `FlowId.String`;
edf227/vision/identifiers.md:10 calls it a hash.
Ruling 10: (a) `FlowId.Integer` everywhere
(b) a `Hash` type (c) something else.

## 11. Inline payload
564f55/vision/archive-ethos.md:43 and
vision-ethos line 216 differ on naming a payload.
Ruling 11: (a) the payload bears the variant's
name (b) a distinct path-overlap name (c) other.

## 12. Committing
vision-committing lines 8–9 and Primary's
CLAUDE.md "Committing" differ on dirty changes.
Ruling 12: (a) a flow commits only what it edited
(b) found dirty changes are committed first, as
their own commit.

## 13. The books
Thirty-six books stand with open rulings; their
needed changes are listed in this flow's
reports/book-audit-verified.md §A. Ninety-seven
are overtaken by a landing or a later record, §B.
Ruling 13: (a) each live owning flow republishes
its §A books and retires its §B books (b) this
flow republishes all of §A (c) retire §B only.
<!-- to-the-living:end -->
`````

### B.10 flows/445410/books/3-the-special-representation.md  «The special representation»

Comments on this book: none found (flows/445410/log.md lines 72-75 record publication, no comment). Origin: the living's 2026-10-09T18:30 words ordering the book (Bearing: flows/d68c82/reports/comments-2026-10-10.md, "The golden standard" thread): "the special representation is basically an implementation for a special way to decode and encode, so that the representation has a different type than the type when it's read into the Rust runtime ... It would be a trait, a special representation, like a custom Datom conversion, basically. We need to be short, but we need to also describe what the trait is." The proposed section is not in origin/main vision/ethos.md or vision/datom.md. The trait name `Represented` is "offered for his word" and unruled. Gate: types Fork 3. Mark: UNRULED.

`````text
## Proposal 1: Special representation

Target: `psyche-skills/skills/vision-ethos.md`

New section, shown whole. Source: `flows/445410/vision/ethos.md`, 2026-10-09.

```
## Special representation

A type whose datom representation differs from its Rust type has a special representation: ethos describes the real Rust type and names its representation type, and Rust implements the conversion between them.
```
`````

### B.11 flows/081064/books/type-ethos.md  «The type ethos»

Comments on this book: none (flows/d68c82/reports/comments-books-evening.md; flows/081064/handover.md item 5). Origin comments are on the hub's book «Sources in the commit message» (flows/d68c82/reports/comments-sources-book.md; flows/081064/vision/ethos.md, 2026-10-10): "Yeah this is good. We could also improve the format so that it essentially fits a datom, which would mean creating an ethos specification, but we wouldn't need to make an implementation that uses it yet. It would just be the ethos that shows. You can use a type, `type ethos`. It just starts with `type` and it defines a single type and you can define everything inline, like these quick type definitions, where you can use the inline import syntax." Not landed (no "type file" section in origin/main). Mark: UNRULED.

Bearing, later comments on a restatement of the same lines (3rd edition P3 and the syntax book, A.3 and A.5), which amend this proposal: the head is capitalized and dotted (`Type.` then the type name and specification), written "inline dotted" with whitespace allowed after the dot; the book's lowercase `type` head and its one-variant style conflict ("All these variants need to be capitalized. This is obligatory."). The proposal's own added example shows CommitMessage with a single variant (Mixed is omitted from it), the shape he called invalid ("We cannot have an enum with only one variant") when restated.

`````text
## Proposal: the type file in vision-ethos

Target: psyche-skills/vision/ethos.md, a new section
"## The type file" between the end of "## Roots"
and "## Non-repetition".

Above, as it stands:

Four roots: Library, Signal, Operation, Memory. Signal declares what a Nexus says; Operation what it does, one operation type for every effect; Memory what it remembers; Library what they share. A memory trait carries a standard successful-or-unsuccessful change and, for each version, the upgrade from the previous format; that upgrade is the very edit the type needs.

Added:

```diff
+## The type file
+
+A type file defines a single type. It starts with
+the head word `type`, then the one type; every type
+that one type needs is defined inline, where it is
+used, and a type from a source comes in by the
+inline import.
+
+```
+; the head: a type file, one type
+type
+; the one type: an enum, one variant per kind
+CommitMessage.[
+  ; a distillation's references: a vector
+  VisionDistillation.Vector<
+    ; of Reference, named and declared in place
+    Reference.{
+      ; type check: open book «The prototype name»
+      Topic.String
+      ; flow id: a String for now
+      FlowId.String }> ]
+```
+```
+; datom, in a position expecting CommitMessage
+VisionDistillation.[ { ethos 081064 } ]
+```
+
```

Below, as it stands:

## Non-repetition

The example omits the Mixed variant, which waits
on question 5, and the checked type of Topic waits on
«The prototype name».

## Distillation

- psyche-skills/vision/ethos.md: a new section
  "## The type file", with the statement, the
  ethos example and the datom line above, placed
  between the end of "## Roots" and
  "## Non-repetition".

It distils flows/081064/vision/ethos.md,
2026-10-10, "the type ethos, and commit messages in
datom" and "the commit message as a variant with a
struct". No Sources line is added to the skill. The
landing commit's message will list `081064 ethos`.

## Ruling

1. The statement "## The type file" lands in
   vision-ethos as proposed, or amended.
2. Question 1: a single declaration, or sections.
3. Question 2: inline imports only, or an imports
   section too.
4. Question 3: a Rust module with its helpers
   public, or nothing yet.
5. Question 4: the variants to name now, or later.
6. Question 5: a Mixed variant, or a top-level
   vector.
`````

### B.12 flows/081064/books/vector-delimiter.md  «A delimiter for vectors»

Comments on this book: none found. Origin notion (flows/081064/notion/ethos.md line 16, 2026-10-12): the two notions (a delimiter for vectors; a comment delimiter) are his, as notions only. Bearing (a comment on a different book, «Battery drain in sleep», 2026-10-16, flows/d68c82/vision/ethos.md lines 83-93): "I actually want long-term marked ethos. I also want a review that I want to add: the different kind of square bracket. There's another pair. I think it's called a white square bracket. I want to use that as sugar in ethos, as a special syntax at the right layer of interpretation, because we have different layers." This names the book's Candidate 1 (⟦ ⟧) but does not rule on the book's line. Not landed (origin/main intrinsics list still has Vector; no ⟦ in vision/ethos.md or vision/protos.md). Both proposals: UNRULED. (4th edition P18 of the vision book restates it.)

Proposal 1, the vector delimiter (three sides):

`````text
### Proposal 1: the vector delimiter

Line 338, the sentence as it stands, with the line above and
below:

Above, as it stands:

Each section has its own parsing context; placement carries the
meaning. Head then symbol is a variant of `Query` or `Response` in
a Signal's first two sections, an alias in the types section.

As it stands:

Where types are defined a bracket is an enum, never a vector.

Added after it, one of three; the pair is the ruling of
question 1 and the spacing of question 3:

Side a, white square brackets:

```
+ A vector is its element type inside ⟦ ⟧:
+ `Names.⟦ String ⟧`. The word Vector is not
+ written.
```

Side b, single guillemets:

```
+ A vector is its element type inside ‹ ›:
+ `Names.‹ String ›`. The word Vector is not
+ written.
```

Side c, mathematical angle brackets:

```
+ A vector is its element type inside ⟨ ⟩:
+ `Names.⟨ String ⟩`. The word Vector is not
+ written.
```

Below, as it stands:

Ethos may generate default implementations for Query and Response,
which is why Signal is its own root.

Line 177 then loses the word from the intrinsics list, under any
side:

```
- Integer, Decimal, Boolean, Meaning, Vector,
- Option, Result, Self.
+ Integer, Decimal, Boolean, Meaning, Option,
+ Result, Self.
```

Removed lines: the one shown, only when the word goes away whole
(question 2).

Impurities discarded: none.

Ruling asked:

1. Land side a, b or c as written.
2. Another pair; name it.
3. Amend by line.
4. Keep `Vector<T>`; close the notion.

`````

Proposal 2, the documentation comment:

`````text
### Proposal 2: the documentation comment

Line 480, as it stands, with the line above and below:

Above, as it stands:

Ethos expands vertically: a structure with more than one element
opens on its line and its elements hang beneath the first, aligned;
the closing delimiter ends the last element's line. Nothing that
has a next layer sits on one line.

As it stands:

Ethos carries a comment on every section and on every line that
has a next layer, saying in plain words what the machine reads
there; a comment runs from ; to the end of the line.

Added after it, the pair being a placeholder until question 10
is ruled:

```
+ A description of an object is a balanced pair
+ the reader keeps, after the object:
+ `Record.{ String Integer } ⟪ a pair ⟫`.
```

Below, as it stands:

## Zero

Removed lines: none.

Impurities discarded: none.

Ruling asked:

1. Land as written, naming the pair.
2. Hold until the vector pair is landed.
3. Amend by line.
`````

### B.13 flows/081064/books/ethos-nexus.md  «The Ethos Nexus»

Comments on this book: none ("No comments." flows/d68c82/reports/comments-books-evening.md; flows/23824a/handover.md lines 30-37 "unruled"). Origin comment, «Sources and the registry» proposal 2 thread (2026-10-10T15:22, flows/d68c82/reports/comments-2026-10-10.md; also flows/d68c82/vision/ethos.md lines 3-14): "In Ethos do we have an Ethos Nexus or is Ethos Zero a non-Nexus? We need to migrate the Ethos Nexus version so that we can do this. In Ethos I want to specify the three aspects: - the signal - the memory - the operation". The five draft ethos files in the book (lines 125-288) are design drafts, not lines proposed for the skill. Proposals: D1 (new section "The Ethos Nexus" in vision-ethos), D2 (registry line with the core fork filled), D3 (Sources lines).

D1: not landed (no such section in origin/main). UNRULED. D2: not landed; the core fork is unruled anywhere. UNRULED. D3 (Sources lines `081064 ethos`, `73ada7 nexus`): RULED-REJECTED (Bearing 4).

`````text
## Distillation

### D1. The Ethos Nexus, a new section of vision-ethos

Target: psyche-skills/vision/ethos.md, the
vision-ethos skill. Place: after the "Generation"
section, before "## Sources".

Removed: none.

Above, unchanged:

~~~text
## Generation

By request to ethos-zero, which is not a daemon, hence its name; committed, held fresh by a test.

```
ethos-zero 'Generate.{ /abs/orchestrate.ethos /abs/out }'
```

~~~

Added:

```diff
+## The Ethos Nexus
+
+The Ethos Nexus has three parts, Signal, Memory
+and Operation, each written in ethos.
+
+Its Memory is a registry of ethos names. Each
+repository carries one datom part naming its
+ethos sources; each part is loaded whole on the
+meta signal, and the parts together make the
+registry. The registry changes whenever a source
+is added, removed or renamed.
+
+A lowercase source name resolves through the
+registry to the path the generator writes.
+
+The content of an ethos file is fetched by name
+from the Source nexus, which keeps the hashes.
+
```

Below, unchanged:

```text
## Sources

01a02a34 ethos
```

If question 1 rules H, the last paragraph is replaced by:

```diff
-The content of an ethos file is fetched by name
-from the Source nexus, which keeps the hashes.
+Each registry entry holds the blake3 of its
+containing source; the content of an ethos file
+is fetched by name from the Source nexus.
```

If question 3 amends, "each part is loaded whole
on the meta signal" reads "parts and their entries
are changed on the meta signal".

### D2. The registry line, with the fork filled

Target: psyche-skills/vision/ethos.md, the Imports
section. Place: after the inline-import paragraph,
before "## What a declaration turns into". This is
the line approved on 2026-10-10, with ⟨the fork⟩
filled by question 2's ruling.

Removed: none.

Above, unchanged:

```text
A type may be declared over a type from a source in place, with no entry in the imports section: `Topic.custom:Name` declares `Topic` over the type `Name` from the source `custom`. The source is known twice: its first letter is lowercase, and a colon follows it.

```

Added, with one of the three fillings:

```diff
+A lowercase source names an entry of the
+registry. What the generator writes for a name
+from `core` is ⟨the fork⟩.
+
```

a. the name fully qualified from the one crate the
   Nexus is configured with for `core`
b. the path that `core`'s registry entry names, as
   for every other source
c. nothing: `core` is not a source, and a name from
   it is refused

Below, unchanged:

```text
## What a declaration turns into
```

### D3. Sources

Target: psyche-skills/vision/ethos.md, the Sources
section, appended after its last line.

Above, unchanged:

```text
88475f ethos
d5df1d ethos
```

Removed: none.

Added:

```diff
+081064 ethos
+73ada7 nexus
```

**Ruling.** 1: the later words, or H. 2: a, b or c.
3: confirm, or amend. 4: keep, or rename, name by
name. D1, D2 and D3 land with those answers. Or
amend any line.
`````

The four questions asked (hash home; core fork; whole-part loading; coined names): lines 341-517, no ruling.

### B.14 flows/081064/books/sources-registry-2.md  «Sources and the registry», second edition

Comments on this edition: none found. On the 1st edition (flows/d5df1d/books/sources-registry.md, artifact RX6W2WyacPbRaubsz5qgbp) the living, 2026-10-10T15:22, on its D1 registry line ("A lowercase source names an entry of the registry. What the generator writes for a name from core is ⟨the fork⟩."):

> Yes this is good and now we need to define the anatomy of that registry and use the same atomically updatable approach. The registry can be populated from multiple sources using the datom files that can be in the repositories that essentially wrap all of the data in that particular repository and can be updated by whoever updates that repo. It can then be loaded along with other repositories to create a full registry.

Same thread, on the question "One registry type ..." (2026-10-10T15:30): "This is actually really interesting. We could just make a registry or sources. We could make a Nexus called sources and we just put it all there. It can refer to a certain Git with a certain revision and we keep our own Blake3 hashes." and on "Two registry types ..." (15:31): "I think it's easier to just make the nexus for all the sources and reuse it for all components, then we only have one place to fix the sources aspect." Reading (flows/081064/log.md line 17, flows/65f93a/reports/package.md Appendix A): the "Yes this is good" sits on the D1 line itself; the core fork stays open, so the registry line has not landed (origin/main vision/ethos.md Imports ends at the inline-import paragraph). No ruling on any of the three sides of the core fork.

Proposal 1 (the registry line with the core fork, sides a/b/c): UNRULED (parent line approved in the 1st edition, fork open, not landed).
Proposal 2 (fetching and resolving are split): UNRULED; the Nexus-called-sources comments above support it but were made on the 1st edition's question 2, not on this proposal.

`````text
### Proposal 1. A source names a registry entry

Removed lines: none.

Added: one paragraph, one of three sides. Every
side is shown on this file:

```
Library
[]
[ Topic.core:Name ]
[]
[]
```

Each side was built as a candidate on the
generator's main line and passed its checks; that
is the claim of flows/1d0733/reports/q8-ac.md and
q8-b6.md, not witnessed here.

Side a. `core` is a crate of its own; the generator
writes core's name from that crate. No crate holding
core's Rust is named; `ethos_core` stands in for it.

```
+A lowercase source names an entry of the
+registry. What the generator writes for a name
+from `core` is that name fully qualified from
+core's own crate, never Rust's `core`.
```

Wrong, then right:

```rust
pub type Topic = core::Name;
pub type Topic = ethos_core::Name;
```

Side b. `core` is one registry entry like any other;
its entry names a Rust path, and the generator
writes that path. A source with no entry is refused.

```
+A lowercase source names an entry of the
+registry. What the generator writes for a name
+from `core` is the Rust path that the registry
+entry for `core` names.
```

Entries, then what is written:

```
[ { core ethos_core }
  { flow signal_flow } ]
```

```rust
pub type Topic = ethos_core::Name;
```

Side c. `core` is not a source; a name sourced from
it is refused where the source is read. This also
refuses `Topic.core:Name`, the key in the registry
example of flows/d5df1d/vision/ethos.md.

```
+A lowercase source names an entry of the
+registry. What the generator writes for a name
+from `core` is nothing: `core` is not a source,
+and a name sourced from `core` is refused.
```

Wrong, the refusal it meets, then right:

```
[ Topic.core:Name ]
```

```
Conceptual.{ [ 1 1 0 1 0 ] Source.core }
```

```
[ Topic.custom:Name ]
```

Impurities discarded: none.

Ruling asked:

1. Land side a as written.
2. Land side b as written.
3. Land side c as written.
4. Amend, by line.

### Proposal 2. Fetching and resolving are split

Removed lines: none.

Added, after Proposal 1's paragraph:

```
+A source is fetched whole, as a snapshot, by
+the Source nexus. The Ethos nexus resolves a
+lowercase source name through the registry.
```

Impurities discarded: none.

Ruling asked:

1. Land as written.
2. Amend, by line.
`````

### B.15 flows/081064/books/bytes.md  «Bytes in ethos»

Comments on this book: none ("No comments." flows/d68c82/reports/comments-books-evening.md line 28). Bearing, comment on «The Source nexus» (flows/d68c82/reports/comments-books-evening.md lines 43-48): "I guess what you're saying is you're going to use 4 64-bit integers but Blake3 is already a type somewhere. This is interesting. We need a way to essentially refer to Rust types from Ethos, which I guess we already do. Maybe it's just a special import syntax: a special way to write syntax, which means this comes from Rust." / "Also if you felt compelled to use 4 integers instead of an array of bytes, then does that mean you thought the Ethos syntax didn't allow you to represent this as an array of bytes? Maybe we represent it in Ethos and then it also just corresponds to the Rust type so that we can see that's an array of bytes in Ethos. That sounds complicated and since we're trying to get started on all of the infrastructure, I wouldn't push too hard on that but it's worth just writing in Notion I guess." No choice ruled. Not landed (origin/main intrinsics list has no Byte or Bytes). One proposal, three choices, plus Sources lines (`058f16 source`, `d4ae97 datom`: RULED-REJECTED, Bearing 4). Mark: UNRULED.

`````text
## Proposal: a statement on bytes in Imports

Target: psyche-skills/vision/ethos.md, section
"## Imports", right after the intrinsic list.

Above, as it stands:

An import names a source and a type: `protos:String` or
`protos:[ String Integer ]`. An explicit import and an intrinsic name
mean the same thing. Intrinsic names known without import: String,
Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self.

### Choice 1: a Bytes intrinsic

```diff
+
+Bytes is an intrinsic known without import: one
+value that is a vector of bytes, of fixed or open
+length. In memory it is a vector of bytes; in
+datom it is written in an alphanumeric encoding.
```

```
Library
[]                         ; imports
[ Blake3.Bytes             ; types: the hash as
  SourceName.String        ;   bytes
  Source.{ SourceName      ;   a source and its
           Blake3 } ]      ;   hash
[]                         ; traits
[]                         ; associations
```

`Blake3.Bytes` names the hash over the new
intrinsic. How a fixed length, 32 for Blake3, is
written in ethos is not chosen by this statement.

```
; datom, in a position expecting Blake3
; the run is illustrative: its length
; follows the encoding, not chosen here
k3m9q2x7ra4bf8nd5wp1ct6ve0zy2hsg
```

### Choice 2: a Byte intrinsic and Vector<Byte>

```diff
+
+Byte is an intrinsic known without import: one
+byte. A run of bytes, a hash among them, is
+Vector<Byte>.
```

```
Library
[]                         ; imports
[ Blake3.Vector<Byte>      ; types: the hash as a
  SourceName.String        ;   vector of Byte
  Source.{ SourceName      ;   a source and its
           Blake3 } ]      ;   hash
[]                         ; traits
[]                         ; associations
```

No new container: bytes ride the existing Vector.
A datom vector is written as its elements in
brackets, so unless Vector<Byte> is given its own
datom form, the hash is written as 32 numbers.

### Choice 3: no new intrinsic

```diff
+
+Ethos has no byte intrinsic. A hash is a struct of
+Integers: a 256-bit hash is four.
```

```
Library
[]                         ; imports
[ Blake3.{ Integer         ; types: the hash as
           Integer         ;   four Integers
           Integer
           Integer }
  SourceName.String
  Source.{ SourceName      ;   a source and its
           Blake3 } ]      ;   hash
[]                         ; traits
[]                         ; associations
```

This is the Source design's draft as it stands.
The Integers are signed, their order is chosen by
hand, and the type does not say bytes.

Below, as it stands:

```
Library
[ protos:[ String Textualizable ]  datom:Datom ]   ; imports
[]                                                 ; types
[]                                                 ; traits
[]                                                 ; associations
```

## Distillation

Proposed skill lines, per choice:

Choice 1. psyche-skills/vision/ethos.md, "##
Imports", after the intrinsic list: the four lines
of the Choice 1 statement, opened by a blank line;
Sources gets `058f16 source` and `d4ae97 datom`.

Choice 2. psyche-skills/vision/ethos.md, the same
place: the three lines of the Choice 2 statement,
opened by a blank line; Sources gets
`058f16 source` and `d4ae97 datom`.

Choice 3. psyche-skills/vision/ethos.md, the same
place: the two lines of the Choice 3 statement,
opened by a blank line; Sources gets
`058f16 source` and `d4ae97 datom`.

Sources:

058f16 source
d4ae97 datom

## Ruling

1. Choice 1: a Bytes intrinsic, a vector of bytes
   of fixed or open length, shown in datom in an
   alphanumeric encoding.
2. Choice 2: a Byte intrinsic; bytes are
   Vector<Byte>.
3. Choice 3: no new intrinsic; a hash is four
   Integers.

Or amend by line.
`````

### B.16 flows/081064/books/prototype-name.md  «The prototype name»

Comments on this book: none ("No comments." flows/d68c82/reports/comments-books-evening.md line 22). Origin comment, 1st-edition registry book thread, 2026-10-10T15:25 (flows/d68c82/reports/comments-2026-10-10.md; flows/d68c82/vision/naming.md):

> In Protos languages like datom and Esos for things that are not types or traits, we are going to use uncapitalized. It's going to be camel case because we do PascalCase for defined objects in the language and we do variants. If there's a string position in datom and it starts with a capital, that's okay because we have a different type that's kind of like a string but it has to be checked whenever we create a new one. This is the Prototypic name or whatever, the prototype name, which is an uncapitalized identifier. It's going to have to be composed of words so we need to put together some kind of fancy check. Well not that fancy, I guess.

That states the rule; it does not choose between the book's Choice 1 (vision/protos.md "Names" section plus pointer lines) and Choice 2 (per language). Not landed in any of the three files (no "Names" section in origin/main vision/protos.md; nothing in vision/ethos.md Naming or vision/datom.md Strings). Question 3 (may a capability input name a concrete type) and the "is prototype name core:Name" question: unanswered. The Sources lines (`081064 ethos`, `445410 flow`): RULED-REJECTED (Bearing 4). Mark of the proposal: UNRULED.

`````text
## Proposal: where the casing rule lands

This distils flows/081064/vision/ethos.md,
2026-10-10, "uncapitalized names in Protos
languages: the prototype name". It also draws on
flows/445410/vision/flow.md, 2026-10-09, "Topic
names are camelCase expressions", which agrees with
it.

The statement says datom and ethos, and calls them
Protos languages. So it can land in two shapes.

### Choice 1: one shared rule in vision-protos

The statement becomes a new section of
vision-protos.
vision-ethos and vision-datom each get one line that
points to it. In vision-protos, "What Protos knows"
already shows capitalization as part of textual
structure. The same section also says protos does
not know what anything is, and a prototype name is a
type.

Target: psyche-skills/skills/vision-protos.md,
between
the end of "## Structure" and "## String, escape,
error".

Above, as it stands:

real protos delimiter. The key-value map, which the guillemets once
delimited, is dropped entirely from protos and its dialects.

Added:

```diff
+## Names
+
+In the Protos languages, datom and ethos among
+them, a defined object, a type or a trait, and a
+variant are named in PascalCase; every other name
+is camelCase, uncapitalized, and is a prototype
+name: a type like a string, an uncapitalized
+identifier composed of words, checked whenever one
+is created. A string position in datom takes a
+string that starts with a capital; it stays a
+string.
+
+```
+; ethos
+Library
+; imports: none
+[]
+; types: the name, held as a string; why a
+; candidate is refused; a reply holding a name
+[ PrototypeName.String
+  Refusal.[ Capitalized
+            NotWords ]
+  Reply.[ Registered.{ PrototypeName String }
+          Pending ] ]
+; traits: a name is made from a string, or
+; refused
+[ Checked.[ create:{ [ String ]   ; <- question 3
+                     [ Result<Self Refusal> ] } ] ]
+; associations: the name bears the check
+[ PrototypeName.[ Checked ] ]
+```
+```
+; datom, in a position expecting Reply
+Registered.{ protosParser ProtosParser }
+```
+
```

Below, as it stands:

## String, escape, error

Target: psyche-skills/skills/vision-protos.md, at
the
end of "## Sources".

564f55 datom
564f55 signal

```diff
+081064 ethos
+445410 flow
```

Target: psyche-skills/vision/ethos.md, at the end of
"## Naming".

and ethos code are switched between so often; once ethos is the
authored language that debt is removed.

```diff
+
+Name casing is stated in vision-protos, Names.
```

## Identity

Target: psyche-skills/skills/vision-datom.md, at the
end of "## Strings", after its example block.

cannot be mistyped for it, and point, so the ends are visible at any
size.

\`\`\`
Ada     TheBuildPassedOnTheThirdTry     «12 Rue de la Paix»
\`\`\`

```diff
+
+Name casing is stated in vision-protos, Names.
```

## Syntax

### Choice 2: the rule lands in each language

The statement lands in vision-ethos and in
vision-datom, each time with that language's code.
vision-protos does not change.

Target: psyche-skills/vision/ethos.md, at the end of
"## Naming".

and ethos code are switched between so often; once ethos is the
authored language that debt is removed.

```diff
+
+A defined object, a type or a trait, and a variant
+are named in PascalCase; every other name is
+camelCase, uncapitalized, and is a prototype name:
+a type like a string, an uncapitalized identifier
+composed of words, checked whenever one is created.
+
+```
+Library
+; imports: none
+[]
+; types: the name, held as a string; why a
+; candidate is refused; a reply holding a name
+[ PrototypeName.String
+  Refusal.[ Capitalized
+            NotWords ]
+  Reply.[ Registered.{ PrototypeName String }
+          Pending ] ]
+; traits: a name is made from a string, or
+; refused
+[ Checked.[ create:{ [ String ]   ; <- question 3
+                     [ Result<Self Refusal> ] } ] ]
+; associations: the name bears the check
+[ PrototypeName.[ Checked ] ]
+```
```

## Identity

Target: psyche-skills/vision/ethos.md, at the end of
"## Sources".

e51411 ethos
88475f ethos
d5df1d ethos

```diff
+081064 ethos
+445410 flow
```

Target: psyche-skills/skills/vision-datom.md, at the
end of "## Strings", after its example block.

cannot be mistyped for it, and point, so the ends are visible at any
size.

\`\`\`
Ada     TheBuildPassedOnTheThirdTry     «12 Rue de la Paix»
\`\`\`

```diff
+
+A head is a variant, PascalCase; every other name
+is camelCase, uncapitalized, and is a prototype
+name: a type like a string, an uncapitalized
+identifier composed of words, checked whenever one
+is created. A string position takes a string that
+starts with a capital; it stays a string.
+
+```
+; Reply: an enum of
+;   Registered.{ PrototypeName String }, Pending
+Registered.{ protosParser ProtosParser }
+```
```

## Syntax

Target: psyche-skills/skills/vision-datom.md, at the
end of "## Sources".

542442 datom
f38926 meaningLanguage

```diff
+081064 ethos
+445410 flow
```

## Distillation

Proposed skill lines, per choice:

Choice 1.
- psyche-skills/skills/vision-protos.md: new section
  "## Names" (the statement, the ethos declaration,
  the datom line), placed before "## String, escape,
  error"; Sources gets `081064 ethos` and
  `445410 flow`.
- psyche-skills/vision/ethos.md: one line at the end
  of "## Naming": Name casing is stated in
  vision-protos, Names.
- psyche-skills/skills/vision-datom.md: the same
  line
  at the end of "## Strings".

Choice 2.
- psyche-skills/vision/ethos.md: the statement and
  the ethos declaration at the end of "## Naming";
  Sources gets `081064 ethos` and `445410 flow`.
- psyche-skills/skills/vision-datom.md: the
  statement and the datom example at the end of
  "## Strings"; Sources gets `081064 ethos` and
  `445410 flow`.

Sources:

081064 ethos
445410 flow

## Ruling

1. Choice 1: the shared rule in vision-protos, with
   one pointer line each in vision-ethos and
   vision-datom.
2. Choice 2: the rule in vision-ethos and in
   vision-datom separately.

3. May an ethos capability input name a concrete
   type? Then the right form stands as the vision.
   Or is the prototype name's check written over Self
   (form a), or over a trait (form b)? The line
   `[ String ]` marked `<- question 3` in the
   proposal blocks is the line this decides; the
   marker is the book's and does not land.

Also: is "prototype name" the name you keep, and is
the prototype name the type core:Name?
`````

## C. What could not be found

- Any comment by the living on «The Ethos vision» 1st edition or 4th edition; any ruling on 3rd P4-P19 or on any of the 4th edition's 18 proposals; any ruling on «The Ethos syntax» P9.
- A written "land" or "reject" ruling for the 3rd-edition comments themselves beyond the d68c82 log line 2028 ("Comments on Ethos 3rd: ... Relayed to 65f93a") and the order for a 4th edition and a syntax book. The syntax rulings (log line 2040) are summarized, not itemized, with "rejected or amended" not split per proposal.
- Any comment by the living on: types, invariants, two-heads, no-tuple, stale-examples, alias-examples, golden-ethos-4, special-representation, type-ethos, vector-delimiter, ethos-nexus, sources-registry-2, bytes, prototype-name, distilled-lines-gone-stale (searched flows/*/log.md, reports/*comment*, vision, notion; artifact ids grepped).
- Any ruling on the `core` fork.
- The local psyche-skills clone has no skills/vision-datom.md or skills/vision-protos.md on origin/main (moved to vision/datom.md and vision/protos.md). Items 1, 2, 3, 6, 7 of «Distilled lines gone stale» sit in other vision files and were checked by grep only.
