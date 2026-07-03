# Rust Auditor Review

## Task And Scope

Audit of the just-landed local OpenAI-compatible subscription provider changes for Spirit/Mind/Agent contract behavior. Scope covered:

- `/git/github.com/LiGoldragon/meta-signal-agent` commit `1f615eba`
- `/git/github.com/LiGoldragon/agent` commit `9bf9d57c`
- `/git/github.com/LiGoldragon/mind` commit `e781e106`
- `/git/github.com/LiGoldragon/spirit` commit `d20982c4`
- implementation report `/home/li/primary/agent-outputs/LocalOpenAiSubscriptionProvider/GeneralCodeImplementer-Evidence.md`

Read `/home/li/primary/AGENTS.md`, each repo's `AGENTS.md`, and relevant architecture/code/test files. `meta-signal-agent` and `agent` `AGENTS.md` reference `INTENT.md`, but no `INTENT.md` exists in either checkout; `AGENTS.md` plus `ARCHITECTURE.md` were the available repo-local guidance.

Spirit query used: `PublicTextSearch [local OpenAI compatible provider subscription authorization]` returned public record `izsf`, which I used only as a review posture: provider changes should be checked structurally across the design, not just at one example call site.

## Findings

### Low: meta-signal-agent architecture and contract witness lag the new `NoSecret` variant

File: `/git/github.com/LiGoldragon/meta-signal-agent/ARCHITECTURE.md:28`

Risk: The schema and generated contract now define `SecretSource::NoSecret` (`schema/lib.schema:30`, `src/schema/lib.rs:102`), but the architecture record list still says the secret source variants are only `Environment`, `Gopass`, and `File` (`ARCHITECTURE.md:30`, `ARCHITECTURE.md:54`). The same repo's invariant says every operation and reply has rkyv and NOTA round-trip witnesses (`ARCHITECTURE.md:74`), while the current round-trip fixture only exercises `ConfigureProvider` with an environment secret source (`tests/round_trip.rs:25`, `tests/round_trip.rs:133`). This is not a runtime break because the downstream `agent` configuration writer successfully parses `NoSecret`, but it leaves the contract owner documentation and direct contract-level NOTA witness behind the shipped wire vocabulary.

Expected correction: Update the `SecretSource` record documentation to include `NoSecret`, and add a direct `meta-signal-agent` NOTA/rkyv round-trip fixture for `ConfigureProvider(... NoSecret)` so the contract crate itself witnesses the new variant.

## No Blocking Runtime Issues Found

DeepSeek remains intact in the audited path. The `agent` live-provider fixture suite passed, including the existing gopass-backed DeepSeek test and the new local no-auth/bearer request-shape tests.

The local provider defaults are present and consistent where expected:

- `agent` maps meta `SecretSource::NoSecret` into `agent::registry::SecretSource::NoSecret` and then into `ProviderAuthorization::None` without calling `KeySource` (`agent/src/registry.rs:100`, `agent/src/registry.rs:251`).
- `OpenAiCompatibleProvider` only attaches `Authorization: Bearer ...` when `ProviderAuthorization::Bearer` is present (`agent/src/provider.rs:367`).
- Mind local defaults are `local-openai`, `gpt-5.5`, and `http://127.0.0.1:18080/v1`; the live harness writes those into the agent provider seed with `NoSecret` and skips gopass preflight for `NoSecret` (`mind/src/configuration.rs:118`, `mind/src/bin/mind-live-knowledge-judge-eval.rs:1398`, `mind/src/bin/mind-live-knowledge-judge-eval.rs:1480`).
- Spirit guardian local defaults are `local-openai`, `gpt-5.5`, and `http://127.0.0.1:18080/v1`, with the guardian config carrying provider/model and relying on the agent daemon's provider seed for endpoint/secret-source resolution (`spirit/src/guardian.rs:87`, `spirit/src/bin/spirit-write-configuration.rs:181`).
- Mind and Spirit suppress DeepSeek-specific `reasoning_effort` and `thinking` fields when the configured provider is `local-openai` (`mind/src/knowledge.rs:289`, `spirit/src/guardian_prompt.rs:325`).

Searches found no `~/.codex/auth.json`, Claude, Gemini, or OAuth/subscription credential path in the changed source/test/doc surfaces. The local proxy credential ownership boundary is therefore preserved in these changes.

## Residual Risks And Test Gaps

- No live `gpt-5.5` local subscription-backed server evaluation was run. The audited evidence proves request shape and configuration, not model quality or local proxy availability.
- The Mind and Spirit reasoning-field suppression keys off the configured provider name being exactly `local-openai`. If a deployment relies on the agent daemon's default provider while leaving Mind/Spirit provider name unset, DeepSeek-specific fields would still be sent. The delivered local profile names the provider explicitly, so this is a deployment-shape caveat rather than a defect in the requested profile.
- `SystemKeySource::resolve(SecretSource::NoSecret)` returns an empty `ProviderApiKey` if called directly (`agent/src/registry.rs:323`), while the registry normally bypasses key resolution for `NoSecret`. This is harmless on the live path but could be tightened by making direct `NoSecret` resolution unreachable or typed separately.

## Checked Evidence

Commands run:

- `/git/github.com/LiGoldragon/meta-signal-agent`: `jj status --no-pager` showed a clean working copy with parent `1f615eba` on `main`.
- `/git/github.com/LiGoldragon/agent`: `jj status --no-pager` showed a clean working copy with parent `9bf9d57c` on `main`.
- `/git/github.com/LiGoldragon/mind`: `jj status --no-pager` showed a clean working copy with parent `e781e106` on `main`.
- `/git/github.com/LiGoldragon/spirit`: `jj status --no-pager` showed a clean working copy with parent `d20982c4` on `main`.
- `jj show --no-pager -r 1f615eba --stat && jj show --no-pager -r 1f615eba --git`
- `jj show --no-pager -r 9bf9d57c --stat && jj show --no-pager -r 9bf9d57c --git`
- `jj show --no-pager -r e781e106 --stat && jj show --no-pager -r e781e106 --git`
- `jj show --no-pager -r d20982c4 --stat && jj show --no-pager -r d20982c4 --git`
- `/git/github.com/LiGoldragon/meta-signal-agent`: `cargo test` passed, 5 tests.
- `/git/github.com/LiGoldragon/meta-signal-agent`: `cargo test --test round_trip provider_configuration_round_trips_through_nota_text_with_secret_source_only` passed, 1 test.
- `/git/github.com/LiGoldragon/agent`: `cargo test --features live-provider local_openai_compatible_provider --test fixture_round_trip` passed, 2 tests.
- `/git/github.com/LiGoldragon/agent`: `cargo test --features live-provider --test fixture_round_trip` passed, 10 tests, including `live_deepseek_flash_returns_valid_nota_with_gopass_key`.
- `/git/github.com/LiGoldragon/mind`: `cargo test local_openai_compatible --test cli` passed, 2 tests.
- `/git/github.com/LiGoldragon/mind`: `cargo test --bin mind-live-knowledge-judge-eval` passed, 6 tests.
- `/git/github.com/LiGoldragon/spirit`: `cargo test --features agent-guardian configuration_writer_accepts_local_openai_compatible_guardian --test process_boundary` passed, 1 test.
- `/git/github.com/LiGoldragon/spirit`: `cargo test --features agent-guardian --test guardian_live_scenarios -- --ignored --list` listed the ignored live DeepSeek scenarios; they were not run.
- Source searches for `auth.json`, `codex`, `claude`, `gemini`, and `oauth` across changed source/test/doc surfaces found no implementation path to subscription OAuth credentials.
