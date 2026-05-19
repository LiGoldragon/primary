# INTENT — primary workspace

*The psyche's intent for this workspace, synthesised from the
intent log (`intent/*.nota`). Verbatim psyche quotes appear in
italics; surrounding prose is agent-composed from intent-log
summaries. Companion to `ESSENCE.md` (the most universal psyche
intent — gold of the gold) and `AGENTS.md` (every-session contract
and override rules). Maintenance: `skills/intent-manifestation.md`.*

## Intent is primordial

Intent drives the system. *If any agent needs to know what to do,
they fall back on intent.* The psyche is the human; psyche prompts
arrive in natural language. Persona messages between agents
(NOTA-formatted) are not psyche; agent-written files are not
psyche. Only the psyche is the source of new intent.

When intent on a question is unclear, absent, or contradicted,
**ask the psyche** before deciding. *Inferring is the discipline
breaking; asking is the discipline working.*

## Guidance files — the layered surface

The workspace calls every file that shapes agent behavior a
**guidance file**: `ESSENCE.md`, `AGENTS.md`, `INTENT.md`, every
skill in `skills/`, every intent file in `intent/`, and per-repo
`INTENT.md` / `skills.md` / `ARCHITECTURE.md`. The shape an intent
statement takes depends on its level of clarity and importance:
*highest-certainty universal psyche statements land in ESSENCE.md;
per-keystroke override-shaped rules in AGENTS.md hard overrides;
topic-specific discipline in skills; raw psyche records in
intent/.*

Editing guidance files is the cadence of workspace evolution.

## The intent layer

Three surfaces, in increasing distillation:

The **intent log** at `intent/<topic>.nota` carries raw psyche
statements as positional NOTA records. Append-only; lock-free
(POSIX `O_APPEND` atomic under PIPE_BUF). Each entry holds a
terse agent rephrasing, the psyche's verbatim quote, surrounding
context, certainty, date, and time. Discipline:
`skills/intent-log.md`.

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

When a psyche prompt arrives, *extracting intent to disk is the
absolute first task — before editing reports, before responding,
before implementing. Everything else derives from intent.* The
agent reads the prompt, identifies every intent statement
(Decision / Principle / Correction / Clarification / Constraint),
writes each to the appropriate `intent/<topic>.nota` via
lock-free `cat >> … <<'EOF' … EOF`, *then* proceeds with the
work the prompt asked for.

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
designer, system-specialist, poet) plus lanes, but as of
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

## Persona-spirit is the apex; concept designer is the entry

`persona-spirit` is a new persona component — *the interface
between the persona mind and the psyche* — sitting at the apex
of the cognitive authority chain (the supervisor has higher
infrastructure permission only). Spawned last; owns mind in the
authority graph. *Persona is a meta AI system — the next
evolutionary step in AI engineering. What animates humans at the
highest level is spirit; persona-spirit is the analog.* Bead:
`primary-ojxq` (persona-spirit triad implementation).

**Concept designer** is a real role — *an entry point for new
concepts the psyche is juggling*. Compares new concepts against
existing ones; surfaces relationships; decides when a concept
earns its own dedicated lane. Captured in
`reports/designer/234-concept-designer-role.md`; fleshing out
next.

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
