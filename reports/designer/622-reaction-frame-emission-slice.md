# Reaction-frame emission slice — Part 1 done + proven, Part 2 split

Branch `next/reaction-frame-emission` in schema-rust-next (worktree
`~/wt/github.com/LiGoldragon/schema-rust-next/reaction-frame-emission`),
two commits, pushed; main untouched.

- `181d7ee` — Part 1: emit the shared generic reaction frame.
- `19fffd9` — Part 2a: emit spirit's frame application; cascade-stop on 2b.

## What landed

### Part 1 — generic frame data enums (complete, proven)

`reaction.schema` (the parameterized frame) now emits exactly the
prototype shape:

```rust
#[cfg_attr(feature = "nota-text", derive(nota_next::NotaDecode, nota_next::NotaEncode))]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub enum Work<Event, WriteDone, ReadDone, EffectDone> { … }

pub enum Action<Reply, Write, Read, Effect, Continuation> { … }
```

No bound attributes (no `omit_bounds`, no `#[rkyv(…)]`, no explicit
`where`) — rkyv 0.8 + nota-next auto-synthesise per-parameter bounds, as
the #408 prototype proved. The schema emits the generic DATA enums only;
the frame BEHAVIOUR (`drive`, `From<Action> for NextStep`) stays
hand-written in triad-runtime (the single-source-of-truth decision).

Mechanism added to the emitter:

- `RustDeclaration`/`RustEnum` carry `parameters: Vec<Name>`, lowered
  from the schema `Declaration` head; `RustGenericParameterTokens` emits
  the `<P…>` list after the type name.
- `TypeReference::Application { head, arguments }` (the new schema-next
  generics node) is handled across `rust_type`, both token renderers
  (`RustTypeReferenceTokens`, migration `TypeRenderer`), and the
  bytes / fixed-bytes / map-key / private-type walkers.
- `Root` is now the `Enum | Application` sum: root lowering filters enum
  roots into `root_enums`; a new `RustAppliedRoot` models the
  `(Head Arg…)` application-form root and emits `pub type <pos> = …`.
- Parameterized enums skip auto-generated variant constructors and
  payload-`From` impls (those would name undeclared binders; the frame's
  constructors live in triad-runtime).

Proof: `tests/reaction_frame_emission.rs` emits the frame with the
`DeclarationModule` target, asserts the exact two-enum shape + absence of
bound attributes / wire enums / runtime support, compiles the generated
module, and rkyv-round-trips a concrete `Work<String, u64, bool, i32>`.

### Part 2a — spirit's frame application (complete, proven)

`spirit-nexus.schema` imports `Work`/`Action` from the reaction frame and
applies them at the root positions. Emission (NexusRuntime target)
produces:

- spirit's payload enums (`SemaWriteSet`, `EffectCommand`,
  `EffectOutcome`, signal `Input`/`Output` payloads, the SEMA structs);
- `pub use reaction::schema::reaction::{Work, Action}` import aliases;
- frame-application aliases
  `pub type Input  = Work<SignalInput, SemaWriteOutput, SemaReadOutput, EffectOutcome>;`
  `pub type Output = Action<SignalOutput, SemaWriteSet, SemaReadInput, EffectCommand, Work<…>>;`
- **no** concrete `NexusWork`/`NexusAction` enum body and **no**
  `into_next_step` shim.

Note the alias names are `Input` / `Output` (the schema's two root
position names), not `Work` / `Action` as the prompt's older Nexus-plane
framing expected — but they bind the same payloads at the same legs, so
the intent ("frame application at root positions, not a concrete body")
is met. `Input` *is* spirit's applied `Work`; `Output` *is* its applied
`Action`. The application head resolves through the import to the generic
`Work` / `Action` in scope.

Proof: `tests/spirit_frame_application.rs` emits spirit over the resolved
reaction dependency, `include!`s the 2691-line generated module over a
local `reaction::schema::reaction::{Work, Action}` stand-in (the proven
derive stack), asserts the aliases + absence of concrete body / shim, and
rkyv-round-trips a spirit `Work` value (the `Input` alias) on two legs.

## Part 2b — STOPPED at the cascade. Why, exactly.

Two coupled deletions the prompt lists (delete `into_next_step` shim;
re-point the runner to drive via `From<Action> for NextStep`) do NOT fit
in this slice. The static-grep site list materially undercounts; the real
blast radius:

1. **`nexus_runner_shape` reads the concrete enum, which no longer
   exists.** It derives the runner's associated types from
   `NexusWork`/`NexusAction` *variant payloads* (`lib.rs:6143`). Under the
   frame model those payloads live in the applied-root *arguments*
   (`RustAppliedRoot` for `Input`/`Output`), not in a local enum
   declaration. Re-pointing means re-deriving the shape from applied
   roots — a rewrite, not a name swap.

2. **Role-trait impls become orphan-rule violations.**
   `push_role_trait_impl_if_local_role_type` emits
   `impl triad_runtime::NexusWork for NexusWork` etc. (`lib.rs:5491`).
   With `Work`/`Action` now *imported* foreign generics, a per-component
   `impl ForeignTrait for ForeignType` is an orphan violation. The impls
   must move to triad-runtime — which is exactly the "frame behaviour is
   hand-written in triad-runtime" decision, and the `From<Action> for
   NextStep` projection the prototype already put there.

3. **The runner adapter constructs via concrete inherent constructors.**
   `NexusRunnerAdapterTokens` calls `NexusWork::sema_write_completed(o)`,
   `NexusAction::reply_to_signal(r)`, `.with_origin_route(…)`,
   `.into_root()` (`lib.rs:2085-2215`). A `pub type Input = Work<…>`
   alias carries none of those — they were emitted onto the concrete
   enum. Re-pointing means rebuilding the adapter against the generic
   frame's variants + the triad-runtime-owned behaviour.

4. **Deleting the shim breaks every still-concrete schema.** Three
   fixtures — `plane-triad.schema`, `runner-triad.schema`,
   `driver-runtime/schema/nexus.schema` — still declare concrete
   `NexusWork`/`NexusAction`, and `runner_generated.rs` (62
   `into_next_step`/`Nexus*` references) plus `emission.rs` and
   `generation_driver.rs` assert the shim. The shim's `into_next_step`
   can only be replaced by `From<NexusAction> for NextStep`, which
   triad-runtime can provide *only* for the generic frame `Action`, not
   for a concrete per-component `NexusAction`. So the shim deletion is
   coupled to migrating every concrete component to the frame — i.e. the
   step-7 14-component fan-out. Deleting it now strands those three
   schemas.

The shim deletion + runner re-point is therefore correctly **blocked on
the step-7 migration**, not a standalone designer change. Doing it here
would balloon into rewriting `nexus_runner_shape`, the runner adapter,
the role-trait emission, three concrete fixtures, and their committed
generated artifacts + tests.

## Dependency seam (operator drops on integration)

`Cargo.toml` carries two `# DESIGNER-PROTOTYPE SEAM` `[patch]` entries:
`nota-next` → `pascal-head-body-shape` worktree (step-1), `schema-next` →
`schema-generics` worktree (step-5, HEAD `5feccb60`). The chain resolves
and builds; operator integrates schema-next + nota-next to their mains
and removes the patches.

One upstream-driven fixture change: `families_generated.rs`' pinned
family-identity blake3 hashes moved (the new schema-next computes the
family closure content hash over the changed schema model). The emitter
faithfully re-pins; I regenerated the fixture. No emission-logic cause.

## Toolchain note

Built under `rust-minimal-1.95.0` (the worktree's `rust-toolchain.toml`).
`cargo test`, `cargo clippy --all-targets -- -D warnings`,
`cargo fmt --check` all clean on what landed; no scoped `#[allow]` for
pre-existing lints was needed.

## Handoff for step-7 / the runner re-point

When the 14 components migrate to the frame, the runner re-point becomes
tractable as one move: read the runner shape from applied roots; delete
`NexusRunnerNextStepProjectionTokens` and re-point `decide_next_step` to
`triad_runtime::NextStep::from(action)`; move the role-trait impls into
triad-runtime (the prototype's `From<Action> for NextStep` is the seam);
migrate the three concrete fixtures and regenerate their artifacts. That
is the mechanical operator integration the prompt anticipated — now
de-risked by Parts 1 + 2a proving the data + application shapes compile
and round-trip.
