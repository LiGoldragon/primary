# Tier2 Schema-Drift Fix — evidence (bead primary-5kxh + zy24 overlap)

Session: RenamePropagator. Role: General Code Implementer (Claude Opus 4.8, 1M).
Scope: the SCHEMA-RETIRED-SYNTAX bucket surfaced (not caused) by the -next→canonical
rename. 11 consumer `.schema` SOURCES used syntax `schema-rust` has retired; they
failed to build against `schema-rust@drop-next 7f746c02` (→ `schema@drop-next a393c8c8`,
`nota@main bea7e284`). Fixed the sources to the current schema language on each repo's
`drop-next` branch. NO migration `main` touched anywhere.

## The retired→current transform (uniform, established once, applied consistently)

Authoritative parser read directly from `schema@a393c8c8` `src/source.rs`
(`SourceField::from_positional_block`, `from_positional_blocks_at`,
`from_explicit_field_reference`, `from_blocks_if_trailing_dot`,
`is_retired_explicit_structural_field`). The retired forms lived only inside struct
bodies `Name { ... }` (declaration-block `Name Definition` pairs, enum `[...]` bodies,
and request/response header blocks are already current and untouched).

A struct-body field written in the retired `role value` pair form maps as follows:

| retired field pair | current form | rule |
|---|---|---|
| `role Type` where `field_name(role) == field_name(Type)`, Type non-scalar | `Type` | bare positional; explicit role would be `RedundantExplicitFieldRole` |
| `role Type`, Type a reserved scalar (`String Integer Boolean Path Bytes`) | `role.Type` | bare scalar illegal as a field; role kept (redundancy check skipped for scalars) |
| `role Type`, `field_name(role) != field_name(Type)` | `role.Type` | explicit dotted role reference (single atom) |
| `role (Composite …)` (Vector/Optional/Map/ScopeOf) | `role.(Composite …)` | trailing-dot named field: atom `role.` + following paren block |
| `Name *` (retired self-type marker) | `Name` | `*` retired; self-typed field becomes the bare type |
| retired vector head `(Vec …)` anywhere | `(Vector …)` | `Vec` is not a built-in head at a393c8c8; `Vector` is |

`field_name(X)` = X lowercased with `_` inserted before each interior uppercase and
`-`→`_` (matches `Name::field_name` in `schema/src/schema.rs`). Every field's generated
name is preserved: bare `Type` derives the same name the retired role carried; `role.Type`
and `role.(Composite)` keep `role` verbatim.

IMPORTANT correction during this lane: the local `~/wt` schema checkout was at the older
`ef499e25` (rename-propagator tip), whose parser still ACCEPTED the parenthesized
role-tag `(Role (Vector X))`. The DEPLOYED producer `schema-rust@7f746c02` pins
`schema@a393c8c8` (verified in its `Cargo.lock`), which RETIRED that form — a first
signal-domain-criome build reproduced `RetiredStructFieldSyntax { …Addresses…Vector…Address… }`
on `(Addresses (Vector Address))`. The transform was corrected to the trailing-dot
`role.(Composite)` form and re-validated end-to-end.

Transform implemented as a NOTA-aware span-rewrite (`scratchpad/transform.py`): only `{}`
blocks nested at depth ≥ 1 are touched; formatting/comments preserved; every produced
schema was diff-reviewed field-by-field.

## Verification model

Per-repo `nix build 'github:LiGoldragon/<repo>/<exact-rev>#packages.x86_64-linux.default'`
on the prometheus builder, pinned to the EXACT pushed rev (branch resolution is cached;
`--refresh`/exact-rev required or nix reuses the stale lock). "Past schema-compile" =
the `build.rs` panic is no longer `RetiredStructFieldSyntax`/`RedundantExplicitFieldRole`
(schema parse+lower+generate at `build.rs:29` succeeds); the next failure is the SEPARATE
`StaleGeneratedArtifact` regen gate (`build.rs:31`, its own bead) or a downstream compile —
neither in this bead's scope. A whole-graph re-verify is the later convergence step.

## Per-repo disposition (drop-next tip after edit · prometheus build)

All 9 own-drift builds pinned to the exact pushed rev. "PAST-SCHEMA" = retired-count 0
and the panic moved to the separate `StaleGeneratedArtifact` regen gate (own bead).
"CASCADE-BLOCKED" = the repo's OWN generation is not what fails; a stale-pinned PRODUCER
dependency (its `Cargo.lock` still pins the pre-fix producer rev) fails its own retired
schema first, before this repo's `build.rs` runs. Clearing it is the whole-graph
lock-rebump convergence step, out of this bead's scope.

| repo | schema file(s) fixed | drop-next tip | prometheus build |
|---|---|---|---|
| signal-domain-criome | schema/lib.schema | `00f43ba8a8ed` | **PAST-SCHEMA** (build.rs:31 StaleGeneratedArtifact; retired 0) |
| signal-cloud | schema/lib.schema | `988c769df5b1` | **PAST-SCHEMA** (build.rs:31 StaleGeneratedArtifact; retired 0) |
| meta-signal-persona | schema/lib.schema | `2cfc27a522c6` | **PAST-SCHEMA** (build.rs:42 StaleGeneratedArtifact; retired 0) |
| meta-signal-upgrade | schema/lib.schema (+guard test) | `003bef5b10c6` | **PAST-SCHEMA** (StaleGeneratedArtifact; retired 0) |
| signal-upgrade | schema/lib.schema (+guard test) | `b8b3f818b0fb` | **PAST-SCHEMA** (StaleGeneratedArtifact; retired 0) |
| meta-signal-cloud | schema/lib.schema | `4b95bc7e32ef` | own-fixed; CASCADE-BLOCKED on `signal-domain-criome@3aca3282` (stale dep pin) |
| meta-signal-domain-criome | schema/lib.schema | `2d7f63a48a3f` | own-fixed; CASCADE-BLOCKED on `signal-domain-criome@3aca3282` |
| domain-criome | schema/sema.schema | `9ed98cc2b4be` | own-fixed; CASCADE-BLOCKED on `signal-domain-criome@3aca3282` |
| upgrade | schema/lib.schema | `70d15dcb9d63` | own-fixed; CASCADE-BLOCKED on `meta-signal-upgrade@92825f31` (stale dep pin) |
| lojix | schema/nexus.schema, schema/sema.schema | `c9344e1b41b2` | own-fixed; CASCADE-BLOCKED on `signal-lojix@4db768af` — see BLOCKER below |
| persona | — (own schema/daemon.schema is empty `{}[][]{}`) | (unchanged) | NO OWN DRIFT — cascade-only; fix lives in meta-signal-persona (PAST-SCHEMA) |

The stale pins (`3aca3282`, `92825f31`, `4db768af`) are the pre-fix producer `drop-next`
tips: each consumer's `Cargo.lock` pins the exact producer rev, so even a `branch=drop-next`
dep resolves to the locked (retired) rev under `--locked`. Once the synchronizer
`staged-cascade` re-locks consumers to the fixed producer tips above, the 5 cascade repos'
OWN (identically-transformed) schemas will surface and clear — the shared dependency
`signal-domain-criome@00f43ba8` is already proven PAST-SCHEMA, which is exactly the schema
3 of them import.

## BLOCKER — retired-syntax bucket is under-enumerated (out-of-list producers)

`lojix`'s cascade dependency **`signal-lojix`** carries the SAME retired struct-field
drift (`schema/lib.schema` on drop-next: `{ policy SourceRevisionPolicy … }`,
`DatabaseMarker { CommitSequence * StateDigest * }`, `(Vec …)`) yet is NOT in bead
5kxh's 11-repo list — it was masked as "no-flake (false-fail)" in the A checkpoint
(couldn't build standalone, so its schema drift was never surfaced). `meta-signal-lojix`
(and possibly other no-flake `signal-*`/`meta-signal-*` contracts) likely share this.
`lojix` cannot reach green until these are also transformed. Recommend extending the
schema-drift scope (or a follow-up bead) to sweep every `signal-*`/`meta-signal-*`
contract `.schema` for the retired forms, not only the 11 that happened to surface a
standalone `nix build` failure.

## Guard-test fixes (bead zy24 overlap)

`signal-upgrade` and `meta-signal-upgrade` `tests/dependency_boundary.rs`: the stale
POSITIVE assertion `tree.contains("nota-next")` (message "nota-text feature should pull
nota-next") → `tree.contains("nota")` / "…pull nota". The LEGITIMATE negative boundary
guard `for forbidden in ["nota-next","nota-codec","signal-core"] { !tree.contains(...) }`
was left LITERAL (it asserts the tree no longer contains the token — still passes
post-rename). These crane-check assertions only run once the upstream retired-syntax +
regen blockers clear; the literal is now post-rename-correct.

`signal-terminal` (the third zy24 literal) is owned by another worker — NOT touched here;
zy24 stays open for it.

## Safety

No migration `main` moved. Every edit is a single commit added on top of each repo's
existing `drop-next` (parent = the synchronizer `cascade dependency bumps` tip), bookmark
moved and pushed on `drop-next` only, via `jj git push --bookmark drop-next`. All work in
the canonical `/git/github.com/LiGoldragon/<repo>` checkouts, each claimed via Orchestrate
lane `schema-drift`, each verified clean (no peer WIP) before editing. `cloud` (Codex
cloud-maintainer claim) is not in scope and was not touched.
