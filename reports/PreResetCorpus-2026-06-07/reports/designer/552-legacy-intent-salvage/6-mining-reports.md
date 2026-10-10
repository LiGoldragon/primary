---
title: 552/6 — Legacy intent salvage — reports.nota mining
role: designer
variant: Audit
date: 2026-06-07
topics: [intent, spirit, intent-maintenance, legacy-nota, reports, reporting]
description: |
  Finder report for the reports.nota legacy file (24 records). Mines for
  CORE, durable, not-too-specific design intent genuinely AT RISK of loss on
  deletion. Two surviving candidates; the rest already deeply preserved.
---

# 552/6 — Legacy intent salvage — reports.nota mining

## Scope

Scanned `reports.nota` — 24 records (read from the date-stripped
`/tmp/intent-text/reports.txt`). This file is the pre-Spirit substrate for the
chat-vs-report discipline, report-naming convention, report supersession /
versioning, and a cluster of cross-lane operator-direction working orders.

The reporting domain is one of the most thoroughly preserved areas in the
workspace: `skills/reporting.md`, `skills/report-naming.md`,
`skills/context-maintenance.md`, AGENTS.md §"Reports go in files", and roughly
40+ deployed Spirit records under the `reports` / `reporting` topics already
carry the chat-vs-report split, the path-not-number rule, the v2/v3
versioning rule, write-new-delete-old supersession, commit-before-delete,
recency-prevails, agglomeration, and the topic-prefix filename convention.
Almost every record fails criterion 3 (already preserved). Two ideas fell
through the cracks.

## Salvage candidates

### 1. Don't manufacture pseudo-gaps — distinguish real undecided gaps from things the psyche already stated or implied

- **Kind:** Constraint
- **Proposed topics:** `intent-clarification`, `open-question-leans`,
  `gap-filling`, `human-facing`, `agent-discipline`
- **Proposed description:** When surfacing gaps in user intent or open
  questions, do not promote to a gap something the psyche already stated or
  clearly implied just because the wording was loose. Pedantically restating
  the obvious as an open decision signals the agent is not reading carefully.
  Distinguish a REAL gap — where a decision is genuinely undecided — from a
  pseudo-gap that only needs contextual reading of what the psyche already
  conveyed.
- **Certainty:** High (legacy Maximum, but the verbatim is a single sharp
  state-reaction; the general rule is durable but I will not inflate to
  Maximum, which is reserved for universal founding rules).
- **Supporting verbatim:** [this is a stupid comment; of course im talking
  about a per-derivation-copy. Im not a fucking idiot!] — reacting to an
  audit that listed an already-implicit framing as a "gap."
- **Preservation check:** Queried Spirit `(Partial [intent-clarification
  clarity communication])` and `(Partial [intent-clarification open-question
  gate])` — grep on the results for `gap / obvious / pedantic /
  already-stated / loose / real-decided` returned EMPTY. Grepped
  `skills/intent-clarification.md` for `real gap / pseudo / genuinely
  undecided / already implied / spurious / manufactured` — EMPTY. The skill
  covers "when to ask vs proceed" and "surface the gap concretely" but the
  inverse discipline (don't fabricate a gap from something already conveyed)
  is absent. Also grepped ESSENCE / AGENTS / INTENT / skills for
  `pseudo-gap / pedantic / restate / already stated / insulting` — only
  unrelated naming-ancestry "restate" hits.
- **At-risk rationale:** This is the quality-of-gap rule, distinct from the
  well-preserved "give the question enough substance" rule. Without it the
  workspace has no guidance against the common failure of inflating an audit
  with pseudo-gaps. Lost entirely on deletion.

### 2. Actions are taken, not announced — replace "ready to X" workflow-state phrasing with the action itself or a specific named question

- **Kind:** Correction
- **Proposed topics:** `chat`, `narration-vs-action`, `agent-discipline`,
  `human-facing`, `workflow-state`
- **Proposed description:** When the agent would write "ready to close",
  "ready to merge", "ready to ship", or similar bureaucratic workflow-state
  phrasing in chat, it instead either DOES the action itself (close the bead,
  merge the branch) or asks a specific question naming the choice.
  "Ready to X" with neither action nor a clarifying question is empty noise:
  it leaves the psyche guessing whether the agent is reporting status, asking
  permission, or asking the psyche to do the action. The indirection compounds
  when paired with a bare opaque identifier.
- **Certainty:** High (legacy Maximum; the general positive rule "actions are
  taken, not announced" is durable — High is the honest read).
- **Supporting verbatim:** [saying bead primary HJ63 is ready to close doesn't
  fucking tell me anything ... Are you asking me if you should close a bead
  that should be closed? ... if it's supposed to be closed, you should close
  it.]
- **Preservation check:** Queried Spirit `(Partial [narration-vs-action chat
  agent-behavior])` and `(Partial [human-facing chat agent-discipline
  agent-behavior])` — grep for `ready / announce / take-the-action / empty
  noise / workflow-state / bureaucratic` returned EMPTY except `waz6`, which
  is the narrower "edit a fresh report directly instead of narrating I-should-
  edit-it" rule. Grepped `skills/reporting.md` / `keep-working.md` /
  `human-interaction.md`: reporting.md has "don't pre-announce what you're
  about to do" (process-narration) and keep-working.md has "don't narrate
  should-I-keep-going" — both adjacent but NEITHER covers the specific
  positive rule that workflow-completion phrasing ("ready to close/merge/ship")
  must resolve to an action OR a named question.
- **At-risk rationale:** The opaque-identifier half of this record's failure
  mode is already an AGENTS.md hard override; the workflow-state-phrasing half
  is NOT preserved anywhere. The sharpened positive rule (act, or ask a
  specific question — never announce "ready") is the load-bearing salvage and
  would be lost on deletion.

## Already preserved / dropped

Confirmed preserved (safe to delete with the file); the 22 dropped records and
where their substance already lives:

- **Chat-vs-report split, user-attention budget** (records 1, 8, 9, 10) —
  AGENTS.md §"Reports go in files; chat is for the user", `skills/reporting.md`,
  Spirit `k24p` (3-7 items, three categories), `[1kfk]` / `g9oc` / `ggyd`
  (full report PATH in chat).
- **No dates in report filenames; commit history records when** (record 2) —
  `skills/reporting.md` ("Commit timestamps already record when each ...").
- **v2/v3 iteration suffix + write-new-delete-old supersession** (records 3,
  16) — Spirit `q9iz` / `[17jp]`, `skills/reporting.md`, `skills/report-naming.md`.
- **Edit ARCHITECTURE.md in place rather than write a report for current-state
  truth; act don't narrate** (record 4) — Spirit `waz6`,
  `skills/architecture-editor.md`, `skills/reporting.md`.
- **Full report PATH in chat, not bare numbers** (records 5, 8, 9, 10) —
  Spirit `[1kfk]` / `g9oc` / `ggyd`, AGENTS.md, `skills/human-interaction.md`.
- **Recency: give more credit to more recent reports on contradiction**
  (record 6) — `skills/context-maintenance.md` §2 "Topic-recency ranking" +
  §"Recent intent prevails", Spirit `[3n4c]` / record 921.
- **Report names name the subject, not conversational ancestry** (record 11) —
  `skills/reporting.md` ("The topic names the report's subject, not its
  conversational ancestry. Avoid names like response-to-..."), ESSENCE.md
  ancestry rule.
- **Never delete an uncommitted report; commit-then-delete** (record 12) —
  Spirit `pjib` ("Reports not in the working tree live in the commit tree"),
  `skills/reporting.md`.
- **Report-naming must hit disk as a skill, not just intent; basic-naming as
  its own skill** (record 13) — manifested as `skills/report-naming.md` (the
  rule literally produced the skill it asked for).
- **Report sweeps remove stale reports after substance committed; topic-scoped
  fresh reports** (record 14) — Spirit `[3k0j]` / `f1l3` / `[0r17]` / `kgqr`,
  `skills/context-maintenance.md` (agglomeration).
- **Questions to the psyche carry inline substance, no bare numbers/locators**
  (record 24) — Spirit `xi3g` / `o7zt`, `skills/reporting.md` §"Questions to
  the user", `skills/human-interaction.md`, AGENTS.md opaque-identifier
  override.
- **Report lanes are owned surfaces; don't edit another lane's reports**
  (record 23) — Spirit `[9o9g]` / `q402`, AGENTS.md §"Roles".
- **Records 17-22** — transient operator working-orders ("analyze report 244",
  "consider report 245-v2", "use 246-v2 as source", "consider a completely
  different engine/repositories"). These are task state, not durable intent
  (they die when the task is erased — fail criterion 1). The one durable
  general idea inside record 20 ("prefer the more elegant long-term logic
  regardless of implementation cost; the better long-term logic always wins")
  is already a deep, multiply-stated workspace principle (ESSENCE.md
  bottom-up-best-shape / disregard-implementation-cost, AGENTS.md
  no-backward-compat override) — preserved.

Net: `reports.nota` is safe to delete once the two candidates above are
recorded (psyche-gated). The remaining 22 records are either already
preserved in the live guidance/Spirit layer or are transient task orders.
