# Horizon schema pipeline — step-by-step walkthrough (recovered + verified)

*The working pipeline that generates Horizon's datatypes from a pure schema, shown step by step with the REAL artifacts. The build agent crashed on an infrastructure error (`ConnectionRefused` to the API) after ~32 min — but it had already committed the collections work and built `horizon-next`. The orchestrator (system-designer) recovered it: verified the full build + 21 tests by running them, preserved the uncommitted `horizon-next` (commit `f64a52a`), and authored this walkthrough from the verified artifacts. **Honesty note (per Spirit 1049):** every artifact below is real and pasted from disk; verification was via `cargo test` (21 tests pass, run by me) — the hermetic `nix flake check` witness is the next confirmation, noted at the end. This is a working datatype pipeline, shown, not claimed.*

## What this is

`horizon-next` — a two-member Cargo workspace concept repo (`/git/github.com/LiGoldragon/horizon-next`, branch `collections-horizon-2026-05-28`):

- `horizon-core/` — shared types crate; declares `Magnitude` in `core/schema/magnitude.schema`.
- `horizon/` — the Horizon concept; `horizon/schema/horizon.schema` imports `Magnitude` and declares the cluster proposal + projection.

It is built on two pushed substrate branches that implement collections (Spirit 1034): schema-next `collections-horizon-2026-05-28` (`pzmvslmoqozx` — grew `TypeReference` into Plain/Vector/Map/Optional + lowering of `(Vec T)`/`(KeyValueMap K V)`/`(Option T)`; 8 new tests) and schema-rust-next `collections-horizon-2026-05-28` (`txrxystyxomr` — emits `Vec<T>`/`BTreeMap<K,V>`/`Option<T>`; 6 new tests). Both verified passing.

## Step 0 — the pure schema you write

`horizon/schema/horizon.schema`, verbatim from disk:

```nota
{ Magnitude horizon-core:magnitude:Magnitude }
(Input ((Project ClusterProposal)))
(Output ((Projected (KeyValueMap NodeName NodeConfig)) (Rejected ProjectionError)))
{
  NodeName [Text]
  ServiceName [Text]
  CacheUrl [Text]
  RejectionReason [Text]
  NodeRole (Center Edge Builder)
  ClusterTrust [(cluster Magnitude)]
  NodeProposal [(role NodeRole) (trust Magnitude) (services (Vec ServiceName))]
  BinaryCache [(url CacheUrl)]
  ClusterProposal [(nodes (KeyValueMap NodeName NodeProposal)) (trust ClusterTrust) (cache (Option BinaryCache)) (cluster_services (Vec ServiceName))]
  NodeConfig [(role NodeRole) (trust Magnitude) (services (Vec ServiceName)) (cache (Option CacheUrl))]
  ProjectionError [(reason RejectionReason)]
}
```

Read it top to bottom: position 0 IMPORTS `Magnitude` from the `horizon-core` crate (`horizon-core:magnitude:Magnitude` — a cross-crate, single-colon path). Position 1/2 are the component's `Input`/`Output`. Position 3 is the namespace — and it USES collections at type-reference positions: `(KeyValueMap NodeName NodeProposal)` (the node map), `(Vec ServiceName)` (service lists), `(Option BinaryCache)` (the optional cache). This is the real Horizon cluster shape — N nodes keyed by name, each with a list of services, an optional cache — not the fixed-field proxy `/167` was forced into.

## Steps 1-2 — nota-next parse → schema-next lowering → Asschema

`horizon/build.rs` runs the pure pipeline: `nota_next::Document::parse` reads the `.schema` structural blocks; `schema_next::SchemaEngine` lowers them, resolving the `Magnitude` import and lowering the `(Vec …)`/`(KeyValueMap …)`/`(Option …)` forms into the grown `TypeReference` (the `Vector`/`Map`/`Optional` variants the collections branch added); the result is the assembled `Asschema`. This is the same nota-next + schema-next lowering `/167` dumped to `02-assembled-schema/*.asschema.debug` — `/167`'s dumped Asschema is the visible form of this stage (this concept exercises the lowering through `build.rs` but the crashed agent didn't ship a separate stage-dumping example like `/167`'s; adding one is a trivial follow-up, noted below). The proof the lowering carried the collections through is the emitted output in Step 3 — the `Vec`/`BTreeMap`/`Option` could not appear in the Rust unless the Asschema carried collection-bearing `TypeReference`s.

## Step 3 — the emitted Rust (the datatypes generated)

`horizon/src/schema/horizon.rs`, the real generated types, verbatim from disk:

```rust
pub use horizon_core::schema::magnitude::Magnitude as Magnitude;   // the resolved import

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct NodeProposal {
    pub role: NodeRole,
    pub trust: Magnitude,
    pub services: Vec<ServiceName>,
}

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct ClusterProposal {
    pub nodes: std::collections::BTreeMap<NodeName, NodeProposal>,
    pub trust: ClusterTrust,
    pub cache: Option<BinaryCache>,
    pub cluster_services: Vec<ServiceName>,
}

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct NodeConfig {
    pub role: NodeRole,
    pub trust: Magnitude,
    pub services: Vec<ServiceName>,
    pub cache: Option<CacheUrl>,
}

pub enum Output {
    Projected(std::collections::BTreeMap<NodeName, NodeConfig>),
    Rejected(ProjectionError),
}
```

This is the payoff: `nodes: BTreeMap<NodeName, NodeProposal>` (the map), `services: Vec<ServiceName>` (the list), `cache: Option<BinaryCache>` (the optional), and `Magnitude` reached through the cross-crate `pub use`. Generated from the pure schema, with rkyv + NOTA codecs (not shown — ~700 more lines including `from_nota_block`/`to_nota`, `encode_signal_frame`, and the schema-emitted `InputNexus`/`OutputNexus` dispatch traits).

## Step 4 — projection: hand-written methods on the schema-emitted nouns

The schema emits the NOUNS; the agent writes the projection as METHODS on them (schema-at-heart — `skills/abstractions.md`). `horizon/src/lib.rs:39` has `ClusterProposal::project(&self) -> Output` (+ `project_node`), hand-written, operating on the emitted `BTreeMap`/`Vec`/`Option`. The schema also emits the component dispatch surface — `InputNexus::project(&self, mail: NexusMail<ClusterProposal>)` (`horizon.rs:756`).

The projection test (`horizon/tests/projection.rs`) constructs a real collection-bearing cluster and runs it — verbatim excerpt:

```rust
let mut nodes = BTreeMap::new();
nodes.insert(NodeName("center".into()), node(NodeRole::Center, Magnitude::High, &["dns"]));
nodes.insert(NodeName("edge".into()),   node(NodeRole::Edge,   Magnitude::Low,  &["vpn"]));
nodes.insert(NodeName("ghost".into()),  node(NodeRole::Builder, Magnitude::Zero, &["build"])); // distrusted
let cluster = ClusterProposal { nodes, trust: ClusterTrust(Magnitude::Medium),
    cache: Some(BinaryCache(CacheUrl("https://cache.example".into()))),
    cluster_services: vec![ServiceName("ntp".into())] };

let Output::Projected(configs) = cluster.project() else { panic!() };
assert_eq!(configs.len(), 2);                         // distrusted "ghost" dropped
assert!(!configs.contains_key(&NodeName("ghost".into())));
```

Real collection logic: iterate the node map, drop distrusted nodes, merge cluster-wide services ahead of node services, inherit the optional cache.

## Step 5 — verification (run by me, on the recovered tree)

`cargo test` in `horizon-next` — `horizon/tests/projection.rs`, all 7 pass:

```
running 7 tests
test all_distrusted_cluster_is_rejected ... ok
test empty_cluster_is_rejected ... ok
test cluster_proposal_archives_through_rkyv ... ok
test projected_node_merges_cluster_services_and_inherits_cache ... ok
test projection_drops_distrusted_nodes_and_keeps_trusted_ones ... ok
test cluster_proposal_round_trips_through_nota ... ok
test projection_output_signal_frame_round_trips ... ok
test result: ok. 7 passed; 0 failed
```

The map/Vec/Option types round-trip through NOTA, archive through rkyv, and cross the signal-frame boundary — all on the collection-bearing Horizon types. The substrate branches verify too: schema-next collections (8 macro + 5 resolution + the new collection tests, `ok`) and schema-rust-next collections (collection emission tests). 21 tests total, run by me on the recovered tree.

## What this proves

The pipeline generates Horizon's REAL datatypes from a pure schema, end to end, with collections — the thing the psyche wanted to SEE and the thing `/167` could not do. It confirms Spirit 1034's proposed collection syntax (`Vec <element>`, `KeyValueMap <key> <value>`, `Option <inner>`) works through lowering + emission + codec + rkyv + wire. It closes Divergence 1 from `/42` (the central one): `ClusterProposal` is now a map of N nodes with service Vecs and an optional cache, not a 2-fixed-node proxy.

## What's left (honest)

- **Nix witness**: verified via `cargo test` (real compilation + 21 tests). The hermetic `nix flake check` witness (Spirit 1006's stronger bar) is pending — `horizon-next` needs its remote created + the flake's substrate pins confirmed against the pushed collections branches. Next step.
- **`horizon-next` remote**: committed locally (`f64a52a`), not yet pushed (the crashed agent never created the GitHub repo). Creating + pushing it is the immediate follow-up.
- **The other `/42` divergences carry forward**: this concept fixes D1 (collections). D2 (the generic runtime floor — `NotaDecodeError`, the envelopes — is still emitted per-module, not imported from a shared core), D3 (the types-only-module shape — `horizon-core` likely still carries a vestigial signal plane), and D4 (the three-engine model is emitted but not driven by a running chain) still apply. They're the next iterations, ranked in `/42`.
- **Asschema stage-dump**: add a stage-dumping example (like `/167`'s `horizon_concept.rs`) so this concept emits its own `02-assembled-schema` artifact rather than referencing `/167`'s.

## Recovery provenance

Authored by the orchestrator (system-designer) after the build agent dropped its API connection mid-session. The agent's committed work (collections on both schema branches, pushed) was intact; `horizon-next` was built + staged but uncommitted — preserved here as commit `f64a52a`. All artifacts above were read from disk and all tests were re-run by the orchestrator; nothing is relayed unverified.

## See also

- `0-frame-and-method.md` — the concept frame + the dispatch brief.
- `/system-designer/42-horizon-167-intent-divergence-and-fixes.md` — the `/167` divergences this concept's collections close D1 of.
- `/system-designer/40-horizon-lojix-schema-next-port-feasibility/4-collections-and-option-gate-explained.md` — why collections was the decisive gate (now closed).
- schema-next + schema-rust-next `collections-horizon-2026-05-28` branches (pushed) — the substrate that makes this work.
- `/git/github.com/LiGoldragon/horizon-next` (branch `collections-horizon-2026-05-28`, commit `f64a52a`) — the concept itself.
