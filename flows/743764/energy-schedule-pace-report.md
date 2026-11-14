# Energy Nexus: usefulness schedule and pace in useful hours (bead primary-k5q9)

The vision followed is psyche-belief `vision/energy-nexus-v1.md` as of commits 90b5bf1, 09947be and d0b875d. All three branches are named `schedule-pace`. Each was cut from its repository's `origin/main` and pushed. Nothing was merged, deployed or restarted.

| Repository | Worktree | Head |
|---|---|---|
| signal-energy-nexus 0.6.0 | /git/worktrees/signal-energy-nexus-schedule-pace | d7d9f8d5d861b484db269755d97b096fad4282ce |
| meta-signal-energy-nexus 0.6.0 | /git/worktrees/meta-signal-energy-nexus-schedule-pace | dd6ec2b8dd25fb5a1577348d1d50fbf7a2ac880e |
| energy-nexus 0.4.0 | /git/worktrees/energy-nexus-schedule-pace | 8e912232edd183a236f77e0f00ab7b148880e9c4 |

The base is `main` (0.3.2, cd4c85c), which is what runs. It is not `energy-stage-one-a9a8d6`, another flow's unmerged rewrite that has uncommitted changes in the main checkout.

## What was built

- **signal-energy-nexus.**
  - New library types: `Hours`, `Hour`, `Weekday`, `Usefulness`, `Baseline`, `Span { weekday_vector, from, to, usefulness }` and `Override { from, to, usefulness }`.
  - The wire has its own finite `Decimal`. It archives as one f64 and refuses a non-finite value. With the `datom` feature its text is datom-codec's decimal. Without it the Nexus process still carries no Datom.
  - `Pace` replaces `per_day` with `hours_left`, `useful_left` and `per_useful_hour`.
  - The comment on the `Read` line in `signal.ethos` changed, so the contract digest moves.
- **meta-signal-energy-nexus.**
  - `Set` gains `Span`, `RemoveSpan`, `Override`, `RemoveOverride` and `Baseline`, each configured one at a time.
  - `Configure.Baseline.20` and `Configure.Span.{ [ … ] 8 22 100 }` read exactly as the vision writes them.
  - Both contracts' wire fixtures were written again. Every unchanged type keeps its 0.4.0 bytes and text. The exception is that every `Set` archive grew to the size of `Span`, its largest variant.
- **energy-nexus.**
  - `crates/core/src/usefulness.rs` (`UsefulTime`) weighs time exactly, in percent-seconds. The usefulness of a moment is decided in this order:
    1. An override covering it.
    2. Otherwise, the most specific span naming the hour: fewer days, then fewer hours.
    3. Otherwise, the baseline.
  - Hours are read in the owner's local time. The daemon passes `TimeZone::system()` (jiff), which follows daylight saving.
  - `Pacing::pace` computes, for each window:
    - expected, counted in useful hours;
    - wall-clock hours left to the target's end;
    - useful hours left, to a tenth;
    - percent left per useful hour, to a hundredth.
  - Memory moves to format version 3, which adds the schedule, the overrides and the baseline. Version 2 upgrades on open to an empty schedule at baseline 100. Versions 1 and the unenveloped archive upgrade to version 3. The schedule's rules are checked on every read and before every write.
  - Also updated: the Ethos files, `energy-pace` output, README, UPGRADES and DESIGN.

## Test results (Nix on the builder)

- signal-energy-nexus: 9 tests pass. These include Pace datom text `{ Codex Week Even 25 35 Over 124 83.5 0.78 }` and the held wire.
- meta-signal-energy-nexus: 5 tests pass. These include each vision `Configure` line and the held wire.
- energy-nexus: `checks.test` passes 90 tests with no failures and no compiler warnings. `checks.nexus-dependency-boundary` and `packages.default` build.
- The module's examples, all in `crates/core/tests/useful_hours.rs`:
  - **His Codex week reads `Even 25 35 Over 124 83.5 0.78`.** Baseline 20, every day 8–22 at 100, 35% used at 13 Nov 16:50.
  - The weekend keeper, the job (Tue/Thu evenings, weekend mornings at 50) and the gradient (6–10 at 60, 10–14 at 100, 14–22 at 70) each give the usefulness the module states, hour by hour.
  - The dentist override counts 0 over a span. The week then reads 81.5 useful hours and 0.8 per hour.
  - "The same energy left reads lower with one day and two nights ahead" holds.
  - Other tests cover the specificity rule, a span past midnight, daylight saving, the configuration rules, and day order in a span.
- `memory_admission.rs` upgrades a version 2 file and keeps a schedule across a restart.

## Assumptions (where the vision is silent)

1. Pace stays per window: `Read.{ Reading Vector<Pace> }` with `Name`, as main already had. The vision's Pace names no window.
2. The owner's local time is the system time zone: `TZ`, else `/etc/localtime`. It is not a setting.
3. The default baseline is 100, so with no schedule pace reads as 0.3.x did.
4. A span covers From up to To. If To is before From, the span runs past midnight into the next day. From equal to To is refused.
5. Every usefulness and the baseline are 0 to 100, because `Usefulness` is a `Percent`.
6. Ties:
   - Two spans with as many days and as many hours: the one configured later counts.
   - Overlapping overrides: the shorter counts, then the one configured later.
   - A span's days are stored in week order, each once. An equal span is not added twice. `RemoveSpan` matches whatever order the days were given in.
7. Overrides stay in Memory until removed. Past ones are not pruned.
8. If the window holds no useful time at all, expected counts plain time. If no useful hour is left, `per_useful_hour` is the whole percent left.
9. `hours_left` and expected round half up. `useful_left` rounds to a tenth and `per_useful_hour` to a hundredth, from the unrounded useful hours.
10. Pace is computed at the reading's instant, as before.

## Design questions for Fable

1. **The second and third worked examples do not follow from their readings.** Under the module's schedule, the SpendBy reading gives `71 92 Over 67 42.8 0.19`; the module shows `88 92 Over 48 32.0 0.25`. The "Later" reading gives `Even 95 92 Under 7 5.6 1.43`; the module shows `23 92 Over 120 80.0 0.1`. That window resets about seven hours after the reading. Should these figures be recomputed, or the readings changed?
2. **The vision's Ethos declares `From` twice,** as `From.Hour` in `Span` and as `From.Instant` in `Override`, and ethos-zero refuses the duplicate. The repository's `library.ethos` names Override's instants `Since` and `Until`. The Rust fields and the datom text are unchanged. Which names should the vision take?
3. **Should the time zone be a configured setting** (e.g. `Configure.TimeZone`) instead of the system's?
4. **Usefulness above 100?** "A morning he means to work hard" cannot count above full use while `Usefulness` is a `Percent`.
5. **Should past overrides expire on their own?** Calendar-made overrides will accumulate otherwise.
6. **The vision's Pace and Read have no window.** The implementation carries Name, FableWeek and WindowTarget. Should the vision take them, or the implementation drop them?
7. **The contract digest covers only each crate's `signal.ethos`,** not the library types it imports. A change to Pace's layout moves the digest only because the comment on the `Read` line was edited. Should the library be part of the contract source?
8. **Deployment.** Both contract digests moved, so the daemon, the translator and the text clients deploy together. `energy-stage-one-a9a8d6` will need this work carried over if it lands.
