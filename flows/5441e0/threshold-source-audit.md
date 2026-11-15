# Threshold persistence: source audit for Psyche nek0

## Observation

Fresh actual Ouranos Configuration before correction had both Fable models at280000. Two keyed Configure.Refresh calls changed each to330000 and exact echoes plus final supported readback confirmed the correction; all other config fields were identical except advancing allocation counters. Evidence is `/tmp/flow-5441e0-fable-restoration/`, and the correction is recorded in `decoder-candidate.md`.

Field reports last pre-stop Configuration had both330000, actual stopped Memory was carried as is, automatic replay unit is absent, and the new Flow PID is245289. This report does not yet have the exact pre-stop330000 file/time or a typed read of the stopped copy. Request8boz to Field asks for those retained receipts and activation/start evidence. A prior live read and an actual stopped database are distinct observations.

## Exact source findings

Inspected immutable Flow `52e5687d13446e3cd22583ff31d717f6250e0534`:
- `crates/flow-nexus/src/lib.rs:1575–1591` opens the place Memory via `FlowStore::open_configured`, then obtains its committed configuration snapshot. No installed models or thresholds file is read on this path.
- `store.rs:2504–2510` performs recognized configured opening, staging only where running tables must be added; `store/staged_open.rs` copies this store and lands the successfully opened copy, not an earlier backup.
- `store.rs:2599,2649` registers the threshold family using its existing descriptor; `760–777` keys thresholds by model name. No threshold-specific upgrade or default seeding is present in the inspected opening path.
- `store.rs:3350–3363` obtains the effective threshold from the keyed Memory table. `6155–6160` builds the Configuration threshold vector directly from that table and sorts it.
- `store.rs:6811–6821` accepts whole-family Thresholds declarations; `6839–6846` accepts a keyed Refresh declaration. These are explicit meta configuration effects.
- The complete37980e10→52e production `store.rs` diff is empty: its sole change is one test identity string. Related store and lib.rs diffs likewise change only test identity strings. No new threshold migration or threshold reset appears in this release delta. Retained exact diff: `/tmp/flow-5441e0-fable-restoration/store-379-to-52e.diff`.

Inspected immutable Home `308f2354d21eb79e111d4e0cfd83c58ebe327a21`:
- `modules/home/profiles/min/flow-nexus-place.nix` declares the daemon with ExecStart alone, no automatic configure service or ExecStartPre setter. The activation hook compiles the place file. Bootstrap families are read only by explicitly invoked `flow-replay-<version>`.
- `modules/home/profiles/min/flow-nexus-config/thresholds.datom` has Fable5-1=280000 and Fable5-2=330000. Replaying that exact file alone would therefore not explain BOTH models becoming280000. It is not evidence that any replay ran.

## Conclusion and next discriminating evidence

The source supports Memory as the threshold authority and does not establish a compiled-default, installed-file or new upgrade reset as the cause. The concrete reset cause remains UNKNOWN. The corrective meta calls have repaired the observed live values; their persistence across a new start has not been tested and no live restart is authorized here.

Next compare the exact stopped copy through a read-only typed reader with the last pre-stop Configuration, then inspect the existing activation/start/configure receipts for a writer or a different store path. If the stopped copy already has280000, investigate the interval before stop; if it has330000, isolate open on a disposable immutable copy and compare its threshold table before/after. This distinguishes an external write/path mismatch from opening/storage behavior. Choose the causal fix only after that distinction; no speculative code or source declaration edit has been made.

## Discriminating stopped-copy and configured-open proof

Field Result8boz supplied the last observed330000 snapshot `/tmp/s60o-exec.x7D3oV/configuration-before.datom` (read time not established), actual after snapshot read15:24:09.888-06 with both280000, and the actual stopped byte capture at15:15:43.790085501-06. The captured database SHA256 is `5413f8feace2ad7479e56e08c95cda9b993400a1578e63efe80222a1a0ce7442`. No stopped-copy typed decode had previously been performed.

This flow copied ONLY that immutable stopped capture, verified its full SHA256, and ran a narrowed version of the predecessor typed reader on a disposable builder copy. It uses redb ReadOnlyDatabase plus ReadTransaction, validates schema3/layout7 and the threshold family schema, and decodes only the threshold table with exact52e generated types. It uses no Engine/FlowStore open, upgrade or repair. Exit0: BOTH Fable thresholds in actual stopped bytes were330000. Copy hash before/after is identical. Evidence `/tmp/flow-5441e0-threshold-reader/`: reader.rs, default.nix, build/read exits, thresholds.json, capture/hash receipts.

A second scratch binary calls exact published52e `FlowStore::open_configured` on ANOTHER disposable copy, then drops it. It launches no daemon, sockets, harness or native witness. A separate read-only typed read afterwards finds ALL threshold records, including their archived-byte SHA256 values, identical to the stopped-copy read: both Fable330000. Open and read exits0. Evidence `/tmp/flow-5441e0-threshold-open/`: reader.rs (the small opener), default.nix, open/read exits, thresholds-after.json, before/after hashes and unchanged immutable source hash. Both scratch binaries were built on Prometheus against the exact published52e library with dependencies reused; no runtime source was edited.

These actual-copy results supersede the earlier unknown stopped-value boundary and the proposed configured-open experiment. They demonstrate the stopped Memory already held330000 and this exact configured-open path preserves it. They do NOT establish which later live writer or path produced280000. Field has been asked for retained activation/start/configuration writer or wrong-path receipts. A causal source fix remains unchosen; no live restart or mutation beyond the earlier authorized narrow setters was performed.

## Transitional old replay actually re-entered

A subsequent finite joint journal read for Flow and flow-configure,15:14–15:22 local time, identifies a previously missing writer between stop/capture and new245289 startup:
-15:15:43: old Flow4058088 and its configure unit stopped.
-15:19:50: OLD Flow restarted as232493, and OLD flow-configure started as232522.
-15:19:52: configure232522 logged Nexus Configured and Models Configured, then was terminated during the switch.
-15:21:22: old232493 was SIGKILLed after stop timeout.
-15:21:27: new245289 started.

Journal metadata for232522 retains its exact script and argument vector. Reading those immutable artifacts shows the old script iterates family requests in order and logs each only after receiving its reply; its THIRD argument is an old thresholds declaration with BOTH Fable models280000. This differs from the final new Home source's asymmetric280000/330000 declaration. The actual old replay thus existed and began changing configuration during transition, despite the configure unit being absent at the final checkpoint.

Evidence `/tmp/flow-5441e0-fable-restoration/`: `transition-unit-journal.txt`, `old-configure-journal.jsonl`, `old-configure-script.txt`, `old-thresholds.datom`. The script was read, never invoked by this flow.

Observation versus inference: actual old replay startup and its first two successful effects are observed; the exact threshold commit has no surviving echo/transaction receipt. An in-flight third request could commit before its client/script was killed. That is the strong causal explanation matching the resulting280000/280000 and the otherwise preserving new opener, but the third commit is an inference, not a witnessed transaction. What caused activation to re-enter the old units requires the deployment owner's activation-order evidence.

The current generation's removal of automatic replay removes that writer from subsequent ordinary starts, and exact52e configured-open is proven to preserve330000 on the stopped-copy experiment. The remaining transition fix is to keep old configure from re-entering between the stopped event and replacement of its unit/declarations, through reviewed deployment ordering or a supported lifecycle hold. No hand mask, speculative deployment patch, live restart or replay was performed here. Current source5-1 declaration debt remains separate and must be aligned before any future explicit owner replay. Field/Core/Psyche received this new writer evidence and its precise limit.
