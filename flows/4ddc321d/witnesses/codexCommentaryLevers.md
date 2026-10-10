# Codex CLI 0.149.1: Commentary control levers

Witness record for tag `rust-v0.149.1` in `/git/github.com/openai/codex`.

## Verdict

No lever exists in Codex CLI 0.149.1 to control commentary frequency, suppress commentary, or filter commentary from history replay. The only output-control knob is `model_verbosity` (Low/Medium/High), which maps to the Responses API `text.verbosity` parameter and controls the model's overall output length, not commentary specifically.

## Findings

### 1. model_verbosity config key

`codex-rs/protocol/src/config_types.rs` line 74:

```rust
pub enum Verbosity {
    Low,
    #[default]
    Medium,
    High,
}
```

Set via `model_verbosity` in `config.toml` (`codex-rs/config/src/config_toml.rs:352`). Passed through to the Responses API as `text.verbosity` (`codex-rs/codex-api/src/common.rs:361-379`). Only effective when `model_info.support_verbosity` is true (`codex-rs/core/src/client.rs:906-916`).

This controls overall output verbosity at the API level. It does not target commentary specifically; it affects all model output (commentary and final alike).

### 2. Personality settings do not affect commentary

`codex-rs/core/src/context/personality_spec_instructions.rs` injects a developer-role message describing communication style ("The user has requested a new communication style..."). The three personality variants (default, friendly, pragmatic) are substituted into the base context template. None reference commentary frequency or emission.

### 3. No phase filtering in history replay

`codex-rs/core/src/context_manager/history.rs`: `for_prompt()` (line 200) calls `for_prompt_annotated()` which calls `normalize_history()` and returns all items. `grep` for `phase`, `Commentary`, and `FinalAnswer` in this file returns zero matches. There is no code path that filters, drops, or truncates commentary items from history before sending to the model.

### 4. No commentary-specific config keys

Searched all `.rs` files under `codex-rs/core/src/config/`, `codex-rs/config/src/`, and `codex-rs/cli/src/` for "commentary". No config key, CLI flag, or setting controls commentary emission, frequency, or retention.

### 5. Server catalog fields

`codex-rs/protocol/src/openai_models.rs` line 423-424: the server catalog's `ModelMessages` struct has `support_verbosity: bool` and `default_verbosity: Option<Verbosity>`. No commentary-specific fields exist in the model catalog structure.

## Summary

The only output-control lever is `model_verbosity`, which is a blunt instrument affecting all model output via the API's `text.verbosity` parameter. Commentary emission is controlled entirely by the base context instructions (which mandate 60-second updates) and the model's compliance with them. The harness has no mechanism to filter commentary from history replay -- all assistant messages pass `is_api_message` identically regardless of phase.

Method: code reads at tag `rust-v0.149.1`.
