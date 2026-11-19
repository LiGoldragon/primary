# December campaign controller implementation report

## Status and frozen identity

Unpaid source and synthetic-fixture work is complete. Research admission remains pending. No paid API call, credential invocation, real processor `invoke`, worker or ledger edit, Rust build, deployment, or campaign execution occurred. The existing Rust binary was used only for local `prepare`; no `results/` directory was created.

Owned files: `controller.py`, `generator.py`, `proposal-manifest.json`, `tests.py`, `implementation-report.md`, and `inputs/` (672 immutable call/prompt files).

- Manifest SHA256: `c5f9523d85061823c3610bb1a3273e8b8c10950d0c0e0acb9cab152e42365307`
- Canonical manifest SHA256: `65e98f7ad95afa3426e6040d6a2bab142cd19b8e28cdf5e60462f7614a3f0e6a`
- Stage UUID namespace: `b8b816ee-56d4-5b14-91d3-aa26db1f49cb` (unchanged)
- Controller SHA256: `7920673ea9bfcf4a4335e27a3d1591baccaf1e9ca4ddfeea9b362f24c0a1d70b`
- Generator SHA256: `7c2cd86f481905025f9c00238167dd7ab3758fe68dbb1934adf57f5cef6b96a4`
- Tests SHA256: `745eded8b91082976bf83e89a4a1d3e569c154ea764d2f3b2be9eabdcdf2c6da`

The refreeze preserved the exact pre-existing call and prompt bytes and hashes for all 336 slot identifiers. Research admission must bind the exact manifest hash, 336-slot ceiling, and 20 USD campaign retained ceiling, and verify the current global budget before any call.

## Frozen campaign and reservation bounds

| Work | Cases | Slots | Admission / Queue slots |
|---|---:|---:|---:|
| Historical deliberate variance | 52 (22 Admission, 30 Queue) | 312 | 132 / 180 |
| Missing-evidence derivations | 4 | 12 | 6 / 6 |
| Declared malformed-answer probes | 4 | 12 | 6 / 6 |
| **Maximum** | **60** | **336** | **144 / 192** |

Each of the 52 historical cases has two prompt-identical replicates across three models. Eight historically scoped permissions remain excluded. Derived cases retain provenance and explicit withheld inputs, assert no semantic labels, and do not alter the strict decoder. Malformed probes declare the incompatible requested output format.

| Model | Slots | Full bound per slot | Full reservation bound | Total output-token bound |
|---|---:|---:|---:|---:|
| `claude-haiku-5-5` | 112 | $0.6656 | $74.5472 | 458,752 |
| `claude-sonnet-5-5` | 112 | $2.138112 | $239.468544 | 458,752 |
| `claude-opus-5-5` | 112 | $0.10048 | $11.25376 | 114,688 |
| **All models** | **336** |  | **$325.269504** | **1,032,192** |

Every Opus prompt satisfies `prompt bytes + 150 system bytes + 1,024 frame bytes <= 20,000`. The full configured reservation exceeds the 20 USD campaign ceiling, so 336 is a hard maximum, not a completion promise. Before each call, the controller requires the complete next model-specific reservation to fit the remaining campaign and global envelopes.

## Execution closure and durable one-shot boundary

The manifest freezes and the controller rechecks the recursive worker Python source closure (`general_adapter.py`, `raw_adapter.py`, `raw_ledger.py`, `ledger.py`, `policy.py`, `model_policy.py`, `settlement_evidence.py`, `producer_guard.py`); `general-policy.json`, native `policy.json`, `settlement-policy.json`, the historical settlement-evidence manifest, and CA bundle; plus exact interpreter, curl, bubblewrap, and gopass file identities. It also freezes the trial processor binary/configuration and campaign sources. Runtime checks re-derive the closure before each slot and fail closed on path or digest drift.

The mutable authoritative ledger is recorded separately by its configured path, device/inode, and configured baseline-prefix SHA256. Ledger contents are not copied into the manifest or controller; the pinned worker and Research retain ledger validation and accounting. No ledger content was changed.

Before a child boundary, the controller durably creates/syncs the result namespace and parent entries, writes and fsyncs `run-started.json`, then durably creates/syncs the slot directory and writes/fsyncs `started.json`. The exclusive launch lock is placed in the durable parent. Any directory-sync failure stops before invocation. A local order fixture confirmed every slot-directory ancestor and both intent markers were durable before the mocked child; an injected slot-directory fsync failure made zero mocked child calls and wrote no slot intent. Restart/concurrency refusal and one-call/no-replay markers remain covered.

## Local evidence

Commands executed with bytecode disabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python -B generator.py --prepare-timeout 30
PYTHONDONTWRITEBYTECODE=1 python -B tests.py
PYTHONDONTWRITEBYTECODE=1 python -B controller.py verify
PYTHONDONTWRITEBYTECODE=1 python -B controller.py dry-run
```

All exited 0. Generator reported 336 slots and zero provider calls. Refreeze comparison confirmed unchanged UUID namespace and exact call/prompt bytes and hashes. All **29** local fixtures passed. `verify` and `dry-run` each reported 336 slots, 112 per model, zero calls; no result namespace was created. Fixtures cover exact count and task mix, injection/drift, per-slot bounds and output limits, prompt reuse, source provenance, missing evidence, malformed probes, budget guards, durable directory/intent ordering and injected sync failure, exclusive launch, restart/no replay, timeout/process/receipt uncertainty, refusal and decoder classification, and production API isolation.

## Limits and execution gate

Provider outcomes are synthetic. The native-refusal fixture checks classification, not real refusal frequency or settlement. The timeout fixture makes no paid request and establishes no actual charge. These tests are not full Flow Nexus certification or Research ledger admission. Any provider or settlement uncertainty must stop the campaign and retain the full reservation.

After Research admits the exact manifest and verifies the current global budget, the pinned interpreter from `flows/250509/trial/processor.json` may run:

```sh
/nix/store/bya4ansy58az5133kryqp2cvrxbnz8qy-python3-3.14.10/bin/python3.14 flows/d343f8/campaign/controller.py verify --manifest flows/d343f8/campaign/proposal-manifest.json
/nix/store/bya4ansy58az5133kryqp2cvrxbnz8qy-python3-3.14.10/bin/python3.14 flows/d343f8/campaign/controller.py dry-run --manifest flows/d343f8/campaign/proposal-manifest.json
/nix/store/bya4ansy58az5133kryqp2cvrxbnz8qy-python3-3.14.10/bin/python3.14 flows/d343f8/campaign/controller.py run --manifest flows/d343f8/campaign/proposal-manifest.json --research-admission /path/to/research-admission.json
```

The final `run` command is not authorized before Research admission. The pinned worker remains the per-call accounting authority and enforces its global reservation gate.
