# Quota component acceptance review

## Basis and scope

This is a source-only review of the local checkout, made without running tests,
the daemon, a CLI, an installed package, or a provider query. Fixture tests are
code that specifies intended cases; they are not execution evidence here.

The desired source cohort is Harness `5a5c37` / 0.6.1,
`signal-harness` `25a2d1` / 8, and `meta-signal-harness` `939bdf` / 1.0.1.
The inspected local `signal-harness` and meta checkouts have those latter two
revisions. The local Harness checkout reports `313755e` (`Document consumers
on older signal-harness contracts`). Read-only `jj` ancestry witnesses
`5a5c37::313755` and no reverse ancestry: `313755` is a descendant of the
intended Harness revision. The path diff from `5a5c37` to `313755` changes only
`ARCHITECTURE.md`; it does not change the reviewed implementation paths
(`src/usage`, `src/daemon.rs`, `src/client.rs`, or their listed fixture tests).
This local source review is still not an acceptance witness for the activated
package revision, executable, or service configuration.

Opus's stated built-package results (typed query 606 ms, view 785 ms, and its
checks) are attributed claims, not rerun or independently verified by this
review. Coordination also records a safe rendered-view artifact at
`/tmp/claude-1001/-home-li-primary/28d847ee-f350-4a24-8cb0-0e88abf16cbe/scratchpad/live-run/view.txt`
with empty stderr files. Those artifacts alone do not establish an executable,
its revision, exit status, or timing. No raw logs or credential material was
read for this review.

## Accepted initial snapshot completion

Field `42265e` now reports that deployment 84 succeeded and generation 1046
is active, with rollback generation 1039 retained. It reports Harness 0.6.1
enabled and active with its owner-only three sockets, and reports that the
installed `harness-usage` and native typed query both succeeded. The wrapper
and daemon are reported to come from the same 0.6.1 package. One supported
initial start was required after activation; this report does not claim an
automatic start.

Field also reports that the selected Home/CriomOS configuration was published
remotely and matched the intended selection. This is execution evidence
reported by Field, not a command run by this reviewer. The retained Field
transcription is `/tmp/field-harness-deployment-result.txt`; Field says it
transcribes the executor receipt with machine identifiers omitted, rather than
being raw stdout. The original successful stdout remains in the flow-contracts
execution receipt.

Coordination's retained source-selection witness identifies published CriomOS
`0792bbf4f7d718afc505a85a05ec1d3b85d1b812`, selecting Home
`85437488dc686d8d73f1c8bb8ef330683cc0ea0a`, whose lock pins Harness
`5a5c37129f4782af075f90ae09ba7b58e73a327a`. The earlier `9b76fc` reference
is a reviewed candidate/predecessor, not the exact deployed Home. The safe
handoff transcription is 838 bytes with SHA-256
`71f51f30e86787006d1cc6cf24f9119b337f1c514ab0917a93f725033aeab0e8`.
This establishes selected source provenance and Field's reported runtime
handoff, not raw exit status, timing, or store-path receipts.

## Accepted source baseline

The typed interface has a `UsageSnapshotQuery` request and `UsageSnapshot`
event, with the request classified as `ReadUsageSnapshot`.
[`signal-harness/ethos/signal.ethos:7-29`](/git/github.com/LiGoldragon/signal-harness/ethos/signal.ethos)
and
[`signal-harness/ethos/signal.ethos:48-50`](/git/github.com/LiGoldragon/signal-harness/ethos/signal.ethos)
define these records. The Harness daemon source matches the request, takes a
fresh reader snapshot, and writes the typed reply
([`harness/src/daemon.rs:122-150`](/git/github.com/LiGoldragon/harness/src/daemon.rs)).
`harness-usage` submits that query and renders the reply; ordinary `harness
UsageSnapshotQuery` remains the native typed form
([`harness/src/client.rs:118-166`](/git/github.com/LiGoldragon/harness/src/client.rs)).

The ordinary `signal-harness` socket, rather than the owner-only meta socket,
carries the usage query. The meta socket is for the `meta-signal-harness`
contract. Transcript stream events carry their subscription token on the
ordinary watch connection
([`harness/ARCHITECTURE.md:101-113`](/git/github.com/LiGoldragon/harness/ARCHITECTURE.md)).
Thus separate socket ownership and event-token semantics exist, but a
one-shot usage snapshot is not an event carrying a subscription token.

The quota contract preserves hundredth-percent precision as basis points and
makes current, stale-after-reset, and unreadable values distinct. It also makes
pending, passed, and unknown reset states distinct; rate and elapsed
derivations carry explicit unknown reasons
([`signal-harness/ethos/signal.ethos:141-178`](/git/github.com/LiGoldragon/signal-harness/ethos/signal.ethos)).
The local normalizer derives a remainder-by-reset clock allowance from a
current share plus a pending reset without needing window duration. Uniform and
elapsed metrics become typed unknown when duration or period semantics are not
established
([`harness/src/usage/window.rs:223-305`](/git/github.com/LiGoldragon/harness/src/usage/window.rs)).
The human rendering calls the first quantity a clock allowance from one
snapshot and expressly says it is not observed burn
([`harness/src/usage/view.rs:241-260`](/git/github.com/LiGoldragon/harness/src/usage/view.rs)).

The local Claude normalizer uses the names `five_hour` and `seven_day` for
their direct stated durations, rather than deducing duration from coincident
reset timestamps
([`harness/src/usage/claude_quota.rs:28-29`](/git/github.com/LiGoldragon/harness/src/usage/claude_quota.rs)).
Codex uses a provider-declared `windowDurationMins` only when supplied
([`harness/src/usage/codex_quota.rs:209-233`](/git/github.com/LiGoldragon/harness/src/usage/codex_quota.rs)).

Collector failures are materialized as typed unavailable observations rather
than erased
([`harness/src/usage/mod.rs:111-237`](/git/github.com/LiGoldragon/harness/src/usage/mod.rs));
per-home Codex quota failures remain visible
([`harness/src/usage/codex_quota.rs:91-149`](/git/github.com/LiGoldragon/harness/src/usage/codex_quota.rs)),
as do Codex socket and Claude registry context-source failures
([`harness/src/usage/codex_context.rs:178-228`](/git/github.com/LiGoldragon/harness/src/usage/codex_context.rs),
[`harness/src/usage/claude_context.rs:170-186`](/git/github.com/LiGoldragon/harness/src/usage/claude_context.rs)).

Codex deduplicates only same returned account IDs, combines their home names,
and withholds the account ID itself from the reply
([`harness/src/usage/codex_quota.rs:117-149`](/git/github.com/LiGoldragon/harness/src/usage/codex_quota.rs),
[`harness/src/usage/codex_quota.rs:181-194`](/git/github.com/LiGoldragon/harness/src/usage/codex_quota.rs)).
Claude and Codex context set Flow identity to absent: neither a Claude session
prefix nor a Codex display name is a witnessed Flow binding
([`harness/src/usage/claude_context.rs:3-12`](/git/github.com/LiGoldragon/harness/src/usage/claude_context.rs),
[`harness/src/usage/codex_context.rs:1-10`](/git/github.com/LiGoldragon/harness/src/usage/codex_context.rs)).

`PlanningProjection::NotConfigured` is the actual sole planning variant in the
contract and is rendered as such
([`signal-harness/ethos/signal.ethos:202-203`](/git/github.com/LiGoldragon/signal-harness/ethos/signal.ethos),
[`harness/src/usage/view.rs:99-103`](/git/github.com/LiGoldragon/harness/src/usage/view.rs)).
It truthfully signals absence of a planning projection; it does not mean a
configurable planning implementation exists.

## Remaining limits and acceptance requirements

The local source retains the *names* of extra usage, spend, credits, and other
unmodelled provider facts, and renders those names. It does not carry or show
their values
([`harness/src/usage/claude_quota.rs:37-44`](/git/github.com/LiGoldragon/harness/src/usage/claude_quota.rs),
[`harness/src/usage/codex_quota.rs:22-31`](/git/github.com/LiGoldragon/harness/src/usage/codex_quota.rs),
[`harness/src/usage/view.rs:140-153`](/git/github.com/LiGoldragon/harness/src/usage/view.rs)).
That avoids silently treating financial allowances as quota windows, but cannot
serve a requested monetary or credit breakdown.

Claude context remains a proxy token count with no emitted context-window size
or exact percentage
([`harness/src/usage/claude_context.rs:3-12`](/git/github.com/LiGoldragon/harness/src/usage/claude_context.rs),
[`harness/src/usage/claude_context.rs:153-166`](/git/github.com/LiGoldragon/harness/src/usage/claude_context.rs)).
There is no verified Flow binding, actual planning projection, retained
history, or observed-burn calculation in this contract.

The current contract makes usage above 100% `PercentageAboveFull` unreadable
([`signal-harness/ethos/signal.ethos:145-146`](/git/github.com/LiGoldragon/signal-harness/ethos/signal.ethos)).
That source-domain policy does not support a conclusion that a legitimate
provider overrun cannot occur. Its upper-bound semantics remain unknown and
would need an explicit contract extension if a provider documents overrun.

At the earlier review stage, Field reported a harness-enabled Home preserving
active fixes and selected CriomOS input, while activation was still
unconfirmed. The completion addendum above supersedes that stage-specific
deployment status. The reviewed `9b76fc` candidate precedes the exact deployed
Home identified in the completion addendum; the local Harness source is a
descendant in the reviewed implementation paths. The
actual OS Router boundary
was reviewed by a sibling and remains unresolved: CriomOS's Router input is
locked at `f60d4e` on the older wire, its conditional `persona-router` service
runs under a system UID, and its actor-home endpoints are supplied by an absent
Horizon payload. The user-private `0600` snapshot socket under its `0700`
directory is neither reachable by nor intended for that system service. Do not
configure that route; a migration/access model is deferred unless that separate
integration is selected. CriomOS's `criomos-home` input at `4a52e8` must also
advance if Field activates via the OS-selected Home; the completion report says
that selected Home/CriomOS publication matched remotely. This does not
establish a Router migration.

Harness itself documents that Persona and Mentci are on pre-8.0.0
`signal-harness`, are not selected for the Home harness service, and make no
compatibility claim
([`harness/ARCHITECTURE.md:362-364`](/git/github.com/LiGoldragon/harness/ARCHITECTURE.md)).
This is bounded snapshot-service acceptance, not a claim that all consumers
have migrated or that deployment has no blockers.

The reported completion covers bounded initial-snapshot activation. It does
not expand acceptance to a full ecosystem migration. The retained Field
transcription makes the installed executable and systemd package provenance,
owner-private three-socket configuration, and human/native query receipts
auditable as reported execution evidence; it is not this reviewer's run or raw
stdout capture.

## Sources

- Local source metadata and read-only ancestry/diff: Harness `5a5c37129f4782af075f90ae09ba7b58e73a327a` is an ancestor of local `313755e97469718b8ca1cff11c2ff82a8b95d630`; the named implementation-path diff contains no changes. `signal-harness` is `25a2d18b81f26ee00caaaa875dce102beed5b6a5`; `meta-signal-harness` is `939bdf75d799706cc2a7e232d5a75e2b26775d09`.
- Field `42265e` deployment update, relayed through flow coordination; not independently activated or probed here.
- Field completion transcription: `/tmp/field-harness-deployment-result.txt`, supplied by Field and read by the main flow. Field describes it as a transcription of the executor receipt with machine identifiers omitted; original successful stdout remains in the flow-contracts execution receipt. This reviewer did not run or raw-capture it.
- Incoming Field `42265e` confirmation relayed by the main flow: deployment 84 succeeded; generation 1046 active with rollback 1039; Harness 0.6.1 active; installed human/native queries succeeded; Home/CriomOS selection remotely matched.
- Coordination's retained source-selection witness: CriomOS `0792bbf4f7d718afc505a85a05ec1d3b85d1b812` selects Home `85437488dc686d8d73f1c8bb8ef330683cc0ea0a`, pinned to Harness `5a5c37129f4782af075f90ae09ba7b58e73a327a`; safe handoff file SHA-256 `71f51f30e86787006d1cc6cf24f9119b337f1c514ab0917a93f725033aeab0e8`, 838 bytes. Relayed through coordination and not reread here.
- Sibling's source-only CriomOS Router/access review, relayed through flow coordination; its underlying source was not reread here.
- [Previous contract review](quota-contract-review.md)
- [Time-metrics design](quota-time-metrics-design.md)
