## Hard Boundaries

- `repos/` and `private-repos/` stay untracked. Agents may inspect and edit
  `private-repos/` freely, like any other untracked repo, with no separate
  authorization required; the leak gate below still applies to its content.
- Before editing shared files or repos, claim the exact paths with Orchestrate;
  release when done.
- Authored skill sources are the `*.md` files under `Psyche skills`, `Mind
  skills`, and `Field skills`. `.agents/`, `.claude/`, `.codex/`, `.pi/`, and
  `.opencode/` trees are generated read-only evidence; never edit them
  directly. Regenerate them through Curriculum Nexus after changing the
  authored sources or manifests.
- On Primary, leave your owned edits for the sole standing committer. Your
  turn-end hook delivers your actual identity and transcript when Primary is
  dirty. Never stage, commit, push, take PrimaryPublish or rewrite Primary
  yourself; preserve foreign changes and report blockers. In every other
  repository, commit and push your own changes as usual.
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

Load the `knowledge-psyche` skill. If your work touches a topic the psyche may
have spoken on, search the vision- and intent- skills, `vision-raw/`, and `flows/*/vision/` before assuming.
