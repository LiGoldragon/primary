# Orchestrate Nexus witness

## Coordination probe — 2026-08-25

Method: probe. From `/git/github.com/LiGoldragon/orchestrate`, invoke the
deployed coordination clients with a concrete registration and a narrow claim:

```text
meta-orchestrate '(Register {{OrchestrateNexus OrchestrateNexus {{[OrchestrateNexus Operator]} Structural} (replace daemon nexus)} Fresh})'
orchestrate '(Claim {OrchestrateNexus [Path./git/github.com/LiGoldragon/orchestrate] (replace daemon nexus)})'
```

Observed output from both invocations:

```text
transport error: transport IO error: No such file or directory (os error 2)
```

The daemon socket was absent. This is not evidence of a registration or claim
refusal. Per the coordination fallback, work continues while recording the
missing advisory service.

## Pre-replacement architecture read — 2026-08-25

Method: code read. At `orchestrate` parent `b1435557`, `ARCHITECTURE.md`
described an ordinary, meta, and upgrade socket; an extensive lane/claim,
worktree, workflow, agent, router, and messenger state domain; and a six-path
positional daemon start interface. `Cargo.toml` pinned a large set of those
peer contracts. The client binaries accepted file-shaped component arguments
and performed presentation behavior beyond a direct typed text-to-Signal
boundary.

The replacement POC deliberately does not retain that domain or its upgrade
socket. It retains only the Nexus boundaries that are independently grounded:
the daemon is the sole durable-state owner, ordinary and meta sockets use their
separate compiled Signal contracts, and text is confined to the two clients.

## Replacement implementation read — 2026-08-25

Method: code read. The replacement at Orchestrate version `0.22.0` has only a
daemon (`src/main.rs`), a durable owner (`src/store.rs`), generated-frame Unix
transport (`src/transport.rs`), and the two thin client binaries. The daemon
accepts one URL-safe-unpadded-base64 argv argument, immediately decodes it as a
generated meta Signal frame, and accepts only `Configure` startup. Base64 is
therefore an argv envelope for a typed frame, never a socket protocol.

The normal socket dispatches generated `Register(PathLock)` and
`Release(PathLockRelease)` requests; the meta socket dispatches generated
`Configure(Configure)`. Both interfaces are imported from the Ethos-generated
contract crates—ordinary `signal-orchestrate` `d23fb6430eda` (v0.16.1, contract
id 1 / wire revision 4) and meta `meta-signal-orchestrate` `ebefb65c7076`
(v0.10.1, contract id 2 / wire revision 3). There is no handwritten contract,
codec, or compatibility protocol. `OrchestrateStore` alone opens the Sema
store, persists the normalized full locks and configuration, and returns
generated typed domain refusal carriers.

## Live POC — 2026-08-25

Method: probe. Ran the `live_daemon_reserves_releases_and_configures_over_separate_signal_sockets`
integration test with `cargo test --offline --test live_nexus -- --nocapture`.
It constructed the framed base64 Configure startup argument, started the real
`orchestrate-daemon` binary with a temporary `.sema` store and two temporary
Unix sockets, then invoked the real `orchestrate` and `meta-orchestrate`
binaries. Its captured client stdout was:

```text
PathLock.{alpha [/tmp/.tmpVkNW36/first] (first reservation)}
  -> PathLockRegistered.{alpha [/tmp/.tmpVkNW36/first] (first reservation)}
PathLock.{alpha [/tmp/.tmpVkNW36/elsewhere] (duplicate reservation)}
  -> PathLockRegistrationRejected.{{alpha [/tmp/.tmpVkNW36/elsewhere] (duplicate reservation)} DuplicateActiveName.{alpha [/tmp/.tmpVkNW36/first] (first reservation)}}
PathLock.{beta [/tmp/.tmpVkNW36/first/nested] (overlapping reservation)}
  -> PathLockRegistrationRejected.{{beta [/tmp/.tmpVkNW36/first/nested] (overlapping reservation)} PathOverlap.{/tmp/.tmpVkNW36/first/nested {alpha [/tmp/.tmpVkNW36/first] (first reservation)}}}
PathLockRelease.{alpha}
  -> PathLockReleased.{alpha}
PathLock.{alpha [/tmp/.tmpVkNW36/first] (first reservation)}
  -> PathLockRegistered.{alpha [/tmp/.tmpVkNW36/first] (first reservation)}
Configure.{/tmp/.tmpVkNW36/orchestrate.sema /tmp/.tmpVkNW36/ordinary.sock /tmp/.tmpVkNW36/meta.sock}
  -> Configured.{/tmp/.tmpVkNW36/orchestrate.sema /tmp/.tmpVkNW36/ordinary.sock /tmp/.tmpVkNW36/meta.sock}
```

The test passed. The temporary directory name is runtime-specific; the captured
sequence proves registration, closed duplicate-name and overlap refusals,
release, re-registration after release, and a Configure round trip through
separate sockets.

## Gates — 2026-08-25

Method: probe.

- Red before replacement: `cargo test --test live_nexus` could not compile the
  old lane/workflow implementation against the retired contract surface (156
  errors). The test was retained as the behavioral replacement target.
- Green: `cargo fmt --check`; `cargo check`; `cargo test --offline` (three
  durable-store unit tests and the live process test); and
  `cargo clippy --offline --all-targets -- -D warnings`.
- Green: `nix flake check --no-build -L` evaluated every Linux build, test,
  live-nexus, doc, format, and Clippy check.
- Green after an upstream contract packaging repair:
  `nix build .#checks.x86_64-linux.live-nexus --no-link -L` completed using the
  configured remote builder. The initially observed immutable-vendor failure
  was fixed in the pinned interface patch revisions by generating into
  `OUT_DIR` and byte-checking committed projections instead of writing source.
