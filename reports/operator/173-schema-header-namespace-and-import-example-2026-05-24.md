# 173 - Schema header namespace and import example, 2026-05-24

## Context

This report responds to the psyche's correction to
`reports/designer/326-v7-spirit-complete-schema-vision.md` and cross-checks it
against the subsequently landed
`reports/designer/326-v8-spirit-complete-schema-vision.md`.

Spirit records captured for this correction:

- 477 - headers are enum namespace nodes, not one payload pair per verb.
- 478 - root header variants are limited; nested header variants are broad.
- 479 - schema lowering should emit and store a fully expanded mid
  representation.
- 480 - schema imports need selective object import as well as load-all.

The code currently landed in `signal-frame`, `signal-persona-spirit`, and
`persona-spirit` implements the v7/v8 Form 1 pair shape:

```nota
(State Statement)
```

That shape remains valid for a single payload. The missing target is Form 2,
the header namespace shape for multiple sub-variants:

```nota
(Watch [State Records ObservationStream])
```

## Corrected Mental Model

The first schema header field is an enum namespace field. It is a vector because
enum declaration order matters. Each item inside it is parsed in enum
declaration context.

At the root header level, per `/326-v8`:

- A bare PascalCase identifier is a unit root variant.
- A parenthesized entry is a data-carrying root variant.
- Form 1 uses one payload type: `(State Statement)`.
- Form 2 uses a sub-enum payload: `(Watch [State Records ObservationStream])`.
- The root data-carrying variant count is constrained, currently framed as at
  most seven.

Inside a Form 2 bracket namespace:

- The nested tokens are endpoint header variants.
- The nested endpoint variants have a broad slot budget, currently framed as up
  to 256.
- The endpoint names resolve against the schema namespace during lowering.
- The lowered representation connects each endpoint to the body schema and
  emitted Rust type.

So the header is a fast dispatch trie. Spirit's current simple case can stay
Form 1:

```nota
[
  (State Statement)
  (Record Entry)
  (Observe Observation)
  (Watch Subscription)
  (Unwatch SubscriptionToken)
]
```

A future richer Watch relation would use Form 2:

```nota
[
  (State Statement)
  (Record Entry)
  (Observe Observation)
  (Watch [State Records ObservationStream])
  (Unwatch SubscriptionToken)
]
```

This says:

- first short-header slot chooses the root: `State`, `Record`, `Observe`,
  `Watch`, `Unwatch`;
- for Form 1, the root directly selects one payload type;
- for Form 2, the second short-header slot chooses the endpoint inside that
  root, such as `Watch.State` or `Watch.Records`;
- after header triage selects the root and optional sub-endpoint, the receiver
  knows which body schema to decode.

## Deeper Spirit Example

This is a worked example of the shape the schema language is aiming at. It is
not accepted by today's parser because Form 2 and selective imports are not yet
implemented.

```nota
{
  SignalSema ((Path schemas/signal-sema/signal-sema.schema)
    (Some [Magnitude SemaOperation SemaOutcome SemaObservation]))
  SchemaCore ((Path schemas/schema/base.schema) All)
}

[
  (State Statement)
  (Record Entry)
  (Observe Observation)
  (Watch [State Records ObservationStream])
  (Unwatch SubscriptionToken)
]

[]

[]

{
  Kind [Decision Principle Correction Clarification Constraint]
  ObservationMode [SummaryOnly WithProvenance]
  Presence [Active Absent]
  UnimplementedReason [NotBuiltYet IntegrationNotLanded]

  Topic (String)
  Summary (String)
  Context (String)
  Quote (String)
  StatementText (String)
  FocusArea (String)
  RecordIdentifier (u64)
  QuestionIdentifier (String)
  QuestionText (String)
  StateSubscriptionToken (u64)
  RecordSubscriptionToken (u64)

  Entry (Topic Kind Summary Context Magnitude Quote)
  Statement (StatementText)
  Observation [State (Records RecordQuery) Topics Questions]
  Subscription [State (Records RecordSubscription) ObservationStream]
  SubscriptionToken [(State StateSubscriptionToken) (Records RecordSubscriptionToken)]

  ObservationStream (ObservationMode)
  RecordQuery ([Option Topic] [Option Kind] ObservationMode)
  RecordSubscription ([Option Topic] ObservationMode)
  RecordSummary (RecordIdentifier Topic Kind Summary Magnitude)
  RecordProvenance (RecordSummary Context Date Time Quote)
  TopicCount (Topic u64)
  State (Presence [Option FocusArea])
  QuestionSummary (QuestionIdentifier QuestionText)

  SubscriptionSnapshot [(State State) (Records [Vec RecordSummary])]

  RecordAccepted (RecordIdentifier)
  StateObserved (State)
  RecordsObserved ([Vec RecordSummary])
  RecordProvenancesObserved ([Vec RecordProvenance])
  TopicsObserved ([Vec TopicCount])
  QuestionsObserved ([Vec QuestionSummary])
  SubscriptionOpened (SubscriptionToken SubscriptionSnapshot)
  SubscriptionRetracted (SubscriptionToken)
  RequestUnimplemented (UnimplementedReason)

  StateChanged (State)
  RecordCaptured (RecordSummary)

  OperationReceived (OperationKind)
  EffectEmitted (SemaObservation)
}

[
  (Reply
    RecordAccepted
    StateObserved
    RecordsObserved
    RecordProvenancesObserved
    TopicsObserved
    QuestionsObserved
    SubscriptionOpened
    SubscriptionRetracted
    RequestUnimplemented)

  (Event (belongs DomainStream)
    StateChanged
    RecordCaptured)

  (Observable
    (filter default)
    (operation_event OperationReceived)
    (effect_event EffectEmitted))
]
```

The example intentionally keeps Spirit's current Form 1 `State Statement` and
uses Form 2 only where it is useful: `Watch` has several watch targets. This
matches `/326-v8`'s rule that a one-subvariant bracket namespace collapses to
Form 1.

## Import Shape

The import field is a map from import binding names to import specifications.
An import specification carries:

- where to load from;
- which names to import.

The selection is not ordinary absence. It is an all-or-some choice:

```nota
AllOrSome [All (Some [Vec EnumIdentifier])]
```

So this:

```nota
SignalSema ((Path schemas/signal-sema/signal-sema.schema)
  (Some [Magnitude SemaOperation SemaOutcome SemaObservation]))
```

means "load this schema and import exactly these names."

And this:

```nota
SchemaCore ((Path schemas/schema/base.schema) All)
```

means "load this schema and import the whole exported namespace."

Designer `/326-v8` uses a compact shorthand:

```nota
SemaSet (Path ../signal-sema/operation.schema [SemaOperation SemaOutcome SemaObservation])
```

Both sketches express the same semantics: default all, specified list means
some. The final parser should choose one concrete surface and keep the lowered
mid-representation explicit.

## Lowered Mid Representation

The short schema should lower into a fully expanded mid representation. The mid
representation is the schema daemon's durable object: it can be stored, queried,
diffed, and used for version migration.

A simplified lowered shape for the header above would look like:

```nota
(SchemaMid
  Spirit
  [
    (Import SignalSema schemas/signal-sema/signal-sema.schema
      [Magnitude SemaOperation SemaOutcome SemaObservation])
    (Import SchemaCore schemas/schema/base.schema All)
  ]
  [
    (HeaderRoot State 0 Statement)
    (HeaderRoot Record 1 Entry)
    (HeaderRoot Observe 2 Observation)
    (HeaderRoot Watch 3 [State Records ObservationStream])
    (HeaderRoot Unwatch 4 SubscriptionToken)
  ]
  [
    (Endpoint State spirit::namespace::Statement)
    (Endpoint Record spirit::namespace::Entry)
    (Endpoint Observe spirit::namespace::Observation)
    (Endpoint Watch State spirit::namespace::State)
    (Endpoint Watch Records spirit::namespace::RecordSubscription)
    (Endpoint Watch ObservationStream spirit::namespace::ObservationStream)
  ])
```

This is intentionally more explicit than the authored `.schema` file. The
authored file is beautiful short syntax. The mid object is for machines:
expanded imports, slot assignments, endpoint resolution, and fully qualified
names.

## Implementation Consequence

The code that just landed is now a useful partial implementation, not the full
target. It proves file-body parsing, import-first parsing, path imports,
namespace forms, aliases, Form 1 header pairs, and current short-header
emission under Nix. The next code pass should add the v8 pieces:

- parse root header entries as root enum nodes;
- parse bracket payloads as nested endpoint namespaces when there is more than
  one sub-variant;
- keep `(State Statement)` as the Form 1 single-payload case;
- add selective `(Path file [Name1 Name2])` imports and `AllOrSome`;
- lower root + endpoint to a mid representation before emitting Rust;
- generate or resolve endpoint body payload types from the schema namespace;
- preserve short-header tests so root and endpoint slots are witnessed.

## Intent Clarification Needed

The one decision that still needs sharp confirmation before code continues:

In Form 2, can nested sub-variants themselves be data-carrying header syntax,
or should they remain header-unit selectors whose complex data lives only in
the resolved body schema?

Designer `/326-v8` says recursive data-carrying sub-variants are allowed. My
operator concern is implementation clarity: if nested header nodes can also
carry data, the short-header trie and body-schema resolution need a sharper
rule for where header structure ends and body payload structure begins.
