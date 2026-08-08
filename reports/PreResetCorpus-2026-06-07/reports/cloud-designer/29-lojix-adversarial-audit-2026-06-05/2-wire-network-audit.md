# Lojix Triad — Dimension 2: Wire / Network Adversarial Audit

Adversarial posture. Every claim cites file:line in the pushed copies. Where I
could not confirm from the actual source, I say so. The daemon serves two
authority-tiered unix sockets via one `MultiListenerDaemon`; this audit attacks
the authority boundary, the cross-contract decode path, the
`execute()` fallback, the length-prefixed codec, the concurrency model, and the
socket lifecycle.

## Code map (what I actually read)

- `triad-runtime/src/frame.rs` (the `LengthPrefixedCodec`, full).
- `triad-runtime/src/daemon.rs` (the `MultiListenerDaemon` accept loop + socket
  bind/chmod, full).
- `lojix/triad-port/src/daemon.rs` (`LojixRuntime`, `handle_ordinary`,
  `handle_owner`, `execute` fallback, full).
- `lojix/triad-port/src/client.rs` (CLI exchange, full).
- `lojix/triad-port/src/lib.rs:91-99` (`DaemonConfiguration`).
- `lojix/triad-port/src/bin/lojix-daemon.rs` (entry, full).
- Both contracts' `short_header` modules + `decode_signal_frame`
  (`signal-lojix/.../schema/lib.rs:929-942,1035-1045`;
  `meta-signal-lojix/.../schema/lib.rs:632-645,732-747`).
- `triad-runtime/src/runner.rs` (continuation budget).
- `lojix/triad-port/tests/build_smoke.rs` (the round-trip test).

## Headline flaws

### W1 (HIGH) — codec pre-allocates attacker-declared length: 4 GiB OOM / DoS per frame

`LengthPrefixedCodec::default()` sets `maximum_body_length =
MaximumFrameLength::maximum_for_u32_prefix()` = `u32::MAX` = 4_294_967_295 bytes
(`frame.rs:36-38,73-77`). The daemon constructs its codec via
`LengthPrefixedCodec::default()` (`lojix/triad-port/src/daemon.rs:94`), so the
effective cap is ~4 GiB.

`read_body` reads the 4-byte big-endian length, calls `validate_length` (which
accepts anything `<= 4 GiB`), then does `let mut body = vec![0_u8; length];`
*before* reading the body (`frame.rs:105-112`). A client that connects and sends
the 4 bytes `FF FF FF FF` makes the daemon immediately attempt a single 4 GiB
zeroed allocation. On a cluster node this is an instant OOM-kill or a multi-second
allocation stall — and because the accept loop is serial (W5), one such frame on
EITHER socket stalls/kills the whole daemon, including the owner deploy surface.
The `validate_length` cap exists but is set so high it provides no protection.

Fix: the daemon must construct the codec with a real bound sized to the largest
legitimate contract frame (kilobytes, not gigabytes) —
`LengthPrefixedCodec::new(MaximumFrameLength::new(REASONABLE_MAX))`, e.g. 64 KiB
or 1 MiB. Additionally, `read_body` should not pre-zero `length` bytes from an
untrusted prefix; cap the pre-allocation and grow as bytes actually arrive (read
in bounded chunks), so a lying prefix can never force a giant allocation even
under a generous cap.

### W2 (HIGH) — connect-and-never-send wedges the whole daemon (no read timeout, serial accept)

Accepted streams have NO read or write timeout set anywhere. The listener is set
non-blocking (`daemon.rs:308`), but on Linux an `accept()`ed socket does NOT
inherit `O_NONBLOCK` from the listener — the returned `UnixStream`
(`daemon.rs:449-450`) is blocking. `handle_ordinary`/`handle_owner` call
`self.codec.read_body(stream)` → `reader.read_exact(...)` (`frame.rs:107`),
which blocks indefinitely. I confirmed no `set_read_timeout` /
`set_write_timeout` call exists in either daemon file (grep over
`triad-runtime/src/daemon.rs` and `lojix/triad-port/src/daemon.rs`).

Because the accept loop is single-threaded and per-connection-serial
(`BoundMultiListenerDaemon::try_serve_next_stream`, `daemon.rs:368-380`, iterates
listeners in-line and calls `handle_stream` synchronously before returning), a
single attacker connection that completes `accept()` but sends fewer than 4 bytes
(or sends the length prefix then nothing) blocks `read_exact` forever. The loop
never returns to poll the other socket. One unauthenticated client on the
ordinary socket permanently denies service to the owner deploy surface.

Fix: set a `set_read_timeout`/`set_write_timeout` on every accepted stream
before reading; on timeout, log and drop the connection. Independently, do not
let a single connection's IO occupy the only accept thread (see W5).

### W3 (HIGH) — the authority boundary is socket-mode-only, AND the mode is unvalidated config

The ONLY thing separating owner (meta: Deploy/Pin/Unpin/Retire) from ordinary
(read/watch) is the unix file mode on the two socket files. There is no peer-uid
check (`SO_PEERCRED`), no token, no capability. The mode is taken verbatim from
the NOTA-decoded `DaemonConfiguration.owner_socket_mode: u32`
(`lib.rs:92-97`) and applied as `fs::Permissions::from_mode(socket_mode.bits())`
(`daemon.rs:578-582`) with NO floor or validation — a config of `438` (0o666) or
`511` (0o777) is accepted silently, making the owner deploy socket
world-writable. The build_smoke test itself uses `432` == 0o660
(`build_smoke.rs:100-108`), so group membership is the entire trust model: any
process in the socket's group can issue a Deploy. Per the audit brief this is
"is it ONLY the socket file mode" — answer: yes, only the mode, and the mode is
itself attacker-influenced configuration.

Fix: (a) add `SO_PEERCRED` peer-uid/gid authorization on the owner socket as
defense-in-depth so the boundary doesn't rest on a single chmod; (b) validate
`owner_socket_mode` in `DaemonConfiguration` decode — reject any mode granting
`o+w`/`o+r` (and ideally `g+w` beyond the intended operator group), failing
closed; the owner tier should never be looser than 0o660.

### W4 (MEDIUM) — socket-mode TOCTOU: bind happens at umask-default mode, chmod applied after

`bind_listener` does `self.prepare()?` then `UnixListener::bind(self.path)?`
then `self.apply_socket_mode()?` (`daemon.rs:551-556`). The socket file is
created by `bind()` at the process umask (commonly 0022 → 0755 world-rwx for a
socket inode is typically masked to 0755/0777-minus-umask depending on libc) and
only restricted to 0660 on the *next* statement. There is a window — however
brief — where the owner socket exists at a looser mode and a racing local process
could `connect()`. Compounding: the parent directory is created with
`fs::create_dir_all(parent)` (`daemon.rs:563-568`) at the umask default with no
explicit mode — `/run/lojix` is likely 0755 (world-traversable), so the socket
path is reachable by any local user; only the final socket mode gates entry.

Fix: bind into a directory created mode 0700 owned by the daemon user, OR set the
umask tight before bind, OR bind to a temp name, chmod, then atomically rename
into place so the socket is never observable at a loose mode. Also create
`/run/lojix` with an explicit restrictive mode rather than umask default.

### W5 (MEDIUM) — one slow `nix build` blocks every socket; the daemon is fully serial

`try_serve_next_stream` (`daemon.rs:368-380`) calls
`self.runtime.handle_stream(...)` synchronously in the accept loop; `handle_owner`
drives the deploy pipeline through `self.engine.execute(work)`
(`lojix/triad-port/src/daemon.rs:110-120,122-125`), and the effect runner calls
`Command::new(...).output()` for real `nix eval` / `nix build`
(`schema_runtime.rs:1292-1296`), which blocks until the process exits.
`nix build` of a system closure can run for minutes. During that entire time the
single accept thread is inside `handle_owner`; the ordinary socket is not polled,
new owner requests are not accepted, and the daemon is unresponsive. There is no
`thread::spawn` anywhere in `schema_runtime.rs` (grep confirmed) and the runtime
trait `handle_stream` takes `&mut self`, so handling is inherently serialized
through one mutable runtime. This is a correctness/availability bug, not just
latency: watches on the ordinary socket stall for the duration of any deploy.

Fix: handle each accepted connection on its own worker (thread pool), or move the
blocking `nix` effect off the accept thread, so the accept loop stays responsive.
Note this interacts with the shared `&mut SchemaRuntime` state — concurrency
needs the store behind its existing `Mutex` (`lib.rs:163-166`) and the engine
made `Send`-safe per connection.

### W6 (MEDIUM) — `execute()` fallback emits an ORDINARY-typed reply for ANY non-reply, even on the owner path

`LojixRuntime::execute` (`lojix/triad-port/src/daemon.rs:122-143`) handles the
runner's terminal action: if it is `NexusAction::ReplyToSignal(output)` it
returns that output, ELSE (`_` arm) it hardcodes a
`SignalOutput::OrdinaryOutput(... QueryRejected ...)` — an ORDINARY contract
reply — regardless of which socket the request arrived on.

Trace the owner path on that fallback: `handle_owner` calls `self.execute(...)`
then `Self::meta_reply(output)` (`daemon.rs:115-116`). `meta_reply`
(`daemon.rs:154-161`) matches `MetaOutput` → Ok, and `OrdinaryOutput(_)` →
`Err(Error::UnexpectedFrame)`. So if the engine ever escapes the runner with a
non-`ReplyToSignal` action on an owner request, `execute` returns an
`OrdinaryOutput`, `meta_reply` rejects it as `UnexpectedFrame`, and
`handle_owner` returns `Err` — which `try_serve_next_stream` only LOGS via
`report_for_listener` (`daemon.rs:372-375`) and then drops the connection WITHOUT
writing any reply. The owner client (`client.rs:104-112`) is blocked in
`self.codec.read_body(&mut stream)` and receives EOF mid-exchange → its
`read_exact` returns `UnexpectedEof` → `FrameError::Io`. So the failure is a hang-
then-EOF on the client, not a clean typed rejection. The code comment at
`daemon.rs:128-129` asserts this `_` arm is an "invariant violation" that
"always terminates with a reply" — but nothing structurally guarantees it; if a
future schema edit lets an action escape, the owner socket silently drops
deploys. The contract-confusion the brief asks about (ordinary reply on the owner
socket) is *caught* by `meta_reply` rather than sent on the wire — good — but the
result is a silent connection drop, not a typed error reply.

Fix: make the fallback contract-aware — `execute` should take the arriving tier
and emit the matching contract's rejection (a meta `DeployRejected` on the owner
path), so the client always gets a decodable typed reply instead of EOF. Better:
have `handle_owner`/`handle_ordinary` write a typed rejection frame on ANY
handler `Err` before dropping the connection, so no exchange ends without a reply.

### W7 (MEDIUM) — cross-contract replay relies entirely on rkyv payload mismatch; the short header does NOT discriminate contracts

The brief asks whether a meta frame can be replayed on the ordinary socket. The
socket→contract binding is hardcoded by `ListenerRole` (`handle_ordinary`
ALWAYS decodes `signal_lojix::Input`, `handle_owner` ALWAYS decodes
`meta_signal_lojix::Input` — `lojix/triad-port/src/daemon.rs:98-120`), so a frame
sent to the ordinary socket is decoded as the ORDINARY contract no matter its
origin. The question is whether a meta-contract frame *also validates* as an
ordinary frame.

The short header is NOT a contract discriminator — it is only the per-enum
variant ordinal, and the two contracts use IDENTICAL header values:

- meta `INPUT_DEPLOY = 0x0000000000000000` (`meta .../lib.rs:633`) ==
  ordinary `INPUT_QUERY = 0x0000000000000000` (`signal .../lib.rs:930`)
- meta `INPUT_PIN = 0x0001...` == ordinary `INPUT_WATCH_DEPLOYMENTS = 0x0001...`
- meta `INPUT_UNPIN = 0x0002...` == ordinary `INPUT_WATCH_CACHE_RETENTION`
- meta `INPUT_RETIRE = 0x0003...` == ordinary `INPUT_UNWATCH = 0x0003...`

So `route_from_short_header` SUCCEEDS for a replayed meta Deploy frame on the
ordinary path (header 0x0 → `InputRoute::Query`), and the `HeaderMismatch` guard
(`decode_signal_frame`, `signal .../lib.rs` ~1042-1045; meta equivalent
`.../lib.rs:742-745`) does NOT catch it, because that guard only compares the
decoded value's header to the frame header — both are 0x0. The ONLY thing
rejecting the cross-contract frame is `rkyv::from_bytes::<Self,...>` failing to
validate the meta `DeployRequest` byte layout as an ordinary `Query`
(`signal .../lib.rs` ~1042). Because `Query` and `Deploy(DeployRequest)` have
very different layouts (`signal .../lib.rs:334-340`; `meta .../lib.rs:73-103`),
this *almost certainly* fails with `ArchiveDecode` → clean reject in practice.
But I CANNOT confirm from source that NO meta frame's rkyv bytes ever validate as
some same-ordinal ordinary variant — rkyv archived validation accepts any
byte-pattern that satisfies the target type's invariants, and several payloads
across the two contracts share `String`/`u64`/`Option`/`Vec` field shapes.
The safety here is incidental (layout divergence), not designed (no contract
identifier in the frame). That is a latent flaw: a future schema edit that makes a
meta variant's layout coincide with an ordinary same-ordinal variant would open a
silent cross-contract confusion with no header-level backstop.

Fix: put a contract identifier into the short header (e.g. reserve a high byte for
ordinary vs meta), so `route_from_short_header` rejects the wrong contract's
frame structurally — independent of whether the rkyv payloads happen to diverge.
This also hardens the CLIENT-side ambiguity in `decode_signal_file`
(`client.rs:79-90`), which tries the meta contract first then falls back to
ordinary purely on decode success — same incidental-disambiguation problem in
reverse.

### W8 (LOW) — one frame per connection; no framing of multiple requests, and partial/oversized handled but unlogged-as-attack

Each handler reads exactly one body and writes exactly one reply
(`handle_ordinary`/`handle_owner`, `lojix/triad-port/src/daemon.rs:98-120`); the
connection is then dropped (handler returns, stream goes out of scope). Truncated
frames (EOF after the 4-byte prefix, or mid-body) surface as
`read_exact` → `io::Error(UnexpectedEof)` → `FrameError::Io` → handler `Err` →
logged by `report_for_listener` and connection dropped (`daemon.rs:372-375`).
That is a safe failure mode (no panic, no unwrap on the read path), which I
confirm. The residual issue is purely observability: a malformed/oversized/
truncated frame is logged identically to a benign IO hiccup via `eprintln!`
(`RequestErrorLog::report_for_listener`, `triad-runtime/src/daemon.rs:151-160`),
with no rate limiting — an attacker can spam connections to flood stderr/logs.
Low severity but worth a bounded/structured log.

## Direct answers to the brief's attack questions

- (a) Authority boundary: ONLY the socket file mode separates owner from ordinary
  (W3); no peer-uid check. A meta frame replayed on the ordinary socket is decoded
  as the ordinary contract (hardcoded by `ListenerRole`) and rejected only by
  incidental rkyv layout mismatch, not by any contract identifier — the short
  header is the same per-ordinal value in both contracts (W7). Cross-contract is
  a *clean reject in practice today*, but the safety is incidental, not designed.
- (b) `execute()` fallback (`daemon.rs:122-143`): a non-reply action on the owner
  path produces an `OrdinaryOutput`, which `meta_reply` rejects as
  `UnexpectedFrame`; `handle_owner` then returns `Err` and the connection is
  DROPPED with NO reply written. So the client does not get a mistyped reply on
  the wire (the wrong-type guard catches it) — instead it gets EOF mid-exchange (a
  hang → `UnexpectedEof` decode failure). Contract violation manifests as silent
  drop, not a decodable error (W6).
- (c) Codec: the length IS bounded but the bound is `u32::MAX` ≈ 4 GiB
  (`frame.rs:36-38,73-77`), and `read_body` pre-allocates the declared length
  before reading (W1) — a huge prefix is an instant OOM/alloc-stall DoS. Partial
  reads / EOF mid-frame fail cleanly via `read_exact` (W8). A connect-and-never-
  send client blocks `read_exact` forever — no timeout — wedging the serial loop
  (W2).
- (d) Yes — one slow/blocking deploy stalls the WHOLE daemon. The accept loop is
  per-connection-serial (`try_serve_next_stream`, `daemon.rs:368-380`) and the
  `nix` effect blocks on `Command::output()` (`schema_runtime.rs:1292-1296`) on
  that same thread; the other socket is not polled meanwhile (W5).
- (e) Socket lifecycle: stale sockets ARE cleaned on bind via `remove_stale_socket`
  (`daemon.rs:570-576`, ignores `NotFound`) and removed on drop via
  `BoundSocketFile::Drop` (`daemon.rs:463-467`) — but Drop's `remove_file` only
  runs on a clean unwind; a `SIGKILL`/OOM-kill (very reachable via W1/W2) leaves a
  stale socket, which the *next* start removes, so this is self-healing on
  restart. Permissions have a TOCTOU window (bind-then-chmod, W4) and the parent
  dir is umask-default (world-traversable). The mode is attacker-influenced config
  with no floor (W3).

## What I could NOT confirm from source

- Whether any specific meta-contract frame's rkyv bytes validate as a same-ordinal
  ordinary variant (W7). I confirmed the headers collide and that only rkyv layout
  divergence rejects the replay; I did not (and cannot, statically) prove no
  collision exists for every payload pair. The design lacks a structural contract
  identifier, so the property is not guaranteed by construction.
- Exact umask of the deploying environment (W4) — the TOCTOU window's width
  depends on it; the ordering flaw (bind before chmod) is confirmed regardless.
