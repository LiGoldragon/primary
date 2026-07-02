# MiniDox Colemak Correction Evidence

## Task And Scope

Correct `/git/github.com/LiGoldragon/kibord` after the prior MiniDox modernization made the base layer depend on host-side Colemak. The user clarified that the MiniDox firmware itself must intentionally emit Colemak, while the OS must not additionally Colemak-remap this device. The modern QMK/Nix stack from commit `5343bc14` was to be preserved.

No keyboard flashing or device-mutating command was run.

## Files And Commands Consulted

- Read repository startup guidance from `/home/li/primary/AGENTS.md` in the task prompt.
- Read local role doctrine for code implementation, edit coordination, and jj version control.
- Claimed `/git/github.com/LiGoldragon/kibord` with Orchestrate before editing.
- Inspected `README.md`, `flake.nix`, `maple_computing/minidox/LiGoldragon/keymap.c`, and the commit metadata for `5343bc14`.
- Checked existing modernization surfaces with `rg` and confirmed QMK `0.33.8` and target `maple_computing/minidox/rev1` remained in `flake.nix`.

## Changed Files

- `maple_computing/minidox/LiGoldragon/keymap.c`
  - Changed the base layer letter keycodes back to firmware-level Colemak.
  - The physical top row now emits `KC_Q KC_W KC_F KC_P KC_G KC_J KC_L KC_U KC_Y KC_SCLN`, so a raw QWERTY host receives `qwfpgjluy;`.
  - Preserved existing layer structure, mod-tap physical positions, thumbs, lower/raise/adjust layers, and tri-layer behavior.
- `README.md`
  - Replaced the QWERTY-position/host-Colemak explanation.
  - Documented that the firmware intentionally emits Colemak, the MiniDox should not receive an additional OS Colemak remap, and laptop-keyboard Colemak should be applied separately per device.

No flake or lockfile modernization changes were reverted.

## Validation

- `nix build .#minidox --print-build-logs --max-jobs 0 --builders @/etc/nix/machines --builders-use-substitutes`
  - Passed on the configured remote builder.
  - Built QMK target `maple_computing/minidox/rev1` with keymap `LiGoldragon`.
  - QMK reported firmware size was within limits.
- `nix flake check --print-build-logs --max-jobs 0 --builders @/etc/nix/machines --builders-use-substitutes`
  - Passed.
  - Reported the existing warning that `SubWorld` is an unknown flake output.
  - Reported `aarch64-linux` was omitted as incompatible; `x86_64-linux` checks passed.
- `jj status --no-pager`
  - Clean after commit and push.

## Commit And Push

- Commit: `c08bb77661ac24397cd53c432890280715c59fc2`
- Message: `kibord: restore minidox firmware colemak`
- Bookmark `main` was advanced and pushed to origin.

## Remaining Risks

- The firmware was built but not flashed or tested on the physical MiniDox, per task safety constraints.
- This correction documents the required OS behavior but does not implement per-device OS layout configuration for the laptop keyboard.
