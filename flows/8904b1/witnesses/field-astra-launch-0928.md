# New seats launch, 2026-09-28 (Field Astra, Field Sol, Mind Sol reach, Psyche Opus)

Method: a subflow of 8904b1 ran the commands below and read back the results passively. The sources were the launcher's output, `herdr --session default agent get/list`, `hm-list`, `hm-heartbeat-state` (read-only), the native Codex rollouts under /home/li/.codex-next/sessions/2026/09/28/, and the messenger-clj 0.2.5 source unpacked from its installed jar. Observations are kept apart from inferences, and inferences are marked.

## Workspace

- /home/li/primary: `@` was on 106cf00b (main@git), not on main 3e0b7727, which the remote also held. The launcher refuses to run unless main is an ancestor of `@`.
- `jj st` showed no changes. Then `jj new main` reported that it had modified 3 files. The old `@` (vstrywnw) had meanwhile picked up an unsaved edit by Mind Astra 6f51ad to flows/6f51ad/log.md: 8 added lines, "Sol review and Field host handover". Moving `@` left that edit in the sibling commit and put main's version of the file on disk.
- Repair within seconds: `jj squash --from vstrywnw --into @`. The edit is back in the working copy as an uncommitted change, and vstrywnw no longer exists. For those seconds the file on disk lacked the 8 lines. If 6f51ad wrote to the file in that window, it would have written onto the older content (not observed).

## Launcher change

- tools/codex-main-flow-launch.mjs: `--aspect` was already an argument, but `ASPECT_SKILLS` held only Mind, so Field was refused ("no startup skill set").
- Change: added `Field: ['spirit','psyche','psyche-interraction','vocabulary','edit-coordination']`, the same startup set as Mind. Mind is unchanged. The usage line now reads `[--aspect Mind|Field]`.
- tools/codex-main-flow-launch.test.mjs: the refusal case now uses Psyche, and a new case accepts Field. Output: "codex-main-flow-launch tests passed".
- Lock 8657 was taken on both paths and released after the push.
- Commit b07a48c2c271da30bd58bfa7b8a06162222c72e6 on main touches only those two paths. `jj git push --bookmark main` succeeded. `git ls-remote git@github.com:LiGoldragon/primary.git refs/heads/main` returned b07a48c2c271da30bd58bfa7b8a06162222c72e6.
- Inference: there is no `field` skill on main. A Field seat therefore starts with the Mind set, and other skills load through the skill interface as the work calls for them.

## Field Astra (run once)

`node /home/li/primary/tools/codex-main-flow-launch.mjs --model gpt-6-astra --aspect Field --brief /home/li/primary/flows/8904b1/launch/field-astra-brief.md` (byte-identical to the copy under /home/li/wt/primary/56ae53)

    workspace: /home/li/primary is the default workspace and holds main
    prompt: composed 19577 bytes from main into /tmp/codex-main-flow-launch-Dc77Gm/first-prompt.md
    pane: w1:pH in tab w1:tF of workspace w1, cwd /home/li/primary
    harness: codex-next thread 01a0e9d0-a52b-7da0-889c-0bdbea031b5c: gpt-6-astra, effort medium, approval never, no sandbox
    first prompt: accepted once; leading block is main-flow as on main
    flow: Flow ID bea031, directory /home/li/primary/flows/bea031
    title: read back "FieldV2.{ Astra bea031 }"
    herdr agent: FAILED: timed out waiting for an interactive agent bound to the thread
    exit=1

- Rollout: /home/li/.codex-next/sessions/2026/09/28/rollout-2026-09-28T14-59-20-01a0e9d0-a52b-7da0-889c-0bdbea031b5c.jsonl.
- User items in the rollout: AGENTS.md with the environment context, one item that begins with the main-flow block (20:59:22.009Z), and one `<skill>subflow` item that Codex injected. The first prompt appears once.
- Herdr: agent field_astra_bea031, pane w1:pH, terminal term_65c915700582013. Terminal title "FieldV2.{ Astra bea031 } | primary". interactive_ready is null at every status: working, idle, done.
- First turn: it ran `flow-id codex` (bea031), wrote flows/bea031/log.md, appended to flows/index.md, and delegated its readiness messages to subagents. It went idle at about 21:04Z. The coordinator reports that its ready message reached it.
- Registration: plain `hm-register bea031 field_astra_bea031 --session default --native-thread 01a0e9d0-a52b-7da0-889c-0bdbea031b5c` was refused with "messenger-clj: Agent is not interactively ready" (exit 1), while the seat was idle.
- The coordinator ordered the mend by supported registration. I then ran the same command with `--readiness-probe HM_READY_fieldastra_bea031_20260928 --rollout <the rollout above>`, and it printed "Registered bea031: field_astra_bea031 (default)". The probe types one line into the pane, "Reply exactly <marker> to confirm this explicit HM readiness probe.", and reads the reply from the rollout.
- `hm-heartbeat-state` then showed route bea031: Bound, pane w1:pH, terminal term_65c915700582013, native_thread 01a0e9d0-…, readiness_proof marker HM_READY_fieldastra_bea031_20260928. This matches the live Herdr agent.

## Cause of the unreachable Codex seats

- Observed: Herdr reports `interactive_ready: null` for every Codex agent here, idle or not: 6f51ad, bea031, b666e7 and caf622. Both Claude agents show true.
- In messenger-clj 0.2.5, `register!` refuses an agent without interactive_ready unless a readiness marker is given. With a marker, `readiness-probe!` prompts the seat and looks for the marker in its native rollout.
- The route of 6f51ad carries readiness_proof marker HM_READY_mindastra_6f51ad_20260928, so it was registered the same way earlier today.
- The launcher's "herdr agent" step waits 120 s for interactive_ready. For a Codex seat that flag never comes, so the step fails and the launcher never reaches its register step. Every Codex seat launched by it is left unregistered: listed with "-", and sends to it are Held/RepairRequired.
- Inference: the mend is `hm-register <id> <name> --session default --native-thread <thread> --readiness-probe HM_READY_<unique> --rollout <rollout>`, run on an idle seat.
- Held message from Mind Astra to bea031: I found no read-only command that lists pending intents (hm-heartbeat-state lists only routes and retirements), so I did not see its id or state. From the source: a held RepairRequired intent is delivered only by `hm-repair <flow> <pending-id> …`, and registration does not deliver it by itself. I did not release or resend it.

## Mind Sol b666e7 (launched by Mind Astra 6f51ad, not by this subflow)

- Passive observation: agent mind_sol_b666e7, pane w1:pJ, tab w1:tG, terminal term_65c915b9906ad14, cwd /home/li/primary. Title "MindV2.{ Sol b666e7 } | primary". Native thread 01a0e9d1-d20f-7b43-98b0-15bb666e70e1, model gpt-6-sol. Rollout rollout-2026-09-28T15-00-37-01a0e9d1-d20f-7b43-98b0-15bb666e70e1.jsonl.
- Its launch brief names it "an independently identified Field Sol review flow" for Mind Astra (curriculum-deploy review, no edits). hm-list first showed it as "- mind_sol_b666e7", unregistered.
- The coordinator later handed me its reach. Registered while idle with `hm-register b666e7 mind_sol_b666e7 --session default --native-thread 01a0e9d1-d20f-7b43-98b0-15bb666e70e1 --readiness-probe HM_READY_mindsol_b666e7_20260928 --rollout <its rollout>`, which printed "Registered b666e7: mind_sol_b666e7 (default)".
- Route afterwards: Bound, pane w1:pJ, terminal term_65c915b9906ad14.
- No Mind Sol was launched by this subflow.

## Field Sol (run once)

The model is gpt-6-sol. The Codex model cache lists gpt-6-sol and gpt-5.6-sol, both mapped to "Sol", and the coordinator confirmed gpt-6-sol.

`node /home/li/primary/tools/codex-main-flow-launch.mjs --model gpt-6-sol --aspect Field --brief /home/li/wt/primary/56ae53/flows/8904b1/launch/field-sol-brief.md`

    workspace: /home/li/primary is the default workspace and holds main
    prompt: composed 19307 bytes from main into /tmp/codex-main-flow-launch-LDlsbw/first-prompt.md
    pane: w1:pK in tab w1:tH of workspace w1, cwd /home/li/primary
    harness: codex-next thread 01a0e9d5-8089-7823-8d1f-522caf622f33: gpt-6-sol, effort medium, approval never, no sandbox
    first prompt: accepted once; leading block is main-flow as on main
    flow: Flow ID caf622, directory /home/li/primary/flows/caf622
    title: read back "FieldV2.{ Sol caf622 }"
    herdr agent: FAILED: timed out waiting for an interactive agent bound to the thread
    exit=1

- Rollout: rollout-2026-09-28T15-04-38-01a0e9d5-8089-7823-8d1f-522caf622f33.jsonl. It holds one main-flow user item (21:04:41.062Z) and the injected subflow item.
- Herdr: agent field_sol_caf622, pane w1:pK, title "FieldV2.{ Sol caf622 } | primary", working. The coordinator reports that its ready message arrived.
- Field Sol was launched before the coordinator's message asking to hold further launches arrived.
- Registration: pending the seat going idle (see below).

## Psyche Opus

Not launched at the time of writing. Research into the Claude launch path is done; see the subflow's return.
