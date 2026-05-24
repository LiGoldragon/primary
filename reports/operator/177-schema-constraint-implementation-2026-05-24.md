# 177 — Schema Constraint Implementation Slice

## Scope

This slice converted the gaps from `reports/operator/176-schema-macro-upgrade-integration-audit/`
into code-backed constraints where the current repositories were ready.

The implemented target was not a full automatic schema-diff code generator. The target was the
next concrete step toward that design:

- the schema crate now has a real `UpgradeRule` builtin macro variant and a Nix constraint that
  lowers through the macro engine;
- persona-spirit now validates the schema-derived `ShortHeader` on the production ordinary ingress
  path, not only in isolated contract tests;
- the upgrade crate now migrates Spirit v0.1.0 stored entries through the contract-owned
  `VersionProjection` instead of duplicating certainty-to-magnitude conversion locally;
- the affected contract tests are exposed as named Nix checks.

## Code Landed

`schema` commit `be6860fb` — `schema: lower upgrade rules through builtin macro variant`

- Added `NodeDefinitionPoint::UpgradeRule`.
- Added `BuiltinMacroVariant::UpgradeRule(UpgradeRuleInput)`.
- Added `UpgradeRuleMacro`, lowering `UpgradeRuleInput` into
  `AssembledFragment::Feature(Feature::Upgrade(...))`.
- Added the named Nix check `test-upgrade-rule-macro-variant`.

`signal-persona-spirit` commit `c1971577` — `signal-persona-spirit: expose schema constraint checks`

- Added named Nix checks for:
  - `test-short-header-dispatch`;
  - `test-box-form`;
  - `test-version-projection`.

`persona-spirit` commit `f2c1538a` — `persona-spirit: validate short headers on ingress`

- Ordinary client frame emission now uses `request.into_frame(exchange)` so frames carry the
  generated schema-derived `ShortHeader`.
- Ordinary daemon frame receive now calls the generated
  `WorkingOperation::kind_from_short_header(short_header)` before dispatch.
- The daemon rejects a mismatched header before mutating the store.
- Added the named Nix check `test-short-header-ingress-triage`.

`upgrade` commit `57a2375c` — `upgrade: use Spirit contract projection in migration`

- Spirit v0.1.0-to-v0.1.1 migration now converts historical stored records through
  `signal_persona_spirit::migration::V010ToV011`.
- Removed the migration-local certainty-to-magnitude mapping from the storage migration.
- Added the named Nix check `test-spirit-migration-uses-contract-projection`.

## Nix Constraints Run

All checks were run through Nix with `--option max-jobs 0`.

- `schema`: `.#checks.x86_64-linux.test-upgrade-rule-macro-variant`
- `signal-persona-spirit`: `.#checks.x86_64-linux.test-short-header-dispatch`
- `signal-persona-spirit`: `.#checks.x86_64-linux.test-box-form`
- `signal-persona-spirit`: `.#checks.x86_64-linux.test-version-projection`
- `persona-spirit`: `.#checks.x86_64-linux.test-short-header-ingress-triage`
- `upgrade`: `.#checks.x86_64-linux.test-spirit-migration-uses-contract-projection`

The persona-spirit check is the important placement witness: it sends a malformed frame through the
daemon socket and verifies the record store remains empty. That proves the `ShortHeader` logic is
on the production receive path.

The upgrade check is the important authority witness: it migrates historical records and proves the
current `Magnitude` values are produced through the signal contract projection, not a parallel
storage-only conversion.

## Still Not Done

The remaining major gap is automatic schema-diff emission of the projection implementation itself.
Today `signal-persona-spirit` owns the projection and `upgrade` consumes it. That is materially
better than duplicate conversion logic, but the projection is still contract-authored Rust rather
than generated from an assembled schema diff.

The next slice should make the schema macro consume the v0.1.0 and v0.1.1 schema declarations and
emit the `VersionProjection` impl that `upgrade` is already prepared to use.

