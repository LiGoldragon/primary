# Persona system repo plan

Status: draft
Author: Codex (operator)

Persona is not just an application that happens to run inside a random
desktop. The project is moving toward a controlled operating-system substrate:
Persona comes with enough of its own system stack to make harness routing,
input management, durable state, and human/agent coordination reliable.

This report sketches the next separation of concerns. Each level of abstraction
becomes a repository. That is how the system keeps components small enough for
agents to reason about and strict enough that the wrong behavior has nowhere to
hide.

## Stack view

```mermaid
flowchart TB
    human[human]
    desktop[Persona desktop UI]
    router[persona-router]
    message[persona-message]
    system[persona-system]
    niri[persona-system-niri]
    harness[persona-harness]
    orchestrate[persona-orchestrate]
    storage[(redb + rkyv)]

    human --> desktop
    desktop --> router
    router --> message
    router --> system
    system --> niri
    router --> harness
    orchestrate --> storage
    message --> storage
    router --> storage
    harness --> storage
```

The current Niri work is the first concrete `persona-system` backend, not a
general portability experiment.

## Repository split

| Repository | Owns | Does not own |
|---|---|---|
| `persona-message` | message contract, CLI surface, serialized message types | routing state, desktop focus, harness lifecycle |
| `persona-router` | pending queues, delivery state machine, subscriptions, actors | message schema ownership, OS-specific focus APIs |
| `persona-system` | generic OS/window/input traits and typed events; first Niri backend may live here | router policy |
| `persona-system-niri` | optional later split for Niri `$NIRI_SOCKET` backend once a second backend is concrete | generic system trait ownership |
| `persona-harness` | harness identity, lifecycle, transcript/input observers | router queue policy |
| `persona-desktop` | human composer, overview, audit UI | terminal injection policy |
| `persona-orchestrate` | workspace coordination state engine: roles, scopes, handoff tasks | harness delivery routing |
| `persona` | high-level integration and project-wide architecture | low-level component internals |

This follows the workspace rule: when there is a real abstraction boundary,
create a component for it.

## System abstraction

`persona-system` is the generic interface people port:

```mermaid
flowchart LR
    system[persona-system]
    niri[Niri backend]
    mac[macOS backend]
    x11[X11 backend]
    future[Persona compositor backend]

    system --> niri
    system --> mac
    system --> x11
    system --> future
```

The interface is event-shaped:

| Event | Meaning |
|---|---|
| `FocusChanged(target, focused)` | compositor focus changed |
| `WindowClosed(target)` | bound window disappeared |
| `InputBufferChanged(target, empty)` | harness input buffer changed |
| `DeadlineExpired(id)` | OS deadline fired |

Backends differ in support. The router does not compensate by polling. Missing
support means the relevant delivery stays queued or the port exposes a weaker
capability.

The first implementation may keep the Niri backend inside `persona-system`.
`persona-system-niri` becomes a separate repo when a second backend is concrete
enough that the abstraction/backend split earns its own repository.

## Router state ownership

```mermaid
stateDiagram-v2
    [*] --> Accepted
    Accepted --> Pending
    Pending --> Delivered
    Pending --> Deferred
    Pending --> Expired
    Deferred --> Pending: producer event
    Deferred --> Expired: deadline event
```

`persona-router` owns this state machine. It receives typed messages from
`persona-message`, system events from `persona-system`, and harness events from
`persona-harness`. It writes durable transitions to redb.

`persona-orchestrate` is a sibling state engine for workspace coordination, not
the same engine. Both are plane reducers under a future unified Persona daemon:

```mermaid
flowchart LR
    router[persona-router<br/>harness delivery plane]
    orchestrate[persona-orchestrate<br/>workspace coordination plane]
    daemon[future Persona daemon]

    router -. absorbed later .-> daemon
    orchestrate -. absorbed later .-> daemon
```

Both engines share the same discipline: typed commands, a pure reducer, pushed
subscriptions, and redb + rkyv durable state.

## redb + rkyv everywhere

The durable state direction is **redb tables with rkyv-archived records**.

NOTA remains a human-facing and harness-facing text format where useful. It is
not the durable state store for router queues, harness bindings, transcripts,
or delivery transitions.

```mermaid
flowchart LR
    cli[CLI / harness text]
    nota[NOTA input/output]
    domain[typed domain values]
    rkyv[rkyv archived records]
    redb[(redb tables)]

    cli --> nota --> domain --> rkyv --> redb
```

The rule should become part of Rust discipline: persistent component state is
typed, archived with rkyv, and stored in redb. Flat NOTA record files are
prototypes or interchange artifacts, not the steady state.

## Actor library

Stateful daemons use actors:

```mermaid
flowchart TB
    router[RouterActor]
    focus[SystemFocusActor]
    input[InputBufferActor]
    deadline[DeadlineActor]
    harness[HarnessActor]

    router <--> focus
    router <--> input
    router <--> deadline
    router <--> harness
```

The actor owns the data behind its verbs:

| Actor | Owns |
|---|---|
| `RouterActor` | pending delivery state, subscriptions, decisions |
| `SystemFocusActor` | OS event subscription and focus map |
| `InputBufferActor` | parsed input-buffer observations |
| `DeadlineActor` | OS-pushed TTL deadlines |
| `HarnessActor` | endpoint and harness binding |

There is no `StorageActor`. A storage-only actor is verb-shaped: it owns
"storing," not domain data. Each domain actor writes its own redb tables. If
cross-table atomicity becomes load-bearing, introduce a typed transaction value
or a narrower domain object rather than a generic storage dispatcher.

## Implementation order

```mermaid
flowchart TD
    report[design audit]
    message[stabilize persona-message contract]
    system[create persona-system]
    niri[Niri backend in persona-system]
    router[create persona-router]
    storage[wire redb + rkyv storage]
    live[live Niri gate test]

    report --> message
    message --> system
    system --> niri
    niri --> router
    router --> storage
    storage --> live
```

Recommended next move:

1. Create `persona-system` with generic event/domain traits.
2. Put the first Niri backend in `persona-system`.
3. Create `persona-router` for the delivery state machine.
4. Move pending delivery storage away from NOTA-line files into redb + rkyv.
5. Keep `persona-message` focused on the message contract and CLI.

## Decisions for the user

| Decision | Recommended answer |
|---|---|
| Is Niri a blocker? | No. Niri is the current OS substrate. Ports come later. |
| Should `persona-router` be separate before coding? | Yes. Routing is a real abstraction level. |
| Should `persona-system` exist before backend work? | Yes. It gives ports a target and bounds OS-facing responsibilities. |
| Should `persona-system-niri` split immediately? | No. Keep Niri inside `persona-system` until a second backend is concrete. |
| Should durable queues use NOTA record files? | No. Use redb + rkyv. |
| Should Rust discipline document redb + rkyv as the storage default? | Yes. Create a designer task to add it. |

## Audit request

This report should be audited before code starts. The audit should check:

- whether the repo split is too fine or exactly right;
- whether `persona-system` is the right name for the OS abstraction;
- whether the actor boundaries match the data each actor owns.
