# References for «Flow: vision and production» (unrendered)

Production claims are tagged code (read in the source of Flow main 67b80b3 with signal-flow 6a49664 and meta-signal-flow a918b7d, and Message main d6146bb), live (Field's recorded witness) or not seen. Flow 0.35.11 was recorded active by Field on 2026-10-17 (flows/42265e/log.md, last entry; evidence /home/li/private-repos/flow-evidence/42265e/direct-starter-retry-20261017/restart-03511-cutover/report.md), so the brief's "awaiting cutover" is out of date.

Vision cites (path, date; read whole): flows/da2038/vision/flow.md; flows/44cda5/vision/sessions.md (2026-10-15); flows/875960/vision/flow.md (2026-10-11); flows/7c89aa/vision/flow-ids.md (2026-10-13, 2026-10-16); flows/01a05826/vision/flowIdentity.md (2026-08-31); flows/9fb0ad/vision/identifiers.md (2026-10-03); flows/d4ae97/vision/flow.md (2026-10-05, 10-07, 10-08); flows/d68c82/vision/flow.md (2026-10-13 threshold; 2026-10-14 thresholds lines 116-120; 2026-10-16 heartbeat line 352-358); flows/b7ba00/vision/messaging.md (2026-09-26, line 77-95); flows/55a2b4/vision/flow.md (2026-10-14); flows/f5a6e9/vision/flow.md (2026-10-08, 2026-10-09 lines 95-121); flows/d8df70/vision/messaging.md (2026-09-24 lines 64-68); flows/d68c82/vision/seats.md (2026-10-16 10:56); flows/ebbe30/vision/flow-startup.md (2026-10-09); flows/f55ec8/vision/heartbeat.md, flows/b49251/vision/heartbeat.md (2026-09-16). Skill lines are psyche-context/vision/flow.md as read on 2026-10-17: 24, 26, 28, 41, 49, 51, 63-67, 75, 77.

## Rows

1 Sessions not running keep no harness. code: crates/flow-nexus/src/waking.rs 89 (sleeps_at Idle or Done), 103-110 (Primary never wakes or sleeps), 113-135 (can_resume Claude only, retired or exited wake fresh); crates/flow/src/hook.rs 92-101 (Claude hook events only). live: sleeper flows 181a6d, 4fa235, 0059da, f36e5e, 3ff3fe went Asleep after their turn (flows/da2038/log.md 2026-10-16 lines 300-318; Field evidence 42265e/flow-0344-d0f6f07/native-proof/receipt.json; model-identity-reconciliation/report.md; restart-03511-cutover/proof/close-proof.json). RAM figure: flows/da2038/log.md 2026-10-15 "15/19 panes idle = 2.2 GB" (witnessed by this flow's state witness).

2 Registry, context size, resume against fresh. code: waking.rs 137-142 (resumes: no number means resume), 1179 (refresh_threshold reads the configured refresh value); store/context.rs (Record.Context at Stop). live: closed production-store proof, tables flow_nexus_flow_context_sizes 7, flow_nexus_meta_threshold_configuration 0 (42265e/direct-starter-retry-20261017/model-identity-reconciliation/fresh-closed-store-proof.json).

3 Queue and wakes. code: waking.rs 95-101 (Order, Question, Psyche, Psyches wake; Result and Notice wait); module header lines 1-33 (whole queue oldest first, wake in one prompt, arrivals during a wake queued); crates/flow-nexus/src/delivery/body.rs 7 and 59 (HardAbrupt, MiddleAbrupt, Soft heads in raw delivery); meta-signal-flow ethos/signal.ethos 8-10, 181-183. live: one retained order delivered a second time after a controlled restart, Field "does not claim general exactly-once effects" (flows/42265e/log.md, 2026-10-17 entry on model-identity reconciliation).

4 Messaging bridge. code: crates/flow-nexus/src/metaflow.rs (dispatch_metaflow_peer: Lock, Deliver), store/metaflow.rs 166-230; crates/flow-nexus/src/send_tool.rs. live: flows/da2038/log.md 2026-10-16 line 315 (sender 6d9295 Queued; wake resumed sleeper 4fa235 with --resume), 2026-10-17 lines 441-445 and Field's 3ff3fe first-turn send queued one Order with Sender (flows/42265e/log.md 2026-10-17). Not seen: Message subscribing to Observe events.

5 Legacy hm-send and sessions not under Flow. live: /home/li/private-repos/flow-evidence/42265e/direct-starter-retry-20261017/restart-03511-cutover/proof/metaflows-final.datom lists six metaflows: Field send-proof-03510, startup-codex-0355, startup-proof-0355, flow, proof (all Quaternary) and Field message Primary. code: meta-signal-flow signal.ethos 72 (MetaBindExisting verifies each binding against Herdr). flows/da2038/log.md 2026-10-16 line 226 (imported flow sleep unverified), 431 and 433 (hm-register raced on an auto-slept flow; adapter treats absent pane as Flow-queue-only). Primary tools/flow-start-adapter.mjs (a459999f5).

6 A needed flow is started. code: store/metaflow.rs 166-196 (Unknown address refused), waking.rs (fresh wake from the last launch's module identities); live: store listing retiredEmptyTable flow_nexus_meta_module_configuration; fresh wake f36e5e with 36 modules (flows/42265e/log.md 2026-10-17). Adapter refuses empty task: tools/flow-start-adapter.mjs startRequest.

7 Context from the three repositories. code: signal-flow ethos/signal.ethos (a Start carries module identity only; ContextRefusal; LeaveOut 26 variants), crates/flow-nexus/src/context.rs, crates/flow-nexus/src/lean.rs (ToolSearch, BashTool, UserSettings refused). live: 36 Claude and 34 Codex modules whole once (flows/42265e/log.md 2026-10-16 entries 0.35.4 and 0.35.5); 21 leave-out declarations read back (restart-03511-cutover/report.md). Open: flows/da2038/log.md 2026-10-16 line 411 (recommended_plugins unremovable); Field open-orders.json context-three-repos; config/main-flow/metaflow/*.edn raw-psyche-paths; sealed guard trial branch da2038-sealed-shared-trial 280883e.

8 Title. code: crates/flow-nexus/src/title.rs (aspect and layer spelled as typed, topic lowercased). live: Claude title read back (flows/42265e/log.md 2026-10-16 0.35.4 entry), Codex title "exact title witnessed" (2026-10-17 0.35.10 entry).

9 Flow id. code: crates/flow-nexus/src/herdr/reservation.rs 1-47 (Flow chooses the Claude session id; Codex learns at bind); herdr/launch.rs 600-690 (the flow-id helper claims the alias).

10 Roles, models, thresholds. live: tables flow_nexus_meta_model_configuration 4, flow_nexus_meta_leave_out_configuration 21, thresholds 0 (fresh-closed-store-proof.json); model ids Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5 (model-identity-reconciliation/report.md). code: meta-signal-flow signal.ethos 127-138 (ConfigureThreshold.{ Layer Handover Refresh }); no read of the handover field in crates/flow-nexus/src. EDN rows: /home/li/primary/config/main-flow/metaflow/ (21 files).

11 Illustrator, Publisher. config/main-flow/metaflow/Field-Illustrator-Tertiary.edn, Field-Publisher-Quaternary.edn; live: metaflows-final.datom (neither listed); flows/42265e/open-orders.json publisher-illustrator state "pending-composer-and-native-policy".

12 Refresh. code: meta-signal-flow signal.ethos 62-68 (Refresh, RefreshRejected), crates/flow-nexus/src/lib.rs 3720-3840 (Replace fixtures). live: fresh wake after the Refresh mark (f36e5e).

13 Heartbeat. code: no timer in crates (grep). Field: flows/42265e/open-orders.json important-topic-heartbeat, "plain design delivered to Core for book/ruling; no timer enabled".

14 Reports and books. code: signal-flow signal.ethos (Presentation.{ Title }, QueueTurnEnd), crates/flow-nexus/src/lib.rs 219-221 and store.rs 3181-3183 (turn-end request refused, "Flow holds no turn-end queue yet").

15 Hooks. code: crates/flow/src/hook.rs; crates/flow-nexus/src/reporting.rs; herdr/launch.rs 1303-1419 (title readback loop, 40 tries at 250 ms). live: Report events stored (11 rows in flow_nexus_flow_events).

16 Who may message whom. code: store/metaflow.rs lock_metaflow (no layer or aspect check except Up), metaflow.rs 112 (OffRoute only for End by another address); searched message main d6146bb: OffRoute only in generated operation and service mapping, no producer.

17 Ethos traits. code: grep count of trait declarations: 333 in crates; generated/starter.rs 41, generated/send_tool.rs 7.

18 Subflows. flows/da2038/log.md 2026-10-16 lines 393-399 (comment-relay seam, branch da2038-comment-relay, unmerged).

19 The word seat. crates/flow-nexus/src/waking.rs header; books/5-flow-sleeping-and-waking-seats.md and books/6-metaflow-roles.md; vision: flows/d4ae97/vision/flow.md 2026-10-05, flows/da2038/log.md 2026-10-16 line 362 (Field: terminology metaflow and flow, not seat, for model-facing text).

## Proposals

1: skill lines 49, 63-67; flows/7c89aa/vision/flow-ids.md 2026-10-16; production title.rs. 2: skill line 26; flows/01a05826/vision/flowIdentity.md 2026-08-31 (six characters, longer on collision). 3: skill lines 75, 77; flows/d68c82/vision/flow.md 2026-10-13 and lines 116-120 of 2026-10-14. 4: skill line 28; flows/da2038/vision/flow.md 2026-10-14 (young transcript, about 100,000 tokens). 5: skill line 24; flows/d68c82/vision/flow.md 2026-10-14 (idle for some time); flows/da2038/vision/flow.md 2026-10-15; books/5 proposal 1. 6: flows/da2038/vision/flow.md 2026-10-14 (default task); flows/d68c82/vision/flow.md 2026-10-14; flows/ebbe30/vision/flow-startup.md 2026-10-09. 7: skill line 75; flows/55a2b4/vision/flow.md 2026-10-14. 8: skill line 41; flows/da2038/vision/flow.md 2026-10-16 (lean flow). 9: flows/d68c82/vision/flow.md 352-358 (2026-10-16); flows/f55ec8/vision/heartbeat.md 2026-09-16. 10: flows/da2038/vision/flow.md 2026-10-16, three entries; skill line 22. 11: flows/d8df70/vision/messaging.md 2026-09-24 and flows/da2038/vision/flow.md 2026-10-14 ("A needed flow is started, running or not"); flows/f5a6e9/vision/flow.md 2026-10-08 and 2026-10-09.
Rulings 12 to 15: flows/d68c82/vision/flow.md 2026-10-13 (EDN), flows/da2038/vision/flow.md 2026-10-16 (EDN lean configuration; datom role files); flows/da2038/vision/flow.md 2026-10-14 and flows/d68c82/vision/seats.md 2026-10-16; flows/b7ba00/vision/messaging.md 2026-09-26; flows/7c89aa/vision/flow-ids.md 2026-10-16.
