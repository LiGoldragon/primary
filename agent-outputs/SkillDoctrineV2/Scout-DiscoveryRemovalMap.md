# Discovery Removal Map

Task: map where `skills.nota` is still wired, generated, expected, documented, or treated as canonical for SkillDoctrineV2. Scope was read-only except for this assigned output file.

Settled direction: remove `skills.nota` entirely as a runtime discovery surface. V2 generated worker role packets should carry curated critical doctrine modules instead of relying on runtime discovery.

## Commands Consulted

- `sed -n '1,220p' /home/li/primary/AGENTS.md`
- `sed -n '1,220p' /home/li/primary/skills/skills.nota`
- `rg -n "skills/skills\\.nota|skills\\.nota|Skill Index|skill index|discovery path|Primary discovery|single NOTA roster|generated-role|active manifest|active-outputs|skills-roster" ...`
- `rg -n "skills/skills\\.nota|skills\\.nota|Skill Index|skill index|discovery path|runtime discovery|named by the task, the role" /git/github.com/LiGoldragon/skills/modules/*/full.md /git/github.com/LiGoldragon/skills/roles/*/full.md`
- `nl -ba` slices for `/git/github.com/LiGoldragon/skills/src/assembly.rs`, `/git/github.com/LiGoldragon/skills/tests/generation.rs`, docs, manifests, and schema.

## Important References

1. `/home/li/primary/AGENTS.md:8`, `:18`, `:58` - classification: replace.
   Observed: startup requires reading `skills/skills.nota`; the "Skill Index" section says it is the discovery path; Rust editing requires Rust skills selected from it.
   Replacement direction: AGENTS should stop naming a runtime skill index. It should say generated worker packets carry their required doctrine, and additional doctrine is selected by explicit prompt/role packet/context rather than querying `skills/skills.nota`. Rust editing should point to curated Rust doctrine in the worker packet or explicit role/module envelope.

2. `/home/li/primary/ARCHITECTURE.md:47-48` - classification: replace.
   Observed: primary tree map lists `skills/<name>.md` and `skills/skills.nota` as "the typed skill index".
   Replacement direction: remove `skills/skills.nota` from the primary tree model. If a source-of-truth note remains, point to the skills repo manifests/generator for source modules and to generated harness skill/role packets as runtime surfaces.

3. `/home/li/primary/INTENT.md:198-201` - classification: inspect.
   Observed: dynamic role creation guidance says a new role queries `skills/skills.nota` for the closest existing role-skill.
   Replacement direction: this may already be stale against current Spirit-only intent direction, so an intent-maintenance pass should decide whether to remove the whole pattern or restate it as "compare against generated role/source module inventory" without runtime discovery.

4. `/git/github.com/LiGoldragon/skills/src/assembly.rs:252-258` - classification: remove.
   Observed: every generation run pushes a rendered `skills/skills.nota` job built from `SkillIndex::new(self.configuration.active_skills()).render()`.
   Replacement direction: delete the rendered index job. V2 role packets should get doctrine through `ActiveRole.included_modules`/manifest-authored curated module lists, not a workspace discovery index.

5. `/git/github.com/LiGoldragon/skills/src/assembly.rs:381-384` - classification: remove.
   Observed: `expected_outputs()` always inserts `skills/skills.nota`.
   Replacement direction: remove the expected-output entry so `check-skills` no longer requires the file.

6. `/git/github.com/LiGoldragon/skills/src/assembly.rs:993-1044` - classification: remove.
   Observed: `SkillIndex` renders the whole NOTA index and `ActiveSkill::index_record()` points entries at `.agents/skills/<name>/SKILL.md`.
   Replacement direction: delete `SkillIndex` if no non-runtime inventory replaces it. If an internal inventory is still useful, keep it source-side under manifests/reports, not as `/home/li/primary/skills/skills.nota`.

7. `/git/github.com/LiGoldragon/skills/tests/generation.rs:13-40` - classification: replace.
   Observed: the first generation test asserts `skills/skills.nota` exists and contains the generated `.agents/skills/example/SKILL.md` index record.
   Replacement direction: assert first-class skill files still emit, and add a negative assertion that `skills/skills.nota` is not generated.

8. `/git/github.com/LiGoldragon/skills/tests/generation.rs:400-419` - classification: replace.
   Observed: stale-check fixture writes `skills/skills.nota` as an old generated output and expects check mode to fail.
   Replacement direction: remove `skills/skills.nota` from ordinary stale-output drift expectations. Add a migration/deletion-specific test only if the generator is intended to prune the retired file once.

9. `/git/github.com/LiGoldragon/skills/tests/generation.rs:421-435` and `:522-532` - classification: replace.
   Observed: legacy roster stale-output test writes an expected empty `skills/skills.nota`; `expected_empty_index()` hardcodes the old index preamble.
   Replacement direction: legacy roster checks should not require an empty discovery file. Delete `expected_empty_index()` unless a separate non-runtime inventory replaces it.

10. `/git/github.com/LiGoldragon/skills/README.md:5`, `:25`, `:37-39` - classification: replace.
    Observed: README says the generator assembles from a single NOTA roster, explains V1 active manifest plus compatibility roster, and says primary discovery currently emits `skills/skills.nota`.
    Replacement direction: update for V2: normal generation is manifest/dependency driven; worker role packets carry curated doctrine modules; no primary discovery index is emitted. Keep `skills/generated-role-outputs.nota` as role cleanup inventory if still true.

11. `/git/github.com/LiGoldragon/skills/ARCHITECTURE.md:42-45`, `:73-82` - classification: replace.
    Observed: architecture lists `skills/skills.nota` as a derived inventory and says generated NOTA outputs include discovery and role inventory files.
    Replacement direction: derived inventory should only name `skills/generated-role-outputs.nota` unless a new non-runtime inventory is introduced. Replace "discovery" with "role cleanup inventory"; describe V2 doctrine inclusion through role manifests.

12. `/git/github.com/LiGoldragon/skills/modules/skill-editor/full.md:47-55`, `:63-85`, `:99-104` - classification: replace.
    Observed: skill-editor says the primary index points at `.agents/skills`, primary keeps `skills/skills.nota` as discovery index, descriptions live in `skills.nota`, every workspace skill has an index entry, and cross-references may point to `skills/skills.nota`.
    Replacement direction: make the active manifest (`manifests/active-outputs.nota`) the source of output identity, description, tier, and target surfaces. For runtime cross-references, use generated harness skill names or source module identifiers, not `skills/skills.nota`.

13. `/git/github.com/LiGoldragon/skills/modules/helper-context-transfer/full.md:23-26` - classification: replace.
    Observed: helper reading envelopes include "skills named by the task, the role, or `skills/skills.nota`".
    Replacement direction: replace with "skills/modules named by the task, generated role packet, or explicit dispatch envelope." This aligns with V2 packets carrying curated doctrine.

14. `/git/github.com/LiGoldragon/skills/modules/nota-design/full.md:9`, `:152-154`, `:281-285`, `:332-333` - classification: replace.
    Observed: NOTA design treats `skills.nota` as the canonical example and tells authors to open it before sketching records.
    Replacement direction: choose a new canonical NOTA example, probably `manifests/active-outputs.nota` for variant-rich manifest design or a small purpose-built fixture in the NOTA repo. Avoid pointing record-design discipline at a retired runtime discovery surface.

15. `/git/github.com/LiGoldragon/skills/modules/nota-schema-docs/full.md:75-79` - classification: replace.
    Observed: see-also points to `skills/skills.nota` as the canonical workspace example.
    Replacement direction: point to the same replacement canonical NOTA example chosen for `nota-design`.

16. `/git/github.com/LiGoldragon/skills/schema/assembly.schema:26-34` - classification: inspect.
    Observed: schema has no `skills.nota` path, but `ActiveRole { OutputIdentifier ModuleIdentifier IncludedModules RoleDescription RoleTargetSurfaces }` already supports ordered included modules.
    Replacement direction: likely reuse or refine `IncludedModules` as the V2 curated critical doctrine list. If V2 needs to distinguish role-body support modules from required doctrine, add a typed field rather than overloading generic included modules.

17. `/git/github.com/LiGoldragon/skills/manifests/active-outputs.nota:1-5`, `:75-84` - classification: inspect.
    Observed: role records already carry "ordered included module ids"; every current role includes only `[agent-output-protocol]`.
    Replacement direction: V2 role records need curated doctrine modules per role here, or a new adjacent manifest field. This is the likely source of truth for generated worker packets.

## Generated-Output and Stale-File Implications

- Existing `/home/li/primary/skills/skills.nota` is generated output under the current code: `/git/github.com/LiGoldragon/skills/src/assembly.rs:252-258` writes it, and `:381-384` expects it.
- Current `check-skills` fails on stale `skills/skills.nota` because rendered outputs call `RenderedOutput::check_file()` and emit `StaleOutput` on mismatch (`src/assembly.rs:1083-1120`; error text in `src/error.rs:83-90`).
- Current pruning does not remove `skills/skills.nota`: `WorkspacePruner::prune()` removes `.agents/skills`, `.claude/skills`, legacy extra paths, and stale role-inventory paths only (`src/assembly.rs:1210-1222`).
- Therefore, after removing the rendered job and expected-output entry, the existing workspace file will become an orphan unless a one-time deletion/migration path handles it. Options: delete `/home/li/primary/skills/skills.nota` in the consuming workspace as part of the V2 cutover, or add a generator tombstone/prune step for the retired path.

## Unknowns and Risks

- I did not deeply audit historical reports. A scoped `rg` found many report mentions of `skills.nota`; most appear historical rather than active runtime surfaces. A later context-maintenance pass can retire or ignore them by lane relevance.
- `/home/li/primary/INTENT.md` still references `skills/skills.nota`, but current settled direction may supersede that whole paragraph. Treat as an intent-maintenance target, not immediate generator work.
- Role packet doctrine curation needs a policy decision: reuse `IncludedModules` for required doctrine, or split role support modules from curated critical doctrine in the schema. The current schema can carry modules, but the name is broad.
- If `skills/skills.nota` is simply deleted from code without deleting the existing workspace file, local agents may still find and trust the stale file by path.

## Not Checked

- No tests were run; this was a read-only scouting pass.
- I did not inspect private scopes or `/home/li/primary/private-repos`.
- I did not enumerate every historical report reference beyond the scoped `rg` signal.
