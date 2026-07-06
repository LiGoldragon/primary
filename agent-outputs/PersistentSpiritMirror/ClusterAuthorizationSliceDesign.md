# Cluster Authorization Slice Design — the criome cluster authorizes propagation of spirit's state

Design for the next vertical slices. Design only; nothing was edited or
committed in any code repo. This is the pickup point for implementation
workers.

Revised 2026-07-06 after psyche review. Folded corrections (all settled
intent): enum addressing with no string identifiers for fixed sets (§1),
batched authorization (§3.4), receiving-side acceptance check (§4.2), the
operational cluster quorum contract as a root-issued sub-contract (§5), and
the former open questions on window and unfounded posture (§0).

Ground truth verified against source on 2026-07-06, re-verified in part in
the revision pass:

- `spirit` main `5541dd3a` ("retire spirit-side quorum, restore criome_gate
  1-of-1 authorization direction", primary-6kz1) — the working copy moved
  DURING the first design pass; a concurrent lane is active in spirit.
  Re-verify the spirit tree state on pickup.
- `criome` main (0.5.0 line): two-round commit, witness clock, durable
  anti-equivocation ledger (`(contract, head) → AuthorizedObjectReference`,
  `root.rs:1788-1868`), real `RouterQuorumVoice::submit` over `RouterClient`
  (`criome/src/voice.rs:240`).
- `router` main: pubkey-keyed durable route store (`CriomeHostId`,
  `InstallRemotePeer`, `remote_route_durable.rs`), durable outbound backlog,
  encrypted peer session, the witnessed founding proof
  `router/tests/founding_over_router.rs` (named output
  `router-two-hosts-found-root-over-router-voice-test`), and the
  criome→standard hand-mapping in `router/src/authorized_object_projection.rs`
  (dissolves under §1).
- `sema-engine` main: hash-chained log (`EntryDigest::from_entry_fields`
  folds `previous_entry_digest`, `versioning.rs:257`, v2 domain tag) and a
  durable outbox with shipped cursor (`outbox.rs`: `unshipped()` yields the
  ordered unshipped suffix; `acknowledge` advances the cursor with typed
  forks).
- Sibling artifacts built on: `CriomeHostAwareness-BuildDesign.md`,
  `CriomeHostAwareness-CurrentStateScout.md`, `Handover-CriomeOperational.md`.

## 0 · Settled constraints (psyche intent — not redesigned here)

- Spirit knows nothing about quorums. Spirit asks its local criome host to
  authorize each head advance and propagates only when authorized.
- Criome runs the two-round commit across the founded cluster for every head
  advance. Members auto-approve; nothing is checked beyond well-formedness.
  Only the founding contract is manually approved. Approval predicates
  (lineage checks, fork rules, thresholds) are explicitly OUT of scope.
- Quorum can't complete = operation refused; the head does not advance
  (cluster-visibly). Fail-closed.
- Everything over the network goes through the router; the router only
  routes. No criome concepts in router-facing design or names.
- **No strings for fixed sets.** Psyche: "Strings should be avoided in
  software design; prefer an enum type when a set doesn't vary often;
  recompilation is not a big deal if the set doesn't constantly change"
  (public Spirit record). Every identifier of a fixed set is a closed enum
  in the contract layer, defined once (§1).
- **The Criome host ID is the only network identifier.** Each host runs
  exactly one instance of each component. A destination is the pair
  (Criome host ID, component); a spirit message goes to that host's one
  spirit, preset and deterministic (§1).
- **The root is the root; there is only one.** The operational cluster
  quorum contract is a sub-contract of the root — issued and anchored by
  it, with its own distinct contract identity (§5); after the early
  prototype phase the root itself is not the contract operational rounds
  run over. Right now the root keys and the first sub-contract keys are
  identical: same hosts, same criome installation, no key export.
  Air-gapping and guarded-root operations are deferred design, not part of
  this slice map. The slices of §3–§4 prototype on the root directly, as
  explicit staging.
- **Quorum window**: an owner-configurable duration with a reasonable
  default covering the two rounds plus network round-trips — nothing
  ceremonial. Order of tens of seconds live, seconds in tests.
- **Gate enabled + local criome unfounded = refuse loudly** (terminal
  `Unavailable`, head held). Founding is rare and precedes system liveness;
  a silent park would hide misconfiguration.
- **Trust boundary confirmed**: the components form one engine; cryptography
  is criome's domain at both ends of every network boundary; spirit never
  re-verifies BLS locally (§3.2).
- Mirror is a verb. No mirror-noun component; the separate mirror daemon
  stays dropped (primary-nbmq).
- A concurrent lane (primary-6kz1) is removing spirit's 1-of-1 local criome
  authorization and adding a spirit-side option to disable criome
  authorization entirely (disabled = fully local, the operative default for
  now). This design targets that end state: **the 1-of-1 gate no longer
  exists**; when criome authorization is enabled, it is CLUSTER
  authorization from the first slice.
- The name "voice" is being renamed away by a concurrent worker. This design
  says "criome's router submission path" and proposes no new name containing
  "voice".

## 1 · The addressing model — host ID + component enum, no strings

Cross-cutting; every slice below speaks it. This section is the target
model; §4.3 names where the changes land.

**Destination = (CriomeHostId, ComponentKind).** The Criome host ID (the
host criome's master public key) is the only network identifier. Each host
runs exactly one instance of each component (criome, spirit, orchestrator,
mind, ...), so the pair is a complete address: no actor names, no lookup
service, no registration of actor homes. The router's durable route store
is already keyed by `CriomeHostId`; the `homes:
HashMap<ActorIdentifier, CriomeHostId>` indirection
(`router/src/remote_router.rs:38-45`) and the `ActorIdentifier(String)`
newtype (twinned in signal-router `:30` and signal-criome `:30`) dissolve.
Local delivery is one closed table: ComponentKind → the local component
ingress (owner-configured socket per deployed component); a component not
deployed on the host is a typed refusal, fail-closed.

**One ComponentKind, defined once.** The vocabulary belongs once in the
shared contract layer (contract-repo: "duplicate local wire types" is a
named mistake). Today it exists at least four times, hand-mapped:
signal-standard (14 variants, `schema/lib.rs:31`), signal-criome (7
variants, `schema/lib.rs:670`), signal-persona (9 variants — the one the
router itself uses for supervision, `router/src/supervision.rs:12`), plus
signal-orchestrate and meta-signal-mentci. The router's
`authorized_object_projection.rs` exists solely to hand-map signal-criome's
`ComponentKind` / `AuthorizedObjectKind` / `AuthorizedObjectReference` onto
their signal-standard twins, variant by variant. Resolution: signal-standard
owns the single `ComponentKind`, `AuthorizedObjectKind`,
`AuthorizedObjectReference`, and `ObjectDigest`; every other signal-* crate
re-exports rather than twins; the projection file and all variant-by-variant
`From` mappings are deleted. The variant set is closed and recompiles when a
component is born or dies (the `Mirror` variant retires with the
mirror-noun). Settled intent, not style.

**Contract dispatch by component, not by string.** `RoutedContractObject`
routes today by `ContractName(String)` + `ContractOperation(String)`
(signal-router `schema/lib.rs:739`, literals like `"signal-criome"` in
`criome/src/conveyance.rs:35`). This dies: one component speaks one contract
(`signal-<component>`, per contract-repo naming), so the destination
component enum IS the contract selector. The forwarded envelope carries
source and destination as (host ID, component) pairs plus opaque payload
octets; the receiving component decodes the payload against its own
contract, whose operations are typed enum variants inside the payload —
never a string beside it.

**The authorization ask is the typed reference.** `SignalCallAuthorization`
carries three string-newtype fixed-set fields — `ContractName`,
`ContractOperationHead`, `AuthorizationScope` (signal-criome
`schema/lib.rs:1688`; spirit fills them with literals at
`criome_gate.rs:317-325`) — while the same schema already owns the typed
shape: `AuthorizedObjectReference { component: ComponentKind, digest:
ObjectDigest, kind: AuthorizedObjectKind }`. The request becomes the typed
reference plus requester identity and optional expiry; the string trio
dissolves. A spirit head advance is exactly
`{ component: Spirit, kind: Head, digest }`.

**Identifier value types.** `CriomeHostId` is currently a `String` newtype
without `Hash` (the route registry keys on its string payload,
`remote_router.rs:33-37`); it becomes the typed master-key bytes it names.
`ObjectDigest(String)` becomes typed digest bytes. These are values, not
fixed sets, but they leave the string shape in the same sweep.

## 2 · What already exists (the slices reuse, not rebuild)

| Piece | Where | Status |
|---|---|---|
| Two-round commit driver (Request round then verified Commit round, majority-of-total, witness-clock gate on both, durable rounds) | `criome/src/actors/root.rs:1328-1786` | Built, audited, in-process proven |
| Member auto-approval of quorum votes (well-formedness only: round-id binding, member-set check, own-clock window check, non-double-sign veto) | `criome/src/actors/root.rs:1393-1470` (`solicit_quorum_vote`) | Built — this IS the psyche's "members auto-approve" |
| Anti-equivocation veto, durable-first, idempotent for an identical re-proposal | `criome/src/actors/root.rs:1809-1868` | Built |
| Criome's router submission path (`SubmitRoutedObjects` origination, fire-and-forget, unreachable peer leaves the round Gathering) | `criome/src/voice.rs` | Built, proven by the founding proof |
| Cross-node two-round over two real routers on loopback TCP | `router/tests/founding_over_router.rs` | Witnessed (founding) |
| Streaming authorization observation: submit, snapshot, pushed updates until a terminal state | criome daemon `handle_streaming_connection` + client `CriomeClient::authorize_signal_call` → `CriomeAuthorizationObservationSession::next_update` (`criome/src/transport.rs:334-401`) | Built — the correct consumption shape spirit must adopt |
| BLS-signed `AuthorizationGrant` (master-key signature over `AuthorizationGrantStatement` signing bytes, binding slot + authorized object digest + contract) | `criome/src/actors/signer.rs:173-192,351-395` | Built |
| Hash-chained log + durable outbox: `unshipped()` = ordered suffix past the shipped cursor; outbox row written in the entry's own transaction | `sema-engine/src/versioning.rs:257`, `src/outbox.rs` | Built |
| Spirit post-commit gate seam: commit locally, then authorize before fan-out; refusal holds the head, local commit stands | `spirit/src/engine.rs:667` (`gate_and_ship_head`), `spirit/src/daemon.rs:146-178` | Built (currently 1-of-1-shaped; being reworked by primary-6kz1) |
| Spirit apply ingress for a pushed authorized record, re-judged by the receiver's own criome | signal-spirit `ApplyAuthorizedRecord` (variant retained; currently answered fail-closed at `spirit/src/nexus.rs:1305`), `CriomeGate::evaluate_carried` (`spirit/src/criome_gate.rs:432`) | Built then parked — §4 reactivates and batches it |
| Router durable outbound backlog + drain on peer-session establishment | `router` §2.10, `outbound_backlog_durable.rs` | Built |

The slices are therefore mostly WIRING of proven halves, plus one deliberate
contract-parsing fix (§3.2), the addressing/contract consolidation (§1,
landing per §4.3), and the contract extensions of §4.3.

Slice map: §3 = cluster authorization of a batched head advance (prototyped
over the root contract); §4 = authorized propagation with receiving-side
acceptance; §5 = the root issues the operational cluster quorum
sub-contract. (Earlier artifacts said "slice 1/2" for §3/§4.)

## 3 · Slice: cluster authorization of a spirit head advance (batched)

One sentence: spirit asks its local criome host over the working socket to
authorize its current head digest — covering the whole unshipped suffix;
that host originates the existing two-round commit across the operational
quorum contract's members over the router; the terminal verdict is pushed
back to spirit over the held socket; spirit ships only on Granted, and a
quorum that cannot complete expires the request fail-closed.

### 3.1 · The ask: spirit → local criome

Spirit's side stays exactly one question with no quorum vocabulary:
"authorize this head digest." Concretely:

- Spirit submits `CriomeRequest::AuthorizeSignalCall` carrying the typed
  `AuthorizedObjectReference { component: Spirit, kind: Head, digest }`
  where the digest is spirit's CURRENT head — the head of the whole
  unshipped suffix (§3.4). No contract-name, operation, or scope strings
  (§1); no Evidence; no window: policy is criome's. This is a signal-criome
  contract change carried by this slice.
- Spirit consumes the reply as an **observation session**, not a one-shot
  reply (§3.2).
- The `SpiritAttestor` contract/Evidence machinery and the
  `EvaluateAuthorization` origination path in the gate are retired with the
  1-of-1 direction (they made spirit carry criome's policy vocabulary).
  `evaluate_carried` STAYS — it is the receive-side seam §4 needs.
  Coordinate with primary-6kz1 on what its rework already removed.

End-state configuration (owned by the concurrent lane, restated for
coherence): a closed spirit-side mode — criome authorization Disabled
(fully local, seam dormant, operative default) or Enabled(socket). Enabled
with no reachable criome holds every head back. There is no 1-of-1 mode.
`GateDecision::Unconfigured` disappears with it: an enabled gate always has
a socket; a disabled gate never runs.

### 3.2 · The seam-drift resolution (deliberate; security-sensitive)

**Witnessed failure** (reproduced in the first pass, spirit main `5541dd3a`,
deps repinned to main):
`criome_gate_1of1::socket_only_gate_observes_signed_auto_approved_authorization`
fails with `CriomeGateError::UnexpectedReply { reply:
"AuthorizationObservationSnapshot(...)" }`.

**Root cause.** The criome daemon now serves `AuthorizeSignalCall` on the
streaming connection path (`criome/src/daemon.rs:212-234`): it submits the
request, and instead of writing the one-shot reply it opens an authorization
observation and writes `CriomeReply::AuthorizationObservationSnapshot`
first, then pushes `AuthorizationUpdate` stream items until a terminal
status. Spirit's gate (`criome_gate.rs:419-457`) still performs a one-shot
`CriomeClient::send` and pattern-matches a bare
`CriomeReply::AuthorizationGranted` — off-contract, so it errors. The error
is fail-closed (the head is held), which is the correct accident; the fix
must preserve that posture everywhere.

**Resolution: adopt criome's shipped session contract.** Spirit replaces the
one-shot send with `CriomeClient::authorize_signal_call(authorization)`
returning a `CriomeAuthorizationObservationSession`, then drains
`next_update()` until a terminal state. This is not merely a parsing fix; it
is the shape cluster authorization REQUIRES: a two-round commit over the
network is not answerable in one frame. Pending-then-pushed-terminal is the
normal case; the auto-approve immediate grant is just the fast path where
the terminal state is already in the snapshot. The special case dissolves.

It is also the push-not-pull fix: criome (the producer of the verdict)
pushes the update over the held socket; spirit never polls. The
agent-guardian `wait_for_pending_authorization` loop in `criome_gate.rs`
(100 ms sleep + re-`ObserveAuthorization`) is a polling pattern; this slice
should migrate it to the same observation session while touching this file
(small, contained; flag to the implementer).

**Session parsing rules — the security-sensitive part, exact and closed.**
Every rule violation is a `CriomeGateError` (a machinery fault) and every
fault holds the head. There is no default-open branch anywhere in this
parse:

1. **Slot binding.** The session token is the request slot criome assigned
   to THIS submission. Spirit considers only state records whose
   `request_slot` equals the session token. It must NOT take
   `snapshot.states().first()` unfiltered. (Note: criome's own client helper
   `transport.rs:355` currently derives the token from `states().first()` —
   acceptable only because the submission connection's snapshot is scoped to
   the submitted request; spirit still re-filters by the token on every
   state it reads, and the criome-side helper should be hardened to filter
   rather than take first — a small criome fix in this slice.)
2. **Digest binding.** `state.request_digest` must equal the submitted head
   digest (the `ObjectDigest` projected from the captured `EntryDigest` —
   one projection feeds both the request and the check, as today).
3. **Terminal Granted requires the grant.** `status == Granted` with
   `grant == None` is a fault, never an authorization. The grant must
   satisfy `grant.request_slot == token` and
   `grant.authorized_object_digest == submitted digest`. Status alone is
   never proof.
4. **Terminal non-Granted refuses.** `Denied` / `Expired` / `Unavailable`
   map to a typed refusal decision (head held, outbox waits, next drain
   retries). These are outcomes, not errors.
5. **Non-terminal waits.** `Pending` / `Signing` / `Parked` keep the session
   draining pushed updates. The session runs on a `spawn_blocking` worker
   (the `CriomeClient` stream is synchronous) with a read deadline slightly
   beyond the authorization window — sized for the catch-up case, which
   chains two rounds (§3.4) — so the actor mailbox is never blocked and a
   silently dead criome process cannot hold the session forever. A deadline
   expiry is treated as Unreachable → head held.

**BLS verification of the grant signature by spirit: deliberately NO** —
confirmed by psyche review; the trust boundary stands as designed. The grant
carries `authorization_grant_signatures` (`StampedSignatureEnvelope`,
BLS12-381 MinPk, signed by the local criome's master key over the
`AuthorizationGrantStatement` signing bytes). Spirit does not verify them,
for three reasons stated so the decision is auditable:

1. **The channel is the trust boundary.** The socket is owner-configured and
   filesystem-permissioned to the co-resident criome. Verifying a signature
   received over channel X against a public key learned over the same
   channel X adds no security — same trust root, circular.
2. **Spirit must stay quorum-ignorant.** Real verification of a
   cluster-backed grant means threshold counting against the quorum
   contract's member registry — importing criome's entire verification
   vocabulary into spirit,
   against settled intent.
3. **Verification lives where the trust boundary actually is.** Where the
   authorization crosses a real boundary — node to node, §4 — the RECEIVING
   node's criome performs the full cryptographic judgment and the
   local-acceptance check (§4.2). Every network boundary gets exactly one
   full re-judgment, by a criome, never by spirit.

Spirit's checks are therefore binding checks (slot, digest, status,
grant-presence) plus chain checks on its own store (§4.2 — sema-engine
digest integrity is spirit's own data structure, not signature
cryptography). The BLS material is carried opaquely as evidence for §4 and
for audit.

**Negative tests locking the posture** (unit level, stub criome socket):
Granted-without-grant → held; mismatched `request_digest` → held; mismatched
`grant.authorized_object_digest` → held; foreign `request_slot` records
ignored; session deadline expiry → held; daemon writing a bare
`AuthorizationGranted` (old shape) → held as off-contract. Plus the repaired
positive: snapshot-with-terminal-Granted authorizes (fixes the failing
test).

### 3.3 · Criome-side: the Quorum-mode bridge to the two-round commit

The gap: today `AuthorizeSignalCall` in `Quorum` mode
(`criome/src/actors/root.rs:333-344`) is handed to the
`AuthorizationCoordinator`, which creates a Signing state and waits for
manually routed signatures. Nothing connects an incoming authorization
request to the two-round cluster commit — that connection previously lived
in spirit (retired by primary-6kz1). This slice builds it INSIDE criome,
where it belongs.

Behavior of `AuthorizeSignalCall` by `AuthorizationMode` (the existing
closed enum — no new flags):

| Mode | Operational quorum contract present | Behavior |
|---|---|---|
| `AutoApprove` | any | Unchanged: immediate self-signed grant (dev/bootstrap fast path; the loopcheck's degenerate case) |
| `ClientApproval` | any | Unchanged: park for owner approval (the agent-guardian flow) |
| `Quorum` | yes | **NEW: originate the two-round commit over the operational quorum contract** — during the prototype stage this is the founded root contract, an explicit staging decision; from §5 on it is the root-issued sub-contract |
| `Quorum` | no | **NEW: terminal `Unavailable` pushed immediately** — fail-closed, refuse loudly (settled): founding is rare and precedes system liveness; a node whose spirit gate is enabled but whose criome is unfounded is misconfigured and must not hold silently |

No component-specific recognition of "spirit": in `Quorum` mode EVERY
`AuthorizeSignalCall` is cluster-authorized. That is what Quorum mode means
once a cluster exists. The spirit head advance is just an authorization; the
special case dissolves (design-quality). The existing intercept for
spirit-context operations (`intercept_signal_authorization`) runs before the
mode branch, unchanged.

The bridge, using only existing machinery (all internal method calls on the
root actor — a node never dials its own socket):

1. **Ingress.** Create the authorization state (Signing) bound to a request
   slot, exactly as the coordinator does today; the streaming connection's
   observation session attaches to that slot.
2. **Window.** Derive the round window `[now, now + Δ]` where Δ is the
   owner-configured quorum window on `CriomeDaemonConfiguration` (new
   optional typed field; settled default: reasonable, covering the two
   rounds plus network round-trips — tens of seconds live, seconds in
   tests, nothing ceremonial; the catch-up case below chains two rounds,
   which the default must cover). When the request carries `expires_at`,
   the window is capped by it (the existing signer-side `window ⊆ lease`
   posture).
3. **Catch-up (the batching no-wedge rule, §3.4).** If the durable
   anti-equivocation ledger holds a SELF-co-signed row at
   `(contract, current head)` whose successor digest differs from the
   requested digest, first re-drive the recorded round for that successor —
   an identical re-proposal, idempotent by construction
   (`QuorumRoundIdentifier::for_phase(digest, phase)` re-opens the same
   durable round with a fresh window; peers' identical rows admit it). On
   its commit the contract head advances to the recorded successor; then
   proceed with step 4 from the new head. If no such row stands, skip.
4. **Originate.** Run the existing Request-round origination
   (`propose_quorum_authorization` internals) with contract = the
   operational quorum contract (resolved criome-side from the registry —
   never from the caller), object = the head-advance
   `AuthorizedObjectReference`, the derived window, phase = Request.
   Solicitation fans out across the contract's members through criome's
   router submission path (fire-and-forget; an unreachable peer leaves the
   round Gathering). The commit round is driven by the originator on
   round-1 majority, as built (`drive_commit_round`).
5. **Terminal Granted.** On round-2 Authorized: assemble the round Evidence
   (`assemble_evidence`), sign the grant (`SignAuthorizationGrant`), store
   the state as Granted **carrying both the grant and the assembled quorum
   Evidence** (the Evidence field is the §4 hand-off, §4.3), and
   `publish_authorization_update` — the held observation session pushes it
   to spirit. The grant binds the requested (batch-head) digest; an
   intermediate catch-up commit is internal to criome and never reaches
   spirit.
6. **Terminal Expired — the fail-closed leg.** Arm a one-shot timer at
   window close when the round opens (an event-scheduled push, not a poll).
   If the round is not Authorized when it fires: mark the authorization
   state Expired, publish the update (spirit's session receives it and holds
   the head), and leave the durable round as-is (the veto row and any cast
   votes stand — safety is never rolled back; §3.4 shows why retry still
   works). Criome owns the refusal because criome owns the window; spirit's
   session deadline (§3.2 rule 5) is only the backstop for a dead criome
   process, which cannot push anything.

Member nodes need NO new behavior: `solicit_quorum_vote` already validates
well-formedness (round-id ⇄ digest+phase binding, full-member-set moment,
own-clock window admission, non-double-sign veto, round-1 verification
before a Commit vote) and votes without any owner gate. That is the
psyche's "members auto-approve; nothing beyond well-formedness," already
built and audited. **This slice adds no approval predicate anywhere** — out
of scope by settled intent.

### 3.4 · The authorization unit: one head advance covering the whole unshipped suffix (batching is sound)

Direct answer to the psyche's question — "is the sema-engine vcs flawed? we
can't authorize several new records in one auth request?": **the VCS is not
flawed, and one authorization request soundly covers several records.**
Why, from verified source facts:

- The quorum machinery binds exactly one opaque digest per round: the round
  id derives from digest + phase alone
  (`QuorumRoundIdentifier::for_phase`, signal-criome `lib.rs:113`), the
  vote signs over that object digest plus the window/member proposition
  (`criome/src/language.rs:209-233`), `advance_head` sets the contract head
  to the one committed digest (`root.rs:1874`), and nothing in criome ever
  decodes what the digest stands for — one log entry or fifty is invisible
  to it.
- The log is hash-chained: each entry's digest folds in its predecessor's
  digest (`EntryDigest::from_entry_fields`, `versioning.rs:257`). One head
  digest therefore transitively fixes every entry beneath it. Authorizing
  the batch head H_n as successor from cluster head H_0 authorizes the
  ordered suffix E_1..E_n as a unit — the cluster co-signs one successor
  per `(contract, head)` exactly as built; ledger, rounds, and grant are
  unchanged.

The earlier draft's one-entry-per-round unit was NOT a VCS constraint; it
was a retry-idempotence choice against a wedge hazard, and the hazard
dissolves criome-side with zero new spirit state:

- The hazard: spirit's suffix head D is proposed from cluster head H_0; the
  round expires (peer down); the originator's durable self-co-signed row
  `(contract, H_0) → D` stands, correctly. Spirit then commits more
  entries; its head is now H_n ≠ D. Naively proposing `H_0 → H_n` would be
  refused by the node's OWN row — a permanent self-wedge.
- The dissolution: **the standing self-co-signed row IS the durable
  proposal pin.** The bridge's catch-up rule (§3.3 step 3) completes the
  recorded round first (identical re-proposal — idempotent, same round id,
  fresh window), advancing the cluster head to D, then opens
  `(contract, D) → H_n`. Both run under the one authorization request and
  window; the grant binds H_n. Because spirit's local log is append-only
  and chain-verified on rebuild, any earlier proposed head is necessarily
  an ancestor of the current head — the sequence is chain-consistent by
  construction.
- If the recorded round can never complete (a peer holds a CONFLICTING row
  — a genuine concurrent-origination fork), the request refuses exactly
  like any refused advance: head held, fork/merge design deferred (psyche:
  premature). Unchanged posture.
- The drain keeps at most one authorization outstanding per contract
  (§3.5), so at most one self-row ever stands ahead of the cluster head.

Consequences:

- The drain captures spirit's CURRENT head (the whole unshipped suffix per
  pass, from the durable outbox's `unshipped()`), not the oldest entry: one
  quorum round per burst of records instead of one per record.
- Criome's per-contract head chain still advances one committed digest at a
  time, in lockstep with the authorized batch heads; veto keying stays
  aligned forever.
- It is the natural unit for §4's batch push: one grant, one evidence, one
  apply message per target.
- A batch of one is the degenerate case; no special casing anywhere.

### 3.5 · Spirit-side drain: decoupled from the working reply

Today `handle_working_input` awaits `gate_and_ship_head` inline before
returning the working reply (`spirit/src/daemon.rs:171`). Acceptable at
local-socket latency; wrong when authorization is a cluster round over the
network (seconds, or a full window on refusal) — the recording caller must
not wait on propagation, and the daemon already ignores the decision there.

Design (actor-systems): a single supervised **propagation drain** — a
serialized background task or actor owned by the engine — receives a
"head advanced" mail after each durable working commit and runs the
authorize-then-ship sequence for the current unshipped suffix, one
outstanding authorization at a time. The working reply path never awaits
it. On Granted it ships the suffix up to the granted digest and
acknowledges the outbox cursor to it. Refusal/unreachable outcomes leave
the outbox intact; the next mail (or a retry mail the drain sends itself on
refusal — event-driven, not a poll loop; an exponential-backoff timer armed
per refusal is acceptable as an event, but prefer re-arming only on the
next commit plus an owner-visible held-head observation) re-attempts with
the then-current head; the catch-up rule (§3.3 step 3) makes that safe even
though the head moved. For deterministic tests the drain is drivable
directly (`Engine::drain_propagation_once()` or equivalent), with the
daemon wiring it to commits.

### 3.6 · Contact points (enum-vs-enum, single matrices)

The load-bearing branching is written as closed cross-products, not
scattered string predicates:

- Criome ingress: `AuthorizationMode` × operational-contract presence →
  behavior (§3.3 table) — one match in the root actor's
  `AuthorizeSignalCall` arm.
- Spirit session parse: `AuthorizationStatus` × grant-presence →
  `GateDecision` — one method on the session-state record
  (`Granted×Some(valid)` → Authorized; `Granted×None|mismatch` → fault;
  `Denied|Expired|Unavailable×_` → refusal; `Pending|Signing|Parked×_` →
  keep draining).
- Spirit gate mode (owned by primary-6kz1): Disabled | Enabled(socket) —
  a closed record, not a boolean.
- Router local delivery: `ComponentKind` × deployed-ingress presence →
  deliver | typed refusal (§1) — one enum-keyed table.

### 3.7 · Slice test/proof plan (testing skill: stateful tests as named outputs)

**Pure/unit (flake checks):**

- The session-parse matrix of §3.2 including every negative (stub criome
  socket writing crafted snapshots/updates) — in spirit.
- Criome bridge unit tests: Quorum+unfounded → Unavailable pushed;
  AutoApprove unchanged (repairs the failing
  `criome_gate_1of1::socket_only_...` test as the positive); window-expiry
  timer marks Expired and publishes; catch-up rule completes a standing
  recorded round before opening the requested one — in criome.
- Idempotent re-proposal after expiry: same digest re-opens the round,
  fresh window, completes — in criome (extends `two_round_commit.rs`).

**The loopcheck (stateful, named output, NOT a flake check — same posture
and pattern as `router-two-hosts-found-root-over-router-voice-test`):**

`spirit-cluster-authorizes-head-advance-over-router-test`, hosted in
`spirit/tests/` (spirit already dev-deps criome; the router dev-dep follows
the existing `offline-full-chain-e2e` precedent. Fallback host if the
router-dep lag bites: `router/tests/` beside the founding proof — decide at
implementation, spirit-hosted preferred). Harness = the founding proof's
node shape (two node directories, two real routers on loopback TCP with
seeded host routes, two real criome daemons with the router submission path
armed), extended with a real spirit engine on node A gated against criome
A, plus criome daemon configuration setting a short quorum window
(seconds).

Sequence and witnessed claims, exercising batch, refusal, and catch-up:

1. Found the 2-of-2 root over the router (reuse the founding drive:
   initiate on A, agent-performed explicit accept on both meta sockets,
   `Founded` with the same anchor on both).
2. **Batched authorized advance:** record TWO entries on spirit A → drive
   the drain → ONE round authorizes the batch head → assert the gate
   decision is Authorized with the grant digest equal to the second
   entry's digest, both entries shipped (cursor at the head), and criome B
   holds the committed round for that one object (its ledger witnessed one
   round, not two).
3. **Refused advance (quorum can't complete):** stop node B's router
   listener, record a third entry on A → drive the drain → the round stays
   Gathering, the window expires, Expired is pushed → assert the decision
   is a refusal, nothing shipped, spirit A's LOCAL head still advanced
   (local commit stands), and the outbox still holds the suffix.
4. **Catch-up retry after refusal:** record a FOURTH entry on A (the head
   moves past the refused proposal), restore B, drive the drain → criome A
   first completes the recorded round for the refused batch head, then
   authorizes the new head; the grant binds the fourth entry's digest; the
   whole suffix ships. (Proves §3.4's no-wedge property end to end.)

Falsification: if spirit bypassed criome, step 3 would ship; if the parse
trusted status without the grant, a crafted Granted-without-grant criome
would ship; if the catch-up rule were missing, step 4 would self-refuse
with `QuorumConflict`.

## 4 · Slice: propagation with receiving-side acceptance (immediately after §3)

### 4.1 · Shape (b), settled

The psyche reviewed the three candidate shapes and settled on (b): **the
authorization approval carries the target host IDs; the state-bearing
spirit pushes.** Recorded reasons, for future readers: (a) — remote criome
notifies its spirit, which fetches — adds a round trip, a new
criome→spirit channel on every node, and misses offline members (its value
is as a future repair/bootstrap pull, §4.6); (c) — spirit keeps its own
mirror list and delivery tracking — duplicates criome's membership and the
router's reachability/queueing inside spirit and erodes the
quorum-ignorance boundary. (b) is pure push with zero new inter-component
channels and zero duplicated ownership: criome owns membership (the
propagation targets are the operational quorum contract's members —
criome-owned, settled), the router owns reachability and the durable delta
queue, spirit pushes exactly where the approval says.

### 4.2 · Design

Flow for one authorized batch (suffix head H) on node A, cluster {A, B, ...}:

1. **Targets on the approval.** When the criome bridge stores the Granted
   state (§3.3 step 5), it also resolves the propagation targets: the
   operational quorum contract's members minus the requesting host, each as
   its **Criome host ID** (the member's master public key — resolved
   criome-side from the admitted contract; identity→key binding already
   exists). These ride the Granted push to spirit as opaque routing data
   (wire shape §4.3).
2. **Spirit pushes one batch per target.** The drain (§3.5) frames the
   authorized suffix as ONE signal-spirit `ApplyAuthorizedRecords` request
   per target — carrying the ordered versioned log entries, and the
   **carried authorization**: its unique identifier (the operational
   contract digest + the authorized batch-head object reference) plus the
   assembled quorum Evidence from the approval. Destination = (target host
   ID, `ComponentKind::Spirit`) — the target host's one spirit, preset and
   deterministic (§1); no actor-name projection, no routing table, no
   lookup. Submitted to the LOCAL router via `SubmitRoutedObjects`; the
   router sees an opaque payload addressed to a (host, component) pair,
   resolves host → route → durable backlog exactly as built.
3. **Peer acceptance — the loop-tying check (settled intent).** Propagated
   state carries the unique identifier of the authorization that allowed
   it, and the receiving spirit MUST verify with its local criome that this
   authorization is real and locally accepted before applying — so no
   spirit can unilaterally skip authorization. Spirit B's
   `ApplyAuthorizedRecords` ingress (reactivating and batching the parked
   `ApplyAuthorizedRecord` seam, `nexus.rs:1305`) hands the carried
   identifier + Evidence to ITS OWN criome (the `evaluate_carried` /
   `EvaluateAuthorization` seam, extended to **accept-and-record**
   semantics). Criome B answers Authorized exactly when:
   - the identified round is already committed in its durable ledger (it
     voted — the normal case), or
   - the carried Evidence BLS-verifies against ITS admitted operational
     quorum contract (signatures + threshold), in which case criome B
     records the co-signed successor row and advances its contract head —
     the offline-at-quorum member catches up and the authorization becomes
     locally accepted; member head chains stay aligned cluster-wide.
   Anything else — unknown contract, failed verification, no local criome
   reachable — is a typed `ApplyRefusal`; nothing written. Cryptography is
   criome's domain at both ends (settled); spirit never verifies BLS.
4. **Peer applies, chain-checked.** Only on criome B's Authorized does
   spirit B apply, atomically, after checking on its own store: the batch's
   first entry chains onto B's current applied head, each entry chains onto
   the previous, and the last entry re-hashes to the authorized digest.
   These are sema-engine digest-integrity checks on spirit's own data
   structure, not signature cryptography. Any break — including a gap
   (first entry not chaining onto the applied head) — is a typed refusal;
   gap repair is future (§4.6).
5. **Offline targets — the delta, no polling.** If a target is unreachable,
   the LOCAL router's durable outbound backlog holds the forward
   (crash-durable) and drains on the peer-session-established push — the
   built nbmq.5 behavior. Spirit tracks nothing; there is no retry loop and
   no poll anywhere in spirit. Pushes to one destination are
   backlog-ordered; the peer applies in log order and refuses a gap.
6. **Both directions.** The design is symmetric by construction: B's own
   head advances run the same §3 authorization and the same push back
   toward A. Nothing additional to build — only the convergence proof
   (§4.5).

The legacy direct mirror path (`MirrorShipper` → `mirror::ComponentShipper`
→ `MirrorTarget::Address` socket) is superseded by the router push and
retires with this slice (a bead; the mirror-noun daemon is already dropped
per nbmq). Checkpoint publication / fresh-node restore is out of slice
scope (§4.6).

### 4.3 · Wire/contract changes (component-architecture: contracts first)

This slice carries the §1 addressing groundwork — it adds the first new
routed path (spirit→spirit), and criome's own quorum traffic migrates onto
the same model in the same move:

- **signal-standard**: owns the single `ComponentKind`,
  `AuthorizedObjectKind`, `AuthorizedObjectReference`, `ObjectDigest`
  (typed bytes). Other signal-* crates re-export; the signal-criome and
  signal-persona twins are deleted (follow-up beads for signal-orchestrate
  and meta-signal-mentci).
- **signal-router**: the forwarded envelope's `SourceActor` /
  `DestinationActor` (`ActorIdentifier(String)`) become
  (CriomeHostId, ComponentKind) pairs; `RoutedContractObject`'s
  `ContractName(String)` / `ContractOperation(String)` dissolve into
  destination-component dispatch with opaque payload octets (§1);
  `CriomeHostId` becomes typed key bytes with `Hash`. `RegisterActor` /
  actor-home registration and the `homes` map dissolve. No criome or
  spirit concept enters the router's vocabulary — host + component +
  opaque payload only.
- **router**: `authorized_object_projection.rs` deleted; local delivery
  table ComponentKind → ingress; route resolution drops the actor-home hop.
- **signal-criome** (versioned, clean-genesis line): the authorization
  request carries the typed `AuthorizedObjectReference` (string trio
  retired, §3.1). The Granted-side state carries (i) the assembled quorum
  `Evidence` for the authorized object and (ii) the propagation targets as
  a vector of Criome host IDs — positional NOTA records, no flags. Fork
  for the implementer, called here: targets INSIDE the BLS-signed
  `AuthorizationGrantStatement` bytes (binds routing advice to the
  signature; costs a statement change) versus beside the grant on the state
  record (routing advice unsigned; the peer acceptance check never trusts
  it anyway — misrouting cannot forge an apply, only misdeliver to a node
  that re-judges). Default: beside the grant — the authorization substance
  stays signed, routing advice stays advice. One canonical asserted
  round-trip per new type (contract-repo).
- **signal-spirit**: `ApplyAuthorizedRecords` — the batch form of the
  existing `ApplyAuthorizedRecord` — carrying ordered entries + the
  authorization identifier (contract digest + authorized object reference)
  + Evidence. Extend from the nbmq.2 shape; a batch of one replaces the
  singular variant.

### 4.4 · What spirit knows at the end (boundary audit)

Spirit's total vocabulary after these slices: "my local criome socket",
"authorize this head digest" (typed reference in, terminal verdict out),
"push this batch to these opaque host IDs via my router", "ask my criome
whether a carried authorization is real and locally accepted before
applying", and its own store's chain integrity. No quorum, no threshold,
no membership, no reachability, no window. The psyche's boundary holds.

### 4.5 · Slice test/proof plan

**Pure/unit (flake checks):**

- Contract round-trips for the new signal-standard / signal-criome /
  signal-spirit / signal-router types; router local-delivery table
  (ComponentKind × presence).
- Criome: Granted state carries evidence + members-minus-self targets
  (founded fixture); accept-and-record: carried-evidence verification
  records the row and advances the head (the offline-member path);
  already-committed round answers Authorized without re-recording.
- Spirit apply ingress negatives (stub criome): tampered evidence →
  refused; unknown authorization identifier → refused; digest/entry
  mismatch → refused; interior chain break → refused; gap (batch not
  chaining onto applied head) → refused; no local criome reachable →
  refused (fail-closed, never applied-untrusted).

**Loopchecks (stateful, named outputs, same pattern as §3.7's):**

1. `spirit-propagates-authorized-head-over-router-test` — extend the §3.7
   harness with a spirit engine on node B: record two entries on A →
   cluster authorizes the batch → A pushes ONE batch over router A →
   router B → B's ingress asks criome B (voter path: round already in its
   ledger) → B applies both entries atomically → assert B's applied head
   equals A's head (`ObserveHead` on both). Falsification: a harness that
   skips the quorum, tampers one signature byte, or forges the
   authorization identifier must yield `apply_refused` and no head
   movement on B.
2. `spirit-delivers-delta-when-peer-returns-test` — the offline delta:
   authorize with both up; take down node B's router listener BEFORE the
   push; assert the forward parks in A's durable outbound backlog and B's
   head is unchanged; restart B's listener / re-establish the peer
   session; assert the backlog drains on the session event (no poll) and B
   converges to A's head. Restart A's router mid-test to prove the backlog
   is crash-durable (existing nbmq.5 property, now witnessed end-to-end to
   a spirit apply).
3. Both-directions convergence (nbmq.10): record distinct entries on A then
   on B (sequentially, not concurrently — concurrent forks are out of
   scope, §3.4) and assert both heads converge on both nodes.

The offline-at-quorum member acceptance (verify-then-record) is covered at
unit level criome-side; a 3-node loopcheck variant (A+B authorize while C
is down; C returns, receives the push, accepts via carried evidence) is
named as an optional extension, not required for the slice.

The live two-VM run (mirror-alpha/mirror-beta, lojix-deployed) is the
operating-system-implementer follow-up after the loopchecks are green —
the nbmq.12 / 79z1.15 endgame, not part of these slices.

### 4.6 · Explicitly out of scope (named so nobody re-derives them)

- Approval predicates: lineage checks, fork rules, thresholds beyond the
  admitted contract's — psyche says premature.
- Concurrent-origination fork resolution (§3.4).
- Gap repair / history fetch / fresh-node bootstrap from peers — the
  (a)-shaped pull as a REPAIR path, plus checkpoint restore. Future slice.
- Spirit pinning its criome's public key for local grant verification
  (§3.2 hardening seam).
- Cluster membership change / rotation (79z1 phase-2; the reissue seam is
  §5).

## 5 · Slice: the root issues the operational cluster quorum sub-contract

Settled intent: the root is the root; there is only one. The operational
cluster quorum contract is a sub-contract of it — issued and anchored by
the root, with its own distinct contract identity — and after the early
prototype phase the root itself is not the contract operational rounds run
over. There is no separation event: right now the root keys and the first
sub-contract keys are identical (same hosts, same criome installation, no
key export), and the root simply continues, unchanged. Air-gapping and
guarded-root operations are explicitly deferred design, not part of this
slice map.

Design:

1. **Issuance.** A cluster quorum sub-contract document — member set (the
   same hosts' Criome host IDs, the same key material as the root's
   members today), threshold, and a reference to the root anchor — is
   authorized over the ROOT contract as an object of kind `Contract`
   (`AuthorizedObjectKind::Contract` exists), through the ordinary
   two-round commit: members auto-approve, nothing beyond well-formedness.
   Manual approval remains unique to founding.
2. **Admission carries the root's authorization.** Each member admits the
   sub-contract into its `ContractStore` together with the root-round
   Evidence. The verification chain every node can walk: pinned root anchor
   (from founding) → root-authorized sub-contract → operational rounds
   under the sub-contract. The §4.2 acceptance check verifies carried
   evidence against the ADMITTED OPERATIONAL contract.
3. **Operational resolution.** The bridge's contract resolution (§3.3 step
   4, "resolved criome-side from the registry") resolves the admitted
   sub-contract as the operational quorum contract once it exists; before
   this slice lands, staging over the founded root contract is the
   explicit prototype posture (§3.3 table). The per-contract ledger and
   head chain are already keyed by contract; the sub-contract starts at
   its own genesis head and the first operational round proposes spirit's
   current head from there — no row migration, no cutover event. The root
   continues, unchanged, as the root.
4. **Membership change / rotation** = the root issues a replacement
   sub-contract the same way — the 79z1 phase-2 seam, not designed here.

Proof for the slice: a loopcheck extending §3.7's — found the root, issue
the sub-contract through the root-quorum round, assert head advances
authorize over the sub-contract (both criome ledgers key the new
contract).

## 6 · Tracker implications (NOTES ONLY — no tracker mutation this pass)

- **primary-nbmq** (persistent both-directions quorum-gated spirit mirror):
  §3 supplies the missing "spirit's ask reaches criome's gather-and-commit"
  bridge criome-side (nbmq.4's driver gains its production ingress); §4
  reactivates the nbmq.2 apply ingress in batch form and is the substance
  of nbmq.10 (both directions + convergence), advancing toward nbmq.12
  (live two-VM proof). nbmq.5's durable outbox + push redial becomes
  load-bearing for the offline delta — its per-destination ordering and its
  redial trigger are verification points (§7).
- **primary-79z1** (operational criome): §3.7's loopcheck is exactly the
  in-process precursor of the open `.15` live proof's second half
  ("authorize a native head-advance op through the two-round commit under
  the clock gate"); the live run should reuse these named outputs' drive
  sequence. §5's root-issued sub-contract replacement is the phase-2
  membership seam.
- **primary-6kz1** (concurrent lane): owns the 1-of-1 retirement and the
  spirit-side disable option this design targets; §3's spirit-side work
  must land after (or coordinated with) it — the session-parse fix touches
  the same `criome_gate.rs`.
- Suggested new beads at pickup (not filed): §1 contract consolidation
  (signal-standard single vocabulary; twins deletion incl.
  `authorized_object_projection.rs`; signal-orchestrate /
  meta-signal-mentci follow-ups); §1 router (host, component) destination
  + `CriomeHostId` retype; §3 criome bridge + catch-up + expiry push; §3
  spirit typed ask + session parse + drain decoupling; §3 loopcheck; §4
  signal-criome grant surface (evidence + targets); §4
  `ApplyAuthorizedRecords` + acceptance check + push; §4 loopchecks; §5
  sub-contract issuance + operational resolution;
  MirrorShipper/MirrorTarget retirement.

## 7 · Worker verification points (facts to confirm at pickup, cheap)

1. Spirit tree state — primary-6kz1 was landing DURING the first pass;
   re-read `criome_gate.rs` / `daemon.rs` / whether the disable option
   landed. Note: the string literals the retiring ask uses differ between
   `spirit` main (`"signal-spirit"` / `"spirit-operation"`,
   `criome_gate.rs:317-325`) and the `spirit-trueschema` variant
   (`"spirit-local-head"` etc.) — confirm which tree is authoritative
   before retiring the trio.
2. Outbox `acknowledge` forks (`MirrorHeadUnknown`, `OutboxEntryMismatch`,
   `MirrorHeadForked`, `outbox.rs:191`) — confirm acknowledge-to-batch-head
   composes with them (the `unshipped()` ordered-suffix and same-transaction
   outbox row facts are verified).
3. Router backlog: per-destination ordering guarantee, and what triggers
   redial to a returned peer besides an inbound session.
4. `ApplyAuthorizedRecord` payload as nbmq.2 built it — the fields to
   extend into the batch shape (§4.3).
5. The founded root contract is admitted into each member's `ContractStore`
   post-founding (the bridge resolves members from it); the founding
   proof's registry-seeding suggests yes — confirm.
6. Criome client helper `transport.rs:355` (`states().first()`) — harden to
   slot-filtering alongside the spirit parse (§3.2 rule 1).
7. `originated_request_rounds` is in-memory; confirm a criome restart
   mid-round recovers originator-driving via the durable round on
   re-proposal (§3.4 catch-up path).
8. When exactly the originator's self-co-signed row is recorded
   (propose-time vs commit-time): the catch-up rule (§3.3 step 3) is
   conditional and safe either way — no standing row means propose directly
   — but the loopcheck step 4 assumes propose-time recording; confirm at
   `record_co_sign` call sites.
9. Whether any further `ComponentKind` twins exist beyond signal-standard /
   signal-criome / signal-persona / signal-orchestrate / meta-signal-mentci
   before filing the consolidation bead.

## 8 · Open questions for the psyche

None at this revision. The former root-key question dissolved: the root
continues unchanged, root and first sub-contract keys are identical for
now (same hosts, same criome installation, no key export), and air-gapping
is deferred design.
