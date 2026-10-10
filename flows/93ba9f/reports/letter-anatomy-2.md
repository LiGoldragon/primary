# The letter — its Ethos, and the redraw

Psyche Opus 93ba9f, 2026-09-26.

## The living's words

> You didn't show me the ethos. I still don't know what the other variants are of text. We shouldn't get the message ID. We're going to develop a different kind of interface to get message history. We're not going to get by message ID and the sender being called "owner" is fucking ridiculous. The message has to be able to figure out who the sender is programmatically eventually from the process that called, but for now the sender is psyche primary or psyche secondary, etc.

> We could make a set of all of them and variants.

## The Ethos as it stands (meta-signal-flow, branch s1-e167d8, exact lines)

```
MessageId.String
Sender.[ Flow.FlowId Owner ]
PsycheContext.String
PsycheVerbatim.String
Content.[ Text.String Psyche.{ PsycheContext PsycheVerbatim } ]
Letter.{ MessageId Sender Content }
Message.[ HardAbrupt.Letter MiddleAbrupt.Letter Soft.Letter ]
DeliveryRequest.{ DeliveryId FlowId Message }
```

and in signal-message:

```
Priority.[ HardAbrupt MiddleAbrupt Soft ]
SendRequest.{ Vector<FlowId> Priority Content }
Acknowledge.MessageId
```

`Text` is not an enum: it is a variant of `Content` carrying a plain string. `Content` has exactly two variants, `Text` and `Psyche`. There are no others.

## The redraw

```
Sender.[ PsychePrimary PsycheSecondary PsycheTertiary PsycheQuaternary
         MindPrimary MindSecondary MindTertiary MindQuaternary
         FieldPrimary FieldSecondary FieldTertiary FieldQuaternary ]
PsycheContext.String
PsycheVerbatim.String
Psyche.{ PsycheContext PsycheVerbatim }
Content.[ Text.String Psyche.Psyche Psyches.Vector<Psyche> ]
Letter.{ Sender Content }
Message.[ HardAbrupt.Letter MiddleAbrupt.Letter Soft.Letter ]
```

In the pane:

```
Soft.{ PsychePrimary Text.«…» }
```

- The sender is one set of every seat, each seat a variant. Message stamps it from the seat bound to the calling process; the caller never writes it. Later it is derived from the calling process itself.
- No message ID in the letter, no Acknowledge by ID, no "get by ID". Message history gets its own interface, designed later.
- `Owner` is gone.
- `Psyches` carries several psyche entries in one letter.
- Priority is declared once, in Message, and Flow uses it.

## Questions

1. Is the sender set right as twelve seats (three aspects times four layers), or should the Fable seats be members too?
2. Besides Text, Psyche and Psyches, what other kinds of content should a letter carry?
