# claude-quota-observe

One run is one reading. The program spends one minimal Claude API turn to make the harness
report its own account's rate limits over `stream-json`, reads that one report, and says what
it saw. It never spends a credit, never holds a policy, and never loops — read-only, and the
seed of the Claude bridge's quota part, to be moved into that bridge later rather than kept
here as a standalone tool.

## Invocation

A datom-speaking CLI: one inline datom value, no flags.

```sh
node tools/claude-quota-observe/claude-quota-observe 'Observe.{ StreamJson }'
```

`StreamJson` runs, from an empty temporary directory with stdin detached and a 90-second
timeout:

```sh
claude -p --output-format stream-json --verbose --tools "" --no-session-persistence -- "Reply OK."
```

and parses its stdout for the first line whose `type` is `rate_limit_event`. Output is one
line:

```
QuotaObserved.{ <fiveHourPercentUsed> <sevenDayPercentUsed> <overagePercentUsed> <sevenDayResetsAtIso> <status> }
```

The three percentages are `utilization * 100`, rounded, for the `five_hour`, `seven_day` and
`seven_day_overage_included` entries of `rate_limit_info.unifiedWindows`; `sevenDayResetsAtIso`
is the `seven_day` window's own `resetsAt` epoch seconds as an ISO instant; `status` is
`rate_limit_info.status`, printed bare, whatever word the harness used for it (`allowed`,
`allowed_warning`, and so on — this program does not enumerate them).

Refusals, each a typed datom and each exiting 2:

```
ObserveRefused.NoRateLimitEvent            ; the stream never carried a rate_limit_event line
ObserveRefused.HarnessFailed.{ <exitCode> } ; claude itself exited nonzero
ObserveRefused.Timeout                      ; the 90-second bound was hit first
```

## The test seam

```sh
node tools/claude-quota-observe/claude-quota-observe 'Observe.{ Fixture.«<path>» }'
```

reads a captured stream file in place of running the harness — the only difference from
`StreamJson` is where the stream text comes from; the parsing and the refusals are the same
code path. This is how the tests exercise the parser without a live account, and how a captured
stream can be replayed later.

## The log

Every successful observation is appended to `$XDG_STATE_HOME/claude-quota-observe/log.ndjson`,
else `~/.local/state/claude-quota-observe/log.ndjson`, as one line:

```json
{"at":"2026-09-16T19:43:12.779Z","kind":"QuotaObserved","fiveHourPercentUsed":10,"sevenDayPercentUsed":66,"overagePercentUsed":78,"sevenDayResetsAtIso":"2026-09-19T13:00:00Z","status":"allowed_warning"}
```

Append-only; nothing is rewritten. A refusal is printed but not logged.

## Cost

Each `StreamJson` run is one minimal API turn — the model reads a two-word prompt and answers
"OK" — about $0.11 USD at list price for a cold cache. The capture in
`fixtures/real-run-2026-09-16.jsonl` ran against an already-warm system-prompt cache and so its
own `result` line reports a much smaller `total_cost_usd` of $0.0100445; list price for a cold
cache is the number to plan a call schedule against, since a periodic checkup invoked from a
fresh, empty directory has no cache of its own to warm between runs.

## Routes not taken

**The OAuth usage endpoint.** The harness holds an OAuth-authenticated usage endpoint that
would answer this same question without spending a turn, but reaching it needs the
credentials file the harness manages for itself — reading that file is exactly the kind of
secret-touching this tool is built to avoid. `StreamJson` pays a small, known, and disclosed
cost instead of reading a credential this tool has no charter to hold.

**The statusline feed.** The harness can be configured to run a statusline command that
receives quota information on stdin on every render; that path is push-driven and tied to an
interactive session's own cadence, not to a standalone checkup that runs on its own schedule
from an empty directory. It was not built here because it does not fit a program meant to be
invoked once and exit.

## Tests

`tools/claude-quota-observe/tests/claude-quota-observe.test.mjs` runs the whole program
against three fixtures in `tools/claude-quota-observe/fixtures/`: a real captured
`stream-json` run with one `rate_limit_event` line (`real-run-2026-09-16.jsonl`, captured by
hand on 2026-09-16 by running the exact harness command once against a live account), a
stream with no `rate_limit_event` line at all, and a stream truncated mid-write before one
completed. It also exercises `harness.mjs` directly against a fake `claude` binary for
`HarnessFailed` and `Timeout`, including that the timed-out process is actually killed. No
live account is touched by the tests, and no fixture's expected datom text is derived from the
parser under test. Exposed as the `claude-quota-observe-fixtures` flake check.
