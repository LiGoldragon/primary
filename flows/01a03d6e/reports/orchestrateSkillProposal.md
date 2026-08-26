# Orchestrate operations skill proposal

## Boundary

A dedicated `orchestrate` skill is the best owner for invoking and interpreting
the deployed Orchestrate Nexus clients. It is an operation reference, not an
architecture guide: `nexus` remains responsible for designing or changing the
long-running Nexus, its sockets, contracts, storage, and process boundary.
It is also not the policy owner for when a writer must reserve paths:
`edit-coordination` remains responsible for that decision and depends on this
operation reference for the concrete call and reply vocabulary.

The trigger is deliberately operation-shaped and does not describe either
neighbour's situation:

`A deployed Orchestrate Nexus request must be constructed, submitted, or interpreted.`

## Exact proposed Curriculum source

Proposed file: `Curriculum skills/orchestrate.md`

```markdown
---
description: A deployed Orchestrate Nexus request must be constructed, submitted, or interpreted.
dependencies: []
---

Use `orchestrate` for ordinary requests and `meta-orchestrate` for meta requests. Each client takes exactly one inline Datom value and no flags. Installed wrappers supply `ORCHESTRATE_SOCKET` and `ORCHESTRATE_META_SOCKET`; direct client binaries require them.

Register a path lock:

    orchestrate 'PathLock.{<name> [<absolute-path> ...] (<description>)}'

`PathLockRegistered` accepts it. `PathLockRegistrationRejected` carries `DuplicateActiveName` or `PathOverlap`. An empty path set, non-absolute path, `..`, or repeated normalized path currently fails without a typed reply.

Release a path lock by name:

    orchestrate 'PathLockRelease.{<name>}'

`PathLockReleased` accepts it. `PathLockReleaseRejected` carries `UnknownActiveName`.

Change the stored socket configuration:

    meta-orchestrate 'Configure.{<ordinary-socket> <meta-socket>}'

`Configured` confirms persistence for the next Nexus start; a running Nexus does not rebind. `ConfigurationRejected` with `InvalidConfiguration` exists in the wire contract, but the current runtime does not emit it.

The current contract has no operation to list or observe active PathLocks. Treat a parsing, environment, transport, framing, or missing-reply failure as a failed operation.
```

## Exact proposed edit-coordination replacement

Proposed file: `Curriculum skills/edit-coordination.md`

```markdown
---
description: Another agent may be writing the same paths.
dependencies: [orchestrate]
---

Reserve the complete write set with `PathLock` before editing.

Edit only after receiving `PathLockRegistered`. On `PathLockRegistrationRejected` or a client failure, report the failure and do not edit.

Release the reservation with `PathLockRelease` when editing ends. Read the typed release reply.
```

This preserves `edit-coordination`'s trigger and its reserve-before-edit
policy, changes its dependency to `[orchestrate]`, and removes its duplicated
CLI syntax, environment detail, and reply catalogue. The proposed
`orchestrate` source owns those facts exactly once.

## Current operations audit

The deployed source and generated Ethos contracts witness this closed surface:

| socket | request | current reply carriers |
| --- | --- | --- |
| ordinary | `Register(PathLock)`; CLI carrier `PathLock.{...}` | `PathLockRegistered`, `PathLockRegistrationRejected` |
| ordinary | `Release(PathLockRelease)`; CLI carrier `PathLockRelease.{...}` | `PathLockReleased`, `PathLockReleaseRejected` |
| meta | `Configure(Configure)`; CLI carrier `Configure.{...}` | `Configured`, `ConfigurationRejected` |

The `ConfigurationRejected` type and `InvalidConfiguration` variant are in the
meta contract, but the current store handler always returns `Configured` for a
decoded `Configure`; the proposal labels this distinction rather than claiming
an unreachable branch is live. A malformed Datom value, missing socket
environment, failed connection, frame failure, or current store validation
failure can fail at the text/transport/process boundary instead of producing a
typed refusal.

The final documentation verdict is partial for the current
`orchestrate/README.md` and `orchestrate/ARCHITECTURE.md`: they describe the
replacement clients and core boundaries, but are not a complete operation
reference. `primary/orchestrate/AGENTS.md` is wholly stale for this replacement;
its lane, claim, worktree, observe, and query catalogue does not describe the
current deployed surface. The current surface is exactly ordinary
`Register(PathLock)` and `Release(PathLockRelease)`, meta `Configure(Configure)`,
and no operation to list or observe active PathLocks.

Current audit pins are Orchestrate package `0.24.0` at release `5b495422`,
`meta-signal-orchestrate` `0.11` at `d4dd208c`, the Orchestrate Cargo pin for
`signal-orchestrate` at `d23fb6430eda`, and the Primary Curriculum input at
`3a5e8ba`. These identify the inspected source and deployment inputs; they do
not authorize changing them here.

The following forms are present in older workspace protocol documents or
historical Orchestrate reports, not in the current deployed operation source:

`Claim`, lane `Release`, `Handoff`, `Observe`, `Query`, lane `Register`, lane
`Retire`, `RequestWorktree`, `ConcludeWorktree`, `RegisterWorktree`,
`RefreshWorktreeIndex`, `ArchiveWorktree`, `Refresh`, `MintAgentIdentity`,
`LaunchAgent`, and `SendOrchestratorMessage`, together with the former
`PERSONA_ORCHESTRATE_*` variables and bootstrap forms.

**Awaiting operations audit:** none of those legacy forms has a current
deployed source witness. Do not add their syntax to either proposed skill
until a fresh operations audit identifies a deployed contract and executable
that accepts it. The existing `primary/orchestrate/AGENTS.md` broad operation
catalogue is therefore a stale documentation surface to correct separately;
this proposal does not silently treat it as authority.

## Dependency and generated-consumer implications

`orchestrate` has no dependency: it is a self-contained operation reference and
must not depend on `edit-coordination`, `nexus`, or deployment skills. The only
new edge is `edit-coordination -> orchestrate`; the existing Spirit,
psyche, flow, and deployment edges remain unchanged, and the graph stays
acyclic.

Curriculum currently contains 35 skill sources. Adding this source makes 36.
The next `curriculum-deploy` generation should therefore add
`.agents/skills/orchestrate/SKILL.md` and `.claude/skills/orchestrate/SKILL.md`.
Changing `edit-coordination` changes both generated companions. The role data
does not change: the current 27 role packets and `roles.datom` remain intact,
so no role packet should change merely because this independently invocable
operation reference is added. The generated-skills-current check must be run
after the living approves and lands the Curriculum changes; no generated tree,
manifest, or code change is part of this proposal.

The proposal hardcodes no user, host, or socket path. `ORCHESTRATE_SOCKET` and
`ORCHESTRATE_META_SOCKET` are stable client variable names; the installed Home
wrappers supply the setup-specific values.

## Approval still required

The living must approve the new Curriculum source, the dependency edge, and
the fail-closed edit-coordination wording before an implementation flow edits
Curriculum or regenerates consumers. This report is only the exact proposal;
it has not edited those sources or generated trees.

## Sources

- `/git/github.com/LiGoldragon/orchestrate/README.md`, `ARCHITECTURE.md`, `src/bin/orchestrate.rs`, `src/bin/meta_orchestrate.rs`, `src/store.rs`, and `src/transport.rs` — current client, reply, persistence, and failure behavior.
- `/git/github.com/LiGoldragon/signal-orchestrate/ethos/signal.ethos`, `README.md`, and `tests/generated_contract.rs` — ordinary request/reply vocabulary and exact Datom carriers.
- `/git/github.com/LiGoldragon/meta-signal-orchestrate/ethos/signal.ethos`, `README.md`, `ARCHITECTURE.md`, and `tests/generated_contract.rs` — meta request/reply vocabulary and exact `Configure` carrier.
- `/git/github.com/LiGoldragon/Curriculum/skills/edit-coordination.md`, `skills/nexus.md`, `skills/skill-designing.md`, and `ARCHITECTURE.md` — authored skill boundary, description, dependency, and source rules.
- `/git/github.com/LiGoldragon/curriculum-deploy/README.md`, `ARCHITECTURE.md`, `src/runtime.rs`, and `tests/runtime.rs` — generated companion and role-packet counts and target surfaces.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/orchestrate.nix` and `UPGRADES.md` — wrapper-provided socket variables and replacement deployment boundary.
- `/home/li/primary/flows/01a03d6e/vision/orchestrateDeployment.md` and `vision/nexus.md` — living direction to replace the old deployment, use the new PathLock Nexus, keep meta configuration, and defer an ordinary Configure operation.
- `/home/li/primary/flows/aa4c7747/vision/orchestrate.md` and `/home/li/primary/flows/01a03952/reports/editCoordinationProposal.md` — prior path-lock and edit-coordination proposal evidence.
- `/home/li/primary/orchestrate/AGENTS.md` and `/home/li/primary/reports/orchestrate-current-functionality-visualization-2026-07-28.md` — historical broad operation catalogues explicitly treated above as stale pending audit.
