# Chroma Emacs slice one

## Result

Public repository [LiGoldragon/chroma-emacs](https://github.com/LiGoldragon/chroma-emacs)
is implemented and pushed at
`0b502607e7a20e08e33f675c6ac3e77696c755fa`.

It provides `chroma-theme`, global `chroma-theme-mode`, and the two supplied
theme customizations. The package uses the stipulated session D-Bus service,
object, interface, stable `emacs` consumer label, full revisioned snapshots,
and typed bounded failure reporting. This is an inspection implementation; it
does not claim the public wire is permanent.

## Interface and file map

- `lisp/chroma-theme.el` owns D-Bus transport, subscribe-before-register
  reconciliation, owner-change reconnection, revision handling, Chroma-only
  theme application and rollback, verification, and local diagnostics.
- `test/chroma-theme-test.el` is the fake-peer behavioral contract.
- `test/run-isolated-daemon.sh` runs that contract in a fresh Emacs daemon.
- `flake.nix` exposes the default package/checks and
  `lib.mkChromaTheme { emacsPackageSet = ...; }` for the exact caller-selected
  Emacs package set; detailed definitions remain in `nix/`.
- `README.md` documents supported use and the current protocol surface;
  `ARCHITECTURE.md` records ownership and invariants.

## Proof

The first ERT run failed because `chroma-theme` did not exist. After the
implementation, all six behavioral tests passed in batch and in an isolated
Emacs daemon: bidirectional projection, overlays, late startup, reconnect,
stale/duplicate revisions, load-failure preservation, and bounded typed
failure.

Flake evaluation passed with `nix flake show --all-systems`. The remote
default check initially failed because the pure Nix builder does not provide
`/usr/bin/env` for the shell-script shebang. `nix/checks.nix` now declares
`pkgs.bash` and invokes it directly. The corrected default check and default
package both passed with local building disabled (`max-jobs = 0`) on configured
remote builder `ssh-ng://nix-ssh@prometheus.goldragon.criome`.

## Limitations and next dependency

The fake peer exercises the transport seam and state behavior; it is not the
as-yet absent Chroma D-Bus service. Slice 2 must implement the corresponding
Chroma service, persisted revisions, sender binding, and consumer status
state. Only then can the CriomOS-home integration and real end-to-end daemon
witness begin. No Chroma, CriomOS-home, CriomOS, deployment, or live service
was changed here.

## Sources

- `flows/01a0238b/reports/emacsAdapterDesign.md`
- `flows/01a0238b/vision/emacsPlugin.md`
- `flows/01a02b4b/vision/emacsPlugin.md`
- `flows/01a02b4c/reports/chromaEmacsReacquisition.md`
- `flows/64515f36/reports/chromaProtocol.md`
- `flows/5ff8f889/reports/chromaEmacsHomeSlices.md`
- `/git/github.com/LiGoldragon/chroma-emacs`
- Flow `a1c42681` command witnesses
