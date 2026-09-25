# Receipt: aggregator and meta-signal-aggregator moved to recursive signal-aggregator 1.0.0

Both consumers of signal-aggregator 1.0.0 (d5ce226) now build and test against it. Both were pushed to main, and `git ls-remote origin main` returned the new head after each push.

## 1. meta-signal-aggregator: 5baab64 to f7e9f4f

- Work clone: scratchpad `msa-rec-38de5b-opus2`, held under Orchestrate lock 6463, since released.
- Repins:
  - signal-aggregator b21dc9f to d5ce226;
  - ethos-zero build-dependency b232d35 to 407f938 (13.0.0). That commit is on ethos-zero origin/main.
- Regeneration: `src/generated/signal.rs` was regenerated with the ethos-zero 407f938 binary. The `build.rs` freshness assertion passes. Only two things changed:
  - `Eq, Hash` added to every derive;
  - `Option` written fully qualified.
- The ethos is unchanged and no arena name occurs in this crate.
- `cargo test --features datom`: 4 passed before, 4 passed after. Plain `cargo test`: 3 passed. Clippy (`--all-targets --features datom`) gives 0 warnings; `cargo fmt --check` is clean.
- Version 0.7.0 to 0.8.0. The crate re-exports signal_aggregator types (`Projection`, `LimitPolicy` and others), which now come from a new major version of that crate. Under 0.x rules that breaks consumers. The archived shapes of this crate's own types are unchanged.

## 2. aggregator (the Nexus): 01fba5e to f7db587

- Work clone: scratchpad `agg-rec-38de5b-opus2`, held under Orchestrate lock 6464, since released.
- Repins: signal-aggregator to d5ce226 and meta-signal-aggregator to f7e9f4f.

### Code changes

- `src/text_query.rs`:
  - `ArenaIndex` and the faults `IndexOutsideArena` and `Cycle` were removed, because the type can no longer express them.
  - A new `ProjectionBudget` bounds the walk while it recurses:
    - depth 32 (`TooDeep`, unchanged);
    - 256 nodes (`TooLarge`, which is now a unit variant counted during the walk instead of being read from an arena length).
- `query.rs` and `evidence.rs` now walk `TextQuery` and `MatchEvidence` in place. The engine-to-contract direction builds the tree directly.
- The doc comment in `src/output_index.rs` was updated.

### Tests: `cargo test` 118 passed before, 120 passed after

| old test (arena) | now |
|---|---|
| nested query survives the arena | the same, through the contract tree |
| hand-written arena names children by index | hand-written tree carries its children in place |
| index outside the arena is a fault | removed because it is unrepresentable. Replacements: a tree wider than the node bound gives `TooLarge`, and a tree at the bound (256 nodes) projects |
| negative index is a fault | removed because it is unrepresentable. Replacement: a negative word distance gives `DistanceOutsideRange` |
| node that reaches itself is a fault | removed because it is unrepresentable |
| arena deeper than the bound | tree deeper than the bound gives `TooDeep` |
| evidence from a real match survives | the same |
| hand-written evidence (checked arena length 4, root 3, node 1 is `Not`) | now asserts the whole hand-written contract tree, then the round trip |
| evidence index outside the arena | removed because it is unrepresentable. Replacements: an evidence position below 0 gives `PositionOutsideRange`, and evidence nested deeper than the bound gives `TooDeep` |
| new | the engine tree projects to the hand-written contract tree |

- `tests/boundary.rs`:
  - The example-search test now checks that the query is `AllOf` with 2 children, then checks its projection.
  - The Nexus rejection loop sends a tree 64 `Not`s deep and an `AnyOf` of 512 leaves. It expects `InvalidQuery` for each. Previously it sent an out-of-range arena and a cyclic arena.

### Changes outside the four files the brief named

These were needed to keep the build and docs coherent:

- `examples/transcript-block-search.datom` is now `AllOf.[ Near.{ Word.quota Word.reset 6 } Contains.Phrase.{ [ rate limit ] } ]`.
- README.md and ARCHITECTURE.md: the arena prose was replaced with a description of the tree.

### Checks and version

- `cargo clippy --all-targets` gives 0 warnings. `cargo fmt --check` is clean after `cargo fmt`.
- Version 0.7.0 to 0.8.0. The Nexus now speaks a new wire major, and the public `TextQueryProjectionFault` lost variants.

## Nix

`nix flake check --no-build` fails as-is, because the substituter prometheus timed out on a source copy. Run with `--option substitute false`, it evaluated every check derivation and printed "all checks passed!" in both repos, for x86_64-linux only. Nothing was built.

## Gap

The depth bound applies only after a frame decodes. The rkyv bytecheck of a received frame recurses over the tree before the projection runs, so validation depth is bounded only by the frame capacity. This was not tested here. signal-aggregator's ARCHITECTURE already names the concern.

## Baseline caveat

The source edits were written while the before-run of `cargo test` was still executing, after its compile had finished. The before counts are from binaries built from 01fba5e.

## Sources

- flows/38de5b/receipts/signal-aggregator-recursion.md
- signal-aggregator d5ce226 `src/generated` (TextQuery, MatchEvidence)
- meta-signal-aggregator f7e9f4f; aggregator f7db587
- scratchpad test logs `agg-opus2-before.txt` and `agg-opus2-after.txt`
