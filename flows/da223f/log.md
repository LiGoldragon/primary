# Datom codec and Protos rewrite

2026-09-05 — The living requested closure of flow 1a6ca4’s Astra audit through an anatomical rewrite of datom-codec and affected protos, landed on main with green gates. Ethos Zero remains outside the write scope. Recovery subflows read the audit, current vision and raw records, and witnessed the starting crate revisions. The audit and source locations will be carried in the closure report.

The living reported a host termination under memory pressure. The resumed implementation subflow witnessed retained lock 796 and the five modified datom-codec files and two modified protos files. All subsequent subflow builds, tests and probes are constrained to 4 GiB and a timeout; no more than two subflows may build at once. The caller-limit versus fixed-limit resource contract remains a pending design question.

Primary’s found-in-tree records were preserved unchanged and pushed by the preservation subflow before this lane was written. Root owns the lane and index reservation, lock 799; implementation owns both crate write sets through lock 796.

2026-09-05 — The living distinguished the latest provider-capacity interruption from the earlier host-memory terminations. Resumed subflows witnessed the retained edits, revisions and locks. Builds and probes continued under a 4 GiB cap and a timeout, with at most two subflows building, Cargo for iteration, and bounded remote Nix checks for the final sources.

The flow resolved the earlier resource-contract question with an explicit caller-owned incorporation budget. This is an implementation decision within the rewrite, not a recovered numerical ruling from the psyche. Independent verification also found raw Datom compositions whose in-memory projection passed while printed Text changed their anatomy. The final admitted word domain and quoted Text projection close that defect; the final independent corpus passed all 738 compositions across 246 admitted words from 3,905 candidates on the shipped revisions.

The implementation and verification subflows report Protos 0.26.0 at `2d999f1733347b7e64e24b2f75ba889ad7182bc0` and datom-codec 0.21.0 at `41a3c073d5c5cdcb3ebb1a5c842e8c068145fdb2`, clean and pushed on main, with datom-codec pinned exactly to Protos. Capped Cargo gates and both final remote Nix flake checks are green. The in-scope F1–F10 closure and its evidence are recorded in [the implementation report](reports/rewrite.md) and [the independent verification report](reports/verification.md), pushed through primary `85be36001a65`.

Ethos Zero remains untouched at 4.0.0 `dc54e3323ae00dc3f88f4d65c2785e6800c06b74`. Its historical generated implementation template needs downstream adaptation to the rewritten API; the reports distinguish this finding from the crates' passing declaration-freshness checks. The source reservation was released with the typed `Released` response for lock 796. The records reservation will be released after this closing log is pushed.
