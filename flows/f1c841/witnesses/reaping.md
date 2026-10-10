# Reaping of 91ea9f and 3ec648

Method: observed on 2026-10-03, 12:30–12:34Z, by a subflow of Psyche.{ Fable f1c841 }, on the living's word that a replaced seat "has to be reaped" (2026-09-17) and the trial-reaping skill (close, archive, deregister; never message or wake). Identity came only from the messenger ledger (`hm-heartbeat-state`: route or retirement marker per flow) matched against `herdr pane list` (pane id, terminal id, title, native session) and `herdr pane process-info` (the `claude` argv's `--session-id` and `--name`). Quiet was checked by `jj status --ignore-working-copy flows/<id>`, a read of each pane, the process tree under each harness PID, and the modification times of each session's transcript, subagent transcripts and scratchpad. Nothing was typed into either pane; no message was sent.

## What was found

| | 91ea9f | 3ec648 |
|---|---|---|
| Ledger | route Bound: default / w1:p1A / term_65cdf2f55d0822c / psyche_fable_91ea9f, native thread 91ea9f9f-e4da-49dd-8102-9f235e68f41a; not retired | no route; retirement marker by f1c841 at 06:02:20Z for default / w1:p1J / term_65ce3003e05a534 / psyche_fable_3ec648, native thread 3ec6480d-5dcf-4615-92e3-7f6f69f9e7a3 (evidence `witnesses/retire-3ec648.md`) |
| Herdr pane | w1:p1A, term_65cdf2f55d0822c, title "Psyche.{ Fable 91ea9f }", agent claude, session 91ea9f9f-…, status done | w1:p1J, term_65ce3003e05a534, title "Psyche.{ Fable 3ec648 }", agent claude, session 3ec6480d-…, status done |
| Harness process | PID 839355 `claude --session-id 91ea9f9f-… --name "Psyche.{ Fable 91ea9f }"`, up 18h41m; children node (agent-intercom) 839894, rust-analyzer 1156540 | PID 1354995 `claude --session-id 3ec6480d-… --name "Psyche.{ Fable 3ec648 }"`, up 14h08m; children: three zsh wait-loops (1610106, 1905331, 1905427: two `until ! pgrep -f "nix flake check --no-build"` loops that match their own command line and so never end, one waiting on `rc=` in an old task output), rust-analyzer 1956679 with three proc-macro servers |
| Pane read | last turn 16:38 local Oct 2: "Published and retired. 91ea9f is closed" after 3ec648's retirement notice; prompt idle | last turn 00:30 local Oct 3: "The loop is stopped; nothing further is needed from this flow, and nothing is out."; prompt idle; "3 shells still running"; two finished background agents listed |
| Last transcript activity | 2026-10-03T00:23:44Z (later lines are harness autoreact-ledger records only) | 2026-10-03T06:30:03Z; its two listed background agents ended with `end_turn` at 03:23:48Z and 04:53:39Z |
| Writes since 06:31Z | none under its transcript directory or scratchpad | none under its transcript directory or scratchpad |
| `jj status --ignore-working-copy flows/<id>` | no changes in the lane | no changes in the lane |

Also found, outside both pane trees: an orphan of 3ec648's session (process group 1716948, parent systemd --user, up 9h27m): `tail -F …/3ec6480d-…/scratchpad/runs.out | ugrep … | while read …` from 3ec648's shell snapshot `snapshot-zsh-1790979898823-njvido`. Also a jj workspace `ws` at 3ec648's scratchpad (`(empty)`), left in place.

## What was ended

- 12:33:02Z `kill -TERM 839355` (91ea9f harness). Exited within 2 s; its node and rust-analyzer children ended with it; Herdr closed pane w1:p1A itself (`pane get` → `pane_not_found`).
- 12:33:13Z `FLOW_ID=f1c841 hm-deregister 91ea9f --session default --pane-id w1:p1A --terminal-id term_65cdf2f55d0822c --name psyche_fable_91ea9f`. Receipt: `Deregistered stale 91ea9f: psyche_fable_91ea9f (default/w1:p1A/term_65cdf2f55d0822c)`.
- 12:33:17Z `kill -TERM 1354995` (3ec648 harness). Exited within 1.5 s; the three wait-loops and rust-analyzer ended with it; Herdr closed pane w1:p1J itself (`pane_not_found`). No deregistration needed: its route was already removed by the 06:02Z retirement, whose marker stays.
- 12:33:31Z `kill -TERM -- -1716948` (3ec648's orphaned tail/ugrep/zsh group). Gone after 1 s.

## After

- `pgrep -af '91ea9f9f-e4da|3ec6480d-5dcf|njvido'`: nothing.
- `herdr pane list`: w1:p1B d86ec0, w1:p1C 01e496, w1:p1E 7de94a, w1:p1F 42265e, w1:p1G 41fa34, w1:p1H dea0ba, w1:p1K f1c841; every other seat unchanged.
- `hm-list`: d86ec0, 01e496, 7de94a, 42265e, 41fa34, dea0ba, f1c841; no STALE rows. Routes: 01e496, 41fa34, 42265e, 7de94a, d86ec0, dea0ba, f1c841. 3ec648's retirement marker retained.
- Untouched: lanes `flows/91ea9f/`, `flows/3ec648/` (jj status shows no change), transcripts `~/.claude/projects/-home-li-primary/{91ea9f9f-…,3ec6480d-…}.jsonl` and subagent directories, both scratchpads, the `ws` jj workspace.

## Not done

- "Archive" in trial-reaping: no archiving step was taken; the brief said to leave lanes, logs and transcripts untouched, and they remain as the archive. No retirement marker was written for 91ea9f (deregistered, not retired; `hm-retire` would need a frozen evidence file and the brief asked only for the reaping).
