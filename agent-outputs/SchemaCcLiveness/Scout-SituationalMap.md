# Scout Situational Map — Is `schema-cc` Live or Dead?

## Task and scope

Read-only investigation: determine whether the standalone repo at
`/home/li/primary/repos/schema-cc` (`/git/github.com/LiGoldragon/schema-cc`,
"schema-cc engine + migration design", carrying a stale ~1019-line uncommitted
diff) is a LIVE part of the stack or effectively dead/superseded. No edits made.

## Verdict

**The standalone repo `LiGoldragon/schema-cc` is DEAD / SUPERSEDED.** Its idea is
LIVE, but it now lives as an **in-tree workspace member inside the `schema-next`
repo** (`repos/schema-next/schema-cc/`), not as the separate repository the brief
points at. Nothing depends on the standalone repo; the deployed system compiles
the `schema-cc` crate **from the `schema-next` git checkout**.

Disposition recommendation: **RETIRE the standalone repo** like `lojix-cli` (do
NOT process its INTENT/doctrine as a live repo — that intent already lives in
`schema-next`). See "Recommended disposition" below.

## The crucial fact: there are TWO `schema-cc`s

| Copy | Path | State | Used? |
|---|---|---|---|
| **Standalone repo** | `repos/schema-cc` → `/git/github.com/LiGoldragon/schema-cc` | Genesis commit (Jun 15) + uncommitted ~1019-line prototype diff; **frozen** | **No dependents** |
| **In-tree member** | `repos/schema-next/schema-cc/` (workspace member of the `schema` repo) | Committed, wired, last touched Jun 30 | **YES — live, builds into the deployed system** |

These are distinct working copies with distinct git histories. The standalone
repo's intent (the compiler-compiler design) was carried forward into the in-tree
member, which then diverged and became the real one.

## Observed facts — evidence

### DEPENDENCY: nobody depends on the standalone repo

- Grep for a git dependency on the standalone repo across all `*.toml`/`*.nix`/
  `*.lock` in `repos/` (excluding `private-repos/`):
  `grep -rI "schema-cc.git\|LiGoldragon/schema-cc"` → **zero hits.** No Cargo
  `git=` dep, no flake input points at `github.com/LiGoldragon/schema-cc`.
- No cargo git checkout exists for a standalone schema-cc:
  `ls /home/li/.cargo/git/checkouts/schema-cc*` → **no matches.**
- The only `schema-cc` Cargo dependency in the whole tree is in
  `repos/schema-next/Cargo.toml`:
  ```
  [build-dependencies]
  schema-cc = { path = "schema-cc" }   # workspace path member, NOT git
  ```
  and `members = ["schema-cc"]` in its `[workspace]`. It is a **path** dep on the
  co-located member, explicitly NOT a sibling repo (the comment in
  `schema-next/Cargo.toml` says so verbatim).

### SUPERSESSION: how it relates to the "next" line

The intended layering (from `schema-cc/ARCHITECTURE.md` and `INTENT.md`) is:

```
nota-next  (frozen seed)
   ▼
schema-cc  (the compiler's definition as typed data — emits the resolver)
   ▼
schema-next / schema-rust-next  (the generated compiler: resolution, lowering, Rust emission)
```

So `schema-cc` is **upstream of** `schema-next`, not a competing/old engine — it
is a build-time generator that emits part of `schema-next`'s source. It is NOT
superseded *by* schema-next conceptually; rather the **standalone repo** was
superseded by folding the same crate into the `schema-next` repo as a workspace
member. Note also a naming drift: `schema-next` is the repo, but its crate is now
`name = "schema"` (v0.2.0) and `schema-rust-next`'s crate is `name = "schema-rust"`
(v0.5.3) — a commit in schema-next reads "schema: drop next from crate names".
The "-next" repos are the live line; the crates have shed the "next" suffix.

### STATUS: what the docs say

- The standalone repo's own `INTENT.md`/`ARCHITECTURE.md`/`AGENTS.md` describe it
  as **active/experimental v0 prototype** ("The prototype proves the
  ReferenceGrammar → resolver generation path... Re-wiring schema-next to consume
  the generated resolver... are the staged next steps in report 652"). They do
  **not** mark it archived — but that is because those docs predate the move
  in-tree. The standalone repo was frozen at genesis; the work continued
  elsewhere.
- The in-tree member (`schema-next/schema-cc/`) reflects the **completed** version
  of that "next step": `schema-next/build.rs` already decodes
  `schemas/reference-grammar.nota`, validates via `ValidatedReferenceGrammar`, and
  emits `src/reference_resolver_generated.rs` (a committed, freshness-gated file
  that the library `include!`s). That generated file **exists**
  (`schema-next/src/reference_resolver_generated.rs`, 2489 bytes, Jun 23). So the
  v0 boundary described in the standalone repo's ARCHITECTURE is **already crossed**
  in `schema-next`.

### The stale ~1019-line uncommitted diff (what it is, how old)

In `repos/schema-cc` (`jj st`):
- Working copy `@` = change `mknnrpyw 36a15f77`, description: *"schema-cc:
  ReferenceGrammar prototype, hardened per operator 384 — precedence-as-data
  generates the resolver; validation enforces the coherent shape...; repo contract
  files (AGENTS/CLAUDE/skills)"*.
- Parent `@-` = `kxuqvymy 68fdb60f` *"schema-cc: genesis — INTENT, ARCHITECTURE,
  Cargo skeleton"*, committer timestamp **2026-06-15**.
- The ~1019-line diff (`jj diff --stat`: 11 files, +1019/-6) is the **prototype
  implementation itself**: `src/grammar.rs` (250), `src/generate.rs` (200),
  `src/validate.rs` (95), `src/error.rs` (51), modified `src/lib.rs`, plus
  `tests/{grammar,validate,generate}.rs` and the repo contract files
  (AGENTS.md/CLAUDE.md/skills.md). Working-copy timestamp **2026-06-15 21:02** —
  this work has sat uncommitted/un-pushed for ~2 weeks while the same prototype
  was re-done and committed in `schema-next/schema-cc/`.
- It is **divergent**, not a copy: `schema-cc/src/grammar.rs` differs from
  `schema-next/schema-cc/src/grammar.rs`; the in-tree member has `dispatch.rs` and
  drops `generate.rs`; the standalone uses dep `nota-next = {...}` while the in-tree
  member uses the aliased `nota = { package = "nota", ... }`. The in-tree copy is
  the further-evolved one.

### DEPLOYMENT: the deployed system uses the in-tree copy, never the standalone

- `repos/spirit/Cargo.lock` lists a `schema-cc` package, and the spirit build
  artifact dep-info file
  (`spirit/target/debug/deps/schema_cc-*.d`) resolves the compiled
  `schema-cc` sources to:
  ```
  /home/li/.cargo/git/checkouts/schema-next-4ae53b43a00d83d7/dea9b55/schema-cc/src/{lib,dispatch,error,grammar,validate}.rs
  ```
  i.e. the `schema-cc` crate that ships into spirit comes from the **schema-next
  git checkout**, transitively (spirit → schema/schema-rust → schema-next
  workspace which build-depends on its `schema-cc` member). The standalone repo is
  not in that path.
- `spirit/flake.nix` (lines ~364-365) `substituteInPlace`s
  `$out/vendor-sources/schema/schema-cc/Cargo.toml` — again the schema-cc that
  lives **under `vendor-sources/schema/`** (the schema-next vendored tree), not a
  standalone vendored repo.
- `skills/flake.nix` and `skills-primary-ascl-doctrine/flake.nix` declare
  `schema-cc = { path = "vendor-sources/schema/schema-cc" }` — once more the
  in-tree member under the vendored `schema` source, populated by
  `cp -R ${schema-source} "$out/vendor-sources/schema"`. (The
  `vendor-sources/` dirs are build-time populated and not present in the working
  tree, so this is the declared wiring, not a proven on-disk file.)

### Retirement precedent: `lojix-cli`

The brief cites `lojix-cli` as the "retire it" precedent. Confirmed it is already
retired: `repos/lojix-cli` is a **dangling symlink** (target
`/git/github.com/LiGoldragon/lojix-cli` is missing), and no `*.toml` in `repos/`
references `lojix-cli`. That is the shape "retired repo" takes here: dependents
removed, then the clone dropped.

## Interpretations (clearly separated from facts)

- The standalone `schema-cc` repo was the **birthplace** of the compiler-compiler
  idea (genesis + a hardened prototype, Jun 15). The decision was then taken to
  **co-locate it as a workspace member of `schema-next`** (the comment in
  `schema-next/Cargo.toml` is explicit: "schema-cc is co-located as a workspace
  member, not a sibling repo"). The standalone clone was left behind with its
  prototype uncommitted.
- Therefore the standalone repo is a **dead fork/origin**: its design intent is
  fully alive, but the *repository* is superseded by the in-tree member. Treating
  the standalone repo as a live repo to process INTENT/doctrine from would be
  processing a stale duplicate of intent that already governs `schema-next`.

## Recommended disposition

- **Retire the standalone repo** `LiGoldragon/schema-cc` like `lojix-cli`: drop the
  `repos/schema-cc` symlink (and the clone) once the psyche confirms the in-tree
  member is canonical. Do **not** run the normal "process this repo's
  INTENT/doctrine" flow on it — that would duplicate intent already manifested in
  `schema-next`.
- Before dropping, **salvage check** the ~1019-line uncommitted diff: confirm the
  in-tree `schema-next/schema-cc/` already contains everything valuable from the
  standalone prototype (it appears further-evolved — has `dispatch.rs`, the
  freshness-gated build.rs path, the live generated resolver — so likely a
  superset, but the divergent `grammar.rs` should be eyeballed by an
  implementer/auditor before discard). The uncommitted diff itself should be
  **discarded, not committed/pushed**, since committing it would push a stale
  duplicate.
- The standalone repo's `INTENT.md`/`ARCHITECTURE.md` reference designer reports
  `649`/`652` and operator review `384`; if those reports are not already pointed
  at `schema-next/schema-cc`, that pointer should be updated there (the live
  surface), not in the dead repo.

## Checks run (exact)

- `ls -la repos/` and `repos/schema-cc/` — inventory and file dates.
- Read `schema-cc/{INTENT,ARCHITECTURE,AGENTS,skills}.md` and `Cargo.toml`.
- `grep -rIl "schema-cc"` over `*.toml/*.nix/*.lock/*.rs/*.md` in `repos/` (minus
  private-repos, minus self) — dependents.
- Per-repo loop over `Cargo.toml`/`flake.nix` for `schema-cc` — found only
  `schema-next` (path member) + skills/spirit vendoring of the in-tree copy.
- `grep -rI "schema-cc.git\|LiGoldragon/schema-cc"` — **zero** git deps on the
  standalone repo.
- `jj st` / `jj diff --stat` / `jj log` in `repos/schema-cc` and
  `repos/schema-next/schema-cc` — the stale diff content and dates.
- `cat schema-next/build.rs`, `schema-next/Cargo.toml`; `ls
  schema-next/src/reference_resolver_generated.rs` and `schema-next/schemas/`.
- `diff` of standalone vs in-tree `src/` listings and `grammar.rs`.
- `cat schema-rust-next/Cargo.toml` (crate `schema-rust` v0.5.3, depends on
  `schema` git = schema-next).
- `ls /home/li/.cargo/git/checkouts/schema-cc*` (none) and `schema-next*` (two);
  read `spirit/target/.../schema_cc-*.d` dep-info — proves compiled origin.
- `grep -n schema-cc spirit/flake.nix`, `skills/flake.nix`.
- Confirmed `repos/lojix-cli` is a dangling symlink (retired precedent).

## Unknowns / not checked / blockers

- **Not run:** any build or test (`cargo build`, `nix build`). Liveness inferred
  from declared wiring + existing build artifacts, not from a fresh successful
  build.
- **vendor-sources/ not on disk:** the `skills`/`spirit` flake `path =
  "vendor-sources/schema/schema-cc"` entries are *declared* surfaces populated at
  build time (`cp -R ${schema-source}`); I did not find a checked-in
  `vendor-sources/` tree to read. The proven runtime origin comes instead from the
  spirit cargo dep-info file pointing at the schema-next git checkout.
- **Spirit intent not queried:** I did not run the `spirit` CLI to read the
  intent records named in the docs (`vpbx` schema-cc, `549v`, `7c71`, `v0n6`,
  `9rjq`). The brief is a repo-liveness scout, and the file evidence is
  conclusive; a curator processing disposition should confirm whether record
  `vpbx` (schema-cc) should be re-pointed at the in-tree member or retired.
- **`private-repos/` not inspected** (boundary; not authorized).
- Whether the in-tree `schema-next/schema-cc/` is a strict superset of the
  standalone prototype is **likely but not byte-verified** — flagged as a salvage
  check for an implementer/auditor before the clone is dropped.
