from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from formats import Block


SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["items"],
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["id", "narration", "corrected_text", "correction_evidence"],
                "properties": {
                    "id": {"type": "integer"},
                    "narration": {"type": "string"},
                    "corrected_text": {"type": ["string", "null"]},
                    "correction_evidence": {"type": ["string", "null"]},
                },
            },
        }
    },
}


def _prompt(blocks: list[Block], focus: str) -> str:
    candidates = []
    for block in blocks:
        text = block.text
        if len(text) > 12_000:
            text = text[:6_000] + "\n[preview elides middle]\n" + text[-6_000:]
        candidates.append({
            "id": block.id,
            "kind": block.kind,
            "speaker": block.speaker,
            "mandatory": block.mandatory,
            "timestamp": block.timestamp,
            "text": text,
        })
    return f"""You are the Luna transcript extractor. Select every block that is potentially useful for understanding this flow, with conservative recall. User/psyche blocks and inter-flow communications marked mandatory must always be selected. Preserve objective disagreements, failures, decisions, discoveries, state changes, and consequential machine reasoning. Omit only mechanical noise with no plausible future value.

Write one short factual narration for each selected block explaining its place in the flow without paraphrasing the raw block. Suggest an STT correction only when the surrounding flow explicitly acknowledged it or makes the intended words unambiguous. A correction must be the complete corrected text, and correction_evidence must state the internal evidence. Never silently alter source text.

Requesting focus: {focus}

Return only the requested JSON object. Candidate blocks:
{json.dumps(candidates, ensure_ascii=False)}"""


def select_with_luna(blocks: list[Block], focus: str, model: str = "gpt-5.6-luna") -> list[dict[str, Any]]:
    with tempfile.TemporaryDirectory(prefix="transcript-extractor-") as temp:
        root = Path(temp)
        schema = root / "schema.json"
        output = root / "output.json"
        schema.write_text(json.dumps(SCHEMA), encoding="utf-8")
        command = [
            "codex", "exec", "--ephemeral", "--ignore-user-config", "--skip-git-repo-check",
            "--sandbox", "read-only", "--model", model, "--output-schema", str(schema),
            "--output-last-message", str(output), "-",
        ]
        run = subprocess.run(command, input=_prompt(blocks, focus), text=True, capture_output=True)
        if run.returncode != 0:
            raise RuntimeError(f"Luna extraction failed ({run.returncode}): {run.stderr[-2000:]}")
        try:
            result = json.loads(output.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise RuntimeError("Luna returned no valid structured extraction") from error
    items = result.get("items")
    if not isinstance(items, list):
        raise RuntimeError("Luna extraction omitted items")
    valid_ids = {block.id for block in blocks}
    selected = {item.get("id"): item for item in items if item.get("id") in valid_ids}
    for block in blocks:
        if block.mandatory and block.id not in selected:
            selected[block.id] = {
                "id": block.id,
                "narration": "A mandatory psyche or inter-flow communication block is retained verbatim.",
                "corrected_text": None,
                "correction_evidence": None,
            }
    return [selected[key] for key in sorted(selected)]
