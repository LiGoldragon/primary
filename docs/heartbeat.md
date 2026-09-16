# Heartbeat POC

`tools/heartbeat.mjs` is one bounded, read-only tick. It reads only its configured quota event log and configured lane-tip, report, and last-turn files. The event-log shape accepts the monitor's `kind: "quota"`, `remainingPercent`, `windowMinutes`, `resetsAt`, and `observedAt` record.

The interval rule is deterministic: remaining quota `>=50%` is 15 minutes, `>=20%` 30, `>=5%` 60, and lower 120. Unknown or stale quota is 60 minutes and explicitly labeled. The committed timer is deliberately a conservative 60-minute source payload. The event's `interval` is the dynamic recommendation for an activation-time declarative scheduler projection; this POC never edits its own timer.

One Luna classifier receives only the curated snapshot and returns a bounded major enum: `main_promoted`, `activation`, `failure`, `living_word_unseen`, `successor_ready`, `none`, or `unavailable`. It has no authority to run commands or trigger repairs. The default delivery is always a report file with `file_only`; no peer transport is attempted unless a future explicit configured adapter records its own receipt.

`--sandbox read-only` limits the model job but does not itself isolate credentials. A deployed runner must provide credential isolation separately. This POC never includes credential paths, environment values, or raw account responses in its snapshot.
