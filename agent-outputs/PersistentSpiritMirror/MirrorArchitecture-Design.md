# Persistent Two-Way Spirit Mirror — Architecture Design (for approval)

Status: design on paper, for the psyche to review and approve before any build.
Nothing here is implemented. All claims are grounded in the current source of
the three components (router, Criome, Spirit) and the two readiness maps in this
folder; where a claim is a design recommendation rather than existing code, it is
marked as a recommendation or a decision.

## Plain-language summary (for the psyche)

Think of each node as a person who keeps a private notebook (that is Spirit),
has a heart that decides whether something is genuine (that is Criome), and has a
voice that carries messages to the other person and listens for theirs (that is
the router). We want two of these people to keep the *same* notebook: when one
writes a line, the other's notebook shows the same line, live, both directions —
and later this same arrangement should work for three or more people, and for
other kinds of notebook too. This round is only about the notebook (Spirit).

Here is the whole story of one change, in plain terms:

1. You write a line in node A's notebook. It is written down as a *proposal*, not
   yet final.
2. Node A's heart looks at it and says "I vouch this is genuine" — that is one
   vote.
3. Node A's voice carries the proposal across to node B's voice, which hands it to
   node B's heart. Node B's heart independently looks at it and, if it agrees,
   casts its own vote and sends that vote back.
4. When enough hearts have voted yes — a *majority* of the nodes; for two nodes
   that means both, for three nodes it means any two — the change becomes final.
   Both notebooks now show the line, live, with no restart. Open node B's notebook
   and it is already there.
5. If node B cannot be reached, the change simply **waits**. It does not become
   final on either side. Nobody's notebook is quietly ahead of the other. The
   moment B comes back, the votes complete and both notebooks catch up on their
   own. There is never a "last writer wins" — it is agreement or nothing.

The same works in reverse: write on B, and A shows it.

### The key choices

- **Reuse the proven halves; build only the missing halves.** Two hard parts are
  already built and tested: the voice's *listening* side (it already receives a
  real notebook entry across the network, checks a real cryptographic signature at
  the door, and files it durably) and the heart's *judging* ability (it already
  demands a real majority of valid signatures and refuses when they fall short,
  and it survives reboot). We do not rebuild those. We build the *sending* side of
  the voice, the *vote-gathering* side of the heart, and the step that drops an
  approved line into the live notebook.

- **No new component, and we even drop one.** Mirroring is not a new program; it
  is just how Spirit, Criome, and the router behave when extended. The earlier
  proof used a fourth "mirror" program as a mailbox on the receiving side. In this
  design the voice hands the entry straight to Spirit, so that fourth program is
  not part of the path at all.

- **Agreement, not copying (quorum consensus).** The rule "a change is valid only
  when a majority of hearts vouch for it" is the heart of the design. It is what
  makes this safe rather than a naive copy. Even your own local change waits for
  the other heart's yes. With both nodes up this takes a single quick round-trip,
  so in practice your own change appears at once; the waiting only shows itself
  when the other node is genuinely down.

- **Private on the wire, and a real "who are you" check.** Today the two voices
  talk in the clear and only sign each message. We add two things: when two voices
  first connect they each prove their node identity to the other (a stranger
  cannot pose as your node's voice), and everything they say is then encrypted so
  no eavesdropper on the network can read the notebook lines in transit. Both the
  "who you are" proof and the "keep it private" encryption are anchored in the same
  one heart-held identity, so there is a single root of trust.

- **Off by default, and it survives reboot.** The whole arrangement is baked into
  each node's permanent configuration so it comes back after a reboot without
  anyone's help — but it starts **switched off**. It only turns on when you flip a
  single switch on the node's private control socket, and only when you trust the
  setup. For now you personally load "these two nodes are the trusted signers"; no
  automatic membership ceremony is built this round (but nothing here blocks adding
  one later).

- **One durable outbox so nothing is lost.** If the other node is down when you
  write, the message sits in a durable outbox that survives a restart, and the
  moment the connection comes back the outbox drains on its own. No repeated
  "are you there yet?" polling — the reconnection itself is the trigger.

### Trade-offs and things worth knowing

- Because a change waits for agreement, a change made while the peer is down is
  *pending*, not live, even on the node that made it. This is the correct meaning
  of "quorum or nothing," but it is a visible behavior: your own edit is not final
  until the other node co-signs. (Recommended, but see the decision list.)
- The first end-to-end milestone can be a one-direction live mirror *before* the
  full vote-gathering is switched on, purely to prove the pipe and the "see it
  live" step, then agreement is layered on. This de-risks the build.
- One deployment reality: the two standing nodes do not currently start
  themselves after a host reboot (they are built but left un-started), and the
  network door for the notebook traffic is only open on a different network than
  the one the two nodes actually use. Both are small, known fixes, listed below.

### Decisions that need you (full list later, short version here)

1. Confirm that an originating node's own change should be **pending until the
   peer co-signs** (true "quorum or nothing"), versus committing locally at once
   and only the *spread* to the peer waiting. Recommendation: pending until quorum.
2. Confirm the single **off-by-default switch lives on the voice's (router's)
   control socket** as the one authoritative gate. Recommendation: yes.
3. Confirm the identity proof is **mutual** (both prove) and **per-session** (once
   per connection, not once per message), riding a persistent encrypted link.
   Recommendation: yes to all three.
4. Confirm you are content that this round **hand-sets the two signers** with no
   founding ceremony (addable later).

Everything below is the engineering detail behind this summary.

## Reconciliation: which "already-proven mirror" was which path

This matters because the folder contains two different "it works" claims and they
are not the same path.

- The **live A→B proof on the standing prometheus guests**
  (`OperatingSystemImplementer-LiveMirrorProof.md`) ran over the **DISCARDED**
  path: Spirit's `mirror-shipper` shipped a body **directly over TCP to a separate
  `mirror` daemon** on node B (`spirit-daemon(mirror-shipper) → [5::8]:7474
  mirror-daemon`). **The router was not in that path**, and it used the separate
  `mirror` component. Per the corrected vision this path is rejected and is not the
  basis of this design.
- The **router-mediated receiving path** is proven only inside the router repo's
  own loopback tests (`router/tests/criome_forward_lands_in_mirror.rs`): a real
  content-addressed Spirit entry body crosses real TCP *through the router*, passes
  a real Criome BLS door-check, and lands durably, re-hashing to Spirit's real
  head. This is the path this design builds on. It is proven as a receive path but
  has never been run on the standing guests, and the *sending* side is still a
  hand-run witness binary, not the standing daemon.

Also reconciled: the old "the router only fans out references, not bodies" claim
is about a **different, local** mechanism (`router/src/authorized_object.rs`
`AuthorizedObjectFanout`, a local pub/sub of typed pointers). The **cross-host
forward carries real bodies** and always has. Implementers should not be misled by
the stale "references only" phrasing.

## Target architecture — the full flow for one change, both directions

Roles (each node runs all three; the separate `mirror` daemon is NOT used):

- **Spirit** — the journal. Owns the durable versioned record log. Originates a
  change; applies an approved change into its live store.
- **Criome** — the heart / notary / judge. Holds the node's identity key. Casts
  this node's vote, gathers the peer's vote across the voice, and renders the
  majority verdict. Owns the validity rule.
- **Router** — the voice / postal service. The only network-facing carrier. Sends
  sealed packages a local component hands it, receives packages from peers, checks
  identity at the door, and delivers to the right local component.

Node addresses: A = `5::7`, B = `5::8` (their projected node IPs). Both symmetric.

### One change, A originates (2-of-2 today; M-of-N later)

```
NODE A                                         NODE B
------                                         ------
Spirit-A: you Record a change
  -> committed locally as a PENDING proposal
  -> Spirit-A asks Criome-A: "authorize this
     under the mirror quorum contract"
Criome-A: casts vote #1 (signs the operation)
Criome-A: needs peer vote -> hands a
  "solicit signature" package to Router-A  ───────voice, encrypted────────►  Router-B
                                                   Router-B: door-check identity,
                                                   deliver to Criome-B
                                               Criome-B: independently validates the
                                                 proposal, casts vote #2 (signs the
                                                 same operation)
Router-A  ◄──────voice, encrypted─────────────  Router-B: return vote #2 package
Criome-A: assembles Evidence {vote#1, vote#2}
  -> evaluate_authorization vs the 2-of-2
     mirror contract -> AUTHORIZED
Spirit-A: proposal -> COMMITTED live record
Spirit-A: hands {authorized versioned entry +
  Evidence} to Router-A destined for Spirit-B ───voice, encrypted───────────►  Router-B
                                                   deliver to Spirit-B ingress
                                               Spirit-B: asks Criome-B to re-judge the
                                                 carried Evidence (fail-closed) -> AUTHORIZED
                                               Spirit-B: applies live via import_record
                                               -> open Spirit-B, the change is THERE, live
```

Reverse direction is byte-for-byte symmetric with A and B swapped.

Where Criome quorum sits: **at the center, twice.** First as the *gather + judge*
that turns a proposal into an authorized change on the originating node (votes
collected across the voice). Second as an *independent re-judge* on the applying
node before it touches its live store, so B never trusts A's say-so — B confirms
the majority for itself from the carried Evidence. Both judgments use the same
already-built majority evaluator.

Peer-unreachable behavior: if B cannot be reached during gather, Criome-A's
proposal stays **pending** and the solicitation package sits in Router-A's durable
outbox. Nothing commits anywhere. When B returns, the reconnection drains the
outbox, B votes, Evidence completes, and *both* nodes commit and converge. This is
the "waits, never last-writer-wins" rule realized.

## Net-new piece 1 — the router sending on its own (origination hand-off)

**Reuse:** the entire receive path (`TailnetForwardIngress`, `apply_forwarded`,
`HarnessDelivery::deliver_to_component_socket`, `RemoteRouterRegistry` route
resolution, `ForwardAdmissionWindow` replay/skew, `CriomeForwardAttestation`
door-check). The attestation digest already folds every routed object's
name/operation/size/octets, so objects are already authenticated end to end.

**The gap (source-confirmed):** the standing daemon cannot originate a
component-object forward. Origin submissions carry only a body string; the outbound
builder drops routed objects on the floor at three points:
`peer_delivery.rs::payload_for` hardcodes `Vec::new()` for routed objects;
`PendingRouterMessage::new` (`router.rs`) sets `routed_objects: Vec::new()` on the
origin path; `forward_to_remote` builds `DeliverRemote { remote_address, message }`
and never passes `pending.routed_objects`. Today only the throwaway
`router-forward-witness` bin can construct an outbound routed-object forward.

**Design — the push hand-off surface (local component → local router → peer):**

- **New origin submission op carrying objects.** Add an origin-side submission that
  carries `Vec<RoutedContractObject>` alongside the body. Two shapes are viable;
  recommendation is a **new router working-tier operation** (a `signal-router`
  input, e.g. `SubmitRoutedObjects { destination_actor, routed_objects }`) rather
  than widening `signal-message`'s `MessageSubmission` (which is a human-message
  vocabulary — a `RoutedContractObject` payload does not belong in a chat-message
  contract; keep the vocabularies separate per contract-repo discipline). The local
  component (Spirit or Criome) connects to its own `router.sock` and submits the
  sealed object; this is a synchronous Unix-socket call.
- **Thread through the existing pending machinery.** Populate the existing (already
  present) `PendingRouterMessage.routed_objects` field on the origin path; add a
  `routed_objects` field to `DeliverRemote`; pass `pending.routed_objects` from
  `forward_to_remote`; replace the `Vec::new()` in `payload_for`/`forward_request`
  with those objects. This reuses the entire inbound object machinery, which
  already carries objects (`forwarded_with_objects`, `DeliverHarness { …,
  routed_objects }`).
- **Push, not poll.** The submit synchronously drives `retry_pending →
  forward_to_remote` in the same call — the component's hand-off *is* the trigger.
  No poller. When the peer is up, delivery is immediate; when down, it parks (see
  piece 2).

**Actor topology:** unchanged root (`RouterRuntime`/`RouterRoot`); the new submit
enters `RouterRoot`'s mailbox exactly like a message submission, is turned into a
`PendingRouterMessage`, and delivery is the existing `RouterPeerDelivery` actor
(one `DeliverRemote` → one forward), now carrying objects.

**Typed contract:** extend `signal-router` with the origin submit op and reply
(`RoutedObjectsAccepted` / typed refusal). `RoutedContractObject`,
`ForwardedMessagePayload`, `RouterForwardRequest` already exist and are unchanged
on the wire — only the origin path stops sending them empty.

## Net-new piece 2 — the router's durable outbox and push redial

**The gap (source-confirmed):** `RouterRoot.pending` is an in-memory `Vec`,
initialized `Vec::new()`, never rehydrated on start. The durable tables are
`channels`, `adjudication_pending`, `messages`, `delivery_attempts`,
`delivery_results` — there is **no** pending/outbound-backlog table. A node that
parks a remote forward (peer down) and restarts loses it. Retry is event-driven
from four inline call sites; there is no peer-liveness/reconnect signal and no
persistent link (connections are one-shot, "one connection = one forward").

**Design — durable outbox (SEMA single-writer):**

- Add a durable **`outbound_backlog`** table in `router/src/tables.rs`, written by
  the router's SEMA plane (single-writer). A row keys on `MessageIdentifier` and
  carries what only lives in `PendingRouterMessage` today: `forward_marker`
  (Origin/Forwarded loop guard), the destination/home, the `origin`, and the
  `routed_objects`. Written when a forward is first enqueued; **removed on a
  terminal outcome** (peer `ForwardAccepted`, or a typed permanent refusal like
  `RecipientUnknown`); **retained** on transport error or transient park.
- On `RouterRoot` start, **rehydrate** `self.pending` from `outbound_backlog`
  before admitting new work, so a restart resumes the backlog. This is the missing
  startup path.
- Correctness note: this is policy-plus-working state that must commit atomically
  with the delivery decision, so it shares the daemon's durable store rather than
  splitting the owner (component-architecture: separate authority in the contract,
  not the state owner).

**Design — push redial (no polling):** unify this with the encrypted session
(piece 8). The redial trigger is **session (re)establishment**: when a peer's
authenticated encrypted session comes up (on start, or on reconnect after the peer
was down), that event pushes a "peer up" fact into `RouterRoot`, which drains the
`outbound_backlog` toward that peer. The reconnection *is* the event; there is no
"are you there yet" loop.

- If a persistent session is deferred (see build sequence), the fallback stays
  within the allowed push-not-pull carve-outs: a **peer-up beacon** — a router, on
  starting/binding its ingress, sends one "hello, I am up" forward to each
  configured peer; receiving that beacon is the peer's push trigger to drain its
  backlog toward the sender. A bounded reachability probe (an explicit carve-out)
  is the last resort, never a general poll loop.

**Contract:** the backlog table is internal (no wire change). The session-up event
is an internal actor message. If the beacon fallback is used, it is an ordinary
forward with a reserved recipient, no new wire type.

## Net-new piece 3 — Criome quorum collection (propose → gather → judge → commit)

This is the genuinely new consensus core. Be explicit: **today's forward
attestation authenticates the SENDER** (it proves "this package came from
Host(A)"), and it is **NOT a quorum vote.** A vote is a signature over the
*operation being authorized*, cast by a *member of the signer set*, counted
against a *majority threshold*. That gathering does not exist yet.

**Reuse (the judge is built and wired):**

- `ContractStore::evaluate` / `Threshold::decide` — counts distinct satisfied
  members, `Authorized` iff `satisfied >= required`, else `Rejected(QuorumShort…)`.
- `QuorumShape::is_valid_majority` — strict majority enforced at admission
  (2-of-2, 2-of-3; sub-majority contracts are rejected).
- `Evidence::has_valid_signature_from` — per-member real BLS verify, binding each
  signature to the member's admitted key, the operation digest, and the
  `AttestedMoment`.
- `evaluate_authorization` (`root.rs`) in `AuthorizationMode::Quorum` (the default)
  — calls the real engine on a caller-assembled `Evidence`.
- The vote preimage already exists: `OperationStatement` under DST
  `CRIOME-OPERATION-AUTHORIZATION-V1` = tag ++ signer identity ++ operation digest
  ++ AttestedMoment proposition digest.
- The ballot-box persistence exists: tables `signature_solicitations`,
  `submitted_signatures`, and the request types `RouteSignatureRequest` /
  `SubmitSignature` — but they only **store**; nothing tallies or dials.

**The gap:** a driver that actually solicits each member's vote across the voice,
collects the `StampedSignatureEnvelope`s, assembles `Evidence`, and drives the
verdict — plus the withhold-until-authorized behavior.

**Design — the quorum-collection round (new actor in Criome):**

1. **Propose.** Spirit-A asks Criome-A to authorize a change under the **mirror
   quorum contract** (a durable `Contract(Rule::Threshold{required: 2, members:
   [KeyMember(Host A), KeyMember(Host B)]})`, hand-admitted — see deployment). The
   proposal names the operation (the content-addressed versioned entry's digest)
   and opens an `AttestedMoment` proposition (a bounded time window with the
   member set as time authorities).
2. **Self-vote.** Criome-A signs the `OperationStatement` with its master key
   (vote #1) and time-signs the `AttestedMoment` (both are existing signing
   primitives). One member satisfied.
3. **Gather.** Criome-A hands a **solicitation package** to Router-A addressed to
   the peer's Criome (a `RoutedContractObject` naming a `signal-criome`
   solicit-vote operation, payload = the proposal: operation digest + moment
   proposition + contract digest). Router-A → Router-B → Criome-B (payload-blind
   octet relay to Criome-B's socket, keyed by the peer-Criome recipient in the
   bootstrap). This reuses the whole transport + door-check.
4. **Peer votes.** Criome-B independently validates the proposal (contract known,
   operation well-formed, moment window acceptable, node policy allows), signs the
   same `OperationStatement` (vote #2) and time-signs the moment, and returns its
   `StampedSignatureEnvelope`(s) back across Router-B → Router-A → Criome-A as a
   return routed object. (This is where `RouteSignatureRequest`/`SubmitSignature`
   get wired to actually move votes rather than merely persist them; the durable
   tables become the crash-safe record of an in-flight round.)
5. **Judge.** Criome-A assembles `Evidence {operation, stamp, evidence_signatures:
   [vote#1, vote#2], …}` and calls `evaluate_authorization` against the mirror
   contract → `Authorized` (2-of-2 satisfied) or `Rejected(QuorumShort)`.
6. **Commit.** On `Authorized`, Criome-A returns the verdict **plus the assembled
   Evidence** to Spirit-A, which commits the proposal to its live store and then
   ships the authorized versioned entry + the Evidence to Spirit-B (piece 4). On
   `Rejected`/timeout/peer-down, the proposal stays **pending and durable**; the
   round resumes when the missing vote arrives.

**Withhold-until-authorized:** the proposal is a durable pending row in Criome
(reuse the `authorization_states` table family). It is never surfaced as a valid
Spirit record until the verdict is `Authorized`. This is the "waits" behavior.

**Generalization to N:** the contract is already arbitrary M-of-N; the collector
solicits all peers and stops when `satisfied >= required`. Evidence is a list, so
adding nodes is data, not code. The re-judge on each applying node makes the
commit safe regardless of how many nodes participated.

**Independent re-judge on apply:** the applying node (piece 4) hands the carried
Evidence to its *own* Criome's `evaluate_authorization` before touching Spirit —
so every node confirms the majority for itself, fail-closed. This dissolves the
special case "trust the sender" into the normal case "judge locally."

**Contract:** `signal-criome` already has the vote/Evidence types
(`AuthorizationEvaluation`, `Evidence`, `StampedSignatureEnvelope`,
`OperationStatement`, `RouteSignatureRequest`, `SubmitSignature`). New wire is a
thin **solicit-vote request/reply** (propose an operation, return a stamped
signature) if the existing `RouteSignatureRequest`/`SubmitSignature` shapes are
not a clean fit for cross-node solicitation; prefer to reuse them and add only the
transport wiring and the tally/commit logic in the daemon.

## Net-new piece 4 — live application into the running Spirit on both nodes

**Reuse (source-confirmed, and this is the good news):** `Import` writes to the
same live `Arc<SemaDatabase>` that ordinary `Observe`/`Lookup` read from, so an
applied record is **immediately visible with no restart or reload** —
`versioned_log_head` advances too. "Open Spirit and see it live" is already real
for the local daemon.

**The gaps:**

- `Import` is an **owner-only meta operation** (0600 socket) and **bypasses the
  guardian and any authorization** — it trusts the owner. We do not want an
  *arriving foreign* record to be applied on owner-trust; it must be applied only
  because the *quorum* authorized it.
- `Import` carries the domain intent `Entry`, not the content-addressed
  `VersionedCommitLogEntry`. For content-address verification (the property that
  made the earlier proof trustworthy — the landed body re-hashes to the head), the
  applied object should be the versioned entry.
- The old `mirror`-component rematerialization hop is a dead end here: the mirror's
  `Restore` returns `NoCheckpoint` without a published checkpoint and rebuilds a
  *fresh* store ("path must hold no prior engine history"), not an incremental live
  apply. Dropping the mirror component removes this problem.

**Design — a new authorized-apply ingress on Spirit (ordinary tier,
quorum-gated):**

- Add a `signal-spirit` **working-tier** operation, e.g. `ApplyAuthorizedRecord
  { record_identifier, versioned_entry, evidence }`, delivered to Spirit's working
  socket by the local router (the recipient the router resolves to on node B).
- Spirit hands the `evidence` to its **local Criome** via `evaluate_authorization`
  under the mirror contract; only on `Authorized` does it call the existing
  `Store::import_record(record_identifier, entry)` to land the record into the live
  store (content-address verified at append time by `SemaVersionedLog`). Any
  non-`Authorized` verdict, or a body whose re-hash disagrees, is refused
  fail-closed.
- This makes the apply path *independently quorum-verified* on the receiving node,
  not owner-trusted, and it is live: an immediately following `Observe` shows it.

**Origination side reconsidered:** Spirit's outbound is no longer the
`mirror-shipper`-to-mirror-address path. On commit of an authorized proposal,
Spirit hands the authorized versioned entry (the same rkyv
`VersionedCommitLogEntry` the shipper already serializes) plus the Evidence as a
`RoutedContractObject` to its **local router** (piece 1). The `mirror-shipper`
feature and the `mirror` daemon leave the path.

**Contract:** new `signal-spirit` op + reply; reuse `import_record`,
`VersionedCommitLogEntry`, and `signal-criome` `AuthorizationEvaluation`/`Evidence`.

## Net-new piece 5 — both directions running autonomously

Symmetry is the whole point and it falls out of the above: every node runs Spirit
+ Criome + router; every node is both an originator (pieces 1, 3, 4-origination)
and an applier (pieces 1-receive, 3-peer-vote + re-judge, 4-apply). The mirror
quorum contract names all members and is identical on every node. The bootstrap on
each router names the peer(s) and the local Criome and Spirit as recipients. There
is no "primary" node. Convergence across a disconnect is handled by the durable
outbox (piece 2) draining on reconnect and each node re-judging on apply.

Conflict model (worth stating): because a change is only valid after a *majority*
co-signs a specific content-addressed operation, two nodes cannot both make
conflicting changes "valid" while partitioned — neither reaches quorum alone (in
2-of-2, neither; in 2-of-3, at most one side of a partition can hold a majority).
On heal, pending proposals complete or are superseded by the record log's existing
ordering rules. This is genuine consensus, not merge-on-copy.

## Net-new piece 6 — deployment, reboot-survivability, and the off-by-default toggle

**Reuse:** `persona-router.nix` (gate `PersonaRouter`, working+meta+supervision
sockets, `bootstrap.rkyv` peers/homes/grants, `criome_socket_path` wired, 7440
opened on the global firewall so it works over the `vmt` tap, hardened,
`wantedBy=multi-user.target`); `criome.nix` (working 0660 + meta 0600 sockets,
master key persisted at `/var/lib/criome/criome.masterkey` 0600, and — confirmed on
main — the `peerIdentitySeeds` `ExecStartPost` hook that issues `RegisterIdentity`
for a peer node's identity/key at deploy time); persistent `/var/lib/*` state dirs;
per-guest persistent `root.img`.

**Net-new / must-author:**

- **`spirit.nix` — does not exist.** Author a hardened, persistent Spirit node
  module mirroring the shape of `criome.nix`/`mirror.nix`: working + owner-only
  meta sockets, store at `/var/lib/spirit/spirit.sema`, config rkyv, gate atom,
  `Restart=on-failure`, `wantedBy=multi-user.target`. This is the missing
  production Spirit surface (only the `mirror` daemon has a module today).
- **Signer-set + contract seeding (hand-set this round).** At deploy time, on each
  node: seed the peer's identity→key via the existing `criome.nix` `peerIdentitySeeds`
  (`RegisterIdentity`), and admit the **2-of-2 mirror quorum contract** via
  `AdmitContract`. No genesis ceremony; an operator loads "these two nodes are the
  signers." (Nothing here blocks a later membership/rotation ceremony — it would be
  a new Criome flow that admits/retires members and re-admits the contract.)
- **Guest autostart.** `test-vm-host.nix` currently builds `microvm@<guest>.service`
  with `autostart = false`. For a *standing* pair that survives host reboot
  unattended, flip autostart on for the two mirror guests (or add an explicit start
  in the node config).
- **Firewall on the real network.** The notebook/vote traffic runs over the `vmt`
  tap between guests, not `tailscale0`. Router 7440 is already global (good). The
  mirror module opened 7474 on `tailscale0` only — since the `mirror` component is
  dropped, its port is irrelevant; but confirm **every** router↔router port used is
  open on the `vmt`-facing firewall. No tap-scoped gap for the router path.
- **`PersonaRouter` is not yet a horizon `NodeService` variant.** It is injected as
  a raw attrset in tests today. A first-class deploy atom for the router (and for
  Spirit) is a small `horizon-rs` `NodeService` addition, or keep the raw injection
  for this round. Flag for decision.

**The off-by-default toggle (net-new — nothing like it exists today):**

- No runtime meta-flip exists on any component; all current toggles are deploy-time
  `mkIf` gates. We add **one** runtime switch, default **OFF**.
- **Recommended placement: the router's meta socket** (the node's control socket),
  as a new `meta-signal-router` operation `SetMirrorEnabled(bool)` whose state is
  **persisted** to the router's SEMA store (so the switch survives reboot) and
  defaults false. Rationale: the router is the single network chokepoint — if it
  will neither originate nor accept mirror forwards, nothing crosses regardless of
  Spirit/Criome state, so this is the safest single gate; and the meta socket is
  owner-only, matching "flip it only when trusted."
- Defense in depth: Spirit also refuses to hand mirror objects to the router while
  the switch is off (it simply does not originate), and Criome refuses to run a
  mirror-quorum collection while off. One authoritative gate (router), honored by
  the others.
- The switch is the proof-of-done control: baked in, reboot-survivable, starts off,
  flipped on via the meta socket, and only then does the mirror run.

## The two security additions — identity proof and encryption

Both are anchored in the **same one root of trust**: the node's Criome-held BLS
identity (`Host(<node>)` master key), the same identity that already backs the
door-check. "Who you are" and "keep it private" share that root.

### Security addition 7 — router identity proof at bootstrap (first connect)

**Reuse:** `CriomeRequest::Sign(SignRequest)` → `Attestation` and
`CriomeRequest::VerifyAttestation(VerifyRequest)` → `VerificationDecision::Valid`.
Verify resolves the signer in the *verifying node's own registry* and returns
`UnknownSigner` if the identity→key binding is absent — so the peer must already
hold the presenter's identity→key (seeded at deploy time via `peerIdentitySeeds`).

**The gap to close:** `VerifyAttestation` does **not** check nonce
freshness/uniqueness today — a still-valid attestation is replayable within its
expiry. A genuine first-connect proof therefore needs challenge-response with a
freshness check *outside* Criome (Criome remains a pure signer/verifier).

**Design (recommended: mutual, per-session):**

- On first connect (session establishment), each router issues the other a **fresh
  random challenge nonce**. Each proves identity by asking its local Criome to
  `Sign` an **identity-proof attestation** whose audit-context nonce is the peer's
  challenge and whose content binds {node identity, this session's ephemeral
  encryption public key (see addition 8)}. Each presents the attestation.
- The verifying router runs `VerifyAttestation` against the registered peer
  identity (must be `Valid`) **and** checks that the attestation's nonce equals the
  challenge it issued (the small new freshness check, done in the router, not
  Criome). Mismatch or non-`Valid` → refuse the session, fail-closed. A stranger
  with no registered identity fails at `UnknownSigner`; a replayer fails the nonce
  check.
- **Mutual** (both prove): recommended, because either node can originate, and an
  encrypted channel needs both ends authenticated to defeat a man-in-the-middle. A
  one-way proof would leave the reverse direction unauthenticated.
- **Per-session** (once per connection, not per message): recommended, because the
  existing per-forward attestation already authenticates each message's content and
  sender; the handshake's distinct job is to establish the encrypted link and prove
  liveness, which is naturally amortized over the session. Per-connect proof on a
  one-shot-connection model would be redundant with the per-forward attestation and
  buy nothing.

### Security addition 8 — encrypted router-to-router channel

**The gap:** today the channel is plaintext `TcpStream` + length-prefixed frames.
It is *attested* (a BLS signature rides inside the frame) but not *encrypted* — the
body, actors, and object octets travel in cleartext.

**Design (authenticated ephemeral key exchange, Criome-rooted):**

- Introduce a **persistent authenticated encrypted session** between peer routers,
  replacing connect-per-forward. Establishment is a small handshake:
  - Each side generates a fresh **ephemeral X25519 keypair** for this session.
    (BLS12-381 keys are signature keys, not key-agreement keys; do not repurpose
    them for ECDH. Instead, the ephemeral X25519 public key is *vouched* by a
    Criome BLS signature — the identity proof of addition 7 signs {identity,
    ephemeral public key, challenge}. This binds the encryption key to the node
    identity without conflating the two key roles.)
  - The two ephemeral public keys are exchanged (each carried inside the identity
    proof so it is authenticated, not swappable by a MITM). Each side verifies the
    peer's proof (addition 7), then derives a shared session secret by **X25519
    ECDH** over the two ephemeral keys, and keys a symmetric AEAD (recommend
    ChaCha20-Poly1305) for all session traffic.
  - **Forward secrecy:** the ephemeral keys are per-session and discarded on close;
    a compromise of the long-term BLS identity key later does not decrypt past
    recorded sessions. Add periodic in-session rekey (new ephemeral ECDH) for
    long-lived sessions to bound the exposure of any one session key.
- This is Noise-IK/XX-shaped, with the *static-identity authentication* delegated
  to Criome BLS attestation rather than a raw static key — so the trust root stays
  the single Criome identity.
- **Synergy (design payoff):** the persistent authenticated session solves three
  net-new needs at once — encryption (this addition), mutual per-session identity
  proof (addition 7), and the **push redial** for piece 2 (session
  (re)establishment is exactly the "peer is back" event that drains the durable
  outbox). One mechanism, three requirements, no polling.

**Contract/keying notes:** the identity-proof + ephemeral-key exchange is a new
`signal-router` handshake message pair (challenge, proof-with-ephemeral-key). The
symmetric key never leaves the router process and is never persisted (secrets
discipline: transient, not written to store, logs, or the Nix store). The BLS
master key stays inside Criome; the router still holds no keys except the transient
per-session symmetric key.

## Quorum protocol — the round in full (propose → gather → judge → commit)

Consolidated for review; ties pieces 3, 4, 5 together.

1. **Propose (originator).** Spirit-A records a change as a durable *pending
   proposal*. It computes the content-addressed operation digest (the versioned
   entry) and asks Criome-A to authorize under the mirror quorum contract. Criome-A
   opens an `AttestedMoment` (bounded time window, member set as time authorities).
2. **Self-vote.** Criome-A signs the `OperationStatement` (member vote) and
   time-signs the moment. Satisfied members: {A}. For 2-of-2, one short.
3. **Gather (across the voice).** Criome-A hands a solicitation package to Router-A
   for the peer Criome. Transport + door-check are the reused receive path. If the
   peer is unreachable, the package parks in the **durable outbox** and the proposal
   stays pending — **nothing commits.**
4. **Peer vote.** Criome-B validates the proposal independently and, if it agrees,
   signs the same `OperationStatement` (member vote) and time-signs the moment,
   returning its stamped signature back across the voice. Satisfied: {A, B}.
5. **Judge.** Criome-A assembles `Evidence` and calls the reused
   `evaluate_authorization`. `Authorized` iff `satisfied >= required` (strict
   majority). Otherwise `Rejected(QuorumShort)` and the round waits for more votes.
6. **Commit (originator).** On `Authorized`, Spirit-A promotes the proposal to a
   live record and hands {authorized versioned entry + Evidence} to Router-A for
   Spirit-B.
7. **Apply (peer), independently re-judged.** Router-B delivers to Spirit-B's
   authorized-apply ingress; Spirit-B re-judges the carried Evidence with Criome-B
   (fail-closed) and, on `Authorized`, applies live via `import_record`. Both stores
   now hold the identical content-addressed head. Converged.

**Peer-unreachable → waits (the load-bearing behavior).** At step 3, an unreachable
peer means the proposal never reaches quorum and stays durably pending on the
originator; the solicitation sits in the durable outbox. No node shows the change
as valid. On reconnect (session up → push redial), the solicitation delivers, the
peer votes, Evidence completes, and *both* nodes commit and converge — with no
manual action. There is no last-writer-wins; a change is agreement or nothing.

**Convergence.** Every valid record is a majority-signed, content-addressed entry;
the apply is idempotent (same identifier + same content re-hashes identically), and
each node re-judges on apply, so redelivery after a crash is safe and lands the
same head. A node that missed a broadcast catches up when the durable outbox
redelivers.

## Deployment & toggle — summary

- **Baked in:** both guests run Spirit + Criome + router as hardened, persistent
  systemd units (`wantedBy=multi-user.target`), state under `/var/lib/*`, sockets
  recreated on start, config rkyv regenerated each start. Author the missing
  **`spirit.nix`**; enable `criome.nix` and `persona-router.nix`; flip guest
  **autostart on**; confirm the router port is open on the `vmt` firewall.
- **Trust seed (hand-set):** each node's Criome is seeded with the peer's
  identity→key (`peerIdentitySeeds` → `RegisterIdentity`) and admits the 2-of-2
  mirror quorum contract (`AdmitContract`). No genesis ceremony.
- **Reboot-survivable:** Criome master key persists (0600), Criome contracts +
  identities persist, Spirit store persists, the new router **outbound backlog**
  persists, and the router's persisted **mirror-enabled switch** persists. After a
  reboot the pair returns to exactly its prior posture.
- **Off by default:** the router's `SetMirrorEnabled` switch defaults false. The
  psyche flips it true over the owner-only meta socket when trusted; only then does
  origination/acceptance of mirror forwards and quorum collection run.

## Build sequence (independently buildable, component-sized pieces)

Recommendation: **prove one direction end to end before enabling both.** Order:

1. **Router origination (piece 1)** — `signal-router` origin submit-with-objects +
   thread routed objects through pending/`DeliverRemote`/`payload_for`. Provable
   against the existing receive side with a two-router loopback test. Unblocks
   "the standing daemon sends a body on its own."
2. **Spirit authorized-apply ingress (piece 4)** — new `signal-spirit` op landing a
   record via `import_record`, gated by a local Criome judge. With (1), this yields
   a **visible one-direction A→B live mirror** using the already-proven 1-of-1
   Criome gate — the first end-to-end milestone, "see it live on B," *before*
   quorum. Strong de-risk.
3. **Criome quorum collection (piece 3)** — the propose→gather→judge driver. Build
   and test **single-host, two Criomes under different users** first (no network),
   then over the router. Replaces the 1-of-1 gate with the real 2-of-2 majority.
4. **Durable outbox + authenticated encrypted session (pieces 2, 7, 8)** — the
   transport hardening and both security additions together (the session gives
   encryption, mutual identity proof, and the push redial in one). Test with induced
   peer-down/restart to prove the outbox survives and drains on reconnect, and that
   an unregistered/replaying peer is refused.
5. **Deployment + toggle (piece 6)** — author `spirit.nix`, enable modules, seed
   identities + admit the contract, autostart, firewall, and the off-by-default
   `SetMirrorEnabled` meta switch. Now reboot-survivable and baked in.
6. **Both directions (piece 5)** — flip the switch, prove A→B live, then B→A live,
   both landing on their own; add convergence tests (write-while-peer-down → waits →
   reconnect → both converge).

Each of 1–5 is a single-component change with its own tests; only 6 exercises the
whole pair. Steps 1–2 deliver a demoable partial result early; the full "quorum or
nothing" system is complete after 5, enabled and shown both ways in 6.

## Where this architecture spec should live (matter homes)

The quorum validity rule and the collection protocol are durable **matter**, not
Spirit intent — they belong in code-repo ARCHITECTURE and code, not in Spirit
records. Split by ownership:

- **Criome `ARCHITECTURE.md`** — the top-level validity rule ("a change is valid
  only when a majority of nodes' Criomes authorize; quorum authorizes or nothing
  changes; unreachable peer → waits; M-of-N, 2-of-2 now") and the
  propose→gather→judge→commit protocol, including the independent re-judge on apply.
  This is the primary home of the rule (Criome owns judging *and now* gathering).
- **Router `ARCHITECTURE.md`** — origination hand-off + durable outbound backlog +
  push redial; the persistent authenticated encrypted session, the mutual
  per-session identity proof, keying, and forward secrecy; the off-by-default
  `SetMirrorEnabled` meta switch.
- **Spirit `ARCHITECTURE.md`** — "mirroring is how Spirit operates over router +
  Criome" (not a component), the pending-proposal semantics, and the
  authorized-apply ingress + live-visibility guarantee.
- **CriomOS modules** — the new `spirit.nix`, module enablement/gating, the
  identity + contract seeding, guest autostart, and `vmt` firewall; the toggle's
  deploy-time default (off).
- **`signal-*` / `meta-signal-*` contract crates** — the new wire ops
  (`signal-router` origin submit + handshake; `meta-signal-router`
  `SetMirrorEnabled`; `signal-spirit` authorized-apply; `signal-criome` solicit-vote
  wiring reusing existing Evidence types). NOTA stays a human projection, never the
  inter-component transport.

## Open design questions / risks / decisions for the psyche

1. **Pending-until-quorum on the originating node (semantics).** Recommendation:
   an originating node's own change is *pending* until the peer co-signs (true
   "quorum or nothing"). Alternative: commit locally at once and only the spread to
   the peer waits (weaker rule, "last-writer-ish" locally). Needs your confirmation.
2. **Live-apply ingress: new ordinary-tier op vs owner-only meta `Import`.**
   Recommendation: a **new quorum-gated ordinary-tier** `signal-spirit` op, because
   meta `Import` is owner-trusted and would apply an arriving record without
   independent quorum verification. Confirm.
3. **Toggle placement.** Recommendation: one authoritative off-by-default switch on
   the **router's** meta socket, honored by Spirit and Criome. Confirm.
4. **Identity proof shape.** Recommendation: **mutual** and **per-session**, riding
   a persistent encrypted session. Confirm (these are the security-posture calls).
5. **Encryption model.** Recommendation: ephemeral X25519 ECDH → ChaCha20-Poly1305,
   with the ephemeral key authenticated by a Criome BLS attestation (single trust
   root), per-session forward secrecy + periodic rekey. Confirm the crypto choices
   or name a preferred suite.
6. **Persistent session vs one-shot forward (transport-model change).** The
   persistent authenticated session is the largest transport change but unifies
   encryption + identity proof + push redial. Risk: it replaces the simple
   connect-per-forward model. Accept the unification, or keep one-shot forwards and
   solve redial with the beacon fallback (less elegant, still push)?
7. **Signer set hand-set, no genesis ceremony this round.** Confirmed as in scope;
   the design leaves room for a later membership/rotation ceremony. Confirm you are
   content with hand-seeding for now.
8. **Deploy realities to accept:** guests currently do not auto-start after host
   reboot (flip autostart); `PersonaRouter`/Spirit are not first-class horizon
   `NodeService` atoms yet (small `horizon-rs` addition or raw injection this
   round); the `mirror` component and its `mirror-shipper` feature leave the path
   entirely. Confirm these are acceptable.
9. **Time-quorum (`AttestedMoment`) cost.** The reused evaluator also requires a
   quorum of *time* signatures on the moment. For 2-of-2 both nodes time-sign in
   the same round; this is folded into gather. Flag only so implementers budget the
   extra signatures; no decision needed unless you want to relax it.

## Pickup map (repos / files / types per piece)

- **Piece 1 (router origination).** `router/src/peer_delivery.rs` (`payload_for`,
  `DeliverRemote`, `forward_request`), `router/src/router.rs`
  (`PendingRouterMessage`, `apply_stamped_message_submission`, `forward_to_remote`,
  `retry_pending`), `signal-router` (new origin submit op; reuse
  `RoutedContractObject`, `ForwardedMessagePayload`, `RouterForwardRequest`).
- **Piece 2 (durable outbox + redial).** `router/src/tables.rs` (new
  `outbound_backlog` table; existing `messages`/`delivery_*`), `router/src/router.rs`
  (`RouterRoot::new`/`on_start` rehydrate; the four `retry_pending` sites),
  `router/src/remote_router.rs` (`RemoteRouterRegistry`), unified with the session
  event from piece 8.
- **Piece 3 (quorum collection).** `criome/src/language.rs`
  (`Threshold::decide`, `QuorumShape::is_valid_majority`,
  `Evidence::has_valid_signature_from`, `OperationStatement`, `ContractStore`),
  `criome/src/actors/root.rs` (`evaluate_authorization`, `admit_contract`),
  `criome/src/actors/authorization.rs` (`route_signature_request`,
  `submit_signature` — wire to actually gather), `criome/src/actors/store.rs` +
  `tables.rs` (`authorization_states`, `signature_solicitations`,
  `submitted_signatures`), `signal-criome` (`AuthorizationEvaluation`, `Evidence`,
  `StampedSignatureEnvelope`, `Contract`, `Threshold`, `PolicyMember`,
  `AttestedMoment`).
- **Piece 4 (live apply).** `spirit/src/engine.rs` (`import`, `configure`),
  `spirit/src/store/mod.rs` (`import_record`, read helpers on the shared
  `Arc<SemaDatabase>`), `signal-spirit` (new `ApplyAuthorizedRecord` op),
  `signal-criome` (`AuthorizationEvaluation`/`Evidence` for the local re-judge);
  drop `spirit/src/shipper.rs` + the `mirror` crate from the path.
- **Piece 5 (both directions).** Symmetric config; convergence tests spanning both
  routers, both Criomes, both Spirits.
- **Piece 6 (deploy + toggle).** New `CriomOS/modules/nixos/spirit.nix`;
  `criome.nix` (`peerIdentitySeeds`, `AdmitContract` seeding);
  `persona-router.nix` (bootstrap peers/homes/grants, `criome_socket_path`);
  `test-vm-host.nix` (autostart, `vmt` firewall); `meta-signal-router` (new
  `SetMirrorEnabled`) + `router/src/config.rs` persisted flag; `horizon-rs`
  `NodeService` (optional new atoms).
- **Security 7 + 8 (identity proof + encryption).** `router/src/criome_attestation.rs`
  (`Sign`/`VerifyAttestation` reuse), `router/src/forward_attestation.rs`
  (`ForwardAttestationVerifier`, `ForwardAdmissionWindow` — add the handshake
  nonce-freshness check), `router/src/peer_delivery.rs` +
  `router/src/router.rs::bind_tailnet_ingress`/`TailnetForwardIngress` (persistent
  session replacing one-shot connect; AEAD wrap), `signal-router` (handshake
  message pair carrying challenge + proof + ephemeral public key), `signal-criome`
  (`SignRequest`/`Attestation`/`VerifyRequest`/`VerificationDecision` reuse); the
  identity→key seed via `criome.nix` `peerIdentitySeeds`.
```
