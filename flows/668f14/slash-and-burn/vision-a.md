# Slash-and-burn sweep A: vision modules (evidence for the judge)

Counts are by statement or paragraph, code blocks and diagrams counted as one each. Quotes are exact.

## account
3 statements, 1 candidate (a second is borderline and left kept).

- > The flow that finds the cause writes the account, and sends it to Psyche, which publishes it as a book, so it reaches him through the book list.

  `procedure`: who sends what to whom is routing that belongs in a role or the book tooling. Harm 1.

## anatomy
4 statements, 0 candidates. Both sections are what an engineer would state unprompted. (Weakest: "though today it is done by an outside program the machine has not been aware of", a one-off detail, harm 1, kept.)

## archive-ethos-monolith
8 statements, 8 candidates. The module describes itself as retired; every paragraph is `stale`. Harm 1 each unless noted (a model loading it may chase a dead stage, so the module as a whole is 2).

- > Retired on landing by flow fe34eb, 2026-09-10. The living ruled Ethos
  > Monolith and Ethos Zero one stage under two names.
  > What still stands is carried by Vision/ethos.md,
  > heading Zero; the words are kept here.

  `stale` and `too specific` (flow id, date). Harm 1.
- > All our systems will be Nexuses, and the correct three-nexus ethos
  > stack is the desired stack — but it is too complex to go for
  > directly, and the previous effort devolved into agent hallucinations
  > for lack of proper instructions. The monolith is the short-term path
  > that brings ethos into production: the earlier stack's code is kept,
  > left in place, frozen, and new repositories carry a simplified path
  > from Ethos straight to Rust.

  `stale`. Harm 2 (describes a short-term path as if live).
- > First named ethos-rust, the schema-rust analogue; then renamed
  > ethos-monolith: it has no nomos and no logos component and goes
  > straight to Rust — a monolith.

  `stale`. Harm 1.
- > The monolith will itself be a Nexus. Nexus by itself names our
  > specifically designed daemon — distinct from Nexus Core, the
  > runtime engine — and executables are named component-nexus.

  `stale` and `too specific` (naming scheme). Harm 1.
- > An incremental implementation and bootstrap process, so that ethos
  > and datom get written and read as soon as possible, at full correctness,
  > and components start being written in ethos.

  `stale`. Harm 1.
- > The Signal, Nexus, SEMA vocabulary and principles are kept, and
  > how they are used and implemented is designed afresh. Nexus is
  > authored in ethos so its main operations are visible. Sema is the
  > database engine, authored in ethos so the stored types are visible;
  > it matters more than nexus, because operational editing should yield
  > database migration operations along with the editing operation.

  `stale`; `duplicate` of vision-memory / vision-nexus. Harm 1.
- > Ethos serves new work in place of legacy schema once the monolith is
  > ready to use; readiness is witnessed.

  `stale`. Harm 1.

## aspects
4 statements, 3 candidates.

- > Flows of the same topic talk at the same layer across aspects, so a Psyche topic Secondary and the Mind Secondary of that topic speak directly. Field reaches Psyche through Mind, unless Psyche has just spoken to Field. This holds for every aspect.

  `not common sense`: an arbitrary routing rule with a surprising exception. A flow may follow it mechanically. Harm 2.
- > Within an aspect, a flow speaks only to the layer next to it: a Quaternary to its Tertiary, a Tertiary to its Secondary, a Secondary to its Primary.

  `procedure`: a fixed chain of command a flow follows blindly; the "only" is the harm. Harm 2.
- > The tracker, a Quaternary, reaches any Secondary directly, in any aspect, and a Primary only through its Secondary.

  `too specific`: one named role's exception. Harm 1.

## belief-modules
About 24 statements, 12 candidates.

- The first mermaid diagram (starts `flowchart TB` / `a["the living"] -- "reviews psyche proposals, line by line" --> b["Psyche: spirit, intent, vision"]`, ends `p["a periodic book or audit"] -- "reads it as a whole and checks it against Mind and Psyche" --> fl`).
  `too specific`: a dense org chart of review flows; a sensible reader needs only "psyche rules over knowledge, knowledge over compensation". Harm 2 (it is the module's largest block and a flow will treat it as binding procedure).
- > Knowledge modules are audited from time to time for truth and currency against practice.

  `procedure`: vague schedule, no actor. Harm 1.
- > A subject the living reviews or asks about has a module, on its topic or a broader one, with room to hold it.

  `not common sense`: unclear meaning; "room to hold it" is unmotivated. Harm 1.
- > The code important to a vision lives in that topic's vision module. The invariant code of Flow, which the Psyche core Primary sees going into the Flow Nexus, lives in vision:flow; a Chronos invariant lives in vision:chronos.

  `too specific` (module names, particular flows). Harm 1.
- The second mermaid diagram (`a["his vision"] -- "is inferred into" --> b["the proposal: prose + invariant code"]` ...).
  `duplicate` of the two preceding statements ("A vision module may be substantial..."). Harm 1.
- > A module declares its placement: the system prompt, or loaded on demand. A skill is the harness's interface for an on-demand module.

  `too specific`: per-harness mechanic. Harm 1.
- > In the long term, intent is placed directly in the system prompt.

  `not common sense`: a future plan stated as belief; says nothing about what now holds (the module itself says "states what holds now"). Harm 1.
- > The vocabulary is context, belief modules and context building.
  > A skill is the legacy name, one harness name for things that differ, becoming obsolete as harness infrastructure improves.

  `stale`: the module calls its own term legacy. Harm 2 (the system's skill list is full of "skill" and this teaches the opposite).
- > A context repository holds one folder per module type, each named for its type. A file is named by its subject alone, and its folder gives its type.

  `too specific` (directory layout). Harm 1.
- > A module is named by its type and its subject. A directory structure gives each type its own directory; a single-string name without whitespace puts the type first, then a colon, then the subject, as vision:book.

  `too specific` (naming syntax). Harm 1.
- > A context repository holds one section of role modules per layer, Primary, Secondary, Tertiary and Quaternary, and may hold sections for specialized topics.

  `too specific` (repo layout). Harm 1.
- > Context lines are richly annotated, because lines of very different categories share one module and are otherwise given the same weight. Separating modules into kinds such as vision and intent is the first, crude form of that annotation.

  `not common sense`: says "richly annotated" while the lines are not; a claim about what is not so. Harm 1.
- > Removal comes before addition.

  `not common sense` as a bare mechanic; and the last diagram (`a["a contradicted line"]`... `e -- "then places" --> g["the new line"]`) and "A line that a module contradicts is edited by removing the contradicted line first." say the same: `duplicate` within the module. Harm 1.

## blocking
3 statements, 1 candidate.

- The mermaid diagram (`a["a task"] -- "needs the output of another? yes: waits for" --> b["its output"]` ...).
  `duplicate` of the first sentence ("A flow waits for one thing..."). Harm 1.

## book
About 22 statements, 14 candidates. The module's content is largely restated by vision-book and compensation-book-making, which are in the system prompt.

- > A book carries belief modules, as they stand and as they are proposed to change; its sources live in its reference file.

  `duplicate` of vision-book ("A book carries belief modules..." and the references-file sentence). Harm 1.
- > A figure shows how a thing moves, one question per figure, readable in seconds. Its grammar: a box is a thing or a collection; an arrow is a one-way relation carrying a verb, so that box, verb, box reads as a sentence; nearness and enclosure are kinship; top to bottom is order; colour carries a role or is absent. A figure is boxes joined by verbed arrows. A diagram in a book's source is a Mermaid flowchart in that grammar, drawn so a phone shows it; every sketch carries its arrows before it is sent. The published book shows the figure drawn from the Mermaid source by a Tertiary or Quaternary subflow given the grammar with the sketch; the figure keeps every box, label and arrow, and says only what the source says; a figure that lost an arrow is returned. A sizable book carries several figures.

  `duplicate` (vision-book, "A figure shows how a thing moves..."); `procedure` (Mermaid, subflow). Harm 2 (two near-identical copies in context can drift).
- > Prose is shown as rendered text. A code block holds code alone, and it may scroll sideways.

  `duplicate` of vision-book. Harm 1.
- > A book is belief modules in the forms below, each under its repo › path; its headings, naming the module and the kind of change, are the only words it has of its own.

  `duplicate` of vision-book. Harm 1.
- > A module shown whole, as it stands, situates the landing.

  `duplicate` of vision-book. Harm 1.
- > A module shown beside another, both as they stand, serves comparison: psyche with knowledge, with compensation.

  `duplicate` of vision-book. Harm 1.
- > A line added shows in green.

  `duplicate` of vision-book. Harm 1.
- > A line removed shows in red.

  `duplicate` of vision-book. Harm 1.
- > A line replaced shows its removal and its addition together, and only the changed words are marked.

  `duplicate` of vision-book. Harm 1.
- > A new module shows whole in green, under the path it will have.

  `duplicate` of vision-book. Harm 1.
- > A module deleted shows whole in red, with a Destroy or Archive mark.

  `duplicate` of vision-book. Harm 1.
- > A line moved between modules is one proposal headed by both paths: the line in red under the module it leaves, the same line in green under the module it enters.

  `duplicate` of vision-book. Harm 1.
- > A dependency changed shows in the module's front matter: the dependency removed in red, the dependency added in green.

  `duplicate` of vision-book. Harm 1.
- > A figure shows as proposed for the module it will live in.
  >
  > A figure proposed for a module shows under that module's path in green, as an added line does; a figure it replaces shows beside it in red.

  `duplicate` of vision-book. Harm 1.
- The mermaid diagram (`a["belief module"] -- "stays" --> b["shown whole or beside another"]` ...).
  `duplicate` of the ASCII figure in vision-book. Harm 1.
- > Code in a book is shown as code, labelled with its language, plain. Ethos and datom in a book are written in the vertical form.

  `too specific` ("vertical form"); partly `duplicate` of compensation-book-making fences. Harm 1.
- > A figure shows one thing, where the idea has a shape, and its colours and marks mean the same in every book.

  `duplicate` of vision-book "Pictures". Harm 1.
- > Every figure, in a book or in a module, is the SVG drawn from a Mermaid flowchart in the figure grammar. A sketch met anywhere is converted to a Mermaid figure.

  `procedure` (tool format); conflicts with vision-book/compensation-book-making, which draw figures from unlabelled box-and-arrow sketches, not Mermaid. Harm 3 (a flow may redraw sketches in a format the builder rejects).

## chronos
About 13 statements, 7 candidates (a domain the owner is designing; kept lines are the core idea).

- > The nodes and the apogee are the true points; the aphelion is the Sun's place when it is farthest from the Earth.

  `too specific`: astronomical detail a model knows. Harm 1.
- > The location is the one a request carries, else the standing location set over the meta socket.

  `too specific`: wire mechanic. Harm 1.
- > Chronos reckons from JPL's DE440 ephemeris, for the years 1550 to 2650.

  `too specific`: version and range, implementation detail. Harm 1.
- > Everything is tropical, the nakṣatras included: Aśvinī begins at 0° Aries.

  `too specific`: a one-off fact (kept core is "tropical"). Harm 1.
- > Everything is reckoned around the ecliptic of the Sun.

  `not common sense`: unclear; "around the ecliptic of the Sun" is unmotivated. Harm 1.
- > Chronos answers arcs. Sign and nakṣatra are derived from an arc, absolute or relative, by the trait methods of the Library, which any client calls on an arc it holds.

  `too specific`: API shape. Harm 1.
- > A lunation of 31° between the Sun and the Moon reads as Taurus.

  `too specific`: a one-off example, and contradictory-looking (a Sun-Moon arc as a sign). Harm 1.
- > Chronos is the golden example: a simple, idiomatic Nexus with a full ethos specification, built on Ethos and the Nexus.
  > Flow is implemented from it, then the other nexuses.

  `procedure`: build order. Harm 1 (borderline).

## clojure
1 statement, 1 candidate.

- > The Clojure translation preserves the anatomy declared in Ethos: named types, struct positions, variant identity and payload, and nested containers. One shared construct mapping defines their Malli schemas and Clojure data representations, including how Datom values become those Clojure values. Each representation keeps enough information to recover the same typed value.

  `too specific` (Malli, construct mapping): per-tool mechanics. Only the final sentence ("keeps enough information to recover the same typed value") is common sense. Harm 1.

## collaboration
6 statements, 3 candidates.

- > A flow that hands work to a Primary, or to any flow above it, first gathers everything that work needs — his words whole, his comments on the books, the records and the files — and sends it in one message, complete. A middle layer carries his words and context whole; the higher layer judges alone.

  `procedure` and `not common sense` in part: "the higher layer judges alone" may make a flow dump everything on the Primary (wasted attention); partly `duplicate` of intent-living-interaction. Harm 2.
- > A ruling a Secondary relays from its Primary carries the Primary authority, and the flow that receives it acts on it without asking the Primary again.

  `not common sense`: a flow acts without checking, even if the ruling looks wrong; a sensible engineer verifies a surprising order. Harm 3.
- > A relay that conflicts with a ruling by an identified authority leaves that ruling in force until its own authority and supersession are shown; the conflict is reported, the work goes on.

  `procedure`: a protocol clause. Harm 2.

## committing
4 statements, 3 candidates.

- > The commit call is explicit with file paths. A flow commits the files
  > it edited, and usually works only in its own flow directory.

  `too specific`: per-tool mechanic and a layout detail; the common-sense core is "commit what you edited". Harm 1.
- > A commit
  > made without paths takes the whole working copy, and is made only
  > while the whole repository is locked, when nobody else may be
  > editing.

  `procedure` (jj/VCS mechanic and locking). Harm 2.
- > For now Primary is one workspace shared by every flow, so a change there is made in its one checkout. This short-term vision ends when flows get workspaces of their own.

  `stale`-in-waiting: a self-declared temporary; `too specific`. Harm 1.

## criomos
12 statements, 7 candidates.

- > CriomOS is made more modular; an anatomy of it shows what should be taken out.

  `not common sense`: vague aspiration. Harm 1.
- > CriomOS has a hardware type, so that it supports several kinds of hardware, the Librem 5 Linux smartphone among them; a module may be gated on it.

  `too specific`: one device, one gating mechanism. Harm 1.
- > A fix that only some hardware needs is a value in the cluster data, marked by the chip or part that makes it necessary.

  `too specific`: a placement rule with a data-layout mechanic. Harm 2.
- > A library reads the cluster's list of its hardware and answers, by processor, model and variant, which fixes a computer needs.

  `too specific`: implementation description. Harm 1.
- > The harnesses and their desktop apps are kept stock in at least one version, under their ordinary executable names.

  `not common sense`: unmotivated, arbitrary. Harm 2.
- > A service is updated by bringing it up at its latest version.

  `not common sense`: contradicts careful practice (pinning, testing). Harm 2.
- > A new artifact does not open a browser tab on its own.

  `too specific`: one-off UI preference (a negative, per the module crystallization's own rule). Harm 2 (a flow may refuse to show him a page he asked for). 

## crystallization
About 30 statements, 15 candidates. Most of the module is the procedure of a pipeline that belongs in the records-cleaner and crystallizer roles.

- > A working instruction logged as vision is a vision impurity. It may
  > sit in a log beside valid vision; when crystallization finds it, the
  > impurity is dissected out of the log and destroyed, and the valid
  > vision around it stays.

  `procedure`. Harm 1.
- > Impurities come out in the course of crystallization: a crystallization
  > proposal points out the impurities it dissects out, and the living
  > rules on them with the statements.

  `procedure`; `duplicate` of the paragraph above and of "Impurities are hunted..." Harm 1.
- > A crystallization proposal says, for every statement, the topic it goes
  > to; a statement under the wrong topic is corrected by a crystallization
  > edit of its own.

  `procedure`. Harm 1.
- > A crystallized statement states its subject in its own voice.

  `not common sense`: unclear on its face. Harm 1.
- > Impurities are hunted by the records cleaner and fall through crystallization alike; every destruction is one commit line naming the record.

  `procedure` and `too specific` (commit line); `duplicate` of the two above. Harm 2.
- > A raw record whose every point a later record of his states better is superseded: it moves to the archive with one line naming the record that supersedes it, in a commit naming both. A record whose subject is gone from the system is irrelevant and archived the same way.

  `procedure`. Harm 1.
- > Crystallization re-articulates psyche records into self-standing statements and merges each with what is already crystallized, so the whole stays cohesive and the new reads as if always written with the original context. The model clarifies and purifies.

  `duplicate` of "A crystallized statement stands on its own words" and the earlier "carries what the living said". Harm 1.
- > A crystallization agglomerates records across flows that touch the
  > same topic. Records are considered one by one.
  > One record may serve many crystallizations; one crystallization may
  > draw from many topics.

  `procedure`. Harm 1.
- > A crystallized statement stands on its own words. A proposed change to a raw record — correction included — is proposed as a crystallization of its subject.

  `procedure`. Harm 1.
- > A statement is composed from the living's quoted words alone. Every term in a
  > crystallized statement is defined. Define the term first, or leave the statement raw.
  > A statement about code carries the code: a crystallized statement on a syntax, a type, a kind, or a wire form shows example code, because machines think in code and the next machine to read it must understand.

  `procedure`; `duplicate` of "A statement carries what the living said" and "Vision is logged from his words alone". Harm 2 (several overlapping "words alone" rules).
- > Vision code is written in the stacks the system is built in: Ethos and Datom first, then Rust and Nix; where a design depends on how any of them is used, the statement carries that code.

  `too specific` (stack list). Harm 1.
- > A crystallized statement lands as lines in a vision- or intent- skill's authored source. A ruling a crystallization lands in a skill is recorded by the landing itself. Intent enters an intent- skill only on the living's explicit word.

  `procedure`; `stale` ("skill" is called legacy in belief-modules). Harm 2.
- > The landing of a line archives the raw records it drew on, in the same commit; a record stays raw only while no line of it has landed.

  `procedure`. Harm 1.
- > A record's id is its originating session's short id and that
  > session's own count.

  `too specific`. Harm 1.
- > Crystallization is proposed on encounter, dispatched proactively by
  > the flow working a subject, or done in dedicated passes.

  `procedure`. Harm 1.
- > What the living says fresh while a crystallization is being composed is logged as a raw record as it is spoken, like any other psyche, and the crystallization draws on it like any other record.

  `procedure`. Harm 1.

## datom
About 50 statements and blocks, 10 candidates. The syntax, strings, containers, compose/derive and Meaning example code illustrate designed types and are kept.

- > Datom is the living’s own coinage for the new data notation, the
  > successor to NOTA and to the rejected name Dotos. The name was
  > chosen for its energetic power and to echo what the notation is:
  > data, strictly typed, super dense, no field names. The library is
  > datom-codec. Datomic names the conceptual layer abstractly, in speech about it.

  `too specific`: etymology and rejected names; `stale` (NOTA, Dotos). Harm 1.
- > Generating Rust is Ethos's duty, in today's division of labor. When
  > Ethos becomes the full authoring language, with Rustlang as its
  > assembly layer, Datom, the data dialect of the Protos family, may gain
  > an inline place in authored Ethos, the way Rustlang composes data
  > directly in code. That road is reached, or even floated, only with
  > explicit context: how, when, and where data yields Rust, stated
  > without ambiguity; until then the division stands as spoken.

  `not common sense`: a speculative future guarded by a gag rule ("or even floated"); a flow may refuse to discuss it. Harm 2.
- The `rust` block under "A datom is a form at a path" (`pub struct Datom { pub path: Path, pub form: Form }` ...) is wanted: illustrates the designed type. Kept.
- > Datom and Ethos are different languages that share an approach, not a
  > parser. What they may share is a substrate, kinds with a shared
  > implementation and types; the universal substrate machinery is homed
  > in protos, all dialects ride it, and datom is the pure-data dialect on
  > it. Ethos could come to depend on Datom for another reason: ethos
  > might be read as datom in one pass. Whether that is even possible,
  > given the situation and the actualization involved in parsing ethos,
  > is not settled, and the question is set aside for now.

  `duplicate` of vision-protos / vision-ethos; the last sentences are an open inquiry stated as belief. Harm 1.
- > Not yet; a written datom gives every position.

  and its block `Deploy.{ ouranos }     ; Arity.{ 2 1 }` (section "Omittable fields"). `not common sense`: a bare "not yet" with an example of an error that names a particular host. `too specific` (ouranos). Harm 1.
- > A program's configuration surface is the datom's shape itself, as the
  > ethos interface declares it: a data enum at the root whose variants
  > are the main operations. A variant's data carries what follows:
  > another enum where sub-operations are wanted, a struct or vector for
  > final options, and a struct may embed further sub-operations, or any
  > combination imaginable. Output is an enum, always; even the most basic
  > response interface is an enum: Success or Failure. The shape already
  > is the interface: datom creates the configuration options by its very
  > shape, and a CLI takes its whole configuration from its datom input. A
  > Nexus reply is written as its heads down to its data, and only what
  > carries data is written: an empty Locks observation is
  > Observed.Locks.[], the Observed variant, its Locks variant, the empty
  > vector; the layout of a nonempty payload is open.

  `too specific` (CLI and Locks reply detail) with an "open" tail; partly `duplicate` of vision-ethos and the Syntax section's `Observed.Locks.[]`. Harm 1.
- The block `Observed.Locks.[]    ; orchestrate's response: ...` / `Success              ; the most basic response: a variant carrying nothing` under "The interface shape".
  `duplicate` of the Syntax section examples (`Observed.Locks.[]` and `Pending`). Harm 1.
- > Everything moves to Datom: all of the stack, Horizon, Lojix, everything.
  > Datom's own line of descent is NOTA, which also
  > passed through the temporary name Dotos; that old notation stays
  > behind, frozen, and may be called legacy. Schema is the abandoned
  > ancestor of Ethos, not of Datom. The library is named datom-codec so
  > that datom is free for the datom nexus, which comes when there is more
  > to do: translating datom objects between formats, and a parsing cache
  > keyed by the content-addressed hash of normalized text.

  `stale` and `too specific` (history, named projects, future nexus). Harm 2 (a migration mandate stated as standing fact).
- > Meaning is postponed so that a working syntax lands as soon as
  > possible: today a parenthesized text lands as a plain String, with
  > the later type marked in code. The name Meaning smells of a verb; it
  > stands provisionally and is reopened together with the type.

  `stale`: the module's last line says the postponement is superseded. Harm 2.
- > The meaning language is now developed, and is defined in
  > Vision/meaning.md; that supersedes the postponement stated above.

  `stale`: a patch note that contradicts the paragraph it follows, left in place; the right fix is to rewrite the Meaning section and drop this line. Harm 2.
