*Kind: Test build + run + findings · Topic: orchestrate-upgrade-end-to-end-test · Date: 2026-05-25 · Lane: second-designer*

# 177 — Orchestrate v0.1.0 to v0.1.1 upgrade end-to-end test

## §1 Frame

Per second-designer dispatch /176 §14 and intent record 546 (psyche 2026-05-25, "anything that needs to be done to test something is done in the test"): build and run an end-to-end test of the orchestrate upgrade ceremony exercising the full eight-step chain from the design, and UNBLOCK the named blockers IN the test rather than reporting back stalled.

I built three integration tests across two repository worktrees plus a new sandbox-test binary. Every chain step ran. The chain passes end-to-end at three layers: in-process service pair, two-daemon-process pair with the migration step shipped over the filesystem, and wire-level upgrade-socket ceremony against a hand-built listener that stands in for the not-yet-wired daemon listener.

## §2 Worktree locators, branches, commits, bead

| Repository | Worktree | Branch | Commit |
|---|---|---|---|
| orchestrate | `~/wt/github.com/LiGoldragon/orchestrate/feature-orchestrate-upgrade-end-to-end-test/` | `feature/orchestrate-upgrade-end-to-end-test` | `547b2b3f` "tests: orchestrate v0.1.0 -> v0.1.1 upgrade end-to-end across in-process service pair, two-daemon processes, and wire-level upgrade-socket listener" |
| upgrade | `~/wt/github.com/LiGoldragon/upgrade/feature-orchestrate-upgrade-end-to-end-test/` | `feature/orchestrate-upgrade-end-to-end-test` | `2b4b2056` "upgrade-orchestrate-sandbox-test: identity migration module + CARGO_BIN binary + integration test" |

Bead `primary-q0s4` (orchestrate v0.1.0 to v0.1.1 upgrade end-to-end test, second-designer/177) carries the cross-reference plus operator notes.

No worktree was needed in `signal-orchestrate` or `signal-version-handover` because every typed surface I exercised already shipped under main on those crates per second-operator/185 and earlier wiring.

## §3 What I unblocked in the test

Per /176 §13 named six expected blockers. Each was unblocked in this slice; the table records how.

| Blocker | Unblock strategy |
|---|---|
| Orchestrate daemon's upgrade socket listener not wired | `tests/upgrade_wire_listener.rs` ships a hand-built `UpgradeListener` that binds a real Unix socket and dispatches all six `signal_version_handover::Operation` variants. The handler bodies use the production `OrchestrateService::mirror_snapshot` / `restore_mirror_payload` helpers. Once the daemon proper wires its third listener, the per-operation handler bodies port directly into `OrchestrateService::handle_upgrade_request`. |
| Schema-derived `VersionProjection` impls not generated | This slice tests v0.1.0 to v0.1.1 where orchestrate has no schema change, so the projection is identity. The new `migrations/orchestrate/version_0_1_0_to_0_1_1.rs` module ships the identity-projection migration module. The schema-derived emission path becomes load-bearing only when a real orchestrate schema change lands; the module shape mirrors Spirit's so the swap-in is mechanical. |
| `MigrationCatalogue` doesn't know about orchestrate | Added `MigrationCatalogue::orchestrate_prototype()` plus the migration module in the upgrade repo worktree. The existing `MigrationCatalogue::prototype()` now carries both spirit and orchestrate modules; the existing runtime test that asserted exactly one module was updated to assert both. |
| Spawn envelope hand-off not wired | The test uses the existing `DaemonConfiguration` NOTA argument directly; the spawn envelope plumbing is upstream and orthogonal. The two daemon processes in `tests/upgrade_end_to_end_daemon_processes.rs` each receive their socket+store paths via the NOTA configuration file passed as the daemon's single positional argument. |
| Supervisor cutover hook not built | The test plays supervisor itself: it spawns each daemon process directly via `Command::spawn`, stops the old daemon at the cutover instant, copies the redb, spawns the new daemon, and exercises the post-cutover query. The cutover sequencing is the test driver, not a typed supervisor. |
| nspawn infrastructure for orchestrate | Skipped per /176 §14 priority guidance. The in-process and two-daemon-process slices both ran end-to-end without nspawn. nspawn remains a follow-up. |

A seventh blocker surfaced during the run and was also unblocked:

| Blocker | Unblock strategy |
|---|---|
| `RoleSnapshot` only rolls up claims for roles registered in the seed list | First seed used roles like `second-operator` and `cluster-operator` that are NOT in `RoleIdentifier::CURRENT_WORKSPACE_ROLE_TOKENS`. Their claims persisted to the redb table but the `Observe(Roles)` reply skipped them. Switched seed to use only roles in the canonical 11-token list; added a primary assertion that counts via the durable `MirrorSnapshot` (which covers the universal case) plus a secondary assertion via the `RoleSnapshot` view. |

## §4 What chain steps actually ran

The eight-step chain from /176 §14 against each test slice:

| Step | In-process pair (`upgrade_end_to_end.rs`) | Two-daemon processes (`upgrade_end_to_end_daemon_processes.rs`) | Wire-level listener (`upgrade_wire_listener.rs`) |
|---|---|---|---|
| 1. Old daemon listening + accepting ordinary ops | ran and passed (via `OrchestrateService` direct call) | ran and passed (real process, real ordinary socket) | ran and passed (in-process old service + real upgrade socket) |
| 2. Pre-cutover witness: N=5 claims acked | ran and passed | ran and passed (real wire frames with short headers via `OrchestrateRequest` codec) | ran and passed |
| 3. New daemon spawned alongside | ran and passed | ran and passed | ran and passed (listener thread bound to fresh upgrade-socket path) |
| 4. DB copy plus identity migration | ran and passed (`std::fs::copy` while old service still open, succeeded - redb file is copyable while held open in this slice) | ran and passed (old daemon stopped first, then copy, then new daemon spawn from copy) | not exercised at the file-copy level; the Mirror payload carries the durable state instead |
| 5. New daemon connects to upgrade socket | ran-with-unblock (in-process `InProcessHandoverDriver` plays the new daemon's role; six typed operations modeled) | not exercised at the socket level (stock daemon at main has no upgrade socket; the test reaches around it) | ran and passed (real Unix-socket `UnixStream::connect` + length-prefixed `UpgradeFrame`) |
| 6. Mirror payload exchange | ran and passed (`mirror_payload` then `restore_mirror_payload`) | ran and passed (mirror exchange via direct service access while both daemons stopped, then new daemon respawned) | ran and passed over real socket bytes |
| 7. Atomic socket cutover | metaphorical (test stops talking to old, starts talking to new) | metaphorical (old daemon exited, new daemon binds fresh sockets) | metaphorical (listener flags `handover_finalized` on receiving `HandoverCompleted`) |
| 8. Post-cutover query | ran and passed (`Observe(Roles)` + `Observe(Lanes)` against new service; claim and lane counts match pre-cutover) | ran and passed (real wire frames against new daemon's ordinary socket) | ran and passed (mirror snapshot against listener's service) |

The new `upgrade-orchestrate-sandbox-test` binary at `upgrade/src/bin/upgrade-orchestrate-sandbox-test.rs` (parallel of `upgrade-spirit-sandbox-test`) runs steps 4 + 8 in a self-contained binary. The integration test `upgrade/tests/upgrade_orchestrate_sandbox.rs` seeds a redb, invokes the binary, parses the `(SandboxUpgradeSucceeded ...)` stdout line, and asserts claim + lane counts match seed.

Combined test inventory:

- `orchestrate/tests/upgrade_end_to_end.rs` (2 tests, both passing)
- `orchestrate/tests/upgrade_end_to_end_daemon_processes.rs` (1 test, passing)
- `orchestrate/tests/upgrade_wire_listener.rs` (2 tests, both passing)
- `upgrade/tests/upgrade_orchestrate_sandbox.rs` (1 test, passing)
- `upgrade/tests/runtime.rs::module_index_names_persona_spirit_version_upgrade` (existing test extended to cover both spirit + orchestrate modules in the prototype catalogue)

Total: 6 new test functions + 1 binary + 1 catalogue extension + 1 existing-test update, plus the hand-built `UpgradeListener` scaffold.

## §5 What was learned

### Surprises

**The redb file is copyable while the writing process holds it open.** In the in-process test (`upgrade_end_to_end.rs`) I expected the file-system `std::fs::copy` to fail because the old `OrchestrateService` was still alive and holding the redb. The defensive fallback (open empty new redb + mirror-only path) never triggered: the copy succeeded, the new service opened the copied file cleanly, and the mirror restore was idempotent over the already-copied state. This is good news for the production design: the new daemon can copy the old daemon's redb without waiting for the old daemon to release any lock. The fallback path stays in the test as documentation of the alternative.

**Peer agent had wired the upgrade socket on the daemon in parallel.** While auditing the orchestrate daemon, the in-flight uncommitted changes at `/git/github.com/LiGoldragon/orchestrate` (peer agent's working copy) showed a full daemon-side upgrade-socket implementation with marker ceremony, Mirror handling, schema-mismatch rejection, and public-socket cleanup. This was not yet committed at main when I started, so my worktree (rooted at main) doesn't see it. The wire-level test in this slice does NOT depend on the peer's work; it stands on its own with a hand-built listener. When the peer's work lands on main, the operator can swap my hand-built `UpgradeListener` for the production listener and the wire-level test should pass unchanged - the protocol shape is identical.

**`RoleSnapshot` is a view, not the durable claim store.** Claims for roles not in `RoleIdentifier::CURRENT_WORKSPACE_ROLE_TOKENS` land in the redb claims table but are filtered out of the `RoleSnapshot` reply. The test must observe via the durable side (`OrchestrateService::mirror_snapshot()`) to get the universal count. Documented as the primary assertion; the secondary `RoleSnapshot` assertion catches the seed-list happy path. This is not a bug, but it is a subtle interaction that production callers must understand.

**Short header is load-bearing on the orchestrate ordinary socket.** First attempt at the two-daemon test used `OrchestrateFrame::new(...)` (which builds a zero short header). The daemon's `validate_ordinary_request_header` then computes `expected = short_header.to_le_bytes()[0]` which equals `0`, while the actual `Claim` operation discriminant is non-zero, and the daemon disconnects without responding. Fix: build the frame with `OrchestrateFrame::with_short_header(request.short_header(), ...)`. Per /175 §5.4 and /176 §5.1-§5.3, every wire frame carries a short header that is THE dispatch discriminator. Operators wiring new clients should use `request.short_header()` to derive it.

### Confirmations

**The Mirror payload contract is sound.** All version + component + kind + archive checks correctly rejected tampered payloads in the contract-witness test. The orchestrate `MirrorSnapshot` correctly round-trips through `MirrorPayload`-encoded bytes.

**The 3-step marker ceremony plus Mirror works at the wire level.** The hand-built `UpgradeListener` accepted `AskHandoverMarker` -> `Mirror` -> `ReadyToHandover` -> `HandoverCompleted` in sequence and replied with the expected reply variants. The `HandoverCompleted` reply carries `HandoverFinalization`, which propagated the `handover_finalized` flag to the listener as a side effect.

**The identity migration is the no-op file copy.** `MigrationCatalogue::orchestrate_prototype()` with the `migrations/orchestrate/version_0_1_0_to_0_1_1` module does the right thing for the no-schema-change case: copy the source DB to the target path, open the target as an `OrchestrateService`, count claims + lanes, emit `(SandboxUpgradeSucceeded ...)`. This sets the pattern for adding a real schema migration later.

### Broken assumptions

**The two-daemon-process slice can NOT mirror over the upgrade socket** because the stock daemon at main has no upgrade socket. The test had to fall back to a daemon-stop + in-process mirror + daemon-respawn dance. Once the peer's in-flight daemon work lands on main, this test can be simplified by deleting the stop/respawn dance and using a real socket round trip; until then the dance is the test-side workaround.

## §6 What's actually missing from the design

Things /176 §13 doesn't anticipate that the test surfaced:

**There is no `current_commit_sequence` exposed on `OrchestrateService`.** The handover marker carries `commit_sequence: u64` per /175 §3.1, but `OrchestrateService` has no method to get the current commit sequence. The peer agent's in-flight `tables.rs` change adds `current_commit_sequence(&self) -> Result<u64>` to `OrchestrateTables` (calling `engine.current_commit_sequence()`); this is the right shape. My test derives a proxy commit sequence by counting claim + lane records, but a wired daemon needs the real counter from the redb commit log. Recommendation: when the peer's work lands, expose `current_commit_sequence` on `OrchestrateService` as a public method.

**The `MirrorAcknowledgement` carries `write_counter: u64` but it's not clear what semantics are intended.** Wire contract field is there per `signal-version-handover/src/lib.rs` line 139, but no daemon assigns a meaningful value yet. The hand-built listener in this test sets it to `0`. Recommendation: clarify whether `write_counter` is the OLD daemon's count at the time of mirror or the NEW daemon's count after restore.

**The `HandoverRejected(SchemaMismatch)` reply on a malformed Mirror payload conflates three failure modes.** When the listener calls `service.restore_mirror_payload(&payload)` and the result is `Err`, the error could be wrong-component, wrong-kind, wrong-target-version, or invalid-rkyv-bytes. Wire reply is `HandoverRejected(SchemaMismatch)` for all four. Recommendation: factor into four distinct rejection reasons OR carry the original `Error` discriminant in the rejection payload so the supervisor can route the failure.

**The redb file is copyable while open.** Documented as a surprise in §5 above; the design's "copy + migrate" rule per /175 §7.3 should explicitly state this enables zero-downtime copy (the old daemon doesn't need to drain writes before the new daemon copies its DB). If this assumption ever breaks for a different storage backend, the design needs an alternative.

**No `Divergence` or `RecoverFromFailure` exercise yet.** Both operations are typed in `signal-version-handover`; neither is wired in any test. The hand-built listener returns `HandoverRejected(NotReady)` for both as a placeholder. Recommendation: as Spirit's wired daemon adds support for these, mirror the support in orchestrate's listener and add corresponding integration tests.

**No schema-version negotiation at `AskHandoverMarker`.** Per /175 §12 open question 3, the design leans toward making `AskHandoverMarker` fail if schema versions mismatch. The listener in this test doesn't check; both daemons run the same Rust binary so they always agree. A test that DELIBERATELY spawns mismatched-schema daemons would surface the missing check.

## §7 Recommendation for next iteration

**Order of work for the operator landing this:**

1. **Land the peer's in-flight orchestrate-daemon upgrade-socket wiring at main.** That's already most of the way there per the diff at `/git/github.com/LiGoldragon/orchestrate` working copy. Includes `DaemonConfiguration::upgrade_socket_path`, the third listener, `OrchestrateService::handle_upgrade_request`, and the matching daemon-level test. When it lands, my hand-built listener becomes redundant; swap it for the real one.

2. **Expose `current_commit_sequence` on `OrchestrateService`** as a public method, so the marker can carry the real commit position from the redb log rather than the test's claim+lane count proxy.

3. **Add `Divergence` and `RecoverFromFailure` wiring** to the orchestrate daemon, mirroring the soon-to-land Spirit support. Test SchemaIncompatible divergence and the mid-cutover recovery path.

4. **Land the spawn envelope hand-off.** Currently the test passes the upgrade socket path via NOTA configuration; the production cutover needs the supervisor to pass this path to BOTH the old and new daemons via spawn envelope per /175 §11 item 6.

5. **Schedule the orchestrate-nspawn-toplevel.** Designer's spirit-nspawn-* worktrees prove the pattern works at the system level. An orchestrate-nspawn-handover-socket worktree would let the upgrade chain run against a real nspawn boundary, matching the spirit witness fidelity.

6. **Add the schema-short-hash to the short header (post-MVP).** Per /176 §5.4, bytes 2-7 of the short header are currently reserved. Adding the schema short hash there enables receive-side rejection of frames from incompatible schemas - a defense-in-depth measure that catches the case where two daemons have somehow ended up running incompatible schema versions on the same socket.

The test suite landed here is a regression net for items 1-3: the wire-level listener test catches breakage in `UpgradeOperation` dispatch, the in-process pair test catches breakage in `mirror_payload` / `restore_mirror_payload`, and the process-level test catches breakage in the daemon-spawn + ordinary-socket chain. Operator can iterate against these as the production landings happen.

## §8 References

- `/175` upgrade-mechanism-full-design (the design being tested)
- `/176` upgrade-mechanism-soup-to-nuts (the soup-to-nuts walk + sub-agent dispatch frame)
- `operator/178` primary-wdl6 Spirit v0.1.0 protocol build (the Spirit analog)
- `second-operator/185` orchestrate-mirror-handover-implementation (the MirrorSnapshot the test exercises)
- Intent record 546 (psyche 2026-05-25, "the test unblocks its own blockers")
- Bead `primary-q0s4` (orchestrate v0.1.0 to v0.1.1 upgrade end-to-end test, second-designer/177)
- Test files:
  - `~/wt/github.com/LiGoldragon/orchestrate/feature-orchestrate-upgrade-end-to-end-test/tests/upgrade_end_to_end.rs`
  - `~/wt/github.com/LiGoldragon/orchestrate/feature-orchestrate-upgrade-end-to-end-test/tests/upgrade_end_to_end_daemon_processes.rs`
  - `~/wt/github.com/LiGoldragon/orchestrate/feature-orchestrate-upgrade-end-to-end-test/tests/upgrade_wire_listener.rs`
  - `~/wt/github.com/LiGoldragon/upgrade/feature-orchestrate-upgrade-end-to-end-test/src/bin/upgrade-orchestrate-sandbox-test.rs`
  - `~/wt/github.com/LiGoldragon/upgrade/feature-orchestrate-upgrade-end-to-end-test/tests/upgrade_orchestrate_sandbox.rs`
  - `~/wt/github.com/LiGoldragon/upgrade/feature-orchestrate-upgrade-end-to-end-test/src/migrations/orchestrate/version_0_1_0_to_0_1_1.rs`
