# Independent Flow LaunchProfile fixture repair

The independent repair is commit `d4107dd25ed740e08bd8458a3daceff06d8b44a8` on remote branch `mind-astra-independent-fixture-repair-f5a74e`. It changes only `crates/flow-nexus/src/herdr/launch.rs` and `crates/flow-nexus/src/lib.rs`.

## Independence

I selected `aba7467592088242a15258abc751c89bb52d4c2c` as the pre-repair base from history metadata: it is the parent of the separately described fixture-repair commit `2586ea19bf8e`, which is a parent of the requested comparison revision `0086947718c8711a5fdcbbd9d50b5cc2eb5b5036`. I did not inspect that repair, the comparison revision's fix, or Mind Sol's patch before committing `d4107dd2`.

On the base, `cargo test -p flow-nexus --lib` found three failures: the Claude launch assertion omitted the new `--system-prompt-file` arguments, and the two durable-launch fixtures supplied `/tmp/flow-system-prompt.md` without creating it. The repair makes the launch assertion include that argument pair and creates a fixture-local regular bundle for each durable-launch profile.

## Validation

`cargo test -p flow-nexus --lib` passed after the repair: 56 passed, 0 failed.

`cargo fmt --check` was unavailable as a passing gate because the pre-existing base already differs from formatter output in `crates/flow-nexus/src/composition.rs` and an unrelated existing line in `crates/flow-nexus/src/herdr/launch.rs`; the repair did not apply those unrelated formatting changes.

The branch was pushed to `origin` and then fetched; its remote bookmark resolves to `d4107dd25ed740e08bd8458a3daceff06d8b44a8`.

## Comparison after recording

After committing, comparison with `0086947718c8711a5fdcbbd9d50b5cc2eb5b5036` found agreement on the Claude assertion. Both repairs create a fixture-local bundle before the two durable-launch profiles. The difference is representational only: main names it `bundle_path`, writes `fixture bundle\n`, and uses `to_string_lossy().into_owned()`; this repair names it `system_prompt_bundle`, writes `fixture system prompt\n`, and uses `display().to_string()`. Each resulting path is an absolute UTF-8 temporary-directory path in these tests. The comparison revision contains the expected changes in `composition.rs` from its preceding bundle-validation work; this repair intentionally leaves that already-valid fixture untouched.

## Recall provenance

Depth-one remembrance of `26c50c` was limited to its own directory, without ancestry traversal. `flows/26c50c` contains only `vision/curriculum.md`, `vision/ethos.md`, and `vision/operational-releaseContribution.md`; it has no `records/`, `log.md`, or `reports/` files. A last model response was unavailable, as previously reported. The relayed instruction appears in `flows/f5a74e/log.md` and is machine-attributed rather than directly witnessed living speech.

Sources: `flows/f5a74e/log.md`; `flows/26c50c/`; Flow history metadata at `aba7467592088242a15258abc751c89bb52d4c2c`, `2586ea19bf8e`, and `0086947718c8711a5fdcbbd9d50b5cc2eb5b5036`; independent branch commit `d4107dd25ed740e08bd8458a3daceff06d8b44a8`; local `cargo test -p flow-nexus --lib` and `cargo fmt --check` output.
