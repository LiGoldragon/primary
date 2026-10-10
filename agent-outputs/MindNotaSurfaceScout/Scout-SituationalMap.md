# Mind NOTA Surface Scout

Task: inspect current `mind`, `signal-mind`, `spirit`, and `signal-spirit` surfaces for accepted-knowledge usability, without implementing changes. Scope is public/local source and read-only Spirit query evidence.

Commands and sources consulted:

- `spirit "(PublicTextSearch [mind nota spirit contract accepted knowledge])"` and `spirit "(Lookup qjrf)"`.
- `ghq list --full-path | rg '(mind|spirit)'`.
- `jj status` in `/git/github.com/LiGoldragon/mind` and `/git/github.com/LiGoldragon/signal-mind`.
- `rg` and `nl -ba ... | sed -n ...` across `/git/github.com/LiGoldragon/mind`, `/git/github.com/LiGoldragon/signal-mind`, `/git/github.com/LiGoldragon/spirit`, and `/git/github.com/LiGoldragon/signal-spirit`.

Observed local state:

- `mind` working copy is clean. Parent commit is `0d786c4d main | mind: add accepted knowledge storage`.
- `signal-mind` working copy is clean. Parent commit is `025e2116 main | signal-mind: add accepted knowledge contract v1`, matching the brief.
- `/home/li/primary/lore/AGENTS.md` was referenced by `mind/AGENTS.md` but was absent or empty in this checkout. No extra lore guidance was applied.

## 1. Current Mind Exposure Points

Observed facts:

- `signal-mind` declares accepted-knowledge roots in `schema/signal-mind.concept.schema:150-207`. The current schema uses plain string newtypes for `KnowledgeStableKey` and `KnowledgeDomainKey` at lines 160-164, with canonical examples `domain:component`, `domain:contract`, `component:mind`, `repo:signal-mind`, and `contract:signal-mind:ordinary`. It also uses `(Option ...)` heavily: `KnowledgeRecordHeader` at line 167, entity/domain/source descriptions at lines 168, 170, and 171, relation endpoint stable keys at line 172, relation notes at line 173, candidate fields at lines 180-184, relation drafts at line 191, rejection retry hints at line 195, and `RelationSelector` optionals at line 207.
- `signal-mind/src/knowledge.rs:32-155` implements `KnowledgeStableKey` and `KnowledgeDomainKey` as strings with hand-written `NotaDecode`.
- `signal-mind/src/knowledge.rs:158-204` enforces colon-delimited key shape by splitting on `:`. Generic keys require at least two segments; domain keys must start with `domain`; allowed characters include `:` at lines 187-194.
- `signal-mind/src/knowledge.rs:317-380` exposes many `Option` fields in accepted records: `stable_key`, `description`, endpoint `stable_key`, and relation `note`.
- `signal-mind/src/knowledge.rs:540-582` exposes `Option` fields in submitted candidates: optional stable keys, descriptions, and relation notes.
- `signal-mind/src/knowledge.rs:623-676` exposes accepted drafts and rejections with vectors plus optional retry hints.
- `signal-mind/src/knowledge.rs:791-795` exposes relation query filters as optional kind/source/target.
- `signal-mind/tests/round_trip.rs:1487-1519` makes the colon shape normative: it asserts `contract:signal-mind:ordinary` and `domain:component` round-trip as NOTA text, rejects `component` for missing separator, rejects `component:mind` as a domain key, and rejects uppercase segments.
- `signal-mind/tests/round_trip.rs:580-659` and `mind/tests/actor_topology.rs:581-676` fixture accepted-knowledge records with `domain:component`, `component:mind`, `contract:signal-mind:ordinary`, `repo:signal-mind`, `statement:architecture:old`, `statement:architecture:new`, and `source:mind-architecture`.
- `mind/src/knowledge.rs:302-312` puts `domain:component` directly into the AI judge prompt's accept example. `mind/tests/actor_topology.rs:950-977` proves the fake-agent prompt includes `domain:component`.
- `mind/src/knowledge.rs:250-274` tells the judge that a valid accept is shaped like that generated example. This likely encouraged the live model to copy the example.
- `mind/src/knowledge.rs:396-411` accepts the judge verdict, and `mind/src/knowledge.rs:451-458` applies an accepted draft. There is no observed deterministic check in this path that the accepted draft corresponds to `self.candidate`.
- `mind/src/knowledge.rs:480-536` only checks non-empty draft, duplicate stable key, materialization, relation endpoint lookup, relation domain/range, and persistence. It does not compare accepted record body/domain/key against the submitted candidate.
- `mind/src/text.rs:108-252` is hand-written/custom NOTA projection machinery for the work-graph convenience surface. `TextOptionalString` renders `None` at lines 234-239 and decodes literal `None` at lines 243-251.
- `mind/src/text.rs:740-844` hand-encodes and hand-decodes convenience request records. `Link` and `StatusChange` use `TextOptionalString` at lines 758-775 and lines 810-825.
- `mind/tests/cli.rs:95-98` includes a user-facing literal `(Link ... None)`.
- `mind/src/command.rs:158-167` tries `MindTextRequest` first, then falls back to parsing the full `signal-mind::MindRequest`. `mind/src/command.rs:184-190` tries `MindTextReply` first, then falls back to full `MindReply`.
- `mind/src/text.rs:1298-1321` explicitly excludes `KnowledgeAccepted`, `KnowledgeRejected`, and `KnowledgeList` from the convenience reply projection, so accepted-knowledge text currently comes from the full `signal-mind` NOTA contract.
- `signal-mind/src/technical.rs:60-124` is the earlier technical key precedent: `TechnicalNodeKey` is also a colon-delimited string shape. Families are mapped at `signal-mind/src/technical.rs:227-260`. This is not the immediate live accepted-knowledge bug, but it is the pattern accepted knowledge copied.

Interpretation:

- The ugly accepted-knowledge surface is not caused by NOTA itself. It is caused by application-level string key design plus exposing Rust-like `Option` shapes through derived or hand-written NOTA.
- The runtime acceptance bug is deterministic: even with a better prompt, `mind` currently treats an AI `Accept` draft as authority to store substitute records. The prompt example made the bug likely, but the missing guard made it possible.

## 2. Spirit Cleaner Model To Imitate

Observed facts:

- Spirit public intent record `qjrf`, observed via `spirit "(Lookup qjrf)"`, says the intent layer holds what the psyche directs or wants, not information or belief. It also says agents ask the psyche when a design surface is incomplete rather than generating plausible synthesis and capturing it as authorized. Conclusion for Mind: accepted knowledge must remain separate from Spirit intent, and replacement shapes should be presented as options for psyche choice.
- `signal-spirit/schema/signal.schema:44-74` uses verb-shaped operation roots: `State`, `Record`, `Observe`, `PublicTextSearch`, `PublicRecords`, `Lookup`, and maintenance verbs. The public input root is a closed enum, not stringly command names.
- `signal-spirit/schema/signal.schema:99-108` declares wrapper nouns such as `Domains`, `Referents`, `Description`, `SearchText`, and `RecordIdentifier`.
- `signal-spirit/schema/signal.schema:122-151` models replies and event records as named structured records.
- `signal-spirit/schema/signal.schema:215-244` models `Entry`, `RecordChange`, `RecordSelection`, and `Query` as structured records over typed domains, kind, magnitudes, referents, and query selectors.
- `signal-spirit/schema/domain.schema:5-64` models domains as nested NOTA variants, for example `(Technology (Software (Data SchemaEvolution)))`, not as strings like `domain:technology:software:data:schema-evolution`.
- `signal-spirit/tests/generated_contract.rs:430-458` proves domain NOTA round trips as `(Technology (Software Data))` and `(Technology (Software (Data SchemaEvolution)))`.
- `signal-spirit/src/schema/signal.rs:840-843` shows generated `RecordRequest { entry, justification }`; `signal-spirit/src/schema/signal.rs:1541-1549` shows generated `Entry { domains, kind, description, certainty, importance, privacy, referents }`.
- `signal-spirit/src/schema/signal.rs:1960-1984` shows the generated closed `Input` enum. `signal-spirit/src/schema/signal.rs:5162-5173` implements `FromStr` and `Display` through generated NOTA decoding/encoding.
- `spirit/src/bin/spirit.rs:71-103` accepts exactly one NOTA input and parses it into generated `Input`; it does not maintain a second hand-written command language.
- `spirit/README.md:47-60` gives ergonomic CLI examples: `Record`, structured `Observe`, and `PublicTextSearch`.
- `spirit/ARCHITECTURE.md:68-78` says Spirit's schema keeps braces strict as NOTA maps and uses exported aliases, avoiding self-repeating wrapper declarations.
- `spirit/ARCHITECTURE.md:388-400` describes `PublicTextSearch`, `PublicRecords`, and `PrivateRecords` as ergonomic read shortcuts that preserve a full structured query beneath.

Important caveat:

- Spirit still exposes `Some` and `None` in some generated query examples, such as `signal-spirit/examples/canonical.nota:7-12`, `spirit/README.md:77-78`, and `spirit/tests/generated_signal_plane.rs:398-432`. The cleaner part to imitate is the nested typed domain and generated contract shape, not optional-wrapper leakage.

Concrete Spirit examples worth imitating:

```nota
(PublicTextSearch [routing protocol])
(Observe (Records ((Full [(Technology (Software (Data SchemaEvolution)))]) (Some Decision) Any Any SummaryOnly)))
(Record (([(Technology (Software (Data SchemaEvolution)))] Constraint [schema creates the interface] Maximum Minimum Zero []) ([schema creates the interface] None)))
```

Better still, for Mind's target, imitate the nested domain style while removing optionals from the visible accepted-knowledge surface.

## 3. Replacement Mind NOTA Shape Options

These are options for psyche choice, not assumptions.

### Option A: Structured Identity Enum Plus Keyed/Unkeyed Variants

Core idea: replace `KnowledgeStableKey(String)` and `KnowledgeDomainKey(String)` with typed enums and use explicit keyed/unkeyed variants instead of `Option<KnowledgeStableKey>`. Use empty vectors for absent descriptions, notes, about-lists, and domains.

Possible schema concepts:

```text
KnowledgeIdentity [
  (Component ComponentName)
  (Repository RepositoryName)
  (Crate CrateName)
  (Contract RepositoryName ContractSurface)
  (Statement StatementName)
  (Source SourceName)
  (Domain KnowledgeDomain)
]
KnowledgeDomain [Component Contract Repository Architecture Interface Storage]
KnowledgeEntityCandidate [
  (Keyed KnowledgeIdentity EntityName DescriptionLines Domains)
  (Unkeyed EntityName DescriptionLines Domains)
]
KnowledgeStatementCandidate [
  (Keyed KnowledgeIdentity StatementText AboutIdentities Domains)
  (Unkeyed StatementText AboutIdentities Domains)
]
```

Example NOTA:

```nota
(SubmitKnowledge (Entity (Keyed (Component mind) [Mind] [] [Component]) FixtureOnly []))
(SubmitKnowledge (Statement (Keyed (Statement accepted-knowledge-store) [Mind owns accepted knowledge through the accepted-knowledge store.] [(Component mind)] [Component]) FixtureOnly []))
(QueryKnowledge (GetByIdentity (Component mind)))
(QueryKnowledge (ListByDomain (Direct Component) CurrentOnly))
```

Pros:

- Removes colon-delimited pseudo-identifiers while preserving exact query/update identity.
- Makes identity family typed, so `Component mind` cannot accidentally be used as a domain key unless the enum allows it.
- Keeps existing `SubmitKnowledge` and `QueryKnowledge` roots.
- Explicit keyed/unkeyed variants avoid public `Some`/`None`.

Cons:

- Largest contract churn in `signal-mind`.
- Requires persistence migration or compatibility bridge for existing stored `AcceptedKnowledge`.
- Requires deciding the initial closed identity/domain vocab.

### Option B: Separate Identity Bindings From Accepted Knowledge Content

Core idea: accepted records get only daemon-minted `KnowledgeIdentifier` values. Human-facing identity is its own accepted record or relation, similar to Spirit referents. Colon strings disappear because identity is a structured binding record.

Possible schema concepts:

```text
KnowledgeName [
  (Component ComponentName)
  (Repository RepositoryName)
  (Contract RepositoryName ContractSurface)
  (Domain KnowledgeDomain)
]
KnowledgeNameBinding { KnowledgeName KnowledgeIdentifier }
KnowledgeCandidate [
  (Entity EntityName DescriptionLines Domains)
  (Statement StatementText AboutIdentifiers Domains)
  (Domain KnowledgeDomain DomainName DescriptionLines)
  (NameBinding KnowledgeName KnowledgeEndpointSelector)
]
```

Example NOTA:

```nota
(SubmitKnowledge (Domain Component [Component] [] FixtureOnly []))
(SubmitKnowledge (Entity [Mind] [] [Component] FixtureOnly []))
(SubmitKnowledge (NameBinding (Component mind) (Identifier kabc) FixtureOnly []))
(QueryKnowledge (GetByName (Component mind)))
```

Pros:

- Normalizes naming as knowledge instead of embedding a stable key in every record.
- Supports multiple names/aliases and later renames without mutating record payloads.
- Very close to Spirit's referent/identifier separation.

Cons:

- More verbose and likely multi-step unless the daemon creates binding and content in one transaction.
- Query identity now depends on an extra binding lookup.
- Harder to keep one-submission ergonomics unless the contract adds a composite submission variant.

### Option C: Spirit-like Domain and Search First, Opaque IDs for Exact Identity

Core idea: remove stable keys from accepted content. Use nested typed domains, opaque daemon IDs for exact reads, and ergonomic search/query roots for user lookup. Structured names may be plain content, not identity.

Possible schema concepts:

```text
KnowledgeDomain reuse-or-mirror signal-spirit Domain subset
KnowledgeQuery [
  (Search SearchText DomainSelection CurrentView QueryLimit)
  (GetByIdentifier KnowledgeIdentifier)
  (ListByDomain DomainSelection CurrentView)
]
```

Example NOTA:

```nota
(SubmitKnowledge (Statement [Mind owns accepted knowledge through the accepted-knowledge store.] [] [(Technology (Software (Data Modeling)))] FixtureOnly []))
(QueryKnowledge (Search [accepted knowledge store] [(Technology (Software Data))] CurrentOnly 10))
(QueryKnowledge (GetByIdentifier kabc))
```

Pros:

- Cleanest visible text for ad hoc use.
- Closest to Spirit's `PublicTextSearch` and nested domain model.
- Avoids prematurely canonicalizing every entity as a stable key.

Cons:

- Does not preserve stable update identity by itself; exact correction/supersession must use opaque IDs.
- Less useful for components that need idempotent upserts or stable cross-references.
- Search quality becomes part of usability.

## 4. Recommendation

Recommend Option A as the first replacement surface.

Reasoning:

- The brief requires preserving query/update identity and typed structure. Option A preserves that directly without colon strings.
- It is the smallest conceptual migration from current `KnowledgeStableKey` and `KnowledgeDomainKey`: replace string syntax with typed enum syntax, keep `SubmitKnowledge`, `QueryKnowledge`, `AcceptedKnowledge`, relation endpoint selectors, and relation validation.
- It gives the AI judge less opportunity to invent or copy pseudo-identifiers, because identities are typed record payloads like `(Component mind)` or `(Contract signal-mind Ordinary)`.
- It can still borrow Spirit's nested domain style. Mind-local `KnowledgeDomain` can start small, or it can reuse a relevant `signal-spirit` domain subset later.

Tradeoffs:

- Option A still needs closed vocab decisions. That is good for correctness but requires psyche/design choice before implementation.
- Option B is more normalized and elegant long-term, but it risks making the first usable CLI too ceremony-heavy.
- Option C is the nicest casual text interface, but it weakens stable identity unless paired with Option A or B later.

## 5. Judge Contract Change

Observed current bug path:

- Prompt example is built in `mind/src/knowledge.rs:250-274`.
- Accept example hardcodes `domain:component` and `description: None` in `mind/src/knowledge.rs:302-312`.
- The user prompt includes the packet at `mind/src/knowledge.rs:277-285`.
- The agent verdict is parsed at `mind/src/knowledge.rs:164-170` and returned at `mind/src/knowledge.rs:204-207`.
- `KnowledgeAdmission::reply_from_judge` applies any accepted draft at `mind/src/knowledge.rs:396-411`.
- `KnowledgeDraftApplication::accepted` stores whatever valid draft appears at `mind/src/knowledge.rs:480-536`.

Recommended contract behavior:

- The judge should judge the submitted candidate. It may return only:
  - `Reject(KnowledgeRejection)`, or
  - `Accept(KnowledgeAcceptance)` that references the submitted candidate, not arbitrary replacement accepted records.
- Deterministic code should materialize accepted records from the original submitted candidate, plus only explicitly allowed adjuncts.
- If semantic judgment needs a better shape, the judge should return a typed rejection such as `NeedsMoreSpecificShape`, not a substituted record.

Concrete replacement patterns:

1. Minimal guard over current contract:
   - Keep `KnowledgeJudgeVerdict::Accept(AcceptedKnowledgeDraft)`.
   - Add `AcceptedDraftCorrespondence` validation before `apply_draft`.
   - Require at least one draft record to be same family as the submitted `KnowledgeCandidate`, with matching body/name/domain identity after canonicalization.
   - Permit additional relation/source records only if their endpoints include the accepted candidate or already existing neighbors.
   - Reject copied examples with `StructuralPreflightFailed(CandidateMismatch)` or a new explicit mismatch reason.

2. Stronger contract:
   - Replace accepted draft return with `Accept(KnowledgeAcceptanceDecision)`.
   - `KnowledgeAcceptanceDecision` carries semantic annotations only: maybe `domains`, `relation intents`, `source required?`, `supersedes`, `confidence`, but not full substitute records.
   - Mind materializes from `self.candidate`.

Likely affected implementation surfaces:

- `signal-mind/schema/signal-mind.concept.schema:150-207`: accepted knowledge schema, identity/domain key shapes, judge verdict, rejection reasons, query selectors.
- `signal-mind/src/knowledge.rs:32-204`: key types and validators.
- `signal-mind/src/knowledge.rs:291-380`: accepted record structs.
- `signal-mind/src/knowledge.rs:503-646`: submission, candidate, judge packet/verdict/draft structures.
- `signal-mind/src/knowledge.rs:731-796`: structural rejection and query selector shapes.
- `signal-mind/src/lib.rs:1255-1311`: likely operation/reply names can stay, but imports and operation payload types will change if the schema changes.
- `signal-mind/tests/round_trip.rs:1487-1703`: accepted-knowledge key, request/reply, and verdict round trips must be replaced.
- `signal-mind/tests/schema_drift.rs:96-125`: currently requires `KnowledgeDomainKey`, `domain:component`, and `contract:signal-mind:ordinary`; those assertions should change.
- `mind/src/knowledge.rs:227-326`: prompt generation and examples.
- `mind/src/knowledge.rs:396-458`: verdict application and candidate/draft correspondence.
- `mind/src/knowledge.rs:480-647`: materialization and relation materialization.
- `mind/src/knowledge.rs:676-959`: identity resolution and query engine.
- `mind/src/tables.rs:45-56`, `108-110`, `514-518`, and `921-940`: stored accepted-knowledge table and archived payload shape.
- `mind/tests/actor_topology.rs:581-676`, `838-947`, and `950-1017`: fixture judge, relation preflight, prompt, malformed verdict, and new substituted-verdict rejection tests.
- `mind/src/bin/mind_write_configuration.rs:209-256` and `mind/src/configuration.rs:19-43` only matter if judge configuration text is included in the cleanup; the accepted-knowledge surface itself does not require changing them.
- `mind/src/text.rs:108-252` and `740-844` are not the accepted-knowledge path, but they are the visible hand-written NOTA surface that leaks `None` for work-graph convenience operations. If the usability sweep includes all Mind NOTA, this file needs a separate cleanup.

## 6. Validation For Implementer

Recommended validation:

- In `signal-mind`, update and run accepted-knowledge NOTA round-trip tests:
  - New structured identity examples round-trip without `:`.
  - New domain examples round-trip as typed variants, not `domain:*` strings.
  - Accepted-knowledge candidates and replies render no public `Some` or `None` for empty stable identity, description, note, retry hint, or relation selector cases.
  - Invalid identity family/domain combinations reject structurally.
  - Relation domain/range validation still rejects invalid endpoint kinds.
- Add a targeted `signal-mind` schema drift test replacing `domain:component` and `contract:signal-mind:ordinary` assertions with the chosen typed examples.
- In `mind`, add a fake-agent test where the submitted candidate is a statement but the judge returns the current prompt example domain. Expected result: `KnowledgeRejected`, no `accepted_knowledge` records stored, and the rejection reason identifies candidate/draft mismatch.
- In `mind`, add a fake-agent test where the judge accepts a transformed but corresponding record only if that transformation is explicitly allowed by the selected contract. If no transformations are allowed, the test should reject any body/key/domain change.
- In `mind`, add a happy-path fake-agent test for the chosen structured identity shape, then query by identity and by domain.
- In `mind`, add a persistence reopen test if stored `AcceptedKnowledge` shape changes.
- Run `cargo test -p signal-mind` or the repo's equivalent Nix check in `/git/github.com/LiGoldragon/signal-mind`.
- Run `cargo test -p mind` or the repo's equivalent Nix check in `/git/github.com/LiGoldragon/mind`.
- Run clippy and Nix package/checks matching the prior portability closeout if the implementer changes Cargo/Nix pins.
- Run a real CLI smoke test against a daemon with `AgentKnowledgeJudge` where the submitted candidate differs from the old prompt example. Verify the persisted record corresponds to the submitted candidate and the prompt example is not stored.

Unknowns and blockers:

- I did not run tests because this was a read-only scout task and tests may write build artifacts.
- I did not inspect a live `.sema` store or private data.
- I did not inspect `meta-signal-mind`; the accepted-knowledge user surface appears to be in ordinary `signal-mind` plus `mind`.
- The exact replacement domain vocabulary needs psyche choice. Option A is recommended, but not assumed.
- Existing stored accepted-knowledge rows, if any, need an explicit migration or compatibility story because `StoredAcceptedKnowledge` archives the full contract type.
