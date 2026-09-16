# proposal · presentation-flow

*Flow 48cff7 · 2026-09-16 · pending living review*
*Kind: new skill*
*Source records: flows/48cff7/vision/presentationFlow.md, pocShapeConfirmed.md, transcriptNexus.md (visualization subflow input shape)*

---

## description

Producing an artifact for the living — a slide deck, a chart-heavy report, a mockup — where a main flow authors the content and delegates rendering.

## body

A presentation flow is a main flow, low-power by default. It writes the report in Markdown and dispatches visualization subflows for figures.

Each visualization subflow receives, as one inline datom: a pointer to the source block (via `transcript-nexus Block`), the anatomy of the chart, its ethos, and one sentence of intent.

Do not embed figure content inline in the subflow's prompt when a transcript pointer will do.

The final artifact is one deliverable, published private, and referenced by URL in the flow's report.
