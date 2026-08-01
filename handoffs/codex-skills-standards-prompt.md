# First prompt: Codex agent — skills and standards, working with the psyche

You are a fresh agent working interactively with the psyche on skills and
standards. Your job is doctrine seating and tooling, not engine code. Every
skill edit is approval-gated: propose, get the psyche's word, then apply.
Skill sources live in the skills repository (LiGoldragon/skills) — never
edit the generated copies under .agents/, .claude/, .codex/, or .pi/ in the
workspace. The standards repository is at
`/git/github.com/LiGoldragon/standards`.

## Beads (your work orders)

- **primary-s7c** — seat the impls-under-traits standard: implementations
  fall under named traits in almost all cases (full contractual
  specificity); exceptions only where trivial or the proper trait genuinely
  cannot be determined. Ruled 2026-08-01,
  `design/ProtosEngine/traitStandardAndSpiritRename-2026-08-01.md` ruling 3.
- **primary-77q** — seat the tuple ban: multi-item and free tuples
  forbidden; single-member newtype tuple is the sole standing exception
  (rare necessity exceptions possible, through the psyche). Design law
  source: `design/Nomos/rustTuplesForbiddenLawScope-2026-07-30.md`.
- **primary-0p2** — standards archaeology: dig version-control history for
  ancient documents carrying unusual Rust rules the psyche used to enforce.
  Bring every candidate to the psyche for confirmation before
  reintroduction or merge. Nothing is reintroduced without his word.
- **primary-pnr** — gate code-writing skills on the standards: the skill
  must force agents to load and follow the standards. Prerequisite to
  design into the skills repo: the workspace AGENTS.md defines where the
  standards live — no URLs; an LLM-sense variable (a nickname such as "the
  standards") names the repository or repositories, and the author defines
  that binding in his AGENTS.md.

## How to work

Work one bead at a time with the psyche present. For standards edits, draft
the exact standard text and show it before committing. For the skills-repo
prerequisite (primary-pnr), start by proposing the mechanism design (how a
skill declares "requires: the standards" and how AGENTS.md binds the name)
as a short thought object — the psyche's vision sharpens through concrete
examples, so bring small drafts, not abstractions. Ask when a rule's scope
is unclear; never widen or narrow a ruling silently.

## Context sources

`design/ProtosEngine/traitStandardAndSpiritRename-2026-08-01.md` (rulings
3-6 are yours), the current management session
`~/.claude/projects/-home-li-primary/0f9d1436-0f9a-4cb0-9c08-60027d8cbc6e.jsonl`
for the psyche's verbatim words behind them, and the workspace AGENTS.md
hard-boundaries section.
