# Skill — context maintenance

## What this skill is for

Context maintenance is the operator lane's checkpoint between one slice of work
and the next. Use it when the lane has accumulated reports, live conversation
state, subagent results the psyche explicitly authorized, or implementation
notes that could be lost on compaction. The goal is not a larger handover; it is
the smallest durable state that lets the next operator resume without stale
context.

Run the pass for the exact current lane: `operator` uses `reports/operator/`,
`second-operator` uses `reports/second-operator/`, and qualified operator lanes
use their own report directory. Everyday context maintenance is single-lane. If
the sweep needs to rank reports across roles or retire a lane, switch to
`context-maintenance-deep.md`.

A clear directive to implement or fix something is itself enough to start work;
do not run a ceremony first. Run this skill after substantial implementation,
before choosing the next slice, before compaction, or when the psyche asks for a
handover / context maintenance pass.

## Sweep shape

Start with the current lane's live context and report directory. Review only the
material needed to answer four questions:

- what landed and is now baseline
- what remains open and who owns the next move
- what durable rule, architecture fact, or repo intent should migrate upward
- what stale working artifact can retire because its substance already landed

Do not scan every workspace report by default. For operator work, the relevant
neighbors are usually the newest designer report that specified the work, the
repo docs changed by the implementation, the tests that now witness the behavior,
and the lane's own recent reports.

If a hard-to-reverse maintenance choice is ambiguous, ask one focused question in
plain chat before editing: name the item, the recommended action, and the
consequence. Otherwise choose the reversible action that preserves information.

## Classify each item

For each report, conversation theme, note, or subagent result, choose exactly one
action:

- **Migrate** when the substance has matured into a permanent home: repo
  `INTENT.md`, `ARCHITECTURE.md`, `skills.md`, workspace skill, test, code, or
  bead. Edit that home directly, then retire or shorten the working artifact.
- **Forward** when the substance is still working context for the next operator
  pass. Put it in the smallest successor report or existing open report, with
  concrete next actions and file paths.
- **Keep** when the artifact is still load-bearing on its own and has no better
  home yet. This should be rare; state why it remains live.
- **Drop** when the artifact is stale, already absorbed, or purely historical.
  Drop only after naming where the load-bearing substance landed.

Use the same rule for live conversation state. A chat insight that would matter
after compaction must land in a report, task, code comment, test, or permanent
doc. A comment that merely says "I ran this command" can disappear.

## Operator-specific checks

Before selecting the next implementation slice, audit for stale intent and stale
design inputs:

- Re-read any designer report, bead, or repo doc that named the just-finished
  work. If implementation changed the design pressure, write an operator
  implementation-consequences report instead of silently carrying the change
  forward in code.
- Check whether a durable implementation rule surfaced. General rules migrate
  to a skill; repo-specific rules migrate to that repo's `skills.md`; shipped
  structure migrates to `ARCHITECTURE.md`; psyche intent goes through the Spirit
  gate before any doc edit claims it as intent.
- Verify the witness remains named. A feature without a test, Nix check, manual
  verification note, or explicit blocker is not a complete handoff.
- Commit and push meaningful edits per `jj.md`. Reports in the lane need no
  claim; shared docs and code do.

This audit is the gate between "what was just done" and "what comes next". It
prevents the next slice from being chosen from whatever happens to be freshest
in the model's context.

## Handoff shape

Only write a handoff report when there is no better home. Put it at
`reports/<lane>/<N>-handover-<topic>.md` and keep it tight:

- current baseline: commits, tests, and files that now define reality
- open work: concrete next actions, with owners or blockers
- migrated substance: where durable rules or design facts landed
- retired context: reports or notes dropped, with the landing evidence

The handoff retires when its open work is absorbed by code, beads, reports, or
permanent docs. Do not keep handoffs as archives; git history carries the path.

## Stopping point

Stop when another operator can answer, without reading the whole conversation:

- what changed
- what proof exists
- what remains open
- where durable substance now lives
- which reports or notes are intentionally still live

Then continue with the next implementation slice, or surface the single blocking
question if the pass found one. Context maintenance is successful when there is
less live clutter and no lost information.

## See also

- `context-maintenance-deep.md` — cross-lane sweeps, meta-report directories,
  and lane retirement.
- `reporting.md` — report paths, handoff reports, and claim-exempt lane reports.
- `intent-alignment.md` — how to ask one focused psyche question when scope or
  success checks are unclear.
