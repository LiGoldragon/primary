# 42 · Lojix production execution — running log

Execution against the staged plan in `reports/cloud-designer/41-lojix-production-refresh/11-synthesis.md`
(S0…S6), toward the psyche goalpost: the daemon-based logics running the
cluster, at feature parity with production `lojix-cli` (full-OS deploy,
survives SSH disconnect, every operation schema-typed), with two CLIs
(meta socket + regular socket). This file logs what actually landed, stage
by stage. Working straight on `main` in the triad repos (Spirit `o5rz`;
psyche re-authorized 2026-06-12).

Durable intent captured this arc: [the lojix component ships two CLIs — a
meta-socket CLI for the policy/owner contract and a regular-socket CLI for
the peer contract] (Spirit `ssk2`, Decision High).

## S1 · Schema modernization + dependency bump — DONE (2026-06-12)

**Reframe confirmed.** The psyche's "schema syntax changed; expect a
rewrite" was half-right: the `.schema` *grammar* changed (2026-06-09→06-11)
but lojix's `schema/nexus.schema` + `schema/sema.schema` were already on the
modern compact surface. The real work was a dependency refresh + artifact
regeneration, not a grammar rewrite (see report 41 file 4).

**The cascade.** `schema-rust-next` `cedb2e06` ("stop emitting nota bridge
methods") removes the inherent `from_nota_block`/`to_nota` convenience
methods from every generated artifact (the `NotaDecode`/`NotaEncode` trait
impls stay). Because the contract crates check in their generated `.rs`, the
removal made *their* artifacts stale — `signal-lojix`'s `build.rs`
freshness gate (`write_or_check("SIGNAL_LOJIX_UPDATE_SCHEMA_ARTIFACTS")`)
panicked before lojix could even regenerate its own. So a one-repo bump is
really a **triad-wide regen in dependency order**:
`signal-lojix → meta-signal-lojix → lojix`, each pushed to origin `main`
before the next consumer's `cargo update` could fetch it.

**What landed (each: bump codegen deps to current main, regen with the
crate's `*_UPDATE_SCHEMA_ARTIFACTS=1`, build green, push main):**

| repo | main before | main after | artifact change |
|---|---|---|---|
| signal-lojix | `b31cd980` | `c33e2be4` | `src/schema/lib.rs` −695 lines (0 bridge methods left) |
| meta-signal-lojix | `317b7fab` | `defade02` | `src/schema/lib.rs` −398 (picks up signal-lojix `c33e2be4`) |
| lojix | `13192bce` | `b3041914` | `nexus.rs` −353, `sema.rs` −331 (0 bridge methods left) |

Crate revs now current across the stack: `schema-rust-next cedb2e06`,
`schema-next 2397d5b2`, `nota-next 065fa2ad`, `signal-frame 166bda84`,
`triad-runtime 6ea83162`, `horizon-lib 9fae4a36` (the last two were already
current — the `DaemonConfiguration → BindingSurface` rename does not touch
any symbol lojix imports, so no code break).

**Verification.** No hand-written code called the removed inherent methods
(lojix uses the traits/derives only), so the break was artifacts-only.
lojix builds clean; the non-ignored suite is green on both gates —
default features 20 passed, `--features nota-text` 22 passed, 7 ignored
real-nix/live-daemon tests in each. No `.schema` grammar edits were needed
(the only candidate touch-ups — collapsing `(OrdinaryInput OrdinaryInput)`
self-pairs to `(OrdinaryInput)` — are cosmetic and were left alone).

## Next

- **S0 · Doc honesty.** Refresh the stale `signal-lojix` /
  `meta-signal-lojix` `INTENT.md` / `ARCHITECTURE.md` (they still describe
  the pre-split single contract with a non-existent `signal_channel!` macro
  and live streams), and manifest `ssk2` (two CLIs) into `lojix/INTENT.md`.
- **S2 · Two CLIs + bootstrap.** Narrow `src/bin/lojix.rs` to the ordinary
  socket; add `src/bin/meta-lojix.rs` (meta socket, mirroring
  `meta-spirit.rs`); add `lojix-write-configuration` (mirroring
  `spirit-write-configuration`); add the meta `Configure` op + virgin-daemon
  apply + SEMA self-resume. Spirit is the verbatim precedent.
