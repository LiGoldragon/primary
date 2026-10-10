# Message Primitive — a prototype for now

Fable b7ba00, Psyche, 2026-09-26, on the living's word relayed by Psyche Opus 93ba9f. Written independently of 93ba9f's prototype. The technical text stands alone; illustration markers name where a figure inserts. Every rule is a proposal until the living rules; the living's words are quoted where they bind (verbatim in `flows/b7ba00/vision/messaging.md` and `callerIdentity.md`).

> Meanwhile let's have just a very primitive version, a proof of concept, with just a few different types of messages, like what we've been doing so far. A better version of message should be redone and redeployed with just a string as the basic form.

## 1. What it is

A Message that a flow can use tomorrow: a handful of kinds, each a Markdown string, sent without naming oneself and often without naming the recipient. Three ideas carry it: the kind is the head; the origin is stamped by Message, never typed by the agent; the address may be a bearing — up, down, across — that Message resolves through Flow.

## 2. The kinds

The living's examples name the sender's aspect in the kind: a Field seat sends a field report, a Psyche seat a psyche question.

> We could type the message based on the type, because if you send the message you have the same type.

```
Markdown.String

Letter.[ FieldReport.Markdown     FieldQuestion.Markdown
         MindReport.Markdown      MindQuestion.Markdown
         PsycheReport.Markdown    PsycheQuestion.Markdown
         Order.Markdown           Answer.Markdown
         PsycheUpdate.{ Context Verbatim } ]
```

Eight string kinds and one for the living's words (context, then whole verbatim — the psyche envelope as it exists today). The head tells the reader what this is before a word is read; the aspect in the head says who speaks, in the reader's own vocabulary. Message refuses a kind whose aspect is not the caller's: a Field seat cannot send a `PsycheReport`.

**Fork 1.** Is the aspect in the kind the sender's (proposed, following the living's "if you send the message you have the same type") or the recipient's? Under the sender reading, `FieldQuestion` is a question from Field; where it goes is the bearing's business (§4).

**Fork 2.** `Order` and `Answer` carry no aspect: an order comes from above by construction and an answer answers a question already addressed. Keep them aspect-free (proposed), or `PsycheOrder`, `FieldAnswer`?

[ILLUSTRATION 1 — nine tiles, one per kind, each showing its head and its payload shape; the three aspects as three columns for the six aspect-bearing kinds, Order/Answer/PsycheUpdate in a fourth column.]

## 3. The origin — stamped, never typed

> It figures out the process that's calling and it can use that to talk to Flow to figure out which Flow used the CLI to send the signal that it just received. It can get its origin without the user having to say, "Hey I'm Psyche Fable." It would just know.

No request to Message carries a sender. Message learns it at the socket:

1. The Nexus accepts a connection on its Unix socket and reads the peer's credentials (the kernel gives the connecting process's pid and uid).
2. It asks Flow to resolve that pid: `ResolveCaller.Pid`. Flow walks the process's ancestry to the harness process it registered for a seat — the same binding Herdr holds for the pane — and answers `Caller.{ FlowId Seat }`, or `CallerUnknown`.
3. Message stamps the letter with that seat as its `Origin` and refuses the send if the caller is unknown. It never guesses.

This is the Signal standard the living names: every Nexus does step 1 the same way, and every Nexus that needs an origin asks Flow the same question. Flow itself uses it for `Refresh`: "who called it?" is the flow to refresh.

```
Origin.Seat                                  ; stamped by Message
Seat.[ Psyche.Layer  Mind.Layer  Field.Layer ]
Layer.[ Primary  Secondary  Tertiary  Quaternary ]

ResolveCaller.Pid  →  Caller.{ FlowId Seat }  |  CallerUnknown
```

**Fork 3.** When a subflow (a child process of a seat's harness) calls Message, the origin resolves to the seat that owns it — the flow is liable for its subflows. Proposed: yes; the ancestry walk stops at the first registered harness process.

[ILLUSTRATION 2 — a call's path: agent CLI → Unix socket → Message Nexus reads peer pid → asks Flow ResolveCaller → Flow answers the seat → the letter is stamped. A crossed-out speech bubble "I am Psyche Fable" beside the agent.]

## 4. The bearing — "send up"

> If you say "send up" it means message higher layer … The message logic has to figure out where that's supposed to go so it can ask the flow.

The address is a **bearing**: a direction from the origin, or an explicit seat.

```
Bearing.[ Up  Down  Across.Aspect  Living  To.Seat ]
Aspect.[ Psyche  Mind  Field ]
```

`Up` is the next higher layer in the origin's own aspect; `Down` the next lower; `Across.Psyche` the same layer in another aspect — the horizontal move the aspect skill already describes ("cross horizontally to that component at your level, then escalate vertically within it"); `Living` reaches the living's pane; `To.Seat` names a seat outright for the cases that need it.

Message resolves a bearing by asking Flow which live flow holds the resolved seat (`ResolvePeer.Seat`). If no live flow holds it, the letter is held and the sender told `NoSeat.Seat` — the living's earlier word on undeliverable letters (try higher, then lower) is the next version's rule, not this one's.

**Fork 4.** The word. "Bearing" is proposed because it is a direction relative to where one stands, which is exactly what `Up` is. Alternatives: `Heading`, `Course`. On the CLI the living's phrase is kept: `send-up`, `send-down`, `send-across psyche`.

[ILLUSTRATION 3 — the 3×4 grid of seats (three aspects across, four layers down); from a Field.Tertiary origin, three arrows: Up to Field.Secondary, Down to Field.Quaternary, Across.Psyche to Psyche.Tertiary; a fourth arrow out of the grid to the living.]

## 5. The request and the reply

One request, one reply, as every Nexus in this system does it:

```
Send.{ Bearing Letter }
  →  Sent.{ Origin Seat }                        ; origin stamped, recipient resolved and prompted
  |  SendRejected.[ CallerUnknown  KindNotCallers.Aspect  NoSeat.Seat  RecipientUnreachable.Seat  EmptyBody ]
```

Examples as a flow types them:

```
message 'Send.{ Up FieldReport.«Deployment 38 is orphaned in Copying; its self-switch replaced the Nexus.» }'
message 'Send.{ Across.Psyche FieldQuestion.«May I retire the 38 row?» }'
message 'Send.{ Down Order.«Regenerate the ouranos proposal against goldragon main.» }'
message 'Send.{ To.Psyche.Primary PsycheUpdate.{ «the living on the letter head» «Actually the head is where we put not only priority…» } }'
```

No sender, no message id, no priority. What lands on the recipient's pane:

```
FieldReport · Field.Primary · 2m
Deployment 38 is orphaned in Copying; its self-switch replaced the Nexus.
```

The origin, the age, and the words. Whether a kind interrupts the recipient is the database's judgment per kind, as the living ruled; the primitive version interrupts nothing and lets every letter wait for the recipient's turn.

**Fork 5.** Should `Sent` carry the resolved recipient seat (proposed, so the sender learns where "up" went) or only acknowledge?

## 6. History

No id. A flow asks its own history by bearing and count, and Message answers with letters as stamped:

```
History.[ Last.Integer  From.Seat  Since.Age ]   →  Letters.Vector<Stamped>
Stamped.{ Origin Seat Moment Letter }
Age.[ Seconds.Integer Minutes.Integer Hours.Integer Days.Integer ]
```

## 7. The database's name

The database now called Sema keeps sema among other things, so it gives the name to the language. Proposed: **Mnema** — Greek for memory and for a record — one word, unused, and it says what the thing does: it remembers what was said. Alternatives: Thesauros (a store), Archeion (an archive).

## 8. What is deliberately absent

Priority and tiers (ruled out of the letter). Message ids and acknowledgements by id. A named sender. Sema beyond the Markdown payload — the kinds above are the first eight sema kinds in disguise, and version one of Sema replaces `Markdown` in place when it lands. Escalation of undeliverable letters. Any letter body that is not a string or the psyche pair.

## 9. Who builds it

The living: Astra designs and orchestrates and takes the big decisions; Sol implements and tests. This prototype and 93ba9f's go to Mind Astra together; Astra reconciles them into the Ethos of `signal-message` and `meta-signal-flow` (where `ResolveCaller` and `ResolvePeer` already stand on the Flow branches), and Sol lands and tests it with a disposable seat, not against the living or a working Field.

## 10. What this book asks the living to rule

1. The aspect in the kind is the sender's (Fork 1), and Order/Answer stay aspect-free (Fork 2).
2. Origin stamped at the socket through Flow's `ResolveCaller`, subflows resolving to their seat (Fork 3), unknown callers refused.
3. The word "bearing" for the address, with Up, Down, Across, Living, To (Fork 4).
4. `Sent` returns the resolved recipient (Fork 5).
5. Mnema for the database.

Sources: `flows/b7ba00/vision/messaging.md`, `callerIdentity.md`, `mindRoles.md`, `sema-version-one.md` and the letter-book addendum in `anatomy-of-the-meaning-language.md`; the flow-aspect skill on horizontal and vertical routing; the messaging and compensation-messenger-clj skills for today's transport.