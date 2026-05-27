# 394 — Report audit + retirement (designer/)

*Kind: Review · Topics: discipline, workspace · 2026-05-27*

*Per spirit record 920 (lane retirement), record 941 (topic-prefix
filenames), and `skills/context-maintenance.md` drop / forward /
migrate / keep discipline: audit of `reports/designer/`. The earlier
38 entries trim to 21 by retiring substance that has migrated into
permanent docs, been absorbed by newer canonical reports
(/387/389/390/391/392), or carries explicit RETRACTION banners
naming records 713-715. Two reports stay under the design-rationale
guard (`skills/context-maintenance.md` §3a) with their existing
status banners; the remaining entries are the active working
surface.*

## Dropped — substance migrated or superseded

| Report | Reason | Successor / destination |
|---|---|---|
| `101-heresy-inventory-2026-05-25.md` | Schema-crystallized-architecture audit; framing has moved on. Heresy taxonomy from records 656-664 is no longer load-bearing as forward design; the chosen designs migrated to per-repo INTENT.md and ARCHITECTURE.md per /341 status banner. | Absorbed: `/341` (design-rationale kept) + per-repo INTENT/ARCH per /393 manifestation pass |
| `102-context-refresh-schema-as-channel-2026-05-25.md` | Schema-as-channel-contract reframing from records 668-670. Framing absorbed into the unified vision (/361) and runtime-triad framing (/371). | Absorbed: `/361`, `/371` |
| `105-implementation-showcase-2026-05-25.md` | RETRACTED per records 713-715 (EffectTable/FanOutTargets/StorageDescriptor are runtime dispatch, not authored schema features). Substance no longer load-bearing as forward design. | Records 713-715; canonical schema in `signal-persona-spirit/spirit.schema` |
| `106-schema-driven-poc-from-v0.3-main-2026-05-26.md` | RETRACTED per records 713-715. The authored Features sections are drift. | Records 713-715 |
| `107-signal-frame-self-hosting-bootstrap-2026-05-26.md` | RETRACTED per records 713-715 (any Features-section scaffolding the bootstrap touched is drift). Pure enum declarations survive in canonical schemas. | Records 713-715 |
| `349-context-maintenance-sweep-2026-05-25/` (meta-dir) | Earlier context-maintenance meta-directory from 2026-05-25. Successor sweeps (/377 designer-side, /386 cross-lane) absorb the discipline + leave a current working surface. | `/377`, `/386` |
| `354-schema-derived-nota-prototype-2026-05-26.md` | Prototype landings (records 746-753); substance shipped to `schema-next`, `schema-rust-next`, `nota-next` and absorbed into /361's six-layer vision. The prototype itself was the empirical foothold, not the lasting artifact. | Absorbed: `/361`, current `schema-next` main |
| `356-new-repos-and-block-parser-prototype-2026-05-26.md` | New-repos creation (`spirit`, `signal-spirit`, `core-signal-spirit`, `nota-next`) + block-parsing prototype. The repos exist; the prototype substance is on operator main. | Absorbed: live repos + `nota-next` main |
| `358-nota-library-schema-schema-prototype-2026-05-26.md` | NOTA-library + schema-schema prototype (records 799-807). Substance landed in operator's `schema-next` + `nota-next` real implementations. | Absorbed: live crates |
| `368-running-spirit-concept-on-new-architecture-2026-05-26.md` | Running-spirit-concept end-to-end. The chain exists in operator's `spirit-next`; the design substance is in /374 + /389 + /390. | Absorbed: live `spirit-next`, `/374`, `/389`, `/390` |
| `370-implementation-gap-audit-designer-side-2026-05-26.md` | Designer-side gap audit complementing operator/206. Gap list absorbed into /389 §"What operator does next" + /390 §"Implementation status" + /391 §"What operator does next". | Absorbed: `/389`, `/390`, `/391` |
| `372-design-signal-frame-schema-concept-2026-05-26.md` | Signal-frame-schema concept proving root-level schema. Subsumed by /390's wire-runtime canonical direction (records 860 + 935). | Absorbed: `/390` |
| `375-finish-macro-engine-and-use-it-2026-05-26.md` | Macro engine completion + spirit.schema authoring exercise. The macro engine is on operator main (records 888-890); substance in /387 + /389. | Absorbed: live `schema-next` main, `/387`, `/389` |
| `378-rust-skill-review-2026-05-27.md` | Rust skills review. All edits landed in `skills/rust/methods.md`, `skills/rust/parsers.md`, `skills/rust/crate-layout.md`, `skills/rust-discipline.md`. The audit substance IS the skill edits. | Migrated: skill files (no longer needs the report) |
| `379-rust-method-rule-audit-and-fix-2026-05-27.md` | Method-rule audit substance is in Nix-enforced checks (`schema-next/flake.nix`, `schema-rust-next/flake.nix`, `nota-next/flake.nix`) + `skills/rust/methods.md`. Named in /391 as explicit retirement candidate. | Migrated: Nix checks + skill; successor `/391` |
| `380-bottom-up-tour-02-schema-macros-2026-05-27.md` | Bottom-up tour Layer 2. The brace-as-key/value-map + dynamic-enum framing now first-class in records 894/932/940; canonical-direction synthesis in /389. Named in /389 §"What this report supersedes". | Successor `/389` (recursive-struct framing) |
| `381-schema-design-truth-finding-2026-05-27.md` | Audit of /380. Since /380 retires and /387/388/389 carry the current canonical schema design, the audit-of-stale-predecessor is now stale itself. | Absorbed: `/387`, `/388`, `/389` |
| `384-emit-to-src-schema-2026-05-27.md` | src/schema emission target per record 909. Substance has landed on operator main (`spirit-next` `0296be2`) + /391 §"The src/schema target — locked". Named in /391 §"What this report supersedes". | Successor `/391` |
| `385-nota-schema-next-stack-design-via-nix-tests-2026-05-27.md` | Five-scenario design via Nix tests. Superseded by /387's 8-section side-by-side mermaid + tests (covers BOTH layers — NOTA and schema). Named in /387 §"What this report supersedes". | Successor `/387` |

Total drops: **19 reports + 1 meta-directory** = 20 entries.

## Refreshed (status banner) — none added this pass

No new status banners landed this pass. The two design-rationale-guard reports (/341, /363) already carried banners from earlier sweeps; their substance and banners are correct as-is. The other surviving reports either are recent enough to need no banner or carry their own forward-looking status in their opening sections.

## Renamed (topic-prefix applied) — none

The topic-prefix convention is forward-only (record 941); renames happen incrementally when a report is touched. No surviving reports were touched for substance reasons this pass, so none received a topic-prefix rename. The next agent doing context maintenance can opportunistically rename when they edit.

The retained reports keeping their pre-941 filenames (no topic prefix in the filename — the topics are in the report headers / opening sections):

- `341-schema-crystallizes-architecture-2026-05-25.md`
- `351-intent-file-tour-2026-05-26.md`
- `352-intent-log-audit-2026-05-26.md`
- `361-latest-vision-schema-derived-nota-stack-2026-05-26.md`
- `363-design-nota-from-schema-comparison-2026-05-26.md`
- `366-component-view-and-truth-verification-2026-05-26.md`
- `367-nota-as-specification-superset-of-capnproto-2026-05-26.md`
- `371-signal-executor-sema-runtime-triad-and-federation-2026-05-26.md`
- `374-deep-spirit-parallel-implementation-2026-05-26.md`
- `376-bottom-up-tour-01-nota-2026-05-27.md`
- `377-context-maintenance-sweep-2026-05-27.md`
- `382-pair-style-sweep-2026-05-27.md`
- `383-next-version-schema-design-study-and-implement-2026-05-27.md`
- `387-nota-schema-design-representation-2026-05-27.md`
- `388-macro-system-exploration-and-brace-enum-sugar-2026-05-27.md`

## Kept untouched — load-bearing reports

| Report | Why kept |
|---|---|
| `341-schema-crystallizes-architecture-2026-05-25.md` | Design-rationale guard (`skills/context-maintenance.md` §3a) — enumerates competing alternatives (P5 InteractTrait + InteractionActor retracted per record 666; effect-table/fan-out further retracted per records 713-715). Status banner already names permanent-doc landings. |
| `351-intent-file-tour-2026-05-26.md` | Intent-file relocation audit per records 717-719. Per /386 §"Handoff section" item 2: migrate to `skills/intent-log.md` / `skills/repo-intent.md` then drop. Migration not yet performed; kept until done. |
| `352-intent-log-audit-2026-05-26.md` | Flagged-for-psyche-review report per record 719 (agents may FLAG, never delete). Psyche review pending; kept until psyche acts on the flags. |
| `361-latest-vision-schema-derived-nota-stack-2026-05-26.md` | Entry-point synthesis of /357 + /199 + /358 + /359 + /360. Still useful as a wide-scope orientation; partial substance has migrated to /389/390/391/392 but the unified vision is what /361 is FOR. The newer /392 is THE primary vision now — /361 is the prior-arc artifact. May absorb fully into /392 in a future pass. |
| `363-design-nota-from-schema-comparison-2026-05-26.md` | Design-rationale guard — enumerates wider vs narrower recursion-floor cuts; verdict (hybrid) migrated to /361 §4 + §12. Status banner already in place. |
| `366-component-view-and-truth-verification-2026-05-26.md` | Component truth-verification table. Recommended migration target: per-repo `ARCHITECTURE.md`. Migration not yet performed; kept until done. |
| `367-nota-as-specification-superset-of-capnproto-2026-05-26.md` | NOTA-as-CapnProto-superset framing (records 839-844). Pending migration to `nota/INTENT.md` + `schema/INTENT.md`; status banner already names the destination. |
| `371-signal-executor-sema-runtime-triad-and-federation-2026-05-26.md` | Federation framing (records 856-859) — signal + executor + SEMA runtime triad. Still load-bearing as the architectural framing for the runtime layer; not yet absorbed into a per-repo ARCH that fully replaces it. |
| `374-deep-spirit-parallel-implementation-2026-05-26.md` | Designer-parallel implementation of v0.3-capability schema-derived Spirit. The work remains a working artifact for the parallel-implementation track. |
| `376-bottom-up-tour-01-nota-2026-05-27.md` | Layer 1 of the in-progress bottom-up tour series (record 868). Layers 3-7 still to come. Series may eventually absorb into `nota-next/INTENT.md` or similar permanent doc; until series completes, keep. |
| `377-context-maintenance-sweep-2026-05-27.md` | Recent designer-side maintenance sweep. Load-bearing for the sub-lane context; absorbed by /386 (cross-lane sweep) but /377 is the predecessor designer-only pass and remains useful as the immediate-predecessor reference. |
| `382-pair-style-sweep-2026-05-27.md` | Pair-style namespace sweep (record 894). Documents what landed where for the brace-is-key/value-map rule. Still load-bearing for naming discipline. |
| `383-next-version-schema-design-study-and-implement-2026-05-27.md` | Active design-and-implement thread for the next-version schema. Current implementation tied to it; not yet fully absorbed by /389. |
| `386-cross-lane-context-maintenance-2026-05-27/` (meta-dir) | RECENT cross-lane sweep meta-directory. Still load-bearing for sub-lane handoffs. Per the punch list: explicitly KEEP. |
| `387-nota-schema-design-representation-2026-05-27.md` | Primary topic report for nota-schema-design-representation (8-section side-by-side mermaid + tests). The canonical reference for the schema language SHAPE. Carries unique fixture detail not in /389. |
| `388-macro-system-exploration-and-brace-enum-sugar-2026-05-27.md` | Primary topic report for macro-system-exploration. Carries 8 match-criteria scenarios as working tests + brace-enum sugar implementation. |
| `389-schema-macros-canonical-direction.md` | Primary topic report for schema + macros (synthesis from records 894-942). Active canonical direction. |
| `390-wire-runtime-canonical-direction.md` | Primary topic report for wire + runtime (records 927-936). Active canonical direction. |
| `391-emission-discipline-direction.md` | Primary topic report for emission + discipline. Active canonical direction. |
| `392-vision-schema-driven-stack-canonical-2026-05-27.md` | Brand-new vision report (records 894-952). The landing-page synthesis; /389/390/391 are its chapters. Active. |
| `393-intent-workspace-discipline-continuous-manifestation-application-2026-05-27.md` | Continuous per-repo intent manifestation discipline + application pass (record 944). Recent. |

Total kept: 19 reports + 2 meta-directories = **21 entries**.

## Surprises

1. **381 (truth-finding audit of /380) is stale because both /380 and the audit target subsumed.** /381 was the audit that corrected /380. With /380 dropping, the audit is doubly absorbed — current canonical state is in /387/389. Dropped /381.

2. **375 (finish macro engine) is implementation-track work that completed on operator main.** The macro engine is real and on `schema-next` main (records 888-890 landed); /375's exercise of authoring `spirit.schema` with macro invocations is now ordinary use. Substance in /387 + /389. Dropped.

3. **The bottom-up tour Layer 2 (/380) is now in the canonical-direction synthesis (/389).** This is a clean topic agglomeration per record 941 — /389 became the primary topic report, /380 retires. Layer 1 (/376) stays until the tour completes Layers 3-7 OR the tour series migrates to a permanent doc (e.g. `nota-next/INTENT.md`).

4. **The 349 meta-directory was a large 5-subagent sweep.** Its predominant move (migrate substance into INTENT/skill edits) succeeded — the manifestation reports under §349/1-5 served their purpose. Successor sweeps /377 + /386 absorb the discipline; the directory retires cleanly.

5. **Peer-agent files in the working copy.** When picking this audit up, the working tree carried 6 reports under `reports/operator/` (216, 217, 218 + subdirs) and 2 modified `skills/` files — all not mine, all out-of-lane. Used `jj commit <my-paths>` to commit only `reports/designer/` deletions, leaving the peer files for their authors. No bundling of cross-lane work into one commit.

6. **The vision report (/392) is brand new — bigger picture than /361.** /392 is now THE landing-page synthesis; /361 is kept as a transitional prior-arc artifact but may absorb into /392 in a future pass.

## JJ commit short-ids — recap

| Commit | Subject |
|---|---|
| `173b4831` | `reports/designer: retire 21 stale reports per /391 + cross-lane sweep (105/106/107 RETRACTED; 379/380/384/385 superseded by 387/389/391; 349 meta-dir superseded by 377+386; 101/102/354/356/358/368/370/372/375/378/381 absorbed)` |

(Second commit lands this report.)

## Cross-references

- `reports/designer/386-cross-lane-context-maintenance-2026-05-27/1-designer.md` — designer-lane punch list this audit operates on.
- `reports/designer/389-schema-macros-canonical-direction.md` §"What this report supersedes" — names /380, /387, /388 as predecessors.
- `reports/designer/391-emission-discipline-direction.md` §"What this report supersedes" — names /384, /379 as predecessors.
- `reports/designer/387-nota-schema-design-representation-2026-05-27.md` §"What this report supersedes" — names /385 as predecessor.
- `skills/context-maintenance.md` §3a "Design-rationale guard against premature DELETE" — protects /341 and /363.
- `skills/reporting.md` §"Filename convention" + §"Topic agglomeration" — the rules this audit follows (record 941).
- Intent records 713-715 (effect-table/fan-out retraction), 920 (lane retirement), 921 (cross-lane reading), 941 (topic-prefix filenames).
