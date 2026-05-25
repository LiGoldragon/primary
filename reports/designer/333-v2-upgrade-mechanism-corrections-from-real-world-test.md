*Kind: Errata + Findings · Topic: corrections to /333 from end-to-end nspawn test · Date: 2026-05-25 · Lane: designer*

# 333-v2 · Upgrade mechanism — corrections from the verification subagent's real-world test

## §1 Frame

`/333` is the design narrative for the upgrade mechanism. The verification subagent at `~/wt/github.com/LiGoldragon/CriomOS-test-cluster/spirit-full-ceremony-e2e` (branch pushed; commit `25d07c98`) exercised the FULL ceremony end-to-end on Prometheus via criomos-nspawn, using operator's just-landed v0.1.0.1 + current v0.1.1. Every ceremony phase emitted witness output. The test passed at the `(SpiritFullCeremonyNspawnTestSucceeded record_count=3)` line — but ALSO uncovered a critical wire-compatibility gap and three semantic gaps the design narrative didn't surface.

`/333` stays as the design vision. This `-v2` is the errata + findings layer; future readers should consult `/333` for the model + `/333-v2` for what actually happens when the model meets the code.

## §2 The critical finding — wire incompatibility between v0.1.0.1 and v0.1.1

**`persona-spirit` v0.1.0.1 and v0.1.1 cannot exchange handover frames as currently built.** The two daemons bind their three sockets, but the frames they emit are mutually unparseable.

- **v0.1.0.1** (operator/178, persona-spirit commit `e7a1b184`, tagged `v0.1.0.1`): built against signal-frame `653773b7` (PRE the ShortHeader commit).
- **v0.1.1** (persona-spirit main): built against signal-frame `1493c59f`, which includes commit `18c22d8` "signal-frame: add frame short header".
- The new ShortHeader is an 8-byte prefix prepended to every wire frame. v0.1.0.1 emits frames without it; v0.1.1's frame parser decodes the body bytes as the ShortHeader (eight bytes interpreted as the wrong record), then attempts to decode the rest as `HandshakeRequest` and fails.

The existing `spirit-nspawn-handover-socket` test (Subagent A, commit `efa557c0`) hid this gap because it only drove same-version daemons — v0.1.0.1↔v0.1.0.1 OR main↔main, never v0.1.0.1↔v0.1.1.

**Implication**: the LIVE two-daemon handover (the ceremony /333 §8 describes) is BLOCKED until v0.1.0.1 is rebuilt against current signal-frame. The brief-outage cutover (`/331`, bead `primary-0jjz`) still works because it's sequential — stop v0.1.0 fully, migrate, start v0.1.1 — there's no cross-version socket exchange.

**Filed bead**: `primary-XXXX` (P0) — Rebuild persona-spirit v0.1.0.1 retrofit against current signal-frame. The ShortHeader is just a prepended 8-byte prefix; the body codec is unchanged so existing handler code should compile + run without modification. Update Cargo.lock; rebuild; re-tag (likely `v0.1.0.2`); re-pin CriomOS-home's v0.1.0 deployment slot.

## §3 What actually ran on Prometheus

The subagent built three artifacts to make the test work despite the wire-compat gap:

1. **`wire-types-v0101/`** (208 LoC) — hand-vendored copies of `Operation`, `Reply`, `MarkerRequest`, `ReadinessReport`, `CompletionReport`, `MirrorPayload`, `DivergencePayload`, `RecoveryRequest`, `HandoverRejection`, `DivergenceReason`, plus `version-projection` newtypes. Plain rkyv derives, byte-identical to `signal-version-handover@eb3af073`. This is the v0.1.0.1-compatible vocabulary — the test driver speaks it directly, bypassing the upstream `signal_channel!([schema])` macro entirely.

2. **`full-ceremony-driver/`** (382 LoC) — wire-level driver with six modes: `MarkerOnly`, `MarkerThenMirrorThenComplete`, `ForceMarkerConflict`, `MirrorBeforeReady`, `DivergenceProbe`, `RecoveryProbe`. Raw `UnixStream` I/O.

3. **`persona-daemon-stub/`** (408 LoC) — STUB supervisor. Forks v0.1.0.1 + v0.1.1 daemons (each on its own version's signal-frame, hence the wire-types bypass for the driver), waits for all six sockets, drives the full happy-path ceremony, verifies retired public sockets, reaps children. Per record 547 (in-test unblock-the-blocker): the missing persona-daemon was BUILT inside the test as a 408-LoC stub.

The test passed end-to-end with witnesses:

```
(PrePopulateSeedsAcked count=3)
(StubSupervisorStarted)
(OldDaemonSpawned binary=Some("persona-spirit-daemon-v0101"))
(OldDaemonAllSocketsBound)
(NewDaemonSpawned binary=Some("persona-spirit-daemon"))
(NewDaemonAllSocketsBound)
(BothDaemonsConcurrent)
(PhaseMarker persona-spirit commit-sequence=3 write-counter=3)
(PhaseReadinessAccepted persona-spirit commit-sequence=3)
(PhaseMirrorRejectedAsExpected persona-spirit reason=NotReady)
(PhaseCompletion persona-spirit commit-sequence=3)
(PhasePublicSocketsRemoved old-ordinary-gone old-owner-gone)
(PhaseRecoveryProbed recovered=false)
(SupervisorChoreographySucceeded)
(StubSupervisorCompleted)
(MarkerConflictDetected persona-spirit reason=CommitSequenceAdvanced)
(MirrorGatingRejected persona-spirit reason=NotReady)
(DivergenceAcknowledged persona-spirit identifier=0)
(RecoveryCompleted persona-spirit recovered=false)
(SpiritFullCeremonyNspawnTestSucceeded record_count=3)
```

Every phase's wire round-trip works, BUT — see §4 for what the wire-success-without-semantic-success means per phase.

## §4 Three additional semantic gaps surfaced

### §4.1 Mirror phase ordering — /333 §8 placed it wrong

`/333` §8 + the sequence diagram in §6 (mermaid) place Mirror **between** AskHandoverMarker/ReadyToHandover (Phase 3, BEFORE readiness). The actual daemon code requires Mirror **AFTER** `HandoverCompleted` — the daemon's state must be `HandoverState::PrivateUpgradeOnly` for the Mirror handler to accept.

The subagent's probe confirmed: sending Mirror before Completion is rejected with `HandoverRejected(NotReady)`. Mirror gating is daemon-side, not protocol-side.

**Two ways to reconcile**:
- (a) Update the design narrative to match the code — Mirror is post-completion, used for ongoing state replication during the post-cutover drain window.
- (b) Update the code to match the design — let Mirror be accepted at marker+ readiness phase (in `HandoverMode` rather than `PrivateUpgradeOnly`). This matches the orchestrate use case where Mirror transfers in-memory state BEFORE the cutover instant, not after.

Lean: (b) — orchestrate needs pre-cutover Mirror to transfer in-flight lane claims; the design narrative's ordering is the correct contract; the daemon gating is too late. But this is a real psyche question.

### §4.2 Divergence has no abort semantics

The Divergence wire round-trips — daemon ACKs with `DivergenceAcknowledged identifier=0`. But the daemon takes NO action: no state transition, no abort logic, no supervisor notification. The "abort path" /333 §8 named doesn't exist beyond the ACK.

**Implication**: Divergence is currently a no-op in code. To make it meaningful, the daemon needs to (a) transition state to `HandoverAborted` or similar on receiving Divergence; (b) optionally notify the supervisor via the upgrade socket reply; (c) keep serving public sockets if it's the old daemon (back to `Serving`), or exit cleanly if it's the new daemon.

Filed as a follow-on operator bead candidate (not yet filed — pending psyche direction).

### §4.3 Recovery similarly wire-only

`RecoverFromFailure` round-trips. v0.1.0.1 always returns `recovered=false`. v0.1.1 has a state transition (`HandoverMode → Active`) but only in the main daemon code; v0.1.0.1's retrofit doesn't carry it.

Recovery is the supervisor's safety net for either-daemon mid-cutover crash. Currently nothing actionable happens on receipt. Same shape as Divergence — wire-only, no semantics.

## §5 What `/333` got right vs wrong (revised matrix)

| `/333` claim | Real status per test | Comment |
|---|---|---|
| §6 ShortHeader outbound wired | ✓ but on signal-frame `1493c59f` only | v0.1.0.1 lacks the ShortHeader — cross-version wire incompatibility |
| §6 ShortHeader receive-dispatch test-only | ✓ matches operator/176 | unchanged |
| §7 three-socket topology wired both versions | partial | sockets are BOUND; cross-version frames don't parse |
| §8 marker phase wired | ✓ same-version | cross-version blocked on §2 |
| §8 Mirror typed, payload landed (orchestrate) | ✓ but phase ordering wrong | see §4.1 |
| §8 Divergence typed | ✓ wire only | no abort semantics — see §4.2 |
| §8 Recovery typed | ✓ wire only | no behavior — see §4.3 |
| §13 matrix "Three-socket topology wired both Spirit versions" | needs caveat | sockets bound != interoperable |
| §13 matrix "Cross-version wire compatibility" | NEW ROW: not wired | the blocker bead |
| §14 verification mission | ✓ subagent executed | this report's findings |

## §6 What the subagent's in-test unblocks teach us

Per record 547 the subagent had license to build whatever the test needed. Three concrete unblocks:

1. **Persona-daemon stub** (`persona-daemon-stub/src/main.rs`, 408 LoC). The supervisor doesn't exist in production yet (`primary-a5hu` is the production-side bead). The stub forks the two daemons, drives the ceremony, reaps. Lesson: the supervisor's REAL interface (what it actually has to do during cutover) is now concretely specified — fork two daemons, wait for socket binding, drive AskHandoverMarker → ReadyToHandover → HandoverCompleted, verify retired sockets. That's the production persona-daemon's choreography boundary.

2. **Wire-types bypass** (`wire-types-v0101/src/lib.rs`, 208 LoC). Cargo refused to unify signal-frame across the two daemon versions; the subagent vendored the wire types as plain rkyv enums to talk to v0.1.0.1's pre-ShortHeader format. Lesson: the test had to recreate the wire vocabulary because the SIGNAL-FRAME version drift breaks the contract crate's normal use. This is itself evidence of the §2 gap — IF cross-version handover were properly supported, the contract crate would unify across versions.

3. **Mirror probe with empty payload**. Spirit's MirrorPayload is empty in production (Spirit has no in-memory critical state). The probe sent an empty payload anyway to verify the wire path. Lesson: the Mirror handler accepts payloads in `PrivateUpgradeOnly` state only — confirms §4.1.

The subagent's unblocks ARE the test's value-add. They're not workarounds — they're concrete specifications of what the production system must eventually contain.

## §7 Concrete operator next steps (post-`333-v2`)

In order of leverage:

1. **`primary-XXXX` (just filed, P0): Rebuild v0.1.0.1 retrofit against current signal-frame.** Unblocks cross-version wire compatibility. Half-day operator slice. Without this, every live-handover plan is blocked.

2. **Decide Mirror phase ordering** (psyche call needed per §4.1). If keeping the design narrative ordering, daemon code needs to accept Mirror in `HandoverMode` state (before completion). If keeping the code ordering, design narrative + state-machine diagrams need updating to reflect post-completion Mirror.

3. **Land Divergence + Recovery semantics** (operator slices; bead candidates not yet filed pending psyche direction). Wire-only-without-behavior is technical debt that surfaces later when something actually diverges.

4. **Build production persona-daemon** (`primary-a5hu`). The subagent's 408-LoC stub is the concrete specification of the choreography interface; the production daemon implements that interface plus the selector-flip + multi-component orchestration.

5. **Re-run the full-ceremony test against the rebuilt v0.1.0.2** to verify cross-version wire compatibility. The subagent's `wire-types-v0101` bypass becomes unnecessary once both versions speak the same signal-frame.

## §8 References

- `reports/designer/333-upgrade-mechanism-full-design-explained.md` — the design vision (v1)
- `reports/operator/178-primary-wdl6-spirit-v0-1-0-protocol-build-2026-05-25.md` — v0.1.0.1 retrofit landing (the wire-compat gap is the unstated dependency on signal-frame version)
- `reports/operator/176-schema-macro-upgrade-integration-audit/5-overview.md` — the prior audit; this `-v2` extends it with the wire-compat finding
- `reports/second-designer/175-upgrade-mechanism-full-design-2026-05-25.md` — second-designer's parallel design; the Mirror phase ordering question (§4.1) is partly an artifact of /175's sequence diagram matching the design's intent rather than the daemon code
- `~/wt/github.com/LiGoldragon/CriomOS-test-cluster/spirit-full-ceremony-e2e/` — the subagent's worktree; commit `25d07c98`; `wire-types-v0101`, `full-ceremony-driver`, `persona-daemon-stub`, runner, SSH wrapper
- `/git/github.com/LiGoldragon/signal-frame/` commits `653773b7` (pre-ShortHeader, what v0.1.0.1 uses) + `1493c59f` (post-ShortHeader, what v0.1.1 uses) + `18c22d8` (the ShortHeader-adding commit)
- `/git/github.com/LiGoldragon/persona-spirit/` tag `v0.1.0.1` (commit `e7a1b184`)
- Spirit records: 539 (always-background subagent — the test only finished because dispatch was non-blocking), 547 (in-test unblock-the-blocker — the test's 1000 LoC of stubs exists because of this rule), 535 (real-world testing — the test ran on Prometheus, not just local build)
