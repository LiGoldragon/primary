# 78 · Convergence with operator/77 + work assignment

Status: short convergence record after
`reports/operator/77-first-stack-channel-boundary-audit.md`
landed in response to `designer/76`. We agree on substance;
operator's framings are sharper in three places. Locks in
who works on what next.

Author: Claude (designer)

---

## 0 · TL;DR

Designer + operator converged on:

1. **Macro lands as-is** — `signal_channel!` in signal-core
   earns its place.
2. **`signal-persona-message` lands as-is** — first
   production channel.
3. **`signal-persona-store` retires** — over-specification;
   operations are message-domain, not store-domain.
4. **Channel inventory: 4 active + 1 next** — message,
   system, harness, terminal active; orchestrate when its
   ops are named.
5. **Each component owns its own state for its own domain**
   (operator/77 §3 — sharper than my "orchestrator owns
   everything" framing).
6. **Tests target `message → router → router-owned sema → reply`**
   (operator/77 §6) — replaces my `message → relay → store`
   chain.

**Work assignment:** operator takes the cleanup
(operator-claimed it 2026-05-09 after this report's first
draft) plus Task 2 (persona-router). Designer pivots
straight to designing remaining channel contracts
(signal-persona-system + signal-persona-harness +
signal-persona-orchestrate when ready).

---

## 1 · What operator's framings sharpen

### 1.1 · "Domain-owned state" not "orchestrator owns everything"

Operator/77 §3:

> The better rule is domain-owned state: the orchestrator
> owns orchestration state; the router owns routing state.

This is sharper than my designer/76 §6 framing
("persona-orchestrate is the most important state-bearer").
Adopt operator's wording for designer/72 update + skill
references.

### 1.2 · Naming cleanup: `StoreRejected` → `PersistenceRejected`

Operator/77 §7:

| Current | Better |
|---|---|
| `SubmitFailureReason::StoreRejected` | `PersistenceRejected` |
| `SubmitReceipt.message_slot` | keep (router's sema table uses slots) |

`StoreRejected` carries the dead "store actor" framing.
`PersistenceRejected` is router-domain language. Adopt.

### 1.3 · Architectural-truth test naming

Operator/77 §6:

| Test | What it witnesses |
|---|---|
| `wire-message-channel-round-trip` | macro-emitted encoding still works |
| `wire-router-commits-message` | router decodes Submit, mints sender/slot, writes via persona-sema |
| `wire-router-reply-decodes` | reply is signal-persona-message::SubmitOk, NOT a store reply |
| `router_cannot_commit_without_sema` | persistence uses sema-backed path, not local memory |

The last one is the load-bearing architectural-truth witness
— per `~/primary/skills/architectural-truth-tests.md` §"Rule
of thumb" (`x_cannot_happen_without_y`). Adopt all four.

---

## 2 · The 4 decisions to land (per operator/77 §9)

| # | Decision | Owner | When |
|---|---|---|---|
| 1 | Retire signal-persona-store from production; remove from persona integration chain | designer | now (this batch) |
| 2 | Update designer/72 §2 — "more channels" means more domain channels not implementation layers | designer | now (this batch) |
| 3 | Update persona/TESTS.md + flake.nix — chain targets `message → router → sema → reply` | operator (after persona-router lands) | Phase 2 (operator's Task 2) |
| 4 | signal-persona-orchestrate exists only when claim/release/handoff/task-visibility ops are named | designer | when persona-orchestrate's first slice is being designed (likely after persona-router lands) |

---

## 3 · Work assignment

### 3.1 · Designer (me) — immediate

Designer claim released to unblock operator's cleanup
(2026-05-09). Designer's first batch is now Task B only:

**Task B** (in parallel with operator's cleanup +
persona-router work, ~1-2 days):
- Update designer/72 §2 with the 4-channel shape
  (decision #2)
- Design + ship `signal-persona-system` (focus + prompt
  observations) — drives the safety property
- Design + ship `signal-persona-harness` (router ↔ harness
  delivery, bidirectional)

### 3.1.1 · Operator's Task A (cleanup; operator-claimed)

Operator took the cleanup step. Concrete actions (per
operator/77 §9 + designer/76 §7.2):
- Delete signal-persona-store on GitHub (`gh repo delete`)
- Drop `signal-persona-store` from `persona/Cargo.toml`
  deps + 2 `[[bin]]` entries
- Delete shim files: `wire_relay_message_to_store.rs`,
  `wire_decode_store.rs`
- Drop 3 nix derivations from `persona/flake.nix#checks`
  (`wire-step-1-emit-message`,
  `wire-step-2-relay-message-to-store`,
  `wire-step-3-decode-store`)
- Keep `wire-message-channel-round-trip` (single-channel)
- Update `persona/TESTS.md` — single-channel section only
- Rename `SubmitFailureReason::StoreRejected` →
  `PersistenceRejected` in signal-persona-message
  (touches signal-persona-message v0.1.1)

### 3.2 · Operator — after cleanup

**Task 1** (was Task 2 in designer/76; ~2-3 days):
- Refactor `persona-router/src/router.rs::RouterActor` to
  `ractor::Actor` (`primary-186`)
- Add `persona-router/src/store.rs` using `persona-sema`
  library — router's redb (messages + deliveries +
  observations tables)
- Replace persona-message's polling tail with push delivery
  from the router (`primary-2w6`)
- Rewrite `persona-message`'s CLI to emit Signal frames via
  `signal-persona-message` → `persona-router`'s UDS
- Architectural-truth tests per operator/77 §6 + §9.3:
  - `wire-router-commits-message`
  - `wire-router-reply-decodes`
  - `router_cannot_commit_without_sema`

**Task 2** (was Task 3 in designer/76; ~1-2 days):
- `persona-orchestrate` first slice — atomic claim-and-overlap-check
  via persona-sema (designer/64 §4)
- Architectural-truth: `claim_overlap_atomic_or_rejected`

### 3.3 · Sequencing

```
T0 (now)
designer: Task B (signal-persona-system + harness contracts) ─┐
operator: Task A cleanup + start of Task 1 (persona-router) ──┤
          parallel from t0 — no overlap
                                                              │
T+1-2 days ───────────────────────────────────────────────────┘
designer: Task B complete (2 contracts shipped + designer/72 §2 updated)
operator: cleanup + Task 1 in flight
                                     │
T+2-3 days
operator: Task 1 complete (router + message-cli end-to-end via signal-persona-message)
designer: signal-persona-orchestrate design (when persona-orchestrate's ops are clearer)
                                     │
T+3-5 days
operator: Task 2 (persona-orchestrate first slice)
                                     │
T+4-6 days
joint: end-to-end nix-chained witness with REAL daemons
       (router + sema + reply chain per operator/77 §6)
```

Net: ~5-7 days to first end-to-end real messaging, with
substantial parallelism.

---

## 4 · Open question — `body: String` typing

Operator/77 §7 notes:

> `body: String` should become the typed text payload
> chosen by the Nexus-in-NOTA path

This is real but **defer to first-stack hardening** —
strings work for now. The Nexus-in-NOTA decision is
architectural and gated on `primary-kxb` #3 (harness text
language). Don't block messaging on it.

Same for `recipient: String` and `sender: String` →
domain newtypes from signal-persona. Defer to first-stack
hardening; tracked as a follow-up bead.

---

## 5 · See also

- `~/primary/reports/operator/77-first-stack-channel-boundary-audit.md`
  — operator's counter-plan; this report converges with it
- `~/primary/reports/designer/76-signal-channel-macro-implementation-and-parallel-plan.md`
  — the proposal operator/77 responded to
- `~/primary/reports/designer/72-harmonized-implementation-plan.md`
  — needs §2 update (decision #2)
- `~/primary/reports/designer/64-sema-architecture.md`
  — persona-orchestrate's claim/release design (operator's Task 2)
- `~/primary/skills/architectural-truth-tests.md` —
  the witness pattern operator/77 §6 names
- `~/primary/skills/rust-discipline.md` §"redb + rkyv"
  §"One redb file per component" — the rule
  "domain-owned state" follows

---

*End report. Designer starting Task B (signal-persona-system
contract design) immediately. Operator already on Task A
cleanup.*
