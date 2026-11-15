# Codex launch, endpoint and migration contract — fod0

Read-only source account for core Taskke1s. No Flow edit, endpoint configuration, server restart, transcript/state migration or R0 runtime change. Upstream release/model identity is core's separate verification; no new Terra model string is assumed here.

## Source and custody

Accepted R0 Flow37980e10bcb8325d9a68c580e0d22c73061bb267 at `/git/worktrees/flow-release-5c5586`; corrected Home0b3d6dfaf29cd6d67e4c92a715c972d071b12f07 at `/git/worktrees/CriomOS-home-release-5c5586`; coherent CriomOS4305f5cad95ab55a516cf430014a5f7dd7b2575e. Sol reservation282 owns the inherited release worktrees. Source/gates/Realizes accepted technically under so2t, not activated: deployed Flow remains prior eabddc8d0.56.2, as Field's current unit evidence establishes. Final R0 slot still waits f4jx conflict disposition. Other warning/typed-cohort worktrees and reservations remain separate.

Primary source pointers: Flow `crates/flow-nexus/src/codex.rs`, `herdr/launch.rs`, `lib.rs` reconfiguration; Home `modules/home/profiles/min/flow-nexus-place.nix`, `flow-nexus-config/models.datom`, `codex-next-candidate.nix`, `codex-remote-control.nix`. This account reads accepted R0 code; treat new-version capabilities as source contract, not evidence they run now.

## Endpoint, place and model configuration

Configure.Nexus carries TWO CodexEndpoint records, each client_path, home, control_socket_path and exact model-name vector (meta83 pinned06fff39). Runtime derives transcript_root as endpoint Home/sessions. CodexEndpoints::endpoint_for(codex.rs96–115) accepts a model present in exactly one endpoint; overlap or omission refuses selection. No version-name heuristic. Launcher validation accepts exact model identities; an unrecognized Codex model is not an invitation to guess an alias.

Home flow-nexus-place currently declares stable `.codex-next` home/control socket and stable flow-client wrapper for gpt-5.6-sol/gpt-5.6-luna; candidate hash-specific Home/socket/client for gpt-6.1-sol/gpt-6-sol/gpt-6-luna/gpt-6-astra. Models replay maps Sol→gpt-6.1-sol, Astra→gpt-6-astra, Luna→gpt-6-luna; Terra has no row. The Flow permaflow model enum already includes Terra. Flow's own main Place/ordinary/meta sockets are DIFFERENT from these Codex control sockets.

codex-next-candidate.nix derives a12-character identity from the candidate package derivation. Its new package means a different CODEX_HOME, socket and systemd unit `codex-remote-control-next-<hash>`. The unit runs that package's `codex app-server --remote-control --listen unix://<socket>`; Flow's client wrapper sets corresponding CODEX_HOME and execs the same package. The preparation step sets up the candidate home/permissions/credential contract, but declares no session/history migration. Plain `codex` remains stable; changing candidate package is not an in-place upgrade of all native threads.

## Launch and subsequent requests

Flow does not start/own the app-server service: Home/systemd does. Flow opens a child `<configured client> app-server proxy --sock <configured socket>` (codex.rs505–506), owns WebSocket/JSON-RPC over that bridge and does not fall back to a direct socket protocol. It probes experimental dynamic-tool capability before opening a thread and refuses a server that cannot carry the required Send tool.

open_thread_in(codex.rs1088 onward) verifies absolute existing cwd and Codex harness, initializes experimental API, calls thread/start with exact model/cwd/baseInstructions, approvalPolicy never, danger-full-access, ephemeral=false, exclusion config and dynamic Send tool. It checks returned thread identity/model/effort/instruction readback, names/reads thread, and binds FlowId to the returned native thread. Herdr attaches the configured executable with `--remote unix://<socket> --model <exact model> ... resume <thread-id>` rather than opening an unrelated local TUI session. Tests in codex.rs and herdr/launch.rs cover start/resume/readback/send-tool/attachment behavior; fake-proxy fixtures are not a live upgrade proof.

Thread subscription initializes and thread/resumes that exact id, starting no turn; it receives notifications/server calls through the proxy. A queued delivery resumes the thread and turn/starts its prompt with tracked ids/receipts; a JSON-RPC response/submission is distinguished from native read/turn completion. Startup and later turn ownership are not recreated by a TUI attaching. Flow's ordinary/meta Restart targets an existing FlowId and native session; for Codex the harness-resume path reattaches to the SAME thread, then verifies binding. Refresh starts a NEW native flow and carries configured continuity/handover/open requests by its separate succession contract; it is not native thread migration.

## Effects of configuration/executable changes

lib.rs1735–1758 compares endpoint fields and updates Live<CodexEndpoints> plus Herdr launch configuration when Configure.Nexus commits. Later endpoint lookups see the new records. Already-created CodexAdapter/proxy/subscription objects contain cloned executable/socket/model fields and open connections; replacing configuration is not an atomic relocation of those connections or an instruction to upgrade running turns. No code here stops the old server, migrates its native history or guarantees an old thread exists at a newly selected socket/home.

Changing a wrapper/link or declared binary does not replace an already running process image. Restarting an app-server may close proxies/clients and interrupt in-flight operations. Persisted threads may be resumable if that PARTICULAR target server/version/home can read and accept them, but Flow's same-thread Restart alone proves neither cross-version storage compatibility nor an in-flight-turn continuation guarantee. Hash-specific candidate homes make “same thread id at new endpoint” especially unestablished. A successful current-thread read/resume/binding and clean turn-state evidence are required; source logic must not be narrated as a successful native migration.

## Minimal selectable-model delta and required unknowns

If core verifies an exact Terra model string and the chosen candidate server supports the same required API, no new Flow model enum or hardwired branch is needed: add the exact native name to ONE endpoint's declared roster and add Terra→that name to Configure.Models (Home-owned declarations), plus any separately approved threshold/model configuration wanted for new launches. Existing running launch profiles/native ids are not automatically converted to Terra. Retain no warning policy without that model's separate native proof. Publish/gate coherent Home/CriomOS through the normal chain; it is a separate post-f4jx/R0 coordinated release, not edits to the held candidate.

A supported harness Restart can reattach an existing thread at its existing compatible endpoint; it does not migrate it. A fresh Flow launch/Refresh at the new endpoint has an explicit new-flow boundary and handover contract, not a claim of same native thread. A true cross-version/home migration still needs upstream-compatible storage evidence, declared credential/config/session-transfer scope, bounded native proof and Field-owned stopped/turn-state choreography. None was approved or run here.

Unknowns for core: exact new Terra model/release and provider availability; app-server dynamic-tool/JSON-RPC/readback compatibility; same-home/cross-home thread resume compatibility; whether in-flight turns recover or must be ended; target unit/home lifecycle and old-home retention; actual current thread/server inventory and how to settle outstanding calls. Keep these unknown until source/isolated execution establishes them. No server restart or native probe is authorized by this report.

Unrelated existing configuration defect observed: SelectsCodexEndpoint::APP_SERVER_TIMEOUT hardwires10seconds. It should become a separately released configured proxy/request timeout if changed; this account makes no such edit or R0 scope expansion.
