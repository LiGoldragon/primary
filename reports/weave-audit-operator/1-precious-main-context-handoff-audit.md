---
title: 1 — preciousMainContext handoff audit
role: weave-audit-operator
variant: Audit
date: 2026-06-24
topics: [precious-main-context, handoff, beads, spirit]
description: |
  Audit of the "Add sweep memories to the weave" handoff against live
  primary state: version control, Spirit records, BEADS graph, and the
  preciousMainContext reports.
---

# 1 — preciousMainContext handoff audit

## Findings

### High — W1 is still open and ready in BEADS, despite the handoff saying it is done

The handoff report says W1 is **DONE** and that W2-W4 are ready:
`reports/preciousMainContext/6-handoff.md:114-117`. Live BEADS state does
not match that. `bd show primary-ptvb.1` reports W1 as `OPEN`, and `bd ready
--limit 100` still lists W1 among the ready items. Because W1 still blocks W2,
W3, W4, W6, and W7, a fresh agent following `bd ready` will see W1 as the next
work item and W2-W4 as blocked.

The updated weave report is internally consistent with BEADS: it marks W1,
W5, S1, S2, and S3 as ready (`reports/preciousMainContext/4-weave.md:44-50`
and `:70-76`). The stale surface is the handoff table and, more importantly,
the open W1 bead.

Recommendation: if W1 is truly done, close W1 with a reason pointing at
commit `761e4ff9` (the W1 human-interaction prune) and
`reports/preciousMainContext/5-human-interaction-cut.md`. If W1 is not done,
remove the "DONE" claim from the handoff and keep W2-W4 blocked.

### High — tool-scaffolding residue still exists in the W1 report

The handoff says W1's helper left literal `</content>` / `</invoke>`
tool-scaffolding and that it is "now removed"
(`reports/preciousMainContext/6-handoff.md:92-93`). That is false for the W1
report: `reports/preciousMainContext/5-human-interaction-cut.md:85` still
contains a trailing `</content>` line. The edited source skill
`skills/human-interaction.md` is clean, but the report is not.

Recommendation: remove the trailing marker before closing W1. This matters
because W5 explicitly includes "read helper-written files back, especially the
end, for tool-scaffolding residue" as a lesson; leaving the residue in the
lesson report undercuts the example.

### Medium — the "pushed" commit does not itself carry the BEADS changes

The claimed pushed commit is real and clean: `main`, `main@git`, and
`main@origin` all resolve to commit `d52e845d`, and `jj st` is clean. But that
commit changes only `reports/preciousMainContext/4-weave.md`; it does not carry
the S1/S2/S3 bead creations in tracked Git content. The active BEADS database
is under `.beads/embeddeddolt`, which is ignored by `.beads/.gitignore`.

This may be acceptable for agents sharing the same local BEADS state, but a
fresh checkout reading only Git will get the report, not the local issue-store
records. Treat "the three sweep memories landed" as a live-local-BEADS claim,
not as something proven by the pushed Git commit.

### Low — report-format hygiene does not match the current reporting contract

The current reporting skill requires YAML front matter with canonical fields.
`reports/preciousMainContext/4-weave.md` and
`reports/preciousMainContext/5-human-interaction-cut.md` have no YAML front
matter. `reports/preciousMainContext/6-handoff.md` has front matter, but uses
`lane` / `discipline` and lacks the canonical `role`, `variant`, and `topics`
fields. This does not break the work graph, but it is contract drift on a lane
whose whole purpose is reducing guidance/reporting entropy.

Recommendation: fix report headers when those reports are next touched; do not
let header cleanup distract from the W1 close/residue fix.

## Verified Good Claims

- Working copy cleanliness and push state are correct: `jj st` reports no
  changes, and `main`, `main@git`, and `main@origin` all point at `d52e845d`.
- The four landed Spirit records exist and match the handoff: `30cu`, `69fa`,
  `hu84`, and `d7ew` all return from `spirit "(Lookup ...)"` with the expected
  descriptions.
- S1, S2, and S3 exist in BEADS with the intended content. S1 blocks W8, S3
  blocks W6, and S2 is independent.
- W5 exists, is open, and blocks W6. Its description centers the
  context-preserving dispatch / minimal-dispatch-envelope rule.
- The dependency graph has no cycles: `bd dep cycles` returns "No dependency
  cycles detected."

## Immediate Fix Order

1. Remove the trailing `</content>` marker from
   `reports/preciousMainContext/5-human-interaction-cut.md`.
2. Close W1 if the human-interaction cut is accepted as done.
3. Re-run `bd ready --limit 100`; W2, W3, W4, W5, S1, S2, and S3 should be the
   preciousMainContext pickup set.
4. Only then hand the lane to a fresh agent; otherwise the first pickup step is
   likely to repeat W1 or distrust the handoff.
