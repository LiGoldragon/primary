# The first harness hook that calls the flow CLI

Verdict: the hook scenario is **red, and it did not land**. The repin did
land.

- **The hook.** It fires on SessionStart, PostToolUse and Stop, and on two of
  them it calls `flow` with one inline datom.
- **The Nexus.** It answers both calls. The contract it is compiled with has
  no operation that records a harness event, so its state never shows the
  flow's events.
- **The repin.** flow-test's main moved from `67e1f0a` to `ac986bec`,
  pinning flow 0.19.0 (`4f3670ef`), as the coordinator asked mid-task. The
  existing scenarios stay green.
- **Where the scenario is kept.** Its source is in this flow's witnesses, not
  in flow-test.

## Hook events in this Claude Code version

The installed harness is 2.1.284. Its binary holds one complete hook-event
list of 33 events:

    PreToolUse PostToolUse PostToolUseFailure PostToolBatch
    Notification UserPromptSubmit UserPromptExpansion
    SessionStart SessionEnd Stop StopFailure
    SubagentStart SubagentStop PreCompact PostCompact
    PreModelSwitch PostModelSwitch PermissionRequest PermissionDenied
    Setup TeammateIdle TaskCreated TaskCompleted
    Elicitation ElicitationResult ConfigChange
    WorktreeCreate WorktreeRemove InstructionsLoaded
    CwdChanged FileChanged DirectoryAdded MessageDisplay

The scenario runs `pkgs.claude-code` 2.1.228 from flow-test's pinned nixpkgs.
It does not use the installed `claude`, because that wrapper prepends
`--dangerously-skip-permissions`. In 2.1.228 all three configured events
fired. Their stdin fields, as witnessed:

    SessionStart  session_id transcript_path cwd
                  hook_event_name source
    PostToolUse   session_id transcript_path cwd prompt_id
                  permission_mode hook_event_name tool_name
                  tool_input tool_response tool_use_id duration_ms
    Stop          session_id transcript_path cwd prompt_id
                  permission_mode hook_event_name stop_hook_active
                  last_assistant_message background_tasks session_crons

`prompt_id` is the only turn identifier the harness gives. It is the same on
PostToolUse and Stop within one turn, so the hook uses it as `TurnId`.

## Mapping to signal-flow operations

Versions:

- flow 0.18.0 pinned signal-flow 7.0.0 (`1c9e4b3`).
- signal-flow 7.1.0 (`5860383`) declared `QueueTurnEnd`.
- flow 0.19.0 pins signal-flow 8.0.0 (`c297d98`). It carries `QueueTurnEnd`
  and refuses it on purpose: "Flow holds no turn-end queue, so it answers
  `TurnEndRejected.QueueRefused` and enqueues nothing" (flow `UPGRADES.md`).

The mapping:

    SessionStart -> ResolveCaller.None
                    answered; it carries no event field:
                    the Nexus names the flow bound to the
                    calling process
    PostToolUse  -> none; no operation in 7.x or 8.0.0
                    records a tool use
    Stop         -> QueueTurnEnd.{ SessionId
                                   TurnId
                                   Some.TranscriptPath }
                    the pre-end wakeup; 7.1.0 and 8.0.0

No operation in signal-flow 7.x or 8.0.0 reports or records an Event such as
Started, ToolUsed or Stopped. The vision's `Report.{ FlowId Event }`
(vision-ethos) has no counterpart on the wire.

## Hook config

The hook itself is `flow-harness-hook`, a `writeShellApplication` built with
jq and the pinned flow. It does five things:

1. It reads the event JSON from stdin.
2. It builds one inline datom from the event's fields, with each string in
   guillemets and any closing guillemet escaped.
3. It calls `flow "<datom>"`.
4. On stderr it writes one tab-separated record: the event, the datom, flow's
   exit code and flow's whole output.
5. It always exits 0, so it never blocks the harness.

The settings, passed as `--settings <root>/settings.json`:

    { "hooks":
        { "SessionStart": [ { "hooks": [ { "type": "command",
                                           "command": "<tap><hook><log>" } ] } ],
          "PostToolUse":  [ { "matcher": "*",
                              "hooks": [ { "type": "command",
                                           "command": "<tap><hook><log>" } ] } ],
          "Stop":         [ { "hooks": [ { "type": "command",
                                           "command": "<tap><hook><log>" } ] } ] } }

    <hook>  /nix/store/…-flow-harness-hook/bin/flow-harness-hook
    <tap>   tee -a "$FLOW_HOOK_WITNESS/inputs.jsonl" |      (scenario only)
    <log>    2>> "$FLOW_HOOK_WITNESS/calls.tsv"             (scenario only)

Do not pass `--setting-sources user` alongside `--settings`. With it, no hook
fired in one run.

## Scenario

`flow-claude-hook` is a semi-sandbox runner, gated on `FLOW_TEST_LIVE=1`, in
blueprint layout.

    lib/components/claude.nix      claude-code from pinned nixpkgs;
                                   unfree allowed for it alone
    lib/components/flow-hook.nix   the hook package, command, settings
    lib/default.nix                adds both components
    packages/flow-claude-hook.nix  the runner

The runner's drive:

1. It refuses if the living's access token expires within 15 minutes.
2. It makes a fresh `mktemp -d /tmp/fh-XXXXXXXX` root. HOME, every XDG root
   and TMPDIR point into it, and an exit trap kills the Nexus and removes the
   root.
3. It copies only `.claude/.credentials.json`.
4. It starts flow-nexus on the root's own sockets with a fresh store, and
   checks that `List.{}` answers `Listed.[]`.
5. It runs one `claude -p` on haiku with these limits:
   - bounds: `systemd-run --user --scope -p MemoryMax=2G`, `timeout 300` and
     `--max-turns 4`;
   - the only allowed tool is `Bash(echo:*)`;
   - flags: `--permission-mode default --strict-mcp-config`.
6. It prints seven checks and then a verdict. It exits 0 only if all seven
   are green.

`systemd-run` reaches the user manager through the living's XDG_RUNTIME_DIR
and bus. The scope is then handed the sandbox runtime directory back.

`nix flake check` with the scenario added was green: lint, flow,
flow-populated-store, and the build of both runners.

The source is kept at `witnesses/flow-claude-hook/` under this flow
directory. The `lib/default.nix` change is there as a patch. Apply it on
flow-test `ac986bec` to reproduce.

## Witnessed output

Method: `FLOW_TEST_LIVE=1 nix run path:.#flow-claude-hook` in the flow-test
checkout, with the scenario applied but not committed. The full output is in
`witnesses/flow-claude-hook.run.txt`.

On flow 0.19.0 (`4f3670ef`):

    run: exit 0, session 4397a906-96d9-4c3e-a633-eda318b22ea6
    SessionStart  ResolveCaller.None   0
                  CallerResolutionRejected.CallerUnknown
    PostToolUse   -  -  no signal-flow operation
    Stop          QueueTurnEnd.{ «4397a906-…»
                                 «74e19513-…»
                                 Some.«/tmp/fh-…/4397a906-….jsonl» }   0
                  TurnEndRejected.QueueRefused
    green: the run exited 0
    green: the hook fired on SessionStart
    green: the hook fired on PostToolUse
    green: the hook fired on Stop
    green: SessionStart: ResolveCaller answered
    red: Stop: QueueTurnEnd answered TurnEndQueued
    List.{} after the run: Listed.[]
    red: the Nexus lists the run's session

On flow 0.18.0 (`ae05027`), before the repin, the checks were the same, but
Stop failed earlier. The CLI itself refused with exit 2:

    invalid Flow query: Error { layer: Composition, path: [],
      kind: Variant { expected: "Query", found: "QueueTurnEnd" } }

### What is red

- **Stop.** 0.19.0 refuses `QueueTurnEnd` by design (`QueueRefused`).
- **Nexus state.** No operation records an event, so `List` stays
  `Listed.[]`.
- **The sandbox run is not a flow Flow holds.** `ResolveCaller` answers
  `CallerUnknown`. A session that Flow did not launch has no FlowNode for its
  events to attach to.

## The repin

flow-test main is now `ac986bec`, which pins flow `4f3670ef` (0.19.0) and
updates the lock. It was committed on its own. These ran green:

- `nix flake check` on the local tree (flow, flow-populated-store, lint, the
  flow-claude build);
- `nix flake check github:LiGoldragon/flow-test` after the push.

The `flow-claude` runner still configures the Nexus and exits 3 as designed,
because its launch step is not built yet.

## Proposal in ethos (not landed)

This is the smallest addition to signal-flow. It is the vision's `Report`,
cut down to what Stop's `QueueTurnEnd` does not already carry:

    Signal
    [ Report.{ SessionId
               HarnessEvent }
      Observe.[ Harness.FlowId ] ]
    [ Reported.{ FlowId
                 HarnessEvent }
      ReportRejected.[ UnknownSession
                       SessionMismatch.Caller
                       PersistenceRefused ]
      HarnessObserved.{ FlowId
                        HarnessEvent } ]
    [ HarnessEvent.[ Started
                     ToolUsed.ToolName ]
      ToolName.String ]

    Memory
    [ Flow.{ FlowId
             Vector<HarnessEvent> } ]

- **Report and the caller.** The Nexus checks `SessionId` against the flow
  bound to the calling process, the way `ResolveCaller` checks its claim. It
  reads the caller from the socket, never from the payload.
- **Stop.** Stop stays on `QueueTurnEnd`, with `prompt_id` as TurnId, so a
  Stopped variant would repeat it. What Stop still needs is a turn-end queue
  in Flow's Memory, in place of today's `QueueRefused`.
- **Observe.Harness.** This is a subscription, never a poll. On open it sends
  the flow's events so far, then one `HarnessObserved` frame per accepted
  Report.

Two decisions remain for the main flow and the living:

- A Report from a session Flow did not launch is either refused with
  `UnknownSession` or adopted as a flow.
- `Report` keys either on `SessionId` as written above, or on `FlowId` as the
  vision writes `Report.{ FlowId Event }`. FlowId reaches the hook only
  through the environment Flow launched it with.

Until one of these is settled, the scenario's last check can turn green only
for a flow Flow itself launched. That needs `Start` through a sandbox Herdr,
which is the `flow-claude` runner's unbuilt step.

## Sources

- `/git/github.com/LiGoldragon/signal-flow/ethos/signal.ethos`, at `1c9e4b3`
  (7.0.0), `5860383` (7.1.0) and `c297d98` (8.0.0)
- `/git/github.com/LiGoldragon/flow`, at `ae05027` (0.18.0) and `4f3670ef`
  (0.19.0, its `UPGRADES.md`)
- `/nix/store/qsq3lh2i05dz77dakipwy9f1fkssq1zw-claude-code-2.1.284/bin/.claude-wrapped`,
  for the hook-event list, read from its strings
- `/git/github.com/LiGoldragon/flow-test`, main `67e1f0a` → `ac986bec`
- `/home/li/primary/flows/3ec648/witnesses/semi-sandbox-capsule.sh`
- `/home/li/primary/flows/f1c841/witnesses/flow-claude-hook.run.txt`
- `/home/li/primary/flows/f1c841/witnesses/flow-claude-hook/`
- the vision-flow, vision-nexus, vision-ethos, knowledge-flow and datom
  skills
