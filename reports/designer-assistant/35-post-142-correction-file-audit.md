# Post-142 Correction File Audit

Date: 2026-05-13  
Role: designer-assistant  
Scope: user-listed correction set after designer's 142 revision:
`protocols/active-repositories.md`,
`signal-persona/ARCHITECTURE.md`, `persona-message/README.md`,
`persona-message/ARCHITECTURE.md`, `persona-router/ARCHITECTURE.md`,
`persona/ARCHITECTURE.md`, and
`reports/designer/142-supervision-in-signal-persona-no-message-proxy-daemon.md`.

## Verdict

The corrected branch is now clear and mostly present:

```text
persona-daemon supervises six first-stack components:
  persona-mind
  persona-router
  persona-system
  persona-harness
  persona-terminal
  persona-message

persona-message-daemon binds:
  message.sock 0660

persona-router binds:
  router.sock 0600

signal-persona owns:
  EngineRequest / EngineReply
  SupervisionRequest / SupervisionReply
```

`protocols/active-repositories.md` is clean. The largest remaining drift is in
`persona-message/ARCHITECTURE.md`, which still has no-daemon/proxy-era sections
below a corrected header. `reports/designer/142` also still has stale
constraints and bead text from the five-component/router-public branch.

## File Findings

### `protocols/active-repositories.md`

Status: **clean**.

The rows now say:

- `persona-router` binds one socket: `router.sock` at `0600`.
- `persona-message` owns both `message` CLI and
  `persona-message-daemon`, and the daemon binds `message.sock` at `0660`.

That matches the current decision.

### `/git/github.com/LiGoldragon/signal-persona/ARCHITECTURE.md`

Status: **mostly correct, with small internal inconsistencies**.

Good:

- It names separate root families:
  `EngineRequest` / `EngineReply` and
  `SupervisionRequest` / `SupervisionReply`.
- `ComponentKind` lists `Message`, not `MessageProxy`.
- It states the message daemon is `persona-message-daemon`.

Remaining fixes:

- Constraint table still says: "The channel has one `signal_channel!`
  declaration." That conflicts with the corrected "each relation has its own
  `signal_channel!` invocation" statement. Change it to "Each named relation
  has its own `signal_channel!` declaration."
- Code map still says `src/lib.rs` has "manager payload records and
  signal_channel! declaration" singular. Make it plural or name both root
  families.
- Boundaries list only `EngineRequest` / `EngineReply` as declared with
  `signal_channel!`; add `SupervisionRequest` / `SupervisionReply`.

### `/git/github.com/LiGoldragon/persona-message/README.md`

Status: **directionally correct, but examples and wording are stale**.

Good:

- It says `persona-message` owns `message` CLI and
  `persona-message-daemon`.
- It says the daemon binds `message.sock` and forwards to router.

Remaining fixes:

- Examples still use `PERSONA_MESSAGE_ROUTER_SOCKET=/run/persona/router.sock`.
  They should point the CLI at the message daemon socket, not router directly.
- The last paragraph still says "The proxy does not..." twice. Rename to "The
  message component" or "The CLI/daemon boundary."
- The README should name the daemon socket env var explicitly once the operator
  chooses it, e.g. `PERSONA_MESSAGE_SOCKET`.

### `/git/github.com/LiGoldragon/persona-message/ARCHITECTURE.md`

Status: **not clean**.

The header is corrected, but most lower sections are still from the old
CLI-only/proxy shape.

Conflicts:

- §0 diagram still shows `message CLI -> persona-router` directly. It should
  be `message CLI -> persona-message-daemon -> persona-router`.
- §1 component surface lists only the `message` binary; it omits
  `persona-message-daemon`, `message.sock`, the daemon accept loop, and the
  router client side.
- §2 says "The proxy owns no durable message state" and requires
  `PERSONA_MESSAGE_ROUTER_SOCKET`; this should describe the daemon's stateless
  boundary and router peer socket separately.
- §3 says the repo owns length-prefixed transport to the configured router
  socket. The CLI should transport to the message daemon socket; the daemon
  transports to router.
- §4 still says "The proxy does not build or run a daemon" and "does not depend
  on an actor runtime." Both are now false.
- Code map lacks `src/bin/persona-message-daemon.rs` or equivalent daemon
  entry and Kameo actor modules.
- Constraint tests still have proxy-named tests and no daemon accept-loop /
  SO_PEERCRED origin witness.

This file needs the biggest cleanup before operators use it.

### `/git/github.com/LiGoldragon/persona-router/ARCHITECTURE.md`

Status: **partially corrected**.

Good:

- §1 now says router has a single internal `router.sock` at mode `0600`.
- It says external engine-owner ingress arrives through
  `persona-message-daemon`.

Remaining fixes:

- It still says `persona-message` is a "stateless CLI/proxy."
- It still describes the first-stack structural channel projection as
  `message-proxy`, and later says the production daemon default is the
  internal `message-proxy -> router` relation.
- Rename those to `message` / `persona-message-daemon -> router`.
- The constraint "Router does not depend on the stateless `persona-message`
  proxy crate" should be reworded. The intent is probably still "router does
  not depend on the runtime crate," but the proxy term should retire.

### `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md`

Status: **mostly correct, with stale labels**.

Good:

- Component sockets now include `message.sock`, not `router-public.sock` or
  `message-proxy.sock`.
- The constraints section says `message.sock` is group-writable and bound by
  `persona-message-daemon`.

Remaining fixes:

- Component map still calls `persona-message` a "Stateless message proxy."
  It should be "message ingress component: `message` CLI plus
  `persona-message-daemon`."
- Engine manager model still says "transitional `persona-message` proxy."
- Constraint line "Every first-stack component has a runnable daemon/proxy
  skeleton" should become "daemon skeleton" or "daemon/CLI skeleton" only if
  the CLI distinction is intentional.

### `reports/designer/142-supervision-in-signal-persona-no-message-proxy-daemon.md`

Status: **top half corrected; lower handoff still stale**.

Good:

- TL;DR is now correct: `persona-message` is the daemon, `MessageProxy` becomes
  `Message`, `message.sock` is bound by `persona-message-daemon`, first stack is
  six.
- §2.1 corrected the separate-root-family issue.
- §4.4 corrected `SupervisionReply::ComponentHealth` as child-to-manager input.
- §5 is mostly corrected and distinguishes architecture-doc edits from
  implementation work.

Remaining fixes:

- §1 still ends with the old wrong sentence: "retire `MessageProxy` from the
  supervised set and rename the user-writable socket to something
  router-owned." It should say rename `MessageProxy` to `Message` and keep
  `persona-message` supervised.
- §2.2 still says "Add the following to `signal-persona/src/lib.rs`, under the
  existing `signal_channel!` declaration." It should say "as a separate
  `signal_channel!` invocation / root family."
- §7 constraint table is still the old wrong branch:
  five components, router two sockets, `router-public.sock`,
  and no daemon binary. Replace with six components, `message.sock`,
  `persona-message-daemon`, and router single socket.
- §8 operator bead is still the old wrong branch:
  remove `MessageProxy`, reduce first stack to five, and make router bind two
  sockets. Replace with rename `MessageProxy -> Message`, keep six, add
  `persona-message-daemon`, and keep router single socket.
- See Also says `persona-router/ARCHITECTURE.md` "gains the two-socket detail";
  that should become "keeps one internal socket; ingress comes via
  persona-message-daemon."

## Bottom Line

The conceptual decision is now settled correctly. The remaining work is
editorial but important: remove lower-section contradictions before operators
claim the bead. The highest-priority cleanup is:

1. `reports/designer/142` §7 and §8.
2. `persona-message/ARCHITECTURE.md` lower sections.
3. stale proxy labels in `persona/ARCHITECTURE.md` and
   `persona-router/ARCHITECTURE.md`.
4. singular `signal_channel!` wording in `signal-persona/ARCHITECTURE.md`.
