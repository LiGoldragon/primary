# Context Maintenance and Intent Supersession

*Kind: operator context-maintenance audit · Topics: trace, client genericization, schema interface, help, context maintenance, Spirit supersession · 2026-06-03*

## Scope

This report audits the old trace/client/help report and Spirit surface against the fresh 2026-06-03 intent records:

- Spirit 1490: trace remains typed until client display.
- Spirit 1491: no trace-on-trace enablement for now.
- Spirit 1492: trace is a schema-defined interface with closed generated enums.
- Spirit 1493: help/documentation is schema data in a mirror description namespace.
- Spirit 1494: authored data files should prefer typed NOTA roots from path/file convention.
- Spirit 1495: daemons avoid NOTA decoding and string surfaces; clients translate/render.
- Spirit 1496: context maintenance may recommend supersession/removal, but Spirit deletion remains reviewable and justified.

No Spirit records were removed. No code files were touched.

## Current spine

The current trace/client/help spine is:

1. Trace names and events are typed generated interface data until the client display boundary. The CLI or user-interface surface may render strings; the daemon and runtime witness path should not treat strings as the trace substrate. Spirit 1490 and 1492 are the strongest current authority.
2. Client trace handling should become generated or generic from schema interface definitions. The CLI should remain a thin client that enables and displays a generic trace surface, not a component-specific trace interpreter. Spirit 1489 and 1495 carry this.
3. Trace should not trace its own trace interface for now. Any future trace-on-trace design needs explicit enablement and filtering so the trace system does not recursively observe itself. Spirit 1491 carries this.
4. Help is no longer best framed as an injected root action alone. Spirit 1396 remains useful as the older generated-help action record, but Spirit 1493 reframes the stronger target: a schema description namespace mirroring the global symbol namespace, with generated defaults for missing descriptions.
5. Reusable trace transport is no longer a per-component `spirit-next` concern. Operator 291 verifies that `triad-runtime` owns reusable trace log, frame, socket, and listener mechanics; `spirit-next` only supplies component-specific archiving and hook overrides.

## Stale report claims

The following report claims are stale or partially stale.

- `reports/designer/470-psyche-backlog-top-6-visual-2026-06-02.md`: item 1's `TraceObjectName(String)` and "newtype vs closed enum" framing is superseded by Spirit 1492. The current target is not a string/newtype trace object; it is a schema-defined trace interface with closed generated enums. Keep the report only as a historical backlog surface until its other open items are migrated.

- `reports/operator/282-trace-header-generated-interface-situation-2026-06-02.md`: still useful for the typed-header mental model, but its proposed split into `TraceInterfaceObject`, `TraceActorObject`, and `TraceObject` is now too local. Spirit 1492 makes trace its own schema-defined interface, not just a header/object helper family adjacent to other generated interfaces. Forward only the typed-header and compact-vs-extended reasoning.

- `reports/operator/283-schema-trace-triad-context-maintenance-2026-06-02.md`: superseded as the current maintenance view. Its guidance against string/newtype trace identity remains correct, but its open questions about whether actor-boundary and interface-object trace both fire should be rephrased under a schema-defined trace interface and no trace-on-trace default.

- `reports/operator/284-fresh-intent-trace-triad-primary-assessment-2026-06-02.md`: stale as "primary assessment." It correctly listed generated Help, interface descriptions, and report retirement as open work, but the fresh 1490-1496 records refine all three. Use this report's current spine instead.

- `reports/designer/483-Audit-tracing-emission-completeness-2026-06-02.md`: stale where it says `TraceLog`, trace socket transport, and listener support are hand-written per-component in `spirit-next`. Operator 291 verifies those reusable mechanics now live in `triad-runtime`. It remains useful for the still-open per-variant route wiring and per-effect trace gaps.

- `reports/designer/484-Audit-production-readiness-meta-2026-06-02/4-shared-runtime.md` and `6-overview.md`: the standalone `triad-runtime` recommendation is now partly landed for trace Wave 1. Keep as architectural sequence evidence, but update future paraphrases from "extract trace surface" to "continue after trace Wave 1 extraction."

- `reports/designer/469-introspect-component-design-2026-06-02.md`: partially stale because it frames introspect ingestion as name-only trace with small typed accompaniments. Spirit 1490 and 1492 now require typed trace interface data until display; `ActivationName String` should become closed generated trace/event vocabulary in any future `signal-introspect` sketch.

- `reports/designer/470-psyche-backlog-top-6-visual-2026-06-02.md` item 5 and Spirit 1396-derived help framing: partially superseded by Spirit 1493. Help still belongs in schema-generated self-description, but the stronger target is a mirror description namespace over symbols, not only recursive `Help` variants.

## Spirit supersession recommendations

These are recommendations only. Record 1496 authorizes audit and recommendation, not unilateral deletion.

### Removal candidates only with psyche authorization

- Spirit 1347 says the CLI is the log surface and "no separate logging daemon or external log sink." This conflicts with the later introspect direction in Spirit 1398 and the production path in designer 469/484 where introspect is the trace destination and queryable intelligence component. Recommendation: ask the psyche whether 1347 should be superseded or narrowed to "CLI is the display/debug surface for local testing; introspect may be the cross-component trace sink." Do not remove without tombstone and explicit authorization.

- Spirit 1400 remains broadly aligned on generated trace names, but its "COMPACT root variant name only" and "EXTENDED nested variant chain" framing should be treated as a header-encoding refinement under Spirit 1492, not the whole trace design. Recommendation: keep, or lower/narrow if Spirit supports typed supersession later.

### Keep but mark as refined by newer intent

- Spirit 1343, 1346, 1349, and 1350 still apply as runtime-witness intent: trace proves real Signal/Nexus/SEMA use. Refine their "logging socket" and "engine logs" wording under 1490/1492: the thing emitted is typed trace interface data, not a string log.

- Spirit 1344 and 1348 still apply at the client/test-launcher configuration layer, but 1495 narrows the daemon side. Typed NOTA configuration belongs at authored/client/configuration surfaces that translate into binary protocol/config data; daemons should not decode NOTA just to configure trace.

- Spirit 1394 still applies as the correction away from rich payload snapshots, but its phrase "record only the name" should now be read as "record the typed generated trace identity/event object," with string names rendered only by clients.

- Spirit 1396 still applies as an older generated-help direction, but 1493 refines it. Future Help implementation should derive from schema description data in the mirror namespace; generated `Help` actions can be a projection from that data, not the source.

- Spirit 1405 and 1408 still apply to trace header identity. They should be kept as compact/extended encoding guidance beneath the new schema-defined trace interface.

## Actionable next steps

1. Update the active operator brief for client trace genericization to start from Spirit 1489-1492 and operator 291. The first target is a generic client display path over typed trace events, not another `spirit-next`-specific string renderer.

2. When touching `schema-rust-next` or `spirit-next` repo context files, manifest the fresh intent: trace as schema-defined closed enum interface; client-only string rendering; daemon binary/no-NOTA boundary; no trace-on-trace for now.

3. Reframe Help work before implementation. The first durable design surface should describe the mirror description namespace and default generation rule from Spirit 1493; only then decide how generated `Help` variants project from that data.

4. Keep designer 483 for the still-open per-variant and per-effect trace gaps, but stop using it as evidence that trace transport belongs in `spirit-next`. Operator 291 is the current transport boundary.

5. Do not delete Spirit records in this pass. If the main agent wants cleanup, prepare a separate tombstone report for any proposed removals and ask the psyche specifically about records 1347 and any duplicate/obsolete trace-log records.

## Bottom line

The stale surface is not "trace exists"; trace remains strongly intended. The stale surface is "trace as log/string/client-specific helper." The live shape is trace as a schema-defined typed interface with closed generated vocabularies, carried as typed data until the client renders it, with reusable runtime mechanics in `triad-runtime` and no trace-on-trace enabled yet.
