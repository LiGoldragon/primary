# Pi local Gemma/API-key situation and agent update handoff

## Why this report exists

The local Pi session was asked to use the Prometheus-hosted local LLM models, including the new Gemma 4 models. A test with `qwen3.5-27b` failed with `401 Invalid API Key`. The user then asked whether the local profile is configured for Gemma 4, asked to update Pi/Claude/Codex if updates exist, and asked whether the local LLM API key can be installed through the standard Pi/Home profile path without exposing plaintext.

## Current observed state

Prometheus side:

- Prometheus successfully booted generation 45.
- Generation 45 includes the local LLM model inventory with `gemma-4-31b` and `gemma-4-26b-a4b` in the llama router models directory/presets.
- The router is enforcing the local LLM API token; the local Pi request that sent a dummy key got `401 Invalid API Key`.
- Generation 46 is staged as BootOnce for the backup SSID rename to `criome-backup`; that is separate from the Pi auth problem.

Local Pi/Home side:

- Active `~/.pi/agent/models.json` does **not** show the Gemma 4 models in the local provider entries I inspected. It still lists the older Qwen/GPT-OSS/Nemotron/GLM set.
- Active Pi config has multiple local-style provider names from prior iterations: `prometheus`, `criomos-largeai`, and `criomos-local`.
- `CriomOS-home/modules/home/profiles/min/pi-models.nix` currently declares provider `criomos-local`, reads models from `inputs.criomos-lib + /data/largeAI/llm.json`, and uses a dummy provider `apiKey = "sk-no-key-required"`.
- The real token already exists in gopass at `goldragon.criome/local-llm-api-token`.

## Pi authentication mechanism

Pi's standard auth file is `~/.pi/agent/auth.json`. For a provider ID, it accepts:

- literal API key strings,
- environment variable names,
- shell-command values prefixed by `!`.

Pi's auth lookup order is runtime override, `auth.json`, OAuth token in `auth.json`, environment variable, then provider fallback from `models.json`. For this use case, the safest standard shape is command-backed `auth.json`, not a plaintext key in Nix or in `models.json`.

Recommended managed entry shape:

```json
{
  "criomos-local": {
    "type": "api_key",
    "key": "!gopass show -o goldragon.criome/local-llm-api-token"
  }
}
```

Because the active local file still has legacy provider names, either prune them during the model config cleanup or add equivalent auth entries for `prometheus` and `criomos-largeai` during transition so old UI selections stop failing.

## Update findings

Updates found before this report was requested:

- Pi upstream tags: current profile is `v0.76.0`; latest tag found is `v0.77.0`.
- Claude Code VSIX: current flake URL is `2.1.153`; Open VSX reports `2.1.156`.
- Codex CLI nix input: current `codex-cli` locked rev differs from upstream `main`; update is available.
- `llm-agents.nix` input for Claude Code also differs from upstream `main`; update is available.
- `CriomOS-lib` likely needs a lock bump in CriomOS-home so Home's Pi model inventory includes the Gemma 4 entries already visible in the checked-out `CriomOS-lib/data/largeAI/llm.json`.

## Recommended implementation plan

1. In `CriomOS-home`, update inputs for `pi-src`, `claude-code-vsix`, `codex-cli`, `llm-agents`, and `criomos-lib`.
2. Extend `pi-models.nix` to manage `~/.pi/agent/auth.json` with a command-backed gopass key for `criomos-local`; include transitional entries for legacy local provider IDs or prune those providers.
3. Ensure local provider config does not send `sk-no-key-required` once Prometheus requires auth.
4. Run `nix flake check` from pushed origin with `--refresh`.
5. Push `CriomOS-home` and activate with `lojix-cli (HomeOnly goldragon ouranos li ... Activate ...)`.
6. Verify locally without exposing the token:
   - `~/.pi/agent/models.json` contains `gemma-4-31b` and `gemma-4-26b-a4b`.
   - `~/.pi/agent/auth.json` contains command-backed entries, not literal token bytes.
   - `pi --list-models` shows the Gemma models under the intended local provider.
   - A local model call succeeds against Prometheus.

## Main design choice

The open design choice for cloud-designer: should the durable local provider name be `criomos-local`, `prometheus`, or a clearer name such as `criomos-largeai`? The implementation should collapse to one canonical provider ID so users do not accidentally select a stale provider that still points at dummy auth.
