# Curriculum deploy realization

## Result

The runtime/data separation is public, breaking, and deployed across the only witnessed consumer.

- `curriculum-deploy` owns the Rust generator/checker/visualizer and engine-only Nix package.
- Curriculum is external data: 35 present skill sources plus one typed `roles.datom`.
- Datom 0.2.0 exposes public schema-driven realization/textualization for consumer-defined types.
- Primary independently pins the runtime and Curriculum data, then supplies exactly one complete inline Datom request.

No compatibility reader or combined-source package remains. Runtime configuration has no DOTOS, `SKILLS_*` environment variables, working-directory default, request-file multiplexing, or separate CLI flag. The typed root carries the operation, external data root, workspace root, and generation mode.

The old activation/index manifests are gone. Skill presence determines the 35 skills. Role configuration and instructional modules live in `roles.datom`; the common role preamble formerly hardcoded in Rust is data there as well. Consumer cleanup inventory is Datom.

The living's approved prompt-crafting rule was added to the authored source only after cross-repository generation passed:

> A prompt explains nothing the harness does automatically and nothing everybody knows; it carries only what the receiving flow would not otherwise have.

## Published revisions

- Datom 0.2.0: `d47419ef872ab76bfbd6bb4b3e84b62a883a8d31`
- curriculum-deploy: `ef35a6dc00c6df13df4f2067ab34e5f1cfc6bc08`
- Curriculum data: `f06e26b8456731920c2e4770a15b332c901e6d9c`
- Primary consumer: `339b22a814192f45b17d1ca3bc9adbdc56d2377e`

## Proof

Datom's Cargo and nine remote Nix gates passed. Runtime Cargo, strict Clippy, tests, public external-data integration, and remote Nix gates passed. Primary generated and checked all managed surfaces through the final public pair, then passed its remote Nix check.

The Rust package derivation path remained identical when only the Curriculum revision changed. Curriculum data therefore no longer invalidates or recompiles the runtime.

Only Primary was enumerable as a checked-out consumer. Uncloned external consumers were not claimed migrated; the breaking deployment path is recorded in repository `UPGRADES.md` files.

## Sources

- `flows/01a035d3/witnesses/curriculumDeployCutover.md`
- `flows/01a035d3/vision/rustCodeFromTheData.md`
- `flows/01a035d3/vision/promptExplainsNothingTheHarnessDoesAutomatically.md`
- `/git/github.com/LiGoldragon/datom/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/curriculum-deploy/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/curriculum-deploy/UPGRADES.md`
- `/git/github.com/LiGoldragon/Curriculum/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/Curriculum/UPGRADES.md`
- `/home/li/primary/flake.nix`
- `https://github.com/LiGoldragon/datom/commit/d47419ef872ab76bfbd6bb4b3e84b62a883a8d31`
- `https://github.com/LiGoldragon/curriculum-deploy/commit/ef35a6dc00c6df13df4f2067ab34e5f1cfc6bc08`
- `https://github.com/LiGoldragon/Curriculum/commit/f06e26b8456731920c2e4770a15b332c901e6d9c`
