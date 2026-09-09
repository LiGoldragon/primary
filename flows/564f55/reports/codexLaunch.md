# Codex remote launch — investigation

Flow 564f55. Subflow report. Design only: no Codex session was started, no
window was opened deliberately (one accidental exception is disclosed in
§7). Every claim below is marked **witnessed** (I ran it or read the file)
or **read** (documentation or another flow's record, not re-verified here).

---

## 1. What "Codex remote" is here

**Installed version (witnessed):** `codex-cli 0.153.4`, at
`/home/li/.nix-profile/bin/codex` →
`/nix/store/wdj0sc69r4n9is1idfb32vcx5739ijkh-codex-0.153.4/bin/codex`
(a bubblewrap PATH wrapper around `.codex-wrapped`).

There are **two different things** called remote, and only one of them
satisfies both of the living's conditions.

### 1a. Codex Cloud — does *not* satisfy (b)

**Witnessed** (`codex cloud --help`): `[EXPERIMENTAL] Browse tasks from
Codex Cloud and apply changes locally`, with `exec`, `status`, `list`,
`apply`, `diff`. `codex cloud exec --env <ENV_ID> [QUERY]` submits a task
that runs on OpenAI's infrastructure. There is no local TUI for it — you
poll with `status` and pull the result with `apply`. It also requires an
`--env` id that must already exist on the OpenAI side. **No prior flow has
ever used `codex cloud`** (witnessed by the flows search). Rejected.

### 1b. Remote Control over the app-server — satisfies (a) and (b)

The app-server daemon holds the session; the ChatGPT/Codex mobile and web
clients attach to it over an OpenAI-brokered websocket (that is the
"visible on the OpenAI side" half), and a local TUI attaches to the *same*
daemon over a unix socket (that is the on-screen half). One thread, two
attached clients.

**The generic CLI surface (witnessed, `codex remote-control --help`):**

```
codex remote-control start   Start the app-server daemon with remote control enabled
codex remote-control stop    Stop the app-server daemon
codex remote-control pair    Create and print a short-lived manual pairing code
```

and lower level (witnessed, `codex app-server daemon --help`):
`bootstrap`, `start`, `restart`, `enable-remote-control`,
`disable-remote-control`, `stop`, `version`.

**Top-level TUI flags (witnessed, `codex --help`):**

```
--remote <ADDR>                 Connect the TUI to a remote app server endpoint.
                                Accepted forms: `ws://host:port`, `wss://host:port`,
                                `unix://`, or `unix://PATH`.
--remote-auth-token-env <ENV_VAR>
-C, --cd <DIR>                  Tell the agent to use the specified directory as its working root
[PROMPT]                        Optional user prompt to start the session
```

`--remote` is also accepted by `codex agents` and `codex queue`.

### 1c. **On this host the daemon is already running and Nix owns it**

This is the single most important finding, and it overrides the generic
`codex remote-control start` recipe.

**Witnessed live:**

```
$ systemctl --user is-active codex-remote-control.service
active
$ systemctl --user show codex-remote-control.service -p ExecStart -p MainPID
MainPID=326495
ExecStart={ ... argv[]=/nix/store/wdj0sc69r4n9is1idfb32vcx5739ijkh-codex-0.153.4/bin/codex \
            app-server --remote-control --listen unix:// ; ... }
$ ls -la /home/li/.codex/app-server-control/
srw------- 1 li users 0 Sep  8 17:45 app-server-control.sock
```

Declared at
`/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix:158`
(`Restart=always`, `UMask=0077`).

A wrapper already exists — **witnessed**, `/home/li/.nix-profile/bin/codex-remote`:

```
exec /nix/store/wdj0sc69r4n9is1idfb32vcx5739ijkh-codex-0.153.4/bin/codex --remote unix:// "$@"
```

declared at `/git/github.com/LiGoldragon/CriomOS-home/owned-agents/codex/remote.nix`.

**Do not run `codex remote-control start` on this host.** Flow 01a03f49
established this (`flows/01a03f49/reports/codexPhoneRemoteControl.md:60-63`,
**read**): that path expects
`$CODEX_HOME/packages/standalone/current/codex` and bootstraps an
installer-owned updater, fighting the Nix-owned lifecycle. The realized
shape is the systemd service above.

**Attachment gotcha (read, `codexPhoneRemoteControl.md:44-48`):** *"A plain
TUI launched before the daemon uses an embedded app-server. No attach,
rebind, or conversion command exists. Starting Remote Control afterward
makes another process try to load the thread, producing the intentional
`already has an active writer` rejection."* — so the session **must be
started with `--remote` from the very first invocation**. A plain `codex`
in a ghostty window can never be made remote afterward.

**Pairing** is a one-time human act: `codex remote-control pair --json`
prints a short-lived code the living enters in the ChatGPT app under "Pair
manually". Flow 01a03f49 recorded a live proof (`:53-58`, **read**): phone
paired, `codex --remote unix://` TUI stayed open, and a message sent from
the phone appeared in that same live terminal conversation. **Not witnessed
by me** — whether that enrollment is still valid today is unknown, and
`remote control requires ChatGPT authentication; API key auth is not
supported` is a string in the binary (witnessed).

**Unwitnessed and load-bearing:** whether the positional `[PROMPT]` is
auto-submitted (versus pre-filled in the composer) when combined with
`--remote`. Verifying it requires starting a session, which this subflow
must not do.

---

## 2. How Codex loads skills

### The `$skill` syntax is real and comes from Codex's own base instructions

**Witnessed** by extracting the base-instruction template out of the
binary (`strings` over `.codex-wrapped`):

> ## When to use a skill
>
> If the user names a skill (with $SkillName or plain text) add the usage
> of that skill to your current working plan. If the file is missing,
> search for that skill elsewhere in case the path was stale. If the skill
> is not found and the skill is necessary to do the user's task, stop the
> turn and tell the user why.

So `$name` is not a parser directive — it is an instruction to the model,
which then reads `SKILL.md` from disk. Skill *metadata* (name +
description) is always in context; the body is read on selection
(progressive disclosure).

### Where they are read from

**Witnessed** in the binary's path literals: the discovery roots are the
`skills` subdirectory of `.codex` and of `.agents`, plus
`$CODEX_HOME/skills`. The concatenated literal
`hooks.json` `.codex` `.agents` `skills` `agents` `plugins` appears
together in the plugin/discovery blob.

- `/home/li/primary/.codex/` — **witnessed**: contains only `agents/`
  (9 role `.toml` files). **No skills here.**
- `/home/li/primary/.agents/skills/` — **witnessed**: 44 skill directories,
  each a single `SKILL.md` with `description:` and `dependencies:`
  frontmatter. **This is the tree Codex reads for primary.**
- `/home/li/.codex/skills/.system/` — **witnessed**: 6 OpenAI-shipped
  skills (`skill-creator`, `skill-installer`, `openai-docs`, …).

The 44 names, all invocable as `$name`: agent-harness-packaging, beads,
behavior, breaking-upgrades, claude-harness, codex-harness,
context-strata, correction, datom, deepseek-harness, design, disk-hygiene,
documentation-placement, edit-coordination, ethos, feature-development,
file-editing, flow-evidence, lojix, main-feature-integration, main-flow,
nexus, nexus-rationale, nix-input-upgrade, nix-workflow, operating-system,
orchestrate, prompt-crafting, protos, psyche, psyche-acquisition,
psyche-distillation, psyche-grasp, psyche-interraction, realization,
repository-lifecycle, secrets, skill-designing, spirit, subflow, testing,
transcript-search, versioning, vocabulary.

### How to guarantee a set is loaded at start

**In the prompt, and that is the established practice here.** Witnessed in
`/home/li/.codex/history.jsonl`: the living's own Codex prompts open with a
bare `$name` list, e.g. verbatim —

```
$main-flow $spirit $psyche $psyche-interraction $behavior $correction
 $vocabulary $edit-coordination $flow-evidence $beads $orchestrate
 $feature-development $main-feature-integration $testing $nix-workflow
 $operating-system $lojix
```

Tally across that history (witnessed): `$spirit` 85, `$psyche-interraction`
83, `$realization` 59, `$psyche` 39, `$behavior` 39, `$main-flow` 31,
`$edit-coordination` 27, `$testing` 16 …

Corroborating witness — `/home/li/.codex/session_index.jsonl` contains a
row whose `thread_name` is literally
`"$main-flow $spirit $psyche $psyche-i"`, i.e. the thread name is derived
from the opening characters of the first prompt. **Useful consequence: the
main flow can identify the launched thread by that name.**

Via config there is a second, weaker lever: `developer_instructions` in
`~/.codex/config.toml` (witnessed — it currently carries a skill-read
de-duplication rule), and an app-server RPC `skills/extraRoots/set` plus
a `skills.*` config table (witnessed as string literals; exact TOML key
shape not witnessed). Neither *forces* a skill to be read. **Recommendation:
put the list in the prompt; do not touch config.**

`AGENTS.md` reinforces persistence — **witnessed**,
`/home/li/primary/AGENTS.md`: *"Skills loaded by the user (with
$skill-name) are to be applied for your entire session, not only for a
single turn."*

---

## 3. Opening a ghostty window with a command and a cwd

**Witnessed:** ghostty 1.3.1 at `/home/li/.nix-profile/bin/ghostty`;
compositor is **niri 26.04** on Wayland (`pgrep -a niri` →
`/nix/store/…-niri-26.04/bin/niri --session`; `NIRI_SOCKET`,
`WAYLAND_DISPLAY=wayland-1`, `XDG_RUNTIME_DIR=/run/user/1001`).

Ghostty is enabled at
`/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix:538`
with no `settings`, so home-manager writes no ghostty config; the live
files are the hand-edited `/home/li/.config/ghostty/config` and
`/home/li/.config/ghostty/config.ghostty`, the latter rewritten at runtime
by chroma (template at `min/chroma.nix:104-116`).

### Flags (witnessed, from `ghostty --help`, `ghostty +show-config --default --docs`, and the shipped desktop entry)

| need | flag |
|---|---|
| run a command | `-e <command> [args…]` — **must be last**; everything after is the argv |
| working directory | `--working-directory=/abs/path` |
| title | `--title='…'` |
| app id (what niri window rules match) | `--class=…` |
| own process/window | `--gtk-single-instance=false` |
| keep window after exit | `--wait-after-command` |

`com.mitchellh.ghostty.desktop` names them canonically: `X-TerminalArgExec=-e`,
`X-TerminalArgTitle=--title=`, `X-TerminalArgAppId=--class=`,
`X-TerminalArgDir=--working-directory=`, `X-TerminalArgHold=--wait-after-command`.

**`--gtk-single-instance=true` is wrong for this job.** The singleton
serves the request over DBus and the new window inherits *the singleton's*
cwd, not the caller's — this is documented in the niri module's own comment
(`min/niri.nix:325`). Ghostty's own docs also warn that a custom `--class`
with single-instance creates separate instances and can break DBus
activation. Use `--gtk-single-instance=false`.

### Does the window stay open after the command exits?

**No.** Witnessed default from this binary
(`ghostty +show-config --default --docs`):

```
# If true, keep the terminal open after the command exits. ...
wait-after-command = false
```

and `grep -rn` for `wait-after-command` / `confirm-close-surface` /
`shell-integration` across both CriomOS repos and both live config files
returns nothing — so the default applies. **Pass `--wait-after-command`
explicitly** if the living is to find the transcript on screen.

### The established spawn pattern to copy

`/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/niri.nix:28-45`,
the rescue terminal — **witnessed**:

```
unit="criomos-rescue-terminal-$(date +%s%N)-$$"
exec systemd-run --user --scope --collect --quiet \
  --unit="$unit" \
  --property=CPUWeight=1000 --property=IOWeight=1000 \
  --property=MemoryAccounting=yes --property=MemoryLow=256M \
  --property=MemoryHigh=2G --property=OOMPolicy=continue \
  ghostty --gtk-single-instance=false \
    --class=criomos-rescue-terminal --title='CriomOS Rescue Terminal'
```

with a matching niri window rule at `niri.nix:275-280` (`open-focused = true`).
There is also a precedent for routing an agent's window to its own
workspace by app-id (`^org\.criome\.AgentTestWindow$`,
`open-on-workspace = "criomos-agent-tests"`, `niri.nix:271-276`).

`min/terminal-scopes.nix` already writes
`~/.config/systemd/user/app-ghostty-.scope.d/oom-policy.conf` with
`[Scope] OOMPolicy=continue`, which covers singleton surfaces; a
`systemd-run --scope` of our own sets its own `OOMPolicy=continue`.

### Reaching the desktop from a headless agent shell

`systemctl --user show-environment` (witnessed) already carries `DISPLAY=:0`,
`WAYLAND_DISPLAY=wayland-1`, `NIRI_SOCKET`, `XDG_CURRENT_DESKTOP=niri:GNOME`,
imported at session start by `criomos-sync-session-environment`
(`niri.nix:135-142`). `systemd-run --user --scope` inherits it, which is
the robust route.

---

## 4. What prior flows already did

**Flow 1a6ca4** launched every Codex flow so far (`flows/da223f` and
`flows/84eb1e` are the Codex-side lanes it created). It used **`codex exec`,
never the TUI, never remote**. Representative (from 1a6ca4's transcript,
**read**):

```
codex exec -m gpt-6-astra -c model_reasoning_effort=xhigh \
  --dangerously-bypass-approvals-and-sandbox -C /home/li/primary \
  -o $S/astraRewriteLast.md "$(cat $S/astraRewritePrompt.txt)" \
  < /dev/null > $S/astraRewrite.log 2>&1
```

Gotchas it recorded, all still relevant:

- **stdin must be closed.** `flows/1a6ca4/log.md:68` — both audits sat 40
  minutes on *"Reading additional input from stdin"*. Only applies to
  `codex exec`; a TUI owns its tty. The proposed line for the codex-harness
  skill was **never landed** (witnessed: `.agents/skills/codex-harness/SKILL.md`
  is 30 lines and says nothing about `exec` or stdin).
- **The Claude harness kills background Codex runs under memory pressure**
  when they are a `systemd-run --scope` child of the harness shell; the
  `--unit` *service* form survived (`log.md:72-73`, landed in
  `.agents/skills/claude-harness/SKILL.md:37-42`). A ghostty window is not
  a harness child, so this does not apply to the launch script — but it is
  why the script should not be run in the foreground of a Claude turn.
- **Provider capacity** (`gpt-6-astra` "at capacity") and Codex's **agent
  thread limit**, plus two safety-layer refusals of robustness work phrased
  in terms of aborts/recursion/untrusted input (`log.md:75,:80`).
- **Ghostty scope OOMPolicy**: an unbounded test binary OOM-killed inside
  `app-ghostty-surface-transient-*.scope` (`OOMPolicy=stop`) took the whole
  scope and the harness with it (`flows/1a6ca4/reports/harnessExit.md:28-29`).

**No prior flow has opened a ghostty window to run an agent.** Two
near-misses: flow 4a8046 launched a disposable ghostty running `cat` as a
transcription receiver and its *first attempt failed on an invalid separate
`--title` argument, producing a Configuration Errors window*
(`flows/4a8046/witnesses/live-wispr.md:22`) — use `--title=…` in one token.
And `sessions/realization/2026-08-18T152526.md:25` records a
`ghostty +new-window --help` probe that opened a real window, after which
all runtime ghostty invocation was stopped.

**Remote control was investigated in full by flow 01a03f49**
(`flows/01a03f49/reports/codexPhoneRemoteControl.md`) and realized as the
Nix service in §1c. `flows/7fba5f/reports/codexReportLoop.md:37`: *"Remote:
codex-remote-control.service runs `codex app-server --remote-control` on a
unix socket, and the TUI attaches only to it. That is the living's remote
path to Codex."*

**Prompt convention (witnessed in 1a6ca4's transcript):** heredoc a prompt
file into scratch, pass it as the positional argument via `"$(cat …)"`.
The identity block (`FLOW_ID=`, `FLOW_DIRECTORY=`) appears **only in
subflow prompts**; main-flow prompts omit it so the Codex flow claims its
own lane through `$main-flow`.

---

## 5. Draft launch script — NOT INSTALLED, NOT RUN

Design only. It has never been executed; nothing below is witnessed
behaviour of the script itself.

```bash
#!/usr/bin/env bash
# codex-flow-window — open a ghostty window running an interactive Codex TUI
# attached to the Nix-owned remote-control app-server, seeded with a prompt.
#
#   codex-flow-window <prompt-file> <working-directory> [title-suffix]
#
# Not installed. Draft for flow 564f55.

set -euo pipefail

promptFile=${1:?usage: codex-flow-window <prompt-file> <working-directory> [title]}
workDir=${2:?usage: codex-flow-window <prompt-file> <working-directory> [title]}
title=${3:-Codex realization}

[ -r "$promptFile" ] || { echo "prompt file not readable: $promptFile" >&2; exit 2; }
[ -d "$workDir" ]    || { echo "working directory not a directory: $workDir" >&2; exit 2; }

# The daemon is Nix-owned. Never `codex remote-control start` on this host.
if ! systemctl --user is-active --quiet codex-remote-control.service; then
  echo "codex-remote-control.service is not active; start it with" >&2
  echo "  systemctl --user start codex-remote-control.service" >&2
  exit 3
fi

socket="${CODEX_HOME:-$HOME/.codex}/app-server-control/app-server-control.sock"
[ -S "$socket" ] || { echo "app-server control socket missing: $socket" >&2; exit 3; }

prompt=$(cat "$promptFile")

unit="codex-flow-window-$(date +%s%N)-$$"

exec systemd-run --user --scope --collect --quiet \
  --unit="$unit" \
  --property=CPUWeight=1000 \
  --property=IOWeight=1000 \
  --property=MemoryAccounting=yes \
  --property=MemoryLow=512M \
  --property=OOMPolicy=continue \
  ghostty \
    --gtk-single-instance=false \
    --class=criomos-codex-flow \
    --title="$title" \
    --working-directory="$workDir" \
    --wait-after-command \
    -e codex-remote --cd "$workDir" "$prompt"
```

Notes on each choice, and what is *not* witnessed:

- **`codex-remote`** expands to `codex --remote unix:// "$@"` (witnessed).
  Using it from the first invocation is mandatory — a plain `codex` cannot
  be attached to the daemon afterward (§1b).
- **`--cd "$workDir"`** duplicates ghostty's `--working-directory` on
  purpose: the former sets the *agent's* working root, the latter the
  shell/process cwd. **Unwitnessed:** whether `--cd` is honoured when
  `--remote` is in play; `codex agents --cd` is documented as *"Use this
  directory for new tasks on a remote server"*, which suggests yes.
- **The prompt as the positional argument.** **Unwitnessed:** whether the
  TUI auto-submits it or pre-fills the composer. If it merely pre-fills,
  the living presses Enter — acceptable either way. It does **not** block
  the main flow from talking to the session (§5a).
- **`-e` is last** and takes a bare argv — no shell, so no quoting hazard
  around the prompt beyond the one `exec` layer. **Unwitnessed:** whether a
  multi-kilobyte prompt as a single argv element is accepted by ghostty's
  `-e` and forwarded intact; `ARG_MAX` is far larger, but ghostty's own
  parser has not been tested with it. **If this proves fragile, the
  fallback is `-e sh -c 'exec codex-remote --cd "$1" "$(cat "$2")"' sh
  "$workDir" "$promptFile"`, which keeps the prompt on disk.**
- **`--wait-after-command`** because the default is `wait-after-command =
  false` (witnessed) and the window would otherwise vanish when Codex exits.
- **`--gtk-single-instance=false`** because the singleton would ignore our
  cwd (witnessed, `niri.nix:325` comment) and because a custom `--class`
  with the singleton is documented as breaking DBus activation.
- **`--title=` as one token** — flow 4a8046 hit a Configuration Errors
  window from a separated `--title` argument.
- **`systemd-run --user --scope`** gives the window its own cgroup with
  `OOMPolicy=continue`, matching the rescue terminal and avoiding the
  `harnessExit.md` failure mode. It also inherits the imported Wayland
  environment, so the script works from a headless agent shell.
- **Model and sandbox are left to config** — `~/.codex/config.toml` already
  sets `model = "gpt-6-astra"`, `model_reasoning_effort = "xhigh"`,
  `approval_policy = "never"`, `sandbox_mode = "danger-full-access"`
  (witnessed). No `--dangerously-bypass-…` flag is needed or wanted in an
  interactive session where the living is watching.
- **A niri window rule** would be the natural companion, matching
  `app-id = "^criomos-codex-flow$"` with `open-focused = true`, modelled on
  the rescue-terminal rule. That belongs in
  `CriomOS-home/modules/home/profiles/min/niri.nix`, not in the script.
- **Pairing is a human step.** If the ChatGPT-side enrollment has lapsed,
  the living runs `codex remote-control pair --json` and enters the code in
  the ChatGPT app. Whether it is currently enrolled was **not witnessed** —
  checking it means talking to the daemon.
- **Placement, when it is installed:** as a `writeShellScriptBin` in
  `CriomOS-home` beside `criomos-rescue-terminal`, not as a loose file.

### 5a. Does passing the prompt interfere with the main flow talking to the session?

No — and it helps. **Witnessed** (`codex queue --help`):

```
codex queue --thread <THREAD> --message <TEXT>   # Session UUID or exact session name
```

`--remote <ADDR>` is accepted here too, so the main flow reaches the same
daemon. The thread is identified either from
`~/.codex/session_index.jsonl` (witnessed: rows are
`{"id":…,"thread_name":…,"updated_at":…}` and `thread_name` is derived from
the opening characters of the first prompt) or by browsing `codex agents`.
Since the prompt's first line is the `$skill` list, the thread name is
predictable. Passing the prompt therefore makes the session *easier* to
address, not harder.

---

## 6. Draft prompt shape

The realization flow continues 564f55's identity, so it is a **subflow**
prompt and carries the identity block. Note that `$realization` declares
`dependencies: [main-flow, psyche-interraction, testing]` (witnessed in
`.agents/skills/realization/SKILL.md`), and it is marked `user-only: true`
— **the living should confirm whether this flow claims its own lane
(`$main-flow`, no identity block) or writes into flows/564f55
(`$subflow` + identity block).** The draft takes the second reading, per
the brief.

Skills, all verified present in `/home/li/primary/.agents/skills/`:
`subflow spirit behavior psyche psyche-acquisition psyche-interraction
realization datom protos ethos nexus vocabulary edit-coordination
orchestrate feature-development repository-lifecycle versioning testing
file-editing nix-workflow flow-evidence`.

`$repository-lifecycle` is included because the derive crate does not exist
yet (witnessed: `/git/github.com/LiGoldragon/datom-codec` has no derive
crate; `Cargo.toml` is a single `[package]`, not a workspace).

```
$subflow $spirit $behavior $psyche $psyche-acquisition $psyche-interraction
 $realization $datom $protos $ethos $nexus $vocabulary $edit-coordination
 $orchestrate $feature-development $repository-lifecycle $versioning
 $testing $file-editing $nix-workflow $flow-evidence

FLOW_ID=564f55. FLOW_DIRECTORY=/home/li/primary/flows/564f55.

Realize the distillation the living approved in flow 564f55 on 2026-09-09
("Okay, then the proposal is good, and land it all"). The approved
statements and the amendments to them are in FLOW_DIRECTORY/log.md; the
distilled records are the authority for what to build.

Acquire the vision yourself before writing code:
  /home/li/primary/Vision/protos.md
  /home/li/primary/Vision/datom.md
  /home/li/primary/Vision/ethos.md
  /home/li/primary/Intent/data.md
  /home/li/primary/Intent/mandatoryTraits.md
  /home/li/primary/Intent/protosParsing.md
  FLOW_DIRECTORY/vision/signal.md, sema.md, nexus.md, datom.md, protos.md,
    ethos.md, designPractice.md
  FLOW_DIRECTORY/notion/datom.md — notion, not vision: it rules nothing.

The amendments the living made to the proposal, which the distilled records
must already carry and the code must honour: string, not text, everywhere;
the migration statement dropped; the error example without parentheses
(Value.x); named-type variants split into two contextualized statements;
every declared struct and enum derives both kinds, with aliases inheriting;
the datom derives conditional on a feature that the CLI enables and the
Nexus does not; and the careful wording of "type" about Protos.

Repositories you change:
  /git/github.com/LiGoldragon/protos        (main, 0.26.0)
  /git/github.com/LiGoldragon/datom-codec   (main, 0.21.0)
  /git/github.com/LiGoldragon/ethos-zero    (main, 5.0.0)
  a new datom-codec derive crate, which does not yet exist.

Land on main with the gates green, bump versions as the versioning skill
rules, and re-pin consumers. Write your report in FLOW_DIRECTORY/reports/.
```

**On what the prompt deliberately omits** (per `$prompt-crafting`,
witnessed: *"A prompt explains nothing the harness does automatically and
nothing everybody knows … A prompt states decisions and asks for an
outcome; the receiving flow determines the mechanism"*): no build commands,
no repository layout, no mechanism for the derive crate, no instruction to
dispatch subflows. Compare `astraRewritePrompt.txt` from flow 1a6ca4, which
the living ruled deliberately minimal.

**Corrections to the brief's own list, witnessed:**

- `Vision/signal.md` **does not exist**. `Vision/` holds datom.md,
  distillation.md, ethos.md, ethosMonolith.md, flowNexus.md,
  highLevelView.md, nexus.md, orchestrate.md, protos.md, remembering.md,
  x11.md, and `sources/`. The signal record is
  `flows/564f55/vision/signal.md` (15 lines). Flow 564f55's own log records
  this: *"no Vision/signal.md or Vision/sema.md exists"*.
- `Intent/*.md` is exactly three files: data.md, mandatoryTraits.md,
  protosParsing.md.
- There is no `$nexus` **Ethos kind** — flow f426777b ruled nexus and sema
  kinds undesigned. The `$nexus` skill is included for reading only, since
  the feature gate distinguishes the CLI from the Nexus.
- A prior joint checkout for protos and datom-codec exists at
  `/home/li/primary/flows/da223f/joint.0jZ7PT/` and is currently dirty
  (witnessed: `git status` shows both as modified submodule entries).
  The realization flow should take its own checkout under
  `$feature-development` rather than inherit that one.

---

## 7. What could not be witnessed, and one disclosure

**Not witnessed, by design:**

- No Codex session was started. Whether the positional `[PROMPT]` is
  auto-submitted under `--remote`, whether `--cd` is honoured under
  `--remote`, and whether the ChatGPT-side pairing is currently enrolled
  all require starting one.
- The draft script was never executed. Its ghostty flags are each
  individually witnessed from `ghostty --help`, `+show-config --default
  --docs`, and the shipped desktop entry, and its systemd-run shape is
  copied from the working rescue terminal — but the composition is
  untested. In particular the size limit on a prompt passed through
  `ghostty -e` as one argv element is unknown; §5 gives the on-disk
  fallback.
- `codex remote-control pair` was not run; doing so would mutate enrollment.

**Disclosure.** The delegated read agent investigating ghostty ran
`ghostty +new-window --help` expecting help text. `+new-window` does not
honour `--help`; it sends a D-Bus request to the running singleton, and a
real window opened (a new `app-ghostty-surface-transient-710631.scope`
appeared). Nothing was written or configured, but a stray ghostty window is
open on the desktop and must be closed by hand (Mod+Q, or its close
button). This repeats the exact mistake recorded in
`sessions/realization/2026-08-18T152526.md:25`; the rule that ghostty's
`+`-commands are runtime actions, not queries, is not in any skill and
arguably should be.

---

## Sources

Witnessed on this machine (2026-09-09):

- `codex --version`, `codex --help`, `codex remote-control --help`,
  `codex remote-control start|pair --help`, `codex cloud --help`,
  `codex cloud exec --help`, `codex app-server --help`,
  `codex app-server daemon --help`, `codex agents --help`,
  `codex resume --help`, `codex queue --help`
- `strings` over
  `/nix/store/wdj0sc69r4n9is1idfb32vcx5739ijkh-codex-0.153.4/bin/.codex-wrapped`
  (base-instruction skill section; skill discovery path literals;
  app-server RPC method names)
- `/home/li/.codex/config.toml`, `/home/li/.codex/history.jsonl`,
  `/home/li/.codex/session_index.jsonl`, `/home/li/.codex/skills/.system/`,
  `/home/li/.codex/app-server-control/`
- `systemctl --user is-active|show codex-remote-control.service`,
  `systemctl --user show-environment`, `/home/li/.nix-profile/bin/codex-remote`
- `/home/li/primary/AGENTS.md`, `/home/li/primary/.agents/skills/` (44),
  `/home/li/primary/.codex/agents/`, `Vision/`, `Intent/`,
  `flows/564f55/{log.md,vision,notion,reports}`
- `/git/github.com/LiGoldragon/{protos,datom-codec,ethos-zero}/Cargo.toml`
- `ghostty --help`, `ghostty +show-config`, `+show-config --default --docs`,
  `com.mitchellh.ghostty.desktop`, `/home/li/.config/ghostty/{config,config.ghostty}`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/`:
  `niri.nix`, `default.nix`, `chroma.nix`, `agent-intercom.nix`,
  `terminal-scopes.nix`, `default-opener.nix`;
  `CriomOS-home/owned-agents/codex/remote.nix`;
  `CriomOS-home/checks/{ghostty-primary-selection,terminal-oom-policy}/`
- `pgrep -a niri`, `ls /run/user/1001`

Read, not re-verified here:

- `/home/li/primary/flows/01a03f49/reports/codexPhoneRemoteControl.md`
- `/home/li/primary/flows/1a6ca4/{log.md,reports/oomPolicy.md,reports/harnessExit.md}`
  and its transcript
  `/home/li/.claude/projects/-home-li-primary/1a6ca4f9-e0fa-4f2c-bd6f-a40651590354.jsonl`
- `/home/li/primary/flows/4a8046/witnesses/live-wispr.md`
- `/home/li/primary/flows/7fba5f/reports/codexReportLoop.md`
- `/home/li/primary/sessions/realization/2026-08-18T152526.md`
- [openai/codex app-server-daemon README](https://github.com/openai/codex/blob/main/codex-rs/app-server-daemon/README.md)
- [Codex CLI Remote Control and Mobile Pairing](https://codex.danielvaughan.com/2026/06/06/codex-cli-remote-control-mobile-pairing-app-server-v2-remodex/)
- [Codex CLI App Server: Remote Access, WebSocket Transport](https://codex.danielvaughan.com/2026/03/31/codex-cli-app-server-remote-websocket/)
- [Enable Codex remote control with only the Codex CLI](https://roboin.io/article/en/2026/08/19/enable-remote-control-using-codex-cli/)
