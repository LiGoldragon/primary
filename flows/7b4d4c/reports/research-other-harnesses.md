# Research: Other Harnesses

Flow 7b4d4c. Thread 4. 2026-09-04.

---

## 1. The DeepSeek Harness

### Identification

The living most plausibly means **DeepSeek Harness (dsh)**, the official
agent runtime from DeepSeek, open-sourced 2026-08-13 alongside DeepSeek
V4-Pro.  [documented: https://github.com/deepseek-ai/deepseek-harness,
2026-09-04]

No widely discussed third-party DeepSeek-specific harness predates it.
A nixpkgs package named `whale` ("Terminal-first AI coding agent for
DeepSeek") exists but is a different, smaller project.  [witnessed: `nix
search nixpkgs deepseek`, 2026-09-04]

### Facts

| Attribute | Value | Evidence |
|---|---|---|
| Repository | `deepseek-ai/deepseek-harness` | documented: GitHub, 2026-09-04 |
| License | MIT | documented: GitHub, 2026-09-04 |
| Language | TypeScript (pnpm monorepo) | documented: GitHub README, 2026-09-04 |
| Install | `npx @deepseek-ai/dsh web` or clone+pnpm | documented: GitHub README, 2026-09-04 |
| Node requirement | >=22.19 or >=24 | documented: GitHub README, 2026-09-04 |
| In nixpkgs | No (`nix search nixpkgs deepseek` returns only python bindings, llm plugin, and `whale`) | witnessed: 2026-09-04 |
| Stars | ~203k in two weeks | documented: multiple sources, Aug 2026 |
| npm version | 0.1.1-rc.2 (latest+next); 0.1.2-alpha.1 (GitHub pre-release only) | documented: multiple sources, Aug 2026 |
| Built on | Cordis (dependency-injection framework) | documented: GitHub README, 2026-09-04 |

### Architecture: "Everything Is a Plugin"

The tagline is literal.  Plugins provide models, tools, skills,
sessions, sandboxes, storage, loops, scheduling, and the UI.  The agent
loop itself is a plugin.  [documented: deepseek.com/harness/en/,
2026-09-04]

A **profile** is the plugin composition for one session: a directory
containing a `package.json` with the ordered bundle list and a
`cordis.patch.yml` for profile-specific config.  [documented:
deepseek-harness docs, 2026-09-04]

### Context Composition

**System prompt assembly** is a two-stage pipeline in
`packages/core/system-prompt`:

1. `assemble()` returns sections with resolved but uninterpolated text,
   ordered tool schemas, and resolved variables.
2. `renderPrompt()` interpolates `{{variable}}` references, eliminates
   empty sections, concatenates.

Config keys:

- `includeHarnessIdentity` (default true) -- the fixed opener
  "You are an AI agent powered by DeepSeek Harness" at order -1000.
- `includeRuntimeContext` (default true) -- dynamic runtime context.
- `persona` (default empty) -- deployment persona fragment at order 0.
- `toolOrder` -- explicit model-facing tool presentation order.

[documented: deepseek-harness/packages/core/system-prompt/README.md,
GitHub, 2026-09-04]

If any section declares itself "complete," that section becomes the
entire system prompt; the waterfall's contexts, tools, and variables
remain.  [documented: same README]

**Agent instructions** (`packages/context/agent-instructions`) load:

1. `$DSH_HOME/AGENTS.md` (user-global)
2. From project root to cwd: `AGENTS.md`, `CLAUDE.md` (base candidates)
3. Then `AGENTS.local.md`, `CLAUDE.local.md` (local overlays)

Duplicate detection suppresses repetition (content-identical files after
trim render once).  Instructions are delivered as user-role messages
wrapped in `<system-reminder>`.  Budget enforcement drops whole broader
files before truncating the most-specific file.  [documented:
deepseek-harness/packages/context/agent-instructions, GitHub,
2026-09-04]

### Providers and Models

Catalog providers: DeepSeek, Anthropic, OpenAI, Bedrock, Vertex, Azure.
Any OpenAI-compatible endpoint can be added in `$DSH_HOME/settings.yaml`
by supplying provider ID, base URL, API protocol (`openai-completions`,
`openai-responses`, or `anthropic-messages`), key env-var name, and
model list.  [documented:
deepseek-harness/docs/user/guide/providers.md, GitHub, 2026-09-04]

Credentials live in `.credentials.yaml`, not in settings.yaml.

### ChatGPT-Subscription Models via dsh

A community plugin `dsh-openai-codex-oauth` (GitHub:
dyuan311/dsh-openai-codex-oauth) wires ChatGPT subscription OAuth into
the openai-codex provider.  [documented: GitHub, 2026-09-04]  Whether
the ChatGPT subscription quota actually permits sustained dsh usage is
subject to the informal tolerance discussed in section 2.

---

## 2. ChatGPT with Third-Party Harnesses

### Current Policy

OpenAI has **no explicit written policy** permitting or prohibiting
ChatGPT subscription tokens in third-party tools.  The Terms of Use
(https://openai.com/policies/row-terms-of-use/) reserve the right to
terminate access if use "could cause risk or harm."  [documented:
manifest.build/blog/chatgpt-plus-tokens-third-party-harnesses/,
2026-09-04; openai.com/policies/row-terms-of-use/]

### Public Signals of Tolerance

- Sam Altman posted on X endorsing third-party harness use.
  [documented: manifest.build article, 2026]
- OpenAI shipped a "Sign in with ChatGPT" OAuth flow covering
  subscription users.  [documented: same]
- The "Codex for Open Source" program names Codex, OpenCode, Cline, Pi,
  OpenClaw as encouraged tools.  [documented: same]
- A ChatGPT Plus subscription delivers ~$100-200 of API-equivalent
  tokens for $20/month; OpenAI has so far tolerated spending them in
  third-party harnesses.  [documented: same]

### Harnesses Documented as Working

OpenCode, Cline, Pi, OpenClaw, OpenHands, KiloCode, Crush, Aider,
Droid, Hermes, and now dsh via community plugin.  [documented:
manifest.build article, 2026-09-04]

### Contrast with Anthropic

- 2026-02-20: Anthropic updated terms to prohibit subscription OAuth
  tokens in third-party tools.  [documented: manifest.build article]
- 2026-04-04: Billing enforcement activated; subscription tokens used
  outside Claude Code are rejected.  [documented: same]

---

## 3. The Pi Harness

### Identification

Pi is a minimal terminal coding-agent harness created by **Mario
Zechner**, originally at `badlogic/pi-mono` (MIT license).  In April
2026 it was acquired by **Armin Ronacher's** company **Earendil Works**;
the repository moved to the `earendil-works` organization and npm
packages were renamed under `@earendil-works` starting at v0.74.0.
[documented: Wikipedia "Pi (AI agent)"; explainx.ai Pi guide, 2026]

The living's characterization "sloppy" does not appear to refer to the
tool's quality -- "sloppy" is actually the name of Pi's fallback edit
mode for models lacking hashline support.  [documented: search results,
2026-09-04]  The living likely found the harness's behavior rough or its
conventions insufficiently rigorous.  [inferred]

### Current Activity

Pi is **not abandoned**.  It is actively maintained (v0.84.1 as
packaged), gaining adoption (54k to 98k stars in three months), and
Databricks benchmarked it as the highest-pass-rate harness on Opus 4.8.
[documented: multiple sources, 2026]

### Packaging in This Environment

**Pi is still packaged here.**

- `/git/github.com/LiGoldragon/CriomOS-home/packages/pi/default.nix` --
  builds `@earendil-works/pi-coding-agent` v0.84.1 from the
  `earendil-works` monorepo with three local patches.  [witnessed:
  2026-09-04]
- `/git/github.com/LiGoldragon/CriomOS-home/packages/pi-criomos/` --
  a CriomOS-specific Pi package (themes, extensions, skills).
  [witnessed: 2026-09-04]
- `/git/github.com/LiGoldragon/CriomOS-home/packages/pi-subagents/` --
  subagent reconciliation.  [witnessed: 2026-09-04]
- `/git/github.com/LiGoldragon/CriomOS-home/packages/pi-continue/` --
  session resume patches.  [witnessed: 2026-09-04]
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/pi-models.nix` --
  model configuration.  [witnessed: 2026-09-04]
- `/home/li/primary/.pi/` -- generated tree with agents (8 files) and
  continue sessions (22 files).  [witnessed: 2026-09-04]

If the living wants Pi abandoned, the packaging and generated tree need
active removal.

---

## 4. Prompt Vocabulary Across Harnesses and APIs

### API-Level Message Roles

| Concept | Anthropic Messages API | OpenAI Chat Completions | OpenAI Responses API | DeepSeek API |
|---|---|---|---|---|
| Top-level instructions | `system` (top-level param, not in messages array) | `system` role in messages (deprecated for new models) | `instructions` (top-level field) | `system` role in messages (OpenAI-compatible) |
| App-layer instructions | `system` role in messages (mid-conversation, Fable 5.1+ only) | `developer` role (replaces `system` from o1 onward) | `instructions` | Not separately named; uses `system` |
| Human input | `user` role | `user` role | `input` (string or array) | `user` role |
| Machine output | `assistant` role | `assistant` role | `output` (response items) | `assistant` role |
| Tool results | `tool_result` content block (inside `user` turn) | `tool` role | `function_call_output` item | `tool` role (OpenAI-compatible) |
| Tool invocations | `tool_use` content block (inside `assistant` turn) | `assistant` with `tool_calls` | `function_call` item | `assistant` with `tool_calls` |

[documented: platform.claude.com/docs/en/build-with-claude/working-with-messages,
2026-09-04; lunary.ai/blog/openai-developer-role, 2026;
developers.openai.com/api/docs/guides/migrate-to-responses, 2026;
api-docs.deepseek.com/, 2026-09-04]

Anthropic is the only API where `system` is a top-level parameter
outside the messages array.  OpenAI deprecated the `system` role in
favor of `developer` starting with o1 models; for GPT-4o, `developer`
auto-converts to `system`.  DeepSeek tracks the OpenAI Chat Completions
format and also offers an Anthropic-compatible endpoint.  [documented:
sources above]

### Harness-Level Instructions Files

| Concept | Claude Code | Codex CLI | DeepSeek Harness (dsh) | Pi |
|---|---|---|---|---|
| Project instructions file | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` then `CLAUDE.md` (both loaded) | Per-package `skills/` directory |
| Local overlay | Not applicable (uses directory hierarchy) | Not documented | `AGENTS.local.md`, `CLAUDE.local.md` | Not documented |
| User-global instructions | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` | `$DSH_HOME/AGENTS.md` | `~/.pi/settings` |
| System prompt name | "system prompt" (assembled from 110+ fragments) | "system prompt" / "base instructions" | "system prompt" (assembled via waterfall) | "system prompt" (sub-1000 tokens) |
| Config format | JSON (`settings.json`) | TOML (`config.toml`) | YAML (`settings.yaml`, `cordis.patch.yml`) | JSON (`package.json` with `pi` key) |

[documented: code.claude.com/docs/en/agent-sdk/modifying-system-prompts,
2026-09-04; developers.openai.com/codex/cli, 2026-09-04;
deepseek-harness GitHub, 2026-09-04; pi Wikipedia / explainx.ai guide,
2026]

The notable design difference: dsh loads both `AGENTS.md` and
`CLAUDE.md` at every directory level, with content deduplication, making
it the only harness that reads a competitor's instructions file by
default.  [documented: deepseek-harness agent-instructions README,
2026-09-04]

---

## 5. Prior Art on Replaceable System Prompts

### 5a. Piebald-AI/claude-code-system-prompts

Repository documenting all parts of Claude Code's system prompt (515
fragments as of 2026-06-12, updated to v2.1.259 on 2026-09-02), 27
built-in tool descriptions, sub-agent prompts, and utility prompts.
Not a replacement harness but the reference for anyone building one.
Reliability: high -- maintained against each Claude Code release, diffs
tracked.  [documented: github.com/Piebald-AI/claude-code-system-prompts,
2026-09-04]

### 5b. rossignol6712/claude-code-custom-prompt

Toolkit for replacing Claude Code's default system prompt and compact
templates.  Uses `--system-prompt-file` to inject ordered Markdown files
at launch, with `--append-system-prompt-file` for a persona layer.
Reliability: moderate -- community project, single maintainer.
[documented: github.com/rossignol6712/claude-code-custom-prompt,
2026-09-04]

### 5c. asgeirtj/system_prompts_leaks

64k+ stars.  Extracted stock system prompts for Claude Fable 5, Opus 5,
Claude Code, ChatGPT GPT-5.6-Sol, Codex, Gemini 3.5, Grok, Cursor,
Copilot, and 45+ more.  Extraction method: social engineering
("Pliny the Liberator").  Trended #1 on GitHub 2026-07-06 to 07-11,
covered by Washington Post and AWS Security Blog.  Reliability: the
prompts are real captured outputs, but may lag behind current
deployments.  [documented: github.com/asgeirtj/system_prompts_leaks,
2026-09-04]

### 5d. Claude Code Agent SDK `--system-prompt` / `systemPrompt`

Anthropic's own first-party mechanism.  The Agent SDK uses a minimal
system prompt by default (tool instructions only, no coding guidelines
or project context).  `systemPrompt` replaces the default entirely;
`appendSystemPrompt` adds to it.  This is the intended extension point.
[documented: code.claude.com/docs/en/agent-sdk/modifying-system-prompts,
2026-09-04]

### 5e. OpenCode Provider-Specific Prompt Files

OpenCode ships per-provider prompt files: `anthropic.txt` for Claude,
`beast.txt` for GPT/o1/o3, `gemini.txt` for Gemini, `codex_header.txt`
for GPT-5, `trinity.txt` for Trinity, `qwen.txt` as fallback.  The
system prompt is fully replaceable via config.  [documented:
github.com/anomalyco/opencode, forums.basehub.com, 2026-09-04]

### 5f. Headroom (headroomlabs-ai/headroom)

68k stars, Apache-2.0.  A context-compression layer that wraps Claude
Code, Codex, Cursor, Aider, OpenCode, and MCP clients.  Does not
replace the system prompt but compresses tool output and history before
it reaches the model, reducing token spend 20-95%.  Relevant as
infrastructure that sits between harness and model.  [documented:
github.com/headroomlabs-ai/headroom, 2026-09-04]

---

## Sources

- https://github.com/deepseek-ai/deepseek-harness -- DeepSeek Harness repository (2026-09-04)
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/core/system-prompt/README.md -- system prompt assembly (2026-09-04)
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/context/agent-instructions -- agent instructions loader (2026-09-04)
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/providers.md -- provider config (2026-09-04)
- https://deepseek.com/harness/en/ -- official DeepSeek Harness page (2026-09-04)
- https://manifest.build/blog/chatgpt-plus-tokens-third-party-harnesses/ -- ChatGPT Plus third-party harness policy analysis (2026)
- https://openai.com/policies/row-terms-of-use/ -- OpenAI Terms of Use (2026-09-04)
- https://github.com/dyuan311/dsh-openai-codex-oauth -- dsh ChatGPT OAuth plugin (2026-09-04)
- https://en.wikipedia.org/wiki/Pi_(AI_agent) -- Pi (AI agent) Wikipedia (2026-09-04)
- https://platform.claude.com/docs/en/build-with-claude/working-with-messages -- Anthropic Messages API (2026-09-04)
- https://lunary.ai/blog/openai-developer-role -- OpenAI developer role (2026)
- https://developers.openai.com/api/docs/guides/migrate-to-responses -- OpenAI Responses API migration (2026)
- https://api-docs.deepseek.com/ -- DeepSeek API docs (2026-09-04)
- https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts -- Claude Code system prompt modification (2026-09-04)
- https://developers.openai.com/codex/cli -- Codex CLI docs (2026-09-04)
- https://github.com/Piebald-AI/claude-code-system-prompts -- Claude Code system prompts archive (2026-09-04)
- https://github.com/rossignol6712/claude-code-custom-prompt -- custom prompt toolkit (2026-09-04)
- https://github.com/asgeirtj/system_prompts_leaks -- system prompt leaks archive (2026-09-04)
- https://github.com/anomalyco/opencode -- OpenCode (2026-09-04)
- https://github.com/headroomlabs-ai/headroom -- Headroom context compression (2026-09-04)
