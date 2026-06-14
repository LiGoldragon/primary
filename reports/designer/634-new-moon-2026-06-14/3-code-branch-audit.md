# New-Moon Audit — Structural-Forms-Integration Branch State

Verified via `git fetch` + `git rev-list`/`git grep` against the live checkouts under `/git/github.com/LiGoldragon/` on 2026-06-14.

## 1. Integration branch: `structural-forms-integration` vs `main` (all 8 repos)

The branch exists on `origin` in every one of the 8 repos, is strictly ahead of `main` (0 commits behind in all), and is **not** an ancestor of `main` anywhere — it is the live integration branch, not yet landed.

| Repo | `origin/main` head | `origin/structural-forms-integration` head | ahead / behind | on main? |
|---|---|---|---|---|
| nota-next | `3d6c2cd` avoid MSRV lint in byte sequence decode | `00d0050` integrate structural macro shapes | +3 / 0 | NOT on main |
| triad-runtime | `1b5d0f1` tailnet TCP listener: PeerIdentity closed sum + TcpListenerDaemon | `7a84034` integrate generic reaction frame | +2 / 0 | NOT on main |
| schema-next | `f460e7b` clean up integrated branch formatting | `2bb0228` integrate structural forms grammar | +8 / 0 | NOT on main |
| schema-rust-next | `00763d6` omit unused multi-listener runtime import | `573375d` integrate structural forms emission | +3 / 0 | NOT on main |
| signal-spirit | `87cf9bf` expose source witnesses | `e85830b` apply current rustfmt | +2 / 0 | NOT on main |
| meta-signal-spirit | `ed7ce82` refresh contract skill invariant | `cc57670` align structural forms dependencies | +1 / 0 | NOT on main |
| sema-engine | `909eaa0` distinguish domain keys from identifiers | `1afcd01` integrate decomposed engine planes | +5 / 0 | NOT on main |
| spirit | `adeba15` correct meta-signal architecture path | `bb6bff6` trace guarded direct sema writes | +10 / 0 | NOT on main |

## 2. Meta-signal split — landed on `spirit` main

Confirmed both commits are on `origin/main` of `spirit` (and `main` HEAD sits on the second one):

- `4ec746b` (full `4ec746bc1c6a3c8797890fa5b9855bc17afd9104`) — **spirit: import meta-signal contract from meta-signal-spirit** (2026-06-14)
- `adeba15` (full `adeba15d7ded108f528ede8d320bb81138ccf4ec`) — **spirit: correct meta-signal architecture path** (2026-06-14) — current `origin/main` HEAD

The source contract on `meta-signal-spirit` main is `d5b5dde` (schema-derived Configure Import contract, 2026-06-14). These split commits are on `main` only; they are independent of and not part of the integration branch.

## 3. Open regressions on the integration branch (from designer review 633)

### 3a. schema-next — 3 reconciliation fold-ins reverted (CONFIRMED by reading `origin/structural-forms-integration`)

Inspected `src/schema.rs` and `src/engine.rs` directly on the sfi branch. All three reconciliations the designer had landed are absent from the integrated state:

1. **Hand NotaDecode/NotaEncode codec handed back** — `TypeReference` carries hand-rolled `impl NotaDecode for TypeReference` (`src/schema.rs:1457`) and `impl NotaEncode for TypeReference` (`src/schema.rs:1524`), rather than the derive. Ten hand codec impls remain in `schema.rs` (also `Name`, `SymbolPath`, `StructFieldMap`, `TableName`), plus one in `engine.rs`. The derive-based reconciliation commit `5baef26` ("TypeReference is a derived StructuralMacroNode; delete the hand-rolled head-dispatch") is **not** reflected in the integrated tree.
2. **SchemaError is not thiserror** — defined at `src/engine.rs:50` with a hand-written `impl std::fmt::Display for SchemaError` (`engine.rs:326`), bare `impl std::error::Error for SchemaError {}` (`engine.rs:332`), and 7 manual `impl From<…>` conversions (`engine.rs:220`–`310`). There is **zero** `thiserror` reference anywhere in the sfi tree, and it is not a Cargo dependency. The reconciliation commit `28b477a` ("SchemaError -> thiserror with typed nota-next sources") is not reflected.
3. **HeadedAtom seam dropped** — `HeadedAtom` has **0 occurrences** across the entire sfi source tree (grep over all of `src/`). The seam carried on nota-next branch `typeref-shape` (`3e18e37` "HeadedAtom structural shape for numeric-atom leaf fields") did not survive into the integration.

### 3b. spirit — testing-trace instrumentation regression (CONFIRMED, feature-gated)

`cargo test --all-features` fails on the `instrumentation_logging` test. This is **feature-gated and does not affect the default build**:

- `Cargo.toml` declares the test with `required-features = ["testing-trace"]` (`Cargo.toml:56-59`); `testing-trace = []` is an opt-in feature (`Cargo.toml:54`).
- The instrumentation lives behind `#[cfg(feature = "testing-trace")]` throughout (`src/bin/spirit.rs`, `src/daemon.rs`, `src/engine.rs`).
- The test only compiles/runs when `testing-trace` is on — which `--all-features` turns on. Default-feature builds and tests are unaffected. The sfi HEAD `bb6bff6` ("trace guarded direct sema writes") is the relevant trace-path commit.

## 4. Designer reconciled branches — naming discrepancy

The two branch names given in the brief do **not** exist on `origin`. The actual reconciliation branches the designer pushed are named differently — flagging this so the meta-report cites the real refs:

| Brief's name | Actual branch on origin | Head | ahead/behind main |
|---|---|---|---|
| nota-next `next/combined-leaf-shapes` | **not present** — closest are `next/pascal-head-body-shape` (`db0f10a`, PascalHeadBody derive shape, +1/0) and `typeref-shape` (`3e18e37`, HeadedAtom numeric-atom leaf, +1/0) | — | — |
| schema-next `next/typeref-structural-generics` | **not present** — closest are `next/schema-generics` (`5feccb6`, reaction frame fixture + full-frame pilot, +4/0) and `typeref-structural-macro` (`5baef26`, derived StructuralMacroNode, +3/0) | — | — |

Recommendation: before the meta-report ships, confirm with the designer which of these refs are the canonical reconciled branches (the leaf-shape work appears split across `next/pascal-head-body-shape` + `typeref-shape`; the typeref/generics work across `next/schema-generics` + `typeref-structural-macro`). The reconciled codec/thiserror/HeadedAtom work clearly lives on `typeref-structural-macro` and `typeref-shape`, which is exactly the work that did NOT make it into `structural-forms-integration` — consistent with regression 3a.

## Bottom line

- Integration branch present and ahead-only on all 8 repos; nothing merged to main.
- Meta-signal split is real and on `spirit` main (`4ec746b`, `adeba15`).
- schema-next regressions confirmed by source inspection: hand codec retained, SchemaError hand-rolled (no thiserror), HeadedAtom absent.
- spirit testing-trace failure confirmed but strictly feature-gated (`required-features = ["testing-trace"]`); default build clean.
- One correction for the report: the reconciled designer branch names in the brief don't match origin; real candidates listed above and need a designer confirm.