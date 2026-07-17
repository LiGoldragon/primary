# Temporary First Mate Bridge

A narrow, local coordinator workflow inspired by
[Kun Chen's First Mate](https://github.com/kunchenguid/firstmate). It bridges
Li's current Pi/intercom/orchestration setup only until Mentci, Orchestrator,
Messenger, and Harness interoperate. It is a tracked instruction and script
directory with a private Herdr session-provider adapter, not a new daemon,
agent distro, or replacement architecture.

## Installed surfaces

- `AGENTS.md` is the conversational coordinator contract. Start Pi from this
directory so it reads this contract in addition to workspace instructions.
- `bin/bridge` creates private request, proposal, decision, and report
  artifacts.
- `bin/bridge-herdr` owns one private named Herdr session: installation,
  configuration, visible worker creation, observation, message delivery,
  report-gated completion, shutdown, and removal.
- `bin/bridge-smoke` is a local deterministic artifact smoke test;
  `bin/bridge-herdr smoke` is the disposable live Herdr transport smoke test.
- `.local/` is the default private state home and is ignored. Set an absolute
  `FIRST_MATE_BRIDGE_HOME` to use another local private home.

The bridge uses Pi as the worker harness, but workers run in visible local
Herdr agent panes rather than through Pi's `subagent` tool. Existing
Orchestrate remains the worker's coordination facility. The bridge never uses
Herdr worktrees, remote/SSH attach, global configuration, generated `.pi/`
configuration, or a project command on the coordinator's behalf.

## Configure one project and Herdr

```sh
cd /home/li/primary/firstmate-bridge
bin/bridge init /home/li/primary
bin/bridge-herdr install
bin/bridge-herdr configure
bin/bridge status
pi
```

`init` records exactly one absolute local project path in
`.local/config/project-path`; it refuses to replace it without `--replace`.
`bridge-herdr install` creates a **local Nix profile** at `.local/herdr/profile`
from Herdr `v0.7.4` (peeled upstream release commit
`50aaa2ec046ee26ff407c20f49de496f522512a8`). It does not edit the user's Nix
profile. `configure` writes a private config at `.local/herdr/config.toml` that
disables remote SSH helpers, update and manifest checks, notifications, sound,
pane-history persistence, and agent-session restoration. Its named session is
`firstmate-bridge` and is scoped through that private config directory.

The coordinator stays read-only over the configured project. Its one delegated
worker follows the existing role packet: it registers a distinct lane, claims
exact paths, uses an isolated worktree when required, validates, commits,
pushes, and returns evidence.

## Conversation flow

1. Put the brain-dump in a local file, then create a request:

   ```sh
   bin/bridge intake cache-cleanup ~/tmp/cache-cleanup-brain-dump.md
   ```

2. In the Pi conversation, ask the coordinator to read that request and create
   a proposal. It creates a template, fills each section, and makes the state
   reviewable without sending it anywhere:

   ```sh
   bin/bridge proposal cache-cleanup-plan cache-cleanup
   ```

3. For a design/product/authority/privacy/security/irreversible ambiguity,
   create a decision record and show it to Li before dispatch. A script cannot
   prove who approved it: only the coordinator records `human-confirmed` after
   Li's explicit answer.

   ```sh
   bin/bridge decision cache-cleanup-choice cache-cleanup-plan
   # after explicit human confirmation, complete both Markdown records
   bin/bridge validate cache-cleanup-plan cache-cleanup-choice
   ```

4. The coordinator dispatches **one** visible local Pi worker only through
   the validated Herdr gate, then communicates and observes it through the
   Herdr socket-backed CLI:

   ```sh
   bin/bridge validate cache-cleanup-plan cache-cleanup-choice
   bin/bridge-herdr start cache-cleanup-worker cache-cleanup-plan cache-cleanup-choice -- pi
   # Write the bounded worker request to a private local file first.
   bin/bridge-herdr send cache-cleanup-worker ~/.local/share/cache-cleanup-worker.md
   bin/bridge-herdr observe cache-cleanup-worker
   ```

   `start` refuses an unvalidated proposal/decision, a second active worker, or
   a missing exact Herdr installation. `send` uses `pane send-text` followed by
   `enter`; the message file is intentionally outside tracked artifacts.

5. After the worker returns evidence, the coordinator creates, completes, and
   validates a report. It can close the worker pane only through that report
   gate:

   ```sh
   bin/bridge report cache-cleanup-report cache-cleanup-plan cache-cleanup-choice
   bin/bridge validate-report cache-cleanup-report
   bin/bridge-herdr finish cache-cleanup-worker cache-cleanup-report
   ```

All artifacts and Herdr state remain private under `.local/` unless an operator
deliberately moves them. Do not place personal brain-dumps, credentials, or
private material in tracked bridge files or worker-message files.

## Checks and live Herdr smoke

```sh
bash tests/bridge-smoke.sh
bin/bridge-herdr smoke
```

`bridge-smoke` runs a deterministic synthetic intake → proposal →
human-confirmed decision → report lifecycle in a temporary state directory.
`bridge-herdr smoke` uses the installed Herdr binary to create an isolated
private session, start a visible shell worker without modifying project source,
observe it, send it `hello-from-bridge`, wait for its terminal response, pass
the report gate, stop/delete the named session, and remove all temporary state.
It does not launch a model, use remote access, create a worktree, or make a
public action.

## Boundaries and removal

This bridge is intentionally limited:

- It is not a reliable worker scheduler, persistent supervision service,
  cross-session messenger, merge authority, or replacement for the planned
  architecture.
- Artifact validation is structural. It cannot verify human identity, approval,
  a worker's reasoning, or project test correctness.
- Existing Pi runtime availability is still required for actual delegation;
  this bridge does not configure or repair it.
- Herdr is a real local process backend, but its worker shell is still a normal
  local process. Keep only one bridge worker active and treat pane output as
  private terminal content.

To remove only the private Herdr backend after every worker passed its report
gate, run:

```sh
bin/bridge-herdr remove
```

It refuses while a worker record remains, stops/deletes only its private named
session, then removes `.local/herdr` including the local Nix profile. To remove
the whole default bridge and all artifacts, stop any worker first, run that
command, then remove this directory:

```sh
rm -rf /home/li/primary/firstmate-bridge
```

If `FIRST_MATE_BRIDGE_HOME` was set, remove that explicitly chosen local state
directory separately. No global service, hook, credential, package, global Pi
setting, SSH configuration, or project source is installed by this bridge.
