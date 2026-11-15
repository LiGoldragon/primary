# Queued refresh and repeated notifications

Bounded read-only diagnosis for Corehlwp, including research9h5v. No Refresh retry, forced replacement, restart, cancellation, store mutation, provider/native endpoint probe or new flow launch occurred.

## Observations

Supported Inspect reads show Mind research Sol Awake082e0f, Mind herdrNexus Sol Awakeab4e4b and Mind core Sol Awake1541ef, retaining their native session/pane bindings. All three had empty visible queues, sender locks, visible attempts and restart records. Inspect does not expose the internal OrderedReplacement or Codex turn ledger.

One finite Ouranos user-unit journal read from15:21 startup through its read checkpoint (last entries17:15) records actual refresh admission by new PID245289: core1541ef15:25:02, research082e0f15:26:01 and herdrab4e4b16:27:49 local time. Each has `works; its refresh waits for its rest`. Later repeated Refresh calls for research and herdr are present. No Stop/settlement, ordered-replacement execution or successor-launch line for these three appears in that bounded window; other flows do have settlement/refusal lines. No common cause is inferred from unrelated flows' launch timeouts.

Metadata-only native transcript reads for the exact research/herdr sessions show task_complete cycles after their refresh admissions, interleaved with later task_started records. Only lifecycle type, timestamp and turn id were retained; no message content was output. Core's session was not found in the one exact dated transcript directory checked; no broad transcript search was performed. Native completion is distinct from Flow's rest ledger. Supported ReadEvents returned empty vectors for all three; that is ordinary hook-event history, not a query of the in-memory Codex ledger.

Evidence: `/tmp/flow-5441e0-refresh-diagnosis/` contains the three Inspect/ReadEvents replies, finite journal and case-filtered lines, and `native-lifecycle-only.json`.

## Exact52e source interpretation

- `waking.rs:2204–2233`: queue_refresh durably records one OrderedReplacement; a duplicate matching the predecessor returns RefreshQueued for the same flow without another replacement. Queued means admitted for a future rest, not a successor-start receipt.
- `waking.rs:3972–4145`: settlement first processes reminders, then under the dispatch gate checks ownership/holds, configured thresholds and the queued order. A Codex predecessor is closable only if `codex_in_turn` is false and `codex_resting` true, even when refresh was explicitly ordered. A successful queued order is then passed to replace_as_ordered. Thus an explicit order does not bypass native-rest requirements.
- `codex_turns.rs:805–861,905–927`: native notification events update an in-memory turn/item/letter ledger; settlement occurs only when that ledger reaches AtRest for the owned seat. A completed native task alone does not prove no running process, orphaned item or pending letter remains, or that the subscription delivered its cut/events.
- `send_tool.rs:748–856,1305–1366`: per-live-thread responders subscribe and establish a thread cut plus background terminals, then process later ledger events. No case-specific subscription failure is recorded in the retained journal. Absence of an error is not proof of an established current ledger.
- `handover_reminding.rs:97–302`: reminders are ordinary MiddleAbrupt notices admitted while their configured warning window remains open and no accepted handover_green closes the reminder. The Past-and-resting guard suppresses a warning immediately before a threshold refresh. This reminder path does not remove the OrderedReplacement. Merely saving a filesystem handover is not itself evidence that this path accepted handover_green.

## Finding and limit

The three original queue admissions are real; repeated notifications do not establish their cancellation. The observed stall boundary is before any recorded rest-time replacement attempt for those three sessions. Native task completions exist, but the supported metadata queries do not reveal their current internal Codex ledger standing, open item/letter identities, subscription cut or pending OrderedReplacement. Therefore the exact cause remains UNKNOWN; a missing/stale rest observation or genuinely retained work are hypotheses, not conclusions.

The next useful diagnostic is a bounded Flow-owned read projection of the pending order and its Codex rest/subscription/turn/item/letter standing (metadata only), correlated with these exact sessions. Inspect/ReadEvents do not currently provide that projection. No forced refresh, restart, raw live-store inspection or speculative code repair is justified by this packet.
