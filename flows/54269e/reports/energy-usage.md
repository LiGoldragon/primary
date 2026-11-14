# Claude and Codex usage over their weeks (data for one graph)

Gathered Sat 2026-11-14 about 09:10 CST (America/Chicago). Nothing was changed; no Codex reset was redeemed.

CSV: `/home/li/primary/flows/54269e/reports/energy-usage.csv`, columns `provider,week_start,week_reset,timestamp,percent` (4586 rows, times local with offset, percent is whole percent used).

## Current reading (about 09:09)

| Provider | Used | Week start | Week reset |
|---|---|---|---|
| Claude | 1% (statusline cache, 09:08:59); Energy's own last reading 0% at 09:05:02 | Sat 2026-11-14 07:00 CST | Sat 2026-11-21 07:00 CST |
| Codex | 38% (62% left), allowed, read live 09:09 | Wed 2026-11-11 20:21:11 CST (reset minus 7 days) | Wed 2026-11-18 20:21:11 CST |

## Weeks in the CSV

| Provider | Week | Rows | First point | Last point |
|---|---|---|---|---|
| Claude | Oct 31 08:00 CDT (07:00 CST) to Nov 7 07:00 CST | 604 | Nov 4 20:33, 42% | Nov 7 06:53, 95% |
| Claude | Nov 7 07:00 to Nov 14 07:00 | 1998 | Nov 7 06:58, 0% | Nov 14 06:23, 100% (first 100% at 04:05) |
| Claude | Nov 14 07:00 to Nov 21 07:00 (current) | 10 | Nov 14 06:24, 0% | Nov 14 09:08, 1% |
| Codex | Nov 4 20:19:11 to Nov 11 20:19:11 | 1281 | Nov 4 20:35, 5% | Nov 10 18:03, 100% |
| Codex | Nov 11 20:21:11 to Nov 18 20:21:11 (current) | 693 | Nov 12 14:17, 18% | Nov 14 09:09, 38% |

## Where each number came from

- Energy Nexus (`energy-nexus.service` and `energy-translator.service`, user units at place `main`, running; repos `/git/github.com/LiGoldragon/energy-nexus`, `signal-energy-nexus`). Its daemon keeps every successful reading in `Memory.history`, saved in `~/.local/state/nexus/main/energy.rkyv` (envelope `ENXMEMRY` version 2). The CLI has no history query (`Read.Provider` answers the latest reading only, `energy-pace` only the pace), and local compilation is disabled on this host, so I could not build a loader with the repo's types. I copied the file to the scratchpad and decoded it by hand from its byte layout: 4628 readings, each `At` (Unix seconds), provider, and the `Week` window's `Usage` percent and `ResetTime` (a `FableWeek` window is also recorded for Claude, not exported). The layout was checked against the live Codex read (38%, reset 1795054871) and against `flows/743764/night-plan.md` (82% at 18:27 and 93% at 22:27 on Nov 13, plan says ~18:30 82% and 22:27 92%), and every decoded percent is 0 to 100 with a plausible reset. This is a hand decode, not the repo's own reader.
- Week reset values are read from the readings; week_start is week_reset minus 7 days (windows are 10080 minutes). Claude resets jitter by a second (06:59:59, 07:00:00, 07:00:01), and are rounded to the minute; Codex Nov 11 20:19:11 and :12 are merged to :11. Readings with identical timestamps were collapsed.
- Current Claude: `~/.cache/claude-rate-limits.json` (written by the statusline: `seven_day.used_percentage 1`, `resets_at 1795266000`, `at` 09:08:59), added as the last Claude row. Energy's `Read.Claude` answers `Refused.ProviderDown.Claude` right now although its last stored Claude reading is 09:05:02.
- Current Codex: `/git/github.com/LiGoldragon/makeshift-tools/codex-usage` (read-only, per `knowledge:codex-reset`): `usedPercent 38`, `resetsAt 1795054871`, `ordinaryUsageAllowed true`, three resets available (expiring Nov 30 14:15, Dec 1 16:44, Dec 12 16:38), added as the last Codex row at 09:09:42. `energy-nexus 'Read.Codex'` gave the same 38% from its reading of 06:02:45.
- The night-plan and handover readings of Claude (82% at 18:30, 83% at 19:12, 88% at 21:21, 92% at 22:27 on Nov 13) were not added: Energy's history already holds that period at finer resolution and agrees.

## What is missing or odd

- Energy's history starts Nov 4 20:33 (Claude) and 20:35 (Codex): nothing earlier is recorded, so the Claude week of Oct 31 and the Codex week before Nov 4 20:19 are absent, and the first week of each is partial. No earlier week reset times are recorded (Claude's Oct 31 08:00 CDT start is derived).
- Codex has no readings from Nov 10 18:03 (100%) to Nov 12 14:17 (18%, in the new window), about 44 hours, while Energy's Codex read was broken (a handover records a removed Codex binary replaced by meta Configure). The old window's reset (Nov 11 20:19:11) and the new window's (reset Nov 18 20:21:11, so its start is 20:21:11) differ by 2 minutes; why the window moved is unrecorded (no redemption by this flow; three credits remain available). The week_start for the current Codex week is derived, no reading exists at that moment.
- Claude Nov 7 week reached 100% at 04:05 on Nov 14. A reading at 06:24:13 already shows the new window at 0% with reset Nov 21, so the Claude week reset about 36 minutes before the nominal 07:00; cause not recorded.
- The first 35 Claude readings carry the Week window only; FableWeek appears later. Reading density varies (several per minute in busy stretches, tens of minutes apart in quiet ones); Energy reads only on turn ends and resets, so quiet stretches have no points.
- 839 Codex readings carry a different allowance byte (0 against 1), inferred to be Disallowed (Codex out); not verified against the type, and the percent is recorded either way.
- Raw copy used: `/tmp/claude-1001/-home-li-primary/54269edf-f13c-57e5-bc2b-8d934731c19d/scratchpad/w/e.rkyv` (decoded rows in `hist.json` beside it).
