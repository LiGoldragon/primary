# Chroma and unfinished Emacs repository state

Method: code read `/git/github.com/LiGoldragon/chroma/src/theme.rs`,
`/git/github.com/LiGoldragon/chroma/src/config.rs`,
`/git/github.com/LiGoldragon/chroma/src/daemon.rs`,
`/git/github.com/LiGoldragon/chroma/flake.nix`, and
`/git/github.com/LiGoldragon/chroma/ARCHITECTURE.md`.

Chroma `main` currently implements a framed Unix-socket CLI and Kameo theme
concern actors. `ThemeConcern::Emacs`, `ThemeAdapters.emacsclient`, the
`Emacsclient` DOTOS parser, and `EmacsThemeConcern` are all present. The
concern constructs a one-shot `emacsclient --eval` form, drops stdout/stderr,
does not require a successful child exit status, and has no postcondition or
consumer acknowledgement. Chroma's daemon starts from config, persists visual
state, and serves only its framed Unix socket; the current daemon has no
public desired-theme D-Bus service, revision, registration, or consumer-status
surface.

The Chroma flake exports only `packages.default`, the terminal sandbox package,
Cargo tests, and the sandbox check. Its sandbox is useful infrastructure for a
future Home witness: it creates isolated HOME/XDG config/state/runtime paths,
starts a private D-Bus session, launches fake gamma and Ghostty D-Bus peers,
starts the real `chroma-daemon`, waits for its socket and ready files with
`inotifywait`, and drives real `SetTheme` requests. It currently omits Emacs
and uses `(Concerns Terminal Ghostty)`, so it is not yet the accepted
Chroma–Emacs witness.

Method: code read `/git/github.com/LiGoldragon/CriomOS-emacs/README.md`,
`/git/github.com/LiGoldragon/CriomOS-emacs/docs/ROADMAP.md`,
`/git/github.com/LiGoldragon/CriomOS-emacs/flake.nix`,
`/git/github.com/LiGoldragon/CriomOS-emacs/modules/home/default.nix`, and
`/git/github.com/LiGoldragon/CriomOS-emacs/packages/mkEmacs/default.nix`.

`CriomOS-emacs` is explicitly a whole-distribution scaffold. Its package
conversion bead and Home wiring remain unfinished; its home module is empty.
It contains a verbatim legacy mkEmacs function and the same startup-only
Darkman read, but it is not the accepted focused `chroma-emacs` repository and
must not be made a compatibility path for this design.

## Sources

- `/git/github.com/LiGoldragon/chroma/src/theme.rs`
- `/git/github.com/LiGoldragon/chroma/src/config.rs`
- `/git/github.com/LiGoldragon/chroma/src/daemon.rs`
- `/git/github.com/LiGoldragon/chroma/flake.nix`
- `/git/github.com/LiGoldragon/chroma/scripts/chroma-sandbox-terminal`
- `/git/github.com/LiGoldragon/chroma/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/CriomOS-emacs/README.md`
- `/git/github.com/LiGoldragon/CriomOS-emacs/docs/ROADMAP.md`
- `/git/github.com/LiGoldragon/CriomOS-emacs/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS-emacs/modules/home/default.nix`
- Flow `01a0238b`, `flows/01a0238b/witnesses/sourceBoundaries.md`
- Flow `5ff8f889`
