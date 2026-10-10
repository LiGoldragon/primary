# Quota Protocol (draft, for the living)

Flow 6cc91b, read at 2026-09-14T18:30:58Z. Part 1 is what was witnessed on this
host just now; Part 2 is proposal, none of it yet acted on.

## Part 1 — how each quota is read, and current values

### Codex — WITNESSED

Method: JSON-RPC 2.0 over a WebSocket handshake on the Unix socket
`/home/li/.codex/app-server-control/app-server-control.sock`, using the `WS`
class in `flows/024bc7/tools/codex_wake.py` (`initialize` then `initialized`).
The exact method name was not in any prior log or report; it was found by
calling a guessed method and reading the server's `-32600 unknown variant`
error, which lists every valid method. The right one is **`account/rateLimits/read`**
(no params). `account/usage/read` and `account/read` are siblings, also read.

Current reading, `account/rateLimits/read` -> `rateLimits.primary`:
- **used 25%**, window 10080 min (7 days), **reset 1789830328 = 2026-09-19T15:05:28Z**
- plan: pro. `codex_bengalfox` (GPT-5.3-Codex-Spark / "Sol"-tier) sub-limit: 0% used,
  5h window resets 2026-09-14T23:30:48Z, 7-day window resets 2026-09-21T18:30:48Z.
- `account/usage/read` today's bucket (`2026-09-14`): 40,229,218 tokens so far.

For comparison, flow bcd02a read the same field at 2026-09-13T19:52:49Z as
"weekly used 7%, reset 1789830328" (`flows/bcd02a/log.md` line 32) — same reset
instant, so the same weekly window; used climbed 7% -> 25% in ~23 hours, well
over 14%/day.

### Claude — PARTIALLY READABLE, live only

`claude --help` has no `usage`/`status`/`quota` subcommand (checked full
Commands list). `~/.claude/settings.json` sets `statusLine.command` to
`~/.claude/statusline.sh`. That script reads its **current values from stdin
JSON that Claude Code itself feeds it on every statusline render** — not from
a file:
`.rate_limits.seven_day.used_percentage`, `.rate_limits.seven_day.resets_at`,
plus `.context_window.used_percentage`, `.model`, `.effort.level`,
`.thinking.enabled`. So the quota **is** exposed, but only live, per-render,
to whatever process Claude Code invokes as the statusline — there is no
persistent cache. Searched `~/.claude/` for a statsig/usage cache: none
exists (no `*statsig*` path anywhere under `~/.claude` or the filesystem
generally); the only `seven_day`/`rate_limits` hits outside `statusline.sh`
are minified JS schema fragments inside old subagent tool-result transcripts
(grep artifacts of someone once reading Claude Code's own bundled `cli.js`),
not live values. **Conclusion: not readable by this subflow right now**; it
would be readable by adding a small hook/wrapper that captures one
statusline stdin payload from a live interactive/print session and logs it.

### Today's subflow count / model mix — PARTIAL, method differs from brief

The brief assumed `.../6cc91bd5-*/tasks/*.output`; the real directory is
`.../6cc91bd5-d4d4-4b16-9642-34b4c9579ef4/subagents/`, one `.jsonl` +
one `.meta.json` per launch (noted as a correction, not followed literally).
Listing only, no transcript content read:

- **43 subagent launches** recorded for this flow (39 with today's mtime).
- Model mix: WITNESSED via the `model` field in `meta.json` for 21 of 43
  (`sonnet` x11, `haiku` x1, fork `inherit` x10 — fork inherits the parent's
  model, Sonnet/"Fable" per `settings.json`). The other 22 have no `model`
  field and CLAIMED-by-inference from `agentType` against the frontmatter
  read in Part 2(b): `read-ordinary` x7 -> sonnet, `write-demanding` x5 ->
  opus, `read-demanding` x4 -> opus, `general-purpose` x5 -> built-in, not
  defined under `.claude/agents/`, presumed to default to the session model
  (sonnet). Best-effort total: **Sonnet ~33, Opus ~9, Haiku ~1** of 43 — the
  22 without an explicit field are inference, not witness.

## Part 2 — protocol draft

### (a) Rhythm
Target **14% of the weekly window per harness per day**, so both meet near
empty at the week's reset. Track `used% / days_elapsed_in_window` against 14;
call a harness "ahead" above it, "behind" below. Whichever harness is
*behind* gets more proof-of-concept driving room that day (per the living:
shift POC work to the harness with room) — the ahead harness drops to small/
trivial jobs or pauses new POC starts until the gap narrows. Recheck at each
day boundary in the reset's timezone (UTC, per the reset timestamps read
above) and once at the week boundary as the explicit meeting point.

### (b) Tiering, mapped to the existing subagent types

| Job size | Claude (this flow's types) | Codex |
|---|---|---|
| Big, custom-prompt, wants its own judgment | `read-demanding` / `write-demanding` -> **Opus** (`.claude/agents/read-demanding.md`, `write-demanding.md`: `model: 'claude-opus-5'`) | **Astra** (main model), medium effort |
| Small, approach known | `read-ordinary` / `write-ordinary` -> **Sonnet** (`model: 'claude-sonnet-5'`) | **Luna** (cheap support), medium effort |
| Trivial, fully specified | `read-trivial` / `write-trivial` -> **Haiku** (`model: 'claude-haiku-4-5'`), Sonnet acceptable | Luna, or the smallest Codex offers |
| High-effort override | any of the above at `effort: high/xhigh` | **Sol** (`codex_bengalfox`/Spark), only under the explicit high-effort protocol (`flows/024bc7/vision/effort.md`: reserved for quota-running-out, not routine) |

All six frontmatter files (`read-trivial.md`, `read-ordinary.md`,
`read-demanding.md`, `write-trivial.md`, `write-ordinary.md`,
`write-demanding.md`) default `effort: medium`, matching "right now we are
in medium mode."

### (c) Priority and update frequency
Core and primary first: agree ideas/POCs directly from primary (highest-tier
model, highest update frequency — same-day, driven live). Secondary next:
production/at-scale implementation of what primary already agreed (daily-to-
weekly cadence, ordinary-tier models by default). Tertiary and quaternary:
lowest frequency (weekly-or-slower, trivial-tier unless a demanding job is
specifically escalated) — "frequency of update" means how often that layer's
artifacts are expected to move at all, not how fast any single job runs.

### (d) Accounting
Record per job: `harness, layer, flow_id, model, effort, tokens_or_proxy, timestamp`.
Proposed as a datom struct (see the `datom` skill for the dialect):

```
QuotaEntry.{ harness layer flow model effort tokens_or_proxy at }
; harness: Claude|Codex   layer: Core|Primary|Secondary|Tertiary|Quaternary
; tokens_or_proxy: Tokens.<int> when known, else Proxy.«description»
```

Where: a flat-file datom log under primary (e.g.
`flows/<id>/reports/quotaLog.datom`, append-only, one `QuotaEntry` per line)
is proposed over a message's-store Datom record, since quota accounting must
survive independent of any single conversation and be greppable across
flows the way `flows/bcd02a/log.md` already is; a message-store record can
mirror it later if the living wants richer querying. Who writes it: the
dispatching flow writes an entry at dispatch (harness, layer, flow, model,
effort planned, timestamp) and appends/updates it at return (tokens or the
best proxy available — for Codex, `account/usage/read`'s daily bucket delta;
for Claude, subagent count/model-mix as read in Part 1 until a real token
figure is captured). The daily 14% check reads `account/rateLimits/read`
for Codex directly (witnessed above) and, for Claude, sums that day's
`QuotaEntry` proxies against yesterday's baseline, reporting both harnesses'
percent-of-14% to the living once a day and once at week's end.

### (e) Five smallest witnesses that the protocol works
1. WITNESSED — Codex weekly usage is machine-readable right now via
   `account/rateLimits/read` (25% used, resets 2026-09-19T15:05:28Z).
2. WITNESSED — the same reset instant was read twice a day apart (7% at
   2026-09-13T19:52Z, 25% now), proving the window and delta are real and
   trackable.
3. WITNESSED — the Claude/Codex tiering already exists in code:
   `.claude/agents/*.md` frontmatter models line up exactly with the
   trivial/ordinary/demanding -> haiku/sonnet/opus mapping proposed above.
4. WITNESSED — this flow already produced 43 dispatched subagents today with
   a partial, filterable model-mix trail (`subagents/*.meta.json`), i.e. a
   count/model proxy is already sitting on disk without new tooling.
5. CLAIMED, not yet witnessed — that a `QuotaEntry` datom log written at
   dispatch/return would actually let a daily script compute both harnesses'
   %-of-14% automatically; no such script exists yet, this is the smallest
   next build, not something already proven.
