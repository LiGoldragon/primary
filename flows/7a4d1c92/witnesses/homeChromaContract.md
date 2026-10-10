# Home Chroma–Emacs contract at revision 002e521a

Method: probe `jj -R /git/github.com/LiGoldragon/CriomOS-home status`; `jj -R /git/github.com/LiGoldragon/CriomOS-home log -r 002e521a625cd8a8fa3c4fd7de2a533084e48634`; `jj file show -r 002e…` for the cited Home files; and `jj diff --from 1a6e22da155bb75a6362d10623301b13d0c24b34 --to 002e521a625cd8a8fa3c4fd7de2a533084e48634 --name-only`.

The audited Home parent is `002e521a625cd8a8fa3c4fd7de2a533084e48634`, titled `home: integrate resident Chroma Emacs projection`. Its Chroma and chroma-emacs input declarations are exact at `flake.nix:146` and `:151`; `flake.lock:418-460` records the same original and locked revisions:

- Chroma: `6a8e4c6a9bb0be0a76baa43b975df91edf6752f9`.
- chroma-emacs: `d432f95db5837e685e32afbf5790060fb15a3703`.

`modules/home/profiles/med/emacs.nix:14-20` constructs `emacsBase = pkgs.emacs-pgtk`, `emacsPackageSet = pkgs.emacsPackagesFor emacsBase`, the plugin package through `mkChromaTheme { inherit emacsPackageSet; }`, and the single `emacsWithPackages` runtime set. The same runtime set is assigned to both `programs.emacs.package` and `services.emacs.package` at `:792-802`. The `initElCompiled` derivation at `:684-716` byte-compiles and synchronously native-compiles with that exact package, while `earlyInitEl` prepends its `.eln` cache at `:718-740`.

The generated init at `modules/home/profiles/med/emacs.nix:316-317` reads Home's `modules/home/emacs/chroma-theme-init.el` and enables `(chroma-theme-mode 1)`. That Home-owned init adds `~/.config/emacs-ignis-themes` to `custom-theme-load-path` and maps `ignis-light`/`ignis-dark` to the plugin variables (`modules/home/emacs/chroma-theme-init.el:1-11`). Home's `modules/home/base.nix:25-110` generates those two symbols from Home's palettes, copies `ignis-light-theme.el` and `ignis-dark-theme.el`, installs them at `.config/emacs-ignis-themes` (`:145-156`), and disables Stylix's Emacs target (`:182-194`).

`modules/home/profiles/min/chroma.nix:107-137` now declares only `(Concerns Terminal Desktop Ghostty Pi)`, starts the pinned Chroma daemon at `:149-169`, and has no Emacs concern or Emacsclient adapter. The residual exact-commit Home scan finds only expected generic editor integration (`EDITOR`/`VISUAL`, the Emacsclient desktop entry, and test control calls), stale Darkman documentation/comments, and a negative `current-mode` assertion. It does not find a functional Darkman state reader or Chroma Emacs projection adapter. Therefore “complete removal” is true for the old projection concern, not literal removal of the generic Emacsclient editor utility.

The exact parent diff from `1a6e22…` includes the Chroma/Home integration files and lock changes but does not include `checks/yt-dlp/default.nix`. Jujutsu parent commits identify the requested Chroma and chroma-emacs revisions; later dirty states in the shared working copies were observed from outside implementation flows and were ignored by this audit.

No product repository, deployment state, or runtime state was changed by this witness.

## Sources

- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix:143-152, 508-509, 556-559`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.lock:418-460`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/emacs.nix:14-20, 316-317, 684-740, 792-855`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/emacs/chroma-theme-init.el:1-11`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/base.nix:25-110, 145-194`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/chroma.nix:107-169`
- `/git/github.com/LiGoldragon/CriomOS-home/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/chroma/` at `6a8e4c6a9bb0be0a76baa43b975df91edf6752f9`
- `/git/github.com/LiGoldragon/chroma-emacs/` at `d432f95db5837e685e32afbf5790060fb15a3703`
- Prior contract: `flows/01a02b4c/reports/chromaEmacsReacquisition.md`
- Prior Home reconnaissance: `flows/5ff8f889/reports/chromaEmacsHomeSlices.md`
