# 180.0 - Frame and method

## Trigger

Psyche asked operator to keep working on Spirit/schema after the latest
schema and upgrade design reports, with explicit permission to use
subagents. The immediate live issue was that schema-derived macro output
still carried Spirit-specific field-name guesses in `signal-frame`.

## Inputs read

- `reports/designer/326-v13-spirit-complete-schema-vision.md`
- `reports/designer/329-schema-macro-component-extensibility.md`
- `reports/designer/333-upgrade-mechanism-full-design-explained.md`
- `reports/designer/333-v2-upgrade-mechanism-corrections-from-real-world-test.md`
- `reports/designer/334-v2-multi-pass-nota-first-schema-reader.md`
- `reports/nota-designer/8-nota-schema-lowering-deviation-audit.md`
- `reports/operator/176-schema-macro-upgrade-integration-audit/5-overview.md`
- `reports/operator/179-schema-field-override-and-upgrade-constraints-2026-05-25.md`
- `reports/second-operator/180-schema-v13-model-and-upgrade-implementation-2026-05-24.md`
- `reports/second-operator/181-schema-e2e-reader-and-redesign-2026-05-24.md`
- `reports/second-operator/186-orchestrate-upgrade-socket-implementation-2026-05-25.md`

## Intent state

The latest designer-logged intent for the prompt was read from Spirit:

- record 569: schema macro application is iterative to a fixed point.
- record 570: schema namespaces are dependency-ordered.
- record 571: newtype emits a Rust single-tuple wrapper.

One missing workflow-level record was added:

- record 574: schema-era design rolls forward globally while one
  component proves each step.

Psyche explicitly said not to duplicate-log the prompt itself, so no
second capture of the same schema design statements was made.

## Subagents

Two explorer subagents were dispatched:

- Bohr: architecture synthesis across schema/upgrade reports.
- Hegel: code-path audit for Spirit/schema implementation gaps.

The implementation followed Hegel's narrow recommendation: remove
Spirit-specific field-name inference from `signal-frame` by preserving
explicit field names from `spirit.schema` through the macro model.

## Work products

- `signal-frame` main: `e4e1581c` -
  `signal-frame: preserve schema field names in macro emission`
- `signal-persona-spirit` main: `03d160b5` -
  `signal-persona-spirit: name schema fields for macro emission`

Designer-owned dirty docs in `signal-persona-spirit/ARCHITECTURE.md`
were left untouched.
