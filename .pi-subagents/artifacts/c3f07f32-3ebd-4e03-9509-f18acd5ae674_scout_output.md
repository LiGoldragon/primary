## Observations

### Directly conflicting or weakening passages

- `modules/code-implementation/full.md:13`  
  > “Treat bare language tests as inner-loop evidence unless the repository names them as durable gates.”  
  This explicitly permits bare local language tests.

- `modules/code-implementation-core/full.md:52-56`  
  > “durable test evidence is owned by Nix when the repo exposes it…”  
  > “Bare language test commands are inner-loop evidence unless the repo says otherwise.”  
  This weakens the requested universal ban by allowing an exception.

- `roles/general-code-implementer/full.md:33-36`  
  > “Run the narrowest meaningful tests first…”  
  It does not constrain “tests” to Nix and therefore can lead to `cargo test`.

- `modules/versioning/full.md:26-28`  
  > “run the relevant tests”  
  Unqualified test execution is prescribed during closeout.

- `modules/main-feature-integration/full.md:13-17,24-25`  
  > “Test the branch family together…”  
  > “rerun the relevant tests.”  
  Again, no Nix-only qualification.

- `roles/rust-auditor/full.md:30-32`  
  > “Run or inspect the Rust checks named by the implementer.”  
  “Checks” is safer than “tests,” but the role does not prohibit accepting Cargo evidence.

- `roles/repo-scaffolder/full.md:31-33` and `modules/repo-scaffold-core/full.md:41-44`  
  Both allow “test discovery”/“test entry” checks without specifying Nix.

- `modules/nix-usage/full.md:7`  
  > “Use local checkout evaluations for diagnosis…”  
  This is Nix-related, not Cargo-specific, but should be distinguished from valid remote test evidence.

### Already aligned

- `modules/testing/full.md:7-15` establishes Nix as the normal test gate and requires flake checks.
- `modules/nix-core/full.md:16-18,52-64` requires portable/remote Nix surfaces and named checks/apps/scripts.
- `modules/nix-usage/full.md:34-40` provides the existing remote-proof mechanism: `--option max-jobs 0`, uncached derivation or `--rebuild`, and explicit evidence classification.
- `modules/nixos-vm-testing/full.md:39-45,65-67` documents the remote Prometheus path and builder reachability.

No `roles/reviewer/full.md` exists in the authoritative repository; the requested reviewer packet has no source file to amend.

### Rust-specific sources

`modules/rust-core/full.md:31-36`, `modules/rust-crate-layout/full.md:15-21,58-84`, and `modules/rust-discipline/full.md:8-19` describe test structure and architecture but do not prescribe local Cargo execution. They need only a shared testing-reference amendment if desired, not repetitive patches.

## Generated reach

- `.agents/skills/testing/SKILL.md`, `.agents/skills/code-implementation/SKILL.md`, etc. are generated projections of `modules/*/full.md`.
- `.pi/agents/<role>.md` role packets include the role source plus universal and configured modules. For example, `.pi/agents/general-code-implementer.md:200-206` contains the generated `code-implementation-core` wording.
- Generator ownership is in `src/assembly.rs`, especially role module assembly around `assembled_modules` and target paths around lines `1431-1463`.
- Therefore amendments belong in authoritative `modules/*`, `roles/*`, and possibly manifests only if module inclusion changes. Do not patch `.agents` or `.pi`.

## Minimal amendment set

1. Amend `modules/testing/full.md` with the normative universal rule and remote-builder evidence procedure.
2. Amend `modules/nix-usage/full.md` to make remote execution proof mandatory for test evidence, reusing `max-jobs 0` and builder-log guidance.
3. Replace the exception in `modules/code-implementation-core/full.md:52-56` and its duplicate standalone wording in `modules/code-implementation/full.md`.
4. Qualify generic verification wording in:
   - `roles/general-code-implementer/full.md`
   - `modules/versioning/full.md`
   - `modules/main-feature-integration/full.md`
   - `roles/rust-auditor/full.md`
   - `roles/nix-auditor/full.md`
   - `roles/operating-system-implementer/full.md`
   - scaffolding/closeout wording where “tests” is intended as execution.
5. Leave Rust layout/architecture modules unchanged unless the psyche wants all Rust test references explicitly cross-linked.

## Proposed normative wording

> Bare local language test commands, including `cargo test`, are invalid testing evidence and must not be run for testing. Test suites must be exposed and executed through Nix as flake checks or named Nix test outputs. Testing evidence is valid only when the Nix derivation executed on an authorized remote builder, not via local fallback.

> To prove remote execution, inspect daemon builder configuration with `nix config show`, run the named test derivation with local slots disabled (`--option max-jobs 0`), use `--print-build-logs`, and retain output showing the remote builder or an equivalent builder-attribution record. A cached substitute is not proof of test execution; use an uncached derivation or `--rebuild` when necessary.

## Scope questions for psyche discussion

- Does the ban cover only test execution, or also `cargo check`, Clippy, rustdoc/doctests, benchmarks, and formatting?
- Must every stateful test be a named Nix output, or may an explicitly documented Nix-entered runner qualify?
- What exact remote-builder attribution is authoritative?
- If remote builders are unavailable, should agents stop and report blocked, or allow a clearly labeled non-evidence diagnostic?
- Should existing repos lacking Nix test exposure receive a migration task before implementation proceeds?

## Migration risk and transition

Repos without Nix-exposed tests cannot immediately produce compliant evidence. Transitional behavior should be:

1. Do not run `cargo test`.
2. Report the missing Nix check/output as a blocker.
3. Add or queue the smallest Nix test exposure needed.
4. Permit only non-test diagnostics (for example source inspection or Nix evaluation) and never silently fall back to Cargo.