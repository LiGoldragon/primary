# Audit: Actor-Native Engine Rewrite, Second Pass

Role: system-operator
Date: 2026-06-07
Variant: Audit
Primary input: edited `reports/designer/553-actor-native-engine-rewrite/`
Previous audit: `reports/system-operator/200-Audit-actor-native-engine-rewrite-2026-06-07.md`

## Verdict

The edited report 553 is materially stronger than the version audited in report 200. It absorbed the load-bearing corrections: no god-actor, per-request Nexus driver, SEMA reads via redb snapshots, typed generated meta tier, operation-specific lojix cancellation, effect taxonomy, pilot order, and runtime truth tests.

The remaining problems are narrower and more concrete. I would not block the architecture direction on them, but I would fix them before using 553 as an implementation brief. The highest-risk issue is not conceptual anymore; it is contradictory guidance in the report and skill surface that could make an implementation agent choose the wrong runtime primitive.

## What The Edited 553 Fixed

Report 553 now directly closes most of report 200's gaps:

- It rejects the single god-actor failure mode and names per-request Nexus drivers.
- It preserves the `2alg` / `k6w1` / `tj99` concurrency intent rather than merely renaming the old mutex bottleneck.
- It moves lojix from blanket blocking-work language to `tokio::process`, with cancellation declared per operation.
- It turns the meta tier into generated typed transport rather than a raw stream hook.
- It classifies effects into short blocking work, long external commands, and indefinite watchers.
- It adopts the test/invariant suite from report 200 instead of duplicating it.
- It correctly treats `schema-rust-next` + `triad-runtime` as the leverage point.

This means report 200's broad critique is mostly superseded by 553's edited text. Report 200 remains useful as source-evidence and test inventory; report 201 is the current correction pass.

## Remaining Findings

### S1 — File 0 still contradicts file 2 on lojix effect handling

`0-frame-and-method.md` still says:

```text
lojix's multi-minute nix build moves to a spawn_blocking + DelegatedReply
blocking-plane actor
```

But `2-actor-native-design.md` correctly says long external commands use `tokio::process`, not `spawn_blocking`, with schema-visible cancellation policy.

The file 2 position is the right one. Multi-minute Nix builds are not finite blocking CPU-local work. They need process ownership, progress streaming, cancellation/durability policy, and supervision. `spawn_blocking` is appropriate for short synchronous redb/filesystem bridges; it is the wrong default for long Nix effects.

Correction: edit file 0 to match file 2, removing `spawn_blocking + DelegatedReply` as the lojix summary.

### S2 — The `spawn_in_thread` claim is over-hardened

Report 553 now says `spawn_in_thread` on a supervised state-bearing actor is forbidden in Kameo 0.20, and that SEMA must use `.spawn()` plus `spawn_blocking`.

That is too absolute given local code reality:

- `mind/src/actors/store/mod.rs` uses `spawn_in_thread()` for `StoreKernel`, with a comment saying the forked Kameo lifecycle waits for actor state to drop before replacement opens the same redb path.
- `chroma/src/state.rs` uses upstream-style Kameo 0.20 and `StateStore::spawn_in_thread(store)` specifically because redb is synchronous.
- The designer report itself warns that `mind` uses a forked Kameo and the emitter should target upstream 0.20, not fork-only APIs.

The correct rule is not "forbidden." The correct rule is:

```text
spawn_in_thread is allowed only if the exact Kameo version's shutdown/drop
semantics are proven by a restart/reopen truth test for the resource it owns.
Without that proof, prefer .spawn() plus a bounded blocking boundary, or design
a triad-runtime-owned dedicated store-thread primitive with tested shutdown.
```

For generated SEMA, the decision should be evidence-driven:

- If `.spawn()` + `spawn_blocking` is chosen, tests must prove writes serialize, long writes do not starve runtime workers, and shutdown waits for in-flight blocking work.
- If `spawn_in_thread` is chosen, tests must prove `wait_for_shutdown` means the redb handle is dropped before replacement opens the same `.sema` path, on the exact Kameo dependency used by the generated stack.

Do not bake a fork-specific lifecycle observation into the workspace as a universal upstream-Kameo law.

### S3 — Harness is a Kameo idiom source, not a listener architecture source

`1-current-stack-map.md` calls `harness/src/daemon.rs` the canonical blocking-listener to Kameo bridge. That can mislead the implementer.

The target in file 2 is async `tokio::net::UnixListener::accept().await`, not a blocking std listener bridged into a Tokio runtime. Therefore:

- copy Harness for Kameo 0.20 idioms: actor lifecycle, `ActorRef`, `ask`, replies, graceful shutdown;
- do not copy Harness for listener architecture if it still binds std listeners and bridges them into async code.

File 2 already has the right architecture. File 1 should add a warning that Harness is a partial template only.

### S4 — Skill correction landed, but the skill still carries old runner wording

`skills/component-triad.md` now has the new section:

```text
Runtime triad engines are kameo actors
```

That part is good. It says `_inner` methods stay sync-pure and the actor shell drives the loop asynchronously.

But later in the same skill, the "Nexus mechanism substrate" section still says the runner loop is `triad-runtime::Runner::drive`, reached from the schema-emitted `NexusEngine::execute` default method, and that component code reaches the daemon one-liner because the runner is a shared library reached from that default method.

That is the old sync-substrate shape. It contradicts report 553's design that the driver loop moves out of the `NexusEngine` default method into actor-owned runtime machinery.

Correction: `skills/component-triad.md` needs a second cleanup pass:

- `NexusEngine::execute` should no longer be described as the default runtime driver.
- `Runner::drive` should be described as the old synchronous substrate or renamed/reworked as an actor-runtime helper.
- The skill should say the actor shell owns the loop and uses the sync `_inner` decisions, not that a trait default method owns the daemon's execution.

This is important because skills are agent context. Leaving both statements will reproduce the same divergence.

### S5 — Toolchain target is underspecified

Report 553 says the rewrite introduces a Rust 1.85 to 1.88 bump because Kameo 0.20 requires 1.88. The local repo reality is mixed:

- `triad-runtime/Cargo.toml` has `rust-version = "1.85"`.
- `schema-rust-next/Cargo.toml` has `rust-version = "1.85"` and `rust-toolchain.toml` channel `1.85.0`.
- `chroma/Cargo.toml` has `rust-version = "1.88"` and uses Kameo 0.20.
- `harness/Cargo.toml` has `rust-version = "1.89"` and uses Kameo 0.20.
- `mind/Cargo.toml` has `rust-version = "1.89"` and uses a forked Kameo.

The implementation brief should not hard-code "1.88" as if it were necessarily the canonical workspace target. The correct gate is:

```text
Resolve the canonical Rust toolchain from CriomOS/Home, then update
triad-runtime, schema-rust-next, and generated consumers to that one version
in Cargo.toml, rust-toolchain.toml, Nix/Fenix inputs, and lock files.
```

If the canonical current profile is 1.89, use 1.89. If 1.88 is deliberately chosen, explain why Harness and Mind are ahead.

### S6 — SEMA read-snapshot API is still conceptual

The edited report correctly says SEMA writes go through a single writer and reads use redb MVCC snapshots. The remaining gap is API shape.

The implementation needs to name the ownership boundary:

- Does `SemaActor` own a `redb::Database` directly and mint read handles?
- Is the database wrapped in an `Arc` that read actors can clone?
- Does `sema-engine` expose a typed `ReadSnapshot` noun?
- Does each read actor open its own read transaction from a path, or receive a shared handle?
- How does a `DatabaseMarker` bind to a snapshot so reads can report the state they observed?
- What bounds a long scan so it does not keep old MVCC pages alive or starve cleanup?

The report can remain conceptual, but the implementation brief should require a small API proof in `sema-engine` or `triad-runtime` before generating the pattern broadly.

### S7 — Contract split must be preserved while meta becomes generated

The edited report says meta tier becomes generated and typed. That is correct, but the implementation must not collapse the two contract repos into one runtime schema.

Current `component-triad.md` is explicit:

- `signal-<component>` is an ordinary wire contract repo with no runtime engines.
- `meta-signal-<component>` is the meta policy wire contract repo with no runtime engines.
- daemon-local `signal.schema`, `nexus.schema`, and `sema.schema` emit runtime planes inside the component repo.

Therefore "generated meta tier" means:

```text
Generate daemon transport/hooks for the meta-signal wire contract and route
decoded meta input through the daemon's runtime triad.
```

It does not mean adding runtime engines to `meta-signal-<component>`, and it does not mean folding ordinary and meta signal repos together.

### S8 — Actor-density tests need behavior more than symbol count

The edited report adopts no-ZST/topology/actor-count tests. Good. But the actual success condition should be behavioral:

- a slow working request does not block accept on working or meta sockets;
- a write serializes database marker updates;
- read observations can progress without queueing behind unrelated long effects;
- subscription publish does not hold a global mutex;
- request disconnect behavior follows the schema-visible operation policy.

Source-shape tests are necessary to prevent sync regression, but actor count alone can be gamed by emitting actors that do not own the right concerns.

The implementation should weight trace-pattern and concurrency witnesses above actor-density counts.

## Updated Implementation Gate

Before an operator starts the broad migration, I would require this small gate:

1. Edit 553 file 0 to remove the `spawn_blocking + DelegatedReply` lojix summary.
2. Edit `skills/component-triad.md` to remove the old `Runner::drive` default-method description or mark it as pre-actor legacy.
3. Decide the exact Kameo store-thread policy with one truth test: redb open, actor stop, wait, reopen same path.
4. Resolve the canonical Rust toolchain from CriomOS/Home and use that, not an assumed 1.88.
5. Add a `sema-engine` or `triad-runtime` API proof for read snapshots before broad code generation.
6. Use `message` as first actor-emitted pilot, but include one slow-request concurrency witness in the same pass.

## Bottom Line

The edited 553 is now good enough as the architectural direction. It is not yet clean enough as an implementation brief because two surfaces still contradict the target:

- file 0 still points lojix toward `spawn_blocking`;
- `component-triad.md` still points agents toward `Runner::drive` as a trait default method.

Fix those two, then the next operator pass can start with the `triad-runtime` + `schema-rust-next` + `message` vertical slice.
