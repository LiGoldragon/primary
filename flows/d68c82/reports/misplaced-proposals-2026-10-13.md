# Misplaced modules and proposals to the living — audit 2026-10-13

Everything below was witnessed by this subflow (read or run on 2026-10-13) unless marked *inference*.
Sources read: psyche-context (parent 8bd55fe, clean), mind-context (parent 344f6c3, uncommitted edits to
operation-book, operation-flashbook, operation-main-flow), field-context (parent 1607152, clean);
`psyche-skills`, `mind-skills`, `field-skills` are symlinks to these three. Primary: `.claude/skills`,
`subagents/`, `tools/main-flow-mode/`, `config/main-flow/*.edn`, and the 23 book sources below.

## 1. Misplaced modules

No module sits in the wrong repository by type: psyche-context holds only spirit-/intent-/vision- (38 in
`skills/`, plus `vision/ethos.md` = vision-ethos); mind-context holds knowledge- (13) and operation- (32);
field-context holds compensation- (20) and trial- (10). There are no `primary/` or `subagents/` module
dirs in the three repos; Primary `subagents/book.md`, `book-page.md`, `book-reader.md` are untyped subflow
definitions.

### Retired types still present (42 source files; 44 in the generated `.claude/skills`)

| type | current repo | files | proper repo |
|---|---|---|---|
| operation- | mind-context | agent-harness-packaging, beads, book, clojure-development, design, disk-hygiene, documentation-placement, edit-coordination, feature-development, file-editing, flashbook, flashbook-illustration, flow-evidence, lojix, main-flow, nix-input-upgrade, nix-workflow, operating-system, orchestrate, prompt-crafting, psyche-acquisition, psyche-distillation, psyche-grasp, psyche-interraction, realization, relaying-the-living, repository-lifecycle, secrets, skill-designing, stale-lock, testing, transcript-search (32) | type retired; no destination ruled. Reviewed lines → psyche-context vision-/intent-; unreviewed procedure → mind knowledge-/inquiry- or field compensation- (*inference* from the brief's rule) |
| trial- | field-context | contact-discipline, generated-projection, independent-review, low-power, presentation-book, psyche-injection, questions-book, reaping, succession, unblocking-commands (10) | type retired; field-context as compensation- or removed (*inference*) |
| trial- | generated `.claude/skills` only | trial-no-polling, trial-recurring-failure | no source in any repo: stale generated output |

### Names that do not exist

| file | reference | kind |
|---|---|---|
| psyche-context/skills/spirit-core.md:3 | compensation-book-crystallization | frontmatter dependency (field has compensation-book-distillation) |
| psyche-context/skills/vision-crystallization.md:3 | operation-psyche-crystallization | frontmatter dependency (mind has operation-psyche-distillation) |
| psyche-context/vision/ethos.md:8, :28 | vision-flow-ethos | body reference |
| Primary subagents/book-page.md:21, :214, :242 | operation-psyche-crystallization | load instruction to the book subflow |
| Primary `.claude/skills/vision-distillation` | (source renamed vision-crystallization) | stale generated module; `intent-main-flow` and `vision-crystallization` absent from the generated tree |

Dependencies that point at retired types (names exist): psyche-context intent-testing:3 (operation-testing),
vision-crystallization:3, intent-psyche-interaction:3 (operation-psyche-interraction), vision-orchestrate:3
(operation-orchestrate), vision-x11:3 (operation-operating-system); field-context compensation-breaking-upgrades:3,
compensation-nix:3, compensation-testing:3, trial-presentation-book:3, trial-generated-projection:3; plus 13
operation- modules depending on each other.

`curriculum 'ResolveSkills.[ … Psyche startup list … ]'` returned `vision-distillation` and resolves
spirit-core to compensation-book-distillation: Curriculum serves a snapshot older than the sources.

## 2. Sentences that route a proposal to the living toward a non-psyche module

Load status, from `config/main-flow/psyche.edn`, `launch-config.mjs:56`, `spirit-system-prompt.mjs:20-31` and
`claude-main-flow-launch.mjs:274-278`, for a Claude Psyche Secondary launched today:
SYSTEM = `tools/main-flow-mode/system-prompt.md` + spirit-core, intent-main-flow, intent-psyche-interaction,
intent-psyche (read from the psyche-skills working copy). STARTUP USER PROMPT = the configured user list plus
its Curriculum closure (witnessed: operation-main-flow, operation-psyche-interraction,
operation-psyche-distillation, operation-edit-coordination, operation-orchestrate, knowledge-psyche,
knowledge-vocabulary, vision-book, vision-distillation, vision-aspects, vision-model-roles, vision-messaging,
compensation-book-distillation, -behavior, -correction, -truth, -orders, -prose, -understanding, -launch,
-design, -default-effort, -messenger-clj, -temporary, intent-design, intent-models, knowledge-protos,
knowledge-datom). Everything else is on demand. d68c82 itself was launched 2026-10-10; its actual seat
prompt was not found under `~/.claude/jobs` (earliest prompt file there is 10-12), so what it really
received is unobserved.

### Directing or allowing

| # | file:line | sentence (verbatim) | load |
|---|---|---|---|
| A1 | mind-context/skills/operation-psyche-interraction.md:100 | "When the psyche corrects how a flow behaves, the same reply presents the line for the owning skill. A correction that reaches only a vision file reaches no later flow." | startup user prompt |
| A2 | mind-context/skills/operation-psyche-interraction.md:91 | "A proposal names the module, the lines removed, and the lines that replace them, verbatim." | startup user prompt |
| A3 | mind-context/skills/operation-psyche-distillation.md:29-31 | "A distilled statement lands as lines in a vision-, intent- or other skill's authored source on the living's explicit approval, and never before." | startup user prompt (Curriculum closure) |
| A4 | field-context/skills/compensation-book-distillation.md:6 | "Every book the living reads is distillation proposals, 99% of it: each section names the file, the lines removed and the lines added, and asks a ruling; …" | startup user prompt |
| A5 | field-context/skills/compensation-book-distillation.md:8 | "…the authored file targeted by a proposal stays named." | startup user prompt |
| A6 | psyche-context/skills/intent-main-flow.md:13 = tools/main-flow-mode/system-prompt.md:7 | "When the living points out a fault, the reply gives its cause and the line that changes the behavior that produced it; repairing the faulty artifact comes second, and never stands in for the behavior change." (target unnamed; the behavior lives mostly in machine modules) | SYSTEM |
| A7 | field-context/skills/compensation-correction.md:10 | "Fix the file that sentence came from, or should have come from, before fixing the output." | startup user prompt (spirit-core dependency) |
| A8 | mind-context/skills/operation-main-flow.md:38 and operation-design.md:11 | "Whatever the psyche must read, rule on or approve goes whole into the living messenger as a presentation; a proposal is revised there until the psyche approves a landing." | main-flow: startup; design: on demand |
| A9 | mind-context/skills/operation-skill-designing.md:59 | "An `operation-` skill is deployed when the living describes what he wants a skill to do or to change; the primary Mind seat reviews and interprets it, and no glance from the living is needed." | on demand |
| A10 | mind-context/skills/operation-skill-designing.md:62 | "Compensation and trial skills are machine-authored without the living in the loop, refined as they are used and reviewed, and upgraded into operation, knowledge, vision or intent skills." | on demand |
| A11 | field-context/skills/compensation-launch.md:30 | "…the sender finds why it misjudged, and that finding is proposed as a skill change." | startup user prompt |
| A12 | mind-context/README.md:7-8; field-context/README.md:7-8 | "Another aspect's flow that wants a change contacts Mind [Field], which investigates it and brings a change to the living." | not loaded (read on demand) |
| A13 | psyche-context/skills/vision-book.md:8 | "Every book has a crystallization section: it proposes the lines that move the living's words into vision, intent and spirit skills." (restricts the living's words to psyche, but gives no rule that a book carries nothing else; the generated copy reads "distillation section") | startup user prompt (generated copy) |
| A14 | Primary subagents/book.md:25 | "Every book has a nonempty crystallization section proposing skill lines and their authored targets." | book subflow only |
| A15 | Primary subagents/book.md:56 | "The file it targets, named in the section, is a chip: …" | book subflow only |
| A16 | Primary subagents/book-page.md:228-233 | "`skill` with a kind and a skill name: how flows should work. Kinds, as the living drew them: Operation, how flows operate, made by Mind with the living involved; Documentation, how a tool is used, made by Mind; Compensation, making up for how models tend to go wrong, the field's; Trial, a compensation skill still being tried." | book-page subflow only |
| A17 | Primary subagents/book-page.md:240-243 | "`Approved` … return it to the caller, who lands it (vision through the `operation-psyche-crystallization` skill; a skill through the seat that owns it)." | book-page subflow only |

`spirit-system-prompt.mjs` carries no routing sentence; it selects modules (the 10-13 book «Where the green
went» P4 proposes adding compensation-book-distillation to the Psyche SYSTEM).

### Saying the opposite

| # | file:line | sentence (verbatim) | load |
|---|---|---|---|
| O1 | psyche-context/skills/intent-psyche.md:16 | "Anything the living has reviewed is psyche: a line he approves is a vision statement at least, whatever module proposed it, and leaves the mind or field module it sat in. A line he has not reviewed is a machine line." | SYSTEM |
| O2 | field-context/skills/compensation-orders.md:10 | "…a book is the route for changes to psyche data and psyche skills, never a gate on a repair." | startup user prompt |
| O3 | field-context/skills/compensation-orders.md:13-16 | "A trial or compensation skill is read whole and rewritten as one body that carries it; a psyche skill's change is proposed in a book; a skill or code another flow owns is handed to that flow." | startup user prompt |
| O4 | field-context/skills/compensation-design.md:6-10 | psyche data "changes only by an edit the living has reviewed and approved … The change is written as a proposal in a book." | startup user prompt |
| O5 | mind-context/skills/operation-skill-designing.md:57 | "A `vision-` or `intent-` skill is gold: the living's approved words, changed only on the living's word." | on demand |

No sentence anywhere says positively that a book proposes only psyche lines; O1 is the only statement of the
consequence, and it describes a reviewed line, not what may be shown. A1, A2, A4 and A6 sit beside it in the
same seat prompt and name a module or file without restricting its type.

## 3. Book proposals targeting non-psyche modules

The index lists 23 books, all dated 2026-10-13 (none 10-12). Sources: 33752b/books/22-41 except 34,
d68c82/books/8-10, d55c56/books/2.

| book (source) | proposal | target |
|---|---|---|
| Where the green went (d68c82/9) | 1, 2 | field compensation-book-distillation |
| | 3 | tools/book-check.mjs |
| | 4 | tools/main-flow-mode/spirit-system-prompt.mjs |
| Why Fable was not refreshed (d68c82/8) | 1 | tools/main-flow-mode/system-prompt.md |
| | 2 | mind operation-main-flow |
| | 3 | field compensation-launch |
| | 4 | compensation-correction (named "mind-context"; it is in field-context) |
| Tools instead of scripts (33752b/39) | 1-4 | transcript tool; Flow and census; component-evidence; book renderer (P5 no target) |
| Three lines from the chat, second edition (36) | 1 | tools/main-flow-mode/system-prompt.md |
| Three lines from the chat (31) | 1 | tools/main-flow-mode/system-prompt.md |
| Crystallization (35) | 2 | mind operation-psyche-distillation merged into vision-crystallization (mixed) |
| | 3 | renames of operation-/compensation- modules, book checker, Primary tools |
| Figures that move (32) | 2 | Primary book agent's drawer brief |
| Short-term and long-term vision (30) | 2, 3 | mind knowledge-psyche; mind knowledge-vocabulary |
| Makeshift, from Core (28) | 2, 3 | mind knowledge-psyche; mind knowledge-vocabulary |
| Makeshift, from Spirit (d55c56/2) | 2 | mind knowledge-psyche |
| Makeshift and goalpost (27) | 2 | mind knowledge-vocabulary |
| Context modules (24) | 2 | mind operation-skill-designing |
| Context modules, second edition (29) | 2 | mind operation-skill-designing |
| Handover and the seat without a shovel (22) | 1, 2 | mind operation-main-flow; field trial-succession |
| Cleaning up the skills (23) | 1-19 | removals in mind/field modules (P13 and P18 also name a vision candidate; P19 also Primary CLAUDE.md) |
| | Rulings 1, 2 | lines in mind operation-prompt-crafting and knowledge-codex-harness |

Totals: 46 proposals plus 2 rulings, in 15 of 23 books. Books with only psyche targets: A guarded compaction
request, Flow: short term and long term, What compaction keeps, Three lines third edition, Short term and long
term, What you review is psyche, Cleaning up the skills second edition (lines move into vision modules and leave
the machine module), Tripping over the shoelaces (P1 names a term with no target).
