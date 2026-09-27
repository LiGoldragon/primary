# Fable Start and acceptance gates

Prepared read-only for a future named owner. No Flow, Message, Herdr, Claude,
or messenger command was run for this report.

## Status and scope

The compact packet is published in Primary commit `f444851f0` under
`flows/38f337/fable-launch/`. It declares `claude-fable-5-1`, `medium`, five
leading skills, one compact launch source, and a 713 UTF-16-unit composed
Claude line. That is a source claim, not a Start or acceptance receipt.

Its own README attributes the composition reproduction to Flow `0.17.2`.
The requested installed target is described elsewhere as Flow-next `0.17.1`.
This review did not locate the installed 0.17.1 source revision or an
installed-profile composition oracle. Therefore the claimed 713 count is not
version-matched acceptance evidence for the proposed Start.

## Ordered future sequence

| Boundary | Responsible owner | Required evidence before crossing it | Hold / failure action |
| --- | --- | --- | --- |
| 1. Profile freeze | Named source owner and independent reviewer | Immutable profile revision; exact Flow 0.17.1 source revision and deployed bundle directory; oracle-rendered full line has no CR/LF, at most five leading slash skills, exact receipt footer, and UTF-16 count at most 800. | Do not submit Start. Correct the profile and remeasure. The 106-unit head is not the full composition. |
| 2. Model and native-login preflight | Named launch owner, witnessed by the living or authorized native observer | Exact native model string `claude-fable-5-1`, effort `medium`, and a login-screen observation that the existing Claude configuration is usable. No credential bytes are read or copied. | Missing/variant model or no login observation blocks Start. |
| 3. Claude V2 and isolation preflight | Flow/Herdr implementation owner | A version-matched Claude adapter can create a fresh native session, clear inherited Claude job/session state, claim a fresh Flow ID, set `PsycheV2.{ Fable <id> }`, and read both native title and Herdr pane label back without changing a sibling title. | Block Start if any part is absent. Existing evidence identifies no proven Claude V2 title adapter and no non-overlap routing guard. |
| 4. Single Start submission | Authorized launch owner under a fresh narrow lock | Gates 1-3 plus an explicit launch grant. Submit exactly one profile; Flow must record native launch intent, create the pane/harness, observe a binding, claim/register the fresh Flow ID, title it, resolve native skills, and submit the first prompt once. | No manual first-prompt retry. A composition refusal before reservation returns to boundary 1. |
| 5. Native receipt and `Started` | Flow Nexus plus independent observer | The native transcript shows the exact first composed body/hash and each required native skill receipt, including `main-flow` first; Flow records the target receipt and answers `Started`. A useful reply is observed, not inferred from a status poll. | An ambiguous delivery remains under the Nexus watcher; preserve its request ID and inspect settlement rather than submit Start again. |
| 6. Separate routes | Named Message/HM owner | After `Started`, title/binding readbacks, and the useful reply, make a fresh HM registration and verify a routed useful reply. Do not adopt `8904b1`'s Flow ID, native thread, title, Herdr pane, HM row, or route. | No registration or route transfer from predecessor. A historical native reply is insufficient. |
| 7. External remote control | Remote-access owner and external client | A separately observed external attach to the newly named remote-control surface. The existing Ouranos Herdr receipt establishes host-side access only, not a connected laptop client. | Keep the new seat unaccepted for remote-control purposes until the external observation exists. |
| 8. Crossover and later reap | Fable/Psyche seat, then Field Luna only on a later Psyche instruction | Once the successor has observed readiness, predecessor `8904b1` is silent/crossover-only and answers successor questions only. A later Psyche-to-Field instruction is recorded before Field Luna reaps it. | No automatic reap and no route adoption. Preserve both seats if that later instruction is absent. |

## Flow source ordering and ambiguity

The locally inspected Flow source is newer than the claimed 0.17.1 target, so
it is explanatory only. In it, the Nexus observes and records the native
binding before it registers the Flow, titles the claimed Flow/pane, resolves
native skills, and submits the prompt. `Started` follows observed receipt,
not merely pane creation. It also has an internal watcher that can promote a
`StartAmbiguous` launch when the receipt arrives. That supports a safe
reconciliation rule: retain the request ID and watch/query its settlement;
never issue a duplicate Start or type the first prompt manually.

If a future exact 0.17.1 oracle differs in API or ordering, that source wins
and this sequence must be revised before any action.

## Unsupported or missing gates

- No version-matched installed 0.17.1 composition oracle or source revision
  was located by this review.
- No current proof shows a Claude launcher that both creates the fresh seat
  and writes and reads back the V2 title without sibling effects.
- No proof establishes a non-overlap routing guard between successor and
  predecessor.
- The exact HM registration API and a current external remote-client witness
  are not established here.
- The compact packet's README says no Nexus-produced composition or Start was
  run. Its 713 count must be independently reproduced against the actual
  deployed configuration.

## Stop and rollback boundaries

Before reservation, correction is source-only: revise and measure; do not
retry. After native harness creation but before `Started`, keep the durable
attempt state and obtain an explicit owner decision before any stop or reap;
do not infer that an ambiguous result failed. After `Started`, preserve the
successor and predecessor separately until the observed-reply, HM, remote,
crossover, and later Psyche-directed reap gates are met.

## Living-word boundary

The actual records used here support refresh and non-waking Fable context,
not a specific Start or retirement. On 2026-09-26 the living said, “Everything
that has a big context should be refreshed and everything that has been
abandoned needs to be reaped” (`flows/93ba9f/vision/flowLaunching.md:5-7`,
STT, direct to Psyche Opus 93ba9f). On 2026-09-25 the Fable-specific record
says, “I don't want to wake up Fable but you can communicate with Field. I
would like it to be refreshed...” (`flows/e51411/vision/refresh.md:39-43`,
STT inferred reconstruction from the e51411 transcript). Neither quote by
itself authorizes this Start, route change, or reap.

## Sources

- `f444851f0:flows/38f337/fable-launch/{README.md,profile.json,sources.md}`.
- `flows/56ae53/summary.md:10,30,38-40` and
  `flows/56ae53/receipts/{roster.md,remote-access.md}`.
- Flow source inspected read-only: `crates/flow-nexus/src/{composition.rs,launching.rs,title.rs,herdr/launch.rs}` in `/git/github.com/LiGoldragon/flow`.
- Psyche provenance listed in the Living-word boundary above.
