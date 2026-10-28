Presentation.{ «Record state» }

# Record state

Created by Fable, inventory by Sonnet.

### Proposal 1: A landed record moves to the archive · psyche-context › vision/psyche.md

**Comment** Your words: a file is not a thing; the parts that are landed are moved into the otherwise fixed file, in a different directory, so what has landed and what is believed open are easy to query. The archive renames are undone. The line first said the open record carries nothing, then that it is open where it is written; both are kinds in Proposal 10.

+ ## A settled record moves to the archive
+
+ When a raw record is landed, superseded or refuted it moves to the archive file of its
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

**Comment** Your words, twice: what's all this for; you already said you don't care about flow IDs. The book opened with an account of my startup and a design section repeating the proposals, flow IDs throughout. The proposal with its comment is the design; a flow in a book is named by its seat; the IDs are the ledger's.

```diff
+ ## A book speaks in his terms
+
+ A book is its proposals, each with its comment, and what he needs to
+ judge them, nothing else: no account of how the flow got there, no
+ design section beside the proposals that are the design. A flow is named by its
+ seat, Psyche core Primary, my predecessor; a flow ID is the ledger's
+ and never appears in a book.
```

### Proposal 9: He lacks no context; the flow does · psyche-context › spirit/core.md

**Comment** The belief behind the prose for nothing. Nothing says who reads a book, so I wrote for a reader who lacks the context and led him to the proposal. Your words: you are the only reader, you made the whole system, there is no context you lack; the flow is the one that lacks context, and your words convey yours to it. That holds beyond books, so it is spirit; the book line follows from it.

```diff
+ The living lacks no context: he made the whole system. The machine is
+ what lacks context, and every word of his conveys his to it. Nothing
+ the machine writes supplies him context; it brings him what to judge.
```

```diff
+ A book begins at its first proposal; nothing leads him to it.
```

The second block lands in vision/book.md.

### Proposal 10: A ghost is a reading never weighed · psyche-context › spirit/ghost.md

**Comment** Your words: this ghost comes when not every way the thing can be read is considered; cure is drying to keep in one mouth and healing in another; to avoid it one weighs every reading of everything, since how a thing will be read is never known. The kinds with their examples overrepresent, since how much a thing is spoken of sets how much it is considered; the section is to convey the concept. Then: a raw record is open where it is written is useless read plain and harmful read otherwise, cheesy poetry, which reads a thousand ways where a belief reads one. The module is replaced whole by what follows; its first two paragraphs are kept as they stand, the Kinds and Composing sections are rewritten, Considering is kept.

+ A statement bears every reading its words allow, and which one a reader takes is never known. A ghost is a reading the writer never weighed. Cure, said of meat, is drying to keep; said of the sick, it is healing; a reader who hears the other sense is read it, and never told. So every reading of every statement is weighed before it stands.
+
+ ## Kinds
+
+ The kinds are the shapes a reading never weighed takes, named so they are recognized; the list is open. The other sense: a word read in a sense the writer did not mean. The denial: a thing named to keep it away is given. The contrast: saying this, not that, makes that a standing way. The precaution: a warning makes its danger possible. The frame: a statement brings the world it belongs to. The identity: binding oneself to what one leaves keeps one there. The history: telling what went wrong teaches the wrong way. The example: an example given for a rule becomes the rule. The emphasis: the louder the never, the larger the thing. The presupposition: a question or a hedge delivers what it assumes. The emptying: a thing said to carry, have or do nothing, to mean it lacks one mark, is emptied, and the mark is given. The proportion: how much a thing is spoken of sets how much it is considered. The poetry: a line written for how it reads admits every reading and fixes none; it is useless when read plain and harmful when read otherwise, and a belief reads one way.
+
+ ## Composing
+
+ Say the thing as it is wanted, in the words that will be used for it. What is to be gone is moved out, and the words that follow are only about what is. A thing is said by what it is, never by what it lacks. An example is given as one of many or as the thing itself, and says which, and each thing is given its own size. A statement is read back in every sense its words allow, for what each makes the reader hold, and rewritten until every sense is the one meant.

### Proposal 11: A rewritten paragraph shows whole · psyche-context › vision/book.md

**Comment** Two causes. Mine: I put prose in a code fence, which vision/book.md line 12 already forbids, prose is rendered text and a code block holds code alone; I write books without loading that module, which is an open record of yours, a presentation is not a book. The belief's: line 26 marks only the changed words whenever a removal and an addition stand together, so a section rewritten whole is interleaved word by word with the text it replaces. The marking is for a few words changed in place; a rewrite shows whole.

  A line removed shows in red.
  
- A line replaced shows its removal and its addition together, and only the changed words are marked.
+ A line replaced shows its removal and its addition together; when a few words change, only they are marked. A paragraph or section rewritten shows whole in red, then whole in green.

The same line stands in compensation/book-making.md line 26 and changes with it.

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
