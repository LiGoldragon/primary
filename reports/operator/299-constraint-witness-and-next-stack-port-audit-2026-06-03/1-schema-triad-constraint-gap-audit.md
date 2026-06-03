# Schema / Triad Constraint Gap Audit

Operator sidecar audit, 2026-06-03. Scope: current `main` code and tests for
`schema-next`, `schema-rust-next`, `triad-runtime`, and `spirit-next`.

Main revisions inspected:

- `schema-next`: `ryxlvlzwqnvt` / `711b5fc9fe88` — `schema-next: preserve bare declarations as aliases`
- `schema-rust-next`: `nmpsslxxumum` / `a789a85e71b0` — `schema-rust: skip From impls for alias payloads`
- `triad-runtime`: `lzkpwskyzumn` / `2b51462fef72` — `triad-runtime: promote triad-engine readability essence`
- `spirit-next`: `uyzqqlzqzqrr` / `8461d3765e5f` — `spirit-next: use alias payloads end to end`

I did not run the full Nix checks. Evidence below is from repo guidance files,
source, tests, and flake check surfaces.

## Already Witnessed

Strong current witnesses:

- `spirit-next` has real daemon/CLI process-boundary witnesses. `tests/process_boundary.rs` starts `CARGO_BIN_EXE_spirit-next-daemon`, drives `CARGO_BIN_EXE_spirit-next`, parses generated `Output`, proves record / observe / remove / reject, and proves `.sema` durability across daemon restart (`tests/process_boundary.rs:157-295`).
- `spirit-next` has a real trace Layer 2 witness. `tests/instrumentation_logging.rs` drives `Engine::handle` through generated Signal, Nexus, and SEMA trait wrappers, asserts generated `ObjectName` values, archives/decodes `TraceEvent` with rkyv, and under `nota-text` parses the rendered trace back into `TraceEvent` (`tests/instrumentation_logging.rs:39-117`).
- `spirit-next` exposes that trace witness through Nix, including a process-boundary trace check: `test-testing-trace` and `test-testing-trace-process-boundary` (`flake.nix:181-188`).
- `spirit-next` has executable binary/text dependency witnesses. `tests/dependency_surface.rs` runs `cargo tree --edges normal --no-default-features` and asserts `nota-next` is absent, then asserts the `nota-text` tree contains it (`tests/dependency_surface.rs:30-50`).
- `spirit-next` has binary-wire negative witnesses. `tests/socket_negative.rs` sends length-prefixed raw NOTA and arbitrary bytes through `SignalTransport`, and raw NOTA through generated `Input::decode_signal_frame`; all must reject (`tests/socket_negative.rs:25-57`).
- `spirit-next` build freshness is strong. `build.rs` reads `schema/lib.schema` as `SchemaSource`, round-trips canonical source, lowers to `Asschema`, writes NOTA and rkyv artifacts, compares checked-in `schema/lib.asschema`, and emits Rust from the checked-in artifact while verifying binary artifact parity (`build.rs:26-74`, `build.rs:85-210`).
- `triad-runtime` has focused trace runtime tests over its real API: in-memory log, disabled sink, fallible socket recording, length-prefixed binary frame, socket listener, count-based collection, timeout, and generic `TraceClient` display edge (`tests/trace.rs:39-181`).
- `schema-next` has real cargo tests for strict schema syntax, source codec, raw core schema, asschema NOTA/rkyv, asschema store persistence, import resolution, collections, and macro lowering. Its flake exposes the cargo test as `checks.test` (`flake.nix:46-48`).

## Highest Risk Missing Witnesses

### 1. Canonical SymbolPath is not implemented or witnessed

Risk: maximum. Workspace essence now says symbols are paths through the schema
namespace and that this identity is canonical across schema, Rust emission,
NOTA rendering, trace identity, and help/description surfaces. I found no
`SymbolPath` type or direct witness in the four audited repos; current trace
identity uses generated `ObjectName` plus string `name()` projections
(`schema-rust-next/tests/emission.rs:473-494`, `spirit-next/src/schema/lib.rs`
around generated `ObjectName` / `TraceEvent`), not a shared canonical path
object.

Suggested witness:

- Add `SymbolPath` to `schema-next` as assembled-schema data, with paths for
  type, field, root variant, route, plane, and actor-boundary symbols.
- Add `schema-next/tests/symbol_path.rs`:
  - lower `tests/fixtures/spirit-crate/schema/lib.schema`;
  - assert paths such as `spirit-next:lib/Input/Record`,
    `spirit-next:lib/Entry/description`, `spirit-next:lib/sema/WriteInput/Record`;
  - round-trip each path through NOTA and rkyv;
  - assert invalid ad hoc strings fail to decode.
- Expose as a real Nix check through cargo test, not positive grep:
  `nix flake check .#checks.$system.test` or a split
  `checks.$system.symbol-path`.

Follow-on witness:

- In `schema-rust-next/tests/emission.rs`, assert generated `ObjectName` /
  `TraceEvent` carries or returns the exact generated `SymbolPath`, and that
  `TraceEvent` NOTA displays the path-derived shape. The current
  `generated_trace_identity_is_typed_from_interface_headers` test proves typed
  object names and rkyv, but not canonical symbol-path identity.

### 2. Trace adapter emission is still handwritten in `spirit-next`

Risk: high. Intent says schema-rust should eventually emit
`TraceEventFrame`, NOTA display adapter, and aliases for generic
`triad-runtime` trace client/log/socket. Current `spirit-next/src/trace.rs`
handwrites all of that: aliases to `triad-runtime`, `TraceEventFrame`, and
`Display`/`FromStr` for `TraceEvent` (`spirit-next/src/trace.rs:1-35`).

Already tested: the handwritten adapter works and is used in process-boundary
trace tests.

Missing constraint: no freshness or emission witness says this adapter is
generated or absent from the component once the emitter owns it.

Suggested witness:

- In `schema-rust-next`, add an emission test named
  `emits_trace_runtime_adapter_for_generated_trace_event` that compiles a
  generated fixture containing:
  - `impl triad_runtime::trace::TraceEventFrame for TraceEvent`;
  - `pub type TraceClient = triad_runtime::trace::TraceClient<TraceEvent>`;
  - `pub type TraceLog = ...`;
  - `Display` / `FromStr` gated on `nota-text`;
  - no trace-on-trace surface.
- In `spirit-next`, after consuming that emitted adapter, replace
  `src/trace.rs` with a re-export or remove it, then add a negative guard:
  no component-local `impl TraceEventFrame for TraceEvent`.

Exact command target:

- `nix flake check` in `schema-rust-next`, plus `nix flake check` in
  `spirit-next` with `test-testing-trace-process-boundary`.

### 3. Help / description namespace is intent-only

Risk: high for the next stack port because CLI help can easily regress into
string tables. `schema-rust-next/INTENT.md` says help/documentation are schema
data in a mirror description namespace keyed by fully qualified schema symbols.
I found no `Help`, `DescriptionNamespace`, or typed description data surface in
`schema-next` / `schema-rust-next` / `spirit-next`; occurrences of
`Description` are domain fields in Spirit schemas, not schema help metadata.

Suggested witness:

- Add schema-level description data in `schema-next` first, not CLI strings:
  `DescriptionNamespace` keyed by `SymbolPath`.
- Add `schema-next/tests/description_namespace.rs`:
  - lower a fixture with no explicit descriptions and assert generated default
    descriptions exist for every root/type/field/variant symbol;
  - lower a fixture with explicit description entries and assert they override
    the defaults by `SymbolPath`;
  - round-trip the description namespace through NOTA and rkyv.
- Add `schema-rust-next/tests/help_emission.rs`:
  - emit a generated typed help action or description table from assembled
    schema data;
  - assert it is data over `SymbolPath`, not `&'static str` CLI tables.
- Add `spirit-next` process-boundary test only after the generated help action
  exists: CLI prints help from generated typed data at the display edge.

### 4. Positive grep checks still masquerade as proof in schema repos

Risk: medium-high. The workspace testing skill allows negative grep guards but
rejects positive grep as architecture proof. Both schema repos still have many
positive flake checks that only prove text or function names exist:

- `schema-next`: `design-examples`, `macro-registry-used`,
  `declarative-schema-macros`, `operator-271-closed-claims`, and others grep
  for test names or source strings (`flake.nix:49-62`, `122-181`).
- `schema-rust-next`: `generated-rkyv-boundary`, `generated-nexus-traits`,
  `generated-mail-events`, `generated-nota-boundary`, and
  `generated-cross-crate-imports` grep fixture/source strings (`flake.nix:64-128`).

Some of those checks point to real cargo tests, so the underlying behavior is
not necessarily missing. The gap is that Nix advertises the grep check as the
constraint witness.

Suggested replacement pattern:

- Keep negative grep checks for retired surfaces.
- Convert positive checks to cargo test filters or small compile tests:
  - `schema-next`: use named tests that construct `SchemaEngine`,
    `MacroRegistry`, `MacroLibrary`, `AsschemaArtifact`, and `AsschemaStore`
    directly; expose as `craneLib.cargoTest` with `cargoExtraArgs = "--test
    operator_271_closed_claims"` instead of grep-for-test-name.
  - `schema-rust-next`: add fixture modules that include generated files and
    instantiate the generated traits/events/frames. Use type assertions and
    method calls, not string containment. For generated source shape that
    truly is text, use `syn` parsing in tests to assert an item exists with a
    particular signature.

### 5. `schema-rust-next` lacks a consumer-style trait implementation witness

Risk: medium-high. The emitter emits engine traits and Spirit consumes them,
so the end-to-end stack has coverage. But the emitter repo itself mostly
asserts generated code contains signatures and compiles. It does not yet have
a local consumer fixture implementing `SignalEngine`, `NexusEngine`, and
`SemaEngine` on data-bearing objects and proving the wrappers call the inner
methods plus trace hooks.

Suggested witness:

- Add `schema-rust-next/tests/generated_engine_trait_usage.rs`:
  - include the generated fixture;
  - define data-bearing `ExampleSignal`, `ExampleNexus`, `ExampleStore`;
  - implement generated traits by overriding inner methods and trace hooks;
  - call public wrappers `triage`, `reply`, `execute`, `apply`, `observe`;
  - assert wrapper trace order and typed generated envelopes.
- This would be a Layer 2 runtime witness inside the emitter repo, complementing
  `spirit-next`'s component-level runtime witness.

### 6. `triad-runtime` has no Nix-visible negative boundary checks

Risk: medium. `triad-runtime` correctly owns generic trace runtime and has real
tests. It does not have Nix checks guarding that it stays generic and does not
grow component-specific schema names or NOTA parsing. Current flake only
exposes `test` and `clippy`.

Suggested witness:

- Add negative guards in `triad-runtime/flake.nix`:
  - no `nota_next` or `nota-next`;
  - no `spirit_next`, `Spirit`, or component schema module names;
  - no component-specific `ObjectName` enum in runtime source.
- Add one positive type witness if/when `TraceEventFrame` becomes emitted:
  a generated event fixture in a test-only module can implement the trait and
  drive `TraceClient` without runtime knowing component-specific variants.

### 7. Local multi-repo override runner is present in Spirit by patches, but not as a named stack command

Risk: medium. `spirit-next` vendors/patches local `nota-next`,
`schema-next`, and `schema-rust-next`, and the flake has a
`local-schema-source-patches` check (`flake.nix:265-275`). That proves local
source patch wiring is present. It does not provide the explicit
multi-repo override command described in `skills/testing.md` for active stack
port work.

Suggested witness:

- Add a versioned script or flake app in `spirit-next`, for example
  `apps.local-next-stack-check`, that runs:
  - `nix flake check`
  - with `--override-input nota-next-source path:/git/github.com/LiGoldragon/nota-next`
  - `--override-input schema-next-source path:/git/github.com/LiGoldragon/schema-next`
  - `--override-input schema-rust-next-source path:/git/github.com/LiGoldragon/schema-rust-next`
- This should run at least the build freshness path, process-boundary test,
  dependency-surface test, and trace process-boundary test.

## Suggested Next Slice

Best next operator slice: implement the `SymbolPath` witness in `schema-next`
first. It is upstream of trace identity, help/description data, generated
Rust symbol identity, and future NOTA display. The cheapest useful first test
is a pure cargo test over lowered `Asschema` from an existing Spirit fixture,
round-tripping paths through NOTA and rkyv.

Second slice: move `TraceEventFrame` / trace aliases / display adapter emission
into `schema-rust-next`, then delete or shrink `spirit-next/src/trace.rs` and
keep the existing `spirit-next` process-boundary trace test as the consumer
proof.
