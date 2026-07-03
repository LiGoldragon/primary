# Provider Interaction Logging Evidence

## Task And Scope

Implemented disabled-by-default full provider interaction logging for the
`agent` component in `/git/github.com/LiGoldragon/agent`.

Scope constraints followed:

- logging is disabled by default;
- enabled logs are written outside the agent database;
- provider authorization values, bearer tokens, API keys, secret values, and
  obvious credential-bearing metadata are redacted;
- no `~/.codex/auth.json` path or contents are read or logged;
- DeepSeek and local OpenAI-compatible no-Authorization behavior are preserved;
- Mind/Spirit prompts were not changed.

## Files Consulted

- `/home/li/primary/AGENTS.md`
- `/git/github.com/LiGoldragon/agent/AGENTS.md`
- `/git/github.com/LiGoldragon/agent/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/agent/README.md`
- `/git/github.com/LiGoldragon/agent/src/config.rs`
- `/git/github.com/LiGoldragon/agent/src/engine.rs`
- `/git/github.com/LiGoldragon/agent/src/provider.rs`
- `/git/github.com/LiGoldragon/agent/src/registry.rs`
- `/git/github.com/LiGoldragon/agent/src/bin/agent_write_configuration.rs`
- `/git/github.com/LiGoldragon/agent/tests/configuration_writer.rs`
- `/git/github.com/LiGoldragon/agent/tests/fixture_round_trip.rs`

Spirit query class used: `PublicTextSearch [agent provider interaction logging secrets]`.
Relevant conclusion: public intent records supported high-quality agent failure
diagnostics but did not add a more specific logging policy than the approved
brief.

## Changes

Committed and pushed in `agent`:

- commit: `14fae75c4722` (`agent: add disabled provider interaction logging (Codex GPT-5)`)
- bookmark: `main`
- push verification: `jj git push --bookmark main` reported `main@origin` already matches `main`.

Changed files:

- `Cargo.toml`, `Cargo.lock`: bumped crate version to `0.2.1`; made
  `serde`/`serde_json` normal dependencies because JSONL logging is available
  without `live-provider`.
- `src/config.rs`: added `ProviderInteractionLogging::{Disabled, JsonLines}` to
  binary daemon configuration. Existing `AgentDaemonConfiguration::new(...)`
  defaults to `Disabled`; new `new_with_provider_interaction_logging(...)`
  accepts an explicit setting.
- `src/bin/agent_write_configuration.rs`: preserved old
  `(AgentConfigurationWriteRequest ...)` as disabled; added
  `(AgentConfigurationWriteRequestWithProviderInteractionLogging (... (JsonLines <log-path>) ...))`.
- `src/interaction_log.rs`: new JSONL side logger, redaction, structured
  provider interaction record model, and database-path equality rejection.
- `src/engine.rs`: logs every provider attempt when enabled, including success,
  provider failure, and NOTA validation failures/retries.
- `src/provider.rs`: centralizes OpenAI-compatible request body projection and
  carries raw response status/body back from the live provider so malformed
  provider responses can be logged.
- `src/registry.rs`: includes provider name in resolved `ProviderCall`.
- `src/schema_daemon.rs`: builds the engine with the configured interaction log.
- `README.md`, `ARCHITECTURE.md`: document the setting, JSONL location, and
  redaction behavior.
- `tests/configuration_writer.rs`, `tests/fixture_round_trip.rs`: added targeted
  disabled/default, enabled success, invalid NOTA, malformed response, and
  config-writer tests.

## Setting And CLI Shape

Binary configuration:

```text
ProviderInteractionLogging::Disabled
ProviderInteractionLogging::JsonLines(ProviderInteractionLogPath)
```

Default:

```text
AgentDaemonConfiguration::new(...) -> ProviderInteractionLogging::Disabled
```

Configuration writer:

```text
(AgentConfigurationWriteRequest (<ordinary-socket> <meta-socket> <meta-mode> <database-path> <provider-seeds> <output-rkyv>))
```

This legacy shape remains valid and disables interaction logging.

Enabled shape:

```text
(AgentConfigurationWriteRequestWithProviderInteractionLogging (<ordinary-socket> <meta-socket> <meta-mode> <database-path> <provider-seeds> (JsonLines <log-path>) <output-rkyv>))
```

`<log-path>` is a JSONL file path. Runtime rejects a log path equal to the
configured database path.

## Log Format And Location

Location:

- disabled: no log path is held and no interaction log is written;
- enabled: append-only JSONL at the configured `JsonLines <log-path>`;
- parent directories are created when the first record is written;
- the log file is separate from the agent database path.

One JSON object is appended per provider attempt. Top-level fields:

- `timestamp_unix_millis`
- `provider`: provider name, endpoint, model, authorization label (`bearer` or
  `none`)
- `request`: chat-completions URL, redacted headers, OpenAI-compatible request
  body including system/messages/options
- `response`: status/body when available
- `provider_result`: completed text/tokens or provider failure kind/detail
- `validation`: `NotRequired`, `ValidNota`, `InvalidNota`, or `NotReached`
- `daemon_outcome`: completed or rejected reason/detail

Redaction:

- bearer token values are never logged;
- Authorization header is logged only as `<redacted>`;
- `NoSecret` emits no Authorization header in the log;
- URL query parameters and JSON object fields with obvious credential-bearing
  names are redacted;
- configured secret source values are not part of provider interaction records.

## Checks Run

- `cargo fmt` - passed.
- `cargo test` - passed: 14 tests total across configuration writer and fixture
  round-trip suites.
- `cargo test --features live-provider local_openai_compatible_provider` -
  passed: local OpenAI-compatible route omits Authorization for `NoSecret` and
  sends configured bearer auth when present.
- `nix build .#checks.x86_64-linux.test` - passed after tracking the new module;
  this check runs the flake test surface with `live-provider`.

Initial Nix attempt failed because `src/interaction_log.rs` was untracked and
therefore absent from `cleanSource`; after `jj file track src/interaction_log.rs`
the Nix check passed.

## Residual Risks And Follow-Up

- Existing binary configuration archives created before `0.2.1` do not contain
  the new rkyv field and should be regenerated with `agent-write-configuration`.
- JSONL can be large when enabled because it intentionally captures full
  prompts and provider response bodies. Rotation/retention policy is not part
  of this change.
- The logger redacts explicit credential metadata and provider auth values, but
  it intentionally does not redact arbitrary prompt/message content.
