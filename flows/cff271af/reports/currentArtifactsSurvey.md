# Current Artifacts Survey

Survey of four artifacts for the design flow to build on.

## 1. Software-Design Skill

**Status: does not exist.**

No file matching `*software-design*` or `*software_design*` exists under `/git/github.com/LiGoldragon/Curriculum/skills/`. No manifest entry in `active-outputs.dotos` references it. No deployed copy exists in `.claude/skills/`, `.agents/`, `.codex/`, or `.pi/`.

Method: `find` and `grep` over the Curriculum skills directory, manifest, and all deployment trees.

Note: a `design.md` skill exists in the Curriculum (description: "Create a design canvas"), but it is the Artifact design canvas skill, not a software-design skill.

## 2. Nexus Skill and Nexus-Rationale Skill

### nexus.md

Authored source: `/git/github.com/LiGoldragon/Curriculum/skills/nexus.md`

Frontmatter:
```yaml
description: A daemon with privileged and ordinary sockets, CLI clients, and binary signal contracts is being designed, built, or changed.
dependencies: []
```

Body sections: The Nexus (repo/binary naming), The daemon (typed store, Configure boot, sema database), Signal (rkyv binary archives, length-prefixed frames, typed refusals), The CLIs (text-to-Signal boundary, single positional argument), The wire type repos (closed vocabulary, verb-form operations, round-trip examples), Traits first (ontology-first, trait pass before bodies, identity is trait-borne), No free functions (`fn main()` is the only one), How nexuses fit together (push subscriptions, no polling, no distributed rollback, one capability per Nexus).

Manifest entry: `Skill.{nexus nexus Architecture Topic [AgentsSkill ClaudeSkill]}`

Deployed copy: `/home/li/primary/.claude/skills/nexus/SKILL.md`

**Deployed body matches authored source exactly.** Frontmatter differs only as expected by the generator: deployed adds `name: nexus`, drops `dependencies: []`.

### nexus-rationale.md

Authored source: `/git/github.com/LiGoldragon/Curriculum/skills/nexus-rationale.md`

Frontmatter:
```yaml
description: A Nexus is being discussed with the living psyche and the reasoning behind its shape is needed.
dependencies: []
```

Body (four paragraphs): independent Nexuses exchanging signal, coarse grain rationale (no compiler partial-replacement today), heart/body analogy for Nexus/Core naming, meta socket as root-user analogy, pure-signal clients because textualizing inside the Nexus destroys simplicity, CLI as bootstrap shim.

Manifest entry: `Skill.{nexus-rationale nexus-rationale Architecture Topic [AgentsSkill ClaudeSkill]}`

Deployed copy: `/home/li/primary/.claude/skills/nexus-rationale/SKILL.md`

**Deployed body matches authored source exactly.** Same frontmatter transformation as nexus.

Method: direct file reads of authored sources and deployed copies; byte comparison of body text.

## 3. Datom Library

**Status: exists and is actively developed.**

Repository: `/git/github.com/LiGoldragon/datom`

Rust library crate, v0.1.0, edition 2024, MSRV 1.85. Self-described as "pure positional typed data on the published Protos substrate." Single external dependency: `protos` (pinned by git rev `bfea114c`).

### Structure

```
datom/
  Cargo.toml, Cargo.lock, flake.nix, flake.lock
  rust-toolchain.toml, .gitignore
  README.md, AGENTS.md
  src/
    lib.rs        -- re-exports
    datom.rs      -- all types and traits
  tests/
    substrate.rs  -- six substantive round-trip tests
```

### Public surface

Concrete models: `Report`, `Entry`, `Group`, `TagList`, `Text`, `InterimNote`.
Text carriers: `ReportText`, `InterimNoteText` (implement Protos `Realize`).
Evidence wrappers: `Realized<T>`, `Projected<T>`, `DatomEvidence`.
Traits: `EvidencedRealizing`, `EvidencedTextualizing`, `EvidenceObserving`, `RealizationViewing`, `ProjectionViewing`.
Errors: `DatomFault`, `DatomProblem` (Shape, Head, Position, ExtraPosition, MissingPosition, AmbiguousMapPair, Protos(WalkFault)).

### Build state

`target/` directory exists with `debug/` build artifacts. The crate has been compiled successfully. Rust toolchain pinned to 1.85.0.

### What is planned but unbuilt

- Structured string meaning: explicitly deferred per README to `structuredStringType.md` and bead `primary-xqb.8.5`.
- Map keys containing dots, and delimited keys followed by `.`: deliberately unsupported pending a psyche ruling; return `DatomFault`.
- No TODO files or empty module stubs found; the codebase is complete for its current scope.

### Design claims from documents

- Datom does not generate Rust (that belongs to Ethos). (README)
- Canonical text is a block projection, not preservation of original whitespace. (AGENTS.md)
- Parenthesis string carrier is the canonical output form; curly-quoted form is accepted as input only. (AGENTS.md)
- Status: "active substrate dialect", tracked by bead `primary-xqb.8.14`. (AGENTS.md)

Method: directory listing, file reads of Cargo.toml, src/lib.rs, src/datom.rs, tests/substrate.rs, README.md, AGENTS.md; `ls target/` for build state.

## 4. Ethos-Monolith Nexus

**Status: exists; scaffold with one working dialect; generator implementation is a later phase.**

Repository: `/git/github.com/LiGoldragon/ethos-monolith` (also at `/home/li/primary/repos/ethos-monolith/`)

Rust library crate, v0.2.0, edition 2024, MSRV 1.89. Self-described as "Reads Ethos text, emits Rust (signal.rs, nexus.rs, sema.rs) per component."

Note: despite the Nexus naming conventions in the nexus skill, ethos-monolith is a code generator library, not a daemon. The term "monolith" refers to the Ethos language, not the daemon pattern. It reads `.ethos` source files and emits three Rust artifacts per Nexus component. Consumers commit the emitted Rust; they never depend on this crate at build or runtime.

### Structure

```
ethos-monolith/
  Cargo.toml, Cargo.lock, flake.nix, flake.lock
  ARCHITECTURE.md, README.md, CLAUDE.md, AGENTS.md, .gitignore
  src/
    lib.rs               -- re-exports build, fixture, generate
    build.rs             -- CargoEthosSourceMetadata, GeneratedArtifact, BuildError
    generate.rs          -- ComponentGeneration, GeneratedComponent (emission boundary)
    fixture/
      mod.rs             -- Interface dialect: bidirectional Protos walk
      generated.rs       -- committed Rust projection of the Interface fixture
  fixtures/
    psyche/
      interface.ethos    -- the Interface slice fixture
  tests/
    generate.rs          -- ComponentGeneration, GeneratedComponent tests
    interface_fixture.rs -- round-trip equality, walk evidence, freshness
    architecture_guards.rs -- architecture enforcement
  checks/
    fixtures/
      architecture-guards/ -- guard test inputs
```

### Three implemented modules

1. **build** -- `CargoEthosSourceMetadata` (Cargo `links` discovery), `GeneratedArtifact` (path + content, staleness check, atomic `.pending` write), `BuildError`. Fully built and tested.

2. **generate** -- `ComponentGeneration` (source + output directory binding, derived file paths for `signal.ethos`/`nexus.ethos`/`sema.ethos` to `signal.rs`/`nexus.rs`/`sema.rs`) and `GeneratedComponent` (three-artifact carrier). The emission boundary types are complete; the generator implementation is declared "a later phase."

3. **fixture** -- Fully working bidirectional dialect for the Interface Ethos format (the psyche component's signal contract). Realizes `.ethos` to typed Rust structs; textualizes back. The committed `generated.rs` is checked for freshness by tests. This is the most substantial code in the repo.

### Build state

Multiple `.rlib` files in `target/debug/deps/`. Rustdoc output in `target/doc/ethos_monolith/`. The Nix flake is present. Gate: `nix flake check -L`.

Recent commits focus on architecture guard tests and Ethos generic/ZST layout rules -- structural law enforcement, not the main generator.

### What is planned but unbuilt

The central purpose -- reading `.ethos` files and writing `signal.rs`, `nexus.rs`, `sema.rs` -- is not yet implemented. The `generate.rs` module doc says: "The generator implementation is supplied by a later phase; this module owns the emission boundary and its types." AGENTS.md echoes: "Current state: implementation scaffold; generation remains a later phase."

The Interface fixture dialect covers only the `Interface` section shape, not `signal.ethos`, `nexus.ethos`, or `sema.ethos` in full.

### Related repositories in the ecosystem

Found at `/git/github.com/LiGoldragon/`:
- `ethos-engine` -- the Ethos parser/engine
- `signal-ethos` -- signal-level Ethos definitions
- `spirit-ethos` -- spirit-level Ethos definitions
- `tree-sitter-ethos` -- grammar for syntax highlighting/tooling
- `protos` -- the structural primitive datom and ethos-monolith both walk

### Psyche references

No psyche file mentions `ethos-monolith` by repository name. The Nexus concept is ruled in `psyche-raw/Vision/nexus.md` (2026-08-19, flow `e06e4c07`). Ethos language design is covered across several psyche-raw entries: `ethosDotosDivisionAndHelp.md`, `ethosNamespaces.md`, `ethosNonRepetitionLaw.md`, `workingSpiritNewEthosSyntax.md`, `colonFormTransformerSyntax.md`.

Method: directory listing, file reads of Cargo.toml, src/*.rs, ARCHITECTURE.md, README.md, AGENTS.md; `ls target/` for build state; `grep -r ethos-monolith` over psyche directories; `ls` of `/git/github.com/LiGoldragon/` for related repos.

## Sources

- `/git/github.com/LiGoldragon/Curriculum/skills/nexus.md` -- code read, full text
- `/git/github.com/LiGoldragon/Curriculum/skills/nexus-rationale.md` -- code read, full text
- `/git/github.com/LiGoldragon/Curriculum/skills/` -- directory listing for software-design search
- `/home/li/primary/manifests/active-outputs.dotos` -- code read
- `/home/li/primary/.claude/skills/nexus/SKILL.md` -- code read for comparison
- `/home/li/primary/.claude/skills/nexus-rationale/SKILL.md` -- code read for comparison
- `/git/github.com/LiGoldragon/datom/` -- directory listing, code reads of Cargo.toml, src/lib.rs, src/datom.rs, tests/substrate.rs, README.md, AGENTS.md; probe of target/
- `/git/github.com/LiGoldragon/ethos-monolith/` -- directory listing, code reads of Cargo.toml, src/lib.rs, src/build.rs, src/generate.rs, src/fixture/mod.rs, ARCHITECTURE.md, README.md, AGENTS.md; probe of target/
- `/home/li/primary/psyche-raw/Vision/nexus.md` -- code read for psyche references
- `/home/li/primary/SKILL_VARIABLES.md` -- code read for repository paths
