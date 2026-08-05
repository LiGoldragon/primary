## Hard Boundaries

- `repos/` and `private-repos/` stay untracked. Agents may inspect and edit
  `private-repos/` freely, like any other untracked repo, with no separate
  authorization required; the leak gate below still applies to its content.
- Before editing shared files or repos, claim the exact paths with Orchestrate;
  release when done. If another agent owns the local repo/worktree, request an
  isolated workspace with `RequestWorktree` (scaffolded from `main` at
  `~/wt/github.com/LiGoldragon/<repo>/<branch>`), claim its path, and conclude it
  with `ConcludeWorktree` merged or rejected when done.
- Skills and agent files under .agents/, .claude/, .codex/, and .pi/ are generated from LiGoldragon/skills; edit their source in that repository, not here.
- On primary, work on `main` directly. Use `jj commit -m '<message>'`,
  `jj bookmark set main -r @-`, and `jj git push --bookmark main`.
- Every description-taking `jj` command uses an inline message or equivalent
  headless flag. Never open an editor.
- Commit the whole working copy; dirty or unrelated existing files in primary are not a blocker and may be included.
- No raw `git` except the documented escape hatches in the `jj` skill.
- No `/nix/store` filesystem search.
- No `---` horizontal rules in markdown.
- DOTOS records are positional; use bare atoms for strings when canonical.
- Rust editing requires the Rust doctrine named by the generated role packet,
  prompt, or explicit context.
- Private information is closed by default and stays out of public reports,
  core Spirit records, commits, and chat.
- Repositories live at the ghq root `/git/<host>/<owner>/<repo>`. Clone a missing
  repository with `ghq get <url>` and never clone elsewhere.
- Domain standards live in `/git/github.com/LiGoldragon/standards`.
- The operating system is declarative. Its source is
  `/git/github.com/LiGoldragon/CriomOS` for the system and
  `/git/github.com/LiGoldragon/CriomOS-home` for the user environment.
