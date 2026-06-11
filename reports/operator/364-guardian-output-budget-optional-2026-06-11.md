# Guardian Output Budget Optional

Operator report for the follow-up requested on 2026-06-11.

## Result

The guardian output token budget is now optional end-to-end.

Landed commits:

- `signal-spirit` `c2bfeb57` — `signal-spirit: make guardian output budget optional`
- `spirit` `c2ed1737` — `spirit: omit guardian output cap when absent`

## Contract Change

`SpiritGuardianAgentConfiguration` now carries:

- `maximum_output_tokens: Option<SpiritGuardianMaximumOutputTokens>`

Its accessor now returns `Option<u64>`. Existing callers may still pass a
budget with `Some(...)`, but the normal guardian path can pass `None`.

## Runtime Change

Spirit's `AgentGuardianConfiguration` now preserves that optional value. The
prompt builder maps it directly into `signal-agent`:

- `Some(n)` becomes `PromptOptions.maximum_output_tokens = Some(n)`
- `None` becomes `PromptOptions.maximum_output_tokens = None`

So the provider request omits `max_tokens` when the guardian has no configured
budget.

## Tests Added

- Contract archive round-trip for guardian config with no output budget.
- Configuration writer process-boundary test for a guardian startup archive with
  `None` output budget.
- Fake-agent assertion that Spirit sends `maximum_output_tokens = None`.
- Large guardian rejection explanation preservation test.
- Live DeepSeek scenario expansion:
  - valid proposal with detailed justification that must not become `Compound`
  - duplicate proposal against a seeded record

## Verification

Green checks:

- `signal-spirit`: `cargo test`
- `signal-spirit`: `cargo clippy -- -D warnings`
- `spirit`: `cargo test --features agent-guardian`
- `spirit`: `cargo test --features nota-text configuration_writer_accepts_guardian_without_output_budget -- --nocapture`
- `spirit`: `cargo clippy --features agent-guardian -- -D warnings`
- `spirit`: `cargo test --features agent-guardian --test guardian_live_scenarios -- --ignored --nocapture`

The live DeepSeek run passed with `deepseek-v4-flash` and no explicit
`max_tokens` setting.
