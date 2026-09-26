# A Primitive Message

Prototype design by Psyche Opus 93ba9f, 2026-09-26. Written without reading Fable's prototype; both go to the Mind, where Astra designs and orchestrates and Sol implements and tests.

## The living's words

> Meanwhile let's have just a very primitive version, a proof of concept, with just a few different types of messages, like what we've been doing so far. A better version of message should be redone and redeployed with just a string as the basic form.

> If you say "send up" it means message higher layer … The message logic has to figure out where that's supposed to go … the message will go to the right place as long as we know where it comes from.

> It figures out the process that's calling and it can use that to talk to Flow to figure out which Flow used the CLI to send the signal that it just received. It can get its origin without the user having to say, "Hey I'm Psyche Fable." It would just know.

## 1. What an agent types

One inline datom, nothing else. No sender, no flow ID, no priority.

```
message 'Up.Report.«Four old flows archived; e167d8 closed.»'
message 'Up.Question.«May I restart the Next pair now?»'
message 'Across.Mind.Question.«Is field-clj safe to redeploy?»'
message 'Down.Order.«Reap the flows abandoned since noon.»'
message 'Seat.Field.Secondary.Answer.«Yes, restart it.»'
```

The reply is one word and the seat it reached:

```
Delivered.Psyche.Secondary
Parked.Psyche.Secondary
Refused.NoSeatAbove
```

## 2. What the recipient sees

```
Report.{ Field.Tertiary «Four old flows archived; e167d8 closed.» }
Question.{ Field.Tertiary «May I restart the Next pair now?» }
```

The kind first, then the sender's seat, then the text. The pane shows no ID, no timestamp, no priority.

## 3. The anatomy

```
Aspect.[ Psyche Mind Field ]
Layer.[ Primary Secondary Tertiary Quaternary ]
Seat.[ Psyche.Layer Mind.Layer Field.Layer ]
Markdown.String

Kind.[ Report.Markdown Question.Markdown Answer.Markdown Order.Markdown PsycheUpdate.Psyche ]
Psyche.{ Markdown Markdown }

Toward.[ Up Down Across.Aspect Seat.Seat ]
Send.{ Toward Kind }

Letter.[ Report.{ Seat Markdown } Question.{ Seat Markdown } Answer.{ Seat Markdown }
         Order.{ Seat Markdown } PsycheUpdate.{ Seat Psyche } ]

Sent.[ Delivered.Seat Parked.Seat Refused.Refusal ]
Refusal.[ NoSeatAbove NoSeatBelow SeatEmpty CallerUnknown ]
```

- **`Toward`** is the "send up" word. `Up` is the next layer above in the sender's own aspect; `Down` the next below; `Across.Mind` the same layer in another aspect; `Seat.…` names one seat outright.
- **The kind is the same type on both ends.** What the sender sends as `Report` arrives as `Report`.
- **"Field report", "psyche report"** fall out without separate types: a `Report` from a Field seat is a field report, because the sender's seat is in the letter.
- **The payload is Markdown in guillemets:** the part of Sema still undeveloped.

## 4. Who called — a Signal standard

Built already, inside Flow only: a Nexus reads the calling process from its own socket (`SO_PEERCRED`), finds the pane that process runs in, and names the flow bound to that pane. Message asks Flow for it on every send.

The proposal: lift that out of Flow into the shared Signal library as a standard every Nexus uses.

```
Origin.{ FlowId Seat Model }
```

- Every Nexus receives the caller's `Origin` beside every request, resolved by Flow, never written by the caller.
- A process in no flow's pane is the owner's own shell; it gets `Origin` refused, or the meta socket.
- Flow uses it on itself: `Refresh` with no argument refreshes the flow that called.

Today's `Caller` carries the old power words (`High Medium Low UltraLow`); it moves to `Seat`, aspect and layer.

## 5. Where "up" goes

Flow holds the roster of seats and which live flow sits on each. Message asks Flow once per send:

```
ResolveToward.{ Seat Toward }  →  Resolved.{ FlowId Seat }  |  Refused.Refusal
```

- `Up` from `Field.Tertiary` is `Field.Secondary`; if that seat is empty, the next above; if none is above, the next below (the living, 24 September).
- A crucial empty seat (every medium and high one) is started rather than skipped (same record).
- How hard a kind breaks in is Message's per-kind table, held in its database, never on the pane:

```
{ PsycheUpdate MiddleAbrupt }
{ Order MiddleAbrupt }
{ Question Soft }
{ Report Soft }
{ Answer Soft }
```

## 6. The database's new name

The meaning language takes the name Sema. The storage every Nexus uses (`sema-engine`, `.sema` files, fifteen consumers) takes a new one. Candidates:

- **Thesauros** — Greek: storehouse, treasury; where Sema is kept.
- **Kosha** — Sanskrit: sheath, treasury, repository.
- **Mnema** — Greek: memory, record (Fable's proposal).

The Ethos root named Sema is one file in one repository, a narrow rename; the storage library is the wide one.

## 7. Building it

1. Signal: the `Origin` standard, lifted from Flow's resolver.
2. Flow: `Seat` in place of the old power words; the roster; `ResolveToward`.
3. Message: `Send.{ Toward Kind }`, the letter by kind, the per-kind interruption table, the one-word reply.
4. Deploy on the Next pair; messenger-clj retires when the Next pair becomes stable.

## Questions

1. Is `Toward` with `Up`, `Down`, `Across` and `Seat` the "send up" you meant?
2. Five kinds to start — Report, Question, Answer, Order, PsycheUpdate — with "field report" read from the sender's seat?
3. Is the database Thesauros, Kosha, Mnema, or another?
4. Does `Origin` become the Signal standard every Nexus uses?
