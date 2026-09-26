# Flow 0.12.1: the live store opens cleanly

An Opus subflow of 38de5b did this on 2026-09-25. It follows the L1 finding in `receipts/flow-l1-resolve-caller.md` that the live store's launch-attempt rows do not decode. The work ran in a fresh clone in the scratchpad dir `store-0121-38de5b`, under Orchestrate lock 6646, which was released before return.

## Revision

- flow `fe709c7e20efc2dc5f4c7bac5969f3be57c610b4`: 0.12.0 → **0.12.1**. `git ls-remote origin main` printed this revision after the push.
- The version is a patch. The rule is that a repair of how the Nexus reads its own store takes a patch when there is no wire or contract change. Here signal-flow and meta-signal-flow are not touched, and the one new table is additive.
- Local `nix build` (`--option builders '' --option substituters https://cache.nixos.org`) gave `/nix/store/42xmmsnnsjr6pq7q8jj7p0mx9mqxf3cw-flow-0.12.1`. Its check phase ran 6+3+113+1+1 tests with 0 failed, and `flow-nexus --version` prints `flow-nexus 0.12.1`.

## What the undecodable rows are

A per-row probe of a copy of `~/.local/state/flow/flow.sema` found two rows in `flow_nexus_launch_attempts`:

- `flow06-luna6-20260924-2305` does not read in the current shape. It does read as the shape from before signal-flow 3.0.0 (ab70332), which added `SystemPromptBundleFile` to `LaunchProfile`. It is a Flow 0.6 disposable acceptance launch with origin 5f38bc, in phase NativeLaunchIntentRecorded, and never bound. This one row made every whole-table read fail.
- `psyche-opus-successor-e51411-1` reads in the current shape. It is 88475f's launch, in phase PromptAmbiguous and bound to 88475f.

The brief's premise needs one correction: the failure was never a change from 0.10 to 0.11. signal-flow 4.0.1 (used by 0.10.5 and 0.10.7) and 5.x archive `LaunchAttempt` byte-identically, as a diff of the generated structs shows. The live Nexus, which was restarted on 0.10.7 at 20:23:52 by someone else, logs the same failure: `flow-nexus: ambiguous launches unreadable: ... rkyv decode failed for table flow_nexus_launch_attempts`. 0.10.5 never scanned the whole table, so it never showed the problem.

All other tables decode in full: 13 flows, 13 routes, and no outcome or replacement tables.

## (1) 0.12.0 on the copy

A temporary XDG_RUNTIME_DIR alone would not have been safe. The store's configuration names `/run/user/1001/flow/flow.sock` and `flow-meta.sock`, and `listen` removes the socket file before it binds. A copy started that way would therefore have deleted the live sockets.

The run was instead done under `bwrap`, which bind-mounts scratch dirs over `/run/user/1001` and `~/.local/state/flow`, with XDG_RUNTIME_DIR and FLOW_SOCKET pointing there.

- 0.12.0 starts, and `List.{}` answers 13 flows. `LaunchStatus` answers.
- The whole log is one untyped line that names no row: `flow-nexus: ambiguous launches unreadable: sema-engine operation failed: sema: rkyv decode failed for table flow_nexus_launch_attempts: subtree pointer overran range: ...`.
- The ambiguous-launch promoter and role adoption from launches silently see nothing. As a result 88475f has no role.

## (2) The change (`crates/flow-nexus/src/store.rs`)

When the store opens, `settle_launch_attempts` reads each row by itself.

- **Reading the rows.** Each row's key and archive bytes come through the engine's read-only `storage_reader()`, reading the redb table as raw bytes. This is an exception, noted at the site. `redb = "4"` was added, and it is the same 4.3.0 that sema already locks.
- **Rows that read.** A row that reads in the current shape stays where it is.
- **Moving a row aside.** Any other row goes, in one atomic commit, into the new `flow_nexus_quarantined_launch_attempts` table, and its retraction is part of that commit. The record kept is `QuarantinedLaunchAttempt { launch_request_id, quarantine_number, archive, shape }`, which holds the original bytes. The retraction goes through a zero-size `UnreadLaunchAttempt` view of the same table, whose empty archive checks against any bytes. This is an exception, noted at the site.
- **Migration.** A row whose shape is `BeforeSystemPromptBundle` is carried forward into the current shape with an empty `SystemPromptBundleFile`, the one field its archive never held. This logs `flow-nexus: LaunchAttemptMigrated.{ <id> BeforeSystemPromptBundle }`. If a carry is interrupted after the row was moved aside, the next open completes it.
- **Quarantine.** A row that no known shape reads stays only in quarantine and logs `flow-nexus: LaunchAttemptQuarantined.{ <id> «<decode error>» }`.
- **Failure of the step itself.** If settlement fails as a whole, the log says `LaunchAttemptsUnsettled.«…»` and the store still opens. Role adoption then logs `RoleAdoptionWithoutLaunchAttempts.«…»` rather than defaulting silently.
- **What each open did** is kept on `FlowStore::opening_settlements` as well as being logged.
- **Roles.** Once every row reads, adoption again takes a launched flow's role from the profile of the launch that bound it.

## Fixtures (121 before → 124 after, 0 failed; clippy `--all-targets` 0 warnings; `cargo fmt --check` clean)

- `earlier_launch_attempt_rows_are_migrated_or_quarantined_once_and_logged` covers a store holding a current row, a row from before the bundle field that bound a flow registered without a role, and an unreadable row.
  - On reopen, the settlements are exactly [Quarantined, Migrated], and the exact log lines are checked.
  - The migrated row equals the earlier row carried forward, and the current row is unchanged.
  - The ambiguous scan, `flow_nodes` (which is what List reads) and `launch_requests_bound_to` all read.
  - The quarantine table holds both rows' original bytes, each with its shape.
  - The bound flow's role is Psyche Medium claude-opus-5-5, taken from the migrated profile.
  - A third open does nothing.
- `a_carry_interrupted_after_quarantine_completes_at_the_next_open`.
- `a_nexus_over_earlier_launch_attempt_rows_opens_and_answers` runs at the RunningNexus level. List answers, LaunchStatus answers LaunchPending for the migrated request, and the quarantined request is UnknownLaunchRequest.

## (3) The nix-built 0.12.1 on the same copy (same bwrap isolation)

- **Start.** It starts. Its whole log is `flow-nexus: LaunchAttemptMigrated.{ flow06-luna6-20260924-2305 BeforeSystemPromptBundle }`, and nothing is quarantined.
- **List.** `List.{}` gives `Listed` with 13 flows: 11 Pending, plus 5f38bc Active and 88475f Active.
- **ResolveCaller.** The flow CLI was run with `HERDR_SESSION=messaging-build HERDR_PANE_ID=w17:p1` faked in its environment, which is 88475f's pane. The live Herdr shows `psyche-opus-88475f` on `term_65c5883e612c88a` there. The answers:
  - `ResolveCaller.None` gives `CallerResolved.{ 88475f Psyche Medium claude-opus-5-5 }`.
  - `ResolveCaller.Some.88475f` gives the same.
  - `Some.ffffff` gives `CallerMismatch` carrying it.
- **LaunchStatus for 88475f.** 88475f has no launch of its own name, so this queries its launch request `psyche-opus-successor-e51411-1`. The answer is `Started.{ 88475f 88475fd7-e328-4e11-9094-db2139a08fe0 { e51411 e5141130-… handover-successor } }`. The startup promoter, now able to read, found the native receipt in 88475f's transcript. It turned PromptAmbiguous into Started and made 88475f Active, in the copy only. Deploying 0.12.1 will do the same on the live store.
- **The migrated attempt.** `LaunchStatus.flow06-luna6-20260924-2305` answers `LaunchPending` with the migrated attempt, whose bundle file is `«»`.
- **The live store was not written.** `~/.local/state/flow/flow.sema` still carries the 20:23 mtime of the 0.10.7 restart. The live sockets were never touched.

## Not settled

- **5f38bc still resolves `CallerUnknown`.** It was registered through the meta `RegisterFlow` (flow type `codex-registered`), and no launch in the store bound it. The only role-shaped text is its Herdr agent name `field-astra-5f38bc`. 00f95a's M1 gate keeps 5f38bc roleless until its receipt and model are verified, so I did not derive a role from that name. A MetaBindExisting for 5f38bc with an explicit role would add the role without disturbing its binding: the store matches the existing thread, harness and route, and asserts the role only when none is present.
- **Only the launch-attempt table is settled.** The outcome and replacement tables are absent in the live store and are not settled the same way.
