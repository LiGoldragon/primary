# Distillation sources: independent witness and completed repair

The distillation-source cleanup is now complete for the four requested main histories and the pinned generated skills. Psyche’s rewrite was already pushed on 2026-10-11. Mind and Field had no distillation Sources footers to remove from their main histories, so their unchanged histories are valid identity results. Curriculum had been missed: I found copied skill footers in its older commits, rewrote that history on 2026-10-12, and Field checked and propagated the new pin. No review of compensation skills or another approval was requested.

| Repository | Witnessed main | What happened | Distillation Sources at HEAD / in main history |
|---|---|---|---|
| psyche-skills | `d0d194c8d1bef78874c8aad842d70047978c4bac` | All 19 commits mapped from old `f776683bdf8b78e996151e6023ae7ddd5eff3a7c`; 243 introduced nonblank source-body lines retained in their landing messages. | 0 / 0 |
| mind-skills | `0d20c637d424235a2e5e93084ba96d17b90fabbf` | 19-commit main history audited; no applicable footers, so no rewrite or moved main was necessary. | 0 / 0 |
| field-skills | `a7bce979f99d61873b967b5d75707d25f8b75dbc` | Main ancestry audited, including the post-rewrite-order messaging update; no distillation footers, so no rewrite was necessary. | 0 / 0 |
| Curriculum | `d6029431faeef01a1b5aec7296641b9db5ccc8d0` | 604 commits and all 7 merge nodes preserved; 12 commits changed, with 236 introduced source-body occurrences moved into their landing messages. | 0 / 0 |

The fresh origin/main witnesses are recorded in `remote-refs-audit.json`. The protected old Psyche main remains at `backup/pre-sources-rewrite-20261011`; the protected old Curriculum main remains at `backup/pre-sources-rewrite-20261012`, pointing to `c390e1e3354b889b0c182d6cb21ef7c39e263103`. These recovery branches deliberately retain the original history. “No Sources in history” here means every commit reachable from each rewritten/current main, not deletion of the mandated backup copies. No other branch is allowed to be presented as the rewritten main.

## What was independently verified

I audited every Markdown path/blob in the named main ancestry, rather than only the current files or the earlier vision-only map. Psyche’s 19-pair old/new map was checked independently for path sets, modes, exact body preservation outside the removed terminal Sources sections, author/committer metadata, mapped parents, old-message preservation, and source-line presence in the mapped landing message. Its `skills/vision-ethos.md` to `vision/ethos.md` R100 rename carries existing references; it is not a new distillation and must not receive a duplicate insertion. The initial per-path audit incorrectly classified that rename as new; the initial output and the explicit rename correction are both retained. The corrected audit has zero errors and agrees with the 243-occurrence map. Persona’s three references were already in its original landing message and remain there without a new append.

For Curriculum I found 27 copied skill paths in three historical commits, giving 81 commit/path occurrences. Its old HEAD was already clean, which is why checking only HEAD missed the work. I then performed an object-only rewrite of the complete 604-commit graph. The independent verifier checked every old/new tree/path/mode, exact removal-only content change, all parent mappings and merge topology, authors and committers, original message preservation, and message multiplicity for every one of the 236 introduced nonblank source-body occurrences. Every changed commit has a good signature. The new and old HEAD trees are identical. No dirty checkout file, index, or checkout HEAD was changed by the rewrite. All of Field’s immutable builds keep their original c390 input reachable through the recovery branch.

The Curriculum publication was one atomic push of the rewritten main and `sources-in-commits-20261012`, with an exact lease requiring old main c390 and an absent candidate ref. It exited 0. A subsequent independent ls-remote matched new main d602 and the c390 backup. No plain force, clone, reset, rebase, or cleanup was used.

## Primary and generated skills

Field’s final checked publication is Primary `3d2a74492cdde899bac6bea0938da6f1a06a3127`, parent `e2b58bd10a3cda8f89a046ac63c7ce76265eccdb`. Only flake.nix and flake.lock changed. The pins are Curriculum d602, Psyche d0d194, Mind 0d20, and Field a7bce9; every other input is preserved. The refreshed Curriculum node retained the identical NAR because the current source tree did not change.

The exact new-pin package realization and one clean RebuildSkills/CheckSkills passed. Field compared all five generated surfaces, 24 role outputs, and two metadata outputs: all 599 were byte-identical. Final generated-skills-current passed, remote main matched shared HEAD, and PrimaryPublish 18616 was released. I separately audit the published generated Markdown to confirm no Sources section or obsolete footer-writing instruction remains. This is source/projection verification, not a claim that already-running native seats reloaded their context.

The selected Mind `skills/operation-psyche-distillation.md` now says references belong “in the message of the commit that lands it and never in a skill.” The obsolete sentence “the references sit in the skill’s Sources section” is absent from the selected source and generated projections. Older historical instructions can be retained as history; their later correction does not make them current instructions.

## Important boundaries

A literal `Sources:` line remains in Field’s compensation-nix-rationale and its five generated copies. It lists external technical documentation, not flow/topic distillation references, and is deliberately retained. Curriculum’s archived review material likewise includes external citations. The order concerned distillation provenance; this report does not hide literal technical citations by reporting a blanket text-search zero.

Some imported legacy Sources bodies contained prose provenance, and some references are `vision-raw <topic>` rather than a reconstructable flow ID. They were preserved in commit messages rather than converted to fabricated IDs. This witness proves no loss and the repository landing placement; it does not pretend to reconstruct pre-repository authorship that the raw records do not establish.

## Remaining work and delivery

No further source/history/pin repair remains for the requested main histories. Old recovery branches must stay protected, and future source changes must keep distillation references in their landing commit messages. The remaining deliverable is the living-requested book: the complete evidence package goes directly to a Sonnet subflow for publication. It is a report on the living’s ordered work, not a compensation-skill proposal. Core is contacted only if an actual blocker or ruling remains.

## Evidence package

The durable witness directory is `/home/li/private-repos/flow-evidence/41fa34/sources-audit-20261012/`:

- `main-history-audit.json`, `post-rewrite-main-audit.json`, and `remote-refs-audit.json`: full history/path and fresh remote-ref witnesses.
- `psyche-independent-no-loss.json`, its retained initial output, `owner-psyche-map.json`, and `owner-psyche-verify.json`: independent old/new checks and the source owner’s original map.
- `mind-skills-identity-map.json` and `field-skills-identity-map.json`: explicit unchanged histories.
- `curriculum-rewrite-map.json`, `rewrite_curriculum.py`, and `curriculum-independent-verification.json`: the full graph, reference/commit map, method, and zero-error verification.
- `field-quiet-window.json`, `curriculum-backup-publication.json`, and `curriculum-main-publication.json`: owner quiet acknowledgement, protected old main, atomic leased push, and remote match.
- `primary-projection-audit.json`, the final projection witness, and the exact one-URL pin packet: old/current projection checks and input scope.

Field’s final propagation receipts are at `/home/li/private-repos/flow-evidence/42265e/curriculum-rewrite-propagation-20261012/`: `source-qualification.json`, `lock-qualification.json`, `new-pin-runtime-realization.json`, `shared-generation.json`, `generated-comparison.json`, `freshness.json`, `publication.json`, and `release.json`.

The three prior source-owner reports are `flows/d68c82/reports/sources-rewrite-{psyche,mind,field}-skills.md`. They were treated as claims until checked against immutable objects and fresh refs. This report was authored by Mind 41fa34 on the living’s 2026-10-12 investigation-and-finish order.
