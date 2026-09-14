# Third open-weight council harness — bounded comparison, 2026-09-14

## Decision criterion

This compares harness control surfaces, not model popularity: independently
configured subagents; per-agent prompt/tools/permissions; noninteractive
remote control and observable events; model/provider/reasoning pinning;
transcript provenance; and a declarative Nix seam. No candidate was installed,
configured, built, or invoked for this audit.

## Kimi K3 constraint before choosing a harness

K3 is an open-weight 2.8T MoE with a one-million-token context window.
[Moonshot K3 README](https://github.com/MoonshotAI/Kimi-K3) The upstream model
card requires every assistant turn to be replayed intact, including
`reasoning_content` and `tool_calls`; dropping either makes a multi-turn/tool
adapter unsafe. [K3 model-card commit](https://huggingface.co/moonshotai/Kimi-K3/commit/c5d1dd4c428bd1ce8b88c5044f3b6ccde9e3b721)
vLLM's current K3 recipe uses distinct K3 reasoning and tool-call parsers and
lists 8×B300 as its minimum published local recipe. [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/moonshotai/Kimi-K3.yaml)
Cloud evaluation is consequently the realistic first seam; no local K3 serving
claim is made here. K3 uses a custom license rather than MIT/Apache; record its terms when selecting a deployment, without treating a source review as legal clearance.

## Candidates

| Surface | Independent subagents and policy | Remote/headless and provenance | K3 round-trip status | Nix seam | Assessment |
|---|---|---|---|---|---|
| **OpenCode** | First-class `subagent` agents have per-agent model, prompt, and wildcard tool/MCP permissions. [agents](https://dev.opencode.ai/docs/agents/) | `opencode serve` publishes OpenAPI and SSE events; CLI also offers ACP over ND-JSON. [server](https://dev.opencode.ai/docs/server/) [CLI](https://dev.opencode.ai/docs/cli/) | Provider/model IDs and provider options are configurable, including reasoning effort. [models](https://dev.opencode.ai/docs/models/) Moonshot's current OpenCode guide documents K3 with `max`/`high`/`low` effort on OpenCode 1.18.3. [Kimi OpenCode guide](https://platform.kimi.ai/docs/guide/open-code) It does **not** prove that its adapter preserves K3 `reasoning_content` plus `tool_calls` verbatim. Treat that as a required fixture gate. | Existing Home explicitly excludes `opencode` from its launch-orchestration check, despite an agent-intercom OpenCode source pin. [ai-agent-launch-orchestration/default.nix](/git/github.com/LiGoldragon/CriomOS-home/checks/ai-agent-launch-orchestration/default.nix:64) | **Best control-plane candidate** if K3 round-trip is proven first. |
| **Kimi Code CLI** | Built-in `Agent` and `AgentSwarm`, custom Markdown agents with frontmatter tool access, selectable subagent model pool, background/resume, and configurable timeout. [agents](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/agents) [tools](https://www.kimi.com/code/docs/en/kimi-code-cli/reference/tools.html) | ACP is JSON-RPC stdio; its local server provides REST/WebSocket. [command](https://www.kimi.com/code/docs/en/kimi-code-cli/reference/kimi-command) Permissions are ordered allow/deny/ask rules. [config](https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/config-files) | Native Kimi path is most likely to understand K3's special turn shape, but that is an inference, not a verified round-trip witness. Config pins provider/model alias, effort, and supported efforts. [config](https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/config-files) | No existing Kimi package/module was found in the targeted Home sources. This pass did not establish the implementation-language/dependency boundary; verify it against the no-Python orchestration requirement before adoption. | Strongest native K3 fallback; packaging and exact transcript/export behavior remain unproven. |
| **Pi + pi-subagents** | Subagents are an extension/package rather than a core permission system. Extensions execute with full system permissions; permissions must be enforced by the surrounding extension/policy. [extensions](https://github.com/fivewillow/badlogic-pi-mono/blob/main/packages/coding-agent/docs/extensions.md) | JSON/RPC and JSON modes exist; sessions are JSONL trees. [session](https://github.com/fivewillow/badlogic-pi-mono/blob/main/packages/coding-agent/docs/session.md) The sample subagent extension spawns isolated `pi` processes in JSON mode. [example](https://github.com/fivewillow/badlogic-pi-mono/blob/main/packages/coding-agent/examples/extensions/subagent/index.ts) | No primary-source evidence here that Pi's OpenAI adapter preserves full K3 assistant `reasoning_content` and `tool_calls`. Required fixture gate. | Already packaged and pinned: Home installs a local `pi-subagents` package and Nix config. [pi-subagents/default.nix](/git/github.com/LiGoldragon/CriomOS-home/packages/pi-subagents/default.nix:1) [pi-models.nix](/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/pi-models.nix:122) | Lowest adoption cost, but weaker native permission boundary and the living previously called Pi "sloppy" in a recorded harness discussion; do not select on packaging alone. |

## Recommendation

Choose **OpenCode as the third-stack harness only after a hermetic K3
conversation fixture passes**: send a K3 assistant response containing both
reasoning and tool calls, feed it through the intended OpenCode provider path,
then assert the next request contains the complete assistant message unchanged.
OpenCode has the clearest independently configurable agents, explicit tool/MCP
permissions, model/reasoning settings, and a documented headless OpenAPI/SSE
control plane.

Keep **Kimi Code CLI** as the comparison baseline for that fixture. It has a
more complete native subagent surface and explicit K3-oriented model control,
but is not presently packaged here and its durable transcript/provenance
contract has not been inspected. **Pi** remains an already-Nix-packaged
fallback, not the recommended council stack, because its subagent and
permission guarantees are extension-defined and its K3 adapter fidelity is
unproven.

## Required admission probes

1. K3 complete-assistant replay: `reasoning_content`, `tool_calls`, tool result,
   and next assistant turn; inspect captured wire JSON, not rendered text.
2. Two differently configured subagents: distinct model/effort, tool allowlist,
   permission denial, isolated transcript IDs, and parent receipt/event.
3. Headless restart/resume: capture event stream, resume one child, and prove
   provenance links without exposing provider credentials.
4. A pinned Nix derivation plus an offline fixture; no provider login, service,
   or automatic loop belongs in the packaging proof.
   Use harness-owned search/fetch or knowledge lookup in the probe; K3's
   built-in web-search surface is documented as being updated and unsuitable as
   a production dependency in its quick-start guidance.

## Local evidence and limits

Existing Home has Pi and `pi-subagents` packaging, and an OpenCode intercom
source pin, but its current launch check excludes OpenCode. This is a packaging
seam, not evidence that either harness is deployable or selected. Earlier
local research records Pi packaging and fork reconciliation, but is historical
context rather than a fresh behavior witness. [research-other-harnesses.md](/home/li/primary/flows/7b4d4c/reports/research-other-harnesses.md:144)

## Sources

- OpenCode primary docs, fetched 2026-09-14: [agents](https://dev.opencode.ai/docs/agents/), [models](https://dev.opencode.ai/docs/models/), [server](https://dev.opencode.ai/docs/server/), [CLI](https://dev.opencode.ai/docs/cli/).
- Kimi primary docs, fetched 2026-09-14: [configuration](https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/config-files), [agents](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/agents), [tools](https://www.kimi.com/code/docs/en/kimi-code-cli/reference/tools), [providers](https://www.kimi.com/code/docs/en/kimi-code-cli/configuration/providers).
- K3/vLLM primary sources, fetched 2026-09-14: [Moonshot K3](https://github.com/MoonshotAI/Kimi-K3), [model-card replay requirement](https://huggingface.co/moonshotai/Kimi-K3/commit/c5d1dd4c428bd1ce8b88c5044f3b6ccde9e3b721), [vLLM recipe](https://github.com/vllm-project/recipes/blob/main/models/moonshotai/Kimi-K3.yaml).
- Pi primary repository documentation and cited local CriomOS-home sources above.
