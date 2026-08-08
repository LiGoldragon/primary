# Engine Report Tooling — CriomOS-Home Side Setup

## Scope

The psyche asked the system-operator lane to get ahead of the operator
by making the CriomOS-side tooling available for engine situation
reports. The operator owns the report/skill shape; this pass only
checks and extends the Home Manager tool bundle.

## Current Tool Surface

CriomOS-home already had the core LSP-agent tooling installed in the
min profile:

- `leta` packaged from crates.io at version `0.13.0`.
- `rust-analyzer` from the canonical `packages.rust-toolchain`.
- `typescript-language-server` plus `typescript`.
- `gopls`.
- `clangd` through `clang-tools`.
- `nil` for Nix.
- `tokei` for code-size inventory.

The current profile already exposes those binaries. `leta --version`
reports `0.13.0`.

External reference: docs.rs describes `leta` as a command-line LSP
client for agents, with symbol search, references, call hierarchy, and
refactoring operations, and says language servers are installed
separately by language. Source:
https://docs.rs/crate/leta/0.11.3

## Changes Made

Changed `CriomOS-home`:

- `modules/home/profiles/min/default.nix`
  - Added `ast-grep` for syntax-tree-aware search/editing.
  - Added `tree-sitter` to the min programming profile so syntax-tree
    tooling is available where the agent LSP bundle is available.
  - Added `scc` for structured code counts alongside `tokei`.

- `checks/leta/default.nix`
  - Extended the existing `leta-profile-tools-check` to verify:
    `leta`, `leta-daemon`, `typescript-language-server`, `gopls`,
    `rust-analyzer`, `clangd`, `ast-grep`, `tree-sitter`, `nil`,
    `tokei`, and `scc`.
  - The check runs help/version commands for the new syntax-tree and
    code-count tools, so it proves the binaries are executable in the
    Nix-built profile context.

## Smoke Results

Nix:

- `nix build .#checks.x86_64-linux.leta --no-link --print-build-logs --option max-jobs 0 --option builders '@/etc/nix/machines'` passed.
- The derivation built on `prometheus.goldragon.criome`, not locally.

Leta:

- `leta workspace add` succeeded for `CriomOS-home`.
- `leta files . -N 12` worked in `CriomOS-home`, giving a structural
  file inventory.
- `leta grep "Record" -k struct,enum -N 10` worked in `spirit-next`,
  returning schema structs such as `Records`, `RecordIdentifier`, and
  `ObservedRecords`.
- `leta grep "observe" -N 10` worked in `spirit-next`, returning enum
  members, impl objects, and generated constants around observation
  operations.

Interpretation: `leta` is useful now for Rust symbol/interface
inventory. For Nix-heavy repos, the immediate proven value is
`leta files` plus the separate `nil` language server in the profile;
Nix symbol extraction itself is not yet a strong proven path.

## Noted Drift

`nix flake show --json --all-systems` on `CriomOS-home` fails during
Darwin check enumeration because `whisrs` is Linux-only but still gets
forced while evaluating `aarch64-darwin` checks. This is unrelated to
the engine-tool bundle, but it means broad all-system flake enumeration
is not currently a valid witness for CriomOS-home.

## Recommended Next Step For Operator

Use `leta` as the first semantic code-reading tool for Rust/Go/TS/JS/C/C++
engine reports:

- `leta workspace add` once per repo.
- `leta files . -N <count>` for a size/shape pass.
- `leta grep <symbol-pattern>` for symbol inventory.
- `leta show <symbol>` and `leta refs <symbol>` for interface and
  usage inspection.

Use `tokei` or `scc` for production-code/schema/generated-code counts.
Use `ast-grep` for syntax-tree queries where LSP support is weak or
where the report needs structural pattern matching rather than symbol
navigation.
