# Criome Prior-Art Research — Cited Comparative Map

Purpose: map existing cryptographic-authority systems onto the five hard problems
in Criome's design, one problem at a time, and say plainly where a system does
something better or differently than the others. This is not a general survey;
every row is scored against Criome's stated mechanics.

Criome-in-one-paragraph (the target we are mapping to): a hierarchy of
cryptographic contracts, each with a `parent`, chaining to a single **root**
whose identity is a content-addressed hash of its accepted genesis state
(ideally carrying the admitting quorum signatures). Children are self-owned by
default; a parent may grant **time-leased self-ownership** that the child renews
or lets lapse (lapse reverts ownership to the parent). A **BLS-majority quorum**
authorizes state changes. Every signing request carries a **time window**; each
signer signs only inside it, so the signatures collectively form a consensus
**clock**, and a request window exceeding a lease is automatically invalid. End
goal: a deployment-authorization layer replacing SSH-as-root.

Legend for the Steal/Avoid column: **STEAL** = adopt this pattern; **AVOID** =
a documented failure mode to design around; **NOTE** = a difference to reconcile.

## Q1. Genesis identity that carries its own signatures

How does a root/genesis object get a durable, self-certifying identity, and how
are the admitting signatures bound to it? Does identity exist at submission or
only after quorum finalizes?

| System | Concrete mechanism | Tradeoff | Steal / Avoid |
|---|---|---|---|
| **KERI inception** [arXiv 1907.02143; ToIP KERI spec] | Identifier prefix = a **SAID** (self-addressing identifier): a digest of the inception (`icp`) event, whose body includes the initial signing keys **and a pre-rotation commitment** (a digest of the *next* key set). Identity self-certifies its own genesis. Signatures are **attachments**, not part of the SAID'd body; witness receipts (from witnesses named in `icp`) are added after and anchor/order the event. | Identity exists **at inception**, before receipts — receipts add accountability/duplicity-detection, not identity. Embedding a SAID inside its own event needs the dummy-placeholder derivation (hash with the SAID field zeroed, then backfill). | **STEAL**: make root identity = digest of the genesis *state incl. the pre-commitment to the admitting/quorum keys*; keep the BLS signatures as attachments keyed to that digest. **STEAL** pre-rotation: commit to the next quorum's key-digest so a root survives key compromise. |
| **TUF root** [TUF spec; theupdateframework.io] | `root.json` = a `signed` body (key definitions + role thresholds + `expires` + integer `version`) plus a sibling `signatures` array; valid iff a **threshold N-of-M** of root keys sign. Root identity is the key set + version, not a hash. Rotation: version n+1 must be signed by a threshold of **both old and new** root keys. | Bootstrap is TOFU — the client must ship an initial root out of band. Identity is not content-addressed, so two histories can share a version number. | **STEAL** the **old+new co-signed rotation** rule verbatim for Criome membership rotation: bind every quorum transition to a threshold of both the outgoing and incoming quorum. **NOTE** signatures live *beside* the signed body, never inside the hashed identity. |
| **BFT genesis block** [Tendermint/CometBFT genesis] | Genesis block/file fixes the initial validator set + chain-id; the block hash becomes chain identity; later blocks carry validator signatures. | Genesis trust is **out-of-band configuration**, not carried self-certifyingly in the object; the admitting signatures are usually absent from genesis itself. | **AVOID** leaning on out-of-band genesis config that the object cannot itself prove. |
| **Content-addressing (IPFS/IPLD CID, git)** [multiformats CID; git object model] | CID = multihash(content)+codec; git oid = hash(type+content). Immutable, self-verifying **integrity**. Signatures are a separate layer (git signed commit/tag; an IPLD node whose field is a signature over a child CID). | The bare hash proves integrity/immutability, **not authority** — a CID says nothing about who admitted it. | **STEAL** content-addressing for durable, relocatable identity. **AVOID** the trap that a hash carries authority: fold the admitting quorum's *keys/commitment* into the hashed genesis and carry the *signatures* adjacent. |

Best-in-class for Q1: **KERI**. It is the only system whose identity is *both*
content-addressed *and* carries the genesis key material self-certifyingly, and
it already answers Criome's "identity at submission vs after quorum" cleanly:
identity exists at inception; quorum/receipts finalize accountability, not
identity. TUF contributes the one thing KERI does not need but Criome does — a
threshold-quorum admission with a proven co-signed rotation rule.

Design-trap flagged: Criome's phrasing "hash **carrying** its own quorum
signatures" is self-referential (signatures would sign a hash computed over the
signatures). Every mature system resolves this the same way — **the digest
covers the state/key-commitment; the signatures are attachments bound to the
digest**. Adopt that split.

## Q2. Authority derivation to a root, with revocation

How does a verifier confirm a child's authority by walking to a known root, and
how is revocation expressed?

| System | Concrete mechanism | Tradeoff | Steal / Avoid |
|---|---|---|---|
| **X.509 path validation** [RFC 5280] | Chain leaf→intermediate(s)→trust-anchor; each link a signature by the issuer's key; `BasicConstraints` (CA, pathlen), `NameConstraints`, `KeyUsage` scope authority. Revocation is **external**: CRL (periodic revoked-serial lists) or OCSP (online query), plus stapling. | Revocation is PKI's chronic failure: CRLs go stale/huge, OCSP is a privacy + availability liability, browsers **soft-fail** so revocation often does nothing. | **STEAL** the walk-to-anchor validation shape. **AVOID** external CRL/OCSP-style revocation as the primary lever — it is the historically broken part; prefer expiry (Q3). |
| **Certificate Transparency** [RFC 6962 / RFC 9162] | Append-only Merkle log of certs; log emits an **SCT** (promise to log) and a signed **STH** (tree head); monitors/auditors + **gossip** detect a log serving split histories; **witness cosigning** of the STH (RFC 9162 / cothority) hardens against equivocation. | Detection, not prevention; needs an ecosystem of monitors. Not a revocation system. | **STEAL** the append-only log + inclusion proofs to make authority grants publicly auditable and **non-equivocable**; cosign the head so a proposer cannot show different quorum-histories to different signers. |
| **SPKI/SDSI** [RFC 2693] | **Authorization** certs, not identity certs: a 5-tuple (issuer, subject, **delegation bool**, authorization S-expr, **validity dates**). Authority derives by chaining auth certs from the verifier's *own* key (no global CA); a chain **reduces** to one effective tuple. The delegation bool controls onward re-grant. | No global namespace — each verifier roots trust in its own keys (decentralizing, but no global identity). Revocation via validity dates + optional revalidation. | **STEAL** authority-as-delegation with an explicit **may-this-child-re-grant** bit — a near-exact fit for Criome parent→child grants — and the "chain reduces to one effective authority" mental model for validation. |
| **KERI delegated identifiers** [KERI spec] | Delegated inception (`dip`) names the delegator AID; the delegation is **anchored by a seal in the delegator's KEL** (delegator's log contains a digest of the child event). **Two-way binding**: child references parent, parent's log anchors child. Cooperative — both events must exist. | Requires both sides to act (delegator must anchor). Heavier than a one-way issuer signature. | **STEAL** the **two-way anchor** — parent contract anchors the child's genesis digest — which is strictly stronger than X.509's one-way "issuer signed child," and is the natural place to encode the time-lease (Q3). |
| **TUF delegated targets** [TUF spec] | Root→targets, targets→sub-roles, each delegation naming keys + a **threshold** + a **path/scope pattern** the sub-role may sign, with terminating vs non-terminating delegations. Revocation = re-sign the parent removing the delegation; `expires` forces refresh. | The delegation graph gets complex; delegation order matters. | **STEAL** per-delegation **threshold + scope** — "one subcontract per cluster" maps directly onto a scoped, thresholded sub-role governing only its subtree. |

Best-in-class for Q2: split verdict. **KERI's two-way anchor** is the strongest
*integrity* binding of child to parent; **SPKI/SDSI** is the cleanest *authority*
model (delegable authorization tuples, no global CA) and matches Criome's
self-owned-child semantics best; **CT** is the reference answer for making the
authority history *non-equivocable*. X.509 is included mainly as the
cautionary tale on revocation.

Design guidance: express revocation as **expiry + re-anchoring** (KERI/TUF),
never as an out-of-band revoked-list (X.509). Give each parent→child grant an
explicit delegation/re-grant bit (SPKI) and a scope (TUF). Cosign the
authority head (CT/RFC 9162) so no proposer can present divergent histories to
different quorum members.

## Q3. Time-leased ownership / capability expiry

How do systems bound a capability in time, and handle renewal vs. lapse?

| System | Concrete mechanism | Tradeoff | Steal / Avoid |
|---|---|---|---|
| **TUF `expires`** [TUF spec] | Every role's metadata carries `expires`; a client **rejects expired metadata**. Short expiry on fast roles (timestamp), long on root. This is the anti-rollback / freshness floor: an attacker withholding updates cannot pin a client on stale metadata past expiry. | Requires an available signer to re-sign before expiry (liveness cost) — i.e. the renewal cost is inherent. | **STEAL** per-contract `expires` as the lease: short on the child's self-ownership grant, long on the root. Reframe "lapse reverts to parent" as **the child's self-signed authority simply stops validating when stale** (a local check), not a broadcast. |
| **Macaroons** [Google 2014] | Caveats **attenuate only** (chained HMAC — easy to add, impossible to remove). A first-party caveat like `time < T` is checked locally by the verifier; a **third-party caveat** needs a discharge macaroon from a named party, recursively verified. | Bearer credential; verifier must have context to evaluate first-party caveats. | **STEAL** the lease as a **first-party time caveat** baked into the capability, and model "signing window ⊆ lease" as a **caveat conjunction** (both must hold). Third-party caveat ≈ "the parent quorum must discharge" for continued self-ownership. |
| **Biscuit** [Biscuit spec, biscuitsec.org] | Offline attenuation via chained signed blocks (single-use keypairs prove chaining); **datalog** checks; TTL = a check on a `time` fact; **third-party blocks** carry an external signature so a block's facts are attributed to a trusted party with no online contact. | Bearer token; revocation needs a revocation-id list. | **STEAL** datalog-style checks to express "window ⊆ lease ⊆ parent-grant" declaratively, and the **third-party block** as the model for a child carrying its parent's lease-grant signature **inline**. |
| **Short-lived certs / ACME** [ACME RFC 8555; short-lived cert practice] | Certificate lifetimes of hours/days so **revocation ≈ expiry**; ACME automates re-issuance. | Requires automated, available renewal infrastructure. | **STEAL** the biggest PKI lesson: **short lifetime instead of revocation**. Criome leases should be short and auto-renewed, not revert-on-broadcast. Leases *are* short-lived certs for ownership. |
| **Vault/Consul leases** [HashiCorp Vault leases] | Every token/secret has a lease TTL + a hard **max_TTL** ceiling; renew extends up to max_TTL; on lapse it is **auto-revoked**; revocation **cascades down the lease tree** (child leases die with parent). | A **central** lease manager tracks and revokes all leases — Criome is distributed, with no such central authority. | **STEAL** the lease tree with a **hard max_TTL ceiling** (= Criome's "window can't exceed lease," generalized) and cascading expiry. **AVOID** Vault's central revoker: Criome must make lapse **locally verifiable** via expiry carried in the object, not by a central revocation service. |

Best-in-class for Q3: **ACME short-lived certs + Vault's max_TTL ceiling**
together are the closest to Criome's leased self-ownership. TUF `expires`
supplies the exact "reject-when-stale" verification rule; macaroons/Biscuit
supply the declarative "window ⊆ lease" check.

Design guidance: implement the lease as **object-carried `expires` + a hard
ceiling**, verified locally; the request-window-exceeds-lease rule is a
caveat/max_TTL conjunction that **each signer must check before signing** (not
only the judge), so a colluding proposer can never collect partial signatures on
an over-long window.

## Q4. Verify-by-ancestor-chain sparse replication

How can a node hold only an object plus its ancestor line to a known root and
still verify it, without the whole global database?

| System | Concrete mechanism | Tradeoff | Steal / Avoid |
|---|---|---|---|
| **X.509 chain validation** [RFC 5280] | To verify a leaf a client needs only leaf→intermediate(s)→anchor, with the anchor pre-provisioned in its trust store (AIA fetches missing parents). No global PKI copy needed. | Says nothing about completeness/currency of the wider PKI (revocation is the separate, weak channel). | **STEAL** — this is Criome's model exactly: hold the object + ancestor contracts; the root digest is the pre-provisioned anchor. Confirms feasibility. |
| **KERI KEL replay + receipts** [KERI spec] | A validator holding only an AID's KEL (ordered, hash-linked key events) replays inception→now, verifying each event's signatures and hash links; witness receipts confirm witnessing. For a **delegated** AID you must also fetch the **delegator's anchoring slice**. | The "ancestor line" of a child is not just the child's own log — it includes the parent's anchoring events. | **STEAL** replay-from-genesis with hash-linking; and the hard requirement that **sparse replication ship the parent's anchoring records**, not only the child's own contract chain. |
| **Merkle-DAG partial sync (IPFS/IPLD, git shallow/partial clone)** [IPLD; git partial clone] | Content-addressed DAG lets a node fetch only the sub-DAG it needs (git `--filter`/`--depth`; IPFS blocks fetched by CID on demand); each CID verifies its children by hash. | Integrity of what you hold ≠ **completeness** — you cannot tell you have the whole relevant set without a head/root reference. | **STEAL** content-addressed sub-DAG shipping (object→root is self-verifying by hash). **AVOID** conflating integrity with completeness — pair it with a signed head. |
| **Merkle inclusion proofs** [RFC 6962/9162] | Prove a leaf is in a tree of size N given the signed head, in O(log N) hashes. | Needs a trusted/cosigned head. | **STEAL** if Criome ever needs "this contract is in the accepted set" without shipping the set — log-space proof against the signed root head. |

Best-in-class for Q4: **KERI KEL replay** is the closest to Criome because it
handles the exact wrinkle Criome has — a *delegated* (child) object's ancestor
line includes the parent's anchoring slice, not just the child's own chain.
X.509 confirms the plain leaf→anchor case; Merkle-DAG sync is the transport
mechanism.

Design guidance: sparse replication ships **the child's contract chain + each
parent's anchoring record up to the root digest**. Because hash-chain integrity
does not prove currency, pair the chain with **anti-rollback**: a signed
head/latest-seen (TUF `expires` / KERI latest-event) so a node cannot be pinned
to a stale-but-valid ancestor line — which conveniently coincides with the lease
expiry from Q3 (a stale chain's leases have lapsed).

## Q5. Witness-based consensus time (the "Criome clock")

How do multiple parties' signatures establish trusted time without a central
clock?

| System | Concrete mechanism | Tradeoff | Steal / Avoid |
|---|---|---|---|
| **Roughtime** [draft-ietf-ntp-roughtime] | Client sends a nonce; server returns a **signed (time ± radius, nonce)**. Client **chains nonces** across servers (`nonce₂ = H(reply₁ ‖ blind)`) so replies are provably ordered; if server B's time precedes A's yet B's reply is provably *after* A's, that is a **cryptographic proof of misbehavior**, third-party-verifiable → revoke the lying key. | **Rough**, not precise (seconds). Needs several independent servers to bound "now." | **STEAL** the **chained-nonce ordering proof** and the **self-incriminating misbehavior artifact**: a Criome time-signature should be over context that provably orders it after a prior event, so a lying signer produces evidence against itself. Also: don't over-claim precision. |
| **KERI witness receipts** [KERI spec] | Witnesses receipt an event (sequence number + prior-event hash give total order within a KEL); a threshold of receipts gives accountable duplicity detection. **KERI deliberately provides ORDER and agreement, not wall-clock time.** | Order is not time. Wall-clock must come from outside. | **STEAL** receipts for consensus **ordering/anchoring**. **NOTE** the sharp lesson: co-signing proves "this happened / a quorum saw it," **not** "now is inside this window" — that requires a per-signer clock check (below). |
| **CT STH timestamps** [RFC 6962/9162] | The STH carries a log-signed timestamp (bounded by max-merge-delay); **witness cosigning** hardens it against a lying/equivocating log. | A single log's timestamp is trust-me; cosigning fixes equivocation but each signer's clock is still its own. | **STEAL** the **cosigned head + timestamp** shape as the "Criome clock" envelope; meaningful only if signers independently check their clocks. |
| **BFT chains (CometBFT `BFT Time`)** [CometBFT spec] | Each validator stamps its **local time** in its precommit; block time = **voting-power-weighted median** of precommit times. Robust as long as >2/3 are honest — a <1/3 minority cannot push the median past the honest range. | Requires each validator to actually stamp its own honest clock; tolerates only <1/3 liars. | **STEAL** the **median/intersection of independently-clocked signer windows** as the robust consensus "now" — this is the most direct blueprint for the Criome clock, and it structurally **requires** the per-signer gate. |

Best-in-class for Q5: **CometBFT BFT-Time (median of signer clocks) + Roughtime
(chained-nonce misbehavior proof)** together. BFT-Time gives the robust
aggregate ("now" = median/intersection of honest signer windows, minority-liar
tolerant); Roughtime gives the artifact that makes a lying signer accountable.
KERI is the cautionary boundary: witness co-signing alone yields **order, not
time**.

Design guidance (this is the load-bearing fix already flagged in Criome's
current-state scout): a co-signed window proves only "a quorum co-signed this
window," **not** "now is inside it," unless **each signer independently consults
its own clock and refuses to time-sign outside `[opens_at, closes_at]`**. Derive
the consensus "now" as the **median / intersection of signer windows**, not the
proposer's asserted window, so a convenient window chosen by a proposer cannot
manufacture time.

## Closest overall system

**KERI is the single closest existing system to Criome's overall design.** It
alone supplies, in one coherent model: (1) a content-addressed, self-certifying
genesis identity that carries its genesis key material (SAID over the inception
event) with **pre-rotation** for key-compromise survival — Q1; (2) **delegated
identifiers with a two-way parent-anchors-child binding** — Criome's parent/child
authority chain, Q2; (3) **KEL replay from genesis + receipts** — verify-by-
ancestor-chain sparse replication including the delegator's anchoring slice, Q4;
and (4) **witness receipts** as the consensus ordering/anchoring layer, part of
Q5. No other single system covers four of the five questions.

What KERI does **not** give Criome, and where to borrow from others: KERI
delegation is **not time-leased** with automatic revert — take that from
**ACME short-lived certs + Vault max_TTL + TUF `expires`** (Q3); KERI uses
per-controller keys + witnesses rather than a **BLS-aggregate threshold** quorum
as the authorizer — Criome keeps its BLS majority; and KERI explicitly gives
**order, not wall-clock time** — take genuine consensus time from
**CometBFT BFT-Time (median of signer clocks) + Roughtime**. Mental model:
**KERI is the skeleton; TUF/ACME/Vault the lease muscle; CometBFT/Roughtime the
clock.**

## Recommended synthesis for Criome

Patterns worth adopting (each phrased as implementer guidance):

1. **Split identity from signatures (KERI SAID / TUF signed|signatures).**
   Content-address the genesis *state incl. the admitting quorum's public-key
   commitment*; carry the BLS admission signatures as **attachments keyed to
   that digest**, never inside the hashed body. Identity exists at submission;
   quorum finalization = accumulating enough attached signatures. Use the
   dummy-placeholder derivation if the digest must appear inside its own object.

2. **Pre-commit the next quorum, and rotate with old+new co-signing
   (KERI pre-rotation + TUF root rotation).** The genesis/root commits to a
   digest of the next quorum's keys; any membership rotation is signed by a
   threshold of **both** the outgoing and incoming quorum, so a node holding the
   old root can always validate forward. This makes root-key compromise
   survivable and rotation verifiable offline.

3. **Two-way parent/child anchoring with an explicit re-grant bit
   (KERI delegation + SPKI delegation bool + TUF scoped threshold).** The child's
   genesis references the parent; the parent contract **anchors the child's
   genesis digest**. Encode the time-lease in that anchor. Carry a delegation
   flag (may the child sub-grant?) and a scope (which subtree it governs) — this
   is where "one subcontract per cluster" lives.

4. **Leased ownership = object-carried `expires` + hard max_TTL, verified
   locally (TUF `expires` + Vault max_TTL + ACME short-lived certs).** The
   child's self-ownership grant *expires by default* and must be renewed;
   "revert to parent on lapse" is implemented as **the stale self-grant failing
   to validate** (a pull/local check), and the "window ⊆ lease" ceiling is
   checked by **every signer before signing**, not only by the judge.

5. **Median/intersection consensus clock with a mandatory per-signer gate
   (CometBFT BFT-Time + Roughtime).** Each signer refuses to time-sign outside
   its own clock's view of the window; consensus "now" is the median/intersection
   of honest signer windows (minority-liar tolerant). Make each time-signature
   cover a nonce/context that provably orders it after a prior event, so a lying
   signer emits a **self-incriminating, third-party-verifiable artifact**.

6. **Cosign the authority/quorum head to kill equivocation, and ship
   ancestor+anchor slices for sparse verify (CT/RFC 9162 + KERI KEL + Merkle-DAG
   sync).** A node holds the object, its contract chain, and each parent's
   anchoring record up to the pre-provisioned root digest; a cosigned head
   prevents a proposer from showing different histories to different signers and
   provides the anti-rollback reference that turns integrity into currency.

Traps to avoid (documented failure modes Criome could walk into):

- **A. Do not hash signatures into the identity.** Criome's "hash carrying its
  own quorum signatures" is chicken-and-egg. Every mature system keeps
  signatures *adjacent* to the digested body. (Fix = pattern 1.)

- **B. Do not treat a co-signed window as proof of "now."** Without a hard
  per-signer clock gate, a proposer picks a convenient window and the quorum
  merely co-signs it — the "clock" is forgeable. This is the exact gap the
  current-state scout flagged (`sign_quorum_vote` time-signs unconditionally).
  KERI (order≠time) and BFT-Time both say the honest per-signer stamp is
  load-bearing. (Fix = pattern 5.)

- **C. Do not implement lease-lapse as active revocation/broadcast.** X.509's
  CRL/OCSP history is the standing warning: external revocation lists go stale,
  soft-fail, and depend on the revoker's availability. Make lapse an **expiry
  that fails to validate locally** (ACME/Vault/TUF model), and make
  window-exceeds-lease a signer-side refusal — otherwise a colluding proposer
  collects partial signatures on an over-long window before the judge ever sees
  it. (Fix = pattern 4; also avoid conflating hash integrity with chain
  completeness — pair the ancestor line with a signed anti-rollback head.)

## Sources

- KERI — Key Event Receipt Infrastructure: [arXiv 1907.02143](https://arxiv.org/abs/1907.02143); [ToIP KERI specification](https://trustoverip.github.io/kswg-keri-specification/); [did:keri method](https://identity.foundation/keri/did_methods/).
- TUF — The Update Framework: [tuf-spec.md](https://github.com/theupdateframework/specification/blob/master/tuf-spec.md); [theupdateframework.io FAQ](https://theupdateframework.io/docs/faq/); [Rugged TUF key rotation](https://rugged.works/background/ceremonies/key-rotation/).
- X.509 / PKIX path validation: [RFC 5280](https://www.rfc-editor.org/rfc/rfc5280).
- Certificate Transparency: [RFC 6962](https://www.rfc-editor.org/rfc/rfc6962); [RFC 9162 (CT v2)](https://www.rfc-editor.org/rfc/rfc9162.html); [Decentralized Witness Cosigning, arXiv 1503.08768](https://arxiv.org/pdf/1503.08768).
- SPKI/SDSI: [RFC 2693, SPKI Certificate Theory](https://www.rfc-editor.org/rfc/rfc2693).
- Macaroons: [Macaroons: Cookies with Contextual Caveats (Google, 2014)](https://research.google.com/pubs/archive/41892.pdf); [libmacaroons](https://github.com/rescrv/libmacaroons).
- Biscuit: [Biscuit specifications](https://doc.biscuitsec.org/reference/specifications.html); [Third-party blocks](https://www.biscuitsec.org/blog/third-party-blocks-why-how-when-who/); [biscuit_auth (Rust)](https://docs.rs/biscuit-auth).
- ACME / short-lived certs: [RFC 8555 (ACME)](https://www.rfc-editor.org/rfc/rfc8555).
- Vault leases: [HashiCorp Vault — Lease, renew, and revoke](https://developer.hashicorp.com/vault/docs/concepts/lease).
- Roughtime: [draft-ietf-ntp-roughtime](https://datatracker.ietf.org/doc/html/draft-ietf-ntp-roughtime-15); [Roughtime at Google](https://roughtime.googlesource.com/roughtime).
- BFT time: [CometBFT / Tendermint BFT Time spec](https://github.com/cometbft/cometbft/blob/main/spec/consensus/bft-time.md).
- Content addressing: [multiformats CID](https://github.com/multiformats/cid); [git object model](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects); [IPLD](https://ipld.io/docs/).
