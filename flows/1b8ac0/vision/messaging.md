# Messaging

## Open the Raw capability on the meta socket; expose the meta socket to everybody for now as the unsafe interface; the message CLI uses Raw as a fallback when the checked interface is not there; commands are a typed queries enum set graded by how secure they are

Context: spoken to PsycheHigh (Fable, flow 1b8ac0) on 2026-09-21 after reading FM7 · Raw or FlowLocked in the Flow/Message question collection. Input mode STT. Locator appended below by a subflow. Logged by the main flow before acting.

> So the raw or flow lock just gave me an idea. It means that you open the raw capability on the meta socket. Right now, we can just expose the meta socket to everybody, so we can expose the unsafe interface. They can use the new message CLI in Nexus with the raw method as a fallback if the checked specified interface doesn't work (because there's no flow lock yet or something else). They want to debug or inject a command or something.
>
> We should have a typed command too, a queries enum set, depending on how secure they are, right? Some harnesses don't allow a lot of commands to be run when their model is running.

-- psyche, STT. 1b8ac00b, line pending.
Locator: 1b8ac00b:1706, 2026-09-21T21:44:14.216Z.

## Exposing the meta socket to everybody means locally only

Context: spoken to PsycheHigh (Fable, flow 1b8ac0) on 2026-09-21, answering the anatomy question whether "expose the meta socket to everybody" reaches across hosts. Input mode STT: "Metolaca" reads "meta socket". Locator: the message after 1b8ac00b:1664 in the same session; line to be appended. Logged by the main flow before acting.

> No, when I say "reach the Metolaca," it's only locally, obviously.

-- psyche, STT. ("Metolaca" reads "meta socket"; corrected here, left as spoken in the quote.)
Locator: 1b8ac00b:1753, 2026-09-21T21:46:13.337Z; typed confirmation "The meta socket" at 1b8ac00b:1762, 2026-09-21T21:46:22.635Z.

## FlowLock does not degrade to Raw: Raw is on meta and not usually accessible; FlowLock messages are the ordinary sends and Raw is FlowLock off, a shorthand; Flow is the only writer in a Herdr session, locks the session for the message, sends the text, unlocks, and answers Message with success or not

Context: spoken to PsycheHigh (Fable, flow 1b8ac0) on 2026-09-21, correcting PsycheHigh's framing of the living's earlier idea as a "fallback" and answering Mind's conflict (accepted decision: FlowLocked refuses with no downgrade). Input mode STT. Locator to be appended by a subflow. Ends with a working instruction ("Let's find all the problems and the anatomy involved in that"). Logged by the main flow before acting.

> No, I didn't say that the Flow lock degrades to raw. I said raw is on meta, so it's not usually accessible. Flow lock is basically that we can have it be a synonym or a link to what we're talking about: Flow lock messages, right? Just send, right, or whatever, send to, or all of these would be Flow lock messages, and then with Flow lock off, which could be synonymous with raw, you can have these shorthands like raw.
>
> It's just a shorthand for a certain configured type of messaging request, or a request to send this text into a particular harness. Flow takes care of the rest of making sure that there's no other writer because it is the only process that can write in that herder session. Eventually, it can safely send the message because it knows that nothing else is going to come in because it's locked that session for a message, right?
>
> It locks the message for the session to send the message, then it sends the message, then it removes the lock. The messaging will send a request to Flow to send the message, and Flow will say, "Yes, that window is locked." I guess Flow would even be the part that sends the text, so message wouldn't need to make this a two-part thing. It would just ask to send a message to a certain Flow, and then the Flow would say successful or not, basically.

-- psyche, STT.
Locator: 1b8ac00b:1872, 2026-09-21T21:49:14.522Z.
