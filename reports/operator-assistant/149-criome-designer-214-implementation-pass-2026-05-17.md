# 149 - Criome designer/214 implementation pass

Date: 2026-05-17
Role: operator-assistant
Scope: `signal-criome`, `criome`
Primary design record: `reports/designer/214-criome-architecture-record-2026-05-17.md`

## Summary

Applied the high-signal parts of designer/214 to the public
`signal-criome` and `criome` repositories.

The pass makes `signal-criome` carry policy-satisfaction evidence
on grants and denial-source evidence on denials. It makes `criome`
own the first actor-heavy routed-authorization skeleton: a
data-bearing `AuthorizationCoordinator`, Sema-backed authorization
state tables, root routing for the authorization request variants,
and a daemon owner-socket mode witness.

Designer/214 supersedes /212 and /213. I also absorbed its newer
owner-session decision: owner socket mode `0600` remains the local
authority boundary, but owner-signal-criome traffic must be
ECDH/AEAD-encrypted before carrying passphrases or owner-class
traffic. That is now in `criome/ARCHITECTURE.md`, `criome/skills.md`,
and a Nix document witness.

## Landed

`signal-criome`

- Added `AuthorizationPolicyClass`, `RequiredSignatureThreshold`,
  and `AuthorizationPolicySatisfaction`.
- `AuthorizationGrant` now carries policy class, threshold, and
  satisfied signers.
- Added `AuthorizationDenial` and `AuthorizationDenialSource`, so
  policy refusal and signer refusal are distinct on the wire.
- Added `AuthorizationStatus::Signing` for pending signature work.
- Added round-trip witnesses for policy evidence, denial-source
  separation, and absence of owner-class operations.
- Updated canonical NOTA examples.
- Published:
  - `9dff026` - `model authorization policy satisfaction`
  - `bd98b9d` - `document authorization policy evidence`

`criome`

- Added `src/actors/authorization.rs` with a data-bearing Kameo
  `AuthorizationCoordinator`.
- `CriomeRoot` now supervises the coordinator and routes
  `AuthorizeSignalCall`, `ObserveAuthorization`,
  `VerifyAuthorization`, `RouteSignatureRequest`,
  `SubmitSignature`, `RejectAuthorization`, and
  `AuthorizationObservationRetraction`.
- Added Sema tables for authorization request state, signature
  solicitations, and submitted signatures.
- The daemon bind path now sets the Unix socket to mode `0600`;
  tests witness this.
- Added a Nix check that fails if the architecture reintroduces the
  stale plaintext-passphrase owner-session wording.
- Published:
  - `2b74697` - `add routed authorization coordinator skeleton`

## Tests

`signal-criome`

- `cargo test`
- `cargo clippy --all-targets -- -D warnings`
- `nix --option max-jobs 1 --option cores 2 flake check -L`

`criome`

- `cargo test`
- `cargo clippy --all-targets -- -D warnings`
- `git diff --check`
- `nix --option max-jobs 1 --option cores 2 flake check -L`

## Worst parts / known debt

- `AuthorizationCoordinator` is still a skeleton. It records pending
  signing state and stores solicitation/submission records, but it
  does not perform real policy lookup, owner-signal approval,
  master-key signing, quorum aggregation, expiry, or replay checks.
- `VerifyAuthorization` currently checks only exact digest equality.
  Signature verification and policy validation are still future work.
- The authorization request slot is derived from the digest string.
  A real typed slot-minting path should replace this before the
  state becomes operationally important.
- Owner-signal-criome does not exist yet. The encryption decision is
  documented and Nix-witnessed, but there is no ECDH/AEAD session
  implementation in code yet.
- The broad `ReadAuthorizationSnapshot` store path exists, but the
  coordinator currently observes by one slot and does not implement a
  pushed subscription stream.
- `Cargo.lock` in `criome` advanced `signal-core` transitively while
  updating `signal-criome`; this matches dependency resolution but
  is worth noting for reviewers.

## Next high-signal work

- Design and create `owner-signal-criome`.
- Implement simple self-signed policy: policy lookup, master-key
  signing, and `AuthorizationGrant` issuance with satisfied policy
  evidence.
- Add the no-effect-before-grant integration witness with Lojix once
  the `CriomeAuthorizationActor` side is ready.
- Replace digest-derived request slots with a typed durable slot
  allocator.
- Turn `ObserveAuthorization` into a real push stream rather than a
  snapshot-only skeleton.
