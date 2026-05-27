# 1 · Browser CLI + dev-port state survey

Survey of CriomOS workspace for the existing Chrome DevTools Protocol configuration, the picked browser-control CLI, and how that CLI currently calls its external model API.

## Chrome dev-port configuration

**Status: Enabled, configured via hexis wrapper, no explicit port flag in CLI launches.**

The Chrome setup is in `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/max/default.nix` (lines 54–82). Chrome (google-chrome, the binary `pkgs.google-chrome`) is wrapped via the `hexis` library (`inputs.hexis.lib.wrapWithHexis`) to seed the Chrome local config on first launch.

The critical seeded state:
- **Path:** `$HOME/.config/google-chrome/Local State` (Chrome's global state file)
- **Declared state:** `devtools.remote_debugging.user-enabled = true` (line 76)
- **Mode:** "once" — set once on first launch, persists forever even if the user toggles it in the UI

This configuration **enables the DevTools remote debugging toggle** that users see at `chrome://inspect/#remote-debugging` but does not explicitly specify a port flag. Chrome defaults to port **9222** when the toggle is enabled via the Local State config. The report `/git/github.com/LiGoldragon/CriomOS/reports/0031-browser-use-packaging-plan.md` (line 5) confirms: "CDP exposed at `127.0.0.1:9222` once gen 80 is live".

**Port number: 9222** (Chrome DevTools Protocol default, hardcoded by Chrome when remote debugging is enabled).

There is no environment variable gating; the configuration is always applied on systems at the `size.large` tier or above (the same tier where Chrome itself is installed).

## Browser-control CLI: browser-use

**Status: Packaging planned, not yet installed. Pre-implementation research and smoke test completed.**

The picked browser-control CLI is **browser-use**, a Python library + CLI wrapper around Chrome DevTools Protocol (CDP) designed for LLM agents. This is documented in `/git/github.com/LiGoldragon/CriomOS/reports/0031-browser-use-packaging-plan.md`.

**Key facts about browser-use:**
- **Version:** 0.12.6 (as of April 2026, per the report)
- **Approach:** Direct CDP via their own `cdp-use` client (migrated off Playwright in 2025)
- **Design:** a11y-tree-snapshot loop for LLM agent interaction
- **Status in this workspace:** Pre-implementation; smoke test passed (lines 34–56 of the report)

**Why it was picked:** It is the mainstream choice in early 2026 (89.1% adoption on WebVoyager per the report, line 28), works against an existing Chrome via CDP, and fits the "CLI that calls another model API" requirement because browser-use itself is agent-agnostic — it accepts `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `GOOGLE_API_KEY` from the environment, then makes model API calls internally.

**Implementation status:** The workspace has completed research and a smoke test but is awaiting Li's surface decisions on (1) CLI-only vs. library-env exposure, (2) LLM API key wiring (gopass integration), (3) profile tier, and (4) closure cost sign-off before packaging into CriomOS-home. The planned location is `/packages/browser-use/` with `uv2nix` and `pyproject.nix` for dependency management.

## How browser-use currently calls external model API

**Status: Designed but not yet wired in CriomOS-home. Will use standard env-var API key pattern.**

browser-use accepts model API keys via environment variables. It does **not** call a local OpenAI-compatible endpoint by default — it speaks directly to the upstream provider (Anthropic, OpenAI, Google).

**Current design per the packaging plan (line 149):**

```
browser-use accepts ANTHROPIC_API_KEY / OPENAI_API_KEY / GOOGLE_API_KEY.
Likely want a similar wrapper that reads from gopass before exec.
```

**Proposed wiring in CriomOS-home (analogue to `linkup`):**

The report shows that `pi` (the coding agent CLI) currently wires its Linkup API key via gopass at exec time: `LINKUP_API_KEY="${LINKUP_API_KEY:-$(${pkgs.gopass}/bin/gopass show -o linkup.so/api-key 2>/dev/null || true)}"` (from `/git/github.com/LiGoldragon/CriomOS-home/packages/pi/default.nix` line 62).

The browser-use packaging plan (lines 147–151) says the same pattern should apply: a shell wrapper around the `browser-use` CLI that reads the API key from gopass before exec. Example shape:

```bash
export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-$(gopass show -o anthropic.com/api-key)}"
export OPENAI_API_KEY="${OPENAI_API_KEY:-$(gopass show -o openai/api-key)}"
exec browser-use "$@"
```

**Redirect surface for local AI node:**

To redirect browser-use to call a local OpenAI-compatible endpoint instead of the cloud provider, the following would change:

1. **Environment variables.** Instead of passing `OPENAI_API_KEY` (pointing to api.openai.com), one would pass:
   - `OPENAI_API_BASE` or `OPENAI_ENDPOINT` (depending on the SDK version and browser-use's wrapper layer)
   - An API key for the local endpoint (could be a dummy key; many local servers accept any key)

2. **Code changes to browser-use or wrapper.** If browser-use's underlying SDK doesn't expose an endpoint override env var, a thin wrapper script or a custom browser-use fork would be needed to pass the endpoint to the Python SDK at init time.

3. **Network exposure of local AI node.** The local AI node must expose its OpenAI-compatible API (e.g., `http://127.0.0.1:8000/v1/chat/completions` or similar) on a network address reachable from browser-use's execution context.

No work has been done yet to wire up the local AI node itself; that is in scope for Scout 2's report (`2-local-ai-node-state.md`).

## Summary for orchestrator design

The orchestrator (running at cloud tier, e.g., GPT-5.5) would:

1. Call `browser-use` CLI or library with a task description.
2. browser-use internally calls an LLM API to interpret the task and decide browser actions.
3. **Redirect goal:** Instead of calling OpenAI/Anthropic cloud API directly, browser-use would call the local Gemma 4 Flash model (via the local AI node's OpenAI-compatible endpoint).
4. The local model drives the Chrome browser via CDP at `127.0.0.1:9222`, which the hexis-wrapped Chrome exposes automatically.

This three-tier flow — orchestrator → CLI → local model → browser — matches the design intent stated in the frame report (lines 17–18).

## Files and line references

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/max/default.nix` — Lines 54–82: Chrome wrap with remote debugging seeded `true`.
- `/git/github.com/LiGoldragon/hexis/nix/wrap.nix` — Lines 46–100: hexis wrapWithHexis function (Chrome launcher pattern).
- `/git/github.com/LiGoldragon/CriomOS/reports/0031-browser-use-packaging-plan.md` — Full pre-implementation research and smoke test for browser-use packaging into CriomOS-home; lines 5 (port 9222), 26–32 (what browser-use is), 147–151 (API key wiring design).
- `/git/github.com/LiGoldragon/CriomOS-home/packages/pi/default.nix` — Lines 61–62: Pattern for gopass-based API key wiring (Linkup example).
