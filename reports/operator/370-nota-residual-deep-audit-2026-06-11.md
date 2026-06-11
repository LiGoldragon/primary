# NOTA Residual Deep Audit

Operator audit of the remaining handwritten NOTA/parser traces after the Spirit/agent cleanup in `reports/operator/369-nota-parser-residual-audit-2026-06-11.md`.

## Scope

I scanned `/git/github.com/LiGoldragon` for production-source NOTA implementation traces:

- explicit `impl NotaDecode` / `impl NotaEncode`
- `from_nota_block`, `to_nota`, `NotaBlock::new`, direct `Block` / `Delimiter` matching
- `NotaSource::parse_root`
- stale generated `pub fn from_nota_block` / `pub fn to_nota` bridge methods under `src/schema`
- `signal_channel!` contracts, because `signal-frame` still macro-emits handwritten NOTA enum codecs

I excluded `target`, `.git`, `.jj`, and lockfiles from the searches. I did not change any code in this audit.

## Bottom Line

The current Spirit daemon path is clean with respect to the specific failure that triggered this: there are no handwritten `DomainScope` codecs, no string path helpers, and no `signal-spirit/nota-text` dependency compiled by Spirit. `spirit` also has no generated `pub fn from_nota_block` / `pub fn to_nota` bridge methods in its current checked-in schema modules.

The wider workspace is not globally clean. There are three real residual classes:

1. `signal-spirit` is still a hand-written active contract with custom `nota-text` implementations.
2. `signal-frame` still emits handwritten NOTA enum codecs for every `signal_channel!` contract.
3. Many older schema-derived repos still have checked-in generated `src/schema` files from before `schema-rust-next` stopped emitting bridge methods.

The strict global target is therefore not "regenerate Spirit once more." It is a sweep across contract style, generator style, and stale generated artifacts.

## Spirit Status

Current `spirit` main is clean for this issue.

Evidence:

- `spirit` has no hits for `pub fn from_nota_block`, `impl NotaDecode`, `impl NotaEncode`, `nota_next::Block`, `ScopePathImplTokens`, string `from_path` helpers, or the old `format!("{value:?}")` domain-scope matching pattern in `src/schema`, `schema`, `src`, `tests`, `build.rs`, or `Cargo.toml`.
- `spirit` is at commit `b9cf5321` (`spirit: send complete live context to guardian`).
- `schema-rust-next` is at commit `cedb2e06` (`schema-rust-next: stop emitting nota bridge methods`), and its tests explicitly assert generated code excludes `from_nota_block` and `fn to_nota(&self) -> String`.

I did not rerun Spirit in this audit because the relevant current-state check is source-shape, and the previous cleanup already ran Spirit cargo/Nix witnesses. The source scan confirms the old residual did not come back.

## Active Problem: signal-spirit

`signal-spirit` is the largest active remaining problem.

It is not schema-generated today. It has:

- no current `schema/lib.schema`
- a hand-written `src/lib.rs`
- a hand-written `signal_channel!` invocation
- custom `nota-text` impls for `Topics`, `RecordIdentifier`, `Date`, `Time`, `ObservationMode`, `Entry`, `TopicSelection`, `PublicRecordQuery`, and `RecordQuery`
- historical projection modules in `src/migration.rs` that derive NOTA for old production shapes

The default build is still binary-only and clean at the dependency boundary:

- `cargo test --no-default-features` passed
- `cargo test --features nota-text` passed
- dependency tests assert default builds do not pull `nota-next`, `nota-codec`, or `signal-core`

So this is not currently breaking the daemon. The problem is architectural: `signal-spirit` remains an active hand-written contract with handwritten text projection behind a feature. If the rule is zero active handwritten NOTA outside `nota-next`, `signal-spirit` must move to a schema-driven contract.

The migration is bigger than deleting a few impls because some hand-written codecs encode real compatibility behavior:

- `Entry` still accepts the older four-field shape and fills privacy as `Zero`.
- `ObservationMode` accepts legacy `DescriptionOnly` as `SummaryOnly`.
- `RecordIdentifier` uses a custom lowercase base36 code over a 96-bit byte value.
- `Date` and `Time` are compact atom forms rather than ordinary struct records.
- query types accept older shorter query shapes and fill defaults.

Those decisions need to become explicit schema/runtime migration objects or be deliberately retired. The current implementation hides them in codec code.

## Active Problem: signal-frame

`signal-frame` still emits handwritten NOTA codecs from `macros/src/emit.rs`.

The important function is `emit_nota_codecs`, which emits `impl nota_next::NotaEncode` and `impl nota_next::NotaDecode` for request/reply/event payload enums by directly wrapping and inspecting parenthesized NOTA objects.

That affects every hand-written contract using `signal_channel!`, including:

- `signal-spirit`
- `meta-signal-spirit`
- `signal-orchestrate`
- `signal-persona`
- `signal-mind`
- `signal-version-handover`
- `signal-repository-ledger`
- many `meta-signal-*` crates

This is macro-generated, not hand-typed in each contract, but it is still a handwritten NOTA implementation surface in the workspace. The durable options are:

- migrate those contracts to `schema-rust-next` `WireContract` emission and retire `signal_channel!` from active contract crates, or
- change `signal-frame` so the macro derives or delegates through `nota-next` derive machinery rather than emitting manual block-walking codecs.

The first option matches the current schema-derived stack direction better. The second option is a smaller containment step if `signal_channel!` survives longer.

## Stale Generated Artifacts

Many checked-in `src/schema/*.rs` files still contain old generated bridge methods:

- `pub fn from_nota_block(block: &nota_next::Block) -> Result<Self, NotaDecodeError>`
- `pub fn to_nota(&self) -> String`

Current `schema-rust-next` no longer emits those bridges. These repos are stale artifacts, not a live generator regression.

Repos with stale generated bridge methods include:

- `cloud`
- `domain-criome`
- `lojix`
- `message`
- `meta-signal-cloud`
- `meta-signal-domain-criome`
- `meta-signal-lojix`
- `meta-signal-orchestrate`
- `meta-signal-router`
- `meta-signal-upgrade`
- `mind`
- `orchestrate`
- `persona`
- `router`
- `signal-cloud`
- `signal-criome`
- `signal-domain-criome`
- `signal-lojix`
- `signal-message`
- `signal-orchestrate`
- `signal-router`
- `signal-terminal`
- `signal-upgrade`
- `terminal`
- `upgrade`

This class should be fixed mechanically: update each repo's schema-rust-next / schema-next / nota-next pins, regenerate, run its tests, and commit. It is a one-component-at-a-time sweep because these are active repos with independent check surfaces.

## Schema-next Boundary

`schema-next` is not the same kind of residual as `signal-spirit`.

It is a legitimate NOTA consumer: it owns schema-language semantics layered on raw NOTA. Its `SchemaSource` path reads `.schema` as typed source data using NOTA blocks and structural macro nodes. That is allowed by the architecture.

There is still hand-coded codec surface in `schema-next/src/schema.rs`, especially for semantic values such as `Name`, `SymbolPath`, `StructFieldMap`, and `TypeReference`. I would classify that as schema-language implementation debt, not forbidden raw parser slop. It belongs in a later schema-next cleanup only if the strict rule becomes "every non-core NOTA value codec must derive or be a structural macro node." It is not in the Spirit daemon text path and it is not the old DomainScope bug.

## Other Handwritten NOTA Surfaces

Other active or adjacent crates still contain explicit hand-written `NotaDecode` / `NotaEncode` implementations. The notable examples are:

- `version-projection`: `ComponentName`, `RecordKind`, and `ContractVersion`, where `ContractVersion` uses a `#hex` literal.
- `signal-sema`: `PatternField`, `Bind`, and `Wildcard`, using transparent pattern matching plus `(Bind)` / `(Wildcard)` markers.
- `signal-persona`: origin and socket-mode primitives.
- `signal-version-handover`: date/time and raw/mirror/divergence payload records.
- `signal-orchestrate`: validated string newtypes and `ActivityQuery`.
- `horizon-rs`, `lojix-cli`, `signal`, `mind`, `repository-ledger`, and several older component crates.

Some of these are typed scalar/newtype projections that may be acceptable temporarily. Some are contract surfaces that should become schema-emitted. The key is ownership: `nota-next` owns generic scalar/container codecs; schema-generated contract types should derive; contract-specific handwritten codecs need a clear reason or removal plan.

## Recommended Cleanup Order

1. `signal-spirit`: create the schema-driven ordinary Spirit contract and port the hand-written compatibility behavior into explicit schema/migration/runtime decisions. This removes the most active exception.
2. `signal-frame`: decide whether `signal_channel!` is being retired by schema `WireContract` emission or updated to stop emitting manual NOTA codec impls. Until this is done, hand-written contracts keep reintroducing macro-generated NOTA impls.
3. Stale generated repos: regenerate every listed `src/schema` surface against current `schema-rust-next`; these should be mostly mechanical, but run each repo's own checks.
4. Contract primitives: audit remaining explicit `impl NotaDecode` / `impl NotaEncode` outside `nota-next`, `schema-next`, and tests. Convert simple newtypes to derives where possible; escalate true custom syntax as a schema/NOTA design decision.
5. Add a fleet-level residual check: a script or Nix check that fails on `pub fn from_nota_block`, direct `impl NotaDecode` / `impl NotaEncode`, `NotaBlock::new`, and `signal_channel!` outside approved owner crates and tests.

## Witness Commands Run

- `cargo test --no-default-features` in `signal-spirit`: passed.
- `cargo test --features nota-text` in `signal-spirit`: passed.
- `cargo test` in `meta-signal-spirit`: passed.
- `cargo test` in `schema-rust-next`: passed.
- source scan over `/git/github.com/LiGoldragon` excluding `target`, `.git`, `.jj`, and lockfiles.

## Operator Read

The earlier caveat was accurate but understated. The active Spirit runtime is clean enough after the cleanup, but the workspace is not globally clean. The main active offender is `signal-spirit`, and the systemic offender is `signal-frame`'s `signal_channel!` macro. Stale generated files are widespread but mechanical.

The next production-quality step is not another local Spirit patch. It is a focused `signal-spirit` schema-driven migration, followed by retiring or cleaning the `signal_channel!` NOTA emission path.
