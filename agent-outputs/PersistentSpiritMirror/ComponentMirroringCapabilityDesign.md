# Component Mirroring Capability — end design

Design only; no repo was edited and no tracker item was mutated. Lane:
CriomeClusterPropagation / component-mirroring-capability-design.

This document answers one question: what is the best end design for
mirroring as a general capability of state-bearing components, given the
settled vision that components do not use a separate mirror program —
spirit mirrors to spirit, mind to mind — and that backward compatibility
is never a constraint.

It composes with the accepted slice design
`ClusterAuthorizationSliceDesign.md` (same directory), which a parallel
worker is amending right now to the corrected authorization semantic:
**the criome cluster quorum gates acceptance everywhere, including
locally — a change that is not authorized is not recorded anywhere.**
This design targets that corrected semantic. Everything mirrored is
therefore authorized by construction; mirroring never has its own
authorization step, it only carries the proof along.

A prior analysis of the mirror stack was forwarded as input, explicitly
not as the final word. Its factual claims were re-verified against
source by three independent scouts; §1 records what held and what did
not, and §9 gives the judgment on its recommendations.

**Amended 2026-07-07.** Two psyche decisions this session, designed in
full in `CriomeStateGovernanceDesign.md` (same directory), rework parts
of this document:

- **Privacy silos replace sealed payloads.** Records of different
  privacy classes live in SEPARATE logs, each with its own chain and
  head; mirroring to an untrusted host ships only the public silo. No
  sealed entries, no payload commitments, no derived chains, no digest
  schema change. §5 is rewritten; §11 question 1 dissolves (the
  metadata-leak dilemma no longer exists).
- **The mirror-target list is quorum-governed state living in
  spirit.** The psyche, verbatim: "the list of mirrors is in spirit,
  changes gated in criome. just another log, like the privacy silos."
  The §4 recommendation to put targets in the sub-contract document is
  superseded; §11 question 2 is resolved. Member targets still ride
  the grant (membership is criome's knowledge); remote targets come
  from spirit's own mirror-list log. §2 step 3, §4, and the slice map
  are amended accordingly.
- Vocabulary: the account record `Contract` is renamed `Criome`
  (settled; that design's §10). This document's older "operational
  quorum contract" phrasing reads as "the operational account" and is
  left in place where unambiguous.

## 0 · Terms

Plain definitions, used throughout:

- **Component** — one program with one job on a host: `spirit` (the
  intent record keeper), `criome` (the identity and authorization
  keeper — all cryptography is its domain), `router` (the network
  carrier — it only routes), and later siblings such as `mind`. Each
  host runs exactly one instance of each deployed component.
- **SEMA / sema-engine** — the shared typed-database engine every
  state-bearing component embeds for its durable state. Both spirit and
  criome already build their stores on it. When the vision says the
  reusable parts live "close to the SEMA functionality," this crate is
  that place.
- **Hash-chained commit log** — sema-engine records every state change
  as a log entry whose digest (a cryptographic fingerprint) folds in the
  previous entry's digest. One head digest therefore pins the entire
  history beneath it. There is one chain per component store; spirit's
  single store is named `spirit:sema` and holds all its record families.
- **Store family** — a named kind of record inside one store (spirit
  has records, referents, migrations). Families share the one chain;
  they are not separate logs.
- **Outbox** — sema-engine's durable "shipped up to here" cursor over
  the commit log; `unshipped()` yields the ordered suffix of entries not
  yet propagated.
- **Quorum / operational quorum contract** — the criome cluster's
  member list and threshold, anchored under the one root contract. A
  head advance is accepted only when the members complete the two-round
  commit over it.
- **Grant and evidence** — when the quorum accepts a head advance,
  criome produces a signed grant (its statement that this digest is
  authorized) plus the assembled evidence (the members' signatures for
  that round). Evidence is what lets any other criome verify the
  acceptance independently.
- **Criome host ID** — the host criome's master public key; the only
  network identifier. A destination is (Criome host ID, component kind).
- **Non-authoritative remote** — the psyche's git-remote analogy: a
  host running criome plus a mirrored component that receives the
  cluster's state but is not a quorum member and can never authorize
  anything.
- **Privacy magnitude** — spirit's existing per-record privacy field: a
  typed ordered level (an 8-step scale, `Zero` through `Maximum`),
  queried with selections such as "at most public."
- **Privacy silo** — one of a small, closed set of privacy classes,
  each backed by its OWN log: its own store, hash chain, head, and
  outbox. Every record lives in exactly one silo, chosen from its
  privacy magnitude by a fixed total mapping (which partition of the
  magnitude scale forms the silo set is an open psyche question,
  recorded in `CriomeStateGovernanceDesign.md` §12). Silos are primary
  logs, not projections derived from a master log.
- **Mirror-list log** — spirit's own log holding the mirror-target
  list: a mapping silo → target hosts, amended only through the same
  quorum gate as any head advance
  (`CriomeStateGovernanceDesign.md` §5.3).

## 1 · Ground truth (verified against source, 2026-07-05)

Checkouts: spirit `1698cba`, mirror / signal-mirror / meta-signal-mirror,
router, sema-engine, criome mains under `/git/github.com/LiGoldragon/`.

What holds:

- The mirror stack is a standalone daemon (`mirror-daemon` binary), an
  in-process service used by tests (`mirror/src/service.rs:37`), a
  component-side shipper (`mirror/src/shipper.rs:77`), and two contract
  crates (signal-mirror, meta-signal-mirror).
- It already builds ON sema-engine rather than beside it: the shipper
  reads sema-engine's outbox and acknowledges its cursor; the mirror's
  own store is a sema-engine store (`mirror/src/store.rs:307-311`).
  The send half of mirroring already lives in the shared layer.
- The genuinely mirror-owned generic machinery is the receive half:
  the append decision engine (duplicate / gap / fork / digest-mismatch
  refusals, `mirror/src/decision.rs:26-105`), crash-window healing (an
  interrupted two-step persist heals on idempotent re-send,
  `decision.rs:73-105`, `store.rs:452-471`), restore-bundle assembly
  (`store.rs:587-617`), and landed-body re-hash verification
  (`mirror/src/readback.rs:42-66`).
- The three mirror repos contain no spirit vocabulary at all — they are
  keyed on an opaque store-name string and payload bytes. Everything
  spirit-shaped (the shipper gate `MirrorShipper`, the mirror-target
  configuration, import materialization, the head witnesses) lives in
  spirit and router, not in the mirror repos.
- Nobody consumes the mirror stack in production. Spirit gates it
  behind an off-by-default feature; router uses it only for a dev
  witness; criome and sema-engine have no edge to it. The deployed
  `mirror.service` crash-loops on a storage-schema mismatch and is being
  disabled on all hosts (tracker note under the nbmq epic, which already
  states the separate mirror daemon is dropped).
- Both forwarded test-topology claims are true: spirit's cluster test
  ships the authorized suffix to an in-process mirror service
  (`spirit/tests/cluster_authorization_over_router.rs`), and the VM
  cluster deploys a real mirror-daemon on node B with a hand-built
  witness binary constructing the mirror append — bypassing spirit's
  shipper (`CriomOS-test-cluster/lib/mkCriomeAuthWitnessTest.nix:35-39`,
  `router/src/bin/router_forward_witness.rs:131-148`).
- The router audit claim is true: per-destination forward ordering does
  NOT hold today. Deliveries to the same destination are spawned as
  racing concurrent tasks (`router/src/router.rs:2750-2778`), a failed
  forward re-enqueues at the tail (`router.rs:3630-3634`), and the
  durable backlog reads back unordered (`router/src/tables.rs:371-375`);
  the backlog witness sorts before asserting.
- sema-engine facts that shape this design: one chain and one head per
  store, not per family (`sema-engine/src/commit_log.rs:36`); one global
  shipped cursor, no per-destination cursors (`outbox.rs:17-19`); and
  the entry digest folds the raw payload bytes directly
  (`versioning.rs:328-338`) — so a payload cannot be withheld from a
  shipped chain without breaking verification. §5 turns on this fact;
  the silo amendment answers it by never needing to withhold one.
- Spirit main already matches the settled direction: the criome gate is
  a closed mode (Disabled, the operative default, or Enabled with a
  cluster authorizer); the old ship seam is a propagation drain
  (`spirit/src/propagation.rs:67,84`); the typed apply ingress exists in
  the contract but the daemon still refuses it
  (`spirit/src/nexus.rs:1310`).

Where the forwarded analysis was wrong, in fact rather than judgment:
"router transport of opaque frames" is not a mirror piece (the mirror
has its own direct TCP ingress — the rejected transport path — and no
router dependency), and its spirit-specific list (store family names,
ComponentKind::Spirit, guardian authorization, head-object witness) is
not in the mirror repos at all; those live in spirit and router. The
consequence matters: the task is not "extract the generic parts out of
mirror" — the mirror is already generic. The task is to merge its
receive half into sema-engine and delete the rest.

## 2 · The end design in one page

Mirroring is a verb of the state-bearing component itself, implemented
once in sema-engine and spoken over each component's own contract.
There is no mirror program, no mirror contract, no mirror store.

The life of one change, end to end, under the corrected acceptance
semantic:

1. A working request reaches the component (say, spirit records an
   intent). The component assembles the proposed log entry and computes
   the digest its head would advance to.
2. The component asks its local criome to authorize that digest — one
   question, no quorum vocabulary. Criome runs the two-round commit
   across the operational quorum contract's members over the router.
   No grant, no record: an unauthorized change is refused everywhere,
   including locally.
3. The grant comes back carrying the MEMBER targets: the quorum
   members minus this host, each as a Criome host ID — membership is
   criome's knowledge, and it rides the grant as opaque routing data.
   The non-authoritative remotes are spirit's own knowledge: the
   shipper reads the current silo → hosts mapping from its own
   mirror-list log at ship time (§4, amended). Each fact has exactly
   one owner; nothing is echoed from a copy. The component commits the
   entry and stores the grant evidence beside it, in the same
   transaction, keyed by the entry digest — so a crash between
   acceptance and shipping loses nothing.
4. The component's propagation drain (a background actor, pushed a mail
   on every commit — never polling) frames the advanced silo's
   unshipped suffix as one typed apply-batch per target of that silo:
   the ordered entries, the authorization identifier (account digest
   plus authorized head reference), and the evidence. Members receive
   every silo; a remote receives exactly the silos the mirror-list
   maps to it (§5). Each batch goes to the local router addressed to
   (target host ID, same component kind) — spirit to spirit, mind to
   mind. The shipped cursor advances when the local router has durably
   accepted the batches; from there delivery is the router's job,
   ordered per destination (§7), held in its durable backlog while a
   peer is away and drained on the session-established push.
5. The receiving component's ingress hands the carried authorization to
   ITS local criome before touching state. A member criome recognizes
   the round from its own ledger, or verifies the evidence and records
   it (the catch-up path). A non-authoritative remote's criome verifies
   the evidence against the quorum contract it has admitted but is not
   part of (§4). Anything else is a typed refusal; nothing is written.
6. Only then does sema-engine's apply validation run — the decision
   matrix ported from the mirror: the batch chains onto the local
   applied head, every entry chains onto its predecessor, the last
   entry re-hashes to the authorized digest, duplicates acknowledge
   idempotently, gaps and forks refuse. The fold commits atomically.
7. Backup is the same mechanism, because a mirror IS a backup: any host
   holding the mirrored chain can produce a restore bundle (latest
   checkpoint plus the entry suffix past it), and a restoring component
   imports it through the same validation, accepting only a head its
   own criome confirms as the authorized cluster head (§6).

The special cases dissolve: a quorum member receiving a push and a
non-authoritative remote receiving a push run the same code path with
one difference inside criome (co-sign and advance versus verify and
follow). A batch of one is a batch. A backup restore is an import. The
mirror daemon's whole reason to exist — being the receiving mailbox —
is simply the sibling component itself.

## 3 · Where the machinery lives

**sema-engine grows the receive half and keeps the send half. No new
crate.** The forwarded analysis proposed extracting a new shared
library. Rejected: sema-engine already owns the chain, the outbox, the
cursor, the checkpoint machinery, and the import fold — half of
mirroring. The receive-side decision matrix and restore assembly are
the same vocabulary (entries, digests, heads, suffixes) operating on
the same store. Splitting one vocabulary across two crates fails the
micro-components split test in the other direction: mirroring is not a
distinct noun, it is the replication verb-set of the versioned commit
log. sema-engine gains a `mirroring` module family:

- Send: per-store (hence per-silo) suffix framing into wire envelopes;
  durable evidence retention keyed by entry digest; the generic
  propagation driver (parameterized by the component's router
  submission and target source — the component wires, the engine
  drives).
- Receive: the ported decision matrix (duplicate / gap / fork / digest
  / continuity) with its crash-window idempotence property and its
  tests, unified with the existing import ingest so apply-batch and
  restore-import are one validation path ending in the atomic fold.
- Restore: bundle assembly (checkpoint + suffix past its coverage) and
  head re-derivation, moved from the mirror's store and readback
  modules.

**signal-sema owns the wire vocabulary.** signal-sema is already the
shared sema contract crate sema-engine consumes. It gains the typed
wire records every mirrored component speaks: the entry envelope
(sequence, previous digest, digest, payload), the
entry suffix (expected head + ordered envelopes), the head mark, the
restore bundle, and the closed refusal reasons. These are redesigned,
not copied, from signal-mirror: the opaque store-name string dies —
under (host ID, component kind) addressing the destination component IS
the store selector; the store schema hash stays as the identity check.
One canonical asserted round-trip per type, per contract-repo
discipline.

**Each component's own contract carries the operations.** signal-spirit
(and later signal-mind, and any sibling) declares the apply-batch
operation — ordered envelopes plus authorization identifier plus
evidence — and its typed receipt and refusal replies, composing the
signal-sema records. The existing single-record apply operation with
hex-string payloads is replaced by this typed batch form (this is the
same operation the pending propagation slice already specifies; this
design supplies its shared types). Restore is a meta-contract
(owner-only) operation on the component, since restoring is an owner
act, not peer traffic.

**What stays component-specific (spirit's residue).** Exactly three
wiring points, which are also the checklist that makes any future
component mirrorable:

1. Its contract declares the apply-batch operation (and the meta
   restore operation) over the shared signal-sema records.
2. Its runtime registers its family materializers (spirit's family
   directory already does this) and, for §5, its record-to-silo
   placement — the fixed mapping from a record's privacy magnitude to
   the silo store it is written into. The engine stays payload-blind;
   it never learns what a magnitude means, only which store to drive.
3. Its daemon wires the propagation drain to its criome authorization
   session and its local router client.

Everything else — validation, healing, cursor, restore — is
engine. Spirit keeps its head witnesses (the meta operations returning
the head digest and the head entry body) as its observability surface;
they remain useful for live proofs.

## 4 · Non-authoritative remotes — quorum awareness without authority

The git-remote analogy made structural. A non-authoritative remote runs
criome plus the mirrored component (spirit mirrors to spirit; the
remote's criome exists because cryptography is criome's domain at both
ends of every network boundary — the component never verifies
signatures itself).

**Enrollment — the one manual trust act.** The owner pins the cluster's
root anchor (the founding proof of the root contract) into the remote's
criome, exactly as trusting a key when adding a git remote. The cluster
then pushes the operational account together with the evidence of the
root-quorum round that issued it; the remote's criome verifies that
chain against the pinned anchor and admits the account as a followed
one — it knows the member set and the threshold. That admitted account
is precisely "awareness of that quorum which allows for the state
change." (It does not see the mirror-target list: that is spirit
state, replicated among members only — a remote needs no copy of the
cluster's trust map to verify the pushes it receives.)

**Verification, per incoming batch.** The remote component's ingress
hands the carried authorization to its local criome, which verifies the
evidence — signatures and threshold against the admitted contract —
and advances a follower head chain for that contract (the same
per-contract head rows a member keeps, minus co-signing). On
Authorized, the component runs the same §2 step-6 apply validation.
This is the already-designed receiving-side acceptance check with one
branch fewer: a follower never finds the round in its own ledger,
because it never votes.

**No authority, structurally.** The remote is not in the member set, so
members never solicit it and would refuse any round it originated (the
member-set well-formedness check, already built). Its own criome cannot
grant a head advance on a contract it merely follows, and under the
corrected semantic an ungranted change is never recorded — so the
mirrored store on the remote is read-only by construction. No flag, no
mode; the absence from the member set is the whole mechanism.

**Where the target list lives (amended 2026-07-07).** The psyche
placed it: "the list of mirrors is in spirit, changes gated in criome.
just another log, like the privacy silos." Spirit holds a
**mirror-list log** — one more hash-chained log beside its silos —
whose current value is the mapping silo → target hosts. Changing it is
an ordinary working operation on spirit, authorized through the same
quorum gate as any head advance, and parked for explicit approval by
default, since this list decides where private data flows. This keeps
the safety property that motivated this section's earlier
in-the-contract recommendation — the target set is cluster-agreed,
evidence-anchored, and identical on every member (the quorum gated it,
and the log replicates to every member like any spirit state) — while
shedding its cost: adding or dropping a backup host is a state change,
not an account reissue. The list never ships to the remotes it names.
Full design: `CriomeStateGovernanceDesign.md` §5.3 and §7. This
resolves §11 question 2.

**Scaling down: the backup case.** A single host wanting off-site
backups is a single-member cluster (the root and a one-member
operational sub-contract) with one or more non-authoritative remotes,
public-only or full per trust. Nothing about mirroring is
cluster-sized; the quorum of one is the degenerate case of the same
design.

## 5 · Record-class gating — privacy silos (rewritten 2026-07-07)

This section previously answered record-class gating with sealed
payload commitments: a digest-schema change letting private payloads
ship as fingerprints inside one shared chain. The psyche superseded
that design this session with a simpler, stronger shape, proposed in
his own words as separate logs per privacy class. The sealed-payload
design, its digest domain-tag change, and its metadata-leak dilemma
are all dead; what follows replaces them.

**Privacy silos: separate logs per privacy class.**

- **The silo set is closed and small.** Each silo is one privacy
  class, backed by its own sema-engine store: its own hash chain, its
  own head, its own outbox. Spirit's single `spirit:sema` store
  becomes one store per silo, plus the mirror-list log (§4). Every
  record lives in exactly ONE silo, chosen from its privacy magnitude
  by a fixed total mapping — the magnitudes partition into silos.
  Which partition (one silo per magnitude, or a coarse split such as
  public / guarded / closed) is an open psyche question, recorded in
  `CriomeStateGovernanceDesign.md` §12.
- **Nothing is sealed, nothing is derived.** Each silo chain carries
  raw payloads and verifies stand-alone — the verified digest fact
  (§1) stays true and stops mattering, because no shipped chain ever
  needs a payload withheld. There are no placeholder entries, no
  second derived chain, no projection maintenance, and no digest
  schema change.
- **Shipping is silo-selective by construction.** The mirror-list log
  (§4) maps each silo to its target hosts; members receive every silo.
  The public silo ships to an untrusted backup host COMPLETE — a
  genuine, verifiable, restorable full backup of all public data. And
  the untrusted host receives NOTHING about private records: not
  existence, not timing, not family, not key, not size. The previous
  revision's metadata-leak question dissolves (§11 question 1).
- **Authorization cost, stated honestly** (the psyche asked for the
  costs): each silo's head advances under its own governed slot
  (`CriomeStateGovernanceDesign.md` §3.1) — N silos mean N chains, N
  heads, and N advance serializations criome-side. A working operation
  touches exactly one silo in the common case, so the cost per
  operation is unchanged: one round. Batching applies per silo exactly
  as the slice design argues for one chain.
- **Cross-silo moves are explicit authorized operations.** A privacy
  reclassification that crosses a silo boundary removes the record
  from the source silo and appends it to the destination silo — staged
  together and authorized by ONE multi-slot round binding both silo
  heads, all or nothing (`CriomeStateGovernanceDesign.md` §5.2). Rare
  by nature; the cost is the multi-slot round machinery, named there.
- **The read-side cost, stated honestly.** A query with a privacy
  selection spans the silos its selection covers and merges results
  (an "at most X" read touches every silo at or below X's class,
  filtering by magnitude inside the boundary silo). Single-silo reads
  — the public-facing case — touch one store.
- **Reference direction is enforced.** A lower-privacy record must
  never reference higher-privacy content — the reference itself would
  leak; the higher may reference the lower. The write path refuses the
  wrong direction. How spirit's families (records, referents,
  migrations) place across silos is a pickup verification point
  (§12).

Backup posture follows directly, unchanged in spirit from the previous
revision: at least one all-silo mirror on a trusted host, any number
of public-silo mirrors on untrusted ones.

## 6 · Backup and restore — the same mechanism

A mirror is a backup because the mirrored artifact is the authoritative
one: the hash-chained log up to an authorized head. Restore is the
already-existing import path fed by a restore bundle (latest checkpoint
plus the suffix past it), assembled by any mirror host — member or
non-authoritative — through the engine's restore module. Under silos
(§5) a bundle is per silo: a full restore gathers every silo from
hosts trusted with each; a public-silo host restores the public silo
completely and nothing else — no placeholders, simply the silos it
holds. Trust on
restore is the same two checks as live apply: every digest re-derives,
and the terminal head is one the restoring host's criome confirms as
the authorized head of the followed contract (its own ledger for a
member; the follower chain, or a fresh evidence verification, for a
remote). Restore is owner-initiated through the component's meta
contract — a one-shot import, not a runtime pull loop; the (a)-shaped
"peer notifies, component fetches" pull remains what the slice design
already deferred it to: a repair and bootstrap path, not the propagation
path.

## 7 · Router ordering — a mirroring prerequisite

The design leans on per-destination delivery order: batch N+1 chains
onto batch N's head, the receiver refuses gaps, and no repair path
exists yet — so a reordered pair of batches wedges the mirror until
repair ships. The verified router facts (§1) say ordering does not hold
today. Two honest options:

- Make the receiver order-insensitive (park out-of-order batches).
  Rejected: it duplicates the router's queueing inside every component
  and turns a refusal into a buffer with its own durability questions.
- Restore per-destination first-in-first-out in the router. Chosen. The
  durable backlog rows already carry sequences; the fix is a
  per-destination delivery lane: one in-flight forward per destination,
  drained in sequence order, a failed forward retrying at the head of
  its own lane (head-of-line blocking per destination is exactly the
  desired semantics for a chained log), different destinations staying
  concurrent. The drain triggers stay the existing push seams
  (session-established, topology-learned). The backlog witness then
  asserts order instead of sorting it away.

Ordering is a property of routing, not of any payload, so this respects
"the router only routes." It should land before or with the pending
propagation slice, whose offline-delta behavior silently depends on it.

## 8 · Deprecation — what dies, with no compatibility path

Settled direction (the nbmq epic already drops the daemon; the deployed
service is already being disabled after crash-looping) carried to its
end. Order of operations:

1. **Salvage into sema-engine** (§3): the decision matrix with its
   refusal taxonomy and tests, the crash-window healing property and
   its witnesses, restore assembly, and the landed-body re-hash idea —
   which becomes the standing head-equality witness between two
   components' meta head observations.
2. **Land the component path** (with the pending propagation slice):
   typed apply-batch ingress wired in spirit (today refused), drain
   shipping over the router, receiving-side acceptance.
3. **Delete in consumers:** spirit's mirror-shipper feature,
   `src/shipper.rs`, the mirror-target meta configuration, and the
   mirror dependencies; router's witness feature, the
   forward-witness binary that hand-builds mirror appends, and the
   mirror dev-dependencies; the spirit cluster test's in-process mirror
   service replaced by a second spirit engine (the pending slice's
   loopcheck already specifies exactly that).
4. **Rebuild the VM cluster** with spirit + criome + router on both
   nodes; the witness becomes head equality between the two spirits'
   meta observations. The node-B mirror-daemon service and its
   configuration module go away; the temporary "disabled reversibly"
   state of the production mirror service becomes permanent removal
   from the deployment aggregate.
5. **Archive the repos** mirror, signal-mirror, meta-signal-mirror
   (read-only, history preserved). No compatibility relay, explicitly:
   there is no production consumer to relay for (verified, §1), a
   relay would keep the rejected direct-TCP transport alive beside the
   router path, and a compatibility shape kept for its own sake
   manufactures legacy. The meta-signal-mirror policy surface
   (store registry, retention placeholder) dies with the daemon;
   per-component retention policy, if ever wanted, belongs in that
   component's own meta contract.

## 9 · Judgment on the forwarded analysis

Agreed, and adopted: the reusable machinery belongs close to SEMA;
state-bearing components must depend on the shared layer, never on a
daemon crate; its two test-topology factual claims verified true; the
list of generic mechanisms (outbox and cursor, envelopes and suffixes
and head marks, append validation, crash-window healing, restore
verification) verified real and worth keeping — most already in or now
moving into sema-engine.

Rejected, with reasons:

- **New shared library ("component-mirroring" / "sema-mirroring").**
  sema-engine already owns half the vocabulary; the other half joins
  it. A new crate would cut one capability in two (§3).
- **Mirror daemon as a compatibility relay.** Contradicts the psyche's
  stated stance, the epic's settled drop, and the facts: nothing in
  production consumes it, and its only live transport is the rejected
  one. Delete, don't relay (§8).
- **Keep signal-mirror temporarily as the payload-blind protocol.** The
  shapes are worth keeping; the crate is not. They migrate redesigned
  into signal-sema (store-name strings die under enum addressing), and
  the crate archives in the same sweep (§3, §8).
- **Keep meta-signal-mirror for standalone daemon policy.** Moot once
  no standalone daemon exists; its retention order was an unenforced
  placeholder (§8).
- **Its spirit-specific inventory.** Mislocated: those pieces live in
  spirit and router, not in the mirror repos, and "router transport of
  opaque frames" was never a mirror piece. The correction changes the
  plan's shape from "extract generic parts out of mirror" to "merge the
  receive half into sema-engine and delete the rest" (§1).
- **Later schema/codegen for per-component mirrored stores.** Deferred
  rightly, but no new framework is needed: the per-component residue is
  exactly the existing schema-driven registrations (materializers, plus
  the record-to-silo placement) — three wiring points, not a codegen
  surface (§3).

## 10 · Slice map — composing with the pending slices

The pending slices (cluster authorization of a batched head advance;
propagation with receiving-side acceptance; the root-issued operational
sub-contract) stand as accepted, under amendment to the corrected
acceptance semantic by a parallel worker. The mirroring slices weave
around them; none blocks them except where marked.

- **M0 — router per-destination delivery lanes** (§7). Independent;
  should land before or with the propagation slice, which silently
  depends on ordering. Witness: backlog drain asserts sequence order
  per destination; two destinations drain concurrently.
- **M1 — shared wire vocabulary** (§3). signal-sema gains envelope /
  suffix / head-mark / restore-bundle / refusal records (payloads
  always carried; the sealed form died with the silo amendment);
  signal-spirit replaces the hex single-record apply with the typed
  apply-batch composing them. Lands with the propagation slice's
  contract work — same genesis sweep as the addressing consolidation.
- **M2 — engine receive half + evidence retention + drain** (§2, §3).
  Port the decision matrix and healing into sema-engine's import path;
  durable evidence rows keyed by entry digest, written in the
  acceptance transaction; generic propagation driver; spirit wires
  ingress (un-refuses the apply arm) and drain. This IS the
  implementation substance of the propagation slice's spirit side, plus
  the engine consolidation.
- **M3 — deletion** (§8 steps 3-5). Immediately after the propagation
  loopchecks are green on spirit-to-spirit; includes the VM-cluster
  rebuild and the repo archival.
- **M4 — non-authoritative remotes** (§4). After account issuance
  lands (the governance design's G4). Criome follower admission and
  verification path; member targets ride the grant, remote targets
  come from the mirror-list log (the governance design's G5).
  Loopcheck: a third, non-member node converges through evidence
  verification alone, and its local write attempt refuses.
- **M5 — privacy silos** (§5, rewritten). The multi-store split (one
  store per silo, plus the mirror-list log), the record-to-silo
  placement, per-silo heads under the governance design's G6, and
  silo-selective shipping. No digest schema change. Loopcheck: a
  public-silo remote converges on the public silo alone, serves public
  observations, and never receives a single private-silo byte; a
  cross-silo move lands atomically on both silos; an all-silo restore
  round-trips completely.
- **M6 — backup restore proof** (§6). Owner-initiated restore of a
  fresh node from a mirror host through the meta contract, one bundle
  per silo, verified against the authorized heads. Closes the "the
  same mechanism is the backup mechanism" loop end to end.

## 11 · Open questions — only the psyche can answer

1. **Metadata leakage on public-only remotes — RESOLVED by the silo
   amendment (2026-07-07).** Private entries are entirely absent from
   what an untrusted host receives — not sealed, absent — and no
   derived chain was needed, because silos are primary logs (§5,
   rewritten). The residual psyche question is the silo set itself
   (which partition of the magnitude scale), recorded in
   `CriomeStateGovernanceDesign.md` §12.
2. **Where replication targets live — RESOLVED by the psyche
   (2026-07-07):** "the list of mirrors is in spirit, changes gated in
   criome. just another log, like the privacy silos." See the amended
   §4 and `CriomeStateGovernanceDesign.md` §5.3.
3. **Remote liveness as a replica** (§4). May a non-authoritative
   remote's component serve reads (a live observation replica for
   public data), or should it be dormant storage only? This decides
   whether its ordinary contract socket is enabled at deployment.
4. **Repo disposal ceremony** (§8). Archive the three mirror repos
   read-only, or delete outright? History preservation versus surface
   reduction — an ownership call, not a technical one.

## 12 · Worker verification points at pickup

1. The amended `ClusterAuthorizationSliceDesign.md` — confirm the
   corrected acceptance semantic's final wording before implementing M2
   (this design assumes: no grant, no record, anywhere).
2. Evidence retention shape: confirm the grant/evidence types criome
   pushes on Granted are stable enough to persist keyed by entry digest
   (they are the §4 hand-off in the pending slice).
3. The multi-store (per-silo) layout: confirm sema-engine's store
   naming, checkpointing, and outbox surfaces compose per silo with no
   cross-store assumptions (one chain per store is already the built
   shape), and settle spirit's family placement across silos (records,
   referents, migrations — including where referent registrations of
   private records live) before M5 freezes the store set.
4. Router backlog rows: confirm the recorded sequence is per-router
   global (sufficient — per-destination order falls out of filtering by
   destination) rather than per-destination, and that retry-at-head is
   expressible in the settle handler.
5. Confirm no other consumer of signal-mirror exists outside spirit and
   router (a lock-file sweep across the component repos) before the M3
   deletion.
