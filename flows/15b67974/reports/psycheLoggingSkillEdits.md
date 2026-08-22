# Psyche-logging skill edits — proposal set

Five proposals encoding the settled logging/distillation protocol. Exact
wordings for psyche green; open mechanics are left out, not drafted
around. Proposed cutover: the batch lands together through Curriculum, and
the landing is the cutover moment — raw logging switches to the flow
directories when these skills deploy.

## 1. psyche skill — "Where psyche lives" section

Replace the current three-item list with:

    - The spirit skill — Spirit lives there, not in a file.
    - `psyche/Intent/<topic>.md` — broad, few.
    - `psyche/Vision/<topic>.md` — distilled psyche: self-standing
      statements, each reviewed by the living psyche before it stands.
      Entries predating the flows protocol remain raw here until
      distillation touches them.
    - `flows/<short-id>/psyche/<topic>.md` — raw records, in the flow
      that heard them. Finding raw psyche means searching
      `flows/*/psyche/`.

## 2. psyche-interraction skill — Logging section, first paragraph

Replace "Log psyche rulings in `psyche/Vision/<topic>.md` by default.
Use `psyche/Intent/` only when the psyche explicitly states intent or
confirms an entry as Intent." with:

    Log psyche rulings in the flow's own `psyche/<topic>.md`.
    A statement enters `psyche/Vision/` only as a distillation the
    psyche has explicitly approved; `psyche/Intent/` only when the
    psyche states intent or confirms an entry as Intent.

Everything else in the section (verbatim quotes, log before acting, one
write per ruling, timestamps, reconstruction, titles) stands unchanged.

## 3. flows skill — directory anatomy

The layout block gains one line:

    flows/
      index.md
      <short-id>/
        log.md
        annotations.md
        psyche/<topic>.md
        witnesses/<subject>.md
        reports/<subject>.md

And beside the witness/report placement sentences:

    A psyche record goes in `psyche/<topic>.md`, the psyche's words
    verbatim.

## 4. New skill: psyche-distillation

Name follows the family (psyche-acquisition, psyche-interraction,
psyche-grasp). Description: "Psyche records across flows touch the same
topic and a self-standing articulation is owed. Requires: psyche."

Body, drafted from settled rulings only:

    Distillation re-articulates psyche records into self-standing
    statements. The model clarifies and purifies; the living psyche
    reviews every distilled statement explicitly before it stands.

    A distillation agglomerates records across flows that touch the
    same topic. Records are considered individually, never by file.
    One record may serve many distillations; one distillation may
    draw from many topics. When readings overlap or contradict, the
    more recent and the more certain statement is favored.

    A proposal re-articulates; it never quotes. The archived
    originals keep every original word.

    A distilled statement lands in `psyche/Vision/<topic>.md` on the
    psyche's explicit approval, and never before. The raw records it
    replaces move into an `archive-` prefixed file beside their
    source file.

    A record's id is its originating session's short id and that
    session's own count.

    Distillation is proposed on encounter or done in dedicated
    passes.

Left out because unruled: the reference-line format by which a distilled
statement names its archived originals (the 2026-08-14 `distills <id>
<id>` draft was called ambiguous and never resolved); where an
unpronounced proposal stages; non-primary-workspace flows' psyche home.

## 5. Retire the session-log skill

sessions/ is retired and the flows protocol carries the session log
(`log.md` per flow). The session-log skill still deploys beside flows,
naming a dead home. Proposal: delete the session-log authored source;
flows already holds the log rules.

## Sources

- psyche/Vision/psycheLogStructure.md — the whole trail: 2026-08-14
  corrections, many-to-many, archive, session-scoped ids (fb1008c0-1),
  ongoing distillation, chain of origin; 2026-08-22 rulings (raw in
  flows/*/psyche/, Vision = distilled home, archive- prefixed files,
  distillation defined).
- psyche/Vision/skillDesigning.md — style rules honored (no actor-style
  openings, no lines guarding imagined failures, no repetition across
  skills).
- Flows: 06196cc7, fb1008c0, 7c3f0c1d (prior draft rounds and their
  rebukes), 5c8be3ca (flows protocol), 15b67974 (this flow).
