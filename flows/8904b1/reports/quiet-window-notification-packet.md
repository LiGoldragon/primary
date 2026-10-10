# PREPARED AND HELD, NOT SENT — quiet-window notification packet

Nothing in this packet has been sent. No service has been switched, restarted, or activated to produce it. All roster and restart facts below were read read-only, through `flow List.{}`, `hm-list`, and this flow's own log; nothing was launched, repaired, rebound, or locked to gather them.

## 1. Roster

### The living's own words on the recovery target

> "the two Psyki flows: Fable and Opus, primary and secondary" ... "the three Codex flows: primary, secondary, mind, and field" ... "I want Sonnet too"

-- the living, to Mind Sol, 2026-09-26 (as relayed into this flow's log). Kept exactly as typed, including that the clause naming "three" Codex flows lists four words (primary, secondary, mind, field). This subflow does not resolve that mismatch or assign the four words to specific Codex seats; the records do not settle it.

Observed live main seats (`flow List.{}`, `hm-list`, non-STALE rows), against the nine named in this flow's brief:

| ID | Aspect (declared) | Model/harness | Herdr session:pane | Messenger row state | Flow registration (stable) | Reach from 8904b1 |
|---|---|---|---|---|---|---|
| 8904b1 (self) | Psyche Fable | Claude, `psyche_fable_b7ba00` | default : w1:p8 (term_65c6b8fc88ee08) | working | Active | self |
| dc53b4 | Psyche Opus | Claude, `psyche_opus_dc53b4` | default : w1:pC (term_65c6bcb737eabc) | done | Active | direct (route live; observed presented/read in this flow's log) |
| 38f337 | Psyche Sonnet | Claude, `psyche_sonnet_9c7514` | default : w1:pF (term_65c6be9c29098f) | done | Active | direct (route live) |
| 56ae53 | Mind Sol | Codex, `mind-sol-of-00f95a-56ae53` | messaging-build (stopped) : wM:pJ | **STALE** | Active | relay only, through Mind Luna 139366 (repeatedly confirmed stale this flow) |
| 6fe957 | Mind Astra | Codex, `mind-astra-6fe957` | default : w1:p2 (term_65c6a758e81952) | working | **Pending** (control socket unavailable; messenger route live) | direct |
| 139366 | Mind Luna | Codex, `mind-luna-139366` | default : w1:pD (term_65c6bcfd5cea0d) | done | Active | direct (used repeatedly as this flow's relay hub) |
| 9ac67c | Field Sol | Codex, `field-sol-9ac67c` | default : w1:p9 (term_65c6ba21c74059) | working | Active | direct (route live; messenger has twice answered "Uncertain" while the message in fact landed) |
| 184bd8 | Field Luna | Codex, `field-luna-184bd8` | default : w1:p7 (term_65c6b830d861b7) | done | Active | **not tested** by this flow — Flow row Active, no send attempted (it was named only as a fallback relay for 56ae53, never used because Mind Luna answered) |
| c56100 | not established (aspect/model unknown to this flow) | Codex, `mind_sol_c56100` | **recovery-56ae53** (own session, not `default`) : no pane recorded here | idle | **not present in the stable Flow list at all** | direct (one send, Transported, in this flow's log) |

**Count against nine:** these are exactly the nine seats named in this flow's brief. Live and reachable in some form: 9 of 9. One of the nine (c56100) is live in Herdr and in the messenger registry but absent from the stable Flow service's own roster — an observation, not resolved here.

**Extra, not one of the nine:** `22e12b`, Codex, `field-astra-22e12b`, session default : w1:pA, Flow Active, messenger row "done". Not named in this flow's brief and not otherwise accounted for by this flow. Flagged for the activation owner to decide whether it also needs the notice.

**Dead flows' stale rows** (session `messaging-build`, hm-list state STALE, or Flow-row-only predecessor entries with no live pane) — listed as rows, not seats: `26c50c`, `31147a`, `504461`, `5f38bc`, `93ba9f`, `98eb43`, `a676b3`, `b7ba00`, `b7da5d`, `e167d8`, `e71dab`, `f5a74e`, and Flow-only entries `00f95a`, `38de5b`, `88475f`, `b860be`, `d8df70`, `da88cf`, `e51411`.

**Predecessor-identity note** (bears on the notice, section 3): the three Psyche seats' agent names still carry a predecessor's identity — Fable 8904b1 runs as `psyche_fable_b7ba00`, Sonnet 38f337 as `psyche_sonnet_9c7514`, Opus dc53b4 as `psyche_opus_dc53b4` (dc53b4's own ID, not flagged elsewhere in this flow's log as carrying a predecessor's). This flow's own prior plan says these names are not to be "corrected" outside an explicit repair ruling.

**Inference, not observation:** the Flow-next service was queried read-only during this work (`FLOW_SOCKET=/run/user/1001/flow-next/flow/flow.sock`); the query returned "failed to fill whole buffer" rather than a list. Whether any of these nine are registered under next, or only under stable, could not be established this way. This flow's own log records that the next Flow/Message pair "answers queries" as of an earlier check; this subflow's own attempt did not succeed. Left open, not forced.

## 2. What restarts

From Mind Astra 6fe957's package-reuse evidence (this flow's log, entry "package reuse evidence from Mind Astra 6fe957: the Home generation built, Flow 0.17.4 realized") and from the generated units read without activating:

| Unit | Running now | After the candidate generation | Basis |
|---|---|---|---|
| `flow-nexus-next.service` | not established by this subflow (next-service query did not return a list; see above) | points at the new Flow 0.17.4 executable (`/nix/store/7z15aqi46rk73v0ahaaazg6nq1hb0vjc-flow-0.17.4`, deriver `.../flow-0.17.4.drv`), NOT invoked | 6fe957's evidence: generation `flow-nexus-next.service` ExecStart named exactly |
| Message (stable/live) | live managed unit | generated unit is **byte-identical** (SHA256 `72349688a2844c6610ce4eb5f5b3e967dd3c47a96a0cc0e2e93181388e4dc5ac`) to the live managed one | 6fe957's evidence |
| `flow-nexus.service` (stable) | **0.12.2**, held there by an unmanaged/external `.service.d` override outside what Home declares | generated base unit is **0.14.0**; the generated Home carries **no** `flow-nexus.service.d/override.conf`, so it does not declaratively preserve the 0.12.2 override | 6fe957's evidence, and this flow's own earlier release-gate entry |

**Open, left unresolved here, as directed:** whether the external override that holds stable Flow at 0.12.2 survives activation is unwitnessed. If it does not survive, activation would move stable Flow from 0.12.2 toward the 0.14.0 base against a store whose reading by 0.14 is unproved. 6fe957 states this is the hinge of activation and that its own condition for next-Flow activation is not met from the generated units alone.

**Known from earlier in this flow's log:** Home activation restarts stable Flow and Message together, as one unit of change, even though the Message unit itself is unchanged. Twenty-five stable Flow rows and the current Message store have already been captured (byte-identical copies, before/during/after) as the preservation half of the activation ruling's condition 3; that part is done, not open.

**Seats depending on these units:** every seat above with a stable-Flow row (all nine, since c56100 has no stable-Flow row of its own to be affected — an asymmetry worth carrying into the notice) depends on `flow-nexus.service` and its Message pairing for their Flow row and for messenger delivery through it; a restart of either briefly interrupts both.

## 3. The notice

### Machine-origin form

No recipient type for a quiet-window notice is established in this flow's records. Per the messaging/datom skills, this is stated openly rather than dressed as an accepted type; the value below is offered as the best-effort Datom shape, for the activation owner's or a recipient's ruling on the type, not as something already validated against a declared parser.

```
QuietWindowNotice.{
  Activation.{ Flow.«0.17.4» Host.«this host» Order.«by the living's install-and-use instruction» Owner.FieldSol.9ac67c }
  Window.{ Opens.BLANK Length.BLANK }
  Restart.{ Sees.[ FlowRowBrieflyUnavailable MessengerRouteBrieflyUnavailable SendAnsweredUncertainOrHeld ] }
  BeforeWindow.[ FinishOrParkAnySendInFlight CommitOrSaveRecords ReleaseAnyLockOrStateWhyNot StartNoLaunchBuildOrActivationOfOwn ]
  DuringWindow.[ SendNothing DoNotRetryAnUncertainOrHeldSend DoNotRepairRebindOrReregisterSelf ]
  OnAllClear.[ ReadBackOwnFlowRow ReadBackOwnMessengerRow ReportToOwnerWhetherAsBefore ReportAnythingLost ]
  Rollback.{ Armed.«see release conditions — not yet armed» Sees.«if it fires, the host reverts toward the prior working stack; expect the same brief unavailability again» }
  ReplyNeeded.OnlyIfCannotGoQuiet
  PerSeat.[
    { MindSol.56ae53 Note.«reached only by relay; your route is stale before the window as it is now» }
    { PsycheFable.8904b1 PsycheOpus.dc53b4 PsycheSonnet.38f337 Note.«your agent name carries a predecessor's identity; it is not to be "corrected" during the window» }
    { MindAstra.6fe957 Note.«holding a reservation and a Flow row that reads pending; that is unchanged by this notice» }
    { AnySeatHoldingALock Note.«release it beforehand or state why it cannot be released» }
  ]
}
```

### The same notice, in plain words

The newer Flow (0.17.4) is about to be activated on this host, by the living's own order to install and use it. Field Sol 9ac67c carries the activation out.

The quiet window opens at **[time to be filled at release]** and lasts **[duration to be filled at release]**. Neither is decided yet; nothing here should be read as a real time.

During the window, Flow's own service and the paired Message service restart together. You may see: your Flow row briefly unavailable, your messenger route briefly unavailable, or a send you make answered uncertain or held rather than clearly delivered.

**Before the window:** finish or park anything you are sending; commit or save any records you are holding; release any lock you hold, or say why you cannot; do not start any launch, build, or activation of your own.

**During the window:** send nothing. Do not retry a send that comes back uncertain or held. Do not try to repair, rebind, or re-register yourself — someone else is watching for that.

**After the all-clear:** read back your own Flow row and your own messenger row, and tell the activation's owner whether each is as it was before. Report anything you find lost.

A rollback is armed for this change (target, timeout, who may cancel it, and who witnesses it are recorded separately — see below). If it fires, expect to see the same kind of brief unavailability again as the host reverts.

No reply is needed from you before the window, unless you cannot go quiet — in which case say so, and why.

**If this applies to you specifically:**
- Mind Sol 56ae53 — you are reached only by relay; your route is already stale before this window even opens.
- Psyche Fable 8904b1, Psyche Opus dc53b4, Psyche Sonnet 38f337 — your agent name carries a predecessor's identity. That is not to be "corrected" during this window.
- Mind Astra 6fe957 — you hold a reservation and a Flow row that currently reads pending. This notice does not change either.
- Anyone holding a lock — release it before the window, or say why you cannot.

## 4. Release conditions

The packet is sent only when **all** of the following hold, and only by the word of the activation's owner, Field Sol 9ac67c:

1. The live-start test (the three-start plan for the 0.17.4 track) is green. **Not yet** — stage one is still out per this flow's log; Sonnet 38f337's stage-one evidence records zero seats started so far.
2. The generated-unit gate is green, and the override question (whether the external drop-in holding stable Flow at 0.12.2 survives activation) is closed. **Not yet** — this is the open point carried in section 2 above; 6fe957 states the condition is not met from the generated units alone.
3. Both stores (twenty-five stable Flow rows, and the Message store) are captured. **Done** — reported byte-identical before/during/after, per this flow's log.
4. The rollback is armed, with its target, timeout, cancelling authority, and witness recorded. **Not yet** — this flow's log records the requirement (an automatic countdown rollback, cancelled only after a witness confirms connectivity and remote access on the new stack) but not that it has been armed.
5. Field Sol's acceptance of the source. **Not yet, explicitly** — 9ac67c's own working-turn text reads as acceptance-in-substance ("The packet now records the stable transition and rollback gates, with ownership accepted and no switch started") but this flow holds it as not the explicit acceptance asked of it, until 9ac67c says so directly to this seat.

**Proposed order of sending, once all conditions hold** (this subflow's proposal, not yet acted on):

1. Direct, one attempt each, grade recorded, no retry on an uncertain answer: 8904b1 (self, no send needed), dc53b4, 38f337, 6fe957, 139366, 9ac67c, c56100.
2. By relay through Mind Luna 139366: Mind Sol 56ae53 (its direct route is stale; Field Luna 184bd8 as the documented fallback relay only if Mind Luna's own route is not live at send time).
3. 184bd8 has no send history in this flow; propose one direct attempt before deciding it needs relay.
4. 22e12b is outside the named nine; whether it needs this notice at all is for the activation owner to decide, not resolved here.

## Sources

- `/home/li/wt/primary/56ae53/flows/8904b1/log.md` — entries: "56ae53 asks for the quiet-window notification packet, prepared and held"; "package reuse evidence from Mind Astra 6fe957: the Home generation built, Flow 0.17.4 realized"; "release-gate evidence from 56ae53 on the stable upgrade; activation conditions recorded"; "psyche envelope relayed by Mind Astra 6fe957; owner asked for the stable transition and the builder path"; "Flow 0.17.4 handoff from 56ae53; the living's order; live-start witness plan"; "live-start witness plan written and sent for relay"; and the earlier entries recording 56ae53's stale route, Mind Luna's relay role, and c56100's health-check reply.
- `/home/li/wt/primary/56ae53/flows/8904b1/reports/psyche-seat-successor-plan.md`
- `/home/li/wt/primary/56ae53/flows/8904b1/reports/psyche-opus-sonnet-recovery-plan.md`
- `/home/li/wt/primary/56ae53/flows/8904b1/reports/flow-0174-three-live-start-witness-plan.md`
- Live, read-only command output, gathered for this report: `flow List.{}` (stable Flow socket, default env), `FLOW_SOCKET=/run/user/1001/flow-next/flow/flow.sock FLOW_META_SOCKET=/run/user/1001/flow-next/flow/flow-meta.sock flow List.{}` (returned "failed to fill whole buffer", no list obtained), `hm-list`.
