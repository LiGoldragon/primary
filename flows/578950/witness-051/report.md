# Flow 0.51 native witness

Started 2026-11-04 20:08:27 CST; deadline 20:23:27 including cleanup.

Artifact: `/nix/store/5w5sqfmcndg8cr1dm72yr8iy591kmxsa-flow-configured-0.51.0`, Flow `916b54574ae0024b893a9f4252f2e97704db48c1`, configured by CriomOS-home `20f11a9f`. Opus supplied and owned the isolated `flow-nexus-051-witness` unit. Both client scripts and the unit executable/socket mapping were read back before use.

Actual executor session `01a1a968-cdb4-7bd2-98df-b3e578950121` adopted only as isolated `Mind witnessSender Secondary`; adoption returned `578950`. It was never stopped.

## Codex results

Disposable `Mind witness Secondary`: `4f913d`, native `01a1a977-78a4-77c0-a914-17f4f913d831`, pane `wQ1:p1`. Actual Working was captured immediately before each request.

| Priority | Original Queued cursor | Subsequent event cursors | Reply | Elapsed seconds |
| --- | --- | --- | --- | --- |
| Soft | 1 | Attempting 2, Uncertain 3 | `SendAccepted.{ 1 Uncertain }` | 10.471 |
| MiddleAbrupt | 4 | Attempting 5, Uncertain 6 | `SendAccepted.{ 4 Uncertain }` | 11.189 |
| HardAbrupt | 7 | Attempting 8, Uncertain 9 | `SendAccepted.{ 7 Uncertain }` | 12.678 |

ObserveSends cursors are **event cursors**: they advance with state changes. Each final acceptance retains the original Queued admission cursor and reports the current Uncertain state. The earlier writer description of a constant cursor across transitions was disconfirmed by these raw streams.

One logical request was in flight at a time to one controlled target. This witnesses target/sequence/cursor/state association, not private logical-ID association. Private-ID invariants remain the separate immutable test/review evidence.

Each of the three unique marker strings occurred once in Codex native `response_item` records with role `user`, and once in the pane capture, before and after one authorized isolated `DeliverAll.{ Mind witness Secondary }`. Its reply was `Drained.{ { Mind witness Secondary } Delivered }`; that reply alone is not the duplicate oracle. The accompanying observer reported current cursor 9 and no new SendChanged event; all three native and pane counts remained one. No Send was replayed.

No exact native receipt produced Sent, including Hard. The positive exact-receipt/Sent path is therefore a native coverage gap. Native occurrence does not establish model consumption or reading. Wall times are whole caller intervals; phase attribution was not measured.

An initial malformed raw recipient was rejected locally as expected Variant/found Struct, with observer cursor 0 and no admission. Its corrected Address form is the Soft request above. This was not a retry of an uncertain submission.

## Claude gap

Initial launch `6c6f30` and the one authorized replacement `9d4773` both ended their turns and were reaped normally under OnDemand before probes. The replacement transcript states TaskOutput was unavailable; it used Monitor, which returned immediately, then ended its turn. No further replacement was launched and **zero Claude probes were admitted**. This is a fixture coverage gap, not a product pass or failure.

## Cleanup

Codex stop returned `Stopped.4f913d`; both Claude IDs were already Asleep with no binding. No witness agent remained in Herdr. Per-probe observers were terminated; the observer orphaned by the missing-Claude-pane precondition failure was specifically terminated as PID 4147501. Opus stopped the witness unit. At 20:13:49 CST, verified inactive/dead/PID 0, removed only the owned witness store and two client scripts, and verified release gcroot `runtime-051` still resolved to the exact artifact. See `cleanup.json`. Cleanup completed within the 15-minute authority.

Raw launch replies, Working snapshots, per-request event streams/replies/timings, native counts, pane captures and meta observations are alongside this report. Native source file: `/home/li/.codex-next-8mkkxq293hk2/sessions/2026/11/04/rollout-2026-11-04T20-09-01-01a1a977-78a4-77c0-a914-17f4f913d831.jsonl`.
