# Criome / Spirit / Router Fabric — System and Test Overview

Retired vocabulary (psyche ruling 2026-07-21): "mouth" -> textual interface; "organs" -> the two trees (nametree, structuretree); "spine" -> core invariant / core pathway; "door" -> entry point; "currency" -> value type. Historical text below is unreworded; read it through this table.

The comprehensive, source-grounded map of the criome cluster-propagation fabric
and its entire test surface. Written for the psyche, who is not fluent in the
agent-coined vocabulary: every term is defined on first use. Read-only survey;
no code was edited and no tracker item mutated.

Verified against source on 2026-07-09, ghq checkouts under
`/git/github.com/LiGoldragon/` (the primary workspace's `repos/` is a symlink to
that path, so both names denote the same clones). Every load-bearing claim
carries a `repo/path:line` citation.

## How to read this document

Two labels run throughout, and they are the whole point of the survey:

- **LANDED** — the behavior exists in committed source on the checked-out head,
  and (where noted) has a test that witnesses it. This is what the machine
  actually does today.
- **DESIGNED-ONLY** — the behavior is specified in an accepted design document
  in this directory but is *not* in the code yet. This is a plan, not a fact.

Three accepted designs are the source of the DESIGNED-ONLY material, all in
`/home/li/primary/agent-outputs/PersistentSpiritMirror/`:

- `ClusterAuthorizationSliceDesign.md` — the everywhere-gate slice (the gate that
  is now LANDED), propagation shape (b), and sub-contract staging.
- `CriomeStateGovernanceDesign.md` — the account/referred-state model: criomes
  ARE the accounts; one quorum-authorized state-change primitive; bounded
  history; the `Contract`→`Criome` and `ExplicitApproval` renames.
- `ComponentMirroringCapabilityDesign.md` — mirroring folds into sema-engine as a
  component capability; the mirror stack is deleted; privacy silos (one for now).

A note on three words that are easy to confuse, resolved here once:

- **criome** (lowercase) — the running program, one per host, that owns all
  cryptography and authorization.
- **Criome / `Contract`** (capitalized, a record type) — one *account*: a tiny
  rule+parent record the criome program keeps. The code still calls this type
  `Contract`; the rename to `Criome` is DESIGNED-ONLY.
- **contract** (as in *signal-contract* / *wire contract*) — the typed
  operation/reply surface a component speaks over its socket. Unrelated to the
  account record; the naming collision dissolves once the account is renamed.

## 0 · Vocabulary (defined once, used throughout)

- **Component** — one program with one job on a host: `spirit` (keeps intent
  records), `criome` (keeps identity and authorizes changes — all cryptography
  is its domain), `router` (carries frames across the network — it only routes),
  `sema-engine` (the shared database engine the state-bearing components embed),
  and later siblings such as `mind`. Each host runs exactly one of each.
- **The triad split (daemon + CLI + contract)** — each component is three
  crates: a `signal-<name>` crate holding the *wire contract* (the typed
  request/reply records peers send, no runtime), a `meta-signal-<name>` crate
  holding the *owner-only* configuration contract, and the component crate itself
  holding the daemon, the thin CLI, and the storage. `component-architecture`
  and `contract-repo` are the doctrine for this shape.
- **Hash-chained commit log** — sema-engine records every state change as a log
  entry whose **digest** (a cryptographic fingerprint) folds in the previous
  entry's digest, so one digest pins the whole history beneath it. The newest
  entry's digest is the **head**. A **head advance** is any operation that
  appends (a record, a supersede, a retire).
- **Quorum / two-round commit** — the founded cluster of criome hosts. To
  authorize one proposed head digest they run a *two-round commit*: a
  first-round majority opens a second round, a second-round majority authorizes.
- **BLS** — the signature scheme criome uses (Boneh–Lynn–Shacham); its property
  that matters here is that many members' signatures over the same statement can
  be verified against the member set. The **grant** is the cluster's signed
  "yes" for one digest; the **evidence** is the assembled member signatures that
  let *any other* criome re-verify the grant independently.
- **The everywhere-gate** — the LANDED acceptance rule: when criome
  authorization is *Enabled*, spirit accepts a head advance *only after* the
  cluster grants its digest; a refused advance is recorded nowhere, including
  locally (fail-closed). Reads are never gated. *Disabled* (the default) keeps
  spirit fully local and the whole seam dormant.
- **Staging seam** — sema-engine's ability to *build* a would-be log entry group
  and compute the head it *would* produce, park it durably, then either
  *materialize* (append) it on a grant or *discard* it on a refusal.
- **Account (criome) vs referred state** — the two states criome keeps apart. An
  *account* is a tiny rule+parent record (pure authority: who may change what).
  *Referred state* is the bulk the account governs (spirit's intent log, the
  mirror-target list). Accounts are small, slow, and travel wide; referred state
  is bulky, fast, sparse, and prunable.
- **Governed state slot** — DESIGNED-ONLY: one named piece of referred state
  under one account, changed by the same proposal→quorum→grant primitive.
- **Criome host ID = identity** — a host's network identity IS its criome's
  master public key. A network destination is the pair `(CriomeHostId,
  ComponentKind)`; there is no other name service.
- **Non-authoritative remote** — the git-remote analogy: a host that runs criome
  plus a mirrored component, follows the cluster's state by verifying evidence,
  but is not a quorum member and can authorize nothing.
- **Test vocabulary** (used in §5): a **flake check** is a pure, self-contained
  test the Nix flake exposes and `nix flake check` sweeps; a **stateful named
  output** is a Nix package (`nix build .#<name>`) that stands up real daemons
  over sockets and is *not* swept automatically; a **loopcheck** is the informal
  name for such a stateful, multi-daemon, in-process integration proof.

## 1 · Executive picture — the fabric in plain language

The fabric is one distributed engine assembled from small single-purpose
components that talk over local Unix sockets and, across hosts, over one network
carrier.

**spirit** is the record keeper. It stores the psyche's intent as an append-only,
hash-chained log and answers reads and writes over its socket. It knows nothing
about cryptography or quorums.

**criome** is the authority. It holds the host's keys, it is the only component
that signs or verifies anything, and it decides whether a proposed change is
authorized. It runs the two-round commit across the cluster.

**router** is the carrier. It moves opaque frames between hosts, addressed only
by `(host, component)` and routed by general type; it understands neither intent
records nor quorum votes — it just routes.

**sema-engine** is the shared database engine spirit and criome both embed. It
owns the hash-chained log, the digest math, the outbox (the "shipped up to here"
cursor), and — new — the staging seam.

They compose into one engine by a strict division of labor. When the gate is
*Enabled* and a write reaches spirit, spirit does not commit it. It *stages* the
would-be entry and computes the head digest it would produce, then asks its
*local* criome, over a socket, to authorize that one digest. Criome runs the
two-round commit across the founded cluster (carried by the router) and, only if
a majority signs, returns a grant. Spirit then materializes the staged entry and
replies "accepted." If the answer is anything else — denied, the window expired,
no cluster, criome unreachable — spirit discards the staged entry and returns a
typed refusal, and no reader ever sees the operation. **The grant is the
acceptance event; acceptance and the write are the same thing.**

The account/referred-state model (DESIGNED-ONLY as an explicit substrate, but
already the mental model criome is built around) says criome keeps two kinds of
state strictly apart. The *accounts* — the criomes — are tiny rule+parent records
that say who may change what; they form a tree rooted at the one founding
ceremony. The *referred state* is everything those accounts govern: spirit's
intent log, and (designed) the mirror-target list. The vision, in the psyche's
words, is that "the accounts (what I called the criomes) and the state they refer
to" are the two layers, and *a new account is itself a state change* proposed
through its parent's quorum — one primitive governs everything, and history stays
bounded because only the live tree plus its newest evidence is retained (never
"another infinitely-sprawling blockchain").

Identity threads all of it: a host's identity is its criome's master public key
(the *Criome host ID*), and every network destination is `(Criome host ID,
component)`. There is no separate node registry.

## 2 · Component ledger

Status key: LANDED = in code on the checked-out head; DESIGNED-ONLY = specified
but absent. Versions and heads are the survey-time truth (see §6 for the full
table).

### criome — the authority (identity, cryptography, quorum)

- **criome 0.8.2** (`criome/Cargo.toml:3`, head `a82b514`). Responsibility:
  hold the host's BLS master key, register and verify identities, keep the
  account tree, and run the two-round commit that authorizes head advances.
- Daemon/CLI/contract split: daemon in `criome/src/daemon.rs` and the actor tree
  under `criome/src/actors/` (the schema-root actor `root.rs`); wire contract in
  **signal-criome 0.11.0** (`signal-criome/Cargo.toml:3`, head `5998cf2`);
  owner-only config in **meta-signal-criome 0.6.0** (head `fdc71cc`). ARCHITECTURE
  (`criome/ARCHITECTURE.md:1-32`) frames it as "a minimal Spartan BLS-signature
  authentication and attestation substrate," Telos's "agreement-and-authorization
  organ."
- Key types (LANDED): the account record `Contract { rule, contract_parent }`
  (`signal-criome/src/schema/lib.rs:789-792`); the parent enum `Root |
  Parent(ContractDigest)` (`:778-781`); the 11-variant `Rule` enum
  (`:959-971`) including the bare `EscalateToPsyche`; `AuthorizedObjectKind
  { Operation, Contract, Agreement, Time, Head }` (`:1389-1395`);
  `AuthorizationMode { Quorum, AutoApprove, ClientApproval }` (`:458-462`).
- Two-round commit (LANDED): ingress `cluster_authorize_signal_call`
  (`criome/src/actors/root.rs:1317-1479`), Request round
  `propose_quorum_authorization` (`:2020-2097`), Commit round driven only by the
  originator `drive_commit_round` (`:2473-2562`), majority judge via the reused
  `ContractStore::evaluate` (`:2343-2383`), independent per-peer witness-clock
  re-check `solicit_quorum_vote` (`:2143`) and signer gate `cast_quorum_vote`
  (`:2419-2442`). Immediate re-grant of a standing committed head with no new
  round: `re_grant_standing_head` (`:1533-1587`).
- Dead-round supersession (LANDED — see §7 for the risk it carries):
  `SuccessorLedgerPoint` (`root.rs:131`), `RecordedRoundLife { Committed, Live,
  Dead }` (`:175-187`), `CoSignAdmission { RecordFresh, AlreadyRecorded,
  RefusedSelfLoop, RefusedConflict, SupersedeDeadRow }` (`:138-156`); the
  admission matrix `co_sign_admission` (`:221-248`). The old catch-up stage
  (`HeadAuthorizationStage::CatchingUp`) is GONE (grep-confirmed absent).
- DESIGNED-ONLY on criome: the `Contract`→`Criome` rename (still `Contract`);
  the `ClientApproval`→`ExplicitApproval` rename (still `ClientApproval`,
  `signal-criome/src/schema/lib.rs:461`, used at `root.rs:534,560,1046`); removal
  of `EscalateToPsyche` (still present, 11 variants); the governed-slot substrate;
  closing the unauthenticated `AdmitContract` admission hole (see §4).

### spirit — the record keeper

- **spirit 0.24.0** (`spirit/Cargo.toml:3`, head `33f16e7`). Responsibility:
  store intent records in a hash-chained log and serve them; under the gate,
  route every head advance through the local criome first. ARCHITECTURE narrates
  the everywhere-gate at `spirit/ARCHITECTURE.md:248-326`.
- Split: component crate `spirit`; wire contract **signal-spirit 0.13.0**
  (`signal-spirit/Cargo.toml:3`, head `1cf7c01`); owner-only config
  **meta-signal-spirit 0.7.1** (head `0a7a243`).
- The LANDED gate:
  - Gate mode `CriomeAuthorization { Disabled (default), Enabled(ClusterAuthorizer) }`
    (`spirit/src/criome_gate.rs:134-142`); `ClusterAuthorizer { socket, deadline }`
    (`:150-153`, default session deadline 120s at `:162`); owner switch at
    `engine.rs:668-685`.
  - Session-parse matrix `HeadSessionBinding::decide` (`criome_gate.rs:308-366`):
    slot binding ignores foreign slots (`:312-315`), digest binding (`:316-326`),
    terminal `Granted` requires a bound grant — "status alone is never proof"
    (`:331-347`), non-Granted terminals map to typed refusals (`:348-357`).
    `GateDecision { Authorized, Refused(GateRefusal), Unreachable }` (`:375-389`).
  - Three-phase intake: `Engine::stage_working_input` (`engine.rs:831-882`),
    `Engine::conclude_staged_advance` (materialize-or-discard, `:895-937`),
    crash-recovery `resolve_parked_staged_group` (`:948-982`) run before the
    residue reconcile in `configure_async` (`:984-1007`); startup surfaces an
    occupied slot at `daemon.rs:147-155`.
  - FIFO advance lock `advance_gate: Mutex<()>` (`engine.rs:330-331`), shared to
    the daemon spine (`daemon.rs:235-240`) and the ship drain
    (`propagation.rs:50,87`): one outstanding staged group; reads bypass it.
  - Intake classification (`daemon.rs:183-211`): head-advancing (staged) =
    `State, Record, Propose, Clarify, ResolveClarification, Supersede, Retire,
    ChangeCertainty, BumpImportance, ChangeRecord, RegisterReferent`; ungated
    (immediate) = all reads plus `ApplyAuthorizedRecord`.
  - `propagation.rs` is now ship-only + residue reconciler — it no longer gates
    ("acceptance happens on the intake path … this drain therefore never gates,"
    `propagation.rs:1-28`, `drain_once` `:86-99`).
- signal-spirit contract (LANDED): `Output::AdvanceRefused(AdvanceRefusal)`
  (`signal-spirit/src/schema/signal.rs:2170`) over the closed 4-reason enum
  `AdvanceRefusalReason { Denied, Expired, Unavailable, Unreachable }` (`:830-835`);
  privacy is `Privacy(Magnitude)` (`:1345`) over the 8-step `Magnitude { Zero,
  Minimum, VeryLow, Low, Medium, High, VeryHigh, Maximum }` (`:2092-2101`).
- Feature seams (LANDED): `criome-gate = ["dep:criome","dep:signal-criome"]`
  (`spirit/Cargo.toml:72`) holds the acceptance gate as its *own* feature so it
  is never compiled out with shipping; `mirror-shipper = ["criome-gate",
  "dep:mirror","dep:signal-mirror"]` (`:79`) holds the (legacy) ship path;
  `cluster-authorization-e2e` and `offline-full-chain-e2e` pull the loopcheck
  legs (`:86,:91`).
- DESIGNED-ONLY on spirit: the batch apply ingress (`ApplyAuthorizedRecords`;
  today only the single-record `ApplyAuthorizedRecord`
  (`signal.rs:330,2130`) exists and is parked/fail-closed at
  `nexus.rs:1282-1284`); the mirror-list log replacing the owner-configured
  `SelectedMirrorTarget`/`MirrorTarget` (`shipper.rs:32,70`); privacy silos (one
  `Primary` store today); removal of the mirror-crate dependency from the shipper
  (`shipper.rs:25` still `use mirror::{ComponentShipper, ShipOutcome}`).

### sema-engine — the shared database engine

- **sema-engine 0.7.0** (`sema-engine/Cargo.toml:3`, head `b3b5fb7`); shared
  contract **signal-sema 0.2.0** (head `8cc1929`). Responsibility: hash-chained
  commit log (one chain and one head *per store*), digest math, outbox cursor,
  atomic entry+outbox+counters transactions, and the staging seam.
- Digest (LANDED): the entry digest folds store name, per-family schema hashes,
  commit sequence, snapshot, previous entry digest, and the ordered
  operations/payload — **no wall clock** (`sema-engine/src/versioning.rs:216-285`),
  which is what makes a staged digest deterministic.
- Staging seam (LANDED): `pub mod staging` (`src/lib.rs:27`), the durable
  one-slot table `__sema_engine_staging_slot` (`src/staging.rs:50`),
  `StagedOperationGroup` / `StagedGroupSummary` / `StagingSession`
  (`src/staging.rs`, re-exported `lib.rs:64-66`), the engaged-session mutex on
  `Engine` (`src/engine.rs:97`), and typed staging faults
  (`src/error.rs:176-205`). This is the substrate the spirit gate's
  stage/materialize/discard sits on.
- DESIGNED-ONLY on sema-engine: the `mirroring` module family (the fold of the
  mirror stack's receive half — decision matrix, restore assembly, evidence
  retention). Absent today (grep-confirmed); signal-sema does not yet carry the
  entry-envelope / suffix / head-mark / restore-bundle wire vocabulary.

### router — the network carrier

- **router 0.6.0** on the *unmerged* branch `router-per-destination-fifo`
  (head `ab1c726`); `origin/main` is 0.5.0 (`47f2882`, per bead primary-ok91).
  Responsibility: carry opaque frames between hosts addressed by `(Criome host
  ID, component)`, route by general type only, and hold undeliverable frames in a
  durable backlog until the peer returns.
- Split: `router`; wire contract **signal-router 0.5.0** (head `501308d`);
  owner-only config **meta-signal-router 0.4.0** (head `1475d4b`).
- LANDED: the durable outbound backlog and drain-on-session-established; the
  per-destination FIFO forward lanes `RemoteForwardLanes` (`router/src/router.rs:2131`)
  and `HeldBacklog` (`:2157`) with `BacklogSequence` enqueue stamps
  (ROUTER_SCHEMA_VERSION 4) — one in-flight forward per destination, different
  destinations concurrent; the encrypted authenticated peer session and the
  mutual criome-issued identity proof.
- DESIGNED-ONLY / not-yet-landed on router: the §1 addressing consolidation is
  only *partly* landed — `router/src/authorized_object_projection.rs` still
  exists (the design deletes it), and the FIFO work is on a branch, not main.
  Router source also *lags* the current contract stack: it does not yet build
  against signal-criome 0.11.0 (36 errors, primary-ok91) — the loopcheck's router
  leg (§5, §7).

### signal-standard — the single shared vocabulary

- **signal-standard 0.2.0** (head `feb6cd0`). Owns the one closed vocabulary the
  fabric addresses by: `ComponentKind` (14 variants — `Spirit, Mind, Criome,
  Message, Router, Mirror, Terminal, Harness, Agent, System, Introspect,
  Orchestrate, Lojix, Persona`, `signal-standard/src/schema/lib.rs:31-45`; note
  `Mirror` is still a variant), `AuthorizedObjectKind` (`:63`),
  `AuthorizedObjectReference` (`:166`), and `ObjectDigest(String)` (`:112`).
- DESIGNED-ONLY: `ObjectDigest` and `CriomeHostId` becoming *typed key bytes*
  (both are still string-backed — `CriomeHostId::new("router-local")` at
  `router/src/router.rs:1207`); `AuthorizedObjectKind::Contract`→`::Criome`;
  full re-export so twin copies dissolve (signal-criome still carries its own
  `ComponentKind` reference in `src/schema/lib.rs`).

### The mirror stack — DELETION-slated

- **mirror 0.2.0** (head `b8cf8ec`), **signal-mirror 0.1.1** (`d2d3c61`),
  **meta-signal-mirror 0.2.0** (`ad0259d`). A standalone mirror-daemon plus two
  contract crates. Its *receive half* is the machinery the mirroring design folds
  into sema-engine: the append decision matrix `AppendDecision` /
  `suffix_inconsistency` / `known_divergence`
  (`mirror/src/decision.rs:28,122,181`), checkpoint/notice decisions (`:228,267`),
  and landed-body re-hash `content_address` (`mirror/src/readback.rs:42`).
- Status: DELETION-slated per `ComponentMirroringCapabilityDesign.md` §8. Still
  consumed today (the tension in §7): spirit's `mirror-shipper` feature pulls
  `dep:mirror` + `dep:signal-mirror` (`spirit/Cargo.toml:79,158,169`) plus a
  non-optional `meta-signal-mirror` (`:231`); router's `witness` feature and
  dev-deps pull mirror/signal-mirror (`router/Cargo.toml:68,79,91,96`). The
  deployed `mirror.service` was crash-looping (redb schema mismatch) and is being
  disabled on all hosts (bead primary-nbmq note). mirror 0.2.0 additionally
  fails its own build: `build.rs` panics on the schema strict-positional
  migration (`ExplicitFieldOnUniqueProductComponent`, bead primary-ok91).

### The primary workspace

- Not part of the runtime fabric: it is the orchestration and knowledge surface.
  It hosts the accepted designs and reports (`agent-outputs/`), the bead tracker
  (queried in §7), the generated skills, and the clones (`repos/` → the ghq
  path). Its boot contract is `AGENTS.md`; work on primary lands on `main`
  directly via `jj`. Agents register a Session/Lane through `meta-orchestrate`
  and claim shared paths before editing (this survey ran under Session
  `CriomeClusterPropagation`, Lane `system-and-test-overview`).

## 3 · Channel & flow ledger — worked flows with trust boundaries

Trust-boundary convention below: **[crypto]** marks where signatures are made or
verified (criome only); **[socket]** marks the local Unix-socket trust boundary
(caller identity is the socket's uid/mode, not a signature); **[opaque]** marks
where the router carries bytes it cannot read.

### Flow A — a spirit head advance under the gate (LANDED)

The stage→authorize→materialize path, fail-closed:

1. A write (say `Record`) reaches spirit's working socket **[socket]**. The
   daemon classifies it as head-advancing (`daemon.rs:183-195`).
2. **Stage** (fast, local): `stage_working_input` runs the nexus pipeline in
   build mode against committed state, assembles the would-be entry group, parks
   it in the durable staging slot, and computes the prospective head digest —
   nothing is committed (`engine.rs:831-882`; sema staging seam,
   `staging.rs:50`). A non-accepting result short-circuits and completes here.
3. **Authorize** (the round): on the connection task (off the engine mailbox, so
   reads keep flowing), `StagedHeadAdvance::resolve` opens a session to the local
   criome and submits `AuthorizeSignalCall` for the prospective digest
   (`criome_gate.rs:469-482,185-250`) **[socket]**.
4. Criome runs the two-round commit (Flow C) **[crypto]**, carried peer-to-peer
   by the router **[opaque]**, and pushes a terminal verdict back on the session.
5. `HeadSessionBinding::decide` parses the verdict (`criome_gate.rs:308-366`):
   only a `Granted` bound to the exact slot and digest, *with* the grant present,
   is `Authorized`; every other terminal is a typed refusal; a dead socket is
   `Unreachable`. Spirit never verifies BLS itself — the socket is the trust
   boundary.
6. **Materialize or discard** (fast, local): on `Authorized`,
   `conclude_staged_advance` atomically appends the staged entries, writes their
   outbox rows, clears the slot, and releases the held `RecordAccepted`
   (`engine.rs:895-908`). On any refusal it discards the slot and returns
   `AdvanceRefused(<reason>)` (`:919-934`); nothing was appended, no reader ever
   saw it.

Falsification the code enforces: if spirit bypassed criome the refusal path
would still accept; if the parse trusted status without the grant, a crafted
"Granted-without-grant" daemon would be accepted. Both are refused
(`cluster_gate_session.rs`, §5).

### Flow B — a founding ceremony (LANDED)

The one account birth that is *not* a proposed state change; it is the axiom the
tree rests on.

1. The founding nodes' criomes each hold their BLS master key **[crypto]**. The
   owner initiates founding on the owner-only *meta* socket **[socket]**
   (`meta-signal-criome`); there is no auto-approval — acceptance is an explicit
   owner act (`root_founding.rs`, criome tests §5).
2. Each node's criome signs the founding cohort unanimously **[crypto]**; the
   signatures are conveyed between nodes (directly, or — the router-mediated
   analogue — over the router **[opaque]**, `founding_over_router.rs`).
3. The result is the **founding anchor**: a digest committing to the founding
   keys, which every verifier pins as the trust root. Both nodes reach
   `RootFoundingState::Founded` on the *same* anchor; a reboot re-verifies the
   persisted anchor and never re-founds (`root_founding.rs` witnesses, §5).

### Flow C — a two-round quorum commit (LANDED)

How the quorum authorizes one proposed head digest for Flow A:

1. The originator opens the **Request** round (`propose_quorum_authorization`,
   `root.rs:2020-2097`), recording its own anti-equivocation row before its own
   vote. The proposal, its votes, and its solicitations ride the router
   **[opaque]** to the members.
2. Each member independently re-checks the time window against its *own* clock
   (`solicit_quorum_vote`, `root.rs:2143`) and casts a BLS vote **[crypto]**
   bound to `{signer, operation, moment}` (`language.rs:209-219`) — members
   auto-approve well-formedness only; no lineage or threshold predicate beyond
   membership exists yet.
3. On a first-round majority the originator drives the **Commit** round
   (`drive_commit_round`, `root.rs:2473-2562`). A second-round majority makes the
   round `Authorized` via the reused `ContractStore::evaluate` (`:2343-2383`);
   the grant plus assembled **evidence** is stored and pushed to the waiting
   session. There is no third round.
4. Peer-unreachable genuinely *waits* (withheld, never last-writer-wins); the
   window is the bound on how long the caller waits before a definite verdict.
   A window-dead, never-committed row becomes supersedable (§7 risk).

### Flow D — propagation / mirroring (mixed: current reality vs designed fold)

**Current reality (LANDED, but off the modern stack):** under `mirror-shipper`,
after materialization spirit's ship drain frames the unshipped outbox suffix and
hands it to the `mirror` crate's `ComponentShipper` (`spirit/src/shipper.rs:25,
132-207`), which either ships to an owner-configured `MirrorTarget::Address`
socket or (in the loopcheck) to an in-process mirror service. The router's role
here is the criome *authorization* traffic, not the mirror payload. This path
depends on the deletion-slated mirror crate and does not build against the
current contract stack (§7).

**Designed fold (DESIGNED-ONLY):** mirroring becomes a verb of the component
itself, implemented once in sema-engine and spoken over each component's own
contract. On a grant, spirit frames the authorized suffix as one typed
`ApplyAuthorizedRecords` batch per target — members ride the grant (criome's
knowledge), remotes come from spirit's own mirror-list log — addressed to
`(target host, Spirit)` and handed to the *local* router **[opaque]**. The
receiving spirit hands the carried authorization to *its* criome **[crypto]**
before applying: a member recognizes the round in its ledger, a follower verifies
the evidence — acceptance-by-verification, no second round. sema-engine's ported
decision matrix then chain-checks and folds atomically. A backup is the same
mechanism (a restore bundle imported through the same validation). The mirror
daemon's whole reason to exist — being the receiving mailbox — becomes the
sibling component itself.

Across all flows: **cryptography happens only in criome**, at both ends of every
network boundary; **spirit is quorum-ignorant** and trusts the socket; **the
router carries opaque frames and routes by `(host, component)` only** — no criome
or spirit concept leaks into it.

## 4 · Trust and state boundaries; the authorization / evidence model

- **The socket is the trust boundary.** Spirit asks its local criome over a Unix
  socket and consumes the verdict as fact; it never verifies BLS. The working
  socket is group-accessible (ordinary requests); the *meta* socket is owner-only
  (mode 0600) and carries owner acts (founding accept, configuration). Caller
  identity on a socket is the uid/mode, not a signature.
- **Cryptography is criome's domain, both ends.** A grant is criome's signed
  "yes"; the **evidence** is the assembled member BLS signatures that let any
  *other* criome re-verify the grant against the member set independently. This
  is what makes the designed receiving-side acceptance sound: a peer re-judges the
  carried evidence with its own criome, so no spirit can skip authorization.
- **Fail-closed everywhere.** Missing store/registry, unreachable criome, expired
  window, off-contract reply, machinery fault — all refuse. There is no
  default-open branch in the session parse (`criome_gate.rs:308-366`) or the
  criome re-judge.
- **The everywhere-gate invariant.** Everything in an *Enabled* spirit's log is,
  by construction, cluster-authorized; the staging slot is machinery invisible to
  every read surface and never survives a refusal, so "nothing is recorded
  anywhere" holds for the observable state.
- **The independent per-peer witness-clock gate.** Both the Request and Commit
  rounds are time-window-gated, and each member re-checks the window on its own
  clock (`root.rs:2143,2419-2442`) — clock skew affects liveness, not the
  cryptographic soundness of a committed round.
- **Two known boundary weaknesses**, both from the security audits (§7): the
  signed vote binds `{signer, operation, moment}` but *no predecessor head*
  (`language.rs:209-219`), and the older (pre-gate) audit's plaintext
  `ForwardMessage` ingress is authenticated-but-cleartext until the encrypted
  session is enforced both directions.

## 5 · The full test ledger (the centerpiece)

Reading the ledger: a **flake check** is pure and swept by `nix flake check`; a
**named output** (Nix package) stands up real daemons and is built explicitly
with `nix build .#<name>`; a **feature-gated cargo test** runs only under an
explicit `cargo test --features <…>` and (important) is *not* swept by the
default `nix flake check`. Status is green / blocked / un-run with the blocker
named.

### 5.1 · The gate unit witnesses (the acceptance semantic, in-process)

These are the pure, deterministic proofs of the LANDED everywhere-gate. They
build against each repo's own pinned dependencies and are green there; the
spirit-side ones are feature-gated (see the swept-vs-unswept note in 5.4).

**sema-engine — the staging seam: `test-staging` flake check + `tests/staging.rs`
(exactly 12 tests).** What it proves, test by test: `stage_then_discard_leaves_no_observable_trace`,
`staged_group_materializes_byte_for_byte_with_direct_writes`,
`prospective_head_equals_materialized_head`,
`occupied_slot_survives_reopen_and_recovery_materialize_matches_the_twin`,
`occupied_slot_resolves_by_discard_after_reopen`,
`begin_is_refused_while_a_parked_group_stands_or_a_session_is_engaged`,
`materialize_after_an_interleaved_commit_is_refused_fail_closed`,
`empty_park_stages_nothing_and_disengages`,
`abandon_drops_the_buffer_without_a_durable_trace`,
`materialize_and_discard_on_an_empty_slot_are_typed_refusals`,
`engaged_reads_overlay_and_disengaged_reads_return_to_committed_state`,
`subscription_deltas_deliver_at_materialize_not_at_buffer_time`
(`sema-engine/tests/staging.rs:264-746`). Pure flake check; **green**.

**criome — the bridge: `tests/cluster_authorization_bridge.rs` (5 tests).** The
head-authorization bridge end to end (single/founded node, in-process):
`founded_single_node_bridge_grants_with_quorum_evidence` (`:215`),
`window_expiry_pushes_expired_fail_closed` (`:277`),
`re_ask_of_a_standing_committed_head_re_grants_and_the_successor_still_grants`
(`:420`), `every_pending_slot_for_one_digest_settles_at_window_close` (`:523`),
`a_window_dead_round_is_superseded_by_a_differing_successor` (`:638`). Run under
criome's `test` flake check; **green**. Note the last test proves *single-node*
supersession — not the peer-committed fork (§5.5).

**criome — the admission matrix unit tests: `src/actors/root.rs` `#[cfg(test)]`
(7 tests).** Purely the `SuccessorLedgerPoint × RecordedRoundLife` matrix:
`fresh_point_admits_a_successor` (`:3637`),
`identical_re_proposal_is_idempotent_whatever_the_round_life` (`:3650`),
`a_conflicting_successor_against_a_live_row_is_vetoed` (`:3672`),
`a_conflicting_successor_against_a_committed_row_is_vetoed_forever` (`:3688`),
`a_conflicting_successor_supersedes_a_window_dead_row` (`:3706`),
`co_signing_the_head_as_its_own_successor_is_refused` (`:3728`),
`a_poisoned_self_loop_row_is_void_for_every_judgment` (`:3747`). **Green** — but
the matrix has *no peer input*, so none of these can witness Finding-1 (§5.5).

**spirit — `tests/staged_intake.rs` (6 tests, `--features criome-gate`).** The
three-phase intake against an in-test `StubCriome`:
`head_advancing_inputs_stage_and_reads_stay_immediate` (`:101`),
`reads_flow_ungated_while_the_gate_is_enabled_and_criome_is_absent` (`:139`),
`a_refused_advance_is_refused_to_the_caller_and_leaves_no_trace` (`:175`),
`a_granted_advance_materializes_exactly_the_staged_group` (`:320`),
`each_terminal_refusal_reason_surfaces_to_the_caller` (`:398`),
`crash_recovery_materializes_a_parked_group_on_the_recovery_grant` (`:443`).
Feature-gated cargo test; **green under the feature, not swept by nix** (5.4).

**spirit — `tests/cluster_gate_session.rs` (12 tests, `--features criome-gate`).**
The security-sensitive session-parse matrix and crafted-daemon falsifications:
`granted_with_binding_grant_authorizes`, `granted_without_grant_is_held_as_a_fault`,
`grant_digest_mismatch_is_held_as_a_fault`, `grant_slot_mismatch_is_held_as_a_fault`,
`request_digest_mismatch_is_held_as_a_fault`, `foreign_slot_records_are_ignored`,
`terminal_refusals_map_to_typed_refusal_decisions`, `non_terminal_states_keep_draining`,
`bare_granted_reply_is_held_as_off_contract`, `session_deadline_expiry_is_held_unreachable`,
`absent_criome_is_held_unreachable`,
`hung_but_accepting_criome_is_held_unreachable_within_the_deadline`. This is the
proof that "status alone is never proof." **Green under the feature, unswept.**

**spirit — `tests/criome_authorization_option.rs` (2, `--features mirror-shipper`).**
`disabled_default_advances_heads_freely_and_keeps_the_ship_seam_dormant` (`:143`),
`enabled_authorization_refuses_head_advances_when_criome_is_unreachable` (`:199`).
Feature-gated; **blocked today** because `mirror-shipper` cannot build (mirror
schema migration, 5.5/§7).

**signal-spirit — the refusal contract.**
`generated_advance_refused_frame_round_trips_without_moving_existing_routes`
(`signal-spirit/tests/generated_contract.rs`) locks the `AdvanceRefused` wire
addition. `daemon_configuration.rs` (4) exercises the `AuthorizationMode`
gating/observing config. Pure flake checks (`build, test, test-nota-text`);
**green**.

### 5.2 · The loopchecks / stateful named outputs (multi-daemon, over sockets)

**THE cluster-authorization loopcheck —
`spirit-cluster-gates-acceptance-over-router-test`** (Nix package,
`spirit/flake.nix:729-736,830-831`; the single test fn lives in
`spirit/tests/cluster_authorization_over_router.rs:559-873`; the beads
primary-knde/primary-ok91 still use the older name
`spirit-cluster-authorizes-head-advance-over-router-test`, so treat the flake
output name as authoritative). Topology:
one real spirit `Engine` on node A gated against criome A, two real `CriomeDaemon`
hosts, two real routers over loopback TCP, and — the tension — **an in-process
mirror *service* as the ship target** (`use mirror::{Engine, Service,
ServiceLink}`, `:65`), *not* a second spirit engine. Six-step scenario and its
asserts: (1) found the 2-of-2 root over the routers; (2) disabled-era residue —
two records commit locally, nothing ships; (3) enable, stage a third — reply
HELD, on grant the head equals the prospective digest and all three entries ship
under ONE round, criome B's ledger shows exactly one committed round and none for
the residue; (4) refused advance — stop router B, stage a fourth → the caller
gets `AdvanceRefused(Expired)`, the head did NOT advance, no store/outbox trace,
reads served mid-round; (5) supersession retry — restore B, a fifth entry
supersedes the dead round and ships; (6) ship-mail path over a coalesced burst.
**Status: BLOCKED (un-runnable today).** It requires the `cluster-authorization-e2e`
feature → `mirror-shipper` → the `mirror` crate, whose `build.rs` panics on the
schema strict-positional migration; and its router leg needs router modernized to
signal-criome 0.11.0 (36 errors). Both blockers are tracked in bead primary-ok91.
This is *the* proof that the whole everywhere-gate works over a real router, and
it is exactly the one that cannot be built right now.

**The founding-over-router loopcheck —
`router-two-hosts-found-root-over-router-test`** (Nix package,
`router/flake.nix:132-138`; test `router/tests/founding_over_router.rs`, fn
`two_hosts_found_the_same_root_anchor_over_the_real_router`). Two in-process
criome hosts found ONE
unanimous root ENTIRELY over the router (Slice D, primary-79z1.23): two real
`RouterRuntime`s on loopback TCP with durable route stores, two real criome
daemons originating over their local routers, founding under the witness-clock
gate, owner-accepted with no auto-approval. Witnessed claim: both hosts reach
`RootFoundingState::Founded` on the SAME anchor. It is **independent of the
mirror stack** — the "mirror switch" it flips is router's own owner-only
origination toggle (`meta_signal_router::set_mirror_enabled`), not the mirror
crate — which is why it is the *green precedent* the (mirror-coupled) cluster
loopcheck was modeled on. **Status: green within the router repo's own pins; but
the router repo lags signal-criome 0.11.0, so it does not currently compose
against the criome-0.8.2 / signal-criome-0.11.0 stack** — the same router-leg
blocker as the cluster loopcheck (§7).

**The per-destination ordering witness — `router/tests/forward_ordering.rs`** (on
the 0.6.0 FIFO branch; security finding F4; mirroring M0 prerequisite). Two
proofs over real loopback TCP + encrypted sessions: many forwards to one
destination arrive in submission order (asserted, never sorted); a black-hole
destination does not block a different destination. Uses the offline identity
prover (no criome daemon). **Green on the branch; the branch is unmerged**
(primary-f5n7).

**The mirror-coupled router witnesses** — `router-criome-forward-lands-in-mirror`,
`router-criome-forward-lands-real-body-in-mirror`, `router-forward-witness-reads-entry-body`
(router flake checks; tests `criome_forward_lands_in_mirror.rs` +
`src/bin/router_forward_witness.rs`, which hand-builds a mirror append). These
depend on the deletion-slated mirror/signal-mirror crates and are superseded by
the designed sema-engine fold; **carried on the branch, deletion-slated**.

**The criome cluster witness binaries** — `packages.cluster-witness`
(`criome/flake.nix`), building `criome-cluster-witness-test`,
`criome-auto-approve-witness-test`, `criome-client-approval-witness-test`,
`criome-write-configuration` behind the `cluster-witness` feature. Build-only
within the criome repo; **driven by an external NixOS harness**
(CriomOS-test-cluster), so un-run from the repo's own checks.

**The live VM cluster witness** — `CriomOS-test-cluster/lib/mkCriomeAuthWitnessTest.nix`
(siblings: `mkVmTest.nix`, `mkDeployTest.nix`, `nestedReachability.nix`,
`nestedSpike.nix`, `standardTest.nix`). Stands up real NixOS guests (node A: a
guardian-compiled spirit daemon + a real criome + a persona-router; node B: a
real criome verifier + a persona-router + a real mirror-daemon) and drives a
`router-forward-witness` sender that hand-builds a `signal-mirror::Append`
(`router/src/bin/router_forward_witness.rs:131-145`) which node B's router relays
into the mirror's durable append; two negatives (UnknownSigner, InvalidSignature)
refuse fail-closed. Exposed as `criome-auth-witness`
(`CriomOS-test-cluster/flake.nix:348`), alongside the other cluster outputs
`lojix-deploy-smoke` (:313), `nested-vm-guest-reachability` (:340),
`nested-microvm-spike` (:332), and the per-node `vm-<node>` suite (:284).
**Status: rebuild pending** — the mirroring design's M3/M4 replaces the node-B
mirror-daemon with a second spirit; the live two-VM proof is primary-nbmq.12 /
primary-79z1.15, both still open. Note the deployed unit was mirror-0.1.2 (the
redb crash-loop), a *distinct* failure mode from the repo-head 0.2.0 `build.rs`
schema panic.

### 5.3 · The rest of the surface, per repo (pure flake checks unless noted)

- **criome (14 checks + tests):** checks `build, test, test-nota-text,
  daemon-skeleton, criome-uses-kameo-not-ractor, criome-signal-criome-contract-boundary,
  criome-meta-session-architecture, criome-authorization-slots-are-store-minted,
  criome-authorization-expiry-and-replay-guard, fmt, clippy, clippy-nota-text,
  doc, default`. Integration tests beyond the bridge: `two_round_commit.rs` (6 —
  round-two authorization, short/forged-round refusal, conflicting-successor
  QuorumConflict, out-of-window refusal, two-successors-converge),
  `witness_clock_gate.rs` (4 — signer/peer clock in/out of window),
  `quorum_collection.rs` (8 — real BLS quorum withhold-until-majority,
  peer-unreachable-waits, forged-member-vote-refused, router-submission framing),
  `quorum_ledger_restart.rs` (1 — veto row survives restart), `root_founding.rs`
  (4), `founding_conveyance.rs` (2), `language.rs` (~26 — rule/threshold/time
  attestation), `intercept_policy.rs`, `daemon_skeleton.rs` (~40 — the broad
  daemon suite incl. `quorum_mode_on_an_unfounded_node_refuses_unavailable`),
  `distinct_node_identities.rs`, `sign_as_criome_host_id.rs`,
  `actor_discipline_truth.rs`; in-src unit modules in `daemon.rs`, `admission.rs`,
  `founding.rs`, `master_key.rs`, `root.rs`. **All green; no `#[ignore]` anywhere
  in the three criome repos.**
- **signal-criome (11 checks):** `build, test, test-round-trip, test-nota-text,
  test-doc, doc, fmt, clippy, clippy-nota-text, rkyv-feature-discipline,
  contract-crate-carries-no-runtime`. Tests: `round_trip.rs` (~35),
  `canonical_examples.rs` (3). **Green.**
- **meta-signal-criome (10 checks):** the standard contract-crate set. Tests:
  `round_trip.rs`, `canonical_examples.rs`. **Green.**
- **sema-engine:** checks `build, test, test-dependency-boundary, test-engine,
  test-operation-log, test-staging, test-subscriptions, doc, fmt, clippy` (also
  exposed as `apps`/`packages` for direct runs). Tests: `checkpoint, concurrency,
  dependency_boundary, engine, family_identity, fold, import, layout_rebuild,
  operation_log, outbox, seam_gap_falsification, signal_frame_seam, staging,
  storage_boundary, subscriptions, tamper`. **Green.**
- **signal-sema:** checks `build, test, test-nota-text, doc, fmt, clippy,
  clippy-nota-text`. Tests: `dependency_boundary, identity, magnitude, operation,
  outcome, pattern`. **Green.**
- **spirit (pure checks):** `build, build-nota-text, test, test-nota-text,
  spirit-observe-head-object-rehashes-to-head, test-configuration-writer-process-boundary,
  test-testing-trace, test-testing-trace-process-boundary, no-old-signal-macro,
  generated-schema-source-checked-in, nota-surface-is-opt-in, binary-boundary-test,
  retired-triad-surfaces-absent, no-production-free-functions,
  no-production-unit-structs, operator-271-closed-claims, fmt, clippy,
  clippy-nota-text, clippy-testing-trace, doc`. Broader tests (behavior from
  names): `runtime_triad.rs` (67 — full Signal/Nexus/SEMA triad + guardian),
  `process_boundary.rs` (17 — real CLI↔daemon over socket),
  `generated_signal_plane.rs` (26), `versioned_store.rs` (4), `observe_head.rs` /
  `observe_head_object.rs`, `collect_removal_candidates.rs` (4),
  `meta_configure.rs` (5), `guardian_*`, `import_auto_register_referents.rs`,
  `operator_271_closed_claims.rs` (7), plus the gate/mirror/e2e files above.
  `nix_integration.rs` (9) and `guardian_live_scenarios.rs` (3) are `#[ignore]`
  (nix-built binaries / live LLM endpoints). **Core green.**
- **signal-spirit (6 checks) / meta-signal-spirit (7 checks):** the standard
  contract-crate sets; `generated_contract, validation, instance_schema,
  help_instance_schema_convergence, true_schema_nota_projection,
  daemon_configuration, dependency_boundary` (signal-spirit) and `round_trip,
  frame, dependency_boundary, true_schema_nota_projection` (meta-signal-spirit).
  **Green.**
- **router (18 checks + named outputs):** checks include
  `router-accepts-only-real-criome-attestation, router-refuses-forward-without-criome-credential,
  router-generated-daemon-answers-working-and-meta-sockets,
  router-runtime-cannot-{depend-on-message,depend-on-terminal-crates,poll,reference-retired-terminal-brand},
  router-daemon-*, router-ingress-cannot-stamp-hidden-owner-origin,
  router-unknown-channel-parks-for-adjudication`, plus the mirror-coupled forward
  checks (5.2). Tests: `actor_runtime_truth, authorized_object_fanout,
  configuration_text_edges, criome_forward_attestation, criome_forward_lands_in_mirror,
  encrypted_peer_session, end_to_end_remote_forward, forward_ordering,
  founding_over_router, mirror_toggle, no_shared_locks_truth, observation_truth,
  outbound_backlog_durable, outdated_store_wipe, process_boundary,
  remote_route_durable, schema_generated, smoke`. **Green on the 0.6.0 branch's
  own pins; the whole repo lags signal-criome 0.11.0 for cross-repo composition
  (§7).**
- **signal-router (7 checks) / meta-signal-router (6 checks) / signal-standard
  (11 checks):** standard contract-crate sets; `round_trip` / `canonical_examples`.
  **Green** (meta-signal-router 0.4.0 and signal-standard 0.2.0 just landed).
- **mirror stack:** mirror tests `append_addressing_refusal, daemon_logic,
  end_to_end_arc, landed_body_readback`; signal-mirror / meta-signal-mirror
  `round_trip`. **Blocked / deletion-slated** — mirror 0.2.0's `build.rs` panics
  on the schema migration; the deployed service is disabled.

### 5.4 · How the gate witnesses are (and are not) invoked — a real gap

An important subtlety a reader must not miss: **`nix flake check` on spirit
enables neither `criome-gate` nor `mirror-shipper`** (its `checks.test` uses
`--no-default-features`). So `staged_intake` (6), `cluster_gate_session` (12),
`criome_authorization_option` (2), and `mirror_shipper` (2) are *not* run by the
default nix sweep — they run only under an explicit `cargo test --features
criome-gate` (or `mirror-shipper`). The loopcheck is a named output, likewise
unswept. Consequence: the LANDED gate's unit witnesses are green when run, but
the *automated* gate (`nix flake check`) does not exercise them; the acceptance
semantic's continuous coverage is opt-in.

### 5.5 · Coverage gaps (named, not filled)

- **Finding-1 (voter-supersedes-peer-committed) has NO witness — and cannot be
  produced by any current or planned test.** The 7 in-source admission unit
  tests (5.1) judge the local `SuccessorLedgerPoint × RecordedRoundLife` matrix,
  which has no peer input; `a_conflicting_successor_against_a_committed_row_is_vetoed_forever`
  covers only a *locally*-committed row. The bridge test
  `a_window_dead_round_is_superseded_by_a_differing_successor` is single-node. The
  loopcheck's supersession step (step 5) is single-writer. Nothing drives two
  real criomes to originate different successors from the same head concurrently
  and witnesses the resulting fork. See §7.
- **The everywhere-gate over a real router is un-run today** — the cluster
  loopcheck (5.2) cannot build.
- **Propagation with receiving-side acceptance (§4 of the slice design) is
  unwitnessed** — the apply ingress is still the single-record parked/fail-closed
  path (`nexus.rs:1282-1284`); `ApplyAuthorizedRecords` and the peer re-judge are
  DESIGNED-ONLY.
- **The mirroring-into-sema-engine fold is unwitnessed** — the `mirroring` module
  and its ported decision-matrix tests do not exist yet.

## 6 · Current-state table

| Repo | Version | Head | Key status | Green / blocked |
|---|---|---|---|---|
| criome | 0.8.2 | a82b514 | gate + dead-round supersession LANDED; renames DESIGNED-ONLY | green (self-tests) |
| signal-criome | 0.11.0 | 5998cf2 | schema-rust 0.7.0 migration; typed refusal vocab; the API consumers must catch up to | green |
| meta-signal-criome | 0.6.0 | fdc71cc | owner config contract | green |
| spirit | 0.24.0 | 33f16e7 | everywhere-gate LANDED (three-phase intake, AdvanceRefused, ship-only drain) | core green; gate witnesses unswept; e2e blocked |
| signal-spirit | 0.13.0 | 1cf7c01 | `AdvanceRefused` LANDED; batch apply DESIGNED-ONLY | green |
| meta-signal-spirit | 0.7.1 | 0a7a243 | owner config contract | green |
| sema-engine | 0.7.0 | b3b5fb7 | staging seam LANDED; mirroring fold DESIGNED-ONLY | green |
| signal-sema | 0.2.0 | 8cc1929 | shared sema contract; mirror wire vocab DESIGNED-ONLY | green |
| router | 0.6.0 (branch `router-per-destination-fifo`) | ab1c726 | FIFO lanes LANDED on branch; main is 0.5.0; lags signal-criome 0.11.0 | green on branch pins; blocks cross-repo loopcheck |
| signal-router | 0.5.0 | 501308d | wire contract | green |
| meta-signal-router | 0.4.0 | 1475d4b | just landed (schema migration) | green |
| signal-standard | 0.2.0 | feb6cd0 | shared vocabulary; typed digest/host-id DESIGNED-ONLY | green |
| mirror | 0.2.0 | b8cf8ec | DELETION-slated; build fails schema migration | blocked |
| signal-mirror | 0.1.1 | d2d3c61 | DELETION-slated | (n/a) |
| meta-signal-mirror | 0.2.0 | ad0259d | DELETION-slated; 5-field migration pending | blocked |

## 7 · Known issues, risks, and the bead landscape

### The single most important risk — Finding-1: dead-round supersession can fork the cluster

The recent security audit found the everywhere-gate **sound as scoped** with one
HIGH latent finding. In `criome/src/actors/root.rs`, a window-dead,
never-committed round row can be superseded by a *different* successor
(`CoSignAdmission::SupersedeDeadRow`, `root.rs:155,236`), and the classification
of a row as `Dead` is judged **purely on the local node** — `recorded_round_life`
(`root.rs:2621-2653`) reads only `self.stored_quorum_round(...)` and tests the
window against `self.clock` (`:2649`); it never checks whether the superseded
round committed on a *peer*. Compounding it, the signed vote binds no predecessor
head (`OperationStatement::to_signing_bytes`, `language.rs:209-219`), so nothing
cryptographically pins which head a vote descends from. Under concurrent /
bidirectional origination from the same head — a deferred regime — two members can
therefore admit different successors of the same head and **fork the cluster**.
Safety today rests on an *argument*, not a peer-verified guarantee: only a round's
originator can drive its commit, and it proposes a different successor only after
its own window expired and it abandoned the round (`root.rs:158-173`). That
argument holds under the **current single-writer scope**, so the finding is
latent, not live. It becomes reachable the moment two writers can originate
against the same head. **No test exercises it** (§5.5), and the one loopcheck that
could be extended to (the cluster-authorization loopcheck) cannot even build
today. This is the risk to carry forward.

### The mirror-stack-deletion tension with the loopcheck

The accepted mirroring design deletes the mirror stack and folds its receive half
into sema-engine. But the *proof that the everywhere-gate works over a real
router* — the `spirit-cluster-gates-acceptance-over-router-test` loopcheck — still
ships to an **in-process mirror service** and pulls the `mirror` crate through the
`mirror-shipper` feature. The mirror crate is simultaneously (a) deletion-slated
and (b) failing its own schema-migration build. So the loopcheck cannot go green
by fixing the mirror crate (that work is throwaway) *and* cannot go green without
it until the sema-engine fold (M2) replaces the mirror service with a second
spirit engine. The clean resolution is the fold, not a mirror repair — but until
the fold lands, the fabric's headline integration proof is un-runnable. This is
the sharpest sequencing pressure in the whole plan.

### The router leg

Independently, router source lags signal-criome 0.11.0 (36 errors from the
`SignatureEnvelope` / `ContentReference` / `AuditContext` / `Attestation` /
`VerifyRequest` / `VerificationResult` / `AuthorizedObjectReference`
restructuring, plus the meta-signal-router 0.4.0 / signal-standard 0.2.0 renames).
Both the founding-over-router and cluster-authorization loopchecks need the router
modernized against the current criome stack. The per-destination FIFO work (the
mirroring M0 prerequisite) sits on the unmerged branch `router-per-destination-fifo`
(0.6.0), stacked on an unmerged TrueSchema producer.

### Bead landscape (read-only; not mutated)

- **primary-knde** (P2, open) — spirit verification debt. Mostly resolved: the
  stale flake signal-router substitution and the nota-text process_boundary break
  are gone on main; runtime_triad passes 64/64 under `agent-guardian` alone. The 7
  "guardian failures" are **mirror-shipper build artifacts**, not guardian-logic
  bugs — re-characterizable only after mirror migrates (routed to primary-ok91).
- **primary-ok91** (P2, open) — the loopcheck router-leg green-up. Two blocker
  classes: CHURN (regeneratable — mirror 0.2.0 + meta-signal-mirror schema
  strict-positional migration) and REAL (not regeneratable — router modernization
  to signal-criome 0.11.0; do not paper over). This is the bead that gates the
  cluster loopcheck.
- **primary-9uq2** (P3, open) — criome solicit-seam: a solicitation redelivered
  inside a live window re-opens the peer's stored round copy, eroding gathered
  votes; sound fix is reconvey-without-reopen gated on proposition-equality. Audit
  F6 remainder.
- **primary-f5n7** (P2, open) — land `router-per-destination-fifo`; full merge to
  main with/after the TrueSchema producer; the mirroring M0 prerequisite.
- **primary-nbmq** (P1 epic) — the persistent both-directions quorum-gated spirit
  mirror; 11/13 children complete; the separate mirror daemon is dropped in favor
  of the router-mediated path; the live two-VM proof (nbmq.12) is open.
- **primary-79z1** (P1 epic) — operational criome: founding, witness-clock gate,
  two-round commit; 18/31 children complete; the live founding proof on the two
  VMs (79z1.15) and the fabric-identity slices remain open.
- **Older pre-gate audit (primary-nbmq.11)** — the crypto core is sound and
  fail-closed (real BLS majority, no 1-of-1 shortcut, MITM-resistant handshake,
  forward secrecy). Its must-fixes are deploy posture: close the plaintext
  `ForwardMessage` ingress once both daemons speak the encrypted session (M1),
  wire real criome-backed provers (M2), pin `Quorum` mode and the admitted
  contract (M3). Its N2 nice-to-have (the vote preimage does not bind the
  contract/predecessor) is the same seam Finding-1 exploits.

## 8 · Recommended build sequence for the remaining accepted design (NOTES, not decisions)

Sequenced as notes with dependencies; landing order respects
producers-before-consumers and keeps each main green.

1. **G0 — rule and mode cleanup (independent, land first).** Remove
   `EscalateToPsyche` from `Rule` (11→10); rename
   `AuthorizationMode::ClientApproval` → `ExplicitApproval`. Small, wire-visible,
   no dependency. signal-criome + criome bumps. Depends on nothing.
2. **G1 — the `Contract`→`Criome` rename.** Across signal-criome, criome,
   meta-signal-criome, and consumers. Preferred *before* G2 so new types are born
   in the settled vocabulary. Dependency: the everywhere-gate lane's claims on
   criome/spirit/sema-engine must be released first (they are — the gate landed).
3. **Router modernization + M0 (unblocks the proofs).** Modernize router source
   against signal-criome 0.11.0 (the REAL, non-regeneratable work in primary-ok91)
   and land `router-per-destination-fifo` to main (primary-f5n7). This is the
   prerequisite for *any* cross-repo loopcheck and for the mirroring offline-delta.
   Independent of G0/G1; can proceed in parallel.
4. **M1/M2 — mirroring into sema-engine, and the loopcheck rebuild.** signal-sema
   gains the entry-envelope / suffix / head-mark / restore-bundle / refusal wire
   vocabulary (M1); sema-engine grows the `mirroring` module (ported decision
   matrix + crash-window healing + restore + evidence retention) and spirit wires
   the drain + un-refuses the apply ingress in batch form (M2). Then rebuild the
   cluster loopcheck to ship to a **second spirit engine** instead of the in-process
   mirror service — this is what makes it green and simultaneously retires the
   mirror dependency. Depends on step 3 (router leg). This resolves the §7 tension.
5. **G2 — the governed-slot substrate.** The closed `GovernedSlot` vocabulary;
   head/anti-equivocation/round rows keyed by `(account, slot)`; criome-held slot
   values stored current-only; newest-evidence retention and the pruning rules
   (reachability GC of dead accounts); multi-slot rounds. The heart of the
   governance design. Depends on G1.
6. **G3 — admission closure.** Delete the unauthenticated `AdmitContract` verb;
   replace with evidence-carried admission (verify the `Children`-round evidence
   against the admitted parent before storing); founding untouched. Depends on G2
   (evidence rows). Closes the real §1/§4 admission hole.
7. **G4 — issuance as a state change.** The `Children` slot live: the root issues
   the operational account as a `Children` change; supersession with slot
   adoption; safe policy defaults (account-layer changes park for explicit
   approval). Subsumes the slice design's §5. Depends on G2.
8. **G5 — the mirror-list log.** Spirit gains the mirror-list log and a typed,
   explicit-approval-defaulted working operation amending it; the shipper unions
   grant-carried members with the mapped remotes from its own log; the old
   `SelectedMirrorTarget` and its meta types die. Depends on G2; composes with M2.
9. **Finding-1 fix.** Close the fork window before enabling any concurrent /
   bidirectional origination regime: bind a predecessor head (and, per the older
   audit's N2, the governing account) into the vote preimage
   (`language.rs:209-219`), and/or make dead-round supersession verify the
   superseded round did not commit on a peer rather than trusting the local clock.
   Add the witness that no current test can produce: two real criomes originating
   different successors from one head, asserting no fork. Not required for the
   single-writer scope, but a hard prerequisite for multi-writer or M-of-N.
10. **Deferred (named): G6 privacy silos** (waits on named silos —
    one `Primary` silo for now), **M3 mirror-stack deletion + VM rebuild** (after
    the loopchecks are green spirit-to-spirit), **M4 non-authoritative remotes**
    (after G4), **the live two-VM proofs** (primary-nbmq.12, primary-79z1.15), and
    **G7 the policy slot**.

The critical path to a green fabric proof is steps 3→4 (router modernization →
mirroring fold + loopcheck rebuild); the governance renames (G0/G1) can land in
parallel; the Finding-1 fix gates any move away from single-writer.
