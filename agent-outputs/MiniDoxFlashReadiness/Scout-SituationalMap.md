# MiniDox Flash Readiness Situational Map

Task: read-only flash-readiness reconnaissance for `/git/github.com/LiGoldragon/kibord` and the currently plugged-in MiniDox keyboard. No files were changed except this report; no flash, reset, or bootloader-entry action was performed.

## Commands And Sources Consulted

- Local repo files: `README.md`, `flake.nix`, `flake.lock`, `maple_computing/minidox/LiGoldragon/keymap.c`, `config.h`, `rules.mk`.
- Local searches: `rg -n "QK_BOOT|RESET|QK_BOOTLOADER|BOOTLOADER|bootloader|leader|LEADER|combo|COMBO|tap_dance|TAP_DANCE|DANCE|BOOTMAGIC|MAGIC|COMMAND|IS_COMMAND|keymap_config|process_combo|process_record|LT\\(|MO\\(|TG\\(|TO\\(|DF\\(" maple_computing/minidox flake.nix README.md`.
- Version state: `jj status`, `jj log -r @`, `jj log -r c08bb77661ac24397cd53c432890280715c59fc2`.
- USB observations: `lsusb`, `lsusb -t`, `udevadm info --query=property --name=/dev/hidraw*`, `udevadm info --query=property --path=/sys/bus/usb/devices/3-1`, `/dev/input/by-id`.
- Upstream QMK locked source via GitHub raw/API at commit `b1093e9da5f27253f3db692352daf5cf4ad5b98d`, from `flake.lock`.
- QMK docs: `docs/flashing.md` at locked QMK commit and current official `https://docs.qmk.fm/flashing`; split handedness docs at `https://docs.qmk.fm/features/split_keyboard`.
- Spirit public intent query: `spirit "(PublicTextSearch [MiniDox keyboard flash QMK kibord])"` returned `(Error [no matching record])`.

## Repo State

- `/git/github.com/LiGoldragon/kibord` has no repo-local `AGENTS.md` found by `find /git/github.com/LiGoldragon/kibord -name AGENTS.md`.
- `jj status` reports a clean working copy. Current working copy commit is empty `f76a117c63c3a40ac01410500bd11477e12baff4`; its parent is `c08bb77661ac24397cd53c432890280715c59fc2` on `main` with description `kibord: restore minidox firmware colemak`.
- `README.md:3` says MiniDox is build-only for now and not to flash until bootloader, half selection, and reset procedure are identified. `README.md:21-26` repeats the pre-flash requirements.

## Required Answer 1: Build Target And Keymap Command

Observed:

- `README.md:7` says MiniDox source lives at `maple_computing/minidox/LiGoldragon` and builds QMK target `maple_computing/minidox/rev1` from QMK `0.33.8`.
- `README.md:11-15` gives the repo build command `nix build .#minidox` and expected hex name `maple_computing_minidox_rev1_LiGoldragon.hex`.
- `flake.nix:6-8` pins `qmk_firmware` to `github:qmk/qmk_firmware/0.33.8`.
- `flake.lock:131-146` locks QMK to commit `b1093e9da5f27253f3db692352daf5cf4ad5b98d` with original ref `0.33.8`.
- `flake.nix:168-170` derives the keymap name from the basename of `iuniksDir`, so `./maple_computing/minidox/LiGoldragon` becomes keymap `LiGoldragon`.
- `flake.nix:190-194` links that directory into `./keyboards/maple_computing/minidox/keymaps/LiGoldragon`.
- `flake.nix:199-205` runs `make ${keyboardModel}:${keymap}` and copies `./.build/*hex` to `$out`.
- `flake.nix:268-275` sets `keyboardModel = "maple_computing/minidox/rev1"` and `keymapKeyboardModel = "maple_computing/minidox"` for `LiGoldragon.minidox`.

Answer:

- Repo-supported build command: `nix build .#minidox`.
- Exact QMK make target inside that build: `make maple_computing/minidox/rev1:LiGoldragon`.
- Equivalent QMK CLI form, if the keymap has first been placed in the QMK tree as the flake does: `qmk compile -kb maple_computing/minidox/rev1 -km LiGoldragon`.

## Required Answer 2: Programmed Bootloader Entry Key Or Chord

Observed:

- `maple_computing/minidox/LiGoldragon/keymap.c:3-8` defines only `BASE`, `LOWER`, `RAISE`, and `ADJUST`.
- `keymap.c:10-11` defines only `LOWER_KEY MO(LOWER)` and `RAISE_KEY MO(RAISE)`.
- `keymap.c:18-44` contains only ordinary keycodes and transparent placeholders across all layers; the `ADJUST` layer at `keymap.c:39-44` is entirely `_______`.
- `keymap.c:47-49` only updates tri-layer state.
- `maple_computing/minidox/LiGoldragon/rules.mk:1-2` sets `COMMAND_ENABLE = no` and `BOOTMAGIC_ENABLE = no`.
- Scoped search found no `QK_BOOT`, `RESET`, `QK_BOOTLOADER`, leader dictionary, combo processing, tap dance, or `process_record` in `maple_computing/minidox`.

Answer:

- No programmed bootloader entry key, leader sequence, combo, tap dance, or chord is present in the current MiniDox keymap.
- The user's suspected leader/chord is not supported by the current MiniDox files. The nearby ErgoDone keymap has leader/reset material, but the MiniDox keymap does not.

## Required Answer 3: Physical Reset Or Bootloader Fallback

Confirmed repo/device/upstream evidence:

- Upstream MiniDox readme at QMK commit `b1093e9...`, `keyboards/maple_computing/minidox/readme.md:7-8`, says the maintainer/manufacturer is That-Canadian and hardware supported is `MiniDox PCB rev1 Pro Micro`.
- Upstream `keyboards/maple_computing/minidox/rev1/keyboard.json:2-8` declares `keyboard_name` `MiniDox`, manufacturer `That-Canadian`, USB VID `0xFEED`, PID `0x3060`, device version `0.0.1`.
- Upstream `keyboard.json:15-21` declares split enabled, serial pin `D0`, and `development_board` `promicro`.
- Upstream QMK `data/mappings/defaults.hjson:68-71` maps `promicro` to `bootloader = "caterina"`, `pin_compatible = "promicro"`, and `processor = "atmega32u4"`.
- QMK flashing docs at locked commit `docs/flashing.md:67-75` say Pro Micro or clone boards use Caterina or a variant and need `BOOTLOADER = caterina`.
- QMK flashing docs at locked commit `docs/flashing.md:87-92` say Caterina bootloader entry methods are `QK_BOOT`, reset button if available, or short RST to GND; there is a 7-second flash window and some variants require reset twice within 750 ms.

Inference:

- The likely physical fallback for this plugged-in MiniDox is to press a reset button on the PCB/controller if present, or briefly short `RST` to `GND` on the Pro Micro. Because some Caterina variants require a double reset, the human-guided test should watch USB enumeration while trying the reset procedure.
- This inference is strong for the QMK target because upstream MiniDox rev1 is explicitly Pro Micro and QMK maps `promicro` to Caterina. It is not yet confirmed for the exact physical controller soldered into this keyboard until bootloader-mode USB identity is observed.

## Required Answer 4: Current Plugged-In USB Evidence

Observed normal-mode USB device:

- `lsusb` shows `Bus 003 Device 082: ID feed:3060 That-Canadian MiniDox`.
- `lsusb -t` shows that device on Bus 003 Port 001 with two HID interfaces, both handled by `usbhid`, at 12M.
- `udevadm info --path=/sys/bus/usb/devices/3-1` shows `PRODUCT=feed/3060/1`, `ID_VENDOR=That-Canadian`, `ID_VENDOR_ID=feed`, `ID_MODEL=MiniDox`, `ID_MODEL_ID=3060`, `ID_REVISION=0001`, and `ID_USB_INTERFACES=:030101:030000:`.
- `/dev/hidraw0` and `/dev/hidraw1` both map to `FEED:3060` and `That-Canadian_MiniDox`; `/dev/hidraw2` is a Synaptics I2C device, not the keyboard.
- `/dev/input/by-id` exposes `usb-That-Canadian_MiniDox-event-kbd`, `usb-That-Canadian_MiniDox-hidraw`, and interface-1 mouse/joystick/event symlinks.
- No `/dev/ttyACM*` or `/dev/ttyUSB*` device was present in the scoped `/dev` check, so the keyboard was not observed in Caterina serial bootloader mode.

Interpretation:

- The plugged-in device identity matches upstream MiniDox normal firmware VID/PID (`FEED:3060`) from `keyboard.json:5-8`.
- Current evidence confirms the keyboard is plugged in and running normal QMK HID firmware. It does not reveal the bootloader identity because no reset/bootloader entry was performed.

## Required Answer 5: Handedness And Half-Specific Flashing Risks

Observed:

- Upstream MiniDox readme `keyboards/maple_computing/minidox/readme.md:25-27` says the two boards are identical and firmware differentiates left/right using either `EE_HANDS` or by define.
- Local `maple_computing/minidox/LiGoldragon/config.h:1-3` only sets `TAPPING_TERM 200`; it does not set `EE_HANDS`, `MASTER_LEFT`, or `MASTER_RIGHT`.
- Local scoped search found no handedness defines in `maple_computing/minidox`.
- `flake.nix:268-275` defines only one MiniDox package/hex; it does not define separate left/right flash artifacts or EEPROM-handedness flash targets.
- QMK split docs say Caterina Pro Micro split handedness can be flashed with `avrdude-split-left` and `avrdude-split-right` when using EEPROM handedness, and also document define-based handedness/default behavior. This repo has not documented which strategy this physical board currently relies on.
- `README.md:23-25` explicitly requires identifying each half's controller/bootloader, confirming which half is connected over USB and how handedness is selected, and flashing one half at a time only after matching bootloader and artifact are known.

Risks/unknowns before flashing:

- Which physical half is currently connected over USB is not proven by USB alone.
- Whether the existing keyboard was flashed with default-left behavior, define-based handedness, or EEPROM handedness is not proven.
- Whether both halves use identical Pro Micro-compatible controllers and the same bootloader variant is not proven from normal-mode USB enumeration.
- The current repo build produces one firmware hex and has no documented half-specific flash command; using a split-left/right flash target without intentionally adopting `EE_HANDS` would be a behavior decision, not a confirmed recovery step.
- TRRS safety remains relevant: `README.md:26` says to disconnect USB power before plugging/unplugging TRRS.

## Required Answer 6: Documentation And Tooling Gap

Gap:

- The repo already documents build-only status and pre-flash safety, but it does not yet document the current conclusion that MiniDox has no programmed bootloader key/chord and likely requires physical Pro Micro reset/shorting for bootloader entry.
- It also lacks a documented non-flashing USB identity test: expected normal-mode identity `feed:3060 That-Canadian MiniDox`; expected bootloader-mode evidence to collect; and a note that no `/dev/ttyACM*`/`ttyUSB*` appeared before reset.
- It lacks half/handedness procedure documentation: which half to connect first, how to identify left/right, whether to keep default-left behavior or deliberately move to `EE_HANDS`, and what flash command will be used for each half.

Recommended implementation-worker next step:

- Make a non-flash documentation update in `README.md` capturing: build command `nix build .#minidox`, raw target `make maple_computing/minidox/rev1:LiGoldragon`, current normal USB identity, absence of programmed bootloader entry, likely Pro Micro/Caterina physical reset fallback, and remaining human-guided bootloader/handedness checks.
- Do not add a scripted flash target yet; the bootloader-mode VID/PID/serial device and half procedure are still unobserved.

## Go/No-Go Recommendation

- Go for a non-flash documentation update now. The evidence is sufficient to document current build command, no programmed bootloader key/chord, normal-mode USB identity, and likely physical reset fallback with uncertainty clearly labeled.
- No-go for actual flashing now. The bootloader-mode identity, reset procedure on the exact hardware, connected half, and handedness strategy remain unconfirmed.
- Go for a human-guided flash-mode test next, if desired, with no firmware write: have the human use the physical reset fallback while an agent watches `lsusb` and `/dev/ttyACM*`/`/dev/ttyUSB*` for the brief Caterina bootloader window. The likely physical action is pressing the reset button if present, or briefly shorting `RST` to `GND`; a double reset may be needed for some Caterina variants.
