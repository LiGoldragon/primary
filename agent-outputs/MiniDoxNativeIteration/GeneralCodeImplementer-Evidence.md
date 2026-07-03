# MiniDox Native Iteration Evidence

## Task And Scope

Created the first clean MiniDox-native iteration for review/test in `/git/github.com/LiGoldragon/kibord` from the recovered layout.

Boundaries observed:

- No hardware flashing.
- No hardware reset, query, or write.
- Preserved the recovered layout except for the requested number reorder and conservative leader one-shot additions.
- Used the pinned upstream MiniDox default keymap style as the visual shell reference, not as a wholesale layout source.

## Files And Commands Consulted

Consulted local task evidence:

- `/home/li/primary/agent-outputs/MiniDoxBinaryRecoveryAvr/GeneralCodeImplementer-RecoveryReport.md`
- `/home/li/primary/agent-outputs/MiniDoxKeymapReconstruction/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/MiniDoxKeymapAudit/Scout-SituationalMap.md`
- `/home/li/primary/agent-outputs/MiniDoxQmkCandidateReview/Scout-CandidateReview.md`

Consulted repository files:

- `/git/github.com/LiGoldragon/kibord/README.md`
- `/git/github.com/LiGoldragon/kibord/flake.nix`
- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/keymap.c`
- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/config.h`
- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/rules.mk`

Consulted upstream pinned QMK source over GitHub raw content:

- `qmk/qmk_firmware` commit `b1093e9da5f27253f3db692352daf5cf4ad5b98d`
- `keyboards/maple_computing/minidox/keymaps/default/keymap.c`
- `docs/one_shot_keys.md`
- `quantum/action_util.h`

Coordination and version-control commands:

- `orchestrate "(Observe Roles)"`
- `orchestrate "(Claim ... keymap.c README.md ...)"`
- `jj status --no-pager`
- `jj diff --stat --no-pager`
- `jj commit -m 'kibord: shape minidox native review layout' -m 'Agent: Codex GPT-5'`
- `jj bookmark set main -r @-`
- `jj git push --bookmark main`

## Changed Files

- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/keymap.c`
- `/git/github.com/LiGoldragon/kibord/README.md`

## Implementation Summary

`keymap.c` now uses MiniDox-shaped visual layer blocks before each `LAYOUT_split_3x5_3(...)` block, following the pinned upstream MiniDox default diagram convention where practical. The diagrams cover `BASE`, `SYMBOLS`, `NUMBERS`, `FUNCTIONS`, and `QWERTY_RECOVERED`.

Recovered behavior was preserved except for the requested number reorder. The `NUMBERS` layer keeps the same physical positions that already held numbers, but their tapped outputs now read left-to-right as `1 2 3 4 5 6 7 8 9 0`. Existing modifier-tap wrappers stayed at their physical positions.

Leader behavior now includes conservative one-shot modifier sequences:

- leader `r e s e t`: calls `reset_keyboard()`, preserved.
- leader `s`: one-shot Shift.
- leader `c`: one-shot Ctrl.
- leader `a`: one-shot Alt.
- leader `g`: one-shot Gui.

`QK_BOOT` remains only on the tri-layer `FUNCTIONS` layer, aliased as `HIDDEN_BOOT` in source to document that it is a tucked-away fallback rather than the primary bootloader path.

`README.md` now documents the first-cycle build, review, and explicit-approval-before-flash workflow, the layer diagram review surface, number reorder semantics, and leader commands.

## Validation

Passed:

- `nix build .#minidox`
- `nix build .#minidox --no-link`

The first build created the normal local `result` symlink, which was removed before commit. The second build used `--no-link` and left no build symlink behind.

Not run by boundary:

- No flash command.
- No bootloader entry.
- No hardware reset.
- No USB/device/hardware query.

## Published Commit

Repository: `/git/github.com/LiGoldragon/kibord`

Commit: `f2a45733a42227fba12062eae58efc977f75557a`

Bookmark: `main`

Push result: `main` advanced on origin from `912b09933b4f` to `f2a45733a422`.

Post-push status:

- `jj status --no-pager`: clean working copy.
- `jj show -r main --stat --no-pager`: `README.md` and `maple_computing/minidox/LiGoldragon/keymap.c` changed, 107 insertions and 11 deletions.

## Warnings And Unknowns

- Exact physical placement for some recovered home/bottom row positions remains a known uncertainty inherited from the recovery audit.
- `QK_USER_0`, `QK_USER_1`, and `QK_USER_3` remain inert historical placeholders because their stripped old behavior was not proven.
- One-shot modifiers are build-proven on QMK `0.33.8`, but not hardware-tested by task boundary.
