# spirit-next Findings

## Current Repo State

Checked revision:

- commit `f8ab84871de7` on `main`
- change `nmmlmmnnzkzr`
- description: `spirit-next: use per-plane trace object names`

The working copy was clean.

## Guidance Files

Read:

- `AGENTS.md`: thin shim to workspace `AGENTS.md`.
- `INTENT.md`: present and current.
- `ARCHITECTURE.md`: present and current.

Missing:

- `skills.md`: absent. This is not a blocker for this pass, but a future repo
  skills file could usefully summarize the local build/test commands and the
  generated-source regeneration loop.

## Manifestation Verdict

No repo edit is needed right now.

`INTENT.md` already manifests the fresh intent from records 1339-1450:

- daemon/CLI separation is binary for process communication and NOTA only for
  the text-facing CLI surface;
- daemon configuration is a binary rkyv `Configuration` file, not a NOTA
  startup argument;
- `nota-next` is absent from binary-only daemon builds and present only for
  the `nota-text` surface;
- old convenience APIs do not remain beside the schema-derived trait path;
- schema declares Signal, Nexus, and split SEMA roots;
- `SignalActor`, `Nexus`, and `Store` implement generated engine traits;
- trace events come from generated trait hooks, not local side traits or grep;
- trace uses generated typed `ObjectName`, not strings;
- `testing-trace` installs a shared recording trace log by default while normal
  packages stay lean.

`ARCHITECTURE.md` already states the live runtime shape:

- generated `src/schema/lib.rs` is checked in and freshness-checked;
- `testing-trace` is a separate explicit package/check surface;
- trace frames cross a real daemon boundary over a Unix trace socket;
- `SignalActor`, `Nexus`, and `Store` override generated trace hooks;
- `TraceLog` decides memory, socket, or disabled recording destination;
- local stack testing names normal and trace packages/checks;
- runtime-chain tests assert schema-emitted objects rather than test-local
  shadow languages.

## Code Evidence

Search evidence confirmed the docs match the implementation:

- `src/schema/lib.rs` contains the generated per-plane object-name enums,
  shared `ObjectName`, `TraceEvent`, and generated trace hook methods.
- `src/engine.rs`, `src/nexus.rs`, and `src/store.rs` override the generated
  hooks and wrap plane-local names into `ObjectName`.
- `src/trace.rs` records and transports rkyv `TraceEvent` frames.
- `src/config.rs` keeps daemon configuration binary and does not link NOTA.
- `tests/instrumentation_logging.rs` asserts typed runtime object sequences.
- `tests/process_boundary.rs` includes the trace-enabled CLI/daemon socket
  witness using `SPIRIT_NEXT_TRACE_SOCKET`.
- `tests/dependency_surface.rs` proves the binary-only dependency boundary
  around `nota-next`.

## Remaining Gaps

The repo correctly carries these as known limits or open future work:

- generated `Help` root actions from Spirit 1396 are not implemented;
- `introspect` from Spirit 1398 is not implemented;
- extended trace headers from records 1400/1405/1408 are not implemented;
- `last-version` package from record 1372 is intentionally not faked because
  no real previous release input/tag exists;
- mail support remains emitter support rather than schema-authored core;
- `Store` is direct redb behind a mutex rather than the production
  `sema-engine` actor substrate.

No stale convenience trace API was found in the guidance surface.
