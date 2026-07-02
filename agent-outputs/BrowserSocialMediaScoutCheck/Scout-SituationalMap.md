# Scout Situational Map

Task: read-only check of the browser-social-media custom agent config and private setup notes. Scope was limited to `/home/li/.pi/agent/agents/browser-social-media-scout.md`, `/home/li/primary/private-repos/social-media/browser-agent-setup.md`, directory listing, and latest note `twitter-following-proof.md`. Sensitive social-media identifiers and credential material were not copied.

Observed facts:
- The current agent frontmatter contains `tools: "read, bash, ext:mcp/mcp"` and `extensions: [mcp]`.
- The body says MCP access is expected through Pi's `mcp` extension tool, narrowed by that `tools` selector and `extensions` frontmatter.
- The setup note says local Pi subagent docs confirmed extension exposure through `extensions:` and `tools:` selectors such as `ext:<extension>` and `ext:<extension>/<tool>`.
- The setup note explicitly says requested `mcp:playwright` spelling was not confirmed in installed Pi subagent docs, so the role narrows to `ext:mcp/mcp` and instructs use/list server `playwright`.
- Latest proof note `twitter-following-proof.md` reports the previous browser-control attempt was blocked by `TimeoutError`, with no credential material printed or persisted.

Interpretation:
- The config appears changed/fixed relative to a missing Playwright-MCP-tool failure if the intended fix was to expose Pi's MCP extension tool rather than a server-specific `mcp:playwright` selector.
- It appears ready to relaunch for discovery/listing of the `playwright` MCP server.

Blocker/unknown:
- Actual Playwright MCP availability and Chrome-session control were not verified in this check; the last private proof still shows a timeout blocker.

Checks run:
- Read current agent config.
- Read private setup note.
- Listed private directory for latest notes.
- Read latest proof note.
