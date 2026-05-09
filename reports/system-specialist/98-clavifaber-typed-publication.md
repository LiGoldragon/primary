# ClaviFaber Typed Publication Pass

## Summary

Implemented the next ClaviFaber step in
`/git/github.com/LiGoldragon/clavifaber`: typed certificate requests/results,
typed Nota request/response execution, and a public-key publication record for
cluster ingestion.

## Repository Changes

- Added `src/request.rs` with `ClaviFaberRequest` and `ClaviFaberResponse`.
  Inline Nota requests now execute through the same path as the compatibility
  CLI.
- Added `src/publication.rs` with `PublicKeyPublication` and
  `PublicKeyPublicationRequest`. The record carries node name, OpenSSH public
  key, optional Yggdrasil address, optional Yggdrasil public key, and optional
  WiFi client certificate PEM.
- Refactored `src/x509.rs` behind data-bearing certificate types:
  `CertificateAuthorityIssuer`, certificate signing requests, `CertificateDer`,
  `ServerCertificate`, and `CertificateChain`.
- Reworked `src/main.rs` so Clap subcommands are compatibility adapters over
  typed requests, while an argv value beginning with `(` is parsed as an inline
  Nota request.
- Added `tests/request_surface.rs` to cover request round-trips, inline Nota
  identity initialization, and cluster-ready public publication output.
- Updated `ARCHITECTURE.md`, `README.md`, and `skills.md` to mark the Nota and
  publication surface as implemented.

## Cluster Database Ownership

ClaviFaber deliberately does not write cluster database files. The database
writer belongs in the cluster-management/deployment layer that owns the
database revision and deployment transaction. In current workspace terms, that
means Lojix/CriomOS cluster publishing or a dedicated successor component.

ClaviFaber's contract now ends at a complete typed `PublicKeyPublication`
record.

## Verification

Passed in `/git/github.com/LiGoldragon/clavifaber`:

- `nix develop --command cargo test`
- `nix develop --command cargo clippy --all-targets -- -D warnings`
- `nix flake check`
- `nix run .#test-pki-lifecycle`

Pushed commit: `11b6610d8d01`.

## Remaining Work

- Wire a cluster-side consumer that accepts `PublicKeyPublication` and updates
  the CriomOS cluster database transactionally.
- Decide where real Yggdrasil identity generation belongs, then feed those
  public values into `PublicKeyPublicationRequest`.
- Replace the compatibility Clap path once downstream scripts have moved to
  the Nota request surface.
