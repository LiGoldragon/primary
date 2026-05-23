# 0 — Frame and dispatch

## Frame

The core NOTA bracket-string work is already on `main`:

- `nota-codec` main at `538555e8` implements bracket strings,
  block strings, canonical bracket encoding, map-key constraints,
  custom map key types, and mixed enum support.
- `nota` main at `40d62711` documents the grammar and examples.
- BEADS `primary-36iq.1` and `primary-36iq.2` are closed with Nix
  verification evidence.

This session starts the downstream migration for `primary-36iq`
(coordinate NOTA bracket-string merge and consumer migration),
especially `primary-36iq.3`, `primary-36iq.6`, and
`primary-36iq.7`.

## Refreshed Intent

The live Spirit scan changed the execution shape in five ways:

- Record 231: sub-agent sessions land in a meta-report directory
  `reports/<role>/<N>-<name>/`; each sub-agent writes one final
  subreport there.
- Record 241: refresh reports and intent before choosing next work.
- Record 242: after bracket-string support is well tested, normal
  NOTA migration avoids quotation-mark string syntax wherever
  practical and prefers bracket strings for authored examples and
  component usage.
- Record 243: visuals in reports are Mermaid diagrams only; no ASCII
  text-block diagrams.
- Testing intent plus `skills/testing.md`: `cargo test` is an
  inner-loop convenience, not final evidence. Migration tests need
  Nix-owned checks or named Nix witnesses.

The prompt itself is treated as task direction, not new durable intent:
it authorizes subagents and asks for this migration start.

## Recent Report Context

Recent designer and second-designer reports reinforce these execution
rules:

- `reports/second-designer/159-intent-manifestation/7-overview.md`
  established the exact meta-report-directory pattern used here.
- `reports/second-designer/159-intent-manifestation/6-operator-work-audit.md`
  and `reports/designer/302-audit-recent-operator-work-2026-05-23.md`
  favor constraint tests and end-to-end Nix witnesses over local-only
  tests.
- `reports/designer/301-design-elegant-cli-macro-with-caller-injection.md`
  and `reports/designer/298-design-help-operations-in-components.md`
  mean any component CLI examples touched during this migration should
  preserve the single-NOTA-argument shape and avoid flag-shaped help or
  configuration.
- `reports/designer/297-design-signal-persona-auth-rename.md`,
  `reports/designer/299-design-origin-process-and-agent-identity.md`,
  and active locks show that Persona/signal repos are undergoing a
  signal-persona-origin rename. Those surfaces are read-only in this
  migration until the rename lock clears.

## Test Naming Preference

Migration tests should read like constraints. Preferred shapes:

- `nota_argument_accepts_apostrophe_text_without_quote_delimiters`
- `cli_accepts_bracket_string_with_apostrophe`
- `canonical_examples_emit_bracket_strings`
- `help_examples_do_not_require_quote_delimiters`
- `legacy_quote_strings_decode_only_as_legacy_coverage`

Avoid vague names like `test_bracket_strings` when the behavior under
protection is more specific.

## Active Lock Constraint

`tools/orchestrate status` showed `second-operator` holding a broad
rename lock over `/home/li/primary` and many Persona/signal repos:
`signal-persona-auth`, `signal-persona-origin`, `signal-persona`,
`signal-persona-message`, `signal-persona-router`,
`signal-persona-mind`, `persona`, `persona-spirit`,
`persona-message`, `persona-introspect`, `persona-system`,
`persona-harness`, `persona-terminal`, `signal-frame`,
`signal-core`, `criome`, and more.

Reports under this directory are exempt from the claim flow, but repo
source edits in those locked surfaces are out of scope for this session.

## Subagent Slices

Four subagents were dispatched with disjoint scopes:

- `1-nota-config-and-spirit-surface.md` — implement/update
  `nota-config` and report Spirit-facing follow-ons.
- `2-deploy-stack-consumers.md` — audit/migrate unlocked deploy-stack
  consumers: `horizon-rs`, `lojix-cli`, `lojix`.
- `3-adjacent-nota-consumers.md` — audit/migrate adjacent unlocked
  consumers: `nexus`, `nexus-cli`, `chronos`, `chroma`.
- `4-locked-persona-signal-audit.md` — read-only audit for locked
  Persona/signal surfaces and deferred migration plan.

