# ClaviFaber Repository Preparation

## Summary

Prepared `/git/github.com/LiGoldragon/clavifaber` as the standalone JJ-backed
repository for CriomOS host key-material provisioning. The existing prototype
was functional but stale against current repo discipline, so this pass kept the
working key/certificate behavior while replacing the repo scaffold, documenting
the architecture, and tightening the local identity implementation.

## Repository State

- Remote: `git@github.com:LiGoldragon/clavifaber.git`.
- Local checkout: `/git/github.com/LiGoldragon/clavifaber`.
- VCS: Jujutsu working copy on `main`.
- Repo docs added:
  - `/git/github.com/LiGoldragon/clavifaber/ARCHITECTURE.md`
  - `/git/github.com/LiGoldragon/clavifaber/skills.md`

## Fixes Applied

- Replaced the old blueprint flake with an explicit crane/fenix flake in
  `/git/github.com/LiGoldragon/clavifaber/flake.nix`.
- Added pure checks for build, test, format, and clippy under `nix flake check`.
- Moved the impure GPG lifecycle test to
  `/git/github.com/LiGoldragon/clavifaber/scripts/test-pki-lifecycle` and
  exposed it as `nix run .#test-pki-lifecycle`.
- Added crate metadata, a real library target, `thiserror`, `tempfile`, and Rust
  lint settings in `/git/github.com/LiGoldragon/clavifaber/Cargo.toml`.
- Replaced `src/complex.rs` with `src/identity.rs`; the signing key is now
  private inside `NodeIdentity`, and identity-directory behavior lives on
  `IdentityDirectory`.
- Changed the binary in `/git/github.com/LiGoldragon/clavifaber/src/main.rs`
  from private command free functions to Clap compatibility request structs.
- Moved SSH key parsing behind `OpenSshPublicKey` in
  `/git/github.com/LiGoldragon/clavifaber/src/ssh_key.rs`.
- Moved atomic write behavior behind `AtomicFile` and Assuan decoding behind
  `AssuanLine` in `/git/github.com/LiGoldragon/clavifaber/src/util.rs`.
- Made GPG signature S-expression parsing private to
  `/git/github.com/LiGoldragon/clavifaber/src/gpg_agent.rs`.
- Replaced the old integration test with premise-named process tests in
  `/git/github.com/LiGoldragon/clavifaber/tests/identity_directory_lifecycle.rs`.

## Current Architecture

ClaviFaber is now documented as four planes:

- Local material: private key formation, permissions, atomic writes, and
  corruption preservation.
- Public projection: public key/certificate records for the rest of CriomOS.
- Certificate authority: the current GPG-to-X.509 bridge.
- Publication: still future work; ClaviFaber should emit typed public-key
  publication records and should not patch cluster database files directly.

The existing `complex-init` and `derive-pubkey` subcommands are retained only as
compatibility names. `ARCHITECTURE.md` records the target operator surface as a
single Nota request argument.

## Verification

All verification passed in `/git/github.com/LiGoldragon/clavifaber`:

- `nix develop --command cargo test`
- `nix develop --command cargo clippy --all-targets -- -D warnings`
- `nix flake check`
- `nix run .#test-pki-lifecycle`

The lifecycle test exercised temporary GPG key creation, CA certificate
generation, server certificate generation, two node certificates, certificate
verification, public-key derivation, and corruption recovery.

## Remaining Work

- Move `/git/github.com/LiGoldragon/clavifaber/src/x509.rs` behind
  data-bearing issuer/request/result types. It is still the largest stale code
  surface and still exposes public free functions.
- Design and implement the typed public projection record for SSH public key,
  Yggdrasil material, and WiFi client certificate metadata.
- Add the Nota request surface and retire new feature work on the Clap
  compatibility CLI.
- Decide which component owns writes into the CriomOS cluster database, then
  make ClaviFaber push typed publication records to that owner instead of
  teaching it database file paths.
