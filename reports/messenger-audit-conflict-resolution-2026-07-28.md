# Messenger audit conflict resolution — 2026-07-28

## Scope

This report preserves the independent read-only review of the conflicting
claims in `core-operations-audit-2026-07-28.md` and
`messenger-first-repair-proposal-2026-07-28.md`. No message was sent and no
service, store, repository, deployment, or tracker was changed.

## Resolution

The repair proposal is correct about the deployed Messenger binary. The core
audit remains correct only that Router is absent and that live delivery was not
witnessed.

- The checked-out default Message worktree is stale: its parent is
  `41627bce`; `main` is `1c47a20e`.
- CriomOS-home pins `1c47a20e`; the active user unit runs `message-0.10.2`.
- The installed package derivation's source is byte-identical to `1c47a20e`
  across all 30 build-source files, including `Cargo.lock`, engine, delivery,
  schema, and daemon code. This is direct compiled-revision evidence, not an
  inference from version naming.
- `41627bce` contains `ForwardToRouter`, `src/router.rs`, and
  `tests/forward_to_router.rs`. Revision `1c47a20e` deletes those and adds
  durable tables, direct delivery, local storage, migration, and delivery
  tests. This explains the core audit's mistaken path trace.

## Deployed code path

Orchestrate is configured with the Messenger working socket. Its registry push
sends `AssignAgentIdentity`, `BindAgentEndpoint`, and `Submit` frames there.
Messenger decodes `Submit`, commits ledger and inbox state in
`messenger.sema`, then invokes `DeliveryRunner`. It delivers directly to a
bound PTY or harness socket; otherwise it parks the entry in its durable outbox
and drains it after endpoint binding.

The Router socket configuration field remains, but `MessageEngine`, daemon
handling, and delivery do not use it. The active Messenger unit names a Router
socket that does not exist; this is a dormant value, not a local-delivery
dependency. Both Messenger sockets listen, and the daemon reopened its state
successfully at service start.

## Claims that survive review

- Router is absent.
- Startup and socket binding alone do not prove delivery.
- No current live delivery witness exists.
- Deployed `message-0.10.2` matches `main` at `1c47a20e` and implements local,
  durable, Router-free routing and direct delivery.
- Current documentation is not uniformly correct. `AGENTS.md`, early
  `ARCHITECTURE.md` text, and `flake.nix` still describe deleted
  Router-forward tests, although later architecture text calls the Router
  field dormant.

The following claims do not survive:

- Current/deployed submission forwards through Router.
- Router absence is the current local-delivery blocker.
- Deployed code and configuration are architecturally inconsistent.

Confidence in the deployed-source and code-path conclusion is very high.

## Remaining unknown and justified action

The remaining unknown is behavioral: whether the current daemon delivers a
real message to a real endpoint and preserves/retries it as designed. Proving
that requires either an isolated temporary-root test against the exact package
or an explicitly authorized synthetic submission and binding against the live
service.

No Router deployment, Router configuration repair, Message code repair, or pin
change is presently justified. A narrow documentation and Nix-check hygiene
change is justified by the stale guidance, but it must not be presented as a
runtime repair.
