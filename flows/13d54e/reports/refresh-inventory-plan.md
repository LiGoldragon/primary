# Event-gated deployed-version open-Refresh inventory

Owner: Mind flowNexus Sol (13d54e), answering Field he19. Prepared only; no live snapshot, store open or inventory run has occurred in this flow. Run once only on Field's explicit per-host event. Every inconsistent attempt returns to Field; no automatic retry or polling loop.

## Retained typed decoder

Prior evidence: `flows/98df55/reports/open-refresh-inventory.md`. Reader source, Nix build expression, build log and baseline output remain under `/tmp/claude-1001/-home-li-primary/98df550b-580c-5645-ac3b-d5ccbe75016d/scratchpad/`. Source `reader/open-refresh-read.rs` SHA256 `a6d02dfda970f54a32db308cd38fcad4529a3c15baf672514dac84b5b2e207ee`; `reader/default.nix` SHA256 `9fe9814219c5f221e78573ab3f9d3fadf9709a1d941a5975719918637a13042a`. The already-built executable exists. Capture its package dynamically from the last line of `reader/build.log`, then use `$reader/bin/open-refresh-read`. No compilation is needed. The build links the deployed eabddc8d Flow0.56.2 library and sema-engine0.19.0; the prior report contains derivation linkage evidence. Revalidate deployed identity before reuse; do not assume a unit description establishes its binary/library.

The reader's Engine open is writable on its PRIVATE COPY (repair/registration may write there). It never receives a live store path or the sole rollback backup. It prints pre-registration catalog identities for all three families, registers Flow's generated types/schema hashes, reads all records, and prints the complete relevant commit-log operations. Its schema is Engine3, ordered-replacement-v1 and successor-intent-v3. A missing catalog family can otherwise be registered empty: the oracle below explicitly rejects that false zero.

## Field event and safe read ownership

Field supplies host/user, actual resolved old unit/binary/library, Place State store path, and a private evidence directory. It grants one bounded read/copy at the named event. Sol verifies the actual deployed binary source/library matches the retained reader's source/layout; any mismatch stops this plan for a matching decoder, rather than forcing this reader onto another format.

Preferred final event: Field has stopped all store writers and produced its verified pre-upgrade backup. Field supplies a disposable duplicate of that backup; Sol duplicates it again for decoder A and untouched control B. This establishes a stopped-writer point immediately before first upgraded open; it is stronger than a live two-copy confidence check. Field retains custody of backup and restoration, and checks no writer restarted between final inventory and upgraded open.

If Field instead authorizes a live pre-stop sample: record UTC window and inode/size/nanosecond-mtime/ctime; copy source to A, stat; copy to B, stat; hash both. Accept the sample only if ALL three stat tuples and both hashes agree. One attempt only. The old snap.sh is reference ONLY: its40-attempt/sleep loop is not executed. A successful live sample is high confidence, not a transactional snapshot or proof about later arrivals; it does not replace the stopped-writer pre-open check.

Run the old deployed `flow-store-check` on private B through its existing `Opens.<path>` contract only after verifying it makes its own private copy, as in the prior report. Run retained `open-refresh-read` on A; preserve stdout/stderr and exit. Hash control B before and after both checks; it must stay equal. Neither reader nor checker opens the live source or sole rollback backup. Remote copied evidence is decoded locally only where Field's host/user grant allows it; otherwise the same retained closure is copied through Nix to the named user, without rebuilding or installing anything persistently.

## Oracle and return

Require: identity matches deployed layout; checker and decoder exit0; catalog lines BEFORE registration show registered=true with expected family name/schema identity for ordered replacements, successor intents and metaflows (compare to retained read.out); untouched B hash equality. Missing or mismatched catalog identities, decode failure or inconsistent copies mean UNKNOWN/STOP, never zero.

Typed queued Refresh is `OrderedReplacement.replacement_order == Refresh`; typed callerless ordered succession is `SuccessorIntent.succession_cause == Ordered`. Emit each such row's Address, predecessor and launch request where carried. Other causes are retained separately; they are not silently relabelled as callerless Refresh. Zero counts for both complete tables plus valid catalog identity is sufficient typed absence. For nonzero tables, inspect each typed Debug row under these exact enum definitions. Independently fold relevant commit-log operations per table/key; each final Retract removes its key, Assert/Mutate leaves it open. Folded open keys must equal decoded table keys. A disagreement stops cutover.

Return one event receipt: host/user, UTC capture window, deployed source/library identity, source/copy hashes and consistency grade, decoder/checker identity/exits, catalog/row counts, named callerless rows, log-fold comparison and evidence path. Nonzero callerless rows return to Field for supported settlement and a NEW explicit sample event. Nothing is cancelled automatically. This is the old-format preflight, not native warning proof or live-switch authorization.

## Exact retained reader invocation (prepared, not executed)

Field supplies `decoder_input` as disposable copy A and `readout` as its new evidence filename; neither may resolve to live source/control/rollback backup. With those paths validated and source hashes above verified:

```sh
prior=/tmp/claude-1001/-home-li-primary/98df550b-580c-5645-ac3b-d5ccbe75016d/scratchpad
reader=$(tail -n 1 "$prior/reader/build.log")
test -x "$reader/bin/open-refresh-read"
"$reader/bin/open-refresh-read" "$decoder_input" > "$readout" 2> "$readout.stderr"
```

The invocation's exit is captured separately, even on failure. Source checks, deployed-library identity, full catalog oracle and independent control hashes precede a zero claim. The checker executable is resolved from the actual old deployed package at the event, not from a stale store-path literal.
