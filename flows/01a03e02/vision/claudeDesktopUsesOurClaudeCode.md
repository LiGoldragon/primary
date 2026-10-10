# force it to use our Claude code

## 2026-08-26T14:54:23+02:00

Context: The diagnosed local-thread failure exposed a Desktop-selected Claude Code `2.1.237` executable under mutable user state while the declarative terminal package was `2.1.241`.

> Okay, so this shows two things. One, the Claude Desktop is trying to use an obsolete version of Claude code, which means the Claude Desktop might be outdated. And yeah, we cannot allow the desktop to try to use something that it's installing statefully. So we have to modify the Claude Desktop Nix code to force it to use our Claude code.

Corrections: the four occurrences of “Clode” were corrected to “Claude” as evident speech-to-text errors.

