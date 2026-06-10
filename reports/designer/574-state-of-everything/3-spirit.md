# Spirit stack (schema-derived pilot vs production)

> The cluster is two daemons running opposite experiments: spirit is the schema-derived future (70% generated, one generated kameo actor, build.rs-live triad-port schemas) but carries a real encoding-pin hazard — it links nota-next d8862b6 (the bump) while its schema-rust-next 9f50920 emits a codec built for ae5c25c — plus ~50 pre-52ro/pre-qz6j schema migration forms; persona-spirit is the production reality (13 hand-written kameo actors, zero generated code) and is clean of NOTA cheating but holds the cluster's only real free-function and fake-NOTA violations and a dead concept.schema. The two contract crates (signal-spirit, meta-signal-spirit) are clean and correct.

## Spirit stack — cluster audit (schema-derived pilot vs production)

The cluster runs two opposite experiments. `spirit` is the schema-derived future: ~70% of its source is generated from four split triad-port `.schema` files through a live `build.rs`, and its single kameo actor (`EngineActor`) is itself emitted. `persona-spirit` is the production reality until cutover: thirteen hand-written kameo actors, zero generated code, frozen on older foundation pins. The two contract crates (`signal-spirit`, `meta-signal-spirit`) are clean, correct, and aligned.

| repo | prod LOC | gen LOC | test LOC | daemon shape | actors | intent fit | nota-next pin | free-fn | fake-NOTA |
|---|---|---|---|---|---|---|---|---|---|
| spirit | 13205 | 9195 | 5499 | schema-derived daemon | 1 (generated `EngineActor`) | aligned | **d8862b6** (bump) | 0 | 0 |
| signal-spirit | 2491 | 0 | 1164 | contract-only | 0 | aligned | ae5c25c (4 behind) | 0 | 0 |
| meta-signal-spirit | 160 | 0 | 282 | contract-only | 0 | aligned | ae5c25c (4 behind) | 0 | 0 |
| persona-spirit | 7478 | 0 | 6401 | real kameo daemon | 13 (hand-written) | mixed | ae5c25c (4 behind) | 9 | 1 |

LOC note: `spirit` and the two contract crates have **zero** inline `#[cfg(test)]` in `src` (tests are external in `tests/`), so prod LOC equals `src` LOC. `persona-spirit` carries 896 inline `#[cfg(test)]` lines (largely `store.rs`), subtracted from its 8374 `src` total to give 7478 prod; its test total is 5505 (`tests/`) + 896 inline = 6401.

### The encoding-pin hazard (the flagged d8862b6)

`spirit` is the only repo on `nota-next d8862b6` — the encoding bump — and it is on it in **both** `Cargo.lock` and `flake.lock` (they agree, so there is no Cargo-vs-flake disagreement here). The hazard is one level deeper: `spirit` pins `schema-rust-next 9f50920`, and that revision — like HEAD `eca4028` — **internally pins `nota-next ae5c25c`**, the pre-bump encoding. So `spirit`'s checked-in generated codec (`src/schema/*.rs`, 9195 LOC) was emitted by an emitter built for `ae5c25c`, while the `nota-next` actually compiled into the daemon is `d8862b6`. The mismatch is `spirit`-vs-its-own-emitter, not lockfile-vs-lockfile. Resolution is either re-pin `nota-next` back to `ae5c25c` to match the emitter, or wait for a `schema-rust-next` revision that itself adopts `d8862b6` and regenerate. The other three repos all correctly stay on `ae5c25c`, matching their emitter — they are not exposed.

### The live/stale schema duality

`spirit`'s schemas are the **live source of truth**: `build.rs` generates 9195 LOC from `schema/{signal,nexus,sema,meta-signal}.schema` — the modern split triad-port form. But they are written in the **old grammar**: ~50 repeated `(Name Name)` variants (pre-`52ro` self-tag), pervasive bare-binding alias transparency (`State Statement`, `Record Entry` — exactly the pattern `qz6j` dropped), `Integer` digests (`StateDigest Integer`) rather than the `lm84` `Digest Bytes` newtype, and no `(Bytes N)` leaf. This is the bulk of the stack's migration debt and the reason the emitter pin is stuck pre-`eca4028`.

`persona-spirit`'s `schema/persona-spirit.concept.schema` is **stale cruft**: a 56-line single concept file dated May 26 stamped `(Status Concept) (Version 0 1)`, with **no `build.rs` consuming it**. It is contradicted by the live v0.5.x code — it declares `Entry [Topic Kind Description Magnitude]` (no multi-topic, no privacy, no daemon-stamped time) and `Identifier [u64]`, while the running store uses a minted base36-string `RecordIdentifier` and the privacy-aware multi-topic `Entry`. The real source of truth in `persona-spirit` is hand-written Rust; the `.concept.schema` is dead documentation. `meta-signal-spirit` carries the same kind of dead `.concept.schema` alongside its live `signal_channel!` macro.

### Free-function violations (all in persona-spirit)

`spirit`, `signal-spirit`, and `meta-signal-spirit` have **zero** free functions outside `fn main`. Every violation is in `persona-spirit`:

- `src/daemon.rs:1469` `serve_ordinary_stream` — the worst: a large free fn running the full read-frame / admit / reply / write-frame exchange. `daemon.rs` has **no `#[cfg(test)]` at all**, so this is pure production. Wants an owning noun (e.g. an `OrdinaryExchange` / `StreamServer`).
- `src/daemon.rs:1495` `receive_handoff_stream` — fd-passing recv over a control socket; method on the control-socket noun.
- `src/daemon.rs:730` `daemon_configuration_argument_text` and `src/migration.rs:661` `migration_configuration_argument_text` — argument-text builders that should hang off the configuration type.
- `src/migration.rs:348/368/388` `migrate_v010_to_v020` / `migrate_v020_to_next` / `migrate_v030_to_v040` — version bridges as loose fns; belong on bridge nouns per the `mod previous`/`mod next` discipline in the repo's own INTENT.
- `src/daemon.rs:1796` `io_error` — a `Display -> io::Error` wrapper that should be `impl From`.
- `src/store.rs:543` `spirit_contract_version` — a `pub const fn` at column 0 returning a const; a free function in disguise (wants `ContractVersion::current()` or an associated const).

### Fake-NOTA (one, in persona-spirit)

- `src/migration.rs:410` — `fn to_nota(&self) -> String { format!("(MigrationCompleted ({}))", self.records) }`. Hand-assembles a parenthesized record with `format!` instead of delegating to `nota-next`'s `Delimiter::Parenthesis.wrap` over a child `to_nota`, and hand-wraps the inner count rather than encoding it as a typed leaf. This is the sole genuine NOTA-cheat in the cluster.

The `to_nota` impls that a naive grep flags in `signal-spirit` (9) and `spirit` (1) are **correct, not cheating**: they call `Delimiter::Parenthesis/SquareBracket.wrap` delegating to child `to_nota`, the sanctioned encoder pattern. `signal-spirit`'s two `format!("{:04}-{:02}-{:02}")` / `format!("{:02}:{:02}:{:02}")` bodies format scalar date/time **leaf** values, not paren records, and are also fine.

### Verdict per repo

- **spirit** — aligned. A genuinely working schema-derived daemon with a clean code-discipline record. Its only real problems are dependency-shaped (the `nota-next d8862b6` / `schema-rust-next 9f50920` encoding mismatch) and grammar-shaped (~50 pre-`52ro` forms, pre-`qz6j` aliases, no `yp29`/`lm84` byte/hash adoption). Both are migration debt, not rot.
- **signal-spirit** — aligned, clean. Complete single-channel contract; only open item is its own deferred goal of becoming schema-emitted once the cross-crate import resolver lands. Mildly behind on `signal-frame`/`version-projection` (1 each).
- **meta-signal-spirit** — aligned, clean. A correct 160-line meta contract; the stale `.concept.schema` is harmless dead documentation worth deleting.
- **persona-spirit** — mixed. The running production daemon honors its functional INTENT well (dumb typed storage, multi-topic description-only shapes, daemon-stamped time, tested migrations, side-by-side deployment) but holds **all** the cluster's code-discipline violations (9 free fns, 1 fake-NOTA) and a dead `.concept.schema`, and is furthest behind on foundation pins (`schema-rust-next` 8 behind). Its thirteen hand-written actors are precisely the tree `spirit`'s emitter must eventually generate — cutover is a regeneration, not a pin bump.
