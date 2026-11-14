# primary-k7jy build: trail and report

## Result

| Repo | Branch | Head (pushed to origin) | Gate |
| --- | --- | --- | --- |
| signal-flow 64.0.0 | `signal64-k7jy-90d453` | 83c04fefc087cf76dd3ca04792ff38b53b283b74 | **green**, 8 of 8 checks; tests 8 (default features) and 57 (datom), 0 failed. Log `/tmp/tmp.bpBsedzRGc/signal-flow-83c04fe.log` |
| meta-signal-flow 83.0.0 | `meta83-k7jy-90d453` | 06fff39fe3e9a3d65720433a1c27abf83a85db74 | tests, doc, fmt, cargo-nix green; tests 12 (default) and 56 (datom), 0 failed. **`crate-features`, `crate-versions` red** (build-base set lacks signal-flow 64), `default` red only through them. Log `/tmp/tmp.bpBsedzRGc/meta-signal-flow-06fff39.log` |
| flow (k7jy) | `k7jy-90d453` | 50ee7dff5ce1e8ade851ca2208b80aaa1f680f90 | 16 of 19 checks green: flow-nexus 957 passed, 0 failed, 9 ignored; flow 32; flow-meta 6; doc, fmt, cargo-nix, no-free-functions, no-inherent-methods, request-id-migration-process, capsule-witnesses, contract pins. **`crate-features`, `crate-versions` red** (build-base set lacks signal-flow 64.0.0 and meta-signal-flow 83.0.0), `default` red only through them. Logs `/tmp/tmp.bpBsedzRGc/flow-50ee7df-full.log`, `/tmp/tmp.bpBsedzRGc/flow-50ee7dff5ce1e8ade851ca2208b80aaa1f680f90-nexus.log` |

The flow head is the k7jy handoff candidate; it is immutable once the build-base set names its contracts (open question 3). Nothing live was touched.


Build agent (Opus) on lock 251's worktrees. Spec: `flows/90d453/reports/k7jy-preflight.md` (with Revision pjw9 and the z35f handoff section). Nothing live is touched: no switch, deploy, restart or message.

## Branches

- flow: `/git/worktrees/flow-k7jy-90d453`, branch `k7jy-90d453`, base eb55a9d4 (release-521d44).
- signal-flow: `/git/worktrees/signal-flow-64-90d453`, branch `signal64-k7jy-90d453`, base 4982eeb (63.0.0).
- meta-signal-flow: `/git/worktrees/meta-signal-flow-83-90d453`, branch `meta83-k7jy-90d453`, base 570b173 (82.0.0 recovery).

The branches already existed with the names of the preflight's handoff section; they are kept.

## Trail

- Started. Reading the preflight and the worktrees.
- Probe run in `mktemp -d` (/tmp/tmp.Rrbzw2bnQv, removed after), own app-server (codex-next-candidate-0.161.0-alpha.2), own CODEX_HOME, local mock Responses server, isolated `tmux -L k7jyprobe` for the TUI. Tools reused from the dead agent's scratch (`90d453b1…/scratchpad/k7jy-build/tools`), copied to this agent's scratchpad. Evidence kept: `/tmp/claude-1001/-home-li-primary/98df550b-580c-5645-ac3b-d5ccbe75016d/scratchpad/probe-evidence/`.
- The dead agent's own probe app-server and mock (PIDs 2097231, 2097229, under `90d453b1…/scratchpad/k7jy-build/probeK0HU`) were still running when this agent started; they are isolated, not live, and were left untouched.

## Probe findings (section 7)

- **P1, thread/closed and background terminals.** 5 runs (2 with `exec sleep 300`, 3 with a shell trapping TERM, HUP and INT). The stored process was killed and reaped 0.8 to 2.8 ms *before* `thread/closed` reached an unsubscribed second connection, in 5 of 5 runs. No `item/completed` for the command was relayed (N20 confirmed). `thread/status/changed` and `thread/closed` reach every initialized connection, subscribed or not. Reading: the kill wins the race by milliseconds; the source does not await the exit, so this is an observed ordering, not a proven one. Consistent with the design; `ItemsOrphaned` is kept as specified (it ends by an explicit act).
- **P2, idle on thread/start or attach.** `thread/start` answers `status: idle` and emits only `thread/started`, no `thread/status/changed`. A `thread/resume` of a loaded idle thread (a raw client, and the `codex --remote … resume` TUI) emits no status change on any connection. `thread/resume` of a thread with no rollout is refused (`no rollout found`). On one connection the `turn/start` answer precedes that turn's `turn/started`. F3 (an idle status read before T1's start, at Confirm) is not produced by `thread/start` or a TUI attach in this probe.
- **P3, terminate and clean.** `thread/backgroundTerminals/terminate` answers `{terminated: true}` and `clean` answers `{}` about 1 ms after the request, *before* the process exits (about 2 ms). Then `item/completed` arrives for the `commandExecution`, status `failed`, exitCode -1, under its original (already completed) turn's id, about 3 to 4 ms after the request. 4 runs. So the answer does not await exit; the `item/completed` does follow it. Matters only for option B.
- **P4, steer, interrupt, second letter.** TUI under an isolated tmux, three runs. A steer typed during a running turn is held ("Messages to be submitted after next tool call"); Esc interrupts T1 (`turn/completed interrupted`) and the TUI submits the held steer alone as T2's first `userMessage` (its own clientId). A letter typed 2 s, 0.2 s and 0.05 s after Esc got its own `userMessage`, exactly its text, never concatenated. Not exercised: a steer already accepted by the server (after a tool call) when the interrupt lands. No concatenation hazard was found; receipts by exact text hold in these runs.
- **P5, resume cut against turns/list under a racing turn/start.** 40 races, delays 0 to 20 ms. The `thread/resume` answer with `initialTurnsPage {limit 1, desc, full}` was consistent every time: 38 listed the new turn `inProgress` (no duplicate `turn/started` followed on that connection); 2 listed the previous turn `completed` with status `idle`, and in both the new turn's `turn/started` followed on that connection (no lost start). In both idle cases the cut was answered about 1.5 ms *before* the racing `turn/start` answer reached its own connection: F2's raw material. Every connection received the new turn's `turn/completed`. `thread/turns/list` reported the running new turn as `interrupted` in 7 of 40 (N17 confirmed). A2, N15 and N17 hold.

No finding contradicts the design. Editing proceeds.
- ethos-zero 27.0.0 (8c95310, the revision signal-flow pins) built on the remote builder; it regenerates 63's `src/generated/signal.rs` byte for byte, and generated 64's.
- No Skill tool is available to this agent, so the `knowledge:ethos` skill was not loaded; the contract was checked with the ethos-zero 27 CLI (`Check`, then `Generate`) and the crate's own build.rs equality check.
- signal-flow 64.0.0 committed 83c04fe on `signal64-k7jy-90d453`, pushed to origin (GitHub). Gate running.

### Finding: RecoveryPredecessorMismatch widens the archived rejection

`RecoveryPredecessorMismatch.{ Address Address FlowId FlowId FlowId }` archives in 44 bytes (Address 10, FlowId 8). Under the rkyv features signal-flow uses (unaligned, 32-bit pointers) that makes `CompositionRefusal` 45 bytes (was 18), `StartRejection` 46 (was 30, fixed by `HarnessSpawnRefusal` at 29) and `ReplaceRejection` 47 (was 31). Every earlier variant keeps its tag and payload position. Consequences:
- signal-flow's own `a_rejection_51_archived_reads_the_same` cannot hold as written. It is replaced by `a_rejection_51_archived_reads_the_same_widened`: the 51 archive with each rejection widened by 16 zero bytes reads as the same rejections, and 64 writes exactly that.
- Flow Memory: `LaunchOutcome` (launch-outcome v10) is 60 bytes wide, fixed by `HandoverSuperseded` (Address 10 + HandoverOwner 8 + LaunchedRecord 33 + Successor 8), so stored v10 outcomes read the same [inf]. The v9 upgrade source `LaunchOutcomeV9` in `store/reap_upgrade.rs` is 42 bytes wide (fixed by `ReplacedRecord` 41) and would widen to 48, misreading a real 0.54.6 store; Flow must keep the 63 layout there itself.
- RecoveryUnavailable (26 bytes) and CallerNotCurrent (17 bytes) widen nothing.
- **signal-flow gate green** at 83c04fe: 8 checks (crate-features, crate-versions, cargo-nix, fmt, doc, test-default, default, signal-flow); tests 8 passed under the default features, 57 under `datom`, 0 failed. Log `/tmp/tmp.bpBsedzRGc/signal-flow-83c04fe.log`. The widened archive test passing confirms the widths (31 to 47 bytes) and that rkyv zero-fills the added bytes.
- meta-signal-flow 83.0.0 committed a0c9326 on `meta83-k7jy-90d453` (signal-flow pinned to 83c04fe by manual Cargo.lock/Cargo.nix/crate-hashes edits; fetchgit hash computed from `git archive`, method checked against 63's recorded hash), pushed. Gate running.
- meta gate at a0c9326: tests failed on an unused import in the non-datom build (fixed in 06fff39, re-gating). `crate-features` and `crate-versions` fail and will keep failing: build-base's crate set (pinned d58fa6f) knows signal-flow only up to 63.0.0 4982eeb. Passing them needs a build-base set bump (signal-flow 64.0.0 83c04fe, meta-signal-flow 83.0.0, and the flow revision) in build-base, outside lock 251. This is a gate limit for every consumer of 64/83, flow included; the integration owns the bump.
- **meta gate at 06fff39**: tests green (12 under default features, 56 under datom, 0 failed), doc, fmt, cargo-nix green; `crate-features` and `crate-versions` red (build-base set, above), and the aggregate `default` red only through them. Log `/tmp/tmp.bpBsedzRGc/meta-signal-flow-06fff39.log`.

### Finding: meta 83 on 82 makes Flow consume meta 80 to 82

release-521d44 (the k7jy base) consumes meta-signal-flow 79.0.0. Meta 83 sits on 82, which carries meta 80/81 (context-warning policy, hook events, `StoreFailure` and the bare `ReadSendOutcomesRejected`/`InspectRejected`) and 82 (recovery text). Pinning 83 therefore makes the k7jy Flow consume 80 to 82, whose real consumer is the warning lane's flow branch (`context-warnings-7cd167`, based on 0.56.2, 25 commits, 3100 lines, with its own Memory families). Taken here, minimally, at flow c3a4e35:
- the renames, spelled exactly as the warning lane spells them, so the same hunks meet at integration;
- the warning lane's three Configure families and `Removal.ContextWarning` are refused `StoreRefused` (new `StoreError::ConfigurationFamilyUnheld`), and the snapshot reports them empty;
- `EndedTurnRetention` gets its own optional Memory family `flow_nexus_meta_turn_retention_configuration` (absent row = seed 64), modelled on the harness-hook family.
The integrator replaces the refusing arms with the warning lane's consumer. If that is not the intended order, the alternative is a meta branch from 79 carrying only the signal-flow 64 re-pin and EndedTurnRetention, which would not be 83.
- flow c3a4e35 (contract consumption): flow-nexus compiled; clippy `result_large_err` failed 16 sites, because signal-flow 64's `CompositionRefusal` carries `RecoveryPredecessorMismatch` whole (136 bytes in memory) and every `CompositionError`/`Failed_Data` result holds one. Answered by a crate-level `#![allow(clippy::result_large_err)]` with its reason in lib.rs (boxing would change the ruled contract spelling).
- flow 87a94f7: the ledger (`ethos/turn_ledger.ethos`, `codex_turns.rs`), its sources (responder cut with `initialTurnsPage` and `thread/backgroundTerminals/list`, item and thread-closed events, the launch part's `turn/start` answer, typed letters, history receipts, owner resolutions, start-up recovery of typed letters), the rest rule in `settle_rested`, caller-bound Refresh, and the tests. Building.
- flow c2722bc: at start, a Codex letter typed before the restart is seeded into its ledger only when history shows no receipt (the outstanding head and later typed attempts alike); a first prompt's batch is never a letter.

## Acceptance checks (Astra 4pzp)

- **(a) Identical repeated payload text.** Met in the ledger: an item takes at most one letter and is remembered by its item id, so its repeats (item/started then item/completed, other connections, a cut page) take nothing more; a letter of the same text typed after it waits for its own item; two pending letters of one text take none (both stay `LetterAwaited`). Test `identical_payload_text_never_takes_the_wrong_or_several_letters`. Limit: the ledger never writes a queue receipt itself; queue receipts stay with the existing history reconciliation, whose own ambiguity rule (`Undecided::Ambiguous`) is unchanged. Two pending letters of one text keep the seat until the owner resolves one.
- **(b) A resume snapshot keeps newer events and Flow typing.** Met: a cut ends only turns it lists ended, or open turns less than a listed turn; an open turn greater than every listed one is kept; a cut never removes a letter. Tests `a_cut_keeps_events_and_typing_newer_than_its_boundary` (every permutation of a newer start, a typed letter and the cut, ending the same) and `a_stale_cut_keeps_the_turn_turn_start_answered`. A reconnect sets the ledger Unreconciled until the next subscription's cut; a fact below the retention watermark does the same and makes the responder take a new cut.

## Deviations from the preflight, with reasons

- **Branch names.** The worktrees were already on `signal64-k7jy-90d453`, `meta83-k7jy-90d453` and `k7jy-90d453` (the handoff section's names); kept.
- **`CallerNotCurrent.{ FlowId Option<FlowId> }`.** The brief's `{ Caller Current }` spelled positionally with the roles in a line comment, as the recovery refusals are; `Current` is optional so the Asleep case is `{ X None }` (preflight §6).
- **RecoveryPredecessorMismatch widens the archived rejection** (finding above). Taken as ruled; signal-flow's archive test now proves the widened layout, and Flow's v9 upgrade source keeps the old layout as its own frozen `StartRejectionV9`/`CompositionRefusalV9` (`store/reap_upgrade.rs`), with a test that a signal-flow 60 `LaunchRefused` archive reads through it. Flow carries `#![allow(clippy::result_large_err)]` for the same reason.
- **The recovery refusals in Flow.** Mapping them in `performing.rs` needs `CompositionError` variants to map from; they are added in `composition.rs` with the warning lane's exact spelling (field names and messages copied from `context-warnings-7cd167`), and nothing constructs them here.
- **Meta 80 to 82 consumed minimally** (finding above): renames as the warning lane spells them; their Configure families refused `StoreRefused`; the snapshot reports them empty.
- **`EndedTurnRetention` storage.** A new optional Memory family `flow_nexus_meta_turn_retention_configuration` rather than a field in the request-policy record (whose layout change would need a Memory upgrade); absent row = seed 64.
- **No `CodexThreadStatus` in the cut.** The preflight records the cut's status and moves nothing with it; nothing reads it, so the ledger vocabulary leaves it out.
- **Turn-bound items are not stored.** They end with their turn and an open turn already keeps the thread working; only process-backed items are held. `ItemClosed` closes an item by id whatever kind the frame reads.
- **History receipts.** `LetterReceived` takes a letter only in a turn the ledger holds (or below its watermark); a turn it has not seen keeps the letter until that turn's own user message. When a turn ends with only letters left, the latest typed payload's history is read (`reconcile_typed`) so a receipt a reconnect hid is still found.
- **Owner resolution.** `ResolveQueueDelivery` of a Codex attempt removes its letter; a rest that steps in is noted for settlement with the stop-at-confirmation set.
- **Start-up.** Letters typed before a restart are seeded from the queue only when history shows no receipt; a first prompt's batch is never a letter.
- **Refresh records its caller in Flow's journal** (`flow-nexus: Refresh of … called by …`), not in Memory: the ordered-replacement record has no origin field for a Refresh, and adding one is a Memory record change.
- **Caller resolution.** A caller's own flow is read even when it is no longer live: its Codex thread ancestry (any lifecycle) or its pane's recorded flows; it is "of the Address" when the metaflow is Awake as it, lists it in Past, or its launch named the Address. The meta socket's Refresh is always "another caller".
- **Option A.** A Codex seat closes only at rest, a due or ordered refresh included; the Claude arm (`refresh_due || ordered_now` closes whatever it runs) is unchanged. `ItemsOrphaned` stays not-rest, as the preflight rules, though P1 found the process gone before `thread/closed` in 5 of 5 runs.

## Open questions

1. **Meta 83 on 82 and the k7jy base.** The k7jy Flow now consumes meta 80 to 82 with refusing stubs for the warning lane's three families. Is the integration to replace those with the warning lane's consumer (as written), or should k7jy's meta be a branch from 79 carrying only the signal-flow 64 re-pin and `EndedTurnRetention` (then not numbered 83)?
2. **The archived rejection widens** with `RecoveryPredecessorMismatch` (30 to 46 bytes for `StartRejection`). Accepted here, with the v9 freeze in Flow and the layout stated in signal-flow's UPGRADES. Any other store that archives a bare `StartRejection`/`ReplaceRejection` (outside Flow) must migrate; a payload within 28 bytes would avoid it.
3. **build-base crate set.** `crate-features`/`crate-versions` stay red for meta and Flow until build-base's set names signal-flow 64.0.0 (83c04fe) and meta-signal-flow 83.0.0 (06fff39); outside lock 251.
4. **`ItemsOrphaned`.** P1 saw the process killed and reaped before `thread/closed` in 5 of 5 runs (TERM-trapping included), by 1 to 3 ms, not awaited by the code. Does that suffice to make `thread/closed` end process-backed items, as the preflight allows "once the probe proves it"? Left not-rest.
5. **Two pending letters of one text** keep their seat until the owner resolves one (`ResolveQueueDelivery`), since no item names either.
6. **Refresh's caller is recorded in the journal**, not Memory. A Memory record would need a new field on the ordered-replacement record.
7. The dead build agent's probe app-server and mock (PIDs 2097231, 2097229, under the 90d453 scratchpad) were left running; they are isolated and can be killed by their owner.
- flow-nexus check at cc7cbd6: 937 passed, 7 failed, 8 ignored; every new ledger, Nexus-level and Refresh test passed. The 7: four snapshot-text expectations (meta 83's new tail); two send-tool tests whose fake answered a cut of an idle thread, which now rests and drains the seat (the fake's cut now shows the turn a connection's first notice starts, the seat working when its responder subscribed); and the interrupted launch's replay barrier, whose request id 3 the new terminal list took (the list moved into the responder, so subscribe_thread is the resume alone). Fixed at 50ee7df. The full Flow gate also needed `flow-request-id-immutable-contract-pins` moved to the new revisions (795e603), as the signal-flow 63 repin did before.
- **flow-nexus check green at 50ee7df**: 957 passed, 0 failed, 9 ignored. Log `/tmp/tmp.bpBsedzRGc/flow-50ee7dff5ce1e8ade851ca2208b80aaa1f680f90-nexus.log`. Pushed. Full gate running.

## Gate verdicts (final)

- signal-flow 83c04fe: green.
- meta-signal-flow 06fff39: green except `crate-features`/`crate-versions` (and the `default` aggregate), which fail only on build-base's crate set.
- flow 50ee7df: green except `crate-features`/`crate-versions` (and `default`), for the same reason; `flow-request-id-immutable-contract-pins` moved to the new revisions.
