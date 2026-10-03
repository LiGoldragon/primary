# Context modules: research before design

Research for the Psyche seat's design of context modules across the stack. No design is
proposed here. Marks: **[W]** witnessed (source read or behavior observed by this subflow),
**[D]** documented by a vendor or a repository's own docs (fetched, not run), **[I]** inferred.
Revisions read: Curriculum `a0f2bf23`, curriculum-deploy `fb171e3b`, flow `83df5605`;
Primary pins Curriculum `c99253ab` and curriculum-deploy `dc7f70ed` in `flake.nix`.

## 1. Curriculum today

**Where.** `SKILL_VARIABLES.md` names `Curriculum skills: /git/github.com/LiGoldragon/Curriculum/skills`.
The data root is `/git/github.com/LiGoldragon/Curriculum`; the generator is a separate repo,
`/git/github.com/LiGoldragon/curriculum-deploy` (Rust, types declared in ethos). [W]

**Canonical data** (Curriculum `ARCHITECTURE.md`): "a pure data repository. Its canonical surface
is 38 described skill sources and one complete Datom role record." Actual count: 69 `skills/*.md`
[W]; the "38" in README/ARCHITECTURE is stale [W]. `review/unapproved/` and `review/retired/`
hold out-of-tree skill drafts that are not deployed [W].

**Skill source.** One flat file `skills/<name>.md`; name = file stem; no `name:` field. [W]
Frontmatter fields in use across all 69 sources: `description` (69), `dependencies` (66),
`user-only` (4: `main-flow`, `design`, `realization`, `trial-contact-discipline`). [W]

```
---
description: A user starts the main flow that coordinates subflows and owns their shared flow lane.
user-only: true
dependencies: [vocabulary, edit-coordination, psyche-interraction, psyche]
---
```

`dependencies` is copied verbatim into every deployed SKILL.md and read by nothing: no reference in
curriculum-deploy or flow source [W]; it is not a Claude, Codex, or Agent Skills frontmatter field
[D]. So it is documentation, not mechanism [I].

**Targets.** The body is rendered once per target by a line-oriented templater
(`runtime.rs`, `SkillBodyRendering`). Directives must stand alone on a line:
`{% if claude %}`, `{% if codex %}`, `{% if pi %}`, `{% else %}`, `{% endif %}`, `{% raw %}`/`{% endraw %}`;
nesting allowed; unclosed/stray directives are errors. [W] Only `main-flow` (2) and
`skill-designing` (1) use them today [W].

**user-only.** Purely textual: for the Claude target the line `user-only: true` is rewritten to
`disable-model-invocation: true`; for Codex the line stays and a sidecar
`.agents/skills/<name>/agents/openai.yaml` = `policy:\n  allow_implicit_invocation: false\n` is
emitted. [W] (Deployed `.claude/skills/main-flow/SKILL.md` confirms the rewrite. [W])

**Outputs of `Generate.{ «curriculum» «workspace» }`** (`Deployment::outputs`): [W]
- `.claude/skills/<name>/SKILL.md` and `.agents/skills/<name>/SKILL.md` for every skill;
- no `.pi/skills` and no `.codex/skills` (Codex reads `.agents/skills`) [W];
- role packets (below), plus `skills/generated-role-outputs.datom`, the inventory used to delete
  stale role files on the next run;
- stale skill dirs are deleted when a `SKILL.md` exists whose name is absent from the source set.
`Check.{…}` byte-compares the same outputs. Primary exposes these as `nix run .#generate-skills`
and `.#check-skills` (`flake.nix`). [W]

**Manifests.** One: `roles.datom`. Ethos schema (`curriculum-deploy.ethos`): [W]

```
Roles.{ Vector<RoleModule> Vector<Model> Vector<RolePermission> Vector<RoleDepth>
        Vector<RoleDescription> Vector<RoleAlias> Vector<String> Vector<TargetInsertion> }
RoleModule.{ String String }                      ; identifier, body
RolePermission.{ String String Permission }       ; read|write, module text, Restricted|Unrestricted
RoleDepth.{ String ModelChoice ModelChoice }      ; trivial|ordinary|demanding -> Claude choice, ChatGpt choice
RoleDescription.{ String String String }          ; discipline, depth, description
RoleAlias.{ String String String String Vector<Surface> }  ; default/explorer/worker/tester/book
TargetInsertion.{ String Surface Vector<String> } ; after module X on surface S insert modules [...]
Surface.[ ClaudeAgent CodexAgent PiAgent ]
```

The live record has four role modules (`general-instructions`, `codex-skill-loading`, `spirit-role`,
`intent-role`), universal modules `[ general-instructions spirit-role intent-role ]`, and one
insertion (`codex-skill-loading` after `general-instructions` on CodexAgent). [W]

**Agent definitions** (`roles.rs`, `Roles::packets`): for each (discipline × depth) and each
surface, body = [permission text if Restricted] + universal modules + target insertions, joined
by blank lines; then: [W]
- Claude: `.claude/agents/<id>.md` frontmatter `name, description, model, effort`, body = modules;
  if Primary has `subagents/<id>.md` it is appended (today `book.md`, `book-reader.md`).
- Codex: `.codex/agents/<id>.toml` with `developer_instructions = "<modules>"`.
- Pi: `.pi/agents/<id>.md` with `model: 'openai-codex/<m>'`, `thinking`, and
  `disallowed_tools: 'edit, write'` when Restricted.
No packet carries a `skills:` list (Claude) or `skills.config` (Codex), although both harnesses
accept one (section 2). [W for absence; D for support]
This subflow's own system prompt is exactly the `read-ordinary` packet text [W, own context].

**Skill types.** Nothing in the generator knows a type: a skill is a name and a body. [W]
Types exist only as name prefixes and as rules in `skill-designing.md`: gold (no prefix, the
living's), `operation-`, `compensation-`, `trial-`; role skills ("carries an aspect's identity …
Mark role skills user-only"); `<skill>-rationale` companions. [W] `knowledge-` (4 sources) and
`vision-` (3) are used as prefixes but have no definition line in `skill-designing` [W]. Role
modules in `roles.datom` are a second, separate module notion with no prefix and no file [W].

**Extending to a (ModuleType, Name) → Location registry** [I]. The seams are:
1. `Deployment::read` enumerates `skills/*.md` from one root; a registry replaces that glob with
   typed entries, each resolving to a path (and later a repo/revision).
2. `Skill { name, source, body }` gains a type; output paths and the user-only/sidecar logic
   could then be chosen by type instead of by frontmatter line-matching.
3. `RoleModule.{ id body }` holds bodies inline; under a registry it becomes a module reference,
   so role bodies and skill bodies share one store.
4. Role packets gain a module selection per placement (definition body vs `skills:` preload).
5. `clean_previous_skills` deletes any unknown dir; several sources per type need namespacing
   or an inventory like the role one.
6. The CLI accepts exactly one inline Datom request, two paths; a registry adds a third input or
   lives inside the data root.

Drift noticed: Primary's working tree deletes `.claude/skills/subflow` and adds
`knowledge-codex`, while Curriculum HEAD still has `skills/subflow.md` [W]; the tree was likely
generated from another Curriculum state [I].

## 2. The harness side

### Claude Code

| Entry | Stratum | Reaches non-fork subagent? | Reaches fork? |
|---|---|---|---|
| `--system-prompt[-file]` (replace) / `--append-system-prompt[-file]` | top | No [W 5578cc/dea0ba, D] | Yes, fork shares system prompt [D]; untested [W gap] |
| Output style | top (layers over stock) | No [D] | Yes [D]; untested |
| CLAUDE.md / AGENTS.md as project instructions | middle (user message) | Yes, unless `omitClaudeMd` or Explore/Plan [W 5578cc, D] | Yes (copied conversation) [D] |
| First prompt (positional or typed) | middle | No | Yes [D] |
| Leading `/skill` commands in first prompt (≤5 stacked, one line) | middle | No | Yes | 
| SessionStart hook `additionalContext` / `initialUserMessage` (`-p`) | middle (system-reminder) | No (own SubagentStart) [D] |  |
| SubagentStart hook `additionalContext` | middle, subagent only | Yes, by hook [D] |  |
| UserPromptSubmit `additionalContext` | middle, beside prompt | No [D] |  |
| Skill loaded via Skill tool | middle, persists; re-attached after compaction (5k tok each, 25k total) [D] | No ("doesn't see … the skills you've already invoked") [D] | Yes |
| Skills listing (names+descriptions, ~1% of window, 1,536 chars/entry) | middle | Subagents can invoke any non-withheld skill [D, W own Skill tool] |  |
| Subagent definition body (`.claude/agents/*.md`) | top of the subagent ("receive only this system prompt plus basic environment details") [D, W own context] | — |  |
| Subagent `skills:` frontmatter | full skill content preloaded at subagent start [D] | — |  |
| Subagent `initialPrompt` | first user turn only when run as main via `--agent` [D] | — |  |
| Brief (Agent tool prompt) | middle | — |  |

Withheld skills (`disable-model-invocation`) cannot be loaded by the model or by subagents; they
enter only through a leading `/name` in the user prompt or a launcher (claude-harness skill). [W skill]

### Codex

| Entry | Stratum |
|---|---|
| Base instructions (`model_instructions_file` replaces; `instructions` key) | top (`instructions` field) |
| `developer_instructions` | middle, developer role, outranks user |
| AGENTS.md (Codex home, repo root → cwd) | middle, user role |
| Skills catalog (name, description, path; ≤2% of window / 8,000 chars) | in session instructions [D] |
| Skill input item `{name, path}` in a turn | expands file text ahead of the prompt [W codex-harness skill] |
| First turn text (`turn/start`) | middle, user role |
| Custom agent `.codex/agents/*.toml`: `name`, `description`, `developer_instructions` required; may set `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config` [D] | subagent's developer role |

Inheritance into Codex subagents: "`sandbox_mode`, `mcp_servers`, and `skills.config`, inherit from
the parent when the custom agent file omits them"; model fields in the file win [D]. A subagent
renders its own catalog and cannot see a withheld skill [W codex-harness skill]. Whether a
main-only bundle reaches a Codex subagent is not measured [W dea0ba]; Flow sends the bundle as
first-turn text, which native descendants "never receive" per Flow's README [D-repo].

### What Flow does today (flow README / UPGRADES, `83df5605`) [D-repo]

`LaunchProfile` carries `Vector<LaunchSource>` (path + sha256), `Vector<SkillName>`, aspect, power,
harness, model, effort, predecessor, remembered flows, Herdr session, `SystemPromptBundleFile`,
`InstructionPrompt`. Claude: a per-launch copy of the bundle (caller bytes + `Predecessor:`/
`Remembered:` lines) is passed as `--system-prompt-file`; the first prompt is one line ≤800 chars,
up to five `/skill` commands, then one sentence (read bundle, load further skills, goal, receipt);
longer is refused (`CompositionRefused`). Codex: stock base instructions kept; bundle text opens
the single first-turn text above `$name` lines, with typed skill inputs resolved via
`skills/list` and journaled path+hash. Skill bodies are never pasted.

### dea0ba's witnessed findings (`flows/dea0ba/reports/prompt-module-research.md`)

1. Witness: Claude Code 2.1.284, Haiku, harmless markers, one turn, no tools.
2. A marker in the main system prompt reached the main seat whether replaced or appended.
3. That marker was absent from `general-purpose` and `Explore` subagents.
4. `CLAUDE.md` reached `general-purpose`.
5. `CLAUDE.md` did not reach `Explore`.
6. An agent with `omitClaudeMd: true` did not receive `CLAUDE.md`.
7. These agree with Claude's public account (fork copies system prompt and conversation).
8. Untested: main-only marker in a fork; output-style marker in a subagent or fork (42265e only).
9. Codex: no public guarantee of subagent isolation for a main-only module; treat as delivery policy.
10. Proposed (not witnessed) `PromptModule.{ Name Class Audience Text Provenance }`, Class
    `[ Purpose Behavior Personality OperationalSafety ]`, Audience `[ MainFlow HarnessSubagent Both ]`.

## 3. The living's words

All quotes verbatim from `flows/*/vision/`; `Vision/` and `vision-raw/` hold nothing on these
topics (searched). Ellipses trim.

### Modules and registry

> "Essentially, the system that we have for skill is really just like a prompt system, so we can use these either in the system prompt or in the prompt, or just let the agent have these skills available to load. So these would be different kinds of context modules, let's say."
-- psyche, STT then pasted, 2026-10-03, `flows/edf227/vision/contextModules.md`

> "Every flow call, or the flow database, has a registry of where each context module is located. … the vector of structs that have the context type … That's another field: the name of it, and the third field would be the location of where it is, either just a local file path for now. Maybe later we can support Git repos and stuff like that. We pass a list of which type and name for the context we want to load at each layer in the system prompt and in the origin startup prompt. … the flow nexus just inserts those values in the right places. … We need to maintain this configuration in Flow that we have to update when we add a new skill … That would be the meta. We can make it the meta socket."
-- psyche, STT then pasted, 2026-10-03, same file

> "Actually, we need to avoid repetition. … It could be a vector with the variant, like vision, and each of the variants contains all of the names of the modules that it wants. Somewhere else in the database, those module names correspond with the path, so that's configured separately, right? … I want to see the anatomy of everything that we're designing."
-- psyche, typed book comment, 2026-10-03T19:02Z, same file

> "I don't see `role` as a kind here, and I don't like `kind` because it collides with our use for `kind`, which is more basic."
-- psyche, typed book comment, 2026-10-03T19:05Z, same file (logged there as "role is a module type too")

> "Yeah, that looks fairly reasonable for now." (on the meta Signal)
-- psyche, typed book comment, 2026-10-03T19:06Z, same file

> "I would like Fable to design the context module side of things, along with the entire stack. … a very extensive design for this system that can both populate the skills and the system prompt. It's a standard for now that Flow can use and that we'll also implement in curriculum, which we could possibly rename context or maybe keep it curriculum (because the word context is used a lot so I think it's better to keep it curriculum)."
-- psyche, typed, 2026-10-03, same file and `flows/5578cc/vision/curriculum.md`

> "Maybe we need to go and overhaul curriculum and have all kinds of different modules for things that become skills from vision. … if curriculum is a nexus, we can't have any data there because it's going to keep rebuilding it. We need curriculum data. It can just be given. It's like a manifest that gives it a bunch of paths with some file names, Markdown, and gives the type of each. … could be in the header and read by this curriculum system that sees the fields that it knows about and maybe ignores the others."
-- psyche, typed, 2026-09-17, `flows/108ab0/vision/operational-curriculumAsModuleSystem.md`

> "We can programmatically compose, essentially, a prompt for something simple to access now to easily compose agents."
-- psyche, typed, 2026-09-17, `flows/108ab0/vision/operational-programmaticPromptComposition.md`

> "We don't need some of these to be agent-accessible because they're just stuff that we load when we start a certain kind of agent. You can even decompose your sub-agent prompt building into these types of personality, behavior, or specialty-type skills."
-- psyche, typed, 2026-09-17, `flows/108ab0/vision/operational-skillTypes.md`

### System prompt and first prompt

> "We need way more configuration for the system prompt so that we'll have modules and then there are going to be different types. There could even be an overlap between what we call skills now and what these modules are … I would like to be able to program the main flow a certain way but not its subagents in its system prompt. … splitting them up into: - what this is - is this behavior? - is this personality? - is this operational safety?"
-- psyche, typed book comment, 2026-10-03T16:20Z, `flows/9fb0ad/vision/systemPrompt.md`

> "Also if we put all of our steady, well-distilled vision, intent, and spirit in the system prompt instead of in the prompt, then we have more room."
-- living, 2026-09-25, `flows/e51411/vision/systemPrompt.md`

> "… the parts that change per model, right? All categorized basically into data files, probably some kind of Markdown with Datom and Ethos syntax everywhere: specify data and then show data basically."
-- living, 2026-09-25, same file

> "… some of our skills are kind of intent in practice, like a spirit and behavior. Spirit is higher than intent … now we're moving into putting it directly in the system prompt."
-- psyche, typed, 2026-09-16, `flows/b49251/vision/systemPrompt.md`

> "The spirit and the intent are also part of the system prompt … you can make those not even accessible to the agent, you can make them sort of per-call optional skills … Those are like behavior modules, skills, and they are just usable through the prompt."
-- psyche, typed, 2026-09-16, `flows/48cff7/vision/skillPromotionAndLayering.md`

> "I want to replace claude and codex's system prompts with a version that doesnt incentivize the sort of behavior im constantly steering against."
-- 2026-08-23, `flows/2f6b1dc5/vision/systemPrompt.md`

### Briefs and subagent definitions

> "No, the main flow should not put anything in every brief. That's what subagent definitions are for. The subagent launch should require as few tokens as possible."
-- psyche, STT, 2026-10-03, `flows/edf227/vision/subflowBriefs.md`

> "I want specialized subagent roles that already have almost everything they need to know to do certain things and you just send them one or two lines, very extremely brief."
-- psyche, typed, 2026-10-03, `flows/41fa34/vision/subflows.md`

> "… adding a skill to dependencies, whether it's a dependency on that skill from another skill or from a subagent definition … For me subagents are a type of skill."
-- psyche, STT, 2026-10-01, `flows/fe945a/vision/skills.md`

### Skill types and Curriculum

> "… we're moving these skill variables into knowledge-type skills. I also want curriculum to support generating skills from more than one source for any type so people could: - write their own knowledge skills - in a plugin kind of way use other people's knowledge skills and some people's vision skills."
-- psyche, typed book comment, 2026-10-03T15:42, `flows/5578cc/vision/skills.md`

> "Let's make sure that all the skills refer to layers and there would be a skill that makes a correspondence of layers to models in the knowledge type skill."
-- psyche, typed book comment, 2026-10-03T15:41, same file

> "We're going to have different types. … - vision - operation - compensation - some other thing like memory or testing … The type is assigned to the repo. It's centrally controlled: which type comes from which repositories."
-- psyche, typed, 2026-09-24, `flows/26c50c/vision/curriculum.md`

> "role skills are what the awareness files become" / "all role skill will be non-flow usable (must be manually triggered in user prompt …)"
-- 2026-08-16, `flows/e4be1c4a/vision/skillTypes.md`

### Layers

> "Yeah let's make it four layers …"
-- psyche, typed book comment, 2026-10-03T15:39, `flows/5578cc/vision/layers.md`

> "… putting together good context for new flows with the right prompts and the right system prompt, and growing the vision."
-- psyche, typed, 2026-09-16, `flows/b49251/vision/layers.md`

**Tensions** [I]: the home of steady vision moved upward over time (prompt 09-09 → fat first
prompt 09-19 → system prompt 09-25 → subagent definitions 10-03). "Type assigned to the repo"
(09-24) versus "more than one source for any type" (10-03). `role` is both a skill kind
(08-16, skill-designing) and something the living found missing from the module-type enum (10-03).

## 4. Prior art (fetched)

**Agent Skills specification** (agentskills.io).
What: `SKILL.md` with required `name` (must match dir) and `description`, optional `license`, `compatibility`, `metadata`, `allowed-tools`; three-level progressive disclosure (metadata, body, resources).
Right for us: a cross-harness module unit with a load-on-demand placement already built in. Lacks: no type, no placement other than "loadable", no dependencies, no registry; `name` is required where our sources derive it.

**Claude Code subagents and plugins** (code.claude.com sub-agents, plugins-reference).
What: agent `.md` with `skills:` (full preload), `omitClaudeMd`, `initialPrompt`; plugin.json bundles skills/agents/hooks/output styles under a namespaced name, with `dependencies` between plugins.
Right: the `skills:` field is exactly "definition carries what every subflow must know", at zero brief cost; plugins show namespacing for multi-source modules. Lacks: Claude-only; no module types; placement is fixed per component kind.

**Codex custom agents and skills** (learn.chatgpt.com).
What: `.codex/agents/*.toml` with `developer_instructions` and `skills.config`; skills catalog ≤2% of window; `agents/openai.yaml` policy.
Right: a second placement target with a ranked developer role, so one module can land above user text. Lacks: no full-content skill preload equivalent to Claude's `skills:` documented; subagent isolation of main-only text undocumented.

**OpenAI Model Spec chain of command** (model-spec.openai.com, 2026-08-18).
What: Root > System > Developer > User > Guideline; quoted text and tool outputs carry "no authority by default".
Right: an authority ladder that maps onto our strata and can type a module's intended rank. Lacks: says nothing about how modules are stored, selected, or composed.

**Anthropic prompting best practices** (platform.claude.com).
What: role in the system prompt; XML tags to separate instructions, context, input; long documents at the top, query last.
Right: a placement rule (stable role/behavior up, task data down) and a delimiter convention for assembled bundles. Lacks: guidance, not a format; no module identity or provenance.

**DSPy signatures** (stanfordnlp/dspy docs source).
What: declarative typed input/output fields plus a docstring; adapters render them into prompts; modules compose and are compiled/optimized.
Right: separates what a module means from how a harness renders it, like our per-target rendering. Lacks: targets task I/O, not standing behavior; prompts are generated, not authored by the living.

**Priompt** (anysphere/priompt).
What: JSX prompt components with priorities and scopes; renderer drops the lowest priority to fit a token budget; `<isolate>` for cache stability.
Right: explicit budgeting and cache-aware composition, which the 800-char Claude line and listing budgets need. Lacks: priority-driven truncation conflicts with a module being binding; code, not data.

**POML** (microsoft/poml) and **AGENTS.md** (agents.md).
What: POML has semantic tags (`<role>`, `<task>`, `<example>`, `<document>`), templating and a CSS-like style layer; AGENTS.md is a nearest-file-wins instruction file read by 20+ tools.
Right: POML separates content from presentation per target; AGENTS.md is the most portable entry-file placement. Lacks: neither has typed module identity, selection by role, or a registry.

## 5. Open questions the design must answer

1. The name of the type axis, since `kind` is taken; and its variants (vision, knowledge, operation, compensation, trial, role, behavior/spirit/intent, rationale?).
2. Are role modules (`roles.datom`) and skills one module store or two?
3. Placements: which exist (system prompt, append, entry file, first prompt, loadable skill, subagent definition body, subagent `skills:` preload, Codex developer_instructions, hook additionalContext), and is placement chosen per launch, per module, or per type?
4. Who holds the registry of (type, name) → location: Flow's database over the meta socket, Curriculum data, or both with one source of truth?
5. Location forms: local path now; Git repo + revision later; how is revision pinned and hash-journaled (Flow already journals path + sha256)?
6. Several sources per type (own vs shared vision/knowledge): namespacing, precedence, conflicts.
7. Selection shape avoiding repetition: vector of per-type selections of names, as the living proposed; how roles and layers inherit selections.
8. Per-target rendering: keep `{% if %}` in bodies, or move target variance into separate modules?
9. user-only becomes what: a placement restriction ("never loadable") rather than a frontmatter line?
10. Does `dependencies` become mechanism (transitive load) or stay documentation?
11. Main-only text: system prompt holds it on Claude (witnessed); what holds it on Codex, and is a fork test needed first?
12. Budget limits: Claude first line ≤800 chars and ≤5 stacked commands; skills listing ~1%/2%; preload size; how a launch that overflows is refused.
13. Does Curriculum stay a generator of files (deploy) while Flow composes at launch, or does Flow read modules directly and Curriculum only validate?
14. Pi: no skills tree today; is it a target?
15. The permission module ("Do not edit files…") collides with delegated report writing (this report); does a module carry its exceptions, or does the brief?
16. Stale docs: Curriculum README/ARCHITECTURE count (38 vs 69) and the Primary tree vs Curriculum HEAD drift; resolve before the standard cites them.

## Sources

- `/home/li/primary/SKILL_VARIABLES.md`; `/home/li/primary/flake.nix` (lines 21-29, 85-115)
- `/git/github.com/LiGoldragon/Curriculum/{README.md,ARCHITECTURE.md,AGENTS.md,UPGRADES.md,roles.datom,skills/*.md}` at `a0f2bf23`
- `/git/github.com/LiGoldragon/curriculum-deploy/{README.md,ARCHITECTURE.md,curriculum-deploy.ethos,src/runtime.rs,src/roles.rs}` at `fb171e3b`
- `/git/github.com/LiGoldragon/flow/{README.md,UPGRADES.md}` at `83df5605`
- `/home/li/primary/.claude/skills/main-flow/SKILL.md`, `/home/li/primary/.claude/agents/read-ordinary.md`
- `/home/li/primary/flows/dea0ba/reports/prompt-module-research.md`
- `/home/li/primary/flows/5578cc/books/answers-on-flow-launch.md`
- Vision files quoted in section 3 (paths inline)
- Skills loaded through the skill interface: claude-harness, codex-harness, context-strata, skill-designing, flow-evidence
- https://code.claude.com/docs/en/sub-agents ; https://code.claude.com/docs/en/skills ; https://code.claude.com/docs/en/hooks ; https://code.claude.com/docs/en/plugins-reference
- https://learn.chatgpt.com/docs/agent-configuration/subagents ; https://learn.chatgpt.com/docs/build-skills
- https://agentskills.io/specification ; https://agents.md/
- https://model-spec.openai.com/2026-08-18.html
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- https://raw.githubusercontent.com/stanfordnlp/dspy/main/docs/docs/learn/programming/signatures.md
- https://github.com/anysphere/priompt ; https://github.com/microsoft/poml
- Provenance receipt: unavailable (no PROVENANCE handoff received; `FLOW_ID` unset in this subflow's environment).
