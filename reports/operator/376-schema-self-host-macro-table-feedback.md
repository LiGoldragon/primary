# Operator feedback — macro-table self-host POC, with structural-node data context

Feedback on `reports/designer/625-operator-spec-self-host-macro-table-type.md`,
read together with
`reports/system-designer/103-structural-macro-as-schema-data.md`.

The designer 625 slice is implementable and is the right operator-sized first
cut, but it should be described more narrowly after 103: it proves
schema-emitted macro-table nouns can replace hand-written Rust nouns for the
pattern family. It does not close the whole structural macro self-host loop,
because 103 correctly identifies another remaining hand-coded island: the
structural-node shape vocabulary still lives in derive attributes and
hand-written `StructuralMacroNode` impls.

## Main operator read

Keep 625's stage 1. Do not pull 103's full `StructuralNodeSpec` / builtin-node
artifact into this implementation slice. The two reports stack cleanly if the
boundary is explicit:

- 625 stage 1: generate the macro-table data nouns from
  `/git/github.com/LiGoldragon/schema-next/schemas/core.schema`, attach the
  existing behavior to the generated pattern-family nouns, and prove the
  checked-in macro library still decodes and executes.
- 103 next layer: make the structural macro-node shape declarations themselves
  data, so `#[shape(...)]` and hand-written `StructuralMacroNode` tables become
  freshness witnesses or generated code rather than source authority.

The current 625 title/wording says "close the self-host bootstrap". That is
true only for the macro-table type noun loop. With 103 in view, the report
should avoid implying that structural-node shapes have also become data.

## Source grounding

The core source does contain the target family:
`/git/github.com/LiGoldragon/schema-next/schemas/core.schema:9` through
`/git/github.com/LiGoldragon/schema-next/schemas/core.schema:23` declare
`MacroLibrarySourceEntry`, `SchemaMacro`, `MacroPattern`,
`MacroPatternObjects`, `MacroPatternObject`, `MacroPatternDelimited`,
`MacroCaptureName`, `MacroAtom`, `MacroDelimiter`, and `MacroPosition`.

The hand-written pattern family in
`/git/github.com/LiGoldragon/schema-next/src/declarative.rs:312`,
`/git/github.com/LiGoldragon/schema-next/src/declarative.rs:408`, and
`/git/github.com/LiGoldragon/schema-next/src/declarative.rs:542` is a real
replaceable noun family: `MacroPattern`, `MacroPatternObject`, and
`MacroPatternDelimited` already carry derived NOTA/rkyv codecs plus local
behavior. The behavior methods can move onto generated nouns without inventing
new architecture.

The template fork in 625 is also real. `core.schema` models
`MacroTemplate` as a structural object mirror at
`/git/github.com/LiGoldragon/schema-next/schemas/core.schema:16`, while the
current executable code models it as typed output kinds at
`/git/github.com/LiGoldragon/schema-next/src/declarative.rs:591` and
`/git/github.com/LiGoldragon/schema-next/src/declarative.rs:684`. Operator
should not resolve that fork inside this slice.

## Implementation pressure points

The spec's "generate exactly the pattern family" is not the public
`schema-rust-next` entry point today. `RustEmitter` emits a module from a whole
schema, and `ModuleEmission::declaration_module` selects the no-runtime
declaration-module target. It does not currently expose a "declaration family
closure" target that emits only `MacroPattern` and its reachable declarations.

That leaves two honest paths:

- Generate a full declaration module from `core.schema`, namespace it clearly
  under `schema-next`'s generated surface, and import only the stage-1 pattern
  family into `declarative.rs`. The generated template mirror exists in the
  module but is explicitly non-authoritative until designer resolves the fork.
- Add a real family/subset emission feature to `schema-rust-next`, then emit
  only the reachable pattern-family closure. Do not hand-write a bespoke
  string filter over generated Rust; that would recreate the codegen drift this
  POC is trying to remove.

I prefer the full declaration module for the first POC unless compilation or
review clarity suffers. It keeps the emitter path ordinary and avoids turning
stage 1 into a new selector feature.

The `MacroPatternObjects` wrapper is a real adaptation point. The current
hand-written runtime uses `children: Vec<MacroPatternObject>` directly in
`MacroPatternDelimited`, and `PatternChildren` operates on a slice at
`/git/github.com/LiGoldragon/schema-next/src/declarative.rs:1084`. The schema
spells `MacroPatternObjects { values (Vec MacroPatternObject) }`, then embeds
that wrapper in `MacroPatternDelimited`. Operator should either attach a small
method surface to the generated wrapper or correct `core.schema` if that
wrapper is not a real noun. Do not preserve the old direct field merely for
compatibility.

The leaf-newtype expectation in 625 is correct. Current schema lowering tests
pin that bare `Name Type` namespace bindings lower to `TypeDeclaration::Newtype`
rather than aliases, so `MacroCaptureName String`, `MacroAtom String`, and
`MacroPattern MacroPatternObject` should become distinct Rust newtypes. The
implementation pressure is adapting existing `&str`/`String` methods and
bindings to those payload accessors, not changing the schema syntax.

Expect possible `rkyv` bound pressure around the recursive enum/struct/vector
cycle. The hand-written code uses `#[rkyv(omit_bounds)]` on recursive payloads.
If generated recursive declarations do not compile cleanly, that is a
`schema-rust-next` emitter gap in scope for the POC, not a reason to keep the
pattern types hand-written.

## Testing feedback

The proof list in 625 should be upgraded from `cargo test` / `cargo clippy`
evidence to Nix evidence. Local `cargo test` is fine for the inner loop, but
review evidence in this workspace is `nix flake check` or named flake outputs.

Minimum witnesses for this slice:

- `schema-next` flake check passes, including existing
  `tests/macro_exploration.rs` and `tests/design_examples.rs`.
- A freshness check proves the generated module is exactly re-emitted from
  `schemas/core.schema`.
- If `schema-rust-next` changes, a local override run proves
  `schema-next` consumes the local emitter rather than only the pinned remote
  revision.
- A negative/source witness should ensure the old hand-written pattern-family
  declarations no longer exist in `src/declarative.rs`, while behavior impls
  remain attached to generated nouns.

The existing `schema-next` flake already has strong architecture witnesses
around no production free functions, no unit-struct method holders, and the
macro-library collapse. This POC should add to that style, not rely on a
manual command transcript.

## Relationship to report 103

103 should constrain the claim language, not block the work. A generated
`MacroPatternObject` with a hand-written `impl StructuralMacroNode for
MacroPattern` is still not the final 103 world, because the shape of that node
is not yet a `StructuralNodeSpec` data artifact. But it is a valuable
intermediate: the data nouns come from schema first, and the remaining
hand-written surface is now isolated as behavior/codec dispatch rather than
also being the data definition.

The handoff to designer after 625 should therefore be specific:

- The pattern-family nouns are schema-emitted and executing.
- The template model fork remains unresolved.
- The structural-node-shape-as-data work from 103 remains unresolved and should
  become its own next design/operator slice.

That gives the psyche the proof they asked for without pretending the larger
self-hosting cascade is done.

## Recommended operator next step

Implement 625 as a narrow feature branch/worktree slice, but adjust the first
commit plan:

1. Add or reuse a generated declaration module path for `core.schema`.
2. Prove the generated module freshness through a Nix check.
3. Swap only the pattern-family type definitions in `declarative.rs` to the
   generated nouns.
4. Adapt behavior methods to generated newtypes and the `MacroPatternObjects`
   wrapper.
5. Run `nix flake check` in `schema-next`; if `schema-rust-next` changed, run a
   local override check from the consumer side.
6. Stop at the template fork and 103 structural-node-data boundary.

The spec is good enough to start if those proof and scope corrections are
accepted.
