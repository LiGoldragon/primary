# Criome + Repository-ledger + Upgrade + Version-handover

> Two genuinely-built daemons anchor the cluster (criome with 7 real kameo actors, repository-ledger with 2), while upgrade is a large real migration/handover library wearing a placeholder daemon shell, and version-handover is contract-only. Fake-NOTA is effectively zero cluster-wide (the to_nota hits are all correct codec delegation or leaf literals), but the whole Criome triad is pinned to the flagged nota-next d8862b6 encoding bump while emitting from an older schema-rust-next — the single sharpest hazard — and a layer of stale .concept.schema cruft sits beside the live split/programmatic schema sources.

## Cluster: Criome + Repository-ledger + Upgrade + Version-handover

Two genuinely-built daemons anchor this cluster — **criome** (7 real kameo actors) and **repository-ledger** (2 real kameo actors) — while **upgrade** is a large real migration/handover engine wearing a placeholder daemon shell, and the seven signal/meta-signal crates plus both version-handover legs are contract-only by design. Fake-NOTA is **zero cluster-wide**; the headline risk is the entire Criome triad pinned to the flagged `nota-next d8862b6` encoding bump while emitting from a 6-7-commit-behind `schema-rust-next`.

### Per-repo table

| Repo | Role | Prod LOC | Gen LOC | Test LOC | Daemon shape | Intent | Free fns | Fake-NOTA |
|---|---|---:|---:|---:|---|---|---:|---:|
| criome | trust/attestation daemon | 3214 | 0 | 644 | real kameo (7 actors) | aligned | 5 | 0 |
| signal-criome | ordinary wire contract | ~105 | 3037 | 914 | contract-only | aligned | 0 | 0 |
| meta-signal-criome | meta config contract | 98 | 0 | 0 | contract-only | aligned | 0 | 0 |
| repository-ledger | event-ledger daemon | 2258 | 260 | 619 | real kameo (2 actors) | aligned | 2 | 0 |
| signal-repository-ledger | ordinary wire contract | 665 | 0 | 114 | contract-only | aligned | 0 | 0 |
| meta-signal-repository-ledger | meta config contract | 134 | 0 | 130 | contract-only | aligned | 0 | 0 |
| upgrade | upgrade/migration runtime | 2338 | 4372 | 823 | thin-CLI + scaffold daemon (no kameo) | mixed | 13 | 0 |
| signal-upgrade | ordinary wire contract | ~13 | 1444 | 497 | contract-only | aligned | 0 | 0 |
| meta-signal-upgrade | meta config contract | ~13 | 1267 | 511 | contract-only | aligned | 0 | 0 |
| signal-version-handover | private handover contract | 438 | 0 | 111 | contract-only | aligned | 0 | 0 |
| meta-signal-version-handover | meta config contract | 330 | 0 | 252 | contract-only | aligned | 0 | 0 |

LOC notes: prod = `src` minus inline `#[cfg(test)]` and `tests/`, generated `src/schema/*.rs` broken out separately. criome has **no** generated dir (fully hand-written runtime). The contract crates are dominated by `@generated schema-rust-next` output — their real hand-written prod surface is the small number shown (~13-105 LOC), which is exactly why they carry zero free functions and zero hand-rolled codecs.

### Daemon reality (not the README)

- **criome** — the only full multi-actor runtime: `CriomeRoot`, `IdentityRegistry`, `SubscriptionRegistry`, `AuthorizationCoordinator`, `StoreKernel`, `AttestationSigner`, `AttestationVerifier` (7 `impl Actor for`). `criome-daemon` runs `CriomeDaemonCommand::from_environment().run()`.
- **repository-ledger** — 2 real kameo actors (`RepositoryLedgerStoreActor`, `SpoolIngestActor` at `src/daemon.rs:340,418`), with the emitted triad-runtime listener shell owning only listener mechanics and a `SpoolIngestTicker` driving ingest on an interval.
- **upgrade** — **no kameo, no daemon loop.** `upgrade-daemon` (`src/bin/upgrade-daemon.rs`) calls `daemon_placeholder_response`, which validates one signal-file argument and prints a fixed string. `execution.rs:162 run_effect` returns stub values (`mirrored_write_count: 0`) and `budget_exhausted_reply` → `not_built_yet_output`. The genuine work — `MigrationCatalogue`, the persona-spirit `0.1.0→0.1.1` migration, handover acceptance/finalization, and the real `sema_engine` integration exercised by `upgrade-spirit-sandbox-test` — is a library behind a scaffold front.

### Dependency pins (Cargo.lock is the only pin surface)

`flake.lock` in every repo carries **only** the Nix toolchain (crane / fenix / nixpkgs / rust-analyzer / systems) — the foundation crates are cargo-vendored git deps, so there is **no Cargo.lock-vs-flake.lock disagreement** to flag; the stale Cargo.lock pin is the single source of truth for what links.

- **schema-next** is uniformly `77e71a4` = **5 behind** HEAD `c8ebb39` → no repo has today's terse-form grammar.
- **nota-next encoding-bump split-brain (the sharp hazard):** the whole Criome triad — **criome, signal-criome, meta-signal-criome** — pins `nota-next d8862b6` (HEAD, the **flagged** 2026-06-09 encoding bump) while pinning `schema-rust-next c0f76c2 / 261c779` (6-7 behind HEAD `eca4028`, which deliberately stays on the pre-bump `ae5c25cd`). Emitting from a pre-bump emitter while linking the post-bump nota runtime is exactly the encoding-format mismatch the bump warns about. **Every other repo** correctly stays on `nota-next ae5c25c` (4 behind) or older `f0e435a` (8 behind) — pre-bump and safe.
- Most-behind emitter pins: `schema-rust-next 0a845c3` (9 behind) in upgrade/signal-upgrade/meta-signal-upgrade; `7282446` (8 behind) in repository-ledger.

### Schema state — live source vs stale concept-cruft

- **criome.concept.schema** — OLD verbose self-tag form (`(Verify Verify)`, `(Observe Observe)`, `(Assert Assert)`); no build.rs reads it; types are hand-written → pure stale cruft.
- **repository-ledger** — daemon shape is generated **programmatically from `build.rs`** (`NexusDaemonShape::new(...)`) into `src/schema/daemon.rs`; **neither** `repository-ledger.concept.schema` (2026-05-24) **nor** `nexus.schema` (2026-06-08) is read → both stale, a live/stale duality to resolve.
- **upgrade / signal-upgrade / meta-signal-upgrade** — live source is `schema/lib.schema` (read by build.rs); each still carries a stale `*.concept.schema` (2026-05-24) beside it. **signal-criome already deleted its concept.schema** (cleanest migration in the cluster).
- **Terse-form debt (52ro self-tag repeats in live lib.schema):** upgrade 30, signal-criome 15, meta-signal-upgrade 11, signal-upgrade 4. upgrade also has `RawByte Integer` that should become the `yp29` `Bytes` leaf, and bare `Name String` newtypes that are now `qz6j`-distinct.

### Free-function violations (12 sites, ~13 fns)

- **criome (5):** `src/actors/mod.rs:26 rejection`, `:30 actor_reply` (a `From<CriomeReply>` in disguise), `src/actors/authorization.rs:281 authorization_store_rejection`, `src/actors/store.rs:535 active_status` (should be `StoredIdentity::is_active()`), `src/transport.rs:13 synthetic_exchange` (should be `ExchangeIdentifier::synthetic()`).
- **repository-ledger (2):** `src/lib.rs:1064 contains_case_insensitive`, `src/client.rs:294 encode_reply` (a bare `.to_nota()` wrapper).
- **upgrade (~6 fns across the worst sites):** `src/placeholder.rs:14/20/27/36/49` (an entire module of free fns — the scaffold layer, incl. `encode_nota` wrapping `.to_nota()`), `src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs:29/42/61/68/72/89` (the migration module is free-function-structured), `src/event.rs:232 contract_version_from_meta` (should be `impl From`), `src/handover.rs:520 acceptance_marker` (should be `HandoverAcceptance::marker()`), `src/catalogue.rs:209 rejection`.

The four contract crates (signal-criome, signal-upgrade, meta-signal-upgrade) and both version-handover legs have **zero** column-0 free functions — they are pure derive surfaces.

### Fake-NOTA: a clean result (count 0)

No repo hand-assembles paren-records — no `format!("(")`, no `push_str("(")`. Every `to_nota` is one of: (a) `Delimiter::Parenthesis.wrap([child.to_nota()...])`, the nota-next structural API delegating to each child's `NotaEncode` (e.g. `signal-version-handover/src/lib.rs:275 MirrorPayload`, `:315 DivergencePayload`); (b) a generated `<Self as NotaEncode>::to_nota(self)` forward under the `nota-text` feature (the bulk of the hits in the `@generated` files); or (c) a legitimate scalar-leaf literal — `Date` `YYYY-MM-DD`, `Time` `HH:MM:SS`, `RawPayload` `#hex`, `Catalog` `"()"`, integer `to_string`. **signal-version-handover is the best in-cluster reference** for correct hand-written NOTA encoding.

### What's most worth the psyche's attention

1. **Resolve the Criome-triad nota-next d8862b6 split-brain** — either back the three crates off the flagged encoding bump to pre-bump `ae5c25c`, or regenerate them from a `schema-rust-next` that has adopted the matching nota-next. As shipped, the generated code and the linked nota runtime disagree on encoding format.
2. **upgrade's daemon is a placeholder** while its migration/handover engine is real — the biggest completeness gap in the cluster; the engine has no real daemon front, and several `run_effect` handlers return stubs.
3. **Retire the stale `*.concept.schema` cruft** (criome, repository-ledger, upgrade, signal-upgrade, meta-signal-upgrade) and resolve repository-ledger's concept-vs-nexus duality — the live sources are the split `lib.schema` / programmatic `build.rs`, and the concept files mislead.
4. **Clear the 12 free-function sites**, concentrated in upgrade's `placeholder.rs` and migration module and in criome's actor helpers — each has an obvious owning noun (`From` impls, `StoredIdentity::is_active`, `HandoverAcceptance::marker`).
