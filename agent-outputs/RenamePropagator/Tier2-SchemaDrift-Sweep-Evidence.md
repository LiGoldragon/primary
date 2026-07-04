# Tier2 Schema-Drift ENUMERATION SWEEP — evidence (bead primary-5kxh gap + zy24 close)

Session: RenamePropagator. Role: General Code Implementer (Claude Opus 4.8, 1M).
Date: 2026-07-04. Closes the ENUMERATION GAP the prior Tier-2 worker flagged:
their 11-repo list was under-enumerated because a repo that cannot build
standalone (no flake) never surfaces its `.schema` retired-syntax drift, so
masked contract repos carried the same drift unfixed. This sweep enumerates
EVERY LiGoldragon schema-bearing repo's `drop-next` `.schema` sources against
the deployed parser, fixes the masked set, and verifies past schema-compile.
NO migration `main` touched anywhere.

## Authoritative verifier (built, not assumed)

Cloned `schema-rust@drop-next` (HEAD `7f746c02`, the deployed producer) into
scratch and built its `examples/emit_schema`, which runs the SAME
`SchemaEngine::lower_source_with_resolver` path a consumer's `build.rs` uses. It
pulls `schema@drop-next a393c8c8` + `nota@main` + `triad-runtime@drop-next` via
Cargo (verified: `schema-rust`'s manifest pins `schema` at `branch=drop-next`,
lockfile resolves `a393c8c8`). Every drift verdict below is this deployed
parser's, not a heuristic.

Re-confirmed the retired→current transform DIRECTLY against `schema@a393c8c8`
`src/source.rs` (`SourceField::from_positional_block`,
`from_explicit_field_reference`, `SourceNamedBlock::from_blocks_if_trailing_dot`,
`is_retired_explicit_structural_field`, `is_reserved_scalar_name`) and
`src/schema.rs` `ReferenceHead::classify`. The table is exactly the prior
worker's:

| retired field pair | current form |
|---|---|
| `role Type` (field_name(role)!=field_name(Type), Type non-scalar) | `role.Type` |
| `role Type` (Type a reserved scalar String/Integer/Boolean/Path/Bytes) | `role.Type` |
| `role Type` (field_name(role)==field_name(Type), non-scalar) | `Type` (bare) |
| `role (Comp …)` (Optional/Vector/Map/ScopeOf) | `role.(Comp …)` (trailing-dot) |
| `Name *` (self-type marker) | `Name` (bare) |
| `(Vec …)` | `(Vector …)` |
| `role.Type` redundant (role==field_name(Type), non-scalar) | `Type` (bare) |

Retired forms that RAISE `RetiredStructFieldSyntax`/`RedundantExplicitFieldRole`
are only these, and only as fields inside a struct body (`{}` nested at
brace-depth ≥ 2). A `Pascal Pascal` pair reads as two valid bare fields (NO
error), so it is not drift.

### IMPORTANT correction to the `(Vec …)` premise (honesty note)

`(Vec X)` is NOT a retired-syntax error at `a393c8c8`. `ReferenceHead::classify`
knows only `Vector Optional ScopeOf Map Bytes`; an unknown Pascal head like `Vec`
falls through to the generic application form `Vec<X>` (`from_record` →
`Self::Application`) and parses fine, failing only at RESOLUTION if `Vec` is
undeclared. Proof: `signal-criome@drop-next` carries nine `role.(Vec X)` fields
and emits FULL clean Rust via the deployed parser (it was GREEN in the A run).
So a bare `(Vec` textual match is NOT a drift signal and was excluded from
enumeration; the `(Vec…)`→`(Vector…)` rewrite is applied ONLY as part of fixing a
repo that already carries genuine `RetiredStructFieldSyntax` struct-field drift
(where the retired sources happen to also use the `Vec` alias, e.g. inside
`generations.(Vector Generation)` and the `NodeSelection` enum payload).

## Enumeration method (structure-agnostic, triangulated)

1. Git-plumbing sweep of all 119 checkouts under `/git/github.com/LiGoldragon`:
   extract every tracked `*.schema` at `drop-next` (or `main` where no
   `drop-next` exists). Result: 78 schema-bearing repos, 200 schema files.
2. Two independent detectors faithful to `source.rs`:
   - atom detector: `*`, non-type-case bare field head, reserved-scalar bare,
     redundant dotted role — at brace-depth ≥ 2, comment- and pipe-delimiter
     (`{| |}` `(| |)`) aware.
   - structural detector v2: pipe-aware tree parse; classifies every struct-body
     field exactly like the parser INCLUDING the `(Role (Comp))` 2-block paren
     form the atom scan can miss.
3. Authoritative `emit_schema` on every signal-shaped `.schema` (with
   cross-import deps where needed), classifying the first error.

Calibration: the detectors agree with `emit_schema` on known cases —
`signal-lojix@drop-next` → `RetiredStructFieldSyntax { found: "policy" }`;
fixed `signal-domain-criome@drop-next` → clean emit; `skills:assembly` /
`signal-criome` / `signal-terminal` (earlier false-positive suspects) → clean
under both detectors AND `emit_schema`. v2 independently re-detects the
retired `cloud`/`tree-sitter-schema` MAIN fixtures, proving it detects drift in
non-signal schema kinds too.

## COMPLETE enumerated retired-drift set (drop-next, in scope)

Across ALL 78 schema-bearing repos' `drop-next` schemas, exactly TWO carry
genuine retired struct-field syntax — both masked no-flake contracts, exactly as
the prior worker predicted (they named `signal-lojix` and "likely
`meta-signal-lojix`"):

| repo | file | detector (atom / v2) | emit_schema (pre-fix) |
|---|---|---|---|
| signal-lojix | schema/lib.schema | bare-role=34, star=48 | `RetiredStructFieldSyntax { found: "policy" }` |
| meta-signal-lojix | schema/lib.schema | star=45, bare-role=20 | `RetiredStructFieldSyntax { found: "*" }` |

No other masked repo exists. Every other schema-bearing consumer scans clean on
`drop-next` under both detectors, and every signal-shaped one that `emit_schema`
could reach either emits clean or fails only on an UNRESOLVED-IMPORT / different
error class (i.e. it PASSED the retired-syntax parse — that check fires before
resolution). Confirmed clean this way: all no-flake suspects
(`signal-mentci` `meta-signal-mentci` `signal-mentci-client`
`meta-signal-mentci-client` `signal-mirror` `meta-signal-mirror` `mentci`
`meta-signal-harness`/`meta-signal-system`=no schema) and the cascade/bumpfail
suspects (`harness` `system` `router` `signal-spirit`).

## FIXES applied (drop-next only)

Transform via the prior worker's validated `scratchpad/transform.py` (struct-body
pair rewrite + `(Vec…)`→`(Vector…)`), byte-verified against a hand-reviewed
field-by-field diff, then re-verified past-schema with the deployed
`emit_schema`. Every generated field name preserved (bare `Type` derives the
retired role's name; `role.Type` and `role.(Comp)` keep `role`; redundant
`operatorHint OperatorHint`→`OperatorHint` keeps `operator_hint`;
`source_revision_policy SourceRevisionPolicy`→`SourceRevisionPolicy` keeps
`source_revision_policy`).

| repo | drop-next before → after | change | verification |
|---|---|---|---|
| signal-lojix | `4db768af` → **`43a97e15`** | schema/lib.schema (54/54) | `emit_schema` FULL clean emit; both detectors 0 retired |
| meta-signal-lojix | `74a7c71e` → **`381f71b6`** | schema/lib.schema (37/37) | `emit_schema` FULL clean emit (composed with fixed signal-lojix as dep); both detectors 0 retired |

Concurrency note: both repos' remote `drop-next` had advanced past my stale
local remote-tracking ref (a `synchronizer: cascade dependency bumps` commit
touching only Cargo.lock/Cargo.toml; schema byte-identical). The first
signal-lojix push was rejected `stale info`; I fetched, confirmed the cascade
tip is a LINEAR descendant with an identical retired schema, rebased the
schema-only fix onto the real remote tip (preserving the cascade bump), and
pushed. Each final push confirmed via `git ls-remote` + a clean-schema re-scan
of the landed tip. Commits authored `li@goldragon.criome.net` (repo convention,
matching `signal-domain-criome`'s fix), message model-tagged.

Verify model: "past schema-compile" = the deployed parser no longer raises
`RetiredStructFieldSyntax`/`RedundantExplicitFieldRole`. For these no-flake
contracts a standalone `nix build` is impossible (the masking), so the
authoritative per-schema check is the deployed `emit_schema` — a genuine
per-repo parser run, not a heuristic. signal-lojix emits fully; meta-signal-lojix
emits fully once composed with the fixed signal-lojix (its only cross-import).

## Cross-checks

- The already-fixed 11 (`domain-criome lojix meta-signal-cloud
  meta-signal-domain-criome meta-signal-persona meta-signal-upgrade persona
  signal-cloud signal-domain-criome signal-upgrade upgrade`) all scan CLEAN on
  `drop-next` — the prior fixes hold; none re-edited. `lojix`'s cascade block was
  on `signal-lojix@4db768af` (retired); my signal-lojix fix directly unblocks it
  at the convergence re-lock.
- The 6 regen repos (`introspect meta-signal-mind meta-signal-orchestrate
  orchestrate signal-orchestrate terminal`) scan clean (their schemas lower fine;
  their gate is the separate StaleGeneratedArtifact bead). Not touched.
- `repository-ledger`/`signal-repository-ledger` (live Tier-1 owner) not touched.

## Skipped / out of scope

- `cloud` — Codex `cloud-maintainer` Orchestrate claim; and its
  `schema/sema.schema` drift (bare-role=11) is MAIN-only (no `drop-next`).
  SKIPPED-PEER-HELD, not clobbered.
- `mind`, `spirit` — named peer-held; both schema-clean on their (main-only)
  sources anyway (v2), so no action needed.
- `tree-sitter-schema` MAIN test fixtures (star/bare-role hits) — the
  tree-sitter grammar's intentional negative/old-syntax parse fixtures, NOT a
  schema-rust consumer contract. Out of scope.
- `schema-next`/`schema-rust-next` in-repo test fixtures — producer/tooling
  fixtures (and pipe-brace false positives now cleared by v2). Out of scope.

## primary-zy24 — three stale guard literals (VERIFIED on current drop-next)

All three POSITIVE stale literals fixed; the LEGITIMATE negative boundary guards
left literal (still pass post-rename):

- `signal-terminal@drop-next 4f75a6c5` `tests/dependency_boundary.rs`:
  `cargo_toml.contains("schema-rust")` (was `"schema-rust-next"`). Negatives
  `!contains("signal-engine-management")`, `!contains("signal-persona-origin")`
  LITERAL. prometheus `packages.default` GREEN (prior evidence).
- `signal-upgrade@drop-next b8b3f818` `tests/dependency_boundary.rs`:
  `tree.contains("nota")` (was `"nota-next"`). Negative guard
  `for forbidden in ["nota-next","nota-codec","signal-core"] { !tree.contains(..) }`
  LITERAL.
- `meta-signal-upgrade@drop-next 003bef5b` `tests/dependency_boundary.rs`:
  identical `tree.contains("nota")` fix + same negative guard LITERAL.

signal-terminal builds green; the two upgrade repos' crane checks pass once their
separately-tracked regen/convergence blocker clears (the zy24 DoD explicitly
decouples crane-green from that upstream blocker). All three literals are
present and correct on drop-next → **primary-zy24 CLOSED**.

## Residual masking risk (stated, not hidden)

Confidence is high but not absolute. What I could NOT verify by the deployed
`emit_schema` directly: four non-signal schema kinds whose root shape
`emit_schema` rejects with `ExpectedRootObjectCount` before reaching fields
(`harness.concept`, `system.concept`, `router.concept`, `signal-spirit:domain`).
These were verified CLEAN by the structure-agnostic detector v2 instead —
calibrated against known-GREEN concept schemas (clean) and known-retired MAIN
fixtures (flagged), so v2 demonstrably detects drift across schema kinds. The
irreducible residual: a retired form inside an exotic nesting v2 does not model
(method-signature `[sigs]`, relation/stream blocks) could in principle escape
both `emit_schema` (wrong root) and v2. I judge this low — retired syntax only
lives in struct-field bodies, which v2 parses regardless of surrounding kind —
but it is the one gap I cannot rule out with a build. It fully clears when these
daemon repos build past their own `build.rs` at the convergence cascade.

## Safety

No migration `main` moved. signal-lojix main `fbb28cf4` and meta-signal-lojix
main `4a8e7911` unchanged (local == remote == session start). All edits on
`drop-next` (fast-forward advances / cascade-preserving rebase), pushed via
`jj git push --bookmark drop-next`. Both repos claimed via Orchestrate lane
`schema-drift` before editing, released after. `cloud` (peer claim) untouched.
Zero project data on any public surface.
