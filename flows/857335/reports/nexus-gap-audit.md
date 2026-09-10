# Current Nexus compliance gaps

This audit is scoped to the releases and source trees inspected on 2026-09-10.
It supersedes any closure wording in earlier chronological reports for the
invariants below. It does not alter the live service or protected deployment
configuration.

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

Ethos Zero 6.1.5 is a generated Library plus a direct `ethos-zero` command. Its
manifest and source contain no daemon package, ordinary/meta Unix sockets,
separate socket clients, Kameo actors, or persistent Nexus state. With no
arguments the command prints its own authored contract; with a Generate request
it performs generation in the invoking process.

The flow's earlier landing reports do not explicitly defer an Ethos Nexus.
Therefore they cannot substantiate the supplied behavior in which generation is
requested from a long-running Ethos Zero daemon. A design and implementation
must define the ordinary/meta Signal contracts and daemon/client boundaries
from the existing Nexus authority without inventing new grammar.

## Newly discovered active consumer edge

Lojix's active Horizon input mode pins Horizon 0.6.0. That release directly
uses Ethos Zero 5.0, Datom 0.21, and Protos 0.26 and exposes those tuple-shaped
contract values to Lojix. This is an active runtime edge through
`horizon_lib::decode`, not only a historical test dependency. Horizon therefore
belongs in the no-compat consumer migration before Lojix can close on the final
stack.

## Sources

- `/git/github.com/LiGoldragon/orchestrate/Cargo.toml` and `nexus/src/main.rs`,
  Orchestrate 0.31.0 release `1bc55af1`.
- `/git/github.com/LiGoldragon/signal-orchestrate/ethos/signal.ethos`, ordinary
  Signal 1.0.4 release `0efc9fda`.
- `/git/github.com/LiGoldragon/meta-signal-orchestrate/ethos/signal.ethos`, meta
  Signal 1.0.0 release `7d81bd96`.
- `/git/github.com/LiGoldragon/ethos-zero/Cargo.toml`, `src/main.rs`, and
  `src/lib.rs`, Ethos Zero 6.1.5 release `79efacaf`.
- `/git/github.com/LiGoldragon/lojix/Cargo.toml`, `src/schema_runtime.rs`, and
  `src/runtime_model.rs`, pre-migration Lojix release `cf231859`.
- `/git/github.com/LiGoldragon/horizon-rs/Cargo.toml`, `lib/Cargo.toml`,
  `lib/src/projection.rs`, and `lib/ethos/horizon.ethos`, active Horizon 0.6.0
  release `05879e7c`.
- `Vision/nexus.md` and the flow's authoritative Nexus statements for actor
  effects, initial ordinary configuration, durable meta-configuration state,
  and meta-only reversal.
