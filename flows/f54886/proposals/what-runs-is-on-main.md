Presentation.{ «What runs is on main» }

# What runs is on main

*Created by Fable.*

From his words: "why are we not merging our work"; "merging is like one command-line call." Fixes of ours sat on a branch never merged, and the running Nexus was built from it. Lands without his review, on his word.

### Proposal 1: What runs is on main · psyche-belief › vision/committing.md

**Comment** A branch, a worktree or a dirty tree is work in motion; the line says what the motion is and whose, and where it ends.

  ## One shared workspace, for now

+ ## What runs is on main
+
+ A version that runs is built from main. A branch, a worktree or a dirty tree of ours carries a line naming what it holds and which flow owns it, and is folded into main or removed when that is done.

+ ```mermaid
+ flowchart TB
+     w["work on a branch, in a worktree, or dirty"] -- "named, owned" --> m["main"]
+     m -- "builds" --> r["the version that runs"]
+ ```
