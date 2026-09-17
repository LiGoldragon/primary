#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

from formats import Block, chunks, read_rollout
from intelligence import select_with_luna


def fence(text: str) -> str:
    marker = "```"
    while marker in text:
        marker += "`"
    return f"{marker}text\n{text.rstrip()}\n{marker}"


def render(source, selections: dict[int, dict], focus: str) -> str:
    digest = hashlib.sha256(source.path.read_bytes()).hexdigest()
    lines = [
        f"# Transcript extract — {source.session_id}", "",
        f"- Harness: `{source.harness}`",
        f"- Source: `{source.path}`",
        f"- Source SHA-256: `{digest}`",
        f"- Focus: {focus}",
        f"- Selected blocks: {len(selections)} of {len(source.blocks)}", "",
        "The narration is interpretive. Every following raw block is copied from the source content; its line and byte interval address the original JSONL record.", "",
    ]
    for block in source.blocks:
        item = selections.get(block.id)
        if not item:
            continue
        lines.extend([
            f"## Block {block.id}: {block.kind}", "",
            item["narration"].strip(), "",
            f"Source: `{source.path}` · session `{source.session_id}` · line {block.line} · bytes {block.byte_start}..{block.byte_end} · timestamp `{block.timestamp or 'unknown'}` · speaker `{block.speaker}`", "",
            fence(block.text), "",
        ])
        corrected = item.get("corrected_text")
        evidence = item.get("correction_evidence")
        if corrected and evidence and corrected != block.text:
            lines.extend(["STT correction (original retained above):", "", fence(corrected), "", f"Evidence: {evidence}", ""])
    return "\n".join(lines).rstrip() + "\n"


def extract(args: argparse.Namespace) -> int:
    source = read_rollout(args.source)
    selected: dict[int, dict] = {}
    for group in chunks(source.blocks, args.chunk_chars):
        for item in select_with_luna(group, args.focus, args.model):
            if item["id"] in selected:
                raise RuntimeError(f"duplicate selection {item['id']}")
            selected[item["id"]] = item
    missing = [block.id for block in source.blocks if block.mandatory and block.id not in selected]
    if missing:
        raise RuntimeError(f"mandatory blocks missing: {missing}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(render(source, selected, args.focus), encoding="utf-8")
    os.replace(temporary, args.output)
    print(json.dumps({"session_id": source.session_id, "blocks": len(source.blocks), "selected": len(selected), "output": str(args.output)}))
    return 0


def open_rollouts() -> set[Path]:
    found: set[Path] = set()
    proc = Path("/proc")
    for pid in proc.iterdir():
        if not pid.name.isdigit():
            continue
        fd_root = pid / "fd"
        try:
            fds = list(fd_root.iterdir())
        except OSError:
            continue
        for fd in fds:
            try:
                target = fd.resolve(strict=True)
            except OSError:
                continue
            if target.suffix == ".jsonl" and ("/.codex/sessions/" in str(target) or "/.claude/projects/" in str(target)):
                found.add(target)
    return found


def inventory(args: argparse.Namespace) -> int:
    roots = [Path.home() / ".codex/sessions", Path.home() / ".claude/projects"]
    active = open_rollouts()
    records = []
    for root in roots:
        for path in root.rglob("*.jsonl"):
            if "/subagents/" in str(path) and not args.include_subagents:
                continue
            stat = path.stat()
            records.append({"path": str(path), "bytes": stat.st_size, "active": path.resolve() in active})
    result = {
        "rollouts": len(records),
        "bytes": sum(item["bytes"] for item in records),
        "estimated_input_tokens_at_full_text": sum(item["bytes"] for item in records) // 4,
        "active": [item["path"] for item in records if item["active"]],
        "records": records if args.verbose else None,
    }
    print(json.dumps(result, indent=2))
    return 0


def archive(args: argparse.Namespace) -> int:
    source = args.source.resolve()
    protected = {Path(item).resolve() for item in args.protect}
    if source in protected or source in open_rollouts():
        raise RuntimeError(f"refusing to archive active or protected rollout: {source}")
    if not args.extract.is_file() or args.extract.stat().st_size == 0:
        raise RuntimeError("refusing to archive without a non-empty extract")
    expected = hashlib.sha256(source.read_bytes()).hexdigest()
    if f"`{expected}`" not in args.extract.read_text(encoding="utf-8"):
        raise RuntimeError("extract does not attest the current source digest")
    try:
        relative = source.relative_to(Path.home())
    except ValueError:
        relative = source.relative_to(source.anchor)
    destination = args.archive_root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise RuntimeError(f"archive destination exists: {destination}")
    shutil.move(source, destination)
    print(json.dumps({"source": str(source), "archive": str(destination), "extract": str(args.extract)}))
    return 0


def _safe_flow_id(value: str) -> bool:
    return len(value) == 6 and all(character in "0123456789abcdef" for character in value)


def infer_flow_id(source) -> str | None:
    candidates: list[str] = []
    for block in source.blocks[:80]:
        text = block.text
        for marker in ("FLOW_ID=", "Flow ID: ", "flow-id ", "/flows/"):
            start = 0
            while True:
                offset = text.find(marker, start)
                if offset < 0:
                    break
                tail = text[offset + len(marker):].lstrip("`'\" ")
                candidate = tail[:6].lower()
                if _safe_flow_id(candidate):
                    candidates.append(candidate)
                start = offset + len(marker)
    if candidates:
        # Earliest explicit flow identity wins; later text often mentions other flows.
        return candidates[0]
    session_prefix = source.session_id[:6].lower()
    flow_path = Path("/home/li/primary/flows") / session_prefix
    return session_prefix if _safe_flow_id(session_prefix) and flow_path.is_dir() else None


def identify(args: argparse.Namespace) -> int:
    source = read_rollout(args.source)
    print(json.dumps({
        "session_id": source.session_id,
        "harness": source.harness,
        "flow_id": infer_flow_id(source),
        "blocks": len(source.blocks),
        "bytes": source.path.stat().st_size,
    }))
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Intelligent, source-addressable rollout extraction")
    sub = root.add_subparsers(dest="command", required=True)
    one = sub.add_parser("extract")
    one.add_argument("source", type=Path)
    one.add_argument("output", type=Path)
    one.add_argument("--focus", default="general understanding of the flow")
    one.add_argument("--model", default="gpt-5.6-luna")
    one.add_argument("--chunk-chars", type=int, default=75_000)
    one.set_defaults(run=extract)
    inv = sub.add_parser("inventory")
    inv.add_argument("--include-subagents", action="store_true")
    inv.add_argument("--verbose", action="store_true")
    inv.set_defaults(run=inventory)
    ident = sub.add_parser("identify")
    ident.add_argument("source", type=Path)
    ident.set_defaults(run=identify)
    arc = sub.add_parser("archive")
    arc.add_argument("source", type=Path)
    arc.add_argument("extract", type=Path)
    arc.add_argument("--archive-root", type=Path, default=Path.home() / ".archive/transcripts")
    arc.add_argument("--protect", action="append", default=[])
    arc.set_defaults(run=archive)
    return root


if __name__ == "__main__":
    try:
        arguments = parser().parse_args()
        sys.exit(arguments.run(arguments))
    except (OSError, RuntimeError, ValueError) as error:
        print(f"extractor: {error}", file=sys.stderr)
        sys.exit(1)
