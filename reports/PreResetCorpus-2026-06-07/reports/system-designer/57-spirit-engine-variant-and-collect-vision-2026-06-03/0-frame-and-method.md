# 57 — Spirit engine variant-and-collect vision (frame)

Kind: meta-report directory (frame + operator vision + designer psyche analysis + overview).
Topics: spirit, variants, collect, defaults, vision, psyche-analysis.
Date: 2026-06-03.
Role: system-designer (orchestrator).

## Psyche directive

The psyche directed today's session at the variant-ladder and
defaults direction with four specific new Spirit operations to add:

[Spirit gains an explicit CollectRemovalCandidates operation as a
Signal root. It collects all records currently at Zero certainty
and emits their summary form to a configurable output target.
Separates the discovery / extraction concern from the destruction
concern in Remove.] (Decision High, today)

[Operations that extract or emit content from Spirit accept a
customizable output-target enum as the final field in the request
shape. Variants include Stdout, Stderr, and File with a path
payload. Not an error channel — Stderr is one option among normal
outputs. Keeps the wire interface uniform across extraction
operations.] (Decision High, today)

[Spirit defines a small-record data type carrying the core
load-bearing fields — identifier, topics, kind, description summary,
magnitude, daemon-stamped date and time. The variant-ladder short
forms and CollectRemovalCandidates emit the small record; archiving
tools consume it. Reduces wire weight; matches the natural reading
shape an agent or human wants.] (Decision High, today)

[Spirit gains a RecordDefault short-form recording operation taking
only fields agents commonly customize — topics, kind, description,
magnitude — with defaults injected for the rest (privacy at Zero per
the dev-mode public-repo grounding, daemon-stamped date and time,
plus any other rarely-customized field). Record remains the
canonical full-fidelity operation.] (Decision High, today)

These are records 1547-1550, captured at the start of this session.
They sit downstream of the variant-ladder direction landed earlier
([Spirit operations should support a simpler-to-more-complex variant
ladder — short forms with summary defaults for normal operations,
complex forms with full metadata for custom operations.], Decision
High, today, record 1474).

## What this directory holds

The psyche asked for two perspectives, both produced via sub-agents,
with operator's vision first and designer's psyche-analysis following
once operator has surfaced their view.

### 1-operator-vision.md (sub-agent — first)

A vision-shape meta-report from the operator perspective. What to
build, in what sequence, with what dependencies, and what concrete
code shape each operation lands as. Reads recent operator and
system-operator reports for the deployment + implementation context;
references the prior audits at
`reports/system-designer/53-spirit-next-production-parity-2026-06-02/`,
`reports/system-operator/182-spirit-privacy-and-shorthand-interface-audit-2026-06-02.md`,
`reports/system-designer/55-spirit-variant-ladder-design-research-2026-06-02.md`,
and `reports/system-designer/56-psyche-meta-report-spirit-recent-work-2026-06-03.md`.

### 2-designer-psyche-analysis.md (sub-agent — second)

A psyche-analysis report that reads the operator's vision and the
current code, then writes the situation-on-the-ground in narrative
voice with verbatim code excerpts, mermaid where it helps, and a
clear list of open decisions for the psyche to ratify, alter, or
suggest. Inherits the discipline at
`/home/li/primary/skills/reporting.md` §"Psyche reports — show the
code, not the summary", §"Psyche reports talk to a human", and
§"Decisions in Psyche reports — distinguish lean from ratification".
Cites intent records per
`/home/li/primary/skills/intent-log.md` §"Citing intent in prose —
bracket-quote the summary" — bracket-quoted description summaries,
not bare numbers.

### 3-overview.md (orchestrator synthesis)

Brief overview tying the two perspectives together with the
prioritised path-to-ship and the questions the psyche needs to
engage with.

## Lane coordination

Per the existing lane discipline at
`/home/li/primary/skills/role-lanes.md`, reports under
`reports/system-designer/` are this lane's. The operator-perspective
report INSIDE this directory is dispatched as a sub-agent inheriting
the system-designer lane (per Spirit 920 inheritance rule), written
from the operator's analytic standpoint. The actual operator agent
in their own lane may produce a parallel report under
`reports/operator/` separately; this directory does not claim to be
the canonical operator vision — it is the designer-side view of what
operator vision would be.

## Sub-agent sequencing

Operator-vision sub-agent dispatches first. Designer-psyche-analysis
sub-agent dispatches after operator-vision lands, so it can integrate
operator's framing rather than guess it.
