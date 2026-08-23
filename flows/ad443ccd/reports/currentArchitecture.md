# Current Chroma–Emacs architecture

## Observed code

The implementation is now a three-repository chain:

```text
CriomOS / CriomOS-home pins
  ├─ Chroma daemon (semantic state, revision, D-Bus status)
  ├─ chroma-emacs (resident projection)
  └─ Home-generated Ignis themes + Emacs setup
```

Current clean revisions are Chroma `6a8e4c6a`, chroma-emacs `119a2313`, and CriomOS-home `a61b02d0`; CriomOS pins Home `a61b02d0` (`/git/github.com/LiGoldragon/CriomOS/flake.nix:35-49`). Home pins Chroma and chroma-emacs at those same revisions (`/git/github.com/LiGoldragon/CriomOS-home/flake.nix:143-152`).

Chroma starts the root actor, session-bus service, config watcher, sleep watcher, schedule engine, and framed UDS server (`chroma/src/daemon.rs:59-104`). The root owns desired mode/revision and the in-memory projection registry (`chroma/src/daemon.rs:123-136`). State persistence is delegated to a dedicated redb actor at `$XDG_STATE_HOME/chroma/state.redb`; the current `theme/current` archive is `(ThemeMode, revision)`, and old theme-only archives migrate at revision zero (`chroma/src/state.rs:21-65`, `207-313`).

The public wire is fixed in code: session bus `io.github.LiGoldragon.Chroma`, object `/io/github/LiGoldragon/Chroma/Theme`, interface `io.github.LiGoldragon.Chroma.Theme1`; registration returns `(state, revision)`, desired-state signals carry `(state, revision)`, reports have five fixed arguments, and status returns `(status, revision)` (`chroma/src/theme_dbus.rs:20-31`, `293-345`). The service binds calls to the D-Bus unique sender (`chroma/src/theme_dbus.rs:281-331`). `ThemeProjection` owns the one-owner-per-`emacs` registry, `Pending`/`Applied`/`Unavailable`/`Failed`, stale/future revision handling, and bounded failure validation (`chroma/src/theme_dbus.rs:163-237`).

On a real mode change the root persists before updating memory, publishes the full snapshot, and enqueues native Chroma concerns (`chroma/src/daemon.rs:231-247`). Same-mode requests do not advance revision but still enqueue native application; overflow rejects before side effects (`chroma/src/daemon.rs:435-443`). Native concern application is now Terminal/Desktop/Ghostty/Pi only (`chroma/src/theme.rs:89-100`, `541-602`), so Emacs is not a Chroma scheduler concern.

The plugin provides `chroma-theme` and global `chroma-theme-mode`. It subscribes to desired state and owner changes before registering; registration errors remain recoverable through a later owner event (`chroma-emacs/lisp/chroma-theme.el:49-95`, `260-300`). It rejects stale revisions before normalizing state, reapplies duplicate current revisions, loads a configured target theme before disabling the opposite, restores exact theme order and overlays, verifies the postcondition, and reports a bounded typed failure on error (`chroma-emacs/lisp/chroma-theme.el:120-228`).

Home owns all concrete assets and process wiring. It generates Ignis themes from its palette and installs them at `.config/emacs-ignis-themes` (`CriomOS-home/modules/home/base.nix:21-106`, `139-153`), configures the plugin symbols/load path (`CriomOS-home/modules/home/emacs/chroma-theme-init.el:1-11`), packages it into the exact `emacs-pgtk` set and enables the resident daemon (`CriomOS-home/modules/home/profiles/med/emacs.nix:14-18`, `109-112`, `313-318`, `794-803`), and runs Chroma as a restarted user service without an Emacs adapter (`CriomOS-home/modules/home/profiles/min/chroma.nix:107-187`).

## Observed behavioral proof

- Chroma state and projection tests passed 12/12 with `cargo test --test theme_dbus --test state`.
- Chroma’s ignored real session-bus witness passed 1/1 under `dbus-run-session`, including durable restore, sender ownership, owner disappearance, status, signals, and service restart (`chroma/src/theme_dbus.rs:409-552`).
- chroma-emacs ERT passed 9/9 (`chroma-emacs/test/chroma-theme-test.el:56-237`).
- The plugin source contains a separate production-transport private-bus script and Nix check (`chroma-emacs/test/run-isolated-dbus-daemon.sh:35-136`, `chroma-emacs/nix/checks.nix:3-23`).
- Home’s real resident witness is wired to run Chroma plus Emacs with private state/runtime directories, check package/native closure, wait on event files, inspect D-Bus `Applied` status and rendered Emacs faces, then restart both daemons (`CriomOS-home/checks/chroma-emacs-resident/run.sh:16-160`). A direct build in the standalone checkout did not reach this witness: Nix evaluation stopped because `stubs/no-system` requires an OS-provided target system/horizon input.

## Inference from the observed code

- Chroma is the semantic authority and durable source of desired theme state; Emacs is a projection client, not a scheduler or palette generator.
- The D-Bus service and root actor are the control boundary; the UDS remains the CLI/control boundary for Chroma’s broader visual axes.
- Chroma’s `Applied` status means the plugin reported a successful local postcondition; it does not mean every native Chroma concern succeeded, because concern actors log their own failures (`chroma/src/theme.rs:702-710`, `739-746`, `822-829`).
- Restart recovery is asymmetric by design: desired state/revision survives in redb, while owner/status returns to `Unavailable` until a fresh client registration.
- The Home resident check is the only checked-out artifact that attempts a full cross-process Chroma plus Emacs runtime proof; repository-local tests isolate transport and projection logic.

## Unknown or unresolved from this trace

- The Home resident Nix check’s runtime result was not observed in this environment because standalone Home evaluation aborts at the no-system stub. A target-provided `system`/`horizon` evaluation is needed to call it a witness.
- The plugin README’s stated matching Chroma revision `d6cea6…` is inconsistent with the live Home/Chroma pin `6a8e4c6…` (`chroma-emacs/README.md:30-32`; Home `flake.nix:146`, `151`). This is documentation drift; the live wire constants match, but the exact historical cause is unknown.
- This trace did not run the full Chroma flake `checks.default` or `checks.sandbox-terminal`; only the targeted state/projection tests and private D-Bus witness were executed.

## Sources

- `flows/ad443ccd/witnesses/currentArchitecture.md`
- `flows/01a02b4b/log.md`
- `flows/01a02b4b/vision/emacsPlugin.md`
- `flows/01a0238b/vision/emacsPlugin.md`
- `/git/github.com/LiGoldragon/chroma/src/daemon.rs`
- `/git/github.com/LiGoldragon/chroma/src/theme_dbus.rs`
- `/git/github.com/LiGoldragon/chroma/src/state.rs`
- `/git/github.com/LiGoldragon/chroma/src/theme.rs`
- `/git/github.com/LiGoldragon/chroma/tests/theme_dbus.rs`
- `/git/github.com/LiGoldragon/chroma/tests/state.rs`
- `/git/github.com/LiGoldragon/chroma-emacs/lisp/chroma-theme.el`
- `/git/github.com/LiGoldragon/chroma-emacs/test/chroma-theme-test.el`
- `/git/github.com/LiGoldragon/chroma-emacs/test/run-isolated-dbus-daemon.sh`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/chroma.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/emacs.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/base.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/chroma-emacs-resident/run.sh`
