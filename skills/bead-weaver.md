# Skill — bead-weaver

## Starting Gate

Use this skill after the intent is already aligned enough to decompose into
work. If the prompt is still deciding what should exist, write the design report
or ask the psyche; do not file speculative beads to force shape.

Before filing a weave, load the local skills that govern the surface you are
about to touch:

- `skills/beads.md` for BEADS lifecycle and close notes.
- `skills/reporting.md` when the weave depends on a design report.
- `skills/intent-log.md` and `skills/spirit-cli.md` when new durable psyche
  intent appears while weaving.
- `skills/architecture-editor.md` when the weave depends on an architecture
  claim that is not yet in the owning `ARCHITECTURE.md`.
- `skills/nota-design.md` when a bead asks for a new NOTA record or schema.

If the aligned prompt names a source report, architecture file, or Spirit
record, read that source. If it names only chat context, first write the missing
report or update the durable guidance file; a bead graph should not depend on
vanishing harness memory.

## Shape the Graph

A bead weave is a dependency graph of discrete jobs. Each bead must have a
definition of done and a natural close note. Do not file beads for permanent
disciplines, broad concerns, or unresolved design questions; land those in a
skill, architecture file, intent file, or report.

Build the graph from outcomes backward:

1. Name the final observable outcome.
2. Name the smallest proof that shows the outcome works.
3. Name each prerequisite that can ship independently.
4. Put architecture/schema/report updates before implementation beads when
   implementation would otherwise guess.
5. Put verification beads after the build beads they witness.

Prefer a thin first slice over a wide backlog. A good first weave exposes
unknowns through working failure: one scaffold, one adapter path, one proof
domain, one closeable verification surface.

## Bead Description Template

Every bead in the weave carries enough context for a clean session to start
without reading chat:

```text
Source: <report path, architecture path, Spirit record summary, or prompt
summary>

Goal: <one concrete outcome>

Done when:
- <observable completion criterion>
- <test, witness, or review signal>

Required reads:
- <skills or architecture files>

Constraints:
- <hard boundaries, privacy, sandboxing, model limits, no-primary rules>

Out of scope:
- <nearby work this bead must not absorb>
```

Use the source summary as prose, not a bare identifier. A Spirit record code or
report path is a locator after the meaning is stated.

## Filing Mechanics

Create each bead with a descriptive title, then wire dependencies explicitly:

```sh
bd create "<title>" -t task -p <priority> -d "<description>"
bd dep <blocker-bead> --blocks <blocked-bead>
```

For a graph, file blocker beads first so the dependency commands read in the
same direction as the work. After filing, read the graph back with `bd show` or
`bd list --status open` and fix unclear descriptions immediately.

Do not claim `.beads/`. If you begin working a bead after filing it, claim the
task through orchestrate with `(Task <bead-id>)`; filing alone is not a claim.

## Handoff Shape

When handing a weave to the psyche or another agent, lead with the work, not the
ids:

- the final outcome;
- the first unblocked bead by title and what it proves;
- any blocked beads and the blocker relationship;
- the source report or architecture path;
- the bead ids only as trailing locators.

Never return a list of bare bead ids as the useful answer.

## Mentci Prompt-to-Weave Slice

For the Mentci prompt-to-bead-weave slice, the first weave is harness-agnostic
and proves only the thin path:

- A prompt enters Mentci.
- A cheap contained API preflight model emits fixed-schema NOTA that loads the
  right skills and creates a minimal scaffold plus `skills/skills.nota`.
- Mentci opens a persistent named, addressable harness session through the
  terminal-cell driver.
- The terminal-cell driver owns process liveness, send/read, idle timeout,
  close signal, and stalled-output detection.
- `orchestrate` lanes own naming, addressing, lane metadata, and session
  lookup.
- The first proof runs on a sandboxed jj task, never on primary.

The first Mentci weave should not file cache/reuse mechanics, savings metrics,
or broad harness parity as first-class jobs. Those become beads only after the
thin slice exposes the real failure modes.

## See also

- `skills/beads.md`
- `skills/reporting.md`
- `skills/nota-design.md`
