#!/usr/bin/env python3
"""Review a primary-profile prompt pair without changing the handoff."""

import argparse
import hashlib
import json
from pathlib import Path
import sys


SKILLS = (
    "spirit", "psyche", "behavior", "correction", "vocabulary", "testing",
    "psyche-interraction", "main-flow", "edit-coordination",
)
MANIFEST_HEADING = "## Exact source coverage manifest\n\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_files(path: Path) -> list[Path]:
    return sorted(item for item in path.rglob("*") if item.is_file())


def source_manifest(user_prompt: str) -> list[dict]:
    try:
        return json.loads(user_prompt.split(MANIFEST_HEADING, 1)[1])
    except (IndexError, json.JSONDecodeError) as error:
        raise ValueError("user prompt has no exact source coverage manifest") from error


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--system-prompt", required=True, type=Path)
    parser.add_argument("--user-prompt", required=True, type=Path)
    parser.add_argument("--primary-root", required=True, type=Path)
    parser.add_argument("--expected-successor", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    if not args.output.parent.is_dir():
        parser.error("output parent directory must already exist")
    system = args.system_prompt.read_text()
    user = args.user_prompt.read_text()
    entries = source_manifest(user)
    failures: list[str] = []
    expected_system = f"# Primary system prompt for {args.expected_successor}"
    expected_user = f"# Original continuation context for {args.expected_successor}"
    require(expected_system in system, "system prompt successor identity differs", failures)
    require(expected_user in user, "user prompt successor identity differs", failures)

    by_path = {entry.get("path"): entry for entry in entries if isinstance(entry, dict)}
    for entry in entries:
        source = Path(entry.get("path", ""))
        require(source.is_file(), f"manifest source is unavailable: {source}", failures)
        if source.is_file():
            require(entry.get("bytes") == source.stat().st_size, f"byte count differs: {source}", failures)
            require(entry.get("sha256") == sha256(source), f"SHA-256 differs: {source}", failures)

    root = args.primary_root.resolve()
    required = regular_files(root / "Vision") + regular_files(root / "Intent")
    required += [root / ".claude" / "skills" / skill / "SKILL.md" for skill in SKILLS]
    for source in required:
        source_path = str(source.resolve())
        require(source_path in by_path, f"required source omitted from manifest: {source_path}", failures)
        if source.is_file():
            require(source.read_text() in system, f"whole source absent from system prompt: {source_path}", failures)

    result = {
        "kind": "handoff-review",
        "reviewed_successor": args.expected_successor,
        "prototype_only": True,
        "manifest_entries": len(entries),
        "required_primary_sources": len(required),
        "ok": not failures,
        "failures": failures,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
