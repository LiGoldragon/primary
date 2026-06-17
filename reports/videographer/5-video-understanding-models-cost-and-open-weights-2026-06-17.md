# Video understanding models, cost, and open weights

variant: Research
date: 2026-06-17
role: videographer

## Question

Are there models that can actually watch video, rather than only using
`ffprobe` or FFmpeg to sample still images every few seconds? Which
models are best for cost if the workflow needs video understanding, and
how does the open-weight world compare?

## Short answer

Yes, but "watch video" has layers.

The practical production distinction is:

- Frame-sampling harness: our code extracts frames with FFmpeg/ffprobe,
  transcribes audio, and sends frames plus text to an image-capable LLM.
- Native video API: the provider accepts a video file or video URL, then
  tokenizes sampled frames, audio, and timestamps internally.
- Research/native temporal model: the model architecture is trained for
  video and temporal reasoning, sometimes with absolute time encoding or
  video-specific position encodings.

Even native video APIs usually do not ingest every source frame. Google's
Gemini video API is explicit: File API video processing defaults to 1
frame per second plus audio; at default media resolution, video is about
300 tokens per second, or about 100 tokens per second at low media
resolution. That is still materially better than ad hoc screenshots,
because the API owns timestamping, multimodal packing, and long-context
handling.

For this workspace, the best route is:

1. Use local FFmpeg/ffprobe, `scenedetect`, and `faster-whisper` for the
   first pass.
2. Use Gemini 2.5 Flash-Lite or Gemini 2.5 Flash when true video
   question-answering is useful.
3. Escalate to Gemini Pro only for hard temporal reasoning or high-value
   reviews.
4. Treat Qwen as the main open-weight/open-model challenger. Qwen3.5
   Flash/Plus and cheap Qwen2.5-VL hosting are more competitive than the
   first pass implied, especially if we use a hosted API before taking on
   local GPU serving.

## What "watching video" means technically

The user intuition is right: many workflows use FFmpeg or ffprobe-like
inspection to sample frames, then ask a vision model to analyze those
still images. This is not fake; it is the dominant practical pattern.
But it has weaknesses:

- It can miss fast events between sampled frames.
- It often loses motion cues.
- Audio/transcript alignment is manually assembled.
- Long videos can exceed context if too many frames are included.
- Cost grows with frame count.

Native video APIs improve this by taking the video input directly and
handling the sampling/tokenization pipeline themselves. They still
compress the video. Gemini's public docs say videos are stored at 1 FPS
through the File API, audio is processed at 1 Kbps single-channel, and
timestamps are added every second. Gemini also lets callers override the
1 FPS sampling rate and choose media resolution.

Open-weight video-language models add a third category. Qwen2.5-VL, for
example, claims long-video comprehension over an hour and second-level
event localization through dynamic resolution and absolute time
encoding. Qwen2.5-Omni and Qwen3-Omni describe text, audio, image, and
video understanding in end-to-end multimodal systems. InternVL3.5 claims
leading open-source multimodal performance and evaluates video
understanding across Video-MME, MVBench, MMBench-Video, MLVU, and
LongVideoBench.

But open-weight does not automatically mean plug-and-play video in our
harness. Serving, GPU memory, quantization, video preprocessing, context
limits, and API compatibility become our problem unless we use a hosted
provider.

## Current provider picture

### Gemini

Gemini is the strongest current production answer for native video
understanding.

Official docs say all Gemini models can process video data. Models with
a 1M context window can process roughly 1 hour at default media
resolution or 3 hours at low media resolution. The File API default is 1
FPS plus audio and timestamps; tokenization is about 258 tokens per
sampled frame at default resolution, 66 tokens per frame at low
resolution, plus 32 audio tokens per second.

Cost at video scale is unusually favorable. Approximate input-only cost
for 1 hour of video:

- Gemini 2.5 Flash-Lite standard: about 1.08M video tokens at default
  resolution, roughly $0.108 input; low resolution about $0.036.
- Gemini 2.5 Flash standard: about $0.324 input at default resolution;
  low resolution about $0.108.
- Gemini 2.5 Pro is much more expensive for hour-scale video, because
  long prompts cross the pricing breakpoint. At default resolution, an
  hour is roughly 1.08M input tokens; at the >200K tier this is about
  $2.70 input. Low resolution is roughly 360K tokens, about $0.90 input.

Output tokens add cost, but video analysis outputs are normally small
compared with the input. A few thousand output tokens are usually cents
or fractions of a cent on Flash-Lite/Flash and more noticeable on Pro.

### OpenAI

OpenAI's API is strong for image understanding, coding, agent harnesses,
and local tool use, but the public API documentation still describes
Responses as supporting text and image inputs, not native video files.
The current OpenAI model page says latest models support text and image
input, text output, multilingual capabilities, and vision. The Images and
Vision guide covers image input analysis and image generation/editing.

For our Codex harness, that means OpenAI is still best used as:

- Codex reasoning over project files and scripts.
- Image/frame review after we sample frames or contact sheets.
- Transcript/timeline planning.
- Tool-driven editing with FFmpeg, Remotion, and scripts.

OpenAI cost for frame-based video review can be controlled, but it is
not as clean as Gemini's video-token accounting. GPT-5.5 is $5/M input
and $30/M output; GPT-5.4 mini is $0.75/M input and $4.50/M output.
Using GPT-5.4 mini on selected frames is plausible; using GPT-5.5 on
large frame sets should be reserved for high-value editorial judgment.

### Claude

Claude's public API vision guide is image-oriented. It documents image
upload through Claude chat, Console Workbench, and API request. I did not
find official Anthropic API documentation for native video-file
understanding comparable to Gemini's video guide.

Claude-style video workflows therefore look similar to OpenAI-style
video workflows: extract frames, transcribe audio, pass images and
timestamped text to the model, and let the coding agent write or revise
tools.

### Qwen / Alibaba

Qwen is the most interesting open-weight video family for our use case.
The Qwen2.5-VL blog says the model can comprehend videos over 1 hour and
pinpoint relevant video segments. The Qwen2.5-VL technical report
attributes this to dynamic resolution processing and absolute time
encoding, with second-level event localization. Qwen2.5-Omni and
Qwen3-Omni expand the direction into end-to-end multimodal systems that
include text, audio, images, video, and speech.

Cost depends on how it is served:

- Alibaba Model Studio lists Qwen2.5-VL-72B-Instruct around $2.80/M
  input and $8.40/M output in one region/deployment table, with cheaper
  7B and 3B variants.
- The same documentation lists newer Qwen-VL-Plus and Max variants with
  much lower regional/global prices in some tables, including
  Qwen-VL-Plus around $0.21/M input and $0.63/M output in one table and
  lower global figures in another.
- OpenRouter currently lists Qwen2.5-VL-72B-Instruct at $0.80/M input
  and $1/M output, with 131K context.
- CloudPrice's provider comparison for Qwen2.5-VL-72B shows that hosted
  price can be much lower than Alibaba's direct list price: it lists
  Nebius at $0.13/M input and $0.40/M output, Fireworks around
  $0.90/M input and output, Novita at $0.80/M input and output, and
  OpenRouter at $0.80/M input and $1/M output.
- OpenRouter lists Qwen3.5 Flash at $0.065/M input and $0.26/M output
  with 1M context and text/image/video input. That is extremely
  competitive for a hosted multimodal model if quality is sufficient.
- OpenRouter lists Qwen3.5 Plus at $0.30/M input and $1.80/M output,
  also with 1M context and text/image/video input. This is less cheap
  than Flash but still competitive against premium closed models.

The price spread is large because "open-weight" can mean official API,
third-party serverless inference, dedicated endpoint, or local GPU. The
model family is attractive, but the exact provider path must be tested
with our actual video payload format.

This corrects the practical recommendation: Qwen should not be treated
only as a later curiosity. It is the most plausible low-cost competitor
to Gemini for the native-video slot. Gemini still has the cleanest
official video-token documentation, but Qwen3.5 Flash/Plus deserve an
early hosted bakeoff because their listed prices are in the same cost
class or cheaper, depending on how video is metered by the provider.

### InternVL and other open models

InternVL3.5 is a strong open-source family. Its paper claims leading
open-source multimodal performance and reports video understanding tests
across Video-MME, MVBench, MMBench-Video, MLVU, and LongVideoBench. The
paper evaluates video with 16, 32, 48, and 64 frame settings for several
benchmarks, which is a reminder that many open video evals are still
multi-frame reasoning, not full continuous video ingestion.

VideoLLaMA3, LLaVA-Video, Hour-LLaVA, and related projects are relevant
research references, but they are not the first practical path for this
workspace unless we want to own model-serving complexity.

## Cost model for our workflow

There are three realistic cost modes.

### Cheap deterministic mode

Use no video-understanding API:

- `ffprobe` metadata
- `scenedetect` shot boundaries
- `faster-whisper` transcript and word timestamps
- local contact sheets
- Codex reasoning over text, frame filenames, and selected stills

This should be the default for edits, captions, trims, shorts
extraction, render recipes, and platform packaging. It is cheap because
models see compact artifacts, not the whole video.

### Cheap native-video mode

Use Gemini 2.5 Flash-Lite or Flash on short clips or selected segments:

- Flash-Lite low resolution is roughly 3.6 cents per hour of input video
  before output tokens.
- Flash default resolution is roughly 32 cents per hour of input video.
- This is cheap enough for batch review of segments, rough summaries,
  and "what happens around this timestamp?" questions.

The catch is quality. Low resolution may miss small text, subtle
gestures, UI details, or composition flaws. Use it for coarse review,
not final quality control.

### Expensive judgment mode

Use Gemini Pro, GPT-5.5 on selected frames, or a strong hosted
open-weight model only when the question needs it:

- Is this scene visually coherent?
- Did the edit preserve the argument?
- What changed between two distant moments?
- Is this shot emotionally landing?
- Did a visual callback happen later?

Do not send entire raw videos to expensive models by default. Segment
first with local tools, then escalate.

## Recommended model ladder

For the Codex videographer lane:

1. Local tools first: FFmpeg/ffprobe, `scenedetect`, `faster-whisper`,
   contact sheets, sampled frames, and manifests.
2. Gemini 2.5 Flash-Lite low resolution for cheap bulk video QA and
   summaries.
3. Gemini 2.5 Flash default resolution when visual detail matters.
4. Gemini Pro only for hard long-range temporal reasoning or high-value
   editorial review.
5. GPT-5.4 mini or GPT-5.5 for Codex-integrated frame review, script
   generation, and tool orchestration, not bulk native video ingestion.
6. Qwen3.5 Flash/Plus and Qwen2.5-VL through a hosted provider as an
   early bakeoff against Gemini, before local open-weight serving.
7. InternVL and fully local open-weight serving after the hosted bakeoff
   proves that the open-model quality is worth operational complexity.

## How this changes the harness design

The harness should not ask one model to "watch the whole video" as the
default. It should create a video evidence packet:

- source metadata
- transcript with word timestamps
- scene boundaries
- thumbnail/contact sheet
- selected frames at boundaries and moments of interest
- audio loudness/silence notes
- platform target
- question being asked

Then the harness chooses a model tier:

- Text-only model for transcript/timeline work.
- Image model for selected stills/contact sheets.
- Native video model for motion or temporal questions.
- Strong reasoning model for final editorial judgment.

This keeps cost down and makes the model's evidence inspectable.

## Practical recommendation

For now, do not chase local open-weight video serving as the first
system. The first system should use our newly deployed local tools to
prepare strong evidence packets, then call a cheap native-video model
only when a question needs actual video. Gemini Flash-Lite/Flash and
Qwen3.5 Flash/Plus are the current cost/performance candidates for that
role.

Open-weight video is worth a second phase. The first useful experiment
would be not "install a huge video model", but a bakeoff on five short
clips:

1. Local-only evidence packet.
2. Gemini Flash-Lite low resolution.
3. Gemini Flash default resolution.
4. Qwen3.5 Flash or Qwen3.5 Plus through a hosted provider.
5. Qwen2.5-VL-72B through the cheapest credible hosted provider.
6. One open model locally only if the deploy path is clean.

Score them against concrete editing tasks: scene summary, event
localization, speaker/action alignment, caption confidence, visual
defects, and final editorial usefulness.

## Sources read

- Google AI for Developers, "Video understanding," accessed
  2026-06-17:
  https://ai.google.dev/gemini-api/docs/video-understanding
- Google AI for Developers, "Gemini Developer API pricing," accessed
  2026-06-17:
  https://ai.google.dev/gemini-api/docs/pricing
- Google Developers Blog, "Advancing the frontier of video understanding
  with Gemini 2.5," accessed 2026-06-17:
  https://developers.googleblog.com/en/gemini-2-5-video-understanding/
- OpenAI Developers, "Models," accessed 2026-06-17:
  https://developers.openai.com/api/docs/models
- OpenAI Developers, "Images and vision," accessed 2026-06-17:
  https://developers.openai.com/api/docs/guides/images-vision
- OpenAI, "API Pricing," accessed 2026-06-17:
  https://openai.com/api/pricing/
- Anthropic, "Vision - Claude API Docs," accessed 2026-06-17:
  https://platform.claude.com/docs/en/build-with-claude/vision
- Qwen, "Qwen2.5-VL," accessed 2026-06-17:
  https://qwenlm.github.io/blog/qwen2.5-vl/
- arXiv, "Qwen2.5-VL Technical Report," accessed 2026-06-17:
  https://arxiv.org/abs/2502.13923
- Qwen, "Qwen2.5-Omni," accessed 2026-06-17:
  https://qwenlm.github.io/blog/qwen2.5-omni/
- GitHub, `QwenLM/Qwen3-VL`, accessed 2026-06-17:
  https://github.com/QwenLM/Qwen3-VL
- GitHub, `QwenLM/Qwen3-Omni`, accessed 2026-06-17:
  https://github.com/QwenLM/Qwen3-Omni
- Alibaba Cloud Model Studio, "Supported Models and Capabilities
  Overview," accessed 2026-06-17:
  https://www.alibabacloud.com/help/en/model-studio/models
- OpenRouter, "Qwen3.5 Flash," accessed 2026-06-17:
  https://openrouter.ai/qwen/qwen3.5-flash-20260224/pricing
- OpenRouter, "Qwen3.5 Plus 2026-04-20," accessed 2026-06-17:
  https://openrouter.ai/qwen/qwen3.5-plus-20260420
- OpenRouter, "Qwen2.5-VL 72B Instruct," accessed 2026-06-17:
  https://openrouter.ai/qwen/qwen2.5-vl-72b-instruct
- CloudPrice, "Qwen2.5 VL 72B Instruct pricing and specs," accessed
  2026-06-17:
  https://cloudprice.net/models/alibaba-qwen2-5-vl-72b-instruct
- arXiv, "InternVL3.5: Advancing Open-Source Multimodal Models in
  Versatility, Reasoning, and Efficiency," accessed 2026-06-17:
  https://arxiv.org/html/2508.18265v1
- GitHub, `DAMO-NLP-SG/VideoLLaMA3`, accessed 2026-06-17:
  https://github.com/DAMO-NLP-SG/VideoLLaMA3
- LongVideoBench, accessed 2026-06-17:
  https://longvideobench.github.io/
- Video-MME, accessed 2026-06-17:
  https://video-mme.github.io/home_page.html
