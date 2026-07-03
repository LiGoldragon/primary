# Scout Situational Map

Task: verification only for ordinary/non-browser agent exposure to MCP/Playwright. Scope limited to available session tools and `/home/li/.pi/agent/settings.json`, `/home/li/.pi/agent/mcp.json`. No browsing, no gopass, no social media, no repository edits.

Observed facts:
- Available tools in this non-browser scout session are local shell/file/search helpers and Linkup web helpers exposed under `functions`; no MCP adapter namespace or browser-control/Playwright tool is exposed in the tool list.
- `/home/li/.pi/agent/settings.json` lists packages: `packages/pi-criomos`, `packages/pi-linkup`, `packages/pi-subagents-tintinweb`, `packages/pi-continue`; no Playwright or MCP browser package appears there.
- `/home/li/.pi/agent/mcp.json` contains `{ "mcpServers": {} }`, so no global MCP servers are configured there.

Interpretations:
- MCP available to this non-browser agent: no, based on exposed tool namespaces.
- Global Playwright configured: no, based on inspected global settings and empty MCP server config.

Checks run:
- Read `/home/li/.pi/agent/settings.json`.
- Read `/home/li/.pi/agent/mcp.json`.

Blockers/unknowns:
- Did not inspect any other config locations or runtime internals.
