---
title: 7 — AI music and sound generation landscape
role: videographer
variant: Research
date: 2026-06-22
topics: [ai-music, sound-effects, models]
description: |
  Survey of closed and open AI music and sound-effects generators: model
  capabilities, cost, efficiency, licensing posture, companies, reviews,
  and practical recommendations for video-production work.
---

# 7 — AI music and sound generation landscape

## Short answer

For videographer work, use two tracks:

1. **Closed tools for immediate production** — Suno for fast vocal/full-song ideation, Stable Audio or ElevenLabs for safer commercial/background work, Adobe Firefly or ElevenLabs for sound effects.
2. **Open/local tools for experimentation and cluster leverage** — ACE-Step 1.5 first, Stable Audio 3.0 open weights second, YuE when full songs with vocals matter, AudioCraft/AudioGen for older-but-solid sound-effect baselines.

The legal/rights axis matters more than raw audio quality. Suno and Udio are musically impressive but litigation/licensing-transition risk remains relevant for commercial release. Stability, Adobe, Google, and ElevenLabs are positioning around licensed/partnered datasets and commercial-safe output. Open models give control and low marginal cost, but the user owns infringement review and operational complexity.

## Recommendation by use case

| Use case | First choice | Why | Backup |
|---|---|---|---|
| Quick song sketch with vocals | Suno Pro | Best creator UX, strong full-song output, cheap entry tier | Udio if its export/licensing state fits the current terms |
| Commercial background music for videos | Stable Audio API/app | Licensed-data story, instrumental/sound-design fit, clear API pricing | ElevenLabs Music |
| Sound effects / foley | Adobe Firefly or ElevenLabs SFX | Firefly has video-timeline/audio-hint workflow; ElevenLabs has simple API pricing | Stable Audio SFX / AudioGen |
| Local/open generation on cluster | ACE-Step 1.5 | Very fast local generation claims, MIT, broad GPU support, API/UI | Stable Audio 3.0 open weights |
| Open full songs with vocals | YuE | Apache 2.0, full-song lyrics-to-song, several-minute output | ACE-Step 1.5 |
| Enterprise/legal-safe audio program | Stability enterprise or Google Lyria 3 Pro | indemnification/partnering/watermark posture, API surfaces | Adobe enterprise/Firefly |

## Closed and commercial tools

### Suno

**Company / posture:** Suno is the category-defining consumer AI song generator. Its official pricing page currently lists Free, Pro, and Premier plans.

**Cost:** Free: 50 credits daily, about 10 songs/day, no commercial use. Pro: $8/month annual, 2,500 credits/month, up to 500 songs, commercial use for new songs. Premier: $24/month annual, 10,000 credits/month, up to 2,000 songs, Suno Studio access.

**Strengths:** Best quick path from prompt to full song with vocals. Strong editing/persona/stem features on paid tiers. Good for ideation, parody-free original sketches, social clips, rough demos, and finding a musical direction fast.

**Weaknesses:** Commercial rights are plan- and timing-dependent. Reviews and legal trackers still flag active/transitioning label litigation and licensing questions. For serious commercial sync, the lack of broad indemnification is more important than whether the output sounds good.

**Verdict:** Use for sketches and low-stakes/personal videos. For commercial client delivery, keep records of prompts/terms/plan state and avoid artist-name imitation.

### Udio

**Company / posture:** Udio is another leading full-song/vocal generator. Public reporting in 2026 frames Udio as transitioning toward licensed label/artist-participation models after major rights-holder deals.

**Cost:** Third-party pricing summaries list Free, Standard around $10/month, and Pro around $30/month, but the official pricing page was not reliably extractable in this pass. Verify live terms before buying or publishing.

**Strengths:** Historically strong audio fidelity, vocal realism, extension/inpainting workflows, and more producer-like control than early Suno.

**Weaknesses:** Reports in 2026 note transition-state restrictions such as disabled or constrained downloads/stems while licensing changes land. This makes it a poor sole dependency unless the current account/export terms are verified.

**Verdict:** Watch closely; potentially excellent, but use only after confirming current download, stem, and commercial-use terms.

### Stable Audio / Stability AI

**Company / posture:** Stability AI positions Stable Audio around licensed data, open weights, and enterprise licensing. The Stable Audio 3.0 page says the family is trained on fully licensed data, includes open weights for Small/Small SFX/Medium, supports full tracks up to six minutes, and offers enterprise indemnification.

**Cost:** Stability API pricing: 1 credit = $0.01. Stable Audio 2.5 costs 20 credits (~$0.20) for up to three minutes. Stable Audio 3.0 costs 26 credits (~$0.26) for up to six minutes.

**Strengths:** Best blend of commercial-safety posture, API clarity, instrumental/background generation, SFX, and open-weight experimentation. Strong fit for video background music, ambient beds, stingers, and sound-design assets.

**Weaknesses:** Less of a viral vocal-song machine than Suno/Udio. Consumer app pricing/licensing pages emphasize license categories more than simple per-month comparisons.

**Verdict:** Best default for videographer production music when commercial safety and API workflow matter.

### ElevenLabs Music and Sound Effects

**Company / posture:** ElevenLabs is strongest in voice, but now has music and sound-effects API surfaces.

**Cost:** API pricing page lists Music at $0.15/minute, 5-minute duration limit, commercial licensing on Starter+ plans, and 44.1 kHz 128–192 kbps audio. Sound Effects are listed at $0.12 per generation with MP3 44.1 kHz or WAV 48 kHz output. Starter API tier is $6/month; Creator $22/month, with included usage buckets.

**Strengths:** Simple API, predictable cost, strong surrounding voice/STT/dubbing stack. Good if the same workflow needs narration, dubbing, sound effects, and music under one vendor.

**Weaknesses:** Music-generation reputation is newer than Suno/Udio/Stability. Free tier/commercial-rights boundaries need care; paid tiers are the commercial baseline.

**Verdict:** Strong for integrated video-audio workflows and SFX; music should be auditioned against Stable Audio before standardizing.

### Google Lyria 3 Pro

**Company / posture:** Google’s Lyria 3 Pro is available through Vertex AI, Google AI Studio, Gemini API, Google Vids, Gemini app, and ProducerAI. Google says it generates up to three-minute tracks, understands intros/verses/choruses/bridges, uses materials Google has rights to use, filters against existing content, and embeds SynthID watermarking.

**Cost:** Public sources in this pass did not expose current Vertex price for Lyria 3 Pro. Third-party summaries cite old Lyria 2 reference pricing around $0.06 per 30 seconds, but that should not be treated as current Lyria 3 Pro pricing.

**Strengths:** Enterprise integration, Google product surfaces, watermarking, and responsible/partnered posture. Useful when already in Google Vids/Gemini/Vertex workflows.

**Weaknesses:** Less open; pricing and access can be product/subscription/public-preview dependent. Track length is up to three minutes, shorter than some competitors.

**Verdict:** Good enterprise/platform candidate; not the first pick for a small videographer workflow until pricing and API access are convenient.

### Adobe Firefly audio

**Company / posture:** Adobe Firefly’s sound-effect generator emphasizes commercially safe output trained on licensed and public-domain data. It supports text prompts, uploaded reference audio/video, and acting out a sound into a mic to guide timing/intensity.

**Cost:** Firefly starts free with limited generative credits; paid plans add credits. Exact audio credit burn was not clear from the fetched page.

**Strengths:** Excellent fit for timeline-based foley and video sound effects: place playhead, act out effect, add text direction, generate variations, layer effects. Strong commercial-safety messaging.

**Weaknesses:** Web/app workflow, not necessarily the easiest autonomous API substrate for agents. Music generation exists in Firefly surfaces, but sound effects are the clearer use case.

**Verdict:** Best human-in-the-loop foley generator for video edits; pair with ElevenLabs/Stable Audio for agentic API generation.

## Open and local models

### ACE-Step 1.5

**Company / community:** ACE Studio / StepFun-led open model, active GitHub repo with roughly 11k+ stars and many releases.

**License:** MIT.

**Capabilities:** 10-second to 10-minute generation; text-to-music, covers, repaint/edit, stem separation, multi-track/layering, vocal-to-BGM, BPM/key/time-signature controls, lyric timestamps, LoRA training, REST API and Gradio UI.

**Efficiency:** README claims under 2 seconds per full song on A100 and under 10 seconds on RTX 3090; local operation below 4 GB VRAM in some configurations; XL models need more VRAM. It supports CUDA, AMD ROCm, Intel XPU, Apple Silicon, and CPU paths.

**Verdict:** Most interesting open/local candidate for this workspace. It should be the first model a cluster operator tests for local music generation.

### Stable Audio 3.0 open weights

**Company / community:** Stability AI. Stable Audio 3.0 Small, Small SFX, and Medium are open-weight; Large is enterprise.

**License / rights posture:** Stability says the family is trained on fully licensed data. The exact Hugging Face model license should be read before deployment, but the posture is much cleaner than unverified scraped-data models.

**Capabilities:** Music and SFX; full tracks with dynamic structure up to six minutes through the broader 3.0 family; Small/Small SFX optimized for mobile/edge generation; Medium for full-song open-weight work.

**Verdict:** Best open-weight choice when commercial-safety story and sound effects matter. Test after ACE-Step if cluster deployment is easy.

### YuE

**Company / community:** HKUST / Multimodal Art Projection. GitHub shows roughly 6k+ stars.

**License:** Apache 2.0. The README explicitly encourages incorporation of outputs into works, including commercial projects, while recommending attribution and AI labeling.

**Capabilities:** Full-song lyrics-to-song, several-minute songs, vocal plus accompaniment, multiple languages/genres/vocal techniques, reference-audio in-context learning, incremental generation, LoRA support.

**Efficiency:** Heavy. README says 30 seconds takes ~150 seconds on H800 and ~360 seconds on RTX 4090. Full-song generation with many sessions wants 80 GB-class GPUs; 24 GB and lower should use fewer sessions or community quantized variants.

**Verdict:** Strong open full-song/vocal research model, but expensive to run. Use when vocals/full-song openness matters more than speed.

### Meta AudioCraft: MusicGen and AudioGen

**Company / community:** Meta FAIR / Facebook Research. GitHub shows roughly 23k+ stars.

**License:** Code MIT; model weights CC-BY-NC 4.0. Non-commercial weights make it research/prototyping rather than commercial production.

**Capabilities:** MusicGen for text/melody-conditioned instrumental music; AudioGen for environmental sounds and sound effects; EnCodec codec; MAGNeT, JASCO, MusicGen Style, AudioSeal.

**Efficiency:** Older baseline; MusicGen Large is around 3.3B parameters and historically wants a meaningful GPU. Good for experiments and as a reference architecture.

**Verdict:** Useful baseline and sound-effect research toolkit. Not the first production choice because weights are non-commercial.

## Sound-effects-specific notes

Sound effects are less risky than full songs because they are shorter, less tied to artist identity, and easier to audition against reality. The best tools are not necessarily the best song tools.

- **Adobe Firefly SFX** is best for human video editing because it aligns to a timeline, accepts voice/audio hints, and claims commercially safe licensed/public-domain training.
- **ElevenLabs SFX** is best for simple agentic API use: $0.12/generation, WAV/MP3 output, royalty-free messaging.
- **Stable Audio Small SFX / Stable Audio API** is best if we want open-weight or Stability-backed SFX under the same family as music beds.
- **AudioGen** is a good local research baseline, but commercial use is limited by weight licensing.
- **MMAudio/FoleyCrafter-style video-to-audio models** are promising for automatic foley synchronized to video, but the production surfaces are less mature and pricing/licensing is less clear than Adobe/ElevenLabs/Stability.

## Practical workflow for this workspace

1. **For a video needing music today:** generate 6–12 candidates with Stable Audio and Suno; pick a direction; if commercial, prefer Stable Audio/ElevenLabs/Adobe or replace the Suno sketch with a safer equivalent.
2. **For SFX:** use Firefly manually when timing matters; use ElevenLabs SFX when an agent can prompt many variations cheaply.
3. **For local cluster testing:** ask system-operator to package ACE-Step 1.5 as a local API first. Acceptance is one prompt → one WAV/MP3 in an agent inbox, plus a timing and VRAM report.
4. **For legal hygiene:** never prompt with living artists or protected song titles for publishable work; store prompt, date, tool, plan, model/version, generated file, and terms snapshot for anything distributed.
5. **For quality:** treat all generators as draft composers. Final deliverables still need loudness normalization, trims/fades, loop points, EQ, and sometimes stems or manual editing.

## Cost sanity checks

- Suno Pro: $8/month annual for up to 500 songs/month, very cheap for ideation, but rights risk is the trade.
- Stable Audio API: $0.20 for up to 3 minutes on 2.5; $0.26 for up to 6 minutes on 3.0, excellent for agentic batch generation.
- ElevenLabs Music: $0.15/minute; simple, predictable, but more expensive per long track than Stable Audio API.
- ElevenLabs SFX: $0.12/generation, reasonable for trying variants.
- Open/local: marginal cost is electricity and cluster time; setup cost and GPU occupancy dominate. ACE-Step is the likely efficiency winner; YuE is quality/control-heavy but slow.

## Bottom line

For the videographer lane: standardize first on **Stable Audio + ElevenLabs/Adobe SFX** for production-safe work, keep **Suno** as the fast creative sketchpad, and ask system-operator to test **ACE-Step 1.5** as the local cluster model. Treat **YuE** as an open full-song/vocal experiment, not the first operational service. Keep **Google Lyria 3 Pro** on the watchlist for Vertex/Gemini workflows once pricing and API access are clear.

## Sources checked

- Suno pricing page — current Free/Pro/Premier credits, commercial-use limits, and model access.
- Stability AI platform pricing — Stable Audio API credit prices for 2.5 and 3.0.
- Stable Audio 3.0 page — licensed-data posture, open-weight model family, enterprise indemnification claim, and six-minute track claim.
- ElevenLabs API pricing — music per-minute and sound-effect per-generation prices.
- Adobe Firefly sound-effect generator page — text/audio/video/voice-hint workflow and commercial-safe training claim.
- Google Keyword Lyria 3 Pro announcement — three-minute tracks, product surfaces, SynthID, and rights/mimicry posture.
- Meta AudioCraft GitHub — model list, code/weight licenses, stars, and MusicGen/AudioGen scope.
- YuE GitHub — Apache 2.0 license, full-song/vocal scope, performance notes, and commercial-output guidance.
- ACE-Step 1.5 GitHub — MIT license, performance claims, VRAM tiers, API/UI surfaces, and feature list.
