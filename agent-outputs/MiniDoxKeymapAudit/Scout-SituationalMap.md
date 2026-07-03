# MiniDox Keymap Audit Situational Map

## Task And Scope

Audit `/git/github.com/LiGoldragon/kibord` at commit `3cd938f3a893` against `/home/li/primary/agent-outputs/MiniDoxBinaryRecoveryAvr/GeneralCodeImplementer-RecoveryReport.md`.

Boundaries observed: no file edits in the `kibord` checkout, no flash/reset/hardware query, no commit/push. The only write was this scout output under `agent-outputs/MiniDoxKeymapAudit/`.

## Findings

1. Blocker for exact lived-layout flashing: the base thumb Backspace position does not match the high-confidence right-artifact table.

   Evidence: the recovery report's right artifact layer 0 matrix row 3 has C2 `KC_BSPC`, C3 raw `0x7c58`, C4 `LT(1,KC_SPC)` at `GeneralCodeImplementer-RecoveryReport.md:69-80`. Current source defines `SYMBOLS_BSPC` as `LT(SYMBOLS, KC_BSPC)` at `maple_computing/minidox/LiGoldragon/keymap.c:11` and places it in the base thumb row at `keymap.c:32`. That changes a high-confidence plain key into a layer-tap and adds access to a `SYMBOLS` layer that is not part of the right artifact's two-layer table. This is not a hardware-brick risk, but it should block flashing if the gate is "actual lived layout as much as possible."

2. No mismatch found in the high-confidence `BASE` alpha/mod-tap matrix after expanding the pinned QMK `LAYOUT_split_3x5_3` right-half reversal, except the Backspace layer-tap noted above.

   Evidence: the report's right layer 0 rows are at `GeneralCodeImplementer-RecoveryReport.md:69-80`. Current `BASE` is at `keymap.c:28-33`. Pinned QMK `keyboard.json` maps the right side in reversed matrix columns, so current physical args `KC_J, KC_L, KC_U, KC_Y, KC_SCLN` expand to matrix row 4 C0..C4 `KC_SCLN, KC_Y, KC_U, KC_L, KC_J`, matching the report.

3. No mismatch found in the high-confidence recovered number/navigation layer, modulo layer index renaming.

   Evidence: the report's right layer 1 table is at `GeneralCodeImplementer-RecoveryReport.md:82-93`. Current `NUMBERS` is at `keymap.c:42-47`. The source uses `NUMBERS` as layer index 2 because it inserts `SYMBOLS` at index 1, but the matrix contents match the report after applying the same QMK layout-map reversal. Base `LT(1,KC_SPC/ESC/ENT)` became `LT(NUMBERS,KC_SPC/ESC/ENT)`, which is behaviorally equivalent for that recovered layer if `NUMBERS` remains the recovered number layer.

4. `QK_USER_0`, `QK_USER_1`, and `QK_USER_3` placeholders are safe in the narrow no-destructive-action sense, but they are behavior-loss risks.

   Evidence: current source aliases them at `keymap.c:16-20` and places `RECOVERED_USER_0/1` in `FUNCTIONS` at `keymap.c:52`, and `RECOVERED_USER_3` in `QWERTY_RECOVERED` at `keymap.c:60`. Pinned QMK `keycodes.h` defines `QK_USER_0 = 0x7E40`, `QK_USER_1 = 0x7E41`, and `QK_USER_3 = 0x7E43`. With no local `process_record_user` switch for those keycodes, QMK's weak `process_record_user` returns true and `action_for_keycode` falls through to `ACTION_NO`, so they are inert. The recovery report only identifies `0x7e40` and `0x7e41` as old special keycodes and says exact names/behavior were not proven (`GeneralCodeImplementer-RecoveryReport.md:111-124`). I found no local source or disassembly evidence that proves what `QK_USER_0/1/3` did.

5. `leader r e s e t` is implemented in a way likely equivalent to the recovered Caterina bootloader-entry behavior.

   Evidence: current `rules.mk:3` enables `LEADER_ENABLE`; `keymap.c:68-71` calls `reset_keyboard()` after `leader_sequence_five_keys(KC_R, KC_E, KC_S, KC_E, KC_T)`. The report shows the right disassembly loading `KC_R KC_E KC_S KC_E KC_T`, calling a five-key sequence predicate, then calling a path that writes `0x7777` to SRAM `0x0800/0x0801` and starts watchdog reset (`GeneralCodeImplementer-RecoveryReport.md:126-163`). Pinned QMK `reset_keyboard()` calls `bootloader_jump()`, and the AVR Caterina implementation writes `0x7777` to `0x0800` and enables the watchdog.

6. Layer names/docs are mostly honest about confidence and no-flash status.

   Evidence: `README.md:3` says the MiniDox target is build-only and should not be flashed until layout, bootloader, half selection, and reset procedure are reviewed. `README.md:18-23` separates high/medium confidence and names the `QK_USER_*` unknown. `README.md:43-53` gives no-flash review steps. One nuance: `README.md:20` says the `NUMBERS` layer was recovered from both artifacts; the recovery report says left layer 3 is "similar to right layer 1" at high confidence, not necessarily byte-for-byte identical (`GeneralCodeImplementer-RecoveryReport.md:103-111`).

## Build Result

`nix build .#minidox --no-link --print-out-paths` passed in `/git/github.com/LiGoldragon/kibord`.

## Observed Facts

- `jj status` in `/git/github.com/LiGoldragon/kibord` reported no changes. Working copy `@` is empty on parent `3cd938f3 main | kibord: reconstruct minidox binary keymap`.
- `jj log -r 3cd938f3a893 --no-graph` resolved the commit as `3cd938f3a89374dd2ca0f1a63b78d24c94e58594 kibord: reconstruct minidox binary keymap`.
- `flake.nix:269-274` builds `.#minidox` from local `maple_computing/minidox/LiGoldragon` as QMK keyboard `maple_computing/minidox/rev1`, keymap keyboard model `maple_computing/minidox`.
- `flake.lock` pins QMK firmware to upstream `qmk/qmk_firmware` rev `b1093e9da5f27253f3db692352daf5cf4ad5b98d` through ref `0.33.8`.
- Pinned QMK `keyboard.json` for `maple_computing/minidox/rev1` maps `LAYOUT_split_3x5_3` right-side arguments to reversed matrix columns: top-right physical arguments map to matrix row 4 C4, C3, C2, C1, C0; the same pattern applies rows 5, 6, and 7.
- `maple_computing/minidox/LiGoldragon/rules.mk` contains `LEADER_ENABLE = yes`; `config.h` sets `LEADER_TIMEOUT 350` and `LEADER_PER_KEY_TIMING`.

## Interpretations

- Flash should remain blocked until the `SYMBOLS_BSPC` vs recovered plain `KC_BSPC` mismatch is consciously resolved.
- Inert `QK_USER_*` placeholders are safer than inventing behavior, but they mean the source is not a complete recovery of the left artifact's old custom behavior.
- The `leader r e s e t` path is the strongest recovered behavior and has a good source-level equivalent in current QMK for Caterina-style ATmega32u4 bootloader entry.

## Commands And Files Consulted

- `spirit "(PublicTextSearch [MiniDox kibord keymap recovery flashing])"`: returned `(Error [no matching record])`.
- `orchestrate "(Observe Roles)"`: no conflicting claim on `/git/github.com/LiGoldragon/kibord` observed.
- `jj status`, `jj log`, `jj diff --from 3cd938f3a893 --to @ --stat`.
- `nix build .#minidox --no-link --print-out-paths`.
- `sed`, `nl`, `rg`, `find` over:
  - `/git/github.com/LiGoldragon/kibord/README.md`
  - `/git/github.com/LiGoldragon/kibord/flake.nix`
  - `/git/github.com/LiGoldragon/kibord/flake.lock`
  - `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/keymap.c`
  - `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/rules.mk`
  - `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/config.h`
  - `/home/li/primary/agent-outputs/MiniDoxBinaryRecoveryAvr/GeneralCodeImplementer-RecoveryReport.md`
  - `/home/li/primary/agent-outputs/MiniDoxBinaryRecoveryAvr/right-avr5.disasm`
  - `/home/li/primary/agent-outputs/MiniDoxBinaryRecoveryAvr/left-avr5.disasm`
  - pinned QMK source files for `keyboard.json`, `quantum/keycodes.h`, `quantum/keymap_common.c`, `quantum/quantum.c`, `quantum/process_keycode/process_leader.c`, `quantum/process_keycode/process_quantum.c`, and `platforms/avr/bootloaders/caterina.c`.

## Unknowns And Not Checked

- I did not flash, reset, enter bootloader, enumerate USB devices, or query hardware.
- I did not fully reverse engineer old `process_record_user`; no local evidence proved `QK_USER_0`, `QK_USER_1`, or `QK_USER_3` behavior.
- I did not rebuild/disassemble the newly built HEX to perform byte-level comparison against the old HEX; the audit compares source/macro expansion and reported recovery evidence.
