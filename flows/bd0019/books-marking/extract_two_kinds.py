#!/usr/bin/env python3
# Copies «Two kinds of output» verbatim from 6997eb's transcript: the lines between the
# <!-- to-the-living:start --> and <!-- to-the-living:end --> marker lines, markers excluded.
import json, hashlib
F = "/home/li/.claude/projects/-home-li-primary/6997eb8a-30eb-49a1-a787-45279164a43b.jsonl"
LINE, UUID = 844, "43f51a8b-658e-4aeb-a9d7-6d87d42b6ec1"
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
assert len(s) == 1 and len(e) == 1 and s[0] < e[0], (s, e)   # markers each on a line of their own, once
body = "\n".join(lines[s[0] + 1:e[0]])
assert body.startswith("```yaml\ntitle: Two kinds of output\n```\n"), body[:60]
open("source-two-kinds.md", "w").write(body)
print("record", LINE, UUID, "timestamp", r.get("timestamp"))
print("marker lines", s[0] + 1, e[0] + 1, "of", len(lines))
print("sha256", hashlib.sha256(body.encode()).hexdigest(), "chars", len(body))
