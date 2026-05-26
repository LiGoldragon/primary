# Code Context

## Files Retrieved

1. `/home/li/primary/reports/nota-designer/5-bracket-string-migration-2026-05-23/5-overview.md` (lines 1-113) - downstream bracket-string migration status, Nix evidence, blockers, and bead state.
2. `/home/li/primary/reports/nota-designer/6-quoted-string-purge-audit-2026-05-24.md` (lines 1-71) - latest quoted-string purge result, fixed teaching surfaces, tests, and remaining exceptions.
3. `/home/li/primary/reports/nota-designer/7-notation-cutover-database-handover.md` (lines 1-90) - NOTA notation hard-cutover/database handover interpretation for Spirit.
4. `/home/li/primary/reports/nota-designer/8-nota-schema-lowering-deviation-audit.md` (lines 1-324) - core schema/NOTA lowering audit and proposed reusable lowering architecture.
5. `/home/li/primary/reports/nota-designer/9-operator-intent-capture-audit-schema-nota-shape-logic.md` (lines 1-130) - latest nota-designer audit of operator intent capture and implementation alignment.

## Key Code

The latest schema-specific design report is `/home/li/primary/reports/nota-designer/8-nota-schema-lowering-deviation-audit.md`.
It says the `schema` crate is close to intent, but schema handling is split: `schema` is the correct typed substrate, while `signal-frame/macros/src/schema_reader.rs` still carries a private schema reader with compatibility grammar that contradicts current NOTA/schema intent (lines 7-20, 53-80).

Current schema intent baseline from report 8:

- `.schema` files are six fixed positional fields: imports, ordinary header, owner header, sema header, namespace, features (lines 32-35).
- Headers use uniform v13 `(Root [SubVariant ...])`; scalar `(Root Payload)` is retired (lines 36-38).
- Authored schemas lower into `AssembledSchema` for short-header generation, code emission, storage descriptors, and version projection (lines 39-41).
- Builtin macro-schema variants at node-definition points are data-carrying variants; each needs a payload struct defining that macro variant's input object (lines 46-49).

The reusable lowering shape in report 8 is:

```rust
pub enum NodeDefinition {
    ImportDirective(ImportDirectiveInput),
    HeaderRoot(HeaderRootInput),
    NamespaceEntry(NamespaceEntryInput),
    TypeDefinition(TypeDefinitionInput),
    Feature(FeatureInput),
}

pub trait BuiltinLowerer {
    type Input;
    fn lower(
        &self,
        context: &mut LoweringContext,
        input: Self::Input,
    ) -> Result<()>;
}
```

Those snippets are from lines 195-219. The key point is that field names are Rust lowering roles, not final NOTA labels; final NOTA value encoding remains positional (lines 84-106, 204-205, 250-252).

Report 8's first-change list for implementation is the most actionable sequence: add component identity and canonical UIDs; add named input structs for builtin nodes while keeping positional NOTA; move engine metadata into `AssembledSchema`; move layout planning from `Document` to `AssembledSchema`; replace `signal-frame-macros/src/schema_reader.rs` with an adapter over `schema::LoadedSchema::read_path(...).assembled()`; add rejection tests for old forms; add schema repo self-schema once the builtin input model settles (lines 303-316).

The latest intent-capture audit is `/home/li/primary/reports/nota-designer/9-operator-intent-capture-audit-schema-nota-shape-logic.md`.
It says records `588` and `589` correctly captured the durable intent: schema macro dispatch should use a reusable NOTA object layer, and macro passes may parse text into generic NOTA values then pass subobjects through later macro passes (lines 20-32).
Records `590` and `591` add concrete delimiter/arity predicates and the report discipline that implementation, tests, design intent, and uncertainty must be separated (lines 34-45).

Report 9 also says not to over-capture: the upgrade-macro line was a request to report current reality, not a new schema-design decision, and the implementation/test/report ending was a work instruction rather than durable Spirit intent (lines 47-72).

The key implementation boundary from report 9: `nota-codec::NotaValue` is the reusable NOTA shape-inspection layer; the schema macro engine is the next layer that consumes shape predicates and lowers typed macro variants into `AssembledSchema` (lines 83-99, 101-130).

Bracket-string / notation context:

- Report 5 says downstream bracket-string migration started after core `nota-codec` and `nota` branches landed on `main`; landed slices had Nix evidence, while remaining pieces were blocked by larger signal-stack migrations or active Persona/signal rename locks (lines 5-12, 25-51, 65-113).
- Report 6 says current teaching surfaces were purged of quote-delimited NOTA strings except explicit legacy/deployed compatibility surfaces and blocked migration surfaces (lines 5-29, 40-60).
- Report 7 says changing canonical NOTA string notation to bracket strings should not break the Spirit database by itself because the DB stores typed rkyv records, not raw NOTA text; the unsafe path is mixing old and new parsers against one live CLI/daemon without an explicit runtime switch (lines 5-20, 80-90).

## Architecture

The intended stack is:

1. `nota-codec` parses authored NOTA into a reusable structural value layer when macro dispatch needs shape inspection.
2. `schema` owns the schema language, builtin macro input structs, lowerer registry, lowering context, and `AssembledSchema` builder.
3. `AssembledSchema` becomes the canonical resolved object with imports, component identity, UIDs, routes, engine annotations, features, layout, and upgrade hints.
4. `signal-frame-macros` and other consumers become adapters over `AssembledSchema`; they should not parse or define schema semantics themselves.

Implication: pi-operator should avoid treating a generic `NotaValue` parser as the schema engine. It is the delimiter/shape substrate. The schema crate still needs macro-pass orchestration, builtin registry, node-definition-point dispatch, fixed-point macro application, and lowering into `AssembledSchema`.

The real-vs-design line matters. Report 9 says schema already has real `BuiltinMacroVariant`, `NodeDefinitionPoint`, `LoweringContext`, route lowering, engine propagation, and upgrade planning. It says the still-not-real part is macro code generation from schema diffs into `VersionProjection` and storage descriptors (lines 114-119). Future pi-operator reports should preserve that split.

Primary jj state inspected headlessly:

- `/home/li/primary` working copy is workspace `default` at `@` change `lxuwnvpn` / commit `e302937f`, no description set.
- Parent is `tzlwqsyk` / `c39d9a98`, description `report operator/198: verify nota structural prototype`.
- Parent below that is `main` at `wmlvvqvy` / `3999552f`, description `skills/jj.md: at-a-glance cheat sheet at top + note structural fix landed in source`.
- `main`, `main@git`, and `main@origin` all point at `wmlvvqvy` / `3999552f`.
- Before this report was written, Primary status already had `A reports/pi-operator/6-recent-intent-reports-branch-read-2026-05-26/0-frame-and-method.md`. This report adds the `4-nota-designer-reports-and-branch.md` file in the same uncommitted working-copy change.
- Path history shows reports 6, 7, 8, and 9 are already ancestors of `main`: report 9 was added by `lxzxwptw` / `a2de6272` (`nota-designer: audit schema shape intent capture`); report 8 by `wxxyxwvl` / `cffa1ab4` (`designer: 2026-05-25 session — /330 through /336 + AGENTS.md hard overrides + human-interaction skill`); report 7 by `yzkwymtn` / `3510b5cc`; report 6 by `nrttrvqm` / `25adf4b4`.
- I found no active Primary bookmark named for `nota-designer`; the nota-designer reports are not sitting on a separate Primary feature bookmark that pi-operator needs to integrate.

Adjacent source checkout observations, only because report 9 names them:

- `/git/github.com/LiGoldragon/nota-codec` currently has `@` on bookmark `nota-codec-intent-synthesis` at `qklotqmr` / `7b0896e9`, parent `main` at `rsltovoy` / `f761421c`, with `A INTENT.md` in the working copy.
- `/git/github.com/LiGoldragon/schema` currently has `@` on bookmarks `designer-schema-derived-nota-2026-05-26` and `designer-schema-schema-prototype-2026-05-26` at `qmvkpqqz` / `0e04c22f`, with dirty prototype block-parser files under `prototype/`.
- `/git/github.com/LiGoldragon/signal-frame` is clean at an empty `@` over `main` `rtwnntwm` / `d61ebf25`.

## Start Here

Start with `/home/li/primary/reports/nota-designer/9-operator-intent-capture-audit-schema-nota-shape-logic.md` because it is the latest nota-designer report and directly tells pi-operator which intent captures are valid, which non-captures are correct, and where the `nota-codec::NotaValue` boundary sits.
Then open `/home/li/primary/reports/nota-designer/8-nota-schema-lowering-deviation-audit.md` for the implementation sequence and the `schema` vs `signal-frame-macros` ownership boundary.
