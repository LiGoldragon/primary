# Recovery of three `--stdin` sends to 8904b1

Source: `/home/li/.codex-next/sessions/2026/09/26/rollout-2026-09-26T20-09-00-01a0e09f-71ca-79a1-8b23-a8e622ce54a1.jsonl`
(session id `01a0e09f-71ca-79a1-8b23-a8e622ce54a1`, thread_source `subagent`, agent_nickname `Ampere`,
agent_path `/root/mind_launch_authority`, depth 1, parent_thread_id `01a0e029-558a-7852-b5df-1919ac67c6d7`,
cwd `/home/li/wt/primary/field-packet-56ae53`). Parent thread `01a0e029-...` (file
`rollout-2026-09-26T18-00-00-01a0e029-558a-7852-b5df-1919ac67c6d7.jsonl`, source "vscode", no parent) is
Field Sol 9ac67c's own pane-hosted seat. All timestamps below converted from the record's UTC
(`2026-09-27T0X:..Z`) to local by subtracting 6h, matching the file's own local-vs-UTC offset.

## 1. Local 2026-09-26 23:04:57 (line 949)
Command:
```
cat <<'EOF' | FLOW_ID=9ac67c hm-send 8904b1 --stdin
HerdrProbeCorrection.{ FieldSol9ac67c «A detached status subflow invoked Herdr's session help syntax; it unexpectedly created a separate named session whose exact name is two leading hyphens plus help. It did not stop/delete it. Field Luna has not proved HERDR_ENV/TTY and did not attach the test session. Please do not Start. Field will coordinate controlled cleanup from a managed pane after exact identity witness.» }
EOF
```
Intended body (stdin heredoc, exact): as printed above between `EOF` markers.
Messenger answered: `{"exit_code":0,"output":"Transported.{ 8904b1 working }\n"}`
Run by: subagent thread `01a0e09f-...` ("Ampere"), a collaboration child of Field Sol's seat — not Field Sol's root session itself — using `FLOW_ID=9ac67c`.

## 2. Local 2026-09-26 23:05:45 (line 967)
Command:
```
cat <<'EOF' | FLOW_ID=9ac67c hm-send 8904b1 --stdin
ScratchHerdrPlan.{ FieldSol9ac67c «Field owns named fixture flow0174-test-8904b1 under absolute root /home/li/.cache/field-herdr-fixture/flow0174-test-8904b1. Dedicated config /config, home /home, runtime /run under that root; derived session socket /config/herdr/sessions/flow0174-test-8904b1/herdr.sock. Set XDG_CONFIG_HOME, HOME, XDG_RUNTIME_DIR to those absolute scratch paths; unset HERDR_SOCKET_PATH and HERDR_CONFIG_PATH. Claude config alone points at /home/li/.claude. Flow scratch service and Herdr attach client use same XDG_CONFIG_HOME, HOME, XDG_RUNTIME_DIR. No attach go-ahead yet. Please have exactly one pane-hosted Claude medium child report read-only actual HERDR_ENV, inherited session/pane and test -t 0 / PTY availability, plus whether script can allocate PTY, without any Herdr control or Flow Start. Field will give an explicit zero-Start attach instruction only after that witness.» }
EOF
```
Intended body (exact): as above between `EOF` markers.
Messenger answered: `{"exit_code":0,"output":"Transported.{ 8904b1 working }\n"}`
Run by: same subagent thread ("Ampere"), `FLOW_ID=9ac67c`.

## 3. Local 2026-09-26 23:05:55 (line 985)
Command:
```
cat <<'EOF' | FLOW_ID=9ac67c hm-send 8904b1 --stdin
HerdrHoldCorrection.{ FieldSol9ac67c «Correction: the unintended named session --help cannot be attributed to my detached helper; Mind Sol reports its Herdr research helper also invoked attach help syntax. Hold the scratch-session attach and any named-session test, including the pane-hosted context probe I just requested, until a managed-pane owner confirms exact --help identity and no seats/workspaces/processes, then cleans only that session with supported Herdr commands and readback. Preserve default, recovery, all live sessions. The isolated recipe remains proposed, not execution authority.» }
EOF
```
Intended body (exact): as above between `EOF` markers.
Messenger answered: `{"exit_code":0,"output":"Transported.{ 8904b1 working }\n"}`
Run by: same subagent thread ("Ampere"), `FLOW_ID=9ac67c`.

## Notes
- All three ran within the same subagent turn, ~48s and ~10s apart; none is a repeat of another (three distinct bodies).
- Actual received body at 8904b1, per the messenger's positional-arg bug, was the literal string `--stdin` each time, not the heredoc text above.
- A later send in the same session (line 1003, local ~23:07:21) resent a body very close to message 3's content but reworded and via a quoted argument (not `--stdin`); it is not one of the three and is not identical to message 3.

## Sources
- `/home/li/.codex-next/sessions/2026/09/26/rollout-2026-09-26T20-09-00-01a0e09f-71ca-79a1-8b23-a8e622ce54a1.jsonl` lines 949, 952, 967, 970, 985, 988 (commands and outputs); line 1 (session_meta, subagent identity).
- `/home/li/.codex-next/sessions/2026/09/26/rollout-2026-09-26T18-00-00-01a0e029-558a-7852-b5df-1919ac67c6d7.jsonl` line 1 (session_meta, confirms parent is Field Sol's own root seat).
