# 150 - Criome authorization slot identity follow-up

Date: 2026-05-17
Role: operator-assistant
Scope: `signal-criome`, `criome`

## Trigger

`reports/designer/214-criome-architecture-record-2026-05-17.md`
named the most urgent implementation debt after the routed
authorization skeleton: authorization request slots were derived
from the request digest. That violated the workspace rule that
infrastructure mints identity. A request digest is content; an
authorization request slot is durable store identity.

## What landed

### signal-criome

Commit: `be950e3` - `carry authorization request slot on grants`

`AuthorizationGrant` now carries `request_slot:
AuthorizationRequestSlot`. This lets verification and denial paths
refer to the presented grant's durable request identity instead of
reconstructing an identity from the authorized object digest.

The contract architecture and repo skill now state the rule:
authorization grants carry daemon-minted request identity, and
verification paths must not derive request slots from request
digests.

Round-trip and canonical NOTA examples were updated so this is part
of the contract surface, not just an implementation convention.

### criome

Commit: `73d34bf` - `mint authorization request slots in store`

`criome` now consumes `signal-criome` at `be950e3`.

`StoreKernel` owns a new `CreateAuthorizationState` message. The
table layer owns `authorization_next_slot`, mints the next durable
authorization slot, stores the pending signing-state, and returns
the stored state to `AuthorizationCoordinator`.

`AuthorizationCoordinator` no longer has a digest-to-slot helper.
For `AuthorizeSignalCall`, it asks the store to create state and
uses the returned slot. For digest-mismatch denial in
`VerifyAuthorization`, it echoes the grant's `request_slot`.

The daemon skeleton test now witnesses the constraint directly:
submitting the same `SignalCallAuthorization` twice yields the same
request digest but two different request slots, and neither slot is
the digest string.

`flake.nix` now has an architectural truth check:
`criome-authorization-slots-are-store-minted`. It asserts that the
store table exists, that the architecture carries the store-minted
constraint, and that source does not reintroduce the old
digest-derived helper shape.

## Architecture and skills updated

`criome/ARCHITECTURE.md` now names:

- `authorization_next_slot` in the Sema table map.
- The constraint that authorization request slots are
  store-minted identities and must not be derived from digests.
- The current implementation status: `AuthorizationCoordinator`
  asks `StoreKernel` to mint authorization request slots.

`criome/skills.md` now carries the same hard invariant for future
agents.

## Verification

In `signal-criome`:

- `cargo test`
- `cargo clippy --all-targets -- -D warnings`
- `git diff --check`
- `nix --option max-jobs 1 --option cores 2 flake check -L`

In `criome`:

- `cargo fmt`
- `cargo test`
- `cargo clippy --all-targets -- -D warnings`
- `git diff --check`
- `nix --option max-jobs 1 --option cores 2 flake check -L`

Both repos were pushed to `origin/main`. `criome` was also pushed to
coordination branch `push-myxskuskznsw`; `signal-criome` was pushed
to coordination branch `push-tkmmmqvolpkw`.

## What remains ugly

- `ObserveAuthorization` is still snapshot-only. The architecture
  says pending authorization is pushed; the code does not yet have a
  subscription actor or delta stream.
- `VerifyAuthorization` still checks only digest equality. The real
  path must verify BLS signatures, signer registry status, policy
  class, threshold satisfaction, expiry, and replay state.
- Simple self-signed policy does not yet issue a real
  master-key-signed grant. The coordinator can persist pending state,
  but it cannot grant permission autonomously.
- Replay and expiry guards are still architecture constraints, not
  implementation.
- `AuthorizationRequestSlot` remains a string newtype at the
  contract boundary. The daemon now mints numeric string slots in the
  store, which is better than digest-derived identity, but a future
  contract pass may want a stronger slot shape.
- The fallback allocator ignores historical non-numeric slots if a
  pre-change database lacks `authorization_next_slot`. That is fine
  for this early prototype, but it is not a real migration story.

## State after this pass

Designer/214 open item 11.11 is implemented in the active contract
and daemon code. The remaining load-bearing slices are 11.10,
11.12, 11.13, and 11.14: push observation stream, real BLS/policy
verification, simple self-signed grant issuance, and replay/expiry
enforcement.
