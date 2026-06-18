# 416 — Operator catch-up: signal-standard and router fan-out

Read:

- `reports/designer/681-signal-standard/1-design.md`
- `reports/designer/681-signal-standard/2-report.md`
- `reports/system-designer/134-universal-component-differentiator-contract-design-2026-06-18.md`
- Spirit `eeeo` — `signal-standard` as the shared cross-component vocabulary library.
- Spirit `l2ha` — Fork A: criome stamps, router matches subscriptions and fans out references.

## Current shape

Designer 681 turns the universal differentiator from a local criome concept into a shared `signal-standard` library:

- `signal-frame` stays the domain-free wire mechanics library.
- `signal-standard` becomes the domain-free cross-component vocabulary library.
- Component signal contracts import both and keep only their component-specific signal tree.

The first `signal-standard` vocabulary is:

- `ComponentKind`
- `AuthorizedObjectKind`
- `Differentiator`
- `ComponentObjectInterest`
- `AuthorizedObjectInterest`
- `AuthorizedObjectReference`
- `ComponentClassification`

The reconciled `ComponentKind` roster is:

```text
Spirit Mind Criome Message Router Mirror Terminal Harness Agent System Introspect Orchestrate Lojix Persona
```

`Persona` is explicitly an aggregate/principal, not a daemon.

## How this connects to the operator landing

The operator landing in report 415 already implemented the local criome half:

- `signal-criome` now has `AuthorizedObjectUpdateToken { subscriber, interest }`.
- `criome` now stores tokens directly, matches `token.interest`, and retracts per `(subscriber, interest)`.

That remains the right mechanism. Designer 681 now says the *types* in that mechanism should move out of `signal-criome` into `signal-standard`, so router and other components can use the same vocabulary without importing criome's local contract.

The clean follow-on is therefore:

1. Create `signal-standard`.
2. Move the shared differentiator and interest types there.
3. Update `signal-criome` to import them.
4. Update `criome` to build against the imported generated types.
5. Update `signal-persona` to import `ComponentKind` and delete `ComponentPrincipal`.
6. Audit and migrate `signal-message::ComponentName`, because it is another closed component roster.
7. Then implement router `Attend` / `Retract` and a durable attendance table keyed by the standard interest coordinate.

## One discrepancy to keep visible

Designer 681 says current evidence shows only `signal-criome` and `signal-persona` declare local `ComponentKind`. That is narrowly true by type name, but System-Designer 134 correctly called out a third roster:

```text
signal-message/schema/lib.schema:
  ComponentName [Mind Message Router Terminal Harness System Introspect Orchestrate Spirit]
```

This is not named `ComponentKind`, but it is a closed component roster and participates in the same conflict. It should not be ignored during migration.

My lean: `signal-message::ComponentName` should either collapse to imported `ComponentKind`, or be renamed/reframed only if it truly means a message-lane endpoint name rather than a component kind. Right now it looks like the same component axis.

## Implementation notes

Build against the schema form on `schema-next` main at landing time. Designer's canonical sketch uses the newer positional/dot form, but the validated variant uses the current name-value struct-field form. The implementation should use the buildable mainline form, not block on the structural-forms branch.

This is a breaking coordinated rebuild by design. Old local enum ordinals should not be preserved as a goal.

## Questions

1. Should `signal-message::ComponentName` collapse into imported `ComponentKind` now?
2. Should `signal-standard` include `ComponentClassification` immediately even if no first consumer uses it yet?
3. Should router attendance be only local router state, or does attendance itself eventually become an authorized criome object? Current design says local router state first.
