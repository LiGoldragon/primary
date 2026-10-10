# StablyAI Orca

Observed 2026-08-22. Architecture and communication claims are pinned to upstream main revision `80b2a0237729af8c3c57c39cd94e087b698058b9`. Stable-release and Nix claims are pinned to release `v1.4.188`, commit `f32ce859047a85a3ea4f507f633604dfbf596a0e`.

## High-level anatomy

Orca is a local-first development environment and orchestrator for terminal-based AI coding agents. It runs agents in PTYs against isolated Git worktrees, keeps their terminals and worktree state together, observes agent status, exposes files/Git/PR context, and adds durable tasks, dispatches, and mailboxes. It is a control plane around existing coding-agent CLIs, not a model provider or provider-native context-composition harness.

The primary desktop application is Electron. Its Electron main process owns `OrcaRuntimeService` and RPC; a React/Vite/Tailwind renderer provides the desktop UI. The same renderer has a browser build. A separate Expo/React Native client pairs with the desktop/headless runtime. `orca serve` starts the packaged runtime without a desktop window; a detached Node PTY daemon owns terminal sessions, and a Node 18 relay deployed over SSH supports remote hosts.

The runtime exposes newline-delimited JSON RPC locally over a Unix socket or Windows named pipe. Browser/mobile clients use WebSocket RPC on port 6768 with device pairing, per-device tokens, and `tweetnacl` encryption.

## Agent communication and context boundary

Normal `orca orchestration send` is durable structured mailbox mail:

1. The sender's CLI calls `orchestration.send` over local RPC.
2. Orca inserts a SQLite `messages` row with addressing, body, type, priority, thread, payload, delivery, and read state.
3. If the receiver already has `orchestration check --wait` pending, that waiter resolves. Otherwise, only when a recognized live recipient is idle, Orca types a notification pointer into its PTY and submits Enter: `You have N orchestration message(s). Run \`orca orchestration check\`.`
4. The body itself is not typed into the PTY. It is returned when the recipient invokes `orca orchestration check`.

At Orca's boundary, no provider SDK is called and no provider-native system, developer, user, tool-result, or synthetic transcript item is constructed. Consequently:

- The idle notification is terminal input and is therefore user-prompt-like, appended as a new turn at the bottom of the existing session. Its body is only a pointer.
- The actual mail body is CLI/RPC output from `orchestration check`; for agents that invoke the CLI through a shell tool, it reaches the model as tool output in that turn. The external agent harness, not Orca, assigns the exact transcript role.
- A waiting `check --wait` returns the message through the already-running CLI/tool call. Orca writes nothing to the PTY in that case.
- A busy receiver gets no PTY injection; unread mail remains durable until a waiter, idle edge, or explicit check.

Tracked task dispatch has a separate `dispatch --inject` path. Orca builds a preamble containing the task/dispatch identities, lifecycle commands, and task spec, bracket-pastes that complete text into the recipient TUI, and submits Enter. This is prompt-like terminal input, intended as a fresh turn. Documentation requires `tui-idle`, but current code does not enforce idleness at the final injection boundary; noncompliant use could type into an active TUI, whose provider behavior Orca cannot define.

Federated messages use persisted relay rows and remote import, then follow the same mailbox/pointer/check path. They do not directly inject cross-server model context.

Design conclusion: Orca supplies direct, durable flow-to-flow communication and task dispatch, but it does not supply privileged context placement. In particular, ordinary mail is not equivalent to a parent's initial subflow prompt: the notification is appended terminal input and the body is normally later tool output.

## Nix status

There is no official Nix packaging. The immutable `v1.4.188` source tree contains no Nix expression, flake, or devshell, and current nixpkgs has no StablyAI Orca package. `nixpkgs#orca` is GNOME Orca, the Linux screen reader.

An unofficial standalone flake exists at `Samuka007/nix-orca`. Its default branch exposes `packages.<system>.orca-ide`, a default package, formatter, and overlay for `x86_64-linux`, `aarch64-linux`, and `aarch64-darwin`, but pins Orca `1.4.146`. Open PR #1 updates it to `1.4.188`; it was unmerged when observed.

## Components worth separate study

- Terminal substrate: `node-pty`, `@xterm/headless`, Xterm serialization, and a detached authenticated PTY daemon. This is the core session-continuity mechanism.
- Durable orchestration: native `node:sqlite`, explicit mailbox/run/dispatch schemas, waiter coordination, idle-gated notification, and federated relay queues.
- Remote/mobile security boundary: Unix/named-pipe RPC, WebSockets, QR/device pairing, `tweetnacl` E2EE, and an SSH-deployed Node relay.
- Browser and automation pieces: `agent-browser`, Playwright, and `serve-sim`.
- Local capabilities and UI: `sherpa-onnx` speech support, Monaco, Tiptap, Zustand, `@parcel/watcher`, Linear SDK, React/Vite/Tailwind, and the separate Expo client.

## Sources

- Subflow report and witness: `flows/4b7c9e21/reports/orcaCommunication.md`, `flows/4b7c9e21/witnesses/orcaCommunication.md`.
- Architecture snapshot: https://github.com/stablyai/orca/tree/80b2a0237729af8c3c57c39cd94e087b698058b9
- README: https://github.com/stablyai/orca/blob/80b2a0237729af8c3c57c39cd94e087b698058b9/README.md
- Desktop manifest: https://github.com/stablyai/orca/blob/80b2a0237729af8c3c57c39cd94e087b698058b9/package.json
- Electron main/runtime: https://github.com/stablyai/orca/blob/80b2a0237729af8c3c57c39cd94e087b698058b9/src/main/index.ts
- Mobile manifest: https://github.com/stablyai/orca/blob/80b2a0237729af8c3c57c39cd94e087b698058b9/mobile/package.json
- Headless CLI: https://github.com/stablyai/orca/blob/80b2a0237729af8c3c57c39cd94e087b698058b9/src/cli/specs/serve.ts
- Runtime RPC: https://github.com/stablyai/orca/blob/80b2a0237729af8c3c57c39cd94e087b698058b9/src/main/runtime/runtime-rpc.ts
- Orchestration RPC: https://github.com/stablyai/orca/blob/80b2a0237729af8c3c57c39cd94e087b698058b9/src/main/runtime/rpc/methods/orchestration.ts
- Mailbox pointer delivery: https://github.com/stablyai/orca/blob/80b2a0237729af8c3c57c39cd94e087b698058b9/src/main/runtime/orchestration/mailbox-pointer-delivery.ts
- Dispatch preamble: https://github.com/stablyai/orca/blob/80b2a0237729af8c3c57c39cd94e087b698058b9/src/main/runtime/orchestration/preamble.ts
- Stable release: https://github.com/stablyai/orca/releases/tag/v1.4.188
- Stable source tree: https://github.com/stablyai/orca/tree/f32ce859047a85a3ea4f507f633604dfbf596a0e
- nixpkgs GNOME Orca expression: https://github.com/NixOS/nixpkgs/blob/2c423e03bbafcff28bfadc6781a4a8257f205cb5/pkgs/by-name/or/orca/package.nix
- Third-party flake: https://github.com/Samuka007/nix-orca/blob/68ac52a1ce58e7c6886a87437301f19b0bed156b/flake.nix
- Third-party package: https://github.com/Samuka007/nix-orca/blob/68ac52a1ce58e7c6886a87437301f19b0bed156b/package.nix
- Third-party update PR: https://github.com/Samuka007/nix-orca/pull/1
