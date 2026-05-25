*Kind: Pattern Audit + Concept Synthesis · Topic: Interact trait + match-as-logic pattern across recent code · Date: 2026-05-25 · Lane: second-designer*

# 195 — The Interact trait + match-as-logic pattern across recent code

## §1 Frame

Per psyche directive 2026-05-25: "Refresh all intent and fresh reports and do an audit of common code patterns in the things that we're working on recently... we need most of the logic to be matches. So we create one domain and another domain and they match together... we should basically make this all into a trait. So like this `Interact` trait... let me know if I seem to not have finished my thought here."

Captures: intent 652 (Interact-trait universal interaction) + 653 (match-as-logic substrate principle) + 654 (typed Unavailable at unmatched cases) + 655 (async state query via actor system).

This report does five things: (1) frames the Interact-trait concept; (2) audits recent code for match-as-logic patterns; (3) shows representative examples from current landings; (4) names where the pattern works + where it strains; (5) flags the incomplete-thought question the psyche asked me to check.

## §2 The Interact trait — psyche's new universal interaction concept

```rust
// Conceptual — psyche's framing translated to Rust trait shape:

pub trait Interact {
    type Other;     // the domain we interact WITH
    type Outcome;   // typed outcome enum (includes Unavailable/Unauthorized/etc.)

    async fn interact(&self, other: Self::Other) -> Self::Outcome;
}
```

The trait is universal. Every object that participates in workspace logic implements `Interact`. The interaction is INHERENTLY between two domains (the self object + the other object). The engine's state is IMPLICIT — accessed via the engine's actor surface when needed (e.g., authorization checks). The async signature lets the actor system suspend the interaction while waiting on outbound state queries.

The `Outcome` type is a typed enum carrying both the SUCCESS shapes AND the FAILURE shapes (Unavailable / Unauthorized / NotImplemented / etc. per intent 654). The caller matches on `Outcome` and dispatches accordingly — the failure cases are not exceptions or unhandled-defaults, they're first-class variants.

### §2.1 Why universal

Three reasons the trait wants to be universal:
1. **Every component does interactions**: schema lowers macro × NotaValue; daemon dispatches header × Operation; supervisor coordinates handover-state × ceremony-message; orchestrate matches lane × claim. The shape is identical across components.
2. **The engine substrate provides state implicitly**: object can ask "is this authorized?" without the caller threading the auth credential; the engine actor handles the query routing.
3. **Async-by-default matches the actor system**: every interaction can suspend at any state query; other actors run concurrently; the wait is invisible to the caller.

### §2.2 Match-as-logic — the load-bearing principle

Per intent 653: most workspace logic IS a match between two domains. Two enums interact; the match-matrix per cell is the engine's behavior. The trait formalizes this: every `Interact` implementation is effectively a typed match between `Self` and `Self::Other`, producing a typed `Outcome`.

Where the match has no defined behavior, the typed `Outcome` returns Unavailable/NotImplemented/etc. The error surface is part of the trait — not an exception.

This generalizes the **enum-contact-points** pattern (per `skills/enum-contact-points.md` Apex skill + designer/338 §2 + operator/182's `NodeDefinitionShape × NotaValueKind`) from a schema-engine-specific pattern to a workspace-universal trait.

## §3 The match-as-logic pattern in recent code

The pattern is observable across multiple recent landings. Each is structurally `(Domain_A × Domain_B) → Outcome`. Concrete examples:

### §3.1 Schema engine — `NodeDefinitionShape × NotaValueKind` → recognizer dispatch

Per operator/181 §"Architecture Reading" + operator/182 + my /190 + /192:

```rust
// schema/src/node_shape.rs — operator/182 commit 2288914c
match (node_definition_point, value.kind()) {
    (NodeDefinitionPoint::Imports, NotaValueKind::Map)
        => Ok(NodeDefinitionShape::ImportDirective),
    (NodeDefinitionPoint::OrdinaryHeader, NotaValueKind::Sequence)
        => Ok(NodeDefinitionShape::HeaderRoot),
    (NodeDefinitionPoint::Namespace, NotaValueKind::Map)
        => Ok(NodeDefinitionShape::NamespaceValue(/* nested classification */)),
    (NodeDefinitionPoint::Features, NotaValueKind::Sequence)
        => Ok(NodeDefinitionShape::FeatureItem),
    (point, kind) => Err(point.unexpected_kind(kind)),
}
```

Two enums (NodeDefinitionPoint × NotaValueKind) match into the NodeDefinitionShape outcome (or a typed error). The unmatched cell returns `point.unexpected_kind(kind)` — typed-error per intent 654.

### §3.2 Schema namespace recognizer — `NamespaceValueShape × NotaValue inspection` → transformation

Per operator/182's `NamespaceValueShape`:

```rust
// Conceptual:
match namespace_value_shape {
    NamespaceValueShape::Enum     => EnumShortSyntaxMacro::apply(name, value, context),
    NamespaceValueShape::Record   => StructShortSyntaxMacro::apply(name, value, context),
    NamespaceValueShape::Newtype  => NewtypeShortSyntaxMacro::apply(name, value, context),
    NamespaceValueShape::Alias    => AliasReferenceMacro::apply(name, value, context),
}
```

Single-domain match (NamespaceValueShape) into transformation macro. Cells are total per enum-exhaustiveness.

### §3.3 Upgrade plan derivation — `(previous AssembledType, current AssembledType) × annotations` → Projection

Per `schema/src/upgrade.rs` + my /182 §4:

```rust
// Conceptual algorithm from AssembledSchema::plan_upgrade_from:
match (previous_type, current_type, annotations.get(name)) {
    (Some(prev), Some(curr), _) if prev == curr
        => Projection::Identity { name },
    (Some(prev), Some(curr), _) if additive_enum_variant(prev, curr).is_some()
        => Projection::Standard { name, kind: StandardProjection::AdditiveEnumVariant },
    (Some(_), Some(_), Some(UpgradeAnnotation::Migrate(_)))
        => Projection::Annotated { name, annotation },
    (None, Some(_), _)
        => Projection::Added { name },
    (Some(_), None, Some(UpgradeAnnotation::RenamedFrom { previous, .. }))
        => Projection::Renamed { current: name, previous },
    (Some(_), None, Some(UpgradeAnnotation::Drop(_)))
        => Projection::Dropped { name },
    (Some(_), None, Some(UpgradeAnnotation::Untranslatable(_)))
        => Projection::Untranslatable { name },
    (Some(_), None, None)
        => Err(RemovedTypeRequiresAnnotation { name }),
    (Some(_), Some(_), None) if prev != curr
        => Err(MissingUpgradeAnnotation { name }),
}
```

Three-domain match (prev × curr × annotation) producing typed Projection enum (or typed error). The 7 projection kinds are the elegant outcome surface; the 2 error kinds are typed unavailable cases.

### §3.4 Daemon ingress dispatch — `ShortHeader (byte 0 root) × decoded body` → handler

Per /176 §5.3:

```rust
// Macro-emitted on the daemon:
match header.byte_0() {
    0 => self.handle_state(body),
    1 => self.handle_record(body),
    2 => self.handle_observe(header.byte_1(), body),
    3 => self.handle_watch(header.byte_1(), body),
    4 => self.handle_unwatch(header.byte_1(), body),
    _ => Reply::RequestUnimplemented(UnimplementedReason::NotBuiltYet),
}
```

Single-byte match (root_slot) into typed handler dispatch. The unmatched cell returns typed `RequestUnimplemented` — exactly the Unavailable pattern per intent 654.

### §3.5 Handover ceremony — `HandoverState × signal-version-handover::Operation` → state transition

Per /175 §7 + /186 + persona-spirit/src/daemon.rs:

```rust
// Conceptual — distilled from existing daemon reply_to_operation:
match (current_state, incoming_operation) {
    (Serving,            AskHandoverMarker(_))    => transition_to(MarkerOffered, reply_with_marker()),
    (MarkerOffered,      Mirror(payload))         => transition_to(MirrorStreaming, apply_mirror(payload)),
    (MarkerOffered,      ReadyToHandover(report)) => transition_to(Acknowledging, validate_and_ack(report)),
    (Acknowledging,      HandoverCompleted(_))    => transition_to(Completing, retire_public_sockets()),
    (any_state,          Divergence(reason))      => transition_to(Diverged, abort_handover(reason)),
    (any_state,          RecoverFromFailure(_))   => transition_to(Recovery, attempt_recovery()),
    (state, op)                                   => Err(InvalidStateTransition { state, op }),
}
```

Two-domain match (HandoverState × Operation) producing transition + reply. Invalid combinations return typed `InvalidStateTransition` error — Unavailable per intent 654.

### §3.6 Orchestrate lane claim — `Lane × ClaimRequest` → ClaimOutcome

Per second-operator/186 + my /173 phase 1:

```rust
// Conceptual — orchestrate's claim resolution:
match (lane.current_state, request.claim_kind) {
    (LaneState::Free,        ClaimKind::Acquire)        => ClaimOutcome::Granted { token: mint_token() },
    (LaneState::Free,        ClaimKind::Release)        => ClaimOutcome::AlreadyFree,
    (LaneState::Held(holder), ClaimKind::Acquire) if holder == requester
                                                         => ClaimOutcome::AlreadyHeld { token: holder.token },
    (LaneState::Held(_),     ClaimKind::Acquire)        => ClaimOutcome::Conflict { current_holder },
    (LaneState::Held(holder), ClaimKind::Release) if holder == requester
                                                         => ClaimOutcome::Released,
    (LaneState::Held(_),     ClaimKind::Release)        => ClaimOutcome::NotYourClaim,
}
```

Two-domain match (LaneState × ClaimKind) producing ClaimOutcome with named-failure variants (Conflict / NotYourClaim) — all typed, all matchable.

## §4 Where the pattern works + where it strains

### §4.1 Works well

- **Single-match-on-incoming-operation** (§3.4 daemon dispatch): clean; macro can emit; exhaustiveness is compile-checked
- **State-machine transitions** (§3.5 handover): the typed-state × typed-message matrix is the clearest way to spec a protocol; bugs show up as missing match arms
- **Type-classification** (§3.1 + §3.2 schema): two-domain match is the right shape for "given this position and this shape, dispatch here"; the recognizer pattern operator landed exemplifies
- **Diff algorithms** (§3.3 upgrade): three-domain match enumerates the cases; typed Projection variants make downstream code clear

### §4.2 Strains

- **Async cross-domain queries** (Criome auth, sema-engine queries): pure match doesn't capture the "wait for state" beat. Currently handled in ad-hoc ways — `block_on` in some places, actor `ask` in others, sync queries threaded through closures elsewhere. The Interact trait async signature would unify this.
- **Multi-actor coordination** (handover ceremony across two daemons + supervisor): current implementations have THREE state machines coordinating; the match-per-actor doesn't show the JOINT state. A `JointState × Event` super-match would be cleaner but explodes combinatorially.
- **Variadic-result cases** (header dispatch when sub-variants vary): macro-emitted dispatch handles this but the human-written analog would be deeply nested matches. The schema-driven emission hides the complexity.
- **Wide enum × wide enum**: when both domains are 10+ variants, the match-matrix has 100+ cells. Many are NotImplemented or Unavailable. Visual scan becomes hard; tooling helps but the cell count strains.

### §4.3 What's inelegant or winded today

- **Predicate-chain dispatch** (operator/187's `is_record() && is_pascal_identifier() && ...` chains): functional but harder to read than a typed-enum match. The Interact trait would naturally use enum-domains.
- **Untyped error fallbacks** (`Err(format!("unexpected ..."))`): operator/182 corrected several of these to typed errors with point+kind info. Pattern not yet universal.
- **`if let Some(x) = ...` cascades for option chains**: works but doesn't match-by-shape. Convertible to nested matches; readability trade.

## §5 The typed-Unavailable response surface (intent 654)

Per intent 654: every unmatched cell returns a TYPED response carrying enough information for the caller to dispatch. Today's examples:

| Pattern | Typed response | Caller can match on |
|---|---|---|
| Schema unknown type | `Error::UnknownType { name }` | the missing name |
| Schema duplicate variant | `Error::DuplicateVariant { declaration, variant }` | both names |
| Header empty | `Error::EmptyHeaderRoot { name }` | the empty root |
| Upgrade plan missing annotation | `Error::MissingUpgradeAnnotation { name }` | the type needing annotation |
| Daemon unknown operation | `Reply::RequestUnimplemented(UnimplementedReason::{NotBuiltYet, IntegrationNotLanded})` | the specific unimplemented reason |
| Handover state mismatch | `DivergencePayload { reason: DivergenceReason }` | the typed divergence reason |
| Orchestrate claim conflict | `ClaimOutcome::Conflict { current_holder }` | who holds the claim |

The pattern emerged organically across multiple components. Intent 654 formalizes it: every unmatched cell IS this shape, not an `Err(String)` or panic.

### §5.1 Universal Outcome enum proposal

Under the Interact trait, the `Outcome` type per implementation could include a UNIVERSAL Unavailable variant alongside domain-specific outcomes:

```rust
pub trait Interact {
    type Other;
    type Success;
    type Unavailable;   // typed reasons-for-unavailable per implementation

    async fn interact(&self, other: Self::Other) -> InteractOutcome<Self::Success, Self::Unavailable>;
}

pub enum InteractOutcome<S, U> {
    Granted(S),
    Unavailable(U),                       // typed local-decision reason
    Unauthorized(AuthorizationReason),     // standard cross-cutting case
    NotImplemented { surface: String },    // standard cross-cutting case
    EngineUnavailable(EngineUnavailableReason),  // when the engine actor itself is down
}
```

Each implementation defines its own `Success` + `Unavailable` types. The four cross-cutting outcome variants (Granted / Unavailable / Unauthorized / NotImplemented / EngineUnavailable) are universal — every interaction can return any of them.

## §6 Async state query + actor system integration (intent 655)

Per intent 655: when an interaction needs the engine's state (e.g., authorization check via Criome), the interaction suspends. The actor system handles the wait; other actors run concurrently.

```rust
// Conceptual — what the engine-state-query looks like:

impl Interact for SchemaUpgrade {
    type Other = TargetVersion;
    type Outcome = UpgradeOutcome;

    async fn interact(&self, target: TargetVersion) -> UpgradeOutcome {
        // 1. Engine-state query — async; actor system handles wait
        let authorized = engine_state::ask_criome(
            CriomeQuery::AuthorizeUpgrade { component: self.component(), target }
        ).await;
        if !authorized {
            return UpgradeOutcome::Unauthorized(AuthorizationReason::CriomeDenied);
        }
        // 2. Engine-state query — current version
        let current = engine_state::ask_version(self.component()).await;
        // 3. Match-based dispatch:
        match (current, target) {
            (Version::V010, Version::V011) => self.plan_v010_to_v011().await,
            (Version::V011, Version::V012) => self.plan_v011_to_v012().await,
            (c, t) if c == t => UpgradeOutcome::AlreadyAtTarget,
            (c, t) if t < c  => UpgradeOutcome::CannotDowngrade { current: c, target: t },
            _                => UpgradeOutcome::NoMigrationPath,
        }
    }
}
```

The implementation reads as a top-to-bottom flow:
1. Async state queries (criome auth + current version)
2. Match-based dispatch on version pair
3. Typed Outcome variants for every case

The actor system handles the `await` points. Other interactions run while this one waits. The Interact trait makes this composition idiomatic across the workspace.

## §7 Criome authorization example

Per psyche directive: "is this authorized in the Criome, for example? This is something that would go out."

The Criome interaction itself is an `Interact` impl:

```rust
impl Interact for CriomeClient {
    type Other = CriomeQuery;
    type Outcome = CriomeOutcome;

    async fn interact(&self, query: CriomeQuery) -> CriomeOutcome {
        // Outbound RPC to Criome service
        match query {
            CriomeQuery::AuthorizeUpgrade { component, target }
                => self.rpc_authorize_upgrade(component, target).await,
            CriomeQuery::AuthorizeOperation { actor, op }
                => self.rpc_authorize_op(actor, op).await,
            CriomeQuery::QueryRole(actor)
                => self.rpc_query_role(actor).await,
        }
    }
}

pub enum CriomeOutcome {
    Authorized { proof: AuthProof },
    Denied { reason: DenialReason },
    Pending,                              // async — caller can recheck
    Unavailable(CriomeUnavailable),       // criome service itself unreachable
}
```

The CALLER of CriomeClient gets a typed Outcome they can match on. If denied, the caller's own `Interact` impl returns `Unauthorized(CriomeDenied)`. If unavailable, the caller can decide whether to fail-closed or fail-open per their policy.

Async naturally composes: the upper-layer `Interact::interact` awaits the Criome `interact`, which awaits an RPC. Actor system handles all wait points; the engine's other interactions run concurrently.

## §8 Refactoring existing patterns to the Interact trait

The pattern is observable today; the trait formalizes it. Migration:

| Current location | Current pattern | Under Interact trait |
|---|---|---|
| `schema::node_shape::recognize` | free function `recognize(point, value)` | `impl Interact for NodeDefinitionPoint { type Other = NotaValue; type Outcome = NodeDefinitionShape; }` |
| `MacroPipeline::run` | imperative pass-walker | composes `Interact` calls per recognized node |
| daemon `serve_ordinary_stream` | match on byte 0 + body decode | `impl Interact for ShortHeader { type Other = FrameBody; type Outcome = Reply; }` |
| handover `reply_to_operation` | match on (state, op) | `impl Interact for HandoverState { type Other = UpgradeOperation; type Outcome = (NewState, UpgradeReply); }` |
| orchestrate claim resolve | match on (lane_state, claim_kind) | `impl Interact for Lane { type Other = ClaimRequest; type Outcome = ClaimOutcome; }` |
| upgrade plan_upgrade_from | algorithm walking type pairs | `impl Interact for AssembledSchema { type Other = AssembledSchema; type Outcome = UpgradePlan; }` |

Each refactor is mechanical: extract the match into an `impl Interact for X`. Existing code keeps working; new code calls `x.interact(y).await` for the canonical surface.

**Cost**: per-refactor LoC modest; pattern alignment substantial. **Benefit**: every interaction in the workspace has the SAME shape; async-state-query becomes idiomatic; typed Outcome enforces error-as-data discipline.

## §9 Incomplete-thought check — what the psyche may not have finished

Per psyche directive ending: "let me know if I seem to not have finished my thought here."

Examining the message for incomplete branches:

1. **"And we need to define that"** — the typed-error/Unavailable surface. The psyche named the need but didn't enumerate WHICH typed errors. /195 §5.1 proposes a universal `InteractOutcome` enum; confirm shape or pull-back.

2. **"This is something that would go out"** — Criome as example of outbound async query. The psyche mentioned Criome SPECIFICALLY but the framework should generalize to any outbound (sema-engine query, lane-registry query, persona-spirit observe, etc.). /195 §7 generalizes; confirm.

3. **"The whole actor system takes care of the rest"** — handwaved at the actor system as the runtime. Open question: which actor library / pattern? The workspace currently uses `kameo` (per persona-spirit src/daemon.rs) — confirm the Interact trait integrates with kameo's actor pattern rather than introducing a parallel runtime.

4. **"That's how objects interact. They interact."** — meta-statement; not actionable but signals the principle's load-bearing-ness. No incompleteness flag.

5. **"Yeah, just write what I've said and let me know if I seem to not have finished my thought here."** — explicit ask. Per above: three potential under-spec items (typed-error enumeration; outbound-target generalization; actor-runtime integration). All have leans; none block the conceptual capture.

## §10 Open psyche questions

Resulting from /195 + the incomplete-thought analysis:

1. **Universal `InteractOutcome` shape** (per /195 §5.1) — `enum InteractOutcome<S, U> { Granted(S), Unavailable(U), Unauthorized(AuthorizationReason), NotImplemented { ... }, EngineUnavailable(...) }` vs leaving the Outcome fully implementation-defined. Lean: universal cross-cutting variants + per-impl Granted/Unavailable types.

2. **Async actor runtime** — confirm `kameo` (current workspace choice) is the substrate, or introduce something else? Lean: kameo since it's already there.

3. **Engine state access** — `engine_state::ask_*` functions are sketches; the real surface needs design. Per the existing pattern (per persona-spirit daemon), the actor reference (`self.root: ActorRef<SpiritRoot>`) is held by the interaction context. Convention: pass engine ActorRef into the interaction's context, not as a global. Confirm.

4. **Outbound query generalization** — Criome / sema-engine / persona-mind / lane-registry — all are outbound async queries. Lean: each has its own `Interact` impl + each can be `await`ed from any other impl. Confirm.

5. **Trait associated types vs generic** — `trait Interact { type Other; type Outcome; }` vs `trait Interact<Other, Outcome>`. Lean: associated types — one impl per (Self, Other) pair forces explicit specialization. Generic version would allow `impl<O> Interact<O, X> for Self` which dilutes the pattern. Confirm.

## §11 What this audit changes about the schema engine + handover work

The pattern is ALREADY THERE in the schema engine + handover ceremony — the Interact trait would formalize it. Concrete migration paths:

- **schema/src/node_shape.rs** — `NodeDefinitionShape::recognize(point, value)` becomes `NodeDefinitionPoint::interact(value)` returning `Outcome<NodeDefinitionShape, RecognitionFailure>`
- **persona-spirit/src/daemon.rs reply_to_operation** — becomes `HandoverState::interact(operation)` returning `Outcome<(NewState, UpgradeReply), HandoverDivergence>`
- **orchestrate claim machinery** — becomes `Lane::interact(claim_request)` returning `Outcome<ClaimToken, ClaimDenial>`

The schema engine emission could even auto-derive `Interact` for every operation — the macro EMITS the Interact impl from the schema's header roots, sub-variants, and reply types. The schema-driven workspace becomes Interact-trait-driven downstream.

## §12 References

- `reports/designer/338-schema-engine-refreshed-vision-2026-05-25.md` §2 — enum-contact-points pattern across schema engine layers
- `reports/operator/182-second-operator-schema-node-shape-audit-2026-05-25.md` — `NodeDefinitionShape × NotaValueKind` match (§3.1 reference)
- `reports/second-designer/192-audit-operator-182-second-operator-schema-node-shape-2026-05-25.md` — match-pattern boundary discussion
- `reports/second-designer/176-upgrade-mechanism-soup-to-nuts-2026-05-25.md` §5 — ShortHeader dispatch (§3.4 reference)
- `reports/second-designer/175-upgrade-mechanism-full-design-2026-05-25.md` §7 — handover state machines (§3.5 reference)
- `reports/second-operator/186-orchestrate-upgrade-socket-implementation-2026-05-25.md` — orchestrate claim shape (§3.6 reference)
- `reports/second-designer/182-schema-crate-state-and-version-projection-derivation-2026-05-25.md` §4 — upgrade plan derivation (§3.3 reference)
- `skills/enum-contact-points.md` — Apex skill formalizing match-as-logic
- `/git/github.com/LiGoldragon/schema/src/node_shape.rs` — landed implementation of §3.1 pattern
- `/git/github.com/LiGoldragon/persona-spirit/src/daemon.rs:1420-1450` — handover dispatch (§3.5)
- Intent records 601 (enum-contact-points skill), 602 (engine ops expose tree-to-tree matching), 603 (two-phase dispatch), 631 (bracket-swap), 652 (Interact trait), 653 (match-as-logic substrate), 654 (typed Unavailable), 655 (async state query)
