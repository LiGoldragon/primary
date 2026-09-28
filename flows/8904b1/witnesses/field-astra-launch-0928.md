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
- Registration, once it was idle (observed idle 21:10:30Z): `hm-register caf622 field_sol_caf622 --session default --native-thread 01a0e9d5-8089-7823-8d1f-522caf622f33 --readiness-probe HM_READY_fieldsol_caf622_20260928 --rollout <its rollout>` printed "Registered caf622: field_sol_caf622 (default)".
- Route afterwards: Bound, pane w1:pK, terminal term_65c9169fa81e015.

## Mind Astra's held messages to Field Astra (not delivered)

- The coordinator named them: the true one is pending c196af75-7250-4668-af09-fadddf6a789e, addressed to bea031; a mistaken one is addressed to field_astra_bea031. Neither was touched.
- From the 0.2.5 source: `hm-repair bea031 --pending-id <id> --session --pane-id --terminal-id --name --agent` delivers exactly the one pending id given. It checks that the pending belongs to flow bea031, so the mistaken one cannot come with it.
- The same code also has two side effects:
  - It rewrites the bea031 route without its readiness_proof (`put-route-and-attempt!` with a bare RouteBinding).
  - After typing, it runs `verify-target!`, which with interactive_ready null and no proof fails "NotReady". The command would then report "Uncertain … do not retry" even though the envelope was typed, and bea031 would need a second readiness-probe registration.
- Inference: Mind Astra sending the message afresh with hm-send now that bea031 is Bound is cleaner. The held record would stay pending.

## Claude launcher

- New tools/claude-main-flow-launch.mjs and tools/claude-main-flow-launch.test.mjs. Lock 8684 was taken on both and released after the push.
- Commit add76a5aff730043ed77026505c076c418872e7e was made from `@` with only those two paths. Its parent was main 844567096b48, so the bookmark moved forward without a duplicate. The push succeeded, and `git ls-remote … refs/heads/main` returned add76a5aff730043ed77026505c076c418872e7e.
- Tests: "claude-main-flow-launch tests passed"; the Codex test still passes.
- What it does:
  - It chooses the session UUID itself and runs `flow-id claude --flows-root … --parent-session <uuid>` before start.
  - It starts `env -u CLAUDE_CODE_CHILD_SESSION -u CLAUDE_JOB_DIR -u CLAUDE_CODE_SESSION_KIND -u CLAUDE_CODE_SESSION_ID -u CLISESSIONID claude --session-id <uuid> --model <m> --effort medium --name '<canonical title>' --remote-control --dangerously-skip-permissions "<first prompt>"` in a new Herdr tab.
  - First prompt: `/main-flow /spirit /psyche /psyche-interraction /vocabulary /edit-coordination # Launch brief\n\n<brief>`.
  - It reads the transcript back (commands, expanded skill bodies, prompt count, and the brief as the argument), then the assistant model, then the custom-title record, then the Herdr agent, then hm-register.
- Not carried over from the older live Claude seats: `--system-prompt-file tools/main-flow-mode/system-prompt.md` and `--settings <job>/main-flow-settings.json` (the reminder hook).
- Found in passing: jj resolves a `file show` path relative to the cwd. The Codex launcher's `.agents/skills/…` read therefore fails if the launcher is run from any directory other than /home/li/primary. The twin uses `root:`. The Codex launcher was left as it is.

## Psyche Opus (run once)

`node /home/li/primary/tools/claude-main-flow-launch.mjs --model claude-opus-5-5 --aspect Psyche --brief /home/li/wt/primary/56ae53/flows/8904b1/launch/psyche-opus-brief.md` (model as the live dc53b4 transcript recorded it: 211 assistant records "claude-opus-5-5"; mapped to Opus)

    workspace: /home/li/primary is the default workspace and holds main
    prompt: composed 2054 bytes into /tmp/claude-main-flow-launch-icRSqu/first-prompt.md; head /main-flow /spirit /psyche /psyche-interraction /vocabulary /edit-coordination
    flow: Flow ID 183ae0 for session 183ae001-cb84-40ed-8a1f-f07a76f0d1f4, directory /home/li/primary/flows/183ae0
    pane: w1:pM in tab w1:tJ of workspace w1, cwd /home/li/primary
    harness: claude session 183ae001-cb84-40ed-8a1f-f07a76f0d1f4, transcript /home/li/.claude/projects/-home-li-primary/183ae001-cb84-40ed-8a1f-f07a76f0d1f4.jsonl
    first prompt: accepted once; commands [main-flow spirit psyche psyche-interraction vocabulary edit-coordination], expanded [main-flow spirit psyche psyche-interraction vocabulary edit-coordination], prompts 1; the brief is the argument
    harness settings: model claude-opus-5-5, effort medium and remote control as started
    title: read back "PsycheV2.{ Opus 183ae0 }"; terminal title "PsycheV2.{ Opus 183ae0 }"
    herdr agent: FAILED: timed out waiting for an interactive agent bound to the session
    exit=1

- Herdr: agent psyche_opus_183ae0, pane w1:pM, terminal term_65c91845ff41d16, agent_session herdr:claude 183ae001-…. interactive_ready null while working and while idle. This is the same cause as for the Codex seats, so the new Claude seat is also affected.
- Effort and remote control are not read back. They are only as started.
- Registration: once idle (21:15:48Z), plain `hm-register 183ae0 psyche_opus_183ae0 --session default --native-thread 183ae001-cb84-40ed-8a1f-f07a76f0d1f4` was refused with "messenger-clj: Agent is not interactively ready".
- With `--readiness-probe HM_READY_psycheopus_183ae0_20260928 --rollout <its transcript>` it printed "Registered 183ae0: psyche_opus_183ae0 (default)". The seat's reply in its transcript was exactly the marker (21:16:01Z). Route afterwards: Bound, pane w1:pM, evidence_kind claude-transcript.
- First turn, read passively from its transcript:
  - It claimed 183ae0, wrote flows/183ae0/log.md, and committed and pushed with raw `git commit` / `git push origin HEAD:main` from /home/li/primary. Remote main went add76a5af..3d4b3d28d, later e9ce208dc747 "Log Psyche Opus middle-stratum load".
  - The living spoke to it directly: "I don't know if talking to Fable is a good idea. That would cost tokens so wait till you have something to tell them and let's talk first." It therefore sent no ready message to 8904b1.
  - On the living's word it loaded 18 of Fable's skills plus two more.

## Final list (hm-list after the last registration)

    8904b1 psyche_fable_b7ba00 working
    6f51ad mind_astra_6f51ad working
    bea031 field_astra_bea031 working
    b666e7 mind_sol_b666e7 done
    caf622 field_sol_caf622 done
    183ae0 psyche_opus_183ae0 done

## Field Astra reach restored (21:18Z)

Method: passive reads through `hm-list`, `hm-heartbeat-state`, `herdr --session default agent list/get`, the native rollouts, and the read-only `messenger-clj.typed-store/pending-for` and `pending-by-id` run under bb from the installed 0.2.5 jar. The only change was one probe registration.

- The send gate is `verify-target!` in 0.2.5 core.clj. It fails with NotReady when Herdr's `interactive_ready` is false and the route's `native_thread` differs from `readiness_proof.thread_id`. After that it also requires an exact pane, terminal, and agent kind, a status that is not blocked, and a native thread matching Herdr's `agent_session`.
- Before the mend (21:18Z), the bea031 route was Bound (w1:pH, term_65c915700582013) but had no `readiness_proof`, and Herdr showed `interactive_ready` null, so a send would be held NotReady. This matches held record 14bd13c3 at 21:16:02Z.
- The seat was idle: its rollout's last event was task_complete at 21:16:43Z, Herdr showed status done, and the rollout still had 371 lines when I checked again at 21:18:51Z.
- Mend: `hm-register bea031 field_astra_bea031 --session default --native-thread 01a0e9d0-a52b-7da0-889c-0bdbea031b5c --readiness-probe HM_READY_fieldastra_bea031_20260928_r2_2118 --rollout <bea031 rollout>` printed "Registered bea031: field_astra_bea031 (default)" (exit 0, 21:18:51–54Z).
- Rollout: one UserMessage with the probe line at 21:18:52.672Z, then the AgentMessage "HM_READY_fieldastra_bea031_20260928_r2_2118" at 21:18:54.726Z, and task_complete at 21:18:54.816Z.
- Route afterwards: Bound, same pane and terminal, readiness_proof with thread 01a0e9d0-… and marker HM_READY_fieldastra_bea031_20260928_r2_2118.

Other seats (passive, 21:18Z; none mended):
- 8904b1: Herdr `interactive_ready` true; the route has no proof and needs none.
- 6f51ad, b666e7, caf622: interactive_ready null. Each has a readiness_proof whose thread_id equals its route's native_thread, and Herdr's agent_session matches.
- 183ae0: the same, with a claude-transcript proof. It was not probed.

Held for bea031 (from `pending-for`; none released or resent):
- 3101c087-bd1b-41d1-baa9-630a1ceb5311: sender caf622 (from the submitted envelope), 21:07:06Z, RepairRequired. It begins "I am Field Sol caf622, the second Field seat beside".
- 14bd13c3-64f4-4d5d-aa92-7d0468e79e96: 21:16:02Z, NotReady. It begins "Preflight acknowledged; retain cable-path uncertainty explicitly. Earlier Zeus build worker". The record does not store the sender. Inference: Mind Astra 6f51ad.
- 888bcec7-d161-423a-93a4-d86f77ce09cd: 21:17:53Z, NotReady. It begins "I am Field Sol caf622, the second Field seat beside". The record does not store the sender. Inference from the body: caf622.
- c196af75 is no longer pending, which is consistent with its release. fd09c63d is still held for flow 6f51ad (RepairRequired, 16:38:35Z) and was not touched.
