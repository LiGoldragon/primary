# Mind Live Judge Eval Evidence

Eval id: `mind-domain-accepted-knowledge-20260706-direct_or_subtle_conflict-v2`
Mode: `isolated-categories`
Model/provider: `deepseek` / `deepseek-v4-flash`
Run status: `failed` (success=false) reasons=["scored_rows_failed"]
Primary cases: 2
Scored rows: 2
Blocked rows: 0
Raw rows: 4
Setup rows: 2/2 passed
Submit calls, including rejection store probes: 2
Exact prefilter hits / semantic judge attempts: 0 / 2
Judge contract calls / parsed completed responses / format failures / diagnostic messages: 2 / 2 / 0 / 0
Verdict class pass rate: 100.00%
Identity-bearing pass rate: 50.00%
Identity existence pass rate: 100.00%
Minimal conflict identity pass rate: 50.00%
Accepted-positive rate: 100.00%
Safety rejection rate: 100.00%
Private/task rejection rate: 100.00%
Temporal/unstable rejection rate: 100.00%
Runner-ledger absence witness rate: 100.00%
Runner-ledger absence witness limitation: observes only accepted records fetched by this harness, not a direct storage scan.
Provider HTTP call count and invalid/retry telemetry: unavailable from Mind eval harness telemetry.

## Category Results

- `direct_or_subtle_conflict`: 1/2 passed (50.00%)

## Failures

- `direct_or_subtle_conflict_02` `direct_or_subtle_conflict` diagnosis=WrongIdentity expected {"allowed_reasons":["ConflictsAcceptedKnowledge"],"expected_domain":null,"target_aliases":["K_DETERMINISTIC_STORAGE"],"verdict":"Rejected"} got {"kind":"Rejected","latency_ms":1172,"reason":"SemanticDuplicate","reason_identity":"p000"} notes=["expected reason in [\"ConflictsAcceptedKnowledge\"], got SemanticDuplicate","wrong identity: expected p001, got p000"]
