Presentation.{ «Record state» }

# Record state

Created by Fable, inventory by Sonnet.

## What failed at my startup

A raw record is written once and nothing ever says what became of it. My launch gave me 7459f3's model-roles and proposal records, both landed and pushed hours earlier, because remembering picks by flow and depth, not by state. It gave me none of the 73 records across twelve flows that no module line answers yet, because they sit in other flows' files. 7459f3 patched this by hand: it renamed landed files to `archive-*.md` and put "Landed in …" on top of some. Twenty-five records are archive-named with no note; the rename moved them and said nothing.

## The design

Mark, do not move. A record keeps its file, its heading and its provenance, and carries one state line under its heading. The lander writes it when the line lands, in the commit that lands it; the flow that hears a later word overruling it writes Superseded; the flow that hears the thing is not wanted writes Refuted. Remembering then selects by state: a fresh flow receives every Open record of its address, whoever wrote it, and a one-line index of the settled ones, so none is re-raised and none is missed. Depth stays only for the transcript.

The Ethos:

```ethos
Library
[]                                               ; imports
[ ModulePath.String                              ; types
  Commit.String
  FlowId.String
  Heading.String
  RecordState.[ Open                             ;   written with the record
                Landed.{ ModulePath Commit }     ;   the lander writes it, same commit
                Superseded.{ FlowId Heading }    ;   a later word of his overruled it
                Refuted.String ]                 ;   he said the thing is not wanted, and why
  Remembering.[ Open                             ;   every Open record of the address
                Predecessors.Integer
                Custom.Vector<FlowId> ] ]
[]                                               ; traits
[]                                               ; associations
```

The datom, as it sits in a record today:

```datom
## 2026-10-28 — A proposal is signed with the models that made it
State: Landed.{ vision/proposal.md 5d81baa }
```

### Proposal 1: A record carries its state · psyche-context › vision/psyche.md

**Comment** Your words: some way for the things that have been landed, changed or refuted not to be passed over. The archive renames are undone and every record marked.

+ ## A raw record carries its state
+
+ A raw record is never moved. Under its heading it carries one state:
+ Open when written; Landed, with the module and the commit, written by
+ the lander in the commit that lands it; Superseded, with the record
+ that overruled it; Refuted, with his reason. A file is never renamed
+ to say what became of its records.

### Proposal 2: Remembering selects by state · psyche-context › vision/remembering.md

**Comment** Your words: you were given things already settled and not the things that were not settled. The launch gains an Open remembering; depth remains for the transcript.

+ ## A fresh flow receives what is open
+
+ A remembering of Open gives a fresh flow every Open record of its
+ address, from every flow that wrote one, and a one-line index of the
+ settled ones: heading and state. Depth and named flows remain for
+ reaching a transcript.

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
