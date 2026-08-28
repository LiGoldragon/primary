# Claude remote session access

This flow is realizing Claude remote control with the same session-wide reach already established for Codex: access newly created sessions and create sessions remotely, without manually enabling each one.

Open:

- Remember the earlier Codex realization at one layer and recover the exact end-shape it established.
- Witness the current Claude remote architecture and whether sessions must remain open.
- Realize and prove the Claude equivalent within the ruled scope.

Active subflows:

- `remember_codex_remote`: recover the prior Codex realization and lightly check its current state.
- `inspect_claude_remote`: witness Claude's present lifecycle and owning implementation.
- `map_remote_parity`: independently map parity, disconfirm assumptions, and identify meaningful tests.

Checkpoint:

- Claude 2.1.246 already provides `claude remote-control` as a persistent multi-session local server that can create same-directory, worktree, and resumed sessions remotely.
- The current home profile has a managed Codex app-server but no corresponding managed Claude remote-control service.
- Existing direct `claude` invocations are not automatically adopted by that owner; live remote-controlled sessions currently depend on their local owner/bridge processes remaining alive.

Remembered: 01a03f49 — depth 1

- The Codex realization made one Home Manager service (`codex app-server --remote-control --listen unix://`) the per-user thread owner and routed ordinary TUIs through its Unix socket; restart, socket permissions, concurrent clients, and live hosts were proved.
- The transferable shape is one persistent per-user owner plus attached terminal clients. Claude differs materially: its auto-connected ordinary sessions remain separate processes, its persistent creator is rooted in one directory, and all remote transcript/tool activity crosses Anthropic's relay.

Settled:

- The user-visible capability exists in Claude 2.1.246, but it is two mechanisms: user-wide `remoteControlAtStartup` for every newly launched interactive session, and a persistent `claude remote-control` server for remote creation.
- Claude cannot currently reproduce Codex's single durable multi-directory inventory exactly; local processes must remain alive for continuous access, with only time-limited resume after stopping.

Blocked on a psyche ruling before realization:

- Whether to expose every Claude interactive session through Anthropic Remote Control, and whether `/home/li/primary` is the root from which the always-on creator should make same-directory/worktree sessions.

Ruling received:

- Flow `01a03f49` is the target design: one persistent per-user owner, with local and remote clients controlling owner-held sessions that outlive an individual UI. Determine whether Claude can realize that contract rather than treating per-process auto-connect as equivalent.

Claude parity finding:

- `claude remote-control` can be the persistent multi-session owner, and Claude Desktop/browser/mobile can view and steer its sessions as Remote Control clients. Those clients may close without ending the sessions while the owner service remains alive.
- Claude exposes no supported local TUI client for a server-owned Remote Control session. A TUI with `--remote-control` owns a separate session; `--resume` starts another process over the conversation history rather than attaching as a thin live client.
- Therefore the exact `01a03f49` topology is not natively realizable in Claude 2.1.246. Its terminal-best supported shape is a managed persistent owner plus Desktop/browser/mobile clients; local TUI interaction remains message-level coordination or a separate owner, not shared-session attachment.

Working instruction:

- Combine the accepted Claude Desktop plus persistent-owner design with the design goal established in flow `01a0437d` and implement the whole result.
- Another flow may be editing the same repository: work in a worktree, coordinate through its Lock, and merge only if the Lock is released before completion. Stop and ask if the merge mechanism is not understood.

Remembered: 01a0437d — depth 1

- CriomOS-home must own canonical Codex and Claude package options, with every TUI, service, Agent Intercom, editor, ChatGPT Desktop, and Claude Desktop consumer using those exact derivations. Desktop product versions remain independent; missing canonical runtimes fail closed.
- Its realization remains uncommitted in the dirty `home-canonical-llm-packages` worktree, tracked by bead `home-42n`; the migration must be finished and proved rather than bypassed.

Cross-flow coordination:

- Flow `01a03f49` owns and lands its smaller Codex sole-daemon change to CriomOS-home `main` first.
- This flow stays in an isolated worktree for the larger canonical-package plus Claude-owner result, then integrates the pushed Codex revision before landing.
- Flow `01a03f49` explicitly accepted ownership of CriomOS-home `main`; it is auditing its exact write set in `/home/li/wt/github.com/LiGoldragon/CriomOS-home/unified-codex-clients` and will send its typed Lock and revision.
- Flow `01a03f49` landed and pushed Home `74f67f56c79d` (`Complete unified Codex client topology`) and released Lock `51`. Its Nix evaluations timed out before the checks, so this flow must supply the combined evaluation/build and live Desktop lifecycle proof before deployment.

Completion instruction:

- The two flows must remain coordinated, merge the totality of both results, run the combined proof, and deploy it. Whichever flow has the most appropriate complete context owns final integration and deployment.

Producer landed:

- CriomOS-home `main` is `f964853a0c067cdabbe0b8d4904346fadeb9a152` (`Migrate canonical Codex and Claude packages`), containing the landed Codex topology from `74f67f56` plus the complete canonical-package and Claude-owner realization.
- Locks `52` and `53` were released after push. The worktree is clean.
- All focused remote-builder gates for Claude/Codex Remote Control, TUI/Desktop gates, VM, Agent Intercom, VSCodium, Claude Desktop CLI/launcher/EGL, updater, Bird isolation, and launch orchestration exited `0` with real Lojix system input.
- Preserved external blockers: Pi 0.84.1 only knows `openai-codex/gpt-5.5` while existing policy names 5.6 models; the untouched orchestrate-wrapper-fallback aggregate fixture lacks `moduleResult.config`.

Open:

- Advance the CriomOS consumer to Home `f964853a`, prove the complete host, deploy, and perform the live signed-in Desktop/daemon lifecycle witness.
