# Flow 01a035fb

Investigated why Claude flows `2f6b1dc5` and `aa4c7747` appeared to lose changes in `primary`.

Remembered: 2f6b1dc5, aa4c7747 — depth 1

Settled:

- Both transcripts survive. Both incidents exposed uncommitted flow work to concurrent movement of the shared primary working-copy state; a later tree did not contain the work, although jj history retained recovery material.
- `2f6b1dc5` is recovered now: its log and three vision files were restored from retained session context and committed as `90575b46c066`. The restored tail has no independent pre-loss byte copy.
- `aa4c7747` observed its vision directory absent on the stale `89ebc65d` line and recovered ten files from `e9dbab8c`; later flow state is committed too.
- No witness identifies the exact concurrent actor or single operation that first selected either stale state. No loss-time `jj restore`, `rebase`, or `abandon` explains `2f6b1dc5`.
- The psyche-approved found-in-tree preservation rule landed afterward in `NON_MANAGEMENT_AGENTS.md` as `634ad0ed5672`. It reduces uncommitted exposure but does not serialize writers or own working-copy state.
- Durable subflow evidence landed in `5ad8e7ba8806`; pre-existing dirty work was separately preserved in `498cf24d93e0`.

Open:

- The terminal state-ownership design: serialize all writers to one primary working copy, isolate writers in independently owned workspaces, or another proven shape.
- Whether the Curriculum file-editing contract should gain any exact wording; every skill edit requires psyche approval, and wording alone cannot close the concurrency defect.
- Repair the stale edit-coordination command syntax and decide whether advisory claims are sufficient; the syntax drift is observed but not proven causal.

