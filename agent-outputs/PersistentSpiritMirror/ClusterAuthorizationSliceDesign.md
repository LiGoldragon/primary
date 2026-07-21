# Cluster Authorization Slice Design — the criome cluster authorizes acceptance of spirit's state

Retired vocabulary (psyche ruling 2026-07-21): "mouth" -> textual interface; "organs" -> the two trees (nametree, structuretree); "spine" -> core invariant / core pathway; "door" -> entry point; "currency" -> value type. Historical text below is unreworded; read it through this table.

Design for the vertical slices. Design only; nothing was edited or committed
in any code repo. This is the pickup point for implementation workers.

Revised 2026-07-06 after psyche review (enum addressing §1, batched
authorization, receiving-side acceptance §4.2, the root-issued sub-contract
§5).

**Amended 2026-07-07 after a hard psyche correction.** The psyche, verbatim:

> "The whole point of the authorization is to gate the operation from being
> accepted, and by that I mean being accepted everywhere, including locally.
> The quorum gates the acceptance everywhere. The criome authorizes or does
> not authorize, and in which case it does not authorize, it's not
> authorized."

The previous revision — and the slice-1 implementation that landed from it
(spirit 0.23.1, criome 0.7.0, both on main, audited sound) — let a working
operation commit to spirit's local log unconditionally and gated only the
propagation of the committed head. That premise is overridden. This
amendment reworks every section that rested on accept-locally-then-authorize
and maps the implementation delta from the current mains (§9).

**What this amendment changes**, for readers of the previous revision:

- §0: the acceptance semantic is corrected — refusal means the operation is
  refused to the caller and nothing is recorded anywhere, including locally.
- §3.3: the criome-side catch-up rule (complete a standing recorded round,
  then chain the new head) dies; a dead-round supersession rule replaces it.
- §3.4: the authorization unit changes from "the whole unshipped suffix per
  drain pass" to "one working operation's entry group per round"; batching
  survives where it still earns its keep, named explicitly.
- §3.5: the post-commit propagation drain as the authorization seat dies;
  the gate moves onto the intake path (stage, authorize, materialize).
- §3.6 (new): what shipping means when all accepted state is by definition
  authorized.
- §3.8 (new): the crash-window ledger.
- §3.9: the loopcheck's refused-window outcome becomes "operation refused,
  head did NOT advance."
- §9 (new): the file-level implementation delta from spirit 0.23.1 /
  criome 0.7.0.

Unchanged and still settled: the addressing model (§1), batching soundness
(§3.4's hash-chain argument), shape (b) propagation with receiving-side
acceptance (§4), the root-issued sub-contract staging (§5), no strings for
fixed sets, and no name containing "voice".

Ground truth re-verified against source on 2026-07-07:

- `spirit` main `1698cba1` (0.23.1): the drain-shaped slice-1 seam is live —
  `handle_working_input` commits then mails the drain
  (`daemon.rs:146-164`), the drain authorizes the unshipped-suffix head and
  ships on Granted (`propagation.rs:67-79`), the session-parse binding
  matrix (`criome_gate.rs:280-347`), the emitted engine actor serializes
  every working request through one mailbox
  (`src/schema/daemon.rs:488-508,569`).
- `criome` main `a486154a` (0.7.0): the originator's anti-equivocation row
  is recorded at propose time, before its own vote (`root.rs:2100,2103`);
  a request for the current contract head re-grants immediately with no new
  round (`re_grant_standing_head`, `root.rs:1347-1351,1525-1530`); a
  still-`Gathering` durable round re-opens idempotently on an identical
  re-proposal, an `Authorized` one does not re-open (`root.rs:2067-2083`);
  the differing-successor case runs the catch-up stage
  (`HeadAuthorizationStage::CatchingUp`, `root.rs:1375-1382,1685-1728`) —
  there is NO window-expiry supersession today; member-side window
  admission is a closed-interval own-clock test with no skew margin
  (`root.rs:2169-2174`, `signer.rs:453-454`, `master_key.rs:314-322`);
  window expiry pushes terminal `Expired` and leaves the round and row
  standing (`root.rs:3465-3512`).
- `sema-engine` main (0.6.3): the entry digest folds a domain tag, store
  name, schema hash, `commit_sequence`, `snapshot`,
  `previous_entry_digest`, and the ordered operations — no wall clock
  (`versioning.rs:257-285,386-399`); `commit_sequence` / `snapshot` /
  `previous_entry_digest` are read from the current head at append
  (`engine.rs:798-799,2035`), so a pre-built entry's digest is
  deterministic exactly when no other entry commits in between; entry +
  outbox + counters commit as one atomic redb transaction
  (`engine.rs:2079-2095`, `outbox.rs:171`); no prepared/staged append seam
  exists today.
- `spirit` write path: no single append choke point — the nexus dispatch
  band (`nexus.rs:1222-1313`) splits reads (`command_sema_read`) from
  sema-writes and effect commands, and the store methods each call
  `self.database.assert/mutate/retract` directly (`store/mod.rs:742,744`,
  retire `1102`, supersede `1262`, resolve `1243`, and the change paths).
  One working input may write SEVERAL versioned-log entries (for example
  `record_with_implied_referents`, `nexus.rs:618-684`).
- `signal-spirit`: a typed authorization-refusal output already exists —
  `Output::ApplyRefused(ApplyRefusal)` with `ApplyRefusalReason`
  (`schema/signal.rs:792-797,2128`) — currently emitted only by the parked
  peer-apply ingress (`nexus.rs:1310-1312`).
- `router` / founding proof / durable outbound backlog: as verified in the
  previous revision, unchanged.

## 0 · Settled constraints (psyche intent — not redesigned here)

- **The quorum gates acceptance everywhere, including locally** (the
  2026-07-07 correction, verbatim above). When criome authorization is
  Enabled, a head-advancing working input is accepted ONLY after the
  cluster grant arrives. Refused, expired, unavailable, or unreachable —
  in every one of these cases the operation is refused to the caller and
  nothing is recorded anywhere: the head does not advance, not even
  locally. Fail-closed. Reads are unaffected.
- **Disabled mode is unchanged**: spirit fully local, heads advance freely,
  nothing propagates, the whole seam dormant. This stays the operative
  default until the owner enables the gate.
- Spirit knows nothing about quorums. Spirit asks its local criome host to
  authorize each head advance; criome owns everything behind that socket.
- Criome runs the two-round commit across the founded cluster for every
  head advance. Members auto-approve; nothing is checked beyond
  well-formedness. Only the founding contract is manually approved.
  Approval predicates (lineage checks, fork rules, thresholds) are
  explicitly OUT of scope.
- Everything over the network goes through the router; the router only
  routes. No criome concepts in router-facing design or names.
- **No strings for fixed sets.** Every identifier of a fixed set is a
  closed enum in the contract layer, defined once (§1).
- **The Criome host ID is the only network identifier.** A destination is
  the pair (Criome host ID, component) (§1).
- **The root is the root; there is only one.** The operational cluster
  quorum contract is a root-issued sub-contract (§5); the slices prototype
  on the root directly, as explicit staging.
- **Quorum window**: an owner-configurable duration with a reasonable
  default covering the two rounds plus network round-trips — tens of
  seconds live, seconds in tests, nothing ceremonial. Under this
  amendment the window is also the bound on how long a recording caller
  can wait before a definite verdict (§3.5).
- **Gate enabled + local criome unfounded = refuse loudly** (terminal
  `Unavailable`; under this amendment that refusal reaches the caller and
  the operation is not recorded).
- **Trust boundary confirmed**: cryptography is criome's domain at both
  ends of every network boundary; spirit never verifies BLS locally
  (§3.2).
- Mirror is a verb. No mirror-noun component.
- The spirit-side mode is a closed option: criome authorization Disabled
  (default) or Enabled(socket). There is no 1-of-1 mode; that retirement
  landed (primary-6kz1).
- The name "voice" was renamed away; this design says "criome's router
  submission path".

### 0.1 · The corrected semantic, in plain words

Terms used throughout: spirit's durable history is an append-only log;
each appended entry has a **digest** (a fingerprint of its content that
also folds in its predecessor's fingerprint, so one digest pins the whole
history beneath it); the newest entry's digest is the **head**. A **head
advance** is any working operation that would append to the log — a new
record, a supersede, a retire, and so on. The **quorum** is the founded
cluster of criome hosts; a **grant** is the cluster's signed yes for one
proposed head digest, produced by the existing two-round commit.

With criome authorization Enabled, the order of events for every head
advance is: spirit builds the would-be entries and computes the head
digest they would produce, WITHOUT committing anything; it asks its local
criome to authorize that digest; criome runs the cluster round; only when
the grant arrives does spirit append the entries and reply to the caller.
**The grant is the acceptance event.** Before the grant, the operation
exists nowhere — not in spirit's log, not on any peer. If the verdict is
anything other than a grant — denied, window expired, no founded contract,
criome unreachable — the caller receives a typed refusal, the prepared
entries are discarded, and no trace of the operation remains in any
durable state a reader can observe. There is no propagation question for
refused operations, because there is nothing to propagate: everything
that exists in an Enabled spirit's log is, by construction, cluster
authorized.

## 1 · The addressing model — host ID + component enum, no strings

Unchanged by this amendment. Cross-cutting; every slice below speaks it.

**Destination = (CriomeHostId, ComponentKind).** The Criome host ID (the
host criome's master public key) is the only network identifier. Each host
runs exactly one instance of each component, so the pair is a complete
address: no actor names, no lookup service, no registration of actor
homes. The router's durable route store is already keyed by
`CriomeHostId`; the `homes` map and the `ActorIdentifier(String)` newtype
dissolve. Local delivery is one closed table: ComponentKind → the local
component ingress; a component not deployed on the host is a typed
refusal, fail-closed.

**One ComponentKind, defined once.** signal-standard owns the single
`ComponentKind`, `AuthorizedObjectKind`, `AuthorizedObjectReference`, and
`ObjectDigest`; every other signal-* crate re-exports rather than twins;
the router's `authorized_object_projection.rs` and all variant-by-variant
`From` mappings are deleted. The variant set is closed and recompiles when
a component is born or dies. Settled intent, not style.

**Contract dispatch by component, not by string.** `ContractName(String)`
and `ContractOperation(String)` die; one component speaks one contract, so
the destination component enum IS the contract selector; the forwarded
envelope carries source and destination as (host ID, component) pairs plus
opaque payload octets, decoded by the receiver against its own contract.

**The authorization ask is the typed reference.** The request is the typed
`AuthorizedObjectReference { component, digest, kind }` plus requester
identity and optional expiry; the string trio (`ContractName`,
`ContractOperationHead`, `AuthorizationScope`) dissolves. A spirit head
advance is exactly `{ component: Spirit, kind: Head, digest }` — already
implemented this way in spirit 0.23.1 (`criome_gate.rs:95-103`).

**Identifier value types.** `CriomeHostId` becomes the typed master-key
bytes it names; `ObjectDigest(String)` becomes typed digest bytes.

## 2 · What already exists (the amendment reuses, moves, or retires)

| Piece | Where | Status under this amendment |
|---|---|---|
| Two-round commit driver (Request then verified Commit, majority-of-total, witness-clock gate on both, durable rounds) | `criome/src/actors/root.rs` | Built, audited — reused unchanged |
| Member auto-approval (well-formedness only) | `root.rs` `solicit_quorum_vote` | Built — reused; gains only the dead-round arm of the same admission check (§3.3) |
| Anti-equivocation row, durable-first at propose time, idempotent identical re-proposal | `root.rs:2100,2665-2701` | Built — admission rule AMENDED (§3.3: dead-round supersession) |
| Immediate re-grant of the standing committed head, no new round | `root.rs:1347-1351` | Built — becomes the ship-time grant fetch (§3.6) |
| Catch-up stage (complete a standing recorded round, then chain) | `root.rs:1375-1382,1685-1728` | Built — DIES (§3.3): completing a refused round would materialize a refused operation |
| Quorum-mode bridge: ingress state, window derivation, origination, terminal Granted with evidence, window-expiry push | `root.rs:1328-1786,3465-3512` | Built — reused; only the differing-successor arm changes |
| Streaming authorization observation session (submit, snapshot, pushed updates to terminal) | criome daemon + `transport.rs:334-401` | Built — reused unchanged; now consumed on spirit's intake path |
| Spirit session-parse binding matrix (slot, digest, grant presence, typed refusals) | `spirit/src/criome_gate.rs:280-347` | Built — reused unchanged; the module's placement comments change |
| Spirit propagation drain (post-commit mail, authorize-then-ship, coalescing) | `spirit/src/propagation.rs`, `engine.rs:679-734`, `daemon.rs:146-164` | Built — REWORKED: no longer the acceptance gate; becomes the ship drain + residue reconciler (§3.6) |
| Hash-chained log, atomic entry+outbox transaction, `unshipped()` ordered suffix, cursor acknowledge | `sema-engine` `versioning.rs`, `engine.rs:2079-2095`, `outbox.rs` | Built — reused; gains the durable staging seam (§3.5) |
| Typed refusal output shape | signal-spirit `ApplyRefused` / `ApplyRefusalReason` | Built — pattern for the new intake refusal (§3.5); the peer-apply variant itself stays parked until §4 |
| Spirit apply ingress for a pushed authorized record | signal-spirit `ApplyAuthorizedRecord`, `nexus.rs:1310-1312` (fail-closed) | Parked — §4 reactivates and batches it |
| Router durable outbound backlog + drain on peer-session establishment | `router` | Built — reused unchanged (§4) |

Slice map: §3 = cluster authorization gating acceptance of a head advance
(prototyped over the root contract); §4 = authorized propagation with
receiving-side acceptance; §5 = the root issues the operational
sub-contract. §9 = the delta from the already-landed drain-shaped slice 1.

## 3 · Slice: cluster authorization gates acceptance of a spirit head advance

One sentence: with the gate Enabled, spirit STAGES each head-advancing
working operation — builds its entries and their would-be head digest
without committing — asks its local criome over the working socket to
authorize that digest, and only on the pushed cluster grant appends the
entries and replies accepted; every other terminal outcome refuses the
operation to the caller and discards the staged entries, so nothing is
recorded anywhere, fail-closed.

### 3.1 · The ask: spirit → local criome

Unchanged in shape from the implemented slice; changed in WHAT the digest
denotes and WHEN it is asked.

- Spirit submits `CriomeRequest::AuthorizeSignalCall` carrying the typed
  `AuthorizedObjectReference { component: Spirit, kind: Head, digest }` —
  where the digest is now the PROSPECTIVE head: the digest the staged
  entry group would produce if appended (§3.5). No contract-name,
  operation, or scope strings; no window: policy is criome's.
- One working operation may write several log entries (implied referents
  ride along with a record). The whole group stages as a unit and the ask
  binds the group's final digest; the hash chain fixes the interior
  entries (§3.4). One operation, one round, regardless of entry count.
- Spirit consumes the reply as an observation session (§3.2), on the
  intake path, before anything commits.

### 3.2 · The session parse (unchanged rules, relocated seat)

The security-sensitive parse is implemented and audited in spirit 0.23.1
(`HeadSessionBinding`, `criome_gate.rs:280-347`) and is reused verbatim;
only its seat moves from the post-commit drain to the intake path. Every
rule violation is a `CriomeGateError` (machinery fault) and every fault
refuses the operation — there is no default-open branch:

1. **Slot binding.** Only state records whose `request_slot` equals the
   session token are considered; foreign records are ignored.
2. **Digest binding.** `state.request_digest` must equal the submitted
   prospective head digest.
3. **Terminal Granted requires the grant**, and the grant must bind the
   slot and the submitted digest. Status alone is never proof.
4. **Terminal non-Granted refuses.** `Denied` / `Expired` / `Unavailable`
   map to typed refusals — under this amendment they refuse the OPERATION
   to the caller (§3.5), not merely a ship.
5. **Non-terminal waits.** `Pending` / `Signing` / `Parked` keep the
   session draining pushed updates on a `spawn_blocking` worker with a
   read deadline slightly beyond the authorization window; deadline
   expiry is treated as Unreachable → operation refused.

BLS verification of the grant signature by spirit: deliberately NO, as
settled — the socket is the trust boundary, spirit stays quorum-ignorant,
and the full cryptographic re-judgment happens at the receiving node's
criome (§4.2). The negative tests locking this posture exist and carry
over; their asserted consequence changes from "head held, ship withheld"
to "operation refused, nothing appended" (§3.9).

### 3.3 · Criome-side: the Quorum-mode bridge, amended

The mode table is unchanged:

| Mode | Operational quorum contract present | Behavior |
|---|---|---|
| `AutoApprove` | any | Immediate self-signed grant (dev/bootstrap; the loopcheck's degenerate case) |
| `ClientApproval` | any | Park for owner approval (the agent-guardian flow) |
| `Quorum` | yes | Originate the two-round commit over the operational quorum contract |
| `Quorum` | no | Terminal `Unavailable` pushed immediately — fail-closed, refuse loudly |

The bridge steps are as implemented (ingress state bound to a request
slot; window `[now, now + Δ]` from the owner-configured quorum window;
origination across the contract's members through criome's router
submission path; terminal Granted stores the grant plus assembled
Evidence and publishes to the held session; a one-shot expiry timer
pushes terminal `Expired` at window close) — with ONE amendment:

**The catch-up rule dies; dead-round supersession replaces it.**

Today (criome 0.7.0), when a request proposes a successor for a contract
head that already has a standing recorded row with a DIFFERENT successor
digest, the bridge first re-drives the recorded round to completion and
then chains the new proposal from the advanced head
(`HeadAuthorizationStage::CatchingUp`, `root.rs:1375-1382,1685-1728`).
That rule existed because, under accept-locally-then-authorize, the
recorded round's entry was already durable in spirit's log and would
eventually ship — completing it was always correct.

Under the everywhere-gate that premise is gone: a round that expired
carried an operation that was REFUSED to its caller; the staged entries
were discarded; the digest names an entry group that will never exist.
Completing that round later would advance the cluster head to a digest
nobody holds content for — materializing a refused operation and
poisoning the contract. So:

- **Supersession rule.** A recorded row `(contract, head H) → D` whose
  round is still `Gathering` (never `Authorized`) and whose window has
  closed on the judging member's own clock is DEAD, and a new proposal
  `(contract, H) → D'` with `D' ≠ D` is admitted, durably replacing the
  row before any signature is produced (the same durable-first discipline
  as today, `root.rs:2665-2701`). An `Authorized` round is never dead:
  once committed, `D` is the only successor of `H`, forever.
- **Identical re-proposal is unchanged.** `D' = D` re-opens the standing
  `Gathering` round with a fresh window exactly as built
  (`root.rs:2067-2083`) — this is the crash-recovery path (§3.8), not the
  refusal path.
- **Live rows still veto.** A conflicting proposal while the recorded
  round's window is OPEN is refused exactly as today
  (`CoSignAdmission::RefusedConflict`, `root.rs:199-222,2627-2646`) —
  that is the genuine concurrent-origination fork, out of scope as
  settled.

**Why supersession is safe** (stated so the decision is auditable): a
round can only commit when its ORIGINATOR assembles the Request-round
majority and drives the Commit round — members vote only when solicited
and never spontaneously commit. The originator proposes a different
successor only after its own window expired and it pushed terminal
`Expired` to its asker; from that moment it will never drive the dead
round's commit. No driver, no commit, anywhere — so admitting a different
successor cannot equivocate against a committed round. Clock skew between
members affects only LIVENESS, not safety: a member whose clock still
holds the dead round's window open refuses the superseding vote
(fail-closed), the new round expires, the caller is refused, and a later
retry succeeds once every clock has passed the old window. The
closed-interval own-clock admission (`master_key.rs:314-322`) needs no
new margin for correctness; an owner-configurable supersession margin is
a permissible liveness refinement, not required for the slice.

This amendment supersedes the previous revision's "safety is never rolled
back; the recorded round is always eventually completed" posture — that
posture and the everywhere-gate cannot coexist, and the psyche's
correction decides which one stands (§8 restates this so it is seen).

No component-specific recognition of "spirit" anywhere; in `Quorum` mode
every `AuthorizeSignalCall` is cluster-authorized. Member nodes need NO
new behavior beyond the supersession arm in the same admission check they
already run. This slice still adds no approval predicate anywhere.

### 3.4 · The authorization unit, reworked: one operation's entry group

The hash-chain soundness argument from the previous revision is unchanged
and still load-bearing: the quorum machinery binds exactly one opaque
digest per round; the log is hash-chained (each entry's digest folds in
its predecessor's, `versioning.rs:257`); therefore one head digest
transitively fixes every entry beneath it, and authorizing a digest
authorizes the ordered group it tops, as a unit. The VCS is not flawed;
one round soundly covers several entries.

What changes is the UNIT the steady state binds:

- **Steady state (gate Enabled): one working operation = one round.** The
  staged entry group's final digest is proposed as the successor of the
  current head. A group of one entry is the degenerate case; an operation
  that writes several entries (record plus implied referents) is still
  one round — the batch argument working at operation scale.
- **The whole-unshipped-suffix batch as the ACCEPTANCE unit dies.** There
  is no unshipped-but-unauthorized suffix in an Enabled spirit's steady
  state: everything appended was granted first. The drain's "capture the
  suffix head and authorize it" pass no longer gates anything.
- **Where the batch round still earns its keep** (all three are the same
  mechanism — propose a digest that chains over many entries — applied to
  the residue cases):
  1. **The Disabled→Enabled transition.** History recorded while Disabled
     exceeds the cluster-authorized head. No ceremony is needed: the
     FIRST granted advance after enabling proposes a digest that chains
     over the entire disabled-era residue, and the one grant covers it
     transitively — the cluster head jumps from its old point to the new
     head in one round. When the owner wants the residue propagated
     WITHOUT waiting for a new write, the reconciler (§3.6) runs one
     batch round for the current head, explicitly.
  2. **Crash windows** (§3.8): recovery re-asks bind the staged group's
     digest — identical re-proposal, idempotent, the built round
     machinery unchanged.
  3. **Grant-then-ship-failure retries** (§3.6): the suffix waiting in
     the outbox is already authorized; the ship-time re-ask hits the
     immediate re-grant of the standing committed head
     (`root.rs:1347-1351`) — no new cluster round.
- **Intake coalescing is a deferred optimization, not part of this
  slice.** Several queued writers COULD stage as one group under one
  round (all-or-nothing: one refusal refuses them all). Named so nobody
  re-derives it; not designed here.

The old wedge-hazard analysis (a refused proposal pinning the contract)
resolves differently now: the pin is broken by dead-round supersession
(§3.3), not by completing the recorded round — because under the
everywhere-gate the recorded round's content no longer exists anywhere.

### 3.5 · The intake path: stage, authorize, materialize

This section replaces the previous revision's §3.5 ("spirit-side drain:
decoupled from the working reply"), whose premise the correction
overrides. The recording caller now waits on the cluster round by design
— that is the psyche's trade, stated plainly in 3.5.4 — and the design
work is making the waiting and refusal surface clean.

**3.5.1 · The three phases.** With the gate Enabled, a head-advancing
working input runs:

1. **Stage** (fast, local). The nexus processing runs in BUILD mode: it
   performs its reads against committed state, assembles the operation
   group — the ordered would-be log entries with their payloads — and
   computes the prospective head digest, WITHOUT touching the log. The
   group is durably parked in a staging slot inside the same store (a new
   sema-engine seam: a staging table beside the commit log, written in
   its own small transaction). The staged group and the held reply are
   bound to the connection.
   The digest is deterministic here because the entry digest folds no
   wall clock — only store name, schema hash, commit sequence, snapshot,
   predecessor digest, and the operations (`versioning.rs:257-285`) —
   and head-advancing intake is serialized (3.5.3), so nothing commits
   between stage and materialize.
2. **Authorize** (the round; seconds normally, bounded by the window on
   refusal). The `ClusterAuthorizer` submits the typed ask and drains the
   observation session (§3.2) — outside the engine actor's mailbox
   (3.5.3), so reads flow meanwhile.
3. **Materialize or discard** (fast, local).
   - On the grant: one atomic transaction appends the staged entries to
     the log (reusing the existing entry+outbox+counters unit,
     `engine.rs:2079-2095`), writes their outbox rows, clears the staging
     slot, and the held reply (for example `RecordAccepted`) goes to the
     caller. Acceptance happened at the grant; this step is the local
     materialization of an already-accepted operation.
   - On any other terminal outcome: the staging slot is cleared and the
     caller receives the typed refusal. Nothing was appended; no reader
     ever observed the operation; nothing propagates.

The staging slot is machinery, not acceptance: it is invisible to every
read surface, it never survives a refusal, and its only purpose is crash
recovery (§3.8). It does not violate "nothing is recorded anywhere" —
what the psyche's rule governs is the operation's existence in observable
state, and a refused operation never reaches any observable state.

**3.5.2 · The typed refusal surface.** signal-spirit gains one versioned
addition: `Output::AdvanceRefused(AdvanceRefusal)`, where
`AdvanceRefusal` carries a closed reason enum — no strings:

- `Denied` — criome reached a terminal deny.
- `Expired` — the authorization window closed before the quorum
  completed (a member down, a partition).
- `Unavailable` — no operational quorum contract (the unfounded-criome
  loud refusal).
- `Unreachable` — the local criome could not be reached or its session
  went dead (spirit's backstop deadline).

The existing `ApplyRefusal` / `ApplyRefusalReason` shape
(`schema/signal.rs:792-797`) is the pattern but stays the peer-apply
ingress vocabulary; the two contact points keep their own closed types.
Mapping is one closed match: `GateDecision::Refused(Denied|Expired|
Unavailable)` and `GateDecision::Unreachable` → the four reasons above.
A `CriomeGateError` machinery fault also refuses the operation (the
caller cannot distinguish machinery from refusal and should not; the
fault is logged loudly on the daemon side).

**3.5.3 · Reads unaffected — the mailbox split.** The emitted engine
actor serializes every working request through one mailbox
(`src/schema/daemon.rs:488-508,569`); awaiting a cluster round inside
`handle_working_input` would stall every read behind every write. The
amendment splits the turn:

- The per-connection task asks the engine actor to **stage** (one fast
  mailbox turn). A read or otherwise non-advancing input completes
  entirely in this turn, exactly as today — reads never wait on a round
  and are never authorized.
- The connection task itself awaits the **authorize** session (the
  existing `spawn_blocking` drive), holding no engine borrow.
- The connection task asks the engine actor to **materialize or
  discard** (one fast mailbox turn) and writes the reply.

Head-advancing flows serialize among THEMSELVES across all three phases
(an async advance lock owned by the daemon spine, first-in first-out):
one outstanding staged group, one outstanding round — which is also what
makes the staged digest deterministic (3.5.1) and keeps at most one
proposal ahead of the cluster head. Queued writers wait behind the
current round; reads bypass the lock entirely and only ever wait for the
millisecond-scale stage and materialize turns. This touches the
schema-rust daemon emitter (the spine is generated), named in the delta
map (§9).

**3.5.4 · The write-path consequence, honestly.** Every head-advancing
operation now waits on the quorum round before its caller hears anything.
The observation session sits on the intake path. Normal case: the
two-round commit across healthy peers — network round-trips plus signing,
around a second locally, a few seconds across real links. Refusal case:
bounded by the quorum window (tens of seconds live, owner-configured)
plus the session backstop. A queued writer additionally waits for the
rounds ahead of it. This is the psyche's designed trade — cluster
acceptance IS the write — and this design does not soften it; it bounds
it (window + backstop, always a definite typed outcome) and keeps reads
out of it. Callers' client-side timeouts must exceed the window bound;
the CLI and harness surfaces should present `AdvanceRefused` reasons as
they are.

One honest edge: a caller whose CONNECTION dies while the round runs has
an indeterminate outcome (the round continues; a grant will materialize
the operation, a refusal will discard it). This is the standard
distributed-write ambiguity every database has at connection death; the
definite signals are only the accepted reply and `AdvanceRefused`
received.

**3.5.5 · Which inputs are gated.** Spirit today classifies reads vs
writes implicitly in the nexus dispatch (`nexus.rs:1222-1313`). The
amendment makes the classification a closed, explicit surface (one match,
enum-contact-points): effect commands and sema-writes (Record, Propose,
Clarify, ResolveClarification, Supersede, Retire, ChangeRecord,
ChangeCertainty, BumpImportance, RegisterReferent — everything that
appends) are head-advancing and gated; queries, observations, lookups,
counts, subscriptions, and Version pass ungated, as does any other input
whose processing appends nothing. `ApplyAuthorizedRecord(s)` (§4) is NOT
gated by intake: it carries an authorization that already happened and is
judged by the receiving criome (acceptance-by-verification), then
materializes directly. The owner-only meta plane (`Import`,
`CollectRemovalCandidates`) stays owner-trust and is not policed by this
option, as settled — noting plainly: `Import` is the privileged escape
hatch and writes locally without a round; it is owner-only by socket and
out of the working plane.

### 3.6 · What shipping means now: distribution of accepted state

Under the everywhere-gate, everything in an Enabled spirit's log is
cluster-authorized by construction. Shipping is therefore pure
DISTRIBUTION — moving accepted state to the other members — never a
second acceptance judgment on the sending side. The drain machinery
survives with its meaning changed:

- **The ship drain** (the reworked `PropagationDrain`): on each
  materialization it receives "head advanced" mail exactly as today and
  ships the unshipped outbox suffix. It no longer gates: by the time it
  runs, acceptance already happened at intake.
- **The ship-time grant fetch.** The §4 push carries the authorization
  identifier and Evidence. Spirit does not durably retain grants; at ship
  time the drain re-asks its criome for the suffix head, which
  short-circuits to the immediate re-grant of the standing committed head
  with the stored round's Evidence (`root.rs:1347-1351,1525-1530`) — a
  local socket round-trip, no cluster round. This keeps spirit stateless
  about grants and makes grant-then-ship-failure retries trivially safe:
  the outbox suffix waits, the next mail re-fetches, ships, and
  acknowledges the cursor.
- **The residue reconciler.** The one case where the drain still asks for
  a genuinely NEW round: disabled-era residue (§3.4 case 1) — an
  unshipped suffix whose head the cluster has never granted. Enabling the
  gate (the owner `Configure`) fires one reconcile mail; the drain
  proposes the current head, the batch grant covers the residue
  transitively, and the suffix ships. This pass goes through the same
  advance lock as intake (3.5.3), keeping one proposal outstanding.
- For deterministic tests the drain stays drivable directly
  (`Engine::drain_propagation_once`), now meaning "ship what is
  accepted" plus the residue round when one is owed.

### 3.7 · Contact points (enum-vs-enum, single matrices)

- Criome ingress: `AuthorizationMode` × operational-contract presence →
  behavior (§3.3 table) — one match, as implemented.
- Criome successor admission: recorded-row presence × row-round state
  (`Gathering`-live | `Gathering`-dead | `Authorized`) × digest equality →
  admit | supersede | idempotent re-open | refuse-conflict (§3.3) — one
  amended match at the existing `co_sign_admission` seam.
- Spirit session parse: `AuthorizationStatus` × grant-presence →
  `GateDecision` — implemented, unchanged.
- Spirit intake classification: `Input` → advancing | non-advancing —
  one new closed match (3.5.5).
- Spirit refusal mapping: `GateDecision` → `Output` (`AdvanceRefused`
  reason | the held accepted reply) — one new closed match (3.5.2).
- Spirit gate mode: Disabled | Enabled(socket) — implemented, unchanged.
- Router local delivery: `ComponentKind` × deployed-ingress presence →
  deliver | typed refusal (§1) — unchanged.

### 3.8 · The crash-window ledger

The staging slot exists for exactly these windows. On every daemon start,
an occupied staging slot is resolved BEFORE the intake path opens:

1. **Crash after stage, before the ask left.** Recovery re-asks with the
   staged digest — from criome's view a first ask. Grant → materialize;
   refusal → discard. Either way resolved.
2. **Crash mid-round.** The durable round stands criome-side
   (`Gathering`); the recovery re-ask is an identical re-proposal and
   re-opens it with a fresh window (`root.rs:2067-2083`). Resolves as
   case 1.
3. **Crash after the grant, before materialization.** The cluster
   accepted the operation — the contract head already advanced to the
   staged digest. The recovery re-ask short-circuits to the immediate
   re-grant (`root.rs:1347-1351`) and recovery materializes the staged
   group. This is the everywhere-gate semantic doing its work: once
   granted, the operation IS accepted; local materialization is
   subordinate bookkeeping and MUST complete. (The original caller never
   got its reply — the indeterminate-outcome edge of 3.5.4.) This is
   also why the stage phase must park the group DURABLY before the ask
   leaves the process: if the staged content could be lost after a grant,
   the cluster head would name a digest nobody can materialize —
   unrecoverable. Durable staging closes that hole by construction.
4. **Crash after materialization, before ship.** The outbox holds the
   authorized suffix; the ship drain's next pass re-fetches the re-grant
   and ships (§3.6). The existing outbox cursor discipline is unchanged.
5. **Criome restarts mid-round.** The durable round survives; spirit's
   session goes dead → `Unreachable` → the operation is refused, staging
   discarded; a later identical or differing proposal resolves through
   the idempotent re-open or dead-round supersession (§3.3). Fail-closed
   at every fork.

Out of scope, named: recovery while the cluster head moved concurrently
(another member advanced the same contract between crash and recovery) is
the concurrent-origination fork, deferred as settled (§4.6).

### 3.9 · Slice test/proof plan (amended)

**Pure/unit (flake checks):**

- The session-parse matrix negatives carry over with the amended
  consequence: Granted-without-grant, digest mismatch, foreign slot,
  deadline expiry, off-contract frame → **operation refused, nothing
  appended, store unchanged** (previously: head held, ship withheld).
- Intake classification: every `Input` variant lands in exactly one arm
  of the closed advancing/non-advancing match; reads complete ungated
  with the gate Enabled and criome absent.
- Staging: stage-then-discard leaves no observable trace (record count,
  head, outbox, queries — all unchanged); stage-then-materialize equals a
  direct Disabled-mode write byte-for-byte (same entries, same digests);
  recovery resolution for ledger cases 1-3 (stub criome socket).
- Criome bridge: the supersession matrix — live-row conflict still
  refused; dead `Gathering` row superseded by a differing successor;
  `Authorized` round never superseded; identical re-proposal re-opens;
  re-grant of the standing head carries the stored Evidence.
- Criome window expiry unchanged (pushes Expired; the row stands until
  superseded).

**The loopcheck** (stateful, named output, same posture and harness as
the founding proof): `spirit-cluster-gates-acceptance-over-router-test`,
two nodes, two real routers on loopback TCP, two real criome daemons,
short quorum window, a real spirit engine on node A gated against
criome A. Sequence and witnessed claims:

1. Found the 2-of-2 root over the router (reuse the founding drive:
   initiate on A, agent-performed explicit accept on both meta sockets,
   `Founded` with the same anchor on both).
2. **Disabled-era residue:** with the gate Disabled, record TWO entries
   on spirit A — accepted immediately, nothing propagates. Enable the
   gate (owner Configure).
3. **Accepted advance covering residue:** record a THIRD entry → the
   intake round proposes its prospective head; ONE round; the caller's
   reply arrives only after the grant; assert the reply is accepted, the
   head equals the third entry's digest, all three entries ship, and
   criome B's ledger witnessed ONE committed round (the batch covering
   the residue transitively).
4. **Refused advance — the corrected outcome:** stop node B's router
   listener; record a FOURTH entry → the round stays Gathering, the
   window expires, Expired is pushed → assert the caller received
   `AdvanceRefused(Expired)`, **the head did NOT advance** (still the
   third entry's digest), the record count is unchanged, no store or
   outbox trace of the fourth operation exists, and reads served
   normally throughout the round (issue an Observe mid-round).
5. **Supersession retry:** restore B; record a FIFTH entry (a different
   operation, hence a different prospective digest from the same head) →
   criome A supersedes the dead round's row and originates fresh →
   granted → assert the head advances to the fifth entry's digest and it
   ships. (Proves §3.3's dead-round supersession end to end.)

Falsification: if spirit bypassed criome, step 4 would accept and
advance; if the parse trusted status without the grant, a crafted
Granted-without-grant criome would accept; if supersession were missing,
step 5 would refuse forever with a conflict; if staging leaked, step 4
would leave an observable trace.

## 4 · Slice: propagation with receiving-side acceptance (immediately after §3)

### 4.1 · Shape (b), settled — unchanged

The authorization approval carries the target host IDs; the state-bearing
spirit pushes. Criome owns membership (the propagation targets are the
operational quorum contract's members), the router owns reachability and
the durable delta queue, spirit pushes exactly where the approval says.
The recorded reasons against shapes (a) and (c) stand as written in the
previous revision: (a) adds a round trip, a new criome→spirit channel on
every node, and misses offline members (its value is as a future
repair/bootstrap pull); (c) duplicates criome's membership and the
router's reachability inside spirit and erodes the quorum-ignorance
boundary.

### 4.2 · Design (adjusted to the everywhere-gate)

Flow for one authorized batch (suffix head H) on node A, cluster {A, B, ...}:

1. **Targets on the approval.** When the criome bridge stores a Granted
   state it resolves the propagation targets: the operational quorum
   contract's members minus the requesting host, each as its Criome host
   ID. These ride the grant — including the ship-time re-grant (§3.6) —
   to spirit as opaque routing data (wire shape §4.3).
2. **Spirit pushes one batch per target.** The SHIP drain (§3.6) frames
   the unshipped suffix as ONE signal-spirit `ApplyAuthorizedRecords`
   request per target — ordered entries plus the carried authorization
   (the operational contract digest + the authorized head reference) plus
   the assembled quorum Evidence, fetched at ship time via the standing
   re-grant. Destination = (target host ID, `ComponentKind::Spirit`),
   submitted to the LOCAL router; the router sees an opaque payload
   addressed to a (host, component) pair, resolves host → route →
   durable backlog exactly as built.
3. **Peer acceptance — the loop-tying check (settled intent).** The
   receiving spirit hands the carried identifier + Evidence to ITS OWN
   criome before applying — so no spirit can unilaterally skip
   authorization. Criome B answers Authorized exactly when the identified
   round is already committed in its durable ledger (it voted — the
   normal case), or the carried Evidence BLS-verifies against its
   admitted operational contract (signatures + threshold), in which case
   criome B records the co-signed successor row and advances its contract
   head — the offline-at-quorum member catches up. Anything else —
   unknown contract, failed verification, no local criome reachable — is
   a typed `ApplyRefusal`; nothing written. Cryptography is criome's
   domain at both ends; spirit never verifies BLS.
4. **Peer applies, chain-checked**, atomically: the batch's first entry
   chains onto B's applied head, each entry chains onto the previous, the
   last entry re-hashes to the authorized digest. Under the
   everywhere-gate this apply is acceptance-by-verification: the round
   ALREADY gated this state's acceptance cluster-wide; B's criome check
   confirms that fact locally. It does not run a new round and does not
   enter B's intake gate (§3.5.5). Any break, including a gap, is a typed
   refusal; gap repair is future (§4.6).
5. **Offline targets — the delta, no polling.** The LOCAL router's
   durable outbound backlog holds the forward (crash-durable) and drains
   on the peer-session-established push. Spirit tracks nothing; no retry
   loop, no poll. Pushes to one destination are backlog-ordered; the peer
   applies in log order and refuses a gap.
6. **Both directions.** Symmetric by construction: B's own head advances
   run the same §3 intake gate and the same push back toward A.
   Sequential only; concurrent forks stay out of scope.

The legacy direct mirror path (`MirrorShipper` → `mirror::ComponentShipper`
→ `MirrorTarget::Address` socket) is superseded by the router push and
retires with this slice (a bead). Checkpoint publication / fresh-node
restore is out of slice scope (§4.6).

### 4.3 · Wire/contract changes

As in the previous revision — this slice carries the §1 addressing
groundwork: signal-standard owns the single vocabulary; signal-router's
envelope becomes (CriomeHostId, ComponentKind) pairs with opaque payload
octets and `CriomeHostId` becomes typed key bytes; the router's
projection file dies and local delivery is the ComponentKind table;
signal-criome's authorization request carries the typed reference
(string trio retired) and its Granted state carries the assembled quorum
Evidence plus the propagation targets (targets beside the grant, not
inside the signed statement — routing advice stays advice, the peer
re-judges anyway); signal-spirit gains `ApplyAuthorizedRecords` (batch
form; a batch of one replaces the singular variant). One canonical
asserted round-trip per new type. Addition from this amendment:
signal-spirit also carries `Output::AdvanceRefused(AdvanceRefusal)`
(§3.5.2), landing with the §3 work, before this slice.

### 4.4 · What spirit knows at the end (boundary audit)

Spirit's total vocabulary after these slices: "my local criome socket",
"authorize this prospective head digest" (typed reference in, terminal
verdict out), "materialize on grant, refuse otherwise", "push this batch
to these opaque host IDs via my router", "ask my criome whether a carried
authorization is real and locally accepted before applying", and its own
store's chain integrity. No quorum, no threshold, no membership, no
reachability, no window. The psyche's boundary holds.

### 4.5 · Slice test/proof plan

As in the previous revision, with acceptance-semantics assertions folded
in. Pure/unit: contract round-trips for the new types; router
local-delivery table; criome Granted-state targets and accept-and-record;
spirit apply-ingress negatives (tampered evidence, unknown identifier,
digest/entry mismatch, interior chain break, gap, no local criome — all
refused, nothing applied). Loopchecks (stateful, named outputs):

1. `spirit-propagates-accepted-head-over-router-test` — extend the §3.9
   harness with a spirit engine on node B: record on A (intake round,
   accepted) → A pushes ONE batch over router A → router B → B's ingress
   asks criome B (voter path: round already in its ledger) → B applies
   atomically → assert B's applied head equals A's head. Falsification: a
   harness that skips the quorum, tampers one signature byte, or forges
   the identifier must yield `apply_refused` and no head movement on B.
2. `spirit-delivers-delta-when-peer-returns-test` — authorize and accept
   with both up; take down B's router listener BEFORE the push; assert
   the forward parks in A's durable backlog and B is unchanged; restore;
   assert the backlog drains on the session event (no poll) and B
   converges. Restart A's router mid-test to witness crash-durability
   end-to-end.
3. Both-directions convergence: distinct entries on A then B
   (sequentially, not concurrently), both heads converge on both nodes.

The offline-at-quorum member acceptance (verify-then-record) is covered
at unit level criome-side; a 3-node loopcheck variant stays an optional
extension. The live two-VM run stays the operating-system-implementer
follow-up after the loopchecks are green.

### 4.6 · Explicitly out of scope (named so nobody re-derives them)

- Approval predicates: lineage checks, fork rules, thresholds — psyche
  says premature.
- Concurrent-origination fork resolution (two members proposing different
  successors from the same head inside one window), including recovery
  under a concurrently-moved cluster head (§3.8).
- Gap repair / history fetch / fresh-node bootstrap from peers; checkpoint
  restore.
- Spirit pinning its criome's public key for local grant verification.
- Cluster membership change / rotation (the reissue seam is §5).
- Intake coalescing of queued writers (§3.4).

## 5 · Slice: the root issues the operational cluster quorum sub-contract

**Subsumed in framing by `CriomeStateGovernanceDesign.md` (same
directory, 2026-07-07).** The psyche set a unified model: a new
contract is a state change proposed through the parent quorum — so the
issuance below becomes a change to the root's child-set state slot, and
the record type `Contract` is renamed `Criome` (that design's §4, §9,
§10). The mechanics of this section survive as the implementation of
that state change: the same root-quorum round, the same
evidence-carrying admission, the same operational resolution and
staging posture. Membership rotation (item 4) becomes account
supersession with slot adoption there. Read this section together with
that design; where the two differ in framing, that design governs.

Unchanged by this amendment. The operational cluster quorum contract is a
sub-contract of the root — issued and anchored by it, with its own
distinct contract identity; right now the root keys and the first
sub-contract keys are identical (same hosts, same criome installation, no
key export), and the root simply continues, unchanged. Air-gapping and
guarded-root operations are deferred design.

1. **Issuance.** The sub-contract document — member set, threshold, root
   anchor reference — is authorized over the ROOT contract as an object
   of kind `Contract`, through the ordinary two-round commit; members
   auto-approve. Manual approval remains unique to founding.
2. **Admission carries the root's authorization.** Each member admits the
   sub-contract with the root-round Evidence; the verification chain
   every node can walk: pinned root anchor → root-authorized sub-contract
   → operational rounds under it. The §4.2 acceptance check verifies
   carried evidence against the ADMITTED OPERATIONAL contract.
3. **Operational resolution.** The bridge resolves the admitted
   sub-contract as the operational quorum contract once it exists;
   before that, staging over the founded root contract is the explicit
   prototype posture. The per-contract ledger and head chain are already
   keyed by contract; no row migration, no cutover event.
4. **Membership change / rotation** = the root issues a replacement
   sub-contract the same way — not designed here.

Proof: a loopcheck extending §3.9's — found the root, issue the
sub-contract through the root-quorum round, assert head advances gate
acceptance over the sub-contract (both criome ledgers key the new
contract).

## 6 · Tracker implications (NOTES ONLY — no tracker mutation this pass)

- **primary-nbmq**: §3 as amended is the acceptance gate nbmq's mirror
  rides on; §4 reactivates the nbmq.2 apply ingress in batch form and is
  the substance of nbmq.10, toward nbmq.12 (live two-VM proof). nbmq.5's
  durable backlog stays load-bearing for the offline delta.
- **primary-79z1**: §3.9's loopcheck remains the in-process precursor of
  the `.15` live proof; §5 is the phase-2 membership seam.
- The already-landed slice-1 lane's work is NOT discarded: the session
  parse, the criome bridge, the window machinery, and the drain skeleton
  all carry over (§2 table); the amendment moves the gate's seat and
  amends one criome admission rule (§9).
- Suggested new beads at pickup (not filed): sema-engine staging seam;
  spirit intake classification + three-phase turn + advance lock (with
  the schema-rust emitter change); signal-spirit `AdvanceRefused`;
  criome dead-round supersession (CatchingUp retirement); drain rework to
  ship/reconcile; gate seam decoupled from the `mirror-shipper` feature;
  the §3.9 loopcheck; then the §4 and §5 items as previously listed
  (contract consolidation, router retype, grant surface,
  `ApplyAuthorizedRecords`, acceptance check + push, loopchecks,
  sub-contract issuance, MirrorShipper/MirrorTarget retirement).

## 7 · Worker verification points (facts to confirm at pickup, cheap)

Resolved since the previous revision (baked into this amendment, cites in
the ground-truth block): the self-row is recorded at propose time; the
committed-head re-grant short-circuit exists; there is no dead-round
supersession today (the catch-up stage is what must be replaced); member
window admission has no skew margin; the entry digest folds no wall
clock; entry+outbox are one atomic transaction; no staged-append seam
exists; `ApplyAuthorizedRecord` answers fail-closed; a typed
authorization-refusal output shape exists.

Still to confirm at pickup:

1. **Build-phase purity.** Whether any effect handler's decision logic
   reads writes made earlier within the SAME operation group (the
   mutate-vs-assert choice in `import_record`, `store/mod.rs:742-744`,
   reads committed state; implied-referent groups look independent —
   confirm across the retire/supersede/change paths). Where a dependency
   exists, the build mode threads a pending-overlay view.
2. **Identifier issuance determinism.** Record identifiers issued during
   the build phase must be stable across stage→materialize (and across
   recovery materialization). Confirm issuance is counter-derived under
   the serialized head, not clock-derived.
3. **The schema-rust daemon emitter.** Confirm the emitted working-input
   turn can be regenerated into the three-phase shape (3.5.3) without
   breaking the other emitted components.
4. Outbox `acknowledge` forks (`MirrorHeadUnknown`, `OutboxEntryMismatch`,
   `MirrorHeadForked`) compose with acknowledge-to-batch-head (carried
   over).
5. Router backlog per-destination ordering and redial triggers (carried
   over, for §4).
6. `ApplyAuthorizedRecord` payload fields to extend into the batch shape
   (carried over, for §4).
7. The founded root contract is admitted into each member's
   `ContractStore` post-founding (carried over).
8. Criome client helper `transport.rs:355` (`states().first()`) — harden
   to slot-filtering (carried over).
9. `originated_request_rounds` is in-memory — confirm a criome restart
   mid-round recovers originator-driving via the durable round on
   re-proposal (carried over; §3.8 leans on it).
10. Guardian interplay: the agent-guardian admission runs BEFORE staging
    (a guardian rejection must not open a round). Confirm the ordering in
    the nexus pipeline.

## 8 · Open questions for the psyche

None at this amendment. The correction is self-contained; its one
non-obvious consequence is stated in §3.3 and restated here so it is
seen: the previous revision's "the recorded round is always eventually
completed; safety is never rolled back" posture cannot survive the
everywhere-gate (completing a refused round would materialize a refused
operation), so a window-dead, never-committed proposal row becomes
supersedable by a different successor. The safety argument — only a
round's originator can drive its commit, and it never will after
abandoning it — is in §3.3. If that consequence reads wrong, it is the
one thing to flag.

## 9 · Implementation delta from spirit 0.23.1 / criome 0.7.0

Landing order respects producers-before-consumers; each block is
independently shippable and leaves main green. Versioning: spirit,
criome, sema-engine, and signal-spirit each take a minor bump with their
block; wire changes ride the signal-spirit line.

**Block 1 — sema-engine: the durable staging seam** (new; no behavior
change for existing callers):

- New staging surface on `Engine`: stage a built operation group (park
  the ordered would-be entries durably in a new staging table beside the
  commit log, in its own small transaction; return the prospective head
  digest), materialize a staged group (one atomic transaction: data rows
  from the parked operations, entry appends, outbox rows, counters,
  staging-slot clear — reusing the `engine.rs:2079-2095` unit), discard
  a staged group, and surface an occupied slot at open (for §3.8
  recovery). The digest computation reuses `versioning.rs` unchanged.
- Materialization applies the PARKED entries verbatim (sharing the
  apply-entries machinery with import/suffix apply) — never re-executes
  the operation — and asserts the produced head equals the staged
  digest.

**Block 2 — criome: dead-round supersession** (root.rs):

- DIES: the catch-up stage — `HeadAuthorizationStage::CatchingUp`, the
  `standing_recorded_successor` re-drive and its settle path
  (`root.rs:1375-1382,1572-1579,1685-1728`).
- AMENDED: the successor-admission contact point
  (`CoSignAdmission` / `check_successor_conflict`,
  `root.rs:199-222,2627-2646`; solicit-side admission around `2195`)
  gains the closed dead-round arm of §3.3/§3.7: dead `Gathering` row +
  differing digest → durably replace and admit; live row → refuse
  conflict (unchanged); `Authorized` → never supersede (unchanged);
  identical digest → idempotent re-open (unchanged, `2067-2083`).
- UNCHANGED: `re_grant_standing_head` (`1347-1351`), the expiry push
  (`3465-3512`), window derivation, origination, evidence assembly,
  member auto-approval.

**Block 3 — signal-spirit: the refusal contract** (versioned):

- New `Output::AdvanceRefused(AdvanceRefusal)` with the closed reason
  enum `{Denied, Expired, Unavailable, Unreachable}` (§3.5.2). One
  canonical asserted round-trip.

**Block 4 — spirit: the gate moves to intake** (the main rework):

- `nexus.rs` (dispatch band `1222-1313`): the explicit closed
  advancing/non-advancing classification (3.5.5); effect and sema-write
  handlers gain the build mode producing staged groups through Block 1's
  seam when the gate is Enabled; Disabled keeps today's direct writes
  byte-for-byte. `ApplyAuthorizedRecord` stays fail-closed until §4.
- `store/mod.rs`: the direct `self.database.assert/mutate/retract` call
  sites (`742,744`, retire, supersede, resolve, change paths) route
  through the staged seam under Enabled.
- `engine.rs`: `handle_async` splits into the stage and
  materialize/discard surfaces; a start-time recovery hook resolves an
  occupied staging slot per §3.8 before the listeners open;
  `notify_head_advanced` becomes the SHIP trigger only; the gate seam
  moves out from under the `mirror-shipper` feature (acceptance gating
  must not be compiled out with shipping — its own feature or core); the
  shipper stays feature-gated.
- `daemon.rs` + the schema-rust daemon emitter: the three-phase
  working-input turn and the first-in-first-out advance lock (3.5.3);
  reads bypass.
- `criome_gate.rs`: survives nearly intact (`ClusterAuthorizer`,
  `HeadSessionBinding`, `GateDecision`, `GateRefusal`); the module and
  policy doc comments rewritten to the acceptance semantic (the
  "Working inputs are NOT refused at ingress" paragraph dies); the
  `GateDecision` → `AdvanceRefused` closed mapping added.
- `propagation.rs`: `PropagationDrain::drain_once` stops gating —
  becomes ship-with-regrant plus the residue reconciler round (§3.6),
  sharing the advance lock; doc comments rewritten.
- Tests: the unit matrix and the
  `spirit-cluster-gates-acceptance-over-router-test` loopcheck per §3.9;
  the existing drain-era tests rework their asserted consequences ("head
  held" → "operation refused, head did NOT advance").

**What dies outright, across blocks:** the accept-locally-then-authorize
premise and every comment stating it (`daemon.rs:152-160`,
`criome_gate.rs` module doc, `propagation.rs` module doc, `engine.rs`
field docs); criome's CatchingUp stage; the whole-unshipped-suffix batch
as the acceptance unit; the old loopcheck's "local head still advanced"
assertion.

**What is deliberately NOT touched:** the two-round commit driver, the
observation-session contract and its parse matrix, the window/expiry
machinery, the outbox/cursor discipline, the addressing model (§1), the
shape (b) propagation design (§4), and the §5 sub-contract staging.
