# Orchestrate Nexus realization

## Result

Orchestrate is now a 0.22.0 durable PathLock Nexus. It replaces the retired
lane/claim/workflow/upgrade runtime with one daemon-owned Sema store, separate
ordinary and meta Unix sockets, and two one-argument clients. The live proof
starts the real daemon and drives both clients through registration, duplicate
and overlapping-path rejection, release, re-registration, and meta Configure.

## Decisions

- The daemon, not either client, owns all durable state. Clients translate one
  concrete Dotos carrier to or from a generated framed Signal value only.
- Locks reserve unique active names and normalized absolute paths. Duplicate
  active names and overlapping active paths are generated typed refusals;
  release makes the row available for registration again.
- Startup is one URL-safe-unpadded-base64 generated Configure frame. This is an
  implementation decision for argv's inability to carry arbitrary NUL bytes;
  the socket boundary remains binary Signal.
- Live Configure accepts the persisted configuration. A changed store is
  `StorePathImmutable`; another change is `InvalidConfiguration`. The POC
  never silently switches a durable store or rebinds sockets while serving.
- The meta executable is `meta-orchestrate` only. Component-specific
  restoration evidence is more specific than the generic naming convention;
  no compatibility alias was introduced.
- The generated ordinary/meta contracts are mandatory. The consumer pins their
  immutable-source-safe releases (`signal-orchestrate` v0.16.1 and
  `meta-signal-orchestrate` v0.10.1); no local wire fallback exists.
- Version 0.22.0 reconciles the already-landed 0.21.0 PathLock carrier with
  the additional Release, Configure, runtime, client, and durable proof work.

## Evidence and gates

The full actual-binary stdout sequence, commands, and pre-implementation red
state are in the companion witness. Green gates are `cargo fmt --check`,
`cargo check`, `cargo test --offline`,
`cargo clippy --offline --all-targets -- -D warnings`, Nix flake evaluation,
and remote-builder `nix build .#checks.x86_64-linux.live-nexus --no-link -L`.

The Nix live check initially found that the interface crates wrote generated
source under a read-only vendored directory. That upstream defect was repaired
before landing by the contract owners; their patched revisions generate in
`OUT_DIR` and verify the committed source projection. The final remote build
is green.

## Sources

- `flows/01a03603/witnesses/orchestrateNexus.md`
- `flows/01a02a34/reports/pathLockEpic.md`
- `flows/01a02a34/reports/orchestrateSituation.md`
- `flows/01a02fd5/vision/interfaces.md`
- `flows/01a02fd5/reports/metaOrchestrateRestoration.md`
- `flows/e06e4c07/vision/nexus.md`
- `flows/98fbfa47/vision/metaSignalNotOptional.md`
- `psyche-raw/Vision/setupIndependentInterfaces.md`
