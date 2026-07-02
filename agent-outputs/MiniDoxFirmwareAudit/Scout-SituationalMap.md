# MiniDox Firmware Audit Situational Map

Task: read-only audit of `/git/github.com/LiGoldragon/kibord` commit `c71c7787338f0ed76dc5d16547f6c9e971ba767c`, reported as enabling QMK Leader bootloader entry for MiniDox, adding fallback `QK_BOOT`, reordering numbers, and updating README. No firmware flashing, hardware reset, commit, push, or source edits were performed.

## Findings

No blockers found that should prevent a cautious first flashing workflow, assuming the pre-flash hardware facts are identified first as the README says. The build succeeds, and the Leader and `QK_BOOT` bootloader paths are QMK 0.33.8-compatible.

Actionable non-blocking notes:

- The implementation report overstates the commit contents for the number row. In commit `c71c7787`, `maple_computing/minidox/LiGoldragon/keymap.c:33` has conventional `KC_1` through `KC_0`, and the parent already had the same row. The current state matches the requested physical direction, but this commit did not itself perform that reorder.
- `README.md:25` accurately describes the Leader sequence at a high level, but QMK Leader normally runs `leader_end_user()` after the Leader timeout/task end rather than instantly on the final key. With `LEADER_TIMEOUT 350` and `LEADER_PER_KEY_TIMING` in `config.h:4-5`, the expected behavior is: tap `QK_LEAD`, type `r e s e t` within the per-key window, then bootloader entry happens shortly after the final `t`.
- The direct fallback `QK_BOOT` at `keymap.c:42` is tucked behind `LOWER+RAISE` on `ADJUST`, but it is physically adjacent to the documented `QK_LEAD` key at `keymap.c:41`. Ordinary accidental activation is unlikely because `ADJUST` requires both layer keys, but a miss while deliberately entering bootloader mode could trigger direct bootloader entry.

## Observed Facts

- Workspace instructions consulted: `/home/li/primary/AGENTS.md`.
- Repo-local instructions: `find /git/github.com/LiGoldragon/kibord -name AGENTS.md -print` returned no nested `AGENTS.md`.
- Spirit query: `spirit "(PublicTextSearch [MiniDox QMK firmware bootloader leader])"` returned `(Error [no matching record])`; no public intent record changed this audit scope.
- Version-control state: `jj status --no-pager` in `/git/github.com/LiGoldragon/kibord` reported a clean working copy, with parent commit `c71c7787 main | kibord: restore minidox bootloader entry`.
- Target commit summary: `jj show -r c71c7787338f0ed76dc5d16547f6c9e971ba767c --no-pager --stat` reported changes only to:
  - `README.md`
  - `maple_computing/minidox/LiGoldragon/config.h`
  - `maple_computing/minidox/LiGoldragon/keymap.c`
  - `maple_computing/minidox/LiGoldragon/rules.mk`
- Build check: `nix build .#minidox --no-link` exited 0. A second check, `nix build .#minidox --no-link --print-out-paths`, exited 0 and printed `/nix/store/s19hsqnfdds9948zs2qc8mfnla126wns-qmk-os-b1093e9`.
- No `result` symlink appeared in the repo after the no-link builds; `jj status --no-pager` remained clean.

## Source Facts

- `flake.lock:131-146` locks `qmk_firmware` to upstream QMK `0.33.8`, revision `b1093e9da5f27253f3db692352daf5cf4ad5b98d`.
- `flake.nix:269-276` builds MiniDox through `mkQmkOS` with `keyboardModel = "maple_computing/minidox/rev1"` and keymap source `./maple_computing/minidox/LiGoldragon`.
- `maple_computing/minidox/LiGoldragon/rules.mk:3` sets `LEADER_ENABLE = yes`.
- `maple_computing/minidox/LiGoldragon/config.h:4-5` sets `LEADER_TIMEOUT 350` and `LEADER_PER_KEY_TIMING`.
- `maple_computing/minidox/LiGoldragon/keymap.c:39-44` places `QK_LEAD` on `ADJUST` left home-row pinky and `QK_BOOT` on `ADJUST` left bottom-row pinky.
- `maple_computing/minidox/LiGoldragon/keymap.c:51-54` implements `leader_end_user()` with `leader_sequence_five_keys(KC_R, KC_E, KC_S, KC_E, KC_T)` calling `reset_keyboard()`.
- `maple_computing/minidox/LiGoldragon/keymap.c:47-49` uses `update_tri_layer_state(state, LOWER, RAISE, ADJUST)`, so `ADJUST` requires `LOWER` and `RAISE` together.
- `maple_computing/minidox/LiGoldragon/keymap.c:32-37` has the `RAISE` number row as `KC_1` through `KC_0` left-to-right. `jj file show -r 'c71c7787338f0ed76dc5d16547f6c9e971ba767c-' .../keymap.c` showed the same row in the parent.
- Upstream QMK 0.33.8 `docs/features/leader_key.md` documents `LEADER_ENABLE = yes`, adding `QK_LEAD`, `leader_end_user()`, `LEADER_TIMEOUT`, `LEADER_PER_KEY_TIMING`, and `leader_sequence_five_keys`.
- Upstream QMK 0.33.8 `quantum/process_keycode/process_quantum.c` handles `QK_BOOTLOADER` by calling `reset_keyboard()` and `QK_REBOOT` by calling `soft_reset_keyboard()`.
- Upstream QMK 0.33.8 `quantum/quantum.c` defines `reset_keyboard()` as `shutdown_quantum(true); bootloader_jump();`.
- Upstream QMK 0.33.8 `platforms/avr/bootloaders/caterina.c` defines `bootloader_jump()` by writing the Caterina boot key at `0x0800`, enabling a watchdog timeout, and waiting for reset.
- Upstream QMK 0.33.8 `keyboards/maple_computing/minidox/rev1/keyboard.json` says `development_board` is `promicro`, and QMK docs for Caterina list `QK_BOOT`, PCB reset button, and shorting `RST` to `GND` as bootloader entry methods.
- Upstream QMK 0.33.8 default MiniDox keymap places `QK_BOOT` on the same `ADJUST` left bottom-row pinky physical position, supporting the README claim at `README.md:26`.

## Interpretations

- The Leader implementation is compatible with the locked QMK version. It uses the documented feature flag, keycode, callback, and five-key sequence helper.
- Calling `reset_keyboard()` from `leader_end_user()` is the same bootloader path used by `QK_BOOTLOADER`/`QK_BOOT` in this QMK revision, not a separate soft reboot path. `bootloader_jump()` is the lower-level platform function and is reached through `reset_keyboard()`.
- `QK_LEAD` is usable from `ADJUST`: press both thumb layer keys to enter `ADJUST`, tap left home-row pinky, release layer keys, then type the base-layer sequence. Leader state persists after releasing the layer keys.
- The fallback `QK_BOOT` is unlikely to be hit during normal typing because it requires both `LOWER` and `RAISE`, but it is not impossible to hit while deliberately using nearby `QK_LEAD`.
- The documentation is appropriately cautious about unverified hardware. `README.md:3` says not to flash until bootloader, half selection, and reset procedure are identified; `README.md:30-37` calls flashing out of scope and warns about controller, handedness, half-specific flashing, TRRS hot-plugging, reference hex files, and Caterina uncertainty.

## Checks Run

- `sed -n '1,220p' AGENTS.md`
- `sed -n '1,220p' /home/li/primary/.agents/skills/spirit-query/SKILL.md`
- `sed -n '1,240p' /home/li/primary/.agents/skills/version-control/SKILL.md`
- `spirit "(PublicTextSearch [MiniDox QMK firmware bootloader leader])"`
- `find /git/github.com/LiGoldragon/kibord -name AGENTS.md -print`
- `jj status --no-pager`
- `jj log -r c71c7787338f0ed76dc5d16547f6c9e971ba767c --no-pager --summary`
- `jj show -r c71c7787338f0ed76dc5d16547f6c9e971ba767c --no-pager --stat`
- `jj diff -r c71c7787338f0ed76dc5d16547f6c9e971ba767c --no-pager -- README.md maple_computing/minidox/LiGoldragon/keymap.c maple_computing/minidox/LiGoldragon/config.h maple_computing/minidox/LiGoldragon/rules.mk`
- `jj file show -r 'c71c7787338f0ed76dc5d16547f6c9e971ba767c-' maple_computing/minidox/LiGoldragon/keymap.c`
- `nix build .#minidox --no-link`
- `nix build .#minidox --no-link --print-out-paths`
- `nl -ba`/`rg` reads of `README.md`, `flake.nix`, `flake.lock`, and MiniDox keymap/config/rules files.
- `curl -fsSL` reads of locked upstream QMK 0.33.8 source/docs at revision `b1093e9da5f27253f3db692352daf5cf4ad5b98d`.

## Unknowns And Residual Risks

- Hardware was not inspected or touched. Actual controller, bootloader, serial/USB half, handedness mechanism, and recovery/reset procedure remain unverified.
- The audit did not flash hardware, enter bootloader, or test key behavior on the physical keyboard.
- The build was verified through Nix only; no independent QMK CLI compile outside the flake was run.
- Because `LEADER_TIMEOUT` is 350 ms with per-key timing, a slow `r e s e t` entry will fail silently rather than entering bootloader. This is a usability risk, not a compile or API blocker.
