# 3 · Hugging Face prefetch precedent survey

## Workspace-internal precedent: Model fetching in CriomOS LLM stack

**Status: Substantial existing pattern, though not yet a reusable prefetch utility.**

The workspace already implements Hugging Face model fetching—but manually, with
hashes pre-computed and baked into configuration. Found in:

- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/llm.nix` (lines 32–64): Core
  pattern for multi-shard + single-file model fetching. Uses `pkgs.fetchurl` with
  explicit `url` + `sha256` hash pairs. Example (multi-shard):

  ```nix
  fetched = map (shard: {
    drv = pkgs.fetchurl {
      url = shard.url;
      sha256 = shard.sha256;
    };
    inherit (shard) filename;
  }) source.shards;
  ```

  Then assembles shards into a `runCommand` derivation with symlinks.

- `/git/github.com/LiGoldragon/CriomOS-lib/data/largeAI/llm.json` (entire file):
  Configuration listing ~15 models, each with explicit URLs to Hugging Face
  `/resolve/<commit-hash>/` endpoints and pre-computed SHA256 hashes (in nixpkgs
  `sha256-<base64>` format). Example entry:

  ```json
  {
    "url": "https://huggingface.co/unsloth/Qwen3.5-122B-A10B-GGUF/resolve/51eab4d59d53f573fb9206cb3ce613f1d0aa392b/Q4_K_M/Qwen3.5-122B-A10B-Q4_K_M-00001-of-00003.gguf",
    "sha256": "sha256-Rnyb2S6lGFOc91v1pfv7016aC0DXZsyqZ78SDhIEHfM=",
    "filename": "Qwen3.5-122B-A10B-Q4_K_M-00001-of-00003.gguf"
  }
  ```

**Gap:** No utility yet exists to automate the "prefetch + hash + populate config" cycle.
Each model is manually added to llm.json with hashes computed outside the Nix
workflow (likely via `sha256sum` or `nix-prefetch-url` on the command line,
then transcribed). The workspace has the *pattern* (fetchurl + hash) but not the
*automation*.

**No prior scout reports or skill documentation** found referencing huggingface,
hf-fetcher, nix-prefetch, or model derivations in `/home/li/primary/reports/` or
`/home/li/primary/skills/`.

## Standard Nix ecosystem: Absence of a canonical `fetchHuggingFace`

**Status: No standard fetcher in nixpkgs; custom implementations exist in the wild.**

Checked via `nix eval`:

- `nixpkgs#huggingface-hub` → does not export directly (no `meta.description`
  attribute in package set). Likely only available via `python3Packages.huggingface-hub`.
- `nixpkgs#hf-transfer` → does not exist as a top-level package.
- `python3Packages.huggingface-hub` → available at version 1.10.2 (confirmed via nix eval).

**Implication:** The Nix ecosystem has no standard `fetchHuggingFace` or
`fetchHfModel` fetcher (unlike `fetchGit`, `fetchurl`, `fetchTarball`, etc.).
Custom utilities are expected. The standard practice is to compose `pkgs.fetchurl`
with the HF `/resolve/...` URL pattern (as CriomOS already does), or wrap the
huggingface-cli Python package for programmatic downloads.

## Hugging Face CLI availability and download mechanism

**Status: `python3Packages.huggingface-hub` v1.10.2 available; CLI via huggingface-cli entrypoint.**

The `huggingface-hub` Python package (v1.10.2 in nixpkgs) ships with:

1. **CLI entrypoint:** `huggingface-cli` (or via `python -m huggingface_hub.cli.download`)
2. **Key command:** `huggingface-cli download <repo_id> [--revision <commit_hash>] [--cache-dir <path>]`
3. **Output:** Downloads model snapshot (single file or multi-file) to cache dir; prints paths.
4. **Hash computation:** The CLI does not compute hashes; would require post-download
   processing (e.g., `sha256sum` on fetched files).

**Design implication:** A Nix prefetch utility must:
- Shell out to `huggingface-cli download` or call `huggingface_hub.api.model_info()`
  (Python API) to resolve model repo + revision.
- Fetch files (or accept pre-computed URLs with explicit `/resolve/<commit_hash>/` endpoints).
- Compute SHA256 hashes (either inline or via `nix-prefetch-url` for direct fetching).
- Output a Nix expression (fetchurl call or derivation) + populate config.

## Precedent synthesis

The workspace has:

1. **Concrete fetching pattern** (multi-shard + single-file via `pkgs.fetchurl`).
2. **Concrete model config structure** (llm.json with URLs + hashes).
3. **No automation** to populate config from HF model IDs.
4. **No standard nixpkgs fetcher** to build on; must use `pkgs.fetchurl` +
   `huggingface-cli` or Python `huggingface_hub` API.

This is **appropriate for a new utility to fill**. The prototype should:
- Accept a Hugging Face model ID (repo + revision or HEAD).
- Resolve to URLs (via `huggingface-cli` or HF API).
- Prefetch + compute hashes.
- Emit llm.json entries (or a Nix derivation, depending on scope).

---

**Sources:**
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/llm.nix`
- `/git/github.com/LiGoldragon/CriomOS-lib/data/largeAI/llm.json`
- nix eval: `python3Packages.huggingface-hub` v1.10.2

