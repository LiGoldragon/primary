# Handover from da2038 (Psyche Flow Secondary)

Awaiting the living's rulings:
- Book 5 sleep/wake: https://claude.ai/artifact/RHpbudqE2dajBhqc488jTA. His comments from 2026-10-16: proposal 1 is "a good long-term vision", proposals 2 and 5 are "This is good", proposal 3 is confusing (low power is not sleep), and the figure needs the past-flow and context check. Needs a revised edition.
- Book 6 metaflow roles: https://claude.ai/artifact/1bjt3LCT3JDszJZQZ3SGr8
- Book 3 pod controller: https://claude.ai/artifact/PXxe5anzqVKT6Z3WbPsT1p
- Book 7 How Flow is used: https://claude.ai/artifact/C6su9yRiGfgob2zDryvkeq
- Book 8 Flow vision and production: https://claude.ai/artifact/DmukKu4iSTF55PYCDHdcGF

Always-on core: the living wants to move to a Flow with an always-on core, kept fresh by age. Migration is held until Psyche Core Secondary relays his ruled anatomy. My study of what Flow has and lacks (standing cells, age clock, automatic rollover, Codex sleep, Primary wake, per-aspect model choice, unknown Address placement) is in my log for 2026-10-17. The study's full report was not saved to a file.

Unrelayed comments: the list is at /home/li/private-repos/flow-evidence/da2038/unrelayed-comments-2026-10-17.md. I have already logged three records in vision/flow.md: the waking figure, low power, and caller identity. Still to do: research provider cache lifetimes, research Steve Yegge's harness and its usage view, and answer "the hook doesn't cue the answer, right?" on the handover book.

Flow branches (unmerged; the 0.35.11 commit 67b80b3 is active in production according to Field's log):
- flow-da2038-0359: pane recovery.
- flow-da2038-model: model-form guard.
- flow-da2038-relay: comment relay, stale against current mains.
- flow-da2038-sealed: the Sealed/Shared trial.

Open:
- Mind's messaging bridge to Flow is not activated.
- No working flow is held by Flow.
- Codex flows and Primaries don't sleep.
- Thresholds are undeclared.
- The Flow README shows CLI forms that Flow refuses.

In flight when da2038 was retired (all Flow branches; nothing merged, pushed or deployed):
- flow-da2038-receipt 9669d5b (0.35.13): the exact-row Claude paste receipt repair. Committed locally; unbuilt and unpushed because Prometheus is offline. The worktree is in the da2038 scratchpad. Two bounded refusals, both reported as PartDiffers: a lookalike of '<', and more than 8 escaped tags. The tests and the bundle lines are in log.md.
- flow-da2038-leaveout-harness: harness-keyed leave-out defaults with migration of the current records. Not to be published until the consumers are updated with Field and Mind.
- flow-da2038-codex-drain: automatic drain of an idle Awake Codex seat. Field drained 17c364 by hand (evidence in 42265e idle-drain-17c364); the defect itself stays open.
- Per-address model choice: on hold until Core gives an explicit ruling on the Psyche flow Secondary model.
- Mind flow Primary 9896d8 is retired, and no successor is known.
- Leave-out branch result: meta-signal-flow da2038-leaveout-harness 5bb519c (25.0.0; contract digest changes) and Flow flow-da2038-leaveout-harness c2a2879 + 0a65ff1 (0.35.13), both pushed. Neither is built or tested, because Prometheus is down. Store v1→v2 migration; a mixed or empty entry stops the store from opening. Pre-migration proof: the production copy holds 21 entries (16 Claude, 5 Codex, none mixed), in /home/li/private-repos/flow-evidence/da2038/leaveout-harness-20261017/; post-migration proof waits for a build (run-configure-only.sh). The cutover must move with Field's CriomOS-home packages/flow-deployment/leave-outs.clj (it must name the harness) and with the Message repin to the new digest. Version collision: the receipt branch is also 0.35.13, and one must be renumbered.
- Codex drain result: flow-da2038-codex-drain 731d670 (0.35.14), pushed and unbuilt. Cause, from reading the code: Codex seats run no Stop hook (herdr/launch.rs:469-487); an Awake seat's queue drains only on a Stop or a wake; wake_due needs the seat Asleep (waking.rs:640); both Codex connections drop turn/completed (send_tool.rs:462,607; codex.rs:1283-1287). QueueTurnEnd (lib.rs:219) has no sender, so it isn't on this path. Repair: codex_turns.rs reads turn/started, turn/completed and thread/status/changed for the subscribed thread, plus the status in the resume answer. A real completion drives the same delivery as Flow's Stop handling, typed into the pane with the sender first. Each completion counts once by turn id; a seat in a turn is kept InTurn. No polling, no turn/start, no forged Stop. 5 tests, with baseline worktree 207e907 to show them failing on main. For review: whether typing through the Stop-handling path meets Mind's "no direct brief typing"; and that the new traits are hand-written, not declared in ethos (a finding, raised for the living). A background verify.sh in the scratchpad waits for Prometheus.
- Codex drain branch now verified: commits 731d670 + 10ced18; nix flake check passed on Prometheus (322 pass, 5 ignored); the 5 new tests fail on main 67b80b3 (main typed a queued psyche into a mid-turn seat). Still unproven natively: that resume subscriptions receive turn events in production; Field's native check is the proof.
- Receipt branch verified: flow-da2038-receipt 517ea88 (0.35.15), pushed. The flake check passes, and all 7 receipt tests fail on 67b80b3 with PartDiffers.
- Leave-out branches verified: msf 5bb519c + 7748a79 (digest 7bbc37359da8843c → 94175d68080bf89a); flow fb73aea (0.35.13). Flake checks pass. Post-migration store proof: Configured.Unchanged on a fresh production copy. Not to be published without the CriomOS-home leave-outs.clj update (Field) and the Message repin.
Ready for review and Field's native validation, each separately: receipt 0.35.15, drain 0.35.14, leave-out 0.35.13 (the coordinated cutover).
