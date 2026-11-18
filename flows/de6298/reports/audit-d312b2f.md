# Audit: Codex Harness Nexus, branch daemon at d312b2f

## Verdict: fail

Two defects stop a pass.

1. A reading can commit the same rows twice. A Reading carries an offset taken outside the serial lock. Startup runs on the main or meta thread while the watch thread reads, so a stale offset gets folded, and the fold accepts it. A probe confirmed the double commit (F1).
2. The Ethos rule is broken widely. About 23 traits and 7 data types are declared by hand in Rust, outside any Ethos file (F2).

Everything else is a named gap. Most of the design is met:

- the atomic commit of a batch together with its offset;
- publishing only after that commit;
- the repeated TurnEnded dropped;
- typed Malformed rows;
- the ClaimIdentity emission;
- one Set variant per value, with no Set.Hooks;
- the awaited and refused sessions directories;
- typed lane failures;
- no polling or timers in the candidate's own code.

All eight files under `src/generated/` match ethos-zero output; the `generated` check passes.

Paths below are relative to the candidate worktree (codex-harness-nexus at d312b2f), unless a repository is named.

## How this was judged

- I read all of the candidate's code, the three contracts (signal 0.3.0 at 68dafec, meta 0.4.0 at b6039b7, harness-nexus-library at 3613d63), the notions and the vision.
- I built these checks on the builder, all green: generated, fmt, codex-harness-nexus, codex-harness-nexus-daemon, codex-harness-translator, and codex-harness-nexus-tests at 697cb79.
- The suite ran once fresh, with my probes added in a scratch worktree of the tests repository: nexus 18/18 (14 original plus 4 probes), pair 12/12, transitions 2/2. The daemon's own tests passed: lane_failure 5/5 and bootstrap_order 2/2.
- I read the author's handover only after these findings were written. The comparison is at the end.

The four probes, appended to `tests/nexus.rs` in that scratch worktree (kept as the patch /tmp/claude-1001/-home-li-primary/621d1fa3-67d9-525e-bb6c-779712f10557/scratchpad/audit.S4KD/audit-probes.patch):

- `audit_a_reading_from_a_look_taken_before_another_reading_reads_its_rows_twice`: passed, which confirms F1.
- `audit_a_restarted_nexus_reads_only_the_rows_written_while_it_was_down`: passed. Restart recovery from the stored offset works.
- `audit_a_known_row_with_a_field_of_the_wrong_type_is_malformed`: passed. A wrong-type field becomes InvalidField, as ruling 3 asks.
- `audit_a_hook_path_that_exists_already_stays_pending_until_its_next_write`: passed, which confirms F6.

## Findings

### F1. A stale Reading commits rows twice (high; observed by probe, the thread interleaving inferred)

- `crates/codex-harness-nexus/src/watching.rs:442-456` (`startup`) and `:460-478` (`woken`) read every record outside the serial lock. Each builds `Operation::Reading(watch)` with the offset as it stood then.
- `crates/codex-harness-nexus/src/nexus.rs:169-192`: the Reading attempt emits `ReadRollout` with that caller-supplied watch. It never compares the offset against the Memory's current one.
- `crates/codex-harness-nexus/src/folded.rs:271-279`: the only guard, `OffsetReversed`, compares the read's *end* offset with the stored offset. A read that starts behind the stored offset but ends at or past it is accepted.
- Callers on different threads:
  - `crates/codex-harness-nexus-daemon/src/serving.rs:137-138`: `follow_watch` starts the watch thread before `open()`.
  - `crates/codex-harness-nexus-daemon/src/waking.rs:90-94`: `open()` sets `opened`, which lets the watch thread read, before it takes the startup snapshot.
  - `waking.rs:100-101`: `configured()` runs `startup()` on a meta connection task.
  - `nexus.rs:300-301`: the read right after an attachment starts at offset 0, outside the lock.
- Evidence: in the probe, a startup look was taken, rows were appended, the watch's own Reading advanced the offset, then the startup look's Reading was performed. It returned the same two transitions again, `[TurnEnded Rested, PromptSubmitted Working]`, and committed and published them. The repeated-TurnEnded drop does not catch this, because the state is Working again by then.
- Effect: duplicate events reach the Flow Nexus, state transitions replay, and malformed records are asserted twice.
- Hypothesis: the window opens at every daemon start, and at every SessionsDirectories set, while a Codex session is writing.
- Fix: the Reading should take its offset from Memory under the serial lock, or the fold should refuse a read whose start offset differs from the stored one.

### F2. Types and traits declared outside Ethos (high, against vision ethos/0, nexus/0 and ruling 4)

Ruling 4 allows hand-written runtime structs to hold native handles. It asks that their capabilities be Ethos-declared traits.

Hand-declared traits:

- core: `Diagnosing` (`diagnosing.rs:5`), `Familial` and `Opening` (`store.rs:46`, `:89`), `ConfigurationReading` and `Locking` (`nexus.rs:60`, `:76`), and `Placing`, `Channelled`, `Replacing`, `Settling`, `Watching` (`watching.rs:83`, `:139`, `:159`, `:223`, `:364`);
- translator: `ReadingRows` (`crates/codex-harness-translator/src/emitting.rs:81`), and `Limiting`, `MetaBudgeting`, `BudgetMerging`, `TextBudgetSetting`, `SettingsReading` (`translating.rs:55`, `:69`, `:89`, `:106`, `:140`);
- daemon: `Answered` and `Carrying` (`emitting.rs:27`, `:71`), `StandardInputReading` (`bootstrap.rs:6`), `DaemonStarting` (`serving.rs:63`), and `ReadyOpening`, `WatchFollowing`, `Supervising` (`waking.rs:21`, `:31`, `:44`).

Hand-written data types that hold no native handle:

- `WatchWord` (with a bare `u64` generation), `Placement`, `Reach` and `Followed` (`watching.rs:30-81`);
- `ListenerFailure` (`serving.rs:83`), an error type outside the vocabulary;
- `TranslatorSettings` (`translating.rs:22`);
- `type Error = &'static str` (`translating.rs:43`).

The structs that do hold handles are within the ruling: Store, HarnessNexus, DirectoryWatch, SessionsWatch, Serving, Daemon, PairedTranslator, CodexHarnessTranslator.

### F3. FindRollout is a stub, and ThreadDatabases is required but never read (medium)

- `crates/codex-harness-translator/src/emitting.rs:94-100` always answers `Unfound`. The notion says the path is read from Codex's own record of its threads.
- `nexus.rs:52` makes `thread_databases` a condition of readiness. No other code reads it.
- So a configured value is mandatory but has no effect, and a session with no hook path falls through to the session_meta first-row search on every unknown write.

### F4. A pending path outside the configured sessions directories is never attached while the daemon runs (medium; inferred)

- `nexus.rs:137-138` records `Rollout::Pending(path)` for any hook path.
- Attachment comes only from `woken` (`watching.rs:460-478`). That is fed by `written` (`watching.rs:334-350`), which reports only paths inside an arrived sessions directory.
- No watch is placed on the pending path itself or on its parent. Such a path attaches only through `startup` at the next start, arrival or SessionsDirectories set.
- Ruling 5 asks for attachment on a created or written event at exactly that path.

### F5. Pending paths are matched by exact string (low; hypothesis)

- `nexus.rs:216-221` matches the hook's path against the notify path, which is built from the configured directory string.
- A sessions directory reached through a symlink, or written in a different spelling, would leave the session Pending forever. A Pending session is also excluded from session_meta matching (`nexus.rs:228`).

### F6. A hook path that already exists waits for the next write (low; observed by probe)

- `nexus.rs:137-138` registers Pending even when the file is there. Rows already in the file are read only at the session's next write, or at startup.
- A session that goes idle right after it starts is not read.

### F7. A SessionStart without a path overwrites an earlier pending path (low; inferred)

- `nexus.rs:128-153`: for a known record whose rollout is `Pending(p)`, a later SessionStart naming no path emits FindRollout. That answers `Unfound`, which writes `Rollout::Unlocated` and loses `p`.

### F8. Typed failures are flattened into text or the wrong variant (medium, against "errors are typed vocabulary")

- `nexus.rs:243-249`: every FoldRefusal except Unregistered becomes `Unrecorded(Diagnostic(format!("{refusal:?}")))`.
- `nexus.rs:193-195`: a rollout the translator could not read is reported as `ReportFailure::Unrecorded`. That variant means a Memory failure; the contract at 68dafec has no variant for an unreadable rollout.
- `nexus.rs:177-180`: a Reading for an unknown flow becomes a formatted string.
- `nexus.rs:349`: a Publisher create error is mapped to `Unconfigured`.
- `watching.rs:410-419`: an UnwatchableDirectory is formatted into a string.
- `store.rs:135-138`, `:182-185`: Memory faults are formatted strings.

### F9. A recorded directory that fails at start goes silent, and the readout says nothing is awaited (medium)

- `waking.rs:110-126` and `serving.rs:132-136`: if the recorded sessions directories cannot be watched at start, the failure only reaches stderr. The daemon still opens.
- `watching.rs:216-220`: `awaited()` answers `[]` when there is no current watch. The readout then reports nothing awaited while nothing is watched.
- Failures while settling the watch also only reach stderr (`waking.rs:134-136`).

### F10. Translator row reading (low)

- `crates/codex-harness-translator/src/emitting.rs:165`: `String::from_utf8_lossy` replaces invalid UTF-8. A row with invalid bytes inside a JSON string parses as valid with U+FFFD, and is not recorded as Malformed.
- `emitting.rs:199-205`: a rollout shorter than its stored offset (truncated or replaced) is refused as `Unreadable` at every later write. The watch never recovers.
- `rollout.rs:28-31`: the outer `type` (`event_msg`) is not checked. Any row kind whose payload.type is one of the four known names would be read as an event. This is a hypothesis; I know of no such row in Codex today.
- `emitting.rs:134-143`: the flow id is accepted as any non-empty hex string, of any length.

### F11. Literals in code (low)

- `store.rs:20-24`, `:54-55`, `:64-65`, `:74-75`: table, family and schema-label strings.
  - The configuration's schema label reads `-v2` while its table and `SCHEMA_VERSION` read v1. That suggests a format change made without an upgrade step. Unknown whether an older Memory still opens.
- `crates/codex-harness-translator/src/emitting.rs:104-108`: the identity producer's argv `codex`, `--flows-root` and the environment variable `CODEX_SESSION_ID`. The translator is where these words belong, but the call is not a typed Command value.
- `flake.nix` pairing block: frame deadline, frame capacity, retry delay and text limits are Nix literals.
  - The translator's text budget is held in memory only (`translating.rs:35-50`). It resets to the literal at every restart and is not kept in Memory.

### F12. Two revisions of the same shared repositories are pinned (low)

- `Cargo.toml`: `nexus` at d020a62 beside `nexus-exchange` and `nexus-serving` at a4bc011; `shared-translator` (translator 0.5.2) at 29601a3 beside `translator-client` and `translator-serving` at 2739d58.
- It compiles. But the shared layer comes from two points in each repository's history, not only the a4bc011 and 2739d58 named in the brief.

### F13. Mutex poisoning is swallowed (low)

- `nexus.rs:76-84`: `Locking` takes the guard back from a poisoned mutex. A panic halfway through moving the watch would leave the SessionsWatch placements and the watched set disagreeing, silently.

## The tests: what they prove and what they do not

Proven:

- typed refusals: unconfigured, unregistered, identity refused, invalid settings, text budget;
- an incomplete last line waits, and a second TurnEnded is dropped;
- an InvalidJson row is recorded and read past;
- session_meta matching for an unlocated session;
- the subscriber's snapshot and its following changes;
- the nested, awaited, removed and remade sessions directories;
- the lane-failure classification and its two outcomes (daemon `tests/lane_failure.rs`);
- the pair's readiness, refusals, meta streaming and SIGTERM handling.

Not proven:

- `the_memory_outlives_the_process` (tests `nexus.rs:502`) only compares the record after reopening. It never reads rows written while the Nexus was down. My restart probe shows that works, but the suite does not test it.
- The pair tests place each rollout whole, by rename (tests `pair.rs:190-194`). No end-to-end test appends to a live file, restarts the daemon, or overlaps startup with watch-thread reads, which is where F1 lives.
- No test covers ruling 3's wrong-type field (my probe does), atomicity under a failed commit, publishing withheld after a failed commit, a pending path outside the sessions directories, or a hook path through a symlink.

## Shared layer, out of the candidate's scope

`nexus` at a4bc011, `crates/exchange/src/exchange.rs:188-201`: a listener's accept is retried after a delay when descriptors run out. That is a timer in the shared layer, configured by the `retryDelayMilliseconds` the flake passes in.

## Compared with the author's handover (flows/de6298/handover.md)

The handover names four gaps:

- A sessions directory created but unwatchable stays awaited, with its failure on stderr only. This agrees with F9, which also covers the start case and the false empty readout.
- A move of a watched directory's ancestor goes undetected. I did not reach this independently. I accept it as stated, with notify keeping the moved inode's watch under the old path names.
- An Unlocated session's rollout is found at its next write. This agrees with F6.
- Configured does not name awaited directories. Not separately found.

Not named in the handover: F1, F2, F3, F4, F5, F7, F8, F10, F11 and F12.
