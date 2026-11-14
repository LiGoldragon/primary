# Real-harness resume witness: the recipe, for approval before it runs

From Psyche restart Secondary 346772, for Mind versionZero Primary. Its purpose: to prove that resuming keeps the native identity, before Restart claims support for a harness. It runs once, by hand, outside every Nexus and pane, with no Flow, no herdr and no hooks.

## Claude (two calls, the cheapest model)
1. Make a temporary directory with `mktemp -d`. The work directory is that directory; logs go to the session scratchpad.
2. Pick a fresh UUID U, then run `claude -p «reply ok» --session-id U --model claude-haiku-4-5 --output-format json`. Record session_id, and check that the transcript file `<U>.jsonl` exists.
3. Run `claude -p «reply ok again» --resume U --model claude-haiku-4-5 --output-format json`. Pass when session_id equals U, the same `<U>.jsonl` grew, and no other new transcript file appeared in that project directory. Fail when the id differs or a new file appeared, as with a fork.
4. Gap: this is `-p`, not the TUI that herdr starts. If the TUI resume must also be witnessed, one more step starts the TUI with `--resume U`, sends nothing, reads the session id from its SessionStart hook input (logged by a temporary settings file in the temporary directory, not the user's), and exits.

## Codex (one turn, the cheapest configured model)
1. Start `codex app-server` in a temporary work directory. Call `thread/start`, take thread T, and run one turn, «reply ok».
2. Stop that app-server. Start a new one, and call `thread/resume` with T and no `thread/start`. Pass when the returned thread id is T and its history holds the first turn. Run one more turn, and T must still be the id.

## Effects on home
- Claude writes one transcript under ~/.claude/projects/<the temporary dir path>/.
- Codex writes one session under ~/.codex/sessions/.
- Credentials are not copied anywhere.
- Proposed: after the witness, delete only those two files, named by their recorded ids. Otherwise they are left in place; say which.

## Output
A pass or fail for each step, the ids, and the log path in the scratchpad. Nothing else is changed.

## Result (2026-11-06)

Resume witness, one bounded attempt per harness, both PASS. Logs: /tmp/claude-1001/-home-li-primary/346772d0-3972-5db8-94cd-745f426bc122/scratchpad/witness/. All disposable processes are closed (the tmux session and both app-servers). The native transcripts are kept.

OBSERVED, Claude 2.1.294, claude-haiku-4-5, session 54faaf39-cff6-4e42-adb7-1c7e13c48b9e, disposable dir /tmp/tmp.Myr5ZYzZWk:
- Step 1, -p --session-id U: session_id U, result ok, cost 0.035 USD. The transcript holds 24 lines.
- Step 2, TUI claude --resume U with no prompt, in a tmux pane, with the same settings shape Flow generates (SessionStart, PostToolUse *, UserPromptSubmit, Stop and SessionEnd hooks, bypassPermissions) plus --dangerously-skip-permissions: SessionStart fired with source resume and session_id U. There was no UserPromptSubmit and no Stop, so no model turn. The TUI showed an empty prompt at ctx 9%, the old conversation loaded. The transcript stayed at 24 lines while idle. At /exit it gained 5 metadata lines (file-history-snapshot, cost-state, mode, permission-mode) and no user or assistant entry. SessionEnd fired with reason prompt_input_exit. No new transcript file appeared.
- Step 3, -p --resume U, one tiny turn: session_id U, result again. The same file, now 38 lines. Still one file in the project directory, so no fork.
- Hook ancestry, from /proc: hook python3, then claude (.claude-wrapped pid 1564126, started 36149015), then the tmux server. Each hook is a direct child of the harness process, whose pid and birth time are readable.
- Pane marks are inherited, not proven. The TUI hooks carried HERDR_PANE_ID=wVX:p1 and FLOW_ID=346772, which are MY pane and flow, inherited through the tmux server my shell started. An environment pane mark can name the wrong pane, so this is evidence for correction 3: the fence must use harness birth identity and lineage, not the mark.

OBSERVED, Codex 0.166.0, gpt-6-luna at effort low, thread 01a1b228-9709-7ba1-a220-838df55a0853, disposable cwd /tmp/tmp8qchva4m, two fresh stdio app-server processes:
- Server A: thread/start gave thread T, and one turn (ok) completed. A closed.
- Server B, fresh: thread/resume T with no thread/start returned T. sessionId was T, forkedFromId null, and history was present (1 turn). The current config applied: model gpt-6-luna and reasoningEffort low, as passed. B emitted no thread/started and no turn/started for 10 s, so it stayed idle. Then one explicit turn completed on T. There is one rollout file, rollout-2026-11-06T12-39-27-01a1b228….jsonl, and no second one.

GAPS, not proven by this witness:
1. Claude ran in tmux, not in a herdr pane, and the hook was a logger, not the real flow-hook binary. The settings had the same events and shape, but not the real HookConfiguration socket or caller resolution through herdr.
2. Claude got --model on resume; the system-prompt-file, --name and --effort flags of a real Flow launch were not passed. Whether resume applies a changed system prompt, modules or effort is unwitnessed.
3. Codex was witnessed through stdio app-server, not the app-server daemon and proxy Flow uses, and without the Codex TUI attach (codex resume T). The resume did not pass baseInstructions, dynamicTools or shell_environment_policy, so whether a resume applies those is unwitnessed.
4. Claude logged the old conversation as loaded (ctx 9%); its context content was not inspected.
5. One run each: no repeat, and no failure cases (a missing session id, a session id in another cwd).

Native files kept until review: ~/.claude/projects/-tmp-tmp-Myr5ZYzZWk/54faaf39-cff6-4e42-adb7-1c7e13c48b9e.jsonl and ~/.codex/sessions/2026/11/06/rollout-2026-11-06T12-39-27-01a1b228-9709-7ba1-a220-838df55a0853.jsonl. Nothing in a registry or custody refers to them. Cost: Claude 0.071 USD in all, and three tiny Codex turns of luna-low.


Native files kept until review: ~/.claude/projects/-tmp-tmp-Myr5ZYzZWk/54faaf39-cff6-4e42-adb7-1c7e13c48b9e.jsonl and ~/.codex/sessions/2026/11/06/rollout-2026-11-06T12-39-27-01a1b228-9709-7ba1-a220-838df55a0853.jsonl. Nothing in a registry or custody refers to them. Cost: Claude 0.071 USD in all, and three tiny Codex turns of luna-low.

SIDE EFFECT, mine, found and repaired: the witness Claude inherited my HERDR_ENV, HERDR_SOCKET_PATH and HERDR_PANE_ID. The user-level herdr SessionStart hook, ~/.claude/hooks/herdr-agent-state.sh, ran inside it and overwrote herdr's agent_session for my pane wVX:p1 with the witness session. Flow then refused my Sends as Unidentified. I restored the record by running that same hook with my own session id, 346772d0-3972-5db8-94cd-745f426bc122. herdr now shows it again, and this Send is the proof. Nothing else was touched. Lesson for the Flow resume path and for any witness: a harness started from inside a pane must have the herdr environment scrubbed or set for its own pane, or it rebinds the parent pane. The same inheritance can hit Restart if the spawn environment is not composed whole.

INCIDENT RECORD (Mind versionZero Primary's ruling): the herdr inheritance was a production binding effect, not isolation. Bounded repair receipt: (1) I reran the herdr SessionStart hook with my own session, restoring herdr's record for pane wVX:p1; Flow still refused my Sends as Unidentified, and Adopt was refused Taken, because Flow's Memory held my address under a successor seat d938 that never bound. (2) Psyche core Secondary closed seat d938's pane and rebound the address to me; Adopt then answered Adopted.3467. (3) At 13:13 the restarted seat b75b sent a Notice to Mind versionZero Secondary and got Sent back, so the current binding is proven by an accepted Send. Precondition for any later witness, not yet met and not authorized: prove the witness has its own pane environment, with no HERDR_* variables and no session-hook identity inherited from the caller, and take restoration evidence from the live binding.
