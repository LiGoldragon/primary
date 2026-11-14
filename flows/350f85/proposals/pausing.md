Presentation.{ «A flow is paused, and resumed while it is hot» Proposal }

# A flow is paused, and resumed while it is hot

Created by Fable 5.2.

### Proposal 1: Pausing · psyche-belief › vision/flow-nexus/0.md

::: comment
His words, 13 November: «Are they being reaped automatically, and does this reaping let us resume the same flow if we want to send it more work, so that we can use the hot cache from its work? It would be cool if the Nexus could actually keep track of that, whether or not a flow is hot in the cache. If someone tries to message a flow with the same aspect, topic, and model, it would just reanimate that flow.» «We need to have different types of flows: some that don't get automatically reaped, taken down, or whatever. I don't like the word "reaping." Maybe they get paused, right?» «I certainly need Fable to be able to talk, and Opus and a few Codex flows should stay up, I think, in case I want to talk to them directly. Maybe a few, like a field saw core and a mine core saw, would be good to keep up permanently.» Later: «Okay, so this on-demand Permaflow, could it be resumed if we tried to message it? That's because if we do that, we have to be able to reuse its cache, because its cache now is still warm.» «If it's on demand, then it doesn't need to refresh so eagerly, right? If it has a job to do, we might be better off letting it run its job, depending, right? Some models are really expensive to run past a certain threshold, but we certainly could use a higher threshold for jobs. Essentially, you could say an on-demand Permaflow kind of behaves a little bit like an ephemeral flow in the sense that it stops when it stops working.»
:::

::: shown
psyche-belief › vision/flow-nexus/0.md
An idle flow keeps its harness, so that the living finds the flow he was talking to.
:::

- An idle flow keeps its harness, so that the living finds the flow he was talking to.
+ A permaflow is maintained or on demand, by its configuration. A maintained flow keeps its harness while idle, so that the living finds the flow he talks to. An on-demand flow stops when its work stops: it is paused, its harness closed and its session kept.

::: shown
psyche-belief › vision/flow-nexus/0.md
A permaflow that is woken resumes its last flow when that flow’s context is still warm in the cache and under a size its configuration sets; otherwise it starts a fresh flow.
:::

- A flow woken for a permaflow is almost always a fresh flow, an old one only when the new input is literally the continuation of that topic.
+ A permaflow that is woken resumes its last flow when that flow’s context is still warm in the cache and under a size its configuration sets; otherwise it starts a fresh flow.

+ A flow has two thresholds, each configured for its model: one at rest, past which it is refreshed where it would have been paused, and a higher one while it works, so that a flow with a job runs it to the end.

+ ```ethos
+ Signal
+ [ flow:[ Address Model HarnessCache ] ]     ; imports: HarnessCache as «Configuration follows the ontology» proposes it
+ [ Configure.Set ]                           ; inputs, on the meta socket: one value at a time
+ [ Configured.Set ]                          ; outputs
+ [ Set.[ Keeping.{ Address Keeping }         ; types: how a permaflow is kept while idle
+         HarnessCache                        ;   how long a harness's cache holds an idle session
+         Threshold.{ Model AtRest Working } ] ;   the context a flow may hold, as a percentage of its window
+   Keeping.[ Maintained                      ;   keeps its harness
+             OnDemand ]                      ;   paused when its work stops
+   AtRest.Integer                            ;   refreshed at rest past this
+   Working.Integer ]                         ;   higher: a job is run to its end below this
+ ```

+ ```datom
+ Configure.Keeping.{ { Mind core Sol } Maintained }
+ Configure.Keeping.{ { Mind flowNexus Sol } OnDemand }
+ Configure.Threshold.{ Sol 40 70 }
+ Configure.HarnessCache.{ Claude 60 }
+ ; a request arrives for a paused permaflow, 20 minutes after its last turn: the same session answers
+ ; the same request 3 hours after: a fresh flow starts from the handover
+ ```

## Questions

1. Maintained, as I read you: Psyche core Fable, Psyche core Opus, Mind core Sol and Field core Sol. Does Psyche get a Sol of its own?
