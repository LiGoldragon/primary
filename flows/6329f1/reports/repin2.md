# repin2 -- re-pin consumers on datomic 0.9.0 and ethos-zero 1.2.0

Report for flow 6329f1, carried account.

## Substrate

- datomic 0.9.0 main e4430bfe: Situated<F> bears Corporal<Datom>/Datomic; impl_datomic_box! macro
- ethos-zero 1.2.0 main 8bcb0b94: Library derives Clone/Debug/PartialEq/Eq; Meaning name; recursive positions boxed with Box impls emitted

## Repos re-pinned

| repo | old main | new main | old version | new version |
|---|---|---|---|---|
| signal-orchestrate | b25bbd9fbc8f | 43db4af50686 | 0.19.0 | 0.20.0 |
| meta-signal-orchestrate | 5a99ccb1781f | a29abc912e4a | 0.13.0 | 0.14.0 |
| orchestrate | d47382d79710 | 1c0dd769c827 | 0.28.0 | 0.29.0 |
| claude-answers | d6ae3ef18fed | a2edb6777b60 | 0.4.0 | 0.5.0 |
| curriculum-deploy | f3f2ee33d661 | 50e12d3ace0d | 0.4.0 | 0.5.0 |

## Per-repo details

### signal-orchestrate 0.20.0 (43db4af5)

Pins: datomic e4430bfe, ethos-zero 8bcb0b94. Generated code unchanged
(freshness test passed without regeneration). Formatting-only changes in
codec and test files from rustfmt edition 2024 re-wrapping. No deviations.

### meta-signal-orchestrate 0.14.0 (a29abc91)

Pins: datomic e4430bfe, ethos-zero 8bcb0b94. Generated code unchanged
(freshness test passed without regeneration). Formatting-only changes in
codec and regeneration test. No deviations.

### orchestrate 0.29.0 (1c0dd769)

Pins: datomic e4430bfe, ethos-zero 8bcb0b94, signal-orchestrate 43db4af5,
meta-signal-orchestrate a29abc91. Generated Library types now carry
`#[derive(Clone, Debug, PartialEq, Eq)]` (expected). UPGRADES.md entry for
0.28.0 to 0.29.0 added. All stderr lines in tests/live_nexus.rs
byte-identical. Deviation: Situated stays locally declared in the ethos
because datomic::Situated<F> (via protos::Situated) lacks PartialEq/Eq
derives required by the Library emitter; the brief asked to import
`datomic:[ Situated Fault ]` but this was not possible without a protos
change.

### claude-answers 0.5.0 (a2edb677)

Pins: datomic e4430bfe, ethos-zero 8bcb0b94. Generated Library types now
carry `#[derive(Clone, Debug, PartialEq, Eq)]` (expected). The generator
emits `datomic::impl_datomic_box!(Query)` for the recursive Box<Query>.
The ethos source changed from `Grep.{ Box<Query> Text }` to
`Grep.{ Query Text }` because the emitter auto-detects recursion and boxes
the position; the explicit `Box<>` in the ethos prevented the macro emission.
Hand-written Box<Query> Corporal/Datomic impls deleted from src/query.rs.
No QueryText leftovers found.

### curriculum-deploy 0.5.0 (50e12d3a)

Pins: datomic e4430bfe, ethos-zero 8bcb0b94. Generated Library types now
carry `#[derive(Clone, Debug, PartialEq, Eq)]` (expected, 20 types).
generated_ext.rs reduced from the full unit_enum_traits! macro (Clone +
Copy + PartialEq + Eq) to four bare `impl Copy` lines -- Copy is still
needed by src/roles.rs. Freshness test passed.

## Primary

flake.nix curriculum-deploy input updated to 50e12d3ace0d. flake.lock
updated. Regeneration via `nix run .#generate-skills` produced
`Generated.{ 38 27 }`. Rendered trees unchanged: only flake.nix and
flake.lock modified. Not committed per the brief.

## Checks

Every repo: cargo test, cargo clippy, cargo fmt --check clean; cargo tree -d
shows no duplicate datomic or protos revs; nix flake check through the
remote builder (ssh://prometheus) passed. Every push was a fast-forward
merge to main with origin/main witnessed.

## Deviations

1. **Situated not imported in orchestrate ethos**: protos::Situated<F> lacks
   PartialEq/Eq, so it cannot be used in a Library ethos (which derives
   those traits on all types). Situated remains locally declared with
   identical shape. A protos change adding the derives would resolve this.

2. **claude-answers ethos source changed**: `Box<Query>` became `Query` in the
   ethos because ethos-zero 1.2.0 auto-detects recursive types and boxes
   them. The explicit Box prevented the impl_datomic_box! emission. This
   is a change in the authored ethos source, not just the generated output.

3. **curriculum-deploy generated_ext.rs still needed for Copy**: ethos-zero
   1.2.0 Library derives do not include Copy. The four unit enums
   (Provider, Permission, Effort, Surface) still need Copy impls that
   the generated code does not emit. The api-deviations.md entry for
   Library mode derives is partially resolved (Clone/Debug/PartialEq/Eq
   now emitted; Copy still manual).

## Sources

- signal-orchestrate origin/main 43db4af50686 (witnessed)
- meta-signal-orchestrate origin/main a29abc912e4a (witnessed)
- orchestrate origin/main 1c0dd769c827 (witnessed)
- claude-answers origin/main a2edb6777b60 (witnessed)
- curriculum-deploy origin/main 50e12d3ace0d (witnessed)
- primary flake.nix and flake.lock (uncommitted)
- nix run .#generate-skills output: Generated.{ 38 27 }
