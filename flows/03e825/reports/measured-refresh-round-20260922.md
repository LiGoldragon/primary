# Measured refresh round ledger — 2026-09-22

This is the receipt for one living-authorized measured refresh round. Field
`03e825` is the sole lifecycle controller for the round. The authorization
does not authorize a launch, refresh execution, route change, predecessor
reaping, or readiness claim.

## Reservation and scope

Orchestrate lock `4492`, `MeasuredRefreshRoundReceipt20260922`, reserves
exactly this report path:

`/home/li/primary/flows/03e825/reports/measured-refresh-round-20260922.md`

No other owner's path, runtime, global launcher, writer, or profile is in
this reservation. Existing writers and protected work remain preserved,
including the network scope identified as `4428`, the existing guest VM
scope `4373`, and the retained partial Ultra work. No runtime action,
outbound message, launch, census invocation, or refresh was performed for
this receipt.

## Authorized selection and measurement rules

The round's strict thresholds are:

- OpenAI: usage must be `>100000`.
- Claude: usage must be `>200000`.

Only fresh passive census evidence may establish those threshold checks.
Last-input proxies, quota values, and cumulative usage are not threshold
proof. Candidate identities must be deduplicated by exact native ID, and
inactive or historical records must be excluded. Retained Field Astra
`6db4fe` may be eligible in the round without creating a thirteenth slot.

Before any individual refresh, every selected owner's authored addendum
must have been requested and incorporated. Each selected native profile
must independently carry its accepted model and effort, audited source and
skills, receipt-first startup, its own Flow ID, exact HM/Herdr binding, and
target-work acceptance. The predecessor remains preserved; there is no
automatic reaping.

## Round state

Selection: **PENDING** census-worker evidence.

Measurements: **PENDING** fresh passive census evidence.

Individual refreshes: **NOT RUN**.

Readiness: **NOT CLAIMED**. This ledger records authorization and gates only;
it is not a native, route, delivery, or paired-readiness receipt.

The census worker must append the measured evidence before selection or
threshold results are treated as settled. Any later refresh receipt must
identify the selected exact native IDs, exclude inactive or historical
records, show the strict comparisons, and preserve the owner-addendum and
profile gates above.

## Sources and coordination

- Living authorization relayed to Field `03e825` for one measured refresh
  round and the stated threshold, selection, profile, predecessor, and
  protected-scope rules.
- Orchestrate `Observe.Locks` read before reservation, followed by
  `Locked.{ 4492 MeasuredRefreshRoundReceipt20260922 03e825 [
  /home/li/primary/flows/03e825/reports/measured-refresh-round-20260922.md ]
  ... }`.
- Existing Field handoffs and reports naming the retained `6db4fe` flow,
  the protected VM scope `4373`, and the separate writer/network lanes; these
  remain context only and were not edited by this receipt.
