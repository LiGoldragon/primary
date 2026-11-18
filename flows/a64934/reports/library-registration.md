# Harness library registration packet — Core d4wi

Owner of this source: Mind harnessNexus Sol, flow a64934. Source reservation: Orchestrate lock 392 over the five new Harness repositories; report reservation 393. Canonical clones and main branches are used, no runtime deployment.

## Exact library

Repository: /git/github.com/LiGoldragon/harness-nexus-library, origin/main, 3613d63d0994de7841bcf6f070c83bebb0ddfa5a, package version 0.1.0. This supersedes aa867386ca79e6b0d4e0a979fa4239e9d6637830 for registration. The latter's only defect was the generation-check source basename; the crate's source did not change.

Cargo.toml, Cargo.lock, Cargo.nix and crate-hashes.json are at that repository's root. The dependency alias `flow` names flow-ethos 0.54.3 at 062ef9e14abbf6552b257e9ce7e1c22f5bc00c27, with manifest rev string `062ef9e1`. Flow's current workspace uses 0.56.2; Mind flowNexus Sol explicitly leaves external pin alignment to Core and does not designate that newer workspace version base-compatible.

The library declares `default = []` and `datom = ["dep:datom-codec", "dep:protos", "flow/datom"]`. Its Rust library name is `harness`. Named sets are `plain`, then `datom`, justified by vision:ethos:0, “The datom traits are compiled in only where text is spoken.” Plain enables no datom feature and attaches neither optional dependency; datom attaches datom-codec and protos. The base owner determines the exact normalized closure strings from the consumer below.

## Exact first consumer

Repository: /git/github.com/LiGoldragon/signal-codex-harness-nexus, origin/main, commit 68562da (full revision is available with git rev-parse HEAD), package 0.1.0. Its Cargo.toml, Cargo.lock, Cargo.nix and crate-hashes.json are committed at the root. They were generated on prometheus.goldragon.criome, not locally. Lock registry versions agree with base a5a58fc.

The dependency alias `harness` resolves the library's exact full 3613d63 revision, with default-features=false. The consumer's datom feature forwards harness/datom, flow/datom and signal/datom and attaches its own optional datom-codec and protos. Its Cargo.nix library entry is lines 452–491: `resolvedDefaultFeatures = [ "datom" ]`; the declared datom closure is `[ "dep:datom-codec" "dep:protos" "flow/datom" ]`. Dependency declarations carry both optional edges.

Consumer gate at 68562da is now green (exit 0), all seven attributes including crate-features and crate-versions; log /tmp/harness-a64934.eixDmZ/signal-gate-68562da.log. It ran zero behavioral test cases.

The consumer flake lock selects the base owner's published candidate 032a18e7 over a5a58fc and the published ethos-zero 30.1.0 generator at 415c3703621c528dd1b587725ab8cec1747cf126. No base file was edited by this flow. This proves the library registration candidate against the datom-enabled signal consumer; plain-consumer behavioral tests are next.

## Evidence already green

Library command: `nix run github:Mic92/nix-fast-build -- --remote prometheus.goldragon.criome --no-nom --no-download --eval-workers 1 --flake github:LiGoldragon/harness-nexus-library/3613d63d0994de7841bcf6f070c83bebb0ddfa5a#checks.x86_64-linux`.

Exit 0; all seven attributes green, including generation byte comparison, Cargo.nix proof, dependency sets, formatting and datom-feature compilation/lint. Log: /tmp/harness-a64934.eixDmZ/library-gate-second.log. The first failed check's log is library-gate-aa86738.log beside it. The library gate ran zero behavioral test cases: it proves compilation and source checks, not event-replay behavior, and is not a Codex Nexus release candidate.

## Disconfirming plain-consumer proof

Plain codex-harness-nexus-tests 52457ae53c8a5ce3db4da7f187776f2969519442 fails against 032a18e7 before behavioral tests. Log /tmp/harness-a64934.eixDmZ/tests-gate-first.log: flow-ethos 0.54.3 union enables datom and attaches datom-codec/protos absent from this plain Cargo.nix. This is distinct from the green datom signal consumer. Core 0hqs authorizes the existing base owner a separate narrow configuration fix: matching plain/datom sets for that existing flow-ethos revision, followed by both exact consumer gates on the same corrected immutable base. No workaround enabling datom on the plain test is authorized. The owner has the source and failure; its correction revision is pending.

## Remaining work

Receive the base correction and prove both consumers against it. Then finish generated Memory/runtime/translator anatomy, compile the rollout parser and the separate tests repository, replay the recorded fixtures, gate the full candidate, and obtain Mind harnessNexus Opus audit before Field deployment. Task 3kyf remains open.
