# Current Chroma–Emacs architecture

Method: code read `/home/li/primary/flows/01a02b4b/log.md`, `flows/01a02b4b/reports/chromaCorrectiveProof.md`, and `flows/01a02b4b/vision/*.md`.

Method: code read `/git/github.com/LiGoldragon/chroma/src/daemon.rs`, `src/theme_dbus.rs`, `src/state.rs`, `src/theme.rs`, `src/config.rs`, `tests/theme_dbus.rs`, `tests/state.rs`, and `flake.nix`.

Method: code read `/git/github.com/LiGoldragon/chroma-emacs/lisp/chroma-theme.el`, `test/chroma-theme-test.el`, `test/fake-chroma-service.el`, `test/run-isolated-dbus-daemon.sh`, `nix/checks.nix`, and `flake.nix`.

Method: code read `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`, `modules/home/profiles/min/chroma.nix`, `modules/home/profiles/med/emacs.nix`, `modules/home/emacs/chroma-theme-init.el`, `modules/home/base.nix`, `checks/chroma-emacs-resident/default.nix`, `checks/chroma-emacs-resident/run.sh`, and `checks/chroma-dotos-config/default.nix`.

Method: probe `jj status` and `jj log` in the three product repositories on 2026-08-23.

Method: probe `cargo test --test theme_dbus --test state` in `/git/github.com/LiGoldragon/chroma` on 2026-08-23.

Method: probe `dbus-run-session -- cargo test --lib actual_theme_dbus_service_binds_the_real_protocol_to_unique_bus_owners -- --ignored` in `/git/github.com/LiGoldragon/chroma` on 2026-08-23.

Method: probe `bash test/run-ert.sh .` in `/git/github.com/LiGoldragon/chroma-emacs` on 2026-08-23.

Method: probe `nix build --no-link .#checks.x86_64-linux.chroma-emacs-resident` in `/git/github.com/LiGoldragon/CriomOS-home` on 2026-08-23.

Observed repository state:

- Chroma is clean at main `6a8e4c6a9bb0be0a76baa43b975df91edf6752f9` (`6a8e4c6a`, “Preserve durable theme state on startup”).
- chroma-emacs is clean at main `119a231358cf69c16161812caf69fff4b726be5c` (`119a2313`, “Preserve overlay priority across theme switches”).
- CriomOS-home is clean at main `a61b02d0cf69de757bdf8b5fa0f336f78f5054ee` (`a61b02d0`, “home: prove resident Chroma projection closure”).
- CriomOS currently pins CriomOS-home to `a61b02d0` in `flake.nix:35-49`. Home pins Chroma `6a8e4c6a` and chroma-emacs `119a2313` in `flake.nix:143-152`; the same revisions are in `flake.lock`.

Observed current entry points and actors:

- `chroma-daemon` is a Tokio multi-thread binary that calls `chroma::daemon::run` (`chroma/src/bin/chroma_daemon.rs:7-10`). `run` loads the default config, starts the Kameo `ChromaRoot`, starts `ThemeDbusService`, config and sleep watchers, reapplies state, starts schedules, then binds the framed UDS (`chroma/src/daemon.rs:59-104`).
- The root owns theme mode/revision, `ThemeProjection`, optional signal publisher, state-store reference, per-axis appliers, and schedule reference (`chroma/src/daemon.rs:123-136`). `ChromaRoot::start_with_state_store` restores state, starts appliers, creates the root, and installs the schedule actor (`chroma/src/daemon.rs:144-192`).
- The D-Bus service owns a session connection, requests `io.github.LiGoldragon.Chroma`, exports `/io/github/LiGoldragon/Chroma/Theme`, installs a signal publisher into the root, and starts a `NameOwnerChanged` watcher (`chroma/src/theme_dbus.rs:20-27`, `347-369`). The watcher sends owner-loss messages only for a disappearing unique name (`chroma/src/theme_dbus.rs:241-246`, `555-575`).
- `ThemeApplier` fans out to Terminal, Desktop, Ghostty, and Pi concern actors; the Emacs concern and `emacsclient` adapter are absent (`chroma/src/theme.rs:89-100`, `487-493`, `541-602`). Concern handlers log native application failures (`chroma/src/theme.rs:702-710`, `739-746`, `822-829`), while the root's D-Bus projection status is acknowledged by the external plugin.
- The Home systemd user unit is the process supervisor for Chroma, requiring wl-gammarelay and restarting on failure (`CriomOS-home/modules/home/profiles/min/chroma.nix:149-170`). Its activation writes the native DOTOS config with Terminal/Desktop/Ghostty/Pi and no Emacs adapter (`.../chroma.nix:107-137`, `172-187`).
- Home's Emacs module creates one exact `emacs-pgtk` package set, adds the pinned chroma-emacs package, enables `programs.emacs` and `services.emacs` with the same package, and starts the global mode in generated init (`CriomOS-home/modules/home/profiles/med/emacs.nix:14-18`, `109-112`, `313-318`, `794-803`).

Observed data and control flow:

1. A CLI request enters the UDS server, is decoded from a length-prefixed rkyv frame, sent to the root, and returned as a framed response; actor failures become `Response::Error` (`chroma/src/daemon.rs:107-121`).
2. `SetTheme` calls `ChromaRoot::set_theme`. A real mode change allocates the next revision, persists `(mode, revision)`, updates the root projection, publishes `DesiredStateChanged` if the publisher exists, then enqueues native theme application; an already-current mode keeps its revision but still enqueues native application (`chroma/src/daemon.rs:231-247`, `435-443`).
3. The public wire is a fixed zbus ABI: `RegisterConsumer(string) -> (string state, u64 revision)`, `ReportProjection(string consumer, u64 revision, string result, string code, string summary)`, `GetProjectionStatus(string) -> (string status, u64 revision)`, and `DesiredStateChanged(string state, u64 revision)` (`chroma/src/theme_dbus.rs:20-31`, `293-345`). The server extracts the unique D-Bus sender from the message header and routes all operations into the root actor (`chroma/src/theme_dbus.rs:270-331`).
4. `ThemeProjection` accepts only `emacs`, binds one live sender, returns `Pending` on registration, enters `Pending` on desired revision replacement, validates bounded failure vocabulary/summary, ignores valid stale reports, rejects future revisions, and records current `Applied` or `Failed` status (`chroma/src/theme_dbus.rs:163-237`).
5. `StateStore` is a dedicated Kameo actor around redb at `$XDG_STATE_HOME/chroma/state.redb`; the `theme/current` value is an archived `StoredThemeState` (`ThemeMode`, `u64`), and a legacy theme-only archive is migrated to revision zero (`chroma/src/state.rs:1-5`, `21-25`, `36-65`, `207-313`, `343-455`).
6. The Emacs mode subscribes to desired-state and owner signals before registration. A registration failure is logged and left to a future owner event. A stale/invalid revision is a no-op before state normalization; a current duplicate reapplies and verifies. Application loads the target before disabling the opposite Chroma theme, restores the exact enabled-theme order, verifies the postcondition, and on failure restores only the Chroma-owned subset while retaining the full diagnostic locally (`chroma-emacs/lisp/chroma-theme.el:49-95`, `97-199`, `230-300`).
7. Emacs reports `Applied` with empty code/summary or maps local errors to `configuration`, `load-failed`, `verification-failed`, or `application-failed`, truncating the UTF-8 summary to 240 bytes (`chroma-emacs/lisp/chroma-theme.el:201-228`).
8. Home generates `ignis-dark-theme.el` and `ignis-light-theme.el` from its Base16 palettes and installs them under `.config/emacs-ignis-themes`; the plugin receives only the path and symbols (`CriomOS-home/modules/home/base.nix:21-106`, `139-153`; `.../emacs/chroma-theme-init.el:1-11`). The Emacs init build includes the plugin in the exact package closure and byte/native-compiles init (`.../profiles/med/emacs.nix:657-717`).

Observed error and recovery paths:

- A missing/unavailable session bus causes `ThemeDbusService::start` to fail before the UDS listener is bound because `run` uses `?` at service startup (`chroma/src/daemon.rs:60-75`; `chroma/src/theme_dbus.rs:353-362`).
- D-Bus owner loss is converted to `Unavailable`; a new owner must register again, and service restart keeps the desired snapshot but not a live owner (`chroma/src/theme_dbus.rs:229-237`; `chroma/src/daemon.rs:642-651`).
- Revision exhaustion rejects a real mode change before persistence, native application, or signal publication (`chroma/src/daemon.rs:231-245`, `435-443`).
- Chroma persists desired state before native application. Native concern errors are logged by concern actors and are not translated into Emacs projection failures; the latter originate only from the plugin's load/verification path (`chroma/src/daemon.rs:236-246`; `chroma/src/theme.rs:702-710`, `739-746`, `822-829`; `chroma-emacs/lisp/chroma-theme.el:175-228`).
- The plugin's owner callback reconnects only when the well-known Chroma name receives a non-empty new owner (`chroma-emacs/lisp/chroma-theme.el:276-291`).

Behavioral probes:

- `cargo test --test theme_dbus --test state`: 12 tests passed (6 state, 6 projection).
- `dbus-run-session -- cargo test --lib actual_theme_dbus_service_binds_the_real_protocol_to_unique_bus_owners -- --ignored`: 1 test passed; it covered durable restart state, registration, second-owner rejection, unrelated-name release, fixed report shape, signal body, unique-owner disappearance, `Unavailable`, and service restart (`chroma/src/theme_dbus.rs:409-552`).
- `bash test/run-ert.sh .`: 9 ERT tests passed, covering theme transitions, overlay priority, subscribe-before-register, owner re-registration, stale/duplicate revisions, stale malformed snapshots, application failure restoration, and bounded reports (`chroma-emacs/test/chroma-theme-test.el:56-237`).
- The plugin's separate isolated D-Bus script is a real production-transport peer witness for late service appearance, signal/application, `Applied` and `Failed` signatures, owner loss/reappearance, and re-registration (`chroma-emacs/test/run-isolated-dbus-daemon.sh:35-136`; `chroma-emacs/nix/checks.nix:3-23`).
- Home's resident check is wired to start a real Chroma daemon and isolated Emacs daemon, assert `Applied` status and rendered faces, restart Chroma, and restart Emacs (`CriomOS-home/checks/chroma-emacs-resident/default.nix:1-75`; `.../run.sh:65-160`). Attempting `nix build --no-link .#checks.x86_64-linux.chroma-emacs-resident` from the standalone Home checkout failed at flake evaluation because `stubs/no-system` requires an OS-provided system/horizon input; this is an environment/setup boundary, not a product-test result.

Observed documentation drift:

- `chroma-emacs/README.md:30-32` says the inspection surface matches Chroma `d6cea6…`, while Home's live input and the checked-out Chroma source are `6a8e4c6…`. The actual wire constants in Chroma and plugin agree; the README revision sentence is stale relative to the current Home pin.

## Sources

- `flows/01a02b4b/log.md`
- `flows/01a02b4b/reports/chromaCorrectiveProof.md`
- `flows/01a02b4b/vision/emacsPlugin.md`
- `flows/01a0238b/vision/emacsPlugin.md`
- `witnesses/currentArchitecture.md`
- `/git/github.com/LiGoldragon/chroma/src/daemon.rs`
- `/git/github.com/LiGoldragon/chroma/src/theme_dbus.rs`
- `/git/github.com/LiGoldragon/chroma/src/state.rs`
- `/git/github.com/LiGoldragon/chroma/src/theme.rs`
- `/git/github.com/LiGoldragon/chroma/tests/theme_dbus.rs`
- `/git/github.com/LiGoldragon/chroma/tests/state.rs`
- `/git/github.com/LiGoldragon/chroma-emacs/lisp/chroma-theme.el`
- `/git/github.com/LiGoldragon/chroma-emacs/test/chroma-theme-test.el`
- `/git/github.com/LiGoldragon/chroma-emacs/test/run-isolated-dbus-daemon.sh`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/chroma.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/emacs.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/base.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/chroma-emacs-resident/run.sh`
