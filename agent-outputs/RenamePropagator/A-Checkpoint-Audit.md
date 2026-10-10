# A-Checkpoint-Audit — independent audit of the whole-graph staged-verify checkpoint

Session: RenamePropagator. Phase: audit-A (bead `primary-zohg`, P2). Role: rust
auditor (Claude Opus 4.8, 1M). Date: 2026-07-03. Read-only / non-mutating: no
`main` touched, no `drop-next` advanced, no push, `staged-cascade` never run.
All builds were non-mutating `nix build` of already-pushed revs; all VCS reads
were `ls-remote` / `gh api` / read-only shallow clones into scratchpad.

## Verdict

- **(1) SAFETY GATE — HELD, CONFIRMED.** No migration `main` was moved by this
  run.
- **(2) CLASSIFICATION — MOSTLY VALIDATED, but ONE real migration defect found**
  (bounded, 2 repos): `repository-ledger` + `signal-repository-ledger` were
  never rename-staged, retain live `-next` deps, and their ledger verdicts
  ("cascade" / "GREEN") mask a migration gap. Every other bucket (retired-syntax,
  stale-generated-artifact, no-flake, bumpfail, guard-test) is HONEST and
  reproduces as claimed.
- **(3) MECHANISM — CONFIRMED.** The 40-GREEN is real and cross-branch-driven:
  multi-level consumers resolve producers at their `drop-next` tips.
- **(4) RESIDUE — REFUTED.** Not "0 live `-next` Cargo deps across all 80":
  exactly 2 staged trees retain live `-next` Cargo deps.

**BOTTOM LINE: NO** — the report is honest that the graph is *not green* and the
safety gate genuinely held, but it is **not** a clean "no hidden migration
defect" checkpoint. There is a bounded, hidden migration gap on 2 repos that the
report's own §2/§4 claims deny and whose failure §3 mislabels as innocent
"cascade." Smallest fix set is in **Named Findings** below.

## (1) Safety gate — HELD (independently verified)

Canonical remotes (`nota.git` / `schema.git` / `schema-rust.git`), not the stale
local `-next` clones:

| producer | remote `main` | expected | drop-next | expected |
|---|---|---|---|---|
| nota | `bea7e284` | `bea7e284` OK | (none) | (none) OK |
| schema | `9af2c546` | `9af2c546` OK | `a393c8c8` | `a393c8c8` OK |
| schema-rust | `6218fb64` | `6218fb64` OK | `7f746c02` | `7f746c02` OK |

- **All 81 component remote `main` HEADs authored by `li@goldragon.criome.net`;
  ZERO by the staging identity `rename-propagator <rename@criome.net>`** (full
  `gh api .../commits/main` sweep of every ledger component). Staging is isolated
  to `drop-next`: every sampled `drop-next` tip (schema, schema-rust, agent,
  signal-frame, …) is authored by `rename@criome.net` with message
  `synchronizer: cascade dependency bumps` (or the rename rewrite), dated
  2026-07-03.
- **The two flagged local↔remote `main` divergences** (`repository-ledger`,
  `signal-repository-ledger`) resolve as claimed **in substance**: both remote
  `main` HEADs are legitimate `li <li@goldragon.criome.net>` commits pre-dating
  the session (`repository-ledger` `48109483`, `signal-repository-ledger`
  `14f08be8`), NOT staging identities. Evidence-accuracy note: the executor's §6
  says these are "dated 2026-07-01"; they are actually **2026-06-20** and
  **2026-06-19**. Substance (legit pre-session `li@`, not moved by staging)
  holds.
- Note (not a breach): a few mains were touched *today* by `li@` (e.g. `agent`
  2026-07-03T14:33, `harness` 2026-07-03T13:09) — the concurrent primary agent /
  normal activity, not this migration's staging identity.

Gate conclusion: producer mains unchanged, no consumer main authored by the
staging identity, staging confined to `drop-next`. **No migration `main` moved.**

## (2) Classification — reproduced error classes

Each check below is a non-mutating `nix build` of the exact ledger `drop-next`
tip on the prometheus builder, or a manifest/history inspection of a read-only
clone.

### VALID buckets (honest, reproduced)

- **SCHEMA-RETIRED-SYNTAX (validated, 2 reproduced + 1 inspected).**
  - `signal-domain-criome@3aca3282`: build panics `build.rs:29` →
    `Schema(RetiredStructFieldSyntax { found: "name" })`. Its `schema/lib.schema`
    is **byte-identical to `main`** (the rename does not touch schema field
    syntax). The build log proves the cross-branch resolution simultaneously: it
    vendored `schema-rust@7f746c02`, `schema@a393c8c8`, `signal-frame@drop-next`,
    `triad-runtime@drop-next`, `nota@bea7e284(main)` — the crate compiled through
    to its `build.rs`, which failed purely on schema language, not any rename
    token / import / dep.
  - `signal-upgrade@e88082ed`: panics inside `schema-rust-0.5.3/src/build.rs:479`
    → `Schema(RetiredStructFieldSyntax { found: "byte" })` (matches its
    `ContractVersion { byte RawBytes }` field). Manifest cleanly rewritten
    (`nota.git`, `schema.git`/`schema-rust.git`@drop-next), 0 `-next` residue.
  - `meta-signal-upgrade@92825f31` inspected: same `{ field Type }` struct
    syntax, clean manifest rewrite.
  - Verdict: genuine pre-existing schema-language drift surfaced by rebuilding at
    schema-rust's current tip; not a rename defect.
- **STALE-GENERATED-ARTIFACT (validated, 1 reproduced + 1 inspected).**
  - `signal-orchestrate@d4cb8676`: panics `build.rs:31` → `StaleGeneratedArtifact
    { path: ".../src/schema/lib.rs", update_environment_variable:
    "SIGNAL_ORCHESTRATE_UPDATE_SCHEMA_ARTIFACTS" }`. The checked-in artifact is
    valid rewritten code (0 live `use *_next`), carrying only an authorized
    `// @generated by schema-rust-next` header comment; the current generator
    emits different content → freshness gate fires. Regen gap, load-bearing, as
    stated.
  - `introspect@01d01bea` inspected: same freshness gate, clean manifest, 0 live
    `use *_next`.
- **NO-FLAKE false-fail (validated, 2 transitively GREEN).** `signal-lojix`,
  `signal-mirror`, `mentci` confirmed to have no `flake.nix` (standalone
  `.#default` impossible). `mirror@11933f21` built **GREEN by me** (exit 0) and
  its manifest pins `signal-mirror@drop-next` + `meta-signal-mirror@drop-next`
  (lines 51/56) — so those two no-flake crates' repins are verified transitively
  by a GREEN consumer. `signal-mirror` drop-next `bed619da` matches the ledger.
- **BUMPFAIL / multi-pin (validated).** `router` drop-next tip is the
  rename-propagator rewrite (not repinned); `signal-criome` appears in two
  same-name entries (lines 57, 76). `signal-spirit` likewise has two `schema`
  entries (lines 29, 39). Synchronizer multi-pin limit, not a rename defect. No
  `-next` residue in either.
- **GUARD-TEST (validated).** `signal-terminal@729a04a9` fails in the crane
  check phase: `tests/dependency_boundary.rs:6` asserts the manifest
  `.contains("schema-rust-next")` → after the rename it contains `schema-rust`,
  so the assertion fails with "schema-rust-next owns generated contract
  emission". A stale test literal; production manifest is correctly migrated
  (`schema-rust@drop-next`).

### THE MIGRATION DEFECT (named finding — see §Named Findings)

The **CASCADE** bucket hides a real gap. `repository-ledger` and
`signal-repository-ledger` — the two "main-divergence" repos — were **never
rename-staged**. Their `drop-next` histories contain **only** a `synchronizer:
cascade dependency bumps` commit on top of the pre-session `main`; there is **no
`rename-propagator: drop -next from family identity` commit** (a properly-staged
repo, e.g. `signal-domain-criome`, has both). Consequently both retain **live
`-next` direct Cargo deps** and the "cascade" / "GREEN" verdicts misrepresent
reality (details below).

## (3) Mechanism — 40-GREEN is real and cross-branch-driven

- `mirror@11933f21` (GREEN, **built by me**, exit 0) and `signal-criome@91096526`
  (GREEN) — both multi-level consumers — lock **`schema-rust.git?branch=drop-next
  #7f746c02`** + **`schema.git?branch=drop-next#a393c8c8`** + `nota.git?branch=
  main#bea7e284`. Their green comes from resolving producers at `drop-next`, not
  from stale pins or luck.
- `signal-frame@44d22a07` and `triad-runtime@f9a6a7c8` built GREEN (nota-only
  consumers → correctly resolve `nota@main`, which has no drop-next).
- The `signal-domain-criome` failing build independently shows the nix-level
  vendoring of all producers at their `drop-next` store paths.

The mechanism (rename rewrite + synchronizer `staged-cascade` cross-branch
repin) is sound and demonstrated end-to-end.

## (4) Residue — REFUTED

Full `gh api` sweep of **all 78 consumer** `drop-next` manifests for a live
`*-next.git` URL or `*-next =` dependency key: **2 hits**, not zero:

- `signal-repository-ledger` `Cargo.toml:24`: `nota-next = { git =
  ".../nota-next.git", branch = "main" }` (marked **GREEN**).
- `repository-ledger` `Cargo.toml:34`: `nota-next = { .../nota-next.git }` and
  `:44`: `schema-rust-next = { .../schema-rust-next.git }` (marked **cascade**).

Their `Cargo.lock`s carry the matching `git+.../nota-next.git` /
`schema-rust-next.git` / `schema-next.git` sources. The §4 claim "**0 live Cargo
`-next` deps … across all 80**" is false. (The companion "0 live `use *_next`
paths" sub-claim does hold — neither repo has a hand-written `use nota_next`
path; the residue is specifically the Cargo dependency, plus the `Cargo.lock`.)

The other buckets' residue is genuinely benign: across the 11 fully-swept trees,
0 live `-next` git URLs, 0 bare `-next` keys, 0 live `use *_next::` paths; the
raw `-next` substring hits are `branch = "drop-next"` (the correct repin),
`@generated by schema-rust-next` header/doc comments, and guard-test literals.

## Named Findings (real migration defects)

### FINDING 1 — 2 repos silently skipped by the rename; half-migrated on drop-next

**Repos:** `repository-ledger` (drop-next `2e4ef76b`), `signal-repository-ledger`
(drop-next `87495b78`).

**Root cause:** rename-propagator skipped exactly the two repos that carry a
pre-existing local jj `main*` divergence. The synchronizer then cascaded them off
**remote main** (which still declares `nota-next`/`schema-rust-next`), repinning
only the staged `signal-*` producers to `drop-next` and leaving the direct
family deps un-rewritten. Blast radius is bounded to these 2 (78-consumer sweep).

**Why it is a defect, not innocent "cascade":**

- `repository-ledger`'s build fails with `error[E0433]: cannot find `nota` in the
  crate root` from the `signal_channel!` macro while compiling its dependency
  `signal-repository-ledger` (the migrated `signal-frame@drop-next` macro emits
  `::nota`, but the unmigrated crate declares the dep as `nota-next` → `nota_next`
  in its namespace). This is a migration-induced compile failure, **not** a
  downstream effect of the enumerated schema-drift roots. The ledger's "cascade"
  label points at the wrong (invisible) root.
- `signal-repository-ledger` is marked **GREEN**, but that green is a
  **false-green on the un-migrated identity**: standalone it builds (default
  features don't exercise the `nota` path; its lock keeps `nota-next@7426a6a7`),
  yet the moment a properly-migrated consumer composes it with
  `features=["nota-text"]` it fails to compile (the E0433 above). Its GREEN
  verdict does not represent a migrated, composable state.

**Contradicts:** §2 ("80 consumers staged, all clean rewrites, 0 NO-EDITS, 0
dirty-skips") and §4 ("0 live `-next` Cargo deps across all 80"). Both are false
for these 2 repos. The executor noted the 2 as a *main-divergence gate* item but
missed that the same divergence caused the *rename to be skipped*.

**Smallest fix set (must clear before any land):**

1. `signal-repository-ledger` `drop-next`: rewrite `nota-next` → `nota`
   (`Cargo.toml:24` + `Cargo.lock`), re-stage; re-verify **as a dep of a migrated
   consumer**, not only standalone.
2. `repository-ledger` `drop-next`: rewrite `nota-next` → `nota` (`Cargo.toml:34`)
   and `schema-rust-next` → `schema-rust` (`Cargo.toml:44`) + `Cargo.lock`,
   re-stage, re-verify.
3. Harden the driver: rename-propagator should not silently skip a repo with a
   local `main*` divergence — it must either stage it or report it as an explicit
   NO-STAGE, so the "all clean" / "0 residue" claims cannot be made over a repo it
   never touched.

## Residual risks / completeness notes (not gate-breaking)

- **Guard-test blocker is under-enumerated.** Because the verify runs `cargo
  test` (crane check phase), any flaked crate whose `dependency_boundary.rs` makes
  a *positive* stale assertion (`assert!(tree.contains("nota-next"))` /
  `contains("schema-rust-next")`) will fail once its earlier blocker clears. In
  the sample: `signal-terminal` (flagged), plus **`signal-upgrade`** and
  **`meta-signal-upgrade`** (masked behind retired-syntax), and `signal-lojix`
  (no-flake, inert). The executor's blocker list names only `signal-terminal`.
  These are stale test literals (the same category the executor acknowledges),
  not production defects — but the guard-test count and §4's "authorized benign
  literal" framing understate real, build-failing test assertions.
- **Evidence-accuracy slip:** the 2 divergence mains are dated 06-19/06-20, not
  the "2026-07-01" the executor wrote (substance unaffected).
- **`nota-next.git` / `schema-rust-next.git` redirects still resolve** (HEAD =
  the renamed repos' `main`), which is why the un-migrated
  `signal-repository-ledger` can still fetch its stale pin and produce a
  false-green. Old-URL resolvability masks incomplete migration — a reason to
  fix Finding 1 before relying on any green.

## Checked evidence

- `ls-remote` of canonical `nota.git`/`schema.git`/`schema-rust.git` (mains +
  drop-next); `gh api .../commits/main` author sweep of all 81 components (0
  staging-identity mains) + the 2 divergence repos' authorship/date.
- Non-mutating `nix build` (prometheus builder) of: `signal-frame`,
  `triad-runtime`, `mirror`, `signal-repository-ledger` → GREEN;
  `signal-domain-criome` (RetiredStructFieldSyntax `name`), `signal-upgrade`
  (RetiredStructFieldSyntax `byte`), `signal-orchestrate` (StaleGeneratedArtifact),
  `signal-terminal` (guard-test), `repository-ledger` (E0433 cannot find `nota`)
  → FAIL with the quoted error classes.
- Read-only `drop-next` clones of 14 components; `git log`/`git diff` of the
  ledger repos' cascade commits; `gh api` manifest/lock reads at exact ledger
  tips.
- Full 78-consumer `drop-next` manifest sweep for live `-next` deps → 2 hits
  (`repository-ledger`, `signal-repository-ledger`).
- GREEN multi-level consumers (`mirror`, `signal-criome`) confirmed to lock
  `schema-rust@7f746c02` + `schema@a393c8c8`.
