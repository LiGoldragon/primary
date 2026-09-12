# Aggregator triad and router: correcting last night's move onto Dotos

Subflow of main flow f6db8d, 2026-09-11/12. Brief: `reports/nota-pins.md`
moved `aggregator`, `signal-aggregator`, `meta-signal-aggregator` and
`router` onto `dotos`, the frozen notation; `reports/stack-membership.md`
found that direction wrong against standing Vision. Correct it — migrate
the four onto the current Datom stack by the method in
`reports/datom-migration.md`, deleting every Dotos file, feature and
compatibility path met.

Everything marked **witnessed** was read or run by this flow on this
machine. **Relayed** means a named subflow of this flow reported it.

## The ruling this corrects

> Everything moves to Datom: all of the stack, Horizon, Lojix,
> everything; no Dotos file remains. Datom's own line of descent is NOTA,
> which also passed through the temporary name Dotos; that old notation
> stays behind, frozen, and may be called legacy.

— `Vision/datom.md:239-243`, "Repository" section, read by this flow
(witnessed). It is distilled Vision, so the living reviewed it; it is
still written psyche, not the living.

## What each repository was, and what it is now

### signal-aggregator — the ordinary contract

**Before** (witnessed): 1594 lines of hand-written Rust deriving
`DotosEncode`/`DotosDecode` over the `dotos` crate, wrapped by
`signal-frame`'s `signal_channel!` macro, with `schema/signal.schema` as
a NOTA-shaped sketch that generated nothing, `examples/canonical.dotos`,
a `generated/README.md` placeholder, and a `default = ["dotos-text"]`
feature. Every scalar was a newtype: `string_newtype!(Timestamp)`,
`count_newtype!(ByteCount, u64, into_u64)`, and so on. The transcript
text query and its matching evidence were re-exports of
`dotos_text_query::Query` and `MatchEvidence`.

**After**: one Ethos Signal declaration, `ethos/signal.ethos`, 373 lines,
generating 1786 lines of Rust into `src/generated/signal.rs` through
Ethos Zero 8.0.1 (`de3d9928`). `build.rs` regenerates on every build and
asserts the checked-in projection matches, so drift cannot land. The
newtypes are `String` and `Integer` aliases; the wire enums are the
generated `Query` and `Response`. The portable rkyv frame, its three
kinds and the four-byte big-endian length prefix come from `signal`
3.0.2 (`8f9a0deb`); the Datom text projection is the `datom` feature over
`datom-codec` 0.26.3 (`627db67f`) and `protos` 0.30.1 (`171b21f6`).

**Deleted**: the `dotos` and `dotos-text-query` dependencies, the
`dotos-text` feature, `signal-frame` and the `signal_channel!` macro with
its `AggregatorWire`/`ContractBinding`/`WireRoute` surface,
`schema/signal.schema`, `examples/canonical.dotos`,
`generated/README.md`, and `tests/channel.rs`. No shim, alias, dual
decode path or version negotiation was added.

### meta-signal-aggregator — the configuration contract

Same treatment. 465 lines of Dotos-derived Rust became a 90-line
`ethos/signal.ethos` importing `Projection`, `LimitPolicy`, `PageLimit`,
`ByteLimit` and `ItemCount` from `signal_aggregator`. The `Default` impls
the old types carried became a `DefaultingPolicy` kind in `src/lib.rs`:
the generated projection derives no `Default`, and a runtime ceiling is a
policy a runtime asks for, not a zero value.

### aggregator — the consumer

**Before** (witnessed): 0.4.0 at `87c48f81`, whose description is
"aggregator: migrate to dotos and pin git dependencies" — last night's
misdirected move, already on main. **After**: 0.6.0 `256a29d5`.

Relayed from the subflow that held lock 1193, which did the 26k-line pass:
`signal-frame` is gone entirely — `Frame`, `FrameBody`, `ReplyEnvelope`,
`Request`, `Reply`, `SubReply`, `NonEmpty`, the exchange identifiers, lanes
and epochs, and the `OrdinarySocketFrame`/`MetaSocketFrame`/`SocketExchange`
machinery that carried them. One request is one `signal` frame carrying the
rkyv archive of `Query`; one reply is one frame of `Response`. There are no
exchange identifiers, lanes or sub-replies, because `signal` 3.0.2 owns no
protocol above the archive and the living has not decided one.

Also deleted, relayed: the `dotos` dependency and every `DotosEncode`/
`DotosDecode`/`DotosSource`/`to_dotos` use; the `dotos-text` feature on all
three contract dependencies; **`LegacyAggregatorConfiguration` and the dual
decode fallback in `ConfigurationStore::read_configuration`** — the 0.1
configuration migration, gone with its test; all seven `examples/*.dotos`,
replaced by four `.datom` examples that four boundary tests actualize
against hand-written expectations; `schema/runtime.schema`;
`generated/README.md`; `Error::Dotos`.

Decisions the subflow had to make that this flow's brief did not settle,
relayed and recorded because they are now the contract's operating
envelope:

- **No aggregator-level `datom` feature.** Text is the CLI's only surface,
  so an optional Datom would only make a build that cannot run.
- **Bounds on peer input.** Datom text is read with 1 MiB extent and depth
  256. The flat query arena is refused above 256 nodes or depth 32, and
  cycles are detected on the reaching path — all before recursion, because
  the arena's edges are peer-supplied and the wire type constrains nothing.
  Each is `OperationRejected`/`InvalidQuery`, witnessed at the projection
  and through `NexusPlane::search_transcript_blocks`.
- **One conversion site for counts.** `src/counting.rs` holds every
  i64/u64/usize crossing: a measure saturates at the signed ceiling, a
  negative peer count reads as zero, a negative length reads as no length.
  The second commit `99013366` exists because the mechanical pass had left
  `try_into().unwrap()` on the page limit, the read bound and the segment
  index — a negative from a peer would have panicked the daemon.
- **Derives.** Ethos Zero gives declared types `Clone, Debug, PartialEq` and
  nothing else. 129 aggregator types lost `Copy` and `Eq` as a consequence.
  Relayed and worth the living's attention: **no contract type derives `Eq`,
  `Hash` or `Default`**, so no contract value can be a map key. That is a
  gap in the generator, not in these contracts.

### The vocabulary is unchanged apart from the two arenas

Witnessed: this flow compared every struct in the old hand-written
`signal-aggregator/src/lib.rs` and `meta-signal-aggregator/src/lib.rs`
against the new Ethos declaration, position by position, and every
declared type keeps its arity and its order —
`SessionInventoryCard`'s seventeen positions, `SubagentTaskMetadata`'s
eight, `OutputInterfaceLimitPolicy`'s nine, `AggregatorConfiguration`'s
ten, and the rest. Only two things moved: the transcript text query and
its matching evidence became arenas, and every position is now named by
its type, so some field names changed (`SourceVolume.source` is now
`source_kind`, `TranscriptTextExcerpt.text` is now `transcript_text`, an
optional position reads `x_option`). The scalars stopped being newtypes:
a `String` alias where there was a `string_newtype!`, an `i64` alias
where there was a `count_newtype!` over `u64` or `u32`.

## Two findings the generator forced

**Ethos Zero's Signal root cannot express a recursive type.** Witnessed:
`fixtures/tree-types.ethos` shows recursion working — a position that
reaches its declaring type is boxed — but that fixture is a `Library`
root, which derives only `datom_codec`. A `Signal` root also derives
`rkyv::Archive`/`Serialize`/`Deserialize`, and rkyv's derive cannot close
the trait bounds of a self-reaching type. This flow generated a minimal
recursive Signal and compiled it: `error[E0275]: overflow evaluating the
requirement Vec<TextQuery>: Archive`, and the same overflow for
`Box<TextQuery>` alone. `dotos-text-query` carries the type that
motivated this and works around it by hand, with explicit
`#[rkyv(omit_bounds)]` and bytecheck/serialize/deserialize bounds
attributes; Ethos Zero emits none. So: any recursive contract type is
presently unexpressible in an Ethos Signal. This flow did not change
Ethos Zero — it was not in the brief, and its repository belongs to
another flow tonight.

The consequence, carried in the contract and recorded in its
`ARCHITECTURE.md`: `TranscriptBlockTextQuery` and
`TranscriptBlockSearchEvidence` are now flat node arenas — a vector of
nodes plus a root index, children named by index into the same vector —
rather than trees. This is a real wire redesign, made because the tree
cannot cross this wire at all, not as a preference.

**A bare enum variant that spells a declared type name becomes a payload
variant.** Ethos Zero resolves a bare variant head against the type table.
Witnessed first in the meta contract: `OperationKind.[ Configure
ObserveConfiguration ValidateConfiguration ]` generated
`ObserveConfiguration(ObserveConfiguration)` because a type of that name was
also declared, and renaming the type to `ConfigurationObservationQuery`
fixed it.

This flow then failed to check the ordinary contract for the same trap and
shipped it into `signal-aggregator` 0.7.0. The aggregator subflow met it and
relayed it; this flow confirmed it by walking the generated file for every
variant whose name equals its payload type. Three were wrong:

| generated | why it is wrong | the type it collided with |
|---|---|---|
| `SourceHealthStatus::MalformedRecords(MalformedRecords)` | a health status carrying a duplicate count | `MalformedRecords.ItemCount` |
| `ScanLimitKind::DiscoveredFiles(DiscoveredFiles)` | a limit kind carrying a duplicate count | `DiscoveredFiles.ItemCount` |
| `ScanLimitKind::ReadFailures(ReadFailures)` | a limit kind carrying the read failures themselves | `ReadFailures.Vector<ReadFailure>` |

The third shows the shape of it: a `ScanLimitKind`, whose whole job is to
name which ceiling was hit, came out holding a vector of failure records,
and `aggregator` was forced to pass `Vec::new()` to satisfy it. The
twenty-one other variants whose name equals their payload type are the
`Response` heads, declared that way on purpose.

Fixed in `signal-aggregator` 0.8.0 `e5009d65` by renaming the three
colliding types — `DiscoveredFileCount`, `MalformedRecordCount`,
`ReadFailureRecords` — leaving the variant heads, which are the wire names,
untouched. Two witnesses build both enums by their bare heads and carry them
over the rkyv frame and through the Datom text; both were seen failing
against 0.7.0 (`expected SourceHealthStatus, found enum constructor`) before
they passed. `meta-signal-aggregator` 0.6.0 `55ac16ac` and `aggregator`
0.6.0 `256a29d5` repinned, and the two workarounds came out.

This is a generator trap, not a one-off: any bare variant in an Ethos file
is silently a payload variant if a type of that name is declared anywhere in
the same file, and nothing warns. `signal-aggregator`'s `ARCHITECTURE.md`
now records it for whoever adds the next variant, but the fix belongs in
Ethos Zero — refuse the ambiguity, or stop resolving bare heads against the
type table. That repository was another flow's tonight.

## router — not migrated, and why

Router's `main` is at `f60d4e33`, untouched by this flow. It is on
`nota`, the notation before Dotos, unconditionally in `src/channel.rs`,
`src/error.rs`, `src/cli_argument.rs`, `src/harness_delivery.rs` and both
writer binaries, with `dotos` behind a `dotos-text` feature for the CLI
and meta text surfaces.

The brief named router as on branch `f6db8d-cargo-update` `5fa990dc`.
Witnessed correction: `5fa990dc` is the head of `f6db8d-nota-pins`, not
`f6db8d-cargo-update`, whose head is `f15220b0`, an empty lockfile-only
commit described "cargo update (lockfile only) — FAILED". Both are
pushed to origin. `5fa990dc` carries the completed Dotos migration and
does not resolve. Witnessed, running `cargo metadata` in that checkout:

```
error: failed to select a version for `signal-persona`.
    ... required by package `signal-mind v0.8.0 (rev cf5d22c0)`
versions that meet the requirements `*` are: 0.2.1
package `signal-persona` links to the native library `signal-persona`,
but it conflicts with a previous package which links to
`signal-persona` as well:
package `signal-persona v0.3.1 (rev 0baf90c8)`
    ... which satisfies git dependency `signal-persona` of package
        `signal-harness v0.5.1 (rev 90e2878d)`
```

`signal-mind` and `signal-harness` pin incompatible `signal-persona`
revisions, and `links = "signal-persona"` admits only one. Witnessed in
the same way: router's `main` resolves cleanly. The Dotos branch is
strictly worse than main and must not land.

Migrating router to Datom is blocked outside router, on six repositories
this brief does not name and in part forbids. Witnessed, reading each
`Cargo.toml`:

| blocker | notation it is on |
|---|---|
| `signal-router` 0.7.0 | `dotos` behind `dotos-text`, over `signal-frame`; `schema/` present |
| `signal-harness` 0.5.1 | `dotos` behind `dotos-text`, over `signal-frame` |
| `signal-mind` 0.8.0 | `dotos` through `signal-frame/dotos-text`; `schema/` present |
| `signal-frame` 0.4.0 | `dotos`; carries its own `schema/` and `schema-rust/` trees |
| `triad-runtime` 0.7.0 | `nota`, behind `nota-text` |
| `sema-engine` 0.15.1 | `schema-rust` |

Three further walls sit on top of that dependency set. `signal-frame`'s
fate is an open question for the living — whether its envelope layer is
the protocol, and so whether it is absorbed into `signal` — recorded at
`flows/fe34eb/vision/signal.md:23` and carried in
`reports/datom-migration.md` §5; router cannot be moved off it before
that is answered. `src/harness_delivery.rs` writes NOTA text over a Unix
socket to the terminal component, so router's notation is half of a live
two-party protocol whose other half is out of scope. And `harness` is
named in the brief as not to be touched.

This flow therefore made no change to router and left no branch: a branch
carrying no migration is noise, and the two branches that exist are
already pushed. The checkout was moved from `5fa990dc` back onto `main`
so the next worker does not build on the Dotos branch by accident.

## Deployment

Witnessed: `aggregator` is a deployed CriomOS-home home-manager unit —
`modules/home/profiles/min/aggregator.nix`, with
`checks/aggregator-deployment/` and a flake input pinned at
`github:LiGoldragon/aggregator/f777eb2a`. That pin is older than
aggregator's `main` and is not moved by this flow; nothing was deployed
and no service was touched. Two consequences wait for whoever advances
that pin: the unit writes and reads
`${XDG_STATE_HOME}/aggregator/configuration.dotos`, which becomes
`configuration.datom`, and it invokes `aggregator-write-configuration
--local-default`, whose output format changes with it. Neither
`signal-aggregator` nor `meta-signal-aggregator` appears in any CriomOS
or CriomOS-home flake input; witnessed, the only consumer of either
contract anywhere under `/git/github.com/LiGoldragon` is `aggregator`
itself.

## What was kept, and the open question it leaves

`dotos-text-query` is kept as `aggregator`'s text matching engine, with
`default-features = false`. Witnessed: with default features off that
crate declares no `dotos` dependency at all — `dotos` is optional there
and reached only through its own `dotos-text` feature. The brief says to
leave it alone, and copying its matcher into aggregator would duplicate
the semantics rather than reuse them. Its types no longer reach the wire:
the contract's flat arenas are projected into and out of
`dotos_text_query::Query` and `MatchEvidence` at the engine boundary.

Open, and for the living: the crate is still named for the frozen
notation, as are `dotos`, `dotos-config` and `tree-sitter-dotos`.
Retiring or renaming them is a `repository-lifecycle` decision, not a
migration step, and `reports/datom-migration.md` §5 already raised it.
## The table

| repository | before | after | gate |
|---|---|---|---|
| signal-aggregator | 0.6.0 `5d2b80e2`, Dotos over signal-frame | **0.8.0** `e5009d65`, Ethos Zero 8.0.1 + Datom + signal 3.0.2, on main | green — test, fmt, clippy, doc, `nix flake check -L --builders ''`, run twice (witnessed) |
| meta-signal-aggregator | 0.4.0 `98cc36fc`, Dotos over signal-frame | **0.6.0** `55ac16ac`, same stack, on main | green — same five steps, run twice (witnessed) |
| aggregator | 0.4.0 `87c48f81`, "aggregator: migrate to dotos and pin git dependencies" | **0.6.0** `256a29d5`, on main | green — the 0.5.0 gate relayed from the subflow holding lock 1193, the 0.6.0 repin's five steps witnessed by this flow |
| router | 0.11.0 `f60d4e33` on `nota`, with a non-resolving Dotos branch at `5fa990dc` | **unchanged**, `f60d4e33` | not run — blocked upstream on six repositories outside this brief; see above |

## Sources

- Brief of main flow f6db8d to this subflow, 2026-09-11.
- `/home/li/primary/flows/f6db8d/reports/stack-membership.md` and
  `reports/nota-pins.md` (relayed) — what last night moved onto Dotos and
  why that reading was wrong.
- `/home/li/primary/flows/f6db8d/reports/datom-migration.md` (relayed) —
  the method followed here, and §5's account of the `dotos-text` estate
  and the unanswered `signal-frame` question.
- `/home/li/primary/Vision/datom.md:239-243` — read by this flow
  (witnessed). Distilled Vision: reviewed by the living, still written
  psyche.
- `flows/fe34eb/vision/signal.md:23` — cited through
  `reports/datom-migration.md` §5 (relayed); this flow did not read it.
- Working trees and `origin` refs under `/git/github.com/LiGoldragon/`
  for `signal-aggregator`, `meta-signal-aggregator`, `aggregator`,
  `router`, `ethos-zero`, `signal`, `signal-message`, `signal-introspect`,
  `dotos-text-query`, `signal-frame`, `signal-router`, `signal-harness`,
  `signal-mind`, `triad-runtime`, `sema-engine`, and
  `CriomOS-home` — read by this flow (witnessed).
- `orchestrate 'Observe.Locks'` before taking locks, and the six
  `Lock`/`Release` replies (witnessed): 1193 aggregator, 1194
  signal-aggregator, 1195 meta-signal-aggregator, 1196 router, then 1205
  and 1206 retaken for the variant-collision fix. All six released.
- Gate runs for `signal-aggregator` (0.7.0 and 0.8.0),
  `meta-signal-aggregator` (0.5.0 and 0.6.0) and `aggregator` 0.6.0 — run by
  this flow on this machine (witnessed). The `aggregator` 0.5.0 gate and the
  account of what that pass deleted and decided are relayed from the subflow
  that held lock 1193.
- The variant-collision defect was relayed by that subflow and then
  confirmed by this flow, witnessed: a walk over
  `src/generated/signal.rs` for every variant whose name equals its payload
  type, and the two new witnesses seen failing against the 0.7.0 contract
  before they passed against 0.8.0.
- The recursion finding is this flow's own experiment, witnessed: a
  minimal recursive Ethos Signal generated with `ethos-zero` `de3d9928`
  and compiled against `rkyv` 0.8 in a scratch crate.
