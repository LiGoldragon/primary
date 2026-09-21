# Curriculum skill namespace ownership contract

**Date:** 2026-09-21  
**Owner:** Mind4b0f60 architecture.  
**Status:** living architecture design for future regeneration. It authorizes neither implementation, deployment, permission changes, nor cleanup of existing generated trees.

## Canonical identity and metadata

Curriculum is the canonical authored metadata source, held in pure data rather than generator or runtime code. A skill has the typed key:

```text
SkillKey = (source_id, type_id, skill_id)
```

`SkillType` is independent of aspect, power, and core/extended module dimensions. Its role is a regeneration namespace such as operational, vision, or testing, never an inference from a prefix or destination path. The original roles now include `spirit-role` and `intent-role`; any old audit that described them as absent is historical only and does not define current metadata.

A trusted source registry binds `source_id` to its canonical root and allowed types. Explicit exposure and trust metadata control accessibility; they are distinct from deletion ownership and are never inferred from namespace. A self-declared arbitrary source cannot adopt existing output. Migration assigns explicit types to known legacy entries; existing flat skills are not blindly classified as operational, and unclassified entries are preserved.

Each consumer owns an installed-projection ledger keyed by `(target_root_or_harness, source_id, type_id)`. The ledger records every generated file's `SkillKey`, exact generated path, owner, last-installed digest, source revision, namespace adapter mapping, and expected inventory generation. This ledger, not a location or name, establishes ownership. A `testing-*` skill that was placed ad hoc and is absent from the ledger remains unowned and preserved even where its filename looks generated.

## Namespace reconciliation

A complete snapshot of one selected `(source, type)` namespace reconciles only manifest entries the same consumer previously owned in that namespace. Its deletion candidate set is:

```text
previous_owned(source, type) − desired(source, type)
```

Deletion requires a complete and successfully parsed source snapshot, a readable ledger, a matching installed digest, and the exact recorded path. Missing/incomplete source, read failure, parse failure, unreadable ledger, or stale plan means **no deletions**. An explicit empty complete snapshot is distinct and can intentionally prune its own unchanged entries. An edited owned file becomes a typed conflict and is preserved. Unknown directories, other source/type entries, files outside the ledger, and unowned files within an owned skill directory are preserved; a namespace update never recursively sweeps `.claude/skills` or another root.

The engine validates every canonical descendant path, rejects symlink escape, sanitizes names, and refuses collisions rather than overwriting or adopting a file. Source-specific deterministic adapters map the typed key into each harness's supported discovery layout. A consumer may flatten source/type/name when its discovery surface requires it, but the typed key stays authoritative. It must not assume nested Claude discovery works. Legacy names persist through an explicit map, not automatic rename. A type move is two explicit namespace plans, never incidental old-type cleanup.

## Safe projection procedure

Before writing, the consumer stages and validates the entire selected-namespace plan, including canonical paths, adapter results, collisions, source completeness, all recorded digests, and the expected inventory generation. It takes an exclusive mutation lock for the target root, shared as a protocol by every projection writer, then CAS-preflights the inventory generation and rechecks digests immediately before application. Each individual replacement is atomic; a durable journal and ledger recovery handle interruption. This contract does not claim a multi-file atomic filesystem transaction. A commit receipt records the applied plan and resulting ledger state.

User edits default to conflict, never forced overwrite. Migration begins with a legacy-tree inventory. Only exact, known generator artifacts with matching hashes may be adopted under an explicit adoption plan; unknown files are preserved. Existing aliases remain until their consumers migrate. One selected namespace cannot silently adopt, rename, or delete another source/type's output.

## Ownership cases

| Case | Required outcome |
|---|---|
| Vision namespace update | Regenerate Vision only; preserve operational and testing outputs from every source. |
| Same type, different source | Preserve the other source's projection. |
| Desired selected skill removed | Delete only its unchanged, ledger-owned files after a complete snapshot. |
| Ad hoc `testing-*` file | Preserve; prefix is not ownership. |
| Ledger-owned file was edited | Return typed conflict; preserve it. |
| Source parse/read incomplete | Fail closed; make no deletions. |
| Complete empty namespace | Prune only unchanged entries previously owned by that exact namespace. |
| Collision or symlink escape | Refuse plan before overwrite/write. |
| Interrupted or concurrent generation | Recover journal/ledger or reject stale plan after digest recheck. |

All actual harness targets need these cases in their behavioral tests. Tests must exercise the real adapter/discovery layout, including any flattening, rather than merely unit-testing pathname strings.

## Scope and evidence gates

The design covers ownership-aware projection only. It does not change Curriculum sources, generator code, or `.agents/`, `.claude/`, `.codex/`, or `.pi/` generated evidence. Before implementation, the concrete generator, manifest, and target-root paths must be audited; the implementation must preserve generated-tree restrictions and coordinate the exclusive target-root mutation lock shared by every projection writer.

That audit is now concrete. Curriculum at `/git/github.com/LiGoldragon/Curriculum` is clean main `2c15ef565847cba600f55c86f7c082ebf318cbe1`. Consumer `curriculum-deploy` is anchored at parent `dc7f70edce087ac4157d7b48af954177ce454491` but has an uncommitted added `result`, which is excluded from this report. [`src/runtime.rs`](/git/github.com/LiGoldragon/curriculum-deploy/src/runtime.rs:280) reads all `Curriculum/skills/*.md` and renders only `.agents/skills/<stem>/SKILL.md` and `.claude/skills/<stem>/SKILL.md`; `user-only: true` additionally writes `.agents/.../agents/openai.yaml`. It has no observed `.codex` or `.pi` skill projection. Its [`clean_previous_skills()`](/git/github.com/LiGoldragon/curriculum-deploy/src/runtime.rs:370) recursively deletes every direct child containing `SKILL.md` when that child name is absent from the current source stems, then calls `remove_dir_all` on it at [line 382](/git/github.com/LiGoldragon/curriculum-deploy/src/runtime.rs:382): it has no ownership manifest, provenance, or type namespace and therefore can delete ad-hoc or other-source directories. [`write()`](/git/github.com/LiGoldragon/curriculum-deploy/src/runtime.rs:346) performs both cleanups before it renders outputs at [line 348](/git/github.com/LiGoldragon/curriculum-deploy/src/runtime.rs:348), so a render failure can delete first. The flat output path at [line 317](/git/github.com/LiGoldragon/curriculum-deploy/src/runtime.rs:317) can overwrite a same-name foreign file. `tests/runtime.rs:24` asserts that legacy global cleanup. This is current code observation, not desired behavior.

Roles use the separate `src/roles.rs` route to `.claude/agents`, `.codex/agents`, and `.pi/agents`, recording only role paths in `skills/generated-role-outputs.datom` as `GeneratedRoleOutputs{Vector<String>}`. That inventory is a partial precedent, not a safe complete solution: it clears listed roles before rendering and holds no digest/source/type identity. Render-time `{% if claude/codex/pi %}` conditionals do not change the observed skills output enumeration, which remains Claude/Codex only. Current `safe(relative)` rejects absolute/parent-directory paths but does not witness symlink containment. No Generate/Check run was performed, and no current type namespace metadata is witnessed. The proposed validation must therefore prevent both deletion and replacement collisions, validate a complete plan before all mutations, and test every actual emitted harness target without claiming all harnesses are currently covered.

`Request::execute` in [`runtime.rs`](/git/github.com/LiGoldragon/curriculum-deploy/src/runtime.rs:104) currently accepts `Generate`, `Check`, and `Visualize` with data/workspace roots, and Generation writes roles and skills together. The proposed evolution is a typed reconciliation request selecting source/types/target surfaces plus expected inventory and complete snapshot, returning typed planned/applied/conflict results. Its exact variant/schema is a proposal, not compiled behavior. Scoped skill regeneration must not invoke unrelated role cleanup. After migration, old unscoped `Generate` must delegate to explicit manifest-owned reconciliation or refuse destructive cleanup; a maintained entrypoint/version rollout prevents an old generator from later sweeping foreign directories.

## Sources

- **Current living instruction and root decisions:** typed identity, canonical Curriculum pure-data metadata, ledger ownership model, selected-namespace reconciliation, projection safety, migration, and required test cases. These are architecture authority, not observed implementation behavior.
- **Root-reviewed authored sources:** `Curriculum/ARCHITECTURE.md` and `roles.datom`, including current `spirit-role` and `intent-role`; the old absence statement is historical only.
- **Root-reviewed living design:** [operational-skillTypes.md](/home/li/primary/flows/108ab0/vision/operational-skillTypes.md), [operational-visionIsSkill.md](/home/li/primary/flows/108ab0/vision/operational-visionIsSkill.md), [operational-operationalSkillsRepo.md](/home/li/primary/flows/108ab0/vision/operational-operationalSkillsRepo.md), and [operational-testTypeSkills.md](/home/li/primary/flows/1ac573/vision/operational-testTypeSkills.md). They ground type creation/access exposure, source module/trust/removability, and test-type treatment; this report keeps trust/exposure separate from delete ownership.
- **Generator-path audit returned by `/root/checkup_architecture`:** Curriculum main `2c15ef565847cba600f55c86f7c082ebf318cbe1`; `curriculum-deploy` parent `dc7f70edce087ac4157d7b48af954177ce454491`; `src/runtime.rs`, `clean_previous_skills()`, `tests/runtime.rs:24`, `src/roles.rs`, and `skills/generated-role-outputs.datom`. It establishes current code behavior and limits only; no Generate/Check or deployment was run.
