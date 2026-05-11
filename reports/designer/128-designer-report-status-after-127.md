# 128 — Designer report status after /127

*Designer record, 2026-05-11. Cleanup pass: which reports
are current, which are deferred (kept as design records),
which were deleted (their substance consolidated in
/125-/127). For operator-side stale-report cleanup, see
`~/primary/reports/designer-assistant/20-operator-report-feedback-after-127.md`
— that's operator-role work; the operator's next session
will pick it up.*

---

## 0 · Current state

The designer report archive after this cleanup:

| Report | Role |
|---|---|
| `/114` | Panoramic Persona vision — still load-bearing |
| `/115` | Engine manager architecture (privileged-user position, multi-engine framing, ConnectionClass shape) — still load-bearing |
| `/119` | persona-system development plan — **deferred record** (kept for when persona-system unpauses; banner at top) |
| `/122` | persona-message stateless proxy + WezTerm retirement — load-bearing for T2 |
| `/125` | Channel choreography + trust model — the decision record; supersedes the per-component class-gating from earlier plans |
| `/126` | Implementation tracks (operator hand-off — T1-T7 + T9) |
| `/127` | Decisions resolved 2026-05-11 (the seven deferred items from /125 §6) |
| `/128` (this report) | Cleanup index |

Eight reports. Down from fourteen.

## 1 · Recommended reading order

For someone new to the work:

1. `/114` — what Persona is at the panoramic level.
2. `/115` — what `persona` (the engine manager) is at the next layer down.
3. `/125` — trust model + channel choreography (the load-bearing decisions).
4. `/127` — refinements + resolved deferred items.
5. `/126` — operator implementation tracks (T1-T7, T9; T8 deferred).
6. `/122` for persona-message specifics; `/119` for persona-system context (deferred).

The cross-role companions still alive:

- `~/primary/reports/designer-assistant/15-architecture-implementation-drift-audit.md` — drift audit (P1/P2/P3 findings)
- `~/primary/reports/designer-assistant/17-pre-today-report-cleanup-agglomeration.md` — DA's earlier cleanup pass (95 pre-today reports retired)
- `~/primary/reports/designer-assistant/19-response-to-designer-127-and-contract-skill.md` — DA's review of /127 + skill substance
- `~/primary/reports/designer-assistant/20-operator-report-feedback-after-127.md` — operator-side stale-report critique (awaiting operator action)
- `~/primary/reports/operator-assistant/105-persona-terminal-message-integration-review.md` — concrete-gap inventory; informs T4, T6, T7

## 2 · Deleted in this cleanup pass

These were partially superseded by /125-/127 and carried "STATUS 2026-05-11" banners pointing readers elsewhere. Their unique substance is now in /125, /126, /127, /114, /115. Git history preserves the deleted content for anyone who wants the pre-/125 framing.

| Deleted | Substance now in |
|---|---|
| `/116-persona-apex-development-plan.md` | `/115` (engine manager framing); `/125` §1 (trust model), §4 (multi-engine as upgrade substrate); `/126` T3 (apex implementation track) |
| `/117-persona-mind-development-plan.md` | `/125` §3 (channel choreography substance mind owns); `/126` T5 (mind implementation track with contract additions) |
| `/118-persona-router-development-plan.md` | `/125` §3 (router's authorized-channel state); `/126` T4 (router implementation track with sema-db tables) |
| `/120-persona-harness-development-plan.md` | `/126` T7 (harness daemon, harness.redb, transcript-pointer fanout); `/127` §4.5 (HarnessKind closed); `/127` §1 (PromptPattern publisher role) |
| `/121-persona-terminal-development-plan.md` | `/126` T6 (supervisor socket + gate-and-cache); `/127` §1 (gate mechanism); the existing `persona-terminal/ARCHITECTURE.md` |
| `/123-terminal-cell-development-plan.md` | `/126` T9 (terminal-cell signal integration); `/127` §2 (control/data plane split); the existing `terminal-cell/ARCHITECTURE.md` |
| `/124-synthesis-drift-audit-plus-development-plans.md` | `/125`, `/126`, `/127` collectively; the audit substance still lives in `~/primary/reports/designer-assistant/15` |

## 3 · For the operator role

Designer-assistant's report `20` enumerates the changes the
operator role should make to operator reports 108, 109,
110, 111 after /127's decisions land. Summary:

- Add /127 update banners to operator reports 108, 110, 111.
- Update operator report 109's bead queue rows:
  - `primary-2w6` — persona-message is a stateless one-shot proxy / CLI surface, not a delivery daemon.
  - `primary-b7i` — typed-Nexus body migration superseded by /127 D2 (specificity grows through `MessageKind` variants); reframe or close.
  - `primary-3fa` — focus/input observation question mostly resolved (prompt state is terminal-owned; persona-system focus is paused); refresh or close.
  - `primary-rhh` — `ActorKind` decision bead; verify code state, close if obsolete.
  - `primary-kxb` — terminal-adapter protocol question now T9-specific (control/data split).
- In operator report 111: T9 means terminal-cell signal integration (not engine-upgrade); engine-level upgrade is a later unscheduled track.

This is operator-role work; the operator's next session will address it. Designer doesn't edit operator reports.

## 4 · What stays open for designer

These are flagged in /125 §6 and /127 but explicitly out of
scope for the current implementation wave:

- **Engine-level upgrade choreography** — substrate (`EngineId`-scoped paths) lands in T3; the upgrade flow (spawn v2, migrate state over channels, retire v1) lands as a later track after T1-T9.
- **Persona-system unpause** — when a concrete OS-level Persona need surfaces (window-aware notifications, multi-engine UI coordination, etc.), `/119` returns to active development.
- **Typed Nexus content variants beyond plain text** — per /127 D2 resolution, specificity grows through `MessageKind` enum evolution; new variants land as schema bumps when new message kinds emerge.
- **Cross-host Persona communication** — a future network component owns external ingress; cross-host route grants get signed-assertion records (NOT in `signal-persona-auth`, which is local-engine only).

## See Also

- `~/primary/reports/designer/114-persona-vision-as-of-2026-05-11.md`
- `~/primary/reports/designer/115-persona-engine-manager-architecture.md`
- `~/primary/reports/designer/119-persona-system-development-plan.md` (deferred record)
- `~/primary/reports/designer/122-persona-message-development-plan.md`
- `~/primary/reports/designer/125-channel-choreography-and-trust-model.md`
- `~/primary/reports/designer/126-implementation-tracks-operator-handoff.md`
- `~/primary/reports/designer/127-decisions-resolved-2026-05-11.md`
- `~/primary/reports/designer-assistant/15-architecture-implementation-drift-audit.md`
- `~/primary/reports/designer-assistant/17-pre-today-report-cleanup-agglomeration.md`
- `~/primary/reports/designer-assistant/19-response-to-designer-127-and-contract-skill.md`
- `~/primary/reports/designer-assistant/20-operator-report-feedback-after-127.md`
- `~/primary/protocols/active-repositories.md`
- `~/primary/ESSENCE.md`
