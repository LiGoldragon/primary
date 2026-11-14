# Scenario 19: SendAccepted Queued on 4fa6aba, Sent on the Emission head

Verdict: **timing, not code.** The two runs reached the Task in different queue states. On the 4fa6aba run (the 0.56.1 line), scenario 19's own Codex Launch was refused by Herdr at spawn. That left scenario 18's c1 Order queued ahead of the Task. On the Emission head the Launch succeeded and took c1, so the Task was alone in the queue. The seven commits change no decision on this path.

Nothing was changed or run. All evidence is existing logs, witnesses and `git diff 1e931e43 0d39641b`, read in /git/worktrees/flow-emission-565bc8-b.

## Observations

### The scenario (capsule/flow-capsule.clj:1793)
- Step 1. `codex` is the Awake flow of `{ Mind test Terra }`. If there is none, the scenario calls `Launch` and watches up to 60 s for Awake. The Launch reply is not recorded.
- Step 2. It sends `Wake Soft.Task.{ 1 «… Tag g1.» }`.
- The seat is Simplified and OnDemand. Its brief is "Answer with one word and stop", so each flow sleeps after its first turn.
- Scenario 18 runs just before it and leaves a `Queue` Order (c1) for that seat. That Order is admitted after the seat has already slept, so it stays queued. This is why 18 fails in every run.

### 4fa6aba run
Files: capsule-codex-wake-4fa6aba.nexus.log lines 126-136; witnesses capsule-0.56.0-20261114T095852Z.
- `flow 15a142 slept at its rest`, then `admitted Order` (c1).
- Then `herdr stage=spawn category=adapter-refused`. This is scenario 19's Launch, and it is the only such line in any of the eight capsule runs surveyed. Accordingly the capsule line reads "Codex flow  session": no flow id.
- `admitted Task …`, then `flow 5f6b8a woke; its first prompt carried 1 requests`.
- The rollout of 5f6b8a holds Tag c1 and no Tag g1, so the wake carried the oldest entry, c1.
- Twice: `5f6b8a kept at its Stop: DrainRefused(WaitingForTurn(…087))`. Cursor 87 is the Task's (`SendAccepted.{ ukmx 87 Queued }`).
- The Done answers `SendRefused.Unresolved`, because the Task was never delivered.

### Emission run, full
Files: capsule-emission-b-0d39641.nexus.log lines 126-148; witnesses capsule-0.56.1-20261114T105748Z.
- `983501 slept`, then `admitted Order` (c1).
- Scenario 19's Launch succeeds and becomes flow cfeceb. Its rollout holds Order 45h7, Tag c1. Then `cfeceb slept at its rest`.
- `admitted Task`, then `flow 33b022 woke; its first prompt carried 1 requests`. The first prompt is Task 42pv (Tag g1). c1 follows only as "Flow cfeceb … left these requests open", which is not a queue entry.
- The answer is `Sent.42pv`.

### Emission rerun
Files: s19-rerun.nexus.log; witnesses capsule-0.56.1-20261114T111732Z.
- The same shape: 86b5fe slept, c1 admitted, Launch to 4eefaa (which took c1), 4eefaa slept, then the Task woke 878eb1 carrying g1. The answer is `Sent.zih4`.

### Earlier runs of scenario 19
The five earlier capsules in flows/e3a7d1 (0.54.7, 0.55.0, 0.56.0 before the fix) all name a launched Codex flow: 51351f, b17dea, 0979ef, 8b3e59, 0ba5fc. Their Launch succeeded as on the Emission head.

## Q1: the path (sending.rs, branch line numbers; 1e931e43 is the same at -5)

`complete_direct_send` (1334) starts with: the seat is not Awake, so `self.wake(address)`.
- **Woken, and the Task no longer queued (1365).** Its first prompt carried it. The loop at 1409 waits up to 10 s for the receipt. When the receipt arrives, `Delivered` maps through `completed_direct_response` (207) to `Sent`.
  - **Emission runs: this branch.** Each run woke a fresh flow whose first prompt was the Task, and the Codex turn landed within about 4 s.
- **Woken, but the Task still queued** (Simplified carries only the oldest entry). The path goes to `drain_all_held`, which answers `WaitingForTurn` because the carried c1 is outstanding. The snapshot is Queued with no carrying attempt, so at 1382 the answer is `SendAccepted(acceptance)` as admitted, Queued, with a pending Send.
  - **4fa6aba run: this branch.** The log's WaitingForTurn(087) is that pending Send's drain.
  - The queued-behind arm of commit 3 (1478) would give the same answer if the wake had answered Failed. The log's successful carry makes the plain Woken arm the likely one.

What decided the branch is whether c1 was still queued. That was decided by whether scenario 19's Launch spawned. It was not decided in sending.rs or waking.rs.

## Q2: the four `send tool invocation Refused` lines

They come from send_tool.rs:204, the journal of a Codex flow's dynamic `send` tool call.
- Flow 33b022 made four calls through `exec`, all answered `Refused.Malformed`. Each tried to answer the predecessor's open Order 45h7, for example `tools.send({request_id:"45h7", answer:"c1"})` and `tools.send({to:"Psyche test Opus", request:{…}})`. After the four refusals it ended its turn with the text "c1".
- In the rerun, 878eb1 got the same prompt and answered "c1" without calling the tool, so there are no lines.
- The 4fa6aba run has none: its Codex flow got only c1, with no inherited open request.
- The 0.54.7 pko0 run has two such lines, so the log line is older than the branch.
- The branch does not touch send_tool.rs or the Codex app-server family.

These lines are model behaviour: a Codex model writing malformed tool arguments. They are not caused by the code under test.

## Q3: does any commit change a decision on this path?

No. Checked against `git diff 1e931e43 0d39641b`:
- **sending.rs:** the only hunk is the Rehearse output line (655). waking.rs, store/ and send_tool.rs are untouched.
- **Herdr `agent start`:**
  - The `HerdrCommand::StartAgent` words in emission.rs:118 and the Codex harness words in emission.rs:325 match the old argv word for word: `--remote unix://…`, `--model`, `-c model_reasoning_effort=…`, `-c tui.terminal_title=["thread-title"]`, lean start, configured arguments, `resume <thread>`. The same is true of `--kind`, `--pane`, `--timeout 30000`, `--executable`.
  - `Emittable<HerdrCli>` runs it with `Command::new(...).args(...).output()`, as before, with no timeout added.
  - A non-zero exit is still `SpawnFailure::Refused(Herdr(from_printed(stderr, stdout)))`.
  - `typed_command_refusal` checks the same words.
- **Pane shell line (commit 7):** used for Claude only (PrepareClaudeEnvironment). The Codex path does not use it.
- **Socket prompt (commit 6):** submits startup parts typed into a pane. A Codex first prompt goes through the app-server, which is untouched.
- **The other Herdr reads on this path** (`agent wait`, `agent get`, workspace create, `pane process-info`, `pane close`): the same words through the same runner.
- **Codex resources:** one decision is new. A Codex command line without an app-server socket is now `Unattempted`; before, `--remote` was left out. Every Codex launch here has its socket, so this is not reached.

## Hypotheses

- H1, held. The 4fa6aba Launch refusal was a transient Herdr `agent start` failure.
  - In the same run, scenario 18's Codex spawn and scenario 19's wake spawn (5f6b8a, seconds later) both succeeded. Every other run's scenario 19 Launch succeeded.
  - The refusal came within about 0.2 s of the Launch, judging by the 60 s watch ending at the Task's admission (10:17:34.49 against c1 at 10:14:34.33 plus 120 s plus 60 s). That points to a fast Herdr refusal, not its 30 s timeout.
- H2, predicted, not observed. On 1e931e43, a scenario 19 whose Launch succeeds answers `Sent`, as the Emission head does. No run of the fixed code has yet had both a successful Launch and the fix: earlier successful launches ran pre-fix code and answered `Failed(StoreRefused)`.

## Unknowns

- What Herdr printed when it refused the 4fa6aba Launch. The Nexus log line carries no cause, and the capsule does not record scenario 19's Launch reply.
- Whether `Sent` holds when the Codex first turn lands later than the 10 s budget. Then the answer would be `SendAccepted Uncertain`. That depends on timing on either code.

## Confirming experiment, not run

To turn H2 into an observation, rerun scenarios 0, 18 and 19 on the 1e931e43 configured package (/nix/store/37cnpkhb…-flow-configured-0.56.0 is 4fa6aba; the released 0.56.1 package serves too). Expected: `Sent.<id>`, with the Launch succeeding.

Separately, the capsule's scenario 19 expects `SendAccepted.` and reads the id only from that form. That is a capsule fault for any run on the fixed code, and it produces the malformed Done.
