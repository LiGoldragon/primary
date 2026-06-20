# 444 — Criome E1 audit and Mentci port

## Request

Audit designer's criome E1 increments 1-3 and port the parts that improve
Mentci.

## Audit conclusion

The useful Mentci-facing pattern in criome E1 is not the BLS/TCP peer transport
itself. That transport belongs to criome's quorum lane: cross-host peer
authorization, admitted-peer public keys, domain-separated frame signatures, and
daemon quorum tally.

The reusable shape for Mentci is the typed endpoint list from the E1
peer-addressing contract: configuration carries named connection points, and
runtime code selects the endpoint by type rather than by positional field.
Mentci is about to connect to multiple component sockets, so `home_criome_socket`
was the wrong model.

## Port landed

- `meta-signal-mentci` now declares `ComponentSocketKind`,
  `ComponentSocket`, and `ComponentSockets` on `MentciDaemonConfiguration`.
- `MentciDaemonConfiguration` now carries typed component socket endpoints
  such as `Mentci` and `MetaCriome`, plus lookup accessors.
- `mentci` now binds the `Mentci` socket and uses `MetaCriome` for criome
  ClientApproval pickup.
- `mentci-write-configuration` writes the new typed endpoint list.
- `mentci-egui` consumes the repinned daemon/meta contract stack and its live
  daemon test builds typed socket fixtures.

## Not ported

`PeerEnvelope`, `CriomePeerCodec`, and the BLS-signed TCP transport were not
ported to Mentci. Mentci's current problem is local component socket selection
and daemon-client observation, not cross-machine quorum signing. Copying criome's
peer transport here would add a security-sensitive network lane without a
Mentci authority model that needs it.

## Commits

- `meta-signal-mentci` main `42222f30` — typed component socket endpoints.
- `mentci` main `f5e17af0` — daemon configuration consumes typed component
  sockets.
- `mentci-egui` main `075cbff4` — GUI consumes the updated daemon/meta contract
  stack.

## Verification

- `meta-signal-mentci`: `cargo test --all-targets --features nota-text`;
  `cargo clippy --all-targets --features nota-text -- -D warnings`.
- `mentci`: `cargo test --all-targets`; `cargo clippy --all-targets -- -D
  warnings`.
- `mentci-egui`: `cargo test --all-targets`; `cargo clippy --all-targets -- -D
  warnings`.
