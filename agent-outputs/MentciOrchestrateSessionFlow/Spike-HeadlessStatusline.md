# Spike — Headless statusline availability (bead primary-og38.1)

Question resolved with real headless `claude` v2.1.198 runs (subscription auth),
guarded against `/home/li/primary`; all runs used a temp scratchpad sandbox as
cwd, project settings, and log dir. Every claim below carries a run witness.

## Verdict (one line)

**NOT available headless — the design's sourcing must change.** The Claude Code
statusline command is **never invoked** in headless `-p` mode, so its
`context_window` / `exceeds_200k_tokens` payload — which §2d/§4b make the
*primary, always-on, mid-turn* context source — **does not exist headless.** This
is a **genuine fork the psyche must rule on** before the .4 subscriber wiring.

## What was proven, and how

### 1 · Statusline is not invoked in headless `-p` mode

Setup: a sandbox `.claude/settings.json` set `statusLine.command` to a logging
script that appends every stdin payload it receives to a log file and echoes a
status string. Then:

- Headless run 1 (`claude -p "..." --session-id <uuid> --output-format
  stream-json --verbose --model haiku --allowedTools ""`): completed, exit 0,
  real assistant output — **statusline log file was never created** (zero
  invocations).
- Headless run 2 (a `claude -p "/context" --resume <id> ...` turn): also zero
  invocations.
- **Interactive control** (same sandbox, same settings, driven over a PTY with
  no `-p`): the statusline log file **was** created, count **1**, and the script's
  echoed string `spike-statusline-ok` rendered in the TUI. This proves the config
  is valid and picked up — it is *specifically headless* that skips the statusline,
  not a misconfiguration.

Total across the whole spike: **1** statusline invocation, and it belongs to the
interactive control run. No `--print`/`stream-json` flag enables a statusline
(full `claude --help` reviewed; statusline is a TUI-only affordance).

### 2 · The `context_window` block is real — but only in the interactive payload

The interactive statusline payload (captured verbatim) carries exactly the block
§2d describes, confirming the design's field spellings against v2.1.198:

```json
"context_window": {
  "total_input_tokens": 0, "total_output_tokens": 0,
  "context_window_size": 200000, "current_usage": null,
  "used_percentage": null, "remaining_percentage": null },
"exceeds_200k_tokens": false
```

(`current_usage`/`used_percentage` are `null` here because the session had not yet
taken a turn — matching §2d's own "absent before the first turn" note.) The point
for this spike: this authoritative pre-computed block is emitted **only** to the
statusline command, which headless never calls. So headless yields **no
`used_percentage`, no `total_input_tokens`, and no native `exceeds_200k_tokens`
flag** — the exact fields §4b's 100K/200K thresholds were designed to read.

### 3 · What headless *does* expose for context size

**(a) stream-json `usage` — present, but summing it is a self-calculation.**
Every headless turn emits per-message `message.usage` and a cumulative
`usage` on the final `result` line:

```
result.usage = { input_tokens:9, cache_creation_input_tokens:4093,
                 cache_read_input_tokens:17106, output_tokens:48, ... }
result.modelUsage["claude-haiku-4-5-..."].contextWindow = 200000   ;; capacity, not used
```

There is **no single pre-labeled "used context" scalar** and **no percentage / no
200K flag**. To get the accumulated-context figure you must sum the input side
yourself: `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`
= 9 + 17106 + 4093 = **21,208 ≈ 21.2k**. That is precisely the
"derive/sum the tokens ourselves" the design **explicitly rejected**. Nuance that
softens the rejection *in the headless context*: the design's rejection rationale
was "the *transcript JSONL* is internal and version-unstable, do not parse it."
But `--output-format stream-json`'s `result.usage` is the **documented SDK output
contract**, not the internal transcript — so summing it is not "parsing the
internal format" the doc warned about. It is still *us* computing "context size"
from token fields rather than reading a labeled figure, but off a stable surface,
and it costs nothing (every turn emits it for free at turn end).

**(b) `/context` at rest — works headless and returns Claude Code's OWN figure.**
`claude -p "/context" --resume <id> ...` completed (exit 0) and returned rendered
text: **`Tokens: 21.2k / 200k (11%)`** plus a category breakdown. This is Claude
Code's authoritative number — **no self-calculation** — and it **exactly matches**
the summed usage above (21.2k). So the design's `/context`-at-rest fallback is
**available and unchanged headless**; it is the closest headless analog to §2d's
"the harness's own number, never a self-calc" principle. Cost: it consumes one
model turn per reading and is only valid at rest — but in the single-shot headless
model, between turns is the natural at-rest state anyway.

## Answering the three sub-questions

**(a) Statusline source available headless?** No. Proven: zero invocations across
two headless runs; the invocation only ever fired in the interactive control.
The `context_window`/`exceeds_200k_tokens` payload has no headless existence.

**(b) Is stream-json `usage` the right source, and does it reopen "don't
self-calculate"?** stream-json `usage` is *available and free*, but reading a
context-size figure from it means **summing input-side tokens ourselves** — which
**does reopen** the design's "never self-calculate" decision. It is a weaker
reopening than the design feared, because the source is the documented stream-json
result, not the internal transcript it warned against. The alternative that keeps
the "never self-calculate" principle intact is `/context`-at-rest (below).

**(c) Is `/context`-at-rest still a fallback, and does it change headless?** It is
**more than a fallback headless — it is the only source that yields Claude Code's
own pre-computed figure**, and it works unchanged (`21.2k / 200k (11%)`, verified
to match the token sum). What changed is the *primary*: the design made statusline
primary "because it is the only source that reports mid-turn." **Headless has no
persistent mid-turn TUI to observe at all** — each turn is a short-lived process
that runs to completion and emits authoritative `usage` at exit, then the session
is at rest. And §4b already states the staleness thresholds "only ever apply to a
session that has already stopped" (evaluated at the *next* routing decision). So
the mid-turn capability that justified statusline being primary is **largely
unneeded in the headless model** — the figure is wanted at rest, which is exactly
when both `/context` and the turn's final stream-json usage are available.

## Is this a genuine fork? Yes — escalate before wiring .4

The accepted design's §2d/§4b sourcing rests on a source that does not exist in
the direction now being built. Two honest replacements, each with a tradeoff the
psyche's stated "don't self-calculate" intent bears on:

- **Option A — `/context`-at-rest as the (new) primary and sole source.** Honors
  "never self-calculate" (Claude Code's own rendered figure). Cost: one extra
  model turn/API call per size reading; no mid-turn reading (acceptable, since
  §4b only gates at-rest routing decisions). Parse the `Tokens: Xk / 200k (N%)`
  line; the native `exceeds_200k_tokens` flag is replaced by comparing the parsed
  figure to the threshold.
- **Option B — sum stream-json `result.usage` (self-calculation, off the stable
  SDK surface).** Free (already emitted at every turn's end), no extra turn,
  reflects the last turn's full accumulated occupancy. Cost: it **reopens** the
  "don't self-calculate" decision — the workspace would compute
  `input + cache_read + cache_creation` itself. Mitigation: it reads the
  documented stream-json contract, not the internal transcript the doc warns
  against, and is verifiable against `/context`.

Both remove the statusline dependency entirely; §2d's "harness supplies a
statusline command that forwards `context_window`" and §4b's "primary source is
statusline, mid-turn" must be rewritten either way. The `ClaudeSessionObservation`
schema itself is unaffected (`accumulated_context?: ContextTokens` stays an
`Option`); only its *producer* changes.

Recommendation (for the psyche's ruling, not a decision taken here): **Option A
(`/context`-at-rest as primary)** best preserves the accepted "never
self-calculate" intent and the "the harness's own number" principle, at the price
of one extra turn per reading — which the headless single-shot model already makes
cheap and natural. Option B is the pragmatic free-and-immediate choice if the
psyche is willing to relax "don't self-calculate" now that the risky surface (the
internal transcript) is off the table.

**Escalate to the psyche before wiring the .4 subscriber `accumulated_context`
path**, exactly as the bead requires: the producer of that field changes from the
design's statusline source to one of the two above, and choosing between them (and
whether to relax "don't self-calculate") is a psyche ruling.

## Evidence / reproduction

- Sandbox (throwaway): `.../scratchpad/headless-spike/` — `.claude/settings.json`
  (statusLine → logging script), `statusline-logger.sh`, `logs/` (stream-json,
  stderr, statusline-invocations.log), `pty-interactive-control.py`.
- Headless transcripts landed at `~/.claude/projects/-tmp-...-headless-spike/`
  (outside primary; disposable).
- `/home/li/primary` untouched by any spike run (all runs cwd'd to the sandbox).
- Key numbers: turn-1 usage sum 9+17106+4093 = 21,208 (21.2k); `/context`
  rendered `21.2k / 200k (11%)`; statusline invocations — 1 total, all from the
  interactive control run.
