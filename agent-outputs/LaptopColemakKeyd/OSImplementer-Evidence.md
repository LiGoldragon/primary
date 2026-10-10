# OS Implementer Evidence

## Task And Scope

Move physical Colemak remapping to the laptop internal keyboard only, at the
lowest practical OS layer, while leaving firmware-level Colemak QMK keyboards
un-remapped. Do not flash or mutate keyboard firmware. Avoid live Home/Niri
activation. Use a boot-once deploy path only if the exact current command is
supported and clear.

Target host for deployment consideration: cluster `goldragon`, node `ouranos`,
deployment shape `System` / `FullOs` from pushed CriomOS revision
`ebedba399293f3b8ff9191ac9a8764ae988937ab`; builder choice would be `None`
unless an operator chooses otherwise. Rollback expectation for a boot-once test
would be the previous boot/default generation or an external keyboard if laptop
input is broken.

## Consulted Surfaces

- `/git/github.com/LiGoldragon/CriomOS/AGENTS.md`, `ARCHITECTURE.md`,
  `docs/ROADMAP.md`, `docs/GUIDELINES.md`, `docs/NIX_GUIDELINES.md`,
  `skills.md`.
- `/git/github.com/LiGoldragon/CriomOS-home/AGENTS.md`, `ARCHITECTURE.md`,
  `docs/ROADMAP.md`, `skills.md`.
- Shared lore agent contract and primary architecture.
- Read-only Spirit public query for existing intent context: one unrelated
  mechanism-vs-agent-judgment principle observed; no task-specific keyboard
  intent record found.
- Live read-only state: `keyd.service`, current `/etc/keyd/laptop.conf`, udev
  properties for `/dev/input/by-path/platform-i8042-serio-0-event-kbd`,
  `/proc/bus/input/devices`, and Lojix generation query for
  `goldragon ouranos`.
- Lojix source/docs search for boot-once command shape.

## Observed Facts

- `keyd.service` is active on `ouranos`.
- Current generated `/etc/keyd/laptop.conf` targeted only `0001:0001` and
  swapped left Alt/Meta.
- The laptop internal keyboard identity is `AT Translated Set 2 keyboard`,
  bus/vendor/product `0011/0001/0001`, stable path
  `/dev/input/by-path/platform-i8042-serio-0-event-kbd`, udev
  `ID_BUS=i8042`, `ID_INTEGRATION=internal`.
- keyd logs showed MiniDox devices being ignored by the current laptop-only
  keyd config.
- Global physical Colemak transforms existed in NixOS XKB/session defaults and
  active Niri/Home compositor config.
- The packaged `keyd check` does not resolve `include layouts/colemak` from a
  generic Nix runtime, so the final module inlines keyd's shipped
  `layouts/colemak` at Nix evaluation time and verifies the generated config.

## Changed Files

CriomOS commit: `ebedba399293f3b8ff9191ac9a8764ae988937ab`

- `modules/nixos/edge/default.nix`: laptop keyd config now targets `0001:0001`,
  inlines keyd's shipped Colemak layout, sets `default_layout = colemak`, and
  preserves the left Alt/Meta swap with `layer(meta)` / `layer(alt)`.
- `modules/nixos/normalize.nix`: `XKB_DEFAULT_LAYOUT` remains `us`; global
  `XKB_DEFAULT_VARIANT` is neutralized to empty instead of `colemak`.
- `modules/nixos/metal/default.nix`: X11 XKB variant is plain/empty instead of
  global Colemak; existing non-layout XKB options remain.
- `checks/laptop-keyboard-keyd/default.nix`: new focused check for laptop-only
  keyd ids, generated keyd config, global XKB neutralization, and X11 variant.
- `flake.nix`: exposes the new check.
- `flake.lock`: pins `criomos-home` to
  `594559c3ebb27df401fef30000d3099feeab6a05`.

CriomOS-home commit: `594559c3ebb27df401fef30000d3099feeab6a05`

- `modules/home/profiles/min/niri.nix`: active Niri keyboard layout stays `us`
  with no global Colemak variant; existing non-layout options remain.
- `modules/home/profiles/min/swayConf.nix`: fallback laptop Sway block no
  longer duplicates Colemak.
- `modules/home/profiles/min/hyprland.nix`: fallback laptop Hyprland block no
  longer duplicates Colemak.
- `checks/keyboard-layout-policy/default.nix`: new focused Home check for Niri
  plain-US layout and fallback compositor non-duplication.
- `flake.nix`: exposes the new check.

## Validation

Passed:

- `nix build .#checks.x86_64-linux.keyboard-layout-policy --no-link --print-build-logs`
  in CriomOS-home.
- `nix build --impure --expr '<direct CriomOS laptop-keyboard-keyd check expression>' --no-link --print-build-logs`
  in CriomOS, because the top-level check namespace needs projected `system`
  and `horizon` inputs.
- `keyd check` against generated laptop keyd config text from the local CriomOS
  checkout: no errors found.
- Targeted source search found no remaining physical Colemak transform in
  CriomOS; CriomOS-home matches only the new check's negative assertions.
- Pushed-revision check:
  `nix build --refresh --expr '<direct github:LiGoldragon/CriomOS/ebedba399293f3b8ff9191ac9a8764ae988937ab laptop-keyboard-keyd check expression>' --no-link --print-build-logs`.
- Pushed-revision check:
  `nix build --refresh github:LiGoldragon/CriomOS-home/594559c3ebb27df401fef30000d3099feeab6a05#checks.x86_64-linux.keyboard-layout-policy --no-link --print-build-logs`.
- `keyd check` against generated laptop keyd config text from pushed CriomOS
  revision `ebedba399293f3b8ff9191ac9a8764ae988937ab`: no errors found.

Not run:

- Full `nix flake check`, because the CriomOS top-level flake requires
  Lojix-projected `system` and `horizon` inputs; direct focused checks were used
  for the edited surfaces.
- Live Home Manager or Niri activation, intentionally avoided for input-stack
  safety.

## Deployment State

No boot-once deploy was performed.

Blocker: the loaded OS-operation doctrine for the current `meta-lojix` interface
documents the accepted `System` deploy shape with `Switch`, while explicitly
forbidding retired `Host` / `CompleteHost` / `UserEnvironment` request names.
Repository source and older CriomOS docs still mention `Host` plus
`ScheduleBootOnce`, but that conflicts with the current operation doctrine.
There is therefore no exact safe boot-once `meta-lojix` command available in
this task. Per the brief, deployment stopped rather than improvising a live
`Switch` or a retired request shape.

Current Lojix read-only evidence before stopping: `lojix "(Query (ByNode
(goldragon ouranos None)))"` returned existing `HomeOnly Switch` and `FullOs
Switch` current-generation records for `ouranos`.

## Next Reboot/Test Instructions

After the exact boot-once `System` command is clarified in current Lojix
doctrine, stage only a boot-once/test generation from:

```text
github:LiGoldragon/CriomOS/ebedba399293f3b8ff9191ac9a8764ae988937ab
```

Then reboot once into that generation. Do not live-switch the active graphical
session for this input-stack change.

Post-boot checks:

- `systemctl is-active keyd.service` reports active.
- `/etc/keyd/laptop.conf` contains `[ids]` with `0001:0001`,
  `[colemak:layout]`, `default_layout = colemak`, `leftalt = layer(meta)`, and
  `leftmeta = layer(alt)`.
- `keyd check /etc/keyd/laptop.conf` reports no errors.
- Laptop internal keyboard types Colemak.
- MiniDox/QMK keyboard letters are not double-remapped.
- `journalctl -u keyd.service` shows the laptop keyboard handled and MiniDox
  devices ignored by the laptop-only config.

Recovery path if input is broken after a future boot-once test: select the
previous/default generation from the bootloader or use a firmware-level QMK/USB
keyboard to log in and revert to the previous system generation. No boot-once
generation was staged by this worker.

## Primary Workspace Note

Before this worker wrote this file, primary already had unrelated pending
agent-output files:

- `agent-outputs/MiniDoxColemakCorrection/GeneralCodeImplementer-Evidence.md`
- `agent-outputs/OsInputStack/Scout-SituationalMap.md`

Primary doctrine requires whole-working-copy commits, so those files are
included if primary is committed after this evidence file.
