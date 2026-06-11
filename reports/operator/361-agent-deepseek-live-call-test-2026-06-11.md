# Agent DeepSeek Live Call Test

## Scope

Implemented and tested real DeepSeek provider calls for the `agent` component without using the most powerful model.

The selected model is `deepseek-v4-flash`.

## Landed Commits

- `signal-agent` main: `b91254b9d43e` — `signal-agent: use DeepSeek flash model in examples`
- `meta-signal-agent` main: `c1165460b7ed` — `meta-signal-agent: use DeepSeek flash model in examples`
- `agent` main: `b554a1bb2e95` — `agent: test live DeepSeek flash calls`

All three were pushed; local `main` and `main@origin` match.

## Changes

- Updated signal-agent and meta-signal-agent tests/examples from `deepseek-chat` to `deepseek-v4-flash`.
- Removed unnecessary brackets around bracket-free-eligible model/provider/key strings in canonical NOTA examples.
- Added an agent live-provider test that:
  - configures the DeepSeek OpenAI-compatible endpoint,
  - resolves the API key through `DEEPSEEK_API_KEY`,
  - calls `deepseek-v4-flash`,
  - requests `OutputMode::Nota`,
  - validates the returned completion parses as NOTA.
- Kept the live test CI-safe: it skips unless `DEEPSEEK_API_KEY` is present.
- Refreshed `agent/Cargo.lock` to current `signal-agent`, `meta-signal-agent`, `schema-next`, and `schema-rust-next` main commits.
- Cleaned one agent clippy blocker by making the Nexus `execute` impl use async-fn syntax and moving the origin-route helper onto `AgentEngine`.

## Verification

- `signal-agent`: `cargo test`
- `signal-agent`: `cargo clippy -- -D warnings`
- `meta-signal-agent`: `cargo test`
- `meta-signal-agent`: `cargo clippy -- -D warnings`
- `agent`: `cargo test`
- `agent`: `cargo clippy --features live-provider -- -D warnings`
- `agent`: live DeepSeek test with the key sourced from gopass:
  - `DEEPSEEK_API_KEY="$(gopass show -o platform.deepseek.com/api-key)" cargo test --features live-provider live_deepseek_flash_returns_valid_nota_when_key_present -- --nocapture`

The real DeepSeek call passed twice: once before the lock refresh and once after the lock refresh.

## Notes

No secret value was printed or persisted. The key only entered the environment of the cargo test process.

This verifies the real provider path inside `agent`: typed Signal prompt, registry resolution, environment key lookup, reqwest OpenAI-compatible call, completion handling, and NOTA parse validation.
