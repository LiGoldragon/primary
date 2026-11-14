# Why Energy answered `Read.Claude` with ProviderDown at 09:09 (Sat 2026-11-14)

Read only. Nothing was changed, restarted or redeemed. One `energy-nexus 'Read.Claude'` question was asked at 09:11 (the ordinary public read). The usage endpoint was not called by hand.

## Verdict

The failure was a five-minute gap, roughly 09:05 to 09:10. In that time every Claude read Energy attempted failed, and it has recovered with no one touching it: Claude readings were stored at 09:10:25, 09:10:33 and 09:11:20 (Week 1%), and `Read.Claude` at 09:11:43 answers `Week 1 ... FableWeek 0`. The weekly reset did not cause it, because reads at 06:24:13, 07:00:00 and from 08:49 to 09:05 succeeded on the new window. The best-supported hypothesis is a transient non-2xx answer from `https://api.anthropic.com/api/oauth/usage`, most likely a 429. The translator turns any failure into `Down` without logging it, so the status code is unknown. Fixing this takes code; configuration has nothing to change. Neither `ethos-565bc8` nor `schedule-pace` touches the Claude read path.

## How Energy obtains Claude's reading (0.3.3, origin/main 2623947)

- The daemon's `Read.Claude` question goes to the schedule (`crates/daemon/src/schedule.rs`, `Event::Question`). If the latest Claude reading is no newer than the last Claude turn end (`Track::stale`), it reads first. Otherwise it answers from memory.
- A read is `Emission::ClaudeUsage` sent to the translator on `energy-emission.sock` (`crates/daemon/src/main.rs`, `Nexus::attempt`). Any outcome other than `Observed` becomes `Refused::ProviderDown(Claude)`.
- The translator's `claude_reading` (`crates/translator/src/lib.rs`) reads the credentials file named in its memory, takes `claudeAiOauth.accessToken`, and sends `GET https://api.anthropic.com/api/oauth/usage` with `anthropic-beta: oauth-2025-04-20` (ureq 3.5.1, no timeout set). Each of the following is `None`, and so `Outcome::Down`, with nothing logged: an unreadable file, bad JSON, a missing token, a transport error, any non-2xx status (ureq 3 makes 4xx and 5xx errors), or a body that is not JSON.
- `claude_document` never fails on shape. Missing `five_hour`, `seven_day` or `weekly_scoped_shares` fields leave out windows and still return `Some(Reading)`. A new-shaped or empty JSON answer therefore reads as a reading with fewer windows, never as down.
- Configuration: `energy-nexus-meta` takes only `Configure` and has no read input. The translator memory `~/.local/state/nexus/main/energy-translator.rkyv` (142 bytes, last written Nov 12 14:20) holds `/home/li/.nix-profile/bin/codex`, `/home/li/.local/bin/flow-nexus` and `/home/li/.claude/.credentials.json`. These are the path strings visible in the archive (`strings`), so the credentials path matches Claude Code's own file.
- When a read fails, the schedule (`Event::Finished`) passes the `Refused` to every waiting question, even when memory holds a reading only minutes old. Memory does not move on, so every later question in that period reads again and gets the same failure until a read succeeds.

## Observations

- Both units have been active since 01:14:05 with no restart. `journalctl --user -u energy-translator.service -u energy-nexus.service --since 06:30` returns `-- No entries --`. The last lines are the translator resubscribing to Flow at 02:37 and 02:38. A failed Claude read leaves no journal line.
- `~/.claude/.credentials.json` was last written at 07:34. Its `expiresAt` is 15:34:30 today, subscription `max`, tier `default_claude_max_20x`. The token was valid throughout 09:05 to 09:10 and the file did not change during or after the failure.
- I decoded the stored Claude readings from `energy.rkyv`: the earlier flow's hand decode plus my own scan of a copy taken at 09:11:20.
  - 06:23:49: Week 100%, reset Nov 14 07:00.
  - 06:24:13: Week 0%, reset Nov 21 07:00. This is the new window, already reported 36 minutes early.
  - 07:00:00: the reset alarm read, which succeeded.
  - Successful reads at 08:49:28, 09:03:45, 09:04:19, 09:04:51, 09:04:52, 09:04:54 and 09:05:02. That is six reads in 77 seconds.
  - No Claude reading between 09:05:02 (or 09:05:04, depending on how one value is decoded) and 09:10:25.
  - Codex readings in that period, at 09:08:57, 09:09:11, 09:10:01 and 09:10:03, succeeded. Turns were ending, the daemon and translator were working, and the network to OpenAI was up.
  - From 09:10:25, Claude readings succeed again at Week 1%.
- `~/.cache/claude-rate-limits.json` is written by `/home/li/.claude/statusline.sh` (the `statusLine` command in `~/.claude/settings.json`). The script saves the `rate_limits` object that Claude Code passes on stdin with each statusline update. It never calls `/api/oauth/usage`. Its figure, `seven_day.used_percentage 1` at 09:08:59, is Claude Code's own and comes by a separate path. Claude Code was getting API answers at 09:08:59.
- Neither `schedule-pace` (8e91223) nor `ethos-565bc8` (08fcb7f) changes `claude_reading`, `ClaudeUsage::emit` or the `Down` mapping. Their diffs to these files are about pace, schedule and generated types. Local `main` (e572252) is older than 2623947 and has no schedule at all.

## Hypotheses

1. Best supported: `/api/oauth/usage` answered 429 or another non-2xx status between about 09:05 and 09:10. Supporting evidence: the token was valid and unchanged, the shape cannot cause it, Codex reads were healthy, and recovery came by itself. A burst of six reads in 77 seconds just before the failure, plus questions from flow 54269e around 09:05 to 09:09 that each triggered another read, fits a rate limit. Public reports describe this endpoint rate-limiting hard and sharing a bucket with Claude Code sessions' own usage polling ([31637](https://claudeissues.com/issue/31637-bug-api-oauth-usage-endpoint-aggressively-rate-limits-making-usage-monitoring-un), [30930](https://claudeissues.com/issue/30930-bug-api-oauth-usage-endpoint-returns-persistent-429-for-claude-max-users-retry-a), [31319](https://claudeissues.com/issue/31319-statusline-usage-data-unavailable-with-multiple-concurrent-sessions-oauth-rate-l)). Evidence against a simple per-client limit: Energy has stored up to 18 successful Claude reads in 5 minutes before now.
2. Alternative: a transient 5xx or transport error from api.anthropic.com on that endpoint. The stored evidence cannot tell this apart from 1.
3. Unlikely: this morning's weekly-limit hit. That limit concerns model usage. Reads at 06:24 and 07:00, near the limit and after the reset, succeeded.

## Unknowns

- The HTTP status, or error, of each failed read. It is not logged or stored anywhere.
- How many Claude reads were attempted between 09:05 and 09:10. Failures are not recorded.
- Whether Claude Code sessions on this host poll `/api/oauth/usage` and share Energy's bucket.
- Why the Anthropic week rolled over at 06:24 rather than 07:00. It did not cause this failure.

## What the fix is

The fix belongs in code. None of it is in 0.3.3 or in either branch:
- The translator should keep the failure. It should log it, or carry it in its `Down`, with the status and `retry-after`, so the next gap has a cause on record.
- The daemon should answer a question whose read failed from the latest reading in memory, marked with its age, rather than `ProviderDown`, and it should hold further reads until the `retry-after` passes.

No configuration change applies: the credentials path is correct and the token is fresh.
