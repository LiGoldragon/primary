# 191.1 - Second-operator report agglomeration

Kind: Review  
Topic: second-operator report agglomeration after intent refresh  
Lane: second-operator  
Date: 2026-05-25  
Intent cut: Spirit record 651

## Frame

This report agglomerates `reports/second-operator/163` through `190`,
including the `179-design-schema-language-v4/` meta-report directory. It
uses the current hot intent window through Spirit record 651: schema delimiter
corrections in 628-631 and 635-636; schema emission split in 637-643; intent,
report, architecture, and code maintenance records 644-650; and report
agglomeration record 651.

No older report is edited or deleted here. This file is the carried-forward
current summary and the deletion plan.

## Current Load-Bearing Reports

| Report or cluster | Substance that still matters now | Status after this agglomeration |
|---|---|---|
| `184-orchestrate-short-header-ingress-implementation` | Orchestrate validates ordinary and owner `ShortHeader` values before service dispatch. The code-level witness is `orchestrate/tests/daemon_cli.rs` with mismatched-header socket tests. | Keep temporarily as the ordinary/owner ingress implementation witness until orchestrate schema-derived contract generation absorbs this into architecture and tests. |
| `186-orchestrate-upgrade-socket-implementation` | Orchestrate has a private upgrade socket, validates upgrade-frame short headers, accepts Mirror before readiness, finalizes handover, and removes ordinary/owner socket paths on completion. Remaining gaps are durable divergence recording, recovery semantics, and old-process termination. | Keep as the current orchestrate handover status report. It supersedes `185` for active desk context. |
| `190-schema-mainline-macro-index-port` | Schema main now reads through `nota_codec::parse_sequence` and `ShapeParser`; `SchemaDocument`, `MacroIndex`, `MacroPipeline`, and `TypeMicroMacro` make the macro-front path real on main. Remaining holes are fixed-point iteration, user macro loading, lazy imported macro lookup, upgrade-code emission, and deletion of the old streaming parser. | Keep as the current schema macro-engine status report until the next schema emission slice lands. |
| This `191` directory | Carries the intent-cut frame plus this agglomeration. It becomes the current report-context entry point for second-operator. | Keep. The older load-bearing residue is carried below. |

Everything else in 163-190 is either a shipped-slice witness whose durable
home is code/tests/commits, a stale context-refresh snapshot, or a design
proposal superseded by newer intent and code.

## Carried-Forward Substance

| Older report(s) | Substance now carried forward |
|---|---|
| `163`, `166` | The lane registry slice shipped: lane vocabulary, owner register/retire/set-authority, store-backed lane table, and observe-lanes behavior. Retired lane identifiers can disappear for now. The old broader `primary-c620` migration report should not be used as current architecture without re-auditing current orchestrate code. |
| `167` | Old Persona engine residue is inactive desk context. Durable lessons are already skill/code-level: typed daemon config, no polling, push subscriptions, actor-density tests, resource-owner restart tests, and architectural truth tests. |
| `168` | Mind should not call Router owner signal directly. The authority chain remains Mind -> owner-signal-orchestrate -> owner-signal-router. The exact Spirit-to-Mind owner verb set and channel-list/adjudication read boundaries remain future design, not current second-operator implementation. |
| `169` | Criome/Lojix authorization remains unfinished but inactive here: real signal-criome client, pushed authorization observations, cryptographic verification, owner approval operations, and Arca preservation still need future work when that topic resumes. |
| `173`-`176` | These are context-refresh snapshots. Their active message is now: refresh intent before choosing work; report lanes are not archives; schema/macro work displaced persona-orchestrate as the hottest local context on 2026-05-24; bracket-string and schema-source corrections were already moving faster than the reports. |
| `177`-`178` | `schema` exists as its own repo and active core repo. Bootstrap facts still true: typed schema metadata, validation, namespace map key support, local imports, and repo guidance files exist. The initial section model is superseded by later six-position schema code and delimiter corrections. |
| `179/` | The meta-report correctly rejected pseudo-NOTA: no outer wrapper, namespace maps are real maps, imports are schema namespace imports, type expressions are data-carrying forms, and comments should not carry schema meaning. Its four-field header-set proposal and its older enum/record examples are superseded by current six-position code and records 628-631/635-636. |
| `180`-`181` | The schema crate crossed from model to language reader: six top-level `.schema` objects, local relative imports, headers, namespace, features, and upgrade annotations parse from real fixtures. The streaming-parser reader and some delimiter examples are superseded by `190` and current code. |
| `182`-`183` | Orchestrate gained parser-backed schema files and tests. The `/tmp` designer prototype should be mined as a target spec, not merged wholesale. Current work must route reusable schema lowering through `schema`, not deepen private `signal-frame-macros` schema readers. |
| `185` | Mirror snapshot body is real and typed, but active context moves to `186`, where the private upgrade socket actually carries Mirror before readiness. |
| `187`-`189` | These established the "real vs not real" boundary for NOTA-node shape parsing and schema macros. `190` makes the strongest part real on main: `Schema::parse_str` uses `NotaValue` shape parsing and the multi-pass pipeline indexes macro candidates. Fixed-point and code emission remain open. |

## Superseded Or Stale

| Superseded item | Superseded by | Current reading |
|---|---|---|
| `179` four-field schema spine: headers/imports/namespace/surfaces | `180`-`181` code and `190` mainline model | The current code surface is six positions: imports, ordinary header, owner header, sema header, namespace, features. If psyche wants to reopen arity, ask directly; do not infer from `179`. |
| `179` / early `180` examples using brackets for enums or parenthesized named fields | Spirit 628-631 and 635-636; current fixture `spirit-v0-1-1.schema` | Parentheses carry enum/variant choices. Square brackets carry struct/field vectors. This applies globally, not only to the examples that triggered the correction. |
| Field records like `(topic Topic)` | Spirit 610-611 and 617; current parser | Field names are inferred from type names. Struct declarations should be field vectors like `Entry [Topic Kind Summary]`; named lowercase field records are rejected except where a container expression is being parsed. |
| Streaming parser as the conceptual schema reader | `190` and current `schema/src/shape_parser.rs` | `Schema::parse_str` now goes through `nota_codec::parse_sequence` and `NotaValue` shape methods. The old streaming parser is only a compatibility/equivalence backstop. |
| `187`-`189` "feature branch real, main no" status | `190` | Main now has the macro-index path. The remaining not-real pieces are fixed-point iteration, user macro loading, lazy imported macro lookup, and `VersionProjection` / Rust emission from upgrade plans. |
| Any schema-derived Rust path that routes through `signal_channel!` | Spirit 637-643 and current `signal-frame` code | The new proc macro is `emit_schema!`. The old body macro is `legacy_signal_channel!`; `signal_channel!` is only a compatibility alias during migration. `schema_entry.rs` uses `schema::LoadedSchema` and `schema_rust::RustComposer`, not `ChannelSpec`. |
| `signal-frame` architecture prose that still describes `signal_channel!` as the normal schema-era integration target | Spirit 637-643 and code in `signal-frame/macros/src/lib.rs` plus `schema-rust/` | The architecture file is stale in places. A later allowed maintenance pass should refresh it; this report only records the mismatch. |
| Orchestrate schema integration as parser-only witness | `184` and `186` | Orchestrate now has production short-header ingress checks and a private version-handover socket. Schema-derived contract generation remains separate future work. |

## Constraint Table

| Area | Current constraint | Evidence / cut | Status and next action |
|---|---|---|---|
| Intent refresh | Maintenance and implementation start by refreshing Spirit, tracking the intent cut and hot-topic window. | Spirit 644-645; this report cut is 651. | Apply on every report/code pass. Reports should name the cut when they synthesize state. |
| Report lane | Reports are not an archive. Agglomerate, keep a small current set, and retire stale originals once substance is carried forward. | Spirit 107, 119-121, 362, 646, 651. | This report carries the old lane substance. Follow with scoped deletion, not more summary reports. |
| Schema delimiter rule | Parentheses are enum/variant forms; square brackets are struct/field vectors. | Spirit 628-631, 635. | Audit every schema example and parser branch globally, not only header examples. |
| Correction scope | Psyche design corrections apply to the whole design unless explicitly scoped. | Spirit 636. | Treat delimiter reversal and header-root corrections as global schema-language rules. |
| `.schema` file shape | Current code reads exactly six top-level values with no outer wrapper: imports, ordinary header, owner header, sema header, namespace, features. | `schema/src/document.rs`, `schema/src/shape_parser.rs`, `schema/src/multi_pass.rs`; reports `180`, `181`, `190`. | Keep unless psyche explicitly replaces the top-level arity. `179` four-field proposal is not current. |
| Header roots | Header roots are ordered dispatch roots whose endpoints are vectors. | Spirit 472, 474-475, 494-495; `schema/src/shape_parser.rs`. | Continue using `(Root [Endpoint...])`, including one-endpoint roots. |
| Namespace values | Namespace map keys are names; values are declarations. Fields infer names from types. | Spirit 461-462, 610-611, 617; current fixture. | Avoid `Entry (Entry ...)` and avoid authored lowercase field-name records. |
| Imports | Imports are a map of explicit import variants and selected names; collisions fail. | Spirit 480-483, 613, 622; `schema/src/shape_parser.rs`. | Keep explicit `Import` / `ImportAll`; maintain collision tests. |
| Schema macro substrate | A universal NOTA parser produces `NotaValue` trees; schema dispatch uses node shape methods plus schema position. | Spirit 549, 588-590, 600, 607-609; reports `187`-`190`. | `190` lands this on main. Next: fixed point, user macro loading, lazy macro imports. |
| Schema assembly | The macro path lowers into canonical `AssembledSchema`; names should be unambiguous by context and ultimately fully qualified where needed. | Spirit 479, 490, 612, 619, 623; `schema::AssembledSchema`. | Keep `AssembledSchema` as the consumer object for emission and upgrade. |
| Upgrade | The next version carries upgrade knowledge and assembles against the previous version; ambiguous transforms need explicit annotations. | Spirit 488, 491, 552, 561-562. | `plan_upgrade_from` is real. `VersionProjection` emission is not real yet. |
| Rust emission | Schema-derived Rust emission is a fresh top-down composer from `AssembledSchema`, not a wrapper around legacy macros. | Spirit 637-643; `signal-frame/macros/src/schema_entry.rs`; `signal-frame/schema-rust/src/lib.rs`; Nix guard `schema-macro-does-not-use-legacy-emitter`. | `emit_schema!` and `legacy_signal_channel!` split exists. Next: expand composer beyond current route/type scaffolding and remove stale architecture prose. |
| Orchestrate ingress | Decode must validate short-header root against generated contract-owned kind before service dispatch. | Report `184`; `orchestrate/src/daemon.rs`; `tests/daemon_cli.rs`. | Ordinary and owner sockets covered. Keep tests as contract. |
| Orchestrate handover | Orchestrate private upgrade socket carries version handover; Mirror occurs before readiness for critical state. | Reports `185`-`186`; `orchestrate/src/handover.rs`; `orchestrate/src/daemon.rs`. | Remaining decisions: divergence ledger, recovery, dynamic role snapshot boundary, old daemon exit. |
| Branch topology | Designers work feature branches in `~/wt`; operators maintain and rebase main. | Spirit 516, 518; report `183`. | `/tmp` prototype branches are mined as specs, not treated as living authoritative worktrees. |
| Repo intent surfaces | Repository `INTENT.md` files are core maintained surfaces. | Spirit 648. | Future maintenance should audit `schema`, `signal-frame`, and `orchestrate` repo `INTENT.md` files after code/report deletion. |
| Implementation taste | If implementation feels contorted, reopen the library/interface question; code should be elegant, succinct, and self-describing. | Spirit 649-650. | Use this before adding compatibility layers around stale macro APIs. Prefer a clean interface change to preserving an ugly call path. |

## Recommended Retirement Plan

Immediate retirement candidates after this report is committed:

- `163-lane-registry-implementation-result-2026-05-22.md`
- `166-review-persona-orchestrate-migration-2026-05-22.md`
- `167-review-persona-engine-backlog-2026-05-22.md`
- `168-review-mind-router-policy-2026-05-22.md`
- `169-review-criome-lojix-authorization-2026-05-22.md`
- `173-current-state-after-consolidation-2026-05-23.md`
- `174-review-after-skill-and-intent-refresh-2026-05-24.md`
- `175-context-refresh-intent-and-reports-2026-05-24.md`
- `176-designer-awareness-beads-and-report-audit-2026-05-24.md`
- `177-schema-repository-bootstrap-2026-05-24.md`
- `178-schema-section-shape-and-nota-map-check-2026-05-24.md`
- `179-design-schema-language-v4/` as one retired meta-report directory
- `180-schema-v13-model-and-upgrade-implementation-2026-05-24.md`
- `181-schema-e2e-reader-and-redesign-2026-05-24.md`
- `182-orchestrate-schema-mainline-integration-2026-05-24.md`
- `183-orchestrate-worktree-audit-and-rework-2026-05-25.md`
- `185-orchestrate-mirror-handover-implementation-2026-05-25.md`
- `187-nota-shape-logic-and-schema-upgrade-macro-2026-05-25.md`
- `188-real-schema-node-method-macro-situation-2026-05-25.md`
- `189-schema-engine-running-model-2026-05-25.md`

Keep for now:

- `184-orchestrate-short-header-ingress-implementation-2026-05-25.md`
- `186-orchestrate-upgrade-socket-implementation-2026-05-25.md`
- `190-schema-mainline-macro-index-port-2026-05-25.md`
- `191-intent-context-maintenance-2026-05-25/`

That leaves the lane with four active report entries: one current context
directory, one schema macro-engine report, and two orchestrate implementation
witnesses. The retained set is below the soft cap and can be read in one pass.

## Open Questions

1. **Is the six-position `.schema` top-level shape still the active shape?**
   Current code and reports `180`, `181`, and `190` use six positions:
   imports, ordinary header, owner header, sema header, namespace, features.
   Report `179` proposed a four-field header-set spine, but later code and
   tests moved to six. Recent intent 628-636 corrects delimiter semantics
   globally; it does not explicitly restate top-level arity. If the psyche
   wants the four-field shape reopened, it should be an explicit design turn.

2. **When should the old streaming schema parser be deleted?** Main now uses
   the `NotaValue` shape parser, while the streaming parser remains as an
   equivalence backstop. Keeping both too long risks drift; deleting too soon
   removes a diagnostic comparator before Spirit and Orchestrate both consume
   the new path. My lean: delete after one clean integration cycle where
   Spirit and Orchestrate both parse through the shape path and tests still
   prove equivalent `AssembledSchema` output.

3. **What is orchestrate's final handover state boundary?** The current Mirror
   snapshot carries claims and lanes. Dynamic roles are also orchestration
   policy state, but `185` followed the critical-state list named at the time.
   The remaining choice is whether to extend Mirror to dynamic roles and
   whether version-handover divergence reuses the existing `divergences` table
   or gets a separate handover-failure ledger.
