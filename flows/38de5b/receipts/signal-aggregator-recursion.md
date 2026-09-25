# Receipt: signal-aggregator arenas replaced by recursive types (1.0.0)

- Repo: LiGoldragon/signal-aggregator. main moved from b21dc9f to d5ce22622bb499da89a87a394d01da9d31dffbb7, a single fast-forward commit. `git ls-remote origin main` returned d5ce226 after the push.
- Work clone: the scratchpad directory `signal-aggregator-rec-38de5b-opus`, under Orchestrate lock 6456, since released. ethos-zero 407f938 was built in `ethos-zero-407-sagg-opus`, a scratch clone of its own. The shared checkout /git/github.com/LiGoldragon/signal-aggregator was not touched.

## Why the arenas existed

ARCHITECTURE.md said, under "Recursion and the wire", that the flat node arenas were "a property of the generator, not a choice this contract would otherwise have made": rkyv could not close its bounds over `Vec<Self>` or `Box<Self>`. The README gave the same reason. Nothing else depended on the index shape. Specifically:

- no sharing of subnodes was documented;
- the only arena-specific semantics was "an index outside the vector is an `InvalidQuery` rejection", which a tree makes impossible.

The rewrite therefore went ahead.

## Change

- The build-dependency ethos-zero moved from b232d35 to 407f938 (13.0.0).
- `TextQuery` replaces `TextQueryNode`. Its variants are `Contains.TextQueryTerm`, `AllOf.TextQueries`, `AnyOf.TextQueries`, `Not.TextQuery` and `Near.NearTextQuery`, with `TextQueries.Vector<TextQuery>`. `TranscriptBlockTextQuery` is now an alias of `TextQuery`, so the request's field name is unchanged.
- `MatchEvidence` replaces `MatchEvidenceNode`. Its variants are `Contains.ContainsEvidence`, `AllOf.MatchEvidences`, `AnyOf.MatchEvidences`, a bare `Not` (kept bare, as before) and `Near.NearEvidence`. `TranscriptBlockSearchEvidence` is now an alias of `MatchEvidence`.
- The following types were removed: `TextQueryNodeIndex(ices)`, `TextQueryRoot`, `TextQueryNodes`, `MatchEvidenceIndex(ices)`, `MatchEvidenceRoot` and `MatchEvidenceNodes`.
- The generated code puts `omit_bounds` on the recursive positions. The only `Box` is on `TextQuery::Not`.
- Regenerating also added `Eq, Hash` to the structs that previously derived only `PartialEq`. This is ethos-zero output drift since b232d35.
- README and ARCHITECTURE were rewritten. ARCHITECTURE now notes that tree depth is bounded only by frame size, so a reader of untrusted frames must bound the nesting depth it validates.

## Tests

| run | before (b21dc9f) | after (d5ce226) |
|---|---|---|
| `cargo test` | 4 passed | 5 passed |
| `cargo test --features datom` | 6 passed | 8 passed |

- The existing witnesses keep their meaning: the search request still carries `AllOf[ Contains alpha, Contains «bounded text» ]`, now as a tree.
- New test `a_nested_query_and_its_nested_evidence_round_trip_through_rkyv`. It builds:
  - a query four levels deep, using `AnyOf`, `AllOf`, `Not(Not(..))`, `Near` and an empty `AllOf`;
  - a `TranscriptBlocksSearched` response carrying nested `MatchEvidence`.

  It sends each through `rkyv::to_bytes`/`rkyv::from_bytes`, which validates the bytes, and then through the Signal frame, and asserts both come back equal.
- New test `datom_round_trip_preserves_a_nested_query_and_its_nested_evidence`: the same two values round-trip through Datom text.
- `cargo clippy --all-targets`, with and without `datom`, gives 0 warnings. `cargo fmt --check` is clean. `cargo doc` is clean. `nix flake check` was not run.

## Version

The version goes from 0.9.0 to 1.0.0, a major bump. This is a wire change: the archived shapes of `SearchTranscriptBlocks` and `TranscriptBlocksSearched` changed, and public types were removed.

## Downstream consumers that must repin

- **aggregator.** Cargo.toml pins signal-aggregator b21dc9f and meta-signal-aggregator 5baab64. It uses the arena in `src/text_query/query.rs`, `src/text_query/evidence.rs`, `tests/text_query_projection.rs`, `tests/boundary.rs` and README.md. Those need a code rewrite, not only a repin.
- **meta-signal-aggregator.** Cargo.toml pins signal-aggregator b21dc9f. No arena names were found in it, so a repin plus regeneration should suffice. It was not verified.
- Both findings come from the local /git checkouts, which may lag their remotes.

## Deviation

The brief asked for the footer "Co-Authored-By: Claude Fable 5.1". The commit carries "Claude Opus 5.5 (1M context)" instead, because that is the model that actually ran this subflow.

## Sources

- signal-aggregator b21dc9f: ethos/signal.ethos, ARCHITECTURE.md, README.md, tests/generated_contract.rs; and d5ce226.
- flows/38de5b/receipts/ethos-fix-3.md, ethos-fixes-5-6-7.md.
- /git/github.com/LiGoldragon/aggregator and meta-signal-aggregator Cargo.toml (local checkouts).
