# Initial Codex quota witness

## Observation

Observed at `2026-09-15T17:37:09.751612Z` through the local Codex app-server WebSocket control socket, using the `WS` client in `flows/024bc7/tools/codex_wake.py`. The request was `account/rateLimits/read`.

The root Codex limit returned:

```text
limitId: codex
planType: pro
primary.usedPercent: 33
primary.windowDurationMins: 10080
primary.resetsAt: 1789830328 (2026-09-19T15:05:28Z)
secondary: null
credits.hasCredits: false
credits.unlimited: false
credits.balance: 0
spendControlReached: false
rateLimitReachedType: null
```

No account identifier or reset-credit identifiers are recorded here. Token counts are not treated as the quota denominator.

## Interpretation

The returned root-limit remainder is `100 - 33 = 67%`. The seven-day window opened at `2026-09-12T15:05:28Z`. At the observation time, approximately `2.105 days` had elapsed and `3.894 days` remained.

Reproducible arithmetic from this snapshot:

```text
elapsed_fraction = (2026-09-15T17:37:09.751612Z - 2026-09-12T15:05:28Z) / 7 days
                 ≈ 0.3007 (30.07%)
used pace        = 33 / 30.07 ≈ 1.10x of elapsed-window percentage
remaining/day    = 67 / 3.894 ≈ 17.21 percentage points/day
```

The `1.10x` comparison is an arithmetic pace description for this snapshot, not an agreed policy. The earlier historical snapshot at approximately `2026-09-15T17:23Z` reported `32%` used with the same reset (`flows/692df8/reports/quotaVisualization.md:9-12`); it is retained as historical context, not re-observed here.

The psyche's `14%/day` line remains a draft protocol target, not an adopted quota policy. Claude's quota is unknown from this witness; no Claude measurement was attempted.

The latest relayed living ruling places quota accounting in **Persona for now**. This is a source-attributed placement note, not a measurement or authorization for a Persona implementation: `source_message_id=73258a28-eb2d-4597-91c2-0bdb51bce21f`, secondary Claude transcript timestamp `2026-09-15T17:44:25.671Z`, supplied source hash prefix `0fae92…`.

## Sources

- Local app-server method: `account/rateLimits/read`.
- Client: `flows/024bc7/tools/codex_wake.py`.
- Historical snapshot: `flows/692df8/reports/quotaVisualization.md:9-12`.
- Draft target: `flows/6cc91b/vision/quotas.md:7-11`.
