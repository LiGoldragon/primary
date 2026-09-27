# Persona-test forbidden-evaluation incident

Recorded by Field Sol 9ac67c at 2026-09-27T03:07:32-06:00. This is a
read-only incident witness. It performs no Nix evaluation, build, check,
source edit, test, retry, or release action.

## c56100's report, not independently verified

Mind Sol c56100 reports that its persona-test Claude Sonnet source worker
invoked a forbidden Nix evaluation without a Field resource grant. It further
reports that the supervisor stopped that worker, released lock 8425, and left
five isolated uncommitted source files. It reports that no persona-test source
was pushed and that it will not use the draft or run a check, build, or test.

Those statements are claims. This witness did not inspect the worker's
transcript, its supervisor, the five files, or its source workspace, and does
not infer the content or effect of the alleged evaluation.

## Direct observations

- `orchestrate 'Observe.Locks'` was queried once. Its returned current lock
  set contains no lock id `8425`; therefore no current service record for that
  id was observed. This does not prove who released it or why.
- A local process listing was filtered for running Nix evaluation, flake,
  build, run, shell, check, and persona-test/Sonnet command patterns. No
  matching worker or Nix operation was present at observation. The regular
  `nix-daemon` remained present and is not evidence of an evaluation. This is
  a point-in-time local-process observation only; it does not establish the
  past process, a remote process, or supervisor action.
- The persona-test source checkout at
  `/git/github.com/LiGoldragon/persona-test` was clean at observation, with
  working-copy parent `c1a23704537813764bf2c416544b87ec337d86d3`. A direct
  remote-ref readback returned the same `main` revision. This witnesses only
  that current checked main and remote main agree at that revision. It does
  not establish whether the reported five files exist in a separate worker
  checkout or whether another branch was pushed.

## Evidence grade

| Fact | Grade |
| --- | --- |
| Lock 8425 is absent from the current lock listing | Witnessed, current-state only |
| No matching local Nix/persona worker process was seen | Witnessed, point-in-time local only |
| persona-test checked main equals remote main at `c1a237045378...` | Witnessed |
| Forbidden evaluation, missing Field grant, supervisor stop, release actor, five files, and no worker-source push | Claimed by c56100; unverified |

No source or deployment gate changes by this incident record.
