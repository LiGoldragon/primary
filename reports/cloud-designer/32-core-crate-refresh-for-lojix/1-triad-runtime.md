# triad-runtime refresh — bearing on the new lojix stack

Crate: `triad-runtime` (shared runtime kernel for schema-derived triad daemons).
Path: `/git/github.com/LiGoldragon/triad-runtime`.
HEAD at survey: `33b9531` (2026-06-06 17:11), version `0.2.1`.
lojix pins `fdfd1831` (its own BoundedWorkers commit) in
`/git/github.com/LiGoldragon/lojix/triad-port/Cargo.lock:648`. lojix is BEHIND
HEAD by exactly the three target commits; `fdfd183` is a confirmed ancestor of
HEAD.

## Headline

The single most important thing: schema-rust-next now emits a COMPLETE daemon
spine (the `triad_main!`-equivalent — `ComponentDaemon`/`DaemonEntry` trait pair,
`GeneratedDaemonRuntime`, `DaemonCommand`, two-socket bind, `ConnectionContext`
threading, `ExitReport` exit) and these three triad-runtime commits are the
runtime-side primitives that emitter consumes. lojix hand-wrote ALL of it
(`daemon.rs`, `lib.rs::DaemonConfiguration`, `bin/lojix-daemon.rs::main`). The
generated spine would replace ~90% of lojix's `daemon.rs` AND close lojix's
deferred owner-socket peer-credential gap (audit R3) — BUT the emitted spine is
SERIAL with no frame cap and no read timeout, so it regresses three lojix
hardenings (R1/R2 + concurrent serving). Adopt the three primitives now; defer
the full spine migration until the emitter regains concurrency.

## What is new since lojix's pin (fdfd1831)

Three commits, all docs-or-`process.rs`, none touching `daemon.rs`,
`runner.rs`, `streaming.rs`, `workers.rs`, `frame.rs`, or `argument.rs`. So the
runtime surfaces lojix already uses (`MultiListenerDaemon`,
`MultiListenerRuntime`, `BoundedWorkers`, `LengthPrefixedCodec`,
`ListenerSocket`, `SocketMode`, `RequestErrorLog`) are byte-identical to lojix's
pin. The drift is purely additive on `process.rs` plus doc reconciliation.

### 1. `33b9531` — `ConnectionContext` (per-connection peer credentials)

`src/process.rs:31-79`. A new `ConnectionContext { user_id: u32, group_id: u32,
process_id: Option<i32> }` with:
- `ConnectionContext::from_stream(&UnixStream) -> std::io::Result<Self>`
  (`process.rs:56`), which wraps `rustix::net::sockopt::socket_peercred` — the
  `getsockopt(SO_PEERCRED)` query. New dependency `rustix` (Cargo.toml:12,
  `default-features = false`, features `std`,`net`). std's
  `UnixStream::peer_cred` is still unstable, and rustix lets the crate keep
  `#![forbid(unsafe_code)]` (`lib.rs:8`) — no raw `getsockopt`.
- `ConnectionContext::new(uid, gid, pid)` const constructor for tests /
  in-process callers.
- `user_id()` / `group_id()` / `process_id()` accessors.

Critical nuance for the report's accuracy: this type is STANDALONE in
`process.rs`. It is NOT wired into `daemon.rs` — neither
`DaemonRuntime::handle_stream` nor `MultiListenerRuntime::handle_stream`
(`daemon.rs:23`, `daemon.rs:40-44`) takes a `ConnectionContext`; both still pass
a bare `UnixStream`. The commit message's claim "the emitted daemon spine
threads `&ConnectionContext` into `handle_working_input`" refers to
schema-rust-next's emitter, NOT to triad-runtime's daemon shell. In
triad-runtime the type is a primitive a caller must invoke `from_stream` on
itself. (Verified: only `lib.rs`, `process.rs`, `tests/process.rs` mention
`ConnectionContext`; `daemon.rs` does not.)

### 2. `1bd383b` — daemon-emit: `DaemonConfiguration` + `ExitReport`

`src/process.rs:90-154`. Two surfaces the EMITTED daemon module reads:
- `DaemonConfiguration` trait (`process.rs:90`): uniform socket/storage
  accessors — `socket_path() -> &Path` (required), `meta_socket_path() ->
  Option<&Path>` (default `None`), `database_path() -> &Path`,
  `trace_socket_path() -> Option<&Path>` (default `None`), `meta_socket_mode()
  -> Option<SocketMode>` (default `None`). A component's hand-written
  `Configuration` implements this so the generated `Daemon::run` binds listeners
  without the emitter naming component-specific accessors.
- `ExitReport` (`process.rs:127`): `ExitReport::new(process_name)` +
  `from_result(Result<(), E>) -> ExitCode` — `Ok` -> success, `Err` -> print
  `"<process_name>: <error>"` to stderr + failure. The component-agnostic
  `fn main` tail, a method on a real noun (the process name) rather than a free
  function re-emitted per component.

Both are NEW exports (`lib.rs:30`). Note `DaemonConfiguration` is a TRAIT here;
lojix has a STRUCT of the same name (`lojix/triad-port/src/lib.rs:95`) — they
are different things with a name collision (see Recommendations).

### 3. `08b624a` — doc reconciliation (runner ownership + `triad_main!` status)

Docs only (INTENT.md +25, ARCHITECTURE.md +27). Pins down: triad-runtime owns
ONLY the generic recursive `Runner`/`NextStep`/`RunnerEngines`/budget; the
per-component runner GLUE (the `NexusEngine::execute` default that builds a
`Runner` and projects the reply back to a `NexusAction`) is schema-rust-next-
emitted into each component, not owned here. And — `triad_main!` is "the INTENDED
runner entry-point emission ... NOT YET BUILT — no `triad_main!` macro exists in
`triad-runtime`, in `schema-rust-next`, or in any component crate" (INTENT.md:84,
ARCHITECTURE.md:96).

STALE-DOC FLAG (adversarial finding): this "NOT YET BUILT" claim is now FALSE.
The doc landed 12:44 on 06-06; later that day schema-rust-next landed the
emitter — `33337d7 land triad_main daemon emitter`, then `6685e7b emit
ConnectionContext into the daemon handle_working_input hook` (17:12, one minute
after triad-runtime's `33b9531`). schema-rust-next HEAD (`6685e7b`, ahead of
lojix's schema-rust-next pin `c0a331a`, which is a confirmed ancestor) carries
`src/daemon_emit.rs` (986 lines), wired via `pub mod daemon_emit` + `pub use`
(`schema-rust-next/src/lib.rs:10,12`) and documented in its own header as "the
`triad_main!` emitter from designer report 542." So the entry-point emission
exists; triad-runtime's INTENT/ARCHITECTURE just hasn't caught up. The runtime-
side ownership claim (triad-runtime owns the loop, not the glue) is correct and
unaffected.

## The schema-rust-next daemon emitter — what it actually emits (context)

This is the load-bearing context for every lojix recommendation, because it is
the thing that consumes all three new triad-runtime surfaces. From
`/git/github.com/LiGoldragon/schema-rust-next/src/daemon_emit.rs`:

- `pub trait ComponentDaemon` (`daemon_emit.rs:378`): the component declares
  `Configuration: DaemonConfiguration`, `Engine`, `Error`, `PROCESS_NAME`, and
  implements `load_configuration`, `build_runtime` (the emitter can't know how
  to open the Store/Engine), and `handle_working_input(engine: &Engine, input:
  Input, connection: &triad_runtime::ConnectionContext) -> Result<Output,
  Error>` (`daemon_emit.rs:412`). `start`/`stop` default to no-ops. The meta
  tier is an owner-only escape hatch the component owns end to end.
- `GeneratedDaemonRuntime<Daemon>` (`daemon_emit.rs:~790`): owns the engine; its
  `handle_working_stream` IS the decode→execute→encode spine — it calls
  `ConnectionContext::from_stream(&stream)` (`daemon_emit.rs:843`) and passes
  `&connection` into `handle_working_input` (`daemon_emit.rs:849`).
- `DaemonBinder::bind` (`daemon_emit.rs:~501`): builds the engine, makes a
  `ListenerSocket::new(ListenerTier::Working, configuration.socket_path())`, and
  — when `configuration.meta_socket_path()` is `Some` — pushes
  `ListenerSocket::new(ListenerTier::Meta, ...).with_socket_mode(...)` using
  `configuration.meta_socket_mode()`. Then `MultiListenerDaemon::new(...)`.
- `DaemonEntry::run_to_exit_code()` (`daemon_emit.rs:976`):
  `ExitReport::new(Self::PROCESS_NAME).from_result(DaemonCommand::<Self>::from_environment().run())`.

So the emitter wires ALL THREE new triad-runtime surfaces:
`ConnectionContext::from_stream` into the working hook, `DaemonConfiguration` as
the bind input, `ExitReport` as the exit tail.

DECISIVE CAVEAT — the emitted spine is SERIAL and UNHARDENED. Verified by
grep over `daemon_emit.rs`: NO `BoundedWorkers`, NO `thread::spawn`, NO
`dispatch`, NO concurrency anywhere; NO `set_read_timeout`; NO
`MaximumFrameLength`/frame cap. `handle_working_stream` reads a frame, executes,
writes the reply inline on the accept thread. That is the M0/M1-minus model lojix
deliberately moved past.

## How each development bears on lojix — does it replace what lojix hand-wrote?

lojix's hand-written daemon (`lojix/triad-port/src/daemon.rs`) currently:
binds two `ListenerSocket`s (Ordinary/Owner) on a `MultiListenerDaemon`
(`daemon.rs:70-81`); `validate_owner_socket_mode` rejects any other-access bit on
the owner socket (`daemon.rs:99-104`) — authority "rests entirely on the socket
file mode (no peer-credential check yet — audit R3)" (`daemon.rs:96-98`);
offloads each request onto a shared `BoundedWorkers` cap-64 pool
(`daemon.rs:111,132,162`, intent 2alg/k6w1); per request sets a 10s read timeout
(`daemon.rs:30,190,202`, audit R2) and an 8 MiB frame cap (`daemon.rs:25,131`,
audit R1); builds a fresh `SchemaRuntime` per request over a shared
`Arc<Store>`; and tags every request `with_origin_route(OriginRoute(0))`
(`daemon.rs:222`) — a HARDCODED origin, no peer identity.

### ConnectionContext → directly addresses lojix's deferred R3 owner-auth gap

YES, this is the close-the-gap surface for lojix's owner socket. Today lojix
authorizes the owner/meta tier PURELY by file mode (`validate_owner_socket_mode`,
`daemon.rs:99`). `ConnectionContext::from_stream(&stream)` gives lojix the
kernel-vouched peer `uid`/`gid`/`pid`, which is the second factor audit R3 asked
for. And lojix already has the exact seam to feed it into: the hardcoded
`OriginRoute(0)` at `daemon.rs:222`. lojix's engine already threads `OriginRoute`
through `apply_sema_write`/`observe_sema_read`
(`lojix/.../schema/nexus.rs:1253-1254`); lojix's `schema_runtime.rs:1421` takes
`_origin_route` (currently unused). So the wiring is: `from_stream` ->
classify uid against the owner uid -> mint a real `OriginRoute` instead of `0`.
This is a genuine MUST-port (it closes a security gap the audit flagged), and it
is small because the seam already exists.

Adversarial check: ConnectionContext does NOT replace
`validate_owner_socket_mode` — file-mode hardening and peer-credential auth are
complementary (defense in depth). lojix should keep both.

### DaemonConfiguration (trait) → partially applies; name collision is real

The trait standardizes the accessors the GENERATED spine reads. lojix's own
`DaemonConfiguration` is a STRUCT (`lojix/.../lib.rs:95`) with fields
`ordinary_socket_path`, `ordinary_socket_mode`, `owner_socket_path`,
`owner_socket_mode` — note: NO `database_path` (lojix Store is in-memory), NO
`trace_socket_path`, and the meta tier is named "owner" not "meta". If lojix
ever adopts the generated spine, its config struct must IMPLEMENT the trait:
`socket_path()` -> ordinary, `meta_socket_path()` -> Some(owner),
`meta_socket_mode()` -> Some(owner mode), and `database_path()` would need a real
path (blocker: lojix has no durable DB yet — `Store` is `Mutex`-backed in-memory,
`lib.rs:166-169`). Until the spine migration, implementing the trait is NICE-TO-
HAVE alignment, not required. The name collision (struct vs imported trait both
`DaemonConfiguration`) must be resolved on import (e.g. `use
triad_runtime::DaemonConfiguration as DaemonConfigurationContract`) or by
renaming lojix's struct.

### ExitReport → cleanly replaces lojix's hand-written exit tails

lojix has TWO hand-written exit tails that ExitReport supersedes:
`bin/lojix-daemon.rs:6-14` (`eprintln!("(DaemonRejected [{error}])");
std::process::exit(2)`) and `bin/lojix.rs:12-20` (CLI). ExitReport gives `Ok ->
SUCCESS, Err -> "<name>: <error>" + FAILURE`. Note a behavioral difference:
ExitReport prints `"<process_name>: <error>"` and exits code 1 (FAILURE);
lojix prints a NOTA-shaped `"(DaemonRejected [...])"` and exits 2. The NOTA-
shaped error and the specific exit code 2 are lojix-intentional (NOTA-only output
discipline). So ExitReport is a CLEAN fit ONLY if lojix accepts plain
`"name: error"` stderr + exit 1; otherwise lojix should keep its NOTA-shaped
tail. This is nice-to-have, and weakly so — adopting it trades a NOTA-shaped
error for a generic one. Recommend NOT adopting ExitReport standalone; it only
makes sense as part of the full generated spine (which owns the whole `fn main`).

### The doc-reconciliation commit → no code bearing on lojix

08b624a is docs only. It changes nothing lojix compiles against. Its bearing is
informational: it (incorrectly, now) says `triad_main!` isn't built. lojix should
NOT trust that line — the emitter is live in schema-rust-next HEAD. No action.

## Must-port vs nice-to-have

MUST-PORT (one):
- ConnectionContext peer-credential auth on the owner socket — closes audit R3,
  the deferred owner-auth gap. Small, because lojix's `OriginRoute(0)` seam and
  engine origin-threading already exist.

NICE-TO-HAVE:
- DaemonConfiguration trait impl on lojix's config struct (only matters for the
  spine migration; blocked on `database_path` / in-memory Store).
- ExitReport (weak; trades NOTA-shaped error for generic; only natural inside the
  full spine).

DO-NOT-PORT-YET (large, blocked):
- The full generated `ComponentDaemon` spine. It would delete ~90% of lojix's
  `daemon.rs` AND auto-wire ConnectionContext — but it is SERIAL with no frame
  cap and no read timeout, regressing lojix audit R1/R2 and intent 2alg/k6w1
  concurrent serving (lojix's headline M1 property: a query answered in ~4ms
  while a deploy ran). Blocked until the emitter regains BoundedWorkers +
  read-timeout + frame-cap. This is the strategic convergence target, not a
  current action.

## Recommendations (with effort + risk)

1. Bump lojix's triad-runtime pin fdfd1831 -> 33b9531 (HEAD). Effort: small.
   Risk: very low — the three new commits are purely additive on `process.rs` +
   docs; `daemon.rs`/`workers.rs`/`runner.rs`/`frame.rs`/`argument.rs` are
   byte-identical to lojix's pin, so nothing lojix uses changed. The only new
   transitive dep is `rustix` (already widely used). Do this first; it's the
   prerequisite for #2.

2. Wire `ConnectionContext::from_stream` into lojix's owner-socket auth (audit
   R3). In `RequestWorker::serve`/`serve_owner` (`daemon.rs:177,201`), read
   `ConnectionContext::from_stream(&stream)`, compare `user_id()` against the
   daemon's owner uid, and mint a real `OriginRoute` (owner vs non-owner) to
   replace the hardcoded `OriginRoute(0)` at `daemon.rs:222`. Effort: small-
   medium (the seam exists; the policy — which uid is "owner", reject vs tag — is
   the design work). Risk: medium — it's an auth-path change; a wrong uid
   comparison either locks out the legitimate owner or fails open. Keep
   `validate_owner_socket_mode` as well (defense in depth). Capture the
   owner-uid policy as intent before coding.

3. Do NOT migrate to the generated `ComponentDaemon` spine yet. Effort to
   migrate: large. Risk: high (concurrency + hardening regression). Instead, file
   the convergence as a tracked item against schema-rust-next: the emitter needs
   `BoundedWorkers`-based concurrent serving, a per-request read timeout, and a
   `MaximumFrameLength` cap before any concurrent daemon (lojix, and eventually
   spirit/cloud) can adopt it without regressing. lojix's hand-written
   `daemon.rs` is currently the reference implementation of those three
   properties — feed it back into the emitter design.

4. (Optional, low priority) When the spine converges, plan to implement
   `triad_runtime::DaemonConfiguration` on lojix's config struct under an aliased
   import to avoid the name collision, and resolve the `database_path` gap (lojix
   in-memory Store has no path). Effort: medium. Risk: low. Not now.

## Open questions

- Owner-uid policy: which uid(s) count as "owner" for the meta tier, and on a
  peer-credential mismatch does lojix REJECT the connection or merely TAG a
  non-owner `OriginRoute` and let the engine refuse privileged verbs? This is
  unstated intent; capture before #2.
- Should the generated spine become lojix's daemon once it gains concurrency, or
  does lojix keep a hand-written daemon permanently because its deploy workload
  (multi-minute nix builds) wants concurrency tuning the emitter won't express?
  This decides whether #2 is throwaway (folded into the spine later) or durable.
- triad-runtime's INTENT.md/ARCHITECTURE.md say `triad_main!` is "NOT YET BUILT"
  but schema-rust-next HEAD emits it — should triad-runtime's docs be corrected
  (designer task on triad-runtime, not lojix)?
- ExitReport prints `"name: error"` + exit 1; lojix prints NOTA-shaped
  `"(DaemonRejected [...])"` + exit 2. Is the NOTA-only output discipline meant
  to extend to the process-exit stderr line, or is a plain `name: error` line
  acceptable at the process edge?
