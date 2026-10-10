# Code Context

## Files Retrieved

1. `reports/designer/341-schema-crystallizes-architecture-2026-05-25.md` (lines 1-31) - preserved design-rationale report with retraction banner for InteractTrait / authored effect-table / fan-out drift.
2. `reports/designer/349-context-maintenance-sweep-2026-05-25/5-overview.md` (lines 1-79, 79-94, 95-142) - context-maintenance sweep summary, per-repo branch handoff, and carry-forward items.
3. `reports/designer/350-schema-feature-drift-retraction-2026-05-26.md` (lines 1-53, 78-130) - authoritative retraction of authored schema `Features` surface and operator follow-ons.
4. `reports/designer/351-intent-file-tour-2026-05-26.md` (lines 1-76, 78-151) - intent-scope cleanup, per-repo branch state, and flags for psyche review.
5. `reports/designer/352-intent-log-audit-2026-05-26.md` (lines 1-24, 299-374, 710-786) - audit discipline and highest-impact misalignment recommendations.
6. `reports/designer/353-schema-derived-nota-design-2026-05-26.md` (lines 1-75) - baseline all-the-way-back schema-derived NOTA design.
7. `reports/designer/355-critique-of-operator-195-schema-driven-nota-reader-2026-05-26.md` (lines 1-80, 199-230) - designer critique of operator's schema-driven NOTA reader prototype.
8. `reports/designer/357-nota-as-library-schema-as-root-struct-2026-05-26.md` (lines 1-75, 79-151, 155-238) - latest refined vision: NOTA as thin structural library, schema as implied root struct, schema-schema/macro layer.

## Key Code

No project/source code was edited or read for implementation. The important report-level interfaces and decisions are:

- Latest target shape is `/357`: NOTA is a thin block-structure library; interpretation moves to macros/schema. The sketched API is `impl Block { is_square_bracket; is_parenthesis; is_brace; holds_root_objects; root_object_at; qualifies_as_symbol; qualifies_as_pascal_case_symbol; qualifies_as_camel_case_symbol; qualifies_as_string; source_span }` from `reports/designer/357...` lines 19-38.
- `/357` narrows `/353`: schema files are not three peer top-level sections; `.schema` implies a root struct with positional fields. The first field is imports/exports namespace; the input/output struct is square-bracket positional substructure; user-defined types and output projections remain part of the canonical example mapping (`reports/designer/357...` lines 83-144).
- `/357` also introduces the default schema-schema and macro interface as the Rust core layer: every schema parse loads the schema-schema; macros implement a trait-like interface over `Block` shape matching and lowering to assembled nodes (`reports/designer/357...` lines 157-208).
- Field ordering is not fully decided. `/357` carries two options and defaults to imports/exports first only pending psyche decision (`reports/designer/357...` lines 210-218).
- `/350` and `/352` are the guardrails: authored `.schema` files must not contain `EffectTable`, `FanOutTargets`, `StorageDescriptor`, or a `Features` section. Schema defines data types only; effects/fan-out are runtime or hidden composer logic, not authored schema content (`reports/designer/350...` lines 8-31; `reports/designer/352...` lines 304-374).
- `/355` says operator's `/195` prototype proves a useful pipeline, but it is not the full design. It schema-derives readers for NOTA payloads, not NOTA itself; it lacks `nota.schema`, the kernel boundary, Input/Output sections, macro shape-interpretation, precompiled core, and schema daemon (`reports/designer/355...` lines 45-55). Recommended next slice: author `nota.schema`, define kernel boundary in `nota-codec`, handle Input/Output, preserve assembled order, remove Feature surface, and add one macro shape example (`reports/designer/355...` lines 201-220).

## Architecture

Latest designer work, in order:

1. `/349` was a large context-maintenance and intent-manifestation sweep. It retired many stale designer reports, added/updated NOTA and Spirit skills, and pushed per-repo docs branches (`designer-sweep-349-intent-2026-05-25`) for `schema`, `signal-frame`, `persona-spirit`, and `signal-persona-spirit` (`reports/designer/349.../5-overview.md` lines 79-90). Treat that handoff as partly superseded by `/350` and `/351`.
2. `/341` remains only as preserved design rationale. Its banner says the InteractTrait alternative was retracted, and `/350` later adds that effect-table/fan-out as authored schema features are also retracted (`reports/designer/341...` lines 3-15).
3. `/350` retracts the `Features` surface and queues cleanup of POC feature branches and POC `.schema` files that still carry authored Feature sections (`reports/designer/350...` lines 102-126).
4. `/351` relocates misplaced intent to the right scope. It reports a pushed `schema` repo branch `designer-intent-cleanup-2026-05-26` at commit `1b5c8037`, awaiting operator integration (`reports/designer/351...` lines 64-76). It also flags `signal-frame`'s stale unmerged `/349` INTENT content for psyche review because it was authored around the now-retracted Features framing (`reports/designer/351...` lines 132-151).
5. `/352` audits Spirit records 1-719. It does not supersede records itself. It recommends psyche supersession of the schema-defines-effects drift cluster and flags duplicate/work-order/hallucination groups (`reports/designer/352...` lines 710-786).
6. `/353` sets the all-the-way-back baseline: `nota.schema` describes NOTA; a small kernel loads it; the codec and downstream schema-emitted code derive from there (`reports/designer/353...` lines 5-70).
7. `/355` validates operator's prototype as a good first slice while naming the missing next slices.
8. `/357` is the current design refinement to use for new schema/NOTA work.

Primary jj state observed before writing this report:

- `main` bookmark: `wmlvvqvy 3999552f`, description `skills/jj.md: at-a-glance cheat sheet at top + note structural fix landed in source`.
- Current working copy before this report write: `@` change `lxuwnvpn`, no description, parent `tzlwqsyk c39d9a98` (`report operator/198: verify nota structural prototype`). That parent is an unbookmarked change one commit ahead of `main`, modifying `reports/operator/198-nota-structural-library-prototype-2026-05-26/4-overview.md` by 17 insertions / 2 deletions.
- Working-copy changes before this report write: added `reports/pi-operator/6-recent-intent-reports-branch-read-2026-05-26/0-frame-and-method.md`. This report adds another file in the same meta-report directory.
- `jj workspace list` showed only the `default` workspace during inspection.
- `jj file list -r main reports/designer` confirmed the current `reports/designer` set is present on `main`: `/341`, `/349/*`, `/350`, `/351`, `/352`, `/353`, `/355`, and `/357`.
- Recent `reports/designer` path history on main includes `designer/350`, `designer/351`, `designer/352`, `/355`, and later commits that touched `/353` and `/357` even when their commit descriptions are operator/report-audit descriptions. So the files are live on Primary main even if some commit descriptions do not read as designer-authored.
- Relevant lingering Primary bookmarks: `push-pptluysywqou` and `push-wuyqxurl` are `/349` subagent bookmarks already in `main` ancestry; do not treat them as active integration branches. Bookmarks not in `main` ancestry include older/stale designer/system-designer items such as `push-ukwtxmxn-lanefix` (canonical NOTA rewrite), `rescue-primary-dirty-2026-05-18` (persona-orchestrate state-of-knowledge), `push-context-maintenance-33`, and `push-omuusptmnxlw`; none are the latest `/350`-`/357` designer report path.

Pi-operator should know:

- Do not implement or integrate authored `.schema` `Features` sections. If a branch still exposes `EffectTable`, `FanOutTargets`, or `StorageDescriptor` as authored schema surface, it is stale/drift unless explicitly rewritten as hidden runtime/composer mechanism.
- Do not blindly fast-forward `/349` per-repo branches. `/349` line 90 called them docs-only fast-forwardable, but `/350` and `/351` later retracted or flagged the Features-based content. The `schema` repo has a newer cleanup branch; `signal-frame` INTENT remains a psyche-review question.
- If working in `nota`, `nota-codec`, or `schema`, start from `/357`: block parser primitives first; schema-schema/macro layer owns interpretation; schema root struct is implied by `.schema`; field ordering remains a decision point.
- If continuing operator `/195`, the meaningful next implementation slices are those in `/355`: `nota.schema`, kernel boundary, Input/Output support, ordered assembled schema, Feature-surface removal, and one macro shape example.
- Intent-log cleanup is not operator-delete work. `/352` only flags; psyche supersession must land as new Spirit records before agents treat old records as formally retired.
- Coordinate before moving `main`: current working copy is not directly on `main`; it sits atop an unbookmarked operator-report change plus pi-operator report additions.

## Start Here

Open `reports/designer/357-nota-as-library-schema-as-root-struct-2026-05-26.md` first. It is the latest refinement and names the implementation surface most likely to affect pi-operator work. Then check `reports/designer/350-schema-feature-drift-retraction-2026-05-26.md` before touching any schema branch so you do not revive the retracted Features design.
