# Shared workspace

## If they are all primary, then they should all work in a shared space, so we would almost have a shared workspace where they have different repos themselves; some are writable by all of them, and they have to coordinate on who can edit them between themselves

Context: typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17, opening the message that also carries the auto-commit-on-write and datom-structural-editing visions (autoCommitOnWrite.md, datomStructuralEditing.md, same date). Refines the orchestrate-locking vision (orchestrateLocking.md, same day) with a concrete shape: one shared workspace directory (per layer — "if they are all primary"), containing multiple repositories side by side, some per-flow (writable by that flow only, no coordination needed), some shared (writable by all flows in that layer, coordination required — the orchestrate file-locks from the earlier vision apply here). Answers the transition question this flow surfaced last turn ("existing sessions in worktrees, new work in shared checkout?") by saying: one shared workspace per layer, populated with the right repos, is the target shape. Logged by the main flow before acting.

> Yeah, that's what I mean. If they're all primary, then they should all work in a shared space, so we would almost have a shared workspace where they have different repos themselves. Some are writable by all of them, and they have to coordinate on who can edit them between themselves.

-- psyche, typed.
