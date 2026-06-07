# 35 — actor divergence forensics: did the generated daemon stack abandon actors by mistake?

cloud-designer, 2026-06-07. Meta-report directory (sub-agent session).

## The psyche's question

The new schema-derived triad daemon stack (`lojix`/`cloud`/`spirit`/`message`/
`triad-runtime`/`schema-rust-next`) is **synchronous thread-per-request with zero
kameo**, while the rest of the workspace is actor-dense and the guidance reads
"actors all the way." The psyche asked, pointedly:

> "Don't we have a skill that says actors all the way? … Is there a good reason
> for it or did the agent just misinterpret something I said and then started
> hallucinating and not following our actors all the way up and down guidelines…
> Literally I'm just saying we only build actor model systems. That's just
> everywhere what we do."

The task is forensic, not designerly: **establish ground truth.** Does the
guidance actually mandate actors (present tense)? Is there any *recorded* psyche
intent that authorized the generated stack being sync? Or did an agent over-read a
narrow deferral into "no actors at all" — and did I then rationalize it?

This matters because in `34/5-redesign.md` I told the psyche the actor-vs-thread
fork was "settled by intent" and that the skill "describes the eventual shape as
if it were current." If that's wrong, I owe a correction, not a defense.

## Method

Hybrid: decisive primary-source checks done inline by the orchestrator, then a
background verification/adversarial workflow to (a) confirm nothing was missed and
(b) trace the code mechanism.

- **Inline, decisive (orchestrator):**
  - *Guidance audit* — read `skills/actor-systems.md` in full.
  - *Intent forensics* — pulled the verbatim text of every record I had cited
    as authorizing the sync deferral (`czw0`, `59dr`, `opvx`, `ocu7`, `rpr5`,
    `7ca4`, `h3u7`) via the deployed Spirit CLI.
- **Background workflow (`Verify` phase, 3 agents):**
  - *Adversarial intent skeptic* — try hard to REFUTE "no record authorizes
    sync"; search the whole Spirit store + lojix/triad INTENT/ARCHITECTURE docs.
  - *Code reality + history* — confirm the stack is actually sync/zero-kameo and
    trace when/how the sync runner was introduced (commit archaeology).
  - *Guidance cross-check* — independently re-read the actor guidance + truth-pin
    to confirm the present-tense mandate isn't a cherry-pick.

## The two decisive findings (inline)

**1. The skill mandates actors in the present tense, with no carve-out for the
generated stack.** `skills/actor-systems.md` says: line 65 "Actors all the way
down"; line 86-94 "In schema-driven daemons, the three default actor-shaped planes
are Signal, Nexus, and SEMA… If that flow appears as a group of helper functions,
the actor boundary has been erased"; line 556 "Runtime roots are actors. A daemon
… is an actor"; line 588 the engine traits "must be implemented on REAL
data-bearing types — the actor / daemon root." There is **no** "today sync /
eventually actors" sentence anywhere in the skill. The carve-out I cited in `34/5`
does not exist in the text — I invented it.

**2. No record authorizes a sync, no-kameo daemon.** The records I leaned on defer
a *specific advanced trait surface*, not actors:
- `czw0` defers "full actor mailbox, backpressure, and runtime-control **traits**"
  while keeping `on_start`/`on_stop` hooks that "persona **supervision** can use"
  — i.e. it describes a *supervised actor with a minimal trait surface*, not a
  sync daemon.
- `59dr` defers "backpressure and deeper runtime-control **machinery**" — again a
  feature deferral, not an actor deferral.
- `opvx` only says the *wire contract* must not encode how parallel a daemon runs.
- `ocu7` (newest) says the kameo components `mind`/`router`/`persona`/
  `terminal-control` **migrate onto** triad_main — so triad_main is meant to be
  the *actor substrate*.

See `1-forensic-verdict.md` for the full verdict; `2`/`3` carry the workflow's
code-history and adversarial confirmation; `4-overview.md` is the synthesis.
