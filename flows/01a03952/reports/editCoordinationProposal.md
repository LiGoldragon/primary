# Edit coordination proposal

The replacement skill should expose only the new ordinary Nexus contract: reserve the complete write set, release it by name, and read the typed reply.

```markdown
---
description: Another agent may be writing the same paths.
dependencies: []
---

Reserve the complete write set before editing.

    ORCHESTRATE_SOCKET=<ordinary-socket> orchestrate \
      'PathLock.{<name> [<absolute-path> ...] (<description>)}'

Release it when finished.

    ORCHESTRATE_SOCKET=<ordinary-socket> orchestrate \
      'PathLockRelease.{<name>}'

Pass exactly one Datom value and read the typed reply.
Edit only after `PathLockRegistered`; otherwise report that no reservation was obtained.
```

This removes the former lane, session, discipline, recovery, Claim, Retire, and meta-client lifecycle. The meta client configures the Nexus and does not participate in ordinary path reservation.

The final sentence is a proposed strict failure policy, not a recovered psyche ruling. Flow 01a03603 continued disjoint work when the old coordination daemon was absent; it did not settle the general meaning of refusal or unavailability in the new Nexus.

The CLI has no ordinary-socket default. Before deployment, an authoritative ordinary socket path must be added to `SKILL_VARIABLES.md` and supplied as `ORCHESTRATE_SOCKET`; the present deployment still targets the retired interface.

## Sources

- Flow 01a03603: `log.md`, `reports/orchestrateNexus.md`, `reports/decisionLedger.md`, and `witnesses/orchestrateNexus.md`
- Flow aa4c7747: `vision/orchestrate.md`
- Flow 01a02a34: `vision/pathLocks.md` and `reports/pathLockEpic.md`
- `/git/github.com/LiGoldragon/Curriculum/skills/edit-coordination.md`
- `/git/github.com/LiGoldragon/orchestrate/README.md`, `ARCHITECTURE.md`, `src/bin/orchestrate.rs`, and `src/store.rs`
- `/git/github.com/LiGoldragon/signal-orchestrate/ethos/signal.ethos`
- `/home/li/primary/SKILL_VARIABLES.md`
