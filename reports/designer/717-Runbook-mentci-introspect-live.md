# 717 — LIVE-RUN RUNBOOK: real spirit trace into introspect (and the mentci gap)

A copy-pasteable runbook that stands up a FRESH, trace-enabled introspect +
spirit pair on temp sockets/stores, drives REAL spirit Signal/Nexus/SEMA
actor-boundary activity, and reads the captured `ComponentTrace` back. Every
mechanism is cited to source `file:line` on the `trace-introspect-slice`
worktrees.

## What is real and what is not (read first)

The task framed three legs: (1) launch a trace-enabled introspect, (2) launch a
trace-enabled spirit whose sink targets introspect, (3) view it in mentci. Legs
1 and 2 are fully real and exercised by tests. Leg 3 — viewing in mentci-egui —
does NOT exist in source yet. Findings:

- The **introspect daemon** ingests pushed `ComponentTraceEvent` frames over a
  Unix trace socket and answers a `ComponentTrace` query. Real and tested:
  `introspect/.../tests/component_trace.rs:82` (end-to-end push → ingest →
  query) and `tests/daemon.rs:43` (real `introspect-daemon` process from a
  binary rkyv config).
- The **spirit daemon** under `--features testing-trace` pushes the SHARED
  `signal_introspect::ComponentTraceEvent` to its configured `trace_socket_path`.
  Real and tested: `spirit/.../tests/process_boundary.rs:1415`
  (`cli_receives_testing_trace_events_from_daemon_trace_socket`) and
  `tests/instrumentation_logging.rs:62` (the exact Signal/Nexus/SEMA event
  sequence a Record then Observe produce).
- **mentci-egui has NO introspect client.** Verified across every branch
  (`main`, `criome-mentci-bootstrap`, `gui-system-theme`): zero hits for
  `introspect`, `ComponentTrace`, or `MENTCI_INTROSPECT_SOCKET`. The checked-out
  worktree `mentci-egui/re-found-on-live-contracts/src/daemon_client.rs:211`
  reads only `MENTCI_SOCKET` / `MENTCI_META_SOCKET` and speaks `signal-mentci`
  to `mentci-daemon`. There is no `trace-introspect-slice` branch for
  mentci-egui or mentci-lib. So "view it in mentci-egui's introspect panel" is
  not yet buildable. Step 9 gives the closest REAL alternative.
- **The introspect CLI cannot issue a ComponentTrace query.** Its surface input
  enum has exactly one variant — `Input::PrototypeWitness` — and
  `Input::into_request` maps only that
  (`introspect/.../src/surface.rs:24`, `src/command.rs:103`). So a `ComponentTrace`
  read must go through a tiny witness binary (Step 8) or the test harness
  (Step 8b), using the real `introspect::daemon::IntrospectionSignalClient`.

## Trace direction (the load-bearing wiring fact)

`triad_runtime::trace` is connect-per-event push to a bound listener:

- PUSHER: `TraceLog::socket(path)` →`record` → `TraceSocketPath::write_event`
  does `UnixStream::connect(path)` for each event
  (`triad-runtime/src/trace.rs:152,176,190`).
- LISTENER: `TraceSocketListener::bind(path)` binds + accepts
  (`triad-runtime/src/trace.rs:203`).

Therefore **introspect binds the trace socket** (`ComponentTraceListener::on_start`
→ `TraceSocketListener::bind`, `introspect/.../src/runtime.rs:604,613`) and
**spirit-daemon connects to it**. The spirit-daemon's config `trace_socket_path`
MUST equal introspect's config `trace_socket_path`.

Do NOT set `SPIRIT_TRACE_SOCKET` on the spirit CLI in this runbook: that env
makes the CLI itself BIND the socket as a listener
(`spirit/.../src/bin/spirit.rs:40` → `TraceClient::from_environment` →
`TraceSocketListener::bind`), which would collide with introspect's bind on the
same path. The CLI's trace env is for spirit's own in-test capture, not for the
introspect path.

## Two facts that determine the ComponentTrace query parameters

1. **engine identity = the spirit daemon's socket path string.** spirit stamps
   every pushed event with `EngineIdentifier::new(configuration.socket_path()
   .to_string_lossy())` (`spirit/.../src/daemon.rs:116`). The query's `engine`
   must be that exact path string.
2. **component is ALWAYS `Signal`.** `impl From<TraceEvent> for
   ComponentTraceEvent` hardcodes `IntrospectionTarget::Signal` for every event
   regardless of Signal/Nexus/SEMA layer
   (`spirit/.../src/trace_event.rs:76-89`); only the `layer` field varies. So the
   query uses `IntrospectionTarget::Signal` and gets the whole stream back.
   (`matches_query` filters on engine + component + optional event_name:
   `signal-introspect/.../src/lib.rs` `ComponentTraceEvent::matches_query`.)

## Production safety

The deployed `spirit-daemon.service` runs spirit 0.16.0 built WITHOUT
`testing-trace` (`#[cfg(not(feature = "testing-trace"))]` build path,
`spirit/.../src/daemon.rs:126`), so it has no trace sink and is untouched by
this runbook. Everything below uses fresh temp sockets/stores under one
throwaway directory and freshly-built worktree binaries. Never point any config
path at `/run/persona/...`, `/var/lib/persona/...`, or the production socket.

## Paths and binaries used

| Role | Worktree | Branch |
|---|---|---|
| introspect daemon + CLI | `/home/li/wt/github.com/LiGoldragon/introspect/trace-introspect-slice` | `trace-introspect-slice` (`introspect/.../Cargo.toml:24` bin `introspect-daemon`) |
| spirit daemon, CLI, write-configuration | `/home/li/wt/github.com/LiGoldragon/spirit/trace-introspect-slice` | `trace-introspect-slice` (`spirit/.../Cargo.toml:25,29` bins) |

Both depend on `triad-runtime` git `main` (`introspect/.../Cargo.toml:40`,
`spirit/.../Cargo.toml:171`), and both pull `signal-introspect` on
`trace-introspect-slice` so the wire `ComponentTraceEvent` type is identical at
both ends.

## Runbook (ordered steps)

Every command uses absolute paths; nothing is path-scoped to the cwd. Run
foreground daemons in separate terminals or with `&`.

### Step 0 — one throwaway run directory

```bash
export RUN=$(mktemp -d /tmp/spirit-trace-live.XXXXXX)
echo "$RUN"
```

Expected: prints a fresh dir like `/tmp/spirit-trace-live.ab12cd`. All sockets
and stores live here; nothing touches production paths.

### Step 1 — build the trace-enabled introspect daemon

```bash
cargo build --manifest-path \
  /home/li/wt/github.com/LiGoldragon/introspect/trace-introspect-slice/Cargo.toml \
  --bin introspect-daemon
```

Expected: `Finished dev [unoptimized + debuginfo] target(s)`. Binary at
`/home/li/wt/github.com/LiGoldragon/introspect/trace-introspect-slice/target/debug/introspect-daemon`.
Introspect has no Cargo feature flags — its trace listener is always present and
binds only when `trace_socket_path` is non-empty
(`introspect/.../src/daemon.rs:153,160`, `runtime.rs:78,608`).

### Step 2 — build the trace-enabled spirit daemon, CLI, and config writer

The spirit-daemon trace sink is gated behind `testing-trace`; the CLI and
config writer need `nota-text` (`spirit/.../Cargo.toml:18,31,83`). Build all
three with both features so binaries land in one target dir:

```bash
cargo build --manifest-path \
  /home/li/wt/github.com/LiGoldragon/spirit/trace-introspect-slice/Cargo.toml \
  --features testing-trace,nota-text \
  --bin spirit-daemon --bin spirit --bin spirit-write-configuration
```

Expected: `Finished`. Binaries under
`/home/li/wt/github.com/LiGoldragon/spirit/trace-introspect-slice/target/debug/`:
`spirit-daemon`, `spirit`, `spirit-write-configuration`. The `spirit-daemon`
must be the `testing-trace` build — the pre-existing target-dir binary may be a
default (no-trace) build, so this rebuild is mandatory, not optional.

### Step 3 — encode introspect's rkyv startup config (GAP: no encode bin)

GAP: introspect ships NO `*-write-configuration` / `*-encode-configuration`
binary (`introspect/.../Cargo.toml` declares only `introspect`,
`meta-introspect`, `introspect-daemon`). The daemon needs ONE pre-generated rkyv
file as its single argv (it rejects inline NOTA and `.nota` paths:
`introspect/.../src/schema/daemon.rs:87-99`, and `IntrospectDaemonConfiguration`
encodes via `to_rkyv_bytes()` `signal-introspect/.../src/lib.rs:945`).

Closest real alternative: a tiny throwaway witness binary that builds the typed
config and writes its rkyv bytes — the exact shape `tests/daemon.rs:258-300`
uses (`write_configuration` + `daemon_configuration`). Create a scratch crate:

```bash
mkdir -p "$RUN/introspect-encode/src"
cat > "$RUN/introspect-encode/Cargo.toml" <<EOF
[package]
name = "introspect-encode"
version = "0.0.0"
edition = "2021"

[dependencies]
signal-introspect = { git = "https://github.com/LiGoldragon/signal-introspect.git", branch = "trace-introspect-slice" }
signal-persona = { git = "https://github.com/LiGoldragon/signal-persona.git", branch = "main" }
EOF
cat > "$RUN/introspect-encode/src/main.rs" <<'EOF'
// One pre-generated rkyv IntrospectDaemonConfiguration written to argv[6].
// argv: <introspect_sock> <supervision_sock> <store> <trace_sock> <uid> <out.rkyv>
use signal_introspect::{IntrospectDaemonConfiguration, SocketMode, WirePath};
use signal_persona::{OwnerIdentity, UnixUserIdentifier};
fn main() {
    let a: Vec<String> = std::env::args().collect();
    let config = IntrospectDaemonConfiguration {
        introspect_socket_path: WirePath::new(a[1].clone()),
        introspect_socket_mode: SocketMode::new(0o600),
        supervision_socket_path: WirePath::new(a[2].clone()),
        supervision_socket_mode: SocketMode::new(0o600),
        store_path: WirePath::new(a[3].clone()),
        manager_socket_path: WirePath::new(String::new()),
        router_socket_path: WirePath::new(String::new()),
        terminal_socket_path: WirePath::new(String::new()),
        trace_socket_path: WirePath::new(a[4].clone()),
        owner_identity: OwnerIdentity::UnixUser(UnixUserIdentifier::new(a[5].parse().unwrap())),
    };
    std::fs::write(&a[6], config.to_rkyv_bytes().expect("rkyv encode")).expect("write");
    println!("wrote {}", a[6]);
}
EOF
cargo build --manifest-path "$RUN/introspect-encode/Cargo.toml"
"$RUN/introspect-encode/target/debug/introspect-encode" \
  "$RUN/introspect.sock" \
  "$RUN/introspect-supervision.sock" \
  "$RUN/introspect.sema" \
  "$RUN/introspect-trace.sock" \
  "$(id -u)" \
  "$RUN/introspect-daemon.rkyv"
```

Expected: `wrote /tmp/.../introspect-daemon.rkyv`, and the file exists. Empty
`manager/router/terminal` paths mean "no peer configured"
(`introspect/.../src/daemon.rs:158-166`). The config struct/field order is fixed
at `signal-introspect/.../src/lib.rs:911-935`; the canonical NOTA form is
witnessed at `signal-introspect/.../tests/round_trip.rs:364-391`.

Note: the daemon arg file must EXIST on disk and NOT end in `.nota`, or
`ComponentCommand` mis-classifies it (`triad-runtime/src/argument.rs:91,201`).
`.rkyv` is fine.

### Step 4 — launch the introspect daemon (binds the trace socket)

```bash
/home/li/wt/github.com/LiGoldragon/introspect/trace-introspect-slice/target/debug/introspect-daemon \
  "$RUN/introspect-daemon.rkyv" &
```

Then confirm both the query socket and the trace socket are bound:

```bash
until [ -S "$RUN/introspect.sock" ] && [ -S "$RUN/introspect-trace.sock" ]; do sleep 0.1; done
ls -l "$RUN/introspect.sock" "$RUN/introspect-trace.sock"
```

Expected: both appear as sockets (`srwx------`). The query socket is bound by the
emitted daemon shell (`introspect/.../src/daemon.rs:174` `socket_path`); the
trace socket is bound by `ComponentTraceListener::on_start`
(`introspect/.../src/runtime.rs:608-620`). The daemon takes EXACTLY one argv (the
rkyv path) — no flags (`src/schema/daemon.rs:101-108`, single-arg enforced at
`argument.rs:102-107`).

### Step 5 — encode spirit's rkyv startup config (pointed at introspect's trace socket)

Use spirit's real config writer. The trace socket is the optional 4th positional
field of `ConfigurationWriteRequest`
(`spirit/.../src/bin/spirit-write-configuration.rs:30-38`); the NOTA record shape
matches `tests/process_boundary.rs:215-221`
`(ConfigurationWriteRequest (<sock> (Some <meta>) <db> (Some <trace>) None <out>))`:

```bash
/home/li/wt/github.com/LiGoldragon/spirit/trace-introspect-slice/target/debug/spirit-write-configuration \
  "(ConfigurationWriteRequest ($RUN/spirit.sock (Some $RUN/spirit-meta.sock) $RUN/spirit.sema (Some $RUN/introspect-trace.sock) None $RUN/spirit-daemon.rkyv))"
```

Expected stdout: `(ConfigurationWritten $RUN/spirit-daemon.rkyv)` (the writer
prints the typed `ConfigurationWriteOutput`,
`spirit-write-configuration.rs:69-72,85`). The trace field points at
introspect's bound trace socket from Step 3/4 — this is the line that wires
spirit's sink to introspect.

The paths contain no spaces, so bare NOTA atoms are correct (no quoting). The
guardian-agent slot is `None` (5th field) — fine because the daemon is built
without `agent-guardian` here, so it never requires a guardian
(`spirit/.../src/daemon.rs:131-140` is `#[cfg(feature = "agent-guardian")]`).

### Step 6 — launch the trace-enabled spirit daemon (pushes to introspect)

```bash
/home/li/wt/github.com/LiGoldragon/spirit/trace-introspect-slice/target/debug/spirit-daemon \
  "$RUN/spirit-daemon.rkyv" &
until [ -S "$RUN/spirit.sock" ] && [ -S "$RUN/spirit-meta.sock" ]; do sleep 0.1; done
ls -l "$RUN/spirit.sock"
```

Expected: `spirit.sock` and `spirit-meta.sock` appear. The daemon's
`build_runtime` (`testing-trace` arm, `spirit/.../src/daemon.rs:110-125`) opens
the store with a `TraceLog::socket(engine_identity, "$RUN/introspect-trace.sock")`
sink, stamping events with engine id = `"$RUN/spirit.sock"`. The daemon takes
exactly one argv (the rkyv config); it does NOT parse NOTA.

### Step 7 — drive REAL spirit activity (Record, then Observe)

The spirit CLI takes one NOTA arg and reads `SPIRIT_SOCKET`
(`spirit/.../src/bin/spirit.rs:38`). Do NOT set `SPIRIT_TRACE_SOCKET` (see the
trace-direction note above).

Record one entry (real Signal admission + Nexus loop + SEMA write):

```bash
SPIRIT_SOCKET="$RUN/spirit.sock" \
/home/li/wt/github.com/LiGoldragon/spirit/trace-introspect-slice/target/debug/spirit \
  "(Record (([(Information Documentation)] Constraint [trace crosses daemon boundary] Maximum Minimum Zero []) ([([trace crosses daemon boundary] None)] [trace crosses daemon boundary])))"
```

Expected stdout: `(RecordAccepted <id>)` with a 4-7 char lower-base36 id
(record-request shape from `tests/process_boundary.rs:418-422`; reply variant
asserted at `:578,605`). This single Record pushes this exact event sequence to
introspect (`tests/instrumentation_logging.rs:93-117`,
`process_boundary.rs:1444-1455`):
`SignalAdmitted, SignalTriaged, NexusEntered, NexusDecided, NexusEntered,
NexusDecided, SemaWriteApplied, NexusEntered, NexusDecided, SignalReplied`
(plus a possible one-time lifecycle prefix `SemaStarted, NexusStarted,
SignalStarted` on the daemon's first request).

Then Observe (real SEMA read):

```bash
SPIRIT_SOCKET="$RUN/spirit.sock" \
/home/li/wt/github.com/LiGoldragon/spirit/trace-introspect-slice/target/debug/spirit \
  "(Observe ((Full [(Information Documentation)]) Any Any Any (Some Constraint) (Exact Zero) (AtLeastCertainty Minimum) Any))"
```

Expected stdout: `(RecordsStashed ...)` (Observe stashes and returns records,
`process_boundary.rs:619-622`). This pushes
`SignalAdmitted, SignalTriaged, NexusEntered, NexusDecided, SemaReadObserved,
NexusEntered, NexusDecided, NexusEntered, NexusDecided, SignalReplied`
(`instrumentation_logging.rs:106-116`, `process_boundary.rs:1471-1482`).

introspect's `ComponentTraceListener::drain` loop continuously accepts and
forwards each pushed frame to its store as a `RecordComponentTraceEvent`
(`introspect/.../src/runtime.rs:577-598`); ingestion is async, so the query in
Step 8 is the observation point.

### Step 8 — read the captured trace back (GAP: no CLI/mentci path; witness binary)

GAP: neither the introspect CLI (only `PrototypeWitness`,
`introspect/.../src/surface.rs:24`) nor mentci-egui (no introspect client) can
issue a `ComponentTrace` query. Closest real path: a tiny witness binary using
the real `introspect::daemon::IntrospectionSignalClient` (exported at
`introspect/.../src/lib.rs`, client at `src/daemon.rs:395-447`) against the
query socket. It mirrors `tests/component_trace.rs:46-61` but over the process
socket.

```bash
mkdir -p "$RUN/trace-witness/src"
cat > "$RUN/trace-witness/Cargo.toml" <<EOF
[package]
name = "trace-witness"
version = "0.0.0"
edition = "2021"

[dependencies]
introspect = { path = "/home/li/wt/github.com/LiGoldragon/introspect/trace-introspect-slice" }
signal-introspect = { git = "https://github.com/LiGoldragon/signal-introspect.git", branch = "trace-introspect-slice" }
signal-persona = { git = "https://github.com/LiGoldragon/signal-persona.git", branch = "main" }
EOF
cat > "$RUN/trace-witness/src/main.rs" <<'EOF'
// argv: <introspect_query_sock> <engine_identity = spirit_sock_path>
use introspect::daemon::IntrospectionSignalClient;
use signal_introspect::{ComponentTraceQuery, IntrospectionRequest, IntrospectionReply,
    IntrospectionTarget};
use signal_persona::EngineIdentifier;
fn main() {
    let a: Vec<String> = std::env::args().collect();
    let query = ComponentTraceQuery::new(
        EngineIdentifier::new(a[2].clone()),
        IntrospectionTarget::Signal, // spirit stamps every event as Signal
        None,                        // None = whole stream for this engine
    );
    let reply = IntrospectionSignalClient::new(a[1].clone())
        .submit(IntrospectionRequest::ComponentTrace(query))
        .expect("introspect replies");
    match reply {
        IntrospectionReply::ComponentTrace(trace) => {
            for e in trace.events() {
                println!("seq {:>3}  {:?}  {}", e.sequence.value(), e.layer, e.event_name.as_str());
            }
            println!("total events: {}", trace.events().len());
        }
        other => panic!("expected ComponentTrace, got {other:?}"),
    }
}
EOF
cargo build --manifest-path "$RUN/trace-witness/Cargo.toml"
"$RUN/trace-witness/target/debug/trace-witness" "$RUN/introspect.sock" "$RUN/spirit.sock"
```

Expected: the captured events in monotonic sequence, e.g.

```
seq   0  Signal  SignalAdmitted
seq   1  Signal  SignalTriaged
seq   2  Nexus   NexusEntered
seq   3  Nexus   NexusDecided
...
seq   6  Sema    SemaWriteApplied
...
total events: 20+
```

The query's `engine` MUST be the spirit socket path string `"$RUN/spirit.sock"`
(`spirit/.../src/daemon.rs:116`) and `component` MUST be `Signal`
(`spirit/.../src/trace_event.rs:79`); otherwise `matches_query` filters
everything out and you get `total events: 0`. To narrow to one event name, pass
`Some(TraceEventName::new("SemaWriteApplied"))` as the third arg
(`signal-introspect/.../src/lib.rs` `ComponentTraceQuery`, filter proven at
`tests/component_trace.rs:146-155`).

If ingestion lags, re-run the witness (the drain loop is asynchronous;
`tests/component_trace.rs:67-80` polls for the same reason).

### Step 8b — alternative read: run the in-process slice test verbatim

If building a scratch crate is unwelcome, the same push → ingest → query path is
the shipped test. It does not use the live daemon process but proves the exact
mechanism end to end with assertions:

```bash
cargo test --manifest-path \
  /home/li/wt/github.com/LiGoldragon/introspect/trace-introspect-slice/Cargo.toml \
  --test component_trace -- --nocapture
```

Expected: `test pushed_signal_trace_events_are_ingested_and_queryable_by_component_and_name ... ok`.

And the cross-process spirit→socket leg (CLI is the listener there, not
introspect, but it proves the daemon's push):

```bash
cargo test --manifest-path \
  /home/li/wt/github.com/LiGoldragon/spirit/trace-introspect-slice/Cargo.toml \
  --features testing-trace,nota-text \
  --test process_boundary cli_receives_testing_trace_events -- --nocapture
```

Expected: `... cli_receives_testing_trace_events_from_daemon_trace_socket ... ok`.

### Step 9 — viewing in mentci (GAP: not implemented; what would be needed)

GAP: there is no mentci-egui introspect panel and no `MENTCI_INTROSPECT_SOCKET`
env. mentci-egui's only client is `signal-mentci` to `mentci-daemon`
(`mentci-egui/.../src/daemon_client.rs:4,211-224`). To "view it in mentci" as
the task envisions, mentci-egui would need a new `IntrospectClient` (an
`IntrospectionSignalClient` against `$RUN/introspect.sock`) plus a panel that
issues the `ComponentTrace` query and renders `ComponentTrace.events()` — i.e.
the Step 8 witness logic moved into an egui view, gated on a new
`MENTCI_INTROSPECT_SOCKET` env. Until that lands, Step 8 (witness binary) or
Step 8b (the slice test) is the real read path. The trace-introspect-slice work
(report 716) deliberately scoped the introspect ingest/query contract first and
left the mentci view for a later increment.

### Step 10 — teardown

```bash
kill %1 %2 2>/dev/null   # spirit-daemon and introspect-daemon (adjust job nums)
pkill -f "$RUN/introspect-daemon.rkyv" 2>/dev/null
pkill -f "$RUN/spirit-daemon.rkyv" 2>/dev/null
rm -rf "$RUN"
```

Expected: both daemons exit (each removes its bound sockets; the trace listener
removes its socket on drop, `triad-runtime/src/trace.rs:315-321`), and the run
dir is gone. Production `spirit-daemon.service` is untouched throughout.

## One-glance flow

1. introspect-daemon BINDS `$RUN/introspect-trace.sock` and listens
   (`runtime.rs:608`).
2. spirit-daemon (testing-trace) CONNECTS to that socket per event and PUSHES
   `ComponentTraceEvent` stamped with engine=`$RUN/spirit.sock`, component=Signal
   (`daemon.rs:116`, `trace.rs:51-56`, `trace_event.rs:79`).
3. introspect's drain loop ingests each into its sema store
   (`runtime.rs:577-598`).
4. A `ComponentTrace` query (engine=spirit-sock, component=Signal) over
   `$RUN/introspect.sock` returns the sequence-ordered events
   (`runtime.rs:165-178`, store filter `store.rs:177-187`).
