# Flow 0.17.4 three-live-start witness, stage two: attempt and blocker

Subflow of 8904b1, 2026-09-26. Scratch root: `/tmp/f74s2.Ym2hZI`
(created fresh, not `/tmp/flow0174-fx.hoygQ9`; left in place for review, not
removed). No Herdr session, workspace, tab, or pane was created by this
seat at any point. No Claude seat was ever spawned. **No pass or fail
verdict was reached for A, B, or C**: all three Start slots were consumed
by repeated, environment-driven `NativeLaunchRefused` on what was intended
as case A alone, before a usable environment was found. This is recorded
as a process fault of this run, disclosed below, not concealed.

## 0. Model display map (checked before the first Start, as ordered)

`config/model-display-names.json` maps `"claude-haiku-4-5-20251001":
"Haiku 4.5"` — **mapped**, not unmapped. A title is not refused for this
identifier on that ground.

## 1. Live baseline (before)

Stable `flow-nexus.service`: PID 1937 (0.12.2), active, 0 restarts. Next
`flow-nexus-next.service`: PID 90750 (0.17.1), active, 0 restarts. Stable
store `flow.sema`: 1,056,768 B, SHA-256 `f03f610a...c78c0f03`. Next store
(`/home/li/.local/state/flow-next/.local/state/flow/flow.sema`, the real
path — the plain `/home/li/.local/state/flow-next/flow.sema` in the fixed
facts does not exist; the store sits one level deeper): 581,632 B,
SHA-256 `ece72cc1...8d35e06e`. All four sockets present, mtimes recorded.
Herdr `session list`: `default` (running), `messaging-build` (stopped),
`recovery-56ae53` (running) — no test session. `agent list`: 10 agents,
all pre-existing.

**Observation, not a live write**: `flow 'List.{ }'` against the live
*stable* socket (0.12.2) through the 0.17.4 `flow` client answers
`Replaced.{          {                   {                            } } }`
— a decode artifact from wire-version skew between the 0.17.4 client's
`Response` enum and the running 0.12.2 service's wire bytes (rkyv archives
are position/tag based; a List reply's bytes are being reinterpreted
under a different variant tag). Repeated twice, byte-identical both
times; store hash and service PID/restart-count unchanged across both
calls, so this is a client-side textualization artifact of a read-only
query, not a live mutation. Recorded, not treated as the 25-row reading
stage one reported (that reading's raw bytes were not preserved for
comparison).

## 2. The fixture

`/tmp/f74s2.Ym2hZI/{home,run,source,work}`, new, empty, `run` mode 700 (17
characters, well under the SUN_LEN bound that broke stage one's first
try). Bundle file written at
`/tmp/f74s2.Ym2hZI/source/flow-system-prompt.md` (non-empty, absolute,
not a symlink — required by `LaunchComposer::validate`/`read_bundle` in
`composition.rs`).

## 3. The scratch service — three restarts, environment repair in the open

**Attempt 1** — `systemd-run --user` with only `HOME`, `XDG_RUNTIME_DIR`,
`FLOW_SOURCE_ROOT` set to scratch paths (as stage one's fixture recipe
gave it). Unit active, child PID 507055, store/sockets confirmed under
scratch by `/proc/<pid>/fd`, scratch `List.{ }` answered `Listed.[]`
(0 rows, not live). Start A sent: **`StartRejected.NativeLaunchRefused`**.

Diagnosis: `flow-nexus`'s `HerdrCli::default()` (`src/herdr.rs`) resolves
`claude_home` from `CLAUDE_CONFIG_DIR` or else `home.join(".claude")`,
where `home` is Flow's own `HOME` (scratch) — and its `herdr` subprocess
inherits `HOME=<scratch>`, so the `herdr` CLI itself looks for its own
config/session directory under `<scratch>/.config/herdr`, which does not
exist. Neither of these is under Flow's control via the three "fixed
facts" variables alone.

**Attempt 2** — added `HERDR_SOCKET_PATH=/home/li/.config/herdr/herdr.sock`.
Unit active, child PID 508552, store/sockets confirmed under scratch,
scratch list empty. Start A (fresh unique request id) sent: still
**`StartRejected.NativeLaunchRefused`**. A read-only manual check
(`herdr --session flow0174-test-8904b1 workspace list`, no
`HERDR_SOCKET_PATH`, plain shell) showed `HERDR_SOCKET_PATH` is irrelevant
to `--session <name>` resolution: it errored
`{"id":"cli:workspace:list","error":{"code":"server_not_running","message":"no herdr server is running at /home/li/.config/herdr/sessions/flow0174-test-8904b1/herdr.sock; run \`herdr session attach flow0174-test-8904b1\` to start or attach it"}}`,
naming the live config path, confirming session lookup is HOME-relative,
not `HERDR_SOCKET_PATH`-relative.

**Attempt 3** — added `XDG_CONFIG_HOME=/home/li/.config` (redirects
Herdr's own config/session-directory resolution to the live tree while
`HOME` stays scratch for Flow's store/sockets — confirmed read-only with
`herdr session list` under `HOME=<scratch> XDG_CONFIG_HOME=/home/li/.config`,
which correctly listed the three live sessions) and
`CLAUDE_CONFIG_DIR=/home/li/.claude` (so Flow's own transcript-reading
observer, not just the pane's own process, looks at the real Claude
project tree instead of `<scratch>/.claude`, which would otherwise never
receive a transcript and leave every Start permanently unobserved). Unit
active, child PID 511452, store/sockets confirmed under scratch, scratch
list empty. Start A (third fresh unique request id) sent: **still
`StartRejected.NativeLaunchRefused`**.

Read-only re-check with the corrected environment (`herdr --session
flow0174-test-8904b1 workspace list`) now correctly targets the live path
but returns the same refusal: **`no herdr server is running at
/home/li/.config/herdr/sessions/flow0174-test-8904b1/herdr.sock; run
\`herdr session attach flow0174-test-8904b1\` to start or attach it`**.

## 4. The blocker

Herdr 0.8.2's `workspace create`/`workspace list` (and, by the same
mechanism, `agent start`) refuse to run against a named `--session` that
has no server already running for it; only `herdr session attach <name>`
starts one, and `create_launch_pane` in `herdr/launch.rs` never calls
`session attach` — only `workspace create`. On this host, with this Herdr
version, **Flow 0.17.4's Start cannot bring a brand-new named Herdr
session into being by itself**; it can only add a workspace/pane to a
session that is already running. This seat's authority explicitly
forbids creating a Herdr session itself ("Create no Herdr session,
workspace, tab, or pane yourself"), so this was not worked around, per
the standing instruction to record a refusal in its exact words and not
route around it. It is not reached via a live-only quirk: the same
`server_not_running` shape reproduces on any never-attached session name
under a correctly pointed `XDG_CONFIG_HOME`.

## 5. Disclosure: the three-start budget was spent on this, not on A/B/C

Every one of this run's three permitted Start calls was sent against the
same intended case (A, two short lines), each with a fresh unique
`launch_request_id`, while chasing the environment fix above. None
reached anywhere past `NativeLaunchRefused` — none composed a native pane,
none produced a transcript, and the scratch store stayed at 0 rows after
all three (`Listed.[]`, checked after the third). By the letter of "no
retry of a start... no fourth start for any reason," this seat stops here:
**no Start B and no Start C were sent**, and no fourth attempt at A will
be made. This is a fault of this run's sequencing (diagnosing the Herdr
dependency should have been done read-only, before any Start was sent,
the same way the socket-length problem was caught read-only in stage
one) — recorded plainly rather than stretched to fit a pass.

## 6. Cleanup — item by item

- Scratch `flow-nexus` unit (`flow0174-scratch-1790484618.service`, the
  live one at the time of stopping): `systemctl --user stop` ->
  inactive/dead, `MainPID=0`; child PID 511452 confirmed gone
  (`kill -0` -> no such process). The two earlier scratch units
  (`...1790483655` no wait, `...1790484275` first attempt and
  `...1790484406` second attempt) were each stopped before starting the
  next, and their child PIDs (507055, 508552) were confirmed gone the
  same way, before the next unit was started.
- No Herdr session, workspace, tab, or pane was ever created for this
  test at any point — `herdr session list` before, between, and after all
  three attempts is byte-identical: `default`, `messaging-build`,
  `recovery-56ae53` only. Nothing to close.
- No Claude seat process, pane, or transcript exists to close — none was
  ever started (`NativeLaunchRefused` precedes any pane creation).
- No Herdr test session to close by name — none exists.
- Scratch service: stopped (above); its process gone.

## 7. Live baseline again (after), compared with step 1

Stable service: PID 1937 unchanged, 0 restarts, store hash
`f03f610a...c78c0f03` unchanged. Next service: PID 90750 unchanged, 0
restarts, store hash `ece72cc1...8d35e06e` unchanged. All four socket
mtimes unchanged. `flow 'List.{ }'` against the live stable socket:
byte-identical `Replaced.{ ... }` artifact both times (see §1). Herdr
`session list`: unchanged, no new session anywhere. `agent list`: still
10 agents, none new. Both live services are the same processes throughout
this seat's work; nothing outside the scratch directory changed.

## 8. What the test left outside the scratch root

Nothing. No transcript, no job directory, no Herdr record — because no
Start ever reached native-launch success. The scratch root
`/tmp/f74s2.Ym2hZI` is left in place for review, containing the empty
scratch store (0 rows) and the unused bundle file, per instruction not to
remove it.

## 9. Budget

Three Start RPCs sent, all rejected before any Claude process spawned;
no seat ran, so no seat-side time or token spend exists to weigh against
the per-start 3-minute/4-GiB bound. Total wall time for this seat's own
work: well under the 10-minute/100k-token combined bound for the three
starts (no model inference by a started seat occurred at all). This
seat's own token usage is outside that budget's scope (it bounds the
started seats, not the tester).

## 10. Refusals, exact words

- Flow, three times, identical: `StartRejected.NativeLaunchRefused`
- Herdr, read-only diagnostic, twice (before and after the
  `XDG_CONFIG_HOME` fix, path corrected the second time):
  `{"id":"cli:workspace:list","error":{"code":"server_not_running","message":"no herdr server is running at /home/li/.config/herdr/sessions/flow0174-test-8904b1/herdr.sock; run \`herdr session attach flow0174-test-8904b1\` to start or attach it"}}`

## What this does and does not show

Shows: Flow 0.17.4's Start, on this host, with Herdr 0.8.2 installed,
cannot originate a brand-new named Herdr session by itself; it depends on
that session already running. Composition itself was reached each time
(the rejection is `NativeLaunchRefused`, not `CompositionRefused`), so
the profile, skills, model, effort, and bundle fields were at least
accepted structurally each time — this is not itself evidence they were
composed correctly, since native launch never got far enough to produce
an inspectable pane or transcript.

Does not show: whether the plain-direct-form fix (the actual subject of
0.17.4) behaves correctly for case A, B, or C; whether the row would have
reached Started; whether the transcript would have shown the two-line
entry byte-exact with the line break kept; any of the model/effort/title/
skill-order findings the brief asked for. None of that could be produced.

## 11. Addendum — wind-down instruction from the main flow

Received mid-run: the stage-two time bound (from dispatch) was reached;
wind down, issue no further start. No start was in flight at that point —
cleanup (§6) was already complete. Answering the main flow's specific
question: every Herdr command in this run that named the test's session
(`flow0174-test-8904b1`) — the one `flow-nexus` issued internally on each
of the three rejected Starts, and the two manual read-only
`workspace list` diagnostics in §3 — **failed**, each with the same
`server_not_running` refusal (§10); none waited, and none brought a
session or server into being. Confirmed again just now:
`/home/li/.config/herdr/sessions/` holds only `messaging-build` and
`recovery-56ae53`; `herdr session list` shows the same three sessions as
before this run (`default`, `messaging-build`, `recovery-56ae53`) and
`herdr agent list` the same 10 agents. Live services unchanged (stable
PID 1937, next PID 90750, both 0 restarts, both store hashes identical to
§1/§7). No scratch systemd unit remains (`systemctl --user list-units
'flow0174-scratch-*'` empty). Nothing to close.

## Sources

- flows/8904b1/witnesses/flow-0174-fixture-and-baseline.md
- flows/8904b1/reports/flow-0174-three-live-start-witness-plan.md
- flows/8904b1/reports/flow-0174-semantic-review.md
- config/model-display-names.json
- /home/li/wt/flow-0174-independent-test-407811 at bc464e5e1b94fcc179af73111f43b69db1f69fc5
  (`crates/flow-nexus/src/{herdr.rs,herdr/launch.rs,composition.rs,store.rs}`)
- Direct commands: `systemd-run --user`, `systemctl --user`,
  `journalctl --user`, `ps`, `ss -xlp`, `stat`, `sha256sum`,
  `/proc/<pid>/{fd,environ}`, `herdr session list`, `herdr --session
  <name> workspace list` (read-only diagnostic only), `flow 'List.{ }'`,
  `flow 'Start.{ ... }'` (three times, case A only).
