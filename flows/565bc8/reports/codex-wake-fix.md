# Codex wake fix: AwakeNotRecorded on a Codex fresh wake

Repository LiGoldragon/flow, branch `codex-wake-565bc8` (pushed; main
untouched), cut from 967f2f5, worktree `/git/worktrees/flow-codex-wake-565bc8`.
Nothing was deployed.

## Commits

1. `33986c83` flow-nexus: a Codex wake carries its first prompt's batch as a
   Claude wake does.
   - `HarnessKind::session_start_anchor` is a new trait, `AnchorsSessionStart`
     in waking.rs. A Claude session starts at
     `ClaudeTranscript(NativeTranscriptCursor::session_start())`. A Codex
     thread starts at `CodexTurns(None)`.
   - `carry_startup` now accepts either harness. It prepares the head with the
     node's harness kind and that harness's session-start anchor.
   - `startup_launch` recognises the session-start anchor for either harness.
     It also requires a new check: the launch's brief (`instruction_prompt`)
     must end with the rendered run of requests that the attempt was parked
     in (`typed_group`).
   - DESIGN.md: the wake paragraph now covers both harnesses.
2. `680dddb4` flow-nexus: a Send whose wake started its seat and kept its
   batch is accepted Uncertain.
   - In `complete_direct_send`, the wake can answer `Failed` while its seat is
     left Awake (`started_unsettled`). This is the branch "failed before any
     native submission" (snapshot Queued, no carrying attempt). In that case
     the Send now answers `SendAccepted` with `DeliveryState::Uncertain`,
     `pending: None`, and no `mark_queue_retryable` is called.
   - A wake whose refusal left no seat Awake answers as before.
   - Test fault `RefusedWrite::DeliveryPrepare` is added in test_faults.rs. It
     is checked under `#[cfg(test)]` at the top of `prepare_oldest_delivery`.
   - DESIGN.md: one sentence added.

## Gates

`nix-fast-build --remote prometheus` over `checks.x86_64-linux`:

- `33986c8`: green. flow-nexus 917 passed, 0 failed.
  Log: `/home/li/primary/flows/565bc8/gate-codex-wake-33986c8.log`.
- `680dddb`: see `/home/li/primary/flows/565bc8/gate-codex-wake-680dddb.log`.
  Green. flow-nexus 918 passed, 0 failed.

Two earlier versions of commit 1 failed the gate. Both were amended and
force-pushed on the branch.

- `29d1375` failed clippy `needless_borrow` in the shared test setup. I
  deleted its log.
- `cafcb14` failed `tests::refreshing::scheduled_warning_admitted_during_replace_drains_once_to_the_successor`.
  The cause is below. Log: `/home/li/primary/flows/565bc8/gate-codex-wake-cafcb14.log`.

## Tests added

- `tests::waking::a_codex_wake_carries_its_batch_until_its_first_answer_receipts_it`.
  - Setup: a Codex fresh wake whose rollout shows the first prompt but not yet
    the first answer.
  - The wake answers `Woken`, the queue is empty, and A is one Uncertain
    attempt at `CodexTurns(None)`.
  - A drain before the answer settles nothing. After the answer lands, two
    drains settle A as Delivered on the launch's receipt.
  - No `agent prompt` is typed. The app-server is reached by exactly its four
    launch connections.
  - Before the fix the wake answered `Failed(StoreRefused)`; I confirmed this.
- `tests::waking::a_direct_send_whose_wake_started_its_seat_and_kept_its_batch_is_accepted_uncertain`.
  - Setup: a Claude direct Send whose wake starts the seat, with its receipt
    late and `DeliveryPrepare` refused once.
  - The Send answers `SendAccepted` Uncertain on both the private and the
    visible answer, with no pending Send. The request is neither Retryable nor
    Failed, and nothing is typed after the first prompt.
  - Before the change it answered `Failed … NotSent("Failed(StoreRefused)")`;
    I confirmed this.
- Refactor: the Codex fresh-wake setup of
  `a_sleeping_codex_address_wakes_fresh_to_a_new_thread_and_binds_to_it` is
  now shared with the new test (`SleepsCodex`, `WritesFreshRollout`). Its
  assertions are unchanged.
- The Claude witnesses are unchanged and green:
  `a_direct_send_its_wake_carried_is_sent_on_the_receipt_that_lands_after_the_wake`
  and `a_due_wake_whose_receipt_lands_late_never_types_its_carried_request_again`.

## Decisions the code forced

1. **Recognising a startup batch needs more than its anchor for Codex.** A
   Codex drain anchors its run at the thread's newest turn. That is
   `CodexTurns(None)` whenever the app-server lists no turn yet. With the
   anchor alone, such a drained run would be taken for the launch's batch and
   settled on the launch's receipt, which is a false receipt. The refresh
   witness above does exactly this, because its fixture app-server lists no
   turns.
   - What I did: `startup_launch` also requires the launch's
     `instruction_prompt` to end with the run's rendered text. That text is
     the batch the wake put in the first prompt
     (`FreshSeat.prompt = startup_text.with_purpose(purpose)`).
   - The check applies to both harnesses. I added no Claude-only branch.
   - Inferred, not verified: on a live app-server the first prompt's turn is
     listed as soon as the launch's `turn/start` answers, which is before
     `Started`. If so, the collision would not happen live. I did not rely on
     this.
   - Residue: if `carry_startup` parks only part of a batch (a store
     refusal), the partial run matches no brief. That run stays Uncertain
     until its own text is found, which for a Codex first prompt it never
     will be.
2. **What "started its seat" means in the Send.** The wake answers only an
   `Outcome`. Signalling this case through the Operation Ethos would have
   needed a new variant and regeneration. Instead the Send reads it as: the
   wake answered `Failed` and `live_awake_flow(address)` is now Some. Under
   the address lease, only this wake can have made the seat Awake. I changed
   no Ethos and regenerated nothing.
3. **"Never sent again" is not guaranteed by change 2 alone.** When the wake
   could not carry its batch, the request is still queued, and the store
   still holds it as `Queued`. The Send answers `Uncertain`, but a later
   drain will type the request again.
   - After change 1 this happens only when the store refuses a write
     (`prepare_oldest_delivery`, `mark_delivery_uncertain`, parking,
     `settle_wake_startup_receipts`) or a Simplified reply binding is
     refused.
   - Making the answer true would mean taking the request out of the queue
     in this residual case, or marking it Uncertain in the store. Either is
     part of the design question with Fable. I left the store untouched.
4. **`AwakeNotRecorded` is still one refusal.** It covers both "Record
   Awoken refused" and "recorded Awake, batch not settled". The Send tells
   them apart by the seat's state, so `WakeRefusal` is unchanged.
5. I added no UPGRADES.md entry and bumped no version. That belongs to
   whoever releases. The stored format does not change.

## Commit 3: the store agrees with the Uncertain answer

`4fa6aba0` flow-nexus: a Send accepted Uncertain after its wake kept its
batch records that batch Uncertain. It is on branch `codex-wake-565bc8`
(pushed; main untouched; nothing deployed). It replaced `94bfd378`, which
failed the gate on one test line (`{:?}` of `PendingSend`, which has no
Debug). I amended it and deleted that log.

What it does (decision point 3 above):
- `CarriesStartup::carry_left_queued(address, flow_id)` (waking.rs) finds
  the requests the launch's first prompt carried that the queue still
  holds. These are the longest head of the queue whose rendered run, after
  whatever is already parked at the session's start for that flow and
  thread, ends the launch's brief. It parks them through `carry_startup`,
  which is `prepare_oldest_delivery`, then `mark_delivery_uncertain`, then
  `park_cohort`. So no drain types them again, and `find_receipt`'s startup
  branch settles them on the launch's receipt.
- In `complete_direct_send`, the branch where the wake started its seat
  and the request is still Queued with no carrying attempt now calls it
  under the dispatch gate and answers from what the store then holds:
  - **The request left the queue:** `SendAccepted` Uncertain. No retry
    cause is written.
  - **The record was refused:** `Failed.Admitted … NotSent("Failed(StoreRefused)")`.
    No retry cause is written, and the request stays queued as it stood.
  - **The request was queued behind what the prompt carried** (for
    example, a Simplified wake carries only its oldest request): `SendAccepted`
    as admitted, with a pending Send, the same disposition as
    WaitingForTurn. The brief does not name this case. I chose it because
    Uncertain would be false here.
- Test faults: `refuse_times(write, n)` arms a refusal for n attempts.
  `refuse_next` is `refuse_times(write, 1)`, so re-arming still sets the
  count to one, as the earlier set-based storage did.
- DESIGN.md: the paragraph from commit 2 now says the Send records the
  batch, and names the refused and queued-behind answers.

Tests:
- `a_direct_send_whose_wake_kept_its_batch_records_it_uncertain_and_no_drain_types_it_again`:
  the wake's prepare is refused once. The answer is Uncertain with nothing
  pending, the queue is empty, and one attempt sits at the Claude session
  start. A drain before the receipt returns `Drained([])` and types
  nothing. After the receipt lands, drains settle it Delivered. Only the
  first prompt was ever typed.
- `a_direct_send_whose_record_of_its_wakes_batch_is_refused_answers_failed_store_refused`:
  prepare is refused twice (the wake's, then the Send's). The answer is
  `Failed.Admitted NotSent("Failed(StoreRefused)")` with nothing pending.
  The request is still queued and not Retryable, and nothing is typed
  after the first prompt.
- Commit 2's witness is unchanged and green.

Gate `4fa6aba`: exit 0. flow-nexus has 920 passed, 0 failed, 8 ignored, and
all 8 checks are green. Log: `/home/li/primary/flows/565bc8/gate-codex-wake-4fa6aba.log`.

Residue: if the store refuses the Simplified reply binding in
`settle_startup`, `carry_left_queued` does not restore it.

## Capsule against 4fa6aba

How it was run:
- Package: the gate's configured-package,
  /nix/store/37cnpkhbkj8v7mk521qcvbx08hy19hps-flow-configured-0.56.0.
- Capsule: the same as the 0.56.0 run. capsule/ is byte-identical from
  40104be to the head, with /home/li/primary/flows/e3a7d1/capsule-scratch-fixes.diff
  applied in scratch, and I verified the result. Its Curriculum is
  /nix/store/79zjg9f0iz9ljndlqnw6csv7bvyc7psc-rust_curriculum-0.1.0, which
  is the head's own `packages.curriculum` too. The wrapper is
  /tmp/claude-1001/-home-li-primary/565bc82a-9854-530d-bd62-4d0faa6e2c11/scratchpad/capsule-94bfd37/bin/flow-capsule.
- Options: `--keep-going`, Codex included, FLOW_CAPSULE_WITNESS_DIR=/home/li/witnesses/565bc8.
- Before the run there was no capsule process and no /run/user/1001/flow-testing.

Result: 7 of 22 passed, exit 1, wall 1474 s, teardown clean.
- **Passed:** 0, 1, 2, 8, 10, 11, 12.
- **Newly failing against 0.56.0:** 5 (Send during Refresh). The Refresh
  reply was empty after 66 s. s5b was admitted before the Refresh took
  hold, so the seat was kept at its Stop waiting for s5b's turn
  (`DrainRefused(WaitingForTurn(…09))`), and the fresh flow's prompt
  lacked Tag s5b.
  - This path makes no wake (the seat was Awake), so commit 3's code is
    not reached.
  - A rerun of scenarios 0–5 alone on the same package passed 5. The
    Refresh was queued first, and the fresh flow's first prompt held s5b.
  - My reading is an ordering race between the capsule's concurrent
    Refresh and Send. I did not prove it.
- **Other failures:** the same scenarios fail as on 0.56.0. One reply
  changed: scenario 19's Codex Task is now `SendAccepted Queued` instead
  of `Failed.Admitted NotSent «Failed(StoreRefused)»`. Its Done is
  `SendRefused.Unresolved`, and the Codex session was not seen holding
  Tag g1. I did not investigate.

Logs:
- Capsule: `/home/li/primary/flows/565bc8/capsule-codex-wake-4fa6aba.log`, Nexus log `capsule-codex-wake-4fa6aba.nexus.log`.
- Witnesses: /home/li/witnesses/565bc8/capsule-0.56.0-20261114T095852Z.
- Rerun: `capsule-codex-wake-4fa6aba-s5-rerun.log` (and `.nexus.log`), witnesses /home/li/witnesses/565bc8/capsule-0.56.0-20261114T102351Z.
