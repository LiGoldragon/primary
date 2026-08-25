# Curriculum Datom cutover

## Authoritative revisions

Method: probe `jj --repository "$RepositoryRoot/github.com/LiGoldragon/Curriculum" log -r 'main | main@origin' --no-graph`.

Observation: Curriculum `main` and `main@origin` resolve to `ccd1e9f00a9a3fcb8e03dd0f29c6eca2864a035b`, whose parent is the data-root cutover `f06e26b8456731920c2e4770a15b332c901e6d9c`.

Method: code read `flake.nix`.

Observation: Primary pins Curriculum at `ccd1e9f00a9a3fcb8e03dd0f29c6eca2864a035b` and `curriculum-deploy` at `ef35a6dc00c6df13df4f2067ab34e5f1cfc6bc08`; the runtime follows that Curriculum input and receives exactly one inline `CurriculumRequest` Datom object.

Method: probe `jj --repository "$RepositoryRoot/github.com/LiGoldragon/datom" log -r 'main | main@origin' --no-graph`.

Observation: Datom `main` and `main@origin` resolve to `d47419ef872ab76bfbd6bb4b3e84b62a883a8d31`.

## Stale workspace correction

Method: probe `jj --repository "$RepositoryRoot/github.com/LiGoldragon/Curriculum" status` before selecting `main`.

Observation: the physical Curriculum working copy was based on legacy commit `e75205421ad6`, which still contained the old generator and DOTOS manifests. It was not the `main` or `main@origin` tree.

Method: probe `curriculum-deploy/target/debug/curriculum-deploy 'CurriculumRequest.{Visualize.{<legacy-data-root> <temporary-workspace>}}'`.

Observation: the legacy tree failed with `read .../roles.datom: No such file or directory`.

Method: probe `jj --repository "$RepositoryRoot/github.com/LiGoldragon/Curriculum" new main`.

Observation: the physical checkout was moved to the authoritative data-only tree. No authored curriculum source was changed in this flow.

## Active-root contract

Method: probe `curriculum-deploy/target/debug/curriculum-deploy 'CurriculumRequest.{Generate.{$RepositoryRoot/github.com/LiGoldragon/Curriculum <temporary-workspace>}}'` followed by the corresponding `Check` request.

Observation: generation printed `Generated.{35 27}` and checking printed `Checked.{35 27}`. The temporary consumer held 35 `.agents` skills, 35 Claude skills, 27 role packets, and `skills/generated-role-outputs.datom` beginning with `GeneratedRoleOutputs.{[`.

## Declarative consumer proof

Method: probe `nix eval --raw .#checks.x86_64-linux.generated-skills-current.drvPath` from Primary with a clean tree.

Observation: evaluation produced `/nix/store/l0sws4bnyw46r0l3bl24kxy4a5sp2m8q-primary-generated-skills-current.drv`.

Method: probe `nix build .#checks.x86_64-linux.generated-skills-current --print-build-logs` from Primary.

Observation: the derivation built on `ssh-ng://nix-ssh@prometheus.goldragon.criome`, printed `Checked.{35 27}` and returned `/nix/store/xf5p2kpff8svswp237fskjvj1lgrlbqb-primary-generated-skills-current`.

## Legacy-absence inspection

Method: probe `jj --repository "$RepositoryRoot/github.com/LiGoldragon/Curriculum" file list -r main`.

Observation: the authoritative tree has `roles.datom`, repository documentation, and `skills/*.md`. It has no tracked `Cargo.toml`, `flake.nix`, `manifests/`, `skills-*.dotos`, `src/`, or `tests/` paths.

Method: code read Primary `flake.nix` and probe generated consumer output.

Observation: active generation uses the external runtime plus the one typed Datom request. Direct Primary inputs named Dotos are not consumed by that curriculum request; generated skill mentions of DOTOS describe unrelated components or legacy terminology, not curriculum configuration.
