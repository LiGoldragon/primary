---
title: 89 — the guardian, as I understand you want it (records, deletion, referents)
role: system-designer
variant: Understanding
date: 2026-06-11
status: pre-audit — reflecting intent back for confirmation, not yet auditing
---

# The guardian as I understand you want it

You asked for my understanding of how you want the guardian to work *before* you
send me on an audit — so this report states the intended shape and marks, for
each piece, whether it is **settled** (captured intent or built), a **gap** (the
thing you're now asking for, not yet there), or **my inference** (where I'm
filling a hole and need you to confirm). It is grounded in a first-hand read of
`src/guardian.rs` and designer report 585, plus a fan-out across the daemon code,
the `signal-spirit` / `meta-signal-spirit` contracts, the designer/operator
design trail (567/572/577/578/581/582/583/584/585; operator 351–357), the
**referent** concept end-to-end, and read-only probes of the live daemon.

## 0. One paragraph

The guardian is Spirit's **semantic admission authority**: the one place an LLM
judgment decides whether a change to the durable intent layer may happen, so the
live store stays *mutually consistent at rest* by construction rather than by
later cleanup. You want its reach to be **complete over two curated sets** —
the **record set** and the **referent vocabulary** — and over **both
directions** of change to each: things entering and things leaving. Today it
guards exactly one door (record `Propose`); you're asking it to guard the rest
(deletion and the other live-arrow-changing writes) and to grow a **second gate
on accepting new referents**. The daemon stays the gate; an agent stays the
brain; the verdict stays binary-with-typed-reasons and fail-closed. The
principle underneath: *no durable mutation to either set enters or leaves without
semantic admission against the relevant existing world.*

## 1. What the guardian is today (built, live)

The deployed daemon is `spirit` v0.8.0 (the agent side runs `gemma-4-26b-a4b`
via the `criomos-local` provider). What ships:

- **One gated door: record `Propose`.** A client proposes an `Entry`; the daemon
  gathers relevant existing records (`guardian_records_for`), hands the candidate
  + bundle to the agent over a Unix socket, and acts on a **binary typed
  verdict** — `GuardianVerdict [Accept (Reject)]`, where `Reject` carries a
  closed `GuardianRejectionReason` + an `Explanation`. Accept → write; Reject or
  any failure → `GuardianRejected`.
- **The daemon is the gate, the agent is the brain.** The daemon routes and
  executes; it never judges and never parses NOTA (the CLI already typed the
  record). This matches decision `mrkv` and `l98v`.
- **Fail-closed.** Socket down / malformed verdict / timeout → reject, never
  admit unjudged. "Blocking is not losing" — a refused proposal is meant to be
  resolved-and-resubmitted, not dropped.
- **A cheap deterministic duplicate guard** still runs (today *after* the model;
  585 argues it should run *before*). On a duplicate it bumps the existing
  arrow's importance instead of adding a row — the anti-bloat reflex.

This much is **settled and built**, and it is the correct skeleton. The captured
controlling intent is decision `mrkv`: *"Spirit capture is a blocking gate not
an advisory check: the guardian must vet and admit a proposed record before
capture succeeds, so duplicates, contradictions, compounds, and non-intent are
resolved or refused at the door rather than admitted and cleaned up later."*

## 2. The two curated sets, and why there are two gates

Spirit holds **two** curated bodies, and your prompt named a gate for each:

| Set | What it is | The "new X" admission op | Gate today |
|---|---|---|---|
| **Records** | forward-intent arrows (the intents themselves) | `Propose Entry` | **LLM guardian** (built, Propose only) |
| **Referents** | the *which-one* facet — concrete named instances an intent governs, drawn from your private inventory (a repo, a project, a child, a marriage) | `RegisterReferent` | **mechanical synonym/name-collision check only** — bypasses the guardian entirely |

A **referent** is distinct from a **domain**: domain answers *about-what*
(universal, a compile-time enum), referent answers *which-one* (particular,
per-person runtime registry data, never an enum). Records may only cite
*registered* referents (an unregistered one is rejected on write), which is what
makes the referent set a curated vocabulary rather than free text — and therefore
something whose *enlargement* is itself an admission decision worth gating.

So "gating the acceptance of new records … and … gating the acceptance of new
referent" is, as I read it, **one guardian principle applied to two admission
surfaces**: the same daemon-is-the-gate / agent-is-the-brain / binary-typed-
verdict / fail-closed shape, instantiated once for records and once for
referents.

## 3. "Gating … the deletion and so on" — completing the reach

I read "the acceptance of new records **or the deletion and so on**" as: the gate
must cover **every write that changes the live arrow set**, in *both* directions
— not just admission. Today only `Propose` is gated; `Record`, `Clarify`,
`Supersede`, `Retire`, `Remove`, and `CollectRemovalCandidates` are **ungated
direct writes**. That is exactly the hole designer 585/581 and operator 355/357
independently flagged as the #1 weakness, and `Supersede` writing its
replacement *blind* (no recheck against the rest of the store) is the sharpest
edge — a side-door for precisely the inconsistency the guardian exists to stop.

What the guardian should *judge* on a deletion/lifecycle op is, I believe, two
different questions depending on the op (this is where I most want your
confirmation — see §6):

- **Supersede / clarify** — re-vet the *replacement* against the store (except
  the named target) so a change can't inject a contradiction. (the 578 rule)
- **Retire / remove / collect** — vet that the *removal is justified*: is this
  arrow genuinely contradicted/obsoleted by newer intent, or is something live
  being destroyed? This lines up with your captured deletion-lifecycle intent:
  `itn7` (zero-certainty review is **not** deletion; expose an explicit GC path),
  `4pd8` (contradicted intent must be retired), `3fnu`/`yu14` (deletion stays
  reviewable and justified by newer intent), `8g9n`/`ue6x` (hard deletion is a
  deliberate, archival-first, recoverable-to-a-horizon stage).

Net: the guardian becomes the admission authority for the record set's **whole
lifecycle**, not just its front door.

## 4. The new-referent gate — what it's for

Today `RegisterReferent` is **self-service and only mechanically gated**: a
verbatim name/alias collision is rejected (`ReferentNameConflict`); re-registering
a known name just merges aliases; anything else is admitted with no judgment, and
it never touches the guardian. The failure that lets through: a **near-duplicate
or synonymous referent** the string check misses (`spiritProject` vs registered
`spirit`), a typo'd spelling, or an off-topic / illegitimate entity — i.e.
**referent sprawl**, the "twenty spellings of spirit" problem.

Designer 584 §4 explicitly left this as an **open psyche decision**: grow the
referent registry *self-service, synonym-gated* **vs** put it behind *an
editorial-board gate the way domains are vetted*. I read your prompt as
**resolving that toward the gated option**: a new referent should pass an
LLM/semantic gate (catch synonyms/duplicates/off-topic the string check can't),
mirroring the record guardian. That gate needs its own typed verdict and
rejection vocabulary — the existing `GuardianRejectionReason` is record-scoped;
there is no referent-rejection type yet.

## 5. Settled vs gap vs my-inference

| Piece | Status |
|---|---|
| Guardian = blocking gate, not advisor; binary typed verdict; fail-closed; daemon-is-gate/agent-is-brain | **Settled** (intent `mrkv`/`l98v`; built for Propose) |
| Gate covers record `Propose` acceptance | **Settled + built** |
| Gate must also cover deletion/supersede/clarify/retire (complete reach, both directions) | **Gap you're now asking for** (already flagged by 585/581/355/357; intent for the deletion *side* exists in `itn7`/`4pd8`/`3fnu`/`yu14`) |
| Supersede must recheck its replacement | **Gap** (decided in 578; not built) |
| Second guardian gate on `RegisterReferent` (new referents) | **Gap you're now asking for**; resolves the open 584 §4 decision |
| Deletion-gate judges "is removal justified by newer intent" vs replacement-recheck | **My inference** — needs confirmation (§6) |
| Referent gate is full-LLM vs synonym-check-then-LLM hybrid | **My inference / open** (§6) |
| One unified guardian with two entry points vs two distinct gates | **My inference** — I assume shared mechanism, separate prompts+verdict types |

## 6. What I need you to confirm before the audit

1. **Deletion-gate semantics.** When the guardian gates a removal (`Retire` /
   `Remove` / `Collect`), is it judging *"is this deletion justified by newer
   intent / safe?"* (a legitimacy check) — while `Supersede`/`Clarify` get the
   *replacement-recheck* treatment? Or do you want one uniform judgment over all
   of them? This decides the verdict's question, the reason vocabulary, and the
   audit's yardstick.

2. **Referent-gate strength.** Full LLM judgment on **every** `RegisterReferent`,
   or **synonym-check-first, LLM only on the residue** (cheap exact/near match
   rejects deterministically; the model is the last resort)? 585's "layer it —
   model is the last resort" argument suggests the hybrid; 584 §4 framed it as
   self-service-vs-editorial-board. Which?

3. **One guardian or two?** Same `AgentGuardian` mechanism with a referent-specific
   prompt + a new referent verdict/rejection type, or a genuinely separate gate?
   ("there should *also* be a mechanism" reads to me as the same principle, second
   surface — confirm.)

4. **Privacy of referent names.** Referents are private particulars (a child's
   name, a therapist, a private project). A referent gate sends those names to the
   guardian agent. The deployed agent is **local** (`criomos-local` gemma), and
   `qoku` already rules hosted inference isn't a publication-leak — so I read this
   as acceptable, but I want to confirm it isn't a line you'd draw.

## 7. The production-vs-code skew (you flagged it)

Worth holding through the audit: the **deployed daemon (v0.8.0) has no referent
registry at all** — it rejects `RegisterReferent` as an unknown input and rejects
the 8-field query. The referent registry + domain enum exist only at code HEAD
(commit `fbf031a`, "add domain enum and referent registry"), not yet live; the
bundled CLI is already ahead of the daemon. So the new-referent gate would land on
top of code that *itself* isn't deployed yet — which is consistent with the
system-operator "getting everything in order before we update." The audit should
state, for every claim, whether it's about the **running daemon** or **HEAD code**.
