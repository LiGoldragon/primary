# Mind Live Judge Eval Evidence

Eval id: `mind-live-judge-gpt-focused3-20260707`
Mode: `isolated-categories`
Model/provider: `local-openai` / `gpt-5.5`
Run status: `failed` (success=false) reasons=["scored_rows_failed"]
Primary cases: 32
Scored rows: 32
Blocked rows: 0
Raw rows: 118
Setup rows: 86/86 passed
Submit calls, including rejection store probes: 32
Exact prefilter hits / semantic judge attempts: 1 / 31
Judge contract calls / parsed completed responses / format failures / diagnostic messages: 31 / 31 / 0 / 0
Verdict class pass rate: 87.50%
Identity-bearing pass rate: 88.89%
Identity existence pass rate: 100.00%
Minimal conflict identity pass rate: 100.00%
Accepted-positive rate: 81.82%
Safety rejection rate: 100.00%
Private/task rejection rate: 100.00%
Temporal/unstable rejection rate: 100.00%
Runner-ledger absence witness rate: 100.00%
Runner-ledger absence witness limitation: observes only accepted records fetched by this harness, not a direct storage scan.
Provider HTTP call count and invalid/retry telemetry: unavailable from Mind eval harness telemetry.

## Category Results

- `adversarial_near_duplicate`: 4/6 passed (66.67%)
- `domain_all_acceptance`: 1/1 passed (100.00%)
- `domain_neighbor_contrast`: 9/9 passed (100.00%)
- `large_neighbor_database`: 4/4 passed (100.00%)
- `recursive_linked_dependency`: 3/4 passed (75.00%)
- `wrong_domain_domain`: 6/8 passed (75.00%)

## Failures

- `adversarial_near_duplicate_domain_lens_01` `adversarial_near_duplicate` diagnosis=ModelVerdictFailure expected {"allowed_reasons":[],"expected_domain":null,"target_aliases":[],"verdict":"Accepted"} got {"kind":"Rejected","latency_ms":6410,"reason":"SemanticDuplicate","reason_identity":"p001"} notes=[]
- `adversarial_near_duplicate_implementation_phrasing_01` `adversarial_near_duplicate` diagnosis=ModelVerdictFailure expected {"allowed_reasons":["NeedsMoreSpecificShape"],"expected_domain":null,"target_aliases":[],"verdict":"Rejected"} got {"domain":"Documentation","kind":"Rejected","latency_ms":3673,"reason":"WrongDomain"} notes=["expected reason in [\"NeedsMoreSpecificShape\"], got WrongDomain"]
- `recursive_linked_dependency_accept_01` `recursive_linked_dependency` diagnosis=ModelVerdictFailure expected {"allowed_reasons":[],"expected_domain":null,"target_aliases":[],"verdict":"Accepted"} got {"kind":"Rejected","latency_ms":4957,"reason":"SemanticDuplicate","reason_identity":"p002"} notes=[]
- `wrong_domain_domain_06` `wrong_domain_domain` diagnosis=ModelVerdictFailure expected {"allowed_reasons":["WrongDomain"],"expected_domain":"Architecture","target_aliases":[],"verdict":"Rejected"} got {"identity":"m6h8","kind":"Accepted","latency_ms":3177} notes=["expected rejection but got non-rejection reply","expected WrongDomain payload"]
- `wrong_domain_domain_08` `wrong_domain_domain` diagnosis=ModelVerdictFailure expected {"allowed_reasons":["WrongDomain"],"expected_domain":"Component","target_aliases":[],"verdict":"Rejected"} got {"identity":"nre0","kind":"Accepted","latency_ms":2274} notes=["expected rejection but got non-rejection reply","expected WrongDomain payload"]
