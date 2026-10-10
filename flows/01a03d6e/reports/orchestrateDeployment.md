# orchestrate deployment

## Final settled state

Orchestrate Nexus 0.24 is at `5b495422`; meta-signal-orchestrate 0.11 is at
`d4dd208c`. The Orchestrate release and its bead evidence (`a4d8f7dc`) are
landed. Home is at `905dfdd9`, CriomOS is at `3d7c8537`, and Primary consumes
Curriculum pin `3a5e8ba`, which contains the Nexus wording and fail-closed edit
coordination. Primary's generated companions and checks are green.

Lojix deployments 64 and 65 both reached terminal success. The live service,
Sema store, sockets, and legacy surfaces remain untouched. The release tests
prove persistence of changed Meta Configure values; that behavior was not
mutated live.

## Evidence classes

### Source and release revisions

Revision evidence identifies the source state: meta-signal-orchestrate 0.11 at
`d4dd208c`; Orchestrate Nexus 0.24 at `5b495422`; bead evidence at `a4d8f7dc`;
Home at `905dfdd9`; CriomOS at `3d7c8537`; and Curriculum pin `3a5e8ba`.

### Generated consumer

Primary's generated companions and its generated-skills-current checks are
green against the Curriculum pin. This is generated-consumer evidence, not a
claim that the live service was changed.

### Deployment terminal state

Lojix deployment records 64 and 65 are terminal successes. Admission and
terminal state are kept distinct here; the claim is only the reported terminal
outcome.

### Live-state boundary

The live service, Sema store, sockets, and legacy surfaces were left untouched.
The successful release-test persistence result for changed Meta Configure
values is therefore separate from live state.

### Coordination

With `XDG_RUNTIME_DIR` explicitly unset, this closeout reserved the complete
write set and received:

```text
PathLockRegistered.{RootFlowCloseout [/home/li/primary/flows/01a03d6e/log.md /home/li/primary/flows/01a03d6e/reports/orchestrateDeployment.md] (close root flow documentation)}
```

After the commit and push, the paired unset-XDG release returned:

```text
PathLockReleased.{RootFlowCloseout}
```

## Architecture and rollout

```text
  source and consumer revisions
  meta-signal 0.11  d4dd208c
  Orchestrate 0.24  5b495422   bead evidence  a4d8f7dc
  Home             905dfdd9   CriomOS          3d7c8537
  Curriculum pin   3a5e8ba
             |
             v
  Primary generated companions + green checks
             |
             v
  Lojix deployment 64  -- terminal success -->  deployment 65
                                                     |
                                             terminal success
                                                     |
                                                     v
                  live service / Sema store / sockets / legacy surfaces
                                      untouched
```

```text
  unset XDG_RUNTIME_DIR
             |
             v
  PathLockRegistered
             |
  document -> commit -> push
             |
  PathLockReleased
```

## Open follow-ups

Only these follow-ups remain separate from the completed deployment: broader
removal of legacy Dotos file surfaces, and stale non-generated Primary
architecture documentation.

## Sources

- `meta-signal-orchestrate` 0.11, commit `d4dd208c`.
- Orchestrate Nexus 0.24, commit `5b495422`; bead evidence commit `a4d8f7dc`.
- CriomOS-home, commit `905dfdd9`.
- CriomOS, commit `3d7c8537`.
- Curriculum pin `3a5e8ba`, including Nexus and fail-closed edit coordination.
- Primary generated companions and generated-skills-current checks.
- Lojix terminal deployment records 64 and 65.
- Orchestrate release-test evidence for changed-value Meta Configure persistence.
- This closeout's unset-XDG `PathLockRegistered` and `PathLockReleased` replies.
