# Child-process test inventory

The test module contains eight tests.

## Child-spawning or child-reaping tests — guarded

Each test below acquires `child_process_test_guard()` as its first local, before any fixture or call capable of spawning a child. The guard therefore outlives later child owners during ordinary return and stack unwinding.

1. `first_owned_terminal_status_relinquishes_only_that_child`
   - Spawns `true` and `sleep` through `ChildFixture` in both owner orderings.
   - Calls the real `waitpid(-1)` path through `wait_for_first_terminal`.
   - Drops the surviving owned child before releasing the guard.
2. `nonterminal_statuses_retain_both_owned_children`
   - Spawns two `sleep` children through `ChildFixture`.
   - Exercises the direct status classifier.
   - `PairedChildren::drop` terminates and reaps both before the guard is released.
3. `unexpected_terminal_pid_is_typed_and_never_classified_as_owned`
   - Spawns two `sleep` children through `ChildFixture`.
   - Exercises the direct unexpected-terminal classifier.
   - `PairedChildren::drop` terminates and reaps both before the guard is released.
4. `reachable_post_spawn_failures_return_through_the_pair_owner`
   - Holds the guard across all three `run` calls.
   - Covers owner rejection (no child reached), second-spawn failure after the first child exists, and a post-spawn transport failure with both children owned.
   - All cleanup/reap completes inside `run` or its owner drop before the guard is released.

The shared static mutex is private to this test binary. Poison recovery preserves serialization after a prior test unwind.

## Tests with no child spawn or reap

- `legacy_only_memory_is_migrated_to_the_current_path`
- `current_only_memory_is_used_without_change`
- `current_and_legacy_memory_are_a_typed_conflict_naming_both_paths`
- `fresh_memory_selects_the_current_path_without_creating_it`

## Source inventory

The only test-side `Command::new(...).spawn()` expressions are the two `ChildFixture` methods. Their call sites are confined to the first three guarded tests. The remaining process creation is production `run`, whose only test call site is the fourth guarded test.
