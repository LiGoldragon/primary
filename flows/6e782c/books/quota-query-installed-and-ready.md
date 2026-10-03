<!-- to-the-living:start -->
Presentation.{ «Quota query: installed and ready» }

### 1. One call now works

```text
harness-usage
```

It reports Claude and Codex subscription quotas, reset times, remaining-time allowances, and session-context observations. Field confirmed the installed client and daemon work together.

For a typed reply:

```text
harness UsageSnapshotQuery
```

### 2. Read amount and time together

The display keeps remaining quota, time left, and the local reset time together.

**Hypothetical example:** 40% left for five hours means 8 percentage points per hour to use that remainder by reset. That is a budget calculation, not measured consumption or an exhaustion forecast.

### 3. The limits stay visible

Exact Claude context percentage and verified flow bindings are unavailable. Money and credit values are not modeled yet.

Planned-hours pacing and historical burn forecasts are not implemented. Missing information is reported explicitly rather than invented.

### 4. The next refinement is optional

The installed tool needs no schedule decision.

For an additional planned-hours view: **which usage intervals should it plan around, and should it reserve a share for autonomous overnight work?** The plan can cover one upcoming stretch rather than a recurring routine.
<!-- to-the-living:end -->
