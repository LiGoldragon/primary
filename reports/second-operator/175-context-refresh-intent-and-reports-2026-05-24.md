*Kind: Review · Topic: context-refresh-intent-and-reports · Date: 2026-05-24*

# 175 — Context refresh after Spirit 396

## Prompt classification

The prompt was a work instruction to refresh context. I did not find
a durable psyche intent statement in the prompt itself, so I did not
record a new Spirit entry.

## Sources refreshed

- Workspace contract: `ESSENCE.md`, `INTENT.md`,
  `repos/lore/AGENTS.md`, `orchestrate/AGENTS.md`.
- Role and mechanism skills: `skills/operator.md`,
  `skills/reporting.md`, `skills/intent-log.md`,
  `skills/spirit-cli.md`, `skills/jj.md`.
- Spirit records via `spirit '(Observe (Records (None None SummaryOnly)))'`,
  now visible through record 396.
- Fresh reports in the designer, operator, second-designer, and
  second-operator lanes, especially:
  `reports/designer/317-sema-upgrade-and-macro-convergence-audit/`,
  `reports/designer/318-upgrade-merger-and-persona-prefix-rename/`,
  `reports/operator/166-sema-upgrade-and-schema-macro-current-state-2026-05-24.md`,
  `reports/operator/167-recent-reports-and-intent-refresh-2026-05-24.md`,
  `reports/operator/168-latest-design-intent-and-bead-orientation-2026-05-24.md`,
  `reports/operator/169-post-318-refresh-and-next-work-2026-05-24.md`,
  and
  `reports/second-designer/163-signal-sema-interaction-and-spirit-architecture-2026-05-24.md`.

## Current operating frame

- `second-operator` remains an operator lane. Reports land under
  `reports/second-operator/`. Subagents are not used unless the
  psyche explicitly asks.
- Chat should stay short. Substantive synthesis belongs in this
  report lane, with chat carrying the report path and user-attention
  items.
- `jj` is the version-control tool. Description-taking commands use
  inline messages. Before committing, isolate only this lane's files;
  the working copy currently includes an unrelated pi-operator report.
- All Nix invocations use `--option max-jobs 0`.

## Intent absorbed

Spirit records 366-396 materially shift the context:

- The upgrade path goes through next-version-as-Cargo-dependency:
  each schema crate can depend on the next schema crate so generation
  can emit `VersionProjection` at compile time.
- The old "Tier 1 micro / small object / small message" language is
  superseded by **short header** or **64-bit short header**.
- MVP short headers are simple: one root enum plus seven sub-enums,
  one byte each. Packing optimizations are later work.
- Sema gets a symmetric sema short header. Tap-anywhere observability
  extends across signal and sema surfaces.
- The source of schema truth is moving out of Rust macro syntax into
  a specialized NOTA schema language. The macro/codegen layer consumes
  structured schema data and emits Rust types, codec impls, slot
  assignment tables, version diffs, signal surfaces, sema operations,
  and sema lowering operations.
- Contract schema top level is a vector of root-verb enums. Variants
  are themselves enums or data-carrying enums; the two-layer
  enum-of-enums structure is mandatory.
- Schema references may be inline or file-path based, with paths
  resolved into the full spec before macro processing.
- `upgrade` is now the merged component triad:
  `upgrade`, `signal-upgrade`, and `owner-signal-upgrade`.
  `version-projection` remains a library. This supersedes older
  uncertainty about whether `sema-upgrade` becomes a separate daemon.
- Component crate names drop the `persona-` prefix except for
  agent-harness backends such as `persona-pi`, `persona-claude`,
  `persona-codex`, `persona-gemini`, and `persona-open-code`.

## Reports absorbed

The current operator/designer picture is:

- `/317` defines the macro convergence epic. The old implemented
  surface is `signal_channel!`; it emits current signal-frame
  contract scaffolding but not the full new Help, short-header,
  next-version projection, sema operation, or sema lowering surface.
- `/318` defines the upgrade merger and persona-prefix rename wave.
  Operator `/169` says several /318 implementation beads have landed:
  `signal-upgrade` and `owner-signal-upgrade` contract merger work,
  moving sema-upgrade/catalogue substance into `upgrade`, narrowing
  Persona's role, and renaming runtime lookup types in
  `version-projection`.
- `/315` is now partly historical: its open "Persona absorbs vs
  separate sema-upgrade daemon" question is answered by record 369
  in favor of the merged `upgrade` triad.
- `/316` keeps the Forge family current direction alive, but it is
  not the main thread of this lane right now.
- Second-designer `/163` is useful for the current signal/sema mental
  model: signal-frame owns the current macro surface, signal-sema is
  currently plain Rust vocabulary/traits, and daemon code performs the
  lowering. Newer records 390-396 extend that model toward symmetric
  sema short headers and NOTA-schema-driven generation.

## Situation

The second-operator reports from 173 and 174 are still useful as lane
history, but they are stale on the schema/macro axis. Any next
implementation choice should treat records 366-396 and designer
317/318 as the current frame.

The most contextualized implementation work appears to be one of:

- macro/schema convergence, especially the path from current
  `signal_channel!` toward NOTA-schema-driven generation;
- small follow-up slices around `upgrade` after the /318 operator
  landings;
- returning to persona-orchestrate only if the psyche explicitly
  routes this lane back to that earlier context.

## Still-relevant questions

1. Should this second-operator lane now follow the macro/schema
   convergence thread, or return to its earlier persona-orchestrate
   lane-registry context?
2. For immediate implementation, is the preferred first slice the
   existing macro surface in `signal-frame-macros`, or the NOTA schema
   language source layer that will eventually feed it?
3. Should older reports in this lane be marked stale by a small
   follow-up consolidation report, or is this refresh enough until
   the next context-maintenance pass?
