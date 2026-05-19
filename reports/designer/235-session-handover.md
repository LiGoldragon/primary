# 235 — Session handover

*Context handover for the next designer (or any agent) picking up
after this session compacts. Captures what landed, what's open, and
where the live edges are. The substance is on disk; this report is
the index.*

## 0 · The big arc of this session

A wholesale rebuild of the workspace's intent surface. The session
started with persona-orchestrate audit work and ended with the
workspace symmetric to per-repo layout (`AGENTS.md` + `ESSENCE.md`
+ `INTENT.md`). Along the way: a new persona component (spirit), a
new role (concept designer), an entire intent layer with five
skills, a NOTA grammar correction across the codec and the spec,
and a deep sweep of older reports.

Every load-bearing decision is recorded in `intent/<topic>.nota` —
that surface is canonical for "what did the psyche actually say."
This report points at the substance; the substance is the truth.

## 1 · The intent layer (new this session)

The workspace records psyche statements in `intent/*.nota` as raw
typed records. The shape:

| File | Role |
|---|---|
| `skills/intent-log.md` | How to record (lock-free shell append; 5-kind positional NOTA; certainty vocabulary; session-first discipline) |
| `skills/intent-maintenance.md` | Supersession protocol (psyche-only; rewrite-not-append; locks) |
| `skills/intent-clarification.md` | When to ask the psyche |
| `skills/repo-intent.md` | Per-repo `INTENT.md` shape |
| `skills/intent-manifestation.md` | Walk through intent; translate into guidance files; italics convention for verbatim quotes |

Current intent files:

```
intent/component-shape.nota   intent/orchestrate.nota
intent/jj.nota                intent/persona.nota
intent/markdown.nota          intent/reports.nota
intent/nota.nota              intent/workspace.nota
intent/arca.nota              intent/deploy.nota
```

(Last two are peer-agent additions from this session.)

Format: positional NOTA records, one of five kinds
(`Decision` / `Principle` / `Correction` / `Clarification` /
`Constraint`), with summary, quote, context, certainty
(`Maximum`/`Medium`/`Minimum`), bare date, bare time. No outer
list brackets — flat sequence of top-level records for lock-free
appendability via `cat >> intent/<topic>.nota <<'EOF' … EOF`.

## 2 · Guidance file layout (workspace = per-repo)

After this session's reshape:

| Workspace | Per-repo |
|---|---|
| `ESSENCE.md` (110 lines — gold of the gold) | `<repo>/ESSENCE.md` when warranted |
| `AGENTS.md` (150 lines — compact contract + file map + skill discovery + hard overrides) | `<repo>/AGENTS.md` per-repo carve-outs |
| `INTENT.md` (214 lines — workspace intent prose) | `<repo>/INTENT.md` per-repo intent |
| `intent/*.nota` (raw log) | (workspace-only for now; eventually per-repo too) |
| `skills/*.md` | `<repo>/skills.md` |

`ONBOARDING.md` retired this session (psyche directive). The
workspace has no special-case file at root; layout is consistent
with what every repo follows.

## 3 · Components in flight

Three persona components have substantive design work:

**`persona-spirit`** (new, /232). Interface between persona-mind
and the psyche. Apex of the cognitive authority chain — owns mind
via `owner-signal-persona-mind`. Spawned last in the engine boot
order. LLM-mediated NLP parses psyche prompts into typed intent
records. Bead **`primary-ojxq`** (persona-spirit triad
implementation; P1) — operator pickup. Six open questions
absorbed in /232; the remaining genuine open point is how mind
receives intent from spirit (verb set "develops as it develops").

**`persona-orchestrate`** (operator handoff in /233, amalgamating
the retired /228 + /229). State-vs-machinery split with mind;
ordinary slice already shipped via `signal-persona-orchestrate`
and `persona-orchestrate` repos. Open work: ship the full triad
(daemon + thin CLI + `owner-signal-persona-orchestrate` + chain
co-arrival contracts + lane registry); bead **`primary-hrhz`**.

**Concept designer** (new role, /234). Entry point for new
psyche concepts; compares against existing concepts; decides when
a concept earns its own dedicated design lane. Fleshing-out has
six open questions; my lean for first move is Q1 (lane mechanics)
before the role is operable. Psyche signalled ready to proceed.

## 4 · NOTA grammar — settled this session

The three-case PascalCase rule, settled by psyche correction over
six iterations:

1. `(VariantName fields…)` — data-carrying enum variant.
2. `(fields…)` without a leading PascalCase — struct (positional,
   no tag).
3. Bare `VariantName` with no preceding `(` — non-data-carrying
   unit variant.

Records vs sequences: `(…)` is a struct or variant; `[…]` is
`Vec<T>` (homogeneous). Heterogeneous positional structure is a
struct, written `(field1 field2 …)`.

Three nota beads filed; status as of session-end:

| Bead | Status |
|---|---|
| `primary-y4l4` (Option wraps `(Some inner)`) | **closed** (second-DA report 8) |
| `primary-x3xj` (Bool as `True`/`False`) | **closed** (second-DA report 8) |
| `primary-r8vi` (forbid bare PascalCase at string positions) | **closed** (second-DA report 8) |
| `primary-hj63` (README rewrites — three-case rule) | **partially closed** (README portion landed; codec PascalCase-head relaxation deferred to operator) |
| `primary-dzrn` (bare ISO-8601 Timestamp type) | open, P2 |
| `primary-uy7o` (codec rejects labeled-field records) | open, P2 |

Skill: `skills/nota-design.md` rewritten with the three-case rule
and a four-step "Before you sketch" checklist. The recurring
agent-NOTA mistakes (labeled fields, superfluous wrappers,
heterogeneous sequences, invented terminology like "head") all
traced to the same root: speculating about NOTA instead of reading
the spec. The skill now points readers at `nota/README.md` and
`skills/skills.nota` first.

## 5 · Workspace-level discipline changes

Three discipline shifts that future agents should know:

**Intent recording is the first task of any psyche-prompt turn.**
Before editing reports, before writing code, before chat — read
the psyche prompt, identify every intent statement, write each to
the appropriate `intent/<topic>.nota` via lock-free `cat >>`. Then
proceed with the work the prompt asked for. AGENTS.md hard
override.

**Roles loosened; beads are not role-labeled.** Any agent picks
up any bead based on topic affinity. The role-label filter on
beads is retired. Lanes still coordinate through lock files +
report subdirectories. `skills/autonomous-agent.md`,
`skills/role-lanes.md`, `orchestrate/AGENTS.md` all updated.

**Chat-output discipline reinforced.** No `---` separators in
markdown OR chat; no labeled-field tables ("Mechanism:",
"Example:") in chat; opaque IDs (bead UIDs, hashes, change IDs)
carry an inline description on every mention. All landed as
AGENTS.md hard overrides.

## 6 · Open beads (operator-shaped work)

Topic labels only; no role:* labels.

| Bead | Priority | Status | Subject |
|---|---|---|---|
| `primary-ojxq` | P1 | open | persona-spirit triad implementation |
| `primary-hrhz` | P1 | open | persona-orchestrate full-triad arc |
| `primary-hj63` | P2 | open (partial) | nota codec PascalCase-head relaxation |
| `primary-dzrn` | P2 | open | nota bare-ISO-8601 Timestamp type |
| `primary-uy7o` | P2 | open | nota-codec rejects labeled-field records |
| `primary-699g` | P2 | open | designer pickup for orchestrate component design |
| `primary-jboc` | P2 | open | RoleName closed-enum gap |
| `primary-68cb` | closed | n/a | orchestrate-cli Rust port (1730087a) |

## 7 · Held / undecided

Items that need psyche input before the next session can progress:

- **Q1 of /234** (concept designer lane mechanics — naming, claim
  file, reports subdir). My lean: settle this first since the role
  isn't operable without it. Psyche signalled ready.
- **Q2 of /234** (concept inventory — derive from intent topics,
  or maintain a `concepts/` directory).
- **/214 criome-architecture-record** — still in `reports/designer/`
  from before this session; might be retire-able if substance has
  migrated to `criome/ARCHITECTURE.md`. Spot-check before deletion.
- The **intent manifestation sweep** — psyche deferred to a future
  session (this one or another). `skills/intent-manifestation.md`
  carries the discipline; an agent reads `intent/*.nota` and
  manifests entries that haven't yet landed in their right
  guidance file.

## 8 · Live reports remaining

```
reports/designer/214-criome-architecture-record-2026-05-17.md
reports/designer/232-persona-spirit-new-component.md
reports/designer/233-persona-orchestrate-operator-handoff.md
reports/designer/234-concept-designer-role.md
reports/designer/235-session-handover.md   ← this report
```

Seven older reports retired during the sweep (commit
`be2440b9f832`): `/204` kameo, `/207` horizon boundary, `/208`
pan-horizon, `/209` + `/210` component-triad, `/211`
persona-terminal consolidation, `/224` workspace-redesign.
Substance migrated into skills and ARCHs; git history holds the
lineage.

## 9 · How to pick this up

For a fresh agent landing in the workspace:

1. Read `ESSENCE.md` first — workspace essence.
2. Read `INTENT.md` — workspace intent prose.
3. Read `AGENTS.md` — compact contract + file map + skill discovery + hard overrides.
4. Query `skills/skills.nota` for the topic you're working on.
5. If picking up a bead: scan `bd ready` and pick by topic affinity.
6. Capture psyche intent FIRST when a prompt arrives, before any other work — see AGENTS.md hard override.

For the specific work surfaces:

- **Persona work**: read `intent/persona.nota` and `/232`
  (spirit) + `/233` (orchestrate) for current direction. Bead
  `primary-ojxq` (spirit) is the next-arc operator pickup.
- **NOTA work**: read `intent/nota.nota` (six corrections in this
  session) + `skills/nota-design.md`. Three nota beads closed,
  three open; `primary-hj63` README portion landed but codec part
  is operator follow-up.
- **Workspace discipline**: read `INTENT.md` + `intent/workspace.nota`.
  The big shifts (intent-first, no role-label beads, chat
  discipline) are AGENTS.md hard overrides.

## 10 · Peer-agent activity this session

Multiple agents have been active in parallel:

- **second-designer-assistant** landed the NOTA three-case rule
  implementation across nota-codec + nota spec + INTENT (commit
  `cd7916e06a1f`).
- **operator** mapped persona-spirit system and intent gaps
  (commit `c56719505527`).
- **designer-assistant** updated repository-ledger contract and
  CLI hook status (multiple commits).
- **system-specialist** consolidated horizon service variant
  reports.
- **system-assistant** recorded intent context sweeps.

The intent files include records from these peer agents too —
intent recording is workspace-wide, not designer-only.

## See also

- `INTENT.md` — workspace intent in prose.
- `ESSENCE.md` — essential intent.
- `AGENTS.md` — compact every-keystroke contract.
- `intent/workspace.nota` — the densest intent file; every
  workspace-shape decision from this session.
- `intent/nota.nota` — the NOTA grammar journey (six corrections;
  the three-case rule).
- `intent/persona.nota` — persona-component intent (spirit,
  orchestrate).
- `skills/intent-manifestation.md` — how to walk through intent
  and translate into guidance files.
- `reports/designer/232-persona-spirit-new-component.md`,
  `233-persona-orchestrate-operator-handoff.md`,
  `234-concept-designer-role.md` — the live work surfaces.
