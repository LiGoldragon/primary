# Intent-log removal audit — biggest hits

*Deep audit of the deployed Spirit intent log (1103 live records, ids
1–1105, gaps at 1098/1099 already removed) for removal candidates, per
psyche 2026-05-28 ("we have the capacity to remove intent now… present
me your biggest hits — stale stuff outdated by newer design, or working
orders mistakenly logged"). Removal capacity captured as record 1103
(supersedes the append-only/flag-only constraint of 1091).*

*Method: a dispatched subagent dumped the full corpus and ran a regex
scan for working-order shapes, then stalled before semantics. This
report is the dispatcher's (system-designer) own work: I took the
corpus + the raw scan, **discarded the regex false positives**, applied
the after-the-task test record-by-record on the candidates, and
verified every supersession pair against the actual record text. The
regex scan over-flags badly — `\bsub-?agent` matched every durable
subagent-discipline principle (5, 57, 110, 231, 288, 539, 599, 920) and
every prototype-development principle (973, 976) — so the scan is a lead
list, not a verdict. Nothing below is a regex hit; everything is a
read-and-judged candidate.*

*This is AUDIT ONLY. No record is removed. The psyche picks from the
biggest-hits list; removal executes on approval.*

## The removal bar (conservative)

The intent layer is the highest-authority surface in the workspace and
removal is irreversible-in-spirit (the provenance is gone). So a record
earns **REMOVE** only if it clears one of two bars, each with its
evidence attached:

- **Working order** — fails the after-the-task test: *erase the task it
  named; is the sentence still meaningful and still guiding future
  work?* If it dies with the task, it was never durable intent.
- **Stale** — a **named** newer record supersedes or contradicts it,
  AND the durable substance (if any) has a permanent home (a later
  record, INTENT.md, AGENTS.md, a skill). "Feels old" is not evidence;
  a supersession id is.

Everything that doesn't clear a bar cleanly goes to **FLAG** for the
psyche, not to the remove pile. Under-removal is cheap; over-removal
deletes load-bearing intent.

## Biggest hits (ranked by confidence, present these first)

### Hit 1 — the log already adjudicated these; 1103 just lets them go (SAFEST)

Three records the psyche-derived log itself already ruled wrong or
superseded under the old flag-only regime. These are the safest possible
removals — the judgment is already in the log, in the psyche's own
records.

| Remove | Kind | Why it's safe | Adjudicated by |
|---|---|---|---|
| **1088** "Create a full schema-language design report… then test through production" | Decision | A working instruction for one session, captured as durable design intent | **1090** explicitly: "1088 was over-captured by the operator… a capture error… durable schema-language design intent should not be inferred" |
| **550** "redb file is COPYABLE WHILE the daemon holds it open… cutover works AS DESIGNED" | Clarification | An empirical claim that proved false | **568** explicitly: "Intent 550 was premature… did NOT prove the copy is transaction-coherent under concurrent writes" |
| **1091** "Intent records are append-only… cannot cancel delete or erase" | Correction | The rule that removal is impossible | **1103** explicitly: "superseding the append-only/flag-only constraint of record 1091" |

This is the record the psyche asked about directly ("is 1088 really
intent?") — yes, it's a working order, and the log already says so.

### Hit 2 — "Psyche asks this lane to do X" working orders (textbook)

The purest working-order shape: the record *names the prompt as a task
to this lane*. Each dies the moment its task completes. This is the
single most common mis-log pattern in the recent log.

| Remove | Text (opening) | Task — now done |
|---|---|---|
| **1055** | "Psyche asks this lane to review report 42, research lojix/horizon intent, audit the implementation… write an independent report" | report 43 / the /42 arc |
| **1058** | near-identical to 1055 ("review report 42… write an independent report") | duplicate of 1055 |
| **1056** | "Psyche asks this lane to fix the concrete issue shown in the attached screenshot" | the ConnectionRefused fix |
| **905** | "Audit production CriomOS changes not ported… create a report… guide the port" | system-operator/162 era |
| **913** | "Audit and critique the production-to-lean CriomOS reconciliation report" | report-audit, done |
| **1005** | "Audit the schema-at-heart prototype and report whether the tests genuinely prove…" | the prove-not-pretend audit (the *principle* is 1006, which stays) |
| **1065** | "Audit production Spirit for bad patterns similar to DescriptionOnly…" | report 43 / system-operator/168 |
| **1009** | "Research and prototype whether schema-next can reuse Cargo crate-resolution…" | report 39 (cross-crate import — proven) |
| **1024** | "Audit the current state of the horizon/lojix rewrite and assess feasibility…" | report 40 (feasibility = YES) |
| **1048** | "Build a working concept prototype that generates all Horizon datatypes from a PURE schema…" | report 41 + horizon-next (built) |
| **1061** | "Dispatch a subagent to FINISH the horizon-next concept… create and push the remote…" | done (commit 1b64d1b, nix check green) |

1009/1024/1048/1061 are my own over-captures — I flagged them when the
psyche asked about 1088, and they belong here. The *durable* intent
these tasks served (schema-at-heart, collections-as-the-gate, the port
feasibility verdict) lives in INTENT.md and reports 40–43, not in the
task directives.

### Hit 3 — the same task logged three times (the over-capture pattern, vivid)

**1073, 1074, 1075** — three consecutive records, all the *same task*:
create `skills/context-maintenance.md` from report 44, using a subagent.
The skill now exists. Three records, one working order, zero durable
intent (the skill IS the durable artifact). This is the clearest single
illustration of the pattern the psyche is worried about — agents
reflexively capturing the working order, and more than once.

### Hit 4 — stale by direct contradiction (most dangerous, remove to stop misleading)

| Remove | Text | Contradicted by |
|---|---|---|
| **109** "The workspace does not use feature branches by default. Merges go directly to main. Version tracking via semver tags… branches are exceptional" | Decision (Maximum) | **515** "Designers work on feature branches in ~/wt; operators rebase for main" — now an AGENTS.md hard override |
| **736** "Intent log audit policy: agents may FLAG… but never delete or supersede unilaterally" | Decision | **1103** (removal capacity) |

109 is the one to remove on *danger* grounds, not just tidiness: an
agent reading 109 today would avoid the worktree workflow the workspace
now mandates. A stale Maximum-magnitude Decision that contradicts
current practice is worse than clutter — it actively misleads.

### Hit 5 — the biggest *volume*, treated most carefully: era-1 schema framings

The `schema` topic alone is **262 records** — by far the largest
cluster. Much of it is era-1 framing (analysis/vision measured against
the legacy `intent/*.nota` substrate) superseded by the era-2
schema-at-heart re-grounding (records 1000, 1028/1054, 964, 1034) whose
substance has since migrated into INTENT.md — the same two-era split the
report-44 context-maintenance sweep found for *reports*.

**I am NOT putting this in the remove pile.** This is exactly where
over-removal destroys design rationale (the §3a guard in
context-maintenance.md). It needs its own dedicated, careful pass —
record-by-record, each with a named superseding record — not a bulk
sweep on topic-age. I flag it as the largest *opportunity* and the one
to treat most conservatively. Recommend a separate audit cycle scoped to
the `schema` topic after the clear hits above are removed.

## Counts

| Class | Count | Disposition |
|---|---|---|
| Total live records | 1103 | — |
| **Hit 1** — log-adjudicated | 3 (1088, 550, 1091) | REMOVE — safest |
| **Hit 2** — "psyche asks this lane" / audit-and-report working orders | 11 named | REMOVE |
| **Hit 3** — triple-logged skill task | 3 (1073/1074/1075) | REMOVE |
| **Hit 4** — stale by contradiction | 2 (109, 736) | REMOVE |
| **Other working orders** (Create-X-now / Build-X / Implement-X, task-scoped, done) | ~18 (214, 294, 297, 304, 308, 360, 375, 530, 531, 533, 595, 638, 664, 671, 754, 915, 985, 990) | REMOVE — see note |
| **FLAG** — working-order shell + durable rationale | ~8 (780, 846, 883, 885, 1016, 1068, 1090, 1056-partial) | psyche call |
| **FLAG** — era-1 schema volume | up to ~150 of 262 | dedicated later pass |
| Durable intent (keep) | the rest | KEEP |

**Roughly 35–40 clear-cut working-order + contradiction removals** in
hits 1–4 plus the "other working orders" row, with strong evidence on
each. The era-1 schema volume could multiply that, but only through the
careful pass.

## FLAG — the psyche's call, not mine

These carry a working-order *shell* around durable *substance*. The task
is dead but the rationale should survive — so removal would lose
something. Recommend keeping the durable half (possibly re-captured
clean) and removing only if the psyche agrees the substance is already
elsewhere.

- **780** "Create three repos: spirit, signal-spirit, core-signal-spirit…" — the "create now" is done, but the **persona→spirit prefix-retirement decision** + the side-by-side retirement plan is durable. Substance partly in the component-triad skill.
- **846** "Create a public spirit-next repository as the running schema-derived pilot" — done, but the *role* of spirit-next (the running schema-derived Spirit pilot) is durable context.
- **1016** "Build the inference node on prometheus, never on the local host…" — task-shaped, but wraps a durable **deploy constraint** (never realize large model closures into the local store; build on the remote builder). Keep the constraint.
- **1068** "Implement a better production Spirit observation surface…" — wraps a durable **principle** (truthful projection names; no single-field vector wrappers). Keep the principle.
- **883 / 885** — the schema-deep-rewrite framing + the concept-implementation methodology; mixed durable design + dispatch directive.
- **1090** — the flag-of-1088. Once 1088 is removed, 1090's job is done; keep as provenance or remove with its target.

## Note on the "other working orders" row

The ~18 records in that row (Create-X-now, Build-X, Implement-X,
Dispatch-subagents-to-X) are task directives that read as clear working
orders under the after-the-task test, and most name tasks that are
demonstrably done (the spirit/signal repos exist, the cloud component
exists, the schema/NOTA MVP shipped). I'm confident in the *class* but
recommend the psyche spot-check 2–3 before a batch removal, because a
few (e.g. 533 "bring orchestrate to Spirit maturity", 664 "conversion of
heresy sweep") carried *direction* that may or may not be fully absorbed
elsewhere. Conservative default: remove the unambiguous ones, FLAG the
direction-carrying ones.

## Recommended order of execution (on approval)

1. **Hits 1 + 3** first — the 6 safest (log-adjudicated + triple-logged).
   Zero risk; the log already says so.
2. **Hit 2** — the 11 "psyche asks this lane" / audit-and-report orders.
3. **Hit 4** — 109 and 736 (the dangerous-stale pair).
4. **Other working orders** — after a psyche spot-check.
5. **Era-1 schema volume** — a separate, dedicated, record-by-record pass.

Then update `skills/intent-log.md` §"When a working order slips in
anyway" — it currently says working orders "cannot be deleted, only
flagged," which 1103 has made stale (I introduced that line before the
removal capacity existed). It should read: flag, then remove on psyche
authority.

## See also

- `skills/intent-log.md` §"The pre-capture gate — the after-the-task
  test" — the working-order discipline this audit enforces retroactively.
- `reports/system-designer/44-cross-lane-context-maintenance-2026-05-28/`
  — the parallel two-era finding for *reports*; the `schema` era-1
  volume here is the intent-record analogue.
- record 1103 (removal capacity) / 1090 (1088 capture-error) / 568 (550
  correction) / 515 (worktree workflow that obsoletes 109) — the
  load-bearing supersession evidence.

## Appendix — full text of removed records (tombstone)

*Removal loses the record from the active store and its provenance.
This appendix preserves the full text + daemon-stamped timestamp of the
19 records removed on psyche approval 2026-05-29, so the audit report
itself is the provenance of what was removed. Captured via
`(Observe (RecordIdentifiers ((Exact N) WithProvenance)))` immediately
before removal.*

- **109** (Decision, Maximum, 2026-05-22) [workspace] — "The workspace does not use feature branches by default. Merges go directly to main. Version tracking happens via semver tags… Branches are exceptional… Default for any operator slice: edit, test, push to main…" — *superseded by 515 (worktree workflow, now an AGENTS.md hard override).*
- **550** (Clarification, Maximum, 2026-05-25) [redb-copyable-while-open] — "The redb file is COPYABLE WHILE the writing daemon holds it open… cutover works AS DESIGNED without any drain-the-writer prerequisite…" — *corrected as premature/unsafe by 568.*
- **736** (Decision, Maximum, 2026-05-26) [workspace] — "Intent log audit policy: agents may FLAG… but never delete or supersede unilaterally. Only the psyche supersedes intent…" — *superseded by 1103 (removal capacity).*
- **905** (Decision, Maximum, 2026-05-27) [criomos lojix horizon] — "Audit production CriomOS changes that have not been ported to the next Lojix and Horizon rewrite stack, create a report, and use the findings to guide the port." — *working order; done.*
- **913** (Decision, High, 2026-05-27) [system-operator reports criomos nota-schema-next] — "Audit and critique the production-to-lean CriomOS reconciliation report after refreshing the latest NOTA/schema-next design context." — *working order; done.*
- **1005** (Constraint, Maximum, 2026-05-27) [schema-stack e2e-tests audit truth-tests…] — "Audit the schema-at-heart prototype and report whether the tests genuinely prove the concept by building real packages through Nix…" — *working order; the durable principle is 1006 (kept).*
- **1009** (Decision, High, 2026-05-28) [schema-next cargo cross-crate-import nix…] — "Research and prototype whether schema-next can reuse Cargo crate-resolution to find schema libraries by the single-colon module naming…" — *working order; report 39 (proven).*
- **1024** (Decision, High, 2026-05-28) [horizon lojix schema-next nota-next port feasibility…] — "Audit the current state of the new-logic horizon/lojix rewrite and assess the feasibility of porting schema-next plus nota-next to be the MAIN driver…" — *working order; report 40 (feasibility = YES).*
- **1048** (Decision, High, 2026-05-28) [horizon schema-pipeline concept…] — "Build a working concept prototype that generates all needed Horizon datatypes from a PURE schema, demonstrated step-by-step end to end…" — *working order; report 41 + horizon-next (built).*
- **1055** (Constraint, High, 2026-05-28) [horizon lojix criomos audit implementation] — "Psyche asks this lane to review report 42, research the broader intent of the lojix/horizon/CriomOS reworking, audit the implementation, become expert in the question, and write an independent report." — *working order; report 43.*
- **1056** (Decision, High, 2026-05-28) [horizon lojix criomos implementation] — "Psyche asks this lane to fix the concrete issue shown in the attached screenshot as part of the audit/fix pass." — *working order; the ConnectionRefused fix.*
- **1058** (Decision, High, 2026-05-28) [lojix horizon criomos audit reports] — "Psyche asks this lane to review report 42, research the full intent behind the lojix/horizon/CriomOS reworking, audit the implementation, and write an independent report." — *near-duplicate of 1055; working order.*
- **1061** (Decision, High, 2026-05-28) [horizon-next finish subagent schema-deep] — "Dispatch a subagent to FINISH the horizon-next schema-driven Horizon concept completely - create and push the remote, land the nix flake check hermetic witness, and close the carried-forward divergences from report 42…" — *working order; done (commit 1b64d1b).*
- **1065** (Decision, High, 2026-05-28) [spirit signal surface bad-pattern audit] — "Audit production Spirit for bad patterns similar to the misleading DescriptionOnly mode and the nested RecordsObserved vector wrapper…" — *working order; report 43 / system-operator/168.*
- **1073** (Decision, High, 2026-05-28) [context-maintenance skills subagent] — "Psyche asks this lane to create or update skills/context-maintenance.md from report 44, and to use a subagent for the work." — *working order; the skill exists.*
- **1074** (Decision, Maximum, 2026-05-28) [context-maintenance skills] — "Create a workspace skills/context-maintenance.md skill from the cross-lane context maintenance report, using a subagent…" — *duplicate of 1073.*
- **1075** (Decision, High, 2026-05-28) [context maintenance with subagent] — "Run the context-maintenance discipline using a subagent, grounded in report 44, while preserving the current in-progress production Spirit work state…" — *duplicate of 1073/1074.*
- **1088** (Decision, High, 2026-05-28) [schema schema-language language-design production-test report] — "Create a full schema-language design report from the current clarified grammar… Then test the design through the production Spirit path…" — *the record the psyche flagged; already adjudicated a capture-error by 1090.*
- **1091** (Correction, High, 2026-05-28) [intent-maintenance intent-capture append-only provenance] — "Intent records are append-only provenance. A later Spirit record cannot cancel delete or erase an earlier Spirit record…" — *superseded by 1103 (removal capacity).*
