# Harness Context-Rung Mechanics — 2026-08-16

Provenance: verified findings relocated from the Design awareness
file (which now keeps only the general principles). Established in
the Design sessions of 2026-08-13/14 (`6863ef19`, `ba906ae2`,
`1030529c`) via in-session subagent probes; the skill-rung claim
survived an adversarial second pass that refuted the first pass's
version. Written down here 2026-08-16 by session `e4be1c4a`.

## The rung model (principle — also in awareness)

Rungs are position at ingestion: top / middle / bottom context.
Within a rung, emphasis is rhetoric; position beats rhetoric only
between rungs. Subagent returns enter at the bottom — information,
never instruction.

## Harness-particular findings

- **The top rung is harness property.** The harness process
  composes every agent's top from its built-in templates plus lent
  doors: definition files, system-prompt flags, config keys. No
  parent LLM outputs a child's top; spawn text enters the child at
  the middle rung. Owning the top means owning the invocation.
- **Skill bodies are harness-injected at the user rung.** In
  Claude, the flow itself can trigger the injection (the skill
  tool). In Codex, only pasted input can ($-named skills). A flow's
  own file-read of a skill enters at the bottom rung. Consequence
  (psyche-ruled): instructing flows how to read skills is useless —
  such instructions were deleted.
- **Rules are harness-relative.** A rule can be unsatisfiable in
  one harness and trivial in another. Before writing loading or
  tool rules, read the harness's own injected instructions, and
  delete rules the harness already carries.
- **Sibling flows cannot bind each other.** Files and intercom
  arrive at the bottom rung. Until the meta-harness exists, the
  psyche's typed middle input is the only authority route between
  live flows; middle authority does not travel — it reaches a
  worker only by launching in the repo or riding the authored
  dispatch.
- **Transcript recovery.** The raw transcript of a past session is
  recoverable from the harness session store by short id (first 8
  hex characters of the session UUID). A session pointer in notes
  can misremember; when a claimed enunciation is absent from the
  recovered transcript, that is a finding (enunciation without
  capture), not a retrieval failure.

## Sources

- `reports/HarnessRungMechanics-2026-08-16.md`, canonical legacy report
  source migrated by flow 01a02a06.
- Flows `6863ef19`, `ba906ae2`, `1030529c`, and `e4be1c4a`, as identified
  by the report's retained provenance.
