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
