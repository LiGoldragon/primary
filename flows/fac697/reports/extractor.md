# Job 3 — transcript extractor

## Delivered

`tools/extractor/` now reads Codex and Claude JSONL rollouts into typed raw blocks with exact source provenance. It sends bounded previews to `gpt-5.6-luna` for conservative relevance selection and narration, then copies selected text from the source itself. The model never rewrites the quoted source. User/psyche blocks and Codex or Claude inter-flow communications are mandatory even when Luna omits them.

Each extract records the harness, session UUID, source path and SHA-256, focus, JSONL line, byte interval, timestamp, speaker, raw text, and any separately labelled STT correction with its internal evidence. Corrections retain the original. Before writing into the tracked primary repository, the renderer rejects selected blocks that match common credential forms; rejection keeps the rollout in place and makes archival impossible.

The CLI provides `identify`, `inventory`, `extract`, and `archive`. Archival is a separate fail-closed action. The five named role UUIDs are permanently protected in code. Current Codex and Claude session IDs from the harness environment are added automatically, and the default refuses any rollout modified within 24 hours. At archive time it also rechecks open file descriptors under `/proc`, explicit protections, active Claude descendants, source stability while hashing, the extract's matching source digest, and destination absence. It then uses an atomic same-filesystem rename to `~/.archive/transcripts/`; it does not delete the preserved original bytes.

## Scale and protection

The complete inventory currently contains 4,798 JSONLs and 10,057,183,585 bytes when Claude descendant sessions are included. Treating all stored bytes as input gives a deliberately conservative upper bound of about 2.51 billion input tokens. Main rollouts alone currently number 2,837 and occupy 9,030,089,519 bytes, an upper bound of about 2.26 billion input tokens.

No bulk extraction or archival ran while scope was unresolved. The five named Codex role sessions remain protected. The current primary Psyche opus `da1e3f9d-857f-49ab-8c6f-3aa0a9db826b`, the active fac697 Codex threads discovered through `/proc`, and Flow POC `01a0b08b-1950-7ee1-92e8-0c5562869d29` also remain in place. The Flow owner confirmed that POC rollout still needed protection while its artifacts were salvaged.

## Witnesses

Seven unit tests pass. They witness Codex source provenance and mandatory psyche retention, mandatory Claude communication retention, rejection without a matching digest, rejection of an explicitly protected source, permanent refusal of a named role session, an atomic move only after digest attestation, and credential-pattern detection. Python compilation also passes.

A bounded Luna extraction of stale Claude session `1af9e036-e89d-4a07-bbb7-5fd59955131a` completed in about six seconds. It selected the psyche block and omitted one mechanical block. The resulting extract is `flows/fac697/reports/extract-1af9e036-e89d-4a07-bbb7-5fd59955131a.md`.

The archive CLI returned `{"source":"/home/li/.claude/projects/-home-li-primary-flows/1af9e036-e89d-4a07-bbb7-5fd59955131a.jsonl","archive":"/home/li/.archive/transcripts/.claude/projects/-home-li-primary-flows/1af9e036-e89d-4a07-bbb7-5fd59955131a.jsonl","extract":"/home/li/primary/flows/fac697/reports/extract-1af9e036-e89d-4a07-bbb7-5fd59955131a.md"}`. The live source path is absent, the archive path is present, and the archived SHA-256 is `9dac3aa013ba47e95021aafc5b73c8b39d38384766e6a080e15fd922e530dd2d`, exactly matching the extract receipt. The original bytes are preserved in the archive.

## Remaining batch decision

Historical processing needs an explicit bounded policy because the discovered corpus is orders of magnitude larger than a small background cleanup. A safe first batch is completed, inactive rollouts from a recent time window whose flow identity resolves unambiguously and whose Claude descendants are also inactive. Sessions with no unambiguous flow identity need a routing policy before their extracts can satisfy `flows/<flow-id>/reports/extract-<uuid>.md`.

## Sources

- Psyche transcript-extraction vision: `flows/6cc91b/vision/transcriptExtraction.md`.
- Job brief: `flows/da1e3f/reports/codex-brief-tools.md`.
- Implementation: `tools/extractor/`.
- Live corpus inventory observed through `tools/extractor/extractor.py inventory` on 2026-09-17.
- Luna smoke extract: `flows/fac697/reports/extract-1af9e036-e89d-4a07-bbb7-5fd59955131a.md`.
