# Worktree hygiene

## We cannot just keep spawning new worktrees; we need to rebase primary and cut a lot of stuff off there because it is too heavy to keep copying that filesystem; we will run out of disk space; clean up the old ones and get them merged; is everything being merged, is somebody merging all of this, we have to merge everything

Context: typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 mid-turn, after the Fable restart order and the three visions logged this turn (psycheChronology.md, threadNaming.md, transcriptSelfReference.md, same date). The trigger is Low's checkup finding of `/home` at 322G free of 916G plus the recovery report's mention of the classifier refusing `jj git clone`, so the pattern that has settled is a new independent JJ clone plus multiple `.claude/worktrees/<flow>/` inside each per launch — costly. The "integrator unnamed" fork is one of the held forks named in f55ec8's handoff to successor (2026-09-16 evening: "integrator unnamed"). Logged by the main flow before acting.

> Oh, and we can't just keep spawning new work trees, right? We need to rebase primary and cut a lot of stuff off there because it's too heavy to keep copying that file system. We're going to run out of disk space. Let's clean up old ones and get them merged. Is everything being merged? Is somebody merging all of this? We have to merge everything.

-- psyche, typed.
