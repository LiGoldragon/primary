# Boot-Once Colemak Deploy Evidence

## Task And Scope

Run only the accepted boot-once deployment for the validated laptop-only
Colemak/keyd CriomOS OS change. The target was cluster `goldragon`, node
`ouranos`, deployment shape `System FullOs`, action `BootOnce`.

Explicit non-actions: no `Switch`, no reboot, no flashing, no Home activation,
and no Niri reload.

## Inputs Confirmed

- CriomOS source revision: `ebedba399293f3b8ff9191ac9a8764ae988937ab`.
- CriomOS flake reference used:
  `github:LiGoldragon/CriomOS/ebedba399293f3b8ff9191ac9a8764ae988937ab`.
- CriomOS-home input pinned in that flake:
  `594559c3ebb27df401fef30000d3099feeab6a05`.
- `meta-lojix --version` and `meta-lojix --help` were rejected as NOTA request
  variants, consistent with the old direct-NOTA deployed CLI reported by the
  scout.

## Command Run

```sh
meta-lojix "(Deploy (System (goldragon ouranos FullOs /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS/ebedba399293f3b8ff9191ac9a8764ae988937ab BootOnce None [] None)))"
```

Result:

```text
(Deployed (33 (541 541)))
```

## Verification

Commands consulted:

- `nix flake metadata github:LiGoldragon/CriomOS/ebedba399293f3b8ff9191ac9a8764ae988937ab --json`
- `lojix "(Query (ByNode (goldragon ouranos None)))"`
- `bootctl list --no-pager`
- `bootctl status --no-pager`

Observed facts:

- Lojix recorded deployment generation `33 33` for `goldragon ouranos FullOs
  BootOnce Current`.
- The staged bootloader entry is `nixos-generation-135.conf`, built on
  2026-07-02 for NixOS Yarara 26.05.20260422.0726a0e with Linux 7.0.1.
- `bootctl status` reported current entry `nixos-generation-131.conf`, default
  entry `nixos-generation-131.conf`, and one-shot entry
  `nixos-generation-135.conf`.
- The live/running boot was not switched; generation 131 remained the selected
  current boot while generation 135 was staged for one-shot use.

Interpretation:

- The next boot is staged as a boot-once boot into generation 135.
- If that boot is not taken or fails to persist, the ordinary default remains
  generation 131.

## User Test And Recovery Instructions

When ready, manually reboot once. On the next boot, test keyboard input before
doing any further deployment work. Verify normal typing, login, terminal input,
Colemak behavior, and any expected keyd-specific remaps.

If input is broken enough to block normal use, power-cycle or reboot again; the
one-shot target should be consumed and the system should fall back to the
ordinary default generation 131. If the boot menu appears, choose generation 131
manually.

Do not run a permanent `Switch` for this revision until typing has been tested
successfully after the one-shot boot.
