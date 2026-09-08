# Unused application removal

## Result

CriomOS-home `c327e752c1b3` removes Traycer, OpenCode, and Pi from the
user-facing Home profile. It removes the Pi model module, Pi command wrappers,
the OpenCode package and activation hooks, the Traycer package and desktop
entry, and the Pi/OpenCode Agent Intercom frontend links. CriomOS
`fefe69a87703` pins that exact Home producer. Both revisions were committed and
pushed before evaluation and deployment.

The deployed profile no longer resolves `traycer`, `opencode`, or `pi`, and it
contains no matching desktop entry. Codex 0.153.4 and Claude Code 2.1.263 remain
available. `codex-remote-control.service` stayed active on PID 326495 with its
original 2026-09-08 17:45:32 CEST start time, so this activation did not restart
the controlling Codex service.

Traycer's supported CLI stopped its host and deregistered
`ai.traycer.host.service`. The Traycer host and its embedded OpenCode server are
no longer running. No Pi process was running before activation. Personal data
and history were preserved: `~/.pi`, `~/.pi-testing`, `~/.traycer`, and
`~/.config/opencode` remain directories.

## Intercom boundary

Agent Intercom's packaged orchestrator still uses private Pi runtime peers and
its internal Pi/OpenCode adapters. Removing that build-time dependency would
break the orchestrator used by Codex and Claude. This change therefore removes
the installed commands, profile configuration, frontend adapters, desktop
entry, and live service while retaining that internal dependency until a
separate Intercom decoupling change replaces it.

## Checks and deployment

The focused checks were built on the configured Prometheus remote builder with
the same projected Horizon and system inputs used by Lojix:

- `checks.x86_64-linux.agent-intercom` verifies that Pi files and OpenCode
  activation hooks are absent while Codex and Claude MCP integration remains;
  its Agent Intercom contract passed 75 of 75 tests.
- `checks.x86_64-linux.ai-agent-launch-orchestration` verifies that `pi`,
  `direct-pi`, `pi-testing`, and `opencode` are absent from the evaluated
  aggregate profile while the Codex surface remains.
- `checks.x86_64-linux.home-profile-absence` verifies that Traycer is absent
  from the evaluated max profile.

All three check derivations completed successfully. Deployment 236,
`UserEnvironment.Realize`, completed with `Some.Succeeded`. Deployment 237,
`UserEnvironment.ActivateNow`, completed at event `(6339 6339)` with
`Some.Succeeded` for immutable CriomOS revision `fefe69a87703`. Direct profile,
PATH, desktop-entry, process, systemd, and data-directory probes produced the
live witnesses above. No reboot occurred.

## Sources

- CriomOS-home removal and evaluated contracts: `c327e752c1b3`.
- CriomOS consumer pin: `fefe69a87703`.
- Lojix replies for deployments 236 and 237.
- Direct remote profile, executable, desktop-entry, process, systemd, and
  preserved-directory observations on logical node `goldragon/ouranos`.
