# Quota time metrics: deterministic snapshot design

This design handoff records implementation directions, not a decision about a
personal routine, overnight allocation, or alert policy.

## What one snapshot can say

Each provider limit and window remains separate. A raw observation carries its
provider, account/home, limit/window identifiers and scope; used and remaining
quota shares; observation time; reset and duration facts; and their source
bases. Provider percentages never become an absolute-capacity comparison.

The component derives independent facts when their operands are known:

| Display | Operand(s) | Meaning |
|---|---|---|
| Remaining | Current quota share | Provider-reported fraction still available. |
| Duration left / local reset | Reset instant plus observation instant | Clock countdown and exact local reset. Available even if period duration is unknown. |
| Remaining-time budget | Remaining share and positive countdown | `r / T`: percentage points per clock hour/day to use the remaining share by reset. Allowance, not observed burn or forecast. |
| Optional elapsed reference | Fixed period semantics, reset, duration | `e = (W - T) / W` and `u - e`. Only when the source establishes a fixed period. |

Use basis points internally. State the unit beside every rate, round only for
display, and retain raw basis-point/second operands in the reply. Reset
instants currently have second resolution; an exact local rendering is exact
to that source precision, using configured local timezone rather than an
invented zone.

`ResetCountdown` already distinguishes `Pending`, `Passed`, and `Unknown`.
Keep those outcomes visible. A passed reset is not zero and an unknown reset is
not a duration. Retain source, freshness, duration basis, unreadable usage,
and invalid-input outcomes; never silently substitute zero. A quota share
outside the valid range is unreadable/invalid, not an apparently empty budget.

Simple per-window display:

```text
Claude / weekly / primary: 40% remaining · 5h left · resets 02:00 local
  use remaining by reset: 8 percentage points/hour
  elapsed-window difference: unavailable (period semantics not established)
```

The values are hypothetical: `40 / 5 = 8` percentage points per clock hour.
They imply neither a provider limit nor a recommendation to use quota.

## Period semantics and three distinct comparisons

A reset and stated duration suffice for a remaining-time budget. They do not
prove that `R - W` is a fixed-window start. Support `u/e` only when provider
period semantics establish a fixed period; a named window or inferred duration
does not prove this for rolling/moving windows.

| Comparison | Formula | Question answered | Prerequisite |
|---|---|---|---|
| Cumulative position | `u / e` | Used share relative to elapsed fixed-window share? | Valid fixed elapsed-period reference. |
| Recent rate vs full-window uniform | `b_recent / b_W`, `b_W = 1/W` | Recent measured consumption above original uniform rate? | Compatible history and valid fixed `W`. |
| Recent rate vs remaining budget | `b_recent / (r/T)` | Recent measured consumption above current allowance? | Compatible history, remaining share, countdown. |

Do not collapse these into a generic “burn multiple.” The established weekly
reference is uniform `100/7%` per day; “14%/day” is its approximation. It is
window-local. A Claude-minus-Codex percentage gap proves neither balance nor
capacity because windows, resets, scopes, and denominators can differ.

## Optional planning projection

A declared planning schedule is a separate projection over provider facts. If
present it may calculate planned-use time left and its budget rate; it never
replaces the clock countdown or clock-time rate.

The profile requires explicit IANA timezone, recurrence, DST/ambiguous-local-
time behavior, version, and validity interval. Without it return `not
configured`/`unavailable`. Do not learn a schedule from prompt timestamps,
reread routine history, infer sleep, equate unscheduled time with human
absence, or apply a default unattended-work coefficient.

For a hypothetical 21:00–02:00 reset window, a profile explicitly selecting
only 21:00–22:00 yields five clock hours and one planned-use hour. At 40%
remaining this displays 8 percentage points/clock hour and 40 percentage
points/planned-use hour. It does not say autonomous overnight work is
unavailable; allocation there is policy. With zero planned-use hours, the
planned-use rate is unavailable, never infinity.

Visuals compare normalized shares: actual `u` against cumulative planned share
`q(t) = A(start,t) / A(start,R)`, with `A` the profile’s weighted opportunity
integral. A separate actual-clock timeline shows when those hours fall. Do not
place raw opportunity hours and quota percentage on one axis, or show `ON
PACE` without named thresholds and policy source.

## Historical rate and runway

Recent rate/runway need Persona-supplied samples for the same account,
provider, limit, window, and scope. That history must handle reset boundaries,
gaps, correction/non-monotonic observations, and zero rate. With a positive
compatible observed rate `b_recent`, runway is `r / b_recent` in time units;
otherwise it is unavailable, not a prediction.

Harness therefore receives compatible samples or their typed result if later
built. It creates no ledger, timer, sampler, or model call. The SRE `1/12`
short/long relation is alert confirmation heuristic, not approved 1h/12h
quota sampling cadence.

## Contract and verification boundary

Current typed vocabulary already includes `WindowUsage`, `ResetBasis`,
`ResetCountdown`, `WindowDurationBasis`, `BudgetDerivation`, and
`WindowFreshness`. Make countdown and remaining-time budget independently
expressible rather than require duration for both. Add only typed provenance
and unavailability required for these distinctions; do not invent dates or
durations.

Independent tests should cover: pending/unknown/passed reset; known reset with
unknown duration; zero/negative countdown; unreadable share; supported versus
unsupported period semantics; rounding; absent schedule and zero planned
hours; compatible versus reset-crossing/gapped/corrected historical samples.
No test is proposed for waking hours, overnight budget, thresholds, or sample
intervals.

The sole unresolved living question is the actual planning profile and whether
unattended work shares or reallocates budget. Ledger location and technical
sampling are architecture decisions deferred without a user decision.

## Sources

- `flows/28d847/reports/quota-pacing.md` — prior pacing analysis; active
  schedule and unattended terms remain policy candidates, not facts.
- `/git/github.com/LiGoldragon/harness/src/usage/pace.rs` — current operands
  and precision behavior.
- `/git/github.com/LiGoldragon/signal-harness/ethos/signal.ethos` — current
  reset, duration, usage, freshness, and budget vocabulary.
- [Google SRE Workbook: Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
  — budget-rate concept; `1/12` is not quota-sampling evidence.
- [A Practical Guide to Budget Pacing Algorithms](https://arxiv.org/html/2503.06942)
  — forecast-shaped allocation needs a valid supply forecast; prompt timestamps
  do not establish human presence.
