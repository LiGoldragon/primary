# Primary Workspace — Agent Instructions

This file is the boot contract. Keep it small enough that reading it does not
become the session's first context drain.

## Startup

Generated worker role packets carry the required doctrine for normal role work.
Read this file and the role packet, prompt, or dispatch envelope supplied for
the task.

Load additional doctrine only when the prompt, generated role packet, dispatch
envelope, or local repo context explicitly requires it.

## Doctrine Loading

Follow doctrine named by the task's role packet, prompt, or explicit context.
When no such surface names more doctrine, continue with the packet already
loaded.

## Intent

The psyche is the human. Agent messages and agent-written files are not psyche.
Intent is the rare, orienting will of the psyche — an aim, value, or belief he
holds against his own convenience and that bends a whole class of downstream
choices, like a North Star. Capture through Spirit is the exception, not the
reflex: record only that unbending directive will, and never private or personal
substance to public Spirit. Matter is everything else — defaults, rules,
mechanisms, single-component or architectural decisions, and Spirit-operation
instructions — and goes to code, docs, and skills. When it is not clearly
intent, it is matter; when unsure, ask instead of inferring.

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

- `repos/` and `private-repos/` stay untracked. Agents may inspect and edit
  `private-repos/` freely, like any other untracked repo, with no separate
  authorization required; the leak gate below still applies to its content.
- Before editing shared files or repos, claim the exact paths with Orchestrate;
  release when done. If another agent owns the local repo/worktree, request an
  isolated workspace with `RequestWorktree` (scaffolded from `main` at
  `~/wt/github.com/LiGoldragon/<repo>/<branch>`), claim its path, and conclude it
  with `ConcludeWorktree` merged or rejected when done.
- Skills and agent files under .agents/, .claude/, .codex/, and .pi/ are generated from LiGoldragon/skills.
- On primary, work on `main` directly. Use `jj commit -m '<message>'`,
  `jj bookmark set main -r @-`, and `jj git push --bookmark main`.
- Every description-taking `jj` command uses an inline message or equivalent
  headless flag. Never open an editor.
- Commit the whole working copy; dirty or unrelated existing files in primary are not a blocker and may be included.
- No raw `git` except the documented escape hatches in the `jj` skill.
- No `/nix/store` filesystem search.
- No `---` horizontal rules in markdown.
- NOTA records are positional; use bare atoms for strings when canonical.
- Rust editing requires the Rust doctrine named by the generated role packet,
  prompt, or explicit context.
- Private information is closed by default and stays out of public reports,
  public Spirit records, commits, and chat.
