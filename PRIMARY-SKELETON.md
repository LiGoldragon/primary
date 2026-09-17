# Primary next: pre-v1 skeleton specification

Status: design POC, 2026-09-17. Authoring flow: `f60a1e`.
This document specifies the next repository and makes the inventory decisions.
It does not activate that repository, migrate records, rewrite history, delete
files, change harness configuration, or modify Curriculum. `pre-v1` is a design
stage here, not a released package version.

## 1. Decision and source boundary

Primary becomes a small, shared workspace bootstrap. Curriculum supplies the
skills selected for a flow when Flow provisions its launch. Durable psyche,
flow records, coordination state, executable tools, and repository history have
owners outside the new primary checkout. Every primary flow uses the same
working directory and main line; a launch configuration is not another clone
or worktree.

The September 17 records in flow `9993b5` are the governing source for this
design. Their original location is:

`/home/li/wt/github.com/LiGoldragon/primary/claude-successor-efa157-jj/.claude/worktrees/flow-9993b5/flows/9993b5/vision/`

In `primarySkeleton.md`, the psyche typed:

> The way the data is kept, the primary workspace is minimal. It's just a skeleton. We need to make this primary, version 1. This was version 0. Now we're going to make pre-version 1, so we rebase the repo from almost nothing and only keep what we want to keep, which is the skeleton for the skill files to come into. Maybe primary has some skills already, and so they're all suffixed. They could have a prefix, I guess, but some are not agent-visible. We have to document how that works in every harness, too.

The decisions below are this flow's design, not additional words attributed to
the psyche. They apply these records together:

| Record | Constraint applied here |
| --- | --- |
| `primaryNext.md`, `oneSharedPrimary.md`, `sharedWorkspace.md` | One shared primary working surface; Flow's database is shared across layers. |
| `workspaceProvisioning.md`, `curriculumNexus.md` | Flow requests a curriculum; Curriculum owns skill delivery and a Nix-declared reseed path. |
| `worktreeHygiene.md`, `sprawlFix.md` | Stop multiplying primary's data, tools, and history across launches. |
| `transcriptOverFiles.md` | Transcripts and Nexus data replace accumulating report and bookkeeping files. |
| `visionAccessibleToAll.md` | All flows can retrieve the complete psyche corpus, including raw vision; distillation does not gate access. |
| `noMoreBranches.md`, `launchOnMain.md`, `orchestrateCommitBinding.md` | Work on shared main; lock exact writes; the lock description is the commit description. |

The current `ARCHITECTURE.md` describes a larger coordination repository and
older lane/role arrangements. It is evidence of v0, not the target inventory.
The August record `flows/1030529c/vision/workspace20.md` proposed parent
workspaces per aspect and smaller flow workspaces. Its concern about selecting
context survives; the later one-shared-primary instruction determines the
working-directory design. Parent instruction discovery alone cannot select a
different curriculum for two flows with the same working directory.
`flows/7b4d4c/reports/psyche-harnesses.md` is an agent collection of sources,
including Pi's retirement direction; it is not a substitute for harness code.

## 2. Exactly what the new repository contains

The initial tracked tree has nine files. All other old top-level content is
accounted for in the inventory below. Empty generated directories need no
placeholder files.

```text
primary/
  .gitignore
  README.md
  ARCHITECTURE.md
  SKILL_VARIABLES.md
  AGENTS.md
  CLAUDE.md
  bootstrap/
    manifest.datom
    skills/
      workspace-primary/SKILL.md
      provisioning-primary/SKILL.md
```

| File or directory | Content and owner |
| --- | --- |
| `README.md` | Short supported-use entry: what this checkout is, how Flow provisions it, and how to reach the shared records. |
| `ARCHITECTURE.md` | The accepted skeleton contract: ownership, provisioning, skill origin/visibility, and record locators. Replace v0's component and lane encyclopedia. This POC is the input to that rewrite; `PRIMARY-SKELETON.md` is not a tenth permanent file. |
| `SKILL_VARIABLES.md` | Setup-specific named values, one `Name: value` per line. Retain the existing variable names; update values at provisioning. No credentials. |
| `AGENTS.md`, `CLAUDE.md` | Small, generated common bootstrap entry files, sourced from Curriculum. They carry universal workspace obligations and variable references, with no aspect-specific role/awareness body. Their contents are stable across concurrent launches. |
| `bootstrap/manifest.datom` | The bundle inventory and provenance: bundle revision, Curriculum seed revision, deployer revision, source identities, output digests, and each bundled skill's visibility. This is proposed deployment data, not a new hand-written parser or a currently supported deploy request. The deployer/Flow runtime owns its concrete schema; Curriculum remains the skill/role data source. |
| `bootstrap/skills/` | Exactly the two generated bundled skill snapshots listed above. Source remains the `*.md` files under the `Curriculum skills` variable. Primary does not become a second skill-authoring repository. |
| `.gitignore` | Excludes provisioning outputs, VCS-local state, logs/caches, and local repository links. No broad ignore of arbitrary authored documents that would conceal an accidental new permanent file. |

The two bundled skills have separate jobs:

| Skill ID | Visibility in an ordinary primary launch | Scope |
| --- | --- | --- |
| `workspace-primary` | Agent | Primary-specific coordination and record-location convention that must work before a role curriculum is available. Generic behavior, Spirit, tools, and domain doctrine continue to come from Curriculum. |
| `provisioning-primary` | Hidden | The bootstrap/provisioning procedure for the launcher or an explicitly selected operator context. Its file ships with primary but is absent from an ordinary primary flow's skill catalog and name-based loader. |

These are proposed source additions, not claims that these skills exist today.
Curriculum emits both the bundled snapshots and the launch projections. A
bundle release regenerates snapshots from its pinned authored sources. A
normal launch verifies and reuses the bundle; it does not edit shared tracked
entry files or replace another flow's snapshot.

### Generated local shape

Provisioning may create this ignored local tree:

```text
.primary/
  content/<curriculum-revision>/skills/<skill-id>/SKILL.md
  launch/<flow-id>/
    receipt.datom
    <harness configuration and selected skill projections>
.agents/   # only a common, universally eligible projection if required
.claude/   # same rule; no role union or worktrees
.codex/    # same rule
.pi/       # only if an explicitly requested Pi launch needs it
```

`.primary/content/` is outside the harnesses' configured discovery roots. It
may contain hidden skill files. `.primary/launch/` holds disposable launch
configuration, not flow memory, a Git repository, or a different working
directory. Where a harness recursively scans a configured parent, that parent
must exclude the content store and other flows' launch projections.

Common discovery roots expose only skills eligible for every flow that uses
them. Role-specific catalogs are immutable per-launch selections. A launcher
must never swap the shared `.agents/skills` or `.claude/skills` directory to
change one flow's role: a concurrent flow could reload the wrong selection.
The per-harness section says where native configuration can express this and
where an adapter is required.

The versioned skeleton has no `flows/`, corpus copy, daemon database, package
cache, checkout index, or executable implementation. Nearby component repos
stay under `Repository root`; runtime data and sockets are owned by their
services. A flow's working directory remains the shared primary root.

### Variables retained and added

Retain the current names `Orchestrate release request`, `Curriculum skills`,
`Claude transcript root`, `NixBuilder`, `Reference skill collections`, `Repository root`, `Standards`,
`The system`, and `The user environment`. Their current values are setup data
in `SKILL_VARIABLES.md`, not constants to embed in reusable skills.

Add named values for `Psyche records`, `Flow records`, `Workspace records`,
`Primary archive`, and `Curriculum service` when those destinations are
provisioned. These name actual mounted paths or service locators. The schema
and variable names are part of this design; endpoints must be witnessed before
activation, not filled with invented addresses. Service definitions, tools,
credentials, and reseed machinery stay in their owning Nix/component repos.

## 3. Skill marking and visibility contract

Use the suffix **`-primary`** for a skill shipped in the primary bootstrap
bundle: `workspace-primary`, for example. Keep the subject first so related
skills sort and read together, and follow the psyche's first suggestion. A
prefix would work technically; it adds no visibility information and is not
needed alongside the suffix.

The suffix marks distribution origin, independent of visibility. An overlay
from Curriculum keeps its canonical unsuffixed ID. Curriculum reserves the
`-primary` namespace for this bundle and rejects a same-ID overlay; it does not
silently shadow a bundled skill. Dependency references and rendered skill names
use the complete ID. Claude plugin namespacing, when present, is an additional
harness namespace and does not replace the canonical skill ID.

The deployment manifest needs these independent facts:

| Field | Meaning |
| --- | --- |
| Origin | `PrimaryBundle` or `CurriculumOverlay`; checked against suffix and source provenance. |
| Visibility | `Agent`, `UserOnly`, or `Hidden`, evaluated for this launch/aspect and harness. |
| Identity and revision | Canonical skill ID, authored source revision, content digest, and dependencies. |

`Agent` means listed and loadable through the harness skill mechanism.
`UserOnly` means the user can explicitly request it, while the agent cannot
discover/invoke it autonomously where the harness supports that distinction.
`Hidden` means the bytes can exist in the workspace, but the skill has no
catalog entry, completion entry, registered skill command, or name-based load
route in this launch. A hidden file is not made visible by a dependency: a
deployment with a visible-to-hidden dependency fails selection or explicitly
changes that dependency's visibility before launch. It does not auto-promote it.

Hiding a skill is a context-selection boundary, not filesystem secrecy.
Ordinary file access may still read it; that does not make it a registered
skill or promote its authority. Replacing a system prompt does not by itself
change skill discovery. A known name must not bypass the launch's hidden-skill
filter.

### Provisioning transaction

1. Flow selects the aspect, layer, harness, and requested model, then asks
   Curriculum for a versioned selection. Model defaults/quota policy belong to
   Flow, not primary's repository layout.
2. Curriculum combines the pinned bundle with the selected overlay, resolves
   dependencies, validates origin and visibility, and renders the selected
   harness projection. It may keep non-exposed content in the off-discovery
   store.
3. Flow validates the actual discovery surface, including parent directories,
   user-level skills, installed plugins, and managed configuration. The
   generated receipt records the exact selection and mechanisms used.
4. Flow launches the harness in the shared primary directory with that
   immutable selection. An unsupported visibility requirement is reported as
   an unsupported launch, not treated as enforced by instructional prose.
5. A changed selection provisions a new launch generation. Active flows retain
   their existing generation; disposal waits until its consumers have ended.

The existing file-based deployer is an implementation starting point. This POC
does not claim that the Curriculum Nexus handshake, manifest fields, or launch
adapter already exist.

## 4. Harness mechanisms and limits

This section distinguishes documented/upstream mechanisms from a tested local
launch. The harness investigation read current documentation and source; it
did not run four model sessions to prove catalog behavior. The acceptance
checks in section 9 are required before deployment. A file outside every root,
explicit path, and provider selected for the launch stays outside its
registered skill interface. Invocation preferences alone are not an adequate
implementation of `Hidden`.

### Claude Code

Keep hidden files in `bootstrap/skills/` or `.primary/content/`, outside
`.claude/skills`, enabled plugin skill roots, and explicitly added skill roots.
Project `.claude/skills` is shared by every flow in this working directory.
Expose a role bundle with a session-selected plugin via `--plugin-dir`, with
only eligible skills in that plugin. Plugin skills are namespaced; record the
canonical-ID-to-plugin-name mapping in the receipt. Audit inherited and
user-level skills as well as the project directory.

`disable-model-invocation: true` implements user-invoked behavior; the user can
still invoke the skill. `user-invocable: false` alone removes the user menu
entry while leaving model invocation possible. Neither alone means hidden.
Current Claude documentation additionally describes `skillOverrides` with
`off` for disabling both paths. Prefer omission from discovery for hidden
bundle content, and use supported overrides to suppress inherited entries
when needed. These overrides do not apply to plugin skills; plugin management
must select or disable those plugins. A session plugin adds a selected bundle;
it does not remove other plugins or inherited skills automatically. These distinctions are documented
in [Claude's skills reference](https://code.claude.com/docs/en/skills) and
[CLI reference](https://code.claude.com/docs/en/cli-reference).

Native Claude supports selection at the root-session launch. A different
catalog for an arbitrary built-in subagent is not established by this POC.
Launch that flow separately with its own selection or add and prove an adapter;
do not infer isolation from an agent role name or a custom system prompt.

### Codex

Keep hidden files outside `.agents/skills` and the enabled user, admin, system,
and plugin discovery roots. For already discovered skills, `[[skills.config]]`
with an absolute `path` and `enabled = false` disables the skill. Generate
flow-specific rules through supported user/session configuration, never by
rewriting a shared project configuration during a launch.

`agents/openai.yaml` with `policy.allow_implicit_invocation: false` only selects
explicit invocation; it does not make a skill unavailable to `$skill` requests.
Therefore the existing `user-only` projection cannot implement `Hidden`.
See [Codex skills](https://developers.openai.com/codex/skills) and the
[configuration reference](https://developers.openai.com/codex/config-reference).

The investigation observed local `codex-cli 0.153.4`: a prompt-input probe
omitted user-only `main-flow` from the catalog while listing ordinary `subflow`.
The debug probe did not establish explicit `$main-flow` loading. Explicit
invocation above is the documented/upstream contract, not a completed local
end-to-end test. That local behavior needs its own acceptance check.

At the pinned upstream revision, even a structured skill-path request resolves
only against the loaded skill set; it cannot load an off-discovery skill.
Ordinary file reads remain possible and provide no skill-interface injection.
For content that an enabled root/plugin does discover, disabled-path rules
also block structured and `$` selection. This design uses documented user or
session configuration for that filtering; enforcement through project
`.codex/config.toml` or a role's agent TOML has not been established for the
shipped runtime and is not relied on. A disable rule also does not add an
arbitrary off-discovery directory as a skill root.
Codex plugin support is a possible additive route, but this POC has not
validated a supported per-launch plugin-selection command for the installed
runtime. Until that route or a Flow/Codex adapter is proved, native Codex can
hide off-discovery files and filter known discovered files; it cannot be
claimed to provide this design's complete role-local additive catalog.
The fallback is an explicitly supported common-only catalog or an unsupported
launch result when the requested role requires additional skills.

### Pi

An explicitly requested Pi launch can use `--no-skills` plus repeated
`--skill <selected-path>` arguments. This suppresses ordinary discovery and
adds only the selected files/directories. Include common skills explicitly as
well. Point each argument at the selected projection, never at the content
store containing all roles. Hidden files stay on disk outside those selections.

Pi's `disable-model-invocation: true` suppresses automatic/model discovery while
leaving `/skill:name` invocation available; it is a user-only mechanism.
Packages and extensions must also be audited for resource loading. A forked
subagent extension with its own loader is not evidence of core Pi behavior.
The implementation must pin and test the actual Pi distribution it launches.
Document this path for completeness; the older psyche record's Pi retirement
direction is not reversed by this POC.
Upstream [Pi's skill documentation](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md)
and `packages/coding-agent/src/core/resource-loader.ts:468–473` establish the
explicit-path behavior. Its loader recursively scans a selected directory and
also accepts a Markdown file; do not pass a directory containing other roles.

### DeepSeek Harness (`dsh`)

The inspected dsh implementation discovers project `.dsh/skills` and
`.agents/skills`, home roots, and configured custom directories. Its registry
also supports scoped skill providers. Keep the content store outside those
roots; a Flow adapter should register the selected projection in that flow's
agent/preset scope. A global `customSkillDirs` union is insufficient when
several flows share one dsh process and configuration.

dsh separates model invocation from user invocation. Both must be disabled for
a registered hidden skill: `disable-model-invocation: true` and
`user-invocable: false`. The ordinary skill tool rejects model invocation in
that state and the user handler rejects user invocation. Even then trusted plugin code can access the
registry. Prefer leaving hidden skills unregistered in the flow's scope.
Plugin authors can defeat a visibility boundary by exposing a broad lookup
tool, so the adapter must filter both listing and invocation, including
explicit names. This POC establishes an upstream extension mechanism, not an
already deployed Flow-to-dsh adapter. Without that adapter or a verified
isolated selection, per-flow catalogs in a shared dsh host are unsupported.
See the upstream [skills subsystem](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md).

### Parent instructions and the current deployer

Claude and Codex parent entry-file traversal, and dsh's loading of both
`AGENTS.md` and `CLAUDE.md`, must be accounted for separately from skill
discovery. Root entry files contain only the common bootstrap. Moving an
awareness file into a parent instruction file makes it common context; it does
not make it a selectively loadable skill. Pi's selected launch must likewise
be checked for inherited instructions and extension-provided context.

The inspected `curriculum-deploy` revision
`37128c6d005425af58af0f609567c9759b850c2b` renders every authored skill into
both `.agents/skills` and `.claude/skills` (`src/runtime.rs:271–327`), with
tests asserting output count equals source count (`tests/runtime.rs:37–54`).
Its Claude `user-only` rendering uses `disable-model-invocation`; Codex uses
`allow_implicit_invocation: false`. Those are existing mechanisms. Manifest
selection, a hidden-content store, and immutable per-flow projections are
implementation changes required by this specification, not a description of
today's generator.

## 5. Documentation changes to author in Curriculum

These are sections to add during implementation, under the `Curriculum skills`
variable. This POC changes no skill source and regenerates no harness tree.
Harness facts live in each harness skill; the workspace owns bundle names and
setup values. Curriculum sources express intended skill visibility; the
deployer/Flow runtime owns its schema, validation, rendering, and receipts.

| Authored source | Sections to add and their exact subject |
| --- | --- |
| `claude-harness.md` | **Skill discovery and workspace overlays** — roots, parent context, session plugins and plugin namespaces. **Skill visibility** — `disable-model-invocation`, `user-invocable`, supported overrides, and hidden off-discovery files. **Concurrent flow selections** — root-session scope and subagent limitation. |
| `codex-harness.md` | **Skill discovery and workspace overlays** — project/user/admin/plugin roots. **Skill visibility** — implicit-invocation policy versus disabled paths; user/session configuration layers. **Concurrent flow selections** — validated additive route or explicit adapter requirement; project/agent config limitation. |
| `pi-harness.md` (new, if retained for supported launches) | **Skill discovery and explicit paths** — `--no-skills`, repeated `--skill`, package/extension roots. **Skill visibility** — menu/model distinction and hidden omission. **Support status** — retirement direction and the exact supported distribution. |
| `deepseek-harness.md` | **Skill discovery and scoped providers** — local roots, custom directories, host versus agent scope. **Skill visibility** — model/user axes and trusted registry access. **Concurrent flow selections** — the Flow adapter's registration and invocation filtering. |
| `skill-designing.md` | Replace the current **Skill types** mapping with the three-state visibility contract, with each harness's limitations referenced rather than restated. |
| The provisioning/Flow discipline and deployer/Flow schema | **Primary bundle origin**, **Immutable launch selection**, and **Provisioning receipt** — reserved suffix, collision/dependency checks, source pins, and selection ownership. Runtime schema/assembly code remains outside Curriculum's pure data repository. |

The per-harness documentation must identify the tested version, how the
launcher selects its roots, which context layer receives skill contents, and
which claims are only conventions. It must say when a file read cannot provide
the skill-interface injection the workspace requested. That mismatch occurred
in this POC's runtime: it exposes filesystem skill loading but no callable
Skill tool. A deployment must not advertise a tool it does not provide.

## 6. Concrete inventory decisions

**Keep** means a file in the nine-file skeleton, sometimes rewritten or
regenerated. **Relocate** means its useful data or implementation survives
outside primary. **Drop** means absent from pre-v1 and left in the preserved
v0 archive; it is not a deletion instruction for this POC.

Two proposed data repositories give the migration an explicit destination
without pretending an unfinished Nexus is operational:

* `primary-records` holds the consolidated psyche corpus, provenance, and
  migrated workspace documents/inventory. It is a new migration data repo to
  provision later, not the existing `psyche` code repository.
* `flow-data` holds flow identity, transcript locators, live handoffs and work
  state outside primary, shared across layers. This follows the dedicated
  flow-data repository direction in `flows/e996e8/vision/flows.md`. New raw
  psyche records enter the shared psyche corpus with their flow ID; flow
  records link to them. A compatibility mount may aid a later migration but
  is not a tracked directory or permanent requirement of the skeleton.

The proposed variable `Primary archive` identifies a retained v0 snapshot and
history, including unmerged sources; it is outside the new clone. `Workspace
records`, `Psyche records`, and `Flow records` resolve the above data locations.
Future Psyche, Flow, and Orchestrate services replace the corresponding data
access paths only after their ingest/read contracts work. Their implementation
repositories do not receive production data as source files.

The `psyche` component's `ARCHITECTURE.md`, in its checkout under `Repository
root`, explicitly says record types, storage, runtime, and contracts are
undefined. Existing `spirit` is a legacy intent
service; existing `mind` is a work-state service. Neither is presumed to accept
the whole historical raw corpus. This design chooses data-repo destinations
now and leaves service activation to its implementation work.

### Required directory inventory

The measurement below was made by the inventory subflow at
2026-09-17 12:01:33 America/Mexico_City, from `jj` revision `066eb794e153`.
Bytes are tracked logical file content measured in the working tree, not disk
blocks, compressed Git size, or a guarantee that the live tree stayed still.

| Current path | Files / bytes | Decision and exact destination or treatment |
| --- | ---: | --- |
| `flows/` | 1,857 / 24,501,319 | **Relocate.** Raw `vision/`, `notion/`, and archived psyche text go to `primary-records/psyche/flows/<id>/…`. Flow metadata, logs, active reports, and transcript locators go to `flow-data/flows/<id>/…`. Preserve the complete unsplit original under the v0 archive and map every old path to its destination. |
| `Vision/` | 25 / 53,688 | **Relocate** unchanged to `primary-records/psyche/Vision/`; keep reviewed/distilled status and sources. |
| `vision-raw/` | 90 / 117,142 | **Relocate** unchanged to `primary-records/psyche/vision-raw/`; legacy status does not justify losing the words. |
| `Intent/` | 9 / 3,769 | **Relocate** unchanged to `primary-records/psyche/Intent/`; preserve the distinction from raw vision and agent interpretation. |
| `psyche-archive/` | 1 / 6,316 | **Relocate** to `primary-records/psyche/psyche-archive/` as legacy material. Also ingest psyche archives embedded in flow directories; the root folder is not the whole archive. |
| `reports/` | 710 / 11,136,489 | **Relocate** to `primary-records/workspace/reports/` as historical evidence. Accepted component facts subsequently belong in the component's architecture; future flow reports live in transcripts/service records. External repository symlink targets are inventoried, not recursively copied. |
| `agent-outputs/` | 1,003 / 150,061,580 | **Drop** from the new workspace; retain in v0 history/archive. Extract any sole-copy psyche quotation or active delivery before cutover. Bulk generated output is not a bootstrap dependency. |
| `handoffs/` | 12 / 60,536 | **Relocate** to `flow-data/legacy/handoffs/`; import open work into Flow's eventual state model without presenting closed handoffs as current. |
| `sessions/` | 8 / 54,386 | **Relocate** to `flow-data/legacy/sessions/`; retain session/flow identity mappings and transcript references. |
| `skills/` | 3 / 1,977 | **Drop** the old generated-role inventory from pre-v1. Its archive remains evidence. The new bundle manifest replaces the inventory function; canonical authored skill sources remain in Curriculum. |
| `tools/` | 20 / 111,809 | **Relocate** implementations to their component/tooling repositories: repository inventory tooling to the repository-data tool owner; transcript fan-out to Flow tooling. Until those transfers land, preserve exact source at `primary-records/workspace/tools/`. No executables ship in the skeleton. |
| `orchestrate/` | 4 / 42,621 | **Relocate** local registry/coordination records to `primary-records/workspace/orchestrate/` as migration evidence. Live locks/state belong to Orchestrate's service database. Code belongs to the separate `orchestrate` component. Historical lock projections are not reacquired as live locks. |
| `awareness/` | 13 / 24,648 | **Relocate** current text to `primary-records/workspace/awareness/`. Role instructions are re-authored in Curriculum with user-only visibility; evidence and accumulated understanding stay records. Do not inject all old awareness into common entry files. |
| `protocols/` | 7 / 188,056 | **Relocate** to `primary-records/workspace/protocols/`, including `repos-manifest.dotos` as the continuing repository-data inventory. Reusable agent instructions move to Curriculum; component contracts to their owners. Primary keeps only a locator, not another inventory copy. |
| `release-trains/` | 2 / 4,096 | **Drop** from pre-v1; historical release bookkeeping remains in the v0 archive. Live release state belongs to its component/release system. |
| `verified/` | 3 / 12,088 | **Drop** from pre-v1; retained witnesses remain historical v0 evidence, carrying their original scope and time. They do not become timeless assurances in bootstrap. |
| `.agents/` | 47 / 91,621 | **Drop** the tracked generated tree; regenerate only the common/selected projection from Curriculum under the new selection rules. |
| `.claude/` | 50 / 93,111 | **Drop** generated files from tracked pre-v1. Preserve nested worktree-only records before retiring the old tree; its runtime data is much larger than these tracked bytes. Regenerate selected Claude output. |
| `.codex/` | 9 / 3,472 | **Drop** tracked generated role files; use supported per-launch configuration and selected projections. |
| `.pi/` | 10 / 92,542 | **Drop** tracked generated role files and continuation cache from pre-v1. Regenerate only for an explicitly supported Pi launch. |

### Every other top-level item in the measured checkout

| Current item(s) | Decision |
| --- | --- |
| `AGENTS.md`, `CLAUDE.md` | **Keep**, regenerated as the common bootstrap described above. |
| `ARCHITECTURE.md`, `SKILL_VARIABLES.md`, `.gitignore` | **Keep**, with their reduced roles above. Preserve the originals in v0 history. |
| `NON_MANAGEMENT_AGENTS.md`, `NON_IDEAL_AGENTS.md` | **Relocate** useful rules/workarounds into the appropriate authored Curriculum sources, preserving originals at `primary-records/workspace/`. They are not extra permanent root instruction files. |
| `design/` | **Relocate** to `primary-records/workspace/design/`; accepted component designs move to their owning architecture during implementation. |
| `.beads/` | **Relocate** task/work state via the store's supported export into `flow-data/legacy/beads/`; preserve the old database snapshot separately. Beads' embedded database is not skeleton content. |
| `flake.nix`, `flake.lock` | **Relocate** provisioning/environment inputs and checks to the declarative runtime/deployment owner. Archive the old files. The bootstrap consumes a pinned receipt, not an additional primary-owned package/environment flake. |
| `CriomOS/` | **Relocate** any unique work to `The system`'s repository; retain the local snapshot until that transfer is proved. No system checkout inside the skeleton. |
| `firstmate-bridge/` | **Relocate** unique implementation/configuration to its bridge/tooling owner; keep the old tree in v0 archive until accounted for. Its `.local` runtime state follows its service, not primary. |
| `repos` | **Drop** the convenience symlink. It points to `Repository root`'s owner directory; the target repositories remain where they are. |
| `private-repos/` | **Relocate** each independent private checkout to the private repository owner/location. Preserve its visibility and unique work. Neither its content nor credentials are imported into a public records repo. |
| `.git/`, `.jj/` | **Drop** old VCS databases from new clones. Preserve one recoverable v0 archive and all distinct unmerged revisions first. New history has its own fresh VCS metadata. |
| `.lojix-bootstrap-primary-mjl6-converged-request`, `.lojix-bootstrap-primary-mjl6-final-request`, `.lojix-bootstrap-primary-mjl6-mainonly-request`, `.lojix-bootstrap-primary-mjl6.2ERN4o` | **Drop** these bootstrap request artifacts from pre-v1; retain their original paths in the v0 archive. |
| `.pi-subagents/`, `.playwright-mcp/` | **Drop** local harness/browser state from the skeleton; retain anything needed for an active session with its harness state owner. |
| `index.js`, `linux-7.1.8/`, `librust_out.rmeta` | **Drop** vendored/build/incident artifacts from pre-v1; preserve v0 evidence. Any live dependency must first be packaged in its actual owner. |
| `error.log`, `results.txt`, `spiritbackup.nota` | **Drop** from pre-v1 after archiving. Treat `spiritbackup.nota` as potentially unique psyche/intent evidence during extraction, not disposable output. |
| `primary.code-workspace` | **Drop** from the mandatory bootstrap; user editor configuration belongs in the user environment. |
| Literal `.../` directory | **Drop** the abandoned zero-byte artifacts from pre-v1; preserve their original path inventory. |

At measurement there were 51 top-level entries: 35 directories, 15 regular
files, and one symlink. This POC then adds `PRIMARY-SKELETON.md` as a v0 design
artifact. Its accepted specification becomes pre-v1 `ARCHITECTURE.md`; its
original evidence remains in the records/archive. During review, a peer added
`PRIMARY-SKELETON-INVENTORY.md` (another v0 design/inventory artifact, preserved
with the workspace documents) and `tools/flow-cli-poc/` (covered by the tool
relocation decision). The root count consequently reached 53. Later peer
additions require inventory deltas before an actual migration; this table is
a dated decision, not a claim to have frozen the shared tree.

## 7. The psyche record survives the history cut

The complete canonical migration corpus is `primary-records/psyche/`, not a
selection of distilled summaries. It contains `Vision/`, `Intent/`, legacy
`vision-raw/`, `psyche-archive/`, and every flow's raw vision/notion/archive
records under their original logical paths. The proposed `Psyche records`
variable exposes it to every layer/flow. All flows receive the same readable
corpus or a query/export service covering it; local skills decide what a flow
loads, not whether it can retrieve another flow's vision.

Preserve exact bytes, original speaker attribution, typed versus STT status,
timestamps/timezones, flow and session identifiers, transcript locators and
record positions, source checkout/revision/path, and content hashes. Keep
agent-written context separate from quoted words. Preserve raw source and
distillation as separate records with provenance links. Record alternate
versions and explicit supersession; neither deduplication nor migration
silently rewrites the psyche's words. An agent's interpretation of an entry
does not become a new psyche ruling.

Unmerged worktrees are first-class migration inputs. In particular, copy and
verify the specified `9993b5` source from its actual worktree, even if no main
commit contains it. Store its original path and revision provenance. Enumerate
other worktrees and clones for unique records and dirty files before any
cleanup. Missing records block retirement of that source; merging code alone
does not establish corpus completeness.

Transcript-only words also survive. Inventory native harness transcripts
outside primary and provide stable transcript locators backed by preserved
records; do not assume the small `sessions/` directory contains them. Original
transcripts may stay in the transcript store, with verified retrieval and
record links in `flow-data`. Corpus export must include raw psyche extracts
and allow retrieval of their original context. A broken link into a deleted
home cache is not preservation.

The migration produces an old-path-to-record mapping and a per-source content
manifest. Two equal files may share stored bytes while retaining both origins.
Readback must resolve `9993b5/primarySkeleton`, retrieve all raw vision for an
arbitrary flow, export the full corpus, and find transcript-only statements.
These checks must work from primary, secondary, and tertiary against the same
shared record location. Distillation may continue after cutover; it is not a
prerequisite for retrieval.

The data repositories and archive retain the source access boundaries. This
specification creates or publishes neither. Rewriting primary's history later
requires completed export/readback and preserved rollback material; "v0
history left behind" does not mean discarding the only copy of a person's words.

## 8. Disk arithmetic and per-clone cost

The motivating report was **45 clones / approximately 11 GB**, with `/home`
**322G free of 916G**. Those are historical observations supplied with the
request. The inventory subflow's fresh `df` reading happened to show the same
322G available of 916G, with 548G used; reserved space and rounding mean those
displayed columns need not sum. This POC reclaimed no space.

The historical mean is `11 GB / 45 = 0.244 GB`, about **244 MB per clone**
using decimal units. If the original “11 GB” meant 11 GiB, the mean is about
**250 MiB per clone**. Neither figure is an exact measurement of today's shared
checkout, and a Git worktree, a full clone, and a JJ workspace need not have
equal storage cost.

### Measurements of today's checkout

| Surface | Measured value |
| --- | ---: |
| Tracked logical content | 3,982 files; 203,631,379 bytes = 194.20 MiB |
| Full local checkout, allocated | Approximately 2.2 GiB |
| Full local checkout, apparent | Approximately 1.7 GiB |
| `.git` allocated | 541,814,784 bytes = 516.71 MiB |
| `.jj` allocated | 1,012,002,816 bytes = 965.12 MiB |
| `.beads` allocated | 288,481,280 bytes = 275.12 MiB |
| `.claude` allocated, including its nested worktree | 218,374,144 bytes = 208.26 MiB |
| Tracked output across `.agents/.claude/.codex/.pi` | 116 files; 280,746 bytes = 274.17 KiB |

The generated skill payload is small; the nested runtime/worktree data is not.
Deleting tracked directories alone would leave their blobs in Git/JJ history.
The later new-history operation and retirement of duplicate VCS stores account
for that separate cost. External record storage still consumes disk once;
relocation is not free storage and is not itself a saving.

Measurements used `jj file list --ignore-working-copy -r @` plus file sizes,
`du -sx` and `du --apparent-size -sx` without following symlinks, and `df -hP`.
This is a live-tree sample; the revision labels the inventory, not an immutable
filesystem image. One later variable-file update changed the small root
sample. Exact archive accounting must use a frozen source manifest at cutover.

### Budget for the proposed skeleton

The nine target files have not been rendered or cloned. Their cost is a
specified budget, not a claimed benchmark:

| Target file(s) | Logical-content ceiling |
| --- | ---: |
| `ARCHITECTURE.md` | 64 KiB |
| `README.md`, `AGENTS.md`, `CLAUDE.md`, `SKILL_VARIABLES.md`, `.gitignore` | 4 KiB each = 20 KiB |
| `bootstrap/manifest.datom` | 8 KiB |
| Two bundled `SKILL.md` snapshots | 16 KiB each = 32 KiB |
| Total | **124 KiB**, within a **128 KiB** tracked-payload budget |

For scale, today's existing candidate root text (`ARCHITECTURE.md`,
`AGENTS.md`, `CLAUDE.md`, `SKILL_VARIABLES.md`, `.gitignore`; no README exists)
totals 35,441 bytes in the follow-up sample. That excludes the proposed
manifest and two skill snapshots, so it is a comparison, not a build result.

Set an acceptance ceiling of **1 MiB allocated per fresh unprovisioned clone**,
including the nine-file checkout and its fresh VCS metadata. A JJ checkout must
be measured as JJ, not substituted with a smaller Git-only figure. Allow
**2 MiB additional allocated space** for the selected initial overlay and its
launch projection, giving a **3 MiB provisioned-clone budget**. Those ceilings
must be measured on the deployed filesystem and adjusted explicitly if a
required harness cannot meet them; growing caches or retaining old generations
is not concealed inside the bootstrap estimate.

| Scenario | 1 clone/workspace | 45 copies, for comparison only |
| --- | ---: | ---: |
| Tracked skeleton payload ceiling | 128 KiB | 5.625 MiB |
| Fresh skeleton with VCS, acceptance budget | 1 MiB | 45 MiB |
| Initial provisioned skeleton, acceptance budget | 3 MiB | 135 MiB |
| Historical baseline mean | About 244 MB, or 250 MiB if binary | Approximately 11 GB as reported |

Under the conservative binary reading, 45 provisioned copies at budget would
be 135 MiB instead of 11,264 MiB: **98.8% less clone storage**. The intended
operating shape is one shared checkout, not 45 smaller clones. With concurrent
launches its storage is `one skeleton + shared content cache + sum of active
launch projections`; transcripts, data repos, archive, and service databases
are separate measured costs. These are projections of avoided duplication,
not a promise to recover that amount of `/home` space through this POC.

## 9. Implementation gates and POC validation

The later implementation has a defined order:

1. Provision the external data/archival destinations with their source access
   boundaries. Inventory every clone/worktree and external transcript store;
   preserve all unique records, dirty work, and unmerged revisions.
2. Produce content manifests and old-path locators; prove corpus and transcript
   readback across layers. Import live state through service APIs or supported
   exports, never by writing directly into a Nexus database.
3. Add the two authored bootstrap sources and the selection/visibility schema
   in their owners. Implement the deployer and Flow harness adapters, including
   source pins and Nix reseed provenance. Rebuild managed outputs from source.
4. Render the nine-file candidate outside any destructive operation, measure
   it with fresh Git/JJ metadata and overlays, and validate the contract below.
5. Only then perform the separately authorized history cut and change launch
   configuration. All primary launches point at the one shared main workspace.
   Retire old copies only after their unique content and rollback value are
   accounted for. This step is outside this POC.

Acceptance checks for that implementation are behavioral:

* A clean checkout has exactly the declared tracked files; provisioning adds
  no tracked diff. It resolves every named variable to a real readable service
  or location and reproduces the same selection from pinned inputs.
* In each supported harness, an ordinary skill is listed/loadable, a user-only
  skill follows that harness's documented invocation rule, and a hidden skill
  remains on disk but is absent from listing, completion, and name/path-based
  skill loading. Test explicit hidden-name attempts as well as discovery.
* Two concurrent flows in the same working directory receive distinct role
  selections without changing each other's catalog. Test parent directories,
  user plugins/skills, package roots, cached catalogs, reloads, and subagent
  inheritance. Unsupported adapters fail before starting a misconfigured flow.
* Reserved-suffix collisions, unknown visibility states, and dependencies that
  would expose hidden content fail provisioning with an actionable error.
  Explicit launch arguments such as Pi's `--skill` cannot select a manifest-hidden
  path: the launcher validates those arguments before invoking the harness.
* Raw words in `9993b5` and other unmerged sources, legacy vision, distilled
  records, and transcript-only entries can be retrieved with their original
  provenance after the old paths are unavailable. Corpus completeness is
  established by source manifests, not by counting files on main alone.
* Measure apparent and allocated storage, VCS metadata, active overlay bytes,
  shared data, and retained archive separately. Report measured cost against
  the budgets above before any cleanup is proposed.

For this documentation POC, validation consists of checking every required
inventory entry, every observed top-level item, all four harnesses, the source
references, and the arithmetic. No runtime migration is reported as tested.
This is a docs-only change, so it does not bump a package version.

### Evidence provenance

The main flow read the requested root declarations, skill variables,
`Vision/highLevelView.md`, both earlier workspace/harness records, and the
thirteen named `9993b5` records at their actual worktree location. The inventory
subflow measured the shared tree and searched `Vision/`, `vision-raw/`, and
per-flow vision; its additional witnesses include
`flows/15b67974/vision/psycheLogStructure.md`,
`flows/fd0f97/vision/flowLifecycle.md`, and
`flows/e996e8/vision/flows.md`.

The harness subflow reported source inspection at these upstream revisions:

| Source | Revision and relevant source areas |
| --- | --- |
| `curriculum-deploy` | `37128c6d005425af58af0f609567c9759b850c2b`; `src/runtime.rs`, `tests/runtime.rs` |
| `openai/codex` | `3d3ae4965ab370217e871b3a7f0d15589557ee4b`; `codex-rs/skills/src/selection.rs` and `model.rs`; distinct from local CLI 0.153.4 |
| `badlogic/pi-mono` | `781139411232411196de9fcc9f8823229c9ae084`; `packages/coding-agent/src/cli/args.ts`, `src/main.ts`, `src/core/resource-loader.ts`, `src/core/skills.ts` |
| `deepseek-ai/deepseek-harness` | `ddefc45fbc7f8e46dd73185e68295696d1297887`; `packages/skill/skill-filesystem/src/index.ts:1000–1009`, the skill tool/user handlers, and subsystem documentation |

Claude claims above are current official-documentation claims, not private
Claude implementation inspection. The harness subflow also checked the
`Reference skill collections`: Superpowers' flat skill namespace and
user-only slash-command precedent, and Anthropic's skill collection. Neither
established an origin suffix; `-primary` is this specification's choice.

The entry-file sample and inventory are dated observations; external APIs,
versions, and service contracts require revalidation at implementation. All
unbuilt destinations, budgets, and launch adapters are explicitly proposed.
