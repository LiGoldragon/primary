# Placing table: three skill repositories

Rule: a module belongs to the aspect whose question it answers. Psyche: what is wanted and why. Mind: how a thing is done, what it is by design. Field: what runs now, what holds it together. Module types are Spirit, Intent, Vision, Notion, Knowledge and Operation; there is no Role type. psyche-skills holds spirit/ intent/ vision/ notion/, mind-skills operation/ knowledge/, field-skills operation/ knowledge/. Field operation/ holds the how-to of the running system under unprefixed names; `compensation-` and `trial-` are prefixes for welds and trials. A seat's identity module is an Operation module of its seat's aspect. Each module is a file at `<repository>/<type>/<stem>.md`. Deployed name is `<type>-<stem>`; Spirit deploys as `spirit`. A field part split from a mind subject takes the running thing's name.

Abbreviations: `psyche` = psyche-skills, `mind` = mind-skills, `field` = field-skills. Curriculum paths are relative to `/git/github.com/LiGoldragon/Curriculum/skills/` at c7d35e2. Primary paths are relative to `/home/li/primary/`. A split part cites its source path, section and lines; the cut texts are in `flows/aa887c/scripts/splits/`, indexed with each source's sha256 in `splits/index.tsv`. "Merged" means the parts are joined in the order given.

Marks for the open items: ‡ the type is `vision` or `intent` by item 3; † the stem is camelCase or kebab-case by item 6 (the table writes it as in the source).

## Curriculum skills, unprefixed (39)

| # | Source | Target | Deployed | Split | Reason |
|---|---|---|---|---|---|
| 1 | spirit.md | psyche/spirit/spirit | `spirit` | no | the philosophy: why AI exists |
| 2 | psyche.md | psyche/vision/psyche: frontmatter of psyche.md, then Vision/psyche.md, then this part | `vision-psyche` | yes. psyche.md intro, Four levels, weighing of records (l.6-46, 65-78) → psyche/vision/psyche. psyche.md "Where psyche lives", the list (l.48-63) → field/knowledge/psyche-records (`knowledge-psyche-records`) | what psyche is and how its levels bind; the paths are where records sit now |
| 3 | vocabulary.md | psyche/vision/vocabulary ‡ | `vision-vocabulary` | no | the living's meaning of our terms |
| 4 | behavior.md | psyche/vision/behavior ‡ | `vision-behavior` | no. behavior.md l.22, the PROVENANCE/checksum paragraph, is cut; it duplicates flow-evidence | what is wanted of every flow's conduct |
| 5 | correction.md | psyche/vision/correction ‡ | `vision-correction` | no | what is wanted when an output is wrong; the cause is context |
| 6 | psyche-interraction.md | psyche/vision/psyche-interraction | `vision-psyche-interraction` | yes. psyche-interraction.md frontmatter, Logging: what is vision (l.24-34), Anatomy, Graduation, Conversation, Authority (l.65-96) → psyche/vision/psyche-interraction (vision by the designer's ruling 2, whatever item 3). psyche-interraction.md Logging (l.6-22) and Preserving the psyche's words (l.36-63) → mind/operation/psyche-logging (`operation-psyche-logging`) | how the living is to be heard and whose word binds; the logging steps are a procedure |
| 7 | psyche-acquisition.md | mind/operation/psyche-acquisition | `operation-psyche-acquisition` | no | a search procedure |
| 8 | psyche-distillation.md | mind/operation/psyche-distillation | `operation-psyche-distillation` | yes. psyche-distillation.md what a distilled statement carries (l.25-27), approval before landing (l.29-33, to "explicit word."), impurities and destination per statement (l.45-49) → psyche/vision/distillation, merged after Vision/distillation.md. psyche-distillation.md intro, sources-file line format, subflow gathering (l.1-23), archive- move (l.33-35), record id and dispatch (l.37-43) → mind/operation/psyche-distillation | the rulings are vision; the bookkeeping is how |
| 9 | psyche-grasp.md | mind/operation/psyche-grasp | `operation-psyche-grasp` | no | how a code site is marked |
| 10 | skill-designing.md | mind/operation/skill-designing | `operation-skill-designing` | yes. skill-designing.md frontmatter, writing craft, description rules, Cut these, Keep these (l.1-48) → mind/operation/skill-designing. skill-designing.md Skill types (l.53-59, 66-67) and the rationale-skill line (l.69) → psyche/vision/skills ‡ (`vision-skills`). skill-designing.md Keep these: the `{% if %}` template line (l.49-51) and Skill types: user-only deployment (l.61-64) → mind/knowledge/skill-source (`knowledge-skill-source`) | the craft of writing a skill is how; who stands behind each kind is a want; the template is generator design |
| 11 | main-flow.md | mind/operation/main-flow | `operation-main-flow` | yes. main-flow.md, less l.22-27 and less l.8, 10, 11, 17, 18, 51 (the lines the system prompt repeats; Context modules, Proposal 6) → mind/operation/main-flow. main-flow.md `flow-id claude/codex` command lines (l.22-27) → field/knowledge/flow, merged after knowledge-flow.md | a seat's identity module is Operation, and the text is how a main flow works |
| 12 | datom.md | psyche/vision/datom: frontmatter of datom.md, then Vision/datom.md, then the body of datom.md | `vision-datom` | no | what datom is wanted to be, one text with its vision |
| 13 | protos.md | psyche/vision/protos: frontmatter of protos.md, then Vision/protos.md, then the body of protos.md | `vision-protos` | no | what protos is wanted to be, one text with its vision |
| 14 | lojix.md | mind/knowledge/lojix | `knowledge-lojix` | yes. lojix.md frontmatter, contracts, Request syntax, Ordinary requests, Owner requests, Replies and terminal state, Deployment contract (l.1-10, 14-257), Placement (l.379-383) → mind/knowledge/lojix. lojix.md socket env variables (l.12), Startup configuration, Store inspection and reset with schema v5, Bootstrap (l.258-378) → field/knowledge/lojix-nexus (`knowledge-lojix-nexus`) | the contract is design; the deployed service's state is what runs |
| 15 | orchestrate.md | mind/knowledge/orchestrate | `knowledge-orchestrate` | yes. orchestrate.md, less one sentence → mind/knowledge/orchestrate. orchestrate.md l.6, the sentence "The installed wrapper supplies `ORCHESTRATE_SOCKET`; a direct client binary requires it." → field/knowledge/nexus, merged after knowledge-nexus.md | the Lock contract is design |
| 16 | context-strata.md | mind/knowledge/context-strata | `knowledge-context-strata` | no | what strata are by design, harness-independent |
| 17 | documentation-placement.md | mind/operation/documentation-placement | `operation-documentation-placement` | no | how a thing is written down |
| 18 | testing.md | mind/operation/testing | `operation-testing` | no | how a change is proved |
| 19 | versioning.md | mind/operation/versioning | `operation-versioning` | no | how a version is bumped |
| 20 | prompt-crafting.md | mind/operation/prompt-crafting | `operation-prompt-crafting` | no | how a prompt is made |
| 21 | design.md | mind/operation/design | `operation-design` | no | how a design round is worked |
| 22 | realization.md | mind/operation/realization | `operation-realization` | no | how a realization round is worked |
| 23 | claude-harness.md | field/knowledge/claude-harness | `knowledge-claude-harness` | no | witnessed facts of the harness as it runs |
| 24 | codex-harness.md | field/knowledge/codex-harness | `knowledge-codex-harness` | yes. codex-harness.md, less l.20 → field/knowledge/codex-harness. codex-harness.md l.20, "A launcher passes the role's model by family name … medium" → field/operation/compensation-default-effort, merged after compensation-default-effort.md | witnessed facts of the harness as it runs; the launcher line is an effort rule |
| 25 | agent-harness-packaging.md | field/operation/agent-harness-packaging | `operation-agent-harness-packaging` | no | how a harness manager is packaged on the running system |
| 26 | nix-workflow.md | field/operation/nix-workflow | `operation-nix-workflow` | no | how a change lands in Nix |
| 27 | nix-input-upgrade.md | field/operation/nix-input-upgrade | `operation-nix-input-upgrade` | no | how inputs are upgraded |
| 28 | operating-system.md | field/operation/operating-system | `operation-operating-system` | no | how the OS is changed |
| 29 | disk-hygiene.md | field/operation/disk-hygiene | `operation-disk-hygiene` | no | how space is reclaimed |
| 30 | secrets.md | field/operation/secrets | `operation-secrets` | no | how a secret reaches a program |
| 31 | file-editing.md | field/operation/file-editing | `operation-file-editing` | yes. file-editing.md, less the Primary sentences of l.11 → field/operation/file-editing. file-editing.md l.11, the Primary sentences (independent clone, no commits in the shared copy, to "path-limited publication.") → field/operation/compensation-primary-commit, merged after compensation-primary-commit.md | how edits are committed; the Primary workaround compensates today's workspace |
| 32 | edit-coordination.md | field/operation/edit-coordination | `operation-edit-coordination` | no | how paths are reserved before editing |
| 33 | beads.md | field/operation/beads | `operation-beads` | no | how work is tracked |
| 34 | flow-evidence.md | field/operation/flow-evidence | `operation-flow-evidence` | no | how a report or witness is written |
| 35 | repository-lifecycle.md | field/operation/repository-lifecycle | `operation-repository-lifecycle` | no | how a repository is made and closed |
| 36 | feature-development.md | field/operation/feature-development | `operation-feature-development` | no (candidate for merging into edit-coordination) | how feature work shares a checkout |
| 37 | breaking-upgrades.md | field/operation/breaking-upgrades | `operation-breaking-upgrades` | no | how a breaking change is deployed |
| 38 | stale-lock.md | field/operation/stale-lock | `operation-stale-lock` | no | how a lock the system does not yet release is cleared (hm-list, Herdr) |
| 39 | transcript-search.md | field/knowledge/transcript-search | `knowledge-transcript-search` | no | the deployed `transcript` CLI as it runs |

## Curriculum skills, prefixed (31)

| # | Source | Target | Deployed | Split | Reason |
|---|---|---|---|---|---|
| 40 | vision-ethos.md | psyche/vision/ethos: frontmatter of vision-ethos.md, then Vision/ethos.md, then the body of vision-ethos.md | `vision-ethos` | no | what ethos is wanted to be |
| 41 | vision-flow.md | psyche/vision/flow: frontmatter of vision-flow.md, then Vision/flowNexus.md, then the body of vision-flow.md | `vision-flow` | no | what Flow is wanted to be |
| 42 | vision-nexus.md | psyche/vision/nexus: frontmatter of vision-nexus.md, then Vision/nexus.md, then the body of vision-nexus.md | `vision-nexus` | no | what a Nexus is wanted to be |
| 43 | knowledge-codex.md | field/knowledge/codex | `knowledge-codex` | no | version-pinned surface of the installed app-server |
| 44 | knowledge-ethos.md | field/knowledge/ethos | `knowledge-ethos` | no | ethos-zero as it runs today |
| 45 | knowledge-flow.md | field/knowledge/flow, then the row 11 part | `knowledge-flow` | no; receives row 11 | deployed Flow 0.23 |
| 46 | knowledge-nexus.md | field/knowledge/nexus, then the row 15 part | `knowledge-nexus` | no; receives row 15 | which nexuses run today |
| 47 | knowledge-layer-models.md | field/knowledge/layer-models: this file less l.14-17, then the row 81 part | `knowledge-layer-models` | yes. knowledge-layer-models.md, less l.14-17 → field/knowledge/layer-models. knowledge-layer-models.md l.14-17, the "Living ruling" rows (Tertiary and Quaternary Living ruling rows), with the table header (l.8-9) copied before them → psyche/vision/modelRoles †, merged after the row 81 part | the configured table is what runs; the rulings are wanted |
| 48 | operation-book.md | mind/operation/book | `operation-book` | no | how a presentation is made |
| 49 | operation-flashbook.md | mind/operation/flashbook | `operation-flashbook` | no | how a flashbook is made |
| 50 | operation-flashbook-illustration.md | mind/operation/flashbook-illustration | `operation-flashbook-illustration` | no | how an illustration is drawn |
| 51 | operation-relaying-the-living.md | mind/operation/relaying-the-living | `operation-relaying-the-living` | no | how living words are passed on |
| 52 | compensation-default-effort.md | field/operation/compensation-default-effort, then the row 24 part | `operation-compensation-default-effort` | no; receives row 24 | effort rule until Flow holds the model |
| 53 | compensation-messenger-clj.md | field/operation/compensation-messenger-clj | `operation-compensation-messenger-clj` | no | the running hm-* messenger |
| 54 | compensation-nix.md | field/operation/compensation-nix | `operation-compensation-nix` | no | test-repository weld |
| 55 | compensation-nix-rationale.md | field/operation/compensation-nix-rationale | `operation-compensation-nix-rationale` | no | travels with its parent skill |
| 56 | compensation-primary-commit.md | field/operation/compensation-primary-commit, then the row 31 part | `operation-compensation-primary-commit` | no; receives row 31 | today's Primary publishing weld |
| 57 | compensation-subflow.md | field/operation/compensation-subflow | `operation-compensation-subflow` | no | weld for subflow message bodies |
| 58 | compensation-update.md | field/operation/compensation-update | `operation-compensation-update` | no | stable/Next rotation weld |
| 59–70 | trial-contact-discipline, trial-generated-projection, trial-independent-review, trial-low-power, trial-no-polling, trial-presentation-book, trial-psyche-injection, trial-questions-book, trial-reaping, trial-recurring-failure, trial-succession, trial-unblocking-commands (.md) | field/operation/trial-<name> | `operation-trial-<name>` | no | welds on trial |

## Vision/<topic>.md (20)

| # | Source | Target | Deployed | Split | Reason |
|---|---|---|---|---|---|
| 71 | Vision/committing.md | psyche/vision/committing | `vision-committing` | no | what a commit is wanted to name |
| 72 | Vision/datom.md | psyche/vision/datom | `vision-datom` | no; receives row 12 | what datom is wanted to be |
| 73 | Vision/deployment.md | psyche/vision/deployment | `vision-deployment` | no | where a proof of concept is wanted to run |
| 74 | Vision/distillation.md | psyche/vision/distillation, then the row 8 part | `vision-distillation` | no; receives row 8 | what distillation is wanted to be |
| 75 | Vision/ethos.md | psyche/vision/ethos | `vision-ethos` | no; receives row 40 | what ethos is wanted to be |
| 76 | Vision/flowNexus.md | psyche/vision/flow | `vision-flow` | no; receives row 41 | what Flow is wanted to be |
| 77 | Vision/highLevelView.md | psyche/vision/highLevelView † | `vision-highLevelView` | no | what view is wanted, and how often |
| 78 | Vision/horizon.md | psyche/vision/horizon | `vision-horizon` | no | what Horizon is wanted to be |
| 79 | Vision/meaning.md | psyche/vision/meaning | `vision-meaning` | no | what the meaning language is wanted to be |
| 80 | Vision/messaging.md | psyche/vision/messaging | `vision-messaging` | yes. Vision/messaging.md, less l.12-20 (l.28-30 "Only messages that act, deliver, or block" stays in the psyche part) → psyche/vision/messaging. Vision/messaging.md "Delivery is harness-specific, and the mechanism differs per tier" (l.12-20) → field/knowledge/messaging (`knowledge-messaging`) | the message shape is wanted; the keystroke mechanics are what runs |
| 81 | Vision/modelRoles.md | psyche/vision/modelRoles †, then the row 47 part | `vision-modelRoles` | yes. Vision/modelRoles.md, less l.31-39 → psyche/vision/modelRoles. Vision/modelRoles.md "The older seat is Opus 4.6…": callable ids and `claude --model` lines (l.31-39) → field/knowledge/layer-models, merged after the row 47 part | seats and ceilings are wanted; witnessed ids are what runs |
| 82 | Vision/nexus.md | psyche/vision/nexus | `vision-nexus` | no; receives row 42 | what a Nexus is wanted to be |
| 83 | Vision/orchestrate.md | psyche/vision/orchestrate | `vision-orchestrate` | no | what deployment and skill scope are wanted |
| 84 | Vision/protos.md | psyche/vision/protos | `vision-protos` | no; receives row 13 | what protos is wanted to be |
| 85 | Vision/psyche.md | psyche/vision/psyche | `vision-psyche` | no; receives row 2. Its prefix paragraph (l.10-12) is kept or cut by item 10 | what psyche is |
| 86 | Vision/remembering.md | psyche/vision/remembering | `vision-remembering` | no | what remembering is wanted to be |
| 87 | Vision/sema.md | psyche/vision/sema | `vision-sema` | no | what sema is wanted to be |
| 88 | Vision/signal.md | psyche/vision/signal | `vision-signal` | no | what signal is wanted to be |
| 89 | Vision/x11.md | psyche/vision/x11 | `vision-x11` | no | what CriomOS is wanted to drop |
| 90 | Vision/archive-ethosMonolith.md | psyche-logs/legacy/archive-ethosMonolith.md | none (not a module) | no | archived raw records, not a topic |

## Intent/<topic>.md (10)

| # | Source | Target | Deployed | Split | Reason |
|---|---|---|---|---|---|
| 91–100 | Intent/anatomy, context, conversion, data, mandatoryTraits †, models, protosParsing †, psycheInteraction †, startupPrompt †, testing (.md) | psyche/intent/<topic> | `intent-<topic>` | no | declared goals and guiding rules |

## New modules, READMEs, logs and data (designer's rulings, 2026-10-04)

| # | Source | Target | Deployed | Split | Reason |
|---|---|---|---|---|---|
| 101 | flows/bad807/books/15-context-modules.md, Proposal 7, `type:` line dropped | mind/operation/psyche-primary | `operation-psyche-primary` | no | the seat's identity module (ruling 3) |
| 102 | Curriculum roles.datom, inline general-instructions | mind/operation/general-instructions | `operation-general-instructions` | no | body verbatim; description "A subagent begins on its brief." (ruling C3) |
| 103 | Curriculum roles.datom, inline codex-skill-loading | mind/operation/codex-skill-loading | `operation-codex-skill-loading` | no | body verbatim; description "A Codex subagent is handed a pasted skill." (ruling C3) |
| 104 | Curriculum roles.datom, inline subflow-role | mind/operation/subflow-role | `operation-subflow-role` | no | body verbatim; description "A subflow starts inside a flow's lane." (ruling C3) |
| 105 | flows/bad807/books/15-context-modules.md, Proposal 1 body; description from Proposal 3 | psyche/vision/contextModules † | `vision-contextModules` | no | the context-module standard (ruling 5) |
| 106 | Primary SKILL_VARIABLES.md | field/knowledge/setup-variables | `knowledge-setup-variables` | no | values that differ between setups (ruling 5) |
| 107 | flows/bad807/books/17-workspace.md, Proposal 1 l.62 | psyche-skills/README.md, replaced | none (not a module) | no | two lines (ruling 5) |
| 108 | flows/bad807/books/17-workspace.md, Proposal 1 l.63 | mind-skills/README.md, replaced | none (not a module) | no | two lines (ruling 5) |
| 109 | flows/bad807/books/17-workspace.md, Proposal 1 l.64-65 | field-skills/README.md, replaced | none (not a module) | no | two lines; the sentence's two lines joined by one space (ruling 5) |
| 110 | vision-raw/*.md | psyche-logs/<flow>/vision/ or psyche-logs/legacy/vision/ | none (not a module) | per record where a file holds several flows: `splits/vision-raw/` | by each record's provenance line (ruling 6); trainingRepo.md goes to 6863ef19 (R2); where the lane already holds that file, the record is carried (R3) |
| 111 | flows/<flow>/vision/*.md | psyche-logs/<flow>/vision/ | none (not a module) | no | raw records (ruling 6) |
| 112 | flows/<flow>/notion/*.md | psyche-logs/<flow>/notion/ | none (not a module) | no | raw notions (ruling 6) |
| 113 | flows/, all else | flow-data/, lane structure unchanged | none (not a module) | no | flow data (ruling 6, C1): a lane's vision/ and notion/ go only to psyche-logs, flow-data gets the rest |
| 114 | knowledge-yt-dlp.md | field/knowledge/yt-dlp | `knowledge-yt-dlp` | no | how yt-dlp runs on this host |

Texts placed in existing modules (ruling 5), cut into `splits/books/` and checked verbatim by the script: row 11, the fifteen lines of `tools/main-flow-mode/system-prompt.md` after main-flow's frontmatter (Proposal 6); row 10, Proposal 10 lines 1-4 for skill-designing l.55-59 and Line 2 of 17-workspace.md for l.66-67 (Proposal 10 line 5 is not placed: Line 2 replaces the same lines); row 2, Line 1 of 17-workspace.md for psyche.md l.24-26; row 8, Proposal 11 after psyche-distillation.md l.25. No module carries a `type:` line (ruling 1).

A vision-raw record is a `## ` section; its provenance lines begin `— psyche`. One named flow (`session <id>` or `flow <id>`) sends it to that flow; none sends it to legacy; more, or a flow beside an unnamed source, makes it ambiguous: listed in `splits/vision-raw/ambiguous.tsv`, and the run refuses until it is ruled. `scripts/cut-texts.py` makes every cut and records it in `splits/index.tsv`.

Placement rule (C1): a lane's `vision/` and `notion/` go only to psyche-logs; every other file of a lane goes to flow-data, its structure unchanged.

Carried records (R3): when a vision-raw record's target file already exists in the lane, the target is `## Carried from vision-raw`, a blank line, the record, a blank line, then the lane's file; both texts whole, the older (vision-raw) words first. Ten records are carried; the script no longer refuses them.

Role record (R4): `scripts/roles/psyche-primary.datom` holds the Psyche Primary record from Proposal 8 of flows/bad807/books/15-context-modules.md, with FirstPrompt selecting `{ Operation [ psyche-logging edit-coordination ] }` and `psyche-interraction` added to its Loadable Vision list. Curriculum `roles.datom` is unchanged until the generator reads the new shape.

## Sidecar sources, not modules

| Source | Target | Note |
|---|---|---|
| Vision/sources/*.md (18) | psyche-skills/vision/sources/<topic>.md † | beside their modules, excluded from deployment; flowNexus.md takes its module's stem, flow |
| Intent/sources/*.md (7) | psyche-skills/intent/sources/<topic>.md † | beside their modules, excluded from deployment |

## Counts

Modules, with item 3 at vision:

| Target | Modules |
|---|---|
| psyche/spirit | 1 |
| psyche/vision | 25 |
| psyche/intent | 10 |
| mind/operation | 20 |
| mind/knowledge | 4 |
| field/operation | 33 |
| field/knowledge | 13 |
| psyche-logs/legacy (not a module) | 1 |

Not modules, from the dry run of 2026-10-04: three READMEs replaced; psyche-logs/legacy/vision 75 files, psyche-logs/<flow>/vision 1554 (ten of them carried), psyche-logs/<flow>/notion 65; flow-data 3865.

With item 3 at intent, four modules (vocabulary, behavior, correction, skills) move from psyche/vision to psyche/intent: 21 and 14. Rows with a split: 12 (rows 2, 6, 8, 10, 11, 14, 15, 24, 31, 47, 80, 81). Six stems are shared by two types with distinct deployed names: flow, nexus, ethos, messaging (vision, knowledge), orchestrate (vision, knowledge), testing (intent, operation).

## Open, for the living

3. **Type of the gold conduct rules in psyche.** behavior, correction, vocabulary, and the Skill types part of skill-designing. (a) vision/. (b) intent/, which enters only on his explicit word. Script variable `CONDUCT_TYPE=vision|intent`.
6. **Stem case.** Vision and Intent stems are camelCase (modelRoles, highLevelView, mandatoryTraits, protosParsing, psycheInteraction, startupPrompt); skill stems are kebab-case. (a) all kebab, e.g. `vision-model-roles`, `intent-psyche-interaction`. (b) all camelCase, e.g. `operation-mainFlow`; `compensation-` and `trial-` stay as prefixes. Script variable `STEM_CASE=kebab|camel`.
10. **Vision/psyche.md prefix paragraph.** It names `operational-` and `testing-` prefixes. (a) cut when Proposal 1 lands. (b) kept as written. Script variable `KEEP_PREFIX_PARAGRAPH=yes|no`.

## Flagged sentence

The sentence beginning "The work is editing context modules" is cut from every module. It occurs in none of the sources: not in Curriculum skills/ at c7d35e2 or on any Curriculum ref, and not in Vision/ or Intent/.

## Rulings applied after the cut

Five new modules (psyche-records, psyche-logging, skill-source, lojix-nexus, field messaging) carry a frontmatter description. Three pointers are retargeted: Authority in psyche-interraction names `vision-skills`; main-flow names `knowledge-flow`; file-editing names `operation-compensation-primary-commit`. The modelRoles part carries its table header. Every module's `dependencies:` list is rewritten by the old-to-deployed map read from this table; a dependency that maps to nothing refuses the run. Edited parts are recorded in `splits/index.tsv` (columns cut_sha256, edited_sha256, edit). The duplicate-stem refusal compares deployed names, so it fires only on a stem repeated within one type.

## Migration

Script: `flows/aa887c/scripts/migrate-skills.sh` (`--dry-run` lists every write). Split texts: `flows/aa887c/scripts/splits/`.

## Sources

- Book «Three skill repositories and the main workspace», https://claude.ai/artifact/6zgqzzzrUWwsotzHokqUNp
- /home/li/primary/flows/bad807/reports/books.md
- /home/li/primary/flows/28d847/reports/skill-kinds.md
- /git/github.com/LiGoldragon/Curriculum/skills/*.md at c7d35e2
- /home/li/primary/Vision/*.md, /home/li/primary/Intent/*.md
- Provenance receipt: unavailable.
