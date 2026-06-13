# 102/1 — Verified findings by dimension

*Every finding below was raised by a deep-read finder and then independently
re-checked by at least one skeptic prompted to refute it (High/Critical: a
second, impact-lens skeptic). Severity and verdict are the post-skeptic values.
Refuted findings are dropped except where the refutation is itself the lesson.
Citations are `file:line` on each repo's `main`.*

Severity legend: **Critical** data-loss/corruption/live-breakage possible ·
**High** correctness bug or intent violation that will bite · **Medium** real
gap with a workaround · **Low** polish · **Info** confirmed-sound or
finding-accuracy note.

## D1 — Deployment & version truth

The deploy shape is healthier than the "manual migration that takes the daemon
down" framing implied. Migrate-before-start IS encoded as a systemd
`ExecStartPre` hook in the deployed home-manager unit
(`CriomOS-home modules/home/profiles/min/spirit.nix:191`, via
`initializeState → migrateState → spirit-migrate-store`), the migration is
idempotent (a v9 store reports `Current` and changes nothing), and
`sema-engine-previous` is pinned to exactly the `ebee6e44` engine that wrote
the live v8 store. The recurrence risk is contained by deploy infrastructure,
not bare operator discipline. The real remaining gaps are about
*observability*: the unmigrated-store error never names the remediation tool, a
failed migration blocks start silently, and the `Version` verb collapses three
version axes into one package number.

| ID | Sev | Verdict | Finding | Fix |
|---|---|---|---|---|
| D1-1 | Info | Confirmed | Migrate-before-start IS encoded as `ExecStartPre`, idempotent | None — record it; the transient down was a deploy that bypassed the hook or a transient failure, not a missing step |
| D1-4 | Medium | Confirmed | `spirit Version` reports only `CARGO_PKG_VERSION` (0.12.0); store schema (9) and wire version invisible | Widen `VersionReport` to a positional record over the axes (bead) |
| D1-3 | Medium | Confirmed | A failing migration aborts the unit before `ExecStart` with only untagged journald — no `OnFailure`/alert | Tag migrate-store NOTA output in journal + start-limit-failure alert (bead) |
| D1-2 | Low | Partial | Unmigrated-store error is honest about *what* but never names `spirit-migrate-store` (and the literal message says "layout 3" while the build is layout 4) | `StoreError::Database` Display appends the tool name |
| D1-5 | Low | Partial | Engine-derived `StoreSchemaHash` exists but no live spirit verb surfaces it | Surface on `Version`/`Marker` when widening (folds into D1-4) |
| D1-7 | Low | Confirmed | Report 101 frames migration as a manual handoff item and omits the version-surface collapse | Amend 101's dossier (this report does that) |
| D1-6 | Info | Confirmed | Built artifact version reads 0.12.0 consistently — the package axis is honest | None |

## D2 — Migration correctness

The logged-fold core is sound and the path that actually ran (v8→v9) is
correct: every migrated row flows through the `database.assert` choke point
(`spirit src/store.rs:387, 406, 550`), the typed `Migration` marker is logged
and materialized, and the swap is single-rename crash-safe (`hard_link` backup
first at `production_migration.rs:1051`, then ONE `rename` at `:1052`). Report
101/1's two-rename crash-window advisory was genuinely fixed in commit
`9c8c44b` and is now stale. One real correctness bug survives, latent for the
live (v8) store but live for any v7 store.

| ID | Sev | Verdict | Finding | Fix |
|---|---|---|---|---|
| D2-1 | **High** | Confirmed | **v7→v9 fold imports zero referents but preserves `entry.referents`** — any v7 record carrying a referent aborts the whole migration on `UnregisteredReferent` (fail-safe, no corruption); the v7 witness masks it with empty referents | Give the v7 path a referent-table read + non-empty witness, or reject v7 in the probe (bead) |
| D2-3 | Medium | Confirmed | v1–v6 From-chain has no test witness — readers/category-mappings compiled but never run | Add a text-category and an enum-category witness, or narrow the probe (bead) |
| D2-6 | Low | Confirmed | Stale migration temp file not swept on re-run despite the doc claiming it is (PID-suffixed; only current PID's temp removed) | Glob-sweep `schema-9-migrating-*.sema` or soften the doc |
| D2-5 | Low | Partial | v7 domain bridge bounces typed→`Debug`-text→typed through `NotaSource` (not hand-rolled; dormant on the v8 path) | Prefer `impl From<v7::Domain> for Domain` |
| D2-4 | Info | Partial | v4/v5 legacy `weight` silently dropped — intended (retired pre-v6 at `8fe88d6`), undocumented | One doc sentence; assert surviving fields if a v4/v5 witness lands |
| D2-2 | Info | Confirmed | Logged choke points + crash-safe single-rename swap correct; 101/1 advisory is stale | None — record so future audits don't re-raise |

## D3 — sema-engine versioned fold

The strongest layer of the arc. The fold law (`view = fold(checkpoint,
suffix)`) holds: every live mutation lands its row, legacy log row, versioned
hash-chained entry, and mirror outbox row in ONE redb transaction through the
single `insert_versioned_row` choke point (`engine.rs:2021`). The hash chain
recomputes each entry digest from its own fields and rejects link mismatch
(`fold.rs:147`); checkpoints are content-addressed and refold-verified
(`checkpoint.rs:558`); import is engine-owned, fresh-only (`&mut Engine`), and
re-derives + checks `StoreSchemaHash`; the **layout-4** guard hard-refuses any
non-current store (`engine.rs:1699`) — this is what makes migration mandatory
and blocks silent corruption. Tamper witnesses drive the real
verify/fold/ingest/rebuild paths. The residue is discipline-level, not
correctness.

| ID | Sev | Verdict | Finding | Fix |
|---|---|---|---|---|
| D3-1 | Low | Confirmed | `RecordKey` domain-vs-identifier is `{kind, value:String}` — stringifies a typed `u64` and re-parses on materialize | Make it `enum RecordKey { Domain(String), Identifier(RecordIdentifier) }`; `identifier_value()` becomes infallible (bead) |
| D3-2 | Low | Partial | Commit-sequence + chain-head digest read outside the write txn on `&self`, no engine lock — concurrent callers could fork the chain | Cannot bite production (single actor serializes); take `&mut self` or fold reads into the write txn + document the single-writer contract (bead) |
| D3-3 | Low | Confirmed | Dead error variant `MaterializeIdentifierParse` — declared, never constructed | Delete it (or retire with the `RecordKey` closed-sum change) |
| D3-4 | Info | Confirmed | Fold law, hash chain, content-addressed checkpoint, fresh-only import, layout-4 guard all verify as claimed | None |
| D3-5 | Info | Confirmed | Tamper witnesses assert on the production load/verify/ingest/rebuild paths, not past them | None |

## D4 — Mirror server (the remote)

The mirror *daemon* is the best-built component in the arc: a single kameo
`Service` actor owns the one `Engine` writer across all three listeners (no
`Arc<Mutex>`, one `Message<Verb>` impl per verb), ingest is genuinely
payload-blind, dedup is digest-verified (`decision.rs known_divergence`),
gap/fork/empty rejections are closed typed sums, the two reported wedges are
really fixed and tested, and the ledger dogfoods a versioned sema-engine store.
But the loop is not closed and the network surface is open.

| ID | Sev | Verdict | Finding | Fix |
|---|---|---|---|---|
| D4-1 | **High** | Confirmed | **Production component-side shipper is unbuilt** — `ComponentShipper` is constructed only in two test sites; spirit has no `mirror` dependency, no drain loop; `ObserveHeads` stays `[]`; `29pb` remote durability is test-only, not live | Build a shipper driver in spirit; state plainly in INTENT/ARCHITECTURE that remote durability is not yet live (bead) |
| D4-2 | **High** | Confirmed | **TCP append-ingest on `0.0.0.0:7474` has no auth/authz at any layer**; BLS deferred; `0.0.0.0` defeats the design's bind-to-tailnet trust boundary | Rebind to the tailnet interface now (cheap); land attestation before the shipper goes live (bead) |
| D4-3 | Low | Partial | Meta surface is owner-only by socket file-mode (0o600) alone — no uid check in `handle_meta_connection` | Add a uid==owner check for defense-in-depth (TCP cannot reach meta, so Low) |
| D4-4 | Info | Confirmed | Both wedges genuinely fixed and digest-verified; no analogous wedge found | Add a contiguity assertion at the shipper boundary when D4-1 lands |
| D4-5 | Info | Partial | Single-writer, per-verb-message, payload-blind, dogfooded, discipline all hold | None |
| D4-6 | Info | Confirmed | Retention is a stored-but-unenforced typed placeholder by explicit decision | When enforcement lands, reconcile with the retire/re-register resume invariant |

## D5 — Schema / identity / generation

The content-identity and family-emission guarantees are real and the psyche's
core commission was delivered: the **three named macro-library hand-parsing
sites were genuinely converted** to `#[shape]`-derived `StructuralMacroNode`
enums (commit `d7b34a2`). `ContentHash` is blake3 over canonical rkyv with
deterministic ordering (`identity.rs:78,160`); `family_identity` consts are
computed at generation as `[u8;32]` literals; the closed `RecordFamily` sum's
`decode()` hard-fails on `SchemaHashMismatch`/`UnknownFamily` with no silent
fallthrough (`schema-rust-next lib.rs:3946`). The one real gap against
"everything should be a structural macro" is the `TypeReference` lowering.

| ID | Sev | Verdict | Finding | Fix |
|---|---|---|---|---|
| D5-1 | Medium | Partial | `TypeReference` reference-grammar lowering is hand-rolled head-dispatch (`match head {Vec\|Vector,...}`) copied across five sites, one already drifted — against the structural-macro commission; build-time codegen only, no runtime risk | Extend the derive vocabulary to make it a `StructuralMacroNode`, or centralize to one path + surface the derive-vocabulary gap to the psyche (bead) |
| D5-5 | Low | Partial | `schema-next SchemaError` hand-written without thiserror; two nota leaf errors stringified (`Nota(String)`/`NotaDecode(String)`) | Carry the typed nota errors; adopt thiserror |
| D5-2 | Low | Refuted | "masking premise — not a hand-rolled parser" | Skeptic refuted: `from_block` operates over nota-next's already-lexed `Block` tree, and `parsers.md` carves out `text.parse::<u64>()`; survives only as a Low doc note on why `TypeReference` keeps a hand codec |
| D5-3 | Info | Confirmed | The three named hand-parsing sites genuinely converted to derived structural macros | None — commission delivered |
| D5-4 | Info | Confirmed | Family identity, closed sum, hard-fail decode are generation-time and corruption-safe | None (dormant until a consumer wires `decode` outside tests) |

## D6 — Discipline & beauty

The hand-authored Rust is disciplined on the hard rules: no anyhow/eyre
anywhere; typed per-crate thiserror enums; no module-level free functions
outside `fn main`/`#[cfg(test)]`; the mirror unit structs are legitimate
type-level markers (not ZST namespaces); the guardian-journal hand-typed
identity is still the *only* sanctioned exception. The top ESSENCE-ladder
failure is the psyche's explicit "no thousand-line files," violated three
times.

| ID | Sev | Verdict | Finding | Fix |
|---|---|---|---|---|
| D6-1 | Medium | Partial | Three files far exceed the ~300-line bar: `engine.rs` 2118 (god-impl, ~1957-line `impl Engine`, 69 methods), `production_migration.rs` 1988, `store.rs` 1798 — no correctness impact | Split `impl Engine` into the fold/log/checkpoint/catalog/query modules it already aggregates; pull store.rs migration-marker/family-directory plumbing onto their own files (bead) |
| D6-3 | Medium | Confirmed | Five byte-identical `SpiritStoreV1/V4/V5/V6/V7` `open`/`records()` impls differ only by constant + record type | Collapse into one generic `PreviousVersionTable<R>`; keep V8 as the lone specialization (bead) |
| D6-2 | Low | Confirmed | Crate-prefix cleanup (`69fe4e7`) missed `mirror::MirrorTailnetClient` (added one commit earlier) | Rename to `TailnetClient` (bead, bundled) |
| D6-4 | Low | Confirmed | `SpiritStorePreviousStore` double-`Store` compound; `archived_records()` a verbatim alias of `records()`; `SpiritStoreV8Database` `Option<TableReference>` as a live/archive flag | Rename; delete alias; model live/archive as two reader types (bead, bundled) |
| D6-5 | Info | Confirmed | Guardian-journal hand-typed family identity is STILL the only sanctioned exception; justification holds | None |
| D6-6 | Info | Partial | `marker_key` stringly format is justified, but the "only stringly record-key mint" survey was wrong — `store.rs:544 archive_identifier` is a second (also justified) | Finding-accuracy note only |
