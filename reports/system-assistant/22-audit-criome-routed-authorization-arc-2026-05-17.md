# 22 — Audit of the criome-routed-authorization arc

Date: 2026-05-17
Role: system-assistant
Scope: Recency-weighted audit of three converging reports on the
criome-routed authorization model: D/213 (most recent, designer-lane,
landed in repo ARCH), SYS/141 (system-specialist synthesis), SYS/21
(this lane's earlier report). Also reads OA/148 and DA/116 as
referenced substrate. Audits where each report holds up, where each
is superseded, and surfaces new questions none of them asked.

Commit-time recency:
- **D/213** — 19:46, `047da5db` — most recent, with companion repo
  edits landed in `criome` `4474bb8` and `signal-criome` `723e6c8`
- **SYS/141** — 18:13, `e38c8942` — sys-specialist synthesis
- **D/212** — 18:13, `ff5f0601` — designer-lane prior to /213
- **OA/148** — uncommitted working copy, ~17:44 — published criome
  authorization-decisions capture
- **DA/116** — uncommitted working copy, ~16:55 — OwnerSignal pattern
- **SYS/21** — 16:24, `28fb4483` — my prior report, the earliest in
  the converging arc

This audit gives most weight to **D/213 and the now-landed repo
ARCH text** (`criome/ARCHITECTURE.md` §"Authorization model" +
§"Security model — Unix-user as boundary"; `signal-criome` extended
wire), then to SYS/141, then to D/212 and OA/148, then to SYS/21.

---

## 0 · Headline

The architecture has converged faster than my SYS/21 anticipated.
Two of SYS/21's framings turned out to be partly wrong; D/213
moves substantially past them. SYS/141 caught most of the
intermediate drift before D/213 landed and asked the right
questions. The arc is now in a place where:

- The Unix-user-as-trust-boundary model (D/213 §1) is the
  architecture's load-bearing claim. It is sharp and well-argued,
  with one notable rough edge worth questioning (§5 below).
- The two policy classes + two escalation kinds in D/213 §4
  resolve the "policy DB vs signature-derived" tension that
  SYS/141 question #1 surfaced.
- The triad question (is `tui-criome` a separate triad?) is
  closed in D/213 favor: `criome` CLI and `tui-criome` are owner
  clients of the user's own `criome-daemon`, not separate
  daemons.
- Caller shape (G14 in SYS/21) is **finer-grained than SYS/21
  said.** SYS/21 said "operator's laptop runs CLI; optionally
  criome if it holds a key." D/213 makes the criome part
  **mandatory** wherever a Unix user wants to issue or approve
  authorization — and adds the under-explored implication that
  **a single host runs N criome daemons, one per Unix user**.

That last point is the audit's biggest finding: the criome
deployment shape that SYS/21 (and to some extent SYS/141) drew is
too coarse. Three meshes per node is wrong-by-one-dimension; the
right model has criome instances per (user, host) pair.

---

## 1 · Recency-weighted overview

| Report | Time | Status | Weight in this audit |
|---|---|---|---|
| D/213 | 19:46 | **Authoritative.** Companion ARCH edits already landed in `criome` and `signal-criome`. Reframes earlier reports' open questions. | Highest |
| SYS/141 | 18:13 | Strong synthesis. Identifies tensions; raises sharp questions. Some now-resolved by D/213. | High |
| D/212 | 18:13 | Prior designer-lane pass. D/213 explicitly resolves or revises most of D/212's findings (D/213 §9 maps them). | Subsumed by D/213 |
| OA/148 | ~17:44 | Captures user decisions on signature-derived (not ACL) permission and `tui-criome` shape. D/213 sharpens the `tui-criome` claim. | Subsumed by D/213 on tui-criome; correct on signature-derived |
| DA/116 | ~16:55 | Introduces the OwnerSignal pattern + per-component Unix-user enforcement. Foundation D/213 builds on. | High (substrate) |
| SYS/21 (mine) | 16:24 | Earliest. Got the broad-strokes three-mesh framing right but mis-framed criome as a policy-DB holder and was too coarse on per-Unix-user criome deployment. | Lowest (superseded in part) |

---

## 2 · What SYS/21 got wrong, called out honestly

### 2.1 Mis-framed criome as a "policy-DB holder"

SYS/21 §0 quoted the user's "*criome holds the permission data
(which key/quorum has which permission)*" and ran with the
implication that criome is essentially an ACL store. OA/148 had
already corrected this by the time SYS/21 was published — the
correct framing (now in `criome/ARCHITECTURE.md` §"Authorization
model"):

> *"Criome holds policy + collects signatures + issues grants. The
> daemon's policy data names which signers / which quorum are
> required for a request kind, but the actual permission is
> signature-derived: a grant is valid signatures over the exact
> request digest that satisfy criome's policy for that request."*

The user's "*criome holds the permission data*" was a statement
about **what criome needs to know** (which keys are needed for
which actions), not about the **mechanism** of authorization
(which is signature-derived, not ACL-derived). SYS/21 elided this.

SYS/141 question #1 caught the same tension and synthesized
correctly: *"Criome stores policy that says which signature
set/quorum is required for a request scope; the actual grant
derives from signatures over the exact request digest."* That
synthesis is now the criome ARCH's position.

**Audit verdict on SYS/21 here: SUPERSEDED.** Anyone reading
SYS/21's §3 ("permission data… policy DB") should read D/213 §4
("Two policy classes") instead.

### 2.2 Too coarse on per-Unix-user criome deployment

SYS/21 §2 drew the three-mesh diagram with one criome-daemon per
node. SYS/21 §4 then said: *"Operator's laptop runs… optionally a
local criome-daemon if the laptop holds a signing key."*

This is wrong-by-one-dimension. D/213 §1 anchors a criome daemon
to **a single Unix user, not a node**. Implications SYS/21 missed:

- A cluster node that runs services as `lojix-system` user AND
  hosts operator logins runs **multiple criome daemons**:
  - `criome-daemon` under `lojix-system` (signs daemon-issued
    cache attestations, holds the system-service signing key)
  - `criome-daemon` under each logged-in operator user (holds that
    operator's signing key)
- The operator's laptop doesn't run criome "optionally" — it runs
  criome **whenever the user wants to issue or approve
  authorization from that device**, which is most of the time.
- Cross-criome routing is therefore **two-axis**: (host, user). A
  request might hop from one user's criome to another user's
  criome on the same host, or to a remote-host criome.

The single-host within one user case (D/213 §1.5) is the cleanest
trust slice; cross-user-same-host and cross-host both leave that
slice.

**Audit verdict on SYS/21 here: WRONG.** The three-mesh diagram
should be re-drawn as "N criome daemons per host (one per
participating Unix user) + 1 lojix-daemon + 1 arca-daemon per
node." See §6 below for the new questions this raises.

### 2.3 Correct in broad strokes; right for the wrong reasons in some sub-points

What SYS/21 got right that D/213 confirms:

- **The three-substrate decomposition** (criome / lojix / arca) is
  the correct shape. D/213 doesn't contradict it.
- **The signal-lojix call is the signed object.** D/213 confirms;
  signal-criome wire now has `AuthorizeSignalCall` /
  `AuthorizationGrant` / `SignedObject` as first-class types.
- **BLS / quorum-capable from day one is a perfect fit.**
  Confirmed; D/213 builds on this directly.
- **ClaviFaber populates per-node Nix signing keys.** Still true,
  but with a sharper open question about how those relate to
  criome master keys — see §6.3.

What SYS/21 hand-waved that needed more precision:

- **"Every receiving daemon verifies independently against its own
  criome-daemon's identity registry."** Right shape, but under
  D/213 the verifier's criome is *a specific user's criome* —
  which one? See §6.4.
- **"Operator's laptop does not run lojix-daemon"** is correct, but
  the corollary "the laptop probably runs criome" is much
  stronger than "optionally" — see §2.2.

---

## 3 · What SYS/141 got right that resolved tensions

SYS/141 is the strongest of the three reports in the arc on
*synthesis*. Specific wins:

### 3.1 Caught the policy-vs-signature framing conflict (Q#1)

SYS/141 saw both my SYS/21 ("criome holds permission data") and
OA/148 ("criome is not an ACL") and synthesized correctly. D/213
adopted essentially that synthesis. **This was the question that
unblocked D/213's two-policy-class framing.**

### 3.2 Caught the tui-criome conflict (Q#2)

OA/148 said tui-criome is "a separate component with its own Sema
database for persistent signing-client state" (a near-triad). D/213
says tui-criome is **an owner client of the user's own
criome-daemon, not a separate triad.** SYS/141 flagged the
contradiction; D/213 chose the cleaner direction.

The leftover question SYS/141 didn't fully resolve: where does
**signing-client private key custody** live if tui-criome is just
an owner client? OA/148 said tui-criome holds "signing-client
private/public keypairs." D/213 says criome holds the master key.
This isn't quite a contradiction — tui-criome could hold *non-
master* signing keys (e.g. delegated subkeys for specific
operations) — but D/213 defers subkeys to future-possibilities,
which leaves tui-criome's key-custody role under-specified.

**Audit verdict: tui-criome's exact key-custody story is still
under-specified after D/213.** See §6.5.

### 3.3 Surfaced the NixDaemonConfigurationActor refinement

SYS/141 §"Nix configuration ownership" sharpened SYS/21 §7 with a
better mechanism: rather than lojix-daemon owning all of
`/etc/nix/nix.conf`, CriomOS installs a stable include point
(`!include /var/lib/lojix/nix/nix.conf`) and lojix-daemon owns
only the include file plus the restart lock. This is **better
than SYS/21's framing** — it preserves human-/system-edit
authority over the main nix.conf and restricts lojix's blast
radius to the include slot.

### 3.4 Concrete `DeploymentArtifactSet` shape

SYS/141 §"Artifact set" enumerated nine specific digests
(signal_lojix_request, criome_authorization, horizon_proposal,
cluster_proposal, viewpoint, projected_horizon,
generated_nix_inputs, topology_snapshot, deployment_plan). This is
more useful than my SYS/21's vague single `DeploymentPlanArtifact`
blob. **Adopt SYS/141's nine-digest enumeration.**

### 3.5 The invariant that makes authorization testable

SYS/141 §"Actors I expect in lojix" states:

> *"No actor that mutates Nix, the store, a cache session, or a
> system profile runs before `CriomeAuthorizationActor` grants the
> exact request/scope."*

This is sharp, testable, and exactly the right invariant. SYS/141
question #9 even names the right first test: *"prove no Nix
effect happens before fake Criome grant; prove a digest-mismatched
grant fails."*

---

## 4 · What D/213 establishes, and where its arguments are strong/weak

### 4.1 STRONG — Unix-user as the security boundary (§1)

The argument: *"In a world of AI agents, a process running as Unix
user X can spawn an agent that controls the entire user-X session
— reading the screen, moving the mouse, listening to audio,
typing keystrokes… The illusion that 'this sensitive operation
runs in its own GUI process, so it's isolated' no longer holds.
What does remain enforced is the kernel's Unix-user file
permission model."*

This is **the correct rationale** for the design choice, and it
generalizes: every owner-class surface in the workspace (per
DA/116's OwnerSignal pattern) should rest its authority on Unix-
user filesystem permissions. The criome ARCH now states this
explicitly.

### 4.2 STRONG — Two policy classes (§4)

Simple (self-signed by master key) and complex (quorum across peer
criome daemons) covers the immediate need without committing to a
rich policy schema. Rich schema deferred to "Future possibilities"
in criome ARCH. This is correct discipline — ship the two cases
that matter; defer the speculative.

### 4.3 STRONG — Two escalation kinds (§4)

Escalation-to-sign (policy pre-baked, criome signs autonomously)
vs escalation-to-approve (criome routes to owner before signing) is
the right cut. The latter is what makes long-running TUIs
necessary. **Worth questioning: D/213 says simple policies *may*
require escalation-to-approve; what's the configured surface for
"this simple policy needs owner approval each time"?** See §6.7.

### 4.4 STRONG — Three-classes-of-clients refinement (§6)

The owner / peer-signer / consumer split (mapped to owner-signal-
criome vs signal-criome) is sharper than D/212's two-worlds split
and resolves the contract-scope question cleanly. Anyone now
asking "what verbs belong on which contract?" has a clear answer.

### 4.5 WEAK — Plaintext-passphrase-over-local-socket reasoning (§1.2)

The argument: *"if attacker is already same-UID, they can do worse
via /proc/<pid>/mem etc., so plaintext password on the socket adds
no attacker surface."*

The reasoning **is true within its stated threat model** but has
two weaknesses worth questioning:

1. **It assumes the attacker has same-UID code-execution.** A
   *different* attack surface (TOCTOU in the daemon's socket
   handling, path-traversal-via-symlink in the runtime dir, a
   protocol bug that allows partial frames to bypass auth) could
   let an attacker who is *not* same-UID intercept passphrase
   bytes. Defense-in-depth crypto on the wire (e.g., symmetric
   encryption with a key derived from a per-session ECDH) is cheap
   and would close this gap.
2. **It tightens a defensive coupling.** Once the architecture
   says "we don't need encryption between same-UID processes,"
   every future feature that crosses that boundary (e.g., a
   privilege-elevated probe, a cross-namespace component, a future
   sandboxing layer) needs to revisit the assumption. Encryption
   on the wire is a no-regret choice.

**Audit verdict on D/213 §1.2: defensible but worth strengthening
with cheap defense-in-depth.** Question for the user in §6.

### 4.6 OPEN — Cross-host transport (§5.3)

Four options listed (TLS-wrapped, per-frame signed envelope,
BLS-signed wire, SSH tunneling); none chosen. D/213 names this as
deferred. SYS/141 also flags this as Q#6. **This is the highest-
priority remaining design decision in the criome arc.** Without
it, quorum-with-remote-peers cannot be implemented.

### 4.7 UNDER-SPECIFIED — Predictable peer socket names (§5.1)

Format: `<user-runtime-dir>/criome/<short-hash-of-master-pubkey>.sock`.
Collision is "inconvenient, not dangerous" because signature
verification is authoritative.

True, but **the routing layer needs a disambiguator when
collision happens.** D/213 says "the operator (or the peer-routing
table) names the target by full pubkey." How exactly? Is there a
fallback path like
`<user-runtime-dir>/criome/<full-pubkey-hex>.sock`? Does the
peer-routing-table entry include both the short hash and the full
pubkey for collision-handling?

This is a small detail but affects implementation cleanliness.

---

## 5 · The biggest weakness across all three reports

**None of the three reports name what happens for unattended
system-daemon criome instances.**

D/213's owner-driven model assumes a Unix user enters a passphrase
on each daemon startup. This works for operator-user criome
(the operator is at the keyboard). It **does not work for a
cluster node's `lojix-system` user criome** that needs to come up
on boot, before any human is around to enter a passphrase.

Two options for unattended boot:

1. **Master key unencrypted at rest, protected only by filesystem
   permissions.** Acceptable under D/213's logic if filesystem
   permissions are the security boundary. But: this means a node
   compromise gives an attacker the system criome master key
   permanently.
2. **Master key passphrase held in TPM or system-secret;
   unsealed on boot via PCR-bound policy.** Stronger but introduces
   TPM dependency and a different operational model.

This is **not** addressed in D/213, SYS/141, OA/148, or SYS/21.
It is a real gap that blocks the production criome deployment on
cluster nodes. See §6.6.

---

## 6 · The best questions to surface (audit's contribution)

Per the user's "bring forth the best questions" — these are the
ones I think matter most, distilled from cross-reading the arc.
Some are SYS/141's still-live; some are new.

### Q1 [NEW] — How does cross-user-on-same-host criome routing actually work?

Under D/213, a cluster node has multiple criome daemons (one per
participating Unix user). When `lojix-daemon` (running as
`lojix-system` user) receives a deployment intent from an operator
command and needs an operator signature, where does the routing go?

- Local UNIX socket lookup at `${OPERATOR_RUNTIME_DIR}/criome/<...>`?
  But `${OPERATOR_RUNTIME_DIR}` typically requires the operator user
  to be logged in; system services can't easily traverse another
  user's runtime dir.
- Same-host TCP loopback with peer authentication?
- A persistent system-level "criome routing socket" that any
  criome can talk to and that brokers cross-user delivery?

D/213 says "predictable peer socket names" but the per-user runtime
directory model breaks if the requester isn't logged in as that
user. **This is a real gap.**

### Q2 [NEW] — Is the cluster system criome a full participant or a "machine identity"?

If yes (full participant): then `lojix-system` user's criome holds
a master key, can sign autonomously per simple-policy, can
participate in quorums. This implies cluster system criomes have
significant authority — they can sign deploy-cache attestations,
verify peer-cluster signatures, etc.

If no ("machine identity" only): then `lojix-system` criome holds
only verification keys + routing tables, never signs anything
itself, and every authorization needs an external (operator)
signature.

D/213 doesn't distinguish. SYS/141 question #4 ("does one
authorization cover all local effects?") leans on this — if the
node criome can sign autonomously for its own local effects, the
operator only needs to sign the top-level intent; per-effect
signatures are unnecessary.

**Lean: full participant, but with policy that requires operator
signature for high-risk actions (initial deploys to production
targets, certain irreversible operations); auto-sign for routine
internal effects (cache content attestation, internal trust
mutation under operator policy).**

### Q3 [SYS/141 Q#7, refined] — Are ClaviFaber's Nix-signing keys, criome master keys, and SSH host keys the same or separate?

D/213 doesn't address. SYS/141 leans separate. I agree separate,
with the additional point that **the right operational model is**:

- ClaviFaber, at first boot, generates a per-node key bundle:
  - Nix binary-cache signing key
  - Criome master key (for `<service-user>-criome`)
  - SSH host key
  - Possibly Wi-Fi/Yggdrasil/cluster-mesh keys
- All published into the appropriate registries (criome identity
  registry for the criome keys; Nix's `trusted-public-keys` for
  the cache key; etc.).
- Each key has one trust domain — never reused across domains.

**Worth confirming with the user before implementing ClaviFaber's
first-boot key generation.**

### Q4 [NEW] — What's the bootstrap passphrase model for unattended system daemons?

(See §5 above.) Options:
(a) Unencrypted master key with filesystem-permission protection
    only.
(b) TPM-sealed passphrase with PCR-bound policy.
(c) Operator-injected passphrase at first cluster bring-up, with
    automatic unlock on subsequent reboots via local KDF (more
    complex; depends on disk integrity).
(d) Cluster-quorum unsealing — node asks N peers to attest its
    identity, then receives a shard that unlocks its key.

**Lean: (a) for v1 (matches D/213's "filesystem permissions are
the boundary" claim); (b) once TPM integration is on the
roadmap.**

### Q5 [SYS/141 Q#3, sharper] — What exact bytes are inside the SignedObject?

Under D/213, `SignedObject` wraps the signal-lojix request payload.
But security-relevant context fields must be inside the signed
bytes to prevent rebinding attacks:

- The exact `request_id` / canonical request digest
- The target cluster
- The target node
- The action (e.g., `Deploy`, `Activate`, `MutateNixConfig`)
- An expiry timestamp
- An anti-replay nonce or sequence number
- The issuing criome's identity (so verifier knows which
  identity-registry to query)

**If any of these are *beside* the signed bytes rather than
*inside*, an attacker can rebind a grant from one context to
another.** SYS/141's lean (all security-relevant scope in the
signed canonical object) is correct; this needs to be made
explicit in the wire crate's `SignedObject` definition.

### Q6 [SYS/141 Q#6, restated] — Cross-host criome transport

D/213 §5.3 names four options, picks none. The decision blocks
quorum-with-remote-peers, which is a load-bearing feature for any
multi-host policy.

My lean (informed by the workspace's existing primitives):
**per-frame BLS-signed envelope** (option 3 in D/213). Reasons:
- Reuses the cryptographic primitive criome already requires
  (BLS via `blst`).
- No TLS PKI management overhead.
- No SSH external dependency.
- Confidentiality only where needed (passphrase exchange never
  crosses hosts anyway — see Q1's cross-user issue, which suggests
  same-host cross-user is a separate problem).

### Q7 [NEW] — When does criome's policy require owner-approval for a simple policy?

D/213 §4 says: *"Either policy class may be paired with escalation-
to-approve."* So a simple policy (criome signs with its own master
key) can still demand owner approval before signing. The
configuration surface for "this simple policy always needs owner
approval" / "this simple policy only needs owner approval for
high-value scope" is **not specified.** Is this a per-policy-record
boolean? A scope-pattern-based predicate?

Probably this is part of the deferred rich policy schema — but it's
worth being explicit that escalation-to-approve frequency is a
real operational lever the user will want to tune.

### Q8 [NEW] — How does an `AwaitingAuthorization` lojix-daemon survive its own restart?

If lojix-daemon submits an `AuthorizeSignalCall`, gets
`AuthorizationPending`, and then crashes/restarts mid-wait, how
does it resume? Recipe:

- lojix-daemon writes the `request_id` + `criome_observation_token`
  to its sema-engine ledger before issuing the call.
- On startup, lojix-daemon scans for pending `AwaitingAuthorization`
  ledger entries and re-issues `ObserveAuthorization` subscriptions.
- If the criome-daemon has restarted in the meantime, the
  authorization may be `AuthorizationUnavailable` — lojix-daemon
  then re-submits.

This composes with SYS/137's "Coordinator dies → participants
continue local jobs" invariant but **wasn't explicitly tested as
a composite invariant** in any of the reports. Worth a witness.

### Q9 [NEW] — Policy mutation auditability

D/213 says policy mutation is an owner-class operation on owner-
signal-criome. But:
- Are policy mutations themselves audit-logged separately from
  signature events?
- Can the owner mutate policy to be more permissive without a
  second signature (the master key is already in the daemon's
  hand)? This is a self-elevation vector.
- Is there a "freeze policy mutation under conditions X" mechanism
  (e.g., during a deploy)?

Probably criome's existing append-only audit log handles (1), but
(2) and (3) are real questions.

### Q10 [NEW] — Verifier's policy vs originator's policy

When peer lojix-daemon B receives a `SignedObject` from lojix-
daemon A and asks B's local criome to verify:

- B's criome verifies the BLS signatures are valid against its
  identity registry.
- But does B's criome check that the signatures satisfy *A's*
  intended policy, or *B's* policy?
- These could differ if A's criome is under a different policy
  set than B's.

Likely answer: the `SignedObject` carries the *satisfied policy
spec* (which signers / what quorum), and B's criome checks "is
this satisfied policy spec acceptable for this action?" — i.e., a
two-step verification: (signatures valid) AND (the spec the
originator satisfied matches what I would have required for this
action). **Worth confirming and putting in the wire.**

### Q11 [SYS/141 Q#9 sharpened] — First testable witness

SYS/141 lean: prove no Nix effect runs before fake Criome grant;
prove digest-mismatched grant fails. Both right.

I'd add one more: **prove that a SignedObject lacking a
required-by-policy signer is rejected**, exercising the policy-
table consultation path end-to-end. Otherwise the first witness
only tests "is auth required at all" without testing "which auth
is required."

### Q12 [NEW] — The relationship between operator-signed deploy intent and operator login state

If quorum gathering can take days (D/213 §3), an operator might
sign at home in the morning, the quorum doesn't complete until
overnight, and by then the operator's laptop is offline. Does the
deploy continue? Specifically:

- If operator's signature was already collected (signed and
  submitted to a criome), the operator going offline is fine —
  the signature persists in some criome's signature-solicitation
  state.
- If operator's signature is still pending (criome routed an
  escalation-to-approve and the operator hasn't responded), the
  operator going offline means the request stalls.
- Wire shape: criome-daemon's pending-authorization state needs to
  track "who is solicited but not yet responded" so the operator
  (on next login) can see what's awaiting them.

D/213 implies this works but doesn't spec it explicitly.

---

## 7 · Risks worth surfacing

### 7.1 Risk: rich-policy-schema deferral lulls implementation into the simple-only case

D/213 §7 defers action-pattern granularity, subkeys, weighted
thresholds. Reasonable for v1 — but implementation should preserve
the **shape** of the policy table such that v2's richer schema can
be added without a table migration. Specifically:

- Policy records should be content-addressed in sema so that v2
  policies (more fields) coexist with v1 policies (fewer fields).
- The policy-lookup path should be a versioned trait, not a
  hard-coded match on the two v1 classes.

### 7.2 Risk: cross-user-same-host criome routing is harder than cross-host

The cross-host case has clear network primitives. The cross-user-
same-host case (Q1) is operationally weirder — you can't easily
reach `${OTHER_USER}/runtime` from a system service. This is a
genuine architectural gap.

### 7.3 Risk: tui-criome's leftover key custody role

OA/148 said tui-criome holds private signing-client keys. D/213
says master key lives in criome-daemon. Subkeys are deferred. Net:
what does tui-criome's "sema database" hold that the criome
daemon doesn't already? If nothing, why does tui-criome need its
own sema at all (vs. being a stateless TUI client of the daemon)?

This is a small but real ambiguity that the next pass should
resolve.

### 7.4 Risk: forgetting that criome IS a PKI

D/213 §5.3 (cross-host transport) notes briefly: *"criome IS a PKI;
criomes can issue certs for each other."* This is a powerful
observation that none of the reports developed. Implications:

- TLS option (5.3 option 1) becomes much cheaper because cert
  issuance is intrinsic.
- The cluster identity model (ClaviFaber registers nodes →
  criome master keys → trust topology) is essentially a CA
  hierarchy without needing a separate CA component.
- Future TLS termination for sensitive UIs can use criome-issued
  certs.

Worth surfacing as an architectural strength.

---

## 8 · Adopt / revise recommendations

Net recommendations for what to take forward from each report:

| Report | Adopt as-is | Revise | Drop / supersede |
|---|---|---|---|
| D/213 | §1 Unix-user trust boundary; §4 two policy classes + two escalation kinds; §6 three-classes-of-clients mapped to two contracts; §5.1 predictable peer socket names | §1.2 plaintext-passphrase reasoning (strengthen with defense-in-depth); §5.3 cross-host transport (pick option 3) | nothing |
| SYS/141 | §"Nix configuration ownership" (include-point shape); §"Artifact set" (9 digests); §"Actors I expect in lojix" invariant (auth-before-nix); §"Best implementation sequence" 1-10 | §"Architecture to implement" §"Meshes" diagram (refine for per-user criome) | nothing |
| OA/148 | "signature-derived, not ACL" core claim | tui-criome description (D/213 supersedes) | tui-criome-as-separate-triad framing (D/213 supersedes) |
| DA/116 | OwnerSignal pattern; per-component Unix-user enforcement direction | nothing material | nothing |
| SYS/21 (mine) | three-substrate decomposition (broadly correct); BLS-quorum match | "every receiving daemon verifies via its own criome" (right shape, needs which-user precision); operator-laptop "optionally" criome | "criome holds permission data" framing as ACL/policy DB (superseded); single-criome-per-node implication (wrong) |

---

## 9 · The shortest-path-to-implementation given this audit

Synthesizing across all four:

1. **Pick cross-host transport now** (Q6). Per-frame BLS-signed
   envelope is my lean. Blocks quorum work.
2. **Resolve cross-user-same-host routing** (Q1). May share the
   cross-host transport answer or be its own decision.
3. **Resolve unattended-system-daemon bootstrap** (Q4). Choose
   between unencrypted-with-filesystem-permissions (v1) and
   TPM-sealed (v2).
4. **Spec the SignedObject canonical bytes** (Q5). What exact
   fields are inside the signed digest.
5. **Spec ClaviFaber's first-boot key bundle** (Q3). Separate
   keys per trust domain.
6. **Build the first witness slice** (Q11): no-Nix-effect-before-
   grant; digest-mismatched-grant-fails; policy-required-signer-
   missing-rejects.
7. **Build the lojix-side `CriomeAuthorizationActor`** (SYS/141
   step 2). Sequenced after 1-5.
8. **Land arca cross-node FetchHash** (SYS/20) — independent of
   the criome work; can land in parallel.
9. **Land the `deploy.rs` split toward new actor planes**
   (SYS/137) — also independent.

Items 1–5 are designer-lane decisions; items 6–9 are operator-
lane implementation. The arc's bottleneck is the designer-lane
sequence above.

---

## 10 · What I'd tell the user inline

The architecture is in a strong state — substantially more
settled than SYS/21 implied. The audit's three biggest takeaways:

1. **My SYS/21 was wrong about per-node criome (it's per-Unix-user
   per-host) and wrong about criome being a policy DB (it derives
   permission from signatures).** D/213 has the right model now.
2. **The single biggest unresolved decision is cross-host criome
   transport (D/213 §5.3 / SYS/141 Q#6).** Pick it before
   quorum-with-remote-peers becomes implementable. My lean:
   per-frame BLS-signed envelope.
3. **The biggest unstated gap is unattended-system-daemon
   bootstrap (§5 of this audit, Q4).** A `lojix-system` user
   criome on a cluster node has no human to enter a passphrase at
   boot. Needs an explicit decision before cluster-side criome
   ships.

The biggest single architectural strength the reports collectively
landed on: **criome IS a PKI.** ClaviFaber registers nodes, criome
masters anchor identity, peer routing is intrinsic. That makes
TLS/certs cheap, makes cross-component trust uniform, and reuses
the existing primitive throughout.
