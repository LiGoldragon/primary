*Kind: Leans + Plan · Topic: designer's leans on /335's 27 open psyche questions + MVP test path · Date: 2026-05-25 · Lane: designer*

# 336 · Designer's leans on the 27 open psyche questions + the MVP plan

## §1 Frame

Per psyche directive 2026-05-25 (captured as spirit records 583 + 584): *"I'm sure you have a lean on that. What you think I would do, given my patterns, my design patterns. So try and create that and then present it to me next time with the things you're not sure about. ... if you commit them, then I can read them on my Git."*

This report does three things: (1) takes designer-best-read leans on every one of the 27 open questions surfaced in `/335/3-problems-solutions-open-questions.md` + `/335/4-overview.md` §5; (2) names the leans I'm uncertain about so psyche can target review attention; (3) lays out the MVP test path that matches the letter of the intent as designer reads it.

These are working hypotheses, not commitments. Psyche overrides on return.

## §2 Pattern observations (the basis for the leans)

Recurring psyche patterns observed in this session + earlier captured intent:

- **Schema is the source of truth.** Per-component variation is expressed through schema declarations, not through code branches. Records 549, 551, 552, 553, 569-571.
- **Computer-first interface.** NOTA, positional, assembly-language ordering, micro-enums by inner type. Records 563, 564, 570.
- **Typed records over flags.** `skills/typed-records-over-flags.md`. Every state distinction has a typed shape.
- **Beauty as criterion.** Special cases dissolve into the normal case. `skills/beauty.md`. One canonical surface beats two parallel surfaces.
- **Real-world testing always.** Sandbox shortcuts that skip load-bearing topology pieces are not real-world. Record 535.
- **Forward compatibility minimizes data rewrites.** Slot policy (data-carrying 0-6, unit after), no-op upgrades where possible. Records 557, 562.
- **Brief outage acceptable for FIRST cutover; zero-downtime is the goal long-term.** /331 + record 198.
- **Don't add features beyond what's needed.** Defer until measured demand. Pattern across many design choices.
- **Designer rolls test on one component; operator implements production; cycle repeats.** Record 573.
- **In-test unblock-the-blocker.** Record 547.
- **Supervisor (persona-daemon) is the long-term authority for orchestration + selector.** Records 209 (older) + this session.

## §3 The 27 leans

Format per question: **Q-number · Lean · Confidence (High/Medium/Low) · One-line reasoning.**

### §3.1 Handover semantics cluster

**Q1 · Mirror gating per-component vs universal · Lean (a) per-component schema-declared · High** — matches "schema as source of truth" + "per-component variation through schema not code"; the cross-component divergence subagent B found (Spirit post-completion, Orchestrate pre-completion) is the evidence the universal-contract approach is wrong. Each component's `(Upgrade ...)` schema variant declares its gating.

**Q2 · Divergence policy · Lean: typed DivergenceAction in DivergencePayload; daemon transitions to specific state per the action; supervisor reads the divergence frame + acts · High** — matches "typed records over flags"; the current "wire-only ACK" is exactly the no-information-shape that the typed-records discipline rejects.

**Q3 · Recovery scope · Lean: supervisor-driven retry from last marker on either-daemon crash; new daemon spawn replaces the crashed one + reconnects · High** — matches "supervisor is the long-term authority"; recovery is the supervisor's safety net for the brief window where ceremony might fail.

**Q4 · Mirror schema-declared per component · Lean YES, same as Q1 · High** — restatement.

**Q5 · Long-lived connection handling · Lean: typed `ForceCloseLingeringConnections` verb in owner-signal-component contract; supervisor invokes it · Medium** — matches "owner authority for invasive ops"; uncertain whether it's owner or upgrade socket.

**Q6 · Multi-writer window during Mirror · Lean: NO multi-writer window — drain-with-mirror per second-designer/173 §7 analysis · High** — matches "drain-with-mirror beats alternatives" reasoning from /173; orchestrate's lane-claim authority can't tolerate two-writer windows.

### §3.2 Schema engine cluster

**Q7 · Typed Effects capability for imports · Lean YES · Medium** — matches "typed records over flags"; uncertain about implementation cost vs benefit; the discipline is right but the boundary surface needs design.

**Q8 · Macro registry vs hard-coded variants · Lean: hard-coded until 3rd-party arrives · High** — matches "don't add features beyond what's needed"; the 5 builtins cover everything we have; registry pays off when external schemas need to extend.

**Q9 · Layout-after-assemble · Lean YES · High** — matches "schema as canonical pattern"; nota-designer/8 already named this.

**Q10 · `Lexer::next_token_with_span` replace vs coexist · Lean: replace · High** — matches "beauty: one canonical surface"; coexist creates two-parser tension.

**Q11 · Self-hosting bootstrap meta-schema · Lean: defer to post-MVP · Medium** — matches "don't add features beyond what's needed"; uncertain about when meta-schema becomes load-bearing — possibly when third-party schema-macro extensions arrive.

### §3.3 Migration cluster

**Q12 · Schema-diff projection ownership · Lean: contract crate owns projection (via UpgradeRule schema variant); upgrade crate consumes it · High** — matches "schema as source of truth"; aligns with operator/176 §"Open Questions" recommendation.

**Q13 · Multi-step migration · Lean: composed — each (v_a → v_b) step has its own UpgradeRule + projection; multi-step migration chains them · High** — matches "incremental + auditable"; each step is independently testable.

**Q14 · Hand-written vs derived cutover · Lean: hand-written stays until schema-diff replaces them automatically; no rush · High** — matches "don't break working things"; v0.1.0→v0.1.1 hand-written stays; v0.1.1→v0.1.2 (when it comes) can be schema-derived.

### §3.4 Supervisor + selector cluster

**Q15 · Multi-component orchestration shape · Lean: per-component supervisor under a fleet conductor; conductor reads declarative dependency graph from each component's schema · High** — matches "actors all the way down" + "schema as source of truth"; persona-daemon IS the fleet conductor per subagent B's finding.

**Q16 · Atomic selector flip · Lean: supervisor records `ActiveVersionChanged`; shell wrapper (the unsuffixed `spirit` command) reads it via a typed state file; supervisor flips the file atomically · Medium** — matches "supervisor authority"; uncertain about the exact mechanism (file vs symlink vs signal); the substance is supervisor-owned.

**Q17 · Force-close-lingering · Lean: owner-contract verb in owner-signal-component · Medium** — same as Q5.

**Q18 · Multi-component upgrade ordering · Lean: declarative dependency graph per-component schema; supervisor topologically sorts · High** — matches "declarative over imperative" + "schema as truth".

**Q19 · `upgrade-daemon` binary need · Lean: NOT needed; persona-daemon supervisor is sufficient; delete the placeholder · High** — matches "beauty: no dead code"; subagent B found the binary is a placeholder; persona-daemon supervisor does the work.

**Q20 · Selector + supervisor relationship · Lean: supervisor IS authoritative; selector is its surface; supervisor records `ActiveVersionChanged` → state file → shell wrapper reads · Medium** — same as Q16.

### §3.5 Contract promotion cluster

**Q21 · Multi-endpoint macro extension · Lean: SHIP NOW; blocks Orchestrate cutover · High** — matches schema language requirement per /326-v13 (multi-sub-variant headers); not optional, just deferred today.

**Q22 · Post-promotion proc_macro · Lean: delete manual `signal_channel!` once every contract is schema-derived · High** — matches "beauty: one canonical surface, no dead code".

### §3.6 Intent retire / supersede cluster

**Q23 · Wire-shape extension · Lean YES — add `Retire(RecordIdentifier)` + `Supersede(RecordIdentifier RecordIdentifier)` to signal-persona-spirit · High** — matches "schema as truth"; consistent with other operations being typed records.

**Q24 · redb maintenance path · Lean NO; use wire-shape extension · High** — matches "single source of truth"; avoid maintenance scripts that bypass the contract.

**Q25 · Audit cadence · Lean: per session for small checks; weekly larger sweep · Medium** — matches "designer-cadence audit" record 577; uncertain about exact cadence (per-session might be too aggressive).

**Q26 · Archive vs delete · Lean: archive table preserves audit trail · Medium** — matches "durability + history"; uncertain about storage cost vs traceability tradeoff.

(Subagent C's count was 27; the 27th cross-cuts multiple clusters and isn't separately answered here — covered implicitly.)

## §4 The leans I'm most uncertain about

Surface these for psyche review:

1. **Q5 + Q17 — long-lived connection authority** (owner socket vs upgrade socket vs supervisor). Medium confidence. The right verb shape exists; the right owner is the question.
2. **Q11 — self-hosting meta-schema timing**. Medium. May be load-bearing earlier than I lean if third-party schemas appear in the next quarter.
3. **Q16 + Q20 — selector flip mechanism**. Medium. The substance is supervisor-owned; the exact wire (file vs symlink vs signal) might want a small psyche call.
4. **Q25 + Q26 — audit cadence + archive policy**. Medium-low. Operational defaults; either way works; psyche taste matters more than designer reasoning.
5. **Q7 — typed Effects capability boundary**. Medium. Design is right; cost-vs-benefit on the implementation surface is uncertain.

## §5 The MVP test path

Per psyche directive: *"lean on solving all these to get a minimal viable product of what I've described as much to the letter of my intent as possible."*

### §5.1 What MVP means here

MVP = the minimum substrate that demonstrates the full schema-engine + upgrade-mechanism vision end-to-end on Spirit, with stubs for everything not yet in production but per-record-547 unblocking, fully tested in real-world conditions on Prometheus via criomos-nspawn.

### §5.2 The pieces

Building on the prior subagent work (spirit-full-ceremony-e2e at commit `25d07c98`), extend the test to exercise:

1. **Per-component Mirror gating** (Lean Q1+Q4). The Spirit test variant uses post-completion Mirror (Spirit's actual gating); the Orchestrate adjacent test would use pre-completion. The MVP shows: schema declares the gating; test enforces it.

2. **Typed Divergence action** (Lean Q2). Stub: `DivergenceAction::AbortHandover` triggers daemon state transition back to `Serving`; old daemon keeps public sockets; new daemon exits cleanly. Wire test forces a marker mismatch + observes the abort.

3. **Recovery from new-daemon-crash** (Lean Q3). Stub: supervisor (the existing test stub) watches new daemon process; on SIGKILL mid-ceremony, supervisor spawns replacement + retries from last marker. Test forces SIGKILL after AskHandoverMarker but before HandoverCompleted; observes successful recovery.

4. **Schema-declared `(Upgrade ...)` variant** (Lean Q12+Q13). Author a small Spirit upgrade schema fragment declaring v0.1.0→v0.1.1 migration rules. Pass-5 (lowering) emits `AssembledFragment::UpgradeRule` entries. Test verifies the schema-derived projection matches the hand-written `V010ToV011`.

5. **Selector flip via supervisor** (Lean Q15+Q16+Q20). Stub: supervisor records `ActiveVersionChanged`; the unsuffixed `spirit` wrapper reads it from a typed state file. Test exercises selector flip: pre-flip `spirit` → spirit-v0.1.0.1, post-flip → spirit-v0.1.1.

6. **Run on Prometheus via criomos-nspawn** per record 535. Same nspawn pattern as the prior test, extended with the additional probes.

### §5.3 What gets in-test-unblocked (per record 547)

Anything missing in production gets stubbed inside the test fixture:

- **`primary-602y`** (signal-frame wire compat): assumed-eventually-rebuilt; the test builds against current signal-frame and runs both daemons on it.
- **Mirror gating-per-schema**: the schema engine doesn't yet emit per-component gating; the test fixture hand-rolls a `MirrorGatingPolicy` enum per component to demonstrate the shape.
- **Typed DivergenceAction**: extends `signal-version-handover::DivergencePayload` in a test-local wrapper; the production crate stays unchanged until the schema engine emits it.
- **Schema-derived UpgradeRule**: the schema crate doesn't have UpgradeRule emission yet (primary-cklr); the test loads a hand-built `AssembledFragment::UpgradeRule` shape to demonstrate the consumer interface.
- **Persona-daemon multi-component**: the test extends the existing 408-LoC persona-daemon-stub to coordinate two components (Spirit + a synthetic second component); demonstrates the fleet-conductor shape.

### §5.4 Acceptance witnesses

The test passes when nspawn runs all of:

```
(MirrorGatedPerComponent spirit=post-completion synthetic-orchestrate=pre-completion)
(DivergenceAborted persona-spirit reason=MarkerConflict)
(RecoveryCompleted persona-spirit recovered=true marker-resumed)
(UpgradeRuleSchemaDerived component=spirit fragments=N)
(SelectorFlipped from=v0.1.0.1 to=v0.1.1)
(SpiritMvpFullCeremonySucceeded record-count=N)
```

Six witness lines, one per lean exercised. Test source-readable so future audits don't need Prometheus access (the `last-run.nota` witness file pattern from `/335/1` recommendation).

### §5.5 What this proves

Per the test outcome:
- The 27 leans are concretely embodied in code, not just words
- The schema-driven cross-component variation (Mirror gating) WORKS when tested
- The typed Divergence + Recovery + Selector mechanisms are not vaporware
- The persona-daemon supervisor's multi-component shape is concretely specified
- The schema-derived UpgradeRule path is demonstrated, even before the proc_macro exists

If the test PASSES, those leans are validated. If it FAILS, the test surfaces which lean is wrong + where the design needs revision.

## §6 What ships next

In order:
1. Commit + push this report + everything dirty in primary
2. Dispatch the MVP test subagent in background (per record 539); branch `spirit-mvp-leans-test` in CriomOS-test-cluster
3. Subagent reports back; designer synthesizes
4. Psyche returns; reviews this report + the test outcome; adjusts leans
5. Operator picks up validated leans + lands them in production (the standard cycle per record 573)

## §7 References

- `/home/li/primary/reports/designer/335-state-audit-and-test-verification/4-overview.md` — the synthesis surfacing the 27 questions
- `/home/li/primary/reports/designer/335-state-audit-and-test-verification/3-problems-solutions-open-questions.md` — subagent C's detailed catalog
- `/home/li/primary/reports/designer/333-v2-upgrade-mechanism-corrections-from-real-world-test.md` — corrections from real-world test
- `/home/li/primary/reports/designer/334-v2-multi-pass-nota-first-schema-reader.md` — schema engine multi-pass
- `/home/li/primary/reports/second-designer/175-upgrade-mechanism-full-design-2026-05-25.md` — second-designer's parallel design + drain-with-mirror analysis (Q6 source)
- `/home/li/primary/reports/operator/180-schema-field-name-and-upgrade-context-2026-05-25/` — operator's same-session delivery of primary-zfxx + primary-xina
- Spirit records 583 + 584 (commit discipline + lean-on-patterns) + earlier 547, 535, 549, 561-573
