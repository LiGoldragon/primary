# INTENT — primary workspace

*The psyche's intent for this workspace, synthesised from Spirit records.
General workspace rules only; repo-specific and technical intent lives in
each repo's `INTENT.md`. Companion to `ESSENCE.md` (the universal core) and
`AGENTS.md` (the every-session contract).*

## Intent is primordial

Intent drives the system; an agent unsure what to do falls back on intent.
The psyche is the human, and only the psyche is the source of new intent —
agent messages and agent-written files are not. When intent is unclear,
absent, or contradicted, ask rather than infer.

## The intent layer

Three surfaces, increasing in distillation:

- **The Spirit store** — the raw log of psyche statements as typed intent
  records (a dense agent-clarified description, kind, magnitude, and
  daemon-stamped time). The sole intent substrate.
- **Per-repo `INTENT.md`** — each project's psyche intent synthesised into
  prose, the same shape as this file.
- **`ESSENCE.md`** — the universal core, the gold of the gold.

The layer outranks every other surface; when two disagree, intent wins.
Agent-written documents (architecture, reports, skills) have lower
precedence. Supersession is always explicit, and only the psyche can
supersede — an agent meeting documented intent that seems wrong asks, it
does not override.

## The Spirit gate runs on every psyche prompt

Before reports, code, or chat, read the prompt and choose one outcome:

- **No capture** — a question, tangent, task-only order, or reaction to
  the current state.
- **Observe / refresh** — context is needed; read recent Spirit records.
- **Ask** — durable meaning, kind, or privacy is unclear.
- **Record** — an explicit durable Decision, Principle, Correction,
  Clarification, or Constraint, captured through the Spirit CLI.

Capture is conservative; a working order that dies when the task is erased
is task state, not intent. Everything else an agent produces derives from
the captured intent.

## Intent alignment is the default

`skills/intent-alignment.md` is the canonical protocol for interactive
psyche-facing goal shaping. It teaches the graph-discovery interview: one
focused question in plain prose, the psyche's answer, then the next question
shaped by that answer until the dependency graph is clear enough to execute.
*"It's what an agent should do by default — unless the agent is a very
specialized agent, in which case it should be trained already."* A clear
directive to implement or to show is itself the answer, so alignment sharpens
intent rather than stalling on it.

## Guidance files — the layered surface

Every file that shapes agent behavior is a guidance file: `ESSENCE.md`,
`AGENTS.md`, `INTENT.md`, the skills, the Spirit records, and per-repo
`INTENT.md` / `skills.md` / `ARCHITECTURE.md`. An intent statement lands at
the level matching its clarity and reach — the most universal in
`ESSENCE.md`, per-keystroke override rules in `AGENTS.md`, topic discipline
in skills, raw statements in Spirit. Editing guidance files is the cadence
of workspace evolution.

## Guidance stays lean

Agents are smart and fill in blanks from good high-level guidance;
over-elaborated guidance costs context without changing behavior. Prefer
cutting to adding — detail that doesn't change what an agent does is noise.
Every statement in an essence or intent surface is anchored in an actual
Spirit record; a claim with no record behind it does not belong, or the
intent is recorded first.

## Push, not poll

Polling design is forbidden. Producers push events; consumers subscribe.
When a mechanism appears to offer only polling, escalate deeper into the
stack and build or use a real event surface rather than tuning sleep
intervals or adding fallback polling. Spirit `c5nq` records the explicit
constraint.

## Reports are for agents; chat is for the psyche

Substantive output — analysis, proposal, audit, synthesis — goes in a
report under `reports/<role>/`. Chat carries the locator plus the
user-attention items, each restated with enough substance to engage
without opening the report. The psyche runs many parallel agents and
cannot read giant chat responses.

## Roles are loose

Work organises under the main roles plus lanes, but role boundaries are
loose — a single agent stays on a topic rather than shuffling context
between windows, and beads carry no role labels; any agent picks up any
item by topic affinity. Lanes still coordinate through lock files and
per-role report subdirectories.

## Two deploy stacks coexist

Production runs the old monolithic stack on `main` in the canonical
checkouts; fixes for live nodes go there. The lean rewrite — the new
daemon, thin CLI, and lean horizon — lives on its rewrite branches in
worktrees and has not been cut over. Don't deploy the rewrite as a fix,
and don't fold one stack into the other piecemeal: the schemas have
diverged, and cutover is a coordinated multi-repo merge after the rewrite
reaches parity.

## Where work happens — primary versus code repos

On **primary** (this coordination repo) everyone works on `main` directly:
edit, commit, push, no branches and no rebase dance. In the **code repos**
under `/git`, production-touching work spanning more than one commit lives
on a feature branch in a separate worktree under `~/wt/...`; the canonical
checkout stays on `main` so every peer sees production reality. Designers
ship on `next` / feature branches there; operators own `main` and
integrate.

## BEADS is transitional

`.beads/` coordinates short-tracked items today; the destination is
persona-mind's native typed work graph. Don't deepen the bd investment or
build a bridge to it — design assuming it goes away. BEADS is never an
ownership lock; any agent may create, update, or close items.

## Workspace truth lives in files every agent can open

Memory and persistent state live in workspace files — skills, reports,
protocols, repo docs, or `.beads/` while it lasts. Don't use
harness-dependent memory that is invisible to other harnesses and to the
human.

## The Nix store is not a search surface

Don't run `rg` / `grep` / `find` / globs against `/nix/store` — it grows
unbounded and the matches are dependency noise. Reach Nix-controlled
values through Nix: the source checkout, `nix eval`, `nix flake show`,
`nix path-info`, or a derivation that exposes the value.

## What the workspace is building

Persona — a meta-AI system that organises models into a structure
emulating human intelligence, animated by persona-spirit. Components are
dumb mechanism; the thinking happens in agent LLMs that drive them through
CLIs and through spirit — no component works without an LLM on the other
end of the wire. Components ship in raw form first (standalone CLI +
daemon + durable state) and are used individually before
component-to-component wiring lands.

## A language is data — structural macros all the way down

The languages built here treat their own constructs — struct, enum,
generics, a schema declaration — as a set of typed structural macros kept as
inspectable data, not frozen inside a compiler. Conventional languages hold
that macro set too; they just save it poorly, smeared across the
implementation. Keeping it as data makes the language open (a new construct is
new data, not a compiler change) and far easier for an LLM to read, write, and
reason about at the meta level. Extensibility stays typed and safe down to a
small frozen seed — the NOTA parser and one derive. (Spirit `7c71`; per-repo
mechanics live in the nota / schema `INTENT.md` files and `skills/structural-forms.md`.)

## The compiler is build-time; binaries carry only rkyv contracts

Because the language is data, the schema/NOTA compiler (`nota-next` →
`schema-next` → `schema-rust-next`) is a *build-time-only* dependency: it emits
each component's typed Rust and never links into the runtime binary. A shipped
daemon therefore stays small and knows only its strict rkyv wire and storage
contracts — none of the parser, lowering, or emitter — and the NOTA text codec
is an optional edge feature, absent from the daemon binary. The schema compiler
structurally never ships, verifiable from the `[build-dependencies]` section
alone. (Spirit `9rjq`.)

## Role is type — the dimensional principle

A struct field's role is its type, so no struct ever has two fields of the
same type. Distinct roles are distinct types (Height and Width are both metres
but cannot be interchanged or multiplied as alike); genuine repetition is a
keyed collection, never repeated fields. Field-name therefore equals type-name
by default, and an explicit field name signals a missing newtype or a
collection. This is the newtype-per-domain-value rule (AGENTS.md) pushed to its
endpoint: a newtype per role. (Spirit `ov30`.)

## Recompiling is cheap; zero-downtime is the goal

Changing a component's schema or enum set is a trivial recompile, not a cost
to design around — zero-downtime upgrade is a design goal. A daemon's
vocabulary therefore lives in its compiled schema and grows by
recompile-and-redeploy, not runtime config. (Spirit record `uuh7`.)

## New roles, and the auditor

A new role created dynamically isn't a dead end: the agent reads
`AGENTS.md`, `ESSENCE.md`, and this file, queries `skills/skills.nota` for
the closest existing role-skill, asks the psyche for scope, and drafts
`skills/<role>.md` as it does real work. A **concept designer** is the
entry point for new concepts — comparing them against existing ones and
deciding when one earns its own lane. An **auditor** role is coming (shape
decided, lane mechanics open): an automated doubter that finds flaws, bad
patterns, and broken rules, closing the loop back to designer.
