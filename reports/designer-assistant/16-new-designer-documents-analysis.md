# 16 - New designer documents analysis

*Designer-assistant report. Scope: the new designer packet in
`reports/designer/114-124`, with emphasis on `116-124` as the
newly added development-plan set. Purpose: analysis, questions,
and critiques before implementation agents turn the packet into
code.*

---

## 0 - Scope

I read these designer documents as one packet:

- `reports/designer/114-persona-vision-as-of-2026-05-11.md` -
  panoramic Persona vision: federation of long-lived typed daemons;
  `persona-message` as Nexus-to-signal proxy; router owns durable
  message state.
- `reports/designer/115-persona-engine-manager-architecture.md` -
  `persona` as host-level engine manager; `ConnectionClass`,
  `EngineRoute`, privileged supervision, and component wiring.
- `reports/designer/116-persona-apex-development-plan.md` -
  development plan for the `persona` daemon and CLI.
- `reports/designer/117-persona-mind-development-plan.md` -
  development plan for `persona-mind`: event log, commit bus,
  subscriptions, and class-aware audit.
- `reports/designer/118-persona-router-development-plan.md` -
  router Sema, class-aware delivery, owner approvals, and route grants.
- `reports/designer/119-persona-system-development-plan.md` -
  OS/window/focus/input observation and privileged action surface.
- `reports/designer/120-persona-harness-development-plan.md` -
  harness daemon, harness identity, transcript fanout, adapter records.
- `reports/designer/121-persona-terminal-development-plan.md` -
  supervisor socket, named sessions, input gate, delivery state.
- `reports/designer/122-persona-message-development-plan.md` -
  stateless message proxy and retirement of local ledger / WezTerm
  vocabulary.
- `reports/designer/123-terminal-cell-development-plan.md` -
  low-level terminal-cell maturity review and remaining tests.
- `reports/designer/124-synthesis-drift-audit-plus-development-plans.md` -
  synthesis of my previous drift audit with the development plans.

## 1 - Overall Assessment

The packet is directionally strong. The biggest improvements over the
older architecture are:

- It consistently rejects made-up actor runtimes and treats Kameo as
  the Rust actor system under consideration, with data-bearing actors.
- It keeps `terminal-cell` small instead of letting the low-level PTY
  primitive grow into a second Persona architecture.
- It gives `persona-message` a clean destination: one NOTA record in,
  one signal frame to the router, one NOTA reply out, with no local
  ledger and no retired terminal-delivery code.
- It pushes every stateful component toward daemon-first, push-shaped,
  redb-backed operation.
- It makes `ConnectionClass` a real architectural axis rather than an
  incidental field.

The main risk is not lack of detail. The main risk is that several
global decisions are described in multiple places with slightly
different answers. Implementation agents will encode those differences
unless the packet gets a short "shared decisions" pass.

The high-risk unresolved decisions are:

1. Where `ConnectionClass` lives.
2. Who owns component sockets and where the engine boundary actually is.
3. Which actor owns each redb writer.
4. Whether `OtherPersona` is preserved as an audit class or downgraded
   to `System`.
5. Who owns input-buffer / prompt-cleanliness observation.
6. Whether hot-swap belongs in the first `persona` daemon build.
7. Whether contract repos are still one relation each, or are absorbing
   multiple relations because it is convenient.

## 2 - Critiques

### 2.1 `ConnectionClass` Has Already Outgrown `signal-persona`

`reports/designer/116-persona-apex-development-plan.md` says
`ConnectionClass` stays in `signal-persona` until "a second contract
domain consumes it." `reports/designer/117-persona-mind-development-plan.md`
then considers redeclaring or aliasing it in `signal-persona-mind` to
keep dependencies narrow. `reports/designer/119-persona-system-development-plan.md`,
`reports/designer/120-persona-harness-development-plan.md`,
`reports/designer/121-persona-terminal-development-plan.md`, and
`reports/designer/122-persona-message-development-plan.md` all consume
the same class concept.

That means the migration trigger has already fired. Keeping the
canonical type in `signal-persona` while the mind/system/harness/
terminal/message contracts consume it creates bad choices:

- import `signal-persona` into contracts that are not really the engine
  manager relation;
- redeclare the enum and risk drift;
- hide the class inside an opaque proof and make downstream code guess
  at projection semantics.

Recommendation: move the canonical class/auth-context vocabulary to
`signal-core` or to a narrow shared auth/identity contract now. I would
avoid redeclaration. `ConnectionClass` is infrastructure-auth context,
not a component-specific record.

Question: should the next designer edit make `ConnectionClass` a
`signal-core` type, or should there be a new small contract such as
`signal-persona-auth` for auth context and route-grant vocabulary?

### 2.2 The Engine Boundary Socket Model Needs One Answer

The packet currently implies two different socket models:

- `reports/designer/116-persona-apex-development-plan.md` says
  `ConnectionAcceptor` owns the manager socket and each engine's
  component sockets, reads peer credentials, mints `ConnectionClass`,
  and hands connections to components.
- The component plans describe each daemon as owning its own socket:
  mind accepts frames on its daemon socket, router accepts message
  frames, terminal has a supervisor socket, harness has a control
  socket, and `persona-message` connects directly to the router socket.

Both can be made to work, but not at the same time without a concrete
proxy or file-descriptor-passing design. "Persona mints the class at
the boundary" is not enough. The boundary has to be named physically.

Two viable models:

- Persona owns all listening sockets. It accepts connections, mints
  auth context, and passes accepted streams to component daemons. This
  keeps one strong engine boundary but requires explicit stream handoff.
- Components own their own sockets. Persona creates per-component
  signed auth material and socket paths in the spawn envelope; components
  read peer credentials and verify the auth proof themselves. This is
  simpler operationally, but the "engine boundary" is distributed.

Recommendation: choose the model in `reports/designer/115...` and update
all component plans to match it. My bias is the second model unless the
project really wants a central acceptor/proxy: components own their
own sockets, but the spawn envelope and signed auth proof are minted by
`persona`.

Question: does `ConnectionAcceptor` literally accept every component
connection, or does each component daemon accept its own connection and
consume auth context minted by `persona`?

### 2.3 Redb Writer Ownership Needs To Be Stricter

The plans use the right redb + rkyv direction, but several actor
topologies blur write ownership:

- `reports/designer/116-persona-apex-development-plan.md` describes
  `RouteCatalog` as holding a redb handle with a "shared transaction"
  with `EngineCatalog`.
- `reports/designer/121-persona-terminal-development-plan.md` names
  `DeliveryStateWriter`, but `NamedSessionRegistry` also appears to own
  session and health state.
- `reports/designer/117-persona-mind-development-plan.md` sometimes
  phrases `CommitBus` as if it pushes to view actors inside the same
  transaction.

The actor rule should be sharper: one database writer actor per redb
file, or one store actor that owns all writes for that file. Other actors
ask it to write. They do not share write transactions. Push fanout happens
after commit, with a durable event sequence that lets subscribers recover.

Recommendation: update `116`, `117`, and `121` so every redb file names
exactly one writer actor and one event sequence. `CommitBus` should be
"after durable commit", not "inside the transaction."

Question: should the workspace standard become "one StoreKernel /
SemaStore actor per redb file owns all writes," with domain actors only
sending typed write requests?

### 2.4 Do Not Downgrade `OtherPersona` To `System`

`reports/designer/118-persona-router-development-plan.md` says the
router may downgrade `OtherPersona` to `System` for the gate.
`reports/designer/120-persona-harness-development-plan.md` preserves
`OtherPersona` and projects it through an `EngineRoute`. `reports/designer/121-persona-terminal-development-plan.md`
keeps this as an open question.

Downgrading loses useful audit information. Another Persona instance is
not the same authority as the local Persona system principal. It may be
allowed to perform an effect because an `EngineRoute` grants that effect,
but the source class should stay visible forever.

Recommendation: carry both:

- `source_class: ConnectionClass`, for audit and provenance;
- `effective_gate_authority`, `RouteGrant`, or another typed decision
  record, for the local gate's simplified allow/reject logic.

Question: can the router and terminal plans be changed so `OtherPersona`
is never rewritten, only accompanied by a gate decision derived from an
approved `EngineRoute`?

### 2.5 Input Buffer Ownership Is Unclear

`reports/designer/114-persona-vision-as-of-2026-05-11.md` says
`persona-system` owns OS/window/input observations and pushes
`InputBufferObservation` to the router and terminal. `reports/designer/119-persona-system-development-plan.md`
says `InputBufferTracker` remains `Unknown` until the terminal source
lands. `reports/designer/121-persona-terminal-development-plan.md` makes
`persona-terminal` the owner of the input gate and the terminal byte path.

Prompt cleanliness is not really an OS observation. Focus is an OS/window
observation. Prompt/input-buffer cleanliness is terminal/harness state.
The low-level byte gate is in `terminal-cell`; the policy gate is in
`persona-terminal`; the router consumes the result.

Recommendation: make `persona-terminal` the producer of prompt/input
state, because it owns the gate and the session. `persona-system` should
produce focus/window observations and may aggregate if needed, but it
should not be the origin of terminal prompt cleanliness.

Question: is `InputBufferObservation` actually a terminal event, with
system focus joined later by the router, or is system intended to be the
aggregator of terminal state?

### 2.6 Hot-Swap Is Over-Specified For The First Daemon

`reports/designer/116-persona-apex-development-plan.md` gives a detailed
hot-swap mechanism. That may be a good eventual design, but the first
daemon still lacks the manager redb, real spawn lifecycle, class minting,
route catalog, component sockets, and health events.

There is also a concrete risk: the hot-swap section describes a v2
component opening the same redb while v1 is still running when schemas
match. If both processes can write, the design depends on redb
multi-process behavior and lock semantics that the plan does not prove.

Recommendation: move hot-swap to a later milestone after the core daemon
works. If it stays in the first plan, add a redb concurrency witness that
proves the old and new component cannot write the same redb concurrently.

Question: should the first `persona` implementation explicitly defer
hot-swap until engine catalog, spawn, health, and class minting are
already real?

### 2.7 Contract Repos Are Starting To Absorb Multiple Relations

The contract discipline says a contract repository represents a relation.
Several plans are now expanding existing contracts beyond their original
relation:

- `signal-persona-harness` starts as router-to-harness delivery, but
  plan `120` adds registration, identity query, transcript tail, lifecycle
  observation, and provider observation.
- `signal-persona-terminal` starts as harness-to-terminal control/event
  but plan `121` adds supervisor queries, delivery-state queries, and
  session health.
- `signal-persona-message` starts as message proxy-to-router ingress, but
  `Tail` would become a streamed inbox/view surface once subscriptions
  exist.
- Router owner approvals and mind notifications need event/control
  surfaces that are named in prose but not yet cleanly assigned to
  contract repos.

Some of this may be fine if the relation is explicitly broadened. But if
the relation silently broadens, the contract repo stops being an
architecture guide and becomes a bag of nearby messages.

Recommendation: add a relation-boundary pass before contract edits land.
Possible outcomes:

- keep one crate but split modules by relation and name that relation in
  ARCH;
- create sibling contracts such as `signal-persona-harness-control`,
  `signal-persona-terminal-supervisor`, or `signal-persona-router-events`;
- explicitly decide that a component-owned contract may contain multiple
  named relations and document the rule.

Question: do contract repos still mean "one relation," or are Persona
component contracts allowed to contain multiple named relations when the
component is the same?

### 2.8 Typed Nexus Body Migration Should Block Schema Hardening

`reports/designer/124-synthesis-drift-audit-plus-development-plans.md`
correctly surfaces that `MessageBody` is still opaque `String` in
`signal-persona-message` and `signal-persona-harness`, and that no plan
owns the typed-Nexus migration. This is not just a cleanup item. Router
and harness Sema schemas will soon make message bodies durable. If they
store opaque strings as the long-term shape, the migration gets more
expensive and less beautiful.

Recommendation: make the typed-Nexus body migration a prerequisite for
hardening router/harness durable message schemas, or at least add the
typed body as an additive variant before those schemas are treated as
stable.

Question: should the typed-Nexus body work be `reports/designer/125`, or
should it be folded into `reports/designer/122-persona-message-development-plan.md`
because the proxy is where Nexus text becomes signal records?

### 2.9 `persona-message` Is Strong, But Its Transitional Identity Story Is Muddy

`reports/designer/122-persona-message-development-plan.md` is one of the
cleanest plans in the packet. The stateless proxy direction is right.
There are three issues:

- The heading says `# 116 - persona-message development plan`, but the
  file is `122`. This is small, but it will confuse cross-references.
- `ActorIndex` remains as a transitional reader of `actors.nota`, while
  the plan also says the proxy owns no local files/state. That can be
  acceptable only if the retirement path is explicit and short.
- `Tail` should retire as a polling implementation, but the user-visible
  behavior should be a typed "unsupported until streaming contract" error
  or a documented absence, not a silent disappearance.

Recommendation: fix the title number, make `ActorIndex`'s retirement gate
explicit, and make `Tail`'s interim user-facing behavior explicit.

Question: where does actor identity lookup live during the short window
after local `actors.nota` is retired but before router-owned actor
registry queries exist?

### 2.10 `persona-system` Should Not Promise More Than The Backend Can Do

`reports/designer/119-persona-system-development-plan.md` names
`ForceFocus` as a privileged request. On Wayland, focus control is often
compositor-specific and sometimes intentionally limited. The plan does
mention backend limits, but the command name still sounds like a
guaranteed effect.

There is also a policy conflict: `reports/designer/115...` says non-owner
focus observation requires owner approval, while `119` says observation
requests can come from any class and policy can be handled downstream by
router policy. Sensitive observation should be guarded by the producing
daemon too, not only by a downstream consumer.

Recommendation: name the privileged action as an intervention request
with typed backend results, not a promised force. Also make
`persona-system` enforce read permissions on sensitive observations at
the source.

Question: should `ForceFocus` become `FocusIntervention` or
`FocusRequest`, with replies like `Applied`, `DeniedByBackend`,
`DeniedByPolicy`, and `NoSuchWindow`?

### 2.11 Harness Transcript Fanout Needs A Privacy Decision

`reports/designer/120-persona-harness-development-plan.md` sends
`TranscriptEventPushed` to router and mind. Its own risk section later
leans toward storing typed summaries or sequence pointers, with raw bytes
remaining in `persona-terminal`. That default should be promoted into the
main architecture.

Router probably needs delivery acks, lifecycle, and gate-relevant
observations. Mind probably needs durable activity, summaries, and audit
records. Neither should automatically receive raw transcript streams just
because a subscription is easy to add.

The same plan also keeps `HarnessKind::Other { name }` while asserting
closed-enum/no-unknown discipline. `Other { name }` is not literally
`Unknown`, but it is the same escape hatch unless its semantics are
restricted.

Recommendation: default to terminal-owned raw transcript bytes,
harness-owned typed provider observations and sequence pointers, and
class/route-gated explicit transcript subscriptions. Also decide whether
`HarnessKind::Other { name }` is temporary compatibility debt or a real
first-class variant.

Question: are router and mind meant to receive raw transcript events, or
only typed observations plus references into terminal-owned transcript
storage?

### 2.12 `terminal-cell` Restraint Is Right, But Worker Observation May Become Necessary

`reports/designer/123-terminal-cell-development-plan.md` is the clearest
boundary document in the packet. It keeps terminal-cell as a bytes-and-
frames primitive and moves Persona-shaped policy up to `persona-terminal`.
That is the right direction.

The only critique is about `WorkerObservation`. The plan says a push form
is optional until real demand appears. If `persona-terminal` needs durable
session health without polling, that demand may already exist. Snapshot
queries are fine for manual inspection; supervisor health usually wants a
subscription.

Recommendation: do not add a new cell protocol casually, but make
`persona-terminal`'s health design decide this explicitly. If terminal
will poll `WorkerObservation`, add the push form now.

Question: will `persona-terminal` observe cell lifecycle by event stream,
or will it periodically ask for `WorkerObservation` snapshots? The latter
should be rejected.

### 2.13 `reports/designer/124...` Is Useful, But It Papers Over Some Cross-Document Conflicts

The synthesis in `reports/designer/124-synthesis-drift-audit-plus-development-plans.md`
is valuable. It correctly maps my drift audit to the new development
plans and names the typed-Nexus body gap.

Its weakness is that it treats some repeated language as convergence when
the hard decision is not actually settled:

- It says `ConnectionClass` authority converges, but not where the type
  lives.
- It repeats `OtherPersona`-to-`System` downgrade from the router plan
  instead of challenging the audit/provenance loss.
- It does not mention the socket-boundary ambiguity between central
  `ConnectionAcceptor` and daemon-owned sockets.
- It does not mention redb writer ownership.
- It sequences typed-Nexus migration before construction, which is right,
  but it does not say that router/harness Sema schema hardening should
  wait for it.

Recommendation: keep `124`, but add a "shared unresolved decisions"
section that names these conflicts explicitly. Otherwise agents will read
the synthesis as if the packet is fully aligned.

## 3 - Questions For The Designer

Each question is self-contained so the answer can be acted on without
scrolling back.

1. Where does `ConnectionClass` live now that mind, router, system,
   harness, terminal, and message all need it: `signal-core`,
   `signal-persona`, or a new narrow auth/identity contract?

2. Does `persona` literally accept every component connection through
   `ConnectionAcceptor`, or do component daemons accept their own sockets
   and verify auth context minted by `persona`?

3. Is the redb discipline "one writer actor per redb file" a hard rule?
   If yes, should every plan name the writer actor and treat all other
   actors as requesters/subscribers?

4. Should `OtherPersona` ever be rewritten to `System`, or should it
   always remain the source class with a separate route-derived gate
   decision?

5. Who produces prompt/input-buffer cleanliness: `persona-terminal`, which
   owns the gate and terminal session, or `persona-system`, which owns OS
   focus/window observation?

6. Is hot-swap part of the first `persona` daemon milestone, or is it
   explicitly deferred until daemon, catalog, spawn, health, and class
   minting work?

7. Are Persona contract repos still one relation each, or can a
   component-owned contract contain multiple named relations? If multiple
   relations are allowed, what is the naming rule?

8. Should typed-Nexus message bodies block router/harness durable schema
   hardening, or may those components store `MessageBody(String)` as a
   temporary durable shape?

9. During `persona-message` cleanup, what replaces `ActorIndex` /
   `actors.nota` before router-owned actor registry queries exist?

10. Is raw transcript fanout to router and mind intended, or should raw
    bytes stay in `persona-terminal` with harness pushing typed
    observations and transcript references?

## 4 - Edits I Would Make Next

I would not start by changing implementation code. I would do a short
designer-document alignment pass:

1. Fix the title of `reports/designer/122-persona-message-development-plan.md`
   from `# 116` to `# 122`.
2. Add a shared-decision table to `reports/designer/124-synthesis-drift-audit-plus-development-plans.md`
   covering `ConnectionClass` home, socket boundary, redb writer owner,
   `OtherPersona` preservation, input-buffer producer, and contract
   relation boundaries.
3. Update `reports/designer/116-persona-apex-development-plan.md` to
   choose one component-socket model and to defer or prove hot-swap redb
   concurrency.
4. Update `reports/designer/117-persona-mind-development-plan.md` so
   `CommitBus` is clearly after-commit fanout, not transactional fanout.
5. Update `reports/designer/118-persona-router-development-plan.md` and
   `reports/designer/121-persona-terminal-development-plan.md` so
   `OtherPersona` is preserved with a separate gate decision.
6. Update `reports/designer/119-persona-system-development-plan.md` and
   `reports/designer/121-persona-terminal-development-plan.md` to settle
   whether input-buffer state originates in terminal or system.
7. Promote `reports/designer/120-persona-harness-development-plan.md`
   section 14.1's transcript-storage default into the main transcript
   architecture.
8. Add the typed-Nexus body migration as its own designer report or fold
   it into `reports/designer/122-persona-message-development-plan.md`.

## 5 - Bottom Line

The packet is good enough to drive implementation only after a small
alignment pass. Without that pass, the likely implementation drift is
predictable: duplicate `ConnectionClass` types, mixed socket ownership,
multiple redb writers, erased `OtherPersona` provenance, and durable
schemas that bake in opaque string message bodies.

My strongest recommendation: resolve the shared decisions before touching
the contract repos. The contracts are the component boundaries; if the
boundaries encode these uncertainties, the code will enforce the wrong
answers.
