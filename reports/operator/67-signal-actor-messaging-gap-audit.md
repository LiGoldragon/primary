# Signal Actor Messaging Gap Audit

*Operator audit of the gap between the current Persona messaging
prototype and Li's stated communication intent.*

---

## 0. Scope

This report audits the current messaging work against the intent
restated on 2026-05-09:

- Every component-to-component message is typed.
- Components communicate through Signal: length-prefixed rkyv frames with
  portable rkyv encoding.
- Each communication channel has a contract repository that owns the
  Signal types crossing that channel.
- Components use the Actor model for asynchronous communication.
- Behavior lives on data-bearing types.
- Zero-sized types are allowed only for actor behavior markers.
- Configuration, scenario data, prompt text, and test messages live in
  configuration records or messages, not embedded in implementation code.

The audit focuses on current work in:

- `repos/signal-core`
- `repos/signal-persona`
- `repos/persona-message`
- `repos/persona-router`
- `repos/persona-system`
- `repos/persona-wezterm`
- `repos/persona-harness`
- `repos/persona-sema`

It builds on the earlier code audit in chat, but reframes every issue
against the stronger Signal + actor contract.

---

## 1. Destination Shape

Persona's runtime should have three visible planes, each with a narrow
format:

```mermaid
flowchart TB
    subgraph "text projection plane"
        human["human"] -->|"Nexus / NOTA text"| message_cli["persona-message CLI"]
        harness_terminal["harness terminal"] -->|"Nexus / NOTA text"| projection["pre-harness projection"]
    end

    subgraph "Signal actor plane"
        message_actor["message actor"] -->|"Signal frame"| router_actor["router actor"]
        router_actor -->|"Signal frame"| store_actor["store actor"]
        system_actor["system actor"] -->|"Signal event frame"| router_actor
        router_actor -->|"Signal command frame"| harness_actor["harness actor"]
        harness_actor -->|"Signal event frame"| router_actor
    end

    subgraph "durable state plane"
        store_actor -->|"rkyv values"| persona_sema["persona-sema"]
    end

    projection -->|"terminal bytes"| durable_pty["durable PTY"]
```

The only text boundary is human/agent-facing. The rest of the system
speaks typed Signal records.

The current prototype instead looks closer to this:

```mermaid
flowchart TB
    message_cli["message CLI"] -->|"NOTA line / local file"| message_log["messages.nota.log"]
    message_cli -->|"hand-built NOTA string"| router_daemon["router daemon"]
    router_daemon -->|"direct method call"| persona_wezterm["persona-wezterm"]
    router_daemon -->|"capture substring check"| pty_screen["PTY screen"]
    test_script["test shell script"] -->|"manual PromptObservation text"| router_daemon
    test_script -->|"niri command output"| router_daemon
```

The prototype proved the user-visible behavior, but it has the wrong
logic-plane shape for the durable system.

---

## 2. Load-bearing Gaps

| Gap | Current shape | Intended shape | Consequence |
|---|---|---|---|
| Router protocol | `persona-message` formats `(RouteMessage ...)` by string | shared Signal request/reply type | no typed request or reply validation |
| Durable message source | local NOTA log plus in-memory router queue | store actor commits typed transitions to `persona-sema` | delivered messages can be missing from durable state |
| Delivery side effect | router injects terminal input directly | router asks harness actor through typed channel | routing policy and terminal mechanics are coupled |
| Guard facts | shell script manually pushes prompt/focus text | system/harness actors publish typed pushed events | tests prove choreography, not runtime machinery |
| Wire format | mixed NOTA, ad hoc rkyv, raw socket tags | Signal everywhere between components | incompatible protocols multiply |
| Actor model | mostly synchronous loops and direct calls | one actor per stateful component | blocked delivery can stall unrelated traffic |
| Configuration | hard-coded actor names, prompts, timings, UI detectors | typed configuration records and scenario messages | tests train code paths instead of exercising configured behavior |
| Rust discipline | local helper functions, string dispatch, ZST commands | data-bearing types and actor-only ZSTs | model remains under-typed |

---

## 3. Signal Contract Gap

`signal-core` and `signal-persona` already contain the start of the
right architecture:

- `signal-core` owns `Frame`, `FrameBody`, `Request`, `Reply`,
  `SemaVerb`, `ProtocolVersion`, `AuthProof`, `Slot<T>`,
  `Revision`, `Bind`, `Wildcard`, and `PatternField<T>`.
- `signal-persona` owns Persona domain records: `Message`,
  `Delivery`, `Binding`, `Harness`, `Observation`, `Lock`,
  `StreamFrame`, `Transition`, and typed query records.

The live implementation mostly bypasses those crates:

- `persona-router` depends on `persona-message`, `persona-system`,
  and `persona-wezterm`; it does not depend on `signal-persona`.
- `persona-message` defines its own `Message`, `Actor`,
  `EndpointTransport`, `RouterInput`, daemon envelope, and local
  command protocol instead of submitting Signal frames.
- `persona-system` defines local `FocusObservation` records and
  renders them with hand-written NOTA strings.
- `persona-wezterm` defines an internal byte-tag protocol for PTY
  clients; that may be acceptable inside the terminal adapter, but
  it is not yet wrapped behind a typed Signal command/event channel
  when called by Persona components.

### Current Contract Duplication

```mermaid
flowchart LR
    signal_message["signal-persona::Message"] -. "not used by live CLI" .-> local_message["persona-message::schema::Message"]
    signal_observation["signal-persona::Observation"] -. "not used by live system events" .-> local_focus["persona-system::FocusObservation"]
    signal_delivery["signal-persona::Delivery"] -. "not used by live router queue" .-> local_pending["persona-router::pending Vec<Message>"]
    signal_binding["signal-persona::Binding"] -. "not used by live endpoint registry" .-> local_endpoint["persona-message::EndpointTransport"]
```

The duplication is not just cosmetic. The duplicate types disagree:

- `signal-persona::Message` contains `recipient` and `body`.
  Infrastructure mints identity and sender.
- `persona-message::schema::Message` contains `id`, `thread`,
  `from`, `to`, `body`, and attachments.

That means the prototype still lets the sending surface own values
that the intended system says infrastructure must own.

### Channel-repo Consequence

The likely repo split is:

| Channel | Contract owner | Runtime owner |
|---|---|---|
| shared Persona domain records | `signal-persona` | none; contract only |
| CLI/text ingress to router | `signal-persona-message` or a module in `signal-persona` | `persona-message` + `persona-router` |
| router to store | `signal-persona-store` or a module in `signal-persona` | `persona-router` + `persona-sema` |
| system events to router | `signal-persona-system` or a module in `signal-persona` | `persona-system` + `persona-router` |
| router to harness actor | `signal-persona-harness` or a module in `signal-persona` | `persona-router` + `persona-harness` |
| harness actor to terminal adapter | `signal-persona-terminal` or `signal-persona-wezterm` | `persona-harness` + `persona-wezterm` |

Decision needed: whether "one repository per channel" means a physical
repo per row above, or whether `signal-persona` can hold submodules for
closely related channels until a channel grows enough to split. The
important invariant is single ownership of each wire type. The current
state violates that invariant either way.

---

## 4. Actor-model Gap

The current code has some actor-shaped naming, but the live messaging
path is not an actor system.

```mermaid
flowchart TB
    listener["UnixListener loop"] -->|"read one line"| apply["RouterActor::apply"]
    apply -->|"direct call"| deliver["HarnessActor::deliver"]
    deliver -->|"direct call"| send_prompt["PtySocket::send_prompt"]
    send_prompt -->|"sleep + enter"| pty["PTY"]
```

The intended shape is:

```mermaid
flowchart TB
    router_actor["RouterActor"] -->|"RouteMessage frame"| store_actor["StoreActor"]
    store_actor -->|"CommitOutcome frame"| router_actor
    system_actor["SystemActor"] -->|"Observation frame"| router_actor
    router_actor -->|"Deliver frame"| harness_actor["HarnessActor"]
    harness_actor -->|"TerminalCommand frame"| terminal_actor["TerminalActor"]
    terminal_actor -->|"DeliveryReceipt frame"| harness_actor
    harness_actor -->|"DeliveryEvent frame"| router_actor
```

Current gaps:

1. `persona-router` has `RouterActor` and `HarnessActor` as ordinary
   structs, not ractor actors. They do not own async mailboxes,
   supervision, or concurrent delivery state.
2. `RouterDaemon::run` handles connections sequentially. A slow terminal
   capture or injected sleep blocks all other router traffic.
3. The harness endpoint is an in-memory field inside the router, but the
   delivery action is still a direct method call into terminal transport.
4. `persona-wezterm` has a `TerminalDeliveryActor`, but router delivery
   does not use it in the PTY path. The PTY daemon path is thread-based
   and frame-based, not actor-supervised.
5. The system focus source is a synchronous object that can subscribe to
   Niri events, but there is no long-lived system actor publishing typed
   Signal observation frames to the router.

The durable design needs actors at the components whose state persists
across time:

- `MessageIngressActor`
- `RouterActor`
- `StoreActor`
- `SystemObservationActor`
- `HarnessActor`
- `TerminalAdapterActor`
- `TranscriptActor`

Each actor's message enum belongs in the matching Signal contract repo.
Each actor's runtime state belongs in the component repo.

---

## 5. Wire-format Gap

`signal-core` uses the right rkyv discipline:

- rkyv 0.8
- `default-features = false`
- `std`, `bytecheck`, `little_endian`, `pointer_width_32`,
  `unaligned`
- 4-byte big-endian length prefix
- bytechecked decode

Several live paths deviate.

### `persona-message`

`persona-message` depends on `rkyv = "0.8"` without the canonical
portable feature set. Its daemon uses an ad hoc `DaemonEnvelope` and
`DaemonFrame`, not `signal_core::Frame`.

`DaemonFrame` also uses a little-endian length prefix:

- read: `u32::from_le_bytes`
- write: `to_le_bytes`

That conflicts with `signal-core`'s big-endian frame prefix and makes
the daemon protocol a different wire.

### `persona-router`

`persona-router` currently reads one NOTA line from a Unix socket and
decodes local `RouterInput` records. This is useful for manual testing,
but it is not Signal.

### `persona-wezterm`

`persona-wezterm` PTY control uses byte tags:

- `H` for handshake
- `I` for input
- `R` for resize

That may remain an internal terminal-adapter protocol, but Persona
components should not call it as their communication channel. The
router should speak Signal to a harness or terminal actor; the terminal
actor can translate to the PTY daemon's private byte protocol.

---

## 6. Correctness Gaps

### 6.1 Delivery can duplicate after side effect

`persona-router` injects the prompt, then sleeps, captures output, and
returns `false` if capture evidence is missing. `retry_pending` keeps
that message pending and can later inject it again.

The type system should model delivery as a state transition:

```mermaid
stateDiagram-v2
    [*] --> Queued
    Queued --> Blocked: guard rejects
    Queued --> Injecting: guard accepts
    Injecting --> SentUnconfirmed: input side effect accepted
    SentUnconfirmed --> Delivered: harness ack or observed receipt
    SentUnconfirmed --> NeedsAudit: receipt missing
    Blocked --> Queued: pushed observation changes
```

Capture failure after input side effect is not "not delivered." It is
`SentUnconfirmed` or `NeedsAudit`.

### 6.2 Router accepts stale facts

The router stores `focus: Option<bool>` and `prompt: PromptFact`.
Prompt facts have no source, generation, observed-at value, or target
revision. Focus has a generation in the system record, but the router
does not enforce a freshness relation between guard check and injection.

The intended guard should be a typed fact record committed by the
system/harness actor, then consumed atomically by delivery logic:

```text
Observation { target, kind, generation, observed_by, value }
DeliveryAttempt { delivery, guard_generation, effect_state }
```

### 6.3 Human messages are not durable router state

The router treats `human` endpoints as delivered and returns `true`.
That is acceptable only if another layer has already persisted the
message and the human inbox projection. In the current code, router
state is in-memory and the CLI append order can lose audit state after
route success.

### 6.4 Unknown actors remain pending without a typed reason

Messages to unknown actors stay in `pending`, but the pending item does
not carry `Blocked(BindingLost)` or equivalent Signal state. The router
cannot distinguish "wait for later registration" from "bad recipient"
or "lost binding."

### 6.5 PTY write failure can be invisible

The PTY daemon ignores write and resize errors in the input thread.
That lets upper layers believe a write completed when the terminal
transport failed. The terminal actor must return a typed receipt or
typed failure.

---

## 7. Logic-plane Separation Gaps

The intended ownership boundary is:

| Plane | Owner | What crosses |
|---|---|---|
| domain vocabulary | `signal-persona` | rkyv record types |
| CLI text projection | `persona-message` | Nexus/NOTA text at human/harness boundary |
| routing policy | `persona-router` | typed route/delivery decisions |
| durable commits | `persona-sema` | typed transitions into redb |
| OS/window facts | `persona-system` | typed pushed observation frames |
| harness lifecycle | `persona-harness` | typed harness events and commands |
| terminal bytes | `persona-wezterm` | raw PTY/WezTerm mechanics only |

Current violations:

1. `persona-message` owns message schema, local store, sender
   resolution, router client, daemon protocol, delivery gate, and
   terminal delivery. That is multiple planes in one repo.
2. `persona-router` imports `persona-wezterm` and directly injects
   terminal prompts. Routing policy and terminal mechanics are coupled.
3. `persona-system` renders facts as NOTA strings and is called from a
   shell test. It should publish typed system facts through a Signal
   subscription.
4. `persona-wezterm` exports semantic `TerminalPrompt` and
   `DeliveryReceipt` types. That is tolerable as adapter vocabulary, but
   Persona message semantics should live above it.
5. `persona-message` and `persona-router` both carry delivery behavior.
   There should be one delivery policy owner.

The corrective rule: every cross-component call should be replaced by a
typed actor message over a Signal channel. Direct Rust calls remain only
inside one component's internal implementation.

---

## 8. Data Embedded In Code

The current prototype has too much scenario data and policy data in code
or shell scripts.

### Test scenario data

`scripts/test-pty-pi-router-relay` embeds:

- actor names: `initiator`, `responder`, `operator`
- model default: `prometheus/qwen3.6-27b`
- thinking default: `medium`
- skill file path
- readiness bodies: `responder-ready`, `initiator-ready`
- request/reply bodies: `relay-reply`, `relay-complete`
- guard bodies: `relay-focus-guard`, `relay-prompt-guard`
- UI readiness detector: model label plus `0.0%/131k`
- terminal dimensions: 32 rows, 120 columns
- wait loop counts and sleep intervals
- Niri app-id strings

Those should become a typed scenario/configuration record:

```text
HarnessRelayScenario {
  participants,
  model_profile,
  skill_projection,
  messages,
  guard_cases,
  observation_sources,
  terminal_geometry
}
```

The script should load the scenario and drive actors. The data should not
be the script.

### Runtime policy data

Embedded runtime policy includes:

- router evidence length: first 24 characters of a message
- router delivery wait: 1000 ms
- PTY send waits: 3000 ms before enter, 1000 ms after enter
- WezTerm pane delivery wait: 500 ms
- PTY capture read timeout: 80 ms
- PTY capture deadline: 800 ms
- resize polling interval: 250 ms
- scrollback limit: 8 MiB
- default socket paths under `/tmp`
- default PTY size 32 x 120
- string endpoint kinds: `human`, `pty-socket`, `wezterm-pane`

Some of these are adapter defaults, but they still need to be named data
on configuration types. Timing heuristics should not be hidden inside
delivery methods.

### Prompt and training text

Agent instructions are currently injected as literal text in the shell
test. The desired shape is:

- skill/training text is a configured projection artifact;
- the message body carries the task;
- the harness actor receives typed delivery work;
- the terminal adapter only renders the projection.

---

## 9. Rust-style Gaps

### 9.1 ZST rule conflict

The new "ZST only for actors" rule conflicts with several current
types:

- `signal_core::Bind`
- `signal_core::Wildcard`
- `persona-message::Tail`
- `persona-message::Agents`
- `persona-message::Flush`
- `persona-router::Status`

This needs a design decision. `Bind` and `Wildcard` were deliberately
made typed marker records after the Nexus grammar rewrite. If the new
rule is absolute, they need a different representation. If typed marker
records are still allowed, the rule should say "actor behavior markers
and schema marker records" rather than "only actors."

### 9.2 Free helper functions remain

Examples:

- `persona-message::schema::expect_end`
- `persona-message::resolver::parent_process`

They are small, but they still indicate missing owner types:

- `NotaInput` or `InputDecoder` should own end-of-input validation.
- `ProcessAncestry` should own parent lookup through a `ProcessTable`
  or `ProcessSource` object.

### 9.3 Stringly dispatch remains

Examples:

- endpoint kind dispatch in `persona-router`
- endpoint kind dispatch in `persona-message`
- `PromptFact` encoded as strings
- `RouterInput` decoded by record-head string
- system observations rendered manually into NOTA text

Closed enums in Signal contracts should replace string branches at
component boundaries.

### 9.4 Rkyv portable feature set is not universal

`signal-core`, `signal-persona`, and `persona-sema` use the canonical
rkyv feature set. `persona-message` uses plain `rkyv = "0.8"` for its
daemon envelope. That creates a second archive dialect.

### 9.5 Data-bearing actor split is incomplete

The actor ZST pattern should look like:

```text
RouterActor       ZST behavior marker
RouterState       data owned across time
RouterArguments   boot configuration
RouterMessage     typed mailbox protocol
```

The current `RouterActor` is a data-bearing struct, not an actor
behavior marker. The current `HarnessActor` is also a data-bearing
struct nested inside the router, not a separately supervised actor.

---

## 10. Repository Gap

The repo set is close, but the dependency direction is still wrong.

### Current problematic dependencies

```mermaid
flowchart LR
    persona_router["persona-router"] --> persona_message["persona-message"]
    persona_router --> persona_wezterm["persona-wezterm"]
    persona_message --> persona_system["persona-system"]
    persona_message --> persona_wezterm
```

These dependencies make text/terminal components visible inside routing
and message construction.

### Intended dependency direction

```mermaid
flowchart LR
    signal_core["signal-core"] --> signal_persona["signal-persona"]
    signal_persona --> persona_message["persona-message"]
    signal_persona --> persona_router["persona-router"]
    signal_persona --> persona_system["persona-system"]
    signal_persona --> persona_harness["persona-harness"]
    signal_persona --> persona_sema["persona-sema"]
    persona_router --> persona_harness
    persona_router --> persona_sema
    persona_harness --> persona_wezterm["persona-wezterm"]
```

The router may depend on harness abstractions, not terminal bytes. The
message CLI may depend on Signal contracts, not delivery mechanics.

If channel-specific repos are introduced, they sit between
`signal-persona` and the paired runtime components:

```mermaid
flowchart TB
    signal_core["signal-core"] --> signal_persona["signal-persona"]
    signal_persona --> signal_persona_router["signal-persona-router"]
    signal_persona --> signal_persona_system["signal-persona-system"]
    signal_persona --> signal_persona_harness["signal-persona-harness"]
    signal_persona --> signal_persona_store["signal-persona-store"]

    signal_persona_router --> persona_router["persona-router"]
    signal_persona_system --> persona_system["persona-system"]
    signal_persona_harness --> persona_harness["persona-harness"]
    signal_persona_store --> persona_sema["persona-sema"]
```

---

## 11. Migration Consequence

The current prototype should be treated as a test harness that proved:

1. visible Pi harness windows can be spawned;
2. harnesses can learn a message CLI skill;
3. the first agent can message a second agent;
4. the second can reply;
5. the first can report completion to the operator;
6. focus/prompt guards can block injection when manually fed facts.

It should not be treated as the implementation architecture.

The next implementation pass should invert the dependency shape:

1. Define the Signal contract for message ingress, delivery state,
   observations, and harness commands.
2. Make `message` submit a typed Signal frame to a router actor.
3. Make the router actor commit message/delivery records through
   `persona-sema` before delivery effects.
4. Make system and harness actors push observation frames into the
   router.
5. Make router delivery create typed `DeliveryAttempt` records.
6. Make harness actors translate delivery attempts into terminal adapter
   commands.
7. Keep terminal adapter byte protocols internal to `persona-wezterm`.
8. Rebuild the live Pi relay test as a configuration-driven actor test,
   with its scenario data in typed records.

---

## 12. Decisions To Bring Forward

1. **ZST rule.** Confirm whether `Bind` and `Wildcard` must stop being
   zero-sized marker records, or whether schema marker records are a
   named exception beside actor behavior markers.
2. **Channel repo granularity.** Confirm whether each channel gets a
   physical `signal-persona-*` repo immediately, or whether
   `signal-persona` can own channel modules until the second concrete
   consumer forces a split.
3. **Text language at harness boundary.** Confirm whether harness-visible
   prompts are rendered as Nexus text, NOTA records, or a named Persona
   projection language while models are still text-trained.
4. **Store ownership.** Confirm that `persona-sema` is the only durable
   state writer and the router never owns a private durable queue.
5. **Terminal adapter protocol.** Confirm whether `persona-wezterm`'s
   private PTY byte protocol can stay internal, with Signal only at the
   harness actor boundary.

---

## 13. Bottom Line

The current prototype is useful evidence, not the architecture. It proved
that real harnesses can exchange messages under scripted guard conditions.
It did not yet implement the core Persona rule:

> every component boundary is a typed Signal channel between actors.

The largest gap is not one bug. It is a layering inversion: the current
message path lets text, files, terminal bytes, and routing state touch
each other directly. The intended system inserts typed Signal contracts
and actors between every one of those concerns.

The next code pass should therefore start with contracts and actor
mailboxes, not by patching more behavior into the current line-oriented
router.
