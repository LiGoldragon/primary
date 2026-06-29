# SkillEditor Directive Slash-Down Acceptance

Task: continue skills slash-down from source first, remove `workspace-update-report` and `language-design`, reduce suspect `structural-forms`, reconcile generated primary runtime surfaces, validate, commit, and push.

Scope consulted:

- `/git/github.com/LiGoldragon/skills/AGENTS.md`
- `/git/github.com/LiGoldragon/skills/skills.md`
- `/git/github.com/LiGoldragon/skills/manifests/{active-outputs.nota,module-dependencies.nota,skills-roster.nota}`
- `/git/github.com/LiGoldragon/skills/modules/{structural-forms,report-naming,stt-interpreter,context-maintenance,architecture-editor,beads}/full.md`
- generated primary surfaces under `.agents/skills/` and `.claude/skills/`

Changed source files in `LiGoldragon/skills`:

- `manifests/active-outputs.nota`: removed `language-design` and `workspace-update-report`; shortened `structural-forms` description.
- `manifests/module-dependencies.nota`: removed dependency-index entries for deleted skills.
- `manifests/skills-roster.nota`: removed roster entries for deleted skills; shortened `structural-forms` description.
- `modules/language-design/full.md`: deleted.
- `modules/workspace-update-report/full.md`: deleted.
- `modules/structural-forms/full.md`: reduced to data-first grammar discipline and removed stale concrete macro vocabulary.
- `modules/report-naming/full.md`: shortened and removed the obsolete `workspace-update-report` reference and local path example.
- `modules/stt-interpreter/full.md`: removed the `language-design` string from the `aski` row so retired skill names do not remain in generated skill surfaces.
- `tests/generation.rs`: updated expected active skill/module counts from 66/76 to 64/74.

Changed generated files in primary:

- Deleted `.agents/skills/language-design/SKILL.md`
- Deleted `.agents/skills/workspace-update-report/SKILL.md`
- Deleted `.claude/skills/language-design/SKILL.md`
- Deleted `.claude/skills/workspace-update-report/SKILL.md`
- Updated `.agents/skills/{structural-forms,report-naming,stt-interpreter}/SKILL.md`
- Updated `.claude/skills/{structural-forms,report-naming,stt-interpreter}/SKILL.md`

Observations:

- `workspace-update-report` and `language-design` were fully removed from source modules, active manifest, module dependency index, compatibility roster, and generated runtime skill directories. No deprecation stubs were left.
- `structural-forms` remains active, but only as minimal current operational discipline: data-first syntax, positional vs named forms, syntax dimensions, orthogonality, and grammar/AST/example/test synchronization.
- Prior audit blockers for `context-maintenance`, `architecture-editor`, and `beads` were already fixed in source and generated copies; targeted scans found no `report`, `Spirit`, `transitional until Persona-mind`, `roadmap`, or `planned` in those touched surfaces.
- Remaining question: should `structural-forms` stay as this generic grammar discipline, or should psyche supply the currently accepted concrete structural-form vocabulary before any pipe/generic/stream/family rules return?

Validation commands and results:

- `SKILLS_SOURCE_ROOT=$PWD SKILLS_WORKSPACE_ROOT=/home/li/primary cargo run -- skills-generate.nota`: passed; regenerated primary surfaces and pruned retired skill directories.
- `SKILLS_SOURCE_ROOT=$PWD SKILLS_WORKSPACE_ROOT=/home/li/primary cargo run -- skills-check.nota`: passed before and after commits.
- `cargo test` in `LiGoldragon/skills`: passed, 16 integration tests.
- Runtime absence check for retired skill directories: passed.
- `rg -n "workspace-update-report|language-design"` over active skills source, manifests, roles, generated skill surfaces, and generated role inventory: no matches.
- Targeted scan over `context-maintenance`, `architecture-editor`, and `beads`: no prior-blocker matches.
- Targeted scan over `structural-forms`: no stale macro/provenance/report/path matches.
- Source frontmatter scan over touched source modules: no harness frontmatter fences.
- Heading uniqueness check over touched source modules: passed.
- Manifest/index source-path resolution check: passed.

Commits and push:

- `LiGoldragon/skills`: `e1a40adbd0d163a9f7ad956d8de5d7d0ad05d589` — `skills: remove retired skills from generation`; pushed, `main@origin` matches `main`.
- `primary`: `57adbaa3d151ea1568dbea9715b1701ae489ee56` — `skills: reconcile retired skill surfaces`; pushed, `main@origin` matches `main`.

Residual working-copy state:

- `LiGoldragon/skills`: clean.
- `primary`: existing unrelated `agent-outputs/HighCountSkillBatchAuditBlockers/SkillEditor-Acceptance.md` remains uncommitted; this acceptance output file is also an uncommitted worker artifact.

Blockers: none for the completed removal/reconciliation. The only follow-up is the psyche question about whether `structural-forms` should remain generic or be rebuilt from accepted concrete vocabulary.
