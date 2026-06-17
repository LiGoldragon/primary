# Spirit Guardian Positive-Guidance Implementation

Date: 2026-06-17
Role: system-designer

## Intent Anchor

The implementation follows Spirit record `nr7h`: guardian admission should accept captures whose operative guidance states the affirmative shape to follow, and should return primarily exclusion/prohibition/definition-by-negation captures for positive rewording.

This was prompted by the failed shape of the earlier spelling correction record `cx2m`, which mixed the canonical `criome` / `criomos` spelling rule with a negative list of rejected spellings. I did not mutate `cx2m`: a `ChangeRecord` attempt was refused by the guardian for insufficient warrant to edit that existing record directly.

## Branches Pushed

| Repo | Branch | Commit | Purpose |
|---|---:|---:|---|
| `signal-spirit` | `guardian-negative-guideline-reason` | `e5f432b2` | Adds `GuardianRejectionReason::NegativeGuideline` to the generated signal contract and round-trip coverage. |
| `meta-signal-spirit` | `guardian-negative-guideline-reason` | `d442d8c6` | Aligns the meta-signal dependency to the signal branch so Spirit can consume one coherent contract source. |
| `spirit` | `guardian-positive-guidance` | `a876d6ff` | Adds the guardian prompt gate, worked examples, docs, and the live-scenario expectation for negative-guideline rejection. |

Pull-request entry points:

- `https://github.com/LiGoldragon/signal-spirit/pull/new/guardian-negative-guideline-reason`
- `https://github.com/LiGoldragon/meta-signal-spirit/pull/new/guardian-negative-guideline-reason`
- `https://github.com/LiGoldragon/spirit/pull/new/guardian-positive-guidance`

## What Changed

`signal-spirit` now has a first-class `NegativeGuideline` rejection reason. The generated schema artifacts were regenerated and a NOTA round-trip test was added so the new reason is not just a prompt convention.

`spirit` now exposes that reason to the agent-guardian model through `MODEL_REASONS`, gives it an admission gloss, and adds an `AFFIRMATIVE GUIDANCE` gate in the checklist. The gate is semantic: it is not a substring filter for words like "not"; it asks whether the operative guidance is centered on the positive rule or primarily on exclusion/prohibition/forbidden wording/definition-by-negation.

The prompt few-shots now include the exact criome/criomos failure mode:

- negative shape: canonical names plus "creome and creomos are misspellings" is rejected as `NegativeGuideline`;
- positive shape: canonical prose uses `criome` for the authentication component and `criomos` for the operating system name, while exact on-disk path spelling is preserved when citing repository paths.

`spirit/INTENT.md` and `spirit/ARCHITECTURE.md` now document the admission rule, the typed rejection reason, and the fact that the submitting agent should re-plead the affirmative rule after rejection.

## Verification

`signal-spirit`:

- `SIGNAL_SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo check --features nota-text`
- `cargo test --features nota-text`
- `cargo fmt --check`

`meta-signal-spirit`:

- `cargo update -p signal-spirit`
- `cargo check --features nota-text`
- `cargo fmt --check`

`spirit`:

- `cargo update -p signal-spirit -p meta-signal-spirit`
- `cargo check --features agent-guardian`
- `cargo fmt --check`
- `cargo test --features agent-guardian guardian_prompt`

The Spirit test run passed the guardian prompt unit tests and runtime prompt-bundle tests. The new live scenario is present as an expected eval case; I did not run a live model evaluation in this pass.

## Integration Notes

This is a three-repo branch chain. Operator integration should merge or rebase `signal-spirit` first, then `meta-signal-spirit`, then `spirit`, or retarget Spirit back to `main` once the contract branches land.

The implementation intentionally leaves the old `cx2m` record untouched. Retiring or changing it should be done only if the psyche explicitly authorizes that specific existing-record mutation.
