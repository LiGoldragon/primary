---
title: 514 — The three-plane split emits no SignalEngine
role: designer
variant: Psyche
date: 2026-06-04
topics: [runtime, runner, signal, nexus, sema, schema-rust-next, spirit, port-readiness]
description: |
  In the three-plane split, no emission target produces SignalEngine, so a
  daemon that implements SignalEngine cannot leave ComponentRuntime. The
  unresolved tail of the Signal-triage-in-the-runner question, now concrete.
  Verified live against the operator's latest generator.
---

# 514 — The three-plane split emits no SignalEngine

## The fact

`schema-rust-next`'s `RustEmissionTarget::runtime_planes()`:

| Target | runtime_planes() |
|---|---|
| `WireContract` | `none()` |
| `ComponentRuntime` | `all()` (signal + nexus + sema) |
| `NexusRuntime` | `nexus_only()` |
| `SemaRuntime` | `sema_only()` |

`SignalEngine` emission is gated on `runtime_planes().emits_signal()`
(`src/lib.rs:1991`, `:2011`), which is true **only for
`ComponentRuntime`**. The three-plane split is
`signal.schema = WireContract`, `nexus.schema = NexusRuntime`,
`sema.schema = SemaRuntime` — `emits_signal()` is false across all
three, so **no `SignalEngine` is emitted anywhere in the split**. The
split emits `NexusEngine` (from `nexus`) and `SemaEngine` (from
`sema`); `SignalEngine` exists only in the `ComponentRuntime` all-in-one.

The daemon implements it: `impl SignalEngine for SignalActor`
(`spirit/src/engine.rs:208`) for admission, triage
(`Signal<Input> -> Nexus<Input>`), and reply
(`Nexus<Output> -> Signal<Output>`) — and still does *after* the runner
cutover (`d4dbc179`). So removing the `ComponentRuntime` module and
rewiring the daemon onto the three planes deletes the trait the daemon
depends on. That is the blocker. It is why spirit is still
`ComponentRuntime` — that target is the only one that emits a complete
engine set, so it is the only one that produces a buildable daemon.
Not an operator oversight; the only complete option today.

## Why it exists — the unresolved tail of the Signal question

This is the same `SignalEngine` question from the runner design (513 /
509), now forced into the open by the split. The contract is wire-only
(`WireContract`, zero engines — the `2593` decision). The two daemon
planes are `NexusRuntime` (decide) and `SemaRuntime` (apply/observe).
Nothing in that set carries the daemon's wire-handling engine — triage
and reply. In `ComponentRuntime` it was emitted because the single
target emits everything; the split has no plane that owns it.

We answered "the contract emits no engine, all engines live in the
daemon" but never answered **which daemon plane owns Signal triage/reply**
once Signal is split off as a wire-only contract. That gap is this bug.

## The two resolutions

**(A) `NexusRuntime` also `emits_signal`.** Make the daemon-runtime
plane carry triage + reply + decide — `SignalEngine` + `NexusEngine`
emitted from `nexus.schema`. `nexus.schema` already imports the
contract's `Input`/`Output`, so it has exactly what triage/reply need.
`runtime_planes()` for `NexusRuntime` becomes signal+nexus. Smallest
change; keeps `SignalEngine` as a generated trait the component
implements (admission/validation stays component logic).

**(B) The runner absorbs triage.** The accept loop does
decode → `Nexus<Input>`; `SignalActor::admit` becomes a runner-level
admission/validation hook the component supplies; the `SignalEngine`
trait retires entirely. This is the direction the runner cutover
started (it moved `decide` to a single step and deleted the recursive
loop) but stopped short of — it kept `SignalEngine`. Finishing it
means deleting `impl SignalEngine for SignalActor` and moving its body
to the runner's accept path + a typed admission hook.

**Lean: (B).** It removes a trait instead of relocating one, and it is
the consistent end-state for the runner (the runner owns wire ingress;
the component owns decide/apply/observe + admission policy). But it is
coupled to the runner, so it is an operator + designer call, not a
unilateral one.

Until one of these lands, no daemon that implements `SignalEngine` can
leave `ComponentRuntime`.

## Verified live (re-checked while writing)

- `schema-rust-next` `d973ae17` (latest): `runtime_planes()` map
  unchanged; `SignalEngine` still `ComponentRuntime`-only. The latest
  generator change was SEMA-side ("accept plane-local sema runtime
  roots"), unrelated.
- `spirit` `d4dbc179` (latest): still `impl SignalEngine for SignalActor`.
- Tracked: bead `primary-jfko`.

## How it surfaced

The branch's `cargo check` passed at first — but only because
`src/schema/lib.rs` (`ComponentRuntime`) was still present and supplied
`SignalEngine`; the three plane modules compiled *alongside* it, not
*instead of* it. The split lowers and emits; it does not produce a
daemon that builds without the all-in-one module. That distinction is
only visible by building it, not by inspecting the schema.
