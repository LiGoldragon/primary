# Curriculum Datom cutover

## Result

The authoritative curriculum stack is already migrated from Dotos to Datom. The apparent old stack was a stale physical Jujutsu workspace, not the repository's published main line.

Curriculum `main@origin` is `ccd1e9f00a9a3fcb8e03dd0f29c6eca2864a035b`. Its tree is pure external data: present authored skill files plus `roles.datom`; it has no Rust runtime or activation manifests. Primary pins that revision together with `curriculum-deploy` `ef35a6dc00c6df13df4f2067ab34e5f1cfc6bc08`, whose Datom dependency is the published Datom `d47419ef872ab76bfbd6bb4b3e84b62a883a8d31` line.

The old Dotos/manifests tree seen locally belonged to Curriculum workspace revision `e7520542`, behind the authoritative bookmark. Moving that workspace to `main` exposed the already-published data-only tree; it required no tracked source change.

## Proof

The active stack accepted one inline typed Datom request, discovered the present skill sources, decoded `roles.datom`, and generated and checked 35 skills and 27 roles. The clean Primary evaluation produced `/nix/store/l0sws4bnyw46r0l3bl24kxy4a5sp2m8q-primary-generated-skills-current.drv`; its build on the configured remote builder `prometheus.goldragon.criome` returned `Checked.{35 27}`.

The active curriculum output contains no curriculum-owned Dotos manifest, runtime input, or generated inventory. Primary still declares legacy Dotos-family inputs, but the witnessed curriculum outputs do not consume them; they are outside this migration and were left untouched.

No runtime, data, consumer, version, or upgrade-document edit was warranted in this flow because the breaking cutover and its deployment documentation had already landed in flow `01a035d3`. This flow aligned the stale local checkout with the published state and independently re-proved that state.

## Landing note

Primary commit `64af4bea8ea6` records this flow and also contains the concurrently authored `01a038b8` log because Jujutsu snapshotted both dirty paths. The public commit was not rewritten. Follow-up `1be2820f4ef3` restored that flow's index entry normally.

## Sources

- `flows/01a038b5/witnesses/curriculumDatomCutover.md`
- `flows/01a038b5/vision/curriculumStackToDatomInsteadOfDotos.md`
- `flows/01a035d3/reports/curriculumDeployRealization.md`
- `flows/01a035d3/vision/rustCodeFromTheData.md`
- `Vision/datom.md`
- `/home/li/primary/flake.nix`
- `/git/github.com/LiGoldragon/Curriculum`
- `/git/github.com/LiGoldragon/curriculum-deploy`
- `/git/github.com/LiGoldragon/datom`
