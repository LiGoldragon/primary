#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


SCRIPT = Path(__file__).with_name("check-handoff.py")
SKILLS = ("spirit", "psyche", "behavior", "correction", "vocabulary", "testing", "psyche-interraction", "main-flow", "edit-coordination")


def entry(title: str, source: Path) -> dict:
    data = source.read_bytes()
    return {"title": title, "path": str(source.resolve()), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


with tempfile.TemporaryDirectory() as temporary:
    root = Path(temporary) / "primary"
    (root / "Vision").mkdir(parents=True)
    (root / "Intent").mkdir()
    (root / "Vision" / "whole.md").write_text("whole Vision")
    (root / "Intent" / "whole.md").write_text("whole Intent")
    sources = [root / "Vision" / "whole.md", root / "Intent" / "whole.md"]
    for skill in SKILLS:
        source = root / ".claude" / "skills" / skill / "SKILL.md"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(f"whole {skill}")
        sources.append(source)
    manifest = [entry("fixture", source) for source in sources]
    system = Path(temporary) / "system-prompt.md"
    user = Path(temporary) / "user-prompt.md"
    result = Path(temporary) / "result.json"
    system.write_text("# Primary system prompt for successor\n" + "\n".join(source.read_text() for source in sources))
    user.write_text("# Original continuation context for successor\n\n## Exact source coverage manifest\n\n" + json.dumps(manifest, indent=2))
    completed = subprocess.run([sys.executable, str(SCRIPT), "--system-prompt", str(system), "--user-prompt", str(user), "--primary-root", str(root), "--expected-successor", "successor", "--output", str(result)], capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr + completed.stdout
    assert json.loads(result.read_text())["ok"] is True
print("flow workbench handoff verifier fixture passed")
