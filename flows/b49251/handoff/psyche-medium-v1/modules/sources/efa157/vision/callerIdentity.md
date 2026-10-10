# Caller identity

## A Nexus knows who talks to it: the CLI's process identified through the socket, Flow knowing which process belongs to which flow, the messaging and orchestrate nexuses the same; a standard identity part of the signal, optional in the signal library, so whoever talks to a socket knows to say whether it has the process id

Context: typed to the primary Claude efa157 on 2026-09-16 at 17:1xZ, the second half of the message whose first half is in transcriptReporting.md. Logged by the main flow before acting.

> I guess we're going to have to have some kind of wrapper that has this information, but it's actually really simple. It just means: have I checked the socket of the process? Can I identify the process that used this CLI, so we can know for sure? The Nexus can know if it's Flow, and Flow would know what process is associated with Flow. It's perfect for that, or the messaging one also, right? The orchestrate all of these things that need to know who's talking to them. They could do that and put that as a standard macro or object. I guess it's a standard signal, you could say. There's a standard part of this, which is a signal. There's this optional part of the signal library to let us add that to it. It would have to be added in the signal library, because then whoever talks to that socket needs to know to tell it if it has the process ID or not, right?

-- psyche, typed.
