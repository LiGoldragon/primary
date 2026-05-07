# Persona message router architecture

Status: current operator synthesis
Author: Codex (operator)

This report supersedes the operator-side Persona reports that led here:

- `reports/operator/1-persona-core-state-pass.md`
- `reports/operator/2-terminal-harness-control-research.md`
- `reports/operator/3-persona-wezterm-harness-plan.md`
- `reports/operator/4-persona-message-plane-design.md`
- `reports/operator/5-persona-message-real-harness-test-plan.md`
- `reports/operator/7-minimal-niri-input-gate.md`
- `reports/operator/8-persona-system-repo-plan.md`

It also folds in the designer audits that are still load-bearing:

- `reports/designer/4-persona-messaging-design.md`
- `reports/designer/12-no-polling-delivery-design.md`
- `reports/designer/13-niri-input-gate-audit.md`
- `reports/designer/15-persona-system-plan-audit.md`

The old operator reports are removed with this report. The filesystem should
now point future operator work at this single current plan.

---

## Current shape

Persona is a typed message fabric around interactive harnesses. The immediate
implementation target is not the final whole Persona daemon; it is the routing
loop that lets agents send messages without corrupting a human's terminal
input.

```mermaid
flowchart TB
    human[human]
    desktop[future Persona desktop]
    message[persona-message]
    router[persona-router]
    system[persona-system]
    harness[persona-harness]
    wezterm[persona-wezterm]
    orchestrate[persona-orchestrate]
    persona[persona integration]
    store[(redb + rkyv)]

    human --> desktop
    desktop --> router
    message --> router
    router --> system
    router --> harness
    harness --> wezterm
    router --> store
    harness --> store
    orchestrate --> store
    persona --> message
    persona --> router
    persona --> system
    persona --> harness
    persona --> orchestrate
```

The public component repos now exist:

| Repository | Role |
|---|---|
| `persona-message` | message contract, `message` CLI, typed NOTA boundary |
| `persona-router` | pending queue, delivery reducer, subscriptions, actor routing |
| `persona-system` | OS/window/input event contracts; first Niri backend lives here |
| `persona-harness` | harness identity, lifecycle, transcript and input observers |
| `persona-wezterm` | current PTY/window adapter used by the live harness tests |
| `persona-orchestrate` | typed successor to workspace claim/handoff coordination |
| `persona` | integration surface and high-level architecture |

`persona-system-niri` is intentionally not created yet. Niri stays inside
`persona-system` until a second backend makes the split real.

`persona-desktop` is intentionally deferred. The desktop composer becomes
useful after the router can deliver safely and expose status.

---

## Layering

The critical next step is a working delivery path:

```mermaid
flowchart LR
    sender[agent or human client]
    cli[message CLI]
    router[RouterActor]
    target[HarnessActor]
    gate[DeliveryGate]
    system[SystemEventSource]
    input[InputBufferActor]
    endpoint[EndpointActor]
    harness[interactive harness]

    sender --> cli
    cli --> router
    router --> target
    target --> gate
    gate --> system
    gate --> input
    target --> endpoint
    endpoint --> harness
```

The boundary between text and durable state is explicit:

```mermaid
flowchart LR
    nota[NOTA text]
    typed[typed domain value]
    reducer[domain reducer]
    archive[rkyv archived value]
    redb[(redb table)]
    projection[NOTA projection]

    nota --> typed
    typed --> reducer
    reducer --> archive
    archive --> redb
    redb --> projection
```

NOTA remains the human-facing and harness-facing text format. It is not the
production queue store. Persistent component state is redb tables with
rkyv-archived values.

---

## The router's job

`persona-router` owns the harness delivery plane. It accepts typed messages,
records their state, asks the target harness actor to attempt delivery, and
subscribes to exactly the event sources that can unblock deferred work.

```mermaid
stateDiagram-v2
    [*] --> Accepted
    Accepted --> Pending: stored
    Pending --> GateCheck: attempt
    GateCheck --> Delivered: safe delivery
    GateCheck --> WaitingForFocus: target focused
    GateCheck --> WaitingForInput: input buffer occupied or absent
    GateCheck --> WaitingUnknown: no authoritative state
    WaitingForFocus --> GateCheck: FocusChanged target unfocused
    WaitingForInput --> GateCheck: InputBufferChanged empty
    WaitingUnknown --> Expired: DeadlineExpired
    WaitingForFocus --> Expired: DeadlineExpired
    WaitingForInput --> Expired: DeadlineExpired
    Delivered --> [*]
    Expired --> [*]
```

The router never polls. It wakes because:

| Wake source | Producer | Why it wakes |
|---|---|---|
| message accepted | `message` CLI or future client | new delivery work exists |
| focus changed | `persona-system` Niri event stream | a focus block may have cleared |
| input buffer changed | `persona-harness` recognizer | an input block may have cleared |
| deadline expired | OS timer primitive | a pending message TTL ended |
| manual discharge | human command | user explicitly resolves a block |

There is no retry timer for `WaitingUnknown`. Unknown stays queued until an
authoritative event, manual discharge, or TTL expiry.

---

## Safe delivery gate

The gate is about protecting input state, not about whether the model is
currently generating tokens. The agent's "idle" state is not a delivery
condition.

```mermaid
flowchart TD
    msg[pending message]
    focus{human focuses target?}
    buffer{target input buffer empty?}
    deliver[deliver]
    queue[queue]

    msg --> focus
    focus -->|yes| queue
    focus -->|unknown| queue
    focus -->|no| buffer
    buffer -->|yes| deliver
    buffer -->|no| queue
    buffer -->|unknown| queue
```

The first gate has two green requirements:

| Requirement | Meaning |
|---|---|
| target not focused | the human is not typing into that harness window |
| input buffer empty | the harness has a visible editable input region, and it contains only prompt chrome |

If the harness is generating output, there may be no editable input region. That
counts as not empty or unknown, so the message stays queued. This protects the
same user-visible state without naming token-generation idle as a separate
condition.

---

## Input-buffer definition

"Empty input buffer" is a two-predicate observation owned by the harness side:

```mermaid
flowchart TD
    screen[terminal screen model]
    present{input buffer present?}
    chrome{only prompt chrome?}
    empty[InputBufferEmpty]
    blocked[InputBufferBlocked]

    screen --> present
    present -->|no| blocked
    present -->|unknown| blocked
    present -->|yes| chrome
    chrome -->|yes| empty
    chrome -->|no or unknown| blocked
```

Per-harness recognizers are closed over the supported harness variants:

| Harness | First recognizer target |
|---|---|
| Pi | prompt box and editable line region |
| Claude | bottom `>` input line |
| Codex | `>` marker and editable row |

The recognizer emits `InputBufferChanged(target, state)` only when it has a new
authoritative observation. The router does not sample the screen on a clock.

---

## System abstraction

`persona-system` owns the portable system event surface. The current system is
Niri/CriomOS; that is not a blocker because Persona is being built with its own
operating-system substrate. Ports implement the same surface with whatever
support their system can offer.

```mermaid
flowchart LR
    system[persona-system]
    niri[Niri backend]
    mac[future macOS backend]
    x11[future X11 backend]
    compositor[future Persona compositor]

    system --> niri
    system --> mac
    system --> x11
    system --> compositor
```

The event surface stays small:

| Event | Meaning |
|---|---|
| `FocusChanged(target, focused)` | target window focus changed |
| `WindowClosed(target)` | bound target window disappeared |
| `InputBufferChanged(target, state)` | harness input-buffer state changed |
| `DeadlineExpired(id)` | OS deadline fired |

Niri gives a real push source through its IPC event stream. The router opens the
stream only when pending focus-blocked work exists and closes it when no pending
focus block remains.

```mermaid
sequenceDiagram
    participant R as RouterActor
    participant F as NiriFocusSource
    participant H as HarnessActor

    R->>H: AttemptDelivery(message)
    H-->>R: Deferred(blocked_on_focus)
    R->>F: ensure subscribed
    F-->>R: FocusChanged(target, false)
    R->>H: AttemptDelivery(message)
    H-->>R: Delivered or Deferred(next reason)
    R->>F: unsubscribe when no focus-blocked targets remain
```

On systems without a push-capable focus source, focus-gated delivery is
unavailable. The correct behavior is deferral, not a fallback poll.

---

## Window binding and races

Harness identity is not a title string. The harness actor owns the explicit
binding between a Persona harness and a system window or terminal endpoint.

```mermaid
flowchart LR
    target[HarnessTarget]
    binding[HarnessBinding]
    window[SystemWindowId]
    endpoint[Endpoint]

    target --> binding
    binding --> window
    binding --> endpoint
```

Niri window IDs are stable only for the lifetime of a window. When the window
closes, the harness actor emits `BindingLost(target)`. Pending messages stay
queued until explicit rebind, manual discharge, or TTL expiry. App id and title
are discovery hints, not identity.

The minimal gate narrows the human-input race but does not eliminate it:

```mermaid
sequenceDiagram
    participant R as Router
    participant H as Harness
    participant W as Window
    participant U as Human

    R->>H: AttemptDelivery
    H->>W: observe unfocused + empty
    U-->>W: could focus/type before write
    H->>W: terminal injection
```

The destination design reduces this further through a system-level delivery
primitive: focus leasing, compositor support, a Persona-owned prompt composer,
or a harness-side extension/API. Until then, the router must treat focus and
input-buffer uncertainty as a queueing reason.

---

## Human prompt composer

The long-term answer is not to make the human type directly into a harness
prompt when routed messages may arrive. Persona needs a human-facing message
composer.

```mermaid
flowchart LR
    human[human]
    composer[Persona composer]
    router[persona-router]
    harness[HarnessActor]
    terminal[interactive harness]

    human --> composer
    composer --> router
    router --> harness
    harness --> terminal
```

The composer gives the human a stable editor and turns the draft into a Persona
message. That keeps all deliveries serialized by the router and avoids splicing
router text into a half-typed human prompt. This belongs to the deferred
`persona-desktop` work, not the first router implementation.

---

## Actor ownership

Actors own data; methods live on the object with the data.

```mermaid
flowchart TB
    router[RouterActor]
    harness[HarnessActor]
    focus[SystemFocusActor]
    input[InputBufferActor]
    deadline[DeadlineActor]
    endpoint[EndpointActor]

    router <--> harness
    router <--> focus
    router <--> deadline
    harness <--> input
    harness <--> endpoint
```

| Actor | Owns |
|---|---|
| `RouterActor` | pending deliveries, block reasons, subscriptions, delivery transitions |
| `HarnessActor` | target identity, window/endpoint binding, current gate observations |
| `SystemFocusActor` | OS event subscription and focus map |
| `InputBufferActor` | parsed screen/input-region observations |
| `DeadlineActor` | OS-pushed TTL deadlines |
| `EndpointActor` | adapter-specific delivery channel |

There is no `StorageActor`. Each domain actor writes its own redb tables. If a
cross-table transaction becomes real, introduce a typed transaction value or a
narrower domain object, not a generic storage dispatcher.

---

## Message flow

The immediate live test should look like this, without telling the receiving
agent what to do in its startup prompt:

```mermaid
sequenceDiagram
    participant T as Test
    participant A as Initiator harness
    participant M as message CLI
    participant R as Router
    participant B as Responder harness
    participant O as Operator harness

    T->>A: train on message skill and endpoint names
    T->>B: train on message skill and endpoint names
    B->>M: Send operator responder-ready
    A->>M: Send operator initiator-ready
    T->>A: user message: ask responder for status
    A->>M: Send responder status request
    M->>R: typed message
    R->>B: gated delivery
    B->>M: Send initiator reply
    M->>R: typed message
    R->>A: gated delivery
    A->>M: Send operator received-reply
    M->>R: typed message
    R->>O: delivered to operator endpoint
```

Two points are non-negotiable:

- agents do not create message IDs; the daemon/router does;
- the operator endpoint must be a real route, not a shell-call return value.

The old NOTA-line prototype helped prove syntax and live harness behavior, but
the next test should route through the daemon/router and inject through the same
delivery gate used for all harnesses.

---

## Implementation order

```mermaid
flowchart TD
    repos[component repos scaffolded]
    msg[stabilize persona-message daemon protocol]
    ids[daemon-owned short message IDs]
    router[persona-router reducer and queue]
    store[redb + rkyv router store]
    system[persona-system Niri focus source]
    harness[persona-harness input-buffer fixtures]
    gate[delivery gate tests]
    live[live Pi/Codex/Claude routed test]
    desktop[deferred Persona composer]

    repos --> msg
    msg --> ids
    ids --> router
    router --> store
    router --> system
    router --> harness
    system --> gate
    harness --> gate
    gate --> live
    live --> desktop
```

First concrete tasks:

1. Move `persona-message` from the NOTA-line prototype toward a daemon-backed
   route: the CLI submits to a Unix socket; the daemon stamps the ID and returns
   an accepted/delivered/queued result.
2. Define the router command/result envelope. Use rkyv for CLI-to-daemon binary
   frames when the route is local; keep NOTA for harness text and audit
   projections.
3. Implement `persona-router`'s reducer with fake system and harness event
   sources first.
4. Add redb + rkyv storage for pending deliveries and delivery transitions.
5. Implement the first `persona-system` Niri focus source behind the generic
   event interface.
6. Implement fixture-driven input-buffer recognizers in `persona-harness`.
7. Re-run live harness tests only after the gate has fake-source coverage.

---

## Tests to land before live harness runs

```mermaid
flowchart LR
    nota[NOTA examples]
    daemon[daemon protocol tests]
    reducer[router reducer tests]
    focus[Niri fixture tests]
    input[input-buffer fixture tests]
    live[live visible harness test]

    nota --> daemon
    daemon --> reducer
    reducer --> focus
    reducer --> input
    focus --> live
    input --> live
```

| Test | Expected result |
|---|---|
| CLI sends without ID | daemon assigns short ID |
| CLI names unknown recipient | typed rejection |
| target focused | message queued with `blocked_on_focus` |
| unrelated focus change | target queue untouched |
| target unfocused but input occupied | queued with `blocked_on_non_empty_input` |
| target unfocused and input empty | delivered once |
| missing focus source | queued; no fallback poll |
| window closes | `BindingLost`; pending messages remain queued or expire |
| TTL deadline fires | message becomes `Expired` without retry |
| operator endpoint receives | message appears in the operator harness, not only in test logs |

The live harness test should start with Pi because it is local and unpaid, then
repeat on Codex and Claude only after the path is stable.

---

## Decisions still needing the human

| Decision | Default recommendation |
|---|---|
| Pending-message TTL | 24 hours, configurable per harness; no infinite memory growth |
| Manual discharge command name | `message discharge <id>` or equivalent in the CLI |
| Human composer priority | defer until routed harness delivery is stable |
| Focus lease / compositor-level lock | future Persona-system work; not a blocker for the first safe gate |
| macOS/X11/Hyprland support | port later behind `persona-system`; no fallback polling |

---

## What is retired

The old operator reports captured useful discovery but are no longer the best
entry point:

| Old report | Live substance now here |
|---|---|
| `1-persona-core-state-pass.md` | reducer/state discipline, redb + rkyv direction |
| `2-terminal-harness-control-research.md` | harness node and remote-first adapter model |
| `3-persona-wezterm-harness-plan.md` | WezTerm remains an adapter, not the core truth |
| `4-persona-message-plane-design.md` | message/delivery/output/state split |
| `5-persona-message-real-harness-test-plan.md` | live harness test strategy |
| `7-minimal-niri-input-gate.md` | focus/input gate and Niri first slice |
| `8-persona-system-repo-plan.md` | repository split and implementation order |

The surviving designer reports remain useful as audit history and independent
design review. Future operator work should start here, then read the designer
reports only when it needs audit lineage.
