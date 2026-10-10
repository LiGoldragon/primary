# Skill — intent maintenance

*Sweep the Spirit intent log: detect supersession, verify entries
still apply. Keeps the intent substrate from rotting as the
workspace and the psyche's positions evolve. Companion to
`skills/intent-log.md` (recording).*

## Supersession protocol — never silent

When an agent encounters a new psyche statement that contradicts a
prior recorded entry:

1. **Surface the contradiction inline, before recording.** Quote
   the prior verbatim and its certainty, and ask:

   > *"You said earlier (Spirit topic `<topic>`):*
   > *— `<prior summary>`*
   > *— `<prior verbatim quote>`*
   > *— certainty `<prior certainty>`, recorded `<prior timestamp>`*
   >
   > *Now you're saying `<new summary inline>`. Override the prior,
   > or am I misreading?"*

2. **Wait for the psyche's confirmation.** Three possible answers:

   | Psyche says | Action |
   |---|---|
   | "Yes, override" | Mark the prior entry superseded and add the new one (step 3) |
   | "No, clarify — the prior still applies, this is a refinement" | Add the new entry as `Clarification`; prior stays |
   | "Both apply in different contexts" | Add the new entry; the existing one stays |

3. **On confirmed override:** use Spirit maintenance tooling when
   it exists; until then, add the new Spirit entry and mark the
   prior entry as superseded in the current maintenance report or
   bead. Spirit is the sole substrate; the `intent/*.nota` substrate
   is retired. Name the supersession in the commit or report
   message (`intent: <topic> — psyche overrides prior <summary
   slug>; new <new summary slug>`).

**History holds the lineage.** Spirit is the current truth; the
retired `intent/*.nota` substrate's history lives in git. Once Spirit
supersession tooling exists, it owns the active/superseded
distinction; until then, supersession is explicitly documented in the
maintenance report or bead and never silently rewritten.

Supersession is **always explicit, and only the psyche can
supersede psyche intent.** A new psyche statement is the only
source that can override a prior psyche statement. An agent
encountering documented intent that seems wrong does NOT supersede
on its own authority; the agent asks the psyche
(`skills/intent-clarification.md`). The protection is load-bearing
against agent hallucination passing as psyche intent.

## Current negation shape

Negation is a specific supersession: the psyche says a prior record
is invalid, not merely refined. Today Spirit has no typed
`Negates`/`Supersedes` relation, so the operative shape is:

1. Observe the prior record by identifier.
2. Ask the psyche to confirm the old record is negated.
3. Record a new `Correction` or `Decision` that names the old
   Spirit identifier and states the replacement truth.

Use wording like: `Spirit record 1053 is negated; the correct
intent is ...`. Do not delete the old record. Until typed
supersession lands, active truth is carried by the newer explicit
psyche correction plus any maintenance report or bead that tracks
the supersession.

## Removing a record — tombstone first

Deployed Spirit supports explicit removal — `spirit "(Remove N)"`,
psyche-authorized (records 1103/1189). This is for records that
should **not remain at all**: mis-logged working orders, or
fully-stale records whose substance is rehomed. When lineage should
stay visible instead, supersede with a `Correction` and keep the
record (see "Current negation shape" above) — do not remove it.

Removal is **destructive and irreversible.** The record leaves the
store, and redb's copy-on-write page reuse overwrites its bytes
within hours (see `sema` ARCHITECTURE §"Deletion durability" and
`reports/system-designer/47`). There is no undelete.

So **capture before you remove.** Before any `(Remove N)`, record the
full text and daemon-stamped provenance into the removing agent's
report:

```sh
spirit "(Observe (RecordIdentifiers ((Exact N) WithProvenance)))"
```

Paste the result into a tombstone appendix in the removing agent's
report; the report then IS the provenance of what was removed. The
discipline emerged from a known loss: an undocumented removal of
records 1157–1175 (no tombstone) proved unrecoverable because redb's
copy-on-write page reuse overwrote the freed bytes within hours; an
earlier removal of 19 psyche-approved records that WAS tombstoned
first preserved their full text. Capture first, then remove.

Stay conservative: when removability is uncertain, flag rather than
remove (record 1103 — over-removal is worse than under-removal).
Lowering a record's certainty to `Zero` marks it as a removal
candidate (records 1192/1215). Production Spirit supports explicit
collection through `CollectRemovalCandidates`: exact-`Zero` candidates
are archived as compact summaries before retraction, while archive
failure returns skipped candidates and leaves records in the store.
Use collection for reviewed batches; use hard single-record `Remove`
only when the tombstone has already been captured.

## Verification — does the entry still apply?

Periodically (when sweeping a topic, or when an entry's substance
crosses the agent's path), verify that the recorded entry still
matches workspace reality. Three failure modes:

- **The workspace evolved past the entry.** The psyche said "X is
  forbidden" in a context that no longer exists. If the constraint
  no longer applies, ask the psyche for explicit retirement —
  don't assume.
- **The recorded summary doesn't match the verbatim.** Agent
  rephrasing drift; the summary says one thing, the quote says
  another. Fix the summary to match the quote.
- **The certainty doesn't match the phrasing.** Re-read the quote
  against `skills/intent-log.md` §"Certainty vocabulary". Correct
  if mismatched.
- **One record bundles claims with different certainty.** A record can
  accidentally carry a settled rule and a tentative design in one
  high-certainty summary. Split or correct it: preserve the settled
  part at its earned certainty, then record the tentative part at its
  lower certainty. This especially matters when the psyche explicitly
  says a new clarification is low-certainty.

Verification corrections that aren't superseding the psyche's
intent (just fixing the agent's transcription) can land directly —
they're discipline cleanup, not author overrides. Log the change
in the commit message
(`intent: corrected Spirit summary in <topic> to match verbatim`).

## Sweep — when and how

Trigger a sweep when:

- A Spirit topic grows substantially or query results become noisy.
  Smaller sweeps run alongside `skills/context-maintenance.md`.
- An agent reviewing a topic notices an entry that no longer
  matches the workspace.
- Major redesigns (the kind that generate `v2` reports) — the
  redesign's premises likely supersede earlier intents and need
  explicit psyche confirmation.
- A context-maintenance pass discovers older intent clearly
  contradicted by newer stronger intent. Per psyche 2026-06-03
  (intent record 1496 Clarification Medium), context-maintenance
  agents may audit even old intent for clear contradictions and
  recommend removals or supersession, but **deletion from Spirit
  remains reviewable and justified by the newer intent**. Propose;
  do not execute unilaterally. The orchestrator (or psyche)
  authorises removals after seeing the contradiction explicitly
  named.

How:

1. Read every Spirit entry in the topic.
2. For each entry, check: does this still apply? Does the summary
   still match the verbatim? Does the certainty still match the
   phrasing? Does one summary bundle sub-claims with different
   certainty?
3. For entries that no longer apply: ask the psyche.
4. For agent-transcription drift: correct directly.
5. For a genuinely noisy topic with two distinct sub-topics:
   carve a new Spirit topic per `skills/intent-log.md` §"When to
   actually split". The split itself is not author intent — it's
   housekeeping; history holds the lineage.

## When to skip recording in the first place

Some psyche statements are too transient for the log (covered in
`skills/intent-log.md` §"When to record" — restated here for
maintenance context):

- "Let's try this and see" — pre-commitment exploration.
- "Maybe X, I'll think about it" — `Minimum`-certainty might be
  worth recording, but if the psyche then commits to something
  else within the same conversation, skip the intermediate.

If you skip recording a borderline case and the psyche later asks
"why isn't this in Spirit?" — at that point, record it.

## Forward — richer supersession lifecycle

Today's protocol treats supersession as binary: the prior is
overridden or it isn't. The psyche has surfaced a richer model
that lands when the multi-agent auditing arc arrives:

- **Negation.** A prior intent is fully invalidated by a new
  statement. Negated entries are candidates for archival and
  eventual garbage collection — archived first (slow storage
  is cheap), deleted only after a retention window.
- **Certainty lowering.** A new statement partially contradicts
  a prior. The prior stays but its certainty drops (`Maximum` →
  `Medium`, `Medium` → `Minimum`) without full negation.
- **Escalation on partial contradiction.** When the agent can't
  decide whether the new statement negates, lowers, or coexists
  with the prior — the contradiction is too tangled — escalate
  to the psyche directly, or to a review agent that takes in
  more context and decides.

The "spirit guardian" is the future sub-actor in `persona-spirit`
that judges among the three responses. Until the multi-agent
auditing system exists, today's spirit is dumb storage that
trusts agent input, and the binary protocol above is the
operative discipline.

## Forward — persona-mind migration

When persona-mind's typed memory variants land, supersession
becomes a typed relation (`Supersedes` linking two
`Authorial<Kind>` memories); Spirit records retire in favor of
memory-graph queries. Until then, Spirit is the sole carrier; the
`intent/*.nota` substrate is retired and its history lives in git.

## See also

- `skills/intent-log.md` — recording discipline; record shape;
  certainty vocabulary; topic granularity.
- `skills/context-maintenance.md` — workspace-wide sweep discipline;
  intent log is one of the things context-maintenance may sweep.
- `skills/nota-design.md` — positional-NOTA discipline these
  records follow.
