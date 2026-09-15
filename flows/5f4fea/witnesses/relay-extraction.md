# Relay extraction provenance witness

## Method

Ran the durable transcript selector in extract-only mode; no Codex or Claude delivery was attempted:

```text
/home/li/primary/tools/prompt-relay extract \
  --source /home/li/.claude/projects/-home-li-primary/942914a6-93d5-41ba-95bf-fa98ee557b09.jsonl \
  --match "Your s..ould. " \
  --source-id 0a3c0db4-7d96-401d-a679-a693de78815a
```

The six-character match was derived directly from the source record's string content: head `Your s`, tail `ould. `.

## Exact observed result

```json
{"kind":"extracted","provenance":{"source_path":"/home/li/.claude/projects/-home-li-primary/942914a6-93d5-41ba-95bf-fa98ee557b09.jsonl","source_format":"claude","source_message_id":"0a3c0db4-7d96-401d-a679-a693de78815a","source_timestamp":"2026-09-15T17:27:47.239Z","sha256_utf8":"d19f5a5d4f9636ee577592ca646d26b445160f80e227a3e4bee8a8385ccc55d0"},"raw_text_bytes":949}
```

## Interpretation

The durable selector's canonical eligible text hash is `d19f5a5d4f9636ee577592ca646d26b445160f80e227a3e4bee8a8385ccc55d0`, matching the supplied provenance header. A separate direct hash over an intermediate `.message.content` representation (`c311b1…`, reported by another helper) is not used here because its exact serialization was not the relay tool's selected text. The source event is human-origin (`origin.kind=human`) and the selector classified it as `source_format=claude`.

This witness establishes extraction only. It has no relay turn ID; the related same-thread continuation turn is `01a0a621-49b2-72b3-b7a3-6a4ac899f8a3`, which is separate and was not created by this extract command.

## Sources

- `/home/li/primary/tools/prompt-relay`
- Source JSONL path and message ID shown in the observed result above.
