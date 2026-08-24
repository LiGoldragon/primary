# Curriculum Nix boundary

## Finding

The living's causal hypothesis is substantially correct, with one important qualification: curriculum-only edits do not rebuild third-party Rust dependencies, but they do invalidate several derivations that compile or check Curriculum's own Rust crate.

The Rust engine does not embed the curriculum. It already reads Markdown and DOTOS at runtime. Nix creates the unnecessary coupling by feeding one combined source tree to both the Rust build and the runtime generator.

```text
combined cleanSource: .rs + .md + .dotos
├── dependency artifacts ── Crane dummy source ── stable on data edits
├── skills package ───────────────── cargo build ─┐
├── build check ──────────────────── cargo build  │ invalidated by data
├── test check ───────────────────── cargo test   │
├── clippy check ─────────────────── cargo clippy │
├── fmt check ────────────────────── cargo fmt ───┘
└── SKILLS_SOURCE_ROOT ── runtime data ── generator checks
```

The reported large check is therefore plausibly several fresh compilations of the local crate, not a recompilation of its entire dependency closure.

No automatic edit-trigger was found in the Curriculum repository. A local Curriculum edit also does not immediately alter Primary: Primary consumes a locked GitHub revision, so the change reaches it only through a lock update or explicit override.

## Mechanical correction

Keep the existing typed runtime handoff, but give its two sides different Nix inputs:

```text
engineSource
  Cargo.toml, Cargo.lock, src/, tests/, Rust build configuration
  └── skills engine package

curriculumData
  authored skill modules and the ruled runtime control data
  └── immutable source_root read by the engine

consumer workspace
  └── generated/checkable harness files
```

The concrete change is:

1. Replace the single combined `cleanSource` with an engine-only source and a data-only source/output.
2. Give both `buildDepsOnly` and every Rust build/test/lint derivation only the engine source.
3. Give the generator apps the cached engine binary plus the data output; set `SKILLS_SOURCE_ROOT` and default request paths to the data output.
4. Update Primary and every real consumer to use that explicit app/data boundary, update their Curriculum pins, regenerate all consumer surfaces, and remove the combined-source invocation rather than retaining a compatibility path.
5. Keep custom source roots as the generator's intentional typed input, not as a legacy fallback.

After this split, a Markdown-only edit changes the data output, app wrapper, and data-sensitive generator checks. It does not change the engine package, build, test, Clippy, or formatting derivation identities; those remain cached.

## Proof required in the realization round

- Existing Rust generation tests pass using their separate temporary runtime source roots.
- The code-only engine package builds through the repository's durable Nix gate.
- Across a controlled Markdown-only change, the engine package derivation/output path remains identical while the data output path changes.
- The cached engine renders the changed data in visualization/generation.
- Primary updates its pin, regenerates every consumer surface, and its generated-output check passes.
- A full Curriculum check witnesses that only data-sensitive checks rebuild after the data-only change.

No such change or build was performed in this investigation round.

## Architecture exposed by the trace

The mechanical separation is clear, but the terminal contents of `curriculumData` are not fully settled by the current implementation.

Recent written psyche says generation should discover the skills that are present, subagent roles belong in their own file, and the elaborate manifest-driven phase is unwanted. Current code and architecture still use `manifests/active-outputs.dotos` and related manifest machinery. Splitting the current tree mechanically would cure recompilation while preserving architecture the living has already called dead machinery.

Two concrete artifacts also lack a settled owner:

- Primary has a divergent local `manifests/active-outputs.dotos`, but its normal wrapper does not use it.
- Curriculum tracks `skills/generated-role-outputs.dotos`, although the engine defines that path as consumer-generated output rather than source data.

The best end-shape should therefore establish the data anatomy before implementation: present authored skill files as the skill set; roles in their separately owned data; setup-specific variables in the consumer workspace; no generated consumer inventory in Curriculum; and no activation manifest unless the living rules a remaining purpose for one.

## Observations, hypotheses, and unknowns

Observed: the combined Nix source changes Rust-bearing derivations on data edits; dependencies use a separate dummy source; the engine reads curriculum data at runtime; Primary is a locked consumer.

Hypothesized: the repeated local-crate compilation explains the perceived giant check cost. No timed post-edit build was run, so the relative wall-clock contribution is not measured.

Unknown: what external workflow invokes the full check after edits; whether Primary's local manifest is intentional or stale; whether any consumers exist outside checked-out repositories; and the final public name/stability promise of the data output.

## Sources

- `flows/01a035d3/witnesses/curriculumNixDerivations.md`
- `flows/01a035d3/witnesses/curriculumRuntimeBoundary.md`
- `flows/01a035d3/witnesses/primaryCurriculumConsumer.md`
- `/git/github.com/LiGoldragon/Curriculum/flake.nix`
- `/git/github.com/LiGoldragon/Curriculum/src/assembly.rs`
- `/git/github.com/LiGoldragon/Curriculum/src/schema/assembly.rs`
- `/git/github.com/LiGoldragon/Curriculum/tests/generation.rs`
- `/home/li/primary/flake.nix`
- `/home/li/primary/flake.lock`
- `psyche-raw/Vision/skillsRepoSourceOnly.md`
- `psyche-raw/Vision/skillsRepository.md`
- `psyche-raw/Vision/entryFiles.md`
- `Vision/datom.md`
- flow `15b67974`
- flow `68512643`
- flow `358f143a`
- flow `e06e4c07`
