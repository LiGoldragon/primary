# Configuration writers, codec adapters, and Resume destination ledger

## Configuration writers

| Actual symbol/location | Context | Planned single guard route / oracle |
|---|---|---|
| `ConfigurationOnlyStore::configure_change` trait+impl `store.rs:4264,4390-4394` | production | validated configuration plan; reopen/readback |
| `RunningStore::configure_change` trait+impl `store.rs:5297,5347-5359` | production | same guard; live replacement |
| `FlowStore::configure_runtime` trait+impl `store.rs:4556,5707` | production runtime setter | same guard where policy-bearing; runtime snapshot |
| `FlowStore::configure_meta_change` `store.rs:8677-8770` | production central dispatcher | sole meta family route; prevalidation/atomic replacement |
| `CountersConfiguration::configure_counters` `store/counters.rs:41,56` | production family writer | typed validation then one commit; counter receipt |
| `DeliveryConfiguration::configure_delivery` `store/delivery.rs:265,387` | production family writer | typed validation then one commit; delivery reopen |
| `lib::Flow::configure_change` call `lib.rs:363` | production network dispatch | enters store guard |
| executable default `lib.rs:704` | production startup seed | explicit startup plan; no implicit policy fallback |
| library setup calls `lib.rs:1846,4137,4365,4394` | tests/fixtures (under test modules where applicable) | fixture-only callers updated with explicit values |
| meta dispatch `main.rs:266` | production `MetaQuery::Configure` | enters store guard |
| internal setup `store/metaflow.rs:744` | inline `#[cfg(test)] mod tests` fixture (`metaflow.rs:732`) | test fixture only, not production bypass |

Query: `rg -n 'fn configure_change|fn configure_meta_change|fn configure_runtime|fn configure_counters|fn configure_delivery|configure_change\('` over the listed Flow Nexus files; every result above classified by enclosing module.

## Codec/adapters exact producer-consumers

- Datom `Budget` definition and methods: pinned `datom-codec/src/core.rs:24-64`; all workspace Budget literals: Flow `flow/src/main.rs:41-46`, `compose_invocation.rs:15-22`, `hook.rs:88-95,226-233`; Meta `flow-meta/src/main.rs:27-34,50-57`, compose `:15-22`; Nexus `flow-nexus/src/main.rs:55-62,361-368,508-515,625-632`, `delivery/body.rs:367-374`, `store/queue_delivery.rs:2786-2793`; tests include `flow-ethos/tests/waking.rs:12-15`, Nexus tests `waking.rs:520-523`, `counters.rs:27-30`, `configuring.rs:807-810,868-871`.
- Datom `Potential::actualize`: pinned `datom-codec/src/core.rs:424,449-460`; `DatomForming::datom_form`: `composition.rs:5-6,160`; generated kinds declaration `datom-codec-kinds.ethos:12,27`. Approved change targets DatomForming/kinds; Composing derive remains `&mut Budget` unchanged.
- Protos `ReaderBudget`/`protosize_with`: pinned `protos/src/core.rs:85-103,558-576`; convenience `protosize` implementations `:553-576` are direct text call paths requiring explicit budget migration. Full dependency tests queried under `protos/tests` and datom tests under `datom-codec/tests`; generated kinds calls are covered by the above.
- Invocation producers/consumers: Flow Ethos `flow/ethos/invocation.ethos:6-9`, generated `flow/src/generated/invocation.rs:5-14`, parser `flow/src/main.rs:30-58`, composer `flow/src/compose_invocation.rs:8-31`, hook `flow/src/hook.rs:47-98`; Meta equivalents `flow-meta/ethos/invocation.ethos:5-7`, main `:39-66`, compose `:8-31`; Hook constructor `flow-nexus/src/herdr/launch.rs:484-496`; Nix constructor `nix/mk-flow-package.nix:89-117,149-200`.

## Resume destination

Exact 916 has native resume only: `launching.rs:1157-1181` (`ResumesReplacement`), `codex_turns.rs:58-59,194-206` (`TurnEvent::Resumed`), `send_tool.rs:617-624`, `codex.rs:1013-1025,1234-1246`, `herdr/launch.rs:1945`. No public Resume symbols exist; this absence is expected authored work.

Planned ordinary destinations from `052-resume-lifecycle.md`: `Resume.FlowId`, `Resumed.FlowId`, `ResumeRejected.ResumeRejection`, `ResumeUncertain.FlowId`; Observe selection `ResumeSelection::{Flow,Attempt}` nested under existing `ObserveSelection.Resume`; replies `ResumeObserved.ResumeInspection` and `ResumeObserveRejected.ResumeObservationRejection`. Planned route: ordinary generated Query/Response → Nexus dispatch → store-private admission owner; no shared Refusal change.

Existing hold/admission mutation owners: `store/address_hold.rs:417-458` (`given_back`, begin/commit hold), `store/metaflow.rs:203-261` lock/hold refusal and commit, `store.rs:3591-3828` AddressHold upgrade, `store.rs:7173,7355` hold reads. Planned generation guard wraps ResumeHead/Attempt + AddressHold mutation in one existing AtomicCommit; stale receipts cannot call `given_back`. Planned tests: concurrent Resume/Launch/Stop, stale generation, crash after reserve/intent/call/observation, Observe read-only one-view response.

## Exact remaining symbols

Generated Resume Ethos/Rust symbols are absent by design and await allocated dependency revisions. External dependency test callsites requiring codec regeneration remain a finite follow-up: all `ReaderBudget`/`Budget` literals in pinned `protos/tests` and `datom-codec/tests`. No source edits or design decisions made.

## Legacy configuration methods and callsites (corrected)

- `ConfigurationOnlyStore::configure(&self, configuration: Configuration) -> Result<Configuration, StoreError>` is the trait implementation body `store.rs:4432-4474`; it atomically asserts/mutates socket/runtime/delivery records. Its callers `store.rs:11083,11118,11686` are all under the `#[cfg(test)] mod tests` beginning `store.rs:8871`; they are fixture consumers, not production writers. (enclosing contexts must be retained when updating). Route production calls through the single validated guard; fixture callers receive explicit test configuration.
- `ConfiguresFlowStore::configure` trait `store.rs:4552-4556`, implementation `store.rs:5669-5687`; callers from query `.configure(` are `store.rs:11083,11118,11686`, all fixture consumers under the test module. Route any future production call to guard; planned oracle is three-family atomic replacement.
- `ConfiguresFlowStore::configure_runtime` trait `store.rs:4552-4556`, implementation `store.rs:5707-5715` uses direct `engine.mutate_keyed`; caller `lib.rs:2208` is inside test fixture setup (`expect fixture` / `set_native_owner_environment_for_tests`), not production. The method remains a production capability writer requiring guard routing when externally invoked; this observed caller is fixture-only.
- `ConfigurationOnlyStore::configure_change` `store.rs:4264,4390-4395` and `FlowStore::configure_change` `store.rs:5297,5347-5359` route to `FlowStore::configure_meta_change` (`store.rs:8677`); meta network caller is `flow-nexus/src/main.rs:266`, Flow caller `lib.rs:363`.
- `configure_counters` definition/implementation `store/counters.rs:41,56`; `configure_delivery` definition/implementation `store/delivery.rs:265,387`; both are existing family writers and must pass the same validated prepared guard where policy-bearing. Query scopes used: `rg -n 'fn configure\(|\.configure\(|configure_runtime|fn configure_counters|fn configure_delivery' crates/flow-nexus/src crates/flow/src crates/flow-meta/src --include='*.rs'`.
- `store/metaflow.rs:740-744` is inside `#[cfg(test)] mod tests` beginning `:~?` (Fixture impl begins `:732`), hence a fixture consumer, not a production bypass.

## Full codec direct-call artifact

`/home/li/primary/flows/e60c75/reports/codec-full-query-results.txt` contains 92 exact matches from Datom/Protos pinned sources plus Flow/Meta/Nexus workspace. Query scopes included `datom_form`, `.protosize()`, `protosize()`, and `Budget` APIs across pinned `datom-codec`, `protos`, and all three Flow packages. Production direct text/protosize calls include `flow-nexus/src/{store/queue_delivery.rs:2785,store/send_v32.rs:39,metaflow.rs:174,delivery/body.rs:158-159,sending.rs:215,send_tool.rs:367,herdr/launch.rs:490,composition.rs:158,604,bin/flow-store-check.rs:42,title.rs:42,66,main.rs:357-369,426,521,641}`, Flow `compose_invocation.rs:34,hook.rs:175,187,main.rs:94`, and Meta `compose_invocation.rs:34,main.rs:91,153`. Test-only direct calls are explicitly present in Datom `tests/core.rs` and `tests/composition.rs`, Protos `tests/{delineation,vertical,protos,textualization}.rs`, and Nexus `src/tests/{counters,configuring}.rs`; all lines are in the artifact. `DatomForming::datom_form` direct calls are recorded there; no production Flow call constructs the trait directly.

## Codec receiver classification

The 92-hit artifact is classified by receiver before migration:

- **Datom output serialization retained:** calls with `value.datomize(...).protosize()` / `datom.protosize()` followed by `.textualize()`/`.compact()` in `flow-nexus/src/{store/queue_delivery.rs:2785,store/send_v32.rs:39,metaflow.rs:174,delivery/body.rs:158-159,sending.rs:215,send_tool.rs:367,composition.rs:158,604,bin/flow-store-check.rs:42,title.rs:42,66,main.rs:357-369,426,521,641}`, `flow/src/{compose_invocation.rs:34,hook.rs:175,main.rs:94}`, and `flow-meta/src/{compose_invocation.rs:34,main.rs:91,153,303,312}`. These are output formatting and remain unchanged.
- **Text-reading convenience:** Protos test receivers such as string literals `.protosize()` in `protos/tests/{delineation.rs:9,13,329,vertical.rs:16,20,85,95,textualization.rs:63,226,238,260,268,275,282,304,protos.rs:17,45,67,82,95,101,115,122,329,343}` and Datom tests where textual input is parsed (`datom-codec/tests/core.rs:225-226`, etc.) require explicit `ReaderBudget` only when they read text. Output-side chained calls in those tests retain output behavior.
- **HookConfiguration output:** `flow-nexus/src/herdr/launch.rs:490` is `HookConfiguration.datomize(...).protosize().compact()` output serialization and is retained; it is not a text-reading convenience call.
- **Direct forming:** `datom-codec/tests/core.rs:226,989` and generated kinds declarations are direct `datom_form` consumers; the approved `DatomForming` signature change targets these plus generated declarations. No production Flow direct forming call was found.

## Adapter-shape gap

The seven proposals specify policy concepts and destinations but do not provide complete exact Ethos layouts/constructor field positions for new Invocation/HookConfiguration adapter fields. Existing layouts are only `flow/ethos/invocation.ethos:6-9`, `flow-meta/ethos/invocation.ethos:5-7`, generated Flow `invocation.rs:5-14`, and HookConfiguration’s current ordinary socket field. Exact new field names/order and every constructor projection remain an explicit missing prebody definition, not an allocation-dependent source absence.
