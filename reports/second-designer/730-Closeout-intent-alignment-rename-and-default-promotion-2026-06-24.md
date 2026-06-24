# Closeout — alignment-interview renamed intent-alignment, promoted to default interactive-agent discipline (2026-06-24)

Psyche directive during a designer context-maintenance session: *"rename it to
intent-alignment, and include it in the primary agent files, since it's what an
agent should do by default — unless the agent is a very specialized agent in
which case it should be trained already. so it should be in interactive agents,
whatever file those agents read, whether claude or chatgpt."*

Captured as Spirit `ky10` (Decision, High) before any file work, per capture-first.

## What landed on main

| Surface | Change |
|---|---|
| `skills/alignment-interview.md` → `skills/intent-alignment.md` | jj-tracked rename (history preserved). Title and opening reframed: intent alignment is the *default first move* for an interactive agent, not only an ambiguity tool. |
| `skills/skills.nota` | Old `(Workflow alignment-interview … Mechanism)` entry removed; new `(Meta intent-alignment … Apex)` entry added beside `human-interaction`. Reclassified because it is now a default psyche-facing discipline, sibling to human-interaction. Index re-validated: 0 quotes, balanced delimiters, 71 entries, every path resolves. |
| `AGENTS.md` Hard overrides | New override **"Interactive agents default to intent alignment"** — the method (one focused question per turn in plain prose; decision/why/recommendation/alternatives; never the questionnaire UI), the carve-out, and the specialized-agent exemption. |
| `INTENT.md` | New section **"Intent alignment is the default"** with the verbatim psyche quote in italics, anchored to `ky10`. |

Commit `prrxptts` (`f8154faa`) on `main@origin`. Lock released.

## Decisions made this session

- **The "directive is the answer" carve-out is woven in everywhere**, anchored
  in Spirit `ki6i` (Correction, High) — *a directive to implement or show is
  itself the answer*. Without it, "align by default" reads as "always
  interview," which would contradict `ki6i`/`48y4` autonomy intent. The skill
  body, the AGENTS.md override, and the INTENT.md section all state: a clear
  directive → do it and present; reserve questions for genuinely blocking,
  hard-to-reverse forks.
- **Lane = `second-designer`, not `designer`.** The `designer` lane is held by a
  live peer (`mentci-lib/re-found-on-live-contracts`). Claiming the primary
  guidance files under `designer` would let either lane's `Release` stomp the
  other's claim, so this work ran under `second-designer` with narrow per-file
  claims.

## Open / surfaced

- **lore/AGENTS.md propagation (decision pending).** The cross-repo canonical
  contract `repos/lore/AGENTS.md` is "the file every interactive agent reads"
  across *all* repos, not just primary. Propagating the default there is the
  fuller reading of the directive, but lore is a `/git` repo under
  designer-branch discipline (operator owns its main), so it needs a designer
  branch + operator integration rather than a main-direct edit.
- **Broader task still open.** The original "designer context maintenance driven
  by relentless psyche alignment, guided by spirit data" was interrupted by this
  rename. Recommended resumption: guidance-surface alignment (skill bodies +
  apex docs vs current Spirit), runnable under `second-designer` without the
  report-tree lane conflict.
- **Stale citation found.** Report 729 cites Spirit `1p0r` ("single source / no
  frontmatter") — that record does not exist in the live store (`Lookup`
  errors). Flagged for a later intent/report-hygiene fix; not touched here.
