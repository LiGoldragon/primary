# Pi Subagent Chat Switching Scout Map

## Task and scope

Research question on 2026-07-01: whether the Pi terminal AI harness supports switching the active chat/session into a sub-agent for direct user interaction, similar to Claude/Codex sub-agent chat switching. Scope prioritized Pi official docs/repos, the Pi sub-agent extension, and other Pi extensions that might provide the behavior. This was a read-only research task; no code edits were made outside this output file.

## Short answer

Supported by another extension, but not by the package named `pi-subagents` from `nicobailon`.

If "the Pi sub-agent extension" means `pi install npm:pi-subagents` / `nicobailon/pi-subagents`, I found launch, monitor, foreground streaming, background status, result collection, chain/parallel orchestration, intercom/clarification, and session fork behavior, but not direct user chat switching into the child session.

If the requirement is "open a sub-agent and talk to it directly from Pi's UI", current ecosystem packages do claim that:

- `@tintinweb/pi-subagents` supports FleetView and a live conversation viewer where the user can open a subagent's conversation and send a user message through an inline composer.
- `pi-ultra-subagents` supports embedded interactive `$agent` chats from the main editor and can save final answer, full transcript, return to the sub-agent session, or discard.
- `HazAT/pi-interactive-subagents` supports direct user-driven subagents in multiplexer panes; it is interactive, but the UX is pane-based rather than Pi's main editor becoming the child chat.

## Evidence table

| Source | What it proves |
|---|---|
| Pi official site, `https://pi.dev/`, lines 49-52 in web open | Pi's official positioning is extension-first: customize with extensions/skills/templates/themes, and core Pi "skips features like sub-agents and plan mode." |
| Pi official README, `https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md`, lines 251-255 and 314-315 in web open | Official repo says Pi is a minimal terminal harness, extendable through TypeScript extensions, skills, prompt templates, themes, and Pi packages; default tools are `read`, `write`, `edit`, `bash`. |
| Pi official README, same file, lines 365-374 and 387-407 in web open | Pi interactive mode supports extension UI in messages/editor/widgets/overlays and extension-registered commands, making chat-switching-like behavior plausible as an extension surface. |
| Pi official README, same file, lines 439-465 in web open | Pi has tree-structured sessions, `/tree`, `/fork`, and `/clone`, but this is ordinary session branching, not a built-in sub-agent chat switch. |
| Pi extension docs raw, `https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/docs/extensions.md`, lines 0-1, 14, and 20-28 in web open | Extensions can register tools/commands, create custom UI with keyboard input, persist session entries, and hook session lifecycle events. This backs the user's belief that non-basic behavior is extension-based. |
| Pi package catalog, `https://pi.dev/packages`, lines 64-74 | The top package named `pi-subagents` is described as "delegating tasks to subagents with chains, parallel execution, and TUI clarification", not as active chat switching. |
| `nicobailon/pi-subagents` README, `https://github.com/nicobailon/pi-subagents`, lines 286-290 | The README defines Pi as the parent session and a subagent as a focused child Pi session; Pi starts the child, gives it a task, and brings the result back. Foreground runs stream; background runs can be checked later. |
| `nicobailon/pi-subagents` README, lines 945-955 and 1152-1179 | Management actions and observability cover list/get/models/status artifacts, temp dirs, per-run logs/jsonl/meta files, child session files, async completion notifications, and widget/status files. This supports launch/monitor/results behavior. |
| `nicobailon/pi-subagents` README, lines 1203-1207 | Foreground runs show compact live progress and `Ctrl+O` expands full streaming view. This is viewing progress/output, not becoming the child chat. |
| `nicobailon/pi-subagents` README / search snippet for "Optional pi-intercom companion" | `pi-intercom` lets child agents talk back to the parent session while running, especially for decisions. The child gets `contact_supervisor`; this is child-to-parent coordination, not direct user chat inside a child. |
| `nicobailon/pi-intercom` README search result | `pi-intercom` routes messages between Pi sessions and integrates with `pi-subagents` by giving delegated children a `contact_supervisor` tool. It is a closest companion behavior, not sub-agent chat switching by itself. |
| Pi package catalog, `https://pi.dev/packages`, lines 108-118 | Official package catalog lists `@tintinweb/pi-subagents` separately from `pi-subagents`. |
| `@tintinweb/pi-subagents` README, `https://github.com/tintinweb/pi-subagents`, lines 286-298 | This package claims Claude-Code-style subagents, foreground/background, mid-run steering, completed-session resume, FleetView, and a conversation viewer. |
| `@tintinweb/pi-subagents` README, lines 374-384 | FleetView renders `main` plus running subagents below the editor; at an empty prompt the user can focus the list and press Enter to open the selected agent's live conversation overlay. |
| `@tintinweb/pi-subagents` README, lines 297-298 | The conversation viewer auto-follows a selected agent's full conversation and lets the user press Enter, type, and submit a message; the message appears as a user message and redirects the agent after its current tool. This is the strongest source-backed match to "chat switching" among checked packages. |
| Pi package page for `pi-ultra-subagents`, `https://pi.dev/packages/pi-ultra-subagents`, lines 17-20 and 62-77 | The package is described by the Pi catalog as a sub-agent extension with isolated child sessions, fork-current context, interactive agent chats, bundled agents, and structured result merging. |
| `liangxiao777/pi-ultra-subagents` README, `https://github.com/liangxiao777/pi-ultra-subagents`, lines 238-249 and 271-291 | The repo says it adds interactive `$agent` sessions, embedded sub-agent chat from the main editor, `$` completion, context inheritance prompts, live child-agent activity, and exit choices including saving final answer/full transcript or returning to the sub-agent session. |
| `HazAT/pi-interactive-subagents` README, `https://github.com/HazAT/pi-interactive-subagents`, lines 245-252 | This extension runs subagents in their own terminal pane with a live widget and returns results to the main session. |
| `HazAT/pi-interactive-subagents` README, lines 505-535 | If the user sends input before the agent finishes, auto-exit is disabled and "the user takes over interactively"; interactive agents can run while the user thinks/types/reads in the subagent's pane. This is true direct interaction, but via pane handoff rather than active Pi chat replacement. |
| `HazAT/pi-interactive-subagents` releases search result for v3.5.1 | Release notes explicitly distinguish long-running, user-driven interactive subagents and suppress parent wakeups for them. |
| `dbachelder/pi-btw` search result and Pi catalog lines 499-509 | `pi-btw` provides parallel side conversations, not sub-agent switching. It is relevant as a separate Pi side-chat pattern but does not prove specialist child-agent chat switching. |

## Observed facts

- Pi core still presents itself as a minimal harness whose built-in feature set intentionally omits sub-agents.
- Official Pi documentation exposes enough extension primitives for packages to implement sub-agent UI: custom tools, commands, input hooks, session hooks, custom TUI, widgets, overlays, and session entries.
- `nicobailon/pi-subagents` is the package installed as `pi install npm:pi-subagents` and its docs describe parent-orchestrated delegation: child Pi sessions are started with a task; foreground output streams into the parent; background runs are checked later; results, logs, JSONL, and status files are collected.
- `nicobailon/pi-subagents` plus `pi-intercom` supports a child asking the parent/supervisor for decisions while running. That is a coordination bridge, not direct user control of the child's chat.
- `@tintinweb/pi-subagents` is a separate package with a direct in-Pi UI surface for opening a subagent's live conversation and sending a user message to it.
- `pi-ultra-subagents` is a separate package, listed on `pi.dev/packages`, that explicitly claims embedded interactive `$agent` chats from the main editor.
- `HazAT/pi-interactive-subagents` supports direct interactive child sessions in multiplexer panes, including user takeover when input is sent before auto-exit.

## Interpretations

- For the package named `pi-subagents` by `nicobailon`, the closest existing behavior is delegation plus monitoring/results, optionally augmented by `pi-intercom` so a child can ask for help. The likely extension gap is a first-class UI action that opens a child session as an interactive chat/composer and routes user input into that child until the user returns.
- For the broader Pi ecosystem, the behavior is not "unsupported"; it appears supported by other packages. The closest "Claude/Codex-like switch from main list into a sub-agent conversation" match is `@tintinweb/pi-subagents` FleetView/conversation viewer. The closest "type `$agent` and enter an embedded child chat" match is `pi-ultra-subagents`.
- `HazAT/pi-interactive-subagents` proves an alternate design: use terminal multiplexer panes and let the user interact directly with the child process. That may satisfy "direct interaction" but not necessarily "active Pi chat/session switch" if the user expects a single embedded conversation view.

## Uncertainty and limits

- I did not run live Pi sessions, install packages, or smoke-test the TUI behavior. Claims are source-backed from current docs, package catalog pages, README text, and search-indexed release/issue snippets.
- I did not inspect every extension source file in full. The primary evidence is README/package docs and official package catalog descriptions.
- The phrase "Pi sub-agent extension" is ambiguous. In current search/package results it may mean `pi-subagents` by `nicobailon`, `@tintinweb/pi-subagents`, or another similarly named package. The answer changes depending on which package the user means.
- `pi-ultra-subagents` is source-backed but young: package page shows version `0.1.0`, published Jun 11, 2026, low downloads, and the GitHub repo page showed one commit / zero stars at time checked. Treat it as evidence of an existing extension claiming the feature, not maturity evidence.
- `@tintinweb/pi-subagents` and `HazAT/pi-interactive-subagents` appear mature enough from README/package activity signals to count as real ecosystem options, but I did not verify install compatibility against the user's Pi version.

## Exact searches and sources checked

Search terms used:

- `Pi terminal AI harness sub-agent extension GitHub`
- `P-I terminal AI harness extensions sub-agent`
- `site:github.com Pi AI harness sub-agent extension`
- `"Pi" "sub-agent" "extension" "terminal" AI harness`
- `site:github.com/nicobailon/pi-subagents/issues interactive subagent chat switch`
- `site:github.com/nicobailon/pi-subagents/issues "interactive" "subagent" "chat"`
- `site:github.com/tintinweb/pi-subagents issues "FleetView" "conversation viewer"`
- `site:github.com/HazAT/pi-interactive-subagents issues "interactive" "subagent"`
- `site:github.com "pi-btw" "Pi" "side conversations"`
- `site:github.com "Pi extension" "side conversations" "/btw"`
- `site:github.com "pi-crew" "interactive" "subagent" "Pi extension"`
- `site:github.com "@gotgenes/pi-subagents" "interactive" "conversation"`
- `pi-intercom Pi subagents GitHub README child agents talk back parent`
- `site:github.com nicobailon pi-intercom pi-subagents "private coordination channel"`
- `site:github.com "pi-intercom" "child agents" "parent" Pi`

Sources checked:

- Official Pi site: `https://pi.dev/`
- Official Pi package catalog: `https://pi.dev/packages`
- Official Pi package page: `https://pi.dev/packages/pi-ultra-subagents`
- Official Pi repository: `https://github.com/earendil-works/pi`
- Official Pi coding-agent README: `https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md`
- Official Pi extension docs raw: `https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/docs/extensions.md`
- `nicobailon/pi-subagents`: `https://github.com/nicobailon/pi-subagents`
- `nicobailon/pi-intercom`: `https://github.com/nicobailon/pi-intercom`
- `tintinweb/pi-subagents`: `https://github.com/tintinweb/pi-subagents`
- `HazAT/pi-interactive-subagents`: `https://github.com/HazAT/pi-interactive-subagents`
- `liangxiao777/pi-ultra-subagents`: `https://github.com/liangxiao777/pi-ultra-subagents`
- `dbachelder/pi-btw`: `https://github.com/dbachelder/pi-btw`

## Local context consulted

- `AGENTS.md` was supplied in the prompt and followed.
- Local search command: `rg -n "Pi|P-I|sub-agent|sub agent|subagent|terminal AI harness|extension" -S AGENTS.md .agents .codex .pi 2>/dev/null`
- Local file list command: `rg --files -g 'README*' -g 'AGENTS.md' -g '*pi*' -g '*Pi*' . 2>/dev/null | head -200`
- Prior local report read: `agent-outputs/RoleSkillReview/Scout-PiSubagentMining.md`, which documents local mining of `pi-subagents` 0.31.0 role material and confirms the local workspace has treated `nicobailon/pi-subagents` as the active package named `pi-subagents`.
- Public intent query command: `spirit "(PublicTextSearch [Pi sub-agent extension terminal AI harness])"` returned general agent-system intent records including `n9fl` about specific agents/skills and `qjrf` about not inferring intent; no Pi-specific user intent record was found.

## Blockers and follow-up requirements

- To answer "will this work in my current installed Pi session?", a live check should run `pi list` and inspect installed package names/versions, then read the installed package README/source or start a test session. That was outside this read-only web research scope.
- If the user is specifically on `pi-subagents` by `nicobailon`, the extension gap is interactive child-session takeover/open-in-chat. If they can switch packages, `@tintinweb/pi-subagents` or `pi-ultra-subagents` should be evaluated against their exact desired UX and Pi version.
