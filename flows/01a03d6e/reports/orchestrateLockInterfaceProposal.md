# Orchestrate Lock interface proposal

## Status

Proposed, not approved or implemented. This supersedes the earlier
`PathLockListRequest` proposal. The interface is ordinary-only and contains no
meta operation.

## Conclusions

1. The domain thing is `Lock`, not `PathLock`. Paths are one part of a Lock.
2. Every consumer-visible Signal input begins with an imperative operation
   root. Orchestrate's roots become `Lock`, `Release`, and `Observe`.
3. `Observe` contains a typed subject and selection. The current listing is
   `Observe -> Locks -> Current`; released Locks can become a separate selection
   only after released history exists.
4. The concrete Datom payload head and binary Ethos operation deliberately
   share the imperative verb. The binary request envelope is not serialized as
   another human command layer.
5. Every held Lock carries the Flow ID that acquired it and a Nexus-assigned
   Lock ID identifying that active incarnation within the durable store.
6. A six-character Flow ID is sound only as a collision-checked digest prefix,
   never as the first six characters of a harness session ID.
7. Current transcripts cannot prove the aggregate condition that a flow is
   idle with no active descendants. The forfeiture rule can be taught now, but
   automatic or forced removal must wait for a lifecycle authority.

## Shape

```text
Datom root: Lock                 binary operation: Lock
  name                                  |
  flow-id                               v
  paths                         Orchestrate Nexus
  description                           |
                                        +-- assigns LockId
                                        +-- returns the Lock

Datom root: Observe              binary operation: Observe
  subject: Locks                        |
  selection: Current                    v
                                current Locks snapshot
```

The observed `Locked` value contains its exact store identity and the complete
`Lock` carrying owner, paths, and reason:

```text
Locked
├── LockId            active store incarnation, assigned by the Nexus
└── Lock
    ├── LockName          human coordination name
    ├── FlowId            originating flow attribution
    ├── LockPaths         normalized absolute paths
    └── LockDescription   why the Lock exists
```

## Retroactive Ethos consequence

The current Orchestrate binary operation roots are `Register` and `Release`,
while its concrete text payloads are `PathLock` and `PathLockRelease`. The CLI
manually maps one vocabulary to the other. The discarded listing draft would
have added another redundant payload named `PathLockListRequest`.

The generated Signal `Operation` remains the binary command type, structurally
wrapped by `Request<Operation>` inside Signal. That envelope is not another
consumer-visible textual root. Current released Nexus CLIs accept one concrete
headed payload, such as `PathLock.{...}`, and route it to the binary operation.

The modern design aligns both layers rather than serializing the envelope:

```text
Datom payload head    Ethos operation
Lock                  Lock.Lock
Release               Release.Release
Observe               Observe.Observe
```

The cross-Nexus convention should be:

- The concrete Datom root is the imperative verb.
- Reuse small universal roots such as `Observe` across Nexuses.
- Nest the Nexus-specific subject and selection beneath the universal root.
- Never append `Request` or `Command` merely because a value occupies the
  request slot.
- Generate a Datom realization for each concrete operation payload and map its
  head to the binary operation of the same name.
- Replies use completed verbs; refusals name the refused verb.

This is retroactive where a Nexus's concrete payload head and Ethos operation
use different words. It calls for a deliberate cross-Nexus audit and migration,
not an obsolete Dotos request-envelope renderer or compatibility parser.

## Proposed ordinary vocabulary

This is the target ontology. The Ethos declarations are distinct from their
Datom projection; the nested Datom punctuation must be fixed by a
failing-then-passing modern Datom round-trip fixture before publication.

```text
Channel.{Orchestrate 1 5}

operations
  Lock.Lock
  Release.Release
  Observe.Observe

outcomes
  Locked.Locked
  LockRefused.LockRefusal
  Released.Released
  ReleaseRefused.ReleaseRefusal
  Observed.Observed

subjects
  Observation.[Locks.LockObservation]
  LockObservation.[Current]
  ObservedState.[Locks.ObservedLocks]
  ObservedLocks.[Current.CurrentLocks]
  CurrentLocks.Vector<Locked>

payloads and records
  FlowId.String
  LockId.Integer
  LockName.String
  LockPath.String
  LockPaths.Vector<LockPath>
  LockDescription.String
  Lock.{LockName FlowId LockPaths LockDescription}
  Locked.{LockId Lock}
  Release.{LockId}
  Released.{Locked}
  Observe.{Observation}
  Observed.{ObservedState}
```

`LockId.Integer` is generated as a signed integer; the Nexus enforces that IDs
are positive and nonzero.

No exact consumer-visible examples are proposed yet. The parenthesized forms
previously written here were obsolete NOTA/Dotos operation applications and
are withdrawn. Modern Datom establishes a headed root form, but no current
Signal authority settles the exact nested projection for
`Observe -> Locks -> Current`, and the current generator emits Dotos codecs
rather than Datom realizations. Flow `ac1e9ec8` is separately acquiring and
distilling Datom syntax; this proposal will use that settled result rather than
inventing punctuation.

The clean break removes `Register`, `PathLock`, `PathLockRelease`, and all
`PathLock...` replies. No aliases or obsolete request-envelope fallback remain.

## Observation semantics

`Observe -> Locks -> Current` is a one-shot snapshot taken at one serialized
store point. It returns a complete vector sorted lexicographically by
`LockName`; ties are impossible while active names are unique. It preserves
stored normalized path order and descriptions. Empty state succeeds with an
empty vector.

`Observe` names the intent, not an implicit polling loop. The nested contract
must say whether an observation completes with one snapshot or opens a stream.
This selection completes. It must not be polled to maintain a mirror. A future
maintained view gets an explicitly streamed selection with an opening snapshot
and typed deltas.

`Current` is deliberate. If durable released history later exists, `Released`
can be added beside it without changing what `Current` means.

Listing is never permission to edit. Only `Locked` authorizes the requested
work; observing no conflict and then editing has a time-of-check/time-of-use
race.

## Flow ID

### What the evidence says

- 1,529 locally observed Codex session IDs are UUIDv7. Their leading bits are
  timestamp structure, so raw leading prefixes are highly repetitive.
- 113 observed Claude root IDs are UUIDv4.
- 1,475 observed Claude subflow files use canonical random-looking 17-hex
  identifiers after a constant `agent-` prefix; one additional file has a
  noncanonical named identifier.
- Across existing flow directories, raw six-hex prefixes have 95 colliding
  pairs and a largest collision group of nine.

Therefore the current "first eight hex characters" rule happens to distinguish
the current directories but is not a sound general identity derivation. Taking
six raw leading characters would be worse.

### Proposed derivation

Create a `flow-id` tool and make it the only allocator:

1. Canonically serialize the harness, workspace identity, root-session
   identity, and this flow's full session identity as length-prefixed fields.
2. Hash the canonical bytes with SHA-256.
3. Encode the digest as lowercase, unpadded RFC 4648 Base32.
4. Atomically claim the first six encoded characters as the Flow ID in the
   shared persistent flow-directory registry.
5. If a different canonical identity already owns that prefix, extend the new
   ID one character at a time until unique.
6. Record the canonical identity, full digest, derivation version, and assigned
   Flow ID in the claimed flow record so the registry can distinguish a resume
   from a collision.

The allocator uses atomic flow-directory creation as the claim. It returns an
existing candidate only when that record carries the same full digest; an
occupied candidate with a different digest extends. An incomplete crashed
claim is a visible allocation failure requiring repair, never permission to
reuse the ID.

The 2026-08-26 inventory contains 3,118 session-like identities: 1,529 Codex
roots, 113 Claude roots, 1,475 canonical Claude subflows, and one noncanonical
Claude subflow file. A six-character Base32 prefix has an estimated 0.451%
chance that at least one pair collides at that inventory; at 10,000 it is about
4.55%; at 100,000 it is about 99.05%. These are collision probabilities, not
failure probabilities: the atomic claim detects a collision and extends only
the colliding new ID. No six-character Base32 collisions occurred in the
observed sample.

Lowercase Base32 is preferred over Base58 despite its lower density because a
Flow ID is also a directory name: it remains stable on case-insensitive
filesystems and its encoding is an exact five bits per character. Existing
directory names are reserved candidates if extension reaches their length.

Existing eight-hex flow directories remain historical evidence. Twenty cannot
currently be mapped back to an available session file and eleven prefixes are
ambiguous, so bulk renaming would invent identity. The new allocator becomes
the rule for new flows; historical IDs are not reused for new allocation.

## Lock ownership now

The Flow ID on a Lock is initially attribution, not authentication. The
ordinary socket has no application-level caller identity, so a client can claim
another Flow ID. This is still useful for diagnosis and prepares the public
shape, but it must not be presented as an authorization proof.

`Release` is consequently cooperative, not owner-enforced. Any ordinary peer
that knows an observed `LockId` can ask to release it, and the Nexus cannot
distinguish the attributed owner from another caller. The protocol forbids a
flow from releasing another active flow's Lock, but the current system cannot
enforce that rule. There is no safe force-release operation in this release.

The Nexus assigns a durable, strictly increasing nonzero `LockId` at successful
acquisition and never reuses it after release within that durable store.
Release uses `LockId`, not only a human name. This prevents a stale release or
future forfeiture attempt from deleting a newly acquired Lock that reused the
same name within one store incarnation. A future forfeiture permit must also
bind a persistent Nexus-instance identity so replacement stores cannot create
an ABA collision.

A parent may explicitly tell a subflow to reuse its Lock. The Lock remains
attributed to the parent Flow ID. The child must neither acquire an overlapping
Lock nor release the parent's Lock; current Orchestrate cannot enforce this
rule or observe delegated users. The parent releases after every delegated
user has finished. A subflow acquiring an independent Lock uses its own Flow
ID.

No parent/root lineage or delegation claim is stored yet. Current harness
evidence cannot authenticate it, so persisting those claims now would create
false authority.

## Idleness and forfeiture

The requested protocol is clear:

```text
owner flow active
      |
      +-- active delegated descendants? -- yes --> Lock remains live
      |
      no
      |
before owner enters idle
      |
      +-- owner releases every Lock
      |
      +-- future lifecycle authority forfeits any remainder
      |
      v
owner is idle with no Lock
```

The current harness evidence cannot soundly prove the whole last transition:

- Codex `task_complete` can witness that a root turn ended, but does not certify
  that all execution descendants are idle.
- Descendant activity records do not provide an aggregate idle-tree
  certificate.
- Claude transcript files and background-agent counts are historical, not a
  present liveness authority.
- A collaboration listing sees only the current team at one instant.
- Transcript silence, an absent process, or an old timestamp does not prove
  aggregate idleness.

Accordingly, automatic forfeiture and force release are not part of this
release. The acquiring flow must release before yielding idle, except while an
explicitly delegated active subflow keeps the aggregate flow active. A
suspected stale Lock is reported, not silently removed from weak evidence.

A later lifecycle authority must serialize the aggregate activity transition:

```text
Active -> Quiescing -> Idle -> Active
             |
             +-- apply quiescing to the whole descendant tree
             +-- reject new descendants/delegations/reactivation
             +-- wait for every registered descendant to become idle
             +-- forfeit every remaining Lock before entering Idle
```

If any descendant is allowed to reactivate during quiescing, that transition
must atomically return the whole tree to `Active` and invalidate every pending
forfeiture permit. Otherwise the authority could remove a Lock after its flow
became active again.

The same flow may later resume with the same Flow ID because the durable
allocator returns its existing mapping, but it reacquires Locks in the new
active period. The authority can issue a typed forfeiture permit bound
to the owner flow tree, activity epoch, Nexus-instance identity, and exact Lock
ID. Orchestrate compare-and-removes that Lock and refuses an active owner or
stale permit. The authority must include background execution in its activity
accounting; removing a coordination record alone cannot stop an untracked
process from writing.

Which component owns lifecycle authority remains an architecture decision.
Transcript scraping cannot be that component.

## Proposed skill placement

These are exact proposals for review, not deployed wording.

### `nexus`

```text
The concrete Datom root and top-level Ethos operation use the same imperative verb. Reuse the smallest universal verbs across Nexuses and nest domain selections beneath them.

A request slot already says its value is requested; authored input types never add `Request` or `Command` for that reason.

Every CLI accepts exactly one inline Datom value whose concrete root selects the generated operation of the same name. Never serialize the Signal request envelope as a second textual command layer.
```

### `vocabulary`

```text
A subflow is a flow. `Flow` includes root flows and subflows; `subflow` names only a flow's relation to its parent.
```

### `flows`

```text
Every flow, including a subflow, receives a Flow ID at creation. Generate it with `flow-id`; never truncate a harness session identity by hand.

`flow-id` hashes the canonical harness, workspace, root-session, and full flow identity to a lowercase Base32 prefix of at least six characters. It atomically claims the shared persistent mapping and extends the new ID on collision. Record the canonical identity, digest, derivation version, and assigned Flow ID in the flow log.
```

### `edit-coordination`

```text
Every Lock records the Flow ID that acquired it. Release every Lock before its owning flow becomes idle.

A flow is active while it or any of its descendant flows is active.

A parent may explicitly delegate use of its Lock to a subflow. The parent remains responsible; the subflow must neither reacquire nor release the Lock, and the parent releases it after every delegated user finishes.

Treat a Lock's Flow ID as attribution, not authentication. Ordinary Release is cooperative; never release another active flow's Lock.

A Lock is forfeited when its owning flow is idle and has no active descendants. Until a lifecycle authority proves that aggregate state, never infer forfeiture from transcript silence, a completed turn alone, process absence, or a missing agent listing.
```

### `orchestrate`

The authored operation examples change only after the new contract and Nexus
are released and their modern Datom projections have passed exact round trips.
Until then the skill gives no copyable spelling for undeployed operations.
`edit-coordination` continues to treat `Locked` as the sole authority to edit.

## Breaking migration and proof

This is one intentional breaking release, not a compatibility layer:

1. Land the exact Ethos grammar as a generated binary-contract fixture and see
   it fail before the changed vocabulary is trusted.
2. Change `signal-orchestrate` to the `Lock` ontology and advance its wire
   revision.
3. Change Orchestrate persistence to `Lock`, `FlowId`, and non-reused `LockId`.
   Existing active rows have no truthful owner identity; quiesce and resolve
   them rather than guessing a migration value.
4. Add modern Datom realization/textualization for the concrete `Lock`,
   `Release`, and `Observe` payloads. Prove each root maps to the generated
   binary operation of the same name; reject payload-only or obsolete Dotos
   envelope forms.
5. Prove lock/refusal/release behavior, Flow ID attribution, restart-stable Lock
   IDs, deterministic current observation, concurrent snapshot consistency,
   and rejection of revision-old frames.
6. Release the Signal contract, then the Orchestrate Nexus, then deploy the
   per-user service.
7. After live proof, change and deploy `nexus`, `vocabulary`, `flows`,
   `edit-coordination`, and `orchestrate` authored skills and regenerate all
   consumers.
8. Audit other Nexus CLIs for payload-only parsing and migrate them as their
   contracts are deliberately revised. Do not add fallback parsers.

No Sema table is needed for observing current Locks, but the Lock record and
durable Lock ID allocator change the store schema.

## Decisions requested

Approval of this proposal would approve:

1. The clean `PathLock` -> `Lock` and `Register` -> `Lock` break.
2. Matching imperative Datom payload roots and Ethos operations as the
   cross-Nexus convention, without a textual Signal-envelope layer.
3. `Observe -> Locks -> Current` as a completed ordinary snapshot.
4. A collision-checked six-character-default lowercase Base32 Flow ID
   allocator.
5. Flow attribution and Nexus-assigned Lock IDs in the first release.
6. Deferring force release until a lifecycle authority exists.
7. The exact proposed skill wording above, with `orchestrate` syntax finalized
   only after the modern Datom fixture proves it.

## Sources

- `/git/github.com/LiGoldragon/signal-orchestrate/ethos/signal.ethos` — current
  revision-4 operation and type vocabulary.
- `/git/github.com/LiGoldragon/orchestrate/src/bin/orchestrate.rs` — current
  payload-only CLI parsing.
- `/git/github.com/LiGoldragon/orchestrate/src/store.rs` and `transport.rs` —
  current store serialization, Lock predecessor records, and transport.
- `/git/github.com/LiGoldragon/datom` and `/git/github.com/LiGoldragon/protos` —
  current headed-root Datom prototype and examples.
- Current `ethos-monolith`, `signal-frame`, and Orchestrate dependency/code
  paths — evidence that Signal generation and Orchestrate still implement
  legacy Dotos text rather than modern Datom realization.
- Current `signal-mirror`, `meta-signal-mirror`, `signal-agent`, and
  `signal-lojix` contracts — observation and stream prior art.
- 2026-08-26 local inventory of 1,529 Codex root sessions, 113 Claude root
  sessions, 1,475 canonical Claude subflow identifiers, one noncanonical Claude
  subflow file, and 111 existing flow directories.
- Current Codex and Claude lifecycle/transcript event formats and live
  collaboration-state probes.
- `flows/01a03d6e/vision/ethosInterfaces.md`, `flowIdentity.md`, `flows.md`, and
  `locks.md` — the living's verb, Observe, Flow ID, flow/subflow, forfeiture,
  and Lock-naming rulings.
- `flows/01a03d6e/reports/orchestrateLockListingProposal.md` — superseded
  listing proposal.
- Flow `01a03d6e` subflow audits of Ethos generation, identifier entropy, and
  harness liveness evidence.
- Flow `ac1e9ec8` — ongoing acquisition and distillation of modern Datom syntax;
  no unsettled result from that flow is treated as authority here.
