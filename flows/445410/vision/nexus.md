## Nexus configuration loaded atomically from files

Context: the living's comment on «The new flows, as they run» (thread 51c6241f, 2026-10-09 20:41), on the passage "Flow Nexus sockets exist; the inspected launcher source does not call them".

> Well, the Flow Nexus will be called directly with the right Datom command, and it might need a few. We need to allow the Nexus to have its configuration loaded atomically so that it can live in separate files in different repositories. That way, we don't have to solve the whole Datom path expansion for now, and we can just load all the configuration, even at different layers, using config files (basically Datom payloads for configuring that particular Nexus that the CLI can use in succession to start up that Nexus with the right payload on the meta socket). It's like a hack to get the Nexus started. This is brilliant. Let's do this. Get this ratified, and then [Mind]. Let's get [Mind] making this on Astra on its own, even Astra and Sol topic flow.

-- psyche, typed, 2026-10-09. Transcription corrected: "mine" → "Mind".
