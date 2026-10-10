# Curriculum read-root witness — 2026-10-09

This is a retained record of commands already observed in this flow. It is
not a new probe.

## Observed command results

`readlink -f /home/li/.nix-profile/bin/curriculum` resolved to the installed
Curriculum wrapper. Reading that wrapper showed these exported source roots:

- `/git/github.com/LiGoldragon/psyche-skills/skills`
- `/git/github.com/LiGoldragon/mind-skills/skills`
- `/git/github.com/LiGoldragon/field-skills/skills`

The already-run read-only command
`curriculum 'ResolveSkills.[ spirit ]'` returned:

```
ResolvedSkills.[ compensation-behavior compensation-correction
knowledge-vocabulary compensation-book-distillation spirit ]
```

The installed wrapper directs requests to the local Curriculum Nexus. The
source statement supporting authored roots to generated trees is
`/git/github.com/LiGoldragon/Curriculum/ARCHITECTURE.md`: it describes the
three authored repositories, the Nexus reread, and generated harness trees.

This records wrapper configuration plus a successful read-only Nexus resolve.
It does not independently inspect the live Nexus process configuration.
