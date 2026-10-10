# Claude cloud remote server — psyche records, flow history, live state

Witnessed by subflow of flow 9e7c9f, 2026-09-12, on host Ouranos. Origin of
every claim is marked inline: **relayed** (from a flow's own log/report/
witness text, itself relaying the living or a prior flow), **verbatim** (the
living's own words, reproduced exactly), or **witnessed** (this subflow's own
direct observation on this machine, this session).

## 1. Raw psyche records

Search covered `flows/*/vision/`, `flows/*/notion/`, and `vision-raw/` under
`/home/li/primary` for every record touching Claude remote control, remote
session creation, the cloud remote server, and desktop access to sessions.
`flows/*/notion/` contained no matches. Every record found is reproduced
verbatim below. None of them have been distilled into `Vision/` — a
repo-wide search of `Vision/` for "remote control", "remote session", and
"cloud remote" found nothing; all remain raw.

### `flows/01a04524/vision/claudeRemoteControl.md`

Still raw (not in `Vision/`).

```
# Claude remote control

## Session 01a03f49 has the right design

On the target architecture for Claude remote control:

> session 01a03f49 has the right design for how we want to do this on codex side. try to aim for the same design with claude (see if its possible)

-- psyche, typed.

## The desktop app can access them

On accepting the supported Claude client boundary:

> but the desktop app can access them then? That would be acceptable.

-- psyche, typed.
```

### `flows/01a047d2/vision/remoteControl.md`

Still raw (not in `Vision/`).

```
# One server for everything

## Both Claude and Codex

> Keep working on the one server for everything solutions, both for Claude and codex

-- psyche, typed.

## Rooted in primary

> Yes, the code server should be rooted in primary.

-- psyche, typed.

## The server running for Codex and Claude

Context: clarification of "one server for everything"; this rules out the proposed Nexus/control-plane interpretation.

> I dont want to start a nexus for this; we just need the server running for codex and claude, and the desktop apps using it locally.

-- psyche, typed.
```

### `flows/db267d/vision/reminders.md`

Still raw (not in `Vision/`).

```
# Reminders

Context: asked for the cloud remote server to be taken out of CriomOS,
with reintroduction left to a later conversation, and then noted that
the deferral itself has nowhere to live.

> I don't know where we put reminders, but I guess we need a system for
> that.

-- psyche, STT.
```

No `log.md` accompanies this vision file inside `db267d/vision/`; the fuller
account of the same request lives in `flows/db267d/log.md` (part 2, below),
where the instruction is paraphrased by the flow itself, not quoted from the
living:

> Take the cloud remote server out of CriomOS. Reintroducing it is a
> later conversation.

This line in `log.md` is the flow's own instructions-received section, not
inside quote marks attributed to the living with "-- psyche" — it is
**relayed**, not a verbatim psyche record, and is included here only because
it is the operative instruction that produced the db267d removal.

### `flows/58a86d/vision/claudeDesktop.md`

Still raw (not in `Vision/`). Touches desktop access to Claude Code, not
remote-session creation specifically, but is one of the "desktop access to
sessions" records the brief asked to include.

```
# Claude desktop app

## 2026-09-05 — updated along with Claude Code; shenanigans to a bare minimum

Context: the living asked the flow to update the Claude desktop app, and to
find out whether the setup overrides the Claude Code the app uses internally
or lets the app download its own.

> It should be updated along with the Claude code. I believe it also uses Claude code internally. ... I would like to keep the amount of shenanigans down to a bare minimum

-- psyche, STT.
```

### `flows/01a057e7/log.md` and `flows/01a05833/annotations.md`

Neither contains a `## <heading>` / `> quote -- psyche` vision-style record.
`01a057e7/log.md` records a **correction of a speech-to-text error**, not a
verbatim psyche quote block, but it is directly on-subject and is reproduced
here for completeness (this is the flow's own prose, relaying the living, not
a quoted verbatim record):

> Correction source: the earlier prompt said, "Remember everything that has
> to do with the cloud server," which led to the mistaken subject. The
> intended words were "Claude Code." No authored skill produced the error.

Also from `01a057e7/log.md`, a later verbatim-style finding (the flow's own
witness prose, not a quote block) worth carrying forward for part 3:

> Correction from the living's current use: Claude Desktop does discover and
> control the locally running Remote Control owner. ... The remaining
> limitation is that the remote session does not expose the local session's
> `bypass permissions` choice.

`01a05833/annotations.md` concerns Bird's profile size (VSCodium extensions),
not Claude remote control; it contains no relevant record and is noted here
only to confirm the search covered it and found nothing on this subject.

### `d05776` — no vision file

`flows/d05776/log.md` exists and is on-subject (Claude/Codex coupled
upgrade, persistent-server work) but contains no `vision/` file and no
quoted psyche record — it is a working-instruction paraphrase, not a
verbatim record, so nothing is reproduced from it here beyond what part 2
already draws on.

## 2. Flow accounts

**Relayed** from each flow's own `log.md`/`reports/`/`witnesses/`, as cited.

### 01a04524 — realized global access to new sessions and remote session creation

From `flows/01a04524/log.md`: this flow set out to give Claude the same
session-wide reach as Codex flow 01a03f49 — access to newly created sessions
and remote session creation without manually enabling each one. It found
"Claude 2.1.246 already provides `claude remote-control` as a persistent
multi-session local server that can create same-directory, worktree, and
resumed sessions remotely," but that this is **two separate mechanisms**:
user-wide `remoteControlAtStartup` for every newly launched interactive
session, and a persistent `claude remote-control` server for remote
creation — and that Claude cannot reproduce Codex's single durable
multi-directory inventory exactly (local processes must stay alive).

Its "Claude parity finding": `claude remote-control` can be the persistent
multi-session owner, with Claude Desktop/browser/mobile as Remote Control
clients that may disconnect without ending owner-held sessions — but "Claude
exposes no supported local TUI client for a server-owned Remote Control
session," so the exact Codex (01a03f49) shared-session-attachment topology
is "not natively realizable in Claude 2.1.246." Its terminal-best shape: "a
managed persistent owner plus Desktop/browser/mobile clients."

It landed CriomOS-home `f964853a0c067cdabbe0b8d4904346fadeb9a152`
("Migrate canonical Codex and Claude packages"), containing the Claude-owner
realization, and reported "all focused remote-builder gates for
Claude/Codex Remote Control ... exited `0`." Its final open item: advance the
CriomOS consumer, prove the complete host, deploy, and witness the live
signed-in Desktop/daemon lifecycle — i.e. it ended without a completed
live-deployment witness.

### 01a047d2 — what broke

From `flows/01a047d2/log.md`, remembering 01a04524 at depth 3: "It knowingly
substituted two vendor-owned servers for Codex parity. Its last response
admitted activation failure and no live Claude/Desktop witness. The deployed
Claude service used `/home/li`, which Claude refuses to trust; it retried
175 times and stopped. Ordinary Claude sessions were never routed into a
shared owner."

Its own "Settled audit conclusion": "the failure was architectural before it
was operational. The work treated vendor parity as sufficient and landed a
second server even though the envisioned shared ownership property was
absent; its tests proved generated configuration, not the real Claude
trust/relay/session lifecycle."

The living's recovery-boundary ruling, relayed in the same log: "do not
introduce a Nexus or cross-vendor broker. Keep the native server capability
running for Codex and Claude, and have their desktop apps use it locally."

01a047d2 then diagnosed and fixed the `/home/li` trust-root defect (Home
commit `ed6832cf59b492601b3cdff4710751b8d1b02832` requiring an explicit
non-home trusted Claude root; CriomOS `b617a56d4eeec18bca380f808186fc0b72a52e99`
setting li's root to `/home/li/primary`), pursued a Desktop-proxy design for
Codex, and via Lojix deployment 84 (2026-08-28 20:32:32 CEST) reported both
units live and healthy: `codex-remote-control.service` PID 1664164 (Codex
0.150.1) and `claude-remote-control.service` PID 1664163 (Claude Code
2.1.250, rooted at `/home/li/primary`). It also recorded that Claude
Desktop is a relay client, not a direct local-socket client, of that owner —
unlike the Codex Desktop proxy, which it found could not simultaneously
preserve ChatGPT Desktop's dynamic app-tools behavior and attach to the
shared owner, leaving that as an explicit open architecture decision.

### 01a057e7, 01a05833, d05776 — later status of that same service

Flow `01a057e7` (Claude Code/Desktop connectivity) later confirmed, by
direct live witness on Claude Code 2.1.251, that Desktop does discover and
control the locally running Remote Control owner, that `--permission-mode
bypassPermissions` is an owner-side flag (not settable from the remote
client, since Anthropic's remote UI omits Auto/Bypass), and that the living
ruled to add that flag to the declarative owner. It records the flag being
deployed (CriomOS-home `33204003…`, CriomOS `e6d23efa…`, Lojix deployments
129/130) to a live unit at PID 857561 with argv
`claude remote-control --spawn=same-dir --permission-mode bypassPermissions`,
and the living's own UI witness that bypass mode became visible after the
first turn of a new remote session.

Flow `01a05833` deployed the then-current Codex/Claude generation to
Ouranos and Zeus, including corrections to "the reusable per-profile
remote-control workspace and Claude trust migration" (deriving each unit's
working directory from the account's own home + `/primary`, since the prior
Zeus attempt failed with the literal `/home/li/primary` inapplicable to
Bird). Its final witnessed state on Zeus: Claude 2.1.251 live at PID 543072
with `/home/bird/primary` and structured trust, Codex 0.151.0 live at PID
521513, zero restarts across the final activation window.

Flow `d05776` is a later working-instruction entry (Claude/Codex coupled
upgrade) that explicitly remembers 01a05833 and the others and states that
its own remembered claims about the persistent servers "still require fresh
witnesses before this flow calls them verified" — it does not itself add new
realized/removed history for the Claude remote-control server; its `log.md`
contains only the one remembering paragraph reproduced in part 1.

### db267d — what was removed and why

`flows/db267d/log.md` records the operative instruction, relayed by the
flow (not a quote block): "Take the cloud remote server out of CriomOS.
Reintroducing it is a later conversation." The same log records the flow's
own uncertainty about the referent at the time: "The 'cloud remote server'
the psyche wants gone is, on a subflow's unverified reading, the
`claude-remote-control` systemd user service in CriomOS-home, restarting
every 2s." That reading was then verified and acted on: "The Claude
remote-control server is out. Verified referent:
`modules/home/profiles/min/claude-remote-control.nix` in CriomOS-home, a
home-manager module gated on `user.size.min` declaring a systemd user
service with `Restart=always` and `RestartSec=2s`. ... Deleted the module,
its check, its import, its flake wiring, and its documentation; no stub and
no disabled option. Codex's remote control is a different unit from a
different package in `agent-intercom.nix` and was left alone."

Removal detail, from `flows/db267d/witnesses/claude-remote-control-removal.md`
(witness method: `jj git clone --colocate` of each repo's `origin/main` into
fresh worktrees, evaluation only, no deployment):

- CriomOS-home: deleted `modules/home/profiles/min/claude-remote-control.nix`
  and `checks/claude-remote-control/`; dropped the module import in
  `modules/home/default.nix`; dropped the `"claude-remote-control"` entry in
  `flake.nix`'s `ownedCheckNames` and its `checks.claude-remote-control`
  `callPackage`; rewrote `ARCHITECTURE.md`'s persistent-owner paragraph to
  state Home declares no such owner; deleted `UPGRADES.md`'s `## Persistent
  Claude Remote Control` section, added a `## Claude Remote Control removal`
  section.
- CriomOS: replaced the `claudeRemoteControl` binding and its
  `WorkingDirectory`/`Restart`/`UMask` assertions in
  `checks/lojix-ownership/default.nix` with negative assertions that no
  projected user has a `claude-remote-control` service; advanced the
  `criomos-home` pin `08717ef8…` → `1ae5da86…`.
- Pushed as CriomOS-home `main` = `1ae5da86099e323cda8f79ab239ca4efaa12ce47`
  ("Remove the Claude Remote Control server") and CriomOS `main` =
  `a48f9cb843f7107772b3b5405bdeadfef06fc038` ("Drop Claude Remote Control
  from the OS contract"). Producer pushed before consumer; **not deployed**
  by this witness (evaluation only).
- Residual flagged for the flow: "An account that already ran the previous
  generation keeps the unit running after activation; home-manager removes
  it from the managed set but does not stop a live unit.
  `systemctl --user disable --now claude-remote-control.service` on each
  such account, once, at deploy time."

**Removed unit, quoted from the git history** — this subflow located the
removal commit directly in `/git/github.com/LiGoldragon/CriomOS-home` (git
log, **witnessed**). Two commits carry the message "Remove the Claude Remote
Control server": `1ae5da86` (the original, on the branch later rolled back)
and `08d66b81` (the same removal replayed onto the rolled-back `main` after
an unrelated overnight-renovation rollback — see below). `08d66b81`'s
message:

```
Remove the Claude Remote Control server

Flow db267d. The persistent claude-remote-control user service ran with
Restart=always / RestartSec=2s in every minimum Home profile and is no
longer wanted. Deleted, not deprecated: the module, its
criomos.claudeRemoteControl options, its import, its contract check, and
its check-name registration. The independent codex-remote-control owner
is untouched; the two never shared a module.
```

Diffstat: `checks/claude-remote-control/default.nix` (-131 lines),
`modules/home/profiles/min/claude-remote-control.nix` (-62 lines),
`modules/home/default.nix` (-1 import), `flake.nix` (-4), plus
`ARCHITECTURE.md` and `UPGRADES.md` rewrites.

Why it was removed, per the explicit deferral record in part 1
(`flows/db267d/vision/reminders.md`): the living asked for it out "with
reintroduction left to a later conversation," and separately noted the
deferral itself had "nowhere to live" — which is the origin of the reminders
mechanism this file itself sits in. No further rationale (e.g. a security or
reliability complaint about the service) is recorded anywhere found in this
search; the removal request is recorded as a standalone instruction, not
argued for.

### What was deferred

Per `flows/db267d/vision/reminders.md` (part 1, verbatim) and the `log.md`
paraphrase: reintroduction of the cloud remote server was explicitly
deferred to "a later conversation" — this present subflow's parent flow
(9e7c9f) is plausibly that later conversation, per the brief's own framing
("the living now says they would like it functional again"). Nothing in the
searched records specifies a target design for reintroduction beyond the
pre-removal state already described in parts above (01a04524/01a047d2's
"managed persistent owner plus Desktop/browser/mobile clients" shape,
`--spawn=same-dir --permission-mode bypassPermissions`, root derived from
each account's own `${homeDirectory}/primary`).

## 3. Live state, witnessed now

All of this section is **witnessed** directly by this subflow on Ouranos,
2026-09-12, unless marked otherwise.

**Installed Claude Code version:**

```
$ claude --version
2.1.263 (Claude Code)
```

This is newer than every version named in the flow accounts above (2.1.246
→ 2.1.263), so the removal-era behavior of `claude remote-control` may not
be identical to what is described in part 2.

**`claude remote-control --help` in this version:**

```
Remote Control - Control local sessions from claude.ai/code or the Claude mobile app

USAGE
  claude remote-control [options]
OPTIONS
  --name <name>                    Name for the session (shown in claude.ai/code)
  --remote-control-session-name-prefix <prefix>
                                   Prefix for auto-generated session names
                                   (default: hostname; env:
                                   CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX)
  -c, --continue                   Reattach to the session `claude remote-control`
                                   last recorded for this directory (or one of its
                                   git worktrees) instead of creating a new one.
                                   Exits with an error if nothing was recorded
                                   here within roughly the last 4 hours
  --session-id <id>                Reattach to a specific session by ID (cannot be
                                   used with spawn flags or --continue)
  --permission-mode <mode>         Permission mode for spawned sessions
                                   (acceptEdits, auto, bypassPermissions, default, dontAsk, plan)
  --debug-file <path>              Write debug logs to file
  -v, --verbose                    Enable verbose output
  -h, --help                       Show this help
  --spawn <mode>                   Spawn mode: same-dir, worktree, session
                                   (default: same-dir)
  --capacity <N>                   Max concurrent sessions in worktree or
                                   same-dir mode (default: 32)
  --[no-]create-session-in-dir     Pre-create a session in the current
                                   directory; in worktree mode this session
                                   stays in cwd while on-demand sessions get
                                   isolated worktrees (default: on)

DESCRIPTION
  Remote Control allows you to control sessions on your local device from
  claude.ai/code (https://claude.ai/code) or the Claude mobile app. Run
  this command in the directory you want to work in, then connect from
  your phone or a browser.

  Remote Control runs as a persistent server that accepts multiple concurrent
  sessions in the current directory. One session is pre-created on start so
  you have somewhere to type immediately. Use --spawn=worktree to isolate
  each on-demand session in its own git worktree, or --spawn=session for
  the classic single-session mode (exits when that session ends). Press 'w'
  during runtime to toggle between same-dir and worktree.

NOTES
  - You must be logged in with a Claude account that has a subscription
  - Run `claude` first in the directory to accept the workspace trust dialog
  - Worktree mode requires a git repository or WorktreeCreate/WorktreeRemove hooks
```

This confirms the shape the flows found: one persistent server process,
rooted in a directory, reachable from claude.ai/code and the mobile app,
supporting `--spawn=same-dir|worktree|session` and
`--permission-mode bypassPermissions`. `--spawn=worktree` gives on-demand
session creation isolated per git worktree; `--spawn=same-dir` (the default,
and what the removed unit used) pre-creates one session and accepts further
concurrent sessions in the same directory, up to `--capacity` (default 32).

**Whether any Claude remote-control process or unit runs now:**

```
$ systemctl --user status claude-remote-control
Unit claude-remote-control.service could not be found.

$ systemctl --user list-unit-files | grep -i claude
(no output)

$ ps aux | grep claude
```

No `claude-remote-control` unit is installed or loaded, and no process on
this host is running `claude remote-control` in any form. Five ordinary
interactive `claude --dangerously-skip-permissions` TUI sessions are running
(agent-intercom-attached, unrelated to Remote Control), plus their
agent-intercom broker/server child processes. Codex's separate, never-removed
`codex-remote-control.service` **is** live: `active (running)` since
2026-09-10 13:30:08, PID 2087, `codex app-server --remote-control --listen
unix://`, enabled and loaded from
`/home/li/.config/systemd/user/codex-remote-control.service`. This confirms
db267d's claim that the two units are independent and that only the Claude
one was removed — the Codex unit's continued presence is direct, live
confirmation.

**What the currently declared CriomOS-home source says:**

```
$ cd /git/github.com/LiGoldragon/CriomOS-home && git log --oneline -1 origin/main
f652ba9a Pin Chroma exact GeoClue accuracy
```

`origin/main` is far ahead of the removal commits (most recent commits are
Chroma/Horizon work, unrelated), but the removal persists — `git grep`
across `origin/main` finds "claude remote" only in prose (`ARCHITECTURE.md`,
`UPGRADES.md`), never in Nix source. `ARCHITECTURE.md` on `origin/main`
currently states:

```
Home declares no persistent Claude Remote Control owner. Claude Code is a
terminal harness here: sessions are created by a person or a flow at the
moment they are wanted, never held open by a restarting background service.
Claude Desktop, the browser, and mobile remain Anthropic-relay clients of
whatever session their own account owns; Home neither hosts nor supervises
one.
```

`UPGRADES.md` retains the standing migration note (`## Claude Remote Control
removal`, quoted in part 2) instructing any account still running the old
unit to `systemctl --user disable --now claude-remote-control.service`
once — this witness's own host (Ouranos) shows no such lingering unit, so
that cleanup step was either already carried out here or never applied
(the unit is absent from `list-unit-files`, consistent with either).

**Proposal for the main flow (not applied here): the smallest declarative reintroduction.**

Based on the source that existed before removal (`db267d`'s witness, part 2)
and the later fixes layered on it by `01a047d2`/`01a057e7`/`01a05833`, the
smallest restoration of "start a new Claude session from the phone/web"
would be:

1. Restore (not reinvent) `modules/home/profiles/min/claude-remote-control.nix`
   and `checks/claude-remote-control/` from CriomOS-home history at
   `1ae5da86^` (the parent of the removal commit), or from the pre-removal
   tip — these are recoverable verbatim from git history rather than
   redesigned.
2. Re-add the module import to `modules/home/default.nix` and the check
   registration in `flake.nix`.
3. Carry forward the two post-removal-era corrections found in the flow
   accounts, since they fixed real defects in the original module and
   should not be silently dropped on restoration: derive the working
   directory as `${config.home.homeDirectory}/primary` per account (from
   `01a05833`'s Zeus fix, commit `122bc1d1…`) rather than a literal
   `/home/li/primary`; and declare `--permission-mode bypassPermissions`
   on the unit's `ExecStart` (from `01a057e7`'s ruling and realization,
   commit `33204003…`) if the bypass-permissions decision the living made
   then still stands — that is itself a re-ruling the main flow should put
   to the living rather than silently re-apply, since a security posture
   choice was involved.
4. Restore the negative assertions in CriomOS's
   `checks/lojix-ownership/default.nix` to positive `claudeRemoteControl`
   bindings, and re-pin CriomOS-home.
5. Deploy through Lojix to each account (Ouranos li, and Zeus bird/li),
   verifying the live unit's argv and Anthropic-relay Desktop/mobile
   discovery as `01a057e7` and `01a05833` did.

**Upstream capability this depends on:** the entire design rests on `claude
remote-control` remaining a supported subcommand of the installed Claude
Code CLI with a persistent-server mode reachable from claude.ai/code and the
mobile app — confirmed still present and materially unchanged in shape at
2.1.263 (`--spawn`, `--permission-mode`, `-c/--continue`, `--capacity`, all
present in the help text above). It also depends on Anthropic's relay
continuing to let Claude Desktop/browser/mobile discover and attach to a
locally-owned Remote Control server without exposing local TUI attachment
(01a04524's finding that Claude "exposes no supported local TUI client for a
server-owned Remote Control session" — unlike Codex — still describes the
gap between this design and the `01a03f49` Codex topology the living
originally asked Claude to match). No live check was made in this witness
session of whether that TUI-attachment gap has narrowed in 2.1.263; it is
carried forward from 01a04524's finding, unverified against the current
version.

## Sources

- `flows/01a04524/vision/claudeRemoteControl.md` (verbatim reproduction, part 1)
- `flows/01a04524/log.md` (relayed, part 2)
- `flows/01a047d2/vision/remoteControl.md` (verbatim reproduction, part 1)
- `flows/01a047d2/log.md` (relayed, part 2)
- `flows/db267d/vision/reminders.md` (verbatim reproduction, part 1)
- `flows/db267d/log.md` (relayed, parts 1 and 2)
- `flows/db267d/witnesses/claude-remote-control-removal.md` (relayed, part 2)
- `flows/58a86d/vision/claudeDesktop.md` (verbatim reproduction, part 1)
- `flows/01a057e7/log.md` (relayed, parts 1 and 2)
- `flows/01a05833/log.md` (relayed, part 2)
- `flows/01a05833/annotations.md` (checked, no relevant record)
- `flows/d05776/log.md` (relayed, part 2)
- `Vision/` (repo-wide search, checked for distillation of the above — none found)
- `/git/github.com/LiGoldragon/CriomOS-home`, `git log`/`git show`/`git grep`
  on `origin/main` and commits `1ae5da86`, `08d66b81` (witnessed directly by
  this subflow, part 2 and part 3)
- `claude --version`, `claude remote-control --help`, `systemctl --user`,
  `ps aux` on host Ouranos (witnessed directly by this subflow, part 3)
