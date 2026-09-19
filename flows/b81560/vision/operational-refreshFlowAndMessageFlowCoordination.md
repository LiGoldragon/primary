# Operational: a refresh flow that blocks message inbox/outbox during spawn, witness screenshots, and the three nexuses — Flow is field, Message and Psyche are the other two, plus the Mentci router

## A refresh flow spawns the new pane, blocks the old flow's inbox and outbox through the messenger, caches both sides. Flow and Message coordinate: Flow tells Message the pane is stable, Message delivers. Witness screenshots for debugging and audit. Flow is like the field aspect, and there's going to be a psyche nexus and the Mentci nexus that talks to everything with the right permissions. The router enum is part of the Signal standard — add a new nexus, everybody recompiles

Context: spoken directly by the living to primary Psyche opus (Claude, medium,
flow b81560) on 2026-09-19. The living describes the refresh coordination
between Flow and Message: Flow blocks the old flow's messaging (inbox and
outbox) during refresh, caches both sides, creates the new pane and flow,
and only unblocks when the successor is live. Flow tells Message when a pane
is stable and has a living flow. Witness screenshots of the pane at message
delivery time for debugging and audit. The living names the three nexuses:
Flow (field aspect), Message (mind aspect implied), and a third psyche nexus
plus the Mentci nexus that routes to everything with compiled signal contracts.
The router enum is part of the Signal standard — adding a nexus to the cluster
means everybody recompiles. Logged by the main flow before acting.

> There should be a flow called refresh flow that allows the flow to refresh itself. It will take care of spawning and locking the fact that something is being spawned, with the messenger telling it that it's creating a new pane or whatever. If it has to block anything, then it creates the pane and it creates the flow. It doesn't send messages to the old flow, so it has blocked the message. It has told the messenger to block that flow inbox and outbox, and so the messenger caches both sides. If the old flow tries to send a message, or if a message tries to get to it, it blocks both sides, so everything is blocked at the right time.
>
> You can figure out the rest. This kind of architecture: message and flow can block each other at the right time if they need to lock something. They can tell the flow, "I need to send a message," right? The flow makes sure this pane stays up, and then the message goes through because the flow told the message, "Yes, this pane is stable and has a living flow in it. You can send your message."
>
> You can even have a witness screenshot taken of that pane when the message goes in, for debugging or for Flow to look at it for audit, to see if that message went through and was received by the harness. We can put all kinds of automation there, which is really cool for debugging. These two components just work together, kind of like psyche and mind, which is funny because the flow kind of personifies more like the field aspect. There's going to be a third aspect here soon, I'm pretty sure: a third nexus, probably psyche. There's going to be a psyche and mind nexus and the Mensch nexus that can pretty much talk to everything if it has the right permission. It's going to be compiled with all the different signals and probably the routing system to be able to talk to multiple things, which is probably what happens when any component can talk to more than one thing. The router enum is part of the Signal standard, too. We have all of the different nexuses in Signal. If we add a new thing to the cluster of nexuses, then everybody has to recompile to be able to talk to it, but that's okay.

-- psyche, direct to primary Psyche opus b81560. ("Mensch" reads "Mentci"; corrected.)
