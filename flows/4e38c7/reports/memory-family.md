# Memory dependency-family correction — j99e / r2ch

Owner: Mind curriculum Sol, flow 4e38c7; coordinator Mind curriculum Astra. Lock 185 retained. No live switch.

## Accepted candidate

- Repository: https://github.com/LiGoldragon/memory-engine
- Branch: build-base-299aa3
- Immutable revision: 32610884907461dc58c6c143f6f9fec0f13695fc
- Parent: 5683edc56d29fced1946724340c2691567476e06
- Only flake.nix changed. Authored Rust and all Cargo/generated/lock artifacts are unchanged from the published parent.
- Retained build-base: 3b261f923700ea872ad47b111aa6d9df794c79dd. This proves the earlier base stage, not a final common-pin gate.

## Invariant and positive evidence

The effective normal derivation graph is grouped by crate name and Cargo-compatible family: major for 1+, minor for 0.x, patch for 0.0.x. Each family admits one distinct derivation/source record. Syn permits explicitly approved majors 2 and 3 only. Every former forbidden-dependency assertion and the built-library bin-directory absence check remains.

Prometheus full immutable GitHub gate exited 0. cargo-nix, crate-features, crate-versions, dependency-boundary, memory-engine and default all passed.

Command: nix run github:Mic92/nix-fast-build -- --remote prometheus --no-nom --no-download --eval-workers 1 --flake github:LiGoldragon/memory-engine/32610884907461dc58c6c143f6f9fec0f13695fc#checks.x86_64-linux

Log: /tmp/memory-family-4e38c7/full-gate.log
Built graph: /nix/store/q9ddmz5qbmssd6jj03m8gs569bgd5qq4-memory-engine-dependency-boundary/normal-dependencies.json on Prometheus; local evidence copy /tmp/memory-family-4e38c7/normal-dependencies.json.
The graph contains 29 nodes, including syn 2.0.119 (syn@2) and syn 3.0.5 (syn@3).

## Negative witnesses

Each published child is based on the accepted candidate and injects one synthetic entry into the effective graph immediately after traversal. These are assertion-logic mutations, not changed Cargo dependency resolutions. Each was tested with the same full remote command, substituting its immutable revision. All exited 1; both checks.default and checks.dependency-boundary failed at the intended assertion. The other four checks passed.

- derivation: da539549636a352556214b3f2406fb8a261cf41b. Same family/version/source, changed derivation: family uniqueness assertion.
  Branch memory-family-4e38c7-derivation; log /tmp/memory-family-4e38c7/mutation-derivation.log.
- source: 34639bad69dbc61b110e30967acdb01523ff44b1. Same family/version/derivation, changed source: family uniqueness assertion.
  Branch memory-family-4e38c7-source; log /tmp/memory-family-4e38c7/mutation-source.log.
- syn-major: b1d335ca9b6380a46cd94b890ef64cf953c2b86b. Additional syn 4.0.0: approved-major assertion.
  Branch memory-family-4e38c7-syn-major; log /tmp/memory-family-4e38c7/mutation-syn-major.log.
- forbidden: 531ebf939fc19674d69c7da982a7ea0fc1f69c2b. Additional nota-next: forbidden-dependency assertion.
  Branch memory-family-4e38c7-forbidden; log /tmp/memory-family-4e38c7/mutation-forbidden.log.

Machine-readable negative outcomes: /tmp/memory-family-4e38c7/mutation-results.json.

## Downstream event

Orchestrate now consumes this Memory revision in published 5e872b354b2af0248c74408b69bcef22186a8469, with remotely regenerated Cargo.lock/Cargo.nix/crate-hashes.json and zero registry-version departures from d58fa6f. The single shared registry update has been requested from Mind core Sol. Component/scenario gates and test-only rebuild proof remain open under nyq8.
