# Bounded validation spelling/source check

Checked proposal `flows/4f3cb8/reports/052-policy-validation.md` against clean `flow-config-d05351-independent` at `916b54574a...` and sibling `protos`/`datom-codec` worktrees. This is source observation, not approval of the proposal.

## Measured source pins

- Protos structural reader budget is `usize`: `protos/src/core.rs:83-96` (`ReaderBudget { remaining: usize }`); reader depth is also `usize` and fixed `MAXIMUM_READER_DEPTH: usize = 256` at `protos/src/core.rs:250-254`. The reader spends the budget at `core.rs:291-309`.
- Datom `Integer` is `i64`: `datom-codec/src/lib.rs:29`. Datom `Budget.remaining`, `depth`, and `maximum_depth` are `Integer` (`datom-codec/src/core.rs:24-31`), and composition checks `depth >= maximum_depth` (`core.rs:53-64`). This matches the proposal's separate Datom-counter row; Protos structural counters are separately `usize`.
- Datom form-building depth is an `Integer` (`datom-codec/src/composition.rs:13-16`) with retained fixed `MAXIMUM_FORMING_DEPTH: Integer = 4_096` (`:15` and check at `:31-37`). This is an observed source bound; the approved codec-boundary destination supplies the replacement configurable cap.
- Existing native Herdr session-name validator is in `flow-nexus/src/composition.rs:300-306`: nonempty and rejects `\r`/`\n` (`InvalidHerdrSessionName`). The updated proposal additionally requires NUL rejection; that is supplied destination behavior, not observed in this HEAD.
- Native fixed limits and units: `composition.rs:181-183` sets Herdr request line `usize = 1 MiB`, envelope allowance `usize = 1024`, and Codex text limit `usize = 1 << 20` characters. `FitsOneMessage` compares Claude encoded byte length plus allowance to request bytes, but Codex `text.chars().count()` to character limit (`:198-204`). The proposal's byte/character separation matches observed code.
- Curriculum exchange uses a `u32` length prefix and converts received prefix to `usize`: `flow-nexus/src/context.rs:118-149`; request conversion is checked with `u32::try_from`. The answer has an independent fixed `ANSWER_FRAME_LIMIT: usize = 64*1024*1024` (`:50-52`, check `:140-142`).
- Existing pane count types are `usize`: `herdr/pane.rs:51-54` (`SUBMISSION_READS`, `INTERRUPT_PRESSES`); retraction count is `usize` (`:392-393`). Existing native durations are `std::time::Duration`, e.g. submission spacing (`pane.rs:52`), title readback interval (`herdr/launch.rs:1447-1453`), and exchange timeout (`context.rs:50`).
- Retry waits are native `Duration`: `send_tool.rs:539-540` (`FIRST_WAIT`, `LONGEST_WAIT`), with checked `Instant::checked_duration_since` at `:545-549`; current multiplier behavior is described as doubling, but no configurable multiplier declaration exists in this HEAD.

## Remaining source distinctions

- The observed Protos fixed reader depth (`256`) and Datom form-building depth (`4096`) are source facts. Per the approved codec-boundary destination, these are replaced by the supplied configurable caps; they are not retained invariants.
- Herdr's observed check is nonempty plus CR/LF. The approved destination adds NUL rejection and the stated session-name spelling; this HEAD cannot witness that addition.
- Herdr request/Codex text limits are native retained constraints with distinct byte/character units. Curriculum's observed 64 MiB answer cap is a current source value; the approved destination chooses the policy-owned family treatment rather than treating it as an unchangeable invariant.
- Existing constants use native `Duration`; no RuntimePolicy declarations exist before bodies. The checked milliseconds-to-`Duration` construction is therefore a prebody acceptance gate, not a missing source declaration.

No RuntimePolicy leaf declarations or generated validation result are expected in this prebody source snapshot; their absence is not an audit finding.
