# Gemma 4 & Browser-Control CLI Ecosystem Research

**Date:** May 27, 2026  
**Research Focus:** Small multimodal Gemma 4 variants and browser-automation CLIs with custom LLM endpoints

---

## Block A: Gemma 4 Small Multimodal Models

### Release & Overview

[Google released Gemma 4 on April 2, 2026](https://cloud.google.com/blog/products/ai-machine-learning/gemma-4-available-on-google-cloud), marking a major expansion of their open-weight model family. [Gemma 4 includes native multimodal support (vision and audio) across all variants](https://huggingface.co/blog/gemma4), distinguishing it from earlier Gemma generations.

The family consists of four size tiers:
- **E2B** (2.3B effective / 5.1B with embeddings) — smallest
- **E4B** (4.5B effective / 8B with embeddings) — mid-small
- **26B MoE** (3.8B active parameters) — mixture of experts
- **31B Dense** — flagship

### Recommended Model: Gemma 4 E4B-it

For the workspace's use case (small multimodal model on a single GPU), **`google/gemma-4-E4B-it`** is the optimal choice.

**Model ID:** `google/gemma-4-E4B-it` (instruction-tuned variant)  
**License:** [Apache 2.0](https://huggingface.co/google/gemma-4-E4B) — commercially permissive, suitable for workspace deployment

**Parameters & Architecture:**
- 4.5B effective parameters (8B total with embeddings)
- 42 layers
- 128K context window
- Vision encoder: ~150M parameters
- Audio encoder: ~300M parameters

**VRAM Requirements** ([quantization guide](https://knightli.com/en/2026/05/01/gemma-4-local-vram-quantization-table/)):
- **4-bit (Q4_K_M):** 8 GB minimum (recommended for single 8GB GPU)
- **8-bit (Q8_0):** 12 GB minimum
- **16-bit (BF16):** ~15 GB
- E4B Q4_K_M GGUF: ~3.5 GB file, loads within 8GB with overhead

**Inference Server Support:**
- [Ollama](https://ollama.com/library/gemma4) — native support, widely tested
- [Unsloth](https://unsloth.ai/docs/models/gemma-4) — includes Gemma 4 optimizations
- vLLM — supported with multimodal inference
- llama.cpp (GGUF format) — works with quantized variants

**Why E4B over E2B?** E4B offers meaningfully better instruction-following and reasoning (2B effective → 4.5B), while remaining single-GPU deployable. E2B suits mobile/edge; E4B suits workstation/server.

### Gemma 3 Alternative (if Gemma 4 unavailable in your supply chain)

If Gemma 4 inventory is constrained, [Gemma 3 4B multimodal](https://huggingface.co/google/gemma-3-4b-it) remains a solid fallback—similar parameter class, proven stability, [available since late 2024](https://ai.google.dev/gemma/docs/releases).

---

## Block B: Browser-Control CLI Ecosystem

The browser-automation agent ecosystem has matured significantly by mid-2026. Below are the three credible candidates that support custom LLM endpoints and multimodal (vision) models.

### Candidate Comparison

| CLI | Base Model (Default) | Custom Endpoint Support | Multimodal (Vision) | Maturity | Install |
|-----|----------------------|------------------------|--------------------|----------|---------|
| **browser-use** | OpenAI GPT-4V | Yes (OpenAI-compatible + LiteLLM) | Yes (native) | v2.0 (Jan 2026) | `pip install browser-use` |
| **Stagehand (Browserbase)** | OpenAI/Anthropic (v3) | Yes (custom baseURL + LLMClient) | Yes (native) | v3 (2026) | `npm install @browserbase/stagehand` |
| **Skyvern** | OpenAI (default) | Yes (LiteLLM + OpenAI-compatible) | Yes (CV-first approach) | 2.0 (2026) | `pip install skyvern` or cloud |

### Detailed Profiles

#### 1. Browser-Use (Python)

**Strengths:**
- [Actively maintained; v2.0 released January 2026 with +12% accuracy improvement](https://github.com/browser-use/browser-use)
- Pure Python, lightweight CLI available
- [Explicitly supports custom OpenAI-compatible models via ChatOpenAI base_url + LiteLLM model strings](https://docs.browser-use.com/open-source/supported-models)
- Native multimodal vision support in latest release

**Custom Configuration Example:**
```python
# Pass custom base_url for OpenAI-compatible endpoint
agent = Agent(model=ChatOpenAI(
    model_name="gemma-4-E4B",
    base_url="http://localhost:8000/v1",  # local Ollama/vLLM
))
```

**CLI Invocation:** `browser-use` CLI interface available; can also run as MCP server or Python API.

[GitHub: browser-use/browser-use](https://github.com/browser-use/browser-use)

---

#### 2. Stagehand (JavaScript/TypeScript, Browserbase)

**Strengths:**
- [v3 released 2026; most production-ready automation framework](https://www.browserbase.com/blog/stagehand-v3)
- Built by Browserbase; integrates cloud browser backend option
- [Supports custom LLM clients via constructor and baseURL override](https://docs.stagehand.dev/v3/references/stagehand)
- Multi-provider: OpenAI, Anthropic, Google, custom endpoints via LLM client abstraction

**Custom Configuration:**
```typescript
// Custom LLM client with any endpoint
const agent = new Stagehand({
  llmClient: customLLMClient,  // Anthropic, local OpenAI-compatible, etc.
});
```

**Architecture:** SDK-first (TypeScript); CLI available via wrapper scripts. Designed for both headless automation and web-based workflow builder.

[GitHub: browserbase/stagehand](https://github.com/browserbase/stagehand)  
[Docs: Stagehand v3](https://docs.stagehand.dev/v3/references/stagehand)

---

#### 3. Skyvern

**Strengths:**
- [Best-in-class performance on form-filling tasks (85.85% WebVoyager 2.0)](https://www.skyvern.com/)
- Hybrid approach: combines LLM reasoning + computer vision (no reliance on HTML parsing)
- [Supports local self-hosted mode with LiteLLM integration](https://github.com/Skyvern-AI/skyvern)
- CLI: `skyvern setup`, `skyvern quickstart`, `skyvern init` for local deployment

**Custom Model Configuration:**
LiteLLM integration allows any OpenAI-compatible endpoint or provider-specific config (Anthropic, Azure, local).

**Unique Advantage:** Vision-first design means it excels on complex, visually-driven workflows where HTML parsing fails.

[GitHub: Skyvern-AI/skyvern](https://github.com/Skyvern-AI/skyvern)  
[Docs: Introduction | Skyvern](https://www.skyvern.com/docs/introduction/)

---

### Selection Guidance

**For lightweight, Python-native deployment with Ollama/vLLM + Gemma 4:**  
→ **browser-use** (simplest local integration, pure Python, minimal dependencies)

**For production automation with cloud browser backend option:**  
→ **Stagehand** (most mature SDK, enterprise-ready, TypeScript ecosystem)

**For vision-intensive, form-heavy workflows:**  
→ **Skyvern** (strongest CV integration, best form-filling accuracy)

---

## Summary

**Gemma 4 E4B-it** (`google/gemma-4-E4B-it`) is the recommended small multimodal model for workspace deployment:
- 4.5B effective parameters, Apache 2.0 license
- 8 GB VRAM at 4-bit quantization
- Full multimodal support (text, image, audio)
- Compatible with Ollama, vLLM, llama.cpp

**Top Browser-Control CLI Candidates:**
1. **browser-use** — easiest for local Ollama + custom models
2. **Stagehand v3** — production-grade, multi-provider LLM support
3. **Skyvern** — best for vision-heavy automation tasks

All three support custom LLM endpoints (OpenAI-compatible base URLs or custom LLM clients), making them suitable for workspace inference deployments alongside Gemma 4.

---

## Sources

- [Google Cloud Blog: Gemma 4 Available](https://cloud.google.com/blog/products/ai-machine-learning/gemma-4-available-on-google-cloud)
- [Hugging Face Blog: Gemma 4](https://huggingface.co/blog/gemma4)
- [Google: Gemma 4 Model Card](https://ai.google.dev/gemma/docs/core/model_card_4)
- [Hugging Face: google/gemma-4-E4B](https://huggingface.co/google/gemma-4-E4B)
- [VRAM Requirements: Gemma 4 Quantization Table](https://knightli.com/en/2026/05/01/gemma-4-local-vram-quantization-table/)
- [Browser-Use GitHub](https://github.com/browser-use/browser-use)
- [Browser-Use Docs: Supported Models](https://docs.browser-use.com/open-source/supported-models)
- [Stagehand v3 Blog](https://www.browserbase.com/blog/stagehand-v3)
- [Stagehand GitHub](https://github.com/browserbase/stagehand)
- [Stagehand Docs](https://docs.stagehand.dev/v3/references/stagehand)
- [Skyvern GitHub](https://github.com/Skyvern-AI/skyvern)
- [Skyvern Docs](https://www.skyvern.com/docs/introduction/)
- [Ollama: Gemma 4](https://ollama.com/library/gemma4)
- [Unsloth: Gemma 4 Documentation](https://unsloth.ai/docs/models/gemma-4)

