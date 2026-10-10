# Lojix and Horizon boundary witnesses

This witness records the immutable releases tested on 2026-09-10. No live
service, live state, or protected CriomOS Home path was changed by these gates.

## Typed Horizon boundary

Horizon 0.8.0 generates `HorizonDefinition` from its authored Ethos and carries
that already actualized value in the data-only Lojix Signal contract. The
Datom/text boundary lives in the meta client and offline input adapter. The
Nexus receives only the typed portable value. Seven local Horizon tests cover
decode, semantic validation, generated freshness, and typed round trips.

A cached remote `nix flake check --print-build-logs` invocation exited 0. It
evaluated the default library package, `horizon-compose`, and the Horizon test
derivation, then reported `all checks passed!`; it built zero derivations
because all results were already present in the Nix store.

## Package and wire boundary

Lojix 1.0.0 established five workspace packages: the shared `lojix` runtime
library, Datom-free `lojix-nexus`, ordinary `lojix` and privileged `lojix-meta`
clients, and `lojix-offline-tools`. Lojix 1.0.1 follows with the same behavior
and moves the newly authored runtime operations under qualifier-named traits.
The default Nix package contains:

- `lojix-nexus`: zero-argument long-running Nexus.
- `lojix`: ordinary Signal client.
- `lojix-meta`: privileged Signal client.
- `lojix-bootstrap`: explicit daemon-free bootstrap.
- `lojix-write-configuration`: historical archive writer for offline input.
- `lojix-migrate-configuration`: one-shot copy migration.
- `lojix-inspect-store`: offline store inspection.
- `lojix-reset-store`: explicit offline reset.

There are no `lojix-daemon` or `meta-lojix` executable aliases. Requests and
responses use generated `Signalizable`, `Signal<T>`, `Restorable`, and
`ByteViewable` over runtime-owned length framing. Direct typed lowering
preserves both nonempty secret-reference variants without reading or printing
their values.

`cargo tree -p lojix-nexus --edges normal` contains neither `datom-codec` nor
`protos`. The Nexus package depends on the shared library with default features
disabled. Datom is enabled only by clients and offline tools.

## Configuration lifecycle and process behavior

The Nexus discovers a stable Sema beneath an explicitly isolated XDG state
root and seeds the executable default only for a fresh store. Desired
configuration and the `meta_configure_occurred` marker persist beside domain
state. Ordinary Configure remains available while the marker is false and does
not set it. Successful meta Configure sets it; only meta reversal clears it.
Desired socket settings take effect on the next zero-argument restart.

Three Nexus package tests prove startup argument rejection before state
creation and an isolated two-socket process sequence across restart: ordinary
Configure, meta Configure, ordinary rejection, meta reversal, desired socket
activation, marker persistence, and stable domain-store retention. Request
effects pass through the Kameo worker and deploy/test actors rather than
mutating the store in the listener.

## Historical archive and safe migration

`tests/fixtures/lojix-v5-pre-nexus-cf231859.sema` was created by exact
pre-Nexus Lojix revision `cf231859d689` using its historical `Store` writer.
Its SHA-256 is
`d5fdafb6a6c8a1830bb45f6397bb9523909b1d5f975abcec638d00fa51a5c7c7`.

Normal opening first copies an existing store to a uniquely created disposable
probe and asks `sema-engine` to validate the copy. A version or configuration
failure removes the probe and leaves source bytes unchanged. The one-shot
migration also copies the historical source to a new target, maps every legacy
configuration and test-default field, retains every domain row and the
allocator/commit sequence, validates reopen, and never opens the source for
mutation. Three offline lifecycle/migration tests, thirteen bootstrap tests,
and three configuration-writer tests passed.

## Gates

- Lojix 1.0.0: full workspace checks and tests passed; root library 96/96, one
  preexisting network test ignored. `nix flake check --print-build-logs` exited
  0 after running 35 derivations, including fresh Nexus startup and the
  same-host restart/deploy VM.
- Lojix 1.0.1: focused Nexus 3/3 and offline 19/19 tests, workspace check,
  formatting, and clippy passed. `nix flake check --print-build-logs` exited 0
  after evaluating 39 checks, including the fresh-start and same-host restart
  VM behavior.
- `nix build .#default --no-link --print-out-paths` on 1.0.0 exited 0; direct
  inspection confirmed the command set above.

## Sources

- Commands and outputs executed by subflow `/root/runtime_complete` on
  2026-09-10.
- Horizon 0.8.0 `e48712203b7aad4bfb03088a4bda0a87ae064692`.
- Nexus 0.1.1 `a84bfa960c0d5c02d30048c4bbbc67dfef79a67c`.
- signal-lojix 1.1.0 `3a57717e5a09591aecbaafd88bd138647a1d872d`.
- meta-signal-lojix 2.2.0
  `901e5da6c8a58993479b7ba2ed1d0d62908d53b1`.
- Lojix 1.0.0 `e2c7bdc55a1098c8a2ec018dfa0f95429b7a22fd`.
- Lojix 1.0.1 `b8f7a8cc834c90e08918410ea32f28d1b4c6949c`.
- Historical Lojix `cf231859d689`, used independently to create the v5 fixture.
- `Vision/nexus.md` and the flow's supplied final Nexus authority.
