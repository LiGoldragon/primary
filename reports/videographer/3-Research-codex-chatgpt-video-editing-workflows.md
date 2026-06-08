# Codex / ChatGPT video editing research

variant: Research
date: 2026-06-08
role: videographer

## Question

What public repositories, notes, and articles show useful ways to use
Codex or ChatGPT for video editing, and what should the videographer lane
borrow for local work?

## Summary

The useful pattern is not "ask a chatbot to edit an MP4." The useful
pattern is: make video editing inspectable as code, project state,
transcripts, timelines, frame samples, and deterministic render commands;
then let Codex or ChatGPT plan and modify those artifacts.

There are two distinct OpenAI product lanes:

- ChatGPT / Sora: useful for ideation, scripts, image generation, and
  Sora-native generated-video operations such as re-cut, remix, blend,
  loop, storyboard, and MP4 download. It is not the same thing as a
  local editor that cuts arbitrary footage.
- Codex: useful as an agent harness for local or repo-backed video
  tooling: Remotion projects, FFmpeg commands, caption scripts, MCP
  tools, generated timelines, and repeatable render pipelines.

For this workspace, the strongest direction is a local-first Codex
workflow around FFmpeg, ffprobe, transcripts, ASS captions, frame
inspection, and a reportable project manifest. Remotion is promising for
motion graphics and template-driven explainer videos, but the current
machine is not ready for it until Node is supplied through Nix or another
workspace-approved ephemeral path.

## Official OpenAI baseline

[OpenAI's Codex launch post](https://openai.com/index/introducing-codex/)
frames Codex as a cloud software engineering agent that can edit files,
run commands, run tests, commit changes in its environment, and cite
terminal logs and test outputs. That makes Codex a good fit for video
editing only when the editing workflow is exposed as files and commands.

[OpenAI's April 16, 2026 Codex update](https://openai.com/index/codex-for-almost-everything/)
expands Codex beyond pure coding: computer use, plugins, in-app browser,
image generation, memory, automations, and a named Remotion plugin are
all part of the public direction. The important implication is that
Codex is becoming a general work harness, but its reliable strength is
still structured tool use and inspectable artifacts.

[OpenAI's Sora help page](https://help.openai.com/en/articles/9957612)
documents Sora's video editor operations: re-cut trims and extends in a
storyboard, remix changes an existing generation, blend transitions
between videos, loop creates seamless loops, and generated videos can be
downloaded as MP4. That is useful for generated-video work, not for
cutting arbitrary local footage with deterministic provenance.

[OpenAI's ChatGPT image input FAQ](https://help.openai.com/articles/8400551-chatgpt-image-inputs-faq)
still says image inputs handle static images, not videos. That matters
because video understanding inside ChatGPT should not be assumed for
editorial work. When ChatGPT helps with video editing today, the robust
route is transcript, still frames, structured metadata, or tool-backed
execution.

## Source map

| Source | Type | What it shows | Videographer read |
|---|---|---|---|
| [remotion-dev/codex-plugin](https://github.com/remotion-dev/codex-plugin) | Repository | Official Remotion Codex plugin repo; small public repo with plugin assets and a Remotion skill. | Strong signal that Codex plus Remotion is a first-class direction, but the public README says it is internal and undocumented. Treat as promising, not turnkey. |
| [Remotion](https://www.remotion.dev/) | Tool docs | React-based programmatic video, reusable templates, props, preview, local/server/serverless MP4 rendering. | Best fit for motion graphics, launch videos, explainers, branded templates, and agent-editable video code. |
| [Skill Vault Remotion plugin page](https://skillvault.md/plugins/codex/remotion) | Plugin index | Lists `/plugins install remotion` and tags the plugin around video, React, animation, rendering, FFmpeg, captions, and audio. | Useful install signal, but secondary source. Prefer official repo and OpenAI update when making claims. |
| [Remotion in OpenAI Codex](https://www.mejba.me/blog/remotion-codex-motion-graphics-ai-video) | Field note / article | A practical Codex plus Remotion launch-video workflow: prompts generate Remotion code, preview runs locally, final H.264 render ships. | Good production narrative. Main lesson is to iterate with short scenes, frame-level feedback, and reusable project structure. |
| [ChatGPT Codex AI Video Editing](https://www.aifire.co/p/chatgpt-codex-ai-video-editing-prompt-instead-of-hours) | Article | Similar Codex plus Remotion motion-graphics workflow, with emphasis on prompts, reusable assets, and local previews. | Confirms the visible creator-market pattern: Codex edits code, Remotion renders video. |
| [FFMPerative](https://github.com/remyxai/FFMPerative) | Repository | Natural-language interface over FFmpeg-style operations: speed, resize, crop, flip, reverse, transcription, captions. | Early but directly aligned with "chat to compose video." Good conceptual reference for command synthesis and caption tasks. |
| [browser-use/video-use](https://github.com/browser-use/video-use) | Repository / skill | "Edit videos with coding agents"; supports Claude Code, Codex, and similar shell agents; uses transcripts, word timestamps, cut proposals, subtitles, color grading, self-evaluation, and project memory. | Very relevant. Borrow the artifact shape: packed transcript, project memory, helper scripts, final output folder, and agent-readable strategy. Be careful with ElevenLabs dependency and secrets. |
| [VibeFrame](https://github.com/vericontext/vibeframe) | Repository | Brief-to-MP4 workflow for coding agents. Uses STORYBOARD.md, DESIGN.md, generated assets, JSON output, dry runs, cost gates, machine-readable reports, and optional MCP. | Closest to this workspace's report-first style. Strong reference for project manifests, cost gates, dry-run builds, render inspection, and machine-readable outputs. |
| [AKMessi/vex](https://github.com/AKMessi/vex) and [Vex Reddit note](https://www.reddit.com/r/aiagents/comments/1tgep9g/vex_i_built_an_opensource_terminal_ai_video/) | Repository plus creator note | Terminal AI video editor using FFmpeg, MoviePy, Whisper, project state, timelines, undo/redo, export validation, subtitles, shorts, color grading, and local/OpenAI-compatible providers. | Strong mental model: the LLM plans; deterministic tools execute; project state owns truth. This is the right direction for real footage. |
| [poseljacob/agentic-video-editor](https://github.com/poseljacob/agentic-video-editor) | Repository | Multi-agent CLI: preprocess, director, trim refiner, editor, reviewer; Gemini plus FFmpeg; YAML pipelines; style templates; retries based on review scores. | Good architecture reference for agent roles and feedback loops, even though it is Gemini-centered rather than Codex-centered. |
| [vidmagik-agent](https://pypi.org/project/vidmagik-agent/) | Package | Full-stack AI video editor with MoviePy MCP backend exposing 60+ video/audio tools, highlight detection, vertical reframing, and multiple LLM providers including OpenAI-compatible APIs. | Relevant for MCP surface design. API-heavy, large, and dependency-rich; inspect before adopting. |
| [moviepy-mcp](https://github.com/vizionik25/moviepy-mcp) | Repository | FastAPI plus FastMCP server exposing MoviePy video/audio/compositing tools for agents. | Useful as a small MCP reference. Low project maturity, but the "agent calls explicit tools" shape is correct. |
| [ddominguez7/ai-video-generator](https://github.com/ddominguez7/ai-video-generator) | Repository | Automated short-form vertical generator using OpenAI Responses API, OpenAI TTS, Whisper, FFmpeg, Docker, subtitles, and publishing metadata. | Better for fully generated shorts than editing existing footage. Useful for output bundle structure. |
| [maxazure/video-editing-skill](https://github.com/maxazure/video-editing-skill) | Repository / agent skill | Codex/OpenClaw skill for talk/vlog editing: speech recognition, sentence splitting, subtitle burning, clip merging, many tests. | Useful skill-shaped reference. Platform assumptions lean macOS and Python package installs, so borrow concepts rather than install directly. |
| [ELLMPEG paper](https://arxiv.org/abs/2602.00028) | Research paper | Tool-aware RAG plus self-reflection to generate and locally verify FFmpeg and VVenC commands at the edge. | Supports the same principle: constrain LLMs with tool docs, local execution, and verification, not free-form command guessing. |
| [Kapwing article on ChatGPT video editing](https://www.kapwing.com/resources/how-to-use-chatgpt-to-edit-videos/) | Article | ChatGPT alone does not reliably edit videos directly; it can help generate FFmpeg instructions, scripts, translations, B-roll suggestions, and effect ideas. | Older article, but still matches the current safe operating model: ChatGPT as collaborator, not renderer. |

## Patterns that repeat

### Video becomes code

Remotion is the clearest example: scenes are React components, timing is
frame math, outputs are renders. Codex can edit this because it looks
like a normal codebase. The Codex agent can run preview/render commands,
read errors, edit imports, and preserve a Git history.

This is strongest for:

- product launch videos
- motion graphics
- technical explainers
- kinetic typography
- charts and UI demos
- reusable branded templates

It is weaker for:

- long-form documentary taste
- messy narrative restructuring
- work where the key judgment is "which emotional beat lands"
- footage with poor audio, bad continuity, or weak coverage

### Video becomes a transcript plus timecode

The most practical editing systems do not ask the model to "watch" the
whole video. They transcribe audio, pack word-level timestamps into a
small text artifact, expose silence and phrase boundaries, and let the
agent cut on those boundaries. This appears in video-use, Vex,
FFMPerative, and the short-form generator repositories.

This is the right path for captions, filler-word removal, dead-air cuts,
quote extraction, vertical shorts, and word-synchronized overlays.

### Video becomes project state

The stronger tools keep source footage immutable and store edit decisions
as project state: manifests, timelines, operations, review reports,
render outputs, and undoable histories. The weaker tools generate one
FFmpeg command and hope the prompt history remains enough.

The local videographer lane should prefer:

- `project.md` or `project.nota` for human intent and current plan
- `sources/` for immutable input media
- `transcripts/` for word-level transcript artifacts
- `timeline/` for edit operations
- `renders/` for outputs
- `inspection/` for contact sheets, sampled frames, ffprobe JSON, and
  quality notes

### Deterministic tools execute the edit

The repeated stack is FFmpeg, ffprobe, MoviePy or Remotion, Whisper or
another ASR engine, optional image generation, and optional MCP. The LLM
should choose and revise operations, but rendering should be handled by
boring deterministic tooling with logged commands and artifacts.

### Review loops matter

The better examples explicitly inspect outputs: render selected frames,
generate contact sheets, review cut boundaries, score quality, or loop
reviewer feedback into the next edit pass. This is the difference
between one-shot command generation and an editing workflow.

## Local implications

The videographer lane already has a usable FFmpeg base: FFmpeg/ffprobe
with libass and VAAPI are present, and `wf-recorder` is available for
Wayland capture. Missing pieces from the previous readiness report are
still load-bearing: word-level transcription, TTS, and display fonts.

One new local constraint surfaced during this research: the official
Codex manual helper could not run because `node` is missing in this
environment. That also means Remotion and many Codex plugin workflows
are not ready to run locally without a Nix-provided Node toolchain.

Do not install the researched projects blindly. Several assume `pip`,
`uv`, Homebrew, persistent skill symlinks, cloud APIs, or third-party API
keys. In this workspace, those choices pass through the existing
discipline: ephemeral tooling where possible, secrets never exposed to
agents, and reports or manifests for durable state.

## Recommendation

Build the videographer lane around a small local "video project" shape
before adopting a large external tool:

1. A deterministic FFmpeg/ffprobe inspection and render loop.
2. A transcript artifact format with word-level timestamps.
3. An ASS caption generation script with local style presets.
4. A project manifest that records sources, edit decisions, commands,
   renders, and inspection notes.
5. Contact-sheet and sampled-frame review commands so Codex can inspect
   visual outputs without relying on memory.
6. A Remotion path only after Node is available through Nix and the
   first FFmpeg/caption workflow is solid.

The first borrowed idea should be from Vex and video-use: the LLM is the
planner, deterministic tools are the editor, and project state is the
truth. The second borrowed idea should be from VibeFrame: make every
agent-facing step emit JSON or a compact report so future sessions can
continue without relying on chat memory.

## Sources read

- OpenAI, [Introducing Codex](https://openai.com/index/introducing-codex/), accessed 2026-06-08.
- OpenAI, [Codex for almost everything](https://openai.com/index/codex-for-almost-everything/), accessed 2026-06-08.
- OpenAI Help Center, [Generating videos on Sora](https://help.openai.com/en/articles/9957612), accessed 2026-06-08.
- OpenAI Help Center, [ChatGPT Image Inputs FAQ](https://help.openai.com/articles/8400551-chatgpt-image-inputs-faq), accessed 2026-06-08.
- Remotion, [Make videos programmatically](https://www.remotion.dev/), accessed 2026-06-08.
- Remotion, [remotion-dev/codex-plugin](https://github.com/remotion-dev/codex-plugin), accessed 2026-06-08.
- Skill Vault, [Remotion Codex plugin](https://skillvault.md/plugins/codex/remotion), accessed 2026-06-08.
- Engr Mejba Ahmed, [Remotion in OpenAI Codex: Prompt-Based Motion Graphics](https://www.mejba.me/blog/remotion-codex-motion-graphics-ai-video), accessed 2026-06-08.
- AI Fire, [ChatGPT Codex AI Video Editing: Prompt Instead of Hours](https://www.aifire.co/p/chatgpt-codex-ai-video-editing-prompt-instead-of-hours), accessed 2026-06-08.
- remyxai, [FFMPerative](https://github.com/remyxai/FFMPerative), accessed 2026-06-08.
- browser-use, [video-use](https://github.com/browser-use/video-use), accessed 2026-06-08.
- vericontext, [VibeFrame](https://github.com/vericontext/vibeframe), accessed 2026-06-08.
- AKMessi, [Vex](https://github.com/AKMessi/vex), accessed 2026-06-08.
- Reddit r/aiagents, [Vex open-source terminal AI video editor note](https://www.reddit.com/r/aiagents/comments/1tgep9g/vex_i_built_an_opensource_terminal_ai_video/), accessed 2026-06-08.
- poseljacob, [agentic-video-editor](https://github.com/poseljacob/agentic-video-editor), accessed 2026-06-08.
- PyPI, [vidmagik-agent](https://pypi.org/project/vidmagik-agent/), accessed 2026-06-08.
- vizionik25, [moviepy-mcp](https://github.com/vizionik25/moviepy-mcp), accessed 2026-06-08.
- ddominguez7, [ai-video-generator](https://github.com/ddominguez7/ai-video-generator), accessed 2026-06-08.
- maxazure, [video-editing-skill](https://github.com/maxazure/video-editing-skill), accessed 2026-06-08.
- arXiv, [ELLMPEG: An Edge-based Agentic LLM Video Processing Tool](https://arxiv.org/abs/2602.00028), accessed 2026-06-08.
- Kapwing, [How to Use ChatGPT to Edit Videos](https://www.kapwing.com/resources/how-to-use-chatgpt-to-edit-videos/), accessed 2026-06-08.
