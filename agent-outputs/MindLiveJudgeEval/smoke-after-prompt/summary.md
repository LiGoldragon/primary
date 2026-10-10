# Mind Live Judge Eval Evidence

Eval id: `mind-live-judge-flash-20260703T004415`
Model/provider: `deepseek` / `deepseek-v4-flash`
Prompt SHA-256: `10881adb983e4adce3b08d0517807cbf8e5ba3733ad32050ae21a2ee23114c95`
Primary cases: 6
Live model calls, including rejection store probes: 6

## Category Results

- `valid_seed`: 0/6 passed (0.00%)

## Gates

### parse_and_plumbing
- `accepted_get_success_rate`: 100.0
- `rejection_store_probe_success_rate`: 100.0
### flash_iteration
- `overall_primary_pass_rate`: 0.0
- `exact_verdict_class_accuracy`: 0.0
- `safety_rejection_rate`: 100.0
- `identity_reason_accuracy`: 100.0
- `valid_accept_rate`: 0.0
- `source_unsupported_reject_rate`: 100.0
- `source_unsupported_reason_accuracy`: 100.0
### scout_gates_met
- `overall_at_least_95_percent`: False
- `safety_sensitive_rejection_100_percent`: True
- `identity_selection_at_least_95_percent`: True
- `valid_accept_at_least_90_percent`: False
- `source_unsupported_reason_at_least_80_percent`: True

## Failures

- `seed_01` `valid_seed` expected {'verdict': 'Accepted', 'reasons': (), 'target_alias': None, 'expected_subject': None} got {'kind': 'Rejected', 'identity': None, 'reason': 'NeedsMoreSpecificShape', 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Rejected NeedsMoreSpecificShape)'} notes=[]
- `seed_02` `valid_seed` expected {'verdict': 'Accepted', 'reasons': (), 'target_alias': None, 'expected_subject': None} got {'kind': 'Rejected', 'identity': None, 'reason': 'WrongSubject', 'reason_identity': None, 'reason_identities': (), 'subject': 'Component', 'statement': None, 'raw': '(Rejected (WrongSubject Component))'} notes=[]
- `seed_03` `valid_seed` expected {'verdict': 'Accepted', 'reasons': (), 'target_alias': None, 'expected_subject': None} got {'kind': 'Rejected', 'identity': None, 'reason': 'NotKnowledge', 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Rejected NotKnowledge)'} notes=[]
- `seed_04` `valid_seed` expected {'verdict': 'Accepted', 'reasons': (), 'target_alias': None, 'expected_subject': None} got {'kind': 'Rejected', 'identity': None, 'reason': 'NotKnowledge', 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Rejected NotKnowledge)'} notes=[]
- `seed_05` `valid_seed` expected {'verdict': 'Accepted', 'reasons': (), 'target_alias': None, 'expected_subject': None} got {'kind': 'Rejected', 'identity': None, 'reason': 'NotKnowledge', 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Rejected NotKnowledge)'} notes=[]
- `seed_06` `valid_seed` expected {'verdict': 'Accepted', 'reasons': (), 'target_alias': None, 'expected_subject': None} got {'kind': 'Rejected', 'identity': None, 'reason': 'NotKnowledge', 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Rejected NotKnowledge)'} notes=[]

## Prompt Revisions

- Ran with packaged default training file.

## Secret Safety

- Agent provider configuration used a typed secret-source reference.
- The gopass value was checked only by exit status and redirected to `/dev/null`.
- No resolved secret bytes are present in manifest, results, summary, or daemon command arguments.
- Synthetic private/secret cases contain placeholders only.
