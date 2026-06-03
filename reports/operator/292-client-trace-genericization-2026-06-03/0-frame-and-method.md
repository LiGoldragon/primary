# Frame And Method

*Kind: operator meta-report frame · Topics: client tracing, trace interface, schema-rust-next, spirit-next, triad-runtime, context maintenance · 2026-06-03 · operator lane*

## Scope

Psyche clarified the client side of tracing after reading operator report 291:
trace is typed interface data until the client display boundary, the CLI should
stay thin, client trace handling should be generated or generic from schema
interfaces, and help/documentation should become typed schema data in a mirror
description namespace.

Captured Spirit records driving this pass:

- 1489: client-side tracing should be generated or generic from schema
  interface definitions; CLI stays thin.
- 1490: tracing remains typed data until the client display boundary.
- 1491: tracing is not enabled on the tracing interface itself for now.
- 1492: tracing is its own schema-defined interface with closed generated enum
  vocabularies.
- 1493: help/documentation is schema data in a mirror description namespace
  over the global symbol namespace.
- 1494: authored workspace data files should prefer typed NOTA roots from
  predictable path/file conventions.
- 1495: daemons stay free of NOTA decoding and string surfaces; clients
  translate NOTA text into binary protocol data and render typed replies or
  traces.
- 1496: context-maintenance agents may recommend supersession/removal, but
  Spirit deletion stays reviewable and justified.

## Method

Two background subagents ran in parallel:

- `1-context-maintenance-and-intent-supersession.md` audited old reports and
  Spirit records for stale trace/client/help framing.
- `2-generated-client-trace-shape-audit.md` audited current code and described
  the generated/generic target shape.

The main operator implemented the smallest compatible production slice while
subagents ran:

- `triad-runtime` gained a generic `TraceClient<Event>` display-edge surface.
- `spirit-next` CLI stopped owning a local trace-output helper and now uses the
  generic typed trace client.
- `schema-rust-next`, `triad-runtime`, and `spirit-next` intent/architecture
  files were updated to reflect the new boundary.

Designer report 487 was read as it appeared. Its frame aligns with the same
Spirit 1489-1496 thread and starts the designer-side trace/help/config/context
meta-report; this operator pass does not edit designer-owned files.

## Output Files

- `0-frame-and-method.md` — this frame.
- `1-context-maintenance-and-intent-supersession.md` — background audit of old
  trace/client/help context and Spirit supersession candidates.
- `2-generated-client-trace-shape-audit.md` — background code-shape audit and
  target generated-client design.
- `3-overview.md` — operator synthesis and implementation closeout.
