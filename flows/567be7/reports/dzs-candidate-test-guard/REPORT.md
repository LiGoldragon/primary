# dzs isolated candidate — serialized child-process tests

## Binding

This is a bounded test-only correction to the previously sealed isolated candidate. The clone remains detached at exact base `c537aec8eaf6a4bea34ef022744d1df89283db97`; only `crates/translator/src/bin/belief-pair.rs` is staged.

- Prior candidate blob: `55a97e14059e31297f8cfbd7894ba3a5be8215f7`
- New candidate blob: `44aa10ba2f7a5c79fe078918e9c7489af74ec362`
- New staged tree: `28187743c0d7e8f5876a37912123f0812a03673c`
- Production prefix SHA-256: `8e8f2f6b50cf47bb77c442f4cd254083999cd661e9f07c83160bbaf93d190f65`

A byte comparison of everything before `#[cfg(test)]` in the prior and new candidate blobs passed. Production bytes are unchanged.

## Test-only correction

A private static mutex now serializes every test in this pair binary that can spawn or reap children. Each guard is acquired before any spawn-capable fixture or `run` call. Because it is the first local in each affected test, it is released after later child owners during return and unwinding. Poison recovery permits later tests to retain serialization after an earlier panic.

The exact inventory and coverage argument are in `child-process-test-inventory.md`. No test path capable of spawning or reaping a child remains outside the shared guard.

## Verification state

- `git diff --cached --check`: passed.
- Production-prefix byte comparison: passed.
- Build and tests: deliberately not run.
- Next gate: independent static coverage review, then one revision-bound remote check by another flow.

No commit, push, production edit, deployment, task closure, or bead mutation was made.
