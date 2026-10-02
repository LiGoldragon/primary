#!/usr/bin/env python3
# Copies «Handling skills» verbatim from Psyche Fable 6997eb's transcript: lines between its to-the-living markers,
# marker lines and the Presentation.{ } datom line excluded.
import json, hashlib
F = "/home/li/.claude/projects/-home-li-primary/6997eb8a-30eb-49a1-a787-45279164a43b.jsonl"
LINE, UUID = 2463, "6b5b3514-62e7-4393-9af4-bc2ccd8694ed"
START, END = "<!-- to-the-living:start -->", "<!-- to-the-living:end -->"
with open(F) as f:
    for i, l in enumerate(f, 1):
        if i == LINE: r = json.loads(l); break
assert r["uuid"] == UUID and r["type"] == "assistant"
text = "".join(c["text"] for c in r["message"]["content"] if c.get("type") == "text")
lines = text.split("\n")
s = [i for i, x in enumerate(lines) if x == START]; e = [i for i, x in enumerate(lines) if x == END]
assert len(s) == 2 and len(e) == 2
a, b = s[0], e[0]
assert lines[a+1] == "Presentation.{ «Handling skills» }"
body = "\n".join(lines[a+2:b])
open("source.md", "w").write(body)
print("record", LINE, UUID, r.get("timestamp"), "marker lines", a+1, b+1, "sha256", hashlib.sha256(body.encode()).hexdigest(), len(body))
