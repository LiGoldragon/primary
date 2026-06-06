# Operator Report 331 — Message / Router / Terminal Engine Port And E2E Start

## Scope

The request was to port the new engine crates across the message-passing
engine surface and start e2e testing. I treated the current surface as:

- `message`
- `router`
- `terminal` (`terminal-control` in earlier wording)

The work landed on main in all three code repos.

## Landed Changes

`message` commit `11f4626` (`message: move CLI onto generated daemon wire`)
moves the CLI off the old daemon-side `signal-message` request path. The CLI
now projects its user NOTA records into `message::schema::signal::Input`,
writes the generated signal frame through `triad-runtime::LengthPrefixedCodec`,
reads `message::schema::signal::Output`, and renders the CLI output at the
edge. A new `src/client.rs` owns that working-socket client so `router.rs`
stays the outbound router-forwarding adapter only.

`router` commit `befff26` (`router: add generated triad schema substrate`)
adds `schema-rust-next` build wiring, `triad-runtime`-compatible generated
modules, and checked-in `schema/signal.schema`, `schema/nexus.schema`, and
`schema/sema.schema`. The generated Nexus schema names the intended internal
features: signal arrival, SEMA writes/reads, delivery effects, and mind
adjudication requests. The generated two-listener daemon spine is present but
not the active `router-daemon` behavior path yet.

`terminal` commit `5b7bb0d` (`terminal: add generated triad schema substrate`)
adds the same generated substrate for terminal. The generated signal schema
names session reads/control, including `WriteInjectionRequest` with an
`injection_sequence`. The generated Nexus schema names session lifecycle,
terminal-cell commands, and event publication; SEMA names registry, prompt,
lease, injection, and transcript records. The active behavior path is still the
transitional supervisor/one-cell runtime.

## E2E Testing Started

I added and ran a real process-boundary witness in `message`:

- `cargo test cli_send_crosses_generated_daemon_socket_and_forwards_to_router --test process_boundary`

That test starts the real `message` CLI, the real generated `message-daemon`,
and a stub router socket. It proves CLI NOTA input crosses the generated daemon
wire, Nexus runs, the router effect executes, and the CLI renders the accepted
reply.

I also reran focused socket-boundary witnesses in `router`:

- `cargo test --test observation_truth router_daemon_connection_routes_router_frame_to_observation_plane`
- `cargo test --test observation_truth meta_grant_installs_channel_visible_to_working_observation`

These prove the current router daemon socket and meta-policy socket paths still
work after the generated substrate landed.

And focused terminal socket-boundary witnesses:

- `cargo test --test terminal_signal_cli terminal_signal_cli_connect_crosses_socket_signal_frame`
- `cargo test --test terminal_supervisor terminal_supervisor_subscription_streams_initial_state_then_delta`

These prove the current terminal signal CLI and supervisor streaming paths
still work after the generated substrate landed.

## Full Verification

Before pushing:

- `message`: `cargo test`, `cargo test --all-features`, and
  `cargo clippy --all-targets --all-features -- -D warnings`.
- `router`: `cargo test` and
  `cargo clippy --all-targets --all-features -- -D warnings`.
- `terminal`: `cargo test` and
  `cargo clippy --all-targets --all-features -- -D warnings`.

## Important Remaining Work

The full real-daemon chain is not done. The next witness should be:

`message CLI -> generated message-daemon -> real router-daemon -> terminal supervisor / terminal-daemon harness endpoint`

The reason I did not claim that as complete is architectural, not test
avoidance:

- `message` is live on the generated daemon wire.
- `router` now has generated schemas and a generated daemon spine, but the live
  daemon behavior still runs through the handwritten actor runtime and legacy
  `signal-message` ingress.
- `terminal` now has generated schemas and a generated daemon spine, but live
  behavior still runs through `terminal-supervisor` plus transitional
  `terminal-daemon` session-cell behavior.

The next implementation slice should therefore be adapter cutover, not more
schema-file creation:

1. Make router's generated daemon adapter call the existing `RouterRuntime`
   behavior, preserving the working and meta socket semantics already tested.
2. Make terminal's generated daemon adapter call the existing supervisor
   behavior, then fold owner/meta session create into the component daemon.
3. Add one cross-repo harness test or script that launches real message,
   router, and terminal processes and asserts the message bytes reach a
   terminal transcript.

## Notes

Terminal exposed a lockfile/runtime compatibility problem: it had resolved
`signal-frame` to a commit incompatible with current `triad-runtime`.
Updating the lock back to the current `signal-frame` main commit resolved it;
no runtime code change was needed.

Primary had an unrelated dirty file at `orchestrate-cli/src/error.rs` when this
report was written. I did not inspect or modify that file.
