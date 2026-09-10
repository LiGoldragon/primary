# Current Nexus compliance gaps

This audit is scoped to the releases and source trees inspected on 2026-09-10.
It supersedes any closure wording in earlier chronological reports for the
invariants below. It does not alter the live service or protected deployment
configuration.

Lojix's Horizon consumer and Nexus-shape gaps are closed at Horizon 0.8.0
`e4871220` and Lojix 1.0.0 `e2c7bdc5`, followed by the trait-surface correction
in Lojix 1.0.1 `b8f7a8cc`. Orchestrate and Ethos Zero remain open below.

## Orchestrate

The published Orchestrate 0.31.0 split proves separate daemon, ordinary client,
and meta client packages, direct portable Signal framing, no polling, and a
Datom-free daemon dependency graph. Source inspection nevertheless found three
open authority requirements:

- The daemon runs two Tokio listener futures over `Arc<Mutex<OrchestrateStore>>`.
  Its manifest has no Kameo dependency, so effect processing is not driven by
  Kameo actors.
- Durable configuration contains socket paths only. No persistent record states
  whether privileged Configure has ever occurred, and a newly created store
  immediately adopts defaults.
- The ordinary generated Query exposes Lock, Release, and Observe only.
  Configure exists only on the meta contract, so ordinary Configure is not
  available while configuration is unset. No explicit meta-only reversal
  operation exists.

These are required implementation work before the runtime can be described as
conforming to the supplied Nexus authority. The live service remains unchanged.

## Ethos Zero

Ethos Zero 6.1.6 is a generated Library plus a direct `ethos-zero` command. Its
manifest and source contain no daemon package, ordinary/meta Unix sockets,
separate socket clients, Kameo actors, or persistent Nexus state. With no
arguments the command prints its own authored contract; with a Generate request
it performs generation in the invoking process.

The flow's earlier landing reports do not explicitly defer an Ethos Nexus.
Therefore they cannot substantiate the supplied behavior in which generation is
requested from a long-running Ethos Zero daemon. A design and implementation
must define the ordinary/meta Signal contracts and daemon/client boundaries
from the existing Nexus authority without inventing new grammar.

## Closed active consumer edge

The audit found that Lojix's active Horizon input mode pinned Horizon 0.6.0,
which directly used Ethos Zero 5.0, Datom 0.21, and Protos 0.26. Horizon 0.8.0
now emits final generated types, and Lojix carries an already actualized
`HorizonDefinition` over its data-only Signal. Text decoding remains on the
client/offline side. Lojix now has separate Nexus, client, and offline-tool
packages; Kameo processing; persistent desired configuration and the exact
meta-Configure marker transitions; and a copy-only historical-store migration.

## Sources

- `/git/github.com/LiGoldragon/orchestrate/Cargo.toml` and `nexus/src/main.rs`,
  Orchestrate 0.31.0 release `1bc55af1`.
- `/git/github.com/LiGoldragon/signal-orchestrate/ethos/signal.ethos`, ordinary
  Signal 1.0.4 release `0efc9fda`.
- `/git/github.com/LiGoldragon/meta-signal-orchestrate/ethos/signal.ethos`, meta
  Signal 1.0.0 release `7d81bd96`.
- `/git/github.com/LiGoldragon/ethos-zero/Cargo.toml`, `src/main.rs`, and
  `src/lib.rs`, Ethos Zero 6.1.6 release `4695ee0c`.
- `/git/github.com/LiGoldragon/lojix/Cargo.toml`, `src/schema_runtime.rs`, and
  `src/runtime_model.rs`, pre-migration Lojix release `cf231859`.
- `/git/github.com/LiGoldragon/horizon-rs/Cargo.toml`, `lib/Cargo.toml`,
  `lib/src/projection.rs`, and `lib/ethos/horizon.ethos`, active Horizon 0.6.0
  release `05879e7c`.
- `/git/github.com/LiGoldragon/horizon-rs`, Horizon 0.8.0 `e4871220`, and
  `/git/github.com/LiGoldragon/lojix`, Lojix 1.0.0 `e2c7bdc5` plus the 1.0.1
  trait-surface correction `b8f7a8cc`, which close the active edge and Lojix
  Nexus invariants at those revision scopes.
- `Vision/nexus.md` and the flow's authoritative Nexus statements for actor
  effects, initial ordinary configuration, durable meta-configuration state,
  and meta-only reversal.
