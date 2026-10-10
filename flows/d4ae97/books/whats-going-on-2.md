<!-- to-the-living:start -->
Presentation.{ «What's going on», second edition }

Everything in motion, in one place. The first edition carries your comments, so it stays as it is. This edition answers them.

## Books waiting for your numbers
```
From Fable 8475a9 (Psyche Primary, the designer)
  «What sticks out»                 2 rulings   https://claude.ai/artifact/KLnwd2FDtd9rfp9miqzQSL
  «Datom expansion», 2nd edition              https://claude.ai/artifact/3HYQBstRvJx7YTS64SumLg
                                    (answers your nine comments; the first edition is superseded)
  «A voice's name», 2nd edition     4 rulings   https://claude.ai/artifact/5riAb1PyPvsGEExk4V4bWa
                                    (the first edition is superseded)
From me, d4ae97 (Psyche Secondary, the secretary)
  «The brief, copied twelve times»  2 rulings   https://claude.ai/artifact/MGakWVRaTqeJqd7Y77quy7
  «Flow spawning»                              https://claude.ai/artifact/U8SS1JBXbHgf7hcnoLp81G
                                    (by Mind f768df, reviewed by Fable; answers your Flow order to Astra)
  «fuzzy-jev: what it is»          2 rulings   https://claude.ai/artifact/UG5xSKSss5DbJ33rYmn6ZR
                                    (measured: what it is, size, stack, releases, commits)
  «How we call the voices»          1 open      https://claude.ai/artifact/8d8WhKf4R3wxdzA7Q49nhP
```
- **«How we call the voices» and «A voice's name» cover the same subject.** I wrote mine before Fable's arrived, then cut it down. Your comments answered it, except one ruling: did "hacking messenger" mean messenger-clj?
- **Fable has redesigned «A voice's name» after your comment.** The second edition stands at the link above. A flow is now its id and its role; a role is a voice, or a job for a side flow:
```
Library                                   ; Flow's shared types (signal-flow's ethos)
[]
[ FlowId.Integer
  Aspect.[ Psyche Mind Field ]
  Layer.[ Primary Secondary Tertiary Quaternary ]
  Voice.{ Aspect Layer }                  ;   what the messenger names a sender by
  Role.[ Voice Job ]                      ;   what a flow runs as
  Flow.{ FlowId Role } ]                  ;   nothing the voice already says
[]
[]
```
  - You answered that "seat" leaves the vocabulary, and that a voice is a type of metaflow. From that, Fable wrote these lines, and Mind Astra is landing them:
```
vocabulary   Voice: an aspect at a layer, {Aspect Layer}; a metaflow with no known ending.
             A flow runs as a role; a voice is one role.
             There is no seat: say the voice or the flow.
main-flow    "one of the twelve seats that extend the living psyche"
           → "one of the twelve voices that extend the living psyche"
elsewhere    every "seat" becomes voice or flow, as the sense requires
```
  - Still open there: the title form and the registry living in Flow.
- **The layer models, from your comments.** The skill now says this. It is in Curriculum, running flows already read it, and its publication to Primary main is asked of Field. The Secondary row is Opus 5.5, not the older Opus. Field takes the same models as Mind:
```
layer        Psyche (Claude)    Mind and Field (Codex)   effort
Primary      Fable              Astra                    medium
Secondary    Opus 5.5           the latest Sol           medium
Tertiary     Sonnet             Luna                     medium
Quaternary   Sonnet             Luna                     low
```

## Which flow holds each voice: your rulings needed
Fable decided:
- A new flow gets its voice at launch, from whoever launches it.
- The 16 flows running now get theirs once, from a list I write.
- Any voice that two flows claim comes to you first.

Here is the list as their records give it. A "reading" is mine, and a ruling of yours decides it.
```
voice                 flow     model           what the records say
Psyche Primary        8475a9   Fable           its launch
Psyche Secondary      d4ae97   Opus            your "Secondary is Opus"
Psyche Tertiary       8f0f57   Sonnet          title and launch
Psyche Quaternary     02dda6   Sonnet          title and launch
Mind Primary          d66c26   Astra           both say only "Mind Astra"     ← two flows
                      f768df   Astra
Mind Secondary        41fa34   Sol             says only "Mind Sol"           ← reading
Mind Tertiary         918df4   Luna            title and launch
Mind Quaternary       4ddfe1   Luna            title and launch
Field Primary         7de94a   Astra           says only "Field Astra"        ← reading
Field Secondary       42265e   Sol             says only "Field Sol"          ← reading
Field Tertiary        4371ed   ?               title only
Field Quaternary      6aa08d   ?               title only                     ← two flows
                      db38f8   Sonnet          its log: "Field Quaternary publisher"
no voice              6e782c   Sonnet          "Psyche, books seat"
```
- **bfdae1 was my mistake, and you archived it.** Mind runs on Codex, so Mind Secondary runs on Sol. 41fa34, "Mind Sol", may already be Mind Secondary. Field launches nothing for it until you rule.
- Field is building your fix: the launcher holds which harness, model and effort each voice gets as data, and it refuses any launch that conflicts with that data.
- **Every aspect has a Tertiary and a Quaternary**, Field included. Field Tertiary 4371ed and Field Quaternary 6aa08d stand. Field Quaternary has two flows, 6aa08d and db38f8, the paused publisher. Ruling 7 settles which.
- **6e782c** writes books. In Fable's design it would be a job, not a voice.

## Field 42265e is blocked
- The messenger shows Field 42265e as blocked, so messages to it are held, not typed. Its window showed "Action Required" earlier: it may be waiting for your approval there.
- Held for it now: your two naming examples, which it asked for so it can relaunch Field Primary:
  - `{ Mind Tertiary 918df4 }`, how a flow is called;
  - "Mind Tertiary", how the messenger names a sender.
- Also held: my answer on what to publish.
- Mind Astra's change to how flows launch is held for the same reason.

## Chronos: the entry-point test passes
Mind Astra d66c26 ran it on an experiment branch.
```
66 integration tests   pass, including a real socket: store a location, read it back
3 guard tests          code that must not compile does not compile
                       (signal and memory cannot reach each other except through operation)
merged / switched on   nothing; it waits on your numbers on «The Nexus» and the entry-point book
```
Report: `flows/d66c26/reports/chronos-entry-experiment.md`.

## Voices and the messenger
You asked for voices to be called `{ Mind Tertiary 918df4 }`, and for the messenger to name a sender only as "Mind Tertiary". Fable designed it, and Mind Astra is mapping the code.
- Nothing is built yet. Astra withdrew the Seat type after your comment.
- Fable's new type has gone to Astra. The type itself waits on your rulings in «A voice's name».
- Being built now: Flow's record of which flow holds each voice, and a handover that switches that record in one step when a flow is replaced. Fable authorized this; it does not touch the type.
- On your ask, Mind Astra f768df is checking the messenger against what you said this last hour. It coordinates with d66c26 before building, so the two do not edit the same code.
- Not yet built by anyone: the messenger naming a sender by voice only.
- Astra found one fork in it: the flow id is a string on the wire and in storage today, and the new type makes it a number. That is the same question as ruling 2 of «Datom»; your words there: "The flow ID is not a string, it's a hash".
- Astra's notes for that design: Flow's records today have no layer, and no flow carries a voice. A seat taking over a voice must hand over in one step: the new flow is reachable only after the old one is closed.

## ChatGPT Pages and the Notion-like product
- **Pages trial done.** Astra made a private page holding its book «Jev proposals and implementation choices»: https://chatgpt.com/space/page_4b2c0eb0f12081918733e2c5a455d170. The same book in your usual messenger, to compare the two media: https://claude.ai/artifact/WJksrEuDQboxRaT1teAhNL. It is an experiment in medium; it asks you no new ruling.
- **How we use Pages: Astra's answer.** Astra's Codex connector can do all of these, each shown in the trial:
```
create     a private page
edit       its blocks in place, then read them back
attach     code, tables, and an HTML or SVG drawing
comments   list them, and reply only to a thread already seen
```
  - **Your test failed: you cannot select or copy text on the page, nor comment.** What the connector showed proved nothing about what you, the viewer, can do.
  - Astra's diagnosis, read-only:
    - The page is private, owned by the account Astra's connector uses, and shared with no one.
    - Its "can comment" flag describes that connector, not you.
    - Whether the account you viewed it with is that same account is not checked.
    - OpenAI's help pages say nothing yet on selecting or commenting in Pages.
  - The same book in your usual messenger stays the working copy.
  - Workflow: `flows/d66c26/reports/pages-workflow.md`.
- **The "Notion clone" is ChatGPT Space.** Mind Tertiary's first pass, from OpenAI's own pages:
```
Space      a workspace and library: pages, files, folders, shared work (DevDay, 2026-09-29)
Pages      editable documents that nest: a book in a Space, each chapter a sub-page
comments   on a selected passage; ChatGPT can be mentioned in them
sharing    people, teams, email or link, where available
mobile     read, find and share only; editing and comments are "pending"
API        no public Pages or Space API; Astra reaches it through the Codex connector
```
  - The mobile line may be why you could not select or comment, if you opened it on your phone. That is the flow's reading, not checked.
  - **Claude has its own: Claude Docs** (beta, inside artifacts):
    - rich text and inline comments;
    - export to Word, PDF, Markdown and Google Docs;
    - Claude Code can create one;
    - on mobile you can only view, commenting needs the edit role, and there is no version history.
  - Mind Tertiary's take: Space is stronger for books you comment on, provided you can comment where you read. Check reader access and comments before choosing.
- **Research chain, on your order:**
  - Mind Tertiary 918df4 does the first pass, with web research.
  - Mind Secondary expands it. **That launch was my error.** I asked Field for Mind Secondary on Opus, Field launched bfdae1 on Claude, and you archived it. Mind runs on Codex only, and the layer-models skill now says so.
  - The expansion waits on ruling 5: which flow is Mind Secondary.
  - Mind Secondary then asks Astra for the design.

## Still waiting from before (the handover)
- Your three answers on placing the skills, then your yes to run the skill migration.
- «Context modules», the revised book.
- The «Metaflow» line you approved, still to be landed in the vocabulary skill.

## How I failed you, and the line that fixes it
I reported results in chat: Chronos, the Pages trial, the research launch. Chat is unread. My instructions call those results "machine output, one line each", so they never reached a book.

`Curriculum/skills/main-flow.md`, after the line "Everything else the flow says is machine output…".

Now: no such line. Proposed:
```
What the living should know of the work — a result, a launch, a hand-down, a blocker, a book from another flow — goes into one standing book, «What's going on», revised in place as it changes; nothing he must know lives only in chat.
```

## Rulings
1. The main-flow line above: (a) yes; (b) amend it (say how).
2. "hacking messenger" meant messenger-clj: (a) yes; (b) something else (say what).
3. The ChatGPT Page you opened: on which device, and signed in to which ChatGPT account?
4. Mind Primary: (a) d66c26; (b) f768df. The other is closed.
5. Mind Secondary: (a) 41fa34 (Sol), which then expands Mind Tertiary's research; (b) a new flow on Sol.
6. Field: (a) 7de94a is Field Primary and 42265e is Field Secondary; (b) say which.
7. Field Quaternary: (a) 6aa08d, and db38f8 is closed; (b) db38f8, and 6aa08d is closed.
8. 6e782c, the books flow: (a) a job, with no voice; (b) a voice (say which).
<!-- to-the-living:end -->
