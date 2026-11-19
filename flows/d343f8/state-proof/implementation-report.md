# System-state proof implementation report

## Frozen unpaid packet

- Manifest SHA-256: `0fc2bed0944deb0089d860ba5124d9e3b6f4f601b108d3a44662fce8ae7e4242`
- Controller SHA-256: `82a40e86f5c177d8058bfc994e04f480db86a51dfe7e2a584e096f400c170407`
- Test SHA-256: `785f9e9b42c0e8d5424e8524c169ca63c01644296e2aec0922f0a6c497556b48`
- Snapshot SHA-256: `3da81d708dfdaf1aa79fe6aed83823b11158103b2faa70ed41669d09c466aba4`
- Snapshot captured: `2026-11-19T06:28:47Z`; all five collection sources were available. The 900-second capture-age window expires at `2026-11-19T06:43:47Z`.
- Slots: exactly three, once each, Haiku → Sonnet → Opus; per-slot maximums `$0.66560`, `$2.138112`, `$0.10048`; conservative sum `$2.904192`; configured campaign cap `$10.00`, count cap 3. The count is an upper bound, not a completion promise.
- Same snapshot and prompt bytes for all slots (prompt SHA-256 `9db078916ec8a951ae648ce081cad2a61bbd1fdc63192d17747fbc5d58ebfbcb`); Opus prompt is 17,198 bytes, within its 20,000-input-token bound under the installed policy's admission rule.
- Frozen closure: 16 source/static files and four external executable identities, derived from installed worker policy. Mutable ledger contents remain outside this controller and are validated only by the unchanged worker.

## Captured facts

The frozen snapshot records 26 flow identities and UI-only status counts (3 `working`, 23 `done`), 20 queues with 46 pending messages, and host load averages `0.05 / 0.02 / 0.00`, one runnable task, 32 CPUs. Queue payloads are withheld. Host load is labeled as load average, not CPU utilization. Claude reports Week 66% and FableWeek 34%, pace `Under` at 73% expected. Codex reports Week 5%, pace `Over` at 3% expected. Its deployed observation is 1,121 seconds old at capture; the exact epoch and age are included. Configuration allows cached weekly Energy readings up to 3,600 seconds old while requiring the host/flow/queue snapshot itself to be no more than 900 seconds old. These limits state evidence age, not a claim that the readings are current.

## Local verification

Command: `PYTHONDONTWRITEBYTECODE=1 /nix/store/bya4ansy58az5133kryqp2cvrxbnz8qy-python3-3.14.10/bin/python3.14 -B tests.py`

Exit: `0`; 32 tests passed. Fixtures are synthetic/local and exercise strict JSON decoding (including duplicate-key rejection), Datom escaping and payload withholding, source interpretation, model-bound calculation, exact three-slot enforcement, drift, concurrency/restart refusal, full-reservation admission, durable intent ordering, and stop-before-next-call behavior on drift, budget, refusal, truncation, and uncertainty. A valid-looking partial JSON answer with `max_tokens` is recorded as `TruncatedOutput`, never accepted as an answer. The production API has no output-path override. No adapter, provider, helper, credential source, ledger, or runtime policy was invoked or changed in this work.

## Admission and execution

Research must first place its exact `ResearchSystemStateAdmission.v1` decision at the configured fixed admission path and match this manifest hash, three-call cap, `$10.00` maximum, UUID namespace, expiry, and at least `$2.904192` global unreserved headroom. The worker remains the sole accounting authority and retains its global gate. Only after Research admission and review, invoke from this directory with the pinned interpreter:

```sh
PYTHONDONTWRITEBYTECODE=1 /nix/store/bya4ansy58az5133kryqp2cvrxbnz8qy-python3-3.14.10/bin/python3.14 -B proof.py run
```

The program checks snapshot and source freshness, manifest and complete installed execution closure at launch and immediately before each child; it creates a durable one-shot namespace and slot intent before the adapter boundary. Any unknown receipt or transport outcome stops the sequence and holds the full current bound. It never retries or reuses a result namespace.

## Limits and unresolved review

- `energy-nexus Read.Codex` returned its stored observation at epoch `1795068606`, age 1,121 seconds at capture. The configured weekly-observation limit is 3,600 seconds; run-time checks fail closed after that limit. The snapshot recency limit remains 900 seconds. Research should inspect these explicit ages; no observation is silently refreshed during `run`.
- The fixtures do not establish real provider refusal frequency, worker deployment behavior, or Nexus certification. Native refusal, task refusal, malformed answer, and timeout/receipt uncertainty cases are synthetic; a timeout fixture performs no provider call.
- The controller records receipt pointers, usage, and worker cost estimates as observations; it is not a second ledger. No paid execution occurred, and no result namespace was created.
