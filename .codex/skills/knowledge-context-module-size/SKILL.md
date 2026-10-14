---
description: What is known about context module size, loading, and adherence.
dependencies: [knowledge-context-strata, knowledge-claude-harness, knowledge-codex-harness]
---

No reviewed evidence establishes a universal optimum for a context module in
words, lines, or tokens. The 500-line recommendation in Anthropic's Agent
Skills authoring guidance is provider guidance for maintainability and
progressive disclosure, not an experimentally verified adherence cutoff. The
Mind instruction to write source files in pieces of a few hundred lines is
undefined operational guidance; it does not define a hard threshold.

The same Anthropic overview describes its provider architecture as roughly
100 tokens per Skill's metadata always loaded, a Level 2 instruction body
under 5,000 tokens when triggered, and no token cost for bundled resources
until accessed. This describes that provider's loading and budget model; it is
not a measured adherence optimum, a local loader cap, or a conversion between
lines, words, and tokens.

Individual module size, the dependency closure actually loaded, cumulative
input budget, constraint count and composition, instruction position and
hierarchy, and output-length constraints are separate variables. A context
window is a budget shared with output and other request material. ComplexBench
and SIFo show that constraint composition, dependency, and order affect
performance even with short inputs; LIFBench and LongIns show model- and
task-dependent effects of long cumulative inputs in their own benchmarks;
LIFEBench measures output-length behavior, not instruction-module capacity;
the Instruction Hierarchy studies privilege and conflicts, not an ideal module
size. These sources do not isolate a universal split threshold.

The harness and registry determine what is loaded. Curriculum indexes the
authored Markdown sources in the configured Psyche, Mind, and Field roots and
expands requested roots through dependencies once, dependency first. Its
projection writes complete generated skill bodies for the supported harness
surfaces and complete standing role packets. Claude launch code expands the
selected source bodies after stripping frontmatter; Codex resolves selected
native skills by name and canonical path, records their source hashes, and
submits typed skill inputs. The launcher's selected closure and the runtime
deployment are distinct observations: config pins, local checkouts, generated
trees, and deployed packets can differ.

The 2026-10-14 inventory counted 136 authored Markdown loader inputs in the
checked-out worktrees: Psyche 41, Mind 45, and Field 50. Psyche's count
includes its current `vision/ethos.md` input alongside 40 `skills/*.md`
files. It measured bytes,
newline lines, and `LC_ALL=C wc -w` words, including frontmatter. It did not
measure model tokens, and the snapshot's rows and revisions are recorded in
`evidence/context-module-inventory.md`; the landing itself changes the Mind
count. The inventory snapshot records Psyche base
`bf03117b424413cea4c3df7cf76a279127c8567d`, Mind base
`344f6c3669d3d882f96f63ed435022a3cfed2bf4`, and Field base
`5070467dd8b596246c47e9cbcbf55415025483fc`; Mind and Field also had dirty or
untracked worktree state. The exact dirty contents are not pinned or
reconstructible from those base revisions. The largest rows are review candidates only when their statements have
multiple coherent owners. Size alone does not prove a split.

The current direction is to keep each statement in one coherent home and to
avoid automatic splitting or module proliferation. A split is a hypothesis
that needs a matched workload test on the target model and harness. Measure
individual module size and cumulative loaded input for budget safety, then
measure adherence with the actual constraints, dependencies, position,
hierarchy, model version, task, and output demand held or varied explicitly.

Primary evidence and exact source revisions for these claims are in
`evidence/instruction-length-research.md`.
