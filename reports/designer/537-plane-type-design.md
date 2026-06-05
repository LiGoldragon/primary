---
title: 537 — PlaneType design — promoting the implicit plane axis to a first-class noun
role: designer
variant: Decision
date: 2026-06-05
topics: [schema-rust-next, plane-type, plane-projection, token-lowering, noun-owned, runtime-emitter, engine, design]
description: |
  The design that unblocks the runtime-half token migration. Promote the
  implicit plane axis (three bools in RuntimePlaneSet + the *Runtime target
  variants + smeared inline conditionals) into TWO first-class nouns — Plane
  (the node: per-plane naming) and PlaneProjection (the edge: cross-plane
  transforms) — that the runtime construct nouns consult while owning their
  own tokens. Grounded in a two-survey catalog of all ~26 runtime emit
  methods (reports captured below).
---

# 537 — PlaneType design

## The problem (grounded)

The runtime half of `schema-rust-next/src/lib.rs` generates Rust through a
god-struct `RustWriter` (lib.rs:1836) — ~26 `emit_*` methods doing
`self.line(format!(...))`. The blocker for moving these onto self-rendering
nouns (`4np2`/`de8i`/`0bw0`) is that **plane** is not a thing — it is an
un-named axis represented three ways at once:

1. `RuntimePlaneSet { signal: bool, nexus: bool, sema: bool }` (lib.rs:435) —
   three bare bools + parallel `emits_signal/nexus/sema/all` methods.
2. `RustEmissionTarget::{SignalRuntime, NexusRuntime, SemaRuntime}` — the
   per-plane daemon targets.
3. Inline `signal/nexus/sema` conditionals and magic strings smeared across
   every `emit_*` method (module names, wrapper paths, trace enum names,
   engine trait names, alias sets).

Move the methods onto nouns naively and each noun re-inlines the same plane
conditionals — one god-struct becomes 26 small ones. The fix (`de8i`):
cross-object logic that belongs to no single noun becomes its own named type
the nouns consult.

## The design: two nouns, not one

The survey of all 26 methods shows the plane logic is a small **graph**, so it
needs two types:

### `Plane` — the node

```rust
enum Plane { Signal, Nexus, Sema }
```

Owns the plane-*intrinsic naming* — pure `&self` constants, no schema or
target needed. These are exactly the magic strings the surveys found smeared
across `emit_plane_namespaces`, `emit_trace_support`, `emit_mail_event_support`,
and `emit_schema_plane_trait_support`:

| Method | Returns (Signal / Nexus / Sema) |
|---|---|
| `module_name()` | `signal` / `nexus` / `sema` |
| `wrapper_name()` | `Signal` / `Nexus` / `Sema` |
| `wrapper_path()` | `signal::Signal` / `nexus::Nexus` / `sema::Sema` (= `{module}::{wrapper}`) |
| `envelope_name()` | the per-plane mail envelope struct name |
| `trace_enum_name()` | `SignalObjectName` / `NexusObjectName` / `SemaObjectName` |
| `trace_prefix()` | `Signal` / `Nexus` / `Sema` |
| `engine_trait_name()` | `SignalEngine` / `NexusEngine` / `SemaEngine` |
| `alias_names()` | `[Input,Output,Signal]` / `[Work,Action,Nexus]` / `[WriteInput,WriteOutput,ReadInput,ReadOutput,Sema]` |
| `canonical_source_type_names()` | `[Input,Output]` / `[NexusWork,NexusAction]` / `[SemaWriteInput,…]` |

### `PlaneProjection` — the edge

The three projection methods (`emit_split_nexus_work_projection` 3440,
`emit_nexus_action_projection` 3526, `emit_split_sema_output_projection` 3573)
are **directed plane-pair** facts, not single-plane — a `Plane` enum cannot
answer them. They become an edge noun:

```rust
enum PlaneProjection {            // directed edges that actually exist
    NexusWorkToNexusAction,
    NexusActionToSemaWrite,
    NexusActionToSemaRead,
    NexusActionToSignalOutput,
    SemaOutputToNexusWork,
}
```

`PlaneProjection` owns the edge identity and the two wrapper paths (via
`from.wrapper_path()` / `to.wrapper_path()`); the per-variant **mapping** is
schema content and stays on the projection construct noun.

## What stays OFF the plane nouns (the survey's `[+]` flags)

Three classes of decision look plane-ish but are not, and must NOT be absorbed
— putting them on `Plane` would just relocate the smear:

1. **Target-set questions** — "is this plane emitted?" and "are ALL planes
   emitted?" depend on the active set, not a single plane. Stay on
   `RuntimePlaneSet` / `RustEmissionTarget`. (`emits_all_runtime_planes` gates
   the cross-plane `schema::Plane` enum, `MessageRoot` placement, and the
   plane-projection block.)
2. **The `SignalRuntime` concreteness special-case** (lib.rs:2810, 3844,
   4010) — a signal-only daemon emits a *different* `SignalEngine` shape than
   an all-in-one runtime. This consults the concrete `RustEmissionTarget`
   variant, not the plane. Stays on the target.
3. **Plane + construct-presence** — role-trait names (plane × role-position),
   actor-variant trace labels (plane × which roots exist), route-type
   membership (plane × construct-name), sema sub-roles (sema × write/read
   presence). `Plane` supplies the name-set; the noun passes the schema roots
   in. These are `Plane` methods that *take roots as a parameter*, or live on
   the noun composing `Plane` with its own data.

So the rule is three tiers: **`Plane`/`PlaneProjection` own naming + edges;
the construct nouns own the construct and compose; `RustEmissionTarget`/
`RuntimePlaneSet` own which-planes-and-which-target.**

## The noun decomposition (where each method lands)

- **Holds a `Plane`** (per-plane construct): `PlaneEnvelopeTokens`,
  `PlaneNamespaceTokens` (one per plane, orchestrated over the active set),
  `PlaneOriginRouteConstructorTokens`, the per-plane trace `ObjectName` enum,
  the per-plane engine-trait noun (`SignalEngineTraitTokens` etc.).
- **Holds a `PlaneProjection`** (edge construct): `SplitNexusWorkProjectionTokens`,
  `NexusActionProjectionTokens`, `SplitSemaOutputProjectionTokens`.
- **Plane-agnostic** (already the target shape, or pure boilerplate):
  `SignalFrameStreamingSupportTokens`, `NexusRunnerAdapterTokens`,
  `NexusRunnerNextStepProjectionTokens` (these already delegate to `*Tokens`
  nouns and consume a pre-resolved `NexusRunnerShape` — the plane work for
  them is *upstream*, in building the shape, not in the emitter);
  `RouteEnumTokens`, `RouteImplTokens`, `UpgradeSupportTokens`,
  `ActorLifecycleSupportTokens`, `ShortHeaderModuleTokens`.
- **Cross-plane orchestrators** (consume the whole active set):
  `SchemaPlaneSupportTokens` (the `schema::Plane` enum), `TraceSupportTokens`,
  `MailEventSupportTokens`, `PlaneProjectionSupportTokens`.

Secondary cleanup this enables: re-express `RuntimePlaneSet` as a set *of*
`Plane` (`emits(plane: Plane) -> bool`) instead of three parallel bools —
collapsing representation #1 above into the new noun.

## Migration approach — one reference family first

Per the designer/operator split: I prototype **one** family end-to-end in a
`~/wt` worktree as the canonical pattern; the operator applies it across the
rest on main. The chosen reference is **`emit_plane_namespaces`** (lib.rs:3090)
→ `PlaneNamespaceTokens` — it is the single richest concentration of plane
naming (module name + alias set + source-type names) AND it exercises the
three-tier composition (tier-1 `Plane` naming + tier-3 presence gating via
`has_type`/`has_root_enum`). It is the best worked example of "a runtime
construct becomes a self-rendering noun holding a `Plane`." The already-migrated
delegating nouns (`SignalFrameStreamingSupportTokens`,
`NexusRunnerAdapterTokens`) confirm the target shape.

## Flagged for a decision (not silently resolved)

- **`emit_signal_frame_support` is plane-UNGATED** (lib.rs:2410, called
  unconditionally at render:275) while every other signal construct is gated
  by `emits_signal()`. So a `NexusRuntime`/`SemaRuntime`/`WireContract` target
  still gets signal-frame code today. Either intentional (frames are always-on
  wire support) or a latent bug. The `Plane` design surfaces it; it needs an
  explicit call before the migration freezes the behavior.
- **Preserve the wire-contract gate**: "wire-contract emits no role impls" is
  the orchestrator gate at lib.rs:276 (`emits_runtime_support()`), not a
  per-method branch. The noun migration must keep that call-site gate, not
  push it into a noun.
- **Dead param**: `emit_split_sema_output_projection`'s `type_name` is unused
  (lib.rs:3581, `let _ = type_name;`) — drop on migration.
- **ZST discipline**: `UpgradeSupportTokens` / `ActorLifecycleSupportTokens`
  carry no data (fixed boilerplate). Per workspace rule they must hang off a
  real owning noun or be a const template, not a ZST namespace.

## Provenance

Grounded in two designer-lane survey passes over all ~26 runtime `emit_*`
methods (plane/runner/projection group; role/engine/lifecycle group), each
anchored to `schema-rust-next/src/lib.rs` file:line. Captured as intent: the
`Plane` + `PlaneProjection` decomposition.

## Implementation status — reference family landed (2026-06-05)

The reference family is **implemented, verified, and pushed** on branch
**`designer-plane-type-2026-06-05`** in `schema-rust-next` (off `main@origin`
`fa0d4fa2`). Scope of this branch:

- **`Plane { Signal, Nexus, Sema }`** with the five naming methods the first
  family needs (`module_name`, `wrapper_name`, `wrapper_path`, `alias_names`,
  `canonical_source_type_names`) — pure `&self` constants, no target/schema
  logic (adversarially grep-verified clean).
- **`PlaneNamespaceTokens` / `PlaneNamespaceAlias` / `PlaneOriginRouteConstructorTokens`**
  — the `emit_plane_namespaces` family migrated to self-rendering `ToTokens`
  nouns via `quote!`, consulting `Plane`. `RuntimePlaneSet::active_planes()`
  added (additive; the three bools unchanged).
- **Signal-frame gating** (`gb95`): `emit_signal_frame_support` now wrapped in
  `if writer.emits_signal()` — nexus/sema/wire targets lose it (157 lines
  each), pinned by absence-assertions in the nexus + sema + wire tests.

Verified: `plane_namespaces` output **byte-identical** (golden snapshots +
an independent old-vs-new dump across all three planes); the only intended
output change is the signal-frame gating; `cargo build` + `test` (54) +
`clippy -D warnings` green from a clean rebuild; three-tier design and
rust-discipline confirmed by adversarial verifiers.

**Operator handoff:** this branch is the canonical pattern for the rest of the
runtime token migration. Adopt `Plane` (grow its methods per family —
`trace_enum_name`, `envelope_name`, `engine_trait_name` land as the trace /
mail / engine-trait families migrate) and introduce `PlaneProjection` when the
projection methods (`emit_split_nexus_work_projection` etc.) migrate. Either
rebase `main` onto the branch or cherry-pick the pattern. Not yet integrated to
`main` — operator owns that.

**Deferred** (noted, not silently dropped): `PlaneProjection` + the other ~25
families; the `RuntimePlaneSet`-as-set-of-`Plane` secondary cleanup; the dead
`type_name` param in `emit_split_sema_output_projection`.

Per psyche 2026-06-05 ("ok lets design it" → "ok implement this").
