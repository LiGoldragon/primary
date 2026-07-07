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
  typed ordered level, queried with selections such as "at most public."
  There is no separate public/private record class; this magnitude is
  the class vocabulary.

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
  (`versioning.rs:328-338`) — so today a payload cannot be withheld
  without breaking chain verification. §5 turns on this fact.
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
3. The grant comes back carrying the propagation targets: the quorum
   members minus this host, plus every configured non-authoritative
   remote, each target as (Criome host ID, privacy ceiling). The
   component commits the entry and stores the grant evidence beside it,
   in the same transaction, keyed by the entry digest — so a crash
   between acceptance and shipping loses nothing.
4. The component's propagation drain (a background actor, pushed a mail
   on every commit — never polling) frames the unshipped suffix as one
   typed apply-batch per target: the ordered entries, the authorization
   identifier (contract digest plus authorized head reference), and the
   evidence. Entries above a target's privacy ceiling ship sealed (§5).
   Each batch goes to the local router addressed to (target host ID,
   same component kind) — spirit to spirit, mind to mind. The shipped
   cursor advances when the local router has durably accepted the
   batches; from there delivery is the router's job, ordered per
   destination (§7), held in its durable backlog while a peer is away
   and drained on the session-established push.
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

- Send: suffix framing into wire envelopes; sealing per privacy ceiling
  (§5); durable evidence retention keyed by entry digest; the generic
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
(sequence, previous digest, digest, payload — carried or sealed), the
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
   directory already does this) and, for §5, a privacy projection per
   family — the one place the payload-blind engine learns a record's
   privacy magnitude.
3. Its daemon wires the propagation drain to its criome authorization
   session and its local router client.

Everything else — validation, healing, cursor, sealing, restore — is
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
then pushes the operational quorum sub-contract together with its
root-round evidence; the remote's criome verifies that chain against
the pinned anchor and admits the contract as a followed contract — it
knows the member set, the threshold, and the replication targets, and
can see itself listed. That admitted contract is precisely "awareness
of that quorum which allows for the state change."

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

**Where the target list lives.** Replication targets are cluster
policy, so they belong in the operational quorum sub-contract document
itself: beside members and threshold, a replication section listing
(Criome host ID, privacy ceiling) per non-authoritative remote. This
makes the target set cluster-agreed, anchored, identical on every
member, and visible to the remote; changing it is issuing a replacement
sub-contract — the same seam as membership rotation. The alternative
(per-host owner configuration) is lighter to change but lets members
disagree about where state flows, which for private data is a safety
property, not a convenience. Recommended: in the contract. This is an
open question only in its operational weight (§11).

**Scaling down: the backup case.** A single host wanting off-site
backups is a single-member cluster (the root and a one-member
operational sub-contract) with one or more non-authoritative remotes,
public-only or full per trust. Nothing about mirroring is
cluster-sized; the quorum of one is the degenerate case of the same
design.

## 5 · Record-class gating — privacy ceilings and sealed payloads

The gate reuses spirit's existing privacy vocabulary: each target
carries a privacy ceiling (a "at most this magnitude" selection, e.g.
at-most-public). No new record-class enum; the magnitude is the class.

The obstacle is a verified fact: entry digests fold raw payload bytes,
so an entry whose payload is withheld cannot be verified, and the chain
breaks for every entry after it. Filtering the log is therefore
impossible today without abandoning verification — which is the whole
point of mirroring.

**Resolution: seal, do not omit.** One deliberate storage-schema
change, versioned as the next entry-digest domain tag: the per-operation
digest folds a payload commitment (the digest of the payload bytes)
instead of the raw bytes. Then a shipped envelope carries each payload
either in the clear or sealed — replaced by its commitment. A sealed
entry verifies identically everywhere: the chain, the head, the
evidence all still check. The component's registered privacy projection
(§3, wiring point 2) tells the engine each record's magnitude; the
drain seals every payload above the target's ceiling. The public-only
remote thus holds the complete verified chain skeleton with only public
payloads materialized: a genuine backup of all public data plus
integrity of the whole history, restorable and verifiable, on a host
trusted with none of the private content.

Consequences, stated plainly:

- This is a breaking change to the digest schema. Existing chains
  re-genesis or re-derive under the new tag; there is no compatibility
  path, consistent with settled intent. It should land in the same
  sweep as the other contract-genesis changes of the pending slices.
- A restore from a public-only remote returns sealed placeholders for
  private records; the restoring component materializes public rows and
  records the sealed identities as unrecoverable-from-this-source. A
  full restore needs a full-ceiling mirror. Backup posture follows
  directly: at least one full-ceiling mirror on a trusted host, any
  number of public-only mirrors on untrusted ones.
- Metadata is not sealed. A public-only remote still learns that
  private entries exist, their timing, family, key, and size. If that
  leakage is unacceptable, the alternative is omitting private entries
  entirely, which requires a second, derived public-only chain with its
  own authorized head — materially more machinery (two heads per
  acceptance, projection maintenance, double evidence). Recommended:
  sealed placeholders now; the derived-chain design only if the psyche
  rules the metadata leak out (§11).

## 6 · Backup and restore — the same mechanism

A mirror is a backup because the mirrored artifact is the authoritative
one: the hash-chained log up to an authorized head. Restore is the
already-existing import path fed by a restore bundle (latest checkpoint
plus the suffix past it), assembled by any mirror host — member or
non-authoritative — through the engine's restore module. Trust on
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
  the new privacy projection) — three wiring points, not a codegen
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
  suffix / head-mark / restore-bundle / refusal records (payload
  carried-or-sealed from day one, even before M5 uses sealed);
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
- **M4 — non-authoritative remotes** (§4). After the sub-contract
  slice (the replication section rides the sub-contract document).
  Criome follower admission and verification path; target resolution
  becomes members-minus-self plus replication targets. Loopcheck: a
  third, non-member node converges through evidence verification alone,
  and its local write attempt refuses.
- **M5 — privacy ceilings and sealed payloads** (§5). The digest
  domain-tag change plus sealing plus spirit's privacy projection.
  Loopcheck: a public-only remote converges with private payloads
  sealed, serves public observations, and a restore from it yields
  sealed placeholders; a full-ceiling restore round-trips completely.
- **M6 — backup restore proof** (§6). Owner-initiated restore of a
  fresh node from a mirror host through the meta contract, verified
  against the authorized head. Closes the "the same mechanism is the
  backup mechanism" loop end to end.

## 11 · Open questions — only the psyche can answer

1. **Metadata leakage on public-only remotes** (§5). Sealed payloads
   hide content but reveal existence, timing, family, key, and size of
   private records to the untrusted host. Acceptable, or must private
   entries be entirely absent (which buys a second derived chain and
   its double-authorization machinery)?
2. **Where replication targets live** (§4). Recommended: in the
   operational quorum sub-contract, so the target set is cluster-agreed
   and anchored — at the cost that adding or dropping a backup host is
   a sub-contract reissue. Per-host owner configuration is the lighter
   alternative with weaker guarantees. Which weight is right?
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
3. The sealed-payload envelope must round-trip through the same rkyv
   archive path as carried payloads — verify signal-sema's codec plan
   against sema-engine's archived entry layout before M1 freezes types.
4. Router backlog rows: confirm the recorded sequence is per-router
   global (sufficient — per-destination order falls out of filtering by
   destination) rather than per-destination, and that retry-at-head is
   expressible in the settle handler.
5. Confirm no other consumer of signal-mirror exists outside spirit and
   router (a lock-file sweep across the component repos) before the M3
   deletion.
