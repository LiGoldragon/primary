Presentation.{ «Record state» }

# Record state

Created by Fable, inventory by Sonnet.

## What failed at my startup

A raw record is written once and nothing ever says what became of it. My launch gave me 7459f3's model-roles and proposal records, both landed and pushed hours earlier, because remembering picks by flow and depth, not by state. It gave me none of the 73 records across twelve flows that no module line answers yet, because they sit in other flows' files. 7459f3 patched this by hand: it renamed landed files to `archive-*.md` and put "Landed in …" on top of some. Twenty-five records are archive-named with no note; the rename moved them and said nothing.

## The design

The record is the thing; a file is only how a flow is handed context. A record that lands moves out of its open file into the archive file of the same topic, in a separate directory, and carries there one line saying what became of it: Landed, with the module and the commit, written by the lander in the commit that lands it; Superseded, by the record that overruled it; Refuted, with your reason. An open record carries nothing, and the open file is what a fresh flow reads whole. Location answers open or settled by one query; the line answers what became of it. The hand-renamed `archive-*.md` files are undone: their open records go back to the topic file, their landed ones to the archive with their line. In the long term the records live in the psyche nexus and the state is a field of the record.

The Ethos is found nowhere: both types are proposed, in Proposals 3 and 4 below. Today the line under an archived record's heading is written by hand as datom:

```datom
Landed.{ vision/proposal.md 5d81baa }
```

### Proposal 1: A landed record moves to the archive · psyche-context › vision/psyche.md

**Comment** Your words: a file is not a thing; the parts that are landed are moved into the otherwise fixed file, in a different directory, so what has landed and what is believed open are easy to query. The archive renames are undone.

+ ## A settled record moves to the archive
+
+ A raw record is open where it is written and carries nothing. When it
+ is landed, superseded or refuted it moves to the archive file of its
+ topic, in a separate directory, under one line that says which:
+ Landed, with the module and the commit, written by the lander in the
+ commit that lands it; Superseded, by the record that overruled it;
+ Refuted, with his reason. A file is never renamed to say what became
+ of its records. In the long term the records live in the psyche nexus
+ and the state is a field.

### Proposal 2: Remembering selects by state · psyche-context › vision/remembering.md

**Comment** Your words: you were given things already settled and not the things that were not settled. The launch gains an Open remembering; depth remains for the transcript.

+ ## A fresh flow receives what is open
+
+ A remembering of Open gives a fresh flow every open record of its
+ address, from every flow that wrote one, and a one-line index of the
+ archived ones: heading and state. Depth and named flows remain for
+ reaching a transcript.

### Proposal 3: Remembering gains Open · signal-flow › ethos/signal.ethos

**Comment** Found at line 259, the launch's remembering as it stands. The Open variant is added; the two that exist stay.

```diff
  RememberingDepth.Integer
- Remembering.[ Predecessors.RememberingDepth Custom.Vector<FlowId> ]
+ Remembering.[ Open                                 ; every open record of the address
+               Predecessors.RememberingDepth
+               Custom.Vector<FlowId> ]
```

### Proposal 4: The settled line has a type · psyche › ethos/memory.ethos

**Comment** Found nowhere. The psyche crate has no ethos yet; this is its first file, and the type of the line written by hand today. It is Memory because the records are what the psyche nexus will remember.

```diff
+ Memory
+ []                                              ; imports
+ [ ModulePath.String                             ; record types
+   Commit.String
+   FlowId.String
+   Heading.String
+   Settled.[ Landed.{ ModulePath Commit }        ;   the lander writes it, same commit
+             Superseded.{ FlowId Heading }       ;   a later word of his overruled it
+             Refuted.String ] ]                  ;   he said the thing is not wanted, and why
```

### Proposal 5: Code in a proposal is found or proposed · psyche-context › vision/proposal.md

**Comment** The belief behind the bare Ethos block. vision:datom says a datom newly made is shown with its Ethos; nothing said that the Ethos of a design is itself proposed and must say so. vision:proposal has no line on code at all, so a design's Ethos stood between the proposals as an illustration. Your words: it has to have been found because it is not shown as an addition.

```diff
+ ## Code in a proposal is found or proposed
+
+ Every line of code in a proposal is one of two things, and says which:
+ found, with the file and line it stands at today; or proposed, shown
+ as an addition at the place it will stand. The Ethos of a design is
+ proposed code. No code stands bare.
```

## What is open now

Sonnet matched every record since 2026-10-26 against psyche-context by distinctive phrase; the modules paraphrase, so Open means no line found, not proof of none. Of 136 records: 73 open, 34 landed, 29 archive-named. The open ones, by flow:

- 74e4d1 (10-26), fourteen: belief editing is always approved, a correction is not written as its instance, teaching needs examples, an audit for unapproved edits; restrictions come from layering, not code, who may message whom is configuration, the restriction feature is left out for now; roles are data queries; Flow delivers regardless; Ethos Notebook; every flow has Ethos and Datom training; raw-run Flow 0.40; implications extracted by layered flows; "all your aspects".
- bf8ae0 (10-27), twenty-two: hourly pulse, a flow wakes itself under an hour, reminders are a Flow feature, a meta operation to order a restart, the rebuilt Flow implemented then tested then used, Codex ramped up; signal out of the Nexus is proper datom, a proof-of-concept message nexus; a tool that checks the vision's code is in the implementation; file modules become skills holding questions; a refresh tool; what is important: vision and intent read as vision, notion less; the one refusing committer; a fresh flow hunts horrible things hourly while he is away; chat or book: silence and size; three CriomOS faults: dark theme at five, battery lost asleep, screen never locks.
- c637a5 (10-27), twelve: the design is the book, reports are books, inferring vision is writing the book; the overnight rebuild; an idle Mind wastes Codex; implementers are not handed raw psyche logs; flows still log everything after he ruled against it, psyche records stay, dated addenda on the design report are the logging he means.
- 9aaaba (10-28), eight: the eventual design is a module of its own, a subtype of vision; the book or the chat, not both; a presentation is not a book; one fix per release; no EDN anywhere; the database is never a blocker, data migrated by interpretation; a watcher on Fable's transcript.
- 046782, 7b6597 (10-28), six: the main flow basket is split; belief modules for every aspect; the pulse never shorter than an hour; a blacklisted module removes the shell line; all vision modules cannot go in a main flow; everything is urgent; orders are beads, not logs.
- 63aef7, 2d9f4d, 5bbab2, b49eaf, d6bbd3, eight: tool removal is configured; a new Flow by the Fable Primary; a tool diffs the stock prompt per harness version; a flow has the publishing tool or is unaware of it; the code-block fault fixed in every book; the harness module is the section; reaching a Primary through its Secondary is a practice; a malformed book brings a proposal.

Four of these bear on this very design and were not in my prompt: a correction is not written down as its instance; orders are beads, not logs; implementers are not handed raw psyche logs; vision and intent read as vision, notion less. Under Proposal 2 a successor of mine would have had all four.

## What I ask

Whether marking is the word, or you want another. Whether the open records go to one Secondary to triage into beads, one per record, worked by me in your order, or whether you set the order yourself from this list.
