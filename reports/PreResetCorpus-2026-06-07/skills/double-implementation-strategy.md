# Skill — double-implementation strategy

*Two parallel implementation tracks for a major architectural break, both
on BRANCHES of the existing repo: one track amalgamates the best of prior
prototypes toward `main`; the other iterates a forward-looking design on a
`next` / feature branch. The two tracks are COMPARED to drive convergence.
Comparison is the integration mechanism; single-track inference drift is
the failure mode this strategy mitigates.*

## Both tracks are branches — never new repos

Per psyche 2026-06-07 (Spirit `op4b` / `53bj`): a major architectural break
is done on **branches**, not by spinning up a new repository. A branch has
no limits — wipe the whole tree, rebuild from scratch, throw it away if it
fails (`skills/feature-development.md` §"A branch has no limits"). The
prior version of this skill routed the two tracks through new repos and
`design-`-prefixed throwaway repos; that produced repo sprawl and is
retired. New repositories are for **genuinely new projects only**
(`skills/repository-management.md` §"When to create a new repository").

## What this skill is for

A major architectural break where multiple prototypes have explored the
same problem from different angles, and the design surface is rich enough
that a single agent working alone would drift via inference. The
double-implementation strategy makes the comparison structural: two agents
in different roles produce two artifacts that are PROVEN convergent or
PROVEN divergent. Divergence surfaces unresolved questions; convergence
signals the design is settling.

## When to apply

- A major break has produced multiple prototype branches
- The design has structural complexity (multiple layers, several open
  shape questions)
- Operator and designer roles both have load-bearing input to the design
- Single-track work would risk inference-driven drift (per intent
  record 735 / 718)

## When NOT to apply

- Routine changes within an existing repo
- Single-layer fixes where one role is clearly authoritative
- Work the psyche has already pinned to one lane explicitly

## The two tracks

### Operator track — `main`

Operator:

1. Works on the repo's **`main`** (in code repos operators own `main`;
   `skills/jj.md`, `skills/main-next.md`).
2. Amalgamates the best ideas from the existing prototype branches into
   `main` as the baseline — reads the prototype reports, cites which
   prototype contributed which piece, integrates into one coherent
   substrate.
3. **Integrates from the designer's `next` branch at the operator's
   discretion** — per Spirit 2556, by rebasing the good parts,
   cherry-picking, re-implementing, or merging the designer branch as-is
   when the code is good. Designer code is not second-class: a clean
   designer `next` branch may be merged to `main` as-is. The choice is
   per-slice on the merits.

### Designer track — the `next` / feature branch

Designer:

1. **Default**: work on the repository's standard **`next` branch** in a
   worktree off the operator's `main` baseline. `next` is the repo's
   designated home for breaking changes — schema reshapes, contract
   reworks, engine ports — not yet safe for `main`. One standing `next`
   branch per repo, rather than a fresh `designer-<topic>-<date>` branch
   per feature. Per Spirit 2556 — [Designer roles work on a standard next
   branch by default in each repository; next is where breaking changes
   happen; operators own main and integrate from next at their discretion.]
   Worktree path per `skills/feature-development.md`:
   `~/wt/github.com/<owner>/<repo>/next/`.
2. **For a contrarian or from-scratch exploration**: use **another
   branch** (a throwaway feature branch in a worktree), not a new repo.
   The branch can wipe the tree and rebuild a different shape from nothing
   — that is exactly what branches are for. Delete the branch after the
   concept integrates or is abandoned. No `design-`-prefixed repos.

## The comparison cadence

Periodically (psyche-triggered or end-of-slice):

1. Designer reads operator's `main`; flags differences from the designer's
   current iteration in a comparison report
2. Operator reads the designer's `next` branch; flags differences from
   `main` in a comparison report
3. Convergent decisions: both lanes agree → the design merges into `main`
   as integration
4. Divergent decisions: surface to the psyche as open shape questions per
   `skills/intent-clarification.md`
5. The convergence report becomes the integration artifact; reports are
   numbered and live in `reports/<lane>/`

## Cleaning up exploration branches

Exploration branches exist for the duration of the design iteration.
Delete the branch (and any `~/wt` worktree) after:

- the concept integrates into `main`, OR
- the design is explicitly retired (the alternative was rejected), OR
- the idea proves unworkable and is abandoned.

Don't let exploration branches accumulate. The point is iteration, not
permanent parallel infrastructure — and never permanent parallel repos.

## Why this works

- **Convergence as signal**: when two independent angles arrive at the
  same shape, the design is empirically reliable
- **Divergence as forcing function**: differences are interview questions
  the psyche or the comparison report must answer
- **Anti-drift**: single-track inference (the failure mode behind the
  schema-defines-effects drift) is mitigated because the other track
  would surface the inference

## See also

- `skills/feature-development.md` — the branch / `~/wt` worktree workflow,
  and "a branch has no limits"
- `skills/repository-management.md` — when a new repository IS justified
  (genuinely new projects only)
- `skills/main-next.md` — the `main` + `next` discipline in code repos
- `skills/jj.md` — `jj` discipline
- `skills/intent-clarification.md` — how to escalate divergence to psyche
- `skills/reporting.md` — where comparison reports land
