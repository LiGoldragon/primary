#!/usr/bin/env python3
# Copies «Illustrated flowcharts, and vision becoming skill» verbatim from Psyche Opus fe945a's transcript: the lines between
# the to-the-living marker lines, markers excluded. First line is the metadata line `Book.«…»`.
import json, hashlib
F = "/home/li/.claude/projects/-home-li-primary/fe945a2e-c785-4af4-9a46-766b6ea512e8.jsonl"
LINE, UUID = 1176, "83222d01-a8a7-4490-aa65-470fbfcd2e86"
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
assert body.startswith("`Book.«Illustrated flowcharts, and vision becoming skill»`\n"), body[:80]
open("source.md", "w").write(body)
print("record", LINE, UUID, "timestamp", r.get("timestamp"))
print("marker lines", s[0] + 1, e[0] + 1, "of", len(lines))
print("sha256", hashlib.sha256(body.encode()).hexdigest(), "chars", len(body))
