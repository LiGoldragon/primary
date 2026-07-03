# Local OpenAI-Compatible Provider Evidence

## Task And Scope

Implementation worker for the approved lane wiring Spirit and Mind agent-backed LLM calls to use a local OpenAI-compatible subscription-backed server as an alternative to DeepSeek. Scope covered the provider contract, the `agent` provider runtime, Mind accepted-knowledge judge configuration/harness, and Spirit guardian configuration. DeepSeek paths were preserved.

Relevant intent query: Spirit `PublicTextSearch [deterministic routing configuration agent judgment]` returned record `w312`; conclusion used here was that provider routing/configuration is deterministic mechanism, not agent judgment.

## Confirmed Plan From Code Inspection

- `agent` is the shared OpenAI-compatible provider caller. It already supports configurable endpoint/base URL through `ProviderEntry.endpoint`; the live provider posts to `{endpoint}/chat/completions`.
- Mind does not call DeepSeek directly. `AgentKnowledgeJudge` sends `signal-agent::Input::Call` to an `agent` socket, with provider/model in `PromptOptions`. The previous helper was `MindKnowledgeJudgeAgentConfiguration::deepseek_flash`.
- Spirit does not call DeepSeek directly. `AgentGuardian` sends `signal-agent::Input::Call` to an `agent` socket, with provider/model in `PromptOptions`.
- The missing runtime capability was a typed no-auth provider seed. Before this change, every configured provider required an API-key secret source and the live provider always sent `Authorization: Bearer ...`.
- The local server auth file `~/.codex/auth.json` is not read by this code. It remains owned by the local server process.

## Changed Repos And Commits

- `meta-signal-agent` commit `1f615eba`: added `SecretSource::NoSecret` to the meta contract, bumped crate/schema version to `0.2.1`, regenerated `src/schema/lib.rs`, and documented the local-provider shape.
- `agent` commit `9bf9d57c`: added `ProviderAuthorization::{Bearer, None}`, mapped `NoSecret` to no Authorization header, kept Environment/Gopass/File bearer behavior, added local mock HTTP request-shape tests, and updated docs.
- `mind` commit `e781e106`: added local judge constants/helper (`local-openai`, `gpt-5.5`, `http://127.0.0.1:18080/v1`), added `--local-openai-compatible` live-eval profile, defaulted that profile to `NoSecret`, and omitted DeepSeek-specific reasoning extensions for that provider name.
- `spirit` commit `d20982c4`: added local guardian constants/helper, omitted DeepSeek-specific reasoning extensions for that provider name, and documented/config-tested the local provider shape.

## Validation

- `meta-signal-agent`: `cargo test` passed, 5 tests.
- `agent`: `cargo test --features live-provider` passed, including local mock tests for no Authorization header and configured bearer header. Existing gated DeepSeek live test also ran because the gopass key was available. No local `gpt-5.5` eval was run.
- `mind`: `cargo test local_openai_compatible --test cli` passed, 2 tests. `cargo test --bin mind-live-knowledge-judge-eval` passed, 6 tests.
- `spirit`: `cargo test --features agent-guardian configuration_writer_accepts_local_openai_compatible_guardian --test process_boundary` passed, 1 test.

## Config Shapes

Start or configure `agent-daemon` with the local provider and no local API-key gate:

```text
(AgentConfigurationWriteRequest (<agent.sock> <agent.meta.sock> 384 <agent.redb> [(ProviderSeed (local-openai http://127.0.0.1:18080/v1 gpt-5.5 NoSecret))] <agent.rkyv>))
```

If the local server is started with an API-key gate, replace `NoSecret` with one of:

```text
(Environment LOCAL_OPENAI_API_KEY)
(File /absolute/path/to/local-openai-api-key)
```

Mind daemon configuration:

```text
(ConfigurationWriteRequest <mind.sock> <mind.meta.sock> <mind.redb> <mind.rkyv> (AgentKnowledgeJudge <agent.sock> local-openai gpt-5.5 180000 2048))
```

Mind live judge harness local profile:

```sh
target/debug/mind-live-knowledge-judge-eval --local-openai-compatible
```

Equivalent explicit harness shape:

```sh
target/debug/mind-live-knowledge-judge-eval \
  --provider local-openai \
  --model gpt-5.5 \
  --endpoint http://127.0.0.1:18080/v1 \
  --secret-source NoSecret \
  --no-check-secret-source
```

Spirit daemon configuration:

```text
(ConfigurationWriteRequest (<spirit.sock> (Some <spirit.meta.sock>) <spirit.sema> None Gating (Some (<agent.sock> (Some [local-openai]) (Some [gpt-5.5]) 180000 None)) <spirit.rkyv>))
```

## Live Eval Follow-Up

Live `gpt-5.5` evaluation remains blocked on the orchestrator starting or verifying the local `openai-api-server-via-codex` at `http://127.0.0.1:18080/v1`. The code intentionally does not read `~/.codex/auth.json`; that file is consumed only by the local server.
