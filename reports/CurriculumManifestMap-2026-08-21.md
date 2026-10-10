# Curriculum Manifest Map

Ground map of the Curriculum manifest mechanism as it currently exists.
Observations, claims, and unknowns are kept separate throughout.

## 1. The manifests

Ten `.dotos` files live under `manifests/` in
`/git/github.com/LiGoldragon/Curriculum`.

### active-outputs.dotos

The primary manifest. Each record is a `Skill.{...}` with five positional
fields (`manifests/active-outputs.dotos:3-31`):

1. **output identifier** -- the skill's published name (e.g. `nexus`)
2. **module identifier** -- which source module supplies the skill's body
3. **category** -- one of `Architecture`, `Craft`, `Programming`, `Workflow`, `Meta`
4. **tier** -- one of `Apex`, `Keystroke`, `Topic`, `Mechanism`
5. **target surfaces** -- a list from `[AgentsSkill ClaudeSkill]`

Currently 29 `Skill.{...}` entries.

### module-dependencies.dotos

Maps every module identifier to its flat source path and kind
(`manifests/module-dependencies.dotos:1-31`). Each record:
`{module-id skills/<id>.md RuntimeSkill|RoleComposition}`.

31 entries total. Two are `RoleComposition` (`general-instructions`,
`codex-skill-loading`); the rest are `RuntimeSkill`.

### model-catalog.dotos

Enumerates known models with provider surface and accepted effort levels
(`manifests/model-catalog.dotos:1-10`). Nine entries across `Claude` and
`ChatGpt` providers.

### role-permissions.dotos

Two permission rows: `read` (Restricted, carries a body text and blocks
editing tools) and `write` (Unrestricted, empty body)
(`manifests/role-permissions.dotos:1-4`).

### role-depths.dotos

Four depth rows: `trivial`, `ordinary`, `demanding`, `critical`. Each
names a Claude model+effort and a ChatGpt model+effort
(`manifests/role-depths.dotos:1-6`).

### role-descriptions.dotos

Eight cells -- one per (permission, depth) pair -- each carrying a
one-sentence human description (`manifests/role-descriptions.dotos:1-10`).

### role-aliases.dotos

Three alias entries (`default`, `explorer`, `worker`) each mapping to a
permission, depth, description, and restricted target surfaces (`[CodexAgent]`)
(`manifests/role-aliases.dotos:1-5`).

### universal-role-modules.dotos

A list of module identifiers included in every generated role packet.
Currently `[general-instructions]`
(`manifests/universal-role-modules.dotos:3`).

### target-module-insertions.dotos

Per-surface module injection. Currently one entry: `general-instructions`
on `CodexAgent` gets `[codex-skill-loading]` inserted
(`manifests/target-module-insertions.dotos:4`).

### skill-module-compositions.dotos

Ordered modules appended after a skill's primary module. Currently empty
(`manifests/skill-module-compositions.dotos:2`).

### Every distinct decision the manifest currently makes

| Decision | Which manifest | Example |
|---|---|---|
| Whether a skill is active (emitted at all) | active-outputs | `nexus` present means it generates; `lojix` absent means it does not |
| Skill output identifier (published name) | active-outputs | first positional field `nexus` |
| Which source module a skill's body comes from | active-outputs + module-dependencies | `nexus` -> `skills/nexus.md` |
| Skill category | active-outputs | `Architecture` |
| Skill tier | active-outputs | `Topic` |
| Which harness surfaces a skill targets | active-outputs | `[AgentsSkill ClaudeSkill]` |
| Module kind (RuntimeSkill vs RoleComposition) | module-dependencies | `general-instructions` is `RoleComposition` |
| Module source path | module-dependencies | `skills/nexus.md` |
| Known models and their provider + effort levels | model-catalog | `claude-opus-4-6[1m]` is Claude, accepts Low/Medium/High/Xhigh |
| Permission axis names and bodies | role-permissions | `read` carries restriction text |
| Tool restriction per permission | role-permissions | `read` is `Restricted` |
| Depth axis names and model assignments | role-depths | `critical` maps to opus + terra |
| Depth-to-model-to-effort binding | role-depths | `demanding` -> opus/Medium, terra/High |
| Human description per (permission, depth) cell | role-descriptions | `write critical` -> "New design, or..." |
| Role aliases | role-aliases | `default` -> write/ordinary on CodexAgent |
| Universal role modules | universal-role-modules | `general-instructions` in every role packet |
| Per-surface module injection | target-module-insertions | `codex-skill-loading` injected for CodexAgent |
| Skill module composition ordering | skill-module-compositions | (currently empty) |

### What "identity and deployment selection" means concretely

Per `CLAUDE.md:12` and `NON_MANAGEMENT_AGENTS.md:12`: the manifests are
the only place that decides which skills exist as outputs and which
harness surfaces they deploy to. The authored `*.md` files are the content;
the manifests are the wiring.

## 2. The generator

### Location

A Rust binary in `/git/github.com/LiGoldragon/Curriculum`. Entry point:
`src/main.rs:6-9`. Core logic: `src/assembly.rs` (~2341 lines). Schema:
`src/schema/assembly.rs` (contract types). Supporting modules:
`src/markdown.rs`, `src/template.rs`, `src/workspace_path.rs`,
`src/trunk_guard.rs`, `src/error.rs`.

### Inputs

The generator takes exactly one DOTOS argument (inline or `.dotos` file
path) resolved by `triad_runtime::ComponentCommand`
(`src/assembly.rs:57-99`). The argument decodes to one of two operations:

- `Generate.{source_root workspace_root manifest_path mode}` -- mode is
  `Write` or `Check`
- `Visualize.{source_root workspace_root manifest_path}` -- read-only
  report

The two config files consumed from the Curriculum repo are:

- `skills-generate.dotos`:
  `Generate.{$SKILLS_SOURCE_ROOT $SKILLS_WORKSPACE_ROOT manifests/active-outputs.dotos Write}`
- `skills-check.dotos`:
  `Generate.{$SKILLS_SOURCE_ROOT $SKILLS_WORKSPACE_ROOT manifests/active-outputs.dotos Check}`

Environment variables `$SKILLS_SOURCE_ROOT` and `$SKILLS_WORKSPACE_ROOT`
are resolved at runtime (`src/assembly.rs:203-208`).

### How it consumes the manifest

`GenerationSource::read()` (`src/assembly.rs:228-293`) reads all ten
manifest files from the source root:

1. `active-outputs.dotos` (required)
2. `module-dependencies.dotos` (required, located relative to the manifest path)
3. `target-module-insertions.dotos` (optional)
4. `universal-role-modules.dotos` (optional)
5. `skill-module-compositions.dotos` (optional)
6. `model-catalog.dotos` (required)
7. `role-permissions.dotos` (required)
8. `role-depths.dotos` (required)
9. `role-descriptions.dotos` (required)
10. `role-aliases.dotos` (optional)

It constructs a `GenerationConfiguration` that validates the cross
product, resolves models, checks cycles, and builds job lists.

### Outputs

Generated trees land in the consumer workspace under four directories:

- `.agents/skills/<name>/SKILL.md` -- Codex/Pi skill surface
- `.claude/skills/<name>/SKILL.md` -- Claude Code skill surface
- `.claude/agents/<role>.md` -- Claude Code role packets (markdown frontmatter)
- `.codex/agents/<role>.toml` -- Codex role packets (TOML)
- `.pi/agents/<role>.md` -- Pi role packets (markdown frontmatter)
- `skills/generated-role-outputs.dotos` -- inventory of all role output paths

For the current repository manifests, this produces:
- 29 skills x 2 surfaces = 58 skill files
- (2 permissions x 4 depths) x 3 surfaces = 24 cross-product role files
- 3 aliases x 1 surface each = 3 alias role files
- 1 role output inventory
- Total: 86 generated files (the test at `tests/generation.rs:1366-1378`
  asserts >= 68 are checked for braces; the actual count is higher)

Additionally, for skills marked `user_only` in their frontmatter,
a companion `.agents/skills/<name>/agents/openai.yaml` is emitted
(`src/assembly.rs:1092-1119`).

### Write mode vs Check mode

Write mode (`src/assembly.rs:126-128`): prunes stale skill directories
(`.agents/skills`, `.claude/skills`), removes retired role outputs, then
writes all files.

Check mode: reads existing files and compares; returns `StaleOutput` error
on any mismatch.

### How a consumer workspace invokes regeneration

In `/home/li/primary/flake.nix:42-80`:

```
apps.generate-skills  -- calls the skill binary with Write mode
apps.check-skills     -- calls the skill binary with Check mode
```

The consumer flake's `checks.generated-skills-current` (`flake.nix:89-93`)
runs `check-skills` as a Nix flake check, ensuring generated outputs stay
current with the source.

The Curriculum repo is referenced as flake input
(`flake.nix:17`: `skills.url = "github:LiGoldragon/Curriculum"`).

### Guard: source checkout protection

The generator refuses to write into its own source checkout
(`src/assembly.rs:165-190`, `tests/generation.rs:53-72`).
A trunk-descendant guard also verifies the source checkout is on
or descended from trunk (`src/trunk_guard.rs`).

## 3. The registration check

### general-instructions assertion

`tests/generation.rs:344-353`:

```rust
fn general_instructions_is_registered_and_tenets_is_not_auto_injected() {
    assert!(
        include_str!("../manifests/universal-role-modules.dotos")
            .contains("[general-instructions]")
    );
    assert!(
        !include_str!("../manifests/universal-role-modules.dotos").contains("tenets"),
        "tenets is a loadable skill and must not be auto-injected into roles"
    );
}
```

This test asserts that the literal text `[general-instructions]` appears
in `universal-role-modules.dotos`. It is a text-level assertion on the
manifest file content, not a structural check.

### Sibling checks of the same form

`tests/generation.rs:44-49`: asserts the DOTOS in `skills-generate.dotos`
decodes as an `Operation::Generate`.

`tests/generation.rs:328-341`: asserts the `psyche-interraction` skill
generates and that a legacy continuation file does not exist.

`tests/generation.rs:1157-1211`: asserts the repository manifests produce
all eight permission-by-depth roles across three surfaces, and spot-checks
specific model and effort assignments for `read-trivial` and
`write-critical`.

`tests/generation.rs:249-276`: asserts that nested legacy module source
paths (e.g. `modules/example/full.md`) are rejected; only the flat
`skills/<id>.md` form is accepted.

## 4. Elaborate-phase leftovers

### Skills broken into modules

The module system itself remains: `module-dependencies.dotos` maps module
identifiers to source paths, and `skill-module-compositions.dotos` allows
appending extra modules after a skill's primary module. However:

- **`skill-module-compositions.dotos` is empty.** No skill currently uses
  multi-module composition.
- **`module-dependencies.dotos` redundantly re-states what the filesystem
  already declares.** Every `RuntimeSkill` entry is exactly
  `{<id> skills/<id>.md RuntimeSkill}` -- the generator enforces this
  with `require_flat_source_path()` (`src/assembly.rs:1588-1601`), which
  rejects any path that does not match `skills/<id>.md`.

### RoleComposition modules

Two modules are marked `RoleComposition` rather than `RuntimeSkill`:
`general-instructions` and `codex-skill-loading`. These are injected into
role packets via `universal-role-modules.dotos` and
`target-module-insertions.dotos` respectively. They cannot be emitted as
standalone skills (`src/assembly.rs:1603-1613`).

### Orphan skill source files

Two `.md` files exist under `skills/` but appear in neither
`module-dependencies.dotos` nor `active-outputs.dotos`:

- `skills/lojix.md` -- has no frontmatter at all; appears to be a
  free-form skill that predates the current generation system
- `skills/nix-input-upgrade.md` -- has frontmatter with `description`
  and `dependencies: [nix-workflow]`; was presumably once active

Neither is consumed by the generator. They are present only on disk.

### generated-role-outputs.dotos in the source tree

`skills/generated-role-outputs.dotos` exists in the Curriculum source
tree as well as being generated into the consumer workspace. This is the
inventory of role output paths. It is a generated artifact that lives
alongside the authored skill sources.

### design/SkillsRedesign directory

`design/SkillsRedesign/CoreSkillsRedesign-2026-07-28.md` exists in the
Curriculum repo. Unknown whether it is still referenced or consumed.

### Category and tier fields

Each `active-outputs.dotos` entry carries `SkillCategory` and `SkillTier`
fields. These are defined in the schema
(`src/schema/assembly.rs:222-234`) but no code in `src/assembly.rs`
consumes them for any generation decision. They are parsed and validated
but produce no output. Unknown: whether they are consumed elsewhere (e.g.
by visualization or an external tool).

## 5. The removal's decision surface

If the manifest were removed and generation ran over whatever skills are
present, each decision the manifest currently makes would need to come
from somewhere else.

| Decision | Current source | Would need to come from | Witnessed example |
|---|---|---|---|
| **Whether a skill is active** | Presence in `active-outputs.dotos` | Presence of `skills/<id>.md` on disk (directory convention) | `lojix.md` exists but is not in active-outputs, so is not generated; after removal, it would generate unless excluded by some other mechanism |
| **Skill output identifier** | First field of `active-outputs.dotos` entry | Derived from filename (`skills/<id>.md` -> `id`); already enforced by `require_flat_source_path()` | `nexus` output identifier matches `skills/nexus.md` filename stem |
| **Module source path** | `module-dependencies.dotos` | Eliminated; the generator already enforces `skills/<id>.md` form, so the path is the identifier | Every entry follows `{<id> skills/<id>.md ...}` |
| **Module kind (RuntimeSkill vs RoleComposition)** | `module-dependencies.dotos` | Per-skill frontmatter, file naming convention, or directory placement | `general-instructions` is `RoleComposition`; the two role-only modules would need to be distinguished from the 29 runtime skills somehow |
| **Skill category** | `active-outputs.dotos` field 3 | Per-skill frontmatter or eliminated | `nexus` is `Architecture`; currently unused by any generation logic |
| **Skill tier** | `active-outputs.dotos` field 4 | Per-skill frontmatter or eliminated | `nexus` is `Topic`; currently unused by any generation logic |
| **Target surfaces** | `active-outputs.dotos` field 5 | Per-skill frontmatter, default convention, or eliminated (all skills target all surfaces) | Every current skill targets `[AgentsSkill ClaudeSkill]` -- all use the same pair |
| **Skill module compositions** | `skill-module-compositions.dotos` | Per-skill frontmatter or eliminated | Currently empty; no skill uses it |
| **Model catalog** | `model-catalog.dotos` | Stays as a manifest or moves to a different config file; not per-skill | Nine models with provider and effort bindings |
| **Permission axis** | `role-permissions.dotos` | Stays as a manifest or moves to config | `read` (Restricted) and `write` (Unrestricted) |
| **Depth axis** | `role-depths.dotos` | Stays as a manifest or moves to config | Four depths with model bindings |
| **Role descriptions** | `role-descriptions.dotos` | Stays as a manifest or moves to config | Eight (permission, depth) -> description cells |
| **Role aliases** | `role-aliases.dotos` | Stays as a manifest or moves to config | Three Codex-only aliases |
| **Universal role modules** | `universal-role-modules.dotos` | Convention, config, or eliminated | `general-instructions` injected into every role |
| **Target module insertions** | `target-module-insertions.dotos` | Per-module frontmatter or config | `codex-skill-loading` injected on `CodexAgent` surface |

### Observations on the decision surface

The decisions fall into two groups:

**Per-skill decisions** (rows 1-8): These currently require the manifest
to name each skill individually. Of these, output identifier and module
source path are already fully determined by the filename convention. Skill
category, tier, and target surfaces are carried in the manifest but
unused or uniform. Module kind distinguishes two role-only modules from
29 runtime skills.

**System-wide decisions** (rows 9-15): These are not per-skill and
would not be affected by removing the per-skill manifest. They configure
the role generation cross product, model bindings, and module injection.

### Unknowns

- Whether `SkillCategory` and `SkillTier` are consumed by any tool
  outside the generator (visualization, external queries, the
  `skills-visualize.dotos` operation).
- Whether any consumer outside the generator reads `active-outputs.dotos`
  or `module-dependencies.dotos` directly.
- Whether the two orphan files (`lojix.md`, `nix-input-upgrade.md`) are
  intentionally retained or simply not yet removed.
- Whether the `design/SkillsRedesign/` directory is still referenced.
- How the successor `training` repo (named in `psyche/Vision/skillsRepository.md:47`)
  relates to this manifest removal -- whether removal happens in
  Curriculum or waits for the successor.
- Whether `generated-role-outputs.dotos` in the source tree is
  intentional or a leftover from an earlier generation scheme.
