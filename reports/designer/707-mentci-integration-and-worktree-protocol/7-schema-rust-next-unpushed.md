# Investigation 7 — the schema-rust-next unpushed work

Read-only forensic pass. No repo, worktree, or bookmark was mutated. `git
fetch origin` ran in `/git/github.com/LiGoldragon/schema-rust-next` and
`/git/github.com/LiGoldragon/schema-next` before the freshness-sensitive
checks (FETCH_HEAD 2026-06-20 19:00 +0300).

## Question

Two worktrees under `/home/li/wt/github.com/LiGoldragon/schema-rust-next/`
hold unique unpushed commits flagged must-not-lose:

- `reaction-expand` — `8b147fac` (thread shape resolver + standard struct
  impls), `a1582dfd` (660/661 composition prototype)
- `structural-forms-integration` — `a0138ce1` (migrate fixtures to
  positional struct-body syntax); its bookmark is diverged from origin
  ahead-5 / behind-5

For each: age + session-break check, what the work implements, whether it
(or an equivalent) is already on `origin/main`, the owner, and a verdict
(preserve / archive / broken-remnant) with the safe action.

## Bottom line

| Worktree | On main? | Verdict | Safe action |
|---|---|---|---|
| `reaction-expand` (`8b147fac`, `a1582dfd`) | NO — a different design direction main did not take | (1) genuinely-unique-at-risk | **Push to preserve** the schema-rust-next consumer onto a `next/` bookmark; the schema-next half is already on origin |
| `structural-forms-integration` (`a0138ce1` + stack) | YES — superseded; main carried the migration further and the one src delta is byte-identical on main | (2) already-on-main / superseded | **Archive** (forget workspace). Nothing unique is at risk |

Both worktrees are clean sessions — no aborted/undone jj op, no conflict.
The "broken mid-work" hypothesis is **not** supported by the op log for
either.

## Worktree A — `reaction-expand`

### (a) Age and session integrity

- `a1582dfd` "base: 660/661 composition prototype" — authored 2026-06-16
  12:16 +0200, committed 2026-06-16 20:29 +0200.
- `8b147fac` "schema-capability-resolution: thread shape resolver +
  standard struct impls" — authored 2026-06-16 20:47 +0200, committed
  2026-06-16 20:48 +0200.

So roughly **4 days old** (today 2026-06-20). The jj working copy is
`43e7dc0f` — empty, no changes, parent `8b147fac`. The shared op log
shows the reaction-expand session as a clean tail (3 days ago):
`commit … -> create bookmark next/schema-capability-resolution -> point
bookmark -> edit 8b147fac -> a89ef284 edit 43e7dc0f (the empty working
copy)`. There is **no** `abort`, `undo`, `abandon`, `restore`, or conflict
op anywhere in the reaction-expand portion of history. The session ended
deliberately on an empty working-copy commit — it was *parked*, not
broken.

Note: `8b147fac` shows as `(divergent)` in `jj log`. Its twin is
`0b17e901` (carries the local bookmark `next/schema-capability-resolution`
in schema-rust-next). `git diff 8b147fac 0b17e901` is **empty** — same
tree, two change-ids. Not a conflict, just a jj divergence.

### (b) The work

`a1582dfd` (+2096/−56, 14 files) lays the composition base: adds
`impls: Vec<RustImpl>` to `RustModule`, an `emit_impl` loop that lowers
the `{| |}` trait/impl constructs to real `impl` blocks, a pipe-delimiter
demo, and the 660/661 composition fixtures.

`8b147fac` (+1293/−115, 15 files) is the architecturally load-bearing
commit. It threads the schema type graph into `RustLoweringContext`
(`with_declarations`) and, in `impl LowerToRust<RustImpl> for
ImplDeclaration`, builds a **`schema_next::CapabilityResolver`** from the
carried declarations + the impl's target, then projects each method body
through it (`method.body().to_rust(resolver)`). It adds
`StructInherentImplTokens` — every concrete multi-field struct emits an
all-fields `new` plus a per-field borrow accessor by default — and
replaces a generation panic with a `compile_error!` path.

This is a **shape-derived capability resolver** replacing the old
name-allowlist resolver. It is one half of a paired prototype: the
schema-next half is `schema-next` commit `3709fc1`
"schema-capability-resolution: shape-derived capability resolver replaces
name allowlist" (authored 2026-06-16 20:48 +0200), and the
`reaction-expand` Cargo.toml carries a
`[patch."…schema-next.git"] schema-next = { path =
"../../schema-next/reaction-expand" }` pin pointing at a local schema-next
worktree of that branch.

### (c) Already on main? — NO, a different direction

`8b147fac` and `a1582dfd` are **not ancestors** of `origin/main`.
`git cherry origin/main 8b147fac` marks both `+` (no equivalent on main).
Merge-base is `9ffa588d` (2026-06-16 morning); main has since advanced 11
commits down a **different path**. `git range-diff 9ffa588..8b147fac
9ffa588..origin/main` shows **zero** correspondence — the two
reaction-expand commits map to nothing on main, and main's 11 commits map
to nothing in reaction-expand. They are independent lines.

The two lines solve the *same* problem (standard-impl emission /
composition resolution) with **competing designs**:

- `origin/main` took the **impl-catalog** route: `90d853c`
  "consume the `{| |}` impl catalog + typed malformed-name errors", driven
  by `referenced_impls` / `EmittedRustSurface` / `verify_catalog`
  (22 references in main `src/lib.rs`), pinned to schema-next main
  `4b7e830a`.
- `reaction-expand` took the **CapabilityResolver** route
  (`CapabilityResolver`, `StructInherentImplTokens` — **0** references on
  main), pinned to a local schema-next checkout of the unmerged
  `next/schema-capability-resolution` branch.

So this is genuinely-unique work, not on main, representing a design
direction the project consciously did not merge.

### Pushed-state and the dependency risk

- schema-rust-next consumer: the bookmark
  `next/schema-capability-resolution` (twin `0b17e901`, identical content
  to `8b147fac`) exists **only locally**. `git ls-remote origin` shows
  `next/reaction-frame-emission` on origin but **no**
  `origin/next/schema-capability-resolution`. The consumer side is the
  genuinely-at-risk artifact.
- schema-next half: `origin/next/schema-capability-resolution` (`3709fc1`)
  **is** on origin (not on schema-next main). The API this consumer needs
  IS preserved remotely — pushed schema-next *main* does **not** define
  `CapabilityResolver` (0 grep hits), so the consumer only builds against
  the `next/` branch, not against any pushed main.

### (d) Owner

Author `li <li@goldragon.criome.net>` (committer same) on host
`li@ouranos` per the op log — the workspace machine identity, not a lane
attribution. The work is schema-toolchain / Rust-emitter
(`schema-rust-next` consuming a new `schema-next` API), which is
**nota-designer / system-designer** territory; both lane locks are
currently empty, so no live claim. Co-author trailer:
`Claude Opus 4.8 (1M context)`. The paired branch names
(`next/schema-capability-resolution` on both repos) confirm a single
designer-lane cross-repo session.

### Verdict A — (1) genuinely-unique-at-risk → preserve

Push the consumer to a `next/schema-capability-resolution` bookmark on
schema-rust-next origin (mirroring the already-pushed schema-next branch
of the same name), so the paired prototype is durable on the remote. Do
**not** archive — this is the only copy of the consumer side, and it
embodies a real alternative design that informs the pending decision
between the catalog route (on main) and the resolver route. Route the
"which design wins" question to the schema-toolchain owner
(nota-designer / system-designer); preservation is the safe action
regardless of that outcome. (Note for whoever pushes: the local-path
`[patch]` to `../../schema-next/reaction-expand` must be repointed to the
pushed `next/schema-capability-resolution` schema-next branch before it
builds anywhere but the original machine — the referenced local worktree
no longer exists; only `impl-reference-syntax` and
`structural-forms-integration` schema-next worktrees are present.)

## Worktree B — `structural-forms-integration`

### (a) Age and session integrity

- `a0138ce1` "migrate fixtures to positional struct-body syntax …" —
  authored 2026-06-15 17:43 +0200, committed 2026-06-16 14:18 +0200.
  Roughly **5 days old**.

The jj working copy `@` sits **on** `a0138ce1` and reports as dirty
(23 files modified). This is **snapshot noise, not new work**: every
sampled dirty file (`spirit-min.schema`, `src/daemon_emit.rs`,
`tests/family_emission.rs`, `collections.schema`, `plane-triad.schema`,
`Cargo.lock`) is **byte-identical** (sha256) to the committed `a0138ce1`
blob — same 23-file footprint, same `field.Type` form. No unique
uncommitted work is hiding in the working copy. The op log shows a
deliberate `restore into 18f5bd6d` (a normal jj restore), bookmark pushes,
and bookmark moves — **no** abort/undo/abandon/conflict. Clean, parked
session.

### (b) The work

`a0138ce1` (+174/−159, 23 files) migrates every schema fixture from the
old struct-body grammar to a positional `name.Type` field syntax (e.g.
`Entry { Topics kind.Kind description.Description magnitude.Magnitude }`),
advances the schema-next pin to the positional integration tip, and adds
one small `src/daemon_emit.rs` change: a `working_streams: bool` field on
`NexusDaemonShape` with builder/accessor.

### (c) Already on main? — YES, superseded

`a0138ce1` is **not an ancestor** of `origin/main` and sits 1-ahead /
13-behind it. But the *substance* is on main and then some:

- **Fixture migration completed further on main.** Same `spirit-min.schema`
  `Entry` line:
  - `a0138ce1`: `Entry { Topics kind.Kind description.Description
    magnitude.Magnitude }` (intermediate `name.Type` form)
  - `origin/main`: `Entry { Topics Kind Description Magnitude }` (pure
    positional / derived-name form)

  Main's `90d853c` commit message states it migrated "every schema fixture
  … to the new positional / field.Type / derived-name grammar." So
  `a0138ce1` is an earlier, less-complete stage of the same migration that
  main has already carried past.

- **The one source delta is identical on main.** `a0138ce1`'s
  `src/daemon_emit.rs` (the `working_streams` field) is **byte-identical**
  to `origin/main:src/daemon_emit.rs` (0 diff lines on `working_streams`;
  the whole file matches). `working_streams` lives on main at lines
  46/57/67/95/306.

- **The divergence is a re-pushed twin stack, not lost work.** Local
  `a1b8adff` vs `origin/structural-forms-integration` (`10db4e5a`) is
  ahead-5 / behind-5. `git range-diff` shows the two 5-commit stacks are
  the **same logical stack** with different hashes: commits 2–5 are
  **identical** (`=`); only commit 1 differs — local `a0138ce` carries the
  extra `daemon_emit.rs working_streams` change that the origin twin
  `ab9d16b` lacks, and that change is *already on main anyway*. So the
  ahead-5 side is a re-commit of work whose only unique bit is redundant
  with main, and the behind-5 side is the already-pushed copy.

### (d) Owner

Same identity: author `li <li@goldragon.criome.net>`, host `li@ouranos`,
Co-author `Claude Opus 4.8`. Schema-toolchain fixture/grammar work →
nota-designer / system-designer lane (locks empty, no live claim). The
schema-next half is fully on origin: both `origin/structural-forms-
integration` and `origin/next/structural-forms` exist.

### Verdict B — (2) already-on-main / superseded → archive

Nothing unique is at risk. The positional-syntax migration is on main in a
more advanced form; the lone `daemon_emit.rs` addition is byte-identical on
main; the bookmark divergence is a twin of an already-pushed stack. Safe
action: **archive** — `jj workspace forget structural-forms-integration`
and let the diverged local `structural-forms-integration` bookmark be
dropped (the must-not-lose flag was a false positive driven by the
ahead-5/behind-5 divergence display). No push needed; no content would be
lost. The dirty working copy is snapshot noise, not unsaved work.

## Method notes

- The `/home/li/wt/.../schema-rust-next/*` directories are **jj
  workspaces** with no `.git`; git inspection runs from the colocated
  store at `/git/github.com/LiGoldragon/schema-rust-next`, jj inspection
  via `jj -R <workspace>`.
- "Already on main" was tested four ways: `merge-base --is-ancestor`,
  `git cherry`, `git range-diff` (structural correspondence), and direct
  `git show <ref>:<path>` content diffs / `git grep` for the concept
  identifiers — not just subject-line matching.
- A third worktree `family-identity-newtype` exists in the same parent dir
  but is out of scope for this investigation and was not analysed.
