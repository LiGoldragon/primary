# Capability-Based Encrypted Storage as the Rigorous Form of Key-Gated Access: Tahoe-LAFS, Cryptree, KBFS, and Matrix Megolm Mapped to Sema's Per-Store Recipient Sets

## Why these four systems, and what they answer for Sema

The psyche's GoPass mental model — a store is a versioned log encrypted to a recipient set; a daemon decrypts the stores whose keys it holds; the view is the union of decryptable stores; queries fan out — is the *informal* version of a body of work that already solved the hard parts rigorously. Four systems form the canon, and each contributes a distinct mechanism Sema needs:

- **Tahoe-LAFS** — the *capability* discipline: a single opaque string is simultaneously the key material AND the access right, and read/write/verify are a one-way diminishing chain. This is the cleanest answer to "the per-store key is both the access boundary AND the crypto-shred unit."
- **Cryptree** — *subtree key derivation*: one key unlocks a whole subtree in constant time via one-way functions, and lazy revocation. This is the answer to per-store-vs-per-record granularity and to "grant a federation member a region, not a flat list."
- **Keybase/KBFS** — *generational per-team keys (PTK)* with a signed key history (sigchain): the production-grade pattern for recipient-set membership, lazy rotation, and per-application sub-keys derived from one team seed. This is the closest 1:1 to "a store encrypted to a set of recipient keys, custodied centrally."
- **Matrix/Megolm** — the *group-ratchet* and its documented *failures*: where forward secrecy and post-compromise security actually live (and don't) when many readers share one symmetric key. This is the cautionary half — it tells Sema which guarantees a recipient-set-per-store model can and cannot offer.

## Tahoe-LAFS: the capability IS the key, and diminishing is one-way

Tahoe's model is the rigorous core of what the psyche is proposing. A **capability** is an opaque cryptographic string that is at once the locator, the decryption key, and the authorization — "provider-independent security": the server is assumed malicious and the cap alone gates access ([Capabilities wiki](https://tahoe-lafs.org/trac/tahoe-lafs/wiki/Capabilities), [Tor blog](https://blog.torproject.org/tor-heart-tahoe-lafs/)).

Three (really four) cap classes form a **one-way diminishing chain**:

```
write-cap → read-cap → verify-cap   (repair-cap is a side branch)
```

You can compute a weaker cap from a stronger one but never the reverse — "deriving a weaker capability from a strong one is called *diminishing*." The **read-cap contains the AES key** ("confidentiality: the promise that nobody who doesn't know the read-cap can see the plaintext"); the **verify-cap** is "the weakest capability that still allows every bit of every share to be validated (hashes checked, signatures verified)" — i.e. a third party can repair/audit integrity *without* read access. Immutable files use `URI:CHK:` where the read-cap embeds a content hash; mutable files/dirs use `URI:SSK:`/`URI:DIR2:` with an RSA write key ([Capabilities](https://tahoe-lafs.org/trac/tahoe-lafs/wiki/Capabilities), [Capabilities search summary](https://grokipedia.com/page/Tahoe-LAFS)).

**The verify-cap is the single most important idea for Sema.** It is exactly the separation we already have between "the log commits over ciphertext" and "private payloads are AEAD-encrypted." A verify-cap is what ouranos (the zero-knowledge append-only server) and a BLS-checkpoint auditor *need and only need*: the power to validate every hash/signature in the log without ever decrypting a payload. Sema's blake3-hash-linked log over ciphertext already produces a natural verify-capability (the hash chain) distinct from the read-capability (the AEAD key). Name them as such.

### Cross-store references across the encryption boundary — Tahoe already solved this

Sema worries about "cross-store REFERENCES / referential integrity across encryption boundaries." Tahoe's **directory nodes** are the canonical answer ([dirnodes spec](https://tahoe-lafs.readthedocs.io/en/latest/specifications/dirnodes.html)). Each child entry is `(name, rocap, rwcap, metadata)`: the **read-only cap sits in the clear-to-readers slot, and the read-write cap is separately encrypted** with "AES-CTR using a key formed from a tagged hash of the IV and the dirnode's writekey." This gives **transitive read-only-ness**: a holder of a read-only parent automatically gets read-only access to all children and *cannot* amplify to write, because they can't decrypt the rwcap slot. This is precisely how Sema can store a reference from store A to a record in store B: hold the *verify-cap or read-cap* of B inline (so referential integrity / hash-validation survives even for instances that can't decrypt B), and gate the write/decrypt power behind a separately-wrapped key. References never leak the stronger capability.

## Cryptree: one key for a whole subtree, and lazy revocation

Cryptree ([ETH paper PDF](https://tik-db.ee.ethz.ch/file/146566189b90f952b8ab1dcf98010781/), [slides](https://slidetodoc.com/cryptree-a-folder-tree-structure-for-cryptographic-file/), [ScienceDirect, Akl-Taylor lineage](https://www.sciencedirect.com/science/article/abs/pii/0020019088900993)) addresses the granularity question head-on. Each folder carries several keys — **data key** (encrypts contents), **backlink key** (upward traversal), **subfolder key** (derives child folder keys), **clearance key** ("revealed to grant access"), **folder-name key**. Subtree keys are derived from a parent key "by iterative application of one-way functions," so **granting one clearance key gives recursive access to the entire subtree in constant time** — avoiding the CACL blow-up where "u users × f files" needs u·f ACL entries.

Two link types matter for Sema's federation:
- **Symmetric link** — "requires knowledge of K₁ to derive and update K₂"; cheap, but the parent can always reach the child.
- **Asymmetric (forward/backward) link** — "K₂ can be replaced without knowing K₁"; lets you re-key a child or sever a relationship without holding the parent secret.

Revocation is **lazy**: "when someone loses read access, the involved items need to be re-encrypted" — but only upon next modification, deferring expensive bulk re-keying.

For Sema this validates a **two-tier key scheme inside the federation**: a store's recipient-set key (the access+shred unit the psyche wants) can itself be a Cryptree-style node, so a single granted key can open a *region* of related stores (e.g. a privacy tier, or a project subtree) without enumerating every store. It also tells us the honest cost: derivation-tree access means a parent key compromise exposes the whole subtree — choose asymmetric links wherever a child must be re-keyable independently of its parent.

## Keybase/KBFS: generational per-team keys with a signed history — the closest production analog

KBFS is the system whose data model is nearest to "a store encrypted to a set of recipient keys, with a custodian managing the keys" — and criome plays the role Keybase's team/sigchain plays ([team crypto spec](https://book.keybase.io/docs/teams/crypto), [KBFS understanding](https://keybase.io/docs/kbfs/understanding_kbfs), [KBFS crypto](https://book.keybase.io/docs/crypto/kbfs)).

A team generation starts from a **32-byte random seed `s`**; from it three keys derive via `HMAC(s, label)`:
```
EdDSA signing   = HMAC(s, "Keybase-Derived-Team-NaCl-EdDSA-1")
Curve25519 DH   = HMAC(s, "Keybase-Derived-Team-NaCl-DH-1")
SecretBox sym   = HMAC(s, "Keybase-Derived-Team-NaCl-SecretBox-1")
```
The **public halves are signed into the team's append-only sigchain**; the seed is then **encrypted to each member's per-user-key**. Per-application keys derive from the generation seed XORed with a **server-held mask**:
```
KBFS key = HMAC(s_i, "Keybase-Derived-Team-KBFS-1") ⊕ S_{i,KBFS}
chat key = HMAC(s_i, "Keybase-Derived-Team-Chat-1") ⊕ S_{i,CHAT}
```
The mask lets the server **withhold an application's key from implicit admins** — fine-grained access derived from one root, with a server-side gate. **Rotation** ("Per-Team-Key rotation") triggers on member removal, device revoke, or account reset; it is **lazy**, mints a *new generation*, encrypts the new seed to remaining members, and **writes new public halves into the sigchain** — but "old data isn't re-encrypted." Revoked devices are simply not served the new generation by the server.

Three direct lessons for Sema:
1. **Generational keys with a signed history** map onto our BLS-signed checkpoints: a "store generation" is created at each recipient-set change, the generation's public attestation goes on the (BLS) signed chain, and criome custodies/distributes the per-generation seed exactly as Keybase distributes seeds to per-user keys — replace NaCl/EdDSA with our blake3+BLS basis.
2. **Per-application sub-keys from one seed** (KBFS vs chat) is the pattern for deriving a store's read-key vs verify-key vs schema-key from one generation seed, rather than minting independent keys.
3. **The server-held mask** is a real second factor worth considering for criome: it makes "the ciphertext is mirrored to ouranos" insufficient on its own to read — you also need criome's mask — without burdening the recipient set.

## Matrix/Megolm: the cautionary half — what a shared symmetric key cannot give you

Megolm is the closest thing to "many readers share one symmetric key over an append-only stream," so its *limits* bound what Sema's recipient-set model can promise ([megolm spec](https://spec.matrix.org/unstable/olm-megolm/megolm/), [megolm.md](https://gitlab.matrix.org/matrix-org/olm/blob/master/docs/megolm.md), [E2EE guide](https://matrix.org/docs/matrix-concepts/end-to-end-encryption/)).

A sender creates an **outbound Megolm session** (counter + Ed25519 keypair + a 4×256-bit ratchet) and **shares the session key to each recipient device over Olm 1:1 channels**. The ratchet advances by a hierarchical hash (reseeding every 2⁸/2¹⁶/2²⁴ steps) giving *partial forward secrecy* — but with the documented catch: **"a device that obtained the starting Megolm key can decrypt everything encrypted in that session,"** and "if a ratchet value is compromised, an attacker can decrypt all subsequent messages." So:

- **Forward secrecy is per-session only.** A session lives until a rotation boundary — by default "100 messages, one week, or a membership change." The client "should invalidate the outbound session when a member leaves so a new session is used next time."
- **Membership change ⇒ new session.** Removing a reader forces a fresh independent session keyed only to remaining members — but only protects *future* messages.
- **No historical access for new joiners** unless explicitly handed an earlier session key. New members "receive only the current ratchet state."
- **Post-compromise security is weak**: formal analysis ([Device-Oriented Group Messaging, IACR 2023/1300](https://eprint.iacr.org/2023/1300.pdf); [Matrix formal analysis, arXiv 2408.12743](https://arxiv.org/html/2408.12743v2); [Nebuchadnezzar attacks](https://nebuchadnezzar-megolm.github.io/)) finds Megolm's PCS "significantly weaker than Sender Keys" — one compromised session key exposes the rest of the session.

The lesson is the **revocation-vs-erasure distinction the psyche already named, made precise**: in every shared-symmetric-key system (Megolm, gopass, KBFS, Cryptree-lazy), *removing a recipient only re-keys forward.* It never reaches data the removed reader already cached. This is identical across gopass ("re-encrypt for remaining recipients," but the old ciphertext+key pair is already in their hands — [gopass features](https://github.com/gopasspw/gopass/blob/master/docs/features.md), [gopass faq](https://github.com/gopasspw/gopass/blob/master/docs/faq.md)) and KBFS ("old data isn't re-encrypted"). **Therefore Sema's crypto-shred (destroy the key, ciphertext becomes noise) is a strictly stronger and different operation than recipient removal — and only crypto-shred is erasure.** Revocation = mint a new generation forward; erasure = destroy the generation key so even cached ciphertext dies. Keep them as two separate verbs in the design.

## How this lands on the GoPass→Sema mapping

The psyche's mapping is sound and matches prior art, with three sharpenings the canon forces:
1. **A store's key is three capabilities, not one** (Tahoe): read-cap (AEAD key), verify-cap (the blake3 hash chain — what ouranos and checkpoint auditors get), and write-cap (append authority). They diminish one-way. Crypto-shred destroys the read-cap; the verify-cap can survive for integrity audit of a tombstoned store.
2. **Recipient-set membership is generational and signed** (KBFS): each recipient change mints a new generation whose attestation lands on the BLS checkpoint chain; criome custodies and distributes the per-generation seed. Lazy rotation; old generations are not re-encrypted but become unreadable to removed members *for new writes only*.
3. **Subtree granting is available without per-store enumeration** (Cryptree): a recipient-set key can be a node in a derivation tree, so one grant opens a privacy tier or project region in constant time — at the honest cost that subtree compromise is transitive.

## Citations index

[Tahoe Capabilities](https://tahoe-lafs.org/trac/tahoe-lafs/wiki/Capabilities) · [Tahoe dirnodes](https://tahoe-lafs.readthedocs.io/en/latest/specifications/dirnodes.html) · [Tor on Tahoe](https://blog.torproject.org/tor-heart-tahoe-lafs/) · [Cryptree ETH PDF](https://tik-db.ee.ethz.ch/file/146566189b90f952b8ab1dcf98010781/) · [Cryptree slides](https://slidetodoc.com/cryptree-a-folder-tree-structure-for-cryptographic-file/) · [Akl-Taylor key hierarchy](https://www.sciencedirect.com/science/article/abs/pii/0020019088900993) · [KBFS team crypto](https://book.keybase.io/docs/teams/crypto) · [KBFS crypto spec](https://book.keybase.io/docs/crypto/kbfs) · [Megolm spec](https://spec.matrix.org/unstable/olm-megolm/megolm/) · [Megolm doc](https://gitlab.matrix.org/matrix-org/olm/blob/master/docs/megolm.md) · [Device-Oriented Group Messaging](https://eprint.iacr.org/2023/1300.pdf) · [Matrix formal analysis](https://arxiv.org/html/2408.12743v2) · [Nebuchadnezzar](https://nebuchadnezzar-megolm.github.io/) · [gopass features](https://github.com/gopasspw/gopass/blob/master/docs/features.md)
