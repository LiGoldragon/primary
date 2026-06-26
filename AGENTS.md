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

Default main-thread work follows this boot contract, the selected skills, and
the active Codex mode.

The constrained lead/subagent mode below applies only when
`.agents/skills/intent-led-orchestration` has triggered at fresh-context
startup. Inside that protocol, the lead stays in one of two modes:

1. **Delegate meaningful reading.** Any meaningful read beyond the skill index
   goes to a subagent with the full reading envelope: workspace files, skills,
   reports, commands, source locators, and return shape. The lead works from
   the helper's distilled result.
2. **Interact with the psyche.** If the next step needs judgment rather than
   delegated reading, ask the psyche focused questions or offer a concrete
   suggestion/clarification with the tradeoff stated plainly. When the request
   is in intent-led orchestration, follow that skill's alignment interview and
   execution gates rather than treating one clarification as enough.

Inside the intent-led orchestration protocol, meaningful reading includes
startup orientation, report triage, broad repo inspection, codebase exploration,
intent refresh, and multi-file context gathering. The lead may do small
mechanical checks needed to dispatch, verify a helper result, edit an explicitly
named file, or commit/push the finished change.

## Skill Index

`skills/skills.nota` is the discovery path. Query it by topic; do not scan
`skills/`. When a skill triggers, follow that skill. If a skill's required
reading is broad, dispatch that reading through a helper only when
`.agents/skills/intent-led-orchestration` is active or the psyche has asked for
delegation.

## Intent

The psyche is the human. Agent messages and agent-written files are not psyche.
When durable intent is clear, capture it through Spirit according to the
triggered intent skills. When intent is unclear, ask instead of inferring.
For psyche-facing goal shaping and orchestration that explicitly enters
intent-led orchestration, route through
`.agents/skills/intent-led-orchestration`; it points to the canonical active
protocol in `skills/intent-led-orchestration.md` for turning a request into an
executable dependency graph. Inside that protocol, implementation planning,
implementation-worker dispatch, file edits, report writing, commits, and pushes
wait until the psyche has explicitly locked alignment and then explicitly
approved the method or dispatch plan.

## Output

Chat and harness output are the primary transient artifacts. Do not write a
manual report merely because an answer is substantive; ordinary findings,
implementation summaries, validation output, and return schemas can live in
chat or the harness stream and be archived programmatically later.

Write a report only when the report itself is the requested or necessary
working surface: a fresh-context handoff, cross-agent design pickup point,
subagent exploration that must survive the current harness output, or a
durable analysis artifact that cannot fit in the answer. When a report exists,
chat carries its path plus the user-attention items: open questions, blockers,
and recommendations restated with enough substance to answer without opening
the report.

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
