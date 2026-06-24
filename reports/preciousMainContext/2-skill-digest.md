# Skill digest — five psyche/intent-facing skills (prune review)

Joint review of the five most-essential, most-overlapping intent-facing skills,
toward a precious-main-context model where a dispatcher selects skills by **name +
manifest description alone**. The five: `intent-alignment` (117 lines),
`human-interaction` (115), `intent-log` (420), `spirit-cli` (465),
`session-lanes` (145). Two sibling skills they defer to — `intent-clarification`
(71) and `intent-maintenance` (206) — were read to confirm redirect targets
genuinely own the deferred material. They do.

## Bottom line

The biggest waste is `human-interaction` and `intent-log`: roughly half of
`human-interaction` restates AGENTS.md hard overrides or sibling-owned taxonomy,
and `intent-log` re-enumerates the five kinds three times and pulls in
manifestation + maintenance + spirit-cli material that has its own skills. The
single highest-value cut is **`human-interaction` shrinks from 14 sections to
~6** by deleting four AGENTS.md-duplicate sections outright (they ship every
session in the contract already) and collapsing four sibling-owned sections to
pointers. `spirit-cli` is mostly load-bearing reference but carries ~120 lines of
misplaced daemon/migration/render material that an intent-capturing agent never
reads.

## Cross-skill overlaps (the load-bearing finding)

Same guidance restated across two or more of the five files. Each row: where it
lives, who should own it, delete-from elsewhere.

| # | Duplicated content | Locations | Owner | Action |
|---|---|---|---|---|
| O1 | The five recordable kinds (Decision / Principle / Correction / Clarification / Constraint) enumerated as a list/table | `intent-log` L36, L85-98, L197; `human-interaction` L22-32; `spirit-cli` L102 | `intent-log` (the canonical taxonomy section) | Cut the `human-interaction` table (L22-32) to a one-line pointer; `intent-log` keeps ONE enumeration (the gate at L36 plus the Recordable-kinds prose) and drops the third copy; `spirit-cli` keeps only the inline `# Kind ∈ {…}` comment. |
| O2 | "Clarification is an edit of the target record, not a sibling Record" | `intent-log` L47-54, L91-96, L358; `human-interaction` L29; `spirit-cli` L121-126; **and the whole of `intent-maintenance` L3-31** | `intent-maintenance` (owns the full edit sequence) | Each of the three files keeps ONE crisp sentence + pointer to `intent-maintenance`; delete the repeated restatements (esp. `intent-log` says it three times). |
| O3 | Certainty-vs-importance: "don't inflate certainty to encode importance; default Medium; full Magnitude ladder" | `intent-log` L249-325 (full); `human-interaction` L32; `spirit-cli` L104-105, L368-374 | `intent-log` (the two-axis model + ladder rubric) | `human-interaction` L32 → pointer (already points there); `spirit-cli` L368-374 → cut to the one storage fact (`Zero` = removal candidate) since the ladder semantics duplicate L104-105 and `intent-log`. |
| O4 | Spirit CLI invocation mechanics: inline-NOTA vs file arg, shell-double-quote boundary, no-file-fallback blocker | `spirit-cli` L17-46 (full); `intent-log` L228-247 | `spirit-cli` (the invocation reference) | Cut `intent-log` L228-247 to a 2-line "record goes through `spirit`; mechanics in `spirit-cli`" pointer; keep only the no-legacy-fallback sentence if not already in the gate. |
| O5 | Record/Entry NOTA wire shape (seven positional fields + Justification) | `intent-log` L187-226; `spirit-cli` L76-106 | `spirit-cli` (closest to deployed source, with the read-from-source instructions) | `intent-log` may keep its annotated block as the capture-side reference but should explicitly defer field-truth to `spirit-cli` (it already flags drift at L225); don't grow both. Acceptable partial overlap — flag, don't force-merge. |
| O6 | "Forwarded prompts — gap-check, don't blind-duplicate" | `human-interaction` L34-43; **AGENTS.md hard override (ships every session)** | AGENTS.md | Delete `human-interaction` L34-43 entirely — the contract already carries it verbatim-in-substance. |
| O7 | "Every subagent dispatch is non-blocking / `run_in_background: true`" | `human-interaction` L77-81; **AGENTS.md hard override** | AGENTS.md | Delete `human-interaction` L77-81 entirely. |
| O8 | "Designer feature branches; operator owns main" | `human-interaction` L95-97; **AGENTS.md hard override**; `main-next` + `feature-development` skills | AGENTS.md / `feature-development` | Delete `human-interaction` L95-97 entirely (zero relation to the human boundary). |
| O9 | "No raw `/nix/store/HASH` paths" | `human-interaction` L99-101; **AGENTS.md hard override**; `nix-usage` skill | AGENTS.md / `nix-usage` | Delete `human-interaction` L99-101 entirely. |
| O10 | "Reports go in files; chat is for the user" + the 3-7-items chat shaping | `human-interaction` L65-75, L103-105; `intent-alignment` L109-111; **AGENTS.md "Reports go in files" section**; `reporting` skill | AGENTS.md + `reporting` for the report/chat split; `human-interaction` keeps ONLY the psyche-boundary chat shaping (3-7 items, chat-as-paraphrase) | Delete `human-interaction` L103-105 (pure AGENTS.md dup); keep L65-75 but trim the visuals-go-in-reports clause to a pointer. |
| O11 | "When intent is unclear, ask — don't infer" + the do/don't-ask lists + `AskUserQuestion` | `human-interaction` L45-63; **the whole of `intent-clarification`** | `intent-clarification` | Cut `human-interaction` L45-63 to a one-line pointer (it already cites `intent-clarification` at L63). |
| O12 | ResolveClarification fold mechanic (field-by-field) | `spirit-cli` L176-228; **`intent-maintenance` L33-59** | `intent-maintenance` for the discipline; `spirit-cli` keeps only the call shapes | Move the discipline prose out of `spirit-cli` L176-200; keep the `Clarify`/`Supersede`/`Retire`/`ResolveClarification` call-shape snippets. |
| O13 | Discipline-vs-lane split + retirement of fixed role-lanes | `session-lanes` L5-25; **AGENTS.md "Disciplines and lanes" section** | AGENTS.md for the concept | `session-lanes` collapses L5-25 to one tight paragraph + the mermaid; the contract already explains the split every session. |
| O14 | Drain → three fates (intent / work / abandon) | `session-lanes` L101-120 and L124; **AGENTS.md "A session lane runs fresh, drains" section** | AGENTS.md + the actionable retire steps in `session-lanes` L122-145 | Collapse `session-lanes` L101-120 to a one-line pointer; the three-fates list is duplicated both in AGENTS.md and again at L124 of the same file. |

## Merge / split (atomicity)

The precious-context goal is **one skill = one atom** so name+description select it.

### Split candidates (a skill carrying two+ unrelated atoms)

- **`human-interaction` is the worst non-atom of the five.** Its manifest line
  advertises five unrelated topics ("load intent skills, capture intent first,
  shape chat, dispatch subagents, frame real-world tests, report back") — the
  description is a grab-bag *because the body is*. The atomic core is exactly
  three things: (1) keep the intent skills loaded fresh, (2) capture intent
  before any other output, (3) shape chat replies toward the psyche. Everything
  else is misplaced:
  - L83-93 (real-world testing conditions; unblock-the-blocker-in-test) → move to
    `autonomous-agent` or a testing skill. Pure work-execution, no human-edge
    content. These two sections are the reason a dispatcher would wrongly load
    `human-interaction` for non-psyche work.
  - L95-101, L107-109 (designer/operator branches; nix paths; parallel-lane
    model) → already AGENTS.md / `feature-development` / orchestrate skills.
  - After cuts, `human-interaction` is a clean ~50-line atom.

- **`spirit-cli` carries three off-topic atoms** that an agent invoking the CLI
  never reads:
  - L346-366 "Rendering public intent snapshots" — `spirit-render` is a
    *separate companion binary* not guaranteed installed; it is not the `spirit`
    CLI. → split to its own tiny skill or fold into an intent-snapshot skill.
  - L397-408 "Daemon startup is binary-only" — daemon (not CLI) discipline;
    `component-triad` territory + an AGENTS.md hard override.
  - L410-453 "Substrate migration discipline" + "No dual-writing" — a Rust
    migration-crate authoring pattern. → move to a migration/rust skill.
  - These ~120 lines are ~26% of the file and have no bearing on writing a
    `spirit` call. Cutting them sharpens the description to exactly "invoke the
    CLI."

- **`session-lanes` carries a report-authoring atom** at L92-99 (fresh-context
  pickup, bead dependency graph, supersede-and-delete predecessor) → belongs in
  `reporting` / `report-naming`, not the lane-lifecycle skill.

- **`intent-alignment` L86-94** (don't silently choose defaults for
  authority/priority/scope/safety/privacy/certainty/kind; don't launder a guess
  through the guardian) is Spirit-metadata discipline → belongs in `intent-log`.
  Small but it's a foreign atom inside an alignment skill.

### Merge candidates

- **No two of the five are one atom — do not merge any of the five.** They form a
  clean ladder: `intent-alignment` (pre-capture interview) → `human-interaction`
  (the psyche boundary + capture-first) → `intent-log` (what counts as intent +
  classification) → `spirit-cli` (how to invoke). Each is a distinct decision a
  dispatcher makes. Merging would *reduce* atomicity.
- The genuine merge opportunity is **outside the five**: O2's clarification-is-an-
  edit guidance is split across `intent-log`, `spirit-cli`, AND
  `intent-maintenance`. Consolidate the *discipline* in `intent-maintenance` and
  leave one-sentence pointers in the other two.

## Prune list (prioritized, concrete cuts)

Ordered by value: delete-outright AGENTS.md/sibling duplicates first, then
misplaced atoms, then internal repetition, then low-value detail.

| Pri | Skill | Section | Lines | Verdict | Action |
|---|---|---|---|---|---|
| 1 | human-interaction | Forwarded prompts | L34-43 | repetitive | DELETE — AGENTS.md hard override ships it every session. |
| 1 | human-interaction | Subagent dispatch non-blocking | L77-81 | repetitive | DELETE — AGENTS.md hard override. |
| 1 | human-interaction | Designer branches / operator main | L95-97 | misplaced | DELETE — AGENTS.md override + `feature-development`. |
| 1 | human-interaction | No raw /nix/store paths | L99-101 | misplaced | DELETE — AGENTS.md override + `nix-usage`. |
| 1 | human-interaction | Reports go in files | L103-105 | repetitive | DELETE — AGENTS.md "Reports go in files" + `reporting`. |
| 2 | human-interaction | Real-world testing / unblock-in-test | L83-93 | misplaced | MOVE to `autonomous-agent` or a testing skill. |
| 2 | human-interaction | Parallel-implementation lane model | L107-109 | misplaced | MOVE to `double-implementation-strategy` / orchestrate. |
| 2 | human-interaction | Ask the psyche when unclear | L45-63 | misplaced | CUT to 1-line pointer → `intent-clarification` (owns it fully). |
| 2 | human-interaction | The five kinds of intent | L22-32 | repetitive | CUT to 1-line pointer → `intent-log`. |
| 2 | spirit-cli | Substrate migration + no dual-writing | L410-453 | misplaced | MOVE to a migration/rust skill. |
| 2 | spirit-cli | Daemon startup binary-only | L397-408 | misplaced | CUT to pointer → `component-triad` (already an AGENTS.md override). |
| 2 | spirit-cli | Rendering snapshots (spirit-render) | L346-366 | misplaced | SPLIT to its own skill (separate binary). |
| 2 | intent-log | Capture manifests into INTENT.md | L147-158 | misplaced | CUT to pointer → `intent-manifestation` / `repo-intent`. |
| 2 | intent-log | When a working order slips in | L179-185 | misplaced | CUT to pointer → `intent-maintenance`. |
| 2 | intent-log | Recording goes through Spirit CLI | L228-247 | misplaced | CUT to pointer → `spirit-cli` (keep no-legacy-fallback line). |
| 2 | intent-alignment | How to use recommendations | L86-94 | misplaced | MOVE Spirit-metadata defaults guidance → `intent-log`. |
| 2 | session-lanes | Reports map to the lane | L92-99 | misplaced | CUT report-authoring para to pointer → `reporting`/`report-naming`. |
| 3 | intent-log | Recordable kinds (3rd enumeration) | L83-105 | repetitive | Keep one enumeration; drop the Clarification-is-edit re-restatement. |
| 3 | intent-log | Non-recordable shapes | L107-118 | repetitive | Tighten — restates the gate's No-capture + brainstorming clause. |
| 3 | intent-log | If the gate says Record | L358-366 | repetitive | Tighten — recaps gate + certainty + L72 query instruction. |
| 3 | intent-log | What this skill is NOT for | L395-402 | repetitive | Tighten — restates L7-8, L23-26. |
| 3 | spirit-cli | Certainty and importance | L368-374 | repetitive | CUT to the one storage fact; ladder dups L104-105 + `intent-log`. |
| 3 | spirit-cli | Encoding rules | L65-73 | repetitive | CUT to pointer → `nota-design` (cited at L460) + AGENTS.md bare-atom override. |
| 3 | session-lanes | Discipline-vs-lane split (prose) | L5-25 | repetitive | Collapse to one paragraph + keep the mermaid. |
| 3 | session-lanes | Lifecycle smart-zone/fleet/drain | L101-120 | repetitive | Collapse to 1-line pointer → AGENTS.md; three-fates dup'd at L124. |
| 4 | intent-log | Forward — persona-mind migration | L404-411 | useless | DELETE — self-described "no work yet; this signposts." Pure future note. |
| 4 | intent-alignment | What this skill is for (intro) | L5-18 | repetitive | Tighten — restates the AGENTS.md override + manifest near-verbatim. |
| 4 | intent-alignment | What to ask about (8-item checklist) | L62-77 | low-value | Tighten — generic interview coverage; L73-74 re-covers the graph section. |
| 4 | intent-log | Citing intent in prose | L368-393 | low-value | Consider moving to `intent-manifestation`/`reporting`; CommonMark detail rarely changes behavior. |
| 4 | intent-log | Privacy gate before recording | L77-81 | low-value | Keep as inline gate reminder; it correctly defers to `privacy`. |
| 4 | spirit-cli | Guardian discipline block | L108-126 | low-value | Tighten — restates daemon-enforced rejection enum; agent rarely pre-empts beyond "supply verbatim." |
| 4 | spirit-cli | ResolveClarification deep detail | L201-228 | low-value | Tighten — field-by-field schema narration; read from source per L48-63. |

Sections marked **keep** in the per-skill digests (the graph taxonomy and
interview shape in `intent-alignment`; the gate, affirmative-framing remand,
one-capturer rule, ladder, and referent discipline in `intent-log`; invocation +
recording + observing in `spirit-cli`; how-an-agent-knows-its-lane + registration
+ retirement in `session-lanes`; load-intent-skills + capture-first + chat-shaping
in `human-interaction`) are the genuine atoms and are not listed for cutting.

## Description quality (name+description-only selection test)

Does each `skills.nota` manifest line suffice for a dispatcher to load/no-load
without reading the body?

| Skill | Sufficient? | Verdict |
|---|---|---|
| `intent-alignment` | **Yes** | Names trigger ("any request not already crisp enough to execute"), method (one focused question per turn in plain prose), four targets, timing, and the crisp-directive escape hatch. Selectable from the string alone. Minor omission (the interview-question template) is body mechanics, not a selection criterion. No change needed. |
| `intent-log` | **Mostly** | Names the load triggers (record intent, five-kind record, capture-vs-ask, clarifications-via-edits, read-fresh). Gap: reads capture-only, undersells the certainty-calibration and citation material, so a "how certain should this be" or "how do I cite intent in a report" turn might not load it. Improve. |
| `human-interaction` | **No** | The grab-bag description ("dispatch subagents, frame real-world tests, report back") advertises sibling-owned topics and would cause **over-loading** — a dispatcher pulls it for non-psyche testing/dispatch work. It's the symptom of the non-atomic body. Rewrite (after the body is cut per the prune list). |
| `spirit-cli` | **Yes** | Names exactly what it is: invoke the CLI to capture/query, RecordRequest shape, operations, query shape, inline-vs-file, read-wire-from-source. Accurate today. (After cutting the render/daemon/migration atoms the description gets *more* accurate, not less.) |
| `session-lanes` | **Yes** | States the core concept (lane = fresh session named for intent; discipline = metadata) and a trigger list (opening/registering/naming/draining) that maps onto the body headings. Selectable from the string. No change needed. |

Proposed improved descriptions for the two that fall short:

- **`intent-log`** → *"How to decide what counts as recordable psyche intent and
  record it through Spirit — the gate (capture / ask / edit / no-capture), the
  five recordable kinds, the positional NOTA record shape,
  certainty-versus-importance calibration, and citing intent in prose. Read fresh
  before any Spirit capture."*
- **`human-interaction`** (assuming the body is trimmed to its atom) → *"The
  psyche-facing boundary: keep the intent skills loaded fresh, capture intent
  before any other output, and shape chat replies (3-7 substantive items,
  paraphrasing a report) toward the human. Load when your lane talks with the
  psyche."*

## Full skills.nota inventory (for planning next review batches)

All 70 skills from the manifest, with line counts (sub-files under `rust/`
included). Tier in parens. The five under review are marked ★; their two
redirect siblings ☆.

### Meta (intent / human-edge) — the cluster this review opened

| Skill | Tier | Lines | Description (manifest) |
|---|---|---|---|
| ★ human-interaction | Apex | 115 | Psyche-facing human boundary: load intent skills fresh, capture intent first, shape chat, dispatch subagents, frame tests, report back. |
| ★ intent-alignment | Apex | 117 | Default discipline for an interactive agent: align on goal/scope/success-checks/dependency-graph via one focused question per turn before planning/building. |
| ★ intent-log | Topic | 420 | Record explicit psyche intent through Spirit: five-kind positional NOTA record, capture-vs-ask, routing clarifications via edits. Read fresh before capture. |
| ★ spirit-cli | Topic | 465 | Invoke the deployed Spirit CLI to capture/query intent — RecordRequest shape, operations, query shape, inline-vs-file, read wire from source. |
| ★ session-lanes | Mechanism | 145 | Lane = fresh work-session identity named for intent, carrying a discipline as metadata. Read when opening/registering/naming/draining a lane. |
| ☆ intent-maintenance | Mechanism | 206 | Sweep the Spirit log: fold standalone clarifications via ResolveClarification, run supersession, verify against current state. |
| ☆ intent-clarification | Topic | 71 | Ask the psyche when intent is unclear/absent/contradicted, offering structured options instead of inferring. |
| autonomous-agent | Mechanism | 223 | When to act vs ask within work, and the claim/work/close/release loop. Pairs with human-interaction. |
| context-maintenance | Mechanism | 368 | Everyday single-lane sweep of reports/conversation, migrating substance to permanent homes. |
| context-maintenance-deep | Mechanism | 65 | Heavier maintenance: cross-lane sweeps, cross-lane meta-report dir, lane retirement. |
| repo-intent | Keystroke | 108 | Why per-repo INTENT.md is first/most-important; agent prose 100% backed by psyche statements, read on entry. |
| intent-manifestation | Mechanism | 146 | Walk Spirit records and manifest intent into the right guidance file (ESSENCE/AGENTS/INTENT/skills), quoting verbatim. |
| keep-working | Keystroke | 49 | Mid-task psyche info-injection is not a stop signal: absorb, capture durable intent, keep working. |

### Role / discipline (Apex)

| Skill | Tier | Lines |
|---|---|---|
| operator | Apex | 220 |
| designer | Apex | 580 |
| schema-designer | Apex | 108 |
| system-operator | Apex | 228 |
| system-maintainer | Apex | 68 |
| poet | Apex | 76 |
| editor | Apex | 61 |
| assistant | Apex | 34 |
| counselor | Apex | 23 |

### Architecture

| Skill | Tier | Lines |
|---|---|---|
| component-triad | Apex | 1160 |
| structural-forms | Apex | 168 |
| contract-repo | Topic | 571 |
| micro-components | Topic | 205 |
| actor-systems | Topic | 624 |
| architectural-truth-tests | Topic | 491 |
| engine-analysis | Topic | 85 |
| engine-report | Topic | 127 |
| language-design | Topic | 282 |
| library | Topic | 155 |
| subscription-lifecycle | Topic | 229 |

### Craft

| Skill | Tier | Lines |
|---|---|---|
| abstractions | Keystroke | 253 |
| enum-contact-points | Apex | 335 |
| naming | Keystroke | 367 |
| secrets | Keystroke | 150 |
| privacy | Keystroke | 99 |
| workspace-vocabulary | Topic | 80 |
| beauty | Keystroke | 81 |
| push-not-pull | Keystroke | 59 |
| reporting | Keystroke | 847 |
| versioning | Keystroke | 101 |
| typed-records-over-flags | Keystroke | 117 |
| prose | Topic | 585 |

### Programming (incl. rust/ sub-files)

| Skill | Tier | Lines |
|---|---|---|
| kameo | Topic | 790 |
| rust-discipline | Topic | 125 |
| rust-methods (rust/methods.md) | Topic | 485 |
| rust-errors (rust/errors.md) | Topic | 43 |
| rust-storage-and-wire (rust/storage-and-wire.md) | Topic | 189 |
| rust-parsers (rust/parsers.md) | Topic | 99 |
| rust-crate-layout (rust/crate-layout.md) | Topic | 148 |
| nix-discipline | Topic | 329 |
| nix-usage | Topic | 94 |
| mermaid | Mechanism | 320 |
| stt-interpreter | Mechanism | 149 |

### Workflow

| Skill | Tier | Lines |
|---|---|---|
| architecture-editor | Mechanism | 358 |
| nota-schema-docs | Mechanism | 79 |
| nota-design | Topic | 334 |
| nota-comments | Topic | 142 |
| jj | Mechanism | 416 |
| testing | Mechanism | 243 |
| feature-development | Mechanism | 177 |
| double-implementation-strategy | Topic | 86 |
| beads | Mechanism | 255 |
| repository-management | Mechanism | 164 |
| skill-editor | Mechanism | 216 |
| report-naming | Mechanism | 51 |
| workspace-update-report | Mechanism | 134 |
| main-next | Keystroke | 35 |
| main-feature-integration | Mechanism | 26 |

### Suggested next review batches

- **Batch 2 — the rest of the Meta cluster** (`autonomous-agent`,
  `context-maintenance`, `context-maintenance-deep`, `repo-intent`,
  `intent-manifestation`, `keep-working`, plus the two siblings already read
  here). High overlap risk with this batch; closes the intent/meta surface.
- **Batch 3 — the always-loaded heavyweights** (`reporting` 847, `naming` 367,
  `abstractions` 253, `beauty`, `privacy`, `secrets`, `versioning`,
  `typed-records-over-flags`, `push-not-pull` — all Keystroke, all in the
  precious path). `reporting` at 847 lines is the single largest Keystroke skill
  and overlaps AGENTS.md's report rules heavily.
- **Batch 4 — Apex role + architecture giants** (`component-triad` 1160, `designer`
  580, `actor-systems` 624, `contract-repo` 571) — biggest bodies, but topic-tier
  so loaded on demand, lower precious-context urgency.
