# repin3 -- re-pin consumers on protos 0.15.1 and ethos-zero 1.3.0

Report for flow 6329f1, carried account.

## Substrate

- protos 0.15.1 main 48061367: Situated<F> derives Clone/Debug/PartialEq/Eq
- datomic 0.9.1 main 4712361c: pin protos 0.15.1
- ethos-zero 1.3.0 main 1d3f6066 (pre-existing): Copy for unit-only enums

## Repos re-pinned

| repo | old main | new main | old version | new version |
|---|---|---|---|---|
| datomic | e4430bfe | 4712361c0194 | 0.9.0 | 0.9.1 |
| ethos-zero | 1d3f6066 | 0f198968d208 | 1.3.0 | 1.3.1 |
| signal-orchestrate | 43db4af5 | f366d6accf8d | 0.20.0 | 0.20.1 |
| meta-signal-orchestrate | a29abc91 | 3ae11c132272 | 0.14.0 | 0.14.1 |
| orchestrate | 1c0dd769 | ef10df213b45 | 0.29.0 | 0.29.1 |
| claude-answers | a2edb677 | f5c15478bdaf | 0.5.0 | 0.5.1 |
| curriculum-deploy | 50e12d3a | 2a1c3371a41f | 0.5.0 | 0.5.1 |

## Per-repo details

### datomic 0.9.1 (4712361c)

Pin protos 48061367 (0.15.1). No source change. Situated<F> now inherits
Clone/Debug/PartialEq/Eq from protos. All 37 tests pass. Nix flake check
green on prometheus.

### ethos-zero 1.3.1 (0f198968)

Pin protos 48061367, datomic 4712361c. Flake inputs protos-map and
datomic-map updated. Fixed pre-existing broken e2e test
`fixture_library_meaning_round_trips_in_e2e`: replaced nonexistent
`protos::Textualizing`/`Text<Meaning>`/`embody()` with direct
`Meaning::Plain` construction; added stub impls for `Summarizable` and
`Fillable` kind association assertions. Bootstrap module unchanged
(freshness test passed without regeneration). All 51 tests pass. Nix flake
check green on prometheus.

### signal-orchestrate 0.20.1 (f366d6ac)

Pin protos 48061367, datomic 4712361c, ethos-zero 0f198968. Regenerated
src/generated/signal.rs; freshness test passed. All 4 tests pass. Nix flake
check green on prometheus.

### meta-signal-orchestrate 0.14.1 (3ae11c13)

Pin protos 48061367, datomic 4712361c, ethos-zero 0f198968. Regenerated
src/generated/signal.rs; freshness test passed. All 3 tests pass. Nix flake
check green on prometheus.

### orchestrate 0.29.1 (ef10df21)

Pin protos 48061367, datomic 4712361c, ethos-zero 0f198968,
signal-orchestrate f366d6ac, meta-signal-orchestrate 3ae11c13.

Situated import attempted per brief (import `datomic:[ Situated Fault ]`,
delete local Situated). The emitter emits `datomic::Situated` without a
generic parameter, but the Rust type is `protos::Situated<F>` which requires
`<F>`. Compilation fails. Reverted: Situated remains locally declared. The
ethos comment updated from "missing derives" to "emitter does not specialize
generics." Recorded in api-deviations.md under repin3.

Generated code byte-identical to 0.29.0 (ethos source unchanged in shape).
All 14 tests pass including all 6 live_nexus stderr-matching tests.
UPGRADES.md entry for 0.29.0 to 0.29.1 added. Nix flake check green on
prometheus.

### claude-answers 0.5.1 (f5c15478)

Pin protos 48061367, datomic 4712361c, ethos-zero 0f198968. Regenerated
src/generated.rs; freshness test passed. All 19 tests pass. Nix flake check
green on prometheus.

### curriculum-deploy 0.5.1 (2a1c3371)

Pin protos 48061367, datomic 4712361c, ethos-zero 0f198968. Regenerated
src/generated.rs; generated code now emits `Clone, Copy, Debug, PartialEq,
Eq` for unit-only enums (Provider, Permission, Effort, Surface). Deleted
src/generated_ext.rs (four manual `impl Copy` lines) and removed its
`mod generated_ext` from lib.rs. Freshness test passed. All 4 tests pass
(2 ignored, require external Curriculum data). Nix flake check green on
prometheus.

## Primary

flake.nix curriculum-deploy input updated to 2a1c3371a41f. flake.lock
updated. Regeneration via `nix run .#generate-skills` produced
`Generated.{ 38 27 }`. Rendered trees unchanged: only flake.nix and
flake.lock modified. Not committed per the brief.

## Checks

Every repo: cargo test, cargo clippy, cargo fmt --check clean; cargo tree -d
shows no duplicate datomic or protos revs; nix flake check through the
remote builder (ssh://prometheus) passed. Every push was a fast-forward
merge to main with origin/main witnessed.

## Deviations

1. **Situated not imported in orchestrate ethos**: the ethos emitter does
   not specialize generic imports. `datomic:Situated` emits
   `datomic::Situated` without `<F>`, which fails to compile because
   `protos::Situated<F>` is generic. The original blocker (missing derives)
   is resolved by protos 0.15.1, but the emitter limitation prevents the
   import. Situated remains locally declared with identical shape. An
   ethos-zero change adding generic-parameter pass-through for imports
   would resolve this.

## Sources

- datomic origin/main 4712361c0194 (witnessed)
- ethos-zero origin/main 0f198968d208 (witnessed)
- signal-orchestrate origin/main f366d6accf8d (witnessed)
- meta-signal-orchestrate origin/main 3ae11c132272 (witnessed)
- orchestrate origin/main ef10df213b45 (witnessed)
- claude-answers origin/main f5c15478bdaf (witnessed)
- curriculum-deploy origin/main 2a1c3371a41f (witnessed)
- primary flake.nix and flake.lock (uncommitted)
- nix run .#generate-skills output: Generated.{ 38 27 }
