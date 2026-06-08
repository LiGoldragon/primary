# 565 — the engine makeover: situation report

designer, 2026-06-08. The whole arc of making every component daemon own its
engine in a real kameo actor instead of a `Mutex`-wrapped synchronous engine
(records `zk6y`/`96mi`/`ilxh`). This report is the standing picture: what was
wrong, the fix, what is landed, the per-daemon taxonomy, and what remains.
Design + change-points are in `564`; the fleet audit that scoped it is `563`.

## One paragraph

The schema-derived daemon emitter (`schema-rust-next`) generated a runtime that
held the component engine **by value and handed it out as `&self.engine`** across
every concurrently-spawned connection task. A shared `&` cannot mutate, so every
component wrapped its real state in a `Mutex` — `orchestrate`'s `Mutex<()>` /
`Mutex<u64>` / `Mutex<HandoverState>`, `spirit`'s `Mutex<Nexus>`. That is the
`zk6y` violation: "schema-emitted engines are kameo actors, not synchronous
spines over mutex-wrapped state." The fix makes the emitter generate a per-daemon
**`EngineActor`** that *owns* the engine; the runtime drives every request through
the actor's mailbox (`engine.ask(WorkingInput{..})`). The mailbox serializes
access exactly as the lock did, but **without holding a guard across `.await`**,
and the actor's handler gets `&mut self` for free. The emitter is done and
landed; `orchestrate` (which typecheck-proves it) and `message` are migrated; the
rest of the fleet is in flight.

## What was wrong (the mechanism)

`triad-runtime`'s `AsyncConnectionRuntime::handle_connection(&self, …)` is
**shared `&self`** — the runtime is an `Arc`, cloned per connection, each
connection `tokio::spawn`ed. `Runner::drive(&mut engines, …)` needs `&mut` across
`.await` points. The only way to reconcile "shared runtime" with "engine needs
`&mut`" without an actor is interior mutability — a `Mutex` the handler locks for
the whole `drive`. That lock, held across `.await`, *is* the hidden serialization
the actor model is supposed to make explicit and supervised.

## The fix (emitter-generated `EngineActor`)

Per-daemon, the emitter now emits:

```text
EngineActor<Daemon> { engine: Daemon::Engine }      // owns the engine
  impl kameo::Actor   (on_start → Daemon::start, on_stop → Daemon::stop)
  impl Message<WorkingInput>   → Daemon::handle_working_input(&mut engine, input, &ctx)
  impl Message<MetaConnection> → Daemon::handle_meta_connection(&mut engine, conn)   (meta tier)
  impl Message<UpgradeConnection> → Daemon::handle_upgrade_connection(&mut engine, conn)  (upgrade tier)
GeneratedDaemonRuntime { engine: ActorRef<EngineActor<Daemon>> }
  handle_working_connection: read+decode frame → engine.ask(WorkingInput{input,context}) → write reply
```

The component changes are minimal and mechanical: `handle_working_input` takes
`&mut Self::Engine` (was `&`), the engine's internal `Mutex`es become plain `&mut`
fields (the mailbox serializes), the `Error` type adds `Debug +
From<EngineRequestError>` (kameo's `ReplyError` needs `Debug`; the send-failure
path needs the `From`), and the component needs **no direct kameo dep** — the
generated code references `triad_runtime::kameo::*`. A startup failure surfaces
through `wait_for_startup_with_result` (kameo 0.20's `wait_for_startup_result`
wants `Error: Clone`, which components don't have); a dead-actor send surfaces as
`EngineRequestError` on the component error channel.

## The four tiers (the emitter treats each differently)

| Tier | Condition | Engine shape |
|---|---|---|
| **Non-stream typed** | `!emits_stream && !component_decoded` | `EngineActor`, `ask(WorkingInput)` → `Result<Output,Error>`. (orchestrate, message.) |
| **Stream typed** | `emits_stream && !component_decoded` | `EngineActor`, `ask(WorkingInput)` → `WorkingOutcome{output, event}` (the actor computes `handle_working_input` **and** `published_event`); the subscription writer-registry stays runtime-side plumbing. (spirit, once adapted.) |
| **Component-decoded** | `component_decoded` | Stays on shared `&self.engine` — the component owns the whole connection loop, so routing it through one engine actor would serialize all connections. These daemons already hold state in their *own* internal kameo actors. (router, terminal.) |
| **Meta / upgrade listeners** | `with_meta_tier` / `with_upgrade_tier` | Component-decoded connections routed *through* the engine actor as `MetaConnection`/`UpgradeConnection` messages (low-volume policy traffic, correct to serialize with working state). |

## Landed (verified by re-running the builds, not agent self-report)

- **`triad-runtime` main** (`f96bd32` + `ae2e817`) — `pub use kameo;`,
  `EngineRequestError`, `DaemonConfiguration::upgrade_socket_path()`.
- **`schema-rust-next` main** (`7282446`) — the full `EngineActor` emitter (all
  tiers + the upgrade listener). Note: its own tests parse-validate the emitted
  module; the real typecheck proof is a consumer building against it.
- **`orchestrate` main** (`c93233c`) — engine in the actor, all three `Mutex`es
  gone, native-async execution, the upgrade tier wired, the **CLI migrated to
  schema frames**, old `BoundedWorkers` spine + `OperationLowering` ZST deleted.
  This is the worked template and the emitter's typecheck proof.
- **`message` main** (`7fe45bf`) — adapted (stateless ingress; `&mut` + the
  `From<EngineRequestError>` arm were the whole change).

## Per-daemon taxonomy (the full fleet)

| Daemon | Current spine | Engine-actor status | Work to finish |
|---|---|---|---|
| `orchestrate` | emitted shell, typed | **on EngineActor** ✓ landed | — |
| `message` | emitted shell, typed | **on EngineActor** ✓ landed | — |
| `spirit` (pilot) | emitted shell, typed+stream | `Mutex<Nexus>`, no kameo dep | regen + drop Mutex + stream-actor adapt (in flight) |
| `router` | emitted shell, **component-decoded** | internal `RouterRuntime` actor | already actor-internal; off-component-decoded is a later contract migration |
| `terminal` | emitted shell, **component-decoded** | internal `TerminalSupervisor` actor | same as router; the worker-lifecycle stream is hand-rolled, not a schema stream |
| `repository-ledger` | hand-wired `AsyncMultiListenerDaemon` | internal store actors | move onto the emitted shell, drop `block_on` (in flight) |
| `mind` | hand-written `UnixListener` loop | internal actors (`MindRoot`…) | full daemon-shell port (in flight) |
| `persona` | hand-written loop (**engine-manager** topology) | internal actors | full port + fold deleted helper vocab (in flight) |
| `harness` | hand-written loop | internal actors | full port (in flight) |
| `introspect` | hand-written loop | internal actors | full port (in flight) |
| `system` | hand-written loop | internal actors | full port (in flight) |
| `terminal-cell` | hand-written loop | `TerminalCell` actor | full port (in flight) |
| `persona-spirit` | hand-written loop (**PRODUCTION**, Stack A) | internal actors | replaced by the `spirit` pilot at cutover — not a blind port |
| `upgrade` | scaffold, no daemon | n/a | build the daemon when its plane lands |

The load-bearing nuance the rollout surfaced: "the engine is a kameo actor" was
**already true** for the daemons that hand-wrote their spine — they carry real
internal kameo actors. The `Mutex`-engine violation was specific to the *typed
emitted-shell* daemons (`orchestrate`, `spirit`). So two distinct workstreams hide
under "engine makeover": (a) the **emitter `EngineActor`** for typed emitted-shell
daemons (done; orchestrate+message+spirit), and (b) the broader **daemon-shell
migration** moving every hand-written-loop daemon onto the emitted shell — which
then hands it the `EngineActor` for free. (b) is the larger remaining axis.

## Wave outcome (daemon-shell migration, `wc3a3e1q6`)

**Landed green (7 of 8):** `spirit` (`f9030182`, on the `EngineActor`, `Mutex<Nexus>`
gone, `SignalActor`→`SignalAdmission`, flake de-vendored), `mind` (`51ae5508`),
`persona` (`390e6759`) + `signal-persona` (`3d8f7ea`) + `meta-signal-persona`,
`introspect` (`db707ba`), `system` (`ea7297c9`) + `signal-system`, `terminal-cell`
(`5229038f`), `repository-ledger` (`4f860608`). The non-spirit ports used the
`component_decoded()` tier (their working contracts are still `signal_channel!`,
not schema-derived) — they adopt the emitted listener/argv/lifecycle spine and
keep their existing internal kameo actors as the engine. So **every component
daemon except `persona-spirit` (production) is now on the schema-emitted shell.**

**`harness` correctly blocked** — and surfaced the real remaining gate: the
archival's deleted `signal-persona-origin` / `signal-engine-management` remotes are
still in ~10 repos' `Cargo.toml`, building only from stale git cache (fresh build
fails). The `persona` agent already did the `n0ss` fold — `signal-persona` absorbed
**both** vocabularies (origin provenance under `signal_persona::origin`, the
lifecycle surface at the crate top level). So the rehome target exists.

**Now in flight (`wmbq8znlv`):** rehome the 5 dangling contract crates
(`signal-agent`/`signal-harness`/`signal-introspect`/`signal-mind`/`meta-signal-terminal`)
then the 7 daemon repos (incl. finishing `harness`'s port, and a conservative
dep-only repoint of production `persona-spirit`) onto `signal-persona`. This is the
last gate to a fresh-buildable fleet, not just cache-buildable.

## Two coordination items

1. **`spirit` swept a peer's working copy.** Per the whole-working-copy-commit
   override, spirit's actor commit drained an uncommitted peer feature
   (`ChangeRecord`/`RecordChange` schema/store/tests + ARCHITECTURE/INTENT edits)
   onto spirit main under the actor-change description. Combined set is green; the
   peer's work is mislabeled but not lost.
2. **Deferred follow-ups** (green-gate-passing, flagged not silently dropped):
   per-component `nix flake check` e2e scripts still launch the old flag-based
   daemons (need a NOTA→rkyv config-encoding bootstrap before the daemon); the
   contract-crate `nota-text` feature-gating sweep `repository-ledger` skirted by
   pinning `signal-frame`.

## Open decisions

1. **Component-decoded daemons** (`router`, `terminal`): leave on shared
   `&self.engine` with their internal actors, or migrate their working contracts
   to typed schema roots so they ride the `EngineActor` too? They are not broken
   today; this is uniformity, not correctness.
2. **`persona-spirit` cutover**: the production daemon migrates by the `spirit`
   pilot replacing it, not by porting persona-spirit in place.
3. **`redb` off the async handler**: the engine actor serializes writes, but redb
   I/O still runs synchronously inside the async handler (`spawn_blocking` is the
   destination). A follow-up hardening, not part of the actor move.

## Closed — fleet on the actor shell and fresh-buildable

Every component daemon is on the schema-emitted kameo-actor shell and every
active repo builds from a clean checkout (no deleted-crate references): the
emitter (all tiers), `orchestrate`/`message`/`spirit` on the `EngineActor`,
`mind`/`persona`/`introspect`/`system`/`terminal-cell`/`repository-ledger`/`harness`/`router`/`terminal`
on the emitted shell, and **production `persona-spirit`** repointed (dep-only,
behaviour unchanged, full gate green). The origin keystone — `signal-persona::origin`
as the canonical origin vocab — and the downstream chains it unblocked
(`terminal-cell`/`terminal` onto the new `signal-terminal`; `signal-orchestrate`
regen + `nota-text` gating; `persona`'s per-contract config types) all landed
green. The lone remaining `nota-codec` refs are in two already-archived repos,
which is correct.

### Deferred follow-ups (small, flagged not buried)
- **`spirit` peer-sweep** — the whole-working-copy commit drained an uncommitted
  peer `ChangeRecord`/`RecordChange` feature onto spirit main under the actor
  description; green but mislabeled, worth a peer heads-up.
- **Bytes-as-`Vec<Integer>`** — the contract byte fields emit `Vec<u64>` (schema-next
  has no `Bytes` primitive); `terminal-cell` does explicit u8↔u64 boundary
  conversions. A `Bytes` primitive in schema-next would retire those.
- **`--no-default-features` test targets** for `signal-orchestrate`/`meta-signal-orchestrate`
  call `NotaSource::parse` unconditionally; the canonical green gate is default
  features. A per-test `cfg(feature = "nota-text")` is the fix.
- **`nix flake check` e2e scripts** still launch flag-based daemons — need a
  NOTA→rkyv config-encoding bootstrap before the binary-only daemons.
- **`signal-message` duplicate** `ConnectionClass`/`MessageOrigin` vs
  `signal-persona::origin` — a de-dup follow-up; consumers use one or the other
  consistently today.

## The lesson on this report

The repeated failure this arc corrected was treating a pre-production prototype as
something whose "breakage" must be managed. There is no production here except the
named Stack A; the only move is to build the target shape everywhere and repair
every consumer. The emitter change broke nothing worth protecting and unblocked
the whole daemon-shell axis. Recorded as a working discipline, not re-litigated.
