# Core operations audit — 2026-07-28

## Scope and method

This is a read-only audit of Mind, Orchestrate, Messenger, and the system
called “Logics” in the dispatch. No deployed component or store was modified,
and no messages, claims, registrations, restarts, or deployments were issued.

There is no exact deployed or source component named `Logics` or `logics`.
The exact-name search across the primary workspace and LiGoldragon sources
returned only audit reports written today, not a component definition. It
therefore remains **unknown** and must not be silently normalized.

Two distinct candidate families were found, with no evidence that either is
the requested term:

- **Logos**: `core-logos`, `logos-runtime`, and `logos-engine`, a source-only
  language/message-plane family on this host.
- **Lojix**: a separately named, deployed typed deploy orchestrator. It is not
  an alias for Logos in the inspected source and deployment text.

Live witnesses were collected at 2026-07-28 CEST: systemd state, executable
paths, Unix sockets, a read-only Orchestrate observation, generated service
units, local state layout, source architecture/tests, `jj` main revisions,
and BEADS read commands. `nix flake check --no-build` completed successfully
for Mind: it evaluated its package and all declared test derivations, but did
not build or execute them.

## Executive result

Only Orchestrate is demonstrated usable for its essential live operation.
Messenger starts and accepts a socket connection, but its only demonstrated
submission path forwards to a router socket that is absent by design; it is
therefore not a reliable delivery system. Mind and Logos have source repos but
no observable deployment on this host. Lojix, if it is what “Logics” meant, is
also demonstrably unavailable because its daemon is in a restart loop. The
four-system goal cannot be met without resolving the name, deploying Mind and
any selected language component, and repairing or replacing Messenger’s live
delivery path.

Highest-leverage next fix: make Messenger's declared messenger-first local
delivery path real in the deployed package, then prove it with a two-endpoint
live acceptance test. It removes the observed hard dependency on an explicitly
undeployed router and is the immediate blocker for multi-agent coordination
beyond Orchestrate’s shared-store operations.

## Observations

### 1. Live deployment

| System | Canonical source and main revision | Observable deployed state | Operational witness |
|---|---|---|---|
| Mind | `/git/github.com/LiGoldragon/mind`, `042550a03083`, package version `0.8.0` | No `mind`, `mind-daemon`, or `meta-mind` executable in the profile; no Mind unit, socket, state directory, or CriomOS/CriomOS-home deployment reference found. | Not runnable on this host. |
| Orchestrate | `/git/github.com/LiGoldragon/orchestrate`, `83e09a131634`, package version `0.16.0` | `orchestrate-daemon.service` active/running since 12:29:47; process and profile both use `orchestrate-0.16.0`; ordinary/meta/upgrade sockets exist under `/run/user/1001/orchestrate`. | `orchestrate '(Observe Lanes)'` returned a live `LanesObserved` response. `Observe Worktrees` also returned the registry. |
| Messenger (source still named Message) | `/git/github.com/LiGoldragon/message`, `1c47a20e9b92`; deployed package reports `message-0.10.2` | `message-daemon.service` active/running since 12:29:47; working and owner sockets exist under `/run/user/1001/message`. | Startup and socket binding work. No non-mutating live delivery operation exists in the documented CLI surface, so successful delivery was not claimed. |
| Logos family (candidate only; not established as “Logics”) | `core-logos` main `5b66127de26b`; `logos-runtime` main `b6ca1daf24f4`; `logos-engine` main `d25d262dfc14` | No `logos-engine` command, service, socket, state directory, or CriomOS/CriomOS-home deployment reference found. | Not runnable on this host. |
| Lojix (candidate only; not established as “Logics”) | `/git/github.com/LiGoldragon/lojix`, main `9adc6c75b8be`, package version `0.10.0` | `lojix-daemon.service` is in `activating/auto-restart`; the deployed `lojix-0.10.0` daemon exits status 2. | It rejects `/var/lib/lojix/lojix.sema`: store schema v1, daemon expects v2. At observation it had restarted 591 times. |

The deployed generated units name the concrete packages and configuration:

- Orchestrate: `/nix/store/...-orchestrate-0.16.0/bin/orchestrate-daemon`.
- Messenger: `/nix/store/...-message-0.10.2/bin/message-daemon`.
- Orchestrate is configured with the co-resident Messenger socket and no
  router label.
- Messenger is configured with `/run/user/1001/router/router.sock` as its
  router peer. That socket does not exist, and no router process or active
  router unit was found.

### 2. Runtime architecture and health

**Orchestrate is wired and presently healthy at its core boundary.** Its daemon
owns `/home/li/.local/state/orchestrate/orchestrate.sema`; the profile wrapper
sets `PERSONA_ORCHESTRATE_SOCKET`; its `Observe Lanes` call completed against
the live Unix socket. Both the daemon and its three endpoints are present.
There were no warning-or-higher journal entries after the 2026-07-28 restart.

The worktree registry is not clean: the live observation returned many active
and abandoned historical worktree records. Older journal entries through
2026-07-27 show failed worktree teardown/auto-land attempts caused by absent
`git`/`ssh`, invalid or missing JJ worktrees, stale working copies, and missing
owning-lane registrations. These are historical failures, not proof that the
new daemon is presently failing: the active unit now explicitly includes
`git`, `jj`, and `gnupg` in `PATH`, and the current boot has no warning-level
entry. They remain a reliability risk for the worktree lifecycle, not a reason
to reject the live claim/observe path.

**Messenger is running but its delivery dependency is absent.** The deployed
`message.nix` explicitly says “No router daemon is deployed”, configures the
router endpoint as `%t/router/router.sock`, and says absence degrades forwards
to a typed unreachable outcome. The endpoint is absent in the running system.
The Message source's documented and tested submission effect is
`ForwardToRouter`; `forward_to_router.rs` has a specific router-unreachable
test expecting a typed error. Thus any current submission requiring that path
cannot complete successfully on this host. Socket presence proves ingress
startup only, not delivery.

There is also a material contract conflict: the current deployment module
describes Messenger as owning a durable agent map and delivery registry, while
the checked-out Message `AGENTS.md` says it owns no local ledger or actor
registration and forwards `signal-message` to router. The current
coordination-liveliness design says local messaging must be messenger-first
and router only host-to-host. The source test/architecture surface still
exposes the router-forwarding path. This is direct evidence of architectural
drift; it does not establish which contract the deployed `0.10.2` binary
implements beyond its router configuration.

**Mind is source-wired but not host-wired.** Its architecture describes a
Unix-socket daemon/client transport around `MindRoot`, with `mind`,
`mind-daemon`, `meta-mind`, and a configuration writer. Its flake declares
seven integration test files and checks for CLI/daemon exchange, work-item
open/query, restart survival, and owner-meta socket reachability. Its
`nix flake check --no-build` evaluated all those derivations successfully.
None is a witness for this machine, because no declarative unit, executable,
state, or socket is deployed.

**Logos is library/source only on this host, and is merely a candidate for the
unresolved word “Logics.”** `core-logos` is the stringless
typed algebra; `logos-runtime` is the shared message-plane runtime;
`logos-engine` describes a daemon and thin CLI projecting CoreLogos through
TextualRust. The engine's main has no `tests/` files and its flake exposes a
package/dev shell but no explicit check set. Neither source capability is
deployed, so no live Logos behavior can be attested.

### 3. Test and tracking evidence

- Per-repository `bd ready --json` for Mind, Orchestrate, Message, and
  Logos-engine all returned “no beads database found.” The primary database is
  therefore the only observable active tracker in this audit context.
- Historical design documents cite Messenger work IDs such as `primary-pm92`,
  `primary-4khu`, and `primary-te4v`, but `bd show` reports none of those IDs
  exist in the current primary database. Those documents are not current issue
  state.
- Mind's flake evaluation succeeded as above. No source test suite was run:
  executing broad build/test gates was deliberately avoided because it would
  not validate the absent deployments and would add unnecessary build activity.
- Orchestrate's live observation is the strongest executed end-to-end check.
  Messenger delivery, Mind, and Logos have no equivalent live witness.

**Lojix is a separate, demonstrably broken deploy service.** It has installed
`lojix`, `meta-lojix`, and `lojix-daemon` commands and a system service, unlike
Logos. The running service logs a fail-closed schema-layout rejection: its
store was written with schema v1 while the deployed v0.10.0 daemon expects v2.
This is not folded into the core four-system conclusion unless the psyche
confirms that “Logics” was intended to mean Lojix.

## Ranked blockers for reliable multi-agent work

1. **P0 — Messenger delivery is unavailable on the deployed topology.** Its
   configured and source-tested forward peer is an absent router socket. This
   prevents a demonstrated reliable path for agent-to-agent delivery and
   orchestration-to-agent messaging.
2. **P0 — Mind is not deployed.** There is no service, client, socket, or
   state store to supply the intended persistent agent-memory/work-state role.
   Source tests cannot compensate for the missing runtime.
3. **P1 — “Logics” is unresolved.** No exact canonical component exists in the
   inspected workspace/repositories. Logos and Lojix are different systems; no
   local evidence makes either the intended target. Clarification is required
   before treating either audit result as the fourth-system verdict.
4. **Conditional P0 — If “Logics” means Lojix, its service is unavailable.**
   The daemon restart loop is directly caused by the v1-to-v2 store schema
   mismatch, blocking all deploy-orchestrator requests until a durable
   migration or compatible deployment is provided.
5. **P1 — Messenger’s source, deployment, and approved-design descriptions
   disagree on ownership and routing.** This blocks a safe repair/deployment
   decision: a router-forwarding patch, a local-ledger implementation, and a
   deployment-only change solve different systems.
6. **P2 — Orchestrate worktree lifecycle has accumulated stale registry and
   historical teardown failures.** Core claim/observe is healthy now, but
   automated worktree landing/cleanup needs a fresh controlled witness before
   it can be trusted for high-volume parallel work.
7. **P2 — No component-local BEADS database exists.** The absence is not an
   execution failure, but it makes component-specific operational work easy to
   lose or misidentify in the primary tracker.

## Hypotheses needing confirmation

- The deployed Message `0.10.2` package may implement more of the
  messenger-first design than the checked-out source documents imply. Its
  configured absent router remains a blocker for the documented forwarding
  path, but a state-mutating submission was intentionally not sent to test
  hidden local routing.
- The many live Worktree records are likely stale operational residue rather
  than active contention. Only a deliberate, authorized lifecycle exercise can
  distinguish them.

## Unknowns

- Whether Mind and Logos are intentionally not part of this host profile or
  simply omitted from deployment.
- The authoritative runtime contract for Messenger local delivery and durable
  inboxes after the messenger-first ruling.
- Which system the psyche means by “Logics.” The evidence does not establish
  Logos, Lojix, or another component as an alias.
- Whether the current live Messenger store already contains registered agent
  endpoints; inspecting it would require a component-level read API or store
  decoder not used in this audit.

## Recommended recovery sequence

1. Decide and state the canonical Messenger contract (local messenger delivery
   versus router forwarding) from the most recent authority, then make source,
   service configuration, and architecture agree.
2. Deploy that contract with the router dependency removed from local delivery,
   and run a non-production two-agent/one-orchestrator acceptance witness:
   identity binding, message submit, durable inbox/read, recipient wake or
   delivery acknowledgement, restart survival, and typed failure for a killed
   recipient.
3. Add Mind’s package, configuration writer, user service, state path, and
   socket wrappers to the active declarative profile; verify its documented
   open/query/restart test against the installed daemon.
4. Ask the psyche to name the fourth system precisely. If it is Logos, deploy
   `logos-engine` with one narrow stored-CoreLogos-to-TextualRust witness. If
   it is Lojix, stop the v1-to-v2 migration/restart loop through an authorized,
   durable store-migration repair and prove a served request. If it is another
   system, audit that named component before acting.
5. After messaging is usable, run one authorized disposable Orchestrate
   worktree request/conclude witness and clean only records proven stale.
