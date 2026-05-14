# Skill — context maintenance

*Sweep the working surface of context — both the filesystem
reports under `reports/<role>/` and the in-conversation context
window — for what's still load-bearing, migrate substance to its
right permanent home, and retire what's done.*

---

## What this skill is for

Two surfaces decay together:

- **Reports on disk** under `reports/<role>/`. Working artifacts.
  The filesystem accumulates them; their substance matures upward
  to permanent docs (skills, architecture, code, `ESSENCE.md`) or
  retires when done. See `~/primary/skills/reporting.md` for the
  disk-side typology and hygiene.
- **Context in the live conversation**. The session's working
  memory. When the context window fills, the unsaved part is lost
  on compaction or clear unless it has migrated to disk.

These are the same kind of thing at different scopes — **a report
is just context saved to disk**. The discipline is the same: keep
load-bearing substance; move it to its right permanent home;
retire what's done. Treating them separately is a smell — they
usually need maintenance at the same time, by the same pass.

---

## When to invoke

- **Compaction trigger.** The context window is approaching its
  limit, or the user is about to clear/compact. Sweep before the
  loss event.
- **Report soft-cap trigger.** A role's `reports/` subdir crosses
  the 12-report soft cap (per `~/primary/skills/reporting.md`
  §"Soft cap"). Sweep older reports to migrate substance and
  retire enough to land back under cap.
- **End-of-session checkpoint.** After substantial work, before
  stepping away. Ensures the next agent (or next conversation)
  has the right artifacts to resume from.
- **Explicit user direction.** "Do a context maintenance" or "do
  a handover" or similar.

Often the triggers coincide. Treat them as one pass.

---

## Method

### 1 · Inventory

List both surfaces:

```sh
# Disk side — reports for each role that's relevant.
ls ~/primary/reports/<role>/
```

For context: review the conversation's themes — what was worked
on, what was decided, what's still open, what insights surfaced.
Don't dump everything; *categorize*.

### 2 · Per item, decide

For each report or context theme, pick one of four actions:

| Action | When |
|---|---|
| **Forward** | Substance is still load-bearing as a working artifact. Roll it forward into a successor report or extend an existing one; retire the predecessor. |
| **Migrate** | Substance is mature enough to be permanent. Inline it into a skill, `ARCHITECTURE.md`, `ESSENCE.md`, or code. Retire the source. |
| **Keep** | Substance is load-bearing on its own and has no permanent home yet. Rare. Foundational decisions still searching for their final shape. |
| **Drop** | Substance is stale, addressed, superseded, or already captured elsewhere. Delete the report (or simply let context lose it). |

For context items specifically:

| Context type | Typical destination |
|---|---|
| Decisions made in conversation | The permanent doc the decision lives in (ARCH, skill, `ESSENCE.md`). |
| Half-formed insights, possible patterns | A short `note:` in the appropriate report or skill, or a sentence in a handover report. Don't lose them; don't over-format them. |
| Process / workflow reflections | A skill if generalizable, a session-summary if local. |
| In-flight work pending pickup | The successor task / `bd` item / report that names what's next. |
| Already-on-disk content | Drop from consideration — already saved. |

### 3 · Distribute

Land the substance in its right home, **not** in a catchall
handover dump. Preferred order:

1. **Existing reports on the same topic** — extend them with the
   new substance. The handover happens in place.
2. **Permanent docs** — inline as the rule, constraint, or
   invariant they actually are. Per
   `~/primary/skills/skill-editor.md` §"Skills never reference
   reports" and
   `~/primary/skills/architecture-editor.md` §"Architecture files
   never reference reports", the permanent docs are where rules
   live, and they don't cite the report that produced them.
3. **A new rollover/handover report** — only as last resort.
   Substance that doesn't fit any existing home and is too
   unsettled to be permanent. The rollover is a working artifact
   for the next session, not an archive.

### 4 · Small thoughts are OK

A one-sentence *"side note: this pattern recurred and might be
worth a skill someday"* landed in the right place beats losing
the thought entirely. Tags like `note:`, `possibly useful:`, or
`undecided:` make a thought discoverable without committing the
workspace to act on it.

Don't over-engineer small thoughts. A line in an existing report
that says `note: agents asked about X three times this week —
might warrant a skill if it recurs` is better than no record.
Discovery later is the value, not formality now.

---

## The rollover / handover report (when one is needed)

If a handover artifact is genuinely needed, it lives at
`reports/<role>/<N>-handover-<date>.md` (or `<N>-rollover-…`).

Structure:

- **What landed** — what's been committed and pushed; one line each.
- **What's open** — what was discussed but not yet resolved.
- **Side notes** — small thoughts worth keeping. Mark each with
  `note:` / `possibly useful:` / `undecided:`.
- **Next-session targets** — concrete pickup points for the next
  conversation or agent.

The handover report retires once the substance migrates to its
right permanent home or the next-session work absorbs it. It is
itself a forwarding-eligible report under the standard hygiene.

---

## Using agents for the sweep

A maintenance pass over many older reports is well-suited to
parallel agent dispatch. The orchestrator doesn't have to read
every report into its own context.

Pattern:

- Give each agent a small batch of older reports + the
  drop/forward/migrate/keep rule from §2.
- Each agent reads the report, checks the surrounding permanent
  docs (does this substance already live in ARCH? in a skill?
  has it been superseded?), then proposes the action.
- Review the agent's proposals; execute the migrations; retire
  the reports.

This keeps the orchestrator's context light. The orchestrator's
role is to apply decisions, not to re-read every report.

For context-only substance (the part that lives in the live
conversation, not on disk), the orchestrator does this sweep
itself — agents can't see the conversation's working memory.

---

## Anti-patterns

- **Dumping all context into a "handover" report.** The handover
  is a fallback, not a default. Most substance has a better home
  (a skill, an ARCH, an existing report). A dumping-ground handover
  isn't a working surface — it's an archive that decays as fast as
  the context it replaced.
- **Keeping reports indefinitely "because they might be useful."**
  Git log preserves history; the filesystem should hold only
  what's actively load-bearing. Per
  `~/primary/skills/reporting.md` §"What gets absorbed, not kept",
  even foundational decisions and incident lessons get absorbed
  into permanent docs rather than living forever as reports.
- **Retiring a report whose substance hasn't migrated.** Before
  dropping, confirm the load-bearing parts are captured elsewhere
  (an updated skill, an ARCH constraint, a successor report). If
  not, migrate first, then drop.
- **Treating context and reports as different disciplines.** They
  aren't. Both are working surfaces; both follow the same
  forward/migrate/keep/drop rule. A maintenance pass over only
  one is half a maintenance pass.
- **Over-formatting small thoughts.** A note-line is a note-line.
  Don't promote a half-formed observation to a numbered section or
  a dedicated report. The shape matches the substance.

---

## See also

- `~/primary/skills/reporting.md` §"Kinds of reports — and where
  their substance ultimately lives" — the typology of report
  shapes and their permanent homes.
- `~/primary/skills/reporting.md` §"Hygiene — soft cap,
  supersession, periodic review" — the disk-side hygiene rules
  this skill operationalizes.
- `~/primary/skills/skill-editor.md` §"Skills never reference
  reports" — the discipline that makes substance-migration
  possible (and necessary): once substance is in a skill, the
  report it came from can retire without leaving a dangling
  citation.
- `~/primary/skills/architecture-editor.md` §"Architecture files
  never reference reports" — same rule for ARCH.
- `~/primary/AGENTS.md` §"No harness-dependent memory" — the
  rule that memory belongs in workspace files every agent can
  read, not in harness-private state. Context maintenance is how
  that rule is honored across sessions.
