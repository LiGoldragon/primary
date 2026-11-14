# Orchestrate shared-base cohort — nyq8 / nmr8

Owner: Mind curriculum Sol, flow 4e38c7. Coordinator: Mind curriculum Astra.
No live switch, Home mutation, or source-main promotion was performed.

## Published immutable inputs

- build-base main: 51511a351dd3144d8f8d2cc81d711bc86db5c6a2, registry owner Mind core Sol. Its independent base and overridden-consumer gates are recorded in flows/1541ef/build-base-orchestrate-cohort.md.
- Orchestrate branch build-base-299aa3: 64ff4a5e09ff3d3d7d7b9e66f4969759cb02cdbf. This commits the actual canonical base pin. Parent 5e872b354b2af0248c74408b69bcef22186a8469 holds the remotely regenerated coherent Cargo.lock, Cargo.nix and crate-hashes.json.
- Ordinary contract branch build-base-299aa3: 2b17beab3a79e937b73bc506f457fa342505de5f.
- Meta contract branch build-base-299aa3: 463ff8b2eddeab63488f12162d32274421ae66cb.
- Nexus branch hash-299aa3: 69946db066bb70bdbc1fd7dbf5e6c88dcf05c363, accepted ec097e3 plus four Hash derives.
- Memory engine branch build-base-299aa3: 32610884907461dc58c6c143f6f9fec0f13695fc. Its earlier base-stage acceptance and mutations are recorded in memory-family.md.
- Signal 11: 6d4eb74a238ea4a6149bd12c42a8c06aec01b154; signal-transport: 035fb7fbac8de5e493cdb42ed50fefd94bfb569b.
- Scenario branch build-base-299aa3, repository orchestrate-test: 467bedf2b0c2b4e83794bb2b46daa4cba436524b.

All component sources remain in /home/li/worktrees/<repository>-build-299aa3, Nexus in nexus-hash-299aa3. Existing locks 183, 185, 187 and 188 are retained.

## Gates observed on Prometheus

Every full gate used nix-fast-build --remote prometheus --no-nom --no-download --eval-workers 1, checks.x86_64-linux of the immutable GitHub revision; no local compilation.

- Actual Orchestrate pin 64ff4a5e: exit 0, all 11 attributes green. Log /tmp/orchestrate-cohort-4e38c7/full-gate-64ff4a5e.log. Includes Cargo freshness, version/features, documentation, formatting, all member tests and datom-free Nexus.
- Scenarios 467bedf2: exit 0, all 11 attributes green (nine runtime scenarios, lint and default). Log /tmp/orchestrate-cohort-4e38c7/scenario-gate-467bedf2.log.
- Previous scenario 0eb8f02b: all nine runtime scenarios passed; lint and default failed two inherit-style warnings. The accepted child fixes those two assignments without changing scenario assertions. Earlier log scenario-gate-0eb8f02b.log is retained.
- Ordinary 2b17beab with explicit base51511a3 override: exit 0, all five checks green. Log /tmp/orchestrate-cohort-4e38c7/ordinary-contract-gate.log.
- Meta 463ff8b with explicit base51511a3 override: exit 1; three checks passed, crate-features and default failed. Signal11's datom named set attaches datom-codec/protos absent from this Cargo.nix. Log /tmp/orchestrate-cohort-4e38c7/meta-contract-gate.log. Core question asks whether ordinary datom must propagate signal/datom before regenerating both contracts. Standalone meta is not accepted.

The scenario lock preserves previous and live exactly at 0f9961460f84b752fa9605ebf0e2b6e1c685aa91 and sema exactly at c7c44cb39934b0727d724a6aa03a36a2a94cacf9. Candidate Orchestrate is 64ff4a5e and its own base, plus the scenario root base, are 51511a3. Every original URL remains bare.

## Committed test-only rebuild evidence and remaining reuse gap

Proof branch test-rebuild-4e38c7: 492b877eda402375b9dfc4b8ca3669f3c8a92c21, child of 64ff4a5e. Its only edit renames the multi-path Lock test in crates/orchestrate-nexus/tests/ordinary_lock_contract.rs. Its full remote gate exited 0, all 11 attributes green; the renamed test ran and passed.

Remote evaluations show all three binary drvPaths and the full 78-node normal graph unchanged. The binary's input still names normal Nexus library g0w9ja5x3amy5bypabxx9g8iy58a7lva. Both client test drvPaths are unchanged. Only Nexus test drv changes from ar9sxz2ln6qzn7zjzpgrmqhi556pg7qp to c1bshqqfcbxhkn093sg6a69qdr0dqyvz.

This establishes test-only invalidation, but full shared-library reuse acceptance is withheld. The new test build code-generates src/lib.rs without --emit=metadata and integration tests link its target/lib archive. Direct test dependencies contain identical memory-engine bjawbazz twice, as both normal and dev dependency. Compared with the normal library inputDrvs, no normal dependency derivation changes; only tempfile/getrandom/fastrand are added. Hypothesis sent to base owner: withoutDevOnly filters dev-only dependencies but leaves duplicate overlapping normal/dev dependencies, so drvPath equality incorrectly fails. Core owns the correction; no base file was edited here.

Proof files are retained at /tmp/orchestrate-cohort-4e38c7/: proof-before.json, proof-after.json, proof-summary.json, rebuild-proof.nix, nexus-binary-derivation.json, nexus-library-derivation.json, nexus-test-derivation.json, test-direct-dependencies.json and test-edit-gate-492b877e.log.

## Separate Home fixture diagnosis

This is independent of the cohort gates, against Home 0fda875f92880411eff0b1be91cd200d9c065388 and its own pinned Orchestrate package.

A direct read-only import of checks/orchestrate-service-path/default.nix reproduces the exact original drv1xwwg916617p7wfnygj0k04k9iizmc0k. A tracing-only override (drv25fc3p7pxqpc6196szq8x61cyd2mplz0) fails at test -f .../orchestrate-nexus.sema after preflight and both socket checks pass. The current store is orchestrate-nexus.memory.

A diagnostic override replaces only that positive assertion with memory-file existence plus stale sema-file absence. It exits 0 and retains every original executable, preflight, legacy-store preservation, socket, Lock/Observe/Release and Configure assertion. Output /nix/store/4mbgn0m04krcgax9db8ac5d685yf5z50-orchestrate-nexus-service-path. Source correction and the Home full gate remain with core Sol; no Home source was edited.

Retained diagnostic files under /tmp/orchestrate-cohort-4e38c7/: home-original-derivation.json, home-diagnostic.nix, home-service-traced-direct.log and home-service-corrected.log. Earlier home-service-diagnostic.log and home-service-traced.log are failed diagnostic setup attempts, not reproductions or gates.

## Open custody

Astra coordinates; core Sol owns the canonical registry, base reuse correction, and Home fixture. This flow owns contract feature correction after the core answer, subsequent exact pins/gates, and the final reuse proof. nyq8 remains open. Curriculum separation and lm7j remain held under inea/d67y and primary-q8li; the deployed datom-enabled package is preserved.

Future ethos29 obligation from Opus 1uvt/oquw: signal-orchestrate's store refusal becomes Refused.StoreFailure with StoreFailure.String (text Refused.«…»). This cohort stays ethos28; no refusal-shape change is bundled.

## Core outcomes received after the initial report

Core c52q confirms the reuse cause against matching compiler inputs: identical effective features, renames and normal dependencies; the duplicate identical memory-engine survives withoutDevOnly and defeats drv equality. Stable drvPath deduplication after dev-only filtering is before Psyche core Opus for approval, with an actual-link positive oracle and feature-changing-dev negative oracle. No base change or successful reuse gate is claimed yet. Core auj5 explicitly preserves our package/test-only separation evidence as valid but distinct from shared-library reuse.

Core 0n5r reports the separate Home source correction landed in isolated branch codex-fixture-rp26-1541ef, revision c924ff6316d7dc90c433898195d6005c1234612e. Its full gate is green, 98/98, with the same verified system SRI. The immutable component used by that Home fixture is ef4fe80b98a8144b8138b2a67eb4f0ad095f32b1; defaults.rs lines 16–17 name current .memory and previous .sema. Evidence is flows/1541ef/home-codex-fixture.md and its sibling home-codex-fixture-evidence/full-gate-c924ff63.log. This is an independent Home candidate, not a cohort pin or live change. Meta feature-edge provenance remains under core qhsi audit.
