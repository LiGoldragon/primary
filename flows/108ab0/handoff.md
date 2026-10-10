# Handoff from 108ab0 to the next primary Psyche opus

Written 2026-09-17 by primary Psyche opus (Claude, medium, flow 108ab0)
in one turn, at the living's direction, before refresh.

## What ran this session

- Refreshed from the launch brief that named predecessor 9993b5. That flow
  was archived — the actual lane on disk was `flows/da1e3f/` (previous
  primary Psyche opus). Ten `operational-*.md` vision entries plus one
  Codex brief were the substrate.
- Verified the Codex reset credit was consumed at 20:15Z today; primary
  window sits at 93% remaining, two credits left, resets next Thursday.
- Proved end-to-end messaging to Codex primary. `codex queue --thread
  <thread> --message <text>` returns exit 0, payload lands in the queue
  DB typed `UserInput` (Codex's user-stratum envelope, distinct from
  system/developer). Delivery into the rollout happens at the recipient's
  next turn — his current one is mid-flight on `wait_agent`.
- Landed three skill edits in Curriculum through a write-ordinary subflow:
  a paragraph in `main-flow.md` introducing subflow scripts, a new term
  in `vocabulary.md`, and a new `subflow-scripts` skill with the initial
  catalogue (`find-codex-session`, `queue-to-codex`, `read-transcript-tail`).
  Curriculum was regenerated; primary skill trees updated and pushed.
- Logged eleven verbatim psyche entries in this lane as
  `operational-*.md`, covering: psyche propagation (an "abrupt"
  Luna-driven propagator subflow), same-tree rule for primary, aggressive
  disk hygiene, fresh primary from the first commit, primary's living
  anatomy, distillation hierarchy Notion→Vision→Intent→Spirit, skills as
  vision, Curriculum overhaul into a typed module system, and
  programmatic prompt composition.

## Rulings from the living, this session

- **Subflow-first main flow.** The main flow never runs mechanical
  investigations itself — locates, probes, peer-messages and tail-reads
  go through subflow scripts, sonnet-class, that return semantic
  outcomes.
- **The main flow never sees noise.** No UUIDs, session ids, rollout
  paths, or long hashes reach the main flow's context. Subflow scripts
  keep those inside themselves.
- **A subflow script is what such a named subflow is called.**
- **Primary contains only distilled psyche.** `Vision/`, `Intent/`,
  `Spirit/` (capitalize), later `Notion/`. Plus top-level rule files.
  Generated skill trees are fine — they regenerate.
- **Flows live in a separate repository.** They are the dirty side.
- **Distillation moves upward.** Raw psyche → distilled Notion → Vision →
  Intent → Spirit.
- **Skills are vision.** Vision-as-skill is the direction; bring things
  back to that when touched. Operational skills carry glance-approval —
  agent-authored, retract-at-will, lighter authority.
- **Skill and vision are unified.** No separate Datom skill and Datom
  vision — same file. A topic has faces: core (named by topic, e.g.
  `datom.md`), extended (`datom-extended.md` or a variant path), and
  subtopic-specific extensive views. Raw vision and raw Notion stay as
  the source distilled into these.
- **Operational skills live in their own repo.** A separate module,
  `operational-` prefix, agent-authored, less human-reviewed, more
  removable than Vision — likely to be taken out when something better
  is found.
- **Begin distilling now.** Raw vision and raw Notion get distilled into
  unified topic files (core and extended). Working instruction, not
  vision.
- **Curriculum overhauled into a typed module system.** Modules have a
  type declared in each Markdown's frontmatter; Curriculum is a nexus
  that reads a manifest of paths and walks them; data lives outside.
- **Same tree for primary.** Do not worktree primary — it is too
  expensive to copy. Merger role hires someone to keep every worktree
  rebased onto main.
- **Aggressive disk garbage collection.** Old worktrees, leftover build
  directories, transcripts older than the last lunation — cleaned up
  aggressively. Archive the psyche turning points before deletion.

## Open questions to the living, in order of impact

1. **Ordering of the fresh-primary cut.** Migrate every existing lane to
   the flows repo first, then cut fresh primary from the trimmed state?
   Or fresh cut now, old primary retires as archive?
2. **Flows repo name.** Proposed `flows`.
3. **Same-tree scope.** Does Codex primary move out of his bootstrap
   worktree to `/home/li/primary` now, or only future launches?
4. **Merger role shape.** Subflow script invoked on each main move, or a
   persistent Flow-owned watcher?
5. ~~What is "extended vision"?~~ **Answered mid-handoff.** Core Vision =
   the most important concepts, more reviewed, more weight, more certain,
   usually more basic and broad. Extended Vision = elaborate detail with
   examples, less reviewed; may promote into core; must not conflict with
   core (conflicts are surfaced). See
   `vision/operational-coreAndExtendedVision.md`.
6. **Skill data location.** Proposed: types live in primary as
   `Vision/`, `Intent/`, `Spirit/` (etc.); Curriculum walks primary by
   manifest.
7. **Manifest form.** Proposed: type in each Markdown's frontmatter plus
   one small `curriculum-manifest.datom` naming repos and directories.
8. **Psyche-propagation subflow — anatomy.** Abrupt = mid-turn-interrupt
   or prioritized-end-of-turn? Default-required routes? Shared-psyche
   cluster marker?
9. **Glance-approval mechanism.** Proposed: `glance-approved by <flow>`
   header in the skill body, no round-trip, retract-at-will.
10. **Juncture-point classifier.** Who classifies old transcripts before
    the pre-lunation cutoff — a Luna sweep, or main-flow review?

## Skill edit proposals staged, not dispatched

- `psyche.md` — upward-distillation paragraph.
- `psyche-distillation.md` — Vision→Intent and Intent→Spirit passes;
  distilled-Notion first pass.
- `skill-designing.md` — introduce operational-skill category.
- `vocabulary.md` — `Notion (distilled)`, `operational skill`,
  `distillation hierarchy`.

## Paired flows

- **Primary Psyche fable** — Flow 79715b (per launch brief;
  unverified), HIGH, conserving. Not messaged this session.
- **Primary Psyche sonnet** — Flow 3f2a43 (per launch brief;
  unverified), LOW, watching/filtering. Not messaged this session.
- **Primary Codex** — thread "Primary Codex, recovery of 2026-09-17 ·
  resets its own usage". Briefed at launch to relay every
  living-typed message to us. One test message queued this turn,
  awaiting his current-turn end.

## Messaging paths that work

- **To Codex (any thread):** `codex queue --thread <UUID-or-name>
  --message <text>`. Proven, exit 0, payload typed `UserInput`.
- **To Claude (this direction from Codex):** prompt-relay mid-turn
  injection. Native to Claude Code.
- **Not yet:** mid-turn abrupt interrupt into Codex. Living asked for a
  Luna-based propagator subflow that gets closer.

## First-task pointers for the successor

1. Read the living's ruling on the open questions above — especially
   items 1–7, which anchor the Curriculum overhaul and the fresh-primary
   cut.
2. If the living has already answered any while this handoff was being
   written, treat that answer as the live one.
3. Check Codex primary's rollout tail (via the `read-transcript-tail`
   subflow script) — my test message may have landed and been answered.
4. Do not undertake the fresh-primary cut, the flows-repo split, or the
   Curriculum overhaul without the living's explicit ordering ruling.
   The successor's first productive move is likely dispatching a design
   subflow to draft the Curriculum overhaul spec — after answers to
   items 5–7.

## Rules for the successor to hold from turn one

- Subflow-first. Delegate every locate, probe, tail-read, peer-message.
- No UUIDs, no session ids, no rollout paths, no long hashes in main
  flow context. Ever. Subflow scripts filter noise.
- Every write reserves an orchestrate lock over the affected paths;
  release on commit or rollback.
- Primary always committed and pushed before idle. Dirty tree committed
  first as its own commit.
- Never do skill file edits directly. Propose wording to the living;
  when approved, dispatch a write subflow that operates in Curriculum
  and regenerates primary's skill trees. Primary itself never edits
  `.claude/`, `.codex/`, `.agents/`, `.pi/`.
