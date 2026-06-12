# 99/3 — triad-runtime TCP listener + typed peer identity

*Implementation sub-agent chapter (workflow run `wf_8724d72d-bd4`, 2026-06-12, system-designer lane). The adversarial review — which independently re-ran every test suite — is appended.*

# triad-runtime `tailnet-listener` — tailnet TCP listener with typed peer identity (Spirit rj9y)

Branch `tailnet-listener` in worktree `/home/li/wt/github.com/LiGoldragon/triad-runtime/tailnet-listener`, head `1b5d0f17840793d00af73e8f16ad7908cad72a38`, pushed to `origin/tailnet-listener` (8 files, +618/−62). All 63 tests green, `cargo build`/`clippy --all-targets`/`fmt --check` clean. Realizes Spirit rj9y (Decision): tailnet-bound TCP listener in triad-runtime, length-prefixed codec reused, peer identity a typed closed sum, ssh-forwarded sockets rejected as transport shape.

## 1. Peer identity is a typed closed sum (`src/process.rs`)

`ConnectionContext` keeps its name and role (trust-boundary carrier, still what emitted hooks receive) but now wraps exactly one field: `PeerIdentity` (src/process.rs:134). The sum (src/process.rs:98) has two variants and only two — `Unix(UnixCredentials)` and `Tcp(SocketAddr)`; the doc states the closure rationale (no third "forwarded" identity because ssh-forwarded sockets are rejected as a transport shape, per rj9y).

- `UnixCredentials` (src/process.rs:27) is the kernel-vouched `SO_PEERCRED` triple. The old `ConnectionContext` accessors `user_id()/group_id()/process_id()` moved onto it wholesale, as did the rustix `socket_peercred` readers `from_stream` / `from_tokio_stream` (std + Tokio, each typed to the Unix stream flavor — deliberately NOT a generic `AsFd` reader, which would have let a TCP stream be queried for credentials). `unsafe_code = "forbid"` preserved; no new dependencies.
- No method pretends a TCP peer has Unix credentials: `ConnectionContext::unix_credentials()` and `tcp_address()` both return `Option`, delegating to the same accessors on `PeerIdentity`; `peer()` exposes the sum for matching.
- Construction is conversion-shaped per the From-rule: `From<PeerIdentity>`, `From<UnixCredentials>` (src/process.rs:180), `From<SocketAddr>` (src/process.rs:186) for `ConnectionContext`. The old positional `ConnectionContext::new(uid, gid, pid)` is gone (pre-production break); explicit construction is `ConnectionContext::from(UnixCredentials::new(...))`.
- `ConnectionContext::from_tcp_stream` (src/process.rs:154) reads `peer_addr()` for callers holding only a stream; the accept loop itself uses the address `TcpListener::accept` already returned (no second syscall).

## 2. Accepted connections and the connection-runtime trait are stream-generic (`src/async_runtime.rs`)

The structure that dissolved the special case: instead of a parallel `AcceptedTcpConnection` + duplicate trait, `AcceptedConnection<Stream = TokioUnixStream>` (src/async_runtime.rs:64) and `AsyncConnectionRuntime<Stream = TokioUnixStream>` (src/async_runtime.rs:134) take the transport stream as a defaulted type parameter. Every existing in-repo consumer — both Unix shells, the inline async tests, and (critically) the schema-rust-next emission `impl AsyncConnectionRuntime for GeneratedDaemonRuntime<Daemon>` — keeps compiling against the bare names. `AsyncMultiConnectionRuntime` stays defaulted-Unix and untouched. `AcceptedConnection::new` widened to `pub(crate)` (src/async_runtime.rs:332) so the TCP shell in its own module can mint admitted connections; `into_parts` doc updated from "kernel-vouched peer credentials" to "carried peer identity".

## 3. The TCP listener noun (`src/tcp.rs`, new)

`TcpListenerDaemon<Runtime>` (src/tcp.rs:25) / `BoundTcpListenerDaemon<Runtime>` (src/tcp.rs:35) mirror the `AsyncSingleListenerDaemon` shell exactly where the shape is shared and drop everything socket-file-shaped:

- Binds the configured `SocketAddr` — module doc states the runtime does not know what a tailnet is; tailnet-only ingress is the deployed bind address.
- Same admission machinery: one `RequestGate` Kameo actor per listener, permits acquired via `AcquireRequestPermit` ask, connection handling spawned as Tokio tasks with per-request error isolation through `RequestErrorLog` (src/tcp.rs:149). `with_concurrency_limit` builder matches siblings.
- `serve_next_connection` (src/tcp.rs:112) builds the context from the remote address `accept()` returned: `AcceptedConnection::new(stream, ConnectionContext::from(remote_address), permit)`.
- Frames: nothing new — handlers run `LengthPrefixedCodec` async methods over `connection.stream_mut()` unchanged.
- No socket modes, no stale-file removal, no `Drop` file cleanup: dropping `BoundTcpListenerDaemon` drops the Tokio listener, which is the whole cleanup story. `local_address()` (src/tcp.rs:98) exposes the OS-assigned port for port-0 binds.
- Errors reuse the existing typed vocabulary: `AsyncListenerError` and `AsyncSingleListenerDaemonError<RuntimeError>`; no new error enum because no new failure class exists.

Component bound is `Runtime: AsyncConnectionRuntime<TcpStream>`; one runtime object can implement both instantiations to serve both transports.

## 4. Witnesses

- `tests/tcp.rs:99` `tcp_listener_round_trips_length_prefixed_frames` — two concurrent loopback clients push length-prefixed frames through the bound listener under a concurrency-2 gate and read typed reversed-body replies.
- `tests/tcp.rs:140` `tcp_peer_identity_is_the_remote_address` — the runtime records `PeerIdentity` per connection; asserts it equals the client's `local_addr()`, is the `Tcp` variant, and `unix_credentials()` is `None`.
- `tests/tcp.rs:177` `dropping_the_bound_listener_releases_the_address` — rebinding the exact dropped address succeeds (the TCP cleanup story made falsifiable).
- `tests/process.rs:171` / `tests/process.rs:185` — explicit Unix vs TCP context construction: Unix carries the credential triple and no address; TCP carries only the address and `unix_credentials() == None`. The existing `UnixStream::pair` / Tokio-pair credential tests updated to assert through the `Unix` variant.
- Unix suites untouched and green: tests/daemon.rs (6), inline async_runtime tests (10), argument/frame/runner/streaming/trace all pass unchanged.

## 5. Docs on the branch

- `INTENT.md` — trust-context paragraph rewritten for the sum; new paragraph bracket-quoting Spirit rj9y (Decision) verbatim; production-slice paragraph now names the tailnet-facing TCP listener edge. Only rj9y was added — no invented intent.
- `ARCHITECTURE.md` — Async Runtime gains the `TcpListenerDaemon` and stream-generic paragraphs; Process Runtime's `ConnectionContext` paragraph rewritten; Code Map gains `src/tcp.rs`, `tests/tcp.rs`, and the previously-missing `tests/process.rs` entry.

## 6. Emitted surfaces needing regeneration (deferred to mirror work — schema-rust-next NOT touched)

The emitted code never reads `user_id()/group_id()/process_id()` itself, so regeneration is light; the breaking edge is component hand-written policy code:

- `schema-rust-next/src/daemon_emit.rs:620` — `handle_working_input(..., connection: &triad_runtime::ConnectionContext)`: signature still compiles (type kept name/role); its emitted doc comment ("carries the accepted stream's kernel-vouched peer credentials (uid / gid / pid via SO_PEERCRED)") is now stale and should say the context carries the typed peer identity.
- `daemon_emit.rs:967/981/1023` (`WorkingTransport` stores/returns `ConnectionContext`) and `daemon_emit.rs:1594` (`WorkingInput.context`) — shape-compatible, recompile as-is.
- Component policy code MUST be updated when components rebase onto this branch: `lojix/src/daemon.rs:176-182` (`authorize` compares `context.user_id()/group_id()`; the closed sum forces an explicit decision for TCP peers — likely reject) and `message/src/router.rs:260-261` (`origin_for_connection` reads `connection.user_id()`; needs a `Tcp` arm, likely non-owner or a new remote origin). Pass-through signatures in `message/src/engine.rs:80,117` and `message/src/daemon.rs:77` compile unchanged.
- When the mirror daemon adopts the TCP shell, its emitted spine should implement `AsyncConnectionRuntime<TcpStream>`; the defaulted parameter means existing Unix emissions need zero text change.

## 7. Shape notes

- One deliberate asymmetry: the Unix shells keep the `Async*` prefix (they sit beside legacy sync shells); the TCP noun is `TcpListenerDaemon` without `Async` because no sync TCP counterpart exists or ever will — the prefix would carry a distinction with no second pole.
- The `RequestGate` actor, delegated-permit wait, and per-listener-gate policy are reused untouched; no new actors were needed (accept loops remain Tokio tasks scoped to socket admission, per the repo's own architecture doc).

## branches
- triad-runtime @ tailnet-listener head 1b5d0f17840793d00af73e8f16ad7908cad72a38 (/home/li/wt/github.com/LiGoldragon/triad-runtime/tailnet-listener)

## testResults
triad-runtime (worktree /home/li/wt/github.com/LiGoldragon/triad-runtime/tailnet-listener, cargo test):
     Running unittests src/lib.rs — test result: ok. 10 passed; 0 failed
     Running tests/argument.rs — test result: ok. 7 passed; 0 failed
     Running tests/daemon.rs — test result: ok. 6 passed; 0 failed
     Running tests/frame.rs — test result: ok. 6 passed; 0 failed
     Running tests/process.rs — test result: ok. 8 passed; 0 failed
     Running tests/runner.rs — test result: ok. 7 passed; 0 failed
     Running tests/streaming.rs — test result: ok. 5 passed; 0 failed
     Running tests/tcp.rs — running 3 tests
       test dropping_the_bound_listener_releases_the_address ... ok
       test tcp_peer_identity_is_the_remote_address ... ok
       test tcp_listener_round_trips_length_prefixed_frames ... ok
       test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
     Running tests/trace.rs — test result: ok. 11 passed; 0 failed
   Doc-tests triad_runtime — test result: ok. 0 passed; 0 failed
Total: 63 passed, 0 failed. cargo build clean, cargo clippy --all-targets clean, cargo fmt --check clean.

## blockers
- Component crates lojix (src/daemon.rs:176-182) and message (src/router.rs:260-261) read ConnectionContext credential accessors directly; they will not compile against this branch until their policy code matches on PeerIdentity — intentional pre-production break, lands with the mirror-work regeneration pass.
- schema-rust-next's emitted handle_working_input doc comment describes the old credentials-only ConnectionContext; regeneration (out of this brief's scope) should refresh it to the typed peer-identity wording.


## Adversarial review

VERDICT: approve

## mustFix

## advisory
- Duplication: BoundTcpListenerDaemon (src/tcp.rs:88-157) replicates BoundAsyncSingleListenerDaemon's run/stop/serve_next_connection/acquire_permit/spawn_connection block nearly line-for-line (src/async_runtime.rs:780-851) — this machinery now exists in four copies (single, multi, AsyncListenerTask, TCP). An acceptor noun (trait: accept() -> (Stream, ConnectionContext)) would dissolve the duplication into one bound-daemon core, with the socket-file lifecycle staying on the Unix acceptor. Follows existing repo idiom, so not blocking, but it is the structure a beauty pass should find.
- ConnectionContext::from_tcp_stream (src/process.rs:154-156) is public, called by no in-repo code (the TCP accept loop builds context from the listener-returned address at src/tcp.rs:113-115), and has no test witness — unlike its Unix siblings which are both production-used and witnessed. Add a witness or drop it until the emitted spine actually needs it.
- TCP backpressure is configured (RequestConcurrencyLimit::new(2) at tests/tcp.rs:106) but never asserted — there is no peak-concurrency witness like the Unix CountingConnectionRuntime (src/async_runtime.rs:1346-1366). TcpListenerDaemon::run/serve_connections full-loop path is also untested (tests drive bind + serve_next_connection + stop). Parity with Unix single-listener coverage, but worth a witness before the TCP edge carries production traffic.
- Accessor asymmetry: PeerIdentity::unix_credentials returns Option<&UnixCredentials> while tcp_address returns Option<SocketAddr> by value (src/process.rs:108-122) though both types are Copy; returning the credentials by value would be symmetric.
- dropping_the_bound_listener_releases_the_address (tests/tcp.rs:177-201) has an inherent micro-flake window: another process could claim the freed ephemeral port between drop and rebind. Negligible locally; worth knowing if this ever runs in busy CI.

## disciplineFindings
- No free functions in src: every new fn lives in an impl on a data-bearing type — TcpListenerDaemon/BoundTcpListenerDaemon both carry real fields (src/tcp.rs:25-40), all process.rs additions are impls or From impls (src/process.rs:105-190). No ZST namespace types introduced.
- Conversions follow the From rule: From<PeerIdentity>, From<UnixCredentials>, From<SocketAddr> for ConnectionContext (src/process.rs:174-190); the TCP accept path uses ConnectionContext::from(remote_address) (src/tcp.rs:114-115).
- The closed sum is genuinely closed: PeerIdentity (src/process.rs:97-103) has exactly Unix(UnixCredentials) and Tcp(SocketAddr), no #[non_exhaustive], Option-returning accessors with no panicking or pretending path; credential accessors moved onto UnixCredentials itself; grep confirms zero stale callers of the removed ConnectionContext::new or context-level uid/gid/pid accessors.
- Naming clean: full English identifiers throughout (socket_address, concurrency_limit, request_error_log, loopback_any_port); TokioTcpListener/TokioTcpStream aliases match the existing TokioUnixStream idiom (src/tcp.rs:14 vs src/async_runtime.rs:20); tcp::TcpListenerDaemon's module-echoing prefix matches the repo's flat-crate-root re-export pattern (trace::TraceClient, daemon::DaemonRuntime) and is load-bearing at the root where the Unix listener nouns live.
- No anyhow anywhere, no dependency changes (Cargo.toml untouched), no hand-rolled parsing (test address uses std parse); errors reuse the existing typed AsyncListenerError/AsyncSingleListenerDaemonError rather than minting parallel TCP error enums — the right reuse.
- Borderline, judged acceptable: the Stream = TokioUnixStream default type parameter on AcceptedConnection and AsyncConnectionRuntime (src/async_runtime.rs:64, :134). I examined it as a possible backward-compatibility shim; it is genuine design — Unix is the dominant same-host transport and deserves the bare name, mirroring std's default-parameter idiom — and the ARCHITECTURE.md framing (lines 95-99) describes naming ergonomics, not non-disruption-as-virtue. Watch that framing if it spreads.
- Pre-existing, not introduced here: the stringly AcquireRequestPermit::new("accepted-connection") label and AsyncListenerError::RequestGate { detail: String } in src/tcp.rs:140-147 replicate the established idiom at src/async_runtime.rs:753-764.
- Test-code carve-out: loopback_any_port() (tests/tcp.rs:94) is the only non-#[test] free helper in the entire test suite; permitted under the #[cfg(test)] exception but slightly off the repo's own test idiom of data-bearing helper nouns (FrameClient in the same file).
- INTENT.md update quotes exactly one Spirit record with identifier and bracket-quote form — per Spirit rj9y (Decision) — matching the stated design constraints; no invented intent. ARCHITECTURE.md file-map additions are accurate, including back-filling the previously unlisted tests/process.rs.

## testHonesty
Yes — I re-ran cargo test myself in /home/li/wt/github.com/LiGoldragon/triad-runtime/tailnet-listener: 63 passed, 0 failed, matching the claim suite-by-suite exactly (lib 10, argument 7, daemon 6, frame 6, process 8, runner 7, streaming 5, tcp 3, trace 11, doc 0). cargo build, cargo clippy --all-targets, and cargo fmt --check are all clean as claimed. The new tests are genuine witnesses, not mock-flattery: tcp_listener_round_trips_length_prefixed_frames drives a real loopback TcpListener with two concurrent real clients through the real LengthPrefixedCodec under a concurrency-2 gate and asserts reversed bodies; tcp_peer_identity_is_the_remote_address asserts the runtime-observed PeerIdentity equals the client's kernel-reported local_addr — a real proof that identity is transport-vouched, not fabricated; dropping_the_bound_listener_releases_the_address proves the drop-is-cleanup story by rebinding the exact freed address. The process.rs witnesses were honestly migrated to the new closed sum and added negative assertions (a Unix peer has no tcp_address, a TCP peer has no unix_credentials). Coverage gaps (untested from_tcp_stream, no TCP peak-concurrency assertion, untested TCP run() loop) are noted as advisory, not concealed failures.

