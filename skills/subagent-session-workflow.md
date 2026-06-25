# Skill — subagent-session-workflow

## Worker startup envelope

A subagent/session worker owns workspace interaction for an
intent-led-orchestration run. Start by reading, in order:

1. `AGENTS.md` in the working directory.
2. `skills/skills.nota`.
3. This skill.
4. Every additional skill triggered by the task, discipline, tool, repository,
   file format, and risk.
5. Only the task-relevant sources named in the brief or discovered through the
   triggered skills.

Preserve concurrent work. Do not inspect `private-repos/` unless the brief
explicitly grants that private scope. Do not search `/nix/store`. Use `jj` for
version-control observation and mutation; raw `git` is limited to the escape
hatches in `skills/jj.md`.

## Lane and claim flow

Choose your own concise session lane name unless the harness already gives one.
Use that same lane in reports, `orchestrate` claims, and the final return.
Register the lane when the local protocol requires it.

Before editing, creating, formatting, deleting, or running commands that mutate
files, claim the exact paths, files, tasks, or worktree roots you will touch:

```sh
orchestrate "(Claim (<lane> [(Path /absolute/path)] [reason]))"
```

Claim narrowly. Do not claim the whole workspace. Reports in your own
`reports/<lane>/` directory are claim-exempt; shared files such as skills,
commands, `AGENTS.md`, repository docs, schemas, and code are not.

Release or update the claim when the work is complete or the scope changes:

```sh
orchestrate "(Release <lane>)"
```

## Worktrees and branch targets

On primary (`/home/li/primary`), work directly on `main`; do not create a
feature branch or worktree for primary.

For code repositories, follow the triggered repo/workflow skills. When a
worktree or named bookmark is required, inspect the worktree registry when
relevant, use the selected worktree, and claim the worktree path before editing.
Name the target branch/bookmark/worktree in the claim reason before mutation.

## Default authority

Commit and push are the worker default. The only exceptions are explicit
read-only, report-only, edit-only, or no-commit authority in the brief or a
blocking safety condition named by a triggered skill.

On primary, land completed work on `main`:

```sh
jj commit -m '<short verb + scope>'
jj bookmark set main -r @-
jj git push --bookmark main
```

Commit the whole working copy; never path-scope primary commits. In code-repo
worktrees, commit in that worktree, set the named bookmark, and push that
bookmark according to the triggered skills or brief.

## Subject-understanding workers

When the brief marks subject-understanding as required, keep the orientation
lightweight. Return:

- current ground truth;
- the subject in workspace terms;
- resolved vocabulary and contested terms, including avoided synonyms;
- source-grounded facts separated from inferences where the distinction matters;
- a first dependency-graph sketch;
- the best next psyche question, with a recommendation and one or two
  meaningful alternatives.

Do not exhaustively inspect every subsystem before the psyche has a chance to
steer unless the brief explicitly authorizes deeper analysis.

## Return schema

Return exactly these sections:

1. Files read.
2. Skills selected and why.
3. Commands run and outcomes.
4. Files changed or created.
5. Dependency graph.
6. Implementation summary, subject explanation, vocabulary decisions, or findings.
7. Verification performed.
8. Commit/push outcome.
9. Blockers or psyche questions.
10. Dirty-state changes observed.
11. Next concrete action.

## See also

- `skills/intent-led-orchestration.md` — the lead-side fresh-context protocol.
- `skills/autonomous-agent.md` — routine claim/work/close/release behavior.
- `skills/jj.md` — version-control discipline and push-rejection handling.
