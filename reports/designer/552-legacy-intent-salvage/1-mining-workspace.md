---
title: 552/1 — Legacy intent salvage — mining workspace.nota
role: designer
variant: Audit
topics: [intent, spirit, legacy-nota, agglomeration, deletion-readiness, workspace]
description: |
  Mining report for the legacy intent/workspace.nota substrate (79 records,
  date-stripped text at /tmp/intent-text/workspace.txt). Propose-only salvage
  audit: surfaces the few core, durable, not-too-specific design ideas that
  would be LOST on deletion because they are not already in deployed Spirit or
  the guidance layer. Most of the 79 records are already preserved.
---

# 552/1 — Legacy intent salvage — mining workspace.nota

Scope: `intent/workspace.nota`, 79 records scanned (text-only extraction at
`/tmp/intent-text/workspace.txt`). Five genuine salvage candidates surfaced;
the other 74 records are already preserved in deployed Spirit or the guidance
layer (ESSENCE / AGENTS / INTENT / skills), or are too specific / transient to
salvage.

## Salvage candidates

### 1. Anything that can be done mechanically will not be done by agents

- **Kind:** Principle
- **Proposed topics:** `[mechanism agents design-methodology workspace cognitive-layer]`
- **Proposed description:** Anything that can be done mechanically — anything
  with a deterministic correct answer derivable from the input (socket
  routing, format selection, lookup, address resolution, dispatch) — is
  mechanism, not agent work. Agents are the cognitive layer; mechanism handles
  every decision code can make. The trajectory: more agents doing more
  substantive work, but less mechanical work per agent as the system matures.
- **Proposed certainty:** High (stated Maximum in the legacy record with
  founding-rule force and flagged an ESSENCE-promotion candidate; held at High
  pending psyche confirmation per the don't-default-to-Maximum discipline,
  Spirit `om3x`).
- **Supporting verbatim:** *"Anything that can be done mechanically will not be
  done by agents. Agents are going to do less and less. … they're not going to
  have to figure all of this stuff out that can be done mechanically."*
- **Preservation evidence:** Spirit queried on `[mechanism agent design
  compatibility correctness]`, `[essence principle workspace agent-discipline
  mechanism]` — no record carries the mechanism-vs-cognition split. Keyword
  scan of `/tmp/spirit-current.txt` for `mechanically` / `cognitive layer` =
  0. `rg` across ESSENCE.md / AGENTS.md / INTENT.md / skills/ for `done
  mechanically` / `cognitive layer` / `deterministic correct answer` = 0.
  ESSENCE's "intent clear enough to create signal becomes action" is adjacent
  but is about intent-to-action, not the mechanism-vs-agent labour boundary.
- **At-risk rationale:** A foundational architectural principle that explains
  WHY the workspace pushes routing / dispatch / lookup into schema-derived
  mechanism and reserves agents for cognition. Stated once, with force, only in
  this legacy file; nothing downstream restates it. Deleting workspace.nota
  erases the only record of it.

### 2. Let the logic find its own path — desire paths

- **Kind:** Principle
- **Proposed topics:** `[design-methodology architecture convergence beauty workspace]`
- **Proposed description:** When the existing shape doesn't fit, follow where
  the logic wants to go — don't be bound by what's already there; let the water
  find where it wants to go downhill. Desire paths name this: the trail walked
  into the grass because it's how the body naturally moves, regardless of where
  the paved walkway was put. Architecture grows the same way; where multiple
  agents independently arrive at the same shape, that's the right shape.
- **Proposed certainty:** High (Maximum in the legacy record and flagged an
  ESSENCE-promotion candidate; held at High pending psyche per `om3x`).
- **Supporting verbatim:** *"let's not be bound by the code that was already
  existed. And let's see where the water wants to go downhill. Desire paths,
  they call it."*
- **Preservation evidence:** Spirit queried on design/correctness/architecture
  vectors; `/tmp/spirit-current.txt` scan for `desire path` / `downhill` = 0.
  `rg` across the full guidance tree for `desire path` / `water.*downhill` = 0.
  ESSENCE §"Backward compatibility is not a constraint" carries the
  break-for-beauty stance but not the positive desire-path / convergence
  framing (let the logic carve its own path; independent convergence = right
  shape).
- **At-risk rationale:** A memorable, generative framing for how architecture
  should grow — the kind of "Tao Te Ching"-shaped line the psyche explicitly
  wants captured (workspace.nota record 5). It survives nowhere else; the
  convergence-as-correctness-signal idea in particular has no other home.

### 3. Disregard implementation cost; the better long-term logic wins

- **Kind:** Principle
- **Proposed topics:** `[design-methodology decision-vs-lean architecture compatibility design-rigor]`
- **Proposed description:** When choosing between design alternatives, the
  better long-term logic always wins; implementation cost is never a
  tiebreaker. The cost of a wrong shape compounds; the cost of a clean break is
  paid once. Weigh elegance, separation of concerns, and clarity — not how
  easy or hard the change is to land. A transitional shape that compromises
  both old and new to avoid breaking either is the wrong shape for both.
- **Proposed certainty:** High (Maximum in the legacy record; held at High per
  `om3x` — it sharpens an existing ESSENCE stance rather than founding a new
  one).
- **Supporting verbatim:** *"disregard implementation cost completely; the
  better long-term logic always wins"*
- **Preservation evidence:** Spirit queried on `[design correctness
  decision-vs-lean architecture design-rigor]` and the compatibility vector —
  no record states the implementation-cost-is-not-a-tiebreaker rule. Scan of
  `/tmp/spirit-current.txt` for `implementation cost` / `long-term logic` = 0.
  `rg` guidance tree = 0. ESSENCE §"What I am not optimising for" has "the
  right shape now is worth more than a wrong shape sooner" (a time/speed
  tradeoff) and §"Backward compatibility is not a constraint", but neither
  states the design-ALTERNATIVE evaluation rule: when comparing two shapes,
  effort-to-implement is excluded from the comparison. NOTE: a weaker, partial
  version exists at `skills/context-maintenance.md:112` ("is the tiebreaker")
  but in a different context. This is the sharp, general form.
- **At-risk rationale:** Agents repeatedly let "but that would need a big
  change" creep into design analysis; this record is the explicit retirement of
  implementation-cost as a tiebreaker. The closest preserved ideas are about
  speed/compatibility, not effort-as-tiebreaker; the distinct rule is lost on
  deletion.

### 4. Inelegant code is not "this works"; inelegant tests do not prove "broken"

- **Kind:** Constraint
- **Proposed topics:** `[beauty verification correctness testing proving-not-pretending]`
- **Proposed description:** Inelegant code does not qualify as "this works,"
  and inelegant tests do not prove something is broken. Elegance is the
  criterion both for whether verification work is done and for whether a
  falsification result is load-bearing: passing tests over ugly code do not
  finish the work, and a failing inelegant test does not establish that the
  code under test is actually broken — the inelegance may be in the test.
- **Proposed certainty:** Medium (legacy record marked Maximum, but it is a
  narrower verification corollary of the already-Maximum beauty principle; held
  at Medium per `om3x`).
- **Supporting verbatim:** *"inelegant code does not qualify as 'this works'
  and inelegant tests does not prove that something is necessarily broken"*
- **Preservation evidence:** `rg` for `inelegant` across ESSENCE.md /
  AGENTS.md / INTENT.md / skills/*.md = 0 (checked beauty.md and the testing /
  architectural-truth-tests skills specifically). Spirit queried on
  `[verification proving-not-pretending correctness testing beauty]` — records
  exist on proving-not-pretending and beauty-as-gate (`61ei`, `vcin`, `wyte`)
  but none state the elegance-as-verification-criterion corollary in either
  direction (ugly-passing ≠ done; ugly-failing ≠ broken). ESSENCE §"Beauty is
  the criterion" says ugliness signals an unsolved problem, but does not apply
  that to test/verification load-bearingness.
- **At-risk rationale:** A precise discipline for reading verification results
  through the beauty lens — distinct from "beauty is the criterion" because it
  governs how to interpret test PASS/FAIL signals, not how to judge a design.
  It guided a real retraction (three of four claimed engine gaps were
  route-aroundable; only the inelegant escape hatch confirmed a real gap). No
  surviving record carries it.

### 5. Agent failure is signal, not fault — fix the guidelines

- **Kind:** Principle
- **Proposed topics:** `[agent-discipline guidance workspace agent-behavior correction]`
- **Proposed description:** An agent is a machine; it does not misbehave and
  there is no such thing as a "violation." An agent's output is a function of
  its context and prompt — when an output looks wrong, the question is which
  part of context produced it, not which rule was broken. Every agent failure
  is therefore signal that the guidance is insufficient; the fix is to upgrade
  the guidelines so they absorb the failure mode, never to blame the agent.
- **Proposed certainty:** High (two reinforcing Maximum legacy records, 55 and
  76; held at High per `om3x` — durable framing rather than a single founding
  rule).
- **Supporting verbatim:** *"There's no such thing as you misbehaving, you're
  just a machine. So we need to upgrade the guidelines"* and *"there's no such
  thing as a 'violation' — your output was the result of your context and
  prompt. so which part made you do that?"*
- **Preservation evidence:** Spirit queried on `[agent-discipline guidance
  correction agent-behavior agent-errors]` — `ui5d` (do-it-properly) and
  `0sef` (keep-working) are adjacent but neither states the
  failure-is-signal / output-is-a-function-of-context framing. Scan of
  `/tmp/spirit-current.txt` for `no such thing as` / `misbehav` / `upgrade the
  guideline` = 0. `rg` across guidance tree for `misbehav` / `no such thing` /
  `function of.*context` / `failure.*signal` = 0.
- **At-risk rationale:** The load-bearing meta-principle behind how the whole
  guidance layer iterates — it reframes every agent error as a guidance gap to
  close. It is the rationale the psyche restates repeatedly in practice ("agents
  keep breaking this rule, so the rule must be made prominent") but is never
  itself written down as a principle anywhere downstream. Lost on deletion.

## Already preserved / dropped

The remaining 74 records are safe to delete because their core is already
preserved, or they are too specific / transient to salvage. Grouped summary:

### Intent-layer founding rules — all preserved in ESSENCE / INTENT / skills
Intent is primordial / cornerstone (rec 3) → ESSENCE §"Intent is the
cornerstone". Psyche is the human; intent is the only source (rec 9) → ESSENCE
+ AGENTS hard overrides. Ask when unclear, don't infer (rec 10) → ESSENCE
§"Inferring intent is forbidden". Intent layer outranks all surfaces (rec 12) →
ESSENCE. ESSENCE is gold-of-the-gold / force+universality bar (recs 4, 5) →
ESSENCE preamble. Per-repo INTENT.md (recs 6, 11) → ESSENCE + AGENTS + Spirit
`nqsb`/`jymr`. Guidance-files vocabulary (rec 39) → INTENT.md §"Guidance files"
+ skills/intent-manifestation.md. Intent-manifestation skill (rec 41) →
skills/intent-manifestation.md. Three-surfaces vocabulary log/file/essence
(rec 42), italics verbatim convention (recs 43, 44, 45) →
skills/intent-manifestation.md + repo-intent.md. Workspace INTENT.md replaces
ONBOARDING (rec 47) → done (INTENT.md exists; no ONBOARDING.md).

### Intent-capture discipline — all preserved in ESSENCE / skills + Spirit
Golden rule: log intent first on a psyche prompt (recs 16, 49) → ESSENCE
§"Logging psyche intent is the first action". Classify-whether-intent-present
first (rec 50) → same ESSENCE section. Conservative / understate / never
overextend (rec 72) → ESSENCE + Spirit `xtk9`, `rvnf`. Inferring is the worst
offense (rec 74) → ESSENCE §"Inferring intent is forbidden". Short prompts =
go-ahead not blanket agreement (rec 73) → ESSENCE §"Inferring intent is
forbidden". Work instructions are not intent (recs 71) → ESSENCE + Spirit
`7hrd`, `7nbu` placement, plus the future-session test. Record everything that
IS intent (rec 52), intent-mining-is-gold-ore-refinement / not-an-archive
(rec 75) → ESSENCE §"Logging psyche intent is the first action" + Spirit
`cuia`. Record from live prompts not compacted history (rec 21) → covered by
the same conservative-capture discipline. Don't blindly duplicate restatements
(recs 29, 32) → superseded by Spirit's record-everything + downstream
agglomeration (`om3x`, `3fnu`, intent-maintenance skill). STT correction table
(recs 23, 34) → skills/stt-interpreter.md + Spirit `7s0j`. Lock-free / Write-OK
append mechanics (recs 18, 19, 20, 22, 51) → obsolete: Spirit daemon replaced
the file-append substrate entirely. Timestamp format (recs 28, 31) → obsolete:
Spirit stamps records itself. Topics broad-not-narrow (rec 14) → Spirit `bh0p`
+ skills/intent-log.md topic discipline.

### Reporting / chat discipline — all preserved
No long chat responses, substance in reports (recs 53, 64) → AGENTS.md
§"Reports go in files" + Spirit `1kfk`, `7u3j`, `k24p`. No `---` / no
labeled-field scaffolding in chat (rec 30) → AGENTS.md hard overrides + chat
policy. Self-contained questions, no vague back-references (rec 54) →
skills/reporting.md + intent-clarification.md + Spirit `sfy0`, `bqok`. Opaque
identifiers carry inline descriptions (rec 37) → AGENTS.md hard overrides +
Spirit `o7zt`. Aggressive report sweep / retain only load-bearing (rec 26) →
skills/reporting.md hygiene + Spirit `0r17`, `3k0j`, `vqfk`. Beads not
psyche-friendly, reference from reports (rec 57) → Spirit `o7zt` +
beads/reporting skills. Positive-over-negative skill framing (rec 79) →
Medium-certainty, narrow stylistic note already embodied across skill files;
not worth a standalone Spirit record (judged too-minor rather than at-risk).

### Roles / lanes / beads / nix — all preserved
AGENTS.md ~100-line soft target / no hard caps / required-reading stays
role-local (recs 1, 2) → AGENTS.md structure embodies it; skill-editor.md.
Skills must not grow noisy (rec 13) → INTENT.md §"Skills must not grow noisy".
Beads carry no role label, any agent picks up any bead (rec 38) → Spirit
`dash`, `7i7i`, `3b26` + role-lanes model. Concept-designer-is-a-real-role
(rec 25) → superseded: the designer/operator dance + concept-branch handoff
(`j028`, `rlyn`) is the live model; concept-designer-as-distinct-lane never
materialised and is not current intent. Designer-implements-first-in-design-
phase (rec 24) → superseded by the full designer/operator model (`l5u3`,
`4wyw`, prototype-driven development `trvl`, `6b55`). Designer-pass is
meaningless vocabulary (rec 58) → embodied in role-lanes (all agents same
models, lane = discipline+locus). second-operator lane correction (rec 78) →
transient lane-assignment note, not durable. `--max-jobs 0` remote builder
(recs 61, 62, 63) → skills/nix-usage.md (full coverage). Recent intent
overrides old / file-approach limits motivate Spirit (rec 56) → realised:
Spirit daemon exists; supersession is Spirit's job (`3fnu`,
intent-maintenance.md).

### Too-specific / transient task state — dropped, not intent
Repository-ledger slices, Gitolite hook path, ouranos local deploy, spool
consumer, query surface (recs 24, 27, 33, 35, 36, 40, 46) — project-specific
task choreography and transient readiness language; the durable cores within
them (e.g. "no-open-clarification ≠ ready-to-use", recs 35/36) are agent-
completion-discipline already covered by the keep-working / do-it-properly
records (`0sef`, `ui5d`). Signal-frame / signal-executor migration targets
(recs 60, 65, 66, 67, 68, 70) — specific report-driven migration decisions,
now landed or superseded by the schema-derived stack; `psyche`-verbatim
placeholders carry no durable general principle. Repository-ledger
discovery-query schema (rec 46) — specific feature, too specific to salvage as
general intent.
