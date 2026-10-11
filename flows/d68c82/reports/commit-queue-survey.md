# Commit queue survey

Marks: (W) witnessed in this flow by reading the file, running the command or reading the code; (C) a claim made by another flow, with where it was made; (I) this flow's inference.

## 1. The living's words

These are the records that speak of a queue for commits, merges or publishing. I searched flows/*/vision, flows/*/notion, vision-raw, the vision- skills and every archive- file. No archive- file and no vision- skill mentions such a queue (W).

**flows/28d847/vision/publishing.md** (first committed 2026-10-03, 8b8386d85). The record's context says it was spoken "after a morning of lock waits and messages between flows to publish files each flow alone owns".

> So just make a tool that does all of this. It just queues everything and does it all properly. Why not?

-- psyche, STT.

**flows/9993b5/vision/mergeQueue.md** (2026-09-17)

> Or we have to lean out primary and then make pushing essentially the committing, right? Before editing, there's that lock problem because it doesn't matter if you're pushing at different times. You still have a merge problem, so you still have to coordinate.
>
> We need to have a pipeline, like a queue, so you can get into the queue where you're going to be merged, and then you can keep working from that because you're in the queue. We should create an orchestration tool that will orchestrate the merges of changes. When something gets checked out, it gets merged where it's supposed to be because it had that spot reserved.
>
> If you're working on something and you don't have a reserved spot, when you're done, you have to get a spot. He'll tell you to rebase on such and such. Once you've rebased, you can, because now you've reserved that spot. Spots also have a certain amount of time that they're reserved for, and if branches haven't been merged and are timed out, then we have to investigate what happened so we can decide what to do with it.

-- psyche, typed.

**flows/108ab0/vision/operational-timeBasedMergeSlots.md** (2026-09-17)

> Manage the merging of objects by assigning each Flow its place when it's ready to merge, so it knows what to rebase on. If it says yes, it has that spot reserved, and then it has to complete the merge in a certain time. Otherwise, we're going to let go of its place.
>
> Everything is time-based, right? If it's running out of space, then the orchestrator can also ask the agent, "Do you need more time?" An agent can say, "Yes, sure." That's why they have to be reachable.

-- psyche, typed. The record itself corrects "space" to "time".

**flows/9993b5/vision/orchestrateCommitBinding.md** (2026-09-17). This record is about the lock that would drive the queue, not the queue itself.

> We have the Orchestrate tool, right? If we ask people to use the Orchestrate tool to lock a file, let's make the lock easy to use. Let's not make the syntax big. Let's make a shorthand for Flow to make a lock on something. The description becomes the commit message, so we ask them to write their Orchestrate lock as they would write their commit message for what they're about to do.
>
> When they unlock, there's a hook that automatically commits or `jj commit push main`, whatever, right? The work tree that we're on, `main`, let's say, commits and pushes that change under that description from the lock that just got released.

-- psyche, typed. The record goes on to say "put some of the functionality of version controlling in the Orchestrate tool for now".

Other records from the same day that bear on this (W):

- 9993b5 orchestrateLocking: "we can lock files. We don't have to lock the whole repo."
- 9993b5 oneSharedPrimary: "go back onto one shared primary for now and use the Orchestrate tool to lock files".
- 9993b5 autoCommitOnWrite: "Eventually, I want a file write event that automatically creates a commit."

Tension (I): the two records of 2026-09-17 disagree on what happens when a spot's time runs out. mergeQueue.md says the timeout is investigated; timeBasedMergeSlots.md says "let go of its place". «The lock queue» puts this choice to the living as Ruling 4.

## 2. «The lock queue»

URL: https://claude.ai/artifact/Dx63sZCET9j3kN34QRsfJ3. It is line 45 of flows/d68c82/books/index.html. Flow 445410 (Core) wrote it, and its source is flows/445410/books/6-the-lock-queue.md (W).

The book says: "Status: all four proposals are unlanded. The Orchestrate in production has no queue; the queue is a proposal by Astra (0c85a3), not yet in any development branch." (W, read through Artifact read.) Astra's proposal (Enqueue, ObserveQueue, Cancel, and a Release that hands the lock to the head of the queue) is found nowhere in Primary except this book (W, grep). Its content is therefore a claim relayed by Core (C).

All four proposals target psyche-skills/skills/vision-orchestrate.md:

| # | Proposal | What the living is asked |
|---|---|---|
| P1 | The lock queue: a conflicting Lock request waits instead of being refused, and Release grants the lock to the next waiting request in the same step. Source: 9993b5 mergeQueue. | Land it, or hold until the merge queue and the lock queue are ruled one thing or two. |
| P2 | Order: first come, first served, but only among requests whose paths conflict. Source: 9993b5 orchestrateLocking; the book marks this as its own inference. | Per conflicting paths, one strict line for all requests, or another order. |
| P3 | Withdrawing: only the requesting flow may withdraw, unless that flow is idle or stale. Source: 01a03d6e locks. | Holder plus idle or stale flows, holder plus meta-orchestrate, or anyone who holds the lock's ID. |
| P4 | Time limit: the holder may extend when asked; on expiry the lock is released and stays observable. Sources: 108ab0 timeBasedMergeSlots, 9993b5 mergeQueue, 01a03eda observe. | Release on expiry, hold on expiry until investigated, or no time limit. |

Status: none of the four has landed. vision-orchestrate.md contains no "queue", and its last commit is fef9864 on 2026-10-07 (W). I found no ruling recorded in the 445410 log (W).

## 3. Existing tools

**tools/primary-publish.mjs** (279 lines, plus a test file; restored to main in 501404eb2 on 2026-10-03) (W).

- What it does: it is a publisher for one caller at a time. It checks that the caller is enrolled by matching its pid, start ticks and boot id against an authority file. It captures the requested paths. It builds the commit through a private GIT_INDEX_FILE on top of origin/main, using commit-tree. It pushes with a fast-forward push, never forced, and retries twice if the remote moves. It keeps a baseline per lane to detect conflicts on owned paths. A crash after the push is reconciled from a state file. Concurrent runs are kept apart by a mkdir lock on the state file.
- Tests: 15 of 15 pass (W, `node --test`).
- What is missing: there is no queue; its lock simply refuses a second caller with "publisher lock is held" (W, code). The controller that enrolls callers and writes /run/user/1001/primary-publish/authority.json does not exist (C: flows/5ed94b/reports/inventory-tools.md:17, which also lists a missing review and a missing skill change). Its design document, flows/dea0ba/reports/per-flow-publisher-design.md, is absent from disk (W).
- Deployed: no. The authority file and the state directory /home/li/.local/state/primary-publish do not exist, and no unit for it runs (W). No skill tells flows to call it (W).

**The PrimaryPublish lock** (skills compensation-primary-commit and operation-orchestrate).

- What it does: Orchestrate 0.37.0 is running as orchestrate-nexus.service (W). The PrimaryPublish lock's only path is the sentinel `<Primary>/.PrimaryPublish.lock`, so that publishers line up on one name. A Lock request that conflicts with a held lock is refused at once.
- What is missing: Orchestrate has no queue, no first-in-first-out order and no cancel, and the flow named in a lock is a label rather than an authority (C: Astra's qualification, 445410 log:237; the same facts appear in the book). Waiting flows retry, and the fastest one wins. "9fed42 refused 5 times" (C: 445410 log:228). The orchestrate source mentions a queue only to argue against an unbounded one in front of the store (W: ARCHITECTURE.md:62, core.rs:23,54).
- Deployed: yes, as a lock only.

**field-clj** (/git/github.com/LiGoldragon/field-clj) (W).

- What it does: it publishes a set of paths for a flow. The installed version (~/.nix-profile/bin/field-clj, whose jar holds jj.clj, built from main a2c278d) makes a jj commit limited to the named paths and pushes main.
- What is missing: the uncommitted working tree replaces jj with a private-index publication. On a race that version keeps the candidate and reports it, with no retry and no queue, and it adds `#publish-and-test`. That work is held under locks 15109 and 15125 by 42265e (W: `git status`, `Observe.Locks`). Neither version has a queue.
- Deployed: the jj version, yes. The private-index version, no.

**tools/jj-branch-queue** (2026-06-01) (W). It is not a queue. It only reports which jj bookmarks have been merged into main.

**Other repositories under /git/github.com/LiGoldragon** (W, grep and README). synchronizer and release-train-dogfood propagate version bumps across repositories, and repository-ledger records push events. None of them is a commit queue for Primary. No repository has a commit, merge or publish queue.

**Earlier precedent.** On 2026-10-03, flow db38f8 ("Field publisher") held PrimaryPublish permanently and published the paths other flows sent it by message (C: flows/28d847/log.md; brief flows/28d847/briefs/publisher-procedure.md). That was a queue run by a flow, not by a tool. A later log calls db38f8 "historical" (C: flows/f768df/log.md:167).

## 4. How flows publish today

**The independent-clone route** (W: skill compensation-primary-commit):

1. Acquire the PrimaryPublish lock.
2. Make an independent Git clone of Primary with a colocated jj workspace (`jj git init --colocate`).
3. Copy in only the flow's own verified paths.
4. Fetch, commit, and duplicate onto `main@origin`.
5. Check the copy with `jj resolve --list`. On a conflict, abandon the copy, release the lock and report.
6. Otherwise set `main` to the copy, run `jj git push --bookmark main`, and release the lock.

The shared working copy is never committed to. Core also ruled that a private-index `read-tree` is acceptable, and that every publisher must check the full base tree and count the paths it changes (C: 445410 log:213, 218). On 2026-10-10, origin/main received 86 commits and no merges, one flow at a time (W: `git log`). One flow pushed without the lock (C: 445410 log:275, 277).

**Core's manual sequencing** (C: 445410 log). When a race or a broken main occurs, Core holds every publisher by message and releases them in order:

- line 211: "All publishers held"
- line 228: "Psyche publishers held for 9fed42"
- line 229: "Publishers released"
- line 232: "lock-queue gap unassigned; manual sequencing continues"
- line 233: Astra 0c85a3 was assigned to qualify lock fairness and then design a bounded first-in-first-out queue, with no implementation.

## Sources

- flows/28d847/vision/publishing.md; flows/9993b5/vision/{mergeQueue,orchestrateCommitBinding,orchestrateLocking,oneSharedPrimary,autoCommitOnWrite}.md; flows/108ab0/vision/operational-timeBasedMergeSlots.md; flows/01a03d6e/vision/locks.md
- https://claude.ai/artifact/Dx63sZCET9j3kN34QRsfJ3 (version 1791614628-f1aa); flows/d68c82/books/index.html:45
- /git/github.com/LiGoldragon/psyche-skills/skills/vision-orchestrate.md
- tools/primary-publish.mjs, tools/primary-publish.test.mjs, tools/jj-branch-queue
- skills compensation-primary-commit, operation-orchestrate, vision-committing, vision-orchestrate
- /git/github.com/LiGoldragon/{orchestrate,field-clj,synchronizer,release-train-dogfood,repository-ledger}; `orchestrate 'Observe.Locks'`; `systemctl --user`
- flows/445410/log.md; flows/5ed94b/reports/inventory-tools.md; flows/28d847/log.md; flows/28d847/briefs/publisher-procedure.md
- Provenance receipt: unavailable, because no receipt handoff exists.
