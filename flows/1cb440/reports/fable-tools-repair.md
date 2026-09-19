# Psyche Fable tool incident and retirement witness

## Method

Field Terra read the protected Claude transcript, controller source, native
agent registry, and the original Herdr pane. It then ran the bounded
same-UUID recovery authorized before the living's later correction. After the
living declared the UUID corrupted, Field Terra stopped the exact foreground
process and removed the Claude session without further prompting or resuming
it.

## Witnessed result

- UUID `1b851735-82cd-41ed-ab5b-28bd23dc19ed` was removed by `claude rm
  1b851735`, which returned `removed 1b851735`.
- Its original Herdr route `messaging-build/wD:p2`, terminal
  `term_65bdacdde8e1d2c`, has foreground process `zsh` (PID `817153`), not
  Claude.
- `claude agents --json` contained no entry for that UUID after removal.
- No Hacky Messenger registration was created for Flow `1b8517`; it has no
  active route and must be treated as invalid rather than reused.
- The retained, inactive transcript is
  `/home/li/.claude/projects/-home-li-primary/1b851735-82cd-41ed-ab5b-28bd23dc19ed.jsonl`.
  At the post-removal witness it was 810679 bytes with SHA-256
  `d08d181bbf17dc8f3e0f307ceba176a0f284be28a4ac45f252af33e100dd247f`.

## Earlier bounded witness, superseded for operation

Before the correction, the same UUID persisted a real structured Claude
`Bash` tool call and matching successful `tool_result` for
`FABLE_TOOL_RESTORE_OK`. This showed that `--tools default` restored the tool
binding. It is evidence of the defect and repair surface only; the living's
later instruction prohibits running or reusing this corrupted UUID.

## Controller repair

`tools/claude-bootstrap-controller.py` now makes a same-UUID continuation
foreground with the explicit built-in `default` tool set, without the empty
tool list, strict empty MCP configuration, or bootstrap guard. Its fixture
test passed after the change. Commit: `b0b4b6e8a889` (`Restore Claude tools on
continuation`), pushed on `main`.

## Sources

- `tools/claude-bootstrap-controller.py`
- `tools/claude-bootstrap-controller.test.py`
- `/home/li/.claude/projects/-home-li-primary/1b851735-82cd-41ed-ab5b-28bd23dc19ed.jsonl`
- `claude rm 1b851735` result
- `herdr --session messaging-build pane process-info --pane wD:p2` result
