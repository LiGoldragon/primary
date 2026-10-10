# CriomOS Chroma–Emacs pin lock chain

Method: code read and immutable-origin probes in `/git/github.com/LiGoldragon/CriomOS`, `/git/github.com/LiGoldragon/CriomOS-home`, `/git/github.com/LiGoldragon/chroma`, and `/git/github.com/LiGoldragon/chroma-emacs` on 2026-08-23.

Observed: CriomOS `main@origin` is `93049a6e3eb7f66a23484402c96d835caa233b99`, titled `checks: align composed Home pin contract`. CriomOS-home `main@origin` is `a61b02d0cf69de757bdf8b5fa0f336f78f5054ee`, titled `home: prove resident Chroma projection closure`. Chroma `main@origin` is `6a8e4c6a9bb0be0a76baa43b975df91edf6752f9`, titled `Preserve durable theme state on startup`. chroma-emacs `main@origin` is `119a231358cf69c16161812caf69fff4b726be5c`, titled `Preserve overlay priority across theme switches`. `jj status` reported no changes in all four repositories.

Observed: CriomOS `flake.nix:35-50` declares `criomos-home` at the Home revision, and CriomOS `flake.lock:nodes.criomos-home.locked.rev` records `a61b02d0cf69de757bdf8b5fa0f336f78f5054ee`. The nested `criomos-home` lock node maps `chroma` and `chroma-emacs` to their named lock nodes.

Observed: CriomOS `flake.lock:494-539` records Chroma revision `6a8e4c6a9bb0be0a76baa43b975df91edf6752f9` and chroma-emacs revision `119a231358cf69c16161812caf69fff4b726be5c`, both following the Home nixpkgs node. CriomOS-home `flake.nix:143-152` declares the same revisions and CriomOS-home `flake.lock:418-460` records the same locked/original revisions. JSON extraction of both lock files returned the same four revision identities.

Observed: Home `modules/home/default.nix:32-91` imports both `profiles/min/chroma.nix` and `profiles/med/emacs.nix`. Home `modules/home/profiles/med/emacs.nix:14-20,109-111,792-803` builds the plugin through `mkChromaTheme` in the same `emacsWithPackages` set used by both `programs.emacs.package` and `services.emacs.package`. Home `modules/home/profiles/min/chroma.nix:19,149-169` installs the pinned Chroma package and starts `chroma-daemon` as a user service.

No product repository was edited by this witness.
