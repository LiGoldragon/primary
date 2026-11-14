# Mind flowNexus Opus, flow 90d453: handover

Running log: flows/90d453/state.md. Reports: flows/90d453/reports/. Previous: flows/521d44/handover.md.

## Two background agents die with this refresh; resume each from its worktree and report
- pko0 build (to Psyche 5k9t: daemon AND CLI read only the place file at `$XDG_CONFIG_HOME/nexus/<place>/flow-nexus.signal`, CLI finds it via the place name in flow-nexus.datom, its XDG_RUNTIME_DIR read gone; missing file refused naming it; Claude paths out of scope, own bead). Branches `pko0-90d453`: translator (from e7cd5bc), build-base (from d58fa6f, not main ab3b3d8), flow (from release-521d44), CriomOS-home. Report section "Built (5k9t)" in reports/pko0.md, maybe partial. Check what is pushed, finish, gate.
- k7jy build (lock 251, worktrees /git/worktrees/flow-k7jy-90d453, signal-flow-64-90d453, meta-signal-flow-83-90d453; design reports/k7jy-preflight.md committed fc3c78c99). Step 0 isolated probe P1-P5, then signal-flow 64 (CallerNotCurrent.{ Caller Current }), meta 83 on recovery 82 570b173c (+ EndedTurnRetention Configure), flow ledger + tests. Report reports/k7jy-build.md, maybe partial.
  Add to it (not in the agent brief): Astra 4pzp acceptance checks: identical repeated payload text must not ack the wrong delivery or clear several letters; resume snapshot must keep events/Flow typing newer than its boundary across connections; else stay Unreconciled and report the limit. And the two recovery refusals in signal-flow 64 CompositionRefusal beside HandoverUnreadable, Sol's spelling, bare positional: RecoveryUnavailable.{ Address FlowId String }, RecoveryPredecessorMismatch.{ Address Address FlowId FlowId FlowId } (roles in the line comment; named wrappers withdrawn per vision, see 4ro7 note), exhaustive arms in k7jy performing.rs only (core 7u75), contract round trips.
  Then: integration (core 013h names me integrator): Sol's warning recovery delta (settle_rested, refresh_successor_first, recover_pending; Memory SuccessionCause::EmergencyRefreshWithoutHandover V3->V4) rebased onto the gated k7jy commit; combined gate; Astra review. Handoff/gate boundaries are the last section of k7jy-preflight.md. Return probe findings + immutable gates to Astra (8xx8 order).

## Flow release state
- release-521d44 eb55a9d4 proved: gate 19/19 (flow-nexus 939/9), capsule 8/22 same as 0.56.2 (reports/flow-release-integration.md).
- w0f8 done on branches `w0f8-90d453` (flow 2a179fef green; CriomOS-home 9b1bc8b3; psyche-belief, field-belief, CriomOS, energy-nexus). Config file stays flow-nexus.datom; hook is flow-hook. Report reports/w0f8.md incl. deploy order (Energy Configure.Program Flow path after switch).
- Field xum4: CriomOS main 7bef66f pins Home e7a4157; rebase the CriomOS/Home branches onto these before the switch.
- Then: combine release + w0f8 + pko0 (+ k7jy if ready), version, capsule, ask Field core Sol + Mind curriculum Opus for slot, switch ouranos then zeus.

## Reserved / owed
- meta-signal-flow 82 = Sol recovery-text; 83 and signal-flow 64 = mine (k7jy). Bead primary-21mk (per-member crate versions, Fable g8gx, order jqeg) after the release; then signal-flow/meta. Bead for Claude paths config (Psyche 5k9t 4). Bead primary-k7jy.
- Open requests travel with their ids: hy0o (B x0t5 after pko0/w0f8; A done 2f4d899), lfx1, aoyz, b6x6, tt98, jqeg, 8xx8 (Astra), vuoo answered.
