# Mind curriculum Astra lifecycle — bounded read-only lookup (e02i)

Finding: the five recent flows named by the initial ledger window followed OnDemand sleep/wake, not the context-refresh path. No implementation, native transcript scan or runtime mutation was performed. These reads themselves were meta observations, not wake requests.

## Observed ledger and daemon events

Initial `Inspect.{ Mind curriculum Astra }` found Awake43fa09, native session01a1dcb9-808d-7f72-949f-ce243fa091f8, with predecessor72cf7f. Its past tail was773706→5ff890→c9169a→93a749→72cf7f; the following table covers the last five at that observation, not a claim these were the only flows today. Daemon journal dates below are2026-11-14, timezone−06:00, unit flow-nexus-0550.service, process654687.

| Flow | Predecessor in ledger | Woke (first-prompt requests) | Slept at rest |
|---|---|---|---|
|5ff890|773706|18:23:38 (2)|18:25:39|
|c9169a|5ff890|18:26:16 (2)|18:26:46|
|93a749|c9169a|18:51:12 (8)|18:52:08|
|72cf7f|93a749|18:58:48 (2)|19:00:02|
|43fa09|72cf7f|19:01:51 (1)|19:04:17|

The journal also shows773706 woke18:16:15 (3) and slept18:18:54. Thus “five today” is not the complete day's count.

During this lookup the ledger advanced: a later Inspect found Awakee382da, native session01a1dcbc-0ddc-7b83-aec7-1e5e382da3a0, predecessor43fa09. Journal confirms e382da woke19:04:39 (1) and slept19:05:12. Latest event observation was19:05:20; e382da is therefore the latest known run and its recorded state transition is sleep. Do not keep43fa09 as a standing current-id claim.

The ordinary per-flow event reader is empty for each of the initial five: `EventsRead.{ <id> [] }`. It does not furnish a lifecycle reason here; cause attribution below comes from the explicit daemon lifecycle events tied to exact deployed source, not invented event records. Current Configuration declares this address Regular/Default/OnDemand.

## Source interpretation and disconfirmation

Exact deployed source eabddc8d `crates/flow-nexus/src/waking.rs`: settle_stopped1491–1540 prints “slept at its rest” ONLY for AtStop::Slept; context/ordered refresh paths print “refreshed…” instead. settle_rested3978–4130 tests context threshold/warning/handover and ordered replacements BEFORE the ordinary sleep branch. With an empty queue and closable OnDemand seat, it closes that harness and returns Slept. wake_plan1647–1687 chooses Fresh for a declared metaflow (or its last launch profile), rather than resuming the previous native thread.

Consequently the observed repeated short sessions are explained by this deployed OnDemand implementation: work ends, queue empties, harness sleeps/closes; a subsequent waking request starts a fresh flow. These five transitions are not evidence of threshold refresh, early-warning refresh or compaction. The journal has no refresh line for any of these ids in the bounded window. Whether an independent warning was ever delivered/read, or which exact input caused each wake, is not established by these lifecycle lines and remains unknown. No inference is drawn from empty handovers or warning timing.

Raw retained evidence and exact deployed source extract are under the temporary directory named by `/tmp/flow-13d54e-curriculum-ledger-pointer`: per-id event replies, debug/configuration snapshots, daemon-journal.log, deployed-waking.rs. No live database copy/open or native transcript read was needed.
