# Third stack offline evaluation

This directory contains a deterministic, synthetic-only evaluation. It does not call a provider, download weights, install a harness, or read credentials. The default command is:

    node flows/34d94e/evaluation/third-stack/run.mjs

The runner validates 12 blinded case inputs against a fixed evidence rubric and exercises a localhost SDK transport fixture. The offline adapter has also completed a root-owned replay against the pinned OpenCode 1.17.13 FHS wrapper. These are fixture-transport checks; they do not produce a provider call, model roundtrip, or model score. A real provider run requires an explicit `--provider-descriptor path` and `--secret-fd N`, plus an adapter implementation wired to that descriptor; absent either flag it exits before network/provider work. No secret is read from argv or environment.

The leading comparison is Kimi K3 + OpenCode, with DeepSeek V4.1 Flash, GLM 5.3, and Qwen 3.8 helper metadata retained from the current recommendation. These are evaluation labels, not a provider selection or production authorization.

## Offline adapter witness

`offline-adapter.mjs --opencode /absolute/path/to/opencode` completed a root-owned replay with the pinned FHS-wrapped OpenCode `1.17.13`. The recorded witness used three localhost chat-completion requests: one auxiliary request and the two required native-tool replay requests. It records the wrapper real path and SHA-256 separately from the unmodified release-member hash. The report retains expected source commit `10c894bdeef3618f5666fb506ef7f9491bb964d8`. It exits 2 when the explicitly supplied binary is absent. It creates a known `fixture.txt` in an isolated temporary cwd, configures a localhost OpenAI-compatible fake provider with reasoning, native tool calls, and `reasoning_content`, then checks the first tool declaration and the second assistant/tool continuation before sending the final stop event. Child stdout and stderr are drained with bounded output; timeout, spawn, JSON, and server failures clean up the child, server, and temporary directories. Only a small allowlist of locale/path/XDG variables reaches OpenCode, so provider credentials are never inherited.

`offline-adapter.test.mjs` uses a local fake executable to exercise runner plumbing for success, missing binary (exit 2), wrong version, secret-env isolation, and timeout cleanup. The successful real-binary replay remains an offline fixture witness, rather than a provider/model result.

## Gated provider driver

After provider access is authorized, the prepared first-real-run command is:

    node flows/34d94e/evaluation/third-stack/provider-run.mjs --provider-descriptor /path/to/descriptor.json --secret-fd 3 --opencode /absolute/path/to/opencode --output /path/to/output

The descriptor must set `access_authorized: true` and explicitly name `provider`,
`baseURL`, `model`, `version`, and OpenCode `1.17.13`. The driver rejects every
gate failure before reading the secret FD or starting a network listener. It verifies
the supplied binary's version first, then reads at most 16 KiB from FD 3 or higher
into memory. It never puts that value in a child environment, configuration file,
log, or output.

Every one of the 12 cases receives a fresh OpenCode process, HOME, cwd, and config.
Its prompt contains only the visible case prompt and that case's referenced synthetic
sources. Hidden expectations are never read. Results are one mode-0600, exclusively
created JSON file per case plus unscored run metadata. The loopback proxy admits only
`POST /v1/chat/completions`, forwards to `baseURL + /chat/completions` without
redirects or retries, and preserves a successful SSE content type. A non-2xx or
ambiguous upstream error is sanitized and latches the proxy closed for later requests.

Run the offline proof with:

    node flows/34d94e/evaluation/third-stack/provider-run.test.mjs

It uses a local fake OpenCode executable and an injected in-memory upstream transport.
Production transport remains strict HTTPS; the local environment has no certificate
generator available, so this test does not claim a live TLS handshake witness. It makes
no real provider call and proves the 12-case isolation, version-before-FD gate, secret
isolation, and sanitized proxy path. It is not a provider/model result.

## Immutable release package

`release-package.nix` packages the immutable upstream OpenCode 1.17.13 Linux x64 release with its published fixed SHA-256 and `fetchurl`. The release archive digest identifies the downloaded asset; it is separate evidence from the expected source-tag commit `10c894bdeef3618f5666fb506ef7f9491bb964d8`. This file does not install or build the package locally; evaluation and remote build are owned by the calling flow.

The package preserves the archive member under `libexec` and runs it through an FHS wrapper; `release-packaging-analysis.md` records why this avoids the earlier ELF fixup confounder.
