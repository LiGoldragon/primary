# BUILD H1 — re-add MirrorTarget to the meta-signal-spirit contract

Slice: re-add the `MirrorTarget` / `MirrorAddress` / `MirrorAddressText`
schema nouns and the `mirror_target` slot on the meta `ConfigureRequest`
(and `ConfigureReceipt`) so spirit's re-landed mirror-shipper feature has a
contract to compile against.

## Result

- Branch (jj bookmark): `mirror-target-reland`
- Worktree: `~/wt/github.com/LiGoldragon/meta-signal-spirit/mirror-target-reland`
  (jj workspace `mirror-target-reland`, off `main@origin` 3283925f — "use
  generated standard newtype impls").
- Build: GREEN. `cargo build`, `cargo test`, and `cargo test --features
  nota-text` all pass.
- Not pushed (operator integrates).

## What history showed

`MirrorTarget` / `MirrorAddress` never appeared in meta-signal-spirit's own
git history — `git log -S MirrorTarget --all` and `-S MirrorAddress --all`
both return empty. The noun lived in spirit's dropped `store-decomposition`
history (per spirit `src/shipper.rs` doc-comment, designer report 669/P1),
back when spirit owned its meta contract inline; it was lost when spirit
moved to re-exporting the external `meta-signal-spirit` crate, whose
`ConfigureRequest(ArchiveDatabaseTarget)` carries no mirror target. So the
shape is recovered not from this repo's history but from spirit's live
mirror-shipper consumer, which is the canonical spec.

## The exact shape spirit needs (the spec)

Cross-checked against spirit's mirror-shipper worktree
(`~/wt/github.com/LiGoldragon/spirit/mirror-shipper/`):

`src/shipper.rs` `MirrorShipper::configure`:

- `target: Option<&MirrorTarget>`, matched as `Some(MirrorTarget::Address(address))`
  and `Some(MirrorTarget::Default) | None` — so `MirrorTarget` is an enum
  with `Default` and `Address(MirrorAddress)`.
- `address.payload().payload()` returns `&String` — so
  `MirrorAddress::payload() -> &MirrorAddressText` and
  `MirrorAddressText::payload() -> &String` (a two-hop newtype chain, the
  same pattern as `ArchivePath` / `ArchivePathText`).

`tests/mirror_shipper.rs`:

- `MirrorTarget::Address(MirrorAddress::new(MirrorAddressText::new(address.to_string())))`
  — `MirrorAddressText::new` accepts a `String` (`impl Into<String>`),
  `MirrorAddress::new` accepts a `MirrorAddressText`.
- `ConfigureRequest { archive_database_target: ArchiveDatabaseTarget::Default,
  mirror_target: Some(mirror_target(address)) }` and `mirror_target: None` —
  so `ConfigureRequest` is a NAMED-FIELD struct with a
  `mirror_target: Option<MirrorTarget>` field, not the current newtype.

## Schema delta

`schema/meta-signal.schema` — three new noun lines plus the two struct
bodies gaining a field:

```
  MirrorAddressText String
  MirrorAddress { MirrorAddressText * }
  MirrorTarget [Default (Address MirrorAddress)]

  ConfigureRequest { ArchiveDatabaseTarget * mirror_target (Optional MirrorTarget) }
  ConfigureReceipt { ArchiveDatabaseTarget * mirror_target (Optional MirrorTarget) DatabaseMarker * }
```

(Before: `ConfigureRequest { ArchiveDatabaseTarget * }`,
`ConfigureReceipt { ArchiveDatabaseTarget * DatabaseMarker * }`.)

Adding the second field flips `ConfigureRequest` from a generated tuple
newtype `ConfigureRequest(ArchiveDatabaseTarget)` to a named-field struct
`ConfigureRequest { archive_database_target, mirror_target }` — exactly the
shape the spirit test constructs. `(Optional X)` generates an `Option<X>`
field (confirmed against `signal-spirit` `VerbatimQuote.antecedent` and
`lojix` `DeployJob`). `mirror_target` is given explicitly because the
auto-name form (`Noun *`) and the `(Optional ...)` wrapper don't combine.

`ConfigureReceipt` also gains `mirror_target` so the receipt echoes the
now-active target — matching the dropped shape the shipper doc-comment
records ("`mirror_target` field on `ConfigureRequest` / `ConfigureReceipt`")
and the engine's stated "reply with the now-active target" intent.

## Regeneration command (NO hand-edited generated Rust)

```
META_SIGNAL_SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo build
```

The crate's `build.rs` drives `schema_rust_next::build::GenerationDriver`
and calls `.write_or_check("META_SIGNAL_SPIRIT_UPDATE_SCHEMA_ARTIFACTS")`:
with the env var set it WRITES `src/schema/meta_signal.rs` from the
`.schema`; unset it only CHECKS freshness. `src/schema/meta_signal.rs` was
regenerated, never hand-written.

Generated surface (verified) matches spirit's call sites exactly:

- `pub struct MirrorAddressText(String)` with `new(impl Into<String>)`,
  `payload() -> &String`.
- `pub struct MirrorAddress(MirrorAddressText)` with `new(MirrorAddressText)`,
  `payload() -> &MirrorAddressText`.
- `pub enum MirrorTarget { Default, Address(MirrorAddress) }` plus
  `MirrorTarget::address(MirrorAddressText)` and `From<MirrorAddress>`.
- `pub struct ConfigureRequest { archive_database_target, mirror_target: Option<MirrorTarget> }`.
- `pub struct ConfigureReceipt { archive_database_target, mirror_target: Option<MirrorTarget>, database_marker }`.

These reach spirit via `lib.rs`'s `pub use schema::meta_signal::*` and
spirit's `pub use meta_signal_spirit::schema::meta_signal::*`, so spirit's
`use spirit::schema::meta_signal::{... MirrorAddress, MirrorAddressText,
MirrorTarget ...}` resolves.

## Build / test result

- `cargo build` — finished clean.
- `cargo test` (default features): `dependency_boundary` 2/2, `frame` 1/1,
  `round_trip` 0 (gated on `nota-text`). All green.
- `cargo test --features nota-text`: `dependency_boundary` 2/2, `frame` 1/1,
  `round_trip` 4/4. All green.

Crate-local test fixtures updated to the new shape (hand-written tests, not
generated): `tests/frame.rs` and `tests/round_trip.rs` switched from
`ConfigureRequest::new(...)` (gone — the newtype constructor) to the named
struct literal, added a `Some(MirrorTarget::Address(...))` round-trip, and
added `mirror_target: None` to the `ConfigureReceipt` literal.
`examples/canonical.nota` updated to the encoder's actual output. NOTA
encodings learned empirically from the round-trip assertions:

- `Option::None` encodes as the bare atom `None`; `Some(x)` as `(Some x)`.
- A two-field struct payload wraps in parens: `Configure` of
  `{Default, None}` is `(Configure (Default None))` (the prior single-field
  form `(Configure Default)` flattened).
- `(Configure (Default (Some (Address 100.64.0.7:7777))))` and
  `(Configured (Default None (1 2)))` are the new canonical lines.

## Blocker for the spirit feature compiling end-to-end (downstream slice)

This slice unblocks gap (1) of two from spirit `src/shipper.rs`. The
contract is now correct, but spirit's `mirror-shipper` feature will NOT
fully compile yet on two counts, neither in this triad repo:

1. SPIRIT-SIDE ADAPTATION (separate slice). Spirit's `src/engine.rs`
   `configure()` (lines 452-460, NOT feature-gated) still treats
   `ConfigureRequest` as the old newtype: it calls `request.into_payload()`
   (which the named-field struct no longer has) and builds
   `ConfigureReceipt { archive_database_target, database_marker }` (missing
   the new `mirror_target` field). It also never reads `mirror_target` nor
   passes it to `MirrorShipper::configure`. So even with this contract,
   `engine.rs` must be adapted to read `request.mirror_target`, arm the
   shipper, and populate the receipt's `mirror_target`. That is spirit-repo
   work, out of this contract slice's scope. The mirror-shipper TEST already
   expects the new struct shape; engine.rs lags it — an internal spirit
   inconsistency this contract exposes.

2. MIRROR-SIDE (gap 2 from shipper.rs, unrelated to this slice). The only
   `mirror::ComponentShipper` taking a shared `Arc<sema_engine::Engine>` is
   on mirror's `arc-shipper` branch, which itself fails against today's tree
   (stale `nota-next` 0.4.0 vs current `signal-mirror` 0.5.0). The
   `Arc<Engine>` shipper must be forward-ported onto mirror main's current
   `nota-next` base — a mirror-repo change.

The meta-signal-spirit contract delta here is complete, builds, and tests
green; the remaining work to make spirit's `mirror-shipper` feature itself
compile is the spirit `engine.rs` adaptation (1) and the mirror forward-port
(2).
