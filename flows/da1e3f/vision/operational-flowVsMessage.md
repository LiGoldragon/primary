# Operational: flow is not message; ordinary vs meta socket

## `flow` is the ordinary CLI of Flow Nexus, and its job is to start or refresh a flow — not to send messages. Messaging goes through the Message Nexus, whose ordinary CLI is `message`. Two Nexus, two verbs; don't conflate

Context: typed to primary Psyche opus (Claude flow da1e3f) on 2026-09-17 correcting me twice in a row. I had first proposed a `flow-send` tool (rejected: use `message`), then muddled `flow`'s role. Logged by the main flow before acting.

> no, message, not flow-send. use the message nexus!

-- psyche, typed.

> flow is to start or refresh a flow

-- psyche, typed.

## Some features on Flow Nexus require the meta socket, like consuming a usage reset — those go through `flow-meta`, not the ordinary `flow`

Context: same message thread, continuation. First named example of a meta-socket feature. Logged by the main flow before acting.

> or to access some other features, some require the meta socket like using a usage reset

-- psyche, typed.
