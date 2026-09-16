#!/usr/bin/env python3
"""Build a hash-checked developer-role startup packet from private sources."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_path(source: dict[str, str], workspace: Path, curriculum: Path) -> Path:
    root = curriculum if source["root"] == "curriculum" else workspace
    return root / source["path"]


def render_source(source: dict[str, str], text: str) -> str:
    metadata = (
        f'kind="{source["kind"]}" logical-path="{source["path"]}" '
        f'sha256="{source["sha256"]}"'
    )
    if source["kind"] == "skill":
        return (
            f"<startup-source {metadata} injection-role=\"developer\">\n"
            "This is a copied authored body in developer-role text. It is not a native skill load.\n"
            f'<skill name="{source["name"]}" location="{source["path"]}">\n'
            f"{text.rstrip()}\n</skill>\n</startup-source>\n"
        )
    status = source.get("status", "reviewed source")
    return (
        f"<startup-source {metadata} status=\"{status}\" injection-role=\"developer\">\n"
        f"{text.rstrip()}\n</startup-source>\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-root", required=True, type=Path)
    parser.add_argument("--curriculum-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    manifest = json.loads((HERE / "manifest.json").read_text())
    rendered = [
        "# Private startup developer packet",
        "",
        "Injection surface: thread/start.developerInstructions.",
        "This packet supplements native Codex instructions; do not pass it as baseInstructions.",
        "Every copied body below is developer-role text, not a system role or a native skill load.",
        "",
    ]
    for source in manifest["sources"]:
        path = source_path(source, args.workspace_root, args.curriculum_root)
        if not path.is_file():
            raise SystemExit(f"missing source: {path}")
        actual = digest(path)
        if actual != source["sha256"]:
            raise SystemExit(f"digest mismatch for {path}: expected {source['sha256']}, got {actual}")
        rendered.append(render_source(source, path.read_text()))
    args.output.write_text("\n".join(rendered))


if __name__ == "__main__":
    main()
