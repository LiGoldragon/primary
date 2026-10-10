# Capsule Is the Compilation Unit — 2026-08-01

Ruling from the psyche vision session, given in direct response to the
design-consistency audit's top finding: the 2026-07-23 dictation carried in
the protos-engine compilation
(`/git/github.com/LiGoldragon/protos-engine/design/ProtosEngine/ProtosEngineDesign-2026-07-29.md:423`,
"a capsule per namespace mirrors the file concept") contradicts the
2026-08-01 capsule-is-a-program ruling with no recorded supersession.

Agent text answered: the audit finding quoting "a capsule per namespace
mirrors the file concept."

Psyche ruling [psyche-verbatim]: "as we said, a capsule is now a program (or
a library) - what would correspond to the code needed to create a compiled
artifact in rust"

## Seated meaning

- **This supersedes the 2026-07-23 capsule-mirrors-file dictation.** A
  capsule does not correspond to a namespace or a source file.
- A capsule is the unit whose content yields one compiled artifact: a
  program or a library. The Rust analogue is the crate (bin or lib) — the
  code needed to create one compiled artifact.
- Composes with the 2026-08-01 rulings already seated
  (`threeLayerNamingAndNomosBootstrap-2026-08-01.md`): the capsule populates
  from encoded names via the registry; rendering it to text is a balanced
  distribution into reasonably sized files; imports/exports are derived
  views; file granularity carries no identity.
- The possible per-object sub-unit ("maybe there's a sub component here that
  deserves its own name") remains an open naming question, unchanged.
