# Scout Situational Map

Task: read-only inspection for why Playwright MCP is visible in ordinary Pi sessions and how to preserve a generic browser-agent path without global visibility.

Commands/files consulted: screenshots via `read`; `AGENTS.md`; `/home/li/.pi/agent/settings.json`; `/home/li/.pi/agent/mcp.json`; `/home/li/.pi/agent/mcp.json.bak-social-proof`; `/home/li/.pi/agent/agents/browser-social-media-scout.md`; project `.pi/agents`; Pi docs `/home/li/.local/share/criomos/pi/package/README.md` and `/home/li/.pi/agent/packages/pi-subagents-tintinweb/README.md`; source `/home/li/.pi/agent/packages/pi-mcp-adapter/{config.ts,index.ts}`.

Observed facts:

1. Cause of all-session visibility/loading: `/home/li/.pi/agent/settings.json` globally enables package `packages/pi-mcp-adapter`. That extension loads every ordinary session, reads default MCP config from `/home/li/.pi/agent/mcp.json` (`config.ts` default path), registers the `mcp` tool/commands, and on `session_start` initializes MCP state (`index.ts`). Because `/home/li/.pi/agent/mcp.json` defines one `mcpServers.playwright`, the status bar shows `MCP: 0/1 servers`; the `/mcp` panel shows server `playwright 0/23`. The server is configured `lifecycle: "lazy"`, so the screenshot state means visible/configured but not connected. Caveat: adapter source shows first-time/missing metadata cache can bootstrap/connect configured servers even if lazy.

2. Files mentioning Playwright/MCP:
- `/home/li/.pi/agent/settings.json`: global package `packages/pi-mcp-adapter`.
- `/home/li/.pi/agent/mcp.json`: server `playwright`, command `bash -lc ... npx -y @playwright/mcp@latest --extension`, env names for extension token and Chrome path, lifecycle `lazy`.
- `/home/li/.pi/agent/mcp.json.bak-social-proof`: older Playwright MCP config.
- `/home/li/.pi/agent/agents/browser-social-media-scout.md`: specialized browser-control agent using `extensions: [pi-mcp-adapter]` and `tools: "read, bash, ext:pi-mcp-adapter/mcp"`.
- `/home/li/.pi/agent/mcp-cache.json` and `/home/li/.pi/agent/mcp-npx-cache.json`: cached Playwright metadata/resolution.
No Playwright/MCP matches found under `/home/li/primary/.pi/agents` or `/home/li/primary/.agents`.

3. Recommended change: remove `packages/pi-mcp-adapter` from global `/home/li/.pi/agent/settings.json` so ordinary sessions neither load the extension nor show MCP status. Keep the Playwright server config out of global `mcp.json` if the adapter remains globally enabled. Create a generic browser agent, e.g. `/home/li/.pi/agent/agents/browser.md`, with broad browser-task instructions, `prompt_mode: replace`, `inherit_context: false`, `skills` as needed, `extensions: [pi-mcp-adapter]`, and `tools: "read, bash, ext:pi-mcp-adapter/mcp"`. Pi-subagents docs say `extensions:` is the loading authority and `ext:` only exposes tools, so this preserves an explicit browser-agent path while ordinary sessions stay invisible.

Unknown/not checked: exact UI behavior after config changes; no browser/MCP/gopass commands were run.
