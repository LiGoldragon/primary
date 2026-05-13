# Review Of Designer 142 - Supervision And Persona Message

Date: 2026-05-13  
Role: designer-assistant  
Subject:
[reports/designer/142-supervision-in-signal-persona-no-message-proxy-daemon.md](/home/li/primary/reports/designer/142-supervision-in-signal-persona-no-message-proxy-daemon.md)

## Verdict

The corrected top of designer/142 now has the right architecture:

- no separate `signal-persona-supervision` repo;
- no `persona-message-proxy` daemon;
- `persona-message` itself remains the supervised daemon component;
- `MessageProxy` should be renamed to `Message`, not deleted;
- first stack remains six supervised components;
- the user-writable ingress socket should be `message.sock`, bound by
  `persona-message-daemon`;
- engine-lifecycle reducer and engine-status reducer are distinct reducers.

That matches my prior
[reports/designer-assistant/33-engine-prototype-naming-and-supervision-corrections.md](/home/li/primary/reports/designer-assistant/33-engine-prototype-naming-and-supervision-corrections.md).
My earlier draft review of designer/142 followed the wrong five-component /
router-public branch; this report replaces that draft.

There are still two issues to fix before operators implement from designer/142:

1. The report's later sections still contain stale text from the bad
   router-public/five-component branch.
2. The supervision relation belongs in `signal-persona`, but it should be a
   separate root request/reply family, not variants folded into
   `EngineRequest` / `EngineReply`.

## Findings

### 1. High - Later Sections Still Contradict The Corrected Top

Designer/142's title and TL;DR now say the right thing:
`persona-message` is the daemon; the first stack has six components; rename
`MessageProxy` to `Message`; use `message.sock`.

But stale text remains later in the same report:

- §1 still says "retire `MessageProxy` from the supervised set" and "rename
  the user-writable socket to something router-owned."
- §5.1 says remove `ComponentKind::MessageProxy`; it should say rename it to
  `ComponentKind::Message`.
- §5.3 still says add `router-public.sock` bound by `persona-router`, and says
  the supervised set is five components.
- §5.4 still tells `persona-router` to bind two sockets.
- §5.5 still says `persona-message` has no daemon runtime.
- §5.6 still says `persona-message` is a CLI-only no-daemon repo.
- §5.7 still says designer/125 should rename the socket to "router public
  ingress."
- §7 still lists tests for a five-component first stack,
  `router-public.sock`, and "persona-message repo has no daemon binary."
- §8's operator bead still instructs operators to remove `MessageProxy`, reduce
  first stack from six to five, and make router bind two sockets.
- §9 still says DA/32's real daemon recommendation is rejected and the
  supervised set is five components.

These are not harmless historical notes; they are inside the implementation
handoff. If an operator reads only §5-§8, they will implement the wrong branch.

### 2. High - Current Repo Architecture Still Reflects The Wrong Branch

The architecture files designer/142 says it edited still contain the
router-public/no-daemon state in several places:

- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` lists
  `router-public.sock` in the component socket set and says the router-public
  socket is group-writable for owner ingress.
- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` still describes
  `persona-message` as a stateless message proxy, not as the supervised message
  daemon.
- `/git/github.com/LiGoldragon/persona-router/ARCHITECTURE.md` says router
  exposes two sockets, `router.sock` and `router-public.sock`.
- `/git/github.com/LiGoldragon/persona-message/ARCHITECTURE.md` says "no
  daemon, no actor runtime, no durable state" and says the `message` CLI sends
  directly to `router-public.sock`.
- `/git/github.com/LiGoldragon/signal-persona/ARCHITECTURE.md` says there is no
  `MessageProxy` variant and that the user-writable ingress socket is bound by
  router directly.

The corrected architecture should instead say:

```text
persona-daemon supervises:
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
```

The current code still has the old `MessageProxy` names, which is expected
until operator renames them. The architecture files should not be on a third
branch while the source waits on implementation.

### 3. High - Supervision Belongs In `signal-persona`, But Needs Its Own Root Family

Designer/142 is right that there should be no
`signal-persona-supervision` repo.

The implementation shape still needs tightening. §2.2 says to add supervision
records "under the existing `signal_channel!` declaration," and
`/git/github.com/LiGoldragon/signal-persona/ARCHITECTURE.md` says the manager
catalog and supervision relations share one `signal_channel!`.

That conflicts with `skills/contract-repo.md`: a multi-relation contract crate
has one root family per relation. The correct shape is:

```text
signal-persona
  EngineRequest / EngineReply                 -- CLI/client -> persona-daemon
  SupervisionRequest / SupervisionReply       -- persona-daemon -> supervised child
```

Same crate, separate root enums. If `signal_channel!` only supports one channel
per crate cleanly, the macro or module layout should be adjusted; the relation
model should not be weakened to fit the macro.

Why it matters: CLI clients and supervised child daemons are different
endpoints. They have different sockets, direction, authority, and witnesses.
One crate is right; one root enum is not.

### 4. Medium - Timestamp Authority Needs To Be Named

Designer/142 sketches:

```text
ComponentReady { since: TimestampNanos }
```

The report should say who mints `since`.

A child can report its own self-time as diagnostic data, but the manager-owned
lifecycle event should use manager-observed time. Otherwise the child supplies
the timestamp that drives the manager lifecycle reducer.

Recommended split:

- supervision reply: `ComponentReady` or `ComponentReady { component_started_at:
  Option<TimestampNanos> }`;
- manager event: `ComponentReady { observed_at: TimestampNanos }`, minted by
  the manager when readiness succeeds.

This follows the contract-repo authority rule: time fields need a named minting
side.

### 5. Medium - `SupervisionReply::ComponentHealth` Is Misdescribed As Manager-To-CLI

Designer/142 §4.4 says:

> `SupervisionReply::ComponentHealth` (manager-to-CLI passthrough)

That crosses the two relations the report is trying to separate.

Correct wording:

- `SupervisionReply::ComponentHealth` is child-to-manager input to the
  engine-status reducer.
- `EngineReply::ComponentStatus` or `EngineReply::EngineStatus` is
  manager-to-CLI output from the engine-status reducer.

## What I Agree With

Designer/142's corrected top-level decisions are right:

- `signal-persona` is the home for common readiness/supervision.
- `persona-message` remains a first-stack daemon.
- `MessageProxy` retires as a name only; the component becomes `Message`.
- `persona-message-daemon` owns `message.sock` at mode `0660`.
- `persona-router` keeps its internal `router.sock` at mode `0600`.
- The two reducers should be explicitly named and tested.
- Exit observation should land before restart policy.
- Criome stays out of the local readiness path.

## Corrected Operator Hand-Off

The handoff should say:

1. `signal-persona`: add `SupervisionRequest` / `SupervisionReply` as a
   separate relation in the same crate; rename `ComponentKind::MessageProxy` to
   `ComponentKind::Message`.
2. `persona`: rename `EngineComponent::MessageProxy` to
   `EngineComponent::Message`; keep six first-stack components; rename
   `message-proxy.sock` to `message.sock`; rename
   `PERSONA_MESSAGE_PROXY_EXECUTABLE` to a message-daemon-shaped variable.
3. `persona-message`: add `persona-message-daemon`; keep the `message` CLI as
   its client; daemon binds `message.sock` and forwards typed frames to
   `persona-router`.
4. `persona-router`: keep `router.sock` as its internal 0600 socket; do not add
   `router-public.sock` for this slice.
5. `persona-daemon`: verify socket metadata before `ComponentReady`, reduce
   lifecycle/status state through the two reducers, and restore latest reduced
   manager state on startup.
6. Tests: first-stack witness has six child processes; message ingress witness
   proves `message` CLI -> `persona-message-daemon` -> `persona-router`, not
   CLI -> router directly.

Once designer/142's stale lower sections and repo architecture edits are
corrected to that handoff, it is a good operator guide.
