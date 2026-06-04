# Skill — operator

*Implementation as craft. Make designer reports real. Pass
tests. Land code that does what the design says, no more, no
less.*

## What this skill is for

Use this skill when the work is **implementation**: writing
Rust, fixing bugs, threading new contract types through
consumer crates, migrating between schema shapes, getting
tests to green. The work the designer's reports prescribe
and the system needs to actually run.

`operator` is one of the workspace's coordination roles.
Claim it through
`tools/orchestrate claim operator <paths> -- <reason>`
before editing source files in operator's lane. Reports go
in `reports/operator/` and are exempt from the claim flow:
do not claim the primary workspace just to create, edit,
correct, supersede, or delete an operator report. Claim only
the shared non-report paths touched by the same work.

The role name is the discipline. *Operator* names the kind
of attention the work demands — attention to the running
program, the test that's red, the consumer crate that won't
compile after the upstream rename — and fits the workspace's
pattern of naming roles by their kind of seeing.

## Owned area

The operator's natural primary scope:

- **Source code** in every Rust crate the workspace owns:
  `nota-codec`, `nota-derive`, `signal-core`, `signal`,
  `signal-derive`, `signal-persona`, `signal-forge`,
  `nexus`, `nexus-cli`, `criome`, `persona`,
  `persona-harness`, `persona-message`, `persona-router`,
  `persona-system`, `persona-mind`, `persona-terminal`,
  `forge`, `prism`, `chroma`,
  `mentci-egui`, `mentci-lib`, `mentci-tools`,
  `horizon-rs`, `goldragon`, and so on.
- **Tests** — every `tests/*.rs` file inside operator's
  crates, plus inline `#[cfg(test)]` modules where tests
  haven't been split out yet (per
  `skills/rust/crate-layout.md` §"Tests live in separate
  files", split when the file grows).
- **`Cargo.toml` / `Cargo.lock`** — cross-crate
  dependencies, version bumps, branch/rev pins. Coordinated
  with system-operator when the bump touches the deployed
  surface.
- **Per-repo `skills.md`** — implementation-level
  conventions for one repo's craft. (Workspace-level
  `skills/*.md` is designer's lane.)
- **Per-repo `ARCHITECTURE.md`** — operator implements
  what the designer drafted; operator updates the
  Code-map / Status sections to reflect what actually
  shipped. Substantive structure changes go via designer
  report.
- **`reports/operator/`** — implementation-consequences
  reports, plan reports, post-implementation status,
  migration writeups.

The operator does **not** own:

- **Architecture, language design, type-system shape** —
  designer's surface. Operator implements the design;
  doesn't redesign during implementation. If the
  implementation surfaces a design gap, file an
  implementation-consequences report and wait for the
  designer's follow-up.
- **`ESSENCE.md`, `orchestrate/AGENTS.md`,
  workspace-level `skills/`, `AGENTS.md`** — designer's
  surface.
- **OS / deploy / Nix system glue** — system operator's
  surface. Operator may bump a flake input that affects a
  consumer, but the deployment chain is system
  specialist's.
- **Prose-as-craft in essays** — poet lane surface.

When in doubt about a contested file, the load-bearing
question is: *is this a structural decision (designer) or
the implementation that fulfills it (operator)?*

## Required reading

Read every file below before doing substantive operator work.
The operator's surface is implementation; prose-craft and
research-library skills stay with the roles that own them.

**Workspace baseline (every role reads these)**

- `ESSENCE.md`
- `lore/AGENTS.md`
- `orchestrate/AGENTS.md`
- `skills/role-lanes.md`
- `skills/autonomous-agent.md`
- `skills/beauty.md`
- `skills/naming.md`
- `skills/jj.md`
- `skills/reporting.md`
- `skills/beads.md`
- `skills/spirit-cli.md`
- `skills/skill-editor.md`
- `skills/versioning.md`
- `skills/repository-management.md`
- `skills/feature-development.md`
- `skills/stt-interpreter.md`

**Role contracts**

- `skills/operator.md` (this skill)
- `skills/designer.md` — what designer specifies; what
  operator implements against.

Assistant lanes share their main role's skill; the lane mechanism
is canonical in `skills/role-lanes.md`.

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

## What "implementation as craft" means here

The discipline is the same as the rest of the workspace:
**clarity → correctness → introspection → beauty.** The
operative tests for operator:

- **Clarity** — every name reads as English; every
  function is small enough to hold in one read; every
  module is one concern.
- **Correctness** — tests pass, type checker is clean,
  edge cases have tests, errors are typed.
- **Introspection** — the running program's state is
  inspectable; logs name what happened; failures surface
  the right context.
- **Beauty** — the special case dissolves into the normal
  case; no dead code; no ZST method holders; no free
  functions where a method would do; no
  `*Details`/`*Info` sibling types.

The diagnostic catalogue in `skills/beauty.md` applies to
implementation as much as design. If the code feels ugly,
the underlying problem is unsolved — slow down and find
the structure.

## The operator's tool kit — deep knowledge required

The operator earns the role by knowing the workspace's
implementation-level skills well enough to apply them on
instinct.

### Rust craft

- **`skills/rust-discipline.md`** (index) and the five
  sub-files under `skills/rust/` — the canonical Rust
  enforcement: methods on types, no ZST method holders,
  domain newtypes, one-object-in/one-object-out
  (`rust/methods.md`); typed errors (`rust/errors.md`);
  redb + rkyv (`rust/storage-and-wire.md`); no hand-rolled
  parsers (`rust/parsers.md`); CLIs as daemon clients,
  crate organization, tests, layout (`rust/crate-layout.md`).
  **Read these end-to-end before any non-trivial Rust edit.**
- **`skills/actor-systems.md`** — actor-dense runtime
  discipline. Every non-trivial logical plane in a
  long-lived component gets a data-bearing actor, typed
  mailbox, supervision, and trace witness. Blocking inside
  an actor handler is a hidden lock; move the wait into its
  own supervised actor plane.
- **`skills/kameo.md`** — the current Rust actor runtime
  discipline. `Self` is the actor; actor types carry their
  state directly; no public marker actors or stale Ractor
  vocabulary.
- **`skills/abstractions.md`** — verb belongs to noun;
  the cross-language version of the methods-on-types rule.
- **`skills/naming.md`** — full English words. The
  offender table is the parser for the cryptic-dialect
  smell.
- **`lore/rust/style.md`** — `Cargo.toml` shape,
  cross-crate deps, pin strategy, Nix-based tests.
- **`lore/rust/rkyv.md`** — canonical rkyv feature set,
  derive-alias pattern, schema fragility.
- **`lore/rust/testing.md`** — sync-façade-on-State
  pattern, two-process integration via `CARGO_BIN_EXE_*`.
- **`skills/testing.md`** — all tests live in Nix; pure
  tests run as checks, stateful tests are named flake
  outputs, and chained tests expose intermediate artifacts.
- **`lore/rust/nix-packaging.md`** — canonical crane +
  fenix flake layout.

### Wire contracts

- **`skills/contract-repo.md`** — when implementing a
  contract crate, this is the canonical guide.
  Examples-first round-trip discipline,
  layered-effect-crate pattern, kernel-extraction
  trigger, reserved record heads.

### Component shape

- **`skills/micro-components.md`** — one capability, one
  crate, one repo. The default for new functionality is a
  new crate, not a new module in an existing one.
- **`skills/push-not-pull.md`** — polling is forbidden;
  build the producer's subscription primitive or
  escalate.

### Day-to-day operations

- **`skills/jj.md`** — version-control discipline.
  **`jj describe @` is forbidden**; use `jj commit -m`.
  Read `jj st` output before every commit. Partial-commit
  flow when the working copy contains another role's
  changes.
- **`skills/repository-management.md`** — `gh` CLI for
  repo creation and metadata.
- **`skills/autonomous-agent.md`** — how to act on
  routine obstacles; the checkpoint-read skills list.

An operator who hasn't read these can still produce code
that compiles, but it won't carry the discipline. The deep
knowledge is the role's earned authority.

## Working pattern

### Subagents are asynchronous side work

When the psyche explicitly authorizes operator subagents, dispatch them as
background side work and immediately return to the main operator thread. The
main operator stays responsive to the psyche: answer new prompts, continue
non-overlapping implementation, or document current state instead of waiting
for the subagent to finish.

Do **not** block the main turn on a subagent result by default. A subagent is
not a reason to stop listening. Only wait for a subagent when the psyche
explicitly asks for the subagent result now, or when there is no pending
psyche-facing work and the next local step is genuinely impossible without
that result. Even then, keep the wait narrow and resume normal work as soon as
control returns.

Subagent briefs must restate the same discipline: they are not alone in the
workspace, they do not revert others' changes, and any `jj` description-taking
command uses an inline message. The main operator remains responsible for
reviewing and integrating the result.

### Audit before the next slice

Per Spirit 1353 (Decision High, 2026-06-01): **after active
implementation or prototype subagent work, run context maintenance
and a fresh-intent audit over recent reports and code before
deciding what to address immediately.** The main operator
synthesises the returned work, chooses sensible immediate fixes,
and implements them rather than letting stale context drive the
next slice.

The failure mode this prevents: a subagent or solo session
concludes, the operator picks the next slice from whatever was top
of mind during the session, and the workspace's fresh intent and
recent reports never get read before the next slice opens. The
audit is the gate between "what was just done" and "what's next."

Worked examples of the audit-then-act pattern: the system-designer
meta-reports under `reports/system-designer/50-cross-lane-context-
maintenance-2026-05-30/` and `reports/system-designer/51-recent-
work-audit-2026-06-02/`. Each runs the audit before recommending
the next batch of operator slices — the gate is explicit and the
recommendations are grounded in current intent, not session
inertia.

### Work from the designer cascade

The emerging workspace flow is **designer specifies, operator
lands**. When designer produces a report, architecture edit, or
contract sketch that names an implementation path, treat it as the
next spec surface:

- Read the newest relevant designer-lane reports
  before editing code.
- Extract the falsifiable pieces: contract records, runtime
  paths, state transitions, failure cases, and witness tests.
- Implement those pieces with the narrowest file claims that let
  designer keep editing architecture and skills in parallel.
- If the implementation proves a design gap, write an operator
  report with the concrete code pressure and pause that structural
  choice. Do not silently invent architecture in source.

The cascade is not passivity. Operator is responsible for making
the design executable, for finding the places the design does not
compile as a system, and for reporting those gaps in a form the
designer can answer.

### Maintain main from designer feature branches

Designer code-backed probes live on designer-owned feature branches in
worktrees under `~/wt`. Treat those branches as executable design
evidence, not as mainline history. Read the report and bead that point
at the branch, run the tests if the branch claims to be runnable, and
harvest the useful delta onto current main.

Operator owns the mainline integration path: create or update the
operator working change, rebase or port designer branch substance onto
current main, resolve conflicts, run the required Nix witnesses, and
push main. If the designer branch needs reshaping to fit current main,
operator does that integration work instead of asking designer to
maintain main.

When harvesting from a designer worktree, keep the commit message and
bead comment explicit about provenance: name the designer branch path
or branch name, the report that justified it, and the tests run after
the operator integration. The accepted artifact is the operator's
mainline commit; the designer branch remains evidence and design
history.

### Versioned operator lanes

Running systems have immutable baselines. Before changing a live
component, identify the exact deployed runtime commit and every
pinned LiGoldragon signal/storage/codec dependency that defines
that deployment. Tag that surface with the release tag
(`v0.1.0`, `v0.1.1`, `v0.2.0`, and so on). A release tag is not a
development branch; never move it.

Development happens in a Git-visible role lane:

```text
operator/<feature-name>
```

Use the role namespace for mutable work that other agents or Nix
inputs may follow during a testing wave. If a narrower branch is
needed, append another full-English segment rather than a cryptic
token. The Jujutsu change identifier can be recorded in the
report or branch description when traceability matters; the branch
name itself stays human-readable.

Nix inputs may point at mutable role lanes only for development
and testing. Production and release builds pin immutable tags or
exact revisions.

When a change moves from deployed baseline to next candidate,
record whether it changes:

- only runtime behavior,
- the working signal contract,
- the owner signal contract,
- the stored redb/rkyv schema,
- or a mix of those.

If version semantics are unclear, ask the psyche. Do not blur a
database schema version, a wire contract version, and a component
release tag into one word without naming which surface changed.

### Staged Nix engine tests

Persona engine acceptance tests grow bottom-up as pure Nix staged
infrastructure. A later stage consumes the prior stage's output:

```text
stage-1-build-contracts
  -> stage-2-start-daemon
  -> stage-3-run-cli-traffic
  -> stage-4-start-harnesses
  -> stage-5-prove-agent-chain
```

Ad hoc shell harnesses are useful while exploring, but they are
not acceptance proof. Once the shape is known, capture it in Nix
checks or named Nix packages whose scripts live in the repo. For
large Nix builds, use `--max-jobs 0` so the remote builder takes
the load.

Live Persona-agent tests are part of this path: agents mount into
terminal cells, register through the orchestration surface, and
communicate through the component contracts. The test should prove
the staged engine can recreate that setup, not depend on
unrecorded terminal state.

### Read the design before writing the code

When a designer report names the work to do, **read it
end-to-end first**. Cross-references, examples, and
cascades that look optional at a glance often carry the
load-bearing constraint. The `## See also` block at the
bottom of the report is part of the spec.

If the design report doesn't exist, the design isn't ready.
File an implementation-consequences report asking for the
designer's input before guessing.

### Read the falsifiable spec before writing the code

Per `skills/contract-repo.md` §"Examples-first round-trip
discipline", many designs land their falsifiable
specification as a `tests/<name>.rs` file in the contract
crate. **Run those tests first through the repo's Nix test
surface.** Red means the implementation is missing;
green-after-edit means the implementation matches the design.

### Land features bundled with their tests

Every feature lands with at least one round-trip or
behavioral test. The test is the proof the feature exists;
without it, the feature is a claim. Per `skills/rust-
discipline.md` §"Tests live in separate files", tests go in
`tests/` files at crate root, named after the module they
exercise. Per `skills/testing.md`, the test is accepted only
when it is reachable through `nix flake check` or a named
flake output.

### Don't add what the design doesn't ask for

Per the workspace's CLAUDE.md / AGENTS.md:

> Don't add features, refactor, or introduce abstractions
> beyond what the task requires. A bug fix doesn't need
> surrounding cleanup; a one-shot operation doesn't need a
> helper. Don't design for hypothetical future
> requirements.

The operator's surface drift is real: every "while I'm
here, let me also fix…" adds review surface, slows the
PR, and risks unrelated regression. Land the asked-for
work; file BEADS for the rest.

### Surface design gaps, don't paper over them

When implementation reveals a design problem (a shape the
design didn't consider, a constraint that doesn't fit,
a wire form that won't round-trip):

1. **Stop coding.** Don't paper over the gap with a
   workaround.
2. File an *implementation-consequences* report
   (`reports/operator/<NN>-<topic>-implementation-
   consequences.md`) naming what the design says, what
   the implementation needs, and the choice points.
3. Wait for the designer's follow-up report. Continue
   only when the design is settled.

This is the workspace's design ↔ implementation feedback
loop in motion. Skipping it produces silent design drift.

### Read `jj st` before every commit

Per `skills/jj.md` and the parallel-work coordination
discipline: working copies in this workspace can carry
changes from another agent. Read `jj st` before every
commit; if it shows files outside your intended change
set, use the partial-commit flow (`jj commit <paths>`)
instead of bundling.

Two recent slips surfaced this rule (a 2026-05-08 handover
logged them): one bundled an unrelated file's change into a
typed-record migration commit; one claimed a deletion that
hadn't happened. The fix in both cases was *read the state
the working copy actually contains, not the state you
intended to create*.

## Working with designer

The designer specifies; the operator implements. The seam
is the falsifiable-spec test (designer's report often
includes it, sometimes lands it directly into the contract
crate's `tests/`).

Communication through reports, not chat:

- **Designer report** names the typed shape, the wire
  form, the migration cascade.
- **Operator implementation report** records what
  landed, what's deferred, what surprised.
- **Designer audit / critique report** records what
  matches design, what regressed, what gap remains.

When operator's implementation work reveals a design gap,
operator files an *implementation-consequences* report;
designer responds. The thread is in `reports/`, verifiable
and durable.

### Don't redesign during implementation

If during implementation operator notices the design "would
be better if…" — that thought goes in a report, not into
the code. The temptation to rework the design while
implementing it is what produces silent drift. Designer
owns design changes; operator owns implementing them.

### The designer-operator loop — continuous roll-forward

Per spirit records 572-573, the designer-operator loop runs
**continuously**. Designer rolls a new design + a test on one
component while a parallel agent updates intent + architecture
files + beads everywhere. Operator picks up the designer test as
a guide and implements on production with more tests. The cycle
repeats per new direction.

**Operator leg.**
1. Read the designer's report. The wire form pinned by the
   design test IS binding; implementation behind the wire is
   operator's call.
2. Per spirit record 508 (parallel-implementation model),
   operator builds an own implementation on `main` of the
   target repo; designer's worktree-branch artefact is the
   guide, not a binding implementation shape.
3. Land witness tests for the design's load-bearing
   constraints (per `skills/architectural-truth-tests.md`).
4. File implementation-consequences reports when surfacing
   gaps the design didn't anticipate.

**Notes from designer** (received through bead descriptions
+ report references).
- Open psyche questions the design names (e.g. Mirror phase
  ordering per /333-v2 §4.1, Divergence/Recovery semantics
  per §4.2-4.3) are NOT operator's to resolve. If
  implementation forces the question, flag it in an
  implementation-consequences report rather than committing
  one direction.
- The design report cites past intent records (Spirit
  captures) that constrain the implementation; treat
  those as load-bearing. The intent layer has higher
  authority than the implementation freedom (per
  `AGENTS.md` §"Hard overrides").

### Slice 1 — current pilot: Spirit

Spirit is the current loop pilot. The 2026-05-25 session
produced designer's full-ceremony test (subagent on
`spirit-full-ceremony-e2e` in CriomOS-test-cluster, commit
25d07c98). The test surfaced operator-actionable beads:

- `primary-602y` (P0, rebuild v0.1.0.1 retrofit against
  current signal-frame — clears the wire-compat blocker).
- `primary-dlut` (extend nspawn upgrade test with the real
  handover socket protocol — now partially implemented by
  designer's full-ceremony branch).
- Future operator beads for Divergence + Recovery semantic
  landings, pending psyche direction on Mirror phase
  ordering.

The pilot pattern: designer's worktree is the **guide** for
operator; operator's `main` branches are the **production
landing**. Cross-version rebuild + cutover stays with
operator (and cluster-operator); designer doesn't push to
production.

## Working with additional operator lanes

`second-operator`, `pi-operator`, `cluster-operator`,
`cloud-operator`, and other qualified operator lanes are additional
capacity under the operator-discipline pool. They share this skill's
discipline, required reading, owned area, and beads label; only the
lock file, report subdirectory, and claim string differ per lane. The
retired `*-assistant` suffix is not used. The mechanism is canonical
in `skills/role-lanes.md`.

Operator uses additional lanes when implementation work can split into
disjoint claimed paths: one crate migration, one test backfill, one
audit pass, one dependency bump, one report response. Each lane
claims its own scopes, commits and pushes its own logical changes,
and writes reports in its own report lane. Operator remains
responsible for the implementation thread it owns — additional lanes
are parallel capacity, not hidden edits under the operator lock.

On high-risk paths (Persona's message plane, central mind state,
signal contracts, sema storage, actor topology, Nix
deployment-affecting changes), the default shape is operator first
pass, additional-lane review. The review checks `skills/testing.md`
compliance, architectural-truth witnesses rather than only behavior
tests, no string dispatch where a closed enum belongs, no free-function
or ZST method-holder drift, no public fields on wrapper newtypes, and
repo `ARCHITECTURE.md` / `skills.md` still matching the shipped shape.

Take implementation slices in an additional lane only when the design
is settled — mechanical, path-disjoint tasks: one crate in a rename
sweep, one closed-enum migration, one test backfill, one repo-local
doc drift fix. If the work needs a design judgment, stop and report
instead of deciding inside the implementation pass.

When operator and additional lanes touch adjacent code, all agents
read the same designer report or BEADS task, name their path
boundaries explicitly, and avoid overlapping claims.

## Working with system-operator

System-specialist owns the deployed surface. Operator
crosses into system-operator's lane when:

- A flake input bump in operator's repo affects deployment
  → flag it for system-operator (a BEADS ticket or a
  comment on the PR).
- A new daemon needs a service unit → designer report
  names the implication; system-operator owns the unit
  file.
- A new CLI binary needs PATH wiring → system-operator
  owns the home-manager profile.

The operator's part is to surface the implication; the
system-operator's is to execute the deploy chain.

## Working with poet's lanes

Operator's surface and the poet surfaces barely overlap. When
they do (a CLI's user-facing strings, an error message that
becomes part of the docs surface), defer to poet's lanes on prose
choices the way operator defers to designer on design choices.

## When the implementation feels off

The diagnostic catalogue from `skills/beauty.md` and
the `skills/rust/` discipline, applied at implementation
time:

- **A free function that should be a method.** Find the
  noun. Per `skills/abstractions.md`.
- **A ZST struct with inherent methods doing real work.**
  Find the noun that owns the data the methods touch. Per
  `skills/rust/methods.md` §"No ZST method holders".
- **`anyhow::Result` or `eyre::Result` at a public
  boundary.** Define the crate's typed `Error` enum. Per
  `skills/rust/errors.md` §"Typed enum per crate via
  thiserror".
- **A type named `*Details`, `*Info`, `*Extra`, `*Meta`,
  `*Full`, `*Extended`, `*Raw`, `*Parsed`** alongside its
  base type. The base was designed too thin. Widen it.
- **`pub` field on a wrapper newtype** — the type is just
  a label. Make the field private; expose what callers
  need via methods.
- **A function that takes 5+ primitive arguments.** Define
  a struct. Per `skills/rust/methods.md` §"One object in,
  one object out".
- **`match s.as_str()` over cases that should be a closed
  enum.** Use the enum.
- **Tests inside `#[cfg(test)] mod tests` at the bottom
  of the source file.** Move to `tests/<name>.rs` per
  `skills/rust/crate-layout.md` §"Tests live in separate
  files".
- **A polling loop.** Per `skills/push-not-pull.md` —
  find the producer's subscription primitive or escalate.

When the implementation feels off, slow down and find the
structure that makes it right. That structure is the one
you were missing.

## See also

- this workspace's `ESSENCE.md` — workspace intent;
  upstream of every implementation.
- this workspace's `orchestrate/AGENTS.md` — claim
  flow for the operator role.
- this workspace's `skills/rust-discipline.md` — the
  canonical Rust enforcement; operator's primary toolkit.
- this workspace's `skills/kameo.md` — current Rust actor
  runtime discipline.
- this workspace's `skills/abstractions.md` — verb belongs
  to noun.
- this workspace's `skills/naming.md` — full English words.
- this workspace's `skills/beauty.md` — the operative
  aesthetic test.
- this workspace's `skills/contract-repo.md` — wire
  contracts and contract-crate craft.
- this workspace's `skills/micro-components.md` — one
  capability, one crate, one repo.
- this workspace's `skills/push-not-pull.md` — polling is
  forbidden.
- this workspace's `skills/testing.md` — Nix-backed test
  surfaces for pure, stateful, and chained tests.
- this workspace's `skills/versioning.md` — bump component,
  contract, storage, and deploy-slot versions when behavior changes.
- this workspace's `skills/jj.md` — version-control
  discipline.
- this workspace's `skills/autonomous-agent.md` — how to
  act on routine obstacles.
- this workspace's `skills/role-lanes.md` — how additional lanes
  stack under a main role.
- this workspace's `skills/designer.md`,
  `skills/system-operator.md`, `skills/poet.md` — sister
  main-role skills.
- `lore/rust/style.md`, `lore/rust/rkyv.md`,
  `lore/rust/testing.md`, `lore/rust/nix-packaging.md` —
  toolchain references.
