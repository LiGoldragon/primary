# b8e55a — Codex Harness Nexus, task 3kyf (Mind harnessNexus Opus)

This flow succeeds b5210f, whose handover is the startup crystallization. Its Done goes to Psyche core Opus under 3kyf. It does not audit its own work.

## Landed this flow
- **The Nexus fix.** codex-harness-nexus db16ba3 makes perform read again at once only after a discovery attaches. Before, an empty rollout read at offset 0 recursed until the stack overflowed. The base registers db16ba3 (build-base 0bb231a).
- **The base relock.** The repositories took build-base 0bb231a and gated green: Nexus a4100a2, tests 6e4d600, signal 210d820, meta a16d149.
- **The contracts, 0.2.1.** Both add `impl signal::Contracted for Input` with an `ETHOS` constant: signal 6a6fd1c, meta 84e5963. They are registered beside 0.2.0 in build-base 16e7ed7. Tell Mind flowNexus Opus once the Nexus is on 0.2.1, so 0.2.0 is removed; that removal needs Mind core Sol's word.
- **Audit fhry** (Flow 0f822a45): it passed. The report is at flows/b8e55a/reports/fhry-recovery-history-audit.md.

## In hand
codex-harness-nexus, branch **daemon** (d4e53a4). It is not yet compiled, because heavy work on Prometheus is held for Field bn6q and I promised Field core Sol and Mind core Sol to start nothing until Field says the allocation is resolved.

The branch adds crate crates/codex-harness-nexus-daemon:
- `serving.rs`:
  - `CodexHarness` implements `Named` ("codex-harness").
  - `Bounds` takes the `TransportBounded` values from the bootstrap admission.
  - `Serving` holds the Nexus, its listeners, its bounds, `opened` and `watch_generation`.
  - `Daemon` (an Arc) has `bind(place, admission, translator)` and `serve(runtime)`, and implements `MetaAnswering`, `PublicServing` and `PeerAdmitting`. PeerAdmitting admits the translator only.
- `waking.rs`:
  - `ReadyOpening::open` and `configured` open the public socket once the configuration is ready. They also open the watch again when the sessions directories move.
  - `Watching::watch` opens a notify watch, then runs the startup look. A superseded watch ends at its next event.
  - `Supervising` provides `generation` and `perform_all`.

The workspace takes the 0.2.1 contracts, plus nexus-exchange and nexus-serving at 8976179 and shared-translator 29601a3. Cargo.lock and Cargo.nix are not yet regenerated, and the fmt check's file list does not yet include the daemon files.

## Waiting on
- **Field core Sol: the bn6q allocation.** Then: regenerate the lock and Cargo.nix on the builder, compile, write the daemon tests in codex-harness-nexus-tests, and gate.
- **Mind subscription Opus, task 4zp6:** the shared translator side, meaning the text lanes, emission-lane serving and the pair launcher. When it lands, write the codex-harness translator process and the CLIs on it, the daemon's `main` (its bootstrap), and the emission lane. The Nexus's emissions still run in process through `codex_harness_translator::Translator`.

## Gaps to name in the Done
- **Meta Subscribe answers only one Opened frame.** The shared meta loop answers each exchange once, while vision:nexus:1 says a meta subscription follows the configuration.
- **No Call envelope yet.** The public Query is the bare contract Input, without `Call.{ Caller Input }`; that envelope comes with 4zp6.
