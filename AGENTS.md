# Primary Workspace — Agent Instructions

The compact contract. Every agent reads this on every session.

## Required reading, in order

1. **`ESSENCE.md`** — workspace essence (most universal psyche
   intent). Upstream of every rule below.
2. **`INTENT.md`** — workspace intent in prose form, synthesised
   from `intent/*.nota`. Read once on starting; consult when a
   topic comes up.
3. **`repos/lore/AGENTS.md`** — cross-workspace agent contract.
4. **`skills/skills.nota`** — typed skill index. Query it whenever
   a topic comes up; don't scan `skills/`.
5. **`orchestrate/AGENTS.md`** — how roles share this workspace.
6. **Your main role's `skills/<role>.md`** — required-reading list
   for the role you're in. Lanes share their main role's skill
   file.
7. **The repo's `AGENTS.md` + `skills.md`** when editing inside a
   repo under `repos/`.

## Where things live

| Path | What |
|---|---|
| `ESSENCE.md` | Workspace essence — most universal psyche intent. |
| `AGENTS.md` | This file. Compact every-keystroke contract. |
| `INTENT.md` | Workspace intent prose, synthesised from `intent/`. |
| `intent/` | Workspace log of psyche statements (NOTA). |
| `<repo>/INTENT.md` | Per-repo synthesis of psyche intent. |
| `orchestrate/AGENTS.md` | Role-coordination protocol. |
| `protocols/active-repositories.md` | Live repo map for architecture sweeps. |
| `skills/<name>.md` | Cross-cutting agent capabilities. |
| `skills/skills.nota` | Typed skill index (name, path, kind, tier, description). |
| `reports/<role>/` | Role-owned reports. Each role writes only into its own subdirectory. Exempt from claim flow. |
| `orchestrate/<lane>.lock` | Per-lane coordination state file. |
| `tools/orchestrate` | Claim/release helper. |
| `.beads/` | Shared short-tracked-item store. Transitional. |
| `repos/` | Symlink index to ghq checkouts under `/git/...`. |
| `RECENT-REPOSITORIES.md` | Broad recent checkout index. |
| `GOALS.md` | Standing high-level goals. |

## Skill discovery — query the index, don't scan

`skills/skills.nota` is the typed index. Each entry carries a
kind (`Role` / `Architecture` / `Craft` / `Programming` /
`Workflow` / `Meta`), a tier (`Apex` / `Keystroke` / `Topic` /
`Mechanism`), and a one-line description. When a topic comes up,
read the matching skill — don't scan `skills/` listing every file.

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
- **NOTA is the only argument language.** Every component binary
  (CLI and daemon) takes exactly one argument: a NOTA string, a path
  to a NOTA file, or a path to a signal-encoded (rkyv) file. No flags
  (`--verbose`, `--format`, `--config=path`) — ever. If a binary
  needs new configuration, the contract's NOTA schema gets a new
  field. Full rule: `skills/component-triad.md` §"The single argument
  rule".
- **NOTA records are positional, not labeled.** Type first, then
  fields in declared order — no keywords inside records. The
  `(key value)` shape from Lisp/Clojure/JSON is not NOTA. Before
  sketching any new record, open `skills/skills.nota` (the canonical
  example) or read `skills/nota-design.md`.
- **Psyche is the human; intent is primordial; ask when unclear.**
  **Psyche** means the human author. Psyche prompts are natural-
  language input to the agent; NOTA-formatted persona messages
  between agents are not psyche, agent-written files are not
  psyche, the intent log is psyche-*derived* but only as a record
  of psyche statements. Record explicit psyche intent in
  `intent/<topic>.nota` (`skills/intent-log.md`); reflect
  into per-repo `INTENT.md` (`skills/repo-intent.md`). **When
  intent on a question is unclear, absent, or contradicted, ask
  the psyche** (`skills/intent-clarification.md`) — don't infer.
  The intent layer has higher authority than every other workspace
  surface; supersession of psyche intent is always explicit
  (`skills/intent-maintenance.md`).
- **Extract intent to disk FIRST when a psyche prompt arrives.**
  Before editing any report, before writing code, before responding
  in chat — read the psyche's message, identify every intent
  statement (Decision / Principle / Correction / Clarification /
  Constraint), and write each to the appropriate
  `intent/<topic>.nota`. Everything else the prompt asked for
  derives from intent and is done *after* the capture. Reports,
  code, and chat are all downstream of intent. This is the
  absolute first task of any session-turn that contains psyche
  input.
- **No harness-dependent memory.** Workspace truth lives in files
  every agent can open. Don't use per-session memory at
  `~/.claude/projects/<workspace>/memory/` or any agent-private store.
- **No `/nix/store` filesystem search.** Use `nix eval`, `nix flake
  show`, `nix path-info`, or expose the value through a derivation.
- **Reach for the right tool, not raw git.** Version control is `jj`
  per `skills/jj.md`; raw `git` is reserved for two named escape-hatch
  cases listed there.
- **No `---` horizontal-rule lines in markdown.** Section structure
  comes from headings (`##`, `###`). `---` between every section is
  pure noise in agent context — costs tokens, conveys nothing
  headings don't already convey. Allowed inside code blocks (e.g.
  illustrating a markdown template); never as a document separator.
- **Opaque identifiers in chat carry an inline description.** A
  bead UID, content hash, jj change id, commit short-id, or any
  other locator the psyche can't decode in their head gets a short
  prose description on first mention: "bead `primary-hj63`
  (README rewrite for the PascalCase rule)" — never just
  "`primary-hj63`". Humans don't have a CLI in their head.
  Generalisation of `skills/reporting.md` §"Human-facing
  references are self-contained".

## Where to look for more

- Workspace intent in prose form (longer-form discipline, the
  two-deploy-stack discipline, worktree flow, BEADS, harness-memory
  rationale, intent layer, dynamic-role escalation): `INTENT.md`.
- Repo map for architecture sweeps: `protocols/active-repositories.md`.
- Standing goals: `GOALS.md`.
