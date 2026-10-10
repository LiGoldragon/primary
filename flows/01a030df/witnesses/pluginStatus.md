# Plugin status

Method: probe `codex plugin list`, plugin dependency and permission queries, and harmless provider metadata calls through research subflows

On `codex-cli 0.149.0`, the subflows observed:

- Gmail: enabled, installed, user-enabled, permissions resolved; profile and inbox-label metadata calls succeeded without emitting account or message values.
- GitHub: enabled and authenticated; profile and login metadata calls succeeded without emitting values.
- Google Calendar: enabled and authenticated; profile and calendar-list metadata calls succeeded without emitting values.
- Sites: dependency and permissions resolved; the authenticated owner-site listing succeeded and returned zero sites.
- Slack: dependency resolver reported `installed=false` and permissions reported `not_installed`; no Slack connector tools were mounted.
- Chrome: Chrome was running, but every profile reported the Codex extension absent and disabled.
- In-app Browser: no browser instance was available to select in the flow.
- Computer Use: configured `enabled = false`.

The probes did not read or expose email messages, calendar events, account profile values, GitHub data, or site metadata. No configuration, permission, connection, or credential changed.
