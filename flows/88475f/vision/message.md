## A message is really just a message

Relayed by e51411 as #psyche; spoken to e51411 on 2026-09-25, on the machine message fields.

> I think that there are too many fields. This timestamp is fucking huge. It's taking so much fucking room and most of the message you got is just gibberish. Let's cut this [right] the fuck down. A message is really just a message. What is this machine relay? Is that like a key-value map? You're using that to kind of emulate the variant?

-- psyche, STT, relayed by e51411. Transcription corrected: "Write the fuck down" → "cut this [right] the fuck down" (correction by the living, per e51411).

## Big messages and the psyche message type

Relayed by e51411 as #psyche; spoken to e51411 on 2026-09-25, on big messages and the psyche-verbatim message type. The leading elision is e51411's.

> I would rather that we can send big messages than have the agents read the files ... Oh right, that's why I wanted to include this psyche-type message. Instead of "message [msg]" being like "psyche" or something, it's verbatim "psyche" with context. I guess first is the context and then the verbatim. We should allow big message size because passing around files like that, I don't think, is better than just dealing with the pasting thing with Claude.

-- psyche, STT, relayed by e51411. Transcription corrected: "MSD" → "msg" (per e51411).

## Psyche messages split into 800-character pieces for Claude

Relayed by e51411 as #psyche; spoken to e51411 on 2026-09-25. Context from e51411: psyche messages stay under Claude's paste wrapper by splitting.

> The psyche type message is working now. We can use these to spread what the psyche has said to other places. Somebody could do multiple calls where he sends a regular message from machine to machine along with another message, so that the size limitation for the psyche is maybe that we only send the psyche messages at 800 characters in size for Claude. We split it up into pieces so we can have a broken-up psyche verbatim if we need more room.

-- psyche, STT, relayed by e51411.

## Spread the psyche with every message that rests on it

Relayed by e51411 as #psyche; spoken to e51411 on 2026-09-25, on spreading the psyche with every message that rests on it. The elision is e51411's.

> I guess you could spread it to whoever you're messaging, whenever you need to quote psyche on whatever created this message. If there's a psyche or more than one psyche verbatim with context behind it, that's when you would send them and you can retrieve them. This is going to be a skill. You can retrieve them from the raw psyche log and then use them in the message so that it comes stronger into the context of the receiving flow. It comes in the prompt, in the user prompt, so it reinforces the narrative better than just reading them. ... It would send a series of them along with maybe one or two machine-to-machine messages.

-- psyche, STT, relayed by e51411.

## No 800-character limit, no part numbers in psyche messages

Spoken to 88475f on 2026-09-25, after the relays arrived as "#psyche [sender context 1/1 verbatim]".

> Let's remove the 800-character limit and take out the 1-out-of-1, 1-out-of-2 thing in the [psyche] messages.

-- psyche, STT. Transcription corrected: "psychic" → "psyche".

## Fix the record when somebody's missing

Spoken to 88475f on 2026-09-25, after Mind Sol reached this seat by direct Herdr fallback because the messenger's route record for it was malformed.

> Let's create a way to fix the record when somebody's missing.

-- psyche, STT.

## Record repair is a judgment call by a thinking machine

Spoken to 88475f on 2026-09-25, after 88475f said it did not know whether the messenger could repair a missing route by itself.

> I think it'll be a judgment call. There's going to be a machine involved, a thinking machine, to make the judgment and then add the pane into the registry or something (because I don't know if we can programmatically figure out what's what so easily).

-- psyche, STT.

## Message passes through Flow; no arbitrary typing into panes

Spoken to 88475f on 2026-09-25, ordering work on Message with Flow after the Fable refresh.

> ... trying to get a datom-based message system that uses Flow to lock the panes and stuff and essentially passes the message through Flow.
>
> You have to configure and create the features that the message will probably need on the meta socket since we're not going to want to allow anything to just write into panes. Message will sort of be like a prioritized access thing or we expose a [safe] interface. We're not going to want arbitrary typing of messages so message will be the interface to send messages to other panes.
>
> We need to check to make sure that it's not just sending a command like `/compact`. At the same time we want to expose these interfaces through the Flow CLI at whatever authority level they need to be at. I guess compact could probably be meta level. I'm leaning towards that but anyway it's not important. I'm just using it as an example.

-- psyche, STT. Transcription corrected: "save interface" → "[safe] interface".

