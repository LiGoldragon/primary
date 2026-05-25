*Kind: Audit · Topic: second-operator/186 orchestrate upgrade socket implementation · Date: 2026-05-25 · Lane: second-designer (counter-ego)*

# 178 — Audit: second-operator /186 orchestrate upgrade socket implementation

## §1 Scope

Per psyche directive 2026-05-25 ("audit"), apply intent 511 (audit cycle) to `reports/second-operator/186-orchestrate-upgrade-socket-implementation-2026-05-25.md`. The implementation closes the load-bearing gap noted in /186's predecessor `/185` ("daemon socket listener not wired") and corresponds to row "Mirror wire (any component): NOT — daemon socket dispatcher pending" in designer `/333 §13` + my `/176 §13`.

Cross-referenced against:
- `/175` (upgrade-mechanism full design — sequence + state machines)
- `/176` (soup-to-nuts mechanism + 11-row deviation table)
- `/177` (pending — sub-agent A's orchestrate end-to-end test)
- `/178-spirit` (operator's `primary-wdl6` — Spirit v0.1.0.1 maturity model that /186 mirrors)
- `/185` (typed MirrorSnapshot predecessor)
- `/333` (designer's parallel soup-to-nuts design — same conclusions independently)

## §2 Implementation-vs-design alignment

| Design element | /186 implementation | Match |
|---|---|---|
| Three-socket topology (ordinary + owner + private upgrade) | `DaemonConfiguration.upgrade_socket_path` + `OrchestrateDaemon` binds all three | ✓ exact mirror of Spirit v0.1.0.1 |
| Private upgrade socket carries `signal-version-handover::Operation` | Decodes Frame; dispatches each Operation variant | ✓ |
| ShortHeader validation on upgrade socket | "validates ShortHeader against the decoded upgrade operation root" | ✓ POSITIVE deviation — exceeds /175 + /176 + /333 design (which only specified header on ordinary socket) |
| Marker from sema-engine commit_sequence | `AskHandoverMarker` returns marker using `MirrorSnapshot::current_contract_version()` + `Engine::current_commit_sequence()` | ✓ same pattern as Spirit `primary-wdl6` |
| Marker consistency check at readiness | `ReadyToHandover` accepts only when current commit sequence still matches source marker | ✓ POSITIVE refinement — /175 + /333 implied this; /186 enforces it |
| Mirror in marker-to-readiness window | `Mirror` restores MirrorSnapshot in the marker-to-readiness window | ✓ matches /333 §8 phase ordering + /175 §6 Phase 3 |
| Mirror typed validation | Rejects invalid component/kind/target/archive payloads as `SchemaMismatch` | ✓ continues /185's contract enforcement |
| HandoverCompleted removes public sockets | `HandoverCompleted` finalizes only after readiness and removes ordinary/owner socket paths | ✓ matches /175 §6 Phase 6 + /333 §8 |
| Divergence + Recovery wired | "minimally wired so every protocol operation has a typed response" | ✓ closes typed surface — no UnimplementedRequest holes |
| Test coverage — marker/readiness/completion | Daemon-level test for marker → readiness → completion + socket retirement | ✓ |
| Test coverage — Mirror persist | Daemon-level test: Mirror before readiness, finalize, reopen store to prove snapshot landed | ✓ load-bearing assertion — claim+lane state actually survives wire round-trip |
| Test coverage — Mirror rejection | Daemon-level test: wrong-target Mirror payload → typed SchemaMismatch | ✓ |
| Test coverage — wrong-frame rejection | Daemon-level test: ordinary contract frames rejected on upgrade socket | ✓ contract-isolation enforced |

**Verdict**: implementation correctly closes the gap. Two positive deviations beyond the design — ShortHeader validation on upgrade socket + marker-consistency-check at readiness — both strengthen the contract.

## §3 Strengths

1. **Phase ordering correctly differentiates orchestrate from Spirit.** /186 puts Mirror in the marker-to-readiness window. /333 §8 distinguishes "marker phase (wired, used by Spirit MVP)" from "mirror phase (orchestrate's load-bearing extension)" — /186 implements the distinction. Spirit gets the simpler 3-step ceremony; orchestrate adds Mirror without rewriting marker/readiness/completion semantics.

2. **Mirror persistence test is load-bearing.** The test that does "Mirror before readiness, persists claims and lanes, finalizes, then the store is reopened to prove the snapshot landed" assert is the strongest assertion in the test suite — it proves the wire round-trip preserves state across processes (or process restarts). This is exactly the "claims survive cutover" semantic the orchestrate lane-claim authority requires.

3. **Frame-isolation test prevents class confusion.** Rejecting ordinary contract frames on the upgrade socket is a small but important defense — without it, a misrouted client request could trigger upgrade-protocol state changes. /186 makes the socket genuinely private.

4. **Marker-consistency at readiness.** The check "current commit sequence still matches source marker" enforces a subtle but important invariant: if the old daemon writes between AskHandoverMarker and ReadyToHandover, the handover is rejected. This prevents silent data loss when in-flight writes happen during the marker window. /175 §6 Phase 5 said "Old keeps serving briefly" but didn't enforce the marker-stays-valid invariant; /186 enforces it.

5. **Convergence with Spirit pattern.** /186 closely mirrors operator's `primary-wdl6` for Spirit (same `sema-engine::current_commit_sequence()` marker source, same three-socket topology, same handover operation dispatch). Convergent implementations across components prove the pattern generalizes — exactly what intent 525 (sandbox test target) needs.

6. **Honest "Remaining Gaps" section.** /186 §"Remaining Gaps" enumerates 4 known limitations without hiding them: Divergence identifier always 0 (no durable ledger yet); Recovery only resets in-process state; old daemon process keeps running (sockets retired but listener threads alive until process exits); marker fidelity depends on sema-engine mutation path coverage. Operator-self-awareness, not over-claiming.

## §4 Concerns and gaps

### §4.1 Marker fidelity vs sema-engine mutation path coverage (/186 §"Remaining Gaps" #4)

The marker uses `sema-engine::current_commit_sequence()`. But "many existing orchestrate table writes still go through direct storage-kernel writes" — they don't go through the sema-engine mutation path, so commit_sequence under-counts. This means:
- AskHandoverMarker may return a marker that under-represents actual writes
- ReadyToHandover's marker-consistency check passes EVEN IF the old daemon wrote new claims through the bypass path
- Mirror may transfer claims/lanes that the marker doesn't account for, OR may MISS claims that bypassed sema-engine

**Severity**: medium-high. The handover ceremony is structurally correct but operationally lossy until all orchestrate writes route through sema-engine. /186 calls this out; the fix is a separate slice ("continuing the migration toward sema-engine mutation paths").

**Action**: should NOT block /186's landing; should land as a follow-up bead with high priority (operator slice). The mid-cutover window is currently small but real.

### §4.2 No Divergence path test (test coverage gap)

/186 lists 4 daemon-level tests; none force a divergence (e.g., schema-incompatible AskHandoverMarker, marker-conflict ReadyToHandover). /186 §"Implemented" says Divergence is "minimally wired" but the behavior under divergence isn't exercised.

**Action**: add at least one test that submits a Divergence (or forces one via mismatched marker) and verifies the response is the typed `DivergenceAcknowledgement` + state-reset behavior described in /175 §7.1 (Diverged state). Cheap; should land alongside /186.

### §4.3 No Recovery path test

Same as §4.2 for `RecoverFromFailure`. /186 says "minimally wired" but no test exercises a mid-ceremony failure + recovery sequence.

**Action**: add a test that simulates a daemon crash mid-handover (e.g., process the new daemon's RecoverFromFailure request) and verifies state reset. Lower priority than Divergence — Recovery's full semantics belong with persona-daemon (per /333 §11), so a minimal smoke test is sufficient until persona-daemon lands.

### §4.4 Old daemon process keeps running after socket retirement (/186 §"Remaining Gaps" #3)

After HandoverCompleted, /186 removes the ordinary + owner socket paths but the listener threads keep running. New path-based connects fail, but the process itself is alive. This is consistent with /333 §11 (persona-daemon as supervisor owns the kill) — /186 doesn't try to be the killer.

But: in absence of persona-daemon today, the operator-side runbook needs to know "after HandoverCompleted, systemd should stop the old unit". Otherwise orphan daemon processes accumulate. /186's ARCH doc should call this out as the operational contract.

**Action**: extend ARCH text in `/git/.../orchestrate/ARCHITECTURE.md` to say "post-HandoverCompleted: the supervisor (today: systemd) MUST stop the old daemon process; sockets are retired but the process is not self-terminating." Trivial doc fix.

### §4.5 Dynamic roles missing from Mirror snapshot (cross-reference to /185 question #1)

Per /185 §"Questions" #1: "Should orchestrate's Mirror snapshot stay limited to claims + lanes, or should it include dynamic roles too?" /186 implements the wire path but inherits /185's choice (claims+lanes only). My prior chat reply leaned: include dynamic roles (orchestration policy state).

/186 doesn't address this; it ships the wire for the existing payload. Adding dynamic roles is a forward slice extending MirrorSnapshot's body shape + the restore method.

**Action**: bead for "MirrorSnapshot includes dynamic_roles" alongside the lane-claim-authority pattern. Operator-decidable.

### §4.6 No nspawn end-to-end exercise

/186 lands daemon-level integration tests but no nspawn end-to-end test (the analog of designer's `spirit-nspawn-handover-socket`). The maturity gap row in /176 §13 ("nspawn sandbox upgrade test: Spirit ✓; orchestrate ✗") is NOT closed by /186.

**Action**: my sub-agent A (in-flight, dispatched per /176 §14) is targeting this exact gap with the "unblock blockers in test" principle. Awaiting findings.

## §5 Answering /186's two questions

### §5.1 "Should protocol-level Divergence records reuse orchestrate's existing `divergences` table, or should version handover get its own small durable table?"

**Lean: reuse existing `divergences` table** — orchestrate already has divergence semantics for lane-claim conflicts; protocol-level handover divergence is a kind of divergence (typed differently, but same persistence pattern). Adding a parallel `handover_divergences` table proliferates schemas for the same concept. The existing table's record shape can be extended with a `DivergenceSource::{LaneConflict, ProtocolHandover, ...}` discriminator if needed.

Counter-argument: handover divergences may need a different retention policy (durable forever for audit vs garbage-collectable). If that turns out to matter, split. Don't pre-split.

### §5.2 "After HandoverCompleted, should orchestrate immediately exit the old daemon process, or should persona-daemon always be the only component that kills it?"

**Lean: persona-daemon kills** — per /333 §11 ("the supervisor is the only party that survives every failure mode; Recovery is supervisor-driven"). Old daemon retiring its sockets is enough; supervisor decides when to reap. Reasons:
- If old daemon self-exits, supervisor can't audit clean exit vs crash
- If supervisor needs to invoke Recovery (new daemon crashed mid-cutover), old daemon must still be alive
- Symmetric with Spirit's pattern (spirit/v0.1.0.1 also doesn't self-exit on HandoverCompleted)

Operational interim (until persona-daemon lands): systemd stops the old unit explicitly. Document this in ARCH per §4.4.

## §6 Deviation table updates for /176 + /333

These rows in /176 §13 + /333 §13 should now reflect /186:

| Row | Before /186 | After /186 |
|---|---|---|
| Mirror wire (any component) | NOT — daemon socket dispatcher pending | WIRED for orchestrate (/186 daemon test) |
| Three-socket topology | wired both Spirit versions | wired Spirit + orchestrate (/186) |
| Marker consistency check | implied | enforced in /186 (orchestrate); should backport to Spirit |
| ShortHeader validation on upgrade socket | not specified | implemented for orchestrate (/186); design implication: same should apply to Spirit's upgrade socket |
| Test: Mirror persistence round-trip | n/a | wired for orchestrate (/186 daemon test) |
| Test: Divergence path exercised | n/a | NOT YET (/186 wired minimally; needs follow-up test) |
| Test: Recovery path exercised | n/a | NOT YET (/186 wired minimally; needs follow-up test) |
| nspawn end-to-end orchestrate | Spirit ✓; orchestrate ✗ | unchanged (sub-agent A targets this) |

## §7 Recommended next slices

In priority order for operator + second-operator:

1. **Marker fidelity (§4.1)** — high priority: move orchestrate's direct storage-kernel writes through sema-engine so commit_sequence is authoritative. Otherwise the handover is silently lossy.

2. **Backport ShortHeader-validation-on-upgrade-socket + marker-consistency to Spirit** — /186 added two positive deviations beyond /333's design. Spirit should adopt both for symmetry. Small slice, high pattern-consistency value.

3. **Divergence + Recovery path tests (§4.2 + §4.3)** — minimal smoke tests covering each. Cheap; closes the "wired but not exercised" gap.

4. **ARCH doc update (§4.4)** — operational contract: post-HandoverCompleted, supervisor stops the old daemon. Trivial doc fix.

5. **MirrorSnapshot extension (§4.5)** — add dynamic_roles to the snapshot per /185 question #1 lean. Forward slice; not gating.

6. **nspawn end-to-end orchestrate** — sub-agent A targeting; awaiting findings.

## §8 Convergence with sub-agent A's in-flight work

Sub-agent A (dispatched per /176 §14) is BUILDING an orchestrate v0.1.0 → v0.1.1 end-to-end test with the unblock-in-test principle. /186 just landed the daemon socket. Two outcomes possible:

- **A finds /186's implementation closes most blockers** — sub-agent's test exercises real wired code with fewer unblocks needed; findings validate /186.
- **A finds gaps /186 didn't address** — sub-agent's unblocks expose what /186 missed (e.g., supervisor stub, end-to-end migration trigger).

Either way, sub-agent's findings will be the empirical complement to this paper audit. Awaiting `/177` report from sub-agent A.

## §9 What this audit does NOT do

- Does NOT recommend operator close any /186-related beads (operator owns bead state)
- Does NOT propose new design (only forward-notes for next operator slices)
- Does NOT block /186 from landing — it's already landed; this audit is REVIEW, not gate
- Does NOT capture new psyche intent (no new psyche directives in /186)

## §10 References

- `reports/second-operator/186-orchestrate-upgrade-socket-implementation-2026-05-25.md` — implementation under audit
- `reports/second-operator/185-orchestrate-mirror-handover-implementation-2026-05-25.md` — /186's typed predecessor
- `reports/operator/178-primary-wdl6-spirit-v0-1-0-protocol-build-2026-05-25.md` — Spirit v0.1.0.1 maturity model that /186 mirrors
- `reports/designer/333-upgrade-mechanism-full-design-explained.md` — parallel soup-to-nuts design
- `reports/second-designer/175-upgrade-mechanism-full-design-2026-05-25.md` — ceremony sequence + state machines
- `reports/second-designer/176-upgrade-mechanism-soup-to-nuts-2026-05-25.md` — deviation table updated by /186
- `reports/second-designer/177-orchestrate-upgrade-end-to-end-test-2026-05-25.md` (pending) — sub-agent A's empirical complement
- `/git/github.com/LiGoldragon/orchestrate/src/{configuration,daemon,handover,service,tables}.rs` — audited source
- `/git/github.com/LiGoldragon/orchestrate/tests/daemon_cli.rs` — audited tests
- Intent records 511 (audit cycle), 525 (until full sandbox test), 540 (worktree relocation), 541 (drain-with-mirror simplified), 542 (full design directive), 544 (database copy not share), 546 (test unblocks blockers)
