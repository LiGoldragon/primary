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
describes an ordinary, meta, and upgrade socket; an extensive lane/claim,
worktree, workflow, agent, router, and messenger state domain; and a six-path
positional daemon start interface. `Cargo.toml` pins a large set of those peer
contracts. `src/bin/orchestrate.rs` and `src/bin/meta_orchestrate.rs` accept
file-shaped component arguments and perform presentation behavior beyond a
direct typed text-to-Signal boundary.

The replacement POC deliberately does not retain that domain or its upgrade
socket. It retains only the Nexus boundaries that are independently grounded:
the daemon is the sole durable-state owner, ordinary and meta sockets use their
separate compiled Signal contracts, and text is confined to the two clients.

## Live POC

Pending generated interface integration and execution.
