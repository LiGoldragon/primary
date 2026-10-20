<!-- to-the-living:start -->
Presentation.{ «Tightening the ship: first report» }

# Tightening the ship: first report

The first cleanup pass gave back about 60 GiB, all of it on Ouranos. Nothing that holds unfinished work was touched.

| Host | Space reclaimed | State |
| --- | --- | --- |
| Ouranos | about 60 GiB | cleaned |
| Prometheus | nothing | checked, one leftover needs you |
| Zeus | nothing | checked, nothing to remove |
| Tiger, vm-testing, mirror-alpha, mirror-beta | unknown | could not be reached |
| Balboa | unknown | its name did not resolve |

## What was removed

Almost all of the space came from old Rust build caches left behind by two retired flows. Their records are kept; only the caches went.

The old Claude conversations of four retired flows were also deleted, about 4 MB. Their records were already committed, and no running program held them. Conversations that still carry an unfinished book, handover or pending judgment were kept. No Codex conversation qualified this time.

## Stateful changes found and replaced

On Ouranos, three hand-made service settings were removed. One raised the open-file limit for the Codex service, which the declared configuration already sets to the same value. The other two were inactive backups of renamed services. The Codex service is still running with the same limit, and no service was restarted.

Prometheus and Zeus showed no hand-made service or kernel settings.

## What remains

More dead weight is still on disk: scratch clones of source, old worktrees whose work is already merged, stray installer files and older evidence. The next passes will sort these by owner, deal with more retired conversations, and go host by host to replace any hand-made state with declared configuration.

Kept on purpose: current Flow repair work, the relay branch that is not yet merged, rollback copies and anything awaiting a judgment.

## What needs you

On Prometheus, a leftover from an earlier Nix proof and its lock can only be removed with administrator rights, and no flow has that access. It needs your hands, or a decision to grant the access.

Six hosts could not be checked: Tiger, vm-testing, mirror-alpha and mirror-beta did not answer in time, and Balboa's name did not resolve. Whether they are switched off, asleep or unreachable is for you to say.

The cleanup flow could not deliver this report through the usual messenger, which refused the send. That fault is with the messenger, not the cleanup.
<!-- to-the-living:end -->
