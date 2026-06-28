# Scout Skills Corpus Findings

## Task and scope

Survey the local skills corpus broadly, using the psyche's stated cleanup concerns as the lens: skills should be drastically shorter and should not carry local file paths, external references, See Also sections, generic manuals, obvious explanations, off-topic material, vaporware, or material that belongs in another skill. This is secondhand ground truth for an intent-led orchestrator; no source repos under `repos/` or `private-repos/` were inspected.

Primary corpus inspected: generated skill surfaces under `.agents/skills/*/SKILL.md`, with `.claude/skills/*/SKILL.md` checked for drift. `skills/generated-role-outputs.nota` was noted but not audited as a skill body.

## Commands consulted

- `find skills .agents/skills .claude/skills -name AGENTS.md -o -name '*.md' | sort | head -200`: identified `.agents/skills` and `.claude/skills` as the broad generated skill corpus; `skills/` itself contains only `skills/generated-role-outputs.nota`.
- `diff -qr .agents/skills .claude/skills`: found the two generated corpora differ only at `intent-led-orchestration/SKILL.md`.
- `find .agents/skills -maxdepth 2 -name SKILL.md | wc -l` and same for `.claude/skills`: 66 skill files in each generated corpus.
- `wc -l` over `.agents/skills/*/SKILL.md`: 15,824 total lines; top files include `component-triad` 1,165 lines, `reporting` 856, `kameo` 795, `actor-systems` 629, `prose` 590, `contract-repo` 576.
- Python metric scan over `.agents/skills`: 48/66 files exceed 100 lines, 37 exceed 150, 27 exceed 200, 18 exceed 300, 6 exceed 500, median 160, only 12 are 80 lines or shorter.
- `rg '^## See also' .agents/skills --glob 'SKILL.md'`: 60/66 skill files contain a `## See also` section.
- `rg` scans for `reports/`, `Spirit`, `intent`, local paths, URLs, `future`, `not yet`, `currently`, and old skill path references found the examples listed below.
- `jj status --no-pager`: before writing this scout output, the working copy had no changes.

## Blunt findings

### Critical: the corpus is massively over-length for skill loading

Observed: `.agents/skills` has 66 skill files totaling 15,824 lines. The median skill is 160 lines. Six files are over 500 lines: `.agents/skills/component-triad/SKILL.md` at 1,165 lines, `reporting` 856, `kameo` 795, `actor-systems` 629, `prose` 590, and `contract-repo` 576.

Interpretation: cleanup is not a polish pass. It is a compression and deletion pass. Many files are closer to manuals, design archives, or project status dossiers than skills.

### Critical: permanent skills contain provenance, report references, intent IDs, commit hashes, and “current branch” status

Examples:

- `.agents/skills/structural-forms/SKILL.md` cites Spirit IDs and reports directly: lines inspected include `Per Spirit 7c71`, `Per Spirit adnn`, `Per Spirit ov30`, `Concept: report 627`, `Reports 645, 647, 649`, and a `See also` bullet listing `reports/designer/627`, `639`, `640`/`643`, `645`/`649`, `655`/`658`.
- The same file records commit hashes and temporal state: `schema-next main as of 2026-06-18: af3705c ... 95f1ee7 ... 1de72dde` and “no longer the `next/structural-forms` epic branch.”
- `.agents/skills/component-triad/SKILL.md` cites intent IDs (`tb9h`, `7sx6`, `u7tj`) and carries current defect diagnosis: “spirit currently violates this”, “meta-signal-spirit is a stale, hand-written, non-schema-derived orphan,” and a proposed correction.
- `.agents/skills/abstractions/SKILL.md` points to `Spirit ov30`; `.agents/skills/reporting/SKILL.md` includes “per Spirit `<id>`” guidance; multiple skills name reports as examples.

Interpretation: this violates the local `skill-editor` rule that skills cite no reports and no intent records, and it is exactly the kind of stale-prone external anchoring the psyche wants removed. The skills are carrying history and proof trail instead of settled present-tense discipline.

### Critical: the generated skill surfaces are inconsistent

Observed: `.agents/skills` and `.claude/skills` both contain 66 skills, but `diff -qr` reports one drift: `.agents/skills/intent-led-orchestration/SKILL.md` differs from `.claude/skills/intent-led-orchestration/SKILL.md`. The `.agents` version is 81 lines and much tighter; the `.claude` version is 144 lines and still contains the older broader protocol text.

Interpretation: an intent-led orchestrator may load a different orchestration protocol depending on harness surface. Fixing only one generated target is unsafe until generation/source-of-truth is clarified.

### High: See Also sections are nearly universal

Observed: `rg '^## See also'` found 60 of 66 `.agents/skills/*/SKILL.md` files have `## See also`. Examples include `actor-systems`, `component-triad`, `kameo`, `reporting`, `skill-editor`, `prose`, `workspace-vocabulary`, `intent-log`, `spirit-cli`, `rust-methods`, and many others.

Interpretation: this is a corpus-wide structural problem, not a few bad endings. The current skills form a cross-reference web. The psyche’s desired shape appears to be self-contained, short skills without See Also tails.

### High: old or broken skill references exist

Observed examples:

- Old slash-style references appear although the generated corpus uses slug directories: `.agents/skills/rust-discipline/SKILL.md` says “five focused sub-files under `skills/rust/`” and links `skills/rust/methods.md`, `skills/rust/errors.md`, `skills/rust/storage-and-wire.md`, `skills/rust/parsers.md`, `skills/rust/crate-layout.md`. Generated files are instead `rust-methods`, `rust-errors`, `rust-storage-and-wire`, `rust-parsers`, `rust-crate-layout`.
- `.agents/skills/rust-crate-layout/SKILL.md`, `kameo`, `actor-systems`, `enum-contact-points`, `contract-repo`, `rust-methods`, and `rust-storage-and-wire` also reference `skills/rust/...` paths.
- `.agents/skills/secrets/SKILL.md` references `skills/system-operator.md`; no `.agents/skills/system-operator/SKILL.md` exists in the 66-skill corpus.
- `.agents/skills/prose/SKILL.md` references `skills/poet.md`; no `.agents/skills/poet/SKILL.md` exists.

Interpretation: even if references were allowed, several are stale or point outside the loaded corpus. This is high-risk for an orchestrator that should not chase local filesystem paths.

### High: local file paths and host-specific commands are embedded in skills

Examples:

- `.agents/skills/repository-management/SKILL.md` hard-codes `/git/<host>/<owner>/<repo>` and `~/primary/repos/<repo>`.
- `.agents/skills/workspace-update-report/SKILL.md` tells agents to run `ls /home/li/primary/reports/*/ | grep -E '\-Update-' | sort | tail -1`.
- `.agents/skills/reporting/SKILL.md` repeatedly names `~/primary/reports/<lane>/`, `reports/newLanesDesign/`, `reports/schemaWorkAudit/`, and report-number examples.
- `.agents/skills/rust-storage-and-wire/SKILL.md` names `~/primary/repos/signal` as a canonical reference.
- `.agents/skills/skill-editor/SKILL.md` names source and generated paths, including `/git/github.com/LiGoldragon/skills/modules/<name>/full.md`, `.agents/skills/<name>/SKILL.md`, and `.claude/skills/<name>/SKILL.md`.

Interpretation: paths may be locally true, but the psyche’s stated cleanup goal says they should not be in skill bodies. They also make generated skills non-portable and stale.

### High: several skills are generic manuals or external-tool references rather than workspace-specific discipline

Examples:

- `.agents/skills/kameo/SKILL.md` is 795 lines and includes Kameo API usage, spawn modes, mailbox capacity, `PreparedActor`, test patterns, anti-patterns, macro docs, and version details. Useful content exists, but it is mostly a framework field guide.
- `.agents/skills/reporting/SKILL.md` is 856 lines and includes extensive report front matter, naming, meta-report directories, artifact lifecycle, report draining, mermaid/reference details, and examples.
- `.agents/skills/prose/SKILL.md` is 590 lines of prose craft doctrine with Hemingway quotes, TheBookOfSol references, primary-source ratios, and broad writing advice. This is mostly a writing manual and literary style sheet, not compact workspace execution discipline.
- `.agents/skills/nota-schema-docs/SKILL.md` teaches pseudo-NOTA mechanics, includes a large example variant set, and links `manifests/active-outputs.nota`.

Interpretation: these may be valuable reference docs, but they should not be loaded as skills in their current form. Split “quick rule” from reference manual, or move manuals to docs/lore and leave skills as triggers plus non-obvious workspace rules.

### High: topic boundaries are porous; material belongs in other skills or repo docs

Examples:

- `.agents/skills/human-interaction/SKILL.md` contains two explicit residue notes: “Move to `skills/autonomous-agent.md` or a testing skill in a later prune item” and “Move to `skills/double-implementation-strategy.md` / orchestrate in a later prune item.” The file itself admits off-topic material was parked there “so no content is lost.”
- `.agents/skills/actor-systems/SKILL.md` contains Kameo 0.20 implementation gotchas that overlap with `.agents/skills/kameo/SKILL.md`.
- `.agents/skills/component-triad/SKILL.md` contains component status, repo naming tables, Signal/Nexus/SEMA runtime design, meta-signal migration diagnosis, lifecycle hooks, and future runtime work. This is at least several topics: packaging, runtime, wire protocol, migration status, and engine design.
- `.agents/skills/architecture-editor/SKILL.md` is partly ARCH writing discipline and partly a general policy for uncertainty sections and future design handling.

Interpretation: the cleanup should not only shorten. It should re-home or delete. Current files are often aggregation bins for adjacent concerns.

### High: vaporware and “current status” are mixed with rules

Examples:

- `.agents/skills/component-triad/SKILL.md` says “No schema-emitted daemon does this yet,” “not yet triad-shaped,” “next implementation arc,” and “Deferred deeper-runtime work.” It also asserts “Kameo adoption itself is NOT deferred: the engines are kameo actors now” without this scout verifying code.
- `.agents/skills/rust-storage-and-wire/SKILL.md` distinguishes “today's `criome` daemon” from the eventual Criome and says cross-machine signaling is deferred.
- `.agents/skills/architecture-editor/SKILL.md` standardizes “Possible future design” sections and says architecture/workspace skills can carry possible features and undecided designs.
- `.agents/skills/intent-manifestation/SKILL.md` says the process is “currently a periodic manual sweep” and has an “eventual target.”

Interpretation: some future-labeled content may be legitimate planning, but skills are not the right home for evolving implementation status or aspiration. An orchestrator relying on this corpus will be fed a blend of present discipline, unverified project state, and future architecture.

### High: internal contradiction around actor lifecycle/current Kameo state

Observed:

- `.agents/skills/kameo/SKILL.md` says supervised `spawn_in_thread` releases `wait_for_shutdown` before `Self::drop()` runs and warns to use `.spawn()` until an upstream hook lands.
- `.agents/skills/actor-systems/SKILL.md` later specifies a release-before-notify shutdown sequence and says “The framework guarantees this ordering,” and “By the time `wait_for_shutdown()` returns, every prior step has completed.”

Interpretation: this may be desired actor-system semantics versus current Kameo reality, but the skill surfaces do not clearly separate current framework truth from target architecture. This is dangerous because the same worker could load both and apply the wrong lifecycle guarantee.

### Medium: explanations of obvious mechanics and templates add weight

Examples:

- `.agents/skills/skill-editor/SKILL.md` spends many lines explaining what a skill file is, markdown structure, manifest descriptions, and example formatting.
- `.agents/skills/reporting/SKILL.md` explains chat vs report audiences, path naming, numbered report directories, front matter, and reference style in great detail.
- `.agents/skills/architecture-editor/SKILL.md` includes a full ARCH template and detailed prose on what an architecture file does and does not contain.
- `.agents/skills/nota-schema-docs/SKILL.md` teaches placeholder syntax and optional markers that could likely be a short convention.

Interpretation: some mechanics are workspace-specific, but they are over-taught. A trained agent does not need generic markdown or documentation-writing lessons repeated in every adjacent skill.

## Recommended cleanup strategy

1. **Declare generated source of truth first.** Resolve why `.agents/skills/intent-led-orchestration/SKILL.md` and `.claude/skills/intent-led-orchestration/SKILL.md` differ before broad edits. Otherwise cleanup may land in one loader surface only.
2. **Set a hard target size.** Default target: 40-80 lines per skill; exceptional ceiling 120. Anything over 200 lines requires split, move-to-reference, or deletion.
3. **Delete all `## See also` sections in one mechanical pass after preserving only indispensable inline pointers.** If a sibling rule is needed to obey the current skill, inline one sentence. Otherwise remove the tail.
4. **Strip provenance and temporal state.** Remove Spirit IDs, report IDs, commit hashes, branch names, “currently,” “as of,” “not landed,” and “next arc” status from skills. If still needed, move to reports, beads, architecture, or repo docs.
5. **Cut local paths and external references.** Replace host-specific paths with role names or commands only when the path itself is the subject. Remove deep file paths and generated-surface paths from normal skills.
6. **Separate rule from reference manual.** For `kameo`, `reporting`, `prose`, `component-triad`, `actor-systems`, and `contract-repo`, create a tiny skill that says the non-obvious workspace discipline and move long API/reference/design material out of skill loading.
7. **Re-home off-topic residue.** Start with admitted residue in `human-interaction`, Kameo overlap in `actor-systems`, runtime design in `component-triad`, and uncertainty-policy material in `architecture-editor`.
8. **Mark present-vs-future with a strict rule: skills only state current operational discipline.** Future design goes to architecture/report/beads, not skills. If a skill must include a target shape, label it as a prohibition or current requirement, not a roadmap.
9. **Run a final grep gate.** At minimum fail on `^## See also`, `reports/`, `Spirit \``, `intent \``, `/home/`, `~/`, `/git/`, `https?://`, `as of`, `currently`, `not yet`, `future`, `later prune`, and `TODO`, with deliberate allowlist only after human approval.

## Unknowns and residual risks

- I did not inspect `/git/github.com/LiGoldragon/skills/modules/...` source modules, only generated local skill surfaces under `.agents/skills` and `.claude/skills`.
- I did not inspect code repos under `repos/`, `private-repos/`, or external clone roots to verify whether “current” claims in the skills match code reality.
- Counts from regex scans are conservative for some categories and broad for others; examples above are hand-checked from local files.
- I did not determine which harness actually loads `.agents` versus `.claude` in this session.
- I wrote this required worker output file under `agent-outputs/SkillsCorpusCleanup/`, which is the only durable change made by this scout.
