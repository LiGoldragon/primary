# 2 — code reality and history (workflow agent: code:reality-and-history)

cloud-designer, 2026-06-07. Verbatim from the verification workflow's code agent.
Confirms the stack is fully sync/zero-kameo across all seven components, and
traces the commit-by-commit construction of the sync runner.

## Forensic verdict: the triad daemon stack is fully synchronous, with no kameo anywhere

### (1) Current state — every component is SYNCHRONOUS; none depend on kameo

Definitive kameo check (Cargo.toml AND Cargo.lock) across all seven: zero kameo
dependencies, zero transitive kameo nodes, zero tokio/async-runtime. The only
string match for "kameo" in any source is `spirit/ARCHITECTURE.md:632`, which
explicitly states `Store` lives inside the Nexus mutex "rather than a kameo actor"
— confirming the absence.

| Component | Sync? | kameo dep? | Runner model |
|---|---|---|---|
| triad-runtime | yes | no | `Single/MultiListenerDaemon` over `std::os::unix::net::UnixListener`; blocking `incoming()` / poll+`thread::sleep`; `BoundedWorkers` = `thread::spawn`-per-task with Mutex+Condvar permit cap |
| schema-rust-next (`daemon_emit.rs`) | yes | no | Emits per-component `src/schema/daemon.rs` wiring engine into triad_runtime's sync listeners; blocking decode->execute->encode spine over `UnixStream` |
| lojix (`lojix-daemon`) | yes | no | Hand-written `MultiListenerDaemon`; `handle_stream` offloads each request onto `BoundedWorkers` (thread-per-request). Cites intent 2alg/k6w1 |
| cloud (`cloud-daemon`) | yes | no | Hand-written: two `thread::spawn` listeners, blocking `incoming()`, `Arc<Mutex<Store>>`, `loop { thread::sleep(60s) }`. Emitted sync path also present |
| message (`message-daemon`) | yes | no | Emitted `SingleListenerDaemon` over `UnixStream`; hand-writes only `ComponentDaemon` hooks |
| spirit (daemon) | yes | no | Emitted `MultiListenerDaemon` (working + meta + streaming); engine behind `std::sync::Mutex<Nexus>` |
| repository-ledger (daemon) | yes | no | Hand-written: two `thread::spawn` listeners, blocking `incoming()`, `Arc<Mutex<Store>>`, spool `loop { thread::sleep(2s) }` |

Two families: emitted (message, spirit — and cloud's secondary path) ride
triad-runtime's generated `Single/MultiListenerDaemon`; hand-written (cloud-live,
repository-ledger, lojix) roll their own thread-per-listener loops. lojix is the
only one using `BoundedWorkers` for true per-request concurrency; the others are
serial-per-listener.

### (2) History — the sync runner was built 2026-06-04..06 and POSTDATES czw0 (2026-06-02)

triad-runtime was born 2026-06-02 (`cfbcca4`, trace runtime only). The sync daemon
spine was added afterward:

- `059f036` (06-04) shared Runner glue (no listener yet)
- `ce68195` (06-05) first sync listener — `SingleListenerDaemon` over blocking `UnixListener`
- `28d03c3` (06-05) `MultiListenerDaemon` poll-loop shell
- `fdfd183` (06-06) `BoundedWorkers` thread-per-task — the only runner commit citing an intent record (k6w1)
- `33337d7` (06-06, schema-rust-next) the emitter `daemon_emit.rs` lands, making the sync skeleton the generated default

Relation to czw0: the entire sync runner postdates czw0 by 2-4 days. czw0
(2026-06-02, Decision) only defers the full actor mailbox / backpressure /
runtime-control trait surface and mandates minimal `on_start`/`on_stop` lifecycle
hooks — and it presumes persona supervision (an actor context). It does not say
"sync" or "no kameo."

Was sync ever justified by intent? No commit message, code comment, or doc cites
an intent record that authorizes choosing sync *instead of* a kameo actor. The
records that ARE cited — k6w1 (concurrency primitive belongs in triad-runtime),
2alg (lojix serves connections concurrently, per-request state), ocu7 (migrate
components onto triad_main) — govern the concurrency model and migration target,
never the actor-vs-sync choice. The closest in-code language is `workers.rs`'s
comment "Daemons with their own concurrency model (e.g. an actor runtime) simply
do not use it" — phrasing that presumes actors exist elsewhere.

### Key file locations
- `/git/github.com/LiGoldragon/triad-runtime/src/daemon.rs` (sync listeners), `/src/workers.rs` (`BoundedWorkers`)
- `/git/github.com/LiGoldragon/schema-rust-next/src/daemon_emit.rs` (the emitter)
- `/git/github.com/LiGoldragon/lojix/triad-port/src/daemon.rs`
- `/git/github.com/LiGoldragon/cloud/src/daemon.rs` + `/src/schema/daemon.rs` (emitted)
- `/git/github.com/LiGoldragon/message/src/schema/daemon.rs` (emitted) + `/src/daemon.rs` (hooks)
- `/git/github.com/LiGoldragon/spirit/src/schema/daemon.rs` (emitted) + `/src/daemon.rs` (hooks)
- `/git/github.com/LiGoldragon/repository-ledger/src/daemon.rs`
