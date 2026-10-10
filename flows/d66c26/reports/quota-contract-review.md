# Source-only review: quota snapshot contract

## Method and evidence boundary

This review read the current `harness/src/usage/` implementation,
`signal-harness` authored contract, and their fixture/test source. It did not
run a test, start a daemon, call either provider, read credentials, or inspect
raw live responses.

Secondary's statements that fixtures cover every case, flake checks are green,
and a live call saw five Claude and twenty Codex sessions in 0.77 seconds are
unrerun claims. They are not evidence in this review. The checked-in live test
is explicitly ignored and prints a constructed typed response if manually run;
it is not daemon/client evidence.

## Contract facts verified from source

`UsageSnapshot` is an authored typed reply containing subscription and session
context observations. It distinguishes provider source, observation time,
quota windows, reset/duration basis, freshness, pace derivation, unavailable
provider observations, context basis, and context freshness. Its output is a
typed native reply. A concise human rendering is a proposed convenience; this
review does not require a second or parallel CLI format.

The module reads four sources concurrently and has no scheduled loop, store,
Watch, or token refresh. Claude last-request context is correctly represented
as a proxy; without the separate statusline publisher, its exact window and
percentage remain unavailable. That limitation is tolerated and must stay
visible rather than estimated.

## Required fixes

### Do not infer a duration from equal reset times

The Claude `limits[]` parser treats group `weekly` as seven days. For any
other group, it declares a five-hour or seven-day duration merely because its
reset timestamp equals a top-level named window. Same reset time does not
establish the same window duration, so derived daily pace and variance can be
false.

Required fix: only use a declared or otherwise documented source duration.
For a grouped limit with only a reset time, retain its reset as observed but
set duration and pace to typed unknown. The existing named top-level windows
can retain their explicitly named basis.

Verified locations:

- `/git/github.com/LiGoldragon/harness/src/usage/claude_quota.rs:374-388`
- `/git/github.com/LiGoldragon/harness/src/usage/claude_quota.rs:418-425`
- `/git/github.com/LiGoldragon/harness/src/usage/pace.rs:58-88`

### Preserve auxiliary allowance and spend/control facts

Claude treats `extra_usage` and `spend` as understood top-level keys, so they
are neither emitted nor retained as unknown-present. Codex similarly treats
`credits`, `spendControlReached`, and `rateLimitReachedType` as understood
bucket keys while emitting none of them. These might be distinct from quota
windows, but silent erasure prevents a full subscription/account breakdown.

Required fix: model provider auxiliary allowance, credit, and spend/control
facts separately from quota windows, or retain them as explicitly present but
unmodeled source facts. Do not synthesize a quota window from them.

Verified locations:

- `/git/github.com/LiGoldragon/harness/src/usage/claude_quota.rs:180-190`
- `/git/github.com/LiGoldragon/harness/src/usage/claude_quota.rs:473-490`
- `/git/github.com/LiGoldragon/harness/src/usage/codex_quota.rs:19-32`
- `/git/github.com/LiGoldragon/harness/src/usage/codex_quota.rs:725-729`

### Make source/collector failure visible

The aggregate reader replaces any reader-thread panic with an empty vector.
Codex context silently skips a failed control-socket open or failed
`thread/loaded/list`. A reply can consequently omit an attempted context
source rather than reporting it unavailable.

Required fix: return a typed unavailable/source-failure result for every
attempted provider, home, and context collector. Preserve its observation time
and cause. An individual failure must not remove the other provider's result.

Verified locations:

- `/git/github.com/LiGoldragon/harness/src/usage/mod.rs:122-150`
- `/git/github.com/LiGoldragon/harness/src/usage/codex_context.rs:416-438`
- `/git/github.com/LiGoldragon/signal-harness/ethos/signal.ethos:155-170`

### Do not authenticate Flow identity through the session title

Codex derives an optional Flow ID solely by accepting the final six
hexadecimal characters of the native thread name. The source neither consults
Flow authority nor proves that a displayed name belongs to that Flow.

Required fix: leave the Flow reference absent unless an exact, separately
witnessed native thread-to-Flow binding is supplied. Keep the native session
name only as display metadata.

Verified locations:

- `/git/github.com/LiGoldragon/harness/src/usage/codex_context.rs:344-353`
- `/git/github.com/LiGoldragon/harness/src/usage/codex_context.rs:399-412`

### State percentage domain and overrun semantics instead of clamping

Claude converts finite percentages to hundredths of a percentage point, as
does Codex. The contract calls those values `UsedBasisPoints`, so the
hundredths representation is coherent. The checked sources establish no
upper bound: utilization above 100 percent might represent a provider-defined
overrun. The current normalization clamps only `remaining` at zero, while
retaining the original used value, and does not distinguish a legitimate
overrun from malformed source data.

Required fix: accept only finite, nonnegative values in the provider's
documented domain. Define the upper-bound/overrun semantics explicitly: if
the provider documents overrun, expose it and derive remaining according to
that rule; if not, return a typed invalid/unreadable source state rather than
silently casting or clamping. Pace must carry the same explicit derivation.

Verified locations:

- `/git/github.com/LiGoldragon/harness/src/usage/claude_quota.rs:363-368`
- `/git/github.com/LiGoldragon/harness/src/usage/codex_quota.rs:183-204`
- `/git/github.com/LiGoldragon/harness/src/usage/pace.rs:31-52`

### Give deduplicated accounts a non-secret grouping identity

Codex deduplicates homes using the server-returned `accountId`, but the value
is deliberately never emitted. The reply contains only homes grouped in a
single `SubscriptionUsage` record; it has no stable non-secret account or
subscription grouping identifier across snapshots.

Required fix: either add an opaque, non-secret account/subscription grouping
reference, or document that the single snapshot record and its home set are
the complete grouping claim. Keep raw `accountId` redacted.

Verified locations:

- `/git/github.com/LiGoldragon/harness/src/usage/codex_quota.rs:160-168`
- `/git/github.com/LiGoldragon/harness/src/usage/codex_quota.rs:111-140`
- `/git/github.com/LiGoldragon/signal-harness/ethos/signal.ethos:127-157`

## Non-blocking limitation retained

Claude exact context percent is not currently available. The context reader
uses last assistant-request input plus cache-create/cache-read tokens, labels
the result `Proxy`, and leaves both context-window tokens and percentage
absent. This is the correct present state without a live statusline publisher;
it must remain `Unknown`/proxy, not be promoted to resident context.

Verified locations:

- `/git/github.com/LiGoldragon/harness/src/usage/claude_context.rs:1-8`
- `/git/github.com/LiGoldragon/harness/src/usage/claude_context.rs:101-120`
- `/git/github.com/LiGoldragon/harness/src/usage/claude_context.rs:184-230`

## Sources

- `flows/d66c26/reports/quota-requirements.md`
- `flows/d66c26/reports/quota-component-design.md`
- `/git/github.com/LiGoldragon/harness/src/usage/mod.rs`
- `/git/github.com/LiGoldragon/harness/src/usage/claude_quota.rs`
- `/git/github.com/LiGoldragon/harness/src/usage/codex_quota.rs`
- `/git/github.com/LiGoldragon/harness/src/usage/pace.rs`
- `/git/github.com/LiGoldragon/harness/src/usage/claude_context.rs`
- `/git/github.com/LiGoldragon/harness/src/usage/codex_context.rs`
- `/git/github.com/LiGoldragon/harness/tests/usage_sources.rs`
- `/git/github.com/LiGoldragon/harness/tests/usage_live.rs`
- `/git/github.com/LiGoldragon/signal-harness/ethos/signal.ethos`
