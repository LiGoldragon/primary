# Flow

## 2026-10-28 — Scrap the queue for now
Context: the living, direct, after the held one-per-turn queue kept him from his flows for hours and its cause was found in the 0.40.0 drain.

> Okay here's the thing: the queue has been such a huge source of problems. Why don't we just fucking scrap it for now?

> I don't even understand why you guys are using the queue so much.

## 2026-10-28 — Not scrapped: the queue flushes as one message, the trigger included
Context: the living, direct, minutes after saying to scrap the queue, watching the Secondary take one call per held message.

> This is not hard to fucking implement so I don't know why we need to scrap it.

> If you have a queue and something, there should be more than one reason why the queue goes out. If, let's say for whatever reason, something comes in that should flush the queue, then all of the messages come into the pane as "one message". All of them, everything, including the one that comes in that gets the queue unstuck, come in as "one message". We don't send a message and then another message and then another message and then another.

> He's acting on incomplete information because every time he gets one more message, that means that what he acted on previously was missing that information. We get horrible results: high cost, slow behavior.

## 2026-10-28 — One fix per release; kill the Mind core Primary thread
Context: the living, direct, on Mind core Primary's turns ending in 429 on Astra, and on the Flow emergency release.

> There are no Astra limits. OpenAI has no limits on how much you can use Astra. Maybe just kill that thread. Make sure it's actually killed so that it doesn't hang around.

> We should only fix one thing at a time. If we fix too many things in one release and then we get broken behavior, it's hard to know what introduced what problem.

## 2026-10-28 — No EDN anywhere; it is all datom
> There shouldn't be EDN involved anywhere. Why are you talking about EDN? It's all datom.
