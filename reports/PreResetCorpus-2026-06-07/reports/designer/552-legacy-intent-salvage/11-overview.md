---
title: 552/11 — Legacy intent salvage — synthesis overview
role: designer
variant: Audit
date: 2026-06-07
topics: [intent, spirit, intent-maintenance, legacy-nota, agglomeration, deletion-readiness, salvage]
description: |
  Synthesis of the ten-finder legacy intent/*.nota salvage audit. Cross-dedupes
  the finders' candidates, re-applies the salvage bar hard, and produces a
  curated PSYCHE-GATED shortlist of Spirit records to consider adding before the
  16 legacy files are deleted. Propose-only: no spirit (Record ...) was run.
---

# 552/11 — Legacy intent salvage — synthesis overview

## Result

364 legacy records were scanned across the 16 `intent/*.nota` files by ten
finders. **334 records were judged already-preserved (in deployed Spirit, in
ESSENCE / AGENTS / INTENT / per-repo INTENT, or in `skills/`) or too-specific /
transient to salvage.** The finders proposed 30 distinct at-risk candidates.
After cross-dedupe (two pairs of finders surfaced the same idea from different
files) and a hard re-application of the bar, this synthesis recommends a
**shortlist of 8 records** for the main list, with 9 more parked in a
"borderline — your call" section the psyche can pull from. Everything below is
PSYCHE-GATED: the psyche picks which (if any) to record; only `spirit (Observe
...)` was run during synthesis.

The psyche asked for "a few things… not a massive import." 8 is the honest
"few" — each is a durable, general design principle with no surviving home. The
borderline set is offered so nothing is silently dropped, not as a second tier
to also import.

## Cross-dedupe notes

Two ideas were independently surfaced by two finders each and are merged here
into one record, citing both source files:

- **Mechanism-not-agents** — `workspace.nota` record 77 (finder 1) AND
  `signal.txt` (finder 9, the CLI socket-dispatch rejection). Same principle,
  two angles (the general labour-split, and the concrete "don't make the agent
  pick the socket" application). Merged as shortlist #1, the strongest of the
  whole audit.
- **Beauty budget to the durable layer / Nix is throwaway** — `horizon.nota`
  record 9 (finder 5) AND `nix.nota` record 3 (finder 10). The horizon finder
  framed it as the layering tradeoff; the nix finder framed it as the
  design-posture ("design as if Nix gets replaced") and additionally found
  `skills/nix-discipline.md` actively frames Nix as *permanent* — so the idea is
  not merely missing but partly contradicted. Merged as shortlist #5.

One cross-finder DISAGREEMENT was resolved against salvage: "disregard
implementation cost; better long-term logic wins" (`workspace.nota` rec 69,
finder 1 flagged at-risk; `reports.nota` rec 20, finder 6 judged preserved).
Spot-verified against `ESSENCE.md` §"What I am not optimising for" (lines
209-220): it carries "the right shape now is worth more than a wrong shape
sooner," "implementation timelines do not appear in design discussions," and
"work is described by what it requires, not how long it will take." The
design-vs-speed/timeline axis is robustly preserved; finder 1's distinct sliver
(effort-as-tiebreaker between two *alternatives*) sits on top of well-preserved
material. Down-ranked to borderline.

## Recommended salvage shortlist

Eight records, grouped by theme. Each carries a one-line rationale, the legacy
verbatim, and a ready-to-run command. The `[description]` in each command is the
GENERAL core idea, not the specific instance that produced it.

### Theme A — Agent-vs-mechanism labour boundary

#### A1. Anything that can be done mechanically is not done by agents

The single strongest salvage of the audit: the foundational rationale for the
whole schema-derivation / macro-emission thrust AND for the small-model auditor
— let machinery do what is derivable, reserve agents for cognition. Stated with
founding force in two legacy files; nowhere in the durable layer (the `rg` hits
for "mechanical" are all descriptive, never the categorical principle).
Verbatim: *"There's no way we're going to make the agents responsible for
figuring out which socket goes where. That's a mechanical thing. Anything that
can be done mechanically will not be done by agents."* (signal.txt) and
*"Agents are going to do less and less… they're not going to have to figure all
of this stuff out that can be done mechanically."* (workspace.nota rec 77).
Source: `workspace.nota` rec 77 + `signal.txt`. PSYCHE-GATED:

    spirit "(Record ([mechanism agent-discipline cognitive-layer design-methodology routing] Principle [Anything with a deterministic correct answer derivable from its input — routing, dispatch, lookup, classification, projection, address resolution — is mechanism, not agent work, and must live in code or schema-derived machinery, never in agent judgment. Agents are the cognitive layer reserved for decisions code cannot make. The trajectory: more agents doing more substantive cognition, less mechanical work per agent as the system matures. This is the load-bearing why behind the schema-derivation/macro-emission thrust and the small-model auditor.] High Zero))"

### Theme B — How architecture is allowed to grow

#### B1. Let the logic find its own path — desire paths; independent convergence is the correctness signal

A memorable, generative framing for how architecture grows — the
Tao-Te-Ching-shaped line the psyche explicitly wanted captured. ESSENCE's
backward-compat stance carries the break-for-beauty negative, but not the
positive desire-path / convergence-as-correctness framing. Verbatim: *"let's
not be bound by the code that was already existed. And let's see where the water
wants to go downhill. Desire paths, they call it."* Source: `workspace.nota`
rec 59. PSYCHE-GATED:

    spirit "(Record ([design-methodology architecture convergence beauty] Principle [When the existing shape does not fit, follow where the logic wants to go rather than being bound by what is already there — let the water find where it wants to go downhill. Desire paths name this: the trail walked into the grass because that is how the body naturally moves, regardless of where the paved walkway was put. Architecture grows the same way, and where multiple agents independently arrive at the same shape, that convergence is the signal it is the right shape.] High Zero))"

### Theme C — The guidance layer iterates on agent output, not agent fault

#### C1. Agent failure is signal, not fault — fix the guidelines

The load-bearing meta-principle behind how the entire guidance layer iterates:
an agent is a machine, there is no "violation," output is a function of context
and prompt, so every failure is a guidance gap to close — never a thing to
blame. The psyche restates the consequence constantly in practice but the
principle is written nowhere. Verbatim: *"There's no such thing as you
misbehaving, you're just a machine… there's no such thing as a 'violation' —
your output was the result of your context and prompt. so which part made you do
that?"* Source: `workspace.nota` recs 55, 76. PSYCHE-GATED:

    spirit "(Record ([agent-discipline guidance correction agent-behavior] Principle [An agent is a machine; it does not misbehave and there is no such thing as a violation. An agents output is a function of its context and prompt — when an output looks wrong the question is which part of the context produced it, not which rule was broken. Every agent failure is therefore signal that the guidance is insufficient, and the fix is to upgrade the guidance so it absorbs the failure mode, never to blame the agent.] High Zero))"

### Theme D — Schema-shape design axes

#### D1. Additive vectors cannot express un-selection, so essence is categorical

A transferable schema-design axis well beyond the node-roles case that produced
it: additive feature/capability vectors only add (no natural way to un-select a
default), so the one-of-N essence of a thing must be a categorical label, not a
defaults-overridable vector. `typed-records-over-flags.md` covers boolean→variant
and mutually-exclusive sums but never this additive-cannot-unselect reasoning.
Verbatim: *"the feature vector doesn't let you turn stuff off. So if you have a
center node… center node has services x, y, z enabled and configured, and then
you can't turn those off."* Source: `horizon.nota` rec 23. PSYCHE-GATED:

    spirit "(Record ([schema typed-records variants categorical design-methodology] Principle [Separate a things categorical KIND (its one-of-N essence) from its additive CAPABILITY vector (the specific things it does). An additive vector only adds and has no natural way to express un-selection of a default, so the categorical essence cannot be modelled as pre-selected defaults overridden by features — it must be an explicit categorical choice with no implicit defaults, mutually-exclusive kinds validated at projection with a typed error. The general axis: additive vectors for things you turn on, categorical labels for the one-of-N essence that has no off.] High Zero))"

### Theme E — Spend cleanliness on the layer that outlives the others

#### E1. Beauty budget goes to the durable layer; the throwaway substrate absorbs the dirt

A sharp reusable tradeoff for WHERE unavoidable ugliness goes when two layers
have different lifespans: invest cleanliness in the layer that outlives the
others, let constants/glue live in the substrate slated for replacement. The
motivating case is Horizon (durable) over Nix (bootstrap, to be replaced by
Forge). Doubly at-risk: `skills/nix-discipline.md` currently frames Nix as
*permanent*, so the posture is partly contradicted, not just absent. Verbatim:
*"I would way rather make the horizon code more beautiful and keep some of this
dirty stuff like port numbers into the Nixcode… the Nixcode is something we
bootstrap on, but eventually move on from."* Source: `horizon.nota` rec 9 +
`nix.nota` rec 3. PSYCHE-GATED:

    spirit "(Record ([design-methodology layering aesthetic-gate nix horizon] Principle [When two layers have different lifespans — a durable reduction/projection layer over a substrate slated for eventual replacement — spend the cleanliness budget on the layer that outlives the others and let unavoidable operational ugliness (constants, derived names, glue) live in the throwaway substrate. Design as if the bootstrap layer gets replaced: choices that hinge on its permanence are wrong. The motivating case is a beautiful Horizon over beautiful Nix code, Nix being bootstrap infrastructure the future Forge replaces.] Medium Zero))"

### Theme F — Daemon privilege and identifier cost

#### F1. Daemon privilege envelope — privileged but not absolute; no ambient access to system private keys

A reusable daemon-security principle: a content/data daemon should be fairly
privileged (nothing dangerous about ingesting and serving content) but NOT
absolutely privileged — its boundary is "can ingest and serve content," not
"can read anything on the system," and it must have no ambient access to system
private-key material. The write-authority half is in `arca/ARCHITECTURE.md`; the
read-side privilege boundary lives only here. Verbatim: *"It shouldn't be able
to read private keys… not like system private keys, like the system SSH key… So
it should not be an absolute privileged daemon."* Source: `arca.nota` rec 5.
PSYCHE-GATED:

    spirit "(Record ([daemon privilege security boundary component-shape] Principle [A content/data daemon should be fairly privileged — there is nothing especially dangerous about ingesting and serving content — but never absolutely privileged. Its privilege boundary is can-ingest-and-serve-content, not can-read-anything-on-the-system: it must have no ambient access to system private-key material and, handed a path to a private key, must be unable to read it. Its store stays unwritable by anything except the daemon itself (root writing it would be system misbehavior).] High Zero))"

#### F2. Opaque/content-addressed identifiers are LLM-token-expensive; the shortest reliable identifier is a design target

The general rationale behind every short-identifier choice in the stack (arca
prefixes, bead UIDs, jj change-ids, Spirit base36 ids): hashes tokenize at ~one
token per character because they are not natural-language words, so they are a
recurring cost in agent context. The durable layer states the *human*
decodability angle (AGENTS.md inline-description rule); the LLM-token-cost driver
survives only in a GC-able report and this file. Verbatim: *"these file paths,
when they end up in… LLM context, they become extremely costly because hashes
are not recognizable tokens… they end up costing, like, a full byte per
character."* Source: `arca.nota` rec 6. PSYCHE-GATED:

    spirit "(Record ([identifier hash token-cost readability naming] Principle [Opaque content-addressed identifiers (blake3/sha hashes and similar) tokenize at roughly one token per character in LLM context because they are not natural-language words, so wherever they land in agent context, logs, references and reports they are a significant recurring cost. Identifier design must treat the shortest reliable identifier as a first-class target — short readable locators over full long hashes — balanced against collision risk: the full digest stays canonical identity, the exposed locator is a stable shortened form never renamed once exposed.] Medium Zero))"

### Theme G — Chat is action, not announcement

#### G1. Actions are taken, not announced — resolve "ready to X" into the action or a specific named question

A sharpened positive chat-discipline rule: workflow-completion phrasing ("ready
to close / merge / ship") must resolve to either DOING the action or asking a
specific named question — never left as empty status noise. The opaque-identifier
half of the original failure is already an AGENTS.md override; this
workflow-state half is preserved nowhere (the adjacent skills cover
process-narration and should-I-continue, not this). Verbatim: *"saying bead
primary HJ63 is ready to close doesn't fucking tell me anything… if it's
supposed to be closed, you should close it."* Source: `reports.nota`.
PSYCHE-GATED:

    spirit "(Record ([chat narration-vs-action agent-discipline human-facing] Correction [Actions are taken, not announced. When the agent would write ready to close / ready to merge / ready to ship or similar workflow-state phrasing in chat, it instead either does the action itself or asks a specific question naming the choice. Ready to X with neither action nor a clarifying question is empty noise — it leaves the psyche guessing whether the agent is reporting status, asking permission, or asking the psyche to do the action.] High Zero))"

## Borderline — your call

Close candidates cut from the main list to honour the "few" constraint. Each is
real and at-risk to some degree; pull any back in if it resonates. One line each:

- **Don't manufacture pseudo-gaps** (`reports.nota`) — Constraint: don't promote
  to an open question something the psyche already stated or clearly implied just
  because the wording was loose. Real gap in `intent-clarification.md` (it covers
  when-to-ask, not don't-fabricate-a-gap); cut only because it is narrower than
  the eight and adjacent to the well-preserved give-the-question-substance rule.
- **Mind says what-work; orchestrate decomposes how (programmable policy)**
  (`persona.nota`) — Principle, the richest single description in the audit, but
  it is mechanism design for an unbuilt component (orchestrate); the static
  state-vs-machinery split is already in `orchestrate/INTENT.md`. Strong
  borderline — promote if the psyche wants the orchestrate-design substance held.
- **Config is always a Mutate** (`component-shape.nota`) — Principle: daemon
  configuration is integral durable policy state, not an out-of-band knob. The
  socket-level rule (config via meta-signal) is in `cgd8`; only the deeper
  "config IS state" modeling reason is at risk.
- **Verbs are cheap — prefer many named verbs over one collapsing verb**
  (`component-shape.nota`) — Principle. `7l7l` settles vocabulary (domain verbs),
  not granularity. Recurring design call; cut as adjacent to the
  more-separation-is-better instinct.
- **Every accepted operation lowers to a NonEmpty named command** (`component-shape.nota`)
  — Principle: no silent no-op plans; every operation leaves a Sema-observable
  witness. Sharp invariant but narrow to the Nexus/Sema execution model.
- **Mind-orchestrate authority follows the mind-body autonomy analogy**
  (`component-shape.nota`) — Principle: Mind interrupts only at cognitive-judgment
  moments; Orchestrate runs its own machinery. The chain is preserved; this is
  the rationale for what flows across it. Medium certainty.
- **Disregard implementation cost; better long-term logic wins** (`workspace.nota`)
  — Principle. Substantially covered by ESSENCE §"What I am not optimising for"
  (resolved disagreement above); the thin distinct sliver is effort-as-tiebreaker
  between two alternatives. Pull in only if that sliver matters.
- **Inelegant code isn't "works"; inelegant tests don't prove "broken"**
  (`workspace.nota`) — Constraint: read PASS/FAIL through the beauty lens. A
  narrow verification corollary of the already-Maximum beauty principle.
- **Node deploys itself locally; criome holds deploy-auth; daemon holds believed
  topology** (`deploy.nota`, three Medium candidates) — the lojix-deploy
  design-direction "why" statements. Real and unpreserved, but Medium/future and
  mechanism-specific to one unbuilt component; hold for an orchestrate/lojix
  design pass rather than a standalone import now.
- **One notation = one meaning; audit the codec for special-case exceptions**
  (`nota.nota`) — Principle. The specific exception is preserved (curly-brace
  maps) and the small-grammar instinct is adjacent in `language-design.md`; only
  the audit posture is at risk. Marginal.
- **Future network daemon; interface names in cluster data are a temporary hack**
  (`horizon.nota`) — Clarification flagging a field-set as transitional. Useful
  guard against building on a surface marked for removal, but narrow.
- **Router reachability query** (`persona.nota`) — Principle: agents ask the
  router which agents they can reach. Narrowest of the persona-machinery
  candidates; the owner-channel/delivery side is fully in `router/INTENT.md`.

## Safe to delete

Once the psyche records the chosen shortlist, the 16 legacy `intent/*.nota`
files are safe to delete. The salvage audit's central finding: **the legacy
substrate's durable core is overwhelmingly already preserved** — 334 of 364
records live in the deployed Spirit store or the guidance layer. The areas are
fully or near-fully covered as follows. The NOTA-design arc (`nota.nota`,
`nota-mixed-enum-support.nota`) is the canonical source of `skills/nota-design.md`
+ `skills/language-design.md` and is manifested verbatim. The persona
architecture (`persona.nota`) is the single best-manifested area — promoted into
ESSENCE, INTENT, and the per-repo INTENT.md files for persona-spirit/mind/router/
orchestrate. Naming (`naming.nota`), reporting (`reports.nota`), the
component-triad shape (`component-shape.nota`), deploy safety (`deploy.nota`),
and the small files (`jj`, `markdown`, `intent-log`, `nix`'s max-jobs,
`signal`'s three-layer model, `spirit`'s query surface) are all live in AGENTS.md
hard overrides, `skills/`, or deployed Spirit. The only material genuinely at
risk is the small set of general design *principles* and design-direction *why*
statements surfaced above; with the shortlist recorded (psyche's choice) and the
borderline set consciously accepted-or-dropped, nothing load-bearing is lost on
deletion. Deletion remains a separate step AFTER the psyche confirms the salvage
set, per the frame's gate.
