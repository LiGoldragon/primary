# Upkeep handover

The cleanup and lean-preview work is complete; nothing further was being implemented. My judgment is to keep the preview unchanged until the living rules, and to require fresh preservation and activity checks for any later cleanup: this audit is a snapshot of repositories that continued changing during the work.

## What a fresh flow needs

- `primary-woc0.5` closed: 34 worktrees and 3 duplicate clones removed; 334 merged unused branches deleted. `worktrees.md` holds the pre-removal decisions; evidence, execution and verification files beside it preserve the proof. All 371 independent postconditions passed. Six Persona worktrees and 40 branch deletions were retained when its live remote default changed. Three paths created during the audit were retained and recorded separately.
- `primary-woc0.7` closed under Opus ruling `7zia`, which explicitly replaced publication acceptance with an isolated, measured, unpushed preview. No new archive or preview ref was published. Do not infer publication from the bead's closed state.
- The unpublished preview is `/git/github.com/LiGoldragon/primary-lean-a8ab9c`, branch `lean/workspace-2026-11-12-a8ab9c`, commit `246872900bf3a3857172975d6318a3d986668c58`, directly parented by the original Primary root. It is held for the living, not a removable stray. Its fetch source is local Primary; its push URL is deliberately disabled. Its committed payload is 74,787,523 bytes, 62.1% smaller than the measured remote-main payload. Exact content verification and measurements are in `lean-workspace.md`, `lean-selection.json` and `lean-clone-verification.json`.
- The immutable preview input is `/tmp/upkeep-a8ab9c/lean-workspace.tar`; its SHA256 is recorded in the selection manifest. The clone is the prepared repository, so the temporary tar is not its sole copy. Primary's full existing remote history was left alone; uncommitted omitted files remain in the live workspace and are not proven preserved by that remote history.
- These reports and this handover are unpublished Primary edits for its sole standing committer. I did not stage, commit or push Primary or switch its branch. Foreign edits were preserved.
- Field inventory independently reconciled all 1,124 initial roots with zero missing, recorded in `flows/866c08/evidence.json` and bead `primary-woc0.6`. It recorded the new preview in `flows/866c08/late-arrivals.csv` as intentional and protected. Its independent disk-footprint measurement is distinct from our logical payload comparison.

## Requests

No substantive open request remains. Inventory question `hrb5` was answered and acknowledged; research question `m6o7` was answered with proof paths and custody (delivery `xqzv` was queued at submission; no read acknowledgement was received). Question `7zia` was answered by Opus and implemented. Closing task `8d23` is answered with this handover's path. Publication awaits the living's future word, not an outstanding publication order.
