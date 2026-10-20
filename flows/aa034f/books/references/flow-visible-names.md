# References: Flow Visible Names

Witnessed in /git/github.com/LiGoldragon/flow at dcb63e6 (flow 0.35.21), `git show dcb63e6:<path>`.

- Title shape and topic verbatim: crates/flow-nexus/src/title.rs:3-6 (shape, topic exactly as the Address holds it), :26-31 (TitledSeat fields), :62 (`topic: self.address.topic.clone()`, no to_lowercase).
- Claude title needs a reserved Flow ID: crates/flow-nexus/src/herdr/launch.rs:1815-1826.
- Claude `--remote-control` and `--name` both carry the title: crates/flow-nexus/src/herdr/launch.rs:1892-1900 (CLAUDE_REMOTE_CONTROL_FLAG :458, CLAUDE_NAME_FLAG :464). Test: :3601.
- Workspace renamed and display-agent set before the agent starts: launch.rs:1834-1838 calls show_title_before_agent, defined :1609-1634 (workspace rename :1614-1621, pane report-metadata --display-agent :1622-1632).
- Pane label and display agent read back: launch.rs:1561-1606 (readback :1584-1605). Workspace label read back: :1636-1665. Both called in the title step: :1694-1697.
- Codex thread name set and read back: crates/flow-nexus/src/codex.rs:1455-1486 (`thread/name/set` :1464, `thread/read` :1468, difference refused :1475-1481); called from launch.rs:1686-1692.
- Herdr agent name internal: launch.rs:1570-1572, :1715-1716, :1831.
- Not witnessed: the live Remote Control readback; no claim about the thread list is made.
