# Configured and working plugins

Gmail, GitHub, and Google Calendar are installed, enabled, authenticated, and working. Harmless metadata calls succeeded against each provider. Sites also responded through its authenticated owner-site listing and currently returned zero sites.

Slack is named in local configuration but is not installed or connected. Chrome is configured but its required Codex browser extension is absent. The in-app Browser bridge had no available browser instance. Computer Use is explicitly disabled.

Documents, PDF, Presentations, Spreadsheets, Template Creator, and Visualize are installed local artifact/capability plugins; external authentication is not applicable to most of them. No live Excel session was present, which says nothing against standalone spreadsheet creation.

## Sources

- Witness: `flows/01a030df/witnesses/pluginStatus.md`
- `/home/li/.codex/config.toml`, lines 102–145
- `/home/li/.codex/.tmp/plugins/plugins/gmail/.codex-plugin/plugin.json`
- `/home/li/.codex/.tmp/plugins/plugins/gmail/.app.json`
- `/home/li/.codex/plugins/cache/openai-curated/plugin-management/0.1.0/skills/plugin-management/SKILL.md`
- `/home/li/.codex/plugins/cache/openai-bundled/chrome/26.721.41059/docs/chrome-troubleshooting.md`
- OpenAI, Plugins in Codex: https://help.openai.com/en/articles/20001256-plugins-in-codex/
