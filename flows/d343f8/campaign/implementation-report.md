# December campaign controller implementation report

## Status and frozen identity

Unpaid source and synthetic-fixture work is complete. Research admission remains pending. No paid API call, credential invocation, real processor `invoke`, worker or ledger edit, Rust build, deployment, or campaign execution occurred. The existing Rust binary was used only for local `prepare`; no `results/` directory was created.

Owned files: `controller.py`, `generator.py`, `proposal-manifest.json`, `tests.py`, `implementation-report.md`, and `inputs/` (672 immutable call/prompt files).

- Manifest SHA256: `d2c41dee2708fda8179e62d20920ae23d9a347006b0433b4a89a45e32a75dbf3`
- Canonical manifest SHA256: `b4e4f146ffe7ef8da1949cc8ddf3cbb93bdca7941366226440e608287b4d599c`
- Stage UUID namespace: `b8b816ee-56d4-5b14-91d3-aa26db1f49cb` (unchanged)
- Controller SHA256: `d2cd59f28c688c42c80db5134cc47be8b1bb8ba7ffcf92511f61af4bd4aedf76`
- Generator SHA256: `ce52caa4de88e65c142d4ff646f8a81162b7d0a87acb3287aa77a5118313f12a`
- Tests SHA256: `0854111c92d01938294ab937ef3fb75bc99ff067b75ea48b967fb5164550ab9f`

The refreeze used the generator's `--refresh-existing-inputs` mode, which verifies the complete existing input set and exact bytes before writing the new manifest. It preserved all 672 input files' bytes, inodes, and modes, as well as exact call/prompt hashes and the UUID namespace. Research admission must bind the exact manifest hash, 336-slot ceiling, and 20 USD campaign retained ceiling, and verify the current global budget before any call.

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

Commands executed from the campaign directory with bytecode disabled:

```sh
/nix/store/bya4ansy58az5133kryqp2cvrxbnz8qy-python3-3.14.10/bin/python3.14 -B generator.py --prepare-timeout 30 --refresh-existing-inputs
/nix/store/bya4ansy58az5133kryqp2cvrxbnz8qy-python3-3.14.10/bin/python3.14 -B tests.py
/nix/store/bya4ansy58az5133kryqp2cvrxbnz8qy-python3-3.14.10/bin/python3.14 -B controller.py verify
/nix/store/bya4ansy58az5133kryqp2cvrxbnz8qy-python3-3.14.10/bin/python3.14 -B controller.py dry-run
```

All exited 0 under the exact pinned interpreter. Generator reported 336 slots and zero provider calls. Refreeze comparison confirmed unchanged input bytes, inodes, modes, UUID namespace, and call/prompt hashes. All **30** local fixtures passed, including equivalent controller-interpreter symlink spelling. `verify` and `dry-run` each reported 336 slots, 112 per model, zero calls; no result namespace was created. Fixtures cover exact count and task mix, injection/drift, per-slot bounds and output limits, prompt reuse, source provenance, missing evidence, malformed probes, budget guards, durable directory/intent ordering and injected sync failure, exclusive launch, restart/no replay, timeout/process/receipt uncertainty, refusal and decoder classification, and production API isolation.

## Limits and execution gate

Provider outcomes are synthetic. The native-refusal fixture checks classification, not real refusal frequency or settlement. The timeout fixture makes no paid request and establishes no actual charge. These tests are not full Flow Nexus certification or Research ledger admission. Any provider or settlement uncertainty must stop the campaign and retain the full reservation.

After Research admits the exact manifest and verifies the current global budget, the pinned interpreter from `flows/250509/trial/processor.json` may run:

```sh
/nix/store/bya4ansy58az5133kryqp2cvrxbnz8qy-python3-3.14.10/bin/python3.14 flows/d343f8/campaign/controller.py verify --manifest flows/d343f8/campaign/proposal-manifest.json
/nix/store/bya4ansy58az5133kryqp2cvrxbnz8qy-python3-3.14.10/bin/python3.14 flows/d343f8/campaign/controller.py dry-run --manifest flows/d343f8/campaign/proposal-manifest.json
/nix/store/bya4ansy58az5133kryqp2cvrxbnz8qy-python3-3.14.10/bin/python3.14 flows/d343f8/campaign/controller.py run --manifest flows/d343f8/campaign/proposal-manifest.json --research-admission /path/to/research-admission.json
```

The final `run` command is not authorized before Research admission. The pinned worker remains the per-call accounting authority and enforces its global reservation gate.
