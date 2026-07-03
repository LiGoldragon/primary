# Rust Auditor Review

## Task And Scope

Audited the just-landed provider interaction logging implementation in
`/git/github.com/LiGoldragon/agent`, commit `14fae75c4722`
(`agent: add disabled provider interaction logging (Codex GPT-5)`).

Scope checked against the brief:

- disabled-by-default configuration and CLI writer shape;
- JSONL log location separate from the agent database;
- request/response/status/body/validation/error logging behavior;
- redaction of auth headers, resolved API key values, secret-source values, and
  credential-bearing metadata;
- no `~/.codex/auth.json` read/log path;
- DeepSeek and local OpenAI-compatible behavior;
- targeted tests for default-off, enabled success, invalid NOTA, and malformed
  provider response behavior.

Spirit query class used: `PublicTextSearch [agent provider interaction logging rust audit]`.
Relevant conclusion: no logging-specific intent was found; broad public records
supported high-quality agent diagnostics and careful mechanism boundaries.

## Findings

### High: resolved bearer values can leak through provider response/error text

Files:

- `/git/github.com/LiGoldragon/agent/src/interaction_log.rs:293`
- `/git/github.com/LiGoldragon/agent/src/interaction_log.rs:300`
- `/git/github.com/LiGoldragon/agent/src/interaction_log.rs:320`
- `/git/github.com/LiGoldragon/agent/src/interaction_log.rs:340`
- `/git/github.com/LiGoldragon/agent/src/interaction_log.rs:457`
- `/git/github.com/LiGoldragon/agent/src/interaction_log.rs:464`
- `/git/github.com/LiGoldragon/agent/src/provider.rs:494`
- `/git/github.com/LiGoldragon/agent/src/provider.rs:500`

Risk:

The implementation redacts the outbound Authorization header, but it does not
redact the actual resolved bearer/API-key value from every logged string. For a
provider rejection or malformed response, `ProviderFailure::ProviderRejected`
carries both `detail` and `response_body`. The live provider builds `detail`
from `status {status}: {response_body}` for non-2xx responses and from the JSON
parse error for malformed 2xx responses. The logger then records failure detail
through `SecretRedactor::metadata(detail)` and response body through
`SecretRedactor::body_text(response_body)`.

`SecretRedactor::body_text` redacts JSON object fields only when the field name
looks credential-bearing, and returns non-JSON bodies unchanged. It does not
replace the known bearer value held by `ProviderCall.authorization()` in the
detail/body text. Common provider error payloads can echo the supplied key in a
message field or in a non-JSON body, for example `Incorrect API key sk-...`.
That would be logged in `response.body`, `provider_result.detail`, or
`daemon_outcome.detail`.

This violates the brief requirement that local API key values are redacted, not
just auth headers. It is also not covered by the current tests: the success test
asserts `test-key` is absent only on a fixture success path with no response
body containing the key.

Expected correction:

Make redaction value-aware for the current interaction. Build a redactor from
the `ProviderCall` that knows the resolved bearer value when present, and apply
it to all logged strings: response body, provider failure detail, daemon
rejection detail, URL/header/body projections, and any parsed JSON string
values. Add a test where a provider rejection or malformed response includes
the literal resolved key in JSON and non-JSON text, and assert the JSONL file
does not contain it.

### Medium: log/database separation can be bypassed by path aliases or symlinks

Files:

- `/git/github.com/LiGoldragon/agent/src/interaction_log.rs:47`
- `/git/github.com/LiGoldragon/agent/src/interaction_log.rs:48`
- `/git/github.com/LiGoldragon/agent/src/interaction_log.rs:78`

Risk:

`ProviderInteractionLog::from_configuration` rejects only raw `PathBuf`
equality between the configured log path and database path. It does not
canonicalize existing paths, normalize lexical aliases, or reject a log path
that is a symlink to the database. The writer later opens the configured log
path with append/create, so an alias or symlink can append JSONL into the agent
database file.

That fails the storage-safety part of the brief: logs must be outside the agent
main database. The current test suite checks writer acceptance of a separate
path, but does not check equal-path rejection or alias/symlink rejection.

Expected correction:

At runtime, reject canonical equivalence when both paths exist; reject a log
path whose final component is a symlink; and normalize or absolutize paths
before equality checks where files do not yet exist. Add tests for exact equal
path, relative alias to the same path, and symlink-to-database rejection.

## Residual Risks And Test Gaps

- Provider-resolution failures before a `ProviderCall` exists are not logged:
  `NoProviderConfigured`, unknown provider, and secret-source resolution errors
  return directly from `AgentEngine::run_provider_effect` without a log record
  (`src/engine.rs:181`). This may be acceptable if "provider interaction" means
  a resolved outbound attempt, but it is a scope edge for diagnostics.
- The malformed-response logging test uses a custom `RejectedProvider` that
  constructs `ProviderFailure::provider_rejected_with_response` directly. It
  exercises engine logging but not the live `OpenAiCompatibleProvider` parse
  path at `src/provider.rs:500`. Add a local HTTP test returning malformed JSON
  through `OpenAiCompatibleProvider` if the orchestrator wants a stronger
  malformed-response witness.
- The URL/query redactor is hand-rolled with `split_once('?')` and `split('&')`
  (`src/interaction_log.rs:440`). That is weaker than a real URL parser for a
  credential boundary, especially with encoded keys.

## Checked Evidence

Files and surfaces consulted:

- `/home/li/primary/AGENTS.md`
- `/home/li/primary/ARCHITECTURE.md`
- `/home/li/primary/agent-outputs/ProviderInteractionLogging/GeneralCodeImplementer-Evidence.md`
- `/git/github.com/LiGoldragon/agent/AGENTS.md`
- `/git/github.com/LiGoldragon/agent/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/agent/Cargo.toml`
- `/git/github.com/LiGoldragon/agent/src/config.rs`
- `/git/github.com/LiGoldragon/agent/src/interaction_log.rs`
- `/git/github.com/LiGoldragon/agent/src/engine.rs`
- `/git/github.com/LiGoldragon/agent/src/provider.rs`
- `/git/github.com/LiGoldragon/agent/src/registry.rs`
- `/git/github.com/LiGoldragon/agent/src/schema_daemon.rs`
- `/git/github.com/LiGoldragon/agent/src/bin/agent_write_configuration.rs`
- `/git/github.com/LiGoldragon/agent/tests/configuration_writer.rs`
- `/git/github.com/LiGoldragon/agent/tests/fixture_round_trip.rs`

Observed facts:

- Commit `14fae75c4722` is present on `main`, `main@git`, and `main@origin`.
- The agent worktree was clean before audit commands.
- `AgentDaemonConfiguration::new(...)` defaults
  `provider_interaction_logging` to `Disabled` (`src/config.rs:111`).
- The legacy writer shape maps to disabled logging
  (`src/bin/agent_write_configuration.rs:174`).
- The enabled writer shape accepts `(JsonLines <log-path>)`
  (`src/bin/agent_write_configuration.rs:70` and `:239`).
- Runtime builds the log from binary configuration and rejects only raw equality
  with `configuration.database_path()` (`src/schema_daemon.rs:81`,
  `src/interaction_log.rs:47`).
- `rg -n "auth\\.json|codex/auth|\\.codex" /git/github.com/LiGoldragon/agent`
  found no matches.

Commands run:

- `jj status` in `/git/github.com/LiGoldragon/agent`: clean working copy; parent
  commit is `14fae75c`.
- `jj show --stat -r 14fae75c4722`: showed 15 changed files, 1146 insertions,
  122 deletions.
- `cargo fmt --check`: passed.
- `cargo test`: passed; 14 tests total.
- `cargo test provider_interaction_logging_records`: passed; 3 targeted
  logging tests.
- `cargo test --features live-provider local_openai_compatible_provider`:
  passed; 2 local OpenAI-compatible tests covering `NoSecret` and bearer auth.
- `cargo test --features live-provider provider_interaction_logging_records`:
  passed; same 3 targeted logging tests under `live-provider`.

Command issues:

- `cargo test --features live-provider <three separate test names>` failed
  because Cargo accepts one test filter. Re-run with the common
  `provider_interaction_logging_records` filter passed.
- `jj show --stat --no-patch -r 14fae75c4722` failed because `jj show` does not
  allow `--no-patch` with `--stat`. Re-run as `jj show --stat -r ...` passed.
