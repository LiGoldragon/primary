# Skill — double-implementation strategy

*Two parallel implementation tracks for major architectural breaks:
operator amalgamates best-of-prototypes into a new repo's main branch;
designer iterates a forward-looking design in worktree branches or
design-prefixed repos. The two tracks are COMPARED to drive convergence.
Comparison is the integration mechanism; single-track drift is the
failure mode this strategy mitigates.*

## What this skill is for

Major architectural breaks (per `skills/major-break-via-new-repo.md`)
where multiple prototypes have explored the same problem from different
angles, and the design surface is rich enough that any single agent
working alone would drift via inference.

The double-implementation strategy makes the comparison structural: two
agents in different roles produce two artifacts that are PROVEN convergent
or PROVEN divergent. Divergence surfaces unresolved questions; convergence
signals the design is settling.

## When to apply

- A major break has produced multiple prototype branches across repos
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

### Operator track — main branch of new repos

Operator:

1. Creates new repositories per `skills/major-break-via-new-repo.md`
   - Suffix `-next` when the new repo is an upgrade of a previous concept
     (`nota-next` for a successor to `nota`)
   - New name when the new repo introduces a new concept
     (`spirit` replacing `persona-spirit`; `nota-core` for a freshly-named
     structural-library concept)
2. Works directly on the **main branch** of the new repos
   - This is the operator-on-main exception per intent record 816
   - Applies only to fresh repos with no production history
   - Production-track repos retain the standard discipline
     (`skills/jj.md` §"The standard flow")
3. Amalgamates the best ideas from existing prototype branches into the
   new main as the starting baseline
   - Reads the prototype reports
   - Cites which prototype contributed which piece
   - Integrates into one coherent substrate
4. Pushes main as the implementation track's canonical artifact

### Designer track — worktree branches OR design-prefixed repos

Designer:

1. **Default**: worktree branches off the operator's main as the base
   - Branch name follows the standard designer convention:
     `designer-<topic>-<date>` per `skills/feature-development.md`
   - Iterate the design against the operator-baseline; comparison happens
     during integration review
2. **Optional**: create a design-prefixed repository for design exploration
   - Prefix: `design-<concept>` (e.g. `design-nota-core`, `design-asschema`)
   - Use when the design needs its own substrate (not just markdown reports)
     — e.g. a parallel Rust crate exploring a different shape; a fixture
     repo for design comparisons; a sandbox for testing a contrarian idea
   - Design repos are **intentionally deletable**
   - Remove them after the concept integrates into operator main

## The naming conventions

| Prefix / suffix | Lane | Lifetime | Example |
|---|---|---|---|
| `-next` | operator | Long (graduates to canonical name when stable) | `nota-next`, `spirit-next` |
| `core-` | operator | Permanent (parallels `signal-` for privileged contracts) | `core-signal-spirit` |
| no prefix / new name | operator | Permanent | `spirit`, `signal-spirit` |
| `design-` | designer | Short (delete after integration) | `design-nota-core`, `design-asschema` |

## The comparison cadence

Periodically (psyche-triggered or end-of-slice):

1. Designer reads operator's main; flags differences from designer's
   current iteration in a comparison report
2. Operator reads designer's iteration; flags differences from operator's
   current main in a comparison report
3. Convergent decisions: both lanes agree → designs merge into operator
   main as integration
4. Divergent decisions: surface to psyche as open shape questions per
   `skills/intent-clarification.md`
5. The convergence report becomes the integration artifact; reports are
   numbered and live in `reports/<lane>/`

## The deletion discipline for design repos

Design repos exist for the duration of the design iteration. Delete them:

- After the concept integrates into operator main
- OR after the design is explicitly retired (the alternative was rejected)
- OR after the design idea proves unworkable and is abandoned

Track each design repo's deletion target in its `INTENT.md` — "this repo
exists to explore X; deletes when X integrates / is retired."

Don't let design repos accumulate. The point is iteration, not
permanent parallel infrastructure.

## Example workflow (illustrative)

A major break around the NotaCore + schema-stack design:

1. **Operator creates new repos**: `nota-next` branch on `nota`, new
   repo `spirit` (and siblings), keeps work on main branches.
2. **Operator amalgamates** best ideas from prototype branches
   (designer-schema-derived-nota, designer-schema-schema-prototype,
   operator-schema-driven-nota-parser-prototype) into the new mains.
3. **Designer creates** `design-asschema` repo to explore an alternative
   shape for the assembled-schema endpoint that operator's main hasn't
   adopted yet.
4. **Periodic comparison**: designer's `design-asschema` vs operator's
   `schema` main asschema crate. Convergence on most shape; divergence
   on lookup-index strategy.
5. **Integration**: design's lookup strategy proves superior in tests;
   operator absorbs into `schema` main. `design-asschema` deletes.

## Why this works

- **Convergence as signal**: when two independent angles arrive at the
  same shape, the design is empirically reliable
- **Divergence as forcing function**: differences are interview questions
  the psyche or the comparison report must answer
- **Anti-drift**: single-track inference (the failure mode behind the
  schema-defines-effects drift per /350) is mitigated because the other
  track would surface the inference

## See also

- `skills/major-break-via-new-repo.md` — the new-repo discipline this
  skill builds on
- `skills/feature-development.md` — the standard designer worktree
  workflow
- `skills/jj.md` — `jj` discipline including the operator-on-main
  exception under `skills/jj.md` §"The standard flow"
- `skills/intent-clarification.md` — how to escalate divergence to
  psyche review
- `skills/reporting.md` — where comparison reports land
