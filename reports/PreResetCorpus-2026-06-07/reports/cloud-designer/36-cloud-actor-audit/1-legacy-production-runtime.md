# 1 — legacy production runtime (what cloud-daemon actually runs)

Workflow dimension `explore:legacy-runtime`, verified by adversarial thesis-1
(verdict **confirmed**) and thesis-3 (verdict **confirmed**). Line numbers are as
of 2026-06-07; a few drifted under same-day edits (noted where it matters).

## Headline

The legacy production runtime (`crate::daemon::Daemon`) that `cloud-daemon`
actually runs is pure `std::thread` + `std::sync::Mutex` with **zero** actors,
mailboxes, thread pools, or `BoundedWorkers` — `Cargo.lock` contains no kameo and
no tokio even transitively. It spawns exactly two OS threads (one per listener),
each running a blocking `listener.incoming()` accept loop that serves every
connection **inline and serially**. Live Cloudflare IO is a `flarectl --json`
**subprocess** shell-out, and the active handler holds the **outer global
`Arc<Mutex<Store>>` lock across the entire request including that subprocess** — so
one in-flight Cloudflare call head-of-line-blocks all ordinary *and* owner work.

## Runtime topology — what cloud-daemon runs

Entrypoint chain (no actor runtime anywhere):

- `src/bin/cloud-daemon.rs:11-13` → `cloud::CloudDaemonCommand::from_environment().run()`.
- `src/daemon_command.rs:46-48` → `CloudDaemonCommand::run` calls
  `Daemon::new(self.configuration()?).run()`. Configuration is read as a single
  rkyv signal file (`daemon_command.rs:36-44`, `66-72`); inline NOTA / `.nota`
  arguments are rejected (`ArgumentError::ExpectedSignalFile`) — satisfies the
  one-argument / binary-startup rule.
- `src/daemon.rs:23-43` → `Daemon::run`, the legacy runtime. **This is the
  production path, NOT** `src/schema/daemon.rs` / `schema_runtime.rs`.

`Daemon::run` (`daemon.rs:23-43`):
1. `let store = Arc::new(Mutex::new(Store::new()));` (`daemon.rs:24`) — ONE global
   `Arc<Mutex<Store>>`.
2. Bind two `UnixListener`s (ordinary + owner) via `bind_socket` (`daemon.rs:25-32`,
   `182-200`).
3. `thread::spawn` ordinary listener (`daemon.rs:34-35`) and `thread::spawn` owner
   listener (`daemon.rs:37-38`) — TWO threads total, each with its own `Arc::clone`
   of the same Store mutex.
4. Main thread parks in `loop { thread::sleep(60s) }` (`daemon.rs:40-42`) — does no
   work, just keeps the process alive.

## Connection serving — one thread per listener, serial inline

`run_ordinary_listener` (`daemon.rs:96-107`) and `run_owner_listener`
(`daemon.rs:109-120`) are identical in shape:

```
for stream in listener.incoming() {          // blocking accept loop
    Ok(mut stream) => serve_*_stream_shared(&store, &mut stream)  // INLINE
    Err(error) => eprintln!(...)
}
```

There is **no** `thread::spawn` per connection, **no** thread pool, **no** worker
queue. Each accepted connection is served **inline on the single listener thread**,
fully, before `incoming()` yields the next stream. Serving is **strictly serial
per socket**. The two listeners run concurrently with each other (two threads), but
within each listener it is one-at-a-time. Each connection is single-request:
`serve_ordinary_stream_shared` (`daemon.rs:122-150`) reads a frame, optionally
answers a handshake, then on the first `Request` handles it, writes the reply, and
returns (closing the connection).

## Locking — outer global lock held across the provider call

Two distinct mutex layers; the first is the load-bearing finding:

1. **Outer global lock** `Arc<Mutex<Store>>` (`daemon.rs:24`). The active handlers
   are the `_shared` variants:
   ```
   let reply = {
       let store = store.lock().map_err(|_| Error::StorePoisoned)?;  // daemon.rs:137
       store.handle_ordinary_request(request)                         // daemon.rs:138
   };                                                                 // guard drops :139
   ```
   The owner side is identical at `daemon.rs:165-168`. The guard is scoped to the
   block, but **the block IS the entire request handler** —
   `handle_ordinary_request` / `handle_owner_request` run to completion (including
   provider IO) before the guard drops. **The outer lock is held across the
   blocking Cloudflare call.** Both `ordinary_store` and `owner_store` are
   `Arc::clone(&store)` (`daemon.rs:34,37`), so the two listeners share this one
   lock.

   (The inline `serve_ordinary_stream`/`serve_owner_stream` at `daemon.rs:45-94`
   take `&Store` with no outer lock — but the runtime never calls them; they appear
   unused.)

2. **Inner per-field locks** inside `Store` (`lib.rs:531-536`): `accounts`,
   `policy`, `plans`, `approved_plans`, `last_known_zones`, `last_known_records`,
   each a `Mutex<…>`. Verified by thesis-1: these are each locked **briefly** inside
   helpers and **released before** the provider call (e.g. `account_bindings` locks
   `accounts`, clones, releases at `lib.rs:904-915`). Under the outer lock they
   never contend across requests — effectively **redundant double-locking**, dead
   weight, not concurrency. It is the OUTER lock, not these, that is held across IO.

## Live Cloudflare IO call path — flarectl subprocess, blocking, under the outer lock

Correction to the brief: production does **not** use the `ureq` HttpApi.
`Store::new` (`lib.rs:548-560`) builds `ProviderClient::production()`, and
`production()` (`cloudflare.rs:290-295`) constructs `FlarectlApi`, the
**`flarectl --json` subprocess adapter**. The `ureq` `HttpApi` is only reachable
via `production_http()` (`cloudflare.rs:297-302`), which nothing calls. Both are
compiled (default `cloudflare` feature, `Cargo.toml:23-24`), but the live wire is
the subprocess.

Trace for an ordinary `Observe(Records)`:
`serve_ordinary_stream_shared` (`daemon.rs:135-139`, outer lock) →
`handle_ordinary_request` (`lib.rs:607-619`) → `observe` → `observe_records` →
`observe_cloudflare_records` → `cloudflare_record_listing` (`lib.rs:868-878`) →
`self.cloudflare.records(...)` → `FlarectlApi::records` (`cloudflare_cli.rs:167-181`),
which first calls `zone_name` → `zones` (`flarectl zone list`) **then**
`flarectl dns list --zone <name>`. Each `execute` (`cloudflare_cli.rs:88-90`) →
`ProcessRunner::run` (`cloudflare_cli.rs:46-63`) → `Command::new("flarectl")
.args(...).env(CF_API_TOKEN,...).output()` — a **blocking spawn-and-wait on a
child process**. So one records listing is **≥2 blocking subprocess executions**.
The apply path is worse: `apply_plan` (`lib.rs:1232-1253`) does an initial
`records`, then a `delete_record`/`create_record`/`update_record` subprocess per
mutation, **each** re-running `zone_name` (another `zone list`) via
`find_record_after_mutation` (`cloudflare_cli.rs:128-144`). A multi-record apply is
easily 5–15 sequential blocking subprocess spawns — all under the held outer lock.

## Second-connection trace while the first is mid-Cloudflare-call

1. The FIRST ordinary connection is served inline on the single ordinary listener
   thread, blocked inside `flarectl … output()`, **holding the outer mutex**
   (`daemon.rs:137`).
2. The ordinary thread is therefore NOT back at `listener.incoming()`. A SECOND
   ordinary connection sits **unaccepted in the kernel backlog** — it cannot even
   handshake. Blocked on the serial accept loop, independent of any lock.
3. Even if accepted concurrently (it cannot be, under this single-thread design), it
   would block again on `store.lock()` (`daemon.rs:137`).
4. An OWNER connection on the separate owner thread gets accepted/handshaked, but
   the moment it reaches `store.lock()` (`daemon.rs:166`) it blocks on the SAME
   global mutex the ordinary thread holds — so owner work also stalls.

Net: a single in-flight Cloudflare call head-of-line-blocks ALL other ordinary
requests (queued at accept) AND all owner requests (blocked on the global mutex),
with **no timeout, no bounded queue, no offload**.

## Concurrency primitive inventory

`grep` across the six legacy files for `kameo|tokio|BoundedWorkers|rayon|
threadpool|Mailbox|spawn`: only the two `thread::spawn` (the two listener threads,
`daemon.rs:35,38`) and the flarectl-subprocess error string (`cloudflare_cli.rs:52`).
Nothing else. `Cargo.lock` grep for `kameo|tokio` is empty even transitively.
Concurrency is `std::thread` + `std::sync::Mutex` only.

## Contradiction with cloud's own ARCHITECTURE.md "Actor Shape"

cloud's `ARCHITECTURE.md` mandates one-actor-per-concern (CloudflareProvider,
PlanStore, PolicyStore, RateLimitGate, RemoteOperationTracker) and "provider calls
… must not block the ordinary listener … behind provider actors with timeouts."
The legacy runtime realizes the **exact opposite on every count**: the provider
call runs inline on the listener thread, under the global Store mutex, with no
actor, no timeout, no rate-limit gate, no remote-operation tracker.

## Open questions raised here

- Are the non-`_shared` `serve_*_stream` variants (`daemon.rs:45-94`) dead code?
- Is the entire `ureq`/`HttpApi`/`production_http()` path dead in production given
  `FlarectlApi` is the only wired adapter?
- Are the six inner per-field mutexes vestigial from a pre-outer-lock design, or
  anticipating a future where the outer lock is removed (the actor cutover)?
- Is head-of-line blocking an accepted property of the pre-cutover slice, or an
  unrecorded regression vs the bounded thread-per-connection SHAPE recorded in
  Spirit `2alg`/`k6w1`/`tj99` (which implies per-connection threads, not
  per-listener)?
