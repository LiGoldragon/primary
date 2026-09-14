# Claude remote-control witness

## What was verified locally

On 2026-09-14, the installed `claude` executable reported version `2.1.263 (Claude Code)`. Its local help lists `--remote-control [name]` as: “Start an interactive session with Remote Control enabled.”

I started an interactive Claude partner in `/home/li/primary` with:

```text
claude --dangerously-skip-permissions --remote-control dc1c58 <subflow brief>
```

The terminal displayed: “/remote-control is active · Continue here, on your phone, or at [a claude.ai/code session URL].” This is a witnessed registration of a live Claude remote-control session. The session received a bounded `$subflow` brief with `FLOW_ID=dc1c58`, `FLOW_DIRECTORY=/home/li/primary/flows/dc1c58`, its Armando Torres research role, and the instruction to avoid unrelated edits and bulk copyrighted text. It then began source searches.

The session URL was sent directly to the user and is deliberately omitted from this durable report.

## What remains unverified

This worker cannot operate the user's phone, so it cannot witness the final phone connection or a phone-originated message. The prior local psyche record `flows/01a03f49/vision/remoteControlAllTheCodexTuiSessionsICreate.md` records such a successful phone-to-terminal round trip for Codex on 2026-08-27; that is helpful precedent, not verification of this Claude session.

The partner is an interactive process (PID witnessed after launch) attached to the current terminal-automation session. It stays live while that hosting PTY stays alive. There is no independent tmux or system-service persistence witness for this exact session, so process launch alone must not be represented as durable accessibility after the PTY is closed. A replacement persistent session would need a separately verified host process and a newly issued remote URL.

The machine's Tailscale client was offline (`BackendState: NoState`) during this check. Claude remote control nevertheless registered, so this specific path did not require a live local Tailscale endpoint.

## Practical conclusion

Remote use is supported and easy in this installed Claude Code build: start an interactive session with `--remote-control`, then use the displayed Claude URL or the phone client. The command is not by itself proof that a phone can join; the “active” status and the session URL are the local witness, while a phone message remains the end-to-end witness.
