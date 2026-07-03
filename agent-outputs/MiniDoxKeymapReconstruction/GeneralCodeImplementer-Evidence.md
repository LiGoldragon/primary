# MiniDox Keymap Reconstruction Evidence

## Task And Scope

Reconstructed the MiniDox QMK source keymap in `/git/github.com/LiGoldragon/kibord` from recovered old binary tables. Preserved the confirmed leader `r e s e t` bootloader path. No hardware flashing, reset, query, or keyboard write was performed.

## Evidence Consulted

- `/home/li/primary/agent-outputs/MiniDoxBinaryRecoveryAvr/GeneralCodeImplementer-RecoveryReport.md`
- `/home/li/primary/agent-outputs/MiniDoxBinaryRecoveryAvr/right.bin`
- `/home/li/primary/agent-outputs/MiniDoxBinaryRecoveryAvr/left.bin`
- `/home/li/primary/agent-outputs/MiniDoxBinaryRecoveryAvr/right-avr5.disasm`
- `/home/li/primary/agent-outputs/MiniDoxBinaryRecoveryAvr/left-avr5.disasm`
- Pinned QMK `0.33.8` source through the repository flake, specifically the MiniDox `keyboard.json`, `quantum/leader.h`, and `quantum/keycodes.h`.
- Public Spirit text search for MiniDox/kibord intent: no matching record.

## Changed Files

- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/keymap.c`
- `/git/github.com/LiGoldragon/kibord/README.md`

## Implementation Summary

`keymap.c` now carries recovered table-derived layers:

- `BASE`: firmware-Colemak layer from the common right layer 0 / left layer 1 evidence. The high-confidence top row is `Q W F P G / J L U Y ;`. Home and bottom rows are kept in recovered matrix order because the exact old physical macro is still uncertain.
- `SYMBOLS`: recovered from left artifact layer 2.
- `NUMBERS`: recovered from right layer 1 / left layer 3.
- `FUNCTIONS`: recovered from left layer 4, with modern `QK_BOOT` replacing recovered `0x7c00`.
- `QWERTY_RECOVERED`: retained non-default historical layer from left artifact layer 0.

`QK_LEAD` replaces recovered `0x7c58`, and `leader_end_user()` still calls `reset_keyboard()` for `leader r e s e t`. Recovered `QK_USER_0`, `QK_USER_1`, and `QK_USER_3` positions are preserved as named inert placeholders because the stripped binary did not prove their old `process_record_user` behavior.

`README.md` now distinguishes recovered-from-binary status, confidence levels, known unknowns, build command, leader reset path, and no-flash safety.

## Validation

- `nix build .#minidox`: pass. Built firmware artifact only; no flashing or hardware action.
- `jj status --no-pager` after push: clean working copy.
- `jj git push --bookmark main --dry-run` after push: `main@origin` already matches `main`.

## Published Commit

- Commit: `3cd938f3a893`
- Bookmark: `main`
- Push result: origin `main` fast-forwarded from `c71c7787338f` to `3cd938f3a893`.

## Remaining Uncertainties

- Exact physical placement of some home/bottom row keys remains medium confidence until the old MiniDox build macro or the actual keyboard behavior is verified.
- Historical custom keycodes `QK_USER_0`, `QK_USER_1`, and `QK_USER_3` have positions but not recovered behavior.
- This remains a no-flash reconstruction until reviewed against the actual hardware and binary evidence.
