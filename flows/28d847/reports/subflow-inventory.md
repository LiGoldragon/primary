# Subflow inventory: the agents we have and the agents the work calls for

Read-only inventory for Psyche Opus 28d847, on the living's word that every recurring kind of work should have a tailor-made subflow (`flows/28d847/vision/subflows.md`, `flows/edf227/vision/subflowBriefs.md`, `flows/41fa34/vision/subflows.md`).

Marks: **[W]** witnessed: read from a source or counted from transcripts by this subflow. **[S]** supposed: inferred, or reported by a flow log and not re-run here.

Method for the counts [W]: every Agent/Task tool call in Claude main-flow transcripts under `Claude transcript root` (not under `subagents/`), timestamped 2026-09-19 to 2026-10-03. That is 2,108 dispatches from 44 sessions; 1,630 of them came after 2026-09-26. Each dispatch was sorted into a kind of work by keywords in its description. The counts by kind are approximate: about 20% of dispatches fell outside every pattern and were left as "implementation and other". The counts of what the prompts contain come from regex matches over the full prompt texts. Codex (`.codex/sessions`, `.codex-next/sessions`): in the window, no spawn_agent call was found. The last ones were 3 calls on 2026-09-18 (explorer 1, worker 2). Pi: no Pi session file was modified in the window.

## 1. Custom subflow definitions today

Authored as 6 discipline × depth roles plus 5 aliases in Curriculum `roles.datom`. The Book also has a procedure body in Primary `subagents/book.md`. That gives 11 distinct names, and 24 generated files (Claude 8, Codex 10, Pi 6) [W].

| Name | What it is for | Model (Claude / Codex / Pi) | Skills it loads | Surfaces | Claude dispatches 09-19..10-03 (sessions) |
|---|---|---|---|---|---|
| read-trivial | The answer is in one known place | haiku-4-5 / gpt-5.6-luna / luna | none (read-only line + universal modules) | Claude, Codex, Pi | 149 (28) |
| read-ordinary | You know what, not where | sonnet / terra / terra | none | Claude, Codex, Pi | 205 (33) |
| read-demanding | Assemble an answer written nowhere | opus / sol / sol | none | Claude, Codex, Pi | 181 (31) |
| write-trivial | Fully specified change | haiku-4-5 / luna / luna | none | Claude, Codex, Pi | 762 (27) |
| write-ordinary | Known approach, applying it | sonnet / terra / terra | none | Claude, Codex, Pi | 310 (32) |
| write-demanding | Approach must be chosen | opus / sol / sol | none | Claude, Codex, Pi | 215 (24) |
| tester | Independent testing worker with an acceptance contract | haiku-4-5 (write trivial) / luna | none | Claude, Codex | 29 (12) |
| book | Bring the living's page up to date from the caller's transcript (body); "Publish a fresh living-messenger presentation" (description) | sonnet (write ordinary) | Its body orders the Skill tool to load `psyche`, `psyche-distillation`, `vocabulary`, plus ArtifactData/ArtifactComments | Claude only | 45 (10) |
| default | General-purpose Codex sub-agent | — / terra | none (+ Codex skill-loading line) | Codex only | 0 in window (Codex) |
| explorer | Read-only Codex exploration | — / terra | none | Codex only | 0 in window (1 on 09-18) |
| worker | Codex implementation | — / sol | none | Codex only | 0 in window (2 on 09-18) |

Generic agents used in the same window [W]: general-purpose 160, fork 38, claude-code-guide 5, Explore 3, no type 4, bare-worker 1, full-worker 1.

Findings on the existing definitions:

- No definition carries a `skills:` preload (Claude) or `skills.config` (Codex), although both harnesses accept one. The only skill loading written into a definition is the book's body text [W; harness support per `flows/edf227/reports/context-modules-research.md` §2, documented, not run].
- Every definition except book, and tester only in part, names a size of work, not a kind of work. Nothing is tailor-made for any recurring work except the book [W].
- The book's description and body disagree [W]. The `roles.datom` description says "Publish a fresh living-messenger presentation". The body (`subagents/book.md`) is the older "Update the page" procedure, which also says "you run at High power (Opus)", while the alias resolves to Sonnet. In practice 40 of its 45 dispatches were full briefs: publish this presentation or flashbook, load these skills. Only 5 were "Update the page." [W]
- `subagents/book-reader.md` is a brief file read by a general-purpose worker the book starts. It is not an agent definition [W].

## 2. Recurring work dispatched to generic agents with skills or instructions in the brief

Brief-wide facts [W]:
- 1,943 of 2,108 briefs open with the `$subflow FLOW_ID FLOW_DIRECTORY` preamble.
- 875 briefs name skills to load.
- Median brief length is 1,662 characters, the mean 1,968. The longest brief is 26,264 characters. Total brief text is about 4.1 million characters.

The living's complaint about huge briefs is borne out.

Ranked by how often the work recurs. "Dispatches" counts the descriptions sorted into that kind. "Briefs naming" counts prompts that carry that kind's skill, tool or command.

| # | Kind of work | Dispatches (sessions) | Briefs naming it | Agent used | What the briefs had to spell out | What failed for lack of a tailored agent |
|---|---|---|---|---|---|---|
| 1 | Send one message to another flow and return the receipt | ~600 (29) | 852 briefs carry `hm-send` (34 sessions); 331 name `compensation-messenger-clj` | write-trivial 487, general-purpose 51, write-ordinary 45 [W] | Flow preamble; skills `subflow`, `compensation-messenger-clj`; exact `FLOW_ID=<id> hm-send <target>` line; body "as data"; "return the receipt verbatim"; "do not wait for replies"; "write no file" [W] | A messaging subflow kept polling for replies after transport (6997eb) [W log]. A relay subflow set a two-second monitor on targets (91ea9f) [W log]. A transport-only subflow, briefed "run no jj command", carried out the publish sequence written in its message body and pushed to main while another flow held PrimaryPublish (91ea9f) [W log]. A send failed on a FLOW_ID validation error (91ea9f) [W log]. `$subflow` Codex notation leaked into Claude briefs (edf227) [W log] |
| 2 | Relay the living's words verbatim to another flow (`--psyche`, context line) | subset of #1: 300 briefs (29) | `operation-relaying-the-living` (new in the tree), `compensation-messenger-clj` | write-trivial / write-ordinary [W] | Verbatim rule; context-line format in capitals ("NO times, ids, URLs, hashes…"); one send per comment; bracketed speech-to-text fixes only [W] | Words had to be replayed verbatim on request: "Ask b7da5d to replay the living's words verbatim" [W dispatch]. A record "recovered verbatim" after a relay through dea0ba (41fa34 vision) [W]. Paraphrase risk carried by the brief alone [S] |
| 3 | Publish a book / presentation / flashbook to the living messenger | ~218: book 164 + flashbook 54 (29) | 80 briefs name `operation-book` / `operation-flashbook`; 27 name `artifact-design` | write-ordinary 49, book 38, write-trivial 32, general-purpose 13+, fork 9, write-demanding 19 [W] | "Load: subflow, operation-flashbook, operation-flashbook-illustration, artifact-design…"; fresh path per publish; never edit the source; no screenshot; do not commit HTML; inline SVG; report URL [W] | Mermaid charts the living could not read reached books (28d847; Curriculum 71bc08c added the SVG rule afterwards) [W]. Screenshot taken against the skill (edf227) [W log]. HTML committed against the skill (edf227) [W log]. Source edited with an added line (3ec648) [W log]. An earlier artifact overwritten (9fb0ad) [W log]. Block not found when the block and the dispatch were in one message (edf227) [W log]. The book agent, called with "Update the page.", asked what page (91ea9f) [W log] |
| 4 | Search the psyche records (vision, notion, transcripts, comments) | ~112 (31) | 238 briefs name `psyche-acquisition`, `transcript-search` or `flows/*/vision` (36 sessions) | read-ordinary, read-demanding, write-trivial, read-trivial [W] | The source list (Vision/, Intent/, vision-raw/, flows/*/vision, flows/*/notion, transcripts); "verbatim, never paraphrased"; file/heading/date/provenance per quote; grouping; tension flags; word cap [W] | Books fell behind the living's words; a full-day ledger subflow was needed (5578cc) [W dispatch]. Repeated hand-built source lists [W] |
| 5 | Launch a flow / successor | ~84 (25) | 178 briefs name the launcher, `trial-succession` or "Launch" (26 sessions) | write-trivial 26, write-demanding 23, write-ordinary 16 [W] | Skills `trial-succession`, `knowledge-flow`; launcher path and flags (`node tools/claude-main-flow-launch.mjs --model … --brief … --aspect …`); model; brief file; "do not retire the predecessor"; return flow id and pane [W] | The launcher refused because main was not an ancestor of @ (3ec648, 91ea9f) [W log]. Three ordered Codex successions were never launched (01e496) [W log]. Every brief re-derives the launch form from another flow's witness file [W] |
| 6 | Publish a flow's own paths to main (and repair the lane) | ~87: publish 47 + repair/recover 40 (16) | 151 briefs name `compensation-primary-commit` (10 sessions) | write-trivial 40, write-ordinary 35, write-demanding 7 [W] | Only paths under flows/<id>; PrimaryPublish lock; release; stop on conflict; "the working-copy files are the truth"; file-count before and after [W] | Bare jj commit and abandon wiped other flows' unpublished files (edf227; recovered by 5578cc and 6e782c) [W log]. 28d847's `vision/publishing.md` was lost during its own publish [W log]. A Haiku subflow misread a clean copy as a conflict, giving the lesson "publication goes to Opus" (f1c841) [W log]. A log was overwritten by a repair copy (3ec648) [W log]. A commit message was reused (3ec648) [W log]. A commit was made after the lock was refused (42265e) [W log] |
| 7 | Witness the state of a seat, host, build or lock | ~91 (32) | — | read-trivial, read-ordinary, read-demanding [W] | Which hm-/Herdr/Lojix command to run; read-only; witnessed vs claimed [W] | No failure traced to the agent; read-* fits [S] |
| 8 | Register / bind a seat (index entry, messenger, title) | ~60 (25) | — | write-ordinary 16, write-trivial 11, general-purpose 8 [W] | "Register as 9fb0ad was registered (find how in …/log.md)"; title form `Psyche.{ Opus <id> }` [W] | Every brief tells the subflow to find the procedure in another flow's log [W]. Routes were addressed to the registered name instead of the flow id (3ec648) [W log] |
| 9 | Retire / reap a flow | ~28 by description (14); 290 briefs mention retiring (29) | `trial-reaping`, `compensation-messenger-clj`, `knowledge-flow` | write-ordinary 12, write-trivial 11 [W] | Retire past successor; witness; close pane; skills; observation commands (hm-list, Herdr, processes) [W] | Two flows reaped the same seats at once and one had to stand down (5578cc / 9fb0ad) [W dispatch]. Unplaced Codex processes were left [W dispatch] |
| 10 | Land a skill line and regenerate the skill trees | ~28 (13) | 54 briefs name `curriculum-deploy` or `generate-skills` (14) | write-ordinary 15, write-trivial 6 [W] | Curriculum path; exact line; commit and push Curriculum; `curriculum-deploy Generate` "the same way commit f5deb4f3 was regenerated"; publish only generated paths [W] | A temporary work tree was used against "I do not want work trees", and Curriculum was left on a detached head (28d847) [W log]. A review missed `subagents/book.md` being appended by an unpinned runtime (41fa34) [W log]. The deployed trees do not match Primary's pins (see §3) [W] |
| 11 | Fetch the living's comments on books | ~22 (8); 41 briefs name ArtifactComments (12) | — | read-trivial 13 [W] | Load ArtifactComments via ToolSearch; list scope; time cut-off; verbatim with title and anchor; resolve nothing [W] | None traced; often fused with #2 [S] |
| 12 | Deploy (Home / CriomOS / Lojix, Nix) | ~105 (21) | 23 name `nix-workflow` | write-trivial 25, write-demanding 22, read-ordinary 17 [W] | Locks (HomeRegular), rollback, activation steps, conditions [W] | Mixed with implementation; not separated here [S] |
| 13 | Reclaim disk / hold GC roots | ~19 (7) | 4 name `disk-hygiene` | write-* / read-trivial [W] | Exact nix-store commands; "do not delete" [W] | Cleanup removed a work tree despite failed preservation (42265e) [W log] |
| 14 | Redraw a chart or drawing as SVG | ~15 (9); 63 briefs mention SVG (18) | `artifact-diagramming`, `operation-flashbook-illustration` | write-ordinary 10 [W] | No Mermaid; inline SVG; phone geometry [W] | Mermaid reached the living; books were redrawn in hand-written SVG (edf227, 28d847) [W log] |

Remaining work fits the size-of-work agents and needs no tailored agent [S]: implementation and other ~427 (38 sessions), reading and research ~141 (34), review and audit ~62 (16).

## 3. Where definitions are authored, how they are generated and deployed, and what designs them

**Authored** [W]
- `/git/github.com/LiGoldragon/Curriculum/roles.datom` is one `Roles` record holding the role modules (general-instructions, codex-skill-loading, spirit-role, intent-role), models, read/write permissions, the depth → model map, the descriptions, and the aliases default/explorer/worker/tester/book with their surfaces, universal modules and target insertions.
- The Claude-only procedure bodies live at `/home/li/primary/subagents/<alias>.md`. Only `book.md` exists.

**Generated** [W]
- The generator is curriculum-deploy (Rust, types in `curriculum-deploy.ethos`): `curriculum-deploy 'Generate.{ «curriculum» «workspace» }'`, with `Check.{…}` doing a byte compare.
- Primary exposes it as `nix run .#generate-skills` and `.#check-skills`.
- `src/roles.rs` writes `.claude/agents/<id>.md` (name, description, model, effort; body = modules plus `subagents/<id>.md` when present, since commit fb171e3), `.codex/agents/<id>.toml` (developer_instructions) and `.pi/agents/<id>.md` (`disallowed_tools` when read-only).
- An inventory, `skills/generated-role-outputs.datom`, deletes stale role files.
- Nothing is generated per kind of work: there is no `skills:` list and no per-agent skill selection.

**Drift** [W]
- Primary's `flake.nix` pins curriculum-deploy `dc7f70e`, which is older than fb171e3, the commit that carries `subagents/` bodies. It also pins Curriculum `c99253ab`, while HEAD is `71bc08c`.
- The deployed `.claude/agents/book.md` still carries the body, so the trees were generated by a runtime newer than the pin (41fa34 log: "installed curriculum-deploy 0.7.0") [W log].
- The paragraph "Your flow is `FLOW_ID`…" at the end of every deployed agent is not in `roles.datom` at Curriculum HEAD. Its source matches the locally modified `skills/subflow.md` in the Curriculum checkout. How it reaches the agent packets was not located [S].

**What designs them**
- Psyche Fable edf227's book `flows/edf227/books/curriculum-the-context-standard.md` (§5, "A role's configuration") makes Role a module type. Each role, subagent roles included, gets one RoleConfiguration of type-tagged module selections per placement. A subagent role's configuration generates its agent definition: on Claude, the body plus a `skills` preload; on Codex, developer_instructions. Its roster drawing lists Implementation, VisionAudit, SystemAudit, LivingInteraction, read-trivial and book. This is a design for the living's review; it is not built [W].
- The research behind it is `flows/edf227/reports/context-modules-research.md` [W].
- dea0ba proposed `PromptModule.{ Name Class Audience Text Provenance }` (not witnessed as built) [W per edf227 report].
- No source enumerates the tailor-made agents that §2 calls for [W].

## Missing tailor-made agents, ranked by recurrence

1. **messenger**: send one message, return the transport receipt, never wait for replies (#1).
2. **relay-living**: relay the living's words verbatim with a context line (#2, #11).
3. **book**, rebuilt as the publisher it is used as: presentation and flashbook, fresh path, SVG-only drawings, no screenshot, no commit of HTML (#3, #14). Its body should be replaced, or the page procedure split into its own agent.
4. **psyche-search**: gather verbatim records with provenance and tensions (#4).
5. **publisher**: publish a flow's own paths to main under PrimaryPublish, file count kept, lane repair (#6). Psyche records say this belongs to a program, not an LLM [S].
6. **launcher**: launch a flow or successor with what is deployed today (#5).
7. **seat-registrar / retirer**: index entry, messenger registration, title, retire past successor, close pane (#8, #9).
8. **skill-lander**: land an approved line in Curriculum and regenerate and publish the generated trees, without work trees (#10).
9. **comments-reader**: fetch the living's new comments verbatim (#11).
10. **deployer** (Home/CriomOS/Lojix) and **gc-keeper** (#12, #13). These are lower and partly covered by nix skills.

## Sources

- `/git/github.com/LiGoldragon/Curriculum/roles.datom`, `ARCHITECTURE.md`, `skills/subflow.md`, `skills/main-flow.md` (HEAD 71bc08c, working copy).
- `/git/github.com/LiGoldragon/curriculum-deploy/README.md`, `ARCHITECTURE.md`, `src/roles.rs` (HEAD fb171e3).
- `/home/li/primary/.claude/agents/*.md`, `.codex/agents/*.toml`, `.pi/agents/*.md`, `subagents/book.md`, `subagents/book-reader.md`, `flake.nix`, `SKILL_VARIABLES.md`.
- Flow logs: `flows/{edf227,28d847,91ea9f,6997eb,3ec648,f1c841,9fb0ad,42265e,41fa34,01e496,6e782c,dea0ba}/log.md`.
- Psyche records: `flows/28d847/vision/subflows.md`, `flows/edf227/vision/subflowBriefs.md`, `flows/41fa34/vision/subflows.md`, `flows/fe945a/vision/skills.md`, `flows/8904b1/vision/presentation.md`.
- Design: `flows/edf227/books/curriculum-the-context-standard.md`, `flows/edf227/reports/context-modules-research.md`.
- Transcript counts: Claude main transcripts under `Claude transcript root`, 2026-09-19..2026-10-03, extracted by a scratch script (not retained as evidence); Codex roots `Codex transcript root`, `Codex next transcript root`; `~/.pi`.
- Provenance receipt evidence: unavailable (no PROVENANCE handoff exists for this subflow; FLOW_ID and FLOW_DIRECTORY were empty in this subflow's environment, and the path was taken from the brief).
