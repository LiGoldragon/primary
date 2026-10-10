# MiniDox Modernization Implementation Evidence

## Task And Scope

Modernized `/git/github.com/LiGoldragon/kibord` for a buildable MiniDox QMK source target without flashing, entering bootloader mode, or changing the operating system keyboard layout. Scope was limited to source, Nix build wiring, and concise build/pre-flash documentation.

## Files And Commands Consulted

- Read `/home/li/primary/AGENTS.md` from the supplied prompt.
- Read repo files: `flake.nix`, `flake.lock`, `ergodone/coleremak/keymap.c`, `ergodone/coleremak/config.h`, `ergodone/coleremak/rules.mk`.
- Read prior lane reports: `agent-outputs/MiniDoxStackRecon/Scout-SituationalMap.md` and `agent-outputs/MiniDoxModernTooling/Scout-SituationalMap.md`.
- Queried upstream QMK release/tag and MiniDox metadata enough to confirm QMK `0.33.8` and target `maple_computing/minidox/rev1`.
- Used Orchestrate claim: `(Claim (GeneralCodeImplementer [(Path /git/github.com/LiGoldragon/kibord)] ...))`.

## Changed Files

- `flake.nix`
  - Pins `qmk_firmware` to QMK `0.33.8`.
  - Adds a pinned `nixpkgs` input for ordinary flake package/check outputs.
  - Keeps the existing `SubWorld` output for compatibility.
  - Adds direct `packages.<system>.minidox` and `checks.<system>.minidox`.
  - Updates QMK Python/tool inputs for current QMK and includes the `qmk` CLI package required by QMK 0.33.8 make.
  - Points `LiGoldragon.minidox` at `maple_computing/minidox/rev1` with keymap source `maple_computing/minidox/LiGoldragon`.
- `flake.lock`
  - Updates QMK and QMK submodule inputs to the QMK 0.33.8-era revisions.
  - Adds `nixpkgs`.
  - Removes obsolete `uGFX`.
  - Restores unrelated `hexdumpSrc` to its prior locked revision.
- `maple_computing/minidox/LiGoldragon/keymap.c`
  - Adds a modern `LAYOUT_split_3x5_3` MiniDox keymap.
  - Base layer sends QWERTY-position letter keycodes so host `us(colemak)` produces Colemak without double-Colemak.
  - Adds lower/raise layers for symbols, navigation, numbers, function keys, and media keys.
  - Leaves adjust layer without a bootloader/reset key because flashing is out of scope.
- `maple_computing/minidox/LiGoldragon/config.h`
  - Sets `TAPPING_TERM 200`.
- `maple_computing/minidox/LiGoldragon/rules.mk`
  - Disables command and bootmagic for the baseline.
- `README.md`
  - Documents MiniDox build command.
  - Documents no-flash boundary, one-half-at-a-time warning, and TRRS powered hot-plug warning.

## Validation

All Nix build/check validation after the user directive was run with local builds disabled:

- `nix build .#minidox --print-build-logs --max-jobs 0 --builders @/etc/nix/machines --builders-use-substitutes`
  - Result: passed.
  - Built remotely on `ssh-ng://nix-ssh@prometheus.goldragon.criome`.
  - QMK output: `maple_computing_minidox_rev1_LiGoldragon.hex`.
  - QMK size check: `22336/28672` bytes used, `6336` bytes free.
  - Transient local artifact symlink: `result/maple_computing_minidox_rev1_LiGoldragon.hex`, size `62846` bytes. The `result` symlink was removed before commit.
- `nix flake check --print-build-logs --max-jobs 0 --builders @/etc/nix/machines --builders-use-substitutes`
  - Result: passed for current system evaluation.
  - Note: Nix warned `SubWorld` is an unknown flake output, preserving existing custom surface.
  - Note: Nix omitted incompatible system `aarch64-linux` in the default check invocation.

No `qmk flash`, `avrdude`, `dfu-programmer`, `dfu-util`, bootloader entry, HID mutation, or OS layout change was run.

## Commit And Push

- Commit: `5343bc14` (`kibord: modernize minidox qmk build`)
- Push: `main@origin` already matches `main` at `5343bc14`.

## Remaining Risks And Auditor Focus

- Flashing remains intentionally blocked until the physical MiniDox controller, bootloader, half behavior, reset method, and handedness strategy are identified.
- Auditor should inspect the physical-to-keycode mapping in `maple_computing/minidox/LiGoldragon/keymap.c` against the user's preferred Colemak ergonomics.
- Auditor should inspect the Nix closure choice: QMK is current and reproducible, but the flake still preserves legacy `SubWorld` and old kp-boot surfaces for compatibility.
- Auditor should confirm whether disabling bootmagic is desired for the first real flash; it is conservative for the no-flash baseline but affects future recovery shortcuts after flashing.
