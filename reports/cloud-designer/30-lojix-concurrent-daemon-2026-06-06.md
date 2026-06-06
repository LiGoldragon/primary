# 30 — lojix daemon made concurrent (resolves audit 29's open question)

cloud-designer lane, 2026-06-06. Psyche decision (intent `2alg`): the lojix
deploy daemon MUST serve multiple connections concurrently — a long `nix` build
must never block other requests, because the host driving lojix dispatches many
deploy commands at once (e.g. updating several hosts in parallel). This settles
audit 29's open question decisively against the single-writer serial model.

## The model — bounded thread-per-connection, contained to lojix

No triad-runtime (kernel) change, so `cloud` is unaffected. The
`MultiListenerDaemon` accept loop calls `handle_stream` then immediately polls
the next listener (`triad-runtime/src/daemon.rs` `try_serve_next_stream`), so
making `handle_stream` return fast frees the loop. lojix's `handle_stream` now:

1. Acquires a **connection permit** (a `Mutex`+`Condvar` counting semaphore,
   cap `MAXIMUM_CONCURRENT_REQUESTS = 64`) — backpressure on the accept loop if
   the cap is reached, so a flood cannot exhaust resources.
2. Spawns a **`RequestWorker` thread** that owns the stream and serves the
   request to completion (read → engine → reply), then returns immediately.
   The permit releases when the worker thread exits.

The accept loop is therefore free to poll BOTH sockets while any number of
deploys (up to the cap) run on worker threads.

## Per-request engine over a shared Store

The audit's refuted-but-latent concern (single-slot in-flight state corrupting
under concurrency) is dissolved structurally: `SchemaRuntime.store` is now
`Arc<Store>`, and each `RequestWorker` builds its OWN `SchemaRuntime` via
`SchemaRuntime::with_store(self.store.clone())`. So:

- The in-flight deploy cursor (`active_deploy`/`active_operation`) is **per
  request** — never shared, so no keyed in-flight map is needed.
- The durable `Store` (the four tables + sequence counters, already
  `Mutex`-backed) is the single shared concurrency point, locked only briefly
  per sema operation. Long `nix` effects run on the worker thread holding NO
  global lock.
- The monotonic counters (`next_commit_sequence`, `next_deployment_identifier`,
  …) increment under the store lock, so concurrent deploys get distinct ids /
  positions with no race.

## Proven

`tests/build_smoke.rs` `concurrent_requests_are_served_in_parallel`
(`#[ignore]`): starts a real owner deploy (a multi-second `nix` eval) on one
thread, then times an ordinary `Query` on the other socket. Result: the query
is answered in **~3 ms while the deploy runs** (the test takes ~7 s total — the
deploy's duration). A serial daemon would have queued the query behind the
deploy. All prior tests still green (8 fast + 6 ignored).

## Carried forward
- Durable-state correctness under concurrent deploys to the SAME node
  (live-set demote, rollback ring — report 26 gaps) is still M3 work; the
  concurrency MECHANISM is correct (all shared mutation is under the store
  lock), but the logical dedup/demote is separate.
- `SO_PEERCRED` owner-socket peer auth remains a triad-runtime follow-up
  (audit R3 defense-in-depth).
