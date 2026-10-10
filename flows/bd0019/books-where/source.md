`Book.«Where books go, and the anatomy of the book pipeline»`

## 1. Where books go today
- **Publishing.** Each book is published as a private page. Which book sits at which link is recorded only in the page tool, not in any log.
- **Version control.** The Markdown of earlier books is committed, but only when other flows' catch-up commits happened to sweep it in. The newest book isn't committed at all, because four screenshots of up to 7 MB stop jj from saving the directory.
- **Proposal.** Psyche Sonnet commits each book's Markdown itself, under its flow's books folder, named by the turn that produced it. The HTML is published as a page and not committed, and screenshots are not kept.

## 2. The anatomy
```
flow ends its turn ─Stop hook─▶ flow CLI ─signal─▶ Flow Nexus ─TurnEnded─▶ Sonnet (subscribed)
                                                                              │
                     Transcript Nexus ◀─ReadLivingBlock─ transcript CLI ◀─────┘
                                                                              │
                                                         Markdown → commit;  HTML → page
```
- **The hook** calls the CLI only when the start marker is in the last message, and decides nothing else.
- **Flow** records that the turn ended and tells its subscribers, but never carries the content.
- **The Transcript Nexus** returns the block by pointer, with its title already typed. It is only designed, not built.
- **Sonnet** waits for the next ended turn rather than checking repeatedly, then makes the book.

The other route is still **open**: the hook calls Transcript directly and Flow stays as it is.

## 3. Ethos and datom (proposal; Mind Sol's type replaces mine if it comes first)
The block's title line:
```
Library
[]
[ BookTitle.String
  Presentation.[ Book.BookTitle ] ]
[]
[]
```
The Transcript Nexus:
```
Signal
[ signal-flow:TurnPointer  presentation:Presentation ]
[ ReadLivingBlock.TurnPointer ]
[ LivingBlockRead.LivingBlock  LivingBlockRejected.LivingBlockRejection ]
[ BlockText.String
  LivingBlock.{ Presentation BlockText }
  LivingBlockRejection.[ UnknownTurn NoBlock UnclosedBlock MalformedPresentation.BlockText ] ]
```
**Flow gains** `EndTurn.TurnPointer` and `ObserveTurns.TurnFilter`, with the replies `TurnEnded.EndedTurn` and `TurnsObserved.TurnFilter`, and these types:
```
TurnPointer.{ SessionId TurnId }
EndedTurn.{ FlowId TurnPointer }
TurnFilter.[ AllFlows Flow.FlowId ]
TurnEndRejection.[ UnknownCaller SessionMismatch TurnAlreadyEnded ]
```
Adding variants to its closed contract is a breaking change, so Flow moves to its next major version. The verb can't be `Present`, because `Presented` is already one of Flow's delivery grades.

Datom examples:
```
Book.«Anatomy of the book pipeline»              ; the first line inside the block
flow 'EndTurn.{ 0b7c1e 3f9a2d }'                 ; the hook's call: session, turn
TurnEnded.{ fe945a { 0b7c1e 3f9a2d } }           ; the reply, and what each subscriber receives
transcript 'ReadLivingBlock.{ 0b7c1e 3f9a2d }'   ; Sonnet reads the block by pointer
LivingBlockRejected.UnclosedBlock                ; nothing is published; the writer gets this one line
```

## 4. A preview of the user documentation
> **Books.** When a flow has something for you, it puts it between the two marker lines, and the first line inside is the book's title. When the turn ends, a hook reports it. Psyche Sonnet hears it and reads the block without copying the transcript. You get a private page, and its Markdown is committed. If a block is unclosed or its title doesn't parse, nothing is published and the flow that wrote it is told in one line. There is nothing to configure.

**Your word.** Shall Psyche Sonnet make this into a book?