# Fresh harness context measurements

Measured on 2026-10-03 with Claude Code 2.1.284, installed Codex CLI 0.158.0-alpha.9, and OpenCode 1.18.16. Every included session was created for this assignment. No historical rollout supplied a figure.

Characters below mean Unicode code points; UTF-8 bytes are reported separately. Native usage is total request usage, not a token count of the system prompt alone. A field missing from a retained native record is **NOT MEASURED**. Static source sizes and behavioral marker tests are identified separately from delivered-message measurements.

Private evidence root: `/home/li/private-repos/flow-evidence/42265e/harness-context-2026-10-03/`. Alias-named Claude stream and Codex rollout copies were compared in code with their original files: MATCH. Private evidence maps retain the original native identifiers and paths; the report uses six-character session aliases. Codex aliases use the random tail rather than the shared timestamp prefix.

## Main-session base instructions

| Harness / case | Session | Base characters | UTF-8 bytes | Native input tokens | Evidence |
| --- | --- | ---: | ---: | ---: | --- |
| Codex Astra, stock base | 836616 | 21,420 | 21,428 | 15,782 | `codex/836616.jsonl`: base at line 1; usage at line 13 |
| Codex Astra, authored text in developer override | 72ce9b | 21,420 | 21,428 | 14,565 | `codex/72ce9b.jsonl`: lines 1, 3, 13 |
| Codex Astra, explicit developer marker | 80ff6f | 21,420 | 21,428 | 14,225 | `codex/80ff6f.jsonl`: lines 1, 3, 13 |
| Codex Luna low, independent CLI session | ea4858 | 17,730 | 17,766 | 11,837 | `codex/ea4858.jsonl`: lines 1, 11; **not a native collaborator** |
| Codex Astra, `model_instructions_file` replacement | d8c6e6 | 1,696 | 1,696 | 10,416 | `codex/d8c6e6.jsonl`: lines 1, 13 |
| Codex Astra, default current CLI context | 2b93b0 | 21,420 | 21,428 | 14,214 | `codex/2b93b0.jsonl`: lines 1, 13 |
| Claude stock | 30f915 | NOT MEASURED | NOT MEASURED | See usage table | `claude/30f915.jsonl`: init line 1; result line 4 |
| Claude replacement | bb5694 | NOT MEASURED | NOT MEASURED | See usage table | `claude/bb5694.jsonl`: init line 1; result line 5 |

The supplied replacement source, `tools/main-flow-mode/system-prompt.md`, measured 1,697 characters and 1,697 UTF-8 bytes. The fresh Codex replacement rollout contains exactly that text with its final newline removed. Claude received the source through `--system-prompt-file`, but its stream does not contain the delivered system-prompt body or its character count.

Replacing Codex developer instructions is different from replacing its base instructions: the developer-override case kept the stock base. The cases also have different skills-block composition and different user prompts, so the input-token differences are not an isolated measurement of replacement savings. No native file reports a system-prompt-only token count.

### Native request usage

| Codex session | Input | Cached input | Cache write | Output | Reasoning output |
| --- | ---: | ---: | ---: | ---: | ---: |
| 836616 | 15,782 | 12,288 | 0 | 7 | 0 |
| 72ce9b | 14,565 | 12,288 | 0 | 8 | 0 |
| 80ff6f | 14,225 | 12,288 | 0 | 8 | 0 |
| ea4858 | 11,837 | 9,984 | 0 | 10 | 0 |
| d8c6e6 | 10,416 | 0 | 0 | 7 | 0 |
| 2b93b0 | 14,214 | 12,288 | 0 | 10 | 0 |

| Claude session | Input | Cache creation | Cache read | Output | Reasoning output |
| --- | ---: | ---: | ---: | ---: | ---: |
| 30f915 stock | 2 | 1,795 | 531 | 13 | 0 |
| bb5694 replacement | 2 | 392 | 561 | 14 | 0 |

The Claude fields come from the result records named above. The Codex fields come from the native `token_usage_record`, not a character-to-token estimate. Claude cache fields and Codex cache fields are kept in their native categories.

## Developer messages, skills, permissions, and instruction files

Codex developer-message bodies are readable in these fresh rollouts. The table gives full message sizes, including their delimiters and any composed content.

| Session | Developer message sizes: characters / UTF-8 bytes | Evidence lines |
| --- | --- | --- |
| 836616 | 11,486 / 11,490; 2,429 / 2,429; 271 / 271 | 3, 4, 5 |
| 72ce9b | 6,142 / 6,146; 2,429 / 2,429; 271 / 271 | 3, 4, 5 |
| 80ff6f | 4,470 / 4,474; 2,429 / 2,429; 271 / 271 | 3, 4, 5 |
| ea4858 | 5,210 / 5,214 | 3 |
| d8c6e6 | 4,445 / 4,449; 2,429 / 2,429; 271 / 271 | 3, 4, 5 |
| 2b93b0 | 4,445 / 4,449; 2,429 / 2,429; 271 / 271 | 3, 4, 5 |

Within the first developer message, the explicitly delimited `skills_instructions` body measures 9,494 characters / 9,498 bytes in 836616, and 2,453 characters / 2,457 bytes in each other Codex case. This body includes catalog guidance and metadata; it is not a measurement of every skill's loaded text. The `permissions instructions` body measures 288 characters / 288 bytes in every case. These component sizes exclude the opening and closing tags. Machine extraction and comparison are retained in `codex/component-summary.json`.

The second and third developer messages are byte-identical across the five Astra main cases. This is main-to-main comparison, **not parent-to-collaborator comparison**. The fresh Codex records contain a 458-character environment-context user message, but no `AGENTS.md instructions` injection in those fixtures; this does not establish how a project instruction file reaches a collaborator. Component provenance is retained in `codex/user-injection-summary.json`.

Claude stock init lists 16 skills, 5 agents, and zero enabled tools. The custom-agent case lists 16 skills, 6 agents, and one enabled Task tool. These are emitted names/counts, not full catalog or tool-schema bodies. All included Claude init records report `permissionMode: bypassPermissions` despite the requested plan mode. Stock and replacement cases enabled no tools; the subagent case enabled Task.

The fresh Claude instruction-file case, 48a387, used its own fixture `CLAUDE.md`. Its harmless marker appears in the assistant response at `claude/48a387.jsonl`:4. This witnesses influence, not the injected file's exact placement or delivered character count.

## Subagents and configured Codex developer instructions

Claude custom-agent session 4dd14f spawned and completed one foreground Task. Its definition marker appears at `claude/4dd14f.jsonl`:6; the parent's completion appears at line 10 and native result at line 11. The supplied agent-definition source measures 148 characters / 148 bytes. That is a source measurement: the native stream does not expose the complete child system prompt, developer messages, catalog bodies, permissions composition, or instruction-file injection. Their character lengths and parent-identical portions are **NOT MEASURED**. The claim that the child receives only its definition plus two fixed paragraphs is neither confirmed nor refuted by these files.

The requested native Codex Luna collaborator could not be created: the orchestrator refused child creation at its agent thread limit. Its system/developer/catalog/permission/instruction-file measurements, parent-identical parts, and configured-developer inheritance are **NOT MEASURED**. The independent Luna CLI case is not substituted for that missing native child.

An explicit developer marker influenced the fresh Astra main case 80ff6f. The 454-character developer text selected from a separate `.codex/config.toml` was absent from the default current-CLI-context case 2b93b0; that CLI used its current CODEX_HOME context, not that separate configuration file. Neither observation determines whether the parent's configured developer instructions reach a native collaborator.

## Claude session-fork inheritance

These controls test the supported CLI session-fork shape `claude -p --resume <parent> --fork-session`; they do not test a Task subagent fork.

| Control | Fresh parent | Fresh fork | Positive parent response | Fork response | Evidence |
| --- | --- | --- | --- | --- | --- |
| Replaced parent system prompt | 397d6c | 00a7f1 | Replacement marker present | Same marker present | `claude/397d6c.jsonl`:2; `claude/00a7f1.jsonl`:4 |
| Appended parent system prompt | e1c476 | d5984d | Append marker present | Same marker present | `claude/e1c476.jsonl`:3; `claude/d5984d.jsonl`:2 |

The commands and fixture inputs are retained with the corresponding private runs. Each pair had successful native results, a private working directory, and Claude 2.1.284 init records. These controls establish behavioral inheritance of the parent replacement and append markers. They do not reveal prompt bodies or their character lengths.

## Tool schemas per request

Full request tool-schema objects are absent from the included Codex rollouts and Claude streams. Schema count and characters per request, for main and native subagent/collaborator, are **NOT MEASURED**. A tool-name list, a Task lifecycle event, or a CLI's advertised capabilities is not used as a schema-size measurement.

## OpenCode

Installed OpenCode 1.18.16 created fresh session efbcb7 with the configured free `opencode/big-pickle` provider and denied tools. The provider returned HTTP 403: `OpenCode's free tier can only be used from within OpenCode`. No authentication workaround or provider change was made.

Retained evidence: `opencode/run.jsonl`:1 and `opencode/export.json`. The export contains the user message and failed assistant record, with no system prompt, developer bodies, or request tool schemas. Its zero usage fields describe the failed request, not a measured zero-size prompt. Main and subagent measurements are **NOT MEASURED** until a supported functioning route is available.

## Findings against the supplied claims

| Claim | Fresh evidence result |
| --- | --- |
| Claude stock prompt is 15,283 characters | NOT MEASURED: stock prompt text/length is absent from the native stream. |
| Our replacement is 1,697 characters | Source file confirmed. Codex records 1,696 after final-newline stripping; Claude delivered length is NOT MEASURED. |
| Claude child gets definition plus two fixed paragraphs, not main prompt | NOT MEASURED: no complete child prompt composition in the retained stream. |
| Codex collaborator has identical 17,730-character base | NOT MEASURED for a native collaborator. Independent Luna main has 17,730; Astra main has 21,420. Do not generalize across models or substitute the independent case for a child. |
| Codex role replaces the parent's app-context developer message | NOT MEASURED: native collaborator creation was refused. |
| Configured Codex developer instructions reach a collaborator | NOT MEASURED: no native child delivery record. |
| Claude replacement and append survive a session fork | Behavioral marker controls passed for both supported session-fork cases. |

## Isolation and retained evidence

Claude fixtures used private HOME/XDG/runtime/working roots and program-only credential copies; those copied credential files were removed after the runs. No live primary seat was woken or retired. No worktree or clone was created for the measurements. Fresh native files and numeric extraction receipts are retained privately; neither credentials nor full prompts are published with this report.

Claude detailed evidence: `/home/li/private-repos/flow-evidence/42265e/claude-context-measurement-2.1.284-2026-10-03.md`. Codex machine mappings and computed summaries are retained under `codex/` in the private evidence root. The original identifiers remain machine evidence, not model-facing receipt values.
