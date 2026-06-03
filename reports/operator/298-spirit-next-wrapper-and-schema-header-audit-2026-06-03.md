# spirit-next wrapper and schema-header audit — 2026-06-03

## Scope

Target repo: `/git/github.com/LiGoldragon/spirit-next`.

Task: audit handwritten runtime/test code for nested generated wrapper
construction and stale schema-header documentation. `src/schema/lib.rs` is
generated and was inspected but not edited.

## Working-copy state

The repo was already dirty on entry, including `schema/lib.schema`,
`schema/lib.asschema`, `src/schema/lib.rs`, handwritten runtime files, and
tests. The generated file currently contains wrapper structs plus generated
constructors, but it does not compile because the generator emitted
`pub fn continue(payload: NexusWork) -> Self` at
`src/schema/lib.rs:1659`; `continue` is a Rust keyword. This must be fixed by
schema-rust-next regeneration, not by hand-editing the generated file.

Probe run:

```sh
cargo test --no-run
```

Result: failed before handwritten-code type checking with the generated
keyword collision above.

## Runtime wrapper construction

Current generated surface still has alias wrapper structs such as
`Record`, `RecordAccepted`, `Rejected`, `Recorded`, `Observed`, and the
Nexus wrapper objects. It also has generated constructors such as
`Input::record`, `Output::rejected`, `NexusWork::signal_arrived`,
`NexusAction::command_sema_write`, and SEMA root constructors. The handwritten
code is mixed: some code still constructs wrappers manually; other tests have
already moved to direct payload variants that do not match the current
generated file.

### Manual nested wrapper sites

- `tests/generated_signal_plane.rs:17`, `:87`, `:111` construct
  `Input::Record(Record(Entry { ... }))`.
  Suggested replacement once the generated constructor surface is buildable:
  `Input::record(Entry { ... })`.
- `tests/generated_signal_plane.rs:36` constructs
  `Output::RecordAccepted(RecordAccepted(SemaReceipt { ... }))`.
  Suggested replacement: `Output::record_accepted(SemaReceipt { ... })`.
- `tests/generated_signal_plane.rs:52` and `:77`,
  `src/engine.rs:529`, `src/nexus.rs:322`, and
  `tests/runtime_triad.rs:681` construct
  `Output::Rejected(Rejected(SignalRejection { ... }))`.
  Suggested replacement: `Output::rejected(SignalRejection { ... })`.
- `src/nexus.rs:316`, `:334`, `:337`, `:361`, `:364`, `:378`,
  `src/engine.rs:543`, and `src/store.rs:67-145` construct output roots by
  manually wrapping generated alias objects:
  `RecordsObserved(...)`, `RecordAccepted(...)`, `RecordRemoved(...)`,
  `RecordFound(...)`, `RecordsCounted(...)`, `RecordsStashed(...)`,
  `Error(...)`, `Recorded(...)`, `Missed(...)`, `Removed(...)`,
  `Observed(...)`, `Found(...)`, and `Counted(...)`.
  Suggested replacements: use the generated root constructors:
  `Output::records_observed`, `Output::record_accepted`,
  `Output::record_removed`, `Output::record_found`,
  `Output::records_counted`, `Output::records_stashed`, `Output::error`,
  `SemaWriteOutput::recorded`, `SemaWriteOutput::missed`,
  `SemaWriteOutput::removed`, `SemaReadOutput::observed`,
  `SemaReadOutput::found`, and `SemaReadOutput::counted`.
- `src/nexus.rs:238-255`, `:286-293`, `:302-315`, `:353`,
  `tests/runtime_triad.rs:146-167`, `:189`, `:250`, `:322`, `:702`,
  `:751`, `:778`, and `:790` still match or build Nexus wrappers such as
  `ReplyToSignal`, `CommandSemaWrite`, `CommandSemaRead`, `CommandEffect`,
  `Continue`, `SignalArrived`, `SemaWriteCompleted`, and
  `SemaReadCompleted`. Matching wrapper payloads is currently required by
  the generated type definitions; construction should move to generated
  constructors such as `NexusAction::reply_to_signal(...)` and
  `NexusWork::signal_arrived(...)` once the keyword collision is fixed.

### Direct-payload sites that are ahead of current generation

- `tests/nix_integration.rs:386` matches
  `Output::RecordAccepted(SemaReceipt { ... })`.
- `tests/nix_integration.rs:415` constructs
  `Output::Rejected(SignalRejection { ... })`.
- `tests/nix_integration.rs:528` matches
  `Output::Error(ErrorReport { ... })`.
- `tests/nix_integration.rs:441`, `:451`, `:492`, and `:559` bind
  `Output` variants and access fields such as `receipt.database_marker` or
  `records.record_set` directly, assuming the variant binding is the payload
  rather than an alias wrapper.
- `tests/process_boundary.rs:173`, `:271`, `:287`, `:312`, `:341`, and
  `:383` have the same direct-payload assumption after matching
  `Output::RecordAccepted` or `Output::RecordsObserved`.
- `tests/instrumentation_logging.rs:45`, `:51`, `:158`, and `:183` call
  `Input::Record(entry(...))`, `Input::Observe(Query { ... })`, or compare
  `Output::Rejected(SignalRejection { ... })`.
- `tests/instrumentation_logging.rs:47` treats the
  `Output::RecordAccepted` binding as a `SemaReceipt` by accessing
  `receipt.database_marker` directly.

Those direct-payload forms are the intended direction after alias lowering,
but they do not match the current generated wrapper file. The lower-risk
intermediate replacement is generated constructors for construction sites and
wrapper-aware pattern matches until alias lowering lands. After alias lowering,
direct payload pattern matches become the simpler final shape.

### Wrapper expectation test

`tests/operator_271_closed_claims.rs:184-203` explicitly asserts generated
wrapper structs and nested enum variants, including `Record(Record)`,
`RecordAccepted(RecordAccepted)`, `RecordsObserved(RecordsObserved)`, and
`Rejected(Rejected)`. That test is now a stale guard: it encodes the wrapper
shape the new design wants to retire. After alias lowering lands, replace it
with absence/constructor/API-shape checks that prove generated root
constructors or direct payload variants, not nested wrappers.

## Schema-header documentation

Repo docs had stale parenthesized schema-body prose:

- `INTENT.md:40-43` described enum bodies as lists containing
  parenthesized records such as `(Record Entry)`.
- `ARCHITECTURE.md:66-68` and `:263-264` described data-carrying
  enum variants as parenthesized signatures.

I edited both files to state the current shape: root enum bodies are bare
square-bracket lists of exported object names, and namespace bindings such as
`Record Entry`, `RecordAccepted SemaReceipt`, and `SignalArrived Input` define
payload shape. A follow-up scan of `README.md`, `INTENT.md`, and
`ARCHITECTURE.md` found no remaining `(Record Entry)` /
`(RecordAccepted SemaReceipt)` header prose.

Older operator reports still carry stale root-header examples. Notable matches:

- `reports/operator/282-trace-header-generated-interface-situation-2026-06-02.md`
  lines 23-31.
- `reports/operator/297-Psyche-typed-text-design-audit-2026-06-03.md`
  lines 59-65 and 135-136.
- `reports/operator/290-enum-payload-variant-pattern-2026-06-02.md`
  lines 58, 163, 322-329.
- `reports/operator/287-nexus-recursive-computation-continuation-2026-06-02.md`
  lines 136-139 and 239-255.
- `reports/operator/281-generated-interface-logic-with-macros-2026-06-02.md`
  lines 29-37.
- `reports/operator/248-schema-nota-spirit-whole-stack-tour.md`
  lines 73-84.

These should be treated as superseded working reports, not current doc
surfaces. If a context-maintenance pass keeps any of them active, add a
supersession note pointing to the bare-header + namespace-binding rule.

## Edits made

- `INTENT.md`: updated schema-body prose to bare exported object names plus
  namespace payload bindings.
- `ARCHITECTURE.md`: updated the same schema-body shape in both current-schema
  paragraphs.
- `reports/operator/298-spirit-next-wrapper-and-schema-header-audit-2026-06-03.md`:
  this audit report.

No Rust runtime/test files were edited. `src/schema/lib.rs` was not edited.

## Tests to rerun after regeneration

Run these after schema-next/schema-rust-next are repinned and `src/schema/lib.rs`
is regenerated with a keyword-safe constructor surface:

```sh
cargo test --no-run
cargo test
cargo test --features nota-text
cargo test --features testing-trace
nix flake check
scripts/check-local-schema-stack
nix run .#nix-integration-tests
```

If alias lowering lands in the same wave, also rerun a focused scan before
committing:

```sh
rg -n "Output::Rejected\\(Rejected|Input::Record\\(Record|RecordAccepted\\(RecordAccepted|Rejected\\(Rejected|Record\\(Record" src tests -g '*.rs' -g '!src/schema/lib.rs'
rg -n "\\[\\(Record|\\[\\(RecordAccepted|NexusWork \\[\\(|NexusAction \\[\\(|SemaWriteInput \\[\\(|SemaReadInput \\[\\(" README.md INTENT.md ARCHITECTURE.md /home/li/primary/reports/operator -g '*.md'
```
