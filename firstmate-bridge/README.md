# Temporary First Mate Bridge

A narrow, local coordinator workflow inspired by
[Kun Chen's First Mate](https://github.com/kunchenguid/firstmate). It bridges
Li's current Pi/subagent/intercom/orchestration setup only until Mentci,
Orchestrator, Messenger, and Harness interoperate. It is a tracked instruction
and script directory, not a new daemon, session backend, agent distro, or
replacement architecture.

## Installed surfaces

- `AGENTS.md` is the conversational coordinator contract. Start Pi from this
directory so it reads this contract in addition to workspace instructions.
- `bin/bridge` creates private request, proposal, decision, and report
artifacts. It never starts workers or executes project commands.
- `bin/bridge-smoke` is a local deterministic lifecycle smoke test.
- `.local/` is the default private state home and is ignored. Set an absolute
`FIRST_MATE_BRIDGE_HOME` to use another local private home.

The bridge reuses the existing Pi `subagent` tool for one background
`general-code-implementer` and its native `contact_supervisor` channel. It does
not install packages, edit generated `.pi/` configuration, create a worktree
manager, poll a worker, or duplicate Intercom/Orchestrate.

## Configure one project

```sh
cd /home/li/primary/firstmate-bridge
bin/bridge init /home/li/primary
bin/bridge status
pi
```

`init` records exactly one absolute local project path in
`.local/config/project-path`; it refuses to replace it without `--replace`.
The coordinator stays read-only over that project. Its one delegated worker
follows the existing role packet: it registers a distinct lane, claims exact
paths, uses an isolated worktree when required, validates, commits, pushes, and
returns evidence.

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

4. The coordinator delegates **one** background
   `general-code-implementer` with the request and approved artifact paths. The
   worker reports decisions/blockers via `contact_supervisor`; it does not merge,
   publish, spend, deploy, or expand credentials.

5. After the worker returns evidence, the coordinator creates and completes a
   report, then validates it:

   ```sh
   bin/bridge report cache-cleanup-report cache-cleanup-plan cache-cleanup-choice
   bin/bridge validate-report cache-cleanup-report
   ```

All artifacts remain private under `.local/` unless an operator deliberately
moves them. Do not place personal brain-dumps, credentials, or private material
in tracked bridge files.

## Deterministic check

```sh
bash tests/bridge-smoke.sh
```

The smoke test runs a complete synthetic intake → proposal → human-confirmed
decision → report lifecycle in a temporary state directory, checks the validator
markers, verifies duplicate intake is refused, and removes that state directory.
It does not launch a model, worker, session, network call, project command, or
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

To remove the default installation and all default local artifacts, stop any
worker first, then remove this directory:

```sh
rm -rf /home/li/primary/firstmate-bridge
```

If `FIRST_MATE_BRIDGE_HOME` was set, remove that explicitly chosen local state
directory separately. No service, hook, credential, package, global Pi setting,
or project source is installed by this bridge.
