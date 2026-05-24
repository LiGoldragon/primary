*Kind: Frame · Topic: schema-macro-upgrade-integration-audit · Date: 2026-05-24 · Lane: operator*

# 176 · Schema macro + upgrade integration audit

## Prompt

Audit whether the upgrade code, header-derivation code, schema-derived
implementations, and the intended schema macro outputs are used directly in
the corresponding component, contract, CLI, and daemon logic.

## Method

Four read-only subagent slices:

1. Schema/header/macro layer: `signal-frame`, `signal-frame-macros`,
   `nota`, and `signal-persona-spirit`.
2. Upgrade/version/handover layer: `upgrade`, `signal-upgrade`,
   `owner-signal-upgrade`, `version-projection`, `sema-engine`, and the
   `CriomOS-test-cluster` nspawn witness.
3. Spirit runtime/CLI/contract path: `persona-spirit`,
   `signal-persona-spirit`, and owner-signal Spirit if present.
4. Repo-wide schema consumption: concept `.schema` files and whether any
   component consumes them beyond validation/architecture markers.

The synthesis checks production code paths separately from tests and mockups.
