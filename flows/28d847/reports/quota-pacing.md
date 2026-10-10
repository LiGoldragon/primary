# Quota pacing: time left, use per time, and when that time falls

Subflow of 28d847, 2026-10-03. Answers the living's 2026-10-03 words
(flows/28d847/vision/quotas.md, "Time left, use per time, and when that time
falls"). WITNESSED = read or run here; CLAIMED = read in a source; INFERRED =
my reasoning. Nothing was built.

## 1. Earlier work, in his words

The words being answered:

> It has to also show us how much time is left and then compute all the other metrics. We looked into that before: some kind of transformation that we would put using the time. We'll refine the algorithms, but let's maybe find out what the best is for this kind of thing, to cognitively better visualize it: how much use you have per time and for how much time. That is also really important because if what I have left is until tomorrow morning, then obviously it's different than me spending it during the daytime.

-- flows/28d847/vision/quotas.md

No record names a "transformation" for quota (searched flows/*/vision,
notion, reports, Vision/, vision-raw/, ~/.claude/history.jsonl,
~/.codex*/history.jsonl). The nearest records, verbatim:

> If my quota is being unused for the daily or hourly rate, or if you divide the week by the number of hours in the week, then we would run some light encouragement to keep concepts materialized so they can be tested.

-- flows/840e42/vision/quota.md

> Well, obviously, the 5-hour window is something to contend with, and I think that it's a good gauge for maintaining a fair amount of usage for each.

-- flows/840e42/vision/quota.md

> When I ask for a report, like a situation report, which is going to be a thing, I guess, then I get the quotes for each subscription that is left, and how much that turns out to be per day, and whether or not we're above or below percentage-wise and stuff. Let's start working out how we want to visualize that best, so you could do some heuristics research on how to best represent something like that.

-- flows/692df8/vision/quota.md

> I want you to start working on a protocol for managing the quotas for the usage of both Claude and Codex, so that they are balanced and meet up at the end of the week if we use them at about 14% per day. We try to keep that rhythm.

-- flows/6cc91b/vision/quotas.md

> The hook could even give it precomputed metrics, like how much time is left and how fast we've been burning it lately. It creates a few, like 4 or 5, useful metrics.

-- flows/b05237/vision/operational-quotaBurnRateHook.md (same words in operational-quotaVisualizationHook.md)

> We can figure out our burn rate at different times and create visual graphs and correspond them with psyche activity and stuff like that.

-- flows/b81560/vision/operational-quotaBurnRateVisualGraphs.md

> It is just to keep track of whether we're in high-power mode or in low-power mode with different providers.

-- flows/b81560/vision/operational-quotaAwarenessSystem.md

> ... have some kind of a quota-gauge program that keeps running and tells people to slow down when they're over quota.

-- flows/139366/notion/quota-gauge-program.md (notion)

> Let's cash in those quotas and see what we can make of all the vision.

-- flows/b81560/vision/operational-nightWorkDirective.md, flows/f38926/vision/nightWork.md (said going to bed)

His typed prompts show the same mental model, with quota spoken of as an
amount over a stretch of his own time (WITNESSED in ~/.claude/history.jsonl;
times are America/Mexico_City). These are history rows, not psyche records:

- 2026-05-09 05:30: "I have a bunch of claude usage left for a couple hours so we could use it"
- 2026-07-11 05:45: "I have lots of cloud usage for the next two hours, so let's use it."
- 2026-07-26 02:04: "I had a job that used up several days of usage overnight."
- 2026-09-12 04:01: "continue you have 3 more hours of essentially unlimited usage."

### Algorithms already proposed

| Source | Algorithm |
|---|---|
| 6cc91b/reports/quotaProtocol.md | Even pace: 14% of the weekly window per day per harness; ahead or behind = used%/days-elapsed against 14; the harness that is behind drives proof-of-concept work. |
| 692df8/reports/quotaVisualization.md | Burn-down against an ideal line; burn multiple (SRE, 1.0x = budget hits zero exactly at reset); remaining %/day; ran %/day so far; ASCII bullet meter with a `|` marker at even pace; verdict word first; pure ASCII, bar last on the line. |
| 5f4fea/reports/quota-situation-report-a.md | That design run live: "BELOW 0.78x, may spend 16.9 %/day, ran 11.1 %/day". |
| b05237/reports/quota-anatomy.md | Five metrics: Left (% and hours to reset), Burn (%/h over a trailing window, width open: 1 h or 3 h), Pace (share used against share elapsed), Runway (hours to exhaustion at current burn against hours to reset), Balance (Claude against Codex weekly gap). Needs a sample ledger. |
| harness dc55863 src/usage/pace.rs | Built: remaining, seconds until reset, window minutes, remaining per day = r·86400/T, even-pace used = (W−T)/W, variance = used − even. |

None weights time by when he is awake. That is the new part.

## 2. Established ways to pace a budget against time

- **Burn-down against an ideal line** (Scrum; Copilot Money's spending chart: a dotted ideal line, a solid actual line, and "Free to Spend" on top). Reads at a glance, but needs a chart.
- **Burn multiple** (Google SRE Workbook, "Alerting on SLOs"): the rate relative to the one that empties the budget exactly at period end. Multiwindow form: alert only when both a long and a short window run hot, with the short window at 1/12 of the long. One dimensionless number; it is unstable early in a window, when the elapsed share is near zero.
- **Allowance per unit time** ("safe to spend per day"): remaining / time left. The most actionable single number, and it already exists as %/day.
- **Time to exhaustion / runway** (Claude-Code-Usage-Monitor: tokens per minute over the last hour, forecast cut-off time). Needs a recent-rate history.
- **Traffic-shaped pacing** (Agarwal et al., "Budget pacing for targeted online advertisements at LinkedIn", KDD 2014; Chen, "A Practical Guide to Budget Pacing Algorithms", arXiv 2503.06942, uniform vs traffic-weighted allocation): the target spend curve follows expected supply per time slot instead of clock time. **This is the formal shape of his point about nights**: the supply is his active hours.
- **Bullet graph** (Few): a bar plus a perpendicular marker for the target; it survives in ASCII.

Judgment (INFERRED). On a phone and in one line, use an allowance per unit of *active* time plus a verdict word. Then add the stretch of active time it covers and the clock time of the reset. Ratios need a mental reference ("1.0x means..."). An allowance answers his "how much use you have per time and for how much time" directly. The bullet bar is the best picture, provided its time axis is active time.

## 3. Proposed metrics

Inputs per window: u = used share, r = 1 − u, t = now, R = reset, W = window
length, T = R − t. Profile: w(τ) ∈ [0,1] = the weight that the living is
active at local time τ; Z = his time zone.

| # | Metric | Formula | Snapshot has it? |
|---|---|---|---|
| 1 | Time left | T = R − t, shown as duration and as local clock time of reset | Yes: SecondsUntilReset, ResetEpochSecond; local time needs Z |
| 2 | Left | r | Yes: RemainingBasisPoints |
| 3 | Allowance per clock time | r / T (per day for weekly, per hour for five-hour) | Yes, per day: RemainingBasisPointsPerDay; per hour by arithmetic |
| 4 | Pace gap / multiple | e = (W − T)/W; gap = u − e (points); multiple = u / e, shown only once e > 10% | Gap yes (PaceVarianceBasisPoints); multiple by arithmetic |
| 5 | Active hours left | A = ∫ₜᴿ w(τ) dτ | No: needs w and Z |
| 6 | Allowance per active hour | r / A; per active day = r / (A / Ā), where Ā = mean active hours per day | No: needs A |
| 7 | Active-time pace | e_a = 1 − A / A_W, where A_W = ∫ from R−W to R of w; gap_a = u − e_a; multiple_a = u / e_a | No: needs w |
| 8 | Unattended hours | N = T − A: hours to reset with him away, which agents alone can spend (night work) | No: needs w |
| 9 | Recent burn | b = Δu/Δt between the two most recent snapshots spanning ≥ 1 h (short) and ≥ 12 h (long), SRE multiwindow | No: the snapshot is one-shot with no store; needs a sample ledger (quota-anatomy Part 2) |
| 10 | Runway / projected end | runway = r / b; exhaustion at t + r/b; projected used at reset = u + b·T; verdict "runs out Thu 14:00, 1.6 d early" or "ends 23% unused" | No: needs b |
| 11 | Balance | Claude weekly u minus Codex weekly u | Yes, by arithmetic over both observations |

Active-hours transform, what it needs:
- **Z**: America/Mexico_City (host timedatectl, WITNESSED). A value that
  differs between setups, so it belongs in SKILL_VARIABLES.md (INFERRED,
  per the behavior skill; not decided here).
- **w declared**: e.g. active 08:00–22:00 local, by weekday. Simplest; he
  states it once.
- **w observed**: per hour of the week, the share of the trailing 4 weeks
  with at least one living-typed prompt in that hour, smoothed, with the
  declared schedule as the prior. Sources: ~/.claude/history.jsonl and
  ~/.codex*/history.jsonl carry timestamped prompts. They also carry
  agent-injected prompts (#msg, launch briefs). A rough filter over
  2026-09-05..10-03 gave 26 days. The share of days active per hour runs
  0.35–0.50 at 08–17h local and 0.04–0.15 at 21–07h. This is a proxy, not
  a witness of when he is present. A clean source needs an origin mark on
  typed prompts.
- Weekly window: w changes A a lot (a 6.7-day window holds ~160 clock hours,
  ~91 active at 14 h/day). Five-hour window: it matters only when the
  window crosses his bedtime.
- If night agent work counts toward planned spend, use
  w'(τ) = w(τ) + λ·(1 − w(τ)), where λ = the agents' unattended burn
  relative to attended burn. λ = 0 is "only my hours count"; he decides.

Worked example (WITNESSED values from flows/28d847/reports/quota-sources.md
at 2026-10-03T20:45Z = 14:45 local; w declared as 08–22 local, INFERRED):

- Claude 7-day: 11% used; reset Sat 10 Oct 07:00 local; T = 160.3 h;
  e = 4.6%, so the multiple is withheld and the gap is +6.4 pts.
  13.3%/day clock. A = 7.25 + 6×14 = 91.3 h, giving 0.97%/active h,
  13.6%/active day. N = 69 h unattended.
- Claude 5-hour: 20% used; reset 17:20 local; T = 2.6 h = A, giving 31%/h,
  all of it his time.
- His own case: at 21:00 with a five-hour window resetting at 02:00,
  T = 5 h but A = 1 h, so the per-active-hour allowance is 5× the clock
  figure. This is the difference he named.

## 4. Display

One line per window (pure ASCII):

```text
Claude wk   ON PACE  1.0%/active h  91 active h  -> Sat 07:00  (69 h unattended)
Claude 5h   LOW      31%/h          2.6 h        -> 17:20
Codex wk    BEHIND   ...
```

Verdict word first, from gap_a (thresholds to set). Then the allowance per
active hour, then how long that lasts in active hours, then the clock reset.

Phone page: per window, one bullet bar whose x-axis is active hours from
window start to reset, so nights shrink to slivers. The ideal line is straight
on that axis, the mark sits at u, and the marker at e_a. Below it, a thin
strip in clock time with nights shaded shows when the remaining hours fall.
Once a ledger exists: a projected-end segment (Few) and a runway marker.

## 5. Open for the living

1. Active hours declared, observed, or declared with observed refinement?
2. Do unattended night hours count toward planned spend (λ), or is night
   spend a separate "cash in" budget?
3. Burn window widths once samples exist (1 h / 12 h proposed).
4. Is 14%/day still the line, or does the line become even per active hour?
5. Should a sample ledger be added beside the one-shot snapshot? Recent burn
   and runway cannot be computed without it.

## Sources

flows/28d847/vision/quotas.md; flows/840e42/vision/quota.md;
flows/692df8/vision/quota.md; flows/6cc91b/vision/quotas.md;
flows/b05237/vision/operational-quotaBurnRateHook.md,
operational-quotaVisualizationHook.md;
flows/b81560/vision/operational-quotaBurnRateVisualGraphs.md,
operational-quotaAwarenessSystem.md, operational-nightWorkDirective.md;
flows/139366/notion/quota-gauge-program.md;
flows/b05237/reports/quota-anatomy.md;
flows/692df8/reports/quotaVisualization.md;
flows/6cc91b/reports/quotaProtocol.md;
flows/5f4fea/reports/quota-situation-report-a.md;
flows/28d847/reports/quota-sources.md;
flows/d66c26/reports/quota-component-design.md;
/git/github.com/LiGoldragon/signal-harness/ethos/signal.ethos;
/git/github.com/LiGoldragon/harness/src/usage/pace.rs (dc55863);
~/.claude/history.jsonl, ~/.codex*/history.jsonl.
Web: https://sre.google/workbook/alerting-on-slos/ ;
https://dl.acm.org/doi/abs/10.1145/2623330.2623366 ;
https://arxiv.org/html/2503.06942 ;
https://help.copilot.money/en/articles/6045480-dashboard-tab-overview ;
https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor