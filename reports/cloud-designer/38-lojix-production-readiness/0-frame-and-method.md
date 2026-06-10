# 38 — lojix production-readiness audit: frame & method

cloud-designer, 2026-06-10. Psyche prompt: *"do an analysis and tell me if
the new logic stack is ready for production."* Spirit gate: working order
(analysis request — dies if the task is erased) → **no capture**. The
readiness *verdict*, if it leads the psyche to decide "cut over" or "hold,"
is theirs to record later; this prompt records nothing.

## What "the new logic stack" means

Resolved from the psyche's own report frames — report 26's frame quotes the
psyche: *"the new logics again… the whole engine rewrite thing"*; report 23
writes *"the new logics."* **"The new logic stack" = the new `lojix` deploy
stack (Stack B)** — the lean rewrite that replaces the production monolith
`lojix-cli`. This lane has audited it across reports 23–37.

## Why this audit is timely

The new stack was promoted to `main` across all three repos within days and
**today** (2026-06-10) received the commit `7d66d2e` *"lojix: materialize
horizon inputs for production eval."* The whole readiness arc is already on
`main`:

```
7d66d2e  materialize horizon inputs for production eval   ← HEAD, today
f9be5df  await generated Nexus runner directly
fe431dd  adopt actor-native daemon listener
c8c4353  bump triad-runtime + nota-next (core-crate refresh, intent tj99)
f78a20f  consume triad-runtime BoundedWorkers (intent k6w1)
ba39fbe  make the daemon concurrent — bounded thread-per-connection (intent 2alg)
f84a8cf  apply adversarial-audit fixes (audit 29)
5c0ee76  import schema-derived triad-port daemon crate (M1 build+evaluate)
```

## Audit target (live code on `main`, HEAD `7d66d2e`)

- New crate: `/git/github.com/LiGoldragon/lojix/triad-port/` — v0.3.0;
  `src/{client,daemon,lib,schema_runtime}.rs`, `src/bin/{lojix-daemon,lojix}.rs`,
  `schema/{nexus,sema}.schema`,
  `tests/{actor_native_runtime,build_smoke,engine_routing,horizon_materialization_contract}.rs`.
- Contracts: `signal-lojix/triad-port/`, `meta-signal-lojix/triad-port/`.
- Parity bar (production today): `lojix-cli` `main`.
- Engine deps: `triad-runtime`, `schema-next`, `schema-rust-next`, `nota-next`,
  `nota-codec`, `sema-engine`, `signal-frame`/`signal-core`, `horizon-rs`.

## Self-stated gates visible before opening the code

1. **Activate rejects.** ARCHITECTURE.md: build + horizon materialization work,
   but *"Activating deploys still reject until copy/activate is target-safe."*
2. **State is in-memory.** INTENT.md: the live generation set (the daemon's
   reason to exist — "what's running on every node") is in-memory; durable
   sema-engine backing is "the next storage cutover."
3. **Zero consumers migrated.** Both `CriomOS` and `CriomOS-home` flake.lock
   still pin legacy `lojix-cli`. The cutover hasn't begun.

## Method

Eight-dimension survey → adversarial verify (per dimension) → synthesis +
completeness critic, run as a background Workflow (`lojix-production-readiness`).
Each finder grounds findings in `file:line` / commit / report and **verifies
report claims against current source** (the prior reports span 06-04…06-07 and
may be stale). Production bar: "ready" means it can *replace* `lojix-cli` for
real node deploys — build **and** activate — durably, safely, with a consumer
migration path. Build-only is not production-ready for a deploy tool.

Dimensions: (1) deploy parity vs `lojix-cli`, (2) build/runtime health,
(3) durable state, (4) concurrency/non-blocking, (5) architecture discipline,
(6) wire-contract completeness, (7) engine-dependency freshness,
(8) cutover & intent gates.

Verified findings land in the numbered files in this directory; the synthesis
is the highest-numbered file.
