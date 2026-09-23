# Persona service and Codex boundary

## Completed desktop action

Following living authorization, an observer rechecked desktop GUI PID 3809062 (`.ChatGPT-wrapped`, start 2026-09-18 09:50:43), its private app-server and the independent managed server. One normal SIGTERM was sent to the GUI root only. Afterward the GUI and its private app-server/helpers/browser sockets were gone; managed app-server PID 2087, its listening control socket and integrator PID 347255 remained alive. No background-server restart, data migration or service configuration mutation was performed.

Two servers were observed, but the cause of failed desktop attachment is not established. Closing the GUI is not proof of a root-cause fix or restored desktop attachment.

## Current and proposed locations

The running managed unit is `codex-remote-control.service`, using Codex 0.153.4, working directory `/home/li/primary`, with `app-server --remote-control --listen unix://`. Current clients explicitly attach to `/home/li/.codex/app-server-control/app-server-control.sock`. Preserve this process and endpoint while sessions and the experimental Flow build are active.

Official documentation supports `CODEX_HOME` (default `~/.codex`) and explicit `--listen unix://PATH` / client `--remote unix://PATH`. These are separate choices: durable configuration/session state versus transport endpoint. Moving either does not itself make the desktop attach to that server.

Proposed future service-owned layout, **not installed**:

- Durable Codex service home: `/home/li/.local/state/persona/codex-managed`.
- Runtime socket: `/run/user/1001/persona/codex-managed.sock`, computed from the actual service user's runtime directory rather than treating 1001 as universal.
- Shared project/data checkout: `/home/li/primary`, independent of Codex home.
- Desktop UI remains a client when its attachment interface supports this topology; otherwise keep it independent and do not promise shared sessions.

Before any migration, establish the desktop attachment contract, quiesce actual writers, preserve configuration/auth/session databases through their supported backup mechanism, provide rollback, update every consumer endpoint and verify native thread continuity plus external client reachability. Do not duplicate credential files into public source, live-copy mutable databases, start a second writer on the same store, or migrate while the current integration is running. This proposal performs none of those actions.

## Persona implementation gap

Read-only source research found case-distinct `persona` at 09ee526cbde8dd6a9dc54b1b3583e2a034d0e063 and `Persona` at b6f6ef0a. Exact authoritative repository/owner must be resolved before implementation; newer date is not authority. The lowercase repository has a pre-existing Cargo.lock change, untouched by this pass.

The inspected configuration is binary rkyv `PersonaDaemonConfiguration`, with manager socket and manager store paths (`src/configuration.rs`, `src/bin/persona_write_configuration.rs`, `src/daemon.rs`). Its production path model is `/var/lib/persona` for durable state and `/var/run/persona` for IPC, with per-engine subdivisions. Typed EngineStatus/ComponentStatus describe Persona-managed records. `ManualUnitController` and `DirectProcessLauncher` do not constitute general systemd service observation.

CriomOS cef111108623617987b6e366ccbe4176c093d6b5 declares persona-router, not a persona-daemon service. Therefore “change Persona configuration to watch all services” needs an initial implementation boundary before later instances can be configuration-only.

Proposed first slice: establish the authoritative Persona producer, then a bounded `services.persona` module owning its identity, state/runtime directories, generated existing configuration and daemon. Add a typed, read-only service-observation adapter with a declared unit allowlist, expected executable/socket, response freshness, provider identity, and explicit unknown/refusal. Initially observe existing managers; do not duplicate systemd's restart ownership. Restart/reconcile policy must be explicit, bounded and independently tested before enabling it. No service or module was changed here.

## Anatomy for the existing Psyche flashbook owner

| Component | Responsibility | Evidence limit |
|---|---|---|
| Persona | Desired component configuration and supervised status | Source exists; general host-service observation/deployment unproved |
| Flow Nexus | Native MAIN identity, validated binding, lifecycle operation | Integrator eb7bae is building the registration-to-resolve slice under 4830 |
| Message | Ordinary durable delivery, queue and receipts | Does not become privileged Flow control |
| Herdr | Terminal/pane adapter and exact native attachment | A visible pane alone is not a ready or remotely reachable Flow |
| Codex / Claude | Native model, skills, context and session execution | Desktop, CLI and background server are distinct processes |
| Orchestrate | Cooperative source/path reservations | A lock is not a transactional lifecycle authority |
| Lojix / CriomOS | Materialization and declarative deployment | Source/check results are not activation receipts |
| Signal / Meta Signal | Typed ordinary and privileged contracts | Peer identity, caller claim and service authority remain separate |

Use Mind source `flows/4b0f60/reports/flow-anatomy-flashbook-source.md` for the detailed flow sequence. Psyche owns the rendered collection. The imagery brief was submitted to 836818 (not a read receipt): illustration-led, at least three pages per existing vision, with routing diagrams integrated into the imagery and explicit current/proposed labels. A Field-generated conceptual plate is review material, not a competing published flashbook or runtime claim.

## Official references

- https://learn.chatgpt.com/docs/config-file/config-advanced — CODEX_HOME and configuration/state location.
- https://learn.chatgpt.com/docs/app-server — custom Unix listener and remote terminal client endpoint.
