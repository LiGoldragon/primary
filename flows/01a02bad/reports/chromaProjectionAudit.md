# Chroma projection audit

## Scope

Read-only audit of Chroma origin revision
`d6cea6bcb41fb75d8a268cd46c66120eb694562c` against the accepted resident
Emacs projection design, and of chroma-emacs origin revision
`d432f95db5837e685e32afbf5790060fb15a3703` against the resulting server wire.
No product repository, GitHub state, deployment, or runtime state was changed.

The full revisions were resolved from `main@origin` after
`jj git fetch --remote origin`; both worktrees were clean.

## Outcome

The server and client wire shapes match. Persistence, legacy migration,
sender binding, second-owner rejection, transient owner-loss status, client
stale handling, duplicate reconciliation, failure vocabulary, and old active
Emacs-concern removal are present.

The slice is not fully proved. Chroma's bus test uses a test-only Rust
interface instead of the production `ThemeDbusService`, and the default Chroma
Nix check does not force a private session bus. No test combines actual Chroma
service restart with persisted revision recovery and owner status.

## Confirmed implementation

### Wire compatibility

`src/theme_dbus.rs:20-31,283-334` and
`chroma-emacs/lisp/chroma-theme.el:35-95` agree on:

- service `io.github.LiGoldragon.Chroma`;
- object `/io/github/LiGoldragon/Chroma/Theme`;
- interface `io.github.LiGoldragon.Chroma.Theme1`;
- `RegisterConsumer(string) -> (string, uint64)`;
- `DesiredStateChanged(string, uint64)`;
- fixed five-argument `ReportProjection(string, uint64, string, string, string)`;
- `GetProjectionStatus(string) -> (string, uint64)`.

Applied reports carry empty code and summary on both sides. The server's
capitalized `Light`/`Dark` values are accepted by the client's normalization.

### Persistence and change revisions

`src/state.rs:36-65,288-312` persists `{ThemeMode, revision}` in the existing
theme table and migrates a legacy theme-only archive to revision zero.
`src/daemon.rs:221-234` persists before mutating memory or publishing and does
not allocate a revision for an unchanged mode. State-store migration/reopen and
reducer tests passed.

### Sender and owner model

`src/theme_dbus.rs:185-195,208-231` allowlists `emacs`, stores the D-Bus
unique sender, rejects another live sender, binds reports to that sender, and
clears ownership/status to `Unavailable` on matching owner disappearance.
These behaviors are covered by in-memory reducer tests, but not by a
production-service D-Bus test.

### Client behavior

`chroma-emacs/lisp/chroma-theme.el:195-223` rejects stale snapshots before
normalization or mutation, reapplies equal revisions to repair drift, verifies
theme membership before Applied, preserves unrelated themes, and maps local
diagnostics to bounded typed failures. ERT 8/8 and the private-bus client
witness passed.

### Removal

`src/theme.rs` contains only Terminal, Desktop, Ghostty, and Pi concern
variants; `src/config.rs:335-350` parses only the remaining Dconf adapter.
No active `EmacsThemeConcern`, `EmacsAdapter`, or `Emacsclient` implementation
remains in Chroma. `skills.md:35` mentions `emacsclient` only to prohibit a
compatibility path. The unintegrated CriomOS-home checkout still has old
one-shot integration references; no Home revision was supplied for this audit.

## Defects

### F1 — owner watcher does not filter the disappeared name

`src/theme_dbus.rs:367-371` subscribes to every `NameOwnerChanged` signal.
`src/theme_dbus.rs:399-405` discards the name and forwards every nonempty-owner
to-empty-owner event as `ProjectionOwnerDisappeared`.

The reducer then compares only the old unique sender at `:226-231`. A consumer
sender that owns more than one well-known name can therefore lose its Chroma
projection when it relinquishes an unrelated name while remaining connected.
The watcher must scope the event to Chroma's service/name or otherwise track
the registered sender's unique-name disappearance. The existing owner-loss
unit test cannot detect this because it calls the reducer directly.

### F2 — stale failed reports bypass failure bounds

`ProjectionReport::validate` correctly enforces the failure-code vocabulary and
240-byte summary bound at `src/theme_dbus.rs:117-129`. However,
`ThemeProjection::report` returns `Ok(())` for a lower revision at lines
208-218 before invoking `report.validate()`.

Consequently, a stale `Failed` report with an invalid code or oversized summary
is accepted at the protocol boundary. It does not change status, but the
declared trust/bounds contract is not enforced for all inputs. Validation must
precede the stale no-op, or the protocol must explicitly document that stale
failure payloads are exempt.

### F3 — saturating revision increment breaks the monotonic identity at max

`src/daemon.rs:221-224` uses `self.theme_revision.saturating_add(1)`. If the
persisted revision is `u64::MAX`, a mode change reuses that revision while
changing the desired mode. The client treats equal revisions as a duplicate
that may be reapplied, so revision identity no longer describes a unique
desired snapshot. There is no boundary test. The implementation should reject
further changes at the maximum or use an explicitly ruled rollover strategy;
silent reuse is not monotonic revisioning.

## Proof gaps and unresolved intent

- `tests/session_dbus.rs:15-86` uses a real session bus only when wrapped, but
  exports `SessionContract`, not `ThemeDbusService`. It does not exercise the
  actual zbus server, status method, failure validation, sender binding,
  second-owner rejection, or owner watcher.
- `flake.nix:75-77` runs ordinary Cargo tests. Without a bus,
  `tests/session_dbus.rs:57-62` prints a skip and returns success. The durable
  Chroma check therefore does not require the private-bus witness.
- `tests/state.rs:123-151` proves redb reopen/migration, while the client
  script's peer replacement proves only fake-service owner loss/reappearance.
  No actual Chroma daemon restart is witnessed together with persisted revision
  and `Unavailable`/re-registration status.
- `tests/theme_dbus.rs:21-31` tests a stale lower report and duplicate Applied,
  but not duplicate Failed, conflicting same-revision reports, or invalid
  stale failure payloads. Whether same-revision status changes are allowed is
  not settled by the audit brief.
- Full failure diagnostics remain local in the client by code inspection, but
  no test asserts diagnostic preservation after a real D-Bus failure.
- A strict “no old term anywhere” reading is unresolved: the active Chroma
  implementation is removed, but a negative `emacsclient` sentence remains in
  `skills.md`, historical Beads records retain the old name, and
  CriomOS-home still awaits its later integration slice.

## Commands and results

- `jj git fetch --remote origin` in both repositories: `Nothing changed`.
- `jj log -r 'main@origin' ...`: resolved both full commit IDs above.
- `jj status` in both repositories: no changes.
- `cargo test --locked` in Chroma: all tests passed, including 4 reducer,
  1 session-bus, and 6 state tests.
- `dbus-run-session -- cargo test --locked --test session_dbus -- --nocapture`:
  1 test passed on a private bus, using the test-only service.
- `bash test/run-ert.sh /git/github.com/LiGoldragon/chroma-emacs`: 8/8 passed.
- `bash test/run-isolated-dbus-daemon.sh /git/github.com/LiGoldragon/chroma-emacs`:
  exit 0; private-bus client/fake-peer witness passed.
- `nix flake check --no-build --no-update-lock-file` in both repositories:
  evaluation passed on x86_64-linux; no runtime build was performed.

## Correction audit — 2026-08-23

The re-audit used Chroma origin revision
`9248420ef8ccff005aa1a5e0e5d8e5505755269e` (“Correct Chroma theme projection
protocol”), resolved after `jj git fetch --remote origin`; the working copy
was clean. The chroma-emacs comparison revision remains
`d432f95db5837e685e32afbf5790060fb15a3703`.

All three implementation defects identified above are corrected:

- F1 is fixed by `unique_owner_disappeared` at
  `src/theme_dbus.rs:241-246`, which requires an empty replacement owner, a
  unique-name-shaped changed name, and equality with the old owner. The
  watcher applies it at `src/theme_dbus.rs:560-565`; unit coverage is at
  `src/theme_dbus.rs:398-406`. The durable witness releases an unrelated
  well-known name and confirms `Pending` at `src/theme_dbus.rs:489-496`, then
  drops the real client unique owner and confirms `Unavailable` at
  `src/theme_dbus.rs:513-537`.
- F2 is fixed because `report.validate()` precedes stale-revision handling at
  `src/theme_dbus.rs:208-226`. `tests/theme_dbus.rs:33-50` now rejects an
  invalid stale failure code and an oversized stale summary while accepting a
  valid stale no-op. The real-bus witness checks an invalid current report at
  `src/theme_dbus.rs:497-503`, but does not itself send an invalid stale
  report; the reducer test is the coverage for that edge.
- F3 is fixed by `next_theme_revision` and checked addition at
  `src/daemon.rs:228-244,431-450`, with `Error::ThemeRevisionExhausted` at
  `src/error.rs:99-101`. A real change at `u64::MAX` is rejected before
  persistence, application, or publication; a same-mode no-op remains valid.

The previous bus-test proof gap is closed for the service boundary. The old
`tests/session_dbus.rs` fake contract is deleted. The ignored durable test at
`src/theme_dbus.rs:409-545` creates a temporary redb store, starts the actual
`ChromaRoot` (`src/daemon.rs:144-180`), starts the actual
`ThemeDbusService` (`src/theme_dbus.rs:353-368`), registers over a real
private session bus, rejects a second live sender, exercises unrelated-name
filtering and unique-owner loss, returns the full registration snapshot,
receives a two-field full `DesiredStateChanged` body, and restarts the D-Bus
service. It has no no-bus success path: `Connection::session().await` is an
`expect`, and `flake.nix:78-82` wraps the ignored test in
`dbus-run-session` as `checks.session-dbus`.

The correction is therefore a grounded clean result for the three prior
implementation defects and for the real service/transport witness. The
remaining proof gap is narrower: the test restarts `ThemeDbusService` on the
same in-memory `ChromaRoot` and `StateStore` actor at
`src/theme_dbus.rs:539-544`; it does not stop and recreate the root/process,
reopen redb, change a persisted revision, and then verify revision recovery
plus `Unavailable`/re-registration. The durable test also does not exercise
both same-current Applied↔Failed transitions or stale-invalid payloads over
the wire; `tests/theme_dbus.rs:53-66` and `:33-50` cover those reducer paths.

The strict “no old term anywhere” question remains as previously recorded:
active Chroma concern/adapter code is absent, while `skills.md:35` retains a
negative `emacsclient` prohibition, historical Beads text retains old names,
and no approved CriomOS-home revision was supplied for the integration side.

Correction commands and results:

- `jj git fetch --remote origin` and `jj log -r 'main@origin' ...`: no remote
  changes; resolved `9248420ef8ccff005aa1a5e0e5d8e5505755269e`.
- `jj status`: Chroma working copy clean.
- `cargo test --locked`: passed; 2 ordinary unit tests passed and the durable
  test was reported ignored as intended, with all integration tests passing.
- `dbus-run-session -- cargo test --locked --lib actual_theme_dbus_service_binds_the_real_protocol_to_unique_bus_owners -- --ignored --nocapture`:
  1 durable real-service test passed.
- `nix flake check --no-build --no-update-lock-file`: all x86_64-linux flake
  outputs and the new `checks.session-dbus` derivation evaluated successfully;
  this command was evaluation-only.

## Sources

- `/home/li/primary/flows/01a0238b/reports/emacsAdapterDesign.md`
- `/home/li/primary/flows/01a0238b/vision/emacsPlugin.md`
- `/home/li/primary/flows/01a02b4b/vision/emacsPlugin.md`
- `/home/li/primary/flows/01a02bad/witnesses/chromaProjectionAudit.md`
- `/git/github.com/LiGoldragon/chroma/src/theme_dbus.rs`
- `/git/github.com/LiGoldragon/chroma/src/daemon.rs`
- `/git/github.com/LiGoldragon/chroma/src/state.rs`
- `/git/github.com/LiGoldragon/chroma/src/theme.rs`
- `/git/github.com/LiGoldragon/chroma/src/config.rs`
- `/git/github.com/LiGoldragon/chroma/tests/theme_dbus.rs`
- `/git/github.com/LiGoldragon/chroma/tests/session_dbus.rs`
- `/git/github.com/LiGoldragon/chroma/tests/state.rs`
- `/git/github.com/LiGoldragon/chroma/flake.nix`
- `/git/github.com/LiGoldragon/chroma-emacs/lisp/chroma-theme.el`
- `/git/github.com/LiGoldragon/chroma-emacs/test/chroma-theme-test.el`
- `/git/github.com/LiGoldragon/chroma-emacs/test/run-isolated-dbus-daemon.sh`
- `/git/github.com/LiGoldragon/chroma-emacs/nix/checks.nix`
