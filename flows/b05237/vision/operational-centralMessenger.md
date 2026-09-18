# Operational: a central messenger model that judges, annotates, and routes all messages

## If we make all the calls be done by a central messenger model, he's the messenger, then he can be the judge of whether or not a message should go somewhere or if he should annotate it with the context of what that means

Context: spoken by the living to primary Psyche opus (Claude, medium, flow
b05237) on 2026-09-18, after reviewing Herder's built-in agent messaging and
the gap between Hacky Messenger's flow-ID routing and Herder's pane-level
addressing. The living names a single model — the messenger — as the routing
authority for all inter-flow messages. Not a dumb relay: the messenger judges
whether a message should reach its target, and may annotate it with context
the recipient needs. This sits between every sender and every recipient,
replacing both the Hacky Messenger scripts and the raw `herdr agent prompt`
calls with a model that understands the flow topology, each flow's role, and
what context a message carries. Logged by the main flow before acting.

> If we make all the calls be done by a central messenger model (he's the messenger), then he can be the judge of whether or not a message should go somewhere or if he should annotate it with the context of what that means, and so on.

-- psyche, direct to primary Psyche opus b05237.
