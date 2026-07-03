# MiniDox Native Keymap Audit

Task: read-only audit of `/git/github.com/LiGoldragon/kibord` commit `f2a45733a42227fba12062eae58efc977f75557a`, focused on the first-cycle MiniDox-native keymap iteration. Scope was limited to local source inspection, pinned QMK source inspection through Nix, jj read-only history/diff commands, and the requested build command. No files in the target repo were edited, no hardware was queried, and no commit/push/flash/reset command was run.

## Findings

1. Medium: the direct `QK_BOOT` fallback is documented as a tri-layer `FUNCTIONS` fallback, but it is not practically reachable from the current `BASE` layer. `FUNCTIONS` is activated by `update_tri_layer_state(state, SYMBOLS, NUMBERS, FUNCTIONS)` in `maple_computing/minidox/LiGoldragon/keymap.c:137`, and `QK_BOOT` is present only as `HIDDEN_BOOT` on `FUNCTIONS` in `maple_computing/minidox/LiGoldragon/keymap.c:15`, `maple_computing/minidox/LiGoldragon/keymap.c:109`, and `maple_computing/minidox/LiGoldragon/keymap.c:110`. However, `BASE` exposes `KC_BSPC`, `QK_LEAD`, and `NUMBERS_*` thumb keys at `maple_computing/minidox/LiGoldragon/keymap.c:43`; it does not expose `SYMBOLS_BSPC` or another `SYMBOLS` entry. `SYMBOLS_BSPC` appears only on `QWERTY_RECOVERED` at `maple_computing/minidox/LiGoldragon/keymap.c:133`, and no inspected current path activates `QWERTY_RECOVERED`. This does not break the leader reset path, but it means README statements at `README.md:55` and `README.md:56` can overstate the availability of a firmware-only direct `QK_BOOT` fallback for normal base-layer use.

## Non-Blocker Observations

- No build blocker found. `nix build .#minidox --no-link --print-out-paths` passed from the current checkout. The checkout is a clean empty jj working-copy commit on top of `f2a45733`.
- The number reorder is correct relative to the pinned QMK MiniDox visual layout. QMK 0.33.8 `keyboard.json` orders `LAYOUT_split_3x5_3` arguments left-hand left-to-right, then right-hand visual left-to-right despite reversed matrix columns. The current `NUMBERS` layer emits `1 2 3 4 5 6 7 8 9 0` when number-bearing positions are sorted by physical x-position: `LSFT_T(KC_1)`, `KC_2`, `KC_3`, `KC_4`, `LGUI_T(KC_5)`, `RGUI_T(KC_6)`, `KC_7`, `KC_8`, `KC_9`, `RSFT_T(KC_0)` in `maple_computing/minidox/LiGoldragon/keymap.c:84` through `maple_computing/minidox/LiGoldragon/keymap.c:88`. The jj diff from the parent shows the same number-bearing slots and mod-tap wrappers were preserved while only tapped number outputs changed.
- The leader one-shot modifier sequences use valid QMK 0.33.8 APIs. `LEADER_ENABLE = yes` is set in `maple_computing/minidox/LiGoldragon/rules.mk:3`; `leader_end_user()` uses `leader_sequence_one_key()` and `set_oneshot_mods(MOD_BIT(KC_*))` at `maple_computing/minidox/LiGoldragon/keymap.c:141` through `maple_computing/minidox/LiGoldragon/keymap.c:152`. Pinned QMK docs and source expose that exact one-shot call shape, and QMK defaults `oneshot_enable` to true on eeconfig initialization. Practical caveat: these leader actions fire when the leader sequence ends, normally after the configured timeout, not immediately on the `s/c/a/g` keypress.
- `leader r e s e t -> reset_keyboard()` remains correct and is not shadowed by the shorter one-shot `s` sequence. QMK 0.33.8 leader processing calls `get_tap_keycode()` before adding keys to the leader sequence, so base mod-taps such as `LCTL_T(KC_R)`, `LALT_T(KC_S)`, and `RALT_T(KC_E)` are matched as `KC_R`, `KC_S`, and `KC_E`. The local sequence checks the five-key reset phrase before one-key sequences at `maple_computing/minidox/LiGoldragon/keymap.c:141` through `maple_computing/minidox/LiGoldragon/keymap.c:152`, and QMK's one-key matcher only matches exactly one stored key.
- The MiniDox diagrams are honest against QMK 0.33.8's own default style. The pinned upstream default keymap uses the same left-hand/right-hand visual ordering, and `keyboard.json` confirms the right half's visual order is represented by reversed matrix columns in the layout metadata. The diagrams are useful as a review surface. Residual risk remains exactly as README states at `README.md:26`: recovered old-binary physical assumptions may still diverge from actual hardware or the old build source.
- README is mostly accurate about build-only/no-flash workflow, review/test cycle, residual `QK_USER_0/1/3` unknowns, and leader commands: see `README.md:3`, `README.md:20` through `README.md:27`, `README.md:39` through `README.md:45`, `README.md:48` through `README.md:56`, and `README.md:58` through `README.md:68`. The notable documentation issue is the tri-layer `QK_BOOT` fallback reachability from base described above.

## Candidate Status

No source/build blocker was found for using this as a cautious first flash/test candidate, provided the flash plan does not rely on the tri-layer `QK_BOOT` fallback being reachable from the base layer. Treat firmware bootloader entry as leader `r e s e t` plus verified physical/controller recovery, not as leader plus an independently reachable `FUNCTIONS` fallback.

## Residual Risks

- `QK_USER_0`, `QK_USER_1`, and `QK_USER_3` remain preserved but behaviorally unknown/inert unless QMK assigns behavior elsewhere; local inspection found no recovered `process_record_user` handling for them.
- Leader actions require timing discipline: with `LEADER_TIMEOUT 350` and `LEADER_PER_KEY_TIMING` in `maple_computing/minidox/LiGoldragon/config.h:4` and `maple_computing/minidox/LiGoldragon/config.h:5`, the reset phrase must be typed with each key inside the timeout and then allowed to end.
- Hardware-specific bootloader, handedness, controller, and actual physical placement were not verified by design. No hardware query, reset, or flash operation was performed.

## Evidence Consulted

- `sed -n '1,220p' AGENTS.md`
- `spirit "(PublicTextSearch [kibord MiniDox keymap])"` returned `(Error [no matching record])`.
- `jj status --no-pager`
- `jj show --stat --no-pager -r f2a45733a42227fba12062eae58efc977f75557a`
- `jj diff --git --no-pager --from f2a45733a42227fba12062eae58efc977f75557a- --to f2a45733a42227fba12062eae58efc977f75557a ...`
- `nix build .#minidox --no-link --print-out-paths`
- `nl -ba` and `rg` over `README.md`, `flake.nix`, `maple_computing/minidox/LiGoldragon/keymap.c`, `config.h`, and `rules.mk`
- `nix eval --impure --raw --expr '(builtins.getFlake "path:/git/github.com/LiGoldragon/kibord").inputs.qmk_firmware.outPath'`, followed by targeted reads of pinned QMK 0.33.8 `keyboards/maple_computing/minidox/rev1/keyboard.json`, `keyboards/maple_computing/minidox/keymaps/default/keymap.c`, `quantum/process_keycode/process_leader.c`, `quantum/leader.c`, `quantum/action.c`, `quantum/action_util.c`, `quantum/eeconfig.c`, `quantum/quantum_keycodes.h`, and `docs/one_shot_keys.md`

## Not Checked

- No hardware behavior, half detection, bootloader entry, reset path on actual controller, flash procedure, or post-flash typing was tested.
- No binary disassembly or old artifact re-analysis was repeated beyond comparing the current commit to its parent for changed number positions.
