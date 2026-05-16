# User Decisions After Designer 184-200 Critique

Date: 2026-05-16
Role: designer-assistant

## Purpose

This records the user's answers to the open questions raised in
`reports/designer-assistant/90-critique-designer-184-200-deep-architecture-scan.md`.

## Decisions

## 1. CLI Environment Variables

Daemon configuration should not use environment variables as an ambient source
of truth. Daemons should be launched with explicit typed configuration or spawn
envelopes.

CLI tools may use environment variables as a convenience fallback when no
socket path is explicitly declared in configuration or command-line input.
This is acceptable because CLI usage changes often and convenience matters at
the human/debugging edge.

Architecture implication:

- daemon env fallback remains a gap to remove;
- CLI env fallback is allowed only as last-resort discovery;
- reports should not conflate CLI convenience with daemon configuration.

## 2. Subscription Close Semantics

Subscription close should be represented as a request/control operation plus a
final reply or event.

Architecture implication:

- do not delete request-side subscription retraction variants just because a
  stream also emits a final close event;
- the clean shape is: subscribe request, typed event stream, close/retract
  request, final acknowledgement event/reply, stream end;
- raw socket close is not semantic protocol.

## 3. Persona System Prototype Priority

`persona-system` can stay paused for the first prototype. The terminal-cell
input gate resolves the immediate prompt-injection/focus concern well enough
for now.

Possible later research area:

- status bar or desktop integration showing agent state, such as active agents,
  idle agents, agents waiting on human answer, and engine health.

Architecture implication:

- first prototype should focus on message, router, mind, harness, terminal,
  terminal-cell, introspect, and engine manager;
- focus and privileged desktop actions should not block the prototype;
- persona-system should remain honest as paused/skeleton unless a concrete
  desktop observation use case is implemented.

## 4. Signal-Core Stable Reference

`signal-core` should become the first target for a stable named API reference.
The preferred shape is a stable bookmark or branch, not a raw revision pin.

Architecture implication:

- the current bare git dependencies on `signal-core` are acceptable only while
  the interface is still moving quickly;
- as soon as the first stable Signal Core boundary is declared, dependent
  contract crates should move to a named API branch/bookmark such as a
  `signal-core` stability lane;
- tags can come later, but the immediate direction is stable named reference,
  not raw `rev = ...`.
