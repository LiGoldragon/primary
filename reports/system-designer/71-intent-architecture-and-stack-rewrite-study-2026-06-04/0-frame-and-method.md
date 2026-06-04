# 71 — Intent architecture + stack rewrite study (frame + method)

Kind: meta-report directory (frame + research sub-agents + orchestrator synthesis).
Topics: spirit, record-shape, intent-maintenance, agglomeration, composite, weight, archive, lojix, horizon, schema, triad-engine, rewrite.
Date: 2026-06-04.
Role: system-designer (orchestrator).

## Psyche directive

A single voice-prompt carrying two intertwined asks:

1. **Get deeply familiar with the stack rewrite.** The lojix
   ("Logics") rewrite and the horizon-rs rewrite, plus the new
   architectural happenings — schema and the triad engine — which are
   "moving fast but starting to stabilize." The psyche wants lojix to
   be built on that substrate. horizon-rs "is still just a hack" and
   does not have the regular component shape.

2. **Redesign the Spirit intent architecture, and implement it for real
   on a feature branch** (designer produces the real implementation;
   operator later does the production implementation). The redesign has
   four coupled moves, three of which were already captured at High and
   are reinforced today, one of which is new today:
   - **Composite / repurposed intent** (already `(Spirit Principle
     audg3)`): Spirit records that reference older records as source
     material, agglomerating repeated/related intent into a newer
     stronger record without losing provenance.
   - **Agglomeration by the certainty ladder** (already `(Spirit
     Principle 1zd6)`): combine many lower-certainty records on one
     subject into a single fresh higher-certainty record; the old ones
     retire under explicit supersession. The psyche notes this is "a
     bit dangerous" (auto-removal of sources).
   - **Weight distinct from certainty** (already `(Spirit Principle
     6vsl)`): records carry both certainty (confidence) and weight
     (accumulated importance / reinforcement); weight compounds on top
     of certainty; a composite has higher weight because it is composed
     of many sources.
   - **Per-kind field sets** (NEW today, `(Spirit Decision 3awz)`):
     record fields vary by kind — a private-bearing record carries a
     privacy field, an ordinary public record omits it — eliminating
     the fields a kind does not use and shrinking the total field count.
     "This is a way better architecture."
   - **Streamlined archive** (`(Spirit Principle 73t3)`): agglomeration's
     retired sources are archived and referenced by hash from the
     composite; the archive mechanism needs streamlining to carry that
     composite→archived-source provenance cleanly.

The psyche also wants the `skills/intent-maintenance.md` skill edited so
that "once enough very similar intents are found, they are replaced by a
newer intent" — a manifestation of the already-captured agglomeration
intent, to be done after the design settles.

## Intent anchors

[Spirit should support composite intent records that reference older intent records as source material, so repeated or closely related intent can be agglomerated into a newer stronger record without losing provenance.] (Spirit Principle audg3)

[Intent should be refreshed by agglomeration: combine many lower-certainty records that belong together into a single fresh higher-certainty record that fuses their ideas; older agglomerated records retire under the explicit-supersession discipline.] (Spirit Principle 1zd6)

[Spirit records should distinguish certainty from weight: certainty is confidence in the statement, while weight is accumulated importance or reinforcement, especially for composite records derived from multiple source records.] (Spirit Principle 6vsl)

[Spirit record fields should vary by record kind rather than every record carrying every field — a private-bearing record carries a privacy field while an ordinary public record omits it; reduces total field count and gives each kind a tighter purpose-fit shape.] (Spirit Decision 3awz)

[lojix should be built on the triad engine and schema substrate now that those are stabilizing, the same schema-derived component shape the other components are converging on, rather than remaining a hand-written hack.] (Spirit Decision 4sff)

[horizon-rs is currently a hack and does not have the regular component-triad shape.] (Spirit Clarification 4v45)

[Do work properly or not at all — no half-assed slop, no underspecified or wrong-shaped dispatch that produces garbage.] (Spirit Correction 157dwrve, this session's standing constraint)

## Method

Three read-only research sub-agents, each writing one numbered report
into this directory and returning structured findings. The orchestrator
then writes the synthesis as the highest-numbered file, and — only after
the design is concrete — produces the real feature-branch implementation
(separately, carefully; NOT a blind dispatch).

| File | Angle |
|---|---|
| `1-stack-rewrite-study.md` | The lojix + horizon-rs rewrite and the schema + triad-engine substrate. Current state of each, what is stabilizing, how lojix should adopt the triad engine + schema, what "horizon is a hack" means concretely. |
| `2-intent-corpus-agglomeration-study.md` | Research the Spirit intent corpus (intent-maintenance, spirit, record-shape, schema, agglomeration, weight, composite, lojix, horizon). Find clusters of repeated/similar intent that are agglomeration candidates; PROPOSE concrete composite records that would replace each cluster (do not execute any removal). A live demonstration of the agglomeration concept. |
| `3-spirit-record-architecture-redesign.md` | The Spirit record-schema redesign: per-kind field sets (variant records), a composite intent kind referencing source hashes, weight compounding on certainty, streamlined archive. Read the deployed signal-persona-spirit contract + persona-spirit store + the schema-derived spirit pilot; produce a concrete schema-language + Rust design ready to implement on a feature branch. |

## Discipline for the research agents

- **Read-only.** Write ONE numbered report into this directory. Do not
  edit source, do not commit, do not run `spirit "(Remove …)"` or any
  mutating Spirit operation. Agglomeration candidates are PROPOSED, not
  executed.
- Verify every line number and type name against current source before
  citing. Honesty about state over fidelity to brief.
- Cite intent as bracket-quoted summaries with the short hash code.
- NOTA discipline if quoting NOTA: bracket-form strings only, positional
  records, no quotation marks.
- Spirit is deployed at **v0.5.0** (hash identity is live; the
  `skills/spirit-cli.md` examples document 0.4.2 — read the deployed
  `signal-persona-spirit` source for the current wire shape, do not infer
  from the skill).

## Lane coordination

This is the designer-side study + design. The real feature-branch
implementation is the designer mockup-on-worktree method; production
implementation is the operator's. No removal of any Spirit record is
executed by this session — the agglomeration demonstration only
proposes. The standing constraint `(Spirit Correction 157dwrve)` governs:
the implementation step happens only once the design is concrete, and is
never a blind/underspecified dispatch.
