---
name: knowledge-flow
description: A flow must be launched, named, claimed or reached, or a hook or sandbox seat run, with what is deployed today rather than with Flow as designed.
dependencies: [vision-flow]
---

The Flow source repository at commit
`ac6ab64193f3c4a43009db5a343284977bd33ea7` declares version `0.24.0`
in its `Cargo.toml` and has four workspace crates: `flow-defaults`,
`flow-nexus`, `flow`, and `flow-meta`. This describes the source tree;
it does not establish the installed client or running service version.

A read-only observation recorded in
`/home/li/primary/flows/6aa08d/log.md` on 2026-10-07 reports the
`/home/li/.local/bin/flow` client at `0.23.0`, the running
`flow-nexus.service` at `0.14.0`, and
`/home/li/.nix-profile/bin/flow-nexus` on `PATH` at `0.12.2`.
The retained record in
`/home/li/primary/flows/9ac67c/summary-flow-upgrade.md` identifies the
service binary as
`/nix/store/j689l77bmlfmgc6ichksrqnnmdnma8ig-flow-0.14.0/bin/flow-nexus`.
These are dated observations, not current runtime proof. The historical
corpus record at
`/home/li/private-repos/flow-evidence/42265e/fable-restart-context/sources/flows/bad807/reports/ethos-nexus-corpus.md:8709`
lists ordinary and meta sockets at
`/run/user/1001/flow/flow.sock` and
`/run/user/1001/flow/flow-meta.sock`; it is not a current endpoint
witness.

The read-root witness at
`/home/li/primary/flows/41fa34/reports/curriculum-read-root-witness-2026-10-09.md`
records that `readlink -f /home/li/.nix-profile/bin/curriculum`
resolved to the installed wrapper, which exports these absolute source
roots:
`/git/github.com/LiGoldragon/psyche-skills/skills`,
`/git/github.com/LiGoldragon/mind-skills/skills`, and
`/git/github.com/LiGoldragon/field-skills/skills`. Its recorded
read-only request `ResolveSkills.[ spirit ]` returned
`ResolvedSkills.[ compensation-behavior compensation-correction
knowledge-vocabulary compensation-book-distillation spirit ]` through
the local Nexus. The record does not independently inspect the live
Nexus process configuration. Curriculum's
`/git/github.com/LiGoldragon/Curriculum/ARCHITECTURE.md` describes the
authored repositories and generated harness trees; the full
source-root-to-five-tree runtime path is an inference from that
architecture and wrapper configuration.

Primary's native launcher source resolves selected skill roots through
`curriculum ResolveSkills.[ ... ]`. The Codex launcher reads resolved
bodies from `.agents/skills` into its first prompt. The Claude launcher
checks `.claude/skills/<name>/SKILL.md` and requests skills through
Claude's native slash-skill prompts. The retained 2026-10-07 launch
report at
`/home/li/private-repos/flow-evidence/0c85a3/launch-witnesses.md`
records a Claude Psyche.Tertiary transcript with all 18 generated
`.claude/skills` bodies and a Codex Mind.Tertiary first prompt with all
18 `.agents/skills` bodies. Its launchers were from checkout `928aed`.
The Codex launcher checksum was
`03004fccf89aad2e053e955f5f4926ecbcd7ee8eb1e335bd2b6ed0aca22bf234`.
The report records the Tertiary Herdr pane/session binding and accepted
first answer. These profile-specific native-launch witnesses do not
validate a FlowStart request or hook, qualify a Mind.Primary launch,
replacement, or retirement, or establish a deployed Flow 0.24 route.

Before launching, naming, claiming, reaching, or reporting a Flow, read
the matching deployed source and obtain the target's explicit response
through the current ordinary or meta socket. Do not infer protocol,
caller identity, store state, or runtime bindings from a source version
or client path.
