#!/usr/bin/env python3
# Copies «The cluster never blocks itself» verbatim from Psyche Opus fe945a's transcript: the lines
# between the to-the-living marker lines, markers excluded. The first line is the metadata line, stripped at build.
import json, hashlib
F = "/home/li/.claude/projects/-home-li-primary/fe945a2e-c785-4af4-9a46-766b6ea512e8.jsonl"
LINE, UUID = 855, "b942a2f7-61af-4580-9d74-1c42bc22d05e"
START, END = "<!-- to-the-living:start -->", "<!-- to-the-living:end -->"
with open(F) as f:
    for i, l in enumerate(f, 1):
        if i == LINE:
            r = json.loads(l); break
assert r["uuid"] == UUID and r["type"] == "assistant", (r["uuid"], r["type"])
text = "".join(c["text"] for c in r["message"]["content"] if c.get("type") == "text")
lines = text.split("\n")
s = [i for i, x in enumerate(lines) if x == START]
e = [i for i, x in enumerate(lines) if x == END]
assert len(s) == 1 and len(e) == 1 and s[0] < e[0], (s, e)
body = "\n".join(lines[s[0] + 1:e[0]])
assert body.startswith("`Presentation.{ «The cluster never blocks itself» }`\n"), body[:80]
assert "```" not in body and "mermaid" not in body.lower()
open("source.md", "w").write(body)
print("record", LINE, UUID, r.get("timestamp"), "marker lines", s[0]+1, e[0]+1, "of", len(lines))
print("sha256", hashlib.sha256(body.encode()).hexdigest(), "chars", len(body))
