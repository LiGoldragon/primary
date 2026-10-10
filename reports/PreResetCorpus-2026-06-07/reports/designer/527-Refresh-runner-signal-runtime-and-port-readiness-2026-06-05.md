---
title: 527 — Refresh — shared triad runner, SignalRuntime, wire-only boundary, port readiness
role: designer
variant: Refresh
date: 2026-06-05
topics: [runtime, runner, triad-runtime, signal, nexus, sema, wire, contract, schema-rust-next, spirit, signal-runtime, port-readiness, component-triad]
description: |
  Agglomerated current-state surface for the runner / SignalRuntime / wire-only
  thread. Merges designer 509 (contract-is-messaging-only), 510 (wire-only
  boundary workspace audit), 511 (triad-engine + schema-stack port readiness),
  512 (spirit plane-schema split exemplar), 513 (shared triad runner design),
  514 (no-SignalEngine-emission-home blocker), 515 (SignalRuntime resolution).
  Most of this thread's design substance has already matured into
  skills/component-triad.md (the WireContract/SignalRuntime boundary, the
  three-plane split, the triad_main! runner loop, the Nexus substrate); this
  Refresh names those landings and carries the residual working-artifact
  substance — the wire-only audit finding, the port-readiness state, and the
  bootstrap-split exemplar.
---

# 527 — Shared triad runner, SignalRuntime, wire-only boundary — current state

The current canonical surface for the thread covering how a daemon gets its
runner for free, where `SignalEngine` is emitted from, and the wire-only
contract boundary. Agglomerates designer reports 509–515.

**Most of this thread's design substance has already landed in
`skills/component-triad.md`** — the migration witness. This Refresh names those
landings and carries the residual working substance the skill does not hold (the
moment-tied audit finding, the port-readiness snapshot, the bootstrap exemplar).

## What already migrated into `skills/component-triad.md`

The skill is the permanent home; these reports' design substance lives there now:

- **The wire-only contract boundary** (reports 509/510). `skills/component-triad.md`
  §"Signal names two different schema files": the public signal contract
  (`signal-<component>`) emits to `WireContract` — **wire vocabulary + codecs
  ONLY, zero engines**. Nexus (decisions) and SEMA (storage) are daemon-internal
  runtime planes that must NOT be derived from the contract. That IS report 509's
  finding ("a signal contract is purely the wire vocabulary; the generator
  wrongly derives Sema and Nexus from it") as a permanent rule.
- **The SignalRuntime resolution** (report 515). Same skill section, lines 28–46:
  `SignalEngine` is generated from the daemon's OWN `schema/signal.schema` via the
  `SignalRuntime` target, never from the public contract. "Signal schema" names
  two distinct files (public `WireContract` vs daemon-local `SignalRuntime`). The
  skill cites report 515 by name as the designer landing witness.
- **The three-plane split + five emission targets** (reports 512/514). Same skill:
  `WireContract`, `ComponentRuntime` (legacy all-in-one), `SignalRuntime`,
  `NexusRuntime`, `SemaRuntime`; a daemon emits `signal.schema`→`SignalRuntime`,
  `nexus.schema`→`NexusRuntime`, `sema.schema`→`SemaRuntime`, dropping the
  all-in-one `ComponentRuntime`. The no-emission-home blocker report 514 raised
  is resolved here (and 514 already carried its own supersession note pointing at
  515).
- **The shared triad runner** (report 513). `skills/component-triad.md`
  §"Nexus mechanism substrate" + §"Lifecycle hooks": the NexusWork/NexusAction
  asymmetric pair + 5-variant action set (ReplyToSignal, CommandSemaWrite,
  CommandSemaRead, CommandEffect, Continue); the macro-generated runner loop
  (`triad_main!` emitted from schema-rust-next); Continue as in-process immediate
  recursion; effects per-component declared in schema; cross-component invocation
  through Signal contracts not Nexus-internal access; the two lifecycle hooks as
  the minimum supervision surface; component code becomes a one-line `main`. That
  is report 513's full design as the canonical mechanism.

## Residual working substance — carried, not yet permanent

### The wire-only boundary violation is CONFINED, not universal (audit, 510)

The psyche escalated a cloud finding to a workspace question: is the
contract-carries-only-wire-vocabulary violation everywhere, or confined?
**Answer: CONFINED.** 43 contract surfaces audited; only **3** leak
engine/Sema/Nexus into the contract — **spirit, signal-upgrade,
meta-signal-upgrade** — and all three share one cause: they are the only
contracts emitted by schema-rust-next, whose single all-in-one emission path
(`ComponentRuntime`) was built for spirit's single-repo (contract == daemon)
shape and copies that fused emission onto the upgrade contracts. The fix is the
emission-target split (above, now in the skill): emitting the upgrade contracts
through `WireContract` instead of `ComponentRuntime` removes the leak. This is an
audit finding tied to the 2026-06-04 moment; it retires when the three contracts
re-emit through `WireContract` and the leak is verified gone.

### The spirit plane-schema split is the bootstrap-exception exemplar (512)

Splitting spirit's all-in-one `schema/lib.schema` (Signal + Nexus + SEMA roots
fused in one `ComponentRuntime` document) into three separate plane-schema files,
each emitted with its own target, is **the clean bootstrap-exception exemplar
every future triad port copies** — the simplest possible shape: one signal
contract, two daemon plane files, no owner/meta leg. The split is what the
`SignalRuntime`/`NexusRuntime`/`SemaRuntime` targets realize per component. The
NOTA schema source for each file was drafted in the predecessor report; the
build.rs migration and Rust regeneration are the driver's job (operator).

### Port-readiness state (audit, 511)

The triad-engine + interface-schema substrate was assessed for "are we stable
enough to port all components properly?" As of the 2026-06-04 audit the substrate
had moved far enough that multi-plane loading + cross-plane import had landed, and
the canonical worked example is `spirit-next` (NexusEngine + SemaEngine
schema-emitted; SignalEngine in the runtime substrate). The remaining gating
work for broad porting is the emission-target split being applied per component
(above) and the Asschema removal (report 526). This is an audit snapshot; it
retires once the porting waves begin against the settled substrate.

## Open / coordination items

- **Apply the emission-target split to the three leaking contracts**
  (spirit/signal-upgrade/meta-signal-upgrade) so the contracts emit through
  `WireContract` and the engine-leak closes. Operator-territory (schema-rust-next
  + the component repos on main).
- **The broad component-porting waves** wait on the settled substrate: the
  emission split applied per component + Asschema removal (report 526). Designer
  drafts the per-component plane-schema sources; operator owns the build.rs
  migration and integration to main.

## Lineage

- **Source reports absorbed:** 509 (contract-is-messaging-only), 510 (wire-only
  boundary audit — CONFINED to 3 contracts), 511 (port-readiness), 512 (spirit
  plane-schema split exemplar), 513 (shared triad runner design), 514
  (no-SignalEngine-emission-home blocker, resolved by 515), 515 (SignalRuntime
  resolution). git history holds each predecessor.
- **Permanent landings:** `skills/component-triad.md` §"Signal names two
  different schema files" (wire-only boundary + SignalRuntime + five emission
  targets), §"Nexus mechanism substrate" + §"Lifecycle hooks" (the runner /
  NexusWork-NexusAction substrate / `triad_main!`), and the runtime-triad section
  generally. The canonical worked example is `spirit-next/ARCHITECTURE.md`.
