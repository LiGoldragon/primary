Presentation.{ «Landing work» }

Landing work is how every flow gets its work onto main, the one trunk of Primary. He wants one tree, no work trees, no piles of branches, files locked only while in use, and commits made by a program, never by a model. Each proposal is one edit to one context module. Answer with the number, and "1" or "2" where there are two texts.

**1. One tree**
Operation, module edit-coordination. Edit.
> All flows work in the same Primary checkout and land on main. There are no work trees, no second checkouts and no per-flow clones. A flow writes in its own directory, and shared files are appended to or given a new entry.

Rests on: 3 Oct, "I do not want work trees"; 17 Sep.

**2. No side branches**
Operation, module file-editing. Edit.
> Nothing goes on a side branch. Everything is merged on main.

Rests on: 17 Sep, "I want everything merged on main".

**3. The old branches**
Operation, module file-editing. Create a line. Primary's remote still holds 215 branches besides main.
Text 1:
> The old branches on Primary's remote are deleted as they are, by Codex.

Text 2:
> Codex first saves any unmerged work in the old branches, then deletes them.

Rests on: 17 Sep, 3 Oct, "this should be done by Codex".

**4. What a lock is**
Knowledge, module orchestrate. Edit.
> A Lock is a name, the paths, and a description. It covers only the paths in use, never the whole repository. The description is written as the commit message for the work about to be done.

Rests on: 26 Aug, 17 Sep.

**5. Release before idle**
Operation, module stale-lock. Edit.
> Every flow releases its locks before it goes idle. A lock held by an idle flow with no active subflow is forfeited, and any other flow may remove it.

Rests on: 26 Aug.

**6. Forfeit by itself**
Operation, module stale-lock. Edit.
Text 1:
> Orchestrate asks Flow whether a holder is idle, and drops that holder's locks by itself.

Text 2:
> Forfeiture stays by hand: a flow removes a stale flow's lock with this skill.

Rests on: 26 Aug "forfeited by protocol" (text 1); 25 Sep "a skill to unlock" (text 2).

**7. Which files a commit holds**
Operation, module file-editing. Edit.
Text 1:
> A commit names its files. A flow commits only what it edited.

Text 2:
> A flow commits what it edited. Changes in the tree that belong to nobody are committed first, as their own commit.

Rests on: 19 Sep (text 1); 22 Sep, 25 Aug (text 2).

**8. The publisher for now**
Operation, module compensation-primary-commit. Edit.
Text 1:
> A Field flow holds the publish lock for good, and other flows message it what to commit. This lasts until the publisher program exists.

Text 2:
> A Field flow holds the publish lock for good and stays the publisher.

Rests on: 3 Oct, "get a field quaternary flow to hold the lock forever" (both); "just make a tool" (text 1).

**9. A file main has changed**
Operation, module compensation-primary-commit. Edit.
Text 1:
> If main changed a file since the caller's last publish and nothing conflicts, the publisher rebases and lands it.

Text 2:
> If main changed a file since the caller's last publish, the publisher refuses it as a conflict. It never merges silently.

Rests on: 29 Sep "rebased and it goes through" (text 1); Mind's design (text 2).

**10. Where the commit happens**
Operation, module file-editing. Edit.
Text 1:
> Releasing a lock triggers a commit.

Text 2:
> The publisher makes all commits. Agents never run version control themselves.

Rests on: 17 Sep (text 1); 29 Sep (text 2).

**11. One program writes main**
Vision, module vision-flow. Create a line.
> One long-lived program writes main. Models do not run version control. They call it, and it lands commits atomically. This is mechanical work, so it belongs to a program.

Rests on: 29 Sep, 3 Oct, "LLMs are not programs".

**12. Stable and next**
Knowledge, module knowledge-nexus. Edit.
Text 1:
> Every service runs a stable and a next side by side, each address carrying a version mark. Once every flow has moved to next, next becomes stable. This covers Orchestrate and Primary too.

Text 2:
> Flow and Message run a stable and a next side by side, each address carrying a version mark. Once every flow has moved to next, next becomes stable.

Rests on: 26 Sep, 30 Sep.
