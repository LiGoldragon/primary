# Placing table: three skill repositories

Rule: a module belongs to the aspect whose question it answers. Psyche: what is wanted and why. Mind: how a thing is done, what it is by design. Field: what runs now, what holds it together. Module types are Spirit, Intent, Vision, Notion, Knowledge and Operation; there is no Role type. psyche-skills holds spirit/ intent/ vision/ notion/, mind-skills operation/ knowledge/, field-skills operation/ knowledge/. A seat's identity module is an Operation module of its seat's aspect. Target is `<repository>/<directory>/<stem>`. Deployed name is `<type>-<stem>`; Spirit deploys as `spirit`. P4 is the first placing in Proposal 4 of «Three skill repositories and the main workspace». "= P4" means same repository as P4. "P4 silent" means P4 names no repository for the row. **DIFFERS** marks a departure, and the reason follows it.

Abbreviations: `psyche` = psyche-skills, `mind` = mind-skills, `field` = field-skills. Curriculum paths are relative to `/git/github.com/LiGoldragon/Curriculum/skills/`. Primary paths are relative to `/home/li/primary/`.

## Curriculum skills, unprefixed (39)

| # | Source | Target | Deployed | Split | Reason | vs P4 |
|---|---|---|---|---|---|---|
| 1 | spirit.md | psyche/spirit/spirit | `spirit` | no | the philosophy: why AI exists | = P4 |
| 2 | psyche.md | psyche/vision/psyche, merged with Vision/psyche.md | `vision-psyche` | yes. Intro, Four levels, weighing of records → psyche/vision/psyche. "Where psyche lives" (paths of records today) → field/knowledge/psyche-records (`knowledge-psyche-records`) | what psyche is and how its levels bind; the paths are where records sit now | = P4; split added |
| 3 | vocabulary.md | psyche/vision/vocabulary | `vision-vocabulary` | no | the living's meaning of our terms | = P4 |
| 4 | behavior.md | psyche/vision/behavior | `vision-behavior` | no. The PROVENANCE/checksum line duplicates flow-evidence and is cut here | what is wanted of every flow's conduct | = P4 |
| 5 | correction.md | psyche/vision/correction | `vision-correction` | no | what is wanted when an output is wrong; the cause is context | = P4 |
| 6 | psyche-interraction.md | psyche/vision/psyche-interraction | `vision-psyche-interraction` | yes. Logging and Preserving the psyche's words (file layout, ordering, provenance line, STT bracket format, `hm-send --psyche` relay) → mind/operation/psyche-logging (`operation-psyche-logging`). What is vision, Anatomy, Graduation, Conversation, Authority → psyche/vision | how the living is to be heard and whose word binds; the logging steps are a procedure | = P4; split added |
| 7 | psyche-acquisition.md | mind/operation/psyche-acquisition | `operation-psyche-acquisition` | no | a search procedure; states nothing wanted | **DIFFERS** (P4: psyche). The text holds procedure only. |
| 8 | psyche-distillation.md | mind/operation/psyche-distillation | `operation-psyche-distillation` | yes. What a distilled statement carries, approval before landing, impurities, destination per statement → psyche/vision/distillation (merge with Vision/distillation.md, which already holds these rulings). Sources-file line format, archive- move, record id, subflow gathering → mind/operation | the rulings are vision; the bookkeeping is how | **DIFFERS** (P4: psyche, whole). The procedure half belongs to mind. |
| 9 | psyche-grasp.md | mind/operation/psyche-grasp | `operation-psyche-grasp` | no | how a code site is marked; levels and mark form are design | **DIFFERS** (P4: psyche). Code-marking convention, not a want. |
| 10 | skill-designing.md | mind/operation/skill-designing | `operation-skill-designing` | yes. "Skill types" section and the rationale-skill line → psyche/vision/skills (the Proposal 1 section). The `{% if %}` template line and user-only deployment mechanics → mind/knowledge/skill-source (`knowledge-skill-source`). Writing craft, description rules, Cut/Keep → mind/operation | the craft of writing a skill is how; who stands behind each kind is a want; the template is generator design | **DIFFERS** (P4: psyche, whole). Most of the text is craft. |
| 11 | main-flow.md | mind/operation/main-flow | `operation-main-flow` | yes. `flow-id claude/codex` command lines → field/knowledge/flow (merge into knowledge-flow) | a seat's identity module is Operation; psyche-skills has no operation/ and the text is how a main flow works | **DIFFERS** (P4: psyche). There is no Role type, and psyche holds no Operation (doubt 4). |
| 12 | datom.md | mind/knowledge/datom | `knowledge-datom` | no (overlap with Vision/datom.md: see doubt 8) | what datom is by design: syntax, types | = P4 |
| 13 | protos.md | mind/knowledge/protos | `knowledge-protos` | no (overlap with Vision/protos.md: see doubt 8) | what protos is by design | = P4 |
| 14 | lojix.md | mind/knowledge/lojix | `knowledge-lojix` | yes. Request syntax, ordinary and owner requests, replies, deployment contract → mind/knowledge/lojix. Socket env variables, startup configuration tested forms, schema v5, store inspection and reset, bootstrap → field/knowledge/lojix-nexus (`knowledge-lojix-nexus`) | the contract is design; the deployed service's state is what runs | = P4; split added |
| 15 | orchestrate.md | mind/knowledge/orchestrate | `knowledge-orchestrate` | yes. "The installed wrapper supplies ORCHESTRATE_SOCKET" → field/knowledge/nexus (merge into knowledge-nexus) | the Lock contract is design | = P4; split added |
| 16 | context-strata.md | mind/knowledge/context-strata | `knowledge-context-strata` | no | what strata are by design, harness-independent | = P4 |
| 17 | documentation-placement.md | mind/operation/documentation-placement | `operation-documentation-placement` | no | how a thing is written down | = P4 |
| 18 | testing.md | mind/operation/testing | `operation-testing` | no | how a change is proved | = P4 |
| 19 | versioning.md | mind/operation/versioning | `operation-versioning` | no | how a version is bumped | = P4 |
| 20 | prompt-crafting.md | mind/operation/prompt-crafting | `operation-prompt-crafting` | no | how a prompt is made | = P4 |
| 21 | design.md | mind/operation/design | `operation-design` | no | how a design round is worked (see doubt 5) | = P4 |
| 22 | realization.md | mind/operation/realization | `operation-realization` | no | how a realization round is worked (see doubt 5) | = P4 |
| 23 | claude-harness.md | field/knowledge/claude-harness | `knowledge-claude-harness` | no | witnessed facts of the harness as it runs | = P4 |
| 24 | codex-harness.md | field/knowledge/codex-harness | `knowledge-codex-harness` | yes. "A launcher passes the role's model by family name … medium" → field/operation/compensation-default-effort (merge) | witnessed facts of the harness as it runs; the launcher line is an effort rule | = P4; split added |
| 25 | agent-harness-packaging.md | mind/operation/agent-harness-packaging | `operation-agent-harness-packaging` | no | how a harness manager is packaged | **DIFFERS** (P4: field). Field operation/ admits only compensation-/trial- names, and this is how-to (doubt 1). |
| 26 | nix-workflow.md | mind/operation/nix-workflow | `operation-nix-workflow` | no | how a change lands in Nix | **DIFFERS** (P4: field). Doubt 1. |
| 27 | nix-input-upgrade.md | mind/operation/nix-input-upgrade | `operation-nix-input-upgrade` | no | how inputs are upgraded | **DIFFERS** (P4: field). Doubt 1. |
| 28 | operating-system.md | mind/operation/operating-system | `operation-operating-system` | no | how the OS is changed | **DIFFERS** (P4: field). Doubt 1. |
| 29 | disk-hygiene.md | mind/operation/disk-hygiene | `operation-disk-hygiene` | no | how space is reclaimed | **DIFFERS** (P4: field). Doubt 1. |
| 30 | secrets.md | mind/operation/secrets | `operation-secrets` | no | how a secret reaches a program | **DIFFERS** (P4: field). Doubt 1. |
| 31 | file-editing.md | mind/operation/file-editing | `operation-file-editing` | yes. The Primary paragraph (independent clone, no commits in the shared copy) → field/operation/compensation-primary-commit (merge) | how edits are committed; the Primary workaround compensates today's workspace | **DIFFERS** (P4: field). Doubt 1. |
| 32 | edit-coordination.md | mind/operation/edit-coordination | `operation-edit-coordination` | no | how paths are reserved before editing | **DIFFERS** (P4: field). Doubt 1. |
| 33 | beads.md | mind/operation/beads | `operation-beads` | no | how work is tracked | **DIFFERS** (P4: field). Doubt 1. |
| 34 | flow-evidence.md | mind/operation/flow-evidence | `operation-flow-evidence` | no | how a report or witness is written | **DIFFERS** (P4: field). Doubt 1. |
| 35 | repository-lifecycle.md | mind/operation/repository-lifecycle | `operation-repository-lifecycle` | no | how a repository is made and closed | **DIFFERS** (P4: field). Doubt 1. |
| 36 | feature-development.md | mind/operation/feature-development | `operation-feature-development` | no (candidate for merging into edit-coordination) | how feature work shares a checkout | **DIFFERS** (P4: field). Doubt 1. |
| 37 | breaking-upgrades.md | mind/operation/breaking-upgrades | `operation-breaking-upgrades` | no | how a breaking change is deployed | **DIFFERS** (P4: field). Doubt 1. |
| 38 | stale-lock.md | field/operation/compensation-stale-lock | `operation-compensation-stale-lock` | no | compensates for locks the system does not yet release (hm-list, Herdr) | **DIFFERS** (P4: field, stem unchanged). Field operation/ requires the prefix (doubt 11). |
| 39 | transcript-search.md | field/knowledge/transcript-search | `knowledge-transcript-search` | no | the deployed `transcript` CLI as it runs | = P4 |

## Curriculum skills, prefixed (31). P4 names only the vision- merge; the rest are placed by rule

| # | Source | Target | Deployed | Split | Reason | vs P4 |
|---|---|---|---|---|---|---|
| 40 | vision-ethos.md | psyche/vision/ethos, merged with Vision/ethos.md | `vision-ethos` | no | what ethos is wanted to be | = P4 (merge) |
| 41 | vision-flow.md | psyche/vision/flow, merged with Vision/flowNexus.md | `vision-flow` | no | what Flow is wanted to be | P4 silent: the topic is named flowNexus, not flow (doubt 7) |
| 42 | vision-nexus.md | psyche/vision/nexus, merged with Vision/nexus.md | `vision-nexus` | no | what a Nexus is wanted to be | = P4 (merge) |
| 43 | knowledge-codex.md | field/knowledge/codex | `knowledge-codex` | no | version-pinned surface of the installed app-server | P4 silent |
| 44 | knowledge-ethos.md | field/knowledge/ethos | `knowledge-ethos` | no | ethos-zero as it runs today | P4 silent |
| 45 | knowledge-flow.md | field/knowledge/flow | `knowledge-flow` | no | deployed Flow 0.23 | P4 silent |
| 46 | knowledge-nexus.md | field/knowledge/nexus | `knowledge-nexus` | no | which nexuses run today | P4 silent |
| 47 | knowledge-layer-models.md | field/knowledge/layer-models | `knowledge-layer-models` | yes. The "Living ruling" rows (Quaternary Sonnet/Luna Low) → psyche/vision/modelRoles | the configured table is what runs; the rulings are wanted | P4 silent |
| 48 | operation-book.md | mind/operation/book | `operation-book` | no | how a presentation is made | P4 silent |
| 49 | operation-flashbook.md | mind/operation/flashbook | `operation-flashbook` | no | how a flashbook is made | P4 silent |
| 50 | operation-flashbook-illustration.md | mind/operation/flashbook-illustration | `operation-flashbook-illustration` | no | how an illustration is drawn | P4 silent |
| 51 | operation-relaying-the-living.md | mind/operation/relaying-the-living | `operation-relaying-the-living` | no | how living words are passed on | P4 silent |
| 52 | compensation-default-effort.md | field/operation/compensation-default-effort | `operation-compensation-default-effort` | no | effort rule until Flow holds the model | P4 silent |
| 53 | compensation-messenger-clj.md | field/operation/compensation-messenger-clj | `operation-compensation-messenger-clj` | no | the running hm-* messenger | P4 silent (the book's own example) |
| 54 | compensation-nix.md | field/operation/compensation-nix | `operation-compensation-nix` | no | test-repository weld | P4 silent |
| 55 | compensation-nix-rationale.md | field/operation/compensation-nix-rationale | `operation-compensation-nix-rationale` | no | travels with its parent skill | P4 silent |
| 56 | compensation-primary-commit.md | field/operation/compensation-primary-commit | `operation-compensation-primary-commit` | no | today's Primary publishing weld | P4 silent |
| 57 | compensation-subflow.md | field/operation/compensation-subflow | `operation-compensation-subflow` | no | weld for subflow message bodies | P4 silent |
| 58 | compensation-update.md | field/operation/compensation-update | `operation-compensation-update` | no | stable/Next rotation weld | P4 silent |
| 59–70 | trial-contact-discipline, trial-generated-projection, trial-independent-review, trial-low-power, trial-no-polling, trial-presentation-book, trial-psyche-injection, trial-questions-book, trial-reaping, trial-recurring-failure, trial-succession, trial-unblocking-commands (.md) | field/operation/trial-<name> | `operation-trial-<name>` | no | welds on trial | P4 silent |

## Vision/<topic>.md (20). P4: every topic → psyche/vision/<topic>

| # | Source | Target | Deployed | Split | Reason | vs P4 |
|---|---|---|---|---|---|---|
| 71 | Vision/committing.md | psyche/vision/committing | `vision-committing` | no | what a commit is wanted to name | = P4 |
| 72 | Vision/datom.md | psyche/vision/datom | `vision-datom` | no (overlap with the datom skill: doubt 8) | what datom is wanted to be | = P4 |
| 73 | Vision/deployment.md | psyche/vision/deployment | `vision-deployment` | no | where a proof of concept is wanted to run | = P4 |
| 74 | Vision/distillation.md | psyche/vision/distillation | `vision-distillation` | no; receives the rulings from row 8 | what distillation is wanted to be | = P4 |
| 75 | Vision/ethos.md | psyche/vision/ethos | `vision-ethos` | no; receives row 40 | what ethos is wanted to be | = P4 |
| 76 | Vision/flowNexus.md | psyche/vision/flow | `vision-flow` | no; receives row 41 | what Flow is wanted to be | = P4 (stem: doubt 7) |
| 77 | Vision/highLevelView.md | psyche/vision/highLevelView | `vision-highLevelView` | no | what view is wanted, and how often | = P4 |
| 78 | Vision/horizon.md | psyche/vision/horizon | `vision-horizon` | no | what Horizon is wanted to be | = P4 |
| 79 | Vision/meaning.md | psyche/vision/meaning | `vision-meaning` | no | what the meaning language is wanted to be | = P4 |
| 80 | Vision/messaging.md | psyche/vision/messaging | `vision-messaging` | yes. "Delivery is harness-specific" (Escape counts, Enter, composer behavior) → field/knowledge/messaging (`knowledge-messaging`) | the message shape is wanted; the keystroke mechanics are what runs | = P4; split added |
| 81 | Vision/modelRoles.md | psyche/vision/modelRoles | `vision-modelRoles` | yes. "The older seat is Opus 4.6…" (callable ids, `claude --model` lines) → field/knowledge/layer-models (merge) | seats and ceilings are wanted; witnessed ids are what runs | = P4; split added |
| 82 | Vision/nexus.md | psyche/vision/nexus | `vision-nexus` | no; receives row 42 | what a Nexus is wanted to be | = P4 |
| 83 | Vision/orchestrate.md | psyche/vision/orchestrate | `vision-orchestrate` | no | what deployment and skill scope are wanted | = P4 |
| 84 | Vision/protos.md | psyche/vision/protos | `vision-protos` | no (overlap with the protos skill: doubt 8) | what protos is wanted to be | = P4 |
| 85 | Vision/psyche.md | psyche/vision/psyche | `vision-psyche` | no; receives row 2 (see doubt 10) | what psyche is | = P4 |
| 86 | Vision/remembering.md | psyche/vision/remembering | `vision-remembering` | no | what remembering is wanted to be | = P4 |
| 87 | Vision/sema.md | psyche/vision/sema | `vision-sema` | no | what sema is wanted to be | = P4 |
| 88 | Vision/signal.md | psyche/vision/signal | `vision-signal` | no | what signal is wanted to be | = P4 |
| 89 | Vision/x11.md | psyche/vision/x11 | `vision-x11` | no | what CriomOS is wanted to drop | = P4 |
| 90 | Vision/archive-ethosMonolith.md | psyche-logs/legacy/archive-ethosMonolith.md | none (not a module) | no | archived raw records, not a topic | **DIFFERS** (P4: every Vision file → vision/). Archived records drain to psyche-logs, like vision-raw. |

## Intent/<topic>.md (10). P4: every topic → psyche/intent/<topic>

| # | Source | Target | Deployed | Split | Reason | vs P4 |
|---|---|---|---|---|---|---|
| 91–100 | Intent/anatomy, context, conversion, data, mandatoryTraits, models, protosParsing, psycheInteraction, startupPrompt, testing (.md) | psyche/intent/<topic> | `intent-<topic>` | no | declared goals and guiding rules | = P4 |

## Sidecar sources, not modules

| Source | Target | Note |
|---|---|---|
| Vision/sources/*.md (18) | undecided | doubt 9 |
| Intent/sources/*.md (7) | undecided | doubt 9 |

## Counts

| Target | Rows (main part of each row) |
|---|---|
| psyche/spirit | 1 |
| psyche/vision | 27 (20 modules after 4 merges) |
| psyche/intent | 10 |
| mind/operation | 28 |
| mind/knowledge | 5 |
| field/knowledge | 8 |
| field/operation | 20 |
| psyche-logs (not a module) | 1 |
| total | 100 |

Rows that differ from P4: 20. These are 18 repository changes (5 psyche→mind, 13 field→mind), 1 deployed-name change (stale-lock), and 1 Vision file moved out of vision/ (archive-ethosMonolith). Rows with a split: 12 (rows 2, 6, 8, 10, 11, 14, 15, 24, 31, 47, 80, 81).

## Doubtful names, for his ruling

1. **Field how-to skills.** Proposal 2 lets field operation/ hold only compensation-/trial- names. Thirteen how-to skills P4 sent to field are affected: agent-harness-packaging, nix-workflow, nix-input-upgrade, operating-system, disk-hygiene, secrets, file-editing, edit-coordination, beads, flow-evidence, repository-lifecycle, feature-development, breaking-upgrades. (a) mind/operation, unprefixed (the table). (b) field/operation, with unprefixed names allowed there. (c) field/operation, renamed `compensation-<name>`.
2. **Psyche procedures.** psyche-acquisition, psyche-grasp, the procedure half of psyche-distillation, and the logging half of psyche-interraction. (a) mind/operation (the table). (b) psyche/vision, whole, as P4. (c) add operation/ to psyche-skills' allowed types.
3. **Type of the gold conduct rules in psyche.** behavior, correction, vocabulary, the rest of psyche-interraction, and the Skill types section. (a) vision/ (the table). (b) intent/, which enters only on his explicit word.
4. **main-flow.** It is the main seat of every aspect, and psyche-skills has no operation/. (a) mind/operation/main-flow (the table). (b) field/operation/main-flow, with unprefixed names allowed there. (c) one Operation module per aspect, mind and field, each with its own stem, and the psyche seat taking one of them.
5. **design and realization (user-only round modes).** (a) mind/operation (the table). (b) fold design into vision/highLevelView and main-flow, and realization into vision.
6. **Stem case.** Vision and Intent stems are camelCase (flowNexus, modelRoles, highLevelView, psycheInteraction); skill stems are kebab-case. (a) keep each as it is, e.g. `vision-modelRoles` (the table). (b) all kebab, e.g. `vision-model-roles`, `intent-psyche-interaction`. (c) all camelCase.
7. **Flow vision stem.** (a) merge Vision/flowNexus.md and vision-flow into vision/flow (the table). (b) merge into vision/flowNexus. (c) keep two modules.
8. **Duplicate datom and protos texts.** The datom and protos skills repeat sections of Vision/datom.md and Vision/protos.md. (a) keep mind/knowledge as the working text and cut the repeated sections from vision. (b) merge each skill into its vision module, one text, the vision's, as with vision-<topic>. (c) keep both as they are (the table).
9. **Vision/sources and Intent/sources.** (a) psyche-skills/vision/sources/ and intent/sources/, excluded from deployment. (b) psyche-logs/sources/. (c) inline at the foot of each module.
10. **Vision/psyche.md prefix paragraph.** It names `operational-` and `testing-` prefixes, which Proposal 2 supersedes. (a) superseded when Proposal 1 lands. (b) kept as written.
11. **stale-lock.** (a) field/operation/compensation-stale-lock (the table). (b) mind/operation/stale-lock, kept gold.
12. **One subject split across mind and field knowledge.** Example: lojix contract vs lojix-nexus. (a) the field part takes the running thing's name, `knowledge-lojix-nexus` (the table). (b) the field part takes a `-deployed` suffix. (c) all Knowledge to mind (book ruling 2b), which removes the split.
13. **psyche-interraction spelling.** (a) keep `psyche-interraction`. (b) rename to `psyche-interaction` on migration.

## Flagged sentence

The sentence beginning "The work is editing context modules" is cut from every module. It occurs in none of the sources: not in Curriculum skills/ at c7d35e2 or on any Curriculum ref, and not in Vision/ or Intent/. No row is flagged.

## Sources

- Book «Three skill repositories and the main workspace», https://claude.ai/artifact/6zgqzzzrUWwsotzHokqUNp (read 2026-10-04; there is no local source under flows/bad807/books/ or reports/).
- /home/li/primary/flows/bad807/reports/books.md
- /home/li/primary/flows/28d847/reports/skill-kinds.md (lists 69 skills; Curriculum now holds 70, adding knowledge-layer-models)
- /git/github.com/LiGoldragon/Curriculum/skills/*.md at c7d35e2
- /home/li/primary/Vision/*.md, /home/li/primary/Intent/*.md
- Provenance receipt: unavailable.
