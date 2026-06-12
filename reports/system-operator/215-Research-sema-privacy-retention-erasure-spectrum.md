---
title: 215 - SEMA privacy, retention, and erasure spectrum
role: system-operator
variant: Research
date: 2026-06-12
topics: [sema, privacy, retention, erasure, versioned-state]
description: |
  Research spectrum for resolving the tension between append-only verifiable
  SEMA history and erasable private or Spirit-class state. It compares
  never-GC, zero-knowledge ciphertext mirrors, cryptographic erasure,
  commitment-only mirrors, retention-window pruning, redactable logs, and
  no-durable-log modes, then recommends a per-store privacy/retention matrix.
---

# 215 - SEMA privacy, retention, and erasure spectrum

## Intent Anchors

[Private information is closed by default.]

[When a Spirit record moves into the archive its privacy variable moves with it and is preserved; archive reads honor the same explicit privacy discipline as the live store.]

[The version-control and backup system should use one consistent cryptographic basis: blake3 for content addressing and criome BLS for signing and attesting history.]

[The current SEMA version-control implementation home is `sema-engine`; future extraction is possible only after the engine nouns settle.]

## Question

System-designer report 95 originally treated ouranos as an append-only mirror
that never garbage-collects. Report 214 pushed back: that is right for public
coordination stores, but private and Spirit-class stores need real deletion,
retention, pruning, and right-to-erase semantics. The decision question is:

Should the remote mirror keep every payload forever for the strongest backup
story, or should SEMA introduce erasable-private history while preserving
verifiable append-only structure?

The answer should not be one global mode. The best shape is a per-store and
per-family privacy/retention matrix, with public history allowed to be
permanent, ordinary private history mirrored as zero-knowledge ciphertext, and
existence-private state routed away from durable versioning entirely.

This report also reads SD's newer
`reports/system-designer/95-versioned-state-grand-design/11-privacy-retention-erasure-deep-design.md`.
That report makes two important corrections which I accept: commit over
ciphertext, never plaintext; and distinguish content-erasure from
existence-erasure. Content can be erased while the log skeleton remains.
Existence cannot be made forgettable while preserving durable verifiable
history.

## Research Baseline

### What the outside world says

The legal and standards prior art does not endorse "encrypted forever" as a
universal privacy answer.

GDPR Article 17 establishes erasure rights, while Article 5's storage-limitation
principle says personal data should be kept in identifiable form only as long as
needed for its stated purpose. The right is not absolute, but it is real enough
that an architecture which makes erasure impossible is choosing a regulatory and
ethical position, not merely a storage format.

The EDPB's 2025 blockchain guidelines are directly relevant because blockchains
share our hard property: replicated append-only history. Their baseline is to
avoid storing personal data in an immutable chain when avoidable, and they warn
that hashing or encryption does not automatically remove data-protection duties.
They prefer off-chain personal data with only commitments, hashes, or pointers on
chain when that still meets the use case.

CNIL's blockchain guidance makes a similar practical distinction: if data must
be anchored in an immutable structure, prefer commitments, keyed hashes, or
ciphertext over raw personal data, and keep the underlying personal data outside
the immutable substrate where erasure can operate.

NIST SP 800-88 Rev. 2 is the sanitization baseline for cryptographic erasure:
destroying all keys can sanitize encrypted data, but only if encryption was
strong, keys were actually the only route to the plaintext, and all key copies,
escrow copies, derived keys, and backup keys are covered. Crypto-erasure is a
key-management protocol, not a flag on a blob.

Transparency logs give the other half of the problem. RFC 9162 and the
Certificate Transparency lineage show how append-only Merkle trees prove
inclusion and consistency. They protect history integrity, but they deliberately
do not solve deletion. That is why SEMA has to separate "the verifiable skeleton"
from "the recoverable private content."

Redactable-blockchain research exists, usually using chameleon hashes or
trapdoor-based redaction. It is technically interesting but a poor default for
SEMA: it introduces a new trust/trapdoor role, conflicts with the psyche's
blake3 content-addressing direction, and makes the audit story harder. It belongs
only as a rejected edge option unless a future requirement explicitly demands
authorized mutation of old log leaves.

### What this means for SEMA

Append-only verifiability and erasable payloads are compatible only if they are
not the same thing.

The append-only layer should keep the public skeleton: sequence, parents,
branch-frontier relation, entry digest, ciphertext or commitment digest, policy
verdicts, erasure receipts, checkpoint roots, and BLS signatures.

The erasable layer should hold private recoverability: plaintext-bearing
payloads, plaintext-derived state digests, per-record keys, checkpoint segment
payloads, and any metadata specific enough to identify private content.

Once that split exists, "purge" can mean: the Merkle/DAG skeleton remains
verifiable, but the private payload becomes unrecoverable and the current
materialized state contains an explicit erased/tombstoned value. That matches
Spirit's lifecycle ladder: recoverable until Purge, then irreversible.

The sharper SD 95/11 form is better than "GC the private mirror": for ordinary
private data, ouranos can still be append-only and never-GC if it only keeps
semantically secure ciphertext or commitments and never receives the keys.
Erasure is key destruction in a mutable local/criome keystore. Mirror deletion
is then optional defense-in-depth, not the primary privacy mechanism.

## The Spectrum

### Option 0 - Global never-GC plaintext append-only mirror

Everything goes to ouranos and stays forever, with payloads readable by any
authorized mirror restore.

This is the strongest backup and time-travel story and the simplest proof
model. It is acceptable for public coordination stores, public build/provenance
logs, repository-ledger public events, and other non-private data.

It is unacceptable as the default for private or Spirit-class stores. It turns
Purge into a UI fiction, makes privacy-class movement ineffective once mirrored,
and puts the system in the same immutable-ledger privacy trap the blockchain
guidance warns about.

Verdict: keep as the `PublicPermanent` class only.

### Option 1 - Zero-knowledge ciphertext mirror with crypto-shredding

The log leaf stores ciphertext and public verification metadata. Each private
payload is encrypted under an entry data-encryption key, which is wrapped under a
store, family, record, subject, class, or epoch key. Erasure destroys the
relevant wrapping key or entry key. The Merkle leaf and BLS-signed checkpoint
remain valid; restore of the erased entry yields an `Erased` marker rather than
the old value.

This is SD's recommendation in its strongest form. Its strength is that backup
and append-only proofs remain intact. It also composes naturally with remote
suffix shipping: ouranos can verify hash continuity and signed heads without
decrypting private payloads. In this mode, "ouranos never-GC" can remain true
for ordinary private data because ouranos holds ciphertext, not recoverable
content.

The weakness is that crypto-shredding is only as real as the key lifecycle.
Every key copy, local cache, outbox retry buffer, checkpoint segment, mirror
replica, backup, crash dump, and debugging export must obey the same destruction
rule. A per-store key is too coarse because deleting one record would erase the
whole store; a per-entry key is maximally granular but operationally noisy. The
best practical hierarchy is usually entry DEKs wrapped by record/subject/class
or epoch KEKs, with explicit erasure receipts. Key custody should likely live in
criome, but that becomes a new secrets-management capability, not reuse of the
current BLS vocabulary.

Verdict: best default for private stores that still need remote restore before
purge.

### Option 2 - Commitment-only remote mirror with local encrypted payloads

ouranos stores the append-only skeleton, signed heads, proofs, and a commitment
to the payload, but not the payload ciphertext itself. The actual encrypted
payload remains on the component host or a narrower private backup target.

This follows the EDPB/CNIL off-chain pattern most closely. It sharply reduces
remote privacy exposure because the mirror can prove history shape without
having recoverable content. It is good for high-privacy Spirit-class data when
the goal is "remote witness plus local restore," not "remote full backup."

The cost is obvious: ouranos alone cannot restore the erased or unavailable
payload. The restore story needs a second, more private backup path or accepts
that some stores have verification without remote recoverability.

Verdict: best high-privacy mode when proof matters more than remote full
restore, or when even durable ciphertext on ouranos feels too exposed.

### Option 3 - Retention-window append-only segments

Private logs are append-only within a retention window. After the window closes,
the system emits a signed checkpoint and prunes old segments, keeping only
checkpoint state, tombstones, erasure receipts, and enough Merkle consistency
information to prove the retained history. Payloads and old per-entry proof
tiles disappear physically as well as cryptographically.

This is stronger operational hygiene than crypto-shredding alone because old
ciphertext does not accumulate forever. It is good for high-churn private stores
and for logs where historical replay past a fixed horizon is not worth the
storage or residual-risk cost.

The cost is that old branch bases and cross-schema merges become constrained:
live branch bases must pin the segments they need, or the checkpoint must carry
an encrypted base-state snapshot. Report 95 already identified this compaction
floor; retention policy has to make it privacy-class aware.

Verdict: useful complement for private/high-churn stores, but not the first
mechanism and not required for content-erasure. Build after checkpoint payload
and restore witnesses exist.

### Option 4 - No durable log for existence-private material

For the highest privacy class, the existence and timing of the record is itself
private. Crypto-shredding does not solve that: after key deletion, the log still
shows that an encrypted thing existed at sequence N and was erased at sequence
M. The only clean existence-erasure mode is to avoid durable versioning for that
material.

This gives the strongest forgettability. It also explicitly gives up the SEMA
version-control promise for that class: no branchable remote suffix, no
permanent inclusion proof, no remote full restore. That is not a failure if the
privacy class chose it knowingly.

Verdict: the right answer for maximum/existence-private material. Make it a
class, not an accident.

### Option 5 - Redactable log via chameleon hashes or authorized mutation

Old log leaves can be rewritten while preserving a higher-level digest, usually
because a trusted party holds a redaction trapdoor. This appears in redactable
blockchain literature as a GDPR/right-to-erasure response.

The tradeoff is bad for SEMA. It adds a new crypto primitive, a new redaction
authority, and a trapdoor that is more dangerous than the content keys it would
replace. It also fights the "one content-addressing basis" direction: blake3
digests should mean content identity, not "content unless the trapdoor holder
rewrote it."

Verdict: reject for the default architecture. It is the wrong way to get
existence-erasure because it weakens exactly the tamper-evidence SEMA is trying
to build.

### Option 6 - Hard-deletable/rewriteable private mirror

Private payloads are mirrored, but the mirror is allowed to physically
delete/rewrite private segments under a signed deletion receipt. The current
branch state remains valid, but old inclusion proofs for deleted leaves may
become non-answerable or answer only with a redaction receipt.

This is weaker than zero-knowledge ciphertext plus key-shred for content-erasure
because it asks the mirror to delete correctly and weakens append-only proof
availability. It can reduce residual ciphertext accumulation, but it should be a
retention/compaction tactic, not the primary privacy model.

Verdict: not the default. Prefer key-shred first, physical prune later.

## Recommended Policy Matrix

| Class | Examples | Remote payload | Retention | Erasure action | Verifiability after erase |
|---|---|---|---|---|---|
| `PublicPermanent` | public coordination, public repository-ledger events, non-private provenance | plaintext or ordinary payload | never-GC | tombstone only when domain wants it | full inclusion, consistency, and restore |
| `PrivateDurable` | ordinary private component state | zero-knowledge ciphertext on ouranos | mirror may never-GC; keys are class-retained | crypto-shred keys; signed erasure receipt by default | full skeleton/proofs over ciphertext; content unavailable |
| `SpiritPrivate` | private/elevated Spirit-class records | ciphertext by default; commitment-only by family when needed | privacy magnitude maps to key and payload retention | record/subject key destruction; optional physical prune at compaction | append skeleton remains; restore yields `Erased` or policy tombstone |
| `HighPrivacyWitnessed` | proof-needed but not remote-full-restore state | commitment-only remote; payload on narrower backup | short or explicit | destroy local payload keys and delete local encrypted blobs | remote proves event existence/ordering but cannot restore content |
| `ExistencePrivate` | maximum class where existence/timing is private | no durable log, or only coarse aggregate signal | local policy only | hard delete/local key destruction | verifiable durable history is intentionally forgone |

This matrix is the best answer to SD's escalation: yes, use crypto-shredding
for content-erasure, but make existence-erasure a separate class that does not
durably log. The system should not pretend one mechanism solves both.

## Design Rules For `sema-engine`

Do not hash private plaintext into public durable identifiers. For private
entries, Merkle leaves should commit to the encrypted envelope or a keyed
commitment, not a raw plaintext digest. Plaintext state digests may exist, but
they need the same privacy class as the payload or must be replaced with
post-erasure state digests after purge.

Do not treat blake3 as encryption. The consistent crypto mandate means blake3
for content addressing and keyed commitments, plus criome BLS for signed heads
and checkpoints. Erasable payloads need one chosen AEAD/key-management profile
across SEMA. The exact AEAD can be selected later, but it must not vary by
component.

Make the mirror zero-knowledge by default for private classes. ouranos should
verify continuity, inclusion, consistency, expected heads, and BLS signatures
over ciphertext/commitments. It should not receive decrypting keys.

Make the guardian the classifier. Spirit already has a `Privacy` magnitude and
an `UnclearPrivacy` rejection reason; that is the natural input to
`DurabilityClass` selection. The same `IntakePolicy` path that admits an entry
should choose whether it is public permanent, private durable, witnessed-only,
or existence-private.

Model erasure as an entry, not a side effect. A purge should append a typed
`ErasureReceipt` or equivalent that names the affected entry/record range,
privacy class, key scope, actor authority, policy identity, deletion time, and
resulting branch/checkpoint root. The receipt must avoid re-identifying the
erased content.

Model deniable erasure as a different class, not a hidden flag. If the fact and
timing of erasure are themselves private, an `ErasureReceipt` is the wrong
artifact; the entry should never have entered durable versioned history.

Apply erasure to checkpoint payloads too. A checkpoint segment is just another
payload store; if it contains private records, it must be encrypted under the
same key hierarchy or excluded from the remote payload mode.

Separate backup mirror from semantic peer. A dumb ouranos mirror validates
hashes, signatures, expected heads, retention authorization, and deletion
receipts. It does not run Spirit's guardian. A semantic import into a component
branch runs `IntakePolicy`.

Treat branch/frontier reachability and privacy retention as different roots.
Branch heads are GC roots for ordinary content. A privacy purge can override
historical recoverability across all branches by destroying keys, while leaving
the branch skeleton and erasure receipt intact. Otherwise an old fork becomes a
privacy bypass.

Make retention class part of the store schema identity or policy identity. A
branch from a `PublicPermanent` store into a `SpiritPrivate` store is not a
format-only change; it changes what old entries mean and what the remote is
allowed to retain.

No untracked key escapes. Outbox rows, retry queues, debug logs, crash reports,
temporary migration branches, and local agent work products must never hold
decrypted private payloads beyond their policy window. Crypto-shredding fails if
keys or plaintext leak into ordinary operational surfaces.

Treat key backup as the central hard problem. Backing up keys preserves data but
can defeat erasure; destroying keys enables erasure but risks accidental data
loss. A criome-custodied keystore under a psyche-held root or hardware secret is
the plausible shape, but it is a separate secrets-management design, not a
detail to hide inside the mirror.

## Best Current Direction

Adopt SD 95/11's stronger direction:

1. `PublicPermanent` stores may be append-only and never-GC on ouranos.
2. Private and Spirit-class stores use encrypt-then-commit-over-ciphertext by
   default; ouranos can still never-GC because it is zero-knowledge.
3. `Purge` in a private durable class means key destruction plus an accountable
   typed erasure receipt; physical pruning can follow later.
4. Existence-private material does not enter durable versioned history. That is
   the only honest way to make existence and timing forgettable.
5. High-privacy families can choose commitment-only remote mode, where ouranos
   witnesses history but does not hold recoverable payload ciphertext.
6. Retention-window segment pruning is a second-stage compaction/storage hygiene
   mechanism after checkpoint payload and restore/import are proven.
7. Redactable/chameleon-hash logs are rejected unless a future requirement
   explicitly chooses a redaction authority.

In one sentence: keep the append-only signed skeleton forever where that is
safe; make private content recoverability explicitly finite; route
existence-private state outside durable versioning.

## Implementation Consequences

The next `sema-engine` design slice should add policy nouns before remote code
hardens:

- `PrivacyClass`
- `DurabilityClass`
- `RetentionPolicy`
- `RemotePayloadMode`
- `KeyScope`
- `ErasureMode`
- `ErasureVisibility`
- `ErasureReceipt`
- `PayloadEnvelope`
- `KeyCustodyPolicy`
- `CheckpointPayloadClass`

The first implementation does not need all storage modes. It should at least
make the policy explicit in the log format so today's public permanent mirror
does not become tomorrow's accidental private-data trap.

The first private-capable implementation should choose one narrow path:
zero-knowledge encrypted payload on ouranos with crypto-shredding receipts.
Commitment-only remote, existence-private routing, and retention-window pruning
can follow once restore/import, checkpoint segments, and key custody are stable.

## Sources

- GDPR Article 17 right to erasure: https://gdpr-info.eu/art-17-gdpr/
- GDPR Article 5 storage limitation principle: https://gdpr-info.eu/art-5-gdpr/
- EDPB Guidelines 02/2025 on processing personal data through blockchain technologies: https://www.edpb.europa.eu/system/files/2025-04/edpb_guidelines_202502_blockchain_en.pdf
- CNIL, Blockchain and the GDPR: https://www.cnil.fr/sites/default/files/atoms/files/blockchain_en.pdf
- NIST SP 800-88 Rev. 2, Guidelines for Media Sanitization: https://csrc.nist.gov/pubs/sp/800/88/r2/final
- RFC 9162, Certificate Transparency Version 2.0: https://www.rfc-editor.org/rfc/rfc9162.html
- C2SP transparency log checkpoint envelope: https://github.com/C2SP/C2SP/blob/main/tlog-checkpoint.md
- Redactable blockchain survey/example research: https://arxiv.org/html/2508.08898v1
- SD report 95/11, privacy/retention/erasure deep design:
  `reports/system-designer/95-versioned-state-grand-design/11-privacy-retention-erasure-deep-design.md`
