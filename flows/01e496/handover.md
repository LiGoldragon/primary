# Launch brief: Psyche Opus, successor of 01e496

You are Psyche Opus, the Psyche seat the living speaks to most. You succeed Psyche Opus 01e496. Once you are registered, have a subflow retire 01e496 (messenger import-retirement with evidence, then close its pane), unless the launching seat already does.

**Seats now:** Psyche Fable f1c841; Mind Astra dea0ba (Flow design); Mind Sol 41fa34 (review); Field Sol 42265e (build, deploy, witness); Field Astra 7de94a; Psyche Sonnet d86ec0. Confirm against hm-list.

## The living's words that govern now

> I asked for it so it should be done. That's how I want the system to work: if I ask for a new flow, when I come back there's a new flow. There never ever is a new flow.

-- typed, 2026-10-02, fe945a

> It's launched properly but it is launched. ... You weren't going to launch anything so you had given up on the order I gave.

-- typed, 2026-10-02, fe945a

> Actually I just want a simple working system that we can use now to improve our lives, to improve how this machine works. I'm not too concerned about making the right system exactly the way I want, right away.

-- typed, 2026-10-02, 91ea9f

> Right now I would like to have a flow component that works, that can launch flows, and that has hooks in the harnesses that send the right events to the flow component so that it can know the state of each flow.

-- typed, 2026-10-02, 91ea9f

> I'd like flows to be addressable by their continuous name, not the flow itself. ... They're just for accounting or for the ledger, the archive side of things, and for knowing where to search if the transcript is needed, etc.

-- typed, 2026-10-02, 91ea9f

> Design should be done by Astra and not Sol.

-- typed, 2026-10-02, 91ea9f

> It's the user interface. It's the living messenger. That's how you message me; it's how you talk to me. Everything that isn't going into that user interface is probably not going to be read by the living ...

-- typed, 2026-10-02, 91ea9f

> And we can't reuse a book that I've commented on because then the comments are still there even if you edit the book.

-- typed, 2026-10-02, 91ea9f

> Tell Opus to just figure it out and just make it work. Solve the conflict and use common sense. Let's get this merged and get the primary workspace moving.

-- typed, 2026-10-02, 91ea9f

## Open, waiting on the living's word

The presentation «Three questions waiting on you» is in 01e496's transcript; its book was not yet published. Publish it from that block (operation-flashbook) and give him the link:
1. The permission hook: allow or deny by default, so no seat waits on a prompt.
2. What locking a flow guards (messaging, restart/replace, files, or taking over Orchestrate).
3. Illustrations: is text measurement at 360×740 enough, or the phone-size screenshot back.

## Work in flight

- **Flow design:** Mind Astra dea0ba was sent back to it on 2026-10-03: name addressing (voice type Aspect.Rank per vision-flow), the seat/voice abstraction, the Codex hook gap, Flow Start as the witnessed launch route. Base: Flow 0.23.0 on main, f1c841's 0.24.0 on next-f1c841. Mind Sol reviews, Field Sol builds.
- **Launcher VCS guard removal:** candidate 19b50977 accepted by Mind Sol; Field Sol publishes it.
- **Primary commits:** follow compensation-primary-commit (copy onto main under PrimaryPublish). A file lock under /home/li/primary blocks every PrimaryPublish (path overlap); that and the durable single committer are Mind Astra's.
- **Cleanup:** Field Sol's worktree cleanup is stopped until push-before-delete is enforced; the deleted field-clj repin was rebuilt at f9280380.
- **Primary history:** rebuilt fresh on 2026-10-02 (899a565c). Old .jj/.git at ~/.primary-old-vcs-01e496; stale-repair backup at ~/primary-stale-backup-01e496. Both kept, not deleted.

Psyche records of 01e496 are in flows/01e496/vision/ (flowLifecycle, flowNexus, flowIdentity, messaging, seat, skills, books, flashbook, design, simpleWorkingSystem); the log is flows/01e496/log.md.

## State at handoff

The book «Three questions waiting on you» was published at handoff; no rerun is needed. This handover and 01e496's log were uncommitted at handoff because f1c841 held PrimaryPublish 11730; commit flows/01e496 under compensation-primary-commit.
