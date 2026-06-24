# Capture drafts — preciousMainContext

*Drafter role: Spirit capture-DRAFTER. NOTHING was written to Spirit. Every
command below is a draft for the main agent to review with the psyche, then
fire. All lookups/searches this session were read-only (`Lookup`,
`PublicTextSearch`).*

This report turns the psyche's settled direction this session into exact NOTA
commands. Each section gives the existing record's **current verbatim
description**, the **draft command**, the **field choices and why**, and the
**psyche-only decisions** that must be settled before firing.

## Verbatim psyche statements this session (testimony source)

These are the quotes the drafts cite as `Testimony`. The main agent should
confirm them against the actual transcript before firing — testimony must be
the psyche's exact words or the guardian rejects `MissingTestimony`.

1. *"always use at least one subagent to get into anything complex - I want
   the main thinking agent to spend more time reasoning than exploring, and he
   can even get his basic training based on the subagent's response, with
   sections of files suggestions even! Let's make the main thread the most
   precious context."*
2. *"We should minimize agents.md, and re-think all our skill ladder for
   efficiency and atomicity with a good manifest to let the dispatcher pick
   skills by their name and description only."*
3. (paraphrase to confirm verbatim) Drop the fixed designer/operator
   distinction; any agent works on whatever the psyche points it at; quality
   comes from cross-audit (codex audits claude's output or vice-versa).
4. (paraphrase to confirm verbatim) The task dependency graph is now "the
   weave"; its nodes are "minds," replacing "beads."
5. *"ask me a few questions at least"* — relax the one-question-per-turn rule
   toward a small batch of questions in prose per turn.

## Existing-record audit (read-only findings)

- **2o3g** — `Constraint`, certainty `Maximum`, importance `Medium`. Current
  description: *"Agents dispatch subagents only when the psyche explicitly
  authorizes it (a per-keystroke AGENTS.md override for all workspace agents).
  When authorized, treat subagents as asynchronous sidecar work: dispatch
  returns control, the main agent keeps the critical path moving or answers
  new psyche prompts, and uses nonblocking sidecars where they materially
  reduce audit, checklist, or verification risk. Block on a subagent only when
  the psyche asks or is waiting on nothing else."*
- **69fa** — `Principle`, certainty `Medium`, importance `Minimum`. Current
  description: *"A session's early high-fidelity context window the psyche's
  mark is the first roughly one hundred thousand tokens is reserved for the
  main agent's deepest thinking and intent alignment; once that window is spent
  the agent launches a fleet of fresh-context sub-agents primed with the
  settled conclusions rather than continuing to reason in a degraded or
  compacted context."*
- **xrxy** — `Decision`, certainty `High`, importance `Minimum`. Current
  description: *"The prime designer chair runs parallel subagent workflows by
  default (a designer-specific exception to the no-subagents default still
  binding operator, system, poet, and assistant lanes); it does not extend to
  second/assistant designer lanes unless the psyche says so. The composite
  designer runs Claude and Codex in parallel on the same prompt, then selects
  or merges. Operators use parallel subagents only when authorized, staying
  responsible for integration, constraints, tests, and the final report."*
- **Vocabulary**: `PublicTextSearch weave` returns **no matching record** —
  draft (d) is a genuine fresh `Record`. `PublicTextSearch beads` /
  `bead` / `mind` show many records that *use* the words but none that *names
  the vocabulary itself* as a renaming decision.
- **Question cadence**: no Spirit record encodes "one focused question per
  turn." That cadence lives in `skills/intent-alignment.md:46-50` and the
  AGENTS.md "Interactive agents default to intent alignment" override. The
  adjacent record is **ky10** (`Decision High`: intent-alignment is the default
  discipline for interactive agents) — but it carries the *default*, not the
  *one-question* cadence. So (f) has no edit target; it is a skill+AGENTS.md
  edit, optionally backed by a light fresh Record.

## Cross-cutting interactions the psyche must arbitrate

- **2o3g, 69fa, and xrxy all touch the same subagent-default knob.** 2o3g says
  "only on explicit authorization" (Maximum), xrxy carves a designer-only
  exception (High), 69fa describes the precious-window-then-fleet shape
  (Medium). The new direction makes "dispatch at least one subagent for
  anything complex" a *standing default for all agents*. Firing (a) + (c)
  together collapses the designer-only exception into a universal default;
  2o3g's old "only when authorized" framing and xrxy's "designer-specific
  exception" framing both retire. Confirm the psyche wants both retired in the
  same pass, not just one.
- **The "minds" naming collides with persona-mind.** Records mn3k, 7yth, ddlv,
  m3ms, a4i6, x92t use **"mind" / "Mind"** for the persona-mind component (the
  typed memory store, "model call + agent = a thinking process"). The psyche's
  new "minds" = nodes-of-the-weave is a *different* concept sharing the word.
  This is a genuine naming clash. **Psyche must decide** whether the
  task-graph node really takes the bare word "mind" (overloading it), or a
  qualified form (e.g. "weave-mind" / "thread"). Draft (d) below uses the bare
  word as instructed but flags this prominently.

## Draft (a) — 2o3g: subagent-for-orientation as the standing default

The new direction inverts the operative half of a `Maximum`-certainty
constraint, so this is a `Supersede` (meaning flips), not a `Clarify`. The
open nuance — does the default open *work-execution* dispatch too, or only
*orientation* — is real and psyche-only. Two variants below; fire exactly one.

### Variant a1 — orientation default-on, heavy work-dispatch stays psyche-gated (recommended)

```
spirit "(Supersede ([2o3g] [([(Technology (Software (Engineering DevelopmentProcess)))] Constraint [|Getting into anything complex starts by dispatching at least one fresh-context subagent to explore and report back, as the standing default for every workspace agent — no per-keystroke psyche authorization needed for orientation work. The main thinking agent spends its turns reasoning over the distilled subagent response rather than exploring the codebase itself. Heavier work-execution dispatch (parallel implementation across many nodes) still asks the psyche unless the lane already carries a standing parallel-work mandate. Subagents are nonblocking sidecars: dispatch returns control and the main agent keeps the critical path moving or answers new psyche prompts.|] High Medium Zero [subagents orientation agents-md async-dispatch precious-context])] ([([always use at least one subagent to get into anything complex - I want the main thinking agent to spend more time reasoning than exploring] (Some [prior 2o3g constraint required explicit psyche authorization for every subagent dispatch]))] [psyche inverts the operative half of the old Maximum constraint: orientation dispatch becomes the standing default while heavy parallel work-execution stays psyche-gated; supersede because the meaning flips, not a clarification])))"
```

### Variant a2 — both orientation and work-execution dispatch default-on

```
spirit "(Supersede ([2o3g] [([(Technology (Software (Engineering DevelopmentProcess)))] Constraint [|Every workspace agent dispatches at least one fresh-context subagent to get into anything complex, as the standing default — orientation and work-execution both, no per-keystroke psyche authorization. The main thinking agent reserves its turns for reasoning over the distilled subagent response rather than exploring. Subagents are nonblocking sidecars: dispatch returns control and the main agent keeps the critical path moving or answers new psyche prompts; block only when the psyche asks or nothing else is waiting.|] High Medium Zero [subagents orientation work-dispatch agents-md async-dispatch precious-context])] ([([always use at least one subagent to get into anything complex - I want the main thinking agent to spend more time reasoning than exploring] (Some [prior 2o3g constraint required explicit psyche authorization for every subagent dispatch]))] [psyche makes subagent-by-default universal across orientation and work-execution; supersede the old Maximum authorization-gate constraint])))"
```

**Field choices.** `Kind` stays `Constraint` (it still draws a boundary on how
agents start complex work). **Certainty drops Maximum → High**: the old
Maximum was for "never dispatch without authorization"; the new rule is a firm
default but the psyche is still settling the orientation/work-execution split,
so it is not a founding axiom — `High` is the honest read of "always use at
least one subagent." Importance held at `Medium` (recurring topic, not yet
blocking everything). Privacy `Zero` (public workspace conduct). Referents add
`orientation` and `precious-context`; `operator` dropped because the rule is
now all-agent.

**Psyche-only:** a1 vs a2 (orientation-only vs orientation+work). Recommend
a1 — the psyche emphasized *thinking over exploring*, which is orientation;
parallel implementation is a heavier commitment worth keeping a hand on.

## Draft (b) — 69fa: strengthen the precious-main-thread principle

The psyche reinforced and *extended* the existing principle (training from
subagent response, specific file-section pointers). Same identity, sharper
meaning → `Clarify`.

```
spirit "(Clarify (69fa [|The main thread is the most precious context: the lead agent optimizes its turns for reasoning and intent alignment over exploration, and dispatches a fresh-context subagent for anything complex rather than spending its own window exploring. It takes its orientation — even its basic training for the task — from the subagent's distilled response, including specific file-section pointers the subagent surfaces. The early high-fidelity window (the psyche's mark, roughly the first one hundred thousand tokens) is reserved for the lead agent's deepest thinking; once spent, work continues through a fleet of fresh-context subagents primed with the settled conclusions rather than reasoning on in a degraded or compacted context.|] ([([he can even get his basic training based on the subagent's response, with sections of files suggestions even! Let's make the main thread the most precious context] (Some [the prior 69fa principle reserved the early window for deepest thinking and then launched a fresh-context fleet]))] [psyche sharpens 69fa: names the main thread the most precious context, and adds that the lead agent takes orientation and basic task-training from the subagent's distilled response including specific file-section pointers; an edit of the existing principle, not a sibling record])))"
```

**Field choices.** `Clarify` carries only the corrected description (kind,
certainty, importance, privacy are preserved by the operation). The principle
keeps `Principle / Medium / Minimum / Zero`. The psyche's wording is firm but
this is a working-style preference, not a near-irreversible axiom — `Medium`
certainty stays honest. **Psyche-only:** whether to bump importance — this
topic is now the *lane's namesake* and recurring, which arguably warrants a
later `BumpImportance 69fa`; flag but don't bundle.

## Draft (c) — xrxy: generalize subagent-by-default to all disciplines

The designer-only exception is exactly what the new direction removes. The
core decision (subagent-by-default + composite cross-audit) survives but the
"designer-specific exception" framing must retire → `Supersede`. (Affirmative
framing: lead with the positive universal rule, not "no longer designer-only.")

```
spirit "(Supersede ([xrxy] [([(Work Teamwork)] Decision [|Subagent-by-default and parallel cross-audit are the universal workspace protocol, not a designer-only exception: any lane dispatches fresh-context subagents to get into complex work, and quality comes from cross-audit — one model audits another's output (Codex audits Claude or the reverse) before it is trusted. The lead agent stays responsible for integration, constraints, tests, and the final report. The old prime-designer-chair scoping (designer runs parallel workflows by default while operator/system/poet/assistant stay gated) is replaced by this all-discipline default.|] High Minimum Zero [subagents cross-audit composite-review claude codex precious-context])] ([([drop the fixed designer/operator distinction; any agent works on whatever the psyche points it at; quality comes from cross-audit] (Some [xrxy scoped subagent-by-default to the prime designer chair only, gating operator/system/poet/assistant]))] [psyche generalizes the designer-only subagent-by-default to every discipline and centers cross-audit as the quality mechanism; supersede the designer-scoped decision])))"
```

**Field choices.** `Kind` stays `Decision`. Certainty `High` carried over —
the psyche stated this firmly and it composes with 2o3g and the dynamic-lane
intent (potn). Importance `Minimum` (fresh framing; bump on recurrence).
Referents swap `prime-designer`/`composite-designer`/`operator` for
`cross-audit`/`composite-review`. **Psyche-only:** confirm testimony #3
verbatim; confirm cross-audit is *the* quality gate (not merely one option).

## Draft (d) — fresh Record: the weave and minds vocabulary

No existing `weave` record → fresh `Decision`. **Naming-collision flag in the
description and below** because "minds" overloads persona-mind.

```
spirit "(Record (([(Information Documentation) (Technology (Software (Engineering Management)))] Decision [|The task dependency graph is named the weave; its nodes are minds, replacing the term beads. A mind is one unit of trackable work linked into the weave by dependency edges (what blocks what, what runs in parallel). This renames the bead/dependency-graph vocabulary workspace-wide. Note the word mind already names the persona-mind memory component; whether the weave node takes the bare word mind or a qualified form is a pending naming decision.|] Medium Minimum Zero [weave minds beads task-graph dependency-graph persona-mind])) ([([the task dependency graph is now the weave; its nodes are minds, the replacement for beads] None)] [psyche settles new workspace vocabulary: weave for the dependency graph, minds for its nodes, replacing beads; fresh Record because PublicTextSearch found no weave record; certainty Medium because the bare-word-mind versus persona-mind collision is unresolved])))"
```

**Field choices.** `Kind` `Decision` (a naming choice). **Certainty `Medium`,
not High**: the psyche named the vocabulary clearly, but the "mind" collision
with persona-mind is unresolved, so the *specific spelling* is not yet settled.
Importance `Minimum`. Domains: documentation + engineering-management (it is
process vocabulary). Referents include both `minds` and `persona-mind` so the
guardian surfaces the collision against existing mind-records.

**Psyche-only (load-bearing):** Does the weave node take the **bare word
"mind"**, overloading persona-mind, or a **qualified form** (weave-mind,
thread, strand)? If the psyche confirms bare "mind," the description's collision
clause can soften to High certainty. If qualified, edit the description before
firing.

## Draft (e) — fresh Record: minimize AGENTS.md, atomic skill manifest

No record states "minimize AGENTS.md to a thin spine." Adjacent records (x3oa
skills.nota as single source; 9x28 two-sentence positive descriptions; k4i3
skills are tight; x92t role-token skill loading) are *complemented*, not
duplicated, by this. Fresh `Principle`.

```
spirit "(Record (([(Information Documentation) (Technology (Software (Intelligence AgentSystems)))] Principle [|AGENTS.md is a thin always-loaded spine; binding rules live as atomic single-purpose skills that a dispatcher selects by name and description alone from the skills manifest. Keep the every-session contract minimal so the precious main context is spent on the task, not on re-reading rules; the skill ladder is re-shaped for efficiency and atomicity, each skill self-contained and pickable from the manifest without opening it.|] High Minimum Zero [agents-md skills-manifest skill-ladder atomicity precious-context])) ([([We should minimize agents.md, and re-think all our skill ladder for efficiency and atomicity with a good manifest to let the dispatcher pick skills by their name and description only] None)] [psyche directs a minimal AGENTS.md spine plus an atomic name-and-description-selectable skill manifest; fresh Principle complementing x3oa/9x28/k4i3 which govern skills.nota content but do not state the minimize-the-spine direction])))"
```

**Field choices.** `Kind` `Principle` (a general rule about how the contract
and skills are shaped). **Certainty `High`** — stated as a clear directive
("We should…") with conviction, and it composes with the precious-context
theme; not a founding axiom, so not Maximum. Importance `Minimum`. Domains:
documentation + agent-systems (skill-loading is agent tooling). **Psyche-only:**
whether this is a Principle or a firmer Decision to actually execute the
minimization now (the latter would also spawn `work` minds for the rewrite).

## Draft (f) — question cadence: a few questions in prose per turn

**No Spirit record encodes "one question per turn"** — it lives in
`skills/intent-alignment.md:46-50` (*"Ask exactly one focused question per
turn… never a batch"*) and the AGENTS.md intent-alignment override. So there is
**no edit target to Clarify**; the change is primarily a **skill-file +
AGENTS.md edit** (note those separately as `work`). Optionally back it with a
light fresh Record so the relaxation is in the intent layer:

```
spirit "(Record (([(Technology (Software (Intelligence AgentSystems))) (Language Rhetoric)] Clarification [|Intent-alignment questions come a few at a time in plain chat prose — a small batch per turn, not strictly one question per turn — still never the structured questionnaire UI. Each question still carries its decision, why it matters, the recommended answer, and the alternatives; the relaxation is batch size, not rigor.|] High Minimum Zero [intent-alignment question-cadence human-interaction])) ([([ask me a few questions at least] (Some [the prior rule was exactly one focused question per turn, never a batch]))] [psyche relaxes the one-question-per-turn cadence toward a small prose batch per turn while keeping the no-questionnaire-UI rule; fresh Clarification because no Spirit record holds the one-question cadence to edit — it lives only in skills/intent-alignment.md and AGENTS.md])))"
```

**Field choices.** `Kind` `Clarification` (the psyche is refining an existing
working rule). This is the rare legitimate standalone `Kind::Clarification`
because **there is genuinely no record to edit** — the rule lived only in
skill/AGENTS.md text. `Certainty High` (a clear directive). Importance
`Minimum`. **Psyche-only:** (i) whether a Spirit record is wanted at all here,
or just the skill+AGENTS.md edit; (ii) confirm "a few questions" means a small
batch, not "as many as needed." The parallel non-Spirit edits to draft
separately: `skills/intent-alignment.md:46-50` and the AGENTS.md "Interactive
agents default to intent alignment" override both currently say "exactly one
focused question per turn, never a batch."

## Gap flag — cross-audit has no standalone capture path here

The psyche's testimony #3 also asserts **drop the fixed designer/operator
distinction; any agent works on whatever the psyche points it at**. Draft (c)
folds the cross-audit half into xrxy, but the *drop-the-fixed-distinction* half
overlaps with **potn** (dynamic topic-named lanes; discipline is metadata,
`Decision High`) and **57hq**/**kxzh** (specialized lanes via skill files).
The psyche should decide whether "any agent works on whatever the psyche points
it at" needs its own Record (or a `Clarify` of potn) beyond what (c) captures.
Recommend: confirm whether the all-discipline framing in (c) plus potn already
holds it, or capture a dedicated record. This is a real underdetermination, not
a drafting omission.

## Summary of verbs and the open psyche decisions

| Draft | Target | Verb | Kind | Certainty | The psyche-only call |
|---|---|---|---|---|---|
| a | 2o3g | Supersede | Constraint | High | a1 (orientation only) vs a2 (orientation+work) |
| b | 69fa | Clarify | Principle | Medium (held) | bump importance later? |
| c | xrxy | Supersede | Decision | High | confirm cross-audit is the quality gate; verbatim #3 |
| d | new | Record | Decision | Medium | bare "mind" vs qualified (persona-mind collision) |
| e | new | Record | Principle | High | Principle vs execute-now Decision |
| f | new | Record | Clarification | High | want a record at all, or skill+AGENTS.md edit only |

Nothing was written to Spirit. These are drafts only.
