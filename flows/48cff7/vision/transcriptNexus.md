# transcriptNexus

## 2026-09-16 — the transcript component is misimplemented; make it a nexus, with datom-syntax CLIs

Context: while refining the anchor-extract flowchart, the living named the transcript component as misimplemented and set the remedy in one line.

> The transcript component is misimplemented. We need to make a nexus out of it and use datom syntax with the CLIs.

-- psyche, typed.

Prior anchors this refines, not replaces:

- The transcript tool's own README already flags itself as "CLI shim … temporary, pending a Nexus" (`/git/github.com/LiGoldragon/transcript/README.md`). The living is cashing in that IOU.
- `flows/692df8/vision/messages.md` (2026-09-15) — the JSON provenance header from `tools/prompt-relay` was rejected as ugly; datom syntax replaces it "everywhere: all the CLIs, everything." The transcript CLI is the concrete next site.

## 2026-09-16 — it needs to be a nexus with Signal and datom syntax only

Context: after the earlier draft was still framing the anchor extract as a fourth argparse subcommand of the shim, and after the living asked whether the skills were bad, the flow loaded the `nexus` and `datom` skills and the shape of the transcript-nexus became explicit.

> It needs to be a nexus with Signal and Datom syntax only.

-- psyche, typed.

Flow reading, not the living's words: the transcript-nexus takes on the shape every Nexus has. Two sockets — ordinary and meta. Its own sema store. Speaks only Signal (rkyv, framed) on the wire. Two wire type repos, in Ethos: `signal-transcript` for the public vocabulary and `meta-signal-transcript` for configuration. Two thin CLIs — `transcript` and `transcript-meta` — each taking exactly one inline datom argument. No flags anywhere. Flag arguments are rejected by design.

## 2026-09-16 — make the transcript tool so the main flow can use it to make the report

Context: after the transcript-nexus shape was settled, the living set the next step.

> Okay, let's make this tool, this transcript tool, so that you can use it to make the report. We're then going to start looking at the anatomy of stuff, and I'm going to correct it. Based on your visual, it is going to be made by a subflow that will be able to know exactly where to get it using the transcript. You're just going to give it the information it needs to know which block in the transcript should be turned into a visual.
>
> It needs the flowchart. It needs the anatomy, right? The anatomy and ethos. We could almost say we're going to create charts out of ethos eventually. The one who renders it makes nice SVGs so we can see the whole graph, because so many Mermaid graphs don't render. I don't even know if it's the best way to represent charts, but it seems to be the standard. All harnesses work with Markdown, right?

-- psyche, typed.

Flow reading, not the living's words: the report is authored by the main flow in Markdown, which every harness handles. The visual for a chart is produced by a **visualization subflow**, dispatched with just the pointer it needs — session_ref, BEG anchor, END anchor — and the anatomy and ethos of what should be drawn. It uses the transcript nexus to fetch the block (the flowchart in the main flow's reply, or wherever the chart's specification lives) and produces the SVG.

Mermaid is the interim notation the main flow can inline into its reply because Markdown viewers of some kinds render it; but the terminal shape is charts specified in ethos and rendered by the visualization subflow to SVG we own, so the graph is guaranteed to render everywhere. "Charts out of ethos" is the direction: the ethos-typed chart is the falsifiable spec; the SVG is a projection.
