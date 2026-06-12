# Verifiable and Attestable History for a Typed Event Log: Transparency-Log Merkle Proofs, Witness Quorums, and criome BLS Checkpoints

## Scope and how this extends report 92

Report 92 (`reports/system-designer/92-reusable-versioned-sema-library/`) surveyed the general version-control prior art — Datomic, Dolt/noms, Fossil, Irmin, IPLD, TerminusDB, event-sourcing, WAL-shipping, CRDT/Merkle-CRDT, serialization formats — and converged on "version the log, not the store": a payload-bearing, **blake3** hash-linked, authoritative log with a rebuildable redb view, a typed schema-hash decoder selector, and a first-class checkpoint. It deliberately did **not** cover how to make that log *verifiable to an untrusted peer* or *cryptographically attestable*. The only crypto it touched was naming criome's `ObjectDigest` (blake3) and `BlsPublicKey`/`BlsSignature` as the in-house seeds, and Irmin's "typed Merkle proofs for sync" in passing.

This report fills exactly that gap. The central finding: **our hash-linked log is tamper-evident but not yet efficiently verifiable, and the upgrade that fixes it is small, well-specified, and production-proven.** A plain blake3 hash-chain (entry N commits to entry N−1) lets a holder detect tampering only by re-reading the whole chain — proofs are O(n). The transparency-log world solved this fifteen years ago with the **Merkle history tree** (Crosby-Wallach 2009), which gives O(log n) inclusion *and* consistency proofs over the *same* append-only sequence. Layering a history tree over the log we already have, signing its head with criome BLS, and having ouranos (plus optional witnesses) cosign, is the whole of "verifiable + attestable." Every piece has a shipping reference implementation and a current (2024-2026) standard.

A second-order finding worth stating up front: the entire C2SP transparency-log stack (checkpoint, tile, witness, cosignature) is **format-compatible with our design by accident of convergence** — their "checkpoint" is our `Checkpoint`, their "signed note" is our BLS-signed head, their "witness quorum" is criome's `ComplexQuorum`/`RequiredSignatureThreshold`, their "tile fetch" is our suffix-sync to ouranos. We are not adopting a foreign system; we are re-deriving a standard we can read off the shelf.

## Part 1 — Hash-chain vs. Merkle history tree: the structure that makes a log verifiable

### What a plain hash-chain gives and does not give

Our direction's log entry carries `prev_digest + sequence` (report 92 §1). Chaining `entry_digest = blake3(payload ‖ prev_digest)` makes the log **tamper-evident**: altering entry *k* changes every digest from *k* onward, so any holder of a later digest detects it. This is the same property git commit parents give. But a hash-chain answers only "is this *whole* prefix intact" — to prove entry *k* is in a log whose head you trust, or to prove version *m* of the log is an append-only extension of version *n*, you must replay every intervening entry. Proofs are **O(n)**. That is fine for a single trusted writer auditing itself; it is too weak to let a *remote* (ouranos) or a *peer* (a fork) prove things to us without us re-downloading everything.

### The Merkle history tree (Crosby-Wallach 2009 → RFC 6962)

Crosby and Wallach's **history tree** is a Merkle tree whose leaves are appended left-to-right; it is the exact structure RFC 6962 Certificate Transparency standardized and Trillian/Tessera/Sunlight/Rekor run at internet scale ([Crosby-Wallach via arXiv survey](https://arxiv.org/pdf/2305.01378), [RFC 6962](https://www.rfc-editor.org/rfc/rfc6962.html)). Over the same append-only entry sequence it provides two O(log n) proofs:

- **Inclusion proof** — a sequence of sibling hashes (the `audit_path`) that recombines a single leaf hash up to the signed root at a given tree size. Proves "entry *k* is leaf *k* of the tree whose head you trust" without revealing or transferring the other entries ([RFC 6962](https://www.rfc-editor.org/rfc/rfc6962.html)).
- **Consistency proof** — a logarithmic set of nodes proving tree-at-size-*m* is a strict append-only **extension** of tree-at-size-*n* (every old leaf unchanged, only appends). This is the cryptographic enforcement of append-only: "if a log attempts to show different things to different people, this can be efficiently detected by comparing tree roots and consistency proofs" ([RFC 6962](https://www.rfc-editor.org/rfc/rfc6962.html)).

The leaves are our log entries (the leaf hash = the entry's blake3 digest). The hash-chain and the history tree are **complementary, not redundant**: the chain gives cheap local sequential integrity on every append; the tree gives cheap *remote* inclusion/consistency proofs. Report 92's "digest beside cursor, never as cursor" rule survives intact — `CommitSequence` stays the ordered cursor, the tree's leaf *index* equals the sequence, and the root hash is the new attestable identity layered beside it.

### Why this specifically beats a hash chain for us

The whole point of the ouranos mirror (report 92 §2) is durability without trusting ouranos to be honest about *what* it stored. A hash-chain mirror forces "re-download and replay to verify." A history-tree mirror lets ouranos return, for any entry we ask about, a ~log-sized inclusion proof against a head we already hold; and lets us verify each suffix-ingest is a pure append via one consistency proof. **This is the single most important upgrade in this report**: it is what converts the mirror from "trusted blob store" into "untrusted prover," satisfying the spirit of Spirit `29pb`'s "native VC, not opaque blob" at the *verification* layer, not just the format layer.

## Part 2 — Checkpoints as signed notes, and what to sign

### The checkpoint format is already our Checkpoint

C2SP's [`tlog-checkpoint`](https://github.com/C2SP/C2SP/blob/main/tlog-checkpoint.md) defines a checkpoint as a **signed note** with a three-line body: (1) **origin** — a unique log identity, schema-less-URL-shaped (`example.com/log42`); (2) **tree size** — decimal leaf count; (3) **root hash** — base64 of the RFC 6962 Merkle root at that size. Optional signed timestamp/extension lines may follow but are discouraged because monitors can't audit them. The binding invariant: **"A log MUST NOT sign any checkpoint which is inconsistent with any checkpoint it previously signed"** — monotonic append-only, cryptographically committed.

This *is* report 92's first-class `Checkpoint` (identity, covered range, digests, retained-suffix policy), now given a precise, interoperable, signable body. Map it directly:

- origin → the component's log identity (e.g. `spirit` / per-component per-branch).
- tree size → `CommitSequence` of the covered head (the leaf count).
- root hash → blake3 Merkle root of the history tree at that size.
- our extra checkpoint fields (schema-hash inventory, pruned-head policy) ride as our typed `Checkpoint` record that *embeds* this signed note; we don't have to cram them into the note body.

### What gets BLS-signed — heads, not entries

The clever economy of the transparency-log design: **you sign the tree head (checkpoint), not every entry.** One signature attests an unbounded number of entries, because inclusion proofs chain each entry to the signed root. So the per-write hot path stays cheap (append + hash-chain + tree update, no signature), and signing happens at checkpoint cadence. This fits our constraint that the daemon write path is latency-sensitive: BLS signing — expensive relative to append — lands at checkpoint boundaries, not per commit.

### Post-quantum flag (genuinely state-of-the-art, against BLS)

C2SP `tlog-checkpoint` now says logs **SHOULD use ML-DSA-44** (post-quantum, FIPS 204) cosignatures, with other algorithms permitted ([tlog-checkpoint](https://github.com/C2SP/C2SP/blob/main/tlog-checkpoint.md)). This is the leading edge moving *past* classical signatures for transparency. It is a real tension with our "one consistent crypto basis = blake3 + criome BLS" mandate: BLS12-381 is ~117-120-bit classical security and **not** post-quantum ([eth2book](https://eth2book.info/latest/part2/building_blocks/signatures/), [BLS12-381 explainer](https://hackmd.io/@benjaminion/bls12-381)). For a *trusted-tailnet, single-psyche* threat model the PQ gap is low-urgency, and BLS buys us aggregation/threshold that ML-DSA does not. But this report flags it explicitly: the note format is algorithm-agnostic by design ("clients MUST ignore unknown signatures"), so a future PQ cosignature can be *added* beside the BLS one without reformatting — do not hard-wire BLS into the checkpoint body such that PQ can't be added later.

## Part 3 — Attestation by quorum: witnesses, cosigning, and criome BLS

### The split-view attack and why one signature is not enough

A signed checkpoint proves *the log* vouches for a head. It does **not** stop the log from showing head A to us and a forked head B to a peer — a **split-view (equivocation) attack**. The transparency-log answer is **witness cosigning**: independent witnesses each cosign only checkpoints **consistent with every checkpoint they previously saw for that log**, so a client that requires a *quorum* of witness cosignatures is safe "unless a quorum of witnesses is colluding with the log" ([transparency.dev witness](https://blog.transparency.dev/can-i-get-a-witness-network), [tlog-cosignature](https://github.com/C2SP/C2SP/blob/main/tlog-cosignature.md)).

The protocol ([`tlog-witness`](https://github.com/C2SP/C2SP/blob/main/tlog-witness.md)): the log `POST`s `add-checkpoint` with the old tree size + a consistency proof; the witness checks the old size matches the latest size it cosigned for that origin (or zero), verifies the consistency proof, and on success returns cosignature note lines, else `409 Conflict` with its last-seen size. The cosignature is a `cosignature/v1` signed note with domain separation. This is **append-only enforced by a distributed quorum**, not by trusting the server.

### How criome already gives us the quorum primitives

criome's contract is startlingly well-shaped for this (`signal-criome/src/schema/lib.rs`, verified in-tree):

- `SignatureScheme::Bls12_381MinPk | Bls12_381MinSig` — the curve/variant choice.
- `RequiredSignatureThreshold(Integer)` + `SignatureAuthorizationMode::{SimpleSelfSigned, ComplexQuorum}` — **exactly** the "single-signer vs. quorum" axis a witness network needs.
- `SignatureAuthorizationResult::{SingleSignature, RequiredSignaturesSatisfied, PendingSignatures}` — the witness-quorum state machine (enough cosignatures yet?).
- `SignatureEnvelope { scheme, public_key, signature }`, `Attestation { signer, envelope }`, `SignedObject` — the cosignature carrier.
- `SignatureSolicitation { request_digest, required_signer }` + `SignatureSolicitationRoute` — **the "log asks a witness to cosign" request**, already a contract verb.

So the witness protocol is not a new subsystem to invent: it is `Attestation`s over a `Checkpoint`'s blake3 root digest, gated by `RequiredSignatureThreshold`, resolved through `SignatureSolicitation`. The default mode (`SimpleSelfSigned`) = single-writer self-attested head (today's trust model); `ComplexQuorum` = witness-cosigned head (the hardened model). **This is the per-component policy hook the new psyche requirements ask for, expressed in crypto: each component's checkpoint policy picks `SimpleSelfSigned` or a `ComplexQuorum` threshold.**

### BLS aggregation is the clever fit for quorum checkpoints

Here is the genuinely clever combination. When multiple witnesses cosign **the same checkpoint** (same message = the root hash), BLS lets you **aggregate** all cosignatures into one 96-byte signature verified against one aggregated public key with **~2 pairings total** via `FastAggregateVerify`, regardless of witness count — this is exactly Ethereum's attestation aggregation ([eth2book](https://eth2book.info/latest/part2/building_blocks/signatures/)). A quorum-attested checkpoint is therefore **constant-size and constant-verify-cost no matter how many witnesses**, where Ed25519/ML-DSA cosignatures would be N separate signatures. Since all witnesses sign the *identical* root hash, we are in the cheap same-message regime, not the costlier `AggregateVerify` (n+1 pairings for distinct messages). criome choosing BLS over Ed25519 pays off precisely here.

**Mandatory caveat — the rogue-key attack.** BLS aggregation is insecure against a *rogue public key* attack unless defended: an attacker registers `pk' = [sk']g − pk_victim` and forges a joint signature the victim never made ([Stanford BLS multisig](https://crypto.stanford.edu/~dabo/pubs/papers/BLSmultisig.html), [eth2book](https://eth2book.info/latest/part2/building_blocks/signatures/)). The standard defenses: **proof-of-possession** (each witness signs its own public key at registration, proving it holds the secret) **or** ensuring every signer signs a *distinct* message (e.g. by binding the public key into the message hash). Our checkpoint case is same-message-by-design (all witnesses sign the identical root), so we **must** use the proof-of-possession scheme (`Bls12_381MinPk` with PoP), the same choice Ethereum made. This is a concrete must-implement, not a footnote — getting it wrong silently breaks quorum security.

### Where quorum does NOT fit (rejecting cargo-cult)

Report 92 already rejected multi-target/quorum *ingest* (rqlite/openraft) for our single-trusted-ouranos durability tier. That rejection stands and must not be confused with witness quorum: **durability quorum (do N servers hold the bytes) is different from attestation quorum (do N independent parties vouch the head is consistent).** We reject the former (one trusted ouranos, queue-and-accrue-RPO on outage). We may *optionally* adopt the latter — but for a single-psyche, single-tailnet deployment the split-view threat is low (there is essentially one client and one writer), so `SimpleSelfSigned` is the sane default and `ComplexQuorum` is an opt-in for components/branches that genuinely admit untrusted contributors. Do not build a witness network because the standard has one; build it only where a real second party needs to disbelieve ouranos. Naming this keeps us off the cargo-cult path.

## Part 4 — Efficient verifiable sync: tiles map onto our suffix-shipping

Report 92's backup model is "ship the log suffix since the peer's last head" (§1). The transparency world's current-best serving model — **tile-based logs** (C2SP [`tlog-tiles`](https://github.com/C2SP/C2SP/blob/main/tlog-tiles.md), Tessera, Sunlight, Rekor v2, [transparency.dev](https://transparency.dev/articles/tile-based-logs/)) — is the verifiable version of exactly that, and it is the freshest (2024-2025 GA) state of the art.

A **tile** is a fixed chunk of consecutive Merkle hashes at one tree level. Instead of the server computing each inclusion/consistency proof on request (the old Trillian model), the server publishes **immutable static tiles**, and clients "fetch the tiles they need in parallel and compute and verify proofs themselves" ([transparency.dev](https://transparency.dev/articles/tile-based-logs/)). Because tiles are immutable and static, they are **trivially CDN/cacheable** — Rekor v2's headline win is "fully cacheable, served by a CDN," eliminating the Trillian log-server/signer infrastructure and cutting storage+egress cost ([Rekor v2 GA](https://blog.sigstore.dev/rekor-v2-ga/)).

The mapping onto our design:

- ouranos becomes a **dumb static file server of tiles + the signed checkpoint** — which is *exactly* report 92's "keep ingest a dumb append-of-suffixes endpoint, not a second engine" constraint, now upgraded to also serve verifiability for free. No engine on ouranos; honour no-shared-daemon.
- our suffix-ship = append new entry tiles + publish a new signed checkpoint. A consumer (us re-pulling, or a peer) fetches new tiles, verifies a consistency proof old-head → new-head, and trusts the suffix without re-downloading history.
- Rekor v2's "return the inclusion proof on upload, persist it alongside the artifact" pattern ([Rekor v2 GA](https://blog.sigstore.dev/rekor-v2-ga/)) maps to: when a write commits, capture its inclusion proof against the then-current checkpoint and store it beside the entry, giving **self-contained offline verification** — a record can be proven to have been in the log at a point in time without re-contacting ouranos.

One genuine mismatch to flag: tiles are tuned for *random-access proof serving to many independent clients*. Our dominant case is *one* consumer re-syncing a *contiguous suffix*. For pure tail-append, a raw byte-suffix copy (report 92's Option C) is cheaper than tile-structured fetch. So tiles earn their keep specifically for (a) inclusion proofs of *individual* records, (b) third-party/peer verification, and (c) post-compaction reconciliation — not for the happy-path bulk suffix sync. Adopt tiles for the proof/verification surface; keep the cheap byte-suffix for bulk catch-up. Do not tile-ify everything because the standard does.

## Part 5 — Keyed views and branches: sparse Merkle trees (a narrower fit)

The history tree authenticates the *log* (an append-only sequence). The new psyche requirement for branching/forking/merging will also want to authenticate the *materialized view* — the current key→value map per branch — so a branch head can be proven and two branch states diffed. The transparency world's tool for an authenticated **key-value map with membership *and non-membership* proofs** is the **sparse Merkle tree** (SMT) / Trillian's "verifiable map," as used by CONIKS and key-transparency systems ([efficient SMT, eprint 2016/683](https://eprint.iacr.org/2016/683.pdf), [CONIKS analysis 2024](https://www.mdpi.com/2076-3417/14/21/9725), [Trillian](https://google.github.io/trillian/)). An SMT commits a sparse key→value map to one root; it proves a key maps to a value *or proves a key is absent* in ~constant time.

This is a **real but secondary** fit, and I flag it as such rather than overselling:

- It fits **per-branch view authentication**: a branch's redb view (the materialized state) gets an SMT root; a branch head = (log-history-tree root, view-SMT root) both BLS-signed. Two branches can then be compared by SMT root, and a merge can prove which keys diverged via (non-)membership proofs.
- It is the natural carrier for "prove the current value of record K on branch B without shipping the whole view."
- But it is **not needed for the log-verifiability core** (Parts 1-4), it adds a second authenticated structure to maintain on every commit, and report 92 already rejected prolly-trees as Dolt-cargo-cult for our append-only shape. An SMT is *not* a prolly tree (it's a fixed-depth sparse commitment, not a probabilistically-chunked B-tree), so the rejection doesn't transitively kill it — but the same discipline applies: adopt the SMT only when the branch/merge requirement concretely needs authenticated view diffs, not preemptively. For single-writer, single-branch operation it is pure overhead.

## Part 6 — The clever combination for our case, end to end

Pulling the verified pieces into the one design that is best-of-breed *and* fits our event-log shape, per-component policy, and blake3+BLS basis:

1. Keep the **blake3 hash-chain** on every append (cheap local sequential integrity, free atomicity in the redb txn — report 92's most-valuable property, untouched).
2. Maintain a **Crosby-Wallach Merkle history tree** over the same entries (leaf = entry blake3 digest, leaf index = `CommitSequence`). This is the verifiability engine: O(log n) inclusion + consistency proofs.
3. At checkpoint cadence, emit a **C2SP-shaped signed-note Checkpoint** (origin, tree size, root hash), **BLS-signed** with criome (`Bls12_381MinPk` + proof-of-possession). One signature attests the whole prefix.
4. Per-component **attestation policy** = criome `SignatureAuthorizationMode`: default `SimpleSelfSigned`; opt into `ComplexQuorum` with a `RequiredSignatureThreshold` for components/branches with untrusted contributors. Witness cosignatures **BLS-aggregate** to constant size/verify-cost (`FastAggregateVerify`, same-message regime). This is the crypto expression of the "per-component customizable policy" the psyche asked for, and it composes with the Spirit GUARDIAN example: the guardian is a *content-admission* policy on intake/rebase; the attestation threshold is a *history-integrity* policy on checkpoints — two orthogonal per-component hooks on the same log.
5. **ouranos serves tiles + the signed checkpoint statically** (dumb append endpoint, no engine, CDN-cacheable). Suffix-sync = append tiles + new checkpoint; consumers verify a consistency proof and trust the suffix. Bulk catch-up still uses the cheap byte-suffix; tiles carry the per-record/peer proof surface.
6. Each committed record optionally stores its **inclusion proof against the contemporaneous checkpoint** (Rekor v2 pattern) for self-contained offline "this was in the log at time T" proofs.
7. **One crypto basis, honoured**: blake3 for *all* content addressing (entry digests, Merkle leaves/nodes, checkpoint root); criome BLS for *all* signing/attesting (checkpoint heads, witness cosignatures). No third hash, no per-component divergence. The only forward-looking seam: keep the checkpoint note algorithm-agnostic so a post-quantum (ML-DSA-44) cosignature can be *added beside* BLS later without reformatting.

What is genuinely state-of-the-art (2024-2026) and load-bearing here: **tile-based static logs** (Tessera/Sunlight/Rekor v2 GA), the **C2SP checkpoint/witness/cosignature spec family**, **witness-quorum split-view defense**, and **same-message BLS aggregation with proof-of-possession**. What is old-but-foundational and we'd be foolish to reinvent: the **Crosby-Wallach history tree / RFC 6962 inclusion+consistency proofs**. The clever part is that these slot onto our existing blake3 hash-linked log and criome BLS *with almost no impedance mismatch* — the standard's "checkpoint" is our `Checkpoint`, its "witness quorum" is our `ComplexQuorum`, its "tile suffix" is our suffix-ship. We get untrusted-mirror verifiability and quorum attestation essentially by *naming* what the transparency-log world already standardized, rather than inventing.

