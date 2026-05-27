# INTENT — primary workspace

*The psyche's intent for this workspace, synthesised from Spirit
intent records and legacy `intent/*.nota` history. Verbatim psyche
quotes appear in italics; surrounding prose is agent-composed from
intent-log summaries. Companion to `ESSENCE.md` (the most universal
psyche intent — gold of the gold) and `AGENTS.md` (every-session
contract and override rules). Maintenance:
`skills/intent-manifestation.md`.*

## Intent is primordial

Intent drives the system. *If any agent needs to know what to do,
they fall back on intent.* The psyche is the human; psyche prompts
arrive in natural language. Persona messages between agents
(NOTA-formatted) are not psyche; agent-written files are not
psyche. Only the psyche is the source of new intent.

When intent on a question is unclear, absent, or contradicted,
**ask the psyche** before deciding. *Inferring is the discipline
breaking; asking is the discipline working.*

## The engine is intent and design

The workspace operates as an **intent-and-design-driven engine** —
*the whole engine is mostly intent and design driven. It's a
back-and-forth of designing and intending. And when enough is, the
intent is clear and the design is good enough, we can implement.*
**Designer and operator are the two halves of that dance.** Intent
clarifies what the system should be; design clarifies how it takes
shape; implementation crosses the threshold when both halves of the
readiness signal are met — intent clear AND design good enough.
Either half missing is a stop sign. The full discipline lives in
`ESSENCE.md` §"Intent and design — the engine's dance"; this prose
synthesis names the dance and its readiness signal. Per psyche
2026-05-22.

## Guidance files — the layered surface

The workspace calls every file that shapes agent behavior a
**guidance file**: `ESSENCE.md`, `AGENTS.md`, `INTENT.md`, every
skill in `skills/`, Spirit intent records and legacy intent files,
and per-repo `INTENT.md` / `skills.md` / `ARCHITECTURE.md`. The
shape an intent statement takes depends on its level of clarity and
importance: *highest-certainty universal psyche statements land in
ESSENCE.md; per-keystroke override-shaped rules in AGENTS.md hard
overrides; topic-specific discipline in skills; raw psyche records
in Spirit.*

Editing guidance files is the cadence of workspace evolution.

## The intent layer

Three surfaces, in increasing distillation:

The **intent log** lives in Spirit. It carries psyche statements as
typed intent entries. The current deployed shape stores one dense
agent-clarified description, kind, magnitude, and daemon-stamped
date/time; it deliberately does not store large verbatim/context
payloads. Agents do not manually append to `intent/*.nota` during
normal work. Discipline: `skills/intent-log.md` and
`skills/spirit-cli.md`.

**Per-repo `INTENT.md`** synthesises the project's psyche intent
into prose, the same shape as this file. Discipline:
`skills/repo-intent.md`.

`ESSENCE.md` (workspace and per-repo where it exists) holds the
**essential intent** — *the gold of the gold; only the most
universal, maximum-certainty psyche intent — statements made
with such force that they could stand as the founding rule of a
whole way of working.* Most psyche intent lives in the log and
in INTENT.md; ESSENCE holds the supreme.

The intent layer has **higher authority than every other
workspace surface**. *When two surfaces disagree, the intent
layer wins.* Agent-written documents (architecture, reports,
skills outside the intent layer) have lower precedence.

Supersession of psyche intent is **always explicit, and only the
psyche can supersede**. An agent encountering documented intent
that seems wrong asks; it does not override on its own
authority.

## Recording is the first task of any psyche-prompt turn

When a psyche prompt arrives, *capturing intent through Spirit is
the absolute first task — before editing reports, before responding,
before implementing. Everything else derives from intent.* The
agent reads the prompt, identifies every intent statement
(Decision / Principle / Correction / Clarification / Constraint),
records each through the deployed `spirit` CLI, *then* proceeds
with the work the prompt asked for. The legacy `intent/*.nota`
append path is not the normal workflow.

## Reports are for agents; chat is for the psyche

Substantive output — analysis, proposal, audit, synthesis — goes
in a report under `reports/<role>/`. Chat carries the
user-attention items inline with full substance. *The user runs
many parallel agents and cannot read giant chat responses.*

A chat reply names the report path and carries open questions,
blockers, and recommendations *each restated with enough
substance that the user can engage without opening the report*.
Opaque IDs (bead UIDs, content hashes, change IDs) always carry
an inline description — humans don't have a CLI in their head.

The full discipline: `skills/reporting.md` and
`skills/report-naming.md`.

## Skills must not grow noisy

Smart models can fill in blanks from good high-level guidance;
over-elaborated skills add cost without benefit. *Agents are
smart. … They can fill in the blanks. They just need good
guidance, good overall guidance.* When editing a skill, prefer
cutting to adding. Detail that doesn't change agent behavior is
noise.

The same principle pulled AGENTS.md to compactness and is the
forcing function on every guidance-file edit going forward.

## Roles are loose; beads are not role-labeled

The workspace organises work under four nominal roles (operator,
designer, system-operator, poet) plus lanes, but as of
2026-05-19 the psyche has loosened role boundaries — *I'm
keeping a single agent on a sort of task or topic instead of
shuffling context back and forth between agent windows.* Beads do
not carry `role:*` labels; any agent can pick up any bead based
on topic affinity rather than a prescribed lane.

Lanes still coordinate through lock files and per-role report
subdirectories; the role-label gate on beads is gone.

## Two deploy stacks coexist

**Production today** runs the old monolithic `lojix-cli` stack on
`main` branches in the canonical checkouts: `horizon-rs`,
`lojix-cli`, `CriomOS`, `CriomOS-home`, `CriomOS-lib`, `goldragon`.
Fixes for live nodes go on `main` in those checkouts.

**The lean rewrite** — new `lojix` daemon + thin `lojix` CLI +
lean horizon proposal/view + pan-horizon config — lives on
`horizon-leaner-shape` branches in worktrees under `~/wt/...`,
plus the new repos `lojix` and `criomos-horizon-config`. It has
smoke-built `zeus` end-to-end through `prometheus` but has not
been cut over. *Do not deploy it as if it were a fix.*

**Do not fold one stack into the other piecemeal.** Schemas have
diverged; cutover happens as a coordinated multi-repo merge
after the rewrite reaches feature parity. Until then:
production edits → `main` in the canonical checkout; rewrite
edits → `horizon-leaner-shape` worktree.

## Production work belongs in worktrees, not the canonical checkout

When work touches code already in production and the arc spans
more than one commit, the work belongs on a feature branch in a
**separate worktree** at `~/wt/github.com/<owner>/<repo>/<branch>/`
— parallel-and-predictable to the ghq layout under `/git/...`.
The canonical checkout stays on `main` so every peer agent sees
production reality without negotiating who-has-the-checkout. Full
discipline: `skills/feature-development.md`.

## Optional third "stable" branch is deferred

Per Spirit record 313 (Maximum certainty, 2026-05-23), an optional
third `stable` branch alongside `main` and `next` is **deferred**
until two preconditions hold: the architecture port from Spirit
(the architecture-discovery pilot) reaches all other components,
AND each component bootstraps from its own architecture discovery.
Until then `main` + `next` is sufficient: `next` carries the
in-flight version daemon for handover; `main` is the current
production version. A third branch dedicated to "stable releases"
would compete for psyche attention without reducing risk that the
existing two-branch model isn't already managing through Persona's
upgrade orchestration. Revisit when the preconditions land.

## BEADS is transitional; persona-mind is the destination

`.beads/` exists today for short-tracked-item coordination. The
destination is **persona-mind's native typed work graph** —
captured as memory variants in `persona-mind`'s schema. *Don't
build a Persona↔bd bridge; don't deepen the bd investment.*
Design new shapes assuming bd goes away.

BEADS is never an ownership lock. Any agent may create, update,
comment on, or close BEADS tasks at any time.

## Workspace truth lives in files every agent can open

Memory and persistent agent state must live in workspace files —
`skills/`, `repos/lore/`, `reports/`, `protocols/`, repo
`skills.md`, repo `ARCHITECTURE.md`, or `.beads/` while bd is
the active substrate. Don't use harness-dependent memory systems
(e.g. Claude Code's per-session memory files at
`~/.claude/projects/<workspace>/memory/`, or any agent-private
state store an outside agent cannot read). *Memory tied to one
harness is invisible to every other harness and to the human.*

## NOTA is the universal embedding-safe payload

NOTA is the workspace's text data format for typed records — used
for `.schema` files, for signal payloads on the wire, for intent
records in Spirit, and for inline CLI arguments to every persona
component. The workspace-shape consequence of NOTA's bracket-only
string discipline is that **a complete NOTA expression embeds
escape-free inside any host whose string syntax uses double quotes**
— JSON, Rust string literals, Nix attribute values, YAML, TOML,
shell double-quote arguments, HTTP request bodies, database string
columns, environment variable values. *"JSON-in-JSON requires
escape cascades; NOTA-in-anything-with-doublequote-strings is
escape-free. This is a load-bearing design property of NOTA, not
an incidental side effect."* Design every workspace emitter and
storage path to take advantage of this — the shell-double-quote
wrapping convention (`spirit "(Record (...))"`) is the same
principle at the CLI scale.

NOTA language design lives in `repos/nota/INTENT.md`; emitter and
decoder discipline lives in `repos/nota-codec/INTENT.md`. Full
agent-side authoring discipline: `skills/nota-design.md`.

## The Nix store is not a search surface

Running `rg`, `grep`, `find`, `fd`, broad globs, or recursive
`ls` against `/nix/store` is forbidden — the store grows
unbounded, full-text search across it exhausts memory, and the
matches are usually dependency-tree noise.

When looking for Nix-controlled information, use Nix: the source
checkout, `nix eval` against an attribute path, `nix flake show`
/ `nix flake metadata`, `nix path-info` for a derivation output,
or a targeted check/passthru that exposes the value. If a value
cannot be reached this way, change the Nix code to expose it.

## Persona is LLM-mediated end-to-end

Persona components are dumb mechanism without internal
intelligence; the thinking happens in agent LLMs that drive
components through CLIs and through persona-spirit. Anything
inside a component that looks like a natural-language-
understanding decision — classifier, supersession judgment,
intent parsing — is an LLM call, not algorithm code.
*"there's no component that works without LLMs."* The LLM is
always on the other end of the wire, agent-side.

## Persona components ship in raw form first

Components ship as standalone CLI + daemon + sema state first;
integration with sibling components comes after the raw form is
working. Agents use components individually through their CLIs
before component-to-component wiring lands. *"we can use the
components in the raw form like they don't have to be talking
to each other right away."* No pre-coordinated integration
ceremony; ship the triad, let usage demand wiring.

## The schema-driven stack

The workspace is migrating to a schema-driven architecture where
each persona component declares its contracts — wire, storage, and
internal-actor channels — in NOTA `.schema` files; the schema is the
canonical source the macro pipeline projects into Rust, NOTA-text,
and rkyv-binary. *The schema IS the architecture, not a tool that
produces it.* Schemas warrant per channel; *contract = channel; one
channel = one contract = one schema*. Three categories — wire (the
process boundary), storage (the lifetime boundary), internal (the
actor mailbox) — with wire schemas in the `signal-*` crate and
storage + internal schemas in the daemon crate. **Schemas define
data types only** — effects, fan-out targets, and effect tables are
runtime dispatch / logic, not authored schema content (per psyche
2026-05-26, records 713-715).

The rkyv binary encoding lives in one byte layout that survives two
homes: **sema** in storage, **signal** on the wire. NOTA is the text
projection on top. The vocabulary closes the loop:
**schema specifies, signal moves, sema holds.**

Authors write from the point of view of **NEXT**; **MAIN** is the
published baseline (imported as comparison); **PREVIOUS** or **LAST**
is the prior iteration. The same vocabulary applies wherever a
prior shape is referenced — schema versions, wire-header
extensions, on-disk migration markers, deployment slots.

Schema-language design (namespace shape, enum/struct syntax,
imports, lowering) lives in `repos/schema/INTENT.md`. Composer +
wire-substrate intent lives in `repos/signal-frame/INTENT.md`.
Actor-schema architecture for the spirit daemon lives in
`repos/persona-spirit/INTENT.md`.

## Concept designer is the entry for new concepts

**Concept designer** is a real role — *an entry point for new
concepts the psyche is juggling*. Compares new concepts against
existing ones; surfaces relationships; decides when a concept
earns its own dedicated lane. Fleshing out next.

(Persona-spirit's own apex-role + architecture intent lives in
`repos/persona-spirit/INTENT.md`; the workspace-shape consequence
is in `ESSENCE.md` §"Persona is meta-AI; spirit animates".)

## When a new role appears without a skill

A workspace where new roles can be created dynamically (e.g. by
a future `persona-orchestrate` daemon, or by the concept
designer spawning a new lane) needs an entry point so that a
new role isn't a dead end. The new-role agent reads `AGENTS.md`,
`ESSENCE.md`, this file; queries `skills/skills.nota` for the
closest existing role-skill (likely `skills/designer.md`,
`skills/operator.md`, or another discipline file); escalates to
the psyche for scope clarification per
`skills/intent-clarification.md`; and drafts a new
`skills/<role>.md` in-place as it does substantive work.

## Possible additional role — auditor (Medium certainty)

Per intent records 234 and 235 (2026-05-22, Medium certainty),
a third role is under consideration: the **auditor**. The
auditor closes the loop back to designer — it doubts, finds
flaws, identifies bad patterns, catches broken workspace rules.
*"The auditor is just going to be mostly mechanical. It's just
a doubter, something that finds flaws or bad patterns … things
that broke rules that we have."* The auditor knows the rules
because they live in the workspace's standing guidance files
(`ESSENCE.md`, `AGENTS.md`, `skills/`); the mechanical nature
of the work makes it suit a smaller model good at pattern
checking. The psyche named **DeepSeek** as the chosen model and
the direction is to **automate** the auditor: *"deep seek is
going to be our main auditor, because our audits are just going
to be mostly mechanical."*

Carried under the carry-uncertainty discipline
(`skills/architecture-editor.md` §"Carrying uncertainty"): the
role is **proposed, not decided**. Open questions: authority
class (structural or support-tier?), lane mechanism (windows on
a shared agent identity or external CI-style pipeline?),
substrate for audit findings flowing back to designer (reports
under a `reports/auditor/` subdir, comments on beads, Spirit
intent records from an auditor agent identity, or PR-style
review on jj commits). No `skills/auditor.md` skill file and no
`reports/auditor/` subdirectory yet — those land when the
role's shape settles. The entry point for the bootstrap, if an
auditor agent starts work before the skill file exists, is the
"When a new role appears without a skill" section above.
