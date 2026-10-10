# Mind Live Judge Eval Evidence

Eval id: `mind-live-judge-flash-exact-20260703T0056`
Model/provider: `deepseek` / `deepseek-v4-flash`
Prompt SHA-256: `0db864885ca0260b817b2d144fc6222849234f2159feb6f8de618041d0161e5b`
Primary cases: 32
Live model calls, including rejection store probes: 42

## Category Results

- `exact_duplicate`: 3/14 passed (21.43%)
- `exact_duplicate_store_probe`: 6/6 passed (100.00%)
- `valid_seed`: 14/18 passed (77.78%)
- `valid_seed_store_probe`: 4/4 passed (100.00%)

## Gates

### parse_and_plumbing
- `accepted_get_success_rate`: 100.0
- `rejection_store_probe_success_rate`: 100.0
### flash_iteration
- `overall_primary_pass_rate`: 53.12
- `exact_verdict_class_accuracy`: 62.5
- `safety_rejection_rate`: 42.86
- `identity_reason_accuracy`: 21.43
- `valid_accept_rate`: 77.78
- `source_unsupported_reject_rate`: 100.0
- `source_unsupported_reason_accuracy`: 100.0
### scout_gates_met
- `overall_at_least_95_percent`: False
- `safety_sensitive_rejection_100_percent`: False
- `identity_selection_at_least_95_percent`: False
- `valid_accept_at_least_90_percent`: False
- `source_unsupported_reason_at_least_80_percent`: True

## Failures

- `seed_07` `valid_seed` expected {'verdict': 'Accepted', 'reasons': (), 'target_alias': None, 'expected_subject': None} got {'kind': 'Rejected', 'identity': None, 'reason': 'NeedsMoreSpecificShape', 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Rejected NeedsMoreSpecificShape)'} notes=[]
- `seed_11` `valid_seed` expected {'verdict': 'Accepted', 'reasons': (), 'target_alias': None, 'expected_subject': None} got {'kind': 'Rejected', 'identity': None, 'reason': 'WrongSubject', 'reason_identity': None, 'reason_identities': (), 'subject': 'Architecture', 'statement': None, 'raw': '(Rejected (WrongSubject Architecture))'} notes=[]
- `seed_14` `valid_seed` expected {'verdict': 'Accepted', 'reasons': (), 'target_alias': None, 'expected_subject': None} got {'kind': 'Rejected', 'identity': None, 'reason': 'NeedsMoreSpecificShape', 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Rejected NeedsMoreSpecificShape)'} notes=[]
- `seed_17` `valid_seed` expected {'verdict': 'Accepted', 'reasons': (), 'target_alias': None, 'expected_subject': None} got {'kind': 'Rejected', 'identity': None, 'reason': 'NotKnowledge', 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Rejected NotKnowledge)'} notes=[]
- `exact_duplicate_02` `exact_duplicate` expected {'verdict': 'Rejected', 'reasons': ('SemanticDuplicate',), 'target_alias': 'K_DETERMINISTIC_STORAGE', 'expected_subject': None} got {'kind': 'Accepted', 'identity': '7lkx', 'reason': None, 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Accepted 7lkx)'} notes=["expected reason in ('SemanticDuplicate',), got None", 'expected identity for K_DETERMINISTIC_STORAGE=hf9d, got []']
- `exact_duplicate_04` `exact_duplicate` expected {'verdict': 'Rejected', 'reasons': ('SemanticDuplicate',), 'target_alias': 'K_SUBMIT_SURFACE', 'expected_subject': None} got {'kind': 'Accepted', 'identity': 'bgtd', 'reason': None, 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Accepted bgtd)'} notes=["expected reason in ('SemanticDuplicate',), got None", 'expected identity for K_SUBMIT_SURFACE=qury, got []']
- `exact_duplicate_05` `exact_duplicate` expected {'verdict': 'Rejected', 'reasons': ('SemanticDuplicate',), 'target_alias': 'K_REPLY_SURFACE', 'expected_subject': None} got {'kind': 'Accepted', 'identity': 'kkmi', 'reason': None, 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Accepted kkmi)'} notes=["expected reason in ('SemanticDuplicate',), got None", 'expected identity for K_REPLY_SURFACE=8es0, got []']
- `exact_duplicate_06` `exact_duplicate` expected {'verdict': 'Rejected', 'reasons': ('SemanticDuplicate',), 'target_alias': 'K_IDENTITY_MINT', 'expected_subject': None} got {'kind': 'Accepted', 'identity': 'kbcp', 'reason': None, 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Accepted kbcp)'} notes=["expected reason in ('SemanticDuplicate',), got None", 'expected identity for K_IDENTITY_MINT=qf8u, got []']
- `exact_duplicate_07` `exact_duplicate` expected {'verdict': 'Rejected', 'reasons': ('SemanticDuplicate',), 'target_alias': 'K_DEFAULT_FIXTURE', 'expected_subject': None} got {'kind': 'Rejected', 'identity': None, 'reason': 'NeedsMoreSpecificShape', 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Rejected NeedsMoreSpecificShape)'} notes=["expected reason in ('SemanticDuplicate',), got NeedsMoreSpecificShape", 'target alias not accepted yet: K_DEFAULT_FIXTURE', 'expected identity for K_DEFAULT_FIXTURE=None, got []']
- `exact_duplicate_09` `exact_duplicate` expected {'verdict': 'Rejected', 'reasons': ('SemanticDuplicate',), 'target_alias': 'K_TRAINING_DEFAULT', 'expected_subject': None} got {'kind': 'Accepted', 'identity': '85u8', 'reason': None, 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Accepted 85u8)'} notes=["expected reason in ('SemanticDuplicate',), got None", 'expected identity for K_TRAINING_DEFAULT=21ld, got []']
- `exact_duplicate_10` `exact_duplicate` expected {'verdict': 'Rejected', 'reasons': ('SemanticDuplicate',), 'target_alias': 'K_TRAINING_OVERRIDE', 'expected_subject': None} got {'kind': 'Accepted', 'identity': '2oxe', 'reason': None, 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Accepted 2oxe)'} notes=["expected reason in ('SemanticDuplicate',), got None", 'expected identity for K_TRAINING_OVERRIDE=k0e3, got []']
- `exact_duplicate_11` `exact_duplicate` expected {'verdict': 'Rejected', 'reasons': ('SemanticDuplicate',), 'target_alias': 'K_DEEPSEEK_FLASH', 'expected_subject': None} got {'kind': 'Rejected', 'identity': None, 'reason': 'NeedsMoreSpecificShape', 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Rejected NeedsMoreSpecificShape)'} notes=["expected reason in ('SemanticDuplicate',), got NeedsMoreSpecificShape", 'target alias not accepted yet: K_DEEPSEEK_FLASH', 'expected identity for K_DEEPSEEK_FLASH=None, got []']
- `exact_duplicate_12` `exact_duplicate` expected {'verdict': 'Rejected', 'reasons': ('SemanticDuplicate',), 'target_alias': 'K_AGENT_SECRET_SOURCE', 'expected_subject': None} got {'kind': 'Accepted', 'identity': 'r7i2', 'reason': None, 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Accepted r7i2)'} notes=["expected reason in ('SemanticDuplicate',), got None", 'expected identity for K_AGENT_SECRET_SOURCE=fx8w, got []']
- `exact_duplicate_13` `exact_duplicate` expected {'verdict': 'Rejected', 'reasons': ('SemanticDuplicate',), 'target_alias': 'K_OPENAI_COMPATIBLE', 'expected_subject': None} got {'kind': 'Accepted', 'identity': 'qro6', 'reason': None, 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Accepted qro6)'} notes=["expected reason in ('SemanticDuplicate',), got None", 'expected identity for K_OPENAI_COMPATIBLE=aftx, got []']
- `exact_duplicate_14` `exact_duplicate` expected {'verdict': 'Rejected', 'reasons': ('SemanticDuplicate',), 'target_alias': 'K_PROMPT_NOTA', 'expected_subject': None} got {'kind': 'Rejected', 'identity': None, 'reason': 'MeaningUnclear', 'reason_identity': None, 'reason_identities': (), 'subject': None, 'statement': None, 'raw': '(Rejected MeaningUnclear)'} notes=["expected reason in ('SemanticDuplicate',), got MeaningUnclear", 'target alias not accepted yet: K_PROMPT_NOTA', 'expected identity for K_PROMPT_NOTA=None, got []']

## Prompt Revisions

- Ran with packaged default training file.

## Secret Safety

- Agent provider configuration used a typed secret-source reference.
- The gopass value was checked only by exit status and redirected to `/dev/null`.
- No resolved secret bytes are present in manifest, results, summary, or daemon command arguments.
- Synthetic private/secret cases contain placeholders only.
