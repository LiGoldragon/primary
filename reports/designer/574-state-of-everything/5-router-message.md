# Router + Message ingress

> A genuinely healthy cluster: router is a real 8-actor kameo daemon with durable sema-engine storage, message is the honest stateless schema-emitted ingress daemon, and the four contract crates are clean generated wire vocabulary. The whole cluster is structurally sound; the real debt is uniform foundation-pin lag — every repo trails schema-rust-next by 8-9 commits, so all checked-in generated code still carries the qz6j transparent `pub type` aliases that a regeneration will break — plus two stale `*.concept.schema` cruft files and one architectural laggard (meta-signal-message, still on the legacy signal_channel! macro with no schema/ or generated code).

## Cluster: Router + Message ingress

A genuinely healthy cluster. `router` is a real 8-actor kameo daemon with durable `sema-engine` storage; `message` is the honest stateless schema-emitted ingress daemon (CLI + emitted async-task spine, no actors); the four contract crates are clean generated wire vocabulary. Structurally sound throughout. The real debt is uniform foundation-pin lag (every repo trails `schema-rust-next` by 8-9 commits, so all checked-in generated code still carries the qz6j transparent `pub type` aliases a regeneration will break), two stale `*.concept.schema` cruft files, and one architectural laggard (`meta-signal-message`, still on the legacy `signal_channel!` macro).

### Per-repo summary

| Repo | Role | prodLoc | testLoc | gen | Daemon shape | Fit | schema-next | schema-rust-next | nota-next | free fn | fake NOTA |
|---|---|--:|--:|--:|---|---|---|---|---|--:|--:|
| router | component daemon | 5604 | 3237 | 2864 | real kameo, 8 actors | aligned | 77e71a4 (−5) | 7282446 (−8) | ae5c25c (−4) | 2 | 0 |
| signal-router | ordinary contract | 60 | 413 | 985 | contract-only | aligned | 77e71a4 (−5) | 0a845c3 (−9) | ae5c25c (−4) | 0 | 0 |
| meta-signal-router | meta contract | 17 | 189 | 950 | contract-only | aligned | 77e71a4 (−5) | 0a845c3 (−9) | ae5c25c (−4) | 0 | 0 |
| message | ingress daemon + CLI | 1507 | 388 | 2870 | thin-CLI + emitted async-task daemon (no kameo) | aligned | 77e71a4 (−5) | 7282446 (−8) | ae5c25c (−4) | 0 | 0 |
| signal-message | ordinary contract | 104 | 375 | 1469 | contract-only | aligned | 77e71a4 (−5) | 0a845c3 (−9) | ae5c25c (−4) | 0 | 0 |
| meta-signal-message | meta contract (legacy macro) | 106 | 0 | 0 | contract-only / `signal_channel!` | drifting | 77e71a4 (−5, transitive) | 7282446 (transitive, unused) | 16493c8 (−3) | 0 | 0 |

prodLoc = non-blank `src` lines minus `src/schema/*` generated and minus inline `#[cfg(test)]`; `gen` = checked-in generated `src/schema/*.rs`. Distances are commits-behind the foundation HEADs (schema-next c8ebb39, schema-rust-next eca4028, nota-next d8862b6). `flake.lock` pins no foundation crates in any repo (only nixpkgs/fenix/crane), so `Cargo.lock` is the sole pin source and no Cargo-vs-flake disagreement is possible.

### Findings

**Daemon reality (README-independent).** `router` is the only repo with hand-written kameo actors — eight of them: `RouterRuntime`, `RouterRoot`, `ChannelAuthority`, `HarnessRegistry`, `HarnessDelivery`, `MindAdjudicationOutbox`, `RouterObservationPlane`, `SupervisionPhase` (entrypoint `RouterProcessDaemon::run_to_exit_code()`; durable state via `RouterTables` opening a `sema_engine::Engine`; config read binary-rkyv-only in `src/config.rs` via `from_rkyv_bytes`/`from_binary_path`, correctly rejecting NOTA per the one-argument daemon rule). `message` is NOT kameo — it is the schema-emitted async-task `ComponentDaemon for MessageDaemon` (~69 hand-written lines over the generated spine in `src/schema/daemon.rs`), with a thin `message` CLI client and an honest no-op `Stateless` SEMA plane. The four `signal-*`/`meta-signal-*` crates are contract-only (no kameo, no tokio).

**Foundation lag is the dominant, uniform debt.** Every consumer pins `schema-next 77e71a4` (5 behind c8ebb39, which includes today's FixedBytes(N) grammar). `schema-rust-next` splits by tier: the daemons (`router`, `message`) pin `7282446` (8 behind), the contracts (`signal-router`, `meta-signal-router`, `signal-message`) pin `0a845c3` (9 behind). The intervening commits matter: `a259139` integrated the no-alias schema-next (qz6j) and `44e472b` switched newtype emission to a private wrapped field — so a regeneration against `eca4028` is **breaking, not byte-stable**. Concretely, every consumer's checked-in `src/schema/*.rs` still emits transparent `pub type X = Y` aliases (router 57, message 46, meta-signal-router 28, signal-router 17, signal-message 9) that the current emitter no longer produces. The generated code is a generation behind the emitter that produced it.

**d8862b6 flag is clean.** No consumer pins `nota-next d8862b6` (the encoding bump). Five repos pin `ae5c25c` (the deliberately-isolated rev, 4 behind); `meta-signal-message` alone pins `16493c8` (3 behind, one commit *ahead* of its siblings, sitting between `ae5c25c` and the d8862b6 encoding work). That is a minor intra-cluster nota-next skew worth aligning, not the dangerous emit-vs-encode mismatch the flag warned about.

**Stale schema cruft.** `router/schema/router.concept.schema` (status `Concept`, last touched May 24) and `signal-router/schema/signal-router.concept.schema` (May 24) are dead: `build.rs` references only the split `signal/nexus/sema.schema` (router) or `lib.schema` (signal-router), all touched June 6-8. Both concept files use the OLD verbose `(X X)` self-tag form. Delete them. Even the *live* schemas have not adopted today's terse `(Name)` self-tag (52ro): `router/nexus.schema` carries 16 `(X X)` repetitions, `message/nexus.schema` 11. No `Bytes` leaf appears anywhere in the cluster — expected, since these are routing/ingress contracts with no hash identifiers, so yp29/lm84 are non-applicable here (not a gap).

**meta-signal-message is the one architectural laggard.** Its content satisfies INTENT (completes `message`'s contract pair; `Configure(MessageDaemonConfiguration)` carries the typed config record), but it is the lone repo still hand-written on the legacy `signal-frame::signal_channel!` macro — no `schema/` dir, no `build.rs`, no generated `src/schema/`, no `tests/`. Its direct counterpart `meta-signal-router` is fully migrated to the generated `schema/lib.schema -> src/schema/lib.rs` shape with round-trip tests, and the `router` INTENT explicitly states future signal/meta-signal deps must follow that schema-next/schema-rust-next shape. Its `schema-rust-next 7282446` pin is transitive (via `signal-message`), confirming it uses no emitter. It also lacks the rkyv+NOTA round-trip witness tests every sibling contract carries.

### Free-function violations (2 total, both router)

| Repo | Location | Name | Why |
|---|---|---|---|
| router | src/supervision.rs:331 | `io_error` | Module-level free fn `fn io_error(error: impl Display) -> io::Error` wrapping `io::Error::new(InvalidData, ...)`, outside `#[cfg(test)]`/`main`. It is a conversion — should be `impl From<E> for io::Error` or a method on the error-bearing type. |
| router | src/router.rs:85 | `synthetic_exchange` | Module-level free fn `fn synthetic_exchange() -> ExchangeIdentifier` minting a fixed ExchangeIdentifier, outside `#[cfg(test)]`/`main`. A constructor doing ExchangeIdentifier's job — should be associated fn `ExchangeIdentifier::synthetic()`. |

### Fake-NOTA violations (0 total)

None. Every NOTA path in the cluster uses the real nota-next codec API. The hundreds of `to_nota` methods are legitimate emitter output in `src/schema/*.rs`. The hand-written cases were each verified legitimate: `message/src/command.rs` impls `NotaEncode`/`NotaDecode` for its CLI-local `Input`/`Output` using `Delimiter::Parenthesis.wrap(...)` (the official nota-next encoder, `nota-next/src/parser.rs:289`) and `NotaBody::from_delimited(...)` (the official parser), delegating payloads to child `.to_nota()`/`from_nota_block` — the prescribed manual pattern, identical in shape to emitter output (a minor smell only: sibling records use `#[derive(...)]`, so this hand-impl could be a derive). `router/src/router.rs:2195,2865` likewise delegate to child `.to_nota()` via `Delimiter::wrap`. `signal-router/src/lib.rs:39` `to_nota_lines` delegates to `operation.to_nota()` then newline-joins (legitimate bootstrap line format). `meta-signal-message/src/lib.rs:40` `ConfigurationGeneration::to_nota` returns `self.0.to_string()` — correct u64-newtype integer delegation.
