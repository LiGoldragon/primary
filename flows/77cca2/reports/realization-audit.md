# Realization Audit: Loose Ends and Report Skill

Flow `77cca2` — 2026-09-04

---

## Recent OS and Deployment Work

| Commit | What happened |
|--------|--------------|
| `f0f286cd2` | Fixed Zeus deployments: stale LAN transport replaced with hostname. Deploys 165+167 succeeded. |
| `857b518d4` | Codex 0.152.1→0.153.2, ChatGPT desktop updated. `li` UserEnvironment deployed. Zeus CompleteHost deploy 158 failed (BuilderUnreachable). |
| `7dd051112` | Orchestrate 0.29.0, claude-answers 0.5.0, curriculum-deploy 0.5.0 deployed. |
| `432df00fe` | Flow 6329f1 landing recorded. |
| `23aaf7a7f` | Protos layers and Ethos Declaration landed. |
| `3cb9c06a7` | Guard instructions removed from agent definitions and NON_MANAGEMENT_AGENTS. |

---

## Branch and Stash Audit

### Branches

#### `push-ktnnmzyuyknz` — Zeus activation contract
- **1 commit ahead, 602 behind main**
- Contains "Record Zeus staged activation contract" from flow `01a02b6a`
- Single commit touches only flow evidence files in `flows/01a02b6a/`
- **Risk**: High divergence. The activation contract evidence may have been superseded by the Zeus deployment fixes that landed on main.
- **Recommendation**: Cherry-pick the evidence commit if the activation contract record is still wanted; otherwise delete the branch.

#### `push-qvurutrqnnno` — stale ancestor
- **0 commits ahead, 704 behind main**
- Pure ancestor of main — pointer to `a8478f34c` (flow anatomy and LLM vocabulary research, 2026-08-21)
- **Risk**: None. Already fully merged.
- **Recommendation**: Delete the branch.

### Stashes

#### `stash@{0}` — Herdr input-route comparison
- Flow `2f6b1dc5` work-in-progress
- Contains vision records (`contextStrata.md`, `vocabulary.md`) and verified evidence (`claude-code-context.md`)
- **Risk**: Vision records may not have landed in main. Potentially valuable.
- **Recommendation**: Pop/apply, review, commit if records are still current.

#### `stash@{1}` — code-workspace setting
- Just 3 lines of `primary.code-workspace`
- Already preserved at `origin/preserve/toolchain-stash-codeworkspace-20260716`
- **Recommendation**: Drop.

### Preserve Branches (remote only)
Seven `origin/preserve/*` branches from July 2026 — archival snapshots of old toolchain work. Not merge candidates. Leave as-is.

---

## Merge Risk Summary

```
Branch/Stash               Status              Risk    Action
─────────────────────────  ──────────────────  ──────  ─────────────────────
push-ktnnmzyuyknz          1 ahead / 602 back  HIGH    Cherry-pick or delete
push-qvurutrqnnno          Pure ancestor       NONE    Delete
stash@{0} (Herdr)          Vision + evidence   MED     Pop, review, commit
stash@{1} (workspace)      Already preserved   NONE    Drop
preserve/* (7 branches)    Archival            NONE    Leave as-is
```

---

## Web Report Skill: Current State

### What exists today

The **`flow-evidence`** skill prescribes Markdown reports in the flow directory:

> "Write the artifact under the supplied `FLOW_DIRECTORY`. Use `reports/<subject>.md` for a carried account."

The **`main-flow`** skill says the main flow writes only logs, psyche records, and beads — everything else goes through subflows.

The **visuals ruling** (psyche, 2026-08-21) establishes a medium rule:

> Response → ASCII; Artifact → Mermaid/SVG.

### What does NOT exist

No skill codifies the "main flow authors Markdown → subagent renders it as a web artifact with SVG charts" pattern. The psyche recorded this intent in two places but it was never implemented as a skill:

- `flows/01a0428b/vision/codexOnlySkill.md` — "Check a recent codex session for the web reporting procedure which we'll put in a codex only skill."
- `flows/01a0428b/vision/useASubflowToPutTheReportTogether.md` — "It would be better to use a subflow to put the report together."

### Would the current behavior produce this pattern naturally?

**No.** Without explicit instruction, the current skills would produce:
1. A Markdown file in the flow directory (flow-evidence)
2. Terminal text with ASCII visuals (visuals ruling)
3. No web artifact at all

---

## Proposed Skill: `flow-report`

A skill that naturally produces the Markdown-first, subagent-renders pattern without the psyche having to demand it each time.

### Design Principles

The skill embodies these psyche rulings:
- **Visuals are soothing** — they create a better dynamic between human and machine
- **Medium rule** — response gets ASCII, artifacts get SVG/Mermaid
- **Subflow renders** — the main flow authors content, a subagent handles presentation
- **Cloud-gated** — web artifacts are Claude-side only until Codex infrastructure catches up

### Proposed Skill Text

```markdown
# flow-report

A flow's findings, when they deserve a presentation to the psyche,
are rendered as a web report.

{% if claude %}
## Rendering

The main flow authors a Markdown report in `FLOW_DIRECTORY/reports/`.
A subflow renders it as a web artifact:

- Read the Markdown report
- Load the `artifact-design` skill
- Render an HTML page with inline SVG for every chart, diagram, and
  visual element
- Diagrams use inline SVG, not Mermaid script — they render without
  a library
- Data tables become charts; process descriptions become flow
  diagrams; status summaries become visual dashboards
- Every section that can be shown visually, is

## Visuals

Visuals are not decoration — they create a better dynamic between
human and machine, and they are soothing to the mind.

A report without visuals is incomplete. Default to visual
representation; fall back to text only when the content is
irreducibly textual.

Charts, diagrams, status indicators, and flow illustrations are
preferred over tables, lists, and prose for any content that has
structure.

## Authoring

The main flow writes the Markdown report with its findings. It does
not concern itself with presentation. The report carries:

- The substance: what was found, what was decided, what remains
- Data in tabular or list form — the rendering subflow decides how
  to visualize it
- Section structure — the rendering subflow preserves it

The main flow dispatches the rendering subflow and returns the
artifact link to the psyche.
{% endif %}

{% if codex %}
## Codex

Web report rendering is not yet available in Codex. The main flow
authors the Markdown report in `FLOW_DIRECTORY/reports/` and
presents its findings in the response.

When Codex infrastructure supports artifact-equivalent rendering,
this section will be replaced with the rendering procedure.
{% endif %}
```

### What this skill changes

Without it: the psyche must say "make me a web report with visuals" every time.

With it: any flow that produces a report naturally authors Markdown and dispatches a rendering subflow that creates an SVG-rich web artifact — the psyche's preferred experience — without being asked.

---

## Visual Summary Data

### Deployment Timeline

```
Date        Event                                          Status
2026-08     Codex 0.152→0.153, ChatGPT desktop updated     ✓
2026-08     Zeus CompleteHost deploy 158                    ✗ BuilderUnreachable
2026-08     Orchestrate 0.29.0 deployed                    ✓
2026-08     claude-answers 0.5.0 deployed                  ✓
2026-08     curriculum-deploy 0.5.0 deployed               ✓
2026-09     Zeus deploys 165+167 (hostname fix)            ✓
2026-09     Protos layers + Ethos Declaration               ✓
2026-09     Guard instructions removed                      ✓
```

### Branch Health

```
Category          Count   Action Needed
Active branches   2       1 cherry-pick/delete, 1 delete
Stashes           2       1 review, 1 drop
Preserve          7       None (archival)
Worktrees         1       Main only — clean
```
