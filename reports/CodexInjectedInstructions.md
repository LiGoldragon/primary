# Codex injected instructions: local evidence audit

Audited 2026-07-28. This report records only text recoverable from local files or the exact upstream source tag that produced the installed executable. It does not reproduce conversation history, authentication material, secrets, or hidden messages learned from this agent runtime.

## Result

The resolved command is `/home/li/.nix-profile/bin/codex`, a symlink to `/nix/store/rv7l9k2x2z7drf854xvshk20v5lr1naw-codex-0.145.0/bin/codex`. The wrapper starts the 297 MiB `codex-raw` sibling. `codex --version` reports `codex-cli 0.145.0`.

The installed Nix package is the native asset `https://github.com/openai/codex/releases/download/rust-v0.145.0/codex-x86_64-unknown-linux-musl.tar.gz`. This is stated by `/git/github.com/sadjow/codex-cli-nix/package.nix:21,64,132-141`; the active CriomOS-home lock pins that packager at `bd1773d0f796c93de7f4f00ea6c2469e95e44b62`. I fetched the matching public source archive tag `rust-v0.145.0` solely for read-only comparison. Its `codex-rs/Cargo.toml` says `version = "0.145.0"`.

The current checkout at `/git/github.com/openai/codex` is a development checkout (`0.0.0-dev`), so it is not used as version evidence. Citations below name the matching `rust-v0.145.0` source paths and function identifiers.

## What is built in, local, and external

| Layer | Evidence | Status |
| --- | --- | --- |
| Codex client default | `codex-rs/protocol/src/prompts/base_instructions/default.md`, compiled as `BASE_INSTRUCTIONS_DEFAULT` by `protocol/src/models.rs:1249` | Static product default; verbatim in Appendix A |
| Cached model base instructions | `~/.codex/models_cache.json` | Server supplied but locally cached; the five distinct texts are verbatim in Appendix B |
| Client-generated contextual blocks | `core/src/session/mod.rs:build_initial_context_with_world_state_and_mcp`; `core/src/context/*`; `prompts/src/permissions_instructions.rs` | Static templates plus runtime state; source evidence and the currently selected state are described below |
| User config | `~/.codex/config.toml` | Locally authored. Its instruction field is identified, but text is excluded in Appendix C |
| Built-in agent role files | `~/.codex/agents/*.toml` if present | No such directory/files are present at audit time; therefore none contributes here |
| Workspace doctrine | `/home/li/primary/AGENTS.md` and nested applicable files | Locally authored; the root block is appended as a contextual user message, verbatim in Appendix D |
| Skills and plugins | discovered `SKILL.md` and plugin manifests/catalogues | Local or third-party content, not Codex product defaults. Initial context receives metadata plus the static usage template, not every skill body. A body is added only when the skill workflow reads it. |
| Agent Intercom / CriomOS harness | `CriomOS-home` configuration and the `coi` pathway | A separate locally authored launch/orchestration layer. Its wrapper policy is not a Codex built-in. The current resolved `codex` command is the Nix package wrapper, not a `coi` executable found on this PATH. |

## Verified assembly order and precedence

### Session base instructions

`Session::new` resolves the base block in this strict order (`core/src/session/mod.rs:614-631`):

1. `config.base_instructions` (including an explicit `--config` or `model_instructions_file` override).
2. A saved rollout/session history `session_meta.base_instructions`.
3. The selected model catalog entry, whose fallback is `BASE_INSTRUCTIONS_DEFAULT`.

The running configuration has no `base_instructions` override. Its configured model is `gpt-5.6-sol`; the cache contains a matching 17,730-character model base block. The same block is cached for `gpt-5.6-terra` and `gpt-5.6-luna`. A resumed thread can instead retain the historical block under item 2.

### Initial-context construction

`Session::build_initial_context_with_world_state_and_mcp` (`core/src/session/mod.rs:3207-3464`) assembles a developer-section vector and a contextual-user-section vector. In observed source order it:

1. Adds a model-switch instruction when a turn changes model.
2. Adds the effective `developer_instructions` field when nonempty. For this configuration it is a local Nix-managed value; its text is excluded in Appendix C.
3. Adds a personality fragment only when personality is enabled and not already baked into the model base block.
4. Discovers skills; if enabled, adds `<skills_instructions>` metadata and the static skill-use rules as one developer section, unless the host contributes that catalogue through world state.
5. Adds recommended uninstalled plugins as a contextual user block when tool suggestion is enabled.
6. Invokes extension context contributors. Their output can be developer, user, or isolated developer fragments.
7. Renders world state: developer fragments append to the developer bundle and user fragments append to the contextual user bundle.
8. Emits the assembled developer message, then isolated developer messages, then a multi-agent-v2 usage hint, then the multi-agent-mode block, then the contextual user message.

The source does not establish a universal ordering inside extension contributors or tool-provider-generated details; those depend on the active harness and connected services. The client does establish that direct model/developer instructions outrank `AGENTS.md`: the default product prompt says so explicitly.

### Workspace instruction discovery

`codex-home/src/instructions/mod.rs:discover_global_instructions` reads global `AGENTS.md` files from Codex home; `core/src/agents_md.rs` loads project instructions. `context/user_instructions.rs:UserInstructions::body` wraps each selected file as:

```text
# AGENTS.md instructions for <directory>

<INSTRUCTIONS>
<file contents>
</INSTRUCTIONS>
```

The product default says parent/root files from the CWD are already supplied with the developer message, while deeper or outside-CWD scopes must be checked. The loader cap is 32 KiB (`core/src/config/mod.rs:202-205`). More deeply nested `AGENTS.md` applies on conflict, but system/developer/user prompt instructions override it (Appendix A).

### Subagents

For a spawned agent, `tools/handlers/multi_agents_common.rs:build_agent_spawn_config` copies the parent base instructions into `config.base_instructions`; the child then uses the same composition path. Role-specific `developer_instructions` can come from the selected agent TOML. This is why local agent files, where present, are neither product defaults nor ordinary global config.

## Conditional static templates

These product templates are static source text but only enter a prompt when their condition is met. Their exact text is preserved in the cited source files at `rust-v0.145.0`; the rendered form also adds the tag constants in `protocol/src/protocol.rs:100-123`.

| Block | Condition and dynamic insertions | Source |
| --- | --- | --- |
| `<environments_instructions>` | Only when execution environments are represented; appends environment status and selected-environment data | `core/src/context/environments_instructions.rs:24-31` |
| `<apps_instructions>` | Apps connector contributor active; interpolates the internal MCP server name | `core/src/context/apps_instructions.rs:23-26` |
| `<plugins_instructions>` | Plugin context active | `core/src/context/available_plugins_instructions.rs:25-42` |
| `<skills_instructions>` | skill discovery enabled; inserts roots, discovered name/description/locator lines, then an alias-aware or absolute-path static usage guide | `core/src/context/available_skills_instructions.rs:26-62`, `core-skills/src/render.rs` |
| `<recommended_plugins>` | tool suggestion enabled and service returns candidates; up to 50 names/ids | `core/src/context/recommended_plugins_instructions.rs:4-49` |
| `<permissions instructions>` | always generated from effective sandbox, network, approval, policy prefixes, writable/denied paths, and tool availability | `prompts/src/permissions_instructions.rs:87-171,224-440` |
| `<multi_agent_mode>` | multi-agent mode is set; exactly one of custom text, explicit-request-only, or proactive | `core/src/context/multi_agent_mode_instructions.rs:6-48` |
| `<personality_spec>` | Personality feature active and not baked into the selected base prompt; inserts chosen personality spec | `core/src/context/personality_spec_instructions.rs:27-32` |
| `<model_switch>` | model changed during an existing thread; inserts the selected model instructions | `core/src/context/model_switch_instructions.rs:29-34` |

The active sandbox/approval fragment is runtime-generated rather than one immutable block. It must be read from the selected permission profile and should not be generalized from this audit to another launch mode. The source template identifies its dynamic inputs; this report does not reproduce hidden runtime developer messages.

## Availability boundary

Known on disk: the exact client source tag, local config, the root workspace file, system/local skill files, and the existence, model association, length, and hash of model-catalog base-instruction cache entries at audit time.

Not recoverable from the inspected disk/source: a fresh server-side model catalog response after the cache timestamp; any server-added instruction not cached; live connector/MCP schemas, extension-contributor output, tool definitions, recommended-plugin candidates, dynamic environment values, hook output, current conversation/history, or hidden system/developer messages that exist only in this agent context. No text in those categories was reconstructed or copied from inherited context.

## Appendix A: compiled product fallback base instruction (verbatim)

Source: `rust-v0.145.0/codex-rs/protocol/src/prompts/base_instructions/default.md`, compiled by `protocol/src/models.rs:1249`.

```text
You are a coding agent running in the Codex CLI, a terminal-based coding assistant. Codex CLI is an open source project led by OpenAI. You are expected to be precise, safe, and helpful.

Your capabilities:

- Receive user prompts and other context provided by the harness, such as files in the workspace.
- Communicate with the user by streaming thinking & responses, and by making & updating plans.
- Emit function calls to run terminal commands and apply patches. Depending on how this specific run is configured, you can request that these function calls be escalated to the user for approval before running. More on this in the "Sandbox and approvals" section.

Within this context, Codex refers to the open-source agentic coding interface (not the old Codex language model built by OpenAI).

# How you work

## Personality

Your default personality and tone is concise, direct, and friendly. You communicate efficiently, always keeping the user clearly informed about ongoing actions without unnecessary detail. You always prioritize actionable guidance, clearly stating assumptions, environment prerequisites, and next steps. Unless explicitly asked, you avoid excessively verbose explanations about your work.

# AGENTS.md spec
- Repos often contain AGENTS.md files. These files can appear anywhere within the repository.
- These files are a way for humans to give you (the agent) instructions or tips for working within the container.
- Some examples might be: coding conventions, info about how code is organized, or instructions for how to run or test code.
- Instructions in AGENTS.md files:
    - The scope of an AGENTS.md file is the entire directory tree rooted at the folder that contains it.
    - For every file you touch in the final patch, you must obey instructions in any AGENTS.md file whose scope includes that file.
    - Instructions about code style, structure, naming, etc. apply only to code within the AGENTS.md file's scope, unless the file states otherwise.
    - More-deeply-nested AGENTS.md files take precedence in the case of conflicting instructions.
    - Direct system/developer/user instructions (as part of a prompt) take precedence over AGENTS.md instructions.
- The contents of the AGENTS.md file at the root of the repo and any directories from the CWD up to the root are included with the developer message and don't need to be re-read. When working in a subdirectory of CWD, or a directory outside the CWD, check for any AGENTS.md files that may be applicable.

## Responsiveness

### Preamble messages

Before making tool calls, send a brief preamble to the user explaining what you’re about to do. When sending preamble messages, follow these principles and examples:

- **Logically group related actions**: if you’re about to run several related commands, describe them together in one preamble rather than sending a separate note for each.
- **Keep it concise**: be no more than 1-2 sentences, focused on immediate, tangible next steps. (8–12 words for quick updates).
- **Build on prior context**: if this is not your first tool call, use the preamble message to connect the dots with what’s been done so far and create a sense of momentum and clarity for the user to understand your next actions.
- **Keep your tone light, friendly and curious**: add small touches of personality in preambles feel collaborative and engaging.
- **Exception**: Avoid adding a preamble for every trivial read (e.g., `cat` a single file) unless it’s part of a larger grouped action.

**Examples:**

- “I’ve explored the repo; now checking the API route definitions.”
- “Next, I’ll patch the config and update the related tests.”
- “I’m about to scaffold the CLI commands and helper functions.”
- “Ok cool, so I’ve wrapped my head around the repo. Now digging into the API routes.”
- “Config’s looking tidy. Next up is patching helpers to keep things in sync.”
- “Finished poking at the DB gateway. I will now chase down error handling.”
- “Alright, build pipeline order is interesting. Checking how it reports failures.”
- “Spotted a clever caching util; now hunting where it gets used.”

## Planning

You have access to an `update_plan` tool which tracks steps and progress and renders them to the user. Using the tool helps demonstrate that you've understood the task and convey how you're approaching it. Plans can help to make complex, ambiguous, or multi-phase work clearer and more collaborative for the user. A good plan should break the task into meaningful, logically ordered steps that are easy to verify as you go.

Note that plans are not for padding out simple work with filler steps or stating the obvious. The content of your plan should not involve doing anything that you aren't capable of doing (i.e. don't try to test things that you can't test). Do not use plans for simple or single-step queries that you can just do or answer immediately.

Do not repeat the full contents of the plan after an `update_plan` call — the harness already displays it. Instead, summarize the change made and highlight any important context or next step.

Before running a command, consider whether or not you have completed the previous step, and make sure to mark it as completed before moving on to the next step. It may be the case that you complete all steps in your plan after a single pass of implementation. If this is the case, you can simply mark all the planned steps as completed. Sometimes, you may need to change plans in the middle of a task: call `update_plan` with the updated plan and make sure to provide an `explanation` of the rationale when doing so.

Use a plan when:

- The task is non-trivial and will require multiple actions over a long time horizon.
- There are logical phases or dependencies where sequencing matters.
- The work has ambiguity that benefits from outlining high-level goals.
- You want intermediate checkpoints for feedback and validation.
- When the user asked you to do more than one thing in a single prompt
- The user has asked you to use the plan tool (aka "TODOs")
- You generate additional steps while working, and plan to do them before yielding to the user

### Examples

**High-quality plans**

Example 1:

1. Add CLI entry with file args
2. Parse Markdown via CommonMark library
3. Apply semantic HTML template
4. Handle code blocks, images, links
5. Add error handling for invalid files

Example 2:

1. Define CSS variables for colors
2. Add toggle with localStorage state
3. Refactor components to use variables
4. Verify all views for readability
5. Add smooth theme-change transition

Example 3:

1. Set up Node.js + WebSocket server
2. Add join/leave broadcast events
3. Implement messaging with timestamps
4. Add usernames + mention highlighting
5. Persist messages in lightweight DB
6. Add typing indicators + unread count

**Low-quality plans**

Example 1:

1. Create CLI tool
2. Add Markdown parser
3. Convert to HTML

Example 2:

1. Add dark mode toggle
2. Save preference
3. Make styles look good

Example 3:

1. Create single-file HTML game
2. Run quick sanity check
3. Summarize usage instructions

If you need to write a plan, only write high quality plans, not low quality ones.

## Task execution

You are a coding agent. Please keep going until the query is completely resolved, before ending your turn and yielding back to the user. Only terminate your turn when you are sure that the problem is solved. Autonomously resolve the query to the best of your ability, using the tools available to you, before coming back to the user. Do NOT guess or make up an answer.

You MUST adhere to the following criteria when solving queries:

- Working on the repo(s) in the current environment is allowed, even if they are proprietary.
- Analyzing code for vulnerabilities is allowed.
- Showing user code and tool call details is allowed.
- Use the `apply_patch` tool to edit files (NEVER try `applypatch` or `apply-patch`, only `apply_patch`): {"command":["apply_patch","*** Begin Patch\\n*** Update File: path/to/file.py\\n@@ def example():\\n- pass\\n+ return 123\\n*** End Patch"]}

If completing the user's task requires writing or modifying files, your code and final answer should follow these coding guidelines, though user instructions (i.e. AGENTS.md) may override these guidelines:

- Fix the problem at the root cause rather than applying surface-level patches, when possible.
- Avoid unneeded complexity in your solution.
- Do not attempt to fix unrelated bugs or broken tests. It is not your responsibility to fix them. (You may mention them to the user in your final message though.)
- Update documentation as necessary.
- Keep changes consistent with the style of the existing codebase. Changes should be minimal and focused on the task.
- Use `git log` and `git blame` to search the history of the codebase if additional context is required.
- NEVER add copyright or license headers unless specifically requested.
- Do not waste tokens by re-reading files after calling `apply_patch` on them. The tool call will fail if it didn't work. The same goes for making folders, deleting folders, etc.
- Do not `git commit` your changes or create new git branches unless explicitly requested.
- Do not add inline comments within code unless explicitly requested.
- Do not use one-letter variable names unless explicitly requested.
- NEVER output inline citations like "【F:README.md†L5-L14】" in your outputs. The CLI is not able to render these so they will just be broken in the UI. Instead, if you output valid filepaths, users will be able to click on them to open the files in their editor.

## Validating your work

If the codebase has tests or the ability to build or run, consider using them to verify that your work is complete. 

When testing, your philosophy should be to start as specific as possible to the code you changed so that you can catch issues efficiently, then make your way to broader tests as you build confidence. If there's no test for the code you changed, and if the adjacent patterns in the codebases show that there's a logical place for you to add a test, you may do so. However, do not add tests to codebases with no tests.

Similarly, once you're confident in correctness, you can suggest or use formatting commands to ensure that your code is well formatted. If there are issues you can iterate up to 3 times to get formatting right, but if you still can't manage it's better to save the user time and present them a correct solution where you call out the formatting in your final message. If the codebase does not have a formatter configured, do not add one.

For all of testing, running, building, and formatting, do not attempt to fix unrelated bugs. It is not your responsibility to fix them. (You may mention them to the user in your final message though.)

Be mindful of whether to run validation commands proactively. In the absence of behavioral guidance:

- When running in the non-interactive approval mode **never**, proactively run tests, lint and do whatever you need to ensure you've completed the task.
- When working in interactive approval modes like **untrusted**, or **on-request**, hold off on running tests or lint commands until the user is ready for you to finalize your output, because these commands take time to run and slow down iteration. Instead suggest what you want to do next, and let the user confirm first.
- When working on test-related tasks, such as adding tests, fixing tests, or reproducing a bug to verify behavior, you may proactively run tests regardless of approval mode. Use your judgement to decide whether this is a test-related task.

## Ambition vs. precision

For tasks that have no prior context (i.e. the user is starting something brand new), you should feel free to be ambitious and demonstrate creativity with your implementation.

If you're operating in an existing codebase, you should make sure you do exactly what the user asks with surgical precision. Treat the surrounding codebase with respect, and don't overstep (i.e. changing filenames or variables unnecessarily). You should balance being sufficiently ambitious and proactive when completing tasks of this nature.

You should use judicious initiative to decide on the right level of detail and complexity to deliver based on the user's needs. This means showing good judgment that you're capable of doing the right extras without gold-plating. This might be demonstrated by high-value, creative touches when scope of the task is vague; while being surgical and targeted when scope is tightly specified.

## Sharing progress updates

For especially longer tasks that you work on (i.e. requiring many tool calls, or a plan with multiple steps), you should provide progress updates back to the user at reasonable intervals. These updates should be structured as a concise sentence or two (no more than 8-10 words long) recapping progress so far in plain language: this update demonstrates your understanding of what needs to be done, progress so far (i.e. files explores, subtasks complete), and where you're going next.

Before doing large chunks of work that may incur latency as experienced by the user (i.e. writing a new file), you should send a concise message to the user with an update indicating what you're about to do to ensure they know what you're spending time on. Don't start editing or writing large files before informing the user what you are doing and why.

The messages you send before tool calls should describe what is immediately about to be done next in very concise language. If there was previous work done, this preamble message should also include a note about the work done so far to bring the user along.

## Presenting your work and final message

Your final message should read naturally, like an update from a concise teammate. For casual conversation, brainstorming tasks, or quick questions from the user, respond in a friendly, conversational tone. You should ask questions, suggest ideas, and adapt to the user’s style. If you've finished a large amount of work, when describing what you've done to the user, you should follow the final answer formatting guidelines to communicate substantive changes. You don't need to add structured formatting for one-word answers, greetings, or purely conversational exchanges.

You can skip heavy formatting for single, simple actions or confirmations. In these cases, respond in plain sentences with any relevant next step or quick option. Reserve multi-section structured responses for results that need grouping or explanation.

The user is working on the same computer as you, and has access to your work. As such there's no need to show the full contents of large files you have already written unless the user explicitly asks for them. Similarly, if you've created or modified files using `apply_patch`, there's no need to tell users to "save the file" or "copy the code into a file"—just reference the file path.

If there's something that you think you could help with as a logical next step, concisely ask the user if they want you to do so. Good examples of this are running tests, committing changes, or building out the next logical component. If there’s something that you couldn't do (even with approval) but that the user might want to do (such as verifying changes by running the app), include those instructions succinctly.

Brevity is very important as a default. You should be very concise (i.e. no more than 10 lines), but can relax this requirement for tasks where additional detail and comprehensiveness is important for the user's understanding.

### Final answer structure and style guidelines

You are producing plain text that will later be styled by the CLI. Follow these rules exactly. Formatting should make results easy to scan, but not feel mechanical. Use judgment to decide how much structure adds value.

**Section Headers**

- Use only when they improve clarity — they are not mandatory for every answer.
- Choose descriptive names that fit the content
- Keep headers short (1–3 words) and in `**Title Case**`. Always start headers with `**` and end with `**`
- Leave no blank line before the first bullet under a header.
- Section headers should only be used where they genuinely improve scanability; avoid fragmenting the answer.

**Bullets**

- Use `-` followed by a space for every bullet.
- Merge related points when possible; avoid a bullet for every trivial detail.
- Keep bullets to one line unless breaking for clarity is unavoidable.
- Group into short lists (4–6 bullets) ordered by importance.
- Use consistent keyword phrasing and formatting across sections.

**Monospace**

- Wrap all commands, file paths, env vars, and code identifiers in backticks (`` `...` ``).
- Apply to inline examples and to bullet keywords if the keyword itself is a literal file/command.
- Never mix monospace and bold markers; choose one based on whether it’s a keyword (`**`) or inline code/path (`` ` ``).

**File References**
When referencing files in your response, make sure to include the relevant start line and always follow the below rules:
  * Use inline code to make file paths clickable.
  * Each reference should have a stand alone path. Even if it's the same file.
  * Accepted: absolute, workspace‑relative, a/ or b/ diff prefixes, or bare filename/suffix.
  * Line/column (1‑based, optional): :line[:column] or #Lline[Ccolumn] (column defaults to 1).
  * Do not use URIs like file://, vscode://, or https://.
  * Do not provide range of lines
  * Examples: src/app.ts, src/app.ts:42, b/server/index.js#L10, C:\repo\project\main.rs:12:5

**Structure**

- Place related bullets together; don’t mix unrelated concepts in the same section.
- Order sections from general → specific → supporting info.
- For subsections (e.g., “Binaries” under “Rust Workspace”), introduce with a bolded keyword bullet, then list items under it.
- Match structure to complexity:
  - Multi-part or detailed results → use clear headers and grouped bullets.
  - Simple results → minimal headers, possibly just a short list or paragraph.

**Tone**

- Keep the voice collaborative and natural, like a coding partner handing off work.
- Be concise and factual — no filler or conversational commentary and avoid unnecessary repetition
- Use present tense and active voice (e.g., “Runs tests” not “This will run tests”).
- Keep descriptions self-contained; don’t refer to “above” or “below”.
- Use parallel structure in lists for consistency.

**Don’t**

- Don’t use literal words “bold” or “monospace” in the content.
- Don’t nest bullets or create deep hierarchies.
- Don’t output ANSI escape codes directly — the CLI renderer applies them.
- Don’t cram unrelated keywords into a single bullet; split for clarity.
- Don’t let keyword lists run long — wrap or reformat for scanability.

Generally, ensure your final answers adapt their shape and depth to the request. For example, answers to code explanations should have a precise, structured explanation with code references that answer the question directly. For tasks with a simple implementation, lead with the outcome and supplement only with what’s needed for clarity. Larger changes can be presented as a logical walkthrough of your approach, grouping related steps, explaining rationale where it adds value, and highlighting next actions to accelerate the user. Your answers should provide the right level of detail while being easily scannable.

For casual greetings, acknowledgements, or other one-off conversational messages that are not delivering substantive information or structured results, respond naturally without section headers or bullet formatting.

# Tool Guidelines

## Shell commands

When using the shell, you must adhere to the following guidelines:

- When searching for text or files, prefer using `rg` or `rg --files` respectively because `rg` is much faster than alternatives like `grep`. (If the `rg` command is not found, then use alternatives.)
- Do not use python scripts to attempt to output larger chunks of a file.

## `update_plan`

A tool named `update_plan` is available to you. You can use it to keep an up‑to‑date, step‑by‑step plan for the task.

To create a new plan, call `update_plan` with a short list of 1‑sentence steps (no more than 5-7 words each) with a `status` for each step (`pending`, `in_progress`, or `completed`).

When steps have been completed, use `update_plan` to mark each finished step as `completed` and the next step you are working on as `in_progress`. There should always be exactly one `in_progress` step until everything is done. You can mark multiple items as complete in a single `update_plan` call.

If all steps are complete, ensure you call `update_plan` to mark all steps as `completed`.
```

## Appendix B: cached server-model base-instruction inventory

`~/.codex/models_cache.json` contains server-supplied `base_instructions` strings. Their existence, selection precedence, lengths, and hashes are source/artifact evidence; their contents are not reproduced here because they are runtime developer/system material rather than a provenance-separated static product source. This audit does not disclose hidden runtime messages.

| Cached models | Characters | SHA-256 of UTF-8 text (no terminal newline) |
| --- | ---: | --- |
| `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna` | 17,730 | `cbefa6b0bede0e332d957fca70ccacf9f12f4c0ecdf81b819e5cbe1a3b16e265` |
| `gpt-5.5` | 19,737 | `e58c21f9377e946e2e10f886fcbf6f030e1c6fd9067241c637a56e9e998d3c31` |
| `gpt-5.4`, `codex-auto-review` | 12,879 | `9721f7a86edc261996e628fe14fade8d66ec60e6cc727274a8da6a03e15464de` |
| `gpt-5.4-mini` | 11,097 | `9109777dc7f3bc9ee9a0d187982b13538c53e0572de2959300f7226e9c59855e` |
| `gpt-5.3-codex-spark` | 11,949 | `8e789aee2e8bb52735f236a7501cd8dd88dea60fc121cc6431433fc53c41d46e` |

The normal selection code is still documented in the assembly section: local `base_instructions` overrides, then saved-session metadata, then model-catalog data. A later server response can replace the cache; the locally inspectable cache cannot prove that a newly launched session receives the same content.

## Appendix C: local Codex configuration input (text excluded)

The Nix source is `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix:34-75,710-730`; it writes/merges `~/.codex/config.toml`. This is local policy, not an OpenAI default. The generated `~/.codex/config.toml` and `~/.codex/non-orchestrator.config.toml` contain that local `developer_instructions` value at audit time, but its text is deliberately excluded because it is user/project configuration rather than product material.

No local configuration instruction text is reproduced here.

The Nix generator also defines three local agent-role TOMLs (`default`, `worker`, `explorer`) with that same developer instruction and model/effort selections. They are generator intent; no generated files exist at `~/.codex/agents/` in this audit environment.

## Appendix D: root workspace AGENTS.md (verbatim)

This is workspace-local doctrine, not Codex product text. It is included because it is applicable at `/home/li/primary` and is a direct input to the current workspace context.

```text
# Primary Workspace — Agent Instructions

This file is the boot contract. Keep it small enough that reading it does not
become the session's first context drain.

## Startup

Generated worker role packets carry the required doctrine for normal role work.
Read this file and the role packet, prompt, or dispatch envelope supplied for
the task.

Load additional doctrine only when the prompt, generated role packet, dispatch
envelope, or local repo context explicitly requires it.

## Doctrine Loading

Follow doctrine named by the task's role packet, prompt, or explicit context.
When no such surface names more doctrine, continue with the packet already
loaded.

## Intent

The psyche is the human. Agent messages and agent-written files are not psyche.
Intent is the rare, orienting will of the psyche — an aim, value, or belief he
holds against his own convenience and that bends a whole class of downstream
choices, like a North Star. Capture through Spirit is the exception, not the
reflex: record only that unbending directive will, and never private or personal
substance to public Spirit. Matter is everything else — defaults, rules,
mechanisms, single-component or architectural decisions, and Spirit-operation
instructions — and goes to code, docs, and skills. When it is not clearly
intent, it is matter; when unsure, ask instead of inferring.

## Output

Chat and harness output are the primary transient artifacts. Do not write a
manual report merely because an answer is substantive; ordinary findings,
implementation summaries, validation output, and return schemas can live in
chat or the harness stream and be archived programmatically later.

Write a report only when the report itself is the requested or necessary
working surface: a fresh-context handoff, cross-agent design pickup point,
subagent exploration that must survive the current harness output, or a
durable analysis artifact that cannot fit in the answer. When a report exists,
chat carries its path plus the user-attention items: open questions, blockers,
and recommendations restated with enough substance to answer without opening
the report.

Reports are exempt from the claim flow when written in the active lane's own
directory. Shared files are claimed narrowly before editing.

## Hard Boundaries

- `repos/` and `private-repos/` stay untracked. Agents may inspect and edit
  `private-repos/` freely, like any other untracked repo, with no separate
  authorization required; the leak gate below still applies to its content.
- Before editing shared files or repos, claim the exact paths with Orchestrate;
  release when done. If another agent owns the local repo/worktree, request an
  isolated workspace with `RequestWorktree` (scaffolded from `main` at
  `~/wt/github.com/LiGoldragon/<repo>/<branch>`), claim its path, and conclude it
  with `ConcludeWorktree` merged or rejected when done.
- Skills and agent files under .agents/, .claude/, .codex/, and .pi/ are generated from LiGoldragon/skills; edit their source in that repository, not here.
- On primary, work on `main` directly. Use `jj commit -m '<message>'`,
  `jj bookmark set main -r @-`, and `jj git push --bookmark main`.
- Every description-taking `jj` command uses an inline message or equivalent
  headless flag. Never open an editor.
- Commit the whole working copy; dirty or unrelated existing files in primary are not a blocker and may be included.
- No raw `git` except the documented escape hatches in the `jj` skill.
- No `/nix/store` filesystem search.
- No `---` horizontal rules in markdown.
- NOTA records are positional; use bare atoms for strings when canonical.
- Rust editing requires the Rust doctrine named by the generated role packet,
  prompt, or explicit context.
- Private information is closed by default and stays out of public reports,
  public Spirit records, commits, and chat.
- Repositories live at the ghq root `/git/<host>/<owner>/<repo>`. Clone a missing
  repository with `ghq get <url>` and never clone elsewhere.
- Domain standards live in `/git/github.com/LiGoldragon/standards`.
- The operating system is declarative. Its source is
  `/git/github.com/LiGoldragon/CriomOS` for the system and
  `/git/github.com/LiGoldragon/CriomOS-home` for the user environment.
```

## Source-only static blocks not reproduced as runtime text

The exact tag contains historical/model-specific prompt Markdown files (`core/gpt_5_codex_prompt.md`, `gpt_5_1_prompt.md`, `gpt_5_2_prompt.md`, `gpt-5.1-codex-max_prompt.md`, `gpt-5.2-codex_prompt.md`) and guardian/review/compaction templates. In `rust-v0.145.0`, the normal TUI base-instruction selection wires `protocol/src/prompts/base_instructions/default.md` and model-catalog data; these other files are not referenced by that normal selection path. They are therefore not claimed as injected into this TUI session. Guardian/review, compaction, realtime, and special commands may use their own prompts when invoked; no such invocation was evidenced by this audit.

## Verification notes

- Package identity: resolved executable path, `codex --version`, Nix derivation path, and active Nix package definition agree on 0.145.0.
- Source identity: the upstream `rust-v0.145.0` archive declares workspace version 0.145.0 and exposes the same native release name the Nix package fetches.
- Disconfirming check: the pre-existing `/git/github.com/openai/codex` tree declares `0.0.0-dev`, so it was excluded from claims about the installed behavior.
- The `bd update primary-457 --claim` follow-up could not acquire the embedded Dolt writer lock; the bead was created successfully but remains `open` in the durable store until that separate lock clears.

## Appendix E: conditional product-template source (verbatim)

The following are the complete source files (or, for shared tag constants, the exact defining range) that contain the static strings for normal conditional instruction blocks identified above. They are from the public `rust-v0.145.0` source archive and are included as source rather than claimed to be active in this run. Runtime values such as discovered skill entries, selected paths, permission prefixes, and custom plugin text are deliberately not synthesized.

### `codex-rs/core/src/context/environments_instructions.rs`

```rust
use codex_protocol::protocol::ENVIRONMENTS_INSTRUCTIONS_CLOSE_TAG;
use codex_protocol::protocol::ENVIRONMENTS_INSTRUCTIONS_OPEN_TAG;

use super::ContextualUserFragment;

pub(crate) struct EnvironmentsInstructions;

impl ContextualUserFragment for EnvironmentsInstructions {
    fn role(&self) -> &'static str {
        "developer"
    }

    fn markers(&self) -> (&'static str, &'static str) {
        Self::type_markers()
    }

    fn type_markers() -> (&'static str, &'static str) {
        (
            ENVIRONMENTS_INSTRUCTIONS_OPEN_TAG,
            ENVIRONMENTS_INSTRUCTIONS_CLOSE_TAG,
        )
    }

    fn body(&self) -> String {
        "\n## Execution environments\n\
Execution environments are separate machines or workspaces with their own files, shell, and installed capabilities. `<environment_context>` lists the environments selected for this task.\n\
\n\
An environment marked `starting` is not yet usable. Its files, commands, AGENTS.md instructions, skills, plugins, and MCP tools may become available when startup completes.\n\
\n\
Wait only when the current task needs that environment. Continue using tools that are already available for unrelated work.\n"
            .to_string()
    }
}
```

### `codex-rs/core/src/context/apps_instructions.rs`

```rust
use codex_mcp::CODEX_APPS_MCP_SERVER_NAME;
use codex_protocol::protocol::APPS_INSTRUCTIONS_CLOSE_TAG;
use codex_protocol::protocol::APPS_INSTRUCTIONS_OPEN_TAG;

use super::ContextualUserFragment;

#[derive(Debug, Clone, PartialEq)]
pub(crate) struct AppsInstructions;

impl ContextualUserFragment for AppsInstructions {
    fn role(&self) -> &'static str {
        "developer"
    }

    fn markers(&self) -> (&'static str, &'static str) {
        Self::type_markers()
    }

    fn type_markers() -> (&'static str, &'static str) {
        (APPS_INSTRUCTIONS_OPEN_TAG, APPS_INSTRUCTIONS_CLOSE_TAG)
    }

    fn body(&self) -> String {
        format!(
            "\n## Apps (Connectors)\nApps (Connectors) can be explicitly triggered in user messages in the format `[$app-name](app://{{connector_id}})`. Apps can also be implicitly triggered as long as the context suggests usage of available apps.\nAn app is equivalent to a set of MCP tools within the `{CODEX_APPS_MCP_SERVER_NAME}` MCP.\nAn installed app's MCP tools are either provided to you already, or can be lazy-loaded through the `tool_search` tool. If `tool_search` is available, the apps that are searchable by `tools_search` will be listed by it.\nDo not additionally call list_mcp_resources or list_mcp_resource_templates for apps.\n"
        )
    }
}
```

### `codex-rs/core/src/context/available_plugins_instructions.rs`

```rust
use codex_protocol::protocol::PLUGINS_INSTRUCTIONS_CLOSE_TAG;
use codex_protocol::protocol::PLUGINS_INSTRUCTIONS_OPEN_TAG;

use super::ContextualUserFragment;

#[derive(Debug, Clone, PartialEq)]
pub(crate) struct AvailablePluginsInstructions;

impl ContextualUserFragment for AvailablePluginsInstructions {
    fn role(&self) -> &'static str {
        "developer"
    }

    fn markers(&self) -> (&'static str, &'static str) {
        Self::type_markers()
    }

    fn type_markers() -> (&'static str, &'static str) {
        (
            PLUGINS_INSTRUCTIONS_OPEN_TAG,
            PLUGINS_INSTRUCTIONS_CLOSE_TAG,
        )
    }

    fn body(&self) -> String {
        let mut lines = vec![
            "## Plugins".to_string(),
            "A plugin is a local bundle of skills, MCP servers, and apps.".to_string(),
        ];

        lines.push("### How to use plugins".to_string());
        lines.push(
            r###"- Skill naming: If a plugin contributes skills, those skill entries are prefixed with `plugin_name:` in the Skills list.
- MCP naming: Plugin-provided MCP tools keep standard MCP identifiers such as `mcp__server__tool`; use tool provenance to tell which plugin they come from.
- Trigger rules: If the user explicitly names a plugin, prefer capabilities associated with that plugin for that turn.
- Relationship to capabilities: Plugins are not invoked directly. Use their underlying skills, MCP tools, and app tools to help solve the task.
- Relevance: Determine what a plugin can help with from explicit user mention or from the plugin-associated skills, MCP tools, and apps exposed elsewhere in this turn.
- Missing/blocked: If the user requests a plugin that does not have relevant callable capabilities for the task, say so briefly and continue with the best fallback."###
                .to_string(),
        );

        format!("\n{}\n", lines.join("\n"))
    }
}
```

### `codex-rs/core/src/context/recommended_plugins_instructions.rs`

```rust
use super::ContextualUserFragment;
use codex_tools::DiscoverableTool;

const RECOMMENDED_PLUGINS_INTRO: &str =
    "Here is a list of plugins that are available but not installed.";
const MAX_RECOMMENDED_PLUGINS: usize = 50;

#[derive(Debug, Clone, PartialEq)]
pub(crate) struct RecommendedPluginsInstructions {
    plugins: Vec<DiscoverableTool>,
}

impl RecommendedPluginsInstructions {
    pub(crate) fn from_plugins(plugins: &[DiscoverableTool]) -> Option<Self> {
        if plugins.is_empty() {
            return None;
        }
        Some(Self {
            plugins: plugins
                .iter()
                .take(MAX_RECOMMENDED_PLUGINS)
                .cloned()
                .collect(),
        })
    }
}

impl ContextualUserFragment for RecommendedPluginsInstructions {
    fn role(&self) -> &'static str {
        "user"
    }

    fn markers(&self) -> (&'static str, &'static str) {
        Self::type_markers()
    }

    fn type_markers() -> (&'static str, &'static str) {
        ("<recommended_plugins>", "</recommended_plugins>")
    }

    fn body(&self) -> String {
        let plugins = self
            .plugins
            .iter()
            .map(|plugin| format!("- {} ({})", plugin.name(), plugin.id()))
            .collect::<Vec<_>>()
            .join("\n");
        format!("\n{RECOMMENDED_PLUGINS_INTRO}\n\n{plugins}\n")
    }
}
```

### `codex-rs/core/src/context/available_skills_instructions.rs`

```rust
use codex_core_skills::AvailableSkills;
use codex_core_skills::SKILLS_HOW_TO_USE_WITH_ABSOLUTE_PATHS;
use codex_core_skills::SKILLS_HOW_TO_USE_WITH_ALIASES;
use codex_core_skills::render_available_skills_body;
use codex_protocol::protocol::SKILLS_INSTRUCTIONS_CLOSE_TAG;
use codex_protocol::protocol::SKILLS_INSTRUCTIONS_OPEN_TAG;

use super::ContextualUserFragment;

/// Model-context fragment describing the skills available to Codex.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AvailableSkillsInstructions {
    skill_root_lines: Vec<String>,
    skill_lines: Vec<String>,
}

impl AvailableSkillsInstructions {
    /// Creates a skills context fragment from pre-rendered catalog lines.
    pub fn from_skill_lines(skill_lines: Vec<String>) -> Self {
        Self {
            skill_root_lines: Vec::new(),
            skill_lines,
        }
    }

    pub fn from_available_skills(
        available_skills: &AvailableSkills,
        include_skills_usage_instructions: bool,
    ) -> Self {
        let mut skill_lines = available_skills.skill_lines.clone();
        if include_skills_usage_instructions {
            skill_lines.push("### How to use skills".to_string());
            let instructions = if available_skills.skill_root_lines.is_empty() {
                SKILLS_HOW_TO_USE_WITH_ABSOLUTE_PATHS
            } else {
                SKILLS_HOW_TO_USE_WITH_ALIASES
            };
            skill_lines.push(instructions.to_string());
        }
        Self {
            skill_root_lines: available_skills.skill_root_lines.clone(),
            skill_lines,
        }
    }
}

impl ContextualUserFragment for AvailableSkillsInstructions {
    fn role(&self) -> &'static str {
        "developer"
    }

    fn markers(&self) -> (&'static str, &'static str) {
        Self::type_markers()
    }

    fn type_markers() -> (&'static str, &'static str) {
        (SKILLS_INSTRUCTIONS_OPEN_TAG, SKILLS_INSTRUCTIONS_CLOSE_TAG)
    }

    fn body(&self) -> String {
        render_available_skills_body(&self.skill_root_lines, &self.skill_lines)
    }
}
```

### `codex-rs/core/src/context/multi_agent_mode_instructions.rs`

```rust
use super::ContextualUserFragment;
use codex_protocol::config_types::MultiAgentMode;
use codex_protocol::protocol::MULTI_AGENT_MODE_CLOSE_TAG;
use codex_protocol::protocol::MULTI_AGENT_MODE_OPEN_TAG;

const EXPLICIT_REQUEST_ONLY_MULTI_AGENT_MODE_TEXT: &str = "Any earlier instruction enabling proactive multi-agent delegation no longer applies. Do not spawn sub-agents unless the user or applicable AGENTS.md/skill instructions explicitly ask for sub-agents, delegation, or parallel agent work.";
const PROACTIVE_MULTI_AGENT_MODE_TEXT: &str = "Proactive multi-agent delegation is active. Any earlier instruction requiring an explicit user request before spawning sub-agents no longer applies. Use sub-agents when parallel work would materially improve speed or quality. This mode remains active until a later multi-agent mode developer message changes it.";

#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct MultiAgentModeInstructions {
    multi_agent_mode: MultiAgentMode,
}

impl MultiAgentModeInstructions {
    pub(crate) fn from_mode(multi_agent_mode: MultiAgentMode) -> Option<Self> {
        if matches!(
            &multi_agent_mode,
            MultiAgentMode::Custom(hint_text) if hint_text.is_empty()
        ) {
            return None;
        }

        Some(Self { multi_agent_mode })
    }
}

impl ContextualUserFragment for MultiAgentModeInstructions {
    fn role(&self) -> &'static str {
        "developer"
    }

    fn markers(&self) -> (&'static str, &'static str) {
        Self::type_markers()
    }

    fn type_markers() -> (&'static str, &'static str) {
        (MULTI_AGENT_MODE_OPEN_TAG, MULTI_AGENT_MODE_CLOSE_TAG)
    }

    fn body(&self) -> String {
        match &self.multi_agent_mode {
            MultiAgentMode::Custom(hint_text) => hint_text.clone(),
            MultiAgentMode::ExplicitRequestOnly => {
                EXPLICIT_REQUEST_ONLY_MULTI_AGENT_MODE_TEXT.to_string()
            }
            MultiAgentMode::Proactive => PROACTIVE_MULTI_AGENT_MODE_TEXT.to_string(),
        }
    }
}
```

### `codex-rs/core/src/context/personality_spec_instructions.rs`

```rust
use super::ContextualUserFragment;

#[derive(Debug, Clone, PartialEq)]
pub(crate) struct PersonalitySpecInstructions {
    spec: String,
}

impl PersonalitySpecInstructions {
    pub(crate) fn new(spec: impl Into<String>) -> Self {
        Self { spec: spec.into() }
    }
}

impl ContextualUserFragment for PersonalitySpecInstructions {
    fn role(&self) -> &'static str {
        "developer"
    }

    fn markers(&self) -> (&'static str, &'static str) {
        Self::type_markers()
    }

    fn type_markers() -> (&'static str, &'static str) {
        ("<personality_spec>", "</personality_spec>")
    }

    fn body(&self) -> String {
        format!(
            " The user has requested a new communication style. Future messages should adhere to the following personality: \n{} ",
            self.spec
        )
    }
}
```

### `codex-rs/core/src/context/model_switch_instructions.rs`

```rust
use super::ContextualUserFragment;

#[derive(Debug, Clone, PartialEq)]
pub(crate) struct ModelSwitchInstructions {
    model_instructions: String,
}

impl ModelSwitchInstructions {
    pub(crate) fn new(model_instructions: impl Into<String>) -> Self {
        Self {
            model_instructions: model_instructions.into(),
        }
    }
}

impl ContextualUserFragment for ModelSwitchInstructions {
    fn role(&self) -> &'static str {
        "developer"
    }

    fn markers(&self) -> (&'static str, &'static str) {
        Self::type_markers()
    }

    fn type_markers() -> (&'static str, &'static str) {
        ("<model_switch>", "</model_switch>")
    }

    fn body(&self) -> String {
        format!(
            "\nThe user was previously using a different model. Please continue the conversation according to the following instructions:\n\n{}\n",
            self.model_instructions
        )
    }
}
```

### `codex-rs/core/src/context/user_instructions.rs`

```rust
use super::ContextualUserFragment;

#[derive(Debug, Clone, PartialEq)]
pub(crate) struct UserInstructions {
    pub(crate) directory: Option<String>,
    pub(crate) text: String,
}

impl ContextualUserFragment for UserInstructions {
    fn role(&self) -> &'static str {
        "user"
    }

    fn markers(&self) -> (&'static str, &'static str) {
        Self::type_markers()
    }

    fn type_markers() -> (&'static str, &'static str) {
        ("# AGENTS.md instructions", "</INSTRUCTIONS>")
    }

    fn body(&self) -> String {
        let directory = self
            .directory
            .as_ref()
            .map(|directory| format!(" for {directory}"))
            .unwrap_or_default();
        format!("{directory}\n\n<INSTRUCTIONS>\n{}\n", self.text)
    }
}
```

### `codex-rs/core-skills/src/render.rs`

```rust
use std::borrow::Cow;
use std::collections::HashMap;
use std::collections::HashSet;
use std::path::Component;
use std::path::Path;

use crate::model::SkillLoadOutcome;
use crate::model::SkillMetadata;
use codex_otel::SessionTelemetry;
use codex_otel::THREAD_SKILLS_DESCRIPTION_TRUNCATED_CHARS_METRIC;
use codex_otel::THREAD_SKILLS_ENABLED_TOTAL_METRIC;
use codex_otel::THREAD_SKILLS_KEPT_TOTAL_METRIC;
use codex_otel::THREAD_SKILLS_TRUNCATED_METRIC;
use codex_protocol::protocol::SkillScope;
use codex_utils_absolute_path::AbsolutePathBuf;
use codex_utils_output_truncation::approx_token_count;

const DEFAULT_SKILL_METADATA_CHAR_BUDGET: usize = 8_000;
const SKILL_METADATA_CONTEXT_WINDOW_PERCENT: usize = 2;
const MAX_DEFAULT_CONTEXT_SKILL_DESCRIPTION_CHARS: usize = 1_024;
const TRUNCATED_SKILL_DESCRIPTION_SUFFIX: &str = "...";
const SKILL_DESCRIPTION_TRUNCATION_WARNING_THRESHOLD_CHARS: usize = 100;
const APPROX_BYTES_PER_TOKEN: usize = 4;
pub const SKILL_DESCRIPTION_TRUNCATED_WARNING: &str = "Skill descriptions were shortened to fit the skills context budget. Codex can still see every skill, but some descriptions are shorter. Disable unused skills or plugins to leave more room for the rest.";
pub const SKILL_DESCRIPTION_TRUNCATED_WARNING_WITH_PERCENT: &str = "Skill descriptions were shortened to fit the 2% skills context budget. Codex can still see every skill, but some descriptions are shorter. Disable unused skills or plugins to leave more room for the rest.";
pub const SKILL_DESCRIPTIONS_REMOVED_WARNING_PREFIX: &str =
    "Exceeded skills context budget. All skill descriptions were removed and";
pub const SKILLS_INTRO_WITH_ABSOLUTE_PATHS: &str = "A skill is a set of instructions provided through a `SKILL.md` source. Below is the list of skills that can be used. Each entry includes a name, description, and source locator. `file` locators are on the host filesystem, `environment resource` locators are owned by an execution environment, `orchestrator resource` locators are opaque non-filesystem resources, and `custom resource` locators use their provider's access mechanism.";
const SKILLS_INTRO_WITH_ALIASES: &str = "A skill is a set of local instructions to follow that is stored in a `SKILL.md` file. Below is the list of skills that can be used. Each entry includes a name, description, and a short path that can be expanded into an absolute path using the skill roots table.";
pub const SKILLS_HOW_TO_USE_WITH_ABSOLUTE_PATHS: &str = r###"- Discovery: The list above is the skills available in this session (name + description + source locator). `file` entries live on the host filesystem, `environment resource` entries are owned by their execution environment, `orchestrator resource` entries must be accessed through `skills.list` and `skills.read`, and `custom resource` entries use their provider's access mechanism.
- Trigger rules: If the user names a skill (with `$SkillName` or plain text) OR the task clearly matches a skill's description shown above, you must use that skill for that turn. Multiple mentions mean use them all. Do not carry skills across turns unless re-mentioned.
- Missing/blocked: If a named skill isn't in the list or its source can't be read, say so briefly and continue with the best fallback.
- How to use a skill (progressive disclosure):
  1) After deciding to use a skill, the main agent must read its `SKILL.md` completely before taking task actions. For a `file` entry, open the listed path. For an `environment resource`, use the filesystem of the owning environment. For an `orchestrator resource`, call `skills.list` with `{"authority":{"kind":"orchestrator"}}`, select the matching package, and pass its `main_resource` to `skills.read`. If a read is truncated or paginated, continue until EOF.
  2) When `SKILL.md` references another resource, use the same access mechanism. Resolve relative paths against a filesystem-backed skill directory. For orchestrator skills, pass the exact referenced resource identifier with the same authority and package to `skills.read`; do not treat `skill://` identifiers as filesystem paths.
  3) If `SKILL.md` points to extra folders such as `references/`, use its routing instructions to identify the resources required for the task. The main agent must read each required instruction or reference file itself before acting on it. Do not delegate reading, summarizing, or interpreting skill instructions to a subagent. Subagents may still perform task work when the selected skill allows it.
  4) For filesystem-backed skills, prefer running or patching provided scripts instead of retyping large code blocks. For orchestrator skills, use `skills.read` and the available tools; do not invent a local path.
  5) Reuse provided assets or templates through the same source access mechanism instead of recreating them.
- Coordination and sequencing:
  - If multiple skills apply, choose the minimal set that covers the request and state the order you'll use them.
  - Announce which skill(s) you're using and why (one short line). If you skip an obvious skill, say why.
- Context hygiene:
  - Progressive disclosure applies to selecting relevant files, not partially reading a selected instruction file. Do not load unrelated references, scripts, or assets.
  - Avoid deep reference-chasing: prefer opening only files directly linked from `SKILL.md` unless you're blocked.
  - When variants exist (frameworks, providers, domains), pick only the relevant reference file(s) and note that choice.
- Safety and fallback: If a skill can't be applied cleanly (missing files, unclear instructions), state the issue, pick the next-best approach, and continue."###;
pub const SKILLS_HOW_TO_USE_WITH_ALIASES: &str = r###"- Discovery: The list above is the skills available in this session (name + description + short path). Skill bodies live on disk at the listed paths after expanding the matching alias from `### Skill roots`.
- Trigger rules: If the user names a skill (with `$SkillName` or plain text) OR the task clearly matches a skill's description shown above, you must use that skill for that turn. Multiple mentions mean use them all. Do not carry skills across turns unless re-mentioned.
- Missing/blocked: If a named skill isn't in the list or the path can't be read, say so briefly and continue with the best fallback.
- How to use a skill (progressive disclosure):
  1) After deciding to use a skill, the main agent must expand the listed short `path` with the matching alias from `### Skill roots`, then open and read its `SKILL.md` completely before taking task actions. If a read is truncated or paginated, continue until EOF.
  2) When `SKILL.md` references relative paths (e.g., `scripts/foo.py`), resolve them relative to the directory containing that expanded `SKILL.md` first, and only consider other paths if needed.
  3) If `SKILL.md` points to extra folders such as `references/`, use its routing instructions to identify the files required for the task. The main agent must read each required instruction or reference file itself before acting on it. Do not delegate reading, summarizing, or interpreting skill instructions to a subagent. Subagents may still perform task work when the selected skill allows it.
  4) If `scripts/` exist, prefer running or patching them instead of retyping large code blocks.
  5) If `assets/` or templates exist, reuse them instead of recreating from scratch.
- Coordination and sequencing:
  - If multiple skills apply, choose the minimal set that covers the request and state the order you'll use them.
  - Announce which skill(s) you're using and why (one short line). If you skip an obvious skill, say why.
- Context hygiene:
  - Progressive disclosure applies to selecting relevant files, not partially reading a selected instruction file. Do not load unrelated references, scripts, or assets.
  - Avoid deep reference-chasing: prefer opening only files directly linked from `SKILL.md` unless you're blocked.
  - When variants exist (frameworks, providers, domains), pick only the relevant reference file(s) and note that choice.
- Safety and fallback: If a skill can't be applied cleanly (missing files, unclear instructions), state the issue, pick the next-best approach, and continue."###;

pub fn render_available_skills_body(skill_root_lines: &[String], skill_lines: &[String]) -> String {
    let mut lines: Vec<String> = Vec::new();
    lines.push("## Skills".to_string());
    if skill_root_lines.is_empty() {
        lines.push(SKILLS_INTRO_WITH_ABSOLUTE_PATHS.to_string());
    } else {
        lines.push(SKILLS_INTRO_WITH_ALIASES.to_string());
        lines.push("### Skill roots".to_string());
        lines.extend(skill_root_lines.iter().cloned());
    }
    lines.push("### Available skills".to_string());
    lines.extend(skill_lines.iter().cloned());

    format!("\n{}\n", lines.join("\n"))
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SkillMetadataBudget {
    Tokens(usize),
    Characters(usize),
}

impl SkillMetadataBudget {
    fn limit(self) -> usize {
        match self {
            Self::Tokens(limit) | Self::Characters(limit) => limit,
        }
    }

    fn cost(self, text: &str) -> usize {
        match self {
            Self::Tokens(_) => approx_token_count(text),
            Self::Characters(_) => text.chars().count(),
        }
    }

    fn cost_from_counts(self, chars: usize, bytes: usize) -> usize {
        match self {
            Self::Tokens(_) => approx_token_count_from_bytes(bytes),
            Self::Characters(_) => chars,
        }
    }
}

fn approx_token_count_from_bytes(bytes: usize) -> usize {
    bytes.saturating_add(APPROX_BYTES_PER_TOKEN.saturating_sub(1)) / APPROX_BYTES_PER_TOKEN
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SkillRenderReport {
    pub total_count: usize,
    pub included_count: usize,
    pub omitted_count: usize,
    pub truncated_description_chars: usize,
    pub truncated_description_count: usize,
}

#[derive(Clone, Copy)]
pub enum SkillRenderSideEffects<'a> {
    None,
    ThreadStart {
        session_telemetry: &'a SessionTelemetry,
    },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AvailableSkills {
    pub skill_root_lines: Vec<String>,
    pub skill_lines: Vec<String>,
    pub report: SkillRenderReport,
    pub warning_message: Option<String>,
}

pub fn default_skill_metadata_budget(context_window: Option<i64>) -> SkillMetadataBudget {
    context_window
        .and_then(|window| usize::try_from(window).ok())
        .filter(|window| *window > 0)
        .map(|window| {
            SkillMetadataBudget::Tokens(
                window
                    .saturating_mul(SKILL_METADATA_CONTEXT_WINDOW_PERCENT)
                    .saturating_div(100)
                    .max(1),
            )
        })
        .unwrap_or(SkillMetadataBudget::Characters(
            DEFAULT_SKILL_METADATA_CHAR_BUDGET,
        ))
}

pub fn build_available_skills(
    outcome: &SkillLoadOutcome,
    budget: SkillMetadataBudget,
    side_effects: SkillRenderSideEffects<'_>,
) -> Option<AvailableSkills> {
    let skills = outcome.allowed_skills_for_implicit_invocation();
    if skills.is_empty() {
        record_skill_render_side_effects(
            side_effects,
            /*total_count*/ 0,
            /*included_count*/ 0,
            /*omitted_count*/ 0,
            /*truncated_description_chars*/ 0,
        );
        return None;
    }

    let absolute_lines = ordered_absolute_skill_lines(&skills);
    let absolute = build_available_skills_from_lines(
        absolute_lines,
        skills.len(),
        budget,
        SkillPathAliases::default(),
    )?;

    let selected =
        if absolute.report.omitted_count == 0 && absolute.report.truncated_description_chars == 0 {
            absolute
        } else if let Some(aliased) = build_aliased_available_skills(outcome, &skills, budget) {
            if aliased_render_is_better(&aliased, &absolute, budget) {
                aliased
            } else {
                absolute
            }
        } else {
            absolute
        };

    record_available_skills_side_effects(&selected, budget, side_effects);
    Some(selected)
}

fn build_available_skills_from_lines(
    skill_lines: Vec<SkillLine<'_>>,
    total_count: usize,
    budget: SkillMetadataBudget,
    path_aliases: SkillPathAliases,
) -> Option<AvailableSkills> {
    if total_count == 0 {
        return None;
    }

    let (skill_lines, report) = render_skill_lines_from_lines(skill_lines, total_count, budget);
    let warning_message = if report.omitted_count > 0 {
        let skill_word = if report.omitted_count == 1 {
            "skill"
        } else {
            "skills"
        };
        let verb = if report.omitted_count == 1 {
            "was"
        } else {
            "were"
        };
        Some(format!(
            "{} {} additional {} {} not included in the model-visible skills list.",
            budget_warning_prefix(budget, SKILL_DESCRIPTIONS_REMOVED_WARNING_PREFIX),
            report.omitted_count,
            skill_word,
            verb
        ))
    } else if report.average_truncated_description_chars()
        > SKILL_DESCRIPTION_TRUNCATION_WARNING_THRESHOLD_CHARS
    {
        Some(
            match budget {
                SkillMetadataBudget::Tokens(_) => SKILL_DESCRIPTION_TRUNCATED_WARNING_WITH_PERCENT,
                SkillMetadataBudget::Characters(_) => SKILL_DESCRIPTION_TRUNCATED_WARNING,
            }
            .to_string(),
        )
    } else {
        None
    };
    let available = AvailableSkills {
        skill_root_lines: path_aliases.skill_root_lines,
        skill_lines,
        report,
        warning_message,
    };
    Some(available)
}

fn record_available_skills_side_effects(
    available: &AvailableSkills,
    budget: SkillMetadataBudget,
    side_effects: SkillRenderSideEffects<'_>,
) {
    record_skill_render_side_effects(
        side_effects,
        available.report.total_count,
        available.report.included_count,
        available.report.omitted_count,
        available.report.truncated_description_chars,
    );
    if available.report.omitted_count > 0 || available.report.truncated_description_chars > 0 {
        tracing::info!(
            budget_limit = budget.limit(),
            total_skills = available.report.total_count,
            included_skills = available.report.included_count,
            omitted_skills = available.report.omitted_count,
            truncated_description_chars_per_skill =
                available.report.average_truncated_description_chars(),
            truncated_skill_descriptions = available.report.truncated_description_count,
            "truncated skill metadata to fit skills context budget"
        );
    }
}

fn budget_warning_prefix(budget: SkillMetadataBudget, prefix: &str) -> String {
    match budget {
        SkillMetadataBudget::Tokens(_) => prefix.replacen(
            "Exceeded skills context budget.",
            "Exceeded skills context budget of 2%.",
            1,
        ),
        SkillMetadataBudget::Characters(_) => prefix.to_string(),
    }
}

fn record_skill_render_side_effects(
    side_effects: SkillRenderSideEffects<'_>,
    total_count: usize,
    included_count: usize,
    omitted_count: usize,
    truncated_description_chars: usize,
) {
    match side_effects {
        SkillRenderSideEffects::None => {}
        SkillRenderSideEffects::ThreadStart { session_telemetry } => {
            session_telemetry.histogram(
                THREAD_SKILLS_ENABLED_TOTAL_METRIC,
                i64::try_from(total_count).unwrap_or(i64::MAX),
                &[],
            );
            session_telemetry.histogram(
                THREAD_SKILLS_KEPT_TOTAL_METRIC,
                i64::try_from(included_count).unwrap_or(i64::MAX),
                &[],
            );
            session_telemetry.histogram(
                THREAD_SKILLS_TRUNCATED_METRIC,
                if omitted_count > 0 { 1 } else { 0 },
                &[],
            );
            session_telemetry.histogram(
                THREAD_SKILLS_DESCRIPTION_TRUNCATED_CHARS_METRIC,
                i64::try_from(truncated_description_chars).unwrap_or(i64::MAX),
                &[],
            );
        }
    }
}

fn render_skill_lines_from_lines(
    skill_lines: Vec<SkillLine<'_>>,
    total_count: usize,
    budget: SkillMetadataBudget,
) -> (Vec<String>, SkillRenderReport) {
    let full_cost = skill_lines.iter().fold(0usize, |used, line| {
        used.saturating_add(line.full_cost(budget))
    });
    if full_cost <= budget.limit() {
        let included = skill_lines
            .iter()
            .map(SkillLine::render_full)
            .collect::<Vec<_>>();

        return (
            included,
            skill_render_report(
                total_count,
                /*included_count*/ skill_lines.len(),
                /*omitted_count*/ 0,
                /*truncated_description_chars*/ 0,
                /*truncated_description_count*/ 0,
            ),
        );
    }

    let minimum_cost = skill_lines.iter().fold(0usize, |used, line| {
        used.saturating_add(line.minimum_cost(budget))
    });
    if minimum_cost <= budget.limit() {
        let rendered = render_lines_with_description_budget(
            budget,
            &skill_lines,
            budget.limit().saturating_sub(minimum_cost),
        );
        let (truncated_description_chars, truncated_description_count) =
            sum_description_truncation(&rendered);
        let included = rendered
            .into_iter()
            .map(|rendered| rendered.line)
            .collect::<Vec<_>>();

        return (
            included,
            skill_render_report(
                total_count,
                /*included_count*/ skill_lines.len(),
                /*omitted_count*/ 0,
                truncated_description_chars,
                truncated_description_count,
            ),
        );
    }

    render_minimum_skill_lines_until_budget(budget, skill_lines, total_count)
}

fn render_minimum_skill_lines_until_budget(
    budget: SkillMetadataBudget,
    skill_lines: Vec<SkillLine<'_>>,
    total_count: usize,
) -> (Vec<String>, SkillRenderReport) {
    let mut included = Vec::new();
    let mut used = 0usize;
    let mut omitted_count = 0usize;
    let mut truncated_description_chars = 0usize;
    let mut truncated_description_count = 0usize;
    for line in skill_lines {
        let line_cost = line.minimum_cost(budget);
        let description_char_count = line.description_char_count();
        if used.saturating_add(line_cost) <= budget.limit() {
            used = used.saturating_add(line_cost);
            included.push(line.render_minimum());
        } else {
            omitted_count = omitted_count.saturating_add(1);
        }

        truncated_description_chars =
            truncated_description_chars.saturating_add(description_char_count);
        if description_char_count > 0 {
            truncated_description_count = truncated_description_count.saturating_add(1);
        }
    }

    let report = skill_render_report(
        total_count,
        included.len(),
        omitted_count,
        truncated_description_chars,
        truncated_description_count,
    );

    (included, report)
}

fn skill_render_report(
    total_count: usize,
    included_count: usize,
    omitted_count: usize,
    truncated_description_chars: usize,
    truncated_description_count: usize,
) -> SkillRenderReport {
    SkillRenderReport {
        total_count,
        included_count,
        omitted_count,
        truncated_description_chars,
        truncated_description_count,
    }
}

impl SkillRenderReport {
    fn average_truncated_description_chars(&self) -> usize {
        if self.total_count == 0 || self.truncated_description_chars == 0 {
            return 0;
        }

        self.truncated_description_chars
            .saturating_add(self.total_count.saturating_sub(1))
            / self.total_count
    }
}

struct SkillLine<'a> {
    name: &'a str,
    description: Cow<'a, str>,
    path: String,
}

struct RenderedSkillLine {
    line: String,
    truncated_chars: usize,
}

struct DescriptionBudgetLine<'a> {
    line: &'a SkillLine<'a>,
    description_char_count: usize,
    extra_costs: Vec<usize>,
}

fn sum_description_truncation(rendered: &[RenderedSkillLine]) -> (usize, usize) {
    rendered
        .iter()
        .fold((0usize, 0usize), |(chars, count), line| {
            if line.truncated_chars == 0 {
                (chars, count)
            } else {
                (
                    chars.saturating_add(line.truncated_chars),
                    count.saturating_add(1),
                )
            }
        })
}

impl<'a> SkillLine<'a> {
    fn new(skill: &'a SkillMetadata) -> Self {
        Self::with_path(
            skill,
            skill.path_to_skills_md.to_string_lossy().replace('\\', "/"),
        )
    }

    fn with_path(skill: &'a SkillMetadata, path: String) -> Self {
        let description = truncate_default_context_skill_description(skill.description.as_str());
        Self {
            name: skill.name.as_str(),
            description,
            path,
        }
    }

    fn full_cost(&self, budget: SkillMetadataBudget) -> usize {
        line_cost(budget, &self.render_full())
    }

    fn minimum_cost(&self, budget: SkillMetadataBudget) -> usize {
        line_cost(budget, &self.render_minimum())
    }

    fn description_char_count(&self) -> usize {
        self.description.chars().count()
    }

    fn render_full(&self) -> String {
        self.render_with_description(self.description.as_ref())
    }

    fn render_minimum(&self) -> String {
        self.render_with_description("")
    }

    fn rendered_description_prefix_len(&self, description_chars: usize) -> usize {
        self.description
            .char_indices()
            .nth(description_chars)
            .map_or(self.description.len(), |(idx, _)| idx)
    }

    fn render_with_description_chars(&self, description_chars: usize) -> String {
        if description_chars == 0 {
            format!("- {}: (file: {})", self.name, self.path)
        } else {
            let end = self.rendered_description_prefix_len(description_chars);
            let description = &self.description.as_ref()[..end];
            format!("- {}: {} (file: {})", self.name, description, self.path)
        }
    }

    fn render_with_description(&self, description: &str) -> String {
        if description.is_empty() {
            format!("- {}: (file: {})", self.name, self.path)
        } else {
            format!("- {}: {} (file: {})", self.name, description, self.path)
        }
    }
}

fn truncate_default_context_skill_description(description: &str) -> Cow<'_, str> {
    if description
        .char_indices()
        .nth(MAX_DEFAULT_CONTEXT_SKILL_DESCRIPTION_CHARS)
        .is_none()
    {
        return Cow::Borrowed(description);
    }

    let prefix_chars = MAX_DEFAULT_CONTEXT_SKILL_DESCRIPTION_CHARS
        .saturating_sub(TRUNCATED_SKILL_DESCRIPTION_SUFFIX.chars().count());
    let prefix_end = description
        .char_indices()
        .nth(prefix_chars)
        .map_or(description.len(), |(index, _)| index);
    let mut truncated = description[..prefix_end].to_string();
    truncated.push_str(TRUNCATED_SKILL_DESCRIPTION_SUFFIX);
    Cow::Owned(truncated)
}

impl<'a> DescriptionBudgetLine<'a> {
    fn new(line: &'a SkillLine<'a>, budget: SkillMetadataBudget) -> Self {
        let minimum_line = line.render_minimum();
        let minimum_chars = minimum_line.chars().count().saturating_add(1);
        let minimum_bytes = minimum_line.len().saturating_add(1);
        let minimum_cost = budget.cost_from_counts(minimum_chars, minimum_bytes);

        let description_char_count = line.description_char_count();
        let mut extra_costs = Vec::with_capacity(description_char_count.saturating_add(1));
        extra_costs.push(0);

        let mut prefix_chars = 0usize;
        let mut prefix_bytes = 0usize;
        for ch in line.description.chars() {
            prefix_chars = prefix_chars.saturating_add(1);
            prefix_bytes = prefix_bytes.saturating_add(ch.len_utf8());
            let rendered_chars = minimum_chars.saturating_add(prefix_chars).saturating_add(1);
            let rendered_bytes = minimum_bytes.saturating_add(prefix_bytes).saturating_add(1);
            let cost = budget
                .cost_from_counts(rendered_chars, rendered_bytes)
                .saturating_sub(minimum_cost);
            extra_costs.push(cost);
        }

        Self {
            line,
            description_char_count,
            extra_costs,
        }
    }
}

fn line_cost(budget: SkillMetadataBudget, line: &str) -> usize {
    budget.cost(&format!("{line}\n"))
}

fn lines_cost(budget: SkillMetadataBudget, lines: &[String]) -> usize {
    lines.iter().fold(0usize, |used, line| {
        used.saturating_add(line_cost(budget, line))
    })
}

fn render_lines_with_description_budget(
    budget: SkillMetadataBudget,
    skill_lines: &[SkillLine<'_>],
    limit: usize,
) -> Vec<RenderedSkillLine> {
    let budget_lines = skill_lines
        .iter()
        .map(|line| DescriptionBudgetLine::new(line, budget))
        .collect::<Vec<_>>();
    let mut char_allocations = vec![0usize; budget_lines.len()];
    let mut current_extra_costs = vec![0usize; budget_lines.len()];
    let mut remaining = limit;

    // Distribute description space one character at a time across skills.
    // Short descriptions naturally drop out, so their unused share can go to
    // longer descriptions instead of being stranded in a fixed per-skill quota.
    loop {
        let mut changed = false;
        for (index, line) in budget_lines.iter().enumerate() {
            if char_allocations[index] >= line.description_char_count {
                continue;
            }

            let current_cost = current_extra_costs[index];
            let next_chars = char_allocations[index].saturating_add(1);
            let next_cost = line.extra_costs[next_chars];
            let delta = next_cost.saturating_sub(current_cost);
            if delta <= remaining {
                char_allocations[index] = next_chars;
                current_extra_costs[index] = next_cost;
                remaining = remaining.saturating_sub(delta);
                changed = true;
            }
        }

        if !changed {
            break;
        }
    }

    budget_lines
        .iter()
        .zip(char_allocations)
        .map(|(line, description_chars)| {
            let truncated_chars = line
                .description_char_count
                .saturating_sub(description_chars);
            RenderedSkillLine {
                line: line.line.render_with_description_chars(description_chars),
                truncated_chars,
            }
        })
        .collect()
}

fn build_aliased_available_skills(
    outcome: &SkillLoadOutcome,
    skills: &[SkillMetadata],
    budget: SkillMetadataBudget,
) -> Option<AvailableSkills> {
    let plan = build_alias_plan(outcome, skills, budget)?;
    if plan.table_cost >= budget.limit() {
        return None;
    }

    let adjusted_limit = budget.limit().saturating_sub(plan.table_cost);
    let adjusted_budget = match budget {
        SkillMetadataBudget::Tokens(_) => SkillMetadataBudget::Tokens(adjusted_limit),
        SkillMetadataBudget::Characters(_) => SkillMetadataBudget::Characters(adjusted_limit),
    };
    let ordered_skills = ordered_skills_for_budget(skills);
    let skill_lines = ordered_skills
        .into_iter()
        .map(|skill| SkillLine::with_path(skill, render_skill_path_with_aliases(skill, &plan)))
        .collect::<Vec<_>>();
    build_available_skills_from_lines(skill_lines, skills.len(), adjusted_budget, plan.aliases)
}

#[derive(Debug, Clone, Default, PartialEq, Eq)]
struct SkillPathAliases {
    skill_root_lines: Vec<String>,
}

struct AliasPlan {
    aliases: SkillPathAliases,
    root_aliases: HashMap<AbsolutePathBuf, String>,
    alias_root_by_path: HashMap<AbsolutePathBuf, AbsolutePathBuf>,
    table_cost: usize,
}

fn build_alias_plan(
    outcome: &SkillLoadOutcome,
    skills: &[SkillMetadata],
    budget: SkillMetadataBudget,
) -> Option<AliasPlan> {
    let skill_paths = skills
        .iter()
        .map(|skill| skill.path_to_skills_md.clone())
        .collect::<HashSet<_>>();
    let skill_root_by_path = outcome
        .skill_root_by_path
        .iter()
        .filter(|(path, _)| skill_paths.contains(*path))
        .map(|(path, root)| (path.clone(), root.clone()))
        .collect::<HashMap<_, _>>();
    let used_roots = outcome
        .skill_roots
        .iter()
        .filter(|root| {
            skill_root_by_path
                .values()
                .any(|skill_root| skill_root == *root)
        })
        .cloned()
        .collect::<Vec<_>>();
    if used_roots.is_empty() {
        return None;
    }

    let plugin_version_skill_counts =
        plugin_version_skill_counts_for_skill_roots(skill_root_by_path.values());
    let alias_root_by_skill_root = used_roots
        .iter()
        .map(|root| {
            (
                root.clone(),
                alias_root_for_skill_root(root, &plugin_version_skill_counts),
            )
        })
        .collect::<HashMap<_, _>>();
    let alias_roots = ordered_alias_roots(&used_roots, &alias_root_by_skill_root)?;
    let root_aliases = alias_roots
        .iter()
        .enumerate()
        .map(|(index, alias_root)| (alias_root.clone(), format!("r{index}")))
        .collect::<HashMap<_, _>>();
    let alias_root_by_path = skill_root_by_path
        .iter()
        .filter_map(|(path, skill_root)| {
            alias_root_by_skill_root
                .get(skill_root)
                .map(|alias_root| (path.clone(), alias_root.clone()))
        })
        .collect::<HashMap<_, _>>();
    let skill_root_lines = build_skill_root_lines(&alias_roots);
    let table_cost = aliased_metadata_overhead_cost(budget, &skill_root_lines);

    Some(AliasPlan {
        aliases: SkillPathAliases { skill_root_lines },
        root_aliases,
        alias_root_by_path,
        table_cost,
    })
}

fn ordered_alias_roots(
    used_roots: &[AbsolutePathBuf],
    alias_root_by_skill_root: &HashMap<AbsolutePathBuf, AbsolutePathBuf>,
) -> Option<Vec<AbsolutePathBuf>> {
    let mut seen = HashSet::new();
    let mut alias_roots = Vec::new();
    for root in used_roots {
        let alias_root = alias_root_by_skill_root.get(root)?.clone();
        if seen.insert(alias_root.clone()) {
            alias_roots.push(alias_root);
        }
    }
    Some(alias_roots)
}

fn alias_root_for_skill_root(
    root: &AbsolutePathBuf,
    plugin_version_skill_counts: &HashMap<AbsolutePathBuf, usize>,
) -> AbsolutePathBuf {
    let Some(plugin_version_base) = plugin_version_base(root.as_path()) else {
        return root.clone();
    };
    let skill_count = plugin_version_skill_counts
        .get(&plugin_version_base)
        .copied()
        .unwrap_or_default();
    if skill_count > 1 {
        root.clone()
    } else {
        plugin_marketplace_base(root.as_path()).unwrap_or_else(|| root.clone())
    }
}

fn plugin_version_skill_counts_for_skill_roots<'a>(
    skill_roots: impl Iterator<Item = &'a AbsolutePathBuf>,
) -> HashMap<AbsolutePathBuf, usize> {
    let mut counts = HashMap::new();
    for root in skill_roots {
        if let Some(plugin_version_base) = plugin_version_base(root.as_path()) {
            let count = counts.entry(plugin_version_base).or_insert(0usize);
            *count = count.saturating_add(1);
        }
    }
    counts
}

fn aliased_metadata_overhead_cost(
    budget: SkillMetadataBudget,
    skill_root_lines: &[String],
) -> usize {
    let empty_skill_lines: &[String] = &[];
    let absolute_body = render_available_skills_body(&[], empty_skill_lines);
    let aliased_body = render_available_skills_body(skill_root_lines, empty_skill_lines);
    budget
        .cost(&aliased_body)
        .saturating_sub(budget.cost(&absolute_body))
}

fn build_skill_root_lines(roots: &[AbsolutePathBuf]) -> Vec<String> {
    roots
        .iter()
        .enumerate()
        .map(|(index, root)| {
            let root_str = root.to_string_lossy().replace('\\', "/");
            format!("- `r{index}` = `{root_str}`")
        })
        .collect()
}

fn plugin_marketplace_base(path: &Path) -> Option<AbsolutePathBuf> {
    let mut candidate = path;
    while let Some(parent) = candidate.parent() {
        if parent.file_name()?.to_str()? == "cache"
            && parent.parent()?.file_name()?.to_str()? == "plugins"
        {
            return AbsolutePathBuf::from_absolute_path(candidate).ok();
        }
        candidate = parent;
    }
    None
}

fn plugin_version_base(path: &Path) -> Option<AbsolutePathBuf> {
    let marketplace_base = plugin_marketplace_base(path)?;
    let mut relative_components = path
        .strip_prefix(marketplace_base.as_path())
        .ok()?
        .components();
    let plugin = match relative_components.next()? {
        Component::Normal(plugin) => plugin,
        _ => return None,
    };
    let version = match relative_components.next()? {
        Component::Normal(version) => version,
        _ => return None,
    };
    AbsolutePathBuf::from_absolute_path(marketplace_base.join(plugin).join(version)).ok()
}

fn render_skill_path_with_aliases(skill: &SkillMetadata, plan: &AliasPlan) -> String {
    outcome_relative_skill_path(skill, plan)
        .unwrap_or_else(|| skill.path_to_skills_md.to_string_lossy().replace('\\', "/"))
}

fn outcome_relative_skill_path(skill: &SkillMetadata, plan: &AliasPlan) -> Option<String> {
    let alias_root = plan.alias_root_by_path.get(&skill.path_to_skills_md)?;
    let alias = plan.root_aliases.get(alias_root)?;
    let relative_path = skill
        .path_to_skills_md
        .as_path()
        .strip_prefix(alias_root.as_path())
        .ok()?;
    let relative_path = relative_path.to_string_lossy().replace('\\', "/");
    Some(format!("{alias}/{relative_path}"))
}

fn aliased_render_is_better(
    aliased: &AvailableSkills,
    absolute: &AvailableSkills,
    budget: SkillMetadataBudget,
) -> bool {
    if aliased.report.included_count != absolute.report.included_count {
        return aliased.report.included_count > absolute.report.included_count;
    }
    if aliased.report.truncated_description_chars != absolute.report.truncated_description_chars {
        return aliased.report.truncated_description_chars
            < absolute.report.truncated_description_chars;
    }
    available_skills_cost(budget, aliased) < available_skills_cost(budget, absolute)
}

fn available_skills_cost(budget: SkillMetadataBudget, available: &AvailableSkills) -> usize {
    let metadata_cost = if available.skill_root_lines.is_empty() {
        0
    } else {
        aliased_metadata_overhead_cost(budget, &available.skill_root_lines)
    };
    metadata_cost.saturating_add(lines_cost(budget, &available.skill_lines))
}

fn ordered_absolute_skill_lines(skills: &[SkillMetadata]) -> Vec<SkillLine<'_>> {
    ordered_skills_for_budget(skills)
        .into_iter()
        .map(SkillLine::new)
        .collect()
}

fn ordered_skills_for_budget(skills: &[SkillMetadata]) -> Vec<&SkillMetadata> {
    let mut ordered = skills.iter().collect::<Vec<_>>();
    ordered.sort_by(|a, b| {
        prompt_scope_rank(a.scope)
            .cmp(&prompt_scope_rank(b.scope))
            .then_with(|| a.name.cmp(&b.name))
            .then_with(|| a.path_to_skills_md.cmp(&b.path_to_skills_md))
    });
    ordered
}

fn prompt_scope_rank(scope: SkillScope) -> u8 {
    match scope {
        SkillScope::System => 0,
        SkillScope::Admin => 1,
        SkillScope::Repo => 2,
        SkillScope::User => 3,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;
    use std::sync::Arc;

    use codex_utils_absolute_path::test_support::PathBufExt;
    use codex_utils_absolute_path::test_support::test_path_buf;
    use pretty_assertions::assert_eq;

    fn make_skill(name: &str, scope: SkillScope) -> SkillMetadata {
        SkillMetadata {
            name: name.to_string(),
            description: "desc".to_string(),
            short_description: None,
            interface: None,
            dependencies: None,
            policy: None,
            path_to_skills_md: test_path_buf(&format!("/tmp/{name}/SKILL.md")).abs(),
            scope,
            plugin_id: None,
        }
    }

    fn make_skill_with_description(
        name: &str,
        scope: SkillScope,
        description: &str,
    ) -> SkillMetadata {
        let mut skill = make_skill(name, scope);
        skill.description = description.to_string();
        skill
    }

    fn expected_skill_line(skill: &SkillMetadata, description: &str) -> String {
        SkillLine::new(skill).render_with_description(description)
    }

    fn normalized_path(path: &AbsolutePathBuf) -> String {
        path.to_string_lossy().replace('\\', "/")
    }

    fn outcome_with_roots(
        skills: Vec<SkillMetadata>,
        roots: Vec<AbsolutePathBuf>,
    ) -> SkillLoadOutcome {
        let skill_root_by_path = skills
            .iter()
            .filter_map(|skill| {
                roots
                    .iter()
                    .find(|root| {
                        skill
                            .path_to_skills_md
                            .as_path()
                            .starts_with(root.as_path())
                    })
                    .map(|root| (skill.path_to_skills_md.clone(), root.clone()))
            })
            .collect::<HashMap<_, _>>();
        SkillLoadOutcome {
            skills,
            skill_roots: roots,
            skill_root_by_path: Arc::new(skill_root_by_path),
            ..Default::default()
        }
    }

    fn build_available_skills_from_metadata(
        skills: &[SkillMetadata],
        budget: SkillMetadataBudget,
    ) -> Option<AvailableSkills> {
        build_available_skills_from_lines(
            ordered_absolute_skill_lines(skills),
            skills.len(),
            budget,
            SkillPathAliases::default(),
        )
    }

    #[test]
    fn skill_usage_instructions_require_complete_main_agent_reads() {
        for instructions in [
            SKILLS_HOW_TO_USE_WITH_ABSOLUTE_PATHS,
            SKILLS_HOW_TO_USE_WITH_ALIASES,
        ] {
            assert!(instructions.contains("read its `SKILL.md` completely"));
            assert!(instructions.contains("continue until EOF"));
            assert!(instructions.contains(
                "The main agent must read each required instruction or reference file itself"
            ));
            assert!(instructions.contains(
                "Do not delegate reading, summarizing, or interpreting skill instructions"
            ));
            assert!(instructions.contains(
                "Subagents may still perform task work when the selected skill allows it"
            ));
            assert!(instructions.contains(
                "Progressive disclosure applies to selecting relevant files, not partially reading a selected instruction file"
            ));
            assert!(!instructions.contains("Read only enough to follow the workflow"));
        }
    }

    #[test]
    fn default_budget_uses_two_percent_of_full_context_window() {
        assert_eq!(
            default_skill_metadata_budget(Some(200_000)),
            SkillMetadataBudget::Tokens(4_000)
        );
        assert_eq!(
            default_skill_metadata_budget(Some(99)),
            SkillMetadataBudget::Tokens(1)
        );
    }

    #[test]
    fn default_budget_falls_back_to_characters_without_context_window() {
        assert_eq!(
            default_skill_metadata_budget(/*context_window*/ None),
            SkillMetadataBudget::Characters(DEFAULT_SKILL_METADATA_CHAR_BUDGET)
        );
        assert_eq!(
            default_skill_metadata_budget(Some(-1)),
            SkillMetadataBudget::Characters(DEFAULT_SKILL_METADATA_CHAR_BUDGET)
        );
    }

    #[test]
    fn default_context_caps_descriptions_without_mutating_metadata() {
        let description = "\u{1F4A1}".repeat(MAX_DEFAULT_CONTEXT_SKILL_DESCRIPTION_CHARS + 1);
        let skill = make_skill_with_description("long-skill", SkillScope::Repo, &description);
        let expected_description = "\u{1F4A1}".repeat(
            MAX_DEFAULT_CONTEXT_SKILL_DESCRIPTION_CHARS
                - TRUNCATED_SKILL_DESCRIPTION_SUFFIX.chars().count(),
        ) + TRUNCATED_SKILL_DESCRIPTION_SUFFIX;

        let rendered = build_available_skills_from_metadata(
            std::slice::from_ref(&skill),
            SkillMetadataBudget::Characters(usize::MAX),
        )
        .expect("skill should render");

        assert_eq!(skill.description, description);
        assert_eq!(
            rendered.skill_lines,
            vec![expected_skill_line(&skill, &expected_description)]
        );
    }

    #[test]
    fn budgeted_rendering_truncates_descriptions_equally_before_omitting_skills() {
        let alpha = make_skill_with_description("alpha-skill", SkillScope::Repo, "abcdef");
        let beta = make_skill_with_description("beta-skill", SkillScope::Repo, "uvwxyz");
        let minimum_cost = SkillLine::new(&alpha)
            .minimum_cost(SkillMetadataBudget::Characters(usize::MAX))
            + SkillLine::new(&beta).minimum_cost(SkillMetadataBudget::Characters(usize::MAX));
        let budget = SkillMetadataBudget::Characters(minimum_cost + 6);

        let rendered = build_available_skills_from_metadata(&[beta.clone(), alpha.clone()], budget)
            .expect("skills should render");

        assert_eq!(rendered.report.included_count, 2);
        assert_eq!(rendered.report.omitted_count, 0);
        assert_eq!(rendered.report.truncated_description_chars, 8);
        assert_eq!(rendered.warning_message, None);
        assert_eq!(
            rendered.skill_lines,
            vec![
                expected_skill_line(&alpha, "ab"),
                expected_skill_line(&beta, "uv"),
            ]
        );
    }

    #[test]
    fn budgeted_rendering_does_not_warn_when_average_description_truncation_is_within_threshold() {
        let alpha = make_skill_with_description("alpha-skill", SkillScope::Repo, "abcdefghij");
        let beta = make_skill_with_description("beta-skill", SkillScope::Repo, "uvwxyzabcd");
        let minimum_cost = SkillLine::new(&alpha)
            .minimum_cost(SkillMetadataBudget::Characters(usize::MAX))
            + SkillLine::new(&beta).minimum_cost(SkillMetadataBudget::Characters(usize::MAX));
        let budget = SkillMetadataBudget::Characters(minimum_cost + 6);

        let rendered = build_available_skills_from_metadata(&[alpha, beta], budget)
            .expect("skills should render");

        assert_eq!(rendered.report.included_count, 2);
        assert_eq!(rendered.report.omitted_count, 0);
        assert_eq!(rendered.report.truncated_description_chars, 16);
        assert_eq!(rendered.report.truncated_description_count, 2);
        assert_eq!(rendered.warning_message, None);
    }

    #[test]
    fn budgeted_rendering_warns_when_average_description_truncation_exceeds_threshold() {
        let long_description = "a".repeat(250);
        let long_skill =
            make_skill_with_description("long-skill", SkillScope::Repo, &long_description);
        let empty_skill = make_skill_with_description("empty-skill", SkillScope::Repo, "");
        let minimum_cost = SkillLine::new(&long_skill)
            .minimum_cost(SkillMetadataBudget::Characters(usize::MAX))
            + SkillLine::new(&empty_skill)
                .minimum_cost(SkillMetadataBudget::Characters(usize::MAX));
        let budget = SkillMetadataBudget::Characters(minimum_cost + 49);

        let rendered = build_available_skills_from_metadata(&[long_skill, empty_skill], budget)
            .expect("skills should render");

        assert_eq!(rendered.report.total_count, 2);
        assert_eq!(rendered.report.included_count, 2);
        assert_eq!(rendered.report.omitted_count, 0);
        assert_eq!(rendered.report.truncated_description_chars, 202);
        assert_eq!(rendered.report.truncated_description_count, 1);
        assert_eq!(
            rendered.warning_message,
            Some(
                "Skill descriptions were shortened to fit the skills context budget. Codex can still see every skill, but some descriptions are shorter. Disable unused skills or plugins to leave more room for the rest."
                    .to_string()
            )
        );
    }

    #[test]
    fn budgeted_rendering_token_budget_truncation_warning_mentions_two_percent() {
        let long_description = "a".repeat(1000);
        let long_skill =
            make_skill_with_description("long-skill", SkillScope::Repo, &long_description);
        let minimum_cost =
            SkillLine::new(&long_skill).minimum_cost(SkillMetadataBudget::Tokens(usize::MAX));
        let budget = SkillMetadataBudget::Tokens(minimum_cost + 1);

        let rendered = build_available_skills_from_metadata(&[long_skill], budget)
            .expect("skills should render");

        assert_eq!(
            rendered.warning_message,
            Some(SKILL_DESCRIPTION_TRUNCATED_WARNING_WITH_PERCENT.to_string())
        );
    }

    #[test]
    fn budgeted_rendering_redistributes_unused_description_budget() {
        let short = make_skill_with_description("short-skill", SkillScope::Repo, "x");
        let long = make_skill_with_description("long-skill", SkillScope::Repo, "abcdefghi");
        let minimum_cost = SkillLine::new(&short)
            .minimum_cost(SkillMetadataBudget::Characters(usize::MAX))
            + SkillLine::new(&long).minimum_cost(SkillMetadataBudget::Characters(usize::MAX));
        let budget = SkillMetadataBudget::Characters(minimum_cost + 11);

        let rendered = build_available_skills_from_metadata(&[short.clone(), long.clone()], budget)
            .expect("skills should render");

        assert_eq!(rendered.report.included_count, 2);
        assert_eq!(rendered.report.omitted_count, 0);
        assert_eq!(rendered.warning_message, None);
        assert_eq!(
            rendered.skill_lines,
            vec![
                expected_skill_line(&long, "abcdefgh"),
                expected_skill_line(&short, "x"),
            ]
        );
    }

    #[test]
    fn budgeted_rendering_preserves_prompt_priority_when_minimum_lines_exceed_budget() {
        let system = make_skill("system-skill", SkillScope::System);
        let user = make_skill("user-skill", SkillScope::User);
        let repo = make_skill("repo-skill", SkillScope::Repo);
        let admin = make_skill("admin-skill", SkillScope::Admin);
        let system_cost = SkillMetadataBudget::Characters(usize::MAX)
            .cost(&format!("{}\n", SkillLine::new(&system).render_minimum()));
        let admin_cost = SkillMetadataBudget::Characters(usize::MAX)
            .cost(&format!("{}\n", SkillLine::new(&admin).render_minimum()));
        let budget = SkillMetadataBudget::Characters(system_cost + admin_cost);

        let rendered = build_available_skills_from_metadata(&[system, user, repo, admin], budget)
            .expect("skills should render");

        assert_eq!(rendered.report.included_count, 2);
        assert_eq!(rendered.report.omitted_count, 2);
        assert_eq!(
            rendered.warning_message,
            Some(
                "Exceeded skills context budget. All skill descriptions were removed and 2 additional skills were not included in the model-visible skills list."
                    .to_string()
            )
        );
        let rendered_text = rendered.skill_lines.join("\n");
        assert!(rendered_text.contains("- system-skill:"));
        assert!(rendered_text.contains("- admin-skill:"));
        assert!(!rendered_text.contains("desc"));
        assert!(!rendered_text.contains("- repo-skill:"));
        assert!(!rendered_text.contains("- user-skill:"));
    }

    #[test]
    fn budgeted_rendering_keeps_scanning_after_oversized_entry() {
        let mut oversized = make_skill("oversized-system-skill", SkillScope::System);
        oversized.description = "desc ".repeat(100);
        let repo = make_skill("repo-skill", SkillScope::Repo);
        let repo_cost = SkillMetadataBudget::Characters(usize::MAX)
            .cost(&format!("{}\n", SkillLine::new(&repo).render_full()));
        let budget = SkillMetadataBudget::Characters(repo_cost);

        let rendered = build_available_skills_from_metadata(&[oversized, repo], budget)
            .expect("skills render");

        assert_eq!(rendered.report.included_count, 1);
        assert_eq!(rendered.report.omitted_count, 1);
        assert_eq!(
            rendered.warning_message,
            Some(
                "Exceeded skills context budget. All skill descriptions were removed and 1 additional skill was not included in the model-visible skills list."
                    .to_string()
            )
        );
        let rendered_text = rendered.skill_lines.join("\n");
        assert!(!rendered_text.contains("- oversized-system-skill:"));
        assert!(rendered_text.contains("- repo-skill:"));
    }

    #[test]
    fn outcome_rendering_omits_aliases_when_absolute_plan_has_no_budget_pressure() {
        let root = test_path_buf("/tmp/skills").abs();
        let alpha_path = root.join("alpha/SKILL.md");
        let beta_path = root.join("beta/SKILL.md");
        let outcome = outcome_with_roots(
            vec![
                skill_with_path("alpha-skill", &alpha_path),
                skill_with_path("beta-skill", &beta_path),
            ],
            vec![root],
        );

        let rendered = build_available_skills(
            &outcome,
            SkillMetadataBudget::Characters(usize::MAX),
            SkillRenderSideEffects::None,
        )
        .expect("skills should render");

        assert!(rendered.skill_root_lines.is_empty());
        assert_eq!(rendered.report.included_count, 2);
    }

    #[test]
    fn outcome_rendering_uses_aliases_when_they_allow_more_skills_to_fit() {
        let root = test_path_buf(
            "/Users/xl/.codex/plugins/cache/openai-curated/example/hash1234567890/skills-with-a-very-long-shared-prefix",
        )
        .abs();
        let skills = (0..12)
            .map(|index| {
                let name = format!("shared-root-skill-{index}");
                skill_with_path(&name, &root.join(format!("skill-{index}/SKILL.md")))
            })
            .collect::<Vec<_>>();
        let outcome = outcome_with_roots(skills.clone(), vec![root]);
        let absolute_minimum = skills.iter().fold(0usize, |cost, skill| {
            cost.saturating_add(
                SkillLine::new(skill).minimum_cost(SkillMetadataBudget::Characters(usize::MAX)),
            )
        });
        let plan = build_alias_plan(
            &outcome,
            &skills,
            SkillMetadataBudget::Characters(usize::MAX),
        )
        .expect("alias plan should build");
        let alias_minimum = skills.iter().fold(plan.table_cost, |cost, skill| {
            cost.saturating_add(
                SkillLine::with_path(skill, render_skill_path_with_aliases(skill, &plan))
                    .minimum_cost(SkillMetadataBudget::Characters(usize::MAX)),
            )
        });
        assert!(
            alias_minimum < absolute_minimum,
            "test fixture should make aliases cheaper"
        );

        let rendered = build_available_skills(
            &outcome,
            SkillMetadataBudget::Characters(alias_minimum),
            SkillRenderSideEffects::None,
        )
        .expect("skills should render");

        assert_eq!(rendered.report.included_count, skills.len());
        assert_eq!(rendered.report.omitted_count, 0);
        assert_eq!(
            rendered.skill_root_lines,
            vec![format!(
                "- `r0` = `{}`",
                normalized_path(
                    &test_path_buf(
                        "/Users/xl/.codex/plugins/cache/openai-curated/example/hash1234567890/skills-with-a-very-long-shared-prefix"
                    )
                    .abs()
                )
            )]
        );
        let rendered_text = rendered.skill_lines.join("\n");
        assert!(rendered_text.contains("r0/skill-0/SKILL.md"));
        assert!(rendered_text.contains("r0/skill-11/SKILL.md"));
    }

    #[test]
    fn outcome_rendering_uses_marketplace_root_for_single_skill_plugin_versions() {
        let github_root =
            test_path_buf("/Users/xl/.codex/plugins/cache/openai-curated/github/hash123/skills")
                .abs();
        let marketplace_root = test_path_buf("/Users/xl/.codex/plugins/cache/openai-curated").abs();
        let github = skill_with_path("github:gh-fix-ci", &github_root.join("gh-fix-ci/SKILL.md"));
        let outcome = outcome_with_roots(vec![github.clone()], vec![github_root.clone()]);
        let plan = build_alias_plan(
            &outcome,
            &[github],
            SkillMetadataBudget::Characters(usize::MAX),
        )
        .expect("alias plan should build");

        assert_eq!(
            plan.aliases.skill_root_lines,
            vec![format!("- `r0` = `{}`", normalized_path(&marketplace_root))]
        );
        assert_eq!(
            render_skill_path_with_aliases(
                &skill_with_path("github:gh-fix-ci", &github_root.join("gh-fix-ci/SKILL.md")),
                &plan
            ),
            "r0/github/hash123/skills/gh-fix-ci/SKILL.md"
        );
    }

    #[test]
    fn outcome_rendering_uses_skill_root_for_multiple_skills_in_one_plugin_version() {
        let github_root =
            test_path_buf("/Users/xl/.codex/plugins/cache/openai-curated/github/hash123/skills")
                .abs();
        let fix_ci = skill_with_path("github:gh-fix-ci", &github_root.join("gh-fix-ci/SKILL.md"));
        let yeet = skill_with_path("github:yeet", &github_root.join("yeet/SKILL.md"));
        let outcome = outcome_with_roots(
            vec![fix_ci.clone(), yeet.clone()],
            vec![github_root.clone()],
        );
        let plan = build_alias_plan(
            &outcome,
            &[fix_ci, yeet],
            SkillMetadataBudget::Characters(usize::MAX),
        )
        .expect("alias plan should build");

        assert_eq!(
            plan.aliases.skill_root_lines,
            vec![format!("- `r0` = `{}`", normalized_path(&github_root))]
        );
        assert_eq!(
            render_skill_path_with_aliases(
                &skill_with_path("github:gh-fix-ci", &github_root.join("gh-fix-ci/SKILL.md")),
                &plan
            ),
            "r0/gh-fix-ci/SKILL.md"
        );
        assert_eq!(
            render_skill_path_with_aliases(
                &skill_with_path("github:yeet", &github_root.join("yeet/SKILL.md")),
                &plan
            ),
            "r0/yeet/SKILL.md"
        );
    }

    #[test]
    fn outcome_rendering_counts_plugin_version_skills_before_budget_omission() {
        let root = test_path_buf(
            "/Users/xl/.codex/plugins/cache/openai-curated/example/hash1234567890/skills-with-a-very-long-shared-prefix",
        )
        .abs();
        let alpha = skill_with_path("alpha-skill", &root.join("alpha/SKILL.md"));
        let beta = skill_with_path("beta-skill", &root.join("beta/SKILL.md"));
        let outcome = outcome_with_roots(vec![alpha.clone(), beta.clone()], vec![root.clone()]);
        let plan = build_alias_plan(
            &outcome,
            &[alpha.clone(), beta.clone()],
            SkillMetadataBudget::Characters(usize::MAX),
        )
        .expect("alias plan should build");
        let alpha_cost = SkillMetadataBudget::Characters(usize::MAX).cost(&format!(
            "{}\n",
            SkillLine::with_path(&alpha, render_skill_path_with_aliases(&alpha, &plan))
                .render_minimum()
        ));
        let rendered = build_aliased_available_skills(
            &outcome,
            &[alpha, beta],
            SkillMetadataBudget::Characters(plan.table_cost + alpha_cost),
        )
        .expect("skills should render");

        assert_eq!(rendered.report.included_count, 1);
        assert_eq!(
            rendered.skill_root_lines,
            vec![format!("- `r0` = `{}`", normalized_path(&root))]
        );
        assert_eq!(
            rendered.skill_lines,
            vec!["- alpha-skill: (file: r0/alpha/SKILL.md)"]
        );
    }

    #[test]
    fn outcome_rendering_uses_each_skill_root_for_multiple_roots_in_one_plugin_version() {
        let skills_root =
            test_path_buf("/Users/xl/.codex/plugins/cache/openai-curated/github/hash123/skills")
                .abs();
        let extra_root = test_path_buf(
            "/Users/xl/.codex/plugins/cache/openai-curated/github/hash123/extra-skills",
        )
        .abs();
        let fix_ci = skill_with_path("github:gh-fix-ci", &skills_root.join("gh-fix-ci/SKILL.md"));
        let yeet = skill_with_path("github:yeet", &extra_root.join("yeet/SKILL.md"));
        let outcome = outcome_with_roots(
            vec![fix_ci.clone(), yeet.clone()],
            vec![skills_root.clone(), extra_root.clone()],
        );
        let plan = build_alias_plan(
            &outcome,
            &[fix_ci, yeet],
            SkillMetadataBudget::Characters(usize::MAX),
        )
        .expect("alias plan should build");

        assert_eq!(
            plan.aliases.skill_root_lines,
            vec![
                format!("- `r0` = `{}`", normalized_path(&skills_root)),
                format!("- `r1` = `{}`", normalized_path(&extra_root)),
            ]
        );
        assert_eq!(
            render_skill_path_with_aliases(
                &skill_with_path("github:gh-fix-ci", &skills_root.join("gh-fix-ci/SKILL.md")),
                &plan
            ),
            "r0/gh-fix-ci/SKILL.md"
        );
        assert_eq!(
            render_skill_path_with_aliases(
                &skill_with_path("github:yeet", &extra_root.join("yeet/SKILL.md")),
                &plan
            ),
            "r1/yeet/SKILL.md"
        );
    }

    #[test]
    fn outcome_rendering_extracts_plugin_marketplace_root_for_multiple_plugins() {
        let github_root =
            test_path_buf("/Users/xl/.codex/plugins/cache/openai-curated/github/hash123/skills")
                .abs();
        let slack_root =
            test_path_buf("/Users/xl/.codex/plugins/cache/openai-curated/slack/hash456/skills")
                .abs();
        let marketplace_root = test_path_buf("/Users/xl/.codex/plugins/cache/openai-curated").abs();
        let github = skill_with_path("github:gh-fix-ci", &github_root.join("gh-fix-ci/SKILL.md"));
        let slack = skill_with_path(
            "slack:daily-digest",
            &slack_root.join("daily-digest/SKILL.md"),
        );
        let outcome = outcome_with_roots(
            vec![github.clone(), slack.clone()],
            vec![github_root.clone(), slack_root.clone()],
        );
        let plan = build_alias_plan(
            &outcome,
            &[github, slack],
            SkillMetadataBudget::Characters(usize::MAX),
        )
        .expect("alias plan should build");

        assert_eq!(
            plan.aliases.skill_root_lines,
            vec![format!("- `r0` = `{}`", normalized_path(&marketplace_root))]
        );
        assert_eq!(
            render_skill_path_with_aliases(
                &skill_with_path("github:gh-fix-ci", &github_root.join("gh-fix-ci/SKILL.md")),
                &plan
            ),
            "r0/github/hash123/skills/gh-fix-ci/SKILL.md"
        );
        assert_eq!(
            render_skill_path_with_aliases(
                &skill_with_path(
                    "slack:daily-digest",
                    &slack_root.join("daily-digest/SKILL.md")
                ),
                &plan
            ),
            "r0/slack/hash456/skills/daily-digest/SKILL.md"
        );
    }

    #[test]
    fn outcome_rendering_uses_one_marketplace_root_for_multiple_plugin_versions() {
        let skills_root =
            test_path_buf("/Users/xl/.codex/plugins/cache/openai-curated/github/hash123/skills")
                .abs();
        let extra_root = test_path_buf(
            "/Users/xl/.codex/plugins/cache/openai-curated/github/hash456/extra-skills",
        )
        .abs();
        let marketplace_root = test_path_buf("/Users/xl/.codex/plugins/cache/openai-curated").abs();
        let fix_ci = skill_with_path("github:gh-fix-ci", &skills_root.join("gh-fix-ci/SKILL.md"));
        let yeet = skill_with_path("github:yeet", &extra_root.join("yeet/SKILL.md"));
        let outcome = outcome_with_roots(
            vec![fix_ci.clone(), yeet.clone()],
            vec![skills_root.clone(), extra_root.clone()],
        );
        let plan = build_alias_plan(
            &outcome,
            &[fix_ci, yeet],
            SkillMetadataBudget::Characters(usize::MAX),
        )
        .expect("alias plan should build");

        assert_eq!(
            plan.aliases.skill_root_lines,
            vec![format!("- `r0` = `{}`", normalized_path(&marketplace_root))]
        );
        assert_eq!(
            render_skill_path_with_aliases(
                &skill_with_path("github:gh-fix-ci", &skills_root.join("gh-fix-ci/SKILL.md")),
                &plan
            ),
            "r0/github/hash123/skills/gh-fix-ci/SKILL.md"
        );
        assert_eq!(
            render_skill_path_with_aliases(
                &skill_with_path("github:yeet", &extra_root.join("yeet/SKILL.md")),
                &plan
            ),
            "r0/github/hash456/extra-skills/yeet/SKILL.md"
        );
    }

    fn skill_with_path(name: &str, path: &AbsolutePathBuf) -> SkillMetadata {
        let mut skill = make_skill(name, SkillScope::User);
        skill.path_to_skills_md = path.clone();
        skill
    }
}
```

### `codex-rs/core-skills/src/skill_instructions.rs`

```rust
use codex_context_fragments::ContextualUserFragment;

use crate::injection::SkillInjection;

#[derive(Debug, Clone, PartialEq)]
pub struct SkillInstructions {
    name: String,
    path: String,
    contents: String,
}

impl From<&SkillInjection> for SkillInstructions {
    fn from(skill: &SkillInjection) -> Self {
        Self {
            name: skill.name.clone(),
            path: skill.path.clone(),
            contents: skill.contents.clone(),
        }
    }
}

impl ContextualUserFragment for SkillInstructions {
    fn role(&self) -> &'static str {
        "user"
    }

    fn markers(&self) -> (&'static str, &'static str) {
        Self::type_markers()
    }

    fn type_markers() -> (&'static str, &'static str) {
        ("<skill>", "</skill>")
    }

    fn body(&self) -> String {
        format!(
            "\n<name>{}</name>\n<path>{}</path>\n{}\n",
            self.name, self.path, self.contents
        )
    }
}
```

### `codex-rs/prompts/src/permissions_instructions.rs`

```rust
use codex_context_fragments::ContextualUserFragment;
use codex_execpolicy::Policy;
use codex_protocol::config_types::ApprovalsReviewer;
use codex_protocol::config_types::SandboxMode;
use codex_protocol::models::PermissionProfile;
use codex_protocol::models::format_allow_prefixes;
use codex_protocol::openai_models::ApprovalMessages;
use codex_protocol::openai_models::PermissionMessages;
use codex_protocol::permissions::FileSystemSandboxPolicy;
use codex_protocol::permissions::NetworkSandboxPolicy;
use codex_protocol::protocol::AskForApproval;
use codex_protocol::protocol::GranularApprovalConfig;
use codex_protocol::protocol::NetworkAccess;
use codex_protocol::protocol::WritableRoot;
use codex_utils_template::Template;
use std::path::Path;
use std::sync::LazyLock;

const APPROVAL_POLICY_NEVER: &str =
    include_str!("../templates/permissions/approval_policy/never.md");
const APPROVAL_POLICY_UNLESS_TRUSTED: &str =
    include_str!("../templates/permissions/approval_policy/unless_trusted.md");
const APPROVAL_POLICY_ON_REQUEST_RULE: &str =
    include_str!("../templates/permissions/approval_policy/on_request.md");
const APPROVAL_POLICY_ON_REQUEST_RULE_REQUEST_PERMISSION: &str =
    include_str!("../templates/permissions/approval_policy/on_request_rule_request_permission.md");
const AUTO_REVIEW_APPROVAL_SUFFIX: &str = "`approvals_reviewer` is `auto_review`: Sandbox escalations with require_escalated will be reviewed for compliance with the policy. If a rejection happens, you should proceed only with a materially safer alternative, or inform the user of the risk and send a final message to ask for approval.";
const NETWORK_ACCESS_PLACEHOLDER: &str = "{{ network_access }}";

const SANDBOX_MODE_DANGER_FULL_ACCESS: &str =
    include_str!("../templates/permissions/sandbox_mode/danger_full_access.md");
const SANDBOX_MODE_WORKSPACE_WRITE: &str =
    include_str!("../templates/permissions/sandbox_mode/workspace_write.md");
const SANDBOX_MODE_READ_ONLY: &str =
    include_str!("../templates/permissions/sandbox_mode/read_only.md");

static SANDBOX_MODE_DANGER_FULL_ACCESS_TEMPLATE: LazyLock<Template> = LazyLock::new(|| {
    Template::parse(SANDBOX_MODE_DANGER_FULL_ACCESS.trim_end())
        .unwrap_or_else(|err| panic!("danger-full-access sandbox template must parse: {err}"))
});
static SANDBOX_MODE_WORKSPACE_WRITE_TEMPLATE: LazyLock<Template> = LazyLock::new(|| {
    Template::parse(SANDBOX_MODE_WORKSPACE_WRITE.trim_end())
        .unwrap_or_else(|err| panic!("workspace-write sandbox template must parse: {err}"))
});
static SANDBOX_MODE_READ_ONLY_TEMPLATE: LazyLock<Template> = LazyLock::new(|| {
    Template::parse(SANDBOX_MODE_READ_ONLY.trim_end())
        .unwrap_or_else(|err| panic!("read-only sandbox template must parse: {err}"))
});

struct PermissionsPromptConfig<'a> {
    approval_policy: AskForApproval,
    approvals_reviewer: ApprovalsReviewer,
    approval_messages: Option<&'a ApprovalMessages>,
    permission_messages: Option<&'a PermissionMessages>,
    exec_policy: &'a Policy,
    exec_permission_approvals_enabled: bool,
    request_permissions_tool_enabled: bool,
}

#[derive(Debug, Clone, PartialEq)]
/// Developer instructions that describe the active sandbox and approval policy.
pub struct PermissionsInstructions {
    text: String,
}

#[derive(Debug, Clone, Copy)]
pub struct ApprovalPromptContext<'a> {
    reviewer: ApprovalsReviewer,
    messages: Option<&'a ApprovalMessages>,
    permission_messages: Option<&'a PermissionMessages>,
}

impl<'a> ApprovalPromptContext<'a> {
    pub fn new(
        reviewer: ApprovalsReviewer,
        messages: Option<&'a ApprovalMessages>,
        permission_messages: Option<&'a PermissionMessages>,
    ) -> Self {
        Self {
            reviewer,
            messages,
            permission_messages,
        }
    }
}

impl PermissionsInstructions {
    /// Builds permissions instructions from the effective permission profile and approval policy.
    pub fn from_permission_profile(
        permission_profile: &PermissionProfile,
        approval_policy: AskForApproval,
        approval_context: ApprovalPromptContext<'_>,
        exec_policy: &Policy,
        cwd: &Path,
        exec_permission_approvals_enabled: bool,
        request_permissions_tool_enabled: bool,
    ) -> Self {
        let file_system_sandbox_policy = permission_profile.file_system_sandbox_policy();
        let (sandbox_mode, writable_roots) =
            sandbox_prompt_from_policy(&file_system_sandbox_policy, cwd);

        Self::from_permissions_with_network_and_denied_reads(
            sandbox_mode,
            network_access_from_policy(permission_profile.network_sandbox_policy()),
            PermissionsPromptConfig {
                approval_policy,
                approvals_reviewer: approval_context.reviewer,
                approval_messages: approval_context.messages,
                permission_messages: approval_context.permission_messages,
                exec_policy,
                exec_permission_approvals_enabled,
                request_permissions_tool_enabled,
            },
            writable_roots,
            denied_reads_text(&file_system_sandbox_policy, cwd),
        )
    }

    pub fn body(&self) -> String {
        self.text.clone()
    }

    #[cfg(test)]
    fn from_permissions_with_network(
        sandbox_mode: SandboxMode,
        network_access: NetworkAccess,
        config: PermissionsPromptConfig<'_>,
        writable_roots: Option<Vec<WritableRoot>>,
    ) -> Self {
        Self::from_permissions_with_network_and_denied_reads(
            sandbox_mode,
            network_access,
            config,
            writable_roots,
            /*denied_reads*/ None,
        )
    }

    fn from_permissions_with_network_and_denied_reads(
        sandbox_mode: SandboxMode,
        network_access: NetworkAccess,
        config: PermissionsPromptConfig<'_>,
        writable_roots: Option<Vec<WritableRoot>>,
        denied_reads: Option<String>,
    ) -> Self {
        let mut text = String::new();
        let sandbox = sandbox_text(sandbox_mode, network_access, config.permission_messages);
        if !sandbox.is_empty() {
            append_section(&mut text, &sandbox);
        }
        append_section(
            &mut text,
            &approval_text(
                config.approval_policy,
                config.approvals_reviewer,
                config.approval_messages,
                config.exec_policy,
                config.exec_permission_approvals_enabled,
                config.request_permissions_tool_enabled,
            ),
        );
        if let Some(writable_roots) = writable_roots_text(writable_roots) {
            append_section(&mut text, &writable_roots);
        }
        if let Some(denied_reads) = denied_reads {
            append_section(&mut text, &denied_reads);
        }
        if !text.ends_with('\n') {
            text.push('\n');
        }
        Self { text }
    }
}

impl ContextualUserFragment for PermissionsInstructions {
    fn role(&self) -> &'static str {
        "developer"
    }

    fn markers(&self) -> (&'static str, &'static str) {
        Self::type_markers()
    }

    fn type_markers() -> (&'static str, &'static str) {
        ("<permissions instructions>", "</permissions instructions>")
    }

    fn body(&self) -> String {
        PermissionsInstructions::body(self)
    }
}

fn sandbox_prompt_from_policy(
    file_system_policy: &FileSystemSandboxPolicy,
    cwd: &Path,
) -> (SandboxMode, Option<Vec<WritableRoot>>) {
    if file_system_policy.has_full_disk_write_access() {
        return (SandboxMode::DangerFullAccess, None);
    }

    let writable_roots = file_system_policy.get_writable_roots_with_cwd(cwd);
    if writable_roots.is_empty() {
        (SandboxMode::ReadOnly, None)
    } else {
        (SandboxMode::WorkspaceWrite, Some(writable_roots))
    }
}

fn network_access_from_policy(network_policy: NetworkSandboxPolicy) -> NetworkAccess {
    if network_policy.is_enabled() {
        NetworkAccess::Enabled
    } else {
        NetworkAccess::Restricted
    }
}

fn append_section(text: &mut String, section: &str) {
    if !text.ends_with('\n') {
        text.push('\n');
    }
    text.push_str(section);
}

fn approval_text(
    approval_policy: AskForApproval,
    approvals_reviewer: ApprovalsReviewer,
    approval_messages: Option<&ApprovalMessages>,
    exec_policy: &Policy,
    exec_permission_approvals_enabled: bool,
    request_permissions_tool_enabled: bool,
) -> String {
    if let Some(approval_messages) = approval_messages {
        let selected = match &approval_policy {
            AskForApproval::OnRequest => match approvals_reviewer {
                ApprovalsReviewer::User => approval_messages.on_request.as_ref(),
                ApprovalsReviewer::AutoReview => approval_messages.on_request_auto_review.as_ref(),
            },
            AskForApproval::Never => approval_messages.never.as_ref(),
            AskForApproval::UnlessTrusted => approval_messages.unless_trusted.as_ref(),
            AskForApproval::Granular(_) => None,
        };
        if let Some(selected) = selected {
            return selected.clone();
        }
    }

    let with_request_permissions_tool = |text: &str| {
        if request_permissions_tool_enabled {
            format!("{text}\n\n{}", request_permissions_tool_prompt_section())
        } else {
            text.to_string()
        }
    };
    let on_request_instructions = || {
        let on_request_rule = if exec_permission_approvals_enabled {
            APPROVAL_POLICY_ON_REQUEST_RULE_REQUEST_PERMISSION.to_string()
        } else {
            APPROVAL_POLICY_ON_REQUEST_RULE.to_string()
        };
        let mut sections = vec![on_request_rule];
        if request_permissions_tool_enabled {
            sections.push(request_permissions_tool_prompt_section().to_string());
        }
        if let Some(prefixes) = approved_command_prefixes_text(exec_policy) {
            sections.push(format!(
                "## Approved command prefixes\nThe following prefix rules have already been approved: {prefixes}"
            ));
        }
        sections.join("\n\n")
    };
    let text = match approval_policy {
        AskForApproval::Never => APPROVAL_POLICY_NEVER.to_string(),
        AskForApproval::UnlessTrusted => {
            with_request_permissions_tool(APPROVAL_POLICY_UNLESS_TRUSTED)
        }
        AskForApproval::OnRequest => on_request_instructions(),
        AskForApproval::Granular(granular_config) => granular_instructions(
            granular_config,
            exec_policy,
            exec_permission_approvals_enabled,
            request_permissions_tool_enabled,
        ),
    };

    if approvals_reviewer == ApprovalsReviewer::AutoReview
        && approval_policy != AskForApproval::Never
    {
        format!("{text}\n\n{AUTO_REVIEW_APPROVAL_SUFFIX}")
    } else {
        text
    }
}

fn sandbox_text(
    mode: SandboxMode,
    network_access: NetworkAccess,
    permission_messages: Option<&PermissionMessages>,
) -> String {
    let selected = permission_messages.and_then(|messages| match mode {
        SandboxMode::DangerFullAccess => messages.danger_full_access.as_deref(),
        SandboxMode::WorkspaceWrite => messages.workspace_write.as_deref(),
        SandboxMode::ReadOnly => messages.read_only.as_deref(),
    });
    if let Some(selected) = selected {
        if selected.is_empty() {
            return String::new();
        }
        let network_access = network_access.to_string();
        return selected.replace(NETWORK_ACCESS_PLACEHOLDER, network_access.as_str());
    }

    let template = match mode {
        SandboxMode::DangerFullAccess => &*SANDBOX_MODE_DANGER_FULL_ACCESS_TEMPLATE,
        SandboxMode::WorkspaceWrite => &*SANDBOX_MODE_WORKSPACE_WRITE_TEMPLATE,
        SandboxMode::ReadOnly => &*SANDBOX_MODE_READ_ONLY_TEMPLATE,
    };
    let network_access = network_access.to_string();
    template
        .render([("network_access", network_access.as_str())])
        .unwrap_or_else(|err| panic!("sandbox template must render: {err}"))
}

fn writable_roots_text(writable_roots: Option<Vec<WritableRoot>>) -> Option<String> {
    let mut roots = writable_roots?;
    if roots.is_empty() {
        return None;
    }
    roots.sort_by(|left, right| left.root.as_path().cmp(right.root.as_path()));

    let roots_list: Vec<String> = roots
        .iter()
        .map(|r| format!("`{}`", r.root.to_string_lossy()))
        .collect();
    Some(if roots_list.len() == 1 {
        format!(" The writable root is {}.", roots_list[0])
    } else {
        format!(" The writable roots are {}.", roots_list.join(", "))
    })
}

fn denied_reads_text(file_system_policy: &FileSystemSandboxPolicy, cwd: &Path) -> Option<String> {
    let mut entries = file_system_policy
        .get_unreadable_roots_with_cwd(cwd)
        .into_iter()
        .map(|root| format!("- path `{}`", root.to_string_lossy()))
        .collect::<Vec<_>>();
    entries.extend(
        file_system_policy
            .get_unreadable_globs_with_cwd(cwd)
            .into_iter()
            .map(|glob| format!("- glob `{glob}`")),
    );
    if entries.is_empty() {
        return None;
    }

    Some(format!(
        "## Denied filesystem reads\nThe active permission profile denies reading these paths/globs. Do not request escalation or additional permissions to read them; these denials are policy restrictions.\n{}",
        entries.join("\n")
    ))
}

fn approved_command_prefixes_text(exec_policy: &Policy) -> Option<String> {
    format_allow_prefixes(exec_policy.get_allowed_prefixes())
        .filter(|prefixes| !prefixes.is_empty())
}

fn granular_prompt_intro_text() -> &'static str {
    "# Approval Requests\n\nApproval policy is `granular`. Categories set to `false` are automatically rejected instead of prompting the user."
}

fn request_permissions_tool_prompt_section() -> &'static str {
    "# request_permissions Tool\n\nThe built-in `request_permissions` tool is available in this session. Invoke it when you need to request additional `network` or `file_system` permissions before later shell-like commands need them. Request only the specific permissions required for the task."
}

fn granular_instructions(
    granular_config: GranularApprovalConfig,
    exec_policy: &Policy,
    exec_permission_approvals_enabled: bool,
    request_permissions_tool_enabled: bool,
) -> String {
    let sandbox_approval_prompts_allowed = granular_config.allows_sandbox_approval();
    let shell_permission_requests_available =
        exec_permission_approvals_enabled && sandbox_approval_prompts_allowed;
    let request_permissions_tool_prompts_allowed =
        request_permissions_tool_enabled && granular_config.allows_request_permissions();
    let categories = [
        Some((
            granular_config.allows_sandbox_approval(),
            "`sandbox_approval`",
        )),
        Some((granular_config.allows_rules_approval(), "`rules`")),
        Some((granular_config.allows_skill_approval(), "`skill_approval`")),
        request_permissions_tool_enabled.then_some((
            granular_config.allows_request_permissions(),
            "`request_permissions`",
        )),
        Some((
            granular_config.allows_mcp_elicitations(),
            "`mcp_elicitations`",
        )),
    ];
    let prompted_categories = categories
        .iter()
        .flatten()
        .filter(|&&(is_allowed, _)| is_allowed)
        .map(|&(_, category)| format!("- {category}"))
        .collect::<Vec<_>>();
    let rejected_categories = categories
        .iter()
        .flatten()
        .filter(|&&(is_allowed, _)| !is_allowed)
        .map(|&(_, category)| format!("- {category}"))
        .collect::<Vec<_>>();

    let mut sections = vec![granular_prompt_intro_text().to_string()];

    if !prompted_categories.is_empty() {
        sections.push(format!(
            "These approval categories may still prompt the user when needed:\n{}",
            prompted_categories.join("\n")
        ));
    }
    if !rejected_categories.is_empty() {
        sections.push(format!(
            "These approval categories are automatically rejected instead of prompting the user:\n{}",
            rejected_categories.join("\n")
        ));
    }

    if shell_permission_requests_available {
        sections.push(APPROVAL_POLICY_ON_REQUEST_RULE_REQUEST_PERMISSION.to_string());
    }

    if request_permissions_tool_prompts_allowed {
        sections.push(request_permissions_tool_prompt_section().to_string());
    }

    if let Some(prefixes) = approved_command_prefixes_text(exec_policy) {
        sections.push(format!(
            "## Approved command prefixes\nThe following prefix rules have already been approved: {prefixes}"
        ));
    }

    sections.join("\n\n")
}

#[cfg(test)]
#[path = "permissions_instructions_tests.rs"]
mod permissions_instructions_tests;
```

### `codex-rs/protocol/src/protocol.rs` tag constants

```rust
/// Open/close tags for special context blocks. Used across crates to avoid duplicated hardcoded
/// strings.
pub const USER_INSTRUCTIONS_OPEN_TAG: &str = "<user_instructions>";
pub const USER_INSTRUCTIONS_CLOSE_TAG: &str = "</user_instructions>";
pub const ENVIRONMENT_CONTEXT_OPEN_TAG: &str = "<environment_context>";
pub const ENVIRONMENT_CONTEXT_CLOSE_TAG: &str = "</environment_context>";
pub const ENVIRONMENTS_INSTRUCTIONS_OPEN_TAG: &str = "<environments_instructions>";
pub const ENVIRONMENTS_INSTRUCTIONS_CLOSE_TAG: &str = "</environments_instructions>";
pub const APPS_INSTRUCTIONS_OPEN_TAG: &str = "<apps_instructions>";
pub const APPS_INSTRUCTIONS_CLOSE_TAG: &str = "</apps_instructions>";
pub const SKILLS_INSTRUCTIONS_OPEN_TAG: &str = "<skills_instructions>";
pub const SKILLS_INSTRUCTIONS_CLOSE_TAG: &str = "</skills_instructions>";
pub const PLUGINS_INSTRUCTIONS_OPEN_TAG: &str = "<plugins_instructions>";
pub const PLUGINS_INSTRUCTIONS_CLOSE_TAG: &str = "</plugins_instructions>";
pub const COLLABORATION_MODE_OPEN_TAG: &str = "<collaboration_mode>";
pub const COLLABORATION_MODE_CLOSE_TAG: &str = "</collaboration_mode>";
pub const MULTI_AGENT_MODE_OPEN_TAG: &str = "<multi_agent_mode>";
pub const MULTI_AGENT_MODE_CLOSE_TAG: &str = "</multi_agent_mode>";
pub const REALTIME_CONVERSATION_OPEN_TAG: &str = "<realtime_conversation>";
pub const REALTIME_CONVERSATION_CLOSE_TAG: &str = "</realtime_conversation>";
pub const CONTEXT_WINDOW_OPEN_TAG: &str = "<context_window>";
pub const CONTEXT_WINDOW_CLOSE_TAG: &str = "</context_window>";
pub const CONTEXT_WINDOW_GUIDANCE_OPEN_TAG: &str = "<context_window_guidance>";
pub const CONTEXT_WINDOW_GUIDANCE_CLOSE_TAG: &str = "</context_window_guidance>";
pub const USER_MESSAGE_BEGIN: &str = "## My request for Codex:";
```
