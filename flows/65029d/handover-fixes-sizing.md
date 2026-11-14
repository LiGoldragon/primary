# Sizing: the two 0.53.3 handover fixes

Read from source only: line request-id-0533-final at 61c09f4b. Nothing was built, run or edited.

## Fix 1: the handover becomes a file — medium, about 2 to 4 days of one lane

- What exists now:
  - Warning text: handover_reminding.rs:33-79. Reminders are sent at each Stop (waking.rs:2984) and on the tick (reminding.rs:116).
  - The handover is held in Memory: store/handover.rs:17-40 (family flow_nexus_handovers v2), and reminder rows in store/handover_reminders.rs.
  - "Green" gate: store/handover.rs:446-476. Close calls: launching.rs:818 and waking.rs:2584.
  - Launches read Memory through MemoryHandoverSource (lib.rs:156-214). The file reader HandoverFile already exists (handover.rs:43-71) and is the composer's default.
  - Keep/Drop/Glance/Read handlers: lib.rs:589-674.
  - Archive to Git and Observe.Retirement: handover_archive.rs (801 lines) and handover_observation.rs (313 lines).
- What changes:
  - About 1,300 production lines removed and 250 added. About 1,100 more go if the archive goes too.
  - Contracts: signal-flow 56 to 57 and meta-signal-flow 71 to 72. Consumers: the flow workspace pins, crates/flow and crates/flow-meta.
  - Tests: 34 removed, handover_reminding rewritten (16 tests), and the green-gate tests changed.
- Memory: no deployed store holds handover rows. 0.53.1 has no handover tables at all, and the 0.53.2 fixture's two families are empty. The new version must still open stores that register those families (store.rs:5127-5168), and sema-engine 0.19 has no API to retire a family.
- Fixture: the compatibility half of the 0.53.3 store-fixture candidate (its pins, manifest and review) must be redone once the code changes.
- The green gate goes away. The refresh happens when context is past the threshold and the flow is idle. The flow's first Stop after the Notice is the event at which the file is read once, to stop repeating Notices; no inotify is needed. If no file exists, the successor starts from its definition and its queue (vision:flow-nexus-v1:151).

## Fix 2: no refresh while working — small, under a day

- waking.rs:3069 (HarnessKind::Claude if refresh_due => true) and :3011 skip the resting check on refresh. Delete the arm, apply the check, and require closable: about 10 lines removed and 25 added.
- No contract or Memory change (KeptAtStop NotResting already exists).
- Tests: refresh_and_compaction.rs:346 flips, and two are added (held while working; a Soft submitted after a Stop is not cut).
- Make the refresh decision and Soft-at-idle delivery take the same dispatch gate, so whichever comes first shuts out the other.

## Open questions

1. Psyche tension: flows/263275/vision/handover.md (Nov 6) calls the handover directory "the hack until the handover lives in the Nexus's Memory, which he approved as direction". This conflicts with vision:flow-nexus-v1:151, vision:remembering and today's ruling.
2. Archive and Observe.Retirement: drop them, or have them publish the files?
3. One Notice, or repeats every EveryMinutes?
4. Do old non-empty rows get exported to files, or refused? Today none exist.
5. Does a file written before the Notice count?
6. What default warning share?
7. What counts as idle for Claude: the Stop, or Herdr showing Idle while background agents run? Nothing pushes an event for Herdr going Idle, so a held seat waits for its next Stop.

## Order

Fix 2 first, together with the Soft-waits-for-idle lane, since both touch settle_rested and delivery. Then settle question 1. Then fix 1: contracts first, then the Nexus. Redo the fixture re-pin once, after both.
