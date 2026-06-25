# preciousMainContext weave — implementation record

This is the implementation record for the `preciousMainContext` weave. It
does **not** supersede reports 4, 6, or 7. Those stand as the durable
artifacts they are: `4-weave.md` is the dependency graph and bead-id map
(the durable git-side record of the work), `6-handoff.md` is the cut recipe
and the landed/pending Spirit state, `7-subagent-delegation-context-audit.md`
is the dispatch-discipline audit that drafted the ready-to-paste carves. This
report records what one execution pass through the weave actually landed and
verified, and what remains gated on psyche authority. Read 4/6/7 for the
reasoning; read this for the state of the graph after this pass.

## What the weave-audit found (report 1, not re-derived)

The audit re-checked the graph against the live `bd` store rather than
trusting the prior handoff, and surfaced four findings:

1. **W1 was genuinely done but its bead was still open.** `6-handoff.md:114`
   claimed W1 `DONE`, yet `primary-ptvb.1` was OPEN in the store. The cut had
   actually landed (`skills/human-interaction.md` at 64 lines / 7 H2 sections
   from a 115/14 baseline; the AGENTS.md-duplicate sections gone; the
   five-kinds table collapsed; testing + parallel-lane sections retained under
   move-banners). The stale-open bead is exactly what kept W2/W3/W4 showing
   blocked-by-W1 in the live graph. Closing it is the unblock.
2. **Tool-scaffolding residue in the W1 report.** Line 85 of
   `5-human-interaction-cut.md` was a literal `</content>` line — the W1
   helper's tool-scaffolding left at the file end. Sharp irony: that report is
   the very lesson teaching "read helper-written files back, especially the
   end, for residue," so leaving it undercut the example.
3. **AGENTS.md still prints the OLD dispatch default.** Report 7 proves
   `AGENTS.md:286-293` still carries the designer-only / do-it-yourself
   dispatch override, directly contradicting the LANDED universal Spirit
   records `30cu` / `69fa` / `hu84`. Fixing it is W6 — which cannot land until
   the `ky10` Spirit record is reconciled (the keystone block; see below).
4. **`.beads` issue data is not git-tracked.** Only `.gitignore`,
   `README.md`, `config.yaml`, `metadata.json` are tracked; `dolt/` (the
   record store) is ignored. So bead state and the S1/S2/S3 sweep memories
   live only in local Dolt state, not in tracked git content. This is
   by-design for the current `bd` substrate and is **not** a blocker — but it
   is a fresh-checkout risk, which is why `4-weave.md` carries the full
   bead-id map + mermaid as the durable git-side record. If the psyche wants
   the bead graph reproducible from git (e.g. a tracked JSONL export), that is
   a separate decision, flagged not acted on.

## What landed, in dependency order — with verify evidence

Five steps were executed and then independently re-verified against the
actual files and the live read-only `bd` state. Every one passed; nothing was
trusted on report. The orchestrator commits the whole working copy after this
record — no `jj`/`git` was run inside the pass.

### Step 1 — cleanup: remove the `</content>` residue (mechanical)

Deleted the final `</content>` line (line 85) from
`5-human-interaction-cut.md`; the file now ends on `...reversible in one
commit.`

Verify: `grep -c '</content>'` returns 0; a full `grep -n` finds nothing; the
file ends on the `## Pattern notes` section. Done first by design — the W1
report is the residue lesson, so the example had to be clean before anything
else.

### Step 2 — close W1 `primary-ptvb.1` (mechanical)

Confirmed the deliverable present (`human-interaction.md` 64/7 from 115/14;
forwarded-prompts / `run_in_background` / `/nix/store` duplicate sections
gone; five-kinds table collapsed; testing + parallel-lane sections retained),
then closed the bead with a reason citing the cut landing at commit
`761e4ff9` (the W1 human-interaction prune commit).

Verify: `bd show primary-ptvb.1` → `CLOSED`. `bd ready` now lists
`primary-ptvb.2` (W2), `.3` (W3), `.4` (W4) and omits `.1`. `bd dep cycles` →
`No dependency cycles detected`. This is the unblock the audit identified:
W2/W3/W4 depend only on W1.

### Step 5 — write `when-to-use-helpers.md` (W5 `primary-ptvb.5`, mechanical)

Created `skills/when-to-use-helpers.md` carrying the minimal-dispatch-envelope
rule from `6-handoff.md:84-89` verbatim as a block quote (run only the
minimal dispatch envelope — Spirit gate, lane/report setup, the helper's
brief — then stop; do not read what the helper was sent to collect; the helper
owns the broad read). Added the residue-readback companion lesson
(`6-handoff.md:91-93`) cross-referencing the named worked example
`reports/schema-help-daemon-pilot-operator/1-skill-change-handoff.md`
(report-7 rec #6). Added a `(Meta when-to-use-helpers skills/when-to-use-helpers.md
Apex [...])` entry to `skills.nota` (line 133), placed adjacent to the
human-interaction / intent-alignment Meta entries; Apex tier chosen to match
those neighbours, the `<Tier>` placeholder having been left open. Closed
`primary-ptvb.5`.

Verify: file exists (written 2026-06-25); the verbatim block quote is present
(lines 11-16); the companion lesson is present (`## Companion lesson — read
written files back for residue`); its tail ends cleanly with the named
worked-example cross-reference and no residue; `skills.nota` line 133 carries
the matching Meta entry; `bd show primary-ptvb.5` → `CLOSED`. W5 still blocks
W6, which is expected.

### rec4 — sharpen the session-lanes Fleet/smart-zone trigger (mechanical)

Replaced the `skills/session-lanes.md` Fleet bullet (lines 110-115) — which
fanned out only "Once that window is spent" — with the ready-to-paste
replacement drafted verbatim at `7-subagent-delegation-context-audit.md:139`:
dispatch fresh-context helpers as soon as a task needs more than a few
already-known files or any multi-level chase, the lead reasoning over the
helpers' distilled responses, the smart zone reserved for thinking and intent
alignment, not exploration the helper owns.

Verify: the bullet now reads the report-7 text verbatim; the old
window-exhaustion-only trigger is gone, so fan-out now triggers on
research-non-triviality. Note: `rec4` is a report-internal recommendation id,
**not** a tracked bead (`bd show rec4` → no issue found); the broader
session-lanes cut is the separate W4 `primary-ptvb.4`. No bead transition was
run because none exists; the file deliverable (the sole done-criterion) is
satisfied.

### rec5 — skill carve-outs in operator / reporting / intent-alignment (mechanical)

Appended the verbatim carve from `7-subagent-delegation-context-audit.md:145`
to each of the three contradicting gating spots, after first confirming each
anchor line still reads as report 7 quotes it: `skills/operator.md:66` (after
the subagent-side-work gating at :64), `skills/reporting.md:259` (after the
slice-ownership gating at :257), `skills/intent-alignment.md:44-47` (after
"dispatching subagents only when the psyche asked" at :41). The carve defers
early-context read/explore to the universal orientation-dispatch default
(Spirit `30cu`, AGENTS.md) and confines the local psyche-gate to change-making
dispatch only.

Verify: `grep 'orientation-dispatch default'` finds the carve in all three at
the cited lines, each attached to the correct gating sentence; the
intent-alignment instance soft-wrapped to the file's prose width. As with
rec4, `rec5` is a report-internal id, not a tracked bead, so no bead
transition was run.

## What is deferred to psyche authority — and exactly why

Six weave items are **not** landed because they are psyche-authority. Three
are Spirit-record sweeps (S1/S2/S3), and three are doc changes blocked behind
them in the graph (W6/W7/W8) or behind the other unlanded cuts. The keystone
is the `ky10` reconcile gating W6.

### The keystone: `ky10` reconcile gates the W6 AGENTS.md shrink

W6 (`primary-ptvb.6`, shrink AGENTS.md to a thin spine) is the fix that
resolves audit finding #3 — replacing the stale `AGENTS.md:286-293`
designer-only dispatch override with the report-7:121 delegate-the-broad-read
bullet and the report-7:129 protect-the-smart-zone / never-double-explore
bullet, and shrinking the file to reading-order + `skills.nota` pointer +
universal rules only.

W6 cannot land until S3 (`primary-ptvb.11`) reconciles Spirit record `ky10`.
`ky10` places intent-alignment **in** the agent-contract files; as written it
directly conflicts with the minimize-AGENTS.md principle (the principle that
authorizes shrinking the contract files to a thin spine + pointers). Spirit's
integrity guardian refused to land the minimize-AGENTS.md record as a sibling
precisely because `ky10` is still wired the other way.

What superseding `ky10` would entail, concretely: a `ChangeRecord` or
`Supersede` on `ky10` that removes the "intent-alignment lives in the contract
files" framing so the contract surface can be reduced to spine + pointers,
**then** a new `Record` landing the minimize-AGENTS.md principle. Only after
that intent-layer change settles can the W6 AGENTS.md shrink be authored.

Why an agent must not do this unprompted: editing or superseding any Spirit
record is psyche-authority by the explicit authority boundary in AGENTS.md —
the intent layer outranks every other surface, and superseding psyche intent
is always explicit. `ky10` encodes a durable psyche decision about where
intent-alignment guidance lives; reversing it is reversing the psyche, not
refactoring a doc. An agent doing this autonomously would be rewriting the
intent layer to suit a downstream doc edit, which inverts the precedence the
contract sets. The correct path is to reload `skills/intent-log.md` +
`skills/spirit-cli.md` and act only on explicit psyche go-ahead, using the
psyche's verbatim testimony — not to infer the supersede from the weave.

### The two coordinated Spirit sweeps (S1, S2)

Both are psyche-authorized in principle (`6-handoff.md:52-66`) but execution
is not autonomous — each `Supersede`/`ChangeRecord` must use the psyche's
verbatim testimony, and per-record judgement calls need confirmation in-pass.

- **S1 `primary-ptvb.9`** — coordinated pass retiring "beads" → Mind/memory/weave
  across `ypg9, el7z, krez, j028, mi6m, pm1b, 3w61, wgii` (+ guardian
  siblings). Intent-side of the rename; gates W8.
- **S2 `primary-ptvb.10`** — coordinated pass retiring the designer/operator
  distinction across `ahop, kxzh, zjop, irmw, jq8w, ty8z`. Independent in the
  weave. Per-record decision: retired vs dormant-for-routing — the guardian
  reports these still actively use the distinction, so the psyche confirms
  each in-pass.

### The downstream doc items (W6, W7, W8)

- **W6 `primary-ptvb.6`** — blocked by W1-W5 + S3; AND the shrink itself
  reshapes the contract surface (psyche-authority). Keystone above.
- **W7 `primary-ptvb.7`** — blocked by W1-W4; sharpen every `skills.nota`
  description for standalone pickability. The single human-interaction line is
  pre-drafted (`5-...:59-64`), but the full pass is open editorial design.
- **W8 `primary-ptvb.8`** — blocked by W6, W7, S1; roll Mind/memory/weave
  across settled docs and retire "beads". Done last so it doesn't churn.

W2/W3/W4 (the intent-log / spirit-cli / session-lanes cuts) are now
unblocked and ready, but are classified **needs-psyche / interactive design**:
each is genuine editorial design (which sections collapse to pointers vs stay
load-bearing, where the ~120 misplaced spirit-cli lines move), not the
transcription of a pre-drafted deliverable. They follow the W1 recipe
(`6-handoff.md:95-108`) but the specific keep/collapse/pointer decisions are a
fresh design call.

## Graph health after this pass

`bd dep cycles` → `No dependency cycles detected` (clean). W1
(`primary-ptvb.1`) is CLOSED and `bd ready` correctly surfaces its three
previously-blocked dependents — `primary-ptvb.2` (W2), `.3` (W3), `.4` (W4) —
with no active blocker, and omits `.1` itself. W5 (`primary-ptvb.5`) is CLOSED
but still BLOCKS W6 (`primary-ptvb.6`), which is expected and consistent. The
live graph now matches `4-weave.md` with W1 and W5 closed.

## Remaining ordered next steps

1. **W2/W3/W4** (`primary-ptvb.2/.3/.4`) — ready now; interactive editorial
   cuts of intent-log / spirit-cli / session-lanes following the W1 recipe.
   Independent of each other; all three unblocked by the W1 close. (If the
   session-lanes W4 lands, fold the already-landed rec4 Fleet text into the
   same pass for coherence — rec4 is already in the file.)
2. **S3** (`primary-ptvb.11`) — psyche-authorized `ky10` reconcile + land the
   minimize-AGENTS.md principle. Gates W6. Spirit-authority; do not execute
   unprompted.
3. **S1** (`primary-ptvb.9`) — psyche-authorized beads-vocabulary sweep. Gates
   W8. Spirit-authority.
4. **S2** (`primary-ptvb.10`) — psyche-authorized designer/operator sweep.
   Independent. Spirit-authority; per-record retire-vs-dormant confirmation.
5. **W6** (`primary-ptvb.6`) — only after W1-W5 + S3 close: the AGENTS.md
   shrink + dispatch-override rewrite. Psyche-authority surface.
6. **W7** (`primary-ptvb.7`) — only after W1-W4 close: the full skills.nota
   description-sharpening pass.
7. **W8** (`primary-ptvb.8`) — only after W6, W7, S1 close: the
   Mind/memory/weave vocabulary rollout across settled docs.

Optional, flagged not acted on (audit finding #4): if the psyche wants the
bead graph itself reproducible from git rather than only from local Dolt
state, decide on a tracked export (e.g. JSONL). Until then `4-weave.md` is the
durable git-side record and should be kept accurate.
