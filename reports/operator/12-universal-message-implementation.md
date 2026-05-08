# Universal Message Implementation

Status: operator feedback report
Author: Codex (operator)

This report responds to `reports/designer/25-what-database-languages-are-really-for.md`.
It translates the language-design direction into implementation consequences for
`nexus`, `signal`, and Persona as they exist right now.

Update after `reports/designer/26-twelve-verbs-as-zodiac.md` and the user's
SEMA decision: **SEMA is the reusable database substrate**, not merely the
database behind Criome. Persona has its own Sema. The implementation question is
therefore how to make Sema reusable while allowing each Sema instance to grow
from practical string-bearing records toward a fully typed semantic database.

---

## 1 · Implementation Reading

Report 25 reframes Nexus/Signal as the universal message layer:

```mermaid
flowchart LR
    human["human or agent"]
    text["nexus text"]
    parser["translator"]
    request["typed Request"]
    database["Sema database actor"]
    reply["typed Reply"]
    renderer["renderer"]

    human --> text
    text --> parser
    parser --> request
    request --> database
    database --> reply
    reply --> renderer
    renderer --> human
```

The key implementation point is that the Sema protocol and actor protocol
become the same thing. A Sema database is a stateful actor. Its messages are
typed requests. Its replies are typed extensions, diagnostics, or subscription
events.

That means the immediate task is not "add syntax." It is to make the Rust
contract model support:

- universal verbs;
- domain-specific record kinds;
- exact text-to-type translation;
- rkyv frames for every Rust-to-Rust boundary;
- no stringly command dispatch.

---

## 2 · Current Code Shape

Current `signal` is already close in spirit but narrow in scope:

```mermaid
flowchart TB
    signal["signal"]
    request["Request"]
    edit["Assert / Mutate / Retract / AtomicBatch"]
    query["Query / Subscribe"]
    records["Node / Edge / Graph"]

    signal --> request
    request --> edit
    request --> query
    edit --> records
    query --> records
```

The current concrete state:

| Area | Current implementation | Pressure from report 25 |
|---|---|---|
| `signal::Request` | `Handshake`, `Assert`, `Mutate`, `Retract`, `AtomicBatch`, `Query`, `Subscribe`, `Validate` | Needs universal verb vocabulary and likely `Query` → `Match` naming |
| `signal::QueryOperation` | closed enum of `NodeQuery`, `EdgeQuery`, `GraphQuery` | Needs `Match`, `Project`, `Aggregate`, `Constrain`, `Recurse`, `Infer` shapes |
| `signal` record kinds | the first Sema vocabulary: `Node`, `Edge`, `Graph` | Needs reusable Sema vocabulary layering |
| `nexus::Parser` | parses text directly to `signal::Request` | Needs parser over a domain's typed vocabulary, not only sema |
| `nexus::Renderer` | renders `signal::Reply` | Needs renderer over the same domain vocabulary |
| Persona | has `signal-persona` scaffold | Should stop inventing Persona request verbs and become a domain record vocabulary |

The good news: the current code already proves the core pattern works. The bad
news: `signal` is not yet factored as a reusable universal protocol kernel. It
is both the universal envelope and the first Sema record vocabulary.

---

## 3 · The Main Refactor

The core implementation seam is this:

```mermaid
flowchart LR
    universal["universal protocol kernel"]
    domain["domain record vocabulary"]
    store["domain Sema actor"]

    universal -->|"verbs / frame / handshake / auth"| domain
    domain -->|"typed payloads"| store
```

Right now, `signal` owns both boxes. For universal messaging, it needs to split
conceptually even if the code stays in one repo at first.

The target shape:

| Layer | Owns |
|---|---|
| `signal` kernel | `Frame`, handshake, auth, protocol version, generic request/reply envelope, universal verb names |
| domain contract | record kinds, query kinds, per-verb operation enums, records reply enum |
| Sema actor | validation, redb storage, subscription fanout, inference/reduction implementation |
| nexus translator | text parser/renderer for a domain's contract |

The design question is whether `signal` becomes generic in Rust terms or
whether it remains the first Sema contract while a new `signal-core` /
`signal-kernel` crate appears.

```mermaid
flowchart TB
    option_a["Option A: generic signal crate"]
    option_b["Option B: split signal-core"]
    sema["base Sema vocabulary"]
    persona["signal-persona"]

    option_a --> sema
    option_a --> persona
    option_b --> sema
    option_b --> persona
```

My implementation preference is Option B if the current `signal` API is already
used by Criome: create or extract a kernel layer, then let the base Sema
vocabulary and Persona's Sema vocabulary depend on it. Option A is elegant but
can make rkyv bounds and derive ergonomics noisy across every type.

---

## 4 · SEMA As The Database Substrate

Sema is now the name of the database substrate. Criome has a Sema. Persona has
a Sema. Future systems can have their own Sema instances with their own domain
vocabularies.

```mermaid
flowchart TB
    kernel["signal / nexus kernel"]
    sema_core["Sema substrate"]
    criome["Criome Sema"]
    persona["Persona Sema"]
    future["future domain Sema"]

    kernel --> sema_core
    sema_core --> criome
    sema_core --> persona
    sema_core --> future
```

This changes the implementation language:

| Old wording | Correct wording now |
|---|---|
| `persona-store` as a bespoke store | Persona's Sema instance |
| sema as Criome's database | Sema as the reusable database substrate |
| domain database actor | Sema actor with a domain vocabulary |
| record graph for one daemon | typed extensions for a Sema instance |

The long-term destination is a fully typed semantic database where strings
disappear as universal containers. That is a direction, not an immediate
constraint. Early Sema records can still carry `String` fields where the
taxonomy is not ready. The correctness rule is evolutionary:

```mermaid
flowchart LR
    raw["String field"]
    newtype["validated newtype"]
    enum["closed enum"]
    lattice["typed semantic lattice"]

    raw --> newtype --> enum --> lattice
```

The implementation should therefore permit compromise without losing the
direction:

- use private wrapper newtypes around string-bearing identities;
- make obvious closed sets into enums immediately;
- record unknown or emergent taxonomy pressure as typed schema-expansion
  proposals;
- avoid stringly dispatch even when fields still contain strings.

---

## 5 · Do Not Implement Generic Records First

Report 25 includes pseudocode with `KindName` and `TypedFields`. That is useful
as explanatory compression, but it should not become the first Rust
implementation.

```mermaid
flowchart TD
    generic["KindName + TypedFields"]
    closed["closed enum per domain"]
    validator["exhaustive validator"]

    generic -. "avoid first" .-> validator
    closed --> validator
```

The current `signal` discipline is still right: each domain gets closed enums:

| Universal verb | Domain-specific payload shape |
|---|---|
| `Assert` | `SemaAssert::Node(Node)` or `PersonaAssert::Message(Message)` |
| `Mutate` | `SemaMutate::Node { slot, new, expected_rev }` |
| `Match` | `SemaMatch::Node(NodeQuery)` |
| `Records` | `SemaRecords::Node(Vec<(Slot<Node>, Node)>)` |

The universal layer names the verb. The domain layer names the record kinds.
This preserves perfect specificity and gives Rust exhaustive matches. A generic
`KindName` representation can exist later as schema-as-data or introspection,
but it should not be the primary execution wire before `prism`/schema tooling
can prove it is typed enough.

---

## 6 · Twelve Verbs As An Implementation Ladder

Report 25's 12 verbs should not all land as one large patch. They form an
ordered implementation ladder:

```mermaid
flowchart TD
    m0["M0: Assert / Mutate / Retract / Match / Validate / Atomic"]
    m1["M1: Subscribe with initial extension"]
    m2["M2: Project / Aggregate"]
    m3["M3: Constrain"]
    m4["M4: Recurse / Infer"]

    m0 --> m1 --> m2 --> m3 --> m4
```

| Milestone | Why here |
|---|---|
| M0 | Current code mostly has it; rename/reshape `Query` as `Match` after design settles |
| M1 | Push-not-pull requires subscription correctness early; default initial snapshot must be resolved |
| M2 | Projection and aggregation are common enough to shape storage APIs |
| M3 | Constrain introduces multi-pattern joins and binding scopes |
| M4 | Recurse and Infer require rule engines and termination policy |

Do not wire `Infer` or `Recurse` before the Sema actor has a clean typed
storage/query core. They are engine features, not parser features.

---

## 7 · Immediate Contradictions To Resolve

There are concrete mismatches between current code/docs and report 25:

| Issue | Current state | Needed decision |
|---|---|---|
| `Query` vs `Match` | `signal::Request::Query(QueryOperation)` and Nexus spec uses Query | Report 25 names `Match`; decide whether to rename or keep `Query` as user-facing term |
| Subscribe initial state | Current `signal` docs say no initial snapshot; report 25 says `ImmediateExtension` should default | Decide now; Persona needs initial extension to avoid poll-like reconciliation |
| Curly syntax | older Nexus spec has `{ }` and `{\| \|}`; report 25 says Project/Constrain are records | Update spec before implementation to avoid two surfaces |
| Current `signal` scope | first-Sema vocabulary and universal mechanics mixed | Extract kernel or accept a breaking refactor |
| Layered crates | `signal-forge` is skeleton design, not proof of code mechanics | Confirm how a layered domain reuses frame/handshake/auth in real Rust/rkyv |

My recommendation:

- Use `Match` in the universal model, but allow a short compatibility window if
  current code/tests are easier to update incrementally.
- Make `Subscribe` carry `InitialMode`, with `ImmediateExtension` as the
  default policy for new code.
- Remove syntax-level Project/Constrain from the live spec once record-shaped
  verbs are accepted.
- Do the kernel/domain split before Persona implements more messaging code.

---

## 8 · Persona Translation

Persona becomes a Sema instance with a domain vocabulary and effect system on
the universal message format.

```mermaid
flowchart TB
    text["nexus text"]
    gateway["nexus translator"]
    signal_persona["signal-persona"]
    sema["Persona Sema"]
    router["persona-router"]
    system["persona-system"]
    harness["persona-harness"]

    text --> gateway
    gateway --> signal_persona
    signal_persona --> sema
    sema --> router
    system --> sema
    harness --> sema
    router --> harness
```

`signal-persona` should define records, not a custom protocol:

| Record | Implementation role |
|---|---|
| `Message` | asserted by human/agent clients |
| `Delivery` | router state machine record |
| `Binding` | harness target to endpoint |
| `FocusObservation` | asserted by system backend |
| `InputBufferObservation` | asserted by harness recognizer |
| `WindowClosed` | asserted by system backend |
| `Deadline` / `DeadlineExpired` | deadline actor state and event |

Then Persona behavior is subscription-driven:

```mermaid
sequenceDiagram
    participant Store as Persona Sema
    participant Router as persona-router
    participant Harness as persona-harness

    Router->>Store: Subscribe(Match Delivery Pending)
    Store-->>Router: initial extension + deltas
    Router->>Store: Match Binding / observations
    Router->>Harness: attempt terminal effect
    Router->>Store: Mutate Delivery state
```

The message CLI becomes a thin Nexus client to Persona's Sema, not its own
language. The existing `persona-store` repository can still be the first
implementation home if renaming would create churn, but conceptually it is not
a separate storage abstraction; it is Persona's Sema actor.

---

## 9 · Nexus Implementation Shape

Nexus should become less sema-specific in the library boundary:

```mermaid
flowchart TB
    codec["nota-codec"]
    grammar["nexus grammar"]
    translator["Translator<Domain>"]
    parser["Parser<Domain>"]
    renderer["Renderer<Domain>"]
    sema["SemaDomain"]
    persona["PersonaDomain"]

    codec --> parser
    grammar --> parser
    translator --> parser
    translator --> renderer
    sema --> translator
    persona --> translator
```

The exact Rust shape needs care, but the ownership is clear:

| Type | Owns |
|---|---|
| `Parser` | token stream and top-level verb dispatch |
| `Domain` trait or generated module | map record heads to typed domain payloads |
| `Renderer` | canonical text for typed replies/events |
| daemon `Connection` actor | per-connection version/subscription state |

The parser should not become a registry of runtime strings. The domain map
should be generated or statically dispatched so adding a record kind updates:

1. the domain contract enum;
2. the parser arm for that record head;
3. the renderer arm for that record/reply shape;
4. round-trip tests.

---

## 10 · Sema Implementation Shape

Each Sema actor follows the same skeleton:

```mermaid
flowchart TB
    actor["SemaActor"]
    request["Request"]
    reducer["typed reducer"]
    tables[("redb tables")]
    subscriptions["subscription index"]
    reply["Reply"]

    request --> actor
    actor --> reducer
    reducer --> tables
    reducer --> subscriptions
    actor --> reply
```

For the first implementation, keep the engine deliberately small:

| Capability | First implementation |
|---|---|
| storage | one redb table per record kind, rkyv archives |
| identity | typed `Slot<Record>` and `Revision` |
| match | table scan plus typed field matching |
| subscribe | connection-local subscription list, immediate extension, pushed deltas |
| validate | run reducer without commit |
| atomic | one redb write transaction, ordered outcomes |
| project / aggregate | defer until match core is correct |

Indexes can wait. Correct typed semantics matter first.

---

## 11 · Concrete Next Steps

```mermaid
flowchart TD
    spec["1. Update Nexus spec to record-shaped verbs"]
    kernel["2. Extract signal kernel decision"]
    request["3. Shape Request/Reply generic or layered model"]
    sema["4. Port sema Node/Edge/Graph to the new shape"]
    persona["5. Rebase signal-persona as domain records"]
    store["6. Build Persona Sema M0"]
    gateway["7. Make message a Nexus client"]

    spec --> kernel --> request --> sema --> persona --> store --> gateway
```

Implementation order I would use now:

| Step | Repository | Output |
|---|---|---|
| 1 | `nexus` | spec report/update that commits to record-shaped Project/Aggregate/Constrain and `Subscribe` initial mode |
| 2 | `signal` | design/code spike for a reusable frame/request kernel without sema records |
| 3 | `signal` + `nexus` | rename or alias `Query`/`Match` consistently |
| 4 | `signal` | add `SubscribeQuery { pattern, initial, buffering }` or equivalent |
| 5 | `signal-persona` | replace invented request protocol with Persona Sema record kinds and per-verb payload enums |
| 6 | `persona-store` / future Sema repo | M0 Persona Sema actor: assert/match/subscribe on `Message` and `Delivery` |
| 7 | `persona-message` | CLI sends Nexus text to the translator/store path |

This keeps Persona from building on a soon-obsolete message language while
still giving it a concrete path.

---

## 12 · Decisions Needed

The implementation can move once these are settled:

| Decision | Operator recommendation |
|---|---|
| Is `Match` the new verb name, replacing `Query`? | Yes, if report 25's vocabulary is accepted; it is more precise. |
| Does `Subscribe` always send initial extension? | Yes by default, with an explicit `DeltasOnly` mode only when requested. |
| Is `signal` the universal kernel repo or does it split? | Split conceptually now; extract a crate if code pressure gets ugly. |
| Are domain records closed enums or generic `KindName` records? | Closed enums now; schema-as-data later. |
| Does Persona wait for the universal refactor? | It should pause custom protocol work and implement only record vocabulary that fits the new kernel. |
| Is Sema reusable beyond Criome? | Yes; this is now decided. Persona has its own Sema. |
| Must early Sema be string-free? | No. The direction is typed semantics; early implementation may carry strings behind typed wrappers while the taxonomy grows. |

---

## 13 · Bottom Line

Report 25 is implementable, but not as a parser expansion. The correct first
move is a contract refactor:

- preserve the current perfect-specificity pattern;
- make universal verbs independent from sema-specific records;
- let each domain provide closed record vocabularies;
- make Nexus the text projection for those typed vocabularies;
- make Sema actors receive the same typed messages they persist and
  publish.

For Persona, this means `signal-persona` becomes a record-kind crate and
`persona-store` becomes the first implementation home for Persona's Sema actor
unless the repo is renamed. The old bespoke `message` protocol should not
advance.
