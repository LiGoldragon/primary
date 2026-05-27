# Local AI Node State Survey

Date: 2026-05-27

## 1. AI Node Hostname and Location

The local AI node is designated **atlas** in the CriomOS cluster. It is configured in the test cluster fixtures as a **LargeAiRouter** node type, though no actual production deployment has been surveyed — only the declarative Nix configuration and model inventory.

- **Hostname:** `atlas` (FQDN would be `atlas.fieldlab.criome` in the test fieldlab cluster)
- **Fixture location:** `/git/github.com/LiGoldragon/CriomOS-test-cluster/fixtures/horizon/atlas.json` (lines 12–290)
- **Node species:** `LargeAiRouter` (line 14)
- **Behavior flag:** `behavesAs.largeAi: true` (line 112), `typeIs.largeAiRouter: true` (line 120)

In a real deployment, atlas would be configured through the `horizon` flake input, which feeds into CriomOS modules. The test fixture defines atlas as:
- 8 cores, 64 GB RAM
- Bare metal (X86_64 architecture)
- Tailnet member with router capabilities

## 2. Model Server Configuration

The node runs **llama.cpp** in "router mode" — an on-demand multi-model server that loads and unloads models dynamically, rather than keeping all models resident.

### Server Runtime

- **Process:** `llama-server` (from the `llama-cpp-strix-halo` package)
- **Binary location:** `/git/github.com/LiGoldragon/CriomOS/packages/llama-cpp-strix-halo.nix` (lines 1–12)
- **Nix module:** `/git/github.com/LiGoldragon/CriomOS/modules/nixos/llm.nix` (lines 1–176)
- **Service name:** `{nodeName}-llama-router` (derived from horizon.node.name; thus `atlas-llama-router` for atlas)

The start script is generated in llm.nix (lines 105–124) and executed by systemd. Key invocation:

```
llama-server \
  --host :: \
  --port 11434 \
  --models-dir ${modelsDir} \
  --models-preset ${presetsIni} \
  --models-max 1 \
  --no-webui \
  --sleep-idle-seconds 300
```

### Server Configuration

Configuration is read from `/git/github.com/LiGoldragon/CriomOS-lib/data/largeAI/llm.json` at build time:

- **Server port:** 11434 (line 2 of llm.json)
- **Models max:** 1 (line 12) — only one model loaded at a time; LRU eviction on swap
- **Idle unload:** 300 seconds (line 14) — models unload after 5 minutes idle
- **GPU layers:** 99 (line 18) — offload all model layers to GPU
- **No MMAP:** true (line 19) — disable memory mapping
- **WebUI:** disabled (`--no-webui`)

### Models in Inventory

The node is preconfigured to serve 8 models (llm.json lines 26–207):

1. **Qwen3.5-122B-A10B** Q4_K_M (lines 27–56) — 122B reasoning + coding, 76.5 GB, loads on startup
2. **GPT-OSS-120B** Q4_K_M (lines 57–81) — 120B general + coding, 63 GB
3. **Nemotron-3-Super-120B-A12B** UD-Q4_K_M (lines 82–111) — 120B MoE reasoning, 63 GB
4. **GLM-4.7-Flash** Q4_K_M (lines 112–127) — 32B fast general, 32 GB
5. **Nemotron-3-Nano-30B-A3B** Q4_K_M (lines 128–143) — 30B fast MoE, 17 GB
6. **Qwen3.5-27B** Q4_K_M (lines 144–159) — 27B dense reasoning, 17 GB
7. **Qwen3.6-35B-A3B** UD-Q4_K_M (lines 160–175) — 35B MoE reasoning, 22 GB
8. **Qwen3.6-27B** Q4_K_M (lines 176–191) — 27B dense reasoning, 17 GB

All models are in GGUF format (quantized), downloaded from Hugging Face. None are explicitly Gemma 4 Flash.

## 3. API Surface

The llama-server exposes an **OpenAI-compatible REST API** on the network. This is the standard llama.cpp HTTP surface and does not require additional translation layers for OpenAI-compatible clients.

### Endpoint

- **Host:** `::` (IPv6 all interfaces, port 11434)
- **Example endpoint:** `http://atlas.fieldlab.criome:11434/v1/chat/completions` (or `http://10.18.0.1:11434/` etc., depending on how the cluster network is configured)

### Authentication

- **Status:** Optional, but can be enforced (see below)
- **Mechanism:** API key file at `/var/lib/llama/api-key` (llm.nix line 30)
- **Support:** Bearer token or `X-Api-Key` header
- **File format:** Newline-delimited list of keys; each non-empty line is an accepted key (report 0036-llm-api-key-review.md line 43)
- **Behavior when file is empty:** Server runs without authentication (report 0036 line 19)

The API key file is **not yet integrated with a declarative secret manager** (agenix, sops-nix, or systemd.credentials). Currently `/var/lib/llama/api-key` is created empty at startup and must be populated out of band. This is a known limitation documented in report 0036 (lines 28–39).

### API Capabilities

The OpenAI-compatible surface provided by llama.cpp includes:

- `/v1/chat/completions` — streaming and non-streaming chat inference
- `/v1/completions` — raw token completion
- `/v1/models` — list available models
- `/health` — server health (no auth required)

Vision/multimodal support depends on whether the loaded model is multimodal. The current inventory contains no multimodal models explicitly (no Gemma 4 Flash or LLaVA variants noted).

## 4. Hardware and GPU Acceleration

The node is built around **AMD Strix Halo GPU** acceleration via Vulkan, not NVIDIA CUDA.

### GPU Setup

- **GPU acceleration library:** Vulkan (not CUDA or ROCm)
- **llama.cpp variant:** `llama-cpp-strix-halo` from `/git/github.com/LiGoldragon/CriomOS/packages/llama-cpp-strix-halo.nix`
- **Package override:** Vulkan support enabled; base is `pkgs.llama-cpp` (line 3)
- **llama.cpp version:** b8470 (line 8)

The service environment variable `HSA_OVERRIDE_GFX_VERSION=11.5.1` (llm.nix line 160) suggests ROCm compatibility support, though Vulkan is the primary path for Strix Halo.

### Memory Constraints

The systemd service limits (llm.nix lines 169–171):

- **MemoryMax:** 110 GB
- **MemoryHigh:** 100 GB

These limits prevent OOM from killing system services (hostapd, SSH) if model loading exhausts memory.

### User and Permissions

The service runs as the `llama` system user (llm.nix lines 128–140) with supplemental groups:

- `video` — GPU device access
- `render` — GPU rendering access

Model files are fetched at build time and placed in the Nix store by fetchurl derivations (llm.nix lines 38–62). The router directory is symlinked into `/var/lib/llama` at runtime.

### Computational Profile

With the current inventory:

- **Max single model:** 122 B parameters (Qwen3.5-122B, 76.5 GB quantized)
- **Typical fast model:** 30 B parameters (Nemotron-3-Nano, 17 GB)
- **GPU layers:** All layers (n-gpu-layers=99) — full GPU inference, not CPU + GPU split

The hardware must support:
- At least 110 GB total system memory to respect the service limit
- Vulkan-capable AMD GPU (Strix Halo or compatible) or fallback to CPU (slow)
- Sufficient VRAM to hold at least one model; with GPU layer offload, this depends on model size and quantization

Gemma 4 Flash (4–8B parameters, ~3–6 GB quantized) would easily fit alongside the existing 17–122 GB models and would be among the fastest in the portfolio if added.

## Gaps and Notes

1. **No Gemma 4 Flash yet:** The inventory does not include Gemma 4 Flash. To support your requirement, a new entry would be added to llm.json with source URL and SHA256 hash.

2. **Multimodal support:** None of the current models are multimodal. Gemma 4 Flash (small variant) is not inherently multimodal in the open-source releases; true multimodal support would require models like LLaVA, GLM-4V, or similar.

3. **No production deployment found:** The survey found only the declarative Nix config and test fixtures. No actual running instance of atlas with live GPU hardware was found; the configuration is ready to deploy to any node that reports `behavesAs.largeAi = true` in horizon.

4. **Authentication not yet enforced:** The API key file exists but is empty by default, so the server currently runs unauthenticated. A secret manager integration is planned (report 0036 lines 103–134).

5. **Network exposure:** The server binds to `::` (all interfaces) and opens port 11434 in the firewall (llm.nix line 142). In a Tailscale-only cluster, this is accessible to all Tailnet members. If public exposure is desired, a firewall rule or proxy would be needed.

---

**Summary:** The local AI node **atlas** is a declaratively configured llama.cpp server in router mode, running on Vulkan-accelerated AMD Strix Halo, preconfigured with 8 large quantized models (up to 122B parameters), and exposing OpenAI-compatible HTTP on port 11434. It is ready to deploy but requires activation through Horizon node config and optional secret provisioning for authentication.
