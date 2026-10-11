<!-- to-the-living:start -->
Presentation.{ «The lock queue» }

Status: all four proposals are unlanded. The Orchestrate in production has no queue; the queue is a proposal by Astra (0c85a3), not yet in any development branch.

Orchestrate today answers a Lock request at once. A request whose name or paths conflict with a held Lock is refused; any other is granted with the next ID. Release is by that ID, and the flow named in the Lock is a label, not an authority. Held Locks and the next ID survive a restart. There is no waiting line, so flows that want the same paths keep retrying, and the fastest retry wins: Astra reports one flow losing the Primary publish lock five times running.

Astra proposes a typed queue: Enqueue, ObserveQueue and Cancel, a durable ID sequence, and a Release that hands the freed Lock to the head of the queue in the same step, so no fresh request can take it first. Three things are open: the order of the queue, who may cancel, and what ends a Lock whose holder never releases.

[diagram: one Lock passing down the queue]
Flow A holds Lock 7
  on the books folder
        |
        | Release 7
        v
Orchestrate
  same step: grant the
  head of the queue
        |
        v
Flow B (was waiting)
  now holds Lock 8
        |
        v
Flow C keeps waiting
  (a new request from
   Flow D queues behind C,
   it cannot take the Lock
   first)

The file all four proposals land in is short; it stands today, whole:

    ---
    description: Orchestrate itself — its deployment, its meta binary, or the scope of its skill — is being designed or judged.
    dependencies: [operation-orchestrate]
    ---

    ## Deployment

    Orchestrate is deployed unconditionally, in the home, for every
    user. Its meta binary is part of it; a deployment without
    meta-orchestrate is wrong.

    ## The skill

    The orchestrate skill covers ordinary operations only; meta
    operations are outside it.

    ## Sources

    01a03d6e orchestrateDeployment
    01a03d6e orchestrateSkill

## 1. Distillation: a conflicting Lock request waits in a queue

Target: psyche-skills/skills/vision-orchestrate.md

Removed: none.

Added, as a new section after «The skill» and before «Sources»:

    ## The lock queue

    A Lock request that conflicts with a held Lock waits in Orchestrate's queue instead of being refused. Releasing a Lock grants it to the next waiting request in the same step; no later request takes it first.

Added to «Sources»:

    9993b5 mergeQueue

Source: flows/9993b5/vision/mergeQueue.md (2026-09-17). That record asks for a queue of reserved spots for merging; reading it as a queue for Orchestrate's Locks is this flow's inference.

Ruling: land as shown, or hold until the merge queue and the Lock queue are ruled one thing or two.

## 2. Distillation: the queue is ordered per conflicting paths

Target: psyche-skills/skills/vision-orchestrate.md

Removed: none.

Added, at the end of «The lock queue»:

    Requests wait in order of arrival only behind requests whose name or paths they conflict with; a request that conflicts with nothing held is granted at once, whatever else waits.

Added to «Sources»:

    9993b5 orchestrateLocking

Source: flows/9993b5/vision/orchestrateLocking.md (2026-09-17), where Orchestrate locks files rather than the whole repository. No record speaks of the queue's order; carrying that record over to the queue is this flow's inference.

Ruling, the order of the queue:
a. per conflicting paths, as shown;
b. one strict line for all requests, so a request on unrelated paths waits behind every earlier one;
c. another order (say which).

## 3. Distillation: who withdraws a request or a Lock

Target: psyche-skills/skills/vision-orchestrate.md

Removed: none.

Added, as a new section after «The lock queue»:

    ## Withdrawing

    A waiting request is cancelled, and a held Lock released, by the flow that made it. Another flow may withdraw it only when that flow is idle with no live subflow, or stale; a live holder is messaged instead. An idle flow's Locks and requests are forfeited.

Added to «Sources»:

    01a03d6e locks

Source: flows/01a03d6e/vision/locks.md (2026-08-26), on releasing before idle, forced removal by another flow, and forfeiture of an idle flow's Locks; the same rule for stale holders already stands in mind-skills/skills/operation-stale-lock.md. Extending it to waiting requests is this flow's inference. Today Orchestrate cannot tell who is asking: the flow in a Lock is only a label, so this rule needs the caller's identity checked by Orchestrate.

Ruling, who may withdraw:
a. the requesting flow, and any flow once that flow is idle or stale, as shown;
b. the requesting flow, and otherwise only through meta-orchestrate;
c. any flow holding the ID, as Release works today.

## 4. Distillation: a Lock is held for a time

Target: psyche-skills/skills/vision-orchestrate.md

Removed: none.

Added, as a new section after «Withdrawing»:

    ## A Lock is held for a time

    A Lock is granted for a set time. Before it runs out, Orchestrate asks the holder whether it needs more, and the holder may extend it; this is why a holder must be reachable. A Lock whose time runs out is released, the queue moves on, and the expired Lock stays observable so what happened can be investigated.

Added to «Sources»:

    108ab0 operational-timeBasedMergeSlots
    9993b5 mergeQueue
    01a03eda observe

Source: flows/108ab0/vision/operational-timeBasedMergeSlots.md (2026-09-17), where an unfinished reserved spot is let go and the holder is asked whether it needs more time; flows/9993b5/vision/mergeQueue.md (2026-09-17), where a spot that times out is investigated before deciding what to do; flows/01a03eda/vision/observe.md (2026-08-26), which names expired Locks as something to observe. The two 2026-09-17 records differ on whether a timed-out spot is released or held for investigation; the lines above release it and keep it observable, which is this flow's reading of both.

Ruling, what ends a Lock that is never released:
a. a time limit with extension on ask; on expiry release it and keep it observable, as shown;
b. a time limit; on expiry hold it, mark it expired, and remove it only through meta-orchestrate after investigation;
c. no time limit; only forfeiture when the holder is idle or stale, as in proposal 3.

## Distillation

The four proposals above all land in psyche-skills/skills/vision-orchestrate.md: 1, the lock queue; 2, its order; 3, who withdraws; 4, the Lock's time. Each carries its added lines and Sources lines; none removes a line.
<!-- to-the-living:end -->
