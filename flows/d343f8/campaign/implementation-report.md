# December campaign controller implementation report

## Status and owned files

Source and unpaid fixture work is complete. Research admission is pending. No provider API, real processor `invoke`, credentials, worker policy, Rust build, deployment, or campaign execution was used. The Rust binary was used only by the generator's local `prepare` operation. The planned `results/` directory was not created.

Owned files:

- `controller.py`
- `generator.py`
- `proposal-manifest.json`
- `tests.py`
- `inputs/` — 672 immutable call and prompt files (336 each)
- `implementation-report.md`

Manifest SHA256: `92f45cecc386cd8b9a3361b147a469de0449a0505743fab4864d802dac6dd53b`  
Manifest canonical SHA256: `99ee9f1c33e28caabe8bea823cc0e24ba56061aafd6f74dffd82764703ad7d21`  
Stage UUID namespace: `b8b816ee-56d4-5b14-91d3-aa26db1f49cb`

Research admission must name the exact manifest file hash above, all 336 slots, the manifest's 20 USD retained ceiling, and a current global-unreserved snapshot. No admission record is present in this work.

## Frozen work and bounds

| Work | Cases | Slots | Task split |
|---|---:|---:|---|
| Historical deliberate variance | 52 (22 Admission, 30 Queue) | 312 | Admission 132, Queue 180 |
| Missing-evidence derivations | 4 (2 per task) | 12 | Admission 6, Queue 6 |
| Declared malformed-answer probes | 4 (2 per task) | 12 | Admission 6, Queue 6 |
| **Total maximum** | 60 | **336** | Admission 144, Queue 192 |

Historical cases have two new replicates for each of three models. Their prompt bytes are checked against the historical prompt and the two new prompt hashes match. Historical receipts are baseline references only. Eight scoped historical cases remain excluded. Each of four derived cases has one slot per model; withheld inputs and wrong-format perturbations are explicit in the manifest, and derived cases have no asserted semantic label. The decoder is unchanged.

| Model | Slots | Max input tokens | Max output tokens/slot | Full reservation bound per slot | All-slot reservation bound | Total output-token bound |
|---|---:|---:|---:|---:|---:|---:|
| `claude-haiku-5-5` | 112 | 1,048,576 | 4,096 | $0.6656 | $74.5472 | 458,752 |
| `claude-sonnet-5-5` | 112 | 1,048,576 | 4,096 | $2.138112 | $239.468544 | 458,752 |
| `claude-opus-5-5` | 112 | 20,000 | 1,024 | $0.10048 | $11.25376 | 114,688 |
| **All models** | **336** |  |  |  | **$325.269504** | **1,032,192** |

Every generated Opus prompt satisfies `prompt UTF-8 bytes + 150 system bytes + 1,024 framing bytes <= 20,000`. The full maximum reservation exceeds the 20 USD campaign ceiling. Therefore, 336 is a hard upper limit, not a completion promise. Before each call the controller checks the whole next model-specific reservation against both the remaining campaign ceiling and the current global-unreserved amount; it stops when either cannot fit.

## Source identity

The manifest freezes the controller, generator, tests, trial processor binary and configuration, worker policy and adapter, relevant Rust processor/decoder sources, historical source packets, baseline receipts, and proposal authority. Selected pinned identities:

- Controller: `3e61e66784f2ddbba2df6ca87a61b128ee72cd898f1d2f6f7afac85982f40556`
- Generator: `fcd382deaad56f4505c70115fea9b14f95220f851ef90b47b0c9146ff9fd4615`
- Tests: `8daca3c2d48ce8c9629af0286e537e2cba51e2a504c92d266852dac3d32dac3c`
- Worker `general-policy.json`: `8f49359c2fab6038a5380f419d2a692df03312ff84dbf3cdde2a564bc5314e34`
- Worker `general_adapter.py`: `889d65b842ec78ce412f4cbca07c9340a8a542ebbeeab8c95faff708254559e8`
- Worker `model_policy.py`: `0016ff2555a21ce739ceec7098cfe08f98ef6e70eda7bfd0265d54b80d4563f2`
- Trial `processor.json`: `c9ba9ea8815fe059f7777a97c8fc75ee345f7ae3a67e3b768b500b0be4e99dc9`
- Typed-call binary: `ecd75629f915161da4c7b476a4087b9125cbc008286c812c11ace8ae158df73c`
- Rust decoder `src/lib.rs`: `60b6d2f32abf7c50a09780561dd65029085dd267b683ddfd11222a3036688e4a`

The manifest also pins `src/main.rs`, `tests/decoding.rs`, and the typed-call report. Effective model response codecs and each slot's call/prompt hashes are frozen there. The production `run_campaign` entry point uses only the frozen result directory and real subprocess boundary; result-directory and runner injection live only in the explicitly named synthetic test harness.

## Local evidence

Commands run from `/home/li/primary` with bytecode disabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python -B flows/d343f8/campaign/generator.py
PYTHONDONTWRITEBYTECODE=1 python -B flows/d343f8/campaign/tests.py
PYTHONDONTWRITEBYTECODE=1 python -B flows/d343f8/campaign/controller.py verify
PYTHONDONTWRITEBYTECODE=1 python -B flows/d343f8/campaign/controller.py dry-run
```

The generator exited 0 and used only `prepare`; its output reported 336 slots and zero provider calls. The local fixture suite exited 0: 25 tests passed. `verify` and `dry-run` each exited 0; dry-run reported 336 maximum slots, 112 per model, zero calls, and no guarantee of completing every configured slot.

Fixtures cover exact count and category/task mix, extra-slot injection, effective per-model reservation formula and drift, model output caps, Opus byte/system/frame bounds, exact replicate prompt reuse, baseline provenance, missing evidence, malformed probes, budget admission before child, campaign and global whole-reservation guards, concurrent launch, restart/no replay, durable uncertainty after timeout/nonzero exit, invalid/missing receipts, native refusal versus task refusal, malformed decoding, max-token stop, prompt/policy/source drift, multi-text response concatenation, allowed hidden-thinking blocks, and production API refusal of result-directory redirection.

## Remaining limits and execution gate

All runtime-boundary receipts and provider outcomes in tests are synthetic. A synthetic native-refusal fixture tests classification only; it does not establish real provider-refusal frequency or settlement behavior. A timeout fixture makes no real paid request and establishes no actual charge amount. Real uncertainty must continue to stop the chain and hold the full reservation. The fixtures are not a full Flow Nexus certification, deployment, or Research ledger admission.

After Research admits the exact manifest hash and confirms the current global snapshot, the operational path is:

```sh
PYTHONDONTWRITEBYTECODE=1 python -B flows/d343f8/campaign/controller.py verify --manifest flows/d343f8/campaign/proposal-manifest.json
PYTHONDONTWRITEBYTECODE=1 python -B flows/d343f8/campaign/controller.py dry-run --manifest flows/d343f8/campaign/proposal-manifest.json
PYTHONDONTWRITEBYTECODE=1 python -B flows/d343f8/campaign/controller.py run --manifest flows/d343f8/campaign/proposal-manifest.json --research-admission /path/to/research-admission.json
```

The `run` command is not authorized by this implementation report and must not be used before Research admission. The pinned worker remains the accounting authority and retains its global gate.
