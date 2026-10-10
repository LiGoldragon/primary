# Operator 322 — frame and method

## Prompt frame

The psyche's correction was that the schema-derived engine stack must be made
properly, not merely partially improved:

- `schema-rust-next` runtime emission still carrying string-format code is debt
  and is moving toward Rust-native typed/token lowering.
- `spirit` must be the copyable contract/daemon/engine-stack exemplar, not an
  all-in-one pilot future components are told not to copy.
- The operator should use subagents liberally, investigate the alleged gaps, and
  implement whatever is clearly deficient.

Durable intent was captured earlier in Spirit as:

- `0bw0`: High-certainty correction that the runtime string emitter is wrong and
  the stack is moving toward a Rust-native typed/token lowering style.
- `y88n`: High-certainty correction that `spirit` is the proper exemplar, not a
  non-copyable all-in-one exception.

## Method

The work was split into four operator tracks:

1. Complete the schema-derived streaming substrate started earlier: stream
   metadata in `schema-next`, reusable subscription runtime in `triad-runtime`,
   and schema-driven emission in `schema-rust-next`.
2. Continue the Rust-native emission migration in `schema-rust-next` by
   tokenizing another runtime-adjacent emitter slice.
3. Clean dependency drift exposed while updating Spirit's stack pins.
4. Make Spirit's production-style proof real by regenerating from the new
   emitter, running the process-boundary and Nix-built binary tests, and fixing
   the Nix packaging defect that made cache misses fall back to network access
   inside Cargo.

## Subagents

Two operator subagents were dispatched.

Hume completed a runtime-emitter audit and ranked the remaining string-based
emitter clusters in `schema-rust-next`. Its most useful recommendation was to
start with trace object-name emission because it was small, local, fixture-heavy,
and adjacent to runtime proof. That slice was implemented.

Peirce was dispatched to audit Spirit exemplar status but was shut down before a
usable result. The main operator thread completed the Spirit verification
directly.

## Report map

- `1-subagent-runtime-emitter-audit.md`: Hume's audit distilled into
  implementation order.
- `2-implementation.md`: code landed across the touched repos.
- `3-verification.md`: commands and test results.
- `4-overview.md`: operator synthesis, current state, and remaining hard work.
