# 559 — the situation: we are replacing the architecture, not maintaining it

designer, 2026-06-08.

**What this is, and is not.** This is a *working* document — the current
snapshot of an in-flight architecture overhaul, written so every agent and the
psyche share one picture and stop re-litigating it each session. It is **not
intent.** The durable principles it rests on are already recorded — `ax2k`
(pre-production: design the single best shape, expect every component to change,
never weigh compatibility), `ug6i` (a contract's Rust is always regenerated from
its schema; the schema is the single source of truth), `hehp` (usage does not
justify keeping a superseded dependency), `r310` (migrate component by
component). This report is how those apply to the migration *right now*. It is
expected to go stale and be retired as the migration completes — that is the
point of it being a report and not a line in ESSENCE or a Spirit record.

## The one sentence

We are **replacing** the architecture, not maintaining it. The codebase is a
draft of a system being born; the psyche's intent is the authority, and the
existing code is not.

## What is actually real

Only the production island is shipped and load-bearing — the only code with
consumers to protect: the deployed Spirit (`persona-spirit` / `spirit-v0.3.0`
CLI), `lojix-cli`, `CriomOS*`, `horizon-rs`, `goldragon`. **Everything else is
pre-production scaffolding** — every `signal-*` contract, every component daemon,
`signal_channel!`, `signal-executor`, the hand-written daemon loops, the old
blocking listener spine. None of it has shipped. None of it has anything to
preserve.

## The rule that settles it: validity comes from the target, not from usage

The only question that decides whether code stays is: **is it the target shape?**
Never: *is it used?*

"Repo Y still imports X" is not a reason to keep X. Y is also a draft, so it is a
reason to *also* fix Y. The worked example from this week: `signal-executor`'s
four consumers (`orchestrate`, `repository-ledger`, `persona-spirit`, `upgrade`)
do not make it valid — they make four more migrations. An agent that answers "is
this still needed?" by grepping for importers is asking the wrong question and
will always conclude the old thing is load-bearing, because in a half-migrated
draft the old thing *is* still imported everywhere.

## The target shape — so "the new thing" is never ambiguous again

A component is its real self only when **all** of these hold:

- its contract is a `.schema`, lowered by schema-next, emitted by
  schema-rust-next — **no `signal_channel!`**;
- its daemon is the schema-rust-next-**emitted** triad shell on the actor
  runtime — **no hand-written accept loop, no old blocking spine**;
- execution runs through the generated **nexus** engine (`NexusWork → NexusAction`,
  `Runner::drive`) — **no `signal-executor`**;
- storage is `sema-engine`, single-writer, with schema-emitted SEMA routes;
- it is **kameo actors** end to end;
- it has exactly **two contracts** — `signal-<c>` and `meta-signal-<c>` — under
  the bare component name.

Short of *all* of that, it is a draft — regardless of how much code is in the
repo or who imports it. `spirit` is the only component that is nearly the real
thing; it runs every request through the nexus engine with zero `signal-executor`.
**It is the template; every other component is being moved to look like it.**

## What is currently dead (a working snapshot — it shrinks to nothing when done)

The scaffolding to remove and replace, not preserve: `signal_channel!`;
`signal-executor` (`Executor`/`Lowering`/`CommandExecutor`/`ObserverSet`);
hand-written daemon accept loops; the old blocking `MultiListenerDaemon` /
`BoundedWorkers` spine; `persona-*` repo/input names; `owner-signal-*` and
`signal-engine-management` third-contract forms; `signal-core`; direct
`signal-sema` projection that exists only to feed the old executor observer. This
list is transient by construction — when the migration completes it is empty,
which is exactly why it belongs in a report and not in an intent surface.

## Why agents keep fighting the psyche (the failure, named)

Agents are trained to treat existing code as ground truth — preserve behavior,
respect what is used, maintain compatibility, don't break consumers. That
instinct is correct for a live product and **catastrophic for a greenfield
rewrite.** Because the architecture changed *after* dozens of components were
built on the old shape, the repository is now mostly old-shape drafts with a few
new-shape pieces. So the codebase out-votes the psyche's intent every session: an
agent reads the majority, sees the old shape everywhere, and concludes the old
shape is the system. It then "responsibly" preserves and re-implements it — and
to the psyche that reads as the agents fighting back and resurrecting dead code.
The gap is not that the psyche is unclear. It is that agents reason from the code
when the code is a draft, and only the intent knows the target.

## How an agent should reason about any piece of code

1. Is it the **production island** (Spirit `v0.3.0`, `lojix-cli`, `CriomOS*`,
   `horizon-rs`, `goldragon`)? → leave it; that is the one place compatibility
   matters.
2. Is it the **target shape** (the checklist above)? → keep it, build on it.
3. Otherwise it is **scaffolding** → replace it with the target shape, and fix
   everything that used it (those are scaffolding too).

Never "it's used, so keep it." Never re-implement the old shape because the
surrounding code models it. When unsure whether something is target or
scaffolding, the tie-breaker is the checklist, not the import graph.

## Where this lives

This is a report — a working surface, linkable from
`protocols/active-repositories.md` so agents meet it early, retired when the
migration lands. It is deliberately **not** in `ESSENCE.md`, `AGENTS.md`, or a
Spirit record: those hold durable intent, and a target-shape checklist plus a
named-dead list are migration state that expires. The timeless rule —
*replace, don't preserve; validity from the target, not from usage* — is already
in `ax2k`/`ug6i`/`hehp`. This report is only their application to the current
fleet, and the per-component status lives in `557` (contracts), `558` (the full
persona-engine plan), and `555` (the signal-executor cutover).
