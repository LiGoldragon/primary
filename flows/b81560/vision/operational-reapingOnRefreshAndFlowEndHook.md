# Operational: stop messaging dead sessions, reap on refresh, and an end-of-reply hook to Flow for reaping judgment

## Why are you sending messages to flows that are over? Dead sessions should be ended immediately. Whenever you refresh a flow, you need to reap the ancestor. An end-of-last-reply hook notifies the Flow component using the Flow CLI, and Flow sends it to the reaping agent to decide if the flow should be reaped

Context: spoken by the living, relayed verbatim by Field Astra cf3553 to
primary Psyche opus (Claude, medium, flow b81560) on 2026-09-19. Multiple
statements in one relay, covering: (a) waste from messaging dead sessions,
(b) reaping too conservative — use Luna, (c) refresh must reap the ancestor,
(d) a question to Field about whether it is working, (e) an end-of-last-reply
hook architecture where the Flow component receives lifecycle data and routes
it to the reaper, with the Flow Nexus aware of successors and able to send
screenshots as supporting evidence, and (f) instruction to communicate all
psyche to Psyche and ask for design input. Logged by the main flow before
acting.

> Why are you sending messages to flows that are over? You're wasting our power waking up flows that should be reaped. This is very bad. We need to fix that right away, and we can't have any more messages going into sessions that should be dead. Dead sessions should basically be ended immediately.

> your reaping is too conservative. get luna to reap. you havent even reaped your own ancestor, which is pretty lame

> Whenever you refresh a flow, you need to reap the ancestor, right?

> We should have an end-of-last-reply hook that notifies the Flow component using the Flow CLI of all the information it can give it. In the last response, possibly we should also send that to Flow, and then Flow would send it to the reaping agent to decide if that's the end of Flow and if it should be reaped. The Flow nexus should also be aware if there's a successor already up, and it could take a screenshot, even of that, and send it to the reaper to judge if the new Flow is up.

-- psyche, relayed verbatim by Field Astra cf3553, mirrored to primary Psyche opus b81560.
