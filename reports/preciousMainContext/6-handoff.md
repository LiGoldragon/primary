---
title: 6 — Handoff: preciousMainContext lane state and continuation
lane: preciousMainContext
discipline: Designer
date: 2026-06-24
description: |
  Consolidated pickup point for the preciousMainContext lane. What landed,
  what is authorized-but-pending, and how a fresh context should execute the
  rest. Synthesises reports 1-5; does not replace them.
---

# 6 — Handoff: preciousMainContext lane state and continuation

This is the fresh-context pickup point. A new agent should be able to read
this one file (plus the detailed reports it points to) and execute the rest
with a clean smart zone. Reports 1-5 in this directory remain the detail;
this is the map.

## The lane in one line

Make the **main thread the most precious context**: the lead agent reasons,
helpers explore. Concretely this lane (a) captured that as intent, (b) is
de-duplicating the skill ladder so AGENTS.md shrinks to a thin spine and
skills are pickable by name+description, and (c) renamed the work-tracking
vocabulary. Named for its intent, discipline Designer, registered as
`precious-main-context-designer`.

## The vocabulary (authorized)

- **Mind** — the work-tracking tool (replaces the beads tool `bd`/`.beads`).
- **a memory** — one work-item (replaces "a bead").
- **the weave** — the dependency graph the memories form (replaces "bead graph").
- The word **"beads" is retired**. (The actual `bd`→Mind tool build is a
  downstream effort, not this lane. This lane uses the existing `bd` tool as
  the current substrate.)

Note: "Mind"/"memory" deliberately echo the persona-mind (a thinking
process). Written contract must self-disambiguate by context.

## Spirit records — what LANDED

Verified by the capture helper (full commands + rejection reasons appended to
`3-capture-drafts.md`):

| Was | Now | Kind | Gist |
|---|---|---|---|
| `2o3g` | `30cu` | Constraint/High | Sending helpers to **read/explore** is the standing default when early in context and facing more than a few known files, or any multi-level exploration. Cite simply; scale effort (simple=one helper/medium, complex=high/xhigh). Sending helpers to **make changes** still needs psyche go-ahead. |
| `69fa` | `69fa` | Principle | The main thread is the most precious context; the lead takes orientation — including specific **file-section pointers** — from the helper's distilled response. |
| `xrxy` | `hu84` | Decision/High | Subagent-by-default + **cross-audit** (one model audits the other's output) is the universal quality protocol — generalized off the designer-only exception. |
| `ljce` | `d7ew` | (Supersede) | **A few** focused questions per turn (asking a few is the standard); still no questionnaire UI. |

## Authorized but PENDING — the two coordinated sweeps

Spirit's integrity guardian refused two single records because the old shapes
are still wired into live record clusters; the psyche has now **authorized
the coordinated sweeps** (Supersede/ChangeRecord across each cluster, done as
one deliberate pass):

1. **Vocabulary rename sweep** — retire "beads" / introduce Mind·memory·weave
   across the cluster the guardian named: `ypg9, el7z, krez, j028, mi6m,
   pm1b, 3w61, wgii` (and any sibling it surfaces during the pass). This is
   the Spirit-side of the rename; the doc-side is weave item **W8**.
2. **Designer/operator retirement sweep** — across `ahop, kxzh, zjop, irmw,
   jq8w, ty8z`. Caveat for the psyche to confirm in-pass: the guardian
   reports these records still *actively use* the distinction, so decide per
   record whether it is genuinely retired or merely dormant-for-routing.

Also pending and related:

- **Minimize-AGENTS.md** record did not land — it conflicts with `ky10`
  (which places intent-alignment in the agent-contract files). Landing the
  minimize principle needs a `ChangeRecord`/`Supersede` of `ky10` first. This
  gates weave item **W6**.

## The context-preserving dispatch rule (for W5)

From the schema-help lane's post-mortem
(`reports/schema-help-daemon-pilot-operator/1-skill-change-handoff.md`) — an
operator dispatched a context helper, then spent its own smart zone redoing
the helper's exploration, and the psyche never got a turn. The missing rule,
to be the centerpiece of **W5** (with a one-line pointer from
`human-interaction.md`):

> When the psyche asks you to use a helper to gather context, save context,
> decide alignment, or prepare a fan-out, run only the **minimal dispatch
> envelope** — the Spirit gate, any lane/report setup, and the helper's brief
> — then stop. Do not read the repos, skills, reports, or weave the helper
> was sent to collect. Wait for its report, or do only genuinely unrelated
> work. The helper owns the broad read; duplicating it defeats the dispatch.

Companion lesson: when a helper **writes** a file, read it back (the end
especially) before trusting it — W1's helper left literal `</content>` /
`</invoke>` tool-scaffolding at the file end (now removed).

## The W1 recipe (replicate on W2-W4)

W1 cut `human-interaction.md` from 115 lines/14 sections to 66/7. The
four-move recipe to repeat on `intent-log`, `spirit-cli`, `session-lanes`:

1. **Delete only verified duplicates** — confirm the rule is genuinely in
   AGENTS.md (cite the line) before deleting; don't trust the digest alone.
2. **Collapse to a pointer** when another skill owns the content.
3. **Flag-and-defer** when content belongs in a *different* skill — leave it
   in place under a "move to X" banner so the move is atomic when that skill
   is cut (nothing floats loose).
4. **Preserve genuine boundary nuance inline** (e.g. the privacy
   "relayed-request-isn't-authority" clause was folded into a pointer, not
   dropped).

## The weave (beads under epic `primary-ptvb`)

| Item | Bead | Status |
|---|---|---|
| W1 | `primary-ptvb.1` | **DONE** — human-interaction cut (residue cleaned) |
| W2 | `primary-ptvb.2` | ready — cut intent-log (recipe above) |
| W3 | `primary-ptvb.3` | ready — cut spirit-cli (move ~120 misplaced lines) |
| W4 | `primary-ptvb.4` | ready — cut session-lanes |
| W5 | `primary-ptvb.5` | ready — write the helpers skill; **centerpiece = the dispatch rule above** |
| W6 | `primary-ptvb.6` | blocked — shrink AGENTS.md (needs W1-W5 + the `ky10` reconcile) |
| W7 | `primary-ptvb.7` | blocked — sharpen skills.nota descriptions |
| W8 | `primary-ptvb.8` | blocked — roll out Mind/memory/weave across docs |

Two new sweep memories are being added under the same epic (see the bead
helper's update): the **vocabulary Spirit-sweep** (blocks W8) and the
**designer/operator Spirit-sweep**, plus a **`ky10` reconcile** memory
(blocks W6).

## Coordination / the lock question

The psyche asked whether the lane-lock system is still in use. Honest state:
the orchestrate **daemon lane-registry is live** — this session registered
`precious-main-context-designer` and `Observe Lanes` returned the active set
(`new-lanes-design-designer`, `schema-designer`, this lane). Whether the
per-lane `orchestrate/<lane>.lock` claim-flow is actively *gating* edits or
commits is **not confirmed** — the "blocked from committing" in the Codex
handoff was that agent's caution about committing another lane's
residue-laden working copy, not a lock denial. With the residue cleaned and
"anybody can commit on primary," there is no actual block. Open question
worth a definitive answer: is the file-lock claim-flow retired in favour of
the daemon registry, or still expected?

## Pickup steps for a fresh context

1. Read this file. Apply the dispatch rule to *yourself*: the detail is in
   reports 1-5 and the named Spirit clusters — if you need them, send a
   helper, don't read broadly in your smart zone.
2. **Execute the two authorized sweeps** (vocabulary; designer/operator) as
   deliberate Supersede/ChangeRecord passes over the named clusters; reload
   `skills/intent-log.md` + `skills/spirit-cli.md` first; use the psyche's
   verbatim words (in this transcript) as testimony.
3. **Reconcile `ky10`**, then land the minimize-AGENTS.md principle.
4. **Run W2-W4** with the W1 recipe; then **W5** (dispatch rule), **W6**
   (shrink AGENTS.md), **W7** (descriptions), **W8** (doc vocabulary).
5. Commit the whole primary working copy and push main as you go (no
   path-scoped commits).

## Pointers

- `1-bearings.md` — workspace orientation (lane model, task-graph, intent).
- `2-skill-digest.md` — the five-skill prune table (PRI 1/2/3, line ranges).
- `3-capture-drafts.md` — the Spirit drafts + the firing report ("what landed").
- `4-weave.md` — the bead graph (mermaid + ids).
- `5-human-interaction-cut.md` — the W1 changelog.
- `reports/schema-help-daemon-pilot-operator/1-skill-change-handoff.md` — the
  dispatch-discipline post-mortem.
