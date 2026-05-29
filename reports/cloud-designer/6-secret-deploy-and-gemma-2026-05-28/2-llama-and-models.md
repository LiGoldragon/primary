# 2 · llama-server module + model inventory (scout synthesis)

## The module

`CriomOS/modules/nixos/llm.nix` — gated by `behavesAs.largeAi` (from
`horizon.node`). Builds `packages/llama-cpp-strix-halo.nix` and runs
`llama-server` in router mode as a systemd service. **prometheus is the
live target** (AMD Strix Halo); `atlas` is only a test fixture
(`CriomOS-test-cluster/fixtures/horizon/atlas.json`).

## API key (current state on main)

- `apiKeyFile = "${runtimeHome}/api-key"` = `/var/lib/llama/api-key`,
  created **empty** by a tmpfiles rule. Nothing in-repo populates it.
- Passed via `--api-key-file` only if non-empty (`[ -s ... ]` guard) —
  so today llama-server **fails open: no auth** when the file is empty
  (noted in `CriomOS/reports/0036-llm-api-key-review.md`).
- `--api-key-file` is newline-delimited; a trailing newline is harmless
  (ignored as an empty trailing line). So the gopass→sops token (which
  may carry a trailing newline) is safe, and matches the client's
  `$()`-stripped key.
- sops-nix already exists on main (`modules/nixos/secrets.nix` +
  a `secrets` flake input stub overridden per-deploy by lojix), but
  **llm.nix on main does not use it yet.**

## Model inventory (current state on main)

`CriomOS-lib/data/largeAI/llm.json`. `mkModelStorePath` dispatches on
`source.kind ∈ { "multi-shard", "fetchurl" }`, each carrying per-file
`sha256`. Nine models today, all Unsloth GGUF.

## Two gaps for Gemma 4

1. **Hash/schema mismatch.** The prefetched hash
   `sha256-5uGLLTbFgT0CEoBAUsaiy3DhgokOYFk3pH2T48cm5bc=` is a
   `fetchHfModel` *snapshot* hash, not a per-file `fetchurl` sha256.
   To add Gemma to llm.json as-is needs the individual GGUF's
   `nix-prefetch-url` sha256; OR teach `mkModelStorePath` a new
   `kind: "hfModel"` that consumes `fetchHfModel` (the designed
   approach — bead `primary-1ubd`). The latter needs the CriomOS-lib
   utility landed (bead `primary-3dqf`) and a CriomOS flake.lock bump.
2. **Multimodal needs mmproj.** `llama-cpp-strix-halo` is
   `llama.cpp` (`vulkanSupport = true`, tag b8470) — the server
   supports `--mmproj` natively, but the module never passes it and
   the schema has no mmproj-file handling. **Text-only Gemma 4 works;
   vision needs an mmproj fetch + `--mmproj` wiring.**

## In-flight reconcile (the coordination issue)

The model inventory is being migrated off `data/largeAI/llm.json` to
`horizon.cluster.aiProviders` on the `horizon-re-engineering` /
`horizon-leaner-shape` branches (which **delete** llm.json). Those
branches already carry the full `resolveSecret` mechanism: an
`apiKey: Option<SecretReference>` resolved through
`cluster.secretBindings` to a `SecretBackend` (Sops / SystemdCredential
/ Agenix); on Sops it emits `sops.secrets.${name}` and points
`--api-key-file` at its path. **This is exactly the sops api-key wiring
the directive wants — but it lives on an in-flight system-operator
branch, not main.** Editing llm.nix/llm.json on main now risks being
obsoleted by this reconcile.
