# 175.3 — Implementation and tests

## Concept Schema Files

Generated `73` concept schema files under:

```text
/git/github.com/LiGoldragon/<repo>/schema/<repo>.concept.schema
```

Each file follows the current six-section `.schema` skeleton:

```text
{}
[]
[]
[]
{}
[(Version 0 1) (Status Concept)]
```

Component files fill the three header sections and namespace section with conservative concept roots. Library files use the same structure with library-appropriate roots.

The files intentionally avoid comments and quote-delimited strings. Headers use the uniform root form:

```text
(Root [SubVariant])
(Root [SubVariantOne SubVariantTwo])
```

## Upgrade Tooling

`/git/github.com/LiGoldragon/upgrade` gained two pieces:

- `scripts/check_concept_schemas.py`
- `src/bin/upgrade-spirit-sandbox-test.rs`

The Rust sandbox app copies the source database first, then runs the prototype Spirit `0.1.0` to `0.1.1` migration against the copy. It opens the migrated target through the current Spirit storage shape and reads records back as the current type.

The source database is never opened for mutation by the test.

## Nix Witnesses

The following checks passed:

```text
nix --option max-jobs 0 flake check
nix --option max-jobs 0 run .#check-concept-schemas -- /git/github.com/LiGoldragon
nix --option max-jobs 0 run .#spirit-sandbox-upgrade-test -- /home/li/.local/state/persona-spirit/v0.1.0/persona-spirit.redb
```

The live-copy sandbox migration reported:

```text
(SandboxUpgradeSucceeded 500 500 [.../source-copy.redb] [.../target-v0.1.1.redb])
```

That means the current live `0.1.0` database copy had `500` records migrated and `500` records were readable as the current `0.1.1` shape.

## Repository State

Most schema files were pushed directly to each repo's `main`. A few repos had non-forward `main` state, so their schema concept commits were pushed to dedicated `push-schema-concept-*` bookmarks instead of forcing a sideways `main` move.

The `schema` repo itself was not edited in this pass because it was outside the safe claimed write surface when the broad generation pass ran. It should get the real schema-engine implementation rather than only a concept marker.

