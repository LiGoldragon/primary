# OS Input Stack Situational Map

## Task And Scope

Scout task: inspect local CriomOS/Nix input configuration for the durable goal that MiniDox remains firmware-level Colemak, the laptop internal keyboard gets Colemak at the lowest practical OS layer, and the OS must not double-remap MiniDox. Also map future fit for laptop-keyboard layers/chords similar to QMK.

No source files, OS settings, keyboard layouts, service state, firmware, or commits were changed. The only write was this required scout output under `agent-outputs/OsInputStack/`.

## Files And Commands Consulted

Local guidance:

- `/home/li/primary/AGENTS.md` from the dispatch context.
- `/home/li/primary/ARCHITECTURE.md`.
- `/home/li/primary/orchestrate/AGENTS.md` and `/home/li/primary/orchestrate/ARCHITECTURE.md`.
- `/git/github.com/LiGoldragon/lore/AGENTS.md`.
- `/git/github.com/LiGoldragon/CriomOS/AGENTS.md`.
- `/git/github.com/LiGoldragon/CriomOS/ARCHITECTURE.md`.
- `/git/github.com/LiGoldragon/CriomOS-home/AGENTS.md`.
- `/git/github.com/LiGoldragon/CriomOS-home/ARCHITECTURE.md`.
- `/home/li/primary/.agents/skills/operating-system-operations/SKILL.md`.

Local source/config:

- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/edge/default.nix`.
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/metal/default.nix`.
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/normalize.nix`.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/niri.nix`.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/swayConf.nix`.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/hyprland.nix`.
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/node.rs`.
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/user.rs`.
- `/git/github.com/LiGoldragon/horizon-rs/docs/DESIGN.md`.
- `/git/github.com/LiGoldragon/goldragon/datom.nota`.

Live read-only commands:

- `jj status`.
- `bd list --status open` in `CriomOS` and `CriomOS-home`.
- `systemctl is-active keyd.service`, `systemctl status keyd.service --no-pager --lines=0`, `systemctl cat keyd.service`.
- `localectl status`.
- `env | sort | rg '^XKB_DEFAULT|^XDG_SESSION|^WAYLAND|^DISPLAY|^NIRI'`.
- `niri msg keyboard-layouts`, `niri msg -j keyboard-layouts`, `niri --version`.
- `lsusb`.
- `sed -n '1,260p' /proc/bus/input/devices`.
- `/sys/class/input/event*/device/{name,phys,uniq,modalias}` reads.
- `udevadm info --query=property --path=/sys/class/input/event0`.
- `udevadm info --query=property --path=/sys/class/input/event20`.
- USB sysfs reads under `/sys/bus/usb/devices`.
- HID sysfs reads under `/sys/bus/hid/devices` and `/sys/class/hidraw`.
- `/etc/keyd/laptop.conf`, `/etc/static/X11/xorg.conf.d/00-keyboard.conf`, `/etc/static/vconsole.conf`, `/home/li/.config/niri/config.kdl`.
- Keyd local docs from the active daemon package: `share/doc/keyd/README.md`, `share/man/man1/keyd.1.gz`, and `share/keyd/layouts/colemak`.

Primary/current web sources used only where local docs were insufficient:

- Niri upstream wiki, Configuration: Input, edited May 1, 2026: `https://github.com/niri-wm/niri/wiki/Configuration%3A-Input`.
- Keyd upstream GitHub README: `https://github.com/rvaiya/keyd`.
- Arch keyd manpage mirror for readable line references: `https://man.archlinux.org/man/extra/keyd/keyd.1.en`.
- MyNixOS option page for `services.keyd.keyboards`: `https://mynixos.com/nixpkgs/option/services.keyd.keyboards`.

## Observed Facts

### Ownership And Safety

- CriomOS is the NixOS host OS surface. `CriomOS/AGENTS.md:7` says it is a NixOS-based host OS, and `CriomOS/AGENTS.md:17` says home lives in `CriomOS-home`.
- CriomOS-home owns Home Manager/Niri desktop configuration. `CriomOS-home/AGENTS.md:9-15` lists Niri compositor config as home-owned.
- NixOS-level device/service concerns belong in CriomOS. `CriomOS-home/skills.md:43-46` explicitly says CriomOS-home does not own NixOS users, groups, udev, kernel modules, or `/dev/uinput`.
- Input/compositor live activation is risky. `CriomOS-home/AGENTS.md:26-28` says live-activating Home Manager generations with compositor/input changes risks losing the session and should use a safe rebuild plus new login.
- CriomOS process guidance says `niri` stays unsignalled (`CriomOS/AGENTS.md:28-29`).

### Existing Declarative Colemak Sources

- Cluster data marks `ouranos` as a ThinkPad T14 Gen 5 Intel node with Colemak input: `goldragon/datom.nota:28-33`.
- The user `li` is also declared with Colemak keyboard preference: `goldragon/datom.nota:196-199`.
- Horizon derives `horizon.node.use_colemak` from `proposal_io.keyboard == Colemak` in `horizon-rs/lib/src/node.rs:510-581`.
- Horizon derives `horizon.user.use_colemak` from `user.keyboard == Colemak` in `horizon-rs/lib/src/user.rs:131-137`.
- The design doc records `use_colemak` as a broad node/user computed field, not a physical-device split: `horizon-rs/docs/DESIGN.md:378-381` and `horizon-rs/docs/DESIGN.md:424-442`.

### Current Local Runtime State

- Host is `ouranos`, kernel `Linux ouranos 7.0.1 ... x86_64 GNU/Linux`; DMI says `LENOVO ThinkPad T14 Gen 5`, product `21MLS18Y00`.
- `keyd.service` is active and running. `systemctl status` showed main PID `1279` and binary `keyd-2.6.0`; `niri --version` showed `niri 25.11 (Nixpkgs)`.
- Generated keyd config exists at `/etc/keyd/laptop.conf`, symlinked through `/etc/static/keyd/laptop.conf` to a Nix store file. Its full content is:

```ini
[ids]
0001:0001

[main]
leftalt = leftmeta
leftmeta = leftalt
```

- The matching declarative source is `CriomOS/modules/nixos/edge/default.nix:123-132`: `services.keyd.enable = size.min`, `keyboards.laptop.ids = [ "0001:0001" ]`, and only left Alt/Meta are swapped.
- The active keyd service is system-level, reads `/dev/input`, writes `/dev/uinput`, and has supplementary `input` and `uinput` groups in `systemctl cat keyd.service`.

### Current Global XKB/Colemak State

- Niri Home Manager config applies XKB Colemak to every Niri keyboard:
  - Source: `CriomOS-home/modules/home/profiles/min/niri.nix:199-205` sets `input.keyboard.xkb.layout = "us"`, `variant = "colemak"`, and options.
  - Generated live config: `/home/li/.config/niri/config.kdl:1-12` has `input.keyboard.xkb.layout "us"`, `variant "colemak"`, and `track-layout "global"`.
  - Live compositor view: `niri msg keyboard-layouts` returned only `English (Colemak)`.
- System-level X11 XKB is global:
  - Source: `CriomOS/modules/nixos/metal/default.nix:550-552` sets `services.xserver.xkb.variant = optionalString useColemak "colemak"` and global XKB options.
  - Generated file: `/etc/static/X11/xorg.conf.d/00-keyboard.conf:1-8` is a `Keyboard catchall` with `MatchIsKeyboard "on"`, `XkbLayout "us"`, and `XkbVariant "colemak"`.
  - `localectl status` reported `X11 Layout: us`, `X11 Variant: colemak`, and `X11 Options: caps:ctrl_modifier, altwin:swap_alt_win`.
- Environment defaults are global:
  - Source: `CriomOS/modules/nixos/normalize.nix:150-155` sets `XKB_DEFAULT_LAYOUT=us` and `XKB_DEFAULT_VARIANT=colemak` when `useColemak`.
  - Live environment contained `XKB_DEFAULT_LAYOUT=us` and `XKB_DEFAULT_VARIANT=colemak`.
- Console keymap is set:
  - `/etc/static/vconsole.conf:1` has `KEYMAP=/nix/store/...-xkb-console-keymap`.
  - `localectl status` reported `VC Keymap: (unset)`, but the static config points at a generated xkb console keymap. I did not decode that keymap file.

### Historical/Inactive Per-Device Attempts

- Sway config has a model-specific laptop rule:
  - `CriomOS-home/modules/home/profiles/min/swayConf.nix:41-48` applies `xkb_variant colemak` only to input `"1:1:AT_Translated_Set_2_keyboard"` when `useColemak`.
  - It explicitly resets ErgoDone devices to basic US at `swayConf.nix:51-58`.
- Hyprland config has a laptop device rule:
  - `CriomOS-home/modules/home/profiles/min/hyprland.nix:49-55` targets `name = at-translated-set-2-keyboard` and applies `kb_variant = colemak`.
- These are not the current Niri path; they are useful precedent that the laptop-only intent existed in older compositor configs.

### Laptop Internal Keyboard Identity

Strong current identity:

- Kernel input device from `/proc/bus/input/devices`:
  - `Name="AT Translated Set 2 keyboard"`.
  - `Bus=0011 Vendor=0001 Product=0001 Version=ab83`.
  - `Phys=isa0060/serio0/input0`.
  - `Handlers=sysrq kbd leds event0`.
  - `Sysfs=/devices/platform/i8042/serio0/input/input0`.
- Stable symlink:
  - `/dev/input/by-path/platform-i8042-serio-0-event-kbd -> ../event0`.
- Udev properties for `/sys/class/input/event0`:
  - `ID_INPUT_KEYBOARD=1`.
  - `ID_BUS=i8042`.
  - `ID_PATH=platform-i8042-serio-0`.
  - `ID_INTEGRATION=internal`.
  - `LIBINPUT_DEVICE_GROUP=11/1/1:isa0060/serio0`.

This matches the existing keyd selector `0001:0001`.

### MiniDox / External Keyboard Identity

- No obvious MiniDox/QMK USB keyboard was present in the current read-only inventory.
- `lsusb` showed only root hubs, integrated camera, Intel Bluetooth, Synaptics, DJI Wireless Microphone RX, and an Actions `MSC-Sample` mass-storage device.
- `/proc/bus/input/devices` showed no USB HID keyboard other than `keyd virtual keyboard` and a Bluetooth AVRCP media-control input.
- USB interface scan showed:
  - `10d6:b00b MSC-Sample` is USB mass storage (`class=08 subclass=06 protocol=50`, `usb-storage`).
  - `2ca3:b00d Wireless Microphone RX` is audio.
  - No USB interface with HID boot keyboard class/protocol was visible.
- HID bus inventory had only the internal Synaptics I2C touchpad HID.

Conclusion: MiniDox identity was not available in normal keyboard mode during this scout. It may be unplugged, powered differently, on a different machine, or not enumerating as a keyboard at the time of inspection.

## Primary Source Findings

- Niri upstream currently applies input settings by device type, not by individual keyboard. The Niri wiki says keyboard/touchpad/mouse/etc. settings apply to every device of that type and that specific-device configuration is not currently available, though planned. It also says Niri XKB settings are passed to libxkbcommon, and if XKB is empty Niri fetches settings from `systemd-localed`/`localectl`.
- Keyd upstream/local docs fit the desired low layer:
  - Keyd remaps using kernel-level input primitives `evdev` and `uinput` (`share/doc/keyd/README.md:7-12`; upstream README same content).
  - Keyd advertises layers, key overloading, keyboard-specific configuration, system-wide config that works in VTs, and multiple keyboards with different layouts (`share/doc/keyd/README.md:28-43`, `README.md:45-55`).
  - The manpage says configs in `/etc/keyd/*.conf` begin with `[ids]`; explicit IDs match only those devices, wildcard with exclusions is also possible, and a device ID may only appear in one config file.
  - Keyd layouts exist; the manpage shows `include layouts/colemak` and `[global] default_layout = ...` / `setlayout(...)`. The local active package includes `/share/keyd/layouts/colemak`, whose mapping includes `s = r`, `d = s`, `f = t`, etc., matching QWERTY-position to Colemak-letter conversion.
  - Keyd supports chords (`j+k = esc` example), oneshot modifiers, overload/tap-hold, homerow-mod helper patterns, macros, and composite layers.
- NixOS has a declarative `services.keyd.keyboards` option that creates corresponding `/etc/keyd/` files, with per-keyboard `ids` and `settings`/`extraConfig`; MyNixOS documents this shape and the local CriomOS code already uses it.

## Interpretations

- Current state double-remaps a firmware-level Colemak MiniDox under Niri/X11 because Colemak is global at compositor/XKB/localed environment layers.
- Niri cannot currently solve laptop-only Colemak directly because its keyboard XKB section is all-keyboards, not per physical keyboard.
- The current keyd setup is already the right system layer to extend: it is active, declaratively managed by CriomOS, targets the laptop `0001:0001` device, and sits below Niri/X11/TTY while leaving non-matching keyboards untouched.
- Kernel `udev`/`hwdb` would be a lower layer than keyd, but it is not the practical layer for this goal because the long-term request includes QMK-like layers/chords and because a full Colemak letter layout plus tap/hold behavior is more naturally represented in keyd than static scancode remaps.
- Horizon's broad `useColemak` boolean currently means "this node/user wants Colemak" and drives broad XKB settings. It does not encode "laptop internal keyboard gets OS Colemak; QMK keyboards remain raw." An implementation should either reinterpret that boolean in CriomOS for edge laptops or add a more precise input-device policy shape later.

## Ranked Options

1. **Best fit: move laptop Colemak into existing system keyd config and make compositor/XKB defaults plain US.**
   - Scope: CriomOS system module plus Niri/Home global XKB cleanup.
   - Mechanism: keep `services.keyd.keyboards.laptop.ids = [ "0001:0001" ]` or `k:0001:0001`; include keyd's Colemak layout and set the laptop keyd default layout to `colemak`; preserve existing Alt/Meta swap in that same laptop config.
   - Then remove/neutralize global `us(colemak)` from Niri (`niri.nix`), X11 catchall (`metal/default.nix`), and `XKB_DEFAULT_VARIANT` (`normalize.nix`) so the display server sees ordinary US keycodes from both keyd's laptop virtual keyboard and MiniDox firmware.
   - Fit: lowest practical layer, per-device, already installed, future layers/chords native, avoids MiniDox double-remap.
   - Risk: a bad keyd config can impair typing; validate with `keyd check` and deploy via safe reboot/new-login path. Keep panic sequence in mind: `backspace+escape+enter` terminates keyd per docs.

2. **Near-term fallback: per-compositor device rules where supported.**
   - Sway/Hyprland examples already exist locally and can target the laptop internal keyboard by name/ID.
   - Fit: can be per-device in those compositors.
   - Risk: not current Niri, not VT/Xwayland-localed consistent, no QMK-like layers/chords, and Niri upstream says per-device config is not currently available.

3. **Kernel hwdb/udev scancode remapping.**
   - Fit: very low layer and can target hardware.
   - Risk: too static for Colemak-plus-layers/chords, harder to reason about/deploy safely, not aligned with existing CriomOS keyd service, and future QMK-like behavior would need another tool anyway.

4. **Add kanata/kmonad.**
   - Fit: capable tools for complex layouts/layers.
   - Risk: not currently configured in the repo or running system; duplicates an already-enabled keyd stack. Only worth revisiting if keyd cannot express a required long-term behavior.

5. **Status quo: global XKB Colemak.**
   - Fit: works only when every keyboard expects OS-level Colemak.
   - Risk: explicitly conflicts with firmware-level Colemak MiniDox by double-remapping it.

## Recommended Implementation Plan

1. In `CriomOS/modules/nixos/edge/default.nix`, extend the existing `services.keyd.keyboards.laptop` config rather than adding a new input daemon. Keep the exact laptop selector and Alt/Meta swap. Use keyd's shipped `layouts/colemak` and default layout support. A conceptual config shape is:

```ini
[ids]
k:0001:0001

include layouts/colemak

[global]
default_layout = colemak

[main]
leftalt = leftmeta
leftmeta = leftalt
```

2. Validate the exact generated keyd config before deploy with the active keyd binary's `check` command or a Nix check. Do not rely on a live unvalidated keyd reload.

3. Remove global Colemak from all active OS/display layers:
   - `CriomOS-home/modules/home/profiles/min/niri.nix:199-205`: set Niri keyboard XKB to plain `layout = "us"` with no `variant = "colemak"`; keep desired non-layout options only if they do not conflict with keyd.
   - `CriomOS/modules/nixos/metal/default.nix:550-552`: stop setting global `services.xserver.xkb.variant = "colemak"`.
   - `CriomOS/modules/nixos/normalize.nix:151-155`: stop exporting global `XKB_DEFAULT_VARIANT=colemak`; leave `XKB_DEFAULT_LAYOUT=us` only if needed.
   - Check console behavior. If keyd is the laptop remapper in VTs after service start, the static xkb console keymap should not also encode Colemak.

4. Preserve existing app-level Colemak adaptations that are not physical key remaps only after reviewing them separately:
   - Shell/tmux/ranger/qutebrowser/Emacs references to `useColemak` may be shortcut/keybinding ergonomics rather than layout transforms. They should not be mechanically deleted with XKB layout changes.

5. Deploy as a system/home coordinated change through the current Lojix path, not a live manual Home Manager activation. Because this touches compositor/input, prefer build/new-login or reboot validation per `CriomOS-home/AGENTS.md:28`.

6. After activation, verify:
   - `localectl status` shows X11 layout `us` and no Colemak variant.
   - `niri msg keyboard-layouts` shows plain English/US, not English Colemak.
   - `/etc/keyd/laptop.conf` contains the laptop-only keyd Colemak config.
   - Internal laptop keyboard types Colemak in Niri and in a VT after keyd starts.
   - MiniDox types Colemak without double-remap in Niri and is not matched by any keyd config.

7. Future layers/chords should be added to the laptop keyd config or included common keyd snippets, still targeted to the laptop ID only. Use keyd layers/chords/overload rather than Niri binds for behavior that should follow the laptop keyboard across Wayland/X/TTY.

## User Physical Verification Needed

- Plug MiniDox in normal keyboard mode, not bootloader, before final implementation verification.
- Capture MiniDox normal identity with read-only commands:
  - `lsusb`.
  - `sed -n '1,260p' /proc/bus/input/devices`.
  - `ls -l /dev/input/by-id /dev/input/by-path`.
  - `udevadm info --query=property --path=/sys/class/input/eventN` for the MiniDox event node.
- Confirm MiniDox firmware is actually emitting Colemak keycodes under a plain US OS layout. This requires typing a small known sequence after global XKB is plain US.
- Confirm whether the user wants laptop internal keyboard only, or also other non-QMK external commodity keyboards, to receive OS-level Colemak. Current goal says laptop keyboard; the safest plan targets only `AT Translated Set 2 keyboard`.
- Keep a recovery input path available for the first keyd-Colemak boot: MiniDox, on-screen keyboard, SSH/root console, or a rescue TTY. Keyd docs warn bad config can make input unusable.

## Unknowns And Blockers

- MiniDox identity was not observable during this scout; no concrete vendor/product/name can be recorded yet.
- I did not run `keyd monitor` because it observes live key events and can be invasive; it is useful later for physical verification if the user is present.
- I did not evaluate or build the exact Nix closure; this was a read-only scout.
- I did not decode the generated console keymap file referenced by `/etc/static/vconsole.conf`.
- I did not inspect private scopes.
- `bd list --status open` in both CriomOS and CriomOS-home returned "no beads database found" plus a permissions warning; no bead context was available locally.
- A broad read-only `/nix/store` maxdepth listing was accidentally run once while locating package docs, contrary to the workspace's no `/nix/store` filesystem search rule. No mutation resulted; subsequent store reads were limited to already identified active package/config paths.

## Verification Summary

- Working copy before report: `jj status` reported no changes.
- Spirit query: `PublicTextSearch [keyboard layout input stack CriomOS MiniDox Colemak]` found no keyboard-specific durable intent record; the controlling intent for this task is the user clarification in the dispatch.
- Orchestrate observation showed no blocking claim for this read-only scout.
- System was not mutated: no service reload/restart, no Niri reload, no layout command, no firmware/bootloader operation, no commit.
