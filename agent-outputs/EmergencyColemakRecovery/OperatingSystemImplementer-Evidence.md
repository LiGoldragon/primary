# Emergency Colemak Recovery — Operating System Implementer Evidence

## Task And Scope

Emergency recovery for an experimental laptop-only keyd/Colemak design that
landed on `main` too early and caused the live Niri profile on `ouranos` to use
QWERTY. Scope covered:

- `/git/github.com/LiGoldragon/CriomOS`
- `/git/github.com/LiGoldragon/CriomOS-home`
- live Home redeploy for `goldragon/ouranos/li`

Constraints honored:

- Did not reboot.
- Did not cancel or modify existing boot-once deployments on `ouranos` or
  `zeus`.
- Did not flash keyboard firmware.
- Did not deploy the experimental FullOs change live.
- Used direct `meta-lojix`/`lojix` interface for Home deploy and observation.

## Coordination And Context Consulted

- Read repo guidance: `CriomOS/AGENTS.md`, `CriomOS-home/AGENTS.md`,
  `/git/github.com/LiGoldragon/lore/AGENTS.md`, both repo
  `ARCHITECTURE.md` files, both repo `skills.md` files, and both
  `docs/ROADMAP.md` files.
- Orchestrate claim accepted for:
  - `/git/github.com/LiGoldragon/CriomOS`
  - `/git/github.com/LiGoldragon/CriomOS-home`
- `bd list --status open` was attempted in both repos, but both checkouts
  reported `.beads` present without a usable beads database.

## Branches And Commits

CriomOS-home:

- Preserved experiment bookmark:
  `test/laptop-colemak-keyd` at
  `a8b98fb09722e8529a7e04178805638384939abb`.
- Restored `main` at
  `e42ca632af4989f2cea3ea4117015c748ce1e7bf`
  (`CriomOS-home: restore compositor Colemak profile`).
- Pushed `main` and `test/laptop-colemak-keyd`.

CriomOS:

- Restored `main` at
  `2c5a31798ad19887800d7b48925135165628f261`
  (`CriomOS: restore global Colemak input policy`).
- Preserved experiment bookmark:
  `test/laptop-colemak-keyd` at
  `7ba01aea6b89dc0688c077953b2c2763f50d77eb`
  (`CriomOS: refresh laptop Colemak test home input`).
- The CriomOS experiment bookmark keeps the OS input-stack feature and pins
  `criomos-home` to the Home experiment bookmark revision
  `a8b98fb09722e8529a7e04178805638384939abb`.
- Pushed `main` and `test/laptop-colemak-keyd`.

## Source Changes

CriomOS-home `main`:

- Restored Niri XKB variant to `colemak`.
- Restored Hyprland fallback AT keyboard `kb_variant = colemak`.
- Restored Sway fallback AT keyboard `xkb_variant colemak`.
- Removed the experimental `keyboard-layout-policy` check that asserted
  compositor/fallback layouts must stay plain US.

CriomOS `main`:

- Restored `XKB_DEFAULT_VARIANT = "colemak"` when `useColemak` is true.
- Restored X11 `xkb.variant` to `optionalString useColemak "colemak"`.
- Restored keyd laptop config to the previous Alt/Meta swap only.
- Removed the experimental `laptop-keyboard-keyd` check.
- Updated `flake.lock` so `criomos-home` points at fixed Home revision
  `e42ca632af4989f2cea3ea4117015c748ce1e7bf`.

Both repos were clean after commits.

## Validation

Commands and results:

- `nix eval .#checks.x86_64-linux --apply builtins.attrNames`
  in `CriomOS-home`: succeeded and no longer listed
  `keyboard-layout-policy`.
- `nix eval .#homeConfigurations --apply builtins.attrNames`
  in `CriomOS-home`: succeeded with `[]` because the default horizon input has
  no users.
- Focused Niri module evaluation in `CriomOS-home`: returned
  `{ layout = "us"; variant = "colemak"; options = "ctrl:nocaps,altwin:swap_ralt_rwin"; }`.
- `nix build .#checks.x86_64-linux.listener-dictation-bindings --no-link --print-build-logs`
  in `CriomOS-home`: succeeded.
- Direct `CriomOS` flake check enumeration was blocked by expected stub inputs:
  default `system` and `horizon` inputs require Lojix projection.
- Focused `CriomOS` module evaluations succeeded:
  - `normalize.nix` with `useColemak = true` returned
    `XKB_DEFAULT_VARIANT = "colemak"`.
  - `edge/default.nix` keyd laptop config returned only:
    `[main]`, `leftalt = leftmeta`, and `leftmeta = leftalt`.
  - `metal/default.nix` with `useColemak = true` returned X11 variant
    `colemak`.
  - CriomOS input `criomos-home` resolved to
    `e42ca632af4989f2cea3ea4117015c748ce1e7bf`.

## Home Deploy

Pre-deploy observation:

- `lojix "(Query (ByNode (goldragon ouranos None)))"` showed existing
  `ouranos` generations, including a `FullOs BootOnce Current` generation.
  That boot-once entry was not changed.

Deploy command:

```sh
meta-lojix "(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home/e42ca632af4989f2cea3ea4117015c748ce1e7bf Activate None [])))"
```

Deploy admission result:

```text
(Deployed (35 (566 566)))
```

Post-admission observation:

- Initial Lojix queries did not yet show generation `35`; the daemon was still
  evaluating the Home activation package.
- `systemctl status lojix-daemon.service --no-pager` showed the system
  `lojix-daemon` running and processing the fixed Home revision.
- A later `lojix "(Query (ByNode (goldragon ouranos None)))"` showed
  generation `35` as `goldragon ouranos HomeOnly Switch Current`.

## Live Layout Verification

After generation `35` became current:

- Ran `niri msg action load-config-file`; command succeeded with no output.
- Ran `niri msg keyboard-layouts`; result:

```text
Keyboard layouts:
 * 0 English (Colemak)
```

- Inspected active Niri config symlink content via
  `rg -n "xkb|layout|variant|colemak|keyboard" ~/.config/niri/config.kdl`;
  observed:
  - `layout "us"`
  - `variant "colemak"`
  - `track-layout "global"`

`home-manager generations` was not available in PATH, but `~/.nix-profile`
resolved to a Nix profile path after activation.

## Remaining Next Steps

- The experimental laptop-only keyd design is preserved on
  `test/laptop-colemak-keyd` in both repos for later boot-once testing.
- Existing boot-once work on `ouranos` and `zeus` was left intact. Any later
  test of the preserved branch should be scheduled deliberately through the
  boot-once path, not by live `FullOs Switch`.
