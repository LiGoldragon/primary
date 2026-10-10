# Chroma Emacs correction

Work started against `chroma-emacs` revision `0b502607e7a20e08e33f675c6ac3e77696c755fa`. The corrected client validates a non-negative revision and rejects an older one before it normalizes state, applies themes, changes `chroma-theme--last-revision` or `chroma-theme--last-diagnostic`, or reports a result. A duplicate current revision remains a deliberate reconciliation.

`chroma-theme-stale-invalid-snapshot-is-a-strict-no-op` was observed red before the correction: after revision 4, a stale unknown state at revision 3 changed the remembered revision to 3. It is green after the correction. `chroma-theme-stale-registration-reply-is-not-normalized` separately covers an obsolete malformed registration reply.

The durable `isolated-daemon` check runs a private `dbus-run-session`, a test-only Emacs peer owning `io.github.LiGoldragon.Chroma` at `/io/github/LiGoldragon/Chroma/Theme` with `io.github.LiGoldragon.Chroma.Theme1`, and a separate Emacs daemon using production client D-Bus calls. It observes late service appearance and registration snapshot, `DesiredStateChanged`, `ReportProjection("emacs", revision, "Applied", "", "")`, `ReportProjection("emacs", revision, "Failed", code, summary)`, owner loss/reappearance, and re-registration. The peer writes registration/report events to a private FIFO, so each readiness edge is the actual event under test rather than an implicit callback race or a sleep. Stale no-op behavior remains directly witnessed by focused ERT.

Chroma revision `d6cea6bcb41fb75d8a268cd46c66120eb694562c` is the final wire ground. Its service, path, interface, registration reply, desired-state signal, and consumer label match this client. It fixes `ReportProjection` to five arguments in all cases; the plugin and fake peer now use the two required empty strings for Applied. `GetProjectionStatus("emacs") -> (status, revision)` is an observer method provided by Chroma and is not a client operation, so no client mismatch remains.

Local green witnesses: `bash test/run-ert.sh .` (9 ERT tests), `bash test/run-isolated-dbus-daemon.sh .`, and Nix evaluation of `default`, `ert`, and `isolated-daemon`. Remote green witnesses: `nix build --no-link --max-jobs 0 .#checks.x86_64-linux.ert` and `nix build --no-link --max-jobs 0 .#checks.x86_64-linux.isolated-daemon`, using the configured `prometheus.goldragon.criome` builder. The first isolated remote run revealed that a sandbox has no `/etc/dbus-1/session.conf`; the check now injects dbus’s Nix-provided session config.

At plugin revision `d432f95d`, a real Home witness found that `load-theme` moves a newly enabled Chroma base theme to the front of `custom-enabled-themes`, where it overrides an unrelated overlay even though the overlay remains enabled. The red regression recorded `(chroma-theme-test-dark chroma-theme-test-overlay)` after a Dark switch instead of `(chroma-theme-test-overlay chroma-theme-test-dark)`. The correction computes the original list with only the Chroma symbol replaced, then calls Emacs `enable-theme` from low to high precedence; it does not reload any unrelated source. Green ERT asserts both the exact list and rendered `mode-line` foreground `#335577`; the private-bus witness repeats that assertion for a live `DesiredStateChanged` transition. The package version is `0.1.2`.

## Sources

- `flows/01a0238b/vision/emacsPlugin.md`
- `flows/a1c42681/reports/chromaEmacsSliceOne.md`
- `/git/github.com/LiGoldragon/chroma` revision `d6cea6bcb41fb75d8a268cd46c66120eb694562c`, `src/theme_dbus.rs`, `README.md`
- Flow `9315a924` command witnesses
