# 225 — Audit: SD criome BLS implementation

## Scope

Audited SD report `reports/system-designer/114-criome-bls-implementation-2026-06-16.md` against the local feature worktree:

- Worktree: `~/wt/github.com/LiGoldragon/criome/criome-auth-pilot`
- Local `jj` bookmark: `criome-auth-pilot`
- Tip: `4e288517` (`criome: wire real BLS sign/verify through the daemon actors`)
- Base: `main` at `2a02cf4d`

The worktree has no `.git` directory and is only usable through `jj` in this checkout. `jj bookmark list` shows the local `criome-auth-pilot` bookmark; it is not pushed.

## Verification Run

Passed:

- `cargo test --offline`
- `cargo clippy --offline --all-targets -- -D warnings`
- `nix flake check`

The reported test count is accurate: 4 `master_key` unit tests, 2 actor-discipline tests, and 16 daemon tests.

## Findings

### P1 — Restored stores can silently mint unverifiable attestations

In `src/actors/root.rs:270-295`, startup derives the master-key path beside the store, loads or generates a key, then tries to register `Host("criome")` with the derived public key. The registration result is discarded.

This creates a real restore/migration failure mode:

1. A `criome.sema` store already contains an active `Host("criome")` identity with public key A.
2. The adjacent `.masterkey` file is missing, corrupt, or copied from another host.
3. Startup generates or loads key B.
4. `RegisterIdentity` rejects the already-active `Host("criome")` as duplicate.
5. The error is ignored.
6. The signer emits attestations with key B and signer `Host("criome")`.
7. The verifier resolves `Host("criome")` from the registry as key A and returns `InvalidSignature`.

That means the daemon can start apparently healthy but sign receipts that its own verifier rejects. This is especially relevant because the system is explicitly building backup/restore and daemon migration paths.

Fix direction: startup must reconcile the master key against the existing registered criome identity. If a `Host("criome")` record exists, its public key must match `master_key.public_key()` or startup must fail with a typed, visible error. If no record exists, register and require success.

### P1 — Expired attestations still verify as `Valid`

`signal-criome` has `VerificationDecision::Expired`, but `src/actors/verifier.rs:58-73` only checks content equality, signer existence, revocation, public-key equality, and BLS validity. It passes `request.attestation.expires_at` through in the result, but never compares it to current time.

So an attestation with a valid signature and an expired `expires_at` returns `VerificationDecision::Valid`, not `Expired`.

If the intended contract is “criome only verifies the signature and callers enforce time,” then the `Expired` decision is misleading and should not exist here. But the current contract enum and architecture imply criome owns validity classification. For the spirit/criome pilot, stale auth accepted as cryptographically valid is the wrong default.

Fix direction: give `AttestationVerifier` a clock like `AttestationSigner`, reject expired attestations with `VerificationDecision::Expired`, and add a daemon test.

### P1 — Key-file creation and loading do not enforce secret-file safety

`src/master_key.rs:71-76` writes the secret with `std::fs::write` and then calls `set_permissions(0600)`. On Unix that creates the file according to process umask first, then narrows permissions. With a permissive umask, there is a window where the secret can exist with broader permissions.

`src/master_key.rs:64-68` also loads an existing secret without checking file type, owner, symlink status, or mode. The test at `src/master_key.rs:252-267` verifies that a newly generated file ends at `0600`, but not that unsafe existing files are rejected.

Fix direction: create with `OpenOptions::create_new(true)` plus `OpenOptionsExt::mode(0o600)`, write/fsync through the opened handle, and reject existing keys unless they are regular files owned by the current uid with mode `0600` or stricter. If symlink handling matters, use `symlink_metadata` before opening and avoid following symlinks for the safety check.

### P2 — Verifier ignores `SignatureEnvelope.scheme`

`signal-criome` defines both `Bls12_381MinPk` and `Bls12_381MinSig`. The signer emits `Bls12_381MinPk` in `src/actors/signer.rs:109-112`, but the verifier never checks the envelope scheme in `src/actors/verifier.rs:58-73`; it always parses the envelope bytes as `blst::min_pk`.

An envelope can claim `Bls12_381MinSig` while carrying min-pk-shaped bytes and still verify. That is not an immediate forgery, but it is algorithm-confusion drift at the trust boundary.

Fix direction: match on `request.attestation.envelope.scheme`. Accept `Bls12_381MinPk` here; return `InvalidSignature` or an explicit unsupported-scheme decision for `Bls12_381MinSig` until that path is implemented.

### P2 — The signed preimage omits signer and validity interval

`AttestationPreimage` signs content and audit context in `src/master_key.rs:124-159`, but not `attestation.signer`, `issued_at`, `expires_at`, `SignatureEnvelope.scheme`, or envelope public key.

SD calls signer/time binding “small hardening,” but for an authentication substrate I would treat at least `signer` and `expires_at` as part of the signed statement. Otherwise, verifier correctness depends on external equality checks and registry constraints rather than the signature directly covering the attestation semantics.

The current branch partially compensates by checking the signer’s registered key equals the envelope public key, but because `RegisterIdentity` is still self-asserted and duplicate public keys are not rejected, relabeling attacks remain easy to create in the current trust model.

Fix direction: define an attestation-preimage schema that includes the full signed statement: content reference, signer identity, audit context, issued/expires fields, and scheme. The envelope signature field itself is naturally excluded.

### P2 — Daemon startup panics on master-key errors

`src/actors/root.rs:270-272` calls:

```rust
let master_key = MasterKey::load_or_generate(&master_key_path)
    .expect("load or generate criome master key");
```

`CriomeRoot::Error` is `Infallible`, so key I/O and decode failures bypass the crate’s typed `Error::MasterKey` path and become a panic. That is especially bad for a daemon: a corrupt key should be a diagnosable startup failure, not an actor panic.

Fix direction: change `CriomeRoot::Error` to the crate `Error`, map child-spawn failures and master-key failures through it, and add a corrupt-key startup test.

### P3 — Architecture docs are now stale

The branch updates code and tests, but `ARCHITECTURE.md:561-563` still says `VerifyAttestation` reports `InvalidSignature` until real BLS verification lands. Since this branch is exactly that landing, the architecture file now misleads the next operator.

Fix direction: update the architecture section in the same integration pass, especially around self-owned signing, verifier checks, expiry behavior, and remaining hardening.

## What Is Solid

The placeholder signature is actually gone from the core path. `MasterKey::sign` uses `blst`, `BlsPublicKey::verify_bls` verifies with the same domain separation tag, and the new daemon witness proves register-requester → sign-as-criome → verify-valid, plus content tamper → invalid.

The self-owned signing model is coherent: criome signs as its own host identity, while the requested caller is carried in audit context. That is the right model given the current registry only stores public keys.

The implementation mostly respects the Rust discipline: behavior is attached to `MasterKey`, `AttestationPreimage`, generated wire nouns, and actor types; no production free functions were added.

## Recommendation

Treat SD’s branch as a good crypto-core spike, not production-ready authentication. I would not integrate it to main as-is for the spirit pilot unless the operator immediately follows with the P1 fixes above.

Minimum landing gate:

1. startup reconciles master key and registered criome identity, failing loudly on mismatch;
2. verifier returns `Expired` for expired attestations;
3. master-key files are created atomically at `0600` and unsafe existing files are rejected;
4. scheme mismatch is rejected;
5. architecture is updated.

The known open item `RegisterIdentity` signature verification remains critical and should stay on `primary-kr40`; it is not retired by this branch.
