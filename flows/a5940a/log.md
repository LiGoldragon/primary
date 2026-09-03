# Main-flow delegation correction

Working instruction: investigate what flow `d30eb1` was doing when its main-thread transcript produced giant command outputs, then propose and land the approved correction to the authored `main-flow` skill.

`FLOW_ID`: `a5940a`. `FLOW_DIRECTORY`: `/home/li/primary/flows/a5940a`.

This request began as investigation and now rules realization of the approved wording. It does not add a Vision entry.

The living approved replacing `Delegate task work to child flows.` with `Delegate task work, probes, and verification to child flows.` and adding `Relay child findings with their origin. When more evidence is needed, ask a child to obtain it.`

The first approved correction landed in Curriculum commit `28f7953ff78116d0e0270cc60196dd92b6825446` and primary projection commit `799ddc3ee859`. A fresh-flow trial reported that its main thread still repeated delegated file reads.

The living then envisioned an exact-path and whole-file-relevance boundary for parent reads; its verbatim record is `vision/mainFlowShouldNeverTryToLocateAFile.md`. The approved rewrite landed in Curriculum commit `b62804533f50e7f34485cf6503d986f2e5432c8b` and primary projection commit `b90b3bf66d34`. Generated-skill checking and the no-build flake check passed. A child reported that a later fresh main thread still ran file-location commands; whether that session loaded the exact new projection remains unwitnessed, so behavioral verification is unresolved.
