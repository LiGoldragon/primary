# Operator Report 332 - Message/Router/Harness E2E And Pi Interface

## Result

The real cross-process message route now has a harness-side e2e witness in
`harness`:

`message` CLI -> `message-daemon` -> `router-daemon` -> `harness-daemon`
configured as `HarnessKind::Pi` -> terminal acceptance socket.

The test is
`/git/github.com/LiGoldragon/harness/tests/message_router_harness_e2e.rs`.
It builds the real external `message` and `router` binaries, starts all three
daemons with one typed configuration argument each, sends:

`message "(Send operator [full route to pi harness])"`

and asserts both:

- the CLI receives `SubmissionAccepted { message_slot: 1 }`;
- the terminal adapter receives bytes containing `full route to pi harness`.

This is not an in-process router unit test and not a terminal-cell smoke. It is
the real Persona message ingress path through live Unix sockets and real
length-prefixed Signal frames, with a fake terminal endpoint only at the final
terminal adapter boundary.

## Pi Interface Situation

`persona-pi` does not currently expose a built Persona message-ingress daemon
or signal contract. In this checkout it is a Nix packaging/concept surface for
the upstream Pi harness, not a runtime component with its own socket.

The built Persona interface that can take routed messages is `harness` through
`signal-harness::MessageDelivery`. `HarnessKind::Pi` is the typed way to say the
target harness is Pi. That means terminal-cell is not the message ingress for
Pi. Terminal-cell is only needed when today's implementation has to drive an
interactive terminal-backed Pi session. A future Pi adapter can replace the
terminal endpoint inside `harness` without changing the upstream message/router
ingress shape.

## Stack Defect Found

The first e2e run failed before daemon startup because `harness/Cargo.lock`
still resolved `signal-frame` to old main commit `2313c5ed`, while
`triad-runtime` now needs current `signal-frame` short-header exports. Updating
the lock to current signal-frame main `6f5a77f1` fixed the build. No
`triad-runtime` or `signal-frame` source change was needed.

That was a real production-readiness finding: cross-repo e2e caught a stale
engine-stack lock that individual repo tests did not catch.

## Verification

Ran in `/git/github.com/LiGoldragon/harness`:

- `cargo test --test message_router_harness_e2e -- --nocapture` - passed.
- `cargo test` - passed, including the new e2e.
- `cargo clippy --all-targets --all-features -- -D warnings` - passed after
  fixing the crate lint priority and an existing `&PathBuf` test-helper lint.

## Remaining Production Notes

This proves the current message/router/harness process path is usable. It does
not prove a direct Pi API adapter yet, because no such Persona-facing Pi adapter
is built in `persona-pi`. It also does not prove terminal-cell itself; the final
terminal boundary is intentionally a signal-terminal acceptance fixture so the
test isolates the message-passing engine path from interactive terminal
flakiness.
