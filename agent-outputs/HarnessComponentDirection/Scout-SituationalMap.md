# Harness Component Direction Situational Map

Task: read-only cleanup/design scout for the harness component direction. Scope was the existing `harness` repo plus relevant local component boundaries: `mentci-lib`, `mentci-egui`, `orchestrate`, `terminal`, `terminal-cell`, `persona`, `persona-pi`, `signal-harness`, `meta-signal-harness`, and local Claude/Codex/Pi command surfaces. I did not inspect `private-repos`, did not search `/nix/store`, did not edit component repos, and did not run tests because the brief only authorized read-only scouting.

## Commands And Files Consulted

- Workspace guidance: `/home/li/primary/AGENTS.md`, `/home/li/primary/INTENT.md`, `/home/li/primary/ARCHITECTURE.md`, `/home/li/primary/protocols/active-repositories.md`, `/home/li/primary/RECENT-REPOSITORIES.md`.
- Role/support doctrine read because this scout used VCS status and wrote a durable output: `/home/li/primary/.agents/skills/jj/SKILL.md`, `/home/li/primary/.agents/skills/repo-intent/SKILL.md`, `/home/li/primary/.agents/skills/reporting/SKILL.md`.
- Discovery/status commands: `ls -la /home/li/primary/repos`, `find /git/github.com/LiGoldragon ...`, `rg --files`, `rg -n ...`, and `jj status --no-pager` in inspected repos.
- Harness surfaces: `/git/github.com/LiGoldragon/harness/{INTENT.md,ARCHITECTURE.md,README.md,AGENTS.md,Cargo.toml,flake.nix}`, `/git/github.com/LiGoldragon/harness/src/{lib.rs,harness.rs,daemon.rs,pi.rs,terminal.rs,subscription.rs,delivery.rs,runtime.rs,configuration.rs,client.rs,meta.rs,command.rs,error.rs}`, `/git/github.com/LiGoldragon/harness/tests/{daemon.rs,pi_rpc_live.rs,subscription_truth.rs,message_router_harness_e2e.rs}`.
- Contract surfaces: `/git/github.com/LiGoldragon/signal-harness/{INTENT.md,ARCHITECTURE.md,src/lib.rs}`, `/git/github.com/LiGoldragon/meta-signal-harness/{ARCHITECTURE.md,src/lib.rs}`.
- Neighbor boundaries: `/git/github.com/LiGoldragon/mentci-lib/{INTENT.md,ARCHITECTURE.md}`, `/git/github.com/LiGoldragon/mentci-egui/{INTENT.md,ARCHITECTURE.md}`, `/git/github.com/LiGoldragon/orchestrate/{INTENT.md,ARCHITECTURE.md}`, `/git/github.com/LiGoldragon/terminal/{INTENT.md,ARCHITECTURE.md}`, `/git/github.com/LiGoldragon/terminal-cell/{INTENT.md,ARCHITECTURE.md}`, `/git/github.com/LiGoldragon/persona/{INTENT.md,ARCHITECTURE.md,src/direct_process.rs}`, `/git/github.com/LiGoldragon/persona-pi/{INTENT.md,ARCHITECTURE.md}`.
- Provider local command help: `codex --help`, `claude --help`, `pi --help`; command paths found with `command -v`.

## 1. Repos And Surfaces Found

Primary workspace:

- `/home/li/primary` is the coordination workspace. `jj status --no-pager` showed unrelated pending additions under `agent-outputs/AgentSkillCompositionIntent/...` and `agent-outputs/MirrorAppendDigestValidation/...`; I did not touch them. `repos/` is a symlink index to `/git/github.com/LiGoldragon/...`.

Relevant clean code repos:

| Surface | Path | `jj status --no-pager` summary | Appears to own |
|---|---|---|---|
| `harness` | `/git/github.com/LiGoldragon/harness` | clean; parent `ymovlrvn 81bcd004 main, use Kameo lifecycle fork` | Harness identity/lifecycle/transcript/adapter runtime, `harness-daemon`, `harness`, `meta-harness`. |
| `signal-harness` | `/git/github.com/LiGoldragon/signal-harness` | clean; parent `woopyoxx 0727beb7 main, signal-harness: bump to 0.2.0 for adapter TUI events` | Router-to-harness delivery/observation wire contract. |
| `meta-signal-harness` | `/git/github.com/LiGoldragon/meta-signal-harness` | clean; parent `vsxzvtvo 2f161d14 main, meta-signal-harness update nota dependency` | Privileged harness meta contract, currently `Configure(HarnessDaemonConfiguration)`. |
| `terminal` | `/git/github.com/LiGoldragon/terminal` | clean; parent `ovwsryrw d6c547f4 main, terminal: bump to 0.2.0 for named viewer attach` | Persona-facing terminal session owner around terminal-cell: session registry, Signal terminal surface, prompt/input gate, terminal SEMA. |
| `terminal-cell` | `/git/github.com/LiGoldragon/terminal-cell` | clean; parent `szlszuzx 17b043c5 main, terminal-cell fix CloseCell process cleanup` | Low-level one-child PTY/transcript/viewer primitive. |
| `orchestrate` | `/git/github.com/LiGoldragon/orchestrate` | clean; parent `rmlrpnwq bfe4f6d3 main, orchestrate: produce fixture workflow receipts` | Orchestration machinery: claims, lanes, roles, activity, future agent-run/spawn/scheduling machinery. |
| `mentci-lib` | `/git/github.com/LiGoldragon/mentci-lib` | clean; parent `skmsxvpn 16af712a main, mentci-lib: update mentci contract pins` | Client-side MVU model for Mentci thin clients. |
| `mentci-egui` | `/git/github.com/LiGoldragon/mentci-egui` | clean; parent `omzzlxol 4e36156a main, test raw spirit approval display path` | Thin egui shell over Mentci model/daemon. |
| `persona` | `/git/github.com/LiGoldragon/persona` | clean; parent `tuqslwrz 6b6bc606 main, use Kameo lifecycle fork` | Engine manager/apex sandbox and component spawn envelope logic. |
| `persona-pi` | `/git/github.com/LiGoldragon/persona-pi` | clean; parent `vmkrwpnq fbbdaf70 main, package pi-subagents direct agent chains` | Nix-packaged Pi harness backend and Pi-side integration; no daemon/contract crate. |

Provider command surfaces on PATH:

- `codex`: `/home/li/.nix-profile/bin/codex`. Help shows interactive default, `codex exec`, `--cd`, `--sandbox`, `--ask-for-approval`, `--no-alt-screen`, `--model`, `--profile`, and `CODEX_HOME`-style config via CLI docs.
- `claude`: `/home/li/.nix-profile/bin/claude`. Help shows interactive default, `--print`, `--bare`, `--no-session-persistence` for print mode, `--remote-control`, `--permission-mode`, `--add-dir`, `--model`, `CLAUDE_CONFIG_DIR`-style isolation implied by persona docs.
- `pi`: `/home/li/.nix-profile/bin/pi`. Help shows `--mode text|json|rpc`, `--session-dir`, `--name`, `--provider`, `--model`, `--no-context-files`, `--no-tools`, and env vars `PI_CODING_AGENT_DIR`, `PI_CODING_AGENT_SESSION_DIR`, `PI_PACKAGE_DIR`.

Observed absence:

- `find /git/github.com/LiGoldragon -maxdepth 1` did not find `persona-harness`, `persona-codex`, or `persona-claude`. `primary.code-workspace` still names `persona-harness` and related `signal-persona-harness` paths, but the active repo map and current symlink index point at `harness` / `signal-harness` instead.

## 2. Harness Repo Classification

`harness` is not vaporware. It has a real Rust crate with:

- binaries `harness`, `meta-harness`, and `harness-daemon` in `Cargo.toml`;
- checked docs/intent aligned around closed `HarnessKind::{Codex, Claude, Pi, Fixture}`;
- `signal-harness`, `meta-signal-harness`, `signal-terminal`, `signal-persona`, `triad-runtime`, and Kameo dependencies;
- a daemon (`src/daemon.rs`) that reads one binary rkyv `HarnessDaemonConfiguration`, binds working and meta sockets through generated daemon machinery, starts multiple internal harness instances, dispatches by `HarnessName`, returns typed status/readiness, and returns typed unimplemented for unfinished operations;
- terminal delivery (`src/terminal.rs`) that writes generated `signal-terminal` frames to a terminal socket and counts delivery only after `TerminalInputAccepted`;
- Pi RPC/JSONL delivery (`src/pi.rs`) that spawns a long-lived `pi --mode rpc`, writes JSONL `prompt`/`steer`/`follow_up`, waits for matching successful response ids, and kills/waits the process on stop/drop;
- transcript subscription actors (`src/subscription.rs`) and tests for open/snapshot, delta fanout, close ack, and slow-subscriber isolation;
- CLI clients (`src/client.rs`, `src/meta.rs`) that take one NOTA request and talk to `HARNESS_SOCKET` / `HARNESS_META_SOCKET`.

Useful pieces to keep:

- The repo name and core ownership are correct for the approved direction.
- The `signal-harness` contract is already provider-neutral enough for first adapters: `AdapterReady`, `AdapterInputAccepted`, `AdapterOutput`, `AdapterProgress`, `AdapterCompletion`, `AdapterConfirmationNeeded`, `AdapterStalled`, `AdapterExited`, plus transcript subscription records.
- The current daemon skeleton, configuration loading, multi-instance dispatch, status/readiness path, terminal adapter, and Pi RPC adapter are useful bootstrap substrate.
- The test suite already names many useful witnesses in `flake.nix`: socket mode, status/readiness, terminal delivery, Pi RPC delivery, typed unimplemented, ordinary/meta CLI, and kind-closure checks.

Vaporware or target-only pieces:

- Provider launch/operation behavior for Claude and Codex is not implemented. The daemon can label an instance `Claude` or `Codex`, but delivery is either terminal socket input or Pi RPC; it does not launch Claude/Codex, detect readiness, parse output, classify confirmations, detect turn completion, or close provider sessions.
- Transcript subscription producer actors are not wired through `HarnessRequestHandler`. In `src/daemon.rs`, `WatchHarnessTranscript` and `UnwatchHarnessTranscript` currently fall through to `HarnessRequestUnimplemented`.
- Meta `Configure` is not implemented. `handle_meta_connection` recognizes `meta-signal-harness` first, but replies `MetaHarnessReply::RequestUnimplemented`.
- Durable `harness.sema` is documented as future. `src/configuration.rs` says the daemon opens no durable store and points the trait `database_path` at the state directory only because the trait requires it.
- The current terminal delivery path sends raw message text with carriage return to `signal-terminal`; provider-specific prompt formatting, gate acquisition, prompt-pattern registration, and turn observation are not yet harness-owned in code.

Stale names / stale docs:

- `signal-harness/ARCHITECTURE.md` still says the destination has four `HarnessKind` variants while current daemon code carries three. Source truth in `/git/github.com/LiGoldragon/signal-harness/src/lib.rs` and `/git/github.com/LiGoldragon/harness/src/harness.rs` now has all four variants including `Fixture`, so that paragraph is stale.
- `persona-pi/ARCHITECTURE.md` refers to `persona-harness` as the consumer. On disk, the existing repo is `harness`; no `persona-harness` checkout was found.
- `persona/src/direct_process.rs` still writes supervised harness daemon config with `HarnessKind::Fixture` by default and comments that the spawn envelope must later carry typed harness kind. That is a real integration gap for Claude/Codex/Pi testing through Persona.

Missing bootstrap surfaces:

- A small authoring/launcher tool for `HarnessDaemonConfiguration` that turns a readable fixture/provider config into the binary startup file used by `harness-daemon`.
- Internal provider adapter modules for Claude, Codex, and Pi/Pi RPC with launch/readiness/send/observe/close behavior.
- A daemon request path that opens and closes transcript subscriptions over the actual socket stream.
- Adapter event publication from provider adapters into `signal-harness` events, not just delivery completion.
- First live provider tests for Claude and Codex. The only live provider test found is `tests/pi_rpc_live.rs`, gated by `HARNESS_LIVE_PI_RPC=1`.

## 3. Boundary Recommendation

Use `harness` as the home for provider operation logic.

`harness` should own:

- Provider adapter modules for `Codex`, `Claude`, `Pi`, and `Fixture`.
- Launch vectors and provider-local runtime state for each harness instance.
- Provider readiness detection, output observation, confirmation-prompt classification, prompt-turn completion detection, stall/exit classification, and close policy.
- Translation from provider observations into `signal-harness` provider-neutral events and transcript deltas.
- Harness identity/lifecycle, per-instance actor ownership, and eventual `harness.sema` history if durable history is needed.

`terminal` should own:

- Named terminal sessions, terminal registry, terminal SEMA metadata, prompt-pattern registry, input-gate leases, write injection, and the Persona-facing `signal-terminal`/meta terminal surfaces.
- The production component boundary around terminal-cell. `terminal/INTENT.md` and `terminal/ARCHITECTURE.md` are explicit that `terminal-cell` is a library/primitive under the terminal owner in production.

`terminal-cell` should own:

- One child PTY/process group, raw byte data plane, append-only transcript, viewer attach/detach, and low-level input gate mechanics.
- Development/test primitive behavior. It should not grow Claude/Codex/Pi semantics.

`orchestrate` should own:

- Lane/role/session assignment, claims, activity, scheduling, spawn/supervision machinery, and meta orders to harness/router/terminal.
- It should choose a harness kind or adapter policy as typed data, but should not contain Claude/Codex/Pi behavior or prompt parsing.

`mentci` / `mentci-lib` / `mentci-egui` should own:

- Psyche-facing UI/message ingress-egress, approval presentation, and thin client state. They should not own harness session execution, provider adapters, terminal transport, or orchestration state.

Provider-specific code should start as modules inside `harness`, not as separate components. Split later only if one adapter becomes independently deployable, has its own durable state/contract, or needs a separate Nix package like `persona-pi`. For V1, separate components would mostly add coordination cost and obscure the fact that provider behavior is one harness abstraction.

## 4. Minimal Bootstrap Plan

Keep the existing component shape:

- daemon: `harness-daemon`;
- ordinary CLI/API: `harness` over `signal-harness`;
- meta CLI/API: `meta-harness` over `meta-signal-harness`;
- config input: one binary rkyv `signal_harness::HarnessDaemonConfiguration` file.

First implementation slice:

1. Add harness-local provider adapter modules, e.g. `src/provider/codex.rs`, `src/provider/claude.rs`, `src/provider/pi.rs`, behind a single data-bearing enum or actor-owned adapter such as `HarnessProviderAdapter`. Keep methods on adapter/session objects.
2. Keep the first contract surface provider-neutral. Use existing `HarnessInstanceConfiguration.harness_kind`, `terminal_socket_path`, and `pi_rpc_adapter` where possible. Add contract fields only when Claude/Codex need typed launch data that cannot be represented by terminal session/configuration policy.
3. Wire `WatchHarnessTranscript` and `UnwatchHarnessTranscript` through the daemon before adding elaborate provider logic. That makes observation first-class and gives every provider test a common proof path.
4. Emit the existing adapter events from real adapter observations: `AdapterReady`, `AdapterInputAccepted`, `AdapterOutput`, `AdapterCompletion`, `AdapterConfirmationNeeded`, `AdapterStalled`, `AdapterExited`.
5. Keep persistence out of V1 unless a test needs it. If state is needed, open a harness-owned `harness.sema`; do not write terminal/router/orchestrate stores.

First tests to add or promote:

- `harness_daemon_opens_transcript_stream_over_working_socket`.
- `harness_daemon_emits_adapter_ready_for_fixture_provider`.
- `harness_daemon_does_not_close_session_on_adapter_completion`.
- `harness_daemon_explicit_close_emits_adapter_exited`.
- `harness_daemon_launches_pi_rpc_adapter` can reuse the existing Pi RPC fixture shape.
- Claude/Codex tests should start as gated live/sandbox tests with dedicated credential roots, not default flake checks.

## 5. Provider Test Plan

Common proof shape for all providers:

- Launch: start a harness instance in an isolated work/state directory; observe process/session identity, provider kind, and `AdapterReady`.
- Persistence: send at least two turns into the same session and prove the second turn can refer to first-turn context or provider session state.
- File writes: ask the provider to create or modify a sentinel file under the sandbox workdir; prove the file exists and content matches expectation.
- State/events: subscribe to transcript/adapter stream and require `AdapterInputAccepted`, at least one `AdapterOutput`, one `AdapterCompletion` for the turn, and no `AdapterExited` until explicit close.
- Close policy: closing a viewer or completing a turn does not kill the harness. Explicit harness close/retire stops the provider process and emits `AdapterExited`; subsequent delivery fails with typed stopped/unavailable reason.

Pi / PersonaPi:

- Use the existing Pi RPC path first because code and a gated live test already exist: `pi --mode rpc --session-dir <dir> --name <name>` with isolated `PI_CODING_AGENT_DIR`, `PI_CODING_AGENT_SESSION_DIR`, and `PI_PACKAGE_DIR`.
- Existing evidence: `/git/github.com/LiGoldragon/harness/tests/pi_rpc_live.rs` gates a live prompt with `HARNESS_LIVE_PI_RPC=1`; `/git/github.com/LiGoldragon/harness/tests/daemon.rs` has `harness_daemon_delivers_message_to_pi_rpc_endpoint` using a JSONL fixture and matching command id `harness-1`.
- Add a sandbox write proof using a local provider/model when available. Observe JSONL response success, session file presence under `--session-dir`, and no host auth/config copy.
- Also keep a terminal-cell Pi lane because `persona/ARCHITECTURE.md` says the terminal-cell sandbox Pi variant proves a real prompt-bearing local model can start and receive input through terminal-cell.

Codex:

- Use a dedicated `CODEX_HOME` and sandbox workdir; do not copy host `~/.codex/auth.json`. `persona/ARCHITECTURE.md` already names `persona-engine-sandbox --bootstrap-auth --harness <kind>` and a real `codex login --device-auth` flow for distinct sandbox credentials.
- First live proof can use terminal-cell with `codex --no-alt-screen --cd <work>` or a noninteractive `codex exec` smoke only as an auth/protocol preflight. The durable harness proof needs a long-lived session, not just `exec`.
- Observe readiness by prompt pattern/output, then send a simple file-write request. Require transcript output and sentinel file content. Completion must mean one prompt turn is done, not session close.

Claude:

- Use a dedicated `CLAUDE_CONFIG_DIR` or credential file path. Do not copy host `~/.claude` credentials/history. `persona/ARCHITECTURE.md` names `PERSONA_CLAUDE_OAUTH_TOKEN_FILE` via `LoadCredential=` or `claude auth login --claudeai` under a separate config dir.
- Start with the memory gate in mind: `/home/li/primary/reports/operator/465-agent-memory-claude-gating-exploration.md` recommends normal Claude launch be shared-memory-only and notes `claude --bare` disables auto-memory but also skips hooks/CLAUDE.md auto-discovery. A wrapper must explicitly restore required workspace contract context if it uses `--bare`.
- Use terminal-cell for the first prompt-bearing proof. Observe process alive, prompt readiness, output, file write, turn completion, and explicit close. A `claude -p` smoke can validate credentials but is not enough for persistent harness behavior.

## 6. Risks And Open Decisions For The Psyche

- Should V1 provider launch use `terminal` as the production session owner immediately, or may harness tests use `terminal-cell` directly while the production path goes through `terminal`? Evidence favors production through `terminal`, with terminal-cell direct use only as a contained test primitive.
- Claude and Codex live tests need dedicated sandbox credentials. Without explicit bootstrap/authorization, only fixture and Pi-local paths are safe to run.
- Claude memory policy is not just a harness detail. Normal Claude launch should avoid Claude-private memory unless the psyche explicitly opts in; the exact wrapper/launch vector still needs a decision.
- Provider readiness and completion are provider-specific. Trying to force these heuristics into `terminal` or `orchestrate` would muddy boundaries; harness should own them, but the psyche may need to accept provider modules inside harness as the V1 shape.
- Decide whether V1 needs durable `harness.sema`. Current code is transient. If tests only need launch/delivery/events, defer storage; if session history must survive daemon restart, implement harness-owned SEMA early.
- Decide whether `signal-harness` should grow typed Claude/Codex launch configuration now. Current config can label kinds and point at terminal/Pi RPC endpoints, but provider launch configuration is not represented for Claude/Codex.
- `persona` currently writes supervised harness config as `Fixture`. End-to-end Persona tests for Claude/Codex/Pi require a typed harness-kind/config path in spawn envelopes before they can be truthful.

## Verification Notes

- No component tests were run. Running `cargo test`/`nix flake check` would write build artifacts and was outside this scout's read-only inspection brief.
- I did not inspect `private-repos`.
- I did not search `/nix/store`.
- I intentionally did not inspect private provider credential/session stores beyond listing public project-local role/config surfaces and CLI help. Report content avoids secret/auth material.
