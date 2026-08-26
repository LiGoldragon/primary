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

`A deployed Orchestrate Nexus request must be constructed, submitted, or interpreted for ordinary path locking or meta socket configuration.`

## Exact proposed Curriculum source

Proposed file: `Curriculum skills/orchestrate.md`

```markdown
---
description: A deployed Orchestrate Nexus request must be constructed, submitted, or interpreted for ordinary path locking or meta socket configuration.
dependencies: []
---

Use the installed `orchestrate` client for ordinary requests and
`meta-orchestrate` for meta requests. Each client takes exactly one positional
Datom value and no flags; pass the value inline and read the printed typed
reply. The installed wrappers provide `ORCHESTRATE_SOCKET` and
`ORCHESTRATE_META_SOCKET`; direct client binaries require those variables.

Register a path lock:

    orchestrate 'PathLock.{<name> [<absolute-path> ...] (<description>)}'

The name, nonempty path vector, and description are one `PathLock` value.
`PathLockRegistered.{...}` accepts it. `PathLockRegistrationRejected.{...}`
is the typed refusal for a duplicate active name or an overlapping active
path, when the running Nexus returns that reply.

Release a path lock by name:

    orchestrate 'PathLockRelease.{<name>}'

`PathLockReleased.{...}` accepts it. `PathLockReleaseRejected.{...}` reports
an unknown active name.

Change the socket configuration through the meta socket:

    meta-orchestrate 'Configure.{<ordinary-socket> <meta-socket>}'

`Configured.{...}` confirms the request. The current Nexus persists the new
configuration for its next start and does not rebind a running Nexus.
`ConfigurationRejected.{...}` is a contract-carried refusal, but the current
runtime does not emit it; preserve it when interpreting a future deployed
reply.

Text parsing, transport, and current runtime validation failures can terminate
the client without a typed reply. A successful process exit alone does not
mean that a request was accepted; use the printed typed carrier when one is
present.
```

## Exact proposed edit-coordination replacement

Proposed file: `Curriculum skills/edit-coordination.md`

```markdown
---
description: Another agent may be writing the same paths.
dependencies: [orchestrate]
---

Reserve the complete write set with the ordinary `PathLock` operation before
editing.

Edit only after receiving `PathLockRegistered`. A typed registration refusal,
text or transport failure, or missing reply obtains no reservation; report it
and do not edit.

Release the reservation with `PathLockRelease` when editing ends. Read the
typed `PathLockReleased` or `PathLockReleaseRejected` reply.

Use `orchestrate` for the client environment and exact Datom form.
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
