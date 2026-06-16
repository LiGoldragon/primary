# Schema-CC Main Landing And Structural Repin

## Summary

I landed Designer's schema-cc integration on `schema-next` main, then reconciled the broader structural-forms branch family on top of that main landing.

The important shape is now clean:

- `schema-next` main owns the co-located `schema-cc` crate and the generated parenthesis-reference resolver.
- `schema-next` `structural-forms-integration` inherits schema-cc from main and carries only the positional struct-body syntax slice on top.
- The downstream structural branch family is repinned to that reconciled schema stack.

No Spirit deployment was performed in this step. This was code-repo main landing plus branch repin and verification.

## Landed Main

`schema-next` main now points at `caa77971` (`schema-next: land schema-cc resolver integration`).

That commit is Designer's merge-ready `next/schema-cc-integration` branch plus the required formatter cleanup. It keeps schema-cc co-located inside the `schema-next` workspace, generates the live parenthesis-reference resolver from `schemas/reference-grammar.nota`, and retires the previous hand-written dispatch.

Verification on `schema-next` main:

- `cargo test --workspace`: green (`schema-cc` 20 tests, `schema-next` 171 tests).
- `cargo clippy --workspace --all-targets -- -D warnings`: green.
- `nix flake check --max-jobs 0`: green after formatting the branch.

## Consumer Main Check

I tested current consumer mains against the new `schema-next` main by temporarily updating their lockfiles, without committing those consumer lockfile changes.

Repos checked:

- `signal-spirit`
- `meta-signal-spirit`
- `spirit`

For each, the generated schema source stayed byte-identical: only `Cargo.lock` changed during the temporary check, and the lockfile was restored afterward.

Verification:

- `signal-spirit`: `cargo test --features nota-text`, `cargo clippy --all-targets --features nota-text -- -D warnings`.
- `meta-signal-spirit`: `cargo test --features nota-text`, `cargo clippy --all-targets --features nota-text -- -D warnings`.
- `spirit`: `cargo build --features nota-text`, `cargo test --features nota-text`, `cargo clippy --all-targets --features nota-text -- -D warnings`.

All were green. No consumer main commits were needed because the schema-cc main landing is byte-transparent to generated downstream schema artifacts.

## Structural Branch Reconciliation

The older `schema-next` `structural-forms-integration` branch still contained my earlier OUT_DIR resolver strategy. After Designer's version landed on main, that duplicate strategy was obsolete.

I rebased the branch family by making `schema-next` `structural-forms-integration` point at the positional syntax commit on top of the new main:

- `schema-next` `structural-forms-integration`: `b7af872e` (`schema-next: positional struct-body field syntax + retired-syntax reject (port onto integration line)`).

This leaves the branch with one clear delta: positional struct-body syntax plus retired-syntax rejection. The schema-cc resolver integration is inherited from main.

Verification on `schema-next` structural:

- `cargo test --workspace`: green (`schema-cc` 20 tests, `schema-next` 174 tests).
- `cargo clippy --workspace --all-targets -- -D warnings`: green.
- `nix flake check --max-jobs 0`: green after formatting the positional branch.

## Repinned Structural Stack

I repinned and pushed the downstream structural branch family:

| Repo | Branch head | Commit |
|---|---:|---|
| `schema-rust-next` | `structural-forms-integration` | `10db4e5a` (`schema-rust-next: repin structural schema-next branch`) |
| `signal-spirit` | `structural-forms-integration` | `4f024d9f` (`signal-spirit: repin structural schema toolchain`) |
| `meta-signal-spirit` | `structural-forms-integration` | `4484c3a9` (`meta-signal-spirit: repin structural schema toolchain`) |
| `spirit` | `structural-forms-integration` | `a9361480` (`spirit: repin structural schema toolchain`) |

Verification:

- `schema-rust-next`: `cargo test`, `cargo clippy --all-targets -- -D warnings`, `nix flake check --max-jobs 0`.
- `signal-spirit`: `cargo test --features nota-text`, `cargo clippy --all-targets --features nota-text -- -D warnings`, `nix flake check --max-jobs 0`.
- `meta-signal-spirit`: `cargo test --features nota-text`, `cargo clippy --all-targets --features nota-text -- -D warnings`, `nix flake check --max-jobs 0`.
- `spirit`: `cargo build --features nota-text`, `cargo test --features nota-text`, `cargo clippy --all-targets --features nota-text -- -D warnings`, `nix flake check --max-jobs 0`.

All passed.

## Nix Patch Finding

Spirit's first Nix gate failed because its vendor patch still assumed `schema-next` depended on `nota-next` via the structural branch form:

`nota-next = { git = "https://github.com/LiGoldragon/nota-next.git", branch = "structural-forms-integration" }`

After schema-cc landed, `schema-next` uses `nota-next` main in both normal and build dependencies, and the co-located `schema-cc` crate has its own `nota-next` main dependency. I updated Spirit's flake vendor patch to rewrite those actual dependency forms. The rerun passed the full `nix flake check --max-jobs 0`.

## State

All touched code repos are clean:

- `schema-next`
- `schema-rust-next`
- `signal-spirit`
- `meta-signal-spirit`
- `spirit`

The immediate main landing is complete for `schema-next`. The structural branch family is coherent and pushed for later main integration when that broader positional syntax stack is ready to land.
