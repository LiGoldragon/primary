# 175 — Schema engine prep: frame and method

## Frame

The slice started from the expanded Spirit/schema MVP direction:

- use the strongest current reading of designer `/326-v13` plus operator schema critique reports;
- place a concept `.schema` file in every reachable component and library repo, starting at version `0.1`;
- treat the files as boilerplate for later schema-derived code generation, not as fully authoritative contracts yet;
- prove the Spirit database migration path against a sandbox copy of the live database only;
- run validation through Nix.

The late-session schema-lowering clarification added one conceptual piece: reusable schema lowering should be built from macro-variant components in the schema builtin engine. Builtin variants appear at `NodeDefinition` points, and each variant is data-carrying: its payload is the input struct for that macro lowerer.

## Inputs

- `reports/designer/327-schema-engine-upgrade-marking-sweep/0-frame-and-method.md`
- `reports/designer/326-v13-spirit-complete-schema-vision.md`
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md`
- `reports/designer/322-spirit-mvp-positional-schema-worked-example.md`
- `reports/operator/170-schema-spirit-mvp-implementation-2026-05-24.md`
- `reports/operator/174-v5-schema-import-header-design-critique-2026-05-24.md`
- Spirit records `496` through `499` and `507`.

## Subagent Method

The work used exploratory subagents because the psyche asked for subagent-assisted prep across many repositories. Each subagent received a bounded inventory question and the `jj` inline-message rule.

- Core persona triads: inspect Spirit, Mind, Router, Message, Orchestrate.
- Adjacent persona components: inspect Terminal, Harness, Introspect, System, Persona Pi, repository-ledger.
- Engine and upgrade stack: inspect Persona, owner/ordinary persona signals, origin, upgrade, sema-engine, version-projection.
- Library/domain stack: inspect signal-frame, signal-derive, signal-sema, nota crates, forge, Criome, Lojix, horizon.

The main operator then generated the concept schemas, added the Nix-visible validation and sandbox migration tools, ran the checks, and pushed or staged the repo changes according to each repository's current branch state.

