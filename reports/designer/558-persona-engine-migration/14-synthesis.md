# 558.14 — synthesis: the persona engine migration plan

designer, 2026-06-08. The cross-component synthesis of the twelve per-component
assessments (`2`–`13`) and the foundation pass (`1`). This is the authoritative
read; the numbered files carry the per-component evidence.

## Headline

The migration is **further along in execution and further behind in shape than
prior reports implied.** Two facts dominate:

- **The nexus execution engine is real and proven.** `triad-runtime`
  `Runner::drive` is a working async driver, the emitter generates the
  `RunnerEngines` adapter + `NexusEngine::execute` glue, and **`spirit` runs
  every request through it with zero `signal-executor`, end to end.** This
  **corrects report `555`**, which framed the executor-four migration as "gated
  on the 553 nexus engine being built — the enums are the data shape, not the
  driver." The driver exists; `spirit` is the working template. The executor-four
  are gated on *adopting* it (per-component work + contract emission), not on
  *building* it.
- **The 553 actor-native shell was never built.** The emitter emits a
  *task-native* `GeneratedDaemonRuntime` (engine behind a tokio `Mutex`) on the
  async listener substrate; the **only real kameo actor in the runtime is
  `RequestGate`.** There is no `RuntimeRoot` / `SemaActor` / per-request Nexus
  driver tree. This is why **`kameo-discipline` is "done" on zero of twelve
  components** and why "actors all the way down" (`zk6y`) is unrealized
  fleet-wide.

## Readiness matrix

D=done · H=hybrid · P=partial · −=not-started · ·=n/a

| Component | Shell | Nexus | Contr→SN | 2-contract | Naming | SEMA | Kameo | NOTA | Docs | Readiness |
|---|---|---|---|---|---|---|---|---|---|---|
| spirit | D | D | H | D | D | D | P | D | D | **mostly** |
| message | D | D | H | P | D | · | · | D | D | **mostly** |
| router | D | H | H | P | D | D | H | D | D | **mostly** |
| terminal | D | H | − | D | D | H | P | D | D | **mostly** |
| orchestrate | H | D | H | D | D | D | − | − | H | partial |
| upgrade | − | H | H | D | D | P | − | D | D | partial |
| repository-ledger | H | − | − | H | D | H | H | D | H | partial |
| mind | − | − | − | H | D | H | H | P | D | partial |
| persona | − | · | − | H | P | H | H | P | D | early |
| introspect | − | · | − | P | D | H | H | D | P | early |
| harness | − | − | − | P | D | − | H | D | H | early |
| system | − | − | − | P | D | · | H | D | H | early |

Reading down the columns: `naming-bare` and `nota-binary-boundary` are nearly
won; `Contr→SN` is **done nowhere** (`signal_channel!` everywhere); `Kameo` is
done nowhere (the missing 553 shell); the daemon-shell "D"s are all
done-on-the-task-substrate, not the actor tree.

## The two foundation gates (block the whole fleet)

Everything downstream waits on two decisions/builds in `schema-rust-next` +
`triad-runtime`:

1. **The 553 shell ruling.** The emitter emits `GeneratedDaemonRuntime impl
   AsyncMultiConnectionRuntime` (task-native, engine behind a `Mutex`). Design
   553 specified a kameo `RuntimeRoot` + `SemaActor` + per-request Nexus driver
   tree. **Either** extend the emitter to emit that actor tree (and move
   `Runner::drive` into a Nexus driver's `handle`), **or** ratify the
   task-native + `RequestGate` + single state-actor shape as the target and amend
   `zk6y`/`553`. Until this is decided, `daemon-shell-actor` and `kameo-discipline`
   cannot reach "done" for anyone — and `r310` ("revise the approach when
   implementation evidence shows a better design") explicitly licenses the second
   option. **This is the single highest-leverage decision and it is the psyche's.**

2. **The contract-crate emitter.** `WireContract` exists but emits *daemon-local
   in-tree* modules, not the published `signal-<c>` / `meta-signal-<c>` crates.
   So `signal_channel!` cannot be retired at the crate boundary yet — which is
   exactly why `Contr→SN` is done nowhere. The emitter must learn to emit a
   standalone contract crate before axis 3 can move for any component.

## Cross-cutting findings

- **`signal_channel!` is the fleet's deepest debt** (axis 3 done nowhere) — a
  structural emitter gap, not per-component laziness.
- **Four meta-signal contracts are missing** — `message`, `introspect`,
  `harness`, `system` have no `meta-signal-<c>` (`n0ss` violation), and
  `signal-engine-management` must fold into `signal-persona`/`meta-signal-persona`.
- **Storage is done at the engine, missing at the actor.** `sema-engine` (redb
  single-writer) is built and proven; what's missing everywhere is the
  schema-emitted SEMA actor wrapper + moving redb I/O off the async handler
  (`spawn_blocking`). The 556 terminal hazards (`spawn_in_thread`, no
  `RestartPolicy`, inline redb) **recur in persona's `ManagerStore` and others** —
  they are a shared substrate fix, not per-component.
- **The old blocking spine persists** (`MultiListenerDaemon` + `BoundedWorkers`,
  still `pub`, still consumed e.g. by orchestrate's running binary) — deletion is
  deferred until consumers move.
- **Stale generated files are a latent break:** `cloud` and `domain-criome` carry
  generated daemons importing the old `Actor*` names; the `Actor*→Async*` rename
  will force their regeneration.

## Sequencing

- **Phase 0 — Foundation (blocks the fleet):** the psyche's 553-shell ruling +
  extend the contract-crate emitter. Nothing else reaches "done" without these.
- **Phase 1 — Harden the exemplar:** take `spirit` from "mostly" to all-nine-green
  so it is the literal copy-template (shell promotion per the ruling, contract
  cutover, kameo state-actor, `spawn_blocking`). `spirit` already proves the
  executor-free nexus path.
- **Phase 2 — Closest copies (cheap wins):** `message` (small), `router`,
  `terminal` — already on the substrate + runner; they need contract migration
  and the kameo hardening template.
- **Phase 3 — The signal-executor four (production cutover):** `orchestrate`,
  `upgrade`, `repository-ledger`, `persona-spirit` — delete
  `Executor`/`Lowering`/`CommandExecutor`/`ObserverSet`, adopt the runner, invert
  the enforcing tests (`555`). `persona-spirit`→`spirit` is the highest-stakes
  step (production Spirit) and lands last in this phase.
- **Phase 4 — Ground-up builds:** `mind`, `introspect`, `harness`, `system`,
  `persona` — no `build.rs`, no emitted shell, missing meta-signal repos; the full
  emitter pipeline applied from scratch. `persona` is special: it is an
  engine-**manager** (spawns/supervises `EngineSupervisor` + `DirectProcessLauncher`
  + FD-handoff), a topology the leaf-component emitter and the `spirit` exemplar
  do **not** exercise — its shell needs proving separately.

## Recommended first moves

1. **Get the psyche's 553-shell ruling** — the one decision that unblocks the
   most (Phase 0 → 1 → everything).
2. **Extend the emitter to emit a published contract crate** (`WireContract` →
   standalone `signal-<c>`/`meta-signal-<c>`), so `signal_channel!` can start to
   die.
3. **Finish `spirit` to all-nine-green** as the template, once 1 + 2 land.
4. **Migrate `message` + `router` contracts together** — they share the
   `signal-message`/`signal-router` surface and router's schema↔wire translation
   seam.
5. **Close the cheap axes now:** clean `persona`'s `flake.nix` of the ~176
   `persona-*` inputs (the lone `naming-bare` holdout) and fold
   `signal-engine-management` into `signal-persona`.
6. **Tee up the three open contract decisions** so they're not on the critical
   path: (a) does `meta-signal-message` exist or is `message` ratified meta-less;
   (b) the `signal-engine-management` fold shape; (c) whether
   `introspect`/`harness`/`system` get real meta tiers.

## Risks

- **Decision deadlock:** the 553-shell ruling and the contract emitter both gate
  Phase 1, and Phase 1 (spirit-as-template) gates everything. Resolve Phase 0
  first or the fan-out of later work stalls.
- **False-done on `daemon-shell-actor`:** five components read "done" but all are
  done-on-the-task-substrate; if the psyche rules for the 553 actor tree, those
  five re-open.
- **Production Spirit cutover** (`persona-spirit`) is the highest-stakes step and
  depends on the entire Phase 1 contract + exemplar chain.
- **Persona supervisor topology is unproven** against the emitter — it is heavier
  than any leaf component.
- **Old-spine deletion deferred indefinitely** while live consumers remain.

## Decisions this meta-report puts to the psyche

1. **Build the 553 kameo actor shell (RuntimeRoot/SemaActor/per-request driver),
   or ratify the task-native + RequestGate + single-state-actor shape and amend
   `zk6y`/`553`?** (Highest leverage.)
2. **`meta-signal-message`** — create it, or ratify `message` as an intentionally
   meta-less stateless ingress boundary?
3. **`introspect` / `harness` / `system` meta tiers** — real `meta-signal-<c>`
   contracts, or n/a by role?
4. **`signal-engine-management` fold** — into `signal-persona`/`meta-signal-persona`,
   confirmed retire?
