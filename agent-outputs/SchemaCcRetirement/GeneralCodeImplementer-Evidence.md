# schema-cc Retirement — Salvage Check and Retirement Evidence

## Task and Scope

Psyche-directed: "retire after salvage-check". Retire the standalone repo
`LiGoldragon/schema-cc` (local clone `/git/github.com/LiGoldragon/schema-cc`,
symlinked as `repos/schema-cc`) which is superseded by the in-tree workspace
member `repos/schema-next/schema-cc/`. Only after confirming the in-tree copy
is a superset (or porting any genuinely unique work) may the local clone and
symlink be deleted. Scope limited to schema-next (any port) and schema-cc
(retirement). private-repos untouched.

## Files / Commands Consulted

- `repos/schema-cc` symlink -> `/git/github.com/LiGoldragon/schema-cc`
- Standalone committed state: `git log` (HEAD = genesis `68fdb60`, src/lib.rs only)
- Standalone uncommitted prototype: `git diff HEAD --stat` (1018 insertions across
  grammar.rs, generate.rs, validate.rs, error.rs, tests, AGENTS/CLAUDE/skills)
- In-tree `repos/schema-next/schema-cc/src/{grammar,dispatch,validate,error}.rs`,
  `tests/{grammar,validate,dispatch}.rs`, AGENTS/CLAUDE/skills
- Normalized diffs (`nota_next`->`nota`, `schema-next`->`schema`,
  `generate`->`dispatch`) between standalone prototype and in-tree.
- `git branch -a`, `git log --all`, `git stash list`, `jj log -r 'all()'`
- `git remote -v`, `jj git remote list`, `gh repo view LiGoldragon/schema-cc`

## Observed Facts

- Standalone git HEAD is the genesis commit (`68fdb60`): only `src/lib.rs`
  skeleton committed. The ~1018-line prototype is uncommitted working tree
  (also carried as jj working-copy commit `36a15f77` on bookmark
  `next/schema-cc`, plus several identical jj operation-log variants).
- `error.rs`: byte-identical to in-tree after `nota_next`->`nota`.
- `validate.rs`: identical to in-tree except one stale doc line (`nota-next`).
- `grammar.rs`: in-tree is a strict superset — adds `BuiltinHead::to_snake_case()`
  (used to name `resolve_<snake>` methods); standalone lacks it. All other
  content identical after rename.
- `generate.rs` (standalone, 200 lines) vs `dispatch.rs` (in-tree, 186 lines):
  the in-tree `dispatch.rs` is the strictly-more-advanced successor. The
  standalone emits an abstract v0 resolver with `todo!()` hooks over invented
  placeholder types (`Resolution`, `ResolveError`, `ReferenceResolver`). The
  in-tree `dispatch.rs` emits dispatch over schema's REAL types (`TypeReference`,
  `SchemaError`, `MacroRegistry`, `MacroContext`, `Block`), wired to schema's
  `resolve_<snake>` methods and the real `from_macro_or_application` tail. The
  in-tree module doc explicitly states it "replaced the v0 standalone resolver,
  which only proved structure and precedence over abstract placeholders with
  `todo!()` arms; that second mechanism could silently drift from the real one,
  so it was retired in favor of this single, consumed emission."
- Test files: `tests/grammar.rs` identical after rename. `tests/validate.rs`
  differs only by rustfmt line-wrapping. Standalone `tests/generate.rs` (183
  lines) tests the retired v0 placeholder resolver — no longer-existing target.
- Contract files (AGENTS/CLAUDE/skills) differ only by stale naming
  (`schema-next`/`nota-next`, an `INTENT.md` read-order line). No unique design.
- Standalone has NO git remote (`git remote -v` and `jj git remote list` both
  empty). `gh repo view LiGoldragon/schema-cc` -> "Could not resolve to a
  Repository" while `gh` auth is healthy (resolved `LiGoldragon/spirit`).
  The repo was never pushed to GitHub; it is local-only.

## Interpretation / Salvage Verdict

The in-tree `repos/schema-next/schema-cc/` is a STRICT SUPERSET of the
standalone in both its committed (genesis) and uncommitted (~1018-line
prototype) state. Nothing in the standalone — including grammar.rs — is unique
and valuable in a form not already present, equal-or-better, in-tree. The
standalone is the retired v0 prototype; the in-tree copy is its consumed,
real-types successor. NOTHING TO PORT.

## Changes Made

None to schema-next. The superset verdict means no port, so no schema-next
commit/push (skipped per the brief's superset branch). No source files edited.

## Retirement Actions

- Remote archive: MOOT. `LiGoldragon/schema-cc` does not exist on GitHub
  (never pushed; no remote configured). `gh repo archive` is not applicable.
- Local clone `/git/github.com/LiGoldragon/schema-cc` and symlink
  `repos/schema-cc`: deleted (see Checks below).

## Safety Confirmation

Inspected every local ref: `git log --all`, `jj log -r 'all()'`,
`git stash list` (empty), untracked files (none). All commits are variants of
the same genesis + ReferenceGrammar prototype already salvage-checked. There is
no remote, so no unpushed-to-remote work can exist beyond local. The only thing
lost by deletion is the accounted-for v0 prototype diff plus the genesis
skeleton, all superseded in-tree. No unexpected valuable work found.

## Checks Run

- `gh repo view LiGoldragon/schema-cc --json isArchived` -> repo does not exist (confirmed local-only)
- Deletion of local clone + symlink -> see chat for exact commands and post-state.
