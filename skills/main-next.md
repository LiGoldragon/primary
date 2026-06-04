# Skill — main and next branches

*Every **code repository under `/git/github.com/LiGoldragon/`** keeps two
long-lived lines: `main` (the integrated line the operator owns) and
`next` (the development line the designer works on). The designer works
on `next`; the operator integrates `next` into `main`.*

## Scope — code repos only, NOT primary

This main-and-next model applies **only to the code repositories under
`/git/github.com/LiGoldragon/`** (`horizon-rs`, `lojix`, `CriomOS`, the
component triads, and so on). It does **not** apply to **primary** — the
workspace coordination repository at `/home/li/primary`. Per psyche
2026-06-04 (record 2585, VeryHigh): on primary everyone always works on
`main` directly — edit, commit, push straight to `main` with the simple
flow ([on primary everyone always works on main directly] — record 2585).
There is no `next` branch on primary and no per-feature branch on
primary. See `skills/jj.md` §"Primary is always main — no branches,
ever". The two-long-lived-lines split below is a code-repo discipline.

## The model

Per psyche 2026-06-04 (record 2561, adopting the idea floated in the
now-superseded record 2544): each **code repo under
`/git/github.com/LiGoldragon/`** keeps two long-lived branches.

- **`main`** — the integrated, canonical line. The operator owns it:
  creates, maintains, and integrates `next` into it. It is the line
  deploys and other repos pin.
- **`next`** — the development line. The designer works here. It is
  long-lived (one `next` per repo, not one branch per feature). The
  operator pulls `next` into `main` when the work is ready, and `next`
  then continues from the new `main`.

Eventually a third long-lived line may be added (record 2561 leaves that
open); the model is `main` + `next` for now.

## How the designer works

- **The designer's home is `next`.** When starting work on a repo, check
  out `next` (in a `~/wt` worktree per `skills/feature-development.md`). If
  `next` does not exist yet, create it from `main` (`jj bookmark create
  next -r main@origin` or branch off `main` in the worktree) and push it.
- **When `main` is locked or busy** — the operator is integrating, or
  another lane holds the claim — the designer works on `next` and never
  blocks on `main`. This is the whole point: `next` is always available.
- **When `main` is free**, the designer may use `main` directly for a
  small, safe change — but the default home is `next`.
- Commit to `next` and push it; the operator integrates `next` → `main`.
  Inline jj messages only (`skills/jj.md`).

## How the operator works

- **The operator owns `main`** and integrates `next` into it when the work
  is ready. After integration, `next` advances from the new `main`.
- This is the steady-state successor to the older per-feature
  `designer-<topic>` concept-branch handoff (`skills/feature-development.md`,
  intent record 515): instead of many concept branches the operator must
  hunt for, there is one `next` per repo carrying the designer's in-flight
  work. Concept branches still exist for genuinely-isolated experiments;
  the steady-state designer line is `next`.

## Why

Two coexisting targets keep the work surface clear: `main` is always the
integrated truth; `next` is always where development lives. The designer
never blocks on a locked `main`, and the operator always knows where to
integrate from. When a component is busy or not production-ready, the
designer makes the change work on `next` rather than stalling.

## See also

- `skills/feature-development.md` — the `~/wt` worktree mechanics the
  `next` branch lives in.
- `skills/jj.md` — commit / push / integrate mechanics; inline messages.
- The deployment-slot vocabulary (a repo named `<x>-next`, or a `next`
  release slot) names the in-flight authored *release line* — related but
  distinct from this per-repo `next` development *branch*.
