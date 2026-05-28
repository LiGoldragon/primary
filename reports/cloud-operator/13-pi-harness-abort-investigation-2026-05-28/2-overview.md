# Pi harness abort investigation — overview

The subagent found that the screenshot was not just the failed `nix flake check` and not a timeout. The Pi session JSONL records a normal bash tool failure (`Command exited with code 1`) followed by a separate zero-token assistant record with `stopReason: aborted` and `errorMessage: Operation aborted`, then compaction.

Best classification: a real command failure was followed by an independent aborted model/assistant operation, then normal proactive compaction near the context limit. If no human pressed Escape or triggered compaction, this is a Pi / OpenAI-Codex Responses abort-settlement bug candidate.

Evidence lives in `1-subagent-investigation.md`; the key local session span is lines 1859-1862 of the session JSONL named there.

Recommended follow-up: ask whether Escape or `/compact` was pressed. If not, file a Pi bug with sanitized evidence from the session lines and add event logging for abort source and compaction reason.
