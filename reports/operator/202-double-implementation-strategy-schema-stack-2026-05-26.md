# 202 — Double implementation strategy for the schema-derived stack

## Status

This report supersedes the repository-strategy portions of:

- `reports/operator/200-latest-notacore-schema-vision-after-designer-359-2026-05-26.md`
- `reports/operator/201-operator-delta-after-designer-361-schema-derived-nota-stack-2026-05-26.md`
- `reports/designer/361-latest-vision-schema-derived-nota-stack-2026-05-26.md` §10 after its `/362` amendment
- `reports/designer/362-critique-of-operator-200-vision-correction-2026-05-26.md`

Those reports still carry useful architecture and prototype substance. They
are stale only on the question of whether the new-repo route is conditional.

Latest psyche intent has now made the new-repo route the active method for
the stack parts being replaced.

This report is the operator-side application of the new workspace skill
`skills/double-implementation-strategy.md`, which now carries the general
workflow discipline. The skill is broader; this report narrows it to the
schema-derived NOTA stack.

## Spirit records

The new strategy is captured in Spirit:

- Record 812: operators create new replacement repositories and operate on
  their `main` branches; designers work in worktree feature branches off the
  operator-created baseline.
- Record 813: replacement repositories use a `next` suffix when they are an
  upgrade of an old concept rather than a newly named concept.
- Record 814: the first operator-created `main` branch in each replacement
  repository starts from an amalgamation of the strongest previous prototype
  ideas, not from an empty scaffold alone.

## Strategy

The workspace now has two simultaneous implementation lines for this break:

1. Production or current repositories continue carrying the running system
   and any necessary maintenance.
2. New replacement repositories carry the schema-derived stack from a clean
   operator-owned `main`.

This is stronger than the earlier "conditional escape hatch" framing. The
conditional question has been answered for this stack: the replacement is
large enough that the old repo surfaces and old branch names create too much
cross-contamination risk.

## Branch ownership

Operators own the `main` branches of the new replacement repositories.

That means:

- operators create the repositories;
- operators create the first baseline on `main`;
- operators integrate, rebase, and keep `main` usable;
- operators run the Nix checks that define readiness;
- operators merge designer worktree branches after review.

Designers work from that operator baseline in `~/wt` worktrees.

That means:

- designers do not push directly to `main`;
- designers create feature branches under
  `~/wt/github.com/LiGoldragon/<repo>/<branch-name>`;
- designer branches start from the operator's best current `main`, not from
  old prototype islands;
- designer reports can still point at prototype branches, but operator decides
  what enters `main`.

## Naming

Use `-next` when the new repository is an upgrade of an existing concept and
is expected to replace it.

Use a new concept name when the replacement changes the concept rather than
only advancing the old one.

Examples:

- A clean successor to `nota` can be `nota-next` if it is still the NOTA
  library.
- A clean successor to `schema` can be `schema-next` if it is still the schema
  engine.
- A repo named around a new concept, such as `asschema` or
  `schema-composer`, should not be forced into a `-next` name if it is not
  just the next version of a previous repository.
- `spirit`, `signal-spirit`, and `core-signal-spirit` are concept-clean
  replacement names, not `persona-spirit-next` names, because the persona
  prefix and owner-signal naming were part of the old surface.

## Operator baseline

The first `main` in a replacement repo is not a blank playground. It should be
the best available concept prototype amalgamation.

For this stack, that means the operator baseline should draw from:

- `reports/operator/199-nota-core-schema-stack-implementation-target-2026-05-26.md`
  for the six-layer stack and delete-or-fence list;
- `reports/operator/200-latest-notacore-schema-vision-after-designer-359-2026-05-26.md`
  for the corrected cleanup priorities;
- `reports/designer/361-latest-vision-schema-derived-nota-stack-2026-05-26.md`
  for the latest six-layer schema-derived NOTA stack synthesis;
- `reports/designer/362-critique-of-operator-200-vision-correction-2026-05-26.md`
  for the critique that identified stale-guidance contamination;
- the designer and second-operator prototype reports cited by `/361` for
  empirical parser and schema-macro tests.

The baseline should include:

- repo-local `AGENTS.md`, `INTENT.md`, `ARCHITECTURE.md`, `README.md`,
  `CLAUDE.md`, `flake.nix`, Rust workspace files, and Nix checks from the
  start;
- raw NOTA structural block parsing as the floor;
- schema macro expansion into a macro-free assembled schema endpoint;
- schema-driven Rust emission as a separate layer, not a reuse of the old
  signal macro;
- fixture tests proving every layer is actually used by the next layer.

## Suggested repository split

This is the current operator split to use unless psyche or designer sharpens
the names:

| Stack part | New repository | Why |
|---|---|---|
| Raw NOTA structural reader and block query library | `nota-next` | It is the next NOTA implementation and should replace the old NOTA surface after proof. |
| Schema macro engine and assembled schema | `schema-next` | It is the next schema implementation; old schema guidance has too much stale six-position/Feature language. |
| Rust code composer from assembled schema | `schema-composer` or `schema-rust-next` | Name depends on whether this stabilizes as a new concept (`schema-composer`) or as the next version of an existing schema-rust surface (`schema-rust-next`). |
| Spirit daemon/runtime | `spirit` | Already created as the cleaned daemon/runtime replacement. |
| Spirit ordinary signal | `signal-spirit` | Already created as the public/ordinary signal replacement. |
| Spirit core policy signal | `core-signal-spirit` | Already created as the owner/core signal replacement. |

The exact composer repo name is still the one unclear naming point. The
default operator lean is `schema-composer` if the repo owns Rust emission as
its concept, because "composer" describes the work more accurately than
"rust-next".

## Relationship to the major-break skill

The previous reports treated `skills/major-break-via-new-repo.md` as an
escape hatch. This prompt turns it into the active method for this stack.
The more specific `skills/double-implementation-strategy.md` now layers the
operator/designer two-track comparison method on top of that major-break
repo discipline.

The skill still supplies the mechanics:

- new repositories are only for real architectural breaks;
- `-next` means replacement-in-progress;
- production repos are not disrupted;
- the new repo eventually takes the canonical short name if it wins.

The new strategy adds a sharper role split:

- operator creates and maintains `main`;
- designer branches from operator `main` in `~/wt`;
- designer branch output is integrated by operator, not pushed through as
  independent truth.

## Immediate operator implications

1. Do not continue treating `nota-core-next` as merely conditional for this
   stack. The new-repo method is selected.
2. Do not let old branch names become the durable coordination surface. They
   are prototype sources and may be mined, but the next implementation target
   is new repositories with operator-owned `main`.
3. When creating the first replacement repo, start from the best prototype
   amalgamation, including Nix checks, rather than scaffold-only setup.
4. Keep reports and per-repo `INTENT.md` files clear about predecessor and
   successor relationship so agents know which repo is production and which is
   the replacement track.

## Open questions

1. Should the first raw NOTA replacement repo be exactly `nota-next`, or is
   `nota-core-next` still the preferred integration name for the combined
   raw-NOTA plus schema-bootstrap baseline?
2. Should the Rust emission layer stabilize as `schema-composer` or as
   `schema-rust-next`?
3. Should `schema-next` and `nota-next` be separate from the first commit, or
   should the operator create one initial combined integration repo and split
   after the layers prove themselves?

## Operator lean

Create separate new repositories for the replacement surfaces unless there is
a direct psyche naming override:

- `nota-next`
- `schema-next`
- `schema-composer`

Keep `spirit`, `signal-spirit`, and `core-signal-spirit` as the first
consumer triad.

Use the old prototype branches only as source material. The new repos'
`main` branches become the shared coordination surface.
