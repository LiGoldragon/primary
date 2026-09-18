# Operational: keep the messenger in sync with pane changes; test closing panes as failure scenarios

## Let's make sure the messenger is staying in sync with pane changes, because some messages ended up in panes that didn't have a harness running. Run light models in and test if closing a pane emulates failure scenarios, seeing what happens

Context: spoken by the living to primary Psyche opus (Claude, medium, flow
b05237) on 2026-09-18, after observing that split panes launched with
`codex exec` that errored left empty shells with no harness — messages routed
there would be lost. The living names two things: (a) the messenger must track
pane lifecycle so it does not route to dead panes, and (b) a test method —
run light models in panes, close them deliberately, and observe what the
messenger does. This extends the reaper vision
(operational-reaperSubflow.md) with the messenger angle, and connects to the
origin-ambiguity hazard from 1ac573's handoff. Logged by the main flow before
acting.

> Let's make sure that the messenger is staying in sync with pane changes, or if that affects it, because it seems maybe some messages ended up in panes that didn't have a harness running or something. I closed them up, but maybe you want to run some kind of sandbox herder. You can run light models in and then test if closing a pane is emulating some failure scenarios or something, and seeing what happens.

-- psyche, direct to primary Psyche opus b05237.
