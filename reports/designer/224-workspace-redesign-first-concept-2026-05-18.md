# 224 — Workspace redesign: first concept (2026-05-18)

*Role redesign + report-repo question + repository-creation skill +
skills-subdivision question. First concept; user pushback now
absorbed in `reports/designer/225-workspace-redesign-direction-after-pushback-2026-05-18.md`.*

**Status**: §2-§7 pattern catalog, research synthesis, repo
conventions, and skills-taxonomy reasoning are still load-bearing.
§4 (lane set) and §10 (open questions) are partially superseded by
/225. Read /225 first for the current direction.

---

## 0 · TL;DR

The user surfaced four entangled questions: rename roles for less
cognitive load; move reports to separate repos to reduce commit churn;
codify repo-naming as a skill; consider subdividing `skills/`. I
researched each with parallel agents (multi-agent role-organization
literature, primary's existing repo conventions, skill-taxonomy
patterns) and the answer is:

1. **Lane key becomes `(subsystem, discipline)`** — two-token,
   hyphenated, full English words. Five subsystems (`primary`,
   `persona`, `system`, `criome`, `poet`) × three disciplines
   (`designer`, `operator`, `deployer`) gives a matrix; only the cells
   with real work get lanes. The "assistant" / "second-" pattern goes
   away. Concurrent capacity comes from **anonymous sub-agents spawned
   from a named lane**, not from sibling lanes. "Concept designer" is a
   *mode*, not a role.

2. **Reports stay in `primary`**, not separate repos. The friction
   that repo-per-lane introduces (cross-repo references, ghq cloning,
   search overhead, indirection to find a path) costs more than the
   commit churn it solves. The churn has cheaper fixes — branch-per-lane
   (jj-native) or per-subsystem rather than per-lane repos if we ever
   decide to split.

3. **Land `skills/repository-creation.md` as a new skill** (alongside
   the existing `skills/repository-management.md` which covers ghq/gh
   mechanics). The discipline already exists in practice — the prefix
   conventions, the canonical 14-file shape, the flake-when-buildable
   rule, the skeleton-vs-implementation distinction — and the skill
   just makes it explicit.

4. **Don't subdivide `skills/`** more than minimally. Anthropic's own
   skills directory is flat. The "selection-accuracy" research shows
   subdivision is for >100 skills; primary has 37. The one carve worth
   doing now: `skills/roles/` (5 files, mechanical). Resist further
   subdivision until the count or topical heterogeneity earns it.

5. **The generic-workspace-for-others ambition is separable** — defer
   it. The role rename and repo discipline land independently. Generic
   packaging (à la Claude Code plugins) is a clean follow-up arc once
   the names stabilize.

Action plan in §9. Open questions for user decision in §10.

---

## 1 · Method

Three parallel `general-purpose` agents researched in parallel:

- **Agent 1**: multi-agent role-organization patterns — AutoGen,
  CrewAI, LangGraph, MetaGPT, ChatDev, Anthropic Research, OpenAI
  Swarm, plus academic literature (Kim et al. 2025 *Towards a Science
  of Scaling Agent Systems*, the 2025 LLM-MAS survey, *Agent as
  Bounded Context*, Manus context engineering).
- **Agent 2**: primary's existing repo-naming conventions — scanned
  `protocols/active-repositories.md`, `repos/` symlinks, ~30 repos
  under `/git/github.com/LiGoldragon/`. Extracted prefix/suffix
  catalog, canonical shape, flake usage rule.
- **Agent 3**: skill taxonomy patterns — Anthropic skills repo, Claude
  Code skills runtime, Agent Skills open spec, SFIA, PMBOK, LangChain,
  Semantic Kernel, plus competency-framework literature.

Agent findings synthesized below. Citations come through from the
agents and appear inline where they shape recommendations.

---

## 2 · Pushback to the user's framing (carried forward from chat)

Five concrete tradeoffs the user should weigh:

**1. The pain is role *ambiguity*, not role *count*.** Today's friction
isn't that there are 11 lanes; it's that `designer / designer-assistant
/ second-designer-assistant` have indistinguishable names. The
literature backs this directly: Kim et al. 2025 show role duplication
without ownership boundaries is exactly where multi-agent error
amplification (up to 17.2× single-agent baseline) lives. The fix is
*meaningful names* — `(subsystem, discipline)` makes scope explicit —
not *fewer names*.

**2. "Concept designer" is a mode, not a role.** The multi-agent
literature is clear: phase-as-role works when phases produce different
artifact types with different toolsets (MetaGPT's PM/Architect/Engineer
pipeline); it fails when "concept" and "detailed" both write into the
same `reports/` tree and edit the same `skills/`/`ARCHITECTURE.md`.
For primary, concept and detailed designer share substrate — they're
modes of one designer. Add a `skills/design-modes.md` if useful, not a
new lane.

**3. Repo-per-lane has costs the user didn't surface.** Cross-references
(today `reports/operator/151-...md`) become cross-repo links. `ghq
clone` of the workspace explodes. Search-across-reports needs new
tooling. The "passable object" pattern in `skills/reporting.md`
(forward a path to another lane) becomes a cross-repo reference.
Cheaper alternative: jj branch-per-lane reaches the same churn-reduction
goal with no new repos. Per-subsystem repos (one for `persona`, one for
`system`, one for `criome`, one for `poet`) is a middle ground if we
must split.

**4. Generic-workspace ambition is separable.** Making primary
cloneable-by-others requires deciding what's "core" vs "user
extension" — a real design question (Claude Code's scope-tier model,
LangChain's core/community split, Anthropic plugin marketplace pattern
are the prior art). Don't bundle this with the role-rename; ship the
rename first, then take a clean run at packaging.

**5. Poet specialization (Vedic / Greek / editor) is premature.** Per
the multi-agent volume rule (CrewAI: split when one agent is doing
many things; AgentPatterns: only add a role when there's measurable
value and an explicit ownership boundary), specialize when you have
*concurrent* Vedic and Greek work. Today, one `poet` plus an optional
`poet-editor` review role covers the actual cadence. Style selection
is a prompt-time concern, not a lane concern.

---

## 3 · Research synthesis

### 3.1 Multi-agent role organization

Across the surveyed projects, five distinct patterns emerge:

| Pattern | Used by | Strength | Failure mode |
|---|---|---|---|
| Role-as-job-title | MetaGPT, ChatDev, CrewAI | Maps to a known workflow; new contributors orient via the metaphor | Names create wrong mental model when work doesn't map to a real org chart |
| Functional-archetype (Planner/Engineer/Critic) | AutoGen, post-MAS literature | Repeatable cognitive pipeline; clear error topology | Same archetype duplicates (two "Critics") becomes ambiguous |
| Orchestrator + anonymous workers | Anthropic Research, OpenAI Swarm | Bursty parallel work; no stable-identity overhead | Long-running collaboration needs accountability that anonymous workers can't provide |
| **Bounded-context-as-agent** (subsystem-prefixed) | Manus, "Agent as Bounded Context" | One subsystem per agent — stable vocabulary, invariants, ownership | Requires real subsystem boundaries; doesn't help if codebase is monolithic |
| LangGraph supervisor/swarm | LangGraph | Typed state machine; durable graph topology | Coordination overhead grows past ~4 roles; truly open work degrades to "network mode" with error amplification |

**Key empirical findings:**

- **17.2× error amplification** in unstructured multi-agent networks
  vs single-agent baseline (Kim et al. 2025, arXiv:2512.08296).
  Centralized orchestration contains it to ~4.4×.
- **45% rule**: adding agents helps most when single-agent accuracy is
  below 45%; above that, additional agents add noise.
- **Performance plateaus around 4 concurrent agents** (Kim et al. 2025).
- **Selection accuracy phase transition at ~50-100 skills**: below it,
  agent selection of the right skill is >95% accurate; at 200 skills
  it collapses to ~20% (arXiv:2601.04748).
- **Anthropic's own guidance**: start with one agent; multi-agent costs
  3-10× more tokens; reasons to split are context-pollution,
  parallelization, or genuinely different tool/behavior bundles —
  **not** "I want a writer agent and a tester agent" (warned against
  as problem-centric decomposition that fails).

**Naming conventions in the wild** (from VoltAgent's 100+ Claude
Code subagent catalog): ~80% role/job-title (`frontend-developer`,
`python-pro`, `cloud-architect`, `kubernetes-specialist`); ~20% verb
(`code-reviewer`, `test-automator`); hyphenated, full words.

### 3.2 Primary's existing repo conventions

Prefix catalog (already in use, validated by the agent):

- `signal-` → wire contract crate (typed records, no daemon)
- `signal-persona-` → Persona-internal wire contract
- `owner-signal-persona-` → owner-socket-only mutation contract
- `persona-` → Persona stack daemon/component
- `nota-`, `nexus-`, `mentci-`, `sema-`, `kameo-` → family-prefix
- `CriomOS-` (PascalCase) → CriomOS Nix-module siblings
- `criomos-` (lowercase) → OS-adjacent config/archive
- `lojix-` (lojix-cli, lojix-archive) → legacy stack siblings
- *No prefix* → standalone unique component or family namesake

Suffix catalog: `-cli`, `-lib`, `-derive`, `-codec`, `-config`,
`-archive`, `-engine`, `-tools`, `-egui`, `-test`/`-testing`, `-rs`.

Canonical repo shape (14 top-level files): `AGENTS.md`, `ARCHITECTURE.md`,
`CLAUDE.md`, `README.md`, `Cargo.toml`, `Cargo.lock`, `flake.nix`,
`flake.lock`, `rust-toolchain.toml`, `skills.md`, `LICENSE.md`, `src/`,
`tests/`. Optional: `examples/`, `scripts/`, `macros/`, `docs/`.

Flake rule: flake.nix exists when the repo *builds* something
(`criome`, `persona-router`); absent when the repo is pure data
(`lore`, `goldragon`, `criomos-horizon-config`) or skeleton-as-design
(`lojix` on `main`, `signal-lojix` on `main`).

For reports-as-separate-repos: existing workspace convention is
`<noun>-<role>` (signal-derive, mentci-lib, CriomOS-pkgs); applying it
gives `<lane>-reports` (e.g. `designer-reports`), not `reports-<lane>`.

### 3.3 Skill taxonomy patterns

Six patterns surveyed; key finding: **dominant on-disk shape is flat
with kebab-case names**, with categorization expressed as prose in the
README, not as directories.

- **Anthropic's `anthropics/skills`**: 17 directories under one flat
  `skills/`. README describes "Creative & Design", "Development &
  Technical", etc., but the disk is flat.
- **Claude Code runtime**: scope tiers (Enterprise > Personal > Project
  > Plugin) determine *where* a skill lives, not category. Within each
  tier the directory is flat.
- **LangChain `tools/`**: flat with hundreds of integrations.
- **Agent Skills open spec**: mandates lowercase `a-z` and `-`, max
  64 chars, no leading/trailing hyphen.
- **Semantic Kernel** (outlier): `PascalCase`, two-level (Plugin/Function).
- **SFIA**: not files but a label scheme — six categories × 17
  subcategories × 7 levels, with each skill carrying a 4-letter code
  (`PROG`, `DAAN`).

**Extension/plugin patterns** (relevant to the user's "generic
workspace" ambition): the dominant model is **namespacing + precedence**,
not core/extension folder split. Claude Code's four tiers handle "ships
with workspace" vs "user's local override". Anthropic plugins
(`.claude-plugin/`) bundle skills + hooks + subagents into installable
units; the host workspace consumes via the plugin marketplace. LangChain
splits into separate Python distributions (`langchain-core`,
`langchain-community`, `langchain-<provider>`).

---

## 4 · Proposed role taxonomy

### 4.1 The lane key

**`(subsystem, discipline)` — two tokens, hyphenated, full English words.**

This is the **bounded-context-as-agent** pattern (Manus, the
literature consensus for long-running collaborative workspaces with
real subsystem boundaries). Each subsystem becomes one agent's home.
Discipline names the kind of work inside that home. Two tokens carry
the meaning; no ordinal suffix is needed.

### 4.2 Subsystems (5)

| Subsystem | Scope |
|---|---|
| `primary` | Workspace-wide: meta-architecture, `ESSENCE.md`, `AGENTS.md`, `skills/`, role definitions, cross-cutting protocols, concept work that doesn't yet have a subsystem home |
| `persona` | The Persona stack — `persona-mind`, `persona-router`, `persona-message`, `persona-harness`, `persona-terminal`, `persona-introspect`, `persona-system`, `persona-orchestrate`, all `signal-persona-*` and `owner-signal-persona-*` contracts |
| `system` | CriomOS + hardware/cluster + the deploy stack: `CriomOS`, `CriomOS-home`, `CriomOS-lib`, `lojix`, `signal-lojix`, `arca`, `signal-arca`, `goldragon`, `horizon-rs`, `criomos-horizon-config`, networking/secrets/Nix-daemon work |
| `criome` | The criome daemon + signing/authorization: `criome`, `signal-criome`, `owner-signal-criome`, `clavifaber`, related authorization/identity work |
| `poet` | Prose craft: `TheBookOfSol`, `substack-cli`, essays, citations |

These five names match how the user already groups work in
conversation. The boundaries are real (different vocabularies,
different invariants, different test surfaces).

### 4.3 Disciplines (3)

| Discipline | What it owns |
|---|---|
| `designer` | Architecture, design reports, skills, language design, contract shape, repo creation |
| `operator` | Implementation: Rust code, tests, `Cargo.toml` work, `ARCHITECTURE.md` updates reflecting what shipped |
| `deployer` | Production deployment: Nix builds + nixos-rebuild + cluster cutover + on-call + production state observability + cross-host runtime invariants |

The `system-specialist` lane today implicitly does all three. Splitting
gives clearer accountability: designer plans, operator implements,
deployer ships and operates.

**Why three disciplines, not more.** Four was tempting (add `editor`
for poet, add `coordinator` for cross-discipline glue), but each
additional discipline adds 5 potential lanes (one per subsystem). The
literature is clear: stay near the 4-agent cap (Kim et al. 2025).
Three disciplines × 5 subsystems = 15 *potential* lanes — but only
the cells with real work become real lanes.

### 4.4 The actual lane set (concrete enumeration)

Not every (subsystem, discipline) cell is needed. The lanes that
actually exist:

| Subsystem | designer | operator | deployer |
|---|:-:|:-:|:-:|
| `primary` | ✓ | ✗ | ✗ |
| `persona` | ✓ | ✓ | (future) |
| `system` | ✓ | ✓ | ✓ |
| `criome` | ✓ | ✓ | ✓ |
| `poet` | (uses `poet` lane) | | |

Plus a single `poet` lane (combined design + operation) and an optional
`poet-editor` review lane if review cadence justifies it. Subsystem
`poet` is the carve-out where the discipline split doesn't fit (one
person writes prose, doesn't deploy it).

**Concrete lane list (10 lanes):**

1. `primary-designer` — workspace-wide design (where I am right now)
2. `persona-designer` — Persona stack design
3. `persona-operator` — Persona stack implementation
4. `system-designer` — CriomOS / deploy stack design
5. `system-operator` — CriomOS / deploy stack implementation
6. `system-deployer` — production cluster deploys, cutover, on-call
7. `criome-designer` — criome architecture / signing model
8. `criome-operator` — criome daemon implementation
9. `criome-deployer` — criome key custody, cluster-side criome deploy
10. `poet` — prose craft

Optional: `persona-deployer` (when Persona has production deployment),
`poet-editor` (when review cadence justifies).

**That's 10 lanes** — one fewer than today's 11 (operator, OA, sec-OA,
designer, DA, sec-DA, system-specialist, system-assistant,
sec-system-assistant, poet, poet-assistant), with every name carrying
meaning.

### 4.5 Capacity beyond one agent per lane

When a lane needs concurrent work (today's "I need extra designer
capacity" use case), use the **named-supervisor-plus-anonymous-workers
pattern** from Anthropic Research and OpenAI Swarm:

- The lane has one named agent. That agent has a single claim on
  `orchestrate/<lane>.lock`.
- For concurrent work, the named agent **spawns sub-tasks via the
  Agent tool** (general-purpose subagents). Each sub-task is scoped to
  the lane's authority and writes findings back to the named agent for
  synthesis and commit.
- Sub-tasks don't claim the lane. Their accountability is to the
  named agent.

This is what I've been doing all session (dispatching `general-purpose`
agents for parallel research). The pattern works; just name it
explicitly.

The lock-file discipline gets simpler: one claim per lane at a time.
Conflict resolution: when two agents want the same lane, the one
without a claim waits or works on a different subsystem.

### 4.6 Modes (concept / detailed / review)

Modes are *prompt-time* selections, not separate lanes. A `persona-designer`
can be in "concept mode" (exploring a new direction; outputs may not
yet have a home in `ARCHITECTURE.md`) or "detailed mode" (refining a
landed concept; outputs flow into ARCH or skill). Capture as a small
`skills/design-modes.md` (or section of `skills/designer.md`) naming
the three modes with one-paragraph descriptions.

This is what the user called "concept designer" — but it lives as a
mode on the appropriate subsystem's designer lane, not as a separate
role.

### 4.7 Rename map (old → new)

| Old lane | New lane | Notes |
|---|---|---|
| `designer` | `primary-designer` | Default scope was already workspace-wide |
| `designer-assistant` | (retired) | Capacity-shard → sub-tasks under named lane |
| `second-designer-assistant` | (retired) | Same |
| `operator` | `persona-operator` (default) | Today most operator work is Persona-side; subsystem-shard explicit going forward |
| `operator-assistant` | (retired) | Capacity-shard |
| `second-operator-assistant` | (retired) | |
| `system-specialist` | `system-designer` + `system-operator` + `system-deployer` | Today's single lane splits into three with clearer accountability. Likely most current work is `system-operator` or `system-deployer`. |
| `system-assistant` | (retired) | Capacity-shard |
| `second-system-assistant` | (retired) | |
| `poet` | `poet` | Unchanged |
| `poet-assistant` | (retired or → `poet-editor`) | If review cadence earns it, keep as `poet-editor`; otherwise retire. |

New lanes added: `persona-designer`, `criome-designer`, `criome-operator`,
`criome-deployer` (some of these had implicit assignment to `designer`
or `system-specialist` before).

### 4.8 Total cognitive surface

Before: 11 lanes, 5 of which have semantically-empty names
("assistant", "second-").
After: 10 lanes, every name a `(subsystem, discipline)` pair that says
exactly what it does.

When a new idea arrives, the user routes it to a lane by asking *what
subsystem? what discipline?* Two-question routing instead of "which
designer-assistant is free?"

---

## 5 · Reports: per-repo vs branches vs status quo

### 5.1 Repo-per-lane

**Pros**: clean per-lane history; independent retention/archival; no
commit churn between lanes; smaller `primary` checkout.

**Cons**:
- Cross-references break easier across repos than within (the
  "passable object" pattern in `skills/reporting.md` becomes
  cross-repo).
- `ghq` cloning of the workspace explodes (10+ repos instead of 1).
- Search-across-reports requires new tooling (today: one `grep`;
  tomorrow: `ghq list | xargs grep`).
- Discoverability degrades: today `ls ~/primary/reports/` shows every
  lane; tomorrow you'd need an umbrella listing.
- The Persona-native-mind direction (`primary-mind`, native typed work
  graph per `orchestrate/AGENTS.md` §"Command-line mind target") is the
  *real* destination. Splitting reports out is a sideways move that
  doesn't help the migration.

**Net**: the churn problem is real but the cost of the cure is high.

### 5.2 Branch-per-lane (jj-native)

Each agent works on a jj branch named `lane/<lane>/<topic>`. Commits
land on that branch without colliding with other lanes' commits.
Branches merge into `main` when work is reviewed or ready.

**Pros**: solves churn without new repos; uses jj's native model;
zero new tooling.

**Cons**: branches need a merge cadence (today's pattern is direct
commits to `main`); concurrent branches each fork from `main` may need
rebase coordination.

### 5.3 Per-subsystem repos

If we split, **`<subsystem>-reports`** (one per subsystem, not per
lane) is the middle ground:

- `primary-reports/`
- `persona-reports/`
- `system-reports/`
- `criome-reports/`
- `poet-reports/`

That's 5 repos. Each holds the reports from every discipline within
that subsystem (designer + operator + deployer all write into one
subsystem repo with subdirs). Cross-subsystem references stay
cross-repo; intra-subsystem stays cheap.

### 5.4 Recommendation

**Status quo (reports stay in `primary`) — no split today.**

Reasons:

1. The friction the split solves (commit churn) is real but not
   blocking. Yesterday's session had ~5 concurrent agents writing
   reports; commits interleaved cleanly with jj's snapshot model.
2. The friction the split *introduces* (cross-repo references, search,
   onboarding) is permanent.
3. The destination is the Persona work-graph in `persona-mind`. A
   per-lane reports repo is a midway state that doesn't accelerate the
   destination.

**If the churn pain proves real over the next 2-3 weeks of operation**,
the right next step is *per-subsystem* repos (5 repos), not per-lane
(10+). That's also a cleaner cut at the bounded-context boundary.

**`primary-reports` carve-out** (a lighter alternative): if the user's
main pain is that `primary`'s git history is dominated by report
churn, we could split *just the reports* into a single `primary-reports`
repo (one repo, not 10) with subdirs per lane. This preserves the
`reports/<lane>/` structure, separates report history from code/skill
history, and avoids the per-lane explosion. **This is the move I'd
recommend if you want to do something now.**

---

## 6 · `skills/repository-creation.md` outline (draft)

Section list (full draft to land in a follow-up; this is the skeleton):

- **When to create a new repo (vs adding to existing)** — invoke
  `skills/micro-components.md` §"Adding a feature defaults to a new
  crate"; name the burden-of-proof rule; list the three legitimate
  "add to existing" cases (same capability, sibling test, derive-of-
  this-crate).
- **Naming rules — prefix selection** — `signal-` / `persona-` /
  `signal-persona-` / `owner-signal-persona-` / `nota-` / `mentci-` /
  `CriomOS-` / `criomos-` / `nexus-` / `sema-` / `kameo-`; "prefix
  names family membership"; warn against squatting subsystem
  namespace.
- **Naming rules — suffix selection** — `-cli` / `-lib` / `-derive` /
  `-codec` / `-config` / `-archive` / `-engine` / `-tools` / `-egui` /
  `-test`/`-testing` / `-rs`; clarify that `-daemon` is a binary name
  inside the unsuffixed repo.
- **Naming rules — no-prefix case** — standalone-identity rule;
  family-namesake rule; the test ("does this concept have or expect
  siblings?").
- **Required top-level files (canonical shape)** — the 14-file
  template: `AGENTS.md`, `ARCHITECTURE.md`, `CLAUDE.md`, `README.md`,
  `Cargo.toml`, `Cargo.lock`, `flake.nix`, `flake.lock`,
  `rust-toolchain.toml`, `skills.md`, `LICENSE.md`, `src/`, `tests/`;
  cite `criome`, `persona-router`, `sema`, `signal-core` as templates.
- **Skeleton-vs-implementation repos** — when a repo legitimately
  exists in skeleton form (namespace lock, spec only); cite `lojix`
  and `signal-lojix` as canonical skeletons.
- **Flake conventions** — flake arrives with code; pure-prose/data
  repos omit; Nix-only repos have flake without Cargo.
- **`AGENTS.md` / `CLAUDE.md` / `skills.md` / `ARCHITECTURE.md`
  responsibilities** — invoke `ESSENCE.md` §"Documentation layers".
- **`Cargo.toml` conventions** — `edition = "2024"`,
  `license = "MIT OR Apache-2.0"`, `publish = false`, `repository`
  URL; `[lib] name = "<repo_with_underscores>"`; `[[bin]] name =
  "<repo>-daemon"` for daemon crates; `[lints.rust]`
  `unsafe_code = "forbid"`; deps via `git = ".../<repo>.git"`, never
  `path =`.
- **Lifecycle — creation** — `gh repo create LiGoldragon/<name>
  --public`, bootstrap, add to `protocols/active-repositories.md`,
  symlink into `~/primary/repos/`.
- **Lifecycle — naming changes** — when (concept changed, family
  graduated); how (gh rename + jj remote URL update + symlink +
  `active-repositories.md` + `Cargo.toml repository` + every
  consumer's `git = ...` line); cite the `lojix-daemon` → `lojix`
  rename.
- **Lifecycle — retirement and archival** — move to "Retired /
  Cleanup Targets"; rename to `<name>-archive`; leave consumers pinned.
- **Workspace integration** — which section of
  `protocols/active-repositories.md`; `~/primary/repos/<name>`
  symlink; ghq layout; `RECENT-REPOSITORIES.md`. Cross-reference
  existing `skills/repository-management.md` for `ghq`/`gh` mechanics.
- **Two-stack discipline** — production-stack repos on `main`-only
  edits; lean-rewrite repos on `horizon-leaner-shape` worktree.
  Cross-reference `skills/feature-development.md` and
  `protocols/active-repositories.md` §"Two deploy stacks coexist".

The existing `skills/repository-management.md` (~140 lines) covers
ghq/gh mechanics. The new `skills/repository-creation.md` covers
**discipline**: naming, shape, lifecycle. They're complementary; both
land.

---

## 7 · Skill directory subdivision

### 7.1 Research consensus: keep flat

Anthropic's official `anthropics/skills` is flat (17 directories under
`skills/`, no category folders). LangChain's `tools/` is flat (hundreds
of integrations). The Agent Skills open spec doesn't mandate
hierarchy; client conventions add tags as metadata.

**Selection-accuracy phase transition at ~50-100 skills**
(arXiv:2601.04748): below this count, flat works; above, hierarchical
chunking is needed. Primary has **37 skill files**. Subdivision is
premature for the count.

### 7.2 Minimum viable carve: `skills/roles/`

If we carve anything, carve out role files only:

```
skills/
├── roles/
│   ├── designer.md
│   ├── operator.md
│   ├── system-specialist.md     # or rename when role taxonomy lands
│   ├── poet.md
│   └── role-lanes.md
└── (other 32 skills stay flat)
```

This matches the actual structural distinction the workspace already
enforces: role files are entry points into role-specific reading lists;
the rest is consulted by topic. The carve is mechanical (5 files
moved), and AGENTS.md tier-table references can be updated in one
pass.

### 7.3 Counter-recommendation: do nothing

A flat 37-file directory is comfortably scannable in one `ls` screen.
**Don't subdivide until the count or topical heterogeneity earns it.**
The cost of subdivision:
- AGENTS.md tier-table references break (currently cite
  `skills/component-triad.md`, etc.); every required-reading list in
  every role skill needs path updates.
- A skill sitting between two buckets (e.g. `skills/testing.md` is
  workflow *and* programming) creates an artificial choice.
- Generic-workspace ambition works *better* with flat layout (no
  bucket negotiation for contributed skills).

### 7.4 Recommendation

**Carve only `skills/roles/`** (5 files) as part of the role rename.
Leave the other 32 flat. Revisit if the count exceeds ~60 or topical
heterogeneity grows.

### 7.5 The "core + extension" pattern (for future generic-workspace)

When primary becomes cloneable-by-others, adopt **scope tiers + name
precedence** (Claude Code's model) — not on-disk subdivision. The
shape:

```
skills/             (workspace-core; ships with primary)
skills-local/       (gitignored; user-specific overrides)
skills-overlay/     (optional submodule; community-contributed)
```

Same-name skills override by tier: `skills-local/foo.md` overrides
`skills/foo.md` for agents in that workspace. Or adopt the
`.claude-plugin/` packaging idiom: shippable bundles with their own
`skills/` subdir and a manifest.

This pattern is out of scope for the role rename; it lands cleanly
later.

---

## 8 · Generic-workspace ambition: deferred

The user mentioned wanting to make primary cloneable-by-others. This
is a real ambition but it's downstream of the role rename. Reasons to
defer:

1. The role pain is acute now; the generic-workspace question is
   not.
2. Generic packaging needs to decide: scope tiers (Claude Code), plugin
   bundles (Anthropic), or distribution split (LangChain). That's a
   design pass on its own.
3. Naming the workspace `primary` already implies it's *one user's*
   workspace, not a public library. A future "primary-template" or
   `claude-workspace-template` would be a separate repo.
4. The role rename is reversible; the generic-workspace decision
   isn't, because it sets API/extension expectations.

Land the role rename and repo discipline first. The generic-workspace
arc can begin once those have a month of operation behind them.

---

## 9 · Action plan

Six stages, each independently revertable. Earlier stages don't depend
on later stages, so we can pause anywhere.

### Stage A — Land `skills/repository-creation.md`

Smallest, cleanest, lowest-risk. The agent already drafted a strong
outline. Land the skill file. No code change. No rename. Cite the
existing conventions; make them explicit.

**Effort**: ~30 minutes editing time.
**Reversible**: trivially.

### Stage B — Rename lanes

Update the lane key from current names to `(subsystem, discipline)`.
Specifically:

1. Update `orchestrate/roles.list` with the new lane names.
2. Update `orchestrate/AGENTS.md` lane table.
3. Update `AGENTS.md` lane references.
4. Rename `orchestrate/<old>.lock` → `orchestrate/<new>.lock` (lock
   files are gitignored, so this is a local rename only).
5. Rename `reports/<old>/` → `reports/<new>/` for each lane. This is
   a directory move; report numbers retained.
6. Update `skills/<role>.md` files: `skills/operator.md` and
   `skills/designer.md` stay as the discipline files; rename
   `skills/system-specialist.md` to `skills/system.md` (or split into
   `system-designer.md`, `system-operator.md`, `system-deployer.md`?
   one option: keep one combined `system.md` with sections; another
   option: split — discuss).
7. Update `skills/role-lanes.md` for the new mechanism (lanes do
   `(subsystem, discipline)`; capacity is via sub-task spawn).

**Effort**: ~2 hours editing time.
**Reversible**: yes, but file paths change so reverting means moving
report directories back.

### Stage C — Drop assistant/ordinal lanes; introduce sub-task spawn pattern

After Stage B, the assistant lanes don't exist. Codify the spawn
pattern:

1. New section in `skills/role-lanes.md`: "Capacity beyond one agent
   per lane — anonymous sub-task spawn".
2. Update `orchestrate/AGENTS.md` to remove assistant references.
3. Update `AGENTS.md` lane table.

**Effort**: ~30 minutes.
**Reversible**: yes.

### Stage D — Carve `skills/roles/`

1. Move `skills/operator.md`, `skills/designer.md`,
   `skills/poet.md`, plus the new `system-*.md` files into
   `skills/roles/`.
2. Move `skills/role-lanes.md` into `skills/roles/`.
3. Update AGENTS.md tier-table references and every cross-reference
   in the workspace (find/replace pass).

**Effort**: ~1 hour.
**Reversible**: yes (move back).

### Stage E — `primary-reports` carve-out (optional)

If commit-churn pain remains after 2-3 weeks:

1. Create `primary-reports` repo (one repo, all lanes).
2. Move `reports/` into it as a submodule or sibling clone.
3. Update cross-references in skills if any (`skills/reporting.md`
   primarily).
4. Add to `protocols/active-repositories.md`.

**Effort**: half a day.
**Reversible**: yes, but cross-references will have moved.

### Stage F — Generic-workspace packaging (deferred)

Out of scope for this iteration. Plan a separate design pass after
Stage E if the user still wants it.

### Recommended starting point

**Stage A** (land the repo-creation skill) and **Stage B + C** (rename
lanes, drop assistant pattern) are the high-leverage moves. Both can
land in one session. Stage D (skills/roles/ carve) is nice-to-have and
can come right after.

Stages E and F are conditional — defer to operational evidence.

---

## 10 · Open questions for the user

The decisions below shape the rename. Each carries the substance
inline so the user can react without opening files.

### Q1. Subsystem boundaries

I propose **5 subsystems**: `primary`, `persona`, `system`, `criome`,
`poet`. Two specific edge cases:

- **Is `lojix` part of `system` or its own subsystem?** Today
  `lojix-cli` (production) is on `main`; the lojix daemon rewrite is
  on `horizon-leaner-shape`. It's not part of CriomOS (the OS), but it
  IS the deploy orchestrator that CriomOS uses. Lean: fold under
  `system` (system-designer designs deploy; system-operator implements
  lojix; system-deployer runs deploys). Alternative: split — a
  `lojix` subsystem distinct from `system`.

- **Is `arca` part of `system` or its own subsystem?** Today the arca
  daemon doesn't exist yet (`/git/.../arca` is skeleton). Same
  question. Lean: fold under `system` for now; carve into its own
  subsystem when the arca daemon ships.

**Confirm**: 5 subsystems as named, or different boundaries?

### Q2. The deployer role

Three deployer lanes proposed (`system-deployer`, `criome-deployer`,
optional `persona-deployer` later). The split from operator is
defensible if the deployer owns a *distinct artifact surface*:
production cluster state, on-call, cutover orchestration. If today's
`system-specialist` is just "design + implement + occasionally
deploy", the split creates ceremony without clear ownership.

**Confirm**: real split (three lanes), or fold deployment back into
operator until volume justifies?

### Q3. Reports: stay in `primary`, or carve out?

Recommendation: stay in `primary` for now; carve into one
`primary-reports` repo (single repo, all lanes) if churn pain remains.
Per-lane repos (10+) is over-engineered.

**Confirm**: stay; carve `primary-reports`; or per-subsystem (5
repos)?

### Q4. `skills/roles/` subdivision

Recommendation: carve out `skills/roles/` (5 files: 4 role disciplines
+ `role-lanes.md`). Leave the other 32 flat.

**Confirm**: carve; or do nothing (keep flat); or carve more (also
`skills/craft/`, `skills/architecture/`, etc.)?

### Q5. Concept mode

Recommendation: capture "concept / detailed / review" as a
`skills/design-modes.md` section, not as separate lanes.

**Confirm**: as a mode; or as a separate cross-subsystem lane
(`concept-designer` cross-cutting)?

### Q6. Poet specialization

Recommendation: `poet` lane stays one combined role; add `poet-editor`
only if review cadence justifies. No Vedic/Greek/etc. specialization
until volume earns it.

**Confirm**: one `poet`; one + editor; or split by style?

### Q7. Stage A vs full sweep

Recommendation: Land Stage A (skills/repository-creation.md) and
Stage B+C (lane rename + assistant retirement) in the next session.
Stage D (skills/roles/) right after.

**Confirm**: that ordering; or different sequencing; or pilot one
stage first?

---

## See also

- `reports/designer/215-workspace-state-of-art-2026-05-18.md` — the
  current workspace state-of-art that this redesign sits on top of.
- `AGENTS.md` — workspace-level discipline (will need updates in Stage B/C).
- `orchestrate/AGENTS.md` — lane mechanism (will need updates in Stage B/C).
- `skills/repository-management.md` — existing repo skill that the new
  `repository-creation.md` complements.
- `skills/role-lanes.md` — current lane meta-pattern; updates in Stage C.
- `protocols/active-repositories.md` — repo discipline that
  `repository-creation.md` will codify.

### External (cited from agent research)

- Kim et al. 2025, *Towards a Science of Scaling Agent Systems* —
  arXiv:2512.08296
- *Survey on LLM-based Multi-Agent System* — arXiv:2412.17481
- *When Single-Agent with Skills Replace Multi-Agent Systems* —
  arXiv:2601.04748
- Anthropic Engineering, *How we built our multi-agent research system*
- Anthropic, *Building Multi-Agent Systems: When and How*
- MetaGPT — arXiv:2308.00352
- *Agent as Bounded Context* (Kostyra)
- Manus context engineering (rlancemartin.github.io)
- Claude Code subagents catalog (VoltAgent)
- Anthropic `skills` repo
- Claude Code skills documentation
- Agent Skills open specification
- SFIA-online
- AgentPatterns "Multi-Agent Overkill"
