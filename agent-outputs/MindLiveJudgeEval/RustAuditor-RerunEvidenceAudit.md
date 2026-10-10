# Mind Live Eval Rerun Evidence Audit

Task and scope: independent audit of the Mind full live eval rerun evidence in `/home/li/primary/agent-outputs/MindLiveJudgeEval/`, especially the report `GeneralCodeImplementer-LiveEvalRerunEvidence.md`, the successful stateful and isolated-category output directories, and the blocked isolated attempt archive. I did not run live provider calls.

## Findings

No evidence or harness-reporting defects found. The worker's summarized counts match the archived JSON/JSONL artifacts, with one non-defect caveat: the raw isolated `results.jsonl` has 447 rows because it includes 234 setup rows, while the reported 213 scored rows are the category-scored non-setup primary/store-probe rows.

No secret-hygiene defect found. The archive contains allowed secret-source references such as `Gopass:platform.deepseek.com/api-key` and synthetic trap text such as `sk-test-not-a-real-secret`; I found no real key bytes, bearer tokens, passwords, provider HTTP dumps, decrypted secret-store output, or prompt/packet/training text diagnostics.

No exact-duplicate prefilter defect found. Exact duplicate rows that had accepted target aliases returned `SemanticDuplicate` in 2-5 ms, consistent with deterministic prefilter behavior. Remaining exact-duplicate failures correlate with missing target aliases caused by earlier seed/setup rejection, not statement normalization or a prefilter miss.

The first isolated attempt is correctly reported as a pre-call Unix socket path-length blocker. Both `rust-full-20260702T233537Z-isolated-categories/` and `rust-full-20260702T233537Z-isolated-categories-blocked/` contain the same blocker metadata; the explicit blocked archive also contains `agent-daemon.err` with `path must be shorter than SUN_LEN`, and `blocker.json` records `submit_calls_before_blocker: 0` and `judge_attempts_before_blocker: 0`.

## Verified Counts

Stateful evidence checked from `rust-full-20260702T233537Z-stateful/`:

- `results.jsonl`: 214 rows, 166 passed.
- Non-probe primary rows: 120 total, 72 passed.
- Store probes: 94 total, 94 passed.
- Setup rows: 0.
- `summary.json` category totals: 214 scored rows, 166 passed, 48 failures.
- `submit_calls`: 214.
- `judge_attempts`: 192; `diagnostics/stateful/judge-diagnostics.jsonl` has 192 lines.
- `MeaningUnclear`, `Unexpected`, and `Unavailable`: 0.
- Accepted `Get` verification failures: 0.

Isolated-category evidence checked from `rust-full-20260702T234043Z-isolated-categories/`:

- `results.jsonl`: 447 rows, 347 passed, including setup rows.
- Scored non-setup rows: 213 total, 171 passed.
- Non-probe primary rows: 120 total, 80 passed.
- Store probes: 93 total, 91 passed.
- Setup rows: 234 total, 176 passed.
- `summary.json` category totals: 213 scored rows, 171 passed, 42 scored failures.
- `submit_calls`: 447.
- `judge_attempts`: 423; isolated diagnostic files sum to 423 lines.
- `MeaningUnclear`: 2 rows, both for `exact_duplicate_14` and its store probe.
- `Unexpected` and `Unavailable`: 0.
- Accepted `Get` verification failures: 0.

Category counts in the worker report match the category totals in both summary files.

## Failure Patterns

The dominant weakness is still model/prompt judgment quality, not harness parsing or storage plumbing.

- Paraphrase duplicates are the largest miss: stateful 0/14 and isolated 2/14. The model often accepted paraphrases as new knowledge, or rejected them as `WrongSubject`, `NeedsMoreSpecificShape`, or `NotKnowledge` instead of `SemanticDuplicate`.
- Direct/subtle conflicts are only 8/14 in both modes. Failures mostly reject for the wrong reason or wrong identity; isolated also has one `ConflictsAcceptedKnowledge` with the wrong identity.
- Source-required versus false/unsupported remains poorly separated: stateful `false_or_unsupported` is 0/6 and `source_needed` is 2/6; isolated is 1/6 and 3/6. Failures skew toward `WrongSubject`, `NeedsMoreSpecificShape`, `ConflictsAcceptedKnowledge`, or `SemanticDuplicate`.
- Valid and positive-control cases are over-rejected: valid seeds are 14/18 in both modes, and ambiguous-positive controls are 1/2 in both modes. Isolated setup magnifies this: 58 of 234 setup rows failed, so category outcomes can inherit missing aliases from model rejection during setup.
- Wrong-subject-domain cases are 4/8 in both modes, with both wrong payload subjects and outright accepts.
- The two isolated store-probe failures are live-judgment instability more than a storage leak signal: `false_or_unsupported_01__rejection_store_probe` and `seed_12__rejection_store_probe` were accepted on resubmission with new identities. That proves the resubmission verdict changed; it does not by itself prove a rejected item was stored.

Exact duplicate details:

- Stateful failures: `exact_duplicate_07`, `exact_duplicate_11`, and `exact_duplicate_14` all note `target alias not accepted yet` and have live-latency rejections around 1.2-1.6s. Their target seed aliases were missing because the corresponding seeds failed earlier in the same stateful run.
- Isolated failures: `exact_duplicate_07` and `exact_duplicate_14` both note `target alias not accepted yet`; exact duplicate setup failed for `seed_07` and `seed_14`. `exact_duplicate_11` passed in isolated mode because its category setup accepted `seed_11`.
- The passing exact duplicates all look like deterministic prefilter hits, not model calls, based on 2-5 ms latency and immediate `SemanticDuplicate` with the expected identity.

## Interpretation

Prompt/model weakness is responsible for most judgment failures: semantic duplicate recognition, conflict identity selection, reason taxonomy, valid acceptance, and subject classification. This matches the Spirit intent lens from `w312`: deterministic duplicate lookup should stay in mechanism, while the remaining semantic categories are agent judgment and currently below gate quality.

Harness/design issues are narrower:

- Isolated-category mode uses live model setup, so category cases that depend on prior accepted aliases can fail for setup reasons before the category's actual behavior is tested.
- The rejected-not-stored store probe currently uses another live `Submit`, so it mixes storage safety with model nondeterminism.
- The blocked isolated attempt shows the harness needs a preflight path-length guard or shorter per-category socket roots before daemon startup.

## Recommendations

Do not promote DeepSeek Flash judge defaults from this run.

For the next implementation/eval pass:

- Add explicit archive metrics for raw result rows, setup rows/pass counts, scored rows, prefilter hit count, and summed diagnostic lines.
- Make exact-duplicate prefilter tests independent of live seed acceptance, either by deterministic accepted-store seeding or by marking alias-missing cases as setup failures instead of duplicate failures.
- Replace or supplement live resubmission store probes with a direct storage absence witness for rejected candidates.
- Add a socket-path preflight check and keep isolated work roots short.
- Focus prompt/model work on paraphrase duplicate examples, conflict identity selection, source-required versus unsupported taxonomy, wrong-subject payload selection, and acceptance of valid architecture facts.

## Evidence Consulted

Files and directories inspected:

- `agent-outputs/MindLiveJudgeEval/GeneralCodeImplementer-LiveEvalRerunEvidence.md`
- `agent-outputs/MindLiveJudgeEval/rust-full-20260702T233537Z-stateful/`
- `agent-outputs/MindLiveJudgeEval/rust-full-20260702T234043Z-isolated-categories/`
- `agent-outputs/MindLiveJudgeEval/rust-full-20260702T233537Z-isolated-categories/`
- `agent-outputs/MindLiveJudgeEval/rust-full-20260702T233537Z-isolated-categories-blocked/`

Commands run were local/read-only: `spirit (PublicTextSearch ...)`, `ls`, `find`, `sed`, `jq`, `wc -l`, `rg`, `head`, `jj log -r 871977c3`, and targeted shell loops over archived JSONL files. No live provider command was run.

Version evidence: `jj log -r 871977c3` resolves to `871977c3b9b14ac428f13fd0c6a8d3cbea7075f7 primary: archive Mind live judge eval rerun evidence`.
