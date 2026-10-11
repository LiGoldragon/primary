---
description: Publish one flow's Primary paths without rewriting shared history.
---

Primary is committed in the shared working copy itself. Under the PrimaryPublish lock, a flow checks that shared HEAD equals origin/main, commits only its own paths, named explicitly (git commit -- <paths>), so nothing else staged in the shared index is taken, pushes without force, and releases. A mismatch or refused push is reported, never repaired. A flow commits through the shared index, never a temporary one. Primary is never cloned.

Outside the PrimaryPublish lock, a flow runs only read-only jj commands in Primary, each with --ignore-working-copy. A command that rewrites @ or its ancestors never runs with --ignore-working-copy.

A lock's paths name only the checkouts being edited; a flow's own lane under Primary is never locked. The PrimaryPublish lock's only path is the sentinel `<Primary>/.PrimaryPublish.lock`, a name with no file ever created there, so publishers serialize on one name and lock no checkout.
