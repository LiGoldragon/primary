# Pi harness abort investigation

## Verdict

This was not a timeout and not the child command failure itself being rendered as `Operation aborted`.

The session shows two distinct records:

1. A `bash` tool result for the `nix flake check github:LiGoldragon/schema-next/collections-horizon-2026-05-28 --print-build-logs` command, marked `isError: true`, ending with `Command exited with code 1`.
2. A separate assistant message immediately afterward with `stopReason: "aborted"`, empty content, zero usage, and `errorMessage: "Operation aborted"`.

Compaction happened after that aborted assistant record. The compaction entry does not store whether it was manual or threshold-triggered, but local settings and the token count support ordinary proactive compaction: compaction was enabled with `reserveTokens: 32768`, the last successful assistant response had ~188k total tokens, and the compaction entry says `tokensBefore: 190034`.

Best classification: a normal `nix flake check` failure was followed by a separate abort of the next assistant/model operation, then built-in compaction. If nobody pressed Escape or manually compacted, this is suspicious and should be treated as a Pi/OpenAI-Codex Responses abort/event-settlement bug candidate.

## Evidence

- Image `/tmp/pi-clipboard-bf9bdaf8-c1c6-4be7-a4b0-007b074608a4.png`: shows the same order: `Command exited with code 1`, then `Operation aborted`, then `[compaction] Compacted from 190,034 tokens`.
- Session file `/home/li/.pi/agent/sessions/--home-li-primary--/2026-05-22T17-28-30-307Z_019e50bb-4363-71a6-aab3-118240392b39.jsonl`:
  - Line 1859: assistant issued the schema-next `nix flake check ... --print-build-logs` bash tool call with `timeout: 300`; usage total was `188758` tokens.
  - Line 1860: `toolName: "bash"`, `isError: true`; output includes `schema-next-no-btree-canonical`, the `BTreeMap` doc-comment hit, and `Command exited with code 1`. No `Command timed out` or `Command aborted` text.
  - Line 1861: separate assistant message: `stopReason: "aborted"`, empty content, zero usage, `errorMessage: "Operation aborted"`.
  - Line 1862: compaction entry after the abort: `tokensBefore: 190034`, `fromHook: false`.
  - Lines 1863-1865: user asked “why did you stop?” after compaction; assistant explained it stopped at the verification failure.
- Bash tool behavior:
  - `/home/li/.local/share/criomos/pi/package/src/core/tools/bash.ts` lines 388-390: timeouts are surfaced as `Command timed out after ... seconds`.
  - Same file lines 397-399: nonzero exits are surfaced as `Command exited with code ...`.
- UI/session behavior:
  - `/home/li/.local/share/criomos/pi/package/docs/session-format.md` lines 81-100: assistant `stopReason` can be `aborted`; tool results separately carry `isError`.
  - `/home/li/.local/share/criomos/pi/package/src/modes/interactive/interactive-mode.ts` lines 2764-2770: the TUI sets aborted assistant messages to display `Operation aborted`.
  - README lines 205-221 document Escape as cancel/abort; interactive code lines 2379-2382 calls abort when Escape is pressed during streaming.
- Compaction behavior:
  - README lines 264-272 and `docs/compaction.md` lines 27-45: compaction can be manual or automatic, and automatic compaction triggers near the context limit.
  - `/home/li/.local/share/criomos/pi/package/src/core/compaction/compaction.ts` lines 219-221: threshold is `contextTokens > contextWindow - reserveTokens`.
  - `/home/li/.pi/agent/settings.json` lines 2-5: local compaction enabled, `keepRecentTokens: 20000`, `reserveTokens: 32768`.

## What I did not find

- No evidence of the bash command timeout path.
- No evidence that the compaction caused the preceding abort; the persisted order is abort first, compaction second.
- No extension hook found in local Pi packages that would obviously abort on a failed bash tool result.
- No safe local event log found that records the abort source or compaction reason. The JSONL compaction entry does not preserve `reason` (`manual`, `threshold`, or `overflow`).

## Recommended next actions

1. Ask the parent/user whether Escape or `/compact` was pressed around the failure. If yes, classify as user/manual abort plus subsequent compaction, not a Pi bug.
2. If not, open a Pi bug/regression with sanitized session evidence from lines 1859-1862: failed bash result followed by zero-usage aborted assistant before compaction.
3. Reproduce with JSON/RPC event logging so `compaction_start.reason`, `agent_end.willRetry`, and abort source are captured.
4. Continue the original audit from the real failure: schema-next `no-btree-canonical` failed because it matched `BTreeMap` in a doc comment; decide false-positive versus invariant violation.
