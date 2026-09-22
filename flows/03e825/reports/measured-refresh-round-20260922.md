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

Selection: **PENDING**. The preparation cohort contains five candidates;
execute-selected remains empty pending the actual threshold, profile, route,
and acceptance gates. The cohort is `6db4fe`, `753e69`, `9ddcbc`, `1b8ac0`,
and `0625c3`; cohort membership is not selection.

Measurements: **PENDING** qualifying threshold evidence. The supplied
2026-09-22T14:29:23.217Z snapshot contains fresh passive route/context
observations, but its OpenAI values are last-input proxies and its Claude
values are bounded transcript-tail proxies. Neither establishes the strict
thresholds. No candidate is threshold-eligible from this snapshot.
The snapshot records `e798f3` at `195484` as a last-input proxy; an earlier
below-100000 summary for that route was erroneous. This correction does not
turn the proxy into threshold proof, and `e798f3` remains excluded as stale.

Individual refreshes: **NOT RUN**.

Readiness: **NOT CLAIMED**. This ledger records authorization and gates only;
it is not a native, route, delivery, or paired-readiness receipt.

The current owner context is unavailable from this snapshot. The three Field
owner addenda declare actual occupancy **UNKNOWN** for `6db4fe`, `753e69`, and
`9ddcbc`; their `114638`, `151173`, and `166338` values remain last-input
proxies. The Psyche High/Low captures are source addenda, not occupancy or
threshold proof. A declaration may honestly be an estimate or `unknown`; it
must not be labeled native occupancy proof.

The message worker delivered one substantive preparation request to each
candidate before any individual refresh. All five owner preparation addenda
and source receipts are now captured in this round:

| Owner | Addendum receipt | Incorporation state |
| --- | --- | --- |
| `6db4fe` | `refresh-round-20260922/root/addendum-1.md` + `root/source-receipt.json` | captured; relay conditions accepted for incorporation, not native acceptance |
| `753e69` | `refresh-round-20260922/field-medium/addendum-1.md` + `field-medium/source-receipt.json` | captured; relay conditions accepted for incorporation, not native acceptance |
| `9ddcbc` | `refresh-round-20260922/field-retained/addendum-1.md` + `field-retained/source-receipt.json` | captured; retained operator conditions accepted for incorporation, not Medium-seat transfer |
| `1b8ac0` | `refresh-round-20260922/psyche-high/addendum-1.md` + `psyche-high/source-receipt.json` | captured; source capture, not occupancy or readiness proof |
| `0625c3` | `refresh-round-20260922/psyche-low/addendum-1.md` + `psyche-low/source-receipt.json` | captured; source capture, not occupancy or readiness proof |

Field `03e825` accepts responsibility for incorporating the owner-authored
work and relay conditions. That acceptance does not establish native
acceptance, resident context, route transfer, target-work acceptance, or
readiness. The three Field addenda are incorporated as immutable source
inputs; they do not authorize launcher-profile or native-receipt changes.

`753e69`'s owner checkpoint reports `wQ:pA` as `pane_not_found`, so current
route health needs a fresh gate before any launch. `9ddcbc` has no accepted
external profile in its addendum and requires a valid actual threshold
witness; the `753e69` profile must not be reused. Root `6db4fe` remains the
network/guest forwarder and preserves VM scope `4373`; retained `9ddcbc`
remains a separate operator route and does not occupy the `753e69` Medium
slot. Psyche High/Low capture owns its four captured files exclusively; this
round does not edit them.

The message worker has now delivered each preparation request once through
HM to the exact bound target pane. These are delivery/presentation receipts,
not authored-addendum receipts and not target Read or Acceptance:

| Candidate | Native ID | Target | Delivery state |
| --- | --- | --- | --- |
| `6db4fe` | `01a0c44c-784a-7fc1-bd0a-65c6db4fe4f8` | `wK:p2` | HM submitted, exact target presented; not Read/Accepted |
| `753e69` | `01a0c4ad-12bd-74c2-9c21-7a4753e69b3d` | `wQ:pA` | HM submitted, exact target presented; not Read/Accepted |
| `9ddcbc` | `01a0c051-d38e-7d92-a79e-c609ddcbc64b` | `w0:p2` | HM submitted, exact target presented; not Read/Accepted |
| `1b8ac0` | `1b8ac00b-6c92-47d2-9d50-47d9428c0956` | `wD:p6` | HM submitted, exact target presented; not Read/Accepted |
| `0625c3` | `0625c31b-798d-44f7-a116-44a7966fe618` | `wD:p7` | HM submitted, exact target presented; not Read/Accepted |

Exact binding and absence of a hold were verified for these deliveries. The
five candidates remain unselected pending current owner-context declarations,
authored addenda, and acceptance evidence.

Automatic selection excludes stale `b80e55`, `e798f3`, and `0347d0`, as well
as historical retained routes `98ac2e` and `9e7ea5`. `0ab019` has no native
ID and is not selection proof. These exclusions do not reap or withdraw any
route. The retained `6db4fe` route remains eligible for consideration without
creating a thirteenth slot, subject to the same owner and profile gates.

The census worker must append qualifying evidence before selection or
threshold results are treated as settled. Any later refresh receipt must
identify selected exact native IDs, exclude inactive or historical records,
show strict comparisons, include owner-context declarations and addendum
receipts, and preserve the profile gates above. No automatic selection is
made from unknown occupancy or proxy values.

## Census source artifact

The preserved source artifact is
`refresh-round-20260922/mind-dispatch-census.json`. It is an exact copy of
`/tmp/mind-dispatch-census.json`, SHA-256
`8a918e459012f864099b0e0ddbb00adb4e0721ff31b8ad0d1bff81ace95dcf69`.
The artifact reports `observed_at` `2026-09-22T14:29:23.217Z`, Herdr at
`14:29:22.655Z`, HM at `14:29:22.657Z`, `exact_routes: 16`, and
`native_context.observed: 15`. It was observed by `vm_runtime_witness`; this
report attributes those facts to that artifact and does not present them as
an independent census run by Field `03e825`.

The artifact’s 16 exact route bindings are listed below. `proxy value` is
reported for provenance only and cannot satisfy the round thresholds.

| Flow | Native ID | Route owner/name | Observed at | Method | Proxy value | Status |
| --- | --- | --- | --- | --- | ---: | --- |
| `0ab019` | unavailable | `mind-astra-of-893603` | unavailable | unavailable | unavailable | exact |
| `1b8ac0` | `1b8ac00b-6c92-47d2-9d50-47d9428c0956` | `flow-1b8ac0` | `14:29:22.660Z` | bounded exact session JSONL tail | 523609 | proxy |
| `b80e55` | `b80e5510-ebe7-436e-9259-2a47735f232d` | `flow-b80e55` | `14:29:22.663Z` | bounded exact session JSONL tail | 247178 | proxy |
| `0625c3` | `0625c31b-798d-44f7-a116-44a7966fe618` | `flow-0625c3` | `14:29:22.666Z` | bounded exact session JSONL tail | 270450 | proxy |
| `98ac2e` | `01a0bcaa-6dcb-7c93-a9e2-49f98ac2e0e5` | `mind-astra-of-0ab019` | `14:29:22.669Z` | app-server thread read plus rollout tail | 116704 | last-input proxy |
| `6db4fe` | `01a0c44c-784a-7fc1-bd0a-65c6db4fe4f8` | `flow-6db4fe` | `14:29:22.669Z` | app-server thread read plus rollout tail | 114638 | last-input proxy |
| `9e7ea5` | `01a0bcea-a838-7421-ab1d-43c9e7ea522d` | `mind-astra-of-98ac2e` | `14:29:22.669Z` | app-server thread read plus rollout tail | 121255 | last-input proxy |
| `4b0f60` | `01a0c0d3-2fc6-7660-ba29-cd64b0f60e7d` | `flow-4b0f60` | `14:29:22.669Z` | app-server thread read plus rollout tail | 77899 | last-input proxy |
| `2c61af` | `01a0c492-7939-7081-82d7-a512c61af5e0` | `flow-2c61af` | `14:29:22.670Z` | app-server thread read plus rollout tail | 72352 | last-input proxy |
| `e798f3` | `01a0c0be-910a-7ea2-a956-1b4e798f39f3` | `flow-e798f3` | `14:29:22.670Z` | app-server thread read plus rollout tail | 195484 | last-input proxy |
| `23d977` | `01a0c0c0-3c39-77b3-a25f-51623d97706d` | `flow-23d977` | `14:29:22.698Z` | app-server thread read plus rollout tail | 85187 | last-input proxy |
| `03e825` | `01a0c4a7-2590-7ae3-8625-bee03e82586d` | `flow-03e825` | `14:29:22.698Z` | app-server thread read plus rollout tail | 49291 | last-input proxy |
| `753e69` | `01a0c4ad-12bd-74c2-9c21-7a4753e69b3d` | `flow-753e69` | `14:29:22.699Z` | app-server thread read plus rollout tail | 151173 | last-input proxy |
| `0347d0` | `01a0c0f9-c28a-7cd3-a3eb-ac60347d0559` | `flow-0347d0` | `14:29:22.699Z` | app-server thread read plus rollout tail | 123150 | last-input proxy |
| `c88918` | `01a0c00e-605e-7f23-91db-814c8891898f` | `flow-c88918` | `14:29:22.699Z` | app-server thread read plus rollout tail | 43618 | last-input proxy |
| `9ddcbc` | `01a0c051-d38e-7d92-a79e-c609ddcbc64b` | `field-medium-9ddcbc` | `14:29:22.706Z` | app-server thread read plus rollout tail | 166338 | last-input proxy |

## Sources and coordination

- Living authorization relayed to Field `03e825` for one measured refresh
  round and the stated threshold, selection, profile, predecessor, and
  protected-scope rules.
- Orchestrate `Observe.Locks` read before reservation, followed by
  `Locked.{ 4492 MeasuredRefreshRoundReceipt20260922 03e825 [
  /home/li/primary/flows/03e825/reports/measured-refresh-round-20260922.md ]
  ... }`.
- Orchestrate `Locked.{ 4494 FieldMeasuredRefreshRound03e825 03e825 [
  /home/li/primary/flows/03e825/refresh-round-20260922 ] ... }`, retained as
  the cooperative sole-controller reservation; it is not atomic Flow
  `BeginRefresh`.
- Captured immutable owner sources: `root/addendum-1.md` from source commit
  `a45f69fac17eb81012c3ca12658652c9b7ff4f76`,
  `field-medium/addendum-1.md` from current source commit
  `09074869b294648dc535803126cb351b024e2f8d` (the uncaptured `3618aed4`
  version is superseded), and `field-retained/addendum-1.md` from source
  commit `1cb65aa2ce684ffeb919c390bd56e317672bfbcd`. Their adjacent
  `source-receipt.json` files record source paths, SHA-256 digests, byte
  lengths, remote ancestry, and the occupancy/proxy boundary.
- Psyche High and Psyche Low addendum/source-receipt pairs were captured by
  their exclusive capture worker in this round before this ledger update.
  Those four files were not edited here; they remain source captures rather
  than occupancy, native acceptance, or readiness proof.
- `/home/li/primary/flows/6db4fe/reports/curriculum-testing-continuity-2026-09-22.md`, branch `field/curriculum-testing-continuity-6db4fe`, commit
  `f55f0118`: authored `c9`, disposable `66 skills/23 roles`, Low `a818`
  shape-only evidence, missing Primary worker procedure, and no native tester
  expansion or acceptance. This continuity evidence is not an owner addendum
  receipt or native readiness proof; its source-side lock context was `3825`
  held by root Codex and `4491` released. Existing 03/Medium/Low lanes remain
  in place and no new writer is implied.
- Existing Field handoffs and reports naming the retained `6db4fe` flow,
  the protected VM scope `4373`, and the separate writer/network lanes; these
  remain context only and were not edited by this receipt.
