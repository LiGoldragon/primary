# Session handoff — 2026-05-07

Date: 2026-05-07
Author: Claude (designer)

A wrap-up of designer-side work in `~/primary` and across
the workspace on 2026-05-07. Written for context compaction
and for the next session (mine or another agent's) to pick
up cleanly.

---

## What changed at the workspace level

Substance promoted upstream from this session's work (now
canonical in skills / ESSENCE / protocols, no longer
reportable-only material):

### Polling is forbidden — ESSENCE-level rule

- `~/primary/ESSENCE.md` §"Polling is forbidden" replaces
  the prior "Push, never pull" section. Tightened
  language: *"forbidden, not discouraged."* The
  partner-keeps-texting metaphor names the failure mode.
  Three named carve-outs: reachability probes,
  backpressure-aware pacing, deadline-driven OS timers.
- Escalation rule: when no push answer is found, escalate
  to the next level of design responsibility, ultimately
  to the human. Falling back to a poll is never the
  answer.
- `~/primary/skills/push-not-pull.md` now references
  ESSENCE for the rule itself; carries only the practical
  "how to apply" + escalation procedure + recognition of
  common pull-shaped traps.

### Four-role orchestration

- Roles: `operator`, `designer`, `system-specialist`,
  `poet`. Each has its own lock file, report subdirectory,
  natural primary scope.
- `~/primary/tools/orchestrate` refactored from binary
  peer-check to N-role iteration. Operator added
  `beads_scope` rejection — `.beads/` is shared
  coordination state, never claimed.
- `~/primary/protocols/orchestration.md`,
  `~/primary/AGENTS.md`,
  `~/primary/skills/system-specialist.md`,
  `~/primary/skills/poet.md` updated.

### Reporting discipline as a workspace skill

- `~/primary/skills/reporting.md` is the canonical home
  for: when to write a report vs answer in chat, the
  *always-name-paths* rule, role-subdir ownership +
  claim-flow exemption, prose-plus-visuals medium, the
  `<N>-<topic>.md` filename convention, present-tense
  framing, when report substance becomes durable.
- Required reading per `~/primary/AGENTS.md` (added
  alongside `autonomous-agent.md` and `skill-editor.md`).
- §"Hygiene" rules: soft cap of 12 reports per role
  subdir, supersession-deletes-old, periodic review with
  the four-action decision table, **numbers not reused
  after deletion** (gaps in listings are visible signals
  that something was retired).
- Reports renamed from `YYYY-MM-DD-<topic>.md` to
  `<N>-<topic>.md`; per-role independent counter; no
  leading zeros; sort with `ls -v` or
  `sort -t- -k1,1n`.

### `jj` is the version-control tool; raw `git` is forbidden as a daily commit tool

- `~/primary/skills/version-control.md` renamed to
  `~/primary/skills/jj.md`. References updated workspace-wide
  (`AGENTS.md`, `lore/AGENTS.md`,
  `skills/autonomous-agent.md`, `skills/nix-discipline.md`).
- Two named git escape hatches: HTTPS→SSH remote fix,
  divergence resolution. Anything else uses jj.
- §"Never let jj open an editor": always use `-m '<msg>'`
  inline. Table maps every description-taking jj command
  to its inline form. `EDITOR=true` shims are anti-patterns.
- §"Partial commits — `jj split` with paths": canonical
  idiom is `jj split -m '<msg>' <paths>`; the working
  copy retains the un-split paths for the peer agent.

### Persistent state — redb + rkyv

- `~/primary/skills/rust-discipline.md` §"Persistent state
  — redb + rkyv" is the new canonical rule. Persistent
  component state lives in redb with rkyv-archived values.
  NOTA stays the wire/projection format. Named exceptions:
  lock-file projections, configs, reports, interchange
  artifacts. Don't pre-abstract a shared storage crate;
  lift after 2–3 components crystallize.
- The "EDB" acronym was operator-coined shorthand, dropped
  workspace-wide. Spell out `redb + rkyv` in prose.

### Pruning + supersession

- 11 stale reports deleted across the session (designer
  1, 2, 3, 5, 6, 7, 8, 10, 11; operator 6; top-level 2).
  Cross-references in survivors updated before deletion.

---

## Active reports

### Top-level (`~/primary/reports/`)

| # | Report | Why it stays |
|---|---|---|
| 1 | `1-gas-city-fiasco.md` | Foundational postmortem; later work points back as "don't reintroduce these failures." |

### Designer (`~/primary/reports/designer/`)

| # | Report | Why it stays |
|---|---|---|
| 4 | `4-persona-messaging-design.md` | Destination architecture for the persona daemon; reducer + plane structure. Load-bearing from reports 12, 14, 15. |
| 9 | `9-cluster-config-audit.md` | Referenced by system-specialist's report 1 (audit lineage on the all-fields-explicit cascade). Don't delete while that link is live. |
| 12 | `12-no-polling-delivery-design.md` | Push primitives + indefinite-deferral + TTL-as-only-timer-carve-out. Cited from ESSENCE-derived discipline. |
| 13 | `13-niri-input-gate-audit.md` | Audit of operator's report 7; operator's work is in flight. |
| 14 | `14-persona-orchestrate-design.md` | Design for `primary-jwi` (operator implements). Lineage of orchestration → typed Persona component. |
| 15 | `15-persona-system-plan-audit.md` | Audit of operator's report 8 (persona stack split). Most recommendations now landed in operator's revision. |

### Operator (`~/primary/reports/operator/`)

Active: `1`–`5`, `7`, `8`. Operator owns; not deleted.
Report 6 (prompt-empty-delivery-gate-design) was retired
when 7 (minimal Niri input gate) superseded it.

### System-specialist (`~/primary/reports/system-specialist/`)

| # | Report |
|---|---|
| 1 | `1-nota-all-fields-present-violation.md` (cascade record for `primary-8rc`) |

### Poet

Empty. `.gitkeep` placeholder only.

---

## Beads at handoff

| Bead | Priority | Owner | Status |
|---|---|---|---|
| `primary-8rc` | P1 | operator | **CLOSED** — fix landed (`nota-codec` `333e73a`); cascade through horizon-rs / lojix-cli / goldragon / CriomOS-home. |
| `primary-0ey` | P2 | designer | **CLOSED** — `redb + rkyv` section landed in `skills/rust-discipline.md`. |
| `primary-77l` | **P1** | system-specialist | **OPEN** — migrate `~/git/<repo>` to `/git/github.com/<org>/<repo>` (ghq); 31 duplicate checkouts diverged; agents reading stale code. |
| `primary-8b6` | P2 | system-specialist | OPEN — decouple dark theme + warm screen. |
| `primary-bmy` | P2 | (any agent, incremental) | OPEN — per-repo `skills.md` rollout. Agent-driven, not batched. |
| `primary-jwi` | P3 | operator | OPEN — implement persona-orchestrate per report 14. |

`primary-77l` is the highest-priority unowned bead. Its
description carries the migration recipe, divergence table,
counts (31 dup / 57 ~/git-only / 11 ghq-only), and
watch-outs.

---

## Operator's parallel work landed mid-session

Worth knowing because it shaped this session's context:

- **BEADS-not-claimable rule** propagated to
  `~/primary/AGENTS.md`, `~/primary/tools/orchestrate`
  (with `beads_scope` rejection),
  `~/primary/skills/autonomous-agent.md`,
  `~/primary/protocols/orchestration.md`. `.beads/` is
  shared coordination state, not a lockable scope.
- **`primary-8rc` cascade** — `nota-codec` `Option<T>`
  decode lax-branch removed; horizon-rs / lojix-cli /
  goldragon / CriomOS-home all updated to carry every
  trailing token explicitly. ouranos redeployed.
- **Operator's report 8 revision** — incorporated my
  report 15 recommendations: `persona-orchestrate` named
  as sibling state engine, `persona-system` +
  `persona-system-niri` merge timing, `StorageActor`
  dropped, redb-and-rkyv terminology fixed.

---

## Live design lineage (the load-bearing arc)

```
reports/designer/4-persona-messaging-design.md
    (destination architecture; reducer + planes)
              │
              ├── reports/designer/12-no-polling-delivery-design.md
              │       (push-primitive surface; TTL carve-out)
              │
              ├── reports/operator/8-persona-system-repo-plan.md
              │       (repo split; persona-router / persona-system /
              │        persona-harness / persona-desktop)
              │           │
              │           └── reports/designer/15-persona-system-plan-audit.md
              │                   (recommendations now incorporated)
              │
              ├── reports/operator/7-minimal-niri-input-gate.md
              │       (first concrete implementation slice)
              │           │
              │           └── reports/designer/13-niri-input-gate-audit.md
              │                   (current; operator's work in flight)
              │
              └── reports/designer/14-persona-orchestrate-design.md
                      (sibling state engine for workspace coordination;
                       maps to bead primary-jwi)
```

Reports 4, 12, 13, 14, 15 form the design-and-audit chain
the next session needs. Report 9 sits adjacent for the
system-specialist's audit lineage.

---

## Things to know going forward

1. **Two-checkout drift** — until `primary-77l` lands,
   verify state with `git fetch` (or `jj git fetch`) before
   reading code in any repo. The cascade fix (commit
   `333e73a` in nota-codec) was visible in `~/git/` but not
   in `/git/github.com/...` until I fetched. **Designer
   audits read stale code without warning.** This drift
   ends when the migration completes.

2. **Operator's report 8 is the active stack design.**
   Read it fresh before any work touching
   `persona-router`, `persona-system`, `persona-harness`.
   The plan absorbed my recommendations; my report 15 is
   now mostly retrospective.

3. **`persona-orchestrate` is operator's bead** (`primary-jwi`).
   My design at report 14 is the starting shape. When
   operator picks it up, consider this proposal as the
   foundational reference for the new repo's
   `ARCHITECTURE.md`.

4. **`persona-message-harness.md` skill update is still
   pending** (Phase 1 of the gate report's plan): teach
   the harness about the three-state delivery outcomes
   (delivered / queued / deferred). Operator's territory.

5. **The Niri gate's input-buffer recognizer** needs a
   precise definition before live screen parsing lands.
   Two predicates: *(a) input buffer present?* and
   *(b) contains only prompt chrome with no user
   characters?* Both true → empty. Per-harness recognizer
   in a closed `Harness` enum. See report 13 §6 and
   recommendation 4.

6. **`persona-desktop`** in operator's stack is far from
   the critical path; design it later, not now.

---

## Where to find things — quick map

For an agent picking up cold:

| If you want to know… | Read |
|---|---|
| Workspace intent | `~/primary/ESSENCE.md` |
| How to act autonomously | `~/primary/skills/autonomous-agent.md` |
| How to write/edit a skill | `~/primary/skills/skill-editor.md` |
| How to write a report | `~/primary/skills/reporting.md` |
| How to commit + push | `~/primary/skills/jj.md` |
| Rust discipline (incl. redb + rkyv) | `~/primary/skills/rust-discipline.md` |
| Nix discipline | `~/primary/skills/nix-discipline.md` |
| Push-not-pull (practical) | `~/primary/skills/push-not-pull.md` |
| Role coordination | `~/primary/protocols/orchestration.md` |
| Open beads | `bd list --status open --flat --no-pager` |
| Lock state | `tools/orchestrate status` |

For substantive context on the persona work:

| Topic | Report |
|---|---|
| The destination architecture | `reports/designer/4-persona-messaging-design.md` |
| The push-primitive surface | `reports/designer/12-no-polling-delivery-design.md` |
| The current Niri gate (in flight) | `reports/operator/7-minimal-niri-input-gate.md` + `reports/designer/13-niri-input-gate-audit.md` |
| The repo split (active) | `reports/operator/8-persona-system-repo-plan.md` + `reports/designer/15-persona-system-plan-audit.md` |
| Workspace coordination component | `reports/designer/14-persona-orchestrate-design.md` |

---

## Designer state at handoff

- Designer lock: idle.
- Last commit: report 6 deletion + this handoff (in this
  same change set).
- Open work in flight: none on the designer side.
- Operator and system-specialist have actionable beads;
  designer does not.

---

## Closing note

This session built ~6,000 lines of substantive design +
audit + skill content; pruned ~10 stale reports; promoted
several rules from reports up to ESSENCE / skills / protocol
where they belong; and exposed the parallel-checkout drift
as a P1 bead. The workspace's discipline surface is in
better shape than at session start: polling is forbidden at
the apex; reporting has its own skill with hygiene; jj usage
is tightened; redb + rkyv is the persistence default; the
four-role orchestration is real.

Designer idle on completion; releasing.

---

## See also

- `~/primary/reports/designer/4-persona-messaging-design.md`
- `~/primary/reports/designer/12-no-polling-delivery-design.md`
- `~/primary/reports/designer/13-niri-input-gate-audit.md`
- `~/primary/reports/designer/14-persona-orchestrate-design.md`
- `~/primary/reports/designer/15-persona-system-plan-audit.md`
- `~/primary/reports/operator/7-minimal-niri-input-gate.md`
- `~/primary/reports/operator/8-persona-system-repo-plan.md`
- `~/primary/reports/system-specialist/1-nota-all-fields-present-violation.md`

---

*End report.*
