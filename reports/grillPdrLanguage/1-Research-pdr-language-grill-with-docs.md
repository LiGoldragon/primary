# Research — PDR language and grill-with-docs adaptation

## 1. Files read

Required startup:

- `AGENTS.md`
- `skills/skills.nota`
- `skills/subagent-session-workflow.md`
- `.agents/skills/intent-led-orchestration/SKILL.md`
- `.agents/skills/subagent-session-workflow/SKILL.md`

Additional local skills selected:

- `skills/spirit-cli.md`
- `skills/intent-log.md`
- `skills/reporting.md`
- `skills/report-naming.md`
- `skills/repository-management.md`
- `skills/skill-editor.md`
- `skills/editor.md`
- `skills/workspace-vocabulary.md`
- `skills/intent-led-orchestration.md`
- `skills/human-interaction.md`
- `skills/autonomous-agent.md`
- `skills/bead-weaver.md`
- `skills/session-lanes.md`
- `skills/context-maintenance.md`

Local primary reports read:

- `reports/operator/461-Research-ai-coding-workflows-matt-pocock.md`
- `reports/operator/462-Research-psyche-alignment-session-management/1-pocock-project-and-session-lifecycle.md`
- `reports/designer/728-Design-alignment-interview-method-and-skill-realignment-2026-06-24.md`

Matt Pocock repo files read from local clone `/git/github.com/mattpocock/skills`:

- `README.md`
- `CONTEXT.md`
- `docs/adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md`
- `skills/engineering/grill-with-docs/SKILL.md`
- `skills/engineering/domain-modeling/SKILL.md`
- `skills/engineering/domain-modeling/CONTEXT-FORMAT.md`
- `skills/engineering/domain-modeling/ADR-FORMAT.md`
- `skills/productivity/grilling/SKILL.md`
- `skills/engineering/to-prd/SKILL.md`
- `skills/engineering/to-issues/SKILL.md`
- `skills/engineering/ask-matt/SKILL.md`
- `skills/engineering/setup-matt-pocock-skills/domain.md`
- `skills/deprecated/ubiquitous-language/SKILL.md`

Web sources checked:

- Matt Pocock skills repo: `https://github.com/mattpocock/skills`
- Raw `grill-with-docs`: `https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/grill-with-docs/SKILL.md`
- Raw `domain-modeling`: `https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/domain-modeling/SKILL.md`
- Raw `grilling`: `https://raw.githubusercontent.com/mattpocock/skills/main/skills/productivity/grilling/SKILL.md`
- Raw `to-prd`: `https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/to-prd/SKILL.md`
- AI Hero article: `https://www.aihero.dev/grill-with-docs`
- AI Hero failure-modes article: `https://www.aihero.dev/things-people-get-wrong-with-grill-me-and-grill-with-docs`
- GitHub issue 130 on `CONTEXT.md` being treated as PRD/plan: `https://github.com/mattpocock/skills/issues/130`

## 2. Skills selected and why

- `subagent-session-workflow`: required by brief; governs this worker's lane, claim, report, return, and no-commit exception.
- `intent-led-orchestration`: explicitly canonical for the requested workflow; used to map findings back to lead/subagent behavior and subject-understanding gate.
- `spirit-cli` and `intent-log`: required because the brief instructed Spirit-first referent handling.
- `reporting` and `report-naming`: substantive output belongs in the lane report.
- `repository-management`: public repo clone through the local `ghq` layout.
- `editor`: source-grounded synthesis with uncertainty separated from claims.
- `workspace-vocabulary` and `skill-editor`: the request is about ubiquitous language and concrete skill edits, without editing now.
- `human-interaction`, `autonomous-agent`, `bead-weaver`, `session-lanes`, `context-maintenance`: local workflow surfaces that constrain where the Pocock pattern can land.

## 3. Commands run and outcomes

- Read required and selected files with `sed` and `rg`.
- Queried Spirit first:
  - `PublicTextSearch PDR`: no matching record.
  - `PublicTextSearch grill-with-docs`: found record `l7kt`, saying intent-led orchestration and grilling periodically dispatch a Spirit-maintenance subagent for psyche answers.
  - `PublicTextSearch [Matt Pocock]`: no exact useful Matt-specific record; results were broad unrelated matches.
  - `PublicTextSearch [ubiquitous language]`: broad vocabulary/domain records, with the strongest local fit being plain-language and workspace-vocabulary guidance.
- Located Matt Pocock's public repo through web search and GitHub.
- Confirmed GitHub canonical user casing with `gh api users/mattpocock --jq .login`: `mattpocock`.
- Claimed `/git/github.com/mattpocock/skills` with orchestrate for clone/explore.
- Cloned via `ghq get https://github.com/mattpocock/skills`.
- Confirmed local clone path with `ghq list -p`.
- Retrieved upstream main commit through GitHub API: `5d78bd0903420f97c791f834201e550c765699f8`.
- Searched primary for `PDR`, `PRD`, `grill`, `ubiquitous`, `glossary`, `CONTEXT.md`, `ADR`, `alignment report`, and related terms.
- Checked `jj status`: primary working copy was clean before this report.
- Tried `orchestrate "(Observe Claims)"`; the CLI rejected it because `Claims` is not a valid ordinary observation variant.

## 4. Files changed or created

- Created this report: `reports/grillPdrLanguage/1-Research-pdr-language-grill-with-docs.md`.
- Created external public clone: `/git/github.com/mattpocock/skills`.
- No primary skills were edited.
- No commit was made.

## 5. Dependency graph

Goal: improve primary skill behavior by copying Pocock's `grill-with-docs` more directly, focused on ubiquitous language and concrete skill edits.

Current gate:

1. Subject-understanding report, this file.
2. Psyche decision: choose the local canonical term and artifact for Pocock's PRD step.
3. Editing design worker: draft exact skill edits, no commit unless separately authorized.
4. Spirit-maintenance worker, if psyche answers settle durable vocabulary or workflow intent.
5. Skill-edit worker: land approved edits.
6. Verification worker: run targeted grep checks and a dry-run prompt review against the edited skills.
7. Optional bead-weaver worker: if the edits imply multi-step rollout, file a dependency graph of implementation beads.

Likely edit sequence if approved:

1. Update `skills/workspace-vocabulary.md` with the canonical alignment terms: probably `alignment report`, `dependency graph`, `ubiquitous language`, and a bridge from `PRD` as the external Pocock term.
2. Update `skills/intent-led-orchestration.md` so the lead protocol explicitly mirrors `grill-with-docs`: one focused question with recommendation, use workers for mechanically discoverable answers, preserve resolved language in the correct durable surface, and require a destination artifact before implementation slicing.
3. Update `skills/subagent-session-workflow.md` so subject-understanding workers identify glossary/durable-language targets and distinguish sourced facts from inferences in returns.
4. Update `skills/reporting.md` only if the psyche ratifies `alignment report` as the local PRD analogue and wants that term added to report lifecycle language.
5. Update `skills/bead-weaver.md` to reference the alignment report as the source artifact for vertical-slice dependency graphs, if not already clear enough.
6. Update `skills/skills.nota` descriptions only if any edited skill's trigger changes.

## 6. Implementation summary, subject explanation, or findings

### Current ground truth: sourced facts

Spirit contains no public record matching `PDR`. Spirit does contain `l7kt`, a public principle tying intent-led orchestration/grilling to periodic Spirit-maintenance workers for psyche answers.

Matt Pocock's relevant artifact is `mattpocock/skills`, not a large implementation repo. `grill-with-docs` itself is a tiny wrapper: run `grilling` using `domain-modeling`. The cloned repo is at `/git/github.com/mattpocock/skills`; upstream URL is `https://github.com/mattpocock/skills`; upstream main commit observed through GitHub API is `5d78bd0903420f97c791f834201e550c765699f8`.

`grilling` is the interview loop: ask one question at a time, resolve the design tree dependency by dependency, include a recommended answer, and inspect the codebase instead of asking when code can answer.

`domain-modeling` is the documentation side: challenge conflicting glossary language, sharpen fuzzy or overloaded terms, stress-test relationships with concrete scenarios, cross-reference code, update `CONTEXT.md` inline when a term resolves, and create ADRs only for hard-to-reverse, surprising, trade-off decisions.

Matt's current shared-language artifact is `CONTEXT.md`, not `UBIQUITOUS_LANGUAGE.md`. The old `ubiquitous-language` skill is in `skills/deprecated/`; it wrote `UBIQUITOUS_LANGUAGE.md`. The current approach folds that behavior into `domain-modeling` and `CONTEXT.md`.

Matt's PRD step is `to-prd`: after grilling, synthesize the current conversation and codebase understanding into a PRD, use glossary vocabulary, respect ADRs, confirm test seams, and include problem statement, solution, user stories, implementation decisions, testing decisions, out-of-scope, and notes. It is not an interview step.

Primary already has two local reports on this topic. Report `461` maps Pocock PRD to a destination report or repo design surface, not to `INTENT.md`. Report `462` says primary should not import `.scratch/` as a parallel tracker and should map issues to beads or successor work tracking. Report `728` records a local vocabulary preference: say `alignment report`, not `PRD`, and `dependency graph`, not Kanban/DAG jargon, in psyche-facing primary work.

No current `skills/alignment-interview.md` exists. The active local home for this behavior is `skills/intent-led-orchestration.md`.

Primary's current agreed-language surface is `skills/workspace-vocabulary.md` for load-bearing workspace terms, backed by Spirit for durable psyche intent. Reports are transitional working surfaces; durable rules migrate into skills, architecture files, repo `INTENT.md`, or Spirit.

### Current ground truth: inferences

The prompt's `PDR` likely means `PRD` in Matt Pocock terms, because every Matt artifact and primary report uses PRD, while `PDR` has no Spirit or targeted workspace hit. Confidence: medium-high. It could also be a local acronym the psyche has not yet recorded or a deliberate renaming. Because the prompt says "Intent-led work must first set a PDR" and asks what it stands for, this should be resolved by asking the psyche before editing skills.

For primary, the best local analogue of Matt's `CONTEXT.md` is not a new root `CONTEXT.md` by default. The closest existing durable glossary is `skills/workspace-vocabulary.md`, with Spirit as the source for settled intent. A new local context artifact might still be useful for specific code repos, but adding one to primary would create a third vocabulary surface unless the psyche explicitly wants that.

For primary, the best local analogue of Matt's PRD is probably `alignment report`: a destination report that records resolved language, problem/solution, decisions, out-of-scope, testing/proof approach, and the initial dependency graph. It should not be treated as durable intent by itself.

The key Pocock behavior primary does not yet express directly enough is "active language refinement during grilling." `intent-led-orchestration.md` has the subject-understanding gate and focused-question discipline, but it does not yet say that fuzzy terms should be challenged and recorded in the glossary surface as they crystallize.

### PDR finding

Definition likely intended:

- External Pocock term: `PRD`, Product Requirements Document.
- Primary-facing candidate term: `alignment report`, a destination report written after the alignment/grilling phase and before implementation slicing.

Required contents before work proceeds, if copying Matt directly but translating to primary:

- problem statement from the psyche/user perspective;
- solution statement from the psyche/user perspective;
- resolved ubiquitous-language terms and avoided synonyms, or a pointer to the glossary edits that settled them;
- implementation decisions, including touched modules/interfaces at concept level, not brittle file-path detail;
- testing/proof decisions, including the highest useful seam or witness;
- out-of-scope decisions as the definition of done;
- open ambiguities that block implementation;
- initial dependency graph / vertical slices, or enough substance for `bead-weaver` to create it.

Confidence:

- High that Matt's artifact is PRD and not PDR.
- Medium that primary should name it `alignment report`, because report `728` says that explicitly but the current psyche prompt reintroduces `PDR`.
- Low that any acronym `PDR` is settled locally, because no Spirit/workspace hit was found.

Unresolved ambiguity:

- Whether the psyche wants to keep a local acronym `PDR`, correct to `PRD`, or avoid both by using `alignment report`.
- Whether "must first set a PDR" means before any implementation work, before any skill-edit work, or before the lead asks further non-mechanical psyche questions.

### Candidate local skill/edit targets

- `skills/workspace-vocabulary.md`: best home for settled ubiquitous-language terms that future agents must use. It should likely define `alignment report`, `dependency graph`, `ubiquitous language`, and how external `PRD` maps into primary.
- `skills/intent-led-orchestration.md`: canonical lead protocol. It should likely import the `grill-with-docs` discipline explicitly: one question at a time, recommended answer, code/subagent research before asking mechanically answerable questions, active term sharpening, and destination artifact before implementation slicing.
- `skills/subagent-session-workflow.md`: worker return shape can require sourced-facts-vs-inferences and candidate vocabulary/edit targets for subject-understanding gates like this one.
- `skills/reporting.md`: if `alignment report` becomes the PRD analogue, reporting needs enough guidance that future agents know this report is transitional and must later drain to intent/work/abandon.
- `skills/bead-weaver.md`: already says graph comes after aligned prompt/source report; may need a tighter bridge that an alignment report is the source for vertical-slice work.
- `skills/human-interaction.md`: may need only a pointer to the orchestration skill's active language-refinement behavior, not the full mechanics.
- `skills/skill-editor.md`: likely no substantive edit except perhaps enforcing that skill edits use canonical workspace vocabulary.
- `skills/skills.nota`: update descriptions only if triggers change after body edits.

### Subject in primary workspace terms

The subject is not "install Matt's skills." It is a local workflow refinement: make primary's intent-led orchestration behave more like `grill-with-docs` by treating alignment as active domain-language design. The lead should not simply ask clarifying questions; it should use workers to ground mechanically answerable facts, ask one focused psyche question with a recommendation for the remaining judgment, and make resolved terms land in the correct durable surface before implementation workers consume the plan.

Primary's durable stack changes the mapping:

- Pocock `CONTEXT.md` becomes primary `workspace-vocabulary` or repo-specific `skills.md`/`ARCHITECTURE.md`/`INTENT.md`, backed by Spirit.
- Pocock ADRs become primary architecture rationale or report-to-permanent-doc migration, with Spirit for durable psyche intent.
- Pocock PRD becomes primary `alignment report` or design report, then bead/dependency graph.
- Pocock issues become beads or the current successor work tracker.

## 7. Verification performed

- Confirmed Spirit query behavior for requested referents.
- Confirmed public repo clone exists at `/git/github.com/mattpocock/skills`.
- Confirmed upstream repo URL and main commit through GitHub API.
- Cross-checked Matt repo files against the AI Hero article and raw GitHub content.
- Searched primary skills/reports for `PDR`; no targeted hit.
- Searched primary skills/reports for `PRD`, `alignment report`, `grill`, `ubiquitous`, `glossary`, and related terms.
- Verified primary working copy was clean before writing the report.

## 8. Commit/push outcome

No commit or push. The brief explicitly says exploration return only, no primary skill edits, and no commit.

## 9. Blockers or psyche questions

Best next psyche question:

Should primary name the required pre-implementation destination artifact `alignment report`, treating Matt Pocock's `PRD` as an external/source term and `PDR` as an unresolved or mistaken acronym?

Recommended answer:

Use `alignment report`. It matches the local plain-language preference already in `reports/designer/728-Design-alignment-interview-method-and-skill-realignment-2026-06-24.md`, avoids importing product-management jargon, and fits primary's report lifecycle: transitional report first, then drain durable intent to Spirit/permanent docs and work to a dependency graph.

Meaningful alternatives:

- Use `PRD` when copying Matt's workflow. This is closest to the source artifacts and easiest for agents familiar with Pocock's terms, but conflicts with local plain-language drift and risks agents treating it as a stale spec.
- Define a new `PDR` acronym if the psyche meant something specific. This should only happen if the psyche supplies the expansion and why it is better than `alignment report`, because no current Spirit/workspace record defines it.

## 10. Dirty-state changes observed

- Before report: `jj status` reported no changes.
- Created report-only file under `reports/grillPdrLanguage/`.
- Created external clone under `/git/github.com/mattpocock/skills`.
- No shared primary skill file changed.

## 11. Next concrete action

Ask the psyche the naming/artifact question above. If they choose `alignment report`, dispatch one editing-design worker to draft exact patches for `skills/workspace-vocabulary.md`, `skills/intent-led-orchestration.md`, `skills/subagent-session-workflow.md`, and possibly `skills/reporting.md`/`skills/bead-weaver.md`, with no commit until the psyche authorizes skill edits.
