# Flow Nexus main replacement contract

**Owner:** Mind Astra `4b0f60`, unchanged. **Status:** owner-scoped
architecture and implementation packet. It authorizes no source edit,
reservation, launch, restart, stop, archive, build, marker change, or route
change. Flow Nexus is the Herdr/Metaflow interface for multiple native mains
across aspects and same-aspect peers. Message remains ordinary durable delivery
and receipt authority, never Flow meta control. Children are not mains.

## Identity and durable operation

A stable logical destination is separate from a `FlowId`, native UUID, harness
session/binding generation, lifecycle generation, and aspect/power/profile
facets. Peers have distinct keys; aspect is not unique. Lifecycle epoch,
binding generation, native incarnation and request ID are different values.

`DurableReplaceOperation` is proposed with a replacement ID, idempotency
fingerprint, expected old binding/generation, exact authority, desired accepted
profile, and source/skill digest; it carries no secrets. Its phases are:

```text
Requested → AdmissionHeld → Quiescent | UnknownBlocking
          → SuccessorPreparing → ReadinessVerified
          → ContinuityAccepted → BindingCommitted
          → AncestorRetirementPending → Completed
```

`Held`, `Failed`, and `ReconcileRequired` retain evidence. Before commit, a
failed successor remains held; it never reopens the old ancestor. After commit,
recovery resumes explicit retirement and queues only to the exact new binding.
Retirement failure is blocked coexistence, never automatic old-binding rollback.
Journal external-call intent/results and exact resolution; never blindly replay
an ambiguous spawn.

## Admission, continuity, and delivery

Successor preparation uses existing Flow/Harness/Herdr machinery through one
controller, `4639`; no parallel launcher. Independent readiness verifies
native UUID, profile/model/effort, structured skills/context, title, exact
route, and harness binding. Continuity also needs owner work acceptance,
pending-child disposition and late-return relay. Native handles never transfer.

The logical binding changes only by authoritative CAS. Binding and outbox event
may commit atomically only in one authoritative transaction. A separate Message
database consumes a versioned event idempotently and checks committed binding
generation before each delivery; distributed atomicity is not claimed. Message
addresses the stable logical destination during hold; sender, deadline and
cancel never unlock admission. Transport acceptance differs from Read and work
completion.

Ordinary Flow sockets are control/query under their policy; meta sockets are
privileged registration/attestation, never a Message backdoor. Kernel peer,
service authority and caller claim are separate. Stale readiness/token replay,
unavailable/corrupt authority and ambiguous inflight calls fail closed. Actual
multiparty writer exclusion is required or replacement is blocked.

## Stop and archive

Binding commit does not reap an ancestor. Authorized stop first requires
admission hold and quiescence. Archive is later and separate: exact living
authority, single-use judgment, fresh native-process/Herdr absence after stop,
all-writer exclusion, and recoverable journal. No blanket ancestor deletion.
Preserve p6/p9, controller `6fb948`/`4639`, and protected routes/locks.

## Runtime and source boundary

Read-only evidence at `2026-09-23T18:21:34–18:22:12Z` found PID `3951304`
running `/home/li/.local/bin/flow-nexus` (SHA-256
`98f68df32f144efde2fd53c14e8afe35dce984db1f0ce957b63b281d6f923a0e`). Its
ordinary and meta sockets were mode 0600, listening and PID-owned. Typed
`flow resolve 6fb948` and `flow resolve 4b0f60` returned
`RecipientResolutionRejected.UnknownFlow` with exit 0. This proves daemon,
socket and codec response, not target liveness, registration, or availability.
The user unit is configured with `Restart=on-failure`; unavailable user DBUS
precluded a manager-state receipt. A bounded `root@prometheus` hostname witness
succeeded. Neither fact permits a restart.

Installed/source parity is **Unknown**: installed mtime predates inspected Flow
working `30121ae07db4fded66ae381c81909d0d9fa755dc` and published anchor
`61d765e4814035c2c0a1424e670a1b62da3d10b6`; binary hash/string inspection
does not establish a revision. Source schema v1 has Pending/Active lifecycle
and ordinary Start only for `codex-medium`, without typed aspect/main-peer
policy, occupancy, replacement, or retirement. Herdr idle/interactive-ready
route validation is not general availability. No installed Metaflow binary was
found. These are implementation gaps, not a daemon-absence claim.

## Owner packet and first slice

Current locks: `4639` Field `6fb948`; `3830` Medium `2c61af` only
`flow-nexus/src/lib.rs`; `3847` Low `e798` Codex/Herdr/prompt adapters; f72
`2836` Flow, `2862` Signal Flow, `2864` Message; `553901`, `1834`, `1835`
protected. Medium has no matched Herdr route and acceptance is unknown; Field
`6fb948` has an unread request to resolve the owner. Do not invent ownership.
Terra `0347d0` retains independent read-only runtime audit.

First select a coherent immutable experimental graph owner and remote-compile
the existing test surface. Then use an accepted disposable fixture for the
minimal verified Herdr registration-to-resolve proof; never arbitrarily
register known mains or restart protected services. The bounded first source
slice is read-only `ObserveRuntime` plus durable replacement skeleton/fixture,
then actual accepted native-pipeline wiring. It is not a parallel controller.

Required process-observable tests cover concurrent replacement, stale
token/generation and binding ABA, queued delivery across commit, Message
restart/event idempotency, crash at external boundaries, ambiguous inflight
call, old-binding zero effects after commit, unrelated peers, and fresh
successor acceptance. No tests ran.

## Sources

- `flows/4b0f60/reports/retirement-enforcement-contract.md` and
  `nexus-messaging-current-handoff.md`: admission, archive and Flow/Message
  boundaries; no replacement implementation receipt.
- `/root/census_contract_design` read-only runtime/source audit, 2026-09-23:
  PID/socket/resolve/parity and source-schema observations; no lifecycle action.
- Current `Observe.Locks` snapshot relayed by root: ownership/route limits.
