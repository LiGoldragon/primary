---
description: A flow has edited Primary, or would stage, commit, push or rewrite there.
dependencies: [vision-committing]
---

Every flow edits Primary and leaves its owned edits for the sole standing Field Quaternary committer. No main flow or subflow stages, commits, pushes, acquires PrimaryPublish, or rewrites Primary itself. The editing seat's turn-end hook sends its actual FLOW_ID (or explicitly labeled native session ID) and transcript path to the committer only when Primary is dirty; a clean turn sends nothing. A blocked hook or handover is reported, never replaced by a direct commit.

The committer alone holds PrimaryPublish for its lifetime at `<Primary>/.PrimaryPublish.lock`, a sentinel name with no file created. It commits in the existing shared working copy, never a clone, reads the firing session's transcript, preserves foreign work, and assigns only qualified owner paths. Late changes are squashed into their corresponding commits with JJ under its owned lock and protected remote lease; ambiguous ownership or a refused push is reported without discarding work. No other flow performs Primary JJ mutations.

A flow editing any other repository commits and pushes its own changes in that repository. Source reservations remain separate from the committer's lifetime publication lock.
