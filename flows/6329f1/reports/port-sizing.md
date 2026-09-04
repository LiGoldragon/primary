# Port sizing: pre-train consumers

Report for flow 6329f1. Sized from code inspection, not from attempting the port.

## 1. claude-answers

**Path**: `/git/github.com/LiGoldragon/claude-answers`
**Remote**: `git@github.com:LiGoldragon/claude-answers.git`
**Branch**: detached HEAD; main present. **Clean**.

**What it is**: A CLI tool that reads Claude Code session transcripts and recalls the interactive questions, chosen options, and typed notes from them. It accepts one inline Datomic query (Latest, All, Session, File, Grep) and prints matching answers. 537 lines of Rust across 5 source files, plus 176 lines of ethos-contract test.

**API surface used (old crates)**:

| Crate | Trait / type | Where | Count |
|---|---|---|---|
| protos | `Portion`, `Separator`, `StructuralEnclosure` | src/query.rs | 28 refs |
| datomic | `Datomic`, `DatomicString`, `PortionBuilding`, `PortionViewing`, `Text`, `TextEdge`, `Fault`, `FaultProblem`, `UnrepresentableString` | src/query.rs, src/error.rs | 46 refs |
| datomic | `embody` method (from `Datomic` trait) | src/query.rs:59, src/query.rs:176 | 2 impls |
| ethos-zero | `FileReader`, `Manifest`, `File`, `Capability`, `TypeDeclaration`, `TypeExpression`, `VariantPayload` | tests/ethos_contract.rs | 6 refs (dev-only) |

**Ethos file** (verbatim):
```
Schema.{0 1 0}
[]
Types.[
  Query.[
    Latest
    All
    Session.String
    File.String
    Grep.{selection.Box<Query> needle.String}
  ]
]
Kinds.[Datomic.{embody.[Result<Self Fault>] portion.[Portion] textualize.[Text<Self>]}]
Associations.[]
```

Root style: `Schema.{0 1 0}` — the old root, not `Interface.{}` or `Signal.{}`.

**Tests**: all 17 pass (3 ethos, 10 query, 4 transcript).

**Deployment**: CriomOS-home flake.nix pins it as an input. CriomOS flake.lock references it transitively. Redeployment: bump CriomOS-home and CriomOS flake inputs.

**Psyche**: no psyche record found under primary mentioning claude-answers.

**Estimate**: **3 h** for a critical writer.
- Port `Portion` → `Protoform`, `Separator`/`StructuralEnclosure` → new structural API, `Datomic` trait → new datom embodiment/textualization traits, `embody` → `incorporate`, rename the Cargo dependency from `datomic` to `datomic` (same URL, new rev), bump protos rev.
- The ethos file must change from `Schema.{}` root to `Signal.{}` and its `Kinds` section must use the new capability names.
- The ethos-zero dev-dependency test must track the new `ethos-zero` API (FileReader → whatever replaces it).
- **Riskiest part**: the `Datomic` trait implementations in query.rs (two non-trivial `embody` impls with manual portion traversal logic, lines 59–214) must be rewritten to the new `Conceptual::conceive` or equivalent datom API.

## 2. curriculum-deploy

**Path**: `/git/github.com/LiGoldragon/curriculum-deploy`
**Remote**: `git@github.com:LiGoldragon/curriculum-deploy`
**Branch**: detached HEAD; main present. **Clean**.

**What it is**: The runtime that projects a Curriculum data checkout into a consumer workspace. It generates skill companions, role packets, and cleanup inventories. Accepts one inline Datom configuration object. 1228 lines of Rust across 4 source files. Used by primary's flake.nix as the `generate-skills` runtime, run as `nix run .#generate-skills 'CurriculumRequest.{…}'`.

**API surface used (old crates)**:

| Crate | Trait / type | Where | Count |
|---|---|---|---|
| datom (old URL) | `DatomRealizing`, `DatomTextualizing`, `DatomRoot`, `DatomText`, `DatomFault`, `DatomProblem`, `PositionAdvancing`, `RecordPosition` | src/runtime.rs, src/roles.rs | 148 refs |
| protos | `Block`, `Head`, `Headed`, `Realize`, `RealizeScope`, `RealizeScoping`, `Shape`, `ShapeDefined`, `SourceText`, `TextualizeScope`, `TextualizeScoping` | src/runtime.rs, src/roles.rs | 89 refs |

**Ethos file**: none.

**Tests**: all 3 pass (1 unit + 2 integration; 1 ignored — requires external Curriculum data).

**Deployment**: primary flake.nix pins `curriculum-deploy/74581e74` and builds the `generate-skills` and `check-skills` apps from it. Not in CriomOS/CriomOS-home directly. Redeployment: bump primary's flake input; regenerate skills tonight with `nix run .#generate-skills`.

**Psyche**: no psyche record directly about curriculum-deploy as a Rust component. The curriculum repository itself is discussed as a data input.

**Estimate**: **6 h** for a critical writer.
- This is the heaviest consumer: 1228 lines of code, 237 total references to old APIs across two files (runtime.rs and roles.rs). Every DatomRealizing/DatomTextualizing impl must be rewritten to the new API. Every protos Shape/Block/Realize/Headed reference must become the new Protoform/Structural/Conceptual API.
- The `datom` Cargo dependency URL must change from the retired `datom` to `datomic`.
- **Riskiest part**: roles.rs (708 lines) has deep, hand-written DatomRealizing and DatomTextualizing implementations for the full role-packet grammar (RolePacket, Roles, 30+ struct/enum variants with nested datom traversal). This is the largest manual datom consumer in the estate.

## 3. signal-spirit (+ meta-signal-spirit)

### signal-spirit

**Path**: `/git/github.com/LiGoldragon/signal-spirit`
**Remote**: `git@github.com:LiGoldragon/signal-spirit.git`
**Branch**: detached HEAD at d3690ae; main at d1a9f2fd. **Clean**.

**What it is**: The Signal contract crate for the ordinary spirit surface. It contains the schema (spirit.schema) and build-time code generation that produces the typed Rust structs and rkyv-derived wire types for the spirit daemon's 21 ordinary roots. 566 lines of generated Rust. It pins protos for the `Input`, `Output`, `Refusal`, `Stream` marker traits.

**API surface used**:

| Crate | Trait / type | Where | Count |
|---|---|---|---|
| protos | `Input`, `Output`, `Refusal`, `Stream` (marker traits only) | src/schema/spirit/generated.rs | 17 impls |

No hand-written protos usage outside generated code. The build.rs generates from schema-rust + sema-translator + core-nomos. No datomic or ethos-zero dependency.

**Schema file root**: `Interface.{1 0 0}` (spirit.schema).

### meta-signal-spirit

**Path**: `/git/github.com/LiGoldragon/meta-signal-spirit`
**Remote**: `git@github.com:LiGoldragon/meta-signal-spirit.git`
**Branch**: detached HEAD at ed7ce82; main at 922f8a0e. **Clean**.

**What it is**: The MetaSignal contract crate for privileged spirit lifecycle and policy. It imports signal-spirit types and defines the meta-surface (Configure, Import, ObserveHead, ObserveHeadObject). 128 lines of generated Rust.

**API surface used**:

| Crate | Trait / type | Where | Count |
|---|---|---|---|
| protos | `Input`, `Output` (marker traits only) | src/schema/meta/generated.rs | 9 impls |

No hand-written protos usage. No datomic or ethos-zero dependency.

**Ethos files**: neither has .ethos files (they have .schema files instead).

**Tests**: signal-spirit — 3 pass (0 unit, 3 integration boundary). meta-signal-spirit — 3 pass (0 unit, 3 authority-sealed).

**Deployment**: both in CriomOS flake.lock as source inputs (for the spirit Nix build). The spirit nexus pins signal-spirit@b37fc96 and meta-signal-spirit@009cb6c; both are behind their respective mains (signal-spirit main is d1a9f2fd, meta-signal-spirit main is 922f8a0e). Redeployment: bump the spirit nexus's Cargo.toml pins, then bump CriomOS and CriomOS-home flake inputs for spirit.

**Psyche**: no psyche record mentioning signal-spirit or meta-signal-spirit by name.

**Estimate**: **1.5 h** for both (combined), critical writer.
- The port is mechanical: bump the protos rev in both Cargo.toml files. The `Input`, `Output`, `Refusal`, `Stream` marker traits are in the new protos API (they are the Signal-layer markers). The generated code is regenerated by `build.rs` from schema-rust; if the marker trait paths or signatures changed, the codegen templates in schema-rust (already updated on main) handle it.
- **Riskiest part**: the build.rs codegen pipeline (schema-rust + sema-translator + core-nomos) must produce valid code with the new protos. If any of those build-dependencies changed their output for the new marker traits, the generated.rs will drift and fail the checked-in comparison. This should be caught immediately by `cargo test`.

## 4. spirit (the nexus)

**Path**: `/git/github.com/LiGoldragon/spirit`
**Remote**: `git@github.com:LiGoldragon/spirit.git`
**Branch**: detached HEAD at 4711fb3; main present. **Dirty**: 18 modified/added files across src/, tests/, scripts/.

**What it is**: The durable intent service (spirit 0.27.0). A daemon with working and meta sockets, NOTA CLI entry points, SEMA storage, guardian admission via an external LLM judge, criome cluster authorization, and mirror shipping. The largest consumer in this set. Consumes protos only transitively through signal-spirit and meta-signal-spirit; it has no direct protos, datomic, or ethos-zero dependency.

**API surface used (via signal-spirit/meta-signal-spirit)**:

| Crate | Usage | Where |
|---|---|---|
| protos (transitive) | `Input`, `Output`, `Refusal`, `Stream` markers on signal-spirit/meta-signal-spirit types | consumed via the generated wire types, not directly |

Spirit's own code does not import or name any protos, datomic, or ethos-zero type. It consumes signal-spirit and meta-signal-spirit as opaque typed wire contracts.

**Ethos files** (2, in schema/):
- `sema.ethos`: `Sema.{1 0 0}` root, psyche-authored sections 1–2, night-transcribed section 3 (pending psyche morning review). Defines StoredRecord, Migration, WriteInput/ReadInput/WriteOutput/ReadOutput decision types.
- `nexus.ethos`: `Nexus.{1 0 0}` root, psyche-authored sections 1–2, night-transcribed section 3 (pending psyche morning review). Defines AdmissionDecision, GuardianDecision, LifecycleDecision, CommandSemaWrite, NexusEffectCommand (12 variants), NexusEffectResult (14 variants), StashRequest/StashResult/GuardianVerdict.

Root style: `Sema.{1 0 0}` and `Nexus.{1 0 0}` — named nexus-scoped roots, not `Interface.{}` or `Schema.{}`.

**Tests**: not run (dirty tree, many feature-gated tests, complex nix integration). The detached HEAD suggests active work.

**Deployment**: CriomOS pins spirit@008d8ca0 in flake.nix; CriomOS-home follows. CriomOS runs a spirit-role-policy check; CriomOS-home runs a spirit-deployment check. Redeployment: bump CriomOS and CriomOS-home spirit input, rebuild.

**Psyche**: newest relevant record — flows/fd301d9a/vision/actorLibrary.md (2026-08-21):
> "persona-spirit? that is an abandonned repo. What is in there that isnt in spirit? Plus spirit is to be abandonned for psyche."

**Estimate**: **2 h** for a critical writer (port scope only — not the psyche-announced abandonment).
- Spirit itself needs only its signal-spirit and meta-signal-spirit Cargo pins bumped. The dirty working tree is a complication: those 18 modified files must be committed or stashed first, and the port must not conflict with whatever work is in progress.
- The .ethos files use named roots (Sema, Nexus), not the old Interface/Schema roots, so they do not need root-style changes for this port.
- **Riskiest part**: the dirty tree. Spirit has active uncommitted work across engine, config, store, trace, and multiple tests. The port must be coordinated with whoever owns that work-in-progress. The second risk is the transitive rebuild: spirit pulls ~30 crates; if signal-spirit or meta-signal-spirit change their generated type shapes (not just marker trait impls), spirit's compiled-against types break across the board.

## 5. core-logos (excluded)

Per Vision/ethosMonolith.md, core-logos belongs to the earlier three-nexus stack that is "kept, left in place, frozen." It pins protos@cdc74bd2 but is not directly in any Cargo.toml (only in lojix's Cargo.lock as a transitive dep, 4 references). Not in CriomOS or CriomOS-home flake.nix. **Not ported per the brief.**

## Sources

- Cargo.toml of each repository (dependency declarations and revisions)
- `git remote -v`, `git branch`, `git status --porcelain` in each repository
- `grep -rn` across src/ and tests/ for API trait/type names
- `find . -name '*.ethos'` and `cat` of each found file
- `nix develop --command cargo test` in each repository (all except spirit)
- CriomOS/flake.nix, CriomOS/flake.lock, CriomOS-home/flake.nix, CriomOS-home/flake.lock
- primary/flake.nix (curriculum-deploy reference)
- `grep -rn` across flows/*/vision/ and Vision/ for psyche records
- Vision/ethosMonolith.md (core-logos frozen status)
- Flow 6329f1 log.md design section (new API shapes)
