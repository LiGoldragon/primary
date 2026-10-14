---
name: knowledge-claude-tool-allowance
description: The distinction between Claude tool availability and allowedTools permission rules, and writing records without Bash.
---

Claude Code 2.1.294 has separate built-in `Write` and `Edit` tools. Their installed implementations operate on file paths; they do not require a Bash call. Therefore a Claude main flow can create or edit its log and psyche record files without Bash when the file tools are available and the applicable path/permission policy permits those writes. A missing file, an unread existing file or a required exact replacement can impose the individual file tool's preconditions.

`--allowedTools` is not the flag that specifies the complete available built-in tool set. The CLI separately exposes `--tools` for that set, and `--disallowedTools` for refusals. Consequently leaving Bash out of `--allowedTools` alone does not prove that Bash has been removed. Permission mode, deny rules, agent tool restrictions and hooks remain relevant. Conversely removing Bash does not by itself remove Write or Edit.

An agent file's `tools` list is a tool-availability selection for that agent. If it supplies only read tools, the fact that Bash is absent does not give it a write capability. If Write and Edit are selected, Bash is not a prerequisite. This knowledge establishes the installed tool contract; it does not certify that any particular live Primary can write every path or that its own log/psyche paths are permitted in its effective configuration.

## Evidence

Installed CLI option declarations around byte 222401221 distinguish `--allowedTools` from `--tools`. The built-in Write description is at byte 208298047 and Edit at 216494795; child tool-resolution function `FA` is at 220235439. The current [Claude permission documentation](https://code.claude.com/docs/en/permissions) corroborates the distinction between tool permissions and availability. Version-pinned source excerpts are retained in `/home/li/private-repos/flow-evidence/41fa34/harness-knowledge-20261013/`. No live seat or log was changed for this inquiry.
