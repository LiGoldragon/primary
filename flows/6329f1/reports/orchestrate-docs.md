# Orchestrate documentation -- flow 6329f1

## What was read

1. `flows/6329f1/log.md` -- the story and the design spec
2. `flows/6329f1/reports/signals-orchestrate.md` -- the signal and orchestrate rewrite report
3. `flows/6329f1/reports/final-witness.md` -- witnessed CLI output at final revs
4. `flows/6329f1/reports/orchestrate-edge.md` -- dirty state, deployed nexus, locks
5. orchestrate origin/ProtoformStack at e631bad92ef2 -- README.md, ARCHITECTURE.md, AGENTS.md, UPGRADES.md, all source files
6. primary orchestrate/AGENTS.md, orchestrate/ARCHITECTURE.md
7. `.claude/skills/orchestrate/SKILL.md` and `SKILL_VARIABLES.md`

## What was written

### orchestrate repo (ProtoformStack branch, then merged to main)

- `README.md` -- rewritten: the Nexus and its sockets, datom CLIs, request/reply shapes with real examples from the final witness, faults as datom on stderr, wire shape, three repositories, store, build/test/deploy.
- `ARCHITECTURE.md` -- rewritten: process boundary, ethos (both signal contracts verbatim), traits-first ontology, state and rules, CLI boundaries with ClientFailure, code map, verification.
- `AGENTS.md` -- rewritten: purpose, local rules, CLI shape with curly-quote rule, ordinary and meta operations, faults, code shape, wire, contract changes, deployment.
- `UPGRADES.md` -- rewritten: 0.26-to-0.27 entry with wire change, datomic API change, ethos source, store compatibility statement, rollout steps. History entries reformatted as X-to-Y transitions.

Committed: `9585484` on ProtoformStack, pushed.

### Merge to main

Fast-forwarded `origin/main` from `dadd537` to `9585484`. Witnessed:
`origin/main` = `origin/ProtoformStack` = `9585484738ce0748d0cf23f0431285f9693ca2ec`.

The ProtoformStack branch is kept as instructed.

### CriomOS-home

Bumped `orchestrate` flake input on main from `e631bad92ef2` to `9585484738ce`.
Committed: `c37cb6132a98` on main, pushed.
Witnessed: `origin/main` = `c37cb6132a98620c97a07310ab0e46ad4e024369`.

### primary orchestrate docs

- `orchestrate/AGENTS.md` -- rewritten: current shape, datom conventions, operations with real examples, faults, no-argument self-description, repositories, deployment.
- `orchestrate/ARCHITECTURE.md` -- rewritten: shape, repositories, code shape, state, datom conventions, faults, contract changes, deployment.

Not committed (main flow commits primary).

### Skill proposal

`flows/6329f1/reports/orchestrate-skill-proposal.md` -- the Lock example needs spaced delimiters and a curly-quote note. Release and Observe lines are correct.

### Superseded draft

The dirty working copy in `/git/github.com/LiGoldragon/orchestrate` (a 2026-08-26 draft) was saved as `flows/6329f1/reports/orchestrate-superseded-draft.patch` before any work.

## Store compatibility

The 0.27 Nexus opens a 0.26 store without migration. Verified by:
- The Sema schema version, table names, table descriptors, and record key shapes are unchanged.
- The persisted rkyv archives of `Configure` and `Lock` use the same positional tuple struct layout.
- The test `released_ids_never_reach_a_later_lock_after_restart` creates a store, stops, and resumes from it.
- No store migration code exists in the 0.27 codebase.

This is test-verified, not deployment-verified: the living's deployed nexus is 0.26.0 and was not touched.

## Sources

- orchestrate origin/ProtoformStack e631bad92ef2 (pre-docs), 9585484 (post-docs)
- orchestrate origin/main dadd537 (pre-merge), 9585484 (post-merge)
- CriomOS-home origin/main f8d5c5d (pre-bump), c37cb61 (post-bump)
- flows/6329f1/reports/final-witness.md (all CLI examples sourced from here)
- flows/6329f1/reports/signals-orchestrate.md (ethos files, code shape)
