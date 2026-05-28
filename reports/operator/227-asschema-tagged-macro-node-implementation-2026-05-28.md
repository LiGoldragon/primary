# 227 — Retired Tagged-Macro Implementation Report

This operator report is retired.

The earlier body described an intermediate no-sigil macro-call pass. That pass
has been superseded by the current split:

- Native NOTA owns the built-in reference forms.
- Schema macros remain data objects, but collection references are no longer
  authored as collection macro calls.
- Rust emission consumes typed assembled schema, not authored schema syntax.

Current references:

- `reports/operator/229-nota-current-design-2026-05-28.md`
- `reports/operator/230-schema-current-design-2026-05-28.md`
- `reports/operator/231-signal-nexus-sema-current-design-2026-05-28.md`
