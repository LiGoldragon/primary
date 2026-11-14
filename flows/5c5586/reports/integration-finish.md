# Integration finish — flow 5c5586

Continues `flows/98df55/reports/integration.md`. Worktree `/git/worktrees/flow-integration-98df55`, branch `integration-98df55`, lock 257 (98df55's, continued). Nothing live.

## Step 1 — request-id-migration-process

Cause found by running the new daemon (`flow-nexus-daemon`, `{ main «runtime» «store dir» }`) on Prometheus over the check's own predecessor fixture (`flow-configured-request-id-predecessor-fixture-0.53.2`, Memory written by the 0.53.2 source). The daemon refused to open it and exited at once, so `flow.sock` never appeared (the "ordinary connection dropped" line is the test's own connect-and-drop on the *predecessor*; the refusal text went to the new daemon's stderr as the one-line error, which the check log did not show because the daemon's exit text is printed by the process only when run alone).

Refusal text, first: `family registration "flow_nexus_meta_handover_configuration" makes a mixed or unauthored Flow Memory v3 identity`; after fixing that, the same for `flow_nexus_successor_intents`.

Cause: `FlowStore::recognize_open_memory` accepts a store whose every registration is either current-chain (`is_current_flow_registration`) or the 0.53.2 request-id predecessor era (`is_request_id_predecessor_registration`, via `request_id_predecessor_family_identity`, which names each family that changed since 0.53.2 and otherwise falls back to the current identity). The integration moved two families past what 0.53.2 wrote and did not teach the predecessor-era check about either: handover configuration (0.53.2 `-v2`, current now `-v3`; the chain's `predecessor_handover` allowance was only in `is_current_flow_registration`) and successor intents (0.53.2 `-v3`, current now `-v4`). Not the reordered chain and not the warning-lane opener: the refusal is at recognition, before any upgrade runs.

Fix (code, not the test; the test asserts nothing the integration changed): `is_request_id_predecessor_registration` admits the handover `-v1` and `-v2` identities; `request_id_predecessor_family_identity` names `flow_nexus_successor_intents` as `flow-nexus-successor-intent-v3`.

Verified on Prometheus with the check's own binaries: the new daemon over the check's 0.53.2 fixture Memory with the fix, run through `cargo test --lib -- --exact store::request_id_migration_process::actual_predecessor_memory_evolves_serves_and_refuses_malformed_policy_without_writing --ignored` (predecessor binary, fixture and a debug build of `flow-nexus-daemon`, `FLOW_MIGRATION_*` as the drv sets them): `ok`, 47 s. The Nix check is re-run in the gate below.

Commit 898a54e4 (pushed to `integration-98df55`): `store.rs` only.

## Step 2 — build-base repin

Commit e41d5bf4: `flake.lock` only, `base` from release-98df55 9d939cc to build-base main `ec5d5d92eb4058b3dc900ce84595508ee573f61b` (narHash zgLY1Soa…). `nix flake lock --override-input base github:LiGoldragon/build-base/ec5d5d92…`. Nothing else changed. Gate of this head (log `/tmp/claude-1001/-home-li-primary/5c558632-6477-5e42-8f93-c95fe58f8c5c/scratchpad/gates/flow-e41d5bf4.log`) was started before step 3: result below.

## Step 3 — the Refresh caller as a Memory fact

Reading, since the ruling says "Caller bare" and the code already has one typed caller: the Caller recorded is the `RefreshCaller` the Nexus already reads from the calling process (`AddressFlow.FlowId` for a flow of the refreshed Address, `Elsewhere.Origin` for a flow of another Address or a process in no flow, including the meta socket's Refresh). It moved from `operation.ethos` to `memory.ethos` (the Memory root's type; every consumer path updated). It is a plain field, not an `Option`, not a `Recorded|Unrecorded` pair, and nothing defaults it: `Elsewhere(Unbound)` is what the Nexus reads for a process in no flow, as it already did before this change. The translator's `Caller.{ ProcessId UserId }` is not a Flow dependency on this branch (Flow reads the peer through `signal_flow::Process` and `ReadsRefreshCaller`), and a bare process id is not a durable identity (reuse), so the flow-level reading is stored. Question 3 below.

Memory (ethos, regenerated with ethos-zero f23eacf: `src/generated/memory.rs`, `operation.rs`):
- `ReplacementOrder.[ Refresh.RefreshCaller Launch.Box<OrderedLaunch> Restart ]`: the queued refresh request. `OrderedReplacement` v1 -> v2.
- `SuccessionCause.[ Refresh Exit Ordered.RefreshCaller Replace EmergencyRefreshWithoutHandover… ]`: the succession a Refresh orders. `SuccessorIntent` v4 -> v5. A threshold `Refresh`, `Exit`, `Replace` and the emergency cause have no caller (nobody called) and stay as they were.
Carried: `refresh` -> `queue_refresh(address, flow, caller)` records it; a Refresh already waiting keeps the caller it was queued with (the second caller is answered RefreshQueued, the record is not rewritten); at the flow's rest `replace_as_ordered` hands the stored caller to `refresh_held`, which owes the successor as `Ordered(caller)`; an owed `Ordered(caller)` taken up after a restart passes through `refresh_successor_first` unchanged. The log line `Refresh of … called by …` and the `CallerNotCurrent` rejection are as they were (the refusal diagnostics).

Upgrade, in the ordered chain after the recovery step (`store/refresh_caller_upgrade.rs`, new): frozen `OrderedReplacementV1` and `successor_upgrade::SuccessorIntentV4` (v4 is now frozen there too; the recovery step's v3 -> v4 writes it, its descriptor `descriptor_v4`, and the current v5 descriptor declares V3 and V4 as predecessors). The step reads both old families before writing: any queued Refresh (v1) or `Ordered` succession (v4) refuses the whole open with `StoreError::RefreshCallerUpgrade(Vec<OpenRefreshWithoutCaller>)`, naming each row: queued Refresh by Address and predecessor flow; succession by Address, predecessor and launch request id. Nothing is written when it refuses (both families stand at v1 and v4). With none open it upgrades both and every other row carries over unchanged. Registration identity admits v1 and v4 (`is_current_flow_registration`) and the 0.53.2 era names ordered replacements at v1.
Deviation: a queued Refresh has no request id of its own (the RefreshQueued answer carries none, and the row is keyed by Address), so its identity in the refusal is Address plus predecessor flow; the succession row's request id is its launch request id. Question 1.
`UPGRADES.md` says so.

Tests (all in `crates/flow-nexus`, passing on Prometheus):
- `store::refresh_caller_upgrade::tests::an_open_refresh_without_a_caller_refuses_the_upgrade_naming_each_one`: exact `OpenRefreshWithoutCaller` list (two queued Refreshes, one Ordered succession; Launch, Restart, threshold, Exit and Replace rows are no refusal), the refusal text, nothing written, same on a second open.
- `…::with_no_open_refresh_both_families_upgrade_and_every_row_carries_over`.
- `…::a_current_refresh_and_its_succession_read_back_with_each_caller_kind`.
- `tests::refreshing::the_ordered_replacement_survives_a_nexus_restart` (now with a caller; a second caller does not replace the first; reopened store keeps it).
- `tests::refreshing::a_queued_refresh_hands_its_caller_to_the_succession_it_causes` (queue, reopen, rest, the owed succession is `Ordered(caller)`, reopen again).
- `tests::refreshing::an_immediate_refresh_records_its_caller_on_the_succession_it_causes`.
- `store::memory_bytes` compares the frozen hand layout with `OrderedReplacementV1` now (the generated type changed).

Commit 21fe85f0 (pushed): step 3, everything above. Gate of e41d5bf4 (steps 1 and 2): 18 of 19 attributes passed, among them `request-id-migration-process` (the real 0.53.2 Memory now opens and serves through the whole chain, so the chain upgrades a store with no open refresh) and `crate-versions`/`crate-features` (the repin needed nothing beyond flake.lock). The one failure was `flow-nexus`: 976 passed, 1 failed, 9 ignored: `handover_archive::tests::publication_timeout_kills_a_descendant_holding_capture_pipes_after_git_exits`, `src/handover_archive.rs:847` `read_to_string(child_pid)` NotFound. The same tests passed in the `default` check of the same run (990 passed there). Cause, from the test: its 200 ms publication deadline can end before the git pre-commit hook has written its pid file on a loaded builder. Not touched by this work; fixed in b795d905 by giving the deadline 3 s (the hook still sleeps 30 s, so the kill is still what ends it). Log `/tmp/claude-1001/-home-li-primary/5c558632-6477-5e42-8f93-c95fe58f8c5c/scratchpad/gates/flow-e41d5bf4.log`.

## Step 4 — the typed handover refusal

Commit c1624558: `configure_meta` answers `StoreError::HandoverConfigurationRefused(reason)` as `ConfigureRefused(ConfigureRefusal::HandoverConfigurationRefused(reason))`, the refusal meta-signal-flow 83 declares, with the store's refusal carried whole. Sol's negative-count fixture (`tests::configuring::recovery_text_is_seeded_configured_preserved_by_other_setters_and_reopened`) is back to expecting the typed refusal, now stronger than Sol's `ConfigureRefused(_)`: it asserts `HandoverConfigurationRefused(NegativeHandoverCount)`, and a zero publication deadline `InvalidPublicationDeadline`. This answers open question 2 of the predecessor's report (map it).

## Step 5 — combined gate

Head `c1624558abb270af1779e454416b8527dd9ca5c8` (pushed, `integration-98df55`). Gate log `/tmp/claude-1001/-home-li-primary/5c558632-6477-5e42-8f93-c95fe58f8c5c/scratchpad/gates/flow-c1624558.log`, exit 0: **19 of 19 attributes**, every one: cargo-nix, crate-features, crate-versions, curriculum-cargo-nix, flow-ethos, flow, flow-meta, flow-defaults, flow-native, flow-request-id-immutable-contract-pins, no-inherent-methods, no-free-functions, fmt, doc, capsule-witnesses, configured-package, request-id-migration-process (1 passed), flow-nexus, default. flow-nexus: 995 passed, 0 failed, 9 ignored (unit 982 passed/8 ignored, integration 10/1, 3). The 995 are the 990 of the predecessor's head plus 5 new (3 upgrade tests, 2 refreshing tests; the restart test was extended, not added).

## Commits on integration-98df55 since e3730092

- 898a54e4 step 1, predecessor-era identities (store.rs)
- e41d5bf4 step 2, build-base ec5d5d92 (flake.lock)
- 21fe85f0 step 3, Refresh caller as a Memory fact
- b795d905 flaky publication-timeout test, 200 ms to 3 s
- c1624558 step 4, typed handover refusal

## Open questions

1. The refusal's "request id": a queued Refresh has none (its row is keyed by Address; the RefreshQueued answer carries no id), so it is named by Address and predecessor flow, and an ordered succession by Address, predecessor and launch request id. Is that the identity wanted, or should a Refresh gain a request id first?
2. The refusal covers `Ordered` successions as open refreshes. A threshold `Refresh` cause (nobody called) and `Replace` (a Launch with its own origin) are not refreshes with a missing caller and upgrade. Is that the wanted line?
3. The stored Caller is the flow-level `RefreshCaller` the Nexus already reads from the peer (`AddressFlow` or `Elsewhere.Origin`), not the translator's raw `Caller.{ ProcessId UserId }` (Flow does not depend on the translator on this branch, and a pid is not a durable identity). Wanted, or should the raw peer credentials be added beside it once Flow takes the translator?
4. A second caller of an already queued Refresh keeps the first caller's record (answered RefreshQueued). Plainest reading; the later caller is only in the log line.
5. Carried from the predecessor: nothing writes the emergency cause; release order (the set rests on build-base main ec5d5d92 now, so question 3 of the predecessor is closed).
