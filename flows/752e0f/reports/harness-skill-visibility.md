# Harness skill visibility: how a user-only skill is hidden and invoked

Scope: Claude Code 2.1.280 and OpenAI Codex CLI 0.153.4 as installed on this
host on 2026-09-24. Establishes, per harness, what hides a skill from the
model and what puts it into context anyway.

---

## Claude Code — how it works in reality

A skill directory carries frontmatter. Two fields govern who may invoke it.
`disable-model-invocation: true` withholds the skill from the model
altogether: the name does not appear in the available-skills listing the
harness writes into context, and the Skill tool refuses the name with an
error. `user-invocable: false` withholds it from the typed command list.
`paths` scopes a skill to a directory. The remaining frontmatter —
`allowed-tools`, `argument-hint`, `model`, `effort`, `context`, `agent`,
`background`, `hooks`, `shell`, `version`, `when-to-use` — shapes how the
skill runs, not who may reach it.

A skill the model cannot invoke still enters through the user's own input.
The harness parses the typed message before the model sees it: if the text,
after leading whitespace, begins with `/name`, the harness resolves that name
against its command table, expands the skill body, and replaces the user turn
with two records — one naming the command, one carrying everything typed
after the name as its arguments — followed by the expanded skill body as a
separate injected message. The expansion is the harness's own work; the model
receives the result, never the decision.

The command must lead the input. The parser reads a command only at the head
of the remaining text, then treats the rest as that command's arguments; up to
five commands may stack head-to-head, and the first text that is not a command
ends the parse. A `/name` on a later line of a pasted block is therefore
ordinary text, delivered verbatim. One block of startup text can still carry
the command, provided the command is its first token and the whole briefing is
its argument.

Two launcher-side paths avoid a typed turn. A SessionStart hook may return
`initialUserMessage` or `additionalContext`, either of which places text into
the new session's first turn. Or the launcher reads the skill file itself and
pastes its body into the first user prompt — what this repository's Claude
launcher does today, leading the prompt with the expanded body of every
startup-only skill and treating a missing block as a failed launch.

A subagent inherits the restriction and has no user. It cannot see a
model-hidden skill in its listing and cannot load it through the Skill tool.
A skill a subagent must carry is either not hidden, or written into the brief.

### Evidence

- Version: `claude --version` → `2.1.280 (Claude Code)`.
- Generated frontmatter, `/home/li/primary/.claude/skills/main-flow/SKILL.md`
  lines 2-4: `disable-model-invocation: true`. The same line is present in
  `field`, `refresh`, `realization`, `design`, `voice-psyche`; absent from
  `spirit`, `subflow`, `skill-designing`, `agent-harness-packaging`.
- Listing omission, witnessed first-person: this report's author is a subagent
  of the 752e0f main flow. Its available-skills listing contains
  `agent-harness-packaging`, `behavior`, `claude-harness`, `codex-harness`,
  `skill-designing`, `subflow`, `spirit` and 60 further names, and contains
  none of `main-flow`, `field`, `refresh`, `realization`, `design`,
  `voice-psyche` — exactly the six `disable-model-invocation: true` skills.
- Skill tool refusal, witnessed first-person: calling the Skill tool with
  `main-flow` returned `Skill main-flow cannot be used with Skill tool due to
  disable-model-invocation. Ask the user to run /main-flow themselves — it
  cannot be invoked via the Skill tool. Do not replicate this skill's workflow
  by other means — it is reserved for explicit user invocation.`
- Transcript record shape, this seat's own transcript
  `~/.claude/projects/-home-li-primary/752e0f7e-49ec-4110-b27b-6107e0eb6520.jsonl`
  line 200, a `user` record with `isMeta` unset:
  `<command-message>main-flow</command-message>\n<command-name>/main-flow</command-name>`
  Line 201 is a second `user` record with `isMeta: true` beginning
  `Base directory for this skill: /home/li/primary/.claude/skills/main-flow`
  followed by the skill body. The research subflow reports that record also
  carries `turnCompanion: true` and a `promptId` shared with the command
  record; this flow did not read those fields out of the transcript.
- Arguments record: across
  `~/.claude/projects/-home-li-primary/*.jsonl`, the same shape appears with a
  third element, e.g. `<command-message>behavior</command-message>\n<command-name>/behavior</command-name>\n<command-args>…</command-args>`,
  where `<command-args>` carries multi-paragraph typed text of several hundred
  words. So a slash command and a long block travel in one message.
- `user-invocable`'s effect on the model's listing is **unresolved**: this
  flow's bundle reading found the command parser terminating on
  `R.userInvocable===!1`, a typed-command concern, while this flow's Claude
  Code research subflow reported, from the published documentation, that the
  skill is hidden from the model as well. Neither reading was witnessed
  against a running session. Carried as unknown below.
- Frontmatter keys known to the installed build, by string occurrence in
  `/nix/store/wz475h72i242nf55ydn0zx7hfk9dh6jv-claude-code-2.1.280/bin/.claude-wrapped`:
  `disable-model-invocation` (18), `user-invocable` (39), `allowed-tools` (73),
  `argument-hint` (16); internal fields `disableModelInvocation` (55),
  `userInvocable` (65). The frontmatter reader in that bundle maps them:
  `…disableModelInvocation:Wkt(e["disable-model-invocation"]),userInvocable:y,
  hooks:j,executionContext:e.context==="fork"?"fork":void 0,agent:…,
  background:…,effort:B,shell:…` — the same object also carries `whenToUse`,
  `version`, `model`, `context`, `agent`, `background`, `effort`, `shell`.
- Command-position rule, same bundle, the command parser:
  ```
  var et=5;
  function _t(e,s,o,u){ … let r=[],p=e,g=s,k=!1;
    for(let S=0;;S++){ let U=p.trimStart();
      if(!U.startsWith("/"))break;
      if(S>=et){k=!0;break}
      let A=Fv(U); if(!A)break;
      … let R=Xs(A.commandName,o);
      if(!R||R.type!=="prompt"||R.context==="fork"||R.getContext!==void 0
         ||R.argsMayContainSlashCommands||R.userInvocable===!1||!Dc(R)||dH(R))break;
      if(p=A.args,g=L,u?.(R))continue; r.push(R) }
    return{stacked:r,trailingArgs:p,capped:k}}
  ```
  `p` starts as the whole input; each iteration requires the *remaining* text
  to start with `/` after `trimStart()`, and sets `p` to that command's
  arguments. Text that is not a leading command terminates the loop and
  becomes `trailingArgs`. `userInvocable===false` also terminates it.
- SessionStart hook output schema, same bundle:
  `u({hookEventName:R("SessionStart"),additionalContext:o().optional(),
  initialUserMessage:o().optional(),sessionTitle:o()…optional(),
  watchPaths:C(o())…optional(),reloadSkills:H()…optional()})`
  and the dispatcher `if(hr.initialUserMessage){…provided initialUserMessage
  (${hr.initialUserMessage.length} chars)…}`, `yield{additionalContexts:[dr]}`.
- Launcher pre-expansion in use today,
  `/home/li/primary/tools/claude-native-seat-refresh.py`:
  - lines 115-119 `expanded_skill` returns
    `f"Base directory for this skill: {file.parent}\n\n{file.read_text().rstrip()}"`
    read from `cwd/.claude/skills/<name>/SKILL.md`.
  - lines 122-128 `startup_skills` selects exactly the names matching
    `^disable-model-invocation:\s*true\s*$` (plus `main-flow`), ordering
    `main-flow` first.
  - line 668 `first_prompt` joins those blocks and the role brief into one
    string; line 700 rejects a launch whose first user prompt does not begin
    with the exact expanded `main-flow` block.
  No slash command is typed anywhere in that launcher.
- Paste wrapper: the same file, `accepted_user_text`, matches
  `\s*<pasted_content id="([^"]+)">\n(.*)\n</pasted_content id="…">\s*` around
  a first user prompt, so a sufficiently large startup block reaches the
  transcript inside a wrapper.

### Unknown — Claude Code

- Whether a leading `/name` survives the `<pasted_content …>` wrapper that a
  large startup block acquires: the parser rule above is read from the bundle,
  not exercised against a pasted block. **Live test pending with e51411**,
  which is running it on a throwaway pane; this flow did not run its own.
- Whether `initialUserMessage` from a SessionStart hook is submitted as a turn
  or only pre-filled into the input, and whether a `/name` inside it is
  expanded. Unknown.
- Whether `additionalContext` is truncated: the bundle carries a map
  `{additionalContext:8000,permissionDecisionReason:2000}` whose meaning
  (hard cap or logging threshold) was not established. Unknown.
- What `user-invocable: false` does to the model's available-skills listing.
  Unknown; see the note above.
- Whether `--append-system-prompt` text is scanned for commands. Not examined;
  it is a system-prompt flag and the command parser reads user input, so the
  expected answer is no, but it is unwitnessed. Unknown.

---

## OpenAI Codex CLI — how it works in reality

Codex renders a `## Skills` catalog into the session instructions: one entry
per discovered skill, each with a name, a description, and the location of its
`SKILL.md`. That catalog is the whole of what the model knows about the
available skills; a skill absent from it does not exist for the model. The
model is told to use a skill when the user names it or when the task matches
its description, and to read the `SKILL.md` itself before acting.

A skill is withheld by a sidecar file beside it. `agents/openai.yaml` next to
the skill's `SKILL.md`, carrying `policy: allow_implicit_invocation: false`,
keeps the entry out of the rendered catalog. Codex has no equivalent of a
frontmatter flag for this; any unrecognised frontmatter key is inert.

A withheld skill still reaches the model when the client puts it there. The
turn request carries an input array, and one of its item kinds is a skill:
`{type: "skill", name, path}`. An item of that kind expands into the turn as a
`<skill>` block containing the file's text, before the user's own text. That
is the launcher's channel — it names the skills by path at turn start, and the
model receives their bodies whether or not the catalog lists them.

A subagent gets the catalog its own session renders, so a withheld skill is
invisible to it too. Delegation does not carry a skill: the harness instructs
the main agent to read skill instructions itself and not to hand that reading
to a subagent.

### Evidence

- Version: `codex --version` → `codex-cli 0.153.4`.
- Catalog text, strings in
  `/nix/store/wdj0sc69r4n9is1idfb32vcx5739ijkh-codex-0.153.4/bin/.codex-wrapped`:
  `A skill is a set of instructions provided through a 'SKILL.md' source.
  Below is the list of skills that can be used. Each entry includes a name,
  description, and source locator.` and the section header `### Available
  skills`, rendered by `render_available_skills` (`ext/skills/src/render.rs`).
  Trigger rule, same bundle: `If the user names an available skill (with
  $SkillName or plain text) OR the task clearly matches an available skill's
  description, you must use that skill for that turn.` Section wrapper:
  `<skills_instructions></skills_instructions>`.
- Sidecar honoured by the installed binary: the strings `agents/openai`,
  `openai.yaml`, `allow_implicit_invocation`, `skills.agents`, and
  `struct SkillMetadataFile` with fields `description interface dependencies
  policy`, plus `struct Policy`, all occur in that binary.
- Sidecar on disk: `/home/li/primary/.agents/skills/main-flow/agents/openai.yaml`
  contains exactly `policy:\n  allow_implicit_invocation: false\n`; the same
  file exists for `design`, `field`, `realization`, `refresh`, `voice-psyche`,
  and for no other skill.
- Effect witnessed live. Command, run in `/home/li/primary`:
  `codex exec --skip-git-repo-check -c model_reasoning_effort=low -c
  sandbox_mode=read-only "Do not use tools. Answer from your context only. Is
  there a '## Skills' section in your instructions? If yes, list the NAMES
  only, comma separated, of every entry in it. Then state whether each of
  these names appears there: main-flow, refresh, field, design, realization,
  voice-psyche, subflow, behavior. Nothing else."`
  Session `01a0d4d3-ac83-7710-a34c-c007b74dabef`, model `gpt-6-astra`. It
  listed 97 entries, among them every non-user-only skill in
  `.agents/skills` (`behavior`, `subflow`, `claude-harness`, `codex-harness`,
  `skill-designing`, `spirit`, `testing-*`, …), and concluded:
  `main-flow: no, refresh: no, field: no, design: no, realization: no,
  voice-psyche: no, subflow: yes, behavior: yes`.
  Grade: the model's own report of its rendered instructions, a machine
  self-report, not an inspected request body. It is consistent with the
  sidecar's presence on exactly those six skills.
- Codex reads `.agents/skills`: the string table of the same binary lists the
  discovery roots `.mcp.json`, `.codex`, `.codex/config.toml`, `.codex/agents`,
  `.codex/hooks`, `.agents`, `.agents/skills`.
- Structured skill input at turn start, protocol schema generated from the
  installed binary by `codex app-server generate-json-schema -o <dir>`,
  `codex_app_server_protocol.v2.schemas.json`: `TurnStartParams` requires
  `input` (array of `UserInput`) and `threadId`; `UserInput` is a `oneOf`
  whose variants include
  `{"title":"SkillUserInput","properties":{"name":{"type":"string"},
  "path":{"type":"string"},"type":{"enum":["skill"]}},
  "required":["name","path","type"]}`
  alongside `TextUserInput`, `ImageUserInput`, `MentionUserInput` and others.
- Launcher use of that variant, `/home/li/primary/tools/native-seat-launch.mjs`:
  - line 136 `function structuredSkills(skills){ return skills.map(skill =>
    ({ type: 'skill', name: skill.name, path: skill.path })); }`
  - line 282 and line 333 `call('turn/start',{threadId,effort:role.effort,
    input:[...structuredSkills(skills),{type:'text',text:plan.firstPrompt}]})`
  - lines 273-277 and 317-321 resolve each required name through
    `call('skills/list',{cwds:[cwd]})` and read its file from the returned
    `path`, failing with `required native skill unavailable: <name>` when the
    name is missing.
  - line 133 pins `requiredMainFlow` to
    `<cwd>/.agents/skills/main-flow/SKILL.md`.
  - line 130, in the first prompt text: `The launcher sends these
    role-specific skills through the native structured interface: … A written
    dollar token is not skill receipt.`
- Expanded form in context: the binary carries the literal tags `<skill>` and
  `</skill>`. `/home/li/.codex/config.toml` line 3 sets
  `developer_instructions` describing `A pasted <skill ...>...</skill> block`
  as the shape a loaded skill takes.
- Skill listing over the protocol: `SkillsListParams{cwds, forceReload}` →
  `SkillsListResponse{data:[SkillsListEntry{cwd, errors, skills}]}` where
  `SkillMetadata` requires `description, enabled, name, path, scope` and
  `SkillScope` is one of `user | repo | system | admin`. A separate
  `SkillsConfigWriteParams{name?, path?, enabled}` toggles a skill's enabled
  state; the binary carries `codex_config::skills_config` and its
  `SkillConfigRules::resolve_disabled_paths`, with config keys `skills` and
  `disabled`.

### Unknown — Codex CLI

- Whether a catalog-suppressed skill can still be named by the user as
  `$main-flow` in the TUI. The binary carries
  `codex_tui::chatwidget::skills::enabled_skills_for_mentions`, which suggests
  a separate mention path, but its relation to `allow_implicit_invocation` was
  not established. The authored source describes the Codex deployment as
  "$-name-only injection"; that phrase is not confirmed by the implementation,
  which emits a policy sidecar. Unknown.
- Whether `allow_implicit_invocation: false` removes the entry from the
  catalog or merely forbids acting on it. The live run shows the names absent
  from what the model reports reading, which is consistent with removal;
  removal was not read out of the renderer. Unknown, leaning removal.
- Whether `skills/list` returns a suppressed skill. The launcher resolves
  `main-flow` through `skills/list` and has been reported working, which
  implies yes, but no direct call was made in this flow. Unknown.
- Whether the guardian layer sees the injected skill. The binary carries
  `guardian.trusted_skills` and `Codex-verified invoked user-owned skill
  paths:`; the semantics were not established. Unknown.
- Whether `SkillMetadata.enabled` and the sidecar policy are the same switch.
  Unknown.

---

## The projection

Authored sources live in `/git/github.com/LiGoldragon/Curriculum/skills/*.md`.
The generator is a separate Rust crate,
`/git/github.com/LiGoldragon/curriculum-deploy`, pinned as a flake input and
run as `Generate.{ «data-root» «workspace-root» }`. Skills project into two
trees only — `.claude/skills` and `.agents/skills`. `.codex/` and `.pi/`
receive role packets from `roles.datom` and no skills at all; there is no
`.codex/skills` or `.pi/skills` on disk.

`user-only: true` becomes:

| target | what it becomes |
| --- | --- |
| `.claude/skills/<name>/SKILL.md` | the line is rewritten to `disable-model-invocation: true` |
| `.agents/skills/<name>/SKILL.md` | the line is kept verbatim as `user-only: true` — inert to Codex |
| `.agents/skills/<name>/agents/openai.yaml` | a new file: `policy:\n  allow_implicit_invocation: false\n` |
| `.codex/…` | nothing; no skill projection exists |
| `.pi/…` | nothing; no skill projection exists |

### Evidence

Reported by this flow's projection subflow, from the generator source:

- `curriculum-deploy/src/runtime.rs:320-327` — the surface loop, two entries:
  `(".agents/skills", SkillTarget::Codex)` and `(".claude/skills",
  SkillTarget::Claude)`.
- `curriculum-deploy/src/runtime.rs:246-251` — the Claude rewrite:
  `if self == Self::Claude && directive == "user-only: true" {
  rendered.push_str("disable-model-invocation: true\n"); } else {
  rendered.push_str(line); }`. It matches any body line, not only frontmatter.
- `curriculum-deploy/src/runtime.rs:328-336` — the Codex sidecar, emitting
  `.agents/skills/<name>/agents/openai.yaml` with
  `"policy:\n  allow_implicit_invocation: false\n"`.
- `curriculum-deploy/src/runtime.rs:422-426` — the predicate `user_only`,
  exact line match `user-only: true` inside the leading `---` block.
- `curriculum-deploy/src/roles.rs:158-190` — the three role surfaces
  (`.claude/agents/*.md`, `.codex/agents/*.toml`, `.pi/agents/*.md`); none
  emits a user-only or explicit-invocation marker.
- `curriculum-deploy/tests/runtime.rs:69-133` pins all of the above;
  `:110-114` asserts the Claude file contains `disable-model-invocation: true`
  and not `user-only: true`.
- There is no per-skill manifest. Every authored `skills/*.md` projects to both
  trees by directory scan (`src/runtime.rs:268-296`); `roles.datom` lists roles
  only.

Confirmed on disk by this flow:
`/home/li/primary/.claude/skills/design/SKILL.md` line 3 reads
`disable-model-invocation: true`; `/home/li/primary/.agents/skills/design/SKILL.md`
line 3 reads `user-only: true`; `/home/li/primary/.agents/skills/design/agents/openai.yaml`
contains the two policy lines. No `.codex/skills` or `.pi/skills` exists.

### Drift found

`skill-designing.md` lines 53-56 say a user-only skill "deploys as
`disable-model-invocation: true` in Claude Code and as $-name-only injection
in Codex". The generator emits a policy sidecar, not a `$`-name arrangement,
and the Codex invocation route that this repository actually uses is the
structured `{type:"skill", …}` turn input. The authored sentence and the
implementation disagree.

Neither `claude-harness.md` nor `codex-harness.md` says anything about skill
visibility. `claude-harness.md` lines 20-25 mention "skills loaded through the
skill interface" only as a context-strata classification;
`codex-harness.md` does not mention skills at all.

---

## Proposed replacement text

### claude-harness.md — insert after the strata paragraph (after line 25)

> A skill's frontmatter says who may invoke it.
> `disable-model-invocation: true` withholds it from the model: the name is
> absent from the available-skills listing, and the skill interface refuses
> it. `user-invocable: false` withholds it from the typed command list.
>
> A withheld skill enters through the living's own input. The harness reads a
> leading `/name` from the typed message, expands the skill body itself, and
> delivers it as a middle-stratum message; two records mark the turn, one
> naming the command and one carrying the rest of the typed text as its
> argument. The command is read only at the head of the input — up to five
> may stack there — and the first text that is not a command ends the parse,
> so a command written further down a block stays literal. One block of
> startup text carries a skill only when the command is its first token.
>
> A launcher that must not spend a typed turn has two other routes: a
> SessionStart hook returns `initialUserMessage` or `additionalContext` into
> the first turn, or the launcher reads the skill file and writes its body
> into the first prompt.
>
> A subflow has no living to type for it. It cannot see or load a withheld
> skill; what it must carry belongs in its brief.

### codex-harness.md — insert after the strata paragraph (after line 29)

> Codex renders a skills catalog into the session instructions: a name, a
> description and a location for each skill it discovers. The catalog is the
> whole of what the machine knows about them. A skill is withheld by an
> `agents/openai.yaml` beside its `SKILL.md` declaring
> `policy: allow_implicit_invocation: false`; the entry then does not appear,
> and unrecognised frontmatter keys change nothing.
>
> A withheld skill still reaches the machine when the client places it there.
> The turn request's input array takes a skill item carrying a name and a
> path, and that item expands into the turn as the file's text ahead of the
> living's own words. This is how a launcher seats a skill the catalog does
> not offer.
>
> A subflow renders its own catalog and so cannot see a withheld skill. The
> base instructions also require the main session to read skill instructions
> itself rather than delegate that reading.

### skill-designing.md — replace lines 53-56

> `user-only: true` — the skill enters only through the living's typed prompt
> or a launcher's first turn; the flow cannot load it. It deploys as
> `disable-model-invocation: true` in Claude Code, and in Codex as a policy
> sidecar beside the skill that withholds it from the skills catalog.

What this preserves, changes, removes: it preserves the rule that a user-only
skill is unreachable by the flow and the Claude deployment line. It corrects
the Codex line, which named a `$`-token convention the generator does not
emit. It adds the launcher's first turn as the second legitimate entrance,
which the current line denies by omission. It removes nothing else.

---

## Sources

- `claude --version`; `codex --version`; `codex --help`;
  `codex app-server --help`; `codex app-server generate-json-schema -o <dir>`.
- Live Codex run, session `01a0d4d3-ac83-7710-a34c-c007b74dabef`, command
  quoted above.
- First-person Skill-tool refusal and available-skills listing of this
  subflow, 2026-09-24.
- `~/.claude/projects/-home-li-primary/752e0f7e-49ec-4110-b27b-6107e0eb6520.jsonl`
  lines 200-201; `<command-args>` shapes surveyed across
  `~/.claude/projects/-home-li-primary/*.jsonl`.
- `/nix/store/wz475h72i242nf55ydn0zx7hfk9dh6jv-claude-code-2.1.280/bin/.claude-wrapped`
  string table.
- `/nix/store/wdj0sc69r4n9is1idfb32vcx5739ijkh-codex-0.153.4/bin/.codex-wrapped`
  string table.
- `/home/li/primary/tools/claude-native-seat-refresh.py` lines 115-128, 668,
  700; `/home/li/primary/tools/native-seat-launch.mjs` lines 130, 133, 136,
  273-277, 282, 317-321, 333.
- `/home/li/primary/.claude/skills/*/SKILL.md`,
  `/home/li/primary/.agents/skills/*/SKILL.md`,
  `/home/li/primary/.agents/skills/*/agents/openai.yaml`;
  `/home/li/.codex/config.toml` line 3.
- Claude Code field list and the transcript record's companion fields relayed
  from this flow's Claude Code research subflow, which read the published
  Claude Code documentation. Its leading-command rule and its subagent finding
  agree with this flow's own bundle reading and first-person witness; its
  `user-invocable` claim does not, and is carried as unknown.
- Generator and authored-source findings relayed from this flow's projection
  subflow, which read `/git/github.com/LiGoldragon/curriculum-deploy/src/runtime.rs`,
  `src/roles.rs`, `tests/runtime.rs`, `/home/li/primary/flake.nix`, and
  `/git/github.com/LiGoldragon/Curriculum/skills/{claude-harness,codex-harness,skill-designing}.md`.
  Line numbers in the projection section are that subflow's, not this flow's;
  the on-disk confirmations named there are this flow's own.
