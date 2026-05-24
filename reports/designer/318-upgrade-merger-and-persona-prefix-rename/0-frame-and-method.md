*Kind: Frame · Topic: upgrade-merger-and-persona-prefix-rename · Date: 2026-05-24*

# 318 · Frame — upgrade triad merger + persona-prefix removal sweep

## §1 Psyche ask + intent captured

> Okay, let's do all of the renaming, merging of the upgrade
> component as upgrade, called upgrade, signal upgrade, owner
> signal upgrade. And that's also file all the beads for all the
> rename for all components to drop the persona suffix except for
> components that have their own binary like persona codex, persona
> claude, persona pi, if these already exist. […] So this is a
> massive repository rename. And then all the dependency paths have
> to be changed because we're going to change the repo names. So do
> a complete research on how this would be done.

Three intent records captured before this dispatch:

- **Spirit 369** (Decision · upgrade-component · Maximum) — merge
  sema-upgrade + version-handover into one `upgrade` component
  triad: `upgrade` (daemon) + `signal-upgrade` (working) +
  `owner-signal-upgrade` (owner). `version-projection` stays a
  separate library. PrototypeHandover deletes. Two MigrationIndex
  types collapse to one. AttemptHandover/AttemptUpgrade resolves
  to one AttemptUpgrade verb.
- **Spirit 370** (Principle · reporting · Maximum) — reports not
  in the working tree live in the commit tree; access via
  `jj show <change>:path` or `git show <commit>:path`. Already
  landed in `skills/reporting.md` §"Deleted reports live in the
  commit tree."
- **Spirit 371** (Decision · component-naming · Maximum) — drop
  persona- prefix from component crate names workspace-wide.
  Exception: agent-harness components (persona-codex,
  persona-claude, persona-pi, persona-gemini, persona-open-code)
  keep the prefix. Persona itself stays persona (its NAME, not a
  prefix).

## §2 Three slices, parallel subagent dispatch

The work splits cleanly into three sub-agent slices. Per spirit
record 231, the meta-report directory is the session unit; each
slice writes a numbered sub-report.

- `0-frame-and-method.md` (this file) — orchestrator frame.
- `1-rename-inventory-and-dependency-graph.md` — Subagent A ·
  enumerate every repo + Cargo.toml + source-code reference + Nix
  flake input touched by either the upgrade merger OR the
  persona-prefix rename. Map dependency graph. Identify per-triad
  rename ordering constraints.
- `2-rename-tooling-and-mechanics.md` — Subagent B · research the
  mechanical how-to for atomic per-triad rename. Cargo workspace
  rename mechanics, Nix flake input updates, ghq + GitHub rename
  coordination, jj headless commit patterns. Feasibility
  assessment.
- `3-upgrade-triad-structural-design.md` — Subagent C · design the
  4-crate upgrade structure (`upgrade` daemon, `signal-upgrade`,
  `owner-signal-upgrade`, `version-projection` library). Exactly
  which operations land in which crate. Confirm: signal-upgrade
  carries the full operation surface (catalogue/flow +
  handover-protocol); component daemons implement only the
  handover-protocol subset and `RequestUnimplemented` the
  catalogue/flow verbs. What deletes (PrototypeHandover, both
  temp bins, redundant MigrationIndex).
- `4-overview-and-bead-list.md` — orchestrator synthesis +
  operator-bead decomposition + recommended landing order.

## §3 Slice contracts

### §3.1 Subagent A — rename inventory + dependency graph

Must produce a structured report covering:

- **Full repo rename list.** Walk `/git/github.com/LiGoldragon/`
  + `protocols/active-repositories.md`. For every component crate
  (and its signal-X + owner-signal-X siblings), name:
  (current crate name, new crate name, repo path on disk, whether
  it's an agent-harness exception). Include sema-upgrade +
  version-handover crates in the upgrade-merger column.
- **Dependency graph.** For each renamed crate, walk its
  consumers — every other crate that imports it (`Cargo.toml`
  `[dependencies]` entries; source-level `use` statements).
  Produce a topological order so consumers update after their
  dependencies' Cargo.toml has its new name.
- **Source-level reference counts.** For each crate, count
  references to its current name in source (`grep -r
  "signal_persona_spirit"` etc.) so operator estimates the
  blast radius of each per-triad rename.
- **Nix flake input inventory.** Each repo has `flake.nix` with
  inputs; renaming a repo on GitHub requires flake input URLs to
  update plus `flake.lock` refresh in dependents. Enumerate the
  flake-input dependency graph.
- **External CI / deploy references.** Anything in
  CriomOS-home, persona deploy scripts, or other infra repos
  that names a current crate name explicitly.
- **Per-triad rename order.** Recommended ordering — leaf
  components (no consumers) first, then components with
  consumers, then Persona (which consumes many). Spirit pilot
  in-flight (`primary-x3ci` + `primary-wdl6`) — flag whether
  signal-persona-spirit rename must wait or can land in parallel.

Hard constraints:
- READ-ONLY on code. Use Read/Grep/Glob/Bash for grep/find/ls.
- No `/nix/store` filesystem search; use `nix eval` / `nix
  flake show` / `nix path-info` if needed.
- No emojis; no `---` horizontal-rule lines.
- File:line citations on every concrete claim.
- jj headless ONLY if you commit (you should not need to):
  `jj describe -m '<msg>'`.
- Write to `1-rename-inventory-and-dependency-graph.md`.
- Mermaid label discipline per `skills/mermaid.md` §"Label
  sizing" — short prose in nodes, IDs in sibling tables.

### §3.2 Subagent B — tooling + mechanics

Must produce a structured report covering:

- **Cargo rename mechanics.** Per workspace: does `cargo` natively
  support a coordinated multi-crate rename, or is it manual? How
  does Cargo.toml `package = "old-name"` directive interact with
  rename (likely the rename target IS to update the
  `[package].name` field; the `package =` directive in dependents
  bridges old↔new during transition if needed). Verify against
  Cargo manifest docs / `cargo` source — do not invent.
- **Nix flake mechanics.** Each repo's `flake.nix` has a
  `description`, `inputs` (other flakes), `outputs`. Renaming a
  flake requires (a) updating the renamed flake's own `description`
  + flake input refs to ITSELF in dependents, (b) `flake.lock`
  refresh in every dependent. Walk through one example end-to-end
  (e.g., renaming `signal-persona-spirit` → `signal-spirit`):
  what changes in the `signal-persona-spirit` repo, what changes
  in dependents.
- **ghq + GitHub rename mechanics.** ghq mirrors GitHub repo
  URLs. Renaming a repo on GitHub creates a redirect; ghq's local
  path is `/git/github.com/<owner>/<old-name>`. Does ghq follow
  the rename automatically (probably no — need to re-clone or
  `mv`)? What's the workflow for renaming locally first, then
  on GitHub, then refreshing dependents?
- **jj for the rename commits.** Each rename touches many files
  (Cargo.toml + flake.nix + every src/ file with `use` stmts).
  jj patterns for landing atomic per-triad rename commits;
  headless `jj describe -m '<msg>'` for the commit message;
  whether `jj split` is needed or single-commit-per-triad is
  cleaner.
- **Tooling: cargo edit, rg --replace, etc.** Survey the tools
  operator would reach for. Specifically: is there a
  workspace-wide rename helper, or does this run sed/rg?
- **Feasibility verdict.** End the report with a clear
  "feasible / has-blockers / blocked" verdict per sub-concern
  (Cargo, Nix, ghq, jj, tooling). Name any blockers explicitly.

Hard constraints: same as A. Write to
`2-rename-tooling-and-mechanics.md`.

### §3.3 Subagent C — upgrade triad structural design

Must produce a fresh DESIGN (not just audit). Sections:

- **The four-crate structure.** `upgrade` (daemon), `signal-upgrade`
  (working), `owner-signal-upgrade` (owner), `version-projection`
  (library). For each: what types/operations live here; what
  current crates contribute substance; what gets deleted; what
  carries forward unchanged.
- **Operation grouping.** `signal-upgrade` carries the FULL surface
  per psyche (one contract, not split into protocol + catalogue).
  Catalogue/flow verbs (Inspect, AttemptUpgrade, Report) +
  handover-protocol verbs (AskHandoverMarker, ReadyToHandover,
  HandoverCompleted, Mirror, Divergence, RecoverFromFailure).
  The `upgrade` daemon implements ALL; component daemons (per
  `RequestUnimplemented` discipline) implement only the
  handover-protocol subset on their private upgrade socket and
  return `RequestUnimplemented` for catalogue/flow verbs they
  receive.
- **Owner contract grouping.** `owner-signal-upgrade` carries
  Register, Allow, Block, Query (from owner-signal-sema-upgrade)
  + ForceFlip, Rollback, Quarantine (from
  owner-signal-version-handover). Confirm: does AttemptHandover
  (today's owner-version-handover verb) survive, or does the
  flow always go through `AttemptUpgrade` (which the daemon
  decomposes into handover-protocol calls)? Lean: AttemptUpgrade
  subsumes AttemptHandover; AttemptHandover deletes.
- **What gets deleted.** PrototypeHandover state machine (per
  `/317-1 §2.6` — superseded by persona-spirit production code).
  Two `MigrationIndex` types collapse to one (the
  `MigrationCatalogue` rename from `/317-overview §6`). Two temp
  bins (sema-upgrade-temporary + sema-upgrade-handover-temporary)
  retire as the upgrade daemon absorbs their roles.
- **Mirror payload coupling — does the merger change the analysis?**
  Per spirit 274, Mirror stays raw bytes. The merger puts
  Mirror in the same crate as the projection trait; does that
  change the raw-vs-typed analysis? Probably no (raw bytes wins
  on cross-component scope still). Confirm.
- **version-projection role.** Carries `VersionProjection` trait
  + `Projected` marker + `ContractVersion` + (renamed)
  `RuntimeMigrationLookup`. Stays a library because every
  contract crate depends on the trait (per spirit 366 next-as-dep
  design from `/317-3`). Confirm the boundary holds — nothing
  from sema-upgrade or version-handover needs to stay in
  version-projection beyond what's there today.
- **Daemon shape.** `upgrade` daemon's three sockets (ordinary +
  owner + private upgrade — wait, does the upgrade daemon ITSELF
  have a private upgrade socket? It's a triad daemon like any
  other, so per `skills/component-triad.md` yes, three sockets).
  Persona deploys the upgrade daemon as a systemd unit; persona's
  role narrows to engine supervision (start/stop) + the upgrade
  daemon owns orchestration.
- **Persona's narrowed role.** Today persona has
  `src/upgrade.rs` (746 lines) + four manager messages + owner
  handover dispatch. Most of that moves to `upgrade`. What stays
  in persona: unit start/stop (the systemd D-Bus client +
  `UnitController` trait). The `HandoverDriver` migrates from
  persona to upgrade.

Hard constraints: same as A/B. Write to
`3-upgrade-triad-structural-design.md`.

## §4 What the overview (file 4) integrates

After A/B/C return:

1. **Feasibility statement.** Bottom-line: is this whole sweep
   safe to land, what are the blockers (if any), what risks
   remain.
2. **Bead list.** Operator-sized beads, parallel where possible,
   sequenced where necessary. Each bead names its target crate(s)
   + scope + dependencies on other beads.
3. **Recommended landing order.** Concrete sequence: upgrade
   merger first or persona-prefix rename first or interleaved.
4. **Risk register.** Spirit pilot collision risk
   (`primary-wdl6` + `primary-x3ci` in flight); coordination
   risk; deploy graph risk.
5. **Open psyche questions.** Distilled from A/B/C; ≤6.

## §5 Constraints to keep in mind across the slice

- **PERSONA stays `persona`** — its name, not a prefix.
  `signal-persona` + `owner-signal-persona` keep that name.
- **Agent-harness components keep persona- prefix.** Today only
  `persona-pi` exists. Future: persona-codex, persona-claude,
  persona-gemini, persona-open-code per `/309`.
- **version-projection is NOT a triad** — stays a library.
- **Spirit pilot in flight.** `primary-wdl6` (v0.1.0 retrofit)
  + `primary-x3ci` (Spirit cutover) are deploy-gated;
  rename / merger work must not delay these. Lean post-pilot
  for the rename; the design beads can land in parallel.
- **Mermaid label discipline** (`skills/mermaid.md` §"Label
  sizing — short prose, IDs out of the node") — short prose
  in nodes, IDs in sibling tables.
- **`jj` headless only.** No `$EDITOR` prompts; use
  `-m '<msg>'` or `--use-destination-message`.
- **NOTA single-argument rule** in any example CLI invocation
  (`upgrade '(Inspect …)'` — never `upgrade inspect`).
- **No `/nix/store` filesystem search** in any subagent — use
  `nix eval` / `nix flake show` / `nix path-info`.
- **No `---` horizontal-rule lines.**
- **PascalCase identifiers spelled in full**
  (`MigrationCatalogue` not `MigrationCat`; `RuntimeMigrationLookup`
  not `RuntimeMigLookup`).

## §6 Notes on the agent-harness exception

Spirit 371's exception list names `persona-codex`, `persona-claude`,
`persona-pi`, `persona-gemini`, `persona-open-code`. Today only
`persona-pi` exists on disk; the others are planned per `/309`
(agent component abstraction). The rename sweep doesn't touch
agent-harness components; subagent A's rename inventory should
flag `persona-pi` (and any future agent-harness crates) as
deliberately kept.
