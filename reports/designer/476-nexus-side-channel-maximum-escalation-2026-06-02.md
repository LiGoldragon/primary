; designer
[nexus-side-channel nexus-output non-sema-decisions typed-variant maximum-escalation real-decision-logic architectural-slot four-component-evidence]
[Focused single-decision report on Nexus typed side-channel NexusOutput — escalating designer 468 candidate 2 from Decision High to Decision Maximum based on four-component evidence (spirit + persona + orchestrate + introspect). The escalation closes designer 466.3 standout finding (Nexus has no real decision logic today — into_nexus_output projects Signal variants directly to SEMA variants with zero algorithmic choice). Provides extensive context — the problem; the architectural slot; per-component evidence; current vs proposed code; downstream effects on 466.3 candidate 5 + introspect design + spirit pilot expansion; implementation cost; edge cases. Single decision ask: ratify Spirit Decision Maximum capture of NexusOutput typed side-channel variants for non-SEMA decisions.]
2026-06-02
designer

# 476 — Nexus typed side-channel `NexusOutput` — Maximum escalation

## TL;DR

**The decision**: ratify a Spirit Decision Maximum capture of the following architectural principle:

> *"NexusOutput carries typed side-channel variants for Nexus's own emitted operations distinct from SEMA writes/reads and Signal direct returns. These variants are how Nexus expresses decisions that produce side effects in the runtime — `Stash` (preserve full result keyed by handle), `Fanout` (emit to live subscribers), `Summarize` (roll into aggregate without per-event durable write), `Drop` (filtered by policy; pure accounting), `Preempt` (revoke + reissue), `Enqueue` (queue for later), `Cascade` (propagate permission/state change). Without typed side-channel slots, side-effect logic smuggles into Nexus implementation code rather than living at the schema layer. Demonstrated across four components: spirit (Stash for slim-output handle), persona (Cascade for permission propagation), orchestrate (Preempt + Enqueue), introspect (Fanout + Summarize + Drop)."*

**Why Maximum**: this closes designer 466.3's standout finding (Nexus has no real decision logic — projection with zero algorithmic choice) AND the same shape recurs across all four pilot components AND it gates downstream work on candidate 5 + introspect minimal slice + spirit pilot expansion. Without ratification, every Nexus impl reinvents side-effect handling outside the typed contract.

## Section 1 — The problem (deep context)

### What spirit-next's Nexus looks like today

Operator 281 + designer 466.2 audit + spirit-next main `7c350679`:

```rust
// spirit-next/src/nexus.rs
impl NexusEngine for Nexus {
    fn decide(&mut self, input: nexus::Nexus<nexus::Input>)
        -> nexus::Nexus<nexus::Output>
    {
        let output = input.into_nexus_output();  // generated projection
        let origin_route = output.origin_route();
        match output.into_root() {
            NexusOutput::SemaWrite(input) => { /* delegate to SEMA */ },
            NexusOutput::SemaRead(input) => { /* delegate to SEMA */ },
            NexusOutput::Signal(output) => { /* direct return, no SEMA */ },
        }
    }
}
```

And the generated `into_nexus_output()` at `spirit-next/src/schema/lib.rs:1367-1388`:

```rust
// schema-emitted projection — zero algorithmic choice:
fn into_nexus_output(self) -> nexus::Nexus<NexusOutput> {
    match self.into_root() {
        NexusInput::Signal(Input::Record(entry)) =>
            NexusOutput::SemaWrite(SemaWriteInput::Record(entry))
                .with_origin_route(self.origin_route()),
        NexusInput::Signal(Input::Observe(query)) =>
            NexusOutput::SemaRead(SemaReadInput::Observe(query))
                .with_origin_route(self.origin_route()),
        NexusInput::Signal(Input::Remove(identifier)) =>
            NexusOutput::SemaWrite(SemaWriteInput::Remove(identifier))
                .with_origin_route(self.origin_route()),
        other => other.project_signal_output(),
    }
}
```

### Why this isn't a real Nexus

Per designer 466.3 §2 — the projection has **zero algorithmic choice**. Each Signal Input variant maps to exactly one downstream operation. There's no:
- Filtering ("this request matches no policy; drop").
- Caching ("recent identical query; return stashed result without SEMA touch").
- Fanout ("notify live subscribers in addition to durable write").
- Routing-by-complexity ("fast path for simple queries; slow path with summarization for complex").
- Conflict-resolution ("two requests racing for same resource; one wins").
- Preemption ("higher-priority arrived; revoke and reissue").

The architecture provides a Nexus SLOT — `NexusEngine::execute` with `&mut self` exclusive borrow — but the slot has no substance to put in it today. Per Spirit 1387 (schema drives most behavior; Rust impl terse), the Rust code is too terse here — there's no decision to make.

Per Spirit 1411 (beauty must prevail), this is a beauty problem: the architectural shape (Nexus as decision center between Signal outer and SEMA inner worlds per Spirit 1388) doesn't manifest in code that has any decision logic.

### Why the existing variants aren't enough

NexusOutput has 3 variants today: `SemaWrite`, `SemaRead`, `Signal`. Every Nexus decision must reduce to one of these. But many natural Nexus decisions don't fit:
- "Drop this request per policy" — fits `Signal` direct return with an error variant, but conflates filtering with errors.
- "Stash this result and return a handle" — no slot; current shape forces inline return of full payload.
- "Emit to live subscribers AND write to SEMA" — no slot for the dual emission.
- "Roll this event into a summary, no per-event durable record" — no slot; would force SemaWrite of the summary.

The pattern: anything that's a Nexus-side runtime effect (not a delegation to SEMA, not a direct Signal return) currently has to be implemented as ad-hoc Rust code in the Nexus impl, OUTSIDE the typed contract. That's the architecture leakage Spirit 1387 warns against.

## Section 2 — The architectural slot

The proposed shape adds typed side-channel variants for Nexus's own emitted operations:

```rust
pub enum NexusOutput {
    SemaWrite(SemaWriteInput),   // delegate write to SEMA (existing)
    SemaRead(SemaReadInput),     // delegate read to SEMA (existing)
    Signal(Output),              // direct return to Signal without SEMA touch (existing)

    // Side-channel variants — Nexus's own emitted operations:
    Stash(StashSpec),            // preserve full result keyed by handle; return slim ack
    Fanout(FanoutSpec),          // emit to live subscribers
    Summarize(SummarizeSpec),    // roll into aggregate without per-event durable write
    Drop(DropReason),            // filtered by policy; pure accounting
    Preempt(PreemptSpec),        // revoke + reissue
    Enqueue(EnqueueSpec),        // queue for later
    Cascade(CascadeSpec),        // propagate permission/state change
}
```

Each side-channel variant carries typed payload:
```rust
pub struct StashSpec {
    pub handle: ResultHandle,
    pub full_result: NexusOutput::FullResultVariant,  // recursive — handle into a stash
    pub durability: StashDurability,  // ephemeral / persistent
}

pub struct FanoutSpec {
    pub subscribers: Vec<SubscriberHandle>,
    pub frame: NexusFanoutFrame,
    pub also_durable: Option<SemaWriteInput>,  // optional SEMA write companion
}

pub struct DropReason {
    pub policy_rule: PolicyRuleIdentifier,
    pub origin_route: OriginRoute,
}
```

The key point: each variant is TYPED — schema-emitted — not a Rust hand-written struct ad-hoc. The macro emits them; components compose their domain-specific extensions.

## Section 3 — Four-component evidence

The strength of the Maximum escalation comes from independent designs landing on the same architectural slot.

### Spirit (designer 466.3 candidate 5 + 470 item 4)

Spirit's slim-Nexus-output design (per Spirit 1389) needs `Stash`: client sends `Observe`; Nexus stashes the full `Vec<Entry>` keyed by handle; client follows up with `Lookup(handle)`. Without `Stash`, the slim-output design has nowhere to land — full payload leaks to wire.

```rust
fn decide_observe(&mut self, query: Query, route: OriginRoute)
    -> nexus::Nexus<NexusOutput>
{
    let entries = SemaEngine::observe(&self.store, SemaReadInput::Observe(query));
    if entries.len() > SLIM_THRESHOLD {
        let handle = self.mail_ledger.stash(entries);
        NexusOutput::Stash(StashSpec {
            handle,
            durability: StashDurability::Ephemeral,
            full_result: NexusOutput::Signal(Output::RecordsObserved(SlimAck {
                result_handle: handle,
                count: entries.len(),
                database_marker: self.database_marker(),
            })),
        }).with_origin_route(route)
    } else {
        NexusOutput::Signal(Output::RecordsObserved(...)).with_origin_route(route)
    }
}
```

### Persona (designer 468 §2)

Persona's permission-cascade decision: grant capability X to persona P → cascade implies permission revocation on derived capabilities for P's children; ALSO notify P's sessions of the change.

```rust
fn decide_grant_capability(&mut self, grant: CapabilityGrant, route: OriginRoute)
    -> nexus::Nexus<NexusOutput>
{
    let durable_write = SemaWriteInput::PersistCapability(grant);
    let cascade_targets = self.compute_cascade_targets(&grant);
    NexusOutput::Cascade(CascadeSpec {
        durable_write,
        cascade_targets,
        notify_sessions: vec![grant.persona_session_handle()],
    }).with_origin_route(route)
}
```

Without `Cascade`, the impl smuggles the cascade logic into Nexus Rust code outside the typed contract.

### Orchestrate (designer 468 §3)

Orchestrate's claim-conflict decision: `Claim` on a locked lane → four branches (grant, queue, preempt, error).

```rust
fn decide_claim(&mut self, claim: ClaimRequest, route: OriginRoute)
    -> nexus::Nexus<NexusOutput>
{
    let current_holder = SemaEngine::observe(&self.store, SemaReadInput::LookupLaneHolder(claim.lane));
    match self.resolve_conflict(claim, current_holder) {
        ConflictResolution::Grant => NexusOutput::SemaWrite(SemaWriteInput::Grant(claim)),
        ConflictResolution::Queue(position) =>
            NexusOutput::Enqueue(EnqueueSpec { wait_queue: claim.lane, position, claim }),
        ConflictResolution::Preempt(victim) =>
            NexusOutput::Preempt(PreemptSpec { revoke: victim, grant: claim }),
        ConflictResolution::Reject(reason) =>
            NexusOutput::Signal(Output::ClaimRejected(reason)),
    }.with_origin_route(route)
}
```

Two NEW side-channel variants: `Preempt` and `Enqueue`. Without them, orchestrate's Nexus is forced to express conflict resolution through ad-hoc Rust + SemaWrite combinations that don't carry the semantic meaning.

### Introspect (designer 469 §"IngestTraceEvent decision")

Introspect's `IngestTraceEvent` decision — the densest Nexus decision in the workspace design corpus per designer 470:

```rust
fn decide_ingest_trace_event(&mut self, frame: TraceFrame, route: OriginRoute)
    -> nexus::Nexus<NexusOutput>
{
    let policy = SemaEngine::observe(&self.store, SemaReadInput::PolicyForComponent(frame.component_identifier));
    match policy {
        Policy::Keep => NexusOutput::SemaWrite(SemaWriteInput::RecordTraceEvent(TraceRecord::from(frame))),
        Policy::Drop(reason) => NexusOutput::Drop(DropReason {
            policy_rule: reason,
            origin_route: frame.route,
        }),
        Policy::Summarize(spec) => NexusOutput::Summarize(SummarizeSpec {
            target: spec.aggregate_target,
            frame_delta: spec.fold(frame),
        }),
        Policy::Fanout(subscribers) => NexusOutput::Fanout(FanoutSpec {
            subscribers,
            frame: frame.into_nexus_fanout_frame(),
            also_durable: Some(SemaWriteInput::RecordTraceEvent(TraceRecord::from(frame))),
        }),
    }.with_origin_route(route)
}
```

THREE new side-channel variants in ONE decision: `Drop`, `Summarize`, `Fanout`. Plus the existing `SemaWrite` for the Keep policy.

### The pattern across all four

| Component | Side-channels needed | Why |
|---|---|---|
| spirit | Stash | Slim Nexus output per Spirit 1389; clients query for specifics |
| persona | Cascade | Capability grants propagate to derived permissions + sessions |
| orchestrate | Preempt, Enqueue | Conflict resolution + wait queue management |
| introspect | Fanout, Summarize, Drop | Trace policy decisions per ingest |

**Seven distinct side-channel variants across four components**. The pattern is universal — every component with substantive Nexus logic needs some side-channel slot. Without typed slots, each component reinvents the side-effect handling outside the contract.

## Section 4 — Downstream effects

### Designer 466.3 candidate 5 (Output split for slim Nexus + QueryByHandle) lands cleanly

The Output split into slim ack variants + Nexus-level `QueryByHandle` follow-up Signal call REQUIRES `Stash` as the Nexus side-channel that preserves full results in the mail ledger keyed by handle. Without `Stash`, candidate 5 has nowhere to land.

Per Spirit 1422 (contract-repo split): the slim `Output` variants live in `signal-spirit` (client-facing). The `Stash` side-channel + the mail ledger storage live in `spirit-next` (daemon-internal). Clean separation.

### Introspect minimal slice (designer 469 + top-6 item 3) gets its decisions

Introspect's `IngestTraceEvent` decision is unrepresentable in the current 3-variant `NexusOutput`. Without ratification, introspect's Nexus has to inline the side-effect logic as Rust ad-hoc — which fails the schema-drives-most-behavior principle per Spirit 1387.

Phase 1 of introspect (just `IngestTraceEvent` + `QueryTraceEvents`) NEEDS at minimum `Drop` and possibly `Fanout` to express Phase 2's policy decisions cleanly.

### Spirit pilot expansion (designer 468 + top-6 item 2) gets first-class slim acknowledgement

Once spirit's 8-variant Input lands (Record + Observe + Lookup + Count + Summarize + Update + Remove + Subscribe), the Nexus decisions on Observe and Summarize benefit from `Stash` for handle-based result fetching. The current per-variant decide_* shape becomes substantive.

### Designer 468 candidate 4 metric becomes verifiable

"Nexus output variant count exceeds SEMA write variant count when Nexus has substantive decisions" — once the side-channel variants land, this metric is concrete. Spirit's NexusOutput becomes 4-5 variants (existing 3 + Stash + maybe Drop); orchestrate's becomes 5 (3 + Preempt + Enqueue); introspect's becomes 6 (3 + Fanout + Summarize + Drop). All four exceed their respective SemaWriteInput counts — Nexus earns its keep.

### Designer 466.3 candidate 4 (Engine actor promotion) connection

The actor-trait pilot per Spirit 1365 if-possible hedge can carry side-channel handling in the actor trait's lifecycle hooks. A `NexusActor::handle_side_channel(NexusOutput) -> Result<(), Error>` method dispatches side-channel variants to their respective handlers. This makes the engine actor-trait promotion + the side-channel pattern compose cleanly.

## Section 5 — Implementation cost

### Schema changes

Add typed side-channel variants to the `NexusOutput` enum declaration in each component's schema source. Per Spirit 1422 (contract-repo split), `NexusOutput` lives in the daemon repo (daemon-internal); each component declares its own side-channel variants.

Common variants (`Stash`, `Drop`) might land in a shared schema-next vocabulary for reuse; component-specific variants (`Cascade`, `Preempt`, `Enqueue`, `Fanout`, `Summarize`) stay per-component.

### Code changes per component

For each component pilot, the NexusEngine impl gains the side-channel dispatch:

```rust
impl NexusEngine for Nexus {
    fn decide(&mut self, input: nexus::Nexus<nexus::Input>)
        -> nexus::Nexus<nexus::Output>
    {
        // ... per-variant decide_* dispatch ...
    }

    fn handle_side_channel(&mut self, output: NexusOutput) -> nexus::Nexus<NexusOutput> {
        match output {
            NexusOutput::Stash(spec) => self.execute_stash(spec),
            NexusOutput::Fanout(spec) => self.execute_fanout(spec),
            NexusOutput::Drop(reason) => self.account_drop(reason),
            // ... etc
            other => other,
        }
    }
}
```

Each side-channel handler is a small focused Rust algorithm (~20-50 lines).

### Phase 1 cost

For spirit-next pilot (just `Stash` + `Drop`): 1-2 operator days. Schema source addition + impl methods + tests asserting the slim-acknowledgement round-trip.

For introspect minimal (top-6 item 3): the `Drop` + `Fanout` variants land WITH introspect's first slice — they're prerequisites, not separate work. Bundled in introspect's minimal scope.

For orchestrate + persona: future, lands with their respective component pilots.

### Schema-rust-next emitter

No changes required. The emitter already supports arbitrary enum variants per the engine-trait emission pattern. Components add their side-channel variants to their schema source; the emitter generates the Rust types automatically.

## Section 6 — Edge cases and open questions

### Composition — side-channels that wrap SEMA operations

Some side-channels include a durable SEMA write companion: `Fanout` may write to SEMA AND emit to subscribers; `Stash` may persist (durable) or not (ephemeral). The typed payload carries the composition explicitly:

```rust
pub struct FanoutSpec {
    pub subscribers: Vec<SubscriberHandle>,
    pub frame: NexusFanoutFrame,
    pub also_durable: Option<SemaWriteInput>,  // ← optional companion
}
```

This is cleaner than expressing fanout-plus-write as two separate NexusOutput values — the typed payload captures the atomic operation.

### Naming — `Stash` vs `Memoize` vs `Cache`

Three plausible names for the preserve-and-handle pattern. `Stash` is the workspace-canonical term from designer 466.3 candidate 5 + designer 468; consistent with the mail-ledger metaphor (stash is where Nexus puts the full result; handle is the receipt). Keep `Stash`.

### Universal vs per-component variants

`Stash` and `Drop` seem workspace-universal — every component might want them eventually. `Cascade`, `Preempt`, `Enqueue`, `Fanout`, `Summarize` are component-specific. Two options:
- (a) **Universal vocabulary**: schema-next emits a shared `BaseNexusOutput` enum with `Stash` + `Drop`; each component's NexusOutput extends it.
- (b) **Per-component declaration**: each component declares its full NexusOutput; common variants get duplicated across components.

Designer recommendation: **(b) per-component**. Schema-next doesn't currently support enum extension; per-component is simpler. If naming converges (every component picks `Stash` for stash-and-handle), workspace-wide convention emerges without forced sharing.

### Recursion — `StashSpec` references `NexusOutput`

The `Stash` variant carries the full underlying result that gets stashed. The full result is itself a `NexusOutput` value (typically `NexusOutput::Signal(full_payload_output)`). This is recursive — `StashSpec` references `NexusOutput`.

Schema-next emitter should already handle recursive enums per Spirit 1358 (recursive variants Box-wrapped). Verify the recursion bottoms cleanly.

## Section 7 — Decision ask

**Single ratification**: Spirit Decision Maximum capture of NexusOutput typed side-channel variants for non-SEMA decisions, with the following body:

> *"NexusOutput carries typed side-channel variants for Nexus's own emitted operations distinct from SEMA writes/reads and Signal direct returns. These variants are how Nexus expresses decisions that produce side effects in the runtime — Stash, Fanout, Summarize, Drop, Preempt, Enqueue, Cascade. Without typed side-channel slots, side-effect logic smuggles into Nexus implementation code rather than living at the schema layer. Demonstrated across four components: spirit (Stash for slim-output handle), persona (Cascade for permission propagation), orchestrate (Preempt + Enqueue for conflict resolution), introspect (Fanout + Summarize + Drop for trace policy). Magnitude Maximum based on universality (every component needs side-channels) + 466.3 standout-finding closure + downstream gate (candidate 5 + introspect minimal slice + spirit pilot expansion all depend)."*

### What ratification unblocks

1. **Designer 466.3 candidate 5** (Output split for slim Nexus + QueryByHandle) — implementation has its substrate.
2. **Introspect minimal slice** (top-6 item 3) — IngestTraceEvent decision is expressible in the typed contract.
3. **Spirit pilot expansion** (top-6 item 2) — per-variant decide_* methods land with substantive slim-acknowledgement support.
4. **Designer 468 candidate 4 metric** (Nexus variant count > SEMA write variant count) — verifiable on each component.

### What ratification commits to

1. Side-channel variants in schema sources are part of the component's typed interface — schema-emitted, not hand-written ad-hoc.
2. Each component's NexusEngine impl handles its declared side-channels in `handle_side_channel` or equivalent dispatch.
3. The mail ledger / stash store / fanout transport are daemon-internal but their wire types (`StashSpec`, `FanoutSpec`, etc.) are schema-declared.
4. Workspace convention: when Nexus has substantive logic, declare the side-channel variants explicitly; when it's pure delegation, the 3-variant base is sufficient.

## Cross-references

- `reports/designer/466-triad-engine-honesty-situation-2026-06-01/3-overview.md` — the standout finding this escalation closes.
- `reports/designer/468-developed-interfaces-spirit-persona-orchestrate-2026-06-02.md` — original candidate 2 capture + persona/orchestrate evidence.
- `reports/designer/469-introspect-component-design-2026-06-02.md` — introspect's IngestTraceEvent decision evidence.
- `reports/designer/470-psyche-backlog-top-6-visual-2026-06-02.md` — item 4 backlog entry this report deepens.
- `reports/designer/475-contract-repo-pipeline-situation-and-proposal-2026-06-02/2-overview.md` — contract-repo split places NexusOutput in daemon (daemon-internal).
- `reports/operator/281-generated-interface-logic-with-macros-2026-06-02.md` — current Nexus impl shape.
- Spirit records 1326-1336 (engine-trait architecture), 1361 (method count matches wire events), 1365 (trace-as-trait + actor traits), 1387 (schema drives behavior; Rust impl terse), 1388 (Nexus inner/outer world), 1389 (Nexus output slim; clients query for specifics), 1411 (beauty), 1419 (operator's programmatic triad), 1422 (contract-repo split), 1427 (spirit triad naming meta-signal-spirit), 1428 (fleet-wide rename to meta-signal).
- `skills/component-triad.md` §"Runtime triad engine traits" — the architecture this extends.
- `skills/architectural-truth-tests.md` §"Proof-of-usage ladder" — Layer 2 witnesses on side-channel handler dispatch.

## For the orchestrator (chat ask)

The pending decision: ratify Spirit Decision Maximum capture of NexusOutput typed side-channel variants. Evidence across 4 components; closes 466.3 standout finding; gates 466.3 candidate 5 + introspect minimal + spirit expansion. Single yes/no.
