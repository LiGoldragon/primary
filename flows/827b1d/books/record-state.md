Presentation.{ «Record state» }

# Record state

Created by Fable, inventory by Sonnet.

## The fault

A raw record is written once and nothing says what became of it, so a fresh flow is handed records already landed and misses open ones that sit in other files. My launch did both.

## The design

The record is the thing; a file is only how a flow is handed context. A record that lands moves out of its open file into the archive file of the same topic, in a separate directory, and carries there one line saying what became of it: Landed, with the module and the commit, written by the lander in the commit that lands it; Superseded, by the record that overruled it; Refuted, with your reason. An open record carries nothing, and the open file is what a fresh flow reads whole. Location answers open or settled by one query; the line answers what became of it. In the long term the records live in the psyche nexus and the state is a field of the record.

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

### Proposal 6: A fault in a thing is a fault in a belief · psyche-context › intent/main-flow.md

**Comment** The belief that did not fire. intent:main-flow already says that when you point out a fault the reply gives its cause and the line that changes the behavior, behavior first, repair second. I held that line and repaired the book first, because I read your words as a fault in the book, not in me, and nothing said those are the same thing. The line that was missing is the one that binds them.

```diff
  When the living points out a fault, the reply gives its cause and the line that changes the behavior that produced it; the behavior change comes first, the repair of the artifact second.
+ A fault he points out in a thing a flow made is a fault in the belief that made it, however he phrases it; the reply gives that belief's line before the thing is repaired.
```

### Proposal 7: The cause and the line go into the book · psyche-context › intent/living-interaction.md

**Comment** The fix was in: the chat line landed and was in my prompt. It falls short because the main-flow line says the reply gives the cause and the belief line, and nothing says where; I gave them in the chat and in the book both. The line names the place.

```diff
  A chat answer is a few sentences. What is long and for the living goes into a presentation; what is long and not for him is said nowhere.
+ When he points out a fault, its cause and its belief line go into the book; the chat says in one sentence which belief failed, and gives the link.
```

### Proposal 8: A book speaks in your terms · psyche-context › vision/book.md

**Comment** Your words: what's all this for; you already said you don't care about flow IDs. The book opened with an account of my startup in machine terms, flow IDs throughout, and listed the open records by flow. A flow in a book is named by its seat; the IDs are the ledger's.

```diff
+ ## A book speaks in his terms
+
+ A book carries the proposals and what he needs to judge them, nothing
+ else: no account of how the flow got there. A flow is named by its
+ seat, Psyche core Primary, my predecessor; a flow ID is the ledger's
+ and never appears in a book.
```

## What is open now

Sonnet matched every record since 2026-10-26 against psyche-context by distinctive phrase; the modules paraphrase, so open means no line found, not proof of none. Of 136 records: 73 open, 34 landed, 29 only archive-named. The open ones, by topic:

- Belief editing: always approved; a correction is not written as its instance; teaching needs examples; an audit for unapproved edits.
- Belief modules: the main-flow basket is split; modules for every aspect; all vision modules cannot go in a main flow; the eventual design is a module of its own, a subtype of vision; a blacklisted module removes the shell line; file modules become skills holding questions.
- Flow: hourly pulse, never shorter; a flow wakes itself under an hour; reminders are a Flow feature; a meta operation to order a restart; the rebuilt Flow implemented, tested, then used, old flows refreshed; one fix per release; roles are data queries; tool removal is configured; a tool diffs the stock prompt per harness version; a new Flow by the Fable Primary; raw-run Flow 0.40; a refresh tool; a watcher on Fable's transcript.
- Messaging: Flow delivers regardless; signal out of the Nexus is proper datom; a proof-of-concept message nexus; reaching a Primary through its Secondary is a practice; who may message whom is configuration; restrictions come from layering, left out for now.
- Books and the chat: the design is the book; reports are books; inferring vision is writing the book; the book or the chat, not both; a presentation is not a book; chat or book: silence and size; the code-block fault fixed in every book; a malformed book brings a proposal.
- Records and logging: orders are beads, not logs; flows still log everything; psyche records stay; dated addenda on the design report are the logging meant; implementers are not handed raw psyche logs; what is important: vision and intent read as vision, notion less.
- Memory: never a blocker; data migrated by interpretation; no EDN anywhere.
- Models and usage: Codex ramped up, resets used; an idle Mind wastes Codex; the overnight rebuild.
- Ethos: everything becomes proto syntax, an Ethos Notebook; every flow has Ethos and Datom training; the harness module is the section.
- Committing: one refusing committer is ridiculous.
- Psyche aspect: a fresh flow hunts horrible things hourly while you are away; "all your aspects"; implications extracted by layered flows; a tool checks the vision's code is in the implementation.
- CriomOS: dark theme at five; battery lost asleep; screen never locks.

Four of these bear on this design and were not in my prompt: a correction is not written down as its instance; orders are beads, not logs; implementers are not handed raw psyche logs; vision and intent read as vision, notion less. Under Proposal 2 a successor of mine would have had all four.

## What I ask

Whether marking is the word, or you want another. Whether the open records go to one Secondary to triage into beads, one per record, worked by me in your order, or whether you set the order yourself from this list.
