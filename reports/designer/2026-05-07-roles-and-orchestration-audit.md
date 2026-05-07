# Roles and orchestration — wide audit + poet onboarding

Date: 2026-05-07
Author: Claude (designer)

A wide exploration of the workspace's coordination surface, an
audit of how the **system specialist** role is currently
expressed, and a proposed shape for adding a fourth role —
**poet** — with its own lock file, report subdirectory, and
skill. Closes with a decision on the `tools/orchestrate`
helper: refactor the Bash now to support N roles, surface the
Rust rewrite as a proposal that lands when the operator's
existing `primary-jwi` bead is picked up.

---

## Executive summary

The workspace ships a two-role coordination model today
(operator + designer). Two more roles are wanted:

- **system specialist** — owns the OS / platform / deploy
  surface (CriomOS, CriomOS-home, lojix-cli, horizon-rs,
  goldragon). Currently named only as a *capability* in
  `skills/system-specialist.md`; the skill explicitly
  disclaims being a lock role. **Not integrated into the
  orchestration protocol.**
- **poet** — owns the writing-as-craft surface (TheBookOfSol,
  publishing, prose where literary quality is the
  load-bearing concern). **Does not exist yet.**

The audit's verdict on the protocol's current shape:

| Surface | Operator | Designer | System specialist | Poet |
|---|---|---|---|---|
| Lock file | `operator.lock` ✅ | `designer.lock` ✅ | none ❌ | none ❌ |
| Reports subdir | `reports/operator/` ✅ | `reports/designer/` ✅ | none ❌ | none ❌ |
| Skill file | (named in protocol) ✅ | (named in protocol) ✅ | `skills/system-specialist.md` (capability only) ⚠️ | none ❌ |
| `tools/orchestrate` | hard-coded peer ✅ | hard-coded peer ✅ | not supported ❌ | not supported ❌ |
| Listed in `~/primary/AGENTS.md` | ✅ | ✅ | ❌ | ❌ |
| Listed in `protocols/orchestration.md` | ✅ | ✅ | ❌ | ❌ |

The fix is straightforward: add the missing rows. The
`tools/orchestrate` helper needs a small refactor — its
`peer_role()` function assumes exactly one peer, which doesn't
generalise. With four roles, every claim checks against three
peers, not one.

---

## Wide exploration — what the workspace looks like today

### Top-level shape

```
~/primary/
├── ESSENCE.md                 — workspace intent (upstream)
├── AGENTS.md                  — workspace-specific agent shim
├── CLAUDE.md                  — one-line shim → AGENTS.md
├── GOALS.md                   — standing goals (Gas City rebuild)
├── RECENT-REPOSITORIES.md     — symlink-index manifest
├── operator.lock              — operator's coordination state
├── designer.lock              — designer's coordination state
├── protocols/
│   └── orchestration.md       — claim/release protocol
├── skills/                    — 13 cross-cutting workspace skills
├── tools/
│   └── orchestrate            — Bash claim/release helper (187 lines)
├── reports/
│   ├── designer/              — 8 reports
│   ├── operator/              — 5 reports
│   └── (top-level)            — 2 historical reports (predate role split)
├── repos/                     — 36 symlinks to /git/github.com/...
└── .beads/                    — short-tracked-item store (transitional)
```

### Skills inventory (13 workspace skills)

Cross-cutting agent capabilities in `skills/`:

| Skill | Role of file |
|---|---|
| `autonomous-agent.md` | Routine-obstacle handling without asking |
| `skill-editor.md` | The meta-skill for naming/locating/cross-referencing skills |
| `version-control.md` | jj + always-push + logical commits |
| `stt-interpreter.md` | STT mistranscription → canonical-spelling table |
| `beauty.md` | Beauty as criterion |
| `abstractions.md` | Verb belongs to noun |
| `naming.md` | Full English words |
| `push-not-pull.md` | Producers push, consumers subscribe |
| `micro-components.md` | One capability, one crate, one repo |
| `rust-discipline.md` | Rust application of the cross-cutting rules |
| `nix-discipline.md` | Flake input forms, lock-side pinning, no `git+file://` |
| `language-design.md` | The 17 instincts for designing a notation |
| `system-specialist.md` | OS/platform capability — *not currently a lock role* |

### Repos linked into the workspace (36)

```
sema-ecosystem      arca, criome, sema, nota, nota-codec,
                    nota-derive, nexus, nexus-cli, signal,
                    signal-derive, signal-forge, prism, forge,
                    hexis, persona, persona-wezterm, orchestrator
system / platform   CriomOS, CriomOS-home, CriomOS-emacs,
                    CriomOS-lib, CriomOS-pkgs, criomos-archive,
                    lojix-cli, lojix-archive, horizon-rs,
                    goldragon
older-generation    mentci-egui, mentci-lib, mentci-tools,
                    gascity, gascity-nix, test-city
writing             TheBookOfSol
docs / meta         lore, workspace
publishing          substack-cli
```

### Persona's role taxonomy

`persona/src/schema.rs` already defines a `HarnessRole` enum:

```rust
pub enum HarnessRole {
    Operator,
    Designer,
    Observer,
}
```

This is a **harness-side** concept (a running AI agent's
declared role inside the persona fabric), distinct from the
workspace's editing-coordination role. The names overlap
intentionally — once persona absorbs the lock protocol (per
`primary-jwi` and the persona-messaging-design report), the
workspace coordination role and the harness role become the
same enum. **`Observer` is a placeholder** — when the workspace
adds `system-specialist` and `poet`, persona's enum should
follow. *Not in scope for this turn.*

---

## Audit — system specialist is missing from the protocol

The `system-specialist.md` skill exists and is well-formed. Its
"What this skill is for" section names the owned area
(CriomOS, CriomOS-home, lojix-cli, horizon-rs, goldragon) and
its working pattern. But the skill carries this disclaimer:

> *The system specialist is a capability, not a primary-workspace
> lock role. Do not claim the `operator` role merely because this
> skill is active. Follow whatever coordination protocol the
> current workspace uses, but keep the concept separate: this
> skill is about OS/platform work.*

That disclaimer made sense when the skill was written and the
workspace only had two locks. Today's request flips it: the
system specialist *is* a lock role. The skill needs the
disclaimer removed and a "Coordination" section added that
points at `protocols/orchestration.md`.

The skill's runbook section (Cluster Nix signing, lines 96–172)
is independently flagged in `2026-05-06-skills-roadmap.md` as
tool-reference material that belongs in `lore/nix/` or
`CriomOS/skills.md`. Moving it isn't blocked by the role
question; deferring the move keeps this turn focused.

---

## Designing the poet role

### What the poet does

The **poet** is the keeper of writing-as-craft. The role name
is the discipline — making sentences that say true things
*beautifully*, where prose is the load-bearing surface.

The natural primary scope:

- **`TheBookOfSol/`** — the essay collection on solar
  nourishment, Āyurveda, chloride toxicology, yogic practice.
  The repo's `AGENTS.md` carries detailed writing conventions
  (IAST transliteration, em-dash attribution, "chloride of
  sodium" not "sodium chloride"). The poet enforces and refines
  these.
- **`bibliography/`** — the standalone scholarly library at
  `~/git/bibliography/` (off-workspace but adjacent). Indexing
  and quote extraction.
- **`substack-cli/`** — the publish-to-substack tool. The poet
  uses it to ship.
- **The prose layer** of any other surface where literary
  quality is the load-bearing concern. ESSENCE.md and key
  sections of skills are written; the poet may refine wording
  while the designer owns the structure. Overlap with designer
  is expected and resolved through the lock protocol.

### What the poet does *not* do

- Code (operator's surface).
- Architecture, naming, type-system design (designer's
  surface).
- Deploy / OS / system glue (system specialist's surface).

The poet's tools are language and citation, not Rust and Nix.

### Why "poet"

The name is honest about what the work is. "Writer" is too
generic; "essayist" is too narrow; "prose lead" is corporate.
*Poet* names the kind of attention the work demands —
attention to rhythm, figure, the texture of the sentence — and
fits the workspace's pattern of naming roles by their *kind of
seeing* (operator sees what to build; designer sees what shape
to build it in; system specialist sees what holds the platform
together; poet sees how the words sound).

### What "poet" does NOT mean

The role is not about adding ornament to existing writing. The
discipline is the same as the rest of the workspace —
**clarity → correctness → introspection → beauty**. The poet's
"beauty" is the same operative criterion: if it isn't
beautiful, it isn't done. The discipline applied to prose is
the same discipline ESSENCE applies to code.

---

## The four-role orchestration model

### Roles and their lock files

| Role | Agent (default) | Lock file | Reports subdir | Primary scope |
|---|---|---|---|---|
| `operator` | Codex | `operator.lock` | `reports/operator/` | Rust crates, persona, sema-ecosystem implementation |
| `designer` | Claude | `designer.lock` | `reports/designer/` | ESSENCE, AGENTS, lore, skills, design reports |
| `system-specialist` | (any) | `system-specialist.lock` | `reports/system-specialist/` | CriomOS, CriomOS-home, lojix-cli, horizon-rs, goldragon |
| `poet` | (any) | `poet.lock` | `reports/poet/` | TheBookOfSol, substack-cli, prose-craft surfaces |

The "Agent (default)" column is convenience labelling for the
lock file, not a binding — any agent (Claude, Codex, future
others) can take any role; the role is what determines scope
authority, not which model holds it.

### Claim flow with N roles

A claim writes the active role's own lock file, then checks
overlap against **all other** active locks (not just one peer).
With four roles, that's three peer checks per claim. The
existing logic in `tools/orchestrate` checks one peer; the
refactor extends it to a loop.

### Cross-role overlap — natural primary scopes don't overlap much

- operator vs designer — overlap on `lore/`, `~/primary/AGENTS.md`,
  skill files, ESSENCE refinements. Handled today via lock-and-rebase.
- operator vs system-specialist — minimal overlap; operator
  works in sema-ecosystem repos, system-specialist in
  platform repos.
- designer vs poet — overlap on ESSENCE.md prose, on the
  reports' wording layer, and on any cross-cutting skills
  that touch writing discipline (TheBookOfSol's `AGENTS.md`
  carries writing rules; if those migrate to `skills/`, they
  could become a poet-owned skill).
- system-specialist vs poet — essentially none.
- system-specialist vs designer — overlap on
  `skills/system-specialist.md` itself (this very file) and on
  `protocols/orchestration.md` when system-related coordination
  rules land. Resolved through normal claim flow.
- operator vs poet — minimal; operator may touch substack-cli
  source if it's a Rust crate, but the writing surface is
  distinct.

The protocol doesn't need new cross-role rules; the existing
"claim before edit" + "release when done" + "lock files exempt
the role's reports/ subdirectory" handles four roles as cleanly
as it handles two.

---

## tools/orchestrate — Bash now, Rust later

### Current shape (Bash, 187 lines)

Strengths:

- Works. Lock semantics are correct. `paths_overlap`,
  `active_scopes`, `print_state` are clean.
- Trivially editable; no toolchain dependency.
- Lives at `tools/orchestrate` and is invoked directly.

Weaknesses against the four-role world:

- `peer_role()` is a binary case/esac: operator → designer,
  designer → operator. Doesn't generalise.
- Agent name is hardcoded in `write_lock` (operator → "Codex",
  designer → "Claude"). For new roles, the agent identity
  should be runtime-configurable.
- Lock-file naming is hardcoded (`operator.lock`,
  `designer.lock`). Generalising to `<role>.lock` is one-line.
- The whole tool is shell — no typed roles, no compile-time
  exhaustiveness check when adding a role.

### Decision — refactor Bash for N roles in this turn

The minimum to enable poet + system-specialist as coordination
roles is:

1. A list of all roles the tool knows about.
2. `peer_role()` becomes `peer_roles()` returning all roles
   except the active one.
3. `write_lock` reads the agent name from a config or accepts
   a `--agent` flag, defaulting to the role name.
4. Lock-file path derives from the role name.

This is ~30 lines of Bash refactoring. Doing it now lets the
new roles claim and release immediately.

### Decision — surface the Rust rewrite as a proposal

The user's question — *"we might want to actually rewrite it
in clean idiomatic Rust"* — is a good question, and the
operator already has an open bead (`primary-jwi`, P3) titled
*"harden the orchestrate helper into a typed Persona
component."* That bead is the natural home for the rewrite.

I do not land a Rust rewrite in this turn because:

1. **Out-of-scope cleanup** per
   `skills/autonomous-agent.md` — the user asked for the four
   roles to land, not for the helper to be rewritten now. The
   Rust rewrite is a substantial refactor.
2. **Operator's territory.** Operator built the Bash; operator
   has the bead for the Rust rewrite. Not my work to take.
3. **Eventually-impossible-to-improve principle.** The Rust
   rewrite shouldn't be a port of the Bash — it should be the
   Persona-component shape (typed records, the same Nota wire
   the rest of persona uses). That's a larger design question
   the operator owns.

The proposal below documents the shape so when the operator
picks up `primary-jwi`, the design intent is on file.

### Proposed Rust rewrite — `orchestrate` crate

A new repo (per `skills/micro-components.md` — one capability,
one crate, one repo): `LiGoldragon/orchestrate`.

**Surface (typed roles, Nota wire):**

```rust
pub enum Role {
    Operator,
    Designer,
    SystemSpecialist,
    Poet,
}

pub struct ScopeClaim {
    role: Role,
    paths: Vec<AbsolutePath>,
    reason: Reason,
}

pub struct Lock {
    role: Role,
    agent: AgentName,
    status: LockStatus,
    updated_at: Timestamp,
    active_scopes: Vec<ScopeEntry>,
}

pub enum LockStatus { Active, Idle }
```

**Claim flow as a method on `Workspace`:**

```rust
impl Workspace {
    pub fn claim(&self, claim: ScopeClaim) -> Result<Lock, Conflict>;
    pub fn release(&self, role: Role) -> Result<Lock, Error>;
    pub fn status(&self) -> Status;
}
```

**Wire format — Nota records on disk.** Each `<role>.lock`
is a single Nota record:

```nota
(Lock
  designer                       ;; role
  "Claude"                       ;; agent
  Active                         ;; status
  "2026-05-07T12:23:30+02:00"    ;; updated_at
  [(Scope "/path/one" "reason text")
   (Scope "/path/two" "reason text")])
```

This makes the lock file a typed record consumable by every
agent in the workspace, not just by the orchestrate tool.

**Distribution:** `orchestrate` ships a binary; the workspace
references it via flake input. The `tools/orchestrate` script
becomes a one-line wrapper that invokes the binary, or is
removed entirely.

**Persona alignment:** when persona's reducer is ready, the
orchestrate crate's `claim` becomes a typed Persona Command
(`ScopeClaimCommand`); the lock files become snapshot
projections of persona's state. The Bash → typed Rust → typed
Persona path is the staged migration.

**Until then,** the Bash works fine. This turn lands the
Bash N-role refactor; the Rust rewrite is an explicit
follow-up.

---

## What lands in this turn

A single coherent change-set:

1. **`protocols/orchestration.md`** — list four roles, four
   lock files, four report subdirectories. Update the role
   list and the canonical claim invocation.
2. **`~/primary/AGENTS.md`** — update the role list and the
   "Where things live" table.
3. **`tools/orchestrate`** — refactor `peer_role` to
   `peer_roles` (all-others); generalise lock-file paths;
   accept `--agent` flag with role-name default.
4. **`skills/system-specialist.md`** — drop the
   "is a capability, not a primary-workspace lock role"
   disclaimer; add a coordination section pointing at
   `protocols/orchestration.md`.
5. **`skills/poet.md`** — new skill file; what the poet does
   and where the poet works.
6. **`reports/system-specialist/`** and **`reports/poet/`** —
   create as empty directories with `.gitkeep`.
7. **`system-specialist.lock`** and **`poet.lock`** — create
   in idle state (so `tools/orchestrate status` reports
   coherently before either role has activity).

All of the above lands as one logical commit (the protocol +
helper + skills + lock seeds are one coordination change) and
gets pushed.

---

## Naming notes

- **`system-specialist`** with a hyphen — matches the existing
  skill filename. Lock file is `system-specialist.lock`. Role
  literal in code is `system-specialist` (kebab-case).
- **`poet`** — single word, no hyphen. Lock file is `poet.lock`.
  Role literal is `poet`.

These match the workspace's full-English-words discipline:
`system-specialist` over `sysspec`, `poet` over `wr` /
`writer-role`.

---

## What this turn does *not* do

- **Persona's `HarnessRole` enum** — keeps `Observer`. When the
  workspace's coordination role and persona's harness role
  unify (a future migration), `Observer` becomes
  `SystemSpecialist | Poet`. *Out of scope for this turn;
  operator's territory anyway.*
- **Move runbook material out of `system-specialist.md`** —
  the Cluster Nix signing section is tool-reference, not
  skill-shape. Flagged in `skills-roadmap.md`. *Defer.*
- **Rust rewrite of `tools/orchestrate`** — proposed above;
  operator's bead `primary-jwi`. *Defer.*
- **TheBookOfSol's writing conventions migrating to a
  workspace skill** — TheBookOfSol's AGENTS.md is project-local
  and reads cleanly; whether it should grow a `skills.md` or
  whether the conventions should lift to a `skills/prose.md` is
  a poet-side question to answer once the role exists. *Surface,
  don't decide.*

---

## Open questions for the user

1. **Agent identity for new roles.** When system-specialist or
   poet claim a lock, should the lock declare which model
   holds the role (Codex / Claude / other)? The current Bash
   has the agent name baked in at the role level. The
   refactor accepts `--agent` with a role-name default, but
   the user might prefer always defaulting to Codex/Claude
   based on their natural pairing with operator/designer.
2. **Default agent for poet.** Open. The poet's writing-craft
   discipline is something either model can do, but the user
   may have a preference (TheBookOfSol's existing convention
   in its `AGENTS.md` is generic to any agent that recognises
   the format).
3. **`reports/system-specialist/` vs `reports/system/`.** I
   chose the longer name (matches the role literal). The user
   may prefer the shorter form. Easy to rename later.
4. **`primary-jwi` rephrasing.** Operator's bead currently
   says "harden the orchestrate helper into a typed Persona
   component." With four roles in play, the bead may want
   updating to mention typed-roles-enum. Operator's choice;
   this report makes the proposal visible.

---

## See also

- `~/primary/protocols/orchestration.md` — the protocol this
  report extends.
- `~/primary/skills/system-specialist.md` — the existing
  capability skill.
- `~/primary/skills/autonomous-agent.md` — when to act and when
  to ask.
- `~/primary/reports/designer/2026-05-06-persona-messaging-design.md`
  — the persona destination that absorbs the lock protocol.
- `~/primary/reports/designer/2026-05-06-skills-roadmap.md` —
  the skills migration map; system-specialist's runbook flagged
  here.
- `~/primary/reports/designer/2026-05-07-session-handoff.md` —
  prior-session context.
- `TheBookOfSol/AGENTS.md` — writing conventions; substance
  the poet skill draws on.
- `persona/src/schema.rs` — `HarnessRole::{Operator, Designer,
  Observer}`; the future unification target.

---

*End report.*
