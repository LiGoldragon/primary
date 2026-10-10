# Fix messaging approval

## Every time you want to send a message, I have to allow it, so you have to fix that

Context: typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the same message that confirms the living has run the v6 Codex launcher command and Codex is now up. The pattern the living names: every message-send tool call requires a per-call permission approval from the living, which is unsustainable for a messaging-based cluster where flows exchange many messages. Related to fullSystemAccess (fullSystemAccess.md, same day), harnessReplacement (harnessReplacement.md, same day), and blockedCallsAndOtherModel (blockedCallsAndOtherModel.md, same day) — each iteration of the "the living has to approve one more thing" problem. The narrow fix is an allow rule for the messaging tools (both the Claude Code cross-session SendMessage and the MCP agent-intercom send-family), which only the living can add. Logged by the main flow before acting.

> Every time you want to send a message, I have to allow it, so you have to fix that. Codex is running now. I've run that command, and I've asked him to try to communicate with you.

-- psyche, typed.
