#!/usr/bin/env python3
# Copies «Hooks, graphs and the book maker» verbatim from Psyche Opus fe945a's transcript: the lines between
# the to-the-living marker lines, markers excluded. First line is the metadata line `Book.«…»`.
import json, hashlib
F = "/home/li/.claude/projects/-home-li-primary/fe945a2e-c785-4af4-9a46-766b6ea512e8.jsonl"
LINE, UUID = 1121, "5bf7bef0-8a5c-4264-8258-e75a81f4c09b"
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
assert body.startswith("`Book.«Hooks, graphs and the book maker»`\n"), body[:80]
open("source.md", "w").write(body)
print("record", LINE, UUID, "timestamp", r.get("timestamp"))
print("marker lines", s[0] + 1, e[0] + 1, "of", len(lines))
print("sha256", hashlib.sha256(body.encode()).hexdigest(), "chars", len(body))
