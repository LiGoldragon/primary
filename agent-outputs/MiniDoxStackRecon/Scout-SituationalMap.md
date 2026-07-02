# Scout Situational Map

## Task And Scope

Read-only reconnaissance for modernizing the programming stack for a plugged-in MiniDox programmable keyboard before changing typing behavior. Scope included the local `LiGoldragon/kibord` checkout, adjacent local `qmkBinaries` artifacts, read-only USB/device enumeration, and local OS keyboard layout state. No firmware build, bootloader entry, flashing, commits, or shared-source edits were performed.

## Commands And Files Consulted

- `spirit "(PublicTextSearch [MiniDox kibord keyboard firmware])"`: returned `(Error [no matching record])`.
- `/home/li/primary/AGENTS.md` was supplied in the task context.
- `ghq list --full-path | rg -i 'kibord|qmk|zmk|minidox|keyboard|ligoldragon'` located `/git/github.com/LiGoldragon/kibord` and `/git/github.com/LiGoldragon/qmkBinaries`.
- `find /git/github.com/LiGoldragon/kibord ...` found no `AGENTS.md`, `ARCHITECTURE.md`, `README*`, `Makefile`, or `justfile`; only `flake.nix`, `flake.lock`, and `ergodone/coleremak/*` source files were present outside VCS metadata.
- `nl -ba` was used on:
  - `/git/github.com/LiGoldragon/kibord/flake.nix`
  - `/git/github.com/LiGoldragon/kibord/flake.lock`
  - `/git/github.com/LiGoldragon/kibord/ergodone/coleremak/keymap.c`
  - `/git/github.com/LiGoldragon/kibord/ergodone/coleremak/config.h`
  - `/git/github.com/LiGoldragon/kibord/ergodone/coleremak/rules.mk`
  - `/git/github.com/LiGoldragon/qmkBinaries/readme.md`
- `jj status`, `jj log`, `jj show`, `jj file list`, and `jj file show` were used read-only in both repos.
- `nix flake show --no-write-lock-file --allow-import-from-derivation` was used only for flake surface inspection; it exposed a custom `SubWorld` output and did not build.
- `lsusb`, `lsusb -t`, `/sys/bus/usb/devices/*` reads, `udevadm info`, and `localectl status` were used for device and OS state.

## Observed Facts

- The local `kibord` checkout is `/git/github.com/LiGoldragon/kibord`, not under `/home/li/primary`. It is a Jujutsu/Git repository with no working-copy changes. `jj status` reported parent `a0929ef1 main | kibord: add ergodone keymap backup` and an empty working copy commit `57770ad3`.
- `/home/li/primary/protocols/repos-manifest.nota:187-188` lists both `qmkBinaries` and `kibord` as active `LiGoldragon` content repos.
- Current `kibord` non-metadata files are:
  - `/git/github.com/LiGoldragon/kibord/flake.nix`
  - `/git/github.com/LiGoldragon/kibord/flake.lock`
  - `/git/github.com/LiGoldragon/kibord/ergodone/coleremak/config.h`
  - `/git/github.com/LiGoldragon/kibord/ergodone/coleremak/keymap.c`
  - `/git/github.com/LiGoldragon/kibord/ergodone/coleremak/rules.mk`
  - `/git/github.com/LiGoldragon/kibord/ergodone/coleremak/#keymap.c#`
- `flake.nix:5-44` defines non-flake inputs for QMK and QMK submodules: `qmk_firmware`, `ChibiOS`, `ChibiOS-Contrib`, `uGFX`, `googletest`, `lufa`, `v-usb`, `printf`, `kp_boot_32u4`, and `hexdumpSrc`.
- `flake.nix:5-7` pins `qmk_firmware` to `github:qmk/qmk_firmware/bc15c4f4ab81c1e2950dfc1c38cf86dc626573c9`.
- `flake.lock:115-130` records the same `qmk_firmware` revision with `lastModified = 1600364742`, which converts to 2020-09-17.
- Other locked upstream timestamps are old by local evidence: `kp_boot_32u4` has `lastModified = 1559970181` (2019-06-08) at `flake.lock:67-80`; `uGFX` has `lastModified = 1578814645` (2020-01-12) at `flake.lock:146-160`; `lufa` has `lastModified = 1630764587` (2021-09-04) at `flake.lock:83-97`; `ChibiOS-Contrib` has `lastModified = 1630157004` (2021-08-28) at `flake.lock:19-33`.
- The flake's build helper is `mkQmkOS` at `flake.nix:177-222`. It links selected local keymap dir into `./keyboards/${keyboardModel}/keymaps/${keymap}` at `flake.nix:206-209`, runs `make ${keyboardModel}:${keymap}` at `flake.nix:214-216`, and copies `./.build/*hex` to `$out` at `flake.nix:218-220`.
- The build inputs include `dfu-programmer`, `dfu-util`, `git`, Python tooling, AVR packages, optional ARM GCC, and optional `teensy-loader-cli` at `flake.nix:194-204`. There is no documented flash phase or flash command in `kibord`.
- The flake defines a custom `SubWorld` output at `flake.nix:55-303`. `nix flake show --no-write-lock-file --allow-import-from-derivation` showed only `SubWorld: unknown`; no conventional `packages` surface was visible.
- `flake.nix:283-290` defines `LiGoldragon.minidox`, but it sets `iuniksDir = ./maple_computing/minidox/one` and `keyboardModel = "ergodone"`. The `maple_computing/minidox/one` path does not exist in the current tree. It also did not exist in the 2023-09-25 `(drafted minidox)` snapshot: `jj file list -r c89db1dfaf9b` showed only the same `ergodone/coleremak`, `flake.nix`, and `flake.lock` files.
- `flake.nix:291-297` defines `LiGoldragon.ergodone` using `iuniksDir = ./ergodone/coleremak` and `keyboardModel = "ergodone"`.
- `ergodone/coleremak/keymap.c:1-2` is a QMK C keymap using `#include QMK_KEYBOARD_H` and `version.h`.
- `ergodone/coleremak/keymap.c:7-9` defines three layers: `COLEMAK = 0`, `QWERTY = 1`, and `FN = 2`.
- `ergodone/coleremak/keymap.c:27-91` defines all layers with `LAYOUT_ergodox`, not a MiniDox layout macro.
- The firmware Colemak layer emits top-row keycodes `KC_Q KC_W KC_F KC_P KC_G` on the left at `ergodone/coleremak/keymap.c:51-54` and `KC_J KC_L KC_U KC_Y KC_SCLN` on the right at `ergodone/coleremak/keymap.c:61-64`.
- The firmware QWERTY layer emits QWERTY top-row keycodes at `ergodone/coleremak/keymap.c:30-42`.
- The FN layer exposes `CLMK` and `QWRTY` custom keycodes at `ergodone/coleremak/keymap.c:82`; `process_record_user` persists QWERTY and Colemak default layers through `set_single_persistent_default_layer()` at `ergodone/coleremak/keymap.c:105-114`.
- Legacy-looking QMK surfaces in the keymap include `fn_actions` with `ACTION_LAYER_TAP_TOGGLE(FN)` at `ergodone/coleremak/keymap.c:93-95`, `KC_FN1` at multiple locations including `ergodone/coleremak/keymap.c:33`, `RESET` at `ergodone/coleremak/keymap.c:82`, `LEADER_EXTERNS()` at `ergodone/coleremak/keymap.c:183`, and `LEADER_DICTIONARY()` at `ergodone/coleremak/keymap.c:185-229`.
- `ergodone/coleremak/config.h:3` defines `DISABLE_SPACE_CADET_ROLLOVER`.
- `ergodone/coleremak/rules.mk:1-3` disables command mode, enables leader, and sets `BOOTMAGIC_ENABLE = lite`.
- `jj log` in `kibord` shows the current main content commit `a0929ef1a644` dated 2025-07-12, recent build-related commits dated 2025-07-12 and 2025-06-01, a `(drafted minidox)` commit dated 2023-09-25, and input snapshot commits dated 2021-10-07 and 2021-05-01.
- Adjacent repo `/git/github.com/LiGoldragon/qmkBinaries` contains MiniDox hex files:
  - `/git/github.com/LiGoldragon/qmkBinaries/minidox/left/maple_computing_minidox_rev1_LiGoldragon.hex`
  - `/git/github.com/LiGoldragon/qmkBinaries/minidox/right/maple_computing_minidox_rev1_LiGoldragon.hex`
- `/git/github.com/LiGoldragon/qmkBinaries/readme.md:7-9` names the repo "Goldragon's QMK binaries" and has a task to research and document methods to flash pro-micro MiniDox and Ergodox hex binaries.
- `jj log` in `qmkBinaries` shows `5f7fe00d62a9` dated 2026-05-30 with description `qmkBinaries: refresh minidox firmware`. File mtimes for both MiniDox hex files are 2025-07-10.
- USB enumeration sees the plugged-in keyboard as `Bus 003 Device 078: ID feed:3060 That-Canadian MiniDox`.
- Sysfs identifies `/sys/bus/usb/devices/3-1` with `idVendor=feed`, `idProduct=3060`, `manufacturer=That-Canadian`, `product=MiniDox`, `bcdDevice=0001`, and `speed=12`.
- `lsusb -t` shows the MiniDox as two HID interfaces on Bus 003 Port 001, both using `usbhid`.
- `udevadm info` shows `/dev/hidraw0` and `/dev/hidraw1` with `ID_VENDOR_ID=feed` and `ID_MODEL_ID=3060`.
- `localectl status` reports `X11 Layout: us`, `X11 Variant: colemak`, and options `caps:ctrl_modifier, altwin:swap_alt_win`.

## Interpretations

- The active local source is a QMK-over-Nix setup, not ZMK, VIA, or Vial. No local ZMK/VIA/Vial references were found by scoped `rg`.
- The source tree does not currently contain a buildable MiniDox keymap source path matching `flake.nix:287`. The only present keymap source is an Ergodox-layout backup under `ergodone/coleremak`.
- The current `LiGoldragon.minidox` flake target is probably stale or incomplete: it names MiniDox but points at a missing `./maple_computing/minidox/one` keymap path and still uses `keyboardModel = "ergodone"`.
- The attached keyboard's observed user output is explainable by double Colemak mapping. The firmware Colemak layer sends logical Colemak keycodes `Q W F P G J L U Y ;`; under the OS-level `us(colemak)` layout, those keycodes produce `q w t ; d n i l j o`, matching the user's reported `qwt;dniljo`. This suggests the keyboard is already on a firmware Colemak-like layer while the OS also applies Colemak.
- The keymap contains several QMK APIs/macros that are compatibility risks when moving to a newer QMK snapshot. This report does not assert their latest upstream deprecation status from memory; it only flags them as legacy-looking surfaces to verify against the chosen target QMK version.

## Risks

- Source/artifact mismatch: `qmkBinaries` has MiniDox hex artifacts, but `kibord` lacks the corresponding MiniDox keymap source path. A later worker should not assume the hex files are reproducible from current `kibord`.
- Hardware target ambiguity: the plugged-in keyboard enumerates as That-Canadian MiniDox (`feed:3060`), while `kibord` currently builds via `keyboardModel = "ergodone"` and `LAYOUT_ergodox`.
- Modernizing QMK first may require simultaneous keymap API migration because the keymap uses old layer/action/leader/reset surfaces.
- Flashing risk is unresolved. There is no local documented flash command, and `qmkBinaries/readme.md` only says to research/document Pro Micro flashing methods. Do not flash until the exact bootloader, left/right half procedure, and reset/bootloader entry path are confirmed.
- EEPROM/default-layer state matters. The QMK keymap can persist default layer changes; the physical keyboard may be in firmware Colemak independent of source defaults or the OS layout.

## Unknowns

- The exact source used to produce the current plugged-in MiniDox firmware was not found.
- The exact source used to produce the refreshed `qmkBinaries` MiniDox hex files was not found.
- The active bootloader for the attached MiniDox was not identified; no bootloader entry was attempted.
- The current QMK upstream API status was not checked online; out-of-date assessment is limited to local pins, local timestamps, and local source patterns.
- No firmware build was run because that would create outputs and was outside read-only reconnaissance.
- No HID feature reports or EEPROM contents were read; only passive USB/sysfs identity was inspected.

## Recommendation For Next Worker

1. First recover or recreate the missing MiniDox source target before updating pins: add a real `maple_computing/minidox/rev1` or equivalent QMK keymap source and make the flake target name the real QMK keyboard target rather than `ergodone`.
2. Reproduce the existing `qmkBinaries` MiniDox hex from source before changing behavior. If reproduction is impossible, treat the hex repo as an artifact backup only.
3. Choose the modernization target explicitly: current QMK with Nix-packaged `qmk_firmware` and submodules is the shortest path; ZMK/VIA/Vial would be a migration, not a stack refresh.
4. During QMK modernization, inspect and update `fn_actions`, `KC_FN1`, `RESET`, leader macros, and layer-state function signatures against the chosen QMK version.
5. Before flashing, document the MiniDox bootloader and per-half flash commands. Use read-only USB identity (`feed:3060 That-Canadian MiniDox`) as the starting point, but do not infer bootloader commands from it alone.
6. For typing correctness after the stack is modernized, avoid double Colemak. Since the OS is already `us(colemak)`, the keyboard's letter layer should probably send QWERTY-position keycodes, or the OS layout should be changed to plain US while the keyboard sends Colemak.

## Verification Not Performed

- No `nix build`, `make`, `qmk compile`, `qmk flash`, `avrdude`, `dfu-programmer`, `dfu-util`, or bootloader command was run.
- No network freshness check against upstream QMK/ZMK/VIA/Vial was performed.
- No private scopes were opened.
