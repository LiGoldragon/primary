# Meta harness survey

Scope: the native launch and voice tooling that starts seats, its
redeployability, and testing it with API keys versus subscriptions.
Labels: **Witnessed** means this flow read the file or ran the command
on 2026-10-10. **Claim** means a record says it and this flow did not
observe the thing. **Inferred** is this flow's own reading.

## 1. What the written psyche says

All quotes are verbatim from the named file. Dates are the record's own
date, or the file's first commit date where the record gives none.

### 1.1 The order this survey serves

`flows/d68c82/vision/metaHarness.md` (also copied to
`flows/9519a1/vision/metaHarness.md` and `flows/875960/vision/harness.md`),
2026-10-10, STT:

> Let's flesh these out and let's also make a conviction of getting a proper base for the meta harness to work smoothly and to be redeployable. Right now it's kind of like a one-off that only exists on my computer. Creating full tests somehow will probably require that we rely on an API for testing since it's easier to deal with the key management than the subscription. We're going to figure out a way to handle subscriptions.

Three asks (inferred split): a proper base that works smoothly; redeployable
beyond this one computer; full tests, likely through an API key, while a way
to handle subscriptions is still to be found.

### 1.2 Earlier words on the meta harness itself

`flows/7328f4/vision/metaHarness.md`, 2026-10-01, typed:

> The most important thing we need now is to improve the meta harness: how easy it is to restart flows, how easy it is to deploy skills, and how much it becomes the implementation that we want with the correctness and the anatomy that we want.

`flows/6997eb/vision/metaHarness.md` (same words relayed in
`flows/bd0019/vision/metaHarness.md` and `flows/fe945a/vision/metaHarness.md`),
2026-10-02, typed:

> Get a full grasp of everything and re-question this: the current implementations and skills, and see, use Opus and Sonnet, and restart the whole psyche stack with a fresh well-concentrated psyche context on making the meta harness more usable.
> - Starting sessions
> - Handling skills
> - Messaging hooks
> - Deprecation of session
> - Restarting of sessions
> - Starting of ephemeral sessions
> - All of the session handling side of things

`flows/1a6ca4/vision/personaMetaHarness.md`, 2026-09-05, STT:

> That phase is like the wild west phase of thinking machines, and the persona meta-harness is going to bring in the dawn of the more complete thinking machine systems, which will be a complex infrastructure of a kind of thinking machine legal system interworking apparatus.

### 1.3 Who launches: Flow, not scripts

Distilled, `vision-flow` (authored source
`/git/github.com/LiGoldragon/psyche-skills/skills/vision-flow.md`, last
commit 2026-10-09): "The Flow Nexus sets up and starts a model flow: its
working directory, system prompt, training files and instruction prompt."
"A Nexus component decides the system prompt and everything about a
launch". "The model behind a voice is configuration, declared once in Flow
and changed only over its meta wire".

Distilled, `vision-model-roles` (authored source, last commit 2026-10-09):
"The model is declared once, as typed configuration in Flow, mutated only
through the meta wire. Skill variables carry that value by name into every
skill, launcher and brief. Nothing else holds a model name, so a launcher
never writes one by hand". Also: "the Max subscription is the only
subscription that can use [the million-token Opus 4.6], so a declaration
never assumes the million-token version is available to every operator."

Distilled, `vision-nexus` (authored source, last commit 2026-10-07) gives
Flow's wire: `Start.{ Voice Capsule }`, `Refused.[ NoCapsule ... ]`,
`Capsule.{ Home.String Login.Vector<String> }`.

Raw, `flows/b81560/vision/operational-flowCLIStartsSessions.md`, 2026-09-19:

> Starting a new session should be done with the Flow Nexus using the Flow CLI.

Raw, `flows/af762b/vision/operational-flowOwnsHerdr.md`, 2026-09-18 (relayed):

> Basically, Flow is in charge of herder. I shouldn't interact with it directly.

Raw, `flows/752e0f/vision/herdrSessions.md`, 2026-09-24, typed:

> I just want a single herder session that's controlled by Flow, the Nexus. I want Flow to be our tool to send messages and stuff until it actually uses the Flow API through its socket to actually send messages more sanely.

Raw, `flows/d8df70/vision/flowTool.md`, 2026-09-24:

> We can add an already-live Herdr meta flow with all of its flows into the running flow with the meta socket. You don't have to spend too much time creating it. Although we should have a tool to import an already-running Herdr session into Flow eventually, otherwise we can just bootstrap by hand for now.

Raw, `flows/fd0f97/vision/launch.md`, 2026-09-15, typed:

> A proper Flow component that launches Claude properly, makes it accessible remotely, and makes it appear on the desktop in a beautifully normally colored terminal, maybe under Herder if it works better. [...] I would need some kind of a simple command to remember, or just a shortcut that maps to this simple command. Actually, we should always have a simple command for everything.

Raw, `flows/da1e3f/vision/operational-launcher.md`, 2026-09-17, typed (the
interim launch script, until Flow owns dispatch):

> Your current view of this system is going to be the operational vision of it, and then you can pass it over to get your script that you can probably launch yourself, together with what I can launch with remote-accessible cloud, high, medium, and low power, all ready to go with all of them considering their role, which is going to be authored separately, right?

Raw, `flows/108ab0/vision/operational-flowDatomLauncherLanguage.md`, 2026-09-17, typed:

> We need to be able to launch flows with a simple Flow Datom language, with all the preconfigured defaults for a short version. We just have a medium model for this, and it's preconfigured, but you have a more extensive language that you can use to launch a more elaborate version. That's better for testing and stuff, or you just have the low-powered one as one of the variants.

Raw, `flows/9993b5/vision/workspaceProvisioning.md`, 2026-09-17, typed:

> When Flow starts, it can ask for curriculum: "Okay, give me a primary psyche, main Flow, like medium Opus, old Opus, or you know, medium." It just asks for medium, and by default, medium means Claude. The Flow can maybe have the power and the quota awareness of how much we spend, so it might start a Claude or a Codex if it's not specified. If it's specified, that's what it's launched with. Curriculum provides all of the skill files for that workspace.

Launch-prompt shape, `flows/e51411/vision/launch.md`, 2026-09-24:

> There should be only one prompt when we start a fresh flow, not two, because then that costs more money and it's less efficient.

> All that matters is that everything comes in as one block.

> I don't understand the problem. Your all [sic] flows should be started with `dangerously skip permissions` so you weren't launched properly, so get relaunched.

Stock harnesses, `flows/b05237/vision/operational-criomosModularHardware.md`, 2026-09-18:

> We want to keep the harnesses as stock as possible in one version, at least, and the ordinary executable name and the desktop apps too. I don't want to keep modifying them.

### 1.4 Redeployment

`flows/445410/vision/deployment.md`, 2026-10-09, typed:

> I don't want stateful stuff that isn't accounted for in [CriomOS], so see if there's any stateful stuff that has been done that's left running in our environment.

> I want it to be easy with just a few CLI calls and an explain method for how to redeploy Zeus.

`flows/01a01a93/vision/hostEnvironmentRecovery.md`, 2026-08-19:

> use the nix user env only, or OS redeploy

`flows/e167d8/vision/deployment.md`, 2026-09-26, STT:

> Like I said I want to start doing constant redeployment when I declare the environment that we're testing to be usable, right? Then we can deploy `main` on the rest of the network.

`flows/d4ae97/vision/deployment.md`, 2026-10-08, STT (Codex login across servers):

> Let's review how we can fix the whole Codex update situation where we had problems with the login token expiring because both servers tried to renew them. If a server isn't being used we should turn it off so we need to think of a design to do that.

`flows/7dc7cc/vision/redeploying-the-operating-system-after-a-user-is-deployed.md` (undated in file):

> "After a user is deployed, we need to redeploy the entire operating system so that, if there's a reboot, the user environment isn't replaced with an older version."

Distilled, `vision-deployment` (last commit 2026-10-07): "A proof of
concept is worked on and deployed on the host the flow is running on."
"Zeus is a stable node, and stable nodes are not where testing happens."

### 1.5 Testing, credentials, subscriptions, API keys

Distilled, `vision-flow`: "The Capsule is the component that makes where a
flow runs. Its first embodiment is the semi-sandbox: only the credential
files are copied, everything else is recreated, with its own sockets and
store, running light models. Later it encrypts the sensitive parts of the
filesystem under a volatile key."

Distilled, `intent-testing` (last commit 2026-10-07): "A proof of concept
is tested in a sandbox first. [...] A proof of concept runs outside a
sandbox only when it cannot run in one, such as a browser login with the
living's credentials."

`flows/91ea9f/vision/testing.md`, 2026-10-02, STT:

> "I want faster testing also. I don't want to have to deploy or depend on deploying fully through CreoOS before testing. We can have a Nix-written sort of semi-sandbox. Again we have to iron out how we move my credentials into a sandbox so that you can test stuff with small cheap models."

`flows/3ec648/vision/capsule.md`, 2026-10-02, STT:

> "You could create and use a different socket. Just create the environment yourself. You can make this semi-sandbox. I know it's possible if you just reuse the same credentials and you just recreate everything else. The only thing you copy is the credentials then it'll work.
>
> If there is a credential rotation then we need to maybe use the new credentials that have been... I don't know. Somebody brought that up but I don't even know if it's a thing. For now let's just test it the simple way."

`flows/e167d8/vision/testRepos.md`, 2026-09-26, STT:

> I think the best would be to copy the login credentials and then generate all the configuration details that work for our test sandbox.

`flows/6cc91b/vision/sandbox.md`, 2026-09-14, STT:

> We have a sandbox test version of this, a light sandbox, which is basically a sandbox of my home environment, and it can reuse my login, but with a different user environment.

`flows/024bc7/vision/sandbox.md`, 2026-09-13, STT (also in
`flows/bcd02a/notion/sandbox.md` as notion):

> Can we copy the token into another host so that my codex and Claude log in? I'm logged in to my subscription so that we can use the models in the virtual machine. I lock the keys into an encrypted, volatile, throwaway key, right, with only the process that needs the token having it. I don't know if we use GoPass, if there's a better system, or if we make our own key encryption system.

`flows/6cc91b/vision/billing.md`, 2026-09-14, STT:

> What is the most affordable pay-per-use token base? If someone wants to get the fair price from Claude, does one have to use a subscription, a max subscription? How do we get a fair price for another model that we can then set up as a credited account easily, so that test machines can have their own account that has a block on the amount that can span and stuff like that, or needs to be refilled manually?

`flows/e1953c/vision/secrets.md`, 2026-09-14, STT:

> Right, even on the public part, there is private data, like tokens, that the public, meaning they push to public repos, shouldn't be trusted with too much, in case they put it in a repo publicly facing stuff.

> It then creates the OpenRouter credential with my name to pay for it with the layer 0, which would be the only layer that is allowed to do stuff like that.

`flows/1b8ac0/vision/flowNexus.md`, 2026-09-21 (relay, verbatim not established):

> - Get Mind to recheck the fully tested pair with a semi-sandbox that lets it use my login to test with Haiku and Luna only, and test it in a VM.

`flows/f38926/vision/operational-openCodeRemoteAccess.md`, 2026-09-19:

> But because we need to log in in the browser with my credentials, and you can't really run this in a virtual machine

Notion, `flows/e51411/notion/v2.md`, 2026-09-25: a second, fully
Flow-controlled Herdr container as a test network ("Psyche V2 Fable"), and
"I'll get OpenRouter credentials."

## 2. What exists today

### 2.1 Native launch tooling in Primary (Witnessed, read 2026-10-10)

| Path | Last commit | Role |
|---|---|---|
| `tools/native-voice-profiles.mjs` | 2026-10-09, plus an uncommitted edit | Voice → harness, model, effort table |
| `tools/native-voice-launch.mjs` | 2026-10-09 | `--voice Aspect.Layer --brief PATH (--root --metaflow FILE \| --predecessor ID)`; dispatches to the Claude or Codex launcher |
| `tools/claude-main-flow-launch.mjs` | 2026-10-09 | Claude seat in a Herdr pane |
| `tools/codex-main-flow-launch.mjs` | 2026-10-09 | Codex seat in a Herdr pane |
| `tools/native-main-flow-launch-shared.mjs` | 2026-10-09 | continuation record, skill resolution, Codex client choice |
| `tools/opencode-main-flow-launch.mjs` | 2026-10-07 | OpenCode seat |
| `tools/native-worker-launch.mjs` | 2026-10-03 | worker launch |
| `tools/claude-native-seat-refresh.py` | 2026-10-07 | Claude seat refresh through Herdr |
| `tools/main-flow-mode/` | 2026-10-03 | system prompt and reminder hook |
| `tools/reap-flow`, `tools/reaper` | 2026-09-25, 2026-09-18 | reaping |
| `tools/third-seat/` | 2026-09-14 | OpenCode + Kimi K3 API-key route, held |

- The voice table is hand-written model names in a script. Its uncommitted
  diff changes `Psyche.Secondary` from `unresolved` to
  `{harness: 'claude', model: 'claude-opus-5-5', effort: 'medium', source: 'living ruling 2026-10-10'}`.
  `Mind.Secondary` is `pending`, `Field.Secondary` `unresolved`.
- Defaults bound to this machine: `workspace: '/home/li/primary'`,
  `herdrSession: 'default'` (claude-main-flow-launch.mjs:87,
  codex-main-flow-launch.mjs:43).
- The Claude seat starts as `claude --session-id … --remote-control
  --dangerously-skip-permissions --system-prompt-file … --settings …`
  inside `herdr --session default pane run` (claude-main-flow-launch.mjs:280-281),
  then waits for `~/.claude/projects/-home-li-primary/<id>.jsonl`.
- Codex client choice hard-codes model names and `~/.nix-profile/bin/codex-next`,
  and parses the installed wrapper for `CODEX_HOME` and its socket
  (native-main-flow-launch-shared.mjs:71-84).
- External programs required on PATH: `herdr`, `claude`, `codex`/`codex-next`,
  `flow-id`, `hm-register`, `curriculum`; skills read from the generated
  `.claude/skills` or `.agents/skills` in the workspace.
- `claude-native-seat-refresh.py` reads `~/.claude/daemon/control.key` and
  `~/.claude/projects` (lines 27-28).
- Credentials: all of these use the living's logged-in subscription
  state in `~/.claude` and `~/.codex*`. No launcher takes an API key.
- Packaging: no Nix module installs these scripts. They run as
  `node /home/li/primary/tools/…` from the Primary checkout. A grep of
  CriomOS-home for `native-voice` and `main-flow-launch` returned nothing.
- Tests: `*.test.mjs` exist for each launcher (native-voice-profiles.test.mjs
  41 lines, native-voice-launch.test.mjs 20 lines). Whether any needs a
  live login was not run here.

### 2.2 Home-manager modules (Witnessed, `/git/github.com/LiGoldragon/CriomOS-home`, tip 2026-10-09)

- `modules/home/profiles/min/flow.nix` (2026-09-30): `flow-nexus` user
  service with `FLOW_SOURCE_ROOT=/home/li/primary`,
  `FLOW_CODEX_STABLE_HOME=/home/li/.codex-next`, a Codex next home
  `/home/li/.codex-next-<hash>`, model lists written in, and
  `Requires = codex-remote-control.service`.
- `flow-message-next.nix` (2026-09-30): sets `HOME=/home/li/.local/state/flow-next`,
  `CLAUDE_CONFIG_DIR=/home/li/.claude`, `CODEX_HOME=/home/li/.codex`,
  `FLOW_SOURCE_ROOT=/home/li/primary`, and literal `/nix/store/…` paths for
  herdr 0.8.2, harness 0.3.4, codex 0.153.4, claude-code 2.1.284, and an
  `ExecStart` on a literal store path.
- `curriculum.nix` (2026-10-07): exports
  `/git/github.com/LiGoldragon/{psyche,mind,field}-skills/skills`.
- `default.nix` (2026-09-30): Codex project trust lists `/home/li/primary`
  and other `/home/li/...` paths.
- `field-monitoring.nix`: patches `/home/li/...` constants out of a
  script and exposes a `primaryRoot` option. This is the one module seen
  that turns a host path into an option.
- `harness.nix` (2026-10-03): a `harness-daemon` user service and
  `harness`, `harness-usage`, `meta-harness` clients from
  `/git/github.com/LiGoldragon/harness` (repo tip 2026-10-03; it also ships
  `flow-id`). Sockets are relative to `XDG_RUNTIME_DIR`, which is portable.
- Also present: `herdr.nix`, `messenger-clj.nix`, `codex-next.nix`,
  `codex-next-candidate.nix`, `codex-remote-control.nix`,
  `opencode-harness.nix`, plus checks under `checks/` (herdr-server,
  flow-id, codex-next, flow-message-next, and others). Not run here.
- Installed binaries observed on this host: `herdr`, `claude`, `codex`,
  `codex-next`, `flow-id`, `curriculum` in `~/.nix-profile/bin`; `hm-send`,
  `hm-register`, `flow`, `flow-meta` in `~/.local/bin` as home-manager
  links.

### 2.3 Test repositories (Witnessed)

- `/git/github.com/LiGoldragon/flow-test` (tip 2026-10-10): pure NixOS-VM
  checks of the Flow Nexus with headless Herdr, no credentials, plus one
  live runner `packages/flow-claude.nix`. The runner refuses unless
  `FLOW_TEST_LIVE=1`, copies only `~/.claude/.credentials.json` (the
  subscription OAuth file) into a `mktemp` root, and uses
  `cheapestModel.claude = "haiku"` (lib/default.nix:19-22). Its header:
  "It needs the living's Claude login and the network, so it is a runner,
  never a check".
- `/git/github.com/LiGoldragon/persona-test` (tip 2026-09-27): README and
  `lib/default.nix:36-50` define the semi-sandbox: only Claude's
  `.credentials.json` and Codex's `auth.json` are copied; configs are
  generated from the login's non-secret `oauthAccount` fields.
- Neither test repo has an API-key path for Claude or Codex.

### 2.4 The API-key route that exists (Witnessed)

`tools/third-seat/` (2026-09-14): OpenCode against Fireworks Kimi K3, or
OpenRouter pinned to Fireworks. The provider runner reads the key only
from a file descriptor ≥ 3, refuses `*_API_KEY` in the environment, and
both descriptors are committed with `access_authorized:false`, so it
cannot make a provider request. It is a third-seat evaluation, not a
Claude or Codex test route.

### 2.5 Further machine bindings

Witnessed by this flow (files read and process listing):

- `codex-remote-control.nix` lines 18-25 apply only when the user is `li`
  with home `/home/li` (or `bird` on a Max node).
- `flow.nix` asserts `config.home.username == "li"`, with the message
  "Flow Nexus currently uses fixed li/1001 state and socket paths; it
  cannot be enabled for another user".
- `herdr.nix:156` declares `server.enable`; no module in CriomOS-home or
  CriomOS sets it. The running `herdr server` (pid 4957) is the
  hand-started one the module comment describes; handing it to the
  declared service "closes every pane".
- `codex-next.nix:34-36` copies `auth.json` and `config.toml` from
  `~/.codex` into the next home. Nothing creates the first login.
- The Flow repo's own launcher,
  `/git/github.com/LiGoldragon/flow/crates/flow-nexus/src/herdr/launch.rs`,
  passes `--dangerously-skip-permissions` (line 141) and `--remote-control`
  (line 150): Flow carries a Herdr launch path of its own beside the
  `tools/` scripts.

Claims from a read-only survey subflow of this flow (it read the code on
2026-10-10; this flow did not re-observe these):

- `tools/field-flow-preflight.mjs:14` defaults to
  `/home/li/.local/bin/flow-nexus`, which does not exist.
- `tools/reap-flow:29` fixes `ROOT = /home/li/primary`, not overridable.
- `reaper`, `reap-flow` and others default to registry
  `~/.local/state/hacky-messenger`; messenger-clj defaults to
  `~/.local/state/messenger-clj`; both directories exist.
- `tools/opencode-main-flow-launch.mjs` and the CLI of
  `tools/claude-native-seat-refresh.py` refuse to launch and point to
  `native-voice-launch.mjs`.
- `tools/flow-message-sandbox/` is the only live end-to-end test; it runs
  on the living's logins and needs the Claude folder-trust prompt
  answered once by hand.
- The harness repo reads `~/.claude/.credentials.json` to query
  `api.anthropic.com/api/oauth/usage` (`src/usage/home.rs:30`,
  `claude_quota.rs:22`).
- No module sets `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` for Claude or
  Codex.
- `field-census` and `field-checkup` units use
  `WorkingDirectory=/home/li/primary`.

## 3. Gaps

Vision silent (Inferred from the records found):

1. No record says what "redeployable" covers: another of the living's
   hosts, another user on this host, or another person's setup.
2. No record says how an API key for tests is obtained, stored, or
   budgeted. The billing record (2026-09-14) asks the question; none
   answers it. Which provider (Anthropic, OpenAI, OpenRouter) is unnamed.
3. "We're going to figure out a way to handle subscriptions": no record
   settles how a subscription login reaches a test host or VM beyond
   "copy only the credential files", nor what happens on token rotation
   (`flows/3ec648/vision/capsule.md` leaves it open).
4. Whether the meta-harness tests should run as Nix checks (no network)
   or only as live runners is not ruled; flow-test and persona-test chose
   "runner, never a check" for anything with a login.
5. No record says where the launcher code should live (Primary `tools/`,
   the Flow repo, or the harness repo), or whether `tools/*.mjs` is
   interim until Flow's `Start` replaces it.

Tooling short of vision (Witnessed facts, gap judged by this flow):

6. Launching is done by Primary scripts, not by Flow's `Start.{ Voice
   Capsule }` as `vision-flow` and the 2026-09-19 record ask.
7. Model names are written by hand in `native-voice-profiles.mjs` and in
   `native-main-flow-launch-shared.mjs`, against "declared once in Flow
   [...] a launcher never writes one by hand".
8. The launchers are not packaged by Nix; they need this Primary checkout
   at `/home/li/primary`, Herdr session `default`, and the living's
   `~/.claude`, `~/.codex*` logins.
9. CriomOS-home Flow modules hard-code `/home/li/...`, `/git/...` paths and
   literal store paths, against "Anything that differs between setups
   [...] must be a skill variable" and against redeployability. Only
   `field-monitoring.nix` turns its root into an option.
10. No Claude or Codex test runs on an API key; every live runner copies
    the subscription credential file. The order prefers an API key for
    full tests.
11. The Capsule's volatile-key encryption is a later design; credentials
    are copied as plain files into a temporary root today.
12. Two launch paths exist side by side: `tools/*-main-flow-launch.mjs`
    and Flow's `launch.rs`. Neither record nor code says which one a
    redeployed setup uses.
13. Bootstrap steps are manual: the Herdr server is hand-started, the
    first Claude and Codex logins are made by hand, and the Flow Nexus and
    Codex remote modules refuse any user but `li`.
14. Not checked here: whether the launcher tests and the CriomOS-home
    checks pass, and whether the deployed Flow Nexus can launch a seat at
    all. These need a test run.

## Sources

- `flows/d68c82/vision/metaHarness.md`, `flows/9519a1/vision/metaHarness.md`, `flows/875960/vision/harness.md`
- `flows/7328f4/vision/metaHarness.md`, `flows/6997eb/vision/metaHarness.md`, `flows/bd0019/vision/metaHarness.md`, `flows/fe945a/vision/metaHarness.md`, `flows/1a6ca4/vision/personaMetaHarness.md`
- `flows/b81560/vision/operational-flowCLIStartsSessions.md`, `flows/af762b/vision/operational-flowOwnsHerdr.md`, `flows/752e0f/vision/herdrSessions.md`, `flows/d8df70/vision/flowTool.md`, `flows/fd0f97/vision/launch.md`, `flows/da1e3f/vision/operational-launcher.md`, `flows/108ab0/vision/operational-flowDatomLauncherLanguage.md`, `flows/9993b5/vision/workspaceProvisioning.md`, `flows/e51411/vision/launch.md`, `flows/b05237/vision/operational-criomosModularHardware.md`
- `flows/445410/vision/deployment.md`, `flows/01a01a93/vision/hostEnvironmentRecovery.md`, `flows/e167d8/vision/deployment.md`, `flows/d4ae97/vision/deployment.md`, `flows/7dc7cc/vision/redeploying-the-operating-system-after-a-user-is-deployed.md`
- `flows/91ea9f/vision/testing.md`, `flows/3ec648/vision/capsule.md`, `flows/e167d8/vision/testRepos.md`, `flows/6cc91b/vision/sandbox.md`, `flows/6cc91b/vision/billing.md`, `flows/024bc7/vision/sandbox.md`, `flows/bcd02a/notion/sandbox.md`, `flows/e1953c/vision/secrets.md`, `flows/1b8ac0/vision/flowNexus.md`, `flows/f38926/vision/operational-openCodeRemoteAccess.md`, `flows/e51411/notion/v2.md`
- Authored skills under `/git/github.com/LiGoldragon/psyche-skills/skills`: `vision-flow.md`, `vision-model-roles.md`, `vision-nexus.md`, `vision-deployment.md`, `intent-testing.md`
- `/home/li/primary/tools/` launch files listed in 2.1
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/` modules listed in 2.2
- `/git/github.com/LiGoldragon/flow-test`, `/git/github.com/LiGoldragon/persona-test`, `/git/github.com/LiGoldragon/harness`, `/git/github.com/LiGoldragon/flow/crates/flow-nexus/src/herdr/launch.rs`
- Survey subflow of this flow, read-only, 2026-10-10 (its claims are marked in 2.5)
- Provenance receipt: unavailable; no receipt handoff exists for this survey.
