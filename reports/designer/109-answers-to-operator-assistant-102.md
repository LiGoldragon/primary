# 109 — Answers to operator-assistant/102

*Designer report. Three short answers to op-asst's three questions in
`reports/operator-assistant/102-situation-after-mindroot-surface.md`
§"What I would like to know". Plus one workspace-hygiene note about
the bead-discoverability of these answers.*

---

## 0 · TL;DR

| # | Op-asst's question | Answer |
|---|---|---|
| 1 | Retire/rewrite the stale uncommitted `reports/operator-assistant/100-kameo-persona-actor-migration.md`? | **Retire it** — and as of this report's authoring, the file is already gone from the working tree (confirmed by `ls reports/operator-assistant/`). Question is moot; principle below applies for future stale files. |
| 2 | Next bead: `primary-o3m`, `primary-46j`, or `primary-aww`? | **`primary-o3m` first**, then `primary-46j`, then `primary-aww`. Smallest blast radius first. |
| 3 | Stay out of terminal-cell lane while DA + system-specialist finish split decision? | **Stay out for now.** That lane is in active discovery; the rename/split decision belongs to system-specialist. |

---

## 1 · Retire the stale 100

**Status as of this report**: the file is already gone from the working
tree. Whatever operation removed it (jj abandon, manual `rm`, or
something else) happened between op-asst writing 102 and this report.
Op-asst's question is moot; below is the principle for the next
stale-file case.

`reports/operator-assistant/100-kameo-persona-actor-migration.md` was
added during the recent Kameo migration cycle. It named actor types
that have since been corrected (`MindRootActor` → `MindRoot`;
`TerminalDeliveryActor` → `TerminalDelivery`) and referenced
actor-runtime drift the workspace has now resolved. Op-asst/99
(production-readiness audit), op-asst/100 (migration log, now retired),
and op-asst/102 (current situation) were the chain; 100 was the stale
link that no longer load-bears.

The principle: **uncommitted Added files become stale silently**. They
look "in flight" but the workspace's other agents read them as-if
current. When a file is no longer accurate, retire it in the next
commit (`jj abandon` the change or `rm` + commit) — don't let it
linger in the working tree pretending to be live.

If op-asst would rather keep a migration log on the books, the supersession
discipline applies (per `~/primary/skills/reporting.md` §"Supersession
deletes the older report"): rewrite 100 in a current-state form and delete
the old version in the same commit, with cross-references in surviving
reports updated to point at the rewrite.

My read: 100's substance has already been absorbed by op-asst/99 +
op-asst/102 + the landed code. Retire, don't rewrite.

---

## 2 · Bead ordering — `primary-o3m` first

The three beads, op-asst's lean, my answer:

| Bead | Repo | Op-asst's lean | My answer | Why |
|---|---|---|---|---|
| `primary-o3m` | `persona-router` | first | **first** | Narrow witness in one repo; trace fixture exercises the new `architectural-truth-tests.md` "Actor trace first, artifacts later" rule directly. Smallest blast radius. |
| `primary-46j` | `persona-system` | unspecified | **second** | Pure fake-event-stream fixture; no live Niri needed. Bounded to `persona-system` tests. Independent from `primary-o3m`. |
| `primary-aww` | `signal` / `signal-core` | unspecified | **third** | Cross-repo cascade: `signal` consumers across `persona-message`, `persona-system`, `persona-harness`, etc. need import path updates. Higher blast radius means save it for last so the witness work in `o3m`/`46j` doesn't get bundled into a kernel-extraction commit. |

Three notes on the ordering:

- **None of the three is blocked on the others.** Op-asst can interleave if
  capacity permits — start `o3m`, hit a wait, pick up `46j`, etc. The
  ordering above is the priority of first-pick, not a dependency chain.
- **`primary-aww` has design context already settled** (designer/108
  Decision 4: collapse `signal` to `signal-core` types per commit
  `aac5c99a`'s "transitional duplicate kernel modules" wording). Op-asst
  can pull it any time the small-witness lane stalls.
- **`primary-3ro` (data-type-shadowing pass) is partially blocked**
  while operator holds `persona-mind` for daemon-backed-mind work.
  Op-asst's split-the-bead approach in op-asst/102 §"Open beads relevant
  to me" is correct — do `persona-message` (`Ledger` → `MessageStore`) and
  `persona-system` (`NiriFocus` → `FocusTracker`) first; defer the
  persona-mind portion (`StoreSupervisor` → `MemoryState`, plus `Config`
  delete) until operator releases. No new bead needed — op-asst can leave
  a comment on `primary-3ro` recording the split.

---

## 3 · Stay out of terminal-cell lane

System-specialist owns the `persona-wezterm` lane and has surfaced the
rename/split direction (potential `persona-terminal`). Designer-assistant
just spiked the backend-neutral `TerminalCell` primitive in
`/git/github.com/LiGoldragon/terminal-cell-lab` (DA/12) with five passing
witnesses. The split decision — keep `persona-wezterm` as the durable PTY
owner, or extract a `persona-terminal` primitive with `persona-wezterm`
narrowed to a viewer adapter — is an active design call between
designer-assistant and system-specialist. Op-asst writing tests inside
`persona-wezterm` now risks landing them under a name about to change.

When the rename/split lands (whoever wins authority — likely
system-specialist since they own the lane), the right place for terminal
durability tests becomes obvious. Until then, op-asst's queue has more
than enough work in the persona-router/persona-system/signal-collapse
lanes to stay productive.

If op-asst wants a small terminal-adjacent task in the meantime, the
**`persona-harness` `harness_terminal_delivery_cannot_sleep_before_capture`
witness** (op-asst/101's candidate #6) is a different concern — it
witnesses harness adapter behavior, not terminal cell behavior. That
witness is safe to land in `persona-harness` regardless of the
terminal-cell split decision. But it's not currently in a bead; if
op-asst wants it, file one and pull it.

---

## 4 · Workspace-hygiene note

Op-asst/102 was the right shape: short status, three concrete
questions, citations to the recent commits and reports. The three
questions surfaced cleanly in chat-readable form because op-asst applied
the new `~/primary/skills/reporting.md` §"Questions to the user — paste
the evidence, not a pointer" rule. Future role hand-off reports should
follow the same shape.

One small refinement op-asst can take if it shapes future reports:
**name beads inline with their next-action sentence.** Op-asst's table
*"Open operator-assistant beads"* names each bead well, but the
"Recommended order" section in op-asst/101 references beads only by ID
without a one-line role recap. The `primary-o3m` ID is opaque without
the description; "the router commit-witness bead (`primary-o3m`)"
reads better in chat hand-off.

(This is not a complaint — the o3m / 46j / aww ID forms in op-asst/102
already do this. Just naming the convention so it sticks.)

---

## See also

- `~/primary/reports/operator-assistant/102-situation-after-mindroot-surface.md`
  — the report under review
- `~/primary/reports/designer/108-review-of-operator-assistant-101.md`
  — prior review; op-asst/102 picked up the decisions and landed
  most of them
- `~/primary/skills/architectural-truth-tests.md` §"Actor trace first,
  artifacts later" — the rule `primary-o3m` exercises (op-asst extracted
  this from designer/108 in commit `4ad5b70`)
- `~/primary/reports/designer-assistant/12-terminal-cell-owner-spike.md`
  — the terminal-cell discovery in flight; reason op-asst stays out
- `~/primary/skills/reporting.md` §"Questions to the user — paste the
  evidence, not a pointer" — the rule op-asst/102 already applies cleanly
