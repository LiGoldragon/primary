# Mind flowNexus Sol — successor handover

## Current work and authority
Psyche **venk** transfers Flow lane from854a8d: finish **0.60.1 first**, including hnc2 rulings, one immutable bounded gate on a newly granted slot, then tell Psyche when gated. Read `flows/854a8d/handover.md` and `state.md` (already read here). **5f30** queues the Reading-field contract release AFTER0.60.1: `Living.{ Context.String Verbatim.String Reading.String }`, vision at psyche-belief5ddfccd, next signal-flow0.x minor, cohort4e8a. No Reading edits yet. No runtime/deploy authority; Field switches.

## Source and custody
`/git/worktrees/flow-reminder-7b5174`, branch `reminder-link-7b5174`, clean **ec4eb9356e9441aec58bee94810d7e67014cbf0b**, published. New reservation **417 flow0601Hnc2**, owned bya7785f/permaflow: whole worktree. No source edits or tests authored by this flow yet; only inspection. No ancestor AGENTS found for this worktree. `/git/github.com/LiGoldragon/flow` is stale. Brief: `flows/7b5174/reminder-link-brief.md`.

Inherited0.60.1:644f0b08 links queued reminder Notices to Task;75e44f49 withdraws on Silence and removes schedules on tool Done;ec4eb935 puts ReminderOfTask.notice in a trait. Flow main0.60.0 at8e609713, ordinary0.68.0/319e3c3f, meta89.0.1/313bc05b, base7fca4d58, Energy3a7b4fdc: inherited evidence, not refreshed here. 0.60.0 landed/not-deployed per854a8d.

## hnc2 changes next
1. Result naming Task must refuse Unresolved on EVERY path. Send tool gains Done, with same accepted answer kinds as ordinary Send.
2. Silence stops reminders but leaves Task open; Done after Silence must close it.

Source pointers (relative to worktree):
- `crates/flow-nexus/src/send_tool.rs`: schema85–133 only Order/Question/Result/Notice; parserkind248, request-id requirement299; BecomesRequest330 currently builds private Result with EMPTY logical id; BecomesMessage352 wraps priority; handler598 constructs this message and answer_route603 routes/keeps it WITHOUT calling ordinary resolver. This is why tool Result bypasses kind/open validation; kept answers are affected too. Prefer shared `resolve_sendable_message` before answer_route, not a new parallel validation. Existing BecomesRequest/Message used only here (bounded search). Internal `ethos/send_tool.ethos` SendKind has no Done; regenerate generated/send_tool.rs with exact ethos-zerof23eacf, not by hand.
- `src/store/logical_delivery.rs`: `answerable_by`477 validates retained request kind and delivered state; `resolve_sendable_message`1855 checks open binding and distinguishes Result/Done correctly, no schedule dependency. `accept_tool_send`1559 assumes validated private message; raw store-level test1324 bypasses model/parser. Ordinary admission2145 REFUSES Done when reminder absent (Silence removes it); remove that dependency. Done commit2350 unconditionally retracts reminder: determine absent-row semantics / make removal conditional as tool path1760 does. Task closure must remain atomic; do not simply admit while leaving an invalid retract.
- `src/store/kept_answer.rs`: answer_route/keep_answer handle non-address senders; shared validation must precede them. Include kept Result/Task refusal and Done-afterSilence tests.
- `tests/unit/queue_operations.rs`: reminded_task helpers; delivered helper; tests1324 (raw tool Done),1398 (Silence withdraws notice/leaves binding Open); add real handler/parity and Done-afterSilence tests. `tests/unit/send_tool.rs`: fixture.codex_seat, handle_send_call, tool_call helpers; declared_result_shape test910 assumes schema conditional constResult, update for Done.
- `src/queue_operations.rs::silence`269 holds dispatch, closes reminder then calls close_task_reminder_notices. `src/store/task_reminder_notice.rs` withdraws notices AFTER store gates are released; inspect lock ordering and preserve delivery-id types/WithdrawRejected Debug concerns listed by predecessor.
- Gate clippy error NOT fixed byec4eb935: `crates/flow/src/hook.rs:546` test Table(Vec<(u32,u32,i64,&[&str],Option<&str>)>) type_complexity. Give fixture row a named shape (no allow). Logs `flows/854a8d/gate-0601-stopped/clippy1.log`/clippy2.log. No compile ran here.

## Builder / sequencing (latest, supersedes old snapshots)
Core **sqds**: old Harnessgu7s STOP+cleanupvvfz, work transferred3kyf to HarnessSol3177aa/lock414; old HarnessOpus taken down, DO NOT WAKE. Current queue SubscriptionSol76b588 first (boundsgap prep, NO heavygrant), Harness3177aa next, corrected0601 after waiters and **NEW explicit grant**. No heavy job started here. Old0601 gate STOPPED/cancelled with no FLAKE_EXIT/w4p6, slot RELEASED. No old snapshot is queue proof.

Gate only one pushed immutable revision, explicit memory cap keeping24GiB floor; start/terminal/process/cleanup receipts DIRECT Core and Field. Use standard per-crate Nix gate on Prometheus and coordinate exact harness with Core; predecessor's cargo+flake recipe would compile twice versus supplied build rules, so resolve that before grant rather than silently duplicating builds. Never heavy local. Fresh source review/fixtures/fmt first; no source change mid-gate. Work within low Codex until reset20:21 (Psychevenk).

## Completed lane / receipts
sv0s0.59.2 is DONE and live Field-confirmed0f822a45 with Energy03fa1f45; final packet `flows/6464a1/sv0s-producer-packet.md`; Field `flows/437627/sv0s/deploy-receipt.md`. Own reports ai71-source-control.md, main-integration.md, recovery-history.md here. Quiet hold released; deferred interfaces/mutex work NOT authorized. Do not reopen old carried requests/lifecycle proofs without current direction. Core2vlp already answered; its oldgu7s ACTIVE snapshot was explicitly superseded bysqds. No pending build/tool worker process owned here.

Threshold **y97e** requires this file and own Refresh. Next act: adopt417, implement hnc2 plus failing-on-ec4 regression fixtures and clippy fixture mend, source review, then request slot. No subagents spawned or code changed in this flow.

Refresh attempt after this handover returned **RefreshRejected.Locked**, no successor admitted. Reported Core/Field; no Unlock, Renew, repeat Refresh or native action. Until supported resolution, a7785f remains actual owner;417 stays reserved for the permaflow.
