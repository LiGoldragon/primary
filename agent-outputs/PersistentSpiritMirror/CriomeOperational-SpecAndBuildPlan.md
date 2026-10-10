# Criome Operational — Protocol Spec and Build Plan

Retired vocabulary (psyche ruling 2026-07-21): "mouth" -> textual interface; "organs" -> the two trees (nametree, structuretree); "spine" -> core invariant / core pathway; "door" -> entry point; "currency" -> value type. Historical text below is unreworded; read it through this table.

Making the Criome the deployment-authorization layer (SSH kept as fallback).
This is the linchpin design artifact for the vision locked in the psyche
interview: **today's spine is the build target; the phase-2 model is
forward-compatibility only.**

Grounding: every data-model and touch-point claim below was read directly on
current `main` of `criome`, `signal-criome`, `meta-signal-criome`, `router`, and
`lojix` under `/git/github.com/LiGoldragon/`. Anchors are `repo/path:line`. This
spec supersedes nothing already built; it names the net-new surface and reuses
the judge, the quorum driver, the router identity+transport, and the `Contract`
type wherever they already carry the weight. Nothing here is built or proven —
this is a plan.

Terminology (locked): **Criome** (C-R-I-O-M-E); *the Criome* = all of them; a
*Criome unit* is one cryptographic contract. We reuse the existing
`signal-criome` `Contract` type as the Criome unit; the reframe is cosmetic in
vocabulary but carries one genuine schema change (the `parent` field, A1).

## Reuse baseline — what already carries weight

These exist and are reused unchanged or nearly so. The net-new surface is small
by comparison, which is the good news.

- **The judge.** `ContractStore::evaluate` / `Threshold::decide`
  (`criome/src/language.rs:418-443`), strict-majority `is_valid_majority`
  (`language.rs:671-674`), real `blst` BLS12-381 min-pk verification bound to the
  registered key + operation + moment. Fail-closed on missing store/registry.
- **The quorum driver.** propose → gather → judge → commit
  (`criome/src/actors/root.rs:1218-1450`): `propose_quorum_authorization`,
  `solicit_quorum_vote`, `submit_quorum_vote`, `assemble_evidence`,
  `cast_quorum_vote`. Rounds are durable (`quorum_rounds` table,
  `criome/src/tables.rs:608`) so a restart resumes a pending round.
- **The transport (the voice).** `RouterQuorumVoice`
  (`criome/src/voice.rs:124-228`) rides the router's opaque routed-object
  carriage. Node identity = Criome `Host(<node>)` master pubkey; the router
  mutually proves identity (`router/src/identity_proof.rs:33-90`) and encrypts
  the session (X25519 ECDH → ChaCha20-Poly1305, forward-secret). **We do NOT
  design a new Criome-to-Criome peer lane; all new messages ride this voice.**
- **The moment / consensus clock.** `AttestedMoment` +
  `AttestedMomentProposition` + `TimeWindow` + `TimeSignature`
  (`signal-criome/src/schema/lib.rs:1015-1042,849`); majority-checked with real
  BLS at the judge (`AttestedMoment::rejection_reason`,
  `criome/src/language.rs:620-654`).
- **Anti-replay + durable authorization state.** `authorization_replay_nonces`
  and `authorization_states` tables (`criome/src/tables.rs:35,55,603-604`),
  `ReplayNonce`, `AuthorizationStateRecord`.
- **The owner-only meta socket.** `meta-signal-criome` `Input::Configure`
  (`meta-signal-criome/src/schema/lib.rs:236`); `CriomeDaemonConfiguration`
  (`signal-criome/src/schema/lib.rs:698-705`).
- **Content addressing.** `Contract::digest()` =
  `blake3(rkyv::to_bytes(Contract))` (`signal-criome/src/lib.rs:160-163`);
  `ObjectDigest::from_bytes` (`:69-72`). This is the exact mechanism the `parent`
  field disturbs (A1).

Net-new this spec adds: a `parent` field + root sentinel; a founding certificate
(genesis identity that carries attached signatures); a founding meta-op with
explicit owner accept; the per-signer clock gate; the two-round commit dimension;
a `Deployment` authorized-object kind + payload; and the lojix activation gate.

## Part A — Protocol spec (today's spine)

### A1. Data model: the Criome unit, the `parent` field, and the root variant

Today `Contract(Rule)` (`signal-criome/src/schema/lib.rs:725`) is a single-field
newtype: no name, no owner, **no parent**. Its content-address is
`blake3(rkyv(Contract))`. Introduce the parent as a net-new field:

```rust
// signal-criome/src/schema/lib.rs — the Criome unit
pub struct Contract {
    pub rule:   Rule,            // unchanged: the existing policy tree
    pub parent: ContractParent,  // NET-NEW
}

pub enum ContractParent {
    Root,                        // the sentinel: its own origin, no parent
    Parent(ContractDigest),      // authority chains upward to this contract
}
```

`ContractParent` is an **enum with named variants** (NOTA-idiomatic:
`nota-design` — model alternatives as variants, not flags; enum variants are
names, not codes). `Root` is a distinguished sentinel variant, **not** a
self-reference — this avoids the self-referential digest trap (a contract whose
digest is a function of a digest of itself) and keeps the base case clean, mirror
of the moment engine's self-grounding base case (`criome/ARCHITECTURE.md:764`).

Semantics of `parent` for **today**: it is a **provenance + authority-derivation
link**, evaluated only when a node walks a child to the root to confirm the child
descends from the founded anchor (A2). Normal `Threshold::decide` evaluation is
unchanged — the parent link does not add a new judged predicate today. This keeps
the judge untouched and defers the semantic weight (leased ownership, scoped
sub-authority) to phase-2, which the field is shaped to accept.

**The digest migration (explicit — this is load-bearing).** Because the digest
covers `rkyv::to_bytes(Contract)` (`signal-criome/src/lib.rs:160-163`), adding
any field re-serialises and therefore **re-digests every contract that ever
existed.** Every `ContractDigest` reference shifts: identity registrations that
name a contract, `PolicyMember::ObjectMember(digest)` links
(`lib.rs:781`), the Nix-seeded `quorumContracts` digests, and any
`QuorumRoundIdentifier::for_operation` derived key. Two migration strategies:

- **(Recommended, TODAY) Clean genesis.** There is **no persistent root and no
  live production contract set** — the Handover is explicit that "the mirror was
  never proven live on the standing machines" and "the persistent root contract
  does not exist." Treat the `parent` addition as pre-genesis: land it as a
  **coordinated storage-schema version bump** (`rust-storage-and-wire`: reordering
  fields / changing archive layout is a versioned storage change, not a
  refactor), add a startup guard that refuses (or, on the standing nodes,
  finds-empty) any pre-`parent` `contracts` table, and let the founding ceremony
  (A3) write the first `parent`-bearing contracts. Recompute the Nix
  `quorumContracts` seed digests under the new schema. This is a **minor** bump
  (breaking public change before 1.0, per `versioning`), and the daemon consuming
  the changed contract bumps too. **Operational precondition to verify before the
  ceremony: the two standing nodes' `contracts` tables hold nothing that must
  survive.**
- **(Fallback, if any durable contract must survive) Re-digest map.** Read each
  old-layout `StoredContract`, reconstruct as `Contract { rule, parent }` with an
  assigned parent, re-digest, rewrite, and **rewrite every dangling reference**
  (identities, object-members, seeds) through a digest-old→new map in one
  transaction. This cascades widely and is expensive; it is justified only if the
  operational precondition above fails. Today's plan assumes clean genesis and
  flags the precondition as a build item.

### A2. Root identity and the founding certificate

The root Criome unit is the contract whose `parent` is `Root`:

```rust
// the accepted initial state — hashed to the anchor, commits to founding keys
pub struct RootGenesis {
    pub root_contract:  Contract,               // parent = Root; rule = founding Threshold
    pub founding_keys:  Vec<FoundingMember>,     // ordered (Identity, BlsPublicKey) commitment
    pub domain:         GenesisDomainTag,         // CRIOME-ROOT-FOUNDING-V1
    pub genesis_nonce:  ReplayNonce,              // uniqueness / anti-collision
}
pub struct FoundingMember { pub identity: Identity, pub public_key: BlsPublicKey }
```

**The anchor** every node bakes in is `RootAnchorDigest =
blake3(rkyv(RootGenesis))`. Because `RootGenesis` embeds the ordered
`founding_keys`, the **hashed genesis commits to the founding quorum's public
keys**, satisfying concept 2 (self-certifying identity, KERI SAID model). The
founding key-set also **seeds the identity registry**, so the founded root
replaces today's single-key `ClusterRoot` admission anchor
(`criome/src/admission.rs:74-102`) — the root Criome, not a bare key, becomes the
trust anchor.

**Founding signatures ride ATTACHED, never folded into the hash** (prior-art
pattern 1; trap A). They are a separate accumulating collection keyed to the
anchor:

```rust
pub struct FoundingSignature { pub signer: Identity, pub envelope: SignatureEnvelope }
// preimage each founder signs: RootFoundingStatement { anchor: RootAnchorDigest, domain }
```

`SignatureEnvelope` already carries `scheme: SignatureScheme`
(`signal-criome/src/schema/lib.rs`), so the founding-signature verification path
stays scheme-tagged — the seam for phase-2 cold/hardware keys on a non-BLS scheme
(D). **Identity exists at submission**: `RootAnchorDigest` is computable the
instant `RootGenesis` is built (concept 2). Quorum finalization does not create
identity — it only accumulates enough `FoundingSignature`s. The `parent` chain of
every non-root Criome terminates at `root_contract`'s own digest; a verifier
walks child → … → root_contract and confirms `root_contract` is the one inside
its anchored `RootGenesis`.

### A3. The founding ceremony (unanimous, owner-accepted)

Founding uses the involved nodes' **Criome master keys**
(`criome/src/master_key.rs:56-63`; cold/hardware keys are phase-2). It is a
**UNANIMOUS/total vote** — every node must willingly establish its own root — and
acceptance is an **explicit owner action on the owner-only meta socket** (no
auto-approval). Two distinct knobs (do not conflate): the **collection window**
(how long the initiator gathers founding signatures — loose/large is fine) and
the **post-founding cooldown** (a settling delay before the founded root may
authorize anything).

Net-new meta-op (owner-only, `meta-signal-criome`, alongside `Configure`):

```
Input::AcceptRootFounding(RootFoundingAcceptance)   ;; owner explicitly founds
RootFoundingAcceptance { anchor : RootAnchorDigest, cohort : RootGenesis }
```

Net-new public-socket read-op (so the client can display the pubkey):

```
Input::ObserveNodePublicKey                          ;; public socket
Output -> NodePublicKey(BlsPublicKey)                ;; the node's Criome master pubkey
```

Sequence:

1. **Configure (each node, meta socket).** Owner sets `node_identity`, socket
   paths, and enrolls the founding cohort (member identities + each member's
   master pubkey, exchanged out-of-band; each pubkey read via
   `ObserveNodePublicKey` on that node's public socket).
2. **Initiator builds `RootGenesis`** (root `Threshold` over the cohort as
   `KeyMember` identities, `founding_keys` = the cohort pubkeys, `parent = Root`),
   computes `RootAnchorDigest`, and opens a founding round with a loose collection
   window. Identity now exists.
3. **Convey the founding proposal** to each peer across the router voice
   (`RouterQuorumVoice`) — no new lane.
4. **Explicit owner accept (each node).** The node's owner submits
   `AcceptRootFounding(anchor)` on that node's meta socket. Only then does the
   node's master key emit a `FoundingSignature` over
   `RootFoundingStatement{anchor}` and return it across the voice. A node signs
   **only if the anchor equals the exact cohort it was configured to found** —
   its own willing establishment. No auto-approval anywhere.
5. **Unanimity.** The initiator accumulates `FoundingSignature`s; founding
   finalizes only when **every** cohort member has signed (contrast A4/A5's
   majority for ordinary changes). One offline/unwilling node blocks founding by
   design — founding is the one place unanimity is correct.
6. **Persist the founded root** on each node: `RootGenesis` + all
   `FoundingSignature`s + `RootAnchorDigest`, in a net-new durable table
   (`root_founding`), and seed the identity registry from `founding_keys`. The
   post-founding cooldown may gate first authorization use.
7. **Later boots verify, never re-found.** On start the node checks its persisted
   anchor and refuses to re-found (closes the Handover's "haywire-bootstrapping
   trust on every boot"). The founded anchor also becomes the root that the
   router identity handshake ultimately derives from (phase-2 wiring; today the
   handshake keeps its first-boot `Host(<node>)` seed).

### A4. The per-signer witness-clock gate (the load-bearing fix)

Today `AttestationSigner::sign_quorum_vote`
(`criome/src/actors/signer.rs:344-368`) time-signs the moment proposition
**unconditionally** — it never reads `SystemClock` (`master_key.rs:222-234`) and
never compares its clock to the window. So an `AttestedMoment` proves only "a
quorum co-signed this window," not "now is inside it" (prior-art trap B). Fix:

**Each signer reads its OWN clock and emits the `time_signature` only if
`now ∈ [window.opens_at, window.closes_at]`; otherwise it refuses.** The refusal
is typed — `EvaluationRejectionReason::OutsideTimeWindow` already exists
(`signal-criome/src/schema/lib.rs:1143`) — and refuses the whole vote (a vote
without a valid time-signature is worthless to the round). Concretely,
`sign_quorum_vote` gains a `clock: &SystemClock` read and a guard before signing
`moment_bytes`; the peer path `solicit_quorum_vote`
(`criome/src/actors/root.rs:1256-1296`) already re-validates the member set and
`proposition_matches_members` (`:1477-1487`) — the clock check joins that guard
so a peer independently refuses a window its clock is not inside.

This makes each `time_signature` a genuine "now is inside the window" witness. It
is structured to accept a phase-2 lease predicate beside it (`now ∈ window` **and**
`window ⊆ lease`, a signer-side conjunction — prior-art pattern 4; the caveat is
checked by every signer, not only the judge).

### A5. The two-round commit (quorum rules + non-double-signing safety)

Today the driver runs a **single** gather round: `QuorumRoundStatus` is only
`{Gathering, Authorized}` (`signal-criome/src/schema/lib.rs:1926-1929`) and
`QuorumRoundIdentifier::for_operation` is per-operation, not per-phase
(`signal-criome/src/lib.rs:99-113`). The psyche wants two rounds **now**. Add a
phase dimension (net-new), keeping "sign the same object everywhere" so BLS
aggregation stays clean:

```rust
pub enum RoundPhase { Request, Commit }   // NET-NEW; append-only
```

- **Round 1 — Request.** The existing gather (A-reuse baseline). A **majority**
  (`required = ⌊n/2⌋+1`) signs the request object, **each within the window**
  (A4 clock gate). This is exactly today's `propose → solicit → submit → judge`,
  reused unchanged except that the round now carries `phase = Request`.
- **Round 2 — Commit.** When round 1 reaches a majority, the initiator broadcasts
  a **commit solicitation** carrying the round-1 evidence (the assembled
  `AttestedMoment` + the majority of operation signatures). Each round-2 signer
  **independently VERIFIES a round-1 majority within the window** (re-runs the
  reused judge on the round-1 evidence; checks `now`/window) **before** signing
  the commit object. Round 2 assembles a **majority-of-the-total**
  (`⌊n/2⌋+1`). **Real approval lands only on round 2.**

**Corrected quorum rule (per the locked vision):** round 2 need **NOT** be a
subset of round 1 — it is just a majority of the total. **Stop at two rounds.**
Both rounds must fit the window, so the initiator sizes `closes_at − opens_at`
for two peer round-trips across the voice (A6 deploy windows must budget this).

**The safety condition (carries correctness with no explicit refusal list):** an
honest node **refuses to co-sign a second, CONFLICTING change to the same Criome**
— only one honest successor per state-point. The "state-point" is the Criome
(contract) + its current head (`ContractOperationHead`,
`signal-criome/src/schema/lib.rs`; `AuthorizedObjectKind::Head`, `:1168`). A
change advances `head H → successor S`; two changes are **conflicting** iff they
propose **different successors from the same H**. Having co-signed successor `S1`
from `H` (in either round), an honest node refuses any `S2 ≠ S1` from `H`,
answering the loser with a direct **"refused, resubmit"** (net-new typed reply
`QuorumConflict { at_head, existing_successor }`). Concurrent **compatible**
(commutative, order-independent same end-state) changes may both commit — but the
merge-state machinery is phase-2; **for today, conflicting → refuse the loser.**
The conflict test is kept pluggable so the phase-2 compatible-merge predicate
slots in (D).

### A6. Deploy authorization and the lojix wiring (the whole point)

Criome today authorizes only `AuthorizedObjectKind { Operation, Contract,
Agreement, Time, Head }` (`signal-criome/src/schema/lib.rs:1163-1169`) — a
deployment is none of these. Add it, **appended last** so persisted discriminants
of existing kinds do not shift (`rust-storage-and-wire`):

```rust
pub enum AuthorizedObjectKind {
    Operation, Contract, Agreement, Time, Head,
    Deployment,                       // NET-NEW, appended
}

// the authorized object payload — bound to config + node + window (anti-replay)
pub struct DeploymentAuthorization {
    pub node:    NodeName,            // WHICH node may activate
    pub closure: StorePath,          // WHICH system closure (nix store path = content address)
    pub action:  HostDeployAction,   // SetBootProfile | ActivateNow | TestActivation | ScheduleBootOnce
    pub window:  TimeWindow,          // WHEN (anti-replay via the clock gate)
    pub nonce:   ReplayNonce,         // anti-replay; consumed once
}
```

**Reuse the propose op unchanged.** `ProposeQuorumAuthorization(QuorumProposal)`
already carries an arbitrary `object: AuthorizedObjectReference`
(`signal-criome/src/schema/lib.rs:1937-1942`), and
`AuthorizedObjectReference { component, digest, kind }` (`:1201-1205`) already has
a `ComponentKind::Lojix` (`:653-661`). So authorizing a deployment is:

```
object = AuthorizedObjectReference {
    component: Lojix,
    digest:    blake3(rkyv(DeploymentAuthorization)),
    kind:      Deployment,
}
```

driven through the **same** two-round commit (A5) with the **same** clock gate
(A4). The net-new is only: the `Deployment` kind, the `DeploymentAuthorization`
payload + a durable store for it (net-new `deployment_authorizations` table
alongside `authorization_states`, reusing `authorization_replay_nonces` for the
nonce, `criome/src/tables.rs:35,603-604`), and the two lojix-side items below.

**The lojix wiring.** Today activation is `ssh -o BatchMode=yes root@<node>
"nix-env -p …/system --set <store> && <store>/bin/switch-to-configuration
<switch|boot|test>"` (`lojix/src/schema_runtime.rs:4056-4078`,
`HostActivation::ssh_invocation`), authenticated by the operator's ambient
gpg-agent SSH key. Two changes make Criome the **authority** while SSH stays a
**fallback transport**:

1. **Activation-side gate (target node).** Before `switch-to-configuration`
   runs, the target confirms a valid, in-window `DeploymentAuthorization`
   authorized-object for `{this node, this closure, now}` exists in its Criome
   (the target's criome resolves the authorized-object update the two-round commit
   published, `criome/src/actors/root.rs:1325-1329`). Absent a valid authorization,
   activation is refused — this is what demotes SSH-as-root from *authority* to
   *transport*.
2. **Initiator flow + SSH fallback.** The initiator's `lojix-daemon`, instead of
   authorizing purely by holding an SSH key, first drives a Criome two-round
   commit to produce the `DeploymentAuthorization`, then activates. `nix copy`
   (store transfer, integrity-checked by Nix closure signatures,
   `lojix/src/schema_runtime.rs:3957-3965`) may remain over ssh-ng for today; the
   router **payload lane** for the closure is phase-2. **SSH is retained as a
   typed fallback** (`typed-records-over-flags`: an explicit
   `ActivationAuthority { Criome | SshFallback }`, not a silent bypass) for when
   the Criome authorization is unavailable — the auditor must confirm the fallback
   is a deliberate, logged degradation, never an implicit skip of the Criome gate.

### A7. Soundness arguments

**Model.** `n` cohort members; at most `f` faulty with `f < n/2` (honest strict
majority). Round-1 quorum and round-2 quorum are each a majority-of-total
(`> n/2`). Two sub-models: **non-equivocating minority** (faulty nodes may be
unavailable / drop messages but never emit a signature over a state they did not
honestly reach) and **Byzantine minority** (faulty nodes may equivocate).

**(i) Two-round + non-double-signing safety (single successor per state-point).**
Every honest node obeys the single-successor rule (A5): at most one co-signed
successor per `(Criome, head H)`. Suppose two conflicting successors `S1 ≠ S2`
from the same `H` both reach a committed round-2 majority `M1`, `M2`.

- *Non-equivocating minority.* Faulty nodes emit no signatures, so `M1`, `M2` are
  honest-only sets, each `> n/2`, drawn from the `≥ n − f > n/2` available honest
  nodes. Two subsets of the honest set each larger than `n/2` intersect in an
  honest node, who by the single-successor rule cannot have signed both `S1` and
  `S2`. Contradiction ⇒ at most one successor commits. **Non-equivocation holds.**
- *n = 2 (today's two standing nodes, 2-of-2).* Majority-of-total `= 2 =
  unanimous`, so **every** commit needs both nodes; a single honest node vetoes any
  conflicting successor. **Safety is strong even against one Byzantine node**
  (liveness then requires both nodes up — an acceptable, explicit trade for a
  2-node cluster).
- *Byzantine minority at n ≥ 3 (honest verdict).* Majority-of-total does **not**
  force a common **honest** signer: at 2-of-3 with one Byzantine node, that node
  can be the intersection and sign both `{byz, A}→S1` and `{byz, B}→S2` (A, B
  honest, distinct), so two conflicting successors commit. Byzantine
  non-equivocation at `n ≥ 3` requires **supermajority** quorums (`2f+1` of
  `3f+1`), not majority-of-total. **This is a real limit of the locked
  majority-of-total rule and is flagged as a decision (risk R1).** Round 2's own
  job is narrower and still holds: because each round-2 signer verified a **real**
  round-1 majority within the window, a dishonest *proposer* cannot pass off a
  "committed" authorization that never had a genuine round-1 majority — "real
  approval lands only on round 2."

**Conclusion.** For **today's 2-of-2** the two-round + single-successor design is
**safe (non-equivocating, in fact veto-strong)**; liveness needs both nodes. For
`n ≥ 3` under a non-equivocating minority it remains safe; under a Byzantine
minority it needs supermajority sizing (R1).

**(ii) Witness-clock gate.** Assume `≥ ⌈(n+1)/2⌉` honest signers, each with a
clock within skew `δ` of true time, and each emits its `time_signature` only when
its own clock lies in `[opens_at, closes_at]` (A4). A valid `AttestedMoment`
requires a strict majority of real BLS time-signatures over the
`AttestedMomentStatement` (`criome/src/language.rs:620-654`). A strict majority
necessarily includes at least one honest signer; that signer's clock was inside
`[opens_at, closes_at]` at signing time, so **true time was within
`[opens_at − δ, closes_at + δ]` when the moment was assembled.** A proposer can no
longer manufacture "now" by choosing a convenient window, because honest signers
refuse windows their clocks are not inside; the robust consensus "now" is the
intersection/median of honest signer windows (CometBFT BFT-Time), which a faulty
minority cannot drag outside the honest range. Without the gate (today's code)
none of this holds — the co-signed window proves only agreement on a *value*, not
on *time*.

## Part B — Build plan

Repo-grouped, dependency-ordered, bead-decomposable. Each item is **TODAY** or
**PHASE-2** and cites its real touch-point. The dependency spine is:
G1 (schema + migration) → G2 (founding) and G3 (clock gate) in parallel → G4
(two-round) → G5 (deploy-auth) → G6 (lojix) → G7 (live proof). G3 and G5-schema
have no dependency on G2 and can start immediately.

### G1 — Contract schema + digest migration (TODAY, blocks all)

- **G1.1 `parent` field.** Add `ContractParent { Root | Parent(ContractDigest) }`
  and change `Contract(Rule)` → `Contract { rule, parent }`
  (`signal-criome/src/schema/lib.rs:725`). Update the NOTA
  encode/decode derives, the rkyv archive, `Rule::referenced_digests`
  traversal awareness, and `Contract::digest()` callers
  (`signal-criome/src/lib.rs:160-163`). Bead: schema-parent-field.
- **G1.2 Storage-schema bump + genesis guard.** Bump the `contracts` table schema
  version (`criome/src/tables.rs:36,605`); add a startup guard that refuses/finds-
  empty any pre-`parent` contract rows. Bead: storage-parent-bump.
- **G1.3 Digest-migration decision + operational precondition.** Confirm the two
  standing nodes' `contracts` tables hold nothing that must survive (clean-genesis
  path, A1). If they do, escalate to the re-digest-map fallback (separate epic).
  Bead: migration-precondition-check.
- **G1.4 Nix seed recompute.** Recompute `quorumContracts` seed digests under the
  new schema in the deploy modules (mirror deploy `peerIdentitySeeds` /
  `quorumContracts`). Bead: nix-seed-recompute.
- **Version surface:** minor bump on `signal-criome` (breaking wire, pre-1.0) +
  daemon `criome` bump (consumes changed contract) + storage-schema version
  (`versioning`, `rust-storage-and-wire`).

### G2 — Founding ceremony (TODAY)

- **G2.1 `RootGenesis` + founding certificate types** (`signal-criome`): the
  `RootGenesis`, `FoundingMember`, `FoundingSignature`, `RootFoundingStatement`,
  `RootAnchorDigest` types + round-trip codec tests (`contract-repo`: examples
  first, assert binary + NOTA). Bead: founding-cert-types.
- **G2.2 `ObserveNodePublicKey` public op** (`signal-criome` + `criome` root
  handler) so the client can display the Criome pubkey. Bead: observe-node-pubkey.
- **G2.3 `AcceptRootFounding` meta-op** (`meta-signal-criome/src/schema/lib.rs`
  alongside `Configure:236`) — the explicit owner accept, no auto-approval. Bead:
  meta-accept-founding.
- **G2.4 Founding driver + `root_founding` durable table** (`criome/src/actors/
  root.rs`, `criome/src/tables.rs`): build proposal, convey over
  `RouterQuorumVoice` (`criome/src/voice.rs:124`), accumulate signatures to
  **unanimity**, persist, seed identity registry from `founding_keys` (replacing
  the single-key `ClusterRoot` seed, `criome/src/admission.rs:74`). Two knobs:
  collection window, post-founding cooldown. Bead: founding-driver.
- **G2.5 Reboot verify-not-refound** on start (`criome/src/actors/root.rs:199-208`
  reconcile path): verify persisted anchor; never re-found. Bead:
  reboot-anchor-verify.

### G3 — Per-signer witness-clock gate (TODAY, small, high-value; parallel to G2)

- **G3.1 Clock gate in `sign_quorum_vote`** (`criome/src/actors/signer.rs:344-368`):
  read `SystemClock` (`criome/src/master_key.rs:222`), refuse when `now ∉ window`
  with `OutsideTimeWindow` (`signal-criome/src/schema/lib.rs:1143`). Bead:
  signer-clock-gate.
- **G3.2 Peer window re-check** join `proposition_matches_members`
  (`criome/src/actors/root.rs:1477-1487`) so a peer independently refuses an
  out-of-clock window. Bead: peer-window-recheck.
- **G3.3 Tests:** mock-clock inside/outside window ⇒ sign/refuse; a proposer's
  convenient future window is refused by honest signers. Bead: clock-gate-tests.
- Structured to accept a phase-2 lease conjunction (`window ⊆ lease`).

### G4 — Two-round commit (TODAY; the largest net-new; depends on G3)

- **G4.1 `RoundPhase { Request, Commit }`** + phase-aware round key /
  `QuorumRoundStatus` (`signal-criome/src/schema/lib.rs:1926,1937-1969`). Bead:
  round-phase-types.
- **G4.2 Commit solicitation + round-1 verification** (`criome/src/actors/
  root.rs`): after a round-1 majority, broadcast round-1 evidence; each round-2
  signer re-runs the reused judge on it within the window before signing the
  commit object. Bead: commit-round-driver.
- **G4.3 Single-successor safety + `QuorumConflict` reply** (A5): track co-signed
  successor per `(Criome, head)`; refuse `S2 ≠ S1` from same `H` with
  "refused, resubmit". Keep the conflict predicate pluggable for phase-2
  commutative merge. Bead: single-successor-guard.
- **G4.4 Quorum sizing decision (R1):** majority-of-total for `n = 2` today;
  document the supermajority requirement for Byzantine safety at `n ≥ 3`. Bead:
  quorum-sizing-note.

### G5 — Deploy authorization object (TODAY; schema parallel to G2/G3)

- **G5.1 `AuthorizedObjectKind::Deployment`** appended last
  (`signal-criome/src/schema/lib.rs:1163`) + `DeploymentAuthorization` payload +
  round-trip tests. Bead: deploy-auth-types.
- **G5.2 Durable `deployment_authorizations` table** + nonce anti-replay reuse
  (`criome/src/tables.rs:35,603-604`). Bead: deploy-auth-store.
- **G5.3 Drive via existing propose op:** deployment rides
  `ProposeQuorumAuthorization` with `object.kind = Deployment`, `component = Lojix`
  (no new propose op). Publish the authorized-object update on commit
  (`criome/src/actors/root.rs:1325-1329`). Bead: deploy-auth-drive.

### G6 — lojix activation wiring (TODAY; depends on G5)

- **G6.1 Activation-side gate (target)** in the switch path
  (`lojix/src/schema_runtime.rs:4056-4078`, `HostActivation::ssh_invocation`):
  require a valid in-window `DeploymentAuthorization` for `{this node, this
  closure, now}` before `switch-to-configuration`. Bead: lojix-activation-gate.
- **G6.2 Initiator drives Criome auth + typed SSH fallback:** `lojix-daemon`
  obtains the Criome authorization, then activates; `ActivationAuthority { Criome |
  SshFallback }` (`typed-records-over-flags`) keeps SSH a deliberate, logged
  degradation, never an implicit skip. Bead: lojix-criome-authority.
- **G6.3 Version surface:** `signal-lojix` + `lojix` bumps; deploy-slot note
  (`versioning`).

### G7 — Live proof (TODAY, gated on psyche go-ahead)

- End-to-end on the two standing nodes: found root → authorize one deploy →
  activate over Criome authority with SSH fallback. Bead: live-two-node-proof.

### Security properties an auditor must verify

1. **Clock gate:** signer refuses the `time_signature` when `now ∉ window`
   (mock-clock test); a proposer-chosen convenient window is refused by honest
   signers (A4, G3).
2. **Two-round integrity:** a round-2 signer verifies a *real* round-1 majority
   within the window before committing; a forged/short/out-of-window round-1 is
   refused (A5, G4.2).
3. **Non-equivocation:** an honest node refuses a second conflicting successor at
   the same `(Criome, head)`; the loser gets "refused, resubmit"; and the
   **quorum-sizing caveat R1** (majority-of-total is Byzantine-unsafe at `n ≥ 3`)
   is explicitly acknowledged in the deployed configuration (A5, A7-i, G4).
4. **Founding:** unanimity required; explicit owner accept only (no auto-approval);
   the anchor commits to the founding keys; founding signatures are ATTACHED, not
   folded into the hash; reboot verifies and never re-founds (A2, A3, G2).
5. **Deploy-auth binding:** authorization bound to `{node, closure, window,
   nonce}`; replay outside the window, on the wrong node, or after nonce
   consumption is refused (A6, G5).
6. **Transport identity:** every solicitation/vote/commit rides the router's
   Criome-rooted authenticated, forward-secret session; a peer whose identity→key
   binding is absent fails `UnknownSigner` (`router/src/identity_proof.rs`).
7. **Fail-closed everywhere:** missing store/registry/contract/authorization ⇒ not
   authorized (reused judge; A6 gate).
8. **SSH fallback is a typed, logged degradation**, never a silent bypass of the
   Criome authority (A6, G6.2).
9. **Digest migration:** no live contract silently mis-digests; the clean-genesis
   precondition was verified or the re-digest map rewrote every reference (A1,
   G1.3).

## Part C — Feasibility verdict

**Can we deploy today on the two standing nodes?** Yes in principle, at 2-of-2,
via a scoped path — but it is a **multi-group build, not a single-sitting change**,
and one group (two-round commit) is the swing risk. The good news the scout found
holds: the judge, the durable quorum driver, the router identity+transport, the
moment/clock infrastructure, the anti-replay store, and the `Contract` type all
already exist, so the net-new surface is genuinely small.

**Tightest realistic end-to-end path** (found root → authorize one deploy →
activate over Criome with SSH fallback):

1. **G1** land `parent` + clean-genesis storage bump (precondition: standing
   nodes' `contracts` tables hold nothing to preserve — verify first, G1.3).
2. **G3** the per-signer clock gate — small, localized (`signer.rs` +
   `root.rs` guard + one existing refusal reason). Highest value per line; do it
   early.
3. **G2** the founding ceremony to found the 2-of-2 root and seed the registry
   from the founding key-set.
4. **G5 + G6** the `Deployment` kind + `DeploymentAuthorization` + lojix
   activation gate + typed SSH fallback — modest, because it reuses the existing
   propose op, `ComponentKind::Lojix`, and the anti-replay store.
5. **G4** the two-round commit — **the biggest net-new and the item most at risk
   of slipping.**

**What must slip for "today" to hold, honestly:**

- **The second round is the swing item.** At 2-of-2 the *already-built* single
  gather round is **unanimous** and therefore veto-strong (A7-i), so the first
  live deploy can, if the day is tight, ride the existing single-gather path and
  land the second round as an immediate fast-follow. The psyche wants two rounds
  now; the honest statement is that founding + clock-gate + deploy-auth + the
  existing single-gather at 2-of-2 is the minimum that *authorizes a deploy over
  Criome today*, and the second round is the piece that may need to trail by a day
  without blocking the live proof.
- **Deploy transport stays on ssh-ng today.** `nix copy` remains over SSH; only
  the **authority** moves to Criome (target refuses activation without a valid
  in-window authorization). The router payload lane for the closure is phase-2.
  This still delivers "Criome is the deployment-authorization layer, SSH is
  fallback" — the whole point — without the phase-2 payload lane.
- **Rotation, sub-quorum gathering, leasing, sparse replication all slip to
  phase-2** and are not on the two-node deploy path.

**The one honest correctness caveat (R1):** the locked "majority-of-total
guarantees honest overlap" rule is **sound at 2-of-2 (today's target)** and under
a non-equivocating minority generally, but is **not** Byzantine-safe at `n ≥ 3`
(that needs supermajority `2f+1`-of-`3f+1`). This does not block today's two-node
deploy; it is a sizing decision to settle before the cluster grows past two nodes.

**Biggest risks / decisions (report):**

- **R1 — Quorum sizing vs. Byzantine safety at n ≥ 3.** Majority-of-total is
  veto-strong at 2-of-2 but not Byzantine-non-equivocating at 3+. Decide: accept
  the non-equivocating-minority model for small permissioned clusters, or move to
  supermajority quorums before growing. (Does not block today.)
- **R2 — Digest migration precondition.** Clean genesis is correct only if the
  standing nodes hold no durable contract that must survive. Verify before the
  ceremony; otherwise the re-digest-map fallback cascades to every
  `ContractDigest` reference (identities, object-members, Nix seeds).
- **R3 — Does the hashed anchor commit to keys, or only the attached signatures?**
  The spec bakes the founding key-set into `RootGenesis` so the anchor itself
  commits to keys (strong reading of concept 2). Confirm this is the intended
  self-certification strength versus the weaker "anchor commits to identity names,
  keys bound via registry" model.
- **R4 — Two-round scope for the first live deploy.** Land full two-round now, or
  ship the first live proof on the existing unanimous single gather at 2-of-2 and
  fast-follow the commit round? (Liveness/schedule call.)
- **R5 — How far does "Criome as deploy authority" go today?** Authority-only
  (target refuses un-authorized activation, transport stays SSH) is achievable;
  full SSH-transport removal is phase-2. Confirm authority-only is "operational
  enough" for the day.

## Part D — Phase-2 forward-compatibility notes (design so nothing forecloses these)

- **Time-leased self-ownership.** Add an `expires`/lease to the Criome unit;
  revert-on-lapse is **passive LOCAL expiry** (a stale self-grant fails to
  validate — TUF/ACME/Vault model), **never broadcast revocation**. `window ⊆
  lease` is a **signer-side refusal** slotted beside the A4 clock gate (structure
  G3 so a second predicate joins the same guard). A sub-Criome voting elsewhere is
  **not** mutating its own state, so its lease does **not** gate that vote.
- **Sub-Criome as a quorum member.** `PolicyMember::ObjectMember(ContractDigest)`
  already exists (`signal-criome/src/schema/lib.rs:781`) and the judge already
  evaluates nested contracts; only the gather driver excludes it
  (`criome/src/actors/root.rs:1466-1469`). Keep "sign-same-object-everywhere" (A5)
  and add a **participation-set bitmap**, not recursive sub-certificates over
  different messages. **Membership ≠ parentage** — any Criome may be a member of
  any other's quorum without being its child; this enlarges the sparse-sync
  closure to *ancestors ∪ referenced-member-Criomes-and-their-ancestors*. The host
  keeps unilateral power to drop a bad member via its own quorum; enforce acyclic
  or depth-bounded evaluation. Do **not** shape the round protocol to hard-exclude
  `ObjectMember`.
- **Commutative-merge concurrency.** Today's conflict test (A5, "different
  successor from same head") is kept **pluggable** so the phase-2 "compatible
  (commutative, same end-state) → both commit" predicate replaces the "refuse the
  loser" branch without touching the round machinery.
- **Cold/hardware-wallet root keys.** BLS aggregation is poorly supported on
  consumer wallets, which favor Ed25519/secp256k1 — a likely **scheme split**.
  Keep the founding-signature path **scheme-tagged** (`SignatureEnvelope.scheme`),
  so the root can be founded/rotated under a non-BLS scheme while ordinary quorum
  aggregation stays BLS. Do not hardcode BLS in the founding-statement
  verification beyond what today needs.
- **Sparse replication.** Hold only the needed closure (object + ancestor `parent`
  chain + each parent's founding/anchor slice up to the baked-in anchor — KERI KEL
  replay model). Today full replication is fine; the `parent` chain + attached
  founding certificate (A2) are exactly the ancestor slice a future sparse node
  replays. Pair with an anti-rollback signed head so integrity does not masquerade
  as currency.
- **Second, parent-revocable ownership type.** Keep ownership modeled as an
  extensible enum so a parent-revocable variant can join the default self-owned
  one without reshaping the unit.
- **Rotation (old+new co-sign).** Root mutation/rotation is **threshold-quorum,
  deliberately NOT unanimous** (one lost node must never freeze the root, A4-of the
  vision). Sign every membership transition by a threshold of **both** the outgoing
  and incoming quorum (TUF root rotation / KERI pre-rotation) so a node holding the
  old anchor validates forward. Specced today; not on the two-node deploy path.
- **Universal-lease dead-state (zombie) handling.** Leave the lease-expiry path so
  a fully-lapsed Criome can be reaped; phase-2.
