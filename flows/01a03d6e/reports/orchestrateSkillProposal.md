# Orchestrate operations skill

## Deployment result

The ordinary-only Orchestrate skill is deployed. Meta material was excluded by
the living ruling.

Deployment evidence:

- Curriculum source: `abd92790`.
- `curriculum-deploy` fixture: `671230f`.
- Primary: `73db7b4e`.
- Generated/Checked: `36/27`.
- Remote gates: passed.
- Live checks with `XDG_RUNTIME_DIR` unset: register succeeded, duplicate
  registration was rejected, and release succeeded.

## Current boundary

There is no operation to list or observe active PathLocks. The current
`orchestrate/README.md` and `orchestrate/ARCHITECTURE.md` are partial. The
legacy `/home/li/primary/orchestrate/AGENTS.md` is stale for the deployed
surface.

## Exact deployed Curriculum sources

### `skills/orchestrate.md`

```markdown
---
description: An ordinary Orchestrate PathLock request must be constructed, submitted, or interpreted.
dependencies: []
---

Use `orchestrate` for ordinary requests. The client takes exactly one inline Datom value and no flags. The installed wrapper supplies `ORCHESTRATE_SOCKET`; a direct client binary requires it.

Register a path lock:

    orchestrate 'PathLock.{<name> [<absolute-path> ...] (<description>)}'

`PathLockRegistered` accepts it. `PathLockRegistrationRejected` carries `DuplicateActiveName` or `PathOverlap`. An empty path set, non-absolute path, `..`, or repeated normalized path currently fails without a typed reply.

Release a path lock by name:

    orchestrate 'PathLockRelease.{<name>}'

`PathLockReleased` accepts it. `PathLockReleaseRejected` carries `UnknownActiveName`.

The current contract has no operation to list or observe active PathLocks. Treat a parsing, environment, transport, framing, or missing-reply failure as a failed operation.
```

### `skills/edit-coordination.md`

```markdown
---
description: Another agent may be writing the same paths.
dependencies: [orchestrate]
---

Reserve the complete write set with `PathLock` before editing.

Edit only after receiving `PathLockRegistered`. On `PathLockRegistrationRejected` or a client failure, report the failure and do not edit.

Release the reservation with `PathLockRelease` when editing ends. Read the typed release reply.
```

## Sources

- `/git/github.com/LiGoldragon/Curriculum` at `abd92790` — exact deployed source bodies.
- `/git/github.com/LiGoldragon/curriculum-deploy` fixture `671230f` — generation and check evidence.
- `/home/li/primary` at `73db7b4e` — deployed Primary and generated/checked evidence.
- Live Orchestrate register, duplicate, and release checks with `XDG_RUNTIME_DIR` unset.
