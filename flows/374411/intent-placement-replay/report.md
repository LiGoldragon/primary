# One-family intent-placement replay

## Authorized operation

At 2026-11-13 17:15:33 -06:00, I used only the validated pinned Flow 0.54.7 owner client:

`/nix/store/fs53xwvgp9kbam4sbc25671hdrvnl37q-flow-configured-0.54.7/bin/flow-nexus-meta`

The exact query/apply/query command sequence is in `exact-commands.sh`. The only mutating request was the single one-argument contents of `/home/li/primary/flows/9adeee/early-live/payload.datom`, whose outer variant is `Configure.Metaflows`.

## Pre-apply observations

- Fresh `Configuration` parsed as 19 fields. Its position-ten Metaflows family was structurally identical to the retained live baseline: 38 declarations and no family drift.
- The separately completed payload audit found the same 38 addresses/order, all seven non-module declaration fields preserved, exactly 27 authorized Psyche/Mind module-list edits, and 11 unchanged Field rows. Evidence: `preflight/report.md`.
- The occupied owner was active/running at PID 1016330, invocation `d59f4448816245ed9ec51938079be49f`, executable in the pinned `fs53…` store path. The ordinary/meta socket inode/owner records and six native pane/session identities were captured before apply.

## Receipt and readback

The one apply began at 17:15:33.664792519 and ended at 17:15:33.684420560 -06:00. Its exact reply was:

`Configured.Replaced`

A fresh `Configuration` completed at 17:15:33.729372705. Its Metaflows family is structurally and canonical-byte identical to the payload body (`payload-after.diff` is empty). Only configuration family index 9 changed. Every other family, including all counters, is identical. In particular, ConfiguredNexus and ConfiguredSendServers are exactly equal before/after; their canonical hashes are recorded in `configuration-family-hashes.json`.

## Independent live continuity

The systemd unit properties, daemon PID/start tick/invocation/executable/cmdline/cgroup, socket inode/owner records, socket process-owner listing, and all six native pane/session/terminal identity records are identical before and after. This establishes continuity independently of the configuration receipt; details are in `live-continuity.json` and the paired raw files.

The bounded application journal contains seven informational records and no error/failure/panic/rejection/refusal match. It records no restart. The daemon PID and invocation remained unchanged.

## Evidence

All raw readbacks and comparisons are under `raw/`: `configuration-before.datom`, `apply-reply.datom`, `configuration-after.datom`, `pre-apply-verification.json`, `post-apply-verification.json`, `configuration-family-hashes.json`, `payload-after.diff`, `live-continuity.json`, paired unit/process/socket/herdr files, `application-journal.txt`, and `operation-timeline.txt`.

No flow was refreshed or restarted; no other configuration family, service, host, profile, or source was changed.
