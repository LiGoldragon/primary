# Role-skill consolidation — survey and proposal

*Second-designer-assistant survey of the role-skill, lock-file,
orchestrate-tool, and protocols layout. Maps the user's intent onto
concrete moves with a safe migration order.*

Date: 2026-05-17

---

## TL;DR

The workspace has **eleven role-skill files** (~3,000 lines) of which
**seven are assistant lanes** that overwhelmingly restate their main
role's reading list, beads label, and claim shape. The four
`second-*` files explicitly say so — they're declared as "copies" with
three identifiers swapped (lock filename, report lane, claim role).

The proposed simplification has four orthogonal pieces:

1. **One skill per discipline.** Collapse the seven assistant skill
   files into a tiny `skills/role-lanes.md` (the meta-pattern) plus
   one short *"Working with assistants"* section inside each of the
   four main role skills. Net: 11 role-skill files → 4 + 1.
2. **Move orchestration out of the workspace root.** New
   `orchestrate/` directory holds the protocol doc + all lock files;
   `tools/orchestrate` stays where it is (or moves too — see §4).
3. **Migrate locks gradually** because four roles are actively
   holding paths right now. New directory is created and the tool
   reads from both locations during a transition window; agents only
   see the change as a path update in their skill.
4. **Rewrite the orchestrate tool** so adding a role / assistant lane
   is a config-file edit, not a shell-array edit. Recommendation:
   keep shell for now and externalise the role list to one
   declarative file; bigger Rust rewrite waits for the `mind` CLI
   destination already named in `protocols/orchestration.md`
   §"Command-line mind target."

The user's intuition that *"agents just use the tool"* is correct —
nothing outside the tool, the protocol doc, the role-skill files,
and `.gitignore` references lock files by name. Renaming or moving
locks does not require agent notification beyond updating those four
surfaces.

**Side-find:** `.gitignore` is missing `/system-assistant.lock` even
though that lock file exists at workspace root and is currently in
use by `system-assistant`. One-line fix, unrelated to consolidation.

---

## Current state

### Eleven roles, eleven lock files, eleven report lanes

| Role               | Lock file                          | Report lane                          | Status now |
|--------------------|------------------------------------|--------------------------------------|------------|
| operator           | `operator.lock`                    | `reports/operator/`                  | held (1 path) |
| operator-assistant | `operator-assistant.lock`          | `reports/operator-assistant/`        | idle |
| second-operator-assistant | `second-operator-assistant.lock` | `reports/second-operator-assistant/` | idle |
| designer           | `designer.lock`                    | `reports/designer/`                  | idle |
| designer-assistant | `designer-assistant.lock`          | `reports/designer-assistant/`        | idle |
| second-designer-assistant | `second-designer-assistant.lock` | `reports/second-designer-assistant/` | **held (me)** |
| system-specialist  | `system-specialist.lock`           | `reports/system-specialist/`         | held (8 paths) |
| system-assistant   | `system-assistant.lock`            | `reports/system-assistant/`          | held (2 paths) |
| second-system-assistant | `second-system-assistant.lock` | `reports/second-system-assistant/`   | idle |
| poet               | `poet.lock`                        | `reports/poet/`                      | idle |
| poet-assistant     | `poet-assistant.lock`              | `reports/poet-assistant/`            | idle |

Four roles are actively holding paths (operator, system-specialist,
system-assistant, me). Migration plans must not yank those locks out
from under them.

### Skill-file sizes — duplication is concentrated in the assistants

```
skills/designer.md                 508 lines
skills/designer-assistant.md       216 lines  ── 90%+ duplicates designer
skills/second-designer-assistant.md 130 lines  ── 95%+ duplicates designer-assistant
skills/operator.md                 484 lines
skills/operator-assistant.md       231 lines  ── 90%+ duplicates operator
skills/second-operator-assistant.md 122 lines  ── 95%+ duplicates operator-assistant
skills/system-specialist.md        320 lines
skills/system-assistant.md         284 lines  ── 90%+ duplicates system-specialist
skills/second-system-assistant.md  129 lines  ── 95%+ duplicates system-assistant
skills/poet.md                     231 lines
skills/poet-assistant.md           187 lines  ── 90%+ duplicates poet
                                   ─────
                              3,445 total
```

The duplicated material is the **required-reading list, the
working-pattern boilerplate, and the see-also block** — three
sections that on average account for ~80% of each assistant file.
The genuinely distinct content per assistant skill is:

- a one-paragraph **owned-area carve-out** (bounded slices vs final
  authority);
- a **when-to-choose** section (a couple of bulleted triggers);
- in `*-assistant.md`, sometimes a **mode-specific** working
  pattern (e.g. operator-assistant's *"Default to audit on
  high-risk paths"*).

The four `second-*` skills carry **none** of that distinct content.
They explicitly state they "copy" the assistant skill and differ only
in three identifiers. The lines below are quoted verbatim from
`skills/second-designer-assistant.md` (and the same shape appears in
the other three `second-*` files):

> All scope, authority, design, report, and version-control rules
> from `skills/designer-assistant.md` apply unchanged. The only
> differences are:
>
> - lock file: `second-designer-assistant.lock`;
> - report lane: `reports/second-designer-assistant/`;
> - claim role: `second-designer-assistant`.

That is a textbook case of `ESSENCE.md` §"Efficiency of instruction":
*Each rule, principle, or pattern lives in one canonical place. Other
docs cite by reference; they don't restate.*

### What references lock files by name

A `grep` across the workspace (excluding `repos/` and `reports/`)
turned up references to lock files or `protocols/orchestration.md` in:

- `tools/orchestrate` — reads/writes the locks; hardcodes role names
  in a single bash array.
- `protocols/orchestration.md` — the protocol doc (canonical
  prose).
- `AGENTS.md` — the role table near the top.
- Every role skill file — references its own lock and report lane.
- `.gitignore` — lists ten of the eleven lock filenames explicitly
  (`/system-assistant.lock` is missing — see §"Side-find" below).

**Nothing else.** No CI job, no separate tool, no agent-private code
opens lock files directly. The user's read is correct: agents
discover the claim shape through the role skill, which points at the
tool. Move the locks, update the tool + protocol + skills +
gitignore, and the agents will follow on next read.

---

## Proposed shape

### 1. Skill consolidation — one skill per discipline

```
Before                                  After
──────                                  ─────
skills/designer.md                      skills/designer.md (+ short
skills/designer-assistant.md              "Working with assistants" section)
skills/second-designer-assistant.md     skills/operator.md (same)
skills/operator.md                      skills/system-specialist.md (same)
skills/operator-assistant.md            skills/poet.md (same)
skills/second-operator-assistant.md     skills/role-lanes.md (new — meta-pattern)
skills/system-specialist.md
skills/system-assistant.md             (7 files deleted)
skills/second-system-assistant.md
skills/poet.md
skills/poet-assistant.md
```

`skills/role-lanes.md` carries the meta-pattern — *one canonical
home* — for everything currently duplicated across the seven
assistant skills:

- A main role has any number of **assistant lanes** stacked under it:
  `<role>-assistant`, `second-<role>-assistant`,
  `third-<role>-assistant`, ... All lanes share the main role's
  identity, required reading, beads label, and discipline.
- What's per-lane: **lock filename**, **report lane**, **claim
  string**. That's the whole list.
- Why the lanes exist: parallel capacity that's visible to the
  coordination protocol. A second agent working under a main role
  with no lock of its own is an invisible peer.
- Beads belong to the main role's label, not the assistant's (this
  rule already lives in `protocols/orchestration.md` §"Beads belong
  to main roles" — `role-lanes.md` should cite it, not restate it).

Each main role's skill (e.g. `skills/designer.md`) gains a short
**"Working with assistants"** section — three to ten lines — that
inherits from `role-lanes.md` and adds *only* the role-specific
guidance (e.g. designer's mention of high-risk audit paths,
system-specialist's "defer on cluster-effecting changes"). The
audit-mode triggers, when-to-choose lists, and bounded-work
checklists currently scattered across the assistant files fold
into that section.

**Why this is the right shape.** The assistants don't have a
different discipline; they have the same discipline with a
narrower-scope expectation. Splitting that into eight files
(four assistants + four second-assistants — and the user's
hinted-at "third-assistant" would make twelve) is the
fragmentation `ESSENCE.md` §"Today and eventually" and
§"Efficiency of instruction" both warn against. The
meta-pattern is the canonical home; the role skills carry
discipline; per-lane bookkeeping is three identifiers.

**Alternative considered (rejected): stub files per lane.** Keep
`skills/designer-assistant.md` as a three-line file saying *"read
`skills/designer.md` + `skills/role-lanes.md`."* Cheaper than the
collapse but still produces a fan-out of one-purpose stubs that the
user has to maintain in lockstep with the main skills. The collapse
is the durable shape.

### 2. `orchestrate/` directory at the workspace root

```
Before                                  After
──────                                  ─────
ESSENCE.md                              ESSENCE.md
AGENTS.md                               AGENTS.md
CLAUDE.md                               CLAUDE.md
MEMORY.md                               MEMORY.md
GOALS.md                                GOALS.md
RECENT-REPOSITORIES.md                  RECENT-REPOSITORIES.md
protocols/                              protocols/
  orchestration.md                        active-repositories.md  (stays)
  active-repositories.md                orchestrate/
tools/orchestrate                         AGENTS.md   (was protocols/orchestration.md)
*.lock  (× 11, runtime state)             roles.toml  (new — see §4)
                                          *.lock      (× 11, runtime state)
                                        tools/orchestrate  (unchanged path, updated implementation)
```

The new `orchestrate/AGENTS.md` is the protocol that today lives at
`protocols/orchestration.md`. Choosing `AGENTS.md` (not `README.md`)
puts it on the path that every agent already reads when entering a
directory — the same pattern `lore/AGENTS.md` and per-repo
`AGENTS.md` use.

**Why the move.** Workspace root currently shows ten `.lock` files
plus seven workspace docs plus the `protocols/`, `reports/`,
`repos/`, `skills/`, `tools/` directories. The `.lock` files are
visual clutter for any agent listing the root — they look like
content but they're transient coordination state. Folding them into
their own directory with the protocol they implement is the right
neighborhood.

`protocols/active-repositories.md` stays where it is — it's not
orchestration state, it's an active-repo map. The `protocols/`
directory thins to one file; eventually it can probably absorb other
workspace-level protocol docs or itself collapse.

### 3. Migration order — safe under live lock-holders

Because operator, system-specialist, system-assistant, and I are
currently holding locks, the migration is staged:

1. **Add the new shape alongside the old** — without removing
   anything yet:
   - Create `orchestrate/` directory.
   - Write `orchestrate/AGENTS.md` (initial copy of
     `protocols/orchestration.md`, edited for the new locations).
   - Write `skills/role-lanes.md` (the new meta-pattern skill).
   - Update `skills/designer.md` / `operator.md` /
     `system-specialist.md` / `poet.md` with their *"Working with
     assistants"* sections (folding in the assistant-specific
     content that survives).
   - Update `tools/orchestrate` so it can **read and write** lock
     files in either `<workspace>/<role>.lock` (old) or
     `<workspace>/orchestrate/<role>.lock` (new). During the
     transition the tool prefers the new path for writes and
     falls back to the old path for reads.
   - Update `.gitignore` to ignore both locations (and add the
     missing `/system-assistant.lock` — see §"Side-find").

2. **Have every active role release once and reclaim under the new
   path.** Active roles right now: operator, system-specialist,
   system-assistant, me. Each agent's next claim/release naturally
   moves it onto the new path. The tool's dual-read keeps idle
   roles' old empty lock files coherent until they're swept.

3. **Delete the old locations once all active roles have rotated.**
   `protocols/orchestration.md` becomes a one-line shim pointing at
   `orchestrate/AGENTS.md` (or is removed entirely — see open
   question §A below). Old `*.lock` files at root are deleted; tool
   loses the dual-read code. Assistant skill files are deleted.
   AGENTS.md role-table prose is updated to point at the new
   skills.

4. **Update the role-discovery surfaces** — `AGENTS.md` role table,
   the see-also blocks in remaining skills, any cross-references.

The reason to stage is purely about live lock-holders, not about
deeper coupling. Once all active roles have rotated through the new
path, the old surface is dead and can be deleted in one commit.

### 4. Better orchestrate tool

Today's `tools/orchestrate` is 242 lines of bash. The "ad hoc"
feeling the user named is mostly the **role list hardcoded twice**
(the `ROLES=(...)` array on line 6, and the usage string and CLI
validation that hand-mention the same names). To add a role you edit
both places.

The minimum-credible cleanup:

- Externalise the role list into `orchestrate/roles.toml` (or
  `roles.nota`, see open question §C). One declarative source of
  truth, parsed once on tool startup. Adding `third-designer-assistant`
  becomes one line in that file.
- A role entry declares its main-role lineage. The "beads belong to
  main roles" rule then drops out of data: every assistant lane
  inherits its main role's beads label.

```toml
# orchestrate/roles.toml (sketch — not the final shape)

[role.designer]
discipline = "designer"

[role.designer-assistant]
discipline = "designer"
assistant-of = "designer"

[role.second-designer-assistant]
discipline = "designer"
assistant-of = "designer"

# ... etc
```

Where the bigger rewrite belongs is the question
`protocols/orchestration.md` §"Command-line mind target" already
names: **the `mind` CLI talking to `persona-mind` as the destination
for all of this.** The orchestrate shell helper is explicitly a
transitional artifact. Spending much effort rewriting it in Rust now
duplicates work that the `mind` CLI will replace; spending zero
effort leaves the role list awkward to extend. The proposal sits in
the middle: keep shell, externalise the role list.

---

## Open questions for the user

**§A. Where does `protocols/orchestration.md` end up?**
Three options:
1. Move to `orchestrate/AGENTS.md` and delete the old path.
2. Move and leave a one-line shim at `protocols/orchestration.md`
   pointing at the new location (kindest to any external link).
3. Move to `orchestrate/AGENTS.md` and rename the directory itself
   from `protocols/` to something narrower (e.g. fold
   `protocols/active-repositories.md` into the root). My weak default
   is option 1 — the workspace doesn't publish external links to
   that path, and the shim adds maintenance with no payoff.

**§B. Naming of the new meta-skill.**
Candidates: `skills/role-lanes.md`, `skills/roles.md`,
`skills/assistant-lanes.md`. I lean `role-lanes.md` because the file
is about *the lane mechanism*, not about role identity (which lives
in each `<role>.md` skill). User vocabulary preference welcome.

**§C. `roles.toml` vs `roles.nota`.**
The workspace's direction is *Nota everywhere* — `lojix-cli` is
already one Nota record (per `skills/system-specialist.md` §"Operator
interface — Nota only"). If we want the role config to land in the
canonical workspace shape, it's Nota, not TOML. But Nota requires
`nota-codec` to be on the orchestrate tool's read path, which raises
the tool from "self-contained bash" to "links a Rust parser." TOML
is faster to land; Nota matches the workspace's eventual shape.
Recommend TOML for the shell helper, with the understanding that
the `mind` CLI rewrite uses Nota natively.

**§D. Order: skill consolidation first, or directory move first?**
The four pieces are mostly independent. My recommended order is:

1. `.gitignore` fix (one line, no downstream impact).
2. Skill consolidation (read-only for the tool — no lock-file moves).
3. New `orchestrate/` directory created alongside, tool dual-reads.
4. Active roles rotate through.
5. Old surfaces deleted; tool rewrite externalises role list.

This minimises the window where coordination state is split across
two locations. Open to flipping if there's a reason to prioritise
the directory move first.

---

## Side-find — `.gitignore` is missing `system-assistant.lock`

`.gitignore` lines 32-41 list ten of the eleven lock filenames.
`/system-assistant.lock` is absent. The file exists at workspace
root, is currently in use (held by `system-assistant` with two
paths), and would be committed if anyone runs `git add` on root.
Unrelated to the consolidation; flagging because the survey turned
it up.

Fix is one line:

```diff
 /designer-assistant.lock
 /second-designer-assistant.lock
 /system-specialist.lock
+/system-assistant.lock
 /second-system-assistant.lock
 /poet.lock
 /poet-assistant.lock
```

---

## What this report doesn't decide

- The actual content of `skills/role-lanes.md` (drafting it is the
  next-step work, after the user confirms shape).
- The actual content of each main role's *"Working with assistants"*
  section (same — depends on whether some content stays per-role or
  promotes to the meta-skill).
- Whether to extend `orchestrate/roles.toml` to declare *report lane
  path* and *lock filename* alongside *assistant-of*, or leave those
  as conventions in the tool. Either works; the declarative form is
  more self-documenting.

I'd value the user's direction on §A-§D before drafting the actual
changes.

---

## See also

- this workspace's `protocols/orchestration.md` — current protocol
  prose; destination is `orchestrate/AGENTS.md`.
- this workspace's `tools/orchestrate` — the shell helper to be
  cleaned up.
- this workspace's `ESSENCE.md` §"Efficiency of instruction" — the
  one-canonical-home principle that makes the assistant-skill
  duplication the right thing to collapse.
- this workspace's `ESSENCE.md` §"Today and eventually" — names
  the shell-helper-now / `mind`-CLI-later split that informs the
  tool-rewrite scope.
- this workspace's `skills/designer.md`, `skills/operator.md`,
  `skills/system-specialist.md`, `skills/poet.md` — the four
  main role skills that absorb each discipline's
  *"Working with assistants"* section.
