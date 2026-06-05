# 76.0 — Frame & method: do message and router overlap enough to merge?

Role: system-designer. Date: 2026-06-05. Session unit: this directory (GC'd whole).

## The question

The psyche asked, after I described message as a "stateless" component in the 75
roadmap: *"So are you saying message feels like a stateless design because of router?
So are message and router essentially overlapping in functionality and should there
just be one of them? Or is there something useful that message can do that we don't
need in router?"*

Three sub-questions, in order: (1) is message thin *because* router absorbs its state;
(2) are the two redundant — should there be one component; (3) what is message's
irreducible value, if any.

## Why this got a workflow and not a from-memory answer

My 75 reports called message "stateless / no durable ledger," which is in tension with
intent `l3k4` ("message creates a log event for the EXISTENCE of the message"). That
tension meant I could not answer from memory without risking repeating my own
imprecision. So the question is answered from **source**, not docs or my prior reports.

## Method (workflow `message-vs-router-overlap`, 7 agents, ~528k tok)

Two phases:

- **Enumerate (3 parallel readers).** One read the message component end-to-end
  (`/git/.../message` daemon + `signal-message` contract + `message/INTENT.md`); one
  read router the same way (`/git/.../router` + `signal-router` + `meta-signal-router` +
  `router/INTENT.md`); one mined the intent rationale (Spirit queries + `INTENT.md` +
  reports 74/75). Each returned a structured capability ledger: every distinct
  capability, whether it touches durable state, its authority surface, and — the crux —
  whether the *sibling* already does or structurally could absorb it. Plus each
  component's durable facts, sockets, irreducible value, and an honest overlap read.

- **Judge (4-lens panel, parallel).** Given the full enumeration, four independent
  judges each rendered a merge-vs-separate verdict from one lens only: **authority
  surface** (untrusted ingress vs delivery authority on one process), **durable fact**
  (existence vs delivery — one ledger or two), **future pipeline** (message → router →
  agent → harness; does message stay load-bearing), and **simplicity / accidental
  complexity** (steelman the merge hard, default to skepticism). Each judge was told to
  fill `whatMessageUniquelyProvides` with the literal word NOTHING if message read as
  redundant from its lens.

The judge panel saw the complete picture (a genuine barrier — each judge reasons over
all three enumerations), so the phase-1 → phase-2 boundary is a `parallel()` barrier,
not a pipeline.

## What is source-verified vs intent-asserted vs inferred

- **Source-verified** (agents cite file:line): message's SO_PEERCRED read
  (`message/src/daemon.rs:725-748`), the socket modes (message.sock 0660 / router.sock
  0600), router's *zero* peer-credential code (empty grep across `router/src`),
  router trusting `stamped.origin` verbatim (`router.rs:1095`), router's seven redb
  tables, the existence record being written by **router** today
  (`router.rs:1163 persist_message`), the message-cannot-own-a-ledger Nix + source-scan
  constraint tests, and the absence of any existence-log emission in message's source.
- **Intent-asserted**: the existence-vs-delivery fact split (`l3k4`/`17ss`), the
  agent-abstraction pipeline (`w4jp`/`gdbf`), per-repo `INTENT.md` ("both are stateless
  boundary surfaces").
- **Inferred** (the panel's judgment, not a quoted source): the fragility note — that
  message's separation is defensible-but-thin TODAY and rests on the address-space
  isolation argument until the `l3k4` existence-log is built.

## Discipline

Read-only on the code repos (`/git`). No intent captured: the psyche asked a question,
made no decision — a decision to build (or not) the existence-log would be the durable
intent, and that is the fork left open in `1-overview-verdict.md`. The raw per-agent
structured output lives in the workflow transcript
(`woslvth2n` / `wf_39217750-840`); this directory carries the synthesis.
