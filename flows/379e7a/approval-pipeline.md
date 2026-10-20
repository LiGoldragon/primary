# Approval pipeline

When the living approves a vision, Flow carries it through four steps with
no act of his: the approval is landed in its psyche module, the modules
every flow loads are deployed, every running flow loaded with a changed
module is retrained, and the change is handed to the flow that implements
it. Each step leaves a witness in Flow's store, and a failed step is
reported to Psyche core Secondary.

```
 living approves (book comment)
          |
          | relayed to
          v
 +---------------------------+
 | Psyche core Secondary     |
 +---------------------------+
          |
          | commits the landing to
          v
 +---------------------------+
 | psyche-context main       |
 +---------------------------+
          |
          | ref change wakes
          v
 +---------------------------+
 | Flow Nexus: landing row   |
 +---------------------------+
    |            |            |
    | runs       | marks      | queues Order to
    v            v            v
 +--------+  +----------+  +----------------+
 | deploy |  | changed  |  | Mind <topic>   |
 | binary |  | flows    |  | Secondary      |
 +--------+  +----------+  +----------------+
    |            |
    | witnessed  | at rest: pane closed,
    | by         | next wake fresh from
    v            v
 +---------------------------+
 | Curriculum: served rev    |
 +---------------------------+
          |
          | Result or failure Order to
          v
 +---------------------------+
 | Psyche core Secondary     |
 +---------------------------+
```

## Trigger

A landing is a commit that is on the context repository's `main` and
that the Curriculum Nexus does not serve yet. Flow watches the
repository's ref files (`refs/heads/main`, `packed-refs` and the remote
refs, in its common git directory) with the same file watch it uses for
transcripts: a change wakes it, no timer polls. When the Nexus starts, and
on every wake, it reads `main`, asks Curriculum which revision it serves,
and records one landing row per commit in `served..main`, oldest first. A
commit it has already recorded is not recorded again. The repository
checkout and the deploy executable are given to the Nexus in its Start
datom by the declarative deployment (CriomOS-home `criomosHome.flow`):

```
{ %t/flow/flow.sock %t/flow/flow-meta.sock %h/.local/state/flow-03521/flow.sema Some.{ /git/github.com/LiGoldragon/psyche-context /nix/store/…-context-deploy/bin/context-deploy } }
```

## Steps

| Step | Performed by | Witness | On failure |
|---|---|---|---|
| 1 Land | Psyche core Secondary, on the living's relayed approval | the commit on psyche-context main, with its reference lines | not observed by Flow (see unknowns) |
| 2 Deploy | Flow runs `context-deploy 'Deploy.{ Repository Commit }'` for the newest landing: the commit reaches the repository's origin main (fast-forward only), is pinned as psyche-context in CriomOS-home main, that Home is pinned in CriomOS main, and the declared Lojix host deploy of the node is submitted and followed to its terminal record | Curriculum's `ResolveSources` of a module of the repository names a revision that includes the commit | step recorded `Failed` with the deploy's answer; an Order to Psyche core Secondary; retried at the next change of main (a push included) and at Nexus start |
| 3 Retrain | Flow marks each live flow whose launch modules (their dependency closure, resolved to source paths through Curriculum) include a changed path; at the flow's next rest Flow closes its pane, records it Stopped, and the metaflow sleeps; queued work wakes a fresh flow composed from the deployed revision | the refresh-due mark, then the Stopped record of the refresh; the next wake's composition names the new revision | a flow with no launch profile is listed as not retrainable in the report; a close Herdr refuses stays marked and is retried at the next rest |
| 4 Implement | Flow queues one Order per changed module to Mind `<topic>` Secondary, or Mind core Secondary when no such metaflow is recorded; it carries the commit, the path and the changed lines | the queued request in the owner's metaflow, then its drain receipt | with neither metaflow recorded nothing is queued and the step is `Failed`; an Order to Psyche core Secondary |
| 5 Report | Flow queues a Result to Psyche core Secondary once steps 2 to 4 have settled for the landing | the queued request | — |

Step 3 runs only after step 2 is witnessed: a flow ended before the
deploy would wake into the old modules. Step 4 runs after step 2 as well,
so the implementer's own fresh flow carries the landed vision.

A refresh-due flow is closed only when Herdr shows it Idle or Done (a
Claude seat whose main turn ended while its background subflows run shows
Working and is left running), or, for Codex, when its app-server thread
rests. Its queued work is not drained into it; it wakes the fresh flow.

## Records

- `flow_nexus_landings`: one row per commit: the commit, its base, the
  changed paths, and each step's state (`Pending`, `Witnessed` with its
  witness, `Failed` with its reason), the flows marked for retraining with
  their state (`Marked`, `Ended`), the owners given implementation work,
  and whether the report was queued.
- `flow_nexus_refresh_due`: one row per flow due a refresh, with its
  cause (`Retrain` with the commit). The P4 threshold refresh adds its own
  cause to the same row and the same executor.

## Boundaries with the parallel work

- The module-deploy work generates the skill trees and Curriculum's cohort
  from the one psyche-context pin in CriomOS-home; `context-deploy` moves
  that pin and deploys it. Flow runs it and witnesses the result through
  Curriculum.
- The refresh-due row and its executor at rest are built here; the P4
  threshold work adds the `Threshold` cause and the message hold.

## Unknowns

1. Step 1 is a flow's act: Flow sees landings, not approvals. A relayed
   approval that is never landed is not detected. Closing it needs the
   comment relay to record approvals in Flow.
2. The harness skill trees are generated by Home from the same pin as
   Curriculum's cohort, so one deploy moves both; Flow witnesses only
   Curriculum's served revision, not the skill trees.
3. The host deploy request (`criomosHome.flow.landingDeployRequest`, a
   `lojix-meta` `Deploy.Host` datom with `@CRIOMOS_REVISION@`) is not
   declared: until the integrator of the ouranos deploy declares it, a
   landing is pinned in CriomOS-home and CriomOS and the deploy step fails
   with that reason. Whether the Lojix watch prints `Some.Succeeded` as
   context-deploy reads it is unwitnessed.
4. Ownership by topic is a rule (Mind `<topic>` Secondary, else Mind core
   Secondary), not a registry. A module whose implementer is in Field, or
   in no topic of its own name, reaches Mind core Secondary to route.
5. The Order and the reports are attributed to Psyche core Secondary,
   since `SentBy` has no variant for Flow itself; a Flow sender needs a
   flow-ethos change every Signal peer repins with.
6. A flow imported without a launch profile cannot be retrained: its wake
   has no modules to compose.
7. Whether a metaflow with nothing queued should be started fresh at once
   after its refresh, rather than at its next request.
8. A deploy that switches the Home generation restarts the Flow Nexus when
   the Flow package changed, ending context-deploy with it; the landing row
   carries the step across the restart, and the next start witnesses the
   deploy through Curriculum or runs it again.
9. A landing whose changed modules no live flow loads retrains nothing:
   today the topic metaflows do not load their `vision-<topic>` module, so a
   vision landing reaches only flows that list it.
