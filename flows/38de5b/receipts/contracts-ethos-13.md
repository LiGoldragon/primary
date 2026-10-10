# Contracts repinned to ethos-zero 13.0.0

Subflow of 38de5b (Fable), 2026-09-25. Both contract repos now pin ethos-zero 13.0.0 at 407f938d083a89236ef8c2c6e8a90561ec6b637a. Each was a fresh clone in the scratchpad (`signal-flow-e13-fable`, `meta-signal-flow-e13-fable`) under Orchestrate locks 6452 and 6453, both released. Generation used an ethos-zero binary built from 407f938 with `cargo install --rev` into the scratchpad's `ez13-fable`. Every push was confirmed with `git ls-remote`.

| repo | from | to | version | regeneration | `cargo test --features datom` |
|---|---|---|---|---|---|
| signal-flow | 5ca97ce | **83171f3f39f53fbcff1a5fdc9bc7c96d6f57ac1f** | 4.0.0 -> 4.0.1 | changed, as expected | 9 passed |
| meta-signal-flow | f715883 | **29ec97d854acfc08ff1aba2813cd0957174901b1** | 6.0.1 -> 6.0.2 | byte-identical | 5 passed |

## signal-flow

- The build-dependency ethos-zero moved from 4bf73ca (10.0.0) to 407f938 (13.0.0). Cargo.lock followed.
- The regenerated `src/generated/signal.rs` has 15 diff lines, as the fixes 5-6-7 receipt predicted:
  - six fields change from `Option<…>` to `std::option::Option<…>`. One is `LaunchProfile.flow_id_option`; the other five are the `LaunchAttempt` `*_option` fields;
  - `EndpointSelection` gains `#[rustfmt::skip]`.
- The build.rs freshness assert passes. The test build ran it.
- Versioning rule: the generated text changed, but every type, field and variant is the same, so the rkyv and datom wire is unchanged. That makes this a **patch**.
- Transitively, `signal` still pins ethos-zero 9.0.0 (b232d35). That pin was not touched.

## meta-signal-flow

- ethos-zero now pins 407f938, and signal-flow now pins 83171f3 (4.0.1). The signal-flow pin was changed in both the dependency and the build-dependency.
- The regenerated `src/generated/signal.rs` is byte-identical (`cmp`). The build.rs assert passes.
- The version is a patch, 6.0.2: only dependency pins changed, and the wire is unchanged.

## Notes

- ethos-zero main has moved past 407f938 to 2a39e50 ("Describe the generated _Data struct in place of the tuple variant"). Its Cargo version is still 13.0.0. As the brief asked, both contracts were pinned to 407f938.
- The flow repo was not touched. Flow can now repin signal-flow to 83171f3 and meta-signal-flow to 29ec97d.
