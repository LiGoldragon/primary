# flow-test: the Flow test twin

`flow-test` lives at `/git/github.com/LiGoldragon/flow-test`, remote
`github.com/LiGoldragon/flow-test` (public, created with `gh repo create` as
orchestrate-test was). `main` was pushed at
`67e1f0acd58f3fbc0a5e5442580b9549842c91f6`. It pins
`github:LiGoldragon/flow/ae0502724c16c33bab523fc9ac800d53c5b48b87` (0.18.0,
remote main), its `nixpkgs` following this flake's. Two pure checks pass; a
gated light-model scenario is documented and never runs in CI.

## Layout

Same blueprint shape as orchestrate-test:

| Path | Role |
|---|---|
| `flake.nix` | Inputs and `inputs.blueprint { inherit inputs; }`. |
| `lib/default.nix` | `flake.lib.components.flow`, `scenario`, `cheapestModel`. |
| `lib/scenario.nix` | Pure frame: fresh root with its own `HOME` and `XDG_RUNTIME_DIR` (Flow's two anchors), `expect` / `expectFailure`, an exit trap that kills the Nexus. |
| `lib/components/flow.nix` | `flow-nexus`, `flow`, `flow-meta` from the pinned package; socket and store paths; a `configuration` body builder; `start`, `stop`. |
| `checks/flow.nix`, `checks/flow-populated-store.nix` | The two pure scenarios. |
| `packages/flow-claude.nix` | The gated semi-sandbox runner. |
| `checks/lint.nix`, `formatter.nix` | nixfmt --check, deadnix, statix; `pkgs.nixfmt`. |
| `README.md`, `AGENTS.md` (`CLAUDE.md` symlink) | How to run each scenario; house rules. |

flow-nexus prints no ready line (orchestrate does), so `start` waits, bounded
to 30 s, until each socket answers a read-only query: `List.{}` on the
ordinary socket and `Retire.ffffff` on the meta socket. Retire of an unknown
flow is a refusal that changes nothing. `stop` sends TERM and requires an
exit within 10 s. flow-nexus installs no TERM handler and leaves its socket
files on disk.

## Scenario `flow` (pure check)

Fresh `HOME` and `XDG_RUNTIME_DIR` under a `mktemp -d` root in the build
sandbox. Asserted, whole stdout and exit code against literal text:

1. `$XDG_RUNTIME_DIR/flow/flow.sock` and `flow/flow-meta.sock` are sockets;
   `$HOME/.local/state/flow/flow.sema` exists.
2. `List.{}` gives `Listed.[]`. Observe was not used: `signal-flow` has only
   `Observe.Agent.<flow-id>` and `Observe.Launch`, and both name something.
   `List` is the read that needs no flow.
3. Meta `Retire.ffffff` gives `RetireRejected.UnknownFlow`.
4. Meta `Configure.{ <sockets> <source root> <stable/next Codex> [ { Codex [ / ] [ esc ] [] } ] [ Psyche Mind ] /opt/message-nexus }`
   gives `Configured.{ { <the same configuration> } NexusRestartRequired }`.
   That is the shape of `Configured.{ Configuration Activation }` in
   meta-signal-flow 2ac045c2 `ethos/signal.ethos`.
5. `List.{}` again gives `Listed.[]`, then the Nexus stops on TERM.

## Scenario `flow-populated-store` (pure check)

A fresh store is configured to move both sockets to `moved/ordinary.sock` and
`moved/meta.sock` (answering `NexusRestartRequired`). The Nexus is stopped with
TERM and restarted on the same directories. It must then:

- bind the moved sockets: `List.{}` gives `Listed.[]` and the same `Configure`
  is answered there;
- leave the default names unserved: both clients get stderr
  `Connection refused (os error 111)`, exit 2, against the stale files.

The configuration therefore persisted in the store and was read back on
start. This is observed through binding rather than through a read, because
the meta contract has no configuration read.

## Seen failing

Run in a detached unit (`flow-test-fail-3ec648`, MemoryMax=4G), log in the
scratchpad `fail.log`, rc 1, no hang:

- `flow`, with the expected Activation set to `Applied`:
  `configure: expected Configured.{ { … } Applied }` (it got
  `NexusRestartRequired`).
- `flow-populated-store`, expecting the default ordinary socket still to
  answer `Listed.[]` after the restart:
  `ordinary-default-unserved:  (exit 2)` /
  `expected Listed.[] (exit 0)`.

Both edits were reverted before the commit.

## Green

- Local `nix flake check -L --keep-going` (unit `flow-test-check-3ec648a`,
  MemoryMax=4G, 2 h bound). Both pure checks passed; the transcripts are
  in `check1.log`. `pkgs-flow-claude` failed on shellcheck SC2329: the
  cleanup function was reachable only through `trap`. It was replaced by an
  inline trap, after which `nix build .#flow-claude` succeeded.
- After the push: `nix flake check --refresh github:LiGoldragon/flow-test/67e1f0ac…`
  (unit `flow-test-remote-3ec648`, MemoryMax=4G, 2 h bound) reported
  `all checks passed!`, rc 0, 48 s wall, x86_64-linux. The checks were
  `flow`, `flow-populated-store`, `lint`, `pkgs-flow-claude` and
  `pkgs-formatter`. The scenario derivations were already built from the
  identical local tree, so most of that run came from cache.

## Scenario `flow-claude` (semi-sandbox, gated)

- Without `FLOW_TEST_LIVE=1` it exits 2 with a refusal. This was seen.
- With the flag, it makes a `mktemp -d /tmp/ft-XXXXXXXX` root and starts a
  Nexus there. It configures the Nexus with the Claude harness profile and
  asserts `Listed.[]`. It then exits 3, because the launch is not yet
  exercised. This was seen: rc 3, and the root was removed.
- No credential is copied and no model is called.
- The launch drive is written at the head of `packages/flow-claude.nix`:
  1. Copy only `.credentials.json`, with a 15-minute expiry guard.
  2. Start a sandbox Herdr.
  3. Send `Start` with a LaunchProfile naming Claude, the cheapest model
     (`FLOW_TEST_MODEL`, default haiku), one skill, a hashed source and a
     receipt instruction.
  4. Assert `Started`, the flow Active in `List`, and `Observe.Agent` reaching
     Idle or Done.
  5. `Stop`, and assert `Stopped`.
  6. Bound it to MemoryMax=2G, 600 s and a turn cap, using the unwrapped
     Claude binary.

## Not proven / open

- Not covered:
  - any `Start`, `Stop` or `Deliver` path;
  - Herdr reconciliation;
  - meta authority for a caller inside a flow's pane (the sandbox has no
    Herdr, so every peer is the owner);
  - Codex adapters (the configured endpoints are fake `/opt` paths, never
    dialled);
  - the deployed live Nexus;
  - systems other than x86_64-linux.
- `Configure` answers with what the store holds, so a Configure echo after a
  restart is not itself proof of persistence. The moved binding is the proof.
- No running flow-nexus, live home or `/run/user/1001` was touched. The
  checks run in the Nix sandbox, and the gated runner's Nexus lived under
  `/tmp/ft-*`.
- This report is written but not published to Primary `main`. Publishing
  needs the PrimaryPublish lock (compensation-primary-commit), and that is
  left to the main flow.

## Sources

- `/git/github.com/LiGoldragon/orchestrate-test` at 97ed7804: flake, `lib/`,
  `checks/`, `packages/orchestrate-claude.nix`, README, AGENTS.md (the shape
  copied).
- `/home/li/primary/flows/3ec648/reports/orchestrate-test.md`,
  `/home/li/primary/flows/3ec648/reports/flow-traits-first.md`.
- `/git/github.com/LiGoldragon/flow` at ae050272: `flake.nix`, README,
  `crates/flow-defaults/src/lib.rs`, `crates/flow-nexus/src/{main,lib,peer,store}.rs`,
  `crates/flow-nexus/tests/default_start.rs`, `crates/flow/src/main.rs`,
  `crates/flow-meta/src/main.rs`, `crates/flow/tests/default_socket.rs`.
- meta-signal-flow 2ac045c2 `ethos/signal.ethos` (Configured and Retire
  shapes).
- Logs in the session scratchpad: `check1.log`, `fail.log`, `remote.log`.
- Skills: subflow, compensation-nix, compensation-nix-rationale,
  repository-lifecycle, nix-workflow, testing, vision-flow, knowledge-flow,
  file-editing, flow-evidence.
