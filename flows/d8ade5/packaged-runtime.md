# Approved packaged producer — d8ade5

Answers core Order8h5x with the larh/lz7d minimal-delta clarification. Producer remains published immutable `60609c55f90432782625275294636a4e396d9497`; ordinary contract remains `8e63176cb1c0f1429a9797412391b4035a25cc68`. No producer descendant, packaging/source/contract/dependency/manifest edit, Home pin change, main promotion or live switch was needed or performed. Standalone plain exports and shared-configurator separation remain under primary-q8li.

## Intended selector, established immutably

Accepted Home `0b3d6dfaf29cd6d67e4c92a715c972d071b12f07` and `0602dd17738bddd2e3a72c95a8d8eeb662f5a8b2` have the identical `packages/curriculum-resolver-deployment/default.nix` Git blob `8c29b35d03a07e7ca2cc2c38759d2e0fcd58b91a`. Its lines4–11 obtain the selected Curriculum's own `inputs.base.lib.contexts.${system}`, import that source's `Cargo.nix` with the context's package set, crate builder and overrides, and set `rootFeatures = [ "default" "datom" ]`; `runtime` is `rootCrate.build`. The service module selects `deployment.runtime` for `ExecStart`, the drop-in does likewise, and the CLI wrapper executes the same runtime's CLI. Exact selector and unit source blobs are retained in the evidence directory below.

Flow owner Resultioyp confirms intended ujg2 Home retains this exact selector with a future60609 source pin and future accepted typed Flow pin. There is no immutable ujg2 Home candidate yet. Immutable0602 itself still pins Curriculum `8881cc11ef4e328d97aa6ab6d281614da8dc0eea`; this report does not claim it pins60609. The resident Primary/Home checkout inspected earlier is stale and was not used as the selector authority.

The proof imports the exact accepted selector blob, supplying immutable60609 as `inputs.curriculum-source`. Its own locked build-base is `4ea69d1fc87c95e7c1f54d02b21166ffb3285edd`. This is the intended Home selector applied to the proposed source pin in isolation, not an evaluation or gate of a nonexistent final Home candidate. Flow's separate `packages.curriculum` export and producer check artifacts were not selected or executed.

## Exact runtime and hashes

Builder: `prometheus.goldragon.criome`. Runtime build exit0.

Runtime output: `/nix/store/hzny5wk4acw2g06rjd6hr6b4zhbaw7b8-rust_curriculum-0.2.0`.
Derivation: `/nix/store/vm6zcqba3gs8yym07vvmm4lp676l3hs4-rust_curriculum-0.2.0.drv`.
Output NAR hash: `sha256-VW79AeNk0OhkqA8IU7YuHzrPo1gdFi+7EoVqxlfi5tE=`.
`bin/curriculum` SHA-256: `a0febe6abcdb2fe6c3d92a92da5854f2e51915e2bc8b172d1af42c063e57eee1`.
`bin/curriculum-nexus` SHA-256: `35d9fef8cdfa570c26ae85519c4f9e1794a44d26a39c65bb00a8cb3a71daf4d1`.

Both binaries were executed directly from that store output on the builder through scratch symlinks. These hashes differ from the prior datom check binaries; the runtime output above is the new evidence boundary.

## Immutable gate and packaged fixture

The complete producer `checks.x86_64-linux` gate was rerun using nix-fast-build remote/no-download against `github:LiGoldragon/Curriculum?rev=60609c55f90432782625275294636a4e396d9497`, exit0: curriculum, cargo-nix, crate-features, crate-versions and default all pass. No local compilation or source evaluation was used. This is the complete producer gate, not a final Home or Flow gate.

The approved e2487d fixture was rerun in isolated runtime/state/source directories with a no-effect refresh program and no roles file. Inotify socket creation announces readiness. A socket relay records the unmodified CLI request and service response frames and archives. The service has exited. Source bundles preserve the exact clean fixture heads: Psyche `74279bd7868e77ca2ba0f1cf886ffeef31d62ea5`; Mind and Field `0412944e349e07c78e58926b8f198679020106cf`.

`Modules` and `ModulesVerbose` both succeed and list exactly the four declared files: energy Single0, binding Span0–1, binding Single1 and core Single0; verbose descriptions are empty for these unframed fixtures. Exact declarations and listing archives are retained. The missing-module composition refuses with CLI exit1 and exact reason `missing module intent:absent:0`; valid startup and the two numeric/span compositions succeed.

For all four original scenarios, the packaged runtime's request archives, answer archives, query datoms, CLI stdout/stderr and exits are byte-identical to the frozen e2487d oracle. All twelve request/response frame lengths and payloads were independently checked. This retains exact actual revision/path/body/rendered hashes and placement indices, not only a successful CLI exit. Binding Single1 produces singleton1 followed by its containing Span0–1; direct Span0–1 selection retains that actual span. Intent energy0 is explicitly co-selected in both binding queries, not evidence of dependency expansion.

## Evidence custody and remaining boundary

Local evidence: `/tmp/curriculum-packaged-d8ade5.ET6F1l/`. `runtime.nix` and `home-selector.nix` reproduce the selector; `producer-flake-metadata.json`, `runtime.drv.json`, `runtime-path-info.json`, `runtime-evidence.txt`, `runtime-build.{json,log,exit}` establish inputs/output/hashes. `producer-gate.{log,exit}` is the complete gate receipt. `fixture-run.{log,exit}`, `verification.txt`, `source-status.txt`, `declarations/` and `captures/` retain fixture execution and exact wire/oracle evidence. Source bundles remain at `/tmp/producer60609-e2487d.a0vRMA/` and in the builder fixture directory.

Builder evidence and fixture: `/tmp/curriculum-packaged-d8ade5/`; its `bin/` symlinks name the exact store runtime above. The four main and binding `.rkyv` pairs plus the new listing pairs, their `.frame`/`.query.datom`/`.stdout`/`.stderr`/`.exit`, `archives.json` and `revisions.json` are also copied into local `captures/`.

This closes the intended packaged-producer fixture boundary without changing packaging. Final typed Flow gate, final authored manifest/source-main evidence, final immutable Home cohort/pin gate, combined review and Psyche authorization remain with their owners. The final Home cohort must select the same artifact or re-establish this boundary if its source/base/selector changes.
