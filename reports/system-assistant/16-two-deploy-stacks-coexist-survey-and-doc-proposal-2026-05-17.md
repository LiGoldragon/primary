# 16 — Two deploy stacks coexist: survey and documentation proposal

Date: 2026-05-17
Role: system-assistant
Scope: survey only; no edits to the workspace, the skill, or any repo.

---

## Why this report

The user is worried a peer agent (especially a system specialist
arriving fresh) will confuse two parallel deploy stacks and either
edit the wrong files, deploy the wrong artefact, or fold the wrong
branch into production. The user asked for a survey of the current
state and a recommendation on where to document the
production-vs-development split — without editing the skill while
the skill consolidation (second-designer-assistant/1) is in flight.

This report is the survey + the recommendation. No edits made.

---

## What's actually on disk right now

### Stack A — **production today** (`main` branches, canonical `/git` checkouts)

This is what every node in the cluster is currently running and
what `lojix-cli` deploys today.

| Repo | Path | Tip change |
|---|---|---|
| `horizon-rs` | `/git/github.com/LiGoldragon/horizon-rs` | `vsrltmvu` (main) — old "fat" Horizon |
| `lojix-cli` | `/git/github.com/LiGoldragon/lojix-cli` | `vyyqsovy` (main) — monolithic CLI; consumes `horizon-rs/main` |
| `CriomOS` | `/git/github.com/LiGoldragon/CriomOS` | `txvqotnu` (main) — flake.lock pins `lojix-cli` at `42529ebd2114` |
| `CriomOS-home` | `/git/github.com/LiGoldragon/CriomOS-home` | main |
| `CriomOS-lib` | `/git/github.com/LiGoldragon/CriomOS-lib` | `yklxrsnp` (main) |
| `goldragon` | `/git/github.com/LiGoldragon/goldragon` | main — cluster data with the current `(criome, criome.net)` constants still in datom |

Deploy path: `lojix-cli` projects `horizon-rs/main` over
`goldragon/datom.nota` and writes `horizon`/`system`/`deployment`
inputs into `CriomOS`. **No daemon.**

### Stack B — **lean rewrite, in development** (`horizon-leaner-shape` branches, worktrees under `~/wt/...`)

This is the new shape — lean horizon proposal/view, pan-horizon
config split into its own repo, new `lojix` daemon + thin `lojix`
CLI client. SYS/134 smoke-built `zeus` end-to-end through
`prometheus` on this stack. **Not yet deployed.**

| Repo | Worktree | Tip |
|---|---|---|
| `horizon-rs` | `~/wt/.../horizon-rs/horizon-leaner-shape` | `45056dc4` — lean proposal/view + projection contract |
| `lojix` *(new repo)* | `~/wt/.../lojix/horizon-leaner-shape` | `5cc1eaf6` — daemon + thin client; canonical `/git/.../lojix` has only AGENTS+ARCH skeleton |
| `lojix-cli` | `~/wt/.../lojix-cli/horizon-leaner-shape` | empty/marker — per active-repositories.md the old CLI is **not** part of the arc and stays on main until cutover |
| `CriomOS` | `~/wt/.../CriomOS/horizon-leaner-shape` | `vrsrqvts` — consumes lean horizon projections |
| `CriomOS-home` | `~/wt/.../CriomOS-home/horizon-leaner-shape` | ditto |
| `CriomOS-lib` | `~/wt/.../CriomOS-lib/horizon-leaner-shape` | `yyvrmuss` — runtime catalogs (llama / NordVPN / resolver / DHCP) |
| `goldragon` | `~/wt/.../goldragon/horizon-leaner-shape` | lean datom; cluster constants migrated out |
| `criomos-horizon-config` *(new repo)* | `/git/.../criomos-horizon-config` (main) | `1218566e` — pan-horizon constants: operator, suffixes, LAN pool, reserved labels |
| `signal-lojix` | `~/wt/.../signal-lojix/horizon-leaner-shape` | wire surface for lojix daemon ↔ client |

### Loose third arc — `horizon-re-engineering`

Worktrees on `horizon-re-engineering` *also exist* for CriomOS,
goldragon, horizon-rs, and lojix. This is the older feature arc
that `horizon-leaner-shape` was built on top of and now supersedes.
`protocols/active-repositories.md` §"Replacement Stack" still names
`horizon-re-engineering` as the active arc — that text is stale.

---

## The risk surface — what can actually go wrong

1. **Edit the wrong checkout.** A system-specialist asked to "fix
   the DHCP pool" reads `goldragon/datom.nota` in `~/wt/.../goldragon/horizon-leaner-shape`
   (because that's the recently-touched worktree) and fixes the
   wrong file — production runs from `/git/.../goldragon/main`,
   which has different cluster data.
2. **Deploy the wrong stack.** Builds the dev stack and tries to
   activate it via the production `lojix-cli`. Schemas have
   diverged: the new horizon JSON doesn't match what the old
   `lojix-cli` projects.
3. **Fold dev branch into main prematurely.** Merges
   `horizon-leaner-shape` into `main` on one repo without the
   whole-stack cutover (e.g. merges `goldragon/horizon-leaner-shape`
   while CriomOS is still on `main`) — breaks production.
4. **Pick up the stale `horizon-re-engineering` arc.** Reads
   `protocols/active-repositories.md`, sees `horizon-re-engineering`
   named as active, and starts editing that branch. Work doesn't
   land anywhere useful.
5. **Add to the wrong CriomOS-lib.** Catalogs were added on
   `horizon-leaner-shape`; landing a new package on `main` won't be
   visible to dev-stack consumers, and vice versa.

---

## What I recommend

Three layers, smallest blast radius first.

### 1. Refresh `protocols/active-repositories.md` (highest leverage, smallest edit)

The §"Replacement Stack" section already exists and is the
"natural home" for this kind of cutover state. Two changes:

- Replace the active-arc paragraph (currently names
  `horizon-re-engineering`) with: `horizon-leaner-shape` is the
  active arc; `horizon-re-engineering` worktrees are superseded.
- Add an explicit "Two deploy stacks coexist" sub-section listing
  Stack A (production, `main`, canonical `/git`) vs Stack B
  (`horizon-leaner-shape`, worktrees) and the cutover state (Stack
  B smoke-builds but does not deploy to any node).

This is a doc that agents already read for repo orientation.
Editing it does not touch the skill that's currently being
consolidated.

### 2. Add a short safety section to workspace `AGENTS.md`

`AGENTS.md` already carries the same shape of cross-cutting safety
rule ("Nix store search is forbidden", "Feature branches live in
worktrees, not the canonical checkout"). The new section would be
~15 lines and would point at `protocols/active-repositories.md`
for the live inventory.

Why `AGENTS.md` and not a skill: this is a workspace-wide safety
rule for any role that touches deployment-adjacent code — not just
system-specialist. A system-assistant doing a CriomOS-home audit,
a designer reading horizon shapes, an operator deploying a fix all
hit the same trap. `AGENTS.md` is the always-loaded surface every
agent reads first; a skill file is only loaded by the role it
belongs to.

### 3. Per-repo `AGENTS.md` one-liner (lowest priority; do last or skip)

In each of the six canonical `/git/.../{horizon-rs,lojix-cli,CriomOS,CriomOS-home,CriomOS-lib,goldragon}/AGENTS.md`,
add a single line near the top:

> This is the **production** checkout (`main`). The lean rewrite —
> new lojix daemon + thin CLI + lean horizon — lives in
> `~/wt/.../<repo>/horizon-leaner-shape`. See
> `primary/protocols/active-repositories.md` §"Two deploy stacks"
> before editing.

This catches an agent who lands directly in the repo and never
reads workspace AGENTS.md.

---

## What the safety section in workspace `AGENTS.md` would say

Drafted in the same shape as the existing "Feature branches live
in worktrees…" section. Not yet edited in.

```markdown
## Two deploy stacks coexist — production and the lean rewrite

**Production today** runs the old monolithic `lojix-cli` stack on
`main` branches in the canonical `/git/...` checkouts:
`horizon-rs`, `lojix-cli`, `CriomOS`, `CriomOS-home`, `CriomOS-lib`,
`goldragon`. If you need to fix something that is live right now,
the fix goes on `main` in those checkouts.

**The lean rewrite** — new `lojix` daemon + thin `lojix` CLI client
+ lean horizon proposal/view + pan-horizon config — lives on
`horizon-leaner-shape` branches in worktrees under `~/wt/...`,
plus two new repos: `lojix` and `criomos-horizon-config`. It
smoke-builds end-to-end (see `reports/system-specialist/134`) but
**has not been cut over**. No node in the cluster runs it. Do not
deploy it as if it were a fix.

**Do not fold one stack into the other piecemeal.** Schemas have
diverged. Cutover happens as a coordinated multi-repo merge after
the rewrite reaches feature parity and the migration is staged per
`protocols/active-repositories.md` §"Replacement Stack". Until
then: production edits → `main`; rewrite edits →
`horizon-leaner-shape` worktree.

The live inventory of what is on which branch (and which arc is
active) lives in `protocols/active-repositories.md`. Stale
worktrees on `horizon-re-engineering` are superseded; don't pick
that branch up.
```

---

## Why I am not editing anything

The user explicitly said *"you shouldn't edit this skill"* and
*"I just want you to give me an idea of how you think we should
do this"*. The skill consolidation pass
(`reports/second-designer-assistant/1-...`) is also actively
reshaping the skill surface and the orchestrate tool — landing my
recommendation as edits before the user has chosen the venue would
collide with their work.

This report is the inventory + draft. The user picks the venue (or
asks for adjustments) before any edits land.

---

## Open question for the user

The three layers above are additive, not exclusive. The lightest
useful version is (1) alone — refresh `active-repositories.md` and
trust agents to read it. (1)+(2) gives a safety net for agents who
don't open `active-repositories.md`. (1)+(2)+(3) catches the
agent who never opens workspace `AGENTS.md` either. Pick whichever
trust level matches the user's experience of how peer agents
behave.
