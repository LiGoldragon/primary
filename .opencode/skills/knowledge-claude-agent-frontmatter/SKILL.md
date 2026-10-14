---
name: knowledge-claude-agent-frontmatter
description: The installed Claude Code contract for an agent file's model, effort and tools frontmatter.
---

The following is the local Markdown agent-file parser in Claude Code 2.1.294, checked on 2026-10-13. The YAML frontmatter declares metadata; the body supplies that agent's prompt. Required `name` and `description` are strings. The local parser rejects a missing description/name, a name beginning with a hyphen, an overlong name or a name containing a colon reserved for plugin namespacing.

| Field | Installed parser behavior |
|---|---|
| `model` | A nonempty string is trimmed; `inherit` is normalized case-insensitively. Aliases such as haiku/sonnet/opus/fable and full model IDs are accepted as strings. Backend model availability is a separate check. Omission permits the configured default subagent/main inheritance path. |
| `effort` | The parser accepts low, medium, high, xhigh and max, plus a parsed integer form. An invalid value produces a warning and is omitted. Model capability and inherited/environment effort handling still apply; this field is not an assurance that every model accepts every value. |
| `tools` | A string or string-list is normalized into tool names. A wildcard resolves to inheritance; omission leaves the inherited pool. An explicit empty list selects no listed tools. Resolution filters against the available tool pool; a declaration cannot manufacture a missing tool. |
| `disallowedTools` | Separate exclusions are applied during tool resolution. |

`model` selects the model; `effort` selects reasoning effort; `tools` selects capabilities. A layer's name is not any of these fields. Agent memory configuration can add its required file tools to an explicitly declared list, so the effective set can differ from the literal list. SDK JSON definitions and plugin agent definitions have related parsers, with additional source-specific restrictions; this local-file contract does not erase those differences.

## Native parsing witness and source

An isolated private `.claude/agents/source-witness.md` declared `model: haiku`, `effort: medium` and `tools: Read, Write, Edit`. The installed SDK initialize response listed the agent with model haiku. That response's agent summary exposes name, description and model, not effective effort or tools; it proves the file was discovered and parsed, not that those settings were exercised in a model turn. No agent was launched.

The installed local loader is `OQn` around byte 214479552; normalization uses `RIe` at 212864467 and `TU` at 208128376; tool resolution uses `FA` at 220235439. The current [Claude subagent documentation](https://code.claude.com/docs/en/sub-agents) is corroboration, not a substitute for the inspected version. Source fragments, the fixture and initialization receipt are retained in `/home/li/private-repos/flow-evidence/41fa34/harness-knowledge-20261013/`.
