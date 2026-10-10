# Mind Live Judge Eval Evidence

Eval id: `mind-live-judge-flash-20260703T004505`
Model/provider: `deepseek` / `deepseek-v4-flash`
Prompt SHA-256: `ae8beeab782abe3a837f61f98657996c3f53a032ecb6ec29212fc7f6e0500a48`
Primary cases: 6
Live model calls, including rejection store probes: 6

## Category Results

- `valid_seed`: 6/6 passed (100.00%)

## Gates

### parse_and_plumbing
- `accepted_get_success_rate`: 100.0
- `rejection_store_probe_success_rate`: 100.0
### flash_iteration
- `overall_primary_pass_rate`: 100.0
- `exact_verdict_class_accuracy`: 100.0
- `safety_rejection_rate`: 100.0
- `identity_reason_accuracy`: 100.0
- `valid_accept_rate`: 100.0
- `source_unsupported_reject_rate`: 100.0
- `source_unsupported_reason_accuracy`: 100.0
### scout_gates_met
- `overall_at_least_95_percent`: True
- `safety_sensitive_rejection_100_percent`: True
- `identity_selection_at_least_95_percent`: True
- `valid_accept_at_least_90_percent`: True
- `source_unsupported_reason_at_least_80_percent`: True

## Failures

No failures.

## Prompt Revisions

- Ran with packaged default training file.

## Secret Safety

- Agent provider configuration used a typed secret-source reference.
- The gopass value was checked only by exit status and redirected to `/dev/null`.
- No resolved secret bytes are present in manifest, results, summary, or daemon command arguments.
- Synthetic private/secret cases contain placeholders only.
