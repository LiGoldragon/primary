# Triad Engine Intent Manifestation Blocked

*Kind: operator report · Topics: spirit-next, schema-rust-next, triad-engine, intent-manifestation · 2026-06-02*

## Scope

Task: spread Spirit record 1419 into repo `INTENT.md` and
`ARCHITECTURE.md` surfaces where it belongs.

Record 1419 says triad engine wiring should be generated/programmatic; daemon
main should shrink to a tiny generated runner or macro call; and domain logic
belongs in non-default algorithm implementations on generated Signal, Nexus,
and SEMA engine traits. Nexus owns heavier decision algorithms, SEMA owns
durable indexes/state, and Signal owns communication.

## Coordination Result

The target repos were already claimed by the main operator:

- `/git/github.com/LiGoldragon/spirit-next`
- `/git/github.com/LiGoldragon/schema-rust-next`

The active claim reason was `triad engine programmatic runner implementation`.
I attempted a `second-operator` claim for the same two repos; the helper
reported overlap with `operator` and cleared the attempted claim. I did not
edit either repo under the main operator's claim.

## Guidance Checked

Read each target repo's `AGENTS.md`, `INTENT.md`, and `ARCHITECTURE.md`.
Both repos currently lack root `skills.md`, so there was no repo-specific
skills file to read.

`schema-next` was also read. Record 1419 does not require a `schema-next`
architecture edit: the record concerns generated Rust engine wiring and
runtime placement of domain algorithms, not the schema lowering surface.

## Manifestation Gaps

### schema-rust-next

Current docs already say generated objects are behavior nouns, generated
Signal/Nexus/SEMA traits are the working path, and old convenience wrappers do
not stay. They do not yet state the new record 1419 endpoint:

- triad engine wiring itself should be emitted/programmatic;
- component daemon runner setup should be generated or macro-projected from the
  schema-emitted engine substrate;
- generated engine traits should expose non-default algorithm extension points
  where domain logic lives.

Precise insertion targets:

- `INTENT.md` after the current schema-plane trait paragraph around lines 66-75.
- `ARCHITECTURE.md` after the generated objects / behavior surfaces constraint
  around lines 101-105, or after the engine-trait paragraph around lines
  106-115.

Suggested wording:

> Triad engine wiring is generated/programmatic. The emitter should be able to
> generate the runner surface that connects Signal, Nexus, and SEMA engine
> implementations so a component daemon main can shrink to a tiny generated
> runner or macro call. Runtime domain logic belongs in non-default algorithm
> implementations on the generated engine traits: Signal algorithms stay
> communication/admission/reply oriented, Nexus algorithms own heavier
> decision-making, and SEMA algorithms own durable indexes and state.

### spirit-next

Current docs already say `SignalActor`, `Nexus`, and `Store` implement the
generated traits, that `Engine` is a thin composer, and that the daemon/CLI
implementation is a shim around generated interfaces. They do not yet state
the record 1419 target that daemon main should shrink to generated runner
construction and that domain logic should be expressed as non-default
algorithm implementations on generated traits.

Precise insertion targets:

- `INTENT.md` after the `schema-rust-next emits SignalEngine...` bullet around
  lines 96-102.
- `ARCHITECTURE.md` in `## Runtime triad`, after the sentence at line 81, or
  in `## Implementation methods` after the paragraph around lines 248-249.

Suggested wording:

> The runner/composition layer should become generated or macro-driven.
> `spirit-next-daemon` main should remain a tiny binary entrypoint that invokes
> the generated runner with binary configuration; it should not accumulate
> orchestration logic. Domain-specific algorithms live as non-default
> implementations on the generated `SignalEngine`, `NexusEngine`, and
> `SemaEngine` traits. Signal owns communication, Nexus owns heavier
> topic-discovery and decision algorithms, and SEMA owns durable indexes/state.

## Evidence

Fresh intent read:

- `spirit "(Observe (RecordIdentifiers ((Range (1326 1419)) SummaryOnly)))"`

Repo guidance read:

- `schema-rust-next/AGENTS.md`, `INTENT.md`, `ARCHITECTURE.md`
- `spirit-next/AGENTS.md`, `INTENT.md`, `ARCHITECTURE.md`
- `schema-next/AGENTS.md`, `INTENT.md`, `ARCHITECTURE.md`

Status checks:

- `tools/orchestrate status`
- failed `tools/orchestrate claim second-operator ...` due overlap with
  `operator`

## Files Changed

Changed only this report:

- `reports/operator/286-triad-engine-intent-manifestation-blocked-2026-06-02.md`

No repo files were edited because the active main operator claim covers the
same target repos and same workstream.

## Main Operator Action

When the active programmatic-runner implementation reaches the doc update step,
fold the suggested wording into `schema-rust-next` and `spirit-next` in the
line ranges above, then commit those repo edits on main under the active claim.
