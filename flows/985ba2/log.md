# ChatGPT desktop images and application updates

User requests recovery of prior desktop-app flows, diagnosis of blank image frames in the running ChatGPT desktop app, and available updates for Codex CLI/TUI, Claude Code, Claude Desktop, and ChatGPT/Codex Desktop. Preserve running-app evidence before restart.

Dispatched desktop_evidence for prior-flow recovery and read-only image diagnostics; updates for installed/release/source inventory; workspace_setup for repository and Beads setup.

Remembered: cf0ed9 — depth 1. Desktop evidence subflow reports earlier malformed-MCP startup fault; current logs witness successful startup and conversation fetch, so this prior fault is not established as the image cause.
Remembered: ea1e56 — depth 1. Desktop evidence subflow recovered prior desktop work.
Remembered: 01a0338f — depth 1. Desktop evidence subflow recovered prior desktop work.
Remembered: 01a03e39 — depth 1. Desktop evidence subflow recovered prior desktop work.

Inventory reports updates Codex 0.153.3 to 0.153.4 and ChatGPT Desktop 26.901.31953 to 26.901.51231. Dispatched implement_updates for owning-source updates, checks, producer/consumer landing and typed deployment.

Beads: claimed primary-6zn (resume Codex update), opened/claimed primary-3uh (desktop image rendering), related the two. Beads claim on primary-6zn succeeded with auto-export git-add warning; follow-up state will be checked at landing.

Read desktop-image-investigation.md. Its carried evidence records current regular-chat fetches succeeding, unavailable per-image request logging, and no source-level image routing/filtering in the Nix wrapper. Current failure cause remains unknown. Prior ea1e56 reports warn about stale Electron processes; 01a0338f and 01a03e39 describe the Wayland override, re-witnessed in current process arguments.

Independent updates review reports no official release note documenting a fix for regular-chat image frames. The Linux preview documentation calls native Wayland experimental; association with this symptom remains unproven.

Implementation subflow reports signed OpenAI and Anthropic repository checks passed, Claude versions unchanged, Home producer 1f158666 and CriomOS consumer b7dced0a committed/pushed. Target identity matched Ouranos. Lojix deployment 234 accepted for UserEnvironment Realize and building remotely; admission is not completion.

After interruption, queried existing deployment 235 without retry. implement_updates witnessed terminal Completed / Some.Succeeded (6280 6280). Both implementation and updates subflows observed codex-remote-control.service replacement during activation: old PID 2217 (0.153.3), stop at 17:44:01 CEST, stop timeout and SIGKILL then new PID 326495 (0.153.4) start at 17:45:32. Running ChatGPT PID 297785 remained old release.

The user asked whether this interruption and subsequent reconnect was a server restart and harness recovery. updates read exact upstream rust-v0.153.4 tui/src/app/reconnect.rs and chatwidget/turn_runtime.rs: generic interrupted-turn notice, new connection resumes existing thread, no automatic retry of user operations, recovered drafts/queues paused. Answered in conversation with service witness and source semantics, distinguishing successful deployment from disconnected tool channel.

Final live witness from implement_updates: profile codex-cli 0.153.4; Claude Code 2.1.263; chatgpt package 26.901.51231; Claude Desktop 1.46388.2. Lojix Current generation 235 and live Home profile agree. Existing GUI PID 297785 remains chatgpt-unwrapped-26.901.31953; user relaunch and visible image retest remain necessary.

Closed primary-6zn with deployment/live proof. primary-3uh remains open for missing-image visual test and diagnosis if still broken after relaunch. Sequential bd dolt push completed successfully (exit 0, Push complete); auto-export git-add warnings did not prevent Dolt synchronization. Dispatched finish_primary for final intended-file review and primary commit/push after application-updates report is ready.

Follow-up: the user asks for the current picture of all LLM applications and the modifications/oddities we implement, with their reasons. Dispatched read-only application_map for installed/package/runtime evidence, harness_map for context/config/tool integration, and application_rationale for psyche/history provenance. Application_map witnessed primary clean before this log write. No application changes are requested by this follow-up.
