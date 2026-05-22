# 15 — Clarification for operator-assistant on Orchestrate→Router authority

*Psyche-issued correction to the authority direction implied by
`reports/operator-assistant/160`. The destination
(`owner-signal-persona-router`) is right; the caller is **Orchestrate,
not Mind**. This report names the correction, what it means for the
work landed in /160, and prior intent the operator-assistant
overlooked when designing the move.*

## The correction

`intent/component-shape.nota` 2026-05-20T13:30:00Z (Correction,
Maximum):

> *"I disagree that this means that the mind owns the router, the
> orchestrator owns the router. There's no need for the mind to take
> care of all of this low-level operation. This is orchestrator work."*

Mind does NOT own Router. Orchestrate owns Router. Channel
choreography orders are Orchestrate→Router, not Mind→Router. The
prior 2026-05-20T13:09:13Z intent record framing these as
"Mind-to-Router authority orders" is superseded.

The chain is:

```text
Mind (cognitive decision: should this channel exist? extend? deny?)
  → owner-signal-persona-orchestrate  (Mind orders Orchestrate)
    → owner-signal-persona-router     (Orchestrate orders Router)
```

Mind decides; Orchestrate enacts. Low-level channel operations are
orchestrator machinery, not mind cognition.

## What this means for /160's work

`owner-signal-persona-router` with `Grant` / `Extend` / `Revoke` /
`Deny` is **correctly placed** — the verbs belong there. What
changes is the **caller**:

- Before correction: Mind calls `owner-signal-persona-router` directly.
- After correction: Orchestrate calls `owner-signal-persona-router`;
  Mind calls `owner-signal-persona-orchestrate` first.

This settles /160's Q2 ("Does Mind call the Router owner socket
directly, or should Mind issue an order to Orchestrate and let
Orchestrate call `owner-signal-persona-router`?") — the latter.

Two concrete implications:

1. **Payload fields** in `Grant`/`Extend`/`Revoke`/`Deny` records
   should be reconsidered under the Orchestrate-as-caller assumption.
   Anything that implicitly assumed Mind as caller (correlation
   identifiers tied to Mind decisions, decision provenance fields)
   should be Orchestrate-shaped — Orchestrate carries its own
   machinery correlation (agent-run identifiers, scope acquisitions,
   role identifiers) that the Router-side payload may need.

2. **`owner-signal-persona-orchestrate` needs corresponding inbound
   verbs.** Today it carries `Create(CreateRoleOrder)`,
   `Retire(RetireRoleOrder)`, `Refresh(RefreshRepositoryIndexOrder)` —
   no channel-choreography vocabulary. The Mind→Orchestrate hop has
   no contract surface yet. The chain breaks at the first hop until
   Orchestrate's owner signal grows verbs that let Mind issue
   channel decisions to Orchestrate (likely shaped as
   "enact this channel choreography decision" rather than as
   Mind doing low-level Grant/Extend semantics).

## Prior intent the operator-assistant overlooked

### 1. The canonical authority chain is on the record

`intent/persona.nota` 2026-05-19T15:30:00Z (Decision, Maximum):

> *"Spirit owns mind in the authority graph. supervisor → spirit
> → mind → orchestrate → router/harness/terminal."*

A single chain. Router's owner is Orchestrate. No parallel
"Mind owns Router" branch. This intent has been on the record
since 2026-05-19; the verb-move design should have respected it.

The mermaid in `skills/component-triad.md` (lines ~308-326) shows
Mind issuing Mutate **directly** to Router as step 3 — that mermaid
is inconsistent with the canonical chain and needs designer-lane
correction. When skill text disagrees with intent, intent wins
(per ESSENCE §"The intent layer").

### 2. The state-vs-machinery split

`intent/persona.nota` 2026-05-18T12:08:41Z (Principle, Maximum):

> *"persona-mind owns STATE — work graph, memory, thoughts, durable
> policy truth, channel-grant authority **decisions**. persona-orchestrate
> owns MACHINERY — role claims, activity log, agent-run lifecycle,
> spawn plans, scope-acquisition workflow, executor capacity,
> scheduling, escalation, lane registry."*

Channel-grant **decisions** live in Mind. The **enactment** of those
decisions (calling Router to install/extend/retract) is
Orchestrate's machinery. The framing "Mind issues channel-grant
orders to Router" conflates decision (Mind) with enactment
(Orchestrate). This principle has been on the record since the
mind/orchestrate redesign discussion.

### 3. The five-missing-owner-signals deliberate-emergence intent

`intent/component-shape.nota` 2026-05-19T20:30:00Z (Clarification,
Maximum):

> *"The 5 missing owner-signal-persona-* repos (mind, router,
> harness, message, auth) are intentionally missing — the workspace
> is moving fast and the owner-signal pattern is recent. Don't
> backfill them by assumption; let them emerge as each component's
> owner discipline crystallizes."*

Creating `owner-signal-persona-router` (one of the five) without
surfacing this intent for explicit psyche affirmation is a
process gap. The psyche has now affirmed creation implicitly by
greenlighting the verb-move, so the contract stays. **Going
forward, before instantiating any of the remaining
deliberately-missing repos (`owner-signal-persona-harness`,
`owner-signal-persona-message`, `owner-signal-persona-auth`),
surface this intent to psyche and ask "is now the time?"**

### 4. The earlier "verbs live in signal-persona-mind" intent

`intent/component-shape.nota` 2026-05-19T20:30:00Z (Decision,
Maximum):

> *"signal-persona-mind's channel-choreography family splits into
> multiple contract-local verbs (Grant / Extend / Revoke / List /
> Deny — names TBD) rather than collapsing under one Adjudicate
> verb."*

This earlier intent literally placed channel-choreography verbs
**inside `signal-persona-mind`**. /160's move out of
`signal-persona-mind` contradicts that earlier record.

The newer intent at 13:09Z and the correction at 13:30Z effectively
supersede this 20:30Z record — verbs live in
`owner-signal-persona-router` called by Orchestrate, not in
`signal-persona-mind`. But **the contradiction should have been
surfaced** as part of the verb-move proposal, not silently
overridden. The supersession protocol
(`skills/intent-maintenance.md`) requires marking the prior record
as superseded explicitly; that's now intent-maintenance work
(designer-lane).

The pattern to follow: when proposing a structural change, grep
the intent log for prior statements on the same area and surface
contradictions for explicit supersession before acting.

## What's still open from /160

The other questions in /160 are unaffected by this correction:

- Q1: `ChannelList` placement (Mind-side read vs Router-side).
- Q3: `AdjudicationRequest` as Router→Mind working signal vs
  router-tap event.

Both remain valid open questions to surface to psyche.

## Concrete next steps

1. **Re-examine `Grant`/`Extend`/`Revoke`/`Deny` payload fields**
   under the Orchestrate-as-caller assumption. Replace any
   Mind-shaped correlation with Orchestrate-shaped surfaces.
2. **Surface to psyche**: what verbs does
   `owner-signal-persona-orchestrate` need to grow so Mind can
   order channel decisions through it? The shape is open — Mind
   probably orders Orchestrate at a *higher* level of abstraction
   than `Grant`/`Extend` (the decision, not the low-level enactment).
3. **Update /160's report** with the Q2 resolution explicitly:
   "Mind orders Orchestrate; Orchestrate orders Router."
4. **Going forward**: before any structural move, grep
   `intent/*.nota` for prior statements on the affected area and
   surface contradictions for explicit psyche supersession.

## References

- `intent/component-shape.nota` 2026-05-20T13:30:00Z — the
  Correction.
- `intent/persona.nota` 2026-05-19T15:30:00Z — canonical authority
  chain.
- `intent/persona.nota` 2026-05-18T12:08:41Z — state-vs-machinery
  split.
- `intent/component-shape.nota` 2026-05-19T20:30:00Z — five missing
  owner-signal-* repos (Clarification) + signal-persona-mind
  channel-verb split (Decision pair).
- `reports/operator-assistant/159-persona-mind-signal-tree-owner-contract-vision.md`
- `reports/operator-assistant/160-owner-signal-persona-router-channel-authority.md`
- `reports/second-designer-assistant/14-audit-of-operator-assistant-159-owner-signal-persona-mind.md`
- `skills/component-triad.md` §"4. Two authority tiers" — canonical
  "orchestrate owns router and harness" wording (consistent with
  intent).
- `skills/component-triad.md` authority-chain mermaid (~lines
  308-326) — inconsistent with the canonical chain; designer-lane
  fix needed.
- `skills/intent-maintenance.md` — supersession protocol the
  20:30Z record needs applied.
