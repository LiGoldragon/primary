# PRODUCTION HARNESS MESSAGE DECLARATION CHECK

## Running identities and launch sources

- Flow: PID 933207, unit `flow-nexus-0531.service`, executable `/nix/store/vnfcw4w5s0vi0gyb6w8h6kzisc2hpnh4-flow-configured-0.53.1/bin/flow-nexus`.
- Codex primary: PID 2238, unit `codex-remote-control-next.service`, cwd `/home/li/primary`, `CODEX_HOME=/home/li/.codex-next`; argv is app-server remote-control/listen only.
- Codex candidate: PID 2242, unit `codex-remote-control-next-8mkkxq293hk2.service`, cwd `/home/li/primary`, `CODEX_HOME=/home/li/.codex-next-8mkkxq293hk2`; argv is app-server remote-control/listen only.
- Claude running sessions inspected: PIDs 836675, 1129986, 1161144, 1167713, 3325600, 3472803, 3650109, 3714734, 3734254; cwd `/home/li/primary`; executable Claude Code 2.1.294. Their argv has inline Flow hooks/settings, no MCP or Message flags.

## Applicable declarations

- `/home/li/.codex-next/config.toml`: MCP keys `agent-intercom`, `cua_repl`, `node_repl`, `openaiDeveloperDocs`; no Message key.
- `/home/li/.codex-next-8mkkxq293hk2/config.toml`: `cua_repl`, `node_repl`; no Message key.
- `/home/li/.claude/settings.json`, `/home/li/primary/.claude/settings.json`, `/home/li/primary/.claude/settings.local.json`: no MCP server declaration. `Bash(message *)` is a shell permission pattern, not an MCP declaration.
- `/home/li/.claude.json`: observed project/global `mcpServers` objects are empty; no Message entry.
- No `/home/li/.mcp.json`, `/home/li/primary/.mcp.json`, or bounded-depth equivalent was present.
- Enabled plugins: Codex primary list contains browser, chatcut, chrome, codex-app-tools, documents, github, gmail, google-calendar, pdf, presentations, rust-analyzer-lsp, sites, slack, spreadsheets, template-creator, visualize; candidate has no plugin entries; Claude enables only `rust-analyzer-lsp@claude-plugins-official`. None is Message.

## Production Flow and Message

Flow source is `/nix/store/y5mwawxkwkmpfb29h3qlkikhsdp8xs47-source`; its Cargo.lock pins `signal-flow 52.0.0` revision `2f9e2bfcb4fdaac5b07dcc7766b547bc1e077908`. No production Message process/unit was found; Message binary and pin are therefore unknown.

## Result and limit

No concrete Message MCP declaration or per-invocation Message launch reference was found in the applicable units, argv, homes, project settings, or enabled plugin lists inspected. Dynamic remote/managed registration not represented in these sources was not observable and remains an explicit limit; no claim is made about such registration.
