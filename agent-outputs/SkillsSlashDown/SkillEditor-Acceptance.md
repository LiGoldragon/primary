# Skill slash-down acceptance

## Task and scope

Continued the skills slash-down from the canonical skills source repo. Applied the new psyche directive against response/output-shape boilerplate, specifically removing the `context-handover` `## Shape` template with `Intent:`, `Useful context:`, and `Open decisions:`. Reconciled generated runtime surfaces in the primary workspace, validated, committed, and pushed the source and generated changes.

## Skills touched and selection reason

- `context-handover`: required by brief; removed response-template boilerplate and tightened handover rules.
- `architectural-truth-tests`: selected for extreme line count, See Also section, examples/tutorial bloat, and status/prose-heavy explanations.
- `workspace-update-report`: selected for local path examples, report-template bloat, Spirit/report references, and high line count.
- `language-design`: selected for high line count, tutorial tone, See Also section, and duplicate scope restatement.
- `mermaid`: selected for high line count, tutorial examples, See Also section, and report-specific prose.
- `abstractions`: selected for high line count, See Also section, external/provenance-style citations, and duplicated examples.
- `human-interaction`: selected for required audit fix; manifest description no longer references other skills, and body response-shape boilerplate was removed.
- `contract-repo`: selected for required audit fix; manifest description no longer advertises pruned details absent from the body.

## Changed files by repo

skills source repo:

- `manifests/active-outputs.nota`
- `manifests/skills-roster.nota`
- `modules/abstractions/full.md`
- `modules/architectural-truth-tests/full.md`
- `modules/context-handover/full.md`
- `modules/human-interaction/full.md`
- `modules/language-design/full.md`
- `modules/mermaid/full.md`
- `modules/workspace-update-report/full.md`

primary generated runtime surfaces:

- `.agents/skills/abstractions/SKILL.md`
- `.agents/skills/architectural-truth-tests/SKILL.md`
- `.agents/skills/context-handover/SKILL.md`
- `.agents/skills/contract-repo/SKILL.md`
- `.agents/skills/human-interaction/SKILL.md`
- `.agents/skills/language-design/SKILL.md`
- `.agents/skills/mermaid/SKILL.md`
- `.agents/skills/workspace-update-report/SKILL.md`
- `.claude/skills/abstractions/SKILL.md`
- `.claude/skills/architectural-truth-tests/SKILL.md`
- `.claude/skills/context-handover/SKILL.md`
- `.claude/skills/contract-repo/SKILL.md`
- `.claude/skills/human-interaction/SKILL.md`
- `.claude/skills/language-design/SKILL.md`
- `.claude/skills/mermaid/SKILL.md`
- `.claude/skills/workspace-update-report/SKILL.md`
- `.claude/agents/rust-auditor.md`
- `.codex/agents/rust-auditor.toml`
- `.pi/agents/rust-auditor.md`

## Commits and push state

- skills source repo: `2acbe6a911c8b0d814f01d612855763f7ee0c30f` — `skill-editor: prune response-boilerplate batch` — pushed; dry-run confirmed `main@origin` matches `main`.
- primary repo: `f1c41fdc6c84e32752fec6b7d17b039805172069` — `skills: reconcile response-boilerplate prune` — pushed; dry-run confirmed `main@origin` matches `main`.

## Final generated body line counts

- context-handover: 38
- architectural-truth-tests: 62
- workspace-update-report: 45
- language-design: 65
- mermaid: 48
- abstractions: 49
- human-interaction: 39
- contract-repo: 52

## Validation commands and results

- `cargo run -- skills-generate.nota`: failed before generation because `SKILLS_SOURCE_ROOT` was not set; rerun with required environment succeeded.
- `SKILLS_SOURCE_ROOT=$PWD SKILLS_WORKSPACE_ROOT=/home/li/primary cargo run -- skills-generate.nota`: passed; regenerated configured runtime outputs.
- `SKILLS_SOURCE_ROOT=$PWD SKILLS_WORKSPACE_ROOT=/home/li/primary cargo run -- skills-check.nota`: passed; generated outputs checked without drift.
- `cargo test`: passed; 16 integration tests passed.
- Forbidden-pattern scan over touched source and generated skill bodies: passed for See Also, `## Shape`, called-out section labels, local paths, URLs, commit-hash language, temporal roadmap markers, provenance markers, and generated-file notices.
- Response-format-boilerplate scan over touched source and generated skill bodies: passed for `Intent:`, `Useful context:`, `Open decisions:`, compact-prompt instructions, response-format phrasing, and section-addition phrasing.
- Unique-heading scan over touched source and generated skill bodies: passed.
- Source-frontmatter scan over touched source modules: passed.
- Module-dependency path existence scan: passed.
- `jj status --no-pager` in skills source repo after commit/push: clean.
- `jj status --no-pager` in primary after generated commit/push: only pre-existing unrelated dirty files remain.

## Residual risks and blockers

No blocker or psyche decision is needed before reintroducing content. Reintroduction should happen only if a deleted rule is non-obvious, current, operational, and belongs in skill source rather than a repo document.

Unrelated primary working-copy files were left uncommitted: `agent-outputs/CriomeAuthWitness/CriomosImplementer-WitnessRunEvidence.md`, `agent-outputs/SkillBatchPrune/SkillEditor-Acceptance.md`, and `reports/legacy-disposition/HANDOVER-2026-06-29-spirit-matter-enforcement.md`.

This acceptance artifact is a worker output and was written after the primary generated-surface commit.
