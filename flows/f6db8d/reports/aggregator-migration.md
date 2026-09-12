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
variant.** Witnessed: `OperationKind.[ Configure ObserveConfiguration
ValidateConfiguration ]` generated
`ObserveConfiguration(ObserveConfiguration)` because a type of that name
was also declared. Renaming the type to `ConfigurationObservationQuery`
fixed it. Whether that is intended is unknown to this flow; it is
recorded as observed behavior, not as a defect.

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
- `orchestrate 'Observe.Locks'` before taking locks, and the four
  `Lock`/`Release` replies (witnessed): 1193 aggregator, 1194
  signal-aggregator, 1195 meta-signal-aggregator, 1196 router. All four
  released.
- Gate runs for `signal-aggregator` and `meta-signal-aggregator` — run by
  this flow on this machine (witnessed). The `aggregator` gate is relayed
  from the subflow that held lock 1193 and did that repository's work.
- The recursion finding is this flow's own experiment, witnessed: a
  minimal recursive Ethos Signal generated with `ethos-zero` `de3d9928`
  and compiled against `rkyv` 0.8 in a scratch crate.
