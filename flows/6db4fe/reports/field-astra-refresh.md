# Field Astra successor refresh — 2026-09-21

## Result and scope

Fresh Field Astra main Flow **03e825** accepted the ongoing work of incumbent **6db4fe**. Its Codex native thread is `01a0c4a7-2590-7ae3-8625-bee03e82586d`, model `gpt-6-astra`, effort `medium`. The incumbent remains alive and routed while it finishes this report and its worker relay. No seat was retired.

The new thread was started by the app-server receipt-first path in `tools/native-seat-launch.mjs`, then attached to that same native thread in Herdr `messaging-build/wQ:p9` (terminal `term_65c003095a6af53`, agent `flow-03e825`). Herdr tab, pane, and Codex native title are `03e825`; native title set had exact ID/model/path preflight, readback, and `thread/name/updated` notification. HM registration points 03e825 at this exact live pane/thread. The target used `flow-id codex` directly and returned `03e825`; a direct structured clock witness succeeded. Interactive readiness and HM target-side reads were witnessed.

Receipt `flows/6db4fe/field-astra-native/receipts/field-astra.json` records the native first turn. Local rollout verification found the complete first input, **21 typed skill entries and expanded bodies**, including `main-flow`, `testing-datom-messaging`, `datom`, and `messaging`, plus the two source bodies. The receipt-only first response, then activation turn, happened before Herdr/HM adoption. Installed Codex CLI observed: `0.153.4`; launcher source last commit `4422cd6ec`. This is a currentness witness for this refresh machinery and its native context, not a claim that Nexus, OS, Message, HM packaging, or every deployed service is current.

## Route and handoff witness

An initial bare `Probe` was read by the target but answered in prose. It lacked the machine-origin envelope and exact reply instruction. One corrected `MACHINE.Relay` containing a locally Datom-validated `Probe` and a reference to the declared temporary control type produced exact `Ack.{ «6db4fe-03e825-typed-01a0c4a7» }`; `tools/field-refresh-control.py` validated head, one string position, and marker. Direct HM transport delivered this envelope; this does **not** authenticate origin or prove general Nexus Message delivery.

One meaningful `Offer` then pointed at `flows/6db4fe/reports/refresh-handoff-current.md`. The target visibly read that file and returned exact `Accept.{ «6db4fe-03e825-offer» }`. Its accepted work includes the unfinished canonical title script (apply disabled pending rollback/failure tests and Claude adapter), current-main native `testing-datom-messaging` skill propagation with receipts, inherited worker results and runtime parity work, and conditional cleanup of old 6db4fe only after the incumbent's final/no-new-work preflight and continuity check. The target was told to preserve existing Sol and crossover routes.

The accepted handoff is responsibility for open work, **not proof that the work is finished**. The old 6db4fe route and this subflow must stay live until the parent has received final results and the explicit retirement gates pass. Current-main skill propagation, title apply, source/deployment parity, and existing workers' outcomes remain successor-owned open items.

## Tests, sources, and limits

- `node tools/native-seat-launch.test.mjs` and `node tools/native-batch-refresh.test.mjs` passed after the launch-source change.
- `python3 tools/test_field_refresh_control.py` passed four parser/shape tests. The test covers envelope generation and exact `Probe`/`Ack`/`Offer`/`Accept` shapes; it does not authenticate a sender or execute a full Ethos codegen check.
- Live source: native receipt and point-in-time rollout file referenced there, Codex app-server read/name/set, Herdr exact pane read, HM registry and target response. The first-prompt sources were `refresh-handoff-current.md` and `flows/33ba2b/vision/operational-fieldRefreshSuccession.md`; neither contained a long hex digest. Hashes are held in machine receipts for verification, not embedded in the human prompt.
- Message traffic from this refresh was bounded: one bare Astra Probe, one corrected Astra Probe, and one meaningful Astra Offer. No further echo/status probes are planned.

