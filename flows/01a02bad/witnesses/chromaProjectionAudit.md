# Chroma projection audit witnesses

Method: code read `/home/li/primary/flows/01a0238b/reports/emacsAdapterDesign.md`,
`/home/li/primary/flows/01a0238b/vision/emacsPlugin.md`, and
`/home/li/primary/flows/01a02b4b/vision/emacsPlugin.md`.

Observed: the accepted shape is a resident same-user session-D-Bus consumer;
Chroma owns desired Light/Dark state and a persisted monotonic revision;
registration returns a snapshot; changed snapshots are signalled; reports are
typed and bounded; owner loss is `Unavailable`; the plugin subscribes before
registering, ignores stale revisions, and reapplies duplicate current
revisions. Ignis generation and declarative deployment remain Home-owned.

Method: probe `jj git fetch --remote origin` in
`/git/github.com/LiGoldragon/chroma` and
`/git/github.com/LiGoldragon/chroma-emacs`.

Observed: both remotes reported `Nothing changed`.

Method: probe `jj log -r 'main@origin' --no-graph -T 'commit_id ++ "\\n" ++ description.first_line() ++ "\\n"'` in both repositories.

Observed: Chroma origin is
`d6cea6bcb41fb75d8a268cd46c66120eb694562c`, “Implement resident Emacs
D-Bus projection”; chroma-emacs origin is
`d432f95db5837e685e32afbf5790060fb15a3703`, “Fix stale Chroma snapshot
reconciliation”.

Method: probe `jj status` in both repositories.

Observed: both working copies had no changes; each had only an empty working
copy above the requested `main` commit.

Method: code read `/git/github.com/LiGoldragon/chroma/src/theme_dbus.rs`.

Observed: constants at lines 20–31 define the service, path, interface,
consumer, failure vocabulary, and 240-byte bound. The reducer at lines
185–231 binds registration and reports to a sender, rejects a different live
owner, transitions owner loss to `Unavailable`, ignores lower revisions, and
updates current status. The exported interface at lines 283–334 defines
`RegisterConsumer(string) -> (string, uint64)`, fixed five-argument
`ReportProjection`, `GetProjectionStatus(string) -> (string, uint64)`, and
`DesiredStateChanged(string, uint64)`. Owner watching at lines 367–405 parses
all `NameOwnerChanged` signals but does not filter the name before forwarding
owner disappearance.

Method: code read `/git/github.com/LiGoldragon/chroma/src/daemon.rs` and
`/git/github.com/LiGoldragon/chroma/src/state.rs`.

Observed: `ChromaRoot::set_theme` at `src/daemon.rs:221-234` only allocates a
revision when the mode changes, persists before updating memory, then publishes
the snapshot. It uses `saturating_add(1)`. `StoredThemeState` is loaded and
legacy `ThemeMode` archives are migrated to revision zero at
`src/state.rs:288-312`.

Method: code read `/git/github.com/LiGoldragon/chroma-emacs/lisp/chroma-theme.el`.

Observed: constants and transport calls at lines 35–95 match the server names
and positional signatures. Snapshot handling at lines 195–223 rejects invalid
and stale revisions before normalization, reapplies equal revisions, applies
before reporting, and sends only typed bounded failures. Registration subscribes
first and owner reappearance reconnects at lines 234–256.

Method: code read `/git/github.com/LiGoldragon/chroma/tests/session_dbus.rs` and
`/git/github.com/LiGoldragon/chroma/flake.nix`.

Observed: `tests/session_dbus.rs:15-86` opens a real zbus connection when run
under a session bus, but exports a test-only `SessionContract`; it does not
export `ThemeDbusService`, test status, sender ownership, owner loss, or restart.
`flake.nix:75-77` exposes ordinary Cargo tests as the default check and does
not wrap them in `dbus-run-session`; `tests/session_dbus.rs:57-62` returns
success when no bus address exists.

Method: code read `/git/github.com/LiGoldragon/chroma-emacs/test/run-isolated-dbus-daemon.sh`.

Observed: lines 27–124 start a private `dbus-run-session`, an isolated Emacs
client, and fake peer daemons. The script exercises production Emacs D-Bus
subscribe/call functions, late service appearance, signals, fixed Applied and
Failed reports, stale signal no-op, peer owner loss, reappearance, and
re-registration. The peer is not Chroma's Rust service.

Method: probe `cargo test --locked` in `/git/github.com/LiGoldragon/chroma`.

Observed: all Cargo test binaries passed, including 4 `theme_dbus` reducer
tests, 1 `session_dbus` test, and 6 state tests. The unwrapped session test used
the host bus in this environment.

Method: probe `dbus-run-session -- cargo test --locked --test session_dbus -- --nocapture` in `/git/github.com/LiGoldragon/chroma`.

Observed: the one test passed on a newly created private session bus, still
against the test-only `SessionContract`.

Method: probe `bash test/run-ert.sh /git/github.com/LiGoldragon/chroma-emacs` in `/git/github.com/LiGoldragon/chroma-emacs`.

Observed: 8 ERT tests passed, 0 unexpected.

Method: probe `bash test/run-isolated-dbus-daemon.sh /git/github.com/LiGoldragon/chroma-emacs` in `/git/github.com/LiGoldragon/chroma-emacs`.

Observed: exit status 0. The witness created a private bus and exercised the
production client transport against its test-only peer.

Method: probe `nix flake check --no-build --no-update-lock-file` in each pinned
repository.

Observed: both flakes evaluated successfully on x86_64-linux. This was
evaluation only, not a built runtime or deployment witness.

Method: probe `rg -n -i 'emacsclient|EmacsThemeConcern|EmacsAdapter|emacs_adapter|emacs-adapter'` over Chroma source, tests, and docs.

Observed: active old concern/adapter identifiers are absent from Chroma code
and configuration. `skills.md:35` retains `emacsclient` only in a negative
statement banning a compatibility path; historical Beads text and the
unintegrated CriomOS-home checkout still contain old integration references.

## Correction audit witness — 2026-08-23

Method: fetch and resolve Chroma `main@origin` after the correction.

Observed: `jj git fetch --remote origin` reported `Nothing changed`;
`jj log -r 'main@origin'` resolved
`9248420ef8ccff005aa1a5e0e5d8e5505755269e`; `jj status` reported a clean
working copy. The client comparison revision remains
`d432f95db5837e685e32afbf5790060fb15a3703`.

Method: inspect the corrected reducer, watcher, daemon revision allocator,
tests, flake, and README.

Observed: owner-loss filtering now requires a unique-name disappearance at
`src/theme_dbus.rs:241-246`, and the watcher uses that predicate at
`:560-565`. The unit test at `:398-406` rejects unrelated well-known-name
release. Stale reports validate before the stale no-op at `:208-226`; tests at
`tests/theme_dbus.rs:33-50` reject stale invalid failure code and 241-byte
summary. Same-current Applied↔Failed reconciliation is asserted at
`tests/theme_dbus.rs:53-66`. Revision exhaustion uses checked addition at
`src/daemon.rs:228-244,431-450`.

Method: inspect the new private-bus test at
`src/theme_dbus.rs:409-545` and its setup.

Observed: the witness creates a temporary redb store, starts
`ChromaRoot::start_with_state_store` and `ThemeDbusService::start`, then uses
real zbus proxies. It asserts the full `(Dark, 0)` registration snapshot and
`Pending` status (`:478-482`), rejects the second live sender (`:484-488`),
releases an unrelated well-known name without losing status (`:489-496`),
rejects an invalid current failure report and accepts the fixed five-argument
Applied report (`:497-503`), receives `(Light, 1)` from the real signal
interface (`:505-510`), observes unique-owner loss and `Unavailable`
(`:513-537`), and re-exports the service with status still `Unavailable`
(`:539-544`).

Observed: this test is ignored in ordinary Cargo runs but has no skip-on-bus
branch (`Connection::session().await.expect(...)` at `:463`). The dedicated
Nix check at `flake.nix:78-82` runs the exact ignored test under
`dbus-run-session`.

Method: run the corrected witnesses.

Observed: `cargo test --locked` passed. The explicit durable command
`dbus-run-session -- cargo test --locked --lib actual_theme_dbus_service_binds_the_real_protocol_to_unique_bus_owners -- --ignored --nocapture`
passed 1/1. `nix flake check --no-build --no-update-lock-file` evaluated all
outputs, including `checks.session-dbus`, successfully.

Remaining proof boundary: the durable test restarts only `ThemeDbusService`
on the same root/state actor. It does not recreate ChromaRoot or reopen redb,
so process-restart recovery of a nonzero persisted revision remains untested.
Stale-invalid and both current reconciliation directions remain reducer-level,
not real-bus assertions. Active old Chroma Emacs concern/adapter code remains
absent, with the previously recorded negative/documentary and unintegrated
Home references unresolved under a strict literal-removal reading.

## Sources

- `/git/github.com/LiGoldragon/chroma/src/theme_dbus.rs`
- `/git/github.com/LiGoldragon/chroma/src/daemon.rs`
- `/git/github.com/LiGoldragon/chroma/src/state.rs`
- `/git/github.com/LiGoldragon/chroma/tests/theme_dbus.rs`
- `/git/github.com/LiGoldragon/chroma/tests/session_dbus.rs`
- `/git/github.com/LiGoldragon/chroma/tests/state.rs`
- `/git/github.com/LiGoldragon/chroma/flake.nix`
- `/git/github.com/LiGoldragon/chroma-emacs/lisp/chroma-theme.el`
- `/git/github.com/LiGoldragon/chroma-emacs/test/chroma-theme-test.el`
- `/git/github.com/LiGoldragon/chroma-emacs/test/run-isolated-dbus-daemon.sh`
- `/git/github.com/LiGoldragon/chroma-emacs/README.md`
- `/home/li/primary/flows/01a0238b/reports/emacsAdapterDesign.md`
- `/home/li/primary/flows/01a0238b/vision/emacsPlugin.md`
- `/home/li/primary/flows/01a02b4b/vision/emacsPlugin.md`
- Flow `01a02bad`
