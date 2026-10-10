# Mind Astra launch, 2026-09-28

Workspace step (authorized by the main flow): in /home/li/primary, `jj git fetch` reported nothing changed; the working copy was empty (tuykplpx 43a0c53d on bc0ce6d4). The only processes with that cwd were the Codex app-server daemons (pids 1936, 1960, 9513). `jj new main` made kstrmyyz af68df32 (empty) on main c3d4c98652c6. jj skipped one update: two symlinks from July, reports/general-code-implementer and reports/SchemaTrainExpansion, which main tracks as directories, stay on disk as symlinks. They do not affect the launch.

Launcher run (once): `node /home/li/primary/tools/codex-main-flow-launch.mjs --model gpt-6-astra --brief /home/li/primary/flows/8904b1/launch/mind-astra-brief.md`

    workspace: /home/li/primary is the default workspace and holds main
    prompt: composed 49984 bytes from main into /tmp/codex-main-flow-launch-EIyBvx/first-prompt.md
    pane: FAILED: expected one Herdr workspace labelled primary, found 0
    exit=1

State left: no tab or pane created; no Codex session started; no first prompt sent; no Flow ID claimed; no title; no registration. Herdr session `default` after the run: workspace w1 labelled `56ae53` (it was labelled `primary` earlier today), panes w1:p8 and w1:pC only.

Rerun, if the main flow authorizes it: the same command plus `--herdr-workspace-label 56ae53`.

## Second run (authorized, with `--herdr-workspace-label 56ae53`)

    workspace: /home/li/primary is the default workspace and holds main
    prompt: composed 49984 bytes from main into /tmp/codex-main-flow-launch-tPycYp/first-prompt.md
    pane: w1:pG in tab w1:tE of workspace w1, cwd /home/li/primary
    harness: codex-next thread 01a0e8d3-aace-7712-aae2-3ce6f51adad5: gpt-6-astra, effort medium, approval never, no sandbox
    first prompt: accepted once; leading block is main-flow as on main
    flow: Flow ID 6f51ad, directory /home/li/primary/flows/6f51ad
    title: read back "MindV2.{ Astra 6f51ad }"
    herdr agent: FAILED: timed out waiting for an interactive agent bound to the thread
    exit=1

Session file: /home/li/.codex-next/sessions/2026/09/28/rollout-2026-09-28T10-23-01-01a0e8d3-aace-7712-aae2-3ce6f51adad5.jsonl

Herdr readback after the failure: agent name mind_astra_6f51ad, pane w1:pG, agent codex; agent_session herdr:codex id 01a0e8d3-aace-7712-aae2-3ce6f51adad5; terminal title "MindV2.{ Astra 6f51ad } | primary"; agent_status working; interactive_ready null. So the session report and the rename both took. Only the wait failed: Herdr gives no interactive_ready while the first turn is running.

Registration: not run. hm-list shows "- mind_astra_6f51ad default working", which means unregistered. hm-register refuses an agent that is not interactively ready, and its fallback, the readiness probe, would prompt the seat. So I held the one allowed repair. Run it once the seat is idle:
`hm-register 6f51ad mind_astra_6f51ad --session default --native-thread 01a0e8d3-aace-7712-aae2-3ce6f51adad5`

First turn, watched passively 10:23 to 10:33:
- It announced that it was applying main-flow and psyche, and ran `flow-id codex --flows-root /home/li/primary/flows`; the ID came out as 6f51ad.
- It spawned a subagent startup_read (read-trivial, model gpt-6-luna, reasoning_effort xhigh) to read the three records, and messaged and waited on it repeatedly. startup_read completed.
- At 10:31 it said: "The remaining step is source review, followed by the authorized message."
- No hm-send to 8904b1 was seen in its tool calls by 10:33. Its status stayed working the whole time.

Launcher fix landed from /home/li/primary: 9d0f2218a3de176f0bb4e06ad5cd0b498ceb76e8 on main. It touches only tools/codex-main-flow-launch.mjs and tools/codex-main-flow-launch.test.mjs. The remote ls-remote shows the same commit. The launcher now uses the only Herdr workspace; a label chooses only when there are several.
