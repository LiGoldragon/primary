# Seats ended, 2026-09-28

Subflow of main flow 8904b1. It ended every machine seat on this host apart from the main flow and Psyche Opus dc53b4, following the psyche's order.

## Excluded tree (method: `ps` ancestry walk from the subflow shell, `herdr pane process-info --pane w1:p8`)

- Main flow Psyche Fable 8904b1: Herdr session `default`, pane w1:p8. Claude pid 110690 (parent shell 110561, herdr server 4957). Its child agent-intercom node is pid 110797. Subflows are in-process agents, and their shells are children of 110690.
- Psyche Opus dc53b4: pane w1:pC, Claude pid 128289 (shell 128160, intercom node 128845), cwd /home/li/wt/primary/opus-sonnet-56ae53. Not prompted and not touched.

## Inventory before ending (method: `herdr session list`, `herdr pane list`, `herdr pane process-info --pane`, with HERDR_SOCKET_PATH set per session; `hm-list` for flow ids)

Session `default`:
| pane | seat | pid (shell) | cwd | thread / session |
|---|---|---|---|---|
| w1:p1 | codex gpt-6-sol, no flow row | 7554 (4979) | /home/li/primary | 01a0de4c-554d-7343-bbc5-e4256ae5366f |
| w1:p2 | MindV2 Astra 6fe957 | 17334 (16720) | /home/li/primary | 01a0dfdc-a500-7271-8f54-e446fe9578dd |
| w1:p3 | FieldV2 Luna 19ff9f | 30381 (29833) | /home/li/primary | 01a0dfef-25bd-7dc3-9f6d-50d19ff9f733 |
| w1:p4 | bare zsh | 105103 | /home/li/wt/primary/56ae53 | - |
| w1:p7 | Field Luna 184bd8 | 109434 (106482) | /home/li/wt/primary/field-packet-56ae53 | 01a0e021-aa68-72a2-a8df-7d6184bd8c00 |
| w1:p9 | Field Sol 9ac67c | 116098 (115771) | same | 01a0e029-558a-7852-b5df-1919ac67c6d7 |
| w1:pA | Field Astra 22e12b | 119371 (117244) | same | 01a0e02b-9036-7361-9078-55222e12bb1f |
| w1:pB | bare zsh | 127897 | /home/li/wt/primary/opus-sonnet-56ae53 | - |
| w1:pD | Mind Luna 139366 | 129350 (129231) | /home/li/primary | 01a0e032-e8aa-7131-90c4-a54139366ece |
| w1:pE | bare zsh | 136564 | /home/li/wt/primary/opus-sonnet-56ae53 | - |
| w1:pF | Psyche Sonnet 38f337 (claude-sonnet-5) | 136885 (136762), intercom 136987 | /home/li/wt/primary/opus-sonnet-56ae53 | 38f33758-72c0-4c2a-ad49-8ffeb8e310fa |
| w2:p1 | codex gpt-6-astra, no flow | 3047349 (3047255) | /home/li/primary | new thread |
| w3:p1 | codex gpt-6-astra "Confirm main flow skill", no flow | 3116721 (3109078) | /home/li/primary | 01a0e3d8-7d7f-7712-8fca-54f5ac3a3e17 |

Session `recovery-56ae53` (herdr server pid 301649):
- w1:p1 is a bare zsh (301671), cwd /home/li/primary.
- w1:p2 is a bare zsh (302362), cwd /home/li/primary.
- w1:p3 is MindV2 Sol c56100, codex pid 318363 (shell 310531), cwd /home/li/wt/primary/mind-sol-successor-56ae53-target, thread 01a0e0a1-7075-7cc2-928d-13fc56100504.

Sessions `messaging-build` and `--help` were stopped with no server.

No headless Claude, Codex or Pi seat processes ran outside the panes (method: `ps -eo pid,ppid,args` filtered on claude/codex/pi). The remaining codex processes are the app-server services 1936 and 1960. The /tmp/codex-daemon-1001/3b2c… socket belongs to 1960 (method: `ss -xlp`). About 40 agent-intercom node and node_repl processes are children of service 1960. They were left untouched because they belong to a service.

## Secured (method: `jj st` snapshot in each copy, `jj commit <paths>`, `jj duplicate … -o main@origin`, `jj rebase -r` of the fresh duplicate only, then push)

- Field Luna 184bd8: flows/184bd8/log.md. Source commit 85ca45a9 was made in field-packet-56ae53, and duplicate 78114603 is on main.
- Field Sol 9ac67c: flows/9ac67c/log.md. Source commit 5f156bba, duplicate dd14e90e.
- Psyche Sonnet 38f337: flows/38f337/artifact-src/startup-anatomy.html, flows/38f337/artifact-src/startup-syntax.html, flows/38f337/log.md, flows/38f337/new-sonnet-first-prompt.md and flows/56ae53/sonnet-recovery/main-flow-hook-state/psyche_sonnet_9c7514/38f33758-72c0-4c2a-ad49-8ffeb8e310fa.count. Source commit 63ea772d, landed as bf12724d.
- Main moved from 2a6d6ac59038 to bf12724de998749c5a1825f7c3280233a82bd3fa. Read-back: `git ls-remote git@github.com:LiGoldragon/primary.git refs/heads/main` returned bf12724de998749c5a1825f7c3280233a82bd3fa.
- Patch (outside flows/): secured-0928/mind-sol-c56100.patch holds .native-seat-receipts/mind-sol-of-56ae53-recovery.json, which was uncommitted in mind-sol-successor-56ae53-target.
- Copies of Herdr state saved before deletion: secured-0928/herdr-session-messaging-build.json and secured-0928/herdr-session-dash-dash-help.json.
- /home/li/primary had no changes.
- flows/56ae53/opus-recovery/…/dc53b4be-….count in opus-sonnet-56ae53 belongs to Opus, which survives. It was left uncommitted.
- A re-check after ending the seats (`jj st`) found no late writes.

## Ended (method: `herdr pane close <id>` after confirming the expected pid in `pane process-info`, then `kill -0` on each pid)

Closed at 10:17:32–10:17:38: default w1:p1, p2, p3, p4, p7, p9, pA, pB, pD, pE, pF, w2:p1 and w3:p1, plus recovery-56ae53 w1:p1, w1:p2 and w1:p3. All seat, shell and intercom pids listed above were confirmed gone. Workspaces w2 and w3 went away with their panes.

## Sessions

- `herdr session stop recovery-56ae53`: server 301649 gone. It was then removed with `herdr session delete recovery-56ae53`.
- `herdr session delete messaging-build`: deleted.
- `--help` (stopped) could not be deleted. Its name parses as a flag, and `./--help` is rejected by the name validator. It remains listed.
- Final `herdr pane list` on default shows only w1:p8 and w1:pC. `herdr session list` shows only default and `--help`.

## Survivors confirmed alive (`kill -0`)

110690, 128289, 128845, herdr server 4957, codex app-servers 1936 and 1960.

## Services left running (`systemctl --user` / `systemctl`)

flow-nexus, flow-nexus-next, message-daemon, message-nexus-next, orchestrate-nexus, codex-remote-control, codex-remote-control-next, opencode, aggregator-daemon, pueued (no running task), and the system service lojix.service.

## Registry rows now pointing at nothing (`hm-list` after ending; not edited)

- Session default, STALE: 139366 mind-luna-139366, 184bd8 field-luna-184bd8, 22e12b field-astra-22e12b, 38f337 psyche_sonnet_9c7514, 6fe957 mind-astra-6fe957, 9ac67c field-sol-9ac67c.
- Session recovery-56ae53 (deleted): c56100 mind_sol_c56100.
- Session messaging-build (deleted): 26c50c, 31147a, 504461, 56ae53, 5f38bc, 93ba9f, 98eb43, a676b3, b7ba00, b7da5d, e167d8, e71dab, f5a74e.
- Row 8904b1 still shows agent `psyche_fable_b7ba00`.
- The Flow Nexus registry was not read: `field-clj 'observe []'` refused with `:no-caller`.
