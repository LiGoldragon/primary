# 227 — Audit: SD criome auth implementation reference

Source under audit:

- SD report: `reports/system-designer/118-criome-auth-implementation-reference-2026-06-16.md`
- Worktree: `/home/li/wt/github.com/LiGoldragon/criome/criome-auth-pilot`
- Branch bookmark: `criome-auth-pilot`
- Branch head: `d09be336` (`criome: cluster-root admission gate (working core, tested)`)
- Base main reported by SD: `2a02cf4d`

## Findings

### P2 — `ClusterRoot::admits` ignores the signature envelope scheme

`src/admission.rs` verifies the admission envelope by checking only that
`admission.public_key` equals the configured root key, then calling
`verify_bls` on the envelope signature:

- `src/admission.rs:83` starts `ClusterRoot::admits`.
- `src/admission.rs:88` checks the public key.
- `src/admission.rs:91` builds the registration statement.
- `src/admission.rs:92` verifies the signature.

There is no check that `admission.scheme` is
`SignatureScheme::Bls12_381MinPk`. `VerifyBls` cannot check that for the
caller because its signature is only:

- `src/master_key.rs:125` defines `VerifyBls`.
- `src/master_key.rs:130` implements `verify_bls(&self, signature, message)`.

The verifier path already fixed this exact class of bug:

- `src/actors/verifier.rs:63` documents the algorithm-confusion guard.
- `src/actors/verifier.rs:65` matches on the envelope scheme.
- `src/actors/verifier.rs:67` rejects `Bls12_381MinSig`.

The admission gate needs the same guard before signature verification. As
written, an admission envelope can claim `Bls12_381MinSig` while carrying a
valid min-pk signature under the cluster-root key, and `admits()` will accept
it.

Recommended fix:

- Add an explicit `SignatureScheme::Bls12_381MinPk` check in
  `ClusterRoot::admits`.
- Add a unit test that mutates a valid cluster-root admission's scheme to
  `Bls12_381MinSig` and expects rejection.

### Status caveat — the branch is a crypto-core reference, not production auth

SD discloses this correctly, and the code confirms it. `src/admission.rs` is
the decision core for the cluster-root gate; `src/actors/registry.rs` is still
the old self-asserted registry:

- `src/actors/registry.rs:90` starts `register`.
- `src/actors/registry.rs:91` checks duplicate active identity.
- `src/actors/registry.rs:95` stores the registration.

There is no `ClusterRoot` field in `IdentityRegistry`, no
`IdentityRegistration.admission`, and no `UnauthorizedRegistration` rejection
yet because those require the `signal-criome` contract delta SD listed.

This is acceptable as a reference branch, but `primary-kr40` should not be
treated as closed until the contract change, regenerate, registry gate, and
Nix repin are integrated on main.

### Residual hardening — key-file load still has custody limits

The key-file fixes are materially better than the earlier audited branch:

- `src/master_key.rs:68` uses `symlink_metadata`.
- `src/master_key.rs:69` rejects non-regular files.
- `src/master_key.rs:75` rejects group/other permission bits.
- `src/master_key.rs:94` creates new key files with `create_new`.
- `src/master_key.rs:97` sets mode `0600`.
- `src/master_key.rs:100` fsyncs the file.

Two production-custody limits remain:

- The existing-file read does not verify file owner.
- The path is checked with metadata, then read by path at `src/master_key.rs:81`;
  that leaves a normal check-then-open race. For a same-user bootstrap this is
  tolerable, but for real custody the final design should open and validate the
  same file handle or use the platform's no-follow/openat pattern.

This is not a blocker to the branch's stated reference purpose. It belongs with
the production key-custody follow-up SD already named.

## Confirmed Fixes From The Previous Audit

The earlier audit findings in report 225 are mostly addressed in this branch:

- **Restore mismatch fail-loud:** `src/actors/root.rs:290` reconciles the
  stored criome identity with the adjacent master key and errors on mismatch.
- **Startup failure surfaced:** `src/actors/root.rs:103` waits for startup and
  returns `Error::Startup` if the root actor is dead.
- **Expiry checked:** `src/actors/verifier.rs:91` returns `Expired` for
  validly signed attestations past their deadline.
- **Verifier scheme checked:** `src/actors/verifier.rs:63` rejects the wrong
  BLS scheme.
- **Full attestation preimage:** `src/master_key.rs:148` documents the signed
  fields; `src/master_key.rs:179` includes content purpose, audit purpose,
  scheme, signer, issued time, expiry, and length-delimited text fields.
- **Signer binds the generated envelope:** `src/actors/signer.rs:104` builds
  the attestation, `src/actors/signer.rs:118` derives the signing bytes from
  that attestation, and `src/actors/signer.rs:119` fills the signature.

## Verification

Run in `/home/li/wt/github.com/LiGoldragon/criome/criome-auth-pilot`:

- `cargo test --offline` — passed, 31 tests.
- `cargo clippy --offline --all-targets -- -D warnings` — passed.
- `cargo fmt --check` — passed.
- `nix flake check` — passed. Nix reported the standard warning that
  `aarch64-linux` was omitted.

## Recommendation

Use the branch as the implementation reference, but fix the admission
scheme check before main integration. Then wire the contract delta in this
order:

1. Add `IdentityRegistration.admission`, `CriomeDaemonConfiguration.cluster_root`,
   and `RejectionReason::UnauthorizedRegistration` to `signal-criome`.
2. Regenerate and repin criome.
3. Thread `Option<ClusterRoot>` into `IdentityRegistry`.
4. Gate every `RegisterIdentity` through `ClusterRoot::admits`.
5. Add end-to-end tests for accepted root-signed registration, rejected missing
   admission, rejected wrong-root admission, rejected relabelled admission, and
   rejected wrong-scheme admission.

After that, the crypto-core and registry boundary line up. Production key
custody and the provisioning ceremony remain separate hardening/deploy work.
