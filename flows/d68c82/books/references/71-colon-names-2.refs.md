# References: A context module is named kind:name

## Proposal 1 (psyche-context vision/context-modules.md)

- flows/d68c82/vision/context-modules.md — A colon between a context module's kind and its name (latest entry): colon between kind and name, visually clear, taught in basic training
- flows/d68c82/vision/context-modules.md — 2026-10-14, a separator between type and name: colon separates type from a hyphenated name; models trained to read it
- psyche-context origin main b938651, vision/context-modules.md: context lines are lines 66 and 68; the three lines land between them
- living's comment on the review: no psyche proposal was visible; this edition opens with it, each line its own green line
- witnessed 2026-10-18 (Field, /tmp/colon-skill-live-20261018-6uxf9dy6/report.json): Claude Code 2.1.294 loads .claude/skills/vision:book and completes /vision:book; Codex 0.158.0-alpha.9 loads it and completes $vision:book
- figure: drawn by the Illustrator (curriculum ComposeRole illustrator ClaudeAgent, Sonnet); arrow labels recoloured to the arrow grey for dark-mode contrast

## Proposal 2 (Curriculum src/registry.rs)

- Curriculum origin main 2ec2862: valid_id line 54 allows [a-z0-9-]; identity built at line 161 as format!("{kind}-{subject}"), checked at 197 (resolve_exact), split at 247 (describe), dependency IDs at 334
- Field witness: in Ethos a name before ':' means an import from that source (Topic.custom:Name, std:time:[ Instant ])
- not shown, change with the ID: src/startup.rs line 81 and 125-126 starts_with("spirit-")/("intent-"), line 164 its own [a-z0-9-] check; roles.datom module IDs
- the earlier kebab_name helper is dropped: no Nix name is built from a module today, so it had no caller

## Proposal 3 (curriculum-deploy src/runtime.rs)

- curriculum-deploy origin main 252729c: SkillTarget impl lines 170-183; outputs 325-341 join skill.name into .agents/skills, .claude/skills, .opencode/skills; clean_previous_skills 388-406
- catalog.rs names a skill by its flat file stem (kind-name); Field witness: OpenCode and the Agent Skills standard accept kebab names only

## Proposal 4 (mind-context knowledge/vocabulary.md)

- mind-context origin main d581978, knowledge/vocabulary.md lines 39 and 41 are the context lines
- Curriculum roles.datom: knowledge-vocabulary is in every general role's standing set
