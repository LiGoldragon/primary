# transcriptAsNexus

## 2026-09-16 — the transcript component is misimplemented; make it a nexus, with datom-syntax CLIs

Context: while refining the anchor-extract flowchart (`flows/48cff7/notion/narratedExtractor.md`), the living named the transcript component as misimplemented and set the remedy in one line.

> The transcript component is misimplemented. We need to make a nexus out of it and use datom syntax with the CLIs.

-- psyche, typed.

Prior anchors this refines, not replaces:

- The transcript tool's own README already flags itself as "CLI shim … temporary, pending a Nexus" (`/git/github.com/LiGoldragon/transcript/README.md`). This is the living cashing in that IOU.
- `flows/692df8/vision/messages.md` (2026-09-15) — the JSON provenance header from `tools/prompt-relay` was rejected as ugly; datom syntax replaces it "everywhere: all the CLIs, everything." The transcript CLI is the concrete next site.

Flow reading, not the living's words: current `transcript show / search / raw` are plain positional/argparse CLIs with rendered text output. Moving to a nexus means the long-running Nexus shape (privileged and ordinary sockets, binary signal contracts) taking over the transcript's job; the CLIs become datom-syntax clients speaking to it. The anchor-extract subcommand proposed in `notion/narratedExtractor.md` should be designed against that nexus, not appended to the current shim.
