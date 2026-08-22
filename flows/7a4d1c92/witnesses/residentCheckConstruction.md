# Exact Home resident-check construction

Method: evaluate the check from the exact Home revision without using the dirty working copy:

```text
nix eval --impure --show-trace --raw --expr '
let
  homeFlake = builtins.getFlake "git+file:///git/github.com/LiGoldragon/CriomOS-home?rev=002e521a625cd8a8fa3c4fd7de2a533084e48634";
  system = "x86_64-linux";
  pkgs = homeFlake.inputs.nixpkgs.legacyPackages.${system};
  check = import "${homeFlake.outPath}/checks/chroma-emacs-resident" {
    inherit pkgs;
    inputs = { chroma = homeFlake.inputs.chroma; chroma-emacs = homeFlake.inputs.chroma-emacs; };
  };
in check.drvPath
'
```

The command exited 0 and returned a `chroma-emacs-resident-check` derivation. `nix derivation show` confirms its build command is `chroma-emacs-resident-witness; touch "$out"`, with `CHROMA_EMACS_DBUS_SESSION_CONF` and the Home init file as environment inputs. The nested witness derivation's generated `PATH` contains:

- `emacs-pgtk-with-packages-30.2/bin`;
- the built `chroma-0.2.5/bin`;
- dbus, GLib, coreutils, grep, inotify-tools, and the fake Gamma wrapper.

This proves exact-revision derivation construction and binary wiring, not a completed build or executed witness. No Nix build was run by this audit.

Method: code read exact revision `checks/chroma-emacs-resident/default.nix` and `run.sh` via `jj file show -r 002e…`.

The check creates a private bus by recursively entering `dbus-run-session --config-file=...` (`run.sh:3-6`), isolates HOME/XDG directories (`:16-22`), starts fake Gamma and the real `chroma-daemon` (`:71-86`), and starts a real packaged PGTK Emacs daemon with the Home init and global mode (`:88-99`). It queries real D-Bus `GetProjectionStatus emacs` and requires `Applied` revisions 0, 1, and 2 (`:101-113`, `:133-165`). It queries Emacs's enabled themes and default/mode-line backgrounds, preserving an unrelated overlay across Dark, Chroma restart, and Light (`:115-131`, `:139-157`), then starts a fresh Emacs daemon and reconciles the latest Light revision (`:159-165`).

The waits are event/barrier-based: inotify watches and bounded `read -t 20` waits; there are no `sleep` commands. The `grep` calls inspect runtime D-Bus/Emacs output, not source text.

Proof boundaries remain:

1. `run.sh:37-55` writes simplified `ignis-light`, `ignis-dark`, and overlay theme source files into the test HOME. The check therefore does not consume the generated Home `base.nix` Ignis artifacts or prove Home activation/install of those files.
2. `run.sh:97` uses `emacs --quick` and manually loads the test init. It does not run Home's generated early-init/native-compiled `.eln` path.
3. The Home script checks only `Applied` statuses. `Pending`, `Unavailable`, and `Failed` remain owned by Chroma/chroma-emacs protocol tests.
4. The script does not explicitly assert that the opposite Chroma theme is disabled; plugin postcondition tests and implementation enforce that behavior.
5. No exact Chroma or chroma-emacs revision string is queried at runtime; lock/source derivation wiring supplies that identity.

No build, test execution, product edit, deployment, or runtime-state mutation was performed by this witness.

## Sources

- `/git/github.com/LiGoldragon/CriomOS-home/checks/chroma-emacs-resident/default.nix:1-42` at Home revision `002e521a625cd8a8fa3c4fd7de2a533084e48634`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/chroma-emacs-resident/run.sh:1-165` at the same revision
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/emacs.nix:684-740`
- `/git/github.com/LiGoldragon/chroma/src/theme_dbus.rs`
- `/git/github.com/LiGoldragon/chroma/src/daemon.rs`
- `/git/github.com/LiGoldragon/chroma-emacs/lisp/chroma-theme.el`
- `/git/github.com/LiGoldragon/chroma-emacs/test/run-isolated-dbus-daemon.sh`
