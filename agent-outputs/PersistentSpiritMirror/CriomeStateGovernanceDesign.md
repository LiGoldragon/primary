# Criome State Governance — one primitive: the quorum-authorized state change

Design only; no code repo was edited and no tracker item was mutated.
Lane: CriomeClusterPropagation / criome-state-governance-design.
Written 2026-07-07.

This document answers how criome governs its OWN state — how new criomes
(accounts) come to exist, where data such as the mirror-target list
lives, how consumers learn that state and hear it change, and how the
whole history stays bounded. It composes with two sibling documents in
this directory: `ClusterAuthorizationSliceDesign.md` (how the cluster
quorum gates acceptance of a component's state; its §5 is subsumed in
framing by this design, see §9) and
`ComponentMirroringCapabilityDesign.md` (how state-bearing components
mirror; amended alongside this design for privacy silos and for the
mirror-target list moving here).

The psyche set the direction this session. His words, verbatim, are the
constraints:

> "Any new contract needs to be proposed through a parent quorum. A new
> contract is a state change."

> "As long as we don't accumulate all the parent contracts forever. I'm
> not building another infinitely-sprawling blockchain."

> "criome needs two states; the accounts (what in my multi-year vision
> I called the criomes, hence the name (cryptographic biomes)), and the
> state they refer to."

> "the list of mirrors is in spirit, changes gated in criome. just
> another log, like the privacy silos."

And he resolved the naming: **rename `Contract` to `Criome` — the
account is the criome.** This design is written in that vocabulary as
settled; the mechanical rename is a slice (§10, §11).

## 0 · Terms

Plain definitions, used throughout:

- **criome (lowercase)** — the identity and authorization program that
  runs on every host. All cryptography is its domain. Each host runs
  exactly one.
- **Criome (the record; capitalized here for the type)** — one account:
  a tiny content-addressed record of exactly two fields, a **rule** and
  a **parent**. This is the type named `Contract` in today's code; the
  rename is settled (§10). The name comes from the psyche's multi-year
  vision: each account is a *cryptographic biome* — a bounded domain of
  authority. The criome program keeps Criome records; when this
  document says "an account" or "a criome," it means one such record.
- **Rule** — the account's transition policy: who must sign, with what
  threshold, under what timing, for a change under this account to be
  authorized. A closed set of typed rule forms (signatures, thresholds,
  compositions, time windows).
- **Parent** — either the sentinel `Root` (the account is the one
  global root, its own origin) or a reference to another account's
  digest. Every account chains to the root.
- **Digest** — a cryptographic fingerprint of content. Accounts are
  content-addressed: an account's digest is computed from its rule and
  parent, so the same account has the same identity everywhere and
  cannot be silently altered.
- **Founding** — the one ceremony that creates the root account: the
  founding nodes' master keys sign unanimously, acceptance is an
  explicit owner-gated act, and the resulting **founding anchor** (a
  digest committing to the founding keys) is the trust root every
  verifier pins. Founding is the only account birth that is not a
  proposed state change (§4).
- **Quorum** — the members named by an account's rule. The **two-round
  commit** is the built mechanism by which a quorum authorizes one
  proposed digest: a first-round majority opens a second round; a
  second-round majority authorizes.
- **Grant and evidence** — the quorum's signed yes for one proposed
  digest, plus the member signatures that let any other criome verify
  the acceptance independently.
- **Head** — for any hash-chained sequence (a component's log, a slot's
  value chain), the digest of the newest state. A **head advance** is a
  change from the current head to a proposed successor.
- **Governed state slot** — this design's central noun: one named piece
  of state governed by an account. Every slot has a current head, and
  every change to it is the same proposal → quorum → grant primitive
  (§3, §5).
- **Working socket / meta socket** — criome's two local sockets: the
  working socket (group-accessible) carries ordinary requests; the meta
  socket (owner-only, mode 0600) carries owner acts such as the
  founding accept.
- **Host policy** — per-host criome configuration that is not account
  state: today the authorization mode (auto-approve for development,
  explicit approval, or quorum). Policy says how THIS host behaves;
  accounts say what the cluster authorizes (§8).
- **The everywhere-gate** — the landed acceptance semantic from
  `ClusterAuthorizationSliceDesign.md`: when criome authorization is
  enabled, an operation is accepted only when the quorum grants its
  proposed head digest; refused operations are recorded nowhere,
  including locally.
- **Non-authoritative remote** — a host running criome plus a mirrored
  component that follows the cluster's state by verifying evidence but
  is not a quorum member and can never authorize anything.
- **Privacy silo** — a separate log per privacy class inside a
  state-bearing component; designed in
  `ComponentMirroringCapabilityDesign.md` §5 (amended), with its
  governance consequences here (§5.3, §11 slice G6).
- **Mirror-list log** — spirit's own log holding the mirror-target
  list: one more log beside the privacy silos, whose head advances
  through the same quorum gate as any other (§5.3). Criome holds only
  its head and evidence, never its content.

## 1 · Ground truth (verified against source, 2026-07-07)

Checkouts under `/home/li/primary/repos/`: criome `0a96a23` (0.8.0),
signal-criome `7436072`, spirit `1698cba`, signal-spirit `eba2afe`,
sema-engine `7cfcece` (0.7.0).

- **The account record is already rule + parent, content-addressed, no
  payload.** `Contract { rule, contract_parent }`
  (signal-criome `src/schema/lib.rs:789-792`); parent is
  `Root | Parent(ContractDigest)` (`:778-781`); the digest is computed
  from these two fields. There is no payload field and no distribution
  mechanism — each node derives records locally; a peer asking for an
  absent one receives a plain `ContractMissing` reply, with no
  auto-backfill.
- **Rule is a closed 11-variant enum** (signal-criome
  `schema/lib.schema:303-315`): `SignedBy`, `All`, `Any`, `Threshold`,
  `Workflow`, `Composition`, `ActiveAfter`, `ActiveUntil`,
  `TimeSwitch`, `Agreement`, and the bare variant `EscalateToPsyche`
  (no payload, no comment). §8 removes the last.
- **The admission hole is real.** `admit_contract`
  (criome `src/actors/root.rs:1899-1913`), reached by
  `CriomeRequest::AdmitContract` on the WORKING socket (group
  accessible, mode 0660), stores any record whose referenced digests
  resolve and whose rule shape is valid
  (`language.rs:246-255`). No signature, no quorum, no evidence. Any
  local process with socket access can admit an account today. §4
  closes this.
- **Nothing is ever pruned.** Accounts are stored append-only
  (`store.rs:837`); no deletion, eviction, or garbage collection path
  exists anywhere in criome. §6 changes this deliberately.
- **Spirit's mirror target today is one owner-configured address,
  criome uninvolved**: `SelectedMirrorTarget` on the meta `Configure`
  input (meta-signal-spirit `schema/meta-signal.schema:27-41`), applied
  at `spirit/src/shipper.rs:70`. §7 replaces this with governed state.
- **Spirit's privacy vocabulary**: every record carries `Privacy`, a
  newtype over the ordered 8-variant `Magnitude` enum
  (`Zero … Maximum`), with `AtMost`/`AtLeast` query selections
  (signal-spirit `schema/signal.schema:196,230,263`). The silo set
  (§5.3) draws on this.
- **A push subscription mechanism already exists**: the
  `SubscriptionRegistry` actor (criome `src/actors/subscription.rs`)
  serves `ObserveAuthorizedObjects`, pushing typed updates to
  registered interests over a long-lived stream. Noted for
  completeness — this design turned out to need no new subscription
  (§7): the mirror list lives with its consumer.
- **The everywhere-gate has LANDED on the mains** (this design's
  baseline, not a pending assumption): spirit has the durable staging
  seam and crash recovery (`engine.rs:850`, `daemon.rs:143-153`, behind
  the `criome-gate` feature), signal-spirit carries
  `AdvanceRefused` with the closed four-reason enum
  (`signal.schema:45,101,137`), and criome 0.8.0 replaced the catch-up
  stage with dead-round supersession (`root.rs:157,235-239,1303`).
- **`AuthorizedObjectKind` is a closed 5-variant enum**
  (`lib.schema:524`): `Operation Contract Agreement Time Head`. §5's
  slot vocabulary replaces the ad-hoc pair (kind, component) for
  governed state.

## 2 · The two layers: criomes, and the state they refer to

Criome needs two states, and this design keeps them strictly apart.

**Layer one — the accounts (the criomes).** Tiny content-addressed
records of rule + parent, forming a tree rooted at the founding. An
account holds no data. It is pure authority: WHO may change WHAT lies
below it, expressed by its rule. Accounts are small (two fields), they
change rarely (a membership rotation, a policy amendment), and they
must be replicated widely — every verifier of anything needs the
accounts on the path from the root to the state it is verifying.

**Layer two — the referred state.** The data each account governs:
spirit's intent log, the mirror-target list, the set of an account's
own live children. Referred state is where the bulk lives. It changes
constantly, it is replicated sparsely (each host holds what it serves;
a remote holds what it follows), and — the heart of §6 — it is kept as
*current value plus the evidence needed to verify it*, with everything
superseded prunable.

The psyche invoked Solana and Tezos as the reference models, and the
shape they share is exactly this split: data lives as state governed by
rules; rules gate every transition; the rules are themselves state,
amended through governed proposals (Tezos amends its own protocol by
on-chain vote; Solana's programs are accounts upgraded under an
authority). Nobody stuffs data into the consensus rule object — the
rule object stays tiny and the data it governs lives beside it, under
it. We take that governance shape and deliberately refuse their history
model: those systems keep every transition forever because strangers
must be able to verify from genesis. Our trust root is an owner-pinned
founding anchor and a closed membership, which is what makes §6's
pruning sound.

The replication consequence, stated once and used everywhere below:
**accounts are small, slow-changing, and travel wide; referred state is
bulky, fast-changing, sparse, and prunable.** Anything that would make
an account bulky (a target list, a data payload) is in the wrong layer.

## 3 · The one primitive

There is exactly one way anything changes: **a proposal, authorized by
the governing account's quorum through the two-round commit, producing
a grant with evidence.** This is the same mechanism that already gates
spirit's head advances under the everywhere-gate. This design adds no
second mechanism; it widens what the one mechanism governs.

### 3.1 · Governed state slots

Every piece of referred state is a **slot**: a named, typed piece of
state under one governing account. The slot vocabulary is a closed enum
(no strings for fixed sets, per settled intent):

```
GovernedSlot [
  Children                                    -- the set of live child accounts
  (ComponentHead ComponentKind ComponentLog)  -- one component log's head
]

ComponentLog [
  (Silo PrivacySilo)  -- one privacy silo's chain
  MirrorTargets       -- the component's mirror-list log
]
```

(Pseudo-schema; exact NOTA form at implementation. `PrivacySilo` is the
closed silo set of §5.3; until silos land, one `Primary` silo keeps the
shape total. The log labels are opaque to criome — it keys separate
chains by them and knows nothing of what "private" or "mirror" means.
Both enums grow by recompilation when a new kind of governed state or
log is born — exactly like `ComponentKind`.)

A slot is addressed by the pair **(governing account digest, slot)**.
Every slot has a **current head**: for a component log, the log's chain
head; for the criome-held child-set value, the digest of the current
value, chained to its predecessor by the same successor-row machinery
the head chain already uses. The per-account
head rows, anti-equivocation rows, and dead-round supersession that
landed in criome 0.8.0 generalize from "per account" to "per (account,
slot)" — the same code, one more key column.

### 3.2 · Every change, one table

| What changes | Which slot | Who authorizes |
|---|---|---|
| A component records / supersedes / retires (a log head advance) | `(ComponentHead kind (Silo …))` under the operational account | The operational account's quorum (as today, landed) |
| The mirror-target list gains or loses a target | `(ComponentHead kind MirrorTargets)` — the component's own mirror-list log advances | The operational account's quorum — the same gate as any advance |
| A new account is issued | `Children` of the parent account | The PARENT's quorum |
| An account is superseded (rotation, rule change) | `Children` of the parent account | The parent's quorum |
| The root account itself rotates | The root's own succession | The root quorum (threshold, not unanimous — settled) |
| The root account is born | Nothing — the founding ceremony | Unanimous founding signatures, explicit owner-gated accept |

Two readings of this table matter:

**A new account is a state change.** Issuing an account is not a
special admission verb; it is an ordinary proposal against the parent's
`Children` slot, whose proposed new value is the child set including
the new account's digest. The account record itself is content the new
head commits to, exactly as a log entry is content a component head
commits to. The founding ceremony is the ONLY account birth that is not
a proposed state change — it is the axiom the whole tree rests on.

**Rules are state.** An account's rule gates transitions beneath it;
to change the rule, you supersede the account through its PARENT's
`Children` slot — a proposal like any other, judged by the parent's
rule. Rules gate state; rules are themselves state amended through
proposals; the regress terminates at the root, whose own succession is
governed by its own rule, born at founding. This is the Tezos shape,
without the ledger.

### 3.3 · What the rule does today, honestly

Today the quorum members auto-approve every well-formed proposal;
approval predicates (lineage checks, thresholds beyond membership, veto
logic) remain explicitly out of scope, as settled. The account's rule
is where such predicates will live when they are wanted; this design
gives them a seat, not an implementation. Until then, what actually
protects each slot is: membership (only the quorum's members can
complete a round), the everywhere-gate (nothing unauthorized is ever
recorded), anti-equivocation (one successor per (account, slot, head)),
and host policy (§8) — with the safe defaults of §5.4.

## 4 · The account layer: issuance, supersession, and closing the hole

### 4.1 · Issuance

To issue an account (for example, the root issuing the operational
cluster account):

1. A caller proposes, against the parent's `Children` slot: current
   head H, proposed successor D = digest of the new child-set value,
   carrying the new value itself (the child set, naming the new
   account's digest) and the new account record.
2. The parent's quorum runs the ordinary two-round commit on D. Members
   judge exactly what they judge for any proposal (well-formedness,
   window, anti-equivocation; predicates later, per §3.3), plus host
   policy (§5.4: account-layer changes default to explicit approval).
3. On the grant, each member's criome stores: the new `Children` value,
   the new account record, and the grant evidence — atomically, as the
   slot's new current state.
4. A member that was offline for the round catches up on the next
   verified push it receives — the newest grant covers what it slept
   through (§6.3).

### 4.2 · Supersession

Superseding an account (membership rotation, rule change) is the same
proposal with a child-set value that replaces the old account's digest
with the new one. Two consequences need naming:

- **Slot adoption.** The replaced account's slots (the operational
  account's `ComponentHead` rows — every component log, the mirror-list
  log among them) must continue under the successor. The superseding proposal carries, beside the new
  account, the adoption list: for each slot of the replaced account,
  the current head the successor starts from. Verification of any later
  advance chains through the adoption grant. One round covers the
  account swap and every adoption atomically (the multi-slot round of
  §5.2 is the same machinery).
- **The dead account prunes.** Once the `Children` head has advanced
  past it, the replaced account is unreachable from the live tree and
  carries no authority; §6 discards it.

### 4.3 · Closing the unauthenticated admission hole

Today any local process on the working socket can admit a well-shaped
account with no evidence (`root.rs:1899-1913`; ground truth §1). Under
this design, "admit an account" stops being a free-standing verb,
because account existence is a governed state change. The working
socket keeps exactly three ways an account record enters a node's
store:

1. **Founding** — the ceremony, on the meta socket, owner-gated,
   unchanged.
2. **Voting** — a member stores what it co-signed: the account arrives
   as the content of a `Children` proposal it judged.
3. **Evidence-carried admission** — the replacement for
   `AdmitContract`: the request carries the account record TOGETHER
   WITH the grant evidence of the `Children` round that created it;
   criome verifies the evidence against the (already admitted) parent
   before storing. This is the same acceptance-by-verification path the
   receiving-side check of `ClusterAuthorizationSliceDesign.md` §4.2
   runs for component state, applied to the account layer. It serves
   offline members catching up and non-authoritative remotes enrolling.

The structure-check-only `AdmitContract` dies. `LookupContract` and the
`ContractMissing` negative reply survive (renamed per §10) as the read
path by which a peer fetches account records it is missing — records
whose admission still requires evidence.

## 5 · Governed slot state: storage, values, rounds

### 5.1 · Criome-held and component-held slots

Every slot is a digest chain governed by criome; slots differ in who
materializes the content:

- **The one criome-held slot** (`Children`): the accounts are criome's
  own state, so the proposal carries the proposed new child-set value
  and criome stores the current value beside the head and evidence.
  Only the current value is stored; predecessor values prune on
  advance (§6).
- **Component-held slots** (every `ComponentHead`, the mirror-list log
  included): the content lives in the component; criome stores only
  the current head and the newest evidence, exactly as the landed gate
  already does. Where referred state LIVES is a placement choice made
  per state — the governance is uniform either way. The psyche placed
  the mirror list with its consumer: in spirit.

### 5.2 · Multi-slot rounds

A proposal normally binds one slot's successor digest. Two named cases
need one round to advance several slots atomically:

- account supersession with slot adoption (§4.2);
- a cross-silo record move (a record's privacy reclassification that
  crosses a silo boundary): the source silo appends the removal, the
  destination silo appends the record, and neither must exist without
  the other.

Design: a proposal may bind a small ordered set of (slot, current head,
successor digest) triples; the round commits all or none; each member's
admission check claims the anti-equivocation row in every named slot
before signing (the same durable-first discipline, over a set). Cost,
honestly: the admission check and the row schema gain a set dimension,
and a multi-slot proposal holds several slots' rows for one window —
acceptable because multi-slot rounds are rare (rotations, moves), and
refusal of any one row refuses the whole proposal, fail-closed. The
alternative — two ordered single-slot rounds with a compensation step
if the second refuses — was rejected: compensation (un-retiring a
record) is a special case that the atomic round dissolves.

### 5.3 · The mirror-target list, concretely (the first named log)

The psyche placed it, verbatim: "the list of mirrors is in spirit,
changes gated in criome. just another log, like the privacy silos."

So the mirror-target list is quorum-governed STATE, and it lives IN
SPIRIT — not a field of any account record (the account stays rule +
parent), not per-host configuration (spirit's `SelectedMirrorTarget`
dies, §7), and not a value criome holds. Spirit keeps a **mirror-list
log**: one more hash-chained log beside its privacy silos, holding the
current target mapping. Criome's involvement is exactly what it is for
every log: the head of `(ComponentHead Spirit MirrorTargets)` advances
only through the quorum gate, and criome retains that head plus the
newest evidence, nothing more.

- **Value shape** (the working assumption, stated for correction): a
  mapping **silo → target hosts** — for each privacy silo, the Criome
  host IDs (each a host criome's master public key, the only network
  identifier) of the non-authoritative remotes that receive that
  silo's chain. The public silo may map to untrusted backup hosts;
  private silos only to trusted ones. Quorum members are never listed
  — membership lives in the operational account's rule, and members
  receive everything by virtue of the propagation design. No reason
  was found for a different shape; if one appears (for example a
  per-target property that is not silo membership), the mapping
  transposes without touching the governance.
- **Changing it**: an ordinary working operation on spirit — append a
  new mapping to the mirror-list log. It runs the SAME intake path as
  recording an intent: stage, ask criome to authorize the mirror-list
  log's head advance, materialize on the grant. Host policy defaults
  the approval to explicit (§5.4), because this list decides where
  private data flows.
- **The list itself replicates to members only.** The mirror-list log
  propagates among quorum members like every spirit log (each member's
  spirit must know the targets, since any member can originate a
  batch), and is never shipped to the remotes it names — a remote has
  no use for the cluster's trust map.
- **Why cluster-governed and not per-host**: if members disagreed
  about the target set, one member would ship state to a host the
  others never agreed to trust — for private data a safety failure,
  not an inconvenience. The quorum gate on the mirror-list log's head
  makes the target set a cluster decision, anchored by evidence,
  identical on every member — and changing a backup host is an
  ordinary state change, not an account reissue. (This resolves
  `ComponentMirroringCapabilityDesign.md` §11 question 2; the
  amendment marks it.)
- **Per component, by construction**: mind — or any later
  state-bearing sibling — holds its own mirror-list log the same way,
  under `(ComponentHead Mind MirrorTargets)`. Nothing here is
  spirit-specific.

### 5.4 · Safe policy defaults per slot kind

Until approval predicates exist (§3.3), host policy carries the
difference in stakes. Defaults, as design:

- Silo head advances (`(ComponentHead kind (Silo …))`): the host's
  configured mode, as today — quorum mode auto-approves well-formed
  advances; this is the landed behavior.
- `Children` changes and mirror-list log advances
  (`(ComponentHead kind MirrorTargets)`): **explicit approval** by
  default (§8) — a parked proposal an authorized agent approves
  deliberately. Rationale: these two slots ARE the authority topology
  and the data-flow topology; auto-approving them would let any
  working-socket caller reroute private data or mint accounts, which is
  the same hole §4.3 closes, reopened one layer up. An owner can relax
  the default; the default itself is fail-closed.

### 5.5 · Criome's own store: the authoritative silo and host-local state

The psyche asked whether the criome daemon itself needs its own
mutable data silo. Yes — and the unified model says exactly what it
holds and how it changes. Criome is itself a state-bearing component
with a durable store (already a sema-engine store, like spirit's).
Under the two layers of §2 it splits in two:

**The authoritative silo.** The account tree — the criomes themselves
— plus, per governed slot, the current head, the current child-set
value, and the newest quorum evidence: the anchor, succession, live
accounts, and per-slot items of §6.2's footprint. Its mutations are
exactly the OUTPUTS of quorum rounds — a `Children` advance when a
parent quorum issues or supersedes an account, a slot head advance
when the gate grants one. Nothing else writes it. The recursion
grounds cleanly, stated plainly: there is no higher gate above this
silo, because its mutations ARE the gate's verdicts. Asking "who
authorizes criome's own state change?" is asking "who authorizes the
round?", and the answer is the round itself, judged by the governing
account's rule — terminating at the founding ceremony, the one
non-proposed birth. This silo is what replicates criome-to-criome, and
widely (accounts travel wide, §2): members converge on it by voting
and by verified catch-up, and a non-authoritative follower consumes
exactly this silo — the admitted accounts and the heads of the chains
it follows — to have awareness of the quorum and verify pushes.
Mirroring it is the same component-mirrors-to-sibling mechanism the
mirroring design gives every state-bearing component: criome mirrors
to criome as spirit mirrors to spirit, carrying the evidence it itself
minted. The loop closes with no special case.

**Host-local operational state.** In-flight round bookkeeping (open
`Gathering` rounds, the anti-equivocation rows for open windows),
window timers, session state, transport and conveyance configuration,
host policy (§8), and the node's own keys. Mutable, per-host, NEVER
mirrored — none of it is cluster truth: two healthy members
legitimately disagree about it at any instant (one is originating a
round the other has not yet heard). It prunes by its own local rules
(§6.2's dead-round and spent-round pruning) and is rebuilt from its
durable rows on restart where recovery needs it.

The split is the two-layer ontology applied to criome itself: the
authoritative silo is layer one plus its evidence — small, slow, wide;
the operational state is machinery, consumed by nobody else.

## 6 · Bounded history: how this avoids the infinitely-sprawling blockchain

The psyche's hard constraint: current state plus the evidence needed to
verify it; superseded accounts and dead state prunable; never
accumulate all the parent contracts forever.

### 6.1 · Why pruning is sound here and not on a blockchain

A public blockchain keeps every transition because any stranger must be
able to verify today's state from genesis with no trusted input. We do
not have strangers: every verifier — member, remote, restored node —
starts from the **owner-pinned founding anchor** and a closed
membership. Three standing facts then make old history redundant:

1. **The newest grant attests everything beneath it.** Heads are
   hash-chained: each digest folds its predecessor. A grant for head
   H(n) therefore transitively vouches for the entire chain below H(n).
   Once the quorum grants H(n), the grants for H(n-1), H(n-2), …
   prove nothing the newest grant does not already prove. Old evidence
   is not discarded knowledge; it is discarded redundancy.
2. **Authority is reachability from the live tree.** An account
   superseded out of its parent's `Children` value is unreachable from
   the root and can authorize nothing; no verification path ever visits
   it. Keeping it would prove only that history happened, which no
   verifier needs.
3. **Committed rounds are terminal and inert below the current head.**
   A proposal must chain from a slot's CURRENT head; nothing can ever
   again be proposed against a superseded head, so anti-equivocation
   rows below the current head can never fire again.

### 6.2 · The durable footprint, exhaustively

What a criome node retains — this list is the whole of it:

- the pinned founding anchor, with its attached founding signatures;
- the root succession chain: the rare rotation grants from the pinned
  anchor to the current root keys (see the open question in §12 on
  compacting even this by owner re-pinning);
- the live account tree: the current account records reachable from
  the root — a handful of tiny rule+parent records;
- per live slot: the current head, the current value (the one
  criome-held slot, `Children`), and the NEWEST grant evidence;
- live proposal rows: rounds whose window is still open, plus the
  anti-equivocation row for the current head of each slot;
- host policy and the node's own keys.

(The first four items are criome's authoritative silo, §5.5 — what
mirrors criome-to-criome; the last two are host-local and never
travel.)

What prunes, and when:

- on every slot advance: the predecessor value, the predecessor's
  grant evidence, and the committed rows below the new head;
- on every `Children` advance: the accounts it removed, together with
  ALL of their slots' state (dead state dies with its account);
- dead `Gathering` rows: on supersession (landed, criome 0.8.0);
- expired terminal rounds: after their refusal has been pushed, on the
  next advance of the same slot.

The footprint is proportional to the LIVE tree and slot count —
independent of how many changes ever happened. That is the plain answer
to sprawl: **history length never appears in the storage bound.**

The component's own log content (spirit's records) is layer-two bulk
governed by spirit's own retention and checkpoint policy — out of scope
here, named so nobody reads this section as pruning spirit's records.
What §6 prunes is criome's governance state: dead accounts, stale
evidence, spent rounds.

### 6.3 · What a verifier needs, walked through

A fresh non-authoritative remote enrolling (or a member restoring from
nothing) needs exactly:

1. the pinned founding anchor (the one manual trust act) and the root
   succession chain to the current root keys;
2. the live account records on the path from the root to the governing
   account (for the operational account: two records), each carried
   with the parent's newest `Children` grant — evidence that THIS is
   the live child set;
3. for each slot it follows: the current head, the newest grant, and —
   for chains whose content it holds — the content, which it verifies
   by re-hashing up to the granted head.

Nothing about any superseded account, any old grant, or any spent round
is ever requested, because no verification path uses them. Catch-up of
an offline member is the same walk shortened: the newest grant it
receives covers, transitively, every advance it slept through — the
batch argument of the slice design, doing double duty as the pruning
argument.

If amendment-by-successor ever fails this test — if some verification
path turns out to require a dead record — the psyche's standing rule
applies: redesign it; backward compatibility is never a design variable
(public Spirit record vjvm). This design finds no such path.

## 7 · The consumer path: the list lives with its consumer

The original ask for this design was consumer lookup plus push
notification: how does spirit learn its mirror-target state, and how
does it hear changes without polling? The psyche's placement dissolves
the machinery: **spirit holds the list itself.** There is nothing to
look up and nobody to subscribe to — the consumer and the holder are
the same component.

- **Lookup** is spirit reading its own mirror-list log's current
  value, in its own store, locally — the same way it reads any of its
  state.
- **Notification** is spirit's own commit flow. A mirror-list change
  is a working operation: it stages, the quorum grants, spirit
  materializes — and the materialization is the event. The shipper
  already receives head-advanced mail on every commit (the landed
  drain seam); a mirror-list materialization is one more such mail,
  carrying which log advanced. Producers push at every hop; there is
  no remote consumer, no subscription session, and no poll anywhere —
  the push-not-pull requirement is satisfied by there being nothing to
  pull.
- **Cross-node** the list flows as spirit state, because it IS spirit
  state: the mirror-list log propagates to the other members through
  the ordinary authorized-batch push, and each member's spirit reacts
  to its own materialization of the change exactly as the originator
  did.

### 7.1 · Where propagation targets come from now

The propagation design (shape (b), settled) had the grant carry the
target host IDs. With the list as spirit's own authorized state, the
target set splits by owner, and each fact keeps exactly one source:

- **Members** are criome's knowledge (the operational account's rule).
  They still ride the grant as opaque routing data — criome resolves
  members-minus-self at grant time, as landed. Spirit stays
  quorum-ignorant: it never learns what a membership is, only where to
  push.
- **Remotes** are spirit's knowledge: the shipper reads the CURRENT
  mirror-list value from its own store at ship time and adds, per
  silo, that silo's mapped hosts.

The union is the push set. This is cleaner than making the grant carry
remotes too: criome would have to hold a copy of spirit's list to echo
it, and a copy is a second source of truth that can drift. The
grant-echo survives exactly where criome is the one owner — membership
— and nowhere else. (The mirroring design's amendment restates this at
its §2 step 3.)

### 7.2 · What spirit does with a target change

- **A host appears in the mapping**: the new target must receive the
  EXISTING chain now, not at the next write. The materialization mail
  for the mirror-list log triggers the backfill: the shipper frames
  the new target's restore bundle / suffix (per the mirroring design's
  restore module) for each silo mapped to it and ships through the
  ordinary router path.
- **A host disappears**: future batches stop; nothing is recalled.
- **Startup**: the shipper seeds itself from the mirror-list log's
  current value at open — its own store, no session to wait for.

### 7.3 · What dies

`SelectedMirrorTarget` on spirit's meta `Configure` input, the
`MirrorTarget`/`MirrorAddress` types in meta-signal-spirit, and the
owner-configures-spirit flow for mirror addresses. The owner act moves
to its proper seat: an ordinary (explicit-approval-parked, §5.4)
working operation on spirit amending the mirror-list log, authorized
by the quorum, propagated to every member. One source of truth,
cluster-agreed, held where it is consumed.

## 8 · Explicit approval: retiring `EscalateToPsyche`

The Rule enum today carries a bare variant `EscalateToPsyche` (ground
truth §1). The psyche's correction: it is wrong twice.

- **Wrong layer.** "Park this for a human" is not a property of an
  account's transition rule; it is HOW THIS HOST behaves when asked to
  approve — criome policy. The behavior already exists as the host
  authorization mode that parks a proposal for owner approval
  (`ClientApproval` in the landed mode table).
- **Wrong concept.** Criome must have no concept of "psyche." The
  program knows only that a proposal *needs explicit approval* — an
  approval some authorized caller performs deliberately on the meta
  surface. Who that caller answers to is outside criome's vocabulary.

Design:

1. **Remove the variant.** Rule goes from 11 variants to 10. No
   replacement rule variant: escalation is not a rule. Signal-criome
   takes the schema change on the clean-genesis posture (nothing
   deployed holds rules to preserve; consistent with settled intent).
   A usage sweep before removal is a verification point (§13).
2. **Rename the mode.** `AuthorizationMode::ClientApproval` becomes
   `ExplicitApproval` — the psyche's own words, "needs explicit
   approval," as the vocabulary everywhere: mode, parked-state name,
   CLI surface.
3. **Policy is itself eventually gateable.** Host policy today is local
   configuration. The psyche notes it should eventually be governable
   by another account — which this design already has a seat for: a
   host-scoped account whose governed slot is the host's policy record.
   Named as a future slot kind, deliberately not designed now.

The defaults of §5.4 (account-layer and target-list changes park for
explicit approval) are where this mode earns its keep immediately.

## 9 · Relation to ClusterAuthorizationSliceDesign §5

That section designed the root issuing the operational sub-contract as
an authorized object of kind `Contract` through the two-round commit,
admitted by members with the root-round evidence. This design subsumes
its FRAMING and keeps its mechanics:

- "The root issues a sub-contract as an authorized object" becomes "the
  root's quorum authorizes a `Children` state change whose new value
  includes the operational account" (§4.1). Same round, same evidence,
  same admission-carries-proof — the object authorized is now the
  slot's successor value rather than a free-standing object kind.
- The sub-contract "document" dissolves into the two layers: member set
  and threshold live in the new account's RULE (the account stays rule
  + parent); the replication/target section that
  `ComponentMirroringCapabilityDesign.md` §4 wanted in the document is
  spirit's own quorum-gated mirror-list log (§5.3).
- Membership rotation ("a replacement sub-contract the same way")
  becomes account supersession with slot adoption (§4.2).
- The staging posture (prototype rounds over the root before the
  operational account exists) is unchanged.

`ClusterAuthorizationSliceDesign.md` §5 has been amended minimally to
point here; its verification chain (pinned root anchor →
root-authorized account → operational rounds under it) is exactly
§6.3's walk.

## 10 · The rename: `Contract` becomes `Criome`

Settled by the psyche: "rename Contract to Criome, the account is the
criome." Scope of the mechanical rename, from the ground-truth sweep:

- signal-criome: `Contract` → `Criome`, `ContractParent` →
  `CriomeParent`, `ContractDigest` → `CriomeDigest`, the working-socket
  operations (`AdmitContract` → the evidence-carried admission verb of
  §4.3, `LookupContract` → `LookupCriome`, `ContractMissing` →
  `CriomeMissing`, `ContractAdmitted` / `ContractFound` /
  `ContractAdmissionRejected` likewise), and
  `AuthorizedObjectKind::Contract` → `::Criome`.
- criome: `ContractStore`, the store tables, the per-contract head and
  round rows, module docs, and every "operational quorum contract"
  phrase → "operational criome."
- consumers: spirit's `criome_gate` doc comments, meta-signal-criome,
  the design documents' running vocabulary.
- **The signal-* crates keep the word "contract"** in their own sense —
  a wire contract, the typed operation/reply surface of a component.
  The overloading this session was asked to flag dissolves by the
  rename itself: the cryptographic record is a Criome; a "contract
  crate" is a wire contract; the two words no longer collide.
- Reading convention, stated once: lowercase **criome** is the program
  and its host; **Criome** (or "an account," "a criome") is the record.
  The program keeps criomes — the name finally means what the vision
  meant.

Versioning: the rename is wire-visible (schema type names) and rides
the clean-genesis posture like every schema change in this family;
signal-criome and criome take minor bumps with their blocks, per the
versioning discipline. Sequencing: the rename must land AFTER the
everywhere-gate implementation lane has released its claims on the same
files (the gate landed on the mains as criome 0.8.0 / sema-engine 0.7.0
— confirm the lane's claims are released at pickup, §13). Landing the
rename BEFORE slices G2-G7 is preferred, so every new type below is
born in the settled vocabulary.

## 11 · Slice map

Each slice independently shippable, producers before consumers.

- **G0 — rule and mode cleanup.** Remove `EscalateToPsyche` from Rule;
  rename `ClientApproval` → `ExplicitApproval` (§8). Small,
  independent, can land immediately. signal-criome + criome bumps.
- **G1 — the rename.** `Contract` → `Criome` across signal-criome,
  criome, meta-signal-criome, and consumers (§10). After the
  everywhere-gate lane's claims are released; before G2 by preference.
- **G2 — the governed-slot substrate.** The closed `GovernedSlot`
  vocabulary; head/anti-equivocation/round rows keyed by (account,
  slot); criome-held slot values stored current-only; newest-evidence
  retention and the §6.2 pruning rules (including account
  garbage-collection by live-tree reachability); multi-slot rounds
  (§5.2). The heart of the design.
- **G3 — admission closure.** The structure-check `AdmitContract` path
  dies; evidence-carried admission replaces it; founding untouched
  (§4.3). Depends on G2 (evidence rows).
- **G4 — issuance as a state change.** `Children` slot live: the root
  issues the operational account as a `Children` change; supersession
  with slot adoption; §5.4 policy defaults. Subsumes
  ClusterAuthorizationSliceDesign §5's implementation. Depends on G2.
- **G5 — the mirror-list log.** Spirit gains the mirror-list log and a
  typed working operation amending it, gated as
  `(ComponentHead Spirit MirrorTargets)` with the explicit-approval
  default; the shipper unions grant-carried members with the mapped
  remotes from its own log and backfills added targets;
  `SelectedMirrorTarget` and its meta types die (§5.3, §7). Depends on
  G2; composes with the mirroring design's M-slices.
- **G6 — privacy-silo governance.** `ComponentHead` gains the silo
  dimension; per-silo advance authorization; cross-silo moves as
  multi-slot rounds (§5.2). Depends on G2 and on the silo work in
  spirit/sema-engine (the amended
  `ComponentMirroringCapabilityDesign.md` §5 / M5). The component-side
  silo mechanics live in that design; this slice is the governance
  face.
- **G7 — the policy slot (future, named only).** Host policy as
  governed state under a host-scoped account (§8, item 3). Not
  scheduled.

## 12 · Open questions — only the psyche can answer

1. **The silo set.** Spirit's privacy vocabulary is an ordered 8-level
   magnitude on every record. The silo set must be closed and SMALL.
   One silo per magnitude (8 parallel logs) is faithful but heavy;
   a coarse partition (for example three: public / guarded / closed,
   each covering a magnitude range) is cheap but fixes a boundary the
   magnitudes currently leave fluid. Which partition — and where do the
   boundaries fall? (The mirroring amendment carries the same question;
   answered once, it settles both.)
2. **Compacting the root succession chain.** The one genuinely
   append-only object left in §6.2 is the chain of root rotation grants
   from the pinned anchor. It is tiny and rotations are rare — but it
   can be compacted to nothing if, after witnessing a rotation, the
   owner may RE-PIN the anchor to the current root identity (a new
   manual trust act replacing the old). Is re-pinning acceptable trust
   posture, or must the original founding anchor remain the immovable
   root of every verification forever?

The two open questions of the mirroring design's §11 that survive its
amendment (remote read-liveness; mirror-repo disposal ceremony) remain
recorded there.

## 13 · Worker verification points at pickup (cheap, factual)

1. Confirm the everywhere-gate lane has released its Orchestrate claims
   on criome/spirit/sema-engine before starting G1 (the mains already
   carry 0.8.0 / 0.7.0).
2. Sweep usages of `Rule::EscalateToPsyche` (criome evaluation paths,
   tests, fixtures) before G0 removes it; the scout found no doc
   comment but did not sweep call sites.
3. Confirm the per-contract head/round row schema in criome 0.8.0
   tolerates the added slot key column as a re-genesis (expected: yes —
   clean-genesis posture, nothing deployed to migrate).
4. Confirm the multi-store spirit layout the silo slice introduces
   accommodates the mirror-list log as one more chain, and that the
   head-advanced mail the drain receives names WHICH log materialized
   (the shipper must distinguish a mirror-list change to trigger
   backfill).
5. Confirm grant-time member resolution (membership minus self — and
   nothing else; remotes come from spirit's own log) sits in the same
   bridge code path that assembles Evidence today, so members and
   evidence stay one push.
6. Confirm nothing outside criome persists old grant evidence in a way
   that would dangle under §6.2 pruning (spirit deliberately does not
   retain grants — it re-fetches the standing head's evidence at ship
   time; verify no other consumer began retaining).
7. For G4: the founding proof pins the root; confirm each member's
   store records the root account itself as live-tree root for
   reachability GC (the founded root is admitted into the store
   post-founding — carried over from the slice design's point 7).
