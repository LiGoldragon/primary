# Flow 0.56.0: "woke but is not recorded Awake" on Codex wakes — root cause

Read only. Nothing was changed, either live or in git. The flow repository's
working tree is checked out at 53782fb, not at the release, so every source
below was read with `git show <rev>:<path>`. Copies of the files I read:
- `waking-40104be.rs`, `waking-082e0f9.rs`, `sending-40104be.rs`,
  `ld-new.rs` and `ld-old.rs` (`store/logical_delivery.rs` at the two revisions)
- `journal.log` (01:14 to 02:38), `journal-week.log`, `journal-0547-0550.log`, `wakes-all.log`
- `flow.sema`, a byte copy of the stopped store. It is redb with rkyv values,
  and I did not decode it (see Unknowns).

All of these are in /tmp/claude-1001/-home-li-primary/565bc82a-9854-530d-bd62-4d0faa6e2c11/scratchpad/.

`waking.rs` is byte-identical between 40104be and 967f2f5. The line numbers
below are those of 40104be.

## 1. Which condition failed, and why only Codex

Condition 1, recording the flow Awake (`perform(Record Awoken)`), succeeded.
Condition 2, `settle_startup`, returned false.

Evidence (verified):
- The journal shows "flow 3c0254 slept at its rest" (02:30:02), and the same
  for 8704bf (02:30:16), 4381d2 (02:30:21) and b32a58 (02:31:22).
  `AtStop::Slept` is reached only after `metaflow_awake_as(flow_id)` returns
  that flow (`settle_rested`, waking.rs about line 3860). So each metaflow was
  recorded Awake as the woken flow.
- The Codex rollouts (below) show a Nexus drain typing into each seat while
  it ran. `drain_held` requires `State::Awake(flow_id)`.

Why `settle_startup` fails for Codex (verified by reading the code):
- waking.rs 3243–3279: `receipt = startup_receipt(..)`. When
  `receipt == None` and the batch has logical rows, the result is
  `carry_startup(..)`. Otherwise it is `settle_wake_startup_receipts(..)`.
- `carry_startup` (3176–3212) returns false for any seat whose
  `harness_kind != Claude`. This is by design: its doc says "False when … the
  seat is no Claude seat".
- `startup_receipt` (3121–3174) returns None for a Codex wake at `Started`
  time:
  (a) The launch's `prompt_delivery_result_option` is not yet Observed.
  (b) `observe_native_target_receipt` requires the first user message *and
      the flow's first answer* in the rollout (herdr/launch.rs 3015ff).
  (c) The events fallback reads `PromptSubmitted`, which only Claude hooks
      report.
- Rollout timing confirms (b). For each of the four threads, the time from
  wake to first assistant message: 3c0254 08:28:54 → 08:29:54 (60 s),
  4381d2 08:29:21 → 08:30:12 (52 s), 8704bf 08:29:51 → 08:30:12 (21 s),
  b32a58 08:30:44 → 08:30:56 (12 s). The refusal was logged in the same
  second as `task_started`.

So every Codex fresh wake with logical queue entries gets `AwakeNotRecorded`.

Claude escapes because 0.55.0 added `carry_startup`. The journal shows it on
0.56.0: "flow 2e404d woke; its first prompt carried 1 requests, their receipt
awaited" (02:08:02), and the same for 565bc8 (02:37:11).

## 2. What changed between 082e0f9 and 40104be

Nothing that causes this. The premise does not hold.
- I diffed `settle_startup`, `waken`, `startup_receipt` and `carry_startup`
  (082e0f9 → 40104be). The only changes are mechanical: generated newtype
  wrappers (`InputDeliveryId(..)`, `Source(..)`, `Completed(..)`),
  `head.attempt_id` → `head.queue_attempt_id.0`, and
  `history_anchor` → `native_history_anchor`. `settle_wake_startup_receipts`
  (store/logical_delivery.rs) is logically identical: field renames only.
- The Codex gap was written down when 0.55.0 shipped. 08080636 ("Flow 0.55.0:
  a request a wake's first prompt carried is never typed again") replaced the
  0.41.1 guard `if has_logical && receipt.is_none() { return false; }`
  (from 5868070b) with `carry_startup` for Claude only. UPGRADES.md:141 says
  "Codex wakes are unchanged: their first prompt's receipt is still awaited
  once."
- The line was not new on 0.56.0. The journal shows `AwakeNotRecorded` from
  Nov 6 onward, including Codex seats on 0.54.7: "Mind flowNexus Sol"
  (2026-11-13 18:19, 22:07) and "Mind curriculum Sol" (17:55, 18:42, 19:11).
  Claude seats appear too ("Mind flowNexus Opus", "Psyche book Haiku"), and
  0.55.0 fixed those.
- 0.55.0 ran only from 2026-11-13 23:50 to 2026-11-14 01:12. Its journal holds
  no wake line of any kind, and a successful Codex wake logs nothing. So
  "never on 0.55.0" carries no evidence either way.
- Inference: 0.55.0 would refuse a Codex wake in the same way, since the code
  path is the same.

## 3. Do the started flows stay running unrecorded? Is there double delivery?

They are recorded Awake (see 1). They ran their turns and were slept at rest
within 1–2 minutes.

The batch is delivered twice, and the Nexus itself does the second delivery
(verified in all four rollouts, under
`~/.codex-next-5ck97j38j3sb/sessions/2026/11/14/rollout-2026-11-14T02-{28-49,29-16,29-47,30-39}-*.jsonl`).
`settle_startup` failed, so the batch stayed in the queue. A later drain
then typed the whole batch again into the running seat:

| flow | first prompt carried | typed again at | extra |
|---|---|---|---|
| 3c0254 | s1lr lwp0 pdj7 | 02:29:22 | + ymfx |
| 4381d2 | ypy1 gwd0 28lz eic9 pmnn 6746 dhqq np7v xxia | 02:30:09 | + xufs |
| 8704bf | 4wp8 10q6 8x4q 8pu0 92gx xvdd klsb i8f8 | 02:29:57 | — |
| b32a58 | y6j4 net7 iyn4 c0bj m570 | 02:31:16 | — |

Every request in each batch appears exactly twice. The predecessor's open
requests (5hnb, 3i58, o9vt, 0mlh, hl3s, puuy, …) appear once. The Herdr
fallback adds a third copy only if the sender used it. No third copy is
visible in these four rollouts.

Why the Send's own request stays queued (verified in code, sending.rs
1329–1456): `complete_direct_send` gets `Outcome::Failed(StoreRefused)` and
types nothing. It finds the logical state Queued with no carrying attempt,
and so takes the "Starting the next flow failed before any native submission"
branch (line 1433). That branch does two things:
- It marks the whole queue `Retryable.WakeRefused(CompositionRefused(Unconfigured))`.
  That label is false, because the flow did start.
- It answers `Failed.Admitted{… NotSent("Failed(StoreRefused)")}`. The entry
  stays in the queue, so the next drain types it.

Hypothesis: the waking request is the last entry of each batch, matched
against the admission times in the journal. For example, the Order admitted
at 02:28:46 matches pdj7.

## 4. Smallest correct fix (description)

Carry a Codex wake's startup batch the same way a Claude wake's is carried,
rather than requiring a receipt at `Started`:
- `carry_startup`: accept `HarnessKind::Codex`. Prepare the head with
  `HarnessKind::Codex` and the Codex thread-start anchor
  `NativeHistoryAnchor::CodexTurns(None)` (this anchor variant exists in
  store/queue_delivery.rs). Then mark it Uncertain and park the cohort.
- `startup_launch`: recognise a Codex attempt at the thread-start anchor in a
  flow whose launch typed a first prompt. `find_receipt`'s startup branch then
  settles the batch on `startup_receipt`. For Codex that receipt is the
  launch's Observed result, which launching.rs (about line 356) records once
  the rollout shows the first message and answer, or `observe_native_target_receipt`.

The batch then leaves the queue at once, no drain retypes it, the wake answers
`Woken`, and the direct Send waits for the receipt and answers it.

This needs a Codex witness alongside
`a_direct_send_its_wake_carried_is_sent_on_the_receipt_that_lands_after_the_wake`.

A separate defect: a wake refused *after* the flow started should not take
the "failed before any native submission" branch. It should not stamp
`CompositionRefused(Unconfigured)`. Once the fix is in, `AwakeNotRecorded`
again means only that the store refused. This part of the fix is design work
for Psyche/Fable, not a one-liner.

## Observed / inferred / unknown

Verified by reading code: the waken and settle_startup path, carry_startup's
Claude-only guard, startup_receipt's three sources, the Slept→Awake
precondition, the complete_direct_send failure branch, that the code is
unchanged across 082e0f9→40104be→967f2f5, and the 0.55.0 UPGRADES note.

Verified from the journal and transcripts: four refusals followed by "slept
at its rest"; first answers 12–60 s after wake; every batch typed twice;
AwakeNotRecorded on Codex seats under 0.54.7; no wakes logged on 0.55.0.

Inferred: that 0.55.0 refuses Codex wakes identically; which request in each
batch was the waking direct Send; and that the second typing came from the
pending-Send or rest drain. The exact trigger is not logged:
`AtStop::Drained` and `drain_awake` are silent.

Unknown:
- Why the later Cancel answered NotYet. `commit_archive_request`
  (store/logical_delivery.rs about 885–990) returns NotYet in four cases: an
  admission answer still pending, an unfinished queue delivery attempt (the
  drain's Codex attempt is a candidate), an open simplified-reply binding, or
  another retained request naming it. Telling which needs the store decoded.
- The store states (logical delivery and launch attempt rows) were not read.
  `flow.sema` is redb with rkyv values, and decoding it needs a reader built
  against 40104be's generated Memory types. The raw bytes only confirm that
  the ids are present.
