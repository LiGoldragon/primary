# Operator Pointers After Sandbox Dev-Stack Smoke

Role: designer-assistant
Date: 2026-05-11
Scope: follow-up guidance after persona commit `5eb64af4`, which made `persona-engine-sandbox --inside-unit` run the Nix-built `persona-dev-stack-smoke`.

## Summary

The new dev-stack sandbox witness is the right move. It proves the sandbox envelope can run actual persona daemons under `systemd-run --user`, not just write manifests. That closes the first implementation gap from `reports/designer-assistant/21-sandbox-full-engine-testing-gap-review.md`.

The next useful target is not the full engine yet. The next target is a terminal-cell live-agent sandbox witness: a real terminal-cell daemon, a real terminal-cell socket at the host-visible sandbox path, a real harness process inside the cell, and a host attach path that can view it.

## Current State

`scripts/persona-engine-sandbox` now exports and runs `PERSONA_DEV_STACK_SMOKE` inside the systemd unit. The current hardening choice is:

- `PrivateUsers=yes`
- `ProtectHome=tmpfs`
- explicit `HOME`
- explicit `WorkingDirectory`
- explicit `ReadWritePaths` for the sandbox root
- no `PrivateTmp=yes`

That is correct for the current host-visible socket/artifact requirement. The operator found that `PrivateTmp=yes` breaks the current `ReadWritePaths` shape, so it should stay deferred until there is a tested replacement.

`scripts/persona-dev-stack` currently starts:

- `persona-message-router-daemon`
- `persona-terminal-daemon`
- an echo-style child path through the terminal contract

It writes process and socket manifests and proves the message CLI plus terminal signal path. It does not yet start:

- terminal-cell
- a live Codex, Claude, or Pi harness
- persona-harness daemon
- persona-mind adjudication
- persona-daemon component launching

That is fine. The witness should stay named as a dev-stack witness, not a full-engine witness.

## Highest-Value Next Step

Add a separate stateful Nix app for the live terminal-cell lane, probably:

`persona-engine-sandbox-terminal-cell-smoke`

This should be separate from `persona-dev-stack`. The dev stack's terminal socket is a persona-terminal contract socket, while the host attach helper needs a terminal-cell socket. Forcing both through one runner will blur the distinction between the terminal supervisor contract and the raw terminal-cell attach surface.

The new smoke should run inside `persona-engine-sandbox` and start:

- `terminal-cell-daemon --socket "$sandbox_dir/run/cell.sock" ...`
- one child harness process inside the cell
- preferably Pi first, because it avoids paid-provider authentication and external account side effects

Then prove, using production terminal-cell commands, that:

- `$sandbox_dir/run/cell.sock` exists and is connectable from the host side.
- `persona-engine-sandbox-attach --sandbox-dir ...` can emit or launch a viewer command for that socket.
- `terminal-cell-send` can inject a prompt.
- `terminal-cell-wait` or the equivalent can wait for an expected marker.
- `terminal-cell-capture` can write an inspectable transcript.

This is the path that should close the still-open live attach bead. It also keeps the next witness honest: it tests the actual daemon and CLI, not a self-contained test fixture.

## Packaging Gap

The persona flake needs a first-class terminal-cell dependency before the terminal-cell smoke can be cleanly reproducible.

Add a flake input for terminal-cell, or otherwise provide Nix-built store paths for:

- `terminal-cell-daemon`
- `terminal-cell-view`
- `terminal-cell-send`
- `terminal-cell-wait`
- `terminal-cell-capture`

The host Ghostty attach helper can remain host-facing because the GUI terminal is deliberately outside the sandbox. But the command it emits should prefer the Nix-built `terminal-cell-view` path, or at least accept an explicit `TERMINAL_CELL_VIEW` override and record the resolved command in an artifact.

Avoid relying on whatever terminal-cell binary happens to be on `PATH` without recording it. If a host binary is used temporarily, write its resolved path and version or commit into the smoke artifacts.

## Pi First, Then Provider Auth

Use Pi as the first live harness because it does not need Codex or Claude account credentials. The smoke should still record the Pi package or executable path it used. If the existing `PI_PACKAGE_DIR` handling only defers to host environment, tighten that now or record the exact fallback path in the artifact.

After Pi works, add a provider-auth smoke for Codex and Claude with dedicated sandbox credentials. The important assertions are:

- `CODEX_HOME` points inside the sandbox credential root.
- `CLAUDE_CONFIG_DIR` or the Claude token file points inside the sandbox credential root.
- host `~/.codex` and `~/.claude` session/history files are not mounted or mutated.
- the sandbox credential root can authenticate once through browser/device flow.
- a tiny model prompt can run inside the cell.

This must remain a stateful Nix app, not a pure `flake check`, because it depends on account credentials, a local auth flow, and possibly a GUI/browser path.

## Artifacts To Write

The terminal-cell smoke should leave enough artifacts that another agent can diagnose failure without rerunning immediately:

- `terminal-cell-run.nota`
- `terminal-cell-processes.nota`
- `terminal-cell-sockets.nota`
- `terminal-cell-transcript.txt`
- `terminal-cell-prompt.nota`
- `host-attach.nota`
- `harness-environment.nota`

The socket manifest should include the exact path:

`$sandbox_dir/run/cell.sock`

The process manifest should include the terminal-cell daemon PID and the child harness command, or the nearest durable identity terminal-cell exposes for that child.

## Architecture Cleanup For Persona

Before or alongside the next implementation step, clean stale auth language in `persona/ARCHITECTURE.md`.

The current architecture decision is:

- local trust comes from filesystem ownership and socket ACLs
- `ConnectionClass` or `MessageOrigin` is provenance/audit data, not a component-local runtime gate
- the persona daemon sets up engine paths, socket paths, ownership, and modes
- the router handles channel authorization and routes messages through mind when needed
- persona-terminal owns terminal input safety and prompt cleanliness
- persona-terminal's input gate prevents human/programmatic interleaving; it is not an auth gate
- persona-system focus handling is deferred for this wave
- `signal-persona-auth` is the home for auth/provenance vocabulary, not `signal-persona`

Specific stale shapes to remove or rewrite:

- manager mints `ConnectionClass` for every connection as if downstream components gate on it
- router quarantines owner/non-owner classes through old `OwnerApprovalInbox` machinery
- terminal drops programmatic input based on caller class
- `signal-persona` owns `ConnectionClass`, `EngineRoute`, or `OwnerIdentity`
- component-owned class policy as the security model

The replacement language should say that the local engine is a privileged-user federation guarded by filesystem ACLs, while message origin remains durable provenance for audit and mind policy.

## TESTS.md Cleanup

`persona/TESTS.md` now documents the dev-stack sandbox witness, but the older "next witness" text can still be read as the next sandbox target.

Split the test roadmap into explicit lanes:

- router persistence and message-store witness
- sandbox dev-stack witness, already landed
- sandbox terminal-cell live-agent witness, next
- full federation witness, later

The next sandbox witness should be terminal-cell live-agent. The router persistence witness is still useful, but it is not the missing host-visible terminal attach path.

## Do Not Regress On PrivateTmp

Keep `PrivateTmp=yes` out of the executable scaffold until a test proves a host-visible socket/artifact path still works with it.

A small source-level guard would be worthwhile: fail a check if `scripts/persona-engine-sandbox` reintroduces `--property=PrivateTmp=yes` without also updating the documented witness. A simpler version is acceptable for now: keep the warning in `ARCHITECTURE.md` and `TESTS.md` direct enough that future agents do not "harden" the unit back into a broken shape.

## After Terminal-Cell Smoke

Once terminal-cell live-agent smoke works, the next implementation order should be:

1. Wire persona-terminal to terminal-cell's Signal control plane.
2. Make persona-terminal own the gate-and-cache injection transaction at the supervisor level.
3. Add persona-harness daemon or a temporary harness bypass that still records the right contract shape.
4. Add router-to-mind adjudication for messages that require mind policy.
5. Teach persona-daemon to launch the component set for a named engine.

Do not make router write terminal bytes directly. Router decides whether a message may be delivered. Persona-terminal owns terminal delivery mechanics.

## Suggested Bead Titles

These are the implementation beads I would file or hand to the operator next:

- Add sandbox terminal-cell live-agent smoke with real `run/cell.sock`.
- Package terminal-cell binaries in persona's flake for sandbox witnesses.
- Record terminal-cell smoke manifests and transcript artifacts.
- Add dedicated Codex/Claude sandbox auth smoke after Pi works.
- Clean stale `ConnectionClass` and `signal-persona` ownership language in persona architecture.
- Split `TESTS.md` next-witness roadmap by lane.

The first three belong together. The architecture cleanup can happen in parallel because it removes stale directions that would otherwise mislead the implementation.
