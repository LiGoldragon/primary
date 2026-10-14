# Values audit (part c): runtime values that should be configuration

Scope as audited. Repositories with a path in SKILL_VARIABLES.md: Primary
(tools/, launchers, hooks), Curriculum (73414b6), CriomOS (b691715),
CriomOS-home (8fa8630c). Not listed in SKILL_VARIABLES.md, so skipped:
flow, nexus, orchestrate, messenger-clj, Lojix, goldragon.
Every finding below was read at the cited lines. Paths are relative to each
repository root. "No switch" marks a feature with no on/off.

## Primary (/home/li/primary)

1. No switch: the main-flow reminder hook goes into every Claude main seat,
   at a fixed cadence.
   `tools/claude-main-flow-launch.mjs:150-156`:
   `'--state-dir', ..., '--every', '20'` then
   `settings = {hooks: {UserPromptSubmit: [...]}}` with no condition.
   `tools/main-flow-mode/reminder-hook.json` uses `--every 1` for the same hook.
   Why configuration: how often the core is re-injected, and whether it is,
   is a policy, and the two files already disagree on it (20 vs 1).
   Lacks: a launch option or setting that turns the reminder off and sets N.
   (The committer Stop hook beside it, lines 158-162, is switched by
   `PRIMARY_COMMITTER_FLOW_ID`; that one has its switch.)

2. No switch: the Field Luna heartbeat reaps routes whenever a valid
   retirement marker is eligible.
   `tools/field-luna-heartbeat.mjs:76-82`: on `eligible` it writes the archive
   receipt, runs `hm-deregister`, then `herdr ... pane close`.
   Line 56 runs `codex exec ... --model gpt-5.6-luna` on every changed
   fingerprint. Neither has an observe-only mode; the sibling
   `tools/field-census-cycle.mjs:12` has `--observe-only`.
   Why configuration: whether a monitor acts or only observes is a
   deployment choice; the model is a choice that changes by ruling.
   Lacks: an observe-only/act switch and a model input.

3. The voice table (aspect.layer to harness, model, effort) is code.
   `tools/native-voice-profiles.mjs:3-25`, e.g.
   `'Psyche.Secondary': {..., model: 'claude-opus-5-5', effort: 'medium', source: 'living ruling 2026-10-10'}`.
   Why configuration: the rows cite living rulings and change with them;
   the code only needs to select a row. SKILL_VARIABLES.md also declares
   `Psyche medium Claude model: claude-opus-4-6[1m]` and
   `Psyche medium Claude effort: medium`; the code table does not read it and
   carries different Claude models. Two surfaces, two values.

4. Model-to-client routing is a literal model list.
   `tools/native-main-flow-launch-shared.mjs:71-76`:
   `const next = ['gpt-6-astra', 'gpt-6-sol', 'gpt-6.1-sol', 'gpt-6-luna'].includes(model);`
   then `~/.nix-profile/bin/codex[-next]` and
   `~/.codex/app-server-control/app-server-control.sock`.
   Why configuration: which models a Codex endpoint serves is declared in
   CriomOS-home (`FLOW_CODEX_NEXT_MODELS=gpt-6-sol,gpt-6-luna,gpt-6-astra`,
   finding H8); the code copy diverges (adds `gpt-6.1-sol`).

5. Committer model and effort fixed in code.
   `tools/primary-committer/seat-process.mjs:38`:
   `{model: 'gpt-6-luna', model_reasoning_effort: 'low', ...}`.
   `tools/primary-committer/restart.mjs:35` (untracked, in progress) refuses
   any config whose `resumeArgs` lack `gpt-6-luna` and
   `model_reasoning_effort="low"`; the rest of restart.mjs is config-fed.
   Why configuration: the seat's model is a role assignment, the same kind
   of value as finding 3.

6. A deployed monitor holds its paths, sender and recipients as constants.
   `flows/98eb43/monitor/census.mjs:7-15`:
   `const root = '/home/li/primary';`,
   `const stateDirectory = '/home/li/.local/state/field-monitor-98eb43';`,
   `herdr`, `hm-list`, `hm-send`, `jj` as `/home/li/...` paths;
   lines 84-85: `for (const recipient of ['e51411', '38de5b'])` and
   `FLOW_ID: '98eb43'`.
   CriomOS-home patches the six path constants by text replacement (H5);
   the recipients and sender are not patched.
   Why configuration: who is alerted and where state lives differ by
   deployment and by which flows are live.

7. Claude and Codex transcript roots hardcoded, beside their declared
   variables (`Claude transcript root`, `Codex transcript root`).
   - `tools/claude-main-flow-launch.mjs:185-186`:
     `path.join(os.homedir(), '.claude', 'projects', ...)`.
   - `tools/field-census.mjs:75` and `:256`:
     `'.claude/projects/-home-li-primary'` (workspace slug baked in);
     `:58`: `path.join(os.homedir(), '.codex/sessions')`.
   - `tools/claude-native-seat-refresh.py:27-28`: `KEY_PATH`, `PROJECT_ROOT`
     under `~/.claude`; `:26` `/tmp/cc-daemon-{uid}`.
   - `tools/native-worker-launch.mjs:36-37`: socket and sessions defaults
     (flag override exists).
   - `tools/canonical-title-alignment.mjs:17` (env override exists).

8. Primary workspace path as default or constant.
   - `tools/reap-flow:29`: `ROOT = pathlib.Path("/home/li/primary")`, no
     override; `FLOWS`, `ARCHIVE` derive from it.
   - `tools/extractor/extractor.py:211`:
     `Path("/home/li/primary/flows") / session_prefix`.
   - `tools/claude-main-flow-launch.mjs:88`, `tools/codex-main-flow-launch.mjs:44`,
     `tools/opencode-main-flow-launch.mjs:44`: `workspace: '/home/li/primary'`.
   - `tools/field-flow-preflight.mjs:13-14`: `/home/li/.local/bin/flow`,
     `/home/li/.local/bin/flow-nexus`.

9. Repository root, a declared variable (`Repository root: /git`), restated.
   - `tools/component-evidence:7`, `tools/repo-inventory:5`:
     `process.env.REPO_ROOT ?? '/git/github.com/LiGoldragon'`.
   - `tools/engine-situation:6-10`: five `/git/github.com/LiGoldragon/...`
     defaults.
   - `tools/nix-local-stack:47`: `github_owner=LiGoldragon`.

10. Hand-written systemd units with user paths in a general repository.
    `tools/field-census/field-census.service:6-10` and
    `tools/field-checkup/field-checkup-shadow.service:7-11`:
    `WorkingDirectory=/home/li/primary`,
    `ExecStart=/home/li/.nix-profile/bin/node /home/li/primary/tools/...`.
    Why configuration: these are deployment declarations; CriomOS-home
    already declares `fieldCensus` and `fieldCheckupShadow` units with enable
    options (`modules/home/profiles/min/field-monitoring.nix:132,147`).

11. Messenger's registry location restated in four consumers.
    `~/.local/state/hacky-messenger` at `tools/canonical-title-alignment.mjs:16`,
    `tools/field-census.mjs:13`, `tools/reap-flow:31-32`, `tools/reaper:31`
    (all with `HM_REGISTRY` override). `tools/messenger:15` uses
    `~/.local/state/messenger`.
    Why configuration: the store location belongs to messenger's
    configuration; consumers should be given it.

12. Model names as tool defaults.
    `tools/native-worker-launch.mjs:9`: `const MODEL = 'gpt-5.6-terra';` (no
    flag). `tools/extractor/extractor.py:234` and
    `tools/extractor/intelligence.py:59`: default `gpt-5.6-luna` (flag exists).

## Curriculum (/git/github.com/LiGoldragon/Curriculum)

C1. No switch: every harness surface is always projected.
    `src/projection.rs:27-53`: `const SURFACES: [Surface; 5]` =
    `.agents`, `.claude`, `.codex`, `.pi`, `.opencode`.
    The directory name per harness is structure (each harness reads its own);
    which harnesses a workspace serves is configuration.
    Lacks: a per-workspace harness set.

C2. Pi agent provider fixed.
    `src/roles.rs:232`: `model: 'openai-codex/{}'`.
    Why configuration: the provider behind a Pi agent is a choice, the model
    beside it already comes from roles.datom.

C3. Socket fallback differs between client and service.
    `src/client.rs:179-185`: `XDG_RUNTIME_DIR` else empty, so a relative
    `curriculum/curriculum.sock`; `src/service.rs:303-307`: else `/run`.
    Settings otherwise come from environment (`src/service.rs:28-42`),
    which is the right shape; the fallbacks are the stray values.

## CriomOS (/git/github.com/LiGoldragon/CriomOS)

O1. No switch: a one-host cleanup runs on every activation of every
    UsbDownlink node.
    `modules/nixos/network/usb-downlink.nix:144-147`:
    `system.activationScripts.usbDownlinkLegacyHotfix` under
    `mkIf declared`; `modules/nixos/network/usb-downlink-hotfix.nix:60-66`
    removes `90-field-prometheus-usb.conf`,
    `field-prometheus-usb-firewall.sh`, `id=prometheus-share-temporary`
    (ouranos artefacts, per the file's own comment, line 1).
    Why configuration: host-specific names in a general module, tied to a
    temporary condition. Lacks: an off once ouranos is clean.

O2. User name and port fixed.
    `modules/nixos/testing/opencode.nix:51`: `owner = "li";`
    `:26`: `--port 4096`. Other modules derive owners
    (`llm.nix:164 owner = runtimeUser`). Why configuration: the operator
    user comes from Horizon.

O3. `devshell.nix:31-34`: `/git/github.com/LiGoldragon/${name}` (the
    `Repository root` variable restated).

## CriomOS-home (/git/github.com/LiGoldragon/CriomOS-home)

H1. Feature enables keyed to a user name.
    `modules/home/profiles/min/flow.nix:46`:
    `default = config.home.username == "li";` and `:63-64` assertion
    "Flow Nexus currently uses fixed li/1001 state and socket paths".
    Same at `flow-message-next.nix:271,279`; `codex-remote-control.nix:18-24`
    and `codex-next.nix:10-16` gate on `"li"`/`"/home/li"` or `"bird"`.
    A switch exists, but its value is an identity test. Why configuration:
    who runs Flow and Codex endpoints is Horizon user data.

H2. Flow's store is relocated by rewriting HOME.
    `lib/stable-next-service.nix:3-11`: "Every Nexus derives its whole
    default layout from two anchors: HOME (its `.sema` store under
    `.local/state/<name>/`) and XDG_RUNTIME_DIR". `:44` sets
    `homeAnchor = "${homeDirectory}/.local/state/${slotName}"`; `:70`
    exports `HOME=${homeAnchor}`; `:17-20` then re-exports the real XDG
    homes because the HOME change reaches children.
    Why it matters: the store path is not an input of the Nexus, so
    configuration reaches it only through HOME. This is today's lead; the
    Flow source itself was not read (see Unknowns).

H3. Flow service paths and models written literally although
    `config.home.homeDirectory` is in scope.
    `modules/home/profiles/min/flow.nix:81-89`: `FLOW_SOURCE_ROOT=/home/li/primary`,
    `FLOW_CODEX_STABLE_HOME=/home/li/.codex-next`, ...;
    `flow-message-next.nix:142-158` (`occupiedNextFlowUnit`) the same, with
    pinned `/nix/store/...` executables. `flow-message-next.nix:114` already
    uses `${homeDirectory}/primary`.

H4. Skill roots restated twice, beside SKILL_VARIABLES `Psyche skills`,
    `Mind skills`, `Field skills`.
    `modules/home/profiles/min/curriculum.nix:14-16` and `:21-23`:
    `CURRICULUM_PSYCHES_SKILLS_DIR=/git/github.com/LiGoldragon/psyche-skills/skills` etc.

H5. Values injected by text patch into a runtime script.
    `modules/home/profiles/min/field-monitoring.nix:74-83`:
    `substituteInPlace ... --replace-fail "const root = '/home/li/primary';" ...`
    for six constants of `flows/98eb43/monitor/census.mjs` (Primary
    finding 6). The script should take these as inputs.

H6. Builder host in the shared min profile, no switch.
    `modules/home/profiles/min/default.nix:516-517`:
    `matchBlocks."prometheus.goldragon.criome prometheus"`,
    `hostname = "prometheus.goldragon.criome"`; comment at 512-513 calls it
    host-specific. SKILL_VARIABLES declares `NixBuilder`.
    Lacks: derivation from the cluster's builder node, or an enable.

H7. Per-user paths in the shared min profile.
    `modules/home/profiles/min/default.nix:89-102`: Codex project trust for
    `/home/li/git/CriomOS`, `/home/li/primary`, ... applied to every user
    of the profile. `:77-80`: `model = "gpt-6-astra"`,
    `model_reasoning_effort = "xhigh"` as the profile default.

H8. Codex endpoint model lists written in two modules.
    `flow-message-next.nix:74-83` (`stableModels`, `nextModels`) and
    `flow.nix:85,89` as literal strings; Primary finding 4 holds a third,
    divergent copy.

## Judged structure, not findings

RPC and subprocess bounds (`timeout: 15000` for herdr calls in the three
launchers, 10_000 in `tools/prompt-relay:224,228`, frame caps in
`tools/messenger:21,120`); harness directory names (`.claude/skills`);
`/var/lib/<service>` state directories inside CriomOS modules (the module is
the configuration surface); Claude Code minimum version for Sonnet 5.5
(`tools/claude-main-flow-launch.mjs:62-63`, a vendor fact).

## Unknowns

- Flow, nexus, orchestrate and messenger-clj sources were not read
  (not in SKILL_VARIABLES.md). The HOME-derived store (H2) and "fixed
  li/1001 state and socket paths" (H1) are claims in CriomOS-home comments
  about that code, not witnessed in it.
- Curriculum reads `CURRICULUM_PSYCHES_REPOSITORY_DIR`
  (`src/service.rs:36`); CriomOS-home sets `CURRICULUM_PSYCHES_SKILLS_DIR`
  (`curriculum.nix:14`). Whether the deployed package (pinned through
  `inputs.primary`) reads the latter was not checked.
- Where the committer Stop hook is installed for editors outside
  `mainFlowMode` was not found in `.claude/settings.json` or CriomOS-home.
- Which of finding 3 and SKILL_VARIABLES governs a Psyche launch is unknown.
