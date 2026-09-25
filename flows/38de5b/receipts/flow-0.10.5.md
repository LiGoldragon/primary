# Flow 0.10.5: one home for predecessor and remembered, pruned launch copies, 16-hex launch names

An Opus subflow of 38de5b did this on 2026-09-25. It closes the three leftovers listed in `flow-0.10.4.md`.

- Repository: github.com/LiGoldragon/flow. The work was done in a fresh scratchpad clone (`flow-prune-38de5b-k3`) based on 84e2304 (0.10.4).
- Pushed to main: 5e1382f2a13731122838a32d9303b497cecec6e5 "Flow 0.10.5: one home for predecessor and remembered, pruned launch copies, 16-hex launch names". `git ls-remote origin main` returned 5e1382f.
- Tests: 103 before (92+6+3+1+1) and 105 after (94+6+3+1+1), with 0 failed. `cargo clippy --all-targets` gives 0 warnings, and `cargo fmt --check` is clean. `nix flake check` was not run.
- Version: this is a patch. It does not change the wire, the storage or the argv shape. Only the argv value (the remote-control name) and the Codex prompt text change. Cargo.toml, Cargo.lock, flake.nix, UPGRADES.md and README.md were updated.
- Orchestrate lock 6497 was taken and released.

## What changed

1. **One home per meaning.** Codex's `# Flow launch` record no longer carries `Predecessor:` or `Remembered flows: id@depth`. They now appear only in the bundle text's trailing section, which opens the same block. The remembering depth no longer reaches Codex, because the section lists IDs only, as the 0.10.4 brief set.
2. **Pruning.** The composer gets `LaunchBundles::remove_for_request(id)`, which ignores NotFound. The store gets `ReadsLaunchAttempt::launch_requests_bound_to(flow_id)`, which scans the attempts' native bindings. `RunningNexus` gets the trait `PrunesLaunchBundles`, whose hooks are:
   - `settle`, when a reserved launch's StartRejected or ReplaceRejected outcome has been stored. LaunchRequestConflict is excluded because its copy belongs to the other request.
   - `Query::Stop`, after `record_stopped`.
   - `reap`, once the predecessor's pane has been closed or confirmed absent.

   Pruning at Started or Replaced was deliberately left out. The running Claude was given the copy as `--system-prompt-file` and told to `Read` it, and the receipt can arrive before that Read. The copy therefore lives until its Flow is stopped.
3. **Collision.** `SHORT_FORM_LENGTH` is now 16, still taken from SHA-256 of `flow-remote-control-v1\0<id>`. `ShortensLaunchRequest` is now also implemented for `str`, so an ID alone gives the copy's path. The remote-control name is `flow-<16hex>` and the copy is `launch-<16hex>.md`.

## Fixtures

- `launches_with_distinct_request_ids_never_share_a_name_or_a_copy` uses `launch-4646` and `launch-72333`. These are a real pair whose first 8 hex are the same (0ed0b35c), found offline. The test checks that the pair now gets distinct names and distinct copies, and that 20,000 IDs produce no shared name or file.
- `stop_removes_the_bundle_copy_of_the_launch_that_bound_the_flow` checks that the bound copy is removed and a sibling copy is kept.
- `launch_status_answers_pending_and_every_outcome_once` now also checks that the copies of the refused Claude Start and the refused Replace are gone.
- `replace_stops_the_predecessor_before_the_successor_is_routable` now also checks that the Started successor's copy survives Replaced.
- The Codex expected-block test now asserts that `Predecessor`, `Remembered`, `1b8ac0` and `836818` each appear once.
- The long-hex guard now removes the known 16-hex short form before it looks for runs of 16 or more.
- Mutation check: with removal disabled, the Stop fixture and the launch-status fixture both fail.

## Open, and not witnessed

- There has been no live Start or Stop.
- Copies that 0.10.4 wrote under 8-hex names are never pruned. UPGRADES.md says to remove them by hand.
- A copy written by compose is left orphaned when its reservation then fails with a store error (the unreserved rejection). It is not pruned because the outcome was never stored.
