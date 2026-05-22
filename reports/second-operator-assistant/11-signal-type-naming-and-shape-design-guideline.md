## 11 — Signal-type / tree naming and shape design guideline (proposal)

**Lane:** second-operator-assistant
**Status:** proposal for designer-lane skill edits. The substance
here belongs in `skills/contract-repo.md`, `skills/naming.md`,
`skills/language-design.md`, and `skills/component-triad.md`. My
lane writes the proposal as a report; designer lifts the
substance into the skill files.

**Reads against:** /237 (schema-as-tree investigation, three
proposed skill edits never landed), /14 (`*Mode` suffix smell;
audit of the new owner contract naming), /15 + /16 (authority-
chain naming corrections revealing structural problems), /252
(engine-manager rename), /253 (`ToSemaOutcome` shape), /254
(observable event-pair naming); `intent/component-shape.nota`
2026-05-20T12:11:26Z (working/policy vocabulary, "signal-type
naming is architecture" principle), 2026-05-20T13:00:00Z (six
CLI-design records), 2026-05-20T13:30:00Z (Mind/Orchestrate/Router
correction), 2026-05-20T13:45:00Z (mind/body analogy),
2026-05-20T15:00:00Z (OperationReceived/EffectEmitted naming);
`intent/naming.nota` (9 records as of /237's investigation);
`intent/persona.nota` 2026-05-19T19:30:00Z (the contract-local-verb
correction sequence that supersedes the "Mutate Configure"
pattern).

## 0 · TL;DR

The workspace has converged on the three-layer model (Contract
Operation / Component Command / Sema Operation) and the two-
signal triad shape (working + policy contracts) — but the naming
and shape discipline for the resulting type trees is scattered
across nine reports, six intent records, and three different skill
files in various states of currency. This guideline consolidates
the substance into one place so agents implementing or reviewing
signal contracts have a single reference.

Eight principles, ranked by load-bearing-ness:

1. **Signal-type naming IS architecture.** When a name feels
   wrong, it is exposing a flawed signal tree, a wrong logic
   separation, or a mis-routed authority. Stop and audit the
   shape, not the name.
2. **Schemas grow as trees, not flat tables.** Repeated category
   words across sibling variants are missing parent enums.
3. **Public verbs are contract-local; Sema verbs are
   classification.** `operation Query(Query)` not `Match
   Query(Query)`; the daemon's `Lowering` projects to Sema
   classes for observation, not for vocabulary.
4. **Names don't restate their ancestry — but they don't
   abbreviate either.** Pair-of-rules from ESSENCE: full English
   words AND drop the namespace prefix the crate/module already
   supplies.
5. **Verbs name what the receiver does on input.** When a verb
   reads as "what gets done to the receiver" (`ChannelGrant`
   inside Mind's contract), the direction is wrong — that verb
   belongs on the outbound side, not the inbound side.
6. **Working and policy signals carry different verb shapes.**
   Working = peer-callable domain operations; policy = owner-only
   cognitive policy + (open question) lifecycle. The two contracts
   are not symmetric; their verb vocabularies don't mirror.
7. **The mind/body analogy applies to authority-surface verbs.**
   Owner-signal verbs from a cognitive caller (Mind →
   Orchestrate) are override-and-instruct, not routine
   micromanagement. The right abstraction level for the verb is
   cognitive intent, not mechanical operation.
8. **Observable events carry the typed component effect, not the
   Sema class.** `EffectEmitted` (typed) is the wire event;
   `SemaObservation` (universal) is composed at observer fanout
   from `ToSemaOperation` + `ToSemaOutcome` projections.

The rest of this guideline operationalizes each principle into
concrete shape rules.

## 1 · Principle 1 — Signal-type naming is architecture

The most load-bearing rule. Stated by psyche
(`intent/component-shape.nota` 2026-05-20T12:11:26Z):

> *"be very critical of the signal types, names, and the logic
> separation, the shape of the schema, the shape of the
> schematry … there's been a refactoring in the name and the
> shape of the signal tree for some component … because the
> naming betrayed a flaw in the design of the signal tree."*

The discipline: when a name feels wrong, do not fix it as a rename.
**Audit the signal tree first.** Three concrete instances where
naming exposed structural problems:

- **`Match Query(Query)`** in `signal-repository-ledger` (the case
  study from /124 + /237). The doubling read as ugly; the audit
  surfaced that the macro was tagging the Sema verb at the
  contract layer, where it doesn't belong. The fix was structural
  (move Sema verbs to execution layer; contract speaks `Query`),
  not cosmetic.
- **`ChannelGrant` / `ChannelExtend` / `ChannelRetract` /
  `AdjudicationDeny`** as ordinary working-signal variants on
  `signal-persona-mind` (per /159, /14, /15). The names read with
  the wrong direction — they look like inbound mind operations
  but represent outbound mind→router orders. The audit surfaced
  that Mind doesn't own Router (per /15's correction) — Orchestrate
  does. The verbs move to `owner-signal-persona-router`, called by
  Orchestrate.
- **`IntentEntry` / `IntentTopic` / `IntentQuote` / …** (16 types
  prefixed `Intent` in `signal-persona-spirit`). The names
  ancestry-stuttered the crate's domain. The audit surfaced that
  agents had been adding "safe" namespace prefixes to make types
  self-introduce, which the pair-of-rules in ESSENCE §"Naming"
  forbids.

The rule: **naming is signal. A name that reads wrong is the
schema asking for attention.** Do not rename around the smell;
audit and reshape.

## 2 · Principle 2 — Schemas grow as trees, not flat tables

The agent's failure mode (per psyche, /237):

> *"the agent doesn't see how the schema needs to evolve because
> it doesn't create the base schema properly from the beginning.
> So it ends up being this really stuffy, flat table of things
> where it should really grow into a tree."*

**Repeated category words across sibling names = missing parent
enum.** When several adjacent variants share the same prefix or
suffix — `*Query`, `*Command`, `*Event`, `*Listing`, `*Selection`,
`*Mode`, `*Result`, `*Order` — that repeated word is the schema
asking for a parent enum, relation, record, module, or contract
layer.

```rust
// Wrong — five siblings repeating `*Query` as a suffix
operation EventQuery(EventQuery),
operation RecentRepositoriesQuery(RecentRepositoriesQuery),
operation ChangedFileQuery(ChangedFileQuery),
operation CommitMessageQuery(CommitMessageQuery),
operation CatalogQuery(CatalogQuery),

// Right — Query is the parent enum
operation Query(Query),

pub enum Query {
    Events(EventSelection),
    RecentRepositories(RecentRepositorySelection),
    ChangedFiles(ChangedFileSelection),
    CommitMessages(CommitMessageSelection),
    Catalog(CatalogSelection),
}
```

The threshold is **behavioral, not numeric**. When adding the
third sibling with the same suffix, stop and lift the parent. The
tree continues to grow as repetition reveals deeper missing
parents (`query → recent → repositories`, etc. — the schema's
shape grows with the domain).

The rule **applies symmetrically to replies**, not just requests.
A reply enum with five `*Listing` siblings has the same missing
parent:

```rust
// Wrong — five siblings repeating `*Listing` as a suffix
reply Reply {
    EventRecorded,
    EventListing,
    RecentRepositoriesListing,
    ChangedFileListing,
    CommitListing,
    CatalogListing,
    RequestUnimplemented,
}

// Right — symmetric with the request side
reply Reply {
    EventRecorded(EventRecorded),
    QueryResult(QueryResult),
    RequestUnimplemented(RequestUnimplemented),
}

pub enum QueryResult {
    Events(EventListing),
    RecentRepositories(RecentRepositoriesListing),
    ChangedFiles(ChangedFileListing),
    CommitMessages(CommitListing),
    Catalog(CatalogListing),
}
```

This pairs with the no-redundant-ancestry rule from ESSENCE §"Naming."
The ancestry rule says "don't restate what the namespace supplies";
the repeated-category-word rule says "if siblings repeat a word,
the schema is missing the namespace that would supply it." Together:
**names carry only what the schema's structure doesn't carry; when
names repeat a word, that word should become structure.**

## 3 · Principle 3 — Public verbs are contract-local; Sema verbs are classification

Settled at `intent/persona.nota` 2026-05-19T19:30:00Z and
2026-05-20T02:00:00Z. The pre-/238 grammar (`Mutate Verb(Payload)`
/ `Match Verb(Payload)`) tagged the request-side variant with a
Sema verb. That was wrong — Sema verbs name what a *database*
does to state, not what a *client* is asking a *daemon* to do.

The new grammar drops the Sema prefix:

```rust
// Wrong — Sema verb prefix at the contract layer
operation Mutate Configure(Configuration),
operation Match Query(Query),

// Right — contract-local public verb
operation Configure(Configuration),
operation Query(Query),
```

Public verbs name the **client's action** in the receiver's
domain. The daemon's `Lowering` impl translates each operation
into a typed `Command` (Layer 2); Sema classification
(`ToSemaOperation` + `ToSemaOutcome`) is for observation only,
not vocabulary.

**Cross-contract verb-name reuse is allowed and expected.** The
verb `Submit` on `signal-persona-mind` does something different
from `Submit` on `signal-persona-orchestrate` — the receiver
determines the effect. The psyche's bird-vs-cloud metaphor
(2026-05-19T19:45Z): "if you tell a cloud to fall, or if you tell
a bird to fall, they're going to have different reactions,
obviously."

The reverse antipattern is **using Sema verbs as if they were
client verbs**. `operation Mutate Configure(Configuration)` reads
as "mutate a configure" — incoherent (you mutate nouns, not
verbs). The right shape is `operation Configure(Configuration)`
where Configure is the client's action verb.

## 4 · Principle 4 — Names don't restate ancestry, but don't abbreviate either

The pair-of-rules from ESSENCE §"Naming":

> *"we don't allow abbreviations for almost anything."*
> *"If I held the name of all my ancestors, I would be speaking
> until I die before I could spell my name out."*

Two rules, applied together:

- **Full English words.** `Request` not `Req`; `Identifier` not
  `Id`; `Configuration` not `Cfg`. Only acronyms that have passed
  into general English (`CPU`) qualify as narrow exception.
- **No ancestry restating.** A type, variant, or field belongs to
  its surrounding namespace; repeating the namespace in the name
  is redundant. Inside `signal-persona-spirit`, the type is
  `Entry`, not `IntentEntry`. Inside a `Profile` struct, the
  field is `size`, not `profileSize`.

The pair only works together. Dropping abbreviations without
dropping ancestry produces stuffy elaboration (`IntentRecordIdentifier`
in a contract whose domain is intent); dropping ancestry without
dropping abbreviations produces cryptic shortenings (`E`, `T`).
The pair is the discipline.

**Anti-pattern observed in `owner-signal-persona-mind`** (per /14):
`AuthorityMode`, `ChoreographyMode`, `IntentSynchronizationMode`
carry the `Mode` framework-category suffix. Reading: a
`Configuration` struct with fields `authority`, `choreography`,
`intent_synchronization` of types `AuthorityMode`, etc. Drop the
`Mode` suffix; the types become `Authority { ObserveOnly,
ProposeOrders, IssueOrders }` etc. — the variant names already
read as kinds-of-authority.

The `*Mode` suffix is a member of a broader family that includes
`*Kind`, `*Type`, `*Info`, `*Details`, `*Meta`, `*Extra`, `*Full`,
`*Extended`, `*Raw`, `*Parsed`. All of these are framework-category
noise indicating the base type was named too thin. Widen the base
type instead.

## 5 · Principle 5 — Verbs name what the receiver does on input

The Mind/Router naming antipattern (per /15) is the case study.

When `signal-persona-mind` carried `ChannelGrant(ChannelGrant)`
as an inbound operation, the verb read as "what gets done to the
receiver" — Mind being told to grant a channel. But the actual
authority direction is Mind → Orchestrate → Router; Mind decides
cognitively and orders Orchestrate; Orchestrate orders Router with
`Grant(...)`. The verb `Grant` belongs on Router's owner contract,
where Router is the receiver and Grant is what it does.

The rule: **verbs name what THIS receiver does on this input.**
A verb that reads as "this gets done to me" is direction-wrong;
the verb belongs on the outbound side, called by the entity above
in the authority chain.

This is verb-belongs-to-noun (`skills/abstractions.md`) applied to
signal contracts. The receiver is the noun; the verbs on its
contract name the receiver's actions. When the wrong noun owns a
verb, the schema is asking for the verb to move.

**Detection heuristic.** Read each operation variant as a sentence:
"The <receiver> <verb>s the <payload>." If the sentence is
incoherent or backwards, the verb is in the wrong contract.

- `signal-persona-router::Grant(ChannelGrant)` — "the router
  grants the channel grant." Direction-coherent.
- `signal-persona-mind::ChannelGrant(ChannelGrant)` — "the mind
  channel-grants the channel grant." Incoherent.

## 6 · Principle 6 — Working and policy signals carry different verb shapes

Settled at `intent/component-shape.nota` 2026-05-18T22:13:54Z
(two authority tiers) and 2026-05-20T12:11:26Z (universal
owner-contract principle):

> *"Every stateful component has an owner contract because
> management and configuration must enter through an owner-only
> signal surface that can be protected by filesystem permissions.
> Owner contracts are the policy/configuration authority surface;
> ordinary contracts are the peer-callable working surface."*

The two contracts are **not symmetric.** Their vocabularies serve
different concerns:

### Working signal — `signal-<component>`

Peer-callable. Variants describe the **domain operations** any
authorized peer can issue. The wire vocabulary is the receiver's
public surface to its peer ecosystem.

Verb shapes typical here:

- **Submit / Record / Receive** — peer hands work or data to
  the receiver.
- **Query / Read / Inspect** — peer reads from the receiver.
- **Watch / Unwatch** — peer subscribes to ongoing changes (or
  the macro-injected `Tap` / `Untap` for the universal
  observation hook).
- **Other domain verbs** — whatever the contract's domain naturally
  uses (`State` for psyche-statement submission on spirit;
  `Claim` / `Release` / `Handoff` for role coordination on
  orchestrate; `Send` / `Inbox` on message).

### Policy signal — `owner-signal-<component>`

Owner-only. Variants describe **policy / configuration / authority
orders** the receiver's owner issues. The owner is the entity
above in the workspace's authority chain.

Verb shapes typical here:

- **Configure** — owner sets the receiver's durable policy
  state.
- **Inspect** — owner reads the receiver's policy state.
- **Start / Drain / Stop / Reload** — lifecycle (open question
  whether this lives here or out-of-band per intent
  2026-05-20T13:45:00Z).
- **Domain authority orders** — owner orders the receiver to do
  something only the owner can authorize. (E.g.,
  `owner-signal-persona-router` carries `Grant` / `Extend` /
  `Revoke` / `Deny` — orders Orchestrate issues to Router because
  Orchestrate owns Router.)

The policy signal's vocabulary is shaped by **who the owner is**
and **what cognitive level the owner operates at**. Per principle
7 below, owner-signal verbs from a cognitive caller (Mind →
Orchestrate) are cognitive-level overrides, not mechanical
operations.

### What policy signals do NOT carry

- **Tap / Untap** — universal observation rides the working
  socket, not the owner socket (`intent/component-shape.nota`
  2026-05-19T20:00Z, refined 2026-05-20T02:00Z).
- **Working-state mutations** — those go through working-signal
  variants, even when the writer is the owner. The owner's
  authority is over policy/configuration; the working state is
  what peers also see.
- **Record-ingestion** for general data — that's a working-signal
  concern (peer hands the receiver work or data).

## 7 · Principle 7 — The mind/body analogy

`intent/component-shape.nota` 2026-05-20T13:45:00Z (Principle,
Maximum):

> *"think of the human mind vs the body; the body does many things
> mindlessly, and the mind does many things that don't involve
> controlling the body, while it still can override the body and
> instruct it to do things it wouldn't do on its own"*

Applied to the authority surface (per /16):

- **The body has autonomy.** Orchestrate runs its routine machinery
  (claims, activity, repository index, lifecycle transitions, scope
  acquisition, scheduling) without Mind's involvement.
- **The mind has its own life.** Mind reads its work graph, runs
  its choreography adjudicator, makes cognitive judgments — most
  of which doesn't involve directing Orchestrate.
- **Mind reaches in for cognitive override-and-instruct.** When
  Mind's judgment needs to redirect the body, the verb crosses
  the seam.

**Verb-naming consequence on owner contracts.** The cognitive
caller's verbs (Mind → Orchestrate) should name **cognitive
intent**, not **mechanical operation**. Examples (open candidates
from /16):

- `AuthorizeChannel(ChannelAuthorization)` — "I've decided this
  channel should exist for this cognitive purpose." Mind delivers
  the cognitive shape (purpose, parties, conditions); Orchestrate
  translates to `Grant(...)` on Router with the right concrete
  duration, message kinds, etc.
- `RetractChannelAuthorization(ChannelAuthorizationToken)` — "that
  authorization no longer holds." Symmetric.
- `SpawnAgent(AgentSpawnIntent)` — "I've decided we need an agent
  in lane X for topic Y." Orchestrate decides spawn plan, scope
  acquisitions, harness orders.
- `EscalateBlockedWork(EscalationIntent)` — "this work is stuck;
  surface for human attention."

The counter-example (what does NOT belong on this surface):

- `Grant(...)` / `Extend(...)` / `Revoke(...)` as the verbs Mind
  speaks on `owner-signal-persona-orchestrate`. That's Router-
  level mechanics; if Mind speaks Router-level on Orchestrate's
  contract, Orchestrate becomes a pass-through translator with
  no value-add — and the body loses autonomy. The cognitive level
  is the right level.

**The general rule for cross-component authority verbs:** name
the caller's cognitive intent, not the callee's mechanical
operation. Let the callee's autonomy translate intent into
mechanics.

## 8 · Principle 8 — Observable events carry typed component effects

Per `intent/component-shape.nota` 2026-05-20T15:00:00Z. The
canonical observable event-pair is `OperationReceived` /
`EffectEmitted` — the Sema prefix is dropped from the effect
side because the event carries the typed component effect, not
the universal Sema classification.

The shape:

```rust
observable {
    filter <FilterType>;
    operation_event OperationReceived;
    effect_event EffectEmitted;
}
```

The macro injects `Tap(<FilterType>) opens <Channel>ObserverStream`
and `Untap(<Channel>ObserverSubscriptionToken)` automatically. The
contract author doesn't name these.

The **universal Sema classification** lives separately:

```rust
pub struct SemaObservation {
    pub operation: SemaOperation,    // payloadless class
    pub outcome: SemaOutcome,        // payloadless class
}
```

Composed at observer fanout from `command.to_sema_operation()`
and `effect.to_sema_outcome()`. Cross-component patterns
("which components performed an Assert in the last hour?") use
the universal classification; component-specific introspection
("which entries got recorded?") uses the typed effect event.

**Why `EffectEmitted` not `SemaEffectEmitted`:** the typed event
carries the daemon's `ComponentEffect`, not the universal
`SemaObservation`. The Sema prefix would be a misname suggesting
the event carries Sema classification.

## 9 · The three-layer naming vocabulary

The three-layer model (`intent/component-shape.nota`
2026-05-20T02:00:00Z) provides the canonical vocabulary for type
names across the stack:

| Layer | Owns | Type name convention |
|---|---|---|
| 1 — Contract Operation | external request/reply language, on the wire | `<Component>Operation`, `<Component>Reply` — owned by `signal-<component>` |
| 2 — Component Command | internal executable, per-daemon | `<Component>Command`, `<Component>Effect` — owned by the daemon crate |
| 3 — Sema Operation | universal payloadless classification | `SemaOperation`, `SemaOutcome`, `SemaObservation` — owned by `signal-sema` |

Naming consistency rules:

- The contract's `<Component>Operation` has variants named in the
  contract's domain verbs (`State`, `Record`, `Query`,
  `Configure`).
- The daemon's `<Component>Command` has variants named as
  imperative-form daemon-internal commands (`RecordEntry`,
  `ReadEntries`, `OpenObserver`, `CheckProposalAgainstCurrent`).
  These are typically more granular than contract operations —
  one operation may lower to multiple commands.
- The daemon's `<Component>Effect` has variants named in past-
  tense outcomes (`EntryRecorded`, `EntriesRead`, `ObserverOpened`,
  `ProposalVerdict`).
- `SemaOperation` variants are the six payloadless classes
  (`Assert`, `Mutate`, `Retract`, `Match`, `Subscribe`,
  `Validate`).
- `SemaOutcome` variants mirror with past-tense classification
  (`Asserted`, `Mutated`, `Retracted`, `Matched`, `Subscribed`,
  `Validated`) plus `NoChange`.

## 10 · CLI design constraints

Six intent records at `intent/component-shape.nota`
2026-05-20T13:00:00Z settle the CLI design:

1. **Naming.** CLI binary name = daemon binary name minus the
   `-daemon` suffix. `mind-daemon` → `mind`. `spirit-daemon` →
   `spirit`. `orchestrate-daemon` → `orchestrate`. The repository
   keeps the `persona-` prefix (filesystem disambiguation); the
   binaries drop it.
2. **Two argument shapes only.** A NOTA string starting with `(`
   (raw NOTA on the shell — most agent usage), or a file path
   (whose contents are NOTA text valid for this CLI). The
   signal-encoded (rkyv) file path is **daemon-only**, not a CLI
   shape.
3. **Pure NOTA↔Signal translation bridge.** The CLI does nothing
   else — no logic, no state, no fan-out, no convenience business
   logic. Translate NOTA in → signal frame → daemon → signal reply
   → NOTA out.
4. **One env-var carve-out.** The CLI is the only workspace
   surface allowed to read an environment variable, and only for
   socket-path override (test daemon, non-canonical deployment).
   The env var is checked FIRST; the canonical path is the
   default. Daemons never read env vars; all daemon config is
   NOTA.
5. **Two-socket dispatch.** The CLI talks to one peer daemon
   exposing two sockets — working (peer-callable
   `signal-<component>`) and policy (owner-only
   `owner-signal-<component>`). The CLI dispatches each NOTA
   request to the correct socket based on which contract it
   belongs to. Triad invariant 1 ("the CLI has exactly one Signal
   peer") still holds — the peer is the single daemon.
6. **Universal CLI shape.** Every CLI follows the same shape;
   per-component CLI ergonomics do not exist.

## 11 · Smell catalogue — names betray flawed structure

When auditing a signal tree, these naming smells reliably indicate
structural problems:

| Smell | Underlying problem | Fix |
|---|---|---|
| Three+ sibling variants with the same suffix (`*Query`, `*Listing`, `*Order`) | Missing parent enum | Lift the suffix into a parent; collapse siblings to one variant |
| Domain prefix repeated on every type (`Intent*`, `Repository*`) | Restating namespace the crate already supplies | Drop the prefix |
| Sema-verb prefix on operation variant (`Mutate Verb(...)`, `Match Verb(...)`) | Conflating execution layer with contract layer | Use contract-local verb only |
| `*Mode` / `*Kind` / `*Type` / `*Info` / `*Details` suffix on a type | Base type designed too thin | Widen the base type |
| `*Order` / `*Request` / `*Reply` suffix duplicating the variant's role | Restating what the position in the tree already says | Drop the suffix |
| Verb reads as "what gets done to me" when on a receiver's contract | Direction reversed | Move to the outbound contract |
| Repeated `*Receipt` / `*Acknowledged` siblings | Missing reply-side parent | Lift to a parent enum, symmetric with request side |
| `Mutate <Verb>(<Payload>)` where `<Verb>` is a verb | Grammatical mismatch (you mutate nouns) | Either the verb names a noun-event or the variant is wrong |
| `*Subscription` suffix on Sema-Subscribe variant payload | Suffix duplicates the variant's verb | Drop the suffix |
| Single-variant `*Scope` / `*Filter` enum carrying no distinction today | Scaffolding for a future variant that's not real yet | Use unit variant on parent until the second variant is real |
| Wrapper struct with one field that names the variant's domain | Variant already supplies the structure | Drop the wrapper; use bare type |
| Type ending in `Snapshot`, `Capture`, `Observation` when used as a Match payload | Domain-vocabulary fine if used once; sibling repetition turns it into the parent-extraction smell | Apply principle 2 at the third repetition |

The catalogue is a working list; the principles in §§1–8 are the
deeper rules. The smells are diagnostic shortcuts.

## 12 · Worked example — persona-spirit's tree (canonical)

The migrated `signal-persona-spirit` (commit `a1909872`) is the
worked example. Read it as the reference shape for any new
contract.

What it gets right:

- **Contract-local verbs.** `operation State(Statement)`,
  `operation Record(Entry)`, no Sema prefix.
- **Tree-shaped read surface.** A single `operation Query(Query)`
  with `Query` as a parent enum carrying the read targets.
- **Reply-side discipline.** Past-tense outcome variants
  (`Stated`, `Recorded`); typed rejection variants
  (`StateRejected(StateRejectionReason)`) that ride in
  `SubReply::Failed.detail`; `RequestUnimplemented` (no contract
  prefix) for skeleton-honesty fallthrough.
- **Observable block — three lines.** `filter default;
  operation_event OperationReceived; effect_event EffectEmitted;`
  No author-named open/close verbs.
- **Layer-2 separation.** `SpiritCommand` and `SpiritEffect` live
  in the daemon crate, not the contract crate. The contract
  speaks only Layer 1.
- **No `Intent*` prefix in the spirit domain.** Types are `Entry`,
  `Topic`, `Quote`, `Context`, `Timestamp` — the crate's
  namespace supplies the "intent" context.

What `owner-signal-persona-mind` (the next worked example to
land) gets right (per /14):

- `Configure(Configuration)` + `Inspect(Inspection)` — owner-only
  policy verbs.
- `RequestUnimplemented` (no contract prefix).
- `OperationKind { Configure, Inspect }` (no `OwnerOperationKind`
  prefix).
- `signal-frame` dep (post-rename).

What still needs fixing in `owner-signal-persona-mind` (per /14):

- Drop `*Mode` suffix from `AuthorityMode`, `ChoreographyMode`,
  `IntentSynchronizationMode` — the bare names already read.
- Retire the `OwnerMindRequest = OwnerMindOperation` type alias
  once consumers update to the post-three-layer naming.

## 13 · Proposed skill-file edits (designer lane)

This guideline distills substance for the following destinations.
The designer lane lifts each section into its target skill, then
this report retires.

### 13.1 — `skills/contract-repo.md`

- **§"Naming the receiver and the verb"** — add Principle 1
  (signal-type naming is architecture; audit the tree when a name
  feels wrong).
- **§"Public contracts use contract-local operation verbs"** —
  already settled in skill text per `intent/persona.nota`
  2026-05-19T19:30:00Z + 2026-05-20T02:00:00Z. Add a paragraph
  cross-referencing Principle 5 (verbs name what the receiver
  does; wrong direction means wrong contract).
- **§"Anti-pattern: repeated category words across sibling
  names"** — new subsection per /237's proposed edit. Include the
  worked example, the symmetric application to replies, and the
  behavioral threshold (third sibling).
- **§"Reply discipline"** — already at `a7f3a0ee`. Add a
  paragraph on the symmetric reply-side tree shape (request
  `Query(Query)` ↔ reply `QueryResult(QueryResult)`).
- **§"Observable block grammar"** — replace any older
  `open <Verb>(<Filter>); close <Verb>;` examples with the three-
  line shape (`filter / operation_event / effect_event`). Note
  the macro injection of standardized `Tap` / `Untap` for
  persona components.
- **§"Working signal vs policy signal"** — add §6's framing:
  the two contracts are not symmetric; their verb shapes serve
  different concerns; Tap/Untap rides working only.
- **§"Cognitive vs mechanical owner verbs"** — add §7's framing:
  the mind/body analogy applied to authority verbs; cognitive
  callers name intent, not mechanics.

### 13.2 — `skills/naming.md`

- **§"Anti-pattern: repeated category words across sibling
  names"** — per /237's proposed edit. The cross-language version
  of the rule (applies to any closed-sum sibling set, not just
  Rust enums).
- **§"Anti-pattern: framework-category suffixes on type names"**
  — already in the skill; add `*Mode` to the offender list with
  the `owner-signal-persona-mind` example.
- **§"Verbs name what the receiver does on input"** — new
  subsection per §5. Cross-language; applies wherever a
  receiver-verb-payload triple appears.

### 13.3 — `skills/language-design.md`

- **Rule 6 strengthening** — per /237's proposed edit. *"As the
  schema grows, repeated category words collapse into typed
  parent enums."* Same shape as the existing "strings collapse
  into typed records" — both are about transitional placeholders
  for structure not yet pulled out.

### 13.4 — `skills/component-triad.md`

- **§"The triad's three legs"** — already corrected per the
  vocabulary clarification at 2026-05-20T12:11:26Z. Verify
  current text matches (daemon + working signal + policy signal;
  CLI is a thin client, not a leg).
- **§"The single argument rule"** — narrow for CLIs: two argument
  shapes (raw NOTA starting with `(`, or file path), per intent
  2026-05-20T13:00:00Z. Daemons still take three shapes.
- **§"Named carve-outs"** — add the CLI socket-path env-var
  carve-out (intent 2026-05-20T13:00:00Z); narrow to CLI only,
  socket-path only, env-var-first dispatch.
- **§"CLI design is workspace-universal"** — new section per the
  Principle at 2026-05-20T13:00:00Z. The CLI binary name
  convention, two-argument shape, pure translation bridge,
  env-var carve-out, two-socket dispatch all apply universally.
- **§"Authority chain"** — verify the existing mermaid does NOT
  show Mind issuing directly to Router per /15's correction.
  /16 §9 named this gap; designer lane should verify and fix.
- **§"Cognitive vs mechanical authority verbs"** — new subsection
  per §7 of this guideline. Verbs on owner contracts called by
  cognitive callers name intent, not mechanics.

### 13.5 — `AGENTS.md` Hard overrides

- **Footnote the env-var carve-out** on the existing "NOTA is the
  only argument language" override.

## 14 · References

### Substantive prior reports

- `reports/designer/237-signal-type-naming-and-schema-tree-investigation.md` — the foundation; the three proposed skill edits this guideline carries forward.
- `reports/designer/247-radical-rethink-or-converge.md` — the convergence verdict that anchors the rest.
- `reports/designer/249-component-intent-gap-analysis.md` — adjacent gap inventory; gap #4 (Tap/Untap as universal hook) is closed by the working assumption here.
- `reports/designer/251-supervisor-identity-disambiguation.md` — disambiguation analysis; resolved by the engine-manager rename (since dropped; substance now in `skills/component-triad.md`).
- `reports/designer/253-tosemaoutcome-trait-shape.md` — two-trait shape settled.
- `reports/designer/254-signal-executor-sema-refresh-audit.md` — five gaps psyche-affirmed.
- `reports/operator/144-signal-sema-executor-refresh-2026-05-20.md` — the landed state.
- `reports/operator/145-signal-sema-spirit-current-handoff-2026-05-20.md` — current operator handoff; names the spirit-pilot's immediate-next work and the stale-on-`CommitStatus::Partial` surfaces.
- `reports/operator-assistant/159-persona-mind-signal-tree-owner-contract-vision.md` — Mind refactor proposal.
- `reports/operator-assistant/160-owner-signal-persona-router-channel-authority.md` — router policy contract.
- `reports/second-designer-assistant/14-audit-of-operator-assistant-159-owner-signal-persona-mind.md` — Mind contract audit; the `*Mode` smell.
- `reports/second-designer-assistant/15-clarification-for-operator-assistant-on-orchestrate-router-authority.md` — Mind/Router authority correction.
- `reports/second-designer-assistant/16-mind-orchestrate-boundary-research-mind-body-analogy.md` — cognitive vs mechanical seam research.
- `reports/second-operator-assistant/10-component-migration-plan-v4-three-layer.md` — sibling migration plan report.

### Intent records (canonical substrate)

- `intent/component-shape.nota` 2026-05-18T22:13:54Z — two authority tiers (working + policy; no middle).
- `intent/component-shape.nota` 2026-05-19T20:00:00Z — universal observer hook on the working socket.
- `intent/component-shape.nota` 2026-05-19T20:30:00Z — 5 missing owner-signal-* repos are intentionally missing.
- `intent/component-shape.nota` 2026-05-20T02:00:00Z — three-layer model affirmation.
- `intent/component-shape.nota` 2026-05-20T12:11:26Z — working/policy vocabulary; "signal-type naming is architecture" principle; universal owner-contract.
- `intent/component-shape.nota` 2026-05-20T13:00:00Z — six CLI-design records.
- `intent/component-shape.nota` 2026-05-20T13:30:00Z — Mind/Orchestrate/Router authority correction.
- `intent/component-shape.nota` 2026-05-20T13:45:00Z — mind/body analogy + lifecycle open question.
- `intent/component-shape.nota` 2026-05-20T15:00:00Z — OperationReceived/EffectEmitted, no-op-as-explicit-command, BatchErrorClassification.
- `intent/persona.nota` 2026-05-19T15:30:00Z — canonical authority chain.
- `intent/persona.nota` 2026-05-19T19:30:00Z — contract-local-verb correction (verbs describe client action, not database execution).
- `intent/persona.nota` 2026-05-19T19:45:00Z — bird/cloud metaphor (same verb, receiver-specific lowering).
- `intent/naming.nota` — 9 records (per /237) including "Query is its own logic plane."

### Substrate skills (already in place)

- `skills/contract-repo.md` — wire-contract crate discipline.
- `skills/naming.md` — full English words + no ancestry restating.
- `skills/language-design.md` — closed enums; structural beauty over ad-hoc strings.
- `skills/component-triad.md` — daemon + working signal + policy signal triad shape.
- `skills/abstractions.md` — verb belongs to noun.
- `skills/nota-design.md` — positional records, no labeled fields.
- `ESSENCE.md` §"Naming" — the pair-of-rules canonical text.

This report retires when the designer lane lifts the substance
into the skill files named in §13, and the lifted skills cite
the intent records directly (per `skills/skill-editor.md`'s rule
that skills cite intent and prior skill text, not reports).
