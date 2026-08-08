# Horizon Pure-Schema Concept Prototype

Worktree:

`/home/li/wt/github.com/LiGoldragon/schema-rust-next/horizon-schema-concept`

Spirit intent:

`1047` — Horizon pure-schema work should be shown through a working end-to-end prototype with imports, assembled schema, and generated data types, not design prose alone.

## What I Built

The prototype lives in `schema-rust-next` because that repository already owns the working path from `schema-next::Asschema` to source-visible Rust data types.

It adds a small Horizon-domain concept under:

`concept/horizon/schema/`

The concept has three authored pure schemas:

- `proposal.schema` — cluster proposal nouns such as `ClusterProposal`, `Node`, `MajorNodeKind`, and `NodeFeature`.
- `view.schema` — projected view nouns such as `Horizon`, `HostView`, and `DomainName`.
- `lib.schema` — importing boundary schema that imports the proposal and view root types and defines `ProjectionRequest`, `ProjectionResult`, and root `Input`/`Output`.

The importing schema uses this shape:

```nota
{
  Proposal horizon-concept:proposal:ClusterProposal
  View horizon-concept:view:Horizon
}
(Input ((Project ProjectionRequest)))
(Output ((Projected ProjectionResult) (Rejected ProjectionRejection)))
```

## Working Pipeline

`examples/horizon_concept.rs` runs the pipeline:

1. Load `concept/horizon/schema/*.schema` through `schema-next::SchemaPackage`.
2. Lower each module through `SchemaEngine` into `Asschema`.
3. Emit Rust source through `schema-rust-next::RustEmitter`.
4. Write the three observable stages to `target/horizon-schema-concept/`.

Command:

```sh
cargo run --example horizon_concept -- target/horizon-schema-concept
```

Output:

- `target/horizon-schema-concept/01-input-schema/*.schema`
- `target/horizon-schema-concept/02-assembled-schema/*.asschema.debug`
- `target/horizon-schema-concept/03-generated-rust/src/schema/{proposal,view,lib}.rs`

The checked test fixtures mirror the generated Rust under:

`tests/fixtures/horizon-concept/generated/src/schema/`

## Import Support Added

Before this pass, `Asschema` carried imports but `schema-rust-next` did not emit any Rust bridge for them.

The emitter now turns an import such as:

```nota
Proposal horizon-concept:proposal:ClusterProposal
```

into:

```rust
pub use crate::schema::proposal::ClusterProposal as Proposal;
```

It also emits one `NotaDecodeError` conversion per imported module. Without that, generated `from_nota_block` methods cannot parse imported payloads because each generated module owns its own decode error type.

## Tests

Added `tests/horizon_concept.rs`.

The tests prove:

- `SchemaPackage` loads `proposal`, `view`, and `lib`.
- `SchemaEngine` lowers `lib` with imports preserved in `Asschema`.
- `RustEmitter` emits generated file paths and import bridges.
- The generated imported modules compile together.
- A real NOTA `Project` signal parses into generated Horizon-domain Rust types, round-trips to NOTA, encodes to a generated signal frame, and decodes back.
- A generated `Projected` output crosses the import boundary into the generated `view` module.

Verification run:

```sh
CARGO_BUILD_JOBS=2 cargo fmt --all -- --check
CARGO_BUILD_JOBS=2 cargo test --jobs 2
nix --max-jobs 0 flake check
```

All passed. The Nix flake check dispatched builds to Prometheus.

## Limits Exposed

This is a real pipeline, but it also exposes the next missing pieces:

- `schema-next::SchemaPackage` is still a module loader, not a full import resolver. It loads modules and preserves imports, while `schema-rust-next` now bridges those imports at Rust emission time.
- The schema language still lacks first-class vector/list cardinality. The concept uses fixed representative fields (`Workstation`, `Router`) instead of a true node vector.
- The generated support floor is duplicated per generated module (`Text`, `Integer`, `NotaDecodeError`, envelopes). This works, but a shared schema core should eventually own those primitives.
- Horizon is not yet a triad component here. The prototype generates Horizon-domain data and signal roots; it does not yet create `horizon`, `signal-horizon`, and `owner-signal-horizon` repositories.

## Next Best Step

Move the next prototype into the actual Horizon stack only after two substrate gaps are handled:

1. Add first-class vector/list cardinality to the schema language and Rust emitter.
2. Decide whether Horizon is a pure library schema, a triad component, or both: a pure projection library plus a daemon that serves projection requests over `signal-horizon`.

