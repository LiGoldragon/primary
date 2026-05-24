# 175.5 — Overview

## What Landed

This slice produced three concrete outcomes:

- `73` concept `.schema` files across reachable LiGoldragon repos, all starting at version `0.1`.
- Upgrade repo tooling for concept-schema validation and Spirit sandbox migration.
- A reusable `NodeDefinition` macro-component design for lowering authored schema forms into `AssembledSchema`.

## What It Accomplishes

The workspace now has a repo-wide marker layer for the schema engine. It is not yet schema-generated Rust, but it gives the next pass concrete files to read, validate, and evolve.

The Spirit migration witness is stronger than a unit test. It copied the live `v0.1.0` database, migrated the copy, and proved every migrated record readable through the current shape:

```text
(SandboxUpgradeSucceeded 500 500 ...)
```

The schema checker gives the first Nix-visible guardrail:

- six top-level sections;
- version `0.1`;
- no comments;
- no quote-delimited strings;
- uniform `(Root [SubVariant...])` header roots.

## What Is Still Not Done

The concept files are not yet consumed by a real schema engine. The next implementation step is the schema crate itself:

- parse `.schema` into `NodeForm`;
- dispatch by `NodeDefinitionPoint`;
- lower through registered builtin macro variants;
- assemble `AssembledSchema`;
- derive headers, signal types, projection traits, and upgrade diff logic.

The `schema` repo should be the center of that work. It was not given a placeholder concept file in this pass because the next meaningful change there is the actual engine, not another marker file.

## Open Questions

The main question is naming and module placement, not mechanics:

Should the extension point be named `NodeDefinitionPoint`, `SchemaNodePoint`, or something closer to the psyche's wording, `nodeDefinition`? The mechanics are clear: point-specific macro variants with typed input structs lower to assembled fragments.

Second question: should import macros be the only effectful builtins, with all other builtin lowerers pure? Operator lean: yes. That keeps the engine testable and makes imports the explicit dependency boundary.

