# Quota accounting proposal

## Current home

The latest relayed living ruling places quota accounting in **Persona for now**. This is a provisional placement in the existing Persona component, not authorization to create a new component or implement a collector, hook, scheduler, or Persona quota field.

The ruling's source is Claude's secondary transcript record:

```text
source_path: /home/li/.claude/projects/-git-github-com-LiGoldragon-secondary/57a7aa02-e52d-4266-8746-6770ff770d11.jsonl
source_message_id: 73258a28-eb2d-4597-91c2-0bdb51bce21f
source_timestamp: 2026-09-15T17:44:25.671Z
sha256_utf8: 0fae92… (source attribution supplied by the relay record)
```

## Read-only facts to preserve in Persona

Persona would store or expose periodic snapshots with the harness, subscription/limit name, used percentage, remaining percentage, window duration, reset timestamp, observation timestamp, and source method. Units must remain explicit: percentages are quota-window percentages; reset and observation values are UTC timestamps; token counts are separate usage data and are not the rate-limit denominator.

Codex currently exposes `account/rateLimits/read` for the root `codex` limit. The initial witness records 33% used and 67% remaining on a seven-day window, with reset `2026-09-19T15:05:28Z`. The same witness derives remaining-window allowance and observed used pace from timestamps. Claude's live quota value is unavailable in this snapshot and must remain unknown until a supported statusline capture exists.

The 14%/day line in the earlier protocol is an unapproved target. It may be shown as a comparison line in a future report, never as an adopted policy. No accounting implementation exists in this proposal.

## Sources

- `flows/6cc91b/reports/quotaProtocol.md` (read in full; draft protocol and read-only method survey)
- `flows/5f4fea/witnesses/quota-initial.md` (fresh Codex measurement)
- Secondary source attribution above and `flows/692df8/log.md:37`
