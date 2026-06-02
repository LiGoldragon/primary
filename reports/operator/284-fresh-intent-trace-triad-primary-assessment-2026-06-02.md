# Fresh Intent Trace/Triad Primary Assessment

*Kind: operator audit · Topics: spirit-next, schema-rust-next, testing-trace, triad-engine, fresh-intent · 2026-06-02*

## Scope

This is the main operator pass requested before the asynchronous per-repo
`INTENT.md` / `ARCHITECTURE.md` maintenance subagent returns.

The audit checks the recent operator work against fresh Spirit intent around:

- schema-generated typed trace names;
- runtime proof of Signal / Nexus / SEMA interface use;
- compact versus extended trace identity;
- no old design-convenience APIs;
- avoiding source-presence checks as proof.

The harness could not spawn a new subagent because the thread limit is reached,
so the maintenance brief was queued to an existing subagent asynchronously.

## Fresh Constraint Refresh

The current load-bearing records for this slice are:

- 1339: remove old design convenience APIs once the working path exists.
- 1341 and 1342: positive grep does not prove live architecture; tests must
  execute the real path.
- 1343 through 1350: testing trace is the runtime witness surface and should
  prove real Signal / Nexus / SEMA usage.
- 1365, 1392, 1393: trace belongs to schema-generated interface and actor
  traits, with default implementations, not local parallel trace traits.
- 1394: trace needs only the activated object name.
- 1395 and 1401: interfaces should be developed multi-variant root enums; a
  single-variant root is usually a newtype in disguise.
- 1396: every root enum should later get an automatic generated Help action.
- 1398: `introspect` is the future trace destination and queryable
  intelligence component.
- 1400, 1405, 1408: trace identity is macro-emitted from interface headers;
  compact object names are live first, extended headers remain an open
  diagnostic layer.
- 1411: beauty is a gate; avoid clutter, duplicate surfaces, and hand-written
  code where schema can drive.

## Current Verdict

The latest operator work is aligned with the compact trace-name slice.

`schema-rust-next` main at `a8c0f012` emits typed per-plane object-name enums:

- `SignalObjectName`
- `NexusObjectName`
- `SemaObjectName`
- shared `ObjectName`
- `TraceEvent { object_name: ObjectName }`

`spirit-next` main at `f8ab8487` consumes those generated names through the
generated engine trait hooks:

- `SignalEngine::trace_signal_activation(SignalObjectName)`
- `NexusEngine::trace_nexus_activation(NexusObjectName)`
- `SemaEngine::trace_sema_activation(SemaObjectName)`

The runtime trace path is not a grep proof. It is tested through the real
daemon boundary: CLI sends the normal request to the daemon, daemon emits
binary `TraceEvent` frames on the trace socket, and CLI decodes and renders
them. That satisfies the Layer 2 runtime-witness requirement for the compact
trace slice.

## Evidence Checked

Code shape:

- `spirit-next/src/schema/lib.rs` contains generated per-plane object-name
  enums and generated trace hooks on `SignalEngine`, `NexusEngine`, and
  `SemaEngine`.
- `spirit-next/src/engine.rs`, `src/nexus.rs`, and `src/store.rs` override the
  generated hooks and wrap the plane-local object name in generated
  `ObjectName`.
- `spirit-next/tests/instrumentation_logging.rs` asserts the actual runtime
  activation sequence crosses Signal, Nexus, and SEMA.
- `spirit-next/tests/process_boundary.rs` asserts trace frames return from a
  trace-enabled daemon to the CLI over the configured trace socket.

Verification already run for the committed work:

- `schema-rust-next`: `cargo test`, `cargo fmt --check`,
  `cargo clippy --all-targets -- -D warnings`.
- `spirit-next`: `cargo test --no-default-features`,
  `cargo test --features nota-text`,
  `cargo test --features nota-text,testing-trace`,
  focused trace-socket process-boundary test, `cargo fmt --check`,
  `cargo clippy --all-targets --features nota-text,testing-trace -- -D warnings`.

## What Is Still Open

The open work is now clearer than before:

1. **Generated Help actions.** Spirit 1396 is not implemented. Root enums do
   not yet get generated `Help` variants or generated help-message roots from
   schema descriptions.

2. **`introspect` component.** Spirit 1398 is not implemented. Trace has a live
   CLI/debug sink, but there is no schema-next `introspect` component that can
   subscribe, decide what to log, store trace intelligence, and answer queries.

3. **Extended trace headers.** Compact typed object names are live. Extended
   row-chain identity from 1400/1405/1408 is still design/open work. The
   current implementation stops at the root route or actor-boundary name.

4. **Interface descriptions as data.** Help and richer trace both need schema
   interface descriptions to become emitted data, not only route enums and
   names. The current emitter derives names from roots but does not yet emit a
   first-class interface-description noun.

5. **Nix last-version package.** Spirit 1372 remains intentionally un-faked in
   `spirit-next`: the architecture says a future package needs a real previous
   release input/tag. That is correct, but still open.

6. **Report/context retirement.** The current report set is still large. Recent
   context maintenance removed or migrated some stale material, but fresh
   intent 1411 raises the standard: old rationale-only surfaces should keep
   being migrated into architecture/skills and then retired.

## Primary Focus Now

The next implementation focus should be:

1. keep `schema-rust-next` as the source of interface behavior;
2. add generated interface-description data;
3. use that data to implement automatic `Help` root actions;
4. then route the same description/trace substrate into the new `introspect`
   component.

That order keeps the work schema-first and avoids building an ad-hoc
introspection side channel.

## Subagent Follow-Up

The queued maintenance subagent should verify whether the repo
`INTENT.md` / `ARCHITECTURE.md` surfaces for `schema-rust-next`,
`spirit-next`, and directly-related `schema-next` / `nota-next` material still
match the live code and the fresh Spirit records above.

When it returns, the operator should re-analyze against its findings and make
small immediate corrections before starting the next feature slice.
