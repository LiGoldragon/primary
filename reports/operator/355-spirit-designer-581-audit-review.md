# Operator Review Of Designer 581

## Scope

This reviews `reports/designer/581-spirit-implementation-audit.md` against the
current `spirit` source, the deployed daemon after the UID-only correction
deployment, and the source design in `reports/designer/578-intent-redesign-synthesis.md`.

The design report was written while the operator lane was still changing the
weight/importance axis. Its non-axis findings mostly survive. Its deployment
state statements about the axis are now stale because Spirit commit `8fe88d66`,
CriomOS-home commit `8e909a40`, and CriomOS commit `df05927f` have been deployed.

## Verified Corrections

Designer 581 is stale on one important state claim:

- Source and production are no longer split on the axis shape. The activated
  daemon accepts the seven-field full query shape and `RecordAccepted` returns
  only the UID.
- Live check after deploy:
  - `Version` returned `(VersionReported (0.8.0 (1420 3566863645473464308)))`.
  - Full-count returned `(RecordsCounted (1418 (1420 3566863645473464308)))`.
  - A temporary live record returned `(RecordAccepted q2pp)`, then removal and
    lookup verified cleanup.

The category count table is still correct when read as an all-record count with
explicit `Any` certainty. Default shorthand hides zero-certainty records, which
is why a default `Meaning` count returns 880 while explicit `Any` certainty
returns 924.

## Findings That Stand

The category critique stands.

Live all-record category counts are still lopsided:

| Category | Count |
|---|---:|
| Meaning | 924 |
| Making | 387 |
| Governing | 300 |
| Relating | 145 |
| Sustaining | 119 |
| Caring | 16 |
| Being | 0 |
| Knowing | 0 |
| Dwelling | 0 |
| Moving | 0 |
| Valuing | 0 |
| Expressing | 0 |

`Meaning` + `Making` co-occur on 213 records. Six categories remain empty. This
is not a healthy retrieval index for a guardian.

The root cause claim also stands: `Categories::from_strings` uses
`Category::push_from_label`, which only emits six of twelve categories and
defaults unmatched labels to `Meaning`. The substring matcher can false-positive
inside larger words.

The guardian reach critique stands.

Current source routes only `Propose` through `guard_propose`. `Clarify` calls
`store.clarify` directly. `Supersede` calls `store.supersede` directly, and the
store archives/removes the named records before calling raw `propose` on the
replacement. `Record`, `Remove`, `ChangeCertainty`, `BumpImportance`, and
`ChangeRecord` are direct SEMA writes.

This conflicts with designer 578 on supersede. That report explicitly says
superseding `X` with `R` checks `R` against everything except the named target.
Current source does not do that.

The clarify finding is slightly more nuanced but still valid. Designer 578 says
clarify does not need a global consistency re-check because a true clarify is
meaning-preserving, but it also says the guardian judges clarify versus trample
or meaning-loss. Current source does neither: it changes the description after
archiving the predecessor.

The dead-reason finding stands. Outside generated schema declarations, the
guardian reasons `ClarifyTramples`, `ClarifyLosesMeaning`,
`SupersedeTargetMissing`, `Compound`, and `HarnessTimedOut` have no source
paths.

The guardian retrieval critique stands.

`guardian_records_for` searches by partial category match and hard-codes
`KeywordMatch::Any` and `TextMatch::Any`. That diverges from designer 578, which
defined the seed bundle as category matches plus content matches from the
proposed text. The keyword extractor and text matcher exist; they are not wired
into the guardian retrieval path.

The kind-fold critique stands.

Live kind counts still include old dialogue kinds:

| Kind | Count |
|---|---:|
| Decision | 497 |
| Principle | 369 |
| Correction | 183 |
| Clarification | 200 |
| Constraint | 124 |

So `Correction` and `Clarification` remain live kinds while `Clarify` and
`Supersede` are also write operations. The schema and data are not folded into
the cleaner model yet.

The no-distillation critique stands. The current store still has 1418 records;
the v6 migration changed shape and dropped legacy weight, but did not perform an
agglomeration/de-bloat pass.

## Findings To Treat As Design Decisions

The grounded category catalog proposed in designer 581 is plausible, but it is a
proposal, not an implementation order. Replacing the gerund catalog should wait
for the psyche to bless the actual category set. The audit is enough evidence
that the current catalog is weak; it is not enough authority to silently choose
the next catalog.

The weight decision should be considered settled for current source and deploy:
Spirit is now two-axis, with `Certainty` and `Importance`. Designer's concern is
valid historically: the removal was triggered by naming confusion. But after the
operator correction, tests and deployment now explicitly support the two-axis
shape. Reintroducing a derived reaffirmation axis should require a new explicit
psyche decision, not a rollback-by-inertia.

The status of raw `Record` is a product decision. It is currently a deliberate
raw write path and the report 354 production notes say callers must use
`Propose` for guarded admission. If the product wants every user-facing capture
guarded, the CLI/workflow should route those captures through `Propose`, or raw
`Record` should become restricted/meta-only.

## Recommended Order

1. Fix guardian retrieval before category replacement: include keyword and text
   leads from the proposed description so the guardian is not purely category
   dependent.
2. Guard `Clarify` and `Supersede`: clarify should be checked for trample/loss;
   supersede replacement should be checked against the remaining live store
   excluding named retired targets.
3. Add tests that prove `ClarifyTramples`, `ClarifyLosesMeaning`, and
   `SupersedeTargetMissing` have live paths.
4. Ask for the category catalog decision, then migrate categories with an
   auditable mapping instead of substring defaults.
5. Finish the kind-fold only after the category decision, because the
   agglomeration pass should rewrite categories and kinds together.

## Bottom Line

Designer 581 is substantially correct on the important implementation gaps. The
two adjustments are:

- ignore the stale "deployed still three-axis" part, because deployment now
  matches source;
- treat the proposed new category catalog as a decision request, not as an
  already-authorized implementation spec.

The urgent operator work is guardian reach and retrieval quality, not the axis.
