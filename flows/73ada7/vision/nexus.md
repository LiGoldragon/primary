# Nexus

## 2026-10-09 — A Nexus's configuration loads atomically from separate files in different repositories: datom payloads the CLI sends in succession on the meta socket to start it

Context: the living's comment on «The new flows, as they run» (thread 51c6241f, 20:41), relayed in part by 445410. The closing order ("Let's do this.") is left out.

> Well, the Flow Nexus will be called directly with the right Datom command, and it might need a few. We need to allow the Nexus to have its configuration loaded atomically so that it can live in separate files in different repositories. That way, we don't have to solve the whole Datom path expansion for now, and we can just load all the configuration, even at different layers, using config files (basically Datom payloads for configuring that particular Nexus that the CLI can use in succession to start up that Nexus with the right payload on the meta socket). It's like a hack to get the Nexus started. This is brilliant.

-- psyche, STT, book comment, 2026-10-09T20:41, relayed by 445410.
