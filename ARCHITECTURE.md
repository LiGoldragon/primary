# primary — architecture

*The coordination workspace. It owns discipline, protocols, skills,
reports, and the symlink index to active code repos. It holds no
shipping software; everything that ships lives in a repo under
`repos/`.*

> Workspace, not component. The shapes below describe how agents
> share a working surface — claim flow, lane ownership, document
> precedence — not a runtime topology.

## 0 · TL;DR

`primary` is the workspace at `~/primary/`. Work is organised by generated
**role packets** and **session lane**. Role packets carry the doctrine bundle,
authority shape, and output contract required for normal role work. A **lane**
is one work session named for its intent (`newLanesDesign`,
`schemaWorkAudit`); it carries role/discipline metadata, owns its own lock file
and report directory, and drains and retires at session close. The lane
mechanism is canonical in the generated `session-lanes` skill packet. Active
code lives in
`/git/github.com/LiGoldragon/` checkouts that primary surfaces via the
`repos/` symlink index. Workspace vision and the durable intent framing
live in this file (§"Workspace vision and intent"); the raw psyche-statement
log lives in the deployed Spirit store. Cross-workspace agent discipline
lives in `repos/lore/AGENTS.md`.

The workspace is the apex of the agent-discipline graph: the Spirit store
(raw psyche statements) and this file's durable vision/intent framing,
then `lore/AGENTS.md`
(cross-workspace contract) → `orchestrate/AGENTS.md` (this workspace's
coordination), then the generated role packet (curated doctrine bundle),
then per-repo `AGENTS.md` + `ARCHITECTURE.md` + `skills.md`. Durable
direction, vision, and telos are recorded in `ARCHITECTURE.md` files (or
code stubs with explanatory comments) and the Spirit store, never in a
workspace `ESSENCE.md` or `INTENT.md`.

## 0.5 · Workspace vision and intent

This section is the durable home for the workspace's vision and the
intent-layer framing. It absorbs the content that previously lived in the
eliminated `ESSENCE.md` and workspace `INTENT.md`; the per-statement source
of truth is the deployed Spirit store, and the topic disciplines live in the
generated skill packets named below.

### What the workspace is building

Persona — a meta-AI system that organises models into a structure emulating
human intelligence, animated by persona-spirit. Components are dumb
mechanism; the thinking happens in agent LLMs that drive them through CLIs
and through Spirit — no component works without an LLM on the other end of
the wire. Components ship in raw form first (standalone CLI + daemon +
durable state) and are used individually before component-to-component
wiring lands.

The end is software eventually impossible to improve — in a bounded domain,
the right shape, chosen carefully, observed cleanly. In priority order,
earlier wins on conflict: **clarity** (the structure of the system is its
own documentation), **correctness** (every typed boundary names exactly what
flows through it), **introspection** (state is visible from outside; derived
values do not hide), and **beauty** (not pretty, but right — ugliness is
evidence the underlying problem is unsolved). What is *not* optimised for:
speed, feature volume, "minimum viable", "ship fast", backward compatibility
for systems being born, or time estimates — the right shape now is worth
more than a wrong shape sooner. The beauty gate is canonical in the generated
`beauty` skill packet; full-English naming is canonical in the generated
`naming` skill packet.

**Backward compatibility is not a constraint for systems being born.** Break
the system if it makes it more beautiful — not carelessness, but refusal to
compromise design to preserve a wrong shape. Compatibility binds only at
explicitly-declared boundaries: published APIs under semantic versioning,
wire contracts pinned by version, schemas externally consumed beyond our
control. Before such a boundary is declared, the system is being shaped, not
preserved. The version-surface mechanics are canonical in the generated
`versioning` and `feature-development` skill packets.

### The intent layer

Intent is primordial: an agent unsure what to do falls back on intent. The
psyche is the human; only the psyche is the source of new intent — agent
messages and agent-written files are not. When intent is unclear, absent, or
contradicted, ask rather than infer; inferring intent the psyche did not
state is forbidden. Intent is rare, and the default response to an utterance
is not to capture. The deployed Spirit store is the raw psyche-statement log
and the sole intent substrate; supersession is always explicit and only the
psyche can supersede. The capture/classification discipline is canonical in
the generated `intent-log`, `intent-clarification`, and `intent-manifestation`
skill packets. Durable direction and vision for a repository land in that
repo's `ARCHITECTURE.md` (or a code stub with an explanatory comment), never
in a per-repo or workspace `INTENT.md`.

### Push, not poll

Polling design is forbidden: producers push events; consumers subscribe.
When a mechanism appears to offer only polling, escalate deeper into the
stack and build or use a real event surface rather than tuning sleep
intervals or adding fallback polling. The application discipline — including
the patterns that look polling-shaped but are not — is canonical in the
generated `push-not-pull` skill packet.

### Today and eventually — different things, different names

When a concept has both a today's form and an eventual encompassing form,
the docs explicitly mark that boundary and give the two forms distinct names:
`sema` (today's typed storage kernel) / `sema-engine` versus the eventual
`Sema` (the universal medium for meaning); `criome` (today's BLS auth daemon)
versus the eventual `Criome` (the universal computing paradigm in Sema). ARCH
docs describe what is built today; eventual scope gets an explicit marker.
This is a scope discipline, not a quality one — "today's piece" is never a
license to cut corners. `protocols/active-repositories.md` carries the live
per-repo today-vs-eventual distinctions and cites this anchor.

## 1 · What lives here

```text
~/primary/
├── AGENTS.md              workspace-specific agent instructions
├── CLAUDE.md              Claude-flavored shim → AGENTS.md
├── ARCHITECTURE.md        this file
├── protocols/
│   ├── active-repositories.md   current active repo map
│   └── retired-lanes.md         append-only retired-lane index
├── .agents/skills/        generated workspace skill packets
├── .codex/agents/         generated Codex role packets
├── .pi/agents/            generated Pi role packets
├── .claude/agents/        generated Claude role packets
├── skills/                generated inventory files
├── reports/<lane>/        session-lane report directories (drain at close)
├── repos/                 symlink index to /git checkouts
├── orchestrate/           coordination protocol, daemon CLI, per-lane lock projections
├── RECENT-REPOSITORIES.md broad recent checkout index + cutoff
└── primary.code-workspace VS Code workspace marker
```

`.beads/` exists as a transitional short-tracked-item store
(see `AGENTS.md` §"BEADS is transitional"); destination is Persona's
native typed work graph.

## 2 · Roles and lanes

Generated role packets carry each role's substantive working doctrine. They
include curated critical modules and dependency-expanded modules, so routine
role work starts from the packet.

A **discipline** is a permanent identity — skills, authority class,
persona-mind memory, signing key. It names *what kind of agent this is*.
A **lane** is one work session named for its intent; it carries a
role/discipline as metadata (the last token of its orchestrate registry role
vector, e.g. `[NewLanesDesign Designer]`), owns `orchestrate/<lane>.lock` and
`reports/<lane>/`, and is created, drained, and retired per session.
The fixed role-named lanes of the prior model (`second-designer`,
`cluster-operator`, ordinal and qualifier shapes) are retired *as the
lane model*; specialized scope is now expressed as the session's intent
plus specialization tokens ahead of the discipline. Lanes register and
retire dynamically through the orchestrate daemon (`Register` /
`Observe Lanes` → `LanesObserved` / `Retire`). The full lane lifecycle —
register, smart-zone, fleet, drain, retire — is canonical in
the generated `session-lanes` skill packet.

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

- Workspace vision and the durable intent framing (this file,
  §"Workspace vision and intent"), anchored to the Spirit store.
- Discipline and lane discipline (`AGENTS.md`, `CLAUDE.md`).
- The coordination protocol (`orchestrate/AGENTS.md`) and the
  active-repo map (`protocols/active-repositories.md`).
- Generated workspace skill packets (`.agents/skills/<name>/SKILL.md` and
  harness-specific peers).
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
- Persistent agent memory beyond workspace files. Harness-private state is not
  a default memory substrate; Claude auto-memory is allowed only through an
  explicit opt-in launch path.

## 5 · Constraints

- The Nix store is never a workspace search surface; agents never run
  generic filesystem search against `/nix/store`. Use Nix evaluation
  paths instead.
- Every identifier is a full English word (`Request` not `Req`,
  `Reply` not `Rep`, `Configuration` not `Cfg`). See the generated
  `naming` skill packet.
- Reports are agent-consumable durable records written as fresh-context
  pickup points; chat is the user's working surface. A chat reply for
  the user is never a bare pointer to a report; user-attention items go
  inline. See the generated `reporting` skill packet.
- Permanent docs (`ARCHITECTURE.md`, `skills.md`, `AGENTS.md`) inline
  load-bearing claims; they don't cite reports. See the generated
  `architecture-editor` skill packet.
- BEADS tasks are never ownership locks. Any agent may create, update,
  comment on, or close BEADS tasks at any time.
- Memory belongs in workspace files every agent can read; harness-private state
  stores, including Claude auto-memory, are gated opt-in paths rather than
  defaults.

## 6 · Invariants

- Intent precedes structure: the intent layer (the Spirit store, with its
  durable framing in §"Workspace vision and intent") is upstream of every
  rule below it. A downstream rule that conflicts with intent loses.
- A discipline is a permanent identity; a lane is a throwaway session
  that carries one. Both are coordination structure, not security
  boundaries.
- The workspace is the apex of agent discipline; component
  architectures live in their own repos.

## See also

- §"Workspace vision and intent" (this file) — the durable home for
  workspace vision and the intent-layer framing.
- `AGENTS.md` — workspace-specific agent instructions.
- `orchestrate/AGENTS.md` — discipline-and-lane coordination.
- `session-lanes` skill packet — the lane mechanism and lifecycle.
- `protocols/active-repositories.md` — current active repo set.
- `repos/lore/AGENTS.md` — the canonical agent-discipline repo
  this workspace points at.
- `architecture-editor` skill packet — the rules this file follows.
