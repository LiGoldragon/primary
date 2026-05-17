# Full Signal executor — operator complement to DA/119

*Endorses the framing in
`reports/designer-assistant/119-full-signal-executor-architecture-concept-2026-05-18.md`:
"full Signal executor" should be read as a **component-local
execution plane**, not as an extension of sema-engine. Contributes
the operator-side specifics: the falsification grounding for
"sema-engine stays verb-shaped," the actor-density argument for
keeping dispatch in the daemon, and the implementation-order
specifics for `persona-terminal` first. Rewritten in place per
`skills/reporting.md` to integrate DA/119 — the first pass of this
report missed DA/119's third meaning and treated terminal
OwnerSignal as future when it is already live.*

Date: 2026-05-18

Author: second-operator-assistant

---

## §0 — TL;DR

DA/119 names the question better. Three meanings of "full Signal
executor":

1. **Engine as protocol host** — sema-engine becomes
   contract-aware, dispatches request variants, owns reply
   shaping. **Rejected.** Breaks the kernel/domain split.
2. **Engine as transaction grouper** — sema-engine stays
   contract-blind but grows a multi-table transaction primitive
   when pressure proves it. **Defer.**
3. **Component-local execution plane** — the daemon-local actor
   topology (socket → exchange → dispatch → reducer → store +
   effects → reply/events/audit) that every triad daemon takes.
   **This is what "full Signal executor" means** in the workspace.

The first pass of this report framed the question as "engine
shape options" and missed meaning 3 — the actual workspace
answer. DA/119 §3-§4 sketches the plane shape; this report
endorses it and adds the operator-side specifics that didn't
make it into 119.

DA's prior lean ("keep split + add helpers") and the audit's
revised verdict ("keep split + defer helpers per falsification")
converge on the split. Helpers stay deferred per the falsification
witnesses at `sema-engine/tests/seam_gap_falsification.rs`.

---

## §1 — Correction: terminal OwnerSignal is already live

DA/119 §0 corrects the first pass of this report. Current
workspace state:

- `owner-signal-persona-terminal` exists.
- `OwnerTerminalRequest` carries
  `Mutate CreateSession(CreateSession)` and
  `Retract RetireSession(RetireSession)`.
- ordinary `signal-persona-terminal` no longer carries those
  variants.
- `persona-terminal` depends on the owner contract and stubs an
  owner request actor returning
  `OwnerTerminalRequestUnimplemented { reason: NotBuiltYet }`.
- the missing work is owner Unix-socket wiring + runtime
  execution, not contract placement.

The audit's two pending witnesses
(`owner-signal-request-uses-same-reducer-through-owner-socket`,
`wrong-contract-frame-does-not-reach-reducer`) shift from "blocked
on the first owner contract crate" to "blocked on owner-socket
runtime wiring." Engine-blind dispatch is the structural enabler;
the engine doesn't change.

---

## §2 — The kernel/domain split, restated

DA/119 §3 + §9.1 names the principle; this section adds the
operator-side framing the audit grounded in code.

**Sema-engine is a database library, not a protocol host.** Per
`sema-engine/ARCHITECTURE.md` §"Non-Goals":

> *"No actors in this crate. No text parser in this crate.
> No daemon process in this crate."*

The engine is contract-blind by design. A contract-aware engine
(DA/119 meaning 1, the first-pass report's "Flavor A") would
require the engine to:

- register handlers per `signal_channel!`-emitted request variant,
- own per-variant dispatch tables and validation hooks,
- shape replies inside the engine,
- host the post-commit event projector.

Each of those moves a daemon-local plane into the engine. The
plane that suffers most is **dispatch**.

### §2.1 — Dispatch is an observable actor plane

Per `skills/actor-systems.md` §"Core rule":

> *"An actor-heavy system should look over-named to conventional
> Rust eyes. That is expected."*

The daemon's `IngressPhase` / `DispatchPhase` / `DomainPhase` /
`ReplyShaper` trace nodes are NAMED PLANES that
`skills/architectural-truth-tests.md` witnesses depend on. A
witness like `request_cannot_bypass_required_actor_plane` exists
*because* dispatch is a plane in the daemon.

If sema-engine absorbs dispatch, the daemon's topology shrinks to
a socket actor + an engine ref. The trace-pattern test plane
loses its substrate. That isn't "elegance gained" — it's
observability lost.

DA/119's plane shape (`SignalExchangeRuntime`,
`ComponentSignalExecutor`, `ComponentReducer`,
`SemaEngineOwnerActor`, `EffectSupervisor`, `ReplyEventProjector`)
keeps these planes in the daemon. The plane names become the
standard topology shape every triad daemon takes; architectural
truth witnesses stay per-component.

### §2.2 — Match-on-variant *is* the dispatch plane

DA/119 §4.3 says generated handler traits are optional, §11 Q2
says "defer until measured repetition appears." The operator-side
reason is the same as §2.1: the match arms aren't pattern-matching
ceremony — each arm names a flow and records trace nodes. The
Rust compiler catches missed variants on the closed contract enum.
A macro-generated handler trait would replace the matched arms
with trait method bodies; the routing semantics still appear
once per variant. Net gain: keystrokes. Net loss: explicit
topology.

This isn't an argument against macros forever. It's an argument
against generating dispatch as a default. Concrete repetition
across two components is the right trigger to revisit; the
audit's first pass proposed the dispatcher trait too eagerly and
the revised audit /2 §4.4 retracted it.

---

## §3 — What the falsification + DA/119 converge on

The audit at
`reports/second-operator-assistant/2-signal-core-sema-engine-fit-audit-2026-05-17.md`
landed six wire→engine seam witnesses
(`sema-engine/tests/signal_core_seam.rs`) and six gap-falsification
witnesses (`sema-engine/tests/seam_gap_falsification.rs`). The
verdict aligns with DA/119:

| Question | Audit (post-falsification) | DA/119 |
|---|---|---|
| Sema-engine as verb-shaped library? | Yes | Yes (§0.5) |
| Engine as protocol host? | No (Flavor A rejected) | No (meaning 1 rejected, §0.5) |
| `validate_write` helper? | Dissolves into `match_records` composition | Don't add speculatively (§0.5) |
| `commit_multi` helper? | Real but unpressed; schema redesign usually cleaner | Wait for actual consumer (§0.5) |
| `unsubscribe` helper? | Soft; component supervisor + sink filter covers correctness | Don't add speculatively (§0.5) |
| Dispatcher-trait macro? | Reconsidered; normal Rust pattern matching | Defer until measured repetition (§4.3, §11 Q2) |

Where DA/119 extends: it names **what to do instead** — the
daemon-local execution plane with the planes in §3-§4. That's
the answer to "full Signal executor" the workspace converges on.

### §3.1 — Effectful-operation discipline

DA/119 §4.7 and §11 Q3 name the rule operations involving
external resources should follow:

1. Validate and reserve durable intent.
2. Commit pending state.
3. Run the effect.
4. Commit success or failure.
5. Emit the reply/event from the committed result.

This handles cross-table atomicity for the operations that most
need it — those touching external resources — without growing
the engine. The saga/outbox shape lives in the daemon's
`EffectSupervisor` per DA/119 §4.7.

### §3.2 — `commit_multi` deferred, schema-first when it surfaces

Pure-state multi-table operations (no external effect) are the
remaining candidates for Flavor B (`Engine::commit_multi` or a
typed transaction handle). The likely first candidate is
`RoleHandoff` once persona-mind implements it. The cleanest
resolution path is usually schema redesign: express handoff as
`Mutate` on the claims table (one table, structural atomicity
in existing `Engine::commit`) rather than `Retract+Assert`
across two tables. The audit's witness
`cross_table_writes_via_two_engine_commits_are_not_engine_atomic`
confirms the gap exists; the workspace's preferred path per
`ESSENCE.md` §"Beauty is the criterion" is "find the structure
that makes the special case dissolve" — usually a one-table
schema.

If a genuinely multi-table operation surfaces that resists
schema redesign, Flavor B is the small contract-blind addition.
Not before.

---

## §4 — Implementation order (operator angle)

DA/119 §10 recommends `persona-terminal` first, then
`lojix-daemon`. The operator-side specifics:

| Step | Operator-side work | Discipline reference |
|---|---|---|
| 1. Owner Unix-socket listener in `persona-terminal` | Socket actor bound to the owner socket path from the spawn envelope. | `skills/kameo.md` §"Mailbox"; `persona-mind/transport.rs` is the in-tree pattern. |
| 2. `TerminalSignalExecutor` module | Inside `persona-terminal`, not in a shared crate. Two ingress adapters: ordinary + owner. One actor per Signal contract surface per `skills/component-triad.md`. | `skills/component-triad.md` invariant 5 + DA/116 §A5. |
| 3. One Sema owner actor | The `StoreKernel` pattern from `persona-mind/ARCHITECTURE.md` §4 — single `Engine` handle, single-writer-actor discipline. | `sema-engine/ARCHITECTURE.md` §"Constraints". |
| 4. `CreateSession` with durable pending state | Three-phase per DA/119 §4.7: reserve name → spawn → mark ready/failed. Each transition is a `Mutate` op through the Sema owner. | `skills/rust/storage-and-wire.md`; engine.rs `Mutation` API. |
| 5. `RetireSession` | Symmetric: mark retiring → shut down terminal-cell → mark retired (or remove). | Same. |
| 6. Witnesses per DA/119 §10 | All daemon-side. The engine doesn't grow new APIs. | `skills/architectural-truth-tests.md`. |

Each step is one logical commit. The Rust-side discipline follows
`skills/rust-discipline.md` (typed errors per crate, no
`anyhow`/`eyre` at boundaries, domain newtypes, methods on types)
and `skills/kameo.md` (actors per plane, no blocking handlers,
release before notify, supervised state-bearing actors on
`.spawn()` not `.spawn_in_thread()` until Kameo grows
`pre_notify_links`).

`lojix-daemon` follows the same plane shape against a non-Persona
domain (Horizon projection + Nix build/deploy effects). When both
implementations exist and the plane is genuinely reusable, the
eventual `signal-executor` library crate per DA/119 §8 becomes
worth extracting.

---

## §5 — Residual uncertainties

Most are named in DA/119 §11. The operator-side residuals worth
flagging:

1. **Audit /2 §3 framing residue.** The first pass of /2 framed
   match-on-variant dispatch and receipt-to-reply shaping as
   "boilerplate." DA/119 §11 Q5 correctly notes /2 is internally
   uneven on this. Companion edit to /2 §3 (landing alongside this
   report) reframes these as component-side responsibilities,
   aligning the section with the revised verdict.
2. **Detached-thread-per-delta cost under load.** Still
   un-benchmarked. `SubscriptionDeliveryMode::Inline` is the
   actor-shaped workaround for high-throughput consumers; whether
   it suffices is empirical.
3. **`SemaEngineOwnerActor` supervised-restart trap.** Per
   `reports/operator-assistant/138-persona-mind-gap-close-2026-05-16.md`
   §"P2", supervised state-bearing actors using
   `.spawn_in_thread()` race redb teardown because Kameo's
   `notify_links` fires before `Self::drop()`. The workaround for
   every daemon's Sema owner: stay on `.spawn()` until upstream
   Kameo grows `pre_notify_links`. Already discipline in
   `skills/kameo.md` §"Blocking-plane templates" Template 2;
   re-flagging here because the executor plane in every triad
   daemon will hit this.

---

## See also

- `~/primary/reports/designer-assistant/119-full-signal-executor-architecture-concept-2026-05-18.md`
  — the canonical concept report. This report endorses it and
  adds operator-side specifics.
- `~/primary/reports/second-operator-assistant/2-signal-core-sema-engine-fit-audit-2026-05-17.md`
  — the audit + falsification grounding; verdict "good fit; no
  engine API additions required." Companion edit lands alongside
  this report cleaning up §3 framing residue.
- `~/primary/reports/designer-assistant/116-permission-scoped-signal-contracts-and-sockets-2026-05-17.md`
  — OwnerSignal as a first-class executor surface (settled
  answers A1-A5).
- `~/primary/skills/component-triad.md` — the five triad invariants;
  invariants 4 + 5 land alongside this executor framing.
- `~/primary/skills/actor-systems.md` §"Core rule" — actor density
  is the workspace's preference for dense observable daemons.
- `~/primary/skills/architectural-truth-tests.md` — the witness
  shape that depends on daemon-side actor topology.
- `~/primary/skills/kameo.md` §"Blocking-plane templates" — the
  supervised state-bearing actor restart trap §5 flags.
- `/git/github.com/LiGoldragon/sema-engine/tests/signal_core_seam.rs`
  — six wire→engine seam witnesses.
- `/git/github.com/LiGoldragon/sema-engine/tests/seam_gap_falsification.rs`
  — six falsification witnesses.
- `/git/github.com/LiGoldragon/owner-signal-persona-terminal/` — the
  live owner contract DA/119 §0 corrects on.
