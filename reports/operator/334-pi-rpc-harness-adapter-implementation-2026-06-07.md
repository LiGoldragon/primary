# Pi RPC harness adapter implementation — 2026-06-07

## Summary

Implemented the programmatic Pi intake path for `harness`.

The signal contract now carries a typed optional
`PiRpcJsonlAdapterConfiguration` in `HarnessDaemonConfiguration`
(`signal-harness` main commit `0b456501947f`). `harness` main commit
`e3eb9ecaac53` consumes that config, spawns a long-lived
`pi --mode rpc` process, writes JSONL `prompt` / `steer` / `follow_up`
commands, and marks `MessageDelivery` completed only after Pi returns the
matching successful JSONL response.

While integrating, the harness terminal path was also moved off the stale
`persona-terminal` helper dependency. Terminal delivery now writes generated
`signal-persona-terminal::TerminalFrame` requests directly and reads generated
reply frames directly.

## What changed

- `signal-harness`
  - Added `PiRpcJsonlAdapterConfiguration`, `PiRpcModelPattern`,
    `PiRpcDeliveryMode`, and `HarnessDaemonConfiguration::pi_rpc_adapter`.
  - Added NOTA and rkyv round-trip tests for the new config.

- `harness`
  - Added `src/pi.rs`: Pi RPC process/session, JSONL command writer, stdout
    reader thread, response correlation, timeout, and delivery receipt.
  - Added `src/delivery.rs`: one daemon-owned mutable adapter slot, with
    terminal and Pi RPC variants.
  - Wired `HarnessDaemonConfiguration::pi_rpc_adapter` into daemon startup.
  - Added a deterministic daemon test proving a Pi-kind harness receives a real
    Signal `MessageDelivery` and emits a `steer` JSONL command to a fake Pi RPC
    sidecar.
  - Added an opt-in live smoke test for the local low-quant Gemma 4 MoE Pi
    model.
  - Removed the stale `persona-terminal` crate dependency.
  - Fixed the message/router/harness e2e test so Nix builders do not assume
    `/git/github.com/...` exists. The real local e2e still runs when sibling
    checkouts or explicit binary paths exist; isolated Nix builders skip it.

## Verification

In `signal-harness`:

- `cargo fmt --check`
- `cargo test`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `nix flake check`

In `harness`:

- `cargo test`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `cargo test --test daemon harness_daemon_delivers_message_to_pi_rpc_endpoint -- --nocapture`
- `cargo test --test message_router_harness_e2e -- --nocapture`
- `HARNESS_LIVE_PI_RPC=1 HARNESS_LIVE_PI_MODEL=gemma-4-26b-a4b-ud-q4-k-xl timeout 180s cargo test --test pi_rpc_live -- --nocapture`
- `nix flake check`

All passed.

## Honest remaining gap

This is not yet the full live two-agent e2e the psyche demanded earlier.

What is now true: a real `harness-daemon` can deliver a real routed
`MessageDelivery` into a Pi RPC sidecar, and the adapter was live-smoked
against the local low-quant Gemma 4 MoE model.

What is not yet true: a live Pi agent B receives a routed message, decides to
run the real `message` CLI back to agent A, and agent A receives that response
through the real stack. That still needs a production-quality way to seed Pi's
role/instructions and to observe explicit reply completion without scraping
assistant prose.
