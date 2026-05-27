# 1 - Report topic survey

*Kind: Synthesis - Topics: reporting, schema, nota - 2026-05-27*

## Scope

This survey read the requested recent report surfaces:

- `reports/operator/190-audit-spirit-docs-and-multi-topic-2026-05-25.md`
- `reports/designer/349-context-maintenance-sweep-2026-05-25/`
- `reports/designer/383-next-version-schema-design-study-and-implement-2026-05-27.md`
- `reports/second-operator/190-schema-mainline-macro-index-port-2026-05-25.md`
- `reports/second-operator/191-intent-context-maintenance-2026-05-25/1-report-agglomeration.md`
- `reports/second-designer/183-fully-schema-and-nota-mvp-2026-05-25.md`
- `reports/second-designer/184-fully-schema-and-nota-comprehensive-understanding-2026-05-25.md`
- `reports/second-designer/188-schema-engine-running-walkthrough-2026-05-25.md`
- `reports/second-designer/189-macro-system-broader-understanding-2026-05-25.md`
- `reports/second-designer/194-bracket-swap-enum-vs-struct-2026-05-25.md`

`reports/designer-assistant/383*` was requested but is absent in the current
working tree. The adjacent current file is `reports/designer/383-...`; its body
still says "Designer-assistant lane", so the lane-retirement migration has left
some historical text inside moved reports.

Spirit already carries the new report-topic intent: record 939 says reports
should carry durable topics and filenames should prefix topics after the number;
record 941 gives the concrete `N-topic-title.md` /
`N-topic1-topic2-title.md` convention and says old reports should be
agglomerated, not bulk-renamed.

## Durable Topic Clusters

### reporting

This is now its own topic, not only a process concern. The cluster includes
topic-prefix filenames, one or more durable report topics, current reports as a
small working surface, and agglomeration into primary topic reports.

High-signal sources: Spirit records 939 and 941, `skills/reporting.md`, the
`reports/designer/349-...` context-maintenance sweep, and
`reports/second-operator/191-.../1-report-agglomeration.md`.

### nota

This cluster covers the NOTA language floor: bracket-only strings, escape-free
embedding, legacy quoted-string input as migration only, the `NotaValue` tree,
shape predicates, and colon-qualified symbols.

High-signal sources: `349/2-nota-discipline-manifestation.md`,
`second-designer/183`, `second-designer/184`, and `designer/383`.

Recommended primary report: `N-nota-canonical-current-state.md`.

### schema

This cluster is the schema language and canonical `.schema` file shape:
schema as architecture, six-position files, schema root / package root,
`schema/lib.schema`, namespace maps, key-value-only braces, imports, headers,
features, and known-struct root shape.

High-signal sources: `349/1-poc-schema-stack-explainer.md`,
`second-designer/184`, `second-designer/194`, `designer/383`, and the recent
operator reports after 210.

Recommended primary report: `N-schema-canonical-current-state.md`.

### macros

This cluster is the schema macro engine: shape-logic dispatch, the macro index,
two-phase structure-match then transformation, micro-macros, lazy loading,
core vs extension macros, fixed-point iteration, and user macro loading.

High-signal sources: `second-designer/188`, `second-designer/189`,
`second-operator/190`, and `second-operator/191`.

Recommended primary report: `N-macros-schema-index-and-loading.md` or, if the
workspace wants broad topic grep first, `N-schema-macros-index-and-loading.md`.

### emission

This cluster covers projection out of assembled schemas: `emit_schema!`,
schema-rust composer output, `OUT_DIR/schema/...` vs `src/schema/...`, Rust
module paths, generated source layout, no legacy `signal_channel!` dependency,
and schema-derived upgrade/Rust code.

High-signal sources: `349/1-poc-schema-stack-explainer.md`, `designer/383`,
and the operator reports around schema-rust-next and spirit-next.

Recommended primary report: `N-schema-emission-current-state.md`.

### spirit

This cluster covers Spirit as the main pilot and intent substrate:
multi-topic intent entries, Spirit deployment slots, CLI wire shape, current
schema pilot, daemon configuration, and migration across v0.2/v0.3/v-next.

High-signal sources: `operator/190`, `349/3-spirit-v020-integration-manifestation.md`,
`349/1-poc-schema-stack-explainer.md`, and the operator 205/206 line.

Recommended primary report: `N-spirit-schema-pilot-current-state.md`.

### wire

This cluster covers signal-frame / wire-contract concerns: short headers,
64-bit or extensible headers, operation/reply/event contracts, owner vs ordinary
headers, compatibility emission, and old-vs-new signal macros.

High-signal sources: `349/1-poc-schema-stack-explainer.md`, second-operator
handover reports summarized in `191`, and the recent operator header reports.

Recommended primary report: `N-wire-header-and-contract-current-state.md`.

### upgrade

This cluster covers version projection, schema diff, migration annotations,
auto-migration on daemon load, upgrade sockets, previous/current shape modules,
and handover state.

High-signal sources: `349/1-poc-schema-stack-explainer.md`,
`second-designer/184`, `second-operator/191`, and the operator schema-spirit
upgrade reports.

Recommended primary report: `N-upgrade-schema-and-runtime-current-state.md`.

## Filename Prefix Convention

Use this practical rule going forward:

1. Put the primary durable topic immediately after the report number.
2. Add at most two secondary topic facets after it.
3. Keep topic atoms short and stable: `nota`, `schema`, `macros`, `emission`,
   `spirit`, `wire`, `upgrade`, `runtime`, `reporting`, `orchestrate`.
4. Put the specific report title after the topic prefix.
5. Put report kind only in the report header, not the filename.

Examples:

- `217-schema-canonical-current-state.md`
- `218-schema-macros-index-and-loading.md`
- `219-nota-shape-logic-floor.md`
- `220-schema-emission-src-target-decision.md`
- `221-spirit-schema-pilot-current-state.md`
- `222-reporting-agglomeration-policy.md`

For grep and agglomeration, primary-topic-first is more useful than
most-specific-first. A future agent should be able to run
`rg --files reports | rg '/[0-9]+-schema-'` and find the primary schema
thread without knowing every subtype.

Avoid prefixes that encode report ancestry instead of subject:
`audit-operator-181`, `response-to-383`, `designer-followup`, and similar names
hide the topic. Put that relationship inside the report body.

## Agglomeration Without Bulk-Renaming

Do not rename old reports just to make filenames pretty. Treat old filenames as
historical locators and create current primary reports per topic.

Recommended flow:

1. Pick one topic cluster, for example `schema`.
2. Write one new primary topic report with the new filename convention.
3. In that report, list the old source reports read and carry forward only the
   current load-bearing substance.
4. Classify each source report as migrated, still-kept, or stale.
5. Delete old reports only when their substance fully migrated and only in the
   same committed change that lands the primary report.
6. Keep reports that preserve unique design rationale, test witnesses, or open
   questions not yet carried into the primary.

For meta-report directories, agglomerate at the directory level when possible.
If the whole directory's substance migrated, retire the directory as one unit.
If one subreport still carries unique evidence, keep the directory until that
evidence has a better home.

For old reports that are still referenced by newer reports, update only the
surviving references during a real agglomeration pass. Do not pre-emptively edit
old reports to add topic banners or rename them in place.

## Conflicts With Current Skills

`skills/reporting.md` already contains the new record-941 filename convention
and topic-agglomeration section. The main conflicts are internal leftovers:

- The "Where reports live" section still lists retired assistant directories
  such as `reports/designer-assistant/` and misses the current lane family
  (`second-designer`, `cloud-operator`, `nota-designer`, etc.).
- The "Kinds of reports" section says both kind and topic sit in the filename,
  but the newer filename convention says kind belongs in the report header or
  opening section, not the filename.
- The "Report header" section says `Kind` is the same value as in the filename.
  That is stale under record 941.
- The context-maintenance step still gives `<N>-review-<topic>.md`, which puts
  kind in the filename. Under the new convention that should be a topic-first
  title with `Kind: Review` in the header.
- The header shape is singular `Topic`, while record 941 and this task require
  one or more topics. The header should accept `Topics: schema, macros` or an
  equivalent multi-topic form.
- The filename convention says multiple topics are "most-specific-first", but
  agglomeration works better with primary-topic-first. The examples already
  mostly behave primary-first.

`skills/report-naming.md` is more stale than `skills/reporting.md`:

- It still documents only `reports/<role>/<N>-<topic>.md`.
- It treats `<topic>` as the whole subject slug, not a durable prefix followed
  by a title slug.
- It has no forward-only/no-bulk-rename rule for topic migration.
- It has no topic-agglomeration rule.
- It still mentions assistant lanes as valid writer subdirectories.

Practical implication: agents should follow `skills/reporting.md` plus Spirit
record 941 for new reports until `skills/report-naming.md` is refreshed.
