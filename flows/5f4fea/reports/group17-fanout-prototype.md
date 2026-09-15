# Group 17 fanout prototype

Status: proposal and offline planner only. No hook, configuration, endpoint
connection, or live fanout was installed or used.

## 1. Witnesses read before the prototype

- OpenAI's current [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
  says user-level `notify` is an array command and that Codex supplies it a
  JSON payload. The reference does not define that payload's fields. This is a
  documentation limit, not an inferred payload contract.
- Anthropic's current [Hooks reference](https://code.claude.com/docs/en/hooks)
  documents `Stop` input including `session_id`, `transcript_path`,
  `stop_hook_active`, and `last_assistant_message`. It says the final message
  is not guaranteed to be in the transcript at Stop time, so a future Stop
  consumer must not assume a transcript lookup contains that just-finished
  assistant message.
- `tools/prompt-relay` was read locally. Its Codex route opens the app-server
  WebSocket and sends provenance followed by selected raw text; its Claude
  route reads `claude agents --json`, refuses unless exactly one matching
  session is `idle`, then attaches to the discovered control socket. The
  existing durable fixture covers both routes and the busy/ambiguous Claude
  refusals.
- Local `claude agents --json` was read on 2026-09-15. It returned one
  `busy` session (`05c6048e`); no attach or delivery was attempted. This is a
  point-in-time local observation, not a claim that the session remains busy.

## 2. Prototype

`tools/prompt-fanout` has only `plan`. It reads one specified transcript once,
selects exactly one unmarked human record by six-character head/tail and an
optional source message ID, freezes its UTF-8 bytes in one buffer, and creates
one plan entry per explicit endpoint. It never discovers, opens, or writes an
endpoint. Its receipt deliberately excludes prompt text.

The planner requires both `--endpoint` and `--body-mode whole|receipt`.
Consequently it makes neither a default-endpoint ruling nor a whole-versus-
receipt ruling. `whole` and `receipt` are accepted labels for a reviewed caller
to choose; this prototype does not implement either delivery format.

The input surface, expressed as a prospective positional Datom value, is:

```text
Plan.{ «/absolute/transcript.jsonl» «Head..Tail» Some.«source-message-id» Whole [ «codex:thread-id@/unruled/codex.sock» «claude:session-id@/unruled/claude.sock» ] }
```

`Plan`, `Some`, and `Whole` are proposal vocabulary only; no Ethos or Signal
contract is asserted by this example.

## 3. Same-bytes witness

The offline fixture injects a counting reader and asserts exactly one source
read; then it asserts both plan endpoints retain the same `Buffer` object as
the selected payload. The asserted SHA-256 is an independently written fixture
value, and the CLI receipt identifies the selected transcript message ID and
byte count without reprinting prompt text.

## 4. Installation, deferred

After owners rule the Codex JSON payload schema, endpoint ownership, and body
mode, installation would consist of placing a reviewed delivery adapter outside
the planner, configuring the user-level Codex notification command and/or a
Claude Stop hook to invoke that adapter, and supplying explicit endpoint
configuration. Nothing in this branch performs those steps: it neither edits
Codex/Claude settings nor adds a hook, and it leaves both default endpoint and
whole-versus-receipt decisions open.

## 5. Minimal provenance

This report was prepared in isolated JJ workspace
`/home/li/wt/github.com/LiGoldragon/primary/group-17-5f4fea`, based on
committed parent `b494b1c3`. The proposed files are `tools/prompt-fanout`,
`tools/prompt-fanout-core.mjs`, and `tools/prompt-fanout.test.mjs`; their Nix
check is `prompt-fanout-fixtures`. No primary-flow log or `flows/index.md` was
read for mutation or modified.

## 6. Existing durable-fixture failure, report only

The pre-existing `prompt-relay-fixtures` Nix check remains reported as an
unresolved historical timeout: `flows/34d94e/log.md` records exit 124 after
180 seconds during dependency-cache downloads. This prototype neither changes
that check nor recasts the failure as a pass. The narrower local Node relay
fixture was green in this workspace; that does not establish the historical
Nix gate as green.
