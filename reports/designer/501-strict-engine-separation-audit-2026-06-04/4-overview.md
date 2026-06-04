---
title: 501 - Strict engine separation audit - overview
role: designer
variant: Synthesis
date: 2026-06-04
topics: [triad-engine, separation, sema, nexus, signal, sema-engine, runner, cutover, structural-enforcement]
description: |
  Synthesis of the strict triad-engine separation audit. The psyche's
  requirement (record 2560): SEMA owns all state, Nexus all decisions, Signal
  all communication, nothing leaking into the daemon. Result: the spirit pilot
  PASSES intra-daemon separation and the strong half is already structural;
  but it fails the sema-engine database boundary (report 63). The five old-stack
  daemons are absent on the triad and need cutover, not a patch. The runner is
  the lever that makes the constraint structural rather than auditor-policed.
---

# 501 - Strict engine separation audit - overview

## The result, in one line

The spirit pilot's triad-engine separation **holds** — and the strong half is
already enforced by the type system. The old-stack daemons don't have the
separation at all (they predate the triad) and need cutover. The runner is
what would make the whole thing structural instead of audited.

## The pilot passes — and two lenses on "SEMA"

Slice 1: in the schema-derived spirit pilot, the strict separation holds. All
decision-making is in Nexus (the decide loop, the deciders, the
Observe→Stash→Reply recursion, the continuation budget); all durable state is
in Store; all communication is on SignalActor with the wire frame codec
**schema-emitted on the Signal types** (so the daemon hand-rolls no frames).
The Engine composer and the per-request path make no domain decision.

There are **two different lenses on the SEMA half**, and they give opposite
verdicts — both correct:

- **Intra-daemon separation** (the audit's lens on record 2560): is all
  database code *inside* the SEMA plane (Store), not leaking into Nexus /
  Signal / the daemon? **Yes — clean.** redb appears only in `store.rs` and
  the generated schema.
- **The sema-engine boundary** (the sharper lens, record 2563, system-designer
  63): does the SEMA plane reach the database *through sema-engine*, or with
  raw redb? **Fails — Store uses raw redb 2.x directly**, hand-rolling what
  sema-engine provides (including its own commit-sequence marker).

So the pilot's *separation* is sound, but its SEMA plane must **adopt
sema-engine** — the real database fix, tracked as bead `primary-w42y`. "DB in
the SEMA engine" means "via sema-engine," not "raw redb contained in Store."

Two design-questions surfaced (not forced edits): the accept loop +
length-prefix transport (`daemon.rs:152`, `transport.rs`) is runner
scaffolding with zero domain logic — extract it into the triad-runtime runner,
do NOT fold socket plumbing into SignalEngine; and the structurally-unreachable
`_ =>` defensive arm at `engine.rs:466-478` is best made a compile-time
impossibility by a `ReplyToSignal`-only runner exit type.

## The old-stack daemons are absent on the triad — cutover, not patch

Slice 2: all five old-stack daemons — persona-spirit, mind, persona, terminal,
router — have **zero** `SignalEngine`/`NexusEngine`/`SemaEngine` in their
source. They predate the triad and partition by Kameo actor/module, mixing the
three concerns. The worst is **router**: one file binds the socket, runs the
frame protocol, opens redb, AND makes routing decisions, with the durable
tables threaded into the decision actors — no SEMA boundary at all. This is not
a patchable leak; it is the **schema-derivation cutover**. All five are
blocked-needs-concept.

Recommended cutover order, with reasons: **persona-spirit** (already runs a
decision loop via signal-executor and names SEMA_WRITER/SEMA_OBSERVER in its
trace — smallest Nexus delta) → **router** (smallest state, clearest contract)
→ **mind** (already on sema-engine — smallest SEMA delta) → **terminal** →
**persona** (last; it is a manager-of-engines, a different question — whether
it becomes a derived triad or stays a hand-written supervisor is open).

## The concept: the runner makes the constraint structural

Slice 3 answers the psyche's "make a concept for how to unblock it in the
engine or the macro system." The key insight: **record 2560 can be made
structural rather than auditor-policed, and the lever is the runner already
ratified in 1574/1581.** The audit and the runner are the same problem from two
ends.

- **The strong half is already structural.** schema-rust-next emits three
  engine traits whose plane-envelope signatures (`signal::Signal` /
  `nexus::Nexus` / `sema::Sema`) make a cross-engine call a *type error* — the
  pilot ships a `compile_fail` doctest proving a Nexus value cannot reach
  `Store::apply`. The only durable verbs are `SemaEngine::apply/observe`; the
  only decision verb is `NexusEngine::decide`. The engines cannot leak into
  each other.
- **The weak half is everything around the engines** — the hand-written accept
  loop, the composer, admission, transport, `bin/main`. None of it leaks today
  (it is thin and only calls engine methods), but each is a hand-written host
  where a leak *could* live with no compiler complaint. That is exactly the
  discipline an auditor must police — and exactly what the runner deletes.
- **The concept:** a non-overridable `TriadComponent::serve()` in triad-runtime
  owns the loop + transport + composition once, generic over the engines;
  schema-rust-next emits the per-component wiring and a one-line `main`. The
  component author writes ONLY the three trait impls plus the data-bearing
  nouns. There is no hand-written code outside the engines for logic to leak
  into — **the audit becomes vacuous by construction.**

## Two design-questions for the psyche

1. **Admission policy** (route/identifier minting + validation, today
   `SignalActor::admit`): does it become a `SignalEngine` trait method (record
   2560 reads toward "all comms in the Signal engine"), or stay generic
   bookkeeping the runner owns?
2. **Runner concurrency**: stay sequential single-flight (the strongest
   single-flight guarantee, what the `&mut Nexus` borrow gives today), or grow
   a generated actor mailbox? The runner concept is correct either way; the
   concurrency model is a genuine decision, not a mechanical extract.

## What this means

The engine architecture is sound where it has been built (the pilot), and its
strongest guarantee is already in the type system. The work is: adopt
sema-engine in the pilot (bead `primary-w42y`); build the runner (the ratified
1574/1581 extraction) which simultaneously deletes the audit's grey zone and
makes record 2560 enforced-by-construction; then cut over the five old-stack
daemons in the named order. The old-stack components are blocked on the
cutover, not on a fixable leak — and the concept for unblocking them is the
schema-derivation the whole engine is built toward.
