# Laptop Colemak Keyd Merge And Live Switch Evidence

## Task And Scope

The user reported that the boot-once test generation on `zeus` proved the
laptop-only keyd Colemak design works, then explicitly approved merging the
tested work into `main` and live-switching the current host.

Scope:

- `/git/github.com/LiGoldragon/CriomOS-home`
- `/git/github.com/LiGoldragon/CriomOS`
- current host `ouranos`

Constraints honored:

- Did not reboot.
- Did not flash keyboard firmware.
- Did not switch `zeus`.
- Did not manually cancel or alter boot-once entries.
- Preserved unrelated `CriomOS-home` main work, including the newer Spirit
  input commit that was already on `main`.

## Coordination

The normal `CriomOS-home` checkout was claimed by another
`operating-system-implementer` for Spirit deployment work. I did not share that
checkout. I created and claimed an isolated JJ workspace at:

```text
/git/github.com/LiGoldragon/CriomOS-home-laptop-colemak-merge
```

Disposition for that workspace: discard when no longer needed. A beads item
could not be filed because both relevant checkouts reported `.beads` present
without a usable beads database.

The normal `/git/github.com/LiGoldragon/CriomOS` checkout was claimed and used
directly.

## Merged Main Commits

CriomOS-home:

- Main commit pushed:
  `329c93ec0fcf868481c0a5a4477a13112ba13fca`
- Commit message:
  `CriomOS-home: use keyd-owned laptop Colemak layout`
- Preserved previous main work by applying the tested Home layout policy on
  top of current `main`.

CriomOS:

- Main commit pushed:
  `d7f3e9d745f0b291de804834f3121ce8c2ffb3de`
- Commit message:
  `CriomOS: use laptop keyd for Colemak layout`
- `flake.lock` pins `criomos-home` to
  `329c93ec0fcf868481c0a5a4477a13112ba13fca`.

## Source Changes

CriomOS-home:

- Niri XKB config now uses plain `layout = "us"` with no Colemak variant.
- Hyprland and Sway fallback configs no longer apply a compositor-level
  Colemak variant for the laptop keyboard.
- Restored `checks.keyboard-layout-policy`, which asserts the compositor
  remains plain US and Colemak is not duplicated outside keyd.

CriomOS:

- Laptop keyd config targets only `0001:0001`.
- Laptop keyd config inlines keyd's shipped Colemak layout and sets
  `default_layout = colemak`.
- Laptop keyd config maps `leftalt = layer(meta)` and
  `leftmeta = layer(alt)`.
- Global XKB defaults and X11 XKB variant stay plain US when `useColemak` is
  true.
- Restored `checks.laptop-keyboard-keyd`.

## Validation

Pushed-source checks:

- `nix build github:LiGoldragon/CriomOS-home/329c93ec0fcf868481c0a5a4477a13112ba13fca#checks.x86_64-linux.keyboard-layout-policy --no-link --print-build-logs --refresh`
  succeeded.
- Direct fetched `CriomOS` check attr
  `github:LiGoldragon/CriomOS/d7f3e9d745f0b291de804834f3121ce8c2ffb3de#checks.x86_64-linux.laptop-keyboard-keyd`
  was blocked by the repo's default `system` stub before checks are exposed.
  This is the expected non-Lojix-projected flake behavior.
- The same pushed `CriomOS` check source was built directly through Nix by
  fetching the pushed tree and calling
  `checks/laptop-keyboard-keyd` with the pushed flake inputs; this succeeded.
- `nix flake metadata --json github:LiGoldragon/CriomOS/d7f3e9d745f0b291de804834f3121ce8c2ffb3de --refresh`
  showed the `criomos-home` lock revision as
  `329c93ec0fcf868481c0a5a4477a13112ba13fca`.

Working tree status:

- `CriomOS` working copy clean after push.
- isolated `CriomOS-home-laptop-colemak-merge` working copy clean after push.

## Live Switch

Confirmed current local host:

```text
ouranos
```

Pre-switch Lojix observation:

- `lojix "(Query (ByNode (goldragon ouranos None)))"` showed existing
  `ouranos` generations, including an existing `FullOs BootOnce Current`.
  I did not manually cancel or modify that entry.

Submitted command:

```sh
meta-lojix "(Deploy (System (goldragon ouranos FullOs /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS/d7f3e9d745f0b291de804834f3121ce8c2ffb3de Switch None [] None)))"
```

Admission result:

```text
(Deployed (38 (612 612)))
```

Terminal Lojix status:

- Lojix later rejected deploy `38`.
- Daemon log showed the failure occurred at the final activation/bootloader
  step after setting the system profile and running
  `switch-to-configuration switch`.
- The failing operation was the bootloader/default-entry cleanup path and
  ended with `NOPERMISSION`; Lojix reported the rejection reason as
  `BuilderUnreachable`.
- I did not manually retry bootloader mutation or clear boot-once state.

## Live State After Switch Attempt

Despite Lojix recording deploy `38` as rejected, live runtime state shows the
new system is active:

- `/run/current-system` and `/nix/var/nix/profiles/system` resolve to the same
  new system profile basename, and `profile_matches_current=yes`.
- `niri msg action load-config-file` succeeded.
- `niri msg keyboard-layouts` reports:

```text
Keyboard layouts:
 * 0 English (US)
```

- Active Niri config contains:
  - `layout "us"`
  - `variant ""`
  - `track-layout "global"`
- `/etc/keyd/laptop.conf` contains:
  - `[ids]` with only `0001:0001`
  - `[colemak:layout]`
  - `[global] default_layout = colemak`
  - `[main] leftalt = layer(meta)`
  - `[main] leftmeta = layer(alt)`
- `keyd.service` is active and was restarted at the switch time.
- `keyd.service` logs show it matched the AT Translated Set 2 keyboard against
  `/etc/keyd/laptop.conf`.

`keyd check /etc/keyd/laptop.conf` was attempted, but `keyd` is not available
on the user PATH. Service activation and keyd's own runtime match log are the
practical live checks available from the session.

## Residual Risk

The live switch completed enough to activate the new runtime behavior, but
Lojix did not record deploy `38` as a current generation because the final
bootloader step failed. Boot persistence/default-entry state should be checked
separately before relying on a future reboot to retain this exact generation.
