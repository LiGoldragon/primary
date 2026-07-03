# rename-propagator — implementation evidence

## Task and scope

Build (not run) a rename-propagation codemod that drops `-next` from three
crate families across the engine: `nota-next.git`→`nota.git` (crate `nota`),
`schema-next.git`→`schema.git` (crate `schema`), `schema-rust-next.git`→
`schema-rust.git` (crate `schema-rust`). Deliver the tool with tests and a
dry-run capability. Do NOT run it across the live engine, rename any GitHub
repo, or edit consumer repos. Build only in the tool's own repo / a shared lib.

## Deliverable

New repository: **`LiGoldragon/rename-propagator`** (private), pushed.
- Commit: `9ff50c6dfd6c759eaeb130cab7be4f00a2d9d403` on `main`.
- Local checkout: `/git/github.com/LiGoldragon/rename-propagator` (jj colocated).
- Two-crate cargo workspace: `crates/manifest-surface` (shared substrate),
  `crates/rename-propagator` (the codemod).

## Sources consulted

- Synchronizer (reuse anchor): `/git/github.com/LiGoldragon/synchronizer`
  `ARCHITECTURE.md`, `src/toml_document.rs`, `src/types.rs`, `src/cargo_manifest.rs`,
  `src/flake_manifest.rs`, `src/report.rs`, `src/configuration.rs`, `src/topology.rs`.
- Producers: `nota-next/Cargo.toml`, `schema-next/Cargo.toml`,
  `schema-rust-next/Cargo.toml` (each already declares its new identity in
  `[package] name` + `[package] repository`).
- Surveyed ~84 consumer `Cargo.toml`, flake files, and `.rs` for token shapes.
- Two scouts (returned in chat, no files): the schema-rust emitter mechanism
  (item 7) and the `spirit/flake.nix` coupling (item 6).

## Design decision — sibling tool + shared crate (not a synchronizer mode)

A rename is a distinct verb from a bump. The synchronizer's model is staleness
against a resolved *revision* (BumpLedger, cascade rule, wire-skew); a rename
has no revision, no staleness — it has an identity map over a token surface.
Folding rename into the synchronizer's driver as a mode would stack an unrelated
special case on the normal case (the beauty-gate anti-pattern) and blur the
synchronizer's version-propagation identity. → **sibling tool, own repo.**

Genuine reuse is of the *substrate*, not the logic: format-preserving edits and
the repository-identity URL grammar. Extracted into `manifest-surface`
(forge/rename/bump-agnostic; deps `toml_edit`, `winnow`, `thiserror`). Practical
constraint that ruled out depending on the synchronizer crate directly:
`synchronizer.git` is not in the cargo git cache, so a git-dep on it would not
build offline; `nota-next.git` *is* cached, so `nota` is available for the NOTA
report.

**Reuse mechanism note / accepted temporary duplication:** `manifest-surface`
holds fresh implementations of the format-preserving TOML document and the
repository-identity grammar. The synchronizer keeps its parallel copies. The
clean end-state is one shared crate both depend on; migrating the psyche-signed
synchronizer onto `manifest-surface` is scoped as a **follow-up**, deliberately
NOT done in this task to avoid destabilizing it right before its own
mass-application. This is the standard extract-then-migrate shape.

## Audit round — three CHANGES REQUIRED landed (tool commit `540b25c6`)

An adversarial audit passed the token engine (25/25 boundary probes, kept
as-is) but returned CHANGES REQUIRED on three items, all now landed with
regression tests; build/test/clippy/fmt stay green (28 tests).

1. **BLOCKING — rev-pinned family deps (refuted the "rev-pins dissolve, no
   manual action" claim; the audit was right).** A family dep pinned by
   `rev`/`tag` (e.g. `mind/Cargo.toml` line 59 and the `[patch]` blocks at
   69-70/72-73/75-76) resolves, at its pinned pre-rename commit, to the *old*
   package name — a token rewrite makes it unresolvable (`no matching package
   named 'schema-rust'`), and lock regen cannot fix it (the manifest pin is
   authoritative). New `crates/rename-propagator/src/cargo_manifest.rs`
   (`CargoManifestRename`) detects such entries — and an entire family
   `[patch."…"]` block that contains one, header included — leaves them
   byte-for-byte unchanged, and surfaces each as a `FlaggedPin`
   (`RevisionPin`/`TagPin`) for landing-time resolution. Branch-pinned family
   deps still rewrite. Corrected the false claim in `ARCHITECTURE.md` §4/§10 and
   `README.md` (and below).
2. **Completeness — residue scan.** After rendering, the sweep now scans *every*
   swept file (classified or not) for leftover whole-token family references and
   reports each as a `ResidueHit`, skipping only lines a Cargo surface protected
   (a flagged pin). Surfaces the spirit shell scripts
   (`scripts/run-nix-integration-tests`, `scripts/check-local-schema-stack`)
   that pass `nota-next`/… as bare flake-override args. Reported, not
   auto-rewritten (a script `*_REF` may need to move with a flagged pin —
   landing's call). `ARCHITECTURE.md` §5/§8 extended for shell/script surfaces.
3. **Guard — post-rewrite TOML re-parse.** Each rewritten `Cargo.toml` is
   re-parsed via `toml_edit`; a rewrite that would duplicate a dependency key
   (or otherwise corrupt the manifest) aborts with `Error::ManifestCorruption`
   before writing, making that class impossible rather than corpus-dependent.

Plan schema grew: `RepositoryPlan` now carries `[flagged-pin]` and
`[residue-hit]` trailing vectors. Regression tests added:
`tests/cargo_manifest.rs` (4: branch-pin rewritten / rev-pin + patch-block
flagged, tag pin, `rev`-not-confused-with-`preview`, duplicate-key guard),
`tests/end_to_end.rs` (+2: residue surfaces a script, rev-pin flagged-not-edited),
`tests/nota_wire.rs` (round-trips the new records). Live binary drive confirmed
`mind` flags its two rev pins and `spirit` surfaces the three script lines as
residue. Two things the audit said landing (not this tool) handles: F3 (exclude
data-only repos like synchronizer/sema-engine from the swept set) and F5 (prefer
regenerating the 28 generated files with a regenerate-and-diff drift check).

## The one mechanism (design-quality: special cases dissolve)

Every edit is a **bounded-token span substitution** (generalizing the
synchronizer's flake.nix input-URL span rewrite). `manifest-surface::token`:
- `BoundaryClass::RepositoryToken` (`[A-Za-z0-9_-]`) — `nota-next` moves in
  `LiGoldragon/nota-next.git` and `"dep:nota-next"` but never in `nota-text`,
  `nota-derive`, `nota-source`.
- `BoundaryClass::RustIdentifier` (`[A-Za-z0-9_]`) — `nota_next` moves in
  `use nota_next::x` but never in `my_nota_next_field`.
Format-preserving: only matched token bytes change; a rename never adds/removes
a line, so the plan is a 1:1 before/after line pairing.

The rename map is **discovered** (`rename_rule.rs`): each `RenameRule` reads a
producer's own `[package] name` (crate) and `[package] repository` (new repo
name); old repo name is the config checkout name. Derived: hyphen repository
token + underscore path ident (`-`→`_`). Zero family names in `src/`.

## Transform surface covered (the tool's own modules, `surface.rs`)

| file | tokens | covers |
|---|---|---|
| `Cargo.toml` | repository | git URLs, dep table keys, `dep:` features, `[patch."url"]` keys, `package=` (none present) |
| `Cargo.lock` | repository | `source = "git+…"` URLs |
| `flake.nix` | repository | `github:owner/repo` shorthand, `git+https` inputs, spirit `substituteInPlace --replace-fail` FROM strings, `[patch]` keys, alias map |
| `flake.lock` | repository | `repo`/`url` fields (rev + narHash preserved — pure metadata rewrite, no prefetch) |
| `*.rs` | path-ident + repository | `use` paths, generated `pub use nota_next::…`, `@generated by schema-rust-next` header |
| other `*.nix` | repository | same as flake.nix |

**Rev/tag-pinned family deps are detect-and-flag, NOT rewritten** (corrected
after the audit — the earlier "dissolve cleanly" claim was wrong): at the
pinned pre-rename commit the crate still publishes the old name, so a rewrite is
unresolvable. `cargo_manifest.rs` leaves such an entry — and a family `[patch]`
block containing one — unchanged and flags it (`FlaggedPin`) for landing.
Branch-pinned family deps still rewrite normally.

**Cargo dep key rename** uses a bare repository-token rewrite — verified safe by
survey: every family token in a workspace `Cargo.toml` is a dep key, git URL,
`dep:` feature, or `[patch]` header (no prose). A renamed key preserves its
following whitespace verbatim, so the `=` shifts by the length delta — the one
accepted cosmetic consequence, shown explicitly in the dry-run plan.

## Item 7 resolution — the schema-rust emitter

The `nota_next::` crate root in generated `src/schema/*.rs` was a **hardcoded
literal** in the emitter's `quote!` calls (not derived from the dep key). The
emitter source was **already** de-`next`ed in schema-rust-next commit `06eec0d`
(2026-06-23): it now emits `nota::` and the header `@generated by schema-rust`;
no `nota_next` literal remains in its `src/`. On disk, 35 generated files
already emit `nota::` (regenerated), 28 still emit `nota_next::` (stale).

**Verdict:** regeneration alone now drops `-next`. The codemod reaches the same
end-state textually — the generated `nota_next::` re-export and the
`@generated by schema-rust-next` header are exactly the underscore-ident and
hyphen-repository tokens the tool rewrites. Regeneration is canonical where the
emitter is run; the tool's rewrite is the equivalent for the 28 stale files. The
emitted `pub use nota::…` only compiles once the consumer's Cargo key is `nota`,
which the same run rewrites. Demonstrated end-to-end on a fixture
`src/schema/nexus.rs`.

## Dry-run plan format (NOTA, `plan.rs`)

```nota
(<generated-at> <rename-map> [<repository-plan>])         ;; RenamePlan
(<repository> [<file-plan>])                               ;; RepositoryPlan
(<relative-path> <surface> [<planned-line>])               ;; FilePlan
(<line-number> <before> <after>)                           ;; PlannedLine
```

Every edit is enumerated before any write; applying is exactly writing each
planned line's `after`. Round-trips through the canonical NOTA codec (test).

## Landing model (`landing.rs`) — gated

Producers-first (topological, discovered via `ProducerGraph`/Kahn), then swept
consumers, on the tool-owned staging branch; never the mainline. The git
commit / force-push / per-lock-graph verify gate is the **gated apply phase** —
it reuses the synchronizer's `GitRepository`/`BuildVerifier` boundaries and is
NOT executed by this crate. The dry-run writes nothing; `--apply` writes only to
a caller-owned checkout (tested on temp fixtures).

## Checks run (offline, all green)

- `cargo build --offline --all-targets` — clean.
- `cargo test --offline` — **23 passed, 0 failed** across:
  - `manifest-surface`: `token.rs` (5, boundary safety), `repository.rs` (5, URL grammar).
  - `rename-propagator`: `surfaces.rs` (5, the non-Cargo surfaces), `cargo_manifest.rs` (4, branch-pin rewrite / rev+tag+patch-block flag / `preview` not a pin / duplicate-key guard), `end_to_end.rs` (6, discover/landing/dry-run/apply + residue + flagged), `nota_wire.rs` (3, config + plan round-trips incl. flagged/residue). 28 total.
- `cargo clippy --offline --all-targets -- -D warnings` — clean.
- `cargo fmt --all -- --check` — clean.
- End-to-end binary drive on a realistic multi-surface fixture (not the live
  engine): dry-run emitted the full NOTA plan; `--apply` rewrote all surfaces
  correctly (files inspected); re-running dry-run after apply produced an
  all-empty plan (idempotent).

## Files created (all under `/git/github.com/LiGoldragon/rename-propagator`)

- Workspace: `Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`, `.gitignore`,
  `ARCHITECTURE.md`, `README.md`, `config.sample.nota`, `AGENTS.md`, `CLAUDE.md`.
- `crates/manifest-surface/`: `Cargo.toml`, `src/{lib,error,types,repository,token,toml_document}.rs`, `tests/{token,repository}.rs`.
- `crates/rename-propagator/`: `Cargo.toml`, `src/{lib,main,error,rename_rule,configuration,surface,discovery,plan,landing,driver}.rs`, `examples/validate.rs`, `tests/{surfaces,end_to_end,nota_wire}.rs`.

## Flagged for the mass-application (gated) phase — must handle by hand

1. **The GitHub repository renames** themselves (`nota-next.git`→`nota.git`,
   etc.). GitHub renames are manual and set up redirects; the tool rewrites
   references but cannot rename a forge repository.
2. **Redirect verification** after the renames: confirm old URLs redirect and
   each rewritten flake input resolves at its recorded revision. (Tree hash is
   unchanged by a rename, so flake `narHash` and Cargo `rev` are preserved — the
   tool never recomputes them.)
3. **Per-graph lock regeneration + verify**: the three unified-lock graphs
   (nota, schema, schema-rust) each regenerate `Cargo.lock`/`flake.lock` and
   build-verify after producers land, before that graph's consumers land.
4. **Regeneration of the 28 stale schema-rust-generated files** is the canonical
   alternative to the textual rewrite where the emitter is run.
5. The rev-pins in `mind/Cargo.toml` (build-dep + three `[patch]` blocks) are
   NOT rewritten by the tool — they are flagged. Landing must, per flagged pin,
   advance the pin to a post-rename revision or inject `package = "<old-name>"`
   so Cargo finds the package the pinned commit publishes.
6. Residue hits in shell/script surfaces (spirit `scripts/*`) are surfaced, not
   rewritten; landing renames the repo-name args (and any coupled `*_REF`).

## Follow-ups / recommendations (provisional)

- **Migrate the synchronizer onto `manifest-surface`** to remove its parallel
  copies of the preserved TOML document and repository-identity grammar,
  collapsing the temporary duplication. Do it when the synchronizer is next
  touched and verify in that lane.
- Consider promoting `rename-propagator` to public (mirrors the synchronizer's
  public-infra nature) once the psyche approves.
- A real criome config belongs in a data-only repo (e.g. `goldragon`), like the
  synchronizer's `synchronizer.nota`, not committed into the tool.

## Boundaries honored

Did not run the migration, did not rename any GitHub repo, did not edit any
consumer/producer/synchronizer repo (only read them to design the transform).
All apply/dry-run exercises were on temporary fixtures.
