*Kind: Design · Topic: EffectEmitted payload + public-traffic routing during cutover · Date: 2026-05-22*

# 154 — EffectEmitted payload + public-traffic routing — explanation + designs

*Per psyche 2026-05-22: "explain" + "get in the details" + "show
both of those with visuals of problems and offered designs". Both
questions are open from /152 + /153.*

**Status update 2026-05-23:** Both questions RATIFIED. Part 1
EffectEmitted = Design D (tier-based default — authority-tier
`SemaObservation`, component-local typed `Effect`) ratified
implicitly via intent 244 (three-tier signal sizing) + 251 (adopt
Part 1 leans). Part 2 public routing = Design D (Persona-orchestrated
FD handoff via SCM_RIGHTS) ratified via intent 252; Design C
(client-side discovery) rejected via intent 246. Beads filed:
`primary-l02o`, `primary-bg9l`, `primary-b86d`, `primary-2py5`,
`primary-ezzp`, `primary-x5ba`, `primary-ak4g`. Carry-forward
issues remain on Mirror payload typing + Read semantics during
handover — see `reports/second-designer/158-...` for the live
status of those.

# Question 1 — `EffectEmitted` payload type

## §1.1 The problem

Every component triad working contract carries an **observable
block** — a typed observation stream that consumers subscribe to in
order to follow what the daemon is doing. The block has TWO event
families:

- **`OperationReceived`** — fires when the daemon accepts an
  operation (the request half of the request/reply pair); carries
  the operation discriminator
- **`EffectEmitted`** — fires when the daemon applies an effect (a
  state change visible to the outside world); carries SOME payload
  describing what changed

The open question is **what kind of payload `EffectEmitted` carries**.
Around seven pending observable blocks are waiting on this decision
— `signal-persona-mind`, `signal-persona-router`,
`signal-persona-message`, `signal-persona-introspect`,
`signal-persona-system`, `signal-persona-terminal`,
`signal-persona-harness` — each one designed but blocked on the
payload type. The just-landed `owner-signal-version-handover`
contract picked `SemaObservation`, which forces the question.

```mermaid
flowchart LR
    subgraph Component["Component daemon (mind / router / message / …)"]
        Op["Operation request<br/>(typed, contract-defined)"]
        Effect["Internal effect<br/>(state change)"]
        Op --> Effect
    end

    subgraph Observable["observable {} block"]
        OR["OperationReceived<br/>(discriminator known)"]
        EE["EffectEmitted<br/>(payload TYPE OPEN)"]
    end

    Op -.->|"echo"| OR
    Effect -.->|"echo"| EE

    Consumer["Subscriber<br/>(persona-introspect, log, monitor)"]
    OR --> Consumer
    EE -.->|"???"| Consumer

    style EE fill:#fee,stroke:#a44,stroke-width:2px
```

The question isn't whether observers exist — they do. It's what
they SEE on the effect side.

## §1.2 Why the question is load-bearing

Three forces pull in different directions:

```mermaid
flowchart TB
    Q["EffectEmitted payload"]

    Q --> A["Pull 1: domain detail<br/>(component knows what changed precisely;<br/>BeadCreated, GrantIssued, MessageDelivered, …)"]

    Q --> B["Pull 2: cross-component uniformity<br/>(observer wants one shape across mind+router+…;<br/>persona-introspect aggregates everything)"]

    Q --> C["Pull 3: lossy projection cost<br/>(translating BeadCreated to SemaObservation<br/>loses bead id, fields, etc.)"]

    A -.->|"favours"| Typed["typed Effect enum<br/>(component-local)"]
    B -.->|"favours"| Sema["SemaObservation<br/>(universal sema-classified)"]
    C -.->|"costs"| Sema

    style Q fill:#fff8dc
```

If every observer needs domain detail, the typed `Effect` wins. If
every observer aggregates across components, `SemaObservation` wins.
In practice **both kinds of observer exist** (persona-introspect
aggregates; a per-component dashboard reads detail), so the question
is which audience is the primary consumer.

## §1.3 The four candidate designs

### Design A — Universal `SemaObservation` everywhere

Every component's `EffectEmitted` carries `SemaObservation`. The
component picks a sema classification at emit time; domain detail
falls into a free-form `summary` string or is dropped.

```mermaid
flowchart LR
    Mind["persona-mind"] --> M_E["EffectEmitted(SemaObservation)"]
    Router["persona-router"] --> R_E["EffectEmitted(SemaObservation)"]
    Spirit["persona-spirit"] --> S_E["EffectEmitted(SemaObservation)"]

    M_E --> Introspect["persona-introspect<br/>aggregator"]
    R_E --> Introspect
    S_E --> Introspect

    Introspect --> Dash["Single dashboard<br/>(everything sema-classified)"]

    style M_E fill:#eef
    style R_E fill:#eef
    style S_E fill:#eef
```

- ✓ Uniform consumer shape across all components
- ✓ One subscription channel for cross-cutting tooling
- ✗ Loses domain detail (`BeadCreated.bead_id` becomes a string)
- ✗ Forces every component to invent a sema classification for every
  effect (cost on the producer side)

### Design B — Component-local typed `Effect` everywhere

Every component's `EffectEmitted` carries a component-local enum:
`persona_mind::Effect`, `persona_router::Effect`, etc. The contract
defines the enum; observers must know each component's vocabulary.

```mermaid
flowchart LR
    Mind["persona-mind"] --> M_E["EffectEmitted(persona_mind::Effect)"]
    Router["persona-router"] --> R_E["EffectEmitted(persona_router::Effect)"]
    Spirit["persona-spirit"] --> S_E["EffectEmitted(persona_spirit::Effect)"]

    M_E --> M_Dash["mind dashboard"]
    R_E --> R_Dash["router dashboard"]
    S_E --> S_Dash["spirit dashboard"]

    Introspect["persona-introspect<br/>aggregator"]
    M_E -. "no aggregation path" .-x Introspect
    R_E -. "no aggregation path" .-x Introspect
    S_E -. "no aggregation path" .-x Introspect

    style M_E fill:#efe
    style R_E fill:#efe
    style S_E fill:#efe
    style Introspect stroke-dasharray:5 5
```

- ✓ Full domain detail preserved
- ✓ Producer cost zero (the effect IS already typed internally)
- ✗ No aggregation path — persona-introspect would have to learn
  every component's `Effect` enum
- ✗ Adding a new component forces every observer to add a case

### Design C — Two-stream (both, separately)

Each component emits TWO observable streams: `EffectEmitted` with
typed local `Effect` AND `SemaEmitted` with `SemaObservation`. The
component does the projection once at emit time; both subscribers
get what they want.

```mermaid
flowchart LR
    Mind["persona-mind"] --> M_T["typed Effect stream"]
    Mind --> M_S["sema stream"]

    M_T --> M_Dash["mind dashboard<br/>(local detail)"]
    M_S --> Introspect["persona-introspect<br/>(sema aggregation)"]

    Router["persona-router"] --> R_T["typed Effect stream"]
    Router --> R_S["sema stream"]
    R_T --> R_Dash["router dashboard"]
    R_S --> Introspect

    style M_T fill:#efe
    style M_S fill:#eef
    style R_T fill:#efe
    style R_S fill:#eef
```

- ✓ Both audiences served
- ✓ Domain detail preserved + aggregation works
- ✗ Producer cost: every effect projected twice
- ✗ Doubles the observable surface in every contract
- ✗ Risk of skew between the two streams if projection forgets
  a case

### Design D — Tier-based default (recommended)

Two tiers of contract, each gets its natural default:

- **Authority-tier contracts** (`owner-signal-*`, cross-cutting
  contracts about other daemons' state — `owner-signal-version-handover`,
  future `owner-signal-mind` policy verbs, etc.) → `SemaObservation`
- **Component-local domain contracts** (`signal-persona-mind`,
  `signal-persona-router`, etc.) → typed component-local `Effect`

`persona-introspect` learns to read both shapes; it gets sema-classified
data from authority-tier emissions for free (because authority-tier
is small and stable) and parses domain effects per-component (one
adapter per known component, manageable count).

```mermaid
flowchart TB
    subgraph Authority["Authority-tier (small, stable)"]
        OSVH["owner-signal-version-handover"]
        OSM["owner-signal-mind (future)"]
        OSR["owner-signal-router (future)"]
        OSVH --> ATier["EffectEmitted(SemaObservation)"]
        OSM --> ATier
        OSR --> ATier
    end

    subgraph Domain["Component-local domain (numerous, varied)"]
        SM["signal-persona-mind"] --> DM["EffectEmitted(mind::Effect)"]
        SR["signal-persona-router"] --> DR["EffectEmitted(router::Effect)"]
        SS["signal-persona-spirit"] --> DS["EffectEmitted(spirit::Effect)"]
    end

    ATier --> Introspect["persona-introspect"]
    DM --> Introspect
    DR --> Introspect
    DS --> Introspect

    Introspect --> Sema_View["Cross-cutting sema view<br/>(from authority-tier + per-component adapters)"]
    DM --> Local_M["mind dashboard"]
    DR --> Local_R["router dashboard"]

    style ATier fill:#eef
    style DM fill:#efe
    style DR fill:#efe
    style DS fill:#efe
```

- ✓ Right default per tier — authority-tier is rare + cross-cutting
  (sema is right); domain is frequent + detail-rich (typed is right)
- ✓ Already matches what landed (`owner-signal-version-handover`
  picked `SemaObservation`)
- ✓ persona-introspect's effort scales with component count, not
  with effect count
- ✗ Two patterns instead of one (cost on writers)
- ✗ Edge case: a domain contract that happens to be cross-cutting
  (e.g. `signal-persona-introspect` itself) needs explicit ruling

## §1.4 Designer recommendation

**Design D — tier-based default.** Capture as Spirit Decision
(Medium certainty) so the seven pending observable blocks can move:

```text
authority-tier contracts (owner-signal-*, cross-cutting state about
other daemons) → EffectEmitted(SemaObservation)
component-local domain contracts (signal-persona-X for X being a
component daemon) → EffectEmitted(component-local typed Effect)
edge case: contracts that span both audiences default to typed
Effect and let persona-introspect adapt
```

The case is strong because:

- `owner-signal-version-handover` already chose `SemaObservation`
  and the choice fits its content
- Domain contracts emit detail-rich effects where sema projection
  is genuinely lossy
- persona-introspect's adapter count is bounded by component count
  (small), not by effect count (large)

If psyche prefers Design A (universal SemaObservation) the cost is
one-time vocabulary work in every component to express its domain
in sema terms; this is conceivable but probably not worth it.

# Question 2 — Public-traffic routing during cutover

## §2.1 The problem

A client (e.g. the `spirit` CLI, a future Mind worker) connects to
"spirit's ordinary socket". During steady state this is
`spirit-v0.1.0`'s ordinary socket; **after a cutover** it must
become `spirit-v0.1.1`'s ordinary socket. The handover protocol on
the private upgrade socket coordinates state copy; the public
**routing** is the missing piece.

Persona owns the active-version selector (snapshot table, manager
schema v4). systemd transient units own per-version process
identity (`persona-component@persona-spirit:v0.1.0.service` vs
`:v0.1.1.service`). Each component daemon binds its own
version-suffixed ordinary socket (e.g.
`~/.local/state/persona-spirit/v0.1.0/spirit.sock`).

```mermaid
flowchart LR
    Client["Client (spirit CLI)"]
    Q["???<br/>How does the client reach the ACTIVE version?"]

    subgraph Versions["systemd transient units"]
        V0["spirit v0.1.0<br/>state/persona-spirit/v0.1.0/spirit.sock"]
        V1["spirit v0.1.1<br/>state/persona-spirit/v0.1.1/spirit.sock"]
    end

    Persona["Persona<br/>(knows active = v0.1.0 now,<br/>v0.1.1 after cutover)"]

    Client --> Q
    Q -.-> V0
    Q -.-> V1
    Persona -.->|"knows answer"| Q

    style Q fill:#fee,stroke:#a44,stroke-width:3px
```

The cutover is supposed to be **atomic from the client's view** —
no client should see "neither", no client should connect to old
during the freeze window AFTER `HandoverCompleted`. The handover
protocol freezes writes on v0.1.0 and v0.1.1 picks up; the routing
question is how the *connection* swings over.

## §2.2 What's already decided

```mermaid
flowchart TB
    subgraph Settled["Already decided"]
        S1["Persona owns the active-version selector<br/>(snapshot table; intent 208/209)"]
        S2["systemd transient units own process identity<br/>(per /291 + operator/163)"]
        S3["Each version binds its own ordinary socket<br/>(version-suffixed paths)"]
        S4["Handover protocol freezes writes during cutover<br/>(signal-version-handover)"]
    end

    subgraph Open["Still open"]
        O1["What socket file does the CLIENT connect to?<br/>(unversioned, or version-discovered)"]
        O2["When the selector flips, how does the new<br/>connection land on the active version?"]
        O3["What happens to existing live connections<br/>at the moment of flip?"]
    end

    Settled --> Open

    style Settled fill:#efe
    style Open fill:#fee
```

## §2.3 The three candidate designs

### Design A — Persona-owned routing socket (proxy)

Persona binds a stable per-component socket
(`~/.local/state/persona-spirit/spirit.sock`); the file is owned by
Persona. Clients connect to this socket. Persona accepts the
connection and proxies bytes to the active version's ordinary
socket. On selector flip, new proxy connections route to the new
active.

```mermaid
sequenceDiagram
    participant C as Client (spirit CLI)
    participant P as Persona routing proxy
    participant V0 as spirit v0.1.0
    participant V1 as spirit v0.1.1

    Note over P: active = v0.1.0
    C->>P: connect ~/.local/state/persona-spirit/spirit.sock
    P->>V0: open + forward bytes
    V0-->>P: reply bytes
    P-->>C: reply bytes

    Note over P: ...handover completes, selector flips to v0.1.1...

    C->>P: connect (new connection)
    P->>V1: open + forward bytes
    V1-->>P: reply bytes
    P-->>C: reply bytes
```

- ✓ Atomic flip from client's view — new connections see new active
- ✓ Persona has live signal on every connection (could rate-limit,
  audit, gate)
- ✓ Existing connections to V0 can be drained on Persona's terms
- ✗ Latency hit per request (extra socket hop + bytes copy)
- ✗ Persona is on the data-plane path — Persona crash = traffic stop
- ✗ Persona is single-threaded by Kameo actor model; high-throughput
  components would queue behind Persona

### Design B — systemd socket activation (one stable socket, Persona swaps which unit listens)

systemd binds the public socket
(`~/.local/state/persona-spirit/spirit.sock`); the socket is owned
by a `persona-spirit.socket` unit with no specific service yet.
Persona issues `start-transient-unit` with `Sockets=persona-spirit.socket`
naming the active unit; systemd hands the listening file descriptor
to that unit. On selector flip, Persona issues `stop-unit
<old>; start-transient-unit <new> --sockets=persona-spirit.socket`
and systemd transfers the listening FD to the new unit.

```mermaid
sequenceDiagram
    participant C as Client
    participant SS as systemd socket unit<br/>(persona-spirit.socket)
    participant SD as systemd
    participant V0 as spirit v0.1.0 unit
    participant V1 as spirit v0.1.1 unit
    participant P as Persona

    Note over SS: ~/.local/state/persona-spirit/spirit.sock (LISTENING)
    Note over SD: SocketUnit owns FD<br/>actively serves to V0
    C->>SS: connect
    SS->>V0: hand off accepted connection
    V0-->>C: reply

    Note over P: selector flip starts
    P->>SD: stop-unit spirit-v0.1.0
    SD->>V0: SIGTERM (after draining)
    P->>SD: start-transient-unit spirit-v0.1.1 --sockets=persona-spirit.socket
    SD->>V1: exec, inherit FD
    Note over SS: FD now serves V1

    C->>SS: connect (new connection)
    SS->>V1: hand off
    V1-->>C: reply
```

- ✓ Atomic flip from client's view (systemd handles FD transfer)
- ✓ No data-plane proxy — bytes flow client ↔ active daemon directly
- ✓ Operating system handles connection draining + idle-timeout
- ✗ Coupling: Persona's correctness now depends on systemd unit
  behavior + socket-unit interaction
- ✗ Existing connections to V0 must drain BEFORE V1 takes the FD
  (handover protocol's freeze window plus a drain delay)
- ✗ Two-phase setup is more complex; harder to test in non-NixOS
  development sandbox

### Design C — Client-side version negotiation (CLI asks Persona, connects direct)

Client first connects to Persona's owner socket; asks "where's
spirit?"; receives `~/.local/state/persona-spirit/v0.1.0/spirit.sock`;
connects there directly. After cutover, a new client's discovery
returns `:v0.1.1/spirit.sock`. Existing connections to V0 stay
connected and drain on V0's terms.

```mermaid
sequenceDiagram
    participant C as Client
    participant P as Persona owner socket
    participant V0 as spirit v0.1.0
    participant V1 as spirit v0.1.1

    Note over P: active = v0.1.0

    C->>P: WhereIsActive(spirit)
    P-->>C: state/persona-spirit/v0.1.0/spirit.sock
    C->>V0: connect + operate
    V0-->>C: reply

    Note over P: ...selector flips to v0.1.1...

    C->>P: WhereIsActive(spirit) [new invocation]
    P-->>C: state/persona-spirit/v0.1.1/spirit.sock
    C->>V1: connect + operate
    V1-->>C: reply

    Note over C,V0: existing live connection to V0 stays<br/>until V0 drains it or client disconnects
```

- ✓ No proxy hop; bytes flow direct after discovery
- ✓ Persona is OFF the data plane — Persona crash doesn't stop
  traffic mid-connection
- ✓ Simple to test (no systemd-socket-activation surface)
- ✗ Client must talk to Persona FIRST per logical session — extra
  round-trip on connection establishment
- ✗ Client caching the discovered path = race window; client may
  reach v0.1.0 after cutover until cache invalidates
- ✗ Per-component daemons would need to coordinate their drain
  policy with Persona's selector flip to avoid client confusion
- ✗ Every client SDK needs the discovery step — couples persona-CLI
  + future-Mind + every signal client library to Persona

## §2.4 Comparison

| Concern                            | A — Persona proxy        | B — systemd socket activation     | C — Client discovery        |
|------------------------------------|--------------------------|-----------------------------------|-----------------------------|
| Atomic flip (client view)          | Yes (new connections)    | Yes (FD transfer)                 | Eventual (cache invalidation) |
| Latency overhead                   | Per-request proxy hop    | Zero after FD handoff             | One discovery round-trip per session |
| Persona on data plane              | Yes (high coupling)      | No                                | No                          |
| Persona crash = traffic stop       | Yes                      | No                                | No (for existing connections) |
| Connection drain at flip           | Persona-managed          | systemd + freeze window           | Per-component drain         |
| Test sandbox complexity            | Low                      | High (needs --user systemd)       | Low                         |
| Client SDK change cost             | None (transparent)       | None (transparent)                | One discovery step per session |
| Composes with handover freeze      | Naturally (proxy holds)  | Tightly (drain → FD swap → new bind) | Loosely (per-component)  |
| New component added                | Add per-component proxy  | Add per-component socket unit     | Add WhereIsActive variant   |

## §2.5 Designer recommendation

**Design B — systemd socket activation, with Design C as fallback
for non-systemd environments.**

The reasoning:

- Persona is already a permissioned system daemon (intent 238/239);
  systemd is the production substrate per /291 + operator/163.
  Coupling to systemd's socket-activation is natural at the
  per-component scope where systemd is already managing units.
- Zero data-plane latency once the FD is in place.
- Persona stays OFF the data plane — fault-isolation between
  Persona and individual component traffic.
- The complexity cost (FD-transfer timing) is bounded; systemd has
  proven the pattern in production.
- The non-systemd development sandbox uses `DirectProcessLauncher`
  per /291 §5 anyway — for that backend, Design C is the fallback
  (Persona returns the version-suffixed path on direct ask).

The fallback discipline keeps the development story simple while
production gets the right primitive.

If psyche prefers Design A (Persona proxy) — viable but accepts
Persona on the data plane. Reasonable if Persona's role is
explicitly broader than "supervisor" (e.g. if Persona is also
expected to gate every request).

If psyche prefers Design C universally — viable but pushes
complexity into every client SDK and accepts the cache-invalidation
race during cutover.

## §2.6 Open follow-on if Design B is chosen

```mermaid
flowchart LR
    Q1["What socket-unit lifecycle directives?<br/>(ListenStream=, SocketUser=,<br/>RemoveOnStop=, etc.)"]
    Q2["Drain protocol:<br/>how long does V0 keep serving<br/>before V1 takes the FD?"]
    Q3["Failure mode:<br/>if V1 fails to bind the FD,<br/>does V0 reclaim it?"]
    Q4["Per-version socket files still exist<br/>(daemon binds them); coexist or<br/>retire after handover?"]
    Q5["Owner socket + upgrade socket:<br/>same FD-handoff treatment or<br/>direct-bind?"]

    Q1 --> Q2 --> Q3
    Q4 --> Q5

    style Q1 fill:#fff8dc
    style Q2 fill:#fff8dc
    style Q3 fill:#fff8dc
    style Q4 fill:#fff8dc
    style Q5 fill:#fff8dc
```

Designer leans on the follow-ons:

- **Q1**: minimal directives — `ListenStream=...`, `SocketUser=persona`,
  `SocketMode=0600`. No `Accept=yes` (keep connection handling in
  the daemon).
- **Q2**: tie to handover protocol's freeze window — V0 stops
  accepting new connections at `ReadyToHandover`, drains existing
  with a configurable timeout (~5s), V1 binds the FD at
  `HandoverCompleted` minus drain timeout.
- **Q3**: V0 reclaims if V1 fails to bind within a timeout; Persona
  records the failure as an event.
- **Q4**: per-version socket files coexist short-term so the upgrade
  socket can still drive the protocol from the inactive side; retire
  the OLD version's ordinary file once `HandoverCompleted` lands.
- **Q5**: owner + upgrade sockets stay direct-bind (per-version) —
  the FD-handoff treatment is for the **public ordinary** socket
  only. Owner socket is on PERSONA, not on the component.

# §3 Combined recommendation summary

Both questions have a recommended design with the same shape: the
SETTLED system-level discipline (Persona + systemd hybrid; sema
universe for cross-cutting + typed Effect for component-local)
flows down to consistent per-contract rules.

| Question | Recommendation | Spirit capture |
|---|---|---|
| EffectEmitted payload | Design D — tier-based default | Decision (Medium certainty); authority-tier defaults to SemaObservation; component-local defaults to typed Effect |
| Public routing during cutover | Design B — systemd socket activation (production); Design C — direct discovery (dev sandbox) | Decision (Medium); follow-on Q1-Q5 per §2.6 |

Both feed the broader workspace shape captured at intent records
208 (Persona as upgrade orchestrator), 238/239 (Persona as
permissioned system daemon), and the foundation crates landed in
this session.

# §4 See also

- `reports/second-designer/152-persona-engine-architecture-overview/`
  — the meta-report context for both questions
- `reports/second-designer/153-refresh-after-prime-systemd-followups-2026-05-22.md`
  — surfaces both as open
- `reports/designer/291-persona-systemd-units-for-daemon-management.md`
  — the systemd hybrid that Design B (Q2) composes with
- `reports/operator/163-persona-systemd-component-management-position.md`
  — operator's systemd alignment
- `reports/designer/285-versionprojection-trait-and-handover-protocol-specification.md`
  — handover protocol Design B (Q2) composes with
- Spirit records 208, 209, 210, 214, 238, 239 — drivers for both
  questions
