# Actor-Native Engine Rewrite — Audit, Gameplan, and Migration Invariants

Role: system-operator. Dates: 2026-06-07.

This merges the two audit passes (reports 200, 201) of designer report `553-actor-native-engine-rewrite` and the implementation gameplan (report 202). The audited target (designer 553) drove the lojix implementation now recorded in reports 203/204/205; this record preserves the reusable design rationale: the migration invariants, the actor-noun ownership table, the effect taxonomy, the contradictions that had to be resolved before implementation, and the open psyche questions.

## Authority and intent chain

Spirit record `zk6y` is the supersession line: schema-emitted Signal, Nexus, and SEMA engines are Kameo actors, not synchronous runner loops over mutex-wrapped state. Supporting records: `3d5z` (strict triad separation — Signal owns communication, Nexus owns decision-making, SEMA owns durable state), `a71r` (every component engine defines and uses its Signal/Nexus/SEMA schema interfaces, with handwritten logic conducted through schema-emitted traits over root types), `tj99` (lojix hand-written daemon properties feed back into the schema-rust-next emitter), `59dr` (deferred machinery was advanced backpressure/scheduling, NOT actors themselves), `xqkv`/`tpcm` (generated runtime traces must prove actual Signal/Nexus/SEMA usage, not symbol presence). The old "defer runtime machinery" argument therefore cannot keep sync daemons; the deferral was about advanced scheduling, not the basic actor substrate.

## Verdict

Proceed as a breaking rewrite. Backward compatibility is not a constraint for this stack: delete the synchronous daemon substrate, delete compatibility wrappers, and make tests assert the old shapes are absent. The load-bearing migration is concentrated in two places: `triad-runtime` and `schema-rust-next/src/daemon_emit.rs`. Once those are actor-native and tests enforce the shape, generated consumers (`spirit`, `message`, `cloud`) follow by regeneration plus thin hook adjustments. Hand-written islands (`lojix/triad-port`, `repository-ledger`, old live `cloud::daemon`) collapse into the generated path.

The central critique: "actors everywhere" must NOT translate the existing synchronous structure into one giant actor. A singleton `NexusActor` owning a runner loop would preserve the bad serialization point under an actor name. The correct shape is a small actor topology: listener actors, per-request driver actors or permit-capped request tasks, SEMA store actors / read snapshots, effect actors for blocking work, subscription actors, and explicit root supervision.

The edited designer 553 (audited in pass 2 / report 201) absorbed the load-bearing corrections: no god-actor, per-request Nexus driver, SEMA reads via redb snapshots, typed generated meta tier, operation-specific lojix cancellation, effect taxonomy, pilot order, and runtime-truth tests. It became good enough as architectural direction; the residual fixes were two contradictions in the brief (below).

## What 553 got right

- **Root cause is shared runtime emission.** Generated daemons are sync because `schema-rust-next` emits a sync runtime around `triad-runtime`. The central correction belongs in the emitter (`daemon_emit.rs`), not per consumer.
- **"Actor shell, pure logic inside" split.** Domain transformations stay pure and synchronous when CPU-local and fast; runtime ownership, lifecycle, transport, concurrency, and backpressure become actor-native. The corrected rule: pure domain methods allowed inside engine nouns; runtime edges are actors; shared mutable state is owned by actors, not `Arc<Mutex<_>>`; blocking effects are explicit blocking-plane actors or async process tasks.
- **lojix is the right stress test.** Long-running Nix effects, two authority surfaces, deployment state, concurrency. If the actor runtime hosts lojix cleanly, smaller components are unlikely to expose deeper flaws.

## Research substrate (external)

- Kameo 0.20: `Self` IS the actor; spawn forms for async actors, custom mailboxes, dedicated-thread actors, pre-linked supervision; `ActorRef` exposes `ask` (replies) and `tell` (one-way); `spawn` uses a Tokio task with bounded default mailbox; `spawn_in_thread` is for blocking operations on a dedicated thread.
- Erlang/OTP, Akka, Orleans: supervision is topology not logging; restart replaces an instance behind a reference; durable stateful entities are separated from stateless/parallel workers.
- Tokio `UnixListener::accept().await` is cancel-safe and replaces `set_nonblocking` + sleep polling. Tokio `process::Command` has `kill_on_drop`, process groups, pipe control, reaping caveats; child processes continue after handle drop unless `kill_on_drop(true)`. `spawn_blocking` is for finite blocking work; started tasks cannot be aborted.
- redb: ACID with MVCC for concurrent readers + one writer.

Practical implication: actor-native does NOT mean every heavy operation goes through `spawn_blocking`. Long/cancellable external commands (Nix builds) need process actors or async process handles. Short redb transactions can use blocking isolation, but a dedicated store actor/thread is preferable to saturating the blocking pool.

## Target architecture and actor nouns

Minimum useful split (ownership is the point, not actor count — every mutable runtime concern has exactly one actor owner, and request concurrency is bounded without global locks):

| Actor / noun | Lives in | Owns | Does not own |
|---|---|---|---|
| `RuntimeRoot` | triad-runtime template emitted into component | startup, supervision, child refs, shutdown, policy | request logic |
| `Listener` | generated/runtime | one Unix socket, async `accept().await` loop per authority tier, peer credentials, stream handoff | decoded domain semantics |
| `AcceptedStream` | triad-runtime | stream + `ConnectionContext` + authority tier | — |
| `RequestPermit` / `PermitPool` | triad-runtime | bounded concurrency admission (async semaphore, replaces `BoundedWorkers`) | — |
| `RequestDriver` | generated/runtime | one connection/request lifecycle, transport, reply writing, cancellation context | durable store |
| `SignalEngineShell` | generated | actor wrapper over sync `SignalEngine` transforms (admission, origin route, validation, outer reply shape) | durable writes |
| `NexusDriver` | generated/runtime | async continuation loop over sync `decide` for ONE in-flight message | global mutable state |
| `SemaStore` | generated/runtime or sema-engine | write transactions, commit markers, durable mutation ordering (single-writer) | public wire handling |
| `ReadSnapshot` | sema-engine proof first | typed redb read observation boundary, parallel reads | write sequencing |
| `SubscriptionRegistry` | triad-runtime | subscriber registry, writer ownership, event fan-out, stream tokens | component decisions |
| `EffectSupervisor` / `ProcessEffect` | triad-runtime + component effect schema | effect actor tree; long external command with process group, streaming, cancellation policy | schema routing |
| `TraceActor` | test-only / runtime | structured trace sink | business logic |

Control flow: `Listener.accept` -> spawn/ask `RequestDriver` with stream+tier -> async read length-prefixed frame -> decode -> ask `SignalEngineShell::Admit` -> validate+attach origin -> ask `NexusDriver::Process` -> execute schema-visible feature verbs, ask `SemaStore` for writes or `ReadSnapshot` for reads, ask `EffectSupervisor` for external effects -> Signal shapes final typed reply -> `RequestDriver` encodes and writes frame. This keeps the Signal/Nexus/SEMA conceptual flow but makes the runtime mechanics honest.

## Concrete critique points (from pass 1, report 200)

1. **"Runner loop moves into Nexus actor" is too easy to misimplement.** A singleton Nexus asked to run the whole loop just moves serialization from `Mutex<Nexus>` into a mailbox. Singleton actors own durable/global concerns; request-local state belongs to a per-request `NexusDriver`. A singleton Nexus-like actor, if it exists, is a factory/router/policy actor, not where every long request waits.
2. **SEMA read/write separation needs concrete ownership.** `SemaStore` owns writes + marker sequencing; `ReadSnapshot` objects are minted from the store and serve read-only requests concurrently (redb MVCC); long scans bounded separately from point lookups; read transactions are sync redb work needing a blocking boundary or dedicated read actor/thread.
3. **Blocking effects need cancellation semantics, not just async APIs.** Tokio children continue after drop unless `kill_on_drop(true)`. For lojix: client disconnect cancels speculative query/build (`kill_on_drop`); deploy jobs survive caller disconnect (job actor + persisted state). Choose per operation; a blanket rule is wrong.
4. **`spawn_blocking` is not a long-running work queue.** Short redb/filesystem bridge: `spawn_blocking` or dedicated SEMA actor thread acceptable. Long Nix/cloud command: `tokio::process` under an effect actor. Indefinite watcher/spool loop: actor with async interval/watch source.
5. **Subscription handling must not stay a mutexed registry.** Emit a `SubscriptionActor` or call into a triad-runtime generic subscription actor.
6. **Meta tier must stop being a raw stream escape hatch.** Schema should emit meta input/output transport like working transport; component hooks receive decoded meta input and return typed meta output; raw-stream escape hatches are rare and named.
7. **Docs are split-brained.** `triad-runtime` and `schema-rust-next` INTENT/ARCHITECTURE still described the sync listener runtime as production; those statements were accurate before `zk6y` and are now stale. Repo docs change in the same changeset as the actor-native code.

## Migration invariants

```text
M1. Generated daemon transport is async and actor-owned.
M2. Every mutable runtime concern has exactly one actor owner.
M3. Request-local Nexus state is not stored in a singleton actor or mutex.
M4. SEMA writes serialize through the SEMA actor; reads use explicit snapshots/read actors.
M5. Subscription state is actor-owned.
M6. Meta tier is generated and typed; raw-stream meta hooks are exceptional.
M7. Long effects are effect actors with typed cancellation/persistence policy.
M8. Trace tests prove the intended path at runtime.
M9. Docs change with code; no stale sync-runtime intent remains.
```

## Tests required before calling it done

- **Mechanical:** generated daemon source must not import `std::os::unix::net`; contains Kameo actor impls for root/listener/request; no `Mutex<Engine>` or `Arc<Mutex<Store>>`; typed meta tier (no raw stream hatch); no mutexed generated `SubscriptionState`.
- **Behavioral (weight these above actor-density counts):** slow request does not block accept on working or meta sockets; working and meta sockets progress independently; SEMA writes order markers monotonically; SEMA reads parallelize during/after a pending write; trace proves Signal admission -> Nexus decision -> SEMA read/write -> Signal reply.
- **Effect:** Nix build streams progress rather than waiting for `.output()`; disconnect either cancels or preserves the job per operation policy; code test forbids long Nix effect via `spawn_blocking`.
- **Runtime-safety:** actor panic supervision for a request child; shutdown drains or rejects per typed policy; permit exhaustion returns a typed busy reply (no hang); no ad hoc `tokio::spawn` task soup in generated runtime.

## Second-pass corrections (report 201, S1-S8)

- **S1.** lojix multi-minute Nix builds use `tokio::process`, NOT `spawn_blocking + DelegatedReply`. `spawn_blocking` is for short synchronous redb/filesystem bridges only.
- **S2.** "`spawn_in_thread` forbidden" is over-hardened. Correct rule: `spawn_in_thread` is allowed only if the exact Kameo version's shutdown/drop semantics are proven by a restart/reopen truth test for the resource it owns (redb open, actor stop, wait, reopen same path). Without that proof, prefer `.spawn()` plus a bounded blocking boundary. `mind` uses a forked Kameo `spawn_in_thread`; `chroma` uses upstream-style `spawn_in_thread` for synchronous redb. Do not bake a fork-specific lifecycle observation into a universal upstream-Kameo law.
- **S3.** `harness/src/daemon.rs` is a Kameo IDIOM source (actor lifecycle, `ActorRef`, `ask`, replies, graceful shutdown), NOT a listener-architecture source — the target is async `tokio::net::UnixListener::accept().await`, not a blocking std listener bridged into a Tokio runtime.
- **S4.** `skills/component-triad.md` carried both the new "runtime triad engines are kameo actors" wording AND the old `triad-runtime::Runner::drive` reached from `NexusEngine::execute` default method. The old wording must be removed or marked pre-actor legacy; the actor shell owns the loop and uses the sync `_inner` decisions.
- **S5.** Toolchain target underspecified: triad-runtime/schema-rust-next at 1.85, chroma 1.88, harness/mind 1.89. Resolve the canonical Rust toolchain from CriomOS/Home and use that one version across Cargo.toml, rust-toolchain.toml, Nix/Fenix inputs, and locks — do not hard-code 1.88.
- **S6.** SEMA read-snapshot API still conceptual: name the ownership boundary (does `SemaStore` own `redb::Database` and mint read handles, or is it `Arc`-wrapped; does sema-engine expose a typed `ReadSnapshot`; how a `DatabaseMarker` binds to a snapshot; what bounds a long scan). Require a small API proof in sema-engine or triad-runtime before broad generation.
- **S7.** Contract split must be preserved: "generated meta tier" means generate daemon transport/hooks for the meta-signal wire contract and route decoded meta input through the daemon's runtime triad. It does NOT mean adding runtime engines to `meta-signal-<component>` or folding ordinary and meta signal repos together.
- **S8.** Actor-density tests need behavior more than symbol count — actor count alone can be gamed by emitting actors that do not own the right concerns.

## Implementation gate / phased plan

Phase 0 — align the brief: edit designer 553 file 0 (remove `spawn_blocking + DelegatedReply` lojix line, point to `tokio::process`); edit `skills/component-triad.md` (remove old `Runner::drive` / `NexusEngine::execute` default-driver wording); update `triad-runtime` and `schema-rust-next` INTENT/ARCHITECTURE to declare the actor-native destination; resolve the canonical Rust toolchain.

Phase 1 — Kameo lifecycle truth lab: tiny proof in triad-runtime — data-bearing actor with owned redb path; start opens store; one write; stop; wait on documented shutdown surface; replacement opens same path immediately; repeat under the exact chosen Kameo dependency. Decides `.spawn()` + blocking bridge vs `spawn_in_thread` vs fork. No guessing.

Phase 2 — triad-runtime actor primitives: `RuntimeRoot`, `Listener` (async accept), `AcceptedStream`, `RequestPermit`/`PermitPool`, `RequestDriver`, actor trace collector, process-effect primitive, subscription registry.

Phase 3 — teach schema-rust-next to emit actor-native daemon modules (preserve token-based `ToTokens` emission).

Phase 4 — regenerate small pilots first: `message` (minimal no-store, plus one slow-request concurrency witness in the same pass) -> `spirit` (full SEMA) -> `cloud` (multi-listener/meta).

Phase 5 — port hand-written islands (lojix/triad-port, repository-ledger, old cloud::daemon) and update docs/skills.

## Open questions for the psyche / designer

1. Should deploy/build effects survive client disconnect? (lojix `tokio::process` policy: durable deploys keep a job actor and persist state; speculative builds can `kill_on_drop`. Expose the distinction in schema, not process-handle behavior.)
2. Is a short-lived sync compatibility layer allowed? (Recommendation: compatibility only on a named migration branch, not a permanent public runtime surface.)
3. Where should generic subscription actor code live? (Likely triad-runtime — every streaming daemon needs it.)
4. Should SEMA read snapshots be generated primitives or component-specific hooks? (Likely triad-runtime + sema-engine expose the pattern; component schemas declare what is readable.)
5. How aggressive should the first pilot be? (`message` first for smallest state surface; not lojix first, to avoid mixing runtime migration with Nix-effect semantics.)

## Outcome

This audit/gameplan was executed: the lojix actor-native migration is recorded in `203` (sync-bridge checkpoint, since superseded), `204` (async runner — the boundary moved into `triad-runtime`'s async `Runner::drive`, generated async Nexus hooks, `tokio::process` effects), and `205` (Horizon production materialization on the actor-native daemon). The Kameo-actor discipline, the actor-noun ownership rule, and the pure-inner/async-shell split now live in `skills/actor-systems.md` and `skills/component-triad.md`.
