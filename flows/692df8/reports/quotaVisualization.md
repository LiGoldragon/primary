# Quota Situation Report — how to show it

Flow 692df8, 2026-09-15. How to show, in a small periodic sitrep read on a phone through Claude remote access (plain text, no images,
narrow), per subscription: quota left, the per-day rate that implies, and whether we are above or below pace. **WITNESSED** = run or
read here, now. **CLAIMED** = read in a source, not re-verified. **INFERRED** = my reasoning.

## 1. What is measurable today

**Codex — fully machine-readable. WITNESSED**, read just now over `/home/li/.codex/app-server-control/app-server-control.sock` with
the `WS` class in `/home/li/primary/flows/024bc7/tools/codex_wake.py`. `account/rateLimits/read` -> `rateLimits.primary`:
**usedPercent 32**, `windowDurationMins` 10080, `resetsAt` 1789830328 = 2026-09-19T15:05:28Z — so the window opened
2026-09-12T15:05:28Z and was **44.2% elapsed** at read. Three more fields matter: sibling limit `codex_bengalfox`
("GPT-5.3-Codex-Spark") at 0% on both a 300-min and a 10080-min window, a second independent quota on one account;
`rateLimitResetCredits.availableCount` = **3** unused "Full reset" grants (INFERRED: these are quota, count them); and
`account/usage/read` -> `dailyUsageBuckets`, per-day tokens (09-09..15 = 386.1M, 684.9M, 124.1M, 159.6M, 146.1M, 410.7M, 8.2M) — the
only per-day series either harness exposes, hence the only possible sparkline.

**Claude — live-only, still not capturable. WITNESSED (negative).** Confirming `flows/6cc91b/reports/quotaProtocol.md` and closing two
further doors: `claude --help` lists no `usage`/`quota`/`status` subcommand; `~/.claude/statusline.sh` reads
`.rate_limits.seven_day.used_percentage` and `.resets_at` per render, then discards them; `~/.claude/stats-cache.json` is **stale**
(`lastComputedDate` 2026-07-03), holding only message/session/tool counts and no rate-limit field; and this session's transcript
`~/.claude/projects/-home-li-primary/942914a6-*.jsonl` (1.0 MB) has **zero** hits for `seven_day` or any `rate_limit*` key.
INFERRED: the only cheap fix is appending the statusline's stdin to a rotating JSONL — a config change, so the living's call. Until it
exists the Claude half is blank and the display must degrade honestly rather than fake it.

**A third, open-weight seat** is absent (`tools/third-seat/` holds only `offline-adapter.mjs` and `refusal-dry-run.mjs`; CLAUDE.md
marks the private part "chartered, NOT ACTIVE"). INFERRED: build for N rows; a local seat has no quota, its scarce resource is time.

## 2. Heuristics worth borrowing (all CLAIMED, from the sources named)

- **Burn-down against an ideal line** (Scrum): remaining work against time with a straight guideline from full to zero at the deadline;
  above it is behind, below is ahead. Burn-up exists to separate scope change from progress and quota scope is fixed, so burn-down
  suffices. The ideal line here *is* the psyche's 14%/day.
- **Burn rate as a multiple** (Google SRE Workbook, ch. 5 "Alerting on SLOs"): "burn rate is how fast, relative to the SLO, the
  service consumes the error budget", normalised so **1 leaves exactly 0 budget at the end of the window**, and rate N exhausts it
  in window/N. One dimensionless number, four characters wide, whose fixed point is already the living's "meet up at the end of the
  week" — hence `0.72x`. AWS Budgets and GCP budgets split this into "actual" and "forecasted" thresholds; INFERRED, the multiple
  already encodes the forecast, so one number does both.
- **Bullet graph** (Few, *Bullet Graph Design Specification*, Perceptual Edge, rev. 2013): a bar for the featured measure plus a
  comparative measure "encoded as a short line that runs perpendicular", built to replace dashboard gauges in far less space; label
  left, bar right. Everything but the grey intensities is positional, so it survives being drawn in characters — a bar with an
  in-bar `|` marker *is* a bullet graph. Few's Optional Features section names our exact problem and splits the bar into
  actual-so-far and projected-at-period-end.
- **Sparkline and data-ink** (Tufte, *Beautiful Evidence*; *VDQI*): "a small intense, simple, word-sized graphic with typographic
  resolution"; erase every mark that is not data (at 40 columns, literal); **small multiples** wants one shared scale and bar origin.
- **The Unicode block ramps, and why I am not using them.** U+2581..U+2588 (sparklines, as in `spark`) and U+258F..U+2588 (1/8-cell
  bars) are the CLI standard, but `EastAsianWidth.txt` classes **2580..258F and 2592..2595 as `A` (Ambiguous)** — two columns wide
  in an East Asian context, which iTerm2, WezTerm and tmux each expose as a setting — while U+2590 and U+2591 (`░`) are class `N`, so
  a `█`/`░` bar mixes two width classes. r-lib's `cli` says it outright for `spark_bar()`: "in most common fixed width fonts these are
  rendered wider than regular characters which means they are not suitable if you need precise alignment." Phone markdown also sets
  body text proportionally. **This is the finding that decides the design**: the recommended report is pure ASCII, and any bar goes
  last on its line so its rendered width is never load-bearing.

## 3. Mockups, 40 columns

**A. ASCII bullet meter, verdict first — RECOMMENDED.** Every Codex number is WITNESSED; the Claude block is the honest state.

```text
QUOTA SITREP    Tue 15 Sep 17:21 UTC
Week 44% gone, 3.9 d to reset Sat.
| on each bar = where we should be.

CODEX PRO     68% left  BELOW 0.72x
  may spend 17.4 %/day to reset
  ran      10.3 %/day so far
  +3 full-reset credits in hand
  [#######..|............]

CLAUDE MAX    --% left   NO READING
  statusline capture not yet wired
  [??????????????????????]
```

Then **B**, the hardest fallback, with no bars at all; and **C**, the Unicode-block upgrade, right only once seen rendering on the
living's own phone.

```text
QUOTA SITREP  15 Sep 17:21Z  wk 44%
SUB      LEFT  /DAY   PACE   RESET
Codex     68%  17.4%  0.72x  Sat 15
Claude     --      -      -  Sat 09
                 (claude: no read)
Codex ran 10.3%/day, 32% of week.
```

```text
QUOTA 15 Sep 17:21Z  week 44% gone
codex  68% 0.72x 17.4/d ██████▍░░░░░░
       7d burn ▅█▂▂▂▅▁
claude --%    --    --/d ░░░░░░░░░░░░░
```

## 4. Why A

The job per subscription is "a single ratio against a limit", which the `dataviz` skill routes to a **meter**, not a chart; N
subscriptions make a KPI row of stat tiles, not a grouped bar. A is that, in characters. It answers the three asked questions in
reading order — how much is left, what that is per day, above or below — with the verdict word (`BELOW`) as the hero, readable
without parsing a glyph; colour is unavailable here, so the word must carry status and a bar may never carry it alone. It is pure
ASCII, so no Ambiguous-width or proportional-font failure from §2 can reach it, and the bar sits last on every line so nothing shifts
even if a glyph renders wide; widest line is 36 columns. It degrades both ways: delete the bar lines and A becomes B, swap the bar
for block elements and it becomes C.

## 5. Questions only the living can answer

1. **Cadence** — daily at a fixed UTC hour, on request only, or both? Resets are UTC, so drawing the daily line at a UTC hour keeps
   the arithmetic clean.
2. **Which subscriptions, and does Spark count separately?** Codex exposes `codex` and `codex_bengalfox` as independent limits: a
   row each, or a footnote?
3. **Confirm the pace line is 14%/day.** `flows/6cc91b/vision/quotas.md` already says "balanced and meet up at the end of the week
   if we use them at about 14% per day", so A assumes even pace. A trailing average, or a split (say 80/50), flips the verdict.
4. **Ratio or points?** `0.72x` and `-12 pts` are one fact in two grammars. A picks the ratio because 1.00x is the meeting point;
   one word settles it.
5. **What on an unreadable value** — omit the row, show the last reading with its age, or blank as in A?
6. **Should it say what to do?** A only reports, but the psyche ties quota to dispatch ("If Codex has not much usage, then Claude can
   start driving the proof of concept more").
7. **Is the statusline capture authorized?** Nothing else unblocks Claude's half.

Smallest first build, INFERRED: one script reading `account/rateLimits/read` and `account/usage/read`, computing elapsed%, pace ratio
and %/day, printing A with Claude blank — correct for one subscription on day one, second row lighting up when the capture lands.
