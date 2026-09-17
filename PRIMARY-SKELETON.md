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
    manifest.dotos
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
| `bootstrap/manifest.dotos` | The bundle inventory and provenance: bundle revision, Curriculum seed revision, deployer revision, source identities, output digests, and each bundled skill's visibility. This is proposed deployment data, not a new hand-written parser or a currently supported deploy request. Its concrete type belongs to Curriculum's schema. |
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
    receipt.dotos
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
`NixBuilder`, `Reference skill collections`, `Repository root`, `Standards`,
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
checks in section 9 are required before deployment. A file outside discovery
is the portable way to keep a skill hidden. Invocation preferences alone are
not an adequate implementation of `Hidden`.

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
when needed. A session plugin adds a selected bundle; it does not remove other
plugins or inherited skills automatically. These distinctions are documented
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

The inspected upstream configuration rules accept skill-disable rules from
user and session-flag layers, not project configuration. Do not assume that
`.codex/config.toml` or a role's agent TOML can enforce the filter. A disable
rule also does not add an arbitrary off-discovery directory as a skill root.
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

### DeepSeek Harness (`dsh`)

The inspected dsh implementation discovers project `.dsh/skills` and
`.agents/skills`, home roots, and configured custom directories. Its registry
also supports scoped skill providers. Keep the content store outside those
roots; a Flow adapter should register the selected projection in that flow's
agent/preset scope. A global `customSkillDirs` union is insufficient when
several flows share one dsh process and configuration.

dsh separates model invocation from user invocation. Both must be disabled for
a registered hidden skill; even then trusted plugin code can access the
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
setup values, while Curriculum owns the common visibility definition.

| Authored source | Sections to add and their exact subject |
| --- | --- |
| `claude-harness.md` | **Skill discovery and workspace overlays** — roots, parent context, session plugins and plugin namespaces. **Skill visibility** — `disable-model-invocation`, `user-invocable`, supported overrides, and hidden off-discovery files. **Concurrent flow selections** — root-session scope and subagent limitation. |
| `codex-harness.md` | **Skill discovery and workspace overlays** — project/user/admin/plugin roots. **Skill visibility** — implicit-invocation policy versus disabled paths; user/session configuration layers. **Concurrent flow selections** — validated additive route or explicit adapter requirement; project/agent config limitation. |
| `pi-harness.md` (new, if retained for supported launches) | **Skill discovery and explicit paths** — `--no-skills`, repeated `--skill`, package/extension roots. **Skill visibility** — menu/model distinction and hidden omission. **Support status** — retirement direction and the exact supported distribution. |
| `deepseek-harness.md` | **Skill discovery and scoped providers** — local roots, custom directories, host versus agent scope. **Skill visibility** — model/user axes and trusted registry access. **Concurrent flow selections** — the Flow adapter's registration and invocation filtering. |
| `skill-designing.md` | Replace the current **Skill types** mapping with the three-state visibility contract, with each harness's limitations referenced rather than restated. |
| The provisioning/Flow discipline and Curriculum deployment schema | **Primary bundle origin**, **Immutable launch selection**, and **Provisioning receipt** — reserved suffix, collision/dependency checks, source pins, and selection ownership. |

The per-harness documentation must identify the tested version, how the
launcher selects its roots, which context layer receives skill contents, and
which claims are only conventions. It must say when a file read cannot provide
the skill-interface injection the workspace requested. That mismatch occurred
in this POC's runtime: it exposes filesystem skill loading but no callable
Skill tool. A deployment must not advertise a tool it does not provide.
