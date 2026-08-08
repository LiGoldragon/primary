# 4 — the provider-blocking hazard (cloud's concrete actor-model payoff)

Workflow dimension `explore:blocking-hazard`, verified by adversarial thesis-3
(verdict **confirmed**, both mechanisms true and compounding).

## Headline

cloud's own `ARCHITECTURE.md:40-41` constraint — "Provider calls must not block the
ordinary listener, owner listener, or plan store … behind provider actors with
timeouts" — is **VIOLATED today** in the live legacy runtime, on **two independent,
compounding axes**, with **zero timeouts** anywhere, making the worst case an
**unbounded whole-daemon stall** on a single hung `flarectl`. This is not a
theoretical concern: it is the concrete, reproducible payoff the actor model (or at
minimum a timeout boundary) would deliver for cloud specifically.

## Which runtime is in production

The hazard is in code that actually runs: `src/bin/cloud-daemon.rs:12` →
`CloudDaemonCommand::run` (`daemon_command.rs:46-48`) → `crate::daemon::Daemon`. The
schema path is not wired to any shipping binary.

## Axis 1 — the global Store mutex is held ACROSS the provider call

The legacy serve path locks the entire Store and holds the guard across
`handle_*_request`:
- Ordinary: `daemon.rs:135-145` — `let reply = { let store = store.lock()…?;
  store.handle_ordinary_request(request) };`. Guard drops only after the handler
  returns. The frame write is outside the lock; **the entire request handling,
  including Cloudflare IO, is inside it.**
- Owner: `daemon.rs:164-168` — identical with `store.lock()` around
  `handle_owner_request`.

`handle_ordinary_request` (`lib.rs:607-619`) / `handle_owner_request`
(`lib.rs:621-633`) dispatch per-operation. Observe-records → `cloudflare_record_listing`
(`lib.rs:867-878`) → `self.cloudflare.records(...)` (blocking IO at `lib.rs:857` for
zones). Owner `ApplyPlan` → `apply_plan` (`lib.rs:1201-1229`) → `apply_cloudflare_plan`
(`lib.rs:1231-1253`, IO at `lib.rs:1242-1244`). Both are called **while the
daemon.rs-level `store.lock()` guard is alive.**

**Rigorous nuance (thesis-3 confirmed):** the *inner* `Store` per-field mutexes
(`accounts`, `policy`, …, `lib.rs:531-536`) are locked **briefly** and **released
before** the IO (e.g. `account_bindings` clones and releases at `lib.rs:904-915`;
`cloudflare_record_listing` holds no inner field lock during the call). So if the
outer lock did not exist, the inner locking would be correct (short spans). The
hazard is entirely the **OUTER `Arc<Mutex<Store>>`** at `daemon.rs:137/166`: it is
coarse-grained, wraps the whole operation, and both listeners share the same Arc
(`daemon.rs:34,37`). Consequence: while an ordinary observe does a Cloudflare
round-trip, an owner `ApplyPlan` arriving on the owner socket blocks at
`daemon.rs:166` until it completes — and vice versa. **The two listeners are not
isolated; the global lock couples them.**

## Axis 2 — each listener's accept loop is fully serial

Independently of the lock, neither listener spawns per-connection work.
`run_ordinary_listener` (`daemon.rs:96-107`) and `run_owner_listener`
(`daemon.rs:109-120`) iterate `listener.incoming()` and call the `_shared` handler
**inline**. The only `thread::spawn` calls are the two at `daemon.rs:35,38` (one per
LISTENER, not per connection). So connection N+1 on the ordinary socket is **not even
accepted** until connection N's full serve — including its complete Cloudflare
round-trip — returns. Bounded-concurrency-of-ONE: every ordinary client serializes
behind the slowest in-flight Cloudflare call on that socket, regardless of the lock.

## No timeouts anywhere on the provider call

A full `grep` for timeout/Duration in `src/` returns only two sites, neither
bounding a provider call:
- `daemon.rs:41` — the 60s main-thread idle sleep.
- `schema_daemon.rs:40,94` — a 10s **meta-socket read** timeout (how long to wait
  for a connected client's frame) in the non-production schema path; not a
  provider-call timeout.

The production adapter is the subprocess one: `ProviderClient::production()`
(`cloudflare.rs:290-295`) → `FlarectlApi`; `ProcessRunner::run`
(`cloudflare_cli.rs:46-63`) does `Command::new(binary).args(...).env(...).output()`
— a blocking spawn-and-wait with **NO timeout**. `Command::output()` waits for the
child to exit and EOF on its pipes; if `flarectl` hangs (network stall, hung TLS,
DNS, auth prompt), `output()` never returns. The unused `HttpApi`/`ureq` path is
also untimed: `get`/`post`/`patch`/`delete` (`cloudflare.rs:140-204`) set no
`.timeout_*`. One DNS apply is 5–15 sequential `flarectl` spawns, each unbounded.

## Worst-case quantification

A single hung `flarectl` (or one slow/black-holed Cloudflare HTTP call) during any
observe / register-verify / prepare-plan / apply-plan:
1. Holds the global `Arc<Mutex<Store>>` (`daemon.rs:137`/`166`) for the entire hang.
2. Therefore blocks the OTHER listener at its `store.lock()` for the entire hang.
3. Also blocks all subsequent connections on the SAME listener (serial accept loop).

With no timeout, "the entire hang" is **unbounded** — a single stuck `flarectl`
wedges the WHOLE daemon (both sockets, all clients) indefinitely. Even a merely slow
Cloudflare (30s) freezes 100% of daemon service for 30s. Read-only capability
observes that need no provider IO (e.g. `Observe::Capabilities`, which never touches
`self.cloudflare`) are collateral victims: they cannot acquire the global lock nor
be accepted while the serial loop is mid-round-trip. This is exactly the
"stops receiving pushes / recreated a hidden lock" failure `actor-systems.md`
§"Blocking is a design bug" names: the global Store mutex held across blocking
process/network IO is the hidden lock; the serial accept loop is the starved
mailbox. **Completeness MISS-4** adds: each provider call forks a **gopass-wrapped**
flarectl (`flake.nix:48-56`) that itself shells out — compounding the blocking cost
held under the lock.

## The schema path does not hit this — but only because it does no IO

`SchemaRuntime::run_effect` (`schema_runtime.rs:458-470`) returns empty listings —
no ureq, no flarectl, no blocking — so the schema engine genuinely cannot block on a
provider. But this is the **cutover-pending stub** (`schema_runtime.rs:11-13`: "live
Cloudflare IO remains the legacy `Store` path"), not a designed non-blocking
boundary. When real IO lands in `run_effect`, the synchronous `Runner::drive` loop
will stall the single serial accept loop for the whole HTTP round-trip — so the
**cutover itself re-poses the blocking question** and must answer it before shipping.

## The remedy, and whether BoundedWorkers alone suffices

The prescribed remedy (`actor-systems.md` §"Blocking is a design bug";
`kameo.md` §"Blocking-plane templates") is to move the blocking plane behind a
named, supervised actor: the `flarectl` subprocess plane → `Command`/`CommandPool`
(Template 3: `tokio::process::Command` + bounded `timeout`); occasional HTTP →
Template 1 (`spawn_blocking` + `DelegatedReply`). This is **exactly**
`ARCHITECTURE.md:32-41`'s "Actor Shape": `CloudflareProvider`, `RateLimitGate`,
`RemoteOperationTracker`, one actor per concern, "slow provider work behind provider
actors with timeouts." Under it: the listener hands a typed message to
`CloudflareProvider` and is immediately free; the provider actor owns the bounded
`timeout` so a hung flarectl resolves to a timeout reply; `PolicyStore`/`PlanStore`
own their state so there is **no global Store lock to hold across IO at all**. That
fixes BOTH axes plus the unbounded-stall.

Does the **authorized BoundedWorkers thread-per-connection shape** alone (no actors)
also mitigate? **Partially.**
- It directly fixes **axis 2**: connection N+1 runs on its own worker thread.
- It dissolves the **cross-listener coupling** IF the coarse `Arc<Mutex<Store>>` is
  dropped for the inner per-field locks (already short, IO-free).
- It does **NOT** fix the absence of **timeouts**: a hung flarectl still ties up a
  worker thread forever, and enough hung calls exhaust the bounded pool and
  re-create a global stall. The "with timeouts" half of the constraint requires a
  timeout boundary (actor Template 3, or setting ureq/subprocess wall-clock
  timeouts directly) regardless.

And note (dimension 2 / MISS-6): BoundedWorkers is itself **wired nowhere** today —
so even this partial mitigation is currently unrealized.

## Net verdict

`ARCHITECTURE.md:40-41` is violated in production on two compounding axes, with zero
provider-call timeouts making the worst case an unbounded whole-daemon stall on a
single hung `flarectl`. The schema path sidesteps it only by not doing IO yet. The
actor shape the same file mandates is the full fix; BoundedWorkers fixes
serialization and (with the coarse lock removed) coupling, but not the "with
timeouts" requirement.

## Cheapest partial mitigation (worth flagging)

The outer `Arc<Mutex<Store>>` (`daemon.rs:24/137/166`) may not be load-bearing at
all, given `Store` already has fine-grained per-field mutexes. Sharing `Arc<Store>`
directly (dropping the outer `Mutex`) would immediately **decouple the two
listeners** and shorten all lock spans to the IO-free inner field locks — a cheap
partial fix short of the full actor shape. The serial accept loop and the missing
timeouts would still remain.
