# References: A context module is named kind:name

## Proposal 1 (psyche-context vision/context-modules.md)

- flows/d68c82/vision/context-modules.md — A colon between a context module's kind and its name (latest entry): colon between kind and name, visually clear, taught in basic training
- flows/d68c82/vision/context-modules.md — 2026-10-14, a proposal checks the higher modules first; a separator between type and name: colon separates type from a hyphenated name; models trained to read it
- psyche-context at b938651, vision/context-modules.md line 66: the folder already gives the type (landed in 8bf1b25), so Proposal 1 does not restate it
- witnessed 2026-10-18 (Field, /tmp/colon-skill-live-20261018-6uxf9dy6/report.json): Claude Code 2.1.294 loads .claude/skills/vision:book and completes /vision:bo to /vision:book (project); Codex 0.158.0-alpha.9 loads it, shows book (vision) [Skill], completes $vision:book

## Proposal 2 (Curriculum src/registry.rs)

- Curriculum origin main 2ec2862: valid_id line 54 allows [a-z0-9-]; the identity is built at line 161 as format!("{kind}-{subject}") and split back at line 245 with split_once('-'); the older valid_name (~97, ~458) is only in the detached local checkout 73414b6
- Field witness: Nix store and derivation names refuse ':' ("illegal character"); no Nix name is built from a module today (curriculum-deploy and Primary flake.nix searched), so kebab_name has no caller yet
- not shown: src/startup.rs line 164 keeps its own [a-z0-9-] check and lines 81 starts_with("spirit-")/("intent-"); roles.datom IDs; both change with the ID

## Proposal 3 (curriculum-deploy src/runtime.rs)

- curriculum-deploy origin main 252729c: outputs (lines 325-341) joins skill.name into .agents/skills, .claude/skills, .opencode/skills; clean_previous_skills (388-406) removes folders the catalog does not define; catalog.rs names a skill by its flat file stem (kind-name)
- Field witness: OpenCode and the Agent Skills standard accept kebab names only; OpenCode frontmatter name stays skill.name

## Proposal 4 (mind-context knowledge/vocabulary.md)

- Curriculum origin main roles.datom: knowledge-vocabulary is in every general role's standing set; spirit-core is in every role but is psyche spirit

## Proposal 5 (mind-context inquiry/context-source-contracts.md)

- Field witness: in Ethos a name before ':' means an import from that source (Topic.custom:Name, std:time:[ Instant ])
