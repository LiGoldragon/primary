# Proposal: rolling distillation in design flows

## Problem

Raw vision accumulates faster than it is distilled. Monologues and successive sessions pile up records that overlap, supersede each other, or contradict where the living changed their mind. The existing skill says "Distillation is proposed on encounter or done in dedicated passes" but gives no cadence or active dispatch mechanism. In practice, distillation waits for dedicated passes that come too late, leaving stale and contradictory raw vision in place.

## Where this belongs

The rolling distillation protocol belongs in the **design skill** (`Curriculum skills/design.md`), not in `psyche-distillation.md` or `flows.md`. Reasoning:

- `psyche-distillation.md` defines what distillation is and how it works. It already says "proposed on encounter or done in dedicated passes." It does not need to say when flows should actively seek distillation candidates; that is a flow-behavior rule.
- `flows.md` governs all flows. Rolling distillation is a design-flow behavior: design flows are the ones that produce heavy raw vision and have the psyche present to approve proposals. Putting cadence in `flows.md` would bind all flow types.
- `design.md` governs the behavior of design flows specifically. It currently has two lines. The cadence of proactive distillation is a design-flow responsibility: while designing, vision accumulates rapidly and the living is present to approve, making it the right moment to distill.

A one-line addition to `psyche-distillation.md` strengthens the "subflow only gathers" rule to cover the dispatch pattern.

## Proposed changes

### 1. `Curriculum skills/design.md`

**Before** (full file body, lines 8-9):

```
Design fleshes out the anatomy of the psyche's vision.

Show the psyche the high-level view routinely.
```

**After**:

```
Design fleshes out the anatomy of the psyche's vision.

Show the psyche the high-level view routinely.

Every second or third turn, check whether a subject touched
heavily in this flow has raw vision accumulating across flows.
When it does, dispatch a subflow to gather all records on that
subject, then compose a distillation proposal in the main flow
for the psyche's approval before any Vision/ change.
```

What this preserves: the existing two lines are untouched.

What this adds: a cadence rule (every second or third turn), a trigger (subject touched heavily with raw vision accumulating), a mechanism (subflow gathers, main flow composes the proposal), and a gate (psyche approves before Vision/ changes). This last gate already exists in `psyche-distillation.md` but is restated here because the cadence makes it load-bearing: agents proposing frequently must not land anything without approval.

### 2. `Curriculum skills/psyche-distillation.md`, line 36

The existing line already covers the concept. The change makes it explicit that proactive dispatch from a flow is the primary mode, not an afterthought.

**Before** (line 36):

```
Distillation is proposed on encounter or done in dedicated
passes.
```

**After**:

```
Distillation is proposed on encounter, dispatched proactively by
the flow working a subject, or done in dedicated passes.
```

What this preserves: "on encounter" and "dedicated passes" remain valid modes.

What this adds: "dispatched proactively by the flow working a subject" as a named mode, bridging to the design skill's cadence rule.

### 3. No change to `Curriculum skills/flows.md`

The rolling distillation is design-flow behavior. The flows skill already establishes the subflow mechanism and the vision-record placement. No change needed.

### 4. No change to `Curriculum skills/psyche-interraction.md`

The distillation-proposal workflow (compose, show to psyche, get approval) is already defined in `psyche-distillation.md`. The interraction skill governs logging, not distillation dispatch. No change needed.

## Mechanism summary

1. A design flow, every second or third turn, notices a subject it has touched heavily.
2. It dispatches a subflow to search `flows/*/vision/`, `psyche-raw/`, and `Vision/` for all records on that subject.
3. The subflow gathers candidates and returns them to the main flow (per existing rule: "A subflow only gathers records that could qualify as candidates for distilling together").
4. The main flow composes a distillation proposal from those candidates (per existing rule: "A distillation is composed only in the main flow").
5. The proposal is shown to the psyche for explicit approval before any Vision/ change (per existing rule: "A distilled statement lands in Vision/<topic>.md on the living's explicit approval, and never before").

No new machinery is introduced. The proposal activates existing distillation mechanics on a regular cadence within design flows.

## Sources

- `/git/github.com/LiGoldragon/Curriculum/skills/design.md` (current full body)
- `/git/github.com/LiGoldragon/Curriculum/skills/psyche-distillation.md` (distillation protocol, line 36 on modes, lines 10-16 on subflow/main-flow split)
- `/git/github.com/LiGoldragon/Curriculum/skills/flows.md` (flow structure, subflow relationship)
- `/git/github.com/LiGoldragon/Curriculum/skills/psyche-interraction.md` (logging protocol)
- `/git/github.com/LiGoldragon/Curriculum/skills/subflows.md` (subflow authority)
- `/git/github.com/LiGoldragon/Curriculum/skills/documentation-placement.md` (placement principle)
- `/home/li/primary/flows/06196cc7/vision/psycheLogStructure.md` (lines 59-89, prior ruling: "distillation is ongoing")
- `/home/li/primary/flows/b675f3d9/vision/distillation.md` (placement ruling: proposals must say where each statement goes)
