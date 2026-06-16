# 114 — criome real BLS sign/verify: designer implementation

*The psyche asked to resume the criome work and finish the implementation. This
records the designer implementation that retires criome's placeholder signature and
makes the daemon authenticate for real — the crypto core of `primary-kr40` and the
foundation of the spirit auth pilot (`primary-5zur`). Code on the feature branch
`criome-auth-pilot` (worktree `~/wt/github.com/LiGoldragon/criome/criome-auth-pilot`),
two commits on top of `main` `2a02cf4d`. Local branch; not pushed — operator
integrates from the bookmark.*

## What was broken

Report 112/113 found criome's crypto core was a skeleton: `AttestationSigner::sign`
emitted the literal string `criome-skeleton-bls-signature`; `AttestationVerifier`
returned `InvalidSignature` on the otherwise-valid branch; `blst` was a declared but
unused dependency. So nothing was actually authenticated.

## What this implements

**`src/master_key.rs` — the crypto core (commit 1).**

- `MasterKey` holds the `blst` min-pk `SecretKey`. Methods: `generate` (32 bytes of
  OS entropy from `/dev/urandom`, `SecretKey::key_gen`), `load_or_generate`
  (persist `0600` on first run — the psyche's transitional key-custody choice,
  Spirit `psc6`), `public_key`/`fingerprint`, and `sign`. The secret never crosses a
  wire boundary.
- `VerifyBls` is a trait on the wire `BlsPublicKey` (the public key is the noun that
  verifies) doing real `blst` verification.
- `Hexadecimal` carries the bytes↔wire-string encoding (the `signal-criome` key/sig
  newtypes are `String`-typed).
- Four unit tests: round-trip, tamper, wrong-key, persisted-reload-with-0600.

**The actor integration (commit 2).**

- `AttestationPreimage` (borrowed `&ContentReference` + `&AuditContext`) is the
  canonical byte preimage the signature covers: the per-operation content digest
  (decision C) bound with the audit-context caller origin (decision A), length-
  delimited and purpose-tagged. Signer and verifier build the identical preimage.
- **Signer**: gates on the requester being a known active identity, then signs **as
  criome** with the master key — the self-owned model the registry forces (it stores
  only public keys, so criome can sign only with its own master secret). The
  attestation's `signer` is criome's `Host` identity; the caller lives in
  `audit_context`. Envelope carries the master public key + the real signature.
- **Verifier**: rebuilds the preimage from the attestation and does real
  `verify_bls`, returning `Valid` / `InvalidSignature`. The prior checks (content
  match, known signer, revocation, registered-key match) stay.
- **`CriomeRoot::on_start`**: derives the master-key path from the store location,
  `load_or_generate`s the key, and registers criome's own `Host("criome")` identity
  with the master public key (purpose `CriomeRoot`) so verification can resolve the
  signer — then passes the key + identity to the signer. No `RootArguments`
  signature change, so existing tests' construction is untouched.

## How it honours the disciplines

"Criome verifies; Persona decides" — criome signs/validates exact bytes; semantic
policy stays elsewhere. Out-of-band — the attestation is the separate record it
always was; no proof embeds in content. Per-exact-request — the preimage binds the
exact content + caller + purpose, and a purpose tag stops cross-purpose replay.
Rust discipline — methods on data-bearing types (`MasterKey`, `Hexadecimal`,
`AttestationPreimage`), traits on the real nouns (`VerifyBls` on `BlsPublicKey`,
`PurposeTag` on `ContentPurpose`), typed `Error::MasterKey`, no free functions.

## Verification

`cargo test --offline`: 4 crypto-core + 2 actor-discipline + **16 daemon tests**
pass, including the new end-to-end `registered_signer_attestation_verifies_under_real_bls`
(register → sign-as-criome → verify = `Valid`; tampered content → `InvalidSignature`).
The existing `sign_with_unregistered_identity_returns_rejection` still passes — the
requester gate is preserved. `cargo clippy` and `cargo fmt --check` clean.

## What remains (operator hardening, not this pass)

- **`RegisterIdentity` signature verification** (`registry.rs:90` still only dedups)
  — until it verifies the Developer/master signature, the registry is self-asserted.
  Part of `primary-kr40`.
- **Production key custody** — `mlock`/`zeroize`, passphrase, and the eventual
  authenticated `meta-signal-criome` key configuration (which does not exist yet).
- **Binding the full attestation** — the preimage binds content + caller + purpose;
  binding `issued_at`/`expires_at`/signer too is a small hardening (the timestamp
  accessor was left out of this pass).
- **The spirit-side pilot** (`primary-5zur`) — the `CriomeAuthority` client, threading
  `ConnectionContext` past `daemon.rs:142`, the `EntryDigest` accessor, and the
  out-of-band attestation ledger. criome's real crypto unblocks it.

## Lane note

Designer demonstration pass: shape proven, real crypto, green tests. Operator owns
production depth (key custody, registration signing) and main integration. The
branch is ready for that integration from the local `criome-auth-pilot` bookmark.
