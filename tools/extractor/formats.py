from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class Block:
    id: int
    kind: str
    speaker: str
    text: str
    timestamp: str | None
    line: int
    byte_start: int
    byte_end: int
    mandatory: bool = False


@dataclass(frozen=True)
class Rollout:
    path: Path
    harness: str
    session_id: str
    blocks: list[Block]


def _texts(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if not isinstance(value, list):
        return []
    found: list[str] = []
    for item in value:
        if isinstance(item, str):
            found.append(item)
        elif isinstance(item, dict):
            text = item.get("text") or item.get("thinking")
            if isinstance(text, str) and text:
                found.append(text)
            elif item.get("type") in {"tool_use", "tool_result"}:
                found.append(json.dumps(item, ensure_ascii=False, sort_keys=True))
    return found


def _codex_block(obj: dict[str, Any]) -> tuple[str, str, str, bool] | None:
    payload = obj.get("payload") or {}
    typ = obj.get("type")
    if typ == "response_item":
        ptype = payload.get("type")
        if ptype == "message":
            role = str(payload.get("role", "unknown"))
            text = "\n\n".join(_texts(payload.get("content")))
            if not text:
                return None
            mandatory = role == "user"
            return ("psyche" if role == "user" else "machine", role, text, mandatory)
        if ptype in {"function_call", "custom_tool_call"}:
            body = {k: payload.get(k) for k in ("name", "arguments", "input") if payload.get(k) is not None}
            return ("machine-action", "machine", json.dumps(body, ensure_ascii=False, sort_keys=True), False)
        if ptype in {"function_call_output", "custom_tool_call_output"}:
            text = payload.get("output")
            if isinstance(text, str) and text:
                return ("tool-result", "tool", text, False)
    if typ == "inter_agent_communication_metadata":
        return ("communication", "flow", json.dumps(payload, ensure_ascii=False, sort_keys=True), True)
    return None


def _claude_block(obj: dict[str, Any]) -> tuple[str, str, str, bool] | None:
    typ = obj.get("type")
    if typ not in {"user", "assistant"}:
        return None
    message = obj.get("message") or {}
    role = str(message.get("role") or typ)
    pieces = _texts(message.get("content"))
    if not pieces:
        return None
    text = "\n\n".join(pieces)
    is_user = role == "user"
    # Tool results are harness observations, while typed user text is psyche.
    tool_only = isinstance(message.get("content"), list) and all(
        isinstance(item, dict) and item.get("type") == "tool_result"
        for item in message["content"]
    )
    if tool_only:
        return ("tool-result", "tool", text, False)
    return ("psyche" if is_user else "machine", role, text, is_user)


def read_rollout(path: Path) -> Rollout:
    blocks: list[Block] = []
    session_id = ""
    harness = "codex" if "/.codex/" in str(path) or path.name.startswith("rollout-") else "claude"
    offset = 0
    with path.open("rb") as source:
        for line_no, raw in enumerate(source, 1):
            start = offset
            offset += len(raw)
            try:
                obj = json.loads(raw)
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            if harness == "codex" and obj.get("type") == "session_meta":
                payload = obj.get("payload") or {}
                session_id = str(payload.get("session_id") or payload.get("id") or session_id)
            session_id = session_id or str(obj.get("sessionId") or "")
            parsed = _codex_block(obj) if harness == "codex" else _claude_block(obj)
            if not parsed:
                continue
            kind, speaker, text, mandatory = parsed
            blocks.append(Block(len(blocks), kind, speaker, text, obj.get("timestamp"), line_no, start, offset, mandatory))
    if not session_id:
        match = re.search(r"([0-9a-f]{8}-[0-9a-f-]{27,})", path.name)
        session_id = match.group(1) if match else path.stem
    return Rollout(path.resolve(), harness, session_id, blocks)


def chunks(blocks: Iterable[Block], max_chars: int) -> Iterable[list[Block]]:
    chunk: list[Block] = []
    used = 0
    for block in blocks:
        preview_size = min(len(block.text), 12_000) + 300
        if chunk and used + preview_size > max_chars:
            yield chunk
            chunk, used = [], 0
        chunk.append(block)
        used += preview_size
    if chunk:
        yield chunk
