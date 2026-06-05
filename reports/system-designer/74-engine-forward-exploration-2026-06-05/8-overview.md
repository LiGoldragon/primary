---
title: 74.8 — Overview — engine-forward: the critical path + the start-porting-now set
role: system-designer
variant: Psyche
date: 2026-06-05
topics: [engine, orchestrate, persona, router, message, introspect, schema-daemon, triad-runtime, cloud, lojix, port-readiness, critical-path]
description: |
  Orchestrator synthesis of the engine-forward exploration (6 mappers + backlog +
  completeness/foundation critiques), corrected for the two psyche reframes
  (Orchestrate = the orchestrate COMPONENT; add router + message) and the critics'
  three load-bearing findings. The runner spine is the critical path and is further
  along than expected (triad-runtime landed; generated Nexus runner adapter landed;
  schema-rust-next green). A concrete SAFE-NOW start-porting set exists. The
  two-listener daemon is already in operator's working copy — do not rebuild.
---

# 74.8 — Overview: where to put effort to move the engine forward

Kind: psyche (orchestrator synthesis). Date: 2026-06-05.
Incorporates the completeness + foundation critiques and the two psyche reframes.

## The two psyche reframes, folded in

- **"Orchestrate" = the `orchestrate` component** (the orchestration component
  runtime), not the verb (`(Spirit Clarification tq18)`). The orchestrate component
  RUNS the set of daemons — persona (the manager), the introspector, the schema
  daemon, the others (`mazv`). Concretely: `orchestrate/src` has **ZERO supervision
  today**; `mind/src/supervision.rs` is the working template. Giving orchestrate the
  engine-management supervision surface is the orchestrate-component-forward move.
- **Add router + message.** The completeness critic independently flagged this as
  the #1 CRITICAL gap: router was mapped only as an introspect observation target;
  the **message → router delivery path** was never ported onto the runner. persona
  `src/engine.rs` already defines `MESSAGE_ROUTER_COMPONENTS` +
  `operational_delivery_components`, and a `PiMessageRouterSmoke` check exists —
  but neither `message` nor `router` consumes triad-runtime yet, and nothing
  asserts a live delivery round-trip under persona supervision.

## The critical path (verified against source)

The runner is the spine — and it is **further along than expected**: triad-runtime
is landed, the hardest `rpr5` claim (generated runner adapter) is LANDED for the
Nexus plane (`spirit/src/schema/nexus.rs:821-832` drives `triad_runtime::Runner`),
schema-rust-next is GREEN (HEAD `ec0678c`, 53 tests), triad-runtime `role.rs` is
committed. The "fix your own red tree" front-runners are already cleared.

Spine: (1) **two-listener daemon shell** in triad-runtime → (2) **per-area
first-consumer ports** (router/message delivery, cloud two-contract, introspect
witness, orchestrate supervision) → (3) **persona standing supervised topology** →
(4) `TriadComponent::serve` umbrella → (5) persona real Launch/Retire — the `mazv`
convergence (the running orchestrated system you want).

Note (1) is **already in progress**: triad-runtime's working copy carries an
uncommitted `MultiListenerDaemon`/`MultiListenerRuntime` implementation (+508 lines,
green tests, dated 14:14) — almost certainly operator's main work. **We do not
rebuild or touch it**; the per-area ports below use the *stable* 3-arg
`SingleListenerDaemon::new` signature and do not modify triad-runtime.

## The START-PORTING-NOW set (SAFE-NOW, corrected by the foundation critic)

All verified foundation-stable on 2026-06-05; none ports onto sand; none touches the
in-flight triad-runtime working copy:

| # | Port | Repo(s) | Size | Why safe / why now |
|---|---|---|---|---|
| P1 | **orchestrate gets engine-management supervision** (port the `mind/src/supervision.rs:157-176` template) | `orchestrate` | M | orchestrate has ZERO supervision today; mind is the proven template; the orchestrate-component-forward move you named |
| P2 | **message + router delivery path onto the runner** + a standing end-to-end delivery assertion under persona supervision | `router`, `message`, persona harness | M | your explicit ask + the #1 critical gap; persona already names the delivery components; uses stable `SingleListenerDaemon` |
| P3 | **persona → signal-introspect pin realign** (persona `Cargo.toml:35` still pins the old `signal-persona-introspect`; rename landed in signal-introspect `b8fdf67`+`152fc0e`) | `persona` | S | pure catch-up to a landed rename — a clean quick win |
| P4 | **orchestrated introspect witness test** (persona spawns real introspect + router; `router/src/observation.rs:38` answers live) | persona harness, `introspect` | M | both wire ends real; gated on P3; assert on decoded reply VALUES not frame bytes (introspect/router still on signal_core+Match — Layer-1 debt, item 21) |
| P5 | **persona standing full-stack runner** (health-tick + crash-restart, extending the already-green `persona/flake.nix:1815` topology check) | `persona` | M | the strongest existing asset — a real enabled check spawns the real persona-daemon |
| P6 | **lojix reconcile to signal-frame + daemon-shell adoption** (keep the Kameo tree behind it) | `lojix`, `signal-lojix` | M | kernel mismatch confirmed; the shell signature is stable |

## Pulled / deferred (do NOT port now)

- **Item 9 — self-host the macro table from core.schema → WAIT.** `core.schema` is
  entirely payload-less bare-variant enums, exactly what `primary-vllc` (operator-
  owned P1 dual-lowering bug) breaks; report 73 already concluded "wait on
  primary-vllc before relying on payload-less variant lowering." Scaffold-only at
  most.
- **Cloud effects/SEMA substance — PREP.** The two cloud wire contracts are frozen
  and the schema_runtime test is green, but the engine substance is gated on the
  two-listener shell + sema-engine persistence. Cloud is the psyche-emphasized first
  TWO-contract consumer, but it follows the shell, not precedes it. Build the cloud
  engines once the shell lands.
- **Anything gated on:** sema-engine emit (signal-core persistence), the Signal
  accept-bridge hook-split, the meta-policy plane shape (`7x50`), the signal-frame
  Layer-1 macro, `primary-vllc`, hash-identity.

## Added (completeness critic, major)

- **The upgrade triad.** `upgrade/Cargo.toml` already depends on triad-runtime,
  schema-next, schema-rust-next, sema-engine, signal-frame; it has handover.rs /
  event.rs / execution.rs + signal-upgrade. The persona FD-handoff cutover is the
  runtime side of the same version-handover concern. Assess + finish its runner
  adoption; surface the persona-cutover dependency. (Not in the first wave.)

## What I'm executing first

The two ports that match your emphasis and are clean SAFE-NOW: **P1 (orchestrate
supervision)** and **P2 (message + router delivery path)** — plus **P3 (persona pin
realign)** as a zero-risk warm-up. All on `~/wt` feature branches (designer
discipline), build + test to green, NOT touching the in-flight triad-runtime
working copy. Cloud follows the two-listener shell.

## See also

- `7-prioritized-backlog.md` — the full ranked backlog + critical-path detail.
- `1-cloud.md` … `6-deploy-and-pilot.md` — the area maps.
- `0-frame-and-method.md` — the frame.
