# Belief rename inventory, 2026-10-29

Order: psyche-context, mind-context, field-context become psyche-belief, mind-belief, field-belief.

## Scope searched
rg -l over /home/li/primary, /git/github.com/LiGoldragon, ~/.claude, ~/.codex; find ~ -maxdepth 4 -lname '*-context*' (none); symlinks under primary/.claude, primary/.codex, ~/.claude/skills (none to the repos; ~/.codex/agents link to the home-manager store only).

## Live consumers (updated)
- Curriculum: src/registry.rs (two repository_name lists), tests/layout_v2.rs, tests/nexus_roundtrip.rs, README.md, ARCHITECTURE.md.
- flow: capsule/flow-capsule.clj (context-roots), crates/flow-nexus/src/main.rs (test fixtures), UPGRADES.md.
- CriomOS-home: flake.nix (primary input overrides, primary pin), flake.lock, modules/home/profiles/min/context-skills.nix, packages/curriculum-resolver-deployment (state paths and origins), packages/context-skills, packages/context-deploy, checks/curriculum-resolver-deployment.
- primary: flake.nix and flake.lock inputs, SKILL_VARIABLES.md (paths, labels now "Psyche belief:" and so on), tools/book-check.mjs (contextRepository regex) and its two test files.
- the three repositories' own docs (README, vision/psyche.md, knowledge/*); evidence/ left as a point-in-time record.
- Curriculum state checkouts ~/.local/state/curriculum-context/<name>.
- Remotes: the three source checkouts; /git/.../mind-context-module-size; worktrees psyche-context-554e1a, -73b5d8, -intentcfg, -land.

## Left as records (not edited)
flows/*/books, publications, reports, logs, archive; primary 2026-09-18 launch prompt; primary-next and primary mirrors under /git; /git/.../books; ~/.claude history. These describe past states.
The parent directory name curriculum-context and the CURRICULUM_*_CONTEXT_* variable names are not repository names and stay.

## Not mine
Worktree directories named *-context-* under /home/li/worktrees belong to other flows and keep their directory names.
