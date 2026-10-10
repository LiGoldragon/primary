# Messenger-first repair proposal — 2026-07-28

Status: read-only proposal. No service, store, repository, tracker, endpoint, or deployment was changed.

## Decision and observed state

The local-delivery contract is **ruled**, not a proposal. The latest authoritative record is `reports/coordination-liveliness-messenger/design.md`, revised for the 2026-07-17 psyche rulings. Its B1 ruling makes all local messaging Messenger-first and limits Router to a host-to-host leg. Messenger owns the durable local registry, ledger, inboxes, threads, local routing, and harness-delivery leg. Q2 directly rules that Orchestrate mints agent IDs before launch and Messenger is their consumer view; Orchestrate pushes identity and reachability rather than Messenger polling.

Exact SEMA layouts, the `ExternalHost` stub, PTY/control-socket mechanics, the delivery outbox, and fixture shape are implementation matter. Cold-session respawn and dead-agent bounce are outside this repair lane.

The core audit correctly found no Router socket, but it did not establish that v0.10.2 locally forwards to Router. The default Message workspace is stale (`41627bce` lineage); main is `1c47a20e`. Main contains v0.9.0 local ledger/inbox/thread routing, v0.10.0 local PtySocket/HarnessSocket delivery and durable outbox, v0.10.1 terminal-cell PTY proof, and v0.10.2's v2-to-v3 store migration.

CriomOS-home pins Message exactly to `1c47a20e`; the live user unit runs `message-0.10.2`. Message main documents the configured Router path as dormant and says the daemon never connects to it locally. The live Orchestrate v0.16.0 unit is configured with the Message socket; that revision contains identity/reachability pushes and routed-message submission to Messenger.

Thus source and declaration wiring are established, but operational delivery is not. No live message was sent, no production store was decoded, and no two real endpoints were observed. Messenger is deployed/source-wired, not yet live-witnessed.

## Smallest lane

Do not reimplement delivery and do not deploy Router. First run a disposable two-agent acceptance witness against the exact v0.10.2 package. If it passes, no production delivery/deployment mutation is needed. Then repair stale guidance and the durable Nix gate so future work cannot restore the retired Router design.

| Repository | Likely paths | Required change |
|---|---|---|
| `message` | `AGENTS.md`, `README.md`, `ARCHITECTURE.md` | Replace stateless `message -> router` guidance with the ruled Messenger-first account. Retain the Router configuration field only as deferred cross-host capability. |
| `message` | `scripts/message-component-cannot-own-local-ledger`, `flake.nix` | Retire/replace the source scan banning the required ledger, registry, and endpoint surfaces; remove old checks naming deleted `tests/forward_to_router.rs`; declare current store, delivery, migration, and two-agent checks. |
| `message` | new `tests/two_agent_daemon_e2e.rs` or a tightly scoped existing test file | Add a real-daemon, two-terminal-cell-session witness: registration/push, A-to-B delivery, B inbox read, restart persistence, and no Router. Use only a short temporary state/runtime root. |
| `message` | `flake.nix` | Make the witness a durable Nix check; inject terminal-cell tools explicitly, rather than environment-gating it. |

No present code or pin change is justified in Router, signal-message, meta-signal-message, Orchestrate, CriomOS, or CriomOS-home. A documentation/test-only Message commit does not need deployment to validate the already installed revision. If the isolated witness finds a runtime defect, stop; then make the smallest Message fix, pin it in `CriomOS-home/flake.nix` and `flake.lock`, evaluate, and seek separate activation approval.

## Acceptance witness

Run only after approval. It must not touch `/home/li/.local/state/message`, `/run/user/1001/message`, or the live user services.

1. Build the exact deployed Message revision and start a separate daemon with a short temporary state root, sockets, and an intentionally absent Router socket.
2. Start two real disposable terminal-cell sessions with separate synthetic agent IDs and endpoints. Establish identity and endpoints with the same Messenger wire operations used by Orchestrate's push client; an isolated Orchestrate producer is preferred, a narrow test-only push client is sufficient for setup.
3. Send A to B through the daemon. Require B's actual terminal transcript and `QueryInbox` to show the committed, provenance-stamped row.
4. Restart only the disposable daemon and reopen its temporary `messenger.sema`; require B's inbox to retain the row. Also park a message for a temporarily unbound B and prove the durable outbox drains exactly once after binding.
5. Require no Router listener/process in the fixture. The test must pass without any Router assertion or connection. Run the migration witness too.

The later live witness needs separate approval: two launcher-created disposable agents, only synthetic payloads/IDs, and no service restart unless explicitly authorized. Otherwise the isolated proof is the release gate; no production message is sent.

## State compatibility and risk

`messenger.sema` is versioned. v0.10.2 recognizes its declared additive v2 prior, preserves it beside the original, re-stamps to v3, and carries registry rows; unknown v1 fails closed without a preserve. This review did not inspect private store contents or prove migration already ran. Do not run an older daemon against v3 and do not overwrite the store to roll back; no reverse migration is evidenced.

The ledger is bounded: retention reaps old ledger rows and their inbox/thread references. That is designed retention rather than a new migration loss, but “durable” is not permanent. All proof data must be isolated.

The immediate service risk is stale guidance/gates: AGENTS, README, old architecture paragraphs, and the flake checks describe the deleted Router path. Preserve the deployed configuration field and binary layout in this lane; removing it is a separate cross-host capability decision.

## Train, worktrees, and rollback

Verified train: CriomOS-home pins Message `1c47a20e`/v0.10.2 and Orchestrate `83e09a13`/v0.16.0. Message's lock contains signal-message `66490df2`, meta-signal-message `98aaf228`, and sema-engine `72015662`. Do not float these while repairing the gate; Router is not a local-train dependency.

Before editing, request an isolated Message worktree and claim exactly the Message paths above through Orchestrate. The default Message workspace is stale. No applicable unmerged repair was found: the former messenger-liveness train is deleted/hidden and its substantive work is already on main; `messenger-thread-slot` is an older v0.6.0 precursor. Existing CriomOS/CriomOS-home worktree beads are unrelated. Claim Home paths only if a runtime defect requires a new pin.

Rollback after a failed isolated witness is removal of its explicit temporary run root and no production action. For a later approved deployment, activate the previous declarative Home generation while preserving `messenger.sema`; never schema-downgrade it in place. A future schema change needs an adjacent preserve, captured-store fixture, forward migration test, and separately approved recovery path.

## Approval text

> Authorize a Messenger-first verification and hygiene lane: create an isolated Message worktree; update only the listed Message documentation, retired source-scan, Nix checks, and a disposable two-agent daemon acceptance test; build and run that test in a temporary root with no Router and no access to production Messenger state or sockets. Do not alter Router, production services, deployed pins, or send a production message. If the test exposes a runtime defect, stop and return the smallest source/deployment patch for separate approval.
