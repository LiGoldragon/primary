# schema-rust-next Findings

## Current Repo State

Checked revision:

- commit `a8c0f012142f` on `main`
- change `wwovnwtxnlro`
- description: `schema-rust: emit per-plane trace object names`

The working copy was clean.

## Guidance Files

Read:

- `AGENTS.md`: thin shim to workspace `AGENTS.md`.
- `INTENT.md`: present and current.
- `ARCHITECTURE.md`: present and current.

Missing:

- `skills.md`: absent. This is not a blocker for this pass, but it means fresh
  agents rely on workspace skills plus `INTENT.md` / `ARCHITECTURE.md` only.

## Manifestation Verdict

No repo edit is needed right now.

`INTENT.md` already manifests the fresh trace/triad intent:

- generated Rust is source-visible under `src/schema/`;
- generated schema objects are the behavior nouns;
- Signal/Nexus/SEMA roots emit generated engine traits;
- trace hooks belong to generated engine traits, not local side traits;
- hooks take typed per-plane object-name enums:
  `SignalObjectName`, `NexusObjectName`, `SemaObjectName`;
- shared `ObjectName` wraps the per-plane names for `TraceEvent` transport;
- trace events do not carry cloned payload snapshots;
- consumers should not carry stringly trace vocabularies beside the generated
  actor/interface contract.

`ARCHITECTURE.md` already states the live shape:

- `RustEmitter` maps `Asschema` into `RustModule`, then rendered source;
- root declarations emit Signal, Nexus, and SEMA traits;
- runtime code implements those traits on data-bearing engine objects;
- generated wrappers own `triage` / `reply` / `execute` / `apply` / `observe`;
- implementors fill inner behavior methods and trace hooks;
- trace hooks activate typed generated object names, not strings;
- `TraceEvent` carries generated `ObjectName`.

## Code Evidence

Search evidence confirmed the docs match the implementation:

- `src/lib.rs` emits `SignalObjectName`, `NexusObjectName`,
  `SemaObjectName`, `ObjectName`, and `TraceEvent`.
- `src/lib.rs` emits trace hook methods on generated `SignalEngine`,
  `NexusEngine`, and `SemaEngine`.
- `tests/fixtures/*generated*.rs` contain the generated typed trace objects.
- `tests/emission.rs` includes a rkyv round-trip for generated `TraceEvent`
  and object-name values.

## Remaining Gap

Some emitter tests still assert generated source fragments with
`contains(...)`. For a code generator, source-text assertions are valid Layer 1
emission checks, but they are not proof that runtime actors used those traits.
That proof currently belongs in `spirit-next`. If `schema-rust-next` ever
claims runtime-use proof on its own, it should add a compile/run fixture that
implements the generated traits and records typed `ObjectName` values through
the wrapper methods.
