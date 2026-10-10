# Ouranos stale deployment diagnosis

Method: read-only ordinary Lojix queries, service status/journal observation,
transcript search, and inspection of the installed 0.17.5 source. No owner
request, deployment submission, activation, build, copy, reboot, daemon
restart, store reset/edit, or runtime mutation was performed.

## Durable records and complete event history

At marker `(687 687)`, `Query.ByNode.(goldragon ouranos None)` returned two
nonterminal CompleteHost deployment records:

- deployment 5: `Host.ActivateNow`, admission/state marker `(62 62)`, phase
  `Copying`, no terminal marker or outcome;
- deployment 7: `Host.ActivateNow`, admission/state marker `(98 98)`, phase
  `Copying`, no terminal marker or outcome.

The full `Query.ByEventLog.(1 700)` history contains the corresponding phase
events. Deployment 5 is `Submitted` at event 9/state marker 62, `Building` at
event 10/70, and `Copying` at event 11/79. Deployment 7 is `Submitted` at
event 14/98, `Building` at event 15/106, and `Copying` at event 16/115. The
numbers 62 and 98 in the current node reply are state/admission markers, not
event-log positions.

Later deployments, including Ouranos user-environment deployments 8, 9, and
11 through 27, and Zeus deployments 28 through 30, have terminal success or
failure events while 5 and 7 remain nonterminal. This is direct evidence that
the existence of these durable records did not impose a global durable-record
admission block.

The ordinary `ByDeployment` and `ByGeneration` forms were not usable for
additional read-only detail: unparenthesized forms were client parser rejects,
and parenthesized forms reached the daemon but ended in frame EOF. The daemon
journal records the corresponding worker panic at `src/adapters.rs:539` while
decoding the verified ordinary ingress shape. `ByNode` and `ByEventLog` remain
the successful public observations. The store could not be independently
opened because the running daemon held its lock.

No prior transcript or flow witness was found that records creation or outcome
of IDs 5 or 7 beyond this durable event history.

## 0.17.5 admission and recovery semantics

The installed daemon is `/nix/store/kcg9m2zi17phw11w4vkjz1ffa41l450n-lojix-0.17.5`.
The inspected source at `/git/github.com/LiGoldragon/lojix` shows:

- admission is owned by the daemon's `DeployJobs` actor, with
  `MAXIMUM_CONCURRENT_DEPLOYS = 8` and an in-memory `active_count`; only when
  that count is at capacity does it create a typed `DeploymentInFlight`
  rejection;
- startup enumerates private persisted deploy-job rows. `Submitted`,
  `Building`, `Built`, and `Copying` rows are `RestartPipeline` candidates;
  `Activating` rows enter activation-unit polling/self-switch reconciliation;
  terminal rows are retracted. A successfully resumed row increments
  `active_count`; a row that cannot be resumed is retained, not silently
  terminalized;
- `Copying` resume restores the durable cursor/phase receipt and proceeds from
  the activation stage. The source describes closure copying as idempotent;
  the persisted cursor therefore does not mean a second public submission;
- startup self-switch reconciliation applies only to qualifying
  self-targeted `ActivateNow` rows at `Activating`, and only when the live
  system profile exactly matches the persisted closure. It is not the path for
  these `Copying` rows;
- the actor does not derive admission from the number of public nonterminal
  deployment records. Thus records 5 and 7 do not by themselves block a new
  deployment. If both private rows were successfully resumed, they could
  consume two of eight actor slots; actual private-row presence, resume result,
  and current `active_count` are not exposed by the ordinary interface.

The source comment saying pre-activation rows are dropped so they cannot wedge
the cap conflicts with the adjacent implementation, which resumes
`RestartPipeline` rows. The implementation, not that comment, is the evidence
used here.

## Deployment, job, generation, and supported operations

A deployment record is the public durable correlation/lifecycle record. A
private `DeployJob` row is a separate resume convenience row keyed by the
deployment ID and normally retracted on terminal completion. A live generation
is the activated system/user-environment generation and has its own live-set
row and GC-root retention. IDs 5 and 7 happen to appear in both the deployment
and generation vectors here; numeric equality does not make the records the
same object.

The owner wire surface has Deploy, Pin, Unpin, Retire, and Test; there is no
typed Cancel or deployment-record retirement operation. `Retire` operates on a
generation's GC root, not on a deployment record or private deploy-job row,
and must not be used as a stale-deployment cancellation. Direct store
retraction/reset is outside the allowed scope and would not be a supported
ordinary resolution.

## Gate

The no-unrelated-active-job gate remains closed. The live evidence says stale
records do not globally block admission, but does not establish that the two
jobs are inactive, nor that actor capacity is available at the instant of a
future request. A safe continuation requires an explicitly approved,
supported read-only way to establish private job/activity state, or an
explicitly approved recovery/cancellation design. Until then, do not submit a
new Ouranos deployment and do not retire generations 5 or 7 as a proxy for
canceling deployments.

## Sources

- `/git/github.com/LiGoldragon/lojix/src/daemon.rs`
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs`
- `/git/github.com/LiGoldragon/lojix/src/lib.rs`
- `/git/github.com/LiGoldragon/lojix/src/adapters.rs`
- `/git/github.com/LiGoldragon/lojix/README.md`
- `/git/github.com/LiGoldragon/lojix/ARCHITECTURE.md`
- successful live `Query.ByNode` and `Query.ByEventLog` responses described
  above
