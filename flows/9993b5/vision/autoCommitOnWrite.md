# Auto-commit on write

## Eventually, I want a file write event that automatically creates a commit

Context: typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message as the shared-workspace and datom-structural-editing visions (sharedWorkspace.md, datomStructuralEditing.md, same date). "Eventually" marks it as a directional aim, not immediate. In the shared-workspace pattern (previous vision), coordination between flows editing the same files is easier when every write leaves a commit that names its author flow — the history itself is the log. Pairs directly with the datom-structural-editing vision (next): the CLI that performs a structural edit is the natural event source for the auto-commit, one commit per edit operation. Removes the current pattern where a flow makes many edits then decides when to commit — a race and a bookkeeping burden. Logged by the main flow before acting.

> Eventually, I want a file write event that automatically creates a commit.

-- psyche, typed.
