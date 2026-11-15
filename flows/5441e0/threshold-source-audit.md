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
