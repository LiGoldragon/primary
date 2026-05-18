# Primary Workspace — Agent Instructions

The compact contract. Every agent reads this on every session.

## Required reading, in order

1. **`ESSENCE.md`** — workspace intent. Upstream of every rule below.
2. **`repos/lore/AGENTS.md`** — cross-workspace agent contract.
3. **`skills/skills.nota`** — typed skill index. Query it whenever a
   topic comes up; don't scan `skills/`.
4. **`orchestrate/AGENTS.md`** — how roles share this workspace.
5. **Your main role's `skills/<role>.md`** — required-reading list for
   the role you're in. Lanes share their main role's skill file.
6. **The repo's `AGENTS.md` + `skills.md`** when editing inside a repo
   under `repos/`.

Bulkier discipline (rationale, longer explanations, topic-specific
rules) lives in `AGENTS-extended.md` — consult when the topic comes
up, not every session.

## Reports go in files; chat is for the user

**Substantive output — anything that explains, proposes, analyses,
audits, or synthesises — goes in `reports/<role>/<N>-<topic>.md`.** Not
in chat. Chat is the user's working surface; the user can't read a
giant chat response while running parallel agents.

The chat reply names the report path and carries the user-attention
items inline — open questions, blockers, recommendations awaiting
approval — each restated with enough substance that the user can
engage without opening the report. Locator-without-substance ("see
report N", "section 5.2") is a discipline violation.

Full discipline: `skills/reporting.md`.

## Skill importance — read the higher tiers first

Tier names match `skills/skills.nota`'s `tier` field. The index has
every skill; this table names the cross-cutting reads.

| Tier | What | Skill(s) |
|---|---|---|
| apex | Workspace intent | `ESSENCE.md` |
| apex | Universal architecture | `skills/component-triad.md` — daemon + thin CLI + `signal-*` + `owner-signal-*`. Read once; recognise the shape in every component ARCH. **If you read only one skill, read this one.** |
| keystroke | Universal craft | `abstractions` · `naming` · `beauty` · `push-not-pull` · `reporting` · `typed-records-over-flags` |
| topic | Consulted by topic | `contract-repo` · `micro-components` · `actor-systems` · `kameo` · `rust-discipline` · `language-design` · `architectural-truth-tests` |
| mechanism | Supports the lane | `role-lanes` · `feature-development` · `jj` · `skill-editor` · `architecture-editor` · `context-maintenance` · `autonomous-agent` |

For the full list with one-line descriptions, query `skills/skills.nota`.

## Roles

Four main roles, each carrying its own discipline. Lanes
(`<role>-assistant`, `second-<role>-assistant`) share their main
role's discipline, skill file, and beads label; only the lock file,
report subdirectory, and claim string differ. Lane mechanism:
`skills/role-lanes.md`.

- `operator` — implementation (default agent: Codex)
- `designer` — architecture, skills, reports (default agent: Claude)
- `system-specialist` — OS / platform / deploy (any agent)
- `poet` — writing as craft (any agent)

Each agent knows its lane before claiming or editing. Coordination:
`orchestrate/AGENTS.md`; helper: `tools/orchestrate`.

## Hard overrides

- **Spell every identifier as a full English word.** `Request` not
  `Req`. `Reply` not `Rep`. The narrow carve-outs and the justification
  live in `ESSENCE.md` §"Naming" and `skills/naming.md`.
- **No harness-dependent memory.** Workspace truth lives in files
  every agent can open. Don't use per-session memory at
  `~/.claude/projects/<workspace>/memory/` or any agent-private store.
- **No `/nix/store` filesystem search.** Use `nix eval`, `nix flake
  show`, `nix path-info`, or expose the value through a derivation.
- **Reach for the right tool, not raw git.** Version control is `jj`
  per `skills/jj.md`; raw `git` is reserved for two named escape-hatch
  cases listed there.

## Where to look for more

- Bulkier discipline (Nix-store rules, two-deploy-stack discipline,
  worktree flow, BEADS, harness-memory rationale, dynamic-role
  escalation): `AGENTS-extended.md`.
- Where each kind of file lives: `AGENTS-extended.md` §"Where things
  live".
- Repo map for architecture sweeps: `protocols/active-repositories.md`.
- Standing goals: `GOALS.md`.
