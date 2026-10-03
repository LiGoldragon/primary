# Passover to 9fb0ad

Method: observed 2026-10-03 by a subflow of Psyche.{ Fable f1c841 }, from the printed receipts of `hm-send`, `import-retirement`, and `hm-heartbeat-state`/`hm-list`.

- Send `FLOW_ID=f1c841 hm-send 9fb0ad --stdin` (one data body: passover, handover.md, deployment report, flow 0.24.0 and dea0ba routing, blocked-commands book owed, living's words from log.md 06:1x). Receipt: `Transported.{ 9fb0ad working }`.
- 91ea9f: `hm-retire` refused (`No current registration; use import-retirement only with retained exact evidence`; route already deregistered). `messenger-clj import-retirement` with evidence `witnesses/retire-91ea9f.md`, sha256 4b6107498f623eddf3b134e547f6bd5c1c063d5cd2755f22f962772e3fb5e7f1. Receipt: `Retired 91ea9f: delivery is blocked before Herdr routing`.
- 3ec648: ledger marker state retired, by f1c841 at 2026-10-03T06:02:20Z, evidence sha256 2bade4d9...f65b. Stands. Not in `hm-list` rows.
- Note: the ledger also shows f1c841 retired by 9fb0ad at 12:48:00Z (evidence flows/9fb0ad/witnesses/retire-f1c841.md); not done by this subflow, and it came before the send above.
