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

## SUPERSEDED — resolved by `RustEmissionTarget::SignalRuntime` (see report 515)

This report correctly witnessed a real blocker: with `WireContract` +
`NexusRuntime` + `SemaRuntime` and the old `src/schema/lib.schema`
removed, nothing emitted `SignalEngine`. That diagnosis stands as the
bug witness.

**Its solution space was too narrow.** The landed answer is neither
**(A)** "`NexusRuntime` also emits signal" nor **(B)** "the runner
absorbs triage and `SignalEngine` retires" — both of which this report
weighed, and it leaned (B). The real answer is **(C)**: a separate
daemon-local **`SignalRuntime`** emission target. The daemon's own
`schema/signal.schema` emits to `SignalRuntime` (`signal_only()` planes)
and produces `SignalEngine`, while public contract repos keep emitting
to `WireContract` (wire-only). The current architecture is
**`SignalRuntime` + `NexusRuntime` + `SemaRuntime`** — NOT
`ComponentRuntime`, and NOT `NexusRuntime`-emits-signal.

**Why this report only saw A/B:** it collapsed two distinct artifacts
both called "the signal schema" — the public `signal-<component>`
**contract** (`WireContract`, zero engines) and the daemon-local
`<component>/schema/signal.schema` **runtime** (`SignalRuntime`, emits
`SignalEngine`). Keeping those distinct makes (C) obvious; conflating
them hides it. My (B) lean was wrong: keeping `SignalEngine` a
generated, plane-local trait is the smaller, more plane-honest move
than dissolving the typed seam into the runner. The two-meanings
distinction is now in `skills/component-triad.md` §"'Signal' names two
different schema files".

Verified landed on spirit main: `RustEmissionTarget::SignalRuntime`
(`schema-rust-next/src/lib.rs:300`), `spirit/build.rs:32`
(`signal_runtime_module("signal")`), `lib.schema` gone, `cargo check`
clean, `SignalEngine` impl at `spirit/src/engine.rs:209`. Full
resolution + workspace-wide boundary verification: **report 515**.

The original analysis follows unchanged, as the bug witness.

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
