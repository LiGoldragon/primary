# Role to Skill Assignment Proposal

## Task and Scope

Propose a curated skill set for each of the 10 V1 worker roles. For every role:
the proposed skill-id list, a one-line justification per skill cluster, what was
deliberately excluded to avoid bloat, and any critical-doctrine skill currently
missing. A shared-by-all baseline is separated from role-specific assignments.
The proposal also states, as a requirement (not an implementation), the
generator and manifest change needed to express role to skill assignment, since
the dependency sidecar is empty today.

This is a read-only proposal. No source was edited. The single writable artifact
is this file.

## Sources Consulted

Role-source prose (the authority for each role's job):

- `/git/github.com/LiGoldragon/skills/roles/intent-translator/full.md`
- `/git/github.com/LiGoldragon/skills/roles/scout/full.md`
- `/git/github.com/LiGoldragon/skills/roles/repo-scaffolder/full.md`
- `/git/github.com/LiGoldragon/skills/roles/general-code-implementer/full.md`
- `/git/github.com/LiGoldragon/skills/roles/criomos-implementer/full.md`
- `/git/github.com/LiGoldragon/skills/roles/rust-auditor/full.md`
- `/git/github.com/LiGoldragon/skills/roles/nix-auditor/full.md`
- `/git/github.com/LiGoldragon/skills/roles/skill-editor/full.md`
- `/git/github.com/LiGoldragon/skills/roles/intent-maintainer/full.md`
- `/git/github.com/LiGoldragon/skills/roles/repo-operator/full.md`

Corpus and generator state:

- `/home/li/primary/skills/skills.nota` (the ~66-skill id list plus trigger
  descriptions and tier).
- `/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota` (the
  `(Role ...)` records; each role's module list is `[agent-output-protocol]`).
- `/git/github.com/LiGoldragon/skills/manifests/module-dependencies.nota` (every
  module plus every `role-*` module carries an empty `[]` dependency list).
- `/home/li/primary/.claude/agents/*.md` (emitted packets, approximately 4 KB
  each: role prose with `agent-output-protocol` inlined, no named skills).

## Observed Generator State (facts, not interpretation)

- The packet today is `<frontmatter>` + role prose + the inlined body of the one
  module `agent-output-protocol`. No skill is named by id anywhere in the packet.
- Assignment is already expressible in principle: the `(Role (<id>
  <role-source-module> [<modules>] [|desc|] [<targets>]))` record in
  `active-outputs.nota` has a module-list slot. It just contains a single id for
  every role.
- The sidecar `module-dependencies.nota` records `(<module-id> <source-path>
  [<dep-ids>])`. All dep lists, including the ten `role-*` records, are `[]`.
  This is the surface the brief identifies as the empty role to skill channel.

Interpretation: the corpus models each skill as a module; "assign skills to a
role" means populating that role's curated module set, either in the
`active-outputs.nota` module list or as dependency edges on the role module in
the sidecar. The generator change is a wiring and emit-semantics decision, not a
new data model.

## Shared Baseline (every spawned worker carries these)

Kept deliberately lean. These are the cross-cutting doctrines that apply
regardless of discipline.

| skill id | why baseline |
| --- | --- |
| `agent-output-protocol` | the durable output-file contract; already the one bundled module; keep |
| `reporting` | every worker emits output; chat-vs-report decision and output hygiene |
| `naming` | full-English-words rule applies to any identifier, filename, or bead title a worker writes |
| `workspace-vocabulary` | shared load-bearing glossary so all workers speak the same terms; supports "preserve the psyche's vocabulary" |
| `privacy` | defensive: keep private-affairs material off public surfaces (a workspace hard boundary) |
| `secrets` | defensive: never leak a token in any output, even when only observed |

Deliberately NOT in baseline: `keep-working`, `human-interaction`,
`intent-led-orchestration`, `when-to-use-helpers`, `autonomous-agent`,
`context-handover`. These are lead and psyche-boundary skills. The brief states
the lead is not a spawned worker role in this V1 set, so its orchestration and
human-boundary doctrine should not be sprayed across every worker packet. The
one exception is the intent-translator, which is itself a spawned worker and
legitimately owns the handoff protocol (see below).

`beauty` and `versioning` were considered for baseline and rejected: they apply
only to making and behavior-changing roles, not to read-only or intent roles, so
they are assigned per role instead.

## Role to Skill Table

Each cell below is role-specific and is carried IN ADDITION to the baseline.
"Conditional" entries are recommended only when the assignment touches that
surface; they are listed in the rationale, not auto-bundled.

| role | role-specific skills | excluded to avoid bloat | critical doctrine currently missing |
| --- | --- | --- | --- |
| intent-translator | `intent-led-orchestration`, `bead-weaver`, `beads`, `intent-clarification` | Rust/Nix clusters, `human-interaction`, `when-to-use-helpers` | `intent-led-orchestration`, `bead-weaver`, `intent-clarification` |
| scout | `nix-usage` (conditional: `engine-analysis`, `engine-report`) | all making/auditing doctrine, intent skills, helper dispatch | none critical; baseline `privacy`/`secrets` cover the read-only risk |
| repo-scaffolder | `repo-intent`, `rust-crate-layout`, `rust-discipline`, `nix-discipline`, `testing`, `architecture-editor`, `repository-management` | runtime Rust logic skills, deep engine skills, intent log | `repo-intent`, `rust-crate-layout`, `nix-discipline`, `testing` |
| general-code-implementer | `rust-discipline`, `rust-methods`, `rust-errors`, `rust-parsers`, `rust-storage-and-wire`, `rust-crate-layout`, `abstractions`, `typed-records-over-flags`, `beauty`, `enum-contact-points`, `actor-systems`, `kameo`, `component-triad`, `push-not-pull`, `subscription-lifecycle`, `testing`, `versioning` | Nix cluster, intent/bead skills, `jj` (operator owns commit) | the whole Rust cluster, `abstractions`, `actor-systems`, `beauty`, `enum-contact-points` |
| criomos-implementer | `nix-discipline`, `nix-usage`, `testing`, `versioning` (conditional: `component-triad`, Rust cluster) | Rust logic by default, bead/intent skills, `jj` | `nix-discipline`, `nix-usage`, `versioning` (deploy-slot), `testing` |
| rust-auditor | `rust-discipline`, `rust-methods`, `rust-errors`, `rust-parsers`, `rust-storage-and-wire`, `rust-crate-layout`, `abstractions`, `typed-records-over-flags`, `beauty`, `enum-contact-points`, `architectural-truth-tests`, `actor-systems`, `kameo`, `subscription-lifecycle`, `push-not-pull`, `component-triad`, `testing`, `versioning` | Nix cluster, intent/bead skills, `jj` | the Rust cluster plus `architectural-truth-tests` |
| nix-auditor | `nix-discipline`, `nix-usage`, `testing`, `versioning` (conditional: `component-triad`) | Rust cluster, intent/bead skills, `jj` | `nix-discipline`, `nix-usage`, `testing`, `versioning` |
| skill-editor | `skill-editor`, `prose`, `nota-design` (conditional: `nota-schema-docs`, `structural-forms`, `architecture-editor`, `testing`) | Rust/Nix logic, intent-log capture skills, `jj` | `skill-editor` (its own doctrine), `prose`, `nota-design` |
| intent-maintainer | `intent-maintenance`, `intent-log`, `spirit-cli`, `intent-manifestation`, `intent-clarification`, `repo-intent` (conditional: `architecture-editor`, `nota-design`) | Rust/Nix clusters, bead skills, `jj` | `intent-maintenance`, `intent-log`, `spirit-cli`, `intent-manifestation`, `intent-clarification` |
| repo-operator | `jj`, `beads`, `main-next`, `main-feature-integration`, `repository-management` (conditional: `report-naming`) | implementation/design skills, audit doctrine | `jj`, `beads`, `main-next`, `main-feature-integration` |

## Per-Role Rationale

### intent-translator
Source: `roles/intent-translator/full.md`. The role turns clarified intent into
a dependency graph, briefs, evidence expectations, and an audit recommendation,
and uses BEADS for tracked work.

- `intent-led-orchestration` plus `bead-weaver` plus `beads`: this role IS the
  Intent Translator handoff named in the orchestration protocol, and the work
  product is a bead dependency graph; `bead-weaver` is the conversion discipline
  and `beads` is the claim/close mechanism.
- `intent-clarification`: the contract explicitly says to write the question
  into the output instead of inventing a definition; this is that doctrine.
- Excluded: it works from already-clarified intent supplied by the lead, so
  `human-interaction` (live psyche boundary) and `when-to-use-helpers` (lead
  dispatch) are not its job; it names auditors but does not audit, so no Rust or
  Nix clusters.

### scout
Source: `roles/scout/full.md`. Read-only fact mapping with `rg`, `ls`, status,
and tool help; separates observation from interpretation.

- The baseline already supplies `reporting`, `naming`, `workspace-vocabulary`,
  `privacy`, `secrets`, which cover most of the scout's needs (precise paths,
  not opening private scopes, not echoing observed secrets).
- `nix-usage` (conditional): when the map touches Nix, this enforces inspection
  through `nix eval`/`flake show`/`path-info` rather than filesystem search,
  matching the workspace no-store-search boundary.
- `engine-analysis`/`engine-report` (conditional): only when scouting a daemon's
  internals; excluded by default to keep the scout lean.
- No critical doctrine missing; the scout is intentionally minimal.

### repo-scaffolder
Source: `roles/repo-scaffolder/full.md`. Prepares a new repo or structural
rework: guidance surfaces, build metadata, source layout, test entry points.

- `repo-intent`: the role establishes guidance surfaces, and the per-repo
  INTENT.md is named the first and most important file per repo. Critical.
- `rust-crate-layout` plus `rust-discipline`: the contract names keeping examples
  and source layout consistent with workspace Rust discipline.
- `nix-discipline` plus `testing`: the contract names exposing checks through the
  flake and setting up test entry points.
- `architecture-editor`: scaffolding establishes the ARCHITECTURE.md surface.
- `repository-management`: when the work creates a new remote (ghq/gh mechanics).
- Excluded: runtime Rust logic skills (`rust-methods`, `actor-systems`, etc.) and
  deep engine skills; the scaffolder builds the starting shape, not behavior.

### general-code-implementer
Source: `roles/general-code-implementer/full.md`. The primary code-writer; the
psyche named the Rust skills and `actor-systems` as the example assignment.

- Full Rust cluster (`rust-discipline`, `rust-methods`, `rust-errors`,
  `rust-parsers`, `rust-storage-and-wire`, `rust-crate-layout`): the craft this
  role applies on every edit. `rust-discipline` is the index that links the rest.
- `abstractions`, `typed-records-over-flags`, `beauty`, `enum-contact-points`:
  the keystroke and apex craft gates for engine logic and load-bearing branching.
- `actor-systems`, `kameo`, `subscription-lifecycle`, `push-not-pull`: the
  actor/async cluster the psyche pointed at; `kameo` is the runtime, the others
  the topology and lifecycle doctrine.
- `component-triad`: apex shape doctrine for the components this role edits.
- `testing` plus `versioning`: it runs checks and changes behavior that must keep
  versions truthful.
- Conditional for generator work: `nota-design`, `structural-forms`,
  `architectural-truth-tests`, `language-design` when the task touches
  schema-authored interfaces.
- Excluded: Nix cluster (separate implementer), intent/bead skills, and `jj`
  because the weave assigns final commit to the repo-operator.
- Note: this is the heaviest set on purpose; for the code-writer this is "enough,"
  not bloat. See the index-collapse lever under corpus-trim flags.

### criomos-implementer
Source: `roles/criomos-implementer/full.md`. CriomOS host, cluster, image, and
deployment work with extra care for running machines, secrets, and rollback.

- `nix-discipline` plus `nix-usage`: NixOS modules and reproducible builds, with
  store-path hygiene.
- `testing`: build, evaluation, and smoke checks appropriate to blast radius.
- `versioning`: explicitly covers deploy-slot versions, matching the contract's
  intended-state-transition and generation-identity language.
- Baseline `secrets` and `privacy` are load-bearing here (host credentials,
  personal infrastructure) and should be treated as primary, not incidental.
- Conditional: `component-triad` and the Rust cluster only when the host work
  includes component or Rust changes.
- Excluded by default: Rust logic skills and bead/intent skills.

### rust-auditor
Source: `roles/rust-auditor/full.md`. Independent review of substantial Rust
work; must cite the workspace rule by name.

- The set mirrors the implementer's Rust and actor clusters because you cannot
  audit a rule you do not hold; the contract names methods on data-bearing types,
  typed errors, no hand-rolled parsers, storage and wire safety, and crate
  layout, which map one to one to the cluster.
- Auditor-specific addition: `architectural-truth-tests` for judging whether the
  tests witness architecture rather than mere regression.
- `versioning` supports the public-API-compatibility review the contract names.
- Excluded: Nix cluster (that is the nix-auditor), intent/bead skills, and `jj`;
  the auditor does not implement or commit.

### nix-auditor
Source: `roles/nix-auditor/full.md`. Independent review of Nix, flake, module,
package, and deployment changes.

- `nix-discipline` plus `nix-usage`: the contract's "values reached through Nix
  rather than filesystem search" is exactly `nix-usage` doctrine; module shape
  and check derivations are `nix-discipline`.
- `testing` plus `versioning`: flake-check coverage and deployment-safety
  version truth.
- Excluded: Rust cluster (rust-auditor owns it), intent/bead skills,
  `repository-management`.
- This set is intentionally the mirror of the criomos-implementer's surface.

### skill-editor
Source: `roles/skill-editor/full.md`. Edits skill-system content: source
modules, role modules, manifests, dependency indexes, instruction prose, and
owns generated-surface reconciliation.

- `skill-editor`: the role's own defining doctrine, currently absent from its
  packet. Critical and slightly ironic.
- `prose`: the instruction surface is prose as a load-bearing craft.
- `nota-design`: the manifests and the dependency index it maintains
  (`active-outputs.nota`, `module-dependencies.nota`) are NOTA records.
- Conditional: `nota-schema-docs` (documenting schemas), `structural-forms` (if
  editing schema-next grammar), `architecture-editor`, and `testing` (running the
  generator or parser check during reconciliation).
- Excluded: Rust and Nix logic, intent-log capture skills, and `jj`.

### intent-maintainer
Source: `roles/intent-maintainer/full.md`. Intent-log work, supersession,
manifestation, and cleanup; quotes psyche statements without overextending.

- `intent-maintenance`: the role's defining sweep-and-supersession doctrine.
- `intent-log` plus `spirit-cli`: the record shape and the deployed CLI wire
  shape it must use to capture and query.
- `intent-manifestation`: walking Spirit records into the right durable surface,
  quoting verbatim, which the contract names directly.
- `intent-clarification`: write the exact clarification question when meaning is
  unclear, which the contract names.
- `repo-intent`: a primary manifestation target surface.
- Conditional: `architecture-editor` and `nota-design` as further manifestation
  targets.
- Baseline `privacy` is load-bearing (no private material on public surfaces).
- Excluded: Rust/Nix clusters, bead skills, `jj`.

### repo-operator
Source: `roles/repo-operator/full.md`. Final repository mechanics after
validation and audit: status, version control, commit, push, bead closeout.

- `jj`: the version-control discipline for concurrent agents, including the
  push-rejected escape hatch; the role's defining mechanism.
- `beads`: close or update tracked items only after durable evidence exists.
- `main-next` plus `main-feature-integration`: the operator branch and bookmark
  policy for code repos, and the producers-before-consumers integration order;
  the integration skill literally describes the operator role.
- `repository-management`: push and PR/closeout mechanics.
- Conditional: `report-naming` for handoff/closeout notes.
- Excluded: implementation and audit doctrine; the operator routes findings back
  rather than fixing them.

## Generator and Manifest Requirement (requirement, not implementation)

The role to skill channel must become expressible and then expressed. Three
requirements, in priority order.

1. Populate the curated set per role. Two existing surfaces can carry it; the
   psyche or generator owner should pick one as canonical:
   - the `[<modules>]` slot of each `(Role ...)` record in
     `active-outputs.nota`, extended from `[agent-output-protocol]` to the
     curated id list; or
   - the `[<dep-ids>]` slot of each `role-*` record in
     `module-dependencies.nota` (currently `[]`), resolved transitively by the
     generator into the packet.
   The sidecar route is the better fit for a shared baseline: declare the
   baseline once as a dependency every role module carries, and let transitive
   resolution dedup, rather than hand-copying six baseline ids into ten records.

2. Decide emit semantics: NAME versus INLINE. This is the load-bearing
   requirement and the biggest open question. Inlining approximately fifteen full
   skill bodies into the heaviest packets would grow each from roughly 4 KB to
   tens of KB, which contradicts "enough, not bloated." The requirement is that a
   packet NAMES its curated skill ids and points at `skills.nota` for on-demand
   loading, keeping only the true always-on contract (`agent-output-protocol`,
   and possibly the lean baseline) inlined. The generator needs a per-module flag
   or two module classes (inline versus reference) to express this.

3. Express the baseline once. Whatever surface is chosen, the shared baseline
   must be a single declaration applied to all roles, not duplicated per record,
   so it can evolve in one place.

Out of scope for this proposal: writing the generator code or editing the
manifests. That is Skill Editor and generator-implementer work, gated on the
psyche's answer to requirement 2.

## Dependency on the Corpus-Trim Proposal (flags)

This proposal works from the CURRENT 66-skill corpus. A separate corpus-trim
worker may merge or eliminate skills. Picks that a likely trim would change:

- Rust sub-cluster collapse: `rust-methods`, `rust-errors`, `rust-parsers`,
  `rust-storage-and-wire`, and possibly `rust-crate-layout` could fold into the
  `rust-discipline` index. If so, general-code-implementer and rust-auditor would
  carry `rust-discipline` (plus `abstractions`, `typed-records-over-flags`,
  `beauty`) as the anchor and drop the explicit sub-ids. This is also a standalone
  lever: even without a trim, naming `rust-discipline` alone reduces the count
  because the index points at its sub-files.
- Nix pair collapse: `nix-discipline` plus `nix-usage` could merge into one Nix
  skill, changing criomos-implementer, nix-auditor, repo-scaffolder, and scout.
- Intent cluster consolidation: `intent-log`, `spirit-cli`, `intent-clarification`,
  `intent-manifestation`, `intent-maintenance` could consolidate, changing
  intent-maintainer and intent-translator.
- Bead pair: `beads` plus `bead-weaver` could merge, changing intent-translator
  and repo-operator.
- Operator branch pair: `main-next` plus `main-feature-integration` could merge,
  changing repo-operator.
- Baseline overlap: `reporting`, `report-naming`, and `agent-output-protocol`
  partly overlap; a trim could collapse the output-hygiene baseline.

Picks a trim would NOT change: none of my core worker assignments depend on the
likely-trim-candidate skills `workspace-update-report`,
`double-implementation-strategy`, `engine-report`, `engine-analysis`, `mermaid`,
`stt-interpreter`, or `nota-comments`. These were already excluded as
lead-tier or over-specialized, so their elimination leaves the worker sets
intact. Lead and helper-dispatch skills (`human-interaction`,
`when-to-use-helpers`, `helper-context-transfer`, `context-handover`,
`context-maintenance`, `context-maintenance-deep`, `autonomous-agent`) are also
unassigned to workers, so trimming them does not change these picks.

## Open Questions and Blockers for the Psyche

1. (Biggest) NAME versus INLINE: should a packet inline the full body of each
   curated skill, or name the skill ids and rely on on-demand loading from
   `skills.nota`? The answer decides whether "enough, not bloated" is achievable
   and shapes the generator change. Recommended default: name, do not inline.
2. Baseline size: is the proposed six-entry baseline (output-protocol, reporting,
   naming, workspace-vocabulary, privacy, secrets) the right floor, or should
   `secrets`/`privacy` be load-on-encounter rather than always-present?
3. Index-collapse policy for Rust: should the heavy roles carry the explicit Rust
   sub-cluster, or only the `rust-discipline` index and trust agents to follow it
   to the sub-files? This interacts directly with the corpus-trim proposal.
4. Conditional handling: should conditional skills (for example `nix-usage` for
   scout, the Rust cluster for criomos-implementer) be carried always, or only
   bound to assignments that touch that surface? V1 packets are static, so
   "conditional" may have to resolve to "always carry" or "never carry."

## Verification of This Proposal

- Every role's job was read from its source path (listed above) before assigning
  skills.
- Every proposed skill id exists in `skills.nota` and `module-dependencies.nota`.
- Lead-only and helper-dispatch skills were held out of worker packets per the
  brief's statement that the lead is not a spawned worker role in V1.
- Not done (out of authority): no manifest or generator edit, no validation that
  the generator can emit named-but-not-inlined references; that is the emit-
  semantics question above.
