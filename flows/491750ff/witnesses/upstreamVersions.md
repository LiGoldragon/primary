# Upstream harness versions

Method: probe `curl -fsSL https://api.github.com/repos/openai/codex/releases/latest | jq -r '[.tag_name,.name,.published_at,.html_url] | @tsv'`, `curl -fsSL https://api.github.com/repos/anthropics/claude-code/releases/latest | jq -r '[.tag_name,.name,.published_at,.html_url] | @tsv'`, and the OpenAI Visual Studio Marketplace extension query with `Accept: application/json;api-version=3.0-preview.1`.

The OpenAI release API returned `rust-v0.149.1`, version `0.149.1`, published `2026-08-24T00:28:28Z`. The Anthropic release API returned `v2.1.241`, version `2.1.241`, published `2026-08-23T00:52:16Z`. The OpenAI Marketplace query returned the validated Linux-x64 Codex VSIX version `26.5818.61809`, updated `2026-08-24T06:07:52.91Z`.

Method: code read `/git/github.com/LiGoldragon/CriomOS-home/flake.lock`, `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`, `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix`, and `/git/github.com/LiGoldragon/CriomOS-home/packages/claude-code/default.nix`.

Published Home main is at `0836e4b7e367efe6a81a4fa657e2a2f741f0d801`. Its ancestry contains the Codex update commit `30e19a081d1fdc8916b7645b7fa4ffffda3c1a8d` and sidebar metadata commit `0836e4b7e367efe6a81a4fa657e2a2f741f0d801`. The lock pins `sadjow/codex-cli-nix` revision `05b1b39da135e34526f898600e09e67b55d5436c`, whose package declares `0.149.1`; Claude source and VSIX metadata declare `2.1.241`; the Codex sidebar metadata declares `26.5818.61809`.
