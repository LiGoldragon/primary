# Field census and passive checkup deployment — 2026-09-20

Owner: Field Medium `9ddcbc`. Living request: periodic six-group system census
to Field Low/Ultra Low and a three-aspect checkup with eventual ultra-low wake.
Design owner: Mind `4b0f60`, contract
`flows/4b0f60/reports/field-census-and-checkup-architecture.md` at
`7b0f443fe995099cad71e0999dc0f074d0e69169`.

## Deployed and witnessed

- `tools/field-census.mjs` on remote main from `a63e08b0d`, later refined at
  `77dce6793` and `902c79ad5`: Herdr agent/pane lists and screens, exact HM
  tuple, native UUID, transcript availability/mtime, Orchestrate lock owners,
  host resources, and Nix daemon. The first complete live pass took 85–97 ms;
  this is an observation, not a guaranteed duration. Six historical HM records
  without native UUIDs remain visible as provenance gaps.
- `tools/field-census-cycle.mjs`, unit/timer, and tests on remote main
  `f5de6bd73`; explicit systemd tool PATH fix `9733d6cca`. The enabled
  `field-census.timer` samples every five minutes. The cycle atomically
  publishes `~/.local/state/field-census/latest.json` by temporary write and
  rename. It sends a short pointer every 1800 seconds to current Field Low
  `0347d0` and Ultra Low `c88918`, configured in
  `~/.config/field-census/recipients.json`. An uncertain send creates a durable
  hold and is not automatically retried. Two live interactive submissions and
  a separate systemd-run submission both returned HM's submitted-only result;
  no read or task completion is claimed. The service returned success with
  `ExecMainStatus=0` after the PATH fix.
- Passive three-aspect adapter, unit, and tests on remote main `ebc7c0907`,
  refined at `6e3ee046b`. Enabled `field-checkup-shadow.timer` runs every
  thirty minutes and consumes the shared census snapshot without another
  probe. Its current roster expectation is
  `~/.config/field-checkup-shadow/roster.json`; latest result is
  `~/.local/state/field-checkup-shadow/latest.json`. The service returned
  success, `ExecMainStatus=0`. It performed zero wake and lifecycle calls.
- Six targeted tests passed on current main. Remote-main hashes were checked
  with `git ls-remote` after each authored commit. Primary was clean after
  commits. Existing `core-heartbeat.timer` (five minutes) and monitoring-only
  `core-checkup.timer` (thirty minutes) remain active; their units and policy
  were not changed. `core-checkup` wake remains disabled.

The census observed 19 panes, 17 named agents, 13 exact HM bindings, 11 stale
registrations, and six unbound panes at the initial live pass. These are not
ready-main or closure counts. The passive checkup observed exact roster
coverage Field 3/4 (High HM mismatch), Mind 3/4 (Medium undeclared), Psyche
2/4 (Low HM mismatch, Ultra Low undeclared). All aspects were `DutyUnknown`
because no authoritative duty grant was configured. The current Flow Low owner
`0347d0` received the result as a submitted HM message and retains one-at-a-
time lifecycle sequencing.

## Remaining activation path

Mind's contract permits shadow monitoring now. Autonomous wake needs typed
desired-duty authority, fresh complete relevant-aspect evidence, pending-work
classification, current exact Flow resolution, one durable wake episode per
aspect and occurrence, Message request/receipt reconciliation, and target
acceptance/report evidence. A transport `Accepted` receipt is submission only.
No HM auto-wake path was installed.

Mind re-witnessed retained writer `f72ab7` via `0ab019` with Flow,
signal-flow, and Message locks. Reviewed isolated `message@9330640` and
`signal-message@7f2fc2d` have `Deliver` keyed by source event and
`QueryDeliveryReceipts`; installed binary parity and stable binding across
refresh remain unverified. Wake payload types belong to `signal-checkup`.
Continue through the published Mind contract and coordinate with retained
owners before integrating or changing the running Message/Flow services.

Mind's later read-only owner/interface return gives exact current
Orchestrate locks `2836` Flow, `2862` signal-flow, and `2864` Message to
`f72ab7`, with contact only through the retained `0ab019` child handle. Its
status-only relay was submitted, not answered at this writing. The reviewed
Message API adds a read-only receipt query by source event and target flows;
it has no subscription or global receipt discovery. Same source id and same
payload replays a stored receipt; changed payload conflicts. Missing receipt
or query failure never authorizes a new event id. An accepted adapter receipt
is transport submission, not target acceptance. `SubmitStamped` remains
unimplemented. Flow `ResolveRecipient` and conflict-protected registration do
not establish a durable wake lease or ready generation. The isolated
cross-refresh hold/reattach draft still lacks accepted binding proof.

Next implementation work can start with new `signal-checkup` duty, occurrence,
pending, episode, and outbox types plus shadow fixtures. A stable source event
per immutable wake envelope is a proposed mapping until the retained Message
owner accepts it. The target application acknowledgement/report protocol,
installed Message parity, isolated replay tests, durable binding gates, and
configured duty authority must precede wake activation. Do not substitute
an HM or untyped JSON sender.

## Twelve-cell structural amendment

The living added the literal four-power × three-aspect pane invariant, logged
at `flows/b80e55/vision/twelveMainsProportionalAssignment.md`. Mind published
its amended contract at `e066bd04553578efa7c1645f1fa57c9cf42dc277`.
Field added the read-only `StructuralReport` projection on remote main
`05f41fadfda5a480e03a70207e09b2f61021e5e0`. It counts distinct physical
Herdr pane/terminal instances, maps each expected cell uniquely, reports
unmatched cells as gaps and every unmatched pane as a ghost, and retains
protection/disposition without inferring removal authority. Harness health,
screen-level model/effort hints, native-role verification, and pending response
remain separate. No numerical compute or workload ratio was invented.

A fresh service rerun at `2026-09-20T23:48:32Z` observed 19 panes, eight
uniquely mapped cells, four gaps, and eleven ghosts. Gaps: Field High and
Psyche Low stale exact bindings; Mind Medium and Psyche Ultra Low undeclared.
The eleven ghosts include protected/retained crossover and writer panes plus
two unreviewed extras. Eight mapped cells still have unknown native health or
assignment evidence, so none is claimed as a fully verified operational cell.
Literal structure is `Nonconforming`; zero launch, wake, or removal authority
follows. Eleven targeted tests passed, including twelve total with duplicate
and missing cell, eight designated plus one extra (four gaps and one ghost),
and duplicate HM joins that do not inflate physical pane count.

## Psyche Ultra Low model correction — 2026-09-21

The living corrected Psyche Ultra Low to Claude Haiku because hallucination
rate matters for psyche work. Mind and Field Ultra Low remain Codex Luna.
Direct source: `flows/b80e55/vision/haikuForPsycheUltraLow.md` at
`4b6fb2eee`. HM showed predecessor Field Low `2fe3f1` stale, so Field sent
the correction to exact live successor `0347d0` at `messaging-build/wZ:p6`,
native `01a0c0f9-c28a-7cd3-a3eb-ac60347d0559`; HM returned submitted-only.

The passive roster now declares the expected Psyche Ultra Low profile as
`Haiku`/`claude` with effort left unknown. Its binding remains null; the
structural report says `Gap/MissingBinding` and makes no readiness or launch
claim. A fresh service run at `2026-09-21T15:05:39Z` showed that profile and
retained Luna declarations for Field/Mind Ultra Low. Nine focused tests passed
for the changed checkup modules.
