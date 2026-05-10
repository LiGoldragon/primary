# 7 - Contract relation naming survey

*Designer-assistant survey of the implemented Signal contract repos,
read through the workspace naming, beauty, abstraction, Rust, language,
and contract-repo skills. I also updated `skills/contract-repo.md` so
the relation-first naming rule is durable workspace doctrine.*

---

## Position

The user's framing is right: contract repos are among the most
important architecture components in the workspace because consumers
cannot escape them. A bad architecture paragraph can be ignored. A bad
contract name becomes a type, a variant, a field, a call site, and a
test fixture.

Every contract repo should be reviewed as a relation vocabulary:

- Which components are related?
- What is the cardinality?
- Which vectors can cross the relation?
- Which side mints identity, time, slots, and sender?
- Which lifecycle states are real domain states instead of temporary
  implementation states?

The root enum pass should always happen first. Root request/reply/event
variants are the grammar of the relation; payload and field names must
fit that grammar.

---

## Skill Change Made

Updated `skills/contract-repo.md` with a new section,
`Contracts name relations`.

The new doctrine says:

- a contract repo is not a shared-types bucket;
- root enums name the closed set of vectors in a relation;
- contract commands should usually be noun-form records crossing the
  wire;
- verbs belong to methods and engines, except for the explicit universal
  verb spine;
- names should neither repeat namespace already supplied by crate/module
  context nor collapse into generic placeholders like `Ok`, `Generic`,
  `Mixed`, `Data`, or `Payload`;
- the naming pass starts with architecture, top-level enums, and root
  variants before moving into payload structs and fields.

This is the durable part of the work. It makes the user's instruction
available to future agents before they start editing contracts.

---

## Contract Inventory

| Repo | Relation sentence | Root shape | First read |
|---|---|---|---|
| `repos/signal-core` | Shared Signal kernel used by every Signal-family contract | `Request<Payload>`, `Reply<Payload>`, `FrameBody`, `SemaVerb` | Clean kernel shape; `SemaVerb` is acceptable only because it is the named universal verb spine |
| `repos/signal` | Sema/Criome vocabulary layered over Signal kernel | direct `Request`, `Reply`, per-verb operations | Structurally useful, but source still has a parallel direct request/reply layer while architecture points at `signal-core` |
| `repos/signal-forge` | criome -> forge effect-bearing build/deploy/store relation | skeleton only | Architecture names the relation well; source has not yet grown the payload vocabulary |
| `repos/signal-persona` | Shared Persona domain vocabulary over `signal-core` | `RequestPayload`, `ReplyPayload`, `Record`, `Mutation`, `Retraction`, `Query` | Strong central vocabulary, but some generic reply and mixed-record names leak uncertainty |
| `repos/signal-persona-message` | message CLI/client -> router ingress relation | `MessageRequest`, `MessageReply` | Highest naming and typing pressure among implemented channel contracts |
| `repos/signal-persona-system` | system observer -> router push/focus/input relation | `SystemRequest`, `SystemEvent` | Good channel boundary; root request variants need noun-form/snapshot polish |
| `repos/signal-persona-harness` | router <-> harness delivery/interaction lifecycle relation | `HarnessRequest`, `HarnessEvent` | Correct lifecycle area; request vectors and failure reasons need sharper domain nouns |
| `repos/signal-persona-mind` | mind CLI/agents -> persona-mind work/claim graph relation | `MindRequest`, `MindReply`, work graph event enums | Strongest typing; role taxonomy and several generic graph names need a naming pass |

---

## Top-Level Enum Pass

### `signal-core`

The kernel is conceptually sound:

- `SemaVerb` names the universal verb spine.
- `Request<Payload>` separates `Handshake` from `Operation`.
- `FrameBody<RequestPayload, ReplyPayload>` separates handshake,
  request, and reply envelopes.
- `PatternField<T>` gives bind/wildcard dispatch a reserved name.

My only naming question is whether `SemaVerb` should eventually become
`Verb` inside `signal-core`. The prefix is defensible because the twelve
verbs are a named Sema concept, but it is also a crate-internal namespace
repeat. I would not rename it before a broader `signal`/`signal-core`
cleanup.

### `signal`

The top-level source still has direct `Request` and `Reply` enums in
addition to the newer `signal-core` kernel story. That is the biggest
architectural ambiguity in this repo.

Names to recheck:

- `AssertOperation`, `MutateOperation`, `RetractOperation`,
  `QueryOperation`: precise but heavy. They may be right because these
  are payloads under the universal verb spine. If examples read better
  as `Assertion`, `Mutation`, `Retraction`, and `Query`, prefer the
  domain nouns.
- `OutcomeMessage`: sounds like transport rather than domain. Consider
  `OperationOutcome` if the record is the outcome of one operation.
- `Records`: useful in a reply position, but weak as a top-level type.
  If it remains, examples should prove the enum context makes it exact.

### `signal-persona`

This is a good shared Persona vocabulary, but it still has names that
hide uncertainty:

- `ReplyPayload::Ok(CommitOutcome)` is generic. The reply vector should
  say what succeeded: commit accepted, validation accepted, subscription
  accepted, etc.
- `CommitOutcome::Generic` is under-specified. A generic outcome is not
  a domain fact.
- `Records::Mixed(Vec<Record>)` is convenient, but it weakens the type
  boundary. If mixed records are real, name the projection: e.g. a view,
  page, batch, or result set.
- `RequestPayload` is only tolerable because it sits under
  `signal_core::Request`. Do not copy that name into channel crates.
- `AtomicOperation` probably wants the word used by examples:
  `AtomicStep`, `AtomicChange`, or `AtomicRecordChange`, depending on
  what is actually committed.
- `Slotted<Record>` uses `Record` as a generic parameter name. That
  reads like the enum name and should become a neutral parameter such as
  `Value` or `RecordValue`.

`Lock`, `Scope`, and `RoleName(String)` should also be revisited after
the role taxonomy settles. The live workspace has `operator-assistant`
and `designer-assistant` lanes; contract role names cannot lag behind
the orchestration model.

### `signal-persona-message`

This repo needs the sharpest relation naming pass.

Current shape:

- request variants: `Submit`, `Inbox`
- reply variants: `SubmitOk`, `SubmitFailed`, `InboxResult`
- payloads: `SubmitMessage`, `SubmitReceipt`, `SubmitFailed`,
  `InboxQuery`, `InboxResult`, `InboxMessage`
- primitive fields: `recipient: String`, `sender: String`,
  `body: String`, `message_slot: u64`

Recommended direction:

- `SubmitMessage` -> `MessageSubmission`.
- `SubmitOk` -> `SubmissionAccepted` or `MessageAccepted`.
- `SubmitFailed` -> `SubmissionRejected`; payload can carry
  `SubmissionRejectionReason`.
- `PersistenceRejected` -> `StoreRejected` if the router is reporting
  storage rejection, not generic persistence.
- `UnknownRecipient` -> `RecipientNotFound` if this is a lookup miss.
- `InboxResult` -> `InboxListing` or `InboxView`; "result" names the
  RPC shape, not the domain projection.
- `message_slot: u64` should be a typed slot/newtype.
- `recipient`, `sender`, and `body` should use contract newtypes or
  shared Persona records, not raw strings.

This channel is the user-facing ingress relation. Its names must make
clear which facts the client is allowed to supply and which facts the
router/store mint.

### `signal-persona-system`

This contract is close to the right model: the system side observes OS
facts and publishes focus/input-buffer facts to the router.

The drift already noted in `reports/designer/80-open-questions-inventory.md`
is still correct: imperative request names should move to noun form.

Recommended direction:

- `SubscribeFocus` -> `FocusSubscription`.
- `UnsubscribeFocus` -> `FocusUnsubscription`.
- `ObserveFocus` should not collide semantically with the emitted
  `FocusObservation`. If it is a one-shot read, `FocusSnapshot` or
  `FocusReading` may be clearer than another `FocusObservation`.
- `ObserveInputBuffer` likewise wants `InputBufferSnapshot` or
  `InputBufferReading` if it is one-shot.
- `TargetNotFound` is serviceable, but `ObservationTargetMissing` would
  be more exact if the only failure is target lookup.
- `generation: u64` should be a newtype once examples prove the update
  semantics.

### `signal-persona-harness`

The relation is right: router requests delivery/interaction work, the
harness reports lifecycle events.

Recommended direction:

- `DeliverMessage` -> `MessageDelivery`.
- `SurfaceInteraction` -> `InteractionSurfacing` if we keep the current
  noun-form decision, though I would test `InteractionPrompt` in
  examples because "surfacing" may still sound like an implementation
  move.
- `CancelDelivery` -> `DeliveryCancellation`.
- `DeliveryCompleted` and `DeliveryFailed` are good lifecycle events.
- `HumanRaceLost` should be renamed. It names a race implementation, not
  the domain condition. Candidates: `HumanInputIntervened`,
  `HumanInputArrivedFirst`, or `HumanOwnedInput`.
- `HarnessTeardown` should become `HarnessStopped` if it simply means
  the harness went away.
- `sender`, `body`, and `message_slot` need the same typed treatment as
  `signal-persona-message`.

### `signal-persona-mind`

This repo has the best current type safety:

- wire paths, task tokens, scope reasons, timestamps, item ids, display
  ids, aliases, operation ids, event sequence, and query limit are all
  newtyped;
- request bodies omit actor identity where the store must mint/stamp it;
- the event header makes actor/operation/event identity explicit.

The remaining issues are naming and taxonomy:

- `RoleName` still has `Assistant`; the live workspace now uses
  `operator-assistant` and `designer-assistant` lock/report lanes. This
  contract will enforce the wrong world unless it is updated with the
  orchestration model.
- `ActorName` may collide with runtime actor vocabulary. If this is
  caller identity, `PrincipalName` or `CallerName` may be a better
  contract name.
- `Kind`, `Status`, and `Priority` are too generic outside their local
  section. Prefer `ItemKind`, `ItemStatus`, and `ItemPriority`.
- `Body` is too broad for a central work graph. Consider `ItemBody`,
  `NoteBody`, or `TextBody` depending on whether one type is intended to
  span all text-bearing records.
- `Opening` is a little abstract. If the relation is opening a work
  item, `ItemOpening` is clearer.
- Root variants `Open`, `AddNote`, `Link`, `ChangeStatus`, `AddAlias`,
  and `Query` are still verb-shaped. Noun-form candidates:
  `ItemOpening`, `NoteAddition`, `EdgeAddition` or `LinkAddition`,
  `StatusChange`, `AliasAssignment`, and `ViewQuery`.
- `View` is acceptable only if the architecture defines exactly what the
  view contains. If it is the work graph projection, `WorkGraphView`
  would be more exact.

---

## To-Do List

1. Add a relation sentence to every contract `ARCHITECTURE.md`.
   The sentence should include endpoints, cardinality, direction, and
   authority. This should be done before any large rename.

2. Run a root enum rename pass across `signal-persona-message`,
   `signal-persona-system`, and `signal-persona-harness`.
   This aligns with bead `primary-28v` and the noun-form command
   decision in `reports/designer/80-open-questions-inventory.md`.

3. Update role taxonomy in `signal-persona-mind`.
   The contract should not encode the old generic `Assistant` role if
   orchestration now has explicit operator/designer assistant lanes.

4. Replace raw primitive wire fields in edge contracts.
   Start with `message_slot: u64`, `recipient: String`,
   `sender: String`, and `body: String` in the message/harness channel
   crates.

5. Decide the `signal` vs `signal-core` source truth.
   If `signal-core::Request<Payload>` is the live kernel, remove or
   clearly layer the older direct `signal::Request`/`Reply` shapes.

6. Remove generic success/mixed placeholders from `signal-persona`.
   `ReplyPayload::Ok`, `CommitOutcome::Generic`, and `Records::Mixed`
   should either be renamed to real relation vectors or deleted.

7. Add canonical examples before each rename lands.
   The examples should make the relation names falsifiable: if the text
   examples read awkwardly, the Rust names are not done.

---

## Suggested Naming Standard

Use this as the contract rename rubric:

- A type name should make sense when spoken without the crate prefix.
- A variant name should make sense when spoken with its enclosing enum.
- A field name should use its containing record for context.
- A primitive crossing a wire should be newtyped as soon as the primitive
  can be confused with another primitive.
- A reply variant should name the domain outcome, not just `Ok` or
  `Result`.
- A rejection reason should name the failed condition, not the
  implementation layer that noticed it, unless that layer is the domain.
- A lifecycle event should be a fact that happened, not a command the
  receiver should run.

The balance point is exactness without namespace noise. Repetition that
comes from crate prefixes, role prefixes, and generic suffixes should be
removed. Repetition that comes from naming the actual relation vector is
acceptable until examples prove a cleaner phrase.

---

## Bottom Line

The contract system is pointed in the right direction, but the edge
contracts need a deliberate naming sweep before more consumers compile
against them.

The most important immediate fixes are:

1. noun-form root vectors in the Persona channel contracts;
2. typed fields instead of raw strings/u64s at Persona edges;
3. role taxonomy correction in `signal-persona-mind`;
4. removal of generic `Ok`/`Generic`/`Mixed` placeholders in
   `signal-persona`;
5. explicit relation sentences in every contract architecture file.

After those land, the contract repos will be much closer to doing what
they should do: enforce the right architecture by making the wrong
program hard to write.
