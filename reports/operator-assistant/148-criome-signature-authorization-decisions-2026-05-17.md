# Criome signature authorization decisions

Date: 2026-05-17
Role: operator-assistant
Scope: `signal-criome`, `criome`, future `tui-criome`

## Summary

The latest user decisions have been promoted into the permanent
architecture layer for Criome authorization. The important correction
is that Criome is not an ACL or permission-slot daemon. It receives
requests, routes signature solicitations, records signature outcomes,
and derives permission from signatures over the exact request digest.

The architecture edits landed in:

- `/git/github.com/LiGoldragon/signal-criome/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/criome/ARCHITECTURE.md`

The implementation consequence is a three-part shape:

1. `signal-criome` is the public wire contract.
2. `criome-daemon` owns routed authorization state and grant issuance.
3. `tui-criome` becomes the stateful signing surface with its own Sema
   database and key custody.

## User decisions captured

- Publish the Criome authorization contract and daemon work through
  public GitHub repositories.
- Criome has a different permission model from the rest of the
  components: it receives authorization requests and asks for
  signatures.
- Criome's permission comes from signatures, not from an internal
  permission slot, ACL row, or daemon-local approval table.
- The authorization subject is the exact canonical Signal request
  digest. A grant for request A cannot authorize request B.
- Pending authorization is first-class state. It is observed through a
  push subscription, not by polling.
- `tui-criome` is needed as a separate component. It is a TUI with its
  own Sema database for persistent signing-client state.
- `tui-criome` stores request history, signing decisions, and
  signing-client private/public keypairs.
- `tui-criome` speaks `signal-criome`; it can be presented signature
  requests, submit signatures or rejections, and create signed requests
  for Criome to route.
- `criome-daemon` keeps Criome's root keypair for criome-issued
  attestations, but signing-client key custody belongs to the signing
  client.

## Architecture consequences

`signal-criome` now states the active contract vocabulary as
signature-solicitation shaped:

- `AuthorizeSignalCall` starts the routed authorization relation.
- `RouteSignatureRequest` presents signature work to a signing surface.
- `SubmitSignature` and `RejectAuthorization` close a signer decision.
- `ObserveAuthorization` pushes pending, granted, denied, expired, and
  unavailable state.

`criome` now states the daemon's owned state as:

- authorization request state;
- signature solicitation state;
- submitted signature state;
- grant state;
- expiry and replay policy.

That is intentionally different from a local permission database. The
authorization grant is an envelope whose authority derives from
signatures over the exact request digest.

## Published state

Before this report, the public repositories were already published and
validated:

- `https://github.com/LiGoldragon/signal-criome`
  - public visibility confirmed;
  - current published commit before this architecture follow-up:
    `e78ffd1 add routed authorization contract`;
  - `cargo test` passed;
  - `nix --option max-jobs 1 --option cores 2 flake check -L` passed.
- `https://github.com/LiGoldragon/criome`
  - public visibility confirmed;
  - current published commit before this architecture follow-up:
    `8b7f497 document signature-derived criome authorization`.

## Open implementation work

The next implementation pass should not add ACL-style permission
records. It should implement the signature-derived path:

- In `criome`, add `AuthorizationCoordinator` runtime behavior and the
  Sema tables for authorization requests, signature solicitations, and
  submitted signatures.
- Add witnesses that Lojix-shaped effects do not execute before
  `AuthorizationGranted`.
- Add a negative witness that an authorization grant for one request
  digest cannot authorize a different request digest.
- Add an observation witness for pending authorization updates through
  `ObserveAuthorization`.
- Create the `tui-criome` component as the keyholding signing client.
  Its first useful state should be request history, key metadata, and
  signer decisions in a local Sema database.
- Add a witness that signing-client private key material is not stored
  in `criome-daemon` state.

## Worst current gaps

The contract exists and the architecture now states the correct model,
but the daemon implementation is still mostly architectural. The
authorization coordinator, durable signature-solicitation tables, and
push observation path still need code and Nix-wired tests.

`tui-criome` is only a named component and bead-backed task right now.
The architecture has enough shape to build it, but key storage details,
TUI workflow, and the exact test harness still need implementation
choices.
