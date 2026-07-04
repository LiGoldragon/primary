# Criome Ceremony — Current-State Scout Map

Read-only ground-truth map for a high-stakes architecture decision: the psyche
wants a truly operational **Criome** (C-R-I-O-M-E) to become the authentication
layer for all components so deployment can stop relying on SSH (SSH kept only as
a fallback). This map tells the designer which of the psyche's named concepts
already exist in code, which are partial, and which are net-new.

Sources: current `main` heads read directly (criome `4bf6f9b`, signal-criome
`8080347`, meta-signal-criome, router `0af3624`). Claims tagged `[observed]`
(read in code/output) vs `[interpretation]`. Anchors use `repo/path:line`;
`criome` = `/git/github.com/LiGoldragon/criome`, `signal-criome` =
`/git/github.com/LiGoldragon/signal-criome`. The two prior maps in this folder
(`CriomeQuorumReadiness-Scout.md`, `MirrorArchitecture-Design.md`) predate the
`.4`/`.6` builds; this map reads the post-build source, so it supersedes their
"quorum collection is MISSING" verdict — the gather driver now exists.

## TL;DR concept verdicts

| # | Psyche concept | Verdict | One-line evidence |
|---|---|---|---|
| 1 | Criome unit = cryptographic contract, complex (subquorums, time windows) | **Exists (substance) / net-new (naming)** | `Contract(Rule)` is a first-class content-addressed persistent object; nested contracts + time rules real; not *called* "Criome unit" |
| 2 | Root signing ceremony → root authority + subcontracts; one subcontract per cluster | **Net-new (partial anchor)** | No ceremony, no subcontract, no root→child relation; the single-key `ClusterRoot` admission anchor is the only "root authority" building block |
| 3 | Root contract = Criome with no parent; `parent` field carries a "root" variant | **Net-new** | `Contract` has NO `parent` field at all; contracts are a flat content-addressed DAG, not a parent/child tree |
| 4 | Time-window / witness-clock; sign only inside window; collective signing = Criome clock; on-demand | **Partial (strongest)** | `TimeWindow`/`AttestedMoment`/`TimeSignature` + consensus-moment judging all exist and ARCHITECTURE describes the vision; the per-signer "sign only if my clock ∈ window" gate is NOT implemented |

## Current-state map

### The data model: is a "contract" a first-class persistent object?

`[observed]` **Yes.** The public policy nouns live in `signal-criome`
(`criome/src/language.rs:1-15` doc + imports). The core type:

- `Contract(Rule)` — `signal-criome/src/schema/lib.rs:725`. A contract is a
  single-field newtype wrapping a `Rule`. Content-addressed by `ContractDigest`
  (`ObjectDigest` newtype, `:78`). It carries **no** name, no version, no owner,
  and critically **no `parent` field**.
- `Rule` enum — `signal-criome/src/schema/lib.rs:733`:
  `SignedBy(Identity)`, `All(Vec<ContractDigest>)`, `Any(Vec<ContractDigest>)`,
  `Threshold(Threshold)`, `Workflow(WorkflowGuard)`, `Composition(Composition)`,
  `ActiveAfter(TimedRule)`, `ActiveUntil(TimedRule)`, `TimeSwitch(TimeSwitch)`,
  `Agreement(AgreementRule)`, `EscalateToPsyche`.
- `Threshold { required_signatures, members: Vec<PolicyMember> }` — `:790`.
- `PolicyMember { KeyMember(Identity) | ObjectMember(ContractDigest) }` — `:779`.
  `ObjectMember` is the mechanism by which a threshold member is *itself another
  contract*.
- Persistence: contracts are a durable sema-engine table `contracts`
  (`StoredContract`) — `criome/src/tables.rs:36,605`. Admitted via wire op
  `AdmitContract(Contract)` (`signal-criome/src/schema/lib.rs:2028`). ARCHITECTURE
  §9 asserts the contract DAG survives restart.

**Parent / hierarchy / subcontract:** `[observed]` ABSENT. A crate-wide search
for `parent|subcontract|child.?contract|hierarch|root.?contract|is_root` in
`criome/src/` returns only filesystem `path.parent()` calls
(`daemon.rs:163`, `master_key.rs:88`). There is no parent field, no root variant,
no subcontract type, no rotation/derivation relation between contracts.

**Subquorum:** `[observed]` PARTIAL, split between judge and gather driver.
- The **judge** fully supports nested-contract subquorums: `PolicyMember::is_satisfied`
  (`criome/src/language.rs:504-...`) resolves `ObjectMember(digest)` by
  `store.evaluate(digest, ...).is_authorized()` — a recursive contract
  evaluation. `Rule::All`/`Any` (`language.rs:290-295`) evaluate a `Vec<ContractDigest>`.
  `Composition` (`:764`) adds another nesting layer. So a Threshold whose member
  is another Threshold contract *is* a working subquorum, evaluated recursively.
- The **gather driver** does NOT: `quorum_members` (`criome/src/actors/root.rs:1455-1472`)
  filters `PolicyMember::ObjectMember` OUT and solicits/collects only flat
  `KeyMember` votes ("quorum collection governs only Threshold contracts"). So a
  subquorum can be *judged* from pre-assembled evidence but cannot yet be *gathered*
  live across nodes.

### The request → sign → judge → commit flow, and time/freshness

`[observed]` The wire request surface is `signal_criome::Input`
(`signal-criome/src/schema/lib.rs:2012-2042`). The quorum-collection ops (the
live consensus path, added in `.4`):

- `ProposeQuorumAuthorization(QuorumProposal)` — `:2038`.
  `QuorumProposal { round, contract: ContractDigest, object: AuthorizedObjectReference, window: TimeWindow }`
  (`:1937`). **The request carries a caller-supplied `window`** — matches concept 4's
  "incoming request carries a time-window parameter."
- `SolicitQuorumVote(QuorumVoteSolicitation)` — `:2039`. Carries the moment
  `proposition` + `originator`.
- `SubmitQuorumVote(QuorumVote)` — `:2040`. `QuorumVote { round, voter, operation_signature, time_signature }`
  (`:1964`) — each vote is TWO BLS signatures: one over the operation, one over
  the moment.
- `ObserveQuorumRound(QuorumRoundQuery)` — `:2041`.
- Judge op (pre-existing): `EvaluateAuthorization(AuthorizationEvaluation)` — `:2030`.
- Contract op: `AdmitContract` `:2028`, `LookupContract` `:2029`.
- Time-check ops: `ScheduleContractTimeCheck(ContractTimeCheck)` `:2033`,
  `RunDueContractChecks(AttestedMoment)` `:2034` — a scheduled evaluation of
  time-gated contracts when a moment is proven.

**The flow** (`criome/src/actors/root.rs:1204-1450`):
1. `propose_quorum_authorization` (`:1218`): round-id is bound to the operation
   digest (`:1230`, audit S1 fix); build `AttestedMomentProposition::new(window, required, members)`
   from the contract's members; cast the self-vote; open a durable
   `StoredQuorumRound`; persist; `solicit_peers`.
2. `solicit_quorum_vote` (`:1256`): peer re-validates (contract admitted here,
   this node is a member `:1276`, proposition names the full member set
   `:1283`), casts its vote, conveys it back over the voice.
3. `submit_quorum_vote` (`:1300`): record vote, drop non-member votes at ingress
   (`:1315`), re-judge.
4. `assemble_evidence` (`:1382`) builds one shared `AttestedMoment` from every
   vote's `time_signature` and an `Evidence` from every `operation_signature`,
   then the reused `ContractStore::evaluate` decides. A round is WITHHELD
   (`Gathering`) until the judge returns `Authorized`; an unreachable peer leaves
   it pending forever (genuine "quorum or nothing / waits").

**Freshness / nonce / timestamp already present:** `[observed]`
- Time is modeled by `AttestedMoment { proposition, time_signatures: Vec<TimeSignature> }`
  (`signal-criome/.../lib.rs:1038`), `AttestedMomentProposition { window: TimeWindow, required_signatures, authorities: Vec<Identity> }`
  (`:1015`), `TimeWindow { opens_at, closes_at }` (`:849`), `TimeSignature { signer, envelope }`
  (`:1027`). This is real freshness infrastructure, not a stub.
- Forward-attestation freshness (a nonce + clock-skew admission window) exists in
  the **router**, not criome (`router/src/forward_attestation.rs`, per
  `SecurityAudit-QuorumAndChannel.md:69`). `VerifyAttestation` in criome itself
  does NOT check nonce freshness (design note carried in the mirror design doc).

### Time-window / witness-clock — where it is real and where it is missing

`[observed]` **The consensus-moment (Criome clock) is real at the judge:**
`AttestedMoment::rejection_reason` (`criome/src/language.rs:615-654`) requires a
well-formed window (`opens_at < closes_at`), a strict majority of registered time
authorities, no duplicate authorities, and a strict-majority of *real BLS
signatures* over the `AttestedMomentStatement`. Time-gated rules compare against
the attested moment's `closes_at`, not any single node's wall clock: `ActiveAfter`/
`ActiveUntil` (`language.rs:297-314`) test `evidence.stamp.closes_at()` against the
rule boundary. This directly realizes concept 4's "quorum's collective signing
forms a consensus cryptographic Criome clock," and ARCHITECTURE §8 "Crystallized-time
and AttestedMoment" (`criome/ARCHITECTURE.md:750-766`) describes exactly the psyche's
vision: *"a quorum signs that the present falls within it, and the window closes at
the last signature or at expiry, crystallizing a non-forgeable monotonic lower bound
on now."*

`[observed]` **The per-signer witness-clock gate is NOT implemented.** The heart
of concept 4 — "any Criome daemon may sign the request ONLY inside that window, so
each signature testifies 'this time is now'" — requires a signer to consult its own
clock and refuse to time-sign outside `[opens_at, closes_at]`. It does not:
`AttestationSigner::sign_quorum_vote` (`criome/src/actors/signer.rs:344-368`) signs
the moment-proposition bytes **unconditionally**; it never reads `SystemClock`
(`master_key.rs:218-234`) and never compares its clock to the window. The peer's
guard `proposition_matches_members` (`root.rs:1477-1487`) checks the member set and
threshold but NOT the window. So today a daemon time-signs any window it is asked
to, regardless of whether "now" is really inside it. The `SystemClock` is used only
on the OLD signal-call grant path (`signer.rs:238,295,370-382`), where `grant_stamp`
builds a degenerate 1-nanosecond self-window at the signer's own clock — not a
caller-supplied window with a per-signer freshness check.

`[interpretation]` Net of this: the time-window as a *data structure carried on the
request*, the *collective consensus moment*, and the *clock-as-consensus for
time-locks* all exist; the missing piece is the enforcement that makes each
signature a genuine "now" witness — the signer checking its own clock against the
window before adding its `TimeSignature`. This is the single most load-bearing gap
for concept 4. On-demand (no heartbeat) is already true: rounds are opened per
operation, there is no periodic time beacon.

### How the signer set / authority is established today

`[observed]` Hand-seeded, founded at first boot, single-key trust anchor —
confirmed precisely:

- **Founded at first boot:** `MasterKey::load_or_generate`
  (`criome/src/master_key.rs:56-63`) generates a BLS12-381 secret on first run and
  persists it atomically at 0600 (`persist` `:87-...`, `from_secret_file` rejects
  symlinks/loose perms `:65-85`). Per Spirit `psc6` (custody). Default node
  identity is `Host("criome")` (`root.rs:113`), overridable via config
  (`daemon.rs:60-70`, `CriomeDaemonConfiguration.node_identity`).
- **Single-key trust anchor (the "root authority" building block):** `ClusterRoot`
  (`criome/src/admission.rs:74-102`) holds ONE cluster-root BLS public key and
  admits an identity into the registry only if the registration carries a valid
  cluster-root signature over the canonical `RegistrationStatement`
  (tag `CRIOME-REGISTRATION-ADMISSION-V1`, `:46`). Wired into
  `IdentityRegistry::register` (per prior scout `registry.rs:106-131`); a
  virgin/dev daemon with no configured root skips the gate. Per Spirit `ermr`.
- **Hand-seeded at deploy:** authority is established by (1) `Configure` on the
  owner-only meta socket setting `cluster_root` + `authorization_mode` +
  `node_identity` (`meta-signal-criome/src/schema/lib.rs:236` `Input::Configure(CriomeDaemonConfiguration)`;
  the config struct `signal-criome/.../lib.rs:698-705`), (2) `RegisterIdentity`
  for each member key (cluster-root-signed), (3) `AdmitContract` for the flat
  Threshold quorum contract. In the mirror deploy this is the Nix `peerIdentitySeeds`
  (`RegisterIdentity` ExecStartPost) + `quorumContracts` 2-of-2 seeding
  (`MirrorArchitecture-Design.md:446-468`, `MirrorBuild-Weave.md:17`).
- **No ceremony / no rotation / no root contract:** there is no
  `EstablishRoot`, `FoundContract`, `RotateMembers`, or subcontract operation on
  either the working `Input` or the meta `Input` surface. `KeyPurpose::CriomeRoot`
  (`admission.rs:56`) is a key-purpose *tag*, not a root contract.

### The JUDGE (BLS majority, reboot-durable) — what persists, and where

`[observed]` The judge is `ContractStore::evaluate` / `Threshold::decide`
(`criome/src/language.rs:418-443`): counts distinct satisfied members, `Authorized`
iff `satisfied >= required`, else `Rejected(QuorumShort)`; `is_valid_majority`
enforces strict majority at admission (`:671-674`); `has_valid_signature_from`
does per-member real `blst` BLS12-381 min-pk verification bound to the member's
registered key + operation + moment. Fail-closed: missing store/registry ⇒ not
authorized.

**Reboot-durable state** lives in the component-local sema-engine store
(`criome/src/tables.rs`), tables registered in `CriomeTables::open` (`:618`):
- `identities` (`StoredIdentity`, `:600`) — the identity↔key registry the judge
  reads.
- `contracts` (`StoredContract`, `:605`) — the admitted content-addressed
  contracts (the quorum/threshold record).
- `quorum_rounds` (`StoredQuorumRound`, `:608`, family `criome-quorum-round`
  `:59`) — NEW in `.4`: in-flight round state (votes gathered so far), so a
  restart resumes a pending round.
- `authorization_states`, `authorization_replay_nonces`, `signature_solicitations`,
  `submitted_signatures`, `attestations`, `revocations`, `intercept_policies`,
  `parked_spirit_requests`, and slot counters (`:600-614`).
- On start `CriomeRoot` reconciles the master key against the registered node
  identity and fails loud (`Error::Startup`) on mismatch (prior scout; `root.rs:199-208`).

### Deployment authentication path (SSH today) and what the router already provides

`[observed]` **What the router handshake already provides for a Criome-based
auth:** the router's peer session performs a mutual node-identity proof anchored
in each node's Criome `Host(<node>)` BLS identity. `CriomeIdentityProver`
(`router/src/identity_proof.rs:63-88`) asks the local Criome to `Sign` a
`RouterIdentityProof` binding `{node identity, ephemeral X25519 public key}` to a
peer-issued challenge (`PeerIdentityProver::prove` `:42`), and verifies the peer's
proof against Criome, returning `UnknownSigner` if the peer identity→key binding is
absent (`:52-55`). This is the exact primitive a Criome-rooted deploy-auth would
build on: a node cryptographically proving it is `Host(<node>)` via its Criome
master key, no SSH key involved. The channel it establishes is an authenticated
encrypted session (X25519 ECDH → ChaCha20-Poly1305, forward-secret) per
`SecurityAudit-QuorumAndChannel.md:206-211`.

`[observed]` **How deploys are authenticated TODAY: SSH as root, via the
operator's gpg-agent key.** The `lojix` daemon (`lojix-daemon`) is the tool that
pushes and activates a system closure on a remote node — not `deploy-rs`, not
`nixos-rebuild --target-host` (those appear only in prose/reports). The chain is
eval → build → copy → activate, and the copy + activate legs go over SSH/ssh-ng:

- SSH target is always `root@<node>.<cluster>.criome` —
  `lojix/src/schema_runtime.rs:3820` (`root_at_node`, `user="root"`), `:3848`
  (`ssh_uri` → `ssh-ng://root@<domain>`), `:3852` (`as_ssh_arg`).
- Store push: `nix copy --substitute-on-destination --to ssh-ng://root@<domain>` —
  `lojix/src/schema_runtime.rs:3957-3965` (`ClosureCopy::invocation`).
- Activation: `ssh -o BatchMode=yes root@<domain> "nix-env -p …/system --set <store>
  && <store>/bin/switch-to-configuration <boot|switch|test>"` —
  `lojix/src/schema_runtime.rs:3856-3867` (`remote_invocation`), `4052-4118`
  (`HostActivation::ssh_invocation`); BootOnce wraps a rollback in `systemd-run`
  `:4098-4117`.
- **The auth material is ambient, not in code:** `NixCommand::run` is a bare
  `Command::new(program).args(...).output()` with no `-i`/IdentityFile, no
  `NIX_SSHOPTS`, no known-hosts option (`lojix/src/schema_runtime.rs:4670-4687`).
  The daemon runs as user `li` with `SSH_AUTH_SOCK =
  /run/user/<uid>/gnupg/S.gpg-agent.ssh` (`CriomOS/modules/nixos/lojix.nix:64,68`),
  so it authenticates with the operator's gpg-agent-backed SSH key. Target side:
  root's `authorizedKeys = adminSshPubKeys` (`CriomOS/modules/nixos/users.nix:47`),
  sshd keys-only (`normalize.nix:171-176`), host-key trust generated from every
  `exNode`'s `sshPubKeyLine` (`normalize.nix:36-43,108`).
- **SSH is the SOLE remote transport.** A search of `lojix/src` for
  `reqwest|hyper|http|bearer|token|tls` finds no remote HTTP/token/signed-activation
  path; the only cryptographic signing is Nix *closure* signatures (integrity, not
  deploy auth). The only non-SSH auth is *local* daemon admission: a Unix socket
  gated by `SO_PEERCRED` uid/gid (`lojix/src/daemon.rs:214-235`; owner `0600` +
  ordinary `0660`, `lojix.nix:35`).
- Deploy verbs (`HostDeployAction`): `SetBootProfile, ActivateNow, TestActivation,
  ScheduleBootOnce` (+ `Evaluate`, `Realize`) — `signal-lojix/src/schema/lib.rs:208-214`;
  the `lojix`/`meta-lojix` CLI submits one NOTA request to the local daemon socket,
  which then runs the ssh/nix-copy commands (`lojix/src/bin/lojix.rs:1-6`,
  `meta-lojix.rs:3-5`).
- `goldragon/datom.nota` (the `ClusterProposal`) defines each node's SSH **host
  public key** and each user's authorized SSH pubkeys (e.g. `mirror-alpha :190`,
  `mirror-beta :204`, `li :244`); schema in `horizon-rs/lib/src/proposal.rs:627,672`.
  The deploy **private** key is never in-repo — it lives in the operator's
  gpg-agent.

`[interpretation]` So the entire remote deploy trust boundary today is "the
operator holds an SSH key that root on every node authorizes." Replacing it with
Criome means the *node-to-node / operator-to-node* authorization moves from an SSH
keypair to a Criome-authorized object, while `nix copy` (store transfer) can remain
or ride the router's payload lane.

`[interpretation]` To *become* the deploy auth layer, Criome would need to expose
an operation that authorizes a deployment/activation as a first-class authorized
object (an `AuthorizedObjectKind` — today the kinds are `Operation | Contract |
Agreement | Time | Head`, `signal-criome/.../lib.rs:1163`; there is no `Deployment`
or `Activation` kind), gathered under a per-cluster contract and carried over the
router's already-authenticated session in place of the SSH transport. The judge,
the identity registry, the encrypted session, and the node-identity proof already
exist; the deploy-specific authorized-object type, the deploy-authorization request
op, and the activation-side gate (accept only a Criome-authorized closure) are the
net-new surface.

## Concept-by-concept gap table

### 1. "The Criome" / "Criome unit" = a cryptographic contract, possibly complex

- **Exists (substance):** `Contract(Rule)` is a first-class, content-addressed,
  reboot-durable object (`signal-criome/.../lib.rs:725`; table `criome/src/tables.rs:605`).
  Complexity is real: nested contracts via `ObjectMember`/`All`/`Any`/`Composition`,
  time rules via `ActiveAfter`/`ActiveUntil`/`TimeSwitch`, plus `Workflow`,
  `Agreement`, `EscalateToPsyche`.
- **Net-new (naming/framing):** nothing in code calls a contract a "Criome" or a
  "Criome unit," and there is no notion that "all contracts collectively = The
  Criome." That identity/vocabulary reframe (a Criome *is* a contract) is a
  designer/ARCHITECTURE decision, not a code change.

### 2. Root signing ceremony → root authority + subcontracts; one subcontract per cluster

- **Net-new:** no ceremony operation, no subcontract type, no root→subcontract
  derivation, no "normal operation happens in subcontracts" split. The current
  cluster runs a single flat 2-of-2 `Threshold` contract (mirror deploy), not a
  root + per-cluster-subcontract structure.
- **Partial anchor:** the single-key `ClusterRoot` admission anchor
  (`admission.rs:74`) is the only existing "root authority," but it authorizes
  *identity registration*, not a subcontract tree, and it is a bare key, not a
  contract. `Identity::Cluster(PrincipalName)` (`lib.rs:689`) and
  `KeyPurpose::CriomeRoot` (`admission.rs:56`) are latent building blocks.

### 3. Root contract = Criome with no parent; `parent` field carries a "root" variant

- **Net-new (clean):** `Contract` has no `parent` field of any kind
  (`signal-criome/.../lib.rs:725` is `Contract(Rule)`). There is no "root" variant
  anywhere on the contract type. Introducing a `parent: ContractParent { Root |
  Contract(ContractDigest) }` field (or equivalent) is a genuine schema addition to
  `signal-criome`, cascading through the rkyv store, the NOTA projection, admission
  validation, and the evaluator. The nearest existing recursion is the *time* base
  case ("`AttestedMoment` is the self-grounding base case", `ARCHITECTURE.md:764`),
  which is conceptually similar (a self-parenting root that stops a regress) but is
  about moments, not contracts.

### 4. Time-window / witness-clock; sign only inside window; collective = Criome clock; on-demand

- **Exists:** the time-window is carried on the request
  (`QuorumProposal.window`, `lib.rs:1941`); the consensus moment
  (`AttestedMoment` + `TimeSignature`s) is real and majority-checked with real BLS
  at the judge (`language.rs:615-654`); time-locks compare against the attested
  moment, i.e. the clock-as-consensus (`language.rs:297-314`); on-demand (no
  heartbeat) is already the model; ARCHITECTURE §8 documents the full vision
  (`ARCHITECTURE.md:750-766`).
- **Partial / missing (the load-bearing gap):** the per-signer gate "sign ONLY if
  my own clock ∈ window, so each signature testifies now" is NOT implemented —
  `sign_quorum_vote` (`signer.rs:344-368`) time-signs unconditionally without
  reading its clock. There is also no helper that constructs the window from "the
  submitting agent's own clock as start"; the caller supplies raw
  `opens_at`/`closes_at`. Making each signature a real "now" witness is net-new
  enforcement on top of an existing structure.

## Biggest gaps between current state and "operational Criome as deploy auth"

1. **No deploy/activation authorized-object or request op.** Criome authorizes
   `Operation | Contract | Agreement | Time | Head` (`lib.rs:1163`); a deployment is
   none of these. Becoming deploy-auth needs a deploy-authorization request +
   authorized-object kind + an activation-side gate that accepts only a
   Criome-authorized closure (and the SSH path demoted to fallback). Today the
   activation gate is `ssh root@<node> switch-to-configuration`
   (`lojix/src/schema_runtime.rs:4052-4118`) with no Criome involvement at all.
2. **Root/subcontract structure is absent.** No `parent` field, no root variant,
   no ceremony, no per-cluster subcontract. The psyche's whole "root authority in
   the root contract, normal work in per-cluster subcontracts" model (concepts 2+3)
   is net-new schema + a new establishment/maintenance flow, on top of today's
   flat single-contract, single-key-anchor reality.
3. **The witness-clock gate is not enforced.** Signers do not check their own clock
   against the window before time-signing (concept 4). Until they do, an
   `AttestedMoment` proves "a quorum co-signed this window," not "now is really
   inside it" — weaker than the psyche's "each signature testifies this time is now."
4. **Live subquorum gathering is missing.** The judge evaluates nested-contract
   subquorums recursively, but the gather driver only solicits flat `KeyMember`
   votes (`root.rs:1455-1472`), so a subquorum-shaped contract cannot be driven to a
   verdict across nodes today.
5. **Cross-node authority establishment is entirely hand-seeded.** No genesis /
   rotation ceremony; deploy-time `Configure` + `RegisterIdentity` + `AdmitContract`
   is the only path (`meta-signal-criome/.../lib.rs:236`; `admission.rs`). A
   "maintains root authority + subcontracts" ceremony (concept 2) does not exist.

## Unknowns / needs-psyche-decision

- `[needs-decision]` **Is a "Criome unit" literally a `Contract`, or a new wrapper?**
  Concept 1 can be satisfied by renaming/reframing the existing `Contract`, or by a
  new `Criome`/`CriomeUnit` type. Which the psyche wants determines whether this is a
  doc change or a schema change.
- `[needs-decision]` **Shape of the `parent` field (concept 3).** A `parent:
  ContractParent { Root | Parent(ContractDigest) }` on `Contract` is the literal
  reading, but it changes a content-addressed type (every existing contract digest
  shifts). Confirm whether "root" is a self-reference, a distinguished sentinel, or
  a separate `RootContract` type; and whether the parent link is semantic (evaluated)
  or purely provenance.
- `[needs-decision]` **What "one subcontract per cluster" governs (concept 2).**
  Is the per-cluster subcontract the *only* thing normal operations evaluate against
  (root reserved for membership/rotation), and does the root contract *contain* or
  merely *authorize* its subcontracts? This decides whether `ObjectMember`/`All`
  composition suffices or a new parent relation is required.
- `[needs-decision]` **Witness-clock enforcement strictness (concept 4).** Should a
  signer refuse to time-sign when its clock is outside the window (hard gate), or
  sign and let the crystallized moment bound "now" loosely as the ARCHITECTURE's
  "coarse crystallized-past" model implies? The current code is effectively the
  loose model; the psyche's phrasing ("only inside that window") reads as the hard
  gate.
- `[needs-decision]` **Does deploy-auth ride the router session or a direct criome-
  to-criome lane?** ARCHITECTURE names a "direct criome-to-criome peer lane for
  time-sensitive agreement" (`ARCHITECTURE.md:784`) separate from the router. Deploy
  auth could use either; the router session already carries the node-identity proof
  and encryption, the direct lane does not yet exist.

## Not checked (explicit)

- No build, `cargo test`, or witness binary was executed (read-only).
- I did not read the `sema-engine` internals (durability/fsync semantics) beyond
  the table API usage.
- The router `peer_session.rs` crypto was taken from `SecurityAudit-QuorumAndChannel.md`
  (committed-head audit), not fully re-read here.
- The SSH deploy path (lojix/CriomOS/goldragon) was mapped by a delegated read-only
  search, not personally re-read line-by-line; its file:line anchors are quoted as
  reported.
