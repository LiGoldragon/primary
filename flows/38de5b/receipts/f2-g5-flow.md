# F2 + G5 receipt: Flow 0.7.1

Repository LiGoldragon/flow. Base main `812053c` (Release 0.7.0). Landed revision `4671f8d4b06197551f36936180c9264607879459` on both `f2-g5-38de5b` and `main` (fast-forward; `git ls-remote` shows main at that revision).

## Tests

- Before: `cargo test --workspace` gave 62 passed (flow 4, flow-meta 2, flow-nexus lib 56). On the first run, `tests::marker_rendered_in_a_different_pane_keeps_the_flow_pending` failed once. It then passed three isolated reruns and a full `--no-fail-fast` rerun, so it is flaky on the base, not broken.
- After: 65 passed, 0 failed (flow 5, flow-meta 2, flow-nexus lib 57, flow-nexus bin 1).

## F2: version answer

signal-flow `ab70332` has no Version query (its Query enum holds Start, Restart, ResolveRecipient, Send, Stop and List). So `--version` on its own is the one allowed invocation that is not a datom. Both binaries answer it before datom parsing or configuration and print the Cargo package version:

    $ flow --version
    flow 0.7.1
    $ flow-nexus --version
    flow-nexus 0.7.1

Any other argument vector keeps its old behavior: one inline datom for `flow`, and daemon start for `flow-nexus`. The version is bumped from 0.7.0 to 0.7.1 in the workspace `Cargo.toml`, `Cargo.lock` and `flake.nix`.

## G5: Remote Control on Claude launches

The exact flag is `--remote-control <name>`. `claude --help` gives it as "Start an interactive session with Remote Control enabled (optionally named)". The name is `flow-<launch_request_id>`, which never begins with `-`, so the flag's optional value binds to it and not to the positional startup prompt.

The Claude argv is now:

    -- --dangerously-skip-permissions --remote-control flow-<launch_request_id> --system-prompt-file <bundle> --model <model> --effort <effort> <startup>

**Launch record.** The composed launch body carries a new header line:
- a Claude launch gets `Remote control: --remote-control flow-<id>`;
- a Codex launch gets `Remote control: app-server endpoint`.

The body is the preimage of `prompt_sha256`, which the target's `FLOW_LAUNCH_RECEIPT_V1` echoes, so the receipt digest covers the line. No wire type changed.

Tests that check this:
- The Claude argv fixture asserts the flag and its name.
- The Codex argv fixture asserts that `--remote-control` is absent.
- A new composition test asserts the Claude record line.
- The Codex body fixture digest is updated to `b383024f…e5f9`.

The flag has not yet been run through a live launch. It is checked only against `claude --help` and the fixtures. A live Start after deploy would show whether Remote Control is enabled, and `testing-harness-visual-state` is the skill for that.
