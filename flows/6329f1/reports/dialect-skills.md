# Dialect skills report

Branch `DialectSkills` at `66dd3b7f` on `Curriculum`, pushed to origin.
Worktree: `/home/li/wt/github.com/LiGoldragon/Curriculum/Curriculum-DialectSkills-6329f1`.
Lock 639 held on the worktree.

Three skills drafted for living approval, not landed on main.

## Judgment calls

- **protos skill**: Listed all six delimiter pairs in one table with what each encloses in each dialect, since agents need to know which glyph to reach for. Included the four layers and the kind table because an agent touching protos needs the descent/ascent vocabulary. Did not include the protos.ethos declaration — too much internal detail for a skill; the table and the rules suffice.
- **datom skill**: Used the Person struct, vector, map, variant, and Meaning examples verbatim from Vision/datom.md. The CLI example uses the witnessed orchestrate reply. Showed the Datomic trait and the actualize/textualize call sites as the living requested ("datom and ethos should show some rust code"). Used `incorporate` and `datomize` as the capability names per the design spec; used `Corporal<Datom>` as the supertrait per the landed code.
- **ethos skill**: Used the Library example from the design spec (Record/Report), not from Vision/ethos.md (which had the not-yet-landed declaration), because the design spec's example aligns with what the code actually does. Signal example from the design spec. Showed target Rust beside every form per the ruling (ad19b1). The complex kind Streamable example is from the design spec. Imports use the colon separator per the witnessed ethos files. Listed intrinsics from the design spec.
- **Vocabulary**: Used "kind" everywhere, never "trait" except in Rust target examples. Used "position" for datom field locations. Used "structure" for protos textual units. Used "capability" for kind methods.
- **Dependencies**: protos has none. datom depends on protos. ethos depends on protos and datom.
- **Form**: Matched the existing Curriculum skills — YAML frontmatter with description and dependencies, terse imperative body, no skill variables needed (these skills describe languages, not installed tools).

## Full text

The corrected skills follow. Corrections applied: (1) protos parentheses row states the witnessed backslash escape; Corporal\<C\> row describes the kind correctly; Embodied is the bound. (2) datom Accepted example uses the vision's bare timestamp; Datomic Rust matches the code on main (`Corporal<Datom, Fault = Fault>`, `incorporate(concept: C)` by value, `textualize() -> protos::Text`); Decimal says “finite, point-mandatory” without claiming no exponent. (3) ethos Library/Signal examples spaced; Rust blocks show named structs with `pub`, compile-time assertion for associations, `impl datomic::Datomic` generated; struct example uses the actual Lock from the orchestrate signal.

### skills/protos.md

(verbatim copy of /home/li/wt/github.com/LiGoldragon/Curriculum/Curriculum-DialectSkills-6329f1/skills/protos.md)

### skills/datom.md

(verbatim copy of /home/li/wt/github.com/LiGoldragon/Curriculum/Curriculum-DialectSkills-6329f1/skills/datom.md)

### skills/ethos.md

(verbatim copy of /home/li/wt/github.com/LiGoldragon/Curriculum/Curriculum-DialectSkills-6329f1/skills/ethos.md)

## Sources

- Vision/protos.md, Vision/datom.md, Vision/ethos.md — distilled vision
- Intent/protosParsing.md — intent on parsing
- flows/e8c4cc61/vision/ethosFileAnatomy.md — the living's handwritten page
- flows/6329f1/log.md ## Design — the synthesis spec
- protos 56c683ec README and protos.ethos — landed code self-description
- datomic a27f9b8e README and datomic.ethos — landed code self-description
- ethos-zero 185f13a9 README, ethos-zero.ethos, signal.ethos — landed code self-description
- POC witness and final witness in flows/6329f1/reports — verbatim CLI output
