# 185 — schema crystallization implementation

## Frame

Input:

- `reports/designer/341-schema-crystallizes-architecture-2026-05-25.md`
- Spirit records 656-664, especially:
  - 657: extended headers preserve the 8-byte prefix.
  - 659: components have two schema-derived vocabularies, wire and effect.
  - 660: internal interactions flow through an interact trait and mediator.
  - 661: schema declares closed effect-table dispatch.
  - 662: actor execution produces fan-out output sets.

This was an operator implementation slice in `signal-frame`, not a schema
syntax redesign. The current schema crate does not yet expose an authored
effect-table section, so the implementation derives a first closed effect
table from the already-assembled route graph. That is intentionally the
smallest real step: code now has the runtime shape that later schema syntax
can feed explicitly.

## What landed

Repository: `/git/github.com/LiGoldragon/signal-frame`

Files:

- `schema-rust/src/lib.rs`
- `tests/emit_schema.rs`
- `ARCHITECTURE.md`
- `README.md`
- `macros/README.md`
- `skills.md`

The `schema-rust` composer now emits these additional surfaces from
`AssembledSchema`:

- `ExtendedHeader`
  - 256-byte fixed header.
  - byte 0..8 is the normal `signal_frame::ShortHeader`.
  - `route_for_extended_header` delegates through the preserved prefix.
- `Interact<Input>`
  - generated trait contact point for schema-derived internal dispatch.
- `InteractionActor<Input>`
  - generated marker trait for the mediator actor shape.
- `Effect`
  - internal effect vocabulary derived from ordinary routes.
- `EffectTable`
  - closed `Operation -> Effect` mapping.
- `FanOut` / `FanOutOutput`
  - closed output-kind scaffold for effect, reply, and event fan-out.
- Parallel owner/sema names when those legs have routes:
  - `OwnerEffect`, `OwnerEffectTable`, `OwnerFanOut`
  - `SemaEffect`, `SemaEffectTable`, `SemaFanOut`

## Generated Shape

For the current fixture:

```text
Operation::State(StateEndpoint::Declaration(Declaration))
  -> EffectTable::effect_for_operation
  -> Effect::State(StateEffect::Declaration(Declaration))
  -> FanOut { outputs: [FanOutOutput::Effect(...)] }
```

That is the first concrete route-to-effect-to-fanout path from `/341`.
It is not yet the final authored effect table. It is the generated runtime
shape the final authored table will target.

## Tests Added

`tests/emit_schema.rs` now proves generated code is usable, not just present:

- `emit_schema_generates_prefix_preserving_extended_header_projection`
  constructs an `ExtendedHeader`, verifies the first eight bytes equal the
  original `ShortHeader`, and routes through the extended header.
- `emit_schema_generates_effect_table_and_interaction_actor_scaffold`
  instantiates `EffectTable`, proves it satisfies
  `InteractionActor<Operation, Output = FanOut>`, calls `Interact::interact`,
  and checks the generated `Declaration` effect payload survives.
- Existing route-table, short-header, and positional-field tests still pass.

`schema-rust`'s unit test now also asserts that the pure composer emits
`Effect`, `EffectTable`, `Interact`, and `ExtendedHeader` tokens.

## Verification

Focused checks run before commit:

```text
nix develop --option max-jobs 0 --command cargo fmt
nix develop --option max-jobs 0 --command cargo test -p schema-rust -- --nocapture
nix develop --option max-jobs 0 --command cargo test --test emit_schema -- --nocapture
```

Result:

- `schema-rust`: 1 test passed.
- `emit_schema` integration test: 5 tests passed.

Full Nix flake checks should be run after committing because the flake source
is Git-cleaned and ignores uncommitted changes.

## What I Discovered

The current schema substrate is ready for prefix-preserving extended headers
because routes already carry leg, root slot, endpoint slot, root name,
endpoint name, and body descriptor.

The effect side is only partially ready. `AssembledSchema` does not yet carry
an authored effect vocabulary or authored effect table. Deriving
`Operation -> Effect` one-to-one from routes is therefore the honest first
bridge: it gives the generated runtime a stable shape without pretending the
schema syntax has already expressed internal actor semantics.

The next durable step is in the schema crate, not in `signal-frame`: add a
schema feature or declaration family for authored effect tables. Once that
exists, `schema-rust` can replace route-derived default effects with the
authored table while keeping the generated `Interact` / `InteractionActor` /
`FanOut` shape.

## Remaining Work

- Add authored schema syntax for effect vocabulary and effect table.
- Feed authored effect rows into `schema::AssembledSchema`.
- Extend `schema-rust` so `EffectTable` maps from authored table rows, not
  default route identity.
- Add output-target fan-out descriptors so generated fan-out can name database
  actor, subscription actor, reply actor, etc.
- Add real Spirit schema witness once `signal-persona-spirit` moves from
  fixture schema to `emit_schema!`.
