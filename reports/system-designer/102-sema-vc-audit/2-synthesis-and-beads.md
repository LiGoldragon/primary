# 102/2 — Synthesis and beads

## Verdict

**The SEMA version-control arc is sound where it shipped, but it is
half-deployed, and the deployed half has two production-path defects worth
fixing now.**

The arc's strongest claim — that the spirit intent corpus now lives on a
tamper-evident versioned store with a faithful, crash-safe migration — **holds
up under adversarial re-verification**. spirit is live at 0.12.0 on a migrated
v9 store; the v8→v9 logged fold that actually ran is correct; every migrated
row flows through the logged choke point; the swap is single-rename crash-safe
(the pre-fix two-rename window flagged in report 101 was genuinely fixed in
`9c8c44b`); and the sema-engine fold law, hash chain, content-addressed
checkpoints, fresh-only import, and **layout-4** guard all verify against the
code, not just tests. The mirror *daemon* is the best-built component in the
arc — single-writer kameo actor, payload-blind ingest, digest-verified dedup,
both reported wedges genuinely fixed. Credit where it is due (102/1 §"what held
up" detail, and the `whatHeldUp` list below).

Two things are not sound as deployed:

1. **The headline live gap is real and total: nothing ships to the mirror.**
   The component-side `ComponentShipper` exists only as a library type
   constructed in two test sites (`mirror/tests/end_to_end_arc.rs:250,390`);
   spirit has no `mirror` dependency, no drain loop, and the live
   `ObserveHeads` returns `[]`. The remote-durability promise of the arc — the
   `29pb` disaster-recovery intent — is **proven only in test, not live**, and
   nothing in the docs flags it. An operator seeing `mirror.service active`
   would reasonably but wrongly assume data is protected off-host.
2. **The mirror's TCP ingress binds `0.0.0.0:7474` with zero authentication at
   any layer** while BLS attestation is deferred; the bind-to-tailnet trust
   boundary the design relies on is defeated by `0.0.0.0`. The blast radius is
   bounded *today* (store idle, TCP can't reach the meta surface, `Append` is
   gated to already-registered stores) — but it converts to a live
   forged-append / store-fork risk the instant the shipper goes live, so it
   must be fixed **before** the shipper, not after.

The remaining confirmed defects are bounded and none can lose or corrupt live
data: a v7-referent migration abort (latent — live store is v8), a god-impl
beauty debt (three files over 1798–2118 lines against the explicit
"no thousand-line files"), the `Version`-verb axis collapse, and a handful of
well-cited naming/discipline warts. The one item the psyche should weigh
directly: the `TypeReference` reference-grammar is still hand-rolled
head-dispatch (a *build-time* codegen path, not runtime) against the explicit
"everything is a structural macro" commission — and the codebase currently
masks this by describing it as "not a hand-rolled parser." That is a real
derive-vocabulary limit that should be *surfaced* as such, per `v0n6`, rather
than papered over.

## Live state, reconciled

| Surface | State | Detail |
|---|---|---|
| spirit daemon | **Deployed & working** | Up at `0.12.0`, serving a v9 versioned store; v8→v9 fold ran in production; migrate-before-start is a real `ExecStartPre` hook, idempotent; the v9/v8 guard at store-open is intact and fail-closed |
| mirror daemon | **Deployed, up, IDLE** | working+meta unix sockets, TCP `0.0.0.0:7474`, `mirror.service` active; ledger dogfoods a versioned sema-engine store; daemon core sound — but `ObserveHeads = []` because nothing ships |
| remote durability (`29pb`) | **Test-only** | The end-to-end ship arc passes over loopback TCP as a fixture; no production shipper drives it |
| TCP authentication | **Missing** | No credential/allowlist check at any layer; the boundary is currently the host firewall/tailnet, not the daemon |
| retention enforcement | **Deferred** | Typed `RetentionSetting` stored; nothing prunes (explicit decision) |
| BLS attestation | **Deferred** | The intended per-request authenticity mechanism is not built |

**Deployed-and-working:** spirit v9 store + crash-resume; the migration hook;
the sema-engine fold/chain/checkpoint/import/layout-guard; the mirror daemon's
ingest/dedup/heal core; the local intent corpus is fully authoritative and
durable on the spirit host. **Proven-only-in-test:** the end-to-end ship arc;
the tamper-witness integrity raises; the `RecordFamily` hard-fail `decode()`
guard (its only caller today is in `#[cfg(test)]`); the v7→v9 and v1–v6
migration paths (only v8→v9 actually ran). **Missing entirely:** the production
shipper driver; TCP auth; retention enforcement; BLS attestation.

## What held up (honest credit, re-verified against `main`)

- The v8→v9 logged fold is faithful and crash-safe; the typed `Migration`
  marker is logged and materialized.
- The crash-window fix is real (`production_migration.rs:1051-1052`, commit
  `9c8c44b`) — 101/1's two-rename advisory is now correctly stale.
- The version probe is total and read-only; re-run on a v9 store is an
  idempotent `Current`.
- The mutation/retraction witness gap 101/1 flagged is closed
  (`versioned_store.rs:149,247`).
- The sema-engine fold layer is the strongest layer: real recompute-and-reject
  hash chain, content-verified checkpoints, engine-owned fresh-only import,
  hard layout-4 guard.
- The tamper witnesses are genuine — they drive the production
  rebuild/checkpoint/ingest paths and assert real flipped digests.
- The two mirror wedges are genuinely fixed and digest-verified; the dogfooding
  claim holds.
- The three NAMED macro-library hand-parsing sites were genuinely converted to
  derived `StructuralMacroNode` enums (`d7b34a2`) — the core commission landed.
- Family-identity / closed-`RecordFamily`-sum / hard-fail `decode` guarantees
  are real in the emitted code.
- Migrate-before-start is correctly encoded as `ExecStartPre` — better than
  report 101's "manual integration step" framing implied.

## Beads (audit output)

Filed to BEADS with topic labels (no role labels, per `orchestrate/AGENTS.md`).
Owner column is the natural lane, not a lock. Dependency: **D4-1 shipper must
not go live against the D4-2 unauthenticated ingress** — fix the bind first.

| Pri | Owner | Title | Closes |
|---|---|---|---|
| P1 | operator | Build the production mirror shipper driver in spirit | D4-1 |
| P1 | system-operator | Rebind mirror TCP ingress off `0.0.0.0` to the tailnet interface; land attestation before shipping | D4-2 |
| P1 | operator | Fix v7→v9 fold dropping referents (or reject v7 in the probe) | D2-1 |
| P2 | system-operator | Add failure escalation around the spirit migrate-store `ExecStartPre` | D1-3 |
| P2 | operator | Witness the v1–v6 migration fold or narrow the probe to reject it | D2-3 |
| P2 | designer | Widen `VersionReport` to carry the store-schema axis + surface `StoreSchemaHash` | D1-4, D1-5 |
| P2 | designer | Split `engine.rs` god-impl and `store.rs` to honor the crate-layout bar | D6-1 |
| P3 | designer | Make `RecordKey` a closed sum `Domain \| Identifier`; delete dead `MaterializeIdentifierParse` | D3-1, D3-3 |
| P3 | designer | Make `TypeReference` lowering a structural macro, or surface the derive-vocabulary gap to the psyche | D5-1 |
| P3 | designer | Collapse `SpiritStoreV1–V7` Database copy-paste into one generic; fix naming warts | D6-3, D6-4 |
| P3 | designer | Rename `mirror::MirrorTailnetClient` → `TailnetClient` | D6-2 |
| P3 | designer | Close the sema-engine commit-sequence/chain-head single-writer gap (`&mut self` or in-txn reads) | D3-2 |
| P3 | operator | Append `spirit-migrate-store` to the unmigrated-store error; sweep stale temp files | D1-2, D2-6 |
| P3 | designer | Carry typed nota errors in `schema-next SchemaError` via thiserror; doc v4/v5 weight drop | D5-5, D2-4 |

The three P1 beads are the gap between "the arc is done" and "the arc protects
data on a safe surface." Everything below P1 is bounded — none risks live data.
