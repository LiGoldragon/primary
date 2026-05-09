# Router Trained Relay Test Implementation

## Goal

Build a visible, repeatable test where trained Pi harnesses use the `message`
command themselves:

```mermaid
flowchart LR
    operator["operator"] -->|"message to initiator"| initiator["initiator"]
    initiator -->|"message request"| responder["responder"]
    responder -->|"reply"| initiator
    initiator -->|"completion"| operator
```

The important distinction from the earlier router delivery test is that only
the first instruction is injected by the test. After that, the harnesses must
use the `message` command according to their skill.

## Current Gap

The existing relay script proves agent-to-agent behavior through the old
`message-daemon` store path:

```mermaid
flowchart LR
    agent["Pi harness"] -->|"message (Send ...)"| message["message CLI"]
    message --> store["prototype NOTA ledger"]
    store -->|"direct delivery / Flush"| terminal["recipient PTY"]
```

The existing router test proves guarded delivery, but the test script sends
`RouteMessage` records directly:

```mermaid
flowchart LR
    script["test script"] --> router["persona-router"]
    router -->|"guarded delivery"| terminal["recipient PTY"]
```

The next shape combines both:

```mermaid
flowchart LR
    agent["Pi harness"] -->|"message (Send recipient body)"| wrapper["test message shim"]
    wrapper -->|"RouteMessage"| router["persona-router actor"]
    router -->|"guarded delivery"| recipient["recipient PTY"]
```

## Implementation Plan

1. Add a router-backed visible Pi relay script in `persona-message`.
2. Generate a temporary `message` shim in the test root so trained agents use
   the same command shape as the real CLI: `message '(Send recipient body)'`.
3. The shim resolves sender identity from `PERSONA_ACTOR`, mints the short
   infrastructure message id, writes an audit log, and submits
   `(RouteMessage (Message ...))` to `persona-router`.
4. Register `operator`, `initiator`, and `responder` in the router. Operator is
   a human endpoint so messages back to operator are recorded in the audit log
   without terminal injection.
5. Train initiator and responder through `skills/persona-message-harness.md`.
6. Prove the relay:
   - responder reports ready to operator;
   - initiator reports ready to operator;
   - operator sends one instruction to initiator;
   - initiator messages responder;
   - responder replies to initiator;
   - initiator reports completion to operator.
7. Prove guards in the same script:
   - focus responder, route a message, assert it remains pending;
   - unfocus via neutral window, push `FocusObservation`, assert delivery;
   - type a draft into responder, route a message, assert it remains pending;
   - clear draft, push `PromptObservation Empty`, assert delivery.

## Test Harness Shape

```mermaid
flowchart TB
    subgraph visible["visible windows"]
        init["initiator Pi"]
        resp["responder Pi"]
        neutral["neutral focus window"]
    end

    subgraph runtime["test runtime"]
        router["persona-router-daemon"]
        shim["message shim"]
        log["messages.nota.log"]
    end

    init -->|"message"| shim
    resp -->|"message"| shim
    shim -->|"append audit"| log
    shim -->|"RouteMessage"| router
    router -->|"PTY injection if safe"| init
    router -->|"PTY injection if safe"| resp
```

## State While Working

- Report created before implementation.
- Added router-aware `message` execution: when `PERSONA_ROUTER_SOCKET` is set,
  `Send` resolves the sender, builds the canonical `Message`, submits
  `(RouteMessage <Message>)` to the router socket, then appends the message to
  the local audit log.
- Added `persona-message/scripts/test-pty-pi-router-relay`.
- Added `persona-message/scripts/teardown-pty-pi-router-relay`.
- Added Nix app names for the relay setup/teardown.
- Added a named diagnostic script,
  `persona-message/scripts/debug-pty-pi-router-relay-state`, after the user
  pointed out that relay inspection also needs to go through Nix-created
  scripts rather than ad-hoc shell commands.
- First live run exposed a lower transport issue: `persona-wezterm-send`
  typed prompt text into Pi but did not reliably submit it when text and
  carriage return were sent through the same socket connection. A separate raw
  carriage return submitted correctly, so the fix belongs in `persona-wezterm`,
  not only in the relay script.
- A later run proved the relay semantics reached `initiator -> responder ->
  initiator`; the remaining failure was the initiator not reliably receiving or
  acting on the original operator router delivery. Debugging stayed inside
  `nix run .#debug-pty-pi-router-relay-state`.
- The next failure was narrower: `initiator` sent the correct message through
  `message`, but `responder` never saw the router delivery. Delivery now
  verifies that the prompt appears in PTY capture before reporting delivered;
  otherwise the router keeps the message pending for the next pushed prompt or
  focus observation.

## First Implementation Cut

The CLI path is now:

```mermaid
sequenceDiagram
    participant H as harness
    participant M as message CLI
    participant R as persona-router
    participant L as audit log

    H->>M: (Send recipient body)
    M->>M: resolve sender from process ancestry
    M->>R: (RouteMessage (Message ...))
    R-->>M: (DeliveryChanged delivered pending)
    M->>L: append canonical Message
    M-->>H: (Accepted (Message ...))
```

The relay script keeps the earlier guard tests but moves the route origin to
`message`, not hand-written router records.

## Transport Fix

`PtySocket::send_prompt` now sends prompt text and the submit carriage return as
two transport writes, with an explicit flush before socket teardown:

```mermaid
sequenceDiagram
    participant C as client
    participant D as PTY daemon
    participant P as Pi harness

    C->>D: input text
    D->>P: prompt bytes
    C->>D: input carriage return
    D->>P: submit
```

This is the same behavior that worked manually during diagnosis and it is the
path used by router delivery.

## Delivery Verification

The router path now treats "write returned Ok" as insufficient:

```mermaid
flowchart TD
    start["send prompt bytes"] --> capture["capture PTY transcript"]
    capture --> seen{"prompt visible?"}
    seen -->|"yes"| delivered["delivered"]
    seen -->|"no"| pending["defer as PromptUnknown"]
    pending --> event["next pushed observation"]
    event --> start
```

The relay script emits explicit prompt observations after each expected
handoff. They stand in for the future harness/system event stream and let the
router retry only when a producer has pushed a new fact.

## Operator-Origin Message

The original relay instruction is sent by the operator side through the
`message` CLI, not by a direct router record:

```mermaid
sequenceDiagram
    participant O as operator test process
    participant M as message
    participant R as persona-router
    participant I as initiator harness

    O->>M: (Send initiator "...")
    M->>M: resolve operator from actors.nota
    M->>R: (RouteMessage (Message ... operator initiator ...))
    R->>I: guarded PTY delivery
```

Direct router calls in the script are limited to actor registration and pushed
system facts such as `PromptObservation` and `FocusObservation`.

## Guard State Fix

The router now treats prompt state as a consumable fact:

```mermaid
stateDiagram-v2
    [*] --> Unknown
    Unknown --> Empty: PromptObservation Empty
    Empty --> Unknown: delivered message
    Unknown --> Occupied: PromptObservation Occupied
    Occupied --> Empty: PromptObservation Empty
```

This avoids reusing stale "empty prompt" knowledge. A second message to the
same harness waits until the system pushes a fresh prompt observation.

## Transport Fix Found During Test

The PTY daemon had a protocol bug: raw input clients that did not send the
viewer handshake were classified as scrollback-replay clients. The daemon could
try to replay scrollback into an input-only socket and skip the input frame if
that replay failed.

```mermaid
flowchart LR
    before["input client"] --> wrong["replay scrollback"]
    wrong --> drop["input frame skipped"]

    fixed["input client"] --> noReplay["no replay"]
    noReplay --> input["frame reaches PTY writer"]
```

The fix is in `persona-wezterm`: a client whose first byte is already an input
frame tag is marked `replay = false`.

## Passing Result

The Nix-scripted visible relay test now passes:

```text
nix run .#test-pty-pi-router-relay
pi_router_relay_test=passed
```

The passed path used two visible Pi harnesses with `prometheus/qwen3.6-27b`
and medium thinking:

```mermaid
sequenceDiagram
    participant O as operator
    participant I as initiator
    participant R as responder

    O->>I: Send responder ...
    I->>R: reply to sender with relay-reply
    R->>I: relay-reply
    I->>O: relay-complete
```

The same script then verifies both guards:

```mermaid
flowchart TD
    focus["focus responder"] --> route1["route message"]
    route1 --> pending1["pending"]
    pending1 --> unfocus["focus neutral + observe focus"]
    unfocus --> prompt1["observe prompt empty"]
    prompt1 --> delivered1["delivered"]

    draft["type human draft"] --> occupied["observe prompt occupied"]
    occupied --> route2["route message"]
    route2 --> pending2["pending"]
    pending2 --> clear["clear draft + observe empty"]
    clear --> delivered2["delivered"]
```
