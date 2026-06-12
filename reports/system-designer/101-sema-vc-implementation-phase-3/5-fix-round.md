# 101/5 — The fix round: every must-fix closed, re-reviewed, approved

*Fix-round run `wf_8b2831ee-e40` (2026-06-12). Three fix agents closed the phase-3 review findings; three re-reviewers reproduced the original failure scenarios against the fixed code and approved all three.*


## mirror: both wedges closed (self-heal proven), all advisories done

# mirror fix round — both must-fix wedges closed, all advisories done

## Reproduction baseline

The reviewer's witness crate at `/tmp/mirror-crash-witness` still existed and reproduced the wedge against mirror head `46193e3b`: after retire + re-register, the re-send returned `WEDGED: MirrorFaulted(... "ledger storage: assert key already exists: received-entries/spirit/...0001")`. After the fixes it prints `SELF-HEALED: AppendReceipt { ... head: HeadMark { sequence: CommitSequence(2), ... } }`.

## MUST-FIX 1 — crash-window re-send now heals

**Decision** (`/git/github.com/LiGoldragon/mirror/src/decision.rs`): the novel remainder is computed against the LOADED KNOWN ROWS, never the head sequence (`src/decision.rs:72-85`). `duplicate_divergence` became `known_divergence` (`src/decision.rs:186-200`): every request entry with a stored row must digest-match (`DigestMismatch` on divergence); a missing row at-or-below the head is `SequenceGap`; missing above-head rows are novel. `expected_head_violation` dropped the `mark_sequence > head_sequence` pre-rejection — the stored-row lookup is the authority, so a suffix may continue from a crash-window orphan row (`src/decision.rs:148-159`). The old `boundary_violation` was deleted: its guarantee is now fully implied by the expected-head row check plus in-suffix chaining plus known-row digest matching. An all-duplicate suffix ending above the head becomes `AcceptSuffix` with an EMPTY entries vector and head = suffix end — the head-only re-advance (`src/decision.rs:86-109`); an all-duplicate suffix at-or-below the head still acknowledges idempotently with the current head.

**Store** (`/git/github.com/LiGoldragon/mirror/src/store.rs`): `persist_suffix` (`:338`) skips the entry transaction when the remainder is empty (sema-engine rejects empty commits) and is now composed of the two honest transaction seams `commit_entry_rows` (`:350`) and `advance_head` (`:361`). `commit_entry_rows` is public as the crash-window seam — the witness commits the first transaction without the head advance, exactly the crash state.

**Witness**: `crash_window_resend_re_advances_the_head_and_the_store_stays_live` (`tests/daemon_logic.rs:278`) registers, drives `commit_entry_rows` for entries 1-2 without the head advance, then through the full Nexus path proves: a divergent re-send into the window is `DigestMismatch`; the honest re-send returns `Appended` head 2 (a re-asserted row would have faulted — sema-engine rejects duplicate assert keys, so `Appended` IS the no-duplicate-rows proof); the store stays live (append 3 succeeds; `ObserveHeads` shows head 3).

**ARCHITECTURE** (`ARCHITECTURE.md`, fsync-then-ack section): the self-heal claim is now stated in its true mechanism (known-rows dedup, digest-verified, head-only re-advance) and cites the witness; the append-decision bullets describe known-rows dedup including the crash window.

## MUST-FIX 2 — retire-then-re-register RESUMES the surviving chain

Chosen shape: **resume**, not refusal. Justification (in `ARCHITECTURE.md`, "The meta tier" section): retirement retracts only the head row and history rows cannot be deleted until retention enforcement lands, so a genesis restart wedges the name (every persist re-asserts surviving rows and faults) and refusal wedges it just as permanently — resume is the only outcome consistent with an append-only ledger. `Store::register_store` (`src/store.rs:401`) loads the surviving entry rows and restores the head from the highest one via the new `ReceivedEntry::to_head_stamp` (`src/store.rs:148`); a virgin name still starts headless. Observable through the typed working surface (`ObserveHeads`). Witness: `retire_then_reregister_resumes_the_surviving_chain` (`tests/daemon_logic.rs:349`) — retire, re-register, head restored to 2, idempotent full re-send acks, chain continues to 3.

## Advisories (all done)

- **Bounded TCP peer witness**: `MirrorService.observed_tcp_peers: Vec<PeerIdentity>` replaced by O(1) `TcpPeerWitness { served_request_count, last_peer }` (`src/service.rs:42,62-101`), queried via `TcpPeerWitnessQuery` (`src/service.rs:215`) / `ServiceLink::tcp_peer_witness`. `kameo::Reply` is hand-implemented because the derive emits absolute `::kameo` paths and mirror reaches kameo only through triad_runtime's re-export (`src/service.rs:67-86`). `tests/end_to_end_arc.rs:461-466` asserts count >= 1 and `last_peer` is `PeerIdentity::Tcp`.
- **StoreName validation**: `Store::name_is_keyable` (`src/store.rs:390`) owns the key-scheme predicate; `MirrorEngine::register_store` refuses separator-bearing names with the new typed `OrderRejectionReason::StoreNameInvalid` (`src/engine.rs:99-104`), added to the meta contract schema (`meta-signal-mirror/schema/lib.schema:63`, regenerated). Witness: `separator_bearing_store_name_is_refused_at_registration` (`tests/daemon_logic.rs:426`).
- **CLI/config error laundering**: typed variants `MissingArgument`, `NotaDecode(nota_next::NotaDecodeError)`, `SocketVariableUnset { variable }`, `Configuration(#[from] ConfigurationError)` (`src/error.rs:13-23`); `TailnetAddressInvalid` retired (its only producer was the laundering `From` in config.rs, now deleted — `ListenAddressInvalid` rides inside `Configuration`). `client.rs` run paths use the typed variants; zero `io::Error::other` laundering remains in `src/`.
- **Dead SEMA meta verbs**: chose ROUTE over delete — `handle_meta` now drives the DECLARED plane verbs: `LoadRegistry` backs the registration/retirement pre-checks and the registry observation (`src/engine.rs:174`), and `RegisterStore`/`RetireStore`/`PersistRetention` go through `SemaEngine::apply` via `apply_meta` (`src/engine.rs:164`), with a distinct meta origin route (`src/engine.rs:229`). Justification: the schema-declared verbs were the intended design (the engine module doc already claimed the meta tier drives the SEMA plane); routing makes the schema the one source of truth, gives meta mutations the generated trace hooks, and avoids plane-schema/identity churn — deleting would have left meta writes outside the declared SEMA write language entirely. `Store::is_registered` became dead and was removed.
- **signal-mirror**: unused `thiserror` dependency dropped (`signal-mirror/Cargo.toml`).
- **Self-report drift**: `the_mirror_own_store_name_is_pinned` (`tests/daemon_logic.rs:447`) pins `RecordFamily::STORE_NAME == "mirror:sema"`; the drifted `schema/sema.schema` header comment (which claimed the store name was `mirror`) now states the emitted identity `mirror:sema`; the ARCHITECTURE plane table names it too. Regeneration confirmed no structural emission change from the comment edit.

## Cross-repo sequencing

meta-signal-mirror gained `StoreNameInvalid` (schema + regenerated `src/schema/lib.rs`), pushed first; mirror then `cargo update -p signal-mirror -p meta-signal-mirror` to pins `4fa767d7` / `674f24d2`. All three repos are the mirror triad's canonical colocated checkouts, pushed straight to main per the greenfield rule.

## Verification

mirror: `cargo test` — daemon_logic 14/14 (4 new witnesses), end_to_end_arc 1/1, all other targets 0 failures; `cargo clippy --all-targets` clean (zero warnings); `cargo fmt` applied. signal-mirror: 14/14 tests, clippy clean. meta-signal-mirror: 6/6 tests, clippy clean. External witness crate re-run prints SELF-HEALED. End-of-session jj check: no unbookmarked descendants in any of the three repos (only empty working-copy commits).

## branches
- mirror @ main head 4724ac0172d4
- signal-mirror @ main head 4fa767d795f0
- meta-signal-mirror @ main head 674f24d2b61d

## testResults
mirror (head 4724ac01): cargo test full suite green — tests/daemon_logic.rs `14 passed; 0 failed` (new: crash_window_resend_re_advances_the_head_and_the_store_stays_live, retire_then_reregister_resumes_the_surviving_chain, separator_bearing_store_name_is_refused_at_registration, the_mirror_own_store_name_is_pinned), tests/end_to_end_arc.rs `1 passed; 0 failed`, all bin/lib/doc targets 0 failed; cargo clippy --all-targets: zero warnings, `Finished dev profile`. signal-mirror (4fa767d7): `14 passed; 0 failed`, clippy clean after thiserror removal. meta-signal-mirror (674f24d2): `6 passed; 0 failed`, clippy clean after StoreNameInvalid regen. External reproduction witness /tmp/mirror-crash-witness: before = `WEDGED: MirrorFaulted("ledger storage: assert key already exists: received-entries/spirit/...0001")`; after = `SELF-HEALED: AppendReceipt { store: StoreName("spirit"), head: HeadMark { sequence: CommitSequence(2), ... } }`.
## blockers
- None. One coordination note (not a blocker): the StoreNameInvalid fix required a meta-signal-mirror contract addition (schema + regenerated lib, pushed as 674f24d2) and mirror now pins it via Cargo.lock; any other consumer of meta-signal-mirror main picks up the new enum variant on its next cargo update (additive, pre-production).


### Re-review

VERDICT: approve

## mustFix

## advisory
- register_store resume scans the store's entire surviving entry history into memory just to take the last row (src/store.rs:401-413, range key(store,0)..key(store,u64::MAX) then surviving.last()); a reverse/last-row range query against sema-engine would make re-registration O(1) instead of O(history). Correctness is fine (zero-padded fixed-width keys at src/store.rs:254-262 make lexicographic order numeric-faithful).
- RegisteredLedger::known_digest is a linear scan per lookup (src/decision.rs:120-124) inside per-entry loops in known_divergence and the novel-remainder filter — O(suffix^2) on large re-sends; a sequence-indexed map in RegisteredLedger would flatten it.
- The unreachable empty-suffix else arm at src/decision.rs:61-71 re-refuses EmptySuffix after the explicit emptiness refusal at line 43; restructuring so the nonempty proof carries (e.g. deciding from a split first/rest) would delete the dead branch.
- Meta and working origin routes are magic numbers (sema OriginRoute::new(2) at src/engine.rs:230, nexus OriginRoute::new(1) at src/engine.rs:334); named constants on the engine would make the plane-distinguishing intent greppable.
- Reproduction artifacts kept for the orchestrator: /tmp/mirror-rereview-witness (my driver: real drop-and-reopen crash-window restart + retire/re-register resume, prints ALL CLEAR), /tmp/mirror-crash-witness (prior reviewer's driver, now SELF-HEALED), /tmp/mirror-pre-fix + /tmp/mirror-pre-fix-witness (parent commit 46193e3 clone where the same driver still prints WEDGED — non-vacuity proof).
## testHonesty
Claims verified exactly, nothing inflated. Pushes: local main == origin/main in all three repos at the claimed heads (mirror 4724ac0172d4, signal-mirror 4fa767d795f0, meta-signal-mirror 674f24d2b61d), trees clean, and mirror/Cargo.lock pins both contracts at those same revisions, so the tested graph is the pushed graph. Suites re-run by me: mirror tests/daemon_logic.rs '14 passed; 0 failed' including the four new witnesses (crash_window_resend... at tests/daemon_logic.rs:278, retire_then_reregister... :349, separator_bearing... :426, pinned-store-name :447), tests/end_to_end_arc.rs '1 passed; 0 failed', all bin/doc targets 0 failed; signal-mirror '14 passed; 0 failed'; meta-signal-mirror '6 passed; 0 failed'. Clippy claims were cache-masked on first run, so I touched sources to force re-lint in all three crates: genuinely zero warnings, 'Finished dev profile'. The claimed external witness reproduced verbatim: prior driver against pre-fix parent 46193e3 (throwaway clone) prints WEDGED: MirrorFaulted(FaultDetail(\"ledger storage: assert key already exists: received-entries/spirit/00000000000000000001\")); the identical driver against the fixed head prints SELF-HEALED with head CommitSequence(2) — matching the claim byte-for-byte in substance. I went one step further than the claim with my own driver (/tmp/mirror-rereview-witness): the crash window is staged through the public Store::commit_entry_rows seam (src/store.rs:350) followed by a REAL restart (store dropped, reopened from disk), then divergent re-send -> DigestMismatch, idempotent re-send -> head-only re-advance to 2, continuation append -> head 3; and retire/re-register resumes at head 2 with both the idempotent full re-send and the direct continuation append succeeding — ALL CLEAR, exit 0. Mechanism audit found no regression hiding behind the green: dedup now runs against loaded known rows (src/decision.rs:77-99, known_divergence :186-200), while continuity stays fully enforced — suffix_inconsistency (:127-139) checks internal consecutiveness/digest chaining, expected_head_violation (:144-179) checks mark+1 == first sequence, digest linkage, and that the mark names a STORED row; the loaded known range spans first-1..last (src/store.rs:307-322) so those lookups are never vacuous. The advisory commits are real: signal-mirror 4fa767d7 removes thiserror from Cargo.toml (remaining lock hits are other crates' transitive deps), meta-signal-mirror 674f24d2 adds StoreNameInvalid in both schema/lib.schema:63 and src/schema/lib.rs:145, mirror's meta tier routes register/retire/retention/registry through the declared SEMA verbs (src/engine.rs:94-230, apply_meta :164, load_registered :174) with the only direct store call left inside the SEMA read-verb handler itself (engine.rs:470, where it belongs), typed CLI/config errors landed (src/error.rs MissingArgument/NotaDecode/SocketVariableUnset/Configuration; no anyhow/eyre anywhere), and the TCP peer witness is bounded O(1) (TcpPeerWitness in src/service.rs, count + last peer, consumed by end_to_end_arc).


## spirit: pin bump, mutation/retraction log witnesses, migration-swap hardening

# spirit `versioned-store-pilot` — fix round: review advisories closed

All four named advisories are closed on branch `versioned-store-pilot`, commit `9c8c44b1` ("review hardening" — appended on top of the orchestrator's flake-lock refresh `a50cc732`), pushed. `flake.nix`/`flake.lock` untouched as instructed.

## 1. sema-engine pin bumped 39991c18 → 3593ffe6

`cargo update -p sema-engine@0.4.0 --precise 3593ffe6`. The lock now reads `git+...sema-engine.git?branch=versioned-fold#3593ffe62695a48cc4ebb08292571234c474faf6` (Cargo.lock:1185 pre-commit numbering). `sema-engine-previous` stays on `main#ebee6e44` (Cargo.toml:69, untouched). Re-verified myself: the full production-migration suite is green against the new pin — all four `production_migration::tests::*` unit tests pass by name (output below), plus every integration test binary.

## 2. Log-coverage witnesses for non-assert paths (tests/versioned_store.rs)

Two new witnesses drive the daemon-storage surface — the generated `SemaEngine` write trait the daemon itself dispatches through (`SemaEngine::apply` with `sema::Sema<sema::WriteInput>` envelopes, built by the test helper `sema_write` at tests/versioned_store.rs:138):

- `versioned_log_witnesses_mutation_payloads` (tests/versioned_store.rs:149): a certainty change (`WriteInput::change_certainty`) and a referent alias merge (`WriteInput::register_referent` against an already-registered referent with a new alias). It filters the decoded versioned log for `SemaOperation::Mutate` (typed label, via the new `signal-sema` dev-dependency, Cargo.toml:84 — no string sniffing), requires exactly two, decodes each payload through the generated closed sum `RecordFamily::decode`, and asserts: the records-family mutation is keyed to the mutated record and carries the post-mutation `Certainty::new(Magnitude::Zero)`; the referents-family mutation carries the merged alias set (`sema engine` + `semantic engine`). Per-family counters require one of each, so a mutation mis-filed into the wrong family also fails.
- `versioned_log_witnesses_retraction_tombstones` (tests/versioned_store.rs:247): a `WriteInput::remove` retraction. It requires exactly one `SemaOperation::Retract` operation and asserts the engine tombstone shape: `payload().is_tombstone()`, `payload().bytes() == None`, keyed to the removed identifier, family schema-hash equal to `RecordFamily::records_family().schema_hash()`; then proves the fold matches (removed identifier gone from the query surface, neighbor record survives).

A log-shape regression on either the mutation or removal path now fails these tests directly instead of passing unnoticed behind assert-only coverage.

## 3. Crash window: taken the trivially better ordering AND documented recovery

The two-rename swap (old src/production_migration.rs:1014-1016) had a window where the live `.sema` path was absent. Replaced with backup-hard-link + single atomic rename, so the live path is never absent (src/production_migration.rs:1050-1052):

```rust
let backup_path = Self::backup_path(&database_path);
fs::hard_link(&database_path, backup_path)?;
fs::rename(temporary_path, database_path)?;
```

`backup_path` mints the first free `<stem>.schema-old-backup-<N>.sema`, so the hard link never collides. The archive-sibling swap had the identical shape and gets the identical ordering (src/production_migration.rs:1093-1094). Crash analysis: before the rename the live path still holds the previous store (the previous engine probe/read is read-only); after the rename the migration is complete and a re-run reports `Current`. The previous store's bytes survive every crash at the backup path.

Documentation landed in both required places: a "# Crash safety of the in-place swap" module-doc section (src/production_migration.rs:20-46) covering the three crash positions, re-run behavior, and the operator rollback command (`cp <stem>.schema-old-backup-<N>.sema <stem>.sema`); and a matching bullet in ARCHITECTURE.md's SEMA migration section (after the `StoreMigration` bullet, ARCHITECTURE.md ~line 461).

## 4. Migration-marker key: one typed home

The hand-formatted key string moved off the `EngineRecord` trait impl into a named inherent method on the generated `Migration` noun — `Migration::marker_key(&self) -> RecordKey` (src/store.rs:1154-1164), typed in (`source_schema_version`), string out, documented as the single home of the format ("one marker row per migrated-from source version"). `EngineRecord::record_key` now delegates (src/store.rs:1167-1171). `from-schema-` appears in exactly one place in the repo.

## Verification

- `cargo clippy --all-targets`: 0 warnings (default features and `--features production-migration`).
- Full `cargo test` green on default, `production-migration`, and `testing-trace` feature sets (store.rs is shared by all); `nix_integration` tests are `#[ignore]`d in-sandbox by design (nix handled by the orchestrator).
- Witness file run: `4 passed; 0 failed` in tests/versioned_store.rs.

## Notes for the orchestrator

- Cargo.lock changed only the sema-engine rev (the `signal-sema` dev-dependency was already a transitive lock entry). The flake-pinned `3593ffe6` and the Cargo pin now agree.
- The first production-migration lib-test run took 218s wall (cold I/O); subsequent runs ~0.1-10s. Not a regression — same tests, same results.
- The hard-link swap assumes live, temp, and backup share a directory (they do — all are `with_extension`/`with_file_name` siblings) and a hard-link-capable filesystem (any Linux deploy target).

## branches
- spirit @ versioned-store-pilot head 9c8c44b15121

## testResults
cargo test (default): 14/14 binaries "test result: ok", 0 failed — incl. tests/versioned_store.rs "running 4 tests ... versioned_log_witnesses_retraction_tombstones ... ok / versioned_log_covers_every_durable_write ... ok / versioned_log_witnesses_mutation_payloads ... ok / checkpoint_and_suffix_restore_an_identical_store ... ok; test result: ok. 4 passed; 0 failed". cargo test --features production-migration: every binary ok, 0 failed; named migration tests: "production_migration::tests::upgrades_version_seven_domains_into_software_branch ... ok / second_migration_run_is_a_current_no_op ... ok / migrated_store_checkpoint_restores_an_identical_fresh_store ... ok / migrates_version_eight_store_as_a_logged_fold ... ok; test result: ok. 4 passed; 0 failed" (nix_integration: 9 ignored, sandbox has no nix). cargo test --features testing-trace: all ok. cargo clippy --all-targets: 0 warnings on default and production-migration feature sets.
## blockers



### Re-review

VERDICT: approve

## mustFix

## advisory
- Stale-temporary recovery doc is slightly oversold: src/production_migration.rs:1106-1108 mints the migration temporary as `<stem>.schema-9-migrating-<pid>.sema` (PID-suffixed), but the module doc (src/production_migration.rs:32-34) and ARCHITECTURE.md:469-470 say a re-run 'removes the stale temporary'. A re-run under a different PID computes a different temporary name, so the crashed run's temp file lingers as garbage (recovery itself still works — the fold writes a fresh temp and the swap succeeds). Either sweep `<stem>.schema-9-migrating-*.sema` on entry or soften the doc.
- The migration swap's backup is a hard link, so after a successful migration the backup path and nothing else holds the old bytes; the documented rollback `cp <stem>.schema-old-backup-<N>.sema <stem>.sema` is correct (cp, not mv, preserves the backup). Worth one ARCHITECTURE sentence noting backups are hard links and survive deletion of the live path.
- Self::backup_path (src/production_migration.rs:1110-1119) probes `exists()` then hard_links non-atomically; a concurrent second migration run could race the same suffix and fail typed on hard_link AlreadyExists. Acceptable for a single-operator tool; noting only.
- The re-review wedge proof lives at /tmp/rereview-wedge-witness (scratch copy of the prior reviewer's /tmp/mirror-crash-witness, extended to three flows: original retire/re-register/re-send, true crash-window orphan rows via Store::commit_entry_rows then re-send then continue, and retire/re-register then append-next). Mirror also carries the same proofs in-repo at tests/daemon_logic.rs:278 (crash_window_resend_re_advances_the_head_and_the_store_stays_live) and tests/daemon_logic.rs:349 (retire_then_reregister_resumes_the_surviving_chain), so the external driver can be discarded.
## testHonesty
Claims reproduced exactly; no overstatement found. (1) spirit default `cargo test`: 14 test-result lines, every one `ok`, 0 failed, including tests/versioned_store.rs 'running 4 tests' with versioned_log_witnesses_mutation_payloads / versioned_log_witnesses_retraction_tombstones / versioned_log_covers_every_durable_write / checkpoint_and_suffix_restore_an_identical_store all ok ('4 passed; 0 failed'). (2) `cargo test --features production-migration`: every binary ok, 0 failed; the four named migration tests (upgrades_version_seven_domains_into_software_branch, second_migration_run_is_a_current_no_op, migrated_store_checkpoint_restores_an_identical_fresh_store, migrates_version_eight_store_as_a_logged_fold) all ok; nix_integration '0 passed; 0 failed; 9 ignored' as claimed (no nix in sandbox). (3) `cargo test --features testing-trace`: all binaries ok, 0 failed (instrumentation_logging 4/4). (4) `cargo clippy --all-targets`: 0 warnings on default AND production-migration feature sets. (5) Changed code verified at the claimed head 9c8c44b1 (= versioned-store-pilot@origin, working copy clean): Cargo.lock sema-engine pin 3593ffe6 (line ~1185) + flake.lock sema-engine-source 3593ffe6; witnesses at tests/versioned_store.rs:149 and :247 drive the daemon's own generated SEMA write surface (SemaEngine::apply) and assert log shape (Mutate/Retract labels, RecordFamily decode, key = record identifier, tombstone bytes None, records-family schema hash); crash-window swap is a real code fix (fs::hard_link backup + single fs::rename, src/production_migration.rs:1050-1052 and 1092-1094, backup_path first-free-N at :1110-1119) with matching docs (module doc :19-47, ARCHITECTURE.md:463-475); typed Migration::marker_key at src/store.rs:1154-1171 is the single home of the 'from-schema-{}' format. (6) Mirror wedges re-proven against fixed mirror main 4724ac01 (pushed, @origin matches; clippy 0 warnings; full suite green incl. tests/daemon_logic.rs:278 and :349): rebuilt the prior reviewer's external driver from scratch (/tmp/rereview-wedge-witness, compiling mirror from /git/github.com/LiGoldragon/mirror and sema-engine versioned-fold#3593ffe6) — flow 1 original driver retire/re-register/re-send: HEALED (Appended, head seq 2); flow 2 true crash-window orphan rows (commit_entry_rows, head not advanced) then re-send then continuing append: HEALED head=3; flow 3 retire/re-register then append next off the resumed head: HEALED head=3. 'ALL FLOWS HEALED', exit 0. The previously-wedging scenarios no longer wedge.


## sema-engine: the last two integrity witnesses

## sema-engine `versioned-fold` fix round — two missing integrity witnesses

Branch `versioned-fold` advanced 3593ffe6 → dbe29427 with one commit (`tamper witnesses: dead latest-checkpoint cursor (CheckpointRowMissing); dangling segment reference at load (SegmentMissing before verify)`), touching only `tests/tamper.rs`. Bookmark pushed to origin.

### 1. `Error::CheckpointRowMissing` witness (raise site `src/engine.rs:1347`)

`tests/tamper.rs:39-40` redeclares the COUNTERS doctoring coordinates beside the existing engine-table consts: `const COUNTERS: sema::Table<&'static str, u64> = sema::Table::new("__sema_engine_counters")` and `const LATEST_CHECKPOINT_KEY: &str = "latest_checkpoint"` — exact mirrors of `src/engine.rs:37` and `src/engine.rs:41`.

Test `dead_latest_checkpoint_cursor_is_a_typed_missing_row` (`tests/tamper.rs:409-429`): builds a genuinely checkpointed store via the existing `Fixture::checkpointed`, computes a dead sequence (`genuine.metadata().sequence().value() + 7`), writes it under `LATEST_CHECKPOINT_KEY` through the raw storage kernel (the only write path to engine tables — `StorageReader` is read-only), reopens, and asserts `Engine::latest_checkpoint()` fails with `CheckpointRowMissing { sequence }` where `sequence == dead` — the doctored value, matched with a guard, not just the variant.

### 2. `Error::SegmentMissing` LOAD-path witness (raise site `src/engine.rs:1349-1354`)

The pre-existing witness (`segment_count_mismatch_is_typed_in_both_directions`, `tests/tamper.rs:540`) only covered the `verify()` count-shortfall raise at `src/checkpoint.rs:510`. The load-path raise — a referenced content address with no stored segment row — had none.

Test `flipped_segment_reference_dangles_at_load_before_verification_runs` (`tests/tamper.rs:471-505`): uses the existing `Splice::flipping` tooling to flip bit 0 of the stored `CheckpointMetadata` segment-reference digest and writes the doctored metadata row back through the raw kernel. Because the segment fetch loop at `src/engine.rs:1349-1354` runs before `Checkpoint::verify()` at `src/engine.rs:1358`, `SegmentMissing` fires first (the stale outer checkpoint digest is never reached). Assertions pin the carried digest to the independently reconstructed flipped value (`assert_eq!(digest, flipped)`), prove it differs from the genuine reference, and prove it is non-zero — in-bounds, real, non-fabricated.

The module doc (`tests/tamper.rs:5-7`) now names both stories: "a dead latest-checkpoint cursor and a dangling segment reference are typed at load before verification runs".

### Survey — other Error raise sites still lacking a behavioral witness

Read every `Error::` raise site (grep over `src/`, cross-checked against all 13 test files). Integrity raise sites with **no** behavioral witness:

- `ReplayMissingKey` — `src/fold.rs:195` (fold) and `src/engine.rs:1181` (`replay_versioned`). Reachable by an internally-valid forged tail entry (digest recomputed, key stripped), the same forgery shape `forged_replacement` already builds.
- `ReplayUnsupportedOperation` — `src/fold.rs:213` and `src/engine.rs:1203`. A digest-consistent forged entry carrying `Match`/`Subscribe`/`Validate` in the versioned log.
- `ReplayTombstonePayload` — `src/fold.rs:181` (checkpoint row), `src/fold.rs:203` (log operation), `src/engine.rs:1227` (replay). The fold.rs:181 case needs a digest-fixed-up forged checkpoint whose `ViewRow` carries a tombstone payload — the `fixed_up_outer_digest` test shows the fix-up technique but never targets this variant.
- `VersionedPayloadDecode` — `src/fold.rs:461` (`RowMaterializer::decode` during materialization) and `src/engine.rs:1232` (replay decode). Genuine-digest bytes that fail rkyv validation for the directory's chosen record type — the directory-contract seam.
- `MaterializeIdentifierParse` — `src/fold.rs:423`. An identified-family row whose key does not parse as a `u64` identifier; reachable via a doctored log for an identified family.

Uncovered but **not** integrity sites (noted for completeness, no action): `Sema` wrapper, `TableAlreadyRegistered` (`src/catalog.rs:41`, registration misuse), `VersionedPayloadEncode` (`src/engine.rs:1983`, encode-side, practically unreachable), `MaterializeTableMismatch` (`src/fold.rs:443`, directory supplies wrong table — consumer-bug guard), `SubscriptionRegistryPoisoned` (`src/subscribe.rs:325,344`, lock poisoning), `SubscriptionSink` (`src/engine.rs:1106`, pre-registration sink failure — sink-failure *behavior* is covered by `subscribe_sink_failure_does_not_roll_back_commit`, the typed variant itself is not asserted).

All other variants have witnesses across `tests/tamper.rs`, `tests/engine.rs`, `tests/checkpoint.rs`, `tests/import.rs`, `tests/outbox.rs`, `tests/fold.rs`, `tests/family_identity.rs`, and `tests/seam_gap_falsification.rs`.

## branches
- sema-engine @ versioned-fold head dbe29427d9a2

## testResults
Full `cargo test` green in the worktree: 101 tests across 13 integration binaries, 0 failed — checkpoint 6, dependency_boundary 8, engine 22, family_identity 9, fold 4, import 5, operation_log 7, outbox 6, seam_gap_falsification 6, signal_frame_seam 5, storage_boundary 3, subscriptions 9, tamper 11 (including the two new witnesses: `dead_latest_checkpoint_cursor_is_a_typed_missing_row` ok, `flipped_segment_reference_dangles_at_load_before_verification_runs` ok). Tail of tamper run: "test result: ok. 11 passed; 0 failed; 0 ignored". `cargo clippy --all-targets`: "Finished `dev` profile" with zero warnings. Build clean.
## blockers



### Re-review

VERDICT: approve

## mustFix

## advisory
- The mirror-wedge reproduction instruction in the re-review brief does not map to this branch: the only claimed fixes are the two tamper witnesses, no wedge scenarios or wedge fixes exist anywhere in this repo (grep for 'wedge' over src/ and tests/ is empty), and the mirror actor/transport/server are explicitly outside this crate (INTENT.md:57-58). The wedge proof-reproduction presumably belongs to a different branch in the orchestrator's batch; nothing to reproduce here.
- The 'before verification runs' half of flipped_segment_reference_dangles_at_load_before_verification_runs (tests/tamper.rs:471) is enforced by code order (segment fetch at src/engine.rs:1349-1356 short-circuits before checkpoint.verify() at src/engine.rs:1358), not by the assertion itself: Checkpoint::verify (src/checkpoint.rs:510) would raise the same SegmentMissing{flipped} for a reference with no matching segment, so the test cannot distinguish the load site from the verify site by error value alone. Acceptable as-is; just note the test name's ordering claim rests on the current load-path shape.
- tests/tamper.rs:38-39 duplicates the engine-internal table name __sema_engine_counters and the latest_checkpoint key (mirroring src/engine.rs:37,41). This is the established tamper-suite idiom (CHECKPOINTS / CHECKPOINT_SEGMENTS were already duplicated) and is structurally necessary since no engine path can write engine tables, but a rename in src/engine.rs would silently turn these witnesses vacuous (the doctoring write would land in a dead table). A shared test-support constant or a cross-check that the doctored cursor is actually read back would harden it.
## testHonesty
I re-ran everything myself in /home/li/wt/github.com/LiGoldragon/sema-engine/versioned-fold at head dbe29427d9a2 (working copy on top is empty, so tests ran against the pushed commit). Full `cargo test`: 101 passed / 0 failed across 13 integration binaries, matching the fix agent's per-binary counts exactly — checkpoint 6, dependency_boundary 8, engine 22, family_identity 9, fold 4, import 5, operation_log 7, outbox 6, seam_gap_falsification 6, signal_frame_seam 5, storage_boundary 3, subscriptions 9, tamper 11 — plus 0 unit and 0 doc tests; tamper tail: 'test result: ok. 11 passed; 0 failed; 0 ignored', with both new witnesses individually listed ok (dead_latest_checkpoint_cursor_is_a_typed_missing_row, flipped_segment_reference_dangles_at_load_before_verification_runs). `cargo clippy --all-targets`: grep count of warning/error lines over the full output is 0; 'Finished dev profile'. Witness genuineness verified by source reading, not just green runs: CheckpointRowMissing has exactly one raise site (src/engine.rs:1347) and the new test pins variant plus exact dead sequence (cursor doctored to sequence+7 via the raw storage kernel, tests/tamper.rs:410-430); SegmentMissing at load (src/engine.rs:1354) fires before checkpoint.verify() (src/engine.rs:1358) and the new test pins the flipped digest and excludes both the original and a zeroed digest (tests/tamper.rs:471-503). I confirmed the sites were genuinely unwitnessed at the parent commit: `git grep` at 3593ffe6 shows zero CheckpointRowMissing test references and SegmentMissing witnessed only through the Checkpoint::verify path (src/checkpoint.rs:510). Push verified directly against GitHub: `git ls-remote origin versioned-fold` returns dbe29427d9a2c6c194909385485ad42b008048b8, and jj's remote-tracking bookmark versioned-fold@origin agrees. The mirror-wedge reproduction step was not performed because it has no referent on this branch: no wedge findings were claimed fixed here and no wedge scenarios exist in this crate (mirror transport is out of scope per INTENT.md:57-58); if the orchestrator holds wedge findings against sema-engine specifically, they were not part of this fix round's claims and remain unevaluated by me.

