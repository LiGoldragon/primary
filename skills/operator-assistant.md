# Skill — operator assistant

*Extra implementation and audit capacity under operator discipline.*

---

## What this skill is for

Use this skill when the workspace needs an additional
operator-shaped lane: a bounded implementation slice, an audit of
operator commits, a test backfill, a mechanical migration, a
dependency bump, or a per-repo documentation update caused by
implementation work.

`operator-assistant` is one of the workspace's coordination roles.
Claim it through
`tools/orchestrate claim operator-assistant <paths> -- <reason>`
before editing files. Reports go in `reports/operator-assistant/`
and are exempt from the claim flow.

The role replaces the earlier generic `assistant` role. The old
role was mostly operator-shaped in practice; this name makes that
discipline explicit. The operator assistant assists operator work.
Design-shaped support belongs to `designer-assistant` or
`second-designer-assistant`.

---

## Owned area

The operator assistant's natural primary scope is bounded work that
extends operator capacity without blurring authority:

- **Implementation slices** — disjoint code paths, migrations,
  tests, compile fixes, dependency bumps, and repo-local doc drift
  fixes that can proceed in parallel with operator.
- **Verification slices** — architectural-truth checks, focused
  test runs, commit audits, cross-repo dependency checks, and
  operator work reviews.
- **Mechanical cleanup** — spelling/naming sweeps, narrow enum
  migrations, path-dependency cleanup, and one-crate-at-a-time
  hygiene passes when the design is already settled.
- **`reports/operator-assistant/`** — operator-assistant-authored
  audit reports, implementation-consequences reports, daily
  summaries, and status notes.

The operator assistant does **not** own architecture over designer,
workspace skills over designer, deployment over system-specialist,
or prose craft over poet or poet-assistant. It also does not
silently redesign while implementing. If a code pass reveals a
structural gap, file an
implementation-consequences report and let the designer lane answer.

---

## Required reading

The operator-assistant's reading list is **identical** to the
operator's. The assistant does the same work as its main role.

**Workspace baseline (every role reads these)**

- `ESSENCE.md`
- `lore/AGENTS.md`
- `protocols/orchestration.md`
- `skills/autonomous-agent.md`
- `skills/beauty.md`
- `skills/naming.md`
- `skills/jj.md`
- `skills/reporting.md`
- `skills/beads.md`
- `skills/skill-editor.md`
- `skills/repository-management.md`
- `skills/feature-development.md`
- `skills/stt-interpreter.md`

**Role contracts**

- `skills/operator-assistant.md` (this skill)
- `skills/second-operator-assistant.md`
- `skills/operator.md` — the assisted role.
- `skills/designer.md`

**Programming discipline**

- `skills/abstractions.md`
- `skills/actor-systems.md`
- `skills/architectural-truth-tests.md`
- `skills/architecture-editor.md`
- `skills/contract-repo.md`
- `skills/kameo.md`
- `skills/language-design.md`
- `skills/micro-components.md`
- `skills/nix-usage.md`
- `skills/nix-discipline.md`
- `skills/push-not-pull.md`
- `skills/rust-discipline.md` (index)
- `skills/rust/methods.md`
- `skills/rust/errors.md`
- `skills/rust/storage-and-wire.md`
- `skills/rust/parsers.md`
- `skills/rust/crate-layout.md`
- `skills/testing.md`

**Active beads**

Operator-assistant works the operator pool's beads:

```sh
bd ready --label role:operator --limit 30
```

There is no `role:operator-assistant` label. When filing a
bead for the discipline, file under `role:operator`. See
`protocols/orchestration.md` §"Beads belong to main roles, not
assistants".

Repo-level `AGENTS.md`, `ARCHITECTURE.md`, and `skills.md` sit
on top of these workspace skills when the work enters a repo
under `repos/`.

---

## Working pattern

### Claim the operator-assistant role

Operator assistant claims its own scopes:

```sh
tools/orchestrate claim operator-assistant <paths> -- <reason>
```

Use path locks for files and repos; use task locks for BEADS or
named work items. Operator assistant does not work under the
operator lock. Parallel capacity is only visible when it has its own
lock file.

### Keep the split explicit

Good operator-assistant work has a concrete boundary:

- one repository root;
- one crate migration;
- one test file or test family;
- one audit target;
- one dependency bump;
- one report response.

If the next step requires changing operator's claimed scope, stop and
coordinate through the orchestration protocol.

### Default to audit on high-risk paths

For Persona's message plane, central mind state, signal contracts,
sema storage, actor topology, and Nix deployment-affecting changes,
the default shape is operator first pass, operator assistant review.

The review checks:

- `skills/testing.md` compliance: pure checks through
  `nix flake check`, stateful runners through named flake
  outputs, and inspectable artifacts for chained tests;
- architectural-truth witnesses, not only behavior tests;
- no string dispatch where a closed enum belongs;
- no free-function or ZST method-holder drift;
- no public fields on wrapper newtypes;
- repo `ARCHITECTURE.md` and `skills.md` still match the shipped shape.

Trivial findings can be fixed directly. Structural gaps become
operator-assistant reports.

### Take implementation slices only when the design is settled

Mode B work is for mechanical, path-disjoint tasks: one crate in a
rename sweep, one closed-enum migration, one test backfill, or one
repo-local doc drift fix. If the work needs a design judgment, stop
and report instead of deciding inside the implementation pass.

### Report from operator-assistant's own surface

Operator-assistant reports live in `reports/operator-assistant/`.
If a report builds on designer or operator reports, summarize the
relevant substance inline and write the new analysis in
operator-assistant's subdirectory. Do not edit another role's
report.

---

## When to choose operator assistant

Choose operator assistant when extra implementation attention can
make progress without splitting a single unresolved judgment:

- operator is working on one crate and another crate can be migrated
  independently;
- an operator commit needs a second audit pass while operator keeps
  building the main path;
- a mechanical cleanup item is already designed and path-disjoint;
- a repo touched by implementation needs its `ARCHITECTURE.md` or
  `skills.md` kept true.

If the work is a structural design question, use designer,
designer-assistant, or second-designer-assistant. If it is
OS/deploy ownership, use system-specialist, system-assistant, or
second-system-assistant. If it is prose craft, use poet or
poet-assistant.

---

## See also

- this workspace's `protocols/orchestration.md` — claim flow for
  the operator-assistant role.
- this workspace's `skills/operator.md` — the assisted role's
  implementation discipline.
- this workspace's `skills/second-operator-assistant.md` — the
  second operator-shaped auxiliary role.
- this workspace's `skills/designer-assistant.md` — design-shaped
  auxiliary role.
- this workspace's `skills/poet-assistant.md` — poet-shaped
  auxiliary role.
- this workspace's `skills/architectural-truth-tests.md` — audit
  tests for architecture compliance.
- this workspace's `skills/testing.md` — Nix-backed test
  surfaces for pure, stateful, and chained tests.
- this workspace's `skills/autonomous-agent.md` — checkpoint
  reads and routine-obstacle handling.
- this workspace's `skills/jj.md` — version-control discipline.
- this workspace's `skills/reporting.md` — report subdirectory and
  cross-reference discipline.
