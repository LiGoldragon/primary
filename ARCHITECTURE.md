# primary — architecture

*The coordination workspace. It owns role discipline, protocols,
skills, reports, and the symlink index to active code repos. It
holds no shipping software; everything that ships lives in a repo
under `repos/`.*

> Workspace, not component. The shapes below describe how agents
> share a working surface — claim flow, lane ownership, document
> precedence — not a runtime topology.

---

## 0 · TL;DR

`primary` is the workspace at `~/primary/`. Eight coordination roles
(four main + four assistants) share it, claiming work through
per-role lock files and writing reports into role-owned report
directories. Active code lives in `/git/github.com/LiGoldragon/`
checkouts that primary surfaces via the `repos/` symlink index.
Workspace intent lives in `ESSENCE.md`; cross-workspace agent
discipline lives in `repos/lore/AGENTS.md`; per-role discipline
lives in `skills/<role>.md`.

The workspace is the apex of the agent-discipline graph:
`ESSENCE.md` (intent) → `lore/AGENTS.md` (cross-workspace contract)
→ `protocols/orchestration.md` (this workspace's coordination)
→ `skills/<role>.md` (per-role required reading) → per-repo
`AGENTS.md` + `ARCHITECTURE.md` + `skills.md` (per-repo).

---

## 1 · What lives here

```text
~/primary/
├── ESSENCE.md             intent (upstream of every other doc)
├── AGENTS.md              workspace-specific agent instructions
├── CLAUDE.md              Claude-flavored shim → AGENTS.md
├── ARCHITECTURE.md        this file
├── GOALS.md               standing high-level goals
├── protocols/
│   ├── orchestration.md   role-coordination protocol
│   └── active-repositories.md   current active repo map
├── skills/<name>.md       cross-cutting agent capabilities
├── reports/<role>/        role-owned report directories
├── repos/                 symlink index to /git checkouts
├── tools/orchestrate      claim/release helper
├── <role>.lock            per-role coordination state
├── RECENT-REPOSITORIES.md broad recent checkout index + cutoff
└── primary.code-workspace VS Code workspace marker
```

`.beads/` exists as a transitional short-tracked-item store
(see `AGENTS.md` §"BEADS is transitional"); destination is Persona's
native typed work graph.

---

## 2 · Roles and lanes

Eight coordination roles. Each role's substantive work goes through
its `skills/<role>.md`; that file's "Required reading" section names
every workspace skill the role must read.

| Role | Default agent | Skill | Report lane |
|---|---|---|---|
| `operator` | Codex | `skills/operator.md` | `reports/operator/` |
| `operator-assistant` | any | `skills/operator-assistant.md` | `reports/operator-assistant/` |
| `designer` | Claude | `skills/designer.md` | `reports/designer/` |
| `designer-assistant` | Codex | `skills/designer-assistant.md` | `reports/designer-assistant/` |
| `system-specialist` | any | `skills/system-specialist.md` | `reports/system-specialist/` |
| `system-assistant` | any | `skills/system-assistant.md` | `reports/system-assistant/` |
| `poet` | any | `skills/poet.md` | `reports/poet/` |
| `poet-assistant` | any | `skills/poet-assistant.md` | `reports/poet-assistant/` |

`<role>.lock` files coordinate claims on shared resources (repos,
files). `tools/orchestrate` is the claim/release helper.
`reports/<role>/` directories are lane-owned: each role writes only
its own subdirectory; report lanes are exempt from the file-claim
flow.

---

## 3 · Repos surface

`repos/` is a symlink directory. Each entry points at the canonical
checkout under `/git/github.com/LiGoldragon/<repo>/`.
`protocols/active-repositories.md` lists the currently active set;
`RECENT-REPOSITORIES.md` is the broader recent checkout index with
its own cutoff rule.

Components ship from those repos. primary itself ships no code; it
is the coordination surface that holds the rules under which the
code is built.

---

## 4 · Boundaries

This workspace owns:

- Workspace intent (`ESSENCE.md`) and standing goals (`GOALS.md`).
- Role discipline (`AGENTS.md`, `CLAUDE.md`).
- The coordination protocol (`protocols/orchestration.md`) and the
  active-repo map (`protocols/active-repositories.md`).
- Cross-cutting workspace skills (`skills/<name>.md`).
- Role-owned report directories (`reports/<role>/`).
- The `repos/` symlink index.
- Per-role coordination state (`<role>.lock`).

It does not own:

- Shipping software (lives in repos under `/git/...`).
- Per-repo discipline (`AGENTS.md`, `ARCHITECTURE.md`, `skills.md`
  inside each repo).
- The canonical cross-workspace agent contract (lives in
  `repos/lore/AGENTS.md`).
- Persistent agent memory (no harness-dependent state per
  `AGENTS.md` §"No harness-dependent memory").

---

## 5 · Constraints

- The Nix store is never a workspace search surface; agents never
  run generic filesystem search against `/nix/store`. Use Nix
  evaluation paths instead.
- Every identifier is a full English word (`Request` not `Req`,
  `Reply` not `Rep`, `Configuration` not `Cfg`). See `ESSENCE.md`
  §"Naming — full English words" and `skills/naming.md`.
- Reports are agent-consumable durable records; chat is the user's
  working surface. A chat reply for the user is never a bare
  pointer to a report; user-attention items go inline. See
  `skills/reporting.md`.
- Permanent docs (`ARCHITECTURE.md`, `skills/<name>.md`,
  `AGENTS.md`) inline load-bearing claims; they don't cite reports.
  See `skills/architecture-editor.md`.
- BEADS tasks are never ownership locks. Any agent may create,
  update, comment on, or close BEADS tasks at any time.
- Memory belongs in workspace files every agent can read; no
  harness-private state stores.

---

## 6 · Invariants

- Intent precedes structure: `ESSENCE.md` is upstream of every
  rule below it. A downstream rule that conflicts with intent
  loses.
- Roles are coordination labels, not security boundaries.
- The workspace is the apex of agent discipline; component
  architectures live in their own repos.

---

## See also

- `ESSENCE.md` — workspace intent.
- `AGENTS.md` — workspace-specific agent instructions.
- `protocols/orchestration.md` — role coordination.
- `protocols/active-repositories.md` — current active repo set.
- `repos/lore/ARCHITECTURE.md` — the canonical agent-discipline
  repo this workspace points at.
- `skills/architecture-editor.md` — the rules this file follows.
