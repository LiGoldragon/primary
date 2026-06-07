# Skill — report naming

Naming, iteration, and supersession discipline for reports. Companion to `skills/reporting.md` (chat-vs-report, inline summaries, visuals, caps).

## Filename

`reports/<role>/<N>-<Variant>-<primary-topic>[-<secondary-topic>]-<title-slug>.md`

- `<role>` is the writer's exact lane subdirectory (`designer`, `operator`, `system-operator`, `poet`, assistant lanes, second/third lanes, specialised lanes).
- `<N>` is **per-role**, the next integer after the highest-numbered report in this role's subdir — `reports/operator/97-…` and `reports/designer/97-…` coexist because the role subdir disambiguates. No leading zeros. No date prefix: commit history records when a report landed.
- `<Variant>` is the capitalized report kind — `Psyche`, `Design`, `Audit`, `Research`, `Synthesis`, `Closeout`, `Handover`, `Update`, `Refresh`. Every report has one. It appears in BOTH the filename (for grep discoverability) and the YAML `variant:` field (for typed metadata). `Update` is the recurring workspace update report (`skills/workspace-update-report.md`); `Refresh` is the context-maintenance output that agglomerates prior reports on a topic into one better form, deleting the merged sources as it lands (`skills/context-maintenance.md`).
- `<primary-topic>` is the durable topic cluster, placed first so `rg --files reports | rg '/[0-9]+-schema-'` finds a topic's current report surface without knowing exact titles. Keep topic atoms short and stable: `nota`, `schema`, `macros`, `emission`, `spirit`, `wire`, `upgrade`, `runtime`, `reporting`, `orchestrate`.
- `<title-slug>` is the specific subject in kebab-case.

Example: `reports/operator/218-Design-schema-macros-index-and-loading.md`

Find the next number, then add 1. Numbers are gap-tolerant and never reused after deletion.

```sh
ls ~/primary/reports/<role>/ | grep -E '^[0-9]+-' \
  | sort -t- -k1,1n | tail -1
```

## Iteration with `-v2` / `-v3`

While a report is actively refined with feedback, the edited version takes a `-v2` / `-v3` suffix (v1 is implicit, no suffix): `225-…`, `225-v2-…`, `225-v3-…`. The current version is canonical; delete the predecessor in the same commit that lands the successor. Don't accumulate versions side by side.

## Supersession with a new number

When the topic shifts enough that the name after the number should change (concept → implementation, scope redirect, absorbing an audit's findings), write a new numbered report carrying forward anything still relevant, and delete the predecessor in the same commit. The predecessor's number is retired; the next report takes next-highest-plus-one, not the freed number.

## Topic agglomeration

When a topic accumulates many reports, do not bulk-rename old files to tidy the directory. Write one current primary-topic report, carry forward the load-bearing substance, list the sources read inside the new report, then delete only the predecessors whose substance fully migrated — in the same committed change that lands the replacement. Historical filenames remain valid locators in git history; new reports use the topic-prefix convention forward.

## Commit before delete

**Never delete an uncommitted report** — that is total loss. Deleting a *committed* report only removes it from the work tree; git history retains the substance and it stays recoverable. So for any rename, supersession, or agglomeration: the new report must be committed in the same commit as the predecessor's deletion. Both the addition and removal land in one whole-working-copy `jj commit` (no path arguments — see `skills/jj.md`), keeping the replacement and its source visible together in one change.

## See also

- `skills/reporting.md` — the larger reporting discipline.
- `skills/jj.md` — the version-control flow these commits use.
