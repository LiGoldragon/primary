# Current Home and Chroma contracts

Method: code read `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`.

Home has a commented, planned `criomos-emacs` input at lines 437–439 but no
Emacs flake input. Chroma is an active pinned input at lines 143–147. Inputs
from sibling components conventionally expose
`inputs.<name>.packages.${system}.default`; Home's Chroma module uses exactly
that shape.

Method: code read `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/emacs.nix`.

The medium profile builds `emacsWithPackages` from `pkgs.emacs-pgtk` and
`pkgs.emacsPackagesFor emacsBase` (lines 13–125), includes `base16-theme`, and
uses a generated `init.el`. The startup form at lines 310–323 adds
`~/.config/emacs-ignis-themes` to `custom-theme-load-path`, reads
`$XDG_STATE_HOME/darkman/current-mode`, and loads `ignis-dark` or
`ignis-light` once. This is the entire resident-projection gap: no
`chroma-theme` feature or global `chroma-theme-mode` is present.

The profile's `initElCompiled` derivation (lines 663–722) writes `init.el`,
byte-compiles it, then synchronously calls `native-compile` into a store
`eln-cache`. `early-init.el` prepends that cache to
`native-comp-eln-load-path`. `programs.emacs` and `services.emacs` both use the
same package, and the service starts with the graphical user session (lines
797–808). The profile also owns editor MIME entries and `EDITOR`/`VISUAL`; the
accepted change concerns theme projection only and should preserve those
surfaces.

Method: code read `/git/github.com/LiGoldragon/CriomOS-home/modules/home/base.nix`.

Home generates `ignis-dark-theme.el` and `ignis-light-theme.el` from the
Stylix dark/light palettes using `mkEmacsBase16Theme` (lines 21–110), then
installs them at `.config/emacs-ignis-themes` (line 156). The generated files
provide the symbols `ignis-dark` and `ignis-light`. Stylix explicitly disables
its Emacs target because Chroma owns native theme switching. The accepted
design keeps this generation in Home; the plugin must consume these symbols,
not regenerate palettes or own the files.

Method: code read `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/chroma.nix`.

Home's Chroma DOTOS config currently declares
`(Concerns Terminal Desktop Ghostty Emacs Pi)` and an `Emacsclient` adapter
path (lines 107–124). The Chroma user service runs the pinned daemon after the
graphical-session pre-target and requires `wl-gammarelay-rs` (lines 156–172).
Its activation seed updates `~/.config/chroma/config.dotos` (lines 174–189).
Slice 3 must remove the `Emacs` concern and `Emacsclient` adapter once the
Chroma D-Bus consumer contract is available; the resident plugin becomes the
sole Emacs projection.

Method: code read `/git/github.com/LiGoldragon/CriomOS-home/checks/chroma-dotos-config/default.nix`.

The existing Home check evaluates the Chroma module with deterministic colors
and inspects generated activation output. It currently requires the
`Emacsclient` path and the Emacs concern (lines 45–82), while also asserting
that the old `current-mode` sidecar is absent. The old positive assertions must
be replaced when Home drops direct Emacs projection. This check is an output
syntax check; a new end-to-end check must run the daemons and observe behavior,
not duplicate source-text greps.

## Sources

- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/emacs.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/base.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/chroma.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/chroma-dotos-config/default.nix`
- Flow `01a0238b`, `flows/01a0238b/reports/emacsAdapterDesign.md`
- Flow `5ff8f889`
