---
title: 289 — Nexus Internal Control Interface
role: operator
variant: Design
date: 2026-06-02
topics: [nexus, internal-interface, recursive-engine, backpressure, actor-scheduling, sema-load]
description: |
  Refinement after Spirit 1464: recursive Nexus does not need to start as a public subprocess protocol. The cleaner first model is a daemon-internal Nexus control interface. Nexus receives external facts through Signal and SEMA completions, but it can also produce internal control actions that schedule more Nexus work, defer SEMA work, shed load, preserve tracing/logging, or notify clients that the system is busy.
---

# 289 — Nexus Internal Control Interface

## Fresh Refinement

The new distinction is:

- External component interface: Signal in, Signal out, SEMA commands and completions.
- Internal Nexus interface: recursive computation, scheduling, overload handling, and runtime control.

That means recursive Nexus does not have to appear first as
`InvokeNexus(Box<Nexus<X>>)` in the public schema surface. It can start
as a daemon-internal control root that Nexus uses to keep deciding.

This fits the prior operator lean:

```text
NexusWork -> NexusEngine -> NexusAction -> runner -> NexusWork | Signal reply
```

But it sharpens the meaning of `Continue`: it is not just "call Nexus
again." It is "put more typed work into the Nexus control loop."

## Shape

The external roots stay straightforward:

```nota
NexusWork [
  (SignalArrived Input)
  (SemaWriteCompleted SemaWriteOutput)
  (SemaReadCompleted SemaReadOutput)
  (EffectCompleted NexusEffectResult)
  (ControlCompleted NexusControlResult)
]

NexusAction [
  (ReplyToSignal Output)
  (CommandSemaWrite SemaWriteInput)
  (CommandSemaRead SemaReadInput)
  (CommandEffect NexusEffectCommand)
  (CommandControl NexusControlCommand)
]
```

The new inner interface is a control vocabulary:

```nota
NexusControlCommand [
  (ScheduleNexus NexusScheduleRequest)
  (DeferSemaWrite DeferredSemaWrite)
  (DeferSemaRead DeferredSemaRead)
  (AssessLoad LoadAssessmentRequest)
  (ShedLoad LoadSheddingRequest)
]

NexusControlResult [
  (NexusScheduled NexusScheduleReceipt)
  (SemaWriteDeferred DeferredReceipt)
  (SemaReadDeferred DeferredReceipt)
  (LoadAssessed LoadAssessment)
  (LoadShed LoadSheddingReceipt)
]
```

This keeps recursive scheduling typed and local. The Nexus action says
"run this control operation"; the runner executes it; the completion
returns as `NexusWork::ControlCompleted`.

## Why This Is Better Than Public Subprocess First

Designer 477's subprocess idea is useful, but it jumps to a broad
cross-component recursion story before proving the local runtime need.

The local Nexus-control interface is a cleaner first proof because it
expresses the immediate problem:

- SEMA may be busy.
- Nexus may still need to keep accepting, tracing, triaging, and
  replying.
- Nexus may need to choose "defer durable work" or "tell the client the
  database is busy" rather than block the whole component.
- Runtime scheduling is a decision surface, not a persistence surface.

SEMA remains the durable state actor. Nexus becomes the actor that
decides when to use SEMA and when not to.

## Actor Scheduling Interpretation

This creates a future path where Nexus becomes the runtime coordinator.
Not in the sense of replacing the actor runtime, but in the sense of
making policy decisions that the actor runtime executes.

Examples:

```text
Database is busy -> Nexus defers SEMA writes and replies Busy to low-priority clients.
Trace pressure is high -> Nexus prioritizes trace ingestion and lowers expensive reads.
Client asked for a huge Observe -> Nexus commands SEMA read, stashes result, replies with handle.
Nexus queue is overloaded -> Nexus sheds low-priority requests before touching SEMA.
```

That is still the triad:

```text
Signal = admission and reply
Nexus = decision and scheduling
SEMA = durable state
```

The control interface just gives Nexus a local actuator for decisions
that are not SEMA operations and not client replies.

## Backpressure As A Schema-Defined Reply

If Nexus decides the database is too busy, that should not be an ad hoc
error string. It should be a schema-defined Signal reply:

```nota
Output [
  (RecordAccepted SemaReceipt)
  (RecordsObserved ObservedRecordsReply)
  (RecordRemoved RemoveReceipt)
  (Busy BusyReport)
  (Rejected SignalRejection)
]

BusyReport {
  reason BusyReason
  retry RetryGuidance
}

BusyReason [DatabaseBusy NexusOverloaded MaintenanceMode]
RetryGuidance [(RetryAfter Integer) RetryLater]
```

Then Nexus can choose:

```text
Sema queue too deep -> ReplyToSignal(Output::Busy(...))
```

That is real decision-making. It avoids pretending every request can
always reach SEMA immediately.

## Implementation Lean

The next implementation should not introduce cross-component recursive
Nexus yet. It should introduce local control:

1. Keep `NexusWork` / `NexusAction`.
2. Add `NexusControlCommand` / `NexusControlResult`.
3. Add `BusyReport` to Signal output.
4. Add a runner-owned queue/load snapshot object that Nexus can inspect
   through `AssessLoad`.
5. Add one behavior: if SEMA is marked busy, `Observe` returns
   `BusyReport` instead of calling SEMA.
6. Trace it: the trace should show Signal admission, Nexus decision,
   control/load assessment, Nexus re-entry, Signal busy reply.

This is smaller than the stash pilot but may be more fundamental. It
proves Nexus as runtime decision-maker before Nexus as result-stashing
or subprocess orchestration.

## Relationship To Prior Reports

Report 287 said Nexus recursion is:

```text
NexusWork -> NexusEngine -> NexusAction -> runner -> NexusWork | Signal reply
```

Report 288 said generic `Nexus<Root>` must stay schema-enumerated.

This report adds: one of the schema-enumerated action families is
`NexusControlCommand`, a daemon-internal interface for scheduling,
load assessment, and backpressure.

So the merged model is:

```text
External facts enter Nexus.
Nexus emits typed actions.
Some actions command SEMA.
Some actions command local Nexus control.
Completions re-enter Nexus.
Only ReplyToSignal exits to the client.
```

## Bottom Line

The important new idea is not "Nexus recursively calls itself" in the
abstract. It is that Nexus owns the computation-control loop inside the
daemon. That loop can prioritize work, avoid overloading SEMA, preserve
tracing/logging, and return honest `Busy` replies when the system cannot
serve a request cleanly.

This makes Nexus feel like the center of decision rather than a
projection function between Signal and SEMA.
