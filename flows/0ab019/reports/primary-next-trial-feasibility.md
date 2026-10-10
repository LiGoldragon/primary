# Primary Next trial: Mind feasibility

2026-09-19. Mind Astra 0ab019. Requested by psyche-fable-fresh, a subflow of b05237. Scope: feasibility and a reviewable trial design. No data migration, repository creation, history rewrite, seat launch, or service activation was performed for this report.

## Assessment

A separate Primary Next trial is feasible. The smallest useful trial is a pinned workspace with three explicitly mounted data repositories, selected vision and operational sources, generated skills, and a native startup packet that addresses those mounts. Existing production flows keep their current workspace and identity. Running well in the trial is evidence for a later migration decision, not that decision itself.

Two adaptations are necessary. Current skill generation reads Curriculum, not arbitrary Psyche/Mind/Field data trees. Current launch packets and readers also expect paths under Primary. Copying files and generating skills alone will not make a flow run correctly in the new layout.

This conclusion combines direct reads of the living's recorded trial brief and current Primary entry points with delegated read-only generator and inventory inspection. No assembled trial, generated trial projection, native startup, or runtime acceptance was witnessed here.

## Three data repositories, preserving the same files

Use one selected immutable source snapshot and a manifest of explicitly included branch snapshots. Keep file bytes intact. Each destination entry records original repository/revision, original path, blob identity, content hash, destination path, and whether it is a canonical record or a preserved handoff copy. New repositories need this source ancestry map even if their Git histories start fresh.

Proposed placement, subject to review:

| Repository | Contents and boundary |
| --- | --- |
| Psyche data | Living raw records, reviewed Vision and Intent, notions, supporting source records, and approval/correction provenance. Raw authority does not depend on whether distillation has occurred. |
| Mind data | Agent-authored operational knowledge, reports, witness indexes, chronology, transcript references, and refresh context. A report quoting living words retains the quote's originating source and its own agent authorship. |
| Field data | Field-owned operational records about machines, endpoints, resources, workspaces and seats. Mind may index these records; indexing does not require another canonical copy. |

Directory names alone cannot classify mixed records. In particular, `flows/<id>/vision/operational-*` often contains direct living speech, and a witness can concern Field operations while remaining a Mind observation. Preserve each mixed file as a whole with an explicit provisional owner and references to its sections. Do not rewrite, split, or promote its contents merely to populate the three repositories. Unresolved ownership belongs in the manifest and must not silently disappear from coverage.

Preserve original relative paths inside each selected data repository for this trial where possible. Expose the data through explicit roots and source locators in the new packet. A single old `flows/` symlink cannot represent files partitioned across three roots. Prefer updating the trial consumers to the intended roots rather than building a permanent compatibility overlay.

The manifest must include `Vision/`, `Intent/`, legacy `vision-raw/`, per-flow vision and notion, reports, witnesses, relevant logs and handoff bundles. Record exclusions individually or by a precise rule. The older 893603 inventory covers 999 files at `fe7b32e4ebfc418c1590d2fc134933938424d291`; it is a structural snapshot, not the current complete corpus. The 056f6d vision manifest explicitly excludes reports, logs and witnesses and identifies 89 handoff-source records missed by ordinary globs. Its counts and findings are attributed to that manifest, not a new census. Neither inventory alone satisfies the requested all-flow-data split. The deferred 840e42 branch preservation also needs an explicit inclusion or exclusion decision; a historical pointer is not evidence its files landed.

## Vision and generated skills first

Keep three things distinct: preserved source records, the selected instructional projection, and generated harness files. The instruction manifest should identify exact source records and revisions, role selection, generated name, and review status. A topic heading is not by itself a skill or a dependency edge. Living-reviewed guidance and agent operational guidance can both inform a flow while retaining their different provenance.

Delegated inspection of curriculum-deploy found explicit data-root and workspace-root arguments. It reads `<data-root>/skills/*.md` and `roles.datom`, then emits harness projections. The current implementation does not directly turn `Vision/`, reports or three data repositories into skills. For an initial trial, retain the permitted Curriculum generation mechanism with an explicit, reviewed source selection. Moving generation into Harness is a separate implementation step, not a prerequisite to demonstrate the workspace shape. Raw records remain unchanged while the instructional projection is reviewed independently.

Pin one exact Curriculum revision, deployer revision, role manifest and Nix input set together. A checkout's current HEAD, an upstream main, and the consumer's pinned input are different evidence. At this review, Curriculum HEAD was directly observed at `7ba91be823ee099d69a5c36731bfa47b6e00f8e6`, while Primary's flake text still named Curriculum `880d1d587d06` and curriculum-deploy `dc7f70edce08`. Do not silently substitute one for another. Generated directories remain read-only output.

Dotted face names remain a naming proposal pending the living's ruling and native discovery/expansion witnesses. The new Type-root FinalResponse proposal and its unresolved named-variant wire spelling are separate from this storage trial. Preserve raw final responses and their source provenance; do not require a speculative parser to recover them.

## What a trial flow needs, and what breaks

| Dependency | Required trial treatment |
| --- | --- |
| Native context | A complete role packet with actual skill expansion receipts, source manifest, model/effort, and native session/turn identity. Source-file presence alone is insufficient. |
| Workspace and data roots | Explicit Primary Next, Psyche, Mind and Field roots; supported read/write ownership; exact pins and writable scope. Setup variables must be used by consumers, not merely listed in a file. |
| Launch manifests | New trial manifests referring only to mounted records. Existing fixed Astra/Sol/Luna bundles expect `Vision/...` and `flows/...`. |
| Identity | Field supplies a fresh trial identity and endpoint binding; original flow markers remain provenance, not identities a trial may claim. Shared identity uniqueness must survive multiple workspace roots. |
| Transcript discovery | Resolve actual native session to its real transcript path. Claude project buckets depend on workspace; existing `/home/li/primary` assumptions and current POC fixed mappings do not cover new seats. Codex files require full-session correlation, not a blind prefix glob. |
| Messaging | Use explicitly verified trial routes and preserve receipt grades. Exclude trial seats from production fanout. Current prototype closed target pairs will not accept arbitrary new flows. No public Message/FlowNexus acceptance is implied. |
| Locks and writes | Reserve actual destination paths. A logically identical path in a different repository is a different reservation. Preserve a single authoritative writer per record. |
| Cross-references | Resolve each link to its selected revision or mark missing/outside/unresolved. Nested handoff copies retain their origin; duplicate filenames cannot be collapsed blindly. |

Concrete source findings: `tools/native-seat-launch.mjs` permits a cwd override, but its role packet requirements are not satisfied by an otherwise empty mounted workspace. `tools/compose-refresh-prompt` derives a root from its own location yet hardcodes `--flows-root /home/li/primary/flows`. `tools/claude-native-seat-refresh.py` uses the native Claude project root. Primary's generated-skills check compares against its flake `self` and pinned Curriculum. These consumers need deliberate trial configuration; changing a directory name does not retarget them.

## Proposed acceptance sequence

1. Review the three-way placement manifest, including mixed records, selected branches, exclusions and unchanged byte hashes. Give each canonical record one owner.
2. Field assembles the isolated workspace and mounted repositories under separately authorized scope. No existing seat is moved or retired.
3. Check generated projection equality against the exact selected inputs using the Nix-built checker. Validate that every startup source reference resolves. These checks establish preparation, not native skill receipt.
4. Field launches a bounded trial flow with its actual native identity and context receipts. Exercise source lookup across all three mounts, an explicitly reserved disposable write, and one benign trial-to-trial message with observed recipient receipt. Verify no production fanout or old-workspace write.
5. Preserve native transcripts and report the actual source used, write location, message receipt grade, startup failures, and resource consumption. Compare destination bytes and source hashes, and verify links and identity continuity after restarting only the disposable trial if that restart is authorized.
6. Bring the evidence and remaining failures to the living before proposing migration. Successful trials authorize no deletion, archive cleanup, source retirement or history rewrite by themselves.

The low-resource policy remains in effect: lightweight inspection and edits locally, compilation and substantial validation only on verified remote Nix builders with no local fallback. This report ran no trial tests or builds. Field owns workspace/launch/seat feasibility and the new successor endpoint; Mind owns this data, provenance and context assessment.

## Delivery

The requested recipients are the newly launched successor Fable of b05237 and the current Psyche main flow. Field has been asked for their exact identities and endpoints. A lineage name is not a routing receipt. Delivery and any recipient acknowledgment will be reported separately once those bindings are supplied.

## Sources

- Direct current Primary reads at main `d38773fd7af963c7b31960a793579436c7547b8a`: `flows/b05237/vision/operational-skillsAreVisionRepropagated.md`, `operational-threeDataReposAndPrimaryNext.md`, `operational-primaryNextPsycheLogging.md`, `operational-logOnMainNowMigrateLater.md`; raw quotations distinguished from their explanatory context.
- Direct reads: `Vision/psyche.md`, `Intent/context.md`, `flows/9993b5/vision/psycheVsMind.md`, `flows/893603/reports/primary-next-mind-report.md`, Primary `AGENTS.md`, `SKILL_VARIABLES.md`, `flake.nix`, and the named launcher paths.
- Existing manifest evidence, read by messaging_finish: `flows/893603/reports/primary-next-source-inventory.json` and `flows/056f6d/reports/vision-corpus-manifest.md`. Counts retain their original snapshot and scope; no complete current recount is claimed.
- Delegated read-only generator inspection by messaging_contract_review: curriculum-deploy `src/runtime.rs:106-123,272-326`, `tests/runtime.rs:23-32`, its flake inputs; Primary `tools/compose-refresh-prompt:20-47,88-105` and native-seat launch preflight. The reader observed deployer working revision `b1e411f0d8e680b8d6198182a11b9a07516dfa0f`; this is not asserted to be Primary's pinned deployer.
- Direct Curriculum HEAD receipt `7ba91be823ee099d69a5c36731bfa47b6e00f8e6`; generated `operational-final-response/SKILL.md` and updated `flows/b05237/reports/final-response.ethos` read in the preceding design exchange.
