# MiniDox Audit Fix Evidence

## Task And Scope

Applied the narrow audit fix in `/git/github.com/LiGoldragon/kibord`: the reconstructed MiniDox `BASE` layer thumb Backspace was changed from layer-tap `SYMBOLS_BSPC` to plain `KC_BSPC`. Hardware flash, reset, and query operations were not run.

The README confidence wording was also softened where present: it no longer claims the `NUMBERS` layer was fully recovered from both artifacts, and instead describes left layer 3 as resembling right layer 1.

## Files Consulted

- `/home/li/primary/AGENTS.md` from the task prompt.
- `/git/github.com/LiGoldragon/kibord/README.md`.
- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/keymap.c`.
- `/git/github.com/LiGoldragon/kibord/flake.nix`.

## Changed Files

- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/keymap.c`
  - `BASE` thumb row first slot now uses plain `KC_BSPC`.
- `/git/github.com/LiGoldragon/kibord/README.md`
  - Confidence wording for `NUMBERS` recovery was softened to match the audit wording.

## Validation

- `nix build .#minidox --no-link --print-out-paths`: passed.

The build emitted the expected dirty-tree warning before commit because the validation ran against the edited working copy. No hardware flashing, reset, or query commands were run.

## Version Control

- Commit: `912b09933b4f1334449df688a910415ad9eb9706`
- Commit message: `kibord: fix minidox base backspace recovery`
- Push: `jj git push --bookmark main` completed successfully.
- Post-push verification: `jj git push --bookmark main --dry-run` reported that `main@origin` already matches `main`.
- Final status: working copy clean.

## Remaining Warnings

- The README still preserves the broader MiniDox no-flash safety warnings and recovery unknowns; they were outside this narrow audit fix.
