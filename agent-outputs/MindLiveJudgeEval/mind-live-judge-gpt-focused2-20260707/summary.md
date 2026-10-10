# Mind Live Judge Eval Evidence

Eval id: `mind-live-judge-gpt-focused2-20260707`
Mode: `isolated-categories`
Model/provider: `local-openai` / `gpt-5.5`
Run status: `incomplete` (success=false) reasons=["scored_rows_failed","setup_rows_failed","blocked_rows_present"]
Primary cases: 23
Scored rows: 9
Blocked rows: 14
Raw rows: 67
Setup rows: 0/44 passed
Submit calls, including rejection store probes: 9
Exact prefilter hits / semantic judge attempts: 0 / 9
Judge contract calls / parsed completed responses / format failures / diagnostic messages: 9 / 9 / 0 / 0
Verdict class pass rate: 77.78%
Identity-bearing pass rate: 75.00%
Identity existence pass rate: 100.00%
Minimal conflict identity pass rate: 100.00%
Accepted-positive rate: 100.00%
Safety rejection rate: 100.00%
Private/task rejection rate: 100.00%
Temporal/unstable rejection rate: 100.00%
Runner-ledger absence witness rate: 100.00%
Runner-ledger absence witness limitation: observes only accepted records fetched by this harness, not a direct storage scan.
Provider HTTP call count and invalid/retry telemetry: unavailable from Mind eval harness telemetry.

## Category Results

- `domain_all_acceptance`: 1/1 passed (100.00%)
- `wrong_domain_domain`: 6/8 passed (75.00%)

## Failures

- `wrong_domain_domain_06` `wrong_domain_domain` diagnosis=ModelVerdictFailure expected {"allowed_reasons":["WrongDomain"],"expected_domain":"Architecture","target_aliases":[],"verdict":"Rejected"} got {"identity":"eibu","kind":"Accepted","latency_ms":2071} notes=["expected rejection but got non-rejection reply","expected WrongDomain payload"]
- `wrong_domain_domain_08` `wrong_domain_domain` diagnosis=ModelVerdictFailure expected {"allowed_reasons":["WrongDomain"],"expected_domain":"Component","target_aliases":[],"verdict":"Rejected"} got {"identity":"uefd","kind":"Accepted","latency_ms":2259} notes=["expected rejection but got non-rejection reply","expected WrongDomain payload"]
