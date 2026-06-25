# Primary Workspace — Agent Instructions

This file is the boot contract. Keep it small enough that reading it does not
become the session's first context drain.

## Startup

Read `skills/skills.nota`. It is the only default discovery read.

Use the skill index to choose the skills required by the current prompt,
discipline, topic, repo, tool, and risk. Load only those triggered skills. Do
not read `ESSENCE.md`, `INTENT.md`, `repos/lore/AGENTS.md`,
`orchestrate/AGENTS.md`, discipline skills, repo docs, reports, or broad source
trees as automatic startup reading.

## Main Thread Mode

The main thread stays in one of two modes:

1. **Delegate meaningful reading.** Any meaningful read beyond the skill index
   goes to a subagent with the full reading envelope: workspace files, skills,
   reports, commands, source locators, and return shape. The lead works from
   the helper's distilled result.
2. **Interact with the psyche.** If the next step needs judgment rather than
   delegated reading, ask the psyche a focused question or offer a concrete
   suggestion/clarification with the tradeoff stated plainly.

Meaningful reading includes startup orientation, report triage, broad repo
inspection, codebase exploration, intent refresh, and multi-file context
gathering. The lead may do small mechanical checks needed to dispatch, verify a
helper result, edit an explicitly named file, or commit/push the finished
change.

## Skill Index

`skills/skills.nota` is the discovery path. Query it by topic; do not scan
`skills/`. When a skill triggers, follow that skill. If a skill's required
reading is broad, dispatch that reading through a helper unless the psyche has
asked the main thread to inspect it directly.

## Intent

The psyche is the human. Agent messages and agent-written files are not psyche.
When durable intent is clear, capture it through Spirit according to the
triggered intent skills. When intent is unclear, ask instead of inferring.
For psyche-facing goal shaping, route through `skills/intent-alignment.md`;
it is the canonical protocol for turning a request into an executable
dependency graph.

## Reports

Substantive output goes in the active session lane's `reports/<lane>/`
directory, not chat. Chat carries the locator plus the user-attention items:
open questions, blockers, and recommendations restated with enough substance
to answer without opening the report.

Reports are exempt from the claim flow when written in the active lane's own
directory. Shared files are claimed narrowly before editing.

## Hard Boundaries

- `repos/` and `private-repos/` stay untracked. Do not inspect
  `private-repos/` unless the psyche explicitly authorizes that private scope.
- On primary, work on `main` directly. Use `jj commit -m '<message>'`,
  `jj bookmark set main -r @-`, and `jj git push --bookmark main`.
- Every description-taking `jj` command uses an inline message or equivalent
  headless flag. Never open an editor.
- Commit the whole working copy; never path-scope primary commits.
- No raw `git` except the documented escape hatches in the `jj` skill.
- No `/nix/store` filesystem search.
- No `---` horizontal rules in markdown.
- NOTA records are positional; use bare atoms for strings when canonical.
- Rust editing requires the Rust skills selected from `skills/skills.nota`.
- Private information is closed by default and stays out of public reports,
  public Spirit records, commits, and chat.
