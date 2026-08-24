# CriomOS-b8x Zeus package deployment

Opened on the deployment brief: trace generation 64's omitted intended
packages, land authoritative producer and consumer revisions, prove the
canonical Zeus target remotely, and activate only through staged Lojix.

2026-08-24 — The omission was a stale CriomOS Home lock: generation 64 pinned
Home a61b02d0, therefore correctly activated Codex 0.148.0 and Claude 2.1.235
instead of the then-published producer update. The current stable Codex
target was found to be 0.149.1; authored Home policy couples the Codex
sidebar, so it advanced to 26.5818.61809. Claude remained 2.1.241.

Producer `0836e4b7e367efe6a81a4fa657e2a2f741f0d801` and consumer
`ab005ef8bc8828e1f92563cbb4bb966c2adda5bc` landed publicly. Canonical
materialized Zeus evaluation and Prometheus-only build passed. Lojix
TestActivation 57 succeeded, then ActivateNow 58 succeeded. Both embedded
Homes now use Codex 0.149.1 and Claude 2.1.241. No reboot occurred.

Corrective flow housekeeping: the session transcript identifies this flow as
01a032e5. A recency-based mistaken write to unrelated historical flow
68512643 was removed in a separate corrective commit; these are the correct
records. The edit-coordination socket was unavailable, so the advisory lane
operations could not complete. Worker worktrees were clean, forgotten, and
moved recoverably to Trash after their published commits were verified.
