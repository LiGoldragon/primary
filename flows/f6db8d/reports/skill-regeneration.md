# Regenerating .agents/.claude/.codex/.pi for the disable-model-invocation fix — blocked

Delegated by main flow f6db8d, following `FLOW_DIRECTORY/reports/recent-vision.md`
item 3: witness that `nix run .#check-skills` confirms the deployed trees are
stale by one regeneration, then run `nix run .#generate-skills` and commit the
result, having confirmed no authored source changed. **The check does not pass
against the current Curriculum content; regeneration could not be run.**

## What was read

- `/home/li/primary/flake.nix:21-29` — `curriculum-deploy` pinned at
  `c669b27b464f652edd1c1f812e6b7fd20b941ab7`, `curriculum` pinned at
  `a7d2f4f1fc57c2376ae041288d05b55ab7577052`.
- `/home/li/primary/flake.nix:49-81` — the `check-skills` / `generate-skills`
  apps, each `exec curriculum-deploy "$1"` with one inline Datom request.
- `git -C /git/github.com/LiGoldragon/curriculum-deploy log -1` — HEAD detached
  at `c669b27`, matching the pin; `git status` clean.
- `git -C /git/github.com/LiGoldragon/Curriculum log -1` — HEAD detached at
  `a7d2f4f`, matching the pin; `git status --porcelain` shows only a
  pre-existing, unrelated `D result` (a tracked build-symlink artifact,
  already deleted in the working tree before this flow touched anything).
- `curriculum-deploy/src/runtime.rs:107-113,272-303` — `Request::execute`
  dispatches `Check`/`Generate`/`Visualize`, each taking `data_root` and
  `workspace_root`; `Deployment::read` loads every `skills/*.md` file and
  `data_root.join("roles.datom")`, parsing the latter as raw Datom/Protos text
  with no comment stripping.
- `curriculum-deploy/tests/runtime.rs:246-252` — the CLI request shape is
  `Generate.{{ «path» «path» }}` (guillemet-quoted paths).
- `curriculum-deploy/Cargo.lock:64-66,244-246` — this build resolves
  `datom-codec 0.25.6` at `f2cc0685…` and `protos 0.29.1` at `b543678c…`.
- `protos` (checked out at the pinned rev `b543678c`) `src/core.rs:447-459` —
  `space()`: after skipping whitespace, if the next glyph is `;` it consumes
  everything up to (not including) the next `\n` as a line comment, in a loop.
  `src/core.rs:21-24` — `Boundary` has exactly two variants, `Guillemets` and
  `Parentheses`; there is no quote boundary for `“ … ”`.
- `/git/github.com/LiGoldragon/Curriculum/roles.datom` — every human-readable
  description is wrapped in typographic `“ … ”` quotes (U+201C/U+201D), not
  guillemets, and several descriptions contain an ordinary mid-sentence
  semicolon, e.g. `“The brief is your authority. Decide what it settles;
  return what it does not.”`.
- `orchestrate 'Observe.Locks'` — lock `851 CurriculumDeployDatomMigration`,
  held by flow `542442`, path
  `/home/li/wt/github.com/LiGoldragon/curriculum-deploy/datom-codec-542442`,
  “Migrate direct Datom consumer”, still open.
- `/home/li/primary/flows/162eb3/log.md:11` (relayed, written by a different
  flow) — “Regeneration of primary's trees is blocked by the in-flight
  Curriculum roles.datom migration (flow 542442, lock 851); live trees
  unchanged.”

## What was run

- `nix run .#check-skills -- 'Check.{ «/git/github.com/LiGoldragon/Curriculum» «/home/li/primary» }'`
  → `Error.{ Protos [] Structural.ProtosError.{ Extent.{ 133 2150 } Unclosed.«{» } }`
  (2150 is exactly the byte length of `roles.datom`; 133 is the byte offset of
  the outermost `Roles.{` — the parser reaches end of file still inside that
  one open brace).
- The same request against a scratch copy of `roles.datom` with its leading
  `;`-comment line removed gave the same shape of error (`Unclosed.«{»`,
  extent ending at EOF), ruling out the header line as the cause.
- The same request against a scratch copy with every `;` inside the quoted
  descriptions replaced by `,` **no longer produced a Protos structural
  error** — it produced a different, later-stage error
  (`Error.{ Composition [ 1 0 0 ] Arity.{ 2 15 } }`, a `datom-codec`
  positional-arity mismatch, expected given the crude byte-for-byte edit).
  This isolates the cause to protos's `space()` treating a bare mid-sentence
  `;` as a line-comment opener, which swallows the remainder of that line —
  including the `}` meant to close the enclosing record — because `“ … ”`
  are not real string boundaries in the pinned protos grammar (only `«…»`
  is), so nothing protects the semicolon from being read as a comment.
- `git -C /git/github.com/LiGoldragon/Curriculum status --porcelain` and
  `git -C /git/github.com/LiGoldragon/Curriculum diff --stat -- skills roles.datom`
  before and after this work: the only dirty entry is the pre-existing
  `D result`; the diff over `skills` and `roles.datom` is empty. No authored
  source was touched by this flow (all edits described above were made to
  throwaway copies under this flow's scratchpad, never inside the Curriculum
  checkout).
- `generate-skills` was never invoked: there is nothing safe to regenerate
  from while `check-skills` cannot even read `roles.datom`, so no witness of
  a before/after change to `.claude/skills/main-flow/SKILL.md` was produced.
  Read directly: `/home/li/primary/.claude/skills/main-flow/SKILL.md:1-3` still
  carries `user-only: true`, and `disable-model-invocation` appears nowhere
  under `.agents/`, `.claude/`, `.codex/`, `.pi/` except as prose in
  `skill-designing/SKILL.md:53` — i.e. the deployed trees are exactly as
  `recent-vision.md` item 3 described them, unchanged by this flow.

## Conclusion (this flow's inference)

`recent-vision.md` item 3 is correct that the generator fix
(`curriculum-deploy/src/runtime.rs:247-248`) is already pinned by
`flake.nix:22` and that no authored skill source needs to change. It did not
itself run `check-skills`, and the premise that regeneration is a single
mechanical step does not hold: `check-skills`/`generate-skills` fail before
they ever reach the generator-fix code path, because `Curriculum/roles.datom`
cannot be parsed by the protos version this build of `curriculum-deploy`
resolves. This reproduces, independently, the same blocker `flows/162eb3/log.md:11`
already named (Orchestrate lock 851, `CurriculumDeployDatomMigration`, owned
by flow 542442) — that migration has not landed on `curriculum-deploy` main,
and `roles.datom`'s typographic `“ … ”` quoting is not valid text under the
protos grammar this main currently pins.

Fixing `roles.datom` (or landing 542442's migration) is outside this flow's
delegated scope and outside `primary`: it is Curriculum-repository authored
content and a separate in-flight migration owned by another flow. No fix was
attempted. No regenerated trees were produced, so no `.agents`/`.claude`/`.codex`/`.pi`
commit was made.

## Sources

- `/home/li/primary/flake.nix`
- `/git/github.com/LiGoldragon/curriculum-deploy` (`src/runtime.rs`, `tests/runtime.rs`, `Cargo.lock`), detached at `c669b27b464f652edd1c1f812e6b7fd20b941ab7`
- `/git/github.com/LiGoldragon/protos` (`src/core.rs`), detached at `b543678cfc8609529cea7174eb4af8a64daa54ad`
- `/git/github.com/LiGoldragon/Curriculum` (`roles.datom`, `skills/`), detached at `a7d2f4f1fc57c2376ae041288d05b55ab7577052`
- `orchestrate 'Observe.Locks'` (run by this flow)
- `/home/li/primary/.claude/skills/main-flow/SKILL.md`, `/home/li/primary/.claude/skills/skill-designing/SKILL.md`
- `/home/li/primary/flows/162eb3/log.md:11` (relayed)
- `/home/li/primary/flows/f6db8d/reports/recent-vision.md` item 3 (relayed brief)
