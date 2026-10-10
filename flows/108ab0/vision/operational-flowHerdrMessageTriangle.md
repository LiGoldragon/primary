# Operational: the Flow ↔ Herdr ↔ Message triangle

## Flow uses Herdr sessions to keep track of these flows. Message asks Flow for the Herdr position of the recipient, and then sends the message through Herdr. That is the draft — Codex is to see if it is possible and build it with Flow, Message, and Herder

Context: typed to primary Psyche opus (Claude, medium, flow 108ab0) on 2026-09-17 after 108ab0 investigated herdr's actual verbs and confirmed `herdr agent start`, `herdr agent prompt`, `herdr agent send-keys`, and `herdr session` provide the primitives. This entry captures the architecture the living just laid down and delegates the feasibility check + build to Codex. Logged by the main flow before acting.

> Flow uses Herder sessions to keep track of these flows, and then Message can ask it for the Herder position, and then it can send it a message through Herder. Ostensibly, that's just a draft you can see if Codex can see if it's possible and build it with Flow, Message, and Herder.

-- psyche, typed.
