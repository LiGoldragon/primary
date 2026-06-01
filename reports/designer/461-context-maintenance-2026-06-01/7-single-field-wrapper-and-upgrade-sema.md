# 461.7 — Single-field wrapper audit + upgrade-as-SEMA + rkyv-wrapping + audit cluster

*Kind: Review · Topics: single-field-wrapper, upgrade-as-sema, rkyv-wrapping, audit-cluster · 2026-06-01*

## Topic arc

Three reports in this catch-all topic; all are stand-alone audits or
design work that doesn't fit the larger clusters covered in
1-engine-trait, 2-spirit-fold, 3-b53f4fc2, 4-bead-cleanup,
5-operator-271, or 6-proof-of-usage. Each is evaluated on its own
substance.

### Sub-topic A: single-field wrapper audit (448)

Designer 448 audited the single-field struct wrapper pattern across
nota-next + schema-next + spirit-next (prompted by
`struct CodecDerive { input: DeriveInput }`). 28 instances surveyed;
all pay their way through one of five reasons. The pattern is the
workspace's method-only-rule answer to "the verb needs a noun the
inner type cannot provide."

Operator's parallel work — reports 269 + 270 — confirmed the same
pattern with closer-to-implementation language. Both 269 + 270 have
been retired by operator 271's sweep (per `git status` D-marks at
session start). Designer 448 is the surviving canonical view.

### Sub-topic B: rkyv enum-wrapping audit (452)

Designer 452 audited the closed-sum-enum-per-shape pattern as the
honest representation for type-erasing structural-macro outputs in
rkyv-archived schema-emitted code. Pilot was `MacroPatternObject` in
schema-next. Eight cargo tests on `audit-rkyv-enum-wrapping-presumption`
feature branch with a flake check. Verdict: HOLDS WITH CAVEATS — the
closed-sum-enum tax is real but small; two open questions remain.

This audit is **independent design rationale** — it enumerates two
design alternatives (closed-sum vs open-bytes) and chose one, with
the rationale documented. Per `skills/context-maintenance.md` §3a
"Design-rationale guard against premature DELETE", reports with
competing design alternatives are load-bearing AS RATIONALE even
after the chosen option migrates.

### Sub-topic C: upgrade-as-SEMA design (447)

Designer 447 sketched the upgrade mechanism as SEMA operations on
Asschema: same library, two object types — today spirit-next applies
SEMA ops to Entry records; tomorrow schema-daemon applies SEMA ops
to Asschemas. This closes the NOTA-to-object correspondence per
Spirit 1312; the system becomes self-editing per Spirit 1314.
Implementation has not started; the design is fresh.

## Current canonical surface

| Surface | What it carries |
|---|---|
| 448 — single-field wrapper audit | Five-reason taxonomy + 28-instance survey. The taxonomy is the durable substance; the survey is the calibration. |
| 452 — rkyv enum-wrapping audit | Design-rationale enumeration: closed-sum-enum vs open-bytes; closed-sum-enum-per-shape chosen with linear-growth witness + variant-tag survival + sized-exact archive. Branch `audit-rkyv-enum-wrapping-presumption` with 8 tests. |
| 447 — upgrade-as-SEMA design | The schema-daemon as editor; SEMA-on-Asschema realization; NOTA-to-object correspondence closure; self-editing system. Implementation gated by designer 444 §5 horizons 1 + 4. |
| `skills/rust/methods.md` (no current §"Single-field wrappers" section) | Method-only discipline; the wrapper-audit substance could land here as a taxonomy section, but the audit itself reads more naturally in report form. |
| `skills/architectural-truth-tests.md` §"Pair-rule sweeps" (landed earlier today) | The pair-rule pattern that motivates running BOTH the wrapper-audit AND the ZST-namespace-audit in the same scope. Already-landed substance. |

## Stale / forward / migrate / keep bands by lane

### Designer lane

| Report | Action | Reason |
|---|---|---|
| 448 — Single-field wrapper audit | KEEP (with note) | The five-reason taxonomy is load-bearing for "why use a single-field struct, then?" — a question that recurs in audit work. The taxonomy could migrate to `skills/rust/methods.md` as a §"Single-field wrappers — the five legitimate reasons" section, but the wrapper-discussion lives more naturally as the audit-report shape (worked examples + per-repo breakdown). Per the operator-side note in 271 §"Reports still active" — "Designer-owned migration candidate" — the substance is recommended for migration to Rust discipline. Defer the migration to a future Rust-discipline maintenance pass that has the wider context to integrate it. Keep with a note. |
| 452 — rkyv enum-wrapping audit | KEEP (under design-rationale guard) | Per `skills/context-maintenance.md` §3a — reports with competing design alternatives are load-bearing AS RATIONALE. The 452 report enumerates closed-sum-enum vs open-bytes with the chosen design's tradeoff witnesses (linear-growth + variant-tag survival + sized-exact). If the chosen design later turns out wrong, this report is the only place the alternative's analysis lives. Add STATUS-BANNER discipline if and when the rkyv-wrapping pattern fully migrates into permanent docs. |
| 447 — Upgrade-as-SEMA design | KEEP | Sole design report for the upgrade mechanism (Spirit 1305-1314). Permanent surface is the future schema-daemon's ARCHITECTURE.md (per `skills/architecture-editor.md` — design lands in the relevant ARCHITECTURE.md when settled). Schema-daemon doesn't exist yet; 447 is the staging-ground. Retires when (a) operator implementation starts and (b) the substance lands in schema-daemon's ARCHITECTURE.md. |

### Operator lane

No operator reports in this cluster. The relevant operator-side
substance (269 + 270 wrapper audits) was retired by operator 271's
sweep.

## Landing evidence

For 448 (NOT migrating this sweep):

- The five-reason wrapper taxonomy COULD live in
  `skills/rust/methods.md` as a §"Single-field wrappers — five
  legitimate reasons" section, but the cost-benefit is:
  - Pro: durable rule discovery
  - Con: the rule-statement is "wrappers are valid when the inner
    type cannot host the methods you need" — that's already implicit
    in the existing method-only discipline + the existing pair-rule
    sweep section
  - The 28-instance survey doesn't fit a skill; it's calibration
    work that retires when the next survey supersedes
- Verdict: defer the migration. The audit stays as a working artifact
  until a Rust-discipline-maintenance sweep has the wider context.

For 452 (NOT migrating this sweep):

- The closed-sum-enum-per-shape pattern is in the chosen design but
  the alternative's analysis lives only in the report. Keep under
  the design-rationale guard.

For 447 (NOT migrating this sweep):

- Schema-daemon ARCHITECTURE.md doesn't exist yet; the upgrade-as-SEMA
  substance lives in 447 until that ARCHITECTURE.md is authored.

## Drop ownership / handoff

**Designer lane**: no drops in this topic this sweep. Future
maintenance:

- 448 retires when a Rust-discipline-maintenance pass migrates the
  five-reason wrapper taxonomy into `skills/rust/methods.md` AND
  the 28-instance survey is replaced by a fresher calibration (or
  judged unnecessary).
- 452 retires when the rkyv enum-wrapping pattern is sufficiently
  workspace-standard that a permanent skills/architecture surface
  carries the chosen-design substance AND the open questions
  (when same-shape sibling variants deserve closed-sum vs newtype
  with discriminator field; when schema-emitter prefers RelPtr over
  Box for recursive variants) are settled.
- 447 retires when (a) operator-implementation pickup happens and
  (b) the substance lands in schema-daemon's ARCHITECTURE.md (which
  doesn't exist yet).

**Operator lane**: no actions in this cluster.

## Pattern observation — pair-rule sweep validation

The 448 wrapper audit + the parallel operator wrapper audits (269 +
270) together motivated the pair-rule-sweep section that landed in
`skills/architectural-truth-tests.md` earlier today. The
substance-chain reads:

- 448 audited valid wrapper patterns; missed the adjacent ZST
  namespace anti-pattern.
- Operator 269+270 audited the same valid pattern; same scope miss.
- The shared scope miss — `^struct \w+ \{$` finds valid wrappers,
  `^struct \w+;$` finds ZST namespaces, both shapes look like "small
  struct with methods" from a distance — became the worked example
  in `skills/architectural-truth-tests.md` §"Pair-rule sweeps".

The pair-rule-sweep skill now applies workspace-wide; this cluster's
specific audit work is the calibration that proved the rule.

## Cross-references

- `reports/designer/448-single-field-wrapper-audit-2026-06-01.md` §"The CodecDerive specific case" — the canonical worked example.
- `reports/designer/452-rkyv-enum-wrapping-audit-2026-06-01.md` §"The hypothesis as captured" — Spirit 1324's framing.
- `reports/designer/447-upgrade-as-sema-design-2026-06-01.md` §"The one-paragraph realization story" — the SEMA-on-Asschema substrate.
- `skills/architectural-truth-tests.md` §"Pair-rule sweeps" — the pattern landed from the wrapper-audit scope miss.
- Spirit records 1305-1314 — upgrade-as-SEMA intent.
- Spirit record 1324 — rkyv enum-wrapping hypothesis.
