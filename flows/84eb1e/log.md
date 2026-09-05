# Ethos Zero rewrite

FLOW_ID: 84eb1e
FLOW_DIRECTORY: /home/li/primary/flows/84eb1e
PRIMARY_REPOSITORY: /home/li/primary
ETHOS_ZERO_REPOSITORY: /git/github.com/LiGoldragon/ethos-zero

## 2026-09-05 — scope and recovery

The living requested reimplementation of Ethos Zero 4.0.0, closing flow 1a6ca4’s Astra audit on protos 0.26.0 (2d999f173334) and datom-codec 0.21.0 (41a3c073d5c5). The substrate repositories are outside the write set. Every build, test, and probe is memory capped and timeout bounded; at most two builds run concurrently, Cargo serves iteration, and one final Nix flake check is reserved for the reviewed implementation. Landing is on main with a report in this lane.

Recovery was delegated to audit_recovery, vision_recovery, and crate_recovery. Their transcript responses carry the detailed source recovery. The audit and substrate closure report identify the generator adaptation as outstanding. Vision recovery found unresolved choices about kind-name collisions, omitted Types associations, and the Nexus scope; three asynchronous clarification questions are pending. Concrete migration and audit fixes proceed through rewrite while those choices remain open.

primary_baseline reports that pre-existing index.js was preserved in commit 4f1bc779 and pushed, with a clean working copy and typed release of lock 815. rewrite holds lock 814 for the complete Ethos Zero write set and has reported a bounded first migration compile exposing the old generated-trait boundary.

## Continuation after harness interruption

The living directed the same flow to continue from its intact lane and landed commits, retaining at most two concurrent builds. The remaining scope is exact fault locations, generic ambiguity and cycles, grouped imports, internal anatomy and naming, then final gates, main landing, and the lane report. The living also requested plain engineering descriptions of malformed-input handling, resource limits, typed refusals, and bounded recursion tests.

On resumption, collaboration listed only the main flow and intercom reported no coworkers. A new implementation subflow, complete_generator, owns the required continuation; it must recover current source and locks before editing.

## Candidate handed to independent review

complete_generator returned a clean, pushed 5.0.0 candidate and reports that the required local Cargo and authored gates pass. Its canonical account is reports/rewrite.md. The continuation fixed path construction, generic ambiguity and cycles, grouped imports, generated naming, internal anatomy, and public name/source validity. review_candidate now owns an independent code and behavior assessment in reports/independentAudit.md. The one final Nix flake check remains reserved until review is resolved.
