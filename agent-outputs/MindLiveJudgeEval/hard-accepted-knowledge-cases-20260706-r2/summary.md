# Mind Live Judge Eval Evidence

Eval id: `hard-accepted-knowledge-cases-20260706-r2`
Mode: `stateful`
Model/provider: `deepseek` / `deepseek-v4-flash`
Run status: `failed` (success=false) reasons=["scored_rows_failed"]
Primary cases: 14
Scored rows: 14
Blocked rows: 0
Raw rows: 57
Setup rows: 43/43 passed
Submit calls, including rejection store probes: 14
Exact prefilter hits / semantic judge attempts: 1 / 13
Judge contract calls / parsed completed responses / format failures / diagnostic messages: 13 / 13 / 0 / 0
Verdict class pass rate: 71.43%
Identity-bearing pass rate: 33.33%
Identity existence pass rate: 33.33%
Minimal conflict identity pass rate: 0.00%
Accepted-positive rate: 0.00%
Safety rejection rate: 100.00%
Private/task rejection rate: 100.00%
Temporal/unstable rejection rate: 100.00%
Runner-ledger absence witness rate: 100.00%
Runner-ledger absence witness limitation: observes only accepted records fetched by this harness, not a direct storage scan.
Provider HTTP call count and invalid/retry telemetry: unavailable from Mind eval harness telemetry.

## Category Results

- `adversarial_near_duplicate`: 0/6 passed (0.00%)
- `large_neighbor_database`: 0/4 passed (0.00%)
- `recursive_linked_dependency`: 1/4 passed (25.00%)

## Failures

- `large_neighbor_database_duplicate_01` `large_neighbor_database` diagnosis=WrongIdentity expected {"allowed_reasons":["SemanticDuplicate"],"expected_subject":null,"reasons":["SemanticDuplicate"],"target_aliases":["K_NEIGHBORS_DATA"],"verdict":"Rejected"} got {"kind":"Rejected","latency_ms":1584,"reason":"WrongSubject","subject":"Architecture"} notes=["expected reason in [\"SemanticDuplicate\"], got WrongSubject","expected identity-bearing rejection payload"]
- `large_neighbor_database_conflict_01` `large_neighbor_database` diagnosis=WrongIdentity expected {"allowed_reasons":["ConflictsAcceptedKnowledge","FalseOrUnsupported"],"expected_subject":null,"reasons":["ConflictsAcceptedKnowledge","FalseOrUnsupported"],"target_aliases":["K_FOUND_PROJECTION"],"verdict":"Rejected"} got {"kind":"Rejected","latency_ms":1599,"reason":"WrongSubject","subject":"Component"} notes=["expected reason in [\"ConflictsAcceptedKnowledge\", \"FalseOrUnsupported\"], got WrongSubject","expected identity-bearing rejection payload"]
- `large_neighbor_database_accept_01` `large_neighbor_database` diagnosis=ModelVerdictFailure expected {"allowed_reasons":[],"expected_subject":null,"reasons":[],"target_aliases":[],"verdict":"Accepted"} got {"kind":"Rejected","latency_ms":1874,"reason":"WrongSubject","subject":"Architecture"} notes=[]
- `large_neighbor_database_source_required_01` `large_neighbor_database` diagnosis=ModelVerdictFailure expected {"allowed_reasons":["SourceRequired","FalseOrUnsupported"],"expected_subject":null,"reasons":["SourceRequired","FalseOrUnsupported"],"target_aliases":[],"verdict":"Rejected"} got {"kind":"Rejected","latency_ms":1688,"reason":"NeedsMoreSpecificShape"} notes=["expected reason in [\"SourceRequired\", \"FalseOrUnsupported\"], got NeedsMoreSpecificShape"]
- `recursive_linked_dependency_duplicate_01` `recursive_linked_dependency` diagnosis=WrongIdentity expected {"allowed_reasons":["SemanticDuplicate"],"expected_subject":null,"reasons":["SemanticDuplicate"],"target_aliases":["K_DEPENDENCY_BASE"],"verdict":"Rejected"} got {"kind":"Rejected","latency_ms":2026,"reason":"WrongSubject","subject":"Architecture"} notes=["expected reason in [\"SemanticDuplicate\"], got WrongSubject","expected identity-bearing rejection payload"]
- `recursive_linked_dependency_accept_01` `recursive_linked_dependency` diagnosis=ModelVerdictFailure expected {"allowed_reasons":[],"expected_subject":null,"reasons":[],"target_aliases":[],"verdict":"Accepted"} got {"kind":"Rejected","latency_ms":1681,"reason":"SemanticDuplicate","reason_identity":"p036"} notes=[]
- `recursive_linked_dependency_conflict_01` `recursive_linked_dependency` diagnosis=WrongIdentity expected {"allowed_reasons":["ConflictsAcceptedKnowledge"],"expected_subject":null,"reasons":["ConflictsAcceptedKnowledge"],"target_aliases":["K_DEPENDENCY_DERIVED"],"verdict":"Rejected"} got {"kind":"Rejected","latency_ms":1471,"reason":"WrongSubject","subject":"Architecture"} notes=["expected reason in [\"ConflictsAcceptedKnowledge\"], got WrongSubject","expected identity-bearing rejection payload"]
- `adversarial_near_duplicate_subject_lens_01` `adversarial_near_duplicate` diagnosis=ModelVerdictFailure expected {"allowed_reasons":[],"expected_subject":null,"reasons":[],"target_aliases":[],"verdict":"Accepted"} got {"kind":"Rejected","latency_ms":1550,"reason":"WrongSubject","subject":"Architecture"} notes=[]
- `adversarial_near_duplicate_temporal_01` `adversarial_near_duplicate` diagnosis=ModelVerdictFailure expected {"allowed_reasons":["SourceRequired","NeedsMoreSpecificShape"],"expected_subject":null,"reasons":["SourceRequired","NeedsMoreSpecificShape"],"target_aliases":[],"verdict":"Rejected"} got {"kind":"Rejected","latency_ms":1873,"reason":"SemanticDuplicate","reason_identity":"p036"} notes=["expected reason in [\"SourceRequired\", \"NeedsMoreSpecificShape\"], got SemanticDuplicate"]
- `adversarial_near_duplicate_negation_01` `adversarial_near_duplicate` diagnosis=ModelVerdictFailure expected {"allowed_reasons":["ConflictsAcceptedKnowledge"],"expected_subject":null,"reasons":["ConflictsAcceptedKnowledge"],"target_aliases":["K_SCOPE_BASE"],"verdict":"Rejected"} got {"kind":"Rejected","latency_ms":1300,"reason":"SemanticDuplicate","reason_identity":"p041"} notes=["expected reason in [\"ConflictsAcceptedKnowledge\"], got SemanticDuplicate"]
- `adversarial_near_duplicate_scope_narrowing_01` `adversarial_near_duplicate` diagnosis=ModelVerdictFailure expected {"allowed_reasons":[],"expected_subject":null,"reasons":[],"target_aliases":[],"verdict":"Accepted"} got {"kind":"Rejected","latency_ms":1293,"reason":"WrongSubject","subject":"Architecture"} notes=[]
- `adversarial_near_duplicate_implementation_phrasing_01` `adversarial_near_duplicate` diagnosis=ModelVerdictFailure expected {"allowed_reasons":["SourceRequired","FalseOrUnsupported"],"expected_subject":null,"reasons":["SourceRequired","FalseOrUnsupported"],"target_aliases":[],"verdict":"Rejected"} got {"kind":"Rejected","latency_ms":1193,"reason":"WrongSubject","subject":"Architecture"} notes=["expected reason in [\"SourceRequired\", \"FalseOrUnsupported\"], got WrongSubject"]
- `adversarial_near_duplicate_source_phrasing_01` `adversarial_near_duplicate` diagnosis=ModelVerdictFailure expected {"allowed_reasons":["SourceRequired"],"expected_subject":null,"reasons":["SourceRequired"],"target_aliases":[],"verdict":"Rejected"} got {"kind":"Rejected","latency_ms":1944,"reason":"WrongSubject","subject":"Architecture"} notes=["expected reason in [\"SourceRequired\"], got WrongSubject"]
