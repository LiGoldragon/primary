# ReaderBudget changed-type consumer ledger

Independent nonauthor reader `/root/independent_supplement_gate`, native `01a1ade3-1edc-7ab3-ae77-8198d3318772`, supplied the classifications below. Parent landed this record and independently reran the exact finite query to preserve unabridged stdout. This records consumers, not a new type-design decision or a whole-world audit.

Raw query receipt: `reader-budget-changedtype-raw-query.txt`, SHA256 `81709e40875de5c790d659cf2650c6348b3cb9c92d70948f9fa9e6bfcad9958e`. It includes exact commands, timestamp, HEAD/tree/status and unfiltered matches in only the three prepared Protos/Datom/Flow roots. Unrelated IO `self.reader` and Datom composition `Budget::spend(path)` matches are retained in raw output and separated below.

## Production type and capability consumers

- Protos `src/core.rs:85-87` public ReaderBudget declaration; `Spendable::spend:92-100` reads `self.remaining == 0` and mutates `self.remaining -= 1`; `Reader::node:288` calls it. Controlled consumption preserves private-field invariants. Reader's fixed `MAXIMUM_READER_DEPTH:254,291-293` must use supplied depth. `BoundedProtosizable:102-103`, `Reader` storage `248-253`, bounded String/str impls `558-565,576-583` retain controlled mutable budget capability, not mutable field references. Hidden convenience constructors `550-555,568-573` are removed as already authored.
- Protos declarations/reexports: `protos.ethos:17`; `protos-kinds.ethos:6,8-9,18`; `generated/protos-kinds.rs:3,8,30`; `src/lib.rs:8`.
- Datom `src/composition.rs:564-581`: Datomizable reads/casts scalar at566; Composing scalar decode/direct construction571-581. Both migrate to exact ordered two-field projection and checked construction/access. `src/core.rs:27` embeds ReaderBudget;464 passes mutable budget to `protosize_with`; `datom-codec.ethos:9,20` imports/embeds it. Other `.spend(path)` hits belong to Datom composition budget, not ReaderBudget.
- Flow production constructors: `flow/src/hook.rs:90`; `flow/src/main.rs:43`; both `flow/src/compose_invocation.rs:17` and `flow-meta/src/compose_invocation.rs:17`; `flow-meta/src/main.rs:52`; `flow-nexus/src/main.rs:57`; `flow-nexus/src/bin/flow-store-check.rs:22`. Current production `flow-nexus/src/main.rs:363` is removed by the approved direct typed StartRefusal construction.

## Fixtures and separate Spendable callers

- Protos `tests/kinds.rs:11-13` adapter impl delegates to `protos::Spendable::spend`; generic caller18-20 loops `budget.spend()`. Constructors/assertions28,30. This is the only separate Spendable adapter/caller beyond production Reader core288 within the finite query scope.
- Other Protos constructors: `tests/delineation.rs:315-317`; `tests/protos.rs:132,142,149`; `tests/scale.rs:41-44`.
- Datom constructors/readback: `tests/composition.rs:13`; `tests/hygiene.rs:45`; `tests/core.rs:65,85,94,96,110,128,140,152,183,198,235,256,265,275,284,293,302,333,352,388,409,424,461,471,493,505,519,529,543,560,571,585,599,620,635,646,666,681,704,724,757,798-800,885,903,918,951,962`.
- Flow fixtures: `flow/src/hook.rs:228`; `flow-meta/src/main.rs:29`; **`flow-ethos/tests/waking.rs:15` is a prior appendix omission, now explicitly added**; `flow-nexus/src/main.rs:510,627`; `flow-nexus/src/delivery/body.rs:370`; `flow-nexus/src/store/queue_delivery.rs:2788`; `flow-nexus/src/tests/counters.rs:29`; `flow-nexus/src/tests/configuring.rs:809,870`; `flow-nexus/src/tests/waking.rs:522`.

## Ruled obligations, pending exact API supplement

Every listed constructor, including fixtures, moves to checked construction. Every decoder/conversion checks actual usize width and Integer representability with typed failure. Counters are private; read-only access and bounded consumption expose no mutable field reference. Mutations preserve the representation invariant. Exact ordered Datom projection is `{ remaining maximum_depth }`, infallible without narrowing, panic, default, or fallback. Exact storage/accessor trait realization remains Core/Primary's authored decision; this ledger supplies no alternative type choice.

Zero remaining is a valid exhausted runtime state, including Datom `tests/core.rs:543`. Initial configured limits separately obey positive validation. Consumption may reach zero; checked fixture construction must preserve this distinction. MAX/oversized boundary evidence remains required by the final authored design.

All changes remain future implementation obligations; no production/source edit or body authority follows.
