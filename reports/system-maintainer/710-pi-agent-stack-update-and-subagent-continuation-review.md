# Pi agent stack update and subagent continuation review

## Deployment

Updated `CriomOS-home` and deployed it to Ouranos for `li`.

Commit: `0fb3ec82` (`home: update pi agent stack`).

Validated after activation:

- `pi` is `0.79.10`.
- `claude` is `2.1.185`.
- `codex` remains current at `0.141.0`.
- `pi-subagents` is `0.30.0`.
- `pi-continue` is `0.8.2`.
- `pi-linkup` is `0.11.0`.
- `pi-web-access` is `0.10.7`.

`nix flake check --refresh --print-build-logs` passed before the commit. The `pi-harness-profile` and `pi-criomos-extension-load` checks specifically loaded the Pi extension set and exposed the `/continue` command.

## What changed

- `pi-src`: `v0.79.8` to `v0.79.10`.
- `llm-agents.nix`: refreshed to the current upstream commit, giving Claude Code `2.1.185`.
- `claude-code` OpenVSX package: `2.1.183` to `2.1.185`.
- `pi-subagents`: `0.29.0` to `0.30.0`.
- `codex-cli-nix`: refreshed; upstream still packages `@openai/codex` `0.141.0`, matching npm.
- Pi top-level extension packages checked against npm: linkup, utils-ui, continue, and web-access were already at current top-level versions.

## Why subagents have seemed flaky

The strongest explanation is a cluster of recently-fixed `pi-subagents` issues rather than one obvious `pi-continue` incompatibility.

Evidence from upstream:

- `pi-subagents` `0.29.0` fixed model inheritance for foreground, chain, async chain, async single, and resume/revive paths. Before that, spawned agents could fall back to global settings or another session's current model.
- `0.29.0` also fixed duplicate `subagent` tool registration for fanout-authorized child processes.
- `0.30.0` fixed a relevant async-control case: live async children are interrupted before `resume` follow-up messages are delivered, so intercom nudges can reach workers that are stuck mid-turn more reliably.
- An upstream issue about async subagents not notifying the parent was closed after async delivery had changed substantially; maintainers asked reporters to verify exact installed versions, because stale installs can look like missing completion notifications.
- Another upstream issue documented foreground/sync runs returning too much after long sessions and crashing the parent; newer versions have added file-only output, truncation, output modes, and better async metadata, but large child outputs remain a design pressure.

Local-specific contributing factors:

- We were on `pi-subagents` `0.29.0`, missing `0.30.0`'s async resume/intercom reliability fixes.
- We carry a local `pi-continue` patch that changes resume dispatch from `followUp` to `steer`. That patch is plausible and remains installed, because the failure it addresses is real: follow-up delivery can wait too long during automatic mid-run continuation. But it also means our continuation behavior differs from upstream and should be watched when diagnosing any weird turn-order behavior.
- `pi-continue` is loaded as a normal Pi package, so child Pi processes may also see it unless a child launch disables extension discovery. This is not proven to be the root cause, but it is a credible interaction surface when subagents run long enough to hit compaction thresholds.

## Extension candidates to try next

Keep current `nicobailon/pi-subagents` as primary for now: it is the most feature-complete and just received fixes matching our symptoms.

Candidates worth sandbox testing, not installing globally yet:

- `@gotgenes/pi-subagents`: in-process/native subagent core, friendly fork of the Claude-style `tintinweb` package. Interesting because it avoids some subprocess/session-file failure modes.
- `@tintinweb/pi-subagents`: Claude Code-style subagents with live widget, steering, custom agent types, foreground/background support.
- `@mjakl/pi-subagent`: simpler subprocess-based package with named persistent specialist sessions. Interesting if we want continuity without the full chain/acceptance surface.
- `@johnnywu/pi-subagents` / `jwu/pi-subagents`: deliberately simple isolated child process model; useful as a control implementation.
- `pi-invisible-continue`: continuation without injecting a visible user prompt. Technically interesting, but it monkey-patches Pi internals, so it should only be tested in a sandbox.
- `pi-retry`: retry/transient-error extension. Could complement continuation for provider hiccups, but indefinite retry behavior needs guardrails before production use.

## Recommendations

1. Use the deployed stack first: Pi `0.79.10` plus `pi-subagents` `0.30.0` includes the most relevant upstream reliability fixes.
2. If subagents still fail, capture exact run evidence: parent Pi version, `pi-subagents` version, foreground vs async, child model, whether `subagent({ action: "status" })` sees completion, and whether `.pi/continue` shows a continuation fired in the child.
3. For long async jobs, prefer file output or `outputMode: "file-only"` when the child may produce huge output.
4. If failures correlate with continuation, run a controlled comparison with `pi-continue` disabled for child agents or for the whole session before replacing the subagent stack.
5. Sandbox `@gotgenes/pi-subagents` and `@mjakl/pi-subagent` next; they represent two different designs worth comparing against the current package.
