# 7 — Audit: subagent delegation, precious early context, and no-double-explore

Lane: preciousMainContext · discipline Designer · 2026-06-24. Audits whether the instruction surface a NEW agent reads at session start tells it to (A) delegate non-trivial research to subagents, (B) preserve its early/main context, and (C) not double-explore the codebase while its subagents explore. Verified this session against the live Spirit store (`spirit "(Lookup 30cu)"` / `69fa` / `hu84` all returned `RecordFound`) and the verbatim text of `AGENTS.md`, `skills/session-lanes.md`, `skills/operator.md`, `skills/intent-alignment.md`, `skills/designer.md`, `skills/reporting.md`, and `skills/context-maintenance.md`, not just the digest. All eight gap claims survived refutation.

## The decisive split: intent layer vs. instruction-file text

There are TWO surfaces and they currently disagree.

1. The **live Spirit intent layer** — confirmed by `Lookup` this session — carries all three claims UNIVERSALLY:
   - `30cu` (Constraint/High, verbatim): "Getting into anything complex starts by dispatching at least one fresh-context subagent to explore and report back, as the standing default for **every workspace agent** — no per-keystroke psyche authorization needed for orientation work… The main thinking agent spends its turns reasoning over the distilled subagent response **rather than exploring the codebase itself**… **Sending helpers to make changes still asks the psyche.**" (Claims A + C, universal; change-MAKING dispatch still psyche-gated.)
   - `69fa` (Principle, verbatim): "The main thread is the most precious context: the early high-fidelity window (the psyche's mark, roughly the first one hundred thousand tokens) is reserved for the lead agent's deepest thinking and intent alignment. **To keep that window precious**, the lead takes its orientation… from a fresh-context subagent's distilled response **rather than spending the window exploring itself**." (Claims B + C.)
   - `hu84` (Decision/High, verbatim): "Subagent-by-default and parallel cross-audit are the **universal workspace protocol, not a designer-only exception**… This all-discipline default **replaces the old prime-designer-chair scoping**, in which the designer ran parallel workflows by default while operator, system, poet, and assistant lanes stayed gated." (Claim A, explicitly universal.)

2. The **AGENTS.md hard-override text** (the file a new agent actually reads) still carries the OPPOSITE default at `AGENTS.md:286-293`: "**Don't dispatch subagents unless the psyche asks — except the designer protocol**… Default for operator, system-operator, system-maintainer, poet, editor, assistant, counselor and their lanes: **do the work yourself**; the psyche authorizes dispatch per task. The prime designer is the exception — it runs parallel subagent workflows by default until reduced."

`AGENTS.md:233-238` says "intent is primordial… **The intent layer outranks every other surface**." So by the workspace's own precedence rule, the landed Spirit records WIN — but a new agent reading AGENTS.md never sees them, and AGENTS.md does not point to them. The instruction *text* a fresh agent loads still teaches the superseded designer-only default. The reconciling doc-edits are captured as pending work (weave items W5/W6, beads `primary-ptvb.5`/`.6`); W6 is explicitly blocked on a `ky10` reconcile (`6-handoff.md:70-73`).

## Verdicts

### CLAIM A (delegate non-trivial research to subagents)

Verdict: **split — instructed-universally in the live Spirit intent layer (`30cu`, `hu84`), but contradicted-by-default in the AGENTS.md instruction text and every discipline skill a new agent reads.**

- Instructed universally (intent layer): `30cu` "standing default for every workspace agent"; `hu84` "universal workspace protocol, not a designer-only exception." Scoped to research/orientation — `30cu` is explicit that "Sending helpers to **make changes** still asks the psyche," which matches Claim A precisely (research, not edits).
- Contradicted-by-default (instruction text): `AGENTS.md:289-291` "do the work yourself; the psyche authorizes dispatch per task." `skills/operator.md:64` "When the psyche explicitly authorizes operator subagents, dispatch them as background side work" — gated. `skills/intent-alignment.md:41` "dispatching subagents only when the psyche asked for delegation." `skills/designer.md:334` carries the dispatch patterns but scoped strictly to the designer ("the designer dispatches two parallel sub-agent waves").
- If a new agent reads only its discipline skill + AGENTS.md (the normal path), it is told the OLD designer-only/psyche-gated rule. The universal rule lives only in Spirit, which AGENTS.md does not surface at session start.

### CLAIM B (preserve / protect the early main context, keep it lean)

Verdict: **instructed-universally in the intent layer (`69fa`) and partially in `skills/session-lanes.md`; implied-not-stated elsewhere; absent from AGENTS.md as an explicit rule.**

- Intent layer: `69fa` "The main thread is the most precious context… reserved for the lead agent's deepest thinking… To keep that window precious, the lead takes its orientation… rather than spending the window exploring itself." This is the explicit preserve-the-window imperative — but only in Spirit.
- `skills/session-lanes.md:106-109` (Smart zone) is the strongest discipline-agnostic file statement a new agent reads: "The session's early high-fidelity window — the psyche's mark is the first ~100,000 tokens — is for the main agent's deepest thinking and intent alignment. Spend it on understanding the goal and settling the design, **not on mechanical work**." In-force, universal, read at session start.
- But it stops short of the imperative "keep it lean / protect it / do not burn it"; the next bullet (`session-lanes.md:110`) only says "**Once that window is spent**, the main agent launches a fleet" — fan-out is triggered by window-exhaustion, not by research-non-triviality. AGENTS.md never states a preserve-early-context rule — its non-blocking-dispatch rationale (`AGENTS.md:296`) is "keeping the main agent **available to the psyche**," a different concern (availability, not context budget).
- `6-handoff.md:84-89` makes preservation an explicit rule ("don't read broadly in your smart zone") but that is a lane report, not the instruction surface; the rule it quotes is the unwritten W5 skill.

### CLAIM C (do NOT self-explore in parallel while subagents explore — orchestrator synthesizes)

Verdict: **instructed-universally in the intent layer (`30cu`/`69fa` "rather than exploring the codebase itself") and stated as an explicit rule ONLY in lane report `6-handoff.md`; implied-not-stated in every skill file; absent from AGENTS.md; and actively cut against by several in-force skills.**

- Intent layer: `30cu` "reasoning over the distilled subagent response **rather than exploring the codebase itself**"; `69fa` "rather than spending the window exploring itself." Universal no-self-explore posture.
- The only place the anti-pattern is NAMED and FORBIDDEN verbatim is `6-handoff.md:84-89`, quoting the unwritten W5 skill: "run only the **minimal dispatch envelope**… then stop. **Do not read the repos, skills, reports, or weave the helper was sent to collect**… The helper owns the broad read; duplicating it defeats the dispatch."
- Every skill file only IMPLIES it via the orchestrator-frames-then-synthesizes division, and several files actively CUT AGAINST a strict rule: `reporting.md:257` lets the main agent own "optionally a slice or two"; `designer.md:83-85` mandates the designer "reads broadly… every active-repo `ARCHITECTURE.md`"; `operator.md:64` tells the main operator to "continue non-overlapping work" in parallel with its subagents; `context-maintenance.md:306` tells the orchestrator to "Deep-read stale candidates" itself. So the in-force skill text permits exactly the double-work the user wants forbidden.

## File-by-file status

Statuses: U = instructed-universally · D = instructed-designer-only · I = implied-not-stated · X = contradicted-by-default · — = absent/silent · NA = irrelevant

| File | A | B | C |
|---|---|---|---|
| `AGENTS.md` | D (X for non-designers) | I | I |
| `ESSENCE.md` | — | — | — |
| `INTENT.md` | — | I (weak) | — |
| `orchestrate/AGENTS.md` | — | — | — |
| `skills/session-lanes.md` | I (window-exhaustion trigger, not research) | U (partial) | I |
| `skills/autonomous-agent.md` | — (defers to human-interaction) | I | — |
| `skills/designer.md` | D | D | I (cut against by "reads broadly") |
| `skills/human-interaction.md` | — | — | — |
| `skills/context-maintenance.md` | I (sweep-scoped) | I | I (sweep-scoped, self-reads too) |
| `skills/context-maintenance-deep.md` | I (sweep-scoped) | — | I |
| `skills/reporting.md` | — | I | I (permits "a slice or two") |
| `skills/intent-alignment.md` | X (psyche-gated) | — | — |
| `skills/operator.md` | X (psyche-gated) | I | X (parallel main work) |
| `skills/feature-development.md` | — | — | — |
| `skills/report-naming.md` | — | — | — |
| `skills/keep-working.md` | NA | NA | NA |
| `skills/push-not-pull.md` | NA | NA | NA |
| `skills/skills.nota` | X (discipline-indexed do-it-yourself) | I | — |
| Live Spirit `30cu` | U | — | U |
| Live Spirit `69fa` | — | U | U |
| Live Spirit `hu84` | U | — | — |
| `reports/.../1-bearings.md` | D + flags the universal direction as pending | I | I |
| `reports/.../2-skill-digest.md` | X/— | I | — |
| `reports/.../3-capture-drafts.md` | U (drafts; landed coda) | U | U |
| `reports/.../4-weave.md` | I (W5 future skill) | I | I |
| `reports/.../5-human-interaction-cut.md` | X (strips dispatch from skill) | — | — |
| `reports/.../6-handoff.md` | U | U | U (names + forbids anti-pattern) |

## Gap claims — all eight survived refutation

Every gap below was put through a refutation pass that searched for instruction text that would fill it. None was refuted; each is confirmed by verbatim quote.

- **G1 (high) — confirmed.** `AGENTS.md:286-293` still instructs the OPPOSITE of Claim A for all non-designer disciplines ("do the work yourself; the psyche authorizes dispatch per task") and was NOT updated after `30cu`/`hu84` landed. Refutation found no superseding edit in the file. A new agent reading AGENTS.md is told the old designer-only/psyche-gated default.
- **G2 (high) — confirmed.** No skill file or AGENTS.md states Claim A as a universal in-force rule. The refutation pass surfaced only the contradicting `AGENTS.md:286-293`, not a filling statement. The universal version exists ONLY in the live Spirit store (`30cu`, `hu84`), which AGENTS.md neither surfaces nor links at session start.
- **G3 (high) — confirmed.** The no-double-exploration rule of Claim C is NAMED and FORBIDDEN only in lane report `6-handoff.md:84-89` (the unwritten W5 skill) and is absent from the entire instruction surface a new agent reads (AGENTS.md, ESSENCE.md, INTENT.md, all skill files). No fill found.
- **G4 (high) — confirmed verbatim.** Several in-force skill files actively PERMIT or endorse the parallel self-exploration that produces the anti-pattern: `skills/operator.md:64` "continue non-overlapping work" while subagents run; `skills/reporting.md:257` main agent may own "optionally a slice or two"; `skills/designer.md:83-85` "reads broadly… every active-repo `ARCHITECTURE.md`"; `skills/context-maintenance.md:306` "Deep-read stale candidates… yourself." All four quotes verified this session.
- **G5 (medium) — confirmed.** Claim B is stated as an explicit imperative nowhere in AGENTS.md; the closest in-force file statement (`skills/session-lanes.md:106-110`) says spend the early window on thinking then fan out *once it is spent*, and does not phrase a "keep it lean / do not burn it / protect it" rule. AGENTS.md's non-blocking-dispatch rationale (`AGENTS.md:296`) is psyche-availability, not context preservation.
- **G6 (medium) — confirmed.** The reconciling doc work is captured but unbuilt: W5 (write the helpers skill, bead `primary-ptvb.5`) is unwritten, and W6 (shrink/rewrite AGENTS.md, bead `primary-ptvb.6`) is BLOCKED on a `ky10` reconcile (`6-handoff.md:70-73,119`). The instruction-surface text remains mis-aligned with landed intent until both land. Corroborated: no `skills/*helper*` file exists and AGENTS.md is still long/un-shrunk.
- **G7 (medium) — confirmed verbatim.** `skills/intent-alignment.md:41` directly contradicts universal Claim A by gating dispatch on "dispatching subagents only when the psyche asked for delegation," echoing the superseded `2o3g` default rather than the landed `30cu` orientation-default-on rule.
- **G8 (low) — confirmed; this is a scoping guardrail, not a defect.** Claim A as landed is scoped to research/orientation only — `30cu` ("Sending helpers to make changes still asks the psyche") and `6-handoff.md:47` are explicit — so the universal default does NOT cover change-making/implementation dispatch. Any recommendation that universalizes ALL dispatch would overreach the captured intent; the recommendations below respect this boundary.

## Tension: who the rule currently binds, and the gap

The `AGENTS.md:286-293` hard override **"do the work yourself unless the psyche asks (except the prime designer)"** currently binds, as written text, every non-designer discipline: operator, system-operator, system-maintainer, poet, editor, assistant, counselor. Their own skill files reinforce it (`operator.md:64`, `intent-alignment.md:41`). The prime designer alone is told to dispatch parallel workflows by default (`designer.md:334`).

The user's expectation — agents delegate non-trivial research to preserve context — is now **landed psyche intent** (`30cu`, `hu84`, `69fa`), and by AGENTS.md's own "intent layer outranks every other surface" rule it supersedes the hard override for ALL disciplines. The gap is purely **doc-lag**:

1. AGENTS.md still prints the old designer-only default and does not mention or link the new records.
2. No skill file carries the universal "delegate research / protect smart zone / don't double-explore" rule; the closest (`session-lanes.md` smart-zone) stops at "spend the early window well, then fan out once it is spent" and is not phrased as the user's three rules.
3. The reconciling work is captured but unbuilt: W5 (write the helpers skill, bead `primary-ptvb.5`, the dispatch-rule centerpiece) is ready; W6 (shrink AGENTS.md to a thin spine, bead `primary-ptvb.6`) is BLOCKED on the `ky10` reconcile. So a fresh agent reading the canonical files is mis-instructed until W5/W6 land.

Net: the rule is **authoritative in intent, contradicted in the text a new agent reads.** A diligent new agent that follows AGENTS.md literally will do the OPPOSITE of what the psyche has now decided — for research dispatch and for protecting the smart zone.

## Is the anti-pattern named and forbidden in the surface?

The user's failure mode — an agent burning its early smart zone self-exploring the codebase WHILE its subagents explore the same thing — is **named exactly once and forbidden exactly once, both in a lane report, not in the instruction surface.**

- Named: `6-handoff.md:77-80` cites the post-mortem `reports/schema-help-daemon-pilot-operator/1-skill-change-handoff.md` — "an operator dispatched a context helper, then spent its own smart zone redoing the helper's exploration, and the psyche never got a turn." That is precisely the double-exploration anti-pattern, and it happened to a non-designer (operator) lane — confirming the AGENTS.md default actively enabled it.
- Forbidden: the W5 dispatch rule, quoted in `6-handoff.md:84-89` and restated in `4-weave.md` W5 ("parent runs only the envelope, never duplicates the helper's exploration").

But this rule lives in a report and an unwritten bead. **NOTHING in the instruction surface a new agent loads (AGENTS.md, ESSENCE.md, INTENT.md, the skill files) names or forbids this anti-pattern.** Worse, several in-force skill files affirmatively permit the parallel self-work that produces it (`operator.md:64`, `reporting.md:257`, `designer.md:83-85`, `context-maintenance.md:306`). So the surface does not just fail to forbid double-exploration — in spots it endorses it.

## Recommendations: ready-to-paste instruction edits

The substance is already designed (W5) and the intent is already landed (`30cu`/`69fa`/`hu84`). The fix is to write the captured intent into the surface a new agent reads. Concrete placements, in workspace hard-override style.

### 1. Replace the AGENTS.md dispatch hard override (lines 286-293) — weave item W6, bead `primary-ptvb.6`

Replace the existing "Don't dispatch subagents unless the psyche asks — except the designer protocol" bullet with:

> - **Delegate the broad read; the main thread is the most precious context.** Getting into anything complex starts by dispatching at least one fresh-context subagent to read/explore and report back — the standing default for every discipline, no per-task psyche authorization for orientation work. The trigger fires whenever you are early in context and would otherwise read more than a few short already-known files, or whenever figuring something out needs multi-level exploration. The lead reasons over the helper's distilled response (including the file-section pointers it surfaces) rather than reading the repos itself; effort scales (simple = one helper at medium, complex = high/xhigh). **Sending helpers to make changes still asks the psyche** — this default is orientation/research only. Supersedes the old designer-only carve-out (Spirit `30cu`, `hu84`).

This lands in the same pass as the `ky10` reconcile that W6 already depends on (`6-handoff.md:70-73`).

### 2. Add a paired preserve-early-context + no-double-explore hard override to AGENTS.md

From `69fa` and the W5 rule (fold into the bullet above or add adjacent):

> - **Protect the smart zone; never double-explore.** The early high-fidelity window (~first 100k tokens) is reserved for the lead's deepest thinking and intent alignment. When you dispatch a helper to gather context, run only the minimal dispatch envelope — the Spirit gate, lane/report setup, and the helper's brief — then stop. **Do not read the repos, skills, reports, or weave the helper was sent to collect.** Wait for its report or do genuinely unrelated work; duplicating the helper's read defeats the dispatch and burns the precious window (Spirit `69fa`).

### 3. Write the W5 helpers skill (bead `primary-ptvb.5`, "ready") with the minimal-dispatch-envelope rule as its centerpiece

Use the verbatim rule drafted at `6-handoff.md:84-89`. Index it in `skills/skills.nota` so a dispatcher selects it by name+description. AGENTS.md carries only the one-line spine + pointer; this skill is the home for the detail, including the named anti-pattern (recommendation 6).

### 4. Sharpen `skills/session-lanes.md:106-114` (smart zone / fleet) so the trigger is research-non-triviality, not just window-exhaustion

Current text fans out only "Once that window is spent." Update the Fleet bullet so the `30cu` trigger fires earlier:

> **Fleet.** Dispatch fresh-context helpers to explore as soon as a task needs more than a few already-known files or any multi-level chase — don't wait for the window to be spent. The lead reasons over the helpers' distilled responses rather than reading broadly itself; the smart zone is for thinking and intent alignment, not for exploration the helper owns.

### 5. Reconcile the contradicting skills so they stop endorsing double-exploration

`skills/operator.md:64` ("continue non-overlapping work"), `skills/reporting.md:257` ("optionally a slice or two"), and `skills/intent-alignment.md:41` ("dispatching subagents only when the psyche asked") each need a one-line carve deferring to the new universal `30cu` orientation-dispatch default for the read/explore case, keeping their gating only for change-making dispatch. Without this, the discipline skills keep contradicting the AGENTS.md spine. Suggested carve to append to each:

> For reading/exploring early in context, the universal orientation-dispatch default (Spirit `30cu`, AGENTS.md) applies: send a helper and reason over its report rather than reading broadly yourself. The psyche-gate here governs change-making dispatch only.

### 6. Name the anti-pattern explicitly in the W5 skill (or `human-interaction.md`)

Add the schema-help post-mortem as the worked example, so the specific "dispatched a helper then redid its exploration and the psyche never got a turn" failure is an explicit don't, cross-referenced to `reports/schema-help-daemon-pilot-operator/1-skill-change-handoff.md`.

Already covered by this lane's reports — reference, don't re-derive: `1-bearings.md` (the designer-only-vs-universal fork and the in-force contract), `3-capture-drafts.md` (the exact NOTA and what landed: `30cu`/`69fa`/`hu84`), `6-handoff.md:75-93` (the verbatim W5 dispatch rule and the named anti-pattern), `4-weave.md` (W5/W6 beads under epic `primary-ptvb`). The audit's recommendation reduces to: execute W5 and unblock+execute W6, because the design and intent are done and only the instruction-surface text lags.
