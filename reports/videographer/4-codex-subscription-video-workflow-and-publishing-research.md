# Codex subscription video workflow and publishing research

variant: Research
date: 2026-06-17
role: videographer

## Question

Can the psyche use Codex plus an existing ChatGPT subscription to access
the models needed for a Codex-harness video-editing workflow, and what
online workflows exist for similar approaches? Also, how could finished
videos be posted to Instagram, TikTok, and YouTube without installing
anything during this research pass?

## Short answer

Yes for the Codex harness layer: current OpenAI documentation says Codex
can be used with ChatGPT sign-in, Codex usage counts against the
plan's agentic usage limit, and Codex's recommended model is currently
`gpt-5.5`, with `gpt-5.4-mini` as the faster/lower-cost option and a Pro
research-preview model for very fast coding iteration. That is enough
for the core harness work: planning edits, writing FFmpeg commands,
creating manifests, generating captions, editing Remotion projects, and
driving inspection loops.

No as a blanket claim that the ChatGPT subscription covers every media
model needed. OpenAI explicitly separates ChatGPT subscription benefits
from API usage. The models and services that may matter for a complete
video shop -- transcription, text-to-speech, generated images, generated
video, external APIs, and platform upload APIs -- can have separate
limits, availability, billing, credentials, and product lifecycles.

The practical path is therefore: use the ChatGPT/Codex subscription for
the agent brain and local harness; use local deterministic media tools
where possible; add API-key backed services only when a specific workflow
requires them and the cost/privacy boundary is acceptable.

## Current local snapshot

This was research-only. No packages were installed and no system
configuration was changed.

- Codex CLI is present: `codex-cli 0.139.0`.
- FFmpeg is present: `ffmpeg 8.0.1`, built with useful media features
  including `libass`, `libx264`, `libx265`, `libvmaf`, `libvidstab`,
  `vaapi`, and `whisper`.
- `yt-dlp` is present: `2026.03.17`.
- Python is present: `Python 3.13.12`.
- Node is not present in this shell, which blocks Remotion workflows
  until Node is supplied through the workspace's normal tooling path.
- The prior videographer report already found the same broad pattern:
  turn video into code, transcripts, timelines, manifests, rendered
  outputs, and inspection artifacts, then let Codex operate on those
  files.

## OpenAI access findings

OpenAI's Codex plan page says Codex usage depends on the user's plan and
counts toward an agentic usage limit; larger codebases, long-running
tasks, and high-context sessions consume more of that allowance. It also
says ChatGPT file upload, image generation, voice, image, and video
limits are separate from Codex limits.

OpenAI's Codex model page currently recommends `gpt-5.5` for complex
coding, computer use, knowledge work, and research workflows in Codex.
It also lists `gpt-5.4` for professional work, `gpt-5.4-mini` for fast
and efficient coding/subagent tasks, and `gpt-5.3-codex-spark` as a
text-only research-preview model available to ChatGPT Pro users. The
same page says Codex can be pointed at other providers that support the
Responses API or Chat Completions API, though Chat Completions support is
deprecated in Codex.

The ChatGPT Plus help page says Plus includes enhanced ChatGPT access,
higher GPT-5.5 limits, advanced reasoning models, image generation, file
uploads, Deep Research where available, and custom GPTs, but also says
API usage is separate and billed independently. The Pro tiers page says
Pro includes Codex, Pro models, Deep Research, image creation, memory,
and file uploads; the two Pro tiers mainly differ by usage allowance.

OpenAI's public Sora situation matters. The Help Center page says Sora
web and app experiences were discontinued on April 26, 2026, and the
Sora API will be discontinued on September 24, 2026. The developer video
generation guide also marks Sora 2 video generation models and the
Videos API as deprecated with the same September 24, 2026 shutdown date.
So Sora should not be treated as the foundation of a durable Codex video
editing workflow. It can be an export/migration concern if old Sora
assets exist, not the center of the system.

Data controls also matter. OpenAI says individual ChatGPT and Codex
content may be used to improve models unless the user opts out, while
business/API products are not used by default unless opted in. It also
notes Codex has separate controls for full-environment training data.

## What models are actually needed

For a local-first Codex video workflow, the critical "model" is the Codex
agent model, because most editing should be deterministic tooling:
FFmpeg, ffprobe, ImageMagick, caption formats, scripts, manifests, and
render commands.

The likely model/tool split:

- Codex model: edit plans, command generation, script writing, manifest
  maintenance, review loops, Remotion code when Node is available.
- Local FFmpeg/ffprobe: cuts, transcodes, audio extraction, subtitle
  burn-in, waveform-adjacent inspection, contact sheets, quality
  metrics.
- Local or API transcription: needed for word-level edits, captions, and
  shorts extraction. Local Whisper via FFmpeg may be enough to prototype;
  API transcription may be cleaner if diarization, speed, or quality
  matter.
- Image generation/editing: useful for thumbnails, title cards,
  diagrams, overlays, and article/video banners. It uses a separate
  ChatGPT image/video limit or API path, not the Codex limit.
- Text-to-speech or voice: optional for generated explainers and shorts.
  This likely means API/keyed service decisions, not "Codex subscription
  covers it automatically."
- Generated video: currently not a durable OpenAI subscription pillar
  because Sora is being discontinued. Treat generated video as an
  external/provider-specific module.

## Online workflow patterns

The strongest public workflows are not "the model edits an MP4." They
are agent harnesses around explicit media tools.

Remotion plus Codex is the cleanest motion-graphics route. Remotion's
own documentation now has a "Prompting videos with coding agents" page
that names Codex alongside Claude Code and OpenCode, requires Node.js,
and recommends creating a Remotion project, running the preview, then
starting the coding agent in the project directory. Remotion's main site
positions the tool as programmatic video: parameterized templates,
preview, and rendering to MP4, WebM, GIF, or PNG.

The creator workflow around "I edited this video 100% with Codex" shows
the more advanced version: shoot the source video first, then use Codex
to iterate on a Remotion project and supporting tools. The author used
segmentation/matting tools plus Remotion for text-behind-person effects,
and the important operational lesson is the review loop: render specific
frames and have Codex inspect them rather than trusting a full render
blindly.

`browser-use/video-use` is the closest published repository to the
desired local harness shape. It presents itself as an open-source way to
edit videos with coding agents, including Codex-compatible setup notes.
Its README describes filler-word and dead-space cuts, color grading,
short fades at cuts, burned subtitles, overlay generation, self-review
at cut boundaries, and persisted `project.md` memory.

`FFMPerative` is a smaller natural-language-over-FFmpeg reference. It
describes chat-based composition for changes like speed, resize, crop,
flip, reverse, speech-to-text transcription, closed captions, frame
sampling, and clip composition. It is useful as a shape reference:
natural language chooses operations, but FFmpeg executes them.

The practical repeated pattern is:

1. Keep raw media immutable.
2. Generate `ffprobe` metadata, audio extracts, frame samples, contact
   sheets, and transcripts.
3. Store the intended edit as a timeline or manifest.
4. Render through deterministic commands.
5. Inspect selected frames, audio peaks, subtitle fit, and platform
   constraints.
6. Iterate from artifacts, not memory.

## Recommended local workflow shape

A useful Codex video project should have a boring file structure:

- `sources/` for immutable raw footage.
- `inspection/` for `ffprobe` JSON, contact sheets, frame samples, audio
  extracts, and quality notes.
- `transcripts/` for text, word timestamps, and subtitle drafts.
- `timeline/` for edit decisions in a compact manifest.
- `renders/` for platform-ready outputs.
- `publishing/` for captions, titles, descriptions, thumbnails, platform
  metadata, and upload receipts.

Codex should do the planning and editing of those artifacts. FFmpeg and
other deterministic tools should do the actual render. The user should
approve strategy before expensive renders or platform publication.

Remotion should wait until Node is available. It is the right route for
motion graphics, explainers, animated captions, title cards, dashboards,
and reusable templates, but it is blocked locally today by missing Node.

## Posting to YouTube, TikTok, and Instagram

Codex can prepare platform-ready bundles now: final video, thumbnail,
title, description, hashtags, tags, captions/subtitles, alt text where
supported, and per-platform constraints. Actual posting requires account
authorization and platform APIs or a user-approved browser/computer-use
flow.

YouTube is the most straightforward official API route. The YouTube Data
API `videos.insert` method uploads a video and metadata, supports media
upload, accepts `video/*` or `application/octet-stream`, and requires an
OAuth scope such as `https://www.googleapis.com/auth/youtube.upload`.
Google's upload guide shows a Python uploader using OAuth 2.0 and a
client secrets file. A practical Codex harness can prepare the upload
bundle and later call a small uploader once OAuth credentials are
created and stored outside chat.

TikTok has an official Content Posting API. For direct posting, TikTok
requires a registered developer app, the Content Posting API product,
Direct Post configuration, approval for the `video.publish` scope, and
authorization from the target TikTok user. TikTok says unaudited clients
can post only privately until the client passes audit. TikTok also
supports upload-to-inbox/draft style flows with `video.upload`, where
the user completes the final post inside TikTok. The upload reference
supports either local file upload or pull-from-URL; a user token is
limited to six requests per minute, and at most five pending shares can
exist in a 24-hour period.

Instagram publishing is possible through Meta's Instagram Platform
content-publishing flow for professional accounts. Meta's current
developer docs are gated behind login in this browser, but the indexed
official page states that publishing a Reel requires creating a video
container with `media_type=REELS` and a `video_url`, then publishing it.
The official Reels API announcement confirms Reels were introduced on
Instagram Platform endpoints beginning June 28, 2022. In practice this
means an Instagram Business or Creator account connected through Meta
developer app permissions, a public or resumable video upload route, and
token handling. This is more setup-heavy than YouTube.

For all three platforms, the safe system shape is:

1. Codex creates a `publishing/<slug>/` bundle.
2. A platform-specific checker verifies duration, aspect ratio, codec,
   bitrate envelope, captions, thumbnail dimensions, title/description
   length, and missing metadata.
3. A dry-run command shows exactly what would be posted.
4. The psyche gives explicit approval for a specific platform/account.
5. The uploader runs using local credential files or a platform OAuth
   flow, never credentials pasted into public chat.
6. The receipt is saved in `publishing/<slug>/receipt.json` and a short
   note is written to the project manifest.

## Risks and boundaries

The subscription does not remove external-platform authorization. Even
if Codex can drive an upload script, YouTube, TikTok, and Instagram each
require OAuth/app setup and have private/public/audit restrictions.

Browser or computer-use posting may be possible, but it should be a
fallback for a user-watched session, not the durable publishing backbone.
APIs give better receipts, repeatability, and fewer fragile UI failures.

Sora should not be a dependency for the durable workflow because OpenAI
has announced discontinuation dates. Generated-video capability should
be treated as pluggable provider work, not assumed from the ChatGPT
subscription.

Secrets are the main operational hazard. API keys, OAuth client secrets,
refresh tokens, platform cookies, and account recovery details should not
be placed in public reports or chat. The report can define the uploader
shape; credential provisioning needs an explicit private/account setup
step.

## Recommendation

The right next implementation is a small local project harness, not a
large external install:

1. Define a video-project manifest and folder shape under the
   videographer lane.
2. Add FFmpeg/ffprobe inspection commands and platform profile checks.
3. Add transcript and subtitle artifacts.
4. Add render recipes for 16:9 YouTube, 9:16 Shorts/Reels/TikTok, and
   square/thumbnail assets.
5. Add publishing bundle generation without live upload.
6. Only after that, add one uploader at a time, starting with YouTube
   because its API path is clearest.

This uses the ChatGPT/Codex subscription for what it is strongest at:
agentic planning, coding, command synthesis, and review. It keeps media
execution local and inspectable, and it leaves platform authorization as
an explicit later step.

## Sources read

- OpenAI Help Center, "Using Codex with your ChatGPT plan," accessed
  2026-06-17: https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- OpenAI Developers, "Codex Models," accessed 2026-06-17:
  https://developers.openai.com/codex/models
- OpenAI Developers, "Codex CLI," accessed 2026-06-17:
  https://developers.openai.com/codex/cli
- OpenAI Help Center, "What is ChatGPT Plus?", accessed 2026-06-17:
  https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus
- OpenAI Help Center, "About ChatGPT Pro tiers," accessed 2026-06-17:
  https://help.openai.com/en/articles/9793128-about-chatgpt-pro-tiers
- OpenAI Help Center, "Model Release Notes," accessed 2026-06-17:
  https://help.openai.com/en/articles/9624314-model-release-notes
- OpenAI Developers, "All models," accessed 2026-06-17:
  https://developers.openai.com/api/docs/models/all
- OpenAI Developers, "Video generation with Sora," accessed
  2026-06-17: https://developers.openai.com/api/docs/guides/video-generation
- OpenAI Help Center, "What to know about the Sora discontinuation,"
  accessed 2026-06-17:
  https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation
- OpenAI Help Center, "How your data is used to improve model
  performance," accessed 2026-06-17:
  https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance
- Remotion, "Prompting videos with coding agents," accessed
  2026-06-17: https://www.remotion.dev/docs/ai/coding-agents
- Remotion, "Make videos programmatically," accessed 2026-06-17:
  https://www.remotion.dev/
- OpenAI Developer Community, "I Edited This Video 100% With Codex,"
  accessed 2026-06-17:
  https://community.openai.com/t/i-edited-this-video-100-with-codex/1373773
- GitHub, `browser-use/video-use`, accessed 2026-06-17:
  https://github.com/browser-use/video-use
- GitHub, `remyxai/FFMPerative`, accessed 2026-06-17:
  https://github.com/remyxai/FFMPerative
- Google Developers, "Videos: insert," accessed 2026-06-17:
  https://developers.google.com/youtube/v3/docs/videos/insert
- Google Developers, "Upload a Video," accessed 2026-06-17:
  https://developers.google.com/youtube/v3/guides/uploading_a_video
- TikTok for Developers, "Content Posting API Get Started," accessed
  2026-06-17:
  https://developers.tiktok.com/doc/content-posting-api-get-started
- TikTok for Developers, "Content Posting API Upload Video," accessed
  2026-06-17:
  https://developers.tiktok.com/doc/content-posting-api-reference-upload-video
- Meta for Developers, "Publish Content - Instagram Platform,"
  accessed 2026-06-17:
  https://developers.facebook.com/docs/instagram-platform/content-publishing/
- Meta for Developers, "Introducing Reels APIs to the Instagram
  Platform," accessed 2026-06-17:
  https://developers.facebook.com/blog/post/2022/06/27/introducing-reels-apis-to-instagram-platform/
