# Witness: reaping of the old Fable lineage (f1c841, 91ea9f, 3ec648)

Observer: subflow of Psyche Fable 9fb0ad (thread 9fb0ad7f-bb95-4b5d-80de-c369fa25ebfe), 2026-10-03.

Method: observation by `hm-list`, `herdr agent list`, `herdr pane list`, `ps`, `systemctl --user show`, `orchestrate 'Observe.Locks'`, before and after; the deployment report watched with `inotifywait` (bounded 580 s); f1c841's claude process ended with SIGTERM, its exit awaited with `tail --pid`. Scope by the split settled with 5578cc: 9fb0ad reaps f1c841, 91ea9f, 3ec648; 5578cc reaps d86ec0 and 01e496. This flow did not touch d86ec0 or 01e496.

## Messages sent (as FLOW_ID=9fb0ad), receipts as printed

1. to 6e782c "9fb0ad owns the reaping of the old seats and is doing it now; will message when done." -> `Transported.{ 6e782c done }`
2. to 5578cc "9fb0ad does the whole reaping (d86ec0, 01e496, then f1c841 last); please stand down from it. ..." -> `Transported.{ 5578cc working }`
3. to 6e782c "Settled: 9fb0ad does the whole reaping; 5578cc asked to stand down. ..." -> `Transported.{ 6e782c done }`
4. to 5578cc "Split accepted: 9fb0ad reaps f1c841, 91ea9f, 3ec648; 5578cc reaps d86ec0 and 01e496. 9fb0ad has not touched d86ec0 or 01e496." -> `Transported.{ 5578cc idle }`
5. to 6e782c "Settled with 5578cc: ..." -> `Transported.{ 6e782c done }`

## Before (06:52-06:54 CST)

- `hm-list`: rows 7de94a, 42265e, 41fa34, dea0ba, 9fb0ad, 5578cc, 6e782c, and `-  psyche_fable_f1c841  default  working` (flow binding already retired, see witnesses/retire-f1c841.md). No row for d86ec0, 01e496, 91ea9f, 3ec648.
- Herdr agents/panes: w1:p1K `psyche_fable_f1c841` (claude session f1c84105-972f-4ef6-a158-c66638429e7b, working), plus p1E, p1F, p1G, p1H, p1M (9fb0ad), p1N (5578cc), p1P (6e782c). No pane for d86ec0, 01e496, 91ea9f, 3ec648.
- Claude processes: 2081112 (f1c841, session f1c84105-...), 2823995 (9fb0ad), 2825212 (5578cc), 2826200 (6e782c). None for 91ea9f, 3ec648, d86ec0, 01e496.
- f1c841's process tree at 06:54:26: 2081112 claude; 2171375 zsh running `while pgrep -f "nix flake check path:.../claude-answers"; do sleep 20; done` (the pgrep matched its own shell, so it never ends); 2299274 and 2312547 zsh each with a nixfmt and `tail -2` started about 05:45 earlier and never finished.
- Successors verified: 9fb0ad is f1c841's successor (9fb0ad's launch brief, read from its process args: "Handover brief: Psyche Fable, successor of f1c841"; registered in hm-list). f1c841's own launch args name it "successor of 3ec648, which succeeded 91ea9f".
- 6e782c's log line 11 relays 5578cc's report that d86ec0 was stopped and 01e496, 91ea9f, 3ec648 were already gone (a claim; this flow witnessed only the absence of their processes and panes).
- Home build unit `f1c841-home-build-regular.service` at 06:52: active (running), its own cgroup under app.slice (not in the claude process tree). At 06:54:05, before any ending step: `ActiveState=inactive SubState=dead Result=success ExecMainStatus=0`. It finished on its own; deployment.md records "Result=success, 06:53".
- Locks at 06:54:05: `Observed.Locks.[ { 11771 PrimaryPublish f1c841 [ /home/li/primary/.PrimaryPublish.lock ] «Publish flows/f1c841/reports/deployment.md» } ]`. Ending was held until it cleared; re-read just after: `Observed.Locks.[]`, origin/main at 33c772219 "Psyche Fable f1c841: deployed orchestrate 0.37, flow 0.23, message 0.19 as regular".

## Deployment report wait

`inotifywait -t 580 -e close_write,moved_to,create --include 'deployment\.md' flows/f1c841/reports` -> `./ CLOSE_WRITE,CLOSE deployment.md` at 06:53:54. After: mtime 2026-10-03 06:53:54.497 -0600, 12449 bytes; last headings `## State reached when the living ordered the seat wound down (06:53)`, `## Next commands, for the successor (in order, each witnessed)`, `## Sources`.

## Ending

- 06:54:26 `kill -TERM 2081112` -> rc 0. `timeout 15 tail --pid=2081112 -f /dev/null` -> rc 0 (exited). Its process groups 2171375, 2299274, 2312547 were gone with it.
- `herdr pane close w1:p1K` -> `{"error":{"code":"pane_not_found","message":"pane w1:p1K not found"}}`: the pane had closed when claude exited.
- Not done: hm-retire for f1c841 (already done, witnesses/retire-f1c841.md). Nothing was done to 91ea9f, 3ec648 (already ended), d86ec0, 01e496 (5578cc's part).

## After (06:54:34)

- `hm-list`: 7de94a, 42265e, 41fa34, dea0ba, 9fb0ad, 5578cc, 6e782c. The f1c841 row is gone.
- Herdr agents: p1E, p1F, p1G, p1H, p1M, p1N, p1P. No p1K.
- Claude processes: 9fb0ad, 5578cc, 6e782c only.
- `f1c841-home-build-regular.service`: inactive, dead, Result=success (unchanged from before the ending).
- `orchestrate 'Observe.Locks'` -> `Observed.Locks.[]`: no lock is held by an ended flow.
