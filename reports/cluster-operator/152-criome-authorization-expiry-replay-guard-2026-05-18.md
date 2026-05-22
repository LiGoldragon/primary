# Criome Authorization Expiry And Replay Guard

Date: 2026-05-18

Role: operator-assistant

Source architecture: `reports/designer/214-criome-architecture-record-2026-05-17.md`

Implementation commit: `criome` `55077e2d2d6d6e1b43b801b951e9da729a2dd1a9`

## What I Implemented

I selected designer/214 open item 11.13, "Replay-guard + expiry enforcement", as the highest-signal implementation slice that fit the current `criome` prototype without needing a new contract.

The landed `criome` change makes `AuthorizeSignalCall` enforce two constraints before entering normal signing state:

- An expired `expires_at` records a durable authorization state with `AuthorizationStatus::Expired` and returns `CriomeReply::AuthorizationExpired`.
- Reuse of the same requester plus replay nonce is rejected as `RejectionReason::ReplayAttempted` before a second authorization request slot is minted.

This keeps the existing store-minted `AuthorizationRequestSlot` rule intact. The request digest remains signed payload content, not request identity.

## Files Changed In `criome`

- `src/error.rs`: added `AuthorizationReplayAttempted`.
- `src/tables.rs`: added the `authorization_replay_nonces` Sema table and `AuthorizationReplayIdentity`.
- `src/actors/store.rs`: made authorization state creation preserve replay and store failures across the Kameo ask boundary.
- `src/actors/authorization.rs`: added expiry handling and replay rejection mapping in `AuthorizationCoordinator`.
- `tests/daemon_skeleton.rs`: added expiry and replay tests, and adjusted slot-minting coverage to use distinct nonces.
- `flake.nix`: added a Nix architecture check for the expiry/replay guard.
- `ARCHITECTURE.md`: updated current implementation status.
- `skills.md`: recorded the local invariant for future contributors.

## Tests

Run in `/git/github.com/LiGoldragon/criome`:

```text
cargo fmt
cargo test --test daemon_skeleton
cargo test
cargo clippy --all-targets -- -D warnings
nix --option max-jobs 1 --option cores 2 flake check -L
```

All passed.

## Remaining Debt

This does not complete criome authorization. It closes only the expiry/replay slice.

Still open from designer/214:

- `ObserveAuthorization` is still snapshot-shaped; the push stream remains needed.
- `VerifyAuthorization` still needs real BLS signature verification against registered public keys.
- Simple self-signed policy still needs master-key signing that produces a real authorization grant.
- `owner-signal-criome` still needs to carry passphrase submission, policy mutation, peer-route mutation, and owner approval prompts.
- The replay key is currently requester plus nonce. The full `SignedObject` canonical bytes decision in designer/214 11.7 is still wider: request digest, target cluster or node, action, expiry, anti-replay nonce, and issuing criome identity.

## Current Assessment

The authorization state machine is now less misleading: expired requests and replayed nonces no longer fall into the same "pending signing" path as live authorization requests. That makes the next slices safer to implement because push observation, real signing, and real verification will not have to retrofit these two basic state transitions later.
