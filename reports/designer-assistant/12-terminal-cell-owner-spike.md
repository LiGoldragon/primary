# 12 - Terminal Cell Owner Spike

Role: designer-assistant.

Status: superseded by
`reports/designer-assistant/13-terminal-cell-relay-architecture-failure.md`.

This report originally concluded that the Terminal Cell viewer/subscriber
prototype was a viable live attach path. Manual Pi testing after the report
proved that conclusion wrong: the full TUI rendered in Ghostty, but human
typing was slow, dropped keypresses, and eventually stopped.

The surviving useful substance is narrower:

- daemon-owned PTY lifecycle is still useful;
- transcript capture is still useful;
- programmatic input is still useful;
- real Pi/Ghostty launch witnesses are still useful diagnostics;
- `terminal-cell-view` as a transcript subscriber is not a valid live human
  attach primitive.

Use report 13 for the current conclusion: the next attach path must be an
abduco-like raw byte pump with transcript, projection, and actor/control logic
as side-channel observers rather than the live display path.
