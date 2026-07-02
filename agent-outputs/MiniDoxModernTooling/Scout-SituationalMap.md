# MiniDox Modern Tooling Situational Map

Task: scout current 2026 ways to build, maintain, and flash a MiniDox or similar QMK-compatible split keyboard for a user who wants modern tooling, minimal repository bloat, and a low-risk recovery path before typing on an unknown-current-firmware MiniDox. Scope is public/project research only; no claims about the user's local repository.

## Commands and Sources Consulted

- Spirit intent query: `spirit "(PublicTextSearch [MiniDox keyboard firmware tooling QMK ZMK])"` returned `(Error [no matching record])`.
- QMK docs: External Userspace, setup, CLI, Configurator, flashing, Bootmagic, split keyboard, Docker, GitHub Userspace, Zadig driver, ISP flashing.
- QMK project/API: `qmk/qmk_firmware`, `qmk/qmk_userspace`, `qmk/qmk_toolbox`, `qmk_cli` PyPI, GitHub API for MiniDox contents and commits.
- VIA docs: `caniusevia.com` specification, supported keyboards, firmware downloads.
- Vial docs and GitHub: `get.vial.today`, `vial-kb/vial-gui`, `vial-kb/vial-qmk`.
- ZMK docs: introduction, supported hardware, split keyboards.
- Local shell probes used only network reads: `curl`, `jq`, `git ls-remote`.

## Observed Facts

- QMK still officially supports MiniDox under `keyboards/maple_computing/minidox/rev1`. The current upstream `keyboard.json` says `keyboard_name: MiniDox`, `development_board: promicro`, split enabled with serial pin `D0`, community layout `split_3x5_3`, and features include `bootmagic: false`, `mousekey: true`, `extrakey: true`, `command: true`. Source: `https://raw.githubusercontent.com/qmk/qmk_firmware/master/keyboards/maple_computing/minidox/rev1/keyboard.json`.
- QMK's hosted keyboard API returns MiniDox metadata for `maple_computing/minidox/rev1` with `last_updated: 2026-06-26 13:22:46 GMT`. Command: `curl -fsSL 'https://keyboards.qmk.fm/v1/keyboards/maple_computing/minidox/rev1/info.json'`.
- QMK has aliases from `minidox/rev1` and `maple_computing/minidox` to `maple_computing/minidox/rev1`. Source command: `curl .../data/mappings/keyboard_aliases.hjson | grep -n -C 2 'minidox'`.
- QMK Firmware tag `0.33.8` points to commit `b1093e9d...` dated `2026-06-26T13:20:10Z`; `master` matched that commit during scouting. Command: `git ls-remote --tags https://github.com/qmk/qmk_firmware.git ...` and GitHub commits API.
- QMK's breaking-change process says `develop` merges to `master` on a 3-month cadence, lists past changes through `2026 May 31`, and schedules the next breaking change for `2026-08-30`. Source: `https://docs.qmk.fm/breaking_changes`.
- QMK CLI is current enough to be active: PyPI `qmk` latest is `1.2.0`, uploaded `2025-11-27T12:59:29Z`. Source command: `curl -fsSL 'https://pypi.org/pypi/qmk/json' | jq ...`.
- QMK Toolbox latest stable page showed `0.3.3` released `2026-06-13`; beta release was dated `2026-06-19`. Source: `https://github.com/qmk/qmk_toolbox/releases`.
- QMK Configurator is official and online. Docs say it generates QMK `.hex` or `.bin` firmware files, but cannot build for a different controller than the keyboard was designed for. Source: `https://docs.qmk.fm/newbs_building_firmware_configurator`.
- Configurator step-by-step docs say it can download a QMK keymap JSON for future changes and then compile/download firmware. Source: `https://docs.qmk.fm/configurator_step_by_step`.
- QMK External Userspace is official: docs say QMK supports keymaps outside the main `qmk_firmware` repository without forking QMK. It mirrors QMK's repository structure. Source: `https://docs.qmk.fm/newbs_external_userspace`.
- External Userspace still has a local-build caveat: docs say CLI commands for manipulating External Userspace definitions currently need a copy of QMK Firmware too. The same page uses `qmk config user.overlay_dir=...`, `qmk userspace-add`, and `qmk userspace-compile`.
- QMK GitHub Userspace workflow is an official clone-light local option. Docs frame it as an out-of-tree repository built by GitHub Actions, avoiding a space-consuming local build environment, using container `ghcr.io/qmk/qmk_cli`, checking out QMK in CI, and downloading artifacts for flashing. Source: `https://docs.qmk.fm/newbs_building_firmware_workflow`.
- QMK Docker workflow is official but still starts by acquiring a local `qmk_firmware` clone with submodules. Source: `https://docs.qmk.fm/getting_started_docker`.
- QMK setup docs still default to `qmk setup`; docs allow `qmk setup -H <path>` for choosing the QMK home. Source: `https://docs.qmk.fm/newbs_getting_started`.
- VIA requires a QMK firmware with VIA support plus a keyboard definition keyed by USB VID/PID. VIA docs say definitions are JSON in the VIA GitHub repo/website and VID/PID identify the keyboard. Source: `https://www.caniusevia.com/docs/specification/`.
- VIA public firmware downloads were last updated `4/7/2026`. Scoped page search found no `minidox` or `maple` matches in VIA firmware downloads/supported keyboards pages. Sources: `https://www.caniusevia.com/docs/download_firmware/`, `https://www.caniusevia.com/docs/supported_keyboards/`.
- Vial GUI latest listed release is `v0.7.5`, released `2025-08-02`; that release added Colemak DH layouts. Sources: `https://get.vial.today/changelog/release-0.7.5.html`, `https://github.com/vial-kb/vial-gui/releases`.
- Vial porting docs require a `keymaps/vial` keymap, `VIA_ENABLE = yes`, `VIAL_ENABLE = yes`, a `vial.json`, generated keyboard UID, and an unlock combo unless insecure mode is used. Source: `https://get.vial.today/docs/porting-to-vial.html`.
- `vial-kb/vial-qmk` contains `keyboards/maple_computing/minidox` on branch `vial`, but the MiniDox keymaps there are only `bepo` and `default`; `keymaps/vial` returned 404. Commands: GitHub API contents for `vial-kb/vial-qmk/.../minidox`.
- ZMK docs identify ZMK as MIT firmware on Zephyr, designed for power efficiency, flexibility, and wired/wireless input devices. They list user configuration repositories as supported. Source: `https://zmk.dev/docs`.
- ZMK docs explicitly say AVR/8-bit chips are not supported; ATmega32U4 controllers such as SparkFun Pro Micro and Elite-C are not supported. Source: `https://zmk.dev/docs/hardware`.
- ZMK split docs say split parts need separate firmware files; Bluetooth split is mature, full-duplex wired UART is recent/early-adopter, and TRRS/TRS hot-plugging can damage controllers if powered. Source: `https://zmk.dev/docs/features/split-keyboards`.
- QMK flashing docs say bootloaders vary; QMK Toolbox aims to support many, and QMK CLI can flash with `qmk flash -kb <keyboard> -km <keymap>`. Source: `https://docs.qmk.fm/flashing`.
- For Pro Micro/Caterina, QMK flashing docs say Pro Micro/clones use Caterina or variants with AVR109 over virtual serial; `BOOTLOADER = caterina`; compatible flashers include QMK Toolbox and `avrdude`; bootloader entry can be `QK_BOOT`, reset button, or shorting RST to GND, with a 7-second window and some variants needing a double reset within 750 ms. Source: `https://docs.qmk.fm/flashing`.
- QMK split docs warn both halves must use the same MCU family and TRRS cables are not hot-pluggable when VCC is carried; disconnect USB before unplugging/plugging TRRS. Source: `https://docs.qmk.fm/features/split_keyboard`.
- QMK Bootmagic docs say Bootmagic can jump into bootloader when holding a configured key while plugging in, but MiniDox's current upstream config has `bootmagic: false`; enabling it would be a new firmware choice. Source: `https://docs.qmk.fm/features/bootmagic` and MiniDox `keyboard.json`.
- QMK Zadig docs say Windows flashing may need bootloader drivers; Caterina/Pro Micro and HalfKay/Teensy are exceptions that do not require Zadig. They warn not to proceed in Zadig if the keyboard is not in bootloader mode and `HidUsb` devices are listed. Source: `https://docs.qmk.fm/driver_installation_zadig`.
- QMK ISP guide says if an AVR bootloader is corrupted or must be changed, USB flashing cannot overwrite the currently running bootloader; ISP flashing is the fallback. It lists Pro Micro/Arduino/Teensy/USBtiny/USBasp options and warns incorrect AVR fuses can make the MCU practically unrecoverable without high-voltage programming. Source: `https://docs.qmk.fm/isp_flashing_guide`.

## Recommendation Matrix

- QMK Configurator + QMK Toolbox: High MiniDox applicability if the physical board is stock Pro Micro-compatible MiniDox rev1. MiniDox is in QMK API and Configurator should see `maple_computing/minidox/rev1`. No local QMK clone; save/export JSON. Download `.hex`, flash with QMK Toolbox. Best first low-friction path for a simple Colemak/Colmac keymap if no custom C is needed. Fails if controller differs from Pro Micro design.
- QMK External Userspace + QMK CLI: High applicability. Official modern maintenance path for personal keymaps outside `qmk_firmware`. Keeps user code small, but local builds still need a QMK firmware checkout. Use a current tag/commit; consider shallow clone manually if not using `qmk setup`, but validate submodules and `qmk doctor`. Flash with `qmk compile`/`qmk flash` or build then flash with Toolbox. Best maintainable path when custom C, repeatable builds, or local iteration matter.
- QMK GitHub Userspace / CI container: High applicability for JSON-style keymaps and modest custom user code. Small local repo; QMK checkout happens in GitHub Actions container. Download CI artifact and flash locally with Toolbox. Best answer to "do not clone giant historical repos locally" while staying official. Slower turnaround and requires GitHub workflow.
- QMK Docker/Podman: Technically applicable. Reproducible environment but still requires local `qmk_firmware` clone with submodules. `util/docker_build.sh ...` can build/flash or produce an artifact. Useful for reproducibility, not for avoiding local clone weight.
- VIA: Not currently turnkey for MiniDox from public VIA lists. Could be ported if firmware plus definition are created. After initial VIA firmware, remaps are GUI/no rebuild. Not the safest first step for unknown MiniDox unless a known-good MiniDox VIA firmware is found or ported and tested.
- Vial: `vial-qmk` has MiniDox tree but no ready `keymaps/vial` found. Port is possible but not turnkey. Needs Vial fork/build, `vial.json`, UID, unlock combo; after flashing, GUI remaps. Attractive after baseline recovery is proven, but higher first-flash risk and porting work. Vial GUI latest is 0.7.5 from 2025-08-02.
- ZMK: Not applicable to a stock Pro Micro/ATmega32U4 MiniDox. Applicable only after controller swap to supported 32-bit boards and likely shield/board work. Modern user config repos and wireless workflows. Good for a future wireless rebuild, not for this wired unknown existing MiniDox unless hardware changes are intended.

## Safest Modern Path to Propose

Facts support a two-stage path:

1. Establish hardware/bootloader identity before flashing. Inspect the controller markings if possible, connect one half at a time, identify normal USB device and bootloader USB device, and confirm whether it behaves like Pro Micro/Caterina, Atmel DFU/Elite-C, Teensy/HalfKay, or something else. Do not hot-plug the TRRS cable while either half is powered.
2. Build a stock-safe baseline firmware for `maple_computing/minidox/rev1` with Colemak/Colmac key placement using QMK Configurator or a QMK JSON keymap. Save the JSON artifact before flashing.
3. Flash only the USB-connected half first, with QMK Toolbox open and the correct firmware loaded. For Pro Micro/Caterina, use Auto-Flash and the reset/double-reset window; for Atmel DFU, use the matching DFU path; for Teensy, use HalfKay/Teensy loader path.
4. Keep a known-good fallback artifact: upstream `default` MiniDox firmware built from current QMK plus the user's JSON/keymap. If both halves need firmware or handedness EEPROM, use QMK's split flash targets only after the bootloader path is known.
5. After a successful baseline, move maintenance to QMK External Userspace. If local clone size is the concern, prefer the official GitHub Userspace/Actions workflow or a manually shallow, tagged QMK checkout validated with `qmk doctor`. Do not use an old personal QMK fork as the source of truth.

My concise recommendation: start with QMK Configurator or GitHub Userspace for the first low-risk build, flash with current QMK Toolbox, then keep the durable keymap in QMK External Userspace. Do not start with VIA/Vial/ZMK for the first flash unless hardware inspection reveals a non-stock controller or a known-good MiniDox-specific firmware already installed.

## Recovery and Rollback Notes

- A MiniDox with Pro Micro-compatible controllers should normally be recoverable through the bootloader even if the application firmware is wrong, as long as the bootloader remains intact. For Caterina, the flash window is short; QMK Toolbox Auto-Flash is safer than manually timing `avrdude`.
- Firmware backup by reading flash is only a possibility, not a guaranteed rollback. It depends on controller, bootloader access, and lock bits. If attempted on AVR, use the exact detected programmer/port and a read operation before writing; do not count on the read image being portable or restorable if lock bits block reads.
- The real low-risk fallback is bootloader entry plus a known-good QMK build for the exact keyboard/controller. ISP flashing is the hardware recovery path if an AVR bootloader is damaged, but it requires wiring to reset/SCLK/MOSI/MISO/VCC/GND and careful fuse handling.
- Avoid changing bootloaders or fuses during the first pass. The current task is to update the keyboard programming stack, not to optimize bootloader behavior.
- On Windows, avoid Zadig unless the keyboard is definitely in bootloader mode. QMK docs warn that changing the driver for the normal HID keyboard device can make the keyboard stop typing until the driver is removed.

## Interpretations

- The least bit-rotten path in 2026 is not an old fork of `qmk_firmware`; it is current upstream QMK plus either Configurator JSON, external userspace, or GitHub Actions userspace.
- "Avoiding huge historical clones" is best satisfied by Configurator or GitHub Actions userspace. If local custom C iteration is needed, a local QMK checkout remains the normal QMK path; shallow/tagged checkout is probably workable but was not found as the official `qmk setup` default.
- VIA/Vial improve day-to-day remapping after the first working flash, but they increase first-flash uncertainty for MiniDox because public VIA does not list it and Vial lacks a ready MiniDox `vial` keymap in the checked branch.
- ZMK is a separate firmware ecosystem for modern 32-bit/wireless builds. It is not a drop-in replacement for a stock MiniDox rev1 Pro Micro.

## Likely Relevant Files / Surfaces for Downstream Workers

- QMK keyboard target: `maple_computing/minidox/rev1`
- QMK layout: `LAYOUT_split_3x5_3`
- QMK source path: `keyboards/maple_computing/minidox/rev1/keyboard.json`
- QMK aliases: `minidox/rev1` and `maple_computing/minidox`
- External userspace layout path if used: `keyboards/maple_computing/minidox/keymaps/<keymap>/`
- JSON/Configurator path if used: a saved QMK Configurator `.json` for the MiniDox target
- Flashing tools to install/check: `qmk` CLI, `qmk doctor`, QMK Toolbox 0.3.3 or newer/beta if needed, `avrdude`, OS USB/serial device tools (`lsusb`, `dmesg`, Device Manager, System Information)

## Unknowns and Blockers

- Unknown physical controller and bootloader on the user's MiniDox. The upstream QMK target says `promicro`, but the physical board may have Pro Micro clone, Elite-C, nice!nano, RP2040, Teensy, or another swap.
- Unknown handedness method currently used by the keyboard. MiniDox readme says EE_HANDS or define strategy; the first flash should avoid assumptions until current behavior and target build choices are known.
- Unknown whether the current firmware exposes `QK_BOOT`, Command bootloader combo, Bootmagic, VIA, Vial, or a custom reset key. Hardware reset pads/buttons should be identified before flashing.
- I did not inspect the user's local repo, attached devices, USB descriptors, or installed OS packages. Another worker is responsible for local repo/device inspection.
- I did not run a build or flash, by instruction. No local source files were changed beyond this required scout output.
