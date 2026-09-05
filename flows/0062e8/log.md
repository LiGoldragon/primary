# CriomOS live installer architecture review

The living requested a review of CriomOS, CriomOS-home, Horizon cluster data, and Lojix: module gating, minimal live installation images, externally supplied synthetic nodes, package organization, historical preOS support, and upstream Nix implementations. This flow investigates and develops a proposal in conversation; implementation has not been approved.

Setup witnesses located the relevant repositories and the primary embedded Beads store. Existing dirty work belongs to flow 4a8046. Its preservation lock was rejected because lock 771 owns that path; no change was made to that work. This flow writes only its separately reserved lane and index entry while the other flow retains ownership.

Raw vision was recorded before substantive investigation. The living corrected the speech-to-text names to CriomOS and Lojix.

The delegated source, history, and upstream investigations are complete. Their carried accounts are preserved in reports/current-architecture.md, reports/vision-and-history.md, and reports/upstream-patterns.md. The source account includes the actually pinned Horizon dependency and the active cluster-data ownership boundary. No operating-system implementation, evaluation, build, or deployment was performed. The proposal remains for conversation.

The living corrected the format name to datom and directed this flow to keep designing while the datom audit is incorporated into a future revision. Format migration is deferred. The next review explains the actual horizon-wide configuration and shared generic node definitions with visuals. Prior source reports used implementation vocabulary as the format name; terminology correction is delegated without changing historical evidence. The living's concern about past guidance is a reason to inspect the architecture, not evidence of a particular defect.

The follow-up source inquiry and visual-design inquiry are complete. The conversation will distinguish authored horizon-wide data, the active cluster projection, reusable generic node definitions, and image/runtime stages. These are explanatory diagrams and a proposal for correction by the living, not approval of a schema, selection policy, identity policy, or source implementation.
