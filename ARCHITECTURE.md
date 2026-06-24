# primary — architecture

*The coordination workspace. It owns discipline, protocols, skills,
reports, and the symlink index to active code repos. It holds no
shipping software; everything that ships lives in a repo under
`repos/`.*

> Workspace, not component. The shapes below describe how agents
> share a working surface — claim flow, lane ownership, document
> precedence — not a runtime topology.

## 0 · TL;DR

`primary` is the workspace at `~/primary/`. Work is organised by
**discipline** and **session lane**. Nine disciplines — `operator`,
`designer`, `system-operator`, `system-maintainer`, `poet`, `editor`,
`videographer`, `assistant`, `counselor` — each carry a permanent
identity (skill set, authority class, persona-mind memory, signing key)
through `skills/<discipline>.md`. A **lane** is one work session named
for its intent (`newLanesDesign`, `schemaWorkAudit`); it carries its
discipline as metadata, owns its own lock file and report directory, and
drains and retires at session close. The lane mechanism is canonical in
`skills/session-lanes.md`. Active code lives in
`/git/github.com/LiGoldragon/` checkouts that primary surfaces via the
`repos/` symlink index. Workspace intent lives in `ESSENCE.md` /
`INTENT.md` (synthesised from the Spirit store); cross-workspace agent
discipline lives in `repos/lore/AGENTS.md`.

The workspace is the apex of the agent-discipline graph: intent
(`ESSENCE.md` / `INTENT.md`, anchored to Spirit) → `lore/AGENTS.md`
(cross-workspace contract) → `orchestrate/AGENTS.md` (this workspace's
coordination) → `skills/<discipline>.md` (per-discipline required
reading) → per-repo `AGENTS.md` + `ARCHITECTURE.md` + `skills.md`.

## 1 · What lives here

```text
~/primary/
├── ESSENCE.md             workspace essence (universal intent surface)
├── INTENT.md              workspace intent synthesis
├── AGENTS.md              workspace-specific agent instructions
├── CLAUDE.md              Claude-flavored shim → AGENTS.md
├── ARCHITECTURE.md        this file
├── protocols/
│   ├── active-repositories.md   current active repo map
│   └── retired-lanes.md         append-only retired-lane index
├── skills/<name>.md       cross-cutting agent capabilities
├── skills/skills.nota     the typed skill index
├── reports/<lane>/        session-lane report directories (drain at close)
├── repos/                 symlink index to /git checkouts
├── orchestrate/           coordination protocol, daemon CLI, per-lane lock projections
├── RECENT-REPOSITORIES.md broad recent checkout index + cutoff
└── primary.code-workspace VS Code workspace marker
```

`.beads/` exists as a transitional short-tracked-item store
(see `AGENTS.md` §"BEADS is transitional"); destination is Persona's
native typed work graph.

## 2 · Disciplines and lanes

Nine disciplines. Each discipline's substantive work goes through its
`skills/<discipline>.md`; that file's "Required reading" section names
every workspace skill the discipline must read.

A **discipline** is a permanent identity — skills, authority class,
persona-mind memory, signing key. It names *what kind of agent this is*.
A **lane** is one work session named for its intent; it carries a
discipline as metadata (the last token of its orchestrate registry role
vector, e.g. `[NewLanesDesign Designer]`), owns `orchestrate/<lane>.lock`
and `reports/<lane>/`, and is created, drained, and retired per session.
The fixed role-named lanes of the prior model (`second-designer`,
`cluster-operator`, ordinal and qualifier shapes) are retired *as the
lane model*; specialized scope is now expressed as the session's intent
plus specialization tokens ahead of the discipline. Lanes register and
retire dynamically through the orchestrate daemon (`Register` /
`Observe Lanes` → `LanesObserved` / `Retire`). The full lane lifecycle —
register, smart-zone, fleet, drain, retire — is canonical in
`skills/session-lanes.md`.

`orchestrate/<lane>.lock` files coordinate claims on shared resources
(repos, files); the orchestrate daemon is their canonical writer and the
lock files are projections. `reports/<lane>/` directories are
lane-owned: each lane writes only its own directory, and report
directories are exempt from the file-claim flow. When a lane drains, its
report directory is deleted (git history and the session transcript are
the archive) and one row is appended to `protocols/retired-lanes.md`.

## 3 · Repos surface

`repos/` is a symlink directory. Each entry points at the canonical
checkout under `/git/github.com/LiGoldragon/<repo>/`.
`protocols/active-repositories.md` lists the currently active set;
`RECENT-REPOSITORIES.md` is the broader recent checkout index with its
own cutoff rule.

Components ship from those repos. primary itself ships no code; it is
the coordination surface that holds the rules under which the code is
built.

## 4 · Boundaries

This workspace owns:

- Workspace intent synthesis (`ESSENCE.md`, `INTENT.md`), anchored to
  the Spirit store.
- Discipline and lane discipline (`AGENTS.md`, `CLAUDE.md`).
- The coordination protocol (`orchestrate/AGENTS.md`) and the
  active-repo map (`protocols/active-repositories.md`).
- Cross-cutting workspace skills (`skills/<name>.md`).
- Session-lane report directories (`reports/<lane>/`) and the
  retired-lane index (`protocols/retired-lanes.md`).
- The `repos/` symlink index.
- Per-lane coordination state (`orchestrate/<lane>.lock`, daemon-owned).

It does not own:

- Shipping software (lives in repos under `/git/...`).
- Per-repo discipline (`AGENTS.md`, `ARCHITECTURE.md`, `skills.md`
  inside each repo).
- The canonical cross-workspace agent contract (lives in
  `repos/lore/AGENTS.md`).
- Persistent agent memory beyond workspace files (no harness-dependent
  state per `AGENTS.md` §"No harness-dependent memory").

## 5 · Constraints

- The Nix store is never a workspace search surface; agents never run
  generic filesystem search against `/nix/store`. Use Nix evaluation
  paths instead.
- Every identifier is a full English word (`Request` not `Req`,
  `Reply` not `Rep`, `Configuration` not `Cfg`). See `ESSENCE.md`
  §"Naming" and `skills/naming.md`.
- Reports are agent-consumable durable records written as fresh-context
  pickup points; chat is the user's working surface. A chat reply for
  the user is never a bare pointer to a report; user-attention items go
  inline. See `skills/reporting.md`.
- Permanent docs (`ARCHITECTURE.md`, `skills/<name>.md`, `AGENTS.md`)
  inline load-bearing claims; they don't cite reports. See
  `skills/architecture-editor.md`.
- BEADS tasks are never ownership locks. Any agent may create, update,
  comment on, or close BEADS tasks at any time.
- Memory belongs in workspace files every agent can read; no
  harness-private state stores.

## 6 · Invariants

- Intent precedes structure: the intent layer (Spirit, synthesised into
  `ESSENCE.md`) is upstream of every rule below it. A downstream rule
  that conflicts with intent loses.
- A discipline is a permanent identity; a lane is a throwaway session
  that carries one. Both are coordination structure, not security
  boundaries.
- The workspace is the apex of agent discipline; component
  architectures live in their own repos.

## See also

- `ESSENCE.md` — workspace essence.
- `AGENTS.md` — workspace-specific agent instructions.
- `orchestrate/AGENTS.md` — discipline-and-lane coordination.
- `skills/session-lanes.md` — the lane mechanism and lifecycle.
- `protocols/active-repositories.md` — current active repo set.
- `repos/lore/ARCHITECTURE.md` — the canonical agent-discipline repo
  this workspace points at.
- `skills/architecture-editor.md` — the rules this file follows.
