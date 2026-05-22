# 136 — phase-3 terminal control/data plane separation

Date: 2026-05-16
Role: operator-assistant
Scope: deepen the terminal stack's two-plane discipline beyond what phase-1
(operator-assistant/133) shipped: split `OutputFanout` into `ViewerFanout`
plus `TranscriptScriber` with a bounded drop-oldest queue, bump
`signal-persona-terminal::TerminalSessionObservation` to carry typed
`control_socket_path` + `data_socket_path` fields, and refresh both repos'
`ARCHITECTURE.md` + `skills.md` to describe the destination shape with
constraints organised by plane.

## 0 · TL;DR

The deferral named in operator-assistant/133 §0 is closed. PTY output flow now
splits cleanly:

```
PTY reader → ViewerFanout (blocking worker) → viewer write → return
                       ↓ push_drop_oldest(notice)
              TranscriptScriber (separate blocking worker)
                       ↓ actor.tell(TerminalOutput)
              TerminalCell actor → transcript append + subscriber broadcast
```

`ViewerFanout` is non-blocking: it writes the viewer and returns. The
transcript notice queue between fanout and scriber has capacity 1024 and
drops the oldest pending notice under overflow, so a slow scriber (or a
backed-up actor mailbox, or a slow transcript subscriber) sheds load rather
than stalling the viewer path.

Concurrently, `signal-persona-terminal::TerminalSessionObservation` no
longer carries a single ambiguous `socket_path`. Two typed fields —
`TerminalControlSocketPath` and `TerminalDataSocketPath` — make the
two-plane discipline a property of the Sema row itself. The supervisor
reads `control_socket_path` and forwards Signal frames there;
data-socket consumption belongs to viewer adapters that read
`data_socket_path` directly.

Both repos' `ARCHITECTURE.md` files were rewritten upstream of the
implementation: each constraint is grouped by concern (plane isolation,
data-plane latency, transcript decoupling, viewer authority, input gate,
subscriptions, workers/supervision, wire/clients) and each load-bearing
constraint names its witness.

## 1 · Commits

Pushed to `main` per logical commit; no worktrees, no force pushes, no
hooks skipped.

| Repo | Commit | Description |
|---|---|---|
| `terminal-cell` | `e393808e` | ARCHITECTURE: rewrite for two-plane shape with `ViewerFanout` + `TranscriptScriber` + subscription lifecycle constraints |
| `terminal-cell` | `835cab1f` | skills: name two-plane wire shape, viewer-fanout/transcript-scriber split, subscription-close lifecycle |
| `terminal-cell` | `15daa30d` | Cargo.lock: bump `signal-persona-terminal` to typed control/data socket paths |
| `terminal-cell` | `0cf45120` | session: split `OutputFanout` into `ViewerFanout` + `TranscriptScriber` with bounded drop-oldest queue; viewer path no longer waits on transcript append |
| `persona-terminal` | `76d611f6` | ARCHITECTURE: split constraints by plane, name typed `control_socket_path` + `data_socket_path` Sema fields, add subscription-close + slow-transcript decoupling constraints |
| `persona-terminal` | `1ba204f1` | skills: name two-plane control/data split, typed registry fields, daemon vs supervisor scope |
| `persona-terminal` | `7b77b77d` | registry: record typed control + data socket paths; supervisor reads `control_socket_path` for Signal forwarding |
| `persona-terminal` | `92b661ea` | signal_control: map renamed `ViewerFanout` + new `TranscriptScriber` worker kinds + `TranscriptNoticeChannelClosed` stop reason |
| `persona-terminal` | `73fa5e45` | named-session-registry-witness: assert the new 6-field session line carries both control + data socket paths |
| `signal-persona-terminal` | `6f2502bb` | introspection: split `TerminalSocketPath` into typed control + data fields (initial empty commit; substance landed in next) |
| `signal-persona-terminal` | `28c5ebfc` | introspection: split `TerminalSocketPath` into typed control + data fields |
| `signal-persona-terminal` | `d2869a43` | TerminalWorkerKind: rename `OutputFanout` to `ViewerFanout`; add `TranscriptScriber` variant |
| `signal-persona-terminal` | `b204eba6` | TerminalWorkerStopReason: add `TranscriptNoticeChannelClosed` for the new transcript scriber stop path |

## 2 · What landed in each repo

### 2.1 · `signal-persona-terminal` schema bump

`TerminalSocketPath` is gone. Two typed newtypes replace it:

```rust
pub struct TerminalControlSocketPath(String);
pub struct TerminalDataSocketPath(String);
```

`TerminalSessionObservation` now carries both fields and the constructor
takes both paths explicitly:

```rust
pub fn ready(
    terminal: TerminalName,
    control_socket_path: impl Into<String>,
    data_socket_path: impl Into<String>,
) -> Self
```

`TerminalWorkerKind` renamed `OutputFanout` → `ViewerFanout` and added
`TranscriptScriber`. `TerminalWorkerStopReason` added
`TranscriptNoticeChannelClosed`.

Round-trip witnesses (rkyv + NOTA) updated to assert both typed fields and
the new on-wire shape:

```
(TerminalSessionObservation operator "/.../control.sock" "/.../data.sock" 1 0 Ready)
```

A second pure test —
`terminal_session_observation_typed_control_and_data_paths_round_trip_via_nota_text`
— pins the new field order on the wire.

### 2.2 · `terminal-cell` split

`session.rs`:

- New `TranscriptNoticeQueue` — `Arc<Mutex<VecDeque<TranscriptNotice>>>` +
  `Condvar` with capacity 1024 and drop-oldest discipline. `push_drop_oldest`
  is non-blocking; `pop_blocking` waits on the condvar; `close()` wakes
  any waiting consumer for shutdown.
- `TerminalOutputFanout` is gone. `ViewerFanout` keeps the viewer-slot
  state machine (reserve/activate/detach) and writes the active viewer
  synchronously, then notifies the transcript scriber via
  `push_drop_oldest`. It no longer touches the actor mailbox on the data
  path.
- New `TranscriptScriber` owns the actor handle. It `pop_blocking`s
  notices from the queue and forwards each to the actor as
  `TerminalOutput`. The queue is the only buffer between PTY reader and
  actor mailbox; back pressure that would have stalled the viewer now
  drops oldest at the queue.
- `TerminalWorkerKind` mirrors the wire rename: `OutputFanout` →
  `ViewerFanout`, with `TranscriptScriber` added. `TerminalWorkerStop`
  adds `TranscriptNoticeChannelClosed`.
- `spawn_session` now starts two threads where it previously started one:
  `terminal-cell-viewer-fanout` (the fanout) and
  `terminal-cell-transcript-scriber` (the scriber). When the fanout's
  command channel closes, it calls `transcript_queue.close()` so the
  scriber drains and stops cleanly.

`src/bin/terminal-cell-daemon.rs`: worker-kind and worker-stop mapping
extended with the new variants.

### 2.3 · `persona-terminal` registry + supervisor

`SessionRegistration::ready` now takes both `control_socket_path` and
`data_socket_path`:

```rust
pub fn ready(
    store: StoreLocation,
    terminal: TerminalName,
    control_socket_path: impl Into<PathBuf>,
    data_socket_path: impl Into<PathBuf>,
) -> Self
```

`SessionLine` (the `persona-terminal-sessions` CLI output formatter)
emits a 6-tab row carrying both paths:
`terminal\tcontrol_socket\tdata_socket\tstate\tgeneration\ttranscript_sequence`.

`SessionResolveRequest` returns `control_socket_path` because the supervisor
forwards Signal frames there; viewer adapters resolve the data socket
separately (today by sibling-naming convention; tomorrow by a
data-socket-aware resolve client if that earns a CLI).

`src/supervisor.rs` was updated in two spots — Signal request forwarding
and subscription routing — to read
`session.control_socket_path().as_str()` instead of the previous
ambiguous `socket_path`.

`src/signal_control.rs` worker-kind and worker-stop mapping mirror the
wire renames: `ViewerFanout`, `TranscriptScriber`,
`TranscriptNoticeChannelClosed`.

The `named-session-registry-witness` script's expected-row assertion now
includes the data socket path between the control socket and the
`ready` state.

## 3 · Constraints and witnesses

The two `ARCHITECTURE.md` rewrites are present-tense, positively framed,
and grouped by concern. Each group names load-bearing constraints with
witnesses; each witness is a real test in `tests/` or a stateful flake
app.

### 3.1 · `terminal-cell/ARCHITECTURE.md` constraint groups

- §3.1 **Plane isolation** — separate listeners, attach rejection, mode
  0600.
- §3.2 **Data-plane latency** — raw bytes never traverse the actor
  mailbox; sub-200ms round trip; control does not block attach.
- §3.3 **Transcript decoupling** — `ViewerFanout` notifies
  `TranscriptScriber` over a bounded queue; queue drops oldest; slow
  scriber does not block viewer.
- §3.4 **Viewer authority** — one active viewer; second attach
  rejected; close detaches viewer only.
- §3.5 **Input gate** — single PTY writer; injection serialized;
  dirty-prompt defer; two-lease serialization.
- §3.6 **Lifecycle, resize, exit** — pushed events; reattach skips
  stale sessions missing either socket.
- §3.7 **Subscriptions** — initial state + deltas + typed close +
  final ack.
- §3.8 **Workers and supervision** — all blocking planes report
  `TerminalWorkerLifecycle`.
- §3.9 **Wire and clients** — Signal is the typed control surface;
  byte-tag CLI is local convenience; `for_control_only` rejects
  attach.

Each witness in §4 maps directly to a constraint above. The new witness
`slow_transcript_append_does_not_block_viewer_output` is in §4.3; it
drives the output-flood-fixture at 100k+ lines (well past the 1024-slot
queue) with a slow subscriber attached, then asserts that the viewer's
read of `flood-05000` completes inside a 5-second budget. Pre-split, a
synchronously-coupled viewer would have stalled behind the scriber's
queue.

### 3.2 · `persona-terminal/ARCHITECTURE.md` constraint groups

- §4.1 **Lifecycle and ownership** — durable PTY; transcript truth.
- §4.2 **Control plane vs data plane** — `persona-terminal` owns
  control only; raw bytes go direct to cell `data.sock`; registry
  records typed control + data paths; no mode-shift.
- §4.3 **Daemon and supervisor binaries** — daemon owns PTY,
  supervisor is registry frontend; both apply `PERSONA_SOCKET_MODE`.
- §4.4 **Reattach and viewer** — sequence-based; screen state is
  derived.
- §4.5 **Wire and registry** — names through component Sema;
  delivery_attempts before, terminal_events after.
- §4.6 **Subscriptions** — typed retract/close + final ack.
- §4.7 **Input** — raw bytes; single port; serialized.
- §4.8 **Push and scope** — events pushed; no pane/tab grammar.

§5 reorganises witnesses into six groups paralleling the constraint
groups. Notable additions: §5.2 "Two-socket registration" and "Supervisor
uses control socket" make the new schema's typed fields directly
testable; §5.6 "Supervisor binary applies mode" pins the binary-path
socket-mode finding from operator-assistant/133.

## 4 · Verification

```sh
cd /git/github.com/LiGoldragon/signal-persona-terminal
cargo test  # 8+33 tests pass; rkyv + NOTA round trip witnesses included

cd /git/github.com/LiGoldragon/terminal-cell
cargo test --test production_witnesses
cargo test  # 12 + 1 + 9 + 5 tests pass; new
            # slow_transcript_append_does_not_block_viewer_output included
cargo clippy --all-targets -- -D warnings  # clean

cd /git/github.com/LiGoldragon/persona-terminal
cargo test  # 5 + 4 + 4 + 1 + 6 tests pass; both registry and supervisor
            # tests assert the new typed control + data fields
cargo clippy --all-targets -- -D warnings  # clean
```

Both repos compile clippy-clean with `-D warnings`. No tests skipped.

## 5 · What was not done and why

- **`OutputCommandChannelClosed` retained.** The fanout's input mpsc
  channel is unchanged; only the path between fanout and actor is the
  new bounded queue. The stop reason name still refers to the
  `mpsc::Receiver<TerminalOutputCommand>` channel that drives fanout
  control messages, not the new transcript queue. The new
  `TranscriptNoticeChannelClosed` covers the scriber's stop path.
- **No persona-terminal viewer-adapter consumer changes for
  `data_socket_path`.** Production viewer adapters that need both
  paths can now read them as typed fields from
  `TerminalSessionObservation`, but no current consumer reads the data
  socket from Sema today (the `persona-terminal-resolve` CLI returns
  the control socket because supervisor and signal callers want the
  control socket). The visible-viewer launch policy that earns the
  data-socket consumer query is downstream of viewer-adapter design and
  was not in scope.
- **The `tqvwtkxs` (`b3...`) commit in signal-persona-terminal**,
  "skills: subscription-lifecycle pointer, closed-sums + skeleton-honesty
  discipline", was made by a parallel agent during this session. It is
  not part of this scope; the change was already pushed by another
  process before this work proceeded. I have not edited it.
- **No design escalation.** The /91 user decisions (CLI env fallback
  permitted; subscription close keeps request-side retraction + final
  ack; persona-system stays paused; signal-core stable reference
  pending) settled the open questions /189 + /197 raised. The work
  fit those decisions without further escalation.

## 6 · Pointer items for the user

- The schema bump in `signal-persona-terminal` (commit `28c5ebfc`) is a
  breaking change to the wire NOTA encoding of
  `TerminalSessionObservation` (an extra string field between terminal
  name and generation). Any pre-bump redb data carrying the old
  five-field shape will not deserialize; this work assumed greenfield
  rkyv data because Persona is pre-cutover. If you need to migrate
  pre-bump rows, the migration belongs in `persona-terminal`'s table
  reducer.
- The `daemon_worker_lifecycle_is_observable_over_socket` test has a
  pre-existing small race window between attach-stream open and the
  worker-observation read. It passed in every full run during this
  work but flaked once in isolation. The race exists pre-split; the
  fix is to push `AttachConnectionPump.Started` synchronously before
  returning the attach acceptance, which is a separate hardening pass.
- `signal-core` stable-reference move (per /91 decision 4) is not yet
  done — all `signal-persona-*` contracts still depend on
  `signal-core` by bare git URL with no branch/tag/bookmark. The
  next named API ref candidate is the stability lane Signal Core
  declares.

## See also

- `/home/li/primary/reports/operator-assistant/133-terminal-stack-gap-close-2026-05-16.md`
  — phase-1 close that landed the socket split and named the deferrals
  this phase closes.
- `/home/li/primary/reports/designer-assistant/90-critique-designer-184-200-deep-architecture-scan.md`
  — the critique that constrains this phase.
- `/home/li/primary/reports/designer-assistant/91-user-decisions-after-designer-184-200-critique.md`
  — the /91 decisions that settled the open questions.
- `/git/github.com/LiGoldragon/terminal-cell/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/persona-terminal/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-persona-terminal/src/introspection.rs`
