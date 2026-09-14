# Third stack offline evaluation

This directory contains a deterministic, synthetic-only evaluation. It does not call a provider, download weights, install a harness, or read credentials. The default command is:

    node flows/34d94e/evaluation/third-stack/run.mjs

The runner validates 12 blinded case inputs against a fixed evidence rubric and exercises a localhost SDK transport fixture. This verifies the installed OpenCode SDK request shape only; it does not prove an OpenCode provider adapter or model roundtrip. A real adapter run requires an explicit `--provider-descriptor path` and `--secret-fd N`, plus an adapter implementation wired to that descriptor; absent either flag it exits before network/provider work. No secret is read from argv or environment.

The leading comparison is Kimi K3 + OpenCode, with DeepSeek V4.1 Flash, GLM 5.3, and Qwen 3.8 helper metadata retained from the current recommendation. These are evaluation labels, not a provider selection or production authorization.

## Offline adapter witness

`offline-adapter.mjs --opencode /absolute/path/to/opencode` is the pending real-binary witness. It requires OpenCode `1.17.13`; the report records expected source commit `10c894bdeef3618f5666fb506ef7f9491bb964d8`, while a successful run records the supplied binary's real path and SHA-256. It exits 2 when the explicitly supplied binary is absent. It creates a known `fixture.txt` in an isolated temporary cwd, configures a localhost OpenAI-compatible fake provider with reasoning, native tool calls, and `reasoning_content`, then checks the first tool declaration and the second assistant/tool continuation before sending the final stop event. Child stdout and stderr are drained with bounded output; timeout, spawn, JSON, and server failures clean up the child, server, and temporary directories. Only a small allowlist of locale/path/XDG variables reaches OpenCode, so provider credentials are never inherited.

`offline-adapter.test.mjs` uses a local fake executable to exercise runner plumbing for success, missing binary (exit 2), wrong version, secret-env isolation, and timeout cleanup. These tests are runner plumbing only; without the pinned real binary, the actual OpenCode gate and provider adapter witness remain pending.
