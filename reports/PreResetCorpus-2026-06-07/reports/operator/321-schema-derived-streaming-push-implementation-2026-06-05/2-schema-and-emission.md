# Schema And Emission

## schema-next

`schema-next` now has first-class stream metadata:

- `Schema::streams()`;
- `StreamDeclaration { name, token, opened, event, close }`;
- `EnumVariant::stream_relation()`;
- `StreamRelation::Opens(Name)` and `StreamRelation::Belongs(Name)`.

The authored schema shape is explicit. A namespace can declare:

```nota
RuntimeEventStream (Stream { token SubscriptionToken opened SubscriptionStarted event RuntimeEvent close SubscriptionToken })
```

Operation or event variants then carry the relation:

```nota
(SubscribeIntent SubscribeIntent opens RuntimeEventStream)
(MailSent MailSent belongs RuntimeEventStream)
```

The old direct lowerer and the `SchemaSource` path both understand this shape,
so the stream metadata survives into typed schema data instead of being guessed
from names.

## schema-rust-next

`schema-rust-next` now emits `signal-frame` streaming support only when the
typed schema declares a stream and the declared event type matches the
`Output.Event` payload.

The generated surface includes:

- `Frame`;
- `FrameBody`;
- `Request`;
- `ReplyEnvelope`;
- `RequestBuilder`;
- `Input::into_frame`;
- `Output::into_reply_frame`;
- `Event::into_subscription_frame`.

The compiled big-schema fixture constructs a generated event, turns it into a
subscription frame, encodes and decodes the rkyv frame, and verifies the body is
`StreamingFrameBody::SubscriptionEvent`.
