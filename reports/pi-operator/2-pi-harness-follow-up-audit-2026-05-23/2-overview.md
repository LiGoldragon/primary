# Overview

## Result

The reviewer subagent completed the read-only audit of `reports/cluster-operator/7-pi-harness-follow-up-after-third-designer-21-2026-05-23.md`. The audit confirms the report's main architectural direction: Pi v1 harness packaging is not `persona-pi`, and future `persona-pi` should use Pi's headless RPC surface rather than driving the interactive TUI.

## Findings to carry forward

The audit found one blocker: the target report describes `CriomOS-home` commit `f2e9c929`, but the live `CriomOS-home` checkout had already moved through later safety-hardening and YOLO-mode changes. Before treating the target report as current deployment truth, another agent must choose the intended revision and update the report or write a successor that says whether `f2e9c929` was superseded.

The audit found three major issues with the reported safety slice:

- The reported operator-safety extension only gates protected-path and dirty-repository mutations for Pi `write` and `edit` tool calls. Bash mutations through redirects, `tee`, `python -c`, or `sed -i` are outside that protection unless the destructive-command regex happens to catch them.
- The subagent authorization rule is prompt-only in the reported revision. It appends a system-prompt guard, but does not enforce the workspace rule at the `tool_call` boundary.
- The activation story reproduced the stale-GitHub-flake hazard: unauthenticated GitHub rate limiting caused Nix to use a cached flake. The audit recommends authenticated or refreshed origin builds, or an explicit local-path-only smoke boundary when testing unmerged home-profile work.

Minor findings: manual `pi -e ... --list-models` extension-load probes should become named Nix checks when they are recurring validation, and the target report should use the current report-kind filename/header shape in its next revision or successor.

## Parent synthesis

The audit does not invalidate the Pi RPC direction. It narrows what the `cluster-operator/7` report proves: it is good evidence for declarative Pi package wiring and Chroma theme integration, but not sufficient evidence for a complete safety policy or a final deployment path.

For Primary architecture, the important next move is not to deepen the v1 extension into a policy engine by accident. The durable shape is still `persona-pi`: daemon + `signal-persona-pi` + `owner-signal-persona-pi`, with Pi RPC as the daemon-facing substrate. The v1 extension can remain a human-harness convenience or be simplified if newer psyche intent prefers YOLO mode.

## Recommended follow-up

If the psyche wants action on this audit, the next agent should first ask which policy direction wins:

- keep safety gates in the Pi v1 harness and harden them beyond prompt-only/write-edit-only behavior;
- simplify v1 into YOLO mode and move real policy enforcement to the future `persona-pi` owner-signal contract;
- keep only minimal warnings in v1 while documenting that it is not an enforcement boundary.

Without that choice, implementation risks oscillating between convenience-mode Pi and policy-enforcing persona infrastructure.
