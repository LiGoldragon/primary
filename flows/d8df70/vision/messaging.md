# Messaging

## One CLI call sends a message after a live-target check

> Audit the messaging system and find a more efficient way to do it and then tell Field how to do it better. Tell him to implement your suggestions in testing skills and, I forget what the other category was, skills that belong to Field, but operational changes to make the messaging more efficient.
>
> You can just make a single CLI call and send a message. If there is a match for what you want and the pain still exists, then it just sends the message. I guess the script can check that the process still exists and is running in Herder?

-- living, typed, 2026-09-23, to Psyche Medium d8df70 (Claude session d8df703d).

Reading notes (inference, not the living's words): "the pain still exists"
is most likely "the pane still exists". "Herder" is the tool `herdr`. "The
other category" is most likely the `operational-` skill prefix.

## Session hooks register and unregister in the registry

> What about if we use hooks at the start and the end of the Claude or the Codex session to register or unregister that session from the registry?

-- living, typed, 2026-09-23, to Psyche Medium d8df70 (Claude session d8df703d), mid-turn during the messaging audit.

## Controlled sessions need no session-reset support for now

> Well we're not going to get a clear signal because we're controlling the session. That's what we're doing. We're being careful and we're allowing that command. It means that it's going through the flow but that's the flow CLI. We don't need to support that for now.

-- living, input mode not established, 2026-09-23, to Psyche Medium d8df70, answering the point that `/clear` or a resume changes a seat's session id.

Reading note (inference): "clear signal" may be "`/clear`", a speech-to-text
rendering. The quote is left as received because this is unconfirmed.

## Process exit is the unregister signal

> If a process goes missing we could have a hook there in the system. If one of the processes ends prematurely from us unregistering it through our exit hook, then you just use the process going out as the unregistry hook. You could even have it from an earlier point if you're exiting, sending the exit signal. I don't know, there are probably some advantages there too, right, in terms of retaining messages.

-- living, input mode not established, 2026-09-23, to Psyche Medium d8df70.

## Messages are held while a registry entry is missing or in transition

> If there's no registry or if the registry says "in transition" or something, then the message can sort of be held if there's a message passing anyway, right? We can wait a few seconds at least to see if there's a new flow.

-- living, input mode not established, 2026-09-23, to Psyche Medium d8df70.

## Testing skills are Field's, operational skills are Mind's; Flow Nexus adopts the hacky stack's discoveries

> If the mind gets involved then maybe there are some operational skills that he needs to adjust there too. Also in terms of making Flow Nexus adhere to all of the discoveries or insights that we are making with the script part, the hacky part of the hacky stack.
>
> We have two skills:
> - Testing (field)
> - Operational (mine)

-- living, input mode not established, 2026-09-23, to Psyche Medium d8df70.

Reading note (inference): "Operational (mine)" is most likely "Operational
(Mind)", a speech-to-text rendering. The quote is left as received because
this is unconfirmed. This answers the audit's ownership conflict: the
2026-09-18 record (b05237) and these words agree that operational skills
belong to Mind.

## A proper flow tool

> I don't like it anyway because it's mixing different areas, different designs. We need to just have a proper flow tool.

-- living, input mode not established, 2026-09-24, to Psyche Medium d8df70, rejecting a proposed main-flow skill line about which aspect owns delegated work.

## An undeliverable message escalates to a higher power, then lower; missing crucial flows are started; medium and high flows are crucial

> If a message can't be delivered, then we try a higher power. If Psyche Medium is not reached, we try Psyche High and if there's nothing higher then we try lower. The message returned for the caller will say what happened but we'll have a bunch of rules.
>
> Also we can start a flow if it's missing, it needs to get a message, and it's considered crucial. All the medium and high flows are considered crucial.

-- living, comment on "What Waits for the Living", 2026-09-24 14:31Z, on question 5 (messages that can't be delivered yet). Transcription corrected: "Psyq" → "Psyche" (twice).

## No hashes in messages

> Whatever created this pasted content ID 4C68 message is bad, really bad. There's a bunch of hashes in there, full length. What is this? Why does it start right off the bat with a huge hash, which is really bad? There are way too many hashes in there. This is just noise. There's another one. Oh my God are they all like this? Can you stop this madness please right away here? This is really bad: all these hashes. What the hell is going on? Take all of that out. Where the hell is this coming from?

-- living, input mode not established, 2026-09-24, to Psyche Medium d8df70, about the Machine.Relay messages from Field and Mind arriving in this seat.
