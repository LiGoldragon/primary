# Actionable Patterns From Designer 463

*Kind: pattern extraction · Topics: testing-trace, schema-rust-next, spirit-next, component-triad, architectural-witness · 2026-06-01 · operator lane*

## Source

Extracted from `reports/designer/463-operator-trace-implementation-audit-and-intent-gaps-2026-06-01.md`.

This report keeps only the actionable patterns. It drops audit narration,
historical framing, and report-to-report comparison except where needed to
drive a next implementation step.

## Pattern 1: Trace Is Trait-First, Event-Second

Actionable rule: do not treat `TraceEvent` as the architecture. The event is
only the serializable payload. The architecture is a generated trait surface
on schema-derived interfaces and on the Signal/Nexus/SEMA actor traits where
that stays clean.

Implementation consequence:

- `schema-rust-next` emits `SignalTrace`, `NexusTrace`, and `SemaTrace` beside
  the generated engine traits.
- The generated actor traits, if the pilot proves the shape, expose the trace
  surface as part of the actor contract.
- `spirit-next` deletes local trace method vocabulary and consumes the
  generated traits.
- Tests include a type witness that Signal, Nexus, and SEMA actors use the
  generated trace traits.

Where this belongs later:

- `repos/schema-rust-next/ARCHITECTURE.md` under generated support surfaces.
- `repos/spirit-next/ARCHITECTURE.md` under runtime triad actor contracts.

## Pattern 2: Compile-Time Existence And Runtime Configuration Are Separate

Actionable rule: cargo features answer "does this code exist in this binary?"
Typed NOTA/binary configuration answers "does this instance use the code, and
how?"

Implementation consequence:

- `testing-trace` remains a compile-time feature gate.
- A typed `TraceConfiguration` field controls runtime trace socket behavior
  when that feature exists.
- A production binary compiled without the feature cannot be configured into
  tracing by any runtime argument.
- A testing binary compiled with the feature can still run with trace disabled.

Where this belongs later:

- `skills/component-triad.md` near the single-argument rule.
- `repos/spirit-next/ARCHITECTURE.md` under daemon configuration.

Open action:

- This should be captured as durable intent before implementing typed NOTA
  build/test configuration. Designer 463 called it intent gap A.

## Pattern 3: Trace Follows The Component Triad

Actionable rule: trace has the same three-way placement as other component
interfaces.

Implementation consequence:

- Trace nouns and interface traits belong in the signal contract layer.
- Trace transport belongs in the daemon implementation layer.
- Trace policy belongs in the owner-signal layer.

That prevents a local `spirit-next` trace module from becoming an unowned
fourth vocabulary. It also keeps transport and policy from leaking into the
ordinary working signal.

Where this belongs later:

- `skills/component-triad.md` as the generic instrumentation placement rule.
- The relevant signal/owner-signal/spirit-next repo `ARCHITECTURE.md` files
  once the trace crates settle.

Open action:

- Capture as durable intent before splitting trace across signal and
  owner-signal crates. Designer 463 called it intent gap B.

## Pattern 4: Runtime Witnesses Replace Positive Grep

Actionable rule: source grep can prove only source spelling or forbidden
absence. It cannot prove live architecture use.

Implementation consequence:

- Keep negative guards such as "daemon has no `nota-next` normal dependency."
- Keep explicit artifact freshness/source spelling checks only if named as
  such.
- Replace positive "this API exists in this file" checks with compile,
  process, or runtime witnesses.
- For trace, the preferred witness is a real binary request that returns a
  normal reply and emits ordered trace frames showing Signal, Nexus, and SEMA
  all ran.

Where this belongs later:

- Already mostly lives in `skills/architectural-truth-tests.md` and
  `skills/testing.md`.
- Repo flake checks should be renamed to match what they actually prove.

Open action:

- Sweep `schema-rust-next` and `schema-next` flake checks for remaining
  positive-grep behavior proxies.

## Pattern 5: Slice Order Follows Dependency, Not Convenience

Actionable rule: do not build outer transport on the wrong inner surface.

Recommended order:

1. `schema-rust-next` emits trace traits and trace payload nouns.
2. `spirit-next` consumes the generated traits and removes local trace
   vocabulary.
3. `spirit-next` adds the CLI-facing binary trace socket.
4. Typed runtime trace configuration lands.
5. Production-copy handover tests assert both normal binary reply and trace
   sequence.

This updates the older "socket first" idea. Spirit 1365 made trait-first the
load-bearing next step.

Where this belongs later:

- `reports/operator/278-gap-vision-and-subagent-implementation-brief-2026-06-01.md`
  already carries the worker brief.
- Repo `ARCHITECTURE.md` files should only absorb this once implementation
  lands, not while it is still planned sequence.

## Pattern 6: Testing Trace Is Full-Payload; Production Debug Would Be Slim

Actionable rule: testing trace may carry full schema payloads inline because
the point is self-contained assertion. A future production-debug trace mode
should probably follow the Signal acknowledgement pattern: small records with
identifiers into durable detail.

Implementation consequence:

- Keep full payloads in current `testing-trace` events.
- Do not generalize that shape into a permanent production observability
  protocol without re-evaluating size and durability.

Where this belongs later:

- `repos/spirit-next/ARCHITECTURE.md` only if production-debug tracing becomes
  a real target.

## Pattern 7: Subagent Readiness Has A Gate

Actionable rule: a subagent is ready when the trait surface, ownership layer,
and witness shape are all known. Otherwise the subagent will implement
plausible clutter.

Current readiness:

- Ready: schema-rust trace trait emission plus spirit-next consumption.
- Ready: positive-grep cleanup using the proof-of-use ladder.
- Not ready until intent gap A is captured: typed NOTA build/test
  configuration.
- Later: production-copy handover with trace, after socket trace exists.

Implementation consequence:

- The next worker brief should be based on report 278 plus this extraction.
- Do not dispatch a worker solely to add more local `spirit-next` trace code.

## Immediate Operator Actions

1. Update the worker brief from report 278 with this extraction if it drifts.
   It is currently aligned with Pattern 1 and Pattern 5.
2. Capture or ask the psyche to confirm Pattern 2 before typed trace
   configuration work starts.
3. Capture or ask the psyche to confirm Pattern 3 before splitting trace nouns
   and trace policy across triad crates.
4. When implementation resumes, begin with schema-rust trace trait emission
   and spirit-next consumption, not log-socket transport.
5. Run the positive-grep cleanup in parallel only if it stays mechanically
   scoped to witness replacement and check renaming.

## Subagent Brief Delta

Any subagent sent after this extraction must be told:

- Trace is trait-first. `TraceEvent` is the payload, not the contract.
- Actor traits are part of the pilot. Try the cleanest generated
  `SignalActor`, `NexusActor`, and `SemaActor` shape, but report ergonomics if
  the super-trait form fights the existing code.
- Do not add compatibility aliases for local trace methods.
- Do not build a socket transport before replacing local trace vocabulary with
  generated traits.
- Runtime witnesses are mandatory; positive grep is not an acceptance test for
  live behavior.
