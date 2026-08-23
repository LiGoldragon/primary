# Restoring meta-orchestrate

## Finding

The path-lock epic removed `meta-orchestrate` without a living ruling authorizing that removal. The living's stripped path-lock ruling constrained the path-lock datum; realizing agents broadened it into removal of older meta surfaces and then deleted the meta CLI and its Dotos path. The deletion is therefore incorrect work, not an intended breaking deployment contract.

The current epic still has the Nexus root surface: the daemon binds its meta socket, decodes `meta-signal-orchestrate` frames, and handles the sole current privileged operation `Refresh(RefreshRepositoryIndexOrder)` with a typed `RepositoryIndexRefreshed` reply.

## Repair boundary

Restore the exact executable name `meta-orchestrate`. It is the default thin client for Orchestrate's meta socket; it is not renamed to `orchestrate-meta` and no alias is added.

The restored client:

- accepts exactly one typed meta request;
- connects only to `PERSONA_ORCHESTRATE_META_SOCKET`, retaining the established default only if the current configuration design requires it;
- frames the request through the current `meta-signal-orchestrate` contract;
- validates and prints the typed reply;
- never opens the Sema store, performs daemon logic, accepts ordinary requests, or auto-routes between sockets.

The source surface is the `meta-orchestrate` Cargo target, `src/bin/meta_orchestrate.rs`, the current-contract `MetaSignalTransport` and export, and a text codec in the meta-signal producer if the living chooses a textual CLI boundary. The old broad owner vocabulary is not restored; the epic's refresh-only contract remains authoritative.

CriomOS-home already wraps `meta-orchestrate` and supplies the runtime meta socket. Its package construction therefore supplies a downstream proof that the binary is present. The unrelated ordinary-socket environment mismatch and typed daemon-configuration follow-up remain separate work.

## Proof

Before source repair, the trusted behavioral witness must fail because `cargo build --bin meta-orchestrate` has no target. After repair it starts the daemon with temporary store and socket paths, waits for the meta socket event, invokes the packaged client against that socket, and observes a successful typed `RepositoryIndexRefreshed(0)` reply. Invalid or ordinary-tier input is rejected at the client boundary.

The witness is exposed through a Nix check. The full epic gates remain `build`, `test`, `test-path-lock-registry`, `stateful-path-lock-scenario`, `fmt`, and `clippy`; Nix evaluation and remote building remain separate. CriomOS-home then proves both the packaged executable and its wrapped invocation.

The epic remains unreleased `0.21.0`, so repairing its accidentally removed package surface does not require another version bump.

## Open ruling

The epic's refresh-only meta-signal contract is rkyv-only and has no current text representation. Restoration therefore needs the living to choose its one input representation: reintroduce a narrow Dotos text form, establish the current Datom/NOTA text form, or accept signal-encoded input only. No source edit should invent that public contract.

The statement that all nexuses have a meta socket guides every Nexus rather than only Orchestrate; its level as Vision or Intent also remains for the living.

## Sources

- Flow `01a02a34`, especially `reports/pathLockEpic.md`, `vision/pathLocks.md`, and the originating transcript events identified by the repair-history subflow.
- Flow `01a02fd5`, `vision/metaOrchestrate.md` and `vision/nexuses.md`.
- Orchestrate `b1435557`: `Cargo.toml`, `src/bin/meta_orchestrate.rs`, `src/signal_transport.rs`, and `src/lib.rs`.
- Orchestrate epic `de59c3f74d7c`: deletion diff, `src/daemon.rs`, `src/service.rs`, `src/configuration.rs`, `Cargo.toml`, and `flake.nix`.
- Meta Signal Orchestrate `f1dec7e3f7b0`: `Cargo.toml` and `src/lib.rs`.
- CriomOS-home `modules/home/profiles/min/orchestrate.nix` and `checks/orchestrate-service-path`.
- Beads `orchestrate-fv7` and `orchestrate-yjo`.
