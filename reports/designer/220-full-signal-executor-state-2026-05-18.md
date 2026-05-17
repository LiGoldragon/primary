# 220 — Full Signal executor state (2026-05-18)

*Topic compendium for the "full Signal executor" question. Part of the
2026-05-18 workspace state-of-art series. Master index lives in
`reports/designer/215-workspace-state-of-art-2026-05-18.md`.*

---

## 1 · State of art

DA/119 names three meanings of "full Signal executor":

1. **Engine as protocol host** — sema-engine becomes contract-aware, dispatches request variants, owns reply shaping. **Rejected** (breaks kernel/domain split).
2. **Engine as transaction grouper** — sema-engine stays contract-blind but grows multi-table transaction primitive when pressure proves it. **Deferred** (no consumer pressure; schema redesign usually cleaner).
3. **Component-local execution plane** — daemon-local actor topology (`socket → exchange → dispatch → reducer → store + effects → reply/events/audit`) every triad daemon takes. **Canonical**.

Sema-engine stays the contract-blind, verb-shaped database executor per
its own ARCH §"Non-Goals" ("No actors. No text parser. No daemon
process."). The six verbs already round-trip cleanly at the seam
(witnesses in `sema-engine/tests/signal_core_seam.rs`).

**No new helper APIs needed today.** The three helpers debated in
sec-OA/2's first pass — `validate_write`, `commit_multi`, `unsubscribe`
— all dissolve, defer, or have component-side route-arounds.

Implementation order: **`persona-terminal` first** (owner socket
already exists; lifecycle moved into `owner-signal-persona-terminal`),
then **`lojix-daemon`** (proves the executor is not Persona-specific),
**then extract a `signal-executor` library** crate. The
`signal-executor` repo does not exist yet — confirmed.

---

## 2 · Load-bearing reports

| Path | Carries |
|---|---|
| `reports/designer-assistant/119-full-signal-executor-architecture-concept-2026-05-18.md` | Canonical concept. Three meanings, plane shape, worked examples (terminal `CreateSession`, lojix deployment), Q1-Q5. |
| `reports/second-operator-assistant/3-full-signal-executor-architecture-consideration-2026-05-18.md` | Operator complement. Endorses meaning 3; actor-density argument (§2.1); implementation-order specifics (§4); residuals (§5) including the supervised-state-bearing-actor restart trap. |
| `reports/second-operator-assistant/2-signal-core-sema-engine-fit-audit-2026-05-17.md` | Audit + falsification witnesses. Verdict: "good fit; no engine API additions required." Verb→engine API table (§1); twelve in-code witnesses. |

---

## 3 · Stale / superseded reports

| Path | Status | Why |
|---|---|---|
| `reports/designer-assistant/118-signal-core-sema-engine-fit-investigation-brief-2026-05-17.md` | **Retire candidate** | The brief explicitly said "this report is not that audit; it is the brief for the agent who should perform it." sec-OA/2 landed the audit; DA/119 + sec-OA/3 refined the answer. Substance (Q1-Q7, seven witness candidates) fully absorbed into DA/119 §2 + sec-OA/2 §1-§2 + §5. |
| First pass of sec-OA/3 | retracted in place | Reframed per `skills/reporting.md`; first pass missed DA/119's third meaning. jj history captures prior pass. |
| First pass of sec-OA/2 | retracted in place | Per falsification results; current /2 §3 explicitly notes the framing collapse. |

---

## 4 · Sema-engine API surface state

| Helper | Verdict | Reason |
|---|---|---|
| `validate_write` | **Dissolves into `match_records` composition** | Witness `seam_gap_falsification.rs::validate_write_dissolves_into_match_records_dry_run`. 3 lines single-op, ~12 lines multi-op with within-batch staging via `HashSet`. Engine's typed errors map onto local enum variants one-for-one. |
| `commit_multi` | **Defer** | Witness `cross_table_writes_via_two_engine_commits_are_not_engine_atomic` confirms gap is real. Escape hatch (`storage_kernel().write(\|txn\|...)`) bypasses commit-log/snapshot/delta. Resolution order: schema first (one-table `Mutate` replaces two-table `Retract+Assert`) → then extend `Engine::commit` for multi-table → document. First candidate: `RoleHandoff`. |
| `unsubscribe` | **Component supervisor + sink filter sufficient** | Witness `subscription_lifetime_can_be_managed_externally_via_handle_id_filter`. Registry growth bounded by daemon lifetime. Bigger residual: detached-thread-per-delta cost (`SubscriptionDeliveryMode::Inline` is the actor-shaped workaround). |
| Dispatcher-trait macro | **Defer until measured repetition** | Match-on-variant dispatch is the *observable dispatch plane*, not boilerplate. Each arm names a flow and records trace nodes. Macro-generated saves keystrokes, loses explicit topology. Question lives in `signal-core-macros` if it lands, not in sema-engine. |

---

## 5 · The three meanings (canonical)

| # | Meaning | Verdict |
|---|---|---|
| 1 | Engine as protocol host (sema-engine accepts Signal requests, contract-aware) | **Rejected.** Violates kernel/domain split. Sema-engine ARCH §"Non-Goals" forbids actors, parsers, daemons, contract-crate dependencies inside the engine. |
| 2 | Engine as transaction grouper (stays contract-blind, grows multi-table tx primitive) | **Deferred.** No consumer pressure; schema redesign usually cleaner. Pure-state multi-table operations are the remaining candidates. `RoleHandoff` likely first. |
| 3 | Component-local execution plane (every triad daemon owns sockets + dispatch + reducer + store + effects + reply/events/audit) | **Canonical.** DA/119 §3-§4 sketches the planes: `OrdinarySignalSocketActor`, `OwnerSignalSocketActor`, `SignalExchangeRuntime`, `GeneratedContractDispatcher`, `ComponentSignalExecutor`, `ComponentReducer`, `SemaEngineOwnerActor`, `EffectSupervisor`, `ReplyEventProjector`. |

---

## 6 · Architectural-truth witnesses

### Wire→engine seam (`sema-engine/tests/signal_core_seam.rs`, 6 witnesses)

1. `signal_core_assert_operation_lands_as_engine_assert_with_matching_verb`
2. `signal_core_mutate_operation_lands_as_engine_mutate_with_matching_verb`
3. `signal_core_retract_operation_lands_as_engine_retract_with_matching_verb`
4. `signal_core_multi_op_request_lands_as_one_commit_log_entry_with_ordered_per_op_verbs`
5. `signal_core_match_operation_lands_as_engine_match_with_matching_verb`
6. `signal_core_universal_check_catches_verb_payload_mismatch_before_engine_call`

### Gap falsification (`sema-engine/tests/seam_gap_falsification.rs`, 6 witnesses)

1. `validate_write_dissolves_into_match_records_dry_run`
2. `multi_op_write_dry_run_composes_with_match_records_plus_local_staging`
3. `subscription_lifetime_can_be_managed_externally_via_handle_id_filter`
4. `cross_table_writes_via_two_engine_commits_are_not_engine_atomic`
5. `read_after_write_is_two_engine_calls_with_monotonic_snapshot_ids`
6. `engine_subscription_registrations_are_listable_for_introspection`

**Together they prove**: six verbs are honest at the seam (wire verb =
payload `signal_verb()` = engine call = receipt verb = commit log
verb); structural multi-op atomicity works for single-table writes;
cross-table atomicity is the only real engine-shape gap and has
schema-side resolutions; the three speculative helper APIs all
dissolve or have component-side route-arounds.

---

## 7 · Implementation order

Per DA/119 §10 + sec-OA/3 §4:

1. **`persona-terminal` first.** Owner Unix-socket listener bound to spawn-envelope owner path; `TerminalSignalExecutor` internal module with two ingress adapters (ordinary + owner); one `SemaEngineOwnerActor` shared by both surfaces; `CreateSession` as first effectful operation with durable pending state (DA/119 §4.7: reserve name → spawn → mark ready/failed); `RetireSession` symmetric; six witnesses per DA/119 §10 step 6.
2. **`lojix-daemon` second.** Same plane shape against non-Persona domain (Horizon projection + Nix build/deploy effects). Proves the executor is not Persona-specific.
3. **`signal-executor` library extraction third.** Only after both consumers prove the shape. Library-only (no daemon, no Kameo dep, no contract-crate dep, not contract-aware). Candidate nouns: `ExecutionEnvelope`, `ExecutionSurface`, `ExecutionContext`, `ExecutionOutcome`, `ExecutionFailure`, `EffectStep`, `ComponentStore`.

Each step is one logical commit.

---

## 8 · Open questions

From DA/119 §11:

- **Q1.** `signal-executor` repo timing? **Refined:** not before two consumers.
- **Q2.** Macro-generated handler traits? **Defer** until measured repetition. Belongs in `signal-core-macros`, not sema-engine.
- **Q3.** Effectful pending state mandatory? **Yes** for operations that create/destroy/mutate external resources.
- **Q4.** Ordinary and owner surfaces share one store actor? **Yes.** A component has one durable state owner; multiple sockets are permission surfaces, not multiple databases.
- **Q5.** Sema-engine ready enough? **Yes as contract-blind database executor** for first daemon-local execution planes. **Not ready, and should not be made ready, to act as contract-aware Signal protocol host.**

Operator-side residuals (sec-OA/3 §5):

- Detached-thread-per-delta cost under load (un-benchmarked).
- `SemaEngineOwnerActor` supervised-restart trap. Every triad daemon's Sema owner stays on `.spawn()` (not `.spawn_in_thread()`) until upstream Kameo grows `pre_notify_links`. Discipline already in `skills/kameo.md` §"Blocking-plane templates" Template 2.

---

## 9 · Recommendations for context maintenance

### Retire (clearest first)

- `reports/designer-assistant/118-signal-core-sema-engine-fit-investigation-brief-2026-05-17.md` — the brief asked for an audit; the audit has landed (sec-OA/2 + DA/119 + sec-OA/3). **Retire now.**

### Keep (load-bearing)

- DA/119 — canonical concept.
- sec-OA/3 — operator complement.
- sec-OA/2 — audit + twelve in-code witnesses.

### Future retirement

- sec-OA/2 retires when sema-engine's contract is stable enough that the verdict is restated inline in engine ARCH or a future `skills/sema-engine.md`. Today, sec-OA/2 carries reasoning not yet elsewhere.
- DA/119 + sec-OA/3 retire when their substance is absorbed into `skills/component-triad.md` (the universal plane shape) or a future `signal-executor` library README/ARCH. Until then, both remain canonical.

**No new reports needed** for this topic. Implementation work begins per DA/119 §10 step 1 (persona-terminal owner socket listener).

---

## See also

- `reports/designer/215-workspace-state-of-art-2026-05-18.md` — master.
- `reports/designer/218-persona-terminal-consolidation-state-2026-05-18.md` — recommended first executor implementation.
- `reports/designer/221-lojix-arca-horizon-leaner-shape-state-2026-05-18.md` — recommended second executor implementation.
- `reports/designer/217-component-triad-mutate-authority-state-2026-05-18.md` — triad pattern the executor plane fits.
