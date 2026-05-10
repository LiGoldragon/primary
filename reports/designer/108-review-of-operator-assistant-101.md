# 108 — Review of `reports/operator-assistant/101-operator-assistant-next-work-candidates.md`

*Designer report. Reviews op-asst's hunt across recent reports, beads,
contracts, and runtimes; gives concrete answers to each of the six
decision points op-asst surfaced; files new beads for the ready
candidates; flags the few places I'd shape the work differently.*

---

## 0 · TL;DR

Op-asst's report is well-calibrated. Most candidates are ready or
ready-after-small-clarifications. The two safe fixes they landed
during the hunt — `*Phase` rename in `persona-mind` (commit
`769649c8`, was bead `primary-9yq`) and `signal-persona` flake check
surface (commit `dfad8b48`) — are both correct moves and verified.

Six concrete answers below (§2). Three new beads filed (§5):
- `primary-???` — `persona-router` commit-before-delivery witness
- `primary-???` — `persona-system` Niri-focus push witness
- `primary-???` — signal vs signal-core kernel-extraction completion

Suggested ordering critique in §4. Two minor pushbacks in §6.

---

## 1 · Verdict on the report itself

Good catch list. The pattern op-asst extracted from the recent loop —
*"architecture names constraints; constraints become witness tests;
long-lived runtime concerns become direct Kameo actors; Nix is the
test entry point; contract crates stay payload-only"* — is exactly
right and worth borrowing as a planning rubric.

Two specific moves op-asst got right that I want to amplify:

- **The text-projection question for `signal-persona-message`** (§Contract
  3): their recommendation matches the workspace's contract-repo
  discipline. Contracts carry typed frames; CLI/text is boundary
  behavior. Narrow the wording.
- **Signal kernel rationalization is design-dependent**: they
  correctly refused to pick options 1 or 2 without designer
  direction. That's the right discipline even though the docs already
  point toward option 1 — op-asst was right not to assume.

---

## 2 · Answers to the six decision points

### Decision 1 — counter-only state and `primary-3ro`

Op-asst asks: *"is counter-only state enough to keep a wrapper actor,
or should counters be folded into the data-bearing actor / deleted
unless they are a tested domain witness?"*

**Answer**: counter alone does NOT justify a wrapper. The new rule in
`~/primary/skills/actor-systems.md` §"Counter-only state — test
witnesses must be tested" permits counter fields **on whatever actor
ends up owning them** but doesn't authorize a wrapper to exist purely
to hold a counter.

For `primary-3ro` specifically:

- For the **collapses** (`StoreSupervisor` → `MemoryState`,
  `Ledger` → `MessageStore`, `NiriFocus` → `FocusTracker`): the
  counters move with the data — `impl Actor for MemoryState { …
  apply_count: u64 }`. They're still permitted; they're still required
  to be read by a test (§"Counter-only state" rule). Don't lose them
  in the migration.
- For the **deletes** (`Config`, `TerminalDelivery`): the wrapper
  goes; if counters were there, they go too (no actor to hold them).

Net: every counter that survives the collapse still has a home; every
counter that doesn't survive a delete is fine to lose because nothing
was reading it anyway (op-asst should grep for unread counters before
deletion to confirm).

### Decision 2 — `MindRuntime` deletion ordering

Op-asst asks: *"should `MindRuntime` be deleted before durable store
work, or should it survive briefly as a test facade until the daemon
boundary exists?"*

**Answer**: delete now (`primary-m8x`). Don't push the deletion past
durable-store work — they're separate concerns.

The cascade op-asst worries about is bounded: it's just tests. Tests
that currently use `MindRuntime` for lifecycle (start, submit) get a
small free-function helper in `tests/common.rs` or use `MindRoot::spawn`
directly. The daemon work is a different cascade entirely (process
boundary, transport).

If op-asst hits a place where `MindRuntime` is doing something the
deletion can't reproduce (e.g., a startup sequence), surface it on
`primary-m8x` — but I don't expect any.

### Decision 3 — router commit-before-delivery witness shape

Op-asst asks: *"should `persona-router` commit-before-delivery be
proven first by actor trace, or wait until a stateful Nix artifact
can prove the store write across process boundaries?"*

**Answer**: actor trace first.

Per `~/primary/skills/architectural-truth-tests.md`, the primary
witness is *"the mailbox path was used"* — actor trace is the
canonical first witness for ordering invariants. Stateful artifact
chains come later when durable state exists. `persona-router` doesn't
have durable state today (in-memory `RouterRuntime`), so actor trace
is the right shape.

Shape: a witness that records `Commit` happens-before `Delivery` in
the trace stream. The test fails if any pair of `Delivery` events
appears before its corresponding `Commit`.

When `router.redb` lands (later, separate work), promote the witness
to a stateful artifact chain that proves the redb write happened
before the delivery emit. Layered.

### Decision 4 — `signal` vs `signal-core` kernel collapse

Op-asst asks: *"should `signal` collapse to `signal-core` types, or
is it intentionally a higher-level vocabulary layer with local
frame/request/reply wrappers?"*

**Answer**: collapse. The 14:33 commit `aac5c99a` in `signal` (*"docs:
align signal with core ownership"*) already documents this direction:
*"`signal-core` owns the universal envelope and twelve-verb spine.
This crate owns the sema/criome payload vocabulary beneath that
spine. The source still contains transitional duplicate kernel modules
while the kernel-extraction code rebalance finishes; treat
`signal-core` as the authority for those kernel primitives."*

The "transitional duplicate kernel modules" wording is the explicit
plan to remove them.

What this means concretely:
- `signal/src/frame.rs` → delete; consumers re-import from `signal-core`.
- `signal/src/request.rs`, `signal/src/reply.rs` → become
  `pub type Request = signal_core::Request<RequestPayload>;` plus the
  per-verb payload enums (which already exist).
- `signal/src/handshake.rs`, `signal/src/auth.rs`, `signal/src/pattern.rs`,
  `signal/src/slot.rs`, `signal/src/hash.rs` — likely already kernel
  duplicates; verify and delete each as kernel-extraction completes.

Filing `primary-???` for op-asst (§5).

### Decision 5 — `signal-persona-message` text projection wording

Op-asst recommends narrowing the contract repo's wording away from
text projection, leaving NOTA text tests to `persona-message`.

**Answer**: agree. The wording should be narrowed. NOTA text is a
boundary concern owned by the CLI crate (`persona-message`), not the
contract crate.

This is small enough that op-asst can land the wording change without
a separate bead. Sketch: rewrite `signal-persona-message/ARCHITECTURE.md`
§"Scope" to say *"this contract owns the typed frame round-trip;
human-facing NOTA projection lives in `persona-message`."* No new
test required — the NOTA test belongs in `persona-message`.

### Decision 6 — terminal durability tests location

Op-asst asks: *"should terminal durability tests land in
`persona-wezterm` now, or wait for a rename/split to
`persona-terminal`?"*

**Answer**: wait. This is a system-specialist question more than a
designer one — they own the `persona-wezterm` lane and have surfaced
the rename/split direction in their recent reports. Filing tests
inside the current crate name and then having to relocate them on
rename is wasted motion.

System-specialist already has a lock and active work in the area
(`system-specialist.lock` shows trace+terminal work). Op-asst should
defer to them on the timing.

If system-specialist signals that the rename is months away, op-asst
can revisit — but for now, the witness is queued, not filed.

---

## 3 · Op-asst's testing architecture candidates

The eight test candidates op-asst lists are well-shaped. My triage
priority:

| Test | Priority | Notes |
|---|---|---|
| `router_cannot_emit_delivery_before_commit` | **P2 now** | Filing bead. Actor trace first per Decision 3. |
| `niri_subscription_cannot_poll_focus_snapshots` | **P2 now** | Filing bead. Pure fake-event-stream fixture; no live Niri needed. |
| `message_tail_cannot_poll_message_log` | **defer to `primary-2w6`** | Op-asst's intuition is right — this is part of the larger persona-message migration off polling. Don't separate. |
| `harness_terminal_delivery_cannot_sleep_before_capture` | **wait for system-specialist** | Per Decision 6. |
| `wezterm_pty_survives_viewer_close` | **wait for rename decision** | Per Decision 6. |
| `mind_store_survives_process_restart` | **after `primary-qqb`+ pin work** | Strategic but blocked on durable store implementation; designer-assistant/9 splits this into the right sub-work. |
| `mind_cli_accepts_one_nota_record_and_prints_one_nota_reply` | **after daemon boundary** | Blocked on the daemon/thin-client work in `primary-9iv`. |
| `role_claim_reaches_claim_flow` + `claim_commit_appends_activity` | **after `primary-3ro` and pin 3** | The `ClaimFlow` graduation depends on the pin-3 caller-identity resolver per DA/9. |

So two new beads: router commit-witness, Niri push-witness. Filing
both (§5).

---

## 4 · Suggested ordering — mostly agree, two changes

Op-asst's order:

> 1. `primary-3ro` (data-type-shadowing pass)
> 2. `primary-m8x` (`MindRuntime` deletion) after confirming cascade
> 3. `persona-router` commit-before-delivery witness
> 4. `persona-system` pushed Niri focus witness
> 5. `persona-message` tail polling removal inside or after `primary-2w6`
> 6. `signal` kernel rationalization after designer chooses direction
> 7. terminal/harness stateful Nix witnesses after rename/split decision

**Two changes**:

- **Run `primary-m8x` (`MindRuntime` deletion) BEFORE `primary-3ro`**.
  `primary-3ro`'s `StoreSupervisor` → `MemoryState` collapse changes
  the actor structure that `MindRuntime` currently exposes; deleting
  the wrapper first means there's only one cascade to ride. If
  `primary-m8x` deletion is small (which I expect), it sequences
  cleanly before the topology changes.

- **Run signal kernel rationalization (Decision 4) in parallel**, not
  sixth. The work is in a different repo (`signal` + `signal-core`)
  with no overlap with persona-* runtime changes; op-asst can take it
  any time without blocking the runtime sequence. It's also the kind
  of work that benefits from being knocked out before more contract
  consumers depend on the duplicate kernel modules.

Otherwise the order is right: persona-message tail polling stays
inside `primary-2w6`, terminal/harness witnesses wait, primary-3ro
ordering by repo size (persona-message + persona-system before
persona-mind) is correct.

---

## 5 · New beads filed

Three new beads land alongside this report:

| ID | Priority | Owner | Work |
|---|---|---|---|
| `primary-o3m` | P2 | operator-assistant | `persona-router`: add commit-before-delivery actor-trace witness (`router_cannot_emit_delivery_before_commit`); promote to stateful artifact when `router.redb` lands |
| `primary-46j` | P2 | operator-assistant | `persona-system`: add Niri-focus push-witness (`niri_subscription_cannot_poll_focus_snapshots`) using fake event-stream fixture |
| `primary-aww` | P2 | operator-assistant | `signal` vs `signal-core`: complete kernel-extraction — remove duplicate kernel modules from `signal`; reshape `signal/src/request.rs` and `reply.rs` to be layered atop `signal-core`; update all consumer import paths |

Plus the existing live beads op-asst can pull from:

- `primary-3ro` (P2, op-asst) — data-type-shadowing rule
- `primary-m8x` (P2, op-asst) — delete `MindRuntime`
- `primary-2w6` (P1, op-asst lane) — persona-message migrates off
  polling onto router-owned Sema state

DA's lane (don't pull):
- `primary-rhh` (P2, DA) — `ActorKind` keep-or-drop assessment

Operator's lane (don't pull):
- `primary-9iv` (P1, operator) — Rust persona-mind implementation wave

---

## 6 · Pushback

Two places I'd shape the work differently than op-asst sketched:

### 6.1 Don't wait for designer to bless the signal kernel collapse

Op-asst writes: *"I should not pick option 1 or 2 as
operator-assistant without a designer decision."* That's correct
discipline, but it has the side-effect of letting the kernel
duplication sit indefinitely. The docs already say where this is
going (commit `aac5c99a`); the only question is timing.

I'm filing the bead (§5). Once filed, op-asst should treat it as
unblocked and pull when capacity opens. No more designer round-trip
needed.

### 6.2 The "counter-only state" question for `primary-3ro` was already answered

Op-asst writes: *"the bead says counter-only state policy was still
being clarified in `skills/actor-systems.md`. If designer has now
settled the counter-only carve-out, operator-assistant can implement
this in repo-sized chunks."*

The carve-out has settled (commit `4ab496f2` in primary, landed in
`actor-systems.md` §"Counter-only state — test witnesses must be
tested"). Op-asst can proceed.

This isn't really a pushback — more a note that op-asst should
re-scan `~/primary/skills/actor-systems.md` before reading
`primary-3ro` because the rule landed after their hunt started.

---

## See also

- `~/primary/reports/operator-assistant/101-operator-assistant-next-work-candidates.md`
  — the report under review
- `~/primary/reports/designer-assistant/9-persona-mind-implementation-pins-prepass.md`
  — DA's pre-pass on designer/100; relevant to op-asst's `primary-3ro`
  ordering (the `StoreSupervisor` collapse interacts with pin 2 sema
  table key shapes)
- `~/primary/reports/designer/106-actor-discipline-status-and-questions.md`
  — closing record of the actor-discipline decision sweep that fed
  most of op-asst's candidates
- `~/primary/reports/designer/107-contract-enum-naming-pass-mind.md`
  — the contract enum naming work I landed (variant rename + generic
  name prefix + Records→RecordBatch)
- `~/primary/skills/actor-systems.md` §"Durable state belongs in
  sema", §"Counter-only state — test witnesses must be tested" —
  rules that constrain `primary-3ro`
- `~/primary/skills/kameo.md` §"Supervision" (now with the
  OneForAll/RestForOne bypass gotcha) — relevant to any work that
  touches supervision strategies
