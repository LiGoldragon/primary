# Independent supplemental prebody gate

**Verdict: PASS — the supplemental prebody design/evidence gaps are closed.** This is a bounded prebody gate only. It grants no source body, sole-writer, publication, deploy, capsule, Adopt, or 051 declaration authority; Core Secondary retains that authority.

Review window 2026-11-05T22:45:11Z–22:54:07Z, before the fixed 22:55:11Z deadline. Fresh nonauthor task `/root/independent_supplement_gate`, native `01a1ade3-1edc-7ab3-ae77-8198d3318772`. I made no file/source/lock/configuration/process mutation and launched no child.

## Pinned inputs and drift

Final hashes independently read and re-read:
- frozen56 `MANIFEST.sha256`: `e545c6c2d378be1a1c86eed9ea688096c8fd259e3e7059ce58f7a31e5e01d38c`; all 56 entries verify.
- exact recovery appendix: `e6df177d36bd1b13abae9fffb212700c23d7b03a83f3da465664ac8a3bd9b0e7`.
- StopPoll correction: `ae49678d642160ee312ddf30f55ed41f079f9daf742b4833ad8328dc8d352ce6`.
- final codec consumers: `3b4d85a9f88dd65fd2de9d67edcc06b37e9c607c5d14dabc59c2d812f1f16511`.
- changed-type ledger: `b957e44f2da8f7967ca397b966fdc75d3db324034f9e7bde34eaa664c55f2ca1`.
- unabridged changed-type raw query: `81709e40875de5c790d659cf2650c6348b3cb9c92d70948f9fa9e6bfcad9958e`.

Prepared Flow/Datom/Protos roots remained tracked-clean at final read: Flow `916b545…` tree `f5f01ef…`; Datom `4dff16b…` tree `3880b21…`; Protos `15b41da…` tree `2d1dce…`.

## Exact gates

- **Cargo/prepared identity: PASS.** Cached and prepared Datom and Protos pairs independently had identical HEAD/tree and clean tracked state; `diff -qr` excluding `.git` and cached `.cargo-ok` was empty. Cached roots contained only untracked `.cargo-ok`. All seven files cited by the 92-row receipt are tracked; the receipt has no `.cargo-ok` hit.
- **Held codec classification: PASS, bounded to the pinned receipts.** Rows1–35 Datom and36–60 Protos are fixture/oracle paths. Flow production structural projections are output-only as classified. I checked the receiver scopes in source: flow-meta `parse_datom`19–36 and hook `report`219–236 are `#[cfg(test)]`; delivery/body, queue_delivery and waking budget sites are fixture/readback code. Production decoders are assigned explicit owners. The changed-type rerun additionally found and classifies `flow-ethos/tests/waking.rs:15`, closing the prior omission. This is semantic classification, not a filename-count claim; the appendix correctly avoids asserting whole-world exhaustiveness beyond the recorded expressions and roots.
- **StartRefusal production receiver: PASS.** Actual callers `main.rs:102–106,121–125`, output function356–377, and exact `StartRefusal::Store(StoreRefusal { path: Path, reason: Reason })` types were checked. The final supplement replaces the text round-trip with direct typed construction, preserves output/exit semantics, and leaves only fixture decoding with explicit fixture budgets.
- **Store-check production receiver/producer: PASS.** Actual raw receiver is `bin/flow-store-check.rs:15–29`; typed request is `StoreCheckRequest { StorePath }`; `store_check.rs:136–140` direct test construction is codec-free. Actual capsule producers are Clojure1751 and1983–1984, each passing one existing request datum through the exact selected package. The approved Nix wrapper has one declared five-budget value, exact raw libexec target, exact argc, quoted byte-preserving request insertion into one typed envelope, and no shell evaluation, PATH/environment/default/parser fallback or implicit arguments. The raw executable fully decodes before `request.check()` effects. The distinction between direct raw invocation and packaged wrapper is explicit and tested.
- **ReaderBudget changed type: PASS.** The final API closes the former infallible usize→Integer gap with one private-i64 record, central checked integer/native factories, field+cause typed error, exact read access, retained zero-safe `Spendable`, configured-depth capability and no mutable field escape. Ordered Datom `{ remaining maximum_depth }` emits exact i64 values and composing requires exactly two positions through the checked constructor; scalar legacy input has no default-depth path. Zero runtime exhaustion remains valid while initial configured limits remain positive. The pinned raw query and ledger cover every constructor/public-field access/mutation/Spendable caller in the finite Protos/Datom/Flow scope, including production `core.rs:92–100,288`, fixture adapter/caller `tests/kinds.rs:11–20`, all literals, and the old scalar projection564–581.
- **Named policy rows: PASS.** Source confirms `FramePolicy.Nexus` at `lib.rs:1386–1445`, including unchecked current outbound cast/write and inbound preallocation check, and ordinary/meta use of the shared carrier. `LaunchPolicy.FlowIdentity`, `ClaudeHome`, and `FlowDirectory` exact production branches at `herdr.rs:143–198`, overlays/test factory332–397, helper execution `herdr/launch.rs:689–710`, workspace/marker consumers651–699 and Claude transcript consumer820–840 match the appendix ownership, activation and oracles. Fixture branches are explicitly scoped.
- **StopPoll correction: PASS.** `ReminderPolicy.Scan` is `reminding.rs:15–16`; both stop-responsive sleep and spent increment are `reminding.rs:95–97` and must use one captured StopPoll snapshot. `PollingPolicy.AgentStop` is separately `observe_agent.rs:217`. The supplement's current-wait/next-wait activation and deterministic oracle are exact.
- **Current custody: PASS, prep-only.** A fresh supported `orchestrate 'Observe.Locks'` showed 25617 Flow, 25618 four dependencies, 25619 redb, and 25620 Datom/Protos, all owned by `2aed8d` with preparation-only reasons. No broader scope or body authority appears in those holds.

## Remaining evidence

No prebody semantic row remains open in the reviewed supplemental scope. Compile, generated-source, process, fault, archive/reopen, capsule and runtime proofs are post-body evidence exactly as the packet states; their absence is not a prebody design gap. One Core-authorized sole writer and body grant remain separate future acts.
