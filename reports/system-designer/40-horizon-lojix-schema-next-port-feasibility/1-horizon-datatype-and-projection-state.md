# Wave A — horizon datatype + projection layer: schema-next port feasibility

*Research-only audit (system-designer lane). Source: the lean horizon-rs
on `horizon-leaner-shape` (worktree `~/wt/github.com/LiGoldragon/horizon-rs/horizon-leaner-shape/`,
change `svwxvkuzsymq`). Compared against schema-next / schema-rust-next /
nota-next / nota-codec under `/git/github.com/LiGoldragon/`. Answers the
five Wave A questions in `0-frame-and-method.md` §"Wave A dispatch brief".*

## Verdict in one line

**POSSIBLE for the projection LOGIC (it is already pure methods on the
proposal nouns — schema-at-heart needs no logic rewrite, only that the
nouns come from schema). PARTIAL / BLOCKED-today for the DATATYPES, on one
specific gap: schema-next has no collection types (no `Vec`, no map). The
horizon datatypes are 30% collections (21 `BTreeMap`, 39 `Vec` across the
lib). Until schema-next grows a collection `TypeReference`, the cluster
proposal cannot be schema-emitted. The projection crux is GREEN; the
datatype layer waits on one schema-language feature.**

## 1. Current datatype inventory

The lib is 7,276 lines total (`lib/` + `cli/`), split into two namespaces
declared in `lib/src/lib.rs:22-31`:

- **`proposal::*`** — input boundary, the shape `goldragon/datom.nota`
  emits. 14 modules under `lib/src/proposal/`.
- **`view::*`** — output boundary, serialised to JSON and read by Nix
  modules in CriomOS via `inputs.horizon`. 7 modules under `lib/src/view/`.
- **Shared value modules** (`species`, `name`, `magnitude`, `address`,
  `pub_key`, `disk`) — used by both sides.

Declaration mechanism: **hand-authored Rust + `serde` + `nota-codec`
derive macros**. Derive-macro census across `lib/src`:

| Derive | Count | Emits |
|---|---|---|
| `NotaRecord` | 32 | positional struct codec |
| `NotaEnum` | 17 | unit-variant enum codec |
| `NotaTransparent` | 13 | newtype passthrough codec |
| `NotaTryTransparent` | 9 | newtype + validation codec |
| `NotaSum` | 6 | data-bearing enum codec |

The big nested structure is `ClusterProposal` (`lib/src/proposal/cluster.rs:29-60`),
the projection input root. Its fields, verbatim, show the collection density:

- `nodes: BTreeMap<NodeName, NodeProposal>`
- `users: BTreeMap<UserName, UserProposal>`
- `domains: BTreeMap<DomainName, DomainProposal>`
- `trust: ClusterTrust` (itself three `BTreeMap`s + a `Magnitude`,
  `cluster.rs:62-72`)
- `secret_bindings: Vec<ClusterSecretBinding>`
- `tailnet: Option<TailnetConfig>`
- `ai_providers: Vec<AiProvider>`
- `vpn_profiles: Vec<VpnProfile>`

`NodeProposal` (`lib/src/proposal/node.rs:29-88`) has ~20 fields including
`Vec<LinkLocalIp>`, `Option<NodeIp>`, `Option<bool>`, `Vec<NodeService>`,
`Vec<WireguardProxy>`. `view::Node` (`lib/src/view/node.rs:23-116`) is even
larger: ~45 fields, a dozen of them `Option<Vec<...>>` (the viewpoint-only
fields). Nested-enum-with-data appears in `NodeService`
(`lib/src/proposal/services.rs:23-46`) where `NixBuilder { maximum_jobs:
Option<u32> }` and `PersonaDevelopment { capabilities:
Vec<PersonaDevelopmentCapability> }` are struct-variants carrying data;
`NodePlacement` (`lib/src/proposal/placement.rs:13-25`) has a `Contained {
8 named fields }` variant.

Aggregate collection density: **112 container-typed field lines** (`Vec` /
`BTreeMap` / `Option`) across `proposal*` + `view*`. This is the central
fact for the capability-gap question (§5).

Test coverage: **185 `#[test]` functions across 21 files** in `lib/tests/`
(notably `view_json_roundtrip.rs` 752 lines, `horizon.rs` 418 lines). This
is a real regression net the port must keep green.

## 2. Which nota crate today + what porting entails

**Today: `nota-codec`** (the legacy/current codec, git dep pinned at
`2618adbf`, `Cargo.toml` workspace dep + `Cargo.lock:156-158`), with its
`nota-derive` proc-macros (`Cargo.lock:165-167`). Every source file imports
from `nota_codec` (24 `use nota_codec::...` sites). The CLI
(`cli/src/main.rs:11,73-93`) reads both nota files through
`nota_codec::Decoder` + `NotaDecode::decode`, then emits JSON via
`serde_json` (`main.rs:103`). So the wire-in is NOTA (hand-derived codec),
wire-out is JSON (serde) — the JSON side is the contract Nix consumes and
must be byte-preserved through any port.

**Crucially, `nota-codec` HAS the collection codecs the datatypes need**
(`/git/github.com/LiGoldragon/nota-codec/src/traits.rs`): blanket
`NotaEncode`/`NotaDecode` impls for `Option<T>` (line 239/252), `Vec<T>`
(442/452), `BTreeMap<K,V>` as `{key value key value}` (266-308), and
`HashMap<K,V>` (310). This is exactly why horizon-rs can lean on
`BTreeMap`/`Vec` freely today: the codec layer covers them.

**Porting to nota-next/schema-next-emitted entails:**
1. **Datatypes move from hand-authored Rust to a `.schema` file** that
   schema-next lowers and schema-rust-next emits as checked-in Rust under
   `src/schema/`. The emitted shape (newtypes, structs, enums-with-data,
   rkyv derives, NOTA `from_nota_block`/`to_nota`, `FromStr`/`Display`) is
   demonstrated in `schema-core/core/src/schema/mail.rs` and the
   `schema-rust-next` emission test fixture.
2. **NOTA parsing moves from `nota-codec::Decoder` to `nota-next::Document`**.
   nota-next's `Block` enum (`nota-next/src/parser.rs:57-64`) is
   `Delimited { delimiter, root_objects } | Atom`, with `Delimiter::{
   Parenthesis, SquareBracket, Brace }`. The emitted `from_nota_block`
   methods walk this `Block` tree positionally (see
   `mail.rs:158-174` `DatabaseMarker::from_nota_block`).
3. **The JSON-out path needs a decision.** Schema-next emits NOTA + rkyv,
   NOT serde-JSON. horizon's entire reason for being is emitting JSON that
   Nix reads. Either (a) keep serde derives ALONGSIDE the schema emission
   (schema owns the type, agent adds `#[derive(Serialize)]` — but you
   can't add derives to generated code without an emitter hook), or (b)
   teach schema-rust-next to emit a JSON projection, or (c) hand-write the
   JSON serialisation as methods on the emitted nouns. This is a real,
   horizon-specific wrinkle the lojix pilots never hit (lojix is NOTA+rkyv
   end-to-end; horizon is NOTA-in / JSON-out).

Cross-crate import already works (`/39` / schema-core): the consumer's
generated `lib.rs:6` carries `pub use
schema_core::schema::mail::DatabaseMarker as DatabaseMarker`, so shared
horizon nouns (the `name::*` newtypes, `Magnitude`, `species::*` enums)
could live in one schema home that both horizon and lojix import.

## 3. THE CRUX — can projection be methods on schema-emitted nouns?

**Yes. The projection is ALREADY pure methods on the proposal nouns.**
There is not a single free projection function in the codebase — the
methods-on-nouns shape the schema-at-heart direction wants is the shape the
code already has. Walking the actual projection code:

**Entry point** — `ClusterProposal::project(&self, horizon:
&HorizonProposal, viewpoint: &Viewpoint) -> Result<Horizon>`
(`lib/src/proposal/cluster.rs:74-254`). It is a method on the proposal
root. It orchestrates the whole projection: validate viewpoint, compute
trust floors, build every `Node`, build every `User`, roll up the
`Cluster`, fill viewpoint-only fields, walk contained nodes, assemble
`Horizon`.

**The projection helpers are all methods**, on the right nouns:

- `ClusterProposal::node_trust` (`cluster.rs:311-324`) — the trust algebra
  `min(input, per_node, cluster)`. A method on the proposal.
- `ClusterProposal::validate_tailnet_topology` (`cluster.rs:271-297`) —
  single-controller enforcement.
- `ClusterProposal::resolve_secret_bindings` (`cluster.rs:260-269`) — folds
  `Vec<ClusterSecretBinding>` into a lookup `BTreeMap`.
- `ClusterProposal::router_node_name` (`cluster.rs:299-308`).
- `NodeProposal::project(&self, ctx: NodeProjection) -> view::Node`
  (`lib/src/proposal/node.rs:103-230`) — the per-node projection. This is
  the densest logic: derives `is_fully_trusted`, `is_remote_nix_builder`,
  `is_dispatcher`, `is_large_edge`, `enable_network_manager`,
  `nix_cache` URL, `max_jobs`, `chip_is_intel`, `model_is_thinkpad`,
  `criome_domain_name`, etc.
- `NodeProposal::resolve_arch` (`node.rs:246-267`) — single-hop pod→host
  arch resolution.
- `BehavesAs::derive(species, placement, io_disks_empty)`
  (`view/node.rs:145-172`) — the species→behavior matrix
  (center/router/edge/next_gen/low_power/...). A method on the view type.
- `UserProposal::project(&self, ctx: UserProjection) -> view::User`
  (`lib/src/proposal/user.rs:71-154`) — derives groups, `enable_linger`,
  `preferred_editor`, email/matrix IDs, size-floor.
- `Node::fill_viewpoint(&mut self, fill: ViewpointFill)`
  (`view/node.rs:240-301`) — second pass for viewpoint-only fields
  (builder configs, admin SSH keys, cache URLs).
- The domain/SSID/CIDR/resolver/tailnet derivations are methods on
  `HorizonProposal`: `router_ssid` (`horizon_proposal.rs:116-118`),
  `internal_domain` / `public_domain` (108-114), `tailnet_base_domain` /
  `service_domain` (120-126), `lan_network` (128-136), `resolver_policy`
  (138-144).

**Is any of it inexpressible as schema-at-heart?** No. Schema-at-heart
(per `skills/abstractions.md` §"Schema-emitted nouns") says: schema emits
the *type declarations + codec*, agents write the *methods*. Every method
above takes `&self` (or a small `ctx` projection struct) and returns view
nouns. They contain `match` on enums (`BehavesAs::derive`), arithmetic
(`Magnitude::min`), `format!` string building (domains, URLs), `BTreeMap`
folding, `.filter().map().collect()` chains. **None of this is schema-
language work — it is exactly the "agent-written Rust = behavior on
schema-emitted objects" row of the labor-split table.** The schema would
emit `ClusterProposal`, `NodeProposal`, `view::Node`, `Magnitude`,
`BehavesAs` as type declarations; these projection methods attach to them
unchanged.

**No genuine logic blocker exists.** The crux question's hypothesised
failure mode — "projection needs computation the schema language can't
express, forcing it to stay hand-written logic that merely consumes
schema-emitted types" — is the *expected and correct* outcome, and it IS
schema-at-heart, not a violation. The schema was never meant to express
the projection arithmetic; it expresses the nouns, and the projection is
methods on them. horizon-rs is already built precisely this way.

The ONE caveat (not a logic blocker, a typing blocker): the methods take
and return collection-shaped nouns (`BTreeMap<NodeName, Node>`,
`Vec<BuilderConfig>`). For these methods to attach to *schema-emitted*
nouns, the emitted nouns must HAVE those collection fields — which routes
straight to the §5 capability gap.

## 4. Feasibility verdict — datatype + projection layer

**Projection logic: POSSIBLE (already in the target shape).** Evidence:
zero free functions; `ClusterProposal::project` + ~12 helper methods, all
`&self`-on-the-noun (`cluster.rs`, `node.rs`, `user.rs`, `horizon_proposal.rs`,
`view/node.rs` cited above). Re-grounding is "delete the hand-authored type
bodies, keep the `impl` blocks, point them at schema-emitted types."

**Datatypes: PARTIAL, gated on ONE schema-next feature.** The scalar /
newtype / unit-enum / data-enum / nested-struct shapes ALL emit today
(proven: `schema-core` + `schema-rust-next` emission test). What does NOT
emit today: **collection types** — and horizon is 112 container-field-lines
deep in them. So:
- The ~40% of horizon types that are scalar-newtype-enum-struct: emittable
  now.
- The ~30% that are `BTreeMap`/`Vec`-bearing (every aggregate root,
  starting with `ClusterProposal` itself): **BLOCKED until schema-next has
  a collection type reference.**

Because the aggregate roots (the whole point of the cluster proposal) are
collection-bearing, the datatype layer is **BLOCKED-in-practice today** even
though most leaf types are fine. The verdict is PARTIAL with a single
named, well-scoped gap — not a deep architectural impossibility.

## 5. Schema-next capability gaps the horizon datatypes need

I read the schema-next type model directly to ground this
(`schema-next/src/asschema.rs`, `declarative.rs`, the `spirit-min.schema`
fixture, and the schema-rust-next emission test). Findings:

**GAP 1 — collection types (BLOCKING, the big one).** schema-next's
`TypeReference` (`asschema.rs:153-156`) is `{ name: Name }` — a single bare
name, **no type arguments, no container kind**. `TypeDeclaration`
(`asschema.rs:113-118`) is only `Struct | Enum | Newtype`. There is no
`List`, `Vec`, `Map`, or `repeated` variant anywhere. I confirmed the
square-bracket single-element form is NOT a list: `lower_struct`
(`declarative.rs:726-731`) makes a 1-field `[X]` into a **`Newtype`**, and
the emission test proves it — `Topics [Topic]` emits `struct
Topics(Topic)` and the test reads `entry.topics.0.0` as a *single* `Topic`
(`schema-rust-next/tests/emission.rs:113-118,139`), not a `Vec<Topic>`.
So `nodes: BTreeMap<NodeName, NodeProposal>`, `services: Vec<NodeService>`,
`ai_providers: Vec<AiProvider>`, and the dozen `Option<Vec<...>>` view
fields have **no schema-next expression today**. This single gap blocks the
cluster-proposal datatype port. (The wire substrate is NOT the blocker:
nota-next already parses `Delimiter::Brace` `{}` blocks
(`nota-next/src/parser.rs`) and legacy nota-codec already has the
`{key value}` map codec — the gap is purely the schema *type model* +
*emitter*, which never grew a collection reference.)

**GAP 2 — `Option<T>` / optionality (BLOCKING).** Same root cause: no way
to mark a field optional. `ClusterProposal.tailnet: Option<TailnetConfig>`,
`NodeProposal.node_ip: Option<NodeIp>`, every `#[serde(default)]` field,
and the entire viewpoint-only `Option<Vec<...>>` family need this.
schema-next has no optional-field concept in `FieldDeclaration`
(`asschema.rs:135-139` — just `name` + `reference`). Smaller than GAP 1 but
equally blocking for `ClusterProposal`.

**GAP 3 — JSON projection emission (horizon-specific, BLOCKING for the
output side).** schema-rust-next emits NOTA + rkyv codecs only (per its
ARCHITECTURE.md). horizon's `view::*` types exist to serialise to JSON for
Nix. The emitter has no serde/JSON output path, and you cannot hand-add
`#[derive(Serialize)]` to generated code. Needs either an emitter feature
or a decision to hand-write JSON as methods. Lojix never hit this (it's
NOTA/rkyv end-to-end); it is uniquely a horizon problem.

**GAP 4 — primitive width / non-`u64` scalars (minor).** schema-next's only
scalar floor is `Integer = u64` and `Text = String` (`mail.rs:3-4`).
horizon uses `u32` (`Resources.cores`, `max_jobs`), `bool` pervasively, and
foreign newtypes over `IpNet` (`LanCidr`, `view/network.rs:16`) and
`std::net` addresses. Booleans and narrower ints are common enough that
`u64`-only is friction; the `IpNet`/IP newtypes have custom
`NotaEncode`/`Decode` impls today (`network.rs:54-68`,
`placement.rs:121-135`) that the schema model has no hook to reproduce
(schema emits the codec; there's no "foreign type with hand-written codec"
escape in the emitted shape).

**Already-covered (NOT gaps):** nested enums-with-data (`Input::Mark(
DatabaseMarker)` proves data-bearing variants — covers `NodeService`,
`NodePlacement`, `Substrate`); newtypes with validation (covered by the
emit shape, though the *validation body* would be an agent method);
cross-crate type sharing (`/39` / schema-core proven); upgrade traits
(`UpgradeFrom<Previous>` emitted, record 950 satisfied); the per-variant
struct fields (e.g. `NixBuilder { maximum_jobs }`) — but note the *payload*
of those variants is itself a single `TypeReference`
(`EnumVariant.payload: Option<TypeReference>`, `asschema.rs:147-151`), so a
variant carrying a collection field still routes back to GAP 1.

## Gating summary for the synthesis

| Capability | Horizon need | schema-next today | Gates the port? |
|---|---|---|---|
| Collections (Vec / map) | 112 field-lines; every root | Absent (newtype/struct/enum only) | **YES — primary gate** |
| Optionality (`Option<T>`) | Pervasive; every `serde(default)` | Absent | **YES** |
| JSON output emission | The whole `view::*` purpose | NOTA+rkyv only | YES (output side) |
| Scalars beyond u64/String | u32, bool, IpNet newtypes | u64 + String floor | Partial (friction) |
| Nested enums-with-data | NodeService, NodePlacement | Emitted | No |
| Cross-crate shared nouns | name/Magnitude/species | Proven (/39) | No |
| Projection logic-on-nouns | ~12 methods, 0 free fns | N/A (agent-written) | No — already done |

**Bottom line for Wave A:** the projection crux resolves GREEN — horizon-rs
is *already* logic-on-nouns, so schema-at-heart needs no logic rewrite.
The datatype port is gated on exactly two general schema-next features
(collections + optionality) plus one horizon-specific one (JSON emission).
Collections is the load-bearing gap: it is the same `Vec`-gap `/37/3`
already flagged, here made concrete and quantified (112 field-lines, every
aggregate root). Close collections + optionality + a JSON-out story and the
horizon datatype layer becomes POSSIBLE; the projection logic is ready now.
