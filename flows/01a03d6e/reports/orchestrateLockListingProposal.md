# Orchestrate PathLock listing proposal

## Status

Superseded before implementation by
`reports/orchestrateLockInterfaceProposal.md`. The later proposal applies the
living's imperative-verb, `Lock`, `Observe`, Flow ID, and forfeiture rulings.
Nothing in this earlier proposal was implemented.

## Proposed outcome

Add one bounded request that returns all PathLocks active at one serialization
point:

```text
agent
  |
  | PathLockListRequest.{}
  v
orchestrate CLI -> ordinary socket -> Orchestrate Nexus
                                      | store mutex
                                      | one Sema snapshot
                                      v
agent          <- PathLocksListed.[...] <- sorted active locks
```

This is a diagnostic snapshot. It is stale as soon as another registration or
release succeeds. It is not a subscription, and callers must not poll it to
maintain a mirror.

## Ordinary contract

Append one operation and reply to `signal-orchestrate`, preserving every
existing route number and advancing the channel wire revision from 4 to 5:

```text
operation: List.PathLockListRequest
reply:     PathLocksListed.PathLockListing

PathLockListRequest.{}
PathLockListing.Vector<PathLock>
```

CLI request:

```sh
orchestrate 'PathLockListRequest.{}'
```

Empty state is a successful empty listing:

```text
PathLocksListed.[]
```

Example non-empty reply:

```text
PathLocksListed.[{alpha [/a /b] (first)} {beta [/c] (second)}]
```

No domain rejection type is added. A list has no ordinary refusal case in the
present authorization model. Parsing, environment, transport, framing,
storage, oversized-reply, and missing-reply failures remain operation failures.

## Snapshot semantics

- Copy the active PathLocks while holding the existing store mutex. Register,
  release, and list therefore have a single serialization order.
- Sort the result lexicographically by `PathLockName`, ascending. Storage
  iteration order is not public behavior.
- Preserve each stored lock's normalized path-vector order and description.
- Exclude released locks.
- In a multi-operation frame, a list observes preceding operations in that
  frame and not following operations.
- Add no timestamp, database marker, revision, cursor, pagination, filter, or
  subscription token.

The current frame limit remains the bound on the complete reply. If lock volume
ever makes that inadequate, pagination or streaming gets its own contract
rather than changing this snapshot's meaning.

## Authority and disclosure

The ordinary socket currently has no application-level caller identity. Its
filesystem ownership and permissions are the authorization boundary. This
proposal consequently exposes every active lock's name, absolute paths, and
description to every process that may connect to the per-user ordinary socket.

That full visibility is proposed deliberately: peers need a shared diagnostic
view of coordination state, and there is no honest basis for a "my locks"
filter without caller identity. Approval of this proposal includes approval of
that per-user disclosure boundary.

## Coordination rule

Listing is never permission to edit. `PathLockRegistered` remains the only
successful acquisition result. A caller that lists, sees no conflict, and then
edits without registering has a time-of-check/time-of-use race.

The eventual `orchestrate` skill should present listing as inspection and
diagnosis. `edit-coordination` should continue to require direct registration
and need not change for this feature.

## Implementation shape

```text
signal-orchestrate
  ethos/signal.ethos       request/reply vocabulary; wire revision 5
            |
            v
orchestrate
  store.rs                 ListPathLocks trait + atomic sorted query
  dispatcher               List -> PathLocksListed
  CLI                      parse request and render reply
  tests                    contract, store, and live Nexus behavior
            |
            v
deployment
  signal contract release -> Nexus release -> Home/Nix deployment
  -> Curriculum orchestrate skill -> Primary regeneration
```

The store implementation should add a `ListPathLocks` trait on the data-bearing
`OrchestrateStore` and return `PathLockListing`. No new Sema table, durable
record, store migration, socket, executable, or meta operation is required.

## Proof required before deployment

1. Contract round trips for the empty request and empty/non-empty replies,
   including exact Datom examples and wire revision 5.
2. Store tests proving empty state, inclusion after registration, exclusion
   after release, and deterministic name ordering.
3. A concurrency witness proving each reply is one whole pre- or post-mutation
   snapshot, never a torn mixture.
4. Live Nexus proof: list empty, register locks out of name order, receive the
   sorted listing, release one, and receive the reduced listing.
5. Existing duplicate-name, overlap, release, restart, framing, and generated
   contract gates remain green.
6. Consumer regeneration and Nix checks pass before the Curriculum skill is
   deployed.

## Explicitly outside this proposal

- Continuous observation, subscriptions, and polling.
- Per-caller filtering or redaction.
- Historical or released locks.
- Pagination and server-side filters.
- Any meta-socket operation or material.
- Reviving the retired Orchestrate operation catalogue.

A future maintained view should be a separate push subscription with an
initial typed snapshot followed by typed deltas. It requires sequence,
backpressure, disconnect, restart, and snapshot/delta ordering decisions that
do not belong in this listing operation.

## Sources

- `/git/github.com/LiGoldragon/signal-orchestrate/ethos/signal.ethos` — current
  ordinary vocabulary and wire revision.
- `/git/github.com/LiGoldragon/orchestrate/src/store.rs` — current PathLock
  persistence, query, and serialization boundary.
- `/git/github.com/LiGoldragon/orchestrate/src/transport.rs` — current
  one-request/one-reply transport and frame bound.
- `/git/github.com/LiGoldragon/orchestrate/README.md` and `ARCHITECTURE.md` —
  current released Nexus documentation.
- `flows/01a02a34/vision/pathLocks.md` — stripped-down PathLock vision.
- `flows/01a03d6e/reports/orchestrateSkillProposal.md` — deployed ordinary
  operation boundary and skill state.
- Flow `01a03d6e` subflow code reads and design reviews — current contract,
  privacy boundary, deterministic ordering, and deployment consequences.
