# Transcript extractor

`extractor.py` turns a Codex or Claude JSONL rollout into a narrated sequence of source-addressable raw blocks. Luna decides what remains potentially useful for the requested focus. The renderer, rather than the model, copies every selected block from the source and records the session UUID, timestamp, JSONL line, byte interval, path, and source digest.

Psyche/user input and inter-flow communications are mandatory. Luna may suggest an STT repair only with evidence from the flow; the output retains the original beside any correction.

Before writing, the renderer rejects selected blocks that match common credential forms. The original remains in place and archival remains impossible until the sensitive material receives an explicitly designed destination.

```sh
python3 tools/extractor/extractor.py extract SOURCE flows/FLOW/reports/extract-UUID.md \
  --focus 'decisions and communications relevant to the requesting flow'
```

Inventory before a batch. Claude descendant sessions are included by default. The estimate is deliberately conservative and assumes the full stored bytes become model input; actual candidate previews are capped per block.

```sh
python3 tools/extractor/extractor.py inventory
```

Archival is a separate fail-closed operation. The five permanent Codex role UUIDs and the current harness session IDs are protected in code. The default also refuses any rollout modified in the last 24 hours, an open rollout or active Claude descendant, an explicitly protected rollout, an absent/empty extract, or an extract whose digest no longer matches the source.

```sh
python3 tools/extractor/extractor.py archive SOURCE EXTRACT \
  --protect /path/to/live-rollout.jsonl
```

Originals move under `~/.archive/transcripts/` with their home-relative directory structure. Nothing is deleted.
