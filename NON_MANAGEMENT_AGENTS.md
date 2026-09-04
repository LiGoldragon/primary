## Hard Boundaries

- `repos/` and `private-repos/` stay untracked. Agents may inspect and edit
  `private-repos/` freely, like any other untracked repo, with no separate
  authorization required; the leak gate below still applies to its content.
- Before editing shared files or repos, claim the exact paths with Orchestrate;
  release when done. If another agent owns the local repo/worktree, request an
  isolated workspace with `RequestWorktree` (scaffolded from `main` at
  `~/wt/github.com/LiGoldragon/<repo>/<branch>`), claim its path, and conclude it
  with `ConcludeWorktree` merged or rejected when done.
- Authored skill sources are only the `*.md` files under `Curriculum skills`.
  Identity and deployment selection are only `manifests/*.dotos`.
  `.agents/`, `.claude/`, `.codex/`, and `.pi/` trees are generated read-only
  evidence; never edit them directly. Regenerate from the consumer workspace
  after changing the authored sources or manifests.
- On primary, work on `main` directly. Use `jj commit -m '<message>`,
  `jj bookmark set main -r @-`, and `jj git push --bookmark main`.
- Every description-taking `jj` command uses an inline message or equivalent
  headless flag. Never open an editor.
- Leave no uncommitted changes behind: what you changed, you commit and push before finishing. When a tree you are about to write in already holds changes, commit those first, as their own commit, described as found in the tree.
- No raw `git` except the documented escape hatches in the `jj` skill.
- No `/nix/store` filesystem search.
- No `---` horizontal rules in markdown.
- DOTOS records are positional; use bare atoms for strings when canonical.
- Rust editing requires the Rust doctrine named by the generated role packet,
  prompt, or explicit context.
- Repositories live under `Repository root` as `<host>/<owner>/<repo>`. Clone a missing
  repository with `ghq get <url>` and never clone elsewhere.
- Domain standards live in `Standards`.
- The operating system is declarative. Its source is `The system` for the system and `The user environment` for the user environment.

A prompt that is or contains only a bead ID (like primary-751) is a
dispatch envelope. Run bd show <id>, load every skill the bead names
as primordial (valid for the whole session), and follow it.

## Psyche

Load the `psyche` skill. If your work touches a topic the psyche may
have spoken on, search `Vision/`, `vision-raw/`, and `flows/*/vision/` before assuming.

