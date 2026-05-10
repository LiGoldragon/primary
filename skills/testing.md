# Skill - Nix-backed testing

*Every test lives in Nix. Constraints become named witnesses, and
the witness is exposed through the component flake.*

## What this skill is for

Use this skill when adding, reviewing, or debugging tests in any
workspace component. It covers the test surface: where tests live,
how they are run, and how stateful or multi-step behavior becomes
inspectable instead of disappearing inside one end-to-end loop.

For the witness catalogue, use `skills/architectural-truth-tests.md`.
This skill answers the runner question: how the witness is made
reproducible through Nix.

## Core rule

**All tests live in Nix.**

That means:

- `nix flake check` is the canonical pure test gate for a repo.
- Pure tests run as `checks.<system>.<name>` or through
  `checks.<system>.default`.
- Stateful tests are still exposed by the flake. If they cannot run
  inside the pure Nix builder, expose a named script or binary through
  `apps.<system>.<name>` or a package output and run it with
  `nix run .#<name>`.
- A recurring manual command is not a test contract until it is a
  versioned script and a named flake output.
- Bare `cargo test`, ad hoc shell commands, and local one-off scripts
  are inner-loop conveniences only. They are not evidence for review.

The point is not to force every stateful experiment into a pure
builder. The point is that the test command, its environment, and its
artifacts are owned by the repo and entered through Nix.

## Constraint to witness to Nix

For every load-bearing behavior or architecture constraint:

1. Name the constraint in plain English.
2. Name the observable witness that proves the intended path happened.
3. Choose the Nix shape: pure check, stateful runner, or chained
   derivations.
4. Expose the shape as a flake output.
5. Name the test after the constraint.

Good test names read like constraints:

- `router_cannot_deliver_without_commit`
- `message_cannot_persist_without_sema`
- `query_cannot_touch_writer_state`
- `handler_cannot_block_mailbox`

If the same visible result can pass through a shortcut, the witness is
not strong enough.

## Pure tests

Pure tests are the default. They run in the Nix build sandbox and are
reachable from `nix flake check`.

Use pure checks for:

- Rust unit, integration, doc, and compile-fail tests.
- Source scans and dependency graph assertions.
- Cargo metadata boundary checks.
- rkyv, NOTA, Signal, and other golden byte or text fixtures.
- Actor topology manifests and actor trace pattern checks that do not
  need a live terminal or host daemon.

Rust tests still follow `skills/rust-discipline.md`: tests live under
`tests/` at the crate root, not in large inline `#[cfg(test)]` blocks.
The Nix check owns the runner.

## Stateful tests

Stateful tests touch a database, terminal, socket, daemon, external
tool, or host-visible harness. They still live in Nix.

Use this shape:

- Put the command in a versioned script or binary owned by the repo.
- Expose it through the flake, normally as `nix run .#test-<name>`.
- Use explicit environment variables and arguments; do not depend on a
  user's home directory, ambient daemon, or untracked local setup.
- Use a fresh state directory unless the point of the test is to read a
  supplied fixture.
- Emit inspectable artifacts: transcript, redb file, actor trace,
  topology manifest, frame bytes, rendered output, or log bundle.
- Prefer a pure check that validates the artifact shape when the live
  run itself cannot happen in the builder.

A stateful test runner that only prints "passed" is weak. It should
leave evidence that another step, tool, or human can inspect.

## Chained tests

Use chained tests when a monolithic end-to-end test could hide a stub,
mock, in-memory shortcut, or unused phase.

The shape is:

1. A first Nix derivation or runner produces an artifact.
2. A second Nix derivation consumes only that artifact and validates it
   with the authoritative reader for that layer.
3. Further derivations repeat the pattern for each real phase.

Examples:

- writer step emits `state.redb`; reader step opens `state.redb` with
  the real Sema/redb reader and asserts typed rows.
- parser step emits `frame.bin`; handler step consumes `frame.bin` and
  emits `reply.bin`; renderer step consumes `reply.bin` and emits
  `output.txt`.
- daemon step emits a shutdown state directory; restart step copies
  that state into a fresh sandbox and proves the next process can read
  it.

The artifact is the boundary. A later step must not share process
memory, mocks, or private helper APIs with the earlier step. If the
writer did not actually write, the reader has nothing to read.

Use lore's `repos/lore/nix/integration-tests.md` for the concrete
chained-derivation pattern.

## Artifact discipline

Artifacts are part of the test design, not leftovers.

- Name artifacts after the constraint or phase they witness.
- Keep them small enough to inspect.
- Prefer stable binary or text formats already owned by the component.
- Do not record raw store hashes in docs; let Nix produce them.
- When a check consumes a previous check's output, reference the flake
  output path instead of copying through an ambient temporary location.
- When copying a store artifact into a writable state directory, set
  writable permissions explicitly.

The test should make the correct path visible and the shortcut path
boring to reject.

## Anti-patterns

- A README command that is not a flake output.
- A recurring debug script that is not versioned.
- `cargo test` as the only claimed verification.
- One huge integration loop that round-trips through the same code and
  exposes no intermediate artifacts.
- Writer and reader using the same mock, cache, or in-memory object.
- A stateful test that depends on an existing home directory, daemon,
  socket path, database, or credential unless that dependency is the
  explicit subject of the test.
- A Nix check that only builds the binary but never executes the
  witness.
- Sleeps or polling used to pretend a push-based event happened. Push
  behavior needs a pushed witness.
- An ignored test without a tracked reason.

## Review checklist

Ask these before accepting a test:

- Can a clean checkout run the canonical suite with `nix flake check`?
- If the test is stateful, is the stateful command exposed through
  `nix run .#<name>` or another named flake output?
- Does each load-bearing constraint have a named witness?
- Does the witness prove the intended component or phase was used?
- Are intermediate artifacts inspectable?
- Would a shortcut, stub, or bypass fail?
- Is the test name the constraint it protects?

## See also

- `skills/nix-discipline.md` - Nix command and flake discipline.
- `skills/architectural-truth-tests.md` - witness catalogue and
  architecture-test patterns.
- `skills/rust-discipline.md` - Rust test layout and crate rules.
- `skills/actor-systems.md` - actor traces and topology tests.
- `skills/push-not-pull.md` - pushed observation tests.
- `repos/lore/nix/integration-tests.md` - chained Nix derivations.
- `repos/lore/rust/testing.md` - Rust testing reference.
