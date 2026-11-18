# Proposal 2 — exact three packages materialized

Core px6a granted the sole phase in `package-phase.md`; rnqk authorized the resolved Bash provider after the nonexistent `/bin/bash` failed before the controller entered. The first absent-exec attempt started no workload. The approved workload then ran once, unchanged, with Bash `/nix/store/lfm00fnq66xfgbn099vqckabyl5jllz6-bash-interactive-5.3p20/bin/bash`.

**EXIT0, 18 November 2026 21:57:13–21:57:27 UTC. Exactly three EVAL, three BUILD and three DOWNLOAD records, all successful, no extra attribute or retry.** This was package materialization, not a repeated whole gate. Source remained exact published fe5a6930871707a7086c9a647867a519734220ef; base7fca4d583adfd2354903c59cbc7f5e928e1baa76, Curriculum60609c55f90432782625275294636a4e396d9497, translator6892a15b11653a2ef8932a4390b34f5e81583744.

## Exact immutable outputs

| Attribute | Locally materialized output | NAR hash |
|---|---|---|
| default | `/nix/store/76vvsfvdifhplj44d3sp6crc704wkg11-flow-workspace-0.60.1` | `sha256-66cfO36+DUVmBZw5MRU49UNFAA0DAiaOSoqATT1ek/s=` |
| curriculum | `/nix/store/ligz6rqy9dm584m1z0dbzpjzqqvycszz-rust_curriculum-0.2.0` | `sha256-VW79AeNk0OhkqA8IU7YuHzrPo1gdFi+7EoVqxlfi5tE=` |
| nexus-configure | `/nix/store/8b2q16kdixa8qawmci4474hdxm6zpnf7-rust_translator-0.6.0-bin` | `sha256-K0jA+ZN8U3mai0cig/xLGPeS5/G6xz6sJLjkt+FCwsk=` |

Derivations respectively: sysdjwm7jlcpmqnzzvgvxlkk6pgxazcn-flow-workspace-0.60.1.drv,486ad4hm9slxrszvn2zqfxbzd63ipgp3-rust_curriculum-0.2.0.drv,c2yi2nzmg882f909bhx8mlqj9q6bix25-rust_translator-0.6.0-bin.drv, all under `/nix/store/`.

Every required executable exists locally, is a regular executable file, and has retained size/mode/resolved path/SHA256 in `local-artifacts.json`. No package executable was run, including no version flag that might contact a daemon or initialize a native process. Binary version provenance is the exact package derivation/manifest, not a self-report. Remote read-only derivation records bind Curriculum0.2.0 and Translator0.6.0; Flow package is0.60.1. The default package's daemon SHA256 is `e0cfb2c6a08241e7d755cd69d08dc06d8d555493785e05439a9fffb8c4f7ea49`, exactly the accepted whole-gate daemon hash.

## Evidence and cleanup

Full evidence: `/tmp/flow-packages-1bd07a.Z1wvMCTK/`, pointer `/tmp/flow-packages-1bd07a.path`. It contains exact run.sh/argv, published source pin/flake.lock, Bash provider/hash, result.json, packages.log, terminal code/start/end, local provider hashes/NAR/deriver metadata, remote read-only derivation records and version-source-evidence.json. Local derivation files were not downloaded, so local derivation introspection refused; one remote metadata read supplied the records, without evaluation/build or a second workload.

Owned local timeout PID/PGID1347632 exited and its exact group is absent (`local-after.txt`, `local-group-final.txt`). Bounded remote before/after/fresh process snapshots show zero nixbld or live NFB/evaluator workloads; only the snapshot command/awk appear. NFB's recorded exact remote scratch `/tmp/tmp.rOqcq9nQhS` is absent (`remote-final.txt`). NFB's own removal command is in packages.log. All logs/results remain retained. Core's release decision is pending; no attributable running workload remains observed.

## Scope and next boundary

This closes the concrete package-output/local-presence gap, subject to Core acceptance. Independent whole-gate source provenance and its separately accepted stamp limit remain as recorded; no diagnostic was relabelled. Driver assembly still needs its complete lifecycle/matrix, one coherent manifest/provider binding, unrun fixtures admitted/executed separately, independent final artifact review and Field native admission. No credential was read/linked, no private service or native flow started, no live configuration/deployment changed, no main/tag/pin changed. These outputs are evidence, not native authorization.
