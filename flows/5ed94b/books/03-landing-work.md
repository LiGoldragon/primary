Presentation.{ «Landing work» }

How the agents' working sessions, called flows, land their work on main, the one trunk of Primary, the one shared repository. Several agents are named below. Flow is the program that launches and tracks flows. Orchestrate is the program that locks files. Mind is the agent that designs and reviews. Field is the agent that builds and runs things.

## Part 1. What he wants

### One tree, one main

Every flow works in the same Primary checkout, and all work lands on main.

> "We can't use different worktrees for primary because then we don't have the same database for the psyche for all the subflows. That's why we have orchestrate."

-- 22 September

> "If you're in the same tree, there's no work tree. We're not using work trees."

-- 29 September

> "We should all just push to main for now"

-- 17 September

There are no work trees, no second checkouts and no per-flow clones.

> "No, I do not want work trees. I do not want fucking work trees. Fuck."

-- 3 October

There are no piles of branches. What exists is removed, and nothing new goes on a side branch.

> "I want everything merged on main, right? All the time. I don't want all these branches. I want all these branches removed. It's too much luggage, too much stuff to carry."

-- 17 September

> "And I don't want a whole bunch of fucking branches either, and this should be done by Codex, not you."

-- 3 October

### Each flow owns its own directory

A flow writes in its own directory. Nobody else writes there, so it is never locked.

> "Only the flow that has this [id] will ever write there."

-- 5 September

> "Plus, they only need their own flow ID subdirectory, so it's not even a problem."

-- 22 September

Shared files are written so that flows do not collide. Each flow appends, or adds its own entry.

> "if you have the right attitude, files can be appended only in the flow, or you just create an entry."

-- 17 September

### What locks what

Orchestrate locks files. Flow locks sessions. These are two separate jobs.

> "No, Flow locks the sessions and [Orchestrate] locks the files. Those are different things."

-- 3 October

A lock covers only the paths in use, never the whole repository.

> "we just worked with orchestrate, and we can lock files. We don't have to lock the whole repo."

-- 17 September

A lock is simply a Lock: a name, the paths and a description, and asking for it returns the whole lock.

> "Better to think of it as a Lock than a PathLock"

-- 26 August

> "the lock returns like a certain structure which shows the paths. That way there's like a better flow of information, as in like receiving the description, like which is the reason why that lock is on."

-- 26 August

The request is short. Its description is written as the commit message for the work about to be done.

> "Let's not make the syntax big. Let's make a shorthand for Flow to make a lock on something. The description becomes the commit message"

-- 17 September

### Release before idle, and stale locks

Every flow releases its locks before it goes idle. A subflow that is handed a lock keeps its parent active.

> "whatever flow put the lock in place is responsible to release that lock before it becomes idle."

-- 26 August

A flow that is idle, with no active subflow, loses its locks automatically. Any other flow may then remove them.

> "if through a transcription file, if it's possible to know that a flow is idle ... then all of its locks are automatically forfeited by protocol."

-- 26 August

> "any lock remains, they can be removed forcefully by another flow since any lock must be released, and this should be part of training."

-- 26 August

Until that is automatic, a skill unlocks a stale flow's lock, and a registry of flows exists even when work is done by hand.

> "We need to develop a skill to allow someone to unlock a [stale] flow lock ... We should have a registry of flows even if we're working by hand, right?"

-- 25 September

Proposed: Flow knows which sessions are alive, so Flow tells Orchestrate when a holder has gone idle, and Orchestrate drops that holder's locks.

### Commits

A commit names its files, and a flow commits what it edited. His own words on this are in question 2.

No uncommitted change is left behind. Changes found in the tree are committed first, as their own commit.

> "instruct agents to never leave uncommitted changes behind like that; if changes are present and one needs to make other changes, simply commit those changes."

-- 25 August

> "Just commit whatever. If somebody else hasn't committed, commit for them."

-- 22 September

The longer aim is that every write makes a commit by itself.

> "Eventually, I want a file write event that automatically creates a commit."

-- 17 September

### Publishing: one writer, a queue, a program

One long-lived program writes main. Nobody else moves it.

> "Do we not just need a single long-lived nexus that has a single writer logic?"

-- 29 September

Models do not run version control. They call that program, and it lands commits atomically. It is a program because this is mechanical work.

> "LLMs are not programs; they're not for that. They're for judging, so we don't want the LLMs to do it."

-- 3 October

Its lock lives in the program's own database.

> "it would have a lock in the database so it would know."

-- 26 September

The caller gives no description unless it wants to. The default comes from who is calling.

> "it's probably less if you don't have to give any description ... depending on who's calling it, they would know what the default commit is."

-- 18 September

The queue gives each request a reserved spot. A spot lasts a set time and can be extended on request. A spot that runs out unmerged is investigated.

> "Spots also have a certain amount of time that they're reserved for, and if branches haven't been merged and are timed out, then we have to investigate what happened"

-- 17 September

> "If it's running out of [time], then the orchestrator can also ask the agent, 'Do you need more time?' An agent can say, 'Yes, sure.' That's why they have to be reachable."

-- 17 September

The design as Mind wrote it, for Field to build:

- A flow gives only its paths and, if it likes, a note. Any path outside the caller's own lane is refused, and it never publishes a path the caller did not name.
- It takes a steady copy of each named file, including deletions, links and file modes, without ever touching the live file. If the file is changing as it reads, it answers "busy editing".
- It fetches main and compares each file with the version it last published. If main has not changed there, it lands the copy. If main already holds it, it reports already current. Anything else it refuses as a conflict, and it never merges one silently.
- It builds the commit straight from file contents, with no checkout, workspace or clone, and pushes only forward, never by force.
- After a crash it checks what reached main before trying again, and never repeats a push blindly.
- It answers with a readable receipt: paths, outcome, and whether a later edit is still waiting.
- It handles requests one at a time, so the queue he asks for is not in it.
- Limits: it needs a library that can build commits without a checkout, each generated file needs one owner, and publishing across several repositories is not atomic.

### Today's order: a Field seat publishes for everyone

Until the program exists, one small Field flow holds the publish lock for good, and every other flow messages it what to commit. His words on this are in question 1.

> "What do you mean, publish? You mean `git push`? Just get out a small agent to do it."

-- 3 October

### Stable and next

Each service runs a stable and a next side by side, on separate addresses. A new version starts as next. Once every flow has moved to it, next becomes stable.

> "Then you can run both side by side when you do a migration. ... We have this rolling mechanism to keep updating."

-- 26 September

> "If all the flows are on the next socket now, next can become stable, and then we can put the next version on next."

-- 30 September

Each address carries a short version mark, so next becomes stable without renaming anything.

> "that way, we can move the next to the stable without changing the socket name, so it doesn't break any of the sessions."

-- 30 September

Primary itself gets a next version: lean, with its data moved into its own repositories.

> "let's design the next version of primary, which we could just call primary next for now."

-- 17 September

## Part 2. What exists today

Witnessed on 3 October 2026.

- Primary has one working copy and no second work tree.
- The publisher program and its design file were dropped from the working copy at 14:42 today by a publish's head import. They survive only in unpublished snapshots. Recovery has been handed to the Psyche secondary seat (Opus), which is also the seat whose publish dropped the files.
- Primary's remote has 215 branches besides main.
- A Field seat holds the publish lock permanently and publishes what flows message it: nine publishes for five flows so far. It is a model following a hand procedure, not a program.
- Orchestrate refuses a taken name or overlapping paths. It does not stop a flow that skips the lock, and two version-control operations ran at once today.
- Nothing forfeits a stale lock. It is done by hand.
- Pushes are force-with-lease, and main is unprotected on the remote.

## Part 3. Questions

Answer each with its number and "1" or "2", or "yes".

1. **Program, or a Field seat?** Today's order and "make a tool" came fourteen minutes apart.

> "So just make a tool that does all of this. It just queues everything and does it all properly. Why not?"

-- 3 October

> "So then just get a field quaternary flow to hold the lock forever, and then whenever you need something committed, you message him. He's just going to do it. He's going to hold the lock, and he's just going to commit and push everything."

-- 3 October

Is the Field seat only a stopgap until the program exists (1), or does a Field seat stay the publisher (2)? Yes means 1.

2. **Commit everything, or commit named files?** The Field seat commits only named files.

> "You have to commit everything basically."

-- 29 September

> "You just commit the files that you edited, right? The call has to be explicit with file paths. Unless the whole repo is locked, in which case nobody else should be editing it."

-- 19 September

Is the rule named files only (1), or does "everything" still apply anywhere, for example to changes in the tree that belong to nobody (2)? Yes means 1.

3. **Wait and rebase, or refuse?** Say main changed a file after the caller's last publish.

> "If there's no conflict then it's rebased and it goes through."

-- 29 September

> "He'll tell you to rebase on such and such."

-- 17 September

That second remark was about queue spots for branches. Mind's design refuses any path main changed since its last publish, and it rebases nothing. Should the publisher wait and rebase (1), or refuse (2)? Yes means 1.

4. **Where does the commit happen?** When a flow releases its lock, or in the publisher?

> "When they unlock, there's a hook that automatically commits"

-- 17 September

> "a really simple nexus that we force agents to use instead of [JJ] and Git commands."

-- 29 September

Should a lock's release still trigger a commit (1), or does the publisher take over all committing (2)? Yes means 2.
