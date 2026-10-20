# Model-facing context authored outside psyche-context, mind-context, field-context

Gathered 2026-10-16 by a read subflow of d68c82. Every entry was witnessed by reading the named file. The "Belongs" column is the subflow's own inference, not a ruling. P = psyche-context, M = mind-context, F = field-context. Revisions read: Curriculum origin/main af528cd (the local working copy is detached and dirty), flow ac6ab64, messenger-clj 85e71b1, nexus ec097e3.

## A. Primary files the harness loads by itself

1. `/home/li/primary/CLAUDE.md`: Claude project instructions, so every Claude main flow and subagent in Primary gets it. It covers loading skills only through the Skill tool, skill variables, committing through vision-committing, searching psyche, and the "Private part" charter, which includes a whole quote of the living. Belongs: skill loading in M knowledge-claude-harness; committing is already in P vision-committing; the quote is a raw record that already lives in flows/6cc91b/vision/privateLayer.md, and the charter would go in P vision-aspects.
2. `/home/li/primary/AGENTS.md`: Codex project instructions. Same as entry 1, plus "Temporary subagent model constraint" (no Sol, Luna/xhigh default, Terra for implementation) and "Codex Instruction Overrides". The effort line conflicts with the medium-effort rule. Belongs: F compensation-temporary and compensation-default-effort; the model rows go to P vision-model-roles.
3. `/home/li/primary/NON_MANAGEMENT_AGENTS.md`: CLAUDE.md and AGENTS.md import it with @. It holds hard boundaries (repos/, path claims, generated trees, the Primary committer, no /nix/store search, no `---`, DOTOS, the Rust doctrine, ghq, Standards, the declarative OS) and the bead-ID dispatch envelope. Belongs: F compensation-edit-coordination, compensation-primary-commit and compensation-file-editing; the bead envelope goes to M operation-beads.
4. `/home/li/primary/NON_IDEAL_AGENTS.md`: nothing that loads automatically imports it. It holds stale rules for Luna xhigh, Terra and Protos compaction. Belongs: F compensation-temporary, or retire it.

## B. Main-flow system prompt and its reminders (Primary tools/)

5. `tools/main-flow-mode/system-prompt.md`: the base of every main-flow system prompt. Claude gets it through `--system-prompt-file`, OpenCode as its agent prompt, and claude-native-seat-refresh as its main-flow prompt. Gist: the main flow delegates all bounded work, runs a shell only for its own writes, protects its context and never blocks. It is a drifted copy of P intent-main-flow (paragraph 2 differs), and the Psyche system list also appends intent-main-flow, so Psyche seats get two versions. Belongs: P intent-main-flow (already there; delete this copy).
6. `tools/main-flow-mode/reminder-hook.py`: the UserPromptSubmit hook sends the first 5 paragraphs of entry 5 as `additionalContext` every 20 prompts. The launcher wires it at claude-main-flow-launch.mjs:157. `reminder-hook.json` (--every 1) is not wired anywhere. Belongs: same as entry 5.
7. `tools/main-seat-roles/psyche-core-tertiary.md`: appended to the Psyche Core Tertiary system prompt (spirit-system-prompt.mjs:51). Curriculum generates it from roles.datom `main-system-psyche-core-tertiary`. Gist: on notice, read every book comment and relay each one whole as #psyche to Core Secondary, using a relay ledger. Belongs: M operation-relaying-the-living, or F compensation-relaying-the-living.

## C. Main-flow startup (user) prompt text in config/main-flow (Primary)

8. `config/main-flow/shared.edn :first-prompt-template`: the wrapper of every main flow's first user prompt. Gist: "Your first response is a crystallization proposal on {{metaflow}} ... The secretary supplies the next bounded work after Field confirms binding." Belongs: P intent-startup-prompt.
9. `config/main-flow/shared.edn :secondary-bootstrap-context`: the brief of a Secondary that secondary-first.mjs:70 starts automatically. Gist: carry the topic as secretary and propose the first crystallization. Belongs: P intent-startup-prompt and vision-flow.
10. `config/main-flow/metaflow/Psyche-Core-Primary.edn`: its own `:first-prompt-template` and `:topic-context` for the Fable Core Primary. Gist: every section is a psyche proposal with no technical part; hold the role until Curriculum generates a startup bundle. Belongs: P vision-book and intent-startup-prompt.
11. `metaflow/Psyche-Chronos-Primary.edn` and `Psyche-Chronos-Secondary.edn :topic-context`: the Chronos design brief, a 2000-character head-start procedure, and "Claude is in low-usage mode". Belongs: the design scope to P vision-nexus; the temporary condition to F compensation-temporary or compensation-low-power.
12. `metaflow/Psyche-Communication-Primary.edn` and `Psyche-Communication-Secondary.edn :topic-context`: visualize change with minimal text and take over the book "Communicating with the living". Belongs: P vision-book.
13. `metaflow/Psyche-Flow-Primary.edn` and `Psyche-Flow-Secondary.edn :topic-context`: Flow, Nexus and Ethos are developed together, and Clojure migration is in question. These also list machine reports (`flows/d68c82/reports/clojure-migration-2026-10-14.edn`, `startup-prompt-draft.md`) under `:raw-psyche-paths`, so machine text is presented as raw psyche. Belongs: P vision-flow; move the reports out of raw-psyche-paths.
14. `metaflow/Mind-Core-Secondary.edn :topic-context`: the Core secretary role and a no-duplicate-writer rule. Belongs: F compensation-main-flow.
15. `metaflow/Mind-Prototyping-Primary.edn` and `Mind-Prototyping-Secondary.edn :topic-context`: these embed the living's STT words verbatim ("I want to move away. Let's get Mind Astra ...") with relayed orders from Core. That is psyche data stored in launch config. Belongs: the words are raw records in flows/*/vision (P vision-clojure once crystallized); the orders go in the per-launch brief.
16. `metaflow/Field-Illustrator-Tertiary.edn :topic-context`: SVG illustration rules, and a note that the old box-and-arrow rule is void. Belongs: M operation-flashbook-illustration and F compensation-flashbook-illustration. Note that it contradicts the figure rules carried by P vision-book in this seat's own system prompt.
17. `metaflow/Field-Publisher-Quaternary.edn :topic-context`: publisher duties, an illustrator exception, and a publish gate ("every section is a proposal ..."). Belongs: M operation-book and P vision-book.
18. Module selection in `psyche.edn`, `mind.edn`, `field.edn` (`:modules :system/:user`) and in each metaflow's `:modules` and `:user-modules`. These are not text, but they decide which modules reach each prompt. Repository routing is hard-coded at launch-config.mjs:63 and spirit-system-prompt.mjs:27. Belongs: Flow's typed configuration (P vision-flow).

## D. Text hard-coded in Primary launchers and hooks

19. `tools/native-worker-launch.mjs:104`: the first prompt of a Codex worker, before its brief. Gist: "You are a native <model> implementation worker. Do not claim a new Flow ID ... Do not spawn a Sol collaboration child." Belongs: F compensation-subflow.
20. `tools/claude-native-seat-refresh.py:701`, `role_brief`: prepends a JSON metadata line and `## Source:` blocks to the handover in the first prompt. It is framing with no rules. Belongs: P intent-startup-prompt (shape).
21. `tools/opencode-main-flow-launch.mjs:72,83`: the `# Launch brief` header and the agent description 'A main flow seat.' This is framing. Belongs: P intent-startup-prompt.
22. `tools/context-refresh-hook.mjs:108`: the `instruction` field of the refresh handover, sent by hm-send to Field Core Secondary. Gist: re-read occupancy, write a judgment-only handover, split topics, then compact or restart. Belongs: F, as a refresh compensation module; the vision of refresh goes to P vision-flow.
23. `tools/primary-committer/brief.md`: the startup brief of the Field Quaternary committer (Luna). Gist: hold PrimaryPublish, publish only through publish-selected.mjs, and handle every hook firing. Belongs: F compensation-primary-commit.
24. `tools/primary-committer/turn-end.mjs:44-48`: the Stop hook sends instruction prose to the committer by hm-send. Gist: "Read this firing session transcript ... never move the shared working copy ... Do not wake a second committer." Belongs: F compensation-primary-commit.
25. `tools/field-luna-heartbeat.mjs:55`: the prompt for `codex exec` (gpt-5.6-luna). Gist: "You are Field Luna, an operational observer ... Return JSON only." Belongs: F, as a Field observer module.
26. `tools/extractor/intelligence.py:49-55`: the Luna transcript-extractor prompt, which selects blocks, narrates them and suggests STT corrections. Belongs: M operation-transcript-search.
27. `tools/flow-message-sandbox/seats.py:27` (SEAT_PRIMER, passed as `--append-system-prompt` and `developer_instructions`) and `scenarios_late.py:14`: prompts for disposable test seats. Belongs: M operation-testing (fixture text).
28. `tools/flow-cli-poc/types.json`: `base_instruction` strings for a proof of concept. It is dormant. Belongs: retire it.

## E. Files that only a generator or brief pulls in (Primary)

29. `/home/li/primary/subagents/book.md`: Curriculum appends it as the "procedure" of `.claude/agents/book.md` (Curriculum roles.rs:132 on main). It is the book-publishing procedure. Belongs: M operation-book and F compensation-book.
30. `/home/li/primary/subagents/book-page.md`: appended in the same way to `.claude/agents/book-page.md`. It keeps the living's page. Belongs: M operation-book.
31. `/home/li/primary/subagents/book-reader.md`: book-page.md:166 tells its reader subagents to follow it. It describes how to read one transcript stretch for the page. Belongs: M operation-book.
32. `/home/li/primary/roles/codex-primary.md`, `codex-medium.md`, `codex-low.md`: old Codex seat prompts ("You are the primary Codex of the mind cluster ..."). No consumer was found. Belongs: retire them.
33. `/home/li/primary/handoffs/*.md` and `/home/li/primary/2026-09-18-152843-launch-prompt-for-the-next-primary-psyche-opus.txt`: historical pasted launch prompts. No automatic consumer. Belongs: retire them or move them to flow logs.

## F. Curriculum roles.datom (origin/main af528cd). This is every subagent definition in .claude/, .codex/ and .pi/ agents

34. `general-instructions`: "The brief is your authority. Decide what it settles; return what it does not." It goes to every agent. Belongs: F compensation-subflow.
35. `codex-skill-loading`: "Do not reload a complete pasted skill unless ..." It goes to Codex agents. Belongs: M knowledge-codex-harness and F.
36. `spirit-role`: "The purpose of AI is to extend a psyche ..." It goes to every agent. P spirit-core says "thinking machine", and the full spirit-core body is also appended, so agents get two differing versions. Belongs: P spirit-core (drop the copy).
37. `intent-role`: "Every layer carries its own context ..." It goes to every agent and duplicates P intent-context. Belongs: P intent-context.
38. `subflow-role`: remote builder only, FLOW_ID and FLOW_DIRECTORY, PROVENANCE receipt, close Beads, no stash or reset of the shared copy, no lane or log, reports only when delegated, load flow-evidence. It goes to every agent. Belongs: F compensation-subflow; the remote-builder rule is already in M operation-nix-workflow and F compensation-nix-workflow.
39. Permission `read`: "Do not edit files, commit, or push. Fetching, cloning, and tool queries are fine." It goes to read-* and explorer agents. Belongs: F compensation-subflow.
40. Six depth descriptions ("The answer is in one known place ...", "The approach has to be chosen.", and the rest): the agent `description` the caller uses to pick a subagent. Belongs: M (subflow kinds) and P vision-model-roles.
41. Agent descriptions for default, explorer, worker, tester, book and book-page. tester's description is a full procedure ("choose the procedure, fixtures, negative cases, and independent oracle ..."). Belongs: M operation-testing and operation-book.
42. `main-system-psyche-core-tertiary`: the source of entry 7. Belongs: as in entry 7.

## G. Flow repository (/git/github.com/LiGoldragon/flow)

43. `crates/flow-nexus/src/performing.rs:138`, `BRIEF_CONTINUATION`: "Launch receipt confirmed. Begin the brief in your first prompt now." It is typed into the seat after the receipt. Belongs: wording in P intent-startup-prompt; the constant stays in code.
44. `crates/flow-nexus/src/composition.rs:177-187`, the receipt footer: "When every skill has loaded, reply once with exactly FLOW_LAUNCH_RECEIPT_V2 and nothing else." It is appended to every Flow first prompt. Belongs: P intent-startup-prompt.
45. `composition.rs:635-660` (`render_claude_line`) and `673-690` (`render_claude_direct`): "Read <bundle> for your launch mode, load ... through the Skill tool in this order, then: <instruction_prompt> Sources: ...". Belongs: P intent-startup-prompt.
46. `composition.rs:699-723` (`render_body`, Codex): puts the bundle inline, adds a `# Flow launch` header (Role, Harness, Model, Effort, Herdr session, Remote control), then the instruction. Line 619 forces `$operation-main-flow`. Lines 105-125 append "Predecessor:" and "Remembered:" lines to the bundle. Belongs: P intent-startup-prompt and vision-flow.

## H. messenger-clj

47. `src/messenger_clj/core.clj:165-179`: the `#msg`/`#psyche`/`#psyches` envelope framing around every flow-to-flow prompt. It is framing with no prose. `core.clj:14` `skill-note` and `hm.py:19` `SKILL_NOTE` are tool-help text that point to stale sources ("authored messaging skills in Curriculum", "compensation-hacky-messenger"). Belongs: the pointers should name F compensation-messenger-clj.

## I. CriomOS-home (the user environment)

48. `modules/home/profiles/min/default.nix:35` `codexSkillReadDeduplicationInstruction`: written as `developer_instructions` into every Codex config (lines 51 and 78). Gist: treat a complete pasted `<skill>` block as already loaded. Belongs: M knowledge-codex-harness and F; it overlaps entry 35.
49. `owned-agents/claude-code/permission-request-hook.nix:19`: the deny message returned to the model on a PermissionRequest ("Destructive commands name their paths through guarded variables ..."). Belongs: F compensation-file-editing.

## J. Repository-local instruction files

50. `AGENTS.md` and `CLAUDE.md` in repositories under /git/github.com/LiGoldragon: 279 files, 188 of them AGENTS.md. The harness loads them when a session's working directory is that repository; Curriculum/AGENTS.md and CriomOS-home/AGENTS.md and CLAUDE.md are examples. They were counted, not read one by one. Belongs: repository-specific facts can stay; any rule goes to F or M.

Not found: no model-facing text in the nexus repository, and none in Primary `.claude/settings.json` (worktree only) or `.claude/settings.local.json`. `~/.claude/settings.json` hooks run Herdr's state script and the permission hook (entry 49). Third-party Herdr was not inspected.

## Composers that accept text from elsewhere

- `tools/claude-main-flow-launch.mjs`: `--brief` any file (:137 composeFirstPrompt, read at :303); `--system-prompt-file` any file replaces the base (:105, :300, :155); hook settings at :153-168; written at :176.
- `tools/codex-main-flow-launch.mjs`: :117 composeFirstPrompt with `--brief` (:176); system prompt :182-183; `baseInstructions` :205; `model_instructions_file` :144.
- `tools/opencode-main-flow-launch.mjs`: :68 composeFirstPrompt; :81 seatConfig; :150 fixed system-prompt.md.
- `tools/main-flow-mode/spirit-system-prompt.mjs`: :21 mainSystemModules (any `tools/main-seat-roles/<role>.md` joins SYSTEM at :51); :62 composeSpiritSystemPrompt; :73 codexModelSystemPrompt (vendor template plus modules).
- `tools/main-flow-mode/launch-config.mjs`: :57 loadLaunchConfig (any EDN in config/main-flow/metaflow); :113 firstPromptFromConfig (template, topic-context, raw-psyche paths).
- `tools/secondary-first.mjs:70`: topic-context or bootstrap context becomes the Secondary brief.
- `tools/claude-native-seat-refresh.py`: :33 main_flow_mode (`--main-flow-prompt` any file, :1004); :701 role_brief; :730 first_prompt.
- `tools/native-worker-launch.mjs:103`: promptText with `--brief-file`.
- `tools/main-flow-mode/reminder-hook.py:24`: core from `--prompt-file`.
- `tools/context-refresh-hook.mjs:104`: handover; `tools/primary-committer/turn-end.mjs:44`: committer message.
- `tools/primary-committer/seat-process.mjs:22` (`--system-prompt`), `codex-birth.mjs:24`, `restart-service.nix:25`: the committer's system prompt is a file the caller supplies.
- Curriculum `src/roles.rs` (origin/main): :40-56 `main-system-*` modules projected to tools/main-seat-roles; :71 packet (role modules from roles.datom); :132 reads `<workspace>/subagents/<name>.md`; :220 render.
- flow `crates/flow-nexus/src/composition.rs`: :738 compose takes `system_prompt_bundle_file` (any absolute file, checked at :450) and `instruction_prompt` from the Start request; :600 render_native_head; :635 render_claude_line; :699 render_body; `performing.rs:138`.
- CriomOS-home `modules/home/profiles/min/default.nix:35,51,78`.

## Sources

Files read directly: the paths named in each entry. Commands: `git show origin/main:roles.datom` and `git show origin/main:src/roles.rs` in Curriculum; `ls -d /git/github.com/LiGoldragon/*/AGENTS.md */CLAUDE.md | wc -l`; a diff of tools/main-flow-mode/system-prompt.md against psyche-context/skills/intent-main-flow.md; greps for duplicated sentences across the three skill directories.
