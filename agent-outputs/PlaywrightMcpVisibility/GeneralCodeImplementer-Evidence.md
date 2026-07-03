# GeneralCodeImplementer Evidence

Task and scope: Implement the approved browser-only Playwright MCP shape. Ordinary Pi sessions should not load or show the MCP adapter or Playwright server; the generic `browser` subagent should be able to load Playwright MCP through a private config without exposing tokens or cookies.

Files consulted:
- `/home/li/.pi/agent/settings.json`
- `/home/li/.pi/agent/mcp.json`
- `/home/li/.pi/agent/packages/pi-mcp-adapter/README.md`
- `/home/li/.pi/agent/packages/pi-mcp-adapter/index.ts`
- `/home/li/.pi/agent/packages/pi-mcp-adapter/config.ts`
- `/home/li/.pi/agent/packages/pi-subagents-tintinweb/README.md`
- `/home/li/.pi/agent/packages/pi-subagents-tintinweb/src/custom-agents.ts`
- `/home/li/.pi/agent/packages/pi-subagents-tintinweb/src/agent-runner.ts`

Observed facts:
- `pi-mcp-adapter` defaults to `/home/li/.pi/agent/mcp.json`, but supports a `--mcp-config` flag and `pi.getFlag("mcp-config")`.
- `pi-subagents-tintinweb` frontmatter supports absolute extension paths via `extensions:` and narrows extension tools through `tools: ext:<extension>/<tool>`.
- A wrapper under `/home/li/.pi/agent/extensions/` is globally discovered by ordinary `pi --help`; moving the wrapper outside that directory removes ordinary MCP visibility.
- MCP metadata caches are read by the adapter after it is loaded; without the adapter globally loaded, they do not independently expose Playwright.

Changed files:
- `/home/li/.pi/agent/settings.json`: removed `packages/pi-mcp-adapter` from global packages.
- `/home/li/.pi/agent/mcp.json`: replaced global server config with an empty `mcpServers` object.
- `/home/li/.pi/agent/browser-mcp.json`: preserved the Playwright server command with the gopass path `playwright.dev/mcp-extension-token` and lazy lifecycle.
- `/home/li/.pi/agent/mcp.json.bak-browser-only-20260703T104425`: backup of the prior global MCP config.
- `/home/li/.pi/agent/browser-mcp/pi-mcp-adapter.ts`: browser-only wrapper that injects the private MCP config for the adapter.
- `/home/li/.pi/agent/agents/browser.md`: new generic browser agent; subagent type is `browser`.
- `/home/li/.pi/agent/agents/browser-social-media-scout.md`: disabled with `enabled: false`, no MCP extension, and a pointer to `browser`.
- `/home/li/primary/private-repos/social-media/browser-agent-generic-2026-07-03.md`: private non-secret note with validation guidance.

Checks run:
- `python` JSON validation for settings, global MCP config, and browser MCP config: passed; global adapter package absent; global MCP servers empty; browser MCP servers contains `playwright`.
- `node --check /home/li/.pi/agent/browser-mcp/pi-mcp-adapter.ts`: passed.
- `pi --help | grep -i -E 'mcp|playwright'`: passed with no matches, so ordinary Pi help no longer exposes MCP/Playwright.
- `pi -e /home/li/.pi/agent/browser-mcp/pi-mcp-adapter.ts --help`: passed; explicit browser wrapper loads the MCP flag without starting Playwright.
- Python frontmatter check for `browser.md` and disabled scout: passed.

Skipped checks:
- No browser navigation, no social-media reading, and no gopass token lookup were run by design.
- Full live browser MCP connection was not tested because it would invoke the browser/token path.

Blockers and follow-up:
- Existing sessions that already loaded `pi-mcp-adapter` may continue to show MCP until restarted or reloaded.
- Existing dirty primary and private social-media worktrees predate this change; they were preserved.
