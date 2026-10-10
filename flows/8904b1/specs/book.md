# Book: a flow's page for the living

Specification by Psyche Fable 8904b1, 2026-09-28, from the living's words in
records 8904b1-27, 30, 32 to 36. Claude only for now: it is the one harness
whose pages the living can comment on.

## What it is for

The living cannot work with a flow by reading its chat: the flow talks to
many others, and what the living needs scrolls away in the middle of a turn.
The flow calls a sub-agent with one line; the sub-agent makes, from the
flow's whole transcript, a page the living works with instead of the chat.

## The page

The present state of everything in the flow, by subject, never by time.

- Made from the whole transcript: what the living said, everything the flow
  said (mid-turn as well as last), what workers returned, what other flows
  sent, what was done.
- Where two things contradict, the most recent wins, whoever said it. What
  is overtaken leaves the page.
- What waits on the living's word is on top.
- The living's own words are not on the page. The living knows what was
  said; the flow's record keeps every word. What the page carries of the
  living is proposed distillations.
- Scrolls down in one column; nothing folded away or swiped.

## Proposed distillations

Each ruling of the living that should outlast the conversation appears as a
proposed distillation with a proposed destination.

    Type
    Distillation.{ Statement Destination Vector<Source> State }
    [ Statement.Markdown  Markdown.String
      Destination.[ Vision.Topic  Intent.Topic  Skill.{ Kind Name } ]
      Kind.[ Operation Documentation Compensation Trial ]
      Topic.String  Name.String
      Source.{ FlowId Topic }  FlowId.String
      State.[ Proposed Approved Changed.Markdown Refused ] ]

- Approved with a Vision or Intent destination: it becomes vision or intent.
- Approved as a good skill of its kind: it goes into that skill.
- Changed: the living's note is the correction; proposed again.
- A distillation cuts what is unnecessary and makes the statement stand by
  itself. The sources point to the raw records, which keep the words.

## Subjects

    Type
    Subject.{ Name State Vector<Waiting> Changed }
    [ Name.String  State.Markdown  Changed.Time  Time.String
      Waiting.{ Question Proposal Vector<Option> Lost Answer }
      Question.Markdown  Proposal.Markdown  Lost.Markdown
      Option.String  Answer.[ None Chosen.{ Option Note } ]  Note.Markdown ]

## Parts

| Part | Power | Work |
|---|---|---|
| Fetch | none, a program | Finds the caller's transcript by the session number in its shell; hands over what is new since the mark; drops only raw machine output |
| Readers | Medium, several at once | Each reads one stretch; returns subjects, their latest state, the living's rulings |
| Judge | High | Merges into the state the page holds; newest wins; orders; proposes distillations and destinations; writes the page's rows in one batch |

First making reads the whole transcript. Afterwards only the new stretch.
The judge returns to the calling flow, in a few lines, what the living
answered on the page since last time.

## The call

`Update the page.` Nothing else. The instructions are in the sub-agent's own
definition, not in a skill it must find.

## Sub-agent definitions

Each aspect holds its sub-agents beside its skills; the generator writes
them for each harness.

    Type
    Subagent.{ Name Aspect Purpose Power Vector<Skill> Vector<Tool> Instructions }
    [ Name.String  Aspect.[ Psyche Mind Field ]  Purpose.String
      Power.[ High Medium Low ]  Skill.String  Tool.String
      Instructions.Markdown  Markdown.String ]

Effort is always medium. Power names a model through the one table that
already exists. The generator today writes name, description, model and
effort only; it must also write instructions, skills and tools.

## Later

The same instructions, started by the harness event at the end of a turn
(a program hook, in the background, its model started without hooks so it
does not trigger itself). Later still the event goes to a nexus that holds
the budget and decides what runs.
